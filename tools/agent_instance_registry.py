"""`P11-W4` — Agent Instance registration under `FD-P11-001 §7`.

**Authorized, and not by construction.** `FD-P11-001 §7`: *"Claude Code may
create and register Agent Instances required for P11-W4, provided every instance
is created through the canonical Agent Instance creation mechanism and is
explicitly attributable to an existing Agent Definition."* The same section
insists creation is an ``AUTHORIZED ACTION`` and *"not: `AUTOMATIC SIDE EFFECT`"*
of P11 authorization.

**The canonical mechanism is used, not replaced.**
`native_core/core/agent/instance.py` already owns `AgentInstance`, which binds
exactly one Definition (`INV-3`) and is deliberately *"Identity only — no
execution, no hosting, no lifecycle, no behavior."*

That covers two of the eight elements `§7` requires. The other six — creation
provenance, creator/delegator provenance, permitted capability surface, lifecycle
state, accountability relationship, verification status — are **organizational**,
and `DP-04` places organizational concepts outside the frozen core. So this
module wraps the canonical identity in an organizational registration record
rather than adding fields to a frozen boundary:

    native_core AgentInstance   identity + definition binding   (frozen core)
    InstanceRegistration        provenance, scope, accountability (organizational)

**`AGENT DEFINITION ≠ AGENT INSTANCE`** (`NC-W4-01`). A Definition describes
*what an agent may be*; an Instance is *an actual instantiated execution
identity*. Registering one does not create the other, and neither is a
Delegation (`NC-W4-02`).

**`AGENT INSTANCE ≠ AUTHORITY`** (`§17`). Creating an instance does not authorize
it to delegate, approve, govern, authorize another instance, or execute arbitrary
work: *"Authority must come from an explicit valid Delegation."* There is
therefore **no method here that returns whether an instance may do anything.**

**Capability scope is bounded by the Definition, not chosen.** `§8` forbids
assigning *"capabilities not supported by the applicable definition"*, so the
permitted surface is intersected with `implemented_capabilities` and a request
for anything outside it fails closed. An instance cannot be registered with more
capability than the Definition it realizes — which is `§16`'s rule applied one
level down: a derived object may not exceed its source.

**Provenance is required, and to `FD-P11-001` specifically.** `§24` rejects a
chain citing only P11, DP-01, a Plan, an Agent Definition, or an implementation
file. Registration therefore demands a citation that resolves **and** names this
Decision — `§10`: `DP-01 ≠ SPECIFIC W4 DELEGATION`.

`§7`: *"No anonymous Agent Instance is valid. No Agent Instance may exist merely
because an implementation function was called."* Both are enforced below.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple

from native_core.core.agent.definition import AgentDefinition
from native_core.core.agent.instance import AgentInstance, InvalidAgentInstance
from tools.planning import AuthorityProvenance

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The Decision that authorizes instance creation. `§24` rejects provenance
#: citing only P11 or DP-01, so the instrument is matched by name and not merely
#: resolved — a resolvable citation to the *wrong* instrument is still invalid.
AUTHORIZING_DECISION = "FD-P11-001"

#: Lifecycle states an instance may hold. `§25` item 10 requires a verifiable
#: lifecycle. Deliberately absent: any state meaning *authorized* — authority
#: comes from a Delegation, never from an instance's own status (`§17`).
REGISTERED = "REGISTERED"
RETIRED = "RETIRED"
LIFECYCLE_STATES = (REGISTERED, RETIRED)

INSTANCE_KEY = re.compile(r"^[a-z0-9][a-z0-9-]{2,63}$")


class InstanceRegistrationError(RuntimeError):
    """Fail closed (`PR-4`)."""


@dataclass(frozen=True)
class InstanceRegistration:
    """One registered Agent Instance, with everything `§7` requires.

    Frozen: a registration that could be edited after the fact would let
    capability scope or accountability drift away from what was authorized.
    Retirement is recorded as a successor state through the registry, never by
    rewriting the record.
    """

    instance: AgentInstance
    permitted_capabilities: Tuple[str, ...]
    created_by: str
    authority: AuthorityProvenance
    accountable_to: str
    lifecycle: str
    registered_at: str
    verified: bool = False

    @property
    def instance_key(self) -> str:
        return self.instance.agent_instance

    @property
    def definition_key(self) -> str:
        return self.instance.agent_definition.agent_definition_key

    def to_payload(self) -> dict:
        return {
            "instance_key": self.instance_key,
            "definition_key": self.definition_key,
            "definition_version":
                self.instance.agent_definition.agent_definition_version,
            "owning_department":
                self.instance.agent_definition.owning_department_key,
            "permitted_capabilities": list(self.permitted_capabilities),
            "created_by": self.created_by,
            "authority_instrument": self.authority.instrument,
            "authority_record": self.authority.record,
            "accountable_to": self.accountable_to,
            "lifecycle": self.lifecycle,
            "registered_at": self.registered_at,
            "verified": self.verified,
        }


class AgentInstanceRegistry:
    """Creates and registers instances. Grants nothing to any of them."""

    def __init__(self, root: Optional[Path] = None):
        self._root = root
        if root is not None:
            root.mkdir(parents=True, exist_ok=True)
        self._registered: Dict[str, InstanceRegistration] = {}

    def register(self, *, instance_key: str, definition: AgentDefinition,
                 permitted_capabilities: Tuple[str, ...], created_by: str,
                 authority: AuthorityProvenance,
                 accountable_to: str) -> InstanceRegistration:
        """Create and register one instance. Every argument is checked.

        There is no defaulting anywhere: `§7` requires each element to be
        *established*, and a default is a value nobody established.
        """
        if not isinstance(instance_key, str) or not INSTANCE_KEY.match(
                instance_key or ""):
            raise InstanceRegistrationError(
                "an instance requires an explicit, well-formed identity — "
                "`§7`: no anonymous Agent Instance is valid")
        if instance_key in self._registered:
            raise InstanceRegistrationError(
                f"instance identity is not unique: {instance_key!r}")
        if not isinstance(definition, AgentDefinition):
            raise InstanceRegistrationError(
                "an instance must derive from an existing Agent Definition — "
                "`§8` forbids inventing one to satisfy W4")

        # `§24`: provenance must name this Decision, not merely resolve.
        if not isinstance(authority, AuthorityProvenance):
            raise InstanceRegistrationError(
                "registration requires a validated authority citation")
        if AUTHORIZING_DECISION not in authority.instrument:
            raise InstanceRegistrationError(
                f"instance creation is authorized by {AUTHORIZING_DECISION}; "
                f"a citation to {authority.instrument!r} does not establish it "
                "— `§10`: DP-01 is not a specific W4 delegation instrument")

        # `§8`/`§16`: scope may not exceed the Definition.
        requested = tuple(permitted_capabilities or ())
        if not requested:
            raise InstanceRegistrationError(
                "an instance requires a bounded capability surface (`§25`.5)")
        unsupported = [c for c in requested
                       if c not in definition.implemented_capabilities]
        if unsupported:
            raise InstanceRegistrationError(
                f"capabilities not supported by {definition.agent_definition_key!r}: "
                f"{unsupported} — `§8` forbids assigning them")

        if not isinstance(created_by, str) or not created_by.strip():
            raise InstanceRegistrationError(
                "creator provenance is required (`§7`)")
        if not isinstance(accountable_to, str) or not accountable_to.strip():
            raise InstanceRegistrationError(
                "an accountability owner is required (`§25`.6)")
        if accountable_to == instance_key:
            raise InstanceRegistrationError(
                "an instance cannot be accountable to itself — "
                "`§15` fixes the chain as instance → delegator → Founder")

        try:
            instance = AgentInstance(agent_instance=instance_key,
                                     agent_definition=definition)
        except InvalidAgentInstance as exc:                # pragma: no cover
            raise InstanceRegistrationError(str(exc)) from exc

        registration = InstanceRegistration(
            instance=instance,
            permitted_capabilities=requested,
            created_by=created_by,
            authority=authority,
            accountable_to=accountable_to,
            lifecycle=REGISTERED,
            registered_at=datetime.now(timezone.utc).isoformat(),
        )
        self._registered[instance_key] = registration
        if self._root is not None:
            (self._root / f"{instance_key}.instance.json").write_text(
                json.dumps(registration.to_payload(), indent=2), encoding="utf-8")
        return registration

    def get(self, instance_key: str) -> InstanceRegistration:
        if instance_key not in self._registered:
            raise InstanceRegistrationError(
                f"no such registered instance: {instance_key!r} — "
                "`§7`: no instance exists merely because a function was called")
        return self._registered[instance_key]

    def is_registered(self, instance_key: str) -> bool:
        return instance_key in self._registered

    def keys(self) -> Tuple[str, ...]:
        return tuple(sorted(self._registered))

    def retire(self, instance_key: str) -> InstanceRegistration:
        """Move an instance to `RETIRED`, replacing the record rather than
        editing it. `§25` item 10: the lifecycle must be verifiable."""
        current = self.get(instance_key)
        retired = InstanceRegistration(
            instance=current.instance,
            permitted_capabilities=current.permitted_capabilities,
            created_by=current.created_by, authority=current.authority,
            accountable_to=current.accountable_to, lifecycle=RETIRED,
            registered_at=current.registered_at, verified=current.verified)
        self._registered[instance_key] = retired
        if self._root is not None:
            (self._root / f"{instance_key}.instance.json").write_text(
                json.dumps(retired.to_payload(), indent=2), encoding="utf-8")
        return retired
