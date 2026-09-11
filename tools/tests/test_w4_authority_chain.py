"""`FD-P11-001` — NC-W4-01…20, the `§25`/`§26` tests, and the `§18` chain.

`§23` makes twenty negative controls mandatory. `§25` and `§26` fix what an
Agent Instance and a Delegation must each prove. `§18` fixes the execution chain
and states that **no stage may be silently skipped** — so the end-to-end test
walks every stage and the controls prove each one is load-bearing.
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from native_core.core.agent.definition import AgentDefinition  # noqa: E402
from native_core.core.agent.instance import AgentInstance  # noqa: E402
from tools.agent_instance_registry import (  # noqa: E402
    REGISTERED,
    RETIRED,
    AgentInstanceRegistry,
    InstanceRegistrationError,
)
from tools.delegation_catalog import read_delegations  # noqa: E402
from tools.planning import (  # noqa: E402
    AuthorityProvenance,
    Goal,
    Plan,
    PlanStep,
    PlanningSurface,
)
from tools.w4_delegation import (  # noqa: E402
    AUTHORIZED_DELEGATOR,
    DelegationError,
    W4Delegation,
    W4DelegationRegistry,
)
from tools.w4_execution import (  # noqa: E402
    ESCALATION,
    SUCCESS,
    ExecutionRefused,
    W4Executor,
)

FD = "docs/governance/acts/FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md"
DP01 = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"

DEFINITION = AgentDefinition(
    agent_definition_key="engineering-intelligence-agent",
    agent_definition_version="1.0",
    owning_department_key="engineering",
    implemented_capabilities=("engineering-intelligence",),
    specified_skills=(), specified_workflows=())


def _fd_authority():
    return AuthorityProvenance("FD-P11-001 §7", FD)


def _registered(registry, key="engineering-intelligence-instance-01"):
    return registry.register(
        instance_key=key, definition=DEFINITION,
        permitted_capabilities=("engineering-intelligence",),
        created_by=AUTHORIZED_DELEGATOR, authority=_fd_authority(),
        accountable_to=AUTHORIZED_DELEGATOR)


def _delegation(delegations, instance_key, *, work_scope=("a", "b"),
                capability_scope=("engineering-intelligence",)):
    return delegations.issue(
        delegator=AUTHORIZED_DELEGATOR, recipient_instance=instance_key,
        authority=AuthorityProvenance("FD-P11-001 §9", FD),
        objective="Execute the authorized plan.",
        capability_scope=capability_scope, work_scope=work_scope,
        lifecycle_boundary="single plan execution",
        resource_boundary="repository-local, no network",
        output_expectation="an outcome per step",
        verification_requirement="every outcome carries a ratified status",
        escalation_condition="any step outside the delegated work scope",
        accountable_party=AUTHORIZED_DELEGATOR,
        termination_condition="on completion of the bound plan, or on revocation")


def _stack():
    registry = AgentInstanceRegistry()
    registration = _registered(registry)
    delegations = W4DelegationRegistry(registry)
    delegation = _delegation(delegations, registration.instance_key)
    return registry, registration, delegations, delegation


def _plan():
    authority = AuthorityProvenance("DP-01 §3 W2", DP01)
    surface = PlanningSurface()
    surface.declare(Goal("g", "Intent.", authority))
    return surface, surface.adopt(Plan(
        key="p", goal_key="g", authority=authority,
        steps=(PlanStep("a", "A."), PlanStep("b", "B.", depends_on=("a",)))))


class NC_W4_01_02_DefinitionInstanceDelegationAreDistinct(unittest.TestCase):
    def test_a_definition_is_not_an_instance(self):
        registry = AgentInstanceRegistry()
        self.assertFalse(registry.is_registered(
            DEFINITION.agent_definition_key))
        self.assertNotIsInstance(DEFINITION, AgentInstance)

    def test_a_definition_alone_cannot_receive_a_delegation(self):
        """`§6.1`: *"An Agent Definition alone is insufficient."*"""
        registry = AgentInstanceRegistry()
        delegations = W4DelegationRegistry(registry)
        with self.assertRaises(DelegationError):
            _delegation(delegations, DEFINITION.agent_definition_key)

    def test_an_instance_is_not_a_delegation(self):
        registry, registration, _, delegation = _stack()
        self.assertNotIsInstance(registration, W4Delegation)
        self.assertNotEqual(registration.instance_key,
                            delegation.delegation_id)


class NC_W4_03_15_DelegationCannotCreateOrExceedAuthority(unittest.TestCase):
    def test_a_grant_beyond_the_instance_surface_is_refused(self):
        """`§16`: delegated ≤ available, enforced as an intersection."""
        registry = AgentInstanceRegistry()
        registration = _registered(registry)
        delegations = W4DelegationRegistry(registry)
        with self.assertRaises(DelegationError) as caught:
            _delegation(delegations, registration.instance_key,
                        capability_scope=("engineering-intelligence",
                                          "governance-artifact-integrity"))
        self.assertIn("exceeds", str(caught.exception))

    def test_an_instance_cannot_hold_more_than_its_definition(self):
        """`§8`: capabilities not supported by the definition are refused."""
        registry = AgentInstanceRegistry()
        with self.assertRaises(InstanceRegistrationError):
            registry.register(
                instance_key="over-scoped-instance", definition=DEFINITION,
                permitted_capabilities=("engineering-intelligence",
                                        "governance-artifact-integrity"),
                created_by=AUTHORIZED_DELEGATOR, authority=_fd_authority(),
                accountable_to=AUTHORIZED_DELEGATOR)

    def test_a_delegation_confers_only_what_it_names(self):
        _, _, _, delegation = _stack()
        self.assertTrue(delegation.permits("engineering-intelligence"))
        self.assertFalse(delegation.permits("governance-artifact-integrity"))


class NC_W4_04_05_06_NothingCascadesAutomatically(unittest.TestCase):
    def test_dp01_cannot_authorize_an_instance(self):
        """`§10`: `DP-01 ≠ SPECIFIC W4 DELEGATION`."""
        registry = AgentInstanceRegistry()
        with self.assertRaises(InstanceRegistrationError) as caught:
            registry.register(
                instance_key="dp01-authorized-instance", definition=DEFINITION,
                permitted_capabilities=("engineering-intelligence",),
                created_by=AUTHORIZED_DELEGATOR,
                authority=AuthorityProvenance("DP-01 §3 W4", DP01),
                accountable_to=AUTHORIZED_DELEGATOR)
        self.assertIn("FD-P11-001", str(caught.exception))

    def test_dp01_cannot_authorize_a_delegation(self):
        registry = AgentInstanceRegistry()
        registration = _registered(registry)
        delegations = W4DelegationRegistry(registry)
        with self.assertRaises(DelegationError):
            delegations.issue(
                delegator=AUTHORIZED_DELEGATOR,
                recipient_instance=registration.instance_key,
                authority=AuthorityProvenance("DP-01 §3 W4", DP01),
                objective="o", capability_scope=("engineering-intelligence",),
                work_scope=("a",), lifecycle_boundary="l",
                resource_boundary="r", output_expectation="o",
                verification_requirement="v", escalation_condition="e",
                accountable_party=AUTHORIZED_DELEGATOR,
                termination_condition="t")

    def test_registering_an_instance_issues_no_delegation(self):
        """`NC-W4-06`. The stages are separate objects, separately created."""
        registry = AgentInstanceRegistry()
        registration = _registered(registry)
        delegations = W4DelegationRegistry(registry)
        self.assertEqual(delegations.for_instance(registration.instance_key), ())
        self.assertEqual(delegations.keys(), ())


class NC_W4_07_ProvenanceIsRequired(unittest.TestCase):
    def test_a_delegation_carries_the_full_chain_to_the_founder(self):
        _, _, _, delegation = _stack()
        chain = delegation.authority_chain()
        self.assertTrue(chain[0].startswith("delegation:"))
        self.assertIn(AUTHORIZED_DELEGATOR, chain[1])
        self.assertIn("FD-P11-001", chain[2])
        self.assertIn("Founder", chain[3])

    def test_a_citation_to_a_nonexistent_instrument_is_refused(self):
        with self.assertRaises(Exception):
            AuthorityProvenance("FD-P11-001", "docs/no-such-decision.md")


class NC_W4_08_09_10_TheDelegatorIsNamedNotAssumed(unittest.TestCase):
    def test_claude_is_not_the_founder(self):
        """`NC-W4-08`. Tested as identity, **not** as substring absence.

        My first version asserted that the delegator string does not contain
        "Founder" — which fails, because ``Co-Founder`` contains it. The
        assertion was wrong and the code was right: the property is that the
        delegator is not the party holding ultimate governance accountability,
        and `§15` names them as distinct rungs of one chain.
        """
        from tools.w4_delegation import ULTIMATE_ACCOUNTABILITY
        self.assertNotEqual(AUTHORIZED_DELEGATOR, ULTIMATE_ACCOUNTABILITY)
        _, _, _, delegation = _stack()
        self.assertNotEqual(delegation.delegator, ULTIMATE_ACCOUNTABILITY)
        self.assertEqual(delegation.authority_chain()[-1],
                         f"founder:{ULTIMATE_ACCOUNTABILITY}")

    def test_engineering_is_not_an_automatic_delegator(self):
        """`§5` rejects the label-becomes-authority assumption."""
        registry = AgentInstanceRegistry()
        registration = _registered(registry)
        delegations = W4DelegationRegistry(registry)
        for label in ("engineering", "Engineering", "platform", "Platform",
                      "Platform Organization"):
            with self.subTest(label=label):
                with self.assertRaises(DelegationError):
                    delegations.issue(
                        delegator=label,
                        recipient_instance=registration.instance_key,
                        authority=AuthorityProvenance("FD-P11-001 §9", FD),
                        objective="o",
                        capability_scope=("engineering-intelligence",),
                        work_scope=("a",), lifecycle_boundary="l",
                        resource_boundary="r", output_expectation="o",
                        verification_requirement="v", escalation_condition="e",
                        accountable_party=AUTHORIZED_DELEGATOR,
                        termination_condition="t")


class NC_W4_16_17_18_AccountabilityAndSelfDelegation(unittest.TestCase):
    def test_an_instance_cannot_be_its_own_accountable_party(self):
        registry = AgentInstanceRegistry()
        registration = _registered(registry)
        delegations = W4DelegationRegistry(registry)
        with self.assertRaises(DelegationError):
            delegations.issue(
                delegator=AUTHORIZED_DELEGATOR,
                recipient_instance=registration.instance_key,
                authority=AuthorityProvenance("FD-P11-001 §9", FD),
                objective="o", capability_scope=("engineering-intelligence",),
                work_scope=("a",), lifecycle_boundary="l",
                resource_boundary="r", output_expectation="o",
                verification_requirement="v", escalation_condition="e",
                accountable_party=registration.instance_key,
                termination_condition="t")

    def test_an_instance_cannot_be_accountable_to_itself_at_registration(self):
        registry = AgentInstanceRegistry()
        with self.assertRaises(InstanceRegistrationError):
            registry.register(
                instance_key="self-accountable-instance", definition=DEFINITION,
                permitted_capabilities=("engineering-intelligence",),
                created_by=AUTHORIZED_DELEGATOR, authority=_fd_authority(),
                accountable_to="self-accountable-instance")

    def test_an_instance_has_no_method_to_delegate_or_authorize(self):
        """`§17`: creating an instance does not authorize it to delegate,
        approve, govern, or authorize another instance."""
        registry, registration, _, _ = _stack()
        for name in dir(registration):
            self.assertFalse(
                any(v in name.lower() for v in
                    ("delegate", "authorize", "approve", "grant", "promote")),
                name)

    def test_accountability_survives_delegation(self):
        """`NC-W4-16`. The delegator remains named on the record."""
        _, _, _, delegation = _stack()
        self.assertEqual(delegation.accountable_party, AUTHORIZED_DELEGATOR)
        self.assertEqual(delegation.delegator, AUTHORIZED_DELEGATOR)


class NoAnonymousInstanceIsValid(unittest.TestCase):
    """`§7`: *"No anonymous Agent Instance is valid."*

    **This control was missing until a mutation probe found it.** Disabling the
    identity check in `agent_instance_registry` left the whole suite passing,
    which meant the suite proved nothing about a requirement the Decision states
    outright. The probe reported `OK` where seven siblings reported `FAILED`, and
    the harness had already ruled out the probe itself being at fault.
    """

    def test_an_unnamed_or_malformed_identity_is_refused(self):
        registry = AgentInstanceRegistry()
        for bad in ("", "   ", None, 42, "x", "UPPERCASE", "has spaces",
                    "-leading-hyphen", "a" * 200):
            with self.subTest(identity=bad):
                with self.assertRaises(InstanceRegistrationError):
                    registry.register(
                        instance_key=bad, definition=DEFINITION,
                        permitted_capabilities=("engineering-intelligence",),
                        created_by=AUTHORIZED_DELEGATOR,
                        authority=_fd_authority(),
                        accountable_to=AUTHORIZED_DELEGATOR)

    def test_a_well_formed_identity_is_accepted(self):
        """The mirror — without it the test above could pass on a registry
        that refuses everything."""
        registry = AgentInstanceRegistry()
        self.assertEqual(_registered(registry).instance_key,
                         "engineering-intelligence-instance-01")

    def test_creator_and_accountability_may_not_be_blank_either(self):
        """`§7` requires creator provenance and an accountability relationship;
        a blank string satisfies neither while looking like a value."""
        registry = AgentInstanceRegistry()
        for field in ("created_by", "accountable_to"):
            with self.subTest(field=field):
                kwargs = dict(
                    instance_key=f"blank-{field.replace('_', '-')}",
                    definition=DEFINITION,
                    permitted_capabilities=("engineering-intelligence",),
                    created_by=AUTHORIZED_DELEGATOR,
                    authority=_fd_authority(),
                    accountable_to=AUTHORIZED_DELEGATOR)
                kwargs[field] = "   "
                with self.assertRaises(InstanceRegistrationError):
                    registry.register(**kwargs)


class Section25_EveryInstanceMustProveTenThings(unittest.TestCase):
    """`§25` items 1–10, each asserted."""

    def setUp(self):
        self.registry = AgentInstanceRegistry()
        self.registration = _registered(self.registry)

    def test_1_derives_from_an_existing_definition(self):
        self.assertIs(self.registration.instance.agent_definition, DEFINITION)

    def test_2_identity_is_unique(self):
        with self.assertRaises(InstanceRegistrationError):
            _registered(self.registry)          # same key twice

    def test_3_creator_provenance_is_recorded(self):
        self.assertEqual(self.registration.created_by, AUTHORIZED_DELEGATOR)

    def test_4_authorization_path_is_valid(self):
        self.assertIn("FD-P11-001", self.registration.authority.instrument)
        self.assertTrue((REPO_ROOT / self.registration.authority.record).is_file())

    def test_5_capability_scope_is_bounded(self):
        self.assertEqual(self.registration.permitted_capabilities,
                         ("engineering-intelligence",))
        for capability in self.registration.permitted_capabilities:
            self.assertIn(capability, DEFINITION.implemented_capabilities)

    def test_6_accountability_owner_is_known(self):
        self.assertTrue(self.registration.accountable_to.strip())
        self.assertNotEqual(self.registration.accountable_to,
                            self.registration.instance_key)

    def test_7_cannot_silently_elevate_its_own_authority(self):
        import dataclasses
        with self.assertRaises(dataclasses.FrozenInstanceError):
            self.registration.permitted_capabilities = ("everything",)

    def test_8_distinguishable_from_the_definition(self):
        self.assertNotEqual(self.registration.instance_key,
                            self.registration.definition_key)

    def test_9_distinguishable_from_a_delegation(self):
        delegations = W4DelegationRegistry(self.registry)
        delegation = _delegation(delegations, self.registration.instance_key)
        self.assertNotEqual(self.registration.instance_key,
                            delegation.delegation_id)

    def test_10_lifecycle_is_verifiable(self):
        self.assertEqual(self.registration.lifecycle, REGISTERED)
        self.assertEqual(self.registry.retire(
            self.registration.instance_key).lifecycle, RETIRED)


class Section26_ADelegationMissingAnyComponentIsBlocked(unittest.TestCase):
    """`§26`: missing any required component means `DELEGATION = BLOCKED`."""

    def test_each_required_element_is_individually_required(self):
        registry = AgentInstanceRegistry()
        registration = _registered(registry)
        delegations = W4DelegationRegistry(registry)
        complete = dict(
            delegator=AUTHORIZED_DELEGATOR,
            recipient_instance=registration.instance_key,
            authority=AuthorityProvenance("FD-P11-001 §9", FD),
            objective="o", capability_scope=("engineering-intelligence",),
            work_scope=("a",), lifecycle_boundary="l", resource_boundary="r",
            output_expectation="oe", verification_requirement="v",
            escalation_condition="e", accountable_party=AUTHORIZED_DELEGATOR,
            termination_condition="t")
        for element in ("objective", "lifecycle_boundary", "resource_boundary",
                        "output_expectation", "verification_requirement",
                        "escalation_condition", "accountable_party",
                        "termination_condition"):
            with self.subTest(element=element):
                incomplete = dict(complete, **{element: ""})
                with self.assertRaises(DelegationError):
                    delegations.issue(**incomplete)


class Section18_TheFullChainExecutes(unittest.TestCase):
    """`§18`: *"No stage may be silently skipped."* Walked end to end."""

    def test_the_authorized_chain_produces_real_execution(self):
        registry, registration, delegations, delegation = _stack()
        surface, plan = _plan()
        executed = []
        report = W4Executor(delegation, registry).execute_plan(
            plan, lambda step: executed.append(step.key) or f"did {step.key}")
        self.assertEqual(executed, ["a", "b"])
        self.assertEqual(report.statuses(), (SUCCESS, SUCCESS))
        self.assertFalse(report.escalated())
        self.assertEqual(report.refusals, [])

    def test_a_step_outside_the_delegation_escalates_and_the_run_continues(self):
        """`§22` fail closed, `§27` continue independent authorized work."""
        registry = AgentInstanceRegistry()
        registration = _registered(registry)
        delegations = W4DelegationRegistry(registry)
        delegation = _delegation(delegations, registration.instance_key,
                                 work_scope=("a",))       # 'b' not delegated
        surface, plan = _plan()
        executed = []
        report = W4Executor(delegation, registry).execute_plan(
            plan, lambda step: executed.append(step.key) or "done")
        self.assertEqual(executed, ["a"])                  # authorized work ran
        self.assertEqual(report.statuses(), (SUCCESS, ESCALATION))
        self.assertEqual(len(report.refusals), 1)
        self.assertEqual(report.refusals[0].required, "b")

    def test_execution_requires_a_live_instance_at_every_step(self):
        registry, registration, delegations, delegation = _stack()
        surface, plan = _plan()
        registry.retire(registration.instance_key)
        report = W4Executor(delegation, registry).execute_plan(
            plan, lambda step: "done")
        self.assertEqual(report.statuses(), (ESCALATION, ESCALATION))

    def test_a_failing_step_is_a_ratified_outcome_not_a_crash(self):
        registry, registration, delegations, delegation = _stack()
        surface, plan = _plan()

        def perform(step):
            if step.key == "b":
                raise RuntimeError("the work failed")
            return "done"

        report = W4Executor(delegation, registry).execute_plan(plan, perform)
        self.assertEqual(report.statuses(), (SUCCESS, "failure"))

    def test_no_stage_may_be_skipped_execution_without_delegation_is_impossible(self):
        registry = AgentInstanceRegistry()
        registration = _registered(registry)
        surface, plan = _plan()
        with self.assertRaises(TypeError):
            W4Executor(None, registry).execute_plan(plan, lambda s: "done")


class Section29_DelegationIsALifecycleObject(unittest.TestCase):
    """`§29`: a Delegation is *"a controlled lifecycle object rather than a
    permanent authority grant."*

    **This was missing until `ACT-CC-P11-008` read `§13` item 14.** The
    delegation carried a `lifecycle_boundary` describing when it should end and
    **no way to end it** — a grant that cannot be withdrawn is the unrestricted
    authority `§11` forbids, wearing a boundary as description.
    """

    def test_a_revoked_delegation_cannot_execute(self):
        registry, registration, delegations, delegation = _stack()
        surface, plan = _plan()
        delegations.revoke(delegation.delegation_id, reason="Proof complete.")
        revoked = delegations.get(delegation.delegation_id)
        self.assertFalse(revoked.is_executable())
        report = W4Executor(revoked, registry).execute_plan(
            plan, lambda step: "should not run")
        self.assertEqual(report.statuses(), (ESCALATION, ESCALATION))

    def test_revocation_preserves_the_terms_that_were_in_force(self):
        registry, registration, delegations, delegation = _stack()
        revoked = delegations.revoke(delegation.delegation_id, reason="Done.")
        self.assertEqual(revoked.capability_scope, delegation.capability_scope)
        self.assertEqual(revoked.authority.instrument,
                         delegation.authority.instrument)
        self.assertEqual(revoked.delegation_id, delegation.delegation_id)

    def test_an_unexplained_revocation_is_refused(self):
        registry, registration, delegations, delegation = _stack()
        with self.assertRaises(DelegationError):
            delegations.revoke(delegation.delegation_id, reason="  ")

    def test_a_termination_condition_is_required_at_issue(self):
        """`§13` item 14. A boundary nobody can act on is a description."""
        registry = AgentInstanceRegistry()
        registration = _registered(registry)
        delegations = W4DelegationRegistry(registry)
        with self.assertRaises(DelegationError):
            delegations.issue(
                delegator=AUTHORIZED_DELEGATOR,
                recipient_instance=registration.instance_key,
                authority=AuthorityProvenance("FD-P11-001 §9", FD),
                objective="o", capability_scope=("engineering-intelligence",),
                work_scope=("a",), lifecycle_boundary="l",
                resource_boundary="r", output_expectation="o",
                verification_requirement="v", escalation_condition="e",
                accountable_party=AUTHORIZED_DELEGATOR,
                termination_condition="")


class ExecutionIsNotAuthority(unittest.TestCase):
    """`§39`: `W4 EXECUTION ≠ GOVERNANCE AUTHORITY`."""

    def test_a_successful_run_widens_nothing(self):
        registry, registration, delegations, delegation = _stack()
        surface, plan = _plan()
        W4Executor(delegation, registry).execute_plan(plan, lambda s: "done")
        self.assertEqual(delegation.capability_scope,
                         ("engineering-intelligence",))
        self.assertFalse(delegation.permits("governance-artifact-integrity"))
        self.assertEqual(registry.get(registration.instance_key)
                         .permitted_capabilities, ("engineering-intelligence",))

    def test_the_executor_cannot_write_a_plan(self):
        """`§19`: the instance does not acquire Planning authority by executing."""
        registry, _, _, delegation = _stack()
        executor = W4Executor(delegation, registry)
        for name in ("adopt", "adapt", "revise", "declare", "plan"):
            self.assertFalse(hasattr(executor, name), name)

    def test_an_outcome_cannot_claim_an_unratified_status(self):
        from tools.w4_execution import ExecutionOutcome
        with self.assertRaises(ValueError):
            ExecutionOutcome(step_key="a", status="authorized", detail="",
                             delegation_id="d", instance_key="i", at="now")

    def test_issuing_a_w4_grant_does_not_write_a_w3_record(self):
        """`§20`: W3 *represents and tracks* the authorized grant — it is not
        written as a side effect of issuing one.

        `ACT-CC-P11-009` established that the two are **one canonical model with
        two projections**, and connected them. Connection is not automation:
        representing a grant in W3 remains a deliberate act, so issuing a
        delegation in memory still writes nothing to the organizational layer.
        """
        before = {r.key for r in read_delegations()}
        registry, registration, delegations, delegation = _stack()
        self.assertEqual({r.key for r in read_delegations()}, before)


if __name__ == "__main__":
    unittest.main()
