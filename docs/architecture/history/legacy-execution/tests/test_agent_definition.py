"""
Dedicated unit tests for execution/agent_definition.py.

Foundation Test Coverage Hardening phase. Exercises load() against the
real, on-disk Agent Definition document -- read-only, no modification.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import agent_definition


class LoadTest(unittest.TestCase):
    def test_load_real_agent_definition_returns_expected_shape(self):
        ad = agent_definition.load()
        self.assertEqual(ad.name, "Governance Artifact Integrity Agent")
        self.assertTrue(ad.path.is_file())
        self.assertIsInstance(ad.version, str)
        self.assertIsInstance(ad.permitted_skills, tuple)
        self.assertIsInstance(ad.permitted_workflows, tuple)

    def test_permitted_skills_are_real_existing_files(self):
        ad = agent_definition.load()
        self.assertGreater(len(ad.permitted_skills), 0)
        for p in ad.permitted_skills:
            self.assertTrue(p.is_file(), f"{p} does not exist on disk")

    def test_permitted_workflows_are_real_existing_files(self):
        ad = agent_definition.load()
        self.assertGreater(len(ad.permitted_workflows), 0)
        for p in ad.permitted_workflows:
            self.assertTrue(p.is_file(), f"{p} does not exist on disk")

    def test_load_is_read_only_does_not_modify_the_document(self):
        content_before = agent_definition.AGENT_DEFINITION_PATH.read_text(encoding="utf-8")
        agent_definition.load()
        content_after = agent_definition.AGENT_DEFINITION_PATH.read_text(encoding="utf-8")
        self.assertEqual(content_before, content_after)

    def test_load_is_deterministic(self):
        ad1 = agent_definition.load()
        ad2 = agent_definition.load()
        self.assertEqual(ad1, ad2)


if __name__ == "__main__":
    unittest.main()
