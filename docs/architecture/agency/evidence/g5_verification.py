"""FR-2 G5 (FD-FR2-002) verification, in a fresh process. READ-ONLY.

Checks `FD-FR2-002 §8` items 1–14 and the `§9` negative controls against what
is on disk, and compares with `G5-BASELINE-2026-10-04.json` (captured before any
code changed). Loads P12-W2, P13 and the root binding by name (the disclosed
verifier pattern), so it enters no consumer or reachability measurement. Writes
only ``G5-VERIFICATION-2026-10-04.json``.
"""
import ast
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
import fr2_baseline as fr2  # noqa: E402
import fr2c_baseline as fr2c  # noqa: E402
import g5_baseline as g5b  # noqa: E402

OUT = HERE / "G5-VERIFICATION-2026-10-04.json"
BASE = json.loads((HERE / "G5-BASELINE-2026-10-04.json").read_text(encoding="utf-8"))
GRANT = "2adef08b8efa4549"
EXECUTION = f"agency-{GRANT}-verify-runtime-path-mechanisms"
normal = fr2c.normal


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True).stdout.strip()


surfaces_before = fr2.surfaces()
w2 = importlib.import_module("tools.p12_operational_state")
chain = importlib.import_module("tools.p12_execution_chain_reader")
traces = importlib.import_module("tools.p12_trace_registry")
prov = importlib.import_module("tools.p12_execution_provenance")
p13_state = importlib.import_module("tools.p13.state")
p13_paths = importlib.import_module("tools.p13.paths")

entries = {e.state_id: e for e in w2.project()}
provenance, recorded = entries["execution.provenance"], entries["execution.recorded"]
live = provenance.value["live"]
execution = {e["execution_id"]: e for e in live["executions"]}.get(EXECUTION, {})
p13_now = g5b.p13_operational_state()
p13_exec = p13_now.get("operational_state.executions", [None, {}, ""])
verdict = {v.execution_id: v for v in chain.verify_live()}.get(EXECUTION)
readers_now = fr2c.certified_readers()
readers_before = BASE["certified_readers"]
measurement = normal(cb.consumer_measurement())

fresh = json.loads(subprocess.run(
    [sys.executable, "-c",
     "import sys,json;sys.path.insert(0,%r);import tools;"
     "from tools.p13.paths import LIVE;from tools.p13.state import SOURCES,StateUnderstanding;"
     "s=StateUnderstanding(LIVE,sources=tuple(x for x in SOURCES if x.name=='operational_state')).observe();"
     "f={x.key:x for x in s.facts}['operational_state.executions'];"
     "e={x['execution_id']:x for x in f.value['live']['executions']}[%r];"
     "print(json.dumps([f.status,f.source,e['provenance'],e['temporal'],e['completed']]))"
     % (str(REPO), EXECUTION)],
    cwd=REPO, capture_output=True, text=True, check=True).stdout)

p13_code = {p.name: p.read_text(encoding="utf-8") for p in sorted((REPO / "tools/p13").glob("*.py"))}
p13_modules = set()
for text in p13_code.values():
    for n in ast.walk(ast.parse(text)):
        if isinstance(n, ast.ImportFrom):
            p13_modules.add(n.module or "")
            p13_modules.update(f"{n.module}.{a.name}" for a in n.names)
        elif isinstance(n, ast.Import):
            p13_modules.update(a.name for a in n.names)
direct = [m for m in p13_modules if any(f in m for f in (
    "p12_runtime_observation", "p12_execution_chain_reader", "p12_execution_provenance",
    "w4_runtime_execution", "agency_runtime_execution"))]
direct_text = [t for t in ("operations/trace-stores", "operations/runtime-observations",
                           "operations/execution-provenance", "LIVE_STORE_ROOT",
                           "LIVE_MANIFEST_ROOT", "OBSERVATION_ROOT", "verify_live")
               if any(t in text for text in p13_code.values())]

cert_prov = {k: v for k, v in provenance.value.items() if k not in ("live", "origin")}
cert_rec = {k: v for k, v in recorded.value.items() if k not in ("live", "origin")}
base_prov = readers_before["p12_w2"]["execution.provenance"]
base_rec = readers_before["p12_w2"]["execution.recorded"]
trace_path = traces.LIVE_STORE_ROOT / execution.get("trace", {}).get("store", "-") / "trace"

section_8 = {
    "1_runtime_execution_intact": execution.get("runtime", {}).get("runtime_id")
    == f"agency-runtime-{GRANT}" and execution["runtime"]["observed"],
    "2_trace_intact": execution.get("trace", {}).get("joined") is True and trace_path.is_file(),
    "3_manifest_intact": (prov.LIVE_MANIFEST_ROOT / execution.get("manifest", "-")).is_file(),
    "4_p12_w2_observes_through_its_projection": provenance.status == w2.CURRENT
    and execution.get("delegation_id") == GRANT
    and execution.get("agent_instance") == "engineering-intelligence-instance-001"
    and execution.get("result", {}).get("available") is True
    and execution.get("result", {}).get("status") == "success",
    "5_p13_receives_through_p12_w2": p13_exec[0] == "VERIFIED"
    and "P12-W2 execution.provenance" in p13_exec[2]
    and EXECUTION in [e["execution_id"] for e in p13_exec[1]["live"]["executions"]],
    "6_p13_reads_no_agency_store": not direct and not direct_text
    and p13_paths.LIVE.trace_stores == traces.STORE_ROOT,
    "7_live_and_certified_distinguishable": provenance.value["origin"] == w2.CERTIFIED_ORIGIN
    and live["origin"] == w2.LIVE_ORIGIN and recorded.value["origin"] == w2.CERTIFIED_ORIGIN
    and recorded.value["live"]["origin"] == w2.LIVE_ORIGIN,
    "8_historical_not_current": execution.get("temporal") == w2.HISTORICAL
    and EXECUTION not in live["active"] and EXECUTION in live["completed"],
    "9_certified_populations_intact": cert_prov == base_prov[1] and cert_rec == base_rec[1]
    and readers_now["chain_summary"] == readers_before["chain_summary"]
    and readers_now["chain_verdicts"] == readers_before["chain_verdicts"]
    and readers_now["trace_registry_certified"] == readers_before["trace_registry_certified"]
    and readers_now["manifests_certified"] == readers_before["manifests_certified"]
    and normal(fb.populations()) == normal(BASE["populations"])
    and normal(fb.verdicts()) == normal(BASE["verdicts"]),
    "10_fr1_state_observation_unchanged": all(
        p13_now[k] == BASE["p13_operational_state"][k]
        for k in ("operational_state.delegations", "operational_state.escalations")),
    "11_provenance_seven_of_seven": bool(verdict and verdict.joined and len(verdict.edges) == 7),
    "12_fresh_process": fresh[:2] == ["VERIFIED", p13_exec[2]] and fresh[2:] == [
        chain.JOINED, w2.HISTORICAL, True],
    "13_consumer_measurement_recognizes_p13": "tools/p13/state.py" in measurement["consumers"]
    and "tools/p13/state.py" in measurement["independent_verifier"]["observed_consumers"]
    and measurement["independent_verifier"]["disagrees"] == 0
    and measurement == normal(BASE["consumer_measurement"]),
    "14_no_second_execution_state_authority": len(w2.SOURCES) == 8
    and readers_now["p12_w2_sources"] == readers_before["p12_w2_sources"]
    and not [c for c in w2.conflicts() if c["kind"] == "CONFLICT"]
    and not any(e.is_authority() for e in entries.values())
    and [s.name for s in p13_state.SOURCES if any("execution" in k for k in s.keys)]
    == ["operational_state"],
}
negative_controls = {
    "N1_p13_no_direct_trace": not [m for m in direct if "trace" in m or "chain" in m]
    and "operations/trace-stores" not in direct_text,
    "N2_p13_no_direct_runtime_store": not [m for m in direct if "observation" in m]
    and "operations/runtime-observations" not in direct_text,
    "N3_no_fabrication": all(e["valid_agency_execution"] == (e["provenance"] == chain.JOINED)
                             for e in live["executions"])
    and len(live["executions"]) == len(prov.manifests(prov.LIVE_MANIFEST_ROOT)),
    "N4_historical_not_current": all(
        (e["temporal"] == w2.CURRENT) == (e["runtime"]["classification"] == "LIVE")
        for e in live["executions"]),
    "N5_result_without_runtime_not_runtime_execution": "3cc612275a914c2c"
    not in {e["delegation_id"] for e in live["executions"]},
    "N6_runtime_without_provenance_not_agency": set(live["unbound_live_runtimes"]).isdisjoint(
        {e["runtime"]["runtime_id"] for e in live["executions"]}),
    "N7_certified_not_mutated": all(
        surfaces_before[k] == BASE["surfaces"][k] for k in BASE["surfaces"]
        if (k.startswith("certified:") and k != "certified:docs/operations")
        or k.startswith("store:docs/architecture")),
    "N8_live_not_in_certified": EXECUTION not in readers_now["manifests_certified"]
    and cert_prov == base_prov[1],
    "N9_no_second_authority": section_8["14_no_second_execution_state_authority"],
    "N10_fr1_unchanged": section_8["10_fr1_state_observation_unchanged"],
}
changed_code = sorted(set(git("diff", "--name-only", BASE["head"], "--", "tools", "native_core",
                              "consumers", "api", "fullstack", "agency_runtime_execution.py")
                          .splitlines()
                          + git("ls-files", "--others", "--exclude-standard", "tools").splitlines()))
surfaces_after = fr2.surfaces()
data_changes = sorted(k for k in BASE["surfaces"] if surfaces_before[k] != BASE["surfaces"][k])
expected_changes = {"code:tools", "p12_state:tools/p12_*.py", "p13:tools/p13", "state_readers",
                    "agency_records:docs/architecture/agency/*.md"}
result = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "head": git("rev-parse", "HEAD"), "baseline_head": BASE["head"],
    "section_8": section_8, "negative_controls": negative_controls,
    "projection": {"execution.provenance": normal(provenance.value),
                   "execution.recorded": normal(recorded.value)},
    "p13_fact": {"status": p13_exec[0], "source": p13_exec[2]},
    "fresh_process": fresh,
    "changed_code": changed_code,
    "surfaces_changed_vs_baseline": data_changes,
    "unexpected_surface_changes": sorted(set(data_changes) - expected_changes),
    "run_changed_nothing": surfaces_before == surfaces_after,
    "integrity_faults": [str(f) for f in importlib.import_module(
        "tools.certified_evidence_integrity").verify().faults],
    "git_status_certified": git("status", "--porcelain", "--", "docs/architecture/p10",
                                "docs/architecture/p11", "docs/architecture/p12",
                                "docs/architecture/p13", "docs/architecture/platform-organization")
    or "(clean)",
    "residual_open": ["G3 Runtime state persistence", "G6 Trace status semantics",
                      "G7 Trace escalation production"],
}
result["all_ok"] = (all(section_8.values()) and all(negative_controls.values())
                    and not result["unexpected_surface_changes"] and result["run_changed_nothing"]
                    and not result["integrity_faults"] and result["git_status_certified"] == "(clean)")
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
print(json.dumps({k: result[k] for k in ("section_8", "negative_controls", "changed_code",
                                          "surfaces_changed_vs_baseline", "unexpected_surface_changes",
                                          "run_changed_nothing", "integrity_faults",
                                          "git_status_certified", "all_ok")}, indent=1, default=str))
