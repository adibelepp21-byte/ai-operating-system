"""What Planning hands to its neighbours — and what it deliberately cannot.

Three boundaries meet here, and each is a place `ACT-CC-P11-005` expects
collapse: Workflow (`§10`), Delegation (`§11`), Observation/Performance (`§12`).
Every type below is **inert**: a frozen description with no method that starts,
routes, delegates, or authorizes anything. Planning describes; others act.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from .goal import AuthorityProvenance


def _require_provenance(value, what: str) -> None:
    """Refuse a citation that is merely *shaped* like one.

    **This guard is the correction of a defect in the first W2 increment.** Both
    handoff types originally carried ``authority_cited: str`` — the formatted
    output of `AuthorityProvenance.cited()`. That flattened a **validated
    citation** into **free text** at the exact moment authority crossed a
    boundary, and a plain string field accepts anything:

        WorkPreparation(..., authority_cited="Founder Reserved Authority")

    was constructible, and **indistinguishable to any consumer from a genuine
    handoff.** `ACT-CC-P11-006 §17` names that failure directly — authority
    *fabricated*, or *lost*, at a transition — and `§19` criterion 7 is why it
    had to be fixed before W4: the autonomous loop passes authority across every
    one of these transitions, so a forgeable citation at the first handoff
    becomes a forgeable citation throughout.

    Carrying the object costs nothing. `AuthorityProvenance` is frozen and has a
    single method returning a string; passing it adds **no capability**, only the
    guarantee that the cited record resolves. The string bought nothing and gave
    up the check.

    **What this still does not establish:** that the cited instrument grants what
    the citing artifact claims. Resolution proves the pointer is real. That
    reading remains a human act, exactly as `AuthorityProvenance` itself says.
    """
    if not isinstance(value, AuthorityProvenance):
        raise TypeError(
            f"{what} requires an AuthorityProvenance, not {type(value).__name__} "
            "— a citation that is only text cannot be verified by whoever "
            "receives it, and unverifiable provenance is fabricated provenance")


@dataclass(frozen=True)
class WorkPreparation:
    """Work described for Workflow to coordinate. **Not a Workflow.**

    `ACT-CC-P11-005 §10`: ``PLANNING ≠ WORKFLOW``, and
    ``PLANNING → WORKFLOW`` *"must preserve authority provenance."* `DP-03 §8.4`
    forbids Planning to *"bypass Workflow."*

    So this carries the authority citation forward — the provenance survives the
    handoff — and carries **no method that transitions anything**. It cannot be
    started, run, or completed. Workflow owns
    `DEFINED · READY · RUNNING · SUCCEEDED · FAILED`; this type touches none of
    them, and a test asserts the two vocabularies stay disjoint.

    A `WorkPreparation` is a proposal in the plain sense: something offered for a
    coordinating surface to accept. Its existence obliges nobody.
    """

    plan_key: str
    step_key: str
    statement: str
    authority: AuthorityProvenance
    depends_on: Tuple[str, ...] = ()

    def __post_init__(self):
        _require_provenance(self.authority, "prepared work")

    def authority_cited(self) -> str:
        """What this preparation claims as its authority. Not a permission check."""
        return self.authority.cited()


@dataclass(frozen=True)
class DelegationRequirement:
    """Work Planning has identified as needing delegation. **Not a delegation.**

    `ACT-CC-P11-005 §11` permits Planning to *"identify work that requires
    delegation"* and to *"prepare delegation-relevant information"*, while
    forbidding it to *"fabricate a delegator"*, *"create authority through
    planning"*, *"populate delegation merely to demonstrate integration"*,
    *"impersonate an authorized delegator"*, or *"convert a plan into a
    delegation record."*

    **The delegator field does not exist**, and that absence is the control. A
    field would have to be filled, and Planning has nobody legitimate to fill it
    with — so it would be filled with a guess, and a guessed delegator is exactly
    the impersonation the Act forbids. `tools/delegation_catalog.py` requires an
    ``Authority Source`` that owns the scope; Planning cannot supply one, and
    saying so structurally is more honest than supplying a placeholder.

    This type therefore **cannot be rendered into a valid delegation record**,
    and a prove-me-wrong test asserts that the delegation catalog rejects
    anything derived from it. `ACT-CC-P11-005 §11`: the empty W3 population
    *"remains valid if no legitimate delegator exists."*
    """

    plan_key: str
    step_key: str
    scope_described: str
    authority: AuthorityProvenance

    def __post_init__(self):
        _require_provenance(self.authority, "a delegation requirement")

    def authority_cited(self) -> str:
        """What this requirement claims as its authority. Not a permission check."""
        return self.authority.cited()

    def as_delegation_record(self):  # pragma: no cover - intentionally absent
        raise NotImplementedError(
            "Planning cannot author a delegation record. `ACT-CC-P11-005 §11` "
            "forbids converting a plan into a delegation and forbids "
            "fabricating a delegator; only a unit that holds the authority may "
            "delegate it. PLAN ≠ AUTHORITY SOURCE.")


@dataclass(frozen=True)
class PlanningEvidence:
    """Something observed, offered to Planning as input. **Not authorization.**

    `ACT-CC-P11-005 §12` fixes the valid direction as
    ``OBSERVATION → EVIDENCE → PLANNING INPUT`` and the invalid one as
    ``OBSERVATION → AUTHORIZATION``. `DP-03 §8.3` confirms Performance as
    ``DETECT-ONLY``, and the Optimization boundary states it *"never submits,
    sends, notifies, requests, approves, promotes, authorizes, or decides."*

    Evidence can motivate a change. It can never widen the authority under which
    the change happens — `adapt()` checks the authority citation separately and
    ignores this entirely when doing so. ``EVIDENCE ≠ AUTHORIZATION``.

    ``source`` records where the observation came from so a later reader can
    weigh it. It confers nothing: an observation from Optimization carries no
    more permission than one typed by hand.
    """

    source: str
    observation: str

    def __post_init__(self):
        if not isinstance(self.observation, str) or not self.observation.strip():
            raise ValueError("evidence requires an observation")


class AdaptationClass(Enum):
    """The classification step of ``DETECT → CLASSIFY → ESCALATE``.

    `ACT-CC-P11-005 §15` requires that adaptation needing new authority
    *"escalate rather than silently expand"*, and `§13` requires that a
    dependency on reserved capability be *identified and classified* rather than
    invented.

    Returned by ``classify_adaptation`` so that classification can happen
    **without** performing the change — detect-only in the literal sense. The
    escalating path raises; this one only reports.
    """

    WITHIN_AUTHORITY = "within-authority"
    REQUIRES_ESCALATION = "requires-escalation"
