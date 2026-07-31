"""
Tier 3 Memory Governance Layer — validation experiments.

Five experiments, per the Architect Approval — Tier 3 Memory Governance
Layer directive: creation, validation, degradation, Human Review
interaction, conflict handling. Experiments 1-3 use small, disclosed,
controlled scenarios (synthetic Trace-shaped dicts, following the same
pattern already accepted for the Tier 2 drift experiment); Experiment 4
uses the real corpus's actual recorded Human Review events (no
fabrication); Experiment 5 uses a real, disclosed, controlled Tool-call
scenario against real scratch files, the same technique already accepted
for execution/memory/drift_experiment.py, because no real conflicting
memory pair exists in the corpus today (checked directly).

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution.memory.extractor import extract_memories, evaluate_relevance
from execution.memory_governance import (
    detect_conflicts, preferred_content, review_state, trust_decision,
)


def _trace(trace_id, kind, content, resolved=True, tool_key=None, parameters=None,
           agent_instance_id="instance-test", timestamp=None):
    evidence = {"source": "tool" if tool_key else "heuristic", "kind": kind,
                "detail": content, "resolved": resolved}
    if tool_key:
        evidence["tool_key"] = tool_key
        evidence["parameters"] = parameters or {}
    return {
        "trace_id": trace_id, "agent_instance_id": agent_instance_id,
        "outputs": {"evidence": [evidence]}, "timestamp": timestamp or time.time(),
    }


def _human_review_trace(trace_id, decision, observation_kind, content, evidence_dict,
                         review_flags=(), edited_content=None, decision_timestamp=None):
    return {
        "trace_id": trace_id,
        "outputs": {
            "event": "human_review_decision_recorded",
            "decision": decision,
            "reviewer_identity": "test-reviewer",
            "rationale": "test rationale",
            "decision_timestamp": decision_timestamp or time.time(),
            "edited_content": edited_content,
            "candidate_snapshot": {
                "observation_kind": observation_kind,
                "content": content,
                "evidence": evidence_dict,
                "review_flags": list(review_flags),
            },
        },
    }


class MemoryCreationTest(unittest.TestCase):
    """Experiment 1: Observation -> Memory creation preserves provenance."""

    def test_provenance_preserved_from_trace_to_memory(self):
        records = [_trace("trace-a", "cross_reference_check", "§9 not found", resolved=False,
                           agent_instance_id="instance-a"),
                   _trace("trace-b", "cross_reference_check", "§9 not found", resolved=False,
                           agent_instance_id="instance-b")]
        memories = extract_memories(records)
        self.assertEqual(len(memories), 1)
        m = memories[0]
        self.assertEqual(set(m.source_trace_ids), {"trace-a", "trace-b"})
        self.assertEqual(set(m.agent_instance_ids), {"instance-a", "instance-b"})
        self.assertEqual(m.occurrence_count, 2)


class MemoryValidationTest(unittest.TestCase):
    """Experiment 2: Memory with valid evidence remains usable."""

    def test_fresh_unreviewed_memory_is_usable(self):
        records = [_trace("trace-a", "cross_reference_check", "§9 not found", resolved=False)]
        memories = extract_memories(records, retention_seconds=3600)
        m = memories[0]
        self.assertEqual(evaluate_relevance(m), "fresh")
        self.assertEqual(trust_decision(m, records), "fresh")
        self.assertEqual(review_state(m, records).state, "unreviewed")


class MemoryDegradationTest(unittest.TestCase):
    """Experiment 3: Changed evidence (time) reduces trust."""

    def test_expired_memory_loses_trust(self):
        old_ts = time.time() - 10000
        records = [_trace("trace-a", "cross_reference_check", "§9 not found", resolved=False,
                           timestamp=old_ts)]
        memories = extract_memories(records, retention_seconds=3600)
        m = memories[0]
        self.assertEqual(trust_decision(m, records), "stale")

    def test_low_confidence_single_occurrence_is_degraded_not_stale(self):
        records = [_trace("trace-a", "cross_reference_check", "§9 not found", resolved=False)]
        memories = extract_memories(records, retention_seconds=3600)
        m = memories[0]
        self.assertEqual(m.confidence, 0.6)  # single occurrence, single instance: base heuristic floor
        self.assertEqual(trust_decision(m, records), "fresh")  # 0.6 is the fresh/low_confidence boundary, not below it

    def test_approved_memory_does_not_bypass_aging(self):
        """Tier 3.5 Phase 2: a real human approve must not exempt a
        memory from later-detected staleness. Controlled, in-memory
        only -- no Trace write."""
        from execution.memory.extractor import MemoryRecord

        old_ts = time.time() - 10000
        memory = MemoryRecord(
            memory_id="memory-controlled-approved-aged", agent_instance_ids=("instance-controlled",),
            source_trace_ids=("trace-controlled",), observation_kind="cross_reference_check",
            content="§9 not found (controlled scenario)", occurrence_count=1, observation_frequency=1.0,
            confidence=1.0, first_observed_at=old_ts, last_observed_at=old_ts, created_at=old_ts,
            retention_seconds=3600, status="provisional",
        )
        review_trace = _human_review_trace(
            "trace-controlled-review", "approve", memory.observation_kind, memory.content,
            evidence_dict={"source_type": "tool", "confidence": 1.0},
        )
        self.assertEqual(review_state(memory, [review_trace]).state, "approved")
        self.assertEqual(trust_decision(memory, [review_trace]), "stale")


class HumanReviewInteractionTest(unittest.TestCase):
    """Experiment 4: approve/reject/edit decisions affect governance correctly."""

    def test_reject_overrides_relevance_to_do_not_use(self):
        content = "§9 not found"
        records = [
            _trace("trace-a", "cross_reference_check", content, resolved=False),
            _human_review_trace("trace-review", "reject", "cross_reference_check", content,
                                 evidence_dict={"source_type": "tool", "confidence": 1.0}),
        ]
        memories = extract_memories([records[0]], retention_seconds=3600)
        m = memories[0]
        self.assertEqual(review_state(m, records).state, "rejected")
        self.assertEqual(trust_decision(m, records), "do_not_use")

    def test_approve_preserves_relevance_based_trust(self):
        content = "§9 not found"
        records = [
            _trace("trace-a", "cross_reference_check", content, resolved=False),
            _human_review_trace("trace-review", "approve", "cross_reference_check", content,
                                 evidence_dict={"source_type": "tool", "confidence": 1.0}),
        ]
        memories = extract_memories([records[0]], retention_seconds=3600)
        m = memories[0]
        self.assertEqual(review_state(m, records).state, "approved")
        self.assertEqual(trust_decision(m, records), "fresh")

    def test_edit_preserves_original_and_exposes_edited_content_separately(self):
        content = "§9 not found"
        edited = "§9 not found in cited.md as of this review"
        records = [
            _trace("trace-a", "cross_reference_check", content, resolved=False),
            _human_review_trace("trace-review", "edit", "cross_reference_check", content,
                                 evidence_dict={"source_type": "tool", "confidence": 1.0},
                                 edited_content=edited),
        ]
        memories = extract_memories([records[0]], retention_seconds=3600)
        m = memories[0]
        self.assertEqual(review_state(m, records).state, "edited")
        self.assertEqual(m.content, content)  # original untouched
        self.assertEqual(preferred_content(m, records), edited)  # caller-facing preference only

    def test_reject_wins_even_if_an_approve_also_exists_for_same_content(self):
        content = "§9 not found"
        records = [
            _trace("trace-a", "cross_reference_check", content, resolved=False),
            _human_review_trace("trace-review-1", "approve", "cross_reference_check", content,
                                 evidence_dict={}, decision_timestamp=1.0),
            _human_review_trace("trace-review-2", "reject", "cross_reference_check", content,
                                 evidence_dict={}, decision_timestamp=2.0),
        ]
        memories = extract_memories([records[0]], retention_seconds=3600)
        m = memories[0]
        self.assertEqual(review_state(m, records).state, "rejected")

    def test_real_corpus_reject_event_is_correctly_governed(self):
        """Grounds against the actual first real reject event this
        session produced (trace-19f71086dd74)."""
        from execution.memory.extractor import load_trace_records
        records = load_trace_records()
        memories = extract_memories(records)
        target = next((m for m in memories if m.observation_kind == "document_structure_parse_failure"
                        and m.content == "§11 cited internally but no heading numbered 11 exists in this document"), None)
        self.assertIsNotNone(target, "the real memory reviewed in Event #5 should still be extractable")
        rs = review_state(target, records)
        self.assertEqual(rs.state, "rejected")
        self.assertEqual(trust_decision(target, records), "do_not_use")

    def test_real_corpus_edit_event_is_correctly_governed(self):
        """Grounds against the actual first real edit event this session
        produced (trace-502ab65e9b0f)."""
        from execution.memory.extractor import load_trace_records
        records = load_trace_records()
        memories = extract_memories(records)
        target = next((m for m in memories if m.observation_kind == "staleness_flag"
                        and m.content.startswith("[severity=2] This gap is not a deliberate")), None)
        self.assertIsNotNone(target, "the real memory reviewed in Event #6 should still be extractable")
        rs = review_state(target, records)
        self.assertEqual(rs.state, "edited")
        self.assertTrue(rs.edited_content.endswith("as an intentional deferral."))
        self.assertEqual(preferred_content(target, records), rs.edited_content)
        self.assertNotEqual(target.content, rs.edited_content)  # original snapshot never overwritten


class ConflictHandlingTest(unittest.TestCase):
    """Experiment 5: conflicting Memory records are detected, not silently overwritten."""

    def test_real_controlled_conflict_is_detected(self):
        """Uses the exact same real Tool + real scratch-file technique
        already accepted for execution/memory/drift_experiment.py: two
        real, live Tool calls against the same reference at two
        genuinely different real states, both retained as separate real
        Trace-shaped records (append-only, neither overwrites the
        other) -- not fabricated resolved values."""
        from execution.memory import drift_experiment as drift
        from execution.tool import ToolRequest, _registry

        citing, cited = drift.setup_scratch()
        execution_a = drift.call_tool(citing, cited)
        ev_a = execution_a.evidence or {}

        drift.introduce_controlled_change(cited)
        execution_b = drift.call_tool(citing, cited)
        ev_b = execution_b.evidence or {}

        self.assertNotEqual(ev_a.get("resolved"), ev_b.get("resolved"),
                             "controlled change must genuinely flip the real result to exercise this experiment")

        content_a = ev_a.get("failure_reason") or "resolved"
        content_b = ev_b.get("failure_reason") or "resolved"
        tool_key = "tool.cross-reference-link-validator-interface"
        params = {
            "citing_document": str(citing), "repository_path": str(drift.REPO_ROOT),
            "reference_target": str(cited), "expected_reference": "§9",
        }
        records = [
            _trace("trace-conflict-a", "cross_reference_check", content_a, resolved=ev_a.get("resolved"),
                   tool_key=tool_key, parameters=params),
            _trace("trace-conflict-b", "cross_reference_check", content_b, resolved=ev_b.get("resolved"),
                   tool_key=tool_key, parameters=params),
        ]
        memories = extract_memories(records, retention_seconds=3600)
        self.assertEqual(len(memories), 2)  # both distinct observations retained, neither overwrote the other

        conflicts = detect_conflicts(memories, records)
        self.assertEqual(len(conflicts), 1)
        conflict = conflicts[0]
        self.assertNotEqual(conflict.resolved_a, conflict.resolved_b)
        self.assertEqual({conflict.memory_a.content, conflict.memory_b.content}, {content_a, content_b})

    def test_no_conflict_when_all_agree(self):
        records = [_trace("trace-a", "cross_reference_check", "§9 not found", resolved=False,
                           tool_key="tool.x", parameters={"reference_target": "/f.md", "expected_reference": "§9"}),
                   _trace("trace-b", "cross_reference_check", "§9 not found (again)", resolved=False,
                           tool_key="tool.x", parameters={"reference_target": "/f.md", "expected_reference": "§9"})]
        # tool.x is unregistered -- both should be skipped (None key), not falsely conflict
        memories = extract_memories(records, retention_seconds=3600)
        conflicts = detect_conflicts(memories, records)
        self.assertEqual(conflicts, ())

    def test_heuristic_sourced_memories_never_produce_conflicts(self):
        """Heuristic evidence has no tool_key/cache_key_fn -- must be
        skipped, not crash or falsely flag."""
        records = [_trace("trace-a", "staleness_flag", "gap A", resolved=None),
                   _trace("trace-b", "staleness_flag", "gap B", resolved=None)]
        memories = extract_memories(records, retention_seconds=3600)
        conflicts = detect_conflicts(memories, records)
        self.assertEqual(conflicts, ())


class RegressionSafetyTest(unittest.TestCase):
    """Structural guarantee: this layer never mutates its inputs."""

    def test_no_mutation_of_memories_or_trace_records(self):
        from execution.memory.extractor import load_trace_records
        records = load_trace_records()
        records_copy = [dict(r) for r in records]
        memories = extract_memories(records)
        memories_copy = list(memories)

        for m in memories[:20]:
            review_state(m, records)
            trust_decision(m, records)
            preferred_content(m, records)
        detect_conflicts(memories, records)

        self.assertEqual(records, records_copy)
        self.assertEqual(memories, memories_copy)


if __name__ == "__main__":
    unittest.main()
