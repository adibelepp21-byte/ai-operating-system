"""`P12-W3` — one real refusal, escalated, and joined to its grant by reference.

`ACT-CC-P12-W3-001 §16`-equivalent (this programme's standing rule,
`ACT-CC-P12-W4-001 §16`): real system work, not a unit test, not a mock, not a
demonstrator. This script issues one real delegation, runs a plan with one
step genuinely outside that delegation's work scope, lets `W4Executor` refuse
it for real (`tools/w4_execution.py`), records the refusal as a real
organizational escalation (`tools/escalation_register.py`, unmodified,
reused), and joins that escalation to the grant it was raised under
(`tools/p12_governance_escalation_join.py`) — structurally, from the
delegation object this script holds, not parsed from anything.

**The subject text is deliberately worded so the existing prose-regex
(`tools/p12_failure_verification.escalation_join`) does not match it.** The
one resident historical escalation joins by parsed prose because its subject
happened to contain the words `"delegation <id>"`; this run's subject does
not, so if the new escalation joins at all, it joins only through the
structural reference this script writes — which is the property `W4-GAP-008`
asked for and the demonstration this script exists to provide.

Verification is not performed here, for the same reason
`p12_w4_integrated_execution.py` does not verify its own chain: `§24`
requires the verdict to come from a reader that did not write the records.
`tools/p12_governance_join_reader.py` is that reader.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.agent_instance_registry import (  # noqa: E402
    AgentDefinition, AgentInstanceRegistry)
from tools.escalation_register import (  # noqa: E402
    EscalationRegister, record_refusals)
from tools.planning import AuthorityProvenance, Plan, PlanStep  # noqa: E402
from tools.w4_delegation import (  # noqa: E402
    AUTHORIZED_DELEGATOR, W4DelegationRegistry)
from tools.w4_execution import W4Executor  # noqa: E402
from tools.p12_governance_escalation_join import (  # noqa: E402
    join_escalation_to_grant)

FD_RECORD = ("docs/governance/acts/"
             "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md")
DP01_RECORD = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"

INSTANCE_KEY = "engineering-intelligence-instance-p12w3-001"

#: The existing P12-W4 delegation root, reused rather than duplicated.
#: `tools/p12_provenance_verification.DELEGATION_ROOTS` already searches this
#: exact directory — adding a new, unlisted root repeats the defect this
#: programme already found once (`p12_provenance_verification.py:40-44`).
DELEGATION_ROOT = REPO_ROOT / "docs/architecture/p12/w4-operations"

#: A new, honestly-labeled home for this run's escalation and join records.
#: `tools/p12_failure_verification.escalation_join` globs
#: `docs/architecture/**/*.escalation.json`, which already covers this path.
GOVERNANCE_ROOT = REPO_ROOT / "docs/architecture/p12/w3-operations"

DEFINITION = AgentDefinition(
    agent_definition_key="engineering-intelligence-agent",
    agent_definition_version="1.0",
    owning_department_key="engineering",
    implemented_capabilities=("engineering-intelligence",),
    specified_skills=(), specified_workflows=())

#: The delegation grants exactly this one step.
WORK_SCOPE = ("verify-delegation-elements",)

#: This step is real, and outside `WORK_SCOPE` — the same shape as the one
#: resident historical refusal (`23f315ba9f504272`), constructed fresh so a
#: new, structurally-joined escalation exists rather than the historical one
#: being retroactively reinterpreted.
OUT_OF_SCOPE_STEP = "report-governance-join-proof"

GOAL_KEY = "p12-w3-governance-escalation"
PLAN_KEY = "p12-w3-governance-escalation-plan-0"


def run(*, persist: bool = True) -> dict:
    """Run once. Returns what was produced, not a verdict."""
    plan_authority = AuthorityProvenance("DP-01 §3 W2", DP01_RECORD)
    plan = Plan(
        key=PLAN_KEY, goal_key=GOAL_KEY, authority=plan_authority,
        steps=(
            PlanStep("verify-delegation-elements",
                     "In-scope step: satisfied by delegation issuance.",
                     requires_delegation=True),
            PlanStep(OUT_OF_SCOPE_STEP,
                     "Out-of-scope step: report that the governance join "
                     "this run exists to prove was written. `§22`: the "
                     "organization may execute more work, it may not "
                     "expand the authority under which it operates.",
                     requires_delegation=True),
        ))

    delegation_root = DELEGATION_ROOT if persist else None
    registry = AgentInstanceRegistry(root=None)
    registration = registry.register(
        instance_key=INSTANCE_KEY, definition=DEFINITION,
        permitted_capabilities=("engineering-intelligence",),
        created_by=AUTHORIZED_DELEGATOR,
        authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
        accountable_to=AUTHORIZED_DELEGATOR)
    delegations = W4DelegationRegistry(registry, delegation_root)
    delegation = delegations.issue(
        delegator=AUTHORIZED_DELEGATOR,
        recipient_instance=registration.instance_key,
        authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
        objective="Prove one real refusal can be escalated and joined to "
                  "its grant by structured reference (W4-GAP-008).",
        capability_scope=("engineering-intelligence",),
        work_scope=WORK_SCOPE,
        lifecycle_boundary=f"one execution of plan {PLAN_KEY}",
        resource_boundary="no repository mutation outside "
                          "docs/architecture/p12",
        output_expectation="one escalation, structurally joined to this "
                           "grant",
        verification_requirement="the join independently resolves through "
                                 "tools/p12_governance_join_reader",
        escalation_condition="any step outside the delegated work scope",
        accountable_party=AUTHORIZED_DELEGATOR,
        termination_condition=f"on completion of plan {PLAN_KEY}")

    executor = W4Executor(delegation, registry)
    report = executor.execute_plan(
        plan, perform=lambda step: "satisfied by delegation issuance")

    if len(report.refusals) != 1:
        raise RuntimeError(
            f"expected exactly one real refusal, got {len(report.refusals)} "
            "— this run's proof depends on the out-of-scope step actually "
            "being refused")
    refusal = report.refusals[0]

    escalation_id = None
    join = None
    if persist:
        # `§13`: `REUSE → FIX → INTEGRATE → VERIFY` before building anything
        # new — the same one wiring path `tools/w4_first_run.py`,
        # `tools/w1_coordination_run.py` and `tools/w1_cross_department_run.py`
        # already share (`test_escalation_subject_integrity.py::E2`).
        (escalation_id,) = record_refusals(
            GOVERNANCE_ROOT, [refusal],
            subject="P12-W3 real refusal proof for FD-P11-001 conformance "
                    "— structural join only, no parsed reference intended",
            authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD))
        register = EscalationRegister(GOVERNANCE_ROOT)
        join = join_escalation_to_grant(
            GOVERNANCE_ROOT, register, escalation_id,
            delegation_id=delegation.delegation_id,
            refusal_type=type(refusal).__name__)

    return {
        "delegation_id": delegation.delegation_id,
        "refusal_required": refusal.required,
        "refusal_held": refusal.held,
        "escalation_id": escalation_id,
        "join": join.to_payload() if join else None,
    }


def main() -> int:
    result = run(persist=True)
    for key, value in result.items():
        print(f"{key:<18} {value}")
    print()
    print("Persisted. The verdict is not this script's to give —")
    print("run `python3 -m tools.p12_governance_join_reader` "
          "or the conformance suite.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
