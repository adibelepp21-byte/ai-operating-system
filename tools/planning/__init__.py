"""`P11-W2` — the organizational Planning surface.

Authorized by `DP-01 §3 W2`; shaped by `DP-03 §8.4` and `DP-04 §8.1`/`§8.2`.
Constructed under `ACT-CC-P11-005`.

**The architecture, from the issued instruments.** `DP-03 §8.4` chooses an
``ORGANIZATIONAL-LAYER PLANNING SURFACE`` and states that it *"may use persisted
organizational records where appropriate, but the architecture MUST support the
mutable Plan lifecycle"* — `PLAN → SEQUENCE → ADAPT → REVISE` — so that *"A Plan
is therefore not constrained to the semantics of a static declaration loaded
once."*

**That sentence rules out the pattern W3 used.** `tools/delegation_catalog.py`
is a loader over persisted markdown: read once, verified, never evolving. Reusing
it here would satisfy the word *record* and fail the word *lifecycle*. So this
package is not a loader. It is a surface over an **append-only chain of immutable
Plan versions**, where the chain evolves and no version ever does.

**Why immutable versions produce a mutable lifecycle.** `ACT-CC-P11-005 §16`
requires that revision *"not erase the distinction between prior and current
state"* and forbids mutating history *"merely to make the current plan appear
continuous."* A `Plan` is therefore frozen: adaptation and revision **construct a
successor** rather than edit a predecessor, and supersession is *derived* from
the chain rather than stamped onto the record it retires. History cannot be
rewritten because there is no operation that writes to a past version — the
guarantee is structural, not promised.

**Residency.** `DP-03 §8.4` places Planning *"outside the frozen Native Core"*.
Native Core Blueprint `§4` fixes the core at *"exactly the eleven frozen
subsystem boundaries — no more"*, and `DP-01 §4` confirms
`NO NEW NATIVE CORE SUBSYSTEM OR ENTITY #12 IS AUTHORIZED`. The organizational
layer's existing code home is ``tools/`` — where `organization_catalog` and
`delegation_catalog` already live — so this package joins them.

    **Observation, not an action taken.** ``consumers/`` exists as a top-level
    region only because `DEC-P6-042` authorized it. A dedicated organizational-
    layer region would need its own authorizing decision, which this Act does not
    grant (`ACT-CC-P11-005 §28`, `§34.3`). ``tools/`` is therefore correct today
    and is reported as a residency question worth deciding later — **not resolved
    here, and not treated as resolved.**

**What Planning is not.** From `DP-04 §8.2`: *"Plan does not constitute
authority"* and *"A Plan cannot authorize itself."* From `DP-04 §8.1`: *"Goal
does not create authority by itself."* From `DP-03 §8.4`, Planning MUST NOT
*"create authority"*, *"self-authorize"*, *"override Governance"*, *"override
Founder authority"*, *"bypass Workflow"*, or *"create a Native Core subsystem."*

There is deliberately **no method anywhere in this package that returns whether
something is authorized.** A Plan carries a *citation* to the authority under
which it was formed and can be asked what that citation is; nothing here converts
a plan's existence, readiness, revision count, or history of success into
permission. `ACT-CC-P11-005 §14`:
``PLAN EXISTENCE ≠ AUTHORIZATION`` · ``PLAN READINESS ≠ AUTHORIZATION`` ·
``PLAN PRIORITY ≠ AUTHORIZATION`` · ``PLAN COMPLETION ≠ AUTHORITY``.

**Sequencing is authorized; prioritization is reserved.** `DP-01 §3 W2`: *"The
reserved prioritization/ranking/decision-heuristic frontier remains reserved."*
The line drawn here is exact and structural:

    SEQUENCING       an order **derived from declared dependencies** — a
                     topological sort, deterministic, with declaration order
                     breaking ties. It reads what the author stated.
    PRIORITIZATION   an order **derived from computed desirability** — scores,
                     weights, ranking, urgency, importance. It decides.

`PlanStep` carries no score, weight, rank, priority or urgency field, and
`sequence()` computes none. A tie between independent steps is broken by the
order the author declared them in, never by a judgement this package forms.
"""

from .exceptions import (
    EscalationRequired,
    InvalidGoal,
    InvalidPlan,
    PlanningError,
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
from .surface import PlanningSurface, classify_adaptation, sequence

__all__ = [
    "AdaptationClass",
    "AuthorityProvenance",
    "classify_adaptation",
    "DelegationRequirement",
    "EscalationRequired",
    "Goal",
    "InvalidGoal",
    "InvalidPlan",
    "Plan",
    "PlanOrigin",
    "PlanStep",
    "PlanningError",
    "PlanningEvidence",
    "PlanningSurface",
    "UnsequenceablePlan",
    "WorkPreparation",
    "sequence",
]
