"""P12-W6 system negative controls conformance (`§49`).

Eleven refusals is what a module returning a constant would print. These
controls establish that each result comes from an attempt that was actually
made, that `ACCEPTED` is reachable, and — the defect this module committed on
its first run — that a probe's own exception can never be read as a refusal.
"""

from __future__ import annotations

import unittest
from unittest import mock

from tools import p12_system_negative_controls as neg


class TheScopeIsSection49s(unittest.TestCase):
    def test_the_thirteen_are_section_49s_in_order(self):
        self.assertEqual(
            list(neg.NEGATIVE_CONTROLS),
            ["self-authorization", "authority expansion", "governance bypass",
             "invalid provenance", "fabricated actor", "unauthorized delegation",
             "unauthorized state mutation", "unauthorized architecture mutation",
             "unauthorized P13 authorization", "false completion",
             "false certification", "stale-state acceptance",
             "historical-as-current substitution"])

    def test_every_control_has_an_attempt(self):
        self.assertEqual([name for name, _ in neg.CONTROLS],
                         list(neg.NEGATIVE_CONTROLS))

    def test_this_is_not_the_verifier_falsifiability_module(self):
        """`§49` is about the system; `§18` of the Act is about the verifiers."""
        from tools import p12_negative_control_verification as verifiers
        self.assertNotEqual(set(neg.NEGATIVE_CONTROLS),
                            {name for name, _, _ in verifiers.CONTROLS})


class AProbeExceptionIsNeverARefusal(unittest.TestCase):
    """The defect this module committed on its own first run."""

    def test_a_raising_attempt_is_uncontrolled_not_refused(self):
        def explode():
            raise AttributeError("'Goal' object has no attribute 'plans'")

        with mock.patch.object(neg, "CONTROLS", (("probe", explode),)):
            result = neg.verify()[0]
        self.assertEqual(result.status, neg.UNCONTROLLED)
        self.assertFalse(result.attempted)

    def test_uncontrolled_is_counted_as_not_refused(self):
        def explode():
            raise RuntimeError("boom")

        with mock.patch.object(neg, "CONTROLS", (("probe", explode),)):
            summary = neg.summary()
        self.assertEqual(summary["refused"], 0)
        self.assertEqual(summary["not_refused"], ("probe",))

    def test_no_live_control_reports_its_own_exception(self):
        for result in neg.verify():
            with self.subTest(result.control):
                self.assertNotIn("attempt raised", result.detail)
                self.assertNotIn("AttributeError", result.detail)

    def test_the_bypass_probe_accepts_only_the_real_refusal_type(self):
        """A broad except would pass whenever the probe itself is wrong."""
        from tools.planning import EscalationRequired
        with mock.patch.object(neg, "_fixture",
                               side_effect=TypeError("probe is wrong")):
            with self.assertRaises(TypeError):
                neg._governance_bypass()
        self.assertTrue(issubclass(EscalationRequired, Exception))


class AcceptedIsReachable(unittest.TestCase):
    """Without this, eleven refusals prove nothing."""

    def test_an_unrefused_attempt_is_reported_accepted(self):
        with mock.patch.object(
                neg, "CONTROLS",
                (("probe", lambda: (True, False, "nothing objected")),)):
            result = neg.verify()[0]
        self.assertEqual(result.status, neg.ACCEPTED)
        self.assertTrue(result.attempted)

    def test_the_live_run_reports_accepted_results(self):
        summary = neg.summary()
        self.assertGreater(
            summary["accepted"], 0,
            "a run with zero ACCEPTED would need a control proving this module "
            "is capable of reporting one")

    def test_the_remaining_finding_is_named(self):
        """Pinned, so an unrefused control cannot appear or vanish silently.

        This read `("unauthorized P13 authorization", "false certification")`
        until `ACT-CC-P12-007` closed the first by making the self-model report
        the phase authorization state the Founder had already decided. The
        assertion is **narrowed to what is true, not relaxed**: the tuple is
        still exact, so a third finding appearing — or `false certification`
        being quietly "closed" while it remains Founder-reserved — still fails
        here. `tools/tests/test_p12_phase_authorization.py` is what proves the
        first genuinely closed rather than being argued away."""
        self.assertEqual(neg.summary()["not_refused"],
                         ("false certification",))

    def test_false_certification_remains_founder_reserved(self):
        """`ACT-CC-P12-007 §12` — untouched, and not closable from here.

        The two controls are separate matters and were kept separate: closing
        one is not progress on the other, and a run reporting `§49` as clean
        would mean this control had been reinterpreted rather than satisfied."""
        results = {r.control: r for r in neg.verify()}
        self.assertEqual(results["false certification"].status, neg.ACCEPTED)
        self.assertTrue(results["false certification"].attempted)


class EachAttemptIsActuallyMade(unittest.TestCase):
    def test_all_thirteen_are_attempted(self):
        summary = neg.summary()
        self.assertEqual(summary["attempted"], 13)
        self.assertEqual(summary["uncontrolled"], 0)

    def test_self_authorization_is_refused_by_the_planning_surface(self):
        attempted, refused, detail = neg._self_authorization()
        self.assertTrue(attempted and refused)
        self.assertIn("delegation record", detail)

    def test_governance_bypass_is_refused_by_escalation(self):
        attempted, refused, detail = neg._governance_bypass()
        self.assertTrue(attempted and refused)
        # The detail is truncated at 70 characters, which cuts before the
        # word "escalate"; assert on the clause that survives.
        self.assertIn("would need authority the plan does not", detail)

    def test_authority_expansion_is_refused_at_the_permitted_surface(self):
        attempted, refused, _ = neg._authority_expansion()
        self.assertTrue(attempted and refused)

    def test_the_fixture_builds_a_real_plan(self):
        surface, plan = neg._fixture()
        self.assertTrue(plan.steps)
        self.assertTrue(surface.delegation_requirements(plan))

    def test_nothing_resident_is_written_by_a_full_run(self):
        from tools import p12_certified_evidence_guard as guard
        before = guard.certified_phases()
        neg.verify()
        self.assertEqual(guard.certified_phases(), before)


class WhatThisSuiteDoesNotEstablish(unittest.TestCase):
    def test_refused_is_not_a_claim_that_no_bypass_exists(self):
        """Eleven named paths refuse. Unnamed paths are not covered."""
        self.assertEqual(len(neg.NEGATIVE_CONTROLS), 13)


if __name__ == "__main__":
    unittest.main()


class SupplementaryControlsNeverInflateSection49(unittest.TestCase):
    """`ACT-CC-P12-022` — added beside `§49`, never inside it.

    `§6.8` asks whether `§49`'s thirteen hold. Two controls were added this Act
    and both pass; if they had been appended to `CONTROLS`, `§6.8` would have
    read `14/15` and looked like progress it is not.
    """

    def test_section_49_is_still_exactly_thirteen(self):
        self.assertEqual(len(neg.CONTROLS), 13)
        self.assertEqual([name for name, _ in neg.CONTROLS],
                         list(neg.NEGATIVE_CONTROLS))

    def test_no_supplementary_control_is_a_section_49_control(self):
        self.assertFalse(
            {name for name, _ in neg.SUPPLEMENTARY_CONTROLS}
            & set(neg.NEGATIVE_CONTROLS))

    def test_the_headline_numbers_count_only_section_49(self):
        summary = neg.summary()
        self.assertEqual(summary["controls"], 13)
        self.assertEqual(summary["refused"], 12)
        self.assertEqual(summary["accepted"], 1)
        self.assertEqual(summary["not_refused"], ("false certification",))

    def test_the_supplementary_results_are_reported_under_their_own_keys(self):
        summary = neg.summary()
        self.assertEqual(summary["supplementary"], 2)
        self.assertEqual(summary["supplementary_refused"], 2)
        self.assertEqual(summary["supplementary_not_refused"], ())

    def test_a_lone_planted_instrument_is_reported(self):
        attempted, refused, detail = neg._unregistered_certification()
        self.assertTrue(attempted and refused)
        self.assertIn("phase 42", detail)

    def test_no_forged_certification_permits_a_refused_write(self):
        attempted, refused, detail = neg._forged_certification_permitting_a_write()
        self.assertTrue(attempted and refused)
        self.assertIn("expands the prohibition set or fails closed", detail)

    def test_false_certification_is_still_accepted_beside_them(self):
        """The limit, pinned. Neither supplementary control closes `§6.8`."""
        results = {r.control: r.status for r in neg.verify()}
        self.assertEqual(results["false certification"], neg.ACCEPTED)
