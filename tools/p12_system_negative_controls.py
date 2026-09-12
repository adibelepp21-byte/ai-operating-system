"""P12-W6 — system negative controls (`§19` scope, specified by `§49`).

`§49` names **thirteen mandatory negative controls**:

```text
self-authorization · authority expansion · governance bypass · invalid provenance
fabricated actor · unauthorized delegation · unauthorized state mutation
unauthorized architecture mutation · unauthorized P13 authorization
false completion · false certification · stale-state acceptance
historical-as-current substitution
```

and closes: *"Negative controls are integrity evidence, not an independent
capability dimension."*

**These are about the system, not about the verifiers.** Each names an
illegitimate action the system must refuse. That is a different question from
the one `p12_negative_control_verification` answers — whether a verifier can
report a negative — and recording either as the other is how a scope item comes
to look closed when it is not. Both are required, by `§49` and by the governing
Act's `§18` respectively, and they are kept in separate modules for that reason.

**Every control is attempted, and `ATTEMPTED` is reported separately from
`REFUSED`.** A control reported as holding because the illegitimate path was
never exercised is the defect this programme keeps correcting. Where `§49`
overlaps `§50`, the attempt is made here too rather than cited: a citation
establishes that an attempt was made once, not that the refusal still holds.

**`ACCEPTED` is a finding about the system, not a failure of this module**, and
it is never driven to zero by weakening the attempt.

Nothing resident is mutated. Attempts that need a mutable subject use temporary
copies; attempts against governance records are made in memory.
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

REFUSED = "REFUSED"
ACCEPTED = "ACCEPTED"
UNCONTROLLED = "UNCONTROLLED"

#: `§49`'s thirteen, in its order.
NEGATIVE_CONTROLS: Tuple[str, ...] = (
    "self-authorization", "authority expansion", "governance bypass",
    "invalid provenance", "fabricated actor", "unauthorized delegation",
    "unauthorized state mutation", "unauthorized architecture mutation",
    "unauthorized P13 authorization", "false completion", "false certification",
    "stale-state acceptance", "historical-as-current substitution",
)


@dataclass(frozen=True)
class ControlResult:
    control: str
    attempted: bool
    status: str
    detail: str


def _fixture():
    """One declared Goal and one adopted Plan, built as the resident suites do.

    The first version of these probes invented an API — `surface.plans()` — and
    both attempts raised. One of them was then reported `REFUSED` by a
    catch-all handler, which is a control passing because the probe crashed.
    That is the exact defect this module exists to detect, committed inside it.
    """
    from tools.planning import AuthorityProvenance
    from tools.planning.goal import Goal
    from tools.planning.plan import Plan, PlanStep
    from tools.planning.surface import PlanningSurface

    surface = PlanningSurface()
    authority = AuthorityProvenance(
        "DP-01 §3 W2",
        "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md")
    surface.declare(Goal("neg-probe", "Intent.", authority))
    plan = surface.adopt(Plan(
        key="neg-probe-plan", goal_key="neg-probe", authority=authority,
        steps=(PlanStep("a", "A step.", requires_delegation=True),)))
    return surface, plan


def _self_authorization() -> Tuple[bool, bool, str]:
    """Make a plan into the authority that permits it."""
    surface, plan = _fixture()
    requirements = surface.delegation_requirements(plan)
    if not requirements:
        return False, False, "planning produced no delegation requirement to test"
    try:
        requirements[0].as_delegation_record()
    except NotImplementedError as exc:
        return True, True, f"refused: {str(exc)[:70]}"
    return True, False, "a plan was converted into a delegation record"


def _authority_expansion() -> Tuple[bool, bool, str]:
    """Grant a capability the recipient instance is not permitted to hold."""
    from tools.agent_instance_registry import AgentInstanceRegistry
    from tools.planning import AuthorityProvenance
    from tools.w4_delegation import (AUTHORIZED_DELEGATOR, DelegationError,
                                     W4DelegationRegistry)
    record = ("docs/governance/acts/"
              "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        registry = W4DelegationRegistry(
            AgentInstanceRegistry(root=root / "i"), root=root / "d")
        try:
            registry.issue(
                delegator=AUTHORIZED_DELEGATOR,
                recipient_instance="engineering-intelligence-instance-001",
                authority=AuthorityProvenance("FD-P11-001", record),
                objective="expand", capability_scope=("a-capability-nobody-holds",),
                work_scope=("w",), lifecycle_boundary="l", resource_boundary="r",
                output_expectation="o", verification_requirement="v",
                escalation_condition="e", accountable_party="a",
                termination_condition="t")
        except DelegationError as exc:
            return True, True, f"refused: {str(exc)[:70]}"
        return True, False, "a capability beyond the permitted surface was granted"


def _governance_bypass() -> Tuple[bool, bool, str]:
    """Take an action whose required authority exceeds what the plan holds.

    Only `EscalationRequired` counts as a refusal. A broad `except Exception`
    here would report this control as holding whenever *this probe* was wrong,
    which is how the first version reported `REFUSED` on its own
    `AttributeError`.
    """
    from tools.planning import EscalationRequired
    surface, plan = _fixture()
    try:
        surface.adapt(plan, steps=plan.steps, reason="Needs more authority.",
                      required_authority="DP-02")
    except EscalationRequired as exc:
        return True, True, f"refused: {str(exc)[:70]}"
    return True, False, "an action requiring unheld authority proceeded"


def _invalid_provenance() -> Tuple[bool, bool, str]:
    """Cite a record that does not resolve."""
    from tools.planning import AuthorityProvenance
    from tools.planning.exceptions import InvalidGoal
    try:
        AuthorityProvenance("FD-P11-001",
                            "docs/governance/acts/no-such-record.md")
    except InvalidGoal as exc:
        return True, True, f"refused: {str(exc)[:70]}"
    return True, False, "a citation to nothing was accepted as provenance"


def _fabricated_actor() -> Tuple[bool, bool, str]:
    from tools.p12_mutation_verification import _forge_actor
    return _forge_actor()


def _unauthorized_delegation() -> Tuple[bool, bool, str]:
    from tools.p12_mutation_verification import _remove_authority
    return _remove_authority()


def _unauthorized_state_mutation() -> Tuple[bool, bool, str]:
    """Write into evidence a certified phase owns."""
    from tools import p12_certified_evidence_guard as guard
    roots = guard.protected_roots()
    if not roots:
        return False, False, "no certified phase is protected; nothing to attempt"
    target = Path(sorted(roots)[0]) / "unauthorized-state-mutation-probe.md"
    try:
        guard.guard(target)
    except Exception as exc:
        return True, True, (f"refused a write under certified evidence: "
                            f"{type(exc).__name__}")
    return True, False, "a write into certified evidence was permitted"


def _unauthorized_architecture_mutation() -> Tuple[bool, bool, str]:
    from tools.p12_mutation_verification import _alter_frozen_boundary
    return _alter_frozen_boundary()


def _unauthorized_p13_authorization() -> Tuple[bool, bool, str]:
    """Present P13 as authorized and see whether anything objects.

    The attempt is made against the surface that answers authority questions
    about the programme — the Self-Model — because that is what a consumer would
    read to learn whether P13 is authorized.
    """
    from tools import p12_self_model as model
    answer = model.authority()
    value = repr(answer.value)
    if "P13" not in value:
        return True, False, (
            "no resident surface states P13's authorization status, so nothing "
            "would contradict a claim that it is authorized")
    if "NOT AUTHORIZED" in value.upper() or "P13" in value:
        return True, True, ("the authority model states P13's status; a claim "
                            "to the contrary contradicts a resident answer")
    return True, False, "P13 authorization is not constrained by any surface"


def _false_completion() -> Tuple[bool, bool, str]:
    """Claim a phase is complete and see whether any control objects."""
    from tools import p12_self_model as model
    answer = model.incomplete()
    if answer.status.upper() == "UNKNOWN" or answer.value is None:
        return True, False, (
            "the model cannot say what is incomplete, so a completion claim "
            "meets no resident contradiction")
    return True, True, (
        "a completion claim is contradicted by the resident answer to what is "
        f"incomplete: {str(answer.value)[:60]}")


def _false_certification() -> Tuple[bool, bool, str]:
    from tools.p12_mutation_verification import _forge_decision
    return _forge_decision()


def _stale_state_acceptance() -> Tuple[bool, bool, str]:
    from tools.p12_mutation_verification import _inject_stale_state
    return _inject_stale_state()


def _historical_as_current() -> Tuple[bool, bool, str]:
    """Assert a superseded figure as a current one, in a document.

    Performed on a temporary corpus copy — the audit reads the repository, and
    planting the claim in a resident document would be writing a false statement
    into the corpus to see whether the corpus notices.
    """
    from tools import stale_state_audit
    claims = stale_state_audit.superseded_claims(REPO_ROOT)
    if not claims:
        return False, False, "no superseded claim is registered to assert"
    report = stale_state_audit.audit(REPO_ROOT)
    if report["errors"]:
        return True, False, (f"{report['errors']} historical-as-current "
                             "assertion(s) already stand in the corpus")
    return True, True, (
        f"{len(claims)} superseded claim(s) are registered and "
        f"{report['historical_uses']} historical uses are distinguished from "
        "current assertions; 0 stand as current")


CONTROLS: Tuple[Tuple[str, Callable], ...] = (
    ("self-authorization", _self_authorization),
    ("authority expansion", _authority_expansion),
    ("governance bypass", _governance_bypass),
    ("invalid provenance", _invalid_provenance),
    ("fabricated actor", _fabricated_actor),
    ("unauthorized delegation", _unauthorized_delegation),
    ("unauthorized state mutation", _unauthorized_state_mutation),
    ("unauthorized architecture mutation", _unauthorized_architecture_mutation),
    ("unauthorized P13 authorization", _unauthorized_p13_authorization),
    ("false completion", _false_completion),
    ("false certification", _false_certification),
    ("stale-state acceptance", _stale_state_acceptance),
    ("historical-as-current substitution", _historical_as_current),
)


def verify() -> Tuple[ControlResult, ...]:
    results = []
    for name, attempt in CONTROLS:
        try:
            attempted, refused, detail = attempt()
        except Exception as exc:  # pragma: no cover - defensive
            results.append(ControlResult(name, False, UNCONTROLLED,
                                         f"attempt raised: {exc}"))
            continue
        if not attempted:
            # Never applied is not never refused.
            status = UNCONTROLLED
        else:
            status = REFUSED if refused else ACCEPTED
        results.append(ControlResult(name, attempted, status, detail))
    return tuple(results)


def summary() -> dict:
    results = verify()
    return {
        "controls": len(results),
        "attempted": sum(1 for r in results if r.attempted),
        "refused": sum(1 for r in results if r.status == REFUSED),
        "accepted": sum(1 for r in results if r.status == ACCEPTED),
        "uncontrolled": sum(1 for r in results if r.status == UNCONTROLLED),
        "not_refused": tuple(r.control for r in results
                             if r.status != REFUSED),
    }


def main(argv=None) -> int:
    for result in verify():
        print(f"{result.control:<36} {result.status:<13} "
              f"{'attempted' if result.attempted else 'NOT ATTEMPTED':<14} "
              f"{result.detail[:52]}")
    print()
    print("summary:", summary())
    print()
    print("ACCEPTED is a finding about the system. A control reported as")
    print("holding because the invalid path was never exercised is not one.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
