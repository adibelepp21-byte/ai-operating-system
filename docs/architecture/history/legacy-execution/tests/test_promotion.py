"""
Regression tests for execution/promotion.py — Promotion Candidate
Selection.

Uses only the standard library (unittest), consistent with
tools/tests/test_validators.py and execution/tests/test_metrics.py.
Synthetic fixtures exercise eligibility, source-type reconstruction, and
review-flag logic in isolation; RealCorpusRegressionTest exercises the
exact acceptance criteria from the Promotion Candidate Selection
Validation Report v1.0 against the real, on-disk corpus.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution.memory.extractor import MemoryRecord
from execution.promotion import is_degenerate_content, select_candidates


def _memory(
    memory_id="mem-1", content="a real observation with enough length to pass",
    observation_kind="cross_reference_check", confidence=1.0, occurrence_count=1,
    observation_frequency=1.0, agent_instance_ids=("instance-1",),
    source_trace_ids=("trace-1",), first_observed_at=1.0, last_observed_at=1.0,
):
    return MemoryRecord(
        memory_id=memory_id, agent_instance_ids=agent_instance_ids,
        source_trace_ids=source_trace_ids, observation_kind=observation_kind,
        content=content, occurrence_count=occurrence_count,
        observation_frequency=observation_frequency, confidence=confidence,
        first_observed_at=first_observed_at, last_observed_at=last_observed_at,
        created_at=100.0, retention_seconds=3600, status="provisional",
    )


def _trace_record(trace_id, kind, detail, source, agent_definition_name="Test Agent"):
    return {
        "trace_id": trace_id,
        "agent_definition_name": agent_definition_name,
        "outputs": {"evidence": [{"kind": kind, "detail": detail, "source": source}]},
    }


class DegenerateContentTest(unittest.TestCase):
    def test_heading_fragment_excluded(self):
        self.assertTrue(is_degenerate_content("## Domain Model Impact"))

    def test_generic_fallback_excluded(self):
        self.assertTrue(is_degenerate_content("resolved"))

    def test_short_content_excluded(self):
        self.assertTrue(is_degenerate_content("short"))

    def test_real_content_not_excluded(self):
        self.assertFalse(is_degenerate_content("§6 not found anywhere in governance-artifact-integrity.md"))

    def test_verbatim_quote_not_excluded(self):
        # low confidence, heuristic, verbatim -- none of these are eligibility exclusions
        self.assertFalse(is_degenerate_content("This ADR does not resolve whether direct authorization is permanent."))


class SelectCandidatesTest(unittest.TestCase):
    def test_degenerate_content_filtered_out(self):
        memories = [_memory(content="## Domain Model Impact"), _memory(memory_id="mem-2", content="resolved")]
        candidates = select_candidates(memories, [])
        self.assertEqual(len(candidates), 0)

    def test_source_type_reconstructed_from_trace(self):
        memories = [_memory(observation_kind="cross_reference_check", content="§6 not found anywhere in doc.md")]
        traces = [_trace_record("trace-1", "cross_reference_check", "§6 not found anywhere in doc.md", "tool")]
        candidates = select_candidates(memories, traces)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].evidence.source_type, "tool")

    def test_unresolvable_source_is_unknown_not_guessed(self):
        memories = [_memory(content="a real observation with no matching trace evidence")]
        candidates = select_candidates(memories, [])  # no trace records at all
        self.assertEqual(candidates[0].evidence.source_type, "unknown")

    def test_ambiguous_source_is_unknown_not_guessed(self):
        memories = [_memory(content="conflicting evidence sources for one memory", source_trace_ids=("trace-1", "trace-2"))]
        traces = [
            _trace_record("trace-1", "cross_reference_check", "conflicting evidence sources for one memory", "tool"),
            _trace_record("trace-2", "cross_reference_check", "conflicting evidence sources for one memory", "heuristic"),
        ]
        candidates = select_candidates(memories, traces)
        self.assertEqual(candidates[0].evidence.source_type, "unknown")

    def test_department_status_always_unavailable(self):
        memories = [_memory()]
        candidates = select_candidates(memories, [])
        self.assertEqual(candidates[0].provenance.department_status, "unavailable")

    def test_ambiguous_agent_definition_name_is_none_not_guessed(self):
        memories = [_memory(content="same fact from two different agent definitions", source_trace_ids=("trace-1", "trace-2"))]
        traces = [
            _trace_record("trace-1", "cross_reference_check", "same fact from two different agent definitions", "tool", agent_definition_name="Agent A"),
            _trace_record("trace-2", "cross_reference_check", "same fact from two different agent definitions", "tool", agent_definition_name="Agent B"),
        ]
        candidates = select_candidates(memories, traces)
        self.assertIsNone(candidates[0].provenance.agent_definition_name)

    def test_review_flags_heuristic_and_low_confidence(self):
        memories = [_memory(content="a low confidence heuristic observation worth flagging", confidence=0.5)]
        traces = [_trace_record("trace-1", "cross_reference_check", "a low confidence heuristic observation worth flagging", "heuristic")]
        candidates = select_candidates(memories, traces)
        self.assertIn("heuristic_source", candidates[0].review_flags)
        self.assertIn("low_confidence", candidates[0].review_flags)

    def test_verbatim_quote_flag_from_observation_kind(self):
        memories = [_memory(observation_kind="uncited_restatement_flag", content="a verbatim excerpt copied directly from source")]
        candidates = select_candidates(memories, [])
        self.assertIn("verbatim_quote", candidates[0].review_flags)

    def test_truncated_flag_heuristic(self):
        truncated = "[severity=2] " + ("x" * 187)  # lands at 200 chars, no terminal punctuation
        self.assertEqual(len(truncated), 200)
        memories = [_memory(content=truncated)]
        candidates = select_candidates(memories, [])
        self.assertIn("truncated", candidates[0].review_flags)

    def test_no_promotion_decision_fields_exist(self):
        """Structural guarantee: CandidatePackage has no approve/reject/status
        field anywhere -- this module cannot make a promotion decision
        because the output shape has nowhere to record one."""
        memories = [_memory()]
        candidates = select_candidates(memories, [])
        c = candidates[0]
        field_names = set(vars(c).keys()) | set(vars(c.provenance).keys()) | set(vars(c.evidence).keys())
        forbidden = {"approved", "rejected", "decision", "status", "promoted"}
        self.assertEqual(field_names & forbidden, set())

    def test_ranking_prioritizes_tool_over_heuristic(self):
        memories = [
            _memory(memory_id="heur", content="a heuristic sourced observation of real length", confidence=1.0, occurrence_count=1),
            _memory(memory_id="tool", content="a tool sourced observation of real length here", confidence=1.0, occurrence_count=1),
        ]
        traces = [
            _trace_record("trace-1", "cross_reference_check", "a heuristic sourced observation of real length", "heuristic"),
        ]
        # tool memory's source_trace_ids default to ("trace-1",) too in the helper, so give it a distinct id
        memories[1] = _memory(memory_id="tool", content="a tool sourced observation of real length here", source_trace_ids=("trace-2",))
        traces.append(_trace_record("trace-2", "cross_reference_check", "a tool sourced observation of real length here", "tool"))
        candidates = select_candidates(memories, traces)
        self.assertEqual(candidates[0].id, "tool")
        self.assertEqual(candidates[1].id, "heur")

    def test_pure_function_no_mutation(self):
        memories = [_memory()]
        traces = [_trace_record("trace-1", "cross_reference_check", memories[0].content, "tool")]
        memories_copy = list(memories)
        traces_copy = [dict(t) for t in traces]
        select_candidates(memories, traces)
        self.assertEqual(memories, memories_copy)
        self.assertEqual(traces, traces_copy)


class RealCorpusRegressionTest(unittest.TestCase):
    """Exercises the exact acceptance criteria from the Promotion
    Candidate Selection Validation Report v1.0 against the real corpus."""

    @classmethod
    def setUpClass(cls):
        from execution.memory.extractor import extract_memories, load_trace_records
        cls.records = load_trace_records()
        cls.memories = extract_memories(cls.records)
        cls.candidates = select_candidates(cls.memories, cls.records)

    def test_known_artifacts_excluded(self):
        contents = {c.content for c in self.candidates}
        self.assertNotIn("resolved", contents)
        self.assertNotIn("## Domain Model Impact", contents)

    def test_all_candidates_have_provenance(self):
        for c in self.candidates:
            self.assertTrue(c.provenance.trace_ids)
            self.assertTrue(c.provenance.memory_id)
            self.assertEqual(c.provenance.department_status, "unavailable")

    def test_source_type_resolves_for_all_candidates(self):
        unresolved = [c for c in self.candidates if c.evidence.source_type == "unknown"]
        self.assertEqual(unresolved, [])

    def test_no_side_effects_on_repeated_runs(self):
        second = select_candidates(self.memories, self.records)
        self.assertEqual(self.candidates, second)

    def test_calibration_A_and_B_top_ranked_and_eligible(self):
        contents = [c.content for c in self.candidates]
        self.assertIn("§6 not found anywhere in governance-artifact-integrity.md", contents)
        self.assertIn(
            "paragraph mentioning 'Agent Definition' reads more similar to 'Agent Instance' (0.22 vs 0.19)",
            contents,
        )

    def test_calibration_D_staleness_flagged(self):
        staleness = [c for c in self.candidates if c.observation_kind == "staleness_flag"]
        self.assertTrue(staleness)
        for c in staleness:
            self.assertIn("heuristic_source", c.review_flags)

    def test_calibration_E_uncited_restatement_flagged(self):
        uncited = [c for c in self.candidates if c.observation_kind == "uncited_restatement_flag"]
        self.assertTrue(uncited)
        for c in uncited:
            self.assertIn("verbatim_quote", c.review_flags)


if __name__ == "__main__":
    unittest.main()
