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

    def test_the_two_findings_are_named(self):
        self.assertEqual(neg.summary()["not_refused"],
                         ("unauthorized P13 authorization",
                          "false certification"))


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
