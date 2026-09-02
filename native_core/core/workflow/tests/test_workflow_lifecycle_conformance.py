"""
Phase 9 Workflow lifecycle conformance — `E9-01`, `E9-02`, `E9-04`, `E9-05`.

`ACT-CC-P9-001 §14` states each criterion together with the negative controls
that must accompany it, and `§19 Step 9` requires those controls prove
**non-execution**, not merely that something was labelled a failure. So every
refusal below is proved twice: the call raises, **and** the recorded lifecycle
state is shown to be exactly what it was before the attempt.

`E9-03` is the real-path criterion and cannot be established here — a unit test
cannot demonstrate Runtime-mediated execution. It lives in
`consumers/tests/test_workflow_agent_runtime.py`.
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

from native_core.core.workflow import (
    DuplicateWorkflowLifecycle,
    InvalidWorkflowTransition,
    UnknownWorkflowLifecycle,
    Workflow,
    WorkflowIdentity,
    WorkflowLifecycle,
    WorkflowLifecycleModel,
    WorkflowMonitor,
    WorkflowState,
    WorkflowSubsystem,
    create_workflow_subsystem,
)
from native_core.core.workflow import lifecycle as lifecycle_module

IDENTITY = WorkflowIdentity(workflow_key="p9-flow", workflow_version="1")
OTHER = WorkflowIdentity(workflow_key="p9-other", workflow_version="1")


def _workflow(identity=IDENTITY):
    return Workflow(identity=identity)


def _at(state):
    """A lifecycle holding one Workflow driven to `state` by lawful steps only."""
    lifecycle = WorkflowLifecycle()
    lifecycle.define(_workflow())
    if state is WorkflowState.DEFINED:
        return lifecycle
    lifecycle.mark_ready(IDENTITY)
    if state is WorkflowState.READY:
        return lifecycle
    lifecycle.enter_running(IDENTITY)
    if state is WorkflowState.RUNNING:
        return lifecycle
    if state is WorkflowState.SUCCEEDED:
        lifecycle.succeed(IDENTITY)
    else:
        lifecycle.fail(IDENTITY, "declined")
    return lifecycle


class E901WorkflowRepresentationAndOwnership(unittest.TestCase):
    """`E9-01` — stable identity, valid representation, ownership preserved."""

    def test_a_lifecycle_state_carries_the_workflows_own_identity(self):
        state = _at(WorkflowState.DEFINED).state_of(IDENTITY)

        self.assertIs(IDENTITY, state.identity)
        self.assertEqual("p9-flow", state.identity.workflow_key)

    def test_identity_is_stable_across_the_whole_lifecycle(self):
        lifecycle = _at(WorkflowState.SUCCEEDED)

        self.assertEqual(IDENTITY, lifecycle.state_of(IDENTITY).identity)

    def test_lifecycle_semantics_live_in_the_workflow_boundary(self):
        """Ownership, asserted by location rather than by prose."""
        path = Path(lifecycle_module.__file__).as_posix()

        self.assertIn("/core/workflow/", path)
        self.assertNotIn("/core/runtime/", path)

    # -- negative controls ---------------------------------------------------

    def test_an_invalid_representation_is_refused(self):
        lifecycle = WorkflowLifecycle()

        for bad in (None, "p9-flow", IDENTITY, object()):
            with self.assertRaises(InvalidWorkflowTransition):
                lifecycle.define(bad)

    def test_an_incomplete_workflow_never_acquires_a_lifecycle(self):
        lifecycle = WorkflowLifecycle()
        with self.assertRaises(InvalidWorkflowTransition):
            lifecycle.define("not a workflow")

        self.assertEqual((), lifecycle.identities())

    def test_the_workflow_package_still_holds_no_execution_surface(self):
        """Runtime cannot replace Workflow semantic ownership, and Workflow has
        not taken Runtime's role in exchange. Both halves of `§8.3`."""
        verbs = {"execute", "run", "invoke", "perform", "call", "act", "start",
                 "apply", "dispatch", "schedule"}
        package = Path(lifecycle_module.__file__).parent
        offences = [
            (path.name, node.name)
            for path in package.rglob("*.py")
            if "tests" not in path.parts
            for node in ast.walk(ast.parse(path.read_text()))
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))
            and node.name.lstrip("_").lower() in verbs
        ]

        self.assertEqual([], offences)

    def test_the_boundary_names_no_runtime_and_no_peer_channel(self):
        """INV-13: unauthorized multi-agent collaboration cannot bypass Workflow,
        because no route between Agent Instances exists to bypass it with.

        Matched on **whole identifiers**, not substrings. A substring pass
        reports `TypeError` as containing `peer`, and a guard that cries wolf on
        a builtin is a guard nobody keeps. The resident Runtime INV-13 guard
        matches whole identifiers for the same reason.
        """
        package = Path(lifecycle_module.__file__).parent
        forbidden = frozenset(
            {"peer", "peers", "peer_instance", "target_agent", "to_agent",
             "from_agent", "channel", "send", "receive", "notify", "broadcast",
             "dispatch", "publish", "subscribe", "mailbox", "inbox", "outbox",
             "runtime"}
        )
        checked = 0
        for path in package.rglob("*.py"):
            if "tests" in path.parts:
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                names = []
                if isinstance(node, ast.Name):
                    names = [node.id]
                elif isinstance(node, ast.Attribute):
                    names = [node.attr]
                elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    names = [node.name]
                for name in names:
                    checked += 1
                    self.assertNotIn(
                        name.lower().lstrip("_"), forbidden, f"{path.name}:{name}"
                    )
        self.assertGreater(checked, 200, "the scan must actually reach identifiers")


class E902ExecutionEligibilityAndLifecycle(unittest.TestCase):
    """`E9-02` — the minimum lifecycle, and only the minimum."""

    def test_the_full_lawful_sequence_reaches_succeeded(self):
        lifecycle = WorkflowLifecycle()

        self.assertIs(WorkflowState.DEFINED, lifecycle.define(_workflow()).state)
        self.assertIs(WorkflowState.READY, lifecycle.mark_ready(IDENTITY).state)
        self.assertIs(WorkflowState.RUNNING, lifecycle.enter_running(IDENTITY).state)
        self.assertIs(WorkflowState.SUCCEEDED, lifecycle.succeed(IDENTITY).state)

    def test_the_full_lawful_sequence_reaches_failed(self):
        lifecycle = _at(WorkflowState.RUNNING)

        self.assertIs(WorkflowState.FAILED, lifecycle.fail(IDENTITY, "declined").state)

    def test_ready_is_the_only_eligible_state(self):
        self.assertEqual(
            (WorkflowState.READY,), WorkflowLifecycleModel.EXECUTION_ELIGIBLE_STATES
        )
        for state in WorkflowState:
            lifecycle = _at(state)
            self.assertEqual(
                state is WorkflowState.READY,
                lifecycle.state_of(IDENTITY).is_eligible,
                state,
            )

    def test_the_transition_table_covers_every_state_exactly_once(self):
        self.assertEqual(
            set(WorkflowState), set(WorkflowLifecycleModel.LAWFUL_TRANSITIONS)
        )

    def test_ordinals_advance_monotonically(self):
        lifecycle = WorkflowLifecycle()
        lifecycle.define(_workflow())
        first = lifecycle.state_of(IDENTITY).ordinal
        lifecycle.mark_ready(IDENTITY)

        self.assertGreater(lifecycle.state_of(IDENTITY).ordinal, first)

    # -- negative controls ---------------------------------------------------

    def test_execution_cannot_begin_from_defined(self):
        """`§11.3`: a defined Workflow is not implicitly executable."""
        lifecycle = _at(WorkflowState.DEFINED)

        with self.assertRaises(InvalidWorkflowTransition):
            lifecycle.enter_running(IDENTITY)

        self.assertIs(WorkflowState.DEFINED, lifecycle.state_of(IDENTITY).state)

    def test_execution_cannot_begin_from_a_terminal_state(self):
        for terminal in WorkflowLifecycleModel.TERMINAL_STATES:
            lifecycle = _at(terminal)

            with self.assertRaises(InvalidWorkflowTransition):
                lifecycle.enter_running(IDENTITY)

            self.assertIs(terminal, lifecycle.state_of(IDENTITY).state)

    def test_a_running_workflow_cannot_re_enter_running(self):
        lifecycle = _at(WorkflowState.RUNNING)
        before = lifecycle.state_of(IDENTITY)

        with self.assertRaises(InvalidWorkflowTransition):
            lifecycle.enter_running(IDENTITY)

        self.assertEqual(before, lifecycle.state_of(IDENTITY))

    def test_success_is_unreachable_without_an_accepted_execution_attempt(self):
        """`E9-05`: `SUCCEEDED` only through a lawful path."""
        for state in (WorkflowState.DEFINED, WorkflowState.READY):
            lifecycle = _at(state)

            with self.assertRaises(InvalidWorkflowTransition):
                lifecycle.succeed(IDENTITY)

            self.assertIs(state, lifecycle.state_of(IDENTITY).state)

    def test_terminal_states_are_not_silently_reactivated(self):
        """`§11.4`: a terminal Workflow shall not silently resume — asserted
        against *every* state, not just the interesting ones."""
        for terminal in WorkflowLifecycleModel.TERMINAL_STATES:
            self.assertEqual((), WorkflowLifecycleModel.LAWFUL_TRANSITIONS[terminal])
            for target in WorkflowState:
                lifecycle = _at(terminal)
                with self.assertRaises(InvalidWorkflowTransition):
                    lifecycle._transition(IDENTITY, target, {})
                self.assertIs(terminal, lifecycle.state_of(IDENTITY).state)

    def test_redefining_a_running_workflow_is_refused_not_reset(self):
        lifecycle = _at(WorkflowState.RUNNING)

        with self.assertRaises(DuplicateWorkflowLifecycle):
            lifecycle.define(_workflow())

        self.assertIs(WorkflowState.RUNNING, lifecycle.state_of(IDENTITY).state)

    def test_failure_does_not_become_retry_or_recovery(self):
        """`§13.2`. Proved by absence: no such surface exists to call."""
        for forbidden in ("retry", "recover", "rollback", "compensate", "resume",
                          "reactivate", "restart"):
            self.assertFalse(hasattr(WorkflowLifecycle, forbidden), forbidden)
            self.assertFalse(hasattr(WorkflowMonitor, forbidden), forbidden)

    def test_a_failure_must_carry_a_reason(self):
        lifecycle = _at(WorkflowState.RUNNING)

        for bad in (None, "", "   ", 7):
            with self.assertRaises(InvalidWorkflowTransition):
                lifecycle.fail(IDENTITY, bad)

        self.assertIs(WorkflowState.RUNNING, lifecycle.state_of(IDENTITY).state)


class E904MonitorableStateDistinctFromTrace(unittest.TestCase):
    """`E9-04` — observable state, and the four `§12.4` questions."""

    def test_the_four_monitoring_questions_are_answerable(self):
        subsystem = create_workflow_subsystem()
        subsystem.lifecycle.define(_workflow())
        subsystem.lifecycle.mark_ready(IDENTITY)
        subsystem.lifecycle.enter_running(IDENTITY)
        monitor = subsystem.monitor

        self.assertEqual((IDENTITY,), monitor.monitored())          # identity
        self.assertIs(WorkflowState.RUNNING, monitor.state_of(IDENTITY).state)
        self.assertTrue(monitor.is_active(IDENTITY))                # active
        self.assertFalse(monitor.is_terminal(IDENTITY))             # not terminal

    def test_terminal_success_and_terminal_failure_are_distinguishable(self):
        good = WorkflowMonitor(_at(WorkflowState.SUCCEEDED))
        bad = WorkflowMonitor(_at(WorkflowState.FAILED))

        self.assertTrue(good.is_terminal(IDENTITY))
        self.assertTrue(good.is_success(IDENTITY))
        self.assertFalse(good.is_failure(IDENTITY))

        self.assertTrue(bad.is_terminal(IDENTITY))
        self.assertTrue(bad.is_failure(IDENTITY))
        self.assertFalse(bad.is_success(IDENTITY))

    def test_zero_workflows_is_a_valid_state(self):
        """`§10.2`."""
        self.assertEqual((), create_workflow_subsystem().monitor.monitored())

    def test_workflow_state_is_not_a_trace_record(self):
        """`§12.2`/`§12.3` — no Trace identifier exists anywhere in the
        boundary, so lifecycle cannot be encoded as Trace even accidentally."""
        package = Path(lifecycle_module.__file__).parent
        for path in package.rglob("*.py"):
            if "tests" in path.parts:
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.Name):
                    self.assertNotIn("trace", node.id.lower(), path.name)
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    self.assertNotIn("trace", node.name.lower(), path.name)

    def test_the_state_answers_a_question_trace_does_not(self):
        """The two are distinct in substance, not only in naming: this is
        current mutable condition, and it changes in place."""
        lifecycle = _at(WorkflowState.READY)
        before = lifecycle.state_of(IDENTITY)
        lifecycle.enter_running(IDENTITY)

        self.assertIsNot(before, lifecycle.state_of(IDENTITY))
        self.assertIs(WorkflowState.RUNNING, lifecycle.state_of(IDENTITY).state)

    # -- negative controls ---------------------------------------------------

    def test_the_monitor_carries_no_mutation_surface(self):
        """Invalid state mutation cannot silently succeed through the monitoring
        path, because that path has no mutation entry point."""
        for forbidden in ("define", "mark_ready", "enter_running", "succeed",
                          "fail", "_transition", "_record"):
            self.assertFalse(hasattr(WorkflowMonitor, forbidden), forbidden)

    def test_a_recorded_state_cannot_be_reassigned(self):
        state = _at(WorkflowState.RUNNING).state_of(IDENTITY)

        with self.assertRaises(Exception):
            state.state = WorkflowState.SUCCEEDED

        self.assertIs(WorkflowState.RUNNING, state.state)

    def test_an_unknown_workflow_fails_closed_rather_than_defaulting(self):
        monitor = create_workflow_subsystem().monitor

        with self.assertRaises(UnknownWorkflowLifecycle):
            monitor.state_of(OTHER)

    def test_monitoring_introduces_no_unauthorized_machinery(self):
        """`§12.4`: no database, no persistence engine, no scheduler."""
        source = Path(lifecycle_module.__file__).read_text()
        tree = ast.parse(source)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
            elif isinstance(node, ast.Import):
                imported.update(a.name.split(".")[0] for a in node.names)

        self.assertEqual(set(), imported & {"sqlite3", "threading", "asyncio",
                                            "socket", "logging", "os", "time"})

    def test_the_subsystem_bundle_cannot_be_swapped(self):
        subsystem = create_workflow_subsystem()

        with self.assertRaises(Exception):
            subsystem.lifecycle = WorkflowLifecycle()


class E905FailClosedExecution(unittest.TestCase):
    """`E9-05` — and the reservations that bound it."""

    def test_a_failure_records_its_reason_and_stops_there(self):
        lifecycle = _at(WorkflowState.RUNNING)

        state = lifecycle.fail(IDENTITY, "substrate declined")

        self.assertIs(WorkflowState.FAILED, state.state)
        self.assertEqual("substrate declined", state.detail["reason"])
        self.assertEqual((), WorkflowLifecycleModel.LAWFUL_TRANSITIONS[state.state])

    def test_a_success_records_its_outcome(self):
        lifecycle = _at(WorkflowState.RUNNING)

        state = lifecycle.succeed(IDENTITY, outcome={"steps": ("s1",)})

        self.assertEqual(("s1",), state.detail["outcome"]["steps"])

    def test_recorded_detail_is_immutable_to_callers(self):
        state = _at(WorkflowState.FAILED).state_of(IDENTITY)

        with self.assertRaises(TypeError):
            state.detail["reason"] = "rewritten"

    def test_no_resumability_engine_was_introduced(self):
        """`§11.5`: state existing is not licence to build durable resume."""
        for forbidden in ("checkpoint", "snapshot_to", "persist", "restore",
                          "load", "save", "resume"):
            self.assertFalse(hasattr(WorkflowLifecycle, forbidden), forbidden)

    def test_an_unknown_workflow_cannot_be_transitioned(self):
        lifecycle = WorkflowLifecycle()

        for attempt in ("mark_ready", "enter_running", "succeed"):
            with self.assertRaises(UnknownWorkflowLifecycle):
                getattr(lifecycle, attempt)(OTHER)

        self.assertEqual((), lifecycle.identities())

    def test_one_workflows_failure_leaves_another_untouched(self):
        lifecycle = WorkflowLifecycle()
        for identity in (IDENTITY, OTHER):
            lifecycle.define(_workflow(identity))
            lifecycle.mark_ready(identity)
            lifecycle.enter_running(identity)

        lifecycle.fail(IDENTITY, "declined")

        self.assertIs(WorkflowState.FAILED, lifecycle.state_of(IDENTITY).state)
        self.assertIs(WorkflowState.RUNNING, lifecycle.state_of(OTHER).state)

    def test_the_monitor_requires_a_real_lifecycle(self):
        for bad in (None, "lifecycle", create_workflow_subsystem()):
            with self.assertRaises(InvalidWorkflowTransition):
                WorkflowMonitor(bad)


class TheCompositionRootIsAssembledNotConstructed(unittest.TestCase):

    def test_the_bundle_carries_a_lifecycle_and_its_own_monitor(self):
        subsystem = create_workflow_subsystem()

        self.assertIsInstance(subsystem, WorkflowSubsystem)
        self.assertIsInstance(subsystem.lifecycle, WorkflowLifecycle)
        self.assertIsInstance(subsystem.monitor, WorkflowMonitor)

    def test_the_monitor_observes_that_same_lifecycle(self):
        subsystem = create_workflow_subsystem()
        subsystem.lifecycle.define(_workflow())

        self.assertIs(
            WorkflowState.DEFINED, subsystem.monitor.state_of(IDENTITY).state
        )

    def test_each_assembly_is_independent(self):
        first, second = create_workflow_subsystem(), create_workflow_subsystem()
        first.lifecycle.define(_workflow())

        self.assertEqual((), second.monitor.monitored())


if __name__ == "__main__":
    unittest.main()
