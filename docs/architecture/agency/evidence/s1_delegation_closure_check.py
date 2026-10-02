"""S-1 delegation closure check — read-only over the P11 ledger.

Directive: docs/governance/acts/DIR-AIOS-AGENCY-S1-DELEGATION-CLOSURE.md
(authority FD-AGENCY-001). For each W4 grant still ACTIVE, establish from
persisted records alone:

* whether its own termination condition is met (bound plan completed);
* whether its lifecycle boundary ("one execution of plan ...") is consumed;
* whether a resident closure path can reach it, and with what result.

Nothing under docs/architecture/p11 is written. The certified-evidence guard is
consulted, never bypassed: a refused closure write is proved by the guard's own
refusal, raised before any bytes move. Output: one JSON file beside this script.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

from tools import certified_evidence_integrity as integrity  # noqa: E402
from tools.agent_instance_registry import AgentInstanceRegistry  # noqa: E402
from tools.escalation_register import EscalationRegister  # noqa: E402
from tools.p12_certified_evidence_guard import CertifiedEvidenceProtected, guard  # noqa: E402
from tools.w4_continuity import continuation_conditions, reconstruct  # noqa: E402
from tools.w4_delegation import DelegationError, W4DelegationRegistry  # noqa: E402

P11 = REPO / "docs/architecture/p11"
MANIFEST = REPO / "docs/governance/AIOS_P11_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json"
OUT = Path(__file__).with_name("S1-DELEGATION-CLOSURE-2026-10-02.json")
GRANTS = {
    "4daebea9012d4cc7": ("w1-operations", "w1-coordination.evidence.json"),
    "4313bd2246124a94": ("w4-operations", "first-execution.evidence.json"),
    "0f7ac0785bd8442b": ("x-department-operations", "cross-department.evidence.json"),
    "a437cdbbd29940af": ("x-department-operations", "cross-department.evidence.json"),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(REPO))


certified = json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]
report = integrity.verify()
result = {
    "directive": "docs/governance/acts/DIR-AIOS-AGENCY-S1-DELEGATION-CLOSURE.md",
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": sha(Path(__file__)),
    "certified_evidence_faults": [str(f) for f in report.faults],
    "p11_writes": 0,
    "delegations": {},
}

for gid, (root_name, evidence_name) in GRANTS.items():
    root = P11 / root_name
    path = root / f"{gid}.delegation.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    evidence = json.loads((root / evidence_name).read_text(encoding="utf-8"))
    before = sha(path)

    # The plan the grant was bound to, and what the evidence says happened to it.
    outcomes = evidence["outcomes"]
    own = [o for o in outcomes if o.get("delegation", evidence.get("delegation_id")) == gid
           or (o.get("delegation") is None and o["step"] in record["work_scope"])]
    in_scope = [o for o in own if o["step"] in record["work_scope"]]
    plan_steps = [o["step"] for o in outcomes]
    plan_completed = (bool(outcomes) and all(o["status"] == "success" for o in outcomes)
                      and "SUCCEEDED" in evidence.get("workflow_terminal_state", "SUCCEEDED")
                      and not evidence.get("escalations"))
    scope_done = (sorted(o["step"] for o in in_scope if o["status"] == "success")
                  == sorted(record["work_scope"]))

    # Recipient instance, read from the same root.
    instance = json.loads((root / f"{record['recipient_instance']}.instance.json")
                          .read_text(encoding="utf-8"))

    # Resident closure path 1: W4DelegationRegistry.revoke, from a fresh process.
    # Constructed with no root, so it cannot write anywhere.
    registry = W4DelegationRegistry(AgentInstanceRegistry(None), None)
    try:
        registry.revoke(gid, reason="S-1 probe")
        revoke_path = "REACHED (unexpected)"
    except DelegationError as exc:
        revoke_path = f"UNREACHABLE: {exc}"

    # Resident closure path 2: the persisting rewrite every prior revocation used
    # (`guard(path).write_text(...)`). Only the guard is called; it raises first.
    try:
        guard(path)
        write_path = "PERMITTED (unexpected)"
    except CertifiedEvidenceProtected as exc:
        write_path = f"REFUSED: {type(exc).__name__}"

    after = sha(path)
    result["delegations"][gid] = {
        "root": rel(root),
        "ledger_status": record["status"],
        "issued_at": record["issued_at"],
        "recipient_instance": record["recipient_instance"],
        "instance_lifecycle": instance.get("lifecycle"),
        "authority_record_resolves": (REPO / record["authority_record"]).is_file(),
        "certified_sha256": certified.get(rel(path)),
        "resident_sha256": before,
        "certified_intact": certified.get(rel(path)) == before == after,
        "work_scope": record["work_scope"],
        "plan": evidence.get("plan"),
        "plan_steps": plan_steps,
        "in_scope_outcomes": [(o["step"], o["status"]) for o in in_scope],
        "work_scope_completed": scope_done,
        "plan_completed": plan_completed,
        "termination_condition": record["termination_condition"],
        "termination_by_completion_met": plan_completed,
        "lifecycle_boundary": record["lifecycle_boundary"],
        "lifecycle_consumed_by": evidence.get("executed_at"),
        "plan_escalations": evidence.get("escalations", []),
        "closure_path_revoke": revoke_path,
        "closure_path_persisting_write": write_path,
    }

for root_name in sorted({r for r, _ in GRANTS.values()}):
    state = reconstruct(P11 / root_name)
    result.setdefault("continuity", {})[root_name] = {
        "active_grants": state["active_grants"],
        "open_escalations": list(EscalationRegister(P11 / root_name).open_escalations()),
        "continuation_conditions": list(continuation_conditions(state)),
    }

OUT.write_text(json.dumps(result, indent=1, default=str) + "\n", encoding="utf-8")
print(json.dumps(result, indent=1, default=str))
