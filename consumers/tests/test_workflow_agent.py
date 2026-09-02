"""
`WorkflowParticipatingAgent` — contract realization, isolation, and authority
limits.

Focused evidence about the consumer itself. The `E9-03` path evidence lives in
`test_workflow_agent_runtime.py`, because a unit test cannot establish it.
"""

from __future__ import annotations

import ast
import inspect
import unittest
from pathlib import Path

from consumers.workflow_agent import StepFailed, WorkflowParticipatingAgent
from native_core.core.agent import Agent
from native_core.core.workflow import (
    AgentInstanceRef,
    DuplicateWorkflowLifecycle,
    InvalidWorkflowTransition,
    SkillRef,
    Workflow,
    WorkflowComposition,
    WorkflowIdentity,
    WorkflowLifecycleError,
    WorkflowState,
    WorkflowStep,
    create_workflow_subsystem,
)

IDENTITY = WorkflowIdentity(workflow_key="unit-flow", workflow_version="1")


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


def _agent(performer=None, keys=("s1", "s2")):
    subsystem = create_workflow_subsystem()
    agent = WorkflowParticipatingAgent(
        subsystem=subsystem,
        workflow=Workflow(identity=IDENTITY),
        composition=_composition(*keys),
        performer=performer,
    )
    return agent, subsystem


class _Execution:
    """A stand-in Execution for the injected-collaborator tests only. The real
    path is exercised against a real Runtime in the companion module."""

    def __init__(self, runtime=None):
        self.runtime = runtime


def _imported_modules():
    source = Path(inspect.getfile(WorkflowParticipatingAgent)).read_text()
    modules = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
        elif isinstance(node, ast.Import):
            modules.update(a.name for a in node.names)
    return modules


class ItRealizesTheAgentContract(unittest.TestCase):

    def test_it_is_an_agent(self):
        self.assertTrue(issubclass(WorkflowParticipatingAgent, Agent))

    def test_an_instance_is_an_agent(self):
        self.assertIsInstance(WorkflowParticipatingAgent(), Agent)

    def test_it_lives_outside_the_native_core(self):
        path = Path(inspect.getfile(WorkflowParticipatingAgent)).as_posix()

        self.assertNotIn("/native_core/", path)
        self.assertIn("/consumers/", path)


class ItDrivesTheLifecycleWithoutOwningIt(unittest.TestCase):

    def test_a_complete_participation_reaches_succeeded(self):
        agent, subsystem = _agent()

        final = agent.participate(_Execution())

        self.assertIs(WorkflowState.SUCCEEDED, final.state)
        self.assertIs(
            WorkflowState.SUCCEEDED, subsystem.monitor.state_of(IDENTITY).state
        )

    def test_it_passes_through_every_lawful_state_in_order(self):
        agent, _ = _agent()

        agent.participate(_Execution())

        self.assertEqual(
            [
                WorkflowState.DEFINED,
                WorkflowState.READY,
                WorkflowState.RUNNING,
                WorkflowState.SUCCEEDED,
            ],
            [s.state for s in agent.observed_states],
        )

    def test_every_configured_step_runs_in_order(self):
        seen = []
        agent, _ = _agent(performer=lambda step: seen.append(step.step_key))

        agent.participate(_Execution())

        self.assertEqual(["s1", "s2"], seen)
        self.assertEqual(("s1", "s2"), agent.completed_steps)

    def test_a_failing_step_drives_the_workflow_to_failed(self):
        def performer(step):
            if step.step_key == "s2":
                raise StepFailed("s2 declined")

        agent, subsystem = _agent(performer=performer)

        final = agent.participate(_Execution())

        self.assertIs(WorkflowState.FAILED, final.state)
        self.assertEqual("s2 declined", final.detail["reason"])
        self.assertTrue(subsystem.monitor.is_failure(IDENTITY))

    def test_a_failing_step_stops_the_remaining_steps(self):
        """Fail closed: the failure is terminal, not a checkpoint to resume
        past."""
        seen = []

        def performer(step):
            seen.append(step.step_key)
            raise StepFailed("declined")

        agent, _ = _agent(performer=performer, keys=("s1", "s2", "s3"))

        agent.participate(_Execution())

        self.assertEqual(["s1"], seen)
        self.assertEqual((), agent.completed_steps)

    def test_nothing_configured_runs_nothing(self):
        agent = WorkflowParticipatingAgent(subsystem=create_workflow_subsystem())

        self.assertIsNone(agent.participate(_Execution()))
        self.assertEqual((), agent.completed_steps)

    def test_a_workflow_with_no_steps_still_completes_lawfully(self):
        agent, _ = _agent(keys=())

        final = agent.participate(_Execution())

        self.assertIs(WorkflowState.SUCCEEDED, final.state)
        self.assertEqual((), agent.completed_steps)

    def test_observations_are_immutable_to_callers(self):
        agent, _ = _agent()
        agent.participate(_Execution())

        self.assertIsInstance(agent.completed_steps, tuple)
        self.assertIsInstance(agent.observed_states, tuple)

    def test_an_unexpected_error_is_not_swallowed_into_success(self):
        """Only `StepFailed` becomes a lawful `FAILED`. A genuine defect
        propagates rather than being relabelled."""

        def performer(step):
            raise ValueError("a real defect")

        agent, subsystem = _agent(performer=performer)

        with self.assertRaises(ValueError):
            agent.participate(_Execution())

        self.assertIs(WorkflowState.RUNNING, subsystem.monitor.state_of(IDENTITY).state)


class ItHoldsNoLifecycleAuthority(unittest.TestCase):
    """`ACT-CC-P9-001 §8.3` and `§10.1`, asserted structurally."""

    def test_it_depends_only_on_the_agent_contract_and_workflow(self):
        core = {m for m in _imported_modules() if m.startswith("native_core")}

        self.assertEqual(
            {"native_core.core.agent", "native_core.core.workflow"}, core
        )

    def test_it_imports_no_runtime_type(self):
        for module in _imported_modules():
            self.assertNotIn("runtime", module)

    def test_it_imports_nothing_from_governance_trace_or_knowledge(self):
        for module in _imported_modules():
            for word in ("governance", "trace", "knowledge"):
                self.assertNotIn(word, module)

    def test_it_defines_no_transition_of_its_own(self):
        """It asks; it does not decide. The lifecycle names it may call all
        belong to `WorkflowLifecycle`, and none is redefined here."""
        tree = ast.parse(Path(inspect.getfile(WorkflowParticipatingAgent)).read_text())
        methods = {
            n.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
            and node.name == "WorkflowParticipatingAgent"
            for n in node.body
            if isinstance(n, ast.FunctionDef)
        }

        for forbidden in ("define", "mark_ready", "enter_running", "succeed",
                          "fail", "transition", "_transition"):
            self.assertNotIn(forbidden, methods)

    def test_it_carries_no_state_machine_of_its_own(self):
        """No lifecycle constant is redeclared here — the transition table lives
        in the Workflow boundary and nowhere else."""
        source = Path(inspect.getfile(WorkflowParticipatingAgent)).read_text()

        for forbidden in ("LAWFUL_TRANSITIONS", "TERMINAL_STATES",
                          "EXECUTION_ELIGIBLE_STATES"):
            self.assertNotIn(forbidden, source, forbidden)

    def test_it_exposes_no_recovery_surface(self):
        agent = WorkflowParticipatingAgent()

        for forbidden in ("retry", "recover", "rollback", "compensate", "resume",
                          "reactivate"):
            self.assertFalse(hasattr(agent, forbidden), forbidden)

    def test_a_wrong_collaborator_type_is_refused(self):
        with self.assertRaises(TypeError):
            WorkflowParticipatingAgent(subsystem="not a subsystem")

    def test_a_wrong_workflow_type_is_refused(self):
        with self.assertRaises(TypeError):
            WorkflowParticipatingAgent(workflow="not a workflow")

    def test_it_cannot_reactivate_a_terminal_workflow(self):
        """The Workflow boundary refuses the consumer exactly as it refuses
        anyone else, and refuses it *earlier* than a transition check would:
        re-participating on a terminal Workflow is stopped at `define`, so no
        transition is ever attempted. `§11.4` — a terminal Workflow shall not
        silently resume."""
        agent, subsystem = _agent()
        agent.participate(_Execution())

        again = WorkflowParticipatingAgent(
            subsystem=subsystem,
            workflow=Workflow(identity=IDENTITY),
            composition=_composition("s1"),
        )

        with self.assertRaises(DuplicateWorkflowLifecycle):
            again.participate(_Execution())

        self.assertIs(
            WorkflowState.SUCCEEDED, subsystem.monitor.state_of(IDENTITY).state
        )
        self.assertEqual((), again.completed_steps)

    def test_that_refusal_is_a_lifecycle_error_either_way(self):
        """Both refusal types share one base, so a caller cannot be refused by
        something outside the Workflow boundary's own error family."""
        for error in (DuplicateWorkflowLifecycle, InvalidWorkflowTransition):
            self.assertTrue(issubclass(error, WorkflowLifecycleError), error)


if __name__ == "__main__":
    unittest.main()
