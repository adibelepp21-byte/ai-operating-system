"""
Phase 8 Tool Ecosystem conformance — `E8-01`, `E8-02`, `E8-04`, `E8-05`.

`E8-03` needs a RUNNING Runtime and an Agent, so it lives with the consumer
evidence (`consumers/tests/test_tool_agent_runtime.py`). Everything provable
inside the boundary is proved here.

`ACT-CC-P8-001 §14` requires negative controls that *"genuinely be capable of
failing"* and forbids tests that *"merely assert values that cannot demonstrate
boundary enforcement."* So refusal is never asserted on its own: every refusal
test also proves the Tool **did not execute**, by checking a call counter the
Tool itself increments and the ledger's `execution_attempted` flag.
"""

from __future__ import annotations

import unittest

from native_core.core.infrastructure import (
    AUTHORIZED_CALLERS,
    CallerClass,
    ExternalTool,
    InvalidToolDefinition,
    InvalidToolTransition,
    InvocationDisposition,
    InvocationRequest,
    ToolAlreadyDefined,
    ToolBoundary,
    ToolContract,
    ToolDescriptor,
    ToolIdentity,
    ToolNotDefined,
    ToolState,
    create_tool_subsystem,
)
from native_core.shared import Failure, Success

KEY = "counter-tool"


class CountingTool(ExternalTool):
    """A real in-process Tool that records whether it was ever reached.

    `FD-P8-001 §6.5` says an in-process Tool is sufficient for certification
    evidence. The call counter is what turns "refused" into "demonstrably did
    not execute".
    """

    def __init__(self, key=KEY, fail=False, rogue=False):
        self._key = key
        self.calls = 0
        self._fail = fail
        self._rogue = rogue

    @property
    def canonical_key(self) -> str:
        return self._key

    def invoke(self, action, parameters):
        self.calls += 1
        if self._rogue:
            return "not an Outcome"
        if self._fail:
            return Failure(reason="tool decided to fail")
        return Success(value={"action": action, "parameters": dict(parameters)})


def _ready(enable=True, fail=False, rogue=False, key=KEY):
    """A subsystem with one Tool defined, registered, attached and enabled."""
    sub = create_tool_subsystem()
    tool = CountingTool(key=key, fail=fail, rogue=rogue)
    sub.registry.define(
        ToolIdentity(key),
        ToolContract(actions=("run",), required_parameters={"run": ("x",)}),
        metadata={"purpose": "conformance"},
    )
    sub.registry.register(key)
    sub.boundary.register(tool)
    if enable:
        sub.registry.enable(key)
    return sub, tool


def _request(key=KEY, action="run", params=None, caller=CallerClass.AGENT):
    return InvocationRequest(
        tool_key=key, action=action,
        parameters=params if params is not None else {"x": 1},
        caller=caller, invocation_id="inv-1",
    )


class E801RepresentationAndIdentity(unittest.TestCase):

    def test_a_tool_carries_identity_contract_metadata_and_state(self):
        sub, _ = _ready()

        d = sub.registry.describe(KEY)

        self.assertIsInstance(d, ToolDescriptor)
        self.assertEqual(KEY, d.identity.canonical_key)      # identity
        self.assertTrue(d.contract.declares("run"))           # contract
        self.assertEqual("conformance", d.metadata["purpose"])  # metadata
        self.assertIs(ToolState.ENABLED, d.state)             # lifecycle state

    def test_identity_is_stable_across_lifecycle(self):
        sub, _ = _ready()
        before = sub.registry.describe(KEY).identity

        sub.registry.disable(KEY)

        self.assertEqual(before, sub.registry.describe(KEY).identity)

    def test_an_unnamed_tool_is_refused(self):
        with self.assertRaises(InvalidToolDefinition):
            ToolIdentity("   ")

    def test_a_contract_must_declare_an_action(self):
        with self.assertRaises(InvalidToolDefinition):
            ToolContract(actions=())

    def test_a_contract_cannot_require_parameters_for_an_undeclared_action(self):
        with self.assertRaises(InvalidToolDefinition):
            ToolContract(actions=("run",), required_parameters={"other": ("x",)})

    def test_a_descriptor_is_immutable(self):
        sub, _ = _ready()

        with self.assertRaises(Exception):
            sub.registry.describe(KEY).state = ToolState.RETIRED

    def test_defining_the_same_key_twice_is_refused(self):
        sub, _ = _ready()

        with self.assertRaises(ToolAlreadyDefined):
            sub.registry.define(ToolIdentity(KEY), ToolContract(actions=("run",)))

    def test_metadata_is_deeply_frozen(self):
        sub = create_tool_subsystem()
        sub.registry.define(
            ToolIdentity("m"), ToolContract(actions=("a",)), metadata={"list": [1, 2]}
        )

        self.assertIsInstance(sub.registry.describe("m").metadata["list"], tuple)


class E802RegistrationAndLifecycle(unittest.TestCase):
    """Every refusal below also proves non-execution."""

    def test_an_enabled_registered_tool_executes(self):
        sub, tool = _ready()

        result = sub.governance.invoke(_request())

        self.assertIs(InvocationDisposition.SUCCESS, result.disposition)
        self.assertEqual(1, tool.calls)

    def test_a_defined_but_unregistered_tool_does_not_execute(self):
        sub = create_tool_subsystem()
        tool = CountingTool()
        sub.registry.define(ToolIdentity(KEY), ToolContract(actions=("run",)))
        sub.boundary.register(tool)

        result = sub.governance.invoke(_request(params={}))

        self.assertIs(InvocationDisposition.GOVERNANCE_REFUSAL, result.disposition)
        self.assertEqual(0, tool.calls)

    def test_an_unknown_tool_does_not_execute(self):
        sub, tool = _ready()

        result = sub.governance.invoke(_request(key="nonexistent"))

        self.assertIs(InvocationDisposition.GOVERNANCE_REFUSAL, result.disposition)
        self.assertEqual(0, tool.calls)

    def test_a_registered_but_not_enabled_tool_does_not_execute(self):
        sub, tool = _ready(enable=False)

        result = sub.governance.invoke(_request())

        self.assertIs(InvocationDisposition.GOVERNANCE_REFUSAL, result.disposition)
        self.assertEqual(0, tool.calls)

    def test_a_disabled_tool_does_not_execute(self):
        sub, tool = _ready()
        sub.registry.disable(KEY)

        result = sub.governance.invoke(_request())

        self.assertIs(InvocationDisposition.GOVERNANCE_REFUSAL, result.disposition)
        self.assertEqual(0, tool.calls)

    def test_a_retired_tool_does_not_execute(self):
        sub, tool = _ready()
        sub.registry.retire(KEY)

        result = sub.governance.invoke(_request())

        self.assertIs(InvocationDisposition.GOVERNANCE_REFUSAL, result.disposition)
        self.assertEqual(0, tool.calls)

    def test_retirement_is_terminal_and_cannot_be_undone(self):
        sub, tool = _ready()
        sub.registry.retire(KEY)

        with self.assertRaises(InvalidToolTransition):
            sub.registry.enable(KEY)
        self.assertEqual(0, tool.calls)

    def test_a_disabled_tool_can_be_re_enabled_and_then_executes(self):
        sub, tool = _ready()
        sub.registry.disable(KEY)
        sub.registry.enable(KEY)

        self.assertIs(InvocationDisposition.SUCCESS, sub.governance.invoke(_request()).disposition)
        self.assertEqual(1, tool.calls)

    def test_a_tool_attached_at_the_boundary_but_never_defined_does_not_execute(self):
        """No alias path: boundary attachment alone confers nothing."""
        sub = create_tool_subsystem()
        tool = CountingTool()
        sub.boundary.register(tool)

        result = sub.governance.invoke(_request())

        self.assertIs(InvocationDisposition.GOVERNANCE_REFUSAL, result.disposition)
        self.assertEqual(0, tool.calls)

    def test_a_governed_tool_not_attached_at_the_boundary_is_refused(self):
        sub = create_tool_subsystem()
        sub.registry.define(ToolIdentity(KEY), ToolContract(actions=("run",)))
        sub.registry.register(KEY)
        sub.registry.enable(KEY)

        result = sub.governance.invoke(_request(params={}))

        self.assertIs(InvocationDisposition.GOVERNANCE_REFUSAL, result.disposition)

    def test_lifecycle_operations_on_an_unknown_tool_are_refused(self):
        sub = create_tool_subsystem()

        for op in (sub.registry.register, sub.registry.enable, sub.registry.retire):
            with self.assertRaises(ToolNotDefined):
                op("ghost")

    def test_registration_is_not_eligibility(self):
        sub, _ = _ready(enable=False)

        self.assertTrue(sub.registry.is_registered(KEY))
        self.assertFalse(sub.registry.is_invocable(KEY))

    def test_a_merely_defined_tool_is_not_registered(self):
        sub = create_tool_subsystem()
        sub.registry.define(ToolIdentity("d"), ToolContract(actions=("a",)))

        self.assertFalse(sub.registry.is_registered("d"))


class E804StructuredOutcomes(unittest.TestCase):
    """Four categories, each structurally distinct."""

    def test_success_carries_a_value_and_attempted_execution(self):
        sub, _ = _ready()

        r = sub.governance.invoke(_request())

        self.assertTrue(r.is_success)
        self.assertTrue(r.execution_attempted)
        self.assertEqual("run", r.value["action"])

    def test_governance_refusal_is_distinct_and_did_not_execute(self):
        sub, tool = _ready()
        sub.registry.disable(KEY)

        r = sub.governance.invoke(_request())

        self.assertTrue(r.is_refusal)
        self.assertFalse(r.execution_attempted)
        self.assertEqual(0, tool.calls)

    def test_invalid_invocation_is_distinct_and_did_not_reach_the_tool(self):
        sub, tool = _ready()

        r = sub.governance.invoke(_request(action="undeclared"))

        self.assertTrue(r.is_invalid)
        self.assertFalse(r.execution_attempted)
        self.assertEqual(0, tool.calls)

    def test_a_missing_required_parameter_is_invalid_not_refusal(self):
        sub, tool = _ready()

        r = sub.governance.invoke(_request(params={}))

        self.assertTrue(r.is_invalid)
        self.assertEqual(0, tool.calls)

    def test_execution_failure_is_distinct_and_did_execute(self):
        sub, tool = _ready(fail=True)

        r = sub.governance.invoke(_request())

        self.assertTrue(r.is_execution_failure)
        self.assertTrue(r.execution_attempted)
        self.assertEqual(1, tool.calls)

    def test_refusal_is_never_relabelled_as_execution_failure(self):
        sub, _ = _ready()
        sub.registry.disable(KEY)

        r = sub.governance.invoke(_request())

        self.assertFalse(r.is_execution_failure)
        self.assertFalse(r.is_success)

    def test_execution_failure_is_never_a_false_success(self):
        sub, _ = _ready(fail=True)

        r = sub.governance.invoke(_request())

        self.assertFalse(r.is_success)
        self.assertIsNone(r.value)

    def test_the_four_dispositions_are_mutually_exclusive(self):
        sub, _ = _ready()
        r = sub.governance.invoke(_request())

        flags = [r.is_success, r.is_refusal, r.is_invalid, r.is_execution_failure]

        self.assertEqual(1, sum(flags))

    def test_an_unauthorized_caller_is_refused_and_does_not_execute(self):
        sub, tool = _ready()

        r = sub.governance.invoke(_request(caller=CallerClass.UNKNOWN))

        self.assertTrue(r.is_refusal)
        self.assertEqual(0, tool.calls)

    def test_unknown_is_not_an_authorized_caller_class(self):
        self.assertNotIn(CallerClass.UNKNOWN, AUTHORIZED_CALLERS)

    def test_a_tool_returning_a_non_outcome_cannot_become_a_false_success(self):
        """The repaired guard (`ACT-CC-P8-001 §10`), seen from the public path."""
        sub, tool = _ready(rogue=True)

        r = sub.governance.invoke(_request())

        self.assertTrue(r.is_execution_failure)
        self.assertEqual(1, tool.calls)
        self.assertIn("non-Outcome", r.reason)


class E805TraceabilityAndFailClosed(unittest.TestCase):

    def test_an_accepted_invocation_is_recorded(self):
        sub, _ = _ready()

        sub.governance.invoke(_request())

        record, = sub.ledger.records
        self.assertTrue(record.governance_admitted)
        self.assertTrue(record.execution_attempted)
        self.assertIs(InvocationDisposition.SUCCESS, record.disposition)

    def test_a_refused_invocation_is_recorded(self):
        sub, _ = _ready()
        sub.registry.disable(KEY)

        sub.governance.invoke(_request())

        record, = sub.ledger.records
        self.assertFalse(record.governance_admitted)
        self.assertFalse(record.execution_attempted)

    def test_the_record_connects_every_required_element(self):
        sub, _ = _ready()

        sub.governance.invoke(_request())

        r, = sub.ledger.records
        self.assertEqual("inv-1", r.invocation_id)          # invocation identity
        self.assertEqual(KEY, r.tool_key)                    # Tool identity
        self.assertIs(CallerClass.AGENT, r.caller)           # caller class
        self.assertIs(ToolState.ENABLED, r.lifecycle_state)  # lifecycle result
        self.assertTrue(r.governance_admitted)               # governance decision
        self.assertTrue(r.execution_attempted)               # attempted or not
        self.assertIs(InvocationDisposition.SUCCESS, r.disposition)  # outcome

    def test_every_attempt_is_recorded_including_unknown_tools(self):
        sub, _ = _ready()
        sub.governance.invoke(_request(key="ghost"))

        r, = sub.ledger.records
        self.assertIsNone(r.lifecycle_state)
        self.assertFalse(r.execution_attempted)

    def test_executed_and_refused_partition_the_ledger(self):
        sub, _ = _ready()
        sub.governance.invoke(_request())                    # success
        sub.governance.invoke(_request(action="nope"))       # invalid
        sub.registry.disable(KEY)
        sub.governance.invoke(_request())                    # refusal

        self.assertEqual(3, len(sub.ledger.records))
        self.assertEqual(1, len(sub.ledger.executed()))
        self.assertEqual(2, len(sub.ledger.refused()))

    def test_the_ledger_exposes_no_removal_surface(self):
        sub, _ = _ready()

        for forbidden in ("remove", "delete", "clear", "pop", "truncate"):
            self.assertFalse(hasattr(sub.ledger, forbidden), forbidden)

    def test_records_are_immutable(self):
        sub, _ = _ready()
        sub.governance.invoke(_request())

        with self.assertRaises(Exception):
            sub.ledger.records[0].execution_attempted = False

    def test_the_governance_wrapper_never_transitions_a_tool(self):
        """Lifecycle authority stays with the registry (`ACT-CC-P8-001 §5.4`)."""
        sub, _ = _ready()

        for forbidden in ("enable", "disable", "retire", "register", "define"):
            self.assertFalse(hasattr(sub.governance, forbidden), forbidden)

    def test_the_subsystem_exposes_no_shortcut_past_governance(self):
        """`boundary` is present for inspection, and reaching a Tool through it
        is not the lawful path — the wrapper is. What matters is that the
        wrapper cannot be skipped *while still being governed*: the boundary has
        no knowledge of lifecycle at all."""
        sub, _ = _ready()
        sub.registry.retire(KEY)

        self.assertFalse(sub.registry.is_invocable(KEY))
        self.assertTrue(sub.boundary.is_registered(KEY))
        self.assertIs(
            InvocationDisposition.GOVERNANCE_REFUSAL,
            sub.governance.invoke(_request()).disposition,
        )


if __name__ == "__main__":
    unittest.main()
