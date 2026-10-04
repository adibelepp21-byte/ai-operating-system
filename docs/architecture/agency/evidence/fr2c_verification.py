"""FR-2 construction (FD-FR2-001) verification, in a fresh process. READ-ONLY.

Checks every item of `FD-FR2-001 §12` against what is on disk, compares the
certified readers and surfaces with `FR2C-BASELINE-2026-10-04.json` (captured
before any code changed), and separates the **data** this construction was
expected to add from **certified** semantics, which must not move. Loads P12-W2
by name (the disclosed verifier pattern), so it never enters the P12 consumer
measurement it reads. Writes only ``FR2C-VERIFICATION-2026-10-04.json``.
"""
import ast
import hashlib
import importlib
import json
import subprocess
import sys
import tempfile
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
import fr2c_baseline as base  # noqa: E402

OUT = HERE / "FR2C-VERIFICATION-2026-10-04.json"
BASE = json.loads((HERE / "FR2C-BASELINE-2026-10-04.json").read_text(encoding="utf-8"))
S4 = REPO / "docs/architecture/agency/operations/w4-s4-plan-outcome"
RUN = json.loads((S4 / "fr2-runtime-run.result.json").read_text(encoding="utf-8"))
GRANT = RUN["log"]["grant"]
GOAL = RUN["log"]["goal"]


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True).stdout.strip()


normal = base.normal
surfaces_before = fr2.surfaces()

from native_core.core.infrastructure import LocalAppendOnlyStorage  # noqa: E402
from native_core.core.runtime import RuntimeNotRunning  # noqa: E402
from native_core.core.trace import TraceReader  # noqa: E402
from tools import authority_citation as ac  # noqa: E402
from tools import p12_execution_chain_reader as chain  # noqa: E402
from tools import p12_execution_provenance as provenance  # noqa: E402
from tools import p12_runtime_observation as observation  # noqa: E402
from tools import p12_trace_registry as traces  # noqa: E402
from tools import planning_continuity, w4_continuity  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402
from tools import w4_runtime_execution as rx  # noqa: E402
from tools.agent_instance_registry import AgentInstanceRegistry  # noqa: E402
from tools.planning import AuthorityProvenance, PlanStep  # noqa: E402
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION  # noqa: E402
# The root binding of both regions, read by name (the disclosed verifier
# pattern): a static import from here would count this evidence tool as the
# system reaching a runtime in `p12_runtime_verification.reachability()`.
arx = importlib.import_module("agency_runtime_execution")

grant = json.loads((S4 / f"{GRANT}.delegation.json").read_text(encoding="utf-8"))
evidence = json.loads((S4 / f"{GRANT}.evidence.json").read_text(encoding="utf-8"))
instance = json.loads((S4 / f"{grant['recipient_instance']}.instance.json").read_text(encoding="utf-8"))
manifest_path = REPO / evidence["runtime"]["execution_manifest"]
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
runtime = evidence["runtime"]
storage = LocalAppendOnlyStorage(traces.LIVE_STORE_ROOT / runtime["trace_store"])
storage.provision()
trace = tuple(TraceReader(storage).read())[runtime["trace_ordinal"]]
observed = {o.runtime_id: o for o in observation.observations(observation.OBSERVATION_ROOT)}
surface = planning_continuity.restore(S4 / "planning.state.json")
goal = surface._goals[GOAL]  # noqa: SLF001
plan = surface.current(GOAL)
met, evidence_path, reasons = w4.plan_completion(S4, grant)
outcome = w4.plan_outcome(surface, GOAL, S4)
dispositions, faults = w4.read_dispositions(S4)
disposition = dispositions.get(GRANT, {})
live_verdict = chain.verify_manifest(manifest, chain.LIVE)
fresh = json.loads(subprocess.run(
    [sys.executable, "-c",
     "import sys,json;sys.path.insert(0,%r);import tools;"
     "from tools import p12_execution_chain_reader as c;"
     "print(json.dumps([[v.execution_id,v.status,v.origin,[e.status for e in v.edges]]"
     " for v in c.verify_live()]))" % str(REPO)],
    cwd=REPO, capture_output=True, text=True, check=True).stdout)


def bypass_probe():
    """A stopped Runtime executes nothing, and a non-Execution is refused."""
    calls = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        registry = AgentInstanceRegistry(None)
        registry.register(instance_key=grant["recipient_instance"], definition=SELECTED_DEFINITION,
                          permitted_capabilities=("engineering-intelligence",),
                          created_by=w4.AUTHORIZED_DELEGATOR,
                          authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
                          accountable_to=w4.AUTHORIZED_DELEGATOR)
        sandbox = w4.W4DelegationRegistry(registry, tmp / "ops").issue(
            delegator=w4.AUTHORIZED_DELEGATOR, recipient_instance=grant["recipient_instance"],
            authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD), objective="probe",
            capability_scope=("engineering-intelligence",), work_scope=("s1",),
            lifecycle_boundary="one execution of plan probe-0", resource_boundary="none",
            output_expectation="none", verification_requirement="none",
            escalation_condition="none", accountable_party=w4.AUTHORIZED_DELEGATOR,
            termination_condition="on completion of plan probe-0")
        store = tmp / "store"
        with rx.hosted_runtime("probe-runtime", observation_root=tmp / "obs") as rt:
            executor = arx.hosted_executor(sandbox, registry, rt, rx.trace_writer(store),
                                           store_path=store)
        try:
            executor.execute_step(PlanStep("s1", "x", requires_delegation=True),
                                  lambda s: calls.append(s) or "x")
            stopped = "executed"
        except RuntimeNotRunning:
            stopped = "refused: RuntimeNotRunning"
        w4x = rx.W4Executor(sandbox, registry)
        one = PlanStep("s1", "x", requires_delegation=True)
        step = arx.PARTICIPANT(lambda action: w4x.execute_step(one, action),
                               grant["recipient_instance"], lambda s: calls.append(s) or "x",
                               rx.trace_writer(store), "1.0")
        try:
            step.participate(object())
            imitation = "accepted"
        except TypeError:
            imitation = "refused: TypeError"
        return {"stopped_runtime": stopped, "imitation_execution": imitation,
                "perform_calls": len(calls)}


source = (REPO / "agency_runtime_execution.py").read_text(encoding="utf-8")
authority_side = (REPO / "tools/w4_runtime_execution.py").read_text(encoding="utf-8")
perform_sites = sum(1 for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute) and n.func.attr == "_perform") \
    + sum(1 for n in ast.walk(ast.parse(authority_side)) if isinstance(n, ast.Call)
          and isinstance(n.func, ast.Name) and n.func.id == "perform")
probe = bypass_probe()
readers_now = base.certified_readers()
before = BASE["certified_readers"]
measurement = normal(cb.consumer_measurement())


def mutated_actor(actor):
    """The real live chain with only the Trace actor replaced, on a copy."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        stores = tmp / "stores" / runtime["trace_store"]
        stores.mkdir(parents=True)
        lines = (traces.LIVE_STORE_ROOT / runtime["trace_store"] / "trace").read_text(
            encoding="utf-8").splitlines()
        lines[runtime["trace_ordinal"]] = lines[runtime["trace_ordinal"]].replace(
            json.dumps(grant["recipient_instance"]), json.dumps(actor))
        (stores / "trace").write_text("\n".join(lines) + "\n", encoding="utf-8")
        original = chain.LIVE_TRACE_STORES
        chain.LIVE_TRACE_STORES = tmp / "stores"
        try:
            verdict = chain.verify_manifest(manifest, chain.LIVE)
        finally:
            chain.LIVE_TRACE_STORES = original
        return {e.target: e.status for e in verdict.edges}["EXECUTION"]


def runtime_observed_delta():
    was = before["p12_w2"]["runtime.observed"][1]
    now = readers_now["p12_w2"]["runtime.observed"][1]
    return {"added_terminated": sorted(set(now["terminated"]) - set(was["terminated"])),
            "removed": sorted(set(was["terminated"]) - set(now["terminated"])),
            "live": now["live"], "observations": [was["observations"], now["observations"]]}


section_12 = {
    "runtime": {
        "agency_work_entered_runtime": runtime["runtime_id"] == f"agency-runtime-{GRANT}"
        and isinstance(runtime["execution_sequence"], int)
        and observed.get(runtime["runtime_id"]) is not None
        and observed[runtime["runtime_id"]].origin == observation.LIVE_ORIGIN,
        "runtime_participation_evidenced": trace.runtime == runtime["runtime_id"]
        == manifest["runtime_id"] == manifest["observation_subject"],
        "direct_bypass_prevented": perform_sites == 1 and probe == {
            "stopped_runtime": "refused: RuntimeNotRunning",
            "imitation_execution": "refused: TypeError", "perform_calls": 0},
    },
    "trace": {
        "produced_by_existing_mechanism": "TracedAction(" in source and trace.status == "success",
        "identifies_actual_agent_instance": trace.agent_instance == grant["recipient_instance"]
        == instance["instance_key"] and trace.agent_instance != instance["definition_key"],
        "associated_with_execution": (manifest["trace_store"], manifest["trace_ordinal"])
        == (runtime["trace_store"], runtime["trace_ordinal"]),
        "associated_with_runtime_observation": trace.runtime in observed,
    },
    "manifest": {
        "produced_by_existing_mechanism": manifest_path.parent == provenance.LIVE_MANIFEST_ROOT
        and set(manifest) - {"contract_elements"}
        == set(provenance.ExecutionManifest.__dataclass_fields__),
        "relationships_reconstructable": manifest["goal"] == GOAL and manifest["plan"] == plan.key
        and manifest["delegation_id"] == GRANT
        and manifest["agent_instance"] == grant["recipient_instance"]
        and live_verdict.joined,
    },
    "provenance": {
        "founder_goal": ac.founder_goal_refusal(goal.authority.instrument, goal.authority.record,
                                                goal.statement) is None,
        "plan": plan.key in grant["lifecycle_boundary"] and plan.goal_key == GOAL,
        "plan_step": grant["work_scope"][0] in [s.key for s in plan.steps],
        "delegation": grant["delegation_id"] == GRANT
        and grant["authority_instrument"] == "FD-P11-001 §9",
        "agent_instance": instance["lifecycle"] == "REGISTERED"
        and instance["instance_key"] == grant["recipient_instance"],
        "execution": [o["status"] for o in evidence["outcomes"]] == ["success"]
        and evidence["delegation_id"] == GRANT,
        "runtime": evidence["runtime"]["runtime_id"] in observed,
        "trace": trace.agent_instance == evidence["agent_instance"],
        "result": evidence["outcomes"][0]["detail"] == manifest["outcome"]["detail"]
        and all(evidence["criteria"].values()),
        "verification": met and evidence_path.name == f"{GRANT}.evidence.json",
        "ceo_decision": disposition.get("decision") == w4.ACCEPT
        and disposition.get("disposition") == w4.COMPLETED and not faults,
        "plan_outcome": outcome["completed"] and not outcome["decision_faults"],
        "fresh_process_chain": [manifest["execution_id"], chain.JOINED, chain.LIVE,
                                [chain.JOINED] * 7] in fresh,
    },
    "observability": {
        "existing_readers_observe_live_agency_execution": live_verdict.joined
        and runtime["trace_store"] in [s.name for s in traces.discover_by_origin()[traces.LIVE_ORIGIN]],
        "certified_historical_distinguishable": readers_now["chain_summary"] == before["chain_summary"]
        and readers_now["chain_verdicts"] == before["chain_verdicts"]
        and readers_now["trace_registry_certified"] == before["trace_registry_certified"]
        and readers_now["manifests_certified"] == before["manifests_certified"]
        and {v.origin for v in chain.verify_all()} == {chain.CERTIFIED},
        # P13 gains no source and no state authority: neither P13 nor P12-W2 code
        # changed, P12-W2's declared contract is identical, and its execution
        # projections (certified stores) read exactly as before.
        "p13_no_second_state_authority": git("diff", BASE["head"], "--", "tools/p13",
                                             "tools/p12_operational_state.py") == ""
        and readers_now["p12_w2_sources"] == before["p12_w2_sources"]
        and all(readers_now["p12_w2"][k] == before["p12_w2"][k]
                for k in ("execution.recorded", "execution.provenance")),
        # `runtime.observed` has read the live observation root since GOAL-V2-002,
        # so the Agency runtime appears there as data: one more observation, the
        # Agency runtime TERMINATED, nothing LIVE, every earlier entry unchanged.
        "p12_w2_runtime_observed_change_is_data_only": runtime_observed_delta()
        == {"added_terminated": [runtime["runtime_id"]], "removed": [], "live": [],
            "observations": [before["p12_w2"]["runtime.observed"][1]["observations"],
                             before["p12_w2"]["runtime.observed"][1]["observations"] + 1]},
    },
    "negative_controls": {
        "direct_execution_cannot_masquerade": probe["perform_calls"] == 0
        and not chain.verify_manifest(dict(manifest, trace_ordinal=99), chain.LIVE).joined,
        "fabricated_instance_fails_provenance": mutated_actor("fabricated-instance-999")
        == chain.DANGLING,
        "definition_cannot_substitute_for_instance": mutated_actor(instance["definition_key"])
        == chain.DANGLING,
        "no_hidden_p13_or_reader_dependency": measurement == normal(BASE["consumer_measurement"]),
        # `certified:docs/operations` is excluded by name: the TD baseline groups the
        # live root with the certified ones for change detection, but `docs/operations`
        # is live state (its README; the barrier does not protect it), and this
        # construction writes there by design. The certified evidence roots are the rest.
        "certified_evidence_not_mutated": all(
            surfaces_before[k] == BASE["surfaces"][k] for k in BASE["surfaces"]
            if (k.startswith("certified:") and k != "certified:docs/operations")
            or k.startswith("store:docs/architecture")),
        "live_cannot_silently_become_certified": not chain.verify_manifest(manifest).joined
        and manifest["execution_id"] not in readers_now["manifests_certified"],
    },
}
residual = {
    "G3_runtime_state_process_local": "the Runtime object is not reconstructable after the "
    "process; what persists is its observation (state, origin live) and, in the evidence and "
    "manifest, its id and the execution sequence. Runtime persistence was not redesigned",
    "G5_p13_execution_visibility": {
        "p12_w2_execution_recorded_read_path": [s[1] for s in readers_now["p12_w2_sources"]
                                                if s[0] == "execution.recorded"][0],
        "p13_trace_stores": str(importlib.import_module("tools.p13.paths").LIVE.trace_stores
                                .relative_to(REPO)),
        "agency_execution_visible_to_p13": False},
    "G6_native_participate_status": "consumers/engineering_intelligence_agent.py unchanged: "
    + str(git("diff", BASE["head"], "--", "consumers/engineering_intelligence_agent.py") == ""),
    "G7_escalation_producer": {
        "traced_action_unchanged": git("diff", BASE["head"], "--", "consumers/observation.py") == "",
        "status_is_success_or_failure_only": 'status = "failure" if (exc_type is not None or '
        'self._failed) else "success"' in (REPO / "consumers/observation.py").read_text(encoding="utf-8"),
        "escalation_produced": False},
}
changed_code = sorted(set(git("diff", "--name-only", BASE["head"], "--", "tools", "native_core",
                              "consumers", "api", "fullstack").splitlines()
                          + git("ls-files", "--others", "--exclude-standard", "tools", "consumers",
                                "native_core", "agency_runtime_execution.py").splitlines()))
surfaces_after = fr2.surfaces()
data_changes = sorted(k for k in BASE["surfaces"] if surfaces_before[k] != BASE["surfaces"][k])
result = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "head": git("rev-parse", "HEAD"), "baseline_head": BASE["head"],
    "grant": GRANT, "execution_id": manifest["execution_id"],
    "section_12": section_12,
    "live_edges": [[e.source, e.target, e.status] for e in live_verdict.edges],
    "bypass_probe": probe,
    "residual_gaps": residual,
    "surfaces_changed_vs_baseline": data_changes,
    "changed_code": changed_code,
    "certified_readers_now": {k: readers_now[k] for k in (
        "chain_summary", "trace_registry_certified", "manifests_certified", "live_roots_present")},
    "live_summary": normal(chain.live_summary()),
    "run_changed_nothing": surfaces_before == surfaces_after,
    "integrity_faults": [str(f) for f in importlib.import_module(
        "tools.certified_evidence_integrity").verify().faults],
    "git_status_certified": git("status", "--porcelain", "--", "docs/architecture/p10",
                                "docs/architecture/p11", "docs/architecture/p12",
                                "docs/architecture/p13", "docs/architecture/platform-organization")
    or "(clean)",
}
expected_changes = {"agency_records:docs/architecture/agency/*.md", "operational:agency/operations",
                    "code:tools", "p12_state:tools/p12_*.py",
                    # The Agent side and its binding: one new root module,
                    # `agency_runtime_execution.py`, outside the served tree.
                    "root_entry_points:*.py",
                    "runtime_trace_code:tools+consumers", "store:docs/operations/runtime-observations",
                    "certified:docs/operations"}
result["unexpected_surface_changes"] = sorted(set(data_changes) - expected_changes)
# New code is added, never substituted: no existing native_core / consumers file
# changed, and the only root entry point added is the binding.
result["existing_core_and_consumers_unchanged"] = git(
    "diff", "--diff-filter=MDR", "--name-only", BASE["head"], "--", "native_core", "consumers") == ""
result["root_entry_points_added"] = sorted(set(
    git("ls-files", "--others", "--exclude-standard", "--", "*.py").splitlines()
    + git("diff", "--diff-filter=A", "--name-only", BASE["head"], "--", ".").splitlines())
    & {p.name for p in REPO.glob("*.py")})
result["all_ok"] = (all(all(v.values()) for v in section_12.values())
                    and not result["unexpected_surface_changes"]
                    and result["existing_core_and_consumers_unchanged"]
                    and result["root_entry_points_added"] == ["agency_runtime_execution.py"]
                    and result["run_changed_nothing"] and not result["integrity_faults"]
                    and result["git_status_certified"] == "(clean)")
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
print(json.dumps({k: result[k] for k in ("section_12", "surfaces_changed_vs_baseline",
                                          "unexpected_surface_changes", "changed_code",
                                          "existing_core_and_consumers_unchanged",
                                          "root_entry_points_added",
                                          "run_changed_nothing", "integrity_faults",
                                          "git_status_certified", "all_ok")}, indent=1, default=str))
