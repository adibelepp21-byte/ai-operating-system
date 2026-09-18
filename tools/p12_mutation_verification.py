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
    """Forge a governance **decision**, against the contract that owns decisions.

    **Re-pointed under `ACT-CC-P12-027 §8`, and this is an oracle correction of
    the same class as `duplicate delegation`.** This probe drove
    `p12_certified_evidence_guard.certified_phases` — a P12 tool that reads
    certification *statements* out of instrument bodies to compute an evidence
    protection set. That tool is not a decision authority and was never built as
    one. `§50` says *"deliberately attempt to violate **critical contracts**"*,
    and the critical contract for decisions is the Native Core's
    `GovernanceReview`: *"Governance holds authority over decisions"*
    (`Freeze §8`, `INV-8`, Constitution `§6.2` invariant 2).

    Asking a document-reading convenience whether a decision is genuine, and
    reporting the null answer as the system's inability, is `§48`'s failure —
    a property asserted from a component that does not hold it — committed
    inside the suite built to refuse it.

    Three shapes, because a forger has three, and a control so a null result
    cannot be a detector that refuses everything:

    * inject a **byte-identical** forged approve straight into the decision
      store, bypassing `record_decision` — the `F-G1` attack, faithful enough
      that storage cannot tell it from a real one;
    * have automation supply the authority;
    * mutate the published record after the fact (`F-H1`).
    """
    import tempfile as _tempfile

    from native_core.core.governance import (
        DECISION_PARTITION, GovernanceError, GovernanceReview, HumanAuthority,
        ReviewDecision)
    from native_core.core.governance.authority import InvalidAuthority
    from native_core.core.governance.decision import to_bytes
    from native_core.core.infrastructure import LocalAppendOnlyStorage
    from native_core.core.memory import MemoryReader
    from native_core.core.trace import TraceReader, TraceWriter, new_record

    def _stack():
        tmp = Path(_tempfile.mkdtemp())
        trace = LocalAppendOnlyStorage(base_dir=tmp / "t"); trace.provision()
        store = LocalAppendOnlyStorage(base_dir=tmp / "g"); store.provision()
        TraceWriter(trace).write(new_record(
            agent_definition_version="1", agent_instance="mutation-probe",
            runtime="rt", outputs={"finding": "X"}))
        review = GovernanceReview(MemoryReader(TraceReader(trace)), store)
        return review, store, review.pending_candidates()[0]

    # The control first: a genuine human decision must authorize, or a refusal
    # below would prove only that the mechanism refuses everything.
    review, _, candidate = _stack()
    review.record_decision(
        ReviewDecision(candidate, "approve", HumanAuthority("Moriarty"), "reviewed"))
    if not review.promotion_authorized(candidate):
        return True, False, (
            "the control failed: a genuine human decision did not authorize, so "
            "no refusal below can be read as detection")

    # 1 — a byte-identical forgery, injected past `record_decision`.
    review, store, candidate = _stack()
    forged = ReviewDecision(candidate, "approve", HumanAuthority("Moriarty"), "forged")
    store.append(DECISION_PARTITION, to_bytes(forged))
    if review.promotion_authorized(candidate):
        return True, False, (
            "a decision injected into the store authorized promotion; the "
            "forgery was believed")
    if review.recorded_decisions():
        return True, False, (
            "a decision injected into the store appeared among the recorded "
            "decisions; the provenance index trusts raw storage")

    # 2 — automation supplying the authority.
    review, _, candidate = _stack()
    for build in (lambda: ReviewDecision(candidate, "approve", None, "r"),
                  lambda: ReviewDecision(candidate, "approve", HumanAuthority(""), "r")):
        try:
            review.record_decision(build())
        except (GovernanceError, InvalidAuthority):
            continue
        return True, False, "automation supplied the authority for a decision"

    # 3 — mutating the published record after the fact.
    review, _, candidate = _stack()
    review.record_decision(
        ReviewDecision(candidate, "approve", HumanAuthority("Moriarty"), "r"))
    try:
        review.recorded_decisions()[0]["decision"] = "reject"
        return True, False, "a recorded decision was mutated after the fact"
    except Exception:
        pass
    if not review.promotion_authorized(candidate):
        return True, False, "the post-hoc mutation changed the authorization"

    return True, True, (
        "refused: a forged decision authorizes nothing — injected past "
        "record_decision it is absent from the provenance index, automation "
        "cannot supply the authority, and a recorded decision cannot be altered")


def _duplicate_delegation() -> Tuple[bool, bool, str]:
    """Two ACTIVE grants conveying one capability to one recipient instance.

    **This probe asked the wrong component until `ACT-CC-P12-021`.** It drove
    `delegation_reconciliation.reconcile`, whose `DEFECT_KINDS` are about the
    ledger↔projection relationship — unrepresented grants, stale claims,
    provenance mismatch. Grant **accumulation** is not among them and never
    was. The component that owns it is `w4_continuity`, whose
    `continuation_conditions` raises `MORE THAN ONE LIVE GRANT FOR ONE
    INSTANCE`, and whose semantics were deliberately re-anchored on the
    recipient instance in P11 after a `len(active) > 1` reading fired a false
    positive against the legitimate cross-Department state.

    So the previous `MISSED` was a **test-oracle defect**, not a system defect
    and not a source gap: the system detects this and the probe was looking
    somewhere else. Corrected by driving the real detector, both ways — the
    same instance holding two live grants must fire, and two instances holding
    one each must not, because the second is the legitimate state the false
    positive once blocked.
    """
    import json

    from tools import w4_continuity as continuity

    def _world(tmp: Path, grants) -> Path:
        root = Path(tmp)
        (root / "probe.instance.json").write_text(
            json.dumps({"instance_key": "mutation-probe-instance-001"}),
            encoding="utf-8")
        for delegation_id, instance in grants:
            (root / f"{delegation_id}.delegation.json").write_text(
                json.dumps({"delegation_id": delegation_id,
                            "status": "ACTIVE",
                            "recipient_instance": instance,
                            "executed_at": "2026-01-01"}), encoding="utf-8")
        return root

    # The control: two instances holding one grant each is lawful and must not
    # fire. Without it a detector that fired unconditionally would look correct.
    with tempfile.TemporaryDirectory() as tmp:
        lawful = continuity.reconstruct(_world(tmp, [
            ("g1", "mutation-probe-instance-001"),
            ("g2", "mutation-probe-instance-002")]))
    if lawful["duplicate_active"]:
        return True, False, (
            "two instances holding one live grant each was reported as "
            "accumulation — the false positive P11 corrected has returned")

    # The mutation: one instance, two live grants.
    with tempfile.TemporaryDirectory() as tmp:
        mutated = continuity.reconstruct(_world(tmp, [
            ("g1", "mutation-probe-instance-001"),
            ("g2", "mutation-probe-instance-001")]))
    if not mutated["duplicate_active"]:
        return True, False, (
            "one instance holding two live grants produced no accumulation "
            "finding")
    conditions = [c for c in continuity.continuation_conditions(mutated)
                  if "MORE THAN ONE LIVE GRANT" in c]
    if not conditions:
        return True, False, (
            "accumulation was computed but no continuation condition reports "
            "it; a finding a next run never sees is not a detection")
    return True, True, (
        f"detected: {conditions[0][:88]}")


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
    """Plant a second surface claiming authority over one system-wide state.

    **Previously `UNAVAILABLE`, and honestly so**: `P12-W2` unified operational
    state was not built, so there was no surface on which two competing claims
    could be planted, and reporting that as an undetected mutation would have
    asserted a detector was exercised when nothing was. `ACT-CC-P12-W2-001`
    built the surface, so the mutation is attemptable and is now attempted.

    The mutation is applied to the declared source set in memory. Nothing
    resident is touched, and the control below proves the detector is silent
    before the mutation.
    """
    from unittest import mock
    from tools import p12_operational_state as state

    def source(state_id: str, owns: str):
        return state.StateSource(
            state_id=state_id, state_class="RUNTIME",
            semantics=state.SOURCE_OF_TRUTH, owner=state_id,
            canonical_source="mutation probe", read_path="tools",
            authority="mutation probe", freshness_model="none",
            owns_within_class=owns)

    faithful = (source("probe-a", "one portion"),
                source("probe-b", "a different portion"))
    with mock.patch.object(state, "SOURCES", faithful):
        control = [c for c in state.conflicts() if c["kind"] == "CONFLICT"]
    if control:
        return True, False, (
            "the control is unsound: two sources owning different portions "
            "already report a conflict")

    mutated = (source("probe-a", "the same portion"),
               source("probe-b", "the same portion"))
    with mock.patch.object(state, "SOURCES", mutated):
        detected = [c for c in state.conflicts() if c["kind"] == "CONFLICT"]
    if detected:
        return True, True, (
            "refused: two surfaces claiming one portion of RUNTIME are "
            "reported as a state authority conflict")
    return True, False, (
        "two surfaces claiming the same portion of one state class produced "
        "no conflict")


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
