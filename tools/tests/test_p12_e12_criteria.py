"""`FD-P12-003 §19` — falsification of the decision-consumption chain.

Six controls, one class each. The instrument arrived with all ten of its
decision fields unfilled, so the live answer is `ACCEPTANCE BOUNDARY
UNAVAILABLE` — which is also what a reader that parsed nothing would print.
Every control therefore drives the reader against a **filled** instrument as
well, so `RESOLVED` is shown to be reachable and the refusal is a measurement
rather than a constant.

`§11`'s direction is the thing under test:

```text
FOUNDER SELECTS → ACCEPTANCE BOUNDARY → CLAUDE MEASURES        permitted
CLAUDE MEASURES → CLAUDE SELECTS → CLAUDE RATIFIES             prohibited
```
"""

from __future__ import annotations

import ast
import shutil
import tempfile
import unittest
from pathlib import Path

from tools import p12_e12_criteria as criteria

REPO_ROOT = Path(__file__).resolve().parents[2]

INSTRUMENT = (REPO_ROOT / criteria.DECISION_ROOT /
              "FD-P12-003-E12-01-05-MEASURABLE-INTERPRETATION.md")

SECTION = """
{number}. FOUNDER DECISION — {criterion}

Canonical Requirement

Read from the actual E12 decision package.

Founder Selection

Founder selects:

{criterion}
→ {selection}

Founder Decision: RATIFIED

Acceptance Boundary:

{boundary}

Claude Code is authorized to measure against this boundary.
"""


def _world(tmp: Path, *, sections: str) -> Path:
    """A repository world holding one instrument and the canonical package."""
    (tmp / criteria.DECISION_ROOT).mkdir(parents=True, exist_ok=True)
    (tmp / criteria.E12_PACKAGE).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(REPO_ROOT / criteria.E12_PACKAGE, tmp / criteria.E12_PACKAGE)
    (tmp / criteria.DECISION_ROOT / "FD.md").write_text(
        "FD-P12-003\n\nDecision Domain: E12-01 THROUGH E12-05\n" + sections,
        encoding="utf-8")
    return tmp


def _filled(selection_for=None, boundary="every material integration edge "
            "carries its ten attributes and is classified") -> str:
    """Five sections, each carrying its own proposed interpretation."""
    proposals = criteria.proposed_interpretations(REPO_ROOT)
    out = []
    for index, criterion in enumerate(criteria.CRITERIA, start=4):
        proposed = proposals[criterion]["proposed"]
        selection = (selection_for(criterion, proposed)
                     if selection_for else proposed)
        out.append(SECTION.format(number=index, criterion=criterion,
                                  selection=selection, boundary=boundary))
    return "\n".join(out)


class TheReaderMovesBothWays(unittest.TestCase):
    """Without this, five `UNRESOLVED` is a constant, not a measurement."""

    def test_a_filled_instrument_resolves_every_criterion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp), sections=_filled())
            found = criteria.summary(root)
            boundaries = criteria.boundaries(root)
        self.assertEqual(5, found["resolved"])
        self.assertTrue(found["measurable"])
        self.assertEqual(set(criteria.CRITERIA), set(boundaries))

    def test_the_live_instrument_resolves_nothing(self):
        found = criteria.summary()
        self.assertEqual(0, found["resolved"])
        self.assertEqual(5, found["unresolved"])
        self.assertFalse(found["measurable"])


class F01WrongInterpretation(unittest.TestCase):
    """An unselected interpretation must be **rejected**, not substituted."""

    def test_a_selection_that_is_not_the_proposed_one_is_rejected(self):
        def wrong(criterion, proposed):
            return ("dormancy is a legitimate operational state and the "
                    "surface need not be crossed by anything at all")
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp), sections=_filled(selection_for=wrong))
            found = criteria.decisions(root)
        self.assertEqual([criteria.REJECTED] * 5, [d.status for d in found])
        for decision in found:
            self.assertIn("does not correspond", decision.detail)

    def test_a_rejected_selection_yields_no_boundary(self):
        def wrong(criterion, proposed):
            return "some entirely unrelated wording nobody proposed"
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp), sections=_filled(selection_for=wrong))
            with self.assertRaises(criteria.AcceptanceBoundaryUnavailable):
                criteria.boundaries(root)


class F02MissingDecision(unittest.TestCase):
    """No decision record → `ACCEPTANCE BOUNDARY UNAVAILABLE`, never a default."""

    def test_an_absent_instrument_raises_rather_than_defaulting(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / criteria.DECISION_ROOT).mkdir(parents=True)
            with self.assertRaises(criteria.AcceptanceBoundaryUnavailable):
                criteria.boundaries(Path(tmp))

    def test_the_live_corpus_raises_today(self):
        """The instrument exists and is signed; its decisions do not."""
        with self.assertRaises(criteria.AcceptanceBoundaryUnavailable) as raised:
            criteria.boundaries()
        self.assertIn("5 of 5", str(raised.exception))

    def test_two_instruments_are_refused_rather_than_picked_between(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp), sections=_filled())
            shutil.copy(root / criteria.DECISION_ROOT / "FD.md",
                        root / criteria.DECISION_ROOT / "FD-second.md")
            found = criteria.decisions(root)
        self.assertTrue(all(d.status == criteria.UNRESOLVED for d in found))
        self.assertIn("Founder question", found[0].detail)


class F03ModifiedBoundary(unittest.TestCase):
    """A lower-level artifact must not be able to supply a boundary."""

    def test_only_the_curated_root_is_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / criteria.DECISION_ROOT).mkdir(parents=True)
            (root / criteria.E12_PACKAGE).parent.mkdir(parents=True)
            shutil.copy(REPO_ROOT / criteria.E12_PACKAGE,
                        root / criteria.E12_PACKAGE)
            # The same filled instrument, planted outside the curated root.
            planted = root / "docs" / "architecture" / "p12"
            planted.mkdir(parents=True, exist_ok=True)
            (planted / "looks-like-a-decision.md").write_text(
                _filled(), encoding="utf-8")
            with self.assertRaises(criteria.AcceptanceBoundaryUnavailable):
                criteria.boundaries(root)

    def test_the_boundary_comes_from_the_instrument_and_nowhere_else(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp),
                          sections=_filled(boundary="BOUNDARY-SENTINEL-VALUE"))
            boundaries = criteria.boundaries(root)
        for value in boundaries.values():
            self.assertIn("BOUNDARY-SENTINEL-VALUE", value)


class F04EvidenceWithoutAcceptance(unittest.TestCase):
    """Evidence while the boundary is unmet must read `NOT SATISFIED`."""

    def test_the_ratified_criterion_falls_when_its_boundary_is_unmet(self):
        """Exercised on `E12-06`, the one criterion that *has* a ratified
        boundary, because it is the only chain where acceptance can be tested
        at all. Evidence exists in quantity; with no crossing it still fails."""
        from unittest import mock
        from tools import p12_cross_phase_verification as cross
        from tools import p12_e12_acceptance as acceptance

        absent = tuple(
            cross.PhaseResult(phase=p, name=n, status=cross.NOT_EXERCISED,
                              evidence="nothing crossed it", locator="probe")
            for p, n in cross.CANONICAL_PHASES)
        with mock.patch.object(cross, "verify", return_value=absent), \
                mock.patch.object(cross, "summary", return_value={
                    "exercised_only_by_a_demonstrator": ()}):
            self.assertEqual(acceptance.NOT_SATISFIED,
                             acceptance.determination()["verdict"])

    def test_this_module_never_returns_a_result(self):
        """It returns boundaries. Acceptance is a measurement someone else
        makes against them — `OBSERVATION ≠ MEASUREMENT ≠ ACCEPTANCE`."""
        printed = str(criteria.summary()) + str(criteria.decisions())
        for forbidden in ("SATISFIED", "PASS", "COMPLETE", "CERTIFIED"):
            with self.subTest(forbidden):
                self.assertNotIn(forbidden, printed)


class F05AcceptanceWithoutEvidence(unittest.TestCase):
    """Satisfaction may not be declared without measurement evidence."""

    def test_a_resolved_boundary_is_not_a_satisfied_criterion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp), sections=_filled())
            found = criteria.summary(root)
        self.assertTrue(found["measurable"])
        # `measurable` says a measurement is now possible. It says nothing
        # about its result, and the module exposes no result to say it with.
        self.assertNotIn("satisfied", found)
        self.assertNotIn("result", found)

    def test_no_criterion_is_reported_satisfied_anywhere_in_this_module(self):
        source = (REPO_ROOT / "tools" / "p12_e12_criteria.py").read_text(
            encoding="utf-8")
        tree = ast.parse(source)
        literals = [n.value for n in ast.walk(tree)
                    if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        self.assertEqual([], [v for v in literals if v.strip() == "SATISFIED"])


class F06ClaudeSelfSelection(unittest.TestCase):
    """The implementation must not be able to select an interpretation."""

    SOURCE = REPO_ROOT / "tools" / "p12_e12_criteria.py"

    def test_the_module_carries_no_interpretation_of_its_own(self):
        """Every proposed interpretation lives in the canonical package. If any
        of their distinguishing phrases appeared as a literal here, the module
        could answer with one after the instrument was deleted."""
        source = self.SOURCE.read_text(encoding="utf-8")
        body = source.split('"""', 2)[-1]  # exclude the module docstring
        for criterion, proposal in criteria.proposed_interpretations().items():
            text = proposal["proposed"]
            self.assertTrue(text, f"{criterion} has no proposed text to check")
            for phrase in [p for p in text.split() if len(p) > 11][:4]:
                with self.subTest(criterion=criterion, phrase=phrase):
                    self.assertNotIn(phrase.strip("`*.,"), body)

    def test_no_function_selects_ratifies_or_defaults(self):
        tree = ast.parse(self.SOURCE.read_text(encoding="utf-8"))
        creating = [n.name for n in ast.walk(tree)
                    if isinstance(n, ast.FunctionDef)
                    and n.name.lower().lstrip("_").startswith(
                        ("select", "choose", "pick", "rank", "ratify",
                         "authorize", "authorise", "adopt", "default",
                         "resolve", "infer", "assume", "merge", "combine"))]
        self.assertEqual([], creating)

    def test_the_module_writes_nothing(self):
        source = self.SOURCE.read_text(encoding="utf-8")
        for forbidden in ("write_text(", "mkdir(", "unlink(", "open("):
            with self.subTest(forbidden):
                self.assertNotIn(forbidden, source)

    def test_the_sole_candidate_is_still_not_adopted(self):
        """The control that matters most.

        The canonical package proposes exactly one interpretation per
        criterion, so an "obvious" value exists for every unfilled bracket.
        The reader must still refuse — `ONE CANDIDATE ≠ A SELECTION`.
        """
        proposals = criteria.proposed_interpretations()
        # The package also proposes one for `E12-06`, which `FD-P12-001`
        # ratified separately; this surface covers the other five.
        self.assertTrue(set(criteria.CRITERIA) <= set(proposals))
        for criterion, proposal in proposals.items():
            with self.subTest(criterion):
                self.assertTrue(proposal["proposed"].strip())
        self.assertFalse(criteria.summary()["measurable"])


class TheLiveInstrumentIsRecordedAsReceived(unittest.TestCase):
    def test_it_is_persisted_in_the_curated_root(self):
        self.assertTrue(INSTRUMENT.is_file())

    def test_its_ten_decision_fields_are_still_unfilled(self):
        """`§14` — historical evidence is preserved. The instrument is stored
        exactly as issued, placeholders included, and is not repaired here."""
        # Count in the supplied artifact only. The persistence provenance
        # block above it quotes the placeholder shape twice, deliberately, to
        # show what was received.
        text = INSTRUMENT.read_text(encoding="utf-8")
        artifact = text.split("\nFD-P12-003 — FOUNDER DECISION", 1)[-1]
        self.assertEqual(10, artifact.count("[INSERT"))
        self.assertEqual(5, artifact.count(
            "[INSERT THE EXACT EXISTING PROPOSED INTERPRETATION"))
        self.assertEqual(5, artifact.count(
            "[INSERT THE EXACT ACCEPTANCE BOUNDARY CORRESPONDING"))

    def test_the_placeholder_recogniser_is_structural(self):
        for blank in ("[INSERT THE EXACT THING]", "[  ]", "____________",
                      "TBD", "", "   ", "E12-01 → [INSERT SOMETHING]"):
            with self.subTest(blank):
                self.assertTrue(criteria._is_placeholder(blank))
        for value in ("RATIFY AS PROPOSED", "R1 — consumption by real work"):
            with self.subTest(value):
                self.assertFalse(criteria._is_placeholder(value))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
