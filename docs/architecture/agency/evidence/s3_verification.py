"""S-3 verification, in a fresh process, from files alone.

Rebuilds Founder Goal → plan → requirement → delegation → agent from the S-3
operational root, answers "why does this agent have this work?", runs the
directive's `§12` negative controls with in-memory registries (nothing is
written), and checks the S-1, S-2 and certified state is untouched.
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

from tools import authority_citation as ac  # noqa: E402
from tools import certified_evidence_integrity as integrity  # noqa: E402
from tools import planning_continuity  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402
from tools.agent_instance_registry import AgentInstanceRegistry  # noqa: E402
from tools.delegation_catalog import operation_roots  # noqa: E402
from tools.planning import AuthorityProvenance, Goal  # noqa: E402
from tools.planning.exceptions import InvalidPlan  # noqa: E402
from tools.w4_continuity import operational_state, reconstruct  # noqa: E402
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION  # noqa: E402

ROOT = REPO / "docs/architecture/agency/operations/w4-s3-founder-goal"
S2_ROOT = REPO / "docs/architecture/agency/operations/w4-s2-plan-delegation"
OUT = Path(__file__).with_name("S3-VERIFICATION-2026-10-03.json")
S3_ID = "DIR-AIOS-AGENCY-S3-FOUNDER-GOAL-TO-PLANNING"
S3_RECORD = f"docs/governance/acts/{S3_ID}.md"
GOAL = "founder-s3-connect-goal-to-planning"
INSTANCE = "engineering-intelligence-instance-001"
FD9 = AuthorityProvenance("FD-P11-001 §9", FD_RECORD)
TERMS = dict(resource_boundary="r", output_expectation="o",
             verification_requirement="v", escalation_condition="e")


def refused(call, *errors):
    try:
        call()
        return "NOT REFUSED"
    except (w4.DelegationError, InvalidPlan, TypeError, NotImplementedError) + errors as exc:
        return f"refused: {type(exc).__name__}"


# Rebuild.
state = reconstruct(ROOT)
surface = planning_continuity.restore(ROOT / "planning.state.json")
gid = state["active_grants"][0]
record = json.loads((ROOT / f"{gid}.delegation.json").read_text(encoding="utf-8"))
instance = json.loads((ROOT / f"{INSTANCE}.instance.json").read_text(encoding="utf-8"))
run = json.loads((ROOT / "s3-run.result.json").read_text(encoding="utf-8"))
goal = surface.goal(GOAL)
plan = surface.current(GOAL)
provenance = w4.plan_provenance(record, surface)
requirement = {r.step_key: r for r in surface.delegation_requirements(plan)}

why = {
    "agent": record["recipient_instance"],
    "agent_definition": f"{instance['definition_key']} v{instance['definition_version']} "
                        f"(department {instance['owning_department']})",
    "work": record["work_scope"], "delegation": record["delegation_id"],
    "delegator": record["delegator"], "delegation_authority": record["authority_instrument"],
    "plan_step": provenance["step"],
    "delegation_requirement": [requirement[k].step_key for k in requirement],
    "plan": provenance["plan"], "plan_authority": provenance["plan_authority"],
    "goal": provenance["goal"], "goal_statement": provenance["goal_statement"],
    "goal_authority": provenance["goal_authority"], "founder_goal": provenance["founder_goal"],
}

# Negative controls (directive §12), in memory only.
memory = AgentInstanceRegistry(None)
memory.register(instance_key=INSTANCE, definition=SELECTED_DEFINITION,
                permitted_capabilities=("engineering-intelligence",),
                created_by=w4.AUTHORIZED_DELEGATOR,
                authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
                accountable_to=w4.AUTHORIZED_DELEGATOR)
issuer = w4.W4DelegationRegistry(memory, None)


def issue(**over):
    kw = dict(delegator=w4.AUTHORIZED_DELEGATOR, recipient_instance=INSTANCE, authority=FD9,
              capability_scope=("engineering-intelligence",), **TERMS)
    kw.update(over)
    return lambda: w4.issue_from_plan(issuer, surface, plan, "verify-founder-goal-intake", **kw)


def founder_goal_from(record_path, statement, instrument=None):
    def call():
        reason = ac.founder_goal_refusal(instrument or Path(record_path).stem, record_path, statement)
        if reason:
            raise w4.DelegationError(reason)
    return call


before = sorted(p.name for p in ROOT.iterdir())
controls = {
    "1_agent_cannot_create_founder_goal": refused(founder_goal_from(
        "docs/architecture/agency/operations/w4-s3-founder-goal/s3-run.result.json", "x")),
    "2_agent_cannot_convert_goal_to_delegation": refused(issue(delegator=INSTANCE)),
    "3_planning_cannot_issue": refused(lambda: requirement["verify-founder-goal-intake"]
                                       .as_delegation_record()),
    "5_candidate_name_cannot_create_instance_or_receive": refused(issue(recipient_instance="usopp")),
    "6_candidate_label_cannot_exercise_authority": refused(issue(delegator="Monkey D. Luffy")),
    "7_caller_cannot_alter_founder_intent": refused(founder_goal_from(
        S3_RECORD, "S-3 — Activate the ten Executive Agents", S3_ID)),
    "7b_goal_cannot_be_redeclared": refused(lambda: surface.declare(Goal(
        key=GOAL, statement="Something else.", authority=AuthorityProvenance(S3_ID, S3_RECORD)))),
    "8_caller_cannot_widen_scope": refused(issue(work_scope=("verify-founder-goal-intake",
                                                             "report-to-founder"))),
    "9_candidate_without_instance_not_active": refused(issue(recipient_instance="franky")),
    "10_founder_reserved_not_delegation_authority": refused(issue(
        authority=AuthorityProvenance(S3_ID, S3_RECORD))),
}
surface.revise(plan, steps=plan.steps, reason="verification probe (in memory only)")
controls["4_non_current_plan_cannot_issue"] = refused(issue())
controls["root_unchanged_by_controls"] = sorted(p.name for p in ROOT.iterdir()) == before

# No candidate became an agent anywhere.
candidates = [c["candidate"] for c in run["candidate_map"]]
all_instances = sorted(p.name for p in REPO.glob("docs/**/*.instance.json"))
tokens = {part for c in candidates for part in c.lower().split() if len(part) > 3}
named = [i for i in all_instances if any(t in i for t in tokens)]

certified = json.loads((REPO / "docs/governance/AIOS_P11_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json")
                       .read_text(encoding="utf-8"))["files"]
mismatch = [k for k, v in certified.items()
            if hashlib.sha256((REPO / k).read_bytes()).hexdigest() != v]


def git(*paths):
    return subprocess.run(["git", "status", "--porcelain", "--", *paths], cwd=REPO,
                          capture_output=True, text=True).stdout.strip()


s2 = reconstruct(S2_ROOT)
s1 = {r: operational_state(REPO / "docs/architecture/p11" / r)["operational_dispositions"]
      for r in ("w1-operations", "w4-operations", "x-department-operations")}

result = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "reconstructed": {"instances": state["instances"], "active_grants": state["active_grants"],
                      "unreadable": state["unreadable_records"],
                      "goal": {"key": goal.key, "statement": goal.statement,
                               "authority": goal.authority.cited()},
                      "plan": {"key": plan.key, "authority": plan.authority.cited(),
                               "goal_key": plan.goal_key},
                      "executive_target": run["executive_target"]},
    "why_does_this_agent_have_this_work": why,
    "negative_controls": controls,
    "candidates": {"instances_named_after_candidates": named,
                   "all_instance_records": all_instances,
                   "map": [{k: c[k] for k in ("candidate", "function", "instance_status",
                                                 "resident_capability")} for c in run["candidate_map"]]},
    "unchanged": {
        "s2_root_active": s2["active_grants"],
        "s1_dispositions": s1,
        "certified_p11_mismatches": mismatch,
        "integrity_faults": [str(f) for f in integrity.verify().faults],
        "git_certified_roots": git("docs/architecture/p11", "docs/architecture/p12",
                                   "docs/architecture/p13", "docs/architecture/platform-organization")
        or "(clean)",
        "s3_root_in_p11_operation_roots": ROOT in operation_roots(),
    },
}
result["all_ok"] = (
    state["active_grants"] == [gid] and not state["unreadable_records"]
    and provenance["founder_goal"] == "VERIFIED" and not provenance["faults"]
    and goal.authority != plan.authority
    and all(v.startswith("refused") for k, v in controls.items() if k != "root_unchanged_by_controls")
    and controls["root_unchanged_by_controls"] and not named
    and s2["active_grants"] == ["0a697039a63f4c17"]
    and s1 == {"w1-operations": {"4daebea9012d4cc7": "COMPLETED"},
               "w4-operations": {"4313bd2246124a94": "REVOKED"},
               "x-department-operations": {"0f7ac0785bd8442b": "COMPLETED",
                                           "a437cdbbd29940af": "COMPLETED"}}
    and not mismatch and not result["unchanged"]["integrity_faults"]
    and result["unchanged"]["git_certified_roots"] == "(clean)")
OUT.write_text(json.dumps(result, indent=1, default=str) + "\n", encoding="utf-8")
print(json.dumps({"why": why, "controls": controls,
                  "named_after_candidates": named, "all_ok": result["all_ok"]}, indent=1))
