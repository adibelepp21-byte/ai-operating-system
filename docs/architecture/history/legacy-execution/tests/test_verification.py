"""
Dedicated unit tests for execution/verification.py (Tier 2 Evidence
Verification Layer). Foundation Test Coverage Hardening phase.

Uses real, temporary on-disk files -- fingerprinting is defined in
terms of real file content, so faking it would test nothing real.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import verification


class ComputeFingerprintTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.tmpdir.name) / "f.md"
        self.file_path.write_text("hello world", encoding="utf-8")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_no_file_shaped_parameters_returns_none(self):
        self.assertIsNone(verification.compute_fingerprint({"passage_a": "x", "passage_b": "y"}))

    def test_empty_parameters_returns_none(self):
        self.assertIsNone(verification.compute_fingerprint({}))

    def test_real_file_parameter_produces_a_fingerprint(self):
        fp = verification.compute_fingerprint({"document_path": str(self.file_path)})
        self.assertIsNotNone(fp)
        self.assertEqual(len(fp), 1)
        self.assertTrue(fp[0].startswith("document_path="))

    def test_nonexistent_file_path_string_is_ignored_not_errored(self):
        fp = verification.compute_fingerprint({"document_path": str(self.file_path) + "-does-not-exist"})
        self.assertIsNone(fp)

    def test_non_string_values_ignored(self):
        fp = verification.compute_fingerprint({"count": 5, "flag": True, "items": ["a", "b"]})
        self.assertIsNone(fp)

    def test_fingerprint_is_order_independent_by_key(self):
        params_a = {"a_path": str(self.file_path), "b_val": "x"}
        second_file = Path(self.tmpdir.name) / "g.md"
        second_file.write_text("other", encoding="utf-8")
        params_a["b_path"] = str(second_file)
        fp1 = verification.compute_fingerprint({"b_path": str(second_file), "a_path": str(self.file_path)})
        fp2 = verification.compute_fingerprint({"a_path": str(self.file_path), "b_path": str(second_file)})
        self.assertEqual(fp1, fp2)

    def test_different_content_produces_different_fingerprint(self):
        other = Path(self.tmpdir.name) / "different.md"
        other.write_text("completely different content", encoding="utf-8")
        fp1 = verification.compute_fingerprint({"path": str(self.file_path)})
        fp2 = verification.compute_fingerprint({"path": str(other)})
        self.assertNotEqual(fp1, fp2)

    def test_same_content_same_path_produces_same_fingerprint(self):
        fp1 = verification.compute_fingerprint({"path": str(self.file_path)})
        fp2 = verification.compute_fingerprint({"path": str(self.file_path)})
        self.assertEqual(fp1, fp2)

    def test_real_content_edit_changes_fingerprint(self):
        fp_before = verification.compute_fingerprint({"path": str(self.file_path)})
        self.file_path.write_text("hello world, edited", encoding="utf-8")
        fp_after = verification.compute_fingerprint({"path": str(self.file_path)})
        self.assertNotEqual(fp_before, fp_after)


class VerifyTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.tmpdir.name) / "f.md"
        self.file_path.write_text("hello world", encoding="utf-8")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_content_only_call_always_verifies(self):
        # cached_fingerprint is realistically None here too: it would have
        # been produced by compute_fingerprint() on this same content-only
        # parameter shape at cache-write time, which also returns None.
        self.assertTrue(verification.verify(None, {"passage_a": "x", "passage_b": "y"}))
        self.assertTrue(verification.verify(None, {"passage_a": "x"}))

    def test_matching_fingerprint_verifies(self):
        params = {"path": str(self.file_path)}
        fp = verification.compute_fingerprint(params)
        self.assertTrue(verification.verify(fp, params))

    def test_missing_cached_fingerprint_fails_closed(self):
        params = {"path": str(self.file_path)}
        self.assertFalse(verification.verify(None, params))

    def test_changed_file_fails_verification(self):
        params = {"path": str(self.file_path)}
        fp = verification.compute_fingerprint(params)
        self.file_path.write_text("changed content", encoding="utf-8")
        self.assertFalse(verification.verify(fp, params))

    def test_stale_fingerprint_from_deleted_file_fails_closed(self):
        """Repaired under Architect Authorization following Foundation
        Test Coverage Hardening: verify() now distinguishes "never had a
        file-shaped parameter" from "had one, it's gone now" by also
        checking whether cached_fingerprint was ever non-None, instead of
        treating any None current-fingerprint as automatically valid."""
        params = {"path": str(self.file_path)}
        fp = verification.compute_fingerprint(params)
        self.file_path.unlink()
        self.assertFalse(verification.verify(fp, params))


if __name__ == "__main__":
    unittest.main()
