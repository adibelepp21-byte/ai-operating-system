"""P12-W6 cross-platform relationship evidence conformance (`§48` v1.1).

Eighteen evidenced pairs is also what a module that read nothing and returned a
constant would print. Every control here makes the measurement move against a
constructed corpus, so that a state is a reading rather than a default.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools import p12_cross_platform_verification as xpl


def _corpus(root: Path, volume: str, division: str, sections: dict) -> None:
    directory = root / volume / division
    directory.mkdir(parents=True)
    for stem, body in sections.items():
        (directory / f"{stem}.md").write_text(body, encoding="utf-8")


class TheScopeIsSection48sTenDivisions(unittest.TestCase):
    def test_all_ten_divisions_are_present_in_v1_1_order(self):
        self.assertEqual([d for d, _ in xpl.DIVISIONS],
                         [f"PD-{n:02d}" for n in range(1, 11)])

    def test_the_four_divisions_v1_0_omitted_are_restored(self):
        present = {d for d, _ in xpl.DIVISIONS}
        for restored in ("PD-01", "PD-02", "PD-06", "PD-07"):
            self.assertIn(restored, present)

    def test_the_pd_10_naming_conflict_is_carried_not_resolved(self):
        names = dict(xpl.DIVISIONS)["PD-10"]
        self.assertEqual(set(names),
                         {"Developer Experience", "Developer Enablement"})

    def test_the_population_is_ninety_ordered_pairs(self):
        self.assertEqual(len(xpl.pairs()), 90)


class NothingIsPromotedBeyondWhatTheSourceSays(unittest.TestCase):
    def test_no_pair_is_reported_verified_or_defined(self):
        rendered = repr(sorted(set(xpl.pairs().values()))).upper()
        self.assertNotIn("VERIFIED", rendered)
        self.assertNotIn("DEFINED", rendered)

    def test_no_interface_is_claimed(self):
        summary = xpl.summary()
        self.assertEqual(summary["interfaces_defined"], 0)
        self.assertEqual(summary["interfaces_verified"], 0)

    def test_an_absent_corpus_is_source_absent_not_no_relationship(self):
        """`§43` — `UNKNOWN ≠ FALSE`."""
        state = xpl.pairs()
        self.assertEqual(state[("PD-06", "PD-01")], xpl.SOURCE_ABSENT)


class TheMeasurementActuallyReadsTheBodies(unittest.TestCase):
    def test_a_mention_outside_a_relationship_heading_is_not_evidence(self):
        """`§48`: not verified merely because both surfaces exist."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _corpus(root, "volume-1", "pd-01-x",
                    {"E4": "E4 — KPI & Success Metrics Framework\nsee PD-02\n"})
            _corpus(root, "volume-2", "pd-02-y", {"A1": "A1 — Identity\n"})
            self.assertEqual(xpl.pairs(root)[("PD-01", "PD-02")], xpl.MENTIONED)

    def test_a_relationship_heading_makes_it_self_declared(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _corpus(root, "volume-1", "pd-01-x",
                    {"C8": "C8 — Cross Platform Governance\nnames PD-02\n"})
            _corpus(root, "volume-2", "pd-02-y", {"A1": "A1 — Identity\n"})
            self.assertEqual(xpl.pairs(root)[("PD-01", "PD-02")],
                             xpl.SELF_DECLARED)

    def test_both_sides_stating_it_makes_it_reciprocated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _corpus(root, "volume-1", "pd-01-x",
                    {"C8": "C8 — Cross Platform Governance\nnames PD-02\n"})
            _corpus(root, "volume-2", "pd-02-y",
                    {"B7": "B7 — Organizational Interface\nnames PD-01\n"})
            self.assertEqual(xpl.pairs(root)[("PD-01", "PD-02")],
                             xpl.RECIPROCATED)

    def test_the_section_title_is_read_not_the_part_banner(self):
        """The defect this module committed on its first run.

        `PD-02`'s sections open with a Part banner and carry their own title on
        the next line. Taking the first line read `C8 — Cross-Platform
        Architecture Governance` as plain governance, and `PD-01 ↔ PD-02` came
        back weaker than both corpora state it.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _corpus(root, "volume-1", "pd-01-x",
                    {"C8": "C8 — Cross Platform Governance\nnames PD-02\n"})
            _corpus(root, "volume-2", "pd-02-y",
                    {"C8": "Part C — Governance Architecture\n"
                           "C8 — Cross-Platform Architecture Governance\n"
                           "names PD-01\n"})
            self.assertEqual(xpl.pairs(root)[("PD-01", "PD-02")],
                             xpl.RECIPROCATED)

    def test_residency_is_discovered_not_declared(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _corpus(root, "volume-9", "pd-07-z", {"A1": "A1 — Identity\n"})
            self.assertEqual(sorted(xpl.resident_corpora(root)), ["PD-07"])

    def test_no_resident_corpus_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(xpl.CorpusUnavailable):
                xpl.statements(Path(tmp))


class TheResidentReading(unittest.TestCase):
    def test_exactly_the_two_resident_volumes_are_found(self):
        self.assertEqual(xpl.summary()["resident_corpora"], ("PD-01", "PD-02"))

    def test_every_readable_pair_is_evidenced(self):
        """The finding: the gap is residency, not missing evidence."""
        summary = xpl.summary()
        readable = 2 * (len(xpl.DIVISIONS) - 1)
        self.assertEqual(summary["evidenced_pairs"], readable)
        self.assertEqual(summary["MENTIONED"], 0)

    def test_the_unreadable_pairs_are_exactly_the_eight_absent_divisions(self):
        summary = xpl.summary()
        self.assertEqual(len(summary["source_absent_divisions"]), 8)
        self.assertEqual(summary[xpl.SOURCE_ABSENT], 8 * 9)


if __name__ == "__main__":
    unittest.main()
