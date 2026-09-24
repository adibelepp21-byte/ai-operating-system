"""`FDR-1 §12` — the 100-question reconciliation holds, and can fail."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools import foundational_question_reconciliation as recon


class TheMatrixHoldsAgainstTheLiveTree(unittest.TestCase):

    def test_every_cited_pointer_holds(self):
        result = recon.verify()
        self.assertTrue(result["holds"], result["faults"])

    def test_it_covers_the_hundred_questions_once_each(self):
        result = recon.verify()
        self.assertEqual(sum(result["counts"].values()), 100)

    def test_the_source_is_recorded_as_non_resident_and_non_canonical(self):
        record = json.loads(recon.MATRIX.read_text(encoding="utf-8"))
        self.assertIs(record["source"]["canonical"], False)
        self.assertIn("NOT RESIDENT", record["source"]["residency"])
        self.assertIn("not a decision", record["authority"])


class EachPointerFormCanFail(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "pkg").mkdir()
        (self.root / "pkg/a.py").write_text("class Present:\n    pass\n",
                                            encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_text_pointers(self):
        self.assertTrue(recon.pointer_holds("pkg/a.py::class Present", self.root))
        self.assertFalse(recon.pointer_holds("pkg/a.py::class Absent", self.root))
        self.assertFalse(recon.pointer_holds("pkg/missing.py::x", self.root))

    def test_a_measured_absence_stops_holding_once_built(self):
        pointer = "!pkg::class Evaluation"
        self.assertTrue(recon.pointer_holds(pointer, self.root))
        (self.root / "pkg/b.py").write_text("class Evaluation:\n    pass\n",
                                            encoding="utf-8")
        self.assertFalse(recon.pointer_holds(pointer, self.root))

    def test_a_solved_claim_without_evidence_is_a_fault(self):
        matrix = self.root / "m.json"
        questions = [{"id": f"Q{i}", "category": "UNKNOWN", "evidence": []}
                     for i in range(1, 101)]
        questions[7] = {"id": "Q8", "category": "ALREADY SOLVED", "evidence": []}
        matrix.write_text(json.dumps({"questions": questions}), encoding="utf-8")
        faults = recon.verify(matrix, self.root)["faults"]
        self.assertTrue(any("Q8" in f and "cites no evidence" in f for f in faults))


if __name__ == "__main__":
    unittest.main()
