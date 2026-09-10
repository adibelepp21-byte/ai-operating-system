"""The mutable Plan lifecycle: `PLAN → SEQUENCE → ADAPT → REVISE`.

`DP-03 §8.4` requires that *"the architecture MUST support the mutable Plan
lifecycle"* and that a Plan is *"not constrained to the semantics of a static
declaration loaded once."* This module is where that requirement is met.

Versions are immutable; the **chain** evolves. `adapt()` and `revise()` construct
successors and never touch what came before, so `ACT-CC-P11-005 §16`'s ban on
mutating history holds because no code path exists to violate it.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .exceptions import (
    EscalationRequired,
    InvalidPlan,
    UnsequenceablePlan,
)
from .goal import AuthorityProvenance, Goal
from .interfaces import (
    AdaptationClass,
    DelegationRequirement,
    PlanningEvidence,
    WorkPreparation,
)
from .plan import Plan, PlanOrigin, PlanStep


def sequence(plan: Plan) -> Tuple[PlanStep, ...]:
    """Order steps by **declared dependencies only** — the authorized `SEQUENCE`.

    A stable topological sort. Among steps whose dependencies are all satisfied,
    the one the author **declared first** goes first.

    **That tie-break is the whole boundary.** `DP-01 §3 W2` holds the
    prioritization / ranking / decision-heuristic frontier reserved, and
    `ACT-CC-P11-005 §13` requires `SEQUENCING` be distinguishable from
    ``AUTONOMOUS PRIORITIZATION / DECISION AUTHORITY``. Breaking ties by
    declaration order reads a fact the author stated. Breaking them by *any*
    computed property — cost, urgency, dependents, estimated value — would be
    this module forming a judgement about what matters more, which is precisely
    the reserved capability. The difference is not the sophistication of the
    rule; it is whether the order comes from the author or from here.

    Raises rather than guessing when the graph is broken: a cycle has no declared
    order, and inventing one would enter that frontier through the back door.
    """
    by_key = {step.key: step for step in plan.steps}
    for step in plan.steps:
        for dependency in step.depends_on:
            if dependency not in by_key:
                raise UnsequenceablePlan(
                    f"step {step.key!r} depends on unknown step {dependency!r}")

    ordered: List[PlanStep] = []
    placed: set = set()
    remaining = list(plan.steps)  # declaration order preserved
    while remaining:
        ready = [s for s in remaining if all(d in placed for d in s.depends_on)]
        if not ready:
            stuck = sorted(s.key for s in remaining)
            raise UnsequenceablePlan(
                f"dependency cycle among steps: {stuck} — a cycle declares no "
                "order, and choosing one would be prioritization, not sequencing")
        chosen = ready[0]          # first *declared*, not first by any measure
        ordered.append(chosen)
        placed.add(chosen.key)
        remaining.remove(chosen)
    return tuple(ordered)


def classify_adaptation(plan: Plan, required_authority: Optional[str]
                        ) -> AdaptationClass:
    """`DETECT → CLASSIFY`, without performing anything.

    `ACT-CC-P11-005 §15`: the correct behaviour is
    ``DETECT → CLASSIFY → ESCALATE``, never ``DETECT → SELF-AUTHORIZE``. This is
    the classify step, separated so that a caller can learn what a change would
    need **before** attempting it — detect-only in the literal sense.

    ``required_authority`` of ``None`` means the change stays inside what the
    plan already cites. Anything else — including an instrument that genuinely
    exists and would genuinely permit the change — classifies as escalation,
    because deciding that a different instrument covers this change is a reading
    of that instrument, and readings are human acts. `ACT-CC-P11-005 §36`:
    ``NECESSITY ≠ AUTHORITY``.
    """
    if required_authority is None:
        return AdaptationClass.WITHIN_AUTHORITY
    if required_authority == plan.authority.instrument:
        return AdaptationClass.WITHIN_AUTHORITY
    return AdaptationClass.REQUIRES_ESCALATION


class PlanningSurface:
    """The evolving chain of Plan versions, per Goal.

    Holds Goals and the append-only version chains that decompose them. This is
    the object that makes the lifecycle *mutable* while every version stays
    immutable.

    **Bounded to Planning.** `ACT-CC-P11-005 §30`: ``P11 PLANNING STATE ≠ P12
    UNIFIED OPERATIONAL STATE``, and *"System-wide integration belongs to P12."*
    This surface therefore knows about goals and plans and **nothing else** — it
    aggregates no runtime, workflow, trace, memory or execution state, and offers
    no system-wide view. `DP-04 §8.4` places `OrganizationalState` integration in
    P12; a planning surface that started answering *"what is the organization
    doing"* would be that, built early and unauthorized.
    """

    def __init__(self):
        self._goals: Dict[str, Goal] = {}
        self._chains: Dict[str, List[Plan]] = {}
        self._by_key: Dict[str, Plan] = {}

    # ---- PLAN ------------------------------------------------------------
    def declare(self, goal: Goal) -> Goal:
        """Record organizational intent. Grants nothing. ``GOAL ≠ AUTHORITY``."""
        if goal.key in self._goals:
            raise InvalidPlan(f"goal already declared: {goal.key!r}")
        self._goals[goal.key] = goal
        self._chains[goal.key] = []
        return goal

    def goal(self, key: str) -> Goal:
        if key not in self._goals:
            raise InvalidPlan(f"no such goal: {key!r}")
        return self._goals[key]

    def adopt(self, plan: Plan) -> Plan:
        """Enter the first version of a plan for a declared Goal."""
        if plan.goal_key not in self._goals:
            raise InvalidPlan(
                f"plan {plan.key!r} decomposes undeclared goal {plan.goal_key!r}")
        if plan.key in self._by_key:
            raise InvalidPlan(f"plan version already exists: {plan.key!r}")
        if self._chains[plan.goal_key]:
            raise InvalidPlan(
                f"goal {plan.goal_key!r} already has a plan — use revise() or "
                "adapt(), which preserve the version it would otherwise replace")
        if plan.origin is not PlanOrigin.PLANNED:
            raise InvalidPlan("the first version of a plan has origin PLANNED")
        sequence(plan)  # refuse to adopt a plan that cannot be ordered
        self._chains[plan.goal_key].append(plan)
        self._by_key[plan.key] = plan
        return plan

    # ---- ADAPT / REVISE --------------------------------------------------
    def _succeed(self, previous: Plan, steps: Tuple[PlanStep, ...],
                 origin: PlanOrigin, reason: str,
                 evidence: Tuple[str, ...]) -> Plan:
        successor = Plan(
            key=f"{previous.key}+{previous.revision + 1}",
            goal_key=previous.goal_key,
            steps=steps,
            authority=previous.authority,   # carried, never widened
            origin=origin,
            revision=previous.revision + 1,
            supersedes=previous.key,
            reason=reason,
            evidence=evidence,
        )
        sequence(successor)
        self._chains[previous.goal_key].append(successor)
        self._by_key[successor.key] = successor
        return successor

    def adapt(self, plan: Plan, *, steps: Tuple[PlanStep, ...], reason: str,
              evidence: Tuple[PlanningEvidence, ...] = (),
              required_authority: Optional[str] = None) -> Plan:
        """Adjust a plan in response to what was observed. `ADAPT`.

        `ACT-CC-P11-005 §15`: ``ADAPT ≠ SELF-AUTHORIZATION``. A plan *"may adapt
        to new evidence only within its existing authority boundary"*; anything
        needing new authority must escalate.

        The successor **carries the predecessor's authority citation unchanged**.
        There is no parameter that widens it — not because widening is checked
        and refused, but because the operation has no way to express it. Evidence
        is recorded as motivation and plays no part in the authority decision:
        ``EVIDENCE ≠ AUTHORIZATION``.
        """
        self._require_current(plan)
        if classify_adaptation(plan, required_authority) is \
                AdaptationClass.REQUIRES_ESCALATION:
            raise EscalationRequired(
                f"adapting plan {plan.key!r} would need authority the plan does "
                f"not hold — escalate rather than expand",
                required=str(required_authority),
                held=plan.authority.instrument)
        if not reason or not reason.strip():
            raise InvalidPlan("adaptation must record why the plan changed")
        return self._succeed(plan, steps, PlanOrigin.ADAPTED, reason,
                             tuple(f"{e.source}: {e.observation}" for e in evidence))

    def revise(self, plan: Plan, *, steps: Tuple[PlanStep, ...], reason: str,
               evidence: Tuple[PlanningEvidence, ...] = (),
               required_authority: Optional[str] = None) -> Plan:
        """Replace a plan with a successor, retaining the original. `REVISE`.

        `ACT-CC-P11-005 §16`: revision must not *"erase the distinction between
        prior and current state"*, must not *"present a revised plan as the
        original plan"*, and must not *"mutate history merely to make the current
        plan appear continuous."*

        All three hold structurally: the predecessor is untouched and stays
        readable through `history()`, the successor names what it supersedes and
        why, and `current()` reports the newest version rather than pretending
        there was only ever one.
        """
        self._require_current(plan)
        if classify_adaptation(plan, required_authority) is \
                AdaptationClass.REQUIRES_ESCALATION:
            raise EscalationRequired(
                f"revising plan {plan.key!r} would need authority the plan does "
                f"not hold — escalate rather than expand",
                required=str(required_authority),
                held=plan.authority.instrument)
        if not reason or not reason.strip():
            raise InvalidPlan("revision must record why the plan changed")
        return self._succeed(plan, steps, PlanOrigin.REVISED, reason,
                             tuple(f"{e.source}: {e.observation}" for e in evidence))

    def _require_current(self, plan: Plan) -> None:
        chain = self._chains.get(plan.goal_key)
        if not chain or plan.key not in self._by_key:
            raise InvalidPlan(f"plan {plan.key!r} is not on this surface")
        if chain[-1].key != plan.key:
            raise InvalidPlan(
                f"plan {plan.key!r} is superseded by {chain[-1].key!r} — "
                "a superseded version cannot be changed, and changing one would "
                "fork history rather than continue it")

    # ---- state ------------------------------------------------------------
    def current(self, goal_key: str) -> Plan:
        chain = self._chains.get(goal_key)
        if not chain:
            raise InvalidPlan(f"goal {goal_key!r} has no plan")
        return chain[-1]

    def history(self, goal_key: str) -> Tuple[Plan, ...]:
        """Every version, oldest first. The original remains readable forever."""
        return tuple(self._chains.get(goal_key, ()))

    def superseded(self, goal_key: str) -> Tuple[Plan, ...]:
        """Versions that have been replaced — **derived, never stamped**.

        Supersession is a fact about the chain, not a flag written onto a record.
        Deriving it means a retired version was never edited to say so, which is
        why `ACT-CC-P11-005 §16`'s ban on mutating history cannot be violated
        here even by mistake.
        """
        return tuple(self._chains.get(goal_key, ())[:-1])

    def is_superseded(self, plan: Plan) -> bool:
        chain = self._chains.get(plan.goal_key, ())
        return bool(chain) and chain[-1].key != plan.key

    # ---- handoffs ---------------------------------------------------------
    def prepare_for_workflow(self, plan: Plan) -> Tuple[WorkPreparation, ...]:
        """Describe the plan's work in dependency order, for Workflow.

        `ACT-CC-P11-005 §10`: ``PLANNING → WORKFLOW`` must *"preserve authority
        provenance"*, and Planning *"must not silently become Workflow."*

        Returns inert descriptions carrying the authority citation forward.
        Nothing here starts, routes, schedules or transitions anything — Workflow
        does that, and this surface has no handle on it.
        """
        self._require_current(plan)
        return tuple(
            WorkPreparation(
                plan_key=plan.key,
                step_key=step.key,
                statement=step.statement,
                authority_cited=plan.authority_provenance(),
                depends_on=step.depends_on,
            )
            for step in sequence(plan)
        )

    def delegation_requirements(self, plan: Plan
                                ) -> Tuple[DelegationRequirement, ...]:
        """Identify work the plan says needs delegating. **Delegates nothing.**

        `ACT-CC-P11-005 §11` permits Planning to identify such work and prepare
        delegation-relevant information, and forbids it to fabricate a delegator
        or convert a plan into a delegation record. The returned type has no
        delegator field to fabricate one into.
        """
        self._require_current(plan)
        return tuple(
            DelegationRequirement(
                plan_key=plan.key,
                step_key=step.key,
                scope_described=step.statement,
                authority_cited=plan.authority_provenance(),
            )
            for step in sequence(plan) if step.requires_delegation
        )
