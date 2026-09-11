"""`ACT-CC-P11-010 §32`/`§33` — attacks on the `PLAN → WORKFLOW` handoff.

The conclusion under attack is **`U2` — existing authority already satisfies the
role**, reached by falsifying a hypothesis of mine: that a *"unit-level
delegator"* was required. `§43`: *"DO NOT TREAT ABSENCE AS LAW. TEST THE
GOVERNING INVARIANT."*

The governing invariant here is `§24`:

    NO HANDOFF UNLESS VALID AUTHORITY PROVENANCE EXISTS

and **not** *"no handoff because no unit delegator exists"*, which was an
absence-of-authority premise of exactly the kind `ACT-CC-P11-009 §94.4` found
rotting in eight earlier controls.
"""

import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from native_core.core.agent.definition import AgentDefinition  # noqa: E402
from native_core.core.workflow import (  # noqa: E402
    AgentInstanceRef, SkillRef, WorkflowStep)
from tools.agent_instance_registry import AgentInstanceRegistry  # noqa: E402
from tools.plan_to_workflow import (  # noqa: E402
    HandoffRefused, authorize_handoff, compose, permitted_skills)
from tools.planning import AuthorityProvenance, WorkPreparation  # noqa: E402
from tools.w1_coordination_run import (  # noqa: E402
    DEFINITION, INSTANCE_KEY, STEP_SKILLS, _plan)
from tools.w4_delegation import (  # noqa: E402
    AUTHORIZED_DELEGATOR, W4DelegationRegistry)

FD = ("docs/governance/acts/"
      "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md")
DP01 = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"
W1_OPS = REPO_ROOT / "docs/architecture/p11/w1-operations"


def _stack(work_scope=tuple(STEP_SKILLS),
           capability_scope=("governance-artifact-integrity",)):
    registry = AgentInstanceRegistry()
    registry.register(
        instance_key=INSTANCE_KEY, definition=DEFINITION,
        permitted_capabilities=("governance-artifact-integrity",),
        created_by=AUTHORIZED_DELEGATOR,
        authority=AuthorityProvenance("FD-P11-001 §7", FD),
        accountable_to=AUTHORIZED_DELEGATOR)
    delegations = W4DelegationRegistry(registry)
    delegation = delegations.issue(
        delegator=AUTHORIZED_DELEGATOR, recipient_instance=INSTANCE_KEY,
        authority=AuthorityProvenance("FD-P11-001 §9", FD),
        objective="o", capability_scope=capability_scope,
        work_scope=work_scope, lifecycle_boundary="l", resource_boundary="r",
        output_expectation="oe", verification_requirement="v",
        escalation_condition="e", accountable_party=AUTHORIZED_DELEGATOR,
        termination_condition="t")
    surface, plan = _plan()
    return registry, delegations, delegation, surface.prepare_for_workflow(plan)


class Attack1_TheHypothesisHasNoCanonicalBasis(unittest.TestCase):
    """`§32` Attack 1: find a canonical source requiring unit-level delegation.

    **None exists.** The phrase appears in no issued instrument — only in
    documents I wrote. That does not by itself make the requirement false, which
    is why the attacks below test the mechanism rather than the wording.
    """

    INSTRUMENTS = (
        "docs/architecture/p11/DP-03-P11-ORGANIZATIONAL-ARCHITECTURAL-SURFACE.md",
        "docs/architecture/p11/DP-04-P11-ORGANIZATIONAL-ENTITY-MODEL.md",
        "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md",
        FD,
    )

    def test_no_issued_instrument_requires_a_unit_level_delegator(self):
        for relative in self.INSTRUMENTS:
            with self.subTest(instrument=Path(relative).name):
                body = (REPO_ROOT / relative).read_text(encoding="utf-8").lower()
                self.assertNotIn("unit-level delegator", body)
                self.assertNotIn("unit delegator", body)

    def test_workflow_requires_an_actor_and_a_skill_not_a_delegating_unit(self):
        """`§32` Attack 3: the blocker was implementation, not architecture."""
        import inspect
        parameters = inspect.signature(WorkflowStep.__init__).parameters
        self.assertEqual(sorted(p for p in parameters if p != "self"),
                         ["composes", "performed_by", "step_key"])

    def test_the_resident_workflow_record_already_names_its_actor(self):
        """`§32` Attack 4: an existing P10 mechanism satisfies the role."""
        record = (REPO_ROOT / "docs/architecture/organization/execution-catalog"
                  / "workflow/governance-corpus-health-check.md"
                  ).read_text(encoding="utf-8")
        self.assertIn("Invokes Agent Instance", record)
        self.assertIn("Governance Artifact Integrity Agent", record)


class Attack5_AValidHandoffSucceedsOnExistingAuthority(unittest.TestCase):
    """`§32` Attack 5, and the `U2` claim itself."""

    def test_the_handoff_produces_a_workflow_step(self):
        registry, _, delegation, prepared = _stack()
        step = authorize_handoff(
            prepared[0], delegation=delegation, registry=registry,
            skill_key=STEP_SKILLS[prepared[0].step_key])
        self.assertIsInstance(step, WorkflowStep)
        self.assertEqual(step.performed_by, AgentInstanceRef(INSTANCE_KEY))
        self.assertEqual(step.composes,
                         SkillRef(STEP_SKILLS[prepared[0].step_key]))

    def test_every_field_is_copied_from_something_already_authorized(self):
        """`§18`: `TRANSLATION ≠ AUTHORIZATION`."""
        registry, _, delegation, prepared = _stack()
        step = authorize_handoff(prepared[0], delegation=delegation,
                                 registry=registry,
                                 skill_key=STEP_SKILLS[prepared[0].step_key])
        self.assertEqual(step.step_key, prepared[0].step_key)          # Plan
        self.assertEqual(step.performed_by.agent_instance_key,
                         delegation.recipient_instance)                # Delegation
        self.assertIn(step.composes.skill_key,
                      permitted_skills(DEFINITION.agent_definition_key))  # Definition


class NC01_07_08_HandoffRequiresLiveAuthority(unittest.TestCase):
    """`§33` NC-01, NC-07, NC-08 — and `§32` Attacks 6, 7, 8."""

    def test_a_handoff_without_a_delegation_is_refused(self):
        registry, _, _, prepared = _stack()
        for absent in (None, "FD-P11-001", 0):
            with self.subTest(value=type(absent).__name__):
                with self.assertRaises(HandoffRefused) as caught:
                    authorize_handoff(prepared[0], delegation=absent,
                                      registry=registry, skill_key="x")
                self.assertEqual(caught.exception.reason, "no-delegation")

    def test_a_revoked_delegation_cannot_authorize_a_handoff(self):
        registry, delegations, delegation, prepared = _stack()
        delegations.revoke(delegation.delegation_id, reason="attack")
        with self.assertRaises(HandoffRefused) as caught:
            authorize_handoff(prepared[0],
                              delegation=delegations.get(delegation.delegation_id),
                              registry=registry,
                              skill_key=STEP_SKILLS[prepared[0].step_key])
        self.assertEqual(caught.exception.reason, "delegation-not-executable")

    def test_a_step_outside_the_delegated_scope_is_refused(self):
        registry, _, delegation, prepared = _stack(
            work_scope=("review-open-items",))
        with self.assertRaises(HandoffRefused) as caught:
            authorize_handoff(prepared[1], delegation=delegation,
                              registry=registry,
                              skill_key=STEP_SKILLS[prepared[1].step_key])
        self.assertEqual(caught.exception.reason, "step-outside-scope")

    def test_a_capability_outside_the_delegation_is_refused(self):
        """Defence in depth, reached by constructing the grant directly.

        The delegation registry already refuses to *issue* a grant naming a
        capability the instance does not hold, so this check is unreachable
        through `issue()`. It is reachable by constructing a `W4Delegation`
        directly — verified rather than assumed, the same way the observation
        guard in `performance_evidence` was shown reachable via a frozen-dataclass
        bypass.
        """
        from datetime import datetime, timezone
        from tools.w4_delegation import W4Delegation
        registry, _, _, prepared = _stack()
        forged = W4Delegation(
            delegation_id="direct", delegator=AUTHORIZED_DELEGATOR,
            recipient_instance=INSTANCE_KEY,
            authority=AuthorityProvenance("FD-P11-001 §9", FD),
            objective="o", capability_scope=("something-else",),
            work_scope=tuple(STEP_SKILLS), lifecycle_boundary="l",
            resource_boundary="r", output_expectation="oe",
            verification_requirement="v", escalation_condition="e",
            accountable_party=AUTHORIZED_DELEGATOR, termination_condition="t",
            issued_at=datetime.now(timezone.utc).isoformat())
        with self.assertRaises(HandoffRefused) as caught:
            authorize_handoff(prepared[0], delegation=forged,
                              registry=registry,
                              skill_key=STEP_SKILLS[prepared[0].step_key])
        self.assertEqual(caught.exception.reason, "capability-not-delegated")


class NC02_03_05_06_IdentityCannotBeFabricated(unittest.TestCase):
    """`§33` NC-02, NC-03, NC-05, NC-06."""

    def test_an_unregistered_instance_cannot_receive_a_handoff(self):
        registry = AgentInstanceRegistry()          # nothing registered
        _, _, delegation, prepared = _stack()
        with self.assertRaises(HandoffRefused) as caught:
            authorize_handoff(prepared[0], delegation=delegation,
                              registry=registry,
                              skill_key=STEP_SKILLS[prepared[0].step_key])
        self.assertEqual(caught.exception.reason, "instance-not-registered")

    def test_a_retired_instance_cannot_receive_a_handoff(self):
        registry, _, delegation, prepared = _stack()
        registry.retire(INSTANCE_KEY)
        with self.assertRaises(HandoffRefused) as caught:
            authorize_handoff(prepared[0], delegation=delegation,
                              registry=registry,
                              skill_key=STEP_SKILLS[prepared[0].step_key])
        self.assertEqual(caught.exception.reason, "instance-not-live")

    def test_a_skill_the_definition_does_not_permit_is_refused(self):
        """`§33` NC-09: the adapter cannot grant a skill."""
        registry, _, delegation, prepared = _stack()
        for invented in ("do-anything", "engineering-intelligence",
                         "staleness-detection-extended"):
            with self.subTest(skill=invented):
                with self.assertRaises(HandoffRefused) as caught:
                    authorize_handoff(prepared[0], delegation=delegation,
                                      registry=registry, skill_key=invented)
                self.assertEqual(caught.exception.reason, "skill-not-permitted")

    def test_a_definition_with_no_skills_can_hand_off_nothing(self):
        """The actual cause of the old blocker, asserted.

        `engineering-intelligence-agent` declares *"Permitted Skills: None
        declared."* An instance of it can never produce a `WorkflowStep`,
        because a `WorkflowStep` requires a Skill.
        """
        self.assertEqual(permitted_skills("engineering-intelligence-agent"), ())
        self.assertEqual(permitted_skills("cognitive-intelligence-agent"), ())
        self.assertGreater(
            len(permitted_skills("governance-artifact-integrity-agent")), 0)

    def test_unprepared_work_cannot_enter_the_handoff(self):
        registry, _, delegation, prepared = _stack()
        for bogus in ("review-open-items", None, {"step_key": "x"}):
            with self.subTest(value=type(bogus).__name__):
                with self.assertRaises(HandoffRefused) as caught:
                    authorize_handoff(bogus, delegation=delegation,
                                      registry=registry, skill_key="x")
                self.assertEqual(caught.exception.reason, "not-prepared-work")


class NC09_11_12_TheAdapterCreatesNoAuthority(unittest.TestCase):
    """`§33` NC-09, NC-11, NC-12 — and `§32` Attack 9."""

    def test_the_adapter_defines_no_way_to_grant_anything(self):
        """Checked over names the module **defines**, not names it imports.

        My first version scanned `dir(module)` for substrings including
        ``register`` — and failed, because the module imports
        `AgentInstanceRegistry` in order to *ask* it whether an instance is
        registered. Substring reasoning over an imported symbol says nothing
        about what a module does; this is the fourth time that class of error has
        cost me a wrong assertion.
        """
        import ast
        source = (REPO_ROOT / "tools" / "plan_to_workflow.py").read_text(
            encoding="utf-8")
        defined = [node.name for node in ast.walk(ast.parse(source))
                   if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
        for name in defined:
            self.assertFalse(
                any(v in name.lower() for v in
                    ("grant", "register", "issue", "delegate", "approve")),
                f"the adapter defines {name!r}")

    def test_composition_preserves_planning_order_and_reorders_nothing(self):
        """Coordination must not become the reserved prioritization frontier."""
        registry, _, delegation, prepared = _stack()
        composition = compose(prepared, delegation=delegation, registry=registry,
                              skill_for=STEP_SKILLS)
        self.assertEqual([s.step_key for s in composition.steps],
                         [p.step_key for p in prepared])

    def test_workflow_construction_writes_no_delegation(self):
        registry, delegations, delegation, prepared = _stack()
        before = set(delegations.keys())
        compose(prepared, delegation=delegation, registry=registry,
                skill_for=STEP_SKILLS)
        self.assertEqual(set(delegations.keys()), before)


class NC13_15_TheRealRunIsBoundedAndHonest(unittest.TestCase):
    """`§33` NC-13, NC-15, `§35` idempotency, and `§19` honesty."""

    def _evidence(self):
        return json.loads((W1_OPS / "w1-coordination.evidence.json")
                          .read_text(encoding="utf-8"))

    def test_the_real_run_reached_a_terminal_succeeded_workflow(self):
        evidence = self._evidence()
        self.assertIn("SUCCEEDED", evidence["workflow_terminal_state"])
        self.assertFalse(evidence["boundary_crossed"])

    def test_the_run_did_not_overstate_coordination(self):
        """`§19`: one acting instance is a **handoff**, not cross-agent
        coordination. Reported as such rather than rounded up."""
        evidence = self._evidence()
        self.assertFalse(evidence["is_multi_agent"])
        self.assertEqual(len(set(evidence["acting_instances"])), 1)

    def test_at_most_one_live_grant_survives_a_rerun(self):
        active = [json.loads(p.read_text(encoding="utf-8"))
                  for p in W1_OPS.glob("*.delegation.json")]
        self.assertLessEqual(
            len([g for g in active if g["status"] == "ACTIVE"]), 1)

    def test_every_retired_grant_states_why(self):
        for path in W1_OPS.glob("*.delegation.json"):
            grant = json.loads(path.read_text(encoding="utf-8"))
            if grant["status"] == "REVOKED":
                with self.subTest(grant=grant["delegation_id"]):
                    self.assertTrue(grant.get("revocation_reason", "").strip())

    def test_the_skills_are_the_ones_the_resident_workflow_names(self):
        record = (REPO_ROOT / "docs/architecture/organization/execution-catalog"
                  / "workflow/governance-corpus-health-check.md"
                  ).read_text(encoding="utf-8")
        for skill in self._evidence()["composed_skills"]:
            with self.subTest(skill=skill):
                self.assertIn(skill, record)


if __name__ == "__main__":
    unittest.main()
