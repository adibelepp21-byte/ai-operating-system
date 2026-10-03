"""S-4: agent result → verification evidence → CEO decision → plan outcome.

Temporary roots for everything written; the certified roots are only read.
"""
import hashlib
import inspect
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools import planning_continuity
from tools import w4_delegation as w4
from tools.agent_instance_registry import AgentInstanceRegistry
from tools.planning import AuthorityProvenance, Goal, Plan, PlanningSurface, PlanStep
from tools.w4_execution import ExecutionRefused, W4Executor, persist_evidence
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION

REPO = Path(__file__).resolve().parents[2]
INSTANCE = "engineering-intelligence-instance-001"
DELEGATOR = w4.AUTHORIZED_DELEGATOR
CEO = AuthorityProvenance(
    "Co-Founder V2 A01 Executive Command",
    "docs/governance/AIOS_COFOUNDER_V2_REGISTRATION_AND_ACTIVATION_RECORD_v1.0.md")
S4 = AuthorityProvenance("DIR-AIOS-AGENCY-S4-AGENT-EVIDENCE-TO-PLAN-OUTCOME",
                         "docs/governance/acts/DIR-AIOS-AGENCY-S4-AGENT-EVIDENCE-TO-PLAN-OUTCOME.md")
TERMS = dict(capability_scope=("engineering-intelligence",), resource_boundary="r",
             output_expectation="o", verification_requirement="v", escalation_condition="e")


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class _Loop(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="s4-"))
        self.root = self.tmp / "ops"
        self.ledger = self.tmp / "ledger"
        self.registry = AgentInstanceRegistry(self.root)
        self.registry.register(instance_key=INSTANCE, definition=SELECTED_DEFINITION,
                               permitted_capabilities=("engineering-intelligence",),
                               created_by=DELEGATOR,
                               authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
                               accountable_to=DELEGATOR)
        self.delegations = w4.W4DelegationRegistry(self.registry, self.root)
        self.surface = PlanningSurface()
        self.surface.declare(Goal(key="g", statement="Prove the loop.", authority=S4))
        self.plan = self.surface.adopt(Plan(key="g-plan-0", goal_key="g", authority=CEO, steps=(
            PlanStep("verify", "Verify the artifact.", requires_delegation=True),
            PlanStep("review", "Review the result (CEO).", depends_on=("verify",)))))
        self.grant = w4.issue_from_plan(
            self.delegations, self.surface, self.plan, "verify", delegator=DELEGATOR,
            recipient_instance=INSTANCE, authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
            **TERMS)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def execute(self, succeed=True):
        def perform(step):
            if not succeed:
                raise AssertionError("3 of 14 criteria satisfied")
            return "14 of 14 criteria satisfied"
        executor = W4Executor(self.grant, self.registry)
        from tools.w4_execution import ExecutionReport
        report = ExecutionReport(outcomes=[executor.execute_step(self.plan.step("verify"), perform)])
        return persist_evidence(self.root, self.plan.key, self.grant, report)

    def review(self, decision, **kw):
        kw.setdefault("reviewer", DELEGATOR)
        kw.setdefault("reason", "reviewed")
        return w4.review_result(self.root, self.grant.delegation_id, surface=self.surface,
                                decision=decision, ledger=self.ledger, **kw)

    def outcome(self):
        return w4.plan_outcome(self.surface, "g", self.root, self.ledger)


class Accept(_Loop):
    def test_a_verified_result_is_accepted_and_the_plan_completes(self):
        self.execute()
        pending = self.outcome()
        self.assertFalse(pending["completed"])
        self.assertEqual((w4.ACTIVE, False), (pending["versions"][0]["steps"][0]["outcome"],
                                              pending["versions"][0]["steps"][0]["done"]))
        self.assertFalse(pending["versions"][0]["steps"][1]["done"])
        result = self.review(w4.ACCEPT)
        self.assertEqual("verification met", result["verification"])
        out = self.outcome()
        self.assertTrue(out["completed"])
        verify, review = out["versions"][0]["steps"]
        self.assertEqual((w4.COMPLETED, True), (verify["outcome"], verify["done"]))
        self.assertTrue(verify["grants"][0]["decision"].startswith("CEO ACCEPT"))
        self.assertEqual(("CEO", True), (review["performed_by"], review["done"]))

    def test_n3_an_unverified_result_cannot_be_accepted(self):
        with self.assertRaisesRegex(w4.DelegationError, "not established"):
            self.review(w4.ACCEPT)
        self.assertFalse(self.ledger.exists())
        self.assertFalse(self.outcome()["completed"])

    def test_n8_ceo_acceptance_is_not_founder_acceptance(self):
        self.execute()
        self.review(w4.ACCEPT)
        self.assertTrue(self.outcome()["founder_acceptance"].startswith("NOT RECORDED"))
        self.assertNotIn("founder", " ".join(inspect.signature(w4.review_result).parameters))


class Rework(_Loop):
    def test_n4_n5_a_failed_result_is_sent_back_and_the_plan_stays_open(self):
        evidence = self.execute(succeed=False)
        with self.assertRaisesRegex(w4.DelegationError, "not every plan step succeeded"):
            self.review(w4.ACCEPT)
        result = self.review(w4.REWORK, rework_steps=(
            PlanStep("verify-again", "Verify the corrected artifact.", requires_delegation=True),
            PlanStep("review", "Review the result (CEO).", depends_on=("verify-again",))))
        out = self.outcome()
        self.assertFalse(out["completed"])
        self.assertEqual(["verify-again", "review"], out["open_steps"])
        old, new = out["versions"]
        self.assertEqual(result["successor_plan"], old["superseded_by"])
        self.assertEqual("REVISED", new["origin"])
        self.assertIn(self.grant.delegation_id, new["reason"])
        self.assertIn("verification not met", new["evidence"][0])
        self.assertIn(evidence.name, new["evidence"][0])
        self.assertEqual(w4.REVOKED, old["steps"][0]["outcome"])
        self.assertTrue(old["steps"][0]["grants"][0]["decision"].startswith("CEO REWORK"))
        self.assertEqual("DELEGATION REQUIRED", new["steps"][0]["outcome"])
        self.assertEqual(CEO, self.surface.current("g").authority)

    def test_n9_history_is_preserved_and_a_decision_is_final(self):
        evidence = self.execute(succeed=False)
        before = (_sha(evidence), _sha(self.root / f"{self.grant.delegation_id}.delegation.json"))
        self.review(w4.REWORK, rework_steps=(PlanStep("x", "x", requires_delegation=True),))
        self.assertEqual(before, (_sha(evidence),
                                  _sha(self.root / f"{self.grant.delegation_id}.delegation.json")))
        self.assertEqual("g-plan-0", self.surface.history("g")[0].key)
        with self.assertRaisesRegex(w4.DelegationError, "not established"):
            self.review(w4.ACCEPT)
        from tools.planning.exceptions import InvalidPlan
        with self.assertRaisesRegex(InvalidPlan, "superseded"):
            self.review(w4.REWORK, rework_steps=(PlanStep("y", "y", requires_delegation=True),))
        with self.assertRaisesRegex(w4.DelegationError, "append-only"):
            w4.record_disposition(self.root, self.grant.delegation_id, disposition=w4.REVOKED,
                                  delegator=DELEGATOR, reason="again", ledger=self.ledger,
                                  authority=w4.DELEGATOR_REVIEW)
        with self.assertRaises(FileExistsError):
            self.execute()


class ReworkNeedsItsSuccessor(_Loop):
    def test_rework_without_saying_what_is_sent_back_is_refused_and_nothing_moves(self):
        self.execute(succeed=False)
        with self.assertRaisesRegex(w4.DelegationError, "what the work is sent back as"):
            self.review(w4.REWORK)
        self.assertFalse(self.ledger.exists())
        self.assertEqual(["g-plan-0"], [p.key for p in self.surface.history("g")])


class Reject(_Loop):
    def test_there_is_no_reject_semantic(self):
        self.execute()
        with self.assertRaisesRegex(w4.DelegationError, "no REJECT semantic"):
            self.review("REJECT")


class AuthorityBoundaries(_Loop):
    def test_n1_n2_an_agent_cannot_accept_its_own_or_any_result(self):
        self.execute()
        with self.assertRaisesRegex(w4.DelegationError, "may not review delegated results"):
            self.review(w4.ACCEPT, reviewer=INSTANCE)
        with self.assertRaisesRegex(w4.DelegationError, "may not review delegated results"):
            self.review(w4.REWORK, reviewer=INSTANCE,
                        rework_steps=(PlanStep("x", "x", requires_delegation=True),))
        self.assertEqual(["g-plan-0"], [p.key for p in self.surface.history("g")])
        with self.assertRaisesRegex(w4.DelegationError, "only 'Claude Code"):
            w4.record_disposition(self.root, self.grant.delegation_id, disposition=w4.COMPLETED,
                                  delegator=INSTANCE, reason="self", ledger=self.ledger,
                                  authority=w4.DELEGATOR_REVIEW)
        self.assertFalse(self.ledger.exists())

    def test_n6_scope_cannot_widen_and_the_ceo_step_is_not_the_agents(self):
        with self.assertRaises(TypeError):
            w4.issue_from_plan(self.delegations, self.surface, self.plan, "verify",
                               delegator=DELEGATOR, recipient_instance=INSTANCE,
                               authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
                               work_scope=("verify", "review"), **TERMS)
        with self.assertRaises(ExecutionRefused):
            W4Executor(self.grant, self.registry).execute_step(
                self.plan.step("review"), lambda step: "accepted")

    def test_n7_an_agent_cannot_issue_a_delegation(self):
        with self.assertRaisesRegex(w4.DelegationError, "not the authorized W4 delegator"):
            w4.issue_from_plan(self.delegations, self.surface, self.plan, "verify",
                               delegator=INSTANCE, recipient_instance=INSTANCE,
                               authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD), **TERMS)

    def test_the_delegator_review_never_reaches_certified_evidence(self):
        root = REPO / "docs/architecture/p11/x-department-operations"
        before = sorted((p.name, _sha(p)) for p in root.iterdir())
        with self.assertRaisesRegex(w4.DelegationError, "outside certified evidence"):
            w4.record_disposition(root, "0f7ac0785bd8442b", disposition=w4.COMPLETED,
                                  delegator=DELEGATOR, reason="x", ledger=self.ledger,
                                  authority=w4.DELEGATOR_REVIEW)
        self.assertEqual(before, sorted((p.name, _sha(p)) for p in root.iterdir()))


class FreshProcess(_Loop):
    def test_n10_the_decision_chain_survives_a_restart(self):
        self.execute()
        self.review(w4.ACCEPT)
        planning_continuity.save(self.surface, self.root / "planning.state.json")
        here = self.outcome()
        script = (
            "import json; from pathlib import Path;"
            "from tools import planning_continuity, w4_delegation as w4;"
            f"root=Path({str(self.root)!r}); ledger=Path({str(self.ledger)!r});"
            "s=planning_continuity.restore(root/'planning.state.json');"
            "print(json.dumps(w4.plan_outcome(s,'g',root,ledger)))")
        there = json.loads(subprocess.run([sys.executable, "-c", script], cwd=REPO,
                                          capture_output=True, text=True, check=True).stdout)
        self.assertEqual(json.loads(json.dumps(here)), there)
        self.assertTrue(there["completed"])


if __name__ == "__main__":
    unittest.main()
