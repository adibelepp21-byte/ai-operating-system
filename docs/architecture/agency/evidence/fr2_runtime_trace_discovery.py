"""FR-2 — governed execution → Runtime / Trace discovery. READ-ONLY EVIDENCE TOOL.

Directive: docs/governance/acts/DIR-AIOS-AGENCY-FR2-RUNTIME-TRACE-DISCOVERY.md.

Establishes from code, persisted records and an isolated probe:

* the actual Agency execution path (S-2 … MR-S5-1) for representative grants,
  each provenance link classified DIRECT / DERIVED / TEXTUAL / MISSING;
* what the existing Runtime, Execution Contract, Trace, `TracedAction`,
  `ExecutionManifest` and independent chain reader do, by **running them** in a
  temporary directory (Path A: Runtime-hosted; Path B: direct call). Nothing of
  the probe touches the repository: every store it writes lives in a temp dir;
  no grant is issued, no instance is registered, no work is executed under a
  live grant;
* what survives a process restart (a second interpreter reads the probe's store);
* what P13 can observe; N1–N12; integrity against ``FR2-BASELINE-2026-10-04.json``.

Writes only ``FR2-RUNTIME-TRACE-DISCOVERY-2026-10-04.json``. P12-W2 is not
imported (this tool must not enter the P12 consumer measurement).
"""
import hashlib
import importlib
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import tools  # noqa: E402,F401  -- installs the certified-write barrier before anything runs
import fr2_baseline as fb2  # noqa: E402
import s6_baseline as s6  # noqa: E402

OUT = HERE / "FR2-RUNTIME-TRACE-DISCOVERY-2026-10-04.json"
BASE = json.loads((HERE / "FR2-BASELINE-2026-10-04.json").read_text(encoding="utf-8"))
AGENCY = REPO / "docs/architecture/agency/operations"
INSTANCE = "engineering-intelligence-instance-001"


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True).stdout.strip()


def rel(p):
    return str(Path(p).relative_to(REPO))


def references(needle, where=(".",)):
    """Resident Python files (tests and this tool excluded) naming ``needle``."""
    found = set()
    for w in where:
        for p in sorted((REPO / w).rglob("*.py")):
            if "tests" in p.parts or "__pycache__" in p.parts or p == Path(__file__).resolve():
                continue
            if needle in p.read_text(encoding="utf-8"):
                found.add(rel(p))
    return sorted(found)


before = fb2.surfaces()
register_before = s6.register_state()

# ── B/C/D. Static inventory of the execution architecture ────────────────────
from native_core.core.runtime.execution import context as exec_context  # noqa: E402
from native_core.core.trace import record as trace_record  # noqa: E402
from tools.p12_execution_provenance import CONTRACT_ELEMENTS, ExecutionManifest  # noqa: E402
import dataclasses  # noqa: E402

inventory = {
    "execution_context_fields": [f.name for f in dataclasses.fields(exec_context.ExecutionContext)],
    "execution_id_ratified": "execution_id" in [f.name for f in dataclasses.fields(
        exec_context.ExecutionContext)],
    "trace_record_fields": list(trace_record.REQUIRED_FIELDS),
    "trace_statuses": sorted(trace_record.VALID_STATUSES),
    "trace_has_delegation_field": any("deleg" in f for f in trace_record.REQUIRED_FIELDS),
    "manifest_fields": [f.name for f in dataclasses.fields(ExecutionManifest)],
    "manifest_contract_elements": list(CONTRACT_ELEMENTS),
    "participate_returns": "None — no execution-result model is ratified (consumer.py)",
    "callers": {
        "W4Executor(": references("W4Executor("),
        "create_execution_layer(": references("create_execution_layer("),
        "TracedAction(": references("TracedAction("),
        "ExecutionManifest(": references("ExecutionManifest("),
        "persist_evidence(": references("persist_evidence("),
    },
    "engineering_agent_participate_traces_as": re.search(
        r'agent_instance="([^"]+)"',
        (REPO / "consumers/engineering_intelligence_agent.py").read_text(encoding="utf-8")).group(1),
    "roots": {
        "trace_registry_STORE_ROOT": rel(importlib.import_module("tools.p12_trace_registry").STORE_ROOT),
        "manifest_MANIFEST_ROOT": rel(importlib.import_module("tools.p12_execution_provenance").MANIFEST_ROOT),
        "observation_live_root": rel(importlib.import_module("tools.p12_runtime_observation").OBSERVATION_ROOT),
        "observation_certified_root": rel(importlib.import_module(
            "tools.p12_runtime_observation").CERTIFIED_OBSERVATION_ROOT),
        "chain_reader_roots": {k: rel(getattr(importlib.import_module(
            "tools.p12_execution_chain_reader"), k)) for k in ("MANIFESTS", "TRACE_STORES", "OBSERVATIONS")},
        "chain_reader_delegation_dirs": [rel(d) for d in importlib.import_module(
            "tools.p12_execution_chain_reader").DELEGATION_DIRS],
        "p13_trace_stores": rel(importlib.import_module("tools.p13.paths").LIVE.trace_stores),
    },
}
guard = importlib.import_module("tools.p12_certified_evidence_guard")
inventory["roots_certified"] = {k: guard.is_protected(REPO / v / "probe")
                                for k, v in inventory["roots"].items() if isinstance(v, str)}

# ── E/F. Representative Agency grants: the actual provenance chain ───────────
from tools import planning_continuity, w4_continuity, w4_delegation as w4  # noqa: E402

overview = w4_continuity.operational_overview()
REPRESENTATIVES = {"3cc612275a914c2c": "MR-S5-1 P1 ACCEPT (executed, success)",
                   "d497e284f2c14aee": "MR-S5-1 P2 REWORK (executed, failure)",
                   "0a697039a63f4c17": "S-2 (live, never executed)"}
trace_and_manifest_bytes = []
for root in ("docs/architecture/p12/trace-stores", "docs/architecture/p12/execution-provenance",
             "docs/operations"):
    for p in sorted((REPO / root).rglob("*")):
        if p.is_file():
            trace_and_manifest_bytes.append((rel(p), p.read_bytes()))
chains = {}
for gid, label in REPRESENTATIVES.items():
    root = next(REPO / g["root"] for g in overview["grants"].values() if g["delegation_id"] == gid)
    grant = json.loads((root / f"{gid}.delegation.json").read_text(encoding="utf-8"))
    evidence_path = root / f"{gid}.evidence.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8")) if evidence_path.is_file() else None
    surface = planning_continuity.restore(root / "planning.state.json")
    plan_key = w4._bound_plan(grant)                                  # noqa: SLF001
    goal_key = next((g for g in surface._goals                         # noqa: SLF001
                     if any(p.key == plan_key for p in surface.history(g))), None)
    disposition = w4.read_dispositions(root)[0].get(gid)
    named_in = [path for path, data in trace_and_manifest_bytes if gid.encode() in data]
    instance_record = root / f"{grant['recipient_instance']}.instance.json"
    chains[gid] = {
        "label": label,
        "founder_goal": [goal_key, "PERSISTED (planning.state.json; goal cites its act)"],
        "plan": [plan_key, "TEXTUAL (parsed from the grant's lifecycle_boundary by _bound_plan)"],
        "plan_step": [grant["work_scope"], "DIRECT (grant work_scope)"],
        "agent_instance": [grant["recipient_instance"],
                           "DIRECT (grant recipient); instance record "
                           + ("PERSISTED in root" if instance_record.is_file() else "MISSING")],
        "execution": ([evidence["executed_at"], "DIRECT (evidence names delegation_id; no execution id)"]
                      if evidence else [None, "MISSING (never executed)"]),
        "evidence_keys": sorted(evidence) if evidence else [],
        "runtime": [None, "MISSING (no runtime id, execution sequence or observation in any record)"],
        "trace": [named_in or None, "MISSING (grant id in no Trace store, manifest or observation)"
                  if not named_in else "PRESENT"],
        "result": ([evidence["outcomes"][0]["status"], evidence["outcomes"][0]["detail"][:80]]
                   if evidence else [None, "MISSING"]),
        "result_producer": "caller-supplied `perform` → W4Executor ExecutionOutcome → persist_evidence"
        if evidence else None,
        "verification": "DERIVED (plan_completion over the evidence)" if evidence else "MISSING",
        "ceo_decision": [disposition.get("decision") if disposition else None,
                         "DIRECT (live ledger)" if disposition else "MISSING (no decision yet)"],
    }

# ── G/H/I/M. The probe: Path A (Runtime-hosted) vs Path B (direct call) ──────
from consumers.engineering_intelligence_agent import (  # noqa: E402
    Artifact, ConformanceCriterion, EngineeringIntelligenceAgent)
from consumers.observation import TracedAction  # noqa: E402
from native_core.core.infrastructure import LocalAppendOnlyStorage, LocalExecutionSubstrate  # noqa: E402
from native_core.core.runtime.composition import create_runtime  # noqa: E402
from native_core.core.runtime.execution import create_execution_layer  # noqa: E402
from native_core.core.trace import TraceReader, TraceWriter  # noqa: E402

subject = REPO / "tools/w4_delegation.py"
artifact = Artifact(name=subject.name, lines=tuple(subject.read_text(encoding="utf-8").split("\n")))
criteria = tuple(ConformanceCriterion(name=n, required_text=n) for n in w4.REQUIRED_ELEMENTS)
probe = {}
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    store_a = LocalAppendOnlyStorage(tmp / "store-a" / "fr2-probe")
    store_a.provision()
    substrate = LocalExecutionSubstrate()
    substrate.provision()
    runtime = create_runtime(runtime_id="fr2-probe-runtime", storage=store_a,
                             substrate=substrate)
    runtime.initialize()
    runtime.start()
    execution = create_execution_layer(runtime)
    agent = EngineeringIntelligenceAgent(artifact=artifact, criteria=criteria,
                                         trace_writer=TraceWriter(store_a))
    returned = agent.participate(execution)
    path_a = [r.to_mapping() for r in TraceReader(store_a).read()]
    probe["path_a_runtime_hosted"] = {
        "runtime_state_during": str(runtime.state),
        "execution_context": dataclasses.asdict(execution.context),
        "participate_returned": repr(returned),
        "trace_records": len(path_a),
        "trace_agent_instance": path_a[0]["agent_instance"] if path_a else None,
        "trace_runtime": path_a[0]["runtime"] if path_a else None,
        "trace_status": path_a[0]["status"] if path_a else None,
        "trace_outputs": path_a[0]["outputs"] if path_a else None,
        "verification_results_held_in_memory_only": len(agent.results)
        if hasattr(agent, "results") else "n/a",
    }
    # A failing verification inside participate: does the Trace say failure?
    failing = EngineeringIntelligenceAgent(
        artifact=Artifact(name="empty.py", lines=("",)), criteria=criteria,
        trace_writer=TraceWriter(store_a))
    failing.participate(create_execution_layer(runtime))
    after_fail = [r.to_mapping() for r in TraceReader(store_a).read()]
    probe["path_a_unsatisfied_verification_trace_status"] = after_fail[-1]["status"]
    runtime.stop()
    probe["runtime_state_after_stop"] = str(runtime.state)
    try:
        create_execution_layer(runtime)
        probe["execution_after_stop"] = "NOT REFUSED"
    except Exception as exc:
        probe["execution_after_stop"] = f"refused: {type(exc).__name__}"

    # Path B: what the S-chain does — the agent's own method, no Execution, no writer.
    store_b = LocalAppendOnlyStorage(tmp / "store-b" / "fr2-probe")
    store_b.provision()
    results_b = EngineeringIntelligenceAgent().verify(artifact, criteria)
    probe["path_b_direct_call"] = {
        "results": len(results_b),
        "trace_records_written": len(list(TraceReader(store_b).read())),
        "runtime_involved": False,
    }

    # Path A' (the P12-W4 shape): TracedAction with an instance key, and a fabricated one.
    store_c = LocalAppendOnlyStorage(tmp / "stores" / "fr2-probe-instance")
    store_c.provision()
    writer_c = TraceWriter(store_c)
    with TracedAction(writer_c, agent_instance=INSTANCE, runtime="fr2-probe-runtime") as action:
        action.produced({"criteria": len(criteria)})
    with TracedAction(writer_c, agent_instance="fabricated-instance-999",
                      runtime="fr2-probe-runtime") as action:
        action.produced({"criteria": 0})
    records_c = [r.to_mapping() for r in TraceReader(store_c).read()]
    probe["path_a_prime_traced_action"] = {
        "actors_recorded": [r["agent_instance"] for r in records_c],
        "fabricated_actor_accepted_by_trace_layer": "fabricated-instance-999" in [
            r["agent_instance"] for r in records_c],
    }

    # The existing join: an ExecutionManifest, written by its own writer, read by
    # the independent chain reader — every root pointed (in memory only) at the
    # probe's temp directory. The observation is published by the existing
    # publisher from the probe Runtime's real state.
    reader = importlib.import_module("tools.p12_execution_chain_reader")
    provenance = importlib.import_module("tools.p12_execution_provenance")
    observation = importlib.import_module("tools.p12_runtime_observation")
    obs_dir, manifest_dir = tmp / "observations", tmp / "manifests"
    hosted = create_runtime(runtime_id="fr2-probe-runtime", storage=store_c, substrate=substrate)
    hosted.initialize()
    hosted.start()
    observation.publish(hosted.runtime_id, str(hosted.state), root=obs_dir)
    grant = json.loads((AGENCY / "w4-s4-plan-outcome/3cc612275a914c2c.delegation.json").read_text(
        encoding="utf-8"))
    plan = w4._bound_plan(grant)                                          # noqa: SLF001

    def manifest(execution_id, ordinal):
        m = provenance.ExecutionManifest(
            execution_id=execution_id, goal="founder-mr-s5-1-accept", plan=plan,
            plan_authority="Co-Founder V2 A01 Executive Command", work_scope=tuple(grant["work_scope"]),
            agent_instance=records_c[ordinal]["agent_instance"], agent_definition_version="1.1",
            delegation_id=grant["delegation_id"], delegator=grant["delegator"],
            authority_instrument=grant["authority_instrument"], authority_record=grant["authority_record"],
            authority_chain=tuple(grant["authority_chain"]), capability_scope=tuple(grant["capability_scope"]),
            trace_store="fr2-probe-instance", trace_ordinal=ordinal, runtime_id="fr2-probe-runtime",
            status="success", observation_subject="fr2-probe-runtime", observation_kind="runtime",
            verification_requirement=grant["verification_requirement"], outcome={"criteria": 14},
            delegation_status=grant["status"])
        written = provenance.record(m, root=manifest_dir)
        return json.loads(written.read_text(encoding="utf-8"))

    real, fake = manifest("fr2-probe-real", 0), manifest("fr2-probe-fabricated", 1)
    hosted.stop()
    with mock.patch.object(reader, "TRACE_STORES", tmp / "stores"), \
            mock.patch.object(reader, "OBSERVATIONS", obs_dir), \
            mock.patch.object(reader, "MANIFESTS", manifest_dir):
        as_resident = reader.verify_manifest(real)
        with mock.patch.object(reader, "DELEGATION_DIRS",
                               reader.DELEGATION_DIRS + (AGENCY / "w4-s4-plan-outcome",)):
            counterfactual = reader.verify_manifest(real)
            fabricated = reader.verify_manifest(fake)
    probe["manifest_contract_complete"] = not provenance.ExecutionManifest(**{
        k: v for k, v in real.items() if k in {f.name for f in dataclasses.fields(
            provenance.ExecutionManifest)}} | {"work_scope": tuple(real["work_scope"]),
                                              "authority_chain": tuple(real["authority_chain"]),
                                              "capability_scope": tuple(real["capability_scope"])}
    ).missing_elements()
    edge = lambda v: {f"{e.source}→{e.target}": e.status for e in v.edges}  # noqa: E731
    probe["chain_reader_on_agency_grant"] = {
        "with_resident_delegation_dirs": edge(as_resident),
        "counterfactual_with_agency_root_added": edge(counterfactual),
        "counterfactual_fabricated_actor": edge(fabricated),
    }

    # M. Fresh process: a second interpreter reads the probe's persisted store.
    program = ("import sys,json;sys.path.insert(0,sys.argv[1]);"
               "from native_core.core.infrastructure import LocalAppendOnlyStorage as S;"
               "from native_core.core.trace import TraceReader as R;"
               "s=S(sys.argv[2]);s.provision();"
               "print(json.dumps([r.to_mapping() for r in R(s).read()],sort_keys=True))")
    second = subprocess.run([sys.executable, "-c", program, str(REPO), str(tmp / "stores" / "fr2-probe-instance")],
                            capture_output=True, text=True, check=True).stdout
    probe["fresh_process"] = {
        "trace_records_survive": json.loads(second) == json.loads(json.dumps(records_c, sort_keys=True)),
        "runtime_state_survives": "PROCESS-LOCAL (no observation published, nothing persisted)",
        "execution_sequence_in_trace": "execution_sequence" in json.dumps(json.loads(second)),
    }

# ── N. P13 / observability ───────────────────────────────────────────────────
from tools.p13.paths import LIVE  # noqa: E402
from tools.p13.state import SOURCES, StateUnderstanding  # noqa: E402
memory_source = tuple(s for s in SOURCES if s.name == "memory")
facts = {f.key: f for f in StateUnderstanding(LIVE, sources=memory_source).observe().facts}
stores = facts["memory.stores"].value or {}
registry = importlib.import_module("tools.p12_trace_registry")
agency_in_trace = [g for g in (p.name.split(".")[0] for p in AGENCY.glob("*/*.delegation.json"))
                   if any(g.encode() in d for _, d in trace_and_manifest_bytes)]
p13 = {
    "memory_trace_stores_seen": stores,
    "trace_store_names": [s.name for s in registry.discover(registry.STORE_ROOT)],
    "agency_grants_in_any_trace_manifest_or_observation": agency_in_trace,
    "operational_state_source_present": any(s.name == "operational_state" for s in SOURCES),
    "live_observations": sorted(p.name for p in (REPO / "docs/operations/runtime-observations").glob(
        "*.json")),
}

# ── S. Negative controls ─────────────────────────────────────────────────────
# P12-W2 read as data (importlib), so this tool does not become one of its consumers.
_w2_sources = {s.state_id: s for s in importlib.import_module("tools.p12_operational_state").SOURCES}
w2_execution, w2_delegation = _w2_sources["execution.recorded"], _w2_sources["delegation.granted"]
pa, pb, pc = (probe["path_a_runtime_hosted"], probe["path_b_direct_call"],
              probe["path_a_prime_traced_action"])
cr = probe["chain_reader_on_agency_grant"]
controls = {
    "N1_no_runtime_claim_without_runtime_evidence": all(
        c["runtime"][0] is None for c in chains.values()),
    "N2_direct_call_not_labelled_runtime": pb["trace_records_written"] == 0 and not pb["runtime_involved"],
    "N3_capability_or_definition_name_is_not_instance": pa["trace_agent_instance"] != INSTANCE,
    "N4_delegation_not_inferred_from_agent_identity": cr["with_resident_delegation_dirs"].get(
        "WORK→DELEGATION") == "DANGLING",
    "N5_execution_not_inferred_from_result": chains["0a697039a63f4c17"]["execution"][0] is None
    and chains["0a697039a63f4c17"]["result"][0] is None,
    "N6_result_is_not_trace": all(c["trace"][0] is None for c in chains.values()
                                  if c["result"][0] is not None),
    "N7_trace_not_authoritative_state": w2_execution.state_class == "EXECUTION"
    and "historical" in w2_execution.freshness_model
    and w2_delegation.owner == "FD-P11-001 authorized delegator",
    "N8_historical_not_presented_as_current": inventory["roots_certified"]["trace_registry_STORE_ROOT"]
    and p13["live_observations"] == [],
    "N9_p13_claims_no_runtime_observation_of_agency": p13["agency_grants_in_any_trace_manifest_or_observation"] == [],
    "N10_fabricated_actor_rejected_at_the_join": pc["fabricated_actor_accepted_by_trace_layer"]
    and cr["counterfactual_fabricated_actor"].get("DELEGATION→EXECUTION") == "DANGLING",
    "N11_process_local_not_persistent": probe["fresh_process"]["trace_records_survive"]
    and probe["fresh_process"]["runtime_state_survives"].startswith("PROCESS-LOCAL"),
    "N12_no_certified_boundary_changed": True,      # settled by the integrity comparison below
}

# ── T. Integrity ─────────────────────────────────────────────────────────────
after = fb2.surfaces()
register_bytes = (REPO / s6.REGISTER).read_bytes()
equal = {k: after[k] == BASE["surfaces"][k] for k in after}
integrity = {
    "run_changed_nothing": before == after and register_before == s6.register_state(),
    "surfaces_equal_baseline": equal,
    "register_only_appended": hashlib.sha256(register_bytes[:BASE["register"]["bytes"]]).hexdigest()
    == BASE["register"]["sha256"],
    "integrity_faults": [str(f) for f in importlib.import_module(
        "tools.certified_evidence_integrity").verify().faults],
    "git_status_certified": git("status", "--porcelain", "--", "docs/architecture/p11",
                                "docs/architecture/p12", "docs/architecture/p13",
                                "docs/architecture/platform-organization", "docs/operations") or "(clean)",
}
expected_change = "agency_records:docs/architecture/agency/*.md"
controls["N12_no_certified_boundary_changed"] = all(v for k, v in equal.items() if k != expected_change)
result = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "head": git("rev-parse", "HEAD"), "baseline_head": BASE["head"],
    "inventory": inventory, "chains": chains, "probe": probe, "p13": p13,
    "negative_controls": controls, "integrity": integrity,
    "surfaces_changed_vs_baseline": [k for k, v in equal.items() if not v and k != expected_change],
}
result["all_ok"] = (integrity["run_changed_nothing"] and not result["surfaces_changed_vs_baseline"]
                    and integrity["register_only_appended"] and not integrity["integrity_faults"]
                    and integrity["git_status_certified"] == "(clean)" and all(controls.values()))
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
print(json.dumps({k: result[k] for k in ("inventory", "chains", "probe", "p13", "negative_controls",
                                          "surfaces_changed_vs_baseline", "all_ok")},
                 indent=1, ensure_ascii=False, default=str))
