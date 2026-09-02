"""
`E9-03` evidence — Runtime-mediated Workflow execution on the real path.

`ACT-CC-P9-001 §14` requires a real authorized execution in which *"Workflow
semantics remain Workflow-owned; Runtime serves as access/execution host;
execution occurs through the reconciled Runtime ↔ Workflow relationship"*, and
`§19 Step 10` requires real-path evidence rather than mocks. So this module
builds a real Runtime with the resident `E-01` pattern, and every lifecycle the
Agent touches is the **Runtime's own hosted subsystem** — several tests assert
identity against `runtime.workflows` so a passing result cannot come from a
collaborator the test handed in.

`§14` also requires negative controls that genuinely fail closed. Each refusal
below is proved twice: the lifecycle refuses, **and** the performer's own call
counter shows the work was never reached.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from consumers.workflow_agent import StepFailed, WorkflowParticipatingAgent
from native_core.core.infrastructure import (
    LocalAppendOnlyStorage,
    LocalExecutionSubstrate,
)
from native_core.core.runtime import RuntimeState
from native_core.core.runtime.composition import create_runtime
from native_core.core.runtime.exceptions import RuntimeNotRunning
from native_core.core.runtime.execution import create_execution_layer
from native_core.core.workflow import (
    AgentInstanceRef,
    DuplicateWorkflowLifecycle,
    SkillRef,
    UnknownWorkflowLifecycle,
    Workflow,
    WorkflowComposition,
    WorkflowIdentity,
    WorkflowLifecycle,
    WorkflowState,
    WorkflowStep,
)

IDENTITY = WorkflowIdentity(workflow_key="p9-flow", workflow_version="1")


class CountingPerformer:
    """A real in-process step performer whose call counter is the negative
    controls' evidence that refusal meant non-execution."""

    def __init__(self, fail_on=None):
        self.calls = 0
        self.seen = []
        self._fail_on = fail_on

    def __call__(self, step):
        self.calls += 1
        self.seen.append(step.step_key)
        if step.step_key == self._fail_on:
            raise StepFailed(f"{step.step_key} declined")


def _runtime(start=True, runtime_id="p9-001-runtime"):
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


def _composition(*keys):
    return WorkflowComposition(
        tuple(
            WorkflowStep(
                step_key=key,
                performed_by=AgentInstanceRef(f"instance-{key}"),
                composes=SkillRef(f"skill-{key}"),
            )
            for key in keys
        )
    )


def _agent(performer=None, keys=("s1", "s2"), identity=IDENTITY):
    """No subsystem is injected: everything is resolved from the Runtime."""
    return WorkflowParticipatingAgent(
        workflow=Workflow(identity=identity),
        composition=_composition(*keys),
        performer=performer,
    )


class E903RuntimeMediatedExecution(unittest.TestCase):
    """The path, link by link."""

    def test_the_runtime_is_actually_running(self):
        self.assertIs(RuntimeState.RUNNING, _runtime().state)

    def test_the_execution_is_minted_by_that_runtime(self):
        runtime = _runtime()

        execution = create_execution_layer(runtime)

        self.assertIs(runtime, execution.runtime)

    def test_the_full_chain_is_traversed_and_the_workflow_succeeds(self):
        runtime = _runtime()
        performer = CountingPerformer()
        agent = _agent(performer)

        final = agent.participate(create_execution_layer(runtime))

        self.assertIs(WorkflowState.SUCCEEDED, final.state)
        self.assertEqual(2, performer.calls)
        self.assertEqual(("s1", "s2"), agent.completed_steps)

    def test_the_lifecycle_used_was_the_runtimes_own(self):
        """The Agent was given no collaborator. Everything it touched was
        resolved from `execution.runtime.workflows`."""
        runtime = _runtime()
        agent = _agent(CountingPerformer())

        agent.participate(create_execution_layer(runtime))

        self.assertEqual((IDENTITY,), runtime.workflows.monitor.monitored())
        self.assertIs(
            WorkflowState.SUCCEEDED,
            runtime.workflows.monitor.state_of(IDENTITY).state,
        )

    def test_state_is_observable_through_the_hosted_monitor(self):
        """`E9-04` on the real path: the four `§12.4` questions, answered from
        the Runtime's own hosted monitoring surface."""
        runtime = _runtime()
        agent = _agent(CountingPerformer(fail_on="s2"))

        agent.participate(create_execution_layer(runtime))
        monitor = runtime.workflows.monitor

        self.assertIn(IDENTITY, monitor.monitored())
        self.assertFalse(monitor.is_active(IDENTITY))
        self.assertTrue(monitor.is_terminal(IDENTITY))
        self.assertTrue(monitor.is_failure(IDENTITY))
        self.assertFalse(monitor.is_success(IDENTITY))

    def test_execution_failure_is_reported_through_the_real_path(self):
        runtime = _runtime()
        performer = CountingPerformer(fail_on="s1")
        agent = _agent(performer)

        final = agent.participate(create_execution_layer(runtime))

        self.assertIs(WorkflowState.FAILED, final.state)
        self.assertEqual("s1 declined", final.detail["reason"])
        self.assertEqual(1, performer.calls)

    def test_workflow_semantics_stayed_workflow_owned(self):
        """The object that decided every transition is the Workflow boundary's
        own type, reached through the Runtime rather than reimplemented by it."""
        runtime = _runtime()

        self.assertIsInstance(runtime.workflows.lifecycle, WorkflowLifecycle)
        self.assertIs(
            WorkflowLifecycle,
            type(runtime.workflows.lifecycle),
        )

    def test_the_hosted_subsystem_is_returned_unchanged(self):
        """Runtime hands back exactly what the composition root assembled — it
        wraps, filters and decorates nothing."""
        runtime = _runtime()

        self.assertIs(runtime.workflows, runtime.workflows)
        self.assertIs(
            runtime.workflows.lifecycle, runtime.workflows.monitor._lifecycle
        )


class TheRunningGateIsReal(unittest.TestCase):
    """`ACT-CC-P9-001 §14` — the required Runtime execution gate is enforced."""

    def test_workflows_are_refused_before_the_runtime_is_running(self):
        runtime = _runtime(start=False)

        with self.assertRaises(RuntimeNotRunning):
            runtime.workflows

    def test_workflows_are_refused_after_the_runtime_stops(self):
        runtime = _runtime()
        runtime.workflows.lifecycle.define(Workflow(identity=IDENTITY))
        runtime.stop()

        with self.assertRaises(RuntimeNotRunning):
            runtime.workflows

    def test_the_gate_is_the_runtimes_own_not_the_consumers(self):
        runtime = _runtime(start=False)
        agent = WorkflowParticipatingAgent()

        with self.assertRaises(RuntimeNotRunning):
            agent._resolve(type("E", (), {"runtime": runtime})())

    def test_no_work_runs_when_the_gate_refuses(self):
        """Fail closed, proved by non-execution rather than by the exception
        type alone."""
        runtime = _runtime(start=False)
        performer = CountingPerformer()
        agent = _agent(performer)

        with self.assertRaises(RuntimeNotRunning):
            agent.participate(create_execution_layer(runtime))

        self.assertEqual(0, performer.calls)
        self.assertEqual((), agent.completed_steps)

    def test_hosted_state_is_released_at_shutdown_not_retained(self):
        runtime = _runtime()
        runtime.workflows.lifecycle.define(Workflow(identity=IDENTITY))
        runtime.stop()

        self.assertIsNone(runtime._workflows)


class NegativeControlsOnTheRealPath(unittest.TestCase):
    """`§14`. Every one proves non-execution, not merely refusal."""

    def test_a_terminal_workflow_does_not_silently_resume(self):
        runtime = _runtime()
        execution = create_execution_layer(runtime)
        _agent(CountingPerformer()).participate(execution)

        performer = CountingPerformer()
        again = _agent(performer)

        with self.assertRaises(DuplicateWorkflowLifecycle):
            again.participate(execution)

        self.assertEqual(0, performer.calls)
        self.assertIs(
            WorkflowState.SUCCEEDED,
            runtime.workflows.monitor.state_of(IDENTITY).state,
        )

    def test_an_unknown_workflow_has_no_observable_state(self):
        runtime = _runtime()

        with self.assertRaises(UnknownWorkflowLifecycle):
            runtime.workflows.monitor.state_of(IDENTITY)

    def test_the_runtime_exposes_no_workflow_lifecycle_bypass(self):
        """Runtime is an access host: it carries no transition, no definition
        and no monitoring surface of its own (`§10.1`)."""
        runtime = _runtime()

        for forbidden in ("define_workflow", "mark_ready", "enter_running",
                          "succeed", "fail", "workflow_lifecycle",
                          "workflow_state", "transition", "execute", "run"):
            self.assertFalse(hasattr(runtime, forbidden), forbidden)

    def test_the_runtime_defines_no_workflow_class_of_its_own(self):
        """No ownership inversion: the Runtime boundary introduces no Workflow
        entity to compete with the real one (`§8.3`, `§9`)."""
        import native_core.core.runtime as runtime_pkg

        for name in dir(runtime_pkg):
            if name.startswith("_"):
                continue
            self.assertNotIn("Workflow", name, name)

    def test_the_agent_holds_no_lifecycle_or_monitor_surface(self):
        agent = WorkflowParticipatingAgent()

        for forbidden in ("define", "mark_ready", "enter_running", "succeed",
                          "fail", "monitor", "lifecycle"):
            self.assertFalse(hasattr(agent, forbidden), forbidden)

    def test_two_runtimes_do_not_share_workflow_state(self):
        """Hosting is per-Runtime; nothing leaks through module state."""
        first, second = _runtime(), _runtime(runtime_id="p9-002-runtime")
        _agent(CountingPerformer()).participate(create_execution_layer(first))

        self.assertEqual((IDENTITY,), first.workflows.monitor.monitored())
        self.assertEqual((), second.workflows.monitor.monitored())

    def test_no_retry_occurs_after_a_failure_on_the_real_path(self):
        """`§13.2`: failure triggers nothing. The failing step ran exactly
        once, and the steps after it never ran at all."""
        runtime = _runtime()
        performer = CountingPerformer(fail_on="s2")
        agent = _agent(performer, keys=("s1", "s2", "s3"))

        agent.participate(create_execution_layer(runtime))

        self.assertEqual(["s1", "s2"], performer.seen)
        self.assertEqual(2, performer.calls)
        self.assertEqual(("s1",), agent.completed_steps)


if __name__ == "__main__":
    unittest.main()
