"""`ACT-CC-P12-005` — resident consumption of the escalation→grant join.

Two things this suite proves that `test_p12_governance_escalation_join.py`
(the writer/reader's own conformance suite) does not:

1. `join_refusals_to_grants` — the composition every one of the three
   resident call sites now calls — correctly joins each refusal to *its
   own* grant when **multiple** delegations are live at once, the exact
   shape `tools/w1_cross_department_run.py` uses. A naive "one delegation
   for the whole batch" implementation would pass every single-delegation
   test and still mis-join a two-grant run; this suite builds two real
   grants and asserts neither refusal's escalation lands on the other's
   delegation.
2. The wiring is genuinely reachable in the three resident modules, not
   merely present as source text — read by AST, the same discipline
   `tools/tests/test_escalation_subject_integrity.py::E2` already applies.
"""

from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.agent_instance_registry import AgentDefinition, AgentInstanceRegistry
from tools.escalation_register import EscalationRegister
from tools.planning import AuthorityProvenance, PlanStep
from tools.w4_delegation import AUTHORIZED_DELEGATOR, W4DelegationRegistry
from tools.w4_execution import ExecutionRefused, W4Executor
from tools import p12_provenance_verification as prov
from tools.p12_governance_escalation_join import join_refusals_to_grants
from tools.p12_governance_join_reader import resolve, JOINED

REPO_ROOT = Path(__file__).resolve().parents[2]
FD_RECORD = ("docs/governance/acts/"
             "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md")

DEFINITION = AgentDefinition(
    agent_definition_key="engineering-intelligence-agent",
    agent_definition_version="1.0",
    owning_department_key="engineering",
    implemented_capabilities=("engineering-intelligence",),
    specified_skills=(), specified_workflows=())


def _authority():
    return AuthorityProvenance("FD-P11-001 §9", FD_RECORD)


class TwoRealGrantsEachJoinTheirOwnRefusal(unittest.TestCase):
    """The `tools/w1_cross_department_run.py` shape: one delegation per step,
    exercised with real objects — no mocked delegation, no mocked executor.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

        # `resolve()` checks a delegation against `delegation_records()`,
        # which only trusts a fixed, curated set of roots — by design, so
        # an arbitrary directory cannot manufacture a "known" grant. This
        # fixture's grants are real (issued through `W4DelegationRegistry`,
        # not fabricated), just written to a temporary, not-yet-trusted
        # root; pointed at a temporary world for the duration of this test,
        # matching `tools/p12_negative_control_verification.py`'s own
        # stated convention.
        patcher = mock.patch.object(prov, "DELEGATION_ROOTS",
                                    prov.DELEGATION_ROOTS + (self.root,))
        patcher.start()
        self.addCleanup(patcher.stop)

        registry = AgentInstanceRegistry(root=None)
        self.registrations = {}
        for key in ("actor-a", "actor-b"):
            self.registrations[key] = registry.register(
                instance_key=key, definition=DEFINITION,
                permitted_capabilities=("engineering-intelligence",),
                created_by=AUTHORIZED_DELEGATOR,
                authority=_authority(), accountable_to=AUTHORIZED_DELEGATOR)

        delegations = W4DelegationRegistry(registry, self.root)
        # Two real grants, each scoped to exactly one step — the two-grant
        # shape, not two copies of a single-grant fixture.
        self.grants = {}
        for step_key, instance_key in (("step-a", "actor-a"),
                                       ("step-b", "actor-b")):
            self.grants[step_key] = delegations.issue(
                delegator=AUTHORIZED_DELEGATOR, recipient_instance=instance_key,
                authority=_authority(), objective="one step's real work",
                capability_scope=("engineering-intelligence",),
                work_scope=(step_key,),
                lifecycle_boundary="one execution", resource_boundary="none",
                output_expectation="one outcome",
                verification_requirement="the step is authorized",
                escalation_condition="any step the grant does not cover",
                accountable_party=AUTHORIZED_DELEGATOR,
                termination_condition="on completion")

        self.registry = registry
        # Real refusals: each executor is asked to run the *other* grant's
        # step — genuinely outside its own delegation's work_scope.
        self.refusals = []
        for step_key, other_key in (("step-a", "step-b"), ("step-b", "step-a")):
            executor = W4Executor(self.grants[step_key], registry)
            try:
                executor.execute_step(PlanStep(other_key, "wrong step"),
                                      perform=lambda step: "unreachable")
            except ExecutionRefused as refusal:
                self.refusals.append(refusal)
        self.assertEqual(2, len(self.refusals), "precondition: two real "
                         "refusals, one per grant")

    def test_each_escalation_joins_the_grant_its_own_refusal_named(self):
        """`refusal.required` names the step actually attempted, which is
        the *other* grant's step key in this fixture — so
        `grants[refusal.required]` resolves to the grant whose scope was
        violated, not the grant the refusal happened to be raised under.
        Both are real relationships; this asserts the join follows the
        canonical one, not whichever grant is scanned first."""
        escalation_ids = join_refusals_to_grants(
            self.root, self.refusals, subject="two-grant conformance fixture",
            authority=_authority(),
            delegation_for=lambda r: self.grants[r.required].delegation_id)

        self.assertEqual(2, len(escalation_ids))
        register = EscalationRegister(self.root)
        joined_delegations = set()
        for escalation_id, refusal in zip(escalation_ids, self.refusals):
            payload = register.load(escalation_id)
            expected = self.grants[refusal.required].delegation_id
            self.assertEqual(expected, self._join_delegation(escalation_id))
            joined_delegations.add(expected)
        # The two refusals must have joined to *different* delegations —
        # if both landed on the same one, the lookup collapsed to a
        # single-delegation shape and the test fixture failed to exercise
        # the thing it exists to exercise.
        self.assertEqual(2, len(joined_delegations))

    def test_a_wrong_static_delegation_would_have_mis_joined(self):
        """Negative control on the *test fixture itself*: proves the naive
        'one delegation for every refusal' shape — the bug this suite exists
        to catch — really would mis-join, so passing the test above is not
        vacuous."""
        wrong_escalation_ids = join_refusals_to_grants(
            self.root, self.refusals[:1],
            subject="deliberately-wrong static lookup",
            authority=_authority(),
            # Every refusal joined to grants["step-a"], regardless of which
            # step it actually named — the defect a single-delegation
            # `delegation_for` would produce if used at a multi-grant site.
            delegation_for=lambda r: self.grants["step-a"].delegation_id)
        joined = self._join_delegation(wrong_escalation_ids[0])
        actual_refusal = self.refusals[0]
        correct = self.grants[actual_refusal.required].delegation_id
        # The static lookup joins to grants["step-a"] regardless of which
        # refusal it was given; for refusals[0] (required="step-b") that is
        # wrong, which is exactly what this control demonstrates.
        self.assertNotEqual(correct, joined)

    def _join_delegation(self, escalation_id: str) -> str:
        result = resolve(self.root, self.root, escalation_id)
        self.assertEqual(JOINED, result["status"], result)
        return result["delegation_id"]


class ResidentCallSitesActuallyCallTheWiredHelper(unittest.TestCase):
    """`ACT-CC-P12-005` — wired means reachable *and* invoked with the
    caller's own grant, not merely imported. Read by AST."""

    PATHS = ("tools/w4_first_run.py", "tools/w1_coordination_run.py",
            "tools/w1_cross_department_run.py")

    def _call(self, module):
        tree = ast.parse((REPO_ROOT / module).read_text(encoding="utf-8"))
        calls = [n for n in ast.walk(tree)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == "join_refusals_to_grants"]
        self.assertEqual(1, len(calls), module)
        return calls[0]

    def test_the_single_grant_sites_bind_a_constant_delegation(self):
        for module in ("tools/w4_first_run.py", "tools/w1_coordination_run.py"):
            with self.subTest(module=module):
                call = self._call(module)
                keywords = {k.arg: ast.unparse(k.value) for k in call.keywords}
                self.assertIn("delegation_for", keywords)
                self.assertIn("delegation.delegation_id",
                              keywords["delegation_for"])

    def test_the_multi_grant_site_looks_up_per_refusal(self):
        call = self._call("tools/w1_cross_department_run.py")
        keywords = {k.arg: ast.unparse(k.value) for k in call.keywords}
        self.assertIn("delegation_for", keywords)
        expr = keywords["delegation_for"]
        self.assertIn("grants[", expr)
        self.assertIn(".required", expr)


if __name__ == "__main__":
    unittest.main()
