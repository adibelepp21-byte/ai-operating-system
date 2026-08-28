"""
`E5-3` evidence — the Engineering Intelligence first milestone.

`GDR-0005 §3.5.3`: *"exactly two (2) of the seven sub-capabilities … **Coding**
and **Testing** — are implemented and verified. The remaining five
(Architecture, Security, Review, Refactoring, Documentation) are **not**
required for Phase 5 exit."*

`exactly two` is asserted in both directions. `Coding` and `Testing` are shown to
work; `TheFiveAreNotRealized` shows the other five are absent, because realizing
a sixth would broaden Phase 5 scope just as surely as leaving one of the two
undone would fail the criterion.
"""

from __future__ import annotations

import ast
import inspect
import unittest
from pathlib import Path

from consumers.engineering_intelligence_agent import (
    REALIZED_SUB_ABILITIES,
    UNREALIZED_SUB_ABILITIES,
    Artifact,
    CheckResult,
    ConformanceCriterion,
    EngineeringIntelligenceAgent,
)
from native_core.core.agent import Agent


def _class_methods(subject, class_name):
    tree = ast.parse(Path(inspect.getfile(subject)).read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return {n.name for n in node.body if isinstance(n, ast.FunctionDef)}
    raise AssertionError(f"{class_name} was not found")


class E503Coding(unittest.TestCase):
    """The first of the two realized sub-abilities."""

    def test_it_constructs_an_engineered_artifact(self):
        agent = EngineeringIntelligenceAgent()

        artifact = agent.construct("module.py", ["def f():", "    return 1"])

        self.assertEqual("module.py", artifact.name)
        self.assertEqual(2, len(artifact.lines))

    def test_what_it_constructed_is_recorded(self):
        agent = EngineeringIntelligenceAgent()

        agent.construct("a.py", ["x = 1"])

        self.assertEqual(1, len(agent.constructed))

    def test_it_changes_an_artifact(self):
        agent = EngineeringIntelligenceAgent()
        original = agent.construct("m.py", ["x = 1"])

        changed = agent.change(original, ["x = 2"])

        self.assertEqual("m.py", changed.name)
        self.assertEqual(("x = 2",), changed.lines)

    def test_a_change_never_edits_the_prior_version_in_place(self):
        """The T-12 discipline, applied to engineered artifacts."""
        agent = EngineeringIntelligenceAgent()
        original = agent.construct("m.py", ["x = 1"])

        changed = agent.change(original, ["x = 2"])

        self.assertEqual(("x = 1",), original.lines)
        self.assertIsNot(original, changed)

    def test_both_versions_are_retained_as_evidence(self):
        agent = EngineeringIntelligenceAgent()
        original = agent.construct("m.py", ["x = 1"])
        agent.change(original, ["x = 2"])

        self.assertEqual(2, len(agent.constructed))

    def test_only_an_artifact_can_be_changed(self):
        agent = EngineeringIntelligenceAgent()

        with self.assertRaises(TypeError):
            agent.change("not an artifact", ["x = 1"])

    def test_an_artifact_must_be_named(self):
        with self.assertRaises(ValueError):
            Artifact(name="  ", lines=("x",))

    def test_an_artifact_is_immutable(self):
        artifact = Artifact(name="a.py", lines=("x",))

        with self.assertRaises(Exception):
            artifact.name = "b.py"


class E503Testing(unittest.TestCase):
    """The second of the two realized sub-abilities."""

    def test_it_verifies_an_artifact_against_stated_criteria(self):
        agent = EngineeringIntelligenceAgent()
        artifact = agent.construct("m.py", ["def f():", "    return 1"])
        criteria = [ConformanceCriterion("declares f", "def f():")]

        results = agent.verify(artifact, criteria)

        self.assertTrue(results[0].satisfied)

    def test_it_reports_a_failing_criterion_rather_than_raising(self):
        """`PR-3` — Detect Don't Decide."""
        agent = EngineeringIntelligenceAgent()
        artifact = agent.construct("m.py", ["x = 1"])

        results = agent.verify(artifact, [ConformanceCriterion("has g", "def g():")])

        self.assertFalse(results[0].satisfied)

    def test_every_criterion_is_reported_not_just_the_first_failure(self):
        agent = EngineeringIntelligenceAgent()
        artifact = agent.construct("m.py", ["a = 1"])
        criteria = [
            ConformanceCriterion("one", "zzz"),
            ConformanceCriterion("two", "a = 1"),
            ConformanceCriterion("three", "yyy"),
        ]

        results = agent.verify(artifact, criteria)

        self.assertEqual(3, len(results))
        self.assertEqual([False, True, False], [r.satisfied for r in results])

    def test_results_are_reported_in_the_order_stated(self):
        agent = EngineeringIntelligenceAgent()
        artifact = agent.construct("m.py", ["a = 1"])
        criteria = [ConformanceCriterion("first", "a"), ConformanceCriterion("second", "b")]

        results = agent.verify(artifact, criteria)

        self.assertEqual(["first", "second"], [r.criterion_name for r in results])

    def test_conformance_is_all_criteria_satisfied(self):
        agent = EngineeringIntelligenceAgent()
        artifact = agent.construct("m.py", ["a = 1", "b = 2"])
        criteria = [ConformanceCriterion("a", "a = 1"), ConformanceCriterion("b", "b = 2")]

        results = agent.verify(artifact, criteria)

        self.assertTrue(agent.is_conformant(results))

    def test_one_failing_criterion_defeats_conformance(self):
        agent = EngineeringIntelligenceAgent()
        artifact = agent.construct("m.py", ["a = 1"])
        criteria = [ConformanceCriterion("a", "a = 1"), ConformanceCriterion("b", "b = 2")]

        self.assertFalse(agent.is_conformant(agent.verify(artifact, criteria)))

    def test_verifying_against_no_criteria_fails_closed(self):
        """`PR-4`. An empty criteria set would report conformance while
        checking nothing."""
        agent = EngineeringIntelligenceAgent()
        artifact = agent.construct("m.py", ["a = 1"])

        with self.assertRaises(ValueError):
            agent.verify(artifact, [])

    def test_conformance_is_undefined_over_an_empty_result_set(self):
        with self.assertRaises(ValueError):
            EngineeringIntelligenceAgent.is_conformant([])

    def test_only_an_artifact_can_be_verified(self):
        agent = EngineeringIntelligenceAgent()

        with self.assertRaises(TypeError):
            agent.verify("not an artifact", [ConformanceCriterion("c", "x")])

    def test_criteria_must_be_stated_as_criteria(self):
        agent = EngineeringIntelligenceAgent()
        artifact = agent.construct("m.py", ["a = 1"])

        with self.assertRaises(TypeError):
            agent.verify(artifact, ["a = 1"])

    def test_a_criterion_must_state_what_it_requires(self):
        with self.assertRaises(ValueError):
            ConformanceCriterion("named", "")

    def test_a_result_is_immutable(self):
        result = CheckResult("a.py", "c", True)

        with self.assertRaises(Exception):
            result.satisfied = False


class TheFiveAreNotRealized(unittest.TestCase):
    """*Exactly* two — the ceiling, asserted."""

    def test_exactly_two_sub_abilities_are_declared_realized(self):
        self.assertEqual(("Coding", "Testing"), REALIZED_SUB_ABILITIES)
        self.assertEqual(2, len(REALIZED_SUB_ABILITIES))

    def test_the_other_five_are_declared_unrealized(self):
        self.assertEqual(5, len(UNREALIZED_SUB_ABILITIES))

    def test_the_seven_partition_without_overlap(self):
        self.assertEqual(
            set(), set(REALIZED_SUB_ABILITIES) & set(UNREALIZED_SUB_ABILITIES)
        )
        self.assertEqual(7, len(set(REALIZED_SUB_ABILITIES) | set(UNREALIZED_SUB_ABILITIES)))

    def test_no_method_implements_an_unrealized_sub_ability(self):
        methods = _class_methods(EngineeringIntelligenceAgent, "EngineeringIntelligenceAgent")
        forbidden = {
            "architect", "design",           # Architecture
            "secure", "audit_security",      # Security
            "review", "approve",             # Review
            "refactor",                      # Refactoring
            "document", "generate_docs",     # Documentation
        }

        self.assertEqual(set(), methods & forbidden)

    def test_it_writes_nothing_to_the_repository(self):
        """The Definition grants no filesystem authority."""
        source = Path(inspect.getfile(EngineeringIntelligenceAgent)).read_text()
        tree = ast.parse(source)
        called = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }

        for forbidden in ("write_text", "write_bytes", "mkdir", "unlink", "system", "run"):
            self.assertNotIn(forbidden, called)

    def test_it_imports_no_filesystem_or_process_module(self):
        source = Path(inspect.getfile(EngineeringIntelligenceAgent)).read_text()
        modules = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
            elif isinstance(node, ast.Import):
                modules.update(a.name for a in node.names)

        for forbidden in ("os", "subprocess", "shutil", "pathlib", "sys"):
            self.assertNotIn(forbidden, modules)

    def test_it_never_executes_what_it_constructs(self):
        source = Path(inspect.getfile(EngineeringIntelligenceAgent)).read_text()
        tree = ast.parse(source)
        called = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }

        for forbidden in ("exec", "eval", "compile", "__import__"):
            self.assertNotIn(forbidden, called)


class TheAgentHoldsNoAuthority(unittest.TestCase):

    def _imported_modules(self):
        source = Path(inspect.getfile(EngineeringIntelligenceAgent)).read_text()
        modules = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
            elif isinstance(node, ast.Import):
                modules.update(a.name for a in node.names)
        return modules

    def test_it_realizes_the_agent_contract(self):
        self.assertTrue(issubclass(EngineeringIntelligenceAgent, Agent))

    def test_an_instance_is_an_agent(self):
        self.assertIsInstance(EngineeringIntelligenceAgent(), Agent)

    def test_it_depends_only_on_the_agent_contract(self):
        core = {m for m in self._imported_modules() if m.startswith("native_core")}

        self.assertEqual({"native_core.core.agent"}, core)

    def test_it_imports_nothing_from_governance_or_knowledge(self):
        for module in self._imported_modules():
            self.assertNotIn("governance", module)
            self.assertNotIn("knowledge", module)

    def test_it_holds_no_approval_authority(self):
        methods = _class_methods(EngineeringIntelligenceAgent, "EngineeringIntelligenceAgent")

        self.assertEqual(set(), methods & {"approve", "authorize", "certify", "ratify"})

    def test_it_lives_outside_the_native_core(self):
        path = Path(inspect.getfile(EngineeringIntelligenceAgent)).as_posix()

        self.assertNotIn("/native_core/", path)
        self.assertIn("/consumers/", path)


if __name__ == "__main__":
    unittest.main()
