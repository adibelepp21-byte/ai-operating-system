"""Plan → delegation (`FD-AGENCY-001` S-2).

The delegator issues one bounded grant for one step a plan marked for
delegation; Planning delegates nothing. Temporary roots only.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from tools import planning_continuity
from tools import w4_delegation as w4
from tools.agent_instance_registry import AgentInstanceRegistry
from tools.planning import AuthorityProvenance, Goal, Plan, PlanningSurface, PlanStep
from tools.planning.exceptions import InvalidPlan
from tools.w4_continuity import reconstruct
from tools.w4_execution import W4Executor
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION

REPO = Path(__file__).resolve().parents[2]
S2_RECORD = "docs/governance/acts/DIR-AIOS-AGENCY-S2-PLAN-TO-DELEGATION.md"
DELEGATOR = w4.AUTHORIZED_DELEGATOR
INSTANCE = "engineering-intelligence-instance-001"
FD9 = AuthorityProvenance("FD-P11-001 §9", FD_RECORD)
TERMS = dict(resource_boundary="read-only over one named file",
             output_expectation="one result per criterion",
             verification_requirement="every criterion reported satisfied or not",
             escalation_condition="any step outside the delegated work scope")


def _surface():
    authority = AuthorityProvenance("FD-AGENCY-001 S-2", S2_RECORD)
    surface = PlanningSurface()
    surface.declare(Goal(key="g", statement="Verify the ledger.", authority=authority))
    plan = surface.adopt(Plan(key="g-plan-0", goal_key="g", authority=authority, steps=(
        PlanStep("verify", "Verify the ledger rules.", requires_delegation=True),
        PlanStep("review", "Review the verification result.", depends_on=("verify",)))))
    return surface, plan


class _Root(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="s2-"))
        self.registry = AgentInstanceRegistry(self.root)
        self.registry.register(
            instance_key=INSTANCE, definition=SELECTED_DEFINITION,
            permitted_capabilities=("engineering-intelligence",), created_by=DELEGATOR,
            authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
            accountable_to=DELEGATOR)
        self.delegations = w4.W4DelegationRegistry(self.registry, self.root)
        self.surface, self.plan = _surface()

    def tearDown(self):
        shutil.rmtree(self.root)

    def issue(self, step="verify", **overrides):
        kwargs = dict(delegator=DELEGATOR, recipient_instance=INSTANCE, authority=FD9,
                      capability_scope=("engineering-intelligence",), **TERMS)
        kwargs.update(overrides)
        return w4.issue_from_plan(self.delegations, self.surface, self.plan, step, **kwargs)


class TheDelegatorIssuesFromThePlan(_Root):
    def test_the_grant_carries_the_plan_step_and_nothing_wider(self):
        grant = self.issue()
        self.assertEqual("Verify the ledger rules.", grant.objective)
        self.assertEqual(("verify",), grant.work_scope)
        self.assertEqual("one execution of plan g-plan-0", grant.lifecycle_boundary)
        self.assertEqual(DELEGATOR, grant.accountable_party)
        self.assertEqual(w4.TERMINATION_ON_PLAN, grant.termination_condition)
        self.assertTrue((self.root / f"{grant.delegation_id}.delegation.json").is_file())

    def test_a_fresh_process_rebuilds_the_grant_and_its_plan(self):
        grant = self.issue()
        planning_continuity.save(self.surface, self.root / "planning.json")
        script = (
            "import json,sys; from pathlib import Path;"
            "from tools.w4_continuity import reconstruct;"
            "from tools import planning_continuity, w4_delegation as w4;"
            f"root=Path({str(self.root)!r}); s=reconstruct(root);"
            "surface=planning_continuity.restore(root/'planning.json');"
            "rec=json.loads((root/(s['active_grants'][0]+'.delegation.json')).read_text());"
            "print(json.dumps({'active':s['active_grants'],'prov':w4.plan_provenance(rec,surface)}))")
        out = json.loads(subprocess.run([sys.executable, "-c", script], cwd=REPO,
                                        capture_output=True, text=True, check=True).stdout)
        self.assertEqual([grant.delegation_id], out["active"])
        prov = out["prov"]
        self.assertEqual({"plan": "g-plan-0", "step": "verify", "faults": [],
                          "goal": "g", "plan_current": True},
                         {k: prov[k] for k in ("plan", "step", "faults", "goal", "plan_current")})
        # S-3: the reader also reports whether the goal is a quoted Founder Goal.
        # This test goal is not one, and is reported as such.
        self.assertTrue(prov["founder_goal"].startswith("NOT VERIFIED"))


class OnlyTheDelegatorAndOnlyWhatThePlanMarked(_Root):
    def test_an_agent_cannot_issue(self):
        with self.assertRaisesRegex(w4.DelegationError, "not the authorized W4 delegator"):
            self.issue(delegator=INSTANCE)
        self.assertEqual((), self.delegations.keys())

    def test_a_step_not_marked_for_delegation_cannot_be_delegated(self):
        with self.assertRaisesRegex(w4.DelegationError, "does not mark step"):
            self.issue(step="review")

    def test_a_superseded_plan_yields_nothing_to_issue(self):
        self.surface.revise(self.plan, steps=self.plan.steps, reason="revised")
        with self.assertRaises(InvalidPlan):
            self.issue()

    def test_the_caller_cannot_widen_or_rename_the_work(self):
        for field in ("work_scope", "objective", "lifecycle_boundary",
                      "accountable_party", "termination_condition"):
            with self.assertRaises(TypeError, msg=field):
                self.issue(**{field: "anything"})

    def test_capability_beyond_the_recipient_is_refused(self):
        with self.assertRaisesRegex(w4.DelegationError, "exceeds"):
            self.issue(capability_scope=("governance-artifact-integrity",))

    def test_a_founder_reserved_instrument_is_not_a_delegation_authority(self):
        reserved = AuthorityProvenance(
            "FD-AGENCY-001", "docs/governance/acts/FD-AGENCY-001-FOUNDER-DECISION.md")
        with self.assertRaisesRegex(w4.DelegationError, "must cite FD-P11-001"):
            self.issue(authority=reserved)

    def test_an_unregistered_recipient_is_refused(self):
        with self.assertRaisesRegex(w4.DelegationError, "not a registered"):
            self.issue(recipient_instance="unregistered-instance")


class TheGrantConfersNoMore(_Root):
    def test_the_grant_is_immutable(self):
        grant = self.issue()
        with self.assertRaises(FrozenInstanceError):
            grant.work_scope = ("verify", "review")

    def test_the_recipient_cannot_execute_beyond_the_step(self):
        grant = self.issue()
        report = W4Executor(grant, self.registry).execute_plan(self.plan, lambda step: "ok")
        self.assertEqual({"verify": "success", "review": "escalation"},
                         {o.step_key: o.status for o in report.outcomes})

    def test_the_grant_carries_no_decision_or_delegation_field(self):
        payload = self.issue().to_payload()
        self.assertFalse([k for k in payload if any(
            w in k for w in ("decide", "decision", "approve", "redelegat", "delegate_to"))])


class ProvenanceFaultsAreReported(_Root):
    def test_a_changed_objective_or_unknown_plan_is_a_fault(self):
        record = self.issue().to_payload()
        self.assertEqual([], w4.plan_provenance(record, self.surface)["faults"])
        self.assertTrue(w4.plan_provenance({**record, "objective": "x"}, self.surface)["faults"])
        self.assertTrue(w4.plan_provenance(
            {**record, "lifecycle_boundary": "one execution of plan other-plan"},
            self.surface)["faults"])


if __name__ == "__main__":
    unittest.main()
