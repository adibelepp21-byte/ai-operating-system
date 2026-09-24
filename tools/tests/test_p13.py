"""P13 — verified against Blueprint `§7`, live, with a negative control per criterion.

Live cycles read the real tree and write to a temporary live root, so no test
writes `docs/operations/p13/`. Each negative control is a case that *would*
fail if the contract did not hold (P12 `§46`: fixtures are supplementary).
"""

from __future__ import annotations

import ast
import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Optional

from tools import certified_write_barrier as barrier
from tools import foundational_question_reconciliation as reconciliation
from tools.p13 import cycle
from tools.p13.authority import AuthorityGate, Envelope, load_envelopes
from tools.p13.catalog import CATALOG, RESERVED
from tools.p13.evaluation import CRITERIA, Criterion, Evaluation
from tools.p13.evidence import EvidenceStore
from tools.p13.evolution import Evolution
from tools.p13.execution import BoundedExecution
from tools.p13.frontier import (EXHAUSTED_WITH_REMAINDER, NOT_EXHAUSTED, Frontier)
from tools.p13.model import (ESCALATE, EXECUTE, FAIL, INFERRED, PASS, REFUSE,
                             UNKNOWN, VERIFIED, ActionProposal, Citation,
                             Conclusion, EvaluationResult, Fact, GateDecision,
                             P13Error, StateSnapshot)
from tools.p13.next_action import NextAction
from tools.p13.paths import LIVE_ROOT, REPO_ROOT, Paths
from tools.p13.reasoning import Reasoning
from tools.p13.state import (SELF_MODEL_KEYS, SOURCES, VERIFICATION_KEYS, Source,
                             StateUnderstanding, read_criteria)

P13_018 = "docs/governance/acts/P13-018-FOUNDER-CONSTRUCTION-AUTHORITY-GATE-DECISION.md"
ENVELOPE = REPO_ROOT / "docs/governance/p13-envelopes/P13-ENV-01.json"
REGISTER = REPO_ROOT / "docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md"
T = "2026-09-24T00:00:00+00:00"
FAST = tuple(s for s in SOURCES if s.name not in ("self_model", "corpus"))
FAST_CRITERIA = tuple(c for c in CRITERIA if not c.id.startswith("CR-CORPUS"))


@dataclass(frozen=True)
class Governed(Paths):
    """The real tree, with envelopes / Delegation Register / matrix / Knowledge redirected."""

    envelope_dir: Optional[Path] = None
    register: Optional[Path] = None
    matrix_file: Optional[Path] = None
    knowledge_dir: Optional[Path] = None

    @property
    def envelopes(self):
        return self.envelope_dir or super().envelopes

    @property
    def delegation_register(self):
        return self.register or super().delegation_register

    @property
    def matrix(self):
        return self.matrix_file or super().matrix

    @property
    def knowledge_store(self):
        return self.knowledge_dir or super().knowledge_store


def _git_status():
    return subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"],
                          cwd=REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout


def fact(key, value, status=VERIFIED, source="test"):
    return Fact(key, value, status, source, T)


def proposal(action_type, certainty=VERIFIED, rank=1, target="state"):
    return ActionProposal(id=f"p:{action_type}", action_type=action_type,
                          target=target, derived_from=("c:test",),
                          rationale="test", certainty=certainty,
                          priority=(rank, "", action_type))


class Tmp(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.paths = Governed(REPO_ROOT, self.tmp / "live")

    def tearDown(self):
        self._tmp.cleanup()


# ---------------------------------------------------------------------------
# Live: two full cycles on the real system state.
# ---------------------------------------------------------------------------

class LiveCycles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.paths = Paths(REPO_ROOT, Path(cls._tmp.name) / "live")
        cls.status_before = _git_status()
        cls.first = cycle.run_cycle(cls.paths, intent="test: live cycle 1",
                                    invoker="tools/tests/test_p13.py")
        cls.second = cycle.run_cycle(cls.paths, intent="test: live cycle 2",
                                     invoker="tools/tests/test_p13.py")
        cls.status_after = _git_status()
        cls.records = [json.loads((cls.paths.cycles / f"{r['cycle_id']}.json")
                                  .read_text(encoding="utf-8"))
                       for r in (cls.first, cls.second)]

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_e13_01_the_snapshot_covers_self_model_integrity_escalations_and_memory(self):
        before = self.records[0]["observation"]["before"]["facts"]
        keys = {f["key"] for f in before}
        self.assertEqual(len(SELF_MODEL_KEYS), 12)
        for key in SELF_MODEL_KEYS + ("integrity.holds", "escalations.open",
                                      "memory.stores", "memory.p13.previous",
                                      "knowledge.corpus_health_criteria",
                                      "native_core.boundaries"):
            self.assertIn(key, keys)
        for f in before:
            self.assertTrue(f["source"] and f["observed_at"], f)
            self.assertIn(f["status"], (VERIFIED, INFERRED, UNKNOWN))

    def test_e13_01_memory_is_read_back_through_memory_reader(self):
        facts = {f["key"]: f for f in self.records[1]["observation"]["before"]["facts"]}
        remembered = facts["memory.p13.previous"]["value"]
        self.assertEqual(remembered["cycle_id"], self.first["cycle_id"])
        self.assertEqual(facts["memory.stores"]["value"]["p13"], 1)
        verified = self.first["executed"]
        key = CATALOG[verified].produces[0]
        if key.startswith("verification."):
            self.assertEqual(facts[key]["status"], INFERRED)
            self.assertIn(self.first["cycle_id"], facts[key]["source"])

    def test_e13_02_every_criterion_is_admitted_and_judged(self):
        record = self.records[1]
        self.assertEqual(record["authority"]["refused_criteria"], [])
        results = {e["criterion"]: e for e in record["evaluations_after"]}
        self.assertEqual(set(results), {c.id for c in CRITERIA})
        for e in results.values():
            self.assertIn(e["result"], (PASS, FAIL, UNKNOWN))
            self.assertTrue(e["authority"])

    def test_e13_02_the_admitted_knowledge_criteria_are_judged_live(self):
        results = {e["criterion"]: e for e in self.records[0]["evaluations_before"]}
        self.assertEqual(results["CR-CORPUS-CITATION-ERRORS"]["result"], PASS)
        self.assertEqual(results["CR-INTEGRITY"]["result"], PASS)
        self.assertEqual(results["CR-NATIVE-CORE"]["result"], PASS)

    def test_e13_05_one_authorized_read_only_action_executed_per_cycle(self):
        for record in self.records:
            executed = [d for d in record["decisions"] if d["decision"] == EXECUTE]
            self.assertEqual(len(executed), 1, record["decisions"])
            self.assertEqual(executed[0]["envelope"], "P13-ENV-01")
            self.assertTrue(executed[0]["action_type"].startswith("verify."))
            self.assertEqual(record["executed"]["status"], "success")
            for d in record["decisions"]:
                if d["decision"] == REFUSE:
                    self.assertTrue(d["reason"].startswith("cycle bound"), d)

    def test_e13_06_after_execution_state_is_re_derived_and_the_difference_recorded(self):
        record = self.records[0]
        self.assertTrue(record["verification"]["re_evaluated"])
        self.assertTrue(record["verification"]["changes"])
        self.assertNotEqual(record["observation"]["digest_before"],
                            record["observation"]["digest_after"])

    def test_e13_06_what_changed_comes_from_memory(self):
        ids = {c["id"]: c for c in self.records[1]["conclusions"]}
        self.assertIn("c:changed", ids)
        self.assertIn("memory.p13.previous", ids["c:changed"]["premises"])

    def test_memory_orders_the_next_verification(self):
        self.assertNotEqual(self.first["executed"], self.second["executed"])

    def test_e13_07_exhaustion_is_assessed_and_the_remainder_classified(self):
        frontier = self.records[1]["frontier"]
        items = " ".join(r["item"] for r in frontier["remainder"])
        for expected in ("GAP-0017", "GAP-0018", "Q39", "Q91", "Q23"):
            self.assertIn(expected, items)
        self.assertEqual(frontier["unclassified_core"], [])

    def test_records_carry_the_twelve_section_29_elements(self):
        self.assertEqual(len(self.records[0]["section_29"]), 12)
        # Q61/Q62: each record carries a briefing that ends in its exhaustion state.
        self.assertTrue(self.records[0]["briefing"][-1].startswith("exhaustion: "))

    def test_own_evidence_verifies_record_and_trace_one_to_one(self):
        result = EvidenceStore(self.paths).verify()
        self.assertEqual((result["records"], result["trace_entries"]), (2, 2))
        self.assertTrue(result["holds"], result["faults"])
        self.assertTrue(self.first["readback_holds"] and self.second["readback_holds"])

    def test_a_live_cycle_writes_nothing_outside_its_live_root(self):
        self.assertEqual(self.status_before, self.status_after)


# ---------------------------------------------------------------------------
# E13-01 negative controls
# ---------------------------------------------------------------------------

class StateNegativeControls(Tmp):

    def test_a_removed_memory_source_yields_unknown_not_omission(self):
        sources = tuple(s for s in FAST if s.name != "memory")
        snapshot = StateUnderstanding(self.paths, sources).observe()
        self.assertIsNone(snapshot.get("memory.p13.previous"))
        without = tuple(Source(s.name, s.describe, s.keys,
                               (lambda p, c: (_ for _ in ()).throw(RuntimeError("gone")))
                               if s.name == "memory" else s.read) for s in FAST)
        snapshot = StateUnderstanding(self.paths, without).observe()
        for key in ("memory.stores", "memory.p13.previous"):
            self.assertEqual(snapshot.get(key).status, UNKNOWN)
            self.assertIn("unavailable — RuntimeError: gone", snapshot.get(key).source)
        for key in VERIFICATION_KEYS:
            self.assertEqual(snapshot.get(key).status, UNKNOWN)

    def test_a_fact_without_a_source_is_rejected(self):
        with self.assertRaises(P13Error):
            Fact("x", 1, VERIFIED, "", T)
        with self.assertRaises(P13Error):
            Fact("x", 1, "CERTAIN", "test", T)
        with self.assertRaises(P13Error):
            StateSnapshot((fact("x", 1), fact("x", 2)), T)

    def test_absent_knowledge_is_a_knowledge_gap_that_escalates(self):
        empty = self.tmp / "empty-store"
        empty.mkdir()
        paths = Governed(REPO_ROOT, self.tmp / "live", knowledge_dir=empty)
        snapshot = StateUnderstanding(paths, FAST).observe()
        self.assertEqual(snapshot.get("knowledge.corpus_health_criteria").status, UNKNOWN)
        corpus = tuple(c for c in CRITERIA if c.id == "CR-CORPUS-CITATION-ERRORS")
        snapshot = snapshot.with_facts((fact("corpus.citation_errors", 0),), T)
        evaluations = Evaluation(paths, corpus).evaluate(snapshot)
        self.assertEqual(evaluations[0].result, UNKNOWN)
        conclusions = Reasoning().reason(snapshot, evaluations)
        gap = next(c for c in conclusions if c.kind == "gap")
        self.assertEqual(gap.gap_class, "knowledge gap")
        proposals = NextAction(corpus).propose(conclusions, snapshot)
        self.assertEqual(proposals[0].action_type, "admit.knowledge")
        envelopes, _ = load_envelopes(paths)
        decision = AuthorityGate(paths, CATALOG, envelopes).decide(proposals[0])
        self.assertEqual(decision.decision, ESCALATE)

    def test_d3_the_criteria_are_read_and_never_written(self):
        store = REPO_ROOT / "docs/architecture/p12/aios-runtime-store/native_core_storage"
        before = hashlib.sha256((store / "knowledge_versions").read_bytes()).hexdigest()
        criteria = read_criteria(Paths(REPO_ROOT))
        self.assertEqual(criteria["content"], {"citation_errors_max": 0,
                                               "live_stale_assertions_max": 0,
                                               "stale_governance_sources_max": 0})
        after = hashlib.sha256((store / "knowledge_versions").read_bytes()).hexdigest()
        self.assertEqual(before, after)
        self.assertTrue(barrier.refuses(store / "knowledge_versions"))


# ---------------------------------------------------------------------------
# E13-02 / E13-03 negative controls
# ---------------------------------------------------------------------------

class EvaluationAndReasoningNegativeControls(Tmp):

    def _criterion(self, citation=None, judge=lambda v: v["x"] == 1):
        return Criterion("CR-TEST", "x is 1",
                         citation or Citation("P13-018", "P13-018", P13_018),
                         ("x",), judge, "error", "change.code")

    def test_a_criterion_whose_authority_does_not_resolve_is_refused(self):
        for citation in (Citation("FD-P99-999", "FD-P99-999", "README.md"),
                         Citation("P13-018", "P13-018", "README.md"),
                         Citation("FD-P11-001", "P13-018", P13_018)):
            evaluation = Evaluation(self.paths, (self._criterion(citation),))
            self.assertEqual(evaluation.admitted, [])
            self.assertEqual(len(evaluation.refused), 1)

    def test_missing_evidence_is_unknown_never_pass(self):
        evaluation = Evaluation(self.paths, (self._criterion(judge=lambda v: True),))
        for snapshot in (StateSnapshot((), T),
                         StateSnapshot((fact("x", None, UNKNOWN),), T)):
            self.assertEqual(evaluation.evaluate(snapshot)[0].result, UNKNOWN)

    def test_an_unjudgeable_criterion_is_unknown(self):
        evaluation = Evaluation(self.paths, (self._criterion(judge=lambda v: v["x"]["y"]),))
        self.assertEqual(evaluation.evaluate(StateSnapshot((fact("x", 1),), T))[0].result,
                         UNKNOWN)

    def test_remembered_evidence_gives_an_inferred_result(self):
        evaluation = Evaluation(self.paths, (self._criterion(),))
        result = evaluation.evaluate(StateSnapshot((fact("x", 1, INFERRED),), T))[0]
        self.assertEqual((result.result, result.certainty), (PASS, INFERRED))

    def test_a_premise_less_conclusion_is_rejected(self):
        with self.assertRaises(P13Error):
            Conclusion("c:x", "R-X", "defect", "x", (), VERIFIED)

    def test_a_premise_naming_nothing_in_the_cycle_is_rejected(self):
        snapshot = StateSnapshot((fact("x", 1),), T)
        Reasoning.check(Conclusion("c:ok", "R", "k", "s", ("x",), VERIFIED), snapshot, ())
        with self.assertRaises(P13Error):
            Reasoning.check(Conclusion("c:bad", "R", "k", "s", ("nonexistent",),
                                       VERIFIED), snapshot, ())

    def test_one_source_behind_several_failures_is_concluded_systemic(self):
        down = "store X: unavailable — OSError"
        results = tuple(EvaluationResult(f"CR-{i}", UNKNOWN, VERIFIED, {}, (down,),
                                         "P13-018", "error", "r", ("x",)) for i in (1, 2))
        snapshot = StateSnapshot((fact("x", None, UNKNOWN, down),), T)
        conclusions = Reasoning().reason(snapshot, results)
        systemic = [c for c in conclusions if c.kind == "systemic"]
        self.assertEqual(len(systemic), 1)
        self.assertEqual(set(systemic[0].premises), {"eval:CR-1", "eval:CR-2"})

    def test_evidence_not_yet_verified_is_not_a_systemic_cause(self):
        """The first live cycles concluded "systemic" from three facts that had
        simply never been verified. Each is obtainable by its own verifier."""
        never = "Memory: verifications recorded by earlier P13 cycles: not reported"
        results = tuple(EvaluationResult(f"CR-{i}", UNKNOWN, VERIFIED, {}, (never,),
                                         "P13-018", "error", "r", ("x",)) for i in (1, 2))
        snapshot = StateSnapshot((fact("x", None, UNKNOWN, never),), T)
        self.assertFalse([c for c in Reasoning().reason(snapshot, results)
                          if c.kind == "systemic"])
        failing = tuple(EvaluationResult(f"CR-{i}", FAIL, VERIFIED, {}, ("audit Y",),
                                         "P13-018", "error", "r", ("x",)) for i in (1, 2))
        snapshot = StateSnapshot((fact("x", 1, VERIFIED, "audit Y"),), T)
        self.assertTrue([c for c in Reasoning().reason(snapshot, failing)
                         if c.kind == "systemic"])

    def test_shortfalls_are_classified_apart(self):
        catalog = dict(CATALOG)
        snapshot = StateSnapshot((fact("knowledge.k", None, UNKNOWN),
                                  fact("y", None, UNKNOWN, "src: unavailable — E"),
                                  fact("z", None, UNKNOWN)), T)
        results = tuple(EvaluationResult(f"CR-{k}", UNKNOWN, VERIFIED, {}, (), "a", "error",
                                         "r", (k,)) for k in ("knowledge.k", "y", "z"))
        classes = {c.subject: c.gap_class for c in Reasoning(catalog).reason(snapshot, results)
                   if c.kind == "gap"}
        self.assertEqual(classes, {"CR-knowledge.k": "knowledge gap",
                                   "CR-y": "limitation", "CR-z": "capability gap"})


# ---------------------------------------------------------------------------
# E13-04 / E13-05 negative controls
# ---------------------------------------------------------------------------

class TheGateIsTheOnlySourceOfExecute(Tmp):

    def setUp(self):
        super().setUp()
        self.envelopes, anomalies = load_envelopes(self.paths)
        self.assertEqual(anomalies, ())
        self.gate = AuthorityGate(self.paths, CATALOG, self.envelopes)

    def test_a_proposal_carries_no_authorization(self):
        names = {f.name for f in fields(ActionProposal)}
        self.assertFalse({n for n in names if "author" in n or "approv" in n
                          or "envelope" in n or "grant" in n})

    def test_a_proposal_cannot_be_executed_directly(self):
        with self.assertRaises(TypeError):
            BoundedExecution(self.paths, CATALOG).execute(
                proposal("verify.p13_evidence"), T)

    def test_nothing_but_the_gate_can_mint_a_decision(self):
        with self.assertRaises(P13Error):
            GateDecision(proposal("verify.p13_evidence"), EXECUTE, "self-issued",
                         "P13-ENV-01")

    def test_a_recommendation_presented_as_a_decision_is_refused(self):
        decided = self.gate.decide(proposal("verify.p13_evidence"))
        for thing in ({"action_type": "verify.p13_evidence", "authorized": True},
                      decided):
            self.assertEqual(AuthorityGate(self.paths, CATALOG, self.envelopes)
                             .decide(thing).decision, REFUSE)

    def test_an_unknown_action_type_is_refused(self):
        self.assertEqual(self.gate.decide(proposal("delete.everything")).decision, REFUSE)

    def test_every_reserved_type_escalates_and_is_recorded_open(self):
        from tools.escalation_register import EscalationRegister
        for action_type in RESERVED:
            with self.subTest(action_type):
                decision = self.gate.decide(proposal(action_type))
                self.assertEqual(decision.decision, ESCALATE)
                record = EscalationRegister(self.paths.escalations).load(
                    decision.escalation_id)
                self.assertEqual(record["refusal_type"], "EscalationRequired")
                self.assertTrue(record["authority_instrument"].startswith("P13-018"))
                self.assertEqual(EscalationRegister(self.paths.escalations)
                                 .status(decision.escalation_id), "OPEN")

    def test_an_open_escalation_is_not_raised_twice(self):
        first = self.gate.decide(proposal("change.code")).escalation_id
        again = self.gate.decide(proposal("change.code")).escalation_id
        self.assertEqual(first, again)
        self.assertEqual(len(list(self.paths.escalations.glob("*.escalation.json"))), 1)

    def test_a_reserved_type_inside_an_envelope_still_escalates(self):
        rogue = Envelope("P13-ENV-X", "Founder", "P13-018", "P13-018", P13_018,
                         ("change.code", "change.governance"), ("observe", "record"), "0")
        gate = AuthorityGate(self.paths, CATALOG, self.envelopes + (rogue,))
        self.assertEqual(gate.decide(proposal("change.code")).decision, ESCALATE)

    def test_an_unknown_premise_is_unknown(self):
        self.assertEqual(self.gate.decide(proposal("verify.p13_evidence", UNKNOWN)).decision,
                         UNKNOWN)

    def test_no_envelope_escalates_on_fdr_2_alone(self):
        from tools.escalation_register import EscalationRegister
        decision = AuthorityGate(self.paths, CATALOG, ()).decide(
            proposal("verify.p13_evidence"))
        self.assertEqual(decision.decision, ESCALATE)
        record = EscalationRegister(self.paths.escalations).load(decision.escalation_id)
        self.assertEqual(record["authority_instrument"], "FDR-2 D05")

    def test_conflicting_envelopes_escalate(self):
        twin = Envelope("P13-ENV-Y", "Founder", "P13-018", "P13-018", P13_018,
                        ("verify.p13_evidence",), (), "0")
        gate = AuthorityGate(self.paths, CATALOG, self.envelopes + (twin,))
        decision = gate.decide(proposal("verify.p13_evidence"))
        self.assertEqual(decision.decision, ESCALATE)
        self.assertIn("conflict", decision.reason)

    def test_a_second_action_in_one_cycle_is_refused(self):
        first = self.gate.decide(proposal("verify.p13_evidence"))
        second = self.gate.decide(proposal("verify.ecosystem_relationships"))
        self.assertEqual((first.decision, second.decision), (EXECUTE, REFUSE))
        execution = BoundedExecution(self.paths, CATALOG)
        execution.execute(first, T)
        with self.assertRaises(P13Error):
            execution.execute(first, T)

    def test_memory_recency_orders_proposals(self):
        previous = {"last_executed": {"verify.p13_evidence": "2026-09-24T01",
                                      "verify.ecosystem_relationships": "2026-09-24T00"}}
        snapshot = StateSnapshot((fact("memory.p13.previous", previous),), T)
        conclusions = tuple(Conclusion(f"c:{a}", "R-STALE", "evidence-stale", "s",
                                       ("memory.p13.previous",), INFERRED, a)
                            for a in ("verify.p13_evidence",
                                      "verify.ecosystem_relationships",
                                      "verify.foundational_question_reconciliation"))
        order = [p.action_type for p in NextAction(CRITERIA).propose(conclusions, snapshot)]
        self.assertEqual(order, ["verify.foundational_question_reconciliation",
                                 "verify.ecosystem_relationships",
                                 "verify.p13_evidence"])


class EnvelopesResolveOrAreAnomalies(Tmp):

    def setUp(self):
        super().setUp()
        self.envelope_dir = self.tmp / "envelopes"
        self.envelope_dir.mkdir()
        self.register = self.tmp / "register.md"
        self.register.write_text(REGISTER.read_text(encoding="utf-8"), encoding="utf-8")
        self.paths = Governed(REPO_ROOT, self.tmp / "live", envelope_dir=self.envelope_dir,
                              register=self.register)

    def _write(self, name, record, register_it=True, status="**ACTIVE**"):
        raw = json.dumps(record, indent=2).encode("utf-8")
        (self.envelope_dir / name).write_bytes(raw)
        if register_it:
            with open(self.register, "a", encoding="utf-8") as handle:
                handle.write(f"\n### {record['envelope_id']} — test\n\n"
                             f"| **Record** | {hashlib.sha256(raw).hexdigest()} |\n"
                             f"| **Status** | {status} |\n")

    def _base(self, **changes):
        record = json.loads(ENVELOPE.read_text(encoding="utf-8"))
        record.update(changes)
        return record

    def test_the_live_envelope_resolves(self):
        envelopes, anomalies = load_envelopes(Paths(REPO_ROOT))
        # P13-ENV-02 is FDR-3's S-OPS envelope (Delegation Register §15).
        self.assertEqual([e.id for e in envelopes], ["P13-ENV-01", "P13-ENV-02"])
        self.assertEqual(anomalies, ())
        for envelope in envelopes:
            self.assertFalse(set(envelope.action_types) & set(RESERVED))

    def test_a_tampered_envelope_is_not_the_recorded_one(self):
        shutil.copy(ENVELOPE, self.envelope_dir / "P13-ENV-01.json")
        self.assertEqual(len(load_envelopes(self.paths)[0]), 1)
        record = self._base()
        record["action_types"]["change.code"] = [1]
        (self.envelope_dir / "P13-ENV-01.json").write_text(json.dumps(record),
                                                          encoding="utf-8")
        envelopes, anomalies = load_envelopes(self.paths)
        self.assertEqual(envelopes, ())
        self.assertIn("tampered or unrecorded", anomalies[0])

    def test_a_planted_envelope_is_not_recorded(self):
        # An id no Register entry holds (P13-ENV-02 is recorded, since FDR-3).
        self._write("P13-ENV-99.json", self._base(envelope_id="P13-ENV-99"),
                    register_it=False)
        envelopes, anomalies = load_envelopes(self.paths)
        self.assertEqual(envelopes, ())
        self.assertIn("not recorded in the Delegation Register", anomalies[0])

    def test_a_forged_citation_does_not_resolve(self):
        self._write("P13-ENV-03.json", self._base(
            envelope_id="P13-ENV-03", instrument="FD-P11-001 §9", record="README.md"))
        envelopes, anomalies = load_envelopes(self.paths)
        self.assertEqual(envelopes, ())
        self.assertIn("not FD-P11-001's act", anomalies[0])

    def test_an_envelope_not_issued_by_the_founder_is_not_authority(self):
        self._write("P13-ENV-04.json", self._base(envelope_id="P13-ENV-04",
                                                  issued_by="Claude Code — CEO"))
        self.assertIn("only a Founder-issued envelope", load_envelopes(self.paths)[1][0])

    def test_an_inactive_or_revoked_envelope_is_not_authority(self):
        self._write("P13-ENV-05.json", self._base(envelope_id="P13-ENV-05"),
                    status="SUSPENDED")
        self.assertIn("not ACTIVE", load_envelopes(self.paths)[1][0])
        shutil.copy(ENVELOPE, self.envelope_dir / "P13-ENV-01.json")
        with open(self.register, "a", encoding="utf-8") as handle:
            handle.write("\n| P13-ENV-01 | REVOKED by the Founder |\n")
        self.assertTrue(any("P13-ENV-01" in a and "revoked or suspended" in a
                            for a in load_envelopes(self.paths)[1]))

    def test_an_envelope_for_another_root_is_not_authority(self):
        self._write("P13-ENV-06.json", self._base(envelope_id="P13-ENV-06",
                                                  designated_live_root="docs"))
        self.assertIn("does not designate", load_envelopes(self.paths)[1][0])

    def test_with_no_recorded_authority_a_cycle_does_nothing_but_escalate(self):
        # An id no Register entry holds (P13-ENV-02 is recorded, since FDR-3).
        self._write("P13-ENV-99.json", self._base(envelope_id="P13-ENV-99"),
                    register_it=False)
        result = cycle.run_cycle(self.paths, intent="t", invoker="t", sources=FAST)
        self.assertEqual(result["status"], "REFUSED")
        self.assertFalse(self.paths.cycles.exists())
        self.assertFalse(self.paths.trace.exists())
        self.assertEqual(len(list(self.paths.escalations.glob("*.escalation.json"))), 1)

    def test_an_unreadable_register_resolves_nothing(self):
        paths = Governed(REPO_ROOT, self.tmp / "live", register=self.tmp / "absent.md")
        envelopes, anomalies = load_envelopes(paths)
        self.assertEqual(envelopes, ())
        self.assertIn("unreadable", anomalies[0])


# ---------------------------------------------------------------------------
# E13-06 / E13-07 and evidence negative controls
# ---------------------------------------------------------------------------

class EvolutionFrontierAndEvidence(Tmp):

    def _matrix(self, mutate):
        record = json.loads(Paths(REPO_ROOT).matrix.read_text(encoding="utf-8"))
        mutate(record["questions"])
        path = self.tmp / "matrix.json"
        path.write_text(json.dumps(record), encoding="utf-8")
        return Governed(REPO_ROOT, self.tmp / "live", matrix_file=path)

    def test_a_core_question_without_evidence_is_a_gap_whose_evolution_escalates(self):
        def strip(rows):
            next(r for r in rows if r["id"] == "Q27")["evidence"] = []
        paths = self._matrix(strip)
        gaps, evolutions = Evolution(paths).derive((), StateSnapshot((), T))
        self.assertEqual([g.id for g in gaps], ["g:matrix:Q27"])
        self.assertEqual(evolutions[0].action_type, "change.code")
        envelopes, _ = load_envelopes(paths)
        decision = AuthorityGate(paths, CATALOG, envelopes).decide(evolutions[0])
        self.assertEqual(decision.decision, ESCALATE)
        self.assertEqual(Frontier(paths).assess((), None, gaps)["state"], NOT_EXHAUSTED)
        self.assertEqual(reconciliation.verify(paths.matrix)["holds"], False)

    def test_the_live_matrix_classifies_every_core_question(self):
        paths = Paths(REPO_ROOT)
        gaps, evolutions = Evolution(paths).derive((), StateSnapshot((), T))
        self.assertEqual((gaps, evolutions), ((), ()))
        self.assertEqual(Frontier(paths).assess((), None, ())["state"],
                         EXHAUSTED_WITH_REMAINDER)
        self.assertTrue(reconciliation.verify()["holds"])

    def test_deferred_work_is_not_exhausted_and_stale_refresh_is_classified(self):
        gate = AuthorityGate(self.paths, CATALOG, load_envelopes(self.paths)[0])
        gate.decide(proposal("verify.p13_evidence"))
        deferred = gate.decide(proposal("verify.ecosystem_relationships", rank=1))
        stale = gate.decide(proposal("verify.foundational_question_reconciliation", rank=3))
        frontier = Frontier(self.paths)
        self.assertEqual(frontier.assess((deferred,), None, ())["state"], NOT_EXHAUSTED)
        assessed = frontier.assess((stale,), None, ())
        self.assertEqual(assessed["state"], EXHAUSTED_WITH_REMAINDER)
        self.assertIn("refreshable", {r["class"] for r in assessed["remainder"]})

    def test_a_tampered_record_or_an_untraced_one_fails_own_verification(self):
        store = EvidenceStore(self.paths)
        path, digest = store.write_cycle({"cycle_id": "c1", "x": 1})
        self.assertTrue(store.readback(path, digest))
        with self.assertRaises(FileExistsError):
            store.write_cycle({"cycle_id": "c1", "x": 2})
        self.assertIn("c1: record has no Trace entry", store.verify()["faults"])
        store.write_trace(outputs={"cycle_id": "c1", "record_digest": digest},
                          status="success", tools_used=(), knowledge_consumed=(),
                          memory_consumed=())
        self.assertTrue(store.verify()["holds"])
        body = json.loads(path.read_text(encoding="utf-8"))
        body["x"] = 3
        path.write_text(json.dumps(body), encoding="utf-8")
        self.assertIn("c1.json: content does not hash to its digest", store.verify()["faults"])

    def test_a_run_is_bounded(self):
        for cycles in (0, cycle.MAX_CYCLES + 1):
            with self.assertRaises(P13Error):
                cycle.run(self.paths, cycles=cycles, intent="t", invoker="t")
        with self.assertRaises(P13Error):
            cycle.run_cycle(self.paths, intent="", invoker="t")


# ---------------------------------------------------------------------------
# Boundaries (Blueprint §10 OUT), held statically
# ---------------------------------------------------------------------------

class Boundaries(unittest.TestCase):
    PACKAGE = REPO_ROOT / "tools/p13"

    def _modules(self):
        return {p: ast.parse(p.read_text(encoding="utf-8"))
                for p in sorted(self.PACKAGE.glob("*.py"))}

    def _imports(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                yield from (a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                yield node.module or ""

    def test_nothing_is_imported_from_consumers(self):
        for path, tree in self._modules().items():
            for name in self._imports(tree):
                self.assertFalse(name.startswith("consumers"), f"{path.name}: {name}")

    def test_no_scheduler_thread_daemon_process_or_endless_loop(self):
        banned = ("threading", "asyncio", "sched", "multiprocessing", "subprocess",
                  "signal", "concurrent", "socket", "urllib", "http")
        for path, tree in self._modules().items():
            for name in self._imports(tree):
                self.assertFalse(name.split(".")[0] in banned, f"{path.name}: {name}")
            for node in ast.walk(tree):
                if isinstance(node, ast.While):
                    self.fail(f"{path.name}: a while loop (P13 runs bounded cycles)")
                if isinstance(node, ast.Attribute) and node.attr in ("fork", "daemon"):
                    self.fail(f"{path.name}: {node.attr}")

    def test_only_the_evidence_store_writes(self):
        writers = []
        for path, tree in self._modules().items():
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    f = node.func
                    name = getattr(f, "attr", getattr(f, "id", ""))
                    if name in ("write_text", "write_bytes", "mkdir", "unlink", "rename",
                                "rmdir", "touch", "symlink_to", "chmod"):
                        writers.append(path.name)
                    # `replace` is also str.replace; only os.replace / Path.replace write.
                    if name == "replace" and len(node.args) == 1:
                        writers.append(path.name)
                    if name == "open" and len(node.args) > 1:
                        writers.append(path.name)
        self.assertEqual(set(writers), {"evidence.py"})

    def test_native_core_is_eleven_and_p13_is_not_in_it(self):
        core = REPO_ROOT / "native_core/core"
        self.assertEqual(len([d for d in core.iterdir()
                              if d.is_dir() and not d.name.startswith("__")]), 11)
        self.assertFalse((core / "p13").exists())

    def test_every_executable_action_is_a_read_only_verifier_or_an_s_ops_transition(self):
        # FDR-3 (Decision Register §23) grants the two S-OPS transitions, and
        # P13-ENV-02 records them. Every other executable type stays a
        # read-only verifier.
        for action in CATALOG.values():
            if action.run is not None:
                self.assertFalse(action.reserved)
                if action.name in ("s_ops.open", "s_ops.close"):
                    self.assertEqual(action.executor, "tools.s_ops.surface.transition")
                else:
                    self.assertTrue(action.name.startswith("verify."), action.name)
                    self.assertEqual(action.effect, "read-only", action.name)
        for name in RESERVED:
            self.assertIsNone(CATALOG[name].run)

    def test_the_live_root_is_live_and_never_certified(self):
        self.assertEqual(LIVE_ROOT, "docs/operations/p13")
        self.assertFalse(barrier.refuses(REPO_ROOT / LIVE_ROOT / "cycles/x.json"))


if __name__ == "__main__":
    unittest.main()
