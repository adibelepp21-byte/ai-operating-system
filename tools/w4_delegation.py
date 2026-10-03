"""`P11-W4` — the Delegation authorized by `FD-P11-001`.

`§9`: *"Every W4 Delegation must have explicit provenance to FD-P11-001 and the
applicable authority chain."* The valid model is

    FOUNDER → FD-P11-001 → AUTHORIZED W4 DELEGATOR
            → AUTHORIZED AGENT INSTANCE → BOUNDED DELEGATION → W4 EXECUTION

and `§9` names the invalid one explicitly: `DP-01 → somehow create Delegation`.
`§10`: **`DP-01 ≠ SPECIFIC W4 DELEGATION`.**

**Why this is separate from `tools/delegation_catalog.py`.** That module is W3 —
the *organizational* delegation relation between units, read from resident
records, whose population is legitimately `0` because no unit-level delegator
exists. This is the **W4 operational** delegation from the authorized delegator
to a registered Agent Instance, which `FD-P11-001 §20` distinguishes: W3 *"may
represent and track the Delegation authorized by FD-P11-001, but W3
implementation must not manufacture authority absent valid provenance."* The two
are different relations at different levels; collapsing them would let a W4
operational grant appear as a unit-to-unit organizational delegation nobody
issued.

**`DELEGATION ≠ AUTHORITY CREATION`** (`§16`), stated formally in the Decision:

    Delegated Authority ≤ Available Delegator Authority
                        ∩ FD-P11-001 Scope
                        ∩ Canonical Boundaries

That inequality is enforced here as an intersection, not a promise: the granted
capability surface is checked against the instance's permitted surface, and a
grant exceeding it fails closed.

**`§14` — no self-authorization.** The delegator is not whoever calls this
module. It is the party `FD-P11-001 §4.1` names, and a delegation citing any
other delegator is refused. The Decision forbids the pattern where Claude
*"creates itself as delegator"*; the delegator is therefore a constant read from
the Decision, not a parameter a caller supplies freely.

**`§12.12` — no approving one's own delegation.** An instance may not be its own
accountable party, and `§17` forbids an instance authorizing another
(`NC-W4-17`, `NC-W4-18`).
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple

from tools.agent_instance_registry import (
    AgentInstanceRegistry,
    InstanceRegistration,
    REGISTERED,
)
from tools import authority_citation
from tools.planning import AuthorityProvenance

#: `§4.1`. The delegator is fixed by the Decision, not chosen by a caller.
#: `§5` explicitly rejects Engineering or Platform becoming the delegator by
#: virtue of being labels, so neither may be substituted here.
AUTHORIZED_DELEGATOR = "Claude Code / AIOS Co-Founder"

#: `§15`. Ultimate human governance accountability does not move.
ULTIMATE_ACCOUNTABILITY = "Founder"

AUTHORIZING_DECISION = "FD-P11-001"

#: `§13`'s thirteen elements, **plus one that is mine and is labelled as mine.**
#:
#: `§13` lists: `DELEGATION ID · DELEGATOR · RECIPIENT AGENT INSTANCE ·
#: AUTHORITY PROVENANCE · OBJECTIVE · CAPABILITY SCOPE · WORK SCOPE ·
#: TIME / LIFECYCLE BOUNDARY · RESOURCE BOUNDARY · OUTPUT EXPECTATION ·
#: VERIFICATION REQUIREMENT · ESCALATION CONDITION · ACCOUNTABLE PARTY` — and a
#: Delegation missing any of them *"is incomplete and must not become executable
#: W4 authority."* That is **thirteen**.
#:
#: ``termination_condition`` is the fourteenth and **`§13` does not list it.**
#: This comment previously said *"`§13`, verbatim"*, which was false, and
#: elsewhere I wrote that *"`§13` item 14 requires a termination condition"* —
#: a miscount of a thirteen-item list that then propagated into six documents.
#: The instrument contains no termination requirement at all; the word does not
#: appear in it.
#:
#: The field is **kept**, because `§29` makes a Delegation *"a controlled
#: lifecycle object rather than a permanent authority grant"* and a grant with
#: no stated ending is the unbounded authority `§11` forbids. Requiring more
#: than `§13` requires is sound; **claiming `§13` requires it was not.**
#: Corrected under `ACT-CC-P11-017`.
REQUIRED_ELEMENTS = (
    "delegation_id", "delegator", "recipient_instance", "authority_provenance",
    "objective", "capability_scope", "work_scope", "lifecycle_boundary",
    "resource_boundary", "output_expectation", "verification_requirement",
    "escalation_condition", "accountable_party", "termination_condition",
)

#: `§29`: a Delegation is *"a controlled lifecycle object rather than a
#: permanent authority grant."* A grant that cannot be withdrawn is exactly the
#: unrestricted authority `FD-P11-001 §11` forbids — so revocation is not an
#: optional convenience, it is what makes the grant bounded in time as well as
#: in scope.
ACTIVE, REVOKED = "ACTIVE", "REVOKED"


class DelegationError(RuntimeError):
    """Fail closed (`PR-4`). `§26`: missing any component means `BLOCKED`."""


@dataclass(frozen=True)
class W4Delegation:
    """A bounded, provenance-bearing grant to one registered Agent Instance."""

    delegation_id: str
    delegator: str
    recipient_instance: str
    authority: AuthorityProvenance
    objective: str
    capability_scope: Tuple[str, ...]
    work_scope: Tuple[str, ...]
    lifecycle_boundary: str
    resource_boundary: str
    output_expectation: str
    verification_requirement: str
    escalation_condition: str
    accountable_party: str
    termination_condition: str
    issued_at: str
    status: str = ACTIVE

    def is_executable(self) -> bool:
        """Whether this grant may still be acted on. **Not a permission check
        for anything else** — a revoked delegation authorizes nothing, and an
        active one authorizes only what its scope names."""
        return self.status == ACTIVE

    def authority_chain(self) -> Tuple[str, ...]:
        """`§24`'s required trace, bottom-up. Evidence, not permission."""
        return (f"delegation:{self.delegation_id}",
                f"delegator:{self.delegator}",
                f"decision:{self.authority.instrument}",
                f"founder:{ULTIMATE_ACCOUNTABILITY}")

    def permits(self, capability: str) -> bool:
        """Whether this grant covers a capability. **Not an authorization check
        for anything else** — it answers only what this delegation says."""
        return capability in self.capability_scope

    def to_payload(self) -> dict:
        return {
            "delegation_id": self.delegation_id, "delegator": self.delegator,
            "recipient_instance": self.recipient_instance,
            "authority_instrument": self.authority.instrument,
            "authority_record": self.authority.record,
            "objective": self.objective,
            "capability_scope": list(self.capability_scope),
            "work_scope": list(self.work_scope),
            "lifecycle_boundary": self.lifecycle_boundary,
            "resource_boundary": self.resource_boundary,
            "output_expectation": self.output_expectation,
            "verification_requirement": self.verification_requirement,
            "escalation_condition": self.escalation_condition,
            "accountable_party": self.accountable_party,
            "termination_condition": self.termination_condition,
            "status": self.status,
            "issued_at": self.issued_at,
            "authority_chain": list(self.authority_chain()),
        }


class W4DelegationRegistry:
    """Issues delegations. Holds no authority of its own."""

    def __init__(self, registry: AgentInstanceRegistry,
                 root: Optional[Path] = None):
        self._instances = registry
        self._root = root
        if root is not None:
            root.mkdir(parents=True, exist_ok=True)
        self._issued: Dict[str, W4Delegation] = {}

    def issue(self, *, delegator: str, recipient_instance: str,
              authority: AuthorityProvenance, objective: str,
              capability_scope: Tuple[str, ...], work_scope: Tuple[str, ...],
              lifecycle_boundary: str, resource_boundary: str,
              output_expectation: str, verification_requirement: str,
              escalation_condition: str, accountable_party: str,
              termination_condition: str) -> W4Delegation:
        """Issue one bounded delegation. Every `§13` element is required."""
        # `§14`: the delegator is the one the Decision names.
        if delegator != AUTHORIZED_DELEGATOR:
            raise DelegationError(
                f"{delegator!r} is not the authorized W4 delegator — "
                f"`FD-P11-001 §4.1` names {AUTHORIZED_DELEGATOR!r}, and `§5` "
                "rejects Engineering or Platform becoming delegator by label")

        # `§24`: provenance to this Decision specifically.
        if not isinstance(authority, AuthorityProvenance):
            raise DelegationError("a delegation requires a validated citation")
        if AUTHORIZING_DECISION not in authority.instrument:
            raise DelegationError(
                f"a W4 delegation must cite {AUTHORIZING_DECISION}; "
                f"{authority.instrument!r} is insufficient — `§9`: "
                "'DP-01 → somehow create Delegation' is invalid")
        # `§24`: the chain must actually reach the Decision. A citation that
        # names it but points elsewhere produces no chain (`GOAL-V2-005`).
        unreached = authority_citation.refusal(
            authority.instrument, authority.record, AUTHORIZING_DECISION)
        if unreached:
            raise DelegationError(
                f"`§24` provenance does not reach {AUTHORIZING_DECISION}: "
                f"{unreached}")

        # `§6.1`: only a registered instance may receive.
        if not self._instances.is_registered(recipient_instance):
            raise DelegationError(
                f"{recipient_instance!r} is not a registered Agent Instance — "
                "`§6.1`: an Agent Definition alone is insufficient")
        registration: InstanceRegistration = self._instances.get(
            recipient_instance)
        if registration.lifecycle != REGISTERED:
            raise DelegationError(
                f"instance {recipient_instance!r} is {registration.lifecycle}; "
                "a delegation may only be issued to a live instance")

        # `§16`: delegated ≤ available. Enforced as an intersection.
        scope = tuple(capability_scope or ())
        if not scope:
            raise DelegationError("a delegation requires a capability scope")
        beyond = [c for c in scope
                  if c not in registration.permitted_capabilities]
        if beyond:
            raise DelegationError(
                f"delegation exceeds the instance's permitted surface: {beyond} "
                "— `§16`: a delegator may not grant more authority than the "
                "recipient may hold")

        # `§12.12` / `§15`: accountability is real and is not the recipient.
        if accountable_party == recipient_instance:
            raise DelegationError(
                "the recipient cannot be its own accountable party — "
                "`§15` fixes instance → delegator → Founder, and `§12` forbids "
                "approving one's own delegation")

        values = dict(
            delegation_id=uuid.uuid4().hex[:16], delegator=delegator,
            recipient_instance=recipient_instance,
            authority_provenance=authority, objective=objective,
            capability_scope=scope, work_scope=tuple(work_scope or ()),
            lifecycle_boundary=lifecycle_boundary,
            resource_boundary=resource_boundary,
            output_expectation=output_expectation,
            verification_requirement=verification_requirement,
            escalation_condition=escalation_condition,
            accountable_party=accountable_party,
            termination_condition=termination_condition,
        )
        missing = [name for name in REQUIRED_ELEMENTS
                   if not values.get(name)]
        if missing:
            raise DelegationError(
                f"delegation is incomplete, missing {missing} — `§13`: it "
                "'must not become executable W4 authority'")

        delegation = W4Delegation(
            delegation_id=values["delegation_id"], delegator=delegator,
            recipient_instance=recipient_instance, authority=authority,
            objective=objective, capability_scope=scope,
            work_scope=values["work_scope"],
            lifecycle_boundary=lifecycle_boundary,
            resource_boundary=resource_boundary,
            output_expectation=output_expectation,
            verification_requirement=verification_requirement,
            escalation_condition=escalation_condition,
            accountable_party=accountable_party,
            termination_condition=termination_condition,
            issued_at=datetime.now(timezone.utc).isoformat())
        target = None
        if self._root is not None:
            # Certified evidence is never written: refused before anything is
            # recorded, in memory or on disk (P12-F12; surfaced by FD-CG7-001).
            from tools.p12_certified_evidence_guard import guard
            target = guard(self._root / f"{delegation.delegation_id}.delegation.json")
        self._issued[delegation.delegation_id] = delegation
        if target is not None:
            guard(target).write_text(json.dumps(delegation.to_payload(), indent=2),
                                     encoding="utf-8")
        return delegation

    def revoke(self, delegation_id: str, *, reason: str) -> W4Delegation:
        """Withdraw a grant. `§29`: `INVALID / REVOKED → NOT EXECUTABLE`.

        Replaces the record with a revoked successor rather than editing it, so
        the terms that were in force remain readable — the same append-only
        discipline the escalation register and the plan chain both follow.

        Revocation is an act of the **delegator**, and it removes authority
        rather than granting any, so it needs no new provenance: nothing can be
        done with a revoked delegation that could not be done with none at all.
        """
        current = self.get(delegation_id)
        if not reason or not reason.strip():
            raise DelegationError("revocation must record why the grant ended")
        revoked = W4Delegation(
            **{**{f: getattr(current, f) for f in current.__dataclass_fields__},
               "status": REVOKED})
        target = None
        if self._root is not None:
            from tools.p12_certified_evidence_guard import guard
            target = guard(self._root / f"{delegation_id}.delegation.json")
        self._issued[delegation_id] = revoked
        if target is not None:
            payload = revoked.to_payload()
            payload["revocation_reason"] = reason
            guard(target).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return revoked

    def get(self, delegation_id: str) -> W4Delegation:
        if delegation_id not in self._issued:
            raise DelegationError(f"no such delegation: {delegation_id!r}")
        return self._issued[delegation_id]

    def for_instance(self, instance_key: str) -> Tuple[W4Delegation, ...]:
        return tuple(d for d in self._issued.values()
                     if d.recipient_instance == instance_key)

    def keys(self) -> Tuple[str, ...]:
        return tuple(sorted(self._issued))


# ---- operational disposition (FD-AGENCY-001 · S-1 · Q-S1-A = A2) -------------
#
# The ledger above writes a grant's **historical status** — `ACTIVE` or
# `REVOKED` — into the delegation record itself. When that record lies in a
# certified evidence root, the status can never move again: the P11 ledger was
# certified by `FD-P11-002`, and `P12-F12` refuses every rewrite. Four grants
# there finished their work and still read `ACTIVE` (S-1, Register `§135`).
#
# The Founder's A2 decision keeps those records as immutable history and allows
# a **live operational ledger outside the certified boundary**. This is that
# ledger, and it is deliberately small:
#
# * it adds **one record per grant**, append-only, beside nothing it describes;
# * it never edits, deletes or reinterprets a delegation record. The historical
#   status stays what the record says; the disposition is a second, separate fact;
# * it accepts a disposition only over a historically `ACTIVE` grant, so a
#   `REVOKED` record is never re-read as anything else;
# * it is bound to the exact bytes of the delegation record (and, for
#   `COMPLETED`, of the evidence) it was recorded against. A reader that finds
#   those bytes changed reports a fault and does not honour it;
# * only the authorized delegator records one (`FD-P11-001 §4.1`). The accountable
#   party does not move.
#
# Semantics (documented in `docs/architecture/agency/W4-OPERATIONAL-LEDGER.md`):
#
#   COMPLETED  the grant's own termination condition "on completion of the bound
#              plan" is met, **computed here from the evidence**, never asserted
#              by a caller: the bound plan's evidence names the grant, every
#              outcome is `success`, no escalation was raised, and every step in
#              the work scope succeeded.
#   REVOKED    the delegator withdrew the grant (`§29` revocation), for a grant
#              whose record cannot be rewritten in place.

COMPLETED = "COMPLETED"
DISPOSITIONS = (COMPLETED, REVOKED)
_REPO_ROOT = Path(__file__).resolve().parent.parent
#: The live operational ledger. It must never lie inside a certified root; the
#: write is guarded, and the reader reports a fault if it ever does.
LIVE_LEDGER = _REPO_ROOT / "docs/architecture/agency/operations/w4-dispositions"
DISPOSITION_AUTHORITY = (
    "FD-AGENCY-001 S-1 Q-S1-A (A2)",
    "docs/governance/acts/FD-AGENCY-001-S1-TERMINAL-STATE-DECISION.md")
_COMPLETION_CLAUSE = "completion of the bound plan"

# ---- P12 extension (FD-CG7-001, Register `§145`) ------------------------------
#
# The Founder extended A2 to P12 for exactly the grants CG-7 identified, with
# exactly one disposition each: FQ-CG7-1 the nine historical proof-run grants,
# FQ-CG7-2 the live grant whose escalation the Founder answered. A disposition
# names the instrument it was recorded under, and each instrument reaches only
# what its text reaches. A2 itself is unchanged (no scope was recorded for it,
# and none is added here).
FD_CG7_RECORD = "docs/governance/acts/FD-CG7-001-P12-OPERATIONAL-STATE-DISPOSITION-DECISION.md"
FD_P11_001_RECORD = "docs/governance/acts/FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md"
_P12_W4 = "docs/architecture/p12/w4-operations"
DISPOSITION_SCOPES: Dict[Tuple[str, str], Optional[dict]] = {
    DISPOSITION_AUTHORITY: None,
    ("FD-CG7-001 FQ-CG7-1", FD_CG7_RECORD): {
        "root": _P12_W4, "dispositions": (REVOKED,),
        "grants": ("08e14bd7aa584ea5", "332d42f021764ab6", "522e84af52444890",
                   "632b256f8335434f", "84e94ea2f001444d", "aa591daf55ca4714",
                   "b304c7ecb1024454", "e668a317fa494342", "e6a3d622cfb54b4f")},
    ("FD-CG7-001 FQ-CG7-2", FD_CG7_RECORD): {
        "root": _P12_W4, "dispositions": (REVOKED,), "grants": ("2494015de36246fd",)},
    # S-4: the delegator's own review of its own grants, in roots that are not
    # certified evidence. `FD-P11-001 §15.2` keeps Claude Code accountable, as
    # the authorized delegator, for "verification requirements"; Co-Founder V2
    # A09 / A11 authorize operational decisions and verification. Certified
    # roots stay reachable only through the Founder instruments above.
    ("FD-P11-001 §15.2", FD_P11_001_RECORD): {
        "uncertified_only": True, "dispositions": (COMPLETED, REVOKED)},
}


def _sha256(path: Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(_REPO_ROOT))
    except ValueError:
        return str(path.resolve())


# ---- ledger identity (FD-CG7-001 R-1) -----------------------------------------
#
# The S-1 ledgers filed each root's entries under ``Path(root).name``. Two roots
# with one basename — `p11/w4-operations` and `p12/w4-operations` — therefore
# shared a folder, and each root's reading met the other's entries as faults.
# A root's ledger identity is now its **full path** (repo-relative, or absolute
# outside the repository), so the same basename is never the same identity.
#
# Entries the S-1 ledgers already wrote under a basename folder stay where they
# are: they are append-only, cited by path, and each records its full ``root``.
# They are read from there and attributed by that recorded root, never by the
# folder; an entry recorded for another root is simply not this root's entry.


def ledger_identity(root: Path) -> str:
    """The unambiguous ledger identity of an operational root: its full path."""
    return _rel(Path(root)).lstrip("/")


def ledger_folder(ledger: Path, root: Path) -> Path:
    """Where the ledger files ``root``'s entries (R-1)."""
    return Path(ledger) / ledger_identity(root)


def legacy_ledger_folder(ledger: Path, root: Path) -> Optional[Path]:
    """The pre-R-1 basename folder, if it differs from the full-path folder."""
    legacy = Path(ledger) / Path(root).name
    return None if legacy == ledger_folder(ledger, root) else legacy


def _bound_plan(record: dict) -> Optional[str]:
    """The plan key in a lifecycle boundary of the form '... of plan <key>'."""
    match = re.search(r"\bplan\s+(\S+)\s*$", record.get("lifecycle_boundary", ""))
    return match.group(1) if match else None


def _names_grant(evidence: dict, delegation_id: str) -> bool:
    return (evidence.get("delegation_id") == delegation_id
            or delegation_id in (evidence.get("grants") or {}).values()
            or any(o.get("delegation") == delegation_id
                   for o in evidence.get("outcomes", [])))


def _names_completion(record: dict, plan: Optional[str]) -> bool:
    """Whether the termination condition is completion of the bound plan.

    R-4: P12 grants phrase the same clause with the plan named — *"on completion
    of plan <key>"* — where P11 says *"the bound plan"*. Both mean the plan in
    the lifecycle boundary; any other plan does not.
    """
    condition = record.get("termination_condition", "")
    return (_COMPLETION_CLAUSE in condition
            or (plan is not None and re.search(
                rf"\bcompletion of plan {re.escape(plan)}\b", condition) is not None))


def _manifest_matches(plan: Optional[str], gid: str, reasons: list) -> list:
    """R-4: P12 execution manifests (`tools.p12_execution_provenance`) naming the grant.

    The manifest is the P12 form of the same evidence: written at execution
    time, it names the plan, the grant, the work scope, the status and the
    outcome. Consulted only when the root holds no evidence record for the grant.
    """
    from tools.p12_execution_provenance import MANIFEST_ROOT
    matches = []
    for path in sorted(Path(MANIFEST_ROOT).glob("*.manifest.json")):
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            reasons.append(f"unreadable execution manifest {path.name}")
            continue
        if manifest.get("plan") == plan and manifest.get("delegation_id") == gid:
            matches.append((path, manifest))
    return matches


def plan_completion(root: Path, record: dict) -> Tuple[bool, Optional[Path], Tuple[str, ...]]:
    """Whether the grant's bound plan completed, from persisted evidence alone.

    Returns ``(met, evidence_path, reasons_not_met)``. Nothing is assumed: an
    absent, unreadable or ambiguous evidence record is a reason, not a pass.
    The evidence is the root's ``*.evidence.json`` (P11 form) or, when the root
    holds none for the grant, a P12 execution manifest (R-4).
    """
    reasons = []
    gid = record.get("delegation_id")
    plan = _bound_plan(record)
    if not _names_completion(record, plan):
        reasons.append("termination condition does not name completion of the bound plan")
    if plan is None:
        reasons.append("lifecycle boundary names no bound plan")
    matches = []
    for path in sorted(Path(root).glob("*.evidence.json")):
        try:
            evidence = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            reasons.append(f"unreadable evidence record {path.name}")
            continue
        if evidence.get("plan") == plan and _names_grant(evidence, gid):
            matches.append((path, evidence))
    if not matches:
        manifests = _manifest_matches(plan, gid, reasons)
        if len(manifests) == 1:
            return _manifest_completion(record, manifests[0], reasons)
        if manifests:
            reasons.append(f"{len(manifests)} execution manifests name plan {plan!r} "
                           f"and grant {gid!r}; exactly one is required")
            return False, None, tuple(reasons)
    if len(matches) != 1:
        reasons.append(f"{len(matches)} evidence records name plan {plan!r} and "
                       f"grant {gid!r}; exactly one is required")
        return False, None, tuple(reasons)
    path, evidence = matches[0]
    outcomes = evidence.get("outcomes", [])
    if not outcomes:
        reasons.append("the evidence records no outcome")
    bad = [(o["step"], o["status"]) for o in outcomes if o.get("status") != "success"]
    if bad:
        reasons.append(f"not every plan step succeeded: {bad}")
    if evidence.get("escalations"):
        reasons.append(f"the plan raised escalations {evidence['escalations']}")
    terminal = evidence.get("workflow_terminal_state")
    if terminal is not None and "SUCCEEDED" not in terminal:
        reasons.append("the workflow did not reach SUCCEEDED")
    done = {o["step"] for o in outcomes if o.get("status") == "success"}
    missing = [s for s in record.get("work_scope", []) if s not in done]
    if missing:
        reasons.append(f"work-scope steps without a success outcome: {missing}")
    return not reasons, path, tuple(reasons)


def _manifest_completion(record: dict, match, reasons: list
                         ) -> Tuple[bool, Optional[Path], Tuple[str, ...]]:
    """The same completion test, read from one P12 execution manifest (R-4)."""
    path, manifest = match
    if manifest.get("status") != "success":
        reasons.append(f"the execution status is {manifest.get('status')!r}, not 'success'")
    unsatisfied = (manifest.get("outcome") or {}).get("unsatisfied")
    if unsatisfied is None:
        reasons.append("the manifest records no outcome")
    elif unsatisfied:
        reasons.append(f"criteria unsatisfied: {unsatisfied}")
    missing = [s for s in record.get("work_scope", [])
               if s not in (manifest.get("work_scope") or [])]
    if missing:
        reasons.append(f"work-scope steps the manifest does not cover: {missing}")
    return not reasons, path, tuple(reasons)


def _disposition_path(ledger: Path, root: Path, delegation_id: str) -> Path:
    return ledger_folder(ledger, root) / f"{delegation_id}.disposition.json"


def _legacy_disposition(ledger: Path, root: Path, delegation_id: str) -> Optional[Path]:
    """A pre-R-1 entry for this grant **of this root**, if one exists."""
    folder = legacy_ledger_folder(ledger, root)
    path = None if folder is None else folder / f"{delegation_id}.disposition.json"
    if path is None or not path.is_file():
        return None
    try:
        item = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return path                     # unattributable: treated as present
    return path if item.get("root") == _rel(Path(root)) else None


def _scope_refusal(authority: Tuple[str, str], root: Path, delegation_id: str,
                   disposition: str) -> Optional[str]:
    """Why ``authority`` does not reach this disposition, or None if it does."""
    if authority not in DISPOSITION_SCOPES:
        return f"{authority[0]!r} is not an instrument under which a disposition is recorded"
    scope = DISPOSITION_SCOPES[authority]
    if scope is None:
        return None
    if scope.get("uncertified_only"):
        from tools.p12_certified_evidence_guard import is_protected
        if is_protected(Path(root)):
            return (f"{authority[0]} reaches only roots outside certified evidence; "
                    f"{_rel(Path(root))!r} is certified")
        if disposition not in scope["dispositions"]:
            return f"{authority[0]} authorizes {scope['dispositions']}, not {disposition!r}"
        return None
    if _rel(Path(root)) != scope["root"]:
        return f"{authority[0]} does not reach root {_rel(Path(root))!r}"
    if delegation_id not in scope["grants"]:
        return f"{authority[0]} does not reach grant {delegation_id!r}"
    if disposition not in scope["dispositions"]:
        return f"{authority[0]} authorizes {scope['dispositions']}, not {disposition!r}"
    return None


def record_disposition(root: Path, delegation_id: str, *, disposition: str,
                       delegator: str, reason: str,
                       ledger: Path = LIVE_LEDGER,
                       authority: Tuple[str, str] = DISPOSITION_AUTHORITY,
                       provenance: Optional[dict] = None) -> Path:
    """Record a grant's terminal operational disposition in the live ledger.

    The delegation record is read, never written. Refuses, rather than
    records, anything it cannot establish. ``authority`` is the Founder
    instrument the disposition is recorded under; it must be one of
    ``DISPOSITION_SCOPES`` and reach this root, grant and disposition.

    ``provenance`` (MR-S5-1) is the delegator's decision, made explicit:
    ``decision``, ``resulting_plan`` and ``rework_target``. It is validated
    before anything is written (`decision_fault`) and, for a decision on a
    result, binds the result's evidence. Records written without it remain
    valid legacy records.
    """
    from tools.p12_certified_evidence_guard import guard

    if disposition not in DISPOSITIONS:
        raise DelegationError(f"{disposition!r} is not a disposition {DISPOSITIONS}")
    if delegator != AUTHORIZED_DELEGATOR:
        raise DelegationError(
            f"only {AUTHORIZED_DELEGATOR!r} records a disposition (FD-P11-001 §4.1)")
    if not reason or not reason.strip():
        raise DelegationError("a disposition must record why the grant ended")
    refused = _scope_refusal(tuple(authority), root, delegation_id, disposition)
    if refused:
        raise DelegationError(refused)
    if DISPOSITION_SCOPES[tuple(authority)] is not None:
        cited = authority_citation.refusal(authority[0], authority[1],
                                           authority[0].split()[0])
        if cited:
            raise DelegationError(f"the disposition authority does not resolve: {cited}")
    source = Path(root) / f"{delegation_id}.delegation.json"
    if not source.is_file():
        raise DelegationError(f"no such delegation record: {source}")
    record = json.loads(source.read_text(encoding="utf-8"))
    if record.get("delegator") != delegator:
        raise DelegationError("the recording party is not the grant's delegator")
    if record.get("status") != ACTIVE:
        raise DelegationError(
            f"historical status is {record.get('status')!r}: a disposition is "
            "recorded only over an ACTIVE grant, never over a revoked one")
    evidence = None
    if provenance is not None:
        fault = decision_fault(provenance, disposition)
        if fault:
            raise DelegationError(f"malformed decision provenance: {fault}")
    if disposition == COMPLETED:
        met, evidence, reasons = plan_completion(root, record)
        if not met:
            raise DelegationError(
                "termination by completion is not established: " + "; ".join(reasons))
    elif provenance is not None:
        _, evidence, _ = plan_completion(root, record)   # the result decided on

    target = _disposition_path(ledger, root, delegation_id)
    guard(target)                       # before any directory is created
    if target.exists() or _legacy_disposition(ledger, root, delegation_id):
        raise DelegationError(
            f"{delegation_id} already has a disposition; the ledger is append-only")
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "delegation_id": delegation_id,
        "root": _rel(Path(root)),
        "disposition": disposition,
        "historical_status": record["status"],
        "record_sha256": _sha256(source),
        "evidence": None if evidence is None else _rel(evidence),
        "evidence_sha256": None if evidence is None else _sha256(evidence),
        "reason": reason,
        "recorded_by": delegator,
        "accountable_party": record.get("accountable_party"),
        "authority_instrument": authority[0],
        "authority_record": authority[1],
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    if provenance is not None:
        payload.update({key: provenance.get(key) for key in PROVENANCE_FIELDS})
    guard(target).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return target


def read_dispositions(root: Path, ledger: Path = LIVE_LEDGER
                      ) -> Tuple[Dict[str, dict], Tuple[str, ...]]:
    """The dispositions the live ledger holds for ``root``, and the faults.

    A disposition is honoured only if everything it was recorded against still
    holds; otherwise it is a fault and the grant keeps its historical status.
    Entries are read from the root's full-path folder and, for entries written
    before R-1, from its basename folder, where only entries recorded for this
    root are this root's.
    """
    from tools.p12_certified_evidence_guard import is_protected

    valid: Dict[str, dict] = {}
    faults = []
    here = _rel(Path(root))
    folders = [(ledger_folder(ledger, root), False)]
    legacy = legacy_ledger_folder(ledger, root)
    if legacy is not None:
        folders.append((legacy, True))
    for folder, is_legacy in folders:
        if not folder.is_dir():
            continue
        if is_protected(folder):
            faults.append(f"live ledger {folder} lies inside a certified root; "
                          "no disposition there is honoured")
            continue
        for path in sorted(folder.glob("*.disposition.json")):
            try:
                item = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                faults.append(f"{path.name}: unreadable")
                continue
            if is_legacy and item.get("root") != here:
                continue                # another root's entry: not this root's (R-1)
            gid = item.get("delegation_id")
            source = Path(root) / f"{gid}.delegation.json"
            problems = []
            if item.get("disposition") not in DISPOSITIONS:
                problems.append(f"unknown disposition {item.get('disposition')!r}")
            if item.get("root") != here:
                problems.append(f"recorded for root {item.get('root')!r}")
            if not source.is_file():
                problems.append("its delegation record is missing")
            elif _sha256(source) != item.get("record_sha256"):
                problems.append("its delegation record changed since it was recorded")
            elif json.loads(source.read_text(encoding="utf-8")).get("status") != ACTIVE:
                problems.append("its delegation record is not historically ACTIVE")
            if item.get("recorded_by") != AUTHORIZED_DELEGATOR:
                problems.append("not recorded by the authorized delegator")
            scoped = _scope_refusal((item.get("authority_instrument"), item.get("authority_record")),
                                    root, gid, item.get("disposition"))
            if scoped:
                problems.append(scoped)
            if item.get("disposition") == COMPLETED or item.get("evidence"):
                evidence = _REPO_ROOT / (item.get("evidence") or "")
                if not item.get("evidence") or not evidence.is_file():
                    problems.append("its evidence record is missing")
                elif _sha256(evidence) != item.get("evidence_sha256"):
                    problems.append("its evidence record changed since it was recorded")
            if any(key in item for key in PROVENANCE_FIELDS):
                fault = decision_fault(item, item.get("disposition"))
                if fault:
                    problems.append(f"decision provenance: {fault}")
            if path.name != f"{gid}.disposition.json":
                problems.append("file name does not match its delegation id")
            if gid in valid:
                problems.append("a second disposition for the same grant")
            if problems:
                faults.append(f"{path.name}: " + "; ".join(problems))
            else:
                valid[gid] = item
    return valid, tuple(faults)


# ---- plan → delegation (FD-AGENCY-001 · S-2) ---------------------------------
#
# Planning identifies work that needs delegating (`PlanningSurface.
# delegation_requirements`) and, by design, can never turn it into a
# delegation: its `DelegationRequirement` has no delegator field, and
# `ACT-CC-P11-005 §11` forbids converting a plan into a delegation record. The
# conversion therefore belongs to the **delegator**, here, and to no one else.
#
# This is the only new code S-2 needs. It adds no authority, contract field,
# state or provenance store:
#
# * the requirement is re-derived from the surface, so it is genuine and its
#   plan is current (a superseded plan, or a step Planning did not mark for
#   delegation, yields nothing to issue);
# * everything that carries provenance is fixed from the requirement and cannot
#   be supplied by the caller: objective = the step statement; work scope =
#   exactly that one step; lifecycle boundary = "one execution of plan <key>",
#   the convention every W4 grant already uses (parsed by `_bound_plan`);
# * accountability and termination are fixed (`FD-P11-001 §15`; the S-1
#   completion semantics);
# * issuance itself is `W4DelegationRegistry.issue`, unchanged: the delegator,
#   the FD-P11-001 citation, the registered recipient and the capability bound
#   are all enforced there.

TERMINATION_ON_PLAN = "on completion of the bound plan, or revocation"


def issue_from_plan(delegations: W4DelegationRegistry, surface, plan, step_key: str,
                    *, delegator: str, recipient_instance: str,
                    authority: AuthorityProvenance, capability_scope: Tuple[str, ...],
                    resource_boundary: str, output_expectation: str,
                    verification_requirement: str,
                    escalation_condition: str) -> W4Delegation:
    """The delegator issues one bounded grant for one step a plan marked.

    Planning delegates nothing; this is the delegator acting on what Planning
    identified. The caller cannot widen the work, rename the plan or move
    accountability.
    """
    if delegator != AUTHORIZED_DELEGATOR:
        raise DelegationError(
            f"{delegator!r} is not the authorized W4 delegator (FD-P11-001 §4.1); "
            "a plan does not make anyone a delegator")
    requirements = {r.step_key: r for r in surface.delegation_requirements(plan)}
    if step_key not in requirements:
        raise DelegationError(
            f"plan {plan.key!r} does not mark step {step_key!r} as requiring "
            "delegation; only work Planning identified may be delegated from it")
    requirement = requirements[step_key]
    return delegations.issue(
        delegator=delegator, recipient_instance=recipient_instance,
        authority=authority, objective=requirement.scope_described,
        capability_scope=tuple(capability_scope),
        work_scope=(requirement.step_key,),
        lifecycle_boundary=f"one execution of plan {requirement.plan_key}",
        resource_boundary=resource_boundary,
        output_expectation=output_expectation,
        verification_requirement=verification_requirement,
        escalation_condition=escalation_condition,
        accountable_party=delegator,
        termination_condition=TERMINATION_ON_PLAN)


def plan_provenance(record: dict, surface) -> dict:
    """Trace a persisted grant back to the plan step it was issued for.

    Reads only existing fields: the lifecycle boundary names the plan, the work
    scope names the step. Returns what was found and every mismatch; it does not
    decide anything.
    """
    plan_key = _bound_plan(record)
    found = {"plan": plan_key, "step": None, "faults": []}
    scope = record.get("work_scope", [])
    if plan_key is None:
        found["faults"].append("the lifecycle boundary names no plan")
        return found
    plans = [p for goal in surface._goals for p in surface.history(goal)  # noqa: SLF001
             if p.key == plan_key]
    if len(plans) != 1:
        found["faults"].append(f"{len(plans)} plans named {plan_key!r} on the surface")
        return found
    plan = plans[0]
    goal = surface.goal(plan.goal_key)
    founder = authority_citation.founder_goal_refusal(
        goal.authority.instrument, goal.authority.record, goal.statement)
    found.update(goal=plan.goal_key, plan_authority=plan.authority.cited(),
                 plan_current=not surface.is_superseded(plan),
                 goal_statement=goal.statement, goal_authority=goal.authority.cited(),
                 # S-3: whether the goal is a verbatim, registered Founder Goal.
                 # Reported, not required: a goal may legitimately rest on other
                 # authority, and saying which is the reader's job.
                 founder_goal="VERIFIED" if founder is None else f"NOT VERIFIED: {founder}")
    if len(scope) != 1:
        found["faults"].append(f"work scope {scope} is not exactly one plan step")
        return found
    step = next((s for s in plan.steps if s.key == scope[0]), None)
    if step is None:
        found["faults"].append(f"step {scope[0]!r} is not in plan {plan_key!r}")
        return found
    found["step"] = step.key
    if not step.requires_delegation:
        found["faults"].append(f"step {step.key!r} is not marked for delegation")
    if record.get("objective") != step.statement:
        found["faults"].append("the objective is not the step statement")
    return found


# ---- result → CEO decision → plan outcome (FD-AGENCY-001 · S-4, MR-S5-1) ------
#
# What already existed, and what S-4 connects:
#
# * the agent's result is an `ExecutionOutcome` (`success` / `failure` /
#   `escalation`), persisted in an evidence record beside the grant;
# * verification against the grant is `plan_completion`: the bound plan's
#   evidence names the grant, every outcome succeeded, nothing escalated, and
#   the work scope is covered;
# * the delegator's terminal disposition is the live ledger (`COMPLETED`, only
#   when `plan_completion` is met; `REVOKED`, a withdrawal);
# * changing the path is Planning's `revise`: a successor plan that carries the
#   predecessor's authority unchanged and records why, with evidence.
#
# `review_result` is the delegator's decision on one result. MR-S5-1 (Register
# `§151`) makes the decision explicit on the disposition record it already
# writes — no new disposition, plan state or record type:
#
#   decision        ACCEPT  → `COMPLETED` (verification must be met)
#                   REWORK  → `REVOKED`; the plan is revised and one new,
#                             delegated step redoes the work (a verification
#                             finding is required)
#                   REJECT  → `REVOKED`; the work is not redone as the same
#                             work: the plan stays as it is, or is revised
#                             without the rejected step
#   resulting_plan  the plan version the decision leaves current
#   rework_target   REWORK only: {"plan", "step"}, the step that redoes the work
#
# S-5 established these meanings; nothing here adds one. A refusal beyond the
# delegator's authority is not a REJECT: it is the existing escalation route.
#
# CEO acceptance is **operational** (Co-Founder V2 A09 / A11 / A15, *"not final
# acceptance"*). Founder acceptance is reserved (A19) and nothing here records
# or implies it.

ACCEPT, REWORK, REJECT = "ACCEPT", "REWORK", "REJECT"
DECISIONS = (ACCEPT, REWORK, REJECT)
DECISION_DISPOSITION = {ACCEPT: COMPLETED, REWORK: REVOKED, REJECT: REVOKED}
PROVENANCE_FIELDS = ("decision", "resulting_plan", "rework_target")
DELEGATOR_REVIEW = ("FD-P11-001 §15.2", FD_P11_001_RECORD)
FOUNDER_ACCEPTANCE = ("NOT RECORDED — CEO acceptance is operational (Co-Founder V2 "
                      "A09 / A11 / A15, not final acceptance); Founder acceptance is "
                      "reserved (A19) and is not produced by this loop")


def decision_fault(provenance: dict, disposition: Optional[str]) -> Optional[str]:
    """Why a decision record is malformed, or None. Shape only (MR-S5-1 §12):
    the plan relationships are checked against the surface by `plan_outcome`."""
    decision = provenance.get("decision")
    if decision not in DECISIONS:
        return f"decision {decision!r} is not one of {DECISIONS}"
    if DECISION_DISPOSITION[decision] != disposition:
        return (f"{decision} is recorded as {disposition!r}, "
                f"not {DECISION_DISPOSITION[decision]!r}")
    plan, target = provenance.get("resulting_plan"), provenance.get("rework_target")
    if not isinstance(plan, str) or not plan:
        return f"{decision} names no resulting plan"
    if decision == REWORK:
        if not isinstance(target, dict) or not target.get("step"):
            return "REWORK names no rework target"
        if target.get("plan") != plan:
            return (f"the rework target belongs to plan {target.get('plan')!r}, "
                    f"not the resulting plan {plan!r}")
    elif target is not None:
        return f"{decision} carries a rework target"
    return None


def _grant_record(root: Path, delegation_id: str) -> dict:
    source = Path(root) / f"{delegation_id}.delegation.json"
    if not source.is_file():
        raise DelegationError(f"no such delegation record: {source}")
    return json.loads(source.read_text(encoding="utf-8"))


def _bound_plan_on(surface, plan_key: Optional[str]):
    plans = [p for goal in surface._goals for p in surface.history(goal)  # noqa: SLF001
             if p.key == plan_key]
    if len(plans) != 1:
        raise DelegationError(f"{len(plans)} plans named {plan_key!r} on the surface")
    return plans[0]


def review_result(root: Path, delegation_id: str, *, surface, decision: str,
                  reviewer: str, reason: str, rework_steps=None, rework_target=None,
                  resulting_steps=None, ledger: Path = LIVE_LEDGER,
                  authority: Tuple[str, str] = DELEGATOR_REVIEW) -> dict:
    """The delegator's operational decision on one delegated result.

    ACCEPT  → `COMPLETED`, recorded only when the result verifies
              (`plan_completion`). The resulting plan is the bound plan.
    REWORK  → requires a result whose verification is **not** met. The bound
              plan is revised to ``rework_steps``; ``rework_target`` names the
              delegated step in them that redoes the work. `REVOKED`.
    REJECT  → requires a result. The work is not redone as the same work:
              the bound plan stays current, or is revised to
              ``resulting_steps``, which must not contain the rejected step.
              `REVOKED`; no rework target.

    Every check runs before the surface is revised or anything is written.
    The caller persists the surface (`planning_continuity.save`). Only the
    grant's delegator reviews it (`FD-AGENCY-001` Q4-A).
    """
    if reviewer != AUTHORIZED_DELEGATOR:
        raise DelegationError(
            f"{reviewer!r} may not review delegated results: only "
            f"{AUTHORIZED_DELEGATOR!r}, the delegator, decides (FD-AGENCY-001 Q4-A)")
    if decision not in DECISIONS:
        raise DelegationError(f"{decision!r} is not a delegator decision {DECISIONS}")
    if not reason or not reason.strip():
        raise DelegationError("a review must record its reason")
    record = _grant_record(root, delegation_id)
    met, evidence, reasons = plan_completion(root, record)
    finding = ("verification met" if met
               else "verification not met: " + "; ".join(reasons))
    stated = (f"CEO {decision} (delegator review, {authority[0]}; Co-Founder V2 "
              f"A09 / A11 — operational, not Founder acceptance): {reason.strip()} "
              f"[{finding}]")
    bound = _bound_plan(record)
    step_key = (record.get("work_scope") or [None])[0]

    if decision == ACCEPT:
        if rework_steps or rework_target or resulting_steps:
            raise DelegationError("ACCEPT takes no rework target and revises no plan")
        provenance = {"decision": ACCEPT, "resulting_plan": bound, "rework_target": None}
        path = record_disposition(root, delegation_id, disposition=COMPLETED,
                                  delegator=reviewer, reason=stated, ledger=ledger,
                                  authority=authority, provenance=provenance)
        return {"decision": ACCEPT, "disposition": str(path), "verification": finding,
                **provenance}

    if evidence is None:
        raise DelegationError(f"{decision} needs a result to decide on: {finding}")
    from tools.planning import PlanningEvidence
    plan = _bound_plan_on(surface, bound)
    observed = PlanningEvidence(source=_rel(evidence), observation=finding)

    if decision == REWORK:
        if met:
            raise DelegationError(
                "REWORK needs a verification finding; this result verifies")
        if resulting_steps:
            raise DelegationError("REWORK revises the plan to rework_steps, not resulting_steps")
        if not rework_steps:
            raise DelegationError("REWORK must say what the work is sent back as")
        target = next((s for s in rework_steps if s.key == rework_target), None)
        if target is None:
            raise DelegationError(
                f"rework target {rework_target!r} is not a step of the revised plan")
        if not target.requires_delegation:
            raise DelegationError(
                f"rework target {rework_target!r} is not delegated work; rework is "
                "the delegated work done again")
        successor = surface.revise(
            plan, steps=tuple(rework_steps),
            reason=f"CEO REWORK of grant {delegation_id}: {reason.strip()}",
            evidence=(observed,))
        provenance = {"decision": REWORK, "resulting_plan": successor.key,
                      "rework_target": {"plan": successor.key, "step": rework_target}}
    else:   # REJECT
        if rework_target or rework_steps:
            raise DelegationError("REJECT carries no rework target: the work is not redone")
        if resulting_steps:
            if step_key in [s.key for s in resulting_steps]:
                raise DelegationError(
                    f"the revised plan still contains {step_key!r}: redoing the same "
                    "work is REWORK, not REJECT")
            successor = surface.revise(
                plan, steps=tuple(resulting_steps),
                reason=f"CEO REJECT of grant {delegation_id}: {reason.strip()}",
                evidence=(observed,))
            resulting = successor.key
        else:
            if surface.is_superseded(plan):
                raise DelegationError(f"plan {bound!r} is superseded; name the resulting steps")
            resulting = bound
        provenance = {"decision": REJECT, "resulting_plan": resulting, "rework_target": None}
    path = record_disposition(root, delegation_id, disposition=REVOKED,
                              delegator=reviewer, reason=stated, ledger=ledger,
                              authority=authority, provenance=provenance)
    return {"decision": decision, "disposition": str(path), "verification": finding,
            "superseded_plan": bound if provenance["resulting_plan"] != bound else None,
            **provenance}


def _decision_of(item: Optional[dict]) -> Tuple[Optional[str], str]:
    """The recorded decision, and whether it is explicit or a legacy reading."""
    if item is None:
        return None, "NONE"
    if "decision" in item:
        return item["decision"], "EXPLICIT"
    if item.get("disposition") == COMPLETED:
        return ACCEPT, "LEGACY (derived: COMPLETED ⇒ ACCEPT)"
    return None, "LEGACY (REVOKED: decision not recorded)"


def plan_outcome(surface, goal_key: str, root: Path,
                 ledger: Path = LIVE_LEDGER) -> dict:
    """The originating plan's outcome, derived from persisted facts only.

    For every plan version: each delegated step's grants, their operational
    status (`ACTIVE` / `COMPLETED` / `REVOKED`), their verification and the
    recorded decision (explicit, or a legacy reading); each CEO step, done once
    every step it depends on has a recorded decision; and, for a step that is a
    rework target, the grant whose work it redoes. The plan is complete only if
    its **current** version has every delegated step `COMPLETED` and every CEO
    step done. Decision records are checked against the plan chain
    (`decision_faults`). Nothing is stored by this function.
    """
    chain = surface.history(goal_key)
    keys = [p.key for p in chain]
    records = []
    for path in sorted(Path(root).glob("*.delegation.json")):
        records.append(json.loads(path.read_text(encoding="utf-8")))
    dispositions, faults = read_dispositions(root, ledger)
    decision_faults = []
    reworks: Dict[Tuple[str, str], dict] = {}
    for record in records:
        item = dispositions.get(record["delegation_id"])
        if not item or "decision" not in item or _bound_plan(record) not in keys:
            continue
        gid, bound = record["delegation_id"], _bound_plan(record)
        resulting = item.get("resulting_plan")
        if resulting not in keys:
            decision_faults.append(f"{gid}: resulting plan {resulting!r} is not on this goal")
            continue
        plan = chain[keys.index(resulting)]
        if keys.index(resulting) < keys.index(bound):
            decision_faults.append(f"{gid}: resulting plan {resulting!r} precedes {bound!r}")
        if item["decision"] == REWORK:
            target = item["rework_target"]["step"]
            step = next((s for s in plan.steps if s.key == target), None)
            if resulting == bound or step is None or not step.requires_delegation:
                decision_faults.append(
                    f"{gid}: rework target {target!r} is not a delegated step of a "
                    f"revision of {bound!r}")
            else:
                reworks[(resulting, target)] = {"plan": bound, "step": record["work_scope"][0],
                                               "grant": gid}
        if item["decision"] == REJECT and resulting != bound and \
                record["work_scope"][0] in [s.key for s in plan.steps]:
            decision_faults.append(f"{gid}: REJECT's resulting plan still contains the step")
    versions = []
    for index, plan in enumerate(chain):
        done: Dict[str, bool] = {}
        decided: Dict[str, bool] = {}
        steps = []
        for step in sequence_steps(plan):
            if step.requires_delegation:
                grants = []
                for record in records:
                    if _bound_plan(record) != plan.key or record.get("work_scope") != [step.key]:
                        continue
                    gid = record["delegation_id"]
                    item = dispositions.get(gid)
                    met, evidence, reasons = plan_completion(root, record)
                    decision, provenance = _decision_of(item)
                    grants.append({
                        "delegation_id": gid, "recipient": record.get("recipient_instance"),
                        "historical_status": record.get("status"),
                        "operational_status": item["disposition"] if item else record.get("status"),
                        "evidence": None if evidence is None else _rel(evidence),
                        "verification": "met" if met else list(reasons),
                        "decision": decision, "decision_provenance": provenance,
                        "resulting_plan": None if item is None else item.get("resulting_plan"),
                        "rework_target": None if item is None else item.get("rework_target"),
                        "reason": None if item is None else item.get("reason"),
                        "decided_under": None if item is None else item.get("authority_instrument")})
                status = [g["operational_status"] for g in grants]
                done[step.key] = COMPLETED in status
                decided[step.key] = bool(grants) and all(s != ACTIVE for s in status)
                steps.append({"step": step.key, "performed_by": "delegated agent",
                              "grants": grants, "done": done[step.key],
                              "reworks": reworks.get((plan.key, step.key)),
                              "outcome": (COMPLETED if COMPLETED in status else
                                          ACTIVE if ACTIVE in status else
                                          REVOKED if grants else "DELEGATION REQUIRED")})
            else:
                deps = step.depends_on
                done[step.key] = decided[step.key] = bool(deps) and all(
                    decided.get(d, False) for d in deps)
                steps.append({"step": step.key, "performed_by": "CEO",
                              "depends_on": list(deps), "done": done[step.key]})
        versions.append({
            "plan": plan.key, "origin": plan.origin.name, "authority": plan.authority.cited(),
            "current": index == len(chain) - 1,
            "superseded_by": chain[index + 1].key if index + 1 < len(chain) else None,
            "reason": plan.reason, "evidence": list(plan.evidence),
            "steps": steps, "completed": all(done.values())})
    current = versions[-1]
    return {"goal": goal_key, "current_plan": current["plan"],
            "completed": current["completed"],
            "open_steps": [s["step"] for s in current["steps"] if not s["done"]],
            "versions": versions, "disposition_faults": list(faults),
            "decision_faults": decision_faults,
            "founder_acceptance": FOUNDER_ACCEPTANCE}


def sequence_steps(plan):
    """Plan steps in dependency order (`tools.planning.surface.sequence`)."""
    from tools.planning.surface import sequence
    return sequence(plan)
