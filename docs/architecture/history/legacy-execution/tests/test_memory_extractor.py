"""
Dedicated unit tests for execution/memory/extractor.py.

Foundation Test Coverage Hardening phase. Other test files (test_promotion.py,
test_evidence_chain.py, test_memory_governance.py) exercise extract_memories()
incidentally as a fixture-building step; this file tests extractor.py's own
functions directly and in isolation: dedup, aggregation, expiry, relevance,
and MemoryStore's real file I/O.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import execution.memory.extractor as extractor_mod
from execution.memory.extractor import (
    MemoryStore, evaluate_relevance, extract_memories, is_expired,
)


def _record(trace_id, kind, detail, agent_instance_id="instance-a", timestamp=None):
    return {
        "trace_id": trace_id, "agent_instance_id": agent_instance_id,
        "outputs": {"evidence": [{"source": "tool", "kind": kind, "detail": detail, "resolved": True}]},
        "timestamp": timestamp if timestamp is not None else time.time(),
    }


class ExtractMemoriesTest(unittest.TestCase):
    def test_empty_input_returns_empty(self):
        self.assertEqual(extract_memories([]), [])

    def test_records_with_no_evidence_are_ignored(self):
        records = [{"trace_id": "t1", "outputs": {"event": "spawned"}}]
        self.assertEqual(extract_memories(records), [])

    def test_single_observation_becomes_one_memory(self):
        memories = extract_memories([_record("t1", "cross_reference_check", "§9 not found")])
        self.assertEqual(len(memories), 1)
        self.assertEqual(memories[0].content, "§9 not found")
        self.assertEqual(memories[0].occurrence_count, 1)

    def test_identical_kind_and_content_dedups_across_records(self):
        records = [
            _record("t1", "cross_reference_check", "§9 not found", agent_instance_id="instance-a"),
            _record("t2", "cross_reference_check", "§9 not found", agent_instance_id="instance-b"),
        ]
        memories = extract_memories(records)
        self.assertEqual(len(memories), 1)
        self.assertEqual(memories[0].occurrence_count, 2)
        self.assertEqual(set(memories[0].agent_instance_ids), {"instance-a", "instance-b"})
        self.assertEqual(set(memories[0].source_trace_ids), {"t1", "t2"})

    def test_different_content_produces_separate_memories(self):
        records = [
            _record("t1", "cross_reference_check", "§9 not found"),
            _record("t2", "cross_reference_check", "§10 not found"),
        ]
        memories = extract_memories(records)
        self.assertEqual(len(memories), 2)

    def test_evidence_missing_kind_or_content_is_skipped(self):
        records = [
            {"trace_id": "t1", "outputs": {"evidence": [{"source": "tool", "kind": None, "detail": "x"}]}},
            {"trace_id": "t2", "outputs": {"evidence": [{"source": "tool", "kind": "x", "detail": None}]}},
        ]
        self.assertEqual(extract_memories(records), [])

    def test_confidence_increases_with_occurrence_and_instance_diversity(self):
        one_occurrence = extract_memories([_record("t1", "k", "c")])
        two_occurrences_two_instances = extract_memories([
            _record("t1", "k", "c", agent_instance_id="a"),
            _record("t2", "k", "c", agent_instance_id="b"),
        ])
        self.assertGreater(two_occurrences_two_instances[0].confidence, one_occurrence[0].confidence)

    def test_confidence_never_exceeds_one(self):
        records = [_record(f"t{i}", "k", "c", agent_instance_id=f"i{i}") for i in range(50)]
        memories = extract_memories(records)
        self.assertLessEqual(memories[0].confidence, 1.0)

    def test_first_and_last_observed_come_from_source_record_timestamps(self):
        records = [
            _record("t1", "k", "c", timestamp=1000.0),
            _record("t2", "k", "c", timestamp=2000.0),
        ]
        memories = extract_memories(records)
        self.assertEqual(memories[0].first_observed_at, 1000.0)
        self.assertEqual(memories[0].last_observed_at, 2000.0)

    def test_status_is_always_provisional_never_promoted(self):
        memories = extract_memories([_record("t1", "k", "c")])
        self.assertEqual(memories[0].status, "provisional")

    def test_pure_function_does_not_mutate_input(self):
        records = [_record("t1", "k", "c")]
        records_copy = [dict(r) for r in records]
        extract_memories(records)
        self.assertEqual(records, records_copy)

    def test_default_retention_seconds_applied_when_not_specified(self):
        memories = extract_memories([_record("t1", "k", "c")])
        from execution.memory.extractor import DEFAULT_RETENTION_SECONDS
        self.assertEqual(memories[0].retention_seconds, DEFAULT_RETENTION_SECONDS)

    def test_custom_retention_seconds_honored(self):
        memories = extract_memories([_record("t1", "k", "c")], retention_seconds=42)
        self.assertEqual(memories[0].retention_seconds, 42)


class IsExpiredTest(unittest.TestCase):
    def test_recent_memory_not_expired(self):
        memories = extract_memories([_record("t1", "k", "c", timestamp=time.time())], retention_seconds=3600)
        self.assertFalse(is_expired(memories[0]))

    def test_old_memory_is_expired(self):
        memories = extract_memories([_record("t1", "k", "c", timestamp=time.time() - 10000)], retention_seconds=3600)
        self.assertTrue(is_expired(memories[0]))

    def test_expiry_boundary_is_strictly_greater_than(self):
        old_ts = time.time() - 3600
        memories = extract_memories([_record("t1", "k", "c", timestamp=old_ts)], retention_seconds=3600)
        # exactly at the boundary should not be expired (age == retention, not >)
        self.assertFalse(is_expired(memories[0], now=old_ts + 3600))

    def test_explicit_now_parameter_is_honored(self):
        memories = extract_memories([_record("t1", "k", "c", timestamp=1000.0)], retention_seconds=100)
        self.assertFalse(is_expired(memories[0], now=1050.0))
        self.assertTrue(is_expired(memories[0], now=1200.0))


class EvaluateRelevanceTest(unittest.TestCase):
    def test_fresh_high_confidence_recent_memory(self):
        records = [
            _record("t1", "k", "c", agent_instance_id="a", timestamp=time.time()),
            _record("t2", "k", "c", agent_instance_id="b", timestamp=time.time()),
        ]
        memories = extract_memories(records, retention_seconds=3600)
        self.assertEqual(evaluate_relevance(memories[0]), "fresh")

    def test_low_confidence_single_occurrence(self):
        memories = extract_memories([_record("t1", "k", "c", timestamp=time.time())], retention_seconds=3600)
        self.assertEqual(memories[0].confidence, 0.6)  # exactly at threshold, not below
        self.assertEqual(evaluate_relevance(memories[0]), "fresh")

    def test_stale_beats_low_confidence_in_severity(self):
        memories = extract_memories([_record("t1", "k", "c", timestamp=time.time() - 10000)], retention_seconds=3600)
        self.assertEqual(evaluate_relevance(memories[0]), "stale")


class MemoryStoreTest(unittest.TestCase):
    def test_write_all_creates_a_real_readable_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(extractor_mod, "MEMORY_RECORDS_DIR", Path(tmp)):
                store = MemoryStore(run_id="test-run")
                memories = extract_memories([_record("t1", "k", "c")])
                path = store.write_all(memories)
                self.assertTrue(path.is_file())
                lines = path.read_text(encoding="utf-8").splitlines()
                self.assertEqual(len(lines), 1)

    def test_distinct_stores_get_distinct_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(extractor_mod, "MEMORY_RECORDS_DIR", Path(tmp)):
                s1 = MemoryStore()
                s2 = MemoryStore()
                self.assertNotEqual(s1.path, s2.path)


if __name__ == "__main__":
    unittest.main()
