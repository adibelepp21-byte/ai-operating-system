"""
Regression tests for execution/human_review_observation.py.

Uses only the standard library (unittest), consistent with the rest of
execution/tests/. Synthetic fixtures for mechanical correctness; a real-
corpus check confirms the module reads the actual pilot event correctly.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution.memory.extractor import load_trace_records
from execution.human_review_observation import (
    decision_distribution, extract_human_review_events, optional_field_usage,
    rationale_stats, review_flag_interaction,
)


def _event(decision="approve", rationale="short", reviewer_identity="reviewer.x",
           review_flags=(), department_override=None, reviewer_confidence=None, additional_notes=None):
    return {
        "outputs": {
            "event": "human_review_decision_recorded",
            "decision": decision, "rationale": rationale, "reviewer_identity": reviewer_identity,
            "department_override": department_override, "reviewer_confidence": reviewer_confidence,
            "additional_notes": additional_notes,
            "candidate_snapshot": {"review_flags": list(review_flags)},
        }
    }


class ExtractionTest(unittest.TestCase):
    def test_extracts_only_human_review_events(self):
        records = [_event(), {"outputs": {"event": "spawned"}}, {"outputs": {"evidence": []}}]
        events = extract_human_review_events(records)
        self.assertEqual(len(events), 1)


class DecisionDistributionTest(unittest.TestCase):
    def test_counts_each_decision_type(self):
        events = [_event(decision="approve"), _event(decision="approve"), _event(decision="reject"), _event(decision="edit")]
        dist = decision_distribution(events)
        self.assertEqual(dist.total, 4)
        self.assertEqual(dist.approve, 2)
        self.assertEqual(dist.reject, 1)
        self.assertEqual(dist.edit, 1)


class RationaleStatsTest(unittest.TestCase):
    def test_length_stats(self):
        events = [_event(rationale="ab"), _event(rationale="abcd")]
        rs = rationale_stats(events)
        self.assertEqual(rs.count, 2)
        self.assertEqual(rs.lengths, (2, 4))
        self.assertEqual(rs.min_length, 2)
        self.assertEqual(rs.max_length, 4)
        self.assertEqual(rs.mean_length, 3.0)

    def test_evidence_keyword_detection_is_substring_only(self):
        events = [_event(rationale="high confidence finding"), _event(rationale="just approving this")]
        rs = rationale_stats(events)
        self.assertEqual(rs.events_referencing_evidence_keywords, 1)

    def test_empty_events_returns_none_stats_not_zero(self):
        rs = rationale_stats([])
        self.assertEqual(rs.count, 0)
        self.assertIsNone(rs.mean_length)


class ReviewFlagInteractionTest(unittest.TestCase):
    def test_flagged_candidate_tracked(self):
        events = [_event(review_flags=("heuristic_source",), rationale="acknowledging heuristic_source here")]
        result = review_flag_interaction(events)
        self.assertEqual(result.events_with_flagged_candidate, 1)
        self.assertEqual(result.events_with_flagged_candidate_referencing_a_flag_in_rationale, 1)

    def test_unflagged_candidate_not_counted(self):
        events = [_event(review_flags=())]
        result = review_flag_interaction(events)
        self.assertEqual(result.events_with_flagged_candidate, 0)


class OptionalFieldUsageTest(unittest.TestCase):
    def test_counts_optional_field_usage(self):
        events = [
            _event(department_override="Platform", reviewer_confidence=0.9, additional_notes="note"),
            _event(),
        ]
        usage = optional_field_usage(events)
        self.assertEqual(usage.department_override_used, 1)
        self.assertEqual(usage.reviewer_confidence_used, 1)
        self.assertEqual(usage.additional_notes_used, 1)
        self.assertEqual(usage.total, 2)


class RealCorpusObservationTest(unittest.TestCase):
    def test_real_pilot_event_is_observed_correctly(self):
        records = load_trace_records()
        events = extract_human_review_events(records)
        self.assertGreaterEqual(len(events), 1)
        dist = decision_distribution(events)
        self.assertGreaterEqual(dist.approve, 1)

    def test_module_does_not_mutate_input(self):
        records = load_trace_records()
        records_copy = [dict(r) for r in records]
        events = extract_human_review_events(records)
        decision_distribution(events)
        rationale_stats(events)
        review_flag_interaction(events)
        optional_field_usage(events)
        self.assertEqual(records, records_copy)


if __name__ == "__main__":
    unittest.main()
