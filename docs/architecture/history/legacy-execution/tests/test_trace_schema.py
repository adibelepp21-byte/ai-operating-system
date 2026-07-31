"""
Dedicated unit tests for execution/trace_schema.py.

Foundation Test Coverage Hardening phase. Exercises normalize_record()
against all three real, on-disk `outputs` generations the module's own
docstring documents, plus boundary/invalid input -- not implementation
internals.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import trace_schema


class NormalizeRecordEventOnlyTest(unittest.TestCase):
    """Generation 3: spawn/terminate/escalation -- nothing to normalize."""

    def test_event_only_outputs_untouched(self):
        raw = {"trace_id": "t1", "outputs": {"event": "spawned"}}
        result = trace_schema.normalize_record(raw)
        self.assertEqual(result["outputs"], {"event": "spawned"})

    def test_none_outputs_untouched(self):
        raw = {"trace_id": "t1", "outputs": None}
        result = trace_schema.normalize_record(raw)
        self.assertIsNone(result["outputs"])

    def test_missing_outputs_key_untouched(self):
        raw = {"trace_id": "t1"}
        result = trace_schema.normalize_record(raw)
        self.assertIsNone(result.get("outputs"))


class NormalizeRecordCurrentGenerationTest(unittest.TestCase):
    """Generation 2 (schema_version 1.1): already current shape."""

    def test_current_shape_evidence_passed_through_unchanged(self):
        evidence = [{"source": "tool", "kind": "cross_reference_check", "resolved": True, "detail": "resolved"}]
        raw = {"trace_id": "t1", "schema_version": "1.1", "outputs": {"evidence": evidence, "failure_class": None, "error": None}}
        result = trace_schema.normalize_record(raw)
        self.assertEqual(result["outputs"]["evidence"], evidence)


class NormalizeRecordLegacyGenerationTest(unittest.TestCase):
    """Generation 1: unversioned, pre-tool-execution-contract shape."""

    def test_flagged_list_becomes_heuristic_legacy_flag_evidence(self):
        raw = {"trace_id": "t1", "outputs": {"flagged": ["some flagged passage"]}}
        result = trace_schema.normalize_record(raw)
        evidence = result["outputs"]["evidence"]
        self.assertEqual(len(evidence), 1)
        self.assertEqual(evidence[0]["source"], "heuristic")
        self.assertEqual(evidence[0]["kind"], "legacy_flag")
        self.assertIsNone(evidence[0]["resolved"])
        self.assertEqual(evidence[0]["detail"], "some flagged passage")

    def test_tool_executions_becomes_tool_evidence(self):
        raw = {
            "trace_id": "t1",
            "outputs": {"tool_executions": [{
                "evidence": {"resolves": True, "match_type": "heading"},
                "parameters": {"citing_document": "a.md", "cited_document": "b.md", "cited_section": "§9"},
            }]},
        }
        result = trace_schema.normalize_record(raw)
        evidence = result["outputs"]["evidence"]
        self.assertEqual(len(evidence), 1)
        e = evidence[0]
        self.assertEqual(e["source"], "tool")
        self.assertEqual(e["kind"], "cross_reference_check")
        self.assertEqual(e["tool_key"], "tool.cross-reference-link-validator-interface")
        self.assertTrue(e["resolved"])
        self.assertEqual(e["detail"], "resolved")
        # legacy parameter names mapped onto current names
        self.assertEqual(e["parameters"]["reference_target"], "b.md")
        self.assertEqual(e["parameters"]["expected_reference"], "§9")
        self.assertIsNone(e["parameters"]["repository_path"])

    def test_tool_executions_unresolved_carries_failure_reason(self):
        raw = {
            "trace_id": "t1",
            "outputs": {"tool_executions": [{
                "evidence": {"resolves": False, "detail": "not found"},
                "parameters": {},
            }]},
        }
        result = trace_schema.normalize_record(raw)
        e = result["outputs"]["evidence"][0]
        self.assertFalse(e["resolved"])
        self.assertEqual(e["detail"], "not found")

    def test_tool_executions_error_takes_priority_over_evidence_detail(self):
        raw = {
            "trace_id": "t1",
            "outputs": {"tool_executions": [{
                "error": "boom",
                "evidence": {"resolves": False, "detail": "not found"},
                "parameters": {},
            }]},
        }
        result = trace_schema.normalize_record(raw)
        self.assertEqual(result["outputs"]["evidence"][0]["detail"], "boom")

    def test_current_style_parameters_left_unmodified(self):
        raw = {
            "trace_id": "t1",
            "outputs": {"tool_executions": [{
                "evidence": {"resolves": True},
                "parameters": {"reference_target": "b.md", "expected_reference": "§9", "repository_path": "/r"},
            }]},
        }
        result = trace_schema.normalize_record(raw)
        params = result["outputs"]["evidence"][0]["parameters"]
        self.assertEqual(params["repository_path"], "/r")


class NormalizeRecordTopLevelDefaultsTest(unittest.TestCase):
    def test_missing_top_level_fields_get_defaults(self):
        raw = {"trace_id": "t1"}
        result = trace_schema.normalize_record(raw)
        self.assertEqual(result["schema_version"], "1.0")
        self.assertIsNone(result["workflow"])
        self.assertIsNone(result["inputs"])
        self.assertIsNone(result["duration_ms"])
        self.assertEqual(result["agent_definition_name"], "unknown")

    def test_present_top_level_fields_preserved(self):
        raw = {"trace_id": "t1", "schema_version": "1.1", "agent_definition_name": "Real Agent"}
        result = trace_schema.normalize_record(raw)
        self.assertEqual(result["schema_version"], "1.1")
        self.assertEqual(result["agent_definition_name"], "Real Agent")

    def test_never_mutates_input_dict(self):
        raw = {"trace_id": "t1", "outputs": {"flagged": ["x"]}}
        raw_copy = {"trace_id": "t1", "outputs": {"flagged": ["x"]}}
        trace_schema.normalize_record(raw)
        self.assertEqual(raw, raw_copy)


class IsCurrentTest(unittest.TestCase):
    def test_current_version_is_current(self):
        self.assertTrue(trace_schema.is_current({"schema_version": "1.1"}))

    def test_missing_version_is_not_current(self):
        self.assertFalse(trace_schema.is_current({}))

    def test_older_version_is_not_current(self):
        self.assertFalse(trace_schema.is_current({"schema_version": "1.0"}))


class RealCorpusNormalizationTest(unittest.TestCase):
    """Confirms normalize_record() does not crash or produce a malformed
    shape against the real, on-disk corpus -- every generation actually
    present, not just the three documented ones."""

    def test_every_real_record_normalizes_without_error(self):
        from execution.memory.extractor import load_trace_records
        records = load_trace_records()  # already passes through normalize_record()
        self.assertGreater(len(records), 0)
        for r in records:
            outputs = r.get("outputs")
            if outputs and ("evidence" in outputs or "event" in outputs):
                continue
            self.fail(f"record {r.get('trace_id')} has neither evidence nor event outputs after normalization")


if __name__ == "__main__":
    unittest.main()
