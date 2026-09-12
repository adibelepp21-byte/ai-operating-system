"""P12-W6 phase-level mutation verification conformance (`§50`).

The suite under test reports seven detections. Seven detections is also exactly
what a suite that attempts nothing and returns `DETECTED` would report, so the
controls here establish the three properties that tell the two apart:

* every mutation runs a real detector, not an existence check;
* the suite can report `MISSED`, so a detection is a measurement;
* a mutation that was never applied is never counted as an undetected one.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools import p12_mutation_verification as mut


class TheScopeIsSection50s(unittest.TestCase):
    def test_all_ten_named_mutations_are_present(self):
        self.assertEqual(len(mut.MUTATIONS), 10)

    def test_every_mutation_is_in_section_50_order(self):
        self.assertEqual(
            [name for name, _ in mut.MUTATIONS],
            ["remove authority", "alter provenance", "change owner",
             "inject stale state", "forge actor", "forge decision",
             "break workflow", "duplicate delegation", "alter state authority",
             "change frozen boundary"])

    def test_every_mutation_returns_the_three_part_result(self):
        for name, attempt in mut.MUTATIONS:
            with self.subTest(name):
                attempted, detected, detail = attempt()
                self.assertIsInstance(attempted, bool)
                self.assertIsInstance(detected, bool)
                self.assertTrue(detail.strip(), "a result must say why")


class AnUnappliedMutationIsNotAnUndetectedOne(unittest.TestCase):
    """The classifier defect this module was built to refuse, held closed."""

    def test_not_attempted_classifies_as_unavailable_not_missed(self):
        original = mut.MUTATIONS
        mut.MUTATIONS = (("never applied", lambda: (False, False, "no subject")),)
        try:
            result = mut.verify()[0]
        finally:
            mut.MUTATIONS = original
        self.assertEqual(result.status, mut.UNAVAILABLE)
        self.assertFalse(result.attempted)

    def test_an_unavailable_result_is_excluded_from_missed(self):
        original = mut.MUTATIONS
        mut.MUTATIONS = (("never applied", lambda: (False, False, "no subject")),)
        try:
            summary = mut.summary()
        finally:
            mut.MUTATIONS = original
        self.assertEqual(summary["missed"], 0)
        self.assertEqual(summary["unavailable"], 1)
        self.assertEqual(summary["missed_mutations"], ())

    def test_a_raising_attempt_is_unavailable_not_detected(self):
        def explode():
            raise RuntimeError("detector import failed")

        original = mut.MUTATIONS
        mut.MUTATIONS = (("broken probe", explode),)
        try:
            result = mut.verify()[0]
        finally:
            mut.MUTATIONS = original
        self.assertEqual(result.status, mut.UNAVAILABLE)
        self.assertIn("detector import failed", result.detail)


class TheSuiteCanReportMissed(unittest.TestCase):
    """Without this, seven detections prove nothing about the system."""

    def test_a_missed_mutation_is_reported_as_missed(self):
        original = mut.MUTATIONS
        mut.MUTATIONS = (("undetected", lambda: (True, False, "nothing refused it")),)
        try:
            result = mut.verify()[0]
            summary = mut.summary()
        finally:
            mut.MUTATIONS = original
        self.assertEqual(result.status, mut.MISSED)
        self.assertEqual(summary["missed_mutations"], ("undetected",))

    def test_the_live_run_actually_reports_missed_results(self):
        summary = mut.summary()
        self.assertGreater(
            summary["missed"], 0,
            "a run with zero MISSED results would need a control proving the "
            "suite is capable of reporting one")


class EachMutationExercisesARealDetector(unittest.TestCase):
    def test_removing_authority_is_refused_by_the_delegation_registry(self):
        attempted, detected, _ = mut._remove_authority()
        self.assertTrue(attempted)
        self.assertTrue(detected)

    def test_a_valid_delegation_request_is_otherwise_accepted(self):
        """The refusals above must be caused by the mutation, not by the fixture."""
        from tools.w4_delegation import AUTHORIZED_DELEGATOR, DelegationError
        with tempfile.TemporaryDirectory() as tmp:
            registry, request = mut._delegation_fixture(Path(tmp))
            with self.assertRaises(DelegationError) as raised:
                registry.issue(delegator=AUTHORIZED_DELEGATOR,
                               recipient_instance="unregistered-instance-001",
                               **request)
        # The only complaint is the unregistered recipient — every `§13`
        # element the fixture supplies is accepted.
        self.assertIn("registered Agent Instance", str(raised.exception))

    def test_altering_provenance_runs_reconcile_not_a_membership_check(self):
        attempted, detected, detail = mut._alter_provenance()
        self.assertTrue(attempted)
        self.assertTrue(detected)
        self.assertNotIn("declared defect kind", detail)

    def test_changing_an_owner_is_detected_against_nesting(self):
        attempted, detected, _ = mut._change_owner()
        self.assertTrue(attempted)
        self.assertTrue(detected)

    def test_changing_an_owner_leaves_the_resident_tree_untouched(self):
        from tools import organization_catalog as org
        before = org.report()["inv1_disputed"]
        mut._change_owner()
        self.assertEqual(org.report()["inv1_disputed"], before)

    def test_a_stale_running_observation_is_refused(self):
        attempted, detected, _ = mut._inject_stale_state()
        self.assertTrue(attempted and detected)

    def test_an_illegal_workflow_transition_is_refused(self):
        attempted, detected, _ = mut._break_workflow()
        self.assertTrue(attempted and detected)

    def test_a_twelfth_frozen_boundary_is_detected(self):
        attempted, detected, _ = mut._alter_frozen_boundary()
        self.assertTrue(attempted and detected)


class TheDuplicateProbeCarriesItsOwnControl(unittest.TestCase):
    """A null result must be a measurement, not a probe that failed to run."""

    def test_duplicated_representation_is_detected(self):
        from tools.delegation_reconciliation import (
            ACTIVE, LedgerGrant, Projection, reconcile)
        grant = LedgerGrant("g1", ACTIVE, "i-001", ("probe",), "FD-P11-001",
                            mut.AUTHORIZING_RECORD, "acct", "synthetic")
        twice = [Projection(f"w3-{n}", f"{n}.md", "g1", "CURRENT", "probe",
                            "i-001") for n in ("a", "b")]
        kinds = [k for k, _, _ in reconcile(twice, {"g1": grant})["defects"]]
        self.assertIn("duplicate-representation", kinds)

    def test_duplicated_delegation_is_not_detected(self):
        attempted, detected, detail = mut._duplicate_delegation()
        self.assertTrue(attempted, "the control must have run")
        self.assertFalse(detected)
        self.assertIn("duplicated delegation", detail)


class TheFindingsAreRecordedAsFindings(unittest.TestCase):
    def test_forging_a_decision_is_missed(self):
        attempted, detected, _ = mut._forge_decision()
        self.assertTrue(attempted)
        self.assertFalse(
            detected,
            "if the certified-evidence guard has since learned to distinguish "
            "an issued instrument from a planted one, this finding is closed "
            "and the evidence record must say so")

    def test_state_authority_is_now_attemptable_and_detected(self):
        """Updated because the system changed, not because the test was wrong.

        This mutation was `UNAVAILABLE` while `P12-W2` did not exist: there was
        no surface on which two competing authority claims could be planted, and
        reporting an unattempted mutation as missed would have asserted a
        detector had been exercised. `ACT-CC-P12-W2-001` built the surface, so
        the mutation is attempted, and the conflict detector refuses it.
        """
        attempted, detected, detail = mut._alter_state_authority()
        self.assertTrue(attempted)
        self.assertTrue(detected, detail)

    def test_the_state_authority_probe_carries_its_own_control(self):
        """A null result must be a measurement, not a detector that never fires."""
        _, _, detail = mut._alter_state_authority()
        self.assertNotIn("control is unsound", detail)

    def test_no_mutation_remains_unavailable(self):
        self.assertEqual(mut.summary()["unavailable"], 0)

    def test_nothing_resident_is_mutated_by_a_full_run(self):
        from tools import organization_catalog as org
        before = org.report()["inv1_disputed"]
        mut.verify()
        self.assertEqual(org.report()["inv1_disputed"], before)


if __name__ == "__main__":
    unittest.main()
