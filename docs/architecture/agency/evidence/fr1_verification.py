"""FR-1 (FD-TD-001) verification, in a fresh process, against the pre-change baseline.

READ-ONLY: writes only ``FR1-VERIFICATION-2026-10-03.json``. Checks every item
of FD-TD-001 `§7`, the `§3` must-nots and the `§8` stop conditions, comparing
with ``FR1-BASELINE-2026-10-03.json`` (captured before any code changed).

Item 6 (P13 receives state through P12-W2) is **not constructed**: wiring it
makes the certified independent consumer verifier report DISAGREES unless its
candidate population is changed, which is a `§4` / `§8` stop. It is reported as
BLOCKED, and this script proves the stop held: P13 unchanged, the certified
consumer measurement agreeing.
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
import td_state_authority_baseline as td  # noqa: E402

OUT = HERE / "FR1-VERIFICATION-2026-10-03.json"
BASE = json.loads((HERE / "FR1-BASELINE-2026-10-03.json").read_text(encoding="utf-8"))


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True).stdout.strip()


# Read as data, by name (the disclosed pattern of `tools/p12_operational_state_verifier.py`):
# an evidence tool measures the surface and is not one of its consumers, so it must
# not enter the P12 consumer measurement (`p12_state_verification.consumers_of`).
w2 = importlib.import_module("tools.p12_operational_state")
from tools import w4_continuity  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402
from tools.p13.catalog import RESERVED  # noqa: E402
from tools.p13.paths import LIVE  # noqa: E402
from tools.p13.state import SOURCES as P13_SOURCES, StateUnderstanding  # noqa: E402

surfaces_before = td.surfaces()
entries = {e.state_id: e for e in w2.project()}
delegation = entries["delegation.granted"].value
escalation = entries["escalation.raised"].value
overview = w4_continuity.operational_overview()
#: The 14 grants the TD gate measured P12-W2 presenting as active (all closed).
stale_14 = json.loads((HERE / "TD-STATE-AUTHORITY-DISCOVERY-2026-10-04.json").read_text(
    encoding="utf-8"))["k7"]["counts"]["p12_w2_active_that_are_operationally_closed"]
live_2 = sorted(g["delegation_id"] for g in overview["grants"].values() if g["executable"])

snapshot = StateUnderstanding(LIVE).observe()                         # the real P13 sources
p13_facts = {f.key: f for f in snapshot.facts}
p13_code = "".join(p.read_text(encoding="utf-8") for p in sorted((REPO / "tools/p13").glob("*.py")))

probe = ("import sys,json,importlib;sys.path.insert(0,%r);import tools;"
         "w=importlib.import_module('tools.p12_operational_state');"
         "e={x.state_id:x.value for x in w.project()};"
         "print(json.dumps([e['delegation.granted'],e['escalation.raised']],sort_keys=True))"
         ) % str(REPO)
second = json.loads(subprocess.run([sys.executable, "-c", probe], cwd=REPO, capture_output=True,
                                   text=True, check=True).stdout)
here = json.loads(json.dumps([delegation, escalation], sort_keys=True, default=str))

from tools import p12_consumer_evidence_verifier as consumer_verifier  # noqa: E402
from tools import p12_state_verification as consumer_measure  # noqa: E402
SURFACE = "tools.p12_operational_state"
measured = (consumer_measure.consumers_of(SURFACE), consumer_measure.importers_of(SURFACE))
consumer_check = consumer_verifier.summary(*measured)

base_surfaces = BASE["surfaces"]
changed_code = sorted(git("diff", "--name-only", BASE["head"], "--", "tools", "native_core",
                          "consumers", "api", "fullstack").splitlines()
                      + [p for p in git("ls-files", "--others", "--exclude-standard", "tools").splitlines()])
expected_code = sorted(["tools/p12_operational_state.py",
                        "tools/tests/test_fr1_operational_state_integration.py"])
# Normalized through JSON, as the baseline was stored (tuples read back as lists).
populations_now = json.loads(json.dumps(fb.populations(), default=str))
verdicts_now = json.loads(json.dumps(fb.verdicts(), default=str))

checks = {
    "1_the_14_stale_no_longer_current": bool(stale_14) and not set(stale_14) & set(delegation["current"])
    and set(stale_14) <= set(delegation["historical"]["recorded_active_not_current"])
    and BASE["readings"]["w2"]["delegation.granted"]["value"]["active"] == 14,
    "2_the_2_live_grants_represented": delegation["current"] == live_2 and len(live_2) == 2
    and delegation["active"] == 2,
    "3_historical_stays_historical": delegation["historical"]["completed"] == sum(
        g["operational_status"] == "COMPLETED" for g in overview["grants"].values())
    and delegation["historical"]["revoked"] == sum(
        g["operational_status"] == "REVOKED" for g in overview["grants"].values())
    and surfaces_before["operational:agency/operations"] == base_surfaces["operational:agency/operations"],
    "4_escalation_semantics_correct": escalation["blocking"] == overview["blocking_escalations"]
    and set(escalation["answered"]) == {e["escalation_id"] for e in overview["escalations"].values()
                                        if e["operational_state"] == "ANSWERED"}
    and p13_facts["escalations.open"].value == BASE["readings"]["p13_escalations_open"],
    "5_certified_evidence_byte_identical": all(
        surfaces_before[k] == base_surfaces[k] for k in base_surfaces if k.startswith("certified:"))
    and not [str(f) for f in __import__("tools.certified_evidence_integrity",
                                        fromlist=["verify"]).verify().faults],
    "7_fresh_process_reconstruction_identical": second == here,
    "8_existing_behaviour_intact": populations_now == BASE["populations"]
    and verdicts_now == BASE["verdicts"]
    and fb.digest(overview) == BASE["readings"]["operational_overview_sha256"]
    and sorted(BASE["readings"]["p13_fact_keys"]) == sorted(p13_facts),
    "9_no_second_current_state_authority": changed_code == expected_code
    and len(w2.SOURCES) == 8 and not w2.conflicts()
    and not any(e.is_authority() for e in entries.values()),
    "10_authority_and_delegation_unchanged": surfaces_before[
        "governance:docs/governance (except Register and the S-6 / TD acts)"] == base_surfaces[
        "governance:docs/governance (except Register and the S-6 / TD acts)"]
    and surfaces_before["p13:envelopes"] == base_surfaces["p13:envelopes"]
    and w4.AUTHORIZED_DELEGATOR == "Claude Code / AIOS Co-Founder"
    and "issue.delegation" in RESERVED,
}
must_not = {
    "F-17_untouched": all(s.provider == w2.UNRESOLVED_PROVIDER for s in w2.SOURCES),
    "ownership_unchanged": (lambda s: (s.state_class, s.semantics, s.owner, s.owns_within_class) == (
        "AUTHORITY", w2.SOURCE_OF_TRUTH, "FD-P11-001 authorized delegator",
        "operational grants and their lifecycle"))(
        next(s for s in w2.SOURCES if s.state_id == "delegation.granted")),
    "verifier_populations_unchanged": populations_now == BASE["populations"],
    "no_agent_capability_store_or_subsystem": all(
        surfaces_before[k] == base_surfaces[k] for k in (
            "agent_registry:*.instance.json", "capability_catalog:docs/architecture/organization",
            "candidates:docs/architecture/candidates", "code:native_core", "code:consumers",
            "code:api", "code:fullstack", "deployment:vercel.json", "root_entry_points:*.py")),
    "no_direct_agency_to_p13": not any(n in p13_code for n in (
        "w4_continuity", "plan_outcome", "LIVE_LEDGER", "LIVE_RESPONSES", "operational_overview")),
    "certified_consumer_measurement_agrees": consumer_check["disagrees"] == 0
    and measured == (("tools/p12_e12_measurement.py", "tools/p12_negative_control_verification.py",
                      "tools/p12_self_model_contract.py"),
                     ("tools/p12_e12_measurement.py", "tools/p12_mutation_verification.py",
                      "tools/p12_negative_control_verification.py", "tools/p12_self_model_contract.py")),
    "p13_certified_root_unchanged": surfaces_before["certified:docs/architecture/p13"]
    == base_surfaces["certified:docs/architecture/p13"],
}
surfaces_after = td.surfaces()
result = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "head": git("rev-parse", "HEAD"), "baseline_head": BASE["head"],
    "p12_w2_before": {k: BASE["readings"]["w2"][k] for k in ("delegation.granted", "escalation.raised")},
    "p12_w2_after": {"delegation.granted": {"status": entries["delegation.granted"].status,
                                            "value": delegation},
                     "escalation.raised": {"status": entries["escalation.raised"].status,
                                           "value": escalation}},
    "item_6_p13_receives_state_through_p12_w2": {
        "status": "BLOCKED — not constructed (FD-TD-001 §4 / §8 stop)",
        "p13_unchanged": surfaces_before["p13:tools/p13"] == base_surfaces["p13:tools/p13"],
        "p13_imports_p12_w2": "p12_operational_state" in p13_code,
        "why": "a P13 import of P12-W2 is measured as a consumer that the certified independent "
               "consumer verifier cannot observe (DISAGREES) unless its CANDIDATES population "
               "and the two pinned certified-consumer tests are changed"},
    "consumer_measurement": {"consumers": measured[0], "importers": measured[1],
                             "independent_verifier": consumer_check},
    "p13_escalations_open_unchanged": p13_facts["escalations.open"].value,
    "changed_code": changed_code,
    "section_7": checks, "section_3_must_not": must_not,
    "run_changed_nothing": surfaces_before == surfaces_after,
    "git_status_certified": git("status", "--porcelain", "--", "docs/architecture/p11",
                                "docs/architecture/p12", "docs/architecture/p13",
                                "docs/architecture/platform-organization", "docs/operations") or "(clean)",
}
result["all_ok"] = (all(checks.values()) and all(must_not.values()) and result["run_changed_nothing"]
                    and result["git_status_certified"] == "(clean)")
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
print(json.dumps({k: result[k] for k in ("section_7", "section_3_must_not", "changed_code",
                                          "run_changed_nothing", "git_status_certified", "all_ok")},
                 indent=1))
