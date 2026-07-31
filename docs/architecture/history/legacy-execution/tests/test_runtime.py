"""
Dedicated unit tests for execution/runtime.py.

Foundation Test Coverage Hardening phase. Exercises bind_runtime()
against the real, on-disk Runtime catalog documents -- read-only.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import runtime


class AvailableRuntimesTest(unittest.TestCase):
    def test_returns_real_runtimes_that_host_agent_instances(self):
        runtimes = runtime.available_runtimes()
        self.assertGreater(len(runtimes), 0)
        for rt in runtimes:
            self.assertTrue(rt.path.is_file())
            self.assertTrue(rt.canonical_key.startswith("runtime."))

    def test_batch_governance_review_substrate_is_present(self):
        keys = {rt.canonical_key for rt in runtime.available_runtimes()}
        self.assertIn("runtime.batch-governance-review-substrate", keys)


class BindRuntimeTest(unittest.TestCase):
    REAL_AGENT_NAME = "Governance Artifact Integrity Agent"

    def test_default_selector_returns_a_real_hosting_runtime(self):
        rt = runtime.bind_runtime(self.REAL_AGENT_NAME)
        self.assertTrue(rt.canonical_key.startswith("runtime."))
        self.assertIn(self.REAL_AGENT_NAME, runtime.read(rt.path))

    def test_explicit_valid_selector_is_honored(self):
        rt = runtime.bind_runtime(self.REAL_AGENT_NAME, selector="runtime.batch-governance-review-substrate")
        self.assertEqual(rt.canonical_key, "runtime.batch-governance-review-substrate")

    def test_unknown_agent_name_raises(self):
        with self.assertRaises(RuntimeError):
            runtime.bind_runtime("An Agent That Does Not Exist Anywhere")

    def test_selector_naming_nonexistent_runtime_raises(self):
        with self.assertRaises(RuntimeError):
            runtime.bind_runtime(self.REAL_AGENT_NAME, selector="runtime.does-not-exist")

    def test_selector_naming_real_runtime_that_does_not_host_this_agent_raises(self):
        # find a real runtime that does NOT declare this agent, if any exists
        all_runtimes = runtime.available_runtimes()
        non_hosting = [rt for rt in all_runtimes if self.REAL_AGENT_NAME not in runtime.read(rt.path)]
        if not non_hosting:
            self.skipTest("every real runtime currently hosts this agent; no negative case available")
        with self.assertRaises(RuntimeError):
            runtime.bind_runtime(self.REAL_AGENT_NAME, selector=non_hosting[0].canonical_key)

    def test_bind_is_read_only(self):
        rt = runtime.available_runtimes()[0]
        before = rt.path.read_text(encoding="utf-8")
        runtime.bind_runtime(self.REAL_AGENT_NAME)
        after = rt.path.read_text(encoding="utf-8")
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
