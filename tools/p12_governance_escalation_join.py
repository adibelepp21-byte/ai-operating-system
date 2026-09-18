"""`P12-W3` — joining a persisted escalation to the grant it was raised under.

`W4-GAP-008` / `W2-GAP-007` (`P12-W4-EXECUTION-INTEGRATION.md §13`,
`P12-W2-UNIFIED-OPERATIONAL-STATE.md §11`): a refusal reaches the grant it was
refused under, but only through a regex over the record's prose ``subject``
field — *"that works until somebody rewords the subject... the relation is
carried by a spelling rather than by a reference."* Both Acts declined to fix
it themselves and named it **W3's to close**: `ACT §30`, `W4 ≠ W3`.

**This module does not modify `EscalationRecord`.** `tools/escalation_register.py`
is frozen and written-once, exactly as `P12-W4-EXECUTION-INTEGRATION.md §3`
found `TraceRecord` to be: *"`TraceRecord` is ratified and closed... So the
relation lives beside the record, on a P12 surface, and names it."* The same
choice is made here. `ExecutionManifest` sits beside `TraceRecord`; this join
sits beside `EscalationRecord`. Neither widens what it sits beside.

**The join is captured structurally, at record time, from the caller's own
delegation object** — not parsed out of prose after the fact. The delegation
id was always available at the call site (`tools/w4_first_run.py:314` already
holds ``delegation.delegation_id`` when it writes ``subject``); what was
missing was only a place to put it that a reader could resolve by reference.

This module is additive only. No existing function's signature changes, and
no historical `.escalation.json` record is read, touched, or retroactively
joined — `§22`: writing a join for a record that never captured one at the
time would be manufacturing evidence about what that record's author knew.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional, Tuple

from tools.escalation_register import EscalationRegister

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The two sanctioned refusal types, named for what this module accepts as
#: `refusal_type` — the same set `tools/escalation_register.py` sanctions,
#: re-declared rather than imported so this module's own validation does not
#: depend on the writer it sits beside staying importable in a particular way.
SANCTIONED_REFUSAL_TYPES = ("ExecutionRefused", "EscalationRequired")


class GovernanceJoinError(RuntimeError):
    """Fail closed (`PR-4`)."""


@dataclass(frozen=True)
class EscalationGrantJoin:
    """One escalation, joined to the grant it was raised under. Written once.

    Carries only what a reader needs to resolve the relationship by
    reference: which escalation, which delegation, which refusal type. It
    does not repeat anything `EscalationRecord` already carries — repeating a
    fact in a second place is how the two drift, which is the defect this
    module exists to remove.
    """

    escalation_id: str
    delegation_id: str
    refusal_type: str
    joined_at: str

    def to_payload(self) -> dict:
        return {
            "escalation_id": self.escalation_id,
            "delegation_id": self.delegation_id,
            "refusal_type": self.refusal_type,
            "joined_at": self.joined_at,
        }


def join_escalation_to_grant(root: Path, register: EscalationRegister,
                              escalation_id: str, *, delegation_id: str,
                              refusal_type: str) -> EscalationGrantJoin:
    """Persist the structural join. Returns what was written.

    ``register`` must be the same register the escalation was recorded
    through — the join refuses to name an escalation that register does not
    hold, so a join can never point at a record that does not exist.
    """
    if not isinstance(root, Path):
        raise GovernanceJoinError("a join requires an explicit root")
    if not isinstance(delegation_id, str) or not delegation_id.strip():
        raise GovernanceJoinError(
            "a join requires the real delegation_id the grant was issued "
            "under — not inferred, not parsed, supplied by the caller that "
            "held the delegation")
    if refusal_type not in SANCTIONED_REFUSAL_TYPES:
        raise GovernanceJoinError(
            f"{refusal_type!r} is not a sanctioned refusal type — a join "
            "may not claim a relationship the register would not have "
            "accepted in the first place")

    # The escalation must already exist. A join cannot precede its subject —
    # raises EscalationRegisterError (a RuntimeError) if it does not.
    recorded = register.load(escalation_id)

    # Since `ACT-CC-P12-027` the record names its own refusal type (`§33`), so
    # two surfaces now state one fact and they must not disagree — a join
    # contradicting the record it sits beside is worse than either alone.
    # A record written before that field existed says nothing, and **silence is
    # not a contradiction**: an absent value is not checked, never overridden.
    # "Cannot check" and "checked and found wrong" are different answers, and
    # only the second may refuse.
    recorded_type = recorded.get("refusal_type")
    if recorded_type is not None and recorded_type != refusal_type:
        raise GovernanceJoinError(
            f"the escalation record names {recorded_type!r} and this join "
            f"claims {refusal_type!r} — a join may not contradict the record "
            "it sits beside")

    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{escalation_id}.governance-join.json"
    if path.exists():
        raise GovernanceJoinError(
            f"refusing to overwrite {path.name} — append-only, one join "
            "per escalation, exactly as the escalation record it sits "
            "beside is append-only")

    join = EscalationGrantJoin(
        escalation_id=escalation_id,
        delegation_id=delegation_id,
        refusal_type=refusal_type,
        joined_at=datetime.now(timezone.utc).isoformat())
    path.write_text(json.dumps(join.to_payload(), indent=2), encoding="utf-8")
    return join


def join_refusals_to_grants(root: Optional[Path], refusals, *, subject: str,
                             authority, delegation_for: Callable
                             ) -> Tuple[str, ...]:
    """`ACT-CC-P12-005` — the one wiring path for resident consumption.

    Composes two existing, unmodified functions rather than adding a third
    way to record a refusal: `tools.escalation_register.record_refusals`
    (reused exactly as `tools/w4_first_run.py` and the two `tools/w1_*_run.py`
    paths already call it) writes each escalation, then
    `join_escalation_to_grant` — this module's own, already-verified writer —
    joins it to the grant `delegation_for(refusal)` names.

    ``delegation_for`` is the caller's own knowledge of which delegation each
    refusal was actually raised under. It is **never inferred here** — for a
    single-delegation call site it is a constant; for a call site that binds
    one delegation per step (`tools/w1_cross_department_run.py`), it must
    look up the delegation that governed the specific step the refusal
    names (`refusal.required`). Supplying the wrong one is a caller defect
    this function has no way to detect, exactly as before this function
    existed — it narrows nothing `join_escalation_to_grant`'s own contract
    already stated.

    Returns exactly what `record_refusals` returns: the escalation ids, in
    order. If `root` is `None` (the existing `persist=False` convention),
    nothing is recorded or joined — matching `record_refusals`'s own
    behaviour, unchanged.
    """
    from tools.escalation_register import EscalationRegister, record_refusals

    escalation_ids = record_refusals(root, refusals, subject=subject,
                                      authority=authority)
    if not escalation_ids:
        return escalation_ids

    register = EscalationRegister(root)
    for escalation_id, refusal in zip(escalation_ids, refusals):
        join_escalation_to_grant(
            root, register, escalation_id,
            delegation_id=delegation_for(refusal),
            refusal_type=type(refusal).__name__)
    return escalation_ids
