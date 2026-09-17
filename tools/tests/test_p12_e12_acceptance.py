"""`ACT-CC-P12-013 §20` — falsification for the ratified `E12-06` measurement.

Seven mandatory controls, one class each. `§20` closes: *"A successful
falsification must not be hidden merely because it prevents completion."*

The live measurement reported `NOT SATISFIED` when this suite was written, so
the controls proved the module **could** report `SATISFIED`. It now reports
`SATISFIED`, and the risk has inverted with it: a module returning a constant
`SATISFIED` would pass every live reading here. So each control that used to
lean on an un-crossed phase now drives the refusal directly — on evidence with
no crossing, and on evidence carrying only a demonstrator — while ratification
is held constant. `R1`, `R2 = NOT SELECTED` and `R3 = NOT SELECTED` are read
from the same instrument throughout; what moved between `4 of 8`, `7 of 8` and
`8 of 8` was the evidence, and these controls exist to keep that true.

`F-06` and `F-07` are the two that matter most, because they guard the step from
a ratified boundary to a claimed pass — the shortcut `§11` names explicitly:

```text
E12 RATIFIED  →  PART J PASS        ← prohibited
```
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import p12_e12_acceptance as acc
from tools import p12_cross_phase_verification as cross

REPO_ROOT = Path(__file__).resolve().parents[2]

ISSUED = """
## 5. §C ACCEPTANCE INTERPRETATION

FOUNDER SELECTION

{reading}

The existence of a component, provisioned capability, demonstrator, test
fixture, or merely callable surface is not by itself sufficient evidence of
consumption by real system work.

## 6. NON-SELECTION OF ALTERNATIVE INTERPRETATIONS

R2 — PROVISIONING BY REAL EXECUTION = NOT SELECTED
R3 — DORMANCY AS A LEGITIMATE OPERATIONAL STATE = NOT SELECTED

## 23. FOUNDER AUTHENTICATION

Decision Status: FINAL / ISSUED
"""


def _world(body: str = None, *, name: str = "decision.md",
           status: str = "Decision Status: FINAL / ISSUED"):
    tmp = tempfile.TemporaryDirectory()
    acts = Path(tmp.name) / "docs" / "governance" / "acts"
    acts.mkdir(parents=True)
    text = body if body is not None else ISSUED.format(
        reading="R1 — CONSUMPTION BY REAL SYSTEM WORK")
    (acts / name).write_text(text.replace(
        "Decision Status: FINAL / ISSUED", status), encoding="utf-8")
    return tmp


def _result(phase, name, status, evidence):
    return cross.PhaseResult(phase=phase, name=name, status=status,
                             evidence=evidence, locator="fixture")


class F01FalseConsumptionClaim(unittest.TestCase):
    """A phase must not be reported consumed without evidence of consumption."""

    def test_a_phase_with_no_execution_is_not_consumed(self):
        """The rule, not the corpus.

        No live phase is un-crossed any more, so reading the live corpus here
        would pass for a module that reported `CONSUMED` unconditionally. The
        refusal is driven on synthetic evidence instead.
        """
        absent = (_result("P4", "Runtime", cross.NOT_EXERCISED,
                          "no Trace record names a runtime"),)
        with mock.patch.object(cross, "verify", return_value=absent), \
                mock.patch.object(cross, "summary", return_value={
                    "exercised_only_by_a_demonstrator": ()}):
            found = acc.determination()
        self.assertEqual(["P4"], sorted(found["not_consumed"]))
        self.assertEqual(["P4"],
                         sorted(found["by_reason"]["no execution ever recorded"]))

    def test_the_verdict_names_which_phases_failed_and_why(self):
        """Pinned exactly. `ACT-CC-P12-014` moved `P4`, `P7` and `P9` into
        consumption by building a real work path; `FD-P12-002` authorized the
        Knowledge admission and the work then consumed the admitted version,
        which moved `P6`. Pinned to the whole result rather than relaxed — a
        phase regressing, or one passing on demonstrator evidence, still fails
        here."""
        found = acc.determination()
        self.assertEqual([], sorted(found["not_consumed"]))
        reasons = found["by_reason"]
        self.assertEqual([], sorted(reasons["no execution ever recorded"]))
        self.assertEqual([], sorted(reasons["demonstrator only"]))
        self.assertEqual(8, len(found["consumed_by_real_work"]))


class F02ProvisionedButNotConsumed(unittest.TestCase):
    """`§6` — `R2` is NOT SELECTED, so provisioning must not satisfy `R1`."""

    def test_provisioning_is_not_accepted_as_consumption(self):
        """`P6` was provisioned by every real runtime — the work reached
        `execution.runtime.knowledge` on a RUNNING Runtime — and consumed by no
        execution, because nothing Active existed to read. Under `R2` that
        would have passed; under the ratified `R1` it did not, and `P6` only
        moved once an admitted version was actually read.

        The rule outlives the state: a phase whose evidence shows provisioning
        but no crossing must still be refused, so it is driven synthetically.
        """
        provisioned = (_result("P6", "Knowledge", cross.NOT_EXERCISED,
                               "knowledge_consumed is empty in every Trace "
                               "record"),)
        with mock.patch.object(cross, "verify", return_value=provisioned), \
                mock.patch.object(cross, "summary", return_value={
                    "exercised_only_by_a_demonstrator": ()}):
            found = {r.phase: r for r in acc.phases()}
        self.assertFalse(found["P6"].accepted)
        self.assertEqual(acc.NOT_EXERCISED_AT_ALL, found["P6"].verdict)

    def test_r2_and_r3_are_recorded_as_not_selected(self):
        self.assertEqual(("R2", "R3"), acc.ratified_boundary().not_selected)

    def test_the_module_refuses_a_reading_it_does_not_implement(self):
        """Combining or substituting a reading is forbidden by `§6`/`§9`."""
        tmp = _world(ISSUED.format(reading="R2 — PROVISIONING BY REAL EXECUTION"))
        self.addCleanup(tmp.cleanup)
        with self.assertRaises(acc.AcceptanceBoundaryUnresolved) as raised:
            acc.phases(Path(tmp.name))
        self.assertIn("R1 only", str(raised.exception))


class F03DemonstratorButNotRealSystemWork(unittest.TestCase):
    """`§5` — a demonstrator is not by itself sufficient."""

    def test_no_phase_is_demonstrator_only_on_the_live_corpus(self):
        """`P4` and `P9` were, until `ACT-CC-P12-014` gave both a real-work
        crossing. Pinned, so a regression still fails here."""
        self.assertEqual([], [r.phase for r in acc.phases()
                              if r.verdict == acc.DEMONSTRATOR_ONLY])

    def test_a_demonstrator_only_crossing_is_still_refused(self):
        """The rule, not the corpus. Driven on synthetic evidence so the
        refusal is proved rather than assumed from an empty list."""
        mixed = (
            _result("P4", "Runtime", cross.EXERCISED, "'p12-f4-runtime-observation'"),
            _result("P5", "Intelligence", cross.EXERCISED,
                    "authored by engineering-intelligence-instance-001"))
        with mock.patch.object(cross, "verify", return_value=mixed), \
                mock.patch.object(cross, "summary", return_value={
                    "exercised_only_by_a_demonstrator": ("P4",)}):
            found = {r.phase: r for r in acc.phases()}
        self.assertFalse(found["P4"].accepted)
        self.assertEqual(acc.DEMONSTRATOR_ONLY, found["P4"].verdict)

    def test_consumption_rose_because_work_was_built_not_because_r1_relaxed(self):
        """`R1` is unchanged; the corpus is not.

        All eight phases are crossed by real work. The boundary that produced
        `4 of 8`, then `7 of 8`, then this is the same one — read from the same
        instrument, with `R2` and `R3` still NOT SELECTED and a demonstrator
        still insufficient. What moved was the evidence.
        """
        boundary = acc.ratified_boundary()
        self.assertTrue(boundary.reading.startswith("R1"))
        self.assertEqual(("R2", "R3"), boundary.not_selected)
        self.assertTrue(boundary.demonstrator_insufficient)
        self.assertEqual(8, cross.summary()["exercised"])
        self.assertEqual(8, len(acc.determination()["consumed_by_real_work"]))
        self.assertEqual(acc.SATISFIED, acc.determination()["verdict"])

    def test_the_boundary_records_that_demonstrators_are_insufficient(self):
        self.assertTrue(acc.ratified_boundary().demonstrator_insufficient)


class F04StaleEvidence(unittest.TestCase):
    """The determination must follow the corpus, not a cached figure."""

    def test_the_verdict_moves_when_the_evidence_moves(self):
        """Driven both ways on synthetic phase results — this is what proves
        `NOT SATISFIED` is measured rather than constant."""
        all_real = tuple(
            _result(p, p, cross.EXERCISED, "authored by engineering-intelligence-instance-001")
            for p in ("P4", "P5"))
        with mock.patch.object(cross, "verify", return_value=all_real), \
                mock.patch.object(cross, "summary", return_value={
                    "exercised_only_by_a_demonstrator": ()}):
            found = acc.determination()
        self.assertEqual(acc.SATISFIED, found["verdict"])
        self.assertEqual([], found["not_consumed"])

    def test_one_demonstrator_is_enough_to_withhold_satisfaction(self):
        mixed = (
            _result("P4", "Runtime", cross.EXERCISED, "p12-f4-runtime-observation"),
            _result("P5", "Intelligence", cross.EXERCISED,
                    "authored by engineering-intelligence-instance-001"))
        with mock.patch.object(cross, "verify", return_value=mixed), \
                mock.patch.object(cross, "summary", return_value={
                    "exercised_only_by_a_demonstrator": ("P4",)}):
            found = acc.determination()
        self.assertEqual(acc.NOT_SATISFIED, found["verdict"])
        self.assertEqual(["P4"], found["not_consumed"])


class F05NonIndependentVerification(unittest.TestCase):
    """The boundary must come from the instrument, not from this module."""

    def test_the_boundary_is_read_from_the_persisted_instrument(self):
        boundary = acc.ratified_boundary()
        self.assertTrue(boundary.reading.startswith("R1"))
        self.assertEqual(
            "docs/governance/acts/"
            "FD-P12-001-E12-RATIFICATION-AND-ACCEPTANCE-BOUNDARY.md",
            boundary.instrument)
        self.assertTrue((REPO_ROOT / boundary.instrument).is_file())

    def test_no_ratified_instrument_raises_rather_than_defaulting(self):
        """An acceptance boundary nobody ratified is not one this office may
        supply. `§9` forbids creating a fourth interpretation, and silently
        defaulting to one would be exactly that."""
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        (Path(tmp.name) / "docs" / "governance" / "acts").mkdir(parents=True)
        with self.assertRaises(acc.AcceptanceBoundaryUnresolved):
            acc.determination(Path(tmp.name))

    def test_an_unissued_instrument_is_not_a_ratification(self):
        tmp = _world(status="Decision Status: PENDING FOUNDER DECISION")
        self.addCleanup(tmp.cleanup)
        with self.assertRaises(acc.AcceptanceBoundaryUnresolved):
            acc.ratified_boundary(Path(tmp.name))

    def test_two_issued_boundaries_are_refused_rather_than_picked_between(self):
        tmp = _world(name="a.md")
        self.addCleanup(tmp.cleanup)
        acts = Path(tmp.name) / "docs" / "governance" / "acts"
        (acts / "b.md").write_text(
            ISSUED.format(reading="R3 — DORMANCY IS LEGITIMATE"), encoding="utf-8")
        with self.assertRaises(acc.AcceptanceBoundaryUnresolved) as raised:
            acc.ratified_boundary(Path(tmp.name))
        self.assertIn("Founder question", str(raised.exception))


class F06FalseSection74PartJPass(unittest.TestCase):
    """`§11` — `E12 RATIFIED → PART J PASS` is prohibited."""

    def test_ratification_alone_does_not_satisfy_the_criterion(self):
        """Ratification is held constant while the evidence is removed.

        The instrument stayed ratified throughout `4 of 8`, `7 of 8` and
        `8 of 8`; the criterion followed the evidence each time. Here the
        ratified boundary is left exactly as it is and the evidence is emptied
        — and the criterion must fall back to NOT SATISFIED. If ratification
        alone could carry it, this would still report SATISFIED.
        """
        self.assertTrue(acc.ratified_boundary().reading.startswith("R1"))
        absent = tuple(
            _result(p, p, cross.NOT_EXERCISED, "nothing crossed it")
            for p in ("P4", "P5"))
        with mock.patch.object(cross, "verify", return_value=absent), \
                mock.patch.object(cross, "summary", return_value={
                    "exercised_only_by_a_demonstrator": ()}):
            self.assertEqual(acc.NOT_SATISFIED,
                             acc.determination()["verdict"])
        self.assertTrue(acc.ratified_boundary().reading.startswith("R1"))

    def test_the_instrument_itself_says_ratification_is_not_a_pass(self):
        body = (REPO_ROOT / "docs" / "governance" / "acts" /
                "FD-P12-001-E12-RATIFICATION-AND-ACCEPTANCE-BOUNDARY.md"
                ).read_text(encoding="utf-8")
        self.assertIn("E12 RATIFICATION ≠ E12 PASS", body)
        self.assertIn("does not itself establish that the E12 criterion has "
                      "passed", body)


class F07UnauthorizedCompletionInference(unittest.TestCase):
    """Completion must not be inferred from ratification or from green tests."""

    def test_the_module_reports_a_criterion_not_a_completion(self):
        found = acc.determination()
        self.assertEqual("E12-06 — System-wide Verification", found["criterion"])
        for forbidden in ("complete", "certified", "P12 COMPLETE"):
            self.assertNotIn(forbidden, str(found))

    def test_the_module_creates_no_authority(self):
        import ast
        tree = ast.parse((REPO_ROOT / "tools" / "p12_e12_acceptance.py")
                         .read_text(encoding="utf-8"))
        creating = [n.name for n in ast.walk(tree)
                    if isinstance(n, ast.FunctionDef)
                    and n.name.lower().startswith(
                        ("ratify", "authorize", "authorise", "certify",
                         "approve", "complete"))]
        self.assertEqual([], creating)

    def test_the_module_writes_nothing(self):
        source = (REPO_ROOT / "tools" / "p12_e12_acceptance.py").read_text(
            encoding="utf-8")
        for forbidden in ("write_text(", "mkdir(", "unlink("):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
