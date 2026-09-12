"""P12-W6 runtime integration conformance (`§30`)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import p12_runtime_verification as rt


class TheScopeIsSection30s(unittest.TestCase):
    def test_the_nine_items_are_section_30s_in_order(self):
        self.assertEqual(
            list(rt.RUNTIME_ITEMS),
            ["runtime entry points", "runtime state", "runtime-hosted workflows",
             "execution actors", "state transitions", "observation",
             "verification", "failure", "persistence"])

    def test_every_item_has_a_probe(self):
        self.assertEqual(set(rt._ITEMS), set(rt.RUNTIME_ITEMS))


class ReachabilityIsMeasuredFromTheImportGraph(unittest.TestCase):
    """Not from file names: `..._proof.py` is a name, not a measurement."""

    def test_no_entry_point_is_classified_by_its_name(self):
        """Executable literals only.

        The first version of this control scanned every string constant and
        matched the module docstring — the paragraph explaining that names are
        *not* used. Docstrings are documentation, not classification logic, so
        they are removed before the check; otherwise the control fires on its
        own explanation, which is the same shape as a locator guard matching
        the comment that describes it.
        """
        import ast
        source = (rt.REPO_ROOT / "tools" / "p12_runtime_verification.py"
                  ).read_text(encoding="utf-8")
        tree = ast.parse(source)
        docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                                 ast.AsyncFunctionDef)):
                body = getattr(node, "body", None)
                if body and isinstance(body[0], ast.Expr) and isinstance(
                        body[0].value, ast.Constant) and isinstance(
                            body[0].value.value, str):
                    docstrings.add(id(body[0].value))
        literals = [n.value for n in ast.walk(tree)
                    if isinstance(n, ast.Constant)
                    and isinstance(n.value, str)
                    and id(n) not in docstrings]
        self.assertFalse([s for s in literals if "_proof" in s],
                         "a name-based classification has crept in")

    def test_an_entry_point_reached_only_by_another_root_script_is_hand_invoked(self):
        points = {p.module: p for p in rt.entry_points()}
        subject = points.get("w1_coordination_proof.py")
        self.assertIsNotNone(subject)
        self.assertIn("p12_w4_observed_work_proof.py", subject.reached_by)
        self.assertEqual(subject.status, rt.HAND_INVOKED,
                         "two hand-invoked scripts do not make one reachable")

    def test_an_entry_point_reached_from_a_package_is_reached(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "entry.py").write_text("x = 1\n", encoding="utf-8")
            package = root / "pkg"
            package.mkdir()
            (package / "consumer.py").write_text("import entry\n",
                                                 encoding="utf-8")
            with mock.patch.object(rt, "REPO_ROOT", root):
                points = {p.module: p for p in rt.entry_points()}
                self.assertEqual(points["entry.py"].status, rt.REACHED)

    def test_the_live_system_is_hand_invoked_only(self):
        reach = rt.reachability()
        self.assertEqual(reach["status"], rt.HAND_INVOKED)
        self.assertEqual(reach["reached_by_the_system"], 0)
        self.assertGreater(reach["entry_points"], 0)


class TheProbesReadRealSurfaces(unittest.TestCase):
    def test_observation_reads_a_count_not_a_sequence(self):
        """It called len() on an int and reported a working surface ABSENT."""
        result = rt._observation()
        self.assertEqual(result.status, rt.DISCOVERED)
        self.assertGreater(result.count, 0)
        self.assertNotIn("raised", result.detail)

    def test_no_probe_reports_its_own_exception_as_a_finding(self):
        for result in rt.verify():
            with self.subTest(result.item):
                self.assertNotIn("probe raised", result.detail)

    def test_verification_is_absent_in_the_ratified_vocabulary(self):
        result = {r.item: r for r in rt.verify()}["verification"]
        self.assertEqual(result.status, rt.ABSENT)

    def test_verification_would_be_discovered_if_the_vocabulary_held_it(self):
        with mock.patch("native_core.core.trace.VALID_STATUSES",
                        frozenset({"success", "verified"})):
            self.assertEqual(rt._verification().status, rt.DISCOVERED)

    def test_a_single_observed_state_is_not_a_transition(self):
        class _One:
            state = "RuntimeState.STOPPED"

        with mock.patch("tools.p12_runtime_observation.observations",
                        return_value=[_One(), _One()]):
            self.assertEqual(rt._state_transitions().status, rt.ABSENT)


class DiscoveryIsSeparateFromIntegration(unittest.TestCase):
    def test_the_summary_reports_both_and_merges_neither(self):
        summary = rt.summary()
        self.assertIn("discovered", summary)
        self.assertIn("reachability", summary)
        self.assertEqual(summary["reachability"], rt.HAND_INVOKED)
        self.assertGreater(summary["discovered"], 0)


if __name__ == "__main__":
    unittest.main()
