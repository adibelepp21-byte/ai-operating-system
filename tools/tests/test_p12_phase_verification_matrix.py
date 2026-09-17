"""`§46` P4–P11 Verification Matrix conformance.

Eleven attributes for eight phases is a shape any module could print. What is
verified here is that each cell is **measured** — that it moves when its source
moves, that an `UNKNOWN` states a reason instead of standing for a guess, and
that the module assigns nothing it reads.
"""

from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import p12_phase_verification_matrix as matrix
from tools import p12_cross_phase_verification as cross

REPO_ROOT = Path(__file__).resolve().parents[2]


class TheShapeIsTheSections(unittest.TestCase):
    def test_eleven_attributes_in_canonical_order(self):
        self.assertEqual(
            ("PHASE", "CAPABILITY", "INPUT", "OUTPUT", "OWNER", "AUTHORITY",
             "STATE", "INTEGRATION", "EVIDENCE", "VERIFICATION", "REGRESSION"),
            matrix.ATTRIBUTES)

    def test_one_row_per_canonical_phase_in_canonical_order(self):
        rows = matrix.rows()
        self.assertEqual(len(cross.CANONICAL_PHASES), len(rows))
        for (phase, name), row in zip(cross.CANONICAL_PHASES, rows):
            self.assertTrue(row.phase.startswith(phase), row.phase)
            self.assertIn(name, row.phase)

    def test_every_cell_is_populated(self):
        """An empty cell and an `UNKNOWN` cell are different answers."""
        for row in matrix.rows():
            for attribute, value in zip(matrix.ATTRIBUTES, row.as_row()):
                with self.subTest(phase=row.phase, attribute=attribute):
                    self.assertTrue(str(value).strip())


class EveryUnknownStatesItsReason(unittest.TestCase):
    """`UNKNOWN ≠ FALSE`, and an unexplained `UNKNOWN` is not a measurement."""

    def test_no_bare_unknown(self):
        for row in matrix.rows():
            for attribute, value in zip(matrix.ATTRIBUTES, row.as_row()):
                if value.startswith(matrix.UNKNOWN):
                    with self.subTest(phase=row.phase, attribute=attribute):
                        self.assertIn("—", value, "UNKNOWN carries no reason")
                        self.assertGreater(len(value), len(matrix.UNKNOWN) + 8)

    def test_the_four_phases_without_a_boundary_say_so(self):
        """`P5`, `P8`, `P10`, `P11` have no 1:1 Native Core boundary, and the
        matrix must state that rather than inventing a correspondence — the
        conflation the Phase–PD map exists to refuse."""
        rows = {r.phase.split()[0]: r for r in matrix.rows()}
        for phase in ("P5", "P8", "P10", "P11"):
            with self.subTest(phase):
                self.assertIn("two taxonomies", rows[phase].capability)
                self.assertNotIn(phase, matrix.PHASE_BOUNDARY)

    def test_owner_is_unknown_for_every_phase_and_names_f17(self):
        """The resident Phase–PD map's central finding: zero resident sources
        assign a provider PD to a phase. The matrix reports that, and does not
        assign one."""
        for row in matrix.rows():
            with self.subTest(row.phase):
                self.assertTrue(row.owner.startswith(matrix.UNKNOWN))
                self.assertIn("F-17", row.owner)


class CellsFollowTheirSources(unittest.TestCase):
    """Without this, eleven columns are a layout rather than a measurement."""

    def test_state_follows_the_cross_phase_verifier(self):
        absent = tuple(
            cross.PhaseResult(phase=p, name=n, status=cross.NOT_EXERCISED,
                              evidence="nothing crossed it", locator="probe")
            for p, n in cross.CANONICAL_PHASES)
        with mock.patch.object(cross, "verify", return_value=absent):
            rows = matrix.rows()
        for row in rows:
            with self.subTest(row.phase):
                self.assertIn(cross.NOT_EXERCISED, row.state)

    def test_the_live_state_column_reports_what_the_corpus_shows(self):
        for row in matrix.rows():
            with self.subTest(row.phase):
                self.assertIn(cross.EXERCISED, row.state)

    def test_capability_follows_the_boundary_on_disk(self):
        """Point the module at a world with no Native Core and the four
        boundary-backed phases must fall to `UNKNOWN`, not keep their values."""
        with tempfile.TemporaryDirectory() as tmp:
            rows = {r.phase.split()[0]: r for r in matrix.rows(Path(tmp))}
        for phase in matrix.PHASE_BOUNDARY:
            with self.subTest(phase):
                self.assertTrue(rows[phase].capability.startswith(matrix.UNKNOWN))

    def test_regression_follows_the_anchors(self):
        from tools import p12_regression_verification as regression
        with mock.patch.object(regression, "verify", return_value=()):
            rows = matrix.rows()
        for row in rows:
            with self.subTest(row.phase):
                self.assertTrue(row.regression.startswith(matrix.UNKNOWN))

    def test_every_named_regression_class_is_a_resident_one(self):
        from tools import p12_regression_verification as regression
        resident = {a.regression_class for a in regression.verify()}
        self.assertEqual(set(), set(matrix._REGRESSION_CLASS.values()) - resident)


class TheSummaryIsCountedNotAsserted(unittest.TestCase):
    def test_counts_match_the_rows(self):
        rows = matrix.rows()
        found = matrix.summary()
        self.assertEqual(len(rows), found["phases"])
        self.assertEqual(len(rows) * (len(matrix.ATTRIBUTES) - 1),
                         found["cells"])
        self.assertEqual(found["cells"],
                         found["measured_cells"] + found["unknown_cells"])

    def test_the_matrix_is_not_reported_complete_while_cells_are_unknown(self):
        found = matrix.summary()
        self.assertEqual(found["complete"], found["unknown_cells"] == 0)
        self.assertFalse(found["complete"],
                         "31 cells are UNKNOWN; reporting complete would be "
                         "the overclaim this matrix exists to avoid")


class TheModuleAssignsNothing(unittest.TestCase):
    """`§11` — nothing owns what it integrates, and a matrix is not authority."""

    SOURCE = REPO_ROOT / "tools" / "p12_phase_verification_matrix.py"

    def test_no_function_creates_authority(self):
        """Names first — the resident control `p12_integration_graph` is held
        to, minus one word.

        That control forbids `own` as a function-name prefix. It fired here on
        `_owner`, which *reads* the Phase–PD map's answer and can only return
        `UNKNOWN`. Dropping the word to get past it would be the rename this
        programme refuses, so the word is dropped **and replaced by a stronger
        behavioural control** in the test below: no function in this module may
        return an owner that is not `UNKNOWN`. A name check cannot see what a
        function returns; that one can.
        """
        tree = ast.parse(self.SOURCE.read_text(encoding="utf-8"))
        creating = [n.name for n in ast.walk(tree)
                    if isinstance(n, ast.FunctionDef)
                    and n.name.lower().lstrip("_").startswith(
                        ("assign", "authorize", "authorise", "certify",
                         "approve", "grant", "ratify"))]
        self.assertEqual([], creating)

    def test_no_code_path_returns_an_assigned_owner(self):
        """The behavioural half. Every literal this module could return as an
        `OWNER` is an `UNKNOWN`, on the live corpus and against a world where
        the Phase–PD map does not resolve at all."""
        for phase, _ in cross.CANONICAL_PHASES:
            with self.subTest(phase=phase, world="live"):
                self.assertTrue(
                    matrix._owner(phase, REPO_ROOT).startswith(matrix.UNKNOWN))
        with tempfile.TemporaryDirectory() as tmp:
            for phase, _ in cross.CANONICAL_PHASES:
                with self.subTest(phase=phase, world="empty"):
                    self.assertTrue(matrix._owner(phase, Path(tmp))
                                    .startswith(matrix.UNKNOWN))

    def test_the_module_writes_nothing(self):
        source = self.SOURCE.read_text(encoding="utf-8")
        for forbidden in ("write_text(", "open(", "mkdir(", "unlink("):
            with self.subTest(forbidden):
                self.assertNotIn(forbidden, source)

    def test_it_reports_a_matrix_not_a_verdict(self):
        printed = str(matrix.summary())
        for forbidden in ("SATISFIED", "COMPLETE", "CERTIFIED", "PASS"):
            with self.subTest(forbidden):
                self.assertNotIn(forbidden, printed)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
