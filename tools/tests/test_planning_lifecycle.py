"""`P11-W2` lifecycle — `PLAN → SEQUENCE → ADAPT → REVISE`, demonstrated.

`ACT-CC-P11-005 §9`: *"The central W2 test is whether the implementation can
genuinely perform PLAN → SEQUENCE → ADAPT → REVISE, not merely store four
labels."* These tests are that demonstration; `test_planning_negative_controls`
holds the constraints.
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.planning import (  # noqa: E402
    AdaptationClass,
    AuthorityProvenance,
    EscalationRequired,
    Goal,
    InvalidPlan,
    Plan,
    PlanOrigin,
    PlanStep,
    PlanningEvidence,
    PlanningSurface,
    UnsequenceablePlan,
    classify_adaptation,
    sequence,
)

#: A real resolvable instrument. `AuthorityProvenance` refuses a citation that
#: points at nothing, so tests must cite something that exists — which is the
#: rule under test, not a fixture convenience.
AUTHORITY = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"


def _authority(instrument="DP-01 §3 W2"):
    return AuthorityProvenance(instrument=instrument, record=AUTHORITY)


def _goal(key="close-w2"):
    return Goal(key=key, statement="Construct the W2 planning surface.",
                authority=_authority())


def _plan(key="p1", goal_key="close-w2", steps=None):
    steps = steps or (
        PlanStep("design", "Design the planning surface."),
        PlanStep("build", "Implement it.", depends_on=("design",)),
        PlanStep("verify", "Verify it.", depends_on=("build",)),
    )
    return Plan(key=key, goal_key=goal_key, steps=steps, authority=_authority())


class ThePlanStepOfTheLifecycle(unittest.TestCase):
    """`PLAN` — *"A valid organizational objective can be represented as a plan."*"""

    def test_a_goal_is_declared_and_decomposed_into_a_plan(self):
        surface = PlanningSurface()
        surface.declare(_goal())
        plan = surface.adopt(_plan())
        self.assertEqual(plan.goal_key, "close-w2")
        self.assertEqual(len(plan.steps), 3)
        self.assertIs(plan.origin, PlanOrigin.PLANNED)
        self.assertEqual(plan.revision, 0)
        self.assertIsNone(plan.supersedes)

    def test_a_plan_for_an_undeclared_goal_is_refused(self):
        surface = PlanningSurface()
        with self.assertRaises(InvalidPlan):
            surface.adopt(_plan(goal_key="never-declared"))

    def test_a_second_plan_cannot_quietly_replace_the_first(self):
        """Replacement goes through revise(), which preserves what it replaces."""
        surface = PlanningSurface()
        surface.declare(_goal())
        surface.adopt(_plan())
        with self.assertRaises(InvalidPlan):
            surface.adopt(_plan(key="p2"))


class TheSequenceStepOfTheLifecycle(unittest.TestCase):
    """`SEQUENCE` — *"Plan elements can be ordered or dependency-related
    sufficiently for execution preparation."*"""

    def test_steps_are_ordered_by_declared_dependencies(self):
        plan = _plan(steps=(
            PlanStep("verify", "Verify.", depends_on=("build",)),
            PlanStep("build", "Build.", depends_on=("design",)),
            PlanStep("design", "Design."),
        ))
        self.assertEqual([s.key for s in sequence(plan)],
                         ["design", "build", "verify"])

    def test_independent_steps_keep_the_order_the_author_declared(self):
        """The tie-break is declaration order — the boundary against ranking.

        If this ever returns a different order, something computed a preference,
        and that is the reserved prioritization frontier.
        """
        plan = _plan(steps=(
            PlanStep("zebra", "First declared."),
            PlanStep("alpha", "Second declared."),
        ))
        self.assertEqual([s.key for s in sequence(plan)], ["zebra", "alpha"])

    def test_a_dependency_cycle_is_refused_rather_than_resolved(self):
        with self.assertRaises(UnsequenceablePlan):
            sequence(_plan(steps=(
                PlanStep("a", "A.", depends_on=("b",)),
                PlanStep("b", "B.", depends_on=("a",)),
            )))

    def test_a_dependency_on_an_unknown_step_is_refused(self):
        with self.assertRaises(UnsequenceablePlan):
            sequence(_plan(steps=(PlanStep("a", "A.", depends_on=("ghost",)),)))


class TheAdaptStepOfTheLifecycle(unittest.TestCase):
    """`ADAPT` — *"Observed information can cause a legitimate plan adjustment."*"""

    def setUp(self):
        self.surface = PlanningSurface()
        self.surface.declare(_goal())
        self.original = self.surface.adopt(_plan())

    def test_observation_causes_a_real_change_to_the_current_plan(self):
        adapted = self.surface.adapt(
            self.original,
            steps=self.original.steps + (
                PlanStep("recheck", "Re-verify after the observation.",
                         depends_on=("verify",)),),
            reason="Observation showed verification was incomplete.",
            evidence=(PlanningEvidence("optimization", "coverage gap detected"),),
        )
        self.assertIs(adapted.origin, PlanOrigin.ADAPTED)
        self.assertEqual(adapted.revision, 1)
        self.assertEqual(adapted.supersedes, self.original.key)
        self.assertEqual(len(adapted.steps), 4)
        self.assertIs(self.surface.current("close-w2"), adapted)

    def test_the_evidence_that_motivated_the_change_is_retained(self):
        adapted = self.surface.adapt(
            self.original, steps=self.original.steps,
            reason="Narrowed after observation.",
            evidence=(PlanningEvidence("optimization", "step 2 is redundant"),))
        self.assertEqual(adapted.evidence,
                         ("optimization: step 2 is redundant",))

    def test_adaptation_carries_the_original_authority_unchanged(self):
        adapted = self.surface.adapt(self.original, steps=self.original.steps,
                                     reason="Adjusted.")
        self.assertEqual(adapted.authority, self.original.authority)

    def test_an_unexplained_adaptation_is_refused(self):
        with self.assertRaises(InvalidPlan):
            self.surface.adapt(self.original, steps=self.original.steps, reason="  ")


class TheReviseStepOfTheLifecycle(unittest.TestCase):
    """`REVISE` — *"A plan can be revised without falsely presenting the previous
    plan as if it remained the current plan."*"""

    def setUp(self):
        self.surface = PlanningSurface()
        self.surface.declare(_goal())
        self.original = self.surface.adopt(_plan())

    def test_revision_produces_a_successor_and_retains_the_original(self):
        revised = self.surface.revise(
            self.original,
            steps=(PlanStep("rebuild", "Start over with a different approach."),),
            reason="The original approach was refuted.")
        self.assertIs(revised.origin, PlanOrigin.REVISED)
        self.assertIs(self.surface.current("close-w2"), revised)
        self.assertIn(self.original, self.surface.history("close-w2"))
        self.assertEqual(self.surface.superseded("close-w2"), (self.original,))

    def test_the_original_is_not_mutated_by_being_superseded(self):
        """Supersession is derived from the chain, never written onto the record."""
        before = (self.original.key, self.original.steps, self.original.origin,
                  self.original.revision, self.original.supersedes)
        self.surface.revise(self.original, steps=self.original.steps,
                            reason="Changed course.")
        after = (self.original.key, self.original.steps, self.original.origin,
                 self.original.revision, self.original.supersedes)
        self.assertEqual(before, after)
        self.assertTrue(self.surface.is_superseded(self.original))

    def test_the_current_plan_is_distinguishable_from_the_original(self):
        revised = self.surface.revise(self.original, steps=self.original.steps,
                                      reason="Changed course.")
        self.assertNotEqual(revised.key, self.original.key)
        self.assertFalse(self.surface.is_superseded(revised))
        self.assertTrue(self.surface.is_superseded(self.original))

    def test_a_superseded_version_cannot_be_revised_again(self):
        """Otherwise history forks and 'the current plan' stops being one thing."""
        self.surface.revise(self.original, steps=self.original.steps,
                            reason="First revision.")
        with self.assertRaises(InvalidPlan):
            self.surface.revise(self.original, steps=self.original.steps,
                                reason="Rewriting the past.")

    def test_the_full_chain_is_readable_in_order(self):
        second = self.surface.revise(self.original, steps=self.original.steps,
                                     reason="Second.")
        third = self.surface.adapt(second, steps=second.steps, reason="Third.")
        self.assertEqual([p.key for p in self.surface.history("close-w2")],
                         [self.original.key, second.key, third.key])
        self.assertEqual([p.revision for p in self.surface.history("close-w2")],
                         [0, 1, 2])


class TheLifecycleIsNotAStaticRecord(unittest.TestCase):
    """`ACT-CC-P11-005 §20` Test A, as a standing test rather than a one-off.

    `DP-03 §8.4`: a Plan is *"not constrained to the semantics of a static
    declaration loaded once."* A static record would fail here by being unable
    to produce a different current state after adaptation.
    """

    def test_a_plan_evolves_through_all_four_lifecycle_operations(self):
        surface = PlanningSurface()
        surface.declare(_goal())
        plan = surface.adopt(_plan())                                  # PLAN
        self.assertEqual([s.key for s in sequence(plan)],              # SEQUENCE
                         ["design", "build", "verify"])
        adapted = surface.adapt(                                       # ADAPT
            plan, steps=plan.steps + (PlanStep("extra", "Added.",
                                               depends_on=("verify",)),),
            reason="Observation required an extra step.",
            evidence=(PlanningEvidence("optimization", "gap"),))
        revised = surface.revise(                                      # REVISE
            adapted, steps=(PlanStep("restart", "Different approach."),),
            reason="Approach refuted.")
        self.assertEqual(len(surface.history("close-w2")), 3)
        self.assertIs(surface.current("close-w2"), revised)
        self.assertNotEqual(revised.steps, plan.steps)
        self.assertEqual([s.key for s in sequence(revised)], ["restart"])


class EscalationRatherThanExpansion(unittest.TestCase):
    """`ACT-CC-P11-005 §15` — ``DETECT → CLASSIFY → ESCALATE``."""

    def setUp(self):
        self.surface = PlanningSurface()
        self.surface.declare(_goal())
        self.plan = self.surface.adopt(_plan())

    def test_classification_happens_without_performing_the_change(self):
        self.assertIs(classify_adaptation(self.plan, None),
                      AdaptationClass.WITHIN_AUTHORITY)
        self.assertIs(classify_adaptation(self.plan, "DP-02"),
                      AdaptationClass.REQUIRES_ESCALATION)
        self.assertEqual(len(self.surface.history("close-w2")), 1)

    def test_an_adaptation_needing_other_authority_escalates(self):
        with self.assertRaises(EscalationRequired) as caught:
            self.surface.adapt(self.plan, steps=self.plan.steps,
                               reason="Needs more.", required_authority="DP-02")
        self.assertEqual(caught.exception.required, "DP-02")
        self.assertEqual(caught.exception.held, "DP-01 §3 W2")

    def test_an_escalated_change_does_not_partially_apply(self):
        """Fail closed: the chain is untouched, not left half-advanced."""
        with self.assertRaises(EscalationRequired):
            self.surface.revise(self.plan, steps=(PlanStep("x", "X."),),
                                reason="Needs more.", required_authority="DP-02")
        self.assertEqual(len(self.surface.history("close-w2")), 1)
        self.assertIs(self.surface.current("close-w2"), self.plan)


if __name__ == "__main__":
    unittest.main()
