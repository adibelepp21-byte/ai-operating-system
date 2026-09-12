"""P12-W6 — cross-phase verification conformance.

The controls that matter are that existence never yields `EXERCISED`, that the
two genuinely uncrossed phases are reported as such rather than smoothed over,
and that a predicate reading *records* instead of *executions* fails — because
one of them did, and passed, before it was caught.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import p12_cross_phase_verification as w6


class TheCanonicalPhaseListIsTheCanonsNotARestatement(unittest.TestCase):
    def test_eight_phases_in_canonical_order(self):
        self.assertEqual(
            w6.CANONICAL_PHASES,
            (("P4", "Runtime"), ("P5", "Intelligence"), ("P6", "Knowledge"),
             ("P7", "Memory"), ("P8", "Tools"), ("P9", "Workflow"),
             ("P10", "Department"), ("P11", "Organization")),
        )

    def test_p8_is_tools_not_the_skill_boundary(self):
        """Two taxonomies, not one: the Native Core boundary is `skill`."""
        self.assertIn(("P8", "Tools"), w6.CANONICAL_PHASES)


class ExistenceIsNotExercise(unittest.TestCase):
    """§48 — a relationship is not verified merely because both surfaces exist."""

    def test_with_no_execution_evidence_nothing_is_exercised(self):
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp)
            with mock.patch.object(w6.traces, "STORE_ROOT", empty), \
                 mock.patch.object(w6.observation, "OBSERVATION_ROOT", empty), \
                 mock.patch.object(w6.traces, "all_records", return_value=()):
                results = w6.verify()
        exercised = [r.phase for r in results if r.status == w6.EXERCISED]
        self.assertEqual(
            exercised, [],
            "every Native Core boundary and organization record still exists; "
            "none of that is evidence that anything crossed them",
        )

    def test_a_department_record_alone_does_not_exercise_p10(self):
        """The first version of this predicate returned EXERCISED because
        delegation *records* exist. A verifier that refuses 'both surfaces
        exist' cannot accept 'a record exists' one function later."""
        with mock.patch.object(w6.traces, "all_records", return_value=()):
            exercised, evidence = w6._department_exercised(())
        self.assertFalse(exercised)
        self.assertIn("declaration", evidence)

    def test_p10_requires_the_actor_to_have_acted(self):
        class _Record:
            agent_instance = "engineering-intelligence-instance-001"
            runtime = "r"
        exercised, evidence = w6._department_exercised((_Record(),))
        self.assertTrue(exercised)
        self.assertIn("authored a Trace record", evidence)


class TheUncrossedPhasesAreReportedHonestly(unittest.TestCase):
    def test_knowledge_and_memory_are_not_exercised(self):
        results = {r.phase: r for r in w6.verify()}
        self.assertEqual(results["P6"].status, w6.NOT_EXERCISED)
        self.assertEqual(results["P7"].status, w6.NOT_EXERCISED)

    def test_their_evidence_states_why(self):
        results = {r.phase: r for r in w6.verify()}
        self.assertIn("empty in every Trace record", results["P6"].evidence)
        self.assertIn("empty in every Trace record", results["P7"].evidence)

    def test_not_exercised_is_not_reported_as_unknown(self):
        """An absent crossing is measured, not undeterminable."""
        results = {r.phase: r for r in w6.verify()}
        self.assertNotEqual(results["P6"].status, w6.UNKNOWN)


class DemonstratorProvenanceIsReported(unittest.TestCase):
    """`F-10`'s error was a coverage figure that counted its own demonstrator.
    Six-of-eight reads differently depending on who made the crossings."""

    def test_the_summary_names_phases_exercised_only_by_a_demonstrator(self):
        summary = w6.summary()
        self.assertIn("exercised_only_by_a_demonstrator", summary)
        self.assertEqual(set(summary["exercised_only_by_a_demonstrator"]),
                         {"P4", "P9"})

    def test_p11_is_not_demonstrator_only(self):
        """P11's crossing came from the resident W1 work path."""
        self.assertNotIn("P11", w6.summary()["exercised_only_by_a_demonstrator"])

    def test_the_counts_sum_to_the_phase_count(self):
        s = w6.summary()
        self.assertEqual(
            s["exercised"] + s["not_exercised"] + s["unknown"], s["phases"])


class EveryResultCarriesItsEvidence(unittest.TestCase):
    def test_no_result_is_silent_about_why(self):
        for result in w6.verify():
            self.assertTrue(result.evidence.strip(), f"{result.phase} has no evidence")

    def test_statuses_use_the_declared_vocabulary(self):
        for result in w6.verify():
            self.assertIn(result.status,
                          (w6.EXERCISED, w6.NOT_EXERCISED, w6.UNKNOWN))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
