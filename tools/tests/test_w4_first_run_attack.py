"""`ACT-CC-P11-008 §26` — twelve attacks on the real authority chain.

`§42`: *"The goal is not to prove the preferred implementation correct. The goal
is to determine whether the implementation survives adversarial attempts to
invalidate it."*

Each test below attacks the chain that actually ran in `tools/w4_first_run.py`,
using the same definition, the same instance shape and the same delegation
terms. `§28` additionally requires that each attack produce an **explicit
validation failure** rather than an incidental `AttributeError`, `KeyError` or
partial execution — so every assertion names the governance exception, not
whatever the runtime would have raised on its own.
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from native_core.core.agent.definition import AgentDefinition  # noqa: E402
from tools.agent_instance_registry import (  # noqa: E402
    AgentInstanceRegistry,
    InstanceRegistrationError,
)
from tools.planning import AuthorityProvenance, InvalidGoal  # noqa: E402
from tools.w4_delegation import (  # noqa: E402
    AUTHORIZED_DELEGATOR,
    DelegationError,
    W4DelegationRegistry,
)
from tools.w4_execution import ESCALATION, ExecutionRefused, W4Executor  # noqa: E402
from tools.w4_first_run import (  # noqa: E402
    CRITERION_NAMES,
    FD_RECORD,
    INSTANCE_KEY,
    SELECTED_DEFINITION,
    _plan,
    run,
)


def _performer(lines, names):
    """A substring performer, standing in for the resident consumer.

    These tests live under `tools/`, which may not import `consumers/`, so the
    real agent cannot be reached from here. That is not a gap: **what is under
    test in this file is the authority chain**, not the verification algorithm,
    and the chain is indifferent to who performs the work — which is precisely
    why the performer is injected. The real consumer drives the real run from
    the module's own entry point, and that run's evidence is persisted.
    """
    text = "\n".join(lines)
    return {name: name in text for name in names}

DP01_RECORD = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"

TERMS = dict(
    objective="o", capability_scope=("engineering-intelligence",),
    work_scope=("verify-delegation-elements",), lifecycle_boundary="l",
    resource_boundary="r", output_expectation="oe",
    verification_requirement="v", escalation_condition="e",
    accountable_party=AUTHORIZED_DELEGATOR, termination_condition="t")


def _live():
    registry = AgentInstanceRegistry()
    registration = registry.register(
        instance_key=INSTANCE_KEY, definition=SELECTED_DEFINITION,
        permitted_capabilities=("engineering-intelligence",),
        created_by=AUTHORIZED_DELEGATOR,
        authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
        accountable_to=AUTHORIZED_DELEGATOR)
    delegations = W4DelegationRegistry(registry)
    return registry, registration, delegations


class NC01_DP01Substitution(unittest.TestCase):
    def test_dp01_cannot_stand_in_for_fd_p11_001(self):
        registry, registration, delegations = _live()
        with self.assertRaises(DelegationError):
            delegations.issue(
                delegator=AUTHORIZED_DELEGATOR,
                recipient_instance=registration.instance_key,
                authority=AuthorityProvenance("DP-01 §3 W4", DP01_RECORD),
                **TERMS)


class NC02_UnknownInstance(unittest.TestCase):
    def test_an_unregistered_recipient_is_refused(self):
        registry, _, delegations = _live()
        with self.assertRaises(DelegationError):
            delegations.issue(
                delegator=AUTHORIZED_DELEGATOR,
                recipient_instance="never-registered-instance",
                authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
                **TERMS)


class NC03_AnonymousInstance(unittest.TestCase):
    """`§10`: no anonymous instance, and none whose provenance is unverifiable.

    **Two layers, and the probe told them apart.** Disabling the organizational
    identity check left this class passing, because the frozen core independently
    refuses an empty, blank or `None` instance key. That `OK` was not a missing
    control — it was a **test-scope** finding: the attack only tried cases the
    core already covers, so it could not observe whether the organizational layer
    was doing anything.

    Measured rather than assumed: with the organizational check disabled, `""`,
    `"   "` and `None` are still refused by the core, while `UPPERCASE`,
    `has spaces`, `-leading-hyphen` and an over-length key are **accepted**.
    Those four are what this layer alone prevents, so they are tested here.
    """

    def test_an_instance_without_identity_is_refused_by_the_core(self):
        registry = AgentInstanceRegistry()
        for anonymous in ("", "   ", None):
            with self.subTest(identity=anonymous):
                with self.assertRaises(InstanceRegistrationError):
                    registry.register(
                        instance_key=anonymous,
                        definition=SELECTED_DEFINITION,
                        permitted_capabilities=("engineering-intelligence",),
                        created_by=AUTHORIZED_DELEGATOR,
                        authority=AuthorityProvenance("FD-P11-001 §7",
                                                      FD_RECORD),
                        accountable_to=AUTHORIZED_DELEGATOR)

    def test_a_malformed_identity_is_refused_by_the_organizational_layer(self):
        """The cases the core lets through. Without these the layer is untested."""
        registry = AgentInstanceRegistry()
        for malformed in ("UPPERCASE", "has spaces", "-leading-hyphen",
                          "a" * 200, "x"):
            with self.subTest(identity=malformed):
                with self.assertRaises(InstanceRegistrationError):
                    registry.register(
                        instance_key=malformed,
                        definition=SELECTED_DEFINITION,
                        permitted_capabilities=("engineering-intelligence",),
                        created_by=AUTHORIZED_DELEGATOR,
                        authority=AuthorityProvenance("FD-P11-001 §7",
                                                      FD_RECORD),
                        accountable_to=AUTHORIZED_DELEGATOR)


class NC04_NullDelegation(unittest.TestCase):
    def test_execution_without_a_delegation_fails_closed(self):
        """`§28`: an explicit validation failure, **not** an `AttributeError`.

        Before this Act the executor stored whatever it was given and failed at
        first use with an attribute error — an incidental failure, which `§28`
        says *"is not considered adequate governance enforcement."*
        """
        registry, _, _ = _live()
        for not_a_delegation in (None, "a delegation", 0, object()):
            with self.subTest(value=type(not_a_delegation).__name__):
                with self.assertRaises(TypeError) as caught:
                    W4Executor(not_a_delegation, registry)
                self.assertIn("W4Delegation", str(caught.exception))


class NC05_ScopeEscalation(unittest.TestCase):
    def test_a_step_outside_the_work_scope_is_refused(self):
        registry, registration, delegations = _live()
        delegation = delegations.issue(
            delegator=AUTHORIZED_DELEGATOR,
            recipient_instance=registration.instance_key,
            authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
            **TERMS)                       # only 'verify-delegation-elements'
        surface, plan = _plan()            # plan also contains 'report-conformance'
        report = W4Executor(delegation, registry).execute_plan(
            plan, lambda step: "done")
        self.assertEqual(report.statuses()[1], ESCALATION)
        self.assertEqual(report.refusals[0].required, "report-conformance")

    def test_a_capability_beyond_the_instance_is_refused(self):
        registry, registration, delegations = _live()
        with self.assertRaises(DelegationError):
            delegations.issue(
                delegator=AUTHORIZED_DELEGATOR,
                recipient_instance=registration.instance_key,
                authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
                **{**TERMS, "capability_scope": ("engineering-intelligence",
                                                 "governance-artifact-integrity")})


class NC06_InvalidLifecycle(unittest.TestCase):
    def test_a_retired_instance_cannot_execute(self):
        registry, registration, delegations = _live()
        delegation = delegations.issue(
            delegator=AUTHORIZED_DELEGATOR,
            recipient_instance=registration.instance_key,
            authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD), **TERMS)
        registry.retire(registration.instance_key)
        surface, plan = _plan()
        report = W4Executor(delegation, registry).execute_plan(
            plan, lambda step: "should not run")
        self.assertTrue(all(s == ESCALATION for s in report.statuses()))

    def test_a_revoked_delegation_cannot_execute(self):
        registry, registration, delegations = _live()
        delegation = delegations.issue(
            delegator=AUTHORIZED_DELEGATOR,
            recipient_instance=registration.instance_key,
            authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD), **TERMS)
        delegations.revoke(delegation.delegation_id, reason="attack test")
        report = W4Executor(delegations.get(delegation.delegation_id),
                            registry).execute_plan(_plan()[1],
                                                   lambda step: "no")
        self.assertTrue(all(s == ESCALATION for s in report.statuses()))


class NC07_SelfDelegation(unittest.TestCase):
    def test_the_instance_cannot_be_its_own_accountable_party(self):
        registry, registration, delegations = _live()
        with self.assertRaises(DelegationError):
            delegations.issue(
                delegator=AUTHORIZED_DELEGATOR,
                recipient_instance=registration.instance_key,
                authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
                **{**TERMS, "accountable_party": registration.instance_key})

    def test_the_instance_cannot_pose_as_the_delegator(self):
        registry, registration, delegations = _live()
        with self.assertRaises(DelegationError):
            delegations.issue(
                delegator=registration.instance_key,
                recipient_instance=registration.instance_key,
                authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
                **TERMS)


class NC08_MissingAccountability(unittest.TestCase):
    def test_a_delegation_without_an_accountable_party_is_refused(self):
        registry, registration, delegations = _live()
        with self.assertRaises(DelegationError):
            delegations.issue(
                delegator=AUTHORIZED_DELEGATOR,
                recipient_instance=registration.instance_key,
                authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
                **{**TERMS, "accountable_party": ""})


class NC09_MissingProvenance(unittest.TestCase):
    def test_a_delegation_without_a_citation_is_refused(self):
        registry, registration, delegations = _live()
        for bogus in (None, "FD-P11-001", 0):
            with self.subTest(value=bogus):
                with self.assertRaises(DelegationError):
                    delegations.issue(
                        delegator=AUTHORIZED_DELEGATOR,
                        recipient_instance=registration.instance_key,
                        authority=bogus, **TERMS)


class NC10_AuthorityForgery(unittest.TestCase):
    def test_an_invented_instrument_cannot_be_cited(self):
        for claim in ("FD-P11-001", "Founder Reserved Authority",
                      "Constitutional Authority", "FD-P11-999"):
            with self.subTest(claim=claim):
                with self.assertRaises(InvalidGoal):
                    AuthorityProvenance(claim, "docs/governance/acts/none.md")

    def test_a_real_but_wrong_instrument_is_refused_for_delegation(self):
        """Resolution is not enough — `§15` requires this Decision by name."""
        registry, registration, delegations = _live()
        with self.assertRaises(DelegationError):
            delegations.issue(
                delegator=AUTHORIZED_DELEGATOR,
                recipient_instance=registration.instance_key,
                authority=AuthorityProvenance("DP-04 §8.3",
                                              "docs/architecture/p11/"
                                              "DP-04-P11-ORGANIZATIONAL-"
                                              "ENTITY-MODEL.md"),
                **TERMS)


class NC11_UnauthorizedAgentDefinition(unittest.TestCase):
    def test_a_definition_implementing_nothing_is_refused_by_the_core(self):
        """The frozen boundary refuses it before my registry is reached.

        My first version of this attack expected `InstanceRegistrationError`
        from the organizational layer. It never got there:
        `native_core/core/agent/definition.py` rejects a Definition that
        implements no Capability outright. **The canonical boundary is stricter
        than the control I wrote to back it up**, which is the right order and
        is recorded rather than papered over.
        """
        from native_core.core.agent.definition import InvalidAgentDefinition
        with self.assertRaises(InvalidAgentDefinition):
            AgentDefinition(
                agent_definition_key="omnipotent-agent",
                agent_definition_version="1.0",
                owning_department_key="engineering",
                implemented_capabilities=(), specified_skills=(),
                specified_workflows=())

    def test_an_instance_cannot_claim_a_capability_its_definition_lacks(self):
        """The attack that *is* constructible: a definition that exists and
        implements something, used to claim something else."""
        registry = AgentInstanceRegistry()
        invented = AgentDefinition(
            agent_definition_key="omnipotent-agent",
            agent_definition_version="1.0", owning_department_key="engineering",
            implemented_capabilities=("something-else",), specified_skills=(),
            specified_workflows=())
        with self.assertRaises(InstanceRegistrationError):
            registry.register(
                instance_key="omnipotent-instance", definition=invented,
                permitted_capabilities=("engineering-intelligence",),
                created_by=AUTHORIZED_DELEGATOR,
                authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
                accountable_to=AUTHORIZED_DELEGATOR)

    def test_the_selected_definition_is_one_of_the_resident_three(self):
        resident = {p.stem for p in (REPO_ROOT / "docs/architecture/organization")
                    .rglob("agent-definitions/*.md")}
        # Re-anchored under `ACT-CC-P11-017`: this asserted `len(resident) == 3`,
        # a population snapshot that would fail on a legitimate fourth Agent
        # Definition and prove nothing the next line does not already prove.
        self.assertTrue(resident, "precondition: no resident Definition found")
        self.assertIn(SELECTED_DEFINITION.agent_definition_key, resident)


class NC12_AuthorityByNecessity(unittest.TestCase):
    """`TECHNICAL NECESSITY ≠ GOVERNANCE AUTHORITY`.

    The attack is the one that would actually be attempted: the work genuinely
    needs a capability, so the caller asserts it. Nothing about needing it
    supplies it.
    """

    def test_needing_a_capability_does_not_confer_it(self):
        registry, registration, delegations = _live()
        with self.assertRaises(DelegationError):
            delegations.issue(
                delegator=AUTHORIZED_DELEGATOR,
                recipient_instance=registration.instance_key,
                authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
                **{**TERMS,
                   "objective": "This work requires governance artifact access.",
                   "capability_scope": ("governance-artifact-integrity",)})

    def test_a_successful_run_confers_nothing_further(self):
        """`§31`: real execution does not widen anything."""
        evidence = run(_performer, persist=False)
        self.assertEqual(evidence["capability_scope"],
                         ["engineering-intelligence"])
        self.assertFalse(evidence["boundary_crossed"])


class LiveGrantsDoNotAccumulate(unittest.TestCase):
    """`§29` applied to the persisted operational record, not just the type.

    **Found by re-running.** Three successive runs of the first-execution proof
    each issued a fresh Delegation and left the previous one `ACTIVE`. Nothing
    used them and nothing would have ended them — a grant nobody withdraws is
    permanent in practice, however carefully its `termination_condition`
    describes an ending. A condition with no mechanism to apply it is a
    description.
    """

    OPERATIONS = REPO_ROOT / "docs/architecture/p11/w4-operations"

    def test_at_most_one_grant_is_live_for_the_instance(self):
        import json
        active = []
        for path in sorted(self.OPERATIONS.glob("*.delegation.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            if record.get("status") == "ACTIVE":
                active.append(record["delegation_id"])
        self.assertLessEqual(len(active), 1, f"live grants: {active}")

    def test_every_retired_grant_records_why(self):
        """Revocation without a reason is deletion with extra steps."""
        import json
        for path in sorted(self.OPERATIONS.glob("*.delegation.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            if record.get("status") == "REVOKED":
                with self.subTest(delegation=record["delegation_id"]):
                    self.assertTrue(record.get("revocation_reason", "").strip())

    def test_a_rerun_supersedes_rather_than_accumulates(self):
        """The mechanism, exercised: the run reports what it withdrew."""
        import json
        evidence = json.loads(
            (self.OPERATIONS / "first-execution.evidence.json")
            .read_text(encoding="utf-8"))
        self.assertIn("superseded_grants", evidence)
        live = evidence["delegation_id"]
        self.assertNotIn(live, evidence["superseded_grants"])


class TheRealRunIsReproducibleAndBounded(unittest.TestCase):
    """`§30`: every link of the chain, asserted on the real run's evidence."""

    def setUp(self):
        self.evidence = run(_performer, persist=False)

    def test_every_link_of_the_chain_is_present(self):
        chain = self.evidence["authority_chain"]
        self.assertTrue(chain[0].startswith("delegation:"))
        self.assertIn(AUTHORIZED_DELEGATOR, chain[1])
        self.assertIn("FD-P11-001", chain[2])
        self.assertEqual(chain[3], "founder:Founder")
        self.assertEqual(self.evidence["agent_definition"],
                         "engineering-intelligence-agent")
        self.assertEqual(self.evidence["agent_instance"], INSTANCE_KEY)
        self.assertEqual(self.evidence["instance_lifecycle"], "REGISTERED")
        self.assertEqual(self.evidence["delegation_status"], "ACTIVE")
        self.assertEqual(self.evidence["accountable_party"],
                         AUTHORIZED_DELEGATOR)

    def test_the_work_was_real_and_every_criterion_was_checked(self):
        self.assertEqual(self.evidence["criteria_total"], len(CRITERION_NAMES))
        self.assertEqual(self.evidence["criteria_satisfied"], len(CRITERION_NAMES))
        self.assertEqual(self.evidence["criteria_unsatisfied"], [])

    def test_every_outcome_carries_a_ratified_status(self):
        for outcome in self.evidence["outcomes"]:
            self.assertIn(outcome["status"], ("success", "failure",
                                              "escalation"))
            self.assertEqual(outcome["instance"], INSTANCE_KEY)

    def test_the_plan_is_bound_and_separate_from_the_delegation(self):
        """`§20`: `PLAN ≠ DELEGATION`."""
        self.assertEqual(self.evidence["plan"],
                         "w4-first-execution-proof-plan-0")
        self.assertNotEqual(self.evidence["plan"],
                            self.evidence["delegation_id"])
        self.assertIn("DP-01 §3 W2", self.evidence["plan_authority"])


if __name__ == "__main__":
    unittest.main()
