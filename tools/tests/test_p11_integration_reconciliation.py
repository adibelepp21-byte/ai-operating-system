"""`ACT-CC-P11-009 §31` — NC-01…15, and the `§22` corruption states.

The three reconciliations this Act performed are held here as standing controls:
W3/W4 are **one canonical model with two projections**, escalation is
**organizational state** rather than refusal, and continuity **reconstructs from
record** rather than from memory.
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from native_core.core.governance import HumanAuthority  # noqa: E402
from tools.delegation_catalog import (  # noqa: E402
    INSTRUMENT_ESTABLISHED_SOURCES,
    read_delegations,
    registered_instances,
    verify,
)
from tools.escalation_register import (  # noqa: E402
    EscalationRegister,
    EscalationRegisterError,
)
from tools.planning import AuthorityProvenance  # noqa: E402
from tools.tests.test_delegation_catalog import _build_organization  # noqa: E402
from tools.w4_continuity import (  # noqa: E402
    ContinuityError,
    continuation_conditions,
    reconstruct,
)
from tools.w4_delegation import AUTHORIZED_DELEGATOR  # noqa: E402
from tools.w4_execution import ExecutionRefused  # noqa: E402

OPERATIONS = REPO_ROOT / "docs/architecture/p11/w4-operations"
FD = ("docs/governance/acts/"
      "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md")


def _w3_record(source, scope, actor, instrument="FD-P11-001"):
    return f"""# grant

## Authority Source

{source}

## Authorized Scope

{scope}

## Delegated Actor

{actor}

## Boundary

b

## Accountability

Claude Code / AIOS Co-Founder

## Verification

[v](../../instr.md)

## Authorizing Instrument

[{instrument}](../../instr.md)
"""


class _W3Fixture(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.org = Path(self._tmp.name) / "organization"
        self.org.mkdir()
        _build_organization(self.org)
        self.delegations = self.org / "delegations"
        self.delegations.mkdir()
        (Path(self._tmp.name) / "instr.md").write_text("# x\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def kinds(self, text):
        (self.delegations / "d.md").write_text(text, encoding="utf-8")
        return {k for k, _, _ in verify(read_delegations(self.delegations),
                                        self.org, self.delegations)}


class NC01_02_W3AndW4AreOneModelNotTwoAuthorities(_W3Fixture):
    """`§4`/`§7` — verdict `R2`: one canonical model, two projections.

    `DP-04 §8.3` defines **one** delegation record shape and **one**
    `AUTHORITY SOURCE`; `FD-P11-001 §20` makes W3 *"the organizational mechanism
    through which the authorized Delegation record is represented and tracked."*

    **The defect this Act found:** W3 structurally rejected the very record it
    was designated to track, because my implementation required the authority
    source to be a Department — a constraint `DP-04 §8.3` never states. It was
    right when written, since Departments were then the only conceivable
    delegators, and became narrower than the architecture when `FD-P11-001 §4.1`
    established a delegator that is not a unit.
    """

    def test_an_instrument_established_delegator_is_representable(self):
        self.assertEqual(
            self.kinds(_w3_record("claude-code-aios-co-founder",
                                  "engineering-intelligence",
                                  "engineering-intelligence-instance-001")),
            set())

    def test_the_department_ownership_rule_is_unchanged(self):
        """The load-bearing control must survive the relaxation."""
        self.assertIn("scope-not-owned",
                      self.kinds(_w3_record("engineering",
                                            "governance-artifact-integrity",
                                            "platform")))

    def test_an_unestablished_source_is_still_refused(self):
        self.assertIn("authority-source-unknown",
                      self.kinds(_w3_record("marketing", "engineering-intelligence",
                                            "engineering")))

    def test_an_instrument_source_must_cite_its_instrument(self):
        """`§20`: W3 *"must not manufacture authority absent valid provenance."*"""
        self.assertIn("source-instrument-not-cited",
                      self.kinds(_w3_record("claude-code-aios-co-founder",
                                            "engineering-intelligence",
                                            "engineering-intelligence-instance-001",
                                            instrument="DP-01")))

    def test_scope_is_bounded_by_the_recipient_not_unbounded(self):
        """`§8` dual-authority: the instrument source must not be a way to grant
        anything at all. `FD-P11-001 §16`: delegated ≤ available."""
        self.assertIn("scope-beyond-recipient",
                      self.kinds(_w3_record("claude-code-aios-co-founder",
                                            "cognitive-intelligence",
                                            "engineering-intelligence-instance-001")))

    def test_the_resident_population_now_represents_the_live_grant(self):
        """Every live grant is represented, and every record verifies clean.

        **Re-anchored under `ACT-CC-P11-013`.** This asserted
        ``len(resident) == 1`` — a population *count*, standing in for the
        claim in its own name. The count was one because exactly one record had
        been written by hand, and the test would have gone on passing while the
        live grant went unrepresented, which is precisely what happened:
        `ACT-CC-P11-012` found the single record pointing at a **revoked**
        grant, with this control green throughout.

        The invariant was never the number. It is that the resident population
        represents what is actually live, which is now asserted against the
        ledger instead of against an integer.
        """
        from tools.delegation_reconciliation import reconcile
        resident = read_delegations()
        self.assertTrue(resident, "the population may not be empty")
        for record in resident:
            self.assertEqual(record.authority_source,
                             "claude-code-aios-co-founder")
        self.assertEqual(verify(resident), [])
        result = reconcile()
        self.assertEqual(sorted(result["active_grants"]),
                         sorted(result["represented_active"]))


class NC03_04_05_GrantLifecycle(unittest.TestCase):
    """`§9`/`§34` — revoked stays revoked, and live grants do not accumulate."""

    def _grants(self):
        return [json.loads(p.read_text(encoding="utf-8"))
                for p in OPERATIONS.glob("*.delegation.json")]

    def test_at_most_one_grant_is_live(self):
        active = [g["delegation_id"] for g in self._grants()
                  if g["status"] == "ACTIVE"]
        self.assertLessEqual(len(active), 1, active)

    def test_every_revoked_grant_states_why_and_stays_revoked(self):
        for grant in self._grants():
            if grant["status"] == "REVOKED":
                with self.subTest(grant=grant["delegation_id"]):
                    self.assertTrue(grant.get("revocation_reason", "").strip())

    def test_reconstruction_reports_revoked_grants_as_revoked(self):
        """`§21`: a recovered grant comes back with the status it actually has,
        never as active because it once was."""
        state = reconstruct()
        self.assertTrue(state["revoked_grants"])
        self.assertNotIn(state["active_grants"][0] if state["active_grants"]
                         else None, state["revoked_grants"])


class NC06_07_08_09_EscalationIsOrganizationalState(unittest.TestCase):
    """`§11`–`§17`. **`REFUSAL ≠ ESCALATION`.**

    Before this Act the W4 path produced an `ExecutionOutcome` with status
    `escalation` inside one run's evidence — an outcome, with no lifecycle, no
    accountable party and no way to resolve. The register existed and **nothing
    referenced it from the W4 path**.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.register = EscalationRegister(Path(self._tmp.name))
        self.refusal = ExecutionRefused("step outside scope", required="b",
                                        held=("a",))

    def tearDown(self):
        self._tmp.cleanup()

    def test_a_refusal_becomes_a_persisted_record_with_accountability(self):
        record = self.register.record(
            self.refusal, subject="plan p",
            authority=AuthorityProvenance("FD-P11-001 §9", FD))
        self.assertEqual(self.register.status(record.escalation_id), "OPEN")
        self.assertEqual(record.required, "b")

    def test_an_invented_refusal_cannot_become_organizational_state(self):
        """`§13`: not everything shaped like a refusal is one."""
        class LooksLikeARefusal:
            required, held = "b", ("a",)
        for bogus in (LooksLikeARefusal(), "blocked", None):
            with self.subTest(value=type(bogus).__name__):
                with self.assertRaises(EscalationRegisterError):
                    self.register.record(
                        bogus, subject="s",
                        authority=AuthorityProvenance("FD-P11-001 §9", FD))

    def test_escalation_does_not_create_authority(self):
        """`§16`: `ESCALATION ≠ APPROVAL`, `BLOCKED ≠ AUTHORIZED`."""
        record = self.register.record(
            self.refusal, subject="p",
            authority=AuthorityProvenance("FD-P11-001 §9", FD))
        for name in dir(self.register):
            self.assertFalse(any(v in name.lower() for v in
                                 ("approve", "authorize", "grant", "permit")),
                             name)
        self.assertNotEqual(self.register.status(record.escalation_id),
                            "APPROVED")

    def test_only_a_human_may_answer_and_answering_is_not_approving(self):
        record = self.register.record(
            self.refusal, subject="p",
            authority=AuthorityProvenance("FD-P11-001 §9", FD))
        with self.assertRaises(EscalationRegisterError):
            self.register.record_response(record.escalation_id,
                                          authority="automation",
                                          response="approved")
        self.register.record_response(record.escalation_id,
                                      authority=HumanAuthority("a-human"),
                                      response="Noted; not granted.")
        self.assertEqual(self.register.status(record.escalation_id), "ANSWERED")

    def test_the_live_escalation_survived_a_process_boundary(self):
        """`§9` of the control list: escalation must not disappear.

        Read in a **separate interpreter** — the real escalation raised by the
        second real run.
        """
        program = ("import sys; sys.path.insert(0, sys.argv[1]);"
                   "from tools.w4_continuity import reconstruct;"
                   "import json; print(json.dumps(reconstruct()"
                   "['open_escalations']))")
        proc = subprocess.run([sys.executable, "-c", program, str(REPO_ROOT)],
                              capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(json.loads(proc.stdout))


class NC10_11_12_13_MemoryIsNotAuthority(unittest.TestCase):
    """`§21`–`§23`. Recovered state says what happened, never what is allowed."""

    def test_reconstruction_reads_files_and_nothing_else(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ContinuityError):
                reconstruct(Path(tmp) / "absent")

    def test_an_open_escalation_blocks_a_naive_continuation(self):
        """Stale memory must not read as 'nothing to do'."""
        state = reconstruct()
        if state["open_escalations"]:
            joined = " ".join(continuation_conditions(state))
            self.assertIn("OPEN ESCALATIONS", joined)

    def test_the_corruption_states_do_not_collapse(self):
        """`§22`: unreadable is not absent, duplicate is not single."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.delegation.json").write_text("{not json",
                                                    encoding="utf-8")
            # Both live grants held by the **same** instance — accumulation.
            for key in ("b", "c"):
                (root / f"{key}.delegation.json").write_text(json.dumps(
                    {"delegation_id": key, "status": "ACTIVE",
                     "recipient_instance": "inst-1"}), encoding="utf-8")
            state = reconstruct(root)
            self.assertEqual(state["unreadable_records"], ["a.delegation.json"])
            self.assertTrue(state["duplicate_active"])
            self.assertEqual({"inst-1": ["b", "c"]}, state["accumulated_grants"])
            joined = " ".join(continuation_conditions(state))
            self.assertIn("UNREADABLE RECORDS", joined)
            self.assertIn("MORE THAN ONE LIVE GRANT", joined)

    def test_two_instances_holding_one_grant_each_is_not_accumulation(self):
        """`ACT-CC-P11-017` — the false positive this detector used to produce.

        `duplicate_active` was `len(active) > 1`, which encoded *one instance per
        operational root*. That held for `w4-operations` and `w1-operations` and
        is false of a cross-Department root, where two grants are live by design
        — one per Department's instance, each bounded to its own step. The reader
        a next run consults therefore reported a **permanent blocking condition
        against a legitimate state**.

        This is the control that keeps the correction honest: the mutation above
        must still fire, and this must not.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for key, instance in (("b", "inst-1"), ("c", "inst-2")):
                (root / f"{key}.delegation.json").write_text(json.dumps(
                    {"delegation_id": key, "status": "ACTIVE",
                     "recipient_instance": instance}), encoding="utf-8")
            state = reconstruct(root)
            self.assertEqual(2, len(state["active_grants"]))
            self.assertFalse(state["duplicate_active"])
            self.assertEqual({}, state["accumulated_grants"])
            self.assertNotIn("MORE THAN ONE LIVE GRANT",
                             " ".join(continuation_conditions(state)))

    def test_the_resident_cross_department_root_is_not_reported_blocked(self):
        """The real corpus, not a fixture — two Departments, two live grants."""
        from tools.delegation_catalog import operation_roots
        for candidate in operation_roots():
            state = reconstruct(candidate)
            holders = state["live_grants_by_instance"]
            if len(holders) > 1:
                self.assertFalse(state["duplicate_active"], candidate.name)
                break
        else:
            self.skipTest("no root currently holds grants for two instances")

    def test_a_previous_failure_is_not_reported_as_done(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "first-execution.evidence.json").write_text(json.dumps(
                {"outcomes": [{"step": "a", "status": "failure"}]}),
                encoding="utf-8")
            state = reconstruct(root)
            self.assertTrue(state["last_failed"])
            self.assertIn("FAILURE", " ".join(continuation_conditions(state)))

    def test_the_second_run_superseded_rather_than_accumulated(self):
        """`§23`: a re-run must not recreate permanent grants."""
        evidence = json.loads(
            (OPERATIONS / "first-execution.evidence.json")
            .read_text(encoding="utf-8"))
        self.assertIn("prior_state", evidence)
        prior = evidence["prior_state"]
        self.assertTrue(prior.get("recovered_instances"))
        for superseded in evidence["superseded_grants"]:
            self.assertNotEqual(superseded, evidence["delegation_id"])


class NC14_15_CoordinationAndDelegatorDistinctions(unittest.TestCase):
    """`§25`/`§26` — no fake coordination, and an instance is not a delegator."""

    def test_no_agent_instance_is_an_authority_source(self):
        """`§26`: an Agent Instance may not function as a unit-level delegator."""
        for key in registered_instances():
            self.assertNotIn(key, INSTRUMENT_ESTABLISHED_SOURCES)

    def test_the_plan_to_workflow_gate_is_still_closed(self):
        """`§25`: coordination must not be manufactured to mark W1 complete."""
        planning = REPO_ROOT / "tools" / "planning"
        for path in sorted(planning.glob("*.py")):
            source = path.read_text(encoding="utf-8")
            for fabricated in ("AgentInstanceRef", "WorkflowStep",
                               "WorkflowComposition"):
                self.assertNotIn(fabricated, source, f"{path.name}")

    def test_w3_actors_do_not_silently_become_delegators(self):
        """Being a valid recipient confers nothing about being a source."""
        source_keys = set(INSTRUMENT_ESTABLISHED_SOURCES)
        self.assertNotIn("engineering-intelligence-instance-001", source_keys)
        self.assertNotIn("engineering-intelligence-agent", source_keys)


if __name__ == "__main__":
    unittest.main()
