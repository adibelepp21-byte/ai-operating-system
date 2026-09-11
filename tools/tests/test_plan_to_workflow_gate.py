"""`PLAN → WORKFLOW` — the gate, and why it is not an unbuilt integration.

`ACT-CC-P11-007 §9`–`§11` require proof that an authorized Plan can actually
reach the sanctioned Workflow surface, and forbid inferring connection *"merely
because both modules exist."*

**The investigation reversed my own prior classification.** `ACT-CC-P11-006`
recorded `PLAN → WORKFLOW not consumed` as `AUTHORIZED + ACTIONABLE`, ranked
fifth — an implementation gap awaiting code. It is not. It is
`AUTHORIZED + BLOCKED`, and blocked for a **correct architectural reason**.

`§11`'s seven questions, answered from the actual surfaces:

1. **What artifact is handed to Workflow?** `WorkPreparation` — plan key, step
   key, statement, dependency keys, and a validated `AuthorityProvenance`.
2. **How is it represented?** A frozen description with no method that starts,
   routes or transitions anything.
3. **How is authority provenance carried?** As the validated citation object
   itself, since `ACT-CC-P11-006`. A consumer can re-verify that the cited
   record resolves rather than reading text it must trust.
4. **What does Workflow accept?** `WorkflowStep(step_key, performed_by:
   AgentInstanceRef, composes: SkillRef)`.
5. **What does Workflow reject?** An empty instance or skill key. **It does not
   reject an invented one** — the refs are key-only and validate shape, not
   existence. This is verified below rather than assumed.
6. **What state transition occurs?** **None.** No Plan version reaches any
   `WorkflowState`, and the vocabularies stay disjoint.
7. **What evidence proves consumption?** **There is none, and there should not
   be yet** — see below.

**Why the gate is correct.** `WorkflowStep` requires *who performs the step* and
*which Skill it composes*. A `PlanStep` carries neither, and cannot: naming the
actor for a piece of work is **allocating work to an actor**, which is
delegation. `DP-04 §8.2` fixes the chain as

    GOAL → PLAN → DELEGATION → EXECUTION

so **Plan does not reach Execution directly — it reaches it through Delegation**,
and Workflow coordinates what has been delegated. W3's population is `0` because
no authorized delegator exists, which `ACT-CC-P11-005` established and
`ACT-CC-P11-007 §12` restates: *"Claude MUST NOT create artificial delegation
merely to demonstrate integration."*

**And the gate is architectural, not mechanical.** Workflow will accept a step
naming an agent instance that does not exist, which is verified below. So nothing
in the type system stops a future increment from "completing" this integration by
inventing instance keys and calling it consumption. That is precisely why the
control in `NothingMayFabricateAnActorAssignment` exists: the gate needs an
enforcer, because the architecture holds it and the compiler does not.
"""

import ast
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from native_core.core.workflow import (  # noqa: E402
    AgentInstanceRef,
    SkillRef,
    WorkflowComposition,
    WorkflowState,
    WorkflowStep,
)
from tools.planning import (  # noqa: E402
    AuthorityProvenance,
    Goal,
    Plan,
    PlanStep,
    PlanningSurface,
    WorkPreparation,
)

AUTHORITY = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"

#: Imported rather than restated. A second copy of this list is a second thing
#: to forget, and the governance suite's completeness guard only watches its own
#: — so a surface added there and duplicated here would drift silently, which is
#: the exact failure mode both lists exist to prevent.
from tools.tests.test_p11_governance_boundary import P11_SURFACES  # noqa: E402

#: Constructing any of these is naming *who acts* or *what skill is used* —
#: an actor assignment, which only a delegator may make.
ACTOR_ASSIGNMENT_TYPES = {"AgentInstanceRef", "SkillRef", "WorkflowStep",
                          "WorkflowComposition", "WorkflowDeclaration"}


def _p11_modules():
    for surface in P11_SURFACES:
        if surface.is_dir():
            yield from sorted(surface.glob("*.py"))
        elif surface.is_file():
            yield surface


def _surface():
    authority = AuthorityProvenance("DP-01 §3 W2", AUTHORITY)
    surface = PlanningSurface()
    surface.declare(Goal("g", "Intent.", authority))
    plan = surface.adopt(Plan(key="p", goal_key="g", authority=authority,
                              steps=(PlanStep("a", "A."),
                                     PlanStep("b", "B.", depends_on=("a",)))))
    return surface, plan


class WhatPlanningHandsOver(unittest.TestCase):
    """`§11` questions 1–3, as behaviour rather than description."""

    def test_prepared_work_carries_the_plan_and_a_verified_citation(self):
        surface, plan = _surface()
        prepared = surface.prepare_for_workflow(plan)
        self.assertEqual([p.step_key for p in prepared], ["a", "b"])
        for item in prepared:
            self.assertIsInstance(item, WorkPreparation)
            self.assertIsInstance(item.authority, AuthorityProvenance)

    def test_a_consumer_can_reverify_the_citation_rather_than_trust_text(self):
        """The point of carrying the object across the boundary."""
        surface, plan = _surface()
        item = surface.prepare_for_workflow(plan)[0]
        self.assertTrue((REPO_ROOT / item.authority.record).is_file())


class WhatWorkflowRequiresAndPlanningLacks(unittest.TestCase):
    """`§11` questions 4–5. The gate, demonstrated on both sides."""

    def test_a_workflow_step_requires_an_actor_and_a_skill(self):
        with self.assertRaises(TypeError):
            WorkflowStep(step_key="s")            # neither supplied

    def test_a_plan_step_carries_neither(self):
        step = PlanStep("a", "A.")
        self.assertFalse(hasattr(step, "performed_by"))
        self.assertFalse(hasattr(step, "composes"))
        self.assertFalse(hasattr(step, "agent_instance_key"))

    def test_prepared_work_carries_neither_either(self):
        surface, plan = _surface()
        item = surface.prepare_for_workflow(plan)[0]
        for absent in ("performed_by", "composes", "agent_instance_key",
                       "skill_key"):
            self.assertFalse(hasattr(item, absent), absent)

    def test_workflow_rejects_an_empty_actor_but_accepts_an_invented_one(self):
        """The finding that makes the control below necessary.

        The refs validate *shape*, not *existence*. Nothing in the type system
        prevents a step from naming an actor that has never existed, so the
        architectural gate has no mechanical enforcement of its own.
        """
        from native_core.core.workflow import InvalidWorkflowStep
        with self.assertRaises(InvalidWorkflowStep):
            AgentInstanceRef("")
        invented = WorkflowStep(step_key="s",
                                performed_by=AgentInstanceRef("never-existed"),
                                composes=SkillRef("also-never-existed"))
        composition = WorkflowComposition(steps=(invented,))
        self.assertEqual(len(composition.acting_instances()), 1)

    def test_no_agent_instance_population_exists_to_draw_from(self):
        """Even a would-be assigner has nothing legitimate to assign to."""
        organization = REPO_ROOT / "docs" / "architecture" / "organization"
        self.assertEqual(list(organization.rglob("*instance*")), [])


class NothingMayFabricateAnActorAssignment(unittest.TestCase):
    """The control the architectural gate needs, because types do not enforce it.

    `DP-04 §8.2` routes `PLAN → DELEGATION → EXECUTION`, and
    `ACT-CC-P11-007 §12` forbids creating *"artificial delegation merely to
    demonstrate integration."* Since Workflow accepts an invented actor, the only
    thing standing between this repository and a fabricated integration is a
    control that says so.
    """

    def test_no_p11_surface_constructs_an_actor_assignment(self):
        offenders = []
        for path in _p11_modules():
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                        and node.func.id in ACTOR_ASSIGNMENT_TYPES:
                    offenders.append(f"{path.name}:{node.func.id}")
        self.assertEqual(offenders, [],
                         f"planning fabricated an actor assignment: {offenders}")

    def test_no_p11_surface_imports_the_workflow_boundary(self):
        offenders = []
        for path in _p11_modules():
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module \
                        and "workflow" in node.module:
                    offenders.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual(offenders, [])

    def test_every_delegation_came_from_a_legitimate_delegator(self):
        """The gate's upstream condition, stated as it was always meant.

        The original wording — *"if this ever becomes non-zero through anything
        but a legitimate delegator, the integration below it is fabricated
        rather than earned"* — already named the real test. It asserted zero
        because no legitimate delegator existed. One now does, so the condition
        is checked directly instead of through its proxy.
        """
        from tools.delegation_catalog import (
            INSTRUMENT_ESTABLISHED_SOURCES, read_delegations,
            verify as verify_w3)
        from tools.organization_catalog import read_departments
        legitimate = {d.key for d in read_departments()} | set(
            INSTRUMENT_ESTABLISHED_SOURCES)
        for record in read_delegations():
            self.assertIn(record.authority_source, legitimate)
        self.assertEqual(verify_w3(read_delegations()), [])


class TheSeparationSurvivesTheHandoff(unittest.TestCase):
    """`§10` — ``PLANNING ≠ WORKFLOW``, at the boundary rather than in general."""

    def test_no_plan_version_carries_a_workflow_state(self):
        surface, plan = _surface()
        for version in surface.history("g"):
            for state in WorkflowState:
                self.assertNotEqual(getattr(version, "origin", None).name,
                                    state.name)

    def test_preparing_work_does_not_advance_the_plan(self):
        """Handing work over is not progress on the plan. If preparation
        mutated the chain, Planning would be tracking execution."""
        surface, plan = _surface()
        before = surface.history("g")
        surface.prepare_for_workflow(plan)
        self.assertEqual(surface.history("g"), before)
        self.assertIs(surface.current("g"), plan)


if __name__ == "__main__":
    unittest.main()
