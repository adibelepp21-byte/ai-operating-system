"""The `ActionCatalog`: every action type P13 can name, and what each one is.

An action type **not** in this catalog is REFUSED by the gate. A **reserved**
type is here only so the gate can recognize it and ESCALATE it: it has no
executor, and no envelope can make it executable (Blueprint `§5.2`). These are
the reserved types: code change, governance or certified-evidence change,
delegation issuance, knowledge admission, Native Core change, Constitution
change. `P13-018 §3` adds three: self-expanding the envelope, granting
authority, and external or business action.

Every executable type runs an **existing resident verifier, read-only**. That is
all `P13-ENV-01` permits: items 1 and 6. P13 has no executor that writes.
The cycle's own records are written by the evidence store, on items 3 and 4.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple

from tools.p13.paths import Paths

Produced = Dict[str, Any]


@dataclass(frozen=True)
class ActionType:
    name: str
    reserved: bool
    produces: Tuple[str, ...] = ()
    executor: str = ""
    run: Optional[Callable[[Paths], Produced]] = None


def _integrity(paths: Paths) -> Produced:
    from tools import certified_evidence_integrity as integrity
    report = integrity.verify(paths.repo)
    return {"integrity.holds": report.holds,
            "integrity.phases": {p: r.holds for p, r in report.phases.items()}}


def _reconciliation(paths: Paths) -> Produced:
    from tools import foundational_question_reconciliation as reconciliation
    result = reconciliation.verify(paths.matrix, paths.repo)
    return {"verification.foundational_question_reconciliation": {
        "holds": result["holds"], "counts": result["counts"],
        "faults": len(result["faults"])}}


def _ecosystem(paths: Paths) -> Produced:
    from tools import ecosystem_relationships as ecosystem
    report = ecosystem.report(paths.repo)
    return {"verification.ecosystem_relationships": {
        f"{r['left']}↔{r['right']}": r["status"] for r in report["relationships"]}}


def _own_evidence(paths: Paths) -> Produced:
    from tools.p13.evidence import EvidenceStore
    return {"verification.p13_evidence": EvidenceStore(paths).verify()}


RESERVED = (
    "change.code", "change.governance", "change.certified_evidence",
    "issue.delegation", "admit.knowledge", "change.native_core",
    "change.constitution", "expand.envelope", "grant.authority",
    "external.action",
)

CATALOG: Dict[str, ActionType] = {
    **{name: ActionType(name, reserved=True) for name in RESERVED},
    "verify.certified_evidence_integrity": ActionType(
        "verify.certified_evidence_integrity", False,
        ("integrity.holds", "integrity.phases"),
        "tools.certified_evidence_integrity.verify", _integrity),
    "verify.foundational_question_reconciliation": ActionType(
        "verify.foundational_question_reconciliation", False,
        ("verification.foundational_question_reconciliation",),
        "tools.foundational_question_reconciliation.verify", _reconciliation),
    "verify.ecosystem_relationships": ActionType(
        "verify.ecosystem_relationships", False,
        ("verification.ecosystem_relationships",),
        "tools.ecosystem_relationships.report", _ecosystem),
    "verify.p13_evidence": ActionType(
        "verify.p13_evidence", False, ("verification.p13_evidence",),
        "tools.p13.evidence.EvidenceStore.verify", _own_evidence),
    # Item 5. The gate records escalations itself; this entry is what an
    # envelope must permit for them to stand on it rather than on G-02 alone.
    "escalate": ActionType("escalate", False, (), "tools.escalation_register"),
}


def producer(key: str, catalog: Dict[str, ActionType] = CATALOG) -> Optional[str]:
    """The executable action type whose run yields `key`, if one exists."""
    return next((a.name for a in catalog.values()
                 if not a.reserved and a.run and key in a.produces), None)
