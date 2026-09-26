"""Tests for the Volume 3 / Volume 4 identity and inventory (ACT-004 §7, §9, NC-03, NC-04)."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from tools import platform_volume_inventory as inv

REPO_ROOT = Path(__file__).resolve().parents[2]


class TheResidentVolumes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.report = inv.report()

    def test_identity_is_read_from_the_bodies(self):
        pd03 = self.report["PD-03"]["identity"]
        self.assertEqual(("PD-03", "Governance & Compliance", "Governance Authority", "1.0", "FROZEN"),
                         (pd03["Platform ID"], pd03["Platform Name"], pd03["Platform Authority"],
                          pd03["Version"], pd03["Status"]))
        pd04 = self.report["PD-04"]["identity"]
        self.assertEqual(("PD-04", "Knowledge & Intelligence", "Knowledge Authority", "FROZEN"),
                         (pd04["Platform ID"], pd04["Official Name"], pd04["Platform Authority"],
                          pd04["Status"]))

    def test_an_undeclared_version_is_not_supplied(self):
        self.assertNotIn("Version", self.report["PD-04"]["identity"])

    def test_structure_is_as_present_not_normalised(self):
        """NC-04: Volume 4 is A–C; no A–H is imposed on it."""
        self.assertEqual(list("ABCDEFGH"), self.report["PD-03"]["parts"])
        self.assertEqual(list("ABC"), self.report["PD-04"]["parts"])

    def test_every_section_identity_is_present(self):
        self.assertEqual((80, []), (self.report["PD-03"]["section_identities"],
                                    self.report["PD-03"]["missing"]))
        self.assertEqual((30, []), (self.report["PD-04"]["section_identities"],
                                    self.report["PD-04"]["missing"]))

    def test_part_b_of_volume_3_declares_its_source_gate(self):
        """E-22, from the body: B2 onward NOT FROZEN — SOURCE GATE BLOCKED."""
        statuses = self.report["PD-03"]["inventory"]["B"]["declared_statuses"]
        self.assertIn("NOT FROZEN — SOURCE GATE BLOCKED", statuses)


class MissingIsReportedNotFilled(unittest.TestCase):
    """§5: a missing section stays missing."""

    def test_a_missing_section_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "Volume_9_Part_A.md").write_text(
                "> **Platform ID:** PD-09\n\n# A1 — Identity\n\n# A2 — Purpose\n", encoding="utf-8")
            parts = inv.inventory(directory)
        self.assertEqual(["A1", "A2"], parts["A"]["sections_present"])
        self.assertEqual([f"A{n}" for n in range(3, 11)], parts["A"]["sections_missing"])

    def test_identity_ignores_the_file_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "Volume_3_Part_A.md").write_text("# A1 — Identity\n", encoding="utf-8")
            self.assertEqual({}, inv.identity(directory))


if __name__ == "__main__":
    unittest.main()
