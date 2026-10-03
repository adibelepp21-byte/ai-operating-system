"""Targeted Discovery — state authority, P13 change boundary, Agency frontiers.

READ-ONLY EVIDENCE TOOL. Directive:
docs/governance/acts/DIR-AIOS-AGENCY-TD-STATE-AUTHORITY-P13-RECONCILIATION.md.

Rebuilds from files, in a fresh process, every comparison the record makes:

* K-7: each state reader's reading of the same grants and escalations
  (P12-W2 Unified Operational State, P13's escalation fact, W3, the A2 / CG-7
  operational overview), and the declared source contract of P12-W2;
* K-8: what the certified P13 manifest holds, what the certified Blueprint's
  integration map names, and what the P13 implementation actually imports;
* K-LABEL: where S-1 … S-7 were first defined, and what each later directive
  calls the same label;
* FR-3: whether LIVE / PENDING / BLOCKED / WAITING / HISTORICAL / COMPLETED /
  REVOKED can be told apart from the existing readers, without changing state;
* FR-4: whether function → capability → agent → current state is representable;
* N1–N12 and the integrity comparison with the baseline.

The classifications here are **evidence computed in this script**, not a
reader: nothing in ``tools/`` gains a caller, and nothing is written except
``TD-STATE-AUTHORITY-DISCOVERY-2026-10-04.json``.
"""
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import tools  # noqa: E402,F401  -- installs the certified-write barrier before anything runs
import td_state_authority_baseline as base  # noqa: E402
import s6_baseline as s6  # noqa: E402

OUT = HERE / "TD-STATE-AUTHORITY-DISCOVERY-2026-10-04.json"
BASELINE = json.loads((HERE / "TD-STATE-AUTHORITY-BASELINE-2026-10-04.json").read_text(
    encoding="utf-8"))
AGENCY_OPS = REPO / "docs/architecture/agency/operations"


def text(rel_path):
    return (REPO / rel_path).read_text(encoding="utf-8")


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True).stdout.strip()


before = base.surfaces()
register_before = s6.register_state()

from tools import delegation_reconciliation as w3  # noqa: E402
from tools import p12_operational_state as w2  # noqa: E402
from tools import p12_provenance_verification as prov  # noqa: E402
from tools import p12_self_model  # noqa: E402
from tools import planning_continuity  # noqa: E402
from tools import w4_continuity  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402

# ── K-7: one population, four readings ───────────────────────────────────────
overview = w4_continuity.operational_overview()
w2_entries = {e.state_id: e for e in w2.project()}
w2_sources = {s.state_id: s for s in w2.SOURCES}
w2_population = {d["delegation_id"]: d.get("status") for d in prov.delegation_records()}
w3_projections = {p.grant_id: p.role for p in w3.reconcile()["projections"] if p.grant_id}
grants = {}
for g in overview["grants"].values():
    gid = g["delegation_id"]
    grants[gid] = {
        "root": g["root"], "certified_record": g["certified_record"],
        "historical": g["historical_status"], "operational": g["operational_status"],
        "classification": g["classification"],
        "p12_w2_counts_it": gid in w2_population,
        "p12_w2_reads_it_as": w2_population.get(gid),
        "w3_role": w3_projections.get(gid),
    }
self_model_open = sorted(p12_self_model.incomplete(REPO).value["open_escalations"])
escalations = {e["escalation_id"]: {"historical": e["historical_state"],
                                    "operational": e["operational_state"],
                                    "classification": e["classification"],
                                    "p13_reads_open": e["escalation_id"] in self_model_open}
               for e in overview["escalations"].values()}
w2_delegation = w2_sources["delegation.granted"]
w2_code = text("tools/p12_operational_state.py") + text("tools/p12_provenance_verification.py")
k7 = {
    "p12_w2": {
        "delegation_entry": {"status": w2_entries["delegation.granted"].status,
                             "value": w2_entries["delegation.granted"].value,
                             "transformation": w2_entries["delegation.granted"].transformation},
        "delegation_source_contract": {k: getattr(w2_delegation, k) for k in (
            "owner", "canonical_source", "read_path", "freshness_model", "owns_within_class",
            "provider")},
        "escalation_entry_value": w2_entries["escalation.raised"].value,
        "providers": sorted({s.provider for s in w2.SOURCES}),
        "delegation_roots": [str(r.relative_to(REPO)) for r in prov.DELEGATION_ROOTS],
        "reads_live_ledger_or_dispositions": any(n in w2_code for n in (
            "LIVE_LEDGER", "read_dispositions", "operational_state(", "operational_overview")),
        "reads_live_responses": "LIVE_RESPONSES" in w2_code or "response_ledger" in w2_code,
        "conflicts_detected_now": len(w2.conflicts()),
        "resident_non_verifier_consumers": sorted(
            str(p.relative_to(REPO)) for p in (REPO / "tools").rglob("*.py")
            if "tests" not in p.parts and p.name != "p12_operational_state.py"
            and "p12_operational_state" in p.read_text(encoding="utf-8")
            and not re.search(r"(verif|measurement|contract)", p.name)),
    },
    "grants": grants,
    "counts": {
        "p12_w2_active": w2_entries["delegation.granted"].value["active"],
        "operational_active": sorted(g for g, v in grants.items() if v["operational"] == "ACTIVE"),
        "operational_active_counted_by_p12_w2": sorted(
            g for g, v in grants.items() if v["operational"] == "ACTIVE" and v["p12_w2_counts_it"]),
        "p12_w2_active_that_are_operationally_closed": sorted(
            g for g, s in w2_population.items() if s == "ACTIVE"
            and grants.get(g, {}).get("operational") in ("COMPLETED", "REVOKED")),
        "w3_current_and_their_operational_status": {
            g: grants.get(g, {}).get("operational") for g, r in w3_projections.items()
            if r == "CURRENT"},
    },
    "escalations": escalations,
    "operational_overview_claims": {
        "docstring_says_reader_not_store": "it writes nothing and holds no state of its own"
        in text("tools/w4_continuity.py")},
    "authority_texts": {
        "A2_current_terminal_disposition": "record the current terminal disposition of delegations"
        in text("docs/governance/acts/FD-AGENCY-001-S1-TERMINAL-STATE-DECISION.md"),
        "A2_reader_may_honor": "The existing delegation state reader may honor this live operational state"
        in text("docs/governance/acts/FD-AGENCY-001-S1-TERMINAL-STATE-DECISION.md"),
        "P12_D7_no_two_competing": "Tidak boleh terdapat dua competing system-wide state authorities"
        in text("docs/governance/acts/P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md"),
        "P12_D7_no_takeover_of_domain_ownership": "P12-W2 tidak boleh mengambil alih domain-specific state ownership"
        in text("docs/governance/acts/P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md"),
        "P12_blueprint_s17_conflict_rule": "STATE AUTHORITY CONFLICT"
        in text("docs/architecture/p12/AIOS_P12_ROADMAP_PRD_CONSTRUCTION_BLUEPRINT_v1.0.md"),
        "P12_blueprint_s19_historical_as_current": "historical state presented as current"
        in text("docs/architecture/p12/AIOS_P12_ROADMAP_PRD_CONSTRUCTION_BLUEPRINT_v1.0.md"),
        "FD_CG7_R2_no_second_model": "Do not create a second competing state model"
        in text("docs/governance/acts/FD-CG7-001-P12-OPERATIONAL-STATE-DISPOSITION-DECISION.md"),
        "delegation_catalog_R2_population_fixed": "``operation_roots()`` stays P11-only"
        in text("tools/delegation_catalog.py"),
    },
}

# ── K-8: certified P13 boundary vs implementation ────────────────────────────
blueprint = "docs/architecture/p13/AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md"
p13_manifest = json.loads(text("docs/governance/AIOS_P13_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json"))
p13_code = {str(p.relative_to(REPO)): p.read_text(encoding="utf-8")
            for p in sorted((REPO / "tools/p13").glob("*.py"))}
from tools.p13.state import SOURCES as P13_SOURCES  # noqa: E402
k8 = {
    "certified_manifest_files": sorted(p13_manifest["files"]),
    "certified_root": p13_manifest["evidence_root"],
    "tools_p13_in_any_certified_manifest": any(
        "tools/p13" in text(str(p.relative_to(REPO)))
        for p in (REPO / "docs/governance").glob("*MANIFEST*.json")),
    "fdr7_certified_root_excludes_implementation": (
        "Supporting implementation, governance records, operational evidence, and historical "
        "proof artifacts remain outside the certified architecture root") in text(
        "docs/governance/acts/FDR-7-P13-FOUNDER-CERTIFICATION-AND-FINAL-SYSTEM-ACCEPTANCE.md"),
    "blueprint_integration_map_names_p12_w2": "`tools.p12_operational_state.project()`" in text(
        blueprint),
    "blueprint_integration_map_excludes_org_beyond_delegations":
        "Workflow, Tool, Agent, Organization (beyond delegations), Runtime" in text(blueprint),
    "blueprint_state_understanding_names_operational_state":
        "P12 self-model (12 answers), operational state" in text(blueprint),
    "p13_sources": [s.name for s in P13_SOURCES],
    "p13_code_imports_p12_operational_state": any(
        "p12_operational_state" in c for c in p13_code.values()),
    "p13_code_reads_agency_state": {n: any(n in c for c in p13_code.values()) for n in (
        "w4_continuity", "plan_outcome", "operational_overview", "LIVE_LEDGER", "LIVE_RESPONSES")},
    "fdr_g1_escalate_if_uncertain": "If uncertain, the change MUST be escalated rather than "
    "classified opportunistically as maintenance" in text(
        "docs/governance/acts/FDR-G1-POST-P13-GOVERNANCE-FOUNDATION.md"),
    "fdr_g1_interfaces_presumed_material": "certified interfaces" in text(
        "docs/governance/acts/FDR-G1-POST-P13-GOVERNANCE-FOUNDATION.md"),
    "fdr_g2_maintenance_must_not_alter_p13_scope": "alter P13 scope" in text(
        "docs/governance/acts/FDR-G2-P13-CLOSURE-RESIDUAL-GOVERNANCE-AND-POST-CLOSURE-OPERATING-MODEL.md"),
    "issue_delegation_reserved_for_p13": "issue.delegation" in __import__(
        "tools.p13.catalog", fromlist=["RESERVED"]).RESERVED,
}

# ── K-LABEL ──────────────────────────────────────────────────────────────────
record = text("docs/architecture/agency/FD-AGENCY-001-DECISION-RECORD.md")
section5 = record[record.index("## 5. Authorized implementation surface"):
                  record.index("## 6. Closure check")]
items = dict(re.findall(r"\| (S-[1-7]) \| ([^|]+) \|", section5))
acts = "docs/governance/acts/"
directive_titles = {}
for label, name in (("S-1", "DIR-AIOS-AGENCY-S1-DELEGATION-CLOSURE.md"),
                    ("S-2", "DIR-AIOS-AGENCY-S2-PLAN-TO-DELEGATION.md"),
                    ("S-3", "DIR-AIOS-AGENCY-S3-FOUNDER-GOAL-TO-PLANNING.md"),
                    ("S-4", "DIR-AIOS-AGENCY-S4-AGENT-EVIDENCE-TO-PLAN-OUTCOME.md"),
                    ("S-5", "DIR-AIOS-AGENCY-S5-DISPOSITION-SEMANTICS-DISCOVERY.md"),
                    ("S-6", "DIR-AIOS-AGENCY-S6-SYSTEMIC-INTEGRATION-FRONTIER-DISCOVERY.md")):
    t = text(acts + name)
    directive_titles[label] = t.splitlines()[0].lstrip("# ").strip()
register = text(s6.REGISTER)
labels = {
    "section5_items": {k: v.strip() for k, v in items.items()},
    "founder_instrument_defines_s_items": bool(re.search(
        r"\bS-[1-7]\b", text(acts + "FD-AGENCY-001-FOUNDER-DECISION.md"))),
    "s1_directive_cites_s2_to_s7": "S-2–S-7" in text(acts + "DIR-AIOS-AGENCY-S1-DELEGATION-CLOSURE.md"),
    "s2_directive_cites_s3_to_s7": "S-3, S-4, S-5, S-6, or S-7" in text(
        acts + "DIR-AIOS-AGENCY-S2-PLAN-TO-DELEGATION.md"),
    "later_directive_titles": directive_titles,
    "s7_directive_exists": any("S-7" in p.name or "S7" in p.name
                               for p in (REPO / acts).glob("DIR-AIOS-AGENCY-*")),
    "register_133_lists_surface": "implementation surface S-1…S-7, none started" in register,
    "explicit_supersession_or_rename_in_register": bool(re.search(
        r"(supersed|renam|relabel)[^\n]{0,120}(FD-AGENCY-001 `?§5|§5 item)", register)),
}

# ── FR-3: the seven states, derived from existing readers only ───────────────
derived = {}
for gid, g in grants.items():
    root = REPO / g["root"]
    executed = (root / f"{gid}.evidence.json").is_file() or bool(
        [m for m in (REPO / "docs/architecture/p12/execution-provenance").glob("*.json")
         if gid in m.read_text(encoding="utf-8")])
    if g["operational"] == "COMPLETED":
        state = "COMPLETED"
    elif g["operational"] == "REVOKED":
        state = "REVOKED"
    elif g["classification"] != "CURRENT OPERATIONAL GRANT":
        state = "HISTORICAL"
    elif gid in overview["blocking_escalations"]:
        state = "BLOCKED"
    elif not executed:
        state = "PENDING (live, not executed)"
    else:
        state = "LIVE"
    derived[gid] = state
waiting = []
for statef in sorted(REPO.glob("docs/**/planning.state.json")):
    surface = planning_continuity.restore(statef)
    for key in sorted(surface._goals):                               # noqa: SLF001
        out = w4.plan_outcome(surface, key, statef.parent)
        if out["completed"]:
            continue
        current = next(v for v in out["versions"] if v["current"])
        for s in current["steps"]:
            if s["performed_by"] == "delegated agent" and not s["grants"] and not s["done"]:
                waiting.append(f"{key} / {s['step']} (open delegated step, no grant)")
vocabulary = {w: [str(p.relative_to(REPO)) for p in (REPO / "tools").glob("*.py")
                  if re.search(rf"\b{w}\b", p.read_text(encoding="utf-8"))
                  and p.name in ("w4_continuity.py", "w4_delegation.py",
                                 "p12_operational_state.py")]
              for w in ("PENDING", "WAITING")}
fr3 = {"derived_states": derived, "waiting_steps": waiting,
       "state_words_in_resident_readers": vocabulary,
       "roots_reporting_coherent_with_pending_grants": [
           r for r, info in overview["roots"].items()
           if any(derived.get(g) == "PENDING (live, not executed)"
                  for g in overview["current_grants"] if r in overview["grants"].get(
                      f"{r}/{g}", {}).get("root", ""))
           and info["conditions"] == ["NO BLOCKING CONDITION — prior state is coherent"]]}

# ── FR-4: organizational function → capability → agent → current state ──────
from tools import organization_catalog as org  # noqa: E402
departments = org.read_departments(org.ORGANIZATION_ROOT)
links, _ = org.w4_chain(departments, org.ORGANIZATION_ROOT)
instances = {}
for p in sorted(REPO.rglob("*.instance.json")):
    if ".git" in p.parts:
        continue
    rec = json.loads(p.read_text(encoding="utf-8"))
    instances.setdefault(rec.get("definition_key"), set()).add(rec.get("instance_key"))
fr4 = []
for department, capability, definition in links:
    held = sorted(instances.get(definition, ()))
    live = sorted(g["delegation_id"] for g in overview["grants"].values()
                  if g["recipient"] in held and g["operational_status"] == "ACTIVE")
    fr4.append({"department": department, "capability": capability, "definition": definition,
                "instances": held, "operationally_active_grants": live})

# ── Negative controls ────────────────────────────────────────────────────────
after = base.surfaces()
register_after = s6.register_state()
register_bytes = (REPO / s6.REGISTER).read_bytes()
equal = {k: after[k] == BASELINE["surfaces"][k] for k in after}
acts_now = sorted(p.name for p in (REPO / acts).glob("*.md"))
acts_new = sorted(set(acts_now) - set(
    git("ls-tree", "--name-only", BASELINE["head"], acts).replace(acts, "").split()))
controls = {
    "N1_no_p13_modification": equal["p13:tools/p13"] and equal["p13:envelopes"]
    and equal["certified:docs/architecture/p13"],
    "N2_no_p12_w2_modification": equal["p12_state:tools/p12_*.py"],
    "N3_no_w3_modification": equal["capability_catalog:docs/architecture/organization"]
    and equal["state_readers"],
    "N4_no_agency_state_mutation": equal["operational:agency/operations"],
    "N5_no_delegation_mutation": equal["operational:agency/operations"]
    and all(equal[k] for k in equal if k.startswith("certified:")),
    "N6_no_plan_mutation": equal["operational:agency/operations"],
    "N7_no_agent_creation": equal["agent_registry:*.instance.json"],
    "N8_no_capability_creation": equal["capability_catalog:docs/architecture/organization"],
    "N9_no_authority_expansion": equal[
        "governance:docs/governance (except Register and the S-6 / TD acts)"]
    and w4.AUTHORIZED_DELEGATOR == "Claude Code / AIOS Co-Founder",
    "N10_no_founder_decision_inferred": acts_new == [
        "DIR-AIOS-AGENCY-TD-STATE-AUTHORITY-P13-RECONCILIATION.md"],
    "N11_no_deployment_activation": equal["deployment:vercel.json"] and equal["code:fullstack"],
    "N12_no_competing_state_model": all(equal[k] for k in equal if k.startswith("code:"))
    and equal["state_readers"] and equal["p12_state:tools/p12_*.py"],
}
probe = ("import sys,json,hashlib;sys.path.insert(0,%r);import tools;"
         "from tools import w4_continuity as c, p12_operational_state as w;"
         "o=c.operational_overview();e=[x.value for x in w.project() if x.state_id=='delegation.granted'];"
         "print(hashlib.sha256(json.dumps([o,e],sort_keys=True,default=str).encode()).hexdigest())"
         ) % str(REPO)
second = subprocess.run([sys.executable, "-c", probe], cwd=REPO, capture_output=True,
                        text=True).stdout.strip()
first = hashlib.sha256(json.dumps([overview, [w2_entries["delegation.granted"].value]],
                                  sort_keys=True, default=str).encode()).hexdigest()
integrity = {
    "run_changed_nothing": before == after and register_before == register_after,
    "surfaces_equal_baseline": equal,
    "register_only_appended": hashlib.sha256(
        register_bytes[:BASELINE["register"]["bytes"]]).hexdigest() == BASELINE["register"]["sha256"],
    "td_act_unchanged": s6.sha(REPO / base.TD_ACT) == BASELINE["td_act_sha256"],
    "integrity_faults": [str(f) for f in __import__(
        "tools.certified_evidence_integrity", fromlist=["verify"]).verify().faults],
    "git_status_certified": git("status", "--porcelain", "--", "docs/architecture/p11",
                                "docs/architecture/p12", "docs/architecture/p13",
                                "docs/architecture/platform-organization",
                                "docs/operations") or "(clean)",
    "fresh_process_equal": first == second,
}
expected_change = "agency_records:docs/architecture/agency/*.md"     # this gate's record
result = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": s6.sha(__file__), "head": git("rev-parse", "HEAD"),
    "baseline_head": BASELINE["head"],
    "k7": k7, "k8": k8, "labels": labels, "fr3": fr3, "fr4": fr4,
    "negative_controls": controls, "integrity": integrity,
    "surfaces_changed_vs_baseline": [k for k, v in equal.items()
                                     if not v and k != expected_change],
}
result["all_ok"] = (integrity["run_changed_nothing"] and not result["surfaces_changed_vs_baseline"]
                    and integrity["register_only_appended"] and integrity["td_act_unchanged"]
                    and not integrity["integrity_faults"]
                    and integrity["git_status_certified"] == "(clean)"
                    and integrity["fresh_process_equal"] and all(controls.values()))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False, default=str) + "\n",
               encoding="utf-8")
print(json.dumps({k: result[k] for k in ("k8", "labels", "fr3", "fr4", "negative_controls",
                                          "surfaces_changed_vs_baseline", "all_ok")},
                 indent=1, ensure_ascii=False, default=str))
print(json.dumps({"counts": k7["counts"], "escalations": k7["escalations"],
                  "p12_w2": k7["p12_w2"], "authority_texts": k7["authority_texts"]},
                 indent=1, ensure_ascii=False, default=str))
