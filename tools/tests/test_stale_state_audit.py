"""Tests for the stale-state detector (`ACT §26` — the tenth property).

`ACT §26`: *"A test that cannot observe the defect it claims to detect is
invalid."* So the positive cases plant a defect and require it to be seen, and
the negative cases plant the exact false positive the first version produced.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.stale_state_audit import (  # noqa: E402
    PROXIMITY,
    ZERO_FIGURE,
    audit,
    superseded_claims,
    _marked_historical,
)


class TheSupersededSetComesFromTheRegister(unittest.TestCase):
    """Nothing is hard-coded: delete a Register row and the check goes with it."""

    def test_claims_are_extracted(self):
        claims = superseded_claims()
        self.assertGreater(len(claims), 0, "the Register's S-rows changed shape")
        phases = {c["phase"] for c in claims}
        self.assertIn("9", phases, "the Phase 9 supersession is the load-bearing one")

    def test_every_claim_carries_its_register_id_and_quote(self):
        for claim in superseded_claims():
            self.assertRegex(claim["id"], r"^S-\d+$")
            self.assertTrue(claim["quote"].strip())

    def test_an_inert_checker_reports_itself(self):
        """Zero claims must not read as a clean corpus."""
        result = audit()
        self.assertGreater(
            result["claims_extracted"], 0,
            "with zero claims the checker is inert and must say so, not pass",
        )


class TheFalsePositiveThatShipped(unittest.TestCase):
    """Regression for two defects found before this checker was committed."""

    def test_zero_percent_does_not_match_inside_one_hundred_percent(self):
        self.assertIsNone(ZERO_FIGURE.search("coverage is currently 100%"))
        self.assertIsNone(ZERO_FIGURE.search("throughput fell to 50%"))
        self.assertIsNotNone(ZERO_FIGURE.search("Phase 9 stands at 0%"))

    def test_two_unrelated_facts_on_one_long_line_are_not_a_claim(self):
        """The exact line that produced the first false positive."""
        line = (
            "Phase 6/7/8 work added documentation and one code repair, and "
            + "x" * 200
            + " Tool-registration coverage is currently 100% but unenforced."
        )
        self.assertGreater(
            line.index("100%") - line.index("Phase 6"), PROXIMITY,
            "fixture no longer exercises the proximity rule",
        )


class ItSeesTheDefectItClaimsToDetect(unittest.TestCase):
    """Positive detection, on a planted assertion."""

    def _probe(self, text):
        probe = REPO_ROOT / "docs" / "ZZ_STALE_PROBE.md"
        probe.write_text(text, encoding="utf-8")
        try:
            result = audit()
            return [
                f for f in result["findings"]
                if "ZZ_STALE_PROBE" in f["source"]
            ]
        finally:
            probe.unlink()

    def test_an_unmarked_stale_assertion_is_an_error(self):
        found = self._probe("The gate is shut because Phase 9 is at 0% today.\n")
        self.assertTrue(found, "planted stale assertion was not seen")
        self.assertEqual(found[0]["severity"], "ERROR", found)

    def test_the_same_assertion_marked_historical_is_not_an_error(self):
        found = self._probe(
            "Historical note, superseded 2026-09-09.\n\n"
            "The gate is shut because Phase 9 is at 0% today.\n"
        )
        self.assertTrue(found, "the marked use should still be reported as INFO")
        self.assertEqual(found[0]["severity"], "INFO", found)


class TheCorpusIsCurrentlyClean(unittest.TestCase):
    """Pins the result of the remediation, so a regression is visible."""

    def test_no_stale_current_state_assertions_remain(self):
        result = audit()
        stale = [f for f in result["findings"] if f["severity"] == "ERROR"]
        self.assertEqual(stale, [], stale)

    def test_historical_uses_are_preserved_rather_than_removed(self):
        """`ACT §16`/`§47`: history is marked, never rewritten."""
        result = audit()
        self.assertGreater(
            result["historical_uses"], 0,
            "zero historical uses would mean the figures were deleted, not marked",
        )


class TheGuardHolds(unittest.TestCase):
    def test_no_finding_comes_from_a_protected_untracked_path(self):
        """Tracked files under `docs/program/` are readable; untracked are not.

        The first version of this test compared ``source`` — which carries a
        ``:line`` suffix — against the tracked set, so every tracked file there
        looked untracked. The suffix is stripped now.
        """
        tracked = _tracked_sources()
        for finding in audit()["findings"]:
            path = finding["source"].rsplit(":", 1)[0]
            if path.startswith("docs/program/"):
                self.assertIn(path, tracked, finding)

    def test_an_untracked_protected_file_is_never_read(self):
        """Positive guard probe, not merely the absence of a finding."""
        probe = REPO_ROOT / "docs" / "program" / "ZZ_STALE_GUARD_PROBE.md"
        probe.write_text("Phase 9 is at 0% today.\n", encoding="utf-8")
        try:
            sources = {f["source"] for f in audit()["findings"]}
            self.assertFalse(
                any("ZZ_STALE_GUARD_PROBE" in s for s in sources),
                "an untracked file under a protected prefix was read",
            )
        finally:
            probe.unlink()


def _tracked_sources():
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=str(REPO_ROOT),
        capture_output=True, text=True, check=True,
    ).stdout
    return {p for p in out.split("\0") if p}


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
