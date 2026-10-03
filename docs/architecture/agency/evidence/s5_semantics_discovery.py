"""S-5 disposition-semantics discovery. READ-ONLY EVIDENCE TOOL.

Directive: docs/governance/acts/DIR-AIOS-AGENCY-S5-DISPOSITION-SEMANTICS-DISCOVERY.md.

It reads the resident state vocabularies from the modules themselves, tries to
reconstruct every recorded delegator decision **without reading any reason
text**, demonstrates (in memory only) whether REWORK and refusal-without-rework
can be told apart from structure, traces provenance both ways, measures how much
of "why is this step in this state?" is structural, and runs the directive's
`§18` negative controls. Every operational and certified byte is hashed before
and after; the only file written is this tool's JSON output.
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

import tools  # noqa: E402,F401  -- installs the certified-write barrier before anything runs

OUT = Path(__file__).with_name("S5-SEMANTICS-DISCOVERY-2026-10-03.json")
WATCHED = ("docs/architecture/agency/operations", "docs/architecture/p11",
           "docs/architecture/p12", "docs/operations")
S4_ROOT = REPO / "docs/architecture/agency/operations/w4-s4-plan-outcome"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def snapshot():
    return {str(p.relative_to(REPO)): sha(p) for w in WATCHED
            for p in sorted((REPO / w).rglob("*")) if p.is_file()}


BEFORE = snapshot()

from native_core.core.governance import decision as native_decision  # noqa: E402
from native_core.core.workflow.lifecycle import WorkflowState  # noqa: E402
from tools import agent_instance_registry as air  # noqa: E402
from tools import certified_evidence_integrity as integrity  # noqa: E402
from tools import planning_continuity  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402
from tools import w4_execution as w4x  # noqa: E402
from tools.delegation_catalog import all_operation_roots  # noqa: E402
from tools.escalation_register import LIVE_RESPONSES, EscalationRegister  # noqa: E402
from tools.p12_failure_verification import FAILURE_STATES  # noqa: E402
from tools.planning import Plan, PlanningSurface, PlanStep  # noqa: E402
from tools.planning import AuthorityProvenance, Goal  # noqa: E402
from tools.planning.interfaces import AdaptationClass  # noqa: E402
from tools.planning.plan import PlanOrigin  # noqa: E402
from tools.w4_continuity import operational_overview  # noqa: E402

# ── A. Semantic inventory, read from the modules ─────────────────────────────
inventory = {
    "delegation_record_status": [w4.ACTIVE, w4.REVOKED],
    "operational_disposition": list(w4.DISPOSITIONS),
    "disposition_instruments": [a[0] for a in w4.DISPOSITION_SCOPES],
    "execution_outcome_status": [w4x.SUCCESS, w4x.FAILURE, w4x.ESCALATION],
    "instance_lifecycle": [air.REGISTERED, air.RETIRED],
    "escalation_state": ["OPEN", "ANSWERED"],
    "plan_origin": [o.name for o in PlanOrigin],
    "adaptation_class": [a.name for a in AdaptationClass],
    "planning_surface_operations": sorted(n for n in dir(PlanningSurface)
                                          if not n.startswith("_")),
    "workflow_state": [s.name for s in WorkflowState],
    "native_review_decision": sorted(native_decision.VALID_DECISIONS),
    "p12_s33_failure_states_measured": list(FAILURE_STATES),
    "s4_review_decisions": [w4.ACCEPT, w4.REWORK],
}
absent = {term: not any(term.lower() in op.lower() for op in inventory["planning_surface_operations"])
          for term in ("abandon", "close", "cancel", "terminate", "drop", "reject", "complete")}

# ── C/D. Reconstruct every recorded decision without reading reason text ────
surfaces = {}
for root in all_operation_roots():
    state = root / "planning.state.json"
    if state.is_file():
        surfaces[root] = planning_continuity.restore(state)


def plan_on_surfaces(plan_key):
    for root, surface in surfaces.items():
        for goal in surface._goals:  # noqa: SLF001 - read-only
            for plan in surface.history(goal):
                if plan.key == plan_key:
                    return root, surface, plan
    return None, None, None


decisions = []
for root in all_operation_roots():
    valid, faults = w4.read_dispositions(root)
    for gid, item in sorted(valid.items()):
        record = json.loads((root / f"{gid}.delegation.json").read_text(encoding="utf-8"))
        met, evidence, _ = w4.plan_completion(root, record)
        plan_key = w4._bound_plan(record)
        _, surface, plan = plan_on_surfaces(plan_key)
        superseded = bool(surface and surface.is_superseded(plan))
        successor = None
        if superseded:
            chain = surface.history(plan.goal_key)
            successor = chain[[p.key for p in chain].index(plan.key) + 1]
        structural = {
            "disposition": item["disposition"], "verification_met": met,
            "plan_on_a_surface": plan is not None, "plan_superseded": superseded,
            "successor_keeps_step_key": (record["work_scope"][0] in [s.key for s in successor.steps]
                                         if successor else None),
            "decided_under": item.get("authority_instrument")}
        if item["disposition"] == w4.COMPLETED:
            reading = "COMPLETED: verified completion recorded by the delegator (≡ ACCEPT)"
        elif superseded:
            reading = "REVOKED + bound plan revised (REWORK or refusal — not distinguishable)"
        elif plan is not None:
            reading = "REVOKED, plan unrevised (withdrawal; step left unresolved)"
        else:
            reading = "REVOKED, plan on no surface (withdrawal of historical grant)"
        text = item.get("reason", "")
        label = text.split()[1] if text.startswith("CEO ") else "(no decision word)"
        decisions.append({"root": str(root.relative_to(REPO)), "grant": gid,
                          "structural": structural, "text_free_reading": reading,
                          "decision_word_in_reason": label})

# ── E. REWORK vs refusal-without-rework: structure alone (in memory only) ───
CEO = AuthorityProvenance("Co-Founder V2 A01 Executive Command",
                          "docs/governance/AIOS_COFOUNDER_V2_REGISTRATION_AND_ACTIVATION_RECORD_v1.0.md")


def scenario(successor_steps):
    surface = PlanningSurface()
    surface.declare(Goal("g", "goal", CEO))
    p0 = surface.adopt(Plan(key="g-plan-0", goal_key="g", authority=CEO, steps=(
        PlanStep("a", "Establish X.", requires_delegation=True),
        PlanStep("b", "Establish Y.", requires_delegation=True))))
    p1 = surface.revise(p0, steps=successor_steps, reason="decision")
    keys0 = {s.key for s in p0.steps if s.requires_delegation}
    keys1 = {s.key for s in p1.steps if s.requires_delegation}
    return {"superseded": surface.is_superseded(p0), "kept": sorted(keys0 & keys1),
            "dropped": sorted(keys0 - keys1), "added": sorted(keys1 - keys0)}


ambiguity = {
    "rework_same_key": scenario((PlanStep("a", "Establish X again.", requires_delegation=True),
                                 PlanStep("b", "Establish Y.", requires_delegation=True))),
    "rework_new_key": scenario((PlanStep("a-redo", "Establish X, corrected.", requires_delegation=True),
                                PlanStep("b", "Establish Y.", requires_delegation=True))),
    "refusal_with_replacement_work": scenario((PlanStep("c", "Establish Z instead.",
                                                        requires_delegation=True),
                                               PlanStep("b", "Establish Y.", requires_delegation=True))),
    "refusal_drop_only": scenario((PlanStep("b", "Establish Y.", requires_delegation=True),)),
}


def shape(view):
    """What the plan contract itself can say: step keys carry no lineage across
    versions, so a new key's name means nothing structurally."""
    return (view["superseded"], tuple(view["kept"]), tuple(view["dropped"]), len(view["added"]))


ambiguity["rework_new_key_vs_refusal_with_replacement_identical_up_to_names"] = (
    shape(ambiguity["rework_new_key"]) == shape(ambiguity["refusal_with_replacement_work"]))
ambiguity["rework_same_key_distinguishable_from_drop"] = (
    shape(ambiguity["rework_same_key"]) != shape(ambiguity["refusal_drop_only"]))
ambiguity["same_key_means_redo_is_a_contract_rule"] = False  # no such rule in tools/planning

# ── G. Provenance, forward and reverse, on the S-4 root (existing readers) ──
s4 = surfaces[S4_ROOT]
provenance = {}
for goal_key in ("founder-s4-accept", "founder-s4-rework"):
    outcome = w4.plan_outcome(s4, goal_key, S4_ROOT)
    reverse = []
    for version in reversed(outcome["versions"]):
        for step in version["steps"]:
            for grant in step.get("grants", []):
                record = json.loads((S4_ROOT / f"{grant['delegation_id']}.delegation.json")
                                    .read_text(encoding="utf-8"))
                prov = w4.plan_provenance(record, s4)
                reverse.append({"plan_outcome": f"{outcome['current_plan']} completed="
                                                f"{outcome['completed']}",
                                "decision": grant["operational_status"],
                                "verification": grant["verification"],
                                "result_evidence": grant["evidence"],
                                "agent": record["recipient_instance"],
                                "delegation": grant["delegation_id"],
                                "plan": prov["plan"], "goal": prov["goal"],
                                "founder_goal": prov["founder_goal"], "faults": prov["faults"]})
    open_steps = [s for s in outcome["versions"][-1]["steps"] if not s["done"]]
    provenance[goal_key] = {
        "reverse_from_outcome": reverse,
        "open_steps": [s["step"] for s in open_steps],
        "open_step_to_failed_step_link": (
            "structural: plan supersedes → predecessor plan → its revoked grant; "
            "which predecessor step the open step replaces: reason text only"
            if open_steps and len(outcome["versions"]) > 1 else None)}

# ── H. Observability: why is each step in its state? ────────────────────────
observability = []
for goal_key in ("founder-s4-accept", "founder-s4-rework"):
    outcome = w4.plan_outcome(s4, goal_key, S4_ROOT)
    for version in outcome["versions"]:
        for step in version["steps"]:
            structural, textual = [], []
            structural.append(f"done={step['done']}")
            if step["performed_by"] == "CEO":
                structural.append(f"depends_on={step['depends_on']} (decided ⇒ done)")
            else:
                structural.append(f"outcome={step['outcome']}")
                for g in step["grants"]:
                    structural += [f"grant {g['delegation_id']} {g['operational_status']}",
                                   f"verification={'met' if g['verification'] == 'met' else 'not met (computed reasons)'}",
                                   f"evidence={g['evidence']}", f"decided_under={g['decided_under']}"]
                    if g["decision"]:
                        textual.append("decision word and rationale (disposition reason)")
            if version["superseded_by"]:
                structural.append(f"plan superseded_by={version['superseded_by']}")
            if version["reason"]:
                textual.append("why the plan was revised (plan reason, plan evidence strings)")
            observability.append({"goal": goal_key, "plan": version["plan"], "step": step["step"],
                                  "structural": structural, "textual_only": textual})

# ── J. Negative controls (§18): each refused before any write ───────────────
accept_gid, rework_gid = "4ff84423cadc48c8", "9925366405d44af8"
AGENT = "engineering-intelligence-instance-001"


def refused(call):
    try:
        call()
        return "NOT REFUSED"
    except Exception as exc:  # recorded, not hidden
        return f"refused: {type(exc).__name__}: {str(exc)[:100]}"


controls = {
    "N1_agent_cannot_create_review_authority": refused(lambda: w4.record_disposition(
        S4_ROOT, accept_gid, disposition=w4.REVOKED, delegator=w4.AUTHORIZED_DELEGATOR,
        reason="x", authority=("AGENT REVIEW AUTHORITY", "docs/x.md"))),
    "N2_agent_cannot_self_accept": refused(lambda: w4.review_result(
        S4_ROOT, accept_gid, surface=s4, decision=w4.ACCEPT, reviewer=AGENT, reason="mine")),
    "N3_agent_cannot_self_reject": refused(lambda: w4.review_result(
        S4_ROOT, rework_gid, surface=s4, decision="REJECT", reviewer=AGENT, reason="mine")),
    "N4_ceo_accept_is_not_founder_approve":
        "held" if w4.plan_outcome(s4, "founder-s4-accept", S4_ROOT)["founder_acceptance"]
        .startswith("NOT RECORDED") else "VIOLATED",
    "N5_failed_verification_cannot_complete": refused(lambda: w4.record_disposition(
        S4_ROOT, rework_gid, disposition=w4.COMPLETED, delegator=w4.AUTHORIZED_DELEGATOR,
        reason="x", authority=w4.DELEGATOR_REVIEW)),
    "N6_revision_keeps_history":
        "held" if [p.key for p in s4.history("founder-s4-rework")][0] == "founder-s4-rework-plan-0"
        and s4.is_superseded(s4.history("founder-s4-rework")[0]) else "VIOLATED",
    "N7_reading_does_not_make_history_current":
        "held" if not ({"2494015de36246fd", accept_gid, rework_gid}
                       & set(operational_overview()["current_grants"])) else "VIOLATED",
    "N8_escalation_is_not_authorization":
        "held" if EscalationRegister(REPO / "docs/architecture/p12/w4-operations", LIVE_RESPONSES)
        .status("9cb90fa0787a478c") == "ANSWERED"
        and w4.read_dispositions(REPO / "docs/architecture/p12/w4-operations")[0]
        ["2494015de36246fd"]["disposition"] == w4.REVOKED else "VIOLATED",
}
AFTER = snapshot()
controls["N9_N10_no_operational_or_certified_byte_changed"] = BEFORE == AFTER
git_certified = subprocess.run(
    ["git", "status", "--porcelain", "--", "docs/architecture/p11", "docs/architecture/p12",
     "docs/architecture/p13", "docs/architecture/platform-organization"],
    cwd=REPO, capture_output=True, text=True).stdout.strip() or "(clean)"

result = {
    "tool": "READ-ONLY EVIDENCE TOOL — S-5",
    "collected_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": sha(__file__),
    "head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True,
                           text=True).stdout.strip(),
    "A_inventory": inventory, "A_planning_operations_absent": absent,
    "C_D_decisions": decisions,
    "E_rework_vs_refusal": ambiguity,
    "G_provenance": provenance,
    "H_observability": observability,
    "J_negative_controls": controls,
    "integrity": {"files_hashed": len(BEFORE), "unchanged": BEFORE == AFTER,
                  "integrity_faults": [str(f) for f in integrity.verify().faults],
                  "git_status_certified": git_certified},
}
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
print(json.dumps({k: result[k] for k in ("A_planning_operations_absent", "E_rework_vs_refusal",
                                          "J_negative_controls", "integrity")},
                 indent=1, ensure_ascii=False))
print(json.dumps([(d["grant"], d["structural"]["disposition"], d["text_free_reading"][:40],
                   d["decision_word_in_reason"]) for d in decisions], ensure_ascii=False))
