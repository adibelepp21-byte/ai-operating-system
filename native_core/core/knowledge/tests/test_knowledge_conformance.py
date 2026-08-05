"""
Knowledge conformance tests (Blueprint §12/§26/§27; knowledge_spec §1–§14;
Roadmap §9.5; Freeze §4/§5 layer 8; INV-7/INV-8/INV-12; OQ-2; PR-3/PR-4).

Baseline 04A — a **verification** baseline. It verifies the existing structure
of the Knowledge boundary and introduces no behavior. Roadmap §9.5 fixes this
boundary's completion as *"no unguided write path; INV-8 test passes."*

Each test asserts one ratified requirement, or one boundary rule the
specification states:

  - INV-8  — entry only via governed promotion. Every public admission entry
             point requires a Governance authorization surface; there is no
             unguided write path.
  - INV-7  — durable and versioned. Versions are immutable, deeply frozen, and
             carry no status field (status is derived); nothing deletes.
  - INV-12 — no external dependency. Cross-boundary imports are limited to the
             three knowledge_spec §7 permits.
  - OQ-2   — authors no Trace; imports nothing from Trace.
  - PR-3   — decides nothing; Governance holds authority.
  - PR-4   — fails closed; every halt is a KnowledgeError.

Verification is structural (AST, dataclass, signature, public-API inspection)
in preference to runtime simulation.

**No source file is modified by this suite.** Findings are reported as evidence.

Standard-library `unittest` only.
Run: python -m unittest native_core.core.knowledge.tests.test_knowledge_conformance
"""

from __future__ import annotations

import ast
import inspect
import sys
import unittest
from dataclasses import fields, is_dataclass
from pathlib import Path

from native_core.core import knowledge as knowledge_pkg
from native_core.core.knowledge import (
    CanonicalStatus,
    InvalidKnowledgeVersion,
    KnowledgeAdmission,
    KnowledgeError,
    KnowledgeRepository,
    KnowledgeRetrieval,
    KnowledgeStorageUnavailable,
    KnowledgeStore,
    KnowledgeVersion,
    KnowledgeVersioning,
    UnauthorizedPromotion,
    VersionIdentity,
    VersionNotFound,
)

PACKAGE = Path(knowledge_pkg.__file__).parent


def _modules():
    """Every non-test source module of this boundary."""
    return sorted(p for p in PACKAGE.rglob("*.py") if "tests" not in p.parts)


def _imports(path):
    """(module, level) for every import in one module."""
    found = []
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, ast.Import):
            found += [(a.name, 0) for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            found.append((node.module or "", node.level or 0))
    return found


def _definitions():
    """(filename, node) for every class and function defined in the boundary."""
    for path in _modules():
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                yield path.name, node


class TestInv8EntryOnlyViaGovernedPromotion(unittest.TestCase):
    """INV-8 — Knowledge is entered only through governed review.

    Roadmap §9.5 completion criterion: *"no unguided write path; INV-8 test
    passes."* knowledge_spec §5 [E]: Knowledge *"exposes **no** capability to be
    written outside governed promotion."*"""

    ADMISSION_ENTRY_POINTS = ("admit", "revise")

    def test_every_admission_entry_point_requires_an_authorization_argument(self):
        """Structural: no admission signature exists without authorization."""
        for name in self.ADMISSION_ENTRY_POINTS:
            method = getattr(KnowledgeAdmission, name)
            params = list(inspect.signature(method).parameters)
            self.assertIn(
                "authorization",
                params,
                f"KnowledgeAdmission.{name} must require an authorization surface",
            )

    def test_admission_entry_points_are_abstract_on_the_contract(self):
        """The contract declares; it does not admit. Behavior belongs to a
        realization, which must still carry the authorization parameter."""
        for name in self.ADMISSION_ENTRY_POINTS:
            self.assertIn(name, KnowledgeAdmission.__abstractmethods__)

    def test_admission_contract_cannot_be_instantiated(self):
        """An abstract admission contract cannot itself admit anything."""
        with self.assertRaises(TypeError):
            KnowledgeAdmission()

    def test_no_public_module_level_write_function_exists(self):
        """No unguided write path: nothing at module scope admits or writes.

        `create` is deliberately **not** a write verb here. A module-level
        `create_*` factory is a composition root — it wires collaborators by
        constructor injection and admits nothing. The ratified precedent is
        `create_execution_layer` in `core/runtime/execution/composition.py`.
        Including it produced a false positive on
        `composition.create_knowledge_subsystem`."""
        write_verbs = ("admit", "write", "store", "save", "insert", "put")
        offences = []
        for path in _modules():
            for node in ast.parse(path.read_text()).body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    lowered = node.name.lstrip("_").lower()
                    if any(lowered.startswith(v) for v in write_verbs):
                        offences.append((path.name, node.name))
        self.assertEqual(offences, [])

    def test_unauthorized_promotion_is_a_declared_halt(self):
        """PR-4: the absence of authorization has a named, fail-closed halt."""
        self.assertTrue(issubclass(UnauthorizedPromotion, KnowledgeError))

    def test_knowledge_holds_no_authority_surface(self):
        """PR-3 / §6.2 invariant 2: Governance decides; Knowledge records.

        Exceptions are excluded from the check. `UnauthorizedPromotion` names
        the *absence* of authority and is the fail-closed halt that enforces
        INV-8 — matching it as an authority surface was a false positive. The
        check therefore applies to non-exception exports only."""
        non_exceptions = [
            name
            for name in knowledge_pkg.__all__
            if not (
                isinstance(getattr(knowledge_pkg, name, None), type)
                and issubclass(getattr(knowledge_pkg, name), BaseException)
            )
        ]
        surface = " ".join(non_exceptions).lower()
        for term in ("approve", "authoriz", "decide", "grant", "permit", "review"):
            self.assertNotIn(term, surface)


class TestInv7DurableAndVersioned(unittest.TestCase):
    """INV-7 — durable, versioned, not casually deleted."""

    def test_version_contracts_are_frozen(self):
        for contract in (KnowledgeVersion, VersionIdentity):
            self.assertTrue(is_dataclass(contract))
            self.assertTrue(
                contract.__dataclass_params__.frozen,
                f"{contract.__name__} must be frozen",
            )

    def test_version_is_immutable(self):
        version = KnowledgeVersion(VersionIdentity("item", 1), "content")
        with self.assertRaises(Exception):
            version.content = "other"

    def test_version_carries_no_status_field(self):
        """Phase 3.306 D2: canonical status is DERIVED, never stored.

        Storing it would require mutating an immutable prior version on
        supersession, which INV-7 forbids."""
        names = {f.name for f in fields(KnowledgeVersion)}
        self.assertEqual(names, {"identity", "content", "validity_conditions"})
        for name in names:
            self.assertNotIn("status", name.lower())

    def test_version_carries_no_forbidden_metadata(self):
        forbidden = (
            "uuid", "hash", "checksum", "signature", "timestamp", "created",
            "updated", "author", "confidence", "trust", "probability",
            "ranking", "score",
        )
        names = {f.name.lower() for f in fields(KnowledgeVersion)}
        for name in names:
            for term in forbidden:
                self.assertNotIn(term, name)

    def test_content_is_deeply_frozen(self):
        """INV-6 capture, don't reference — nested collections are immutable."""
        version = KnowledgeVersion(
            VersionIdentity("item", 1), {"a": [1, 2], "b": {"c": 3}}
        )
        with self.assertRaises(TypeError):
            version.content["a"] = "mutated"
        self.assertIsInstance(version.content["a"], tuple)

    def test_identity_is_a_governed_ordinal_pair(self):
        """Phase 3.306 D1: (knowledge_item_key, version_sequence)."""
        self.assertEqual(
            [f.name for f in fields(VersionIdentity)],
            ["knowledge_item_key", "version_sequence"],
        )

    def test_identity_rejects_malformed_input_fail_closed(self):
        for bad in (("", 1), ("   ", 1), ("item", -1), ("item", True), ("item", "1")):
            with self.assertRaises(InvalidKnowledgeVersion):
                VersionIdentity(*bad)

    def test_version_requires_identity_and_content(self):
        with self.assertRaises(InvalidKnowledgeVersion):
            KnowledgeVersion("item", "content")
        with self.assertRaises(InvalidKnowledgeVersion):
            KnowledgeVersion(VersionIdentity("item", 1), None)

    def test_no_delete_or_overwrite_surface_exists(self):
        """Not casually deleted (INV-7); superseded, never removed."""
        delete_verbs = ("delete", "remove", "drop", "purge", "erase", "overwrite")
        offences = [
            (f, n.name)
            for f, n in _definitions()
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            and any(v in n.name.lstrip("_").lower() for v in delete_verbs)
        ]
        self.assertEqual(offences, [])

    def test_canonical_status_is_binary_with_no_candidate_state(self):
        """Domain Model §6; Phase 3.289 §2 — a candidate belongs to Memory."""
        self.assertEqual(
            {m.name for m in CanonicalStatus}, {"ACTIVE", "SUPERSEDED"}
        )
        self.assertNotIn("CANDIDATE", {m.name for m in CanonicalStatus})


class TestInv12DependencyConformance(unittest.TestCase):
    """INV-12 and knowledge_spec §7/§8 — permitted dependencies only."""

    #: knowledge_spec §7 [E]: Governance (promotion authority), Memory
    #: (candidate source), and a storage facility beneath it. Nothing else.
    PERMITTED_BOUNDARIES = {"governance", "memory", "infrastructure"}
    FORBIDDEN_BOUNDARIES = {
        "trace", "runtime", "agent", "workflow", "capability", "skill",
        "optimization",
    }

    def test_no_external_dependency(self):
        """Standard library only — nothing installed, fetched, or vendored."""
        allowed = set(sys.stdlib_module_names) | {"native_core"}
        offences = [
            (p.name, m)
            for p in _modules()
            for m, level in _imports(p)
            if level == 0 and m.split(".")[0] and m.split(".")[0] not in allowed
        ]
        self.assertEqual(offences, [])

    def test_no_forbidden_boundary_import(self):
        """knowledge_spec §8: must not depend on execution or ownership layers."""
        offences = []
        for path in _modules():
            for module, level in _imports(path):
                parts = {p for p in module.split(".") if p}
                hit = parts & self.FORBIDDEN_BOUNDARIES
                if hit:
                    offences.append((path.name, module, sorted(hit)))
        self.assertEqual(offences, [])

    def test_cross_boundary_imports_are_within_the_permitted_three(self):
        """Every sibling-package import resolves to Governance, Memory, or
        Infrastructure — the three knowledge_spec §7 permits."""
        observed = set()
        for path in _modules():
            for module, level in _imports(path):
                if level == 2 and module:  # `from ..<boundary> import ...`
                    observed.add(module.split(".")[0])
        self.assertTrue(
            observed <= self.PERMITTED_BOUNDARIES,
            f"unpermitted cross-boundary imports: {sorted(observed - self.PERMITTED_BOUNDARIES)}",
        )

    def test_no_network_filesystem_or_process_access(self):
        """A facility beneath Knowledge owns storage; Knowledge owns semantics."""
        forbidden = {
            "socket", "http", "urllib", "subprocess", "shutil", "sqlite3",
            "asyncio", "threading", "pathlib", "os",
        }
        offences = [
            (p.name, m)
            for p in _modules()
            for m, level in _imports(p)
            if level == 0 and m.split(".")[0] in forbidden
        ]
        self.assertEqual(offences, [])

    def test_no_async_or_threading(self):
        offences = []
        for path in _modules():
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, (ast.AsyncFunctionDef, ast.Await)):
                    offences.append(path.name)
        self.assertEqual(offences, [])


class TestOq2AuthorsNoTrace(unittest.TestCase):
    """OQ-2 — Knowledge storage is a facility, not an independent traced actor."""

    def test_no_trace_import(self):
        offences = [
            (p.name, m)
            for p in _modules()
            for m, _ in _imports(p)
            if "trace" in {x for x in m.split(".") if x}
        ]
        self.assertEqual(offences, [])

    def test_no_trace_authoring_callable(self):
        offences = [
            (f, n.name)
            for f, n in _definitions()
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            and "trace" in n.name.lower()
        ]
        self.assertEqual(offences, [])

    def test_no_trace_field_on_any_version_contract(self):
        for contract in (KnowledgeVersion, VersionIdentity):
            for f in fields(contract):
                self.assertNotIn("trace", f.name.lower())

    def test_public_surface_names_no_trace(self):
        self.assertNotIn("trace", " ".join(knowledge_pkg.__all__).lower())


class TestPr4FailClosed(unittest.TestCase):
    """PR-4 — every halt is named, and nothing degrades silently."""

    HALTS = (
        UnauthorizedPromotion,
        InvalidKnowledgeVersion,
        VersionNotFound,
        KnowledgeStorageUnavailable,
    )

    def test_every_halt_is_a_knowledge_error(self):
        for halt in self.HALTS:
            self.assertTrue(issubclass(halt, KnowledgeError))

    def test_knowledge_error_is_a_runtime_error(self):
        self.assertTrue(issubclass(KnowledgeError, RuntimeError))

    @unittest.expectedFailure
    def test_halt_messages_are_strings(self):
        """**RECORDED FINDING F-2 — Category B. Expected to fail.**

        Five raise sites pass a *list* to `KnowledgeError` instead of a message
        string, so `str(exc)` renders as `"['...']"` rather than the message:

            admission.py:86, admission.py:88
            repository.py:95, repository.py:97
            retrieval.py:64

        Baseline 04A is a **verification** baseline: source modification is
        prohibited, so this defect is recorded rather than repaired. The test is
        marked `expectedFailure` so the suite reports the finding without
        blocking the green-suite gate. Should the source be corrected under a
        future authorization, this becomes an *unexpected success* — which is
        the intended signal to remove the marker."""
        offences = []
        for path in _modules():
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call):
                    for arg in node.exc.args:
                        if isinstance(arg, (ast.List, ast.Tuple, ast.Dict, ast.Set)):
                            offences.append((path.name, getattr(node, "lineno", "?")))
        self.assertEqual(offences, [])


class TestBoundaryStructure(unittest.TestCase):
    """Blueprint §12/§26 — contracts, isolation, and the declared public surface."""

    ABSTRACT_CONTRACTS = (
        KnowledgeAdmission,
        KnowledgeRepository,
        KnowledgeRetrieval,
        KnowledgeStore,
        KnowledgeVersioning,
    )

    def test_every_declared_contract_is_abstract(self):
        """The boundary publishes contracts; realizations are separate."""
        for contract in self.ABSTRACT_CONTRACTS:
            self.assertTrue(
                contract.__abstractmethods__,
                f"{contract.__name__} must declare abstract methods",
            )
            with self.assertRaises(TypeError):
                contract()

    def test_public_surface_is_exactly_the_declared_exports(self):
        self.assertEqual(
            set(knowledge_pkg.__all__),
            {
                "KnowledgeVersion",
                "VersionIdentity",
                "CanonicalStatus",
                "KnowledgeVersioning",
                "KnowledgeStore",
                "KnowledgeRepository",
                "KnowledgeAdmission",
                "KnowledgeRetrieval",
                "KnowledgeError",
                "UnauthorizedPromotion",
                "InvalidKnowledgeVersion",
                "VersionNotFound",
                "KnowledgeStorageUnavailable",
            },
        )

    def test_no_module_level_mutable_state(self):
        """No cache, no registry, no singleton hiding in module state.

        An UPPER_CASE name bound to an immutable literal is a constant, not
        state, and is excluded — flagging `KNOWLEDGE_PARTITION =
        "knowledge_versions"` was a false positive. Anything mutable, or any
        lower-case module-level binding, is still an offence."""
        immutable_literal = (ast.Constant,)
        offences = []
        for path in _modules():
            for node in ast.parse(path.read_text()).body:
                targets, value = [], None
                if isinstance(node, ast.Assign):
                    targets, value = node.targets, node.value
                elif isinstance(node, ast.AnnAssign):
                    targets, value = [node.target], node.value
                for target in targets:
                    if not isinstance(target, ast.Name) or target.id.startswith("__"):
                        continue
                    is_constant = target.id.isupper() and isinstance(
                        value, immutable_literal
                    )
                    if not is_constant:
                        offences.append((path.name, target.id))
        self.assertEqual(offences, [])

    def test_no_registry_or_discovery_surface(self):
        """Registry/discovery discipline is [O] reserved (Blueprint §25)."""
        surface = " ".join(knowledge_pkg.__all__).lower()
        for term in ("registry", "register", "catalog", "discover", "index"):
            self.assertNotIn(term, surface)

    def test_no_trust_scoring_or_ranking(self):
        """Domain Model §10 defers Knowledge Trust Scoring; PR-3 forbids gating."""
        surface = " ".join(knowledge_pkg.__all__).lower()
        for term in ("trust", "score", "rank", "confidence", "probability"):
            self.assertNotIn(term, surface)


class TestDeterminism(unittest.TestCase):
    """Same input, same result — no hidden state, no generated identity."""

    def test_version_construction_is_deterministic(self):
        first = KnowledgeVersion(VersionIdentity("item", 1), {"a": 1})
        second = KnowledgeVersion(VersionIdentity("item", 1), {"a": 1})
        self.assertEqual(first.identity, second.identity)
        self.assertEqual(dict(first.content), dict(second.content))

    def test_identity_is_hashable_and_comparable(self):
        self.assertEqual(VersionIdentity("item", 1), VersionIdentity("item", 1))
        self.assertEqual(len({VersionIdentity("i", 1), VersionIdentity("i", 1)}), 1)
        self.assertLess(VersionIdentity("item", 1), VersionIdentity("item", 2))

    def test_version_hashes_by_identity(self):
        """Captured content may contain mappings; identity keeps it hashable."""
        version = KnowledgeVersion(VersionIdentity("item", 1), {"a": 1})
        self.assertEqual(hash(version), hash(VersionIdentity("item", 1)))

    def test_no_generated_identity_in_the_boundary(self):
        """No UUID, timestamp, or randomness — identity is a governed ordinal."""
        offences = [
            (p.name, m)
            for p in _modules()
            for m, level in _imports(p)
            if level == 0 and m.split(".")[0] in {"uuid", "random", "time", "datetime", "secrets"}
        ]
        self.assertEqual(offences, [])


if __name__ == "__main__":
    unittest.main()
