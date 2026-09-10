"""`P11-W4` — the autonomous execution loop, bounded by an issued Delegation.

`DP-01 §3 W4` authorizes *"the P11 autonomous operating loop within already
established authority"*:

    PLAN → DELEGATE → EXECUTE → OBSERVE → VERIFY → ADAPT → CONTINUE / ESCALATE

and bounds it: *"The authorization does not permit the autonomous organization to
enlarge its own authority."* `FD-P11-001 §18` fixes the full chain and adds:
**"No stage may be silently skipped."**

**Every execution requires a delegation, checked at the point of execution.**
Not at construction, not once at start-up — at each step. A loop that validated
authority once and then ran would be relying on a decision made before the work
it authorizes, which is how `PLAN READINESS ≠ AUTHORIZATION` fails in practice.

**What this module refuses to do.**

`§19`: the instance *"does not become the owner of Planning authority merely
because it executes a Plan."* So the loop **reads** a Plan and never writes one:
it holds no `PlanningSurface` method that adopts, adapts or revises. Adaptation
is *proposed back*, and whoever holds planning authority decides.

`§22`: *"Autonomous execution must fail closed when a requested action crosses
Founder Reserved Authority. The autonomous organization may execute more work. It
may not autonomously expand the authority under which it operates."* A step
outside the delegation's capability scope raises rather than proceeding, and the
escalation records what was required against what was held.

`§27`: on encountering a condition needing authority not granted —
`STOP → PRESERVE EVIDENCE → RECORD BLOCKER → ESCALATE → CONTINUE INDEPENDENT
AUTHORIZED WORK`. *"W4 must not solve an authority gap by implementation."*
`execute_plan` therefore continues with the steps that remain in scope after
recording a refusal, rather than aborting the run or silently widening it.

**Outputs are evidence, not authority.** A completed step produces an
`ExecutionOutcome` carrying what happened. `§21`: observation may inform
planning and may not *"authorize delegation"*, *"approve an Agent Instance"* or
*"create authority"*. Nothing here promotes a success into a permission —
`§39`: `W4 EXECUTION ≠ GOVERNANCE AUTHORITY`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, List, Optional, Tuple

from tools.agent_instance_registry import AgentInstanceRegistry, REGISTERED
from tools.planning import Plan, PlanStep, sequence
from tools.w4_delegation import W4Delegation

#: Outcomes an execution step may report. Deliberately the **ratified Trace
#: vocabulary** (`native_core/core/trace/record.py`, Domain Model `§2.1`):
#: ``success`` · ``failure`` · ``escalation``. Reusing it means a W4 outcome can
#: never claim a status the canonical model does not recognise — and there is no
#: ``authorized`` among them.
SUCCESS, FAILURE, ESCALATION = "success", "failure", "escalation"


class ExecutionRefused(RuntimeError):
    """The step lies outside the delegation. Fail closed (`§22`)."""

    def __init__(self, message: str, *, required: str, held: Tuple[str, ...]):
        super().__init__(message)
        self.required = required
        self.held = held


@dataclass(frozen=True)
class ExecutionOutcome:
    """What happened when one step ran. Evidence only."""

    step_key: str
    status: str
    detail: str
    delegation_id: str
    instance_key: str
    at: str

    def __post_init__(self):
        if self.status not in (SUCCESS, FAILURE, ESCALATION):
            raise ValueError(
                f"{self.status!r} is not a ratified outcome — Domain Model §2.1 "
                "fixes success / failure / escalation")


@dataclass
class ExecutionReport:
    """The run's evidence. `§27` requires the blocker preserved, not discarded."""

    outcomes: List[ExecutionOutcome] = field(default_factory=list)
    refusals: List[ExecutionRefused] = field(default_factory=list)

    def statuses(self) -> Tuple[str, ...]:
        return tuple(o.status for o in self.outcomes)

    def escalated(self) -> bool:
        return any(o.status == ESCALATION for o in self.outcomes)


class W4Executor:
    """Executes plan steps under one delegation, and nothing else.

    Holds the delegation and the registry so it can re-check both **per step**.
    It does not hold a `PlanningSurface`: `§19` keeps Planning authority with
    Planning, and an executor that could revise the plan it is executing would
    be authorizing its own next instruction.
    """

    def __init__(self, delegation: W4Delegation, registry: AgentInstanceRegistry):
        # `§18`: no stage may be silently skipped — and an executor holding
        # something that is not a Delegation has skipped the delegation stage
        # entirely. Refused here rather than at first use, because failing on
        # the *first step* would mean the object existed in an unauthorized
        # state for however long the caller held it.
        if not isinstance(delegation, W4Delegation):
            raise TypeError(
                "W4 execution requires an issued W4Delegation — "
                "`FD-P11-001 §18` forbids skipping the delegation stage")
        if not isinstance(registry, AgentInstanceRegistry):
            raise TypeError(
                "W4 execution requires the instance registry to re-check the "
                "recipient's lifecycle at every step")
        self._delegation = delegation
        self._registry = registry

    def _authorize_step(self, step: PlanStep) -> None:
        """`§18`: no stage silently skipped. Re-checked for every step."""
        registration = self._registry.get(self._delegation.recipient_instance)
        if registration.lifecycle != REGISTERED:
            raise ExecutionRefused(
                f"instance {registration.instance_key!r} is "
                f"{registration.lifecycle}; a retired instance executes nothing",
                required=step.key, held=self._delegation.capability_scope)
        if step.key not in self._delegation.work_scope:
            raise ExecutionRefused(
                f"step {step.key!r} is outside the delegated work scope — "
                "`§22`: the organization may execute more work, it may not "
                "expand the authority under which it operates",
                required=step.key, held=self._delegation.work_scope)

    def execute_step(self, step: PlanStep,
                     perform: Callable[[PlanStep], str]) -> ExecutionOutcome:
        """Run one step, having proved it is inside the delegation.

        ``perform`` is supplied by the caller and does the actual work. This
        module does not decide *what* the work is — that came from the Plan —
        and does not decide *whether it may* happen beyond the delegation check
        above.
        """
        self._authorize_step(step)
        try:
            detail = perform(step)
            status = SUCCESS
        except Exception as exc:                      # failure is an outcome
            detail, status = f"{type(exc).__name__}: {exc}", FAILURE
        return ExecutionOutcome(
            step_key=step.key, status=status, detail=detail,
            delegation_id=self._delegation.delegation_id,
            instance_key=self._delegation.recipient_instance,
            at=datetime.now(timezone.utc).isoformat())

    def execute_plan(self, plan: Plan,
                     perform: Callable[[PlanStep], str]) -> ExecutionReport:
        """Run a plan's steps in dependency order, within the delegation.

        A step outside scope is **recorded as an escalation and skipped**, and
        the run continues with the remainder. `§27`: preserve evidence, record
        the blocker, escalate, and *"continue independent authorized work"* —
        aborting the whole run would discard authorized work because unrelated
        work was refused.
        """
        report = ExecutionReport()
        for step in sequence(plan):
            try:
                report.outcomes.append(self.execute_step(step, perform))
            except ExecutionRefused as refusal:
                report.refusals.append(refusal)
                report.outcomes.append(ExecutionOutcome(
                    step_key=step.key, status=ESCALATION, detail=str(refusal),
                    delegation_id=self._delegation.delegation_id,
                    instance_key=self._delegation.recipient_instance,
                    at=datetime.now(timezone.utc).isoformat()))
        return report
