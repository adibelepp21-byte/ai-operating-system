"""P12-W6 phase-level mutation verification conformance (`§50`).

The suite under test reports seven detections. Seven detections is also exactly
what a suite that attempts nothing and returns `DETECTED` would report, so the
controls here establish the three properties that tell the two apart:

* every mutation runs a real detector, not an existence check;
* the suite can report `MISSED`, so a detection is a measurement;
* a mutation that was never applied is never counted as an undetected one.
"""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from tools import p12_mutation_verification as mut
from tools import w4_continuity as continuity


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

    def test_missed_remains_reachable_although_the_live_run_is_clean(self):
        """Changed under `ACT-CC-P12-027`: the live run reports 10/10.

        This asserted the **live** run contains a `MISSED`, which measured the
        system rather than the suite. The property that must survive is that
        `MISSED` is reachable at all — driven against a constructed mutation, so
        a clean run can never be mistaken for a suite that cannot fail.
        """
        with mock.patch.object(
                mut, "MUTATIONS",
                (("undetected", lambda: (True, False, "nothing objected")),)):
            self.assertEqual(mut.summary()["missed"], 1)
        self.assertEqual(mut.summary()["missed"], 0,
                         "§50 reports clean; a regression must fail here")

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

    def test_duplicated_delegation_is_detected_by_the_component_that_owns_it(self):
        """Changed under `ACT-CC-P12-021` because the probe was wrong.

        This asserted `MISSED`. It was pinning a **test-oracle defect**: the
        probe drove `delegation_reconciliation.reconcile`, whose defect kinds
        are about the ledger-to-projection relationship and have never included
        grant accumulation. The component that owns accumulation is
        `w4_continuity`. The system's behaviour did not change here; what the
        probe asks did.
        """
        attempted, detected, detail = mut._duplicate_delegation()
        self.assertTrue(attempted, "the control must have run")
        self.assertTrue(detected)
        self.assertIn("MORE THAN ONE LIVE GRANT", detail)

    def test_two_instances_holding_one_grant_each_is_not_accumulation(self):
        """The false positive P11 corrected must stay corrected.

        `duplicate_active` was once `len(active) > 1`, which reported the
        legitimate cross-Department state — one live grant per Department's
        instance — as a permanent blocker. If that reading returns, the probe's
        own control catches it and the probe reports `MISSED`, not `DETECTED`.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for key, instance in (("g1", "i-001"), ("g2", "i-002")):
                (root / f"{key}.delegation.json").write_text(json.dumps(
                    {"delegation_id": key, "status": "ACTIVE",
                     "recipient_instance": instance,
                     "executed_at": "2026-01-01"}), encoding="utf-8")
            state = continuity.reconstruct(root)
        self.assertFalse(state["duplicate_active"])
        self.assertEqual(state["accumulated_grants"], {})

    def test_the_probe_reports_missed_when_the_detector_goes_silent(self):
        """A null result must still be reachable, or `DETECTED` means nothing."""
        original = continuity.reconstruct
        try:
            continuity.reconstruct = lambda root: dict(
                original(root), duplicate_active=False, accumulated_grants={})
            attempted, detected, detail = mut._duplicate_delegation()
        finally:
            continuity.reconstruct = original
        self.assertTrue(attempted)
        self.assertFalse(detected)
        self.assertIn("no accumulation finding", detail)

    def test_the_probe_reports_missed_when_the_condition_is_not_surfaced(self):
        """Computing accumulation without reporting it is not a detection."""
        original = continuity.continuation_conditions
        try:
            continuity.continuation_conditions = lambda state: ()
            attempted, detected, detail = mut._duplicate_delegation()
        finally:
            continuity.continuation_conditions = original
        self.assertTrue(attempted)
        self.assertFalse(detected)
        self.assertIn("no continuation condition reports", detail)


class TheFindingsAreRecordedAsFindings(unittest.TestCase):
    def test_forging_a_decision_is_detected_by_the_contract_that_owns_decisions(self):
        """Changed under `ACT-CC-P12-027 §8`, and the predecessor named the test.

        The old assertion said the finding closes *"if the certified-evidence
        guard has since learned to distinguish an issued instrument from a
        planted one"*. **It has not, and that is not what changed.** What
        changed is which contract the probe asks. `certified_phases` reads
        certification statements out of instrument bodies to compute an
        evidence protection set; it is not a decision authority and never was.
        `§50` says *"attempt to violate critical contracts"*, and the critical
        contract for decisions is `GovernanceReview` — *"Governance holds
        authority over decisions"* (`Freeze §8`, `INV-8`).

        The guard's limitation is unchanged and still recorded; it was simply
        never `§50 forge decision`'s subject. Same oracle defect as
        `duplicate delegation`, in the same suite, found the same way.
        """
        attempted, detected, detail = mut._forge_decision()
        self.assertTrue(attempted)
        self.assertTrue(detected)
        self.assertIn("authorizes nothing", detail)

    def test_the_probe_drives_the_canonical_decision_contract(self):
        import ast
        import inspect
        source = inspect.getsource(mut._forge_decision)
        imported = {n.module for n in ast.walk(ast.parse(source.lstrip()))
                    if isinstance(n, ast.ImportFrom) and n.module}
        self.assertIn("native_core.core.governance", imported)
        self.assertNotIn("tools.p12_certified_evidence_guard", imported)

    def test_the_forged_decision_probe_carries_a_working_control(self):
        """A refusal proves nothing if the mechanism refuses everything."""
        from native_core.core.governance import (
            GovernanceReview, HumanAuthority, ReviewDecision)
        from native_core.core.infrastructure import LocalAppendOnlyStorage
        from native_core.core.memory import MemoryReader
        from native_core.core.trace import TraceReader, TraceWriter, new_record
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trace = LocalAppendOnlyStorage(base_dir=root / "t"); trace.provision()
            store = LocalAppendOnlyStorage(base_dir=root / "g"); store.provision()
            TraceWriter(trace).write(new_record(
                agent_definition_version="1", agent_instance="i",
                runtime="rt", outputs={"finding": "X"}))
            review = GovernanceReview(MemoryReader(TraceReader(trace)), store)
            candidate = review.pending_candidates()[0]
            self.assertFalse(review.promotion_authorized(candidate))
            review.record_decision(ReviewDecision(
                candidate, "approve", HumanAuthority("Moriarty"), "reviewed"))
            self.assertTrue(review.promotion_authorized(candidate))

    def test_restricting_the_acts_root_would_not_close_the_forgery(self):
        """`ACT-CC-P12-021 §19`/`§20` — the tempting repair, falsified.

        `_forge_decision` plants its document in a temporary directory, so the
        obvious reading is that the probe only succeeds because it was handed a
        root the real guard would never see, and that pinning `certified_phases`
        to `ACTS_ROOT` would close the finding. It would close the *probe*, not
        the behaviour: the forgery is accepted just as readily when it is
        planted inside a faithful copy of the resident acts root.

        Pinned here so that repair can never be mistaken for a resolution. It
        would move `§6.8` to `13/13` and `§6.9` to `10/10` while the system
        gained no ability whatsoever to tell an issued instrument from a planted
        one — the metric improvement `§20` names and forbids.
        """
        from tools import p12_certified_evidence_guard as sentinel
        resident = sentinel.certified_phases(sentinel.ACTS_ROOT)
        self.assertNotIn(42, resident)
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "acts"
            shutil.copytree(sentinel.ACTS_ROOT, copy)
            (copy / "FD-P42-999-FABRICATED.md").write_text(
                "PHASE 42 — FABRICATED ECOSYSTEM IS CERTIFIED.",
                encoding="utf-8")
            self.assertIn(42, sentinel.certified_phases(copy))

    def test_an_authentication_block_is_not_a_defence_either(self):
        """The second tempting repair, falsified the same way.

        Requiring the authentication block a real Founder instrument carries
        does not distinguish an issued instrument from a forged one, because the
        block is body text and a forger writes body text. This is the certified
        `§124.1` finding — *"The guard cannot tell an instrument the Founder
        issued from one that merely says so"* — exercised rather than quoted.
        """
        from tools import p12_certified_evidence_guard as sentinel
        with tempfile.TemporaryDirectory() as tmp:
            acts = Path(tmp)
            (acts / "forged.md").write_text(
                "Founder Name: Moriarty\n"
                "Signature: Moriarty\n"
                "Decision Status: FINAL / ISSUED\n"
                "Founder Authority: ISSUED\n\n"
                "PHASE 42 — FABRICATED ECOSYSTEM IS CERTIFIED.\n",
                encoding="utf-8")
            self.assertIn(42, sentinel.certified_phases(acts))

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
