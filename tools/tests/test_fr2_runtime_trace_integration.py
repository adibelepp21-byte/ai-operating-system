"""FR-2 (`FD-FR2-001`) — delegated Agency work through the existing Runtime path.

Two kinds of test:

* **Sandboxed** — the integration and the readers, on temporary roots: each one
  drives the real Runtime, Execution Layer, `TracedAction`, `ExecutionManifest`
  writer and chain reader, and attacks one property `§12` requires.
* **On the repository** — the one authorized execution
  (`docs/architecture/agency/evidence/fr2_runtime_execution_run.py`), read back
  from persisted bytes: Founder Goal → … → Plan Outcome.
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from native_core.core.runtime import RuntimeNotRunning
from native_core.core.trace import TraceReader
from native_core.core.infrastructure import LocalAppendOnlyStorage

from tools import p12_certified_evidence_guard as sentinel
from tools import p12_execution_chain_reader as chain
from tools import p12_execution_provenance as provenance
from tools import p12_trace_registry as traces
from tools import planning_continuity
from tools import w4_delegation as w4
from tools import w4_runtime_execution as rx
# The root composition module binds the Agent side (`consumers/`) to the
# authority side (`tools/`); neither region may import the other, and this
# suite, under `tools/`, reaches the participant only through the binding, as
# the corpus-health suites reach `aios_corpus_health_run`.
import agency_runtime_execution as arx
from tools.agent_instance_registry import AgentInstanceRegistry
from tools.planning import AuthorityProvenance, Plan, PlanStep
from tools.w4_execution import ESCALATION, FAILURE, SUCCESS, ExecutionRefused
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION

REPO = Path(__file__).resolve().parents[2]
INSTANCE = "engineering-intelligence-instance-001"
DEFINITION_KEY = SELECTED_DEFINITION.agent_definition_key
S4 = REPO / "docs/architecture/agency/operations/w4-s4-plan-outcome"
RUN = json.loads((S4 / "fr2-runtime-run.result.json").read_text(encoding="utf-8"))
GRANT = RUN["log"]["grant"]
CERTIFIED_SUMMARY = {"manifests": 5, "joined": 5, "dangling": 0, "unresolved": 0,
                     "edges_per_chain": 7, "not_joined": ()}


def _records(store: Path):
    storage = LocalAppendOnlyStorage(store)
    storage.provision()
    return tuple(TraceReader(storage).read())


class _Sandbox(unittest.TestCase):
    """A registered instance, a grant bound to a plan, and live roots in a temp dir."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.ops = self.tmp / "agency/operations/w4-fr2"
        self.store = self.tmp / "trace-stores" / rx.AGENCY_TRACE_STORE
        self.manifests = self.tmp / "execution-provenance"
        self.observations = self.tmp / "runtime-observations"
        self.registry = AgentInstanceRegistry(None)
        self.registry.register(
            instance_key=INSTANCE, definition=SELECTED_DEFINITION,
            permitted_capabilities=("engineering-intelligence",),
            created_by=w4.AUTHORIZED_DELEGATOR,
            authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
            accountable_to=w4.AUTHORIZED_DELEGATOR)
        self.grant = self.issue(INSTANCE)
        for patch in (mock.patch.object(chain, "LIVE_MANIFESTS", self.manifests),
                      mock.patch.object(chain, "LIVE_TRACE_STORES", self.store.parent),
                      mock.patch.object(chain, "LIVE_OBSERVATIONS", self.observations),
                      mock.patch.object(chain, "AGENCY_OPERATIONS", self.tmp / "agency/operations")):
            patch.start()
            self.addCleanup(patch.stop)

    def tearDown(self):
        self._tmp.cleanup()

    def issue(self, recipient, scope=("s1",), registry=None):
        return w4.W4DelegationRegistry(registry or self.registry, self.ops).issue(
            delegator=w4.AUTHORIZED_DELEGATOR, recipient_instance=recipient,
            authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD), objective="fr2 sandbox",
            capability_scope=("engineering-intelligence",), work_scope=scope,
            lifecycle_boundary="one execution of plan fr2-plan-0", resource_boundary="none",
            output_expectation="one result", verification_requirement="the step reported",
            escalation_condition="out of scope", accountable_party=w4.AUTHORIZED_DELEGATOR,
            termination_condition="on completion of plan fr2-plan-0")

    def host(self, runtime, grant=None):
        return arx.hosted_executor(grant or self.grant, self.registry, runtime,
                                        rx.trace_writer(self.store), store_path=self.store)

    def runtime(self, runtime_id="fr2-sandbox-runtime"):
        return rx.hosted_runtime(runtime_id, observation_root=self.observations)

    def run_and_record(self, perform=lambda s: "done", runtime_id="fr2-sandbox-runtime"):
        with self.runtime(runtime_id) as runtime:
            hosted = self.host(runtime).execute_step(
                PlanStep("s1", "the step", requires_delegation=True), perform)
        path = rx.record_manifest(
            hosted, self.grant, goal="fr2-goal", plan="fr2-plan-0",
            plan_authority="CEO (record)", agent_definition_version="1.0",
            outcome={"status": hosted.outcome.status}, root=self.manifests)
        return hosted, json.loads(path.read_text(encoding="utf-8"))


class RuntimeParticipation(_Sandbox):
    """`§12` Runtime: Agency work actually enters the Runtime."""

    def test_the_step_runs_inside_a_runtime_issued_execution(self):
        seen = {}
        with self.runtime("rt-a") as runtime:
            def perform(step):
                seen["state"] = str(runtime.state)
                return "done"
            hosted = self.host(runtime).execute_step(
                PlanStep("s1", "x", requires_delegation=True), perform)
        self.assertEqual(seen["state"], "RuntimeState.RUNNING")
        self.assertEqual((hosted.runtime_id, hosted.execution_sequence), ("rt-a", 0))
        self.assertEqual(hosted.outcome.status, SUCCESS)

    def test_each_step_is_a_fresh_execution_with_the_runtimes_sequence(self):
        grant = self.issue(INSTANCE, scope=("s1", "s2"))
        with self.runtime() as runtime:
            plan = Plan(key="fr2-plan-0", goal_key="g", authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
                        steps=(PlanStep("s1", "a", requires_delegation=True),
                               PlanStep("s2", "b", requires_delegation=True,
                                        depends_on=("s1",))))
            report, hosted = self.host(runtime, grant).execute_plan(plan, lambda s: s.key)
        self.assertEqual([h.execution_sequence for h in hosted], [0, 1])
        self.assertEqual([o.status for o in report.outcomes], [SUCCESS, SUCCESS])

    def test_the_runtime_is_observed_while_running_and_when_stopped(self):
        from tools import p12_runtime_observation as obs
        with self.runtime("rt-o"):
            running = obs.observations(self.observations)
        stopped = obs.observations(self.observations)
        self.assertEqual([o.state for o in running], ["RuntimeState.RUNNING"])
        self.assertEqual([o.state for o in stopped], ["RuntimeState.STOPPED"])


class NoBypass(_Sandbox):
    """`§12`: direct function-call bypass is prevented for the authorized path."""

    def test_a_stopped_runtime_executes_nothing(self):
        calls = []
        with self.runtime() as runtime:
            executor = self.host(runtime)
        with self.assertRaises(RuntimeNotRunning):
            executor.execute_step(PlanStep("s1", "x", requires_delegation=True),
                                  lambda s: calls.append(s) or "x")
        self.assertEqual(calls, [])
        self.assertFalse((self.store / "trace").exists()
                         and _records(self.store))

    def test_the_participant_accepts_only_a_real_execution(self):
        calls = []
        executor = rx.W4Executor(self.grant, self.registry)
        step = PlanStep("s1", "x", requires_delegation=True)
        participant = arx.PARTICIPANT(lambda action: executor.execute_step(step, action),
                                      INSTANCE, lambda s: calls.append(s) or "x",
                                      rx.trace_writer(self.store), "1.0")

        class Imitation:
            context = type("C", (), {"runtime_id": "fake", "execution_sequence": 0})()
        with self.assertRaises(TypeError):
            participant.participate(Imitation())
        self.assertEqual(calls, [])

    def test_a_participant_that_is_not_an_agent_is_refused(self):
        calls = []

        def impostor(run_step, *args):
            class Direct:
                def participate(self, execution):
                    run_step(lambda s: calls.append(s) or "x")
            return Direct()
        with self.runtime() as runtime, self.assertRaises(TypeError):
            rx.RuntimeHostedExecutor(self.grant, self.registry, runtime,
                                     rx.trace_writer(self.store), participant=impostor,
                                     store_path=self.store).execute_step(
                PlanStep("s1", "x", requires_delegation=True), lambda s: "x")
        self.assertEqual(calls, [])

    def test_perform_is_called_only_inside_the_traced_action(self):
        """Static: the authority side never calls the work; the Agent calls it
        once, inside its `TracedAction`."""
        tools_tree = ast.parse((REPO / "tools/w4_runtime_execution.py").read_text(encoding="utf-8"))
        self.assertFalse([n for n in ast.walk(tools_tree) if isinstance(n, ast.Call)
                          and isinstance(n.func, ast.Name) and n.func.id == "perform"])
        agent_tree = ast.parse((REPO / "agency_runtime_execution.py").read_text(encoding="utf-8"))
        calls = [n for n in ast.walk(agent_tree) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Attribute) and n.func.attr == "_perform"]
        self.assertEqual(len(calls), 1)
        withs = [n for n in ast.walk(agent_tree) if isinstance(n, ast.With)
                 and "TracedAction" in ast.unparse(n.items[0].context_expr)]
        self.assertEqual(len(withs), 1)
        self.assertIn(calls[0], list(ast.walk(withs[0])))

    def test_the_served_tree_is_unchanged(self):
        """`FD-FR2-001 §11`: deployment stays paused, so FR-2 adds nothing the
        deployment serves (`fullstack/readiness.py` `SERVED_PATHS`)."""
        from fullstack.readiness import SERVED_PATHS
        added = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "--",
                                *SERVED_PATHS], cwd=REPO, capture_output=True,
                               text=True).stdout.split()
        self.assertEqual(added, [])
        changed = subprocess.run(["git", "diff", "--name-only", "2571089", "--",
                                  *SERVED_PATHS], cwd=REPO, capture_output=True,
                                 text=True).stdout.split()
        self.assertEqual(changed, [])
        self.assertNotIn("agency_runtime_execution.py", " ".join(SERVED_PATHS))

    def test_the_two_regions_do_not_import_each_other(self):
        for relative, forbidden in (("tools/w4_runtime_execution.py", "consumers"),):
            tree = ast.parse((REPO / relative).read_text(encoding="utf-8"))
            modules = {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)} \
                | {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
            self.assertFalse([m for m in modules if m and m.startswith(forbidden)], relative)

    def test_a_direct_run_leaves_nothing_a_chain_can_join(self):
        """A plain `W4Executor` call writes no Trace, so no manifest of it can join."""
        outcome = rx.W4Executor(self.grant, self.registry).execute_step(
            PlanStep("s1", "x", requires_delegation=True), lambda s: "direct")
        self.assertEqual(outcome.status, SUCCESS)
        self.assertEqual(traces.discover(self.store.parent), ())
        forged = {"execution_id": "forged", "goal": "fr2-goal", "plan": "fr2-plan-0",
                  "plan_authority": "x", "work_scope": ["s1"],
                  "delegation_id": self.grant.delegation_id,
                  "trace_store": rx.AGENCY_TRACE_STORE, "trace_ordinal": 0,
                  "observation_subject": "fr2-sandbox-runtime",
                  "verification_requirement": "x", "outcome": {}}
        verdict = chain.verify_manifest(forged, chain.LIVE)
        self.assertFalse(verdict.joined)
        statuses = {e.target: e.status for e in verdict.edges}
        self.assertEqual(statuses["EXECUTION"], chain.DANGLING)
        self.assertEqual(statuses["OBSERVATION"], chain.DANGLING)


class TraceIdentity(_Sandbox):
    """`§6` / `§12` Trace: produced by the existing mechanism, naming the instance."""

    def test_one_record_per_step_under_the_recipient_instance_and_runtime(self):
        hosted, _ = self.run_and_record(runtime_id="rt-t")
        records = _records(self.store)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].agent_instance, INSTANCE)
        self.assertNotEqual(records[0].agent_instance, DEFINITION_KEY)
        self.assertEqual(records[0].runtime, "rt-t")
        self.assertEqual(hosted.trace_ordinal, 0)

    def test_a_refused_step_is_not_traced_and_is_escalated_by_the_plan(self):
        with self.runtime() as runtime:
            executor = self.host(runtime)
            with self.assertRaises(ExecutionRefused):
                executor.execute_step(PlanStep("outside", "x", requires_delegation=True),
                                      lambda s: "x")
            plan = Plan(key="fr2-plan-0", goal_key="g", authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
                        steps=(PlanStep("outside", "x", requires_delegation=True),))
            report, hosted = executor.execute_plan(plan, lambda s: "x")
        self.assertEqual([o.status for o in report.outcomes], [ESCALATION])
        self.assertEqual(hosted, ())
        self.assertFalse((self.store / "trace").is_file() and _records(self.store))

    def test_the_hosted_run_path_makes_refusals_organizational_escalations(self):
        """`ACT-CC-P11-015` / `ACT-CC-P12-005`: through the one existing wiring."""
        from tools.escalation_register import EscalationRegister
        plan = Plan(key="fr2-plan-0", goal_key="g",
                    authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
                    steps=(PlanStep("s1", "in scope", requires_delegation=True),
                           PlanStep("outside", "out of scope", requires_delegation=True,
                                    depends_on=("s1",))))
        with self.runtime() as runtime:
            report, hosted, escalations = arx.run_hosted_plan(
                self.grant, self.registry, runtime, rx.trace_writer(self.store), plan,
                lambda s: "done", root=self.ops, authority_record=FD_RECORD,
                store_path=self.store)
        self.assertEqual([o.status for o in report.outcomes], [SUCCESS, ESCALATION])
        self.assertEqual(len(hosted), 1)
        self.assertEqual(len(escalations), 1)
        recorded = EscalationRegister(self.ops).load(escalations[0])
        self.assertIn(self.grant.delegation_id, json.dumps(recorded))
        self.assertEqual(len(_records(self.store)), 1)

    def test_failure_uses_the_existing_mapping(self):
        def fails(step):
            raise AssertionError("criteria unsatisfied")
        hosted, _ = self.run_and_record(perform=fails)
        self.assertEqual(hosted.outcome.status, FAILURE)
        self.assertEqual(_records(self.store)[0].status, "failure")

    def test_a_retired_instance_is_refused_before_any_trace(self):
        self.registry.retire(INSTANCE)
        with self.runtime() as runtime, self.assertRaises(ExecutionRefused):
            self.host(runtime).execute_step(PlanStep("s1", "x", requires_delegation=True),
                                            lambda s: "x")
        self.assertFalse((self.store / "trace").is_file() and _records(self.store))


class ManifestAndChain(_Sandbox):
    """`§7` / `§12` Manifest and Provenance, verified by the independent reader."""

    def test_the_hosted_execution_joins_all_seven_edges_live(self):
        _, payload = self.run_and_record()
        verdict = chain.verify_manifest(payload, chain.LIVE)
        self.assertTrue(verdict.joined, [(e.target, e.detail) for e in verdict.edges
                                         if e.status != chain.JOINED])
        self.assertEqual(verdict.origin, chain.LIVE)
        self.assertEqual([v.execution_id for v in chain.verify_live()], [payload["execution_id"]])

    def test_the_manifest_uses_the_existing_schema_only(self):
        _, payload = self.run_and_record()
        fields = {f.name for f in provenance.ExecutionManifest.__dataclass_fields__.values()}
        self.assertEqual(set(payload) - {"contract_elements"}, fields)

    def test_a_definition_key_or_fabricated_actor_does_not_join(self):
        _, payload = self.run_and_record()
        line = (self.store / "trace").read_text(encoding="utf-8").splitlines()[0]
        for actor in (DEFINITION_KEY, "fabricated-instance-999"):
            (self.store / "trace").write_text(
                line.replace(f'"{INSTANCE}"', f'"{actor}"') + "\n", encoding="utf-8")
            verdict = chain.verify_manifest(payload, chain.LIVE)
            edge = [e for e in verdict.edges if e.target == "EXECUTION"][0]
            self.assertEqual(edge.status, chain.DANGLING, actor)

    def test_a_fabricated_instance_cannot_be_delegated_to(self):
        with self.assertRaises(Exception):
            self.issue("fabricated-instance-999")

    def test_a_live_manifest_is_not_completed_by_certified_roots(self):
        _, payload = self.run_and_record()
        verdict = chain.verify_manifest(payload)          # certified origin
        self.assertFalse(verdict.joined)
        self.assertEqual(verdict.origin, chain.CERTIFIED)

    def test_a_certified_manifest_is_not_completed_by_live_roots(self):
        certified = dict(provenance.manifests()[0])
        self.assertTrue(chain.verify_manifest(certified).joined)
        self.assertFalse(chain.verify_manifest(certified, chain.LIVE).joined)


class LiveCertifiedSeparation(unittest.TestCase):
    """`§4` / `§5`: live data stays live, certified populations stay as certified."""

    def test_certified_population_and_verdicts_are_as_certified(self):
        self.assertEqual(chain.summary(), CERTIFIED_SUMMARY)
        self.assertEqual({v.origin for v in chain.verify_all()}, {chain.CERTIFIED})
        self.assertNotIn(GRANT, json.dumps([v.execution_id for v in chain.verify_all()]))

    def test_the_live_population_is_identified_as_live(self):
        live = chain.verify_live()
        self.assertEqual({v.origin for v in live}, {chain.LIVE})
        self.assertEqual(chain.live_summary()["origin"], chain.LIVE)

    def test_resident_reader_defaults_still_read_certified_roots(self):
        self.assertEqual(traces.what_has_run(), traces.what_has_run(traces.STORE_ROOT))
        self.assertNotIn(rx.AGENCY_TRACE_STORE, traces.what_has_run()["store_names"])
        self.assertEqual(provenance.manifests(), provenance.manifests(provenance.MANIFEST_ROOT))
        by_origin = traces.discover_by_origin()
        self.assertIn(rx.AGENCY_TRACE_STORE, [s.name for s in by_origin[traces.LIVE_ORIGIN]])
        self.assertNotIn(rx.AGENCY_TRACE_STORE,
                         [s.name for s in by_origin[traces.CERTIFIED_ORIGIN]])

    def test_live_data_cannot_be_written_as_certified(self):
        with self.assertRaises(sentinel.CertifiedEvidenceProtected):
            rx.trace_writer(traces.STORE_ROOT / rx.AGENCY_TRACE_STORE)
        payload = json.loads(next(provenance.LIVE_MANIFEST_ROOT.glob("*.manifest.json"))
                             .read_text(encoding="utf-8"))
        payload.pop("contract_elements")
        payload["execution_id"] = "fr2-certified-attempt"
        for key in ("work_scope", "authority_chain", "capability_scope"):
            payload[key] = tuple(payload[key])
        with self.assertRaises(sentinel.CertifiedEvidenceProtected):
            provenance.record(provenance.ExecutionManifest(**payload))
        self.assertFalse((provenance.MANIFEST_ROOT / "fr2-certified-attempt.manifest.json").exists())

    def test_the_trace_writer_refuses_before_touching_storage(self):
        """The guard, not only the process-wide barrier, refuses a certified store."""
        with mock.patch.object(rx, "LocalAppendOnlyStorage") as storage, \
                self.assertRaises(sentinel.CertifiedEvidenceProtected):
            rx.trace_writer(traces.STORE_ROOT / rx.AGENCY_TRACE_STORE)
        storage.assert_not_called()

    def test_live_roots_are_outside_every_certified_root(self):
        for root in (traces.LIVE_STORE_ROOT, provenance.LIVE_MANIFEST_ROOT,
                     chain.LIVE_MANIFESTS, chain.LIVE_TRACE_STORES, chain.LIVE_OBSERVATIONS):
            self.assertFalse(sentinel.is_protected(root / "x.json"), root)
        self.assertEqual(chain.LIVE_MANIFESTS, provenance.LIVE_MANIFEST_ROOT)
        self.assertEqual(chain.LIVE_TRACE_STORES, traces.LIVE_STORE_ROOT)


class NoHiddenConsumer(unittest.TestCase):
    """`§10` / `§12`: no hidden P12-W2 or P13 dependency, no second state authority."""

    MODULES = ("tools/w4_runtime_execution.py", "agency_runtime_execution.py",
               "docs/architecture/agency/evidence/fr2_runtime_execution_run.py")

    def test_the_integration_imports_nothing_from_p12_w2_or_p13(self):
        for relative in self.MODULES:
            tree = ast.parse((REPO / relative).read_text(encoding="utf-8"))
            names = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    names.add(node.module or "")
                    names.update(f"{node.module}.{a.name}" for a in node.names)
                elif isinstance(node, ast.Import):
                    names.update(a.name for a in node.names)
            self.assertFalse([n for n in names if "p12_operational_state" in n
                              or n.startswith("tools.p13")], relative)

    def test_the_consumer_measurement_is_unchanged(self):
        from tools import p12_state_verification as sv
        surface = "tools.p12_operational_state"
        self.assertEqual(len(sv.consumers_of(surface)), 4)
        self.assertEqual(len(sv.importers_of(surface)), 5)
        for relative in self.MODULES:
            self.assertNotIn(relative, sv.importers_of(surface))

    def test_p13_is_not_wired_to_agency_execution(self):
        p13 = "".join(p.read_text(encoding="utf-8") for p in sorted((REPO / "tools/p13").glob("*.py")))
        for name in ("w4_runtime_execution", "operations/trace-stores",
                     "operations/execution-provenance", "verify_live"):
            self.assertNotIn(name, p13)
        from tools.p13.paths import LIVE
        self.assertEqual(LIVE.trace_stores, traces.STORE_ROOT)


class TheAuthorizedExecution(unittest.TestCase):
    """The one authorized Agency execution, read back from persisted bytes."""

    @classmethod
    def setUpClass(cls):
        cls.grant = json.loads((S4 / f"{GRANT}.delegation.json").read_text(encoding="utf-8"))
        cls.evidence = json.loads((S4 / f"{GRANT}.evidence.json").read_text(encoding="utf-8"))
        cls.manifest_path = REPO / RUN["log"]["manifest"]
        cls.manifest = json.loads(cls.manifest_path.read_text(encoding="utf-8"))

    def test_founder_goal_to_plan_to_step_to_delegation_to_instance(self):
        from tools import authority_citation as ac
        surface = planning_continuity.restore(S4 / "planning.state.json")
        goal = surface._goals["founder-fr2-runtime-trace"]  # noqa: SLF001
        self.assertIsNone(ac.founder_goal_refusal(goal.authority.instrument,
                                                  goal.authority.record, goal.statement))
        self.assertIn("FD-FR2-001", goal.authority.record)
        plan = surface.current("founder-fr2-runtime-trace")
        self.assertIn(plan.key, self.grant["lifecycle_boundary"])
        self.assertEqual(self.grant["work_scope"], ["verify-runtime-path-mechanisms"])
        self.assertEqual(self.grant["recipient_instance"], INSTANCE)
        self.assertEqual(self.grant["authority_instrument"], "FD-P11-001 §9")

    def test_execution_to_runtime_to_trace_to_manifest(self):
        runtime = self.evidence["runtime"]
        self.assertEqual(runtime["runtime_id"], f"agency-runtime-{GRANT}")
        self.assertEqual(self.manifest["runtime_id"], runtime["runtime_id"])
        self.assertEqual((self.manifest["trace_store"], self.manifest["trace_ordinal"]),
                         (runtime["trace_store"], runtime["trace_ordinal"]))
        self.assertEqual(REPO / runtime["execution_manifest"], self.manifest_path)
        record = _records(traces.LIVE_STORE_ROOT / runtime["trace_store"])[runtime["trace_ordinal"]]
        self.assertEqual((record.agent_instance, record.runtime, record.status),
                         (INSTANCE, runtime["runtime_id"], "success"))

    def test_the_independent_reader_joins_every_edge(self):
        verdict = chain.verify_manifest(self.manifest, chain.LIVE)
        self.assertTrue(verdict.joined, [(e.target, e.detail) for e in verdict.edges
                                         if e.status != chain.JOINED])
        self.assertIn(self.manifest["execution_id"],
                      [v.execution_id for v in chain.verify_live() if v.joined])

    def test_result_to_verification_to_ceo_decision_to_plan_outcome(self):
        met, path, reasons = w4.plan_completion(S4, self.grant)
        self.assertTrue(met, reasons)
        self.assertEqual(path.name, f"{GRANT}.evidence.json")
        surface = planning_continuity.restore(S4 / "planning.state.json")
        outcome = w4.plan_outcome(surface, "founder-fr2-runtime-trace", S4)
        self.assertTrue(outcome["completed"])
        self.assertEqual(outcome["decision_faults"], [])
        decisions = json.dumps(outcome)
        self.assertIn(GRANT, decisions)
        self.assertIn("ACCEPT", decisions)

    def test_the_chain_reconstructs_in_a_fresh_process(self):
        probe = ("import sys,json;sys.path.insert(0,%r);import tools;"
                 "from tools import p12_execution_chain_reader as c;"
                 "print(json.dumps([[v.execution_id,v.status,v.origin] for v in c.verify_live()]))"
                 ) % str(REPO)
        out = json.loads(subprocess.run([sys.executable, "-c", probe], cwd=REPO, check=True,
                                        capture_output=True, text=True).stdout)
        self.assertIn([self.manifest["execution_id"], chain.JOINED, chain.LIVE], out)

    def test_the_grant_is_no_longer_current(self):
        from tools import w4_continuity
        overview = w4_continuity.operational_overview()
        grant = overview["grants"][f"{S4.relative_to(REPO).as_posix()}/{GRANT}"]
        self.assertEqual((grant["operational_status"], grant["executable"]), ("COMPLETED", False))


if __name__ == "__main__":
    unittest.main()
