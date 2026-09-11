"""The persisted `E11` measurement must not be allowed to go quietly stale.

`docs/architecture/p11/e11-measurement.json` is the record a reader consults to
learn whether P11 currently satisfies the criteria `DP-02` ratified. **Nothing
verified that it still matched the repository.** A regression after it was
written would leave a file asserting `10/10 PASS` with no control able to
notice — the same shape as a W3 record naming a revoked grant, one layer up.

Found by `ACT-CC-P11-017`'s fresh discovery, not by a failing test.

**`E11-06` is deliberately excluded from the comparison.** Measuring it runs
`unittest discover` over all three suites as subprocesses, and one of those
suites is this one — a control that re-ran the suite containing it would recurse.
Its currency is instead guaranteed by the condition under which this test runs at
all: the suite is executing, so the suite exists and is being evaluated.

The root entry points are checked here too, and by **AST rather than import**.
`w4_first_execution.py`, `w1_coordination_proof.py` and
`cross_department_coordination_proof.py` wire `tools/` to `consumers/`, which is
precisely why no test in either region may import them — so nothing tested them
at all. Reading them is the strongest check available without breaking the
isolation that puts them at the repository root.
"""

from __future__ import annotations

import ast
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tools.e11_measurement import (  # noqa: E402
    CRITERIA, FAIL, PASS, e11_06_verification)

RECORD = REPO_ROOT / "docs/architecture/p11/e11-measurement.json"

#: Every entry point that wires the two isolated regions together. Discovered,
#: not listed: any root-level module importing both regions qualifies.
def _entry_points():
    found = []
    for path in sorted(REPO_ROOT.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
        modules = {n.module or "" for n in ast.walk(tree)
                   if isinstance(n, ast.ImportFrom)}
        if any(m.startswith("consumers") for m in modules) and \
                any(m.startswith("tools") for m in modules):
            found.append(path)
    return found


class ThePersistedMeasurementIsCurrent(unittest.TestCase):

    def setUp(self):
        self.assertTrue(RECORD.is_file(), RECORD)
        self.persisted = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_it_records_every_ratified_criterion_and_no_others(self):
        recorded = [r["criterion"] for r in self.persisted["results"]]
        declared = [c.__name__.split("_")[0].upper() + "-"
                    + c.__name__.split("_")[1] for c in CRITERIA]
        self.assertEqual(sorted(recorded), sorted(declared))
        self.assertEqual(10, len(recorded), recorded)

    def test_every_verdict_still_holds_when_re_measured(self):
        """The control that makes the file evidence rather than a snapshot."""
        by_key = {r["criterion"]: r["verdict"] for r in self.persisted["results"]}
        for criterion in CRITERIA:
            if criterion is e11_06_verification:
                continue                      # see module docstring
            result = criterion()
            with self.subTest(criterion=result.key):
                self.assertIn(result.verdict, (PASS, FAIL))
                self.assertEqual(by_key[result.key], result.verdict,
                                 f"{result.key}: persisted {by_key[result.key]!r}, "
                                 f"measured {result.verdict!r} — "
                                 f"{result.gap or 'no gap recorded'}")

    def test_the_summary_agrees_with_its_own_results(self):
        """A record whose summary disagreed with its rows would mislead a reader
        who read only the summary — which is how such a record is usually read."""
        results = self.persisted["results"]
        passed = sorted(r["criterion"] for r in results if r["verdict"] == PASS)
        failed = sorted(r["criterion"] for r in results if r["verdict"] == FAIL)
        self.assertEqual(sorted(self.persisted["passed"]), passed)
        self.assertEqual(sorted(self.persisted["failed"]), failed)
        self.assertEqual(self.persisted["e11_pass"], not failed)

    def test_it_names_the_decision_it_was_measured_against(self):
        self.assertEqual("DP-02", self.persisted["decision"])
        self.assertTrue((REPO_ROOT / self.persisted["decision_record"]).is_file())


class TheEntryPointsAreCheckedWithoutBeingImported(unittest.TestCase):

    def test_at_least_one_entry_point_exists(self):
        self.assertTrue(_entry_points(), "no region-joining entry point found")

    def test_each_parses_and_defines_a_main(self):
        for path in _entry_points():
            with self.subTest(entry=path.name):
                tree = ast.parse(path.read_text(encoding="utf-8"))
                names = {n.name for n in ast.walk(tree)
                         if isinstance(n, ast.FunctionDef)}
                self.assertIn("main", names)

    def test_each_names_symbols_that_still_exist_in_both_regions(self):
        """The break these files are most exposed to: a rename on either side.

        Nothing imports them, so a renamed export in `tools/` or `consumers/`
        would leave them broken until someone ran them by hand.
        """
        import importlib
        for path in _entry_points():
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.ImportFrom) or not node.module:
                    continue
                if not node.module.startswith(("tools", "consumers")):
                    continue
                module = importlib.import_module(node.module)
                for alias in node.names:
                    with self.subTest(entry=path.name,
                                      symbol=f"{node.module}.{alias.name}"):
                        self.assertTrue(hasattr(module, alias.name),
                                        f"{path.name} imports {alias.name!r} "
                                        f"from {node.module}, which no longer "
                                        "defines it")



class TheCriterionSetMatchesTheRatifiedDecision(unittest.TestCase):
    """The measuring instrument is checked against the Decision it measures.

    `CRITERIA` transcribes the ten criteria `DP-02` ratified, and **nothing
    compared it to the Decision body.** That is the shape `ACT-CC-P11-017` found
    one layer down, where two tuples transcribed `FD-P11-001 §13` and disagreed
    with each other and with the instrument — the conformance proof omitting
    `AUTHORITY PROVENANCE` while reporting *"13 of 13"*.

    An instrument free to measure a different set from the one ratified is an
    instrument that can report `PASS` against criteria nobody issued.
    """

    DECISION = (REPO_ROOT / "docs/governance/acts/"
                "DP-02-P11-E11-RATIFICATION.md")

    def _ratified_ids(self):
        import re
        body = self.DECISION.read_text(encoding="utf-8")
        start = body.index("5. NEGATIVE-CONTROL REQUIREMENT")
        end = body.index("6. EXPLICIT EXCLUSIONS", start)
        return sorted(set(re.findall(r"\bE11-\d\d\b", body[start:end])))

    def test_the_decision_still_enumerates_ten_criteria(self):
        ids = self._ratified_ids()
        self.assertEqual(10, len(ids), ids)
        self.assertIn("E11-09", ids)
        self.assertIn("E11-10", ids)

    def test_the_instrument_measures_exactly_what_was_ratified(self):
        measured = sorted(
            c.__name__.split("_")[0].upper() + "-" + c.__name__.split("_")[1]
            for c in CRITERIA)
        self.assertEqual(self._ratified_ids(), measured)

    def test_the_persisted_record_covers_exactly_what_was_ratified(self):
        persisted = sorted(r["criterion"] for r in json.loads(
            RECORD.read_text(encoding="utf-8"))["results"])
        self.assertEqual(self._ratified_ids(), persisted)


if __name__ == "__main__":
    unittest.main()
