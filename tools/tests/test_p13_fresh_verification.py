"""`FDR-G2` `§6.3`: fresh verification before the Founder Closure Decision.

The live tree is verified read-only. Every control that breaks a state runs on
a disposable copy of the repository, and the real tree is compared before and
after.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from tools import certified_evidence_integrity as integrity
from tools import p12_certified_evidence_guard as sentinel
from tools import p13_fresh_verification as fresh

REPO_ROOT = Path(__file__).resolve().parents[2]
EXPECTED = ["V%02d" % n for n in range(1, 18)]


def _status(report: dict, identifier: str) -> str:
    (check,) = [c for c in report["checks"] if c["id"] == identifier]
    return check["status"]


def _tree(root: Path) -> dict:
    out = {}
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for name in files:
            path = Path(base) / name
            out[path.relative_to(root).as_posix()] = hashlib.sha256(
                path.read_bytes()).hexdigest()
    return out


class TheLiveVerification(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.report = fresh.verify()

    def test_every_state_named_in_6_3_is_checked_and_passes(self):
        self.assertEqual(EXPECTED, [c["id"] for c in self.report["checks"]])
        self.assertTrue(self.report["holds"],
                        [c for c in self.report["checks"] if c["status"] != fresh.PASS])

    def test_it_is_a_state_verification_not_a_live_proof(self):
        self.assertIn("not an E13-05 live proof", self.report["statement"])
        self.assertIn("closes nothing", self.report["statement"])

    def test_the_stated_closure_form_in_fdr_g2_is_not_a_grant(self):
        (check,) = [c for c in self.report["checks"] if c["id"] == "V16"]
        self.assertIn("unrecognised closure grants in Register-resolving instruments: []",
                      check["evidence"])
        self.assertTrue(any("FDR-G2" in e for e in check["evidence"]))

    def test_verification_writes_nothing_and_changes_no_state(self):
        before_tree, before_integrity = _tree(REPO_ROOT / "docs"), integrity.verify()
        fresh.verify()
        self.assertEqual(before_tree, _tree(REPO_ROOT / "docs"))
        self.assertEqual(before_integrity, integrity.verify())
        self.assertEqual(frozenset({10, 11, 12, 13}), sentinel.certified_phases())


class BrokenStateFails(unittest.TestCase):
    """On disposable copies of the repository."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name) / "repo"
        shutil.copytree(REPO_ROOT, self.repo,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.before = integrity.verify()

    def tearDown(self):
        self._tmp.cleanup()
        self.assertEqual(integrity.verify(), self.before, "a control changed the real tree")

    def _edit(self, relative: str, old: str, new: str) -> None:
        path = self.repo / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def _register(self, line: str) -> None:
        with (self.repo / fresh.REGISTER).open("a", encoding="utf-8") as register:
            register.write(f"\n{line}\n")

    def test_the_copy_holds(self):
        report = fresh.verify(self.repo)
        self.assertTrue(report["holds"],
                        [c for c in report["checks"] if c["status"] != fresh.PASS])

    def test_a_registered_closure_grant_fails_v16(self):
        (self.repo / fresh.ACTS / "FDR-99-TEST-P13-CLOSURE.md").write_text(
            "# test\n\nP13 CLOSURE = GRANTED\n", encoding="utf-8")
        self._register("| FDR-99 | test closure |")
        self.assertEqual(fresh.FAIL, _status(fresh.verify(self.repo), "V16"))

    def test_an_unregistered_closure_line_is_not_read(self):
        (self.repo / fresh.ACTS / "FDR-99-TEST-P13-CLOSURE.md").write_text(
            "# test\n\nP13 CLOSURE = GRANTED\n", encoding="utf-8")
        self.assertEqual(fresh.PASS, _status(fresh.verify(self.repo), "V16"))

    def test_fdr_g2_without_its_disclaimer_is_read_as_a_grant(self):
        """The stated-form reading holds only while the instrument says so."""
        self._edit(fresh.ACTS + "/" + next(iter(fresh.STATED_FORM)),
                   "FDR-G2 does not itself close P13.", "(removed)")
        self.assertEqual(fresh.FAIL, _status(fresh.verify(self.repo), "V16"))

    def test_a_phase_14_row_fails_v14(self):
        path = self.repo / fresh.ROADMAP
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        (index,) = [i for i, line in enumerate(lines) if line.startswith("| 13 |")]
        lines.insert(index + 1, "| 14 | Test | test | P13 | test |\n")
        path.write_text("".join(lines), encoding="utf-8")
        self.assertEqual(fresh.FAIL, _status(fresh.verify(self.repo), "V14"))

    def test_an_unretired_env_02_fails_v07(self):
        path = self.repo / "docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md"
        text = path.read_text(encoding="utf-8")
        cut = text.index("## 16. P13-ENV-02 Retirement Append")
        path.write_text(text[:cut], encoding="utf-8")
        self.assertNotEqual(fresh.PASS, _status(fresh.verify(self.repo), "V07"))

    def test_a_changed_certified_byte_fails_v09(self):
        blueprint = self.repo / "docs/architecture/p13/AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md"
        blueprint.write_text(blueprint.read_text(encoding="utf-8") + "edit\n",
                             encoding="utf-8")
        self.assertEqual(fresh.FAIL, _status(fresh.verify(self.repo), "V09"))

    def test_residual_drift_fails_v11(self):
        path = self.repo / "docs/architecture/p13-preparation/" \
                           "P13-015-FOUNDATIONAL-QUESTION-RECONCILIATION.json"
        matrix = json.loads(path.read_text(encoding="utf-8"))
        (row,) = [r for r in matrix["questions"] if r["id"] == "Q23"]
        row["category"] = "P13 FRONTIER"
        path.write_text(json.dumps(matrix), encoding="utf-8")
        self.assertEqual(fresh.FAIL, _status(fresh.verify(self.repo), "V11"))

    def test_without_the_a17_determination_v04_and_v05_fail(self):
        self._edit(fresh.REGISTER, "| **A17 determination** |", "| **A17 (removed)** |")
        report = fresh.verify(self.repo)
        self.assertEqual(fresh.FAIL, _status(report, "V04"))
        self.assertEqual(fresh.FAIL, _status(report, "V05"))

    def test_an_unregistered_certification_elsewhere_fails_v15(self):
        (self.repo / fresh.ACTS / "FD-P5-999-TEST.md").write_text(
            "FOUNDER DECISION: CERTIFY P5.\n", encoding="utf-8")
        self._register("| FD-P5-999 | test |")
        self.assertEqual(fresh.FAIL, _status(fresh.verify(self.repo), "V15"))

    def test_a_second_certification_of_p13_fails_v03_and_v15(self):
        """The certified set is unchanged, but an unauthorized certifying
        instrument appears in the provenance."""
        (self.repo / fresh.ACTS / "FDR-98-TEST-P13-RECERTIFICATION.md").write_text(
            "FOUNDER DECISION: CERTIFY P13.\n", encoding="utf-8")
        self._register("| FDR-98 | test |")
        report = fresh.verify(self.repo)
        self.assertEqual(fresh.FAIL, _status(report, "V03"))
        self.assertEqual(fresh.FAIL, _status(report, "V15"))

    def test_env_02_without_its_retirement_record_fails_v07(self):
        """Not active is not the same as retired: the retirement must be on
        record."""
        (self.repo / "docs/governance/p13-envelopes/P13-ENV-02.json").unlink()
        path = self.repo / "docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(text[:text.index("## 16. P13-ENV-02 Retirement Append")],
                        encoding="utf-8")
        self.assertEqual(fresh.FAIL, _status(fresh.verify(self.repo), "V07"))

    def test_an_unreadable_register_does_not_hold(self):
        (self.repo / fresh.REGISTER).unlink()
        report = fresh.verify(self.repo)
        self.assertFalse(report["holds"])
        self.assertIn("UNDETERMINABLE", report["statement"])


if __name__ == "__main__":
    unittest.main()
