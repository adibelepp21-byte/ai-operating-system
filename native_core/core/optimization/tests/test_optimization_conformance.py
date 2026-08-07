"""
Optimization conformance tests (Blueprint §15/§26/§27/§31; optimization_spec
§1–§14; Roadmap §9.11; Freeze §5 layer 10; PR-3/PR-4; INV-5/INV-8/INV-12).

Baseline 06 — L10 Optimization, the eleventh and last frozen boundary.

Each test asserts one ratified requirement, one specification rule, or one
governance ruling that fixed this baseline's scope:

  - PR-3   — detect, don't decide. No decision path exists under test; this is
             the boundary's stated completion criterion (Roadmap §9.11).
  - INV-8  — no promotion path; Memory is never moved into Knowledge here.
  - INV-5  — Trace is read, never written.
  - INV-12 — no external dependency; cross-boundary imports are Trace and
             Memory only.
  - PR-4   — fail closed on anything that cannot be formed accountably.
  - P7-I27 A — no Governance dependency; publication, never submission.
  - P7-I27 B — the reserved design space is preserved, not filled.
  - P7-I27 C — no legacy asset imported, copied, or migrated.

Verification is structural (AST, dataclass, signature, abstract-interface and
public-API inspection) in preference to runtime simulation.

Standard-library `unittest` only.
Run: python -m unittest native_core.core.optimization.tests.test_optimization_conformance
"""

from __future__ import annotations

import abc
import ast
import dataclasses
import inspect
import sys
import unittest
from pathlib import Path

from native_core.core import optimization as optimization_pkg
from native_core.core.memory import MemoryReader, MemoryRecord
from native_core.core.optimization import (
    MEMORY_SOURCE,
    OBSERVABLE_SOURCES,
    TRACE_SOURCE,
    InvalidObservation,
    InvalidOptimizationConfiguration,
    InvalidProposal,
    MemoryObservationSource,
    ObservationPublication,
    ObservationSource,
    OptimizationError,
    OptimizationObservation,
    OptimizationProposal,
    PassiveObservationPublication,
    TraceObservationSource,
    create_optimization,
)
from native_core.core.infrastructure import StorageFacility
from native_core.core.trace import TraceReader, TraceWriter, new_record

PACKAGE = Path(optimization_pkg.__file__).parent
CORE = PACKAGE.parent
BOUNDARY = "optimization"
ROOT_PACKAGE = "native_core.core"


# --------------------------------------------------------------------------
# structural helpers
# --------------------------------------------------------------------------


def _modules():
    return sorted(p for p in PACKAGE.rglob("*.py") if "tests" not in p.parts)


def _tree(path):
    return ast.parse(path.read_text())


def _dotted(path):
    parts = path.relative_to(PACKAGE).with_suffix("").parts
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join((ROOT_PACKAGE, BOUNDARY) + parts)


def _containing_package(path):
    dotted = _dotted(path)
    return dotted if path.name == "__init__.py" else dotted.rsplit(".", 1)[0]


def _resolve(path, module, level):
    """Resolve an import to an absolute module name.

    Resolving the relative level is what distinguishes `from .observation
    import` (level 1 — this boundary) from `from ..trace import` (level 2 —
    another boundary). Substring matching cannot make that distinction."""
    if level == 0:
        return module
    base = _containing_package(path).split(".")
    if level > 1:
        base = base[: -(level - 1)]
    return ".".join(base + ([module] if module else []))


def _import_records():
    records = []
    for path in _modules():
        for node in ast.walk(_tree(path)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    records.append((path, alias.name, (alias.name,)))
            elif isinstance(node, ast.ImportFrom):
                records.append(
                    (
                        path,
                        _resolve(path, node.module or "", node.level or 0),
                        tuple(a.name for a in node.names),
                    )
                )
    return records


def _boundary_of(dotted):
    prefix = ROOT_PACKAGE + "."
    if not dotted.startswith(prefix):
        return None
    return dotted[len(prefix) :].split(".")[0]


def _cross_boundary_records():
    return [
        (p, m, n)
        for p, m, n in _import_records()
        if _boundary_of(m) not in (None, BOUNDARY)
    ]


def _definitions():
    for path in _modules():
        for node in ast.walk(_tree(path)):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                yield path.name, node


def _identifiers():
    """Every real identifier in the boundary. Docstrings and comments are
    excluded by construction — prose is not evidence."""
    for path in _modules():
        for node in ast.walk(_tree(path)):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                yield path.name, node.name
            elif isinstance(node, ast.Name):
                yield path.name, node.id
            elif isinstance(node, ast.Attribute):
                yield path.name, node.attr
            elif isinstance(node, ast.arg):
                yield path.name, node.arg


def _field_types(klass):
    return [
        (f.name, f.type if isinstance(f.type, str) else f.type.__name__)
        for f in dataclasses.fields(klass)
    ]


def _is_declaration_only(node):
    return all(
        isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) for s in node.body
    )


# --------------------------------------------------------------------------
# hermetic test doubles — no filesystem, no external dependency
# --------------------------------------------------------------------------


class _MemoryStorage(StorageFacility):
    """An in-process StorageFacility, so the suite touches no filesystem. It
    implements exactly the abstract facility surface and nothing more."""

    name = "storage.optimization-conformance"

    def __init__(self):
        super().__init__()
        self._records = {}

    def _provision(self) -> None:
        return None

    def append(self, partition, record):
        self.require_ready()
        self._records.setdefault(partition, []).append(bytes(record))

    def read(self, partition):
        self.require_ready()
        return iter(tuple(self._records.get(partition, ())))

    def partitions(self):
        self.require_ready()
        return iter(sorted(self._records))


def _trace_record(instance="instance-a", status="success"):
    return new_record(
        agent_definition_version="1.0.0",
        agent_instance=instance,
        runtime="runtime-a",
        skills_used=(),
        tools_used=(),
        knowledge_consumed=(),
        memory_consumed=(),
        outputs={"result": "ok"},
        cost_resource_metadata={},
        status=status,
    )


def _readers(instances=("instance-a", "instance-b")):
    """A TraceReader over synthetic records, and the MemoryReader derived from
    it. Records are written through Trace's own `TraceWriter`, so the fixture
    exercises the real public surfaces of both boundaries rather than a
    hand-rolled serialization."""
    storage = _MemoryStorage()
    storage.provision()
    writer = TraceWriter(storage)
    for name in instances:
        writer.write(_trace_record(name))
    trace_reader = TraceReader(storage)
    return trace_reader, MemoryReader(trace_reader)


def _observation(source=TRACE_SOURCE, subject="subject-a", observed="content"):
    return OptimizationObservation(source=source, subject=subject, observed=observed)


# --------------------------------------------------------------------------
# PR-3 — detect, don't decide  (Roadmap §9.11 completion criterion)
# --------------------------------------------------------------------------


class TestDetectDontDecide(unittest.TestCase):
    """Roadmap §9.11 fixes this boundary's completion as *"PR-3 upheld; no
    decision path under test"*, and rates *"automation acquiring a decision"* a
    **Critical** risk. The property is therefore verified structurally: a
    decision must be unrepresentable, not merely undocumented."""

    DECISION_VERBS = frozenset(
        {
            "decide",
            "decision",
            "approve",
            "reject",
            "authorize",
            "authorization",
            "grant",
            "deny",
            "permit",
            "revoke",
            "promote",
            "promotion",
            "admit",
            "veto",
            "sign_off",
        }
    )

    def test_no_decision_identifier_exists_in_the_boundary(self):
        for filename, identifier in _identifiers():
            self.assertNotIn(identifier, self.DECISION_VERBS, f"{filename}: {identifier}")

    def test_no_decision_operation_is_defined(self):
        for filename, node in _definitions():
            self.assertNotIn(node.name, self.DECISION_VERBS, f"{filename}:{node.name}")

    def test_the_contracts_declare_only_read_shaped_operations(self):
        """Neither contract carries a verb that could reach outward or accept a
        decision."""
        self.assertEqual({"observe"}, set(ObservationSource.__abstractmethods__))
        self.assertEqual(
            {"published", "proposals"}, set(ObservationPublication.__abstractmethods__)
        )

    def test_no_governance_authority_type_is_reachable(self):
        """A decision needs an authority. None is imported, held, or named."""
        for name in ("HumanAuthority", "ReviewDecision", "GovernanceReview"):
            self.assertFalse(hasattr(optimization_pkg, name), name)
        for _, _, names in _import_records():
            for name in names:
                self.assertNotIn(name, ("HumanAuthority", "ReviewDecision", "GovernanceReview"))

    def test_a_proposal_carries_no_authority_and_no_verdict(self):
        names = {f.name for f in dataclasses.fields(OptimizationProposal)}
        for absent in ("decision", "verdict", "approved", "authority", "reviewer", "outcome"):
            self.assertNotIn(absent, names)


# --------------------------------------------------------------------------
# P7-I27 Conflict A — publication, never submission
# --------------------------------------------------------------------------


class TestNoGovernanceDependency(unittest.TestCase):
    """P7-I27 Conflict A: *"Optimization shall not submit proposals directly to
    Governance… There shall be no Governance API dependency originating from
    the Optimization boundary."*"""

    OUTBOUND_VERBS = frozenset(
        {
            "submit",
            "send",
            "notify",
            "request",
            "dispatch",
            "publish_to",
            "push",
            "emit",
            "post",
            "deliver",
            "escalate",
            "call",
            "invoke",
        }
    )

    def test_governance_is_never_imported(self):
        for path, module, _ in _import_records():
            self.assertNotEqual("governance", _boundary_of(module), path.name)

    def test_no_governance_identifier_exists(self):
        for filename, identifier in _identifiers():
            self.assertNotIn(
                "governance", identifier.lower(), f"{filename}: {identifier}"
            )

    def test_no_outbound_verb_exists(self):
        """Publication is passive: nothing here reaches a consumer."""
        for filename, identifier in _identifiers():
            self.assertNotIn(identifier, self.OUTBOUND_VERBS, f"{filename}: {identifier}")

    def test_the_publication_is_read_only_in_both_directions(self):
        """It exposes what it holds and accepts nothing back."""
        public = {n for n in dir(PassiveObservationPublication) if not n.startswith("_")}
        self.assertEqual({"published", "proposals"}, public)
        for name in ("published", "proposals"):
            self.assertEqual(
                ["self"],
                list(inspect.signature(getattr(PassiveObservationPublication, name)).parameters),
                f"{name} must accept nothing",
            )

    def test_publication_is_immutable(self):
        publication = PassiveObservationPublication(_observations=(), _proposals=())
        self.assertTrue(dataclasses.is_dataclass(PassiveObservationPublication))
        self.assertTrue(PassiveObservationPublication.__dataclass_params__.frozen)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            publication._observations = (_observation(),)


# --------------------------------------------------------------------------
# P7-I27 Conflict B — reserved design space preserved, not filled
# --------------------------------------------------------------------------


class TestReservedDesignSpaceIsPreserved(unittest.TestCase):
    """P7-I27 Conflict B reserves the signal catalogue, evaluation scoring,
    prioritization model, optimization algorithm, recommendation engine,
    ranking model, decision heuristics, and promotion strategy.

    These tests assert those are **absent**. They verify a reservation was
    honoured — they do not question it and do not resolve it."""

    RESERVED = frozenset(
        {
            "score",
            "scores",
            "scoring",
            "rate",
            "rating",
            "rank",
            "ranking",
            "priority",
            "prioritize",
            "prioritization",
            "weight",
            "confidence",
            "severity",
            "urgency",
            "threshold",
            "heuristic",
            "recommend",
            "recommendation",
            "suggest",
            "suggestion",
            "evaluate",
            "evaluation",
            "signal",
            "signals",
            "catalog",
            "catalogue",
            "strategy",
            "algorithm",
        }
    )

    def test_no_reserved_identifier_exists_in_the_boundary(self):
        for filename, identifier in _identifiers():
            self.assertNotIn(identifier, self.RESERVED, f"{filename}: {identifier}")

    def test_no_reserved_operation_is_defined(self):
        for filename, node in _definitions():
            self.assertNotIn(node.name, self.RESERVED, f"{filename}:{node.name}")

    def test_no_value_object_carries_a_judgement_field(self):
        for klass in (OptimizationObservation, OptimizationProposal):
            for name, _ in _field_types(klass):
                self.assertNotIn(name, self.RESERVED, klass.__name__)

    def test_the_contract_declares_no_reserved_surface(self):
        """A reserved model cannot be supplied by a realization, because no
        contract declares it."""
        declared = set(ObservationSource.__abstractmethods__) | set(
            ObservationPublication.__abstractmethods__
        )
        self.assertEqual(set(), declared & self.RESERVED)

    def test_proposals_are_carried_never_derived(self):
        """Deriving a proposal would require the reserved evaluation and
        prioritization models. The composition root passes them through
        unchanged instead."""
        trace_reader, memory_reader = _readers()
        supplied = (OptimizationProposal(proposal_key="p-1", observations=(_observation(),)),)
        publication = create_optimization(trace_reader, memory_reader, supplied)
        self.assertEqual(supplied, publication.proposals())

    def test_no_proposal_appears_without_being_supplied(self):
        trace_reader, memory_reader = _readers()
        self.assertEqual((), create_optimization(trace_reader, memory_reader).proposals())


# --------------------------------------------------------------------------
# detect-only observation — completeness, no selection
# --------------------------------------------------------------------------


class TestObservationIsDetectOnly(unittest.TestCase):
    """optimization_spec §2: *"Observe Trace and Memory; surface candidates,
    conditions, and quality signals — as proposals only."* Transcription is the
    whole of it: selecting *which* records matter would be a judgement."""

    def test_both_sources_realize_the_contract(self):
        for klass in (TraceObservationSource, MemoryObservationSource):
            self.assertTrue(issubclass(klass, ObservationSource))
            self.assertFalse(inspect.isabstract(klass))

    def test_the_contract_is_abstract_and_declaration_only(self):
        self.assertTrue(issubclass(ObservationSource, abc.ABC))
        self.assertTrue(inspect.isabstract(ObservationSource))
        with self.assertRaises(TypeError):
            ObservationSource()
        contract = PACKAGE / "contract.py"
        for node in ast.walk(_tree(contract)):
            if isinstance(node, ast.FunctionDef):
                self.assertTrue(_is_declaration_only(node), node.name)

    def test_every_trace_record_is_transcribed_in_order(self):
        """Completeness: no record is filtered away, and the order is the order
        read. A filter would be a hidden selection heuristic."""
        instances = ("a", "b", "c", "d")
        trace_reader, _ = _readers(instances)
        observed = TraceObservationSource(_reader=trace_reader).observe()
        self.assertEqual(len(instances), len(observed))
        self.assertEqual(list(instances), [o.subject for o in observed])
        self.assertTrue(all(o.source == TRACE_SOURCE for o in observed))

    def test_every_memory_record_is_transcribed_in_order(self):
        trace_reader, memory_reader = _readers(("a", "b", "c"))
        expected = memory_reader.read()
        observed = MemoryObservationSource(_reader=memory_reader).observe()
        self.assertEqual(len(expected), len(observed))
        self.assertEqual([r.scope for r in expected], [o.subject for o in observed])
        self.assertTrue(all(o.source == MEMORY_SOURCE for o in observed))

    def test_observing_is_repeatable_and_changes_nothing(self):
        """Deterministic and side-effect free: observing twice yields the same
        result, and observing does not alter what was observed."""
        trace_reader, _ = _readers(("a", "b"))
        source = TraceObservationSource(_reader=trace_reader)
        self.assertEqual(source.observe(), source.observe())

    def test_a_source_returns_an_immutable_tuple(self):
        trace_reader, memory_reader = _readers()
        for source in (
            TraceObservationSource(_reader=trace_reader),
            MemoryObservationSource(_reader=memory_reader),
        ):
            self.assertIsInstance(source.observe(), tuple)

    def test_observe_takes_no_selection_argument(self):
        """No filter, scope, limit, or predicate can be passed in — so no caller
        can push a selection judgement into the boundary."""
        for klass in (TraceObservationSource, MemoryObservationSource):
            self.assertEqual(["self"], list(inspect.signature(klass.observe).parameters))

    def test_sources_fail_closed_on_a_wrong_reader(self):
        trace_reader, memory_reader = _readers()
        with self.assertRaises(InvalidOptimizationConfiguration):
            TraceObservationSource(_reader=memory_reader)
        with self.assertRaises(InvalidOptimizationConfiguration):
            MemoryObservationSource(_reader=trace_reader)
        for klass in (TraceObservationSource, MemoryObservationSource):
            with self.assertRaises(InvalidOptimizationConfiguration):
                klass(_reader=object())


# --------------------------------------------------------------------------
# immutable value objects
# --------------------------------------------------------------------------


class TestImmutableValueObjects(unittest.TestCase):
    """Blueprint §15: Optimization owns non-authoritative records only. They are
    frozen, so nothing downstream can mutate what was observed."""

    def test_both_are_frozen_dataclasses(self):
        for klass in (OptimizationObservation, OptimizationProposal):
            self.assertTrue(dataclasses.is_dataclass(klass), klass.__name__)
            self.assertTrue(klass.__dataclass_params__.frozen, klass.__name__)

    def test_observation_fields(self):
        self.assertEqual(
            [("source", "str"), ("subject", "str"), ("observed", "Any")],
            _field_types(OptimizationObservation),
        )

    def test_proposal_fields(self):
        self.assertEqual(
            [
                ("proposal_key", "str"),
                ("observations", "Tuple[OptimizationObservation, ...]"),
            ],
            _field_types(OptimizationProposal),
        )

    def test_value_objects_cannot_be_mutated(self):
        observation = _observation()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            observation.subject = "other"
        proposal = OptimizationProposal(proposal_key="p", observations=(observation,))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            proposal.proposal_key = "other"

    def test_value_objects_compare_by_value(self):
        self.assertEqual(_observation(), _observation())
        self.assertEqual(1, len({_observation(), _observation()}))

    def test_the_observable_source_set_is_closed(self):
        """Optimization observes Trace and Memory and nothing else
        (optimization_spec §7)."""
        self.assertEqual({TRACE_SOURCE, MEMORY_SOURCE}, set(OBSERVABLE_SOURCES))
        self.assertIsInstance(OBSERVABLE_SOURCES, frozenset)
        for bad in ("knowledge", "governance", "runtime", "agent", ""):
            with self.assertRaises(InvalidObservation):
                _observation(source=bad)

    def test_an_observation_cannot_alias_mutable_state(self):
        """A mutable container would let an observation change after it was
        recorded — the record would no longer be what was observed."""
        for mutable in ([1], {"a": 1}, {1, 2}, bytearray(b"x")):
            with self.assertRaises(InvalidObservation):
                _observation(observed=mutable)

    def test_an_observation_requires_a_subject(self):
        for bad in ("", "   ", None, 7):
            with self.assertRaises(InvalidObservation):
                _observation(subject=bad)


class TestProposalsAreEvidenceBearing(unittest.TestCase):
    """optimization_spec §2/§11 — a proposal rests on what was observed, and an
    uncertain boundary proposes nothing rather than deciding."""

    def test_a_proposal_without_evidence_is_unrepresentable(self):
        with self.assertRaises(InvalidProposal):
            OptimizationProposal(proposal_key="p", observations=())

    def test_evidence_must_be_immutable(self):
        with self.assertRaises(InvalidProposal):
            OptimizationProposal(proposal_key="p", observations=[_observation()])

    def test_evidence_must_be_observations(self):
        with self.assertRaises(InvalidProposal):
            OptimizationProposal(proposal_key="p", observations=("not-an-observation",))

    def test_a_proposal_requires_an_identity(self):
        for bad in ("", "   ", None, 7):
            with self.assertRaises(InvalidProposal):
                OptimizationProposal(proposal_key=bad, observations=(_observation(),))

    def test_a_proposal_preserves_its_evidence_unchanged(self):
        observations = (_observation("trace", "a"), _observation("memory", "b"))
        self.assertEqual(
            observations,
            OptimizationProposal(proposal_key="p", observations=observations).observations,
        )


# --------------------------------------------------------------------------
# INV-5 / INV-8 — Trace unwritten, Knowledge unreachable
# --------------------------------------------------------------------------


class TestTraceAndPromotionBoundaries(unittest.TestCase):
    """INV-5: Trace is immutable — Optimization reads it and never writes it.
    INV-8: Knowledge is entered only via governed review — no promotion path
    exists here."""

    def test_no_trace_write_surface_is_imported(self):
        for path, module, names in _import_records():
            if _boundary_of(module) != "trace":
                continue
            self.assertNotIn("TraceWriter", names, path.name)
            for name in names:
                self.assertNotIn("write", name.lower(), path.name)

    def test_no_write_identifier_targets_trace(self):
        for filename, identifier in _identifiers():
            self.assertNotIn(
                identifier, ("write", "append", "record_trace", "emit_trace"), filename
            )

    def test_knowledge_is_never_imported(self):
        """INV-8: no promotion path can exist if Knowledge is unreachable."""
        for path, module, _ in _import_records():
            self.assertNotEqual("knowledge", _boundary_of(module), path.name)

    def test_no_knowledge_or_promotion_identifier_exists(self):
        for filename, identifier in _identifiers():
            self.assertNotIn("knowledge", identifier.lower(), f"{filename}: {identifier}")
            self.assertNotIn("promot", identifier.lower(), f"{filename}: {identifier}")

    def test_optimization_authors_no_trace(self):
        """OQ-2: the boundary is a facility, not an independently traced actor.
        It observes Trace records; it creates none."""
        for filename, identifier in _identifiers():
            self.assertNotIn(identifier, ("new_record", "TraceWriter"), filename)


# --------------------------------------------------------------------------
# dependency direction — INV-12, module isolation, Conflict C
# --------------------------------------------------------------------------


class TestDependencyDirection(unittest.TestCase):
    """Blueprint §26; optimization_spec §7/§8; INV-12."""

    PERMITTED = frozenset({"trace", "memory"})
    FORBIDDEN = frozenset(
        {
            "governance",
            "knowledge",
            "runtime",
            "agent",
            "capability",
            "skill",
            "workflow",
            "infrastructure",
        }
    )
    STDLIB = frozenset({"__future__", "abc", "dataclasses", "typing"})

    def test_cross_boundary_imports_are_only_trace_and_memory(self):
        reached = {_boundary_of(m) for _, m, _ in _cross_boundary_records()}
        self.assertEqual(self.PERMITTED, reached)

    def test_no_forbidden_boundary_is_imported(self):
        for path, module, _ in _cross_boundary_records():
            self.assertNotIn(
                _boundary_of(module), self.FORBIDDEN, f"{path.name} imports {module}"
            )

    def test_dependencies_are_reached_at_their_public_surface(self):
        """Blueprint §26: no boundary reaches into another's internals."""
        for path, module, _ in _cross_boundary_records():
            self.assertIn(
                module,
                (f"{ROOT_PACKAGE}.trace", f"{ROOT_PACKAGE}.memory"),
                f"{path.name} reaches an internal module: {module}",
            )

    def test_no_external_dependency_exists(self):
        """INV-12: Tool is the only entity permitted an external dependency."""
        for path, module, _ in _import_records():
            if _boundary_of(module) is not None:
                continue
            root = module.split(".")[0]
            self.assertIn(root, self.STDLIB, f"{path.name} imports {module}")
            self.assertTrue(
                root in sys.stdlib_module_names or root == "__future__", root
            )

    def test_no_legacy_asset_is_imported_or_referenced(self):
        """P7-I27 Conflict C — the legacy assets are REFERENCE ONLY and
        CANONICAL REFERENCE: not imported, not copied, not migrated."""
        for path, module, _ in _import_records():
            for legacy in ("observability", "metrics", "promotion", "legacy"):
                self.assertNotIn(legacy, module, f"{path.name} imports {module}")
        for filename, identifier in _identifiers():
            for legacy in ("observability", "legacy"):
                self.assertNotIn(legacy, identifier.lower(), f"{filename}: {identifier}")

    def test_internal_relative_imports_stay_in_boundary(self):
        """Anti-false-positive: `from .observation import` (level 1) is a
        same-boundary import; resolving the level distinguishes it from
        `from ..trace import` (level 2)."""
        internal = [
            (p.name, m) for p, m, _ in _import_records() if _boundary_of(m) == BOUNDARY
        ]
        self.assertTrue(internal)
        for filename, module in internal:
            self.assertTrue(module.startswith(f"{ROOT_PACKAGE}.{BOUNDARY}"), filename)

    def test_no_boundary_outside_optimization_depends_on_it(self):
        """No reverse edge, therefore no cycle. Optimization is last in the
        dependency order (Blueprint §23; Roadmap §9.11 priority 11)."""
        offenders = []
        for path in sorted(CORE.rglob("*.py")):
            relative = path.relative_to(CORE).parts
            if "tests" in relative or (relative and relative[0] == BOUNDARY):
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.ImportFrom) and BOUNDARY in (node.module or ""):
                    offenders.append((str(path), node.module))
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if BOUNDARY in alias.name:
                            offenders.append((str(path), alias.name))
        self.assertEqual([], offenders)


# --------------------------------------------------------------------------
# public API surface
# --------------------------------------------------------------------------


class TestPublicApiSurface(unittest.TestCase):
    """Blueprint §26 — the boundary exposes exactly its declared surface."""

    EXPECTED = (
        "ObservationSource",
        "ObservationPublication",
        "OptimizationObservation",
        "OBSERVABLE_SOURCES",
        "TRACE_SOURCE",
        "MEMORY_SOURCE",
        "OptimizationProposal",
        "create_optimization",
        "TraceObservationSource",
        "MemoryObservationSource",
        "PassiveObservationPublication",
        "OptimizationError",
        "InvalidObservation",
        "InvalidProposal",
        "InvalidOptimizationConfiguration",
    )

    def test_exports_are_exactly_the_declared_names(self):
        self.assertEqual(list(self.EXPECTED), list(optimization_pkg.__all__))

    def test_every_export_resolves(self):
        for name in optimization_pkg.__all__:
            self.assertTrue(hasattr(optimization_pkg, name), name)

    def test_no_export_leaks_another_boundary(self):
        for name in optimization_pkg.__all__:
            module = getattr(getattr(optimization_pkg, name), "__module__", None)
            if module is None:
                continue
            self.assertTrue(
                module.startswith(f"{ROOT_PACKAGE}.{BOUNDARY}"),
                f"{name} is exported from {module}",
            )

    def test_the_documented_surface_matches_the_declared_surface(self):
        docstring = optimization_pkg.__doc__ or ""
        for name in optimization_pkg.__all__:
            self.assertIn(name, docstring, f"{name} is exported but undocumented")

    def test_no_foreign_entity_name_is_exported(self):
        for name in optimization_pkg.__all__:
            for word in ("Knowledge", "Governance", "Agent", "Workflow", "Skill", "Capability"):
                self.assertNotIn(word, name)


# --------------------------------------------------------------------------
# PR-4 — fail closed
# --------------------------------------------------------------------------


class TestFailsClosed(unittest.TestCase):
    """optimization_spec §11; PR-4 — *"if evaluation is uncertain, it proposes
    nothing rather than deciding."*"""

    def test_every_halt_shares_one_base(self):
        for error in (InvalidObservation, InvalidProposal, InvalidOptimizationConfiguration):
            self.assertTrue(issubclass(error, OptimizationError), error.__name__)

    def test_the_base_does_not_shadow_the_builtin(self):
        self.assertTrue(issubclass(OptimizationError, RuntimeError))
        self.assertIsNot(OptimizationError, RuntimeError)

    def test_composition_fails_closed_on_a_wrong_reader(self):
        trace_reader, memory_reader = _readers()
        for args in (
            (None, memory_reader),
            (object(), memory_reader),
            (memory_reader, memory_reader),
            (trace_reader, None),
            (trace_reader, object()),
            (trace_reader, trace_reader),
        ):
            with self.assertRaises(InvalidOptimizationConfiguration):
                create_optimization(*args)

    def test_composition_fails_closed_on_non_sequence_proposals(self):
        trace_reader, memory_reader = _readers()
        for bad in (7, object(), "proposal"):
            with self.assertRaises(InvalidOptimizationConfiguration):
                create_optimization(trace_reader, memory_reader, bad)

    def test_publication_fails_closed_on_wrong_content(self):
        for kwargs in (
            {"_observations": [_observation()], "_proposals": ()},
            {"_observations": (), "_proposals": ["p"]},
            {"_observations": ("not-an-observation",), "_proposals": ()},
        ):
            with self.assertRaises(InvalidOptimizationConfiguration):
                PassiveObservationPublication(**kwargs)

    def test_every_halt_message_is_a_string(self):
        """AST: each raise passes a single string, so no halt reaches an
        operator as a structured object needing interpretation."""
        for path in _modules():
            for node in ast.walk(_tree(path)):
                if not isinstance(node, ast.Raise) or not isinstance(node.exc, ast.Call):
                    continue
                for argument in node.exc.args:
                    self.assertIsInstance(
                        argument, (ast.Constant, ast.JoinedStr), f"{path.name}:{node.lineno}"
                    )
                    if isinstance(argument, ast.Constant):
                        self.assertIsInstance(argument.value, str)

    def test_nothing_is_caught_or_suppressed(self):
        for path in _modules():
            for node in ast.walk(_tree(path)):
                self.assertNotIsInstance(node, ast.Try, path.name)
                self.assertNotIsInstance(node, ast.ExceptHandler, path.name)


# --------------------------------------------------------------------------
# composition discipline and deterministic architecture
# --------------------------------------------------------------------------


class TestCompositionAndDeterminism(unittest.TestCase):
    """Blueprint §26 — constructor injection only; no clock, no randomness, no
    hidden state, no reflection, no concurrency."""

    NONDETERMINISM = frozenset(
        {
            "random",
            "secrets",
            "uuid",
            "time",
            "datetime",
            "threading",
            "asyncio",
            "multiprocessing",
            "concurrent",
            "socket",
            "importlib",
            "os",
            "subprocess",
        }
    )
    DYNAMIC = frozenset(
        {"eval", "exec", "compile", "globals", "locals", "vars", "__import__", "setattr", "delattr"}
    )

    def test_no_source_of_nondeterminism_is_imported(self):
        for path, module, _ in _import_records():
            self.assertNotIn(module.split(".")[0], self.NONDETERMINISM, path.name)

    def test_no_reflection_or_dynamic_import_is_used(self):
        for filename, identifier in _identifiers():
            self.assertNotIn(identifier, self.DYNAMIC, filename)

    def test_no_concurrency_construct_is_declared(self):
        for path in _modules():
            for node in ast.walk(_tree(path)):
                for forbidden in (ast.AsyncFunctionDef, ast.Await, ast.AsyncFor, ast.AsyncWith):
                    self.assertNotIsInstance(node, forbidden, path.name)

    def test_module_level_state_is_limited_to_immutable_declarations(self):
        """No singleton, no registry, no cache. `__all__` is the export
        declaration; an UPPER_CASE name bound to an immutable literal or a
        `frozenset(...)` is a constant, not state."""
        for path in _modules():
            for node in _tree(path).body:
                if not isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                    continue
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    self.assertIsInstance(target, ast.Name, path.name)
                    if target.id == "__all__":
                        continue
                    self.assertTrue(
                        target.id.isupper() or target.id.startswith("_"),
                        f"{path.name}: module-level state {target.id!r}",
                    )
                    value = node.value
                    self.assertTrue(
                        isinstance(value, ast.Constant)
                        or (
                            isinstance(value, ast.Call)
                            and isinstance(value.func, ast.Name)
                            and value.func.id == "frozenset"
                        )
                        or isinstance(value, ast.Tuple),
                        f"{path.name}: {target.id!r} is not an immutable declaration",
                    )

    def test_the_boundary_mutates_nothing(self):
        """No AugAssign anywhere: the boundary observes and records; it
        accumulates no counter and updates no state."""
        mutations = [
            (path.name, node.lineno)
            for path in _modules()
            for node in ast.walk(_tree(path))
            if isinstance(node, ast.AugAssign)
        ]
        self.assertEqual([], mutations)

    def test_composition_constructs_a_fresh_graph_every_call(self):
        trace_reader, memory_reader = _readers()
        first = create_optimization(trace_reader, memory_reader)
        second = create_optimization(trace_reader, memory_reader)
        self.assertIsNot(first, second)
        self.assertEqual(first.published(), second.published())

    def test_composition_observes_trace_then_memory(self):
        """Deterministic assembly order, so the publication is reproducible."""
        trace_reader, memory_reader = _readers(("a", "b"))
        published = create_optimization(trace_reader, memory_reader).published()
        sources = [o.source for o in published]
        self.assertEqual(
            sorted(set(sources), key=sources.index), [TRACE_SOURCE, MEMORY_SOURCE]
        )

    def test_composition_constructs_only_this_boundary(self):
        """Readers are injected, never constructed here."""
        source = PACKAGE / "composition.py"
        constructed = {
            node.func.id
            for node in ast.walk(_tree(source))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        self.assertNotIn("TraceReader", constructed)
        self.assertNotIn("MemoryReader", constructed)


# --------------------------------------------------------------------------
# repository structural conformance
# --------------------------------------------------------------------------


class TestRepositoryStructuralConformance(unittest.TestCase):
    """Blueprint §3/§15/§31 — Optimization is the eleventh frozen boundary and
    completes the core region."""

    def test_optimization_is_a_direct_child_of_the_core_region(self):
        self.assertEqual("core", CORE.name)
        self.assertEqual(CORE, PACKAGE.parent)

    def test_the_core_region_now_holds_the_eleven_frozen_boundaries(self):
        expected = {
            "trace",
            "memory",
            "knowledge",
            "governance",
            "runtime",
            "agent",
            "capability",
            "skill",
            "workflow",
            "infrastructure",
            "optimization",
        }
        present = {
            p.name
            for p in CORE.iterdir()
            if p.is_dir() and not p.name.startswith("__")
        }
        self.assertEqual(expected, present)

    def test_the_boundary_consists_of_exactly_its_declared_modules(self):
        self.assertEqual(
            [
                "__init__.py",
                "composition.py",
                "contract.py",
                "exceptions.py",
                "observation.py",
                "proposals.py",
            ],
            [p.name for p in _modules()],
        )

    def test_the_boundary_introduces_no_subpackage(self):
        subpackages = [
            p.name
            for p in PACKAGE.iterdir()
            if p.is_dir() and p.name not in ("tests", "__pycache__")
        ]
        self.assertEqual([], subpackages)

    def test_no_domain_model_entity_is_declared(self):
        """Roadmap §9.11 — *"Entity: (none; detect-only)"*; Blueprint §31 — no
        new entity or subsystem is introduced.

        Matched on the **exact** class name, not as a substring: naming the
        source a class reads from — `TraceObservationSource` — declares no Trace
        entity, and a substring rule would report it as one."""
        forbidden = {
            "Knowledge",
            "Memory",
            "Trace",
            "Governance",
            "Runtime",
            "Agent",
            "AgentDefinition",
            "AgentInstance",
            "Workflow",
            "Skill",
            "Capability",
            "Department",
            "Tool",
            "Organization",
        }
        for filename, node in _definitions():
            if not isinstance(node, ast.ClassDef):
                continue
            self.assertNotIn(node.name, forbidden, f"{filename}:{node.name}")


if __name__ == "__main__":
    unittest.main()
