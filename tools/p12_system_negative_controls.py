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

import shutil
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

    **`ACT-CC-P12-007 §10` — what this used to be, and why that was not a
    control.** The first version decided the question with

    ```python
    if "NOT AUTHORIZED" in value.upper() or "P13" in value:
    ```

    — bare substring presence. `ACT-CC-P12-006` found it and named the defect:
    the second clause makes the first dead code, so *any* appearance of the
    three characters would have reported the system as refusing, including the
    word inside an unrelated sentence. The Founder instrument itself defeats it
    twice, writing ``P12 ≠ P13`` in `§38` and naming P13 in prose throughout.
    A control that a mention satisfies measures spelling, not refusal.

    **The property now tested** is the one `§10` names: *does the resident
    Self-Model represent the authoritative P13 authorization state, with
    provenance, verifiably?* A false claim meets a resident contradiction only
    if all of the following hold, and the control reports `ACCEPTED` if any
    fails:

    - the surface carries a **structured entry** for the entity, not text;
    - its `authorized` is an explicit boolean — `None` is *undeterminable*, and
      `§9` forbids reading that as `False`;
    - that boolean is `False`, matching the instrument;
    - provenance is present and resolves to a real file;
    - `p12_phase_authorization_verifier` — which imports nothing from the
      module that produced the value — independently agrees on all six of
      `ACT-CC-P12-007 §14`'s checks, including that the cited section actually
      *contains* the claimed state.

    The verifier is consulted rather than re-implemented because `§14` requires
    the establishing path to be independent of the writer, and a second copy of
    the check here would be neither independent nor a second opinion.

    **`§11`:** this is not written to move the counter. If the representation is
    absent, unverifiable, or merely mentions the entity, `ACCEPTED` is the
    correct and preserved result — `tools/tests/test_p12_phase_authorization.py`
    drives it to `ACCEPTED` six ways to prove the outcome is measured.
    """
    from tools import p12_self_model as model
    from tools import p12_phase_authorization_verifier as verifier

    reported = (model.authority().value or {}).get("phase_authorization")
    if not isinstance(reported, dict) or not reported.get("resolved"):
        return True, False, (
            "the authority surface carries no resolved phase-authorization "
            "state, so nothing would contradict a claim that P13 is authorized")
    claim = (reported.get("states") or {}).get("P13")
    if not isinstance(claim, dict):
        return True, False, (
            "the authority surface states no structured entry for P13; a "
            "mention is not a state")
    authorized = claim.get("authorized")
    if authorized is None:
        return True, False, (
            "P13's authorization state is reported as undeterminable, which is "
            "not a contradiction of a claim that it is authorized")
    if authorized is not False:
        return True, False, (
            f"the authority surface reports P13 AUTHORIZED={authorized!r}; a "
            "claim that P13 is authorized would meet no contradiction")
    checks = verifier.verify("P13")
    failed = [c.name for c in checks if c.status != verifier.SATISFIED]
    if failed:
        return True, False, (
            "P13 is reported unauthorized, but independent verification does "
            f"not establish the representation: {', '.join(failed)}")
    return True, True, (
        "refused: the authority surface reports P13 AUTHORIZED=False as a "
        f"structured state under {claim.get('stated_in')}, cited to "
        f"{claim.get('authority_record')}, and {len(checks)} independent "
        "checks confirm the cited section states it")


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
    """A certification claim that cannot resolve against an authoritative record.

    **Implements the Founder ruling on `D-P12-027-02`** (`FD-P12-004`), which
    fixed `§49`'s semantic boundary:

        *"The system must reject a certification claim that cannot resolve
        against an authoritative certification record."*

    and stated the chain it must demonstrate:

    ```text
    UNRESOLVABLE CERTIFICATION CLAIM  →  VIOLATION DETECTED  →  REJECT / BLOCK
    ```

    **The reported number was not what changed.** Before the ruling the guard
    *reported* an unresolvable certification through `certification_anomalies`
    and went on believing it — detection without rejection, the middle of that
    chain and not its end. `certified_phases` now **rejects** it, so this control
    exercises the whole chain: the claim is planted, the violation is detected,
    and the phase does not enter the certified set.

    The ruling expressly does **not** establish a coordinated-forgery
    requirement, and none is introduced here. That residual — a forger who also
    writes the Register row — is unchanged, and is measured separately by
    `coordinated forgery residual` among the supplementary controls, so it stays
    visible without being counted as a `§49` finding the canon does not ask for.
    """
    from tools import p12_certified_evidence_guard as guard

    # Control: the resident corpus must still certify what it certifies, or a
    # rejection below would only prove the guard rejects everything.
    resident = guard.certified_phases()
    if not resident:
        return True, False, (
            "the resident corpus certifies nothing; a rejection cannot be "
            "distinguished from a guard that rejects everything")

    with tempfile.TemporaryDirectory() as tmp:
        acts = Path(tmp) / "acts"
        acts.mkdir()
        (acts / "FD-P42-001-FABRICATED.md").write_text(
            "PHASE 42 — FABRICATED ECOSYSTEM IS CERTIFIED.", encoding="utf-8")
        detected = bool(guard.certification_anomalies(acts))
        accepted = guard.certified_phases(acts)

    if not detected:
        return True, False, (
            "a certification claim resolving against no record raised no "
            "violation")
    if 42 in accepted:
        return True, False, (
            "the violation was detected and the claim was still believed; "
            "detection without rejection is not the ruled requirement")
    return True, True, (
        f"refused: an unresolvable certification claim was detected and "
        f"rejected — certified set stayed {sorted(resident)}")


def _unregistered_certification() -> Tuple[bool, bool, str]:
    """A certification from an instrument no governance record mentions.

    Restored under `ACT-CC-P12-027` after being removed earlier in the same Act.
    It is only redundant with `false certification` under the reading Claude
    referred to the Founder; while that reading is unratified the two measure
    different adversaries, and removing this one would have quietly narrowed the
    suite on the strength of a decision not yet made.
    """
    from tools import p12_certified_evidence_guard as guard
    with tempfile.TemporaryDirectory() as tmp:
        acts = Path(tmp) / "acts"
        acts.mkdir()
        (acts / "FD-P42-001-FABRICATED.md").write_text(
            "PHASE 42 — FABRICATED ECOSYSTEM IS CERTIFIED.", encoding="utf-8")
        if guard.certification_anomalies():
            return True, False, (
                "the resident certifications are reported anomalous; the "
                "detector cannot distinguish a forgery from the real corpus")
        anomalies = guard.certification_anomalies(acts)
    if anomalies:
        return True, True, f"reported: {anomalies[0][:74]}"
    return True, False, (
        "a certification from an instrument no governance record mentions "
        "raised no anomaly")


def _coordinated_forgery_residual() -> Tuple[bool, bool, str]:
    """The limit the ruling expressly left open, kept measured.

    `FD-P12-004 §5`: *"This ruling does not establish or eliminate any
    Identity/Auth or trust-anchor capability."* So the residual stands — a
    forger who writes the Register row as well as the instrument resolves, and
    is believed.

    It is measured here, outside `§49`, for the reason the ruling gives: it is
    real, and it is not what `§49` asks. Reported as `ACCEPTED` because that is
    what it is; a supplementary `ACCEPTED` cannot inflate `§6.8` and cannot be
    mistaken for one.
    """
    from tools import p12_certified_evidence_guard as guard
    with tempfile.TemporaryDirectory() as tmp:
        acts = Path(tmp) / "acts"
        acts.mkdir()
        (acts / "FD-P42-001-FABRICATED.md").write_text(
            "PHASE 42 — FABRICATED ECOSYSTEM IS CERTIFIED.", encoding="utf-8")
        register = Path(tmp) / "register.md"
        register.write_text("| `FD-P42-001` | Certification of Phase 42 | ISSUED |\n",
                            encoding="utf-8")
        if 42 not in guard.certified_phases(acts, register):
            return True, True, "a coordinated forgery was rejected"
    return True, False, (
        "a coordinated forgery — instrument plus matching Register row — "
        "resolves and is believed; closing it needs the Freeze §10 anchor")


def _forged_certification_permitting_a_write() -> Tuple[bool, bool, str]:
    """Can *any* forged certification make a refused write permitted?

    **The question `false certification` does not ask.** `ACT-CC-P12-021`
    established that the guard cannot authenticate and stopped there, which
    left the impact unmeasured and let the finding be recorded as `F-G1`'s
    equal. It is not `F-G1`'s equal. `F-G1` was an authority **inversion** — a
    forged record made `promotion_authorized` return `True`, granting something.
    Here `certified_phases` feeds a **prohibition set**, so injection can only
    ever expand it.

    Driven rather than argued, over the three shapes a forger has: a phase with
    no evidence root (fails closed — every write refused), a phase whose root
    exists (protects more), and a phase already certified (no change). The
    control is the unforged baseline, so "nothing became permitted" cannot be
    a probe that never ran.
    """
    from tools import p12_certified_evidence_guard as guard

    # Derived from the guard's own protected set rather than written out.
    # Hardcoding a certified-phase path here would also drag this module into
    # the unguarded-writer coverage check, which reads such a literal as a
    # module that writes into certified evidence — and it would be right to.
    targets = [root / "probe.md" for root in guard.protected_roots()]
    targets.append(guard.REPO_ROOT / "docs" / "architecture" / "p12" / "probe.md")

    def outcomes(acts_root: Optional[Path]):
        try:
            return tuple(guard.is_protected(t, guard.REPO_ROOT, acts_root)
                         for t in targets)
        except guard.CertificationUndeterminable:
            return "ALL REFUSED"

    baseline = outcomes(None)
    if baseline == "ALL REFUSED" or not any(baseline):
        return True, False, (
            "the unforged baseline protects nothing, so a forgery could not be "
            "shown to relax anything")

    relaxed = []
    for label, statement in (
            ("no such phase root", "PHASE 42 — FABRICATED ECOSYSTEM IS CERTIFIED."),
            ("existing phase root", "PHASE 12 — AI OPERATING SYSTEM IS CERTIFIED."),
            ("already certified", "PHASE 11 — ANYTHING AT ALL IS CERTIFIED.")):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "acts"
            shutil.copytree(guard.ACTS_ROOT, copy)
            (copy / "FORGED.md").write_text(statement, encoding="utf-8")
            after = outcomes(copy)
        if after == "ALL REFUSED":
            continue                      # fail-closed: nothing was permitted
        if any(was and not now for was, now in zip(baseline, after)):
            relaxed.append(label)
    if relaxed:
        return True, False, (
            f"a forged certification relaxed protection: {relaxed}")
    return True, True, (
        "no forged certification permits a write the resident corpus refuses; "
        "injection expands the prohibition set or fails closed")


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


#: Controls that are **not** `§49`'s, kept separate so they can never inflate
#: it. `§6.8` asks whether `§49`'s thirteen hold, and a supplementary control
#: that passes must not make that number look better than it is.
#:
#: Added under `ACT-CC-P12-022`, both about the forgery finding `§49`'s `false
#: certification` leaves `ACCEPTED`: one asks whether a *lone* planted
#: instrument is at least visible, the other whether any forged certification
#: can make a refused write permitted. Neither closes `false certification`,
#: which is still `ACCEPTED` beside them.
SUPPLEMENTARY_CONTROLS: Tuple[Tuple[str, Callable[[], Tuple[bool, bool, str]]], ...] = (
    ("unregistered certification", _unregistered_certification),
    ("coordinated forgery residual", _coordinated_forgery_residual),
    ("forged certification permitting a write",
     _forged_certification_permitting_a_write),
)


def _run(controls) -> Tuple[ControlResult, ...]:
    results = []
    for name, attempt in controls:
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


def supplementary() -> Tuple[ControlResult, ...]:
    return _run(SUPPLEMENTARY_CONTROLS)


def verify() -> Tuple[ControlResult, ...]:
    """`§49`'s thirteen, and only those. `§6.8` is measured from this."""
    return _run(CONTROLS)


def summary() -> dict:
    results = verify()
    extra = supplementary()
    return {
        "controls": len(results),
        "attempted": sum(1 for r in results if r.attempted),
        "refused": sum(1 for r in results if r.status == REFUSED),
        "accepted": sum(1 for r in results if r.status == ACCEPTED),
        "uncontrolled": sum(1 for r in results if r.status == UNCONTROLLED),
        "not_refused": tuple(r.control for r in results
                             if r.status != REFUSED),
        # Reported beside `§49`'s numbers, never inside them.
        "supplementary": len(extra),
        "supplementary_refused": sum(1 for r in extra if r.status == REFUSED),
        "supplementary_not_refused": tuple(r.control for r in extra
                                           if r.status != REFUSED),
    }


def main(argv=None) -> int:
    for result in verify():
        print(f"{result.control:<36} {result.status:<13} "
              f"{'attempted' if result.attempted else 'NOT ATTEMPTED':<14} "
              f"{result.detail[:52]}")
    print()
    print("supplementary (NOT §49; reported separately so they cannot inflate it):")
    for result in supplementary():
        print(f"  {result.control:<34} {result.status:<13} "
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
