"""
Dedicated unit tests for execution/tool_executor.py.

Foundation Test Coverage Hardening phase. Uses a real ToolRegistry with
small, real (not mocked-away) adapter functions, and real temporary
files where fingerprinting is exercised -- avoids mocking behavior that
can instead be exercised for real.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution.tool import ToolRequest
from execution.tool_contract import ToolResponse
from execution.tool_executor import ToolExecutor
from execution.tool_registry import ToolRegistry


def _content_only_adapter(passage_a=None, passage_b=None):
    return {"resolved": passage_a == passage_b, "failure_reason": None if passage_a == passage_b else "differ"}


def _file_adapter(document_path=None):
    text = Path(document_path).read_text(encoding="utf-8")
    return {"resolved": len(text) > 0, "failure_reason": None}


def _legacy_response_adapter(**kwargs):
    return ToolResponse(status=True, payload={"x": 1}, failure_reason=None)


def _raising_adapter(**kwargs):
    raise ValueError("adapter blew up")


class ExecuteWithoutCacheTest(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry()
        self.registry.register("tool.content", _content_only_adapter)
        self.executor = ToolExecutor(self.registry)

    def test_unregistered_tool_returns_not_implemented(self):
        result = self.executor.execute(ToolRequest(tool_canonical_key="tool.missing", action="x", parameters={}))
        self.assertFalse(result.succeeded)
        self.assertEqual(result.error, "not_implemented")

    def test_successful_call_returns_raw_and_response(self):
        result = self.executor.execute(ToolRequest(
            tool_canonical_key="tool.content", action="compare", parameters={"passage_a": "x", "passage_b": "x"},
        ))
        self.assertTrue(result.succeeded)
        self.assertTrue(result.raw["resolved"])
        self.assertTrue(result.response.status)

    def test_no_cache_means_every_call_is_live(self):
        result = self.executor.execute(ToolRequest(
            tool_canonical_key="tool.content", action="compare", parameters={"passage_a": "x", "passage_b": "y"},
        ))
        self.assertFalse(result.from_cache)
        self.assertEqual(result.verification_status, "not_applicable")

    def test_adapter_exception_is_caught_and_reported(self):
        registry = ToolRegistry()
        registry.register("tool.raises", _raising_adapter)
        executor = ToolExecutor(registry)
        result = executor.execute(ToolRequest(tool_canonical_key="tool.raises", action="x", parameters={}))
        self.assertFalse(result.succeeded)
        self.assertIn("ValueError", result.error)
        self.assertIn("adapter blew up", result.error)

    def test_legacy_toolresponse_adapter_normalized_correctly(self):
        registry = ToolRegistry()
        registry.register("tool.legacy", _legacy_response_adapter)
        executor = ToolExecutor(registry)
        result = executor.execute(ToolRequest(tool_canonical_key="tool.legacy", action="x", parameters={}))
        self.assertTrue(result.succeeded)
        self.assertIsInstance(result.response, ToolResponse)
        self.assertTrue(result.response.status)

    def test_deterministic_repeat_calls_produce_same_result(self):
        req = ToolRequest(tool_canonical_key="tool.content", action="compare", parameters={"passage_a": "a", "passage_b": "b"})
        r1 = self.executor.execute(req)
        r2 = self.executor.execute(req)
        self.assertEqual(r1.raw, r2.raw)


class ExecuteWithCacheTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.tmpdir.name) / "f.md"
        self.file_path.write_text("real content", encoding="utf-8")

        self.registry = ToolRegistry()
        self.registry.register(
            "tool.file", _file_adapter,
            cache_key_fn=lambda request: ("tool.file", request.parameters.get("document_path")),
        )
        self.cache = {}
        self.executor = ToolExecutor(self.registry, cache=self.cache)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_cache_miss_executes_live_and_populates_cache(self):
        req = ToolRequest(tool_canonical_key="tool.file", action="x", parameters={"document_path": str(self.file_path)})
        result = self.executor.execute(req)
        self.assertFalse(result.from_cache)
        self.assertEqual(result.verification_status, "no_entry")
        self.assertEqual(len(self.cache), 1)

    def test_cache_hit_with_unchanged_file_is_verified_and_served_from_cache(self):
        req = ToolRequest(tool_canonical_key="tool.file", action="x", parameters={"document_path": str(self.file_path)})
        self.executor.execute(req)  # populates cache
        result = self.executor.execute(req)
        self.assertTrue(result.from_cache)
        self.assertEqual(result.verification_status, "verified")

    def test_cache_hit_with_changed_file_is_invalidated_and_re_executed(self):
        req = ToolRequest(tool_canonical_key="tool.file", action="x", parameters={"document_path": str(self.file_path)})
        self.executor.execute(req)
        self.file_path.write_text("changed content", encoding="utf-8")
        result = self.executor.execute(req)
        self.assertFalse(result.from_cache)
        self.assertEqual(result.verification_status, "invalidated")

    def test_invalidated_entry_is_removed_before_live_call_not_left_stale(self):
        req = ToolRequest(tool_canonical_key="tool.file", action="x", parameters={"document_path": str(self.file_path)})
        self.executor.execute(req)
        cache_key = ("tool.file", str(self.file_path))
        self.file_path.write_text("changed again", encoding="utf-8")
        self.executor.execute(req)
        # after re-execution the cache must reflect the *new* fingerprint, not the stale one
        self.assertIn(cache_key, self.cache)
        self.assertNotEqual(self.cache[cache_key]["fingerprint"], None)

    def test_cache_without_registered_cache_key_fn_is_never_consulted(self):
        registry = ToolRegistry()
        registry.register("tool.nocachefn", _content_only_adapter)  # no cache_key_fn
        executor = ToolExecutor(registry, cache={})
        result = executor.execute(ToolRequest(tool_canonical_key="tool.nocachefn", action="x", parameters={"passage_a": "a", "passage_b": "a"}))
        self.assertEqual(result.verification_status, "not_applicable")
        self.assertFalse(result.from_cache)

    def test_execution_never_mutates_the_request_object(self):
        req = ToolRequest(tool_canonical_key="tool.file", action="x", parameters={"document_path": str(self.file_path)})
        params_snapshot = dict(req.parameters)
        self.executor.execute(req)
        self.assertEqual(req.parameters, params_snapshot)


if __name__ == "__main__":
    unittest.main()
