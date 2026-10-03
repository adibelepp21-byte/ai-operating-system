"""S-4 verification, in a fresh process, from files alone. READ-ONLY.

Rebuilds both decision chains from the S-4 root, traces them forward (Founder
Goal → … → plan outcome) and backward (agent → … → Founder Goal), runs the
directive's `§15` negative controls (refused before anything is written; the
root and ledgers are hashed before and after), and checks certified history.
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
from tools.escalation_register import LIVE_RESPONSES  # noqa: E402
from tools.planning import AuthorityProvenance, PlanStep  # noqa: E402
from tools.planning.exceptions import InvalidPlan  # noqa: E402
from tools.w4_continuity import operational_overview, operational_state, reconstruct  # noqa: E402
from tools.w4_execution import ExecutionRefused, W4Executor  # noqa: E402
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION  # noqa: E402

ROOT = REPO / "docs/architecture/agency/operations/w4-s4-plan-outcome"
OUT = Path(__file__).with_name("S4-VERIFICATION-2026-10-03.json")
INSTANCE = "engineering-intelligence-instance-001"
FD9 = AuthorityProvenance("FD-P11-001 §9", FD_RECORD)
P12_DIGEST = "5be77e5634d78b237fc7a5ab781c7e0d754f76ccb4e791284349efc0c7a15cf9"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def tree(*roots):
    return {str(p.relative_to(REPO)): sha(p) for r in roots for p in sorted(Path(r).rglob("*"))
            if p.is_file()}


def refused(call, *errors):
    try:
        call()
        return "NOT REFUSED"
    except (w4.DelegationError, TypeError, ExecutionRefused, InvalidPlan) + errors as exc:
        return f"refused: {type(exc).__name__}: {str(exc)[:110]}"


run = json.loads((ROOT / "s4-run.result.json").read_text(encoding="utf-8"))
surface = planning_continuity.restore(ROOT / "planning.state.json")
watched = (ROOT, w4.LIVE_LEDGER, LIVE_RESPONSES)
before = tree(*watched)

chains = {}
for path, entry in run["paths"].items():
    gid = entry["grant"]
    record = json.loads((ROOT / f"{gid}.delegation.json").read_text(encoding="utf-8"))
    evidence = json.loads((REPO / entry["evidence"]).read_text(encoding="utf-8"))
    provenance = w4.plan_provenance(record, surface)
    outcome = w4.plan_outcome(surface, entry["goal"], ROOT)
    first = outcome["versions"][0]
    step = first["steps"][0]
    chains[path] = {
        "forward": {
            "founder_goal": f"{surface.goal(entry['goal']).statement!r} — "
                            f"{provenance['founder_goal']} ({provenance['goal_authority']})",
            "plan": f"{first['plan']} (authority {first['authority']})",
            "plan_step": step["step"],
            "delegation": f"{gid} by {record['delegator']} under {record['authority_instrument']}",
            "agent": f"{record['recipient_instance']} (engineering-intelligence)",
            "execution": [(o["step"], o["status"]) for o in evidence["outcomes"]],
            "result": evidence["outcomes"][0]["detail"],
            "verification": step["grants"][0]["verification"],
            "ceo_decision": step["grants"][0]["decision"],
            "decided_under": step["grants"][0]["decided_under"],
            "plan_outcome": {"current_plan": outcome["current_plan"],
                             "completed": outcome["completed"],
                             "open_steps": outcome["open_steps"]},
        },
        "backward": {"agent": record["recipient_instance"], "delegation": gid,
                     "plan_step": provenance["step"], "plan": provenance["plan"],
                     "goal": provenance["goal"], "founder_goal": provenance["founder_goal"],
                     "faults": provenance["faults"]},
        "outcome_matches_run": json.loads(json.dumps(outcome)) == run["plan_outcomes"][path],
        "outcome": outcome,
    }

# §15 negative controls, against the live root. Each is refused before any write.
accept_gid = run["paths"]["accept"]["grant"]
rework_gid = run["paths"]["rework"]["grant"]
memory = AgentInstanceRegistry(None)
memory.register(instance_key=INSTANCE, definition=SELECTED_DEFINITION,
                permitted_capabilities=("engineering-intelligence",), created_by=w4.AUTHORIZED_DELEGATOR,
                authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
                accountable_to=w4.AUTHORIZED_DELEGATOR)
issuer = w4.W4DelegationRegistry(memory, None)
current_rework = surface.current("founder-s4-rework")
memory_grant = w4.issue_from_plan(
    issuer, surface, current_rework, "report-continuity-elements",
    delegator=w4.AUTHORIZED_DELEGATOR, recipient_instance=INSTANCE, authority=FD9,
    capability_scope=("engineering-intelligence",), resource_boundary="r",
    output_expectation="o", verification_requirement="v", escalation_condition="e")
controls = {
    "N1_agent_cannot_self_accept": refused(lambda: w4.review_result(
        ROOT, accept_gid, surface=surface, decision=w4.ACCEPT, reviewer=INSTANCE, reason="mine")),
    "N2_agent_cannot_record_ceo_acceptance": refused(lambda: w4.record_disposition(
        ROOT, rework_gid, disposition=w4.COMPLETED, delegator=INSTANCE, reason="ceo",
        authority=w4.DELEGATOR_REVIEW)),
    "N3_unverified_result_cannot_be_accepted": run["paths"]["accept"]["accept_without_evidence"],
    "N4_failed_verification_cannot_complete": run["paths"]["rework"]["accept_after_failure"],
    "N4b_failed_result_still_not_acceptable_now": refused(lambda: w4.review_result(
        ROOT, rework_gid, surface=surface, decision=w4.ACCEPT, reviewer=w4.AUTHORIZED_DELEGATOR,
        reason="again")),
    "N5_rework_leaves_the_plan_open": (
        "held" if not chains["rework"]["outcome"]["completed"]
        and chains["rework"]["outcome"]["open_steps"] else "VIOLATED"),
    "N6_scope_cannot_widen": refused(lambda: w4.issue_from_plan(
        issuer, surface, current_rework, "report-continuity-elements",
        delegator=w4.AUTHORIZED_DELEGATOR, recipient_instance=INSTANCE, authority=FD9,
        capability_scope=("engineering-intelligence",), resource_boundary="r",
        output_expectation="o", verification_requirement="v", escalation_condition="e",
        work_scope=("report-continuity-elements", "ceo-review-verification"))),
    "N6b_agent_cannot_execute_the_ceo_step": refused(lambda: W4Executor(
        memory_grant, memory).execute_step(current_rework.step("ceo-review-verification"),
                                           lambda s: "ok")),
    "N7_agent_cannot_issue_a_delegation": refused(lambda: w4.issue_from_plan(
        issuer, surface, current_rework, "report-continuity-elements", delegator=INSTANCE,
        recipient_instance=INSTANCE, authority=FD9, capability_scope=("engineering-intelligence",),
        resource_boundary="r", output_expectation="o", verification_requirement="v",
        escalation_condition="e")),
    "N8_ceo_accept_is_not_founder_accept": (
        "held" if all(c["outcome"]["founder_acceptance"].startswith("NOT RECORDED")
                      for c in chains.values()) else "VIOLATED"),
    "N9_a_decision_cannot_be_redone": refused(lambda: w4.record_disposition(
        ROOT, accept_gid, disposition=w4.REVOKED, delegator=w4.AUTHORIZED_DELEGATOR,
        reason="overwrite the acceptance", authority=w4.DELEGATOR_REVIEW)),
    "N9b_superseded_plan_cannot_be_revised_again": refused(lambda: surface.revise(
        surface.history("founder-s4-rework")[0], steps=(PlanStep("z", "z"),), reason="z")),
}
after = tree(*watched)
controls["root_and_ledgers_unchanged_by_controls"] = before == after

state = {"historical": reconstruct(ROOT), "operational": operational_state(ROOT)}
dispositions, faults = w4.read_dispositions(ROOT)
overview = operational_overview()
p12 = tree(REPO / "docs/architecture/p12")
p12_digest = hashlib.sha256(json.dumps(p12, sort_keys=True, default=str,
                                       ensure_ascii=False).encode()).hexdigest()
git_certified = subprocess.run(
    ["git", "status", "--porcelain", "--", "docs/architecture/p11", "docs/architecture/p12",
     "docs/architecture/p13", "docs/architecture/platform-organization"],
    cwd=REPO, capture_output=True, text=True).stdout.strip() or "(clean)"

result = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": sha(__file__),
    "chains": {k: {x: v[x] for x in ("forward", "backward", "outcome_matches_run")}
               for k, v in chains.items()},
    "plan_outcomes": {k: v["outcome"] for k, v in chains.items()},
    "negative_controls": controls,
    "state": {"historical_active": state["historical"]["active_grants"],
              "operational_active": state["operational"]["active_grants"],
              "dispositions": {k: v["disposition"] for k, v in dispositions.items()},
              "disposition_faults": list(faults),
              "s4_grants_in_current_overview": [g for g in overview["current_grants"]
                                                if g in (accept_gid, rework_gid)],
              "blocking_escalations": overview["blocking_escalations"]},
    "integrity": {"p12_tree_digest": p12_digest, "p12_digest_unchanged": p12_digest == P12_DIGEST,
                  "integrity_faults": [str(f) for f in integrity.verify().faults],
                  "git_status_certified": git_certified},
}
result["all_ok"] = (
    all(c["outcome_matches_run"] and not c["backward"]["faults"]
        and c["backward"]["founder_goal"] == "VERIFIED" for c in chains.values())
    and chains["accept"]["outcome"]["completed"] and not chains["rework"]["outcome"]["completed"]
    and all(str(v).startswith(("refused", "held")) for k, v in controls.items()
            if k != "root_and_ledgers_unchanged_by_controls")
    and controls["root_and_ledgers_unchanged_by_controls"]
    and result["state"]["dispositions"] == {accept_gid: "COMPLETED", rework_gid: "REVOKED"}
    and not faults and result["state"]["operational_active"] == []
    and result["integrity"]["p12_digest_unchanged"] and not result["integrity"]["integrity_faults"]
    and git_certified == "(clean)")
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
print(json.dumps({"chains": result["chains"], "negative_controls": controls,
                  "state": result["state"], "integrity": result["integrity"],
                  "all_ok": result["all_ok"]}, indent=1, ensure_ascii=False, default=str))
