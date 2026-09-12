"""P12-W6 — phase-level mutation verification (`§50`, `§19` scope: `MUTATION`).

`§50`: *"Mutation tests shall deliberately attempt to violate critical
contracts"*, naming ten. Expected result:

```text
VIOLATION DETECTED
ACTION REJECTED / BLOCKED / ESCALATED
```

**Every mutation here is actually attempted.** A control reported as holding
because the invalid path was never exercised is the defect this programme has
corrected repeatedly, so each function performs the violation against the real
detector and records what came back. `ATTEMPTED` is reported separately from
`DETECTED` precisely so an unexercised control cannot masquerade as a passing
one.

**A `MISSED` result is the point, not a failure of the suite.** `§50` asks
whether the system detects these violations; where it does not, the honest
output is `MISSED` with the reason, because a mutation suite that returns ten
detections is indistinguishable from one that attempts nothing.

Nothing here mutates a real artifact. Certified evidence is protected by `F-12`
and is not written; where a mutation needs a mutable subject it is performed on a
temporary copy, so the attempt is genuine and the corpus is untouched.
"""

from __future__ import annotations

import json
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

DETECTED = "DETECTED"
MISSED = "MISSED"
UNAVAILABLE = "UNAVAILABLE"


@dataclass(frozen=True)
class MutationResult:
    mutation: str
    attempted: bool
    status: str
    detail: str


#: `FD-P11-001` as it is resident. A delegation attempt needs *valid* provenance
#: before the mutation under test is the only thing wrong with it — otherwise the
#: refusal proves the citation check works, not the control being mutated.
AUTHORIZING_RECORD = (
    "docs/governance/acts/"
    "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md")


def _delegation_fixture(tmp: Path):
    """An isolated delegation registry plus one otherwise-valid grant request.

    Every `§13` element is supplied so that the *only* defect in each attempt is
    the mutation itself. An attempt that is refused for an unrelated reason —
    missing element, unresolvable citation — would report a detection the
    mutated control never made.
    """
    from tools.planning import AuthorityProvenance
    from tools.agent_instance_registry import AgentInstanceRegistry
    from tools.w4_delegation import W4DelegationRegistry

    registry = W4DelegationRegistry(
        AgentInstanceRegistry(root=tmp / "instances"), root=tmp / "delegations")
    request = dict(
        authority=AuthorityProvenance(instrument="FD-P11-001",
                                      record=AUTHORIZING_RECORD),
        objective="mutation probe", capability_scope=("probe",),
        work_scope=("probe",), lifecycle_boundary="single attempt",
        resource_boundary="temporary directory",
        output_expectation="refusal or acceptance",
        verification_requirement="observed here",
        escalation_condition="acceptance",
        accountable_party="mutation-verification",
        termination_condition="attempt returns")
    return registry, request


def _remove_authority() -> Tuple[bool, bool, str]:
    """Issue a delegation from a delegator the Founder Decision did not name."""
    from tools.w4_delegation import AUTHORIZED_DELEGATOR, DelegationError
    with tempfile.TemporaryDirectory() as tmp:
        registry, request = _delegation_fixture(Path(tmp))
        try:
            registry.issue(delegator="some-unauthorized-party",
                           recipient_instance="mutation-probe-instance-001",
                           **request)
        except DelegationError as exc:
            return True, True, f"refused: {str(exc)[:70]}"
        return True, False, (
            f"accepted a delegator other than {AUTHORIZED_DELEGATOR!r}")


def _forge_actor() -> Tuple[bool, bool, str]:
    """Delegate to an Agent Instance that was never registered."""
    from tools.w4_delegation import AUTHORIZED_DELEGATOR, DelegationError
    with tempfile.TemporaryDirectory() as tmp:
        registry, request = _delegation_fixture(Path(tmp))
        try:
            registry.issue(delegator=AUTHORIZED_DELEGATOR,
                           recipient_instance="instance-that-does-not-exist",
                           **request)
        except DelegationError as exc:
            return True, True, f"refused: {str(exc)[:70]}"
        return True, False, "accepted an unregistered Agent Instance"


def _inject_stale_state() -> Tuple[bool, bool, str]:
    """Publish a RUNNING observation older than the liveness horizon."""
    from tools import p12_runtime_observation as obs
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        when = datetime.now(timezone.utc) - timedelta(
            seconds=obs.LIVE_HORIZON_SECONDS + 3600)
        obs.publish("stale-runtime", "RuntimeState.RUNNING", root=root, now=when)
        answer = obs.what_is_running(root)
        if not answer["answerable"]:
            return True, True, "stale RUNNING refused as evidence of current state"
        return True, False, "a stale RUNNING record was accepted as live"


def _break_workflow() -> Tuple[bool, bool, str]:
    """Attempt an illegal Workflow lifecycle transition."""
    from native_core.core.workflow import (
        Workflow, WorkflowIdentity, WorkflowLifecycle)
    from native_core.core.workflow.exceptions import InvalidWorkflowTransition
    identity = WorkflowIdentity(workflow_key="mutation-probe", workflow_version="1.0")
    lifecycle = WorkflowLifecycle()
    lifecycle.define(Workflow(identity=identity))
    try:
        lifecycle.succeed(identity)   # DEFINED → SUCCEEDED is not a legal edge
    except InvalidWorkflowTransition as exc:
        return True, True, f"refused: {str(exc)[:70]}"
    except Exception as exc:
        return True, True, f"refused ({type(exc).__name__})"
    return True, False, "an illegal lifecycle transition was accepted"


def _alter_frozen_boundary() -> Tuple[bool, bool, str]:
    """Present a boundary set with a twelfth member and see if it is noticed."""
    from tools import derived_views as views
    with tempfile.TemporaryDirectory() as tmp:
        fake = Path(tmp) / "native_core" / "core"
        fake.mkdir(parents=True)
        for name in views._boundaries(REPO_ROOT):
            (fake / name).mkdir()
        (fake / "twelfth").mkdir()
        measured = views._boundaries(Path(tmp))
        if len(measured) != 11:
            return True, True, (
                f"boundary count detector reports {len(measured)}, not 11 — "
                "a twelfth subsystem is visible to measurement")
        return True, False, "a twelfth boundary was not visible to measurement"


def _forge_decision() -> Tuple[bool, bool, str]:
    """Plant a document asserting a certification that no Founder issued."""
    from tools import p12_certified_evidence_guard as sentinel
    with tempfile.TemporaryDirectory() as tmp:
        acts = Path(tmp)
        (acts / "forged.md").write_text(
            "PHASE 42 — FABRICATED ECOSYSTEM IS CERTIFIED.", encoding="utf-8")
        phases = sentinel.certified_phases(acts)
        if 42 in phases:
            return True, False, (
                "a planted certification statement was accepted; the guard reads "
                "bodies and cannot distinguish an issued instrument from a forged one")
        return True, True, "forged certification statement rejected"


def _duplicate_delegation() -> Tuple[bool, bool, str]:
    """Two ACTIVE grants conveying one capability to one recipient instance.

    `reconcile` is pure with respect to disk when both inputs are supplied, so
    the mutation is applied to the inputs themselves rather than to a synthetic
    directory the loaders would read differently from the real one.

    Two shapes are attempted, because they are not the same mutation and the
    system does not treat them the same way. The first — one grant projected
    twice — is a duplicated *representation*. The second — two independent
    grants of the same capability to the same recipient — is a duplicated
    *delegation*, which is what `§50` names. The first is exercised here as the
    control: it proves the detector under test can fire at all, so a null result
    on the second cannot be read as the suite failing to run.
    """
    from tools.delegation_reconciliation import (
        ACTIVE, LedgerGrant, Projection, reconcile)

    def grant(key: str) -> LedgerGrant:
        return LedgerGrant(
            delegation_id=key, lifecycle=ACTIVE,
            recipient_instance="mutation-probe-instance-001",
            capability_scope=("probe",), authority_instrument="FD-P11-001",
            authority_record=AUTHORIZING_RECORD,
            accountable_party="mutation-verification", source="synthetic")

    def projection(key: str, grant_id: str) -> Projection:
        return Projection(key=key, record=f"{key}.md", grant_id=grant_id,
                          role="CURRENT", authorized_scope="probe",
                          delegated_actor="mutation-probe-instance-001")

    control = reconcile([projection("w3-a", "g1"), projection("w3-b", "g1")],
                        {"g1": grant("g1")})["defects"]
    if not any(kind == "duplicate-representation" for kind, _, _ in control):
        return True, False, (
            "the control did not fire: duplicated representation of one grant "
            "was not reported, so this probe cannot distinguish a missing "
            "detector from a suite that is not running")

    defects = reconcile([projection("w3-a", "g1"), projection("w3-b", "g2")],
                        {"g1": grant("g1"), "g2": grant("g2")})["defects"]
    if defects:
        return True, True, f"detected: {defects[0][0]}"
    return True, False, (
        "two ACTIVE grants of one capability to one recipient produced no "
        "defect; duplicated representation is detected, duplicated delegation "
        "is not")


def _alter_provenance() -> Tuple[bool, bool, str]:
    """A representation whose delegated actor contradicts the grant it names.

    The mutation is applied to `reconcile`'s inputs and the function is run. An
    earlier version of this probe checked only that `'provenance-mismatch'` was
    a declared defect kind and reported a detection — which is `§48` exactly:
    the detector existed, the relationship between detector and mutation was
    never established. That version is replaced, and the replacement is
    recorded here rather than quietly substituted.
    """
    from tools.delegation_reconciliation import (
        ACTIVE, LedgerGrant, Projection, reconcile)

    grant = LedgerGrant(
        delegation_id="g1", lifecycle=ACTIVE,
        recipient_instance="mutation-probe-instance-001",
        capability_scope=("probe",), authority_instrument="FD-P11-001",
        authority_record=AUTHORIZING_RECORD,
        accountable_party="mutation-verification", source="synthetic")
    faithful = Projection(key="w3-a", record="a.md", grant_id="g1",
                          role="CURRENT", authorized_scope="probe",
                          delegated_actor="mutation-probe-instance-001")

    control = reconcile([faithful], {"g1": grant})["defects"]
    if any(kind == "provenance-mismatch" for kind, _, _ in control):
        return True, False, (
            "the control is unsound: an unmutated projection already reports "
            "provenance-mismatch, so a detection here would prove nothing")

    mutated = Projection(key="w3-a", record="a.md", grant_id="g1",
                         role="CURRENT", authorized_scope="probe",
                         delegated_actor="some-other-instance-002")
    defects = reconcile([mutated], {"g1": grant})["defects"]
    if any(kind == "provenance-mismatch" for kind, _, _ in defects):
        return True, True, (
            "refused: a projection naming an actor other than the grant's "
            "recipient is reported as provenance-mismatch")
    return True, False, (
        "a projection contradicting the grant it names produced no "
        f"provenance-mismatch; defects were {[k for k, _, _ in defects]}")


def _change_owner() -> Tuple[bool, bool, str]:
    """Change a capability record's stated Owner in a copied organization tree.

    Nothing resident is touched: the whole tree is copied and the mutation is
    applied to the copy. The independent authority the mutated statement is
    compared against is the record's **nesting** — which Department directory
    holds it — so the detector is not reading the same statement twice.
    """
    from tools import organization_catalog as org

    if not org.ORGANIZATION_ROOT.is_dir():
        return False, False, "no resident organization tree to copy"

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "organization"
        shutil.copytree(org.ORGANIZATION_ROOT, root)

        baseline = org.report(root=root)["inv1_disputed"]
        if baseline:
            return True, False, (
                "the control is unsound: the unmutated copy already reports "
                f"{len(baseline)} owner disagreement(s)")

        target = None
        for record in org.read_departments(root):
            for key in record.capabilities:
                path = root / record.key / "capabilities" / f"{key}.md"
                if path.is_file() and org.OWNER_SECTION.search(
                        path.read_text(encoding="utf-8")):
                    target = (record.key, key, path)
                    break
            if target:
                break
        if target is None:
            return False, False, (
                "no capability record with an Owner section to mutate")

        department, capability, path = target
        text = path.read_text(encoding="utf-8")
        stated = org.OWNER_SECTION.search(text).group(1).strip()
        forged = ("Knowledge Department" if "Knowledge" not in stated
                  else "Runtime Department")
        path.write_text(text.replace(stated, forged, 1), encoding="utf-8")

        disputed = org.report(root=root)["inv1_disputed"]
        if any(entry[0] == capability for entry in disputed):
            return True, True, (
                f"refused: {capability} declaring {forged!r} while nested under "
                f"{department!r} is reported as a disputed owner")
        return True, False, (
            f"{capability} was moved to {forged!r} and the catalog reported no "
            "disagreement")


def _alter_state_authority() -> Tuple[bool, bool, str]:
    """Two surfaces claiming authority over the same system-wide state.

    Reported as **not attempted**. `P12-W2` unified operational state is not
    built, so there is no surface on which two competing authority claims could
    be planted. Reporting this as attempted-and-missed would assert that a
    detector was exercised and stayed silent; nothing was exercised. The
    absence is the finding, and it is recorded as an absence.
    """
    import importlib
    for candidate in ("tools.p12_unified_state", "tools.p12_operational_state",
                      "tools.p12_state_authority"):
        try:
            importlib.import_module(candidate)
        except ImportError:
            continue
        return True, False, (
            f"{candidate} is resident but this probe does not know its "
            "authority model; the mutation was not applied")
    return False, False, (
        "P12-W2 unified operational state is not built: no state-authority "
        "surface exists to plant a competing claim on")


#: `§50`'s ten, in its order.
MUTATIONS: Tuple[Tuple[str, Callable], ...] = (
    ("remove authority", _remove_authority),
    ("alter provenance", _alter_provenance),
    ("change owner", _change_owner),
    ("inject stale state", _inject_stale_state),
    ("forge actor", _forge_actor),
    ("forge decision", _forge_decision),
    ("break workflow", _break_workflow),
    ("duplicate delegation", _duplicate_delegation),
    ("alter state authority", _alter_state_authority),
    ("change frozen boundary", _alter_frozen_boundary),
)


def verify() -> Tuple[MutationResult, ...]:
    results = []
    for name, attempt in MUTATIONS:
        try:
            attempted, detected, detail = attempt()
        except Exception as exc:  # pragma: no cover - defensive
            results.append(MutationResult(name, False, UNAVAILABLE,
                                          f"attempt raised: {exc}"))
            continue
        if not attempted:
            # A mutation that was never applied is not an undetected mutation.
            # Classifying it as MISSED would report a control as having stayed
            # silent when nothing was ever put in front of it — and a detection
            # claimed the same way is the defect this whole module exists to
            # refuse. UNAVAILABLE says what actually happened: no attempt.
            status = UNAVAILABLE
        else:
            status = DETECTED if detected else MISSED
        results.append(MutationResult(name, attempted, status, detail))
    return tuple(results)


def summary() -> dict:
    results = verify()
    return {
        "mutations": len(results),
        "attempted": sum(1 for r in results if r.attempted),
        "detected": sum(1 for r in results if r.status == DETECTED),
        "missed": sum(1 for r in results if r.status == MISSED),
        "unavailable": sum(1 for r in results if r.status == UNAVAILABLE),
        "missed_mutations": tuple(r.mutation for r in results if r.status == MISSED),
    }


def main(argv=None) -> int:
    for r in verify():
        mark = "attempted" if r.attempted else "NOT ATTEMPTED"
        print(f"{r.mutation:<24} {r.status:<12} {mark:<14} {r.detail[:66]}")
    print()
    print("summary:", summary())
    print()
    print("A MISSED result is a finding about the system, not a failure of this suite.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
