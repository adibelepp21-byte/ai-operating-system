"""S-6 systemic Agency integration frontier discovery. READ-ONLY EVIDENCE TOOL.

Directive: docs/governance/acts/DIR-AIOS-AGENCY-S6-SYSTEMIC-INTEGRATION-FRONTIER-DISCOVERY.md.

Rebuilds, from files alone and in a fresh process, every fact the S-6 record
classifies:

* the Agency chain as it stands (goals, plans, grants, decisions, outcomes) in
  every operational root and on every persisted planning surface;
* each boundary's evidence: Execution ↔ Runtime / Trace, State ↔ Observability,
  Observability ↔ Re-discovery (P13), Organization ↔ Delegation (W3);
* whether the three FD-AGENCY-001 `§5` surface items never started (P13 reads
  work state; unified view; resident runtime binding) have any resident code;
* the negative controls N1–N12, run in memory through the lawful interfaces;
* the integrity comparison against ``S6-BASELINE-2026-10-03.json``.

Writes only ``S6-FRONTIER-DISCOVERY-2026-10-03.json``. Every surface it reads is
hashed before and after the run; the comparison is part of the result.
"""
import hashlib
import importlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

import tools  # noqa: E402,F401  -- installs the certified-write barrier before anything runs

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import s6_baseline as base  # noqa: E402

OUT = HERE / "S6-FRONTIER-DISCOVERY-2026-10-03.json"
BASELINE = json.loads((HERE / "S6-BASELINE-2026-10-03.json").read_text(encoding="utf-8"))
AGENCY_OPS = REPO / "docs/architecture/agency/operations"

from tools import planning_continuity  # noqa: E402
from tools import w4_continuity  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402
from tools.p12_certified_evidence_guard import is_protected  # noqa: E402


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True).stdout.strip()


def rel(p):
    return str(Path(p).relative_to(REPO))


def code_files(where="tools"):
    return [p for p in sorted((REPO / where).rglob("*.py"))
            if "tests" not in p.parts and "__pycache__" not in p.parts]


def references(needles, where="tools", exclude=()):
    """Resident modules (tests excluded) whose source names any needle."""
    hits = {}
    for p in code_files(where):
        if rel(p) in exclude or p == Path(__file__).resolve():
            continue                      # this tool names every needle it looks for
        text = p.read_text(encoding="utf-8")
        found = sorted(n for n in needles if n in text)
        if found:
            hits[rel(p)] = found
    return hits


before = base.surfaces()
register_before = base.register_state()


# ── A/B. The chain as it stands, from files ──────────────────────────────────
def chain():
    overview = w4_continuity.operational_overview()
    surfaces = {}
    for state in sorted(REPO.glob("docs/**/planning.state.json")):
        root = state.parent
        surface = planning_continuity.restore(state)
        goals = {}
        for key in sorted(surface._goals):                              # noqa: SLF001
            goal = surface.goal(key)
            out = w4.plan_outcome(surface, key, root)
            goals[key] = {
                "authority": goal.authority.instrument,
                "plans": [p["plan"] for p in out["versions"]],
                "current_plan": out["current_plan"], "completed": out["completed"],
                "open_steps": out["open_steps"], "decision_faults": out["decision_faults"],
                "founder_acceptance": out["founder_acceptance"],
                "grants": sorted({g["delegation_id"] for v in out["versions"]
                                  for s in v["steps"] for g in s.get("grants", [])}),
            }
        surfaces[rel(state)] = {"certified": is_protected(state), "goals": goals}
    decisions = {"explicit": 0, "legacy": 0}
    from tools.delegation_catalog import all_operation_roots
    for root in all_operation_roots():
        valid, _ = w4.read_dispositions(root)
        for item in valid.values():
            _, prov = w4._decision_of({k: v for k, v in item.items() if k != "reason"})  # noqa: SLF001
            decisions["explicit" if prov == "EXPLICIT" else "legacy"] += 1
    return overview, surfaces, decisions


overview, surfaces, decisions = chain()
current = overview["current_grants"]
open_goals = {f"{s}::{g}": v["open_steps"] for s, d in surfaces.items()
              for g, v in d["goals"].items() if not v["completed"]}
grants_on_open_goals = {k: sorted(set(surfaces[k.split("::")[0]]["goals"][k.split("::")[1]]["grants"]))
                        for k in open_goals}
pending_not_flagged = {
    r: info["conditions"] for r, info in overview["roots"].items()
    if info["operational_active"] and info["conditions"] == [
        "NO BLOCKING CONDITION — prior state is coherent"]}


# ── F. Execution ↔ Runtime / Trace ───────────────────────────────────────────
agency_evidence = sorted(AGENCY_OPS.glob("*/*.evidence.json"))
evidence_keys = sorted({k for p in agency_evidence
                        for k in json.loads(p.read_text(encoding="utf-8"))})
agency_grants = sorted({p.name.split(".")[0] for p in AGENCY_OPS.glob("*/*.delegation.json")})
trace_and_observation_roots = [REPO / "docs/architecture/p12/trace-stores",
                               REPO / "docs/operations/runtime-observations",
                               REPO / "docs/operations/p13"]
seen_in_trace = {}
for root in trace_and_observation_roots:
    for p in sorted(root.rglob("*")):
        if p.is_file():
            data = p.read_bytes()
            for gid in agency_grants:
                if gid.encode() in data:
                    seen_in_trace.setdefault(gid, []).append(rel(p))
w4_executor_callers = references(["W4Executor("], where=".", exclude=("tools/w4_execution.py",))
runtime_in_callers = {f: bool(references(["create_execution_layer", "participate(",
                                          "WorkflowParticipatingAgent"], where=".").get(f))
                      for f in w4_executor_callers}
eng_agent = (REPO / "consumers/engineering_intelligence_agent.py").read_text(encoding="utf-8")
runtime_trace = {
    "agency_evidence_records": len(agency_evidence),
    "agency_evidence_keys": evidence_keys,
    "agency_evidence_carries_runtime_or_trace": any(
        k for k in evidence_keys if "runtime" in k or "trace" in k),
    "agency_grants": len(agency_grants),
    "agency_grants_in_any_trace_observation_or_p13_record": seen_in_trace,
    "trace_store_root_certified": is_protected(REPO / "docs/architecture/p12/trace-stores/x"),
    "w4_executor_callers_using_runtime": runtime_in_callers,
    "resident_binder_w4_to_execution_layer": references(
        ["create_execution_layer"], exclude=("tools/p12_knowledge_admission_verifier.py",)),
    "trace_identity_in_participate": (
        'agent_instance="engineering-intelligence-agent"' in eng_agent),
}


# ── H/J. Observability and executive re-discovery (P13) ──────────────────────
from tools.p13.state import SOURCES  # noqa: E402
from tools import p12_self_model  # noqa: E402
p13_source_text = (REPO / "tools/p13/state.py").read_text(encoding="utf-8")
cycles = sorted((REPO / "docs/operations/p13/cycles").glob("*.json"))
self_model_open = sorted(p12_self_model.incomplete(REPO).value["open_escalations"])
operational_open = sorted(e["escalation_id"] for e in overview["escalations"].values()
                          if e["operational_state"] == "OPEN")
p13 = {
    "sources": [s.name for s in SOURCES],
    "source_reads_agency_state": {n: n in p13_source_text for n in (
        "w4_continuity", "w4_delegation", "plan_outcome", "operational_overview",
        "planning_continuity", "read_dispositions")},
    "cycles": len(cycles), "latest_cycle": cycles[-1].name if cycles else None,
    "escalations_open_executive_view": self_model_open,
    "escalations_open_operational_view": operational_open,
    "escalations_blocking_operational_view": overview["blocking_escalations"],
    "issue_delegation_reserved": "issue.delegation" in __import__(
        "tools.p13.catalog", fromlist=["RESERVED"]).RESERVED,
}
readers = {
    "planning_surface_discovery_in_tools": references(["planning.state.json"]),
    "plan_outcome_callers_in_tools": references(["plan_outcome("],
                                                exclude=("tools/w4_delegation.py",)),
    "operational_overview_callers_in_tools": references(
        ["operational_overview("], exclude=("tools/w4_continuity.py",)),
}

# ── G/H. The canonical Unified Operational State (P12-W2) against operations ──
# Read as data, by name (the disclosed pattern of `tools/p12_operational_state_verifier.py`):
# an evidence tool measures the surface and is not one of its consumers, so it must
# not enter the P12 consumer measurement (`p12_state_verification.consumers_of`).
w2 = importlib.import_module("tools.p12_operational_state")
from tools import p12_provenance_verification as prov  # noqa: E402
w2_entries = {e.state_id: e for e in w2.project()}
w2_delegation = w2_entries["delegation.granted"]
operational_active = sorted(g["delegation_id"] for g in overview["grants"].values()
                            if g["operational_status"] == "ACTIVE")
canonical_state = {
    "delegation_granted": {"status": w2_delegation.status, "value": w2_delegation.value,
                           "source": w2_delegation.source},
    "delegation_roots_read": [rel(r) for r in prov.DELEGATION_ROOTS],
    "agency_roots_read": any("agency" in rel(r) for r in prov.DELEGATION_ROOTS),
    "operational_active": operational_active,
    "operational_active_visible_to_canonical": [
        g for g in operational_active
        if any((r / f"{g}.delegation.json").is_file() for r in prov.DELEGATION_ROOTS)],
    "canonical_reads_live_ledger": "LIVE_LEDGER" in (
        REPO / "tools/p12_operational_state.py").read_text(encoding="utf-8")
    or "read_dispositions" in (REPO / "tools/p12_operational_state.py").read_text(encoding="utf-8"),
    "consumers": sorted(references(["p12_operational_state"],
                                   exclude=("tools/p12_operational_state.py",))),
}

# ── E/K. Organization ↔ Delegation (W3) ──────────────────────────────────────
from tools import delegation_reconciliation as w3  # noqa: E402
operational_status = {g["delegation_id"]: g["operational_status"]
                      for g in overview["grants"].values()}
w3_report = w3.reconcile()
projected_current = sorted(p.grant_id for p in w3_report["projections"] if p.role == "CURRENT")
w3_view = {
    "roots_read": [rel(r) for r in w3.LEDGER_ROOTS],
    "projected_current": {g: operational_status.get(g) for g in projected_current},
    "current_grants_not_projected": [g for g in current if g not in projected_current],
}

# ── FD-AGENCY-001 §5 items never started ─────────────────────────────────────
fd_surface = {
    "S-5 (§5): P13 reads organizational work state": not any(
        p13["source_reads_agency_state"].values()),
    "S-6 (§5): unified agency state view": not readers["planning_surface_discovery_in_tools"]
    and not readers["plan_outcome_callers_in_tools"],
    "S-7 (§5): resident runtime binding": not runtime_trace["resident_binder_w4_to_execution_layer"],
}

# ── Negative controls (in memory; nothing written) ───────────────────────────
from tools.agent_instance_registry import AgentInstanceRegistry  # noqa: E402
from tools.planning import AuthorityProvenance, Goal, Plan, PlanStep, PlanningSurface  # noqa: E402
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION  # noqa: E402


def refused(call):
    try:
        call()
        return "NOT REFUSED"
    except Exception as exc:
        return f"refused: {type(exc).__name__}: {str(exc)[:110]}"


AGENT = "engineering-intelligence-instance-001"
S4_ROOT = AGENCY_OPS / "w4-s4-plan-outcome"
mem = AgentInstanceRegistry(None)
mem.register(instance_key=AGENT, definition=SELECTED_DEFINITION,
             permitted_capabilities=("engineering-intelligence",),
             created_by=w4.AUTHORIZED_DELEGATOR,
             authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
             accountable_to=w4.AUTHORIZED_DELEGATOR)
surface = PlanningSurface()
surface.declare(Goal("s6-control", "control", AuthorityProvenance("S-6 control", FD_RECORD)))
plan = surface.adopt(Plan(key="s6-control-plan-0", goal_key="s6-control",
                          authority=AuthorityProvenance("S-6 control", FD_RECORD),
                          steps=(PlanStep("x", "x", requires_delegation=True),)))
s4_surface = planning_continuity.restore(S4_ROOT / "planning.state.json")
any_grant = "3cc612275a914c2c"
controls = {
    "N8_agent_cannot_decide": refused(lambda: w4.review_result(
        S4_ROOT, any_grant, surface=s4_surface, decision=w4.ACCEPT, reviewer=AGENT,
        reason="agent")),
    "N9_agent_cannot_delegate": refused(lambda: w4.issue_from_plan(
        w4.W4DelegationRegistry(mem, None), surface, plan, "x", delegator=AGENT,
        recipient_instance=AGENT, authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
        capability_scope=("engineering-intelligence",), resource_boundary="r",
        output_expectation="o", verification_requirement="v", escalation_condition="e")),
    "N2_capability_not_created_by_delegation": refused(lambda: w4.W4DelegationRegistry(
        mem, None).issue(
        delegator=w4.AUTHORIZED_DELEGATOR, recipient_instance=AGENT,
        authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD), objective="o",
        capability_scope=("risk-management",), work_scope=("x",), lifecycle_boundary="l",
        resource_boundary="r", output_expectation="o", verification_requirement="v",
        escalation_condition="e", accountable_party=w4.AUTHORIZED_DELEGATOR,
        termination_condition="t")),
    "N7_candidate_not_a_recipient": refused(lambda: w4.W4DelegationRegistry(
        mem, None).issue(
        delegator=w4.AUTHORIZED_DELEGATOR, recipient_instance="monkey-d-luffy",
        authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD), objective="o",
        capability_scope=("engineering-intelligence",), work_scope=("x",),
        lifecycle_boundary="l", resource_boundary="r", output_expectation="o",
        verification_requirement="v", escalation_condition="e",
        accountable_party=w4.AUTHORIZED_DELEGATOR, termination_condition="t")),
    "N10_decision_outside_the_three": refused(lambda: w4.review_result(
        S4_ROOT, any_grant, surface=s4_surface, decision="APPROVE_AS_FOUNDER",
        reviewer=w4.AUTHORIZED_DELEGATOR, reason="x")),
}
candidates = ("luffy", "nami", "zoro", "usopp", "robin", "franky", "chopper", "sanji",
              "jinbe", "brook")
instance_names = [p.name for p in REPO.rglob("*.instance.json") if ".git" not in p.parts]
controls["N7_no_instance_named_after_a_candidate"] = not [
    n for n in instance_names if any(c in n.lower() for c in candidates)]
controls["N12_gaps_named_against_existing_mechanisms"] = all(
    (REPO / m).is_file() for m in (
        "tools/w4_continuity.py", "tools/w4_delegation.py", "tools/planning_continuity.py",
        "tools/p13/state.py", "tools/delegation_reconciliation.py", "tools/w4_execution.py",
        "native_core/core/runtime/execution/composition.py", "consumers/observation.py",
        "tools/p12_trace_registry.py", "tools/escalation_register.py"))

# ── Fresh-process determinism: the same reconstruction in a second process ───
probe = (
    "import sys,json,hashlib;sys.path.insert(0,%r);import tools;"
    "from tools import w4_continuity as c;o=c.operational_overview();"
    "print(hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest())"
) % str(REPO)
second = subprocess.run([sys.executable, "-c", probe], cwd=REPO, capture_output=True,
                        text=True).stdout.strip()
first = hashlib.sha256(json.dumps(overview, sort_keys=True, default=str).encode()).hexdigest()

# ── Integrity: after equals before equals baseline ───────────────────────────
after = base.surfaces()
register_after = base.register_state()
register_bytes = (REPO / base.REGISTER).read_bytes()
expected_change = "agency_records:docs/architecture/agency/*.md"   # the S-6 record itself
integrity = {
    "run_changed_nothing": before == after and register_before == register_after,
    "surfaces_equal_baseline": {k: after[k] == BASELINE["surfaces"][k] for k in after},
    "register_only_appended": register_bytes[:BASELINE["register"]["bytes"]] and hashlib.sha256(
        register_bytes[:BASELINE["register"]["bytes"]]).hexdigest() == BASELINE["register"]["sha256"],
    "s6_act_unchanged": base.sha(REPO / base.S6_ACT) == BASELINE["s6_act_sha256"],
    "integrity_faults": [str(f) for f in __import__(
        "tools.certified_evidence_integrity", fromlist=["verify"]).verify().faults],
    "git_status_certified": git("status", "--porcelain", "--", "docs/architecture/p11",
                                "docs/architecture/p12", "docs/architecture/p13",
                                "docs/architecture/platform-organization",
                                "docs/operations") or "(clean)",
}
unchanged_required = [k for k in after if k != expected_change]
controls.update({
    "N1_no_new_agent": integrity["surfaces_equal_baseline"]["agent_registry:*.instance.json"],
    "N2_no_new_capability": integrity["surfaces_equal_baseline"][
        "capability_catalog:docs/architecture/organization"],
    "N3_no_new_canonical_entity": integrity["surfaces_equal_baseline"][
        "governance:docs/governance (except Register and S-6 act)"]
    and integrity["register_only_appended"],
    "N4_no_delegation_issued": integrity["surfaces_equal_baseline"][
        "operational:agency/operations"],
    "N5_no_operational_state_change": integrity["surfaces_equal_baseline"][
        "operational:agency/operations"],
    "N6_no_certified_change": all(v for k, v in integrity["surfaces_equal_baseline"].items()
                                  if k.startswith("certified:")),
    "N7_candidates_unchanged": integrity["surfaces_equal_baseline"][
        "candidates:docs/architecture/candidates"],
    "N10_authority_unchanged": w4.AUTHORIZED_DELEGATOR == "Claude Code / AIOS Co-Founder"
    and integrity["surfaces_equal_baseline"][
        "governance:docs/governance (except Register and S-6 act)"],
    "N11_deployment_unchanged": integrity["surfaces_equal_baseline"]["deployment:vercel.json"]
    and integrity["surfaces_equal_baseline"]["code:fullstack"],
    "code_unchanged": all(v for k, v in integrity["surfaces_equal_baseline"].items()
                          if k.startswith("code:") or k.startswith("root_entry_points")),
})

result = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": base.sha(__file__), "head": git("rev-parse", "HEAD"),
    "baseline_head": BASELINE["head"],
    "chain": {"planning_surfaces": surfaces, "decisions_by_provenance": decisions,
              "open_goals": open_goals, "grants_on_open_goals": grants_on_open_goals,
              "current_grants": current, "roots": overview["roots"],
              "escalations": {k: {x: e[x] for x in ("historical_state", "operational_state",
                                                     "classification")}
                              for k, e in overview["escalations"].items()},
              "roots_with_live_grants_reported_coherent": pending_not_flagged},
    "runtime_trace": runtime_trace,
    "p13": p13, "readers": readers, "w3": w3_view, "canonical_state": canonical_state,
    "fd_agency_001_section_5_items_not_started": fd_surface,
    "fresh_process": {"overview_sha256_this_process": first,
                      "overview_sha256_second_process": second, "equal": first == second},
    "negative_controls": controls,
    "integrity": integrity,
    "surfaces_changed_vs_baseline": [k for k in unchanged_required
                                     if not integrity["surfaces_equal_baseline"][k]],
}
result["all_ok"] = (
    integrity["run_changed_nothing"] and not result["surfaces_changed_vs_baseline"]
    and integrity["register_only_appended"] and integrity["s6_act_unchanged"]
    and not integrity["integrity_faults"] and integrity["git_status_certified"] == "(clean)"
    and all(str(v).startswith("refused") for k, v in controls.items() if isinstance(v, str))
    and all(v for v in controls.values() if isinstance(v, bool))
    and result["fresh_process"]["equal"])
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False, default=str) + "\n",
               encoding="utf-8")
print(json.dumps({k: result[k] for k in (
    "runtime_trace", "p13", "readers", "w3", "canonical_state", "fd_agency_001_section_5_items_not_started",
    "fresh_process", "negative_controls", "surfaces_changed_vs_baseline", "all_ok")},
    indent=1, ensure_ascii=False, default=str))
print(json.dumps(result["chain"]["open_goals"], indent=1))
print(json.dumps(result["integrity"], indent=1, default=str))
