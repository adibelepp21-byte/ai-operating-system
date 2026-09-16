"""Independent reader for the escalation→grant join (`W4-GAP-008`/`W2-GAP-007`).

`ACT-CC-P12-W4-001 §24`: *"IMPLEMENTATION → SELF-REPORT → PASS"* is forbidden
— a join only the writer believes in is not a join. Matching
`tools/p12_execution_chain_reader.py`'s own discipline, this module **imports
nothing from `tools/p12_governance_escalation_join.py`**: it reads bytes off
disk and resolves every reference against the record it names, independently.
A conformance control parses this module's imports and fails if that ever
changes.

Two references, both checked: the escalation the join names must actually
exist (resolved through the resident `EscalationRegister`, not by re-parsing
the JSON this reader also wrote — there is no "this reader also wrote"), and
the delegation the join names must resolve to a real, resident grant
(resolved through `tools/p12_provenance_verification.delegation_records`,
the same resident population `tools/p12_failure_verification.escalation_join`
already reads).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

from tools.escalation_register import EscalationRegister, EscalationRegisterError
from tools.p12_provenance_verification import delegation_records

REPO_ROOT = Path(__file__).resolve().parent.parent

JOINED = "JOINED"
DANGLING = "DANGLING"

#: Same sanctioned set the writer declares, re-declared independently. If the
#: two ever diverge, that is a defect worth finding, not one worth hiding
#: behind a shared import.
SANCTIONED_REFUSAL_TYPES = ("ExecutionRefused", "EscalationRequired")


def resolve(join_root: Path, escalation_root: Path, escalation_id: str) -> dict:
    """Independently resolve one join. Never raises for an unresolved join."""
    join_path = join_root / f"{escalation_id}.governance-join.json"
    if not join_path.is_file():
        return {"escalation_id": escalation_id, "status": DANGLING,
                 "reason": "no join record"}

    try:
        join = json.loads(join_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return {"escalation_id": escalation_id, "status": DANGLING,
                 "reason": f"unreadable join: {exc}"}

    if join.get("escalation_id") != escalation_id:
        return {"escalation_id": escalation_id, "status": DANGLING,
                 "reason": "join names a different escalation than the file "
                           "it is beside"}

    # Reference one: the escalation actually exists, resolved through the
    # register that owns it — not by trusting the join's own claim.
    register = EscalationRegister(escalation_root)
    try:
        register.load(escalation_id)
    except EscalationRegisterError:
        return {"escalation_id": escalation_id, "status": DANGLING,
                 "reason": "join names an escalation the register does not "
                           "hold"}

    # Reference two: the delegation resolves to a real, resident grant.
    delegation_id = join.get("delegation_id")
    known = {d["delegation_id"] for d in delegation_records()}
    if delegation_id not in known:
        return {"escalation_id": escalation_id, "status": DANGLING,
                 "reason": f"delegation {delegation_id!r} does not resolve "
                           "to a real grant"}

    refusal_type = join.get("refusal_type")
    if refusal_type not in SANCTIONED_REFUSAL_TYPES:
        return {"escalation_id": escalation_id, "status": DANGLING,
                 "reason": f"refusal_type {refusal_type!r} is not a "
                           "sanctioned refusal"}

    return {"escalation_id": escalation_id, "status": JOINED,
             "delegation_id": delegation_id, "refusal_type": refusal_type}


def resolve_all(join_root: Path, escalation_root: Path) -> Tuple[dict, ...]:
    """Resolve every join file present. Population is what is on disk."""
    ids = sorted(p.name.split(".")[0]
                 for p in join_root.glob("*.governance-join.json"))
    return tuple(resolve(join_root, escalation_root, i) for i in ids)
