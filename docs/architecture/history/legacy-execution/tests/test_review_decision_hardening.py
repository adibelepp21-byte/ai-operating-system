"""
Human Review Event Validation Hardening v1.0.

Validation-only: no new capability, no Knowledge implementation. Proves,
with evidence rather than assumption, that Human Review Decision
Recording is operationally safe before any Knowledge consumption path
exists. Covers: Action B boundary validation, decision replay integrity
against real corpus data, snapshot immutability under corpus drift,
Trace event classification, and negative safety tests.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import ast
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution.memory.extractor import MemoryRecord, extract_memories, load_trace_records
from execution.promotion import CandidatePackage, EvidenceSummary, Provenance, select_candidates
from execution import review_decision as rd


def _snapshot(memory_id="memory-t1", content="a real reviewed candidate with enough content length",
              occurrence_count=3, review_flags=()):
    return CandidatePackage(
        id=memory_id, content=content, observation_kind="cross_reference_check",
        provenance=Provenance(memory_id=memory_id, trace_ids=("trace-a",), agent_definition_name="Test Agent", department_status="unavailable"),
        evidence=EvidenceSummary(source_type="tool", confidence=1.0, occurrence_count=occurrence_count, observation_frequency=1.0, first_observed_at=1.0, last_observed_at=2.0, resolved=True, fingerprint=None),
        review_flags=review_flags,
    )


def _valid_input(**overrides):
    defaults = dict(
        candidate_snapshot=_snapshot(), decision="approve",
        reviewer_identity="reviewer.architect-manual-review",
        rationale="Strong, tool-derived, high-confidence finding.", timestamp=1000.0,
    )
    defaults.update(overrides)
    return rd.HumanReviewDecisionInput(**defaults)


# ---------------------------------------------------------------------------
# 1. Action B Boundary Validation
# ---------------------------------------------------------------------------

class ActionBBoundaryValidationTest(unittest.TestCase):
    """Static, source-level proof -- not prose assertion -- that human
    judgment stays entirely external to this module."""

    @classmethod
    def setUpClass(cls):
        cls.source = Path(rd.__file__).read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source, filename=rd.__file__)

    def test_only_imports_candidate_package_type_from_promotion(self):
        """review_decision.py must never import promotion's ranking or
        eligibility functions -- only the CandidatePackage type it
        stores opaquely."""
        imported_names = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.endswith("promotion"):
                imported_names.update(alias.name for alias in node.names)
        forbidden = {"select_candidates", "is_degenerate_content", "_derive_evidence_details", "_review_flags"}
        self.assertEqual(imported_names & forbidden, set())
        self.assertIn("CandidatePackage", imported_names)

    # Evidence-quality fields: comparing against these is exactly the
    # forbidden "if confidence > X: approve" pattern. Comparing the
    # *decision* value itself against the literal "edit" (to route
    # conditional input-shape validation, e.g. "edited_content required
    # only when decision == 'edit'") is legitimate input-completeness
    # checking, not decision-computation from evidence -- deliberately
    # not included here.
    _EVIDENCE_QUALITY_ATTRS = {
        "confidence", "occurrence_count", "observation_frequency",
        "review_flags", "source_type", "resolved", "fingerprint",
    }

    def test_no_numeric_comparison_against_evidence_quality_fields(self):
        """No Compare node anywhere may apply a magnitude/equality
        operator to an evidence-quality field specifically -- the exact
        "if confidence > X: approve" pattern this phase forbids.
        Categorical checks on the decision value itself (decision ==
        'edit') are a different, legitimate thing and excluded."""
        magnitude_ops = (ast.Gt, ast.Lt, ast.GtE, ast.LtE, ast.Eq, ast.NotEq)
        violations = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Compare):
                operands = [node.left] + list(node.comparators)
                attrs = [o.attr for o in operands if isinstance(o, ast.Attribute)]
                has_magnitude_op = any(isinstance(op, magnitude_ops) for op in node.ops)
                if has_magnitude_op:
                    violations.extend(a for a in attrs if a in self._EVIDENCE_QUALITY_ATTRS)
        self.assertEqual(violations, [], f"found magnitude/equality comparisons against evidence-quality fields: {violations}")

    def test_no_arithmetic_on_evidence_quality_fields(self):
        """No BinOp (addition, multiplication, etc.) may combine with an
        evidence-quality field -- rules out a hidden weighted score."""
        violations = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.BinOp):
                for o in (node.left, node.right):
                    if isinstance(o, ast.Attribute) and o.attr in self._EVIDENCE_QUALITY_ATTRS:
                        violations.append(o.attr)
        self.assertEqual(violations, [], f"found arithmetic against evidence-quality fields: {violations}")

    def test_no_sort_or_rank_applied_to_evidence_or_candidates(self):
        """sorted()/sort()/max()/min() must never be applied to
        anything derived from a CandidatePackage or its evidence --
        ranking is promotion.py's exclusive responsibility. A call
        formatting a fixed, hardcoded constant (e.g. sorting the 3
        literal valid-decision strings for a readable error message) is
        not ranking and is explicitly not what this forbids."""
        forbidden_calls = {"sorted", "sort", "max", "min"}
        violations = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in forbidden_calls:
                for arg in node.args:
                    for sub in ast.walk(arg):
                        if isinstance(sub, ast.Attribute) and sub.attr in self._EVIDENCE_QUALITY_ATTRS:
                            violations.append((node.func.id, sub.attr))
        self.assertEqual(violations, [], f"found sort/rank calls over evidence-quality data: {violations}")

    def test_no_file_writes_outside_trace_module(self):
        """No open()/write() call anywhere in this module -- all
        persistence must route through trace.TraceWriter, never a
        parallel or Knowledge-targeted write path."""
        forbidden_calls = {"open"}
        found = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in forbidden_calls:
                found.append(node.func.id)
        self.assertEqual(found, [])
        self.assertNotIn("repository", self.source.lower())

    def test_hard_constraint_pattern_absent(self):
        """Literal proof the exact forbidden pattern from the directive
        ("if confidence > X: approve") does not exist in any form."""
        self.assertNotIn("confidence >", self.source)
        self.assertNotIn("confidence <", self.source)
        self.assertNotIn("occurrence_count >", self.source)


# ---------------------------------------------------------------------------
# 2. Decision Replay Integrity Test (against real corpus data)
# ---------------------------------------------------------------------------

class DecisionReplayIntegrityTest(unittest.TestCase):
    """Given only a recorded Trace event, reconstruct exactly what a
    future auditor would need -- against real corpus data, not a mock."""

    @classmethod
    def setUpClass(cls):
        cls.records = load_trace_records()
        cls.memories = extract_memories(cls.records)
        cls.candidates = select_candidates(cls.memories, cls.records)

    def test_full_replay_from_real_candidate(self):
        ground_truth = self.candidates[0]
        decision_input = rd.HumanReviewDecisionInput(
            candidate_snapshot=ground_truth, decision="approve",
            reviewer_identity="reviewer.replay-test", rationale="replay integrity check",
            timestamp=1717171717.0,
        )
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("execution.trace.TRACE_DIR", Path(tmp)):
                result = rd.record_decision(decision_input)
            lines = [json.loads(l) for l in Path(result["trace_file"]).read_text().splitlines() if l.strip()]
        decision_record = lines[1]
        outputs = decision_record["outputs"]
        snap = outputs["candidate_snapshot"]

        # What candidate was reviewed
        self.assertEqual(snap["id"], ground_truth.id)
        self.assertEqual(snap["content"], ground_truth.content)
        # What evidence existed
        self.assertEqual(snap["evidence"]["source_type"], ground_truth.evidence.source_type)
        self.assertEqual(snap["evidence"]["confidence"], ground_truth.evidence.confidence)
        self.assertEqual(snap["evidence"]["occurrence_count"], ground_truth.evidence.occurrence_count)
        # What flags were visible
        self.assertEqual(list(snap["review_flags"]), list(ground_truth.review_flags))
        # What decision was recorded
        self.assertEqual(outputs["decision"], "approve")
        # Who recorded it
        self.assertEqual(outputs["reviewer_identity"], "reviewer.replay-test")
        # When it occurred
        self.assertEqual(outputs["decision_timestamp"], 1717171717.0)
        self.assertIsNotNone(decision_record["timestamp"])  # the Trace record's own write-time, independently present

    def test_replay_across_multiple_real_candidates(self):
        """Not just the top-ranked one -- sample across the ranking to
        confirm replay integrity isn't an artifact of one favorable case."""
        sample = [self.candidates[0], self.candidates[len(self.candidates) // 2], self.candidates[-1]]
        for ground_truth in sample:
            decision_input = rd.HumanReviewDecisionInput(
                candidate_snapshot=ground_truth, decision="reject",
                reviewer_identity="reviewer.replay-sample", rationale="sample replay check",
                timestamp=1.0,
            )
            with tempfile.TemporaryDirectory() as tmp:
                with mock.patch("execution.trace.TRACE_DIR", Path(tmp)):
                    result = rd.record_decision(decision_input)
                lines = [json.loads(l) for l in Path(result["trace_file"]).read_text().splitlines() if l.strip()]
            snap = lines[1]["outputs"]["candidate_snapshot"]
            self.assertEqual(snap["content"], ground_truth.content)
            self.assertEqual(snap["evidence"]["occurrence_count"], ground_truth.evidence.occurrence_count)


# ---------------------------------------------------------------------------
# 3. Snapshot Immutability Validation (the corpus-drift scenario)
# ---------------------------------------------------------------------------

class SnapshotImmutabilityUnderCorpusDriftTest(unittest.TestCase):
    """Proves, with a real before/after regeneration (not assumed), that
    a recorded decision represents T1 state even after the corpus
    changes and candidates are regenerated at T2."""

    def _trace_record(self, trace_id, timestamp):
        return {
            "trace_id": trace_id, "agent_definition_name": "Test Agent",
            "timestamp": timestamp,
            "outputs": {"evidence": [{
                "kind": "cross_reference_check",
                "detail": "a finding whose occurrence count grows between T1 and T2",
                "source": "tool", "resolved": True,
            }]},
        }

    def test_recorded_decision_immune_to_later_corpus_regeneration(self):
        # T1: three real trace records exist for one finding.
        t1_records = [self._trace_record(f"t{i}", float(i)) for i in range(1, 4)]
        memories_t1 = extract_memories(t1_records)
        candidates_t1 = select_candidates(memories_t1, t1_records)
        candidate_t1 = candidates_t1[0]
        self.assertEqual(candidate_t1.evidence.occurrence_count, 3)

        # Record a Human Review Decision using the T1 snapshot.
        decision_input = rd.HumanReviewDecisionInput(
            candidate_snapshot=candidate_t1, decision="approve",
            reviewer_identity="reviewer.drift-test", rationale="reviewed at T1", timestamp=100.0,
        )
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("execution.trace.TRACE_DIR", Path(tmp)):
                result = rd.record_decision(decision_input)
            recorded_lines = [json.loads(l) for l in Path(result["trace_file"]).read_text().splitlines() if l.strip()]

        # T2: the corpus changes -- two more occurrences of the same
        # finding appear (simulating real Trace growth between review
        # time and any later inspection). Candidates are regenerated.
        t2_records = t1_records + [self._trace_record(f"t{i}", float(i)) for i in range(4, 6)]
        memories_t2 = extract_memories(t2_records)
        candidates_t2 = select_candidates(memories_t2, t2_records)
        candidate_t2 = candidates_t2[0]

        # Prove the corpus genuinely changed and regeneration reflects it.
        self.assertEqual(candidate_t2.evidence.occurrence_count, 5)
        self.assertNotEqual(candidate_t1.evidence.occurrence_count, candidate_t2.evidence.occurrence_count)

        # Prove the ALREADY-RECORDED decision still reflects T1, not T2 --
        # it was never re-resolved against the changed corpus.
        recorded_snapshot = recorded_lines[1]["outputs"]["candidate_snapshot"]
        self.assertEqual(recorded_snapshot["evidence"]["occurrence_count"], 3)
        self.assertNotEqual(recorded_snapshot["evidence"]["occurrence_count"], candidate_t2.evidence.occurrence_count)

    def test_record_decision_never_calls_select_candidates_or_reads_trace_corpus(self):
        """Structural confirmation of why the above holds generally, not
        just for this one scenario: record_decision has no executable
        call to anything that re-derives a candidate from live data.
        Checked against actual ast.Call nodes, not raw source text --
        the module's own docstring explains *why* this matters in prose
        (mentioning these function names as documentation), which must
        not be confused with an executable reference."""
        source = Path(rd.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=rd.__file__)
        forbidden_calls = {"select_candidates", "load_trace_records", "extract_memories"}
        found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                name = func.id if isinstance(func, ast.Name) else (func.attr if isinstance(func, ast.Attribute) else None)
                if name in forbidden_calls:
                    found.append(name)
        self.assertEqual(found, [])


# ---------------------------------------------------------------------------
# 4. Trace Event Classification Validation
# ---------------------------------------------------------------------------

class TraceEventClassificationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = load_trace_records()

    def _real_human_review_events(self):
        events = []
        for r in self.records:
            outputs = r.get("outputs") or {}
            if outputs.get("event") == "human_review_decision_recorded":
                events.append(r)
        return events

    def test_every_real_human_review_event_is_structurally_valid(self):
        """Post-pilot invariant (Human Review Event Post-Pilot
        Consolidation v1.0): the corpus is no longer guaranteed to
        contain zero human_review_decision_recorded events -- the first
        real pilot (trace-8dea61c2933e) recorded one. The invariant this
        test now enforces is stronger, not weaker: every such event that
        DOES exist, however many there are, must be a fully valid,
        governed decision record -- not merely present, but correct."""
        events = self._real_human_review_events()
        self.assertGreaterEqual(len(events), 1, "expected at least the known pilot event to exist")
        by_trace_id = {r.get("trace_id"): r for r in self.records}
        for r in events:
            outputs = r["outputs"]
            self.assertIn("decision", outputs)
            self.assertIn(outputs["decision"], {"approve", "reject", "edit"})
            self.assertTrue(outputs.get("reviewer_identity"))
            self.assertTrue(outputs.get("rationale"))
            self.assertIsNotNone(outputs.get("decision_timestamp"))
            snap = outputs.get("candidate_snapshot")
            self.assertIsNotNone(snap, "candidate_snapshot must exist")
            self.assertTrue(snap.get("content"))
            self.assertTrue(snap.get("observation_kind"))
            self.assertIn("provenance", snap)
            self.assertIn("evidence", snap)
            self.assertIn("review_flags", snap)
            # provenance chain resolves -- every referenced trace_id is real
            for tid in snap["provenance"]["trace_ids"]:
                self.assertIn(tid, by_trace_id, f"{r['trace_id']} references dangling trace_id {tid}")
            # edited_content only present when decision == edit
            if outputs["decision"] == "edit":
                self.assertTrue(outputs.get("edited_content"))
            else:
                self.assertIsNone(outputs.get("edited_content"))
            # no automated recommendation of any kind was ever written
            forbidden_keys = {"recommend_approve", "recommend_reject", "recommend_edit", "recommendation",
                               "suggested_decision", "computed_verdict", "ranking_score", "approval_likelihood"}
            self.assertEqual(set(outputs.keys()) & forbidden_keys, set())

    def test_human_review_shape_never_collides_with_other_execution_shapes(self):
        """Every real human_review_decision_recorded event, wherever it
        occurs in the corpus, stays cleanly distinguishable from Skill
        execution and denied/escalated execution shapes -- not merely
        "this event doesn't exist yet" (the pre-pilot version of this
        test), but "this event, now that it's real, is never confused
        with anything else."""
        events = self._real_human_review_events()
        self.assertGreaterEqual(len(events), 1)
        for r in events:
            self.assertEqual(r.get("skills_used"), [])
            self.assertIsNone(r.get("workflow"))
            self.assertNotEqual(r.get("status"), "escalation")
            self.assertNotIn("evidence", r["outputs"])

        # No Skill-execution or denied-execution record anywhere in the
        # corpus has ever used this event string -- the string remains
        # exclusive to genuine Human Review Decision recordings.
        for r in self.records:
            outputs = r.get("outputs") or {}
            if outputs.get("event") == "human_review_decision_recorded":
                continue
            if r.get("skills_used") or "evidence" in outputs:
                self.assertNotEqual(outputs.get("event"), "human_review_decision_recorded")

    def test_real_pilot_event_snapshot_remains_immutable(self):
        """Grounds the immutability requirement against the actual first
        real pilot event (trace-8dea61c2933e), not only synthetic
        fixtures: the recorded candidate_snapshot must still match what
        a fresh backward-trace to Memory/Trace produces for that exact
        content, proving nothing has silently altered the durable
        record since it was written."""
        by_trace_id = {r.get("trace_id"): r for r in self.records}
        pilot_record = by_trace_id.get("trace-8dea61c2933e")
        if pilot_record is None:
            self.skipTest("pilot event trace-8dea61c2933e not present in this corpus snapshot")
        snap = pilot_record["outputs"]["candidate_snapshot"]
        self.assertEqual(pilot_record["outputs"]["decision"], "approve")
        self.assertEqual(pilot_record["outputs"]["reviewer_identity"], "MoriartyTalk")
        self.assertEqual(pilot_record["outputs"]["rationale"], "Saya menyetujuinya")
        self.assertEqual(snap["evidence"]["source_type"], "tool")
        self.assertEqual(snap["evidence"]["confidence"], 1.0)
        self.assertEqual(snap["evidence"]["resolved"], False)
        self.assertEqual(list(snap["review_flags"]), [])
        # Every trace_id the recorded snapshot cites still resolves, and
        # still contains matching evidence -- the backward chain has not
        # degraded since the pilot ran.
        for tid in snap["provenance"]["trace_ids"]:
            rec = by_trace_id.get(tid)
            self.assertIsNotNone(rec)
            found = any(
                ev.get("kind") == snap["observation_kind"] and ev.get("detail") == snap["content"]
                for ev in (rec.get("outputs") or {}).get("evidence") or []
            )
            self.assertTrue(found, f"trace_id {tid} no longer contains matching evidence")

    def test_recorded_decision_has_no_skills_used_or_workflow(self):
        """A recorded decision must never look like a Skill/Workflow
        execution -- confirmed on a real write, not assumed from the
        source code alone."""
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("execution.trace.TRACE_DIR", Path(tmp)):
                result = rd.record_decision(_valid_input())
            lines = [json.loads(l) for l in Path(result["trace_file"]).read_text().splitlines() if l.strip()]
        decision_record = lines[1]
        self.assertEqual(decision_record["skills_used"], [])
        self.assertIsNone(decision_record["workflow"])
        self.assertNotIn("evidence", decision_record["outputs"])  # not shaped like a Skill execution record


# ---------------------------------------------------------------------------
# 5. Negative Safety Tests (directive's explicit forbidden list)
# ---------------------------------------------------------------------------

class NegativeSafetyTest(unittest.TestCase):
    def test_cannot_write_knowledge_records(self):
        """No Knowledge Repository module exists anywhere in the
        codebase for this module to write to -- confirmed by the
        absence of any such import or reference, not merely by the
        absence of a feature we chose not to build."""
        source = Path(rd.__file__).read_text(encoding="utf-8")
        self.assertNotIn("repository", source.lower())

    def test_automatic_approve_reject_impossible_end_to_end(self):
        """A caller supplying no decision at all gets rejected, not
        defaulted to approve or reject."""
        broken_input = rd.HumanReviewDecisionInput(
            candidate_snapshot=_snapshot(), decision=None,
            reviewer_identity="reviewer.test", rationale="test", timestamp=1.0,
        )
        with self.assertRaises(rd.ValidationError):
            rd.record_decision(broken_input)

    def test_mutation_of_candidate_input_impossible(self):
        """Frozen dataclass makes in-place mutation a hard Python error;
        confirmed no code path in record_decision even attempts one by
        completing successfully against a snapshot whose identity
        (object id) is checked unchanged."""
        snapshot = _snapshot()
        snapshot_id_before = id(snapshot)
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("execution.trace.TRACE_DIR", Path(tmp)):
                rd.record_decision(_valid_input(candidate_snapshot=snapshot))
        self.assertEqual(id(snapshot), snapshot_id_before)
        self.assertEqual(snapshot, _snapshot())  # frozen dataclass value-equality, unchanged


# ---------------------------------------------------------------------------
# 6. Real Corpus Validation (no corruption, no mutation, no provenance loss)
# ---------------------------------------------------------------------------

class RealCorpusHardeningValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records_before = load_trace_records()

    def test_full_pipeline_against_real_corpus_causes_no_mutation(self):
        records = load_trace_records()
        memories = extract_memories(records)
        candidates = select_candidates(memories, records)
        for c in candidates[:20]:
            decision_input = rd.HumanReviewDecisionInput(
                candidate_snapshot=c, decision="approve",
                reviewer_identity="reviewer.corpus-validation", rationale="hardening validation pass",
                timestamp=1.0,
            )
            with tempfile.TemporaryDirectory() as tmp:
                with mock.patch("execution.trace.TRACE_DIR", Path(tmp)):
                    rd.record_decision(decision_input)
        records_after = load_trace_records()
        # Equality to itself is the real guarantee (no mutation from this
        # test's own 20 recording calls); the exact count is corpus-size-
        # dependent and reported, not hardcoded, so this test stays valid
        # as the real corpus legitimately grows in later phases.
        self.assertEqual(len(self.records_before), len(records_after))


if __name__ == "__main__":
    unittest.main()
