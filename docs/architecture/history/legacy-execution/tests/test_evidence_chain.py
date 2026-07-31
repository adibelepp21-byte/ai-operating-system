"""
Evidence Chain Auditability Hardening v1.0 — dedicated chain tests.

Exercises the full backward lineage Trace -> Memory -> Promotion
Candidate -> Human Review Decision -> (back to) original Trace evidence,
against the real, on-disk corpus wherever possible, plus targeted
synthetic fixtures for the fail-closed/no-guessing guarantees that are
hard to force via real data alone.

Run with:
    python3 -m unittest discover -s execution/tests
"""

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


class TraceToMemoryLineageTest(unittest.TestCase):
    """1. Trace -> Memory lineage survives."""

    @classmethod
    def setUpClass(cls):
        cls.records = load_trace_records()
        cls.by_trace_id = {r.get("trace_id"): r for r in cls.records}
        cls.memories = extract_memories(cls.records)

    def test_every_memory_source_trace_id_resolves_to_a_real_trace_record(self):
        for m in self.memories:
            for tid in m.source_trace_ids:
                self.assertIn(tid, self.by_trace_id, f"memory {m.memory_id} references dangling trace_id {tid}")

    def test_every_memory_content_recoverable_as_real_evidence_in_its_own_traces(self):
        for m in self.memories:
            found = False
            for tid in m.source_trace_ids:
                rec = self.by_trace_id.get(tid)
                if not rec:
                    continue
                for ev in (rec.get("outputs") or {}).get("evidence") or []:
                    if ev.get("kind") == m.observation_kind and ev.get("detail") == m.content:
                        found = True
                        break
                if found:
                    break
            self.assertTrue(found, f"memory {m.memory_id} content not recoverable from any of its own source traces")

    def test_timestamps_derived_from_real_trace_timestamps_not_wall_clock(self):
        for m in self.memories[:20]:  # sample -- full corpus checked in the source-recovery test above
            trace_timestamps = [self.by_trace_id[t]["timestamp"] for t in m.source_trace_ids if t in self.by_trace_id]
            if not trace_timestamps:
                continue
            self.assertEqual(m.first_observed_at, min(trace_timestamps))
            self.assertEqual(m.last_observed_at, max(trace_timestamps))


class MemoryToCandidateLineageTest(unittest.TestCase):
    """2. Memory -> Candidate lineage survives."""

    @classmethod
    def setUpClass(cls):
        cls.records = load_trace_records()
        cls.memories = extract_memories(cls.records)
        cls.candidates = select_candidates(cls.memories, cls.records)
        cls.memories_by_id = {m.memory_id: m for m in cls.memories}

    def test_every_candidate_traces_back_to_a_real_memory_record(self):
        for c in self.candidates:
            self.assertIn(c.provenance.memory_id, self.memories_by_id)

    def test_candidate_confidence_and_occurrence_match_source_memory_exactly(self):
        for c in self.candidates:
            m = self.memories_by_id[c.provenance.memory_id]
            self.assertEqual(c.evidence.confidence, m.confidence)
            self.assertEqual(c.evidence.occurrence_count, m.occurrence_count)
            self.assertEqual(c.evidence.observation_frequency, m.observation_frequency)

    def test_source_resolved_fingerprint_recovered_where_determinable(self):
        """The Evidence Chain Auditability Hardening fix: source, resolved,
        and fingerprint are recovered from original Trace evidence, not
        just source alone."""
        resolved_recovered = sum(1 for c in self.candidates if c.evidence.resolved is not None)
        fingerprint_recovered = sum(1 for c in self.candidates if c.evidence.fingerprint is not None)
        self.assertGreater(resolved_recovered, 0)
        self.assertGreater(fingerprint_recovered, 0)

    def test_no_candidate_has_unknown_source_in_current_corpus(self):
        unresolved = [c for c in self.candidates if c.evidence.source_type == "unknown"]
        self.assertEqual(unresolved, [])


class CandidateSnapshotImmutabilityTest(unittest.TestCase):
    """3. Candidate snapshot remains unchanged after review recording."""

    def setUp(self):
        self.snapshot = CandidatePackage(
            id="memory-x", content="a real observation of sufficient length to be eligible",
            observation_kind="cross_reference_check",
            provenance=Provenance(memory_id="memory-x", trace_ids=("trace-1",), agent_definition_name="Test Agent", department_status="unavailable"),
            evidence=EvidenceSummary(source_type="tool", confidence=1.0, occurrence_count=3, observation_frequency=1.0, first_observed_at=1.0, last_observed_at=2.0, resolved=False, fingerprint=("k=v",)),
            review_flags=("low_confidence",),
        )
        self.original_repr = repr(self.snapshot)

    def _record(self, tmp):
        decision_input = rd.HumanReviewDecisionInput(
            candidate_snapshot=self.snapshot, decision="approve",
            reviewer_identity="reviewer.test", rationale="test rationale", timestamp=1.0,
        )
        with mock.patch("execution.trace.TRACE_DIR", Path(tmp)):
            return rd.record_decision(decision_input)

    def test_snapshot_object_unchanged_after_recording(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._record(tmp)
        self.assertEqual(repr(self.snapshot), self.original_repr)

    def test_recorded_snapshot_matches_original_field_by_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._record(tmp)
            lines = [json.loads(l) for l in Path(result["trace_file"]).read_text().splitlines() if l.strip()]
        stored = lines[1]["outputs"]["candidate_snapshot"]
        self.assertEqual(stored["id"], self.snapshot.id)
        self.assertEqual(stored["content"], self.snapshot.content)
        self.assertEqual(stored["observation_kind"], self.snapshot.observation_kind)
        self.assertEqual(stored["evidence"]["confidence"], self.snapshot.evidence.confidence)
        self.assertEqual(stored["evidence"]["resolved"], self.snapshot.evidence.resolved)
        self.assertEqual(list(stored["evidence"]["fingerprint"]), list(self.snapshot.evidence.fingerprint))
        self.assertEqual(list(stored["review_flags"]), list(self.snapshot.review_flags))
        self.assertEqual(stored["provenance"]["trace_ids"], list(self.snapshot.provenance.trace_ids))


class ReviewDecisionReferencesOriginalEvidenceTest(unittest.TestCase):
    """4. Review Decision can always reference original evidence -- the
    full end-to-end chain, against real corpus data."""

    def test_full_chain_trace_to_memory_to_candidate_to_decision_to_original_evidence(self):
        records = load_trace_records()
        by_trace_id = {r.get("trace_id"): r for r in records}
        memories = extract_memories(records)
        candidates = select_candidates(memories, records)
        top = candidates[0]

        decision_input = rd.HumanReviewDecisionInput(
            candidate_snapshot=top, decision="approve",
            reviewer_identity="reviewer.chain-test", rationale="chain integrity check", timestamp=1.0,
        )
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("execution.trace.TRACE_DIR", Path(tmp)):
                result = rd.record_decision(decision_input)
            lines = [json.loads(l) for l in Path(result["trace_file"]).read_text().splitlines() if l.strip()]

        decision_record = lines[1]
        stored_snapshot = decision_record["outputs"]["candidate_snapshot"]

        # Walk backward from the decision record to the original Trace evidence
        # it claims to justify -- using only what the decision record itself
        # stored, exactly as a future auditor would have to.
        original_trace_ids = stored_snapshot["provenance"]["trace_ids"]
        self.assertTrue(original_trace_ids)
        found_original_evidence = False
        for tid in original_trace_ids:
            real_record = by_trace_id.get(tid)
            self.assertIsNotNone(real_record, f"decision references trace_id {tid} not present in the real corpus")
            for ev in (real_record.get("outputs") or {}).get("evidence") or []:
                if ev.get("kind") == stored_snapshot["observation_kind"] and ev.get("detail") == stored_snapshot["content"]:
                    found_original_evidence = True
                    break
            if found_original_evidence:
                break
        self.assertTrue(found_original_evidence, "decision record's snapshot content is not recoverable from any referenced original trace evidence")

    def test_edited_content_comparable_against_original(self):
        snapshot = CandidatePackage(
            id="memory-y", content="the original unedited observation text is preserved here",
            observation_kind="uncited_restatement_flag",
            provenance=Provenance(memory_id="memory-y", trace_ids=("trace-1",), agent_definition_name="Test Agent", department_status="unavailable"),
            evidence=EvidenceSummary(source_type="heuristic", confidence=0.6, occurrence_count=1, observation_frequency=1.0, first_observed_at=1.0, last_observed_at=1.0, resolved=None, fingerprint=None),
            review_flags=("heuristic_source", "verbatim_quote"),
        )
        decision_input = rd.HumanReviewDecisionInput(
            candidate_snapshot=snapshot, decision="edit",
            reviewer_identity="reviewer.test", rationale="rewritten for clarity", timestamp=1.0,
            edited_content="A synthesized, standalone rewrite of the original observation.",
        )
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("execution.trace.TRACE_DIR", Path(tmp)):
                result = rd.record_decision(decision_input)
            lines = [json.loads(l) for l in Path(result["trace_file"]).read_text().splitlines() if l.strip()]
        outputs = lines[1]["outputs"]
        # Both the original (inside the snapshot) and the edited text are
        # present side by side in the same record -- directly diffable.
        self.assertEqual(outputs["candidate_snapshot"]["content"], "the original unedited observation text is preserved here")
        self.assertEqual(outputs["edited_content"], "A synthesized, standalone rewrite of the original observation.")
        self.assertNotEqual(outputs["candidate_snapshot"]["content"], outputs["edited_content"])


class MissingProvenanceFailsExplicitlyTest(unittest.TestCase):
    """5. Missing provenance fails explicitly. 6. No silent fallback or
    guessing occurs."""

    def test_memory_with_dangling_trace_reference_resolves_unknown_not_guessed(self):
        fake_memory = MemoryRecord(
            memory_id="memory-dangling", agent_instance_ids=("instance-1",),
            source_trace_ids=("trace-does-not-exist",), observation_kind="cross_reference_check",
            content="an observation whose source trace record has vanished",
            occurrence_count=1, observation_frequency=1.0, confidence=1.0,
            first_observed_at=1.0, last_observed_at=1.0, created_at=1.0,
            retention_seconds=3600, status="provisional",
        )
        candidates = select_candidates([fake_memory], [])  # no trace records at all -- dangling by construction
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].evidence.source_type, "unknown")
        self.assertIsNone(candidates[0].evidence.resolved)
        self.assertIsNone(candidates[0].evidence.fingerprint)

    def test_record_decision_rejects_missing_provenance_fields(self):
        broken_snapshot = CandidatePackage(
            id="memory-z", content="a candidate missing its provenance object entirely",
            observation_kind="cross_reference_check",
            provenance=None,  # simulates a caller failing to supply provenance
            evidence=EvidenceSummary(source_type="tool", confidence=1.0, occurrence_count=1, observation_frequency=1.0, first_observed_at=1.0, last_observed_at=1.0, resolved=True, fingerprint=None),
            review_flags=(),
        )
        decision_input = rd.HumanReviewDecisionInput(
            candidate_snapshot=broken_snapshot, decision="approve",
            reviewer_identity="reviewer.test", rationale="test", timestamp=1.0,
        )
        errors = rd.validate_decision_input(decision_input)
        self.assertTrue(any("provenance" in e for e in errors))
        with self.assertRaises(rd.ValidationError):
            rd.record_decision(decision_input)

    def test_disagreeing_fingerprint_across_occurrences_reported_as_none_not_guessed(self):
        records = [
            {"trace_id": "t1", "outputs": {"evidence": [
                {"kind": "cross_reference_check", "detail": "a stable finding with disagreeing fingerprints", "source": "tool", "resolved": True, "fingerprint": ["a=1"]},
            ]}, "timestamp": 1.0},
            {"trace_id": "t2", "outputs": {"evidence": [
                {"kind": "cross_reference_check", "detail": "a stable finding with disagreeing fingerprints", "source": "tool", "resolved": True, "fingerprint": ["a=2"]},
            ]}, "timestamp": 2.0},
        ]
        memory = MemoryRecord(
            memory_id="memory-conflict", agent_instance_ids=("i1", "i2"),
            source_trace_ids=("t1", "t2"), observation_kind="cross_reference_check",
            content="a stable finding with disagreeing fingerprints",
            occurrence_count=2, observation_frequency=1.0, confidence=1.0,
            first_observed_at=1.0, last_observed_at=2.0, created_at=1.0,
            retention_seconds=3600, status="provisional",
        )
        candidates = select_candidates([memory], records)
        self.assertEqual(candidates[0].evidence.source_type, "tool")  # source/resolved genuinely agree
        self.assertTrue(candidates[0].evidence.resolved)
        self.assertIsNone(candidates[0].evidence.fingerprint)  # but a real conflict -> unresolvable, not guessed

    def test_generational_fingerprint_absence_not_treated_as_conflict(self):
        """One occurrence predates fingerprint recording (None), the other
        postdates it -- this must resolve cleanly to the recorded value,
        not be treated as a disagreement. This is the exact real-corpus
        regression this hardening phase found and fixed."""
        records = [
            {"trace_id": "t1", "outputs": {"evidence": [
                {"kind": "cross_reference_check", "detail": "a finding observed before and after fingerprinting existed", "source": "tool", "resolved": False},
            ]}, "timestamp": 1.0},
            {"trace_id": "t2", "outputs": {"evidence": [
                {"kind": "cross_reference_check", "detail": "a finding observed before and after fingerprinting existed", "source": "tool", "resolved": False, "fingerprint": ["a=1"]},
            ]}, "timestamp": 2.0},
        ]
        memory = MemoryRecord(
            memory_id="memory-generational", agent_instance_ids=("i1", "i2"),
            source_trace_ids=("t1", "t2"), observation_kind="cross_reference_check",
            content="a finding observed before and after fingerprinting existed",
            occurrence_count=2, observation_frequency=1.0, confidence=1.0,
            first_observed_at=1.0, last_observed_at=2.0, created_at=1.0,
            retention_seconds=3600, status="provisional",
        )
        candidates = select_candidates([memory], records)
        self.assertEqual(candidates[0].evidence.source_type, "tool")
        self.assertEqual(candidates[0].evidence.resolved, False)
        self.assertEqual(candidates[0].evidence.fingerprint, ("a=1",))


if __name__ == "__main__":
    unittest.main()
