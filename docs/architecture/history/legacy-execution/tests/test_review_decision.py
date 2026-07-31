"""
Regression tests for execution/review_decision.py — Human Review
Decision Recording (Execution Event boundary only).

Uses only the standard library (unittest), consistent with
execution/tests/test_metrics.py and execution/tests/test_promotion.py.
Exercises real Trace writes against a temporary output directory (no
pollution of the real execution/traces/ corpus), boundary/negative tests
proving this module cannot compute a decision, and validation tests
proving it fails closed on ambiguity.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import ast
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import review_decision as rd
from execution.promotion import CandidatePackage, EvidenceSummary, Provenance


def _snapshot(content="a real reviewed candidate with enough content length", review_flags=()):
    return CandidatePackage(
        id="memory-test-1",
        content=content,
        observation_kind="cross_reference_check",
        provenance=Provenance(
            memory_id="memory-test-1", trace_ids=("trace-a", "trace-b"),
            agent_definition_name="Test Agent", department_status="unavailable",
        ),
        evidence=EvidenceSummary(
            source_type="tool", confidence=1.0, occurrence_count=5,
            observation_frequency=1.0, first_observed_at=1.0, last_observed_at=2.0,
            resolved=True, fingerprint=("reference_target=abc123",),
        ),
        review_flags=review_flags,
    )


def _valid_input(**overrides):
    defaults = dict(
        candidate_snapshot=_snapshot(),
        decision="approve",
        reviewer_identity="reviewer.architect-manual-review",
        rationale="Strong, tool-derived, high-confidence finding.",
        timestamp=1000.0,
    )
    defaults.update(overrides)
    return rd.HumanReviewDecisionInput(**defaults)


class ValidationTest(unittest.TestCase):
    def test_valid_input_has_no_errors(self):
        self.assertEqual(rd.validate_decision_input(_valid_input()), [])

    def test_missing_reviewer_rejected(self):
        errors = rd.validate_decision_input(_valid_input(reviewer_identity=None))
        self.assertTrue(any("reviewer_identity" in e for e in errors))

    def test_missing_snapshot_rejected(self):
        errors = rd.validate_decision_input(_valid_input(candidate_snapshot=None))
        self.assertTrue(any("candidate_snapshot" in e for e in errors))

    def test_missing_snapshot_content_rejected(self):
        bad_snapshot = _snapshot(content="")
        errors = rd.validate_decision_input(_valid_input(candidate_snapshot=bad_snapshot))
        self.assertTrue(any("content" in e for e in errors))

    def test_invalid_decision_value_rejected(self):
        errors = rd.validate_decision_input(_valid_input(decision="auto_approve"))
        self.assertTrue(any("decision must be one of" in e for e in errors))

    def test_missing_rationale_rejected(self):
        errors = rd.validate_decision_input(_valid_input(rationale=None))
        self.assertTrue(any("rationale" in e for e in errors))

    def test_missing_timestamp_rejected(self):
        errors = rd.validate_decision_input(_valid_input(timestamp=None))
        self.assertTrue(any("timestamp" in e for e in errors))

    def test_edit_without_edited_content_rejected(self):
        errors = rd.validate_decision_input(_valid_input(decision="edit", edited_content=None))
        self.assertTrue(any("edited_content is required" in e for e in errors))

    def test_edited_content_without_edit_decision_rejected(self):
        errors = rd.validate_decision_input(_valid_input(decision="approve", edited_content="rewritten text"))
        self.assertTrue(any("must not be provided" in e for e in errors))

    def test_edit_with_edited_content_is_valid(self):
        errors = rd.validate_decision_input(_valid_input(decision="edit", edited_content="rewritten claim text"))
        self.assertEqual(errors, [])

    def test_department_override_without_reason_rejected(self):
        errors = rd.validate_decision_input(_valid_input(department_override="Platform", department_override_reason=None))
        self.assertTrue(any("department_override" in e for e in errors))

    def test_department_override_with_reason_is_valid(self):
        errors = rd.validate_decision_input(
            _valid_input(department_override="Platform", department_override_reason="Reviewer's own domain judgment")
        )
        self.assertEqual(errors, [])

    def test_multiple_errors_all_reported(self):
        errors = rd.validate_decision_input(
            rd.HumanReviewDecisionInput(
                candidate_snapshot=None, decision="bogus", reviewer_identity=None,
                rationale=None, timestamp=None,
            )
        )
        self.assertGreaterEqual(len(errors), 5)


class RecordDecisionTest(unittest.TestCase):
    def setUp(self):
        self._tmp_patchers = []

    def tearDown(self):
        for p in self._tmp_patchers:
            p.stop()

    def _patch_trace_dir(self, tmp_path):
        p = mock.patch("execution.trace.TRACE_DIR", tmp_path)
        p.start()
        self._tmp_patchers.append(p)

    def test_invalid_input_raises_and_writes_nothing(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            self._patch_trace_dir(Path(tmp))
            before = list(Path(tmp).glob("*.jsonl"))
            with self.assertRaises(rd.ValidationError):
                rd.record_decision(_valid_input(reviewer_identity=None))
            after = list(Path(tmp).glob("*.jsonl"))
            self.assertEqual(before, after)

    def test_valid_input_writes_exactly_three_trace_records(self):
        import tempfile, json
        with tempfile.TemporaryDirectory() as tmp:
            self._patch_trace_dir(Path(tmp))
            result = rd.record_decision(_valid_input())
            trace_file = Path(result["trace_file"])
            lines = [l for l in trace_file.read_text(encoding="utf-8").splitlines() if l.strip()]
            self.assertEqual(len(lines), 3)
            events = [json.loads(l) for l in lines]
            self.assertEqual(events[0]["outputs"]["event"], "spawned")
            self.assertEqual(events[1]["outputs"]["event"], "human_review_decision_recorded")
            self.assertEqual(events[2]["outputs"]["event"], "terminated")

    def test_candidate_snapshot_preserved_in_trace(self):
        import tempfile, json
        with tempfile.TemporaryDirectory() as tmp:
            self._patch_trace_dir(Path(tmp))
            snapshot = _snapshot(content="a specific reviewed claim worth preserving exactly")
            result = rd.record_decision(_valid_input(candidate_snapshot=snapshot))
            trace_file = Path(result["trace_file"])
            lines = [json.loads(l) for l in trace_file.read_text(encoding="utf-8").splitlines() if l.strip()]
            decision_record = lines[1]
            stored_snapshot = decision_record["outputs"]["candidate_snapshot"]
            self.assertEqual(stored_snapshot["content"], "a specific reviewed claim worth preserving exactly")
            self.assertEqual(stored_snapshot["evidence"]["confidence"], 1.0)
            self.assertEqual(stored_snapshot["evidence"]["occurrence_count"], 5)

    def test_review_flags_preserved_in_trace(self):
        import tempfile, json
        with tempfile.TemporaryDirectory() as tmp:
            self._patch_trace_dir(Path(tmp))
            snapshot = _snapshot(review_flags=("heuristic_source", "truncated"))
            result = rd.record_decision(_valid_input(candidate_snapshot=snapshot))
            trace_file = Path(result["trace_file"])
            lines = [json.loads(l) for l in trace_file.read_text(encoding="utf-8").splitlines() if l.strip()]
            stored_flags = lines[1]["outputs"]["candidate_snapshot"]["review_flags"]
            self.assertEqual(list(stored_flags), ["heuristic_source", "truncated"])

    def test_provenance_chain_preserved_in_trace(self):
        import tempfile, json
        with tempfile.TemporaryDirectory() as tmp:
            self._patch_trace_dir(Path(tmp))
            result = rd.record_decision(_valid_input())
            trace_file = Path(result["trace_file"])
            lines = [json.loads(l) for l in trace_file.read_text(encoding="utf-8").splitlines() if l.strip()]
            stored_provenance = lines[1]["outputs"]["candidate_snapshot"]["provenance"]
            self.assertEqual(stored_provenance["memory_id"], "memory-test-1")
            self.assertEqual(list(stored_provenance["trace_ids"]), ["trace-a", "trace-b"])
            self.assertEqual(stored_provenance["department_status"], "unavailable")

    def test_department_never_guessed_stays_unavailable(self):
        import tempfile, json
        with tempfile.TemporaryDirectory() as tmp:
            self._patch_trace_dir(Path(tmp))
            result = rd.record_decision(_valid_input())
            trace_file = Path(result["trace_file"])
            lines = [json.loads(l) for l in trace_file.read_text(encoding="utf-8").splitlines() if l.strip()]
            self.assertEqual(
                lines[1]["outputs"]["candidate_snapshot"]["provenance"]["department_status"], "unavailable"
            )

    def test_reject_decision_records_no_edited_content(self):
        import tempfile, json
        with tempfile.TemporaryDirectory() as tmp:
            self._patch_trace_dir(Path(tmp))
            result = rd.record_decision(_valid_input(decision="reject"))
            trace_file = Path(result["trace_file"])
            lines = [json.loads(l) for l in trace_file.read_text(encoding="utf-8").splitlines() if l.strip()]
            self.assertEqual(lines[1]["outputs"]["decision"], "reject")
            self.assertIsNone(lines[1]["outputs"]["edited_content"])

    def test_input_snapshot_not_mutated(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            self._patch_trace_dir(Path(tmp))
            snapshot = _snapshot()
            snapshot_copy = _snapshot()
            decision_input = _valid_input(candidate_snapshot=snapshot)
            rd.record_decision(decision_input)
            self.assertEqual(snapshot, snapshot_copy)  # frozen dataclass equality, unmutated


class NegativeBoundaryTest(unittest.TestCase):
    """Structural guarantees that this module cannot compute a decision,
    rank candidates, or select candidates -- verified by static
    inspection of the module's own source, the same technique
    execution/tests/test_metrics.py's LayeringTest already uses, not
    merely asserted in prose."""

    _FORBIDDEN_ATTRS = {"confidence", "occurrence_count", "observation_frequency", "review_flags", "source_type"}

    def test_no_comparison_against_evidence_quality_fields(self):
        """No Compare node anywhere in review_decision.py may apply a
        magnitude/equality operator (>, <, >=, <=, ==, !=) to an
        evidence-quality field -- that would be exactly the
        "if confidence > X: approve" pattern this phase's Hard
        Constraints forbid. `is None` / `is not None` presence checks
        (used by validate_decision_input to confirm a field wasn't
        omitted, never to gate on its value) are structurally different
        and explicitly allowed."""
        magnitude_ops = (ast.Gt, ast.Lt, ast.GtE, ast.LtE, ast.Eq, ast.NotEq, ast.In, ast.NotIn)
        source = Path(rd.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=rd.__file__)
        violations = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare):
                operands = [node.left] + list(node.comparators)
                attr_names = [o.attr for o in operands if isinstance(o, ast.Attribute)]
                if not attr_names:
                    continue
                has_magnitude_op = any(isinstance(op, magnitude_ops) for op in node.ops)
                if has_magnitude_op:
                    for attr in attr_names:
                        if attr in self._FORBIDDEN_ATTRS:
                            violations.append(attr)
        self.assertEqual(violations, [], f"found magnitude/equality comparisons against evidence-quality fields: {violations}")

    def test_no_ranking_or_selection_functions_defined(self):
        """This module must not define anything resembling
        promotion.py's select_candidates/ranking responsibility -- that
        stays exclusively in promotion.py."""
        source = Path(rd.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=rd.__file__)
        function_names = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
        forbidden_names = {"select_candidates", "rank_candidates", "rank", "select", "approve", "reject", "decide"}
        self.assertEqual(function_names & forbidden_names, set())

    def test_output_carries_no_computed_verdict(self):
        """record_decision()'s return value only ever identifies where
        the decision was written (trace_id, trace_file) -- it never
        echoes back anything resembling a computed approve/reject
        verdict distinct from what the caller already provided."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("execution.trace.TRACE_DIR", Path(tmp)):
                result = rd.record_decision(_valid_input())
        self.assertEqual(set(result.keys()), {"trace_id", "trace_file"})

    def test_cannot_modify_promotion_candidate_output(self):
        """record_decision() must not mutate the CandidatePackage it
        receives -- frozen dataclasses already make an in-place mutation
        a hard Python error, so this proves no such attempt exists by
        confirming a normal call completes without one."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("execution.trace.TRACE_DIR", Path(tmp)):
                snapshot = _snapshot()
                original_repr = repr(snapshot)
                rd.record_decision(_valid_input(candidate_snapshot=snapshot))
                self.assertEqual(repr(snapshot), original_repr)


if __name__ == "__main__":
    unittest.main()
