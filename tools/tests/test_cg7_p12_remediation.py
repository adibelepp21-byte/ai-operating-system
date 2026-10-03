"""FD-CG7-001 remediation: R-1…R-4, the P12 disposition scopes, and their controls.

Temporary roots for everything written. The resident roots are only read.
"""
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from native_core.core.governance import HumanAuthority
from tools import w4_delegation as w4
from tools.agent_instance_registry import AgentInstanceRegistry
from tools.delegation_catalog import all_operation_roots, operation_roots
from tools.escalation_register import LIVE_RESPONSES, EscalationRegister
from tools.p12_certified_evidence_guard import CertifiedEvidenceProtected
from tools.planning import AuthorityProvenance
from tools.w4_continuity import CURRENT, HISTORICAL, operational_overview, reconstruct
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION

REPO = Path(__file__).resolve().parents[2]
P11_W4 = REPO / "docs/architecture/p11/w4-operations"
P12_W4 = REPO / "docs/architecture/p12/w4-operations"
P12_W3 = REPO / "docs/architecture/p12/w3-operations"
DELEGATOR = w4.AUTHORIZED_DELEGATOR
FQ1 = ("FD-CG7-001 FQ-CG7-1", w4.FD_CG7_RECORD)
FQ2 = ("FD-CG7-001 FQ-CG7-2", w4.FD_CG7_RECORD)


def _grant(gid, *, recipient="instance-001", plan="demo-plan-0",
           termination="on completion of the bound plan, or revocation"):
    return {"delegation_id": gid, "delegator": DELEGATOR, "recipient_instance": recipient,
            "status": "ACTIVE", "work_scope": ["step-a"], "accountable_party": DELEGATOR,
            "lifecycle_boundary": f"one execution of plan {plan}",
            "termination_condition": termination, "authority_instrument": "FD-P11-001 §9"}


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class _Tmp(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="cg7-"))
        self.ledger = self.tmp / "ledger"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def root(self, *parts, grants=("g1",), registered=True, **kw):
        root = self.tmp.joinpath(*parts)
        root.mkdir(parents=True)
        if registered:
            (root / "instance-001.instance.json").write_text(json.dumps(
                {"instance_key": "instance-001", "lifecycle": "REGISTERED"}))
        for gid in grants:
            (root / f"{gid}.delegation.json").write_text(json.dumps(_grant(gid, **kw), indent=2))
        return root


class R1_SameBasenameIsNotTheSameLedgerIdentity(_Tmp):
    def test_p11_w4_and_p12_w4_have_different_identities(self):
        self.assertEqual(P11_W4.name, P12_W4.name)
        self.assertNotEqual(w4.ledger_identity(P11_W4), w4.ledger_identity(P12_W4))
        self.assertNotEqual(w4.ledger_folder(w4.LIVE_LEDGER, P11_W4),
                            w4.ledger_folder(w4.LIVE_LEDGER, P12_W4))

    def test_a_disposition_for_one_root_is_invisible_to_its_namesake(self):
        a, b = self.root("a", "ops"), self.root("b", "ops")
        w4.record_disposition(a, "g1", disposition=w4.REVOKED, delegator=DELEGATOR,
                              reason="withdrawn", ledger=self.ledger)
        self.assertEqual(["g1"], list(w4.read_dispositions(a, self.ledger)[0]))
        self.assertEqual(({}, ()), w4.read_dispositions(b, self.ledger))
        self.assertEqual(["g1"], reconstruct(b, operational_ledger=self.ledger)["active_grants"])

    def test_a_pre_r1_entry_stays_where_it_is_and_is_attributed_by_its_recorded_root(self):
        a, b = self.root("a", "ops"), self.root("b", "ops")
        legacy = self.ledger / "ops" / "g1.disposition.json"
        legacy.parent.mkdir(parents=True)
        legacy.write_text(json.dumps({
            "delegation_id": "g1", "root": w4._rel(a), "disposition": w4.REVOKED,
            "record_sha256": _sha(a / "g1.delegation.json"), "recorded_by": DELEGATOR,
            "authority_instrument": w4.DISPOSITION_AUTHORITY[0],
            "authority_record": w4.DISPOSITION_AUTHORITY[1]}))
        self.assertEqual(["g1"], list(w4.read_dispositions(a, self.ledger)[0]))
        self.assertEqual(({}, ()), w4.read_dispositions(b, self.ledger))
        with self.assertRaisesRegex(w4.DelegationError, "append-only"):
            w4.record_disposition(a, "g1", disposition=w4.REVOKED, delegator=DELEGATOR,
                                  reason="again", ledger=self.ledger)

    def test_a_response_for_one_root_does_not_answer_its_namesake(self):
        a, b = self.root("a", "ops", grants=()), self.root("b", "ops", grants=())
        for root in (a, b):
            (root / "e1.escalation.json").write_text(json.dumps({"escalation_id": "e1"}))
        legacy = self.ledger / "ops" / "e1.response.json"
        legacy.parent.mkdir(parents=True)
        legacy.write_text(json.dumps({"escalation_id": "e1", "root": w4._rel(a),
                                      "escalation_record_sha256": _sha(a / "e1.escalation.json")}))
        self.assertEqual("ANSWERED", EscalationRegister(a, self.ledger).status("e1"))
        self.assertEqual("OPEN", EscalationRegister(b, self.ledger).status("e1"))

    def test_the_resident_p11_reading_is_unchanged_and_p12_has_no_spurious_fault(self):
        valid, faults = w4.read_dispositions(P11_W4)
        self.assertEqual({"4313bd2246124a94": "REVOKED"},
                         {k: v["disposition"] for k, v in valid.items()})
        self.assertEqual((), faults)
        self.assertEqual("ANSWERED", EscalationRegister(
            P11_W4, LIVE_RESPONSES).status("23f315ba9f504272"))
        self.assertEqual((), w4.read_dispositions(P12_W4)[1])


class R2_EveryPhaseIsVisibleAndP11DiscoveryDoesNotMove(unittest.TestCase):
    def test_the_p11_population_is_unchanged(self):
        self.assertEqual([p.name for p in operation_roots()],
                         ["w1-operations", "w4-operations", "x-department-operations"])
        self.assertTrue(all("p11" in str(p) for p in operation_roots()))

    def test_p12_and_agency_roots_are_discovered(self):
        found = {w4._rel(p) for p in all_operation_roots()}
        for root in (P11_W4, P12_W4, P12_W3):
            self.assertIn(w4._rel(root), found)
        self.assertIn("docs/architecture/agency/operations/w4-s3-founder-goal", found)
        self.assertFalse(any("w4-dispositions" in r or "escalation-responses" in r for r in found))


class R3_HistoricalRecordVersusCurrentGrant(_Tmp):
    def test_active_with_a_registered_recipient_is_current(self):
        root = self.root("ops")
        grant = operational_overview([root])["grants"][f"{w4._rel(root)}/g1"]
        self.assertEqual((True, CURRENT), (grant["executable"], grant["classification"]))

    def test_active_without_a_registered_recipient_is_not_executable(self):
        root = self.root("ops", registered=False)
        grant = operational_overview([root])["grants"][f"{w4._rel(root)}/g1"]
        self.assertEqual(("ACTIVE", "ACTIVE", False, HISTORICAL),
                         (grant["historical_status"], grant["operational_status"],
                          grant["executable"], grant["classification"]))

    def test_an_escalation_is_blocking_only_behind_a_current_grant_and_never_reported_answered(self):
        root = self.root("ops", grants=("g1", "g2"))
        for eid, gid in (("e1", "g1"), ("e2", "g2")):
            (root / f"{eid}.escalation.json").write_text(json.dumps({"escalation_id": eid}))
            (root / f"{eid}.governance-join.json").write_text(
                json.dumps({"escalation_id": eid, "delegation_id": gid}))
        with mock.patch.object(w4, "LIVE_LEDGER", self.ledger):
            w4.record_disposition(root, "g2", disposition=w4.REVOKED, delegator=DELEGATOR,
                                  reason="withdrawn", ledger=self.ledger)
            view = operational_overview([root])
        e1, e2 = (view["escalations"][f"{w4._rel(root)}/{e}"] for e in ("e1", "e2"))
        self.assertEqual("OPEN — BLOCKING CURRENT WORK", e1["classification"])
        self.assertEqual("OPEN — HISTORICAL (its grant is not current)", e2["classification"])
        self.assertEqual(("OPEN", "OPEN"), (e2["historical_state"], e2["operational_state"]))


class R4_PlanCompletionReadsTheP12Form(_Tmp):
    def manifest(self, folder, name, **fields):
        folder.mkdir(exist_ok=True)
        payload = {"plan": "demo-plan-0", "delegation_id": "g1", "status": "success",
                   "work_scope": ["step-a"], "outcome": {"unsatisfied": []}}
        payload.update(fields)
        (folder / f"{name}.manifest.json").write_text(json.dumps(payload))

    def completion(self, folder, **kw):
        record = _grant("g1", **kw)
        root = self.tmp / "ops"
        root.mkdir(exist_ok=True)
        with mock.patch("tools.p12_execution_provenance.MANIFEST_ROOT", folder):
            return w4.plan_completion(root, record)

    def test_the_p12_clause_names_the_bound_plan(self):
        record = _grant("g1", termination="on completion of plan demo-plan-0")
        self.assertTrue(w4._names_completion(record, "demo-plan-0"))
        other = _grant("g1", termination="on completion of plan other-plan-0")
        self.assertFalse(w4._names_completion(other, "demo-plan-0"))

    def test_a_successful_manifest_completes(self):
        folder = self.tmp / "manifests"
        self.manifest(folder, "m1")
        met, path, reasons = self.completion(folder, termination="on completion of plan demo-plan-0")
        self.assertTrue(met, reasons)
        self.assertEqual("m1.manifest.json", path.name)

    def test_a_failed_status_alone_does_not_complete(self):
        folder = self.tmp / "manifests"
        self.manifest(folder, "m1", status="failure")
        met, _, reasons = self.completion(folder)
        self.assertFalse(met)
        self.assertIn("'failure'", " ".join(reasons))

    def test_a_failed_or_ambiguous_manifest_does_not(self):
        folder = self.tmp / "manifests"
        self.manifest(folder, "m1", status="failure", outcome={"unsatisfied": ["x"]})
        self.assertFalse(self.completion(folder)[0])
        self.manifest(folder, "m2")
        met, _, reasons = self.completion(folder)
        self.assertFalse(met)
        self.assertIn("2 execution manifests", " ".join(reasons))

    def test_the_resident_p12_grants_read_as_their_evidence_says(self):
        def met(gid):
            record = json.loads((P12_W4 / f"{gid}.delegation.json").read_text())
            return w4.plan_completion(P12_W4, record)[0]
        self.assertTrue(met("e668a317fa494342"))          # manifest 001, success 14/14
        for gid in ("b304c7ecb1024454", "332d42f021764ab6", "2494015de36246fd",
                    "aa591daf55ca4714"):
            self.assertFalse(met(gid), gid)               # failure · none · escalated · none


class TheP12ScopesGrantNothingNew(_Tmp):
    """FD-CG7-001 reaches exactly its grants, root and disposition."""

    def test_out_of_scope_uses_are_refused_before_anything_is_written(self):
        root = self.root("ops")
        cases = [
            (dict(authority=FQ1), "does not reach root"),
            (dict(authority=("FD-CG7-001 FQ-CG7-9", w4.FD_CG7_RECORD)), "not an instrument"),
            (dict(authority=FQ1, delegator="engineering-intelligence-instance-001"),
             "only 'Claude Code"),
        ]
        for kw, message in cases:
            args = dict(disposition=w4.REVOKED, delegator=DELEGATOR, reason="x",
                        ledger=self.ledger)
            args.update(kw)
            with self.subTest(message), self.assertRaisesRegex(w4.DelegationError, message):
                w4.record_disposition(root, "g1", **args)
        for gid, disposition, message in (("0a697039a63f4c17", w4.REVOKED, "does not reach grant"),
                                          ("e668a317fa494342", w4.COMPLETED, "authorizes")):
            with self.subTest(gid):
                self.assertIn(message, w4._scope_refusal(FQ1, P12_W4, gid, disposition) or "")
        self.assertFalse(self.ledger.exists())

    def test_a_forged_entry_claiming_the_p12_instrument_elsewhere_is_a_fault(self):
        root = self.root("ops")
        path = w4._disposition_path(self.ledger, root, "g1")
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({
            "delegation_id": "g1", "root": w4._rel(root), "disposition": w4.REVOKED,
            "record_sha256": _sha(root / "g1.delegation.json"), "recorded_by": DELEGATOR,
            "authority_instrument": FQ1[0], "authority_record": FQ1[1]}))
        valid, faults = w4.read_dispositions(root, self.ledger)
        self.assertEqual({}, valid)
        self.assertIn("does not reach root", " ".join(faults))


class NoWriteIntoCertifiedEvidence(unittest.TestCase):
    def setUp(self):
        self.memory = AgentInstanceRegistry(None)
        self.memory.register(instance_key="engineering-intelligence-instance-001",
                             definition=SELECTED_DEFINITION,
                             permitted_capabilities=("engineering-intelligence",),
                             created_by=DELEGATOR,
                             authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
                             accountable_to=DELEGATOR)
        self.before = sorted((p.name, _sha(p)) for p in P12_W4.iterdir())

    def test_issuing_into_a_certified_root_is_refused_and_nothing_is_recorded(self):
        registry = w4.W4DelegationRegistry(self.memory, P12_W4)
        with self.assertRaises(CertifiedEvidenceProtected):
            registry.issue(delegator=DELEGATOR, recipient_instance="engineering-intelligence-instance-001",
                           authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
                           objective="o", capability_scope=("engineering-intelligence",),
                           work_scope=("s",), lifecycle_boundary="one execution of plan p",
                           resource_boundary="r", output_expectation="o",
                           verification_requirement="v", escalation_condition="e",
                           accountable_party=DELEGATOR, termination_condition="t")
        self.assertEqual((), registry.keys())
        self.assertEqual(self.before, sorted((p.name, _sha(p)) for p in P12_W4.iterdir()))

    def test_answering_a_historical_escalation_needs_a_human_and_is_never_automatic(self):
        register = EscalationRegister(P12_W3, LIVE_RESPONSES)
        with self.assertRaises(Exception):
            register.record_response("0991300404cf44d8", authority="Claude Code", response="x")
        self.assertEqual("OPEN", register.status("0991300404cf44d8"))


class TheRecordedP12State(unittest.TestCase):
    """After FD-CG7-001 was executed: history untouched, current state as decided."""

    NINE = w4.DISPOSITION_SCOPES[FQ1]["grants"]

    def test_history_still_reads_ten_active_and_three_open(self):
        self.assertEqual(10, len(reconstruct(P12_W4)["active_grants"]))
        self.assertEqual(["9cb90fa0787a478c"], reconstruct(P12_W4)["open_escalations"])
        self.assertEqual(2, len(reconstruct(P12_W3)["open_escalations"]))

    def test_every_p12_grant_is_operationally_revoked_under_its_own_instrument(self):
        valid, faults = w4.read_dispositions(P12_W4)
        self.assertEqual((), faults)
        self.assertEqual(set(self.NINE) | {"2494015de36246fd"}, set(valid))
        for gid, item in valid.items():
            self.assertEqual(w4.REVOKED, item["disposition"])
            expected = FQ2 if gid == "2494015de36246fd" else FQ1
            self.assertEqual(expected, (item["authority_instrument"], item["authority_record"]))

    def test_the_live_escalation_is_answered_by_the_founder_and_the_others_are_not(self):
        view = operational_overview()
        rel = w4._rel(P12_W4)
        self.assertEqual("ANSWERED", view["escalations"][f"{rel}/9cb90fa0787a478c"]["classification"])
        for eid in ("0991300404cf44d8", "9d6bc0ad47294ef0"):
            item = view["escalations"][f"{w4._rel(P12_W3)}/{eid}"]
            self.assertEqual(("OPEN", "OPEN — HISTORICAL (its grant is not current)"),
                             (item["operational_state"], item["classification"]))
        self.assertNotIn("2494015de36246fd", view["current_grants"])
        self.assertEqual([], view["blocking_escalations"])


if __name__ == "__main__":
    unittest.main()
