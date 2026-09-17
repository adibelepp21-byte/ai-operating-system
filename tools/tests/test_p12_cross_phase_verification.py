"""P12-W6 — cross-phase verification conformance.

The controls that matter are that existence never yields `EXERCISED`, that an
uncrossed phase is reported as such rather than smoothed over, and that a
predicate reading *records* instead of *executions* fails — because one of them
did, and passed, before it was caught.

All eight phases are now crossed by real work, which makes the live corpus a
weak witness on its own: it would look identical for a verifier that returned
`EXERCISED` unconditionally. So each predicate is also driven directly against
evidence that should refuse it.
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
    def test_every_phase_is_now_exercised(self):
        """`P7` was pinned here until `ACT-CC-P12-014` built a real work path
        that consumes Memory; `P6` until `FD-P12-002` authorized the Knowledge
        admission and the work consumed the admitted version. The class name
        stays, because what it guards is unchanged — the measurement must be
        exact in both directions, so this pins the *whole* result rather than
        relaxing to "at least the ones we expect"."""
        results = {r.phase: r.status for r in w6.verify()}
        self.assertEqual({w6.EXERCISED}, set(results.values()), results)

    def test_the_predicate_still_reports_an_absent_crossing(self):
        """The verifier must still be able to say NOT EXERCISED.

        With every live phase crossed, a test that only reads the live corpus
        would pass for a predicate that returned `EXERCISED` unconditionally.
        This drives the Knowledge predicate directly with a record that
        consumed nothing.
        """
        class Bare:
            knowledge_consumed = ()
        exercised, evidence = w6._knowledge_exercised((Bare(),))
        self.assertFalse(exercised)
        self.assertIn("empty in every Trace record", evidence)

    def test_its_evidence_states_what_was_consumed(self):
        results = {r.phase: r for r in w6.verify()}
        self.assertIn("corpus-health.criteria", results["P6"].evidence)

    def test_memory_is_exercised_by_captured_content(self):
        """`INV-6` — the record holds captured content, not references, and the
        predicate reads it. Before `ACT-CC-P12-014` it could only read bare
        strings, so the first record that honoured the invariant made the phase
        report `UNKNOWN`."""
        results = {r.phase: r for r in w6.verify()}
        self.assertEqual(results["P7"].status, w6.EXERCISED)
        self.assertNotEqual(results["P7"].status, w6.UNKNOWN)
        self.assertIn("corpus-health.finding", results["P7"].evidence)

    def test_no_phase_is_reported_unknown(self):
        """An absent crossing would be measured, not undeterminable.

        `UNKNOWN` is the status the Knowledge and Memory predicates produced
        when they could only read records that broke `INV-6`. No phase may
        reach it.
        """
        results = {r.phase: r for r in w6.verify()}
        self.assertEqual([], [p for p, r in results.items()
                              if r.status == w6.UNKNOWN])


class DemonstratorProvenanceIsReported(unittest.TestCase):
    """`F-10`'s error was a coverage figure that counted its own demonstrator.
    Six-of-eight reads differently depending on who made the crossings."""

    def test_no_phase_is_exercised_only_by_a_demonstrator(self):
        """`P4` and `P9` were demonstrator-only until `ACT-CC-P12-014` gave both
        a real-work crossing. Pinned exactly, so a regression to
        demonstrator-only still fails here."""
        summary = w6.summary()
        self.assertIn("exercised_only_by_a_demonstrator", summary)
        self.assertEqual((), tuple(summary["exercised_only_by_a_demonstrator"]))

    def test_the_attribution_still_fires_when_every_crossing_is_a_demonstrator(self):
        """Without this, an empty list would be a constant rather than a
        measurement. Driven on evidence naming only demonstrators."""
        only = f"workflow observation published for ['{w6.DEMONSTRATOR_EXECUTIONS[2]}']"
        self.assertTrue(w6._is_demonstrator_only(only))
        mixed = (f"workflow observation published for "
                 f"['aios-corpus-health', '{w6.DEMONSTRATOR_EXECUTIONS[2]}']")
        self.assertFalse(w6._is_demonstrator_only(mixed))

    def test_the_superseded_marker_rule_would_have_misattributed_the_new_work(self):
        """The rule this replaced asked whether the evidence mentioned a
        demonstrator and mentioned neither `p11-` nor `engineering-intelligence`.
        A new real-work crossing carries neither marker, so the old rule would
        have called a genuinely crossed phase demonstrator-only."""
        evidence = ("Trace records name runtimes ['aios-corpus-health-runtime', "
                    "'p12-f4-runtime-observation']")
        superseded = (any(n in evidence for n in w6.DEMONSTRATOR_EXECUTIONS)
                      and not any(m in evidence for m in
                                  ("p11-", "engineering-intelligence")))
        self.assertTrue(superseded, "the superseded rule flagged it")
        self.assertFalse(w6._is_demonstrator_only(evidence),
                         "the structural rule does not")

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
