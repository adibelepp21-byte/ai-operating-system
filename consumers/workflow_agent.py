"""
Phase 9 — the caller side of Runtime-hosted Workflow execution (`E9-03`).

`ACT-CC-P9-001 §10` fixes the authorized execution relationship as a path, not a
call:

```text
Agent / lawful caller → existing Workflow semantics → Runtime execution/access
host → authorized Workflow execution path → Workflow state outcome
```

This module is the caller that makes that path traversable end to end.

**Why the driver lives here and not in a core boundary.** It has nowhere else it
could lawfully live, and that is a structural result rather than a convenience:

  - `core/workflow/` may not hold it. The Workflow conformance suite forbids any
    definition in that package named `execute`, `run`, `invoke`, `perform`,
    `call`, `act`, `start`, `apply`, `dispatch` or `schedule` — workflow_spec §8
    [E], a Workflow *"is not the Runtime."*
  - `core/runtime/` may not hold it either. The Runtime conformance suite
    forbids any definition named `execute`, `run`, `perform`, `act`, `invoke`,
    `decide`, `plan`, `schedule`, `submit` or `spawn`, and forbids any class
    name containing `Workflow`. Runtime is a facility, not an actor.

So Workflow owns the lifecycle, Runtime hosts it, and the concrete driver sits
outside `native_core/` on the `E-01` precedent (`DEC-P6-042`), exactly as the
Phase 8 Tool consumer does. That is `§8.3` made structural — *"Hosting is not
ownership"* and *"Execution context is not Workflow authority"* — because the
one component that actually drives work is neither of the two boundaries whose
authority could be inverted by it.

**What this caller may not do.** It holds no lifecycle authority. It cannot
decide that a transition is lawful; it can only ask, and `WorkflowLifecycle`
answers. Every state change below goes through that object, and an unlawful
request raises rather than being coerced — which is how `§13.3`'s prohibition on
*"silently normalized into successful execution"* survives contact with a real
caller.

It also opens no agent-to-agent channel. Steps are executed one at a time
against a performer supplied by this module's own caller; no step receives a
reference to another step's actor, and nothing here carries one Agent Instance
to another. INV-13 is preserved because the only coordination that exists is the
Workflow's own ordered composition.

**Failure is terminal here.** A step that raises, or reports failure, drives the
Workflow to `FAILED` and stops. Nothing retries, compensates, rolls back or
recovers — `§13.2` forbids failure from triggering any of them, and there is no
branch in this module that could.

Dependencies: the `Agent` contract and the Workflow public surface. No Runtime
type is imported and the hosting Runtime is never named.
"""

from __future__ import annotations

from typing import Any, Callable, List, Optional, Tuple

from native_core.core.agent import Agent
from native_core.core.workflow import (
    Workflow,
    WorkflowComposition,
    WorkflowLifecycleState,
    WorkflowStep,
    WorkflowSubsystem,
)


class StepFailed(Exception):
    """A performer reported that a step could not be completed.

    Raised by a performer, caught by `participate`, and turned into a terminal
    `FAILED` — never into a retry. Carrying it as an exception rather than a
    return code keeps a failed step from being mistaken for a completed one that
    happened to return something falsy.
    """


class WorkflowParticipatingAgent(Agent):
    """A concrete `Agent` that drives one Workflow through its lifecycle on the
    Runtime-hosted path.

    Construction takes the Workflow subsystem by injection, or nothing, in which
    case it is resolved from the hosting Runtime at participation time.
    """

    def __init__(
        self,
        subsystem: "Optional[WorkflowSubsystem]" = None,
        workflow: "Optional[Workflow]" = None,
        composition: "Optional[WorkflowComposition]" = None,
        performer: "Optional[Callable[[WorkflowStep], Any]]" = None,
    ) -> None:
        if subsystem is not None and not isinstance(subsystem, WorkflowSubsystem):
            raise TypeError(
                "a Workflow-participating Agent requires a WorkflowSubsystem"
            )
        if workflow is not None and not isinstance(workflow, Workflow):
            raise TypeError("workflow must be a Workflow")
        self._subsystem = subsystem
        self._workflow = workflow
        self._composition = composition
        self._performer = performer
        self._completed: List[str] = []
        self._states: List[WorkflowLifecycleState] = []

    # -- observation -------------------------------------------------------

    @property
    def completed_steps(self) -> Tuple[str, ...]:
        """The step keys that actually ran, in order.

        The evidence that a refusal meant non-execution: a Workflow refused
        before `RUNNING` leaves this empty, and a Workflow that failed at step
        two shows exactly one entry. `§13.3` requires invalid execution not be
        normalized into successful execution, and an empty tuple beside a
        refusal is what makes that observable rather than asserted.
        """
        return tuple(self._completed)

    @property
    def observed_states(self) -> Tuple["WorkflowLifecycleState", ...]:
        """Every lifecycle state this caller was handed, in order. Ordinary
        in-memory evidence for its own callers; the authoritative state is the
        Workflow boundary's, not this."""
        return tuple(self._states)

    # -- internal ----------------------------------------------------------

    def _resolve(self, execution: "object") -> "WorkflowSubsystem":
        """Return the Workflow subsystem this participation will use.

        An injected subsystem wins when present. Otherwise it comes from the
        Runtime hosting this Execution — `execution.runtime.workflows` — which
        is RUNNING-gated by the Runtime itself. This consumer adds no access
        control and bypasses none: if the Runtime is not RUNNING, the Runtime
        refuses and the refusal propagates.
        """
        if self._subsystem is not None:
            return self._subsystem
        return execution.runtime.workflows

    def _observe(self, state: "WorkflowLifecycleState") -> "WorkflowLifecycleState":
        self._states.append(state)
        return state

    # -- the Agent contract ------------------------------------------------

    def participate(self, execution: "object") -> "Optional[WorkflowLifecycleState]":
        """Drive the configured Workflow through `DEFINED → READY → RUNNING →
        SUCCEEDED / FAILED` during one bound Execution.

        This is the `E9-03` path in one method. Each transition is *requested*
        from `WorkflowLifecycle`, which is the only thing that decides whether
        it is lawful; this method contains no state machine of its own and no
        branch that could reach a terminal state without passing through
        `RUNNING`.

        Returns the terminal state, or `None` when nothing was configured to
        run. A lawful failure is a completed participation with a terminal
        `FAILED` — the caller drove the Workflow correctly and the work did not
        succeed, which is not the same as the participation failing.
        """
        subsystem = self._resolve(execution)
        if self._workflow is None:
            return None

        lifecycle = subsystem.lifecycle
        identity = self._workflow.identity

        self._observe(lifecycle.define(self._workflow))
        self._observe(lifecycle.mark_ready(identity))
        self._observe(lifecycle.enter_running(identity))

        steps = self._composition.steps if self._composition is not None else ()
        for step in steps:
            try:
                self._perform_one(step)
            except StepFailed as failure:
                return self._observe(lifecycle.fail(identity, str(failure)))
            self._completed.append(step.step_key)

        return self._observe(
            lifecycle.succeed(identity, outcome={"steps": tuple(self._completed)})
        )

    def _perform_one(self, step: "WorkflowStep") -> None:
        """Run one step against the supplied performer.

        With no performer the step is a no-op that still counts as completed —
        Phase 9 measures the lifecycle and the path, not the work, and inventing
        work here would make the evidence about this module rather than about
        the architecture. A performer that raises anything other than
        `StepFailed` is left to propagate: swallowing an unexpected error would
        turn a broken step into a silent success.
        """
        if self._performer is not None:
            self._performer(step)
