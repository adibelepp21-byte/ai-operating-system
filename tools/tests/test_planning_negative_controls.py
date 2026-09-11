"""`ACT-CC-P11-005 §19` — NC-W2-01…24, structural negative controls for W2.

`§19`: *"Tests must constrain actual behavior. A test that merely searches its
own source text or asserts a string that it itself contains is not valid
structural coverage."*

That instruction names a defect I made and recorded two Acts ago: a test that
scanned its own source for a string its own assertion contained, which could
never pass and constrained nothing while reading as coverage. **No control below
inspects this file.** Each either exercises the surface and asserts what it
does, or parses the *planning package's* AST and asserts what it does not
contain.
"""

import ast
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from native_core.core.workflow.lifecycle import WorkflowState  # noqa: E402
from tools.delegation_catalog import read_delegations, verify  # noqa: E402
from tools.planning import (  # noqa: E402
    AuthorityProvenance,
    DelegationRequirement,
    WorkPreparation,
    EscalationRequired,
    Goal,
    InvalidGoal,
    InvalidPlan,
    Plan,
    PlanOrigin,
    PlanStep,
    PlanningEvidence,
    PlanningSurface,
    UnsequenceablePlan,
    sequence,
)

PACKAGE = REPO_ROOT / "tools" / "planning"
AUTHORITY = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"

#: Names that would mean this package had begun deciding permission.
#: ``authority_provenance`` is *not* one: it returns a citation string, and the
#: distinction between citing an authority and granting one is the distinction
#: this whole package is built on.
PERMISSION_VERBS = ("authorize", "authorise", "is_authorized", "is_authorised",
                    "grant", "approve", "permit", "self_authorize")

#: Fields whose presence would *be* the reserved prioritization frontier —
#: something must set them, and whatever sets them is judging what matters.
RANKING_FIELDS = ("priority", "score", "rank", "ranking", "weight", "urgency",
                  "importance", "value")


def _package_trees():
    for path in sorted(PACKAGE.glob("*.py")):
        yield path, ast.parse(path.read_text(encoding="utf-8"))


def _defined_names():
    names = []
    for path, tree in _package_trees():
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.ClassDef)):
                names.append((path.name, node.name))
    return names


def _annotated_fields():
    fields = []
    for path, tree in _package_trees():
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.AnnAssign) and isinstance(
                            item.target, ast.Name):
                        fields.append((node.name, item.target.id))
    return fields


def _imported_modules():
    names = set()
    for _, tree in _package_trees():
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module)
    return names


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


class NC_W2_01_GoalCannotSelfAuthorize(unittest.TestCase):
    def test_a_goal_citing_an_instrument_that_does_not_exist_is_refused(self):
        with self.assertRaises(InvalidGoal):
            Goal("g", "Intent.",
                 AuthorityProvenance("DP-99", "docs/does-not-exist.md"))

    def test_a_goal_exposes_no_permission_method(self):
        self.assertEqual(
            [n for n in dir(Goal("g", "Intent.", _authority()))
             if any(v in n.lower() for v in PERMISSION_VERBS)], [])


class NC_W2_02_PlanCannotSelfAuthorize(unittest.TestCase):
    def test_a_plan_citing_an_instrument_that_does_not_exist_is_refused(self):
        with self.assertRaises(InvalidGoal):
            Plan(key="p", goal_key="g", steps=(PlanStep("a", "A."),),
                 authority=AuthorityProvenance("DP-99", "docs/nowhere.md"))

    def test_provenance_returns_a_citation_not_a_verdict(self):
        _, plan = _surface()
        cited = plan.authority_provenance()
        self.assertIsInstance(cited, str)
        self.assertNotIsInstance(cited, bool)
        self.assertIn("DP-01 §3 W2", cited)


class NC_W2_03_04_05_PlanCannotCreateAuthority(unittest.TestCase):
    """Founder, Architect and constitutional authority alike.

    All three collapse to one structural fact: **the package cannot reach the
    boundary that holds authority.** `native_core/core/governance` owns
    `HumanAuthority`, and nothing here imports it, so no code path in Planning
    can construct, supply, or stand in for a governed decision.
    """

    def test_planning_does_not_import_governance(self):
        self.assertEqual(
            [m for m in _imported_modules() if "governance" in m], [])

    def test_planning_defines_no_permission_granting_callable(self):
        offenders = [f"{f}:{n}" for f, n in _defined_names()
                     if any(v in n.lower() for v in PERMISSION_VERBS)]
        self.assertEqual(offenders, [])


class NC_W2_06_07_08_PlanningCannotDelegate(unittest.TestCase):
    """Delegation authority, delegator impersonation, and W3 population."""

    def test_a_delegation_requirement_has_no_delegator_field(self):
        fields = [f for cls, f in _annotated_fields()
                  if cls == "DelegationRequirement"]
        self.assertNotIn("delegator", fields)
        self.assertNotIn("authority_source", fields)
        self.assertEqual(sorted(fields),
                         ["authority", "plan_key", "scope_described",
                          "step_key"])

    def test_planning_refuses_to_render_a_delegation_record(self):
        _, plan = _surface()
        requirement = DelegationRequirement("p", "b", "B.", _authority())
        with self.assertRaises(NotImplementedError):
            requirement.as_delegation_record()

    def test_identifying_delegable_work_populates_nothing(self):
        surface, plan = _surface()
        requirements = surface.delegation_requirements(plan)
        self.assertEqual(len(requirements), 1)
        self.assertEqual(requirements[0].step_key, "b")
        # Planning populated nothing: no resident record names a plan as its
        # authority source. (The population is no longer empty — `FD-P11-001`
        # created a delegator — so the property is checked, not the count.)
        for record in read_delegations():
            self.assertNotEqual(record.authority_source, "p")
            self.assertNotIn("plan", (record.authority_source or "").lower())


class NC_W2_09_10_11_12_ObservationCannotAuthorize(unittest.TestCase):
    """Observation and Performance provide evidence, never permission."""

    def test_evidence_does_not_change_what_authority_is_required(self):
        surface, plan = _surface()
        with self.assertRaises(EscalationRequired):
            surface.adapt(plan, steps=plan.steps, reason="Observed.",
                          evidence=(PlanningEvidence("optimization", "x"),),
                          required_authority="DP-02")

    def test_more_evidence_does_not_accumulate_into_authorization(self):
        """Ten observations authorize exactly as much as zero: nothing."""
        surface, plan = _surface()
        many = tuple(PlanningEvidence("optimization", f"finding {i}")
                     for i in range(10))
        with self.assertRaises(EscalationRequired):
            surface.adapt(plan, steps=plan.steps, reason="Observed a lot.",
                          evidence=many, required_authority="DP-02")

    def test_evidence_is_recorded_as_motivation_only(self):
        surface, plan = _surface()
        adapted = surface.adapt(plan, steps=plan.steps, reason="Observed.",
                                evidence=(PlanningEvidence("optimization", "x"),))
        self.assertEqual(adapted.authority, plan.authority)
        self.assertEqual(adapted.evidence, ("optimization: x",))

    def test_planning_does_not_import_optimization(self):
        self.assertEqual(
            [m for m in _imported_modules() if "optimization" in m], [])


class NC_W2_25_AuthorityCannotBeForged(unittest.TestCase):
    """`ACT-CC-P11-007 §6` — forge authority provenance, by name.

    *"Each must fail wherever a validated authority provenance object is
    required. The test must demonstrate behavioral failure."*

    Every string below names a real authority in this programme, which is what
    makes them the right probes: a forgery that reads as nonsense proves
    nothing, while one that reads exactly like the genuine article is what a
    consumer would actually be fooled by. **Before `ACT-CC-P11-006`, all four
    were accepted at both handoff boundaries.**
    """

    FORGERIES = ("Founder Reserved Authority", "Architect Authority",
                 "Governance Authority", "System Authority")

    def test_no_named_authority_can_be_asserted_as_a_bare_string(self):
        for claim in self.FORGERIES:
            with self.subTest(claim=claim):
                with self.assertRaises(TypeError):
                    WorkPreparation(plan_key="p", step_key="s",
                                    statement="do it", authority=claim)
                with self.assertRaises(TypeError):
                    DelegationRequirement(plan_key="p", step_key="s",
                                          scope_described="anything",
                                          authority=claim)

    def test_a_forged_citation_cannot_be_smuggled_through_the_provenance_type(self):
        """The type is not a wrapper to launder a claim through.

        `AuthorityProvenance` requires a record that resolves, so naming a real
        authority while citing nothing is refused — the instrument must exist.
        """
        for claim in self.FORGERIES:
            with self.subTest(claim=claim):
                with self.assertRaises(InvalidGoal):
                    AuthorityProvenance(claim, "docs/no-such-instrument.md")

    def test_what_this_does_not_prevent_is_stated_rather_than_implied(self):
        """A citation to a *real* instrument is accepted even if that instrument
        grants nothing of the sort.

        Resolution proves the pointer is real. Whether the cited body authorizes
        the claim is a reading, and readings are human acts — the same limit
        `AuthorityProvenance` and the corpus auditor both state. Asserted here so
        the forgery controls above are not mistaken for more than they are.
        """
        overreaching = AuthorityProvenance("Founder Reserved Authority", AUTHORITY)
        self.assertIn("Founder Reserved Authority", overreaching.cited())


class NC_W2_13_PrioritizationRemainsReserved(unittest.TestCase):
    def test_no_planning_type_carries_a_ranking_field(self):
        offenders = [f"{cls}.{f}" for cls, f in _annotated_fields()
                     if f.lower() in RANKING_FIELDS]
        self.assertEqual(offenders, [])

    def test_no_callable_computes_a_ranking(self):
        offenders = [f"{f}:{n}" for f, n in _defined_names()
                     if any(w in n.lower() for w in
                            ("rank", "score", "prioriti", "heuristic", "weigh"))]
        self.assertEqual(offenders, [])

    def test_ordering_is_a_function_of_declaration_and_dependencies_alone(self):
        """Reversing declaration order reverses independent output. Nothing else
        could produce that, and no metric could preserve it."""
        first = Plan(key="x", goal_key="g", authority=_authority(),
                     steps=(PlanStep("m", "M."), PlanStep("n", "N.")))
        second = Plan(key="y", goal_key="g", authority=_authority(),
                      steps=(PlanStep("n", "N."), PlanStep("m", "M.")))
        self.assertEqual([s.key for s in sequence(first)], ["m", "n"])
        self.assertEqual([s.key for s in sequence(second)], ["n", "m"])


class NC_W2_14_15_ChangeCannotExpandAuthority(unittest.TestCase):
    def test_adapt_has_no_parameter_that_sets_authority(self):
        self.assertNotIn("authority",
                         PlanningSurface.adapt.__code__.co_varnames[
                             :PlanningSurface.adapt.__code__.co_argcount +
                             PlanningSurface.adapt.__code__.co_kwonlyargcount])

    def test_revise_has_no_parameter_that_sets_authority(self):
        self.assertNotIn("authority",
                         PlanningSurface.revise.__code__.co_varnames[
                             :PlanningSurface.revise.__code__.co_argcount +
                             PlanningSurface.revise.__code__.co_kwonlyargcount])

    def test_every_successor_carries_the_original_citation(self):
        surface, plan = _surface()
        adapted = surface.adapt(plan, steps=plan.steps, reason="One.")
        revised = surface.revise(adapted, steps=adapted.steps, reason="Two.")
        for version in surface.history("g"):
            self.assertEqual(version.authority, plan.authority)


class NC_W2_16_WorkflowRemainsDistinct(unittest.TestCase):
    def test_planning_and_workflow_vocabularies_do_not_intersect(self):
        planning = {origin.name for origin in PlanOrigin}
        workflow = {state.name for state in WorkflowState}
        self.assertEqual(planning & workflow, set())

    def test_planning_does_not_import_workflow(self):
        self.assertEqual([m for m in _imported_modules() if "workflow" in m], [])

    def test_prepared_work_cannot_be_started_by_planning(self):
        surface, plan = _surface()
        prepared = surface.prepare_for_workflow(plan)
        self.assertEqual(len(prepared), 2)
        for item in prepared:
            offenders = [n for n in dir(item)
                         if any(v in n.lower() for v in
                                ("start", "run", "execute", "transition",
                                 "complete"))]
            self.assertEqual(offenders, [], offenders)

    def test_prepared_work_carries_authority_provenance_forward(self):
        surface, plan = _surface()
        for item in surface.prepare_for_workflow(plan):
            self.assertIs(item.authority, plan.authority)
            self.assertIn("DP-01 §3 W2", item.authority_cited())

    def test_provenance_crosses_the_boundary_as_a_verified_citation(self):
        """The correction of `ACT-CC-P11-006 §17`'s finding.

        Both handoff types once carried the *formatted string* rather than the
        citation, so a consumer received text it could not verify and anyone
        could construct one saying whatever they liked. Passing the object costs
        no capability — it is frozen, with one method returning that same string
        — and buys the guarantee that the cited record resolves.
        """
        surface, plan = _surface()
        for item in surface.prepare_for_workflow(plan):
            self.assertIsInstance(item.authority, AuthorityProvenance)
        for item in surface.delegation_requirements(plan):
            self.assertIsInstance(item.authority, AuthorityProvenance)

    def test_a_citation_that_is_only_text_is_refused_at_both_boundaries(self):
        """Forgery, attempted directly. Before the fix, both of these
        succeeded and were indistinguishable from a genuine handoff."""
        with self.assertRaises(TypeError):
            WorkPreparation(plan_key="p", step_key="s", statement="x",
                            authority="Founder Reserved Authority")
        with self.assertRaises(TypeError):
            DelegationRequirement(plan_key="p", step_key="s",
                                  scope_described="x",
                                  authority="Constitutional Authority")


class NC_W2_17_DelegationRemainsDistinct(unittest.TestCase):
    def test_planning_does_not_import_the_delegation_catalog(self):
        self.assertEqual(
            [m for m in _imported_modules() if "delegation" in m], [])

    def test_a_requirement_is_not_a_delegation_record(self):
        surface, plan = _surface()
        requirement = surface.delegation_requirements(plan)[0]
        self.assertNotIsInstance(requirement, Plan)
        self.assertFalse(hasattr(requirement, "authority_source"))


class NC_W2_18_PlanningIsNotP12OperationalState(unittest.TestCase):
    """`ACT-CC-P11-005 §30`: ``P11 PLANNING STATE ≠ P12 UNIFIED OPERATIONAL STATE``."""

    def test_the_surface_holds_planning_state_only(self):
        surface, _ = _surface()
        self.assertEqual(sorted(vars(surface)), ["_by_key", "_chains", "_goals"])

    def test_the_surface_aggregates_no_other_subsystem(self):
        for module in _imported_modules():
            self.assertFalse(
                module.startswith("native_core"),
                f"planning reached into the core: {module}")


class NC_W2_19_NoTwelfthNativeCoreBoundary(unittest.TestCase):
    def test_the_core_still_holds_eleven_boundaries(self):
        core = REPO_ROOT / "native_core" / "core"
        present = {p.name for p in core.iterdir()
                   if p.is_dir() and not p.name.startswith("__")}
        self.assertEqual(len(present), 11, sorted(present))

    def test_the_planning_package_lives_outside_the_core(self):
        self.assertFalse((REPO_ROOT / "native_core" / "core" / "planning").exists())
        self.assertTrue(PACKAGE.is_dir())


class NC_W2_20_FailureCannotPresentAsCompletion(unittest.TestCase):
    def test_an_unsequenceable_plan_cannot_be_adopted(self):
        surface = PlanningSurface()
        surface.declare(Goal("g", "Intent.", _authority()))
        with self.assertRaises(UnsequenceablePlan):
            surface.adopt(Plan(key="p", goal_key="g", authority=_authority(),
                               steps=(PlanStep("a", "A.", depends_on=("b",)),
                                      PlanStep("b", "B.", depends_on=("a",)))))
        with self.assertRaises(InvalidPlan):
            surface.current("g")

    def test_a_failed_change_leaves_no_partial_successor(self):
        surface, plan = _surface()
        with self.assertRaises(EscalationRequired):
            surface.adapt(plan, steps=plan.steps, reason="Needs more.",
                          required_authority="DP-02")
        self.assertEqual(len(surface.history("g")), 1)
        self.assertIs(surface.current("g"), plan)


class NC_W2_21_EscalationCannotBecomeApproval(unittest.TestCase):
    def test_repeating_an_escalated_request_escalates_again(self):
        """`SILENCE ≠ APPROVAL`. Persistence is not consent."""
        surface, plan = _surface()
        for _ in range(3):
            with self.assertRaises(EscalationRequired):
                surface.adapt(plan, steps=plan.steps, reason="Again.",
                              required_authority="DP-02")
        self.assertEqual(len(surface.history("g")), 1)

    def test_no_override_parameter_exists_on_either_operation(self):
        for method in (PlanningSurface.adapt, PlanningSurface.revise):
            names = method.__code__.co_varnames[
                :method.__code__.co_argcount + method.__code__.co_kwonlyargcount]
            for forbidden in ("force", "override", "approved", "confirm",
                              "bypass"):
                self.assertNotIn(forbidden, names)


class NC_W2_22_23_ExistenceAndReadinessAreNotAuthorization(unittest.TestCase):
    def test_planning_has_no_ready_state_to_misread(self):
        """`READY` belongs to Workflow. A plan cannot be *marked ready* here
        because there is nothing to mark."""
        self.assertNotIn("READY", {o.name for o in PlanOrigin})
        self.assertIn("READY", {s.name for s in WorkflowState})

    def test_an_existing_plan_yields_a_citation_and_nothing_more(self):
        surface, plan = _surface()
        self.assertEqual(
            [n for n in dir(plan)
             if any(v in n.lower() for v in PERMISSION_VERBS)], [])


class NC_W2_24_PastSuccessAuthorizesNothing(unittest.TestCase):
    def test_a_long_successful_history_still_escalates(self):
        surface, plan = _surface()
        current = plan
        for i in range(5):
            current = surface.adapt(current, steps=current.steps,
                                    reason=f"Successful change {i}.")
        self.assertEqual(len(surface.history("g")), 6)
        with self.assertRaises(EscalationRequired):
            surface.adapt(current, steps=current.steps, reason="One more.",
                          required_authority="DP-02")


if __name__ == "__main__":
    unittest.main()
