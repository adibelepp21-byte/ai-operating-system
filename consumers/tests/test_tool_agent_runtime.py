"""
`E8-03` evidence — governed Tool invocation on the real execution path.

`ACT-CC-P8-001 §13` requires at least one real execution proving:

```text
Authorized Caller / Agent → Execution → Runtime (RUNNING) → Invocation Governance
                          → ToolBoundary → Tool → Structured Result
```

and `§19 Step 10` states that *"mocks may support edge-case testing but cannot
replace E8-03 real execution evidence."* So this module builds a real Runtime
with the resident `E-01` pattern, and every Tool the Agent reaches is the
**Runtime's own hosted subsystem** — several tests assert identity against
`runtime.tools.ledger` so a passing result cannot come from a collaborator the
test handed in.

`§14` requires negative controls that genuinely fail closed. Each refusal below
is therefore proved twice: the disposition says refused, **and** the Tool's own
call counter shows it was never reached.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from consumers.tool_agent import ToolProposingAgent
from native_core.core.infrastructure import (
    CallerClass,
    ExternalTool,
    InvocationDisposition,
    ToolContract,
    ToolIdentity,
)
from native_core.core.infrastructure import (
    LocalAppendOnlyStorage,
    LocalExecutionSubstrate,
)
from native_core.core.runtime import RuntimeState
from native_core.core.runtime.composition import create_runtime
from native_core.core.runtime.exceptions import RuntimeNotRunning
from native_core.core.runtime.execution import create_execution_layer
from native_core.shared import Failure, Success

KEY = "p8-echo"


class EchoTool(ExternalTool):
    """A real in-process Tool whose call counter is the negative controls'
    evidence that refusal meant non-execution."""

    def __init__(self, fail=False):
        self.calls = 0
        self._fail = fail

    @property
    def canonical_key(self) -> str:
        return KEY

    def invoke(self, action, parameters):
        self.calls += 1
        if self._fail:
            return Failure(reason="echo declined")
        return Success(value={"echoed": dict(parameters)})


def _runtime(start=True, runtime_id="p8-001-runtime"):
    """The resident E-01 pattern, unchanged."""
    storage = LocalAppendOnlyStorage(Path(tempfile.mkdtemp()))
    storage.provision()
    substrate = LocalExecutionSubstrate()
    substrate.provision()
    runtime = create_runtime(runtime_id=runtime_id, storage=storage, substrate=substrate)
    runtime.initialize()
    if start:
        runtime.start()
    return runtime


def _with_tool(runtime, enable=True, fail=False):
    """Define, register, attach and (optionally) enable a Tool on the Runtime's
    own hosted Tool Ecosystem."""
    tools = runtime.tools
    tool = EchoTool(fail=fail)
    tools.registry.define(
        ToolIdentity(KEY),
        ToolContract(actions=("echo",), required_parameters={"echo": ("message",)}),
        metadata={"phase": "8"},
    )
    tools.registry.register(KEY)
    tools.boundary.register(tool)
    if enable:
        tools.registry.enable(KEY)
    return tool


class E803GovernedInvocationThroughTheRuntime(unittest.TestCase):
    """The path, link by link."""

    def test_the_runtime_is_actually_running(self):
        self.assertIs(RuntimeState.RUNNING, _runtime().state)

    def test_the_execution_is_minted_by_that_runtime(self):
        runtime = _runtime()

        execution = create_execution_layer(runtime)

        self.assertIs(runtime, execution.runtime)

    def test_the_full_chain_is_traversed_and_the_tool_executes(self):
        runtime = _runtime()
        tool = _with_tool(runtime)
        agent = ToolProposingAgent(proposal=(KEY, "echo", {"message": "hi"}))

        agent.participate(create_execution_layer(runtime))

        result, = agent.results
        self.assertIs(InvocationDisposition.SUCCESS, result.disposition)
        self.assertEqual({"message": "hi"}, result.value["echoed"])
        self.assertEqual(1, tool.calls)

    def test_the_governance_used_was_the_runtimes_own(self):
        """The Agent was given no collaborator. Everything it touched was
        resolved from `execution.runtime.tools`."""
        runtime = _runtime()
        _with_tool(runtime)
        agent = ToolProposingAgent(proposal=(KEY, "echo", {"message": "hi"}))

        agent.participate(create_execution_layer(runtime))

        self.assertEqual(1, len(runtime.tools.ledger.records))
        self.assertEqual("participation", runtime.tools.ledger.records[0].invocation_id)

    def test_governance_ran_before_execution(self):
        """A refused invocation leaves a ledger record and an untouched Tool —
        which is only possible if the decision preceded the call."""
        runtime = _runtime()
        tool = _with_tool(runtime, enable=False)
        agent = ToolProposingAgent(proposal=(KEY, "echo", {"message": "hi"}))

        agent.participate(create_execution_layer(runtime))

        self.assertEqual(1, len(runtime.tools.ledger.records))
        self.assertFalse(runtime.tools.ledger.records[0].execution_attempted)
        self.assertEqual(0, tool.calls)

    def test_participation_completes_by_returning_none(self):
        runtime = _runtime()
        _with_tool(runtime)
        agent = ToolProposingAgent(proposal=(KEY, "echo", {"message": "hi"}))

        self.assertIsNone(agent.participate(create_execution_layer(runtime)))

    def test_a_refusal_completes_participation_rather_than_raising(self):
        runtime = _runtime()
        _with_tool(runtime, enable=False)
        agent = ToolProposingAgent(proposal=(KEY, "echo", {"message": "hi"}))

        self.assertIsNone(agent.participate(create_execution_layer(runtime)))
        self.assertEqual(1, len(agent.refused))

    def test_execution_failure_is_reported_through_the_real_path(self):
        runtime = _runtime()
        tool = _with_tool(runtime, fail=True)
        agent = ToolProposingAgent(proposal=(KEY, "echo", {"message": "hi"}))

        agent.participate(create_execution_layer(runtime))

        result, = agent.results
        self.assertTrue(result.is_execution_failure)
        self.assertEqual(1, tool.calls)


class TheRunningGateIsReal(unittest.TestCase):
    """`FD-P8-001 §8.7` — Runtime not lawfully available must refuse access, not
    provide a bypass path to Tool implementation."""

    def test_tools_are_refused_before_the_runtime_is_running(self):
        runtime = _runtime(start=False)

        with self.assertRaises(RuntimeNotRunning):
            runtime.tools

    def test_tools_are_refused_after_the_runtime_stops(self):
        runtime = _runtime()
        _with_tool(runtime)
        runtime.stop()

        with self.assertRaises(RuntimeNotRunning):
            runtime.tools

    def test_the_gate_is_the_runtimes_own_not_the_consumers(self):
        runtime = _runtime(start=False)
        agent = ToolProposingAgent()

        with self.assertRaises(RuntimeNotRunning):
            agent._resolve(type("E", (), {"runtime": runtime})())


class NegativeControlsOnTheRealPath(unittest.TestCase):
    """`ACT-CC-P8-001 §14`. Every one proves non-execution, not merely refusal."""

    def _agent_and_tool(self, **kw):
        runtime = _runtime()
        tool = _with_tool(runtime, **kw)
        return runtime, tool, create_execution_layer(runtime)

    def test_unregistered_tool_does_not_execute(self):
        runtime = _runtime()
        tool = EchoTool()
        runtime.tools.boundary.register(tool)  # attached but never defined
        agent = ToolProposingAgent(proposal=(KEY, "echo", {"message": "x"}))

        agent.participate(create_execution_layer(runtime))

        self.assertTrue(agent.results[0].is_refusal)
        self.assertEqual(0, tool.calls)

    def test_disabled_tool_does_not_execute(self):
        runtime, tool, ex = self._agent_and_tool()
        runtime.tools.registry.disable(KEY)
        agent = ToolProposingAgent(proposal=(KEY, "echo", {"message": "x"}))

        agent.participate(ex)

        self.assertTrue(agent.results[0].is_refusal)
        self.assertEqual(0, tool.calls)

    def test_retired_tool_does_not_execute(self):
        runtime, tool, ex = self._agent_and_tool()
        runtime.tools.registry.retire(KEY)
        agent = ToolProposingAgent(proposal=(KEY, "echo", {"message": "x"}))

        agent.participate(ex)

        self.assertTrue(agent.results[0].is_refusal)
        self.assertEqual(0, tool.calls)

    def test_invalid_invocation_does_not_reach_the_tool(self):
        runtime, tool, ex = self._agent_and_tool()
        agent = ToolProposingAgent(proposal=(KEY, "undeclared", {"message": "x"}))

        agent.participate(ex)

        self.assertTrue(agent.results[0].is_invalid)
        self.assertEqual(0, tool.calls)

    def test_a_missing_required_parameter_does_not_reach_the_tool(self):
        runtime, tool, ex = self._agent_and_tool()
        agent = ToolProposingAgent(proposal=(KEY, "echo", {}))

        agent.participate(ex)

        self.assertTrue(agent.results[0].is_invalid)
        self.assertEqual(0, tool.calls)

    def test_an_unauthorized_caller_class_does_not_execute(self):
        runtime, tool, ex = self._agent_and_tool()
        agent = ToolProposingAgent(
            proposal=(KEY, "echo", {"message": "x"}), caller=CallerClass.UNKNOWN
        )

        agent.participate(ex)

        self.assertTrue(agent.results[0].is_refusal)
        self.assertEqual(0, tool.calls)

    def test_refusal_is_not_relabelled_as_execution_failure(self):
        runtime, tool, ex = self._agent_and_tool()
        runtime.tools.registry.disable(KEY)
        agent = ToolProposingAgent(proposal=(KEY, "echo", {"message": "x"}))

        agent.participate(ex)

        self.assertFalse(agent.results[0].is_execution_failure)
        self.assertEqual(0, tool.calls)

    def test_the_runtime_exposes_no_tool_bypass(self):
        """Runtime is an access host: it carries no invoke, no registration and
        no lifecycle surface of its own."""
        runtime = _runtime()

        for forbidden in ("invoke", "register_tool", "enable_tool", "disable_tool",
                          "retire_tool", "tool_registry"):
            self.assertFalse(hasattr(runtime, forbidden), forbidden)

    def test_the_agent_holds_no_lifecycle_or_boundary_surface(self):
        agent = ToolProposingAgent()

        for forbidden in ("register", "define", "enable", "disable", "retire",
                          "boundary", "registry"):
            self.assertFalse(hasattr(agent, forbidden), forbidden)


if __name__ == "__main__":
    unittest.main()
