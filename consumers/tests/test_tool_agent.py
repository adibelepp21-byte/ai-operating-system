"""
`ToolProposingAgent` — contract realization, isolation, and authority limits.

Focused evidence about the consumer itself. The `E8-03` path evidence lives in
`test_tool_agent_runtime.py`, because a unit test cannot establish it.
"""

from __future__ import annotations

import ast
import inspect
import unittest
from pathlib import Path

from consumers.tool_agent import ToolProposingAgent
from native_core.core.agent import Agent
from native_core.core.infrastructure import (
    CallerClass,
    ExternalTool,
    InvocationRequest,
    ToolContract,
    ToolIdentity,
    create_tool_subsystem,
)
from native_core.shared import Success

KEY = "unit-tool"


class Echo(ExternalTool):
    def __init__(self):
        self.calls = 0

    @property
    def canonical_key(self):
        return KEY

    def invoke(self, action, parameters):
        self.calls += 1
        return Success(value="ok")


def _agent(enable=True):
    sub = create_tool_subsystem()
    tool = Echo()
    sub.registry.define(ToolIdentity(KEY), ToolContract(actions=("run",)))
    sub.registry.register(KEY)
    sub.boundary.register(tool)
    if enable:
        sub.registry.enable(KEY)
    return ToolProposingAgent(governance=sub.governance), sub, tool


def _imported_modules():
    source = Path(inspect.getfile(ToolProposingAgent)).read_text()
    modules = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
        elif isinstance(node, ast.Import):
            modules.update(a.name for a in node.names)
    return modules


class ItRealizesTheAgentContract(unittest.TestCase):

    def test_it_is_an_agent(self):
        self.assertTrue(issubclass(ToolProposingAgent, Agent))

    def test_an_instance_is_an_agent(self):
        self.assertIsInstance(ToolProposingAgent(), Agent)

    def test_it_lives_outside_the_native_core(self):
        path = Path(inspect.getfile(ToolProposingAgent)).as_posix()

        self.assertNotIn("/native_core/", path)
        self.assertIn("/consumers/", path)


class ItProposesAndIsGoverned(unittest.TestCase):

    def test_it_composes_a_request_without_reaching_a_boundary(self):
        request = ToolProposingAgent().compose(KEY, "run", {"a": 1})

        self.assertIsInstance(request, InvocationRequest)
        self.assertIs(CallerClass.AGENT, request.caller)

    def test_a_composed_request_carries_no_approval_field(self):
        request = ToolProposingAgent().compose(KEY, "run")

        for forbidden in ("approved", "admitted", "authorized", "disposition"):
            self.assertFalse(hasattr(request, forbidden), forbidden)

    def test_an_admitted_proposal_executes(self):
        agent, _, tool = _agent()

        result = agent.propose(agent.compose(KEY, "run"))

        self.assertTrue(result.is_success)
        self.assertEqual(1, tool.calls)

    def test_a_refused_proposal_is_recorded_and_does_not_execute(self):
        agent, _, tool = _agent(enable=False)

        result = agent.propose(agent.compose(KEY, "run"))

        self.assertTrue(result.is_refusal)
        self.assertEqual(0, tool.calls)
        self.assertEqual(1, len(agent.refused))

    def test_results_partition_into_executed_and_refused(self):
        agent, sub, _ = _agent()
        agent.propose(agent.compose(KEY, "run"))
        sub.registry.disable(KEY)
        agent.propose(agent.compose(KEY, "run"))

        self.assertEqual(2, len(agent.results))
        self.assertEqual(1, len(agent.executed))
        self.assertEqual(1, len(agent.refused))

    def test_observations_are_immutable_to_callers(self):
        agent, _, _ = _agent()
        agent.propose(agent.compose(KEY, "run"))

        self.assertIsInstance(agent.results, tuple)

    def test_a_wrong_collaborator_type_is_refused(self):
        with self.assertRaises(TypeError):
            ToolProposingAgent(governance="not a governance wrapper")

    def test_proposing_without_a_collaborator_refuses_rather_than_guessing(self):
        agent = ToolProposingAgent()

        with self.assertRaises(RuntimeError):
            agent.propose(agent.compose(KEY, "run"))


class ItHoldsNoToolAuthority(unittest.TestCase):
    """`FD-P8-001 §4.6` and `§4.8`, asserted structurally."""

    def test_it_depends_only_on_the_agent_contract_and_infrastructure(self):
        core = {m for m in _imported_modules() if m.startswith("native_core")}

        self.assertEqual(
            {"native_core.core.agent", "native_core.core.infrastructure",
             "native_core.core.trace"},
            core,
        )

    def test_it_imports_no_runtime_type(self):
        for module in _imported_modules():
            self.assertNotIn("runtime", module)

    def test_it_imports_nothing_from_governance_or_knowledge(self):
        for module in _imported_modules():
            self.assertNotIn("governance", module)
            self.assertNotIn("knowledge", module)

    def test_it_never_references_the_tool_boundary_directly(self):
        """The only Tool surface it touches is the governance wrapper, so there
        is no path here that could bypass the gate."""
        source = Path(inspect.getfile(ToolProposingAgent)).read_text()
        tree = ast.parse(source)
        names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
        names |= {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}

        for forbidden in ("ToolBoundary", "boundary", "registry"):
            self.assertNotIn(forbidden, names, forbidden)

    def test_it_defines_no_lifecycle_method(self):
        tree = ast.parse(Path(inspect.getfile(ToolProposingAgent)).read_text())
        methods = {
            n.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef) and node.name == "ToolProposingAgent"
            for n in node.body
            if isinstance(n, ast.FunctionDef)
        }

        for forbidden in ("register", "define", "enable", "disable", "retire", "invoke"):
            self.assertNotIn(forbidden, methods)


if __name__ == "__main__":
    unittest.main()
