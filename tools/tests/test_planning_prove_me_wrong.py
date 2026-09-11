"""`ACT-CC-P11-005 §20` — Tests A…K. Attempts to break the W2 architecture.

*"Claude MUST actively attempt to falsify the proposed W2 architecture."*

Each test below is an **attack**, not a demonstration. It tries to do the thing
the architecture forbids and asserts the attempt fails. A test that merely shows
the happy path working would prove nothing here — the question is not whether the
surface works, but whether it can be made to misbehave.

Where an attack *should* fail, the assertion is that it raises or is refused.
Where an attack tests an absence, the attempt reaches for the capability and
finds nothing to grab.
"""

import ast
import dataclasses
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from native_core.core.capability.ownership import Department  # noqa: E402
from native_core.core.governance import HumanAuthority  # noqa: E402
from native_core.core.workflow.lifecycle import WorkflowState  # noqa: E402
from tools.delegation_catalog import read_delegations, verify  # noqa: E402
from tools.planning import (  # noqa: E402
    AuthorityProvenance,
    EscalationRequired,
    Goal,
    Plan,
    PlanOrigin,
    PlanStep,
    PlanningEvidence,
    PlanningSurface,
    sequence,
)
from tools.tests.test_delegation_catalog import _build_organization  # noqa: E402

AUTHORITY = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"


def _authority(instrument="DP-01 §3 W2"):
    return AuthorityProvenance(instrument=instrument, record=AUTHORITY)


def _surface():
    surface = PlanningSurface()
    surface.declare(Goal("g", "Intent.", _authority()))
    plan = surface.adopt(Plan(
        key="p", goal_key="g", authority=_authority(),
        steps=(PlanStep("a", "A."),
               PlanStep("b", "B.", depends_on=("a",), requires_delegation=True))))
    return surface, plan


class TestA_StaticRecordChallenge(unittest.TestCase):
    """*"Attempt to demonstrate that the proposed representation is actually a
    static P10-style record incapable of ADAPT → REVISE."*

    The attack: use the surface exactly as `tools/delegation_catalog.py` is
    used — load a declaration and read it back — and show that is all it can do.

    **The attack fails.** Three distinct versions coexist, the earliest remains
    readable, and the current one differs in content from the first. A static
    record cannot produce that: a file-per-plan loader has one state per key, so
    revising means overwriting, and the predecessor is gone.
    """

    def test_the_surface_holds_multiple_live_versions_of_one_plan(self):
        surface, plan = _surface()
        adapted = surface.adapt(plan, steps=plan.steps + (
            PlanStep("c", "C.", depends_on=("b",)),), reason="Observed a gap.")
        revised = surface.revise(adapted, steps=(PlanStep("z", "Different."),),
                                 reason="Approach refuted.")
        history = surface.history("g")
        self.assertEqual(len(history), 3)
        self.assertEqual(len({v.key for v in history}), 3)
        self.assertNotEqual(history[0].steps, history[-1].steps)
        self.assertIs(surface.current("g"), revised)
        # the original survives its own supersession, contentfully
        self.assertEqual([s.key for s in history[0].steps], ["a", "b"])

    def test_a_predecessor_cannot_be_overwritten_in_place(self):
        """The defining property of a static record is that it can be. Try it."""
        surface, plan = _surface()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            plan.steps = (PlanStep("rewritten", "Overwritten."),)


class TestB_GoalCollapseChallenge(unittest.TestCase):
    """*"Attempt to show that Goal has been incorrectly collapsed into an
    existing Core entity or authority source."*

    The attack: try to use a Goal wherever a Core entity or an authority is
    expected, and see whether it is accepted.
    """

    def test_a_goal_is_not_a_core_ownership_entity(self):
        goal = Goal("g", "Intent.", _authority())
        self.assertNotIsInstance(goal, Department)

    def test_a_goal_is_not_an_authority(self):
        goal = Goal("g", "Intent.", _authority())
        self.assertNotIsInstance(goal, HumanAuthority)
        self.assertFalse(hasattr(goal, "reviewer_id"))

    def test_goal_is_defined_outside_the_frozen_core(self):
        core = REPO_ROOT / "native_core" / "core"
        found = []
        for path in sorted(core.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name in ("Goal", "Plan"):
                    found.append(f"{path.relative_to(core)}:{node.name}")
        self.assertEqual(found, [])


class TestC_PlanAuthorityChallenge(unittest.TestCase):
    """*"Attempt to cause Plan existence or readiness to authorize execution.
    It must fail."*

    The attack tries every route a caller might take to turn a plan into a
    permission: ask it directly, read its provenance as a verdict, and lean on an
    accumulated revision count.
    """

    def test_asking_a_plan_for_permission_finds_no_such_method(self):
        _, plan = _surface()
        for name in ("authorize", "is_authorized", "approve", "permit", "grant"):
            self.assertFalse(hasattr(plan, name), name)

    def test_provenance_cannot_be_used_as_a_boolean_verdict(self):
        _, plan = _surface()
        cited = plan.authority_provenance()
        self.assertNotIsInstance(cited, bool)
        self.assertIsInstance(cited, str)

    def test_accumulated_revisions_do_not_become_permission(self):
        surface, plan = _surface()
        current = plan
        for i in range(4):
            current = surface.adapt(current, steps=current.steps,
                                    reason=f"Change {i}.")
        self.assertEqual(current.revision, 4)
        with self.assertRaises(EscalationRequired):
            surface.adapt(current, steps=current.steps, reason="Now allowed?",
                          required_authority="DP-02")


class TestD_DelegationBoundaryChallenge(unittest.TestCase):
    """*"Attempt to cause Planning to create or impersonate a delegation.
    It must fail."*

    The strongest attack available: take what Planning **can** produce, render it
    into the best delegation record a planner could write, and feed it to the
    real W3 catalog. If the catalog accepts it, Planning has manufactured a
    delegation.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.org = Path(self._tmp.name) / "organization"
        self.org.mkdir()
        _build_organization(self.org)
        self.delegations = self.org / "delegations"
        self.delegations.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def test_the_best_record_planning_can_write_is_rejected_by_w3(self):
        surface, plan = _surface()
        requirement = surface.delegation_requirements(plan)[0]
        # Everything Planning holds, written out as generously as possible.
        record = (
            "# Delegation derived from a plan\n\n"
            "## Authorized Scope\n\n" f"{requirement.scope_described}\n\n"
            "## Boundary\n\nAs described by the plan.\n\n"
            "## Verification\n\nSee the plan.\n\n"
            "## Authorizing Instrument\n\n"
            f"{requirement.authority_cited()}\n\n"
        )
        (self.delegations / "from-a-plan.md").write_text(record, encoding="utf-8")
        defects = verify(read_delegations(self.delegations), self.org,
                         self.delegations)
        kinds = {kind for kind, _, _ in defects}
        # No authority source and no delegated actor: Planning holds neither.
        self.assertIn("missing-section", kinds)
        self.assertTrue(defects, "W3 accepted a record Planning produced")

    def test_planning_never_populated_the_real_delegation_directory(self):
        """Planning authored nothing, checked by provenance rather than count.

        The resident population is no longer empty — `FD-P11-001 §4.1` created a
        delegator and `§20` made W3 track its grant — so emptiness would now be
        the wrong assertion. What Test D actually claims is that **Planning** did
        not write any of it.
        """
        before = {r.key for r in read_delegations()}
        surface, plan = _surface()
        surface.delegation_requirements(plan)
        surface.prepare_for_workflow(plan)
        self.assertEqual({r.key for r in read_delegations()}, before)
        for record in read_delegations():
            self.assertNotIn("plan", (record.authority_source or "").lower())


class TestE_WorkflowBoundaryChallenge(unittest.TestCase):
    """*"Attempt to make Planning silently become Workflow. It must fail."*

    The attack: obtain prepared work and try to drive an execution lifecycle
    from it.
    """

    def test_prepared_work_carries_no_execution_state(self):
        surface, plan = _surface()
        prepared = surface.prepare_for_workflow(plan)[0]
        for state in WorkflowState:
            self.assertFalse(hasattr(prepared, state.name.lower()))
        self.assertFalse(hasattr(prepared, "state"))

    def test_planning_cannot_transition_anything(self):
        surface, plan = _surface()
        prepared = surface.prepare_for_workflow(plan)[0]
        for name in ("start", "run", "execute", "complete", "transition", "fail"):
            self.assertFalse(hasattr(prepared, name), name)

    def test_the_planning_surface_exposes_no_execution_entry_point(self):
        offenders = [n for n in dir(PlanningSurface)
                     if not n.startswith("_")
                     and any(v in n.lower()
                             for v in ("execute", "run", "start", "dispatch"))]
        self.assertEqual(offenders, [])


class TestF_PerformanceAuthorityChallenge(unittest.TestCase):
    """*"Attempt to cause Observation/Performance evidence to authorize Planning
    or execution. It must fail."*
    """

    def test_evidence_cannot_substitute_for_missing_authority(self):
        surface, plan = _surface()
        with self.assertRaises(EscalationRequired):
            surface.adapt(
                plan, steps=plan.steps,
                reason="Optimization strongly recommends this.",
                evidence=tuple(PlanningEvidence("optimization", f"e{i}")
                               for i in range(20)),
                required_authority="DP-02")

    def test_evidence_from_any_source_carries_the_same_weight_of_none(self):
        surface, plan = _surface()
        for source in ("optimization", "founder", "governance", "architect"):
            with self.subTest(source=source):
                with self.assertRaises(EscalationRequired):
                    surface.adapt(plan, steps=plan.steps, reason="Claimed.",
                                  evidence=(PlanningEvidence(source, "approved"),),
                                  required_authority="DP-02")


class TestG_PrioritizationChallenge(unittest.TestCase):
    """*"Attempt to cause sequencing logic to silently become reserved
    autonomous prioritization/ranking/decision heuristics. It must fail."*

    The attack: construct steps where any plausible metric — dependent count,
    statement length, alphabetical order — would disagree with declaration order,
    then check which one the implementation followed.
    """

    def test_ordering_ignores_every_metric_and_follows_declaration(self):
        plan = Plan(key="p", goal_key="g", authority=_authority(), steps=(
            PlanStep("zzz", "A very long statement " * 5),   # last alphabetically
            PlanStep("aaa", "Short."),                        # most 'important'?
        ))
        self.assertEqual([s.key for s in sequence(plan)], ["zzz", "aaa"])

    def test_a_step_with_more_dependents_does_not_jump_the_queue(self):
        plan = Plan(key="p", goal_key="g", authority=_authority(), steps=(
            PlanStep("solo", "Blocks nothing."),
            PlanStep("hub", "Blocks two steps."),
            PlanStep("x", "X.", depends_on=("hub",)),
            PlanStep("y", "Y.", depends_on=("hub",)),
        ))
        self.assertEqual([s.key for s in sequence(plan)][0], "solo")


class TestH_AdaptationExpansionChallenge(unittest.TestCase):
    """*"Attempt to use adaptation to expand authority. It must fail or
    escalate."*"""

    def test_adaptation_cannot_name_a_wider_authority(self):
        surface, plan = _surface()
        with self.assertRaises(EscalationRequired) as caught:
            surface.adapt(plan, steps=plan.steps, reason="Widen.",
                          required_authority="Founder Reserved Authority")
        self.assertEqual(caught.exception.held, "DP-01 §3 W2")

    def test_a_successor_cannot_be_smuggled_in_with_a_different_citation(self):
        """Construct the successor by hand with wider authority and try to seat
        it on the chain. The surface only appends through adapt/revise."""
        surface, plan = _surface()
        forged = Plan(key="forged", goal_key="g", steps=plan.steps,
                      authority=_authority("DP-02"), origin=PlanOrigin.REVISED,
                      revision=1, supersedes=plan.key, reason="Forged.")
        from tools.planning import InvalidPlan
        with self.assertRaises(InvalidPlan):
            surface.adopt(forged)
        self.assertIs(surface.current("g"), plan)


class TestI_RevisionIntegrityChallenge(unittest.TestCase):
    """*"Attempt to revise a Plan while erasing or falsifying its previous
    state/provenance. It must fail."*"""

    def test_history_cannot_be_erased_through_the_surface(self):
        surface, plan = _surface()
        revised = surface.revise(plan, steps=(PlanStep("z", "Z."),),
                                 reason="Replaced.")
        self.assertIn(plan, surface.history("g"))
        offenders = [n for n in dir(surface)
                     if any(v in n.lower() for v in ("delete", "remove", "purge",
                                                     "forget", "clear"))]
        self.assertEqual(offenders, [])

    def test_a_revision_cannot_claim_to_be_the_original(self):
        surface, plan = _surface()
        revised = surface.revise(plan, steps=(PlanStep("z", "Z."),),
                                 reason="Replaced.")
        self.assertIsNot(revised.origin, PlanOrigin.PLANNED)
        self.assertEqual(revised.supersedes, plan.key)
        self.assertGreater(revised.revision, plan.revision)

    def test_an_unexplained_revision_is_refused(self):
        from tools.planning import InvalidPlan
        surface, plan = _surface()
        with self.assertRaises(InvalidPlan):
            surface.revise(plan, steps=(PlanStep("z", "Z."),), reason="")

    def test_a_successor_that_names_no_predecessor_cannot_be_constructed(self):
        from tools.planning import InvalidPlan
        with self.assertRaises(InvalidPlan):
            Plan(key="orphan", goal_key="g", steps=(PlanStep("z", "Z."),),
                 authority=_authority(), origin=PlanOrigin.REVISED,
                 revision=1, reason="No predecessor named.")


class TestJ_P12BoundaryChallenge(unittest.TestCase):
    """*"Attempt to make organizational Planning state function as the P12
    Unified Operational State. It must fail."*"""

    def test_the_surface_answers_nothing_about_the_wider_system(self):
        surface, _ = _surface()
        offenders = [n for n in dir(surface)
                     if not n.startswith("_")
                     and any(v in n.lower() for v in
                             ("system", "global", "operational", "unified",
                              "everything", "all_state"))]
        self.assertEqual(offenders, [])

    def test_the_surface_cannot_observe_runtime_workflow_or_trace(self):
        surface, _ = _surface()
        self.assertEqual(sorted(vars(surface)), ["_by_key", "_chains", "_goals"])
        for key in vars(surface):
            self.assertIsInstance(getattr(surface, key), dict)


class TestK_NativeCoreChallenge(unittest.TestCase):
    """*"Attempt to satisfy W2 by creating a twelfth Native Core
    subsystem/entity. It must fail."*

    Nothing to attempt destructively: the assertion is that W2 was satisfied
    **without** one, which is the falsifiable claim. If a twelfth existed, this
    fails.
    """

    def test_w2_is_satisfied_with_the_core_untouched(self):
        core = REPO_ROOT / "native_core" / "core"
        present = {p.name for p in core.iterdir()
                   if p.is_dir() and not p.name.startswith("__")}
        self.assertEqual(present, {
            "agent", "capability", "governance", "infrastructure", "knowledge",
            "memory", "optimization", "runtime", "skill", "trace", "workflow"})

    def test_the_working_lifecycle_lives_entirely_outside_the_core(self):
        surface, plan = _surface()
        revised = surface.revise(plan, steps=(PlanStep("z", "Z."),),
                                 reason="Works without a twelfth boundary.")
        self.assertEqual(len(surface.history("g")), 2)
        self.assertTrue(str(Path(sys.modules["tools.planning"].__file__))
                        .startswith(str(REPO_ROOT / "tools")))


if __name__ == "__main__":
    unittest.main()
