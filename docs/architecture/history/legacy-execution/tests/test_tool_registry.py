"""
Dedicated unit tests for execution/tool_registry.py.

Foundation Test Coverage Hardening phase.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution.tool_registry import ToolRegistry


class ToolRegistryTest(unittest.TestCase):
    def test_register_then_get_returns_registration(self):
        registry = ToolRegistry()
        adapter = lambda **kw: {"resolved": True}
        registry.register("tool.x", adapter)
        reg = registry.get("tool.x")
        self.assertIs(reg.adapter, adapter)
        self.assertEqual(reg.tool_key, "tool.x")

    def test_get_unregistered_key_returns_none(self):
        registry = ToolRegistry()
        self.assertIsNone(registry.get("tool.nonexistent"))

    def test_default_legacy_is_true(self):
        registry = ToolRegistry()
        registry.register("tool.x", lambda **kw: None)
        self.assertTrue(registry.get("tool.x").legacy)

    def test_default_cache_key_fn_is_none(self):
        registry = ToolRegistry()
        registry.register("tool.x", lambda **kw: None)
        self.assertIsNone(registry.get("tool.x").cache_key_fn)

    def test_register_with_cache_key_fn_and_legacy_false(self):
        registry = ToolRegistry()
        key_fn = lambda request: ("k",)
        registry.register("tool.x", lambda **kw: None, cache_key_fn=key_fn, legacy=False)
        reg = registry.get("tool.x")
        self.assertIs(reg.cache_key_fn, key_fn)
        self.assertFalse(reg.legacy)

    def test_re_register_same_key_overwrites(self):
        registry = ToolRegistry()
        first = lambda **kw: "first"
        second = lambda **kw: "second"
        registry.register("tool.x", first)
        registry.register("tool.x", second)
        self.assertIs(registry.get("tool.x").adapter, second)

    def test_all_returns_every_registration(self):
        registry = ToolRegistry()
        registry.register("tool.a", lambda **kw: None)
        registry.register("tool.b", lambda **kw: None)
        all_regs = registry.all()
        self.assertEqual(set(all_regs.keys()), {"tool.a", "tool.b"})

    def test_all_returns_a_copy_not_live_reference(self):
        registry = ToolRegistry()
        registry.register("tool.a", lambda **kw: None)
        snapshot = registry.all()
        registry.register("tool.b", lambda **kw: None)
        self.assertNotIn("tool.b", snapshot)


if __name__ == "__main__":
    unittest.main()
