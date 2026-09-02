"""
R2-A acceptance evidence — exactly one durable Trace per Agent-Instance action.

`ACT-CC-R1-SYSTEMIC-001` measured the observation axis as the most material
connective-integrity failure in AIOS: the Trace boundary was complete and
**zero** execution paths authored a record. This module is the evidence that the
wire is now connected.

Every assertion below reads **persisted storage through `TraceReader`**, never
the in-memory writer. `ACT-CC-R2A-IMPL-001 §16` is explicit that an in-memory
object is not proof of persistence, and §20 requires the loss test to inspect
observable storage rather than assume the writer was called.

The mandatory test is `RefusalIsAnObservedOutcome` (§19). A governance refusal
must leave **one** record with `status="failure"` *and* prove the protected
operation never ran — `§12`'s *"Trace exists + execution did not occur"*. A test
that checked only the returned result would satisfy neither.

`escalation` is not exercised. `ACT-CC-R2A-IMPL-001 §2` freezes it N/A for R2-A:
the repository has no producing semantic, and inventing one is forbidden.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from consumers.observation import TracedAction, runtime_identity
from consumers.tool_agent import ToolProposingAgent
from consumers.workflow_agent import StepFailed, WorkflowParticipatingAgent
from native_core.core.infrastructure import (
    CallerClass,
    ExternalTool,
    LocalAppendOnlyStorage,
    LocalExecutionSubstrate,
    ToolContract,
    ToolIdentity,
)
from native_core.core.runtime.composition import create_runtime
from native_core.core.runtime.execution import create_execution_layer
from native_core.core.trace import TraceReader, TraceWriter
from native_core.core.workflow import (
    AgentInstanceRef,
    SkillRef,
    Workflow,
    WorkflowComposition,
    WorkflowIdentity,
    WorkflowStep,
)
from native_core.shared import Success

KEY = "r2a-tool"


class CountingTool(ExternalTool):
    """A real Tool whose call counter is the non-execution proof (`§12`)."""

    def __init__(self, fail=False):
        self.calls = 0
        self._fail = fail

    @property
    def canonical_key(self) -> str:
        return KEY

    def invoke(self, action, parameters):
        self.calls += 1
        if self._fail:
            from native_core.shared import Failure

            return Failure(reason="tool declined")
        return Success(value="ok")


def _storage():
    storage = LocalAppendOnlyStorage(Path(tempfile.mkdtemp()))
    storage.provision()
    return storage


def _runtime(storage, runtime_id="r2a-runtime"):
    substrate = LocalExecutionSubstrate()
    substrate.provision()
    runtime = create_runtime(runtime_id=runtime_id, storage=storage, substrate=substrate)
    runtime.initialize()
    runtime.start()
    return runtime


def _with_tool(runtime, enable=True, fail=False):
    tool = CountingTool(fail=fail)
    runtime.tools.registry.define(ToolIdentity(KEY), ToolContract(actions=("go",)))
    runtime.tools.registry.register(KEY)
    runtime.tools.boundary.register(tool)
    if enable:
        runtime.tools.registry.enable(KEY)
    return tool


def _records(storage):
    """Every Trace recovered from durable storage — the only evidence source
    these tests accept."""
    return list(TraceReader(storage).read())


class SuccessIsObservedExactlyOnce(unittest.TestCase):
    """`§17` — one successful action, one durable `success` record."""

    def test_a_successful_action_writes_exactly_one_success_record(self):
        storage = _storage()
        runtime = _runtime(storage)
        tool = _with_tool(runtime)
        agent = ToolProposingAgent(
            proposal=(KEY, "go", {}), trace_writer=TraceWriter(storage)
        )

        agent.participate(create_execution_layer(runtime))
        records = _records(storage)

        self.assertEqual(1, len(records))
        self.assertEqual("success", records[0].status)
        self.assertEqual(1, tool.calls)

    def test_the_record_carries_the_acting_identity_and_host(self):
        """`§16` — correct `agent_instance`, correct `runtime`."""
        storage = _storage()
        runtime = _runtime(storage, runtime_id="named-runtime")
        _with_tool(runtime)
        agent = ToolProposingAgent(
            proposal=(KEY, "go", {}), trace_writer=TraceWriter(storage)
        )

        agent.participate(create_execution_layer(runtime))
        record, = _records(storage)

        self.assertEqual("tool-proposing-agent", record.agent_instance)
        self.assertEqual("named-runtime", record.runtime)

    def test_evidence_survives_the_writer(self):
        """Durability, not object identity: the record is read back through a
        reader that never saw the writer."""
        storage = _storage()
        runtime = _runtime(storage)
        _with_tool(runtime)
        ToolProposingAgent(
            proposal=(KEY, "go", {}), trace_writer=TraceWriter(storage)
        ).participate(create_execution_layer(runtime))

        recovered = list(TraceReader(storage).read())

        self.assertEqual(1, len(recovered))
        self.assertEqual("success", recovered[0].status)


class FailureIsObservedExactlyOnce(unittest.TestCase):
    """`§18` — a failed action leaves durable evidence that it failed."""

    def _workflow_agent(self, storage, performer):
        return WorkflowParticipatingAgent(
            workflow=Workflow(identity=WorkflowIdentity("r2a-flow", "1")),
            composition=WorkflowComposition(
                (
                    WorkflowStep(
                        step_key="a",
                        performed_by=AgentInstanceRef("i-a"),
                        composes=SkillRef("s-a"),
                    ),
                )
            ),
            performer=performer,
            trace_writer=TraceWriter(storage),
        )

    def test_a_failed_action_writes_exactly_one_failure_record(self):
        storage = _storage()
        runtime = _runtime(storage)

        def performer(step):
            raise StepFailed("step declined")

        agent = self._workflow_agent(storage, performer)
        agent.participate(create_execution_layer(runtime))
        records = _records(storage)

        self.assertEqual(1, len(records))
        self.assertEqual("failure", records[0].status)

    def test_failure_evidence_is_durable_not_in_memory(self):
        """The finding this closes: before R2-A a failed action's reason lived
        only in the returned state object and vanished with the process."""
        storage = _storage()
        runtime = _runtime(storage)
        agent = self._workflow_agent(
            storage, lambda step: (_ for _ in ()).throw(StepFailed("boom"))
        )

        agent.participate(create_execution_layer(runtime))
        record, = list(TraceReader(storage).read())

        self.assertEqual("failure", record.status)
        self.assertIn("boom", str(record.outputs))

    def test_a_raising_action_still_writes_before_propagating(self):
        """`§13.3` is unchanged — the error still reaches the caller — and the
        action is still observed exactly once."""
        storage = _storage()
        runtime = _runtime(storage)
        agent = self._workflow_agent(
            storage, lambda step: (_ for _ in ()).throw(ValueError("a real defect"))
        )

        with self.assertRaises(ValueError):
            agent.participate(create_execution_layer(runtime))
        records = _records(storage)

        self.assertEqual(1, len(records))
        self.assertEqual("failure", records[0].status)


class RefusalIsAnObservedOutcome(unittest.TestCase):
    """`§19` — MANDATORY. Refusal produces one failure record **and** proves the
    protected operation never executed."""

    def test_a_refused_action_writes_one_failure_record_and_does_not_execute(self):
        storage = _storage()
        runtime = _runtime(storage)
        tool = _with_tool(runtime, enable=False)   # registered, never enabled
        agent = ToolProposingAgent(
            proposal=(KEY, "go", {}), trace_writer=TraceWriter(storage)
        )

        agent.participate(create_execution_layer(runtime))
        records = _records(storage)

        self.assertEqual(1, len(records), "refusal must be observed exactly once")
        self.assertEqual("failure", records[0].status)
        self.assertEqual(0, tool.calls, "the protected operation must NOT execute")

    def test_the_refusal_record_names_the_governance_disposition(self):
        storage = _storage()
        runtime = _runtime(storage)
        _with_tool(runtime, enable=False)
        agent = ToolProposingAgent(
            proposal=(KEY, "go", {}), trace_writer=TraceWriter(storage)
        )

        agent.participate(create_execution_layer(runtime))
        record, = _records(storage)

        self.assertIn("GOVERNANCE_REFUSAL", str(record.outputs))

    def test_an_unauthorized_caller_is_observed_and_does_not_execute(self):
        storage = _storage()
        runtime = _runtime(storage)
        tool = _with_tool(runtime)
        agent = ToolProposingAgent(
            proposal=(KEY, "go", {}),
            caller=CallerClass.UNKNOWN,
            trace_writer=TraceWriter(storage),
        )

        agent.participate(create_execution_layer(runtime))
        records = _records(storage)

        self.assertEqual(1, len(records))
        self.assertEqual("failure", records[0].status)
        self.assertEqual(0, tool.calls)


class ExactlyOneIsEnforced(unittest.TestCase):
    """`§20`, `§21` — loss and duplication are both detectable from storage."""

    def test_zero_traces_is_detectable(self):
        """The loss test. Fresh storage with no action yields no record — the
        baseline that makes a missing Trace visible."""
        self.assertEqual(0, len(_records(_storage())))

    def test_one_action_never_yields_two_records(self):
        storage = _storage()
        runtime = _runtime(storage)
        _with_tool(runtime)
        ToolProposingAgent(
            proposal=(KEY, "go", {}), trace_writer=TraceWriter(storage)
        ).participate(create_execution_layer(runtime))

        self.assertEqual(1, len(_records(storage)))

    def test_duplication_would_be_detected(self):
        """Negative control on the detector itself: two writes are visibly two
        records, so the exactly-one assertions above are not vacuous."""
        storage = _storage()
        writer = TraceWriter(storage)
        for _ in range(2):
            action = TracedAction(writer, agent_instance="probe", runtime="rt")
            with action:
                pass

        self.assertEqual(2, len(_records(storage)))

    def test_a_reentered_action_still_writes_once(self):
        """`§13` — the guard that makes exactly-one structural rather than
        conventional."""
        storage = _storage()
        action = TracedAction(TraceWriter(storage), agent_instance="probe", runtime="rt")
        with action:
            pass
        self.assertTrue(action.written)
        action.__exit__(None, None, None)      # a second exit must not re-write

        self.assertEqual(1, len(_records(storage)))

    def test_two_actions_yield_two_records(self):
        storage = _storage()
        runtime = _runtime(storage)
        _with_tool(runtime)
        execution = create_execution_layer(runtime)
        for _ in range(2):
            ToolProposingAgent(
                proposal=(KEY, "go", {}), trace_writer=TraceWriter(storage)
            ).participate(execution)

        self.assertEqual(2, len(_records(storage)))


class CrossPhaseContextIsCarried(unittest.TestCase):
    """`§22` — real populated context, no synthetic values."""

    def test_a_tool_action_records_the_tool_it_reached(self):
        storage = _storage()
        runtime = _runtime(storage)
        _with_tool(runtime)
        ToolProposingAgent(
            proposal=(KEY, "go", {}), trace_writer=TraceWriter(storage)
        ).participate(create_execution_layer(runtime))
        record, = _records(storage)

        self.assertIn(KEY, record.tools_used)

    def test_a_workflow_action_records_its_outputs(self):
        storage = _storage()
        runtime = _runtime(storage)
        WorkflowParticipatingAgent(
            workflow=Workflow(identity=WorkflowIdentity("ctx-flow", "1")),
            composition=WorkflowComposition(
                (
                    WorkflowStep(
                        step_key="a",
                        performed_by=AgentInstanceRef("i-a"),
                        composes=SkillRef("s-a"),
                    ),
                )
            ),
            trace_writer=TraceWriter(storage),
        ).participate(create_execution_layer(runtime))
        record, = _records(storage)

        self.assertIn("ctx-flow", record.skills_used)
        self.assertIn("a", str(record.outputs))

    def test_unexercised_context_stays_empty_rather_than_fabricated(self):
        """`§9` forbids inventing context. A Tool action consumed no Knowledge
        and no Memory, and the record says so by being empty."""
        storage = _storage()
        runtime = _runtime(storage)
        _with_tool(runtime)
        ToolProposingAgent(
            proposal=(KEY, "go", {}), trace_writer=TraceWriter(storage)
        ).participate(create_execution_layer(runtime))
        record, = _records(storage)

        self.assertEqual((), record.knowledge_consumed)
        self.assertEqual((), record.memory_consumed)


class AuthorshipStaysWhereCanonPutsIt(unittest.TestCase):
    """`§23`–`§26` — the boundaries R2-A must not move."""

    def test_an_agent_without_a_writer_authors_nothing(self):
        """Provisioning is injected, never assumed: the pre-R2-A behaviour is
        unchanged for an Agent given no writer."""
        storage = _storage()
        runtime = _runtime(storage)
        _with_tool(runtime)

        ToolProposingAgent(proposal=(KEY, "go", {})).participate(
            create_execution_layer(runtime)
        )

        self.assertEqual(0, len(_records(storage)))

    def test_the_runtime_exposes_no_trace_surface(self):
        """`§23` — Runtime is not the author and holds no accessor."""
        runtime = _runtime(_storage())

        for forbidden in ("trace", "traces", "trace_writer", "tracing", "evidence"):
            self.assertFalse(hasattr(runtime, forbidden), forbidden)

    def test_infrastructure_supplies_capability_not_meaning(self):
        """`§26` — the writer takes a record; it decides no status."""
        writer = TraceWriter(_storage())

        self.assertEqual(["write"], [m for m in dir(writer) if not m.startswith("_")])

    def test_runtime_identity_is_read_never_fabricated(self):
        """An Execution stand-in carrying no runtime yields an explicit
        placeholder, not an invented identity (`§9`)."""
        self.assertEqual(
            "unknown-runtime", runtime_identity(type("E", (), {"runtime": None})())
        )


if __name__ == "__main__":
    unittest.main()
