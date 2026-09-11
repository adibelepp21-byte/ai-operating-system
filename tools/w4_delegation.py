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
        self._issued[delegation.delegation_id] = delegation
        if self._root is not None:
            (self._root / f"{delegation.delegation_id}.delegation.json"
             ).write_text(json.dumps(delegation.to_payload(), indent=2),
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
        self._issued[delegation_id] = revoked
        if self._root is not None:
            payload = revoked.to_payload()
            payload["revocation_reason"] = reason
            (self._root / f"{delegation_id}.delegation.json").write_text(
                json.dumps(payload, indent=2), encoding="utf-8")
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
