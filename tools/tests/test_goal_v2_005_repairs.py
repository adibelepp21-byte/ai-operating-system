"""`GOAL-V2-005` — repairs found by re-discovery, each shown able to fail.

* **Authority citation.** A W4 citation must reach `FD-P11-001` itself
  (`FD-P11-001 §24`). It is not enough to name it while pointing elsewhere.
* **Open escalations.** The self-model reports every resident escalation that
  the register holds OPEN, not only those under `p11`.
* **Phantom gates.** The corpus gate count is not inflated by examples written
  in execution records.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools import authority_citation as citation
from tools import derived_views as views
from tools import p12_self_model as model
from tools.agent_instance_registry import (
    AgentInstanceRegistry,
    InstanceRegistrationError,
)
from tools.planning import AuthorityProvenance
from tools.tests.test_w4_authority_chain import (
    AUTHORIZED_DELEGATOR,
    DEFINITION,
    FD,
    _delegation,
    _registered,
)
from tools.w4_delegation import DelegationError, W4DelegationRegistry

REPO_ROOT = Path(__file__).resolve().parents[2]
ID = "FD-P11-001"


class ACitationMustReachTheDecisionItNames(unittest.TestCase):

    def test_the_real_citation_reaches_it(self):
        self.assertIsNone(citation.refusal("FD-P11-001 §9", FD, ID))

    def test_naming_it_while_pointing_elsewhere_is_refused(self):
        for record in ("README.md",
                       "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md",
                       "docs/governance/acts/GOAL-V2-005-P13-COMPLETION-AND-"
                       "SYSTEMIC-GAP-CLOSURE.md"):
            with self.subTest(record):
                self.assertIsNotNone(citation.refusal("FD-P11-001 §9", record, ID))

    def test_the_identifier_must_be_a_whole_token(self):
        for instrument in ("FD-P11-0019", "NOT-FD-P11-001", "xFD-P11-001"):
            with self.subTest(instrument):
                self.assertIsNotNone(citation.refusal(instrument, FD, ID))

    def test_a_planted_act_that_the_register_does_not_record_is_refused(self):
        """A file in the acts directory is not a Founder Decision."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            acts = root / "docs/governance/acts"
            acts.mkdir(parents=True)
            (acts / "FD-P77-001-PLANTED.md").write_text("x", encoding="utf-8")
            register = root / "register.md"
            register.write_text("`FD-P77-0011` only", encoding="utf-8")
            why = citation.refusal(
                "FD-P77-001 §1", "docs/governance/acts/FD-P77-001-PLANTED.md",
                "FD-P77-001", repo_root=root, register=register)
            self.assertIn("not recorded in the Decision Register", why)
            register.write_text("`FD-P77-001` issued", encoding="utf-8")
            self.assertIsNone(citation.refusal(
                "FD-P77-001 §1", "docs/governance/acts/FD-P77-001-PLANTED.md",
                "FD-P77-001", repo_root=root, register=register))

    def test_an_unreadable_register_fails_closed(self):
        self.assertIn("cannot be read", citation.refusal(
            "FD-P11-001 §9", FD, ID, register=REPO_ROOT / "no-such-register.md"))


class TheW4RegistriesEnforceIt(unittest.TestCase):

    def _stack(self):
        registry = AgentInstanceRegistry()
        return registry, W4DelegationRegistry(registry), _registered(registry)

    def test_a_valid_delegation_is_still_issued(self):
        _, delegations, registration = self._stack()
        self.assertTrue(_delegation(delegations, registration.instance_key)
                        .delegation_id)

    def test_a_delegation_citing_a_different_file_is_refused(self):
        _, delegations, registration = self._stack()
        with self.assertRaises(DelegationError) as caught:
            delegations.issue(
                delegator=AUTHORIZED_DELEGATOR,
                recipient_instance=registration.instance_key,
                authority=AuthorityProvenance("FD-P11-001 §9", "README.md"),
                objective="o", capability_scope=("engineering-intelligence",),
                work_scope=("a",), lifecycle_boundary="l", resource_boundary="r",
                output_expectation="o", verification_requirement="v",
                escalation_condition="e", accountable_party=AUTHORIZED_DELEGATOR,
                termination_condition="t")
        self.assertIn("§24", str(caught.exception))

    def test_an_instance_citing_a_different_file_is_refused(self):
        registry = AgentInstanceRegistry()
        with self.assertRaises(InstanceRegistrationError):
            registry.register(
                instance_key="engineering-intelligence-instance-99",
                definition=DEFINITION,
                permitted_capabilities=("engineering-intelligence",),
                created_by=AUTHORIZED_DELEGATOR,
                authority=AuthorityProvenance(
                    "FD-P11-001 §7",
                    "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"),
                accountable_to=AUTHORIZED_DELEGATOR)

    def test_every_resident_delegation_and_instance_still_resolves(self):
        """The repair must not invalidate history. Every resident record's
        citation reaches the Decision it names."""
        records = [p for base in ("docs/architecture", "docs/operations")
                   for pattern in ("*.delegation.json", "*.instance.json")
                   for p in (REPO_ROOT / base).rglob(pattern)]
        self.assertGreater(len(records), 10)
        for path in records:
            record = json.loads(path.read_text(encoding="utf-8"))
            if "authority_record" not in record:
                continue
            with self.subTest(path.name):
                self.assertIsNone(citation.refusal(
                    record["authority_instrument"], record["authority_record"], ID))


class EveryResidentOpenEscalationIsReported(unittest.TestCase):

    def test_the_self_model_reports_what_the_register_holds_open(self):
        from tools.escalation_register import EscalationRegister
        expected = set()
        for path in (REPO_ROOT / "docs").rglob("*.escalation.json"):
            expected |= set(EscalationRegister(path.parent).open_escalations())
        answer = model.incomplete()
        self.assertEqual(set(answer.value["open_escalations"]), expected)
        self.assertIn("23f315ba9f504272", expected)
        self.assertGreaterEqual(len(expected), 4)

    def test_an_answered_escalation_is_not_reported_open(self):
        from native_core.core.governance import HumanAuthority
        from tools.escalation_register import EscalationRegister
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ops = root / "docs/operations/example"
            ops.mkdir(parents=True)
            for eid in ("aaaa", "bbbb"):
                (ops / f"{eid}.escalation.json").write_text(
                    json.dumps({"escalation_id": eid}), encoding="utf-8")
            (root / "docs/architecture").mkdir(parents=True)
            EscalationRegister(ops).record_response(
                "aaaa", authority=HumanAuthority("founder"), response="answered")
            original = views.unbridged_gates
            views.unbridged_gates = lambda root: []
            try:
                value = model.incomplete(root).value
            finally:
                views.unbridged_gates = original
        self.assertEqual(value["open_escalations"], ("bbbb",))
        self.assertEqual(value["escalations_by_root"]["docs/operations/example"]
                         ["answered"], ("aaaa",))


class NoPhantomGateComesFromARecordsExamples(unittest.TestCase):

    def test_the_goal_004_record_names_no_invented_identifier(self):
        text = (REPO_ROOT / "docs/governance/AIOS_GOAL_V2_004_CERTIFIED_"
                "EVIDENCE_WRITE_CLOSURE_RECORD_v1.0.md").read_text(encoding="utf-8")
        for phantom in ("FD-P10-00`", "FD-P12-999"):
            self.assertNotIn(phantom, text)
        gates = set(views.unbridged_gates())
        self.assertFalse({"FD-P10-00", "FD-P12-999", "FD-P12-999-FORGED"} & gates)


if __name__ == "__main__":
    unittest.main()
