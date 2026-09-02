"""
Phase 9 Workflow execution lifecycle and monitorable state (`FD-P9-001`;
`ACT-CC-P9-001 §11`, `§12` — `E9-02`, `E9-04`).

`ACT-CC-P9-001 §11.1` fixes the minimum monitorable lifecycle:

```text
DEFINED → READY → RUNNING → SUCCEEDED / FAILED
```

and `§11.2` fixes who owns it: *"Workflow owns the semantics of this lifecycle.
Runtime may host execution across the lifecycle but SHALL NOT redefine lifecycle
ownership."* So the state model lives **here**, inside the Workflow boundary, and
the Runtime hosting it holds no method that could redefine any part of it.

**Why this module carries no execution.** workflow_spec §8 [E] states that a
Workflow *"is not the Runtime"*, and the Workflow conformance suite enforces it
by name: no definition in this package may be called `execute`, `run`, `invoke`,
`perform`, `call`, `act`, `start`, `apply`, `dispatch` or `schedule`. That rule
is not worked around here. This module decides **whether a transition is
lawful** and records the result; it never performs the work. The work is driven
from outside `native_core/`, through the Runtime that hosts this subsystem —
which is precisely the split `ACT-CC-P9-001 §8.3` demands when it says *"Hosting
is not ownership"* and *"Execution context is not Workflow authority."*

**State is not Trace.** `§12.2` requires the two stay distinct concepts, and
`§12.3` forbids encoding Workflow lifecycle solely as Trace records or
reinterpreting Trace as the owner of mutable Workflow state. Nothing here is a
Trace record: this is *current mutable execution condition*, answering *"what is
the current execution lifecycle condition of this Workflow?"* — a question Trace
does not answer. No Trace type is imported, and no identifier here names one.
The Workflow boundary continues to author no Trace at all (INV-4).

**What is deliberately absent.** `§11.4` requires that a terminal Workflow *"SHALL
NOT silently resume"*, and `§11.5` states that Phase 9 *"does not authorize a
general resumability engine."* `SUCCEEDED` and `FAILED` therefore have **no**
lawful successor — not even back to `DEFINED` — and this module offers no
retry, recovery, compensation, rollback or reactivation surface. `§13.2` forbids
failure from automatically triggering any of them; the way to guarantee that is
to not build them, so they are not built.

Dependencies: stdlib and this package only. Nothing from Runtime, Agent, Skill,
Capability, Governance, Trace, Memory, Knowledge, Optimization or
Infrastructure, and no external dependency (INV-12; workflow_spec §8).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Dict, Mapping, Tuple

from .exceptions import (
    DuplicateWorkflowLifecycle,
    InvalidWorkflowTransition,
    UnknownWorkflowLifecycle,
)
from .models import Workflow, WorkflowIdentity


class WorkflowState(Enum):
    """The lifecycle states a Workflow execution occupies (`§11.1`).

    `DEFINED` is a Workflow known to the lifecycle but not yet eligible —
    `§11.3` requires that *"a defined Workflow is not implicitly executable
    unless eligible to become READY."* `READY` is the sole eligible state.
    `RUNNING` represents *"an actual accepted execution attempt"*, not an
    intention to execute. `SUCCEEDED` and `FAILED` are terminal.
    """

    DEFINED = "defined"
    READY = "ready"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class WorkflowLifecycleModel:
    """The lifecycle model as data: which states are eligible, which are
    terminal, and which transitions are lawful.

    **Why these are class attributes and not module constants.** The Workflow
    conformance suite bans *every* module-level binding in this package —
    `test_no_module_level_mutable_state`, whose purpose is that *"no registry
    can hide in module state."* These three values are immutable and are not a
    registry, so the rule's stated intent does not reach them; its text does,
    and it holds for the whole package today. Narrowing an absolute rule so that
    new code passes is the one move a conformance suite exists to prevent, so
    the rule was left exactly as it was and the model was placed where the rule
    already permits it. Sibling boundaries (`memory/lifecycle.py`,
    `infrastructure/tool_lifecycle.py`) use module constants because their own
    suites permit that; this package is stricter, and stays stricter.
    """

    #: Terminal states. `§11.3` makes both terminal and `§11.4` forbids silent
    #: resumption from either.
    TERMINAL_STATES: Tuple[WorkflowState, ...] = (
        WorkflowState.SUCCEEDED,
        WorkflowState.FAILED,
    )

    #: The only state from which execution may lawfully begin (`§11.3`).
    EXECUTION_ELIGIBLE_STATES: Tuple[WorkflowState, ...] = (WorkflowState.READY,)

    #: Lawful transitions. Both terminal states have an **empty** successor
    #: tuple, which is what makes `§11.4`'s no-silent-resume requirement
    #: structural rather than a convention someone could forget.
    LAWFUL_TRANSITIONS: Mapping[WorkflowState, Tuple[WorkflowState, ...]] = (
        MappingProxyType(
            {
                WorkflowState.DEFINED: (WorkflowState.READY,),
                WorkflowState.READY: (WorkflowState.RUNNING,),
                WorkflowState.RUNNING: (
                    WorkflowState.SUCCEEDED,
                    WorkflowState.FAILED,
                ),
                WorkflowState.SUCCEEDED: (),
                WorkflowState.FAILED: (),
            }
        )
    )


def _freeze(value: Any) -> Any:
    """Deeply immutable snapshot, local to this boundary."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    return value


@dataclass(frozen=True)
class WorkflowLifecycleState:
    """One Workflow's current execution condition (`E9-04`).

    Frozen. A state object whose `state` field could be reassigned by whoever
    holds a reference would make every eligibility and terminality guarantee
    unenforceable, so transitions produce new values rather than mutating this
    one.

    `detail` carries whatever the transition recorded — a failure reason, an
    outcome value. It is descriptive only and no decision is taken from it.
    """

    identity: WorkflowIdentity
    state: WorkflowState
    ordinal: int
    detail: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.identity, WorkflowIdentity):
            raise InvalidWorkflowTransition(
                "a lifecycle state requires a WorkflowIdentity"
            )
        if not isinstance(self.state, WorkflowState):
            raise InvalidWorkflowTransition("a lifecycle state requires a WorkflowState")
        object.__setattr__(self, "detail", _freeze(dict(self.detail)))

    @property
    def is_eligible(self) -> bool:
        """Whether execution may lawfully begin from here (`§11.3`)."""
        return self.state in WorkflowLifecycleModel.EXECUTION_ELIGIBLE_STATES

    @property
    def is_active(self) -> bool:
        """Whether an accepted execution attempt is in progress (`§12.4`)."""
        return self.state is WorkflowState.RUNNING

    @property
    def is_terminal(self) -> bool:
        return self.state in WorkflowLifecycleModel.TERMINAL_STATES

    @property
    def is_success(self) -> bool:
        """Terminal success, distinguishable from terminal failure (`§12.4`)."""
        return self.state is WorkflowState.SUCCEEDED

    @property
    def is_failure(self) -> bool:
        return self.state is WorkflowState.FAILED


class WorkflowLifecycle:
    """The Workflow boundary's own lifecycle authority (`§11.2`).

    Every lawful state change passes through here, and every unlawful one is
    refused here. A Runtime hosting this object may ask for a transition; it
    cannot make one, cannot redefine what is lawful, and cannot reach past this
    object to the state it holds.
    """

    def __init__(self) -> None:
        self._states: Dict[WorkflowIdentity, WorkflowLifecycleState] = {}
        self._sequence = 0

    # -- admission into the lifecycle --------------------------------------

    def define(self, workflow: "Workflow") -> WorkflowLifecycleState:
        """Bring a Workflow under lifecycle management, in `DEFINED`.

        Refuses anything that is not a valid `Workflow`, so an incomplete or
        malformed representation never acquires a lifecycle at all (`E9-01`).
        Refuses a duplicate rather than resetting the existing one — silently
        returning a fresh `DEFINED` for a Workflow already `RUNNING` would be a
        reactivation path, which `§11.4` forbids.
        """
        if not isinstance(workflow, Workflow):
            raise InvalidWorkflowTransition(
                "only a Workflow may be brought under lifecycle management"
            )
        identity = workflow.identity
        if identity in self._states:
            raise DuplicateWorkflowLifecycle(
                f"{identity.workflow_key}@{identity.workflow_version} "
                "already holds a lifecycle state"
            )
        return self._record(identity, WorkflowState.DEFINED, {})

    # -- lawful transitions -------------------------------------------------

    def mark_ready(self, identity: "WorkflowIdentity") -> WorkflowLifecycleState:
        """`DEFINED → READY`. Eligibility is granted deliberately, never
        implied by definition (`§11.3`)."""
        return self._transition(identity, WorkflowState.READY, {})

    def enter_running(self, identity: "WorkflowIdentity") -> WorkflowLifecycleState:
        """`READY → RUNNING` — an accepted execution attempt (`§11.3`).

        Lawful from `READY` alone. An attempt from `DEFINED`, from a terminal
        state, or from `RUNNING` again is refused and the state is left
        untouched, which is what makes `E9-05`'s *"invalid execution does not
        silently execute"* observable: the caller sees a refusal and the
        lifecycle shows no progress.
        """
        return self._transition(identity, WorkflowState.RUNNING, {})

    def succeed(
        self, identity: "WorkflowIdentity", outcome: "Any" = None
    ) -> WorkflowLifecycleState:
        """`RUNNING → SUCCEEDED`, terminal.

        Reachable only from `RUNNING`, so `SUCCEEDED` cannot be arrived at
        without an accepted execution attempt having happened first — `E9-05`
        requires success be reached *"only through a lawful path."*
        """
        return self._transition(
            identity, WorkflowState.SUCCEEDED, {"outcome": outcome}
        )

    def fail(
        self, identity: "WorkflowIdentity", reason: str
    ) -> WorkflowLifecycleState:
        """`RUNNING → FAILED`, terminal.

        Records the reason and stops. Nothing here retries, compensates, rolls
        back or recovers — `§13.2` forbids failure from triggering any of them,
        and this method has no branch that could.
        """
        if not isinstance(reason, str) or not reason.strip():
            raise InvalidWorkflowTransition("a failure must carry a reason")
        return self._transition(identity, WorkflowState.FAILED, {"reason": reason})

    # -- observation --------------------------------------------------------

    def state_of(self, identity: "WorkflowIdentity") -> WorkflowLifecycleState:
        """The current lifecycle state. Fails closed on an unknown Workflow
        rather than inventing a default — a synthesized `DEFINED` would make an
        unmanaged Workflow look executable."""
        try:
            return self._states[identity]
        except (KeyError, TypeError):
            raise UnknownWorkflowLifecycle(
                "no lifecycle state is held for this Workflow"
            ) from None

    def holds(self, identity: "WorkflowIdentity") -> bool:
        try:
            return identity in self._states
        except TypeError:
            return False

    def identities(self) -> Tuple["WorkflowIdentity", ...]:
        return tuple(self._states)

    # -- internal -----------------------------------------------------------

    def _transition(
        self, identity: "WorkflowIdentity", target: "WorkflowState", detail: dict
    ) -> WorkflowLifecycleState:
        current = self.state_of(identity)
        allowed = WorkflowLifecycleModel.LAWFUL_TRANSITIONS[current.state]
        if target not in allowed:
            raise InvalidWorkflowTransition(
                f"{identity.workflow_key}@{identity.workflow_version} cannot move "
                f"{current.state.value!r} → {target.value!r}; lawful targets are "
                f"{tuple(s.value for s in allowed)!r}"
            )
        return self._record(identity, target, detail)

    def _record(
        self, identity: "WorkflowIdentity", state: "WorkflowState", detail: dict
    ) -> WorkflowLifecycleState:
        self._sequence += 1
        recorded = WorkflowLifecycleState(
            identity=identity, state=state, ordinal=self._sequence, detail=detail
        )
        self._states[identity] = recorded
        return recorded


class WorkflowMonitor:
    """The read-only monitoring surface over Workflow lifecycle state
    (`§12.4`; `E9-04`).

    `§12.4` requires it be possible to determine, through the authorized public
    path: Workflow identity, current lifecycle state, whether execution is
    active or terminal, and whether a terminal result is success or failure.
    This answers exactly those four and nothing else.

    Separated from `WorkflowLifecycle` on purpose. Monitoring is observation, so
    the monitoring surface carries **no** transition method — which is how
    `E9-04`'s *"invalid state mutation does not silently succeed"* is held
    structurally: there is no mutation entry point here to misuse.

    `§12.4` also states monitoring need not introduce a database, external
    observability infrastructure, distributed tracing, dashboards, schedulers or
    persistence engines. None is introduced.
    """

    def __init__(self, lifecycle: "WorkflowLifecycle") -> None:
        if not isinstance(lifecycle, WorkflowLifecycle):
            raise InvalidWorkflowTransition(
                "a monitor observes a WorkflowLifecycle"
            )
        self._lifecycle = lifecycle

    def state_of(self, identity: "WorkflowIdentity") -> WorkflowLifecycleState:
        return self._lifecycle.state_of(identity)

    def is_active(self, identity: "WorkflowIdentity") -> bool:
        return self._lifecycle.state_of(identity).is_active

    def is_terminal(self, identity: "WorkflowIdentity") -> bool:
        return self._lifecycle.state_of(identity).is_terminal

    def is_success(self, identity: "WorkflowIdentity") -> bool:
        return self._lifecycle.state_of(identity).is_success

    def is_failure(self, identity: "WorkflowIdentity") -> bool:
        return self._lifecycle.state_of(identity).is_failure

    def monitored(self) -> Tuple["WorkflowIdentity", ...]:
        """Every Workflow currently under lifecycle management. Zero Workflows
        is a valid state (`ACT-CC-P9-001 §10.2`)."""
        return self._lifecycle.identities()
