"""
Skill conformance tests (Blueprint §9/§27; skill_spec §1–§14; Roadmap §9.7;
Freeze INV-4/INV-12/INV-15; PR-3/PR-4).

Roadmap §9.7 fixes this boundary's invariants as *"INV-15, INV-12, INV-4."*
Each test below asserts one of those, or one of the boundary rules the
specification states:

  - INV-15 — an Agent Definition may specify zero or more Skills; an empty
             Skill declaration is a **valid architectural state** and is never
             raised on (Domain Model §7 invariant 15; ADR-0007).
  - INV-12 — Tool is the only entity permitted an external dependency, so this
             boundary holds none (skill_spec §7/§8).
  - INV-4  — every Agent Instance action produces exactly one Trace, so a Skill
             authors none of its own; accountability runs through the invoking
             action's Trace (skill_spec §9).
  - PR-4   — an unresolvable Skill halts the invoking action accountably rather
             than proceeding silently (skill_spec §11).
  - Reserved scope — no registry, discovery, index or catalogue surface exists
             (skill_spec §13/§14 [O]; Blueprint §9).
  - No execution surface — skill_spec §5/§8; Freeze §4.
  - Immutability and determinism — contracts are frozen; same input, same
             result.

Standard-library `unittest` only.
Run: python -m unittest native_core.core.skill.tests.test_skill_conformance
"""

from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path

from native_core.core import skill as skill_pkg
from native_core.core.skill import (
    AgentDefinitionRef,
    DuplicateSkillDeclaration,
    InvalidSkill,
    InvalidSkillDeclaration,
    Skill,
    SkillDeclaration,
    SkillError,
    SkillIdentity,
    UnresolvedSkill,
)

AGENT = AgentDefinitionRef("engineering-intelligence-agent")
OTHER_AGENT = AgentDefinitionRef("cognitive-intelligence-agent")


def _identity(key: str, version: str = "v1") -> SkillIdentity:
    return SkillIdentity(key, version)


class TestInv15DeclarationCardinality(unittest.TestCase):
    """INV-15 — zero or more Skills; an empty declaration is valid."""

    def test_zero_declared_skills_is_valid(self):
        """Domain Model §7 invariant 15; ADR-0007: a valid architectural state."""
        declaration = SkillDeclaration(AGENT)
        self.assertTrue(declaration.is_empty())
        self.assertEqual(declaration.declared(), ())

    def test_empty_declaration_never_raises(self):
        """No minimum cardinality is imposed — inventing one would exceed the model."""
        try:
            SkillDeclaration(AGENT, ())
        except SkillError as exc:  # pragma: no cover - failure path
            self.fail(f"empty declaration must be valid, raised {exc!r}")

    def test_one_declared_skill_is_valid(self):
        declaration = SkillDeclaration(AGENT, (_identity("coding"),))
        self.assertFalse(declaration.is_empty())
        self.assertEqual(declaration.declared(), (_identity("coding"),))

    def test_many_declared_skills_are_valid(self):
        declared = (_identity("coding"), _identity("testing"), _identity("review"))
        self.assertEqual(SkillDeclaration(AGENT, declared).declared(), declared)

    def test_declaration_order_is_preserved(self):
        declared = (_identity("testing"), _identity("coding"))
        self.assertEqual(SkillDeclaration(AGENT, declared).declared(), declared)

    def test_declaring_agent_definition_is_mandatory(self):
        with self.assertRaises(InvalidSkillDeclaration):
            SkillDeclaration(None, ())

    def test_declaring_agent_definition_must_be_a_reference(self):
        with self.assertRaises(InvalidSkillDeclaration):
            SkillDeclaration("engineering-intelligence-agent", ())

    def test_empty_agent_definition_key_fails_closed(self):
        with self.assertRaises(InvalidSkillDeclaration):
            AgentDefinitionRef("   ")

    def test_non_identity_member_fails_closed(self):
        with self.assertRaises(InvalidSkillDeclaration):
            SkillDeclaration(AGENT, ("coding",))

    def test_non_tuple_declaration_fails_closed(self):
        with self.assertRaises(InvalidSkillDeclaration):
            SkillDeclaration(AGENT, [_identity("coding")])

    def test_repeated_skill_key_fails_closed(self):
        """A repeated key makes the declared set ambiguous — never resolved arbitrarily."""
        with self.assertRaises(DuplicateSkillDeclaration):
            SkillDeclaration(AGENT, (_identity("coding"), _identity("coding", "v2")))


class TestPr4FailClosedResolution(unittest.TestCase):
    """skill_spec §11 — an unresolvable Skill halts accountably (PR-4)."""

    def test_declared_skill_resolves(self):
        declaration = SkillDeclaration(AGENT, (_identity("coding", "v2"),))
        self.assertEqual(declaration.resolve("coding"), _identity("coding", "v2"))

    def test_undeclared_skill_raises_rather_than_returning_a_default(self):
        with self.assertRaises(UnresolvedSkill):
            SkillDeclaration(AGENT, (_identity("coding"),)).resolve("testing")

    def test_resolution_against_an_empty_declaration_fails_closed(self):
        """Empty is valid to hold, and still resolves nothing (INV-15 + PR-4)."""
        with self.assertRaises(UnresolvedSkill):
            SkillDeclaration(AGENT).resolve("coding")

    def test_failure_names_the_declaring_agent_definition(self):
        with self.assertRaises(UnresolvedSkill) as raised:
            SkillDeclaration(OTHER_AGENT).resolve("coding")
        self.assertIn("cognitive-intelligence-agent", str(raised.exception))

    def test_every_failure_is_a_skill_error(self):
        for error in (
            InvalidSkill,
            InvalidSkillDeclaration,
            UnresolvedSkill,
            DuplicateSkillDeclaration,
        ):
            self.assertTrue(issubclass(error, SkillError))


class TestSkillContract(unittest.TestCase):
    """Domain Model §2/§5/§6 — the Skill contract itself."""

    def test_skill_carries_a_versioned_identity(self):
        skill = Skill(_identity("coding", "v2"))
        self.assertEqual(skill.identity.skill_version, "v2")

    def test_identity_requires_a_key(self):
        with self.assertRaises(InvalidSkill):
            SkillIdentity("", "v1")

    def test_identity_requires_a_version(self):
        with self.assertRaises(InvalidSkill):
            SkillIdentity("coding", "   ")

    def test_identity_must_be_an_identity(self):
        with self.assertRaises(InvalidSkill):
            Skill("coding")

    def test_skill_carries_no_owning_department(self):
        """Domain Model §5 [E]: Skill is *owned centrally* — no owner field."""
        self.assertEqual(set(Skill.__dataclass_fields__), {"identity"})

    def test_no_version_format_is_imposed(self):
        """Domain Model §6 versions Skill independently; no scheme is ratified."""
        for version in ("v1", "1.0", "2026-07-31", "draft"):
            self.assertEqual(SkillIdentity("coding", version).skill_version, version)


class TestInv4NoIndependentTrace(unittest.TestCase):
    """INV-4 — a Skill authors no Trace; accountability is the invoker's."""

    PACKAGE = Path(skill_pkg.__file__).parent

    def _modules(self):
        return sorted(p for p in self.PACKAGE.rglob("*.py") if "tests" not in p.parts)

    def test_no_trace_boundary_import(self):
        """skill_spec §9: accountability runs through the invoking action's Trace."""
        offences = []
        for path in self._modules():
            for node in ast.walk(ast.parse(path.read_text())):
                modules = []
                if isinstance(node, ast.Import):
                    modules = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom):
                    if (node.level or 0) > 0:
                        continue
                    modules = [node.module or ""]
                for module in modules:
                    if "trace" in {p for p in module.split(".") if p}:
                        offences.append((path.name, module))
        self.assertEqual(offences, [])

    def test_no_trace_authoring_callable(self):
        offences = []
        for path in self._modules():
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if "trace" in node.name.lower():
                        offences.append((path.name, node.name))
        self.assertEqual(offences, [])

    def test_no_trace_field_on_any_contract(self):
        for contract in (Skill, SkillIdentity, SkillDeclaration, AgentDefinitionRef):
            for field in contract.__dataclass_fields__:
                self.assertNotIn("trace", field.lower())

    def test_public_surface_names_no_trace(self):
        self.assertNotIn("trace", " ".join(skill_pkg.__all__).lower())


class TestInv12NoExternalDependency(unittest.TestCase):
    """INV-12 — Tool is the only entity permitted an external dependency."""

    PACKAGE = Path(skill_pkg.__file__).parent
    FORBIDDEN_BOUNDARIES = {
        "agent",
        "workflow",
        "tool",
        "runtime",
        "capability",
        "governance",
        "trace",
        "memory",
        "knowledge",
        "optimization",
        "infrastructure",
    }

    def _modules(self):
        return sorted(p for p in self.PACKAGE.rglob("*.py") if "tests" not in p.parts)

    def test_no_external_dependency(self):
        """Standard library only — nothing is installed, fetched, or vendored."""
        allowed = set(sys.stdlib_module_names) | {"native_core"}
        offences = []
        for path in self._modules():
            for node in ast.walk(ast.parse(path.read_text())):
                modules = []
                if isinstance(node, ast.Import):
                    modules = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom):
                    if (node.level or 0) > 0:
                        continue
                    modules = [node.module or ""]
                for module in modules:
                    top = module.split(".")[0]
                    if top and top not in allowed:
                        offences.append((path.name, module))
        self.assertEqual(offences, [])

    def test_no_forbidden_boundary_import(self):
        """skill_spec §8; Blueprint §9: Skill is used by others, depends on none."""
        offences = []
        for path in self._modules():
            for node in ast.walk(ast.parse(path.read_text())):
                modules = []
                if isinstance(node, ast.Import):
                    modules = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom):
                    if (node.level or 0) > 0:
                        continue
                    modules = [node.module or ""]
                for module in modules:
                    hit = {p for p in module.split(".") if p} & self.FORBIDDEN_BOUNDARIES
                    if hit:
                        offences.append((path.name, module, sorted(hit)))
        self.assertEqual(offences, [])

    def test_no_network_filesystem_or_process_access(self):
        """A facility, not an actor (skill_spec §2) — it reaches nothing outside."""
        forbidden = {
            "socket",
            "http",
            "urllib",
            "subprocess",
            "shutil",
            "os",
            "pathlib",
            "sqlite3",
        }
        offences = []
        for path in self._modules():
            for node in ast.walk(ast.parse(path.read_text())):
                modules = []
                if isinstance(node, ast.Import):
                    modules = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom):
                    if (node.level or 0) > 0:
                        continue
                    modules = [node.module or ""]
                for module in modules:
                    if module.split(".")[0] in forbidden:
                        offences.append((path.name, module))
        self.assertEqual(offences, [])


class TestReservedScopeIsNotBuilt(unittest.TestCase):
    """skill_spec §13/§14 [O]; Blueprint §9 — registry and discovery reserved."""

    PACKAGE = Path(skill_pkg.__file__).parent
    RESERVED_TERMS = ("registry", "register", "catalog", "discover", "index")
    EXECUTION_VERBS = {
        "execute",
        "run",
        "invoke",
        "perform",
        "call",
        "act",
        "start",
        "apply",
    }

    def _modules(self):
        return sorted(p for p in self.PACKAGE.rglob("*.py") if "tests" not in p.parts)

    def test_no_registry_or_discovery_in_the_public_surface(self):
        surface = " ".join(skill_pkg.__all__).lower()
        for term in self.RESERVED_TERMS:
            self.assertNotIn(term, surface)

    def test_no_registry_or_discovery_callable_or_class(self):
        offences = []
        for path in self._modules():
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                ):
                    lowered = node.name.lower()
                    for term in self.RESERVED_TERMS:
                        if term in lowered:
                            offences.append((path.name, node.name))
        self.assertEqual(offences, [])

    def test_resolution_is_declaration_scoped_not_system_wide(self):
        """No catalogue exists: a Skill declared elsewhere is not resolvable here."""
        SkillDeclaration(AGENT, (_identity("coding"),))
        with self.assertRaises(UnresolvedSkill):
            SkillDeclaration(OTHER_AGENT).resolve("coding")

    def test_no_module_level_mutable_state(self):
        """A registry cannot hide in module state — none exists to hide in."""
        offences = []
        for path in self._modules():
            tree = ast.parse(path.read_text())
            for node in tree.body:
                targets = []
                if isinstance(node, ast.Assign):
                    targets = node.targets
                elif isinstance(node, ast.AnnAssign):
                    targets = [node.target]
                for target in targets:
                    if isinstance(target, ast.Name) and not target.id.startswith("__"):
                        offences.append((path.name, target.id))
        self.assertEqual(offences, [])

    def test_no_execution_surface(self):
        """skill_spec §5/§8; Freeze §4: a Skill is ability, it does not run itself."""
        offences = []
        for path in self._modules():
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.name.lstrip("_").lower() in self.EXECUTION_VERBS:
                        offences.append((path.name, node.name))
        self.assertEqual(offences, [])

    def test_no_async_or_threading(self):
        offences = []
        for path in self._modules():
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, (ast.AsyncFunctionDef, ast.Await)):
                    offences.append(path.name)
        self.assertEqual(offences, [])

    def test_capability_and_workflow_composition_is_not_modelled(self):
        """skill_spec §14 [O]: Skill↔Capability/Workflow composition unratified."""
        surface = " ".join(skill_pkg.__all__).lower()
        self.assertNotIn("capability", surface)
        self.assertNotIn("workflow", surface)

    def test_tool_reference_is_not_modelled(self):
        """INV-12 keeps the external boundary with Tool; that edge is not built."""
        self.assertNotIn("tool", " ".join(skill_pkg.__all__).lower())

    def test_public_surface_is_exactly_the_declared_exports(self):
        self.assertEqual(
            set(skill_pkg.__all__),
            {
                "AgentDefinitionRef",
                "DuplicateSkillDeclaration",
                "InvalidSkill",
                "InvalidSkillDeclaration",
                "Skill",
                "SkillDeclaration",
                "SkillError",
                "SkillIdentity",
                "UnresolvedSkill",
            },
        )


class TestImmutabilityAndDeterminism(unittest.TestCase):
    """Frozen contracts; same input, same result — no hidden state."""

    def test_contracts_are_frozen(self):
        for contract in (Skill, SkillIdentity, SkillDeclaration, AgentDefinitionRef):
            self.assertTrue(
                contract.__dataclass_params__.frozen,
                f"{contract.__name__} must be frozen",
            )

    def test_skill_is_immutable(self):
        skill = Skill(_identity("coding"))
        with self.assertRaises(Exception):
            skill.identity = _identity("testing")

    def test_declaration_is_immutable(self):
        declaration = SkillDeclaration(AGENT)
        with self.assertRaises(Exception):
            declaration.skills = (_identity("coding"),)

    def test_identity_is_hashable_and_comparable(self):
        self.assertEqual(_identity("coding"), _identity("coding"))
        self.assertEqual(len({_identity("coding"), _identity("coding")}), 1)
        self.assertLess(_identity("coding"), _identity("testing"))

    def test_resolution_is_deterministic(self):
        declaration = SkillDeclaration(
            AGENT, (_identity("coding"), _identity("testing"))
        )
        self.assertEqual(
            declaration.resolve("testing"), declaration.resolve("testing")
        )
        self.assertEqual(declaration.declared(), declaration.declared())


if __name__ == "__main__":
    unittest.main()
