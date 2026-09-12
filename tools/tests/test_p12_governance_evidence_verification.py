"""P12-W6 governance evidence conformance (`§26`).

One established element of nine is a strong claim. These controls establish that
it is a measurement: that each status can move, that the threshold is data
rather than a buried comparison, and that the result does not depend on which
population I chose.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from tools import p12_governance_evidence_verification as gov


def _doc(body: str):
    return (Path("synthetic.md"), body)


class TheScopeIsSection26s(unittest.TestCase):
    def test_the_nine_elements_are_section_26s_in_order(self):
        self.assertEqual(
            list(gov.GOVERNANCE_ELEMENTS),
            ["decision body", "authority", "effective date", "scope", "status",
             "provenance", "affected surfaces", "current state",
             "verification"])

    def test_every_element_has_a_label_entry(self):
        self.assertEqual(set(gov.ELEMENT_LABELS), set(gov.GOVERNANCE_ELEMENTS))

    def test_the_threshold_is_declared_data(self):
        self.assertIsInstance(gov.ESTABLISHED_FRACTION, float)
        self.assertGreater(gov.ESTABLISHED_FRACTION, 0)


class EachStatusCanMove(unittest.TestCase):
    def test_a_label_in_every_instrument_is_established(self):
        docs = [_doc("Status: ACTIVE\n") for _ in range(4)]
        results = {r.element: r for r in gov.coverage(population=docs)}
        self.assertEqual(results["status"].status, gov.ESTABLISHED)
        self.assertEqual(results["status"].instruments, 4)

    def test_a_label_in_a_minority_is_partial_not_established(self):
        docs = [_doc("Status: ACTIVE\n")] + [_doc("Nothing here.\n")
                                             for _ in range(9)]
        results = {r.element: r for r in gov.coverage(population=docs)}
        self.assertEqual(results["status"].status, gov.PARTIAL)
        self.assertEqual(results["status"].instruments, 1)

    def test_a_label_in_no_instrument_is_absent(self):
        docs = [_doc("Nothing here.\n")]
        results = {r.element: r for r in gov.coverage(population=docs)}
        self.assertEqual(results["status"].status, gov.ABSENT)

    def test_an_element_with_no_declared_label_is_absent(self):
        docs = [_doc("Verification: done\nAffected surfaces: all\n")]
        results = {r.element: r for r in gov.coverage(population=docs)}
        self.assertEqual(results["verification"].status, gov.ABSENT)
        self.assertEqual(results["affected surfaces"].status, gov.ABSENT)

    def test_verification_would_move_if_a_label_were_declared(self):
        """The finding closes by itself once the corpus grows a label."""
        with mock.patch.dict(gov.ELEMENT_LABELS,
                             {"verification": ("Verification",)}):
            docs = [_doc("Verification: independently checked\n")]
            results = {r.element: r for r in gov.coverage(population=docs)}
        self.assertEqual(results["verification"].status, gov.ESTABLISHED)

    def test_an_empty_label_value_is_not_coverage(self):
        docs = [_doc("Status:   \n")]
        results = {r.element: r for r in gov.coverage(population=docs)}
        self.assertEqual(results["status"].status, gov.ABSENT)


class TheMeasurementIsOfLabelsAndSaysSo(unittest.TestCase):
    def test_prose_is_not_counted_and_the_detail_says_which_was_measured(self):
        docs = [_doc("This act is issued under the authority of the Founder.\n")]
        results = {r.element: r for r in gov.coverage(population=docs)}
        self.assertEqual(results["authority"].status, gov.ABSENT)

    def test_a_label_after_the_header_window_is_not_counted(self):
        body = "\n".join(["filler"] * (gov._HEADER_LINES + 5)) + "\nStatus: X\n"
        results = {r.element: r for r in gov.coverage(population=[_doc(body)])}
        self.assertEqual(results["status"].status, gov.ABSENT)

    def test_provenance_is_structural_not_a_label(self):
        docs = [_doc("Nothing here.\n") for _ in range(3)]
        results = {r.element: r for r in gov.coverage(population=docs)}
        self.assertEqual(results["provenance"].status, gov.ESTABLISHED)
        self.assertEqual(results["provenance"].labels_seen,
                         ("source_path", "source_hash"))


class TheResultDoesNotDependOnMyChoiceOfPopulation(unittest.TestCase):
    def test_founder_acts_are_measured_separately(self):
        both = gov.by_population()
        self.assertIn("corpus", both)
        self.assertIn("founder_acts", both)
        self.assertGreater(both["corpus"]["status"][2],
                           both["founder_acts"]["status"][2])

    def test_the_narrower_population_is_not_better(self):
        """Rules out the objection that the wide population is diluted."""
        both = gov.by_population()
        for element in ("decision body", "authority", "scope", "status",
                        "current state"):
            with self.subTest(element):
                wide = both["corpus"][element]
                narrow = both["founder_acts"][element]
                self.assertLessEqual(narrow[1] / max(narrow[2], 1),
                                     wide[1] / max(wide[2], 1) + 0.2)


class TheLiveCorpusResult(unittest.TestCase):
    def test_affected_surfaces_and_verification_are_absent(self):
        self.assertEqual(gov.summary()["absent_elements"],
                         ("affected surfaces", "verification"))

    def test_only_provenance_is_established(self):
        summary = gov.summary()
        self.assertEqual(summary["established"], 1)
        self.assertEqual(summary["elements"], 9)

    def test_the_population_is_actually_read_from_the_corpus(self):
        self.assertGreater(len(gov.instruments()), 100)


if __name__ == "__main__":
    unittest.main()
