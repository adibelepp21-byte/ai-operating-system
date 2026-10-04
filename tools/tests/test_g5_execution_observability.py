"""FR-2 G5 (`FD-FR2-002`) — Agency execution observed through P12-W2, by P13.

The path is Agency Runtime / Trace → P12-W2 execution projection → P13, and
never Agency Runtime / Trace → P13. Two kinds of test:

* **Sandboxed** — the projection over temporary live roots, populated by the
  real Runtime-hosted path, to attack each property `§4`, `§5` and `§9` name;
* **On the repository** — the FR-2 execution (`2adef08b8efa4549`) as P12-W2
  projects it and as P13 receives it, including in a fresh process.
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import ExitStack
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from tools import p12_execution_chain_reader as chain
from tools import p12_execution_provenance as prov
from tools import p12_operational_state as w2
from tools import p12_runtime_observation as obs
from tools import p12_trace_registry as traces
from tools import w4_delegation as w4
from tools import w4_runtime_execution as rx
from tools.agent_instance_registry import AgentInstanceRegistry
from tools.planning import AuthorityProvenance, PlanStep
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION
# The root binding (`agency_runtime_execution.py`) joins the two regions; this
# suite reaches the participant only through it, as the FR-2 suite does.
import agency_runtime_execution as arx

REPO = Path(__file__).resolve().parents[2]
INSTANCE = "engineering-intelligence-instance-001"
GRANT = "2adef08b8efa4549"
EXECUTION = f"agency-{GRANT}-verify-runtime-path-mechanisms"
BASE = json.loads((REPO / "docs/architecture/agency/evidence/G5-BASELINE-2026-10-04.json")
                  .read_text(encoding="utf-8"))


def _entries():
    return {e.state_id: e for e in w2.project()}


def _projected(state_id):
    """One declared source, projected by its own projector."""
    source = next(s for s in w2.SOURCES if s.state_id == state_id)
    return w2._PROJECTIONS[state_id](source)  # noqa: SLF001


def _live():
    return _projected("execution.provenance").value["live"]


class _LiveSandbox(unittest.TestCase):
    """Empty live roots in a temp dir, with every reader pointed at them."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        t = Path(self._tmp.name)
        self.ops = t / "agency/operations/w4-g5"
        self.stores = t / "trace-stores"
        self.store = self.stores / rx.AGENCY_TRACE_STORE
        self.manifests = t / "execution-provenance"
        self.observations = t / "runtime-observations"
        for p in (self.stores, self.manifests, self.observations):
            p.mkdir(parents=True)
        stack = ExitStack()
        self.addCleanup(stack.close)
        for target, name, value in (
                (prov, "LIVE_MANIFEST_ROOT", self.manifests),
                (traces, "LIVE_STORE_ROOT", self.stores),
                (chain, "LIVE_MANIFESTS", self.manifests),
                (chain, "LIVE_TRACE_STORES", self.stores),
                (chain, "LIVE_OBSERVATIONS", self.observations),
                (chain, "AGENCY_OPERATIONS", t / "agency/operations"),
                (obs, "OBSERVATION_ROOT", self.observations)):
            stack.enter_context(mock.patch.object(target, name, value))
        self.registry = AgentInstanceRegistry(None)
        self.registry.register(
            instance_key=INSTANCE, definition=SELECTED_DEFINITION,
            permitted_capabilities=("engineering-intelligence",),
            created_by=w4.AUTHORIZED_DELEGATOR,
            authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
            accountable_to=w4.AUTHORIZED_DELEGATOR)
        self.grant = w4.W4DelegationRegistry(self.registry, self.ops).issue(
            delegator=w4.AUTHORIZED_DELEGATOR, recipient_instance=INSTANCE,
            authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD), objective="g5",
            capability_scope=("engineering-intelligence",), work_scope=("s1",),
            lifecycle_boundary="one execution of plan g5-plan-0", resource_boundary="none",
            output_expectation="one result", verification_requirement="reported",
            escalation_condition="out of scope", accountable_party=w4.AUTHORIZED_DELEGATOR,
            termination_condition="on completion of plan g5-plan-0")

    def execute(self, runtime_id="g5-runtime", perform=lambda s: "done", record=True):
        with rx.hosted_runtime(runtime_id, observation_root=self.observations) as runtime:
            hosted = arx.hosted_executor(self.grant, self.registry, runtime,
                                         rx.trace_writer(self.store),
                                         store_path=self.store).execute_step(
                PlanStep("s1", "the step", requires_delegation=True), perform)
        if record:
            rx.record_manifest(hosted, self.grant, goal="g5-goal", plan="g5-plan-0",
                               plan_authority="CEO (record)", agent_definition_version="1.0",
                               outcome={"status": hosted.outcome.status}, root=self.manifests)
        return hosted

    def observe(self, runtime_id, state="RuntimeState.RUNNING", age=0):
        obs.publish(runtime_id, state, root=self.observations, kind=obs.RUNTIME)
        if age:
            path = next(self.observations.glob(f"{runtime_id}*.json"))
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["observed_at"] = (datetime.now(timezone.utc)
                                      - timedelta(seconds=age)).isoformat()
            path.write_text(json.dumps(payload), encoding="utf-8")


class TheProjectionObservesAgencyExecution(_LiveSandbox):
    """`§4`: everything P13 needs, read through P12-W2."""

    def test_a_completed_execution_carries_the_whole_observation_model(self):
        self.execute()
        live = _live()
        self.assertEqual(len(live["executions"]), 1)
        e = live["executions"][0]
        self.assertEqual((e["agent_instance"], e["delegation_id"], e["origin"]),
                         (INSTANCE, self.grant.delegation_id, w2.LIVE_ORIGIN))
        self.assertEqual(e["runtime"]["runtime_id"], "g5-runtime")
        self.assertTrue(e["runtime"]["observed"])
        self.assertEqual(e["runtime"]["classification"], obs.TERMINATED)
        self.assertTrue(e["trace"]["joined"])
        self.assertTrue(e["result"]["available"])
        self.assertEqual(e["result"]["status"], "success")
        self.assertEqual(e["provenance"], chain.JOINED)
        self.assertTrue(e["valid_agency_execution"])
        self.assertEqual(e["temporal"], w2.HISTORICAL)
        self.assertTrue(e["completed"])
        self.assertEqual(live["completed"], [e["execution_id"]])
        self.assertEqual(live["active"], [])

    def test_a_failed_execution_is_observed_with_its_outcome(self):
        def fails(step):
            raise AssertionError("unsatisfied")
        self.execute(perform=fails)
        e = _live()["executions"][0]
        self.assertEqual(e["result"]["status"], "failure")
        self.assertTrue(e["valid_agency_execution"])

    def test_an_execution_whose_runtime_is_live_is_current(self):
        self.execute()
        self.observe("g5-runtime")                         # the Runtime observed live again
        live = _live()
        self.assertEqual(live["executions"][0]["temporal"], w2.CURRENT)
        self.assertFalse(live["executions"][0]["completed"])
        self.assertEqual(live["active"], [live["executions"][0]["execution_id"]])
        # A live Runtime that a manifest names is that execution's Runtime, not
        # an unbound one: it is reported once, as the execution's.
        self.assertEqual(live["unbound_live_runtimes"], [])


class NegativeControls(_LiveSandbox):
    """`§9` N3–N6, N8: the projection asserts nothing its owners did not persist."""

    def test_n3_no_manifest_means_no_execution(self):
        self.execute(record=False)                         # Runtime + Trace, no manifest
        self.assertEqual(_live()["executions"], [])

    def test_n3_a_manifest_whose_trace_is_missing_is_not_a_valid_execution(self):
        self.execute()
        (self.store / "trace").write_text("", encoding="utf-8")
        e = _live()["executions"][0]
        self.assertFalse(e["trace"]["joined"])
        self.assertEqual(e["provenance"], chain.DANGLING)
        self.assertFalse(e["valid_agency_execution"])
        self.assertEqual(_live()["completed"], [])

    def test_n4_a_stale_runtime_is_not_presented_as_current(self):
        self.execute()
        self.observe("g5-runtime", age=3600)
        e = _live()["executions"][0]
        self.assertEqual(e["runtime"]["classification"], obs.STALE)
        self.assertEqual(e["temporal"], w2.HISTORICAL)
        self.assertEqual(_live()["active"], [])

    def test_n5_a_result_without_runtime_and_trace_is_not_runtime_execution(self):
        """Agency evidence written by the direct path is not projected."""
        rx.W4Executor(self.grant, self.registry).execute_step(
            PlanStep("s1", "x", requires_delegation=True), lambda s: "direct")
        self.assertEqual(_live()["executions"], [])

    def test_n6_a_runtime_without_instance_provenance_is_not_an_agency_execution(self):
        self.observe("some-unbound-runtime")
        live = _live()
        self.assertEqual(live["executions"], [])
        self.assertEqual(live["active"], [])
        self.assertEqual(live["unbound_live_runtimes"], ["some-unbound-runtime"])

    def test_n6_a_fabricated_actor_does_not_make_a_valid_execution(self):
        self.execute()
        trace = self.store / "trace"
        trace.write_text(trace.read_text(encoding="utf-8").replace(
            f'"{INSTANCE}"', '"fabricated-instance-999"'), encoding="utf-8")
        e = _live()["executions"][0]
        self.assertFalse(e["valid_agency_execution"])
        self.assertEqual(e["edges"]["DELEGATION→EXECUTION"], chain.DANGLING)

    def test_n8_live_executions_never_enter_the_certified_counts(self):
        before = {k: v for k, v in _projected("execution.provenance").value.items()
                  if k != "live"}
        self.execute()
        after = {k: v for k, v in _projected("execution.provenance").value.items()
                 if k != "live"}
        self.assertEqual(before, after)
        self.assertEqual(after["origin"], w2.CERTIFIED_ORIGIN)


class P13ReceivesItThroughP12W2(unittest.TestCase):
    """`§6` / `§8` 5–6, N1, N2, N9."""

    P13 = sorted((REPO / "tools/p13").glob("*.py"))

    def test_p13_maps_the_projection_and_nothing_else(self):
        from tools.p13 import state as p13_state
        self.assertEqual(p13_state.OPERATIONAL_STATE_KEYS["execution.provenance"],
                         "operational_state.executions")
        source = next(s for s in p13_state.SOURCES if s.name == "operational_state")
        self.assertIn("operational_state.executions", source.keys)

    def test_n1_n2_p13_opens_no_agency_trace_or_runtime_store(self):
        forbidden_modules = ("p12_runtime_observation", "p12_execution_chain_reader",
                             "p12_execution_provenance", "w4_runtime_execution",
                             "agency_runtime_execution")
        forbidden_text = ("operations/trace-stores", "operations/runtime-observations",
                          "operations/execution-provenance", "LIVE_STORE_ROOT",
                          "LIVE_MANIFEST_ROOT", "OBSERVATION_ROOT", "verify_live")
        for path in self.P13:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
            modules = {n.module or "" for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)} \
                | {f"{n.module}.{a.name}" for n in ast.walk(tree)
                   if isinstance(n, ast.ImportFrom) for a in n.names} \
                | {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
            self.assertFalse([m for m in modules if any(f in m for f in forbidden_modules)],
                             path.name)
            self.assertFalse([t for t in forbidden_text if t in source], path.name)

    def test_n1_p13_memory_still_reads_only_the_certified_trace_stores(self):
        from tools.p13.paths import LIVE
        self.assertEqual(LIVE.trace_stores, traces.STORE_ROOT)
        self.assertNotIn(rx.AGENCY_TRACE_STORE,
                         [s.name for s in traces.discover(LIVE.trace_stores)])

    def test_n9_no_second_execution_state_authority(self):
        self.assertEqual(len(w2.SOURCES), 8)
        self.assertFalse([c for c in w2.conflicts() if c["kind"] == "CONFLICT"])
        self.assertFalse(any(e.is_authority() for e in w2.project()))
        from tools.p13 import state as p13_state
        readers = [s.name for s in p13_state.SOURCES
                   if any("execution" in k for k in s.keys)]
        self.assertEqual(readers, ["operational_state"])

    def test_the_consumer_measurement_still_agrees(self):
        from tools import p12_consumer_evidence_verifier as independent
        from tools import p12_state_verification as sv
        surface = "tools.p12_operational_state"
        consumers, importers = sv.consumers_of(surface), sv.importers_of(surface)
        self.assertIn("tools/p13/state.py", consumers)
        summary = independent.summary(consumers, importers)
        self.assertEqual(summary["disagrees"], 0, summary["not_agreeing"])
        self.assertIn("tools/p13/state.py", summary["observed_consumers"])


class OnTheRepository(unittest.TestCase):
    """The FR-2 execution as P12-W2 projects it and P13 receives it."""

    def test_p12_w2_projects_the_fr2_execution_and_keeps_certified_counts(self):
        value = _entries()["execution.provenance"].value
        base = BASE["certified_readers"]["p12_w2"]["execution.provenance"][1]
        self.assertEqual((value["manifests"], value["statuses"]),
                         (base["manifests"], base["statuses"]))
        e = {x["execution_id"]: x for x in value["live"]["executions"]}[EXECUTION]
        self.assertEqual((e["delegation_id"], e["agent_instance"], e["provenance"],
                          e["temporal"], e["completed"]),
                         (GRANT, INSTANCE, chain.JOINED, w2.HISTORICAL, True))
        recorded = _entries()["execution.recorded"].value
        rbase = BASE["certified_readers"]["p12_w2"]["execution.recorded"][1]
        self.assertEqual({k: recorded[k] for k in rbase}, rbase)
        self.assertIn(rx.AGENCY_TRACE_STORE, recorded["live"]["store_names"])

    def test_p13_receives_it_through_p12_w2(self):
        from tools.p13 import state as p13_state
        from tools.p13.paths import LIVE
        source = next(s for s in p13_state.SOURCES if s.name == "operational_state")
        facts = {f.key: f for f in
                 p13_state.StateUnderstanding(LIVE, sources=(source,)).observe().facts}
        fact = facts["operational_state.executions"]
        self.assertEqual(fact.status, p13_state.VERIFIED)
        self.assertIn("P12-W2 execution.provenance", fact.source)
        self.assertIn(EXECUTION, [e["execution_id"] for e in fact.value["live"]["executions"]])

    def test_n10_fr1_operational_state_is_unchanged(self):
        from tools.p13 import state as p13_state
        from tools.p13.paths import LIVE
        source = next(s for s in p13_state.SOURCES if s.name == "operational_state")
        facts = {f.key: f for f in
                 p13_state.StateUnderstanding(LIVE, sources=(source,)).observe().facts}
        for key in ("operational_state.delegations", "operational_state.escalations"):
            was = BASE["p13_operational_state"][key]
            now = json.loads(json.dumps([facts[key].status, facts[key].value,
                                         facts[key].source], sort_keys=True, default=str))
            self.assertEqual(now, was, key)

    def test_the_fr2_chain_is_still_seven_of_seven(self):
        verdict = {v.execution_id: v for v in chain.verify_live()}[EXECUTION]
        self.assertTrue(verdict.joined)
        self.assertEqual(len(verdict.edges), 7)

    def test_p13_receives_it_in_a_fresh_process(self):
        probe = ("import sys,json;sys.path.insert(0,%r);import tools;"
                 "from tools.p13.paths import LIVE;from tools.p13.state import SOURCES,StateUnderstanding;"
                 "s=StateUnderstanding(LIVE,sources=tuple(x for x in SOURCES if x.name=='operational_state')).observe();"
                 "f={x.key:x for x in s.facts}['operational_state.executions'];"
                 "print(json.dumps([f.status,[e['execution_id'] for e in f.value['live']['executions']]]))"
                 ) % str(REPO)
        out = json.loads(subprocess.run([sys.executable, "-c", probe], cwd=REPO, check=True,
                                        capture_output=True, text=True).stdout)
        self.assertEqual(out[0], "VERIFIED")
        self.assertIn(EXECUTION, out[1])


if __name__ == "__main__":
    unittest.main()
