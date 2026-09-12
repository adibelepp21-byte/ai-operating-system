"""P12-W5 self-model semantic contract conformance (`§18`, `§36`–`§41`).

Twelve bound answers is what a checker that follows every alias would print
whether or not the binding exists, so the controls here drive it to `UNBOUND`
and hold the canonical question set against the Authorization body.
"""

from __future__ import annotations

import unittest
from unittest import mock

from tools import p12_self_model_contract as contract


class TheQuestionSetIsSection18s(unittest.TestCase):
    def test_twelve_questions_in_the_authorization_order(self):
        self.assertEqual(
            list(contract.canonical_questions()),
            ["What am I?", "What do I own?", "What authority do I have?",
             "What capabilities exist?", "What is running?", "What failed?",
             "What is incomplete?", "What is authoritative?", "What changed?",
             "What is stale?", "What do I not know?",
             "What decisions are recorded?"])

    def test_the_contract_covers_the_canonical_set_in_full(self):
        """`§36`: no shortened substitute set may silently replace it."""
        complete = contract.contract_is_complete()
        self.assertEqual(complete["canonical"], complete["contracted"])
        self.assertTrue(complete["in_order"])
        self.assertEqual(complete["missing"], ())
        self.assertEqual(complete["extra"], ())

    def test_a_missing_question_is_detected(self):
        with mock.patch.object(contract, "CONTRACT", contract.CONTRACT[:-1]):
            complete = contract.contract_is_complete()
        self.assertEqual(len(complete["missing"]), 1)
        self.assertFalse(complete["in_order"])

    def test_every_question_states_why_its_answer_is_correct(self):
        """`ACT §25` — the goal is not to produce an answer."""
        for item in contract.CONTRACT:
            with self.subTest(item.question):
                self.assertGreater(len(item.why_correct), 40)
                self.assertTrue(item.source_authority.strip())


class BindingsAreMeasuredNotAsserted(unittest.TestCase):
    """The checker read only function-local imports and reported three false
    `UNBOUND` results. Held closed."""

    def test_every_answer_is_bound_to_its_declared_source(self):
        unbound = [name for name, status in
                   contract.answers_bound_to_their_source()
                   if status == contract.UNBOUND]
        self.assertEqual(unbound, [])

    def test_answers_reading_through_a_module_alias_are_bound(self):
        bindings = dict(contract.answers_bound_to_their_source())
        for name in ("incomplete", "stale", "decisions"):
            with self.subTest(name):
                self.assertEqual(bindings[name], contract.BOUND)

    def test_the_checker_can_still_report_unbound(self):
        wrong = contract.QuestionContract(
            "What is running?", "running", "tools.nothing_reads_this",
            contract.AUTHORITATIVE, "none", "none", "a deliberately wrong "
            "binding used to prove this check can fail")
        with mock.patch.object(contract, "CONTRACT", (wrong,)):
            bindings = dict(contract.answers_bound_to_their_source())
        self.assertEqual(bindings["running"], contract.UNBOUND)

    def test_declared_constants_are_not_required_to_import_anything(self):
        kinds = contract.source_kinds()
        self.assertIn(contract.DECLARED, kinds)
        self.assertIn("identity", kinds[contract.DECLARED])


class Section41SourcesAreClassified(unittest.TestCase):
    """*"operational state must derive from current authoritative sources"*."""

    def test_operational_answers_read_authoritative_sources(self):
        by_answer = {c.answered_by: c for c in contract.CONTRACT}
        for name in ("capabilities", "running", "failed", "changed"):
            with self.subTest(name):
                self.assertEqual(by_answer[name].source_kind,
                                 contract.AUTHORITATIVE)

    def test_no_answer_reads_a_projection_over_sources(self):
        """W2 is a projection; `§41` names sources."""
        kinds = {c.source_kind for c in contract.CONTRACT}
        self.assertNotIn(contract.PROJECTION, kinds)

    def test_unknowns_is_the_only_internally_derived_answer(self):
        internal = [c.answered_by for c in contract.CONTRACT
                    if c.source_kind == contract.DERIVED_INTERNALLY]
        self.assertEqual(internal, ["unknowns"])


class ProjectionFreshnessIsNotSourceFreshness(unittest.TestCase):
    """`ACT §10` — the distinction a re-derived projection cannot establish."""

    def test_the_two_are_measured_separately(self):
        result = contract.projection_freshness_is_not_source_freshness()
        self.assertIn("projection_observed_at", result)
        self.assertIn("source_live", result)
        self.assertIn("source_stale_or_terminated", result)

    def test_the_live_corpus_demonstrates_the_distinction(self):
        result = contract.projection_freshness_is_not_source_freshness()
        self.assertTrue(
            result["distinct"],
            "the projection should report CURRENT while underlying "
            "observations are stale or terminated")
        self.assertGreater(result["source_stale_or_terminated"], 0)
        self.assertEqual(result["source_live"], 0)

    def test_a_fresh_projection_does_not_imply_a_live_source(self):
        result = contract.projection_freshness_is_not_source_freshness()
        self.assertEqual(result["projection_status"], "CURRENT")
        self.assertEqual(result["source_live"], 0,
                         "a self-model inferring source freshness from "
                         "projection freshness would report a stopped world "
                         "as live")


class TheSelfModelIsNotAuthority(unittest.TestCase):
    """`§18`: `SELF-MODEL ≠ AUTHORITY`. `§40`: no field may create authority."""

    def test_no_function_creates_authority_by_naming_it(self):
        result = contract.self_model_is_not_authority()
        self.assertEqual(result["authority_creating_functions"], ())

    def test_the_authority_answer_represents_rather_than_grants(self):
        from tools import p12_self_model as model
        answer = model.authority()
        self.assertIsNotNone(answer.value)
        self.assertIn("founder_reserved", answer.value)

    def test_the_check_detects_an_authority_creating_function(self):
        import ast
        planted = ast.parse("def authorize_everything():\n    return True\n")
        with mock.patch("ast.parse", return_value=planted):
            result = contract.self_model_is_not_authority()
        self.assertIn("authorize_everything",
                      result["authority_creating_functions"])


if __name__ == "__main__":
    unittest.main()
