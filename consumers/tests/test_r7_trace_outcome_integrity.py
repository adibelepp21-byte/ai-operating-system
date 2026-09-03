"""
`ACT-CC-R7` — the Trace a Tool invocation leaves must say what actually happened.

`ACT-CC-R6-SYSTEMIC-001` proved, on a real Runtime, that an invocation which
reached the Tool and came back `EXECUTION_FAILURE` was filed as
`Trace.status="success"`. The producer branched on `execution_attempted`, and an
execution failure has `execution_attempted=True`, so it fell to the success
side. Because `tools/derived_views.py` selects failures by `status == "failure"`,
a genuinely failed invocation was invisible to the system's own self-knowledge —
and Trace is append-only, so each such record was permanently wrong.

These tests lock the corrected invariant: **only `SUCCESS` is a success.** Every
other ratified disposition is a failure, whether or not the Tool was reached.

`execution_attempted` is not weakened by this and is asserted alongside every
case below: it remains the evidence about whether *protected execution occurred*,
which is a different question from whether the action *succeeded*. The
`InvocationLedger` still separates executed from refused, so both facts stay
independently observable — `§7` requires exactly that distinction be preserved.

Every fixture here is a real Runtime with a real Tool at a real boundary; the
counters on `CountingTool` are what make "refused" mean "never ran".

The downstream half of the evidence — that a corrected `failure` record actually
reaches `tools/derived_views.py` — lives in `tools/tests/test_r7_failure_visibility.py`.
It cannot live here: `consumers/` may depend on nothing in `tools/`, and
`test_reference_agent.TestResidency` enforces that over this whole region,
test files included.
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
    LocalAppendOnlyStorage,
    LocalExecutionSubstrate,
    ToolContract,
    ToolIdentity,
)
from native_core.core.runtime.composition import create_runtime
from native_core.core.runtime.execution import create_execution_layer
from native_core.core.trace import TraceReader, TraceWriter, new_record
from native_core.core.trace.record import REQUIRED_FIELDS
from native_core.shared import Failure, Success

TOOL_KEY = "r7.tool"


class CountingTool(ExternalTool):
    """A real Tool at the real boundary. `calls` is the evidence that a refusal
    meant the Tool was never reached — an assertion about the disposition alone
    could not establish that."""

    def __init__(self, fail: bool = False):
        self._fail = fail
        self.calls = 0

    @property
    def canonical_key(self) -> str:
        return TOOL_KEY

    def invoke(self, action, parameters):
        self.calls += 1
        if self._fail:
            return Failure(reason="the tool declined the action")
        return Success(value={"action": action})


def _fixture(fail=False, caller=CallerClass.AGENT, action="run"):
    """One real Runtime, one real Tool, one participation. Returns everything an
    assertion might need to distinguish outcome from execution."""
    storage = LocalAppendOnlyStorage(Path(tempfile.mkdtemp()))
    storage.provision()
    substrate = LocalExecutionSubstrate()
    substrate.provision()
    runtime = create_runtime(runtime_id="r7-runtime", storage=storage, substrate=substrate)
    runtime.initialize()
    runtime.start()

    tool = CountingTool(fail=fail)
    runtime.tools.boundary.register(tool)
    runtime.tools.registry.define(
        ToolIdentity(canonical_key=TOOL_KEY), ToolContract(actions=("run",))
    )
    runtime.tools.registry.register(TOOL_KEY)
    runtime.tools.registry.enable(TOOL_KEY)

    trace_storage = LocalAppendOnlyStorage(Path(tempfile.mkdtemp()))
    trace_storage.provision()
    writer, reader = TraceWriter(trace_storage), TraceReader(trace_storage)

    agent = ToolProposingAgent(
        proposal=(TOOL_KEY, action, {}), caller=caller, trace_writer=writer
    )
    agent.participate(create_execution_layer(runtime))

    return agent.results[0], list(reader.read()), tool, runtime, reader


class OutcomeDeterminesTraceStatus(unittest.TestCase):
    """`§9` T-01 … T-04 — the mapping, one case per ratified disposition."""

    def test_t01_a_successful_invocation_records_success(self):
        result, records, tool, _, _ = _fixture()

        self.assertIs(InvocationDisposition.SUCCESS, result.disposition)
        self.assertTrue(result.execution_attempted)
        self.assertEqual(1, tool.calls)
        self.assertEqual(1, len(records))
        self.assertEqual("success", records[0].status)

    def test_t02_an_execution_failure_records_failure(self):
        """The R6 defect, locked. This case fails on the pre-fix implementation:
        the Tool *was* reached, so `execution_attempted` is True, and the old
        branch filed it as `success`."""
        result, records, tool, _, _ = _fixture(fail=True)

        self.assertIs(InvocationDisposition.EXECUTION_FAILURE, result.disposition)
        self.assertTrue(result.execution_attempted)
        self.assertEqual(1, tool.calls, "the failure is a real one: the Tool ran")
        self.assertEqual(1, len(records))
        self.assertEqual("failure", records[0].status)

    def test_t03_a_governance_refusal_still_records_failure(self):
        """Correcting the execution-failure branch must not disturb refusal
        semantics, which were already right."""
        result, records, tool, runtime, _ = _fixture(caller=CallerClass.UNKNOWN)

        self.assertIs(InvocationDisposition.GOVERNANCE_REFUSAL, result.disposition)
        self.assertFalse(result.execution_attempted)
        self.assertEqual(0, tool.calls)
        self.assertEqual("failure", records[0].status)
        self.assertEqual(1, len(runtime.tools.ledger.refused()))
        self.assertEqual(0, len(runtime.tools.ledger.executed()))

    def test_t04_status_follows_the_outcome_not_the_execution_attempt(self):
        """The whole table at once. The two `True` rows disagreeing on status is
        the point: `execution_attempted` cannot be the predicate, because it
        does not distinguish a Tool that worked from a Tool that failed."""
        success, refusal = _fixture(), _fixture(caller=CallerClass.UNKNOWN)
        failure = _fixture(fail=True)

        observed = [
            (r.disposition, r.execution_attempted, recs[0].status)
            for r, recs, _, _, _ in (success, failure, refusal)
        ]

        self.assertEqual(
            [
                (InvocationDisposition.SUCCESS, True, "success"),
                (InvocationDisposition.EXECUTION_FAILURE, True, "failure"),
                (InvocationDisposition.GOVERNANCE_REFUSAL, False, "failure"),
            ],
            observed,
        )

    def test_an_invalid_invocation_keeps_the_semantics_it_already_had(self):
        """`NC-03` — no outcome is invented for `INVALID_INVOCATION`. It was a
        failure before this change and remains one, by the same rule."""
        result, records, tool, _, _ = _fixture(action="not-a-declared-action")

        self.assertIs(InvocationDisposition.INVALID_INVOCATION, result.disposition)
        self.assertFalse(result.execution_attempted)
        self.assertEqual(0, tool.calls)
        self.assertEqual("failure", records[0].status)


class NegativeControls(unittest.TestCase):
    """`§13` — the properties whose violation would mean the correction went
    further than it was authorized to go."""

    def test_nc01_no_execution_failure_can_produce_a_success_record(self):
        for _ in range(3):
            _, records, tool, _, _ = _fixture(fail=True)
            self.assertEqual(1, tool.calls)
            self.assertNotEqual("success", records[0].status)

    def test_nc02_refusal_still_executes_nothing(self):
        _, records, tool, runtime, _ = _fixture(caller=CallerClass.UNKNOWN)

        self.assertEqual(0, tool.calls)
        self.assertEqual(0, len(runtime.tools.ledger.executed()))
        self.assertEqual("failure", records[0].status)

    def test_nc04_a_pre_existing_record_is_never_rewritten(self):
        """Historical evidence stays historical. A record written the old way —
        `EXECUTION_FAILURE` filed as `success` — is still there, unchanged,
        beside a correctly-written new one. `§12` forbids migrating it."""
        storage = LocalAppendOnlyStorage(Path(tempfile.mkdtemp()))
        storage.provision()
        writer, reader = TraceWriter(storage), TraceReader(storage)
        writer.write(
            new_record(
                agent_definition_version="unversioned",
                agent_instance="tool-proposing-agent",
                runtime="legacy",
                outputs={"disposition": "EXECUTION_FAILURE"},
                status="success",   # the defect, as history recorded it
            )
        )
        writer.write(
            new_record(
                agent_definition_version="unversioned",
                agent_instance="tool-proposing-agent",
                runtime="corrected",
                outputs={"reason": "EXECUTION_FAILURE for r7.tool.run"},
                status="failure",
            )
        )

        history = list(reader.read())

        self.assertEqual(2, len(history))
        self.assertEqual("success", history[0].status, "history is not rewritten")
        self.assertEqual("failure", history[1].status)

    def test_nc05_the_trace_schema_is_unchanged(self):
        _, records, _, _, _ = _fixture(fail=True)

        self.assertEqual(set(REQUIRED_FIELDS), set(records[0].to_mapping()))
        self.assertEqual(10, len(REQUIRED_FIELDS))

    def test_the_correction_added_no_status_value(self):
        from native_core.core.trace.record import VALID_STATUSES

        self.assertEqual({"success", "failure", "escalation"}, set(VALID_STATUSES))

    def test_exactly_one_record_is_written_per_action(self):
        for kwargs in ({}, {"fail": True}, {"caller": CallerClass.UNKNOWN}):
            _, records, _, _, _ = _fixture(**kwargs)
            self.assertEqual(1, len(records), kwargs)


if __name__ == "__main__":
    unittest.main()
