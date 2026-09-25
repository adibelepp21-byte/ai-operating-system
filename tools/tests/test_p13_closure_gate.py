"""`FDR-G1` `§33`: the P13 closure gate evaluates and never closes.

The live tree is evaluated read-only. Every control that removes evidence runs
on a disposable copy of the repository, and the real tree is compared before
and after.
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
from tools import p13_closure_gate as gate

REPO_ROOT = Path(__file__).resolve().parents[2]


def _tree(root: Path) -> dict:
    """Every file under `root` and its sha256, so a write anywhere shows."""
    out = {}
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for name in files:
            path = Path(base) / name
            out[path.relative_to(root).as_posix()] = hashlib.sha256(
                path.read_bytes()).hexdigest()
    return out


def _status(report: dict, number: int) -> str:
    return report["criteria"][number - 1]["status"]


class TheLiveGate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.report = gate.evaluate()

    def test_it_evaluates_the_eight_founder_criteria_in_order(self):
        self.assertEqual(list(gate.CRITERIA),
                         [c["criterion"] for c in self.report["criteria"]])
        self.assertEqual(8, len(self.report["criteria"]))

    def test_it_is_not_satisfied_and_closes_nothing(self):
        self.assertEqual(gate.NOT_SATISFIED, self.report["gate"])
        self.assertIs(False, self.report["closes"])
        self.assertNotIn("CLOSED", json.dumps(self.report).replace("NOT CLOSED", ""))

    def test_what_the_record_answers_is_evidenced(self):
        for number in (1, 2, 3, 4, 7):
            with self.subTest(f"C{number}"):
                self.assertEqual(gate.EVIDENCED, _status(self.report, number))

    def test_what_the_record_leaves_open_is_the_founders(self):
        for number in (5, 6, 8):
            with self.subTest(f"C{number}"):
                self.assertEqual(gate.FOUNDER, _status(self.report, number))

    def test_the_open_escalations_are_listed_not_judged(self):
        evidence = " ".join(self.report["criteria"][4]["evidence"])
        for escalation in ("0991300404cf44d8", "23f315ba9f504272",
                           "9cb90fa0787a478c", "9d6bc0ad47294ef0"):
            self.assertIn(escalation, evidence)

    def test_evaluation_writes_nothing_and_changes_no_certification(self):
        before_tree = _tree(REPO_ROOT / "docs")
        before_integrity = integrity.verify()
        gate.evaluate()
        self.assertEqual(before_tree, _tree(REPO_ROOT / "docs"))
        self.assertEqual(before_integrity, integrity.verify())
        self.assertEqual(frozenset({10, 11, 12, 13}), sentinel.certified_phases())


class ASatisfiedGateIsStillNotAClosure(unittest.TestCase):

    def test_every_item_evidenced_still_closes_nothing(self):
        items = [gate._item(n, gate.EVIDENCED, ["test"])
                 for n in range(1, len(gate.CRITERIA) + 1)]
        report = gate._report(items)
        self.assertEqual(gate.SATISFIED, report["gate"])
        self.assertIs(False, report["closes"])
        self.assertIn("A satisfied gate is not a closure", report["statement"])

    def test_one_founder_item_leaves_the_gate_unsatisfied(self):
        items = [gate._item(n, gate.EVIDENCED, ["test"])
                 for n in range(1, len(gate.CRITERIA))]
        items.append(gate._item(len(gate.CRITERIA), gate.FOUNDER, []))
        self.assertEqual(gate.NOT_SATISFIED, gate._report(items)["gate"])


class RemovedEvidenceIsNotEvidenced(unittest.TestCase):
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

    def test_the_copy_evaluates_like_the_live_tree(self):
        self.assertEqual([c["status"] for c in gate.evaluate()["criteria"]],
                         [c["status"] for c in gate.evaluate(self.repo)["criteria"]])

    def test_without_the_exit_decision_c1_is_not_evidenced(self):
        (self.repo / gate.FDR5).unlink()
        self.assertEqual(gate.NOT_EVIDENCED, _status(gate.evaluate(self.repo), 1))

    def test_without_the_frontier_acceptance_c3_is_not_evidenced(self):
        self._edit(gate.FDR7, "FDQ-7.7 = ACCEPT AS CLASSIFIED / NON-BLOCKING",
                   "FDQ-7.7 = (removed)")
        self.assertEqual(gate.NOT_EVIDENCED, _status(gate.evaluate(self.repo), 3))

    def test_an_unregistered_foundation_decision_evidences_nothing(self):
        """An instrument the Register does not resolve is not read."""
        self._edit(gate.REGISTER, "FDR-G1", "FDR-XX")
        report = gate.evaluate(self.repo)
        self.assertEqual(gate.NOT_EVIDENCED, _status(report, 7))
        self.assertEqual(gate.NOT_EVIDENCED, _status(report, 2))

    def test_an_unreadable_register_is_undeterminable(self):
        (self.repo / gate.REGISTER).unlink()
        report = gate.evaluate(self.repo)
        self.assertEqual({gate.UNDETERMINABLE},
                         {c["status"] for c in report["criteria"]})
        self.assertEqual(gate.NOT_SATISFIED, report["gate"])

    def test_founder_items_never_become_evidenced(self):
        """Nothing in the record can turn a Founder judgement into evidence,
        not even a closure line planted in a registered act."""
        with (self.repo / gate.FDRG1).open("a", encoding="utf-8") as act:
            act.write("\nP13 CLOSED\nFOUNDER DECISION: CLOSE P13.\n")
        report = gate.evaluate(self.repo)
        for number in (5, 6, 8):
            with self.subTest(f"C{number}"):
                self.assertEqual(gate.FOUNDER, _status(report, number))
        self.assertIs(False, report["closes"])

    def test_without_the_registered_a17_determination_c2_is_not_evidenced(self):
        """`GOV-002` `§5`: an authorization record in force is not remaining
        work. The exhaustion has to be a registered determination."""
        self._edit(gate.REGISTER, "| **A17 determination** |", "| **A17 (removed)** |")
        self.assertEqual(gate.NOT_EVIDENCED, _status(gate.evaluate(self.repo), 2))

    def test_a_mention_of_exhaustion_in_prose_does_not_count(self):
        self._edit(gate.REGISTER, "| **A17 determination** |", "| **A17 (removed)** |")
        with (self.repo / gate.REGISTER).open("a", encoding="utf-8") as register:
            register.write(f"\nThe gate looks for {gate.EXHAUSTION}.\n")
        self.assertEqual(gate.NOT_EVIDENCED, _status(gate.evaluate(self.repo), 2))

    def test_without_the_retention_in_fdr_7_c4_is_not_evidenced(self):
        self._edit(gate.FDR7, gate.RETAINED, "(retention removed)")
        self.assertEqual(gate.NOT_EVIDENCED, _status(gate.evaluate(self.repo), 4))


if __name__ == "__main__":
    unittest.main()
