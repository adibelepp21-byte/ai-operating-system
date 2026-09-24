"""E13-05 — the full loop on a controlled operational object. TEST-VERIFIED only.

The instruction is `acts/P13-E13-05-BOUNDED-OPERATIONAL-STATE-PROOF-SURFACE-INSTRUCTION.md`.

**What this is.** A fixture *operational* object, not P13's knowledge or
evidence: two work orders in a temporary sandbox, each OPEN or DONE (a
LOCKED order cannot be transitioned). The only valid transition is
`OPEN --close--> DONE`.

The harness supplies three things:

* **the world**: which orders are open;
* **the capability**: a fixture action able to close an order, standing where a
  production action type would. None exists in production;
* **a fixture envelope**, written into a *temporary copy* of the Delegation
  Register.

It **never** names the order to act on, the action to take, or the expected
result. P13 derives all three from the state it observes. The same
capabilities in a different world yield a different decision, or none
(`test_the_harness_cannot_make_p13_act`).

**What this is not.** Nothing here is LIVE evidence. The production catalog has
no state-changing action, the live envelope grants none, and no recorded
authority permits one. `EXECUTION CAPABLE ≠ EXECUTION AUTHORIZED`.
"""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from native_core.core.infrastructure import LocalAppendOnlyStorage
from native_core.core.trace import TraceReader
from tools.p13 import cycle
from tools.p13.catalog import CATALOG, STATE_CHANGING, ActionType
from tools.p13.evaluation import Criterion
from tools.p13.evidence import EvidenceStore, decision_provenance
from tools.p13.model import ESCALATE, EXECUTE, REFUSE, VERIFIED, Citation
from tools.p13.paths import REPO_ROOT
from tools.p13.state import SOURCES, Source
from tools.tests.test_p13_post_construction import (DELEGATIONS, ENVELOPE,
                                                    P13_018, Governed)

CLOSE = "fixture.close_work_order"
WO = {"WO-1": "sandbox/work-order-1.json", "WO-2": "sandbox/work-order-2.json"}


class World:
    """The operational object: work orders on disk, observed and changed for real."""

    def __init__(self, root: Path, states, rogue=False):
        self.root = root
        (root / "sandbox").mkdir()
        for order, state in states.items():
            (root / WO[order]).write_text(json.dumps({"id": order, "state": state}),
                                          encoding="utf-8")
        (root / "sandbox/ledger.txt").write_text("unrelated", encoding="utf-8")
        self.rogue = rogue

    def state(self, order):
        return json.loads((self.root / WO[order]).read_text(encoding="utf-8"))["state"]

    # -- the capability the harness supplies (never the decision) ----------
    def observe(self, paths, target):
        return {p.relative_to(self.root).as_posix():
                hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted((self.root / "sandbox").glob("*")) if p.is_file()}

    def close(self, paths, target):
        record = json.loads((self.root / target).read_text(encoding="utf-8"))
        # A rogue executor believes it closed the order and writes the wrong state.
        record["state"] = "DEFERRED" if self.rogue else "DONE"
        (self.root / target).write_text(json.dumps(record), encoding="utf-8")
        return {}

    def executor_says_it_worked(self, paths, target, before, after):
        return before.get(target) != after.get(target), "the order file changed"

    def order_is_open(self, paths, target):
        state = json.loads((self.root / target).read_text(encoding="utf-8"))["state"]
        return None if state == "OPEN" else f"{target} is {state}; only OPEN may close"

    def action(self):
        return ActionType(CLOSE, False, (), "tests: World.close", self.close,
                          effect=STATE_CHANGING, observe=self.observe,
                          verify=self.executor_says_it_worked,
                          preconditions=(self.order_is_open,))

    def source(self):
        return Source("work-orders", "tests: work orders on disk",
                      tuple(f"workorder.{o}" for o in WO),
                      lambda p, c: {f"workorder.{o}": (self.state(o), VERIFIED)
                                    for o in WO})


def criteria():
    return tuple(Criterion(
        f"CR-{order}", f"work order {order} is done",
        Citation("P13-018", "P13-018 (fixture)", P13_018),
        (f"workorder.{order}",), lambda v, o=order: v[f"workorder.{o}"] == "DONE",
        "error", CLOSE, WO[order]) for order in WO)


class Fixture(unittest.TestCase):
    STATES = {"WO-1": "OPEN", "WO-2": "DONE"}
    ROGUE = False

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.world = World(self.tmp, dict(self.STATES), rogue=self.ROGUE)
        self.envelope_dir = self.tmp / "envelopes"
        self.envelope_dir.mkdir()
        self.register = self.tmp / "delegations.md"
        self.register.write_text(DELEGATIONS.read_text(encoding="utf-8"), encoding="utf-8")
        self.paths = Governed(REPO_ROOT, self.tmp / "live", self.envelope_dir, self.register)

    def tearDown(self):
        self._tmp.cleanup()

    def grant(self, envelope_id="P13-ENV-T5", targets=tuple(WO.values()), **changes):
        record = json.loads(ENVELOPE.read_text(encoding="utf-8"))
        record["envelope_id"] = envelope_id
        record["action_types"] = {CLOSE: {"items": [0], "targets": list(targets)}}
        record.update(changes)
        raw = json.dumps(record, indent=2).encode("utf-8")
        (self.envelope_dir / f"{envelope_id}.json").write_bytes(raw)
        with open(self.register, "a", encoding="utf-8") as handle:
            handle.write(f"\n### {envelope_id} — fixture\n\n| **Record** | "
                         f"{hashlib.sha256(raw).hexdigest()} |\n| **Status** | **ACTIVE** |\n")

    def basis_only(self):
        """P13-ENV-01 alone: a cycle may run, and closing work orders is not granted."""
        (self.envelope_dir / "P13-ENV-01.json").write_bytes(ENVELOPE.read_bytes())

    def run_cycle(self, intent="E13-05 fixture"):
        sources = tuple(s for s in SOURCES if s.name not in ("self_model", "corpus")) + (
            self.world.source(),)
        return cycle.run_cycle(self.paths, intent=intent, invoker="tools/tests/test_p13_e13_05.py",
                               sources=sources, criteria=criteria(),
                               catalog={**CATALOG, CLOSE: self.world.action()})

    def record(self, result):
        return json.loads((self.paths.cycles / f"{result['cycle_id']}.json").read_text())

    def trace(self):
        storage = LocalAppendOnlyStorage(self.paths.trace)
        storage.provision()
        return list(TraceReader(storage).read())

    def decision_on(self, result, order):
        return result["decisions"].get(f"P13 {CLOSE} {WO[order]}")


class CaseAValidAuthority(Fixture):

    def test_p13_decides_executes_verifies_traces_reobserves_rediscovers(self):
        self.grant()
        first = self.run_cycle()
        # P1: P13 chose WO-1 from the world. WO-2 was already DONE and untouched.
        self.assertEqual(first["executed"], CLOSE)
        self.assertEqual(self.decision_on(first, "WO-1"), EXECUTE)
        self.assertIsNone(self.decision_on(first, "WO-2"))
        # P3: a real operational transition, and nothing else changed.
        self.assertEqual((self.world.state("WO-1"), self.world.state("WO-2")), ("DONE", "DONE"))
        self.assertEqual((self.tmp / "sandbox/ledger.txt").read_text(), "unrelated")
        # P4: the expectation was fixed before the gate, and matched.
        self.assertEqual(first["consequence"], {
            "action_type": CLOSE, "target": WO["WO-1"], "expected": {"CR-WO-1": "PASS"},
            "actual": {"CR-WO-1": "PASS/VERIFIED"}, "execution_status": "success",
            "matched": True})
        record = self.record(first)
        after = {f["key"]: f for f in record["observation"]["after"]["facts"]}
        self.assertEqual(after["workorder.WO-1"]["value"], "DONE")   # re-observed
        self.assertEqual(after["workorder.WO-1"]["source"], "tests: work orders on disk")
        # P5: the chain is in the record and the Trace, and it verifies.
        entry = self.trace()[-1].outputs
        self.assertEqual(entry["execution"]["authority"], "P13-018 D-2b")
        self.assertEqual(entry["execution"]["envelope"], "P13-ENV-T5")
        self.assertTrue(entry["execution"]["derived_from"])
        self.assertTrue(entry["consequence"]["matched"])
        self.assertEqual(decision_provenance(record), [])
        # P6: the next cycle starts from the changed state and has nothing to do.
        second = self.run_cycle("E13-05 fixture: rediscovery")
        self.assertIsNone(second["executed"])
        self.assertEqual(second["results"], {"CR-WO-1": "PASS/VERIFIED",
                                             "CR-WO-2": "PASS/VERIFIED"})
        self.assertTrue(EvidenceStore(self.paths).verify()["holds"])


class CaseBInvalidAuthority(Fixture):

    def test_no_grant_refuses_and_nothing_changes(self):
        self.basis_only()
        result = self.run_cycle()
        self.assertEqual(self.decision_on(result, "WO-1"), ESCALATE)
        self.assertIsNone(result["executed"])
        self.assertEqual(self.world.state("WO-1"), "OPEN")
        traced = {d["subject"]: d["decision"] for d in self.trace()[-1].outputs["decisions"]}
        self.assertEqual(traced[f"P13 {CLOSE} {WO['WO-1']}"], ESCALATE)


class CaseCAmbiguousAuthority(Fixture):

    def test_expired_or_duplicated_authority_stops_and_nothing_changes(self):
        for changes in ({"expires": "2026-01-01"},):
            self.grant(**changes)
        self.basis_only()
        result = self.run_cycle()
        self.assertEqual(self.decision_on(result, "WO-1"), ESCALATE)
        self.assertEqual(self.world.state("WO-1"), "OPEN")

    def test_two_grants_conflict(self):
        self.grant("P13-ENV-T5")
        self.grant("P13-ENV-T6")
        result = self.run_cycle()
        self.assertEqual(self.decision_on(result, "WO-1"), ESCALATE)
        self.assertEqual(self.world.state("WO-1"), "OPEN")


class CaseDInvalidTarget(Fixture):

    def test_a_grant_for_another_order_does_not_reach_this_one(self):
        self.grant(targets=(WO["WO-2"],))
        result = self.run_cycle()
        self.assertEqual(self.decision_on(result, "WO-1"), REFUSE)
        self.assertEqual(self.world.state("WO-1"), "OPEN")

    def test_a_tampered_target_list_is_not_the_recorded_grant(self):
        self.grant(targets=(WO["WO-2"],))
        path = self.envelope_dir / "P13-ENV-T5.json"
        record = json.loads(path.read_text())
        record["action_types"][CLOSE]["targets"] = list(WO.values())
        path.write_text(json.dumps(record))
        self.basis_only()
        result = self.run_cycle()
        self.assertNotEqual(self.decision_on(result, "WO-1"), EXECUTE)
        self.assertEqual(self.world.state("WO-1"), "OPEN")


class CaseEFailedPrecondition(Fixture):
    STATES = {"WO-1": "LOCKED", "WO-2": "DONE"}

    def test_a_locked_order_is_refused_and_nothing_changes(self):
        self.grant()
        result = self.run_cycle()
        self.assertEqual(self.decision_on(result, "WO-1"), REFUSE)
        self.assertEqual(self.world.state("WO-1"), "LOCKED")
        reasons = [d["reason"] for d in self.record(result)["decisions"]]
        self.assertTrue(any(r.startswith("missing precondition") for r in reasons))


class CaseFConsequenceMismatch(Fixture):
    ROGUE = True

    def test_mismatch_is_not_success_and_is_reviewed_not_repeated(self):
        self.grant()
        first = self.run_cycle()
        self.assertEqual(self.world.state("WO-1"), "DEFERRED")     # it did change
        # The executor's own check passed; the expected consequence did not occur.
        self.assertEqual(first["consequence"]["execution_status"], "success")
        self.assertIs(first["consequence"]["matched"], False)
        self.assertEqual(first["consequence"]["actual"], {"CR-WO-1": "FAIL/VERIFIED"})
        self.assertEqual(self.trace()[-1].status, "failure")
        # Rediscovery: the next cycle concludes the remedy failed, sends it for
        # review, and does not simply run it again.
        second = self.run_cycle("E13-05 fixture: after a mismatch")
        record = self.record(second)
        self.assertIn("R-MISMATCH", {c["rule"] for c in record["conclusions"]})
        self.assertEqual(second["decisions"].get(
            f"P13 review.consequence {CLOSE}:{WO['WO-1']}"), ESCALATE)
        self.assertIsNone(self.decision_on(second, "WO-1"))
        self.assertIsNone(second["executed"])


class CaseFFailedExecutionIsNeverAMatch(Fixture):

    def test_a_failing_executor_is_not_credited_with_a_consequence(self):
        """The order ends DONE, but the executor raised. The consequence is not
        attributed to an execution that failed."""
        self.grant()
        original = self.world.close

        def close_then_fail(paths, target):
            original(paths, target)
            raise RuntimeError("executor crashed after writing")

        self.world.close = close_then_fail
        result = self.run_cycle()
        self.assertEqual(self.world.state("WO-1"), "DONE")
        self.assertEqual(result["consequence"]["execution_status"], "failure")
        self.assertIs(result["consequence"]["matched"], False)


class TheDecisionIsP13s(Fixture):

    def test_the_harness_cannot_make_p13_act(self):
        """Same capability, same grant, a world with nothing to do: no action."""
        self.world = World(Path(tempfile.mkdtemp(dir=self.tmp)),
                           {"WO-1": "DONE", "WO-2": "DONE"})
        self.grant()
        result = self.run_cycle()
        self.assertIsNone(result["executed"])
        self.assertEqual(result["decisions"], {})

    def test_an_injected_execution_has_no_provenance(self):
        self.grant()
        record = self.record(self.run_cycle())
        injected = copy.deepcopy(record)
        injected["decisions"].append({"proposal": "p:injected", "decision": "EXECUTE"})
        self.assertTrue(decision_provenance(injected))
        severed = copy.deepcopy(record)
        for p in severed["proposals"]:
            p["derived_from"] = ["c:from-the-test-runner"]
        self.assertTrue(decision_provenance(severed))
        unobserved = copy.deepcopy(record)
        for c in unobserved["conclusions"]:
            c["premises"] = ["fact.supplied-by-the-test-runner"]
        self.assertTrue(any("were not observed or evaluated" in f
                            for f in decision_provenance(unobserved)))

    def test_an_expectation_rewritten_to_fit_the_result_is_detected(self):
        self.grant()
        record = self.record(self.run_cycle())
        rewritten = copy.deepcopy(record)
        rewritten["verification"]["consequence"]["expected"] = {"CR-WO-1": "FAIL"}
        self.assertTrue(any("expected consequence" in f
                            for f in decision_provenance(rewritten)))

    def test_an_execution_without_consequence_verification_is_a_fault(self):
        self.grant()
        record = self.record(self.run_cycle())
        record["verification"]["consequence"] = None
        self.assertIn("an action executed, but its consequence was not verified",
                      decision_provenance(record))

    def test_trace_and_record_must_agree_on_what_executed(self):
        store = EvidenceStore(self.paths)
        _, record_digest = store.write_cycle({"cycle_id": "c-x", "executed": {
            "action_type": CLOSE}})
        store.write_trace(outputs={"cycle_id": "c-x", "record_digest": record_digest,
                                   "executed": None}, status="success", tools_used=(),
                          knowledge_consumed=(), memory_consumed=())
        self.assertIn("c-x: Trace and record disagree on the executed action",
                      store.verify()["faults"])

    def test_a_state_change_with_no_expected_consequence_is_refused(self):
        from tools.p13.authority import AuthorityGate, load_envelopes
        from tools.p13.model import ActionProposal
        self.grant()
        gate = AuthorityGate(self.paths, {**CATALOG, CLOSE: self.world.action()},
                             load_envelopes(self.paths)[0])
        decision = gate.decide(ActionProposal("p", CLOSE, WO["WO-1"], ("c",), "r",
                                              VERIFIED, (0, "", "x")))
        self.assertEqual(decision.decision, REFUSE)
        self.assertIn("no expected consequence", decision.reason)
        self.assertEqual(self.world.state("WO-1"), "OPEN")


if __name__ == "__main__":
    unittest.main()
