"""The P13 closure gate: evaluation only (`FDR-G1` `FD-G2`, `§16`–`§21`, `§33`).

`FDR-G1` keeps P13 CERTIFIED + OPEN and establishes that closure needs an
explicit gate and a Founder closure decision:

```text
P13 CERTIFIED + OPEN  →  CLOSURE GATE  →  FOUNDER CLOSURE DECISION  →  P13 CLOSED
```

This module is the gate's evaluation step and nothing more. `§33` authorizes
it on four conditions:
- it records or evaluates closure criteria only;
- it does not close P13;
- it gives Claude no closure authority;
- it does not alter P13's certification.

It evaluates the eight minimum determinations of `§18`, in the Founder's
words, against the resident record. Each gets one of four statuses:

| Status | Meaning |
|---|---|
| `EVIDENCED` | the record answers it, and the check re-reads that record on every run |
| `NOT EVIDENCED` | the check ran and the record does not answer it |
| `FOUNDER DETERMINATION REQUIRED` | a judgement, or a definition the Founder has not made |
| `UNDETERMINABLE` | a source could not be read |

The gate is `SATISFIED` only when every item is `EVIDENCED`. It is not
satisfied today, because several items are the Founder's to determine. Even a
satisfied gate closes nothing: *"The existence of a closure gate implementation
MUST NOT be interpreted as: P13 CLOSED."* (`§33`).

It does not decide which items the Founder must determine. It reports where
the record is silent and says so.

Nothing here authorizes anything, and nothing here writes.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
ACTS = "docs/governance/acts"
REGISTER = "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
FDR5 = f"{ACTS}/FDR-5-P13-EXIT-CONTRACT-SATISFACTION.md"
FDR7 = f"{ACTS}/FDR-7-P13-FOUNDER-CERTIFICATION-AND-FINAL-SYSTEM-ACCEPTANCE.md"
FDRG1 = f"{ACTS}/FDR-G1-POST-P13-GOVERNANCE-FOUNDATION.md"
DELEGATIONS = "docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md"
#: `ACT-CC-POST-P13-GOV-002` `§5`: the CEO's bounded A17 determination
#: (F04 `§22`, F06 A17, E1) that `P13-018` `D-1`'s authorized scope has no
#: actionable construction left. It is read from the Decision Register, the
#: only place it counts. It is not a revocation: the authorization record
#: stays in force, and its disposition is the Founder's.
EXHAUSTION = "P13-018 D-1: AUTHORIZED ACTIONABLE CONSTRUCTION SURFACE EXHAUSTED"
#: Only a Register field row declaring it counts. A mention in prose does not.
_EXHAUSTION_ROW = re.compile(r"^\| \*\*A17 determination\*\* \| " + re.escape(EXHAUSTION),
                             re.MULTILINE)
#: `FDR-7` `§8` (`FDQ-7.6` CONFIRM): the operating model retained through
#: certification.
RETAINED = "The existing bounded delegated autonomy model remains in force"

EVIDENCED = "EVIDENCED"
NOT_EVIDENCED = "NOT EVIDENCED"
FOUNDER = "FOUNDER DETERMINATION REQUIRED"
UNDETERMINABLE = "UNDETERMINABLE"
SATISFIED = "SATISFIED"
NOT_SATISFIED = "NOT SATISFIED"

#: `FDR-G1` `§18`, verbatim: what the gate must determine, at minimum.
CRITERIA = (
    "whether all authorized P13 obligations are satisfied",
    "whether no authorized construction remains",
    "whether remaining frontier items are appropriately classified",
    "whether required operational responsibilities have been transferred or "
    "explicitly retained",
    "whether residual governance matters are acceptable",
    "what evidence constitutes closure",
    "what authority grants closure",
    "what post-closure operating state means",
)


def _registered_text(relative: str, root: Path, register_text: str) -> Optional[str]:
    """The instrument's text, if it exists and the Register resolves it."""
    from tools import p12_certified_evidence_guard as sentinel
    path = root / relative
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if sentinel._register_identity(path.stem, register_text) is None:
        return None
    return text


def _item(number: int, status: str, evidence: List[str], note: str = "") -> dict:
    return {"id": f"C{number}", "criterion": CRITERIA[number - 1], "status": status,
            "evidence": evidence, "note": note}


def evaluate(root: Path = REPO_ROOT) -> Dict[str, object]:
    """Evaluate the `§18` minimum against the resident record. Closes nothing."""
    try:
        register_text = (root / REGISTER).read_text(encoding="utf-8")
    except OSError as error:
        items = [_item(n, UNDETERMINABLE, [], f"Decision Register unreadable: {error}")
                 for n in range(1, len(CRITERIA) + 1)]
        return _report(items)

    fdr5 = _registered_text(FDR5, root, register_text)
    fdr7 = _registered_text(FDR7, root, register_text)
    g1 = _registered_text(FDRG1, root, register_text)
    items = []

    # C1: the obligations the record defines are the exit contract and
    # certification. Both are Founder determinations, read from their
    # registered instruments; certification is also read through the guard.
    from tools import p12_certified_evidence_guard as sentinel
    try:
        certified = 13 in sentinel.certified_phases(root / ACTS, root / REGISTER)
    except sentinel.CertificationUndeterminable as error:
        items.append(_item(1, UNDETERMINABLE, [], str(error)))
    else:
        exit_ok = fdr5 is not None and "P13 Exit Contract = SATISFIED" in fdr5
        evidence = ([f"{FDR5}: P13 Exit Contract = SATISFIED"] if exit_ok else []) + \
                   ([f"guard: P13 certified ({FDR7})"] if certified else [])
        items.append(_item(1, EVIDENCED if exit_ok and certified else NOT_EVIDENCED,
                           evidence, "No record lists P13 obligations beyond the exit "
                           "contract and certification."))

    # C2: an authorization record in force is not remaining work. The
    # frontier is stated as NONE, and the CEO's A17 exhaustion determination
    # for `P13-018` `D-1` must be registered.
    frontier_none = g1 is not None and "P13 CONSTRUCTION FRONTIER\nNONE" in g1
    exhausted = _EXHAUSTION_ROW.search(register_text) is not None
    try:
        from tools.p13 import authority
        from tools.p13.paths import Paths
        construction = authority.authority_dimensions(Paths(root)).get(
            "construction_authorization", {}).get("state", "UNKNOWN")
    except Exception as error:  # an unreadable projection is not an answer
        construction = f"UNDETERMINABLE: {error}"
    evidence = ([f"{FDRG1} §39: P13 CONSTRUCTION FRONTIER NONE"] if frontier_none else [])
    if exhausted:
        evidence.append(f"Decision Register: {EXHAUSTION} (A17)")
    evidence.append(f"P13 authority projection: construction_authorization = "
                    f"{construction} (the record, not remaining work)")
    items.append(_item(2, EVIDENCED if frontier_none and exhausted else NOT_EVIDENCED,
                       evidence, "The P13-018 authorization record stays in force. "
                       "Its disposition at closure is the Founder's (C8)."))

    # C3: every frontier row cites evidence that still verifies, and the
    # Founder accepted the frontier as classified (`FDQ-7.7`).
    from tools import foundational_question_reconciliation as frontier
    try:
        checked = frontier.verify(root=root)
    except (OSError, ValueError) as error:
        items.append(_item(3, UNDETERMINABLE, [], str(error)))
    else:
        accepted = fdr7 is not None and \
            "FDQ-7.7 = ACCEPT AS CLASSIFIED / NON-BLOCKING" in fdr7
        evidence = [f"P13-015 matrix holds: {checked['holds']}; counts "
                    f"{json.dumps(checked['counts'], sort_keys=True)}"]
        if accepted:
            evidence.append(f"{FDR7}: FDQ-7.7 = ACCEPT AS CLASSIFIED / NON-BLOCKING")
        items.append(_item(3, EVIDENCED if checked["holds"] and accepted
                           else NOT_EVIDENCED, evidence,
                           "Accepted as classified at certification. The frontier "
                           "is not solved."))

    # C4: responsibility is retained, not transferred. `FDR-7` `§8` keeps the
    # bounded delegated model in force after certification. The in-force
    # delegation holds operational execution, and `P13-ENV-01`'s holder is P13
    # when a human or the CEO invokes it (Delegation Register `§14`).
    from tools import governance_delegation_register as delegation
    try:
        in_force = [d.identifier for d in delegation.read_register(root / DELEGATIONS)
                    if d.in_force]
    except Exception as error:  # an unreadable register is not an answer
        in_force = []
        retention_note = f"Delegation Register unreadable: {error}"
    else:
        retention_note = ""
    retained = fdr7 is not None and RETAINED in fdr7
    try:
        from tools.p13 import authority
        from tools.p13.paths import Paths
        envelopes, _ = authority.load_envelopes(Paths(root))
        surface = [f"active envelope {getattr(e, 'id', e)}" for e in envelopes]
        surface += [f"retired envelope {r.get('envelope')} ({r.get('retired_by')})"
                    for r in authority.retired_envelopes(Paths(root))]
    except Exception as error:
        surface = [f"envelopes undeterminable: {error}"]
    evidence = surface + ["live record root docs/operations/p13",
                          f"delegations in force: {in_force}"]
    if retained:
        evidence.append(f"{FDR7} §8: {RETAINED}")
    items.append(_item(4, EVIDENCED if retained and "DEL-CFV2-CEO-001" in in_force
                       else NOT_EVIDENCED, evidence,
                       retention_note or "Explicitly retained through certification, "
                       "not transferred. Retention after closure is part of the "
                       "post-closure model (C8)."))

    # C5: what remains open is listed; whether it is acceptable is a judgement.
    from tools.escalation_register import EscalationRegister
    opened = []
    for base in (root / "docs/architecture", root / "docs/operations"):
        if base.is_dir():
            for directory in sorted({p.parent for p in base.rglob("*.escalation.json")}):
                opened.extend(EscalationRegister(directory).open_escalations())
    items.append(_item(5, FOUNDER, [f"open escalations: {sorted(opened)}"],
                       "Acceptability is the Founder's judgement."))

    # C6: `FD-G2` leaves the criteria, and so the closure evidence, to be defined.
    defined = g1 is not None and "CLOSURE CRITERIA\nTO BE DEFINED" in g1
    items.append(_item(6, FOUNDER,
                       [f"{FDRG1} §44 FD-G2: CLOSURE CRITERIA TO BE DEFINED"] if defined
                       else [], "The closure evidence is not yet defined."))

    # C7: `FD-G2` names the closure authority.
    named = g1 is not None and "CLOSURE AUTHORITY\nFOUNDER" in g1
    items.append(_item(7, EVIDENCED if named else NOT_EVIDENCED,
                       [f"{FDRG1} §44 FD-G2: CLOSURE AUTHORITY FOUNDER"] if named else []))

    # C8: `§19`–`§20` set a default boundary and leave operation to be governed.
    default = g1 is not None and ("Closing P13 terminates P13 as an active phase "
                                  "lifecycle state") in g1
    items.append(_item(8, FOUNDER,
                       [f"{FDRG1} §19: closure retains certified evidence and history; "
                        "§20: post-closure operation must be governed separately"]
                       if default else [],
                       "The default boundary is set. The post-closure operating model "
                       "is not."))
    return _report(items)


def _report(items: List[dict]) -> Dict[str, object]:
    satisfied = all(item["status"] == EVIDENCED for item in items)
    return {
        "phase": "P13",
        "instrument": "FDR-G1 FD-G2, §18",
        "gate": SATISFIED if satisfied else NOT_SATISFIED,
        "closes": False,
        "closure_authority": "Founder (FDR-G1 FD-G2)",
        "criteria": items,
        "counts": {status: sum(1 for item in items if item["status"] == status)
                   for status in (EVIDENCED, NOT_EVIDENCED, FOUNDER, UNDETERMINABLE)},
        "statement": ("Evaluation only. This closes nothing and grants no closure "
                      "authority. A satisfied gate is not a closure: closure is a "
                      "Founder decision (FDR-G1 §16, §33)."),
    }


def main() -> int:
    print(json.dumps(evaluate(), indent=2))
    return 0


if __name__ == "__main__":
    # GOAL-V2-004: install the certified-write barrier before anything runs,
    # even when this file is run by path and has not imported `tools`.
    import os, sys  # noqa: E401
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
