"""
`MemoryConsumingAgent` — contract realization, isolation, and authority limits.

Focused evidence about the consumer itself. The `E7-03` path evidence lives in
`test_memory_agent_runtime.py`, because a unit test cannot establish it.
"""

from __future__ import annotations

import ast
import inspect
import unittest
from pathlib import Path

from consumers.memory_agent import MemoryConsumingAgent
from native_core.core.agent import Agent
from native_core.core.memory import (
    MemoryCandidate,
    MemoryState,
    create_memory_subsystem,
)

KEY = "unit-key"


def _agent(rule=None):
    sub = create_memory_subsystem(rule)
    return MemoryConsumingAgent(lifecycle=sub.lifecycle, retrieval=sub.retrieval), sub


def _imported_modules():
    source = Path(inspect.getfile(MemoryConsumingAgent)).read_text()
    modules = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
        elif isinstance(node, ast.Import):
            modules.update(a.name for a in node.names)
    return modules


class ItRealizesTheAgentContract(unittest.TestCase):

    def test_it_is_an_agent(self):
        self.assertTrue(issubclass(MemoryConsumingAgent, Agent))

    def test_an_instance_is_an_agent(self):
        self.assertIsInstance(MemoryConsumingAgent(), Agent)

    def test_it_lives_outside_the_native_core(self):
        path = Path(inspect.getfile(MemoryConsumingAgent)).as_posix()

        self.assertNotIn("/native_core/", path)
        self.assertIn("/consumers/", path)


class ItProposesAndReads(unittest.TestCase):

    def test_it_forms_a_candidate(self):
        candidate = MemoryConsumingAgent().form_candidate(KEY, "v")

        self.assertIsInstance(candidate, MemoryCandidate)
        self.assertEqual("agent-instance", candidate.provenance.source)

    def test_a_proposal_is_admitted_by_the_boundary(self):
        agent, _ = _agent()

        admitted = agent.propose(agent.form_candidate(KEY, "v"))

        self.assertEqual(MemoryState.RETAINED, admitted.state)
        self.assertEqual(1, len(agent.memory_admitted))

    def test_it_reads_eligible_memory(self):
        agent, _ = _agent()
        agent.propose(agent.form_candidate(KEY, "v"))

        self.assertEqual("v", agent.read(KEY).payload)

    def test_reading_an_unknown_key_yields_none(self):
        agent, _ = _agent()

        self.assertIsNone(agent.read("absent"))

    def test_a_refusal_is_recorded_not_swallowed(self):
        agent, _ = _agent(rule=lambda c: False)

        result = agent.propose(agent.form_candidate(KEY, "v"))

        self.assertIsNone(result)
        self.assertEqual(1, len(agent.proposals_refused))
        self.assertEqual((), agent.memory_admitted)

    def test_it_reads_the_history_line(self):
        agent, sub = _agent()
        agent.propose(agent.form_candidate(KEY, "v1"))
        sub.lifecycle.update(KEY, "v2")

        self.assertEqual(2, len(agent.history(KEY)))

    def test_observations_are_immutable_to_callers(self):
        agent, _ = _agent()
        agent.propose(agent.form_candidate(KEY, "v"))

        self.assertIsInstance(agent.memory_admitted, tuple)
        self.assertIsInstance(agent.memory_read, tuple)

    def test_a_wrong_collaborator_type_is_refused(self):
        with self.assertRaises(TypeError):
            MemoryConsumingAgent(lifecycle="not a lifecycle")
        with self.assertRaises(TypeError):
            MemoryConsumingAgent(retrieval="not a retrieval")

    def test_reading_without_a_collaborator_refuses_rather_than_guessing(self):
        with self.assertRaises(RuntimeError):
            MemoryConsumingAgent().read(KEY)

    def test_proposing_without_a_collaborator_refuses(self):
        with self.assertRaises(RuntimeError):
            MemoryConsumingAgent().propose(
                MemoryConsumingAgent().form_candidate(KEY, "v")
            )


class ItHoldsNoAuthority(unittest.TestCase):
    """`FD-P7-001 §5` and `FD-P7-002 §3`, asserted structurally."""

    def test_it_depends_only_on_the_agent_contract_and_memory(self):
        core = {m for m in _imported_modules() if m.startswith("native_core")}

        self.assertEqual({"native_core.core.agent", "native_core.core.memory"}, core)

    def test_it_imports_no_runtime_type(self):
        for module in _imported_modules():
            self.assertNotIn("runtime", module)

    def test_it_imports_nothing_from_governance_or_knowledge(self):
        for module in _imported_modules():
            self.assertNotIn("governance", module)
            self.assertNotIn("knowledge", module)

    def test_it_imports_nothing_from_tools(self):
        for module in _imported_modules():
            self.assertFalse(module.startswith("tools"))

    def test_it_defines_no_lifecycle_transition_method(self):
        tree = ast.parse(Path(inspect.getfile(MemoryConsumingAgent)).read_text())
        methods = {
            n.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef) and node.name == "MemoryConsumingAgent"
            for n in node.body
            if isinstance(n, ast.FunctionDef)
        }

        for forbidden in ("expire", "invalidate", "update", "consolidate", "admit"):
            self.assertNotIn(forbidden, methods)

    def test_it_never_names_the_hosting_runtime(self):
        """It reaches the Runtime only through the Execution it is handed."""
        source = Path(inspect.getfile(MemoryConsumingAgent)).read_text()
        tree = ast.parse(source)
        called = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }

        self.assertNotIn("create_runtime", called)
        self.assertNotIn("create_execution_layer", called)


if __name__ == "__main__":
    unittest.main()
