"""Founder Goal → CEO plan → delegation (`FD-AGENCY-001` S-3).

A Founder Goal is a planning `Goal` that quotes a registered, verbatim Founder
instrument. The CEO plans under its own authority; only the delegator issues.
Temporary roots for anything written; the real S-3 directive is only read.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools import authority_citation as ac
from tools import planning_continuity
from tools import w4_delegation as w4
from tools.agent_instance_registry import AgentInstanceRegistry
from tools.planning import AuthorityProvenance, Goal, Plan, PlanningSurface, PlanStep
from tools.planning.exceptions import InvalidPlan
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION

REPO = Path(__file__).resolve().parents[2]
S3_ID = "DIR-AIOS-AGENCY-S3-FOUNDER-GOAL-TO-PLANNING"
S3_RECORD = f"docs/governance/acts/{S3_ID}.md"
S3_GOAL = "S-3 — Connect Founder Goal to the CEO Planning Surface"
CEO = AuthorityProvenance(
    "Co-Founder V2 A01 Executive Command",
    "docs/governance/AIOS_COFOUNDER_V2_REGISTRATION_AND_ACTIVATION_RECORD_v1.0.md")
INSTANCE = "engineering-intelligence-instance-001"
FD9 = AuthorityProvenance("FD-P11-001 §9", FD_RECORD)
TERMS = dict(resource_boundary="r", output_expectation="o",
             verification_requirement="v", escalation_condition="e")


class FounderGoalsAreQuotedFromRegisteredFounderInstruments(unittest.TestCase):
    def test_the_s3_goal_verifies(self):
        self.assertIsNone(ac.founder_goal_refusal(S3_ID, S3_RECORD, S3_GOAL))

    def test_a_paraphrase_alters_founder_intent(self):
        self.assertIn("verbatim", ac.founder_goal_refusal(
            S3_ID, S3_RECORD, "S-3 — Build the Executive Agency and activate it"))

    def test_an_agent_output_is_not_a_founder_goal(self):
        record = "docs/architecture/agency/operations/w4-s2-plan-delegation/s2-run.result.json"
        self.assertIsNotNone(ac.founder_goal_refusal("s2-run.result", record, "x"))

    def test_a_non_founder_act_is_not_a_founder_goal(self):
        self.assertIn("no verbatim Founder content", ac.founder_goal_refusal(
            "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION",
            FD_RECORD, "x"))


class AFakeOrChangedInstrumentIsRefused(unittest.TestCase):
    """In a temporary repository: what an agent could write is never enough."""

    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="founder-"))
        (self.repo / "docs/governance/acts").mkdir(parents=True)
        self.register = self.repo / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
        self.body = "\nDIRECTIVE\n\nShip the thing.\n"

    def tearDown(self):
        shutil.rmtree(self.repo)

    def act(self, name, header="**Received:** from the Founder (Moriarty)."):
        path = self.repo / f"docs/governance/acts/{name}.md"
        path.write_text(f"# {name}\n\n{header}\n\n````text{self.body}\n````\n", encoding="utf-8")
        return f"docs/governance/acts/{name}.md"

    def refuse(self, name, record, statement="Ship the thing."):
        return ac.founder_goal_refusal(name, record, statement, repo_root=self.repo,
                                       register=self.register)

    def registered(self, *lines):
        self.register.write_text("\n".join(lines), encoding="utf-8")

    def test_an_unregistered_act_is_refused(self):
        record = self.act("DIR-X")
        self.registered("nothing here")
        self.assertIn("not recorded in the Decision Register", self.refuse("DIR-X", record))

    def test_registered_with_its_hash_is_accepted(self):
        import hashlib
        record = self.act("DIR-X")
        self.registered("DIR-X", hashlib.sha256(self.body.encode()).hexdigest())
        self.assertIsNone(self.refuse("DIR-X", record))

    def test_changed_content_is_refused(self):
        import hashlib
        record = self.act("DIR-X")
        self.registered("DIR-X", hashlib.sha256(b"\nother\n").hexdigest())
        self.assertIn("not the registered content", self.refuse("DIR-X", record))

    def test_a_message_not_from_the_founder_is_refused(self):
        import hashlib
        record = self.act("DIR-X", header="**Written by:** an agent.")
        self.registered("DIR-X", hashlib.sha256(self.body.encode()).hexdigest())
        self.assertIn("not recorded as a message from the Founder", self.refuse("DIR-X", record))


class TheChainFromFounderGoalToAgent(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="s3-"))
        self.registry = AgentInstanceRegistry(self.root)
        self.registry.register(
            instance_key=INSTANCE, definition=SELECTED_DEFINITION,
            permitted_capabilities=("engineering-intelligence",),
            created_by=w4.AUTHORIZED_DELEGATOR,
            authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
            accountable_to=w4.AUTHORIZED_DELEGATOR)
        self.delegations = w4.W4DelegationRegistry(self.registry, self.root)
        self.surface = PlanningSurface()
        self.goal = self.surface.declare(Goal(
            key="founder-s3", statement=S3_GOAL,
            authority=AuthorityProvenance(S3_ID, S3_RECORD)))
        self.plan = self.surface.adopt(Plan(
            key="founder-s3-plan-0", goal_key="founder-s3", authority=CEO, steps=(
                PlanStep("verify", "Verify the Founder Goal check.", requires_delegation=True),
                PlanStep("review", "Review the result (CEO).", depends_on=("verify",)))))

    def tearDown(self):
        shutil.rmtree(self.root)

    def issue(self, **over):
        kw = dict(delegator=w4.AUTHORIZED_DELEGATOR, recipient_instance=INSTANCE,
                  authority=FD9, capability_scope=("engineering-intelligence",), **TERMS)
        kw.update(over)
        return w4.issue_from_plan(self.delegations, self.surface, self.plan, "verify", **kw)

    def test_goal_and_plan_stay_distinct_and_the_founder_goal_verifies(self):
        self.assertNotEqual(self.goal.authority, self.plan.authority)
        grant = self.issue()
        prov = w4.plan_provenance(grant.to_payload(), self.surface)
        self.assertEqual("VERIFIED", prov["founder_goal"])
        self.assertEqual(S3_GOAL, prov["goal_statement"])
        self.assertEqual([], prov["faults"])

    def test_a_fresh_process_answers_why_the_agent_has_this_work(self):
        grant = self.issue()
        planning_continuity.save(self.surface, self.root / "planning.state.json")
        script = (
            "import json; from pathlib import Path;"
            "from tools.w4_continuity import reconstruct;"
            "from tools import planning_continuity, w4_delegation as w4;"
            f"root=Path({str(self.root)!r}); s=reconstruct(root);"
            "surface=planning_continuity.restore(root/'planning.state.json');"
            "rec=json.loads((root/(s['active_grants'][0]+'.delegation.json')).read_text());"
            "print(json.dumps({'rec':rec,'prov':w4.plan_provenance(rec,surface)}))")
        out = json.loads(subprocess.run([sys.executable, "-c", script], cwd=REPO,
                                        capture_output=True, text=True, check=True).stdout)
        self.assertEqual(grant.delegation_id, out["rec"]["delegation_id"])
        self.assertEqual(INSTANCE, out["rec"]["recipient_instance"])
        self.assertEqual("VERIFIED", out["prov"]["founder_goal"])
        self.assertIn(S3_RECORD, out["prov"]["goal_authority"])

    def test_the_founder_goal_cannot_be_redeclared_with_other_words(self):
        with self.assertRaises(InvalidPlan):
            self.surface.declare(Goal(key="founder-s3", statement="Something else.",
                                      authority=AuthorityProvenance(S3_ID, S3_RECORD)))

    def test_planning_itself_cannot_issue(self):
        requirement = self.surface.delegation_requirements(self.plan)[0]
        self.assertFalse(hasattr(requirement, "delegator"))
        with self.assertRaises(NotImplementedError):
            requirement.as_delegation_record()

    def test_an_agent_or_a_candidate_name_cannot_issue(self):
        for actor in (INSTANCE, "Monkey D. Luffy", "Luffy (CEO)"):
            with self.assertRaisesRegex(w4.DelegationError, "not the authorized W4 delegator"):
                self.issue(delegator=actor)

    def test_a_candidate_without_an_instance_is_not_an_agent(self):
        for candidate in ("usopp", "franky", "nico-robin"):
            with self.assertRaisesRegex(w4.DelegationError, "not a registered"):
                self.issue(recipient_instance=candidate)

    def test_scope_cannot_be_widened_from_the_goal(self):
        with self.assertRaises(TypeError):
            self.issue(work_scope=("verify", "review"))

    def test_a_founder_reserved_instrument_is_not_delegation_authority(self):
        with self.assertRaisesRegex(w4.DelegationError, "must cite FD-P11-001"):
            self.issue(authority=AuthorityProvenance(S3_ID, S3_RECORD))


if __name__ == "__main__":
    unittest.main()
