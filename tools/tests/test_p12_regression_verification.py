"""P12-W6 phase-level regression verification conformance (`§51`).

Ten `HELD` is exactly what a module that checks nothing would print. Every
control here exists to make one anchor drift on demand, so that a `HELD` is a
measurement rather than a default.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from tools import p12_regression_verification as reg


class TheScopeIsSection51s(unittest.TestCase):
    def test_the_eleven_classes_are_section_51s_in_order(self):
        self.assertEqual(
            list(reg.REGRESSION_CLASSES),
            ["functional", "authority", "governance", "state", "runtime",
             "workflow", "evidence", "provenance", "boundary", "security",
             "quality"])

    def test_every_class_has_an_anchor_entry(self):
        self.assertEqual(set(reg.ANCHORS), set(reg.REGRESSION_CLASSES))

    def test_the_baseline_is_the_p11_certification_commit(self):
        subject = reg._git("log", "-1", "--format=%s", reg.BASELINE)
        self.assertIn("FD-P11-002", subject)


class TheStructuralComparisonCanDetectLoss(unittest.TestCase):
    """The one control that needs no class mapping, and cannot be narrowed."""

    def test_a_removed_control_is_a_regression(self):
        before = {"a.py::C::test_one": 3, "a.py::C::test_two": 2}
        after = {"a.py::C::test_one": 3}
        with mock.patch.object(reg, "inventory",
                               side_effect=[before, after]):
            result = reg.structural()
        self.assertEqual(result["status"], reg.REGRESSED)
        self.assertEqual(result["removed"], ("a.py::C::test_two",))

    def test_a_weakened_control_is_a_regression(self):
        before = {"a.py::C::test_one": 3}
        after = {"a.py::C::test_one": 1}
        with mock.patch.object(reg, "inventory", side_effect=[before, after]):
            result = reg.structural()
        self.assertEqual(result["status"], reg.REGRESSED)
        self.assertEqual(result["weakened"], (("a.py::C::test_one", 3, 1),))

    def test_a_renamed_control_reads_as_removed(self):
        """Renaming is how a control disappears while the count goes up."""
        before = {"a.py::C::test_one": 3}
        after = {"a.py::C::test_one_renamed": 3, "a.py::C::test_new": 1}
        with mock.patch.object(reg, "inventory", side_effect=[before, after]):
            result = reg.structural()
        self.assertEqual(result["status"], reg.REGRESSED)
        self.assertEqual(result["removed"], ("a.py::C::test_one",))

    def test_growth_alone_is_not_a_regression(self):
        before = {"a.py::C::test_one": 3}
        after = {"a.py::C::test_one": 3, "a.py::C::test_two": 1}
        with mock.patch.object(reg, "inventory", side_effect=[before, after]):
            self.assertEqual(reg.structural()["status"], reg.HELD)

    def test_a_lost_assert_raises_context_manager_is_counted(self):
        """`with self.assertRaises(...)` is the assertion in most controls."""
        import ast
        strong = ast.parse(
            "def test_x(self):\n"
            "    with self.assertRaises(ValueError):\n"
            "        f()\n").body[0]
        stripped = ast.parse("def test_x(self):\n    f()\n").body[0]
        self.assertGreater(reg._assertion_weight(strong),
                           reg._assertion_weight(stripped))

    def test_the_live_comparison_runs_against_two_real_revisions(self):
        result = reg.structural()
        self.assertEqual(result["baseline"], reg.BASELINE)
        self.assertGreater(result["controls_at_baseline"], 1000)
        self.assertGreaterEqual(result["controls_now"],
                                result["controls_at_baseline"])


class AnUnanchoredClassHasNotHeld(unittest.TestCase):
    def test_a_none_anchor_is_unanchored_not_held(self):
        with mock.patch.dict(reg.ANCHORS,
                             {"quality": lambda: (None, True, "nothing ran")}):
            result = [r for r in reg.verify()
                      if r.regression_class == "quality"][0]
        self.assertEqual(result.status, reg.UNANCHORED)

    def test_unanchored_is_excluded_from_held(self):
        summary = reg.summary()
        self.assertNotIn("quality", [c for c in reg.REGRESSION_CLASSES
                                     if c not in summary["unanchored_classes"]
                                     and c == "quality"])
        self.assertIn("quality", summary["unanchored_classes"])
        self.assertEqual(summary["held"] + summary["regressed"]
                         + summary["unanchored"] + summary["unavailable"],
                         summary["classes"])

    def test_a_raising_anchor_is_unavailable_not_held(self):
        def explode():
            raise RuntimeError("verifier import failed")

        with mock.patch.dict(reg.ANCHORS, {"runtime": explode}):
            result = [r for r in reg.verify()
                      if r.regression_class == "runtime"][0]
        self.assertEqual(result.status, reg.UNAVAILABLE)
        self.assertIn("verifier import failed", result.detail)


class EveryAnchorCanReportRegressed(unittest.TestCase):
    """Without this, ten HELD proves nothing about P4–P11 behavior."""

    def test_a_failing_anchor_is_reported_as_regressed(self):
        for name in reg.REGRESSION_CLASSES:
            with self.subTest(name):
                with mock.patch.dict(
                        reg.ANCHORS,
                        {name: lambda: ("some anchor", False, "it drifted")}):
                    result = [r for r in reg.verify()
                              if r.regression_class == name][0]
                self.assertEqual(result.status, reg.REGRESSED)

    def test_regressed_classes_are_named_in_the_summary(self):
        with mock.patch.dict(
                reg.ANCHORS,
                {"state": lambda: ("stale_state_audit.audit", False, "drift")}):
            summary = reg.summary()
        self.assertEqual(summary["regressed_classes"], ("state",))
        self.assertEqual(summary["regressed"], 1)


class EachAnchorRunsARealVerifier(unittest.TestCase):
    def test_the_boundary_anchor_drifts_when_the_boundary_set_does(self):
        import tempfile
        from tools import derived_views as views
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "native_core" / "core"
            fake.mkdir(parents=True)
            for name in views._boundaries(reg.REPO_ROOT):
                (fake / name).mkdir()
            (fake / "twelfth").mkdir()
            with mock.patch.object(reg, "REPO_ROOT", Path(tmp)):
                _, held, detail = reg._boundary()
        self.assertFalse(held)
        self.assertIn("12", detail)

    def test_the_boundary_anchor_holds_on_the_resident_tree(self):
        anchor, held, detail = reg._boundary()
        self.assertTrue(held)
        self.assertIn("11 boundaries", detail)

    def test_the_provenance_anchor_refuses_an_unresolvable_citation(self):
        _, held, detail = reg._provenance()
        self.assertTrue(held)
        self.assertIn("does not resolve", detail)

    def test_the_security_anchor_names_a_protected_root(self):
        from tools import p12_certified_evidence_guard as guard
        self.assertTrue(guard.certified_phases())
        _, held, _ = reg._security()
        self.assertTrue(held)

    def test_the_evidence_anchor_reads_the_whole_corpus(self):
        _, held, detail = reg._evidence()
        self.assertTrue(held)
        self.assertIn("citations", detail)

    def test_the_governance_anchor_checks_hashes_not_only_parsing(self):
        _, held, detail = reg._governance()
        self.assertTrue(held)
        self.assertIn("0 stale", detail)


class WhatThisSuiteDoesNotEstablish(unittest.TestCase):
    """Stated as a control so it cannot be quietly dropped."""

    def test_a_class_is_only_as_covered_as_its_anchor(self):
        held = [r for r in reg.verify() if r.status == reg.HELD]
        for result in held:
            self.assertIsNotNone(
                result.anchor,
                "HELD without a named anchor would be an unfalsifiable claim")

    def test_quality_remains_unanchored(self):
        summary = reg.summary()
        self.assertIn(
            "quality", summary["unanchored_classes"],
            "if a resident quality gate has since been built, this finding is "
            "closed and the evidence record must say so")


if __name__ == "__main__":
    unittest.main()
