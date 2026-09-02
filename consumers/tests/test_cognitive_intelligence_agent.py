"""
`E5-2` evidence — the Cognitive Intelligence first milestone.

`GDR-0005 §3.5.3`: *"a single unit of execution work is decomposed into two (2)
or more ordered sub-steps, demonstrated on real execution rather than plan."*
The count and the ordering are asserted here; the *real execution* half is
supplied by `test_phase5_intelligence_runtime.py`, because a unit test invoking
the consumer directly cannot establish it.

The negative classes matter as much as the positive ones. `E5-2` is a count, and
a count is trivially satisfiable by fabricating sub-steps — so
`NothingIsInvented` and `TheBoundedRealizationHolds` exist to show that the
implementation cannot reach the number by manufacturing it, and that it stays
inside the Capability's recorded Phase 5 realization.
"""

from __future__ import annotations

import ast
import inspect
import unittest
from pathlib import Path

from consumers.cognitive_intelligence_agent import (
    CognitiveIntelligenceAgent,
    IndecomposableUnitOfWork,
    SubStep,
)
from native_core.core.agent import Agent


def _code_strings_and_identifiers(subject):
    """Every identifier and every non-docstring string literal in a module.

    Docstrings are excluded deliberately: documentation that *describes* a
    prohibition necessarily contains the prohibited word, and a check that
    cannot tell the two apart reports the description as a violation.
    """
    tree = ast.parse(Path(inspect.getfile(subject)).read_text())
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc is not None:
                docstrings.add(doc)
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value not in docstrings:
                found.append(node.value)
        elif isinstance(node, ast.Name):
            found.append(node.id)
        elif isinstance(node, ast.Attribute):
            found.append(node.attr)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            found.append(node.name)
        elif isinstance(node, ast.arg):
            found.append(node.arg)
    return found


class E502TheDecompositionCriterion(unittest.TestCase):
    """The ratified criterion, asserted as the count it is."""

    def test_a_unit_of_work_yields_two_or_more_sub_steps(self):
        agent = CognitiveIntelligenceAgent()

        steps = agent.decompose("read the contract; derive the sub-steps; record the order")

        self.assertGreaterEqual(len(steps), 2)

    def test_the_sub_steps_are_ordered(self):
        agent = CognitiveIntelligenceAgent()

        steps = agent.decompose("first thing; second thing; third thing")

        self.assertEqual([1, 2, 3], [step.ordinal for step in steps])

    def test_the_stated_order_is_preserved_not_rearranged(self):
        """Ordering means preserving what the work states, not scoring it."""
        agent = CognitiveIntelligenceAgent()

        steps = agent.decompose("zebra; alpha; mango")

        self.assertEqual(["zebra", "alpha", "mango"], [s.description for s in steps])

    def test_a_separator_other_than_semicolon_is_read(self):
        agent = CognitiveIntelligenceAgent()

        steps = agent.decompose("open the file then read it then close it")

        self.assertEqual(3, len(steps))

    def test_already_separated_steps_need_no_separator_convention(self):
        agent = CognitiveIntelligenceAgent()

        steps = agent.decompose_stated_steps(["compile", "link", "verify"])

        self.assertEqual(["compile", "link", "verify"], [s.description for s in steps])

    def test_the_decomposition_is_observable_after_the_fact(self):
        agent = CognitiveIntelligenceAgent()

        agent.decompose("one; two")

        self.assertEqual(2, len(agent.decomposition))


class NothingIsInvented(unittest.TestCase):
    """The count is satisfied by the work, or it is not satisfied."""

    def test_a_single_step_unit_raises_rather_than_being_padded(self):
        agent = CognitiveIntelligenceAgent()

        with self.assertRaises(IndecomposableUnitOfWork):
            agent.decompose("do the whole thing at once")

    def test_an_empty_unit_raises(self):
        agent = CognitiveIntelligenceAgent()

        with self.assertRaises(IndecomposableUnitOfWork):
            agent.decompose("   ")

    def test_a_single_stated_step_raises(self):
        agent = CognitiveIntelligenceAgent()

        with self.assertRaises(IndecomposableUnitOfWork):
            agent.decompose_stated_steps(["only one"])

    def test_every_sub_step_is_substring_of_the_stated_work(self):
        """Nothing in the output was absent from the input."""
        unit = "gather the evidence; classify it; report the result"
        agent = CognitiveIntelligenceAgent()

        steps = agent.decompose(unit)

        for step in steps:
            self.assertIn(step.description, unit)

    def test_no_decomposition_is_recorded_when_none_was_asked_for(self):
        agent = CognitiveIntelligenceAgent()

        self.assertEqual((), agent.decomposition)

    def test_a_failed_decomposition_records_nothing(self):
        agent = CognitiveIntelligenceAgent()
        with self.assertRaises(IndecomposableUnitOfWork):
            agent.decompose("indivisible")

        self.assertEqual((), agent.decomposition)

    def test_a_non_text_unit_of_work_is_refused(self):
        agent = CognitiveIntelligenceAgent()

        with self.assertRaises(TypeError):
            agent.decompose(["already", "a", "list"])


class TheSubStepContract(unittest.TestCase):

    def test_a_sub_step_is_immutable(self):
        step = SubStep(ordinal=1, description="something")

        with self.assertRaises(Exception):
            step.ordinal = 2

    def test_ordinals_are_one_based(self):
        with self.assertRaises(ValueError):
            SubStep(ordinal=0, description="something")

    def test_a_sub_step_must_describe_work(self):
        with self.assertRaises(ValueError):
            SubStep(ordinal=1, description="   ")

    def test_the_decomposition_is_immutable_to_callers(self):
        agent = CognitiveIntelligenceAgent()
        agent.decompose("one; two")

        self.assertIsInstance(agent.decomposition, tuple)


class TheBoundedRealizationHolds(unittest.TestCase):
    """The Capability declares three sub-abilities and records that Phase 5
    realizes only task decomposition and ordered planning."""

    def _tree(self):
        source = Path(inspect.getfile(CognitiveIntelligenceAgent)).read_text()
        return ast.parse(source)

    def _class_methods(self):
        for node in ast.walk(self._tree()):
            if isinstance(node, ast.ClassDef) and node.name == "CognitiveIntelligenceAgent":
                return {n.name for n in node.body if isinstance(n, ast.FunctionDef)}
        self.fail("the Agent class was not found")

    def test_it_realizes_the_agent_contract(self):
        self.assertTrue(issubclass(CognitiveIntelligenceAgent, Agent))

    def test_an_instance_is_an_agent(self):
        self.assertIsInstance(CognitiveIntelligenceAgent(), Agent)

    def test_it_carries_out_no_work_it_decomposed(self):
        """*"It does not itself carry out the work it decomposes."*"""
        forbidden = {"execute", "run", "perform", "carry_out", "dispatch", "invoke"}

        self.assertEqual(set(), self._class_methods() & forbidden)

    def test_it_exposes_no_reflection_or_review_surface(self):
        """Reasoning and Reflection are outside the Phase 5 realization."""
        forbidden = {"reflect", "review", "reason", "critique", "evaluate"}

        self.assertEqual(set(), self._class_methods() & forbidden)

    def test_it_names_no_technology_vendor_or_model(self):
        """Constitution §6.2 invariant 1.

        Scanned over **code**, not prose. A raw-text scan cannot distinguish a
        module that names a vendor from one whose documentation says it names
        none — this module's own header contains the word `vendor` for exactly
        that reason. Identifiers and non-docstring literals are what would carry
        a real technology decision, so those are what is checked.
        """
        forbidden = ("openai", "anthropic", "gpt", "llm", "vendor", "api_key", "http")

        for text in _code_strings_and_identifiers(CognitiveIntelligenceAgent):
            for term in forbidden:
                self.assertNotIn(term, text.lower())


class TheAgentHoldsNoAuthority(unittest.TestCase):
    """A consumer owns only its own behaviour."""

    def _imported_modules(self):
        source = Path(inspect.getfile(CognitiveIntelligenceAgent)).read_text()
        modules = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
            elif isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
        return modules

    def test_it_depends_only_on_the_agent_contract(self):
        core = {m for m in self._imported_modules() if m.startswith("native_core")}

        self.assertEqual(
            {"native_core.core.agent", "native_core.core.trace"}, core
        )

    def test_it_imports_nothing_from_governance_or_knowledge(self):
        for module in self._imported_modules():
            self.assertNotIn("governance", module)
            self.assertNotIn("knowledge", module)

    def test_it_imports_nothing_from_tools(self):
        for module in self._imported_modules():
            self.assertFalse(module.startswith("tools"))

    def test_it_lives_outside_the_native_core(self):
        path = Path(inspect.getfile(CognitiveIntelligenceAgent)).as_posix()

        self.assertNotIn("/native_core/", path)
        self.assertIn("/consumers/", path)


if __name__ == "__main__":
    unittest.main()
