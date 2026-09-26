"""FS-09 — the readiness gate: evaluated live, and ratification is read, not assumed."""

from __future__ import annotations

import unittest

from fullstack import readiness
from fullstack.readiness import BLOCKED, FAIL, NOT_READY, PACKAGES, ratified

RATIFY_ALL = "\n".join(
    f"### {p}-R — Architect Decision · test fixture\n\n| Field | Value |\n|---|---|\n"
    f"| **Identifier** | `{p}-R` |\n| **Decided by** | Architect |\n| **Ratifies** | {p} |\n"
    for p in PACKAGES)


class Ratification(unittest.TestCase):
    def test_only_a_decided_register_entry_ratifies(self):
        self.assertEqual({}, ratified("### X — Proposal\n\n| **Ratifies** | FS-DP-01 |\n"))
        self.assertEqual({}, ratified("| **Decided by** | Architect |\n| **Ratifies** | FS-DP-01 |\n"))
        self.assertEqual(set(PACKAGES), set(ratified(RATIFY_ALL)))

    def test_nothing_is_ratified_today(self):
        self.assertEqual({}, ratified(readiness.REGISTER.read_text(encoding="utf-8")))

    def test_a_decision_package_cannot_ratify_itself(self):
        for path in (readiness.REPO_ROOT / "docs/fullstack/decision-packages").glob("*.md"):
            with self.subTest(package=path.name):
                self.assertEqual({}, ratified(path.read_text(encoding="utf-8")))


class TheGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.live = readiness.evaluate(runs=2)

    def test_it_is_not_ready_and_says_exactly_why(self):
        self.assertEqual(NOT_READY, self.live["result"])
        self.assertEqual(["FS-DP-01", "FS-DP-02", "FS-DP-03", "FS-DP-04", "FS-DP-06",
                          "FS-DP-07"], self.live["awaiting"])
        self.assertEqual([], [c for c in self.live["criteria"] if c["status"] == FAIL])

    def test_every_measurable_criterion_passes(self):
        measured = [c for c in self.live["criteria"] if c["status"] != BLOCKED]
        self.assertEqual({"PASS", "OBSERVED"}, {c["status"] for c in measured})

    def test_ratification_alone_does_not_make_it_ready(self):
        """A ratified package still needs its implementation: BLOCKED becomes FAIL."""
        gate = readiness.evaluate(runs=1, register_text=RATIFY_ALL)
        self.assertEqual(NOT_READY, gate["result"])
        self.assertEqual([], gate["awaiting"])
        self.assertTrue([c for c in gate["criteria"] if c["status"] == FAIL])

    def test_the_gate_never_releases(self):
        self.assertIn("never releases", self.live["release"])
        self.assertIn("D4-A", self.live["release"])

    def test_external_dependencies_are_named(self):
        self.assertEqual(["EXT-01", "EXT-02"],
                         [d["id"] for d in self.live["external_dependencies"]])


if __name__ == "__main__":
    unittest.main()
