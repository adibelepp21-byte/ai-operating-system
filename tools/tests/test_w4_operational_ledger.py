"""The live W4 operational ledger (`FD-AGENCY-001` S-1, Q-S1-A = A2).

Certified delegation records stay immutable; a disposition beside them records
what became of the grant. These tests run against temporary roots, except the
last class, which reads the certified P11 roots and writes nothing.
"""
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools import w4_delegation as w4
from tools.p12_certified_evidence_guard import CertifiedEvidenceProtected
from tools.w4_continuity import continuation_conditions, reconstruct

REPO = Path(__file__).resolve().parents[2]
P11 = REPO / "docs/architecture/p11"
DELEGATOR = w4.AUTHORIZED_DELEGATOR


def _grant(gid, status="ACTIVE", scope=("step-a",)):
    return {
        "delegation_id": gid, "delegator": DELEGATOR,
        "recipient_instance": "instance-001", "status": status,
        "work_scope": list(scope), "accountable_party": DELEGATOR,
        "lifecycle_boundary": "one execution of plan demo-plan-0",
        "termination_condition": "on completion of the bound plan, or revocation",
        "authority_instrument": "FD-P11-001 §9",
    }


def _evidence(gid, outcomes, escalations=(), terminal="WorkflowState.SUCCEEDED"):
    return {"plan": "demo-plan-0", "delegation_id": gid, "executed_at": "2026-09-11T00:00:00",
            "outcomes": [{"step": s, "status": st} for s, st in outcomes],
            "escalations": list(escalations), "workflow_terminal_state": terminal}


class _Roots(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="w4-ledger-"))
        self.root = self.tmp / "ops"
        self.ledger = self.tmp / "ledger"
        self.root.mkdir()
        (self.root / "instance-001.instance.json").write_text(json.dumps(
            {"instance_key": "instance-001", "lifecycle": "REGISTERED"}))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write(self, name, payload):
        path = self.root / name
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    def sha(self, path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def complete(self, gid="g1"):
        return w4.record_disposition(self.root, gid, disposition=w4.COMPLETED,
                                     delegator=DELEGATOR, reason="bound plan completed",
                                     ledger=self.ledger)


class CompletionIsComputedNotAsserted(_Roots):
    def test_a_completed_plan_closes_and_the_history_is_untouched(self):
        record = self.write("g1.delegation.json", _grant("g1"))
        self.write("run.evidence.json", _evidence("g1", [("step-a", "success")]))
        before = self.sha(record)
        self.complete()
        self.assertEqual(before, self.sha(record))
        state = reconstruct(self.root, operational_ledger=self.ledger)
        self.assertEqual([], state["active_grants"])
        self.assertEqual(["g1"], state["historical_active_grants"])
        self.assertEqual({"g1": "COMPLETED"}, state["operational_dispositions"])
        self.assertEqual(["g1"], state["completed_grants"])
        self.assertEqual([], state["disposition_faults"])

    def test_the_default_reading_is_the_historical_one(self):
        self.write("g1.delegation.json", _grant("g1"))
        self.write("run.evidence.json", _evidence("g1", [("step-a", "success")]))
        without = reconstruct(self.root)
        self.complete()
        self.assertEqual(without, reconstruct(self.root))
        self.assertEqual(["g1"], reconstruct(self.root)["active_grants"])
        self.assertNotIn("operational_dispositions", reconstruct(self.root))

    def test_an_escalated_plan_is_not_completed(self):
        self.write("g1.delegation.json", _grant("g1"))
        self.write("run.evidence.json", _evidence(
            "g1", [("step-a", "success"), ("step-b", "escalation")], escalations=["e1"]))
        with self.assertRaisesRegex(w4.DelegationError, "not every plan step succeeded"):
            self.complete()
        self.assertFalse(self.ledger.exists())

    def test_a_failed_workflow_is_not_completed(self):
        self.write("g1.delegation.json", _grant("g1"))
        self.write("run.evidence.json", _evidence(
            "g1", [("step-a", "success")], terminal="WorkflowState.FAILED"))
        with self.assertRaisesRegex(w4.DelegationError, "SUCCEEDED"):
            self.complete()

    def test_no_evidence_is_not_completion(self):
        self.write("g1.delegation.json", _grant("g1"))
        with self.assertRaisesRegex(w4.DelegationError, "0 evidence records"):
            self.complete()

    def test_a_grant_without_a_completion_clause_cannot_complete(self):
        grant = _grant("g1")
        grant["termination_condition"] = "on revocation only"
        self.write("g1.delegation.json", grant)
        self.write("run.evidence.json", _evidence("g1", [("step-a", "success")]))
        with self.assertRaisesRegex(w4.DelegationError, "completion of the bound plan"):
            self.complete()


class TheLedgerIsBoundedAndAppendOnly(_Roots):
    def setUp(self):
        super().setUp()
        self.record = self.write("g1.delegation.json", _grant("g1"))
        self.evidence = self.write("run.evidence.json",
                                   _evidence("g1", [("step-a", "success")]))

    def test_only_the_authorized_delegator_records(self):
        with self.assertRaisesRegex(w4.DelegationError, "only"):
            w4.record_disposition(self.root, "g1", disposition=w4.COMPLETED,
                                  delegator="instance-001", reason="x", ledger=self.ledger)

    def test_a_historically_revoked_grant_is_never_reinterpreted(self):
        self.write("g2.delegation.json", _grant("g2", status="REVOKED"))
        with self.assertRaisesRegex(w4.DelegationError, "never over a revoked one"):
            w4.record_disposition(self.root, "g2", disposition=w4.REVOKED,
                                  delegator=DELEGATOR, reason="x", ledger=self.ledger)

    def test_append_only(self):
        self.complete()
        with self.assertRaisesRegex(w4.DelegationError, "append-only"):
            self.complete()

    def test_unknown_disposition_and_empty_reason_are_refused(self):
        with self.assertRaises(w4.DelegationError):
            w4.record_disposition(self.root, "g1", disposition="DONE",
                                  delegator=DELEGATOR, reason="x", ledger=self.ledger)
        with self.assertRaises(w4.DelegationError):
            w4.record_disposition(self.root, "g1", disposition=w4.REVOKED,
                                  delegator=DELEGATOR, reason=" ", ledger=self.ledger)

    def test_a_persisted_grant_can_be_withdrawn_without_rewriting_it(self):
        """C-2: the in-process registry cannot reach this grant; the ledger can."""
        before = self.sha(self.record)
        w4.record_disposition(self.root, "g1", disposition=w4.REVOKED,
                              delegator=DELEGATOR, reason="withdrawn", ledger=self.ledger)
        state = reconstruct(self.root, operational_ledger=self.ledger)
        self.assertEqual(["g1"], state["operationally_revoked_grants"])
        self.assertEqual([], state["active_grants"])
        self.assertEqual(before, self.sha(self.record))

    def test_a_ledger_inside_a_certified_root_is_refused_before_anything_is_created(self):
        ledger = P11 / "w4-dispositions-negative-control"
        with self.assertRaises(CertifiedEvidenceProtected):
            self.complete_into(ledger)
        self.assertFalse(ledger.exists())

    def complete_into(self, ledger):
        return w4.record_disposition(self.root, "g1", disposition=w4.COMPLETED,
                                     delegator=DELEGATOR, reason="x", ledger=ledger)


class AChangedBasisIsAFaultNotAClosure(_Roots):
    def setUp(self):
        super().setUp()
        self.record = self.write("g1.delegation.json", _grant("g1"))
        self.evidence = self.write("run.evidence.json",
                                   _evidence("g1", [("step-a", "success")]))
        self.complete()

    def assert_faulted(self, fragment):
        state = reconstruct(self.root, operational_ledger=self.ledger)
        self.assertEqual(["g1"], state["active_grants"])
        self.assertEqual({}, state["operational_dispositions"])
        self.assertIn(fragment, " ".join(state["disposition_faults"]))
        self.assertTrue(continuation_conditions(state)[0].startswith("DISPOSITION FAULTS"))

    def test_a_changed_delegation_record(self):
        self.record.write_text(self.record.read_text() + " ", encoding="utf-8")
        self.assert_faulted("delegation record changed")

    def test_changed_evidence(self):
        self.evidence.write_text(self.evidence.read_text() + " ", encoding="utf-8")
        self.assert_faulted("evidence record changed")

    def test_a_forged_recorder(self):
        path = w4._disposition_path(self.ledger, self.root, "g1")
        item = json.loads(path.read_text())
        item["recorded_by"] = "instance-001"
        path.write_text(json.dumps(item))
        self.assert_faulted("not recorded by the authorized delegator")

    def test_an_unreadable_disposition(self):
        w4._disposition_path(self.ledger, self.root, "g1").write_text("{")
        self.assert_faulted("unreadable")


class TheCertifiedLedgerReadsAsS1Found(unittest.TestCase):
    """Read-only over the certified P11 roots: the evaluation matches S-1."""

    def test_completion_is_established_for_exactly_three_grants(self):
        expected = {("w1-operations", "4daebea9012d4cc7"): True,
                    ("w4-operations", "4313bd2246124a94"): False,
                    ("x-department-operations", "0f7ac0785bd8442b"): True,
                    ("x-department-operations", "a437cdbbd29940af"): True}
        for (root, gid), met in expected.items():
            record = json.loads((P11 / root / f"{gid}.delegation.json").read_text())
            self.assertEqual(met, w4.plan_completion(P11 / root, record)[0], gid)

    def test_the_live_ledger_is_outside_every_certified_root(self):
        from tools.p12_certified_evidence_guard import is_protected
        self.assertFalse(is_protected(w4.LIVE_LEDGER))



class EscalationResponsesStayOutsideCertifiedEvidence(unittest.TestCase):
    """F-S1-4 / B1: a response to a certified-root escalation is routed outside."""

    ROOT = P11 / "w4-operations"
    ESC = "23f315ba9f504272"

    def setUp(self):
        from native_core.core.governance import HumanAuthority
        from tools.escalation_register import EscalationRegister, EscalationRegisterError
        self.Register, self.Error = EscalationRegister, EscalationRegisterError
        self.human = HumanAuthority("test reviewer")
        self.tmp = Path(tempfile.mkdtemp(prefix="responses-"))
        self.beside = self.ROOT / f"{self.ESC}.response.json"
        self.certified = hashlib.sha256(
            (self.ROOT / f"{self.ESC}.escalation.json").read_bytes()).hexdigest()

    def tearDown(self):
        shutil.rmtree(self.tmp)
        self.assertFalse(self.beside.exists())
        self.assertEqual(self.certified, hashlib.sha256(
            (self.ROOT / f"{self.ESC}.escalation.json").read_bytes()).hexdigest())

    def test_without_a_ledger_the_response_is_refused_not_written_in_place(self):
        with self.assertRaisesRegex(self.Error, "certified evidence"):
            self.Register(self.ROOT).record_response(
                self.ESC, authority=self.human, response="x")

    def test_with_a_ledger_it_is_written_outside_and_read_only_on_request(self):
        path = self.Register(self.ROOT, self.tmp).record_response(
            self.ESC, authority=self.human, response="acknowledged", basis="test")
        self.assertTrue(path.is_relative_to(self.tmp))
        self.assertEqual("OPEN", self.Register(self.ROOT).status(self.ESC))
        self.assertEqual("ANSWERED", self.Register(self.ROOT, self.tmp).status(self.ESC))
        self.assertIn(self.ESC, reconstruct(self.ROOT)["open_escalations"])
        self.assertEqual([], reconstruct(self.ROOT, response_ledger=self.tmp)["open_escalations"])

    def test_append_only(self):
        register = self.Register(self.ROOT, self.tmp)
        register.record_response(self.ESC, authority=self.human, response="a")
        with self.assertRaisesRegex(self.Error, "append-only"):
            register.record_response(self.ESC, authority=self.human, response="b")

    def test_a_response_bound_to_other_bytes_is_not_honoured(self):
        path = self.Register(self.ROOT, self.tmp).record_response(
            self.ESC, authority=self.human, response="a")
        item = json.loads(path.read_text())
        item["escalation_record_sha256"] = "0" * 64
        path.write_text(json.dumps(item))
        self.assertEqual("OPEN", self.Register(self.ROOT, self.tmp).status(self.ESC))

    def test_automation_still_cannot_respond(self):
        with self.assertRaises(self.Error):
            self.Register(self.ROOT, self.tmp).record_response(
                self.ESC, authority="Claude Code", response="x")


class UncertifiedEscalationsAreAnsweredAsBefore(unittest.TestCase):
    def test_the_response_is_written_beside_and_its_shape_is_unchanged(self):
        from native_core.core.governance import HumanAuthority
        from tools.escalation_register import EscalationRegister
        tmp = Path(tempfile.mkdtemp(prefix="esc-"))
        try:
            (tmp / "e1.escalation.json").write_text(json.dumps({"escalation_id": "e1"}))
            path = EscalationRegister(tmp).record_response(
                "e1", authority=HumanAuthority("r"), response="ok")
            self.assertEqual(tmp / "e1.response.json", path)
            self.assertEqual({"escalation_id", "responded_by", "response", "responded_at"},
                             set(json.loads(path.read_text())))
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
