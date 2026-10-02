"""S-2 verification, in a fresh process, from files alone.

Reads the S-2 operational root and the persisted planning state, rebuilds the
grant and traces it to its plan step, runs negative controls against the real
restored plan with **in-memory** registries (nothing is written), and checks
the certified boundary. Writes only its own JSON beside this script.
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

from tools import certified_evidence_integrity as integrity  # noqa: E402
from tools import planning_continuity  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402
from tools.agent_instance_registry import AgentInstanceRegistry  # noqa: E402
from tools.delegation_catalog import operation_roots  # noqa: E402
from tools.p12_certified_evidence_guard import is_protected  # noqa: E402
from tools.planning import AuthorityProvenance  # noqa: E402
from tools.planning.exceptions import InvalidPlan  # noqa: E402
from tools.w4_continuity import reconstruct  # noqa: E402
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION  # noqa: E402

ROOT = REPO / "docs/architecture/agency/operations/w4-s2-plan-delegation"
OUT = Path(__file__).with_name("S2-VERIFICATION-2026-10-03.json")
INSTANCE = "engineering-intelligence-instance-001"
FD9 = AuthorityProvenance("FD-P11-001 §9", FD_RECORD)
TERMS = dict(resource_boundary="r", output_expectation="o",
             verification_requirement="v", escalation_condition="e")


def refused(call):
    try:
        call()
        return "NOT REFUSED"
    except (w4.DelegationError, InvalidPlan, TypeError) as exc:
        return f"refused: {type(exc).__name__}"


state = reconstruct(ROOT)
surface = planning_continuity.restore(ROOT / "planning.state.json")
gid = state["active_grants"][0] if state["active_grants"] else None
record = json.loads((ROOT / f"{gid}.delegation.json").read_text(encoding="utf-8"))
plan = surface.current("agency-s2-ledger-rule-verification")
provenance = w4.plan_provenance(record, surface)

# Negative controls on the real restored plan; in-memory registries only.
memory = AgentInstanceRegistry(None)
memory.register(instance_key=INSTANCE, definition=SELECTED_DEFINITION,
                permitted_capabilities=("engineering-intelligence",),
                created_by=w4.AUTHORIZED_DELEGATOR,
                authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
                accountable_to=w4.AUTHORIZED_DELEGATOR)
issuer = w4.W4DelegationRegistry(memory, None)


def issue(step="verify-ledger-rules", **over):
    kw = dict(delegator=w4.AUTHORIZED_DELEGATOR, recipient_instance=INSTANCE,
              authority=FD9, capability_scope=("engineering-intelligence",), **TERMS)
    kw.update(over)
    return lambda: w4.issue_from_plan(issuer, surface, plan, step, **kw)


before = sorted(p.name for p in ROOT.iterdir())
controls = {
    "agent_cannot_issue": refused(issue(delegator=INSTANCE)),
    "unmarked_step_cannot_be_delegated": refused(issue(step="review-ledger-verification")),
    "caller_cannot_widen_work_scope": refused(issue(work_scope=("verify-ledger-rules",
                                                                 "review-ledger-verification"))),
    "caller_cannot_rename_plan": refused(issue(lifecycle_boundary="one execution of plan x")),
    "caller_cannot_move_accountability": refused(issue(accountable_party=INSTANCE)),
    "capability_beyond_recipient_refused": refused(issue(capability_scope=("governance-artifact-integrity",))),
    "founder_reserved_instrument_refused": refused(issue(authority=AuthorityProvenance(
        "FD-AGENCY-001", "docs/governance/acts/FD-AGENCY-001-FOUNDER-DECISION.md"))),
    "unregistered_recipient_refused": refused(issue(recipient_instance="unregistered-instance")),
}
surface.revise(plan, steps=plan.steps, reason="verification probe (in memory only)")
controls["superseded_plan_refused"] = refused(issue())
controls["root_unchanged_by_controls"] = sorted(p.name for p in ROOT.iterdir()) == before

certified = json.loads((REPO / "docs/governance/AIOS_P11_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json")
                       .read_text(encoding="utf-8"))["files"]
mismatch = [k for k, v in certified.items()
            if hashlib.sha256((REPO / k).read_bytes()).hexdigest() != v]
git_certified = subprocess.run(
    ["git", "status", "--porcelain", "--", "docs/architecture/p11", "docs/architecture/p12",
     "docs/architecture/p13", "docs/architecture/platform-organization"],
    cwd=REPO, capture_output=True, text=True).stdout.strip()

result = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "reconstructed": {k: state[k] for k in ("instances", "active_grants", "revoked_grants",
                                             "open_escalations", "unreadable_records")},
    "grant": {k: record[k] for k in ("delegation_id", "delegator", "recipient_instance",
                                      "authority_instrument", "objective", "capability_scope",
                                      "work_scope", "lifecycle_boundary",
                                      "verification_requirement", "escalation_condition",
                                      "accountable_party", "termination_condition", "status")},
    "plan_provenance": provenance,
    "negative_controls": controls,
    "boundary": {
        "root_protected": is_protected(ROOT),
        "root_in_p11_operation_roots": ROOT in operation_roots(),
        "certified_p11_files_checked": len(certified), "certified_mismatches": mismatch,
        "integrity_faults": [str(f) for f in integrity.verify().faults],
        "git_status_certified_roots": git_certified or "(clean)",
    },
}
result["all_ok"] = (
    state["active_grants"] == [gid] and not state["unreadable_records"]
    and not provenance["faults"] and provenance["step"] == "verify-ledger-rules"
    and all(v.startswith("refused") for k, v in controls.items() if k != "root_unchanged_by_controls")
    and controls["root_unchanged_by_controls"]
    and not result["boundary"]["root_protected"] and not mismatch
    and not result["boundary"]["integrity_faults"] and not git_certified)
OUT.write_text(json.dumps(result, indent=1, default=str) + "\n", encoding="utf-8")
print(json.dumps({"provenance": provenance, "controls": controls,
                  "boundary": result["boundary"], "all_ok": result["all_ok"]}, indent=1, default=str))
