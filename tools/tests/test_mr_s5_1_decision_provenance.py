"""MR-S5-1: the delegator's decision, made explicit on the disposition record.

ACCEPT / REWORK / REJECT, the resulting plan and the rework target are persisted
and reconstructed without reading reason text. Temporary roots for everything
written; resident records are only read.
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
from tools.p12_certified_evidence_guard import CertifiedEvidenceProtected
from tools.w4_execution import ExecutionReport, W4Executor, persist_evidence
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION

REPO = Path(__file__).resolve().parents[2]
INSTANCE = "engineering-intelligence-instance-001"
DELEGATOR = w4.AUTHORIZED_DELEGATOR
CEO = AuthorityProvenance(
    "Co-Founder V2 A01 Executive Command",
    "docs/governance/AIOS_COFOUNDER_V2_REGISTRATION_AND_ACTIVATION_RECORD_v1.0.md")
FD9 = AuthorityProvenance("FD-P11-001 §9", FD_RECORD)
TERMS = dict(capability_scope=("engineering-intelligence",), resource_boundary="r",
             output_expectation="o", verification_requirement="v", escalation_condition="e")


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def text_free(item):
    """What a reader may use: every field except the reason."""
    return {k: v for k, v in item.items() if k != "reason"}


class _Loop(unittest.TestCase):
    """One goal; plan: a (delegated), b (delegated), review (CEO, after a and b)."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="mr-s5-1-"))
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
        self.surface.declare(Goal(key="g", statement="Prove the decisions.", authority=CEO))
        self.plan = self.surface.adopt(Plan(key="g-plan-0", goal_key="g", authority=CEO, steps=(
            PlanStep("a", "Establish A.", requires_delegation=True),
            PlanStep("b", "Establish B.", requires_delegation=True),
            PlanStep("review", "Review (CEO).", depends_on=("a", "b")))))
        self.grants = {}

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def grant(self, step, plan=None):
        plan = plan or self.surface.current("g")
        self.grants[step] = w4.issue_from_plan(
            self.delegations, self.surface, plan, step, delegator=DELEGATOR,
            recipient_instance=INSTANCE, authority=FD9, **TERMS)
        return self.grants[step]

    def execute(self, step, succeed=True, plan=None):
        plan = plan or self.surface.current("g")
        grant = self.grant(step, plan)

        def perform(s):
            if not succeed:
                raise AssertionError("3 of 14 criteria")
            return "14 of 14"
        report = ExecutionReport(outcomes=[W4Executor(grant, self.registry).execute_step(
            plan.step(step), perform)])
        persist_evidence(self.root, plan.key, grant, report)
        return grant

    def decide(self, grant, decision, **kw):
        kw.setdefault("reviewer", DELEGATOR)
        kw.setdefault("reason", "reviewed")
        return w4.review_result(self.root, grant.delegation_id, surface=self.surface,
                                decision=decision, ledger=self.ledger, **kw)

    def item(self, grant):
        return w4.read_dispositions(self.root, self.ledger)[0][grant.delegation_id]

    def outcome(self):
        return w4.plan_outcome(self.surface, "g", self.root, self.ledger)


class P1_Accept(_Loop):
    def test_accept_is_explicit_and_the_plan_completes(self):
        a, b = self.execute("a"), self.execute("b")
        self.decide(a, w4.ACCEPT)
        self.decide(b, w4.ACCEPT)
        item = text_free(self.item(a))
        self.assertEqual(("ACCEPT", "g-plan-0", None),
                         (item["decision"], item["resulting_plan"], item["rework_target"]))
        out = self.outcome()
        self.assertTrue(out["completed"])
        self.assertEqual(("ACCEPT", "EXPLICIT"), (out["versions"][0]["steps"][0]["grants"][0]["decision"],
                                                  out["versions"][0]["steps"][0]["grants"][0]["decision_provenance"]))
        self.assertEqual([], out["decision_faults"])


class P2_Rework(_Loop):
    def test_rework_names_the_revised_plan_and_the_step_that_redoes_the_work(self):
        a = self.execute("a", succeed=False)
        result = self.decide(a, w4.REWORK, rework_target="a-corrected", rework_steps=(
            PlanStep("a-corrected", "Establish A, corrected.", requires_delegation=True),
            PlanStep("b", "Establish B.", requires_delegation=True),
            PlanStep("review", "Review (CEO).", depends_on=("a-corrected", "b"))))
        item = text_free(self.item(a))
        self.assertEqual("REWORK", item["decision"])
        self.assertEqual("g-plan-0+1", item["resulting_plan"])
        self.assertEqual({"plan": "g-plan-0+1", "step": "a-corrected"}, item["rework_target"])
        self.assertEqual(result["resulting_plan"], self.surface.current("g").key)
        out = self.outcome()
        self.assertFalse(out["completed"])
        redo = out["versions"][1]["steps"][0]
        self.assertEqual({"plan": "g-plan-0", "step": "a", "grant": a.delegation_id}, redo["reworks"])
        self.assertEqual([], out["decision_faults"])
        # The rework, performed and accepted, completes the revised plan.
        self.decide(self.execute("a-corrected"), w4.ACCEPT)
        self.decide(self.execute("b"), w4.ACCEPT)
        self.assertTrue(self.outcome()["completed"])


class P3_Reject(_Loop):
    def test_reject_with_a_revised_path_that_does_not_redo_the_work(self):
        a = self.execute("a", succeed=False)
        self.decide(a, w4.REJECT, resulting_steps=(
            PlanStep("b", "Establish B.", requires_delegation=True),
            PlanStep("review", "Review (CEO).", depends_on=("b",))))
        item = text_free(self.item(a))
        self.assertEqual(("REJECT", "g-plan-0+1", None),
                         (item["decision"], item["resulting_plan"], item["rework_target"]))
        self.assertEqual(w4.REVOKED, item["disposition"])
        out = self.outcome()
        self.assertEqual([], out["decision_faults"])
        self.assertNotIn("a", [s["step"] for s in out["versions"][1]["steps"]])
        self.assertIsNone(out["versions"][1]["steps"][0]["reworks"])
        self.decide(self.execute("b"), w4.ACCEPT)
        self.assertTrue(self.outcome()["completed"])

    def test_reject_without_revision_leaves_the_step_unresolved(self):
        a = self.execute("a")
        self.decide(a, w4.REJECT)
        item = text_free(self.item(a))
        self.assertEqual(("REJECT", "g-plan-0", None),
                         (item["decision"], item["resulting_plan"], item["rework_target"]))
        out = self.outcome()
        self.assertFalse(out["completed"])
        self.assertEqual(w4.REVOKED, out["versions"][0]["steps"][0]["outcome"])


class NegativeControls(_Loop):
    def test_n1_n2_n3_an_agent_cannot_decide(self):
        a = self.execute("a")
        for decision, kw in ((w4.ACCEPT, {}), (w4.REJECT, {}),
                             (w4.REWORK, {"rework_target": "x", "rework_steps": (
                                 PlanStep("x", "x", requires_delegation=True),)})):
            with self.subTest(decision), self.assertRaisesRegex(w4.DelegationError,
                                                                "may not review"):
                self.decide(a, decision, reviewer=INSTANCE, **kw)
        with self.assertRaisesRegex(w4.DelegationError, "only 'Claude Code"):
            w4.record_disposition(self.root, a.delegation_id, disposition=w4.COMPLETED,
                                  delegator=INSTANCE, reason="x", ledger=self.ledger,
                                  authority=w4.DELEGATOR_REVIEW,
                                  provenance={"decision": w4.ACCEPT, "resulting_plan": "g-plan-0",
                                              "rework_target": None})
        self.assertFalse(self.ledger.exists())
        self.assertEqual(["g-plan-0"], [p.key for p in self.surface.history("g")])

    def test_n4_accept_without_valid_verification_is_refused(self):
        a = self.grant("a")
        with self.assertRaisesRegex(w4.DelegationError, "not established"):
            self.decide(a, w4.ACCEPT)
        b = self.execute("b", succeed=False)
        with self.assertRaisesRegex(w4.DelegationError, "not established"):
            self.decide(b, w4.ACCEPT)
        self.assertFalse(self.ledger.exists())

    def test_n5_n6_rework_needs_a_finding_a_revised_plan_and_a_valid_target(self):
        a = self.execute("a", succeed=False)
        steps = (PlanStep("x", "x", requires_delegation=True), PlanStep("ceo", "c", depends_on=("x",)))
        cases = [({"rework_target": "x"}, "what the work is sent back as"),
                 ({"rework_steps": steps}, "is not a step of the revised plan"),
                 ({"rework_steps": steps, "rework_target": "nope"}, "is not a step of the revised plan"),
                 ({"rework_steps": steps, "rework_target": "ceo"}, "is not delegated work")]
        for kw, message in cases:
            with self.subTest(message), self.assertRaisesRegex(w4.DelegationError, message):
                self.decide(a, w4.REWORK, **kw)
        b = self.execute("b")
        with self.assertRaisesRegex(w4.DelegationError, "needs a verification finding"):
            self.decide(b, w4.REWORK, rework_target="x", rework_steps=steps)
        self.assertFalse(self.ledger.exists())
        self.assertEqual(["g-plan-0"], [p.key for p in self.surface.history("g")])

    def test_n7_a_rework_target_in_another_plan_is_refused(self):
        bad = {"decision": w4.REWORK, "resulting_plan": "g-plan-0+1",
               "rework_target": {"plan": "other-plan", "step": "x"}}
        self.assertIn("belongs to plan 'other-plan'", w4.decision_fault(bad, w4.REVOKED))
        a = self.execute("a", succeed=False)
        with self.assertRaisesRegex(w4.DelegationError, "malformed decision provenance"):
            w4.record_disposition(self.root, a.delegation_id, disposition=w4.REVOKED,
                                  delegator=DELEGATOR, reason="x", ledger=self.ledger,
                                  authority=w4.DELEGATOR_REVIEW, provenance=bad)

    def test_n8_reject_cannot_become_rework(self):
        a = self.execute("a", succeed=False)
        with self.assertRaisesRegex(w4.DelegationError, "carries no rework target"):
            self.decide(a, w4.REJECT, rework_target="a")
        with self.assertRaisesRegex(w4.DelegationError, "redoing the same work is REWORK"):
            self.decide(a, w4.REJECT, resulting_steps=(
                PlanStep("a", "Establish A.", requires_delegation=True),))
        for bad in ({"decision": w4.REJECT, "resulting_plan": "p",
                     "rework_target": {"plan": "p", "step": "a"}},
                    {"decision": w4.REWORK, "resulting_plan": "p", "rework_target": None}):
            self.assertIsNotNone(w4.decision_fault(bad, w4.REVOKED))
        self.assertIsNotNone(w4.decision_fault(
            {"decision": w4.REJECT, "resulting_plan": "p", "rework_target": None}, w4.COMPLETED))
        self.assertFalse(self.ledger.exists())

    def test_n9_a_decision_rewrites_no_history(self):
        a = self.execute("a", succeed=False)
        evidence = self.root / f"{a.delegation_id}.evidence.json"
        record = self.root / f"{a.delegation_id}.delegation.json"
        before = (_sha(evidence), _sha(record))
        self.decide(a, w4.REJECT)
        self.assertEqual(before, (_sha(evidence), _sha(record)))
        with self.assertRaisesRegex(w4.DelegationError, "append-only"):
            self.decide(a, w4.REJECT)

    def test_n10_certified_evidence_is_never_reached(self):
        root = REPO / "docs/architecture/p11/x-department-operations"
        before = sorted((p.name, _sha(p)) for p in root.iterdir())
        with self.assertRaisesRegex(w4.DelegationError, "outside certified evidence"):
            w4.record_disposition(root, "0f7ac0785bd8442b", disposition=w4.COMPLETED,
                                  delegator=DELEGATOR, reason="x", ledger=self.ledger,
                                  authority=w4.DELEGATOR_REVIEW,
                                  provenance={"decision": w4.ACCEPT, "resulting_plan": "p",
                                              "rework_target": None})
        grant = self.execute("a")
        with self.assertRaises(CertifiedEvidenceProtected):
            w4.record_disposition(self.root, grant.delegation_id, disposition=w4.REVOKED,
                                  delegator=DELEGATOR, reason="x",
                                  ledger=REPO / "docs/architecture/p12/ledger-probe")
        self.assertEqual(before, sorted((p.name, _sha(p)) for p in root.iterdir()))
        self.assertFalse((REPO / "docs/architecture/p12/ledger-probe").exists())

    def test_n12_founder_authority_is_unchanged(self):
        a, b = self.execute("a"), self.execute("b")
        self.decide(a, w4.ACCEPT)
        self.decide(b, w4.ACCEPT)
        self.assertTrue(self.outcome()["founder_acceptance"].startswith("NOT RECORDED"))
        self.assertNotIn("founder", " ".join(inspect.signature(w4.review_result).parameters))
        self.assertEqual(("ACCEPT", "REWORK", "REJECT"), w4.DECISIONS)


class FreshProcess(_Loop):
    def test_n11_all_three_reconstruct_in_a_fresh_process_without_reason_text(self):
        a, b = self.execute("a", succeed=False), self.execute("b", succeed=False)
        self.decide(b, w4.REJECT)
        self.assertEqual("g-plan-0", self.surface.current("g").key)
        self.decide(a, w4.REWORK, rework_target="a2", rework_steps=(
            PlanStep("a2", "A again.", requires_delegation=True),
            PlanStep("review", "Review.", depends_on=("a2",))))
        c = self.execute("a2")
        self.decide(c, w4.ACCEPT)
        planning_continuity.save(self.surface, self.root / "planning.state.json")
        script = (
            "import json; from pathlib import Path;"
            "from tools import planning_continuity, w4_delegation as w4;"
            f"root=Path({str(self.root)!r}); ledger=Path({str(self.ledger)!r});"
            "valid,_=w4.read_dispositions(root, ledger);"
            "s=planning_continuity.restore(root/'planning.state.json');"
            "print(json.dumps({'items':{k:{f:v.get(f) for f in w4.PROVENANCE_FIELDS} "
            "for k,v in valid.items()},'outcome':w4.plan_outcome(s,'g',root,ledger)}))")
        out = json.loads(subprocess.run([sys.executable, "-c", script], cwd=REPO,
                                        capture_output=True, text=True, check=True).stdout)
        decisions = {k: v["decision"] for k, v in out["items"].items()}
        self.assertEqual({a.delegation_id: "REWORK", b.delegation_id: "REJECT",
                          c.delegation_id: "ACCEPT"}, decisions)
        self.assertEqual({"plan": "g-plan-0+1", "step": "a2"},
                         out["items"][a.delegation_id]["rework_target"])
        self.assertEqual([], out["outcome"]["decision_faults"])
        redo = next(s for s in out["outcome"]["versions"][1]["steps"] if s["step"] == "a2")
        self.assertEqual(a.delegation_id, redo["reworks"]["grant"])


class Legacy(unittest.TestCase):
    def test_pre_mr_s5_1_records_read_as_before_and_are_not_given_a_decision(self):
        p11 = REPO / "docs/architecture/p11/w4-operations"
        valid, faults = w4.read_dispositions(p11)
        self.assertEqual((), faults)
        item = valid["4313bd2246124a94"]
        self.assertNotIn("decision", item)
        self.assertEqual((None, "LEGACY (REVOKED: decision not recorded)"), w4._decision_of(item))
        x = w4.read_dispositions(REPO / "docs/architecture/p11/x-department-operations")[0]
        self.assertEqual((w4.ACCEPT, "LEGACY (derived: COMPLETED ⇒ ACCEPT)"),
                         w4._decision_of(x["0f7ac0785bd8442b"]))
        s4 = REPO / "docs/architecture/agency/operations/w4-s4-plan-outcome"
        surface = planning_continuity.restore(s4 / "planning.state.json")
        out = w4.plan_outcome(surface, "founder-s4-rework", s4)
        legacy = out["versions"][0]["steps"][0]["grants"][0]
        self.assertEqual((None, "LEGACY (REVOKED: decision not recorded)"),
                         (legacy["decision"], legacy["decision_provenance"]))
        self.assertEqual([], out["decision_faults"])
        self.assertEqual((), w4.read_dispositions(REPO / "docs/architecture/p12/w4-operations")[1])


class Mutations(_Loop):
    """Each mutation of a decision record, on a temporary copy, is detected."""

    def setUp(self):
        super().setUp()
        a = self.execute("a", succeed=False)
        self.decide(a, w4.REWORK, rework_target="a2", rework_steps=(
            PlanStep("a2", "A again.", requires_delegation=True),
            PlanStep("review", "Review.", depends_on=("a2",))))
        self.gid = a.delegation_id
        self.path = w4._disposition_path(self.ledger, self.root, self.gid)
        self.original = self.path.read_text()

    def mutate(self, change):
        item = json.loads(self.original)
        change(item)
        self.path.write_text(json.dumps(item))
        valid, faults = w4.read_dispositions(self.root, self.ledger)
        out = self.outcome()
        self.path.write_text(self.original)
        return valid, " ".join(faults), out

    def test_each_mutation_is_detected(self):
        cases = {
            "decision removed": (lambda i: i.pop("decision"), "decision None"),
            "decision changed to ACCEPT": (lambda i: i.update(decision="ACCEPT"),
                                           "is recorded as 'REVOKED'"),
            "resulting plan removed": (lambda i: i.pop("resulting_plan"), "names no resulting plan"),
            "rework target removed": (lambda i: i.update(rework_target=None),
                                      "REWORK names no rework target"),
            "target in another plan": (lambda i: i.update(rework_target={"plan": "g-plan-0",
                                                                         "step": "a2"}),
                                       "belongs to plan"),
        }
        for name, (change, message) in cases.items():
            with self.subTest(name):
                valid, faults, _ = self.mutate(change)
                self.assertNotIn(self.gid, valid)
                self.assertIn(message, faults)

    def test_a_broken_plan_step_relationship_is_detected(self):
        _, faults, out = self.mutate(lambda i: i.update(
            rework_target={"plan": "g-plan-0+1", "step": "review"}))
        self.assertEqual("", faults)
        self.assertIn("is not a delegated step", " ".join(out["decision_faults"]))
        _, _, out = self.mutate(lambda i: i.update(
            resulting_plan="g-plan-9", rework_target={"plan": "g-plan-9", "step": "a2"}))
        self.assertIn("is not on this goal", " ".join(out["decision_faults"]))

    def test_changed_verification_evidence_is_detected(self):
        evidence = self.root / f"{self.gid}.evidence.json"
        original = evidence.read_text()
        evidence.write_text(original + " ")
        valid, faults = w4.read_dispositions(self.root, self.ledger)
        evidence.write_text(original)
        self.assertNotIn(self.gid, valid)
        self.assertIn("evidence record changed", " ".join(faults))


if __name__ == "__main__":
    unittest.main()
