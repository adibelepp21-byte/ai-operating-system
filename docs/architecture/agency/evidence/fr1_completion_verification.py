"""FR-1 completion (FD-FR1-001) verification, in a fresh process. READ-ONLY.

Compares the state after P13 is wired and registered with
``FR1-COMPLETION-BASELINE-2026-10-03.json`` (captured before), checks every item
of FD-FR1-001 `§6` and `§8`, and separates **data changes** (what a consumer
appearing is expected to move) from **certified semantic changes** (which must
be none). Writes only ``FR1-COMPLETION-VERIFICATION-2026-10-03.json``.
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
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import tools  # noqa: E402,F401  -- installs the certified-write barrier before anything runs
import fr1_baseline as fb  # noqa: E402
import fr1_completion_baseline as cb  # noqa: E402
import td_state_authority_baseline as td  # noqa: E402

OUT = HERE / "FR1-COMPLETION-VERIFICATION-2026-10-03.json"
BASE = json.loads((HERE / "FR1-COMPLETION-BASELINE-2026-10-03.json").read_text(encoding="utf-8"))
STALE_14 = json.loads((HERE / "TD-STATE-AUTHORITY-DISCOVERY-2026-10-04.json").read_text(
    encoding="utf-8"))["k7"]["counts"]["p12_w2_active_that_are_operationally_closed"]
P13_KEYS = ("operational_state.delegations", "operational_state.escalations")


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True).stdout.strip()


def normal(value):
    return json.loads(json.dumps(value, sort_keys=True, default=str))


# Read as data, by name (the disclosed verifier pattern): this tool measures the
# surface and must not enter the consumer measurement it is checking.
w2 = importlib.import_module("tools.p12_operational_state")
from tools import w4_continuity  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402
from tools.p13.catalog import RESERVED  # noqa: E402
from tools.p13.paths import LIVE  # noqa: E402
from tools.p13.state import StateUnderstanding  # noqa: E402

surfaces_before = td.surfaces()
entries = {e.state_id: e for e in w2.project()}
delegation, escalation = entries["delegation.granted"].value, entries["escalation.raised"].value
overview = w4_continuity.operational_overview()
live = sorted(g["delegation_id"] for g in overview["grants"].values() if g["executable"])
facts = {f.key: f for f in StateUnderstanding(LIVE).observe().facts}       # the real P13 sources
measurement = normal(cb.consumer_measurement())
populations, verdicts = normal(fb.populations()), normal(fb.verdicts())
p13_code = "".join(p.read_text(encoding="utf-8") for p in sorted((REPO / "tools/p13").glob("*.py")))

probe = ("import sys,json;sys.path.insert(0,%r);import tools;"
         "from tools.p13.paths import LIVE;from tools.p13.state import SOURCES,StateUnderstanding;"
         "s=StateUnderstanding(LIVE,sources=tuple(x for x in SOURCES if x.name=='operational_state')).observe();"
         "print(json.dumps({f.key:[f.value,f.status] for f in s.facts},sort_keys=True,default=str))"
         ) % str(REPO)
second = json.loads(subprocess.run([sys.executable, "-c", probe], cwd=REPO, capture_output=True,
                                   text=True, check=True).stdout)
here = normal({k: [facts[k].value, facts[k].status] for k in P13_KEYS})

changed = sorted(set(git("diff", "--name-only", BASE["head"], "--", "tools", "native_core",
                         "consumers", "api", "fullstack").splitlines()
                     + git("ls-files", "--others", "--exclude-standard", "tools").splitlines()))
expected = sorted(["tools/p13/state.py", "tools/p12_consumer_evidence_verifier.py",
                   "tools/tests/test_p12_state_verification.py",
                   "tools/tests/test_p12_consumer_measurement.py", "tools/tests/test_p13.py",
                   "tools/tests/test_p13_e13_05.py", "tools/tests/test_p13_post_construction.py",
                   "tools/tests/test_fr1_operational_state_integration.py"])
verifier_diff = [line for line in git("diff", "-U0", BASE["head"], "--",
                                      "tools/p12_consumer_evidence_verifier.py").splitlines()
                 if line[:1] in "+-" and not line.startswith(("+++", "---"))]
base_cm = BASE["consumer_measurement"]
links_now = measurement["state_chain_links"]

data_changes = {
    "consumers": [base_cm["consumers"], measurement["consumers"]],
    "importers": [base_cm["importers"], measurement["importers"]],
    "registered_candidates_added": [c for c in measurement["candidates"]
                                    if c not in base_cm["candidates"]],
    "consumer_link": [base_cm["state_chain_links"]["CONSUMER"], links_now["CONSUMER"]],
    "p13_facts_added": sorted(set(facts) - set(BASE["readings"]["p13_fact_keys"])),
}
semantic_unchanged = {
    "certified_roots_byte_identical": all(surfaces_before[k] == BASE["surfaces"][k]
                                          for k in BASE["surfaces"] if k.startswith("certified:")),
    "p13_certified_blueprint_unchanged": surfaces_before["certified:docs/architecture/p13"]
    == BASE["surfaces"]["certified:docs/architecture/p13"],
    "consumer_scanner_unchanged": git("diff", BASE["head"], "--", "tools/p12_state_verification.py") == "",
    "independent_verifier_change_is_one_registration": all(
        line.startswith("+") for line in verifier_diff)
    and any('("tools.p13.state", "_operational_state")' in line for line in verifier_diff),
    "independent_verifier_checks_same": [c for c in measurement["independent_verifier"]["not_agreeing"]] == []
    and measurement["independent_verifier"]["checks"] == base_cm["independent_verifier"]["checks"],
    "state_chain_link_statuses_same": {k: v[0] for k, v in links_now.items()}
    == {k: v[0] for k, v in base_cm["state_chain_links"].items()},
    "p12_w2_contract_same": len(w2.SOURCES) == 8 and all(
        s.provider == w2.UNRESOLVED_PROVIDER for s in w2.SOURCES)
    and git("diff", BASE["head"], "--", "tools/p12_operational_state.py") == "",
    "verifier_populations_same": populations == BASE["populations"],
    "verifier_verdicts_same": verdicts == normal(BASE["verdicts"]),
    "governance_and_envelopes_same": all(surfaces_before[k] == BASE["surfaces"][k] for k in (
        "governance:docs/governance (except Register and the S-6 / TD acts)", "p13:envelopes")),
}
section_6 = {
    "1_w2_current_vs_historical": delegation["current"] == live and len(live) == 2
    and not set(STALE_14) & set(delegation["current"])
    and set(STALE_14) <= set(delegation["historical"]["recorded_active_not_current"]),
    "2_w2_blocking_vs_historical_answered": escalation["blocking"] == overview["blocking_escalations"]
    and set(escalation["answered"]) == {e["escalation_id"] for e in overview["escalations"].values()
                                        if e["operational_state"] == "ANSWERED"},
    "3_p13_receives_through_p12_w2": facts["operational_state.delegations"].status == "VERIFIED"
    and facts["operational_state.delegations"].value["current"] == live
    and all("P12-W2" in facts[k].source for k in P13_KEYS),
    "4_certified_measurement_recognizes_p13": "tools/p13/state.py" in measurement["consumers"]
    and "tools/p13/state.py" in measurement["independent_verifier"]["observed_consumers"]
    and measurement["independent_verifier"]["disagrees"] == 0
    and links_now["CONSUMER"][0] == "SATISFIED",
    "5_existing_certified_verifiers_valid": semantic_unchanged["verifier_verdicts_same"]
    and semantic_unchanged["state_chain_link_statuses_same"],
    "6_source_populations_unchanged": semantic_unchanged["verifier_populations_same"],
    "7_no_direct_agency_to_p13": not any(n in p13_code for n in (
        "w4_continuity", "w4_delegation", "plan_outcome", "LIVE_LEDGER", "LIVE_RESPONSES",
        "operational_overview", "planning_continuity"))
    and "from tools import p12_operational_state as w2" in p13_code,
    "8_fresh_process_reproduces": second == here,
    "9_s1_to_mr_s5_1_intact": fb.digest(overview) == BASE["readings"]["operational_overview_sha256"]
    and facts["escalations.open"].value == BASE["readings"]["p13_escalations_open"],
    "10_no_new_current_state_authority": changed == expected and not w2.conflicts()
    and w4.AUTHORIZED_DELEGATOR == "Claude Code / AIOS Co-Founder" and "issue.delegation" in RESERVED,
}
surfaces_after = td.surfaces()
result = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "head": git("rev-parse", "HEAD"), "baseline_head": BASE["head"],
    "section_6": section_6,
    "data_changes": data_changes,
    "certified_semantics_unchanged": semantic_unchanged,
    "p13_observed": {k: {"status": facts[k].status, "source": facts[k].source,
                         "value": facts[k].value} for k in P13_KEYS},
    "changed_code": changed,
    "run_changed_nothing": surfaces_before == surfaces_after,
    "integrity_faults": [str(f) for f in importlib.import_module(
        "tools.certified_evidence_integrity").verify().faults],
    "git_status_certified": git("status", "--porcelain", "--", "docs/architecture/p11",
                                "docs/architecture/p12", "docs/architecture/p13",
                                "docs/architecture/platform-organization", "docs/operations") or "(clean)",
}
result["all_ok"] = (all(section_6.values()) and all(semantic_unchanged.values())
                    and result["run_changed_nothing"] and not result["integrity_faults"]
                    and result["git_status_certified"] == "(clean)")
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
print(json.dumps({k: result[k] for k in ("section_6", "certified_semantics_unchanged", "data_changes",
                                          "changed_code", "run_changed_nothing", "integrity_faults",
                                          "git_status_certified", "all_ok")}, indent=1, default=str))
