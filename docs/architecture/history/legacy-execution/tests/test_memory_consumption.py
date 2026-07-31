"""
Dedicated unit tests for execution/memory/consumption.py.

Foundation Test Coverage Hardening phase. Uses the real Tool registry
and real, self-contained scratch files -- avoids mocking Tool behavior
since the real adapters are cheap, deterministic, and already used this
way by execution/memory/drift_experiment.py.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import tool as tool_mod
from execution.memory.consumption import _derive_key, build_input_keyed_cache

CROSS_REF_TOOL_KEY = "tool.cross-reference-link-validator-interface"


class DeriveKeyTest(unittest.TestCase):
    def test_registered_tool_returns_a_key(self):
        key = _derive_key(CROSS_REF_TOOL_KEY, {"reference_target": "/a.md", "expected_reference": "§9"})
        self.assertEqual(key, (CROSS_REF_TOOL_KEY, "/a.md", "§9"))

    def test_unregistered_tool_returns_none(self):
        self.assertIsNone(_derive_key("tool.does-not-exist", {"x": 1}))

    def test_same_parameters_always_derive_the_same_key(self):
        params = {"reference_target": "/a.md", "expected_reference": "§9"}
        self.assertEqual(_derive_key(CROSS_REF_TOOL_KEY, params), _derive_key(CROSS_REF_TOOL_KEY, params))


class BuildInputKeyedCacheTest(unittest.TestCase):
    def test_empty_records_produce_empty_cache(self):
        self.assertEqual(build_input_keyed_cache([]), {})

    def test_records_with_no_evidence_are_ignored(self):
        records = [{"trace_id": "t1", "outputs": {"event": "spawned"}}]
        self.assertEqual(build_input_keyed_cache(records), {})

    def test_heuristic_sourced_evidence_is_excluded(self):
        records = [{"trace_id": "t1", "outputs": {"evidence": [
            {"source": "heuristic", "kind": "staleness_flag", "detail": "x", "resolved": None},
        ]}}]
        self.assertEqual(build_input_keyed_cache(records), {})

    def test_real_tool_evidence_with_registered_key_fn_populates_cache(self):
        records = [{"trace_id": "t1", "outputs": {"evidence": [{
            "source": "tool", "kind": "cross_reference_check", "tool_key": CROSS_REF_TOOL_KEY,
            "resolved": True, "detail": "resolved",
            "parameters": {"reference_target": "/a.md", "expected_reference": "§9"},
        }]}}]
        cache = build_input_keyed_cache(records)
        self.assertEqual(len(cache), 1)
        key = (CROSS_REF_TOOL_KEY, "/a.md", "§9")
        self.assertIn(key, cache)
        self.assertTrue(cache[key]["resolved"])

    def test_missing_tool_key_is_skipped_not_guessed(self):
        records = [{"trace_id": "t1", "outputs": {"evidence": [{
            "source": "tool", "kind": "cross_reference_check", "tool_key": None,
            "resolved": True, "detail": "resolved", "parameters": {},
        }]}}]
        self.assertEqual(build_input_keyed_cache(records), {})

    def test_fingerprint_list_normalized_to_tuple_for_hashability(self):
        records = [{"trace_id": "t1", "outputs": {"evidence": [{
            "source": "tool", "kind": "cross_reference_check", "tool_key": CROSS_REF_TOOL_KEY,
            "resolved": True, "detail": "resolved",
            "parameters": {"reference_target": "/a.md", "expected_reference": "§9"},
            "fingerprint": ["a=1", "b=2"],  # JSON round-trip shape: list, not tuple
        }]}}]
        cache = build_input_keyed_cache(records)
        key = (CROSS_REF_TOOL_KEY, "/a.md", "§9")
        self.assertEqual(cache[key]["fingerprint"], ("a=1", "b=2"))
        self.assertIsInstance(cache[key]["fingerprint"], tuple)

    def test_missing_fingerprint_is_none_not_fabricated(self):
        records = [{"trace_id": "t1", "outputs": {"evidence": [{
            "source": "tool", "kind": "cross_reference_check", "tool_key": CROSS_REF_TOOL_KEY,
            "resolved": True, "detail": "resolved",
            "parameters": {"reference_target": "/a.md", "expected_reference": "§9"},
        }]}}]
        cache = build_input_keyed_cache(records)
        key = (CROSS_REF_TOOL_KEY, "/a.md", "§9")
        self.assertIsNone(cache[key]["fingerprint"])

    def test_later_record_overwrites_earlier_cache_entry_for_same_key(self):
        params = {"reference_target": "/a.md", "expected_reference": "§9"}
        records = [
            {"trace_id": "t1", "outputs": {"evidence": [{"source": "tool", "kind": "cross_reference_check", "tool_key": CROSS_REF_TOOL_KEY, "resolved": False, "detail": "old", "parameters": params}]}},
            {"trace_id": "t2", "outputs": {"evidence": [{"source": "tool", "kind": "cross_reference_check", "tool_key": CROSS_REF_TOOL_KEY, "resolved": True, "detail": "new", "parameters": params}]}},
        ]
        cache = build_input_keyed_cache(records)
        key = (CROSS_REF_TOOL_KEY, "/a.md", "§9")
        self.assertTrue(cache[key]["resolved"])
        self.assertEqual(cache[key]["detail"], "new")


class MemoryAwareInvokeIntegrationTest(unittest.TestCase):
    """Real, end-to-end: a real cache entry built from a real Tool call,
    consulted through the real memory-aware invoke path (the same one
    the drift experiment and consumption experiments use)."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.cited = self.root / "cited.md"
        self.citing = self.root / "citing.md"
        self.cited.write_text("# Cited\n\n## 9. Heading\n\nBody.\n", encoding="utf-8")
        self.citing.write_text("Cites §9\n", encoding="utf-8")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_cache_hit_on_unchanged_file_serves_without_a_live_call(self):
        from execution.memory.consumption import _make_memory_aware_invoke
        from execution.tool_executor import ToolExecutor
        from execution import verification

        params = {
            "citing_document": str(self.citing), "repository_path": str(self.root),
            "reference_target": str(self.cited), "expected_reference": "§9",
        }
        fp = verification.compute_fingerprint(params)
        cache_key = (CROSS_REF_TOOL_KEY, str(self.cited), "§9")
        cache = {cache_key: {"resolved": True, "detail": "resolved", "fingerprint": fp}}

        call_log = []
        memory_aware_invoke = _make_memory_aware_invoke(cache, call_log)
        REAL_TOOL_PATH = Path(__file__).resolve().parent.parent.parent / "docs" / "architecture" / "organization" / "execution-catalog" / "tool" / "cross-reference-link-validator-interface.md"

        execution = memory_aware_invoke(REAL_TOOL_PATH, "verify_cross_reference", **params)
        self.assertTrue(execution.from_cache)
        self.assertEqual(len(call_log), 1)
        self.assertFalse(call_log[0].real_call)


if __name__ == "__main__":
    unittest.main()
