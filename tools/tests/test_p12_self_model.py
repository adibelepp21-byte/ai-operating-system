"""P12-W5 self-model conformance.

The controls that matter here are not that the answers are *present* — that is
easy and was briefly true while two of them were empty or mislabelled. They are
that an absent source produces `UNKNOWN`, that no answer confers authority, and
that the model's account of its own ignorance is derived rather than asserted.
"""

from __future__ import annotations

import unittest

from tools import p12_self_model as model
from tools.derived_views import INFERRED, UNKNOWN, VERIFIED


#: Built once. The module recomputes from source on every call **by design** —
#: that is what keeps it a representation rather than a cache — but seventeen
#: rebuilds of the whole governance index cost 100s of suite time to re-verify
#: a value that cannot change mid-run. The design is the module's; the
#: repetition was the test's.
_MODEL = None


def _model():
    global _MODEL
    if _MODEL is None:
        _MODEL = model.self_model()
    return _MODEL


def _answer(question):
    return next(a for a in _model() if a.question == question)


class TheTwelveQuestions(unittest.TestCase):
    def test_the_decision_lists_twelve_and_the_model_answers_twelve(self):
        self.assertEqual(len(model.QUESTIONS), 12)
        self.assertEqual(len(_model()), 12)

    def test_answers_arrive_in_the_order_section_18_lists_them(self):
        self.assertEqual(
            tuple(a.question for a in _model()), model.QUESTIONS,
            "§18 order is part of the citation; a reader must be able to read down",
        )

    def test_every_answer_names_its_source(self):
        for answer in _model():
            self.assertTrue(
                answer.source.strip(),
                f"{answer.question} carries no source",
            )

    def test_every_status_is_one_of_the_three(self):
        for answer in _model():
            self.assertIn(answer.status, (VERIFIED, INFERRED, UNKNOWN))


class UnknownIsPreserved(unittest.TestCase):
    """`§23`: MEASUREMENT ≠ PREDICTION. An absent source must not be filled in."""

    def test_runtime_questions_are_unknown_not_guessed(self):
        for question in ("What is running?", "What failed?"):
            answer = _answer(question)
            self.assertEqual(answer.status, UNKNOWN)
            self.assertIsNone(answer.value)

    def test_an_unknown_answer_still_names_the_absent_source(self):
        answer = _answer("What is running?")
        self.assertTrue(
            answer.source.strip(),
            "an UNKNOWN that does not say why is indistinguishable from a bug",
        )

    def test_the_ignorance_list_is_derived_not_asserted(self):
        """A hand-kept list of one's own unknowns is the first thing to go stale."""
        answer = _answer("What do I not know?")
        measured = tuple(
            a.question for a in _model()
            if a.status == UNKNOWN and a.question != "What do I not know?"
        )
        self.assertEqual(tuple(answer.value["unanswered_questions"]), measured)
        self.assertEqual(answer.value["count"], len(measured))


class SelfModelIsNotAuthority(unittest.TestCase):
    """`§18`: SELF-MODEL ≠ AUTHORITY, and it may not self-authorize."""

    def test_authority_answer_reports_holders_and_grants_the_caller_nothing(self):
        answer = _answer("What authority do I have?")
        self.assertIsNone(
            answer.value["self_model_authority"],
            "the model must not report authority of its own",
        )
        self.assertIn("founder_reserved", answer.value)
        self.assertIn("architect_reserved", answer.value)

    def test_reserved_matters_are_reported_as_reserved_not_resolved(self):
        answer = _answer("What authority do I have?")
        reserved = answer.value["founder_reserved"] + answer.value["architect_reserved"]
        for matter in ("FDP-P10-001 Security", "FDP-P10-003 Governance",
                       "ADP-P10-001 entity semantics"):
            self.assertIn(matter, reserved)

    def test_no_answer_returns_a_permission(self):
        for answer in _model():
            rendered = repr(answer.value).lower()
            for word in ("authorized: true", "permitted: true", "may_proceed"):
                self.assertNotIn(word, rendered)


class AnswersAreAnchoredInRealSources(unittest.TestCase):
    """Each regression here was an actual defect in this module, not a hypothetical."""

    def test_capabilities_are_discovered_not_empty(self):
        """It reported INFERRED over an empty tuple: the repo root was passed
        where the organization root was wanted, so it found nothing and did not
        raise."""
        answer = _answer("What capabilities exist?")
        self.assertEqual(answer.status, INFERRED)
        self.assertGreater(answer.value["count"], 0)
        self.assertIn("engineering-intelligence", answer.value["declared"])

    def test_an_empty_department_set_would_be_unknown_not_inferred(self):
        from unittest import mock
        with mock.patch("tools.organization_catalog.read_departments", return_value=[]):
            answer = model.capabilities()
        self.assertEqual(answer.status, UNKNOWN)
        self.assertIsNone(answer.value)

    def test_change_reports_supersession_not_the_staleness_list(self):
        """It first relabelled the open-synchronization list as
        'recorded_supersessions' — a label describing what the data was not."""
        changed = _answer("What changed?")
        stale = _answer("What is stale?")
        self.assertIsInstance(changed.value["recorded_supersessions"], int)
        self.assertNotEqual(changed.value, stale.value)

    def test_identity_is_structural_not_self_described(self):
        answer = _answer("What am I?")
        self.assertEqual(answer.value["native_core_boundaries"], 11)
        self.assertEqual(len(answer.value["boundaries"]), 11)

    def test_the_founder_decisions_that_govern_this_phase_are_visible(self):
        """F-2: DP-01 and DP-02 were registered and invisible. If this regresses,
        the system cannot see the instruments that authorize it."""
        answer = _answer("What decisions are recorded?")
        identifiers = answer.value["identifiers"]
        for decision in ("DP-01", "DP-02", "FD-P11-001", "FD-P11-002", "FD-P10-005"):
            self.assertIn(decision, identifiers)


class CoverageIsMeasured(unittest.TestCase):
    def test_coverage_sums_to_the_question_count(self):
        c = model.coverage()
        self.assertEqual(c["verified"] + c["inferred"] + c["unknown"], c["questions"])
        self.assertEqual(c["questions"], 12)

    def test_coverage_does_not_claim_the_unknowns_are_answered(self):
        self.assertGreaterEqual(model.coverage()["unknown"], 2)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
