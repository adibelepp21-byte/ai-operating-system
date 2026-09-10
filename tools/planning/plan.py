"""Plan and PlanStep — one immutable version in an evolving chain.

`DP-04 §8.2`: Plan *"shall exist in the organizational layer outside the frozen
Native Core"*, *"represents the structured decomposition and sequencing of
organizational work"*, *"does not constitute authority"*, and *"cannot authorize
itself."*
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple

from .exceptions import InvalidPlan
from .goal import AuthorityProvenance


class PlanOrigin(Enum):
    """How a version came to exist. **Not a workflow state.**

    `ACT-CC-P11-005 §10` and `NC-W2-16` require Planning to stay distinct from
    Workflow. `native_core/core/workflow/lifecycle.py` owns the execution states
    `DEFINED · READY · RUNNING · SUCCEEDED · FAILED`, and **none of them appears
    here.** A Plan is never RUNNING and never SUCCEEDED: those describe work
    being done, and Planning does not do work.

    Keeping the vocabularies disjoint is what makes *"Planning must not silently
    become Workflow"* checkable rather than merely stated — a test asserts the
    two name sets do not intersect.
    """

    PLANNED = "planned"
    ADAPTED = "adapted"
    REVISED = "revised"


@dataclass(frozen=True)
class PlanStep:
    """One unit of planned work.

    ``depends_on`` names other steps in the same plan. It is the **only** input
    to ordering, which is what keeps ordering inside the authorized
    `SEQUENCE` semantics and outside the reserved prioritization frontier.

    **Deliberately absent: any score, weight, rank, priority, urgency or
    importance field.** `DP-01 §3 W2` holds that frontier reserved. A field like
    that would not merely enable prioritization later — its presence *is* the
    judgement, because something must set it, and whatever sets it is deciding
    what matters. A test asserts no such field exists.
    """

    key: str
    statement: str
    depends_on: Tuple[str, ...] = ()
    requires_delegation: bool = False

    def __post_init__(self):
        if not isinstance(self.key, str) or not self.key.strip():
            raise InvalidPlan("a plan step requires a key")
        if not isinstance(self.statement, str) or not self.statement.strip():
            raise InvalidPlan("a plan step requires a statement")
        if not isinstance(self.depends_on, tuple):
            raise InvalidPlan("depends_on must be a tuple of step keys")
        if self.key in self.depends_on:
            raise InvalidPlan(f"step {self.key!r} depends on itself")


@dataclass(frozen=True)
class Plan:
    """One immutable version of a plan for a Goal.

    **Frozen on purpose.** `ACT-CC-P11-005 §16` forbids mutating history *"merely
    to make the current plan appear continuous"* and forbids presenting *"a
    revised plan as the original plan."* Because no operation writes to an
    existing version, neither is possible — the prohibition is enforced by the
    absence of a capability rather than by a rule someone must remember.

    The lifecycle is mutable at the level of the *chain*: `adapt()` and
    `revise()` construct successors, and `PlanningSurface` tracks which version
    is current. `DP-03 §8.4`: a Plan is *"not constrained to the semantics of a
    static declaration loaded once."*

    ``supersedes`` points backwards, never forwards. A version cannot know what
    replaced it — learning that would require editing it.
    """

    key: str
    goal_key: str
    steps: Tuple[PlanStep, ...]
    authority: AuthorityProvenance
    origin: PlanOrigin = PlanOrigin.PLANNED
    revision: int = 0
    supersedes: Optional[str] = None
    reason: Optional[str] = None
    evidence: Tuple[str, ...] = field(default=())

    def __post_init__(self):
        if not isinstance(self.key, str) or not self.key.strip():
            raise InvalidPlan("a plan requires a key")
        if not isinstance(self.goal_key, str) or not self.goal_key.strip():
            raise InvalidPlan("a plan requires the goal it decomposes")
        if not isinstance(self.steps, tuple) or not self.steps:
            raise InvalidPlan("a plan requires at least one step")
        keys = [s.key for s in self.steps]
        if len(set(keys)) != len(keys):
            raise InvalidPlan("plan step keys must be unique within a plan")
        if not isinstance(self.authority, AuthorityProvenance):
            raise InvalidPlan("a plan requires an authority citation")
        if self.origin is not PlanOrigin.PLANNED and not self.supersedes:
            raise InvalidPlan(
                f"a {self.origin.value} plan must name the version it succeeds")
        if self.origin is not PlanOrigin.PLANNED and not self.reason:
            raise InvalidPlan(
                f"a {self.origin.value} plan must record why it changed — "
                "an unexplained change is indistinguishable from a rewrite")

    def step(self, key: str) -> PlanStep:
        for candidate in self.steps:
            if candidate.key == key:
                return candidate
        raise InvalidPlan(f"no such step: {key!r}")

    def authority_provenance(self) -> str:
        """The authority this version **cites**. Not a permission check.

        Named for what it returns. A method called ``authorized()`` returning
        this string would read as a verdict at every call site, and call sites
        are where `PLAN EXISTENCE ≠ AUTHORIZATION` gets forgotten.
        """
        return self.authority.cited()
