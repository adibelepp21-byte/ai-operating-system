"""`P11-W6` → `P11-W2` — the evidence path from Observation to Planning.

Authorized by `DP-01 §3 W6`: *"Performance evidence may inform Planning or
Governance through their legitimate authority paths."* Constructed under
`ACT-CC-P11-006 §16`, which requires that each transition in the P11 chain be
**real** rather than assumed — *"Do not accept: A exists, B exists, therefore
A → B exists."*

Before this module, `OptimizationObservation` and `PlanningEvidence` both
existed and **nothing connected them.** `PlanningEvidence` could only be built by
hand, so `OBSERVE → ADAPT` was a transition on a diagram and not in the code.

**Why this is a separate module and not part of either side.**

    Optimization  ◀── reads ──  performance_evidence  ── produces ──▶  Planning

Neither endpoint depends on the other. The Optimization boundary states that *"no
subsystem imports Optimization — no inversion, no cycle"*, and the W2 negative
controls assert that Planning imports neither Optimization nor Governance. An
adapter living inside Planning would break both. Living here, it depends on both
and **is depended on by neither**, so the direction stays inverted exactly as the
frozen boundary requires.

**What crossing this boundary does not do.** `DP-01 §3 W6` fixes Performance as
`DETECT-ONLY` and lists what it may not do: *"authorize"*, *"approve"*,
*"promote"*, *"decide"*, *"create governance authority"*, *"create execution
authority"*, and *"silently convert observation into authorization."* It closes
with:

    PERFORMANCE EVIDENCE ≠ PLANNING AUTHORITY.

So this module produces **evidence and nothing else.** It does not call
`adapt()`, does not choose whether a plan should change, and holds no reference
to any plan or surface. A human or a caller with authority decides what to do
with what it returns — and `adapt()` checks the authority citation separately,
ignoring evidence entirely when it does.

**The asymmetry that makes that safe:** evidence can motivate a change but can
never widen the authority under which the change happens. Twenty observations
authorize exactly as much as zero, which the W2 controls assert directly.
"""

from __future__ import annotations

from typing import Iterable, Tuple

from native_core.core.optimization import (
    OBSERVABLE_SOURCES,
    OptimizationObservation,
)
from tools.planning import PlanningEvidence


class UnobservableSource(ValueError):
    """The observation names a source Optimization does not observe.

    Fail closed (`PR-4`). The frozen boundary observes Trace and Memory; an
    observation claiming any other origin has not come through the sanctioned
    detect-only surface, and admitting it would let arbitrary text enter Planning
    wearing Optimization's name.
    """


def as_planning_evidence(observation: OptimizationObservation) -> PlanningEvidence:
    """Convert one detect-only observation into planning evidence.

    The conversion is deliberately **lossy in one direction only**: it carries
    what was observed and where it came from, and carries **no judgement about
    what should happen next.** `DP-01 §3 W6` permits Performance to *"identify
    improvement opportunities"* but not to *"decide"*, and a field saying
    *recommended action* would be that decision travelling under the name of
    evidence.

    The source is preserved rather than normalized away, so a reader can weigh
    it. It confers nothing: evidence from Trace carries exactly the authority of
    evidence typed by hand, which is none.
    """
    if not isinstance(observation, OptimizationObservation):
        raise TypeError(
            "planning evidence is derived from an OptimizationObservation — "
            "the detect-only surface is the only sanctioned origin")
    if observation.source not in OBSERVABLE_SOURCES:
        raise UnobservableSource(
            f"{observation.source!r} is not an observable source; "
            f"Optimization observes {sorted(OBSERVABLE_SOURCES)}")
    return PlanningEvidence(
        source=f"optimization/{observation.source}",
        observation=f"{observation.subject}: {observation.observed}",
    )


def collect(observations: Iterable[OptimizationObservation]
            ) -> Tuple[PlanningEvidence, ...]:
    """Convert a batch, preserving order.

    Order is preserved and **nothing is ranked, scored or filtered by
    significance.** `DP-03 §8.3` holds the prioritization / ranking /
    decision-heuristic frontier reserved, and sorting observations by how
    important they look is that frontier — the same boundary `sequence()`
    respects on the Planning side, applied to the input rather than the output.
    """
    return tuple(as_planning_evidence(o) for o in observations)
