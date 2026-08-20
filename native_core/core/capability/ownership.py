"""
Organization and Department — the ownership context Capability lives in.

**Why this module is here, and not a sibling boundary.** Native Core Blueprint
§4 **[E]** defines the Spine as *"**capability + the ownership context it lives
in**"*, and Blueprint §7 **[E]** lists the Capability package's allowed
dependencies as *"**its Department**; other Capabilities via governed versioned
contracts"*. `NCIR §9.6` **[E]** records *"Department ownership (Phase-5 stub)"*
as a dependency **of this package**, and **[O]** *"Blocked by: Department
ownership (Phase 5) for full realization — built with a governance stub in Phase
3."* This module is that full realization; `DepartmentRef` was its stub.

Blueprint §4 also fixes the core region at *"exactly the eleven frozen subsystem
boundaries — no more (no new entity/subsystem may be introduced)"*, so a twelfth
`core/department/` boundary is not available. Realization belongs here.

Organization and Department are **already-ratified** Freeze §4 entities — two of
the twelve. This module realizes them and ratifies nothing. Authorized by
FOUNDER · `ACT-CC-F03-035` (`DEC-DEPT-REALIZATION = AUTHORIZE`) and located by
`ACT-CC-F03-036` Outcome A.

**Ownership reconciliation** (`ACT-CC-F03-037`). Realization put INV-1 on both
sides of the ownership edge: a Capability names its owner through
`DepartmentRef`, and a Department names what it owns through
`owned_capabilities`. Two representations of one fact can contradict each other,
so `resolve` requires both sides to agree before treating an edge as ownership
(PR-4), and `disputed_ownership` / `unbacked_ownership_claims` survey a corpus
without halting (PR-3). This enforces INV-1 and `capability_spec §11`; it adds
no invariant.

Deliberately absent, because Freeze §4 does not establish them: roles,
workforce, budgets, KPIs, lifecycle *states*, Department nesting, and
Department↔Skill/Workflow relations (Inferred, reserved).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Iterable, Mapping, Optional, Tuple

from .exceptions import (
    ConflictingAgentDefinitionOwnership,
    DisputedCapabilityOwnership,
    ConflictingCapabilityOwnership,
    InvalidDepartment,
    InvalidOrganization,
    UnknownDepartment,
    UnknownOrganization,
)
from .models import Capability, _require_text


@dataclass(frozen=True, order=True)
class OrganizationIdentity:
    """The stable identity of an Organization.

    Freeze §4: Organization is the hierarchy root — *"Dependencies: none above
    it."* Identity is therefore the whole of it at this boundary."""

    organization_key: str

    def __post_init__(self) -> None:
        _require_text(
            self.organization_key, "organization_key", InvalidOrganization
        )


@dataclass(frozen=True)
class Organization:
    """The hierarchy root and accountability root (Freeze §4).

    Owns Departments. Not an actor: Freeze §4 forbids Organization *"acting as
    an executor"*, so this exposes no execution surface and authors no Trace."""

    identity: OrganizationIdentity

    def __post_init__(self) -> None:
        if not isinstance(self.identity, OrganizationIdentity):
            raise InvalidOrganization("identity must be an OrganizationIdentity")


@dataclass(frozen=True, order=True)
class DepartmentIdentity:
    """The stable identity of a Department.

    The key is the value `DepartmentRef.department_key` has carried as a stub
    since Phase 3; realization gives that key a referent."""

    department_key: str

    def __post_init__(self) -> None:
        _require_text(self.department_key, "department_key", InvalidDepartment)


@dataclass(frozen=True)
class Department:
    """An accountability unit owned by exactly one Organization (Freeze §4).

    Freeze §4 [E] gives a Department two ownership responsibilities — it *"owns
    Capabilities **and Agent Definitions**"* — and INV-2 [E] fixes the second:
    *"Every Agent Definition is owned by exactly one Department."* Both are held
    as identity *keys*, never as embedded state; the owned entity's own boundary
    owns its data, and holding keys is what keeps this package free of any
    dependency on Agent (department_spec §8).

    INV-2's *second* clause — that a Definition *"implements at least one
    Capability"* — is **not** enforced here. Checking a Definition against
    Capabilities is Agent construction discipline, which `agent_spec §12`/`§13`
    [O] place in the Agent Factory, *"reserved to the Architect"*."""

    identity: DepartmentIdentity
    organization: OrganizationIdentity
    owned_capabilities: Tuple[str, ...] = field(default_factory=tuple)
    owned_agent_definitions: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.identity, DepartmentIdentity):
            raise InvalidDepartment("identity must be a DepartmentIdentity")
        if not isinstance(self.organization, OrganizationIdentity):
            raise InvalidDepartment(
                "organization must be exactly one OrganizationIdentity "
                "(Freeze §4: a Department is owned by an Organization)"
            )
        self._validate_owned(
            self.owned_capabilities, "owned_capabilities", "capability_key", "INV-1"
        )
        self._validate_owned(
            self.owned_agent_definitions,
            "owned_agent_definitions",
            "agent_definition_key",
            "INV-2",
        )

    def _validate_owned(
        self, owned: Tuple[str, ...], field_name: str, key_name: str, invariant: str
    ) -> None:
        """Both ownership sets carry the same rule: distinct, non-empty keys.

        `agent_definition_key` is the ratified identity name already used by the
        Agent Definition contract; it is named identically here to avoid
        terminology drift."""
        if not isinstance(owned, tuple):
            raise InvalidDepartment(f"{field_name} must be a tuple")
        seen = set()
        for key in owned:
            _require_text(key, key_name, InvalidDepartment)
            if key in seen:
                raise InvalidDepartment(
                    f"{self.identity.department_key!r} claims {key!r} more "
                    f"than once; ownership is exactly one ({invariant})"
                )
            seen.add(key)


class OwnershipGraph:
    """An immutable, queryable Organization → Department ownership graph.

    Construction validates the Freeze §4 parent edge and INV-1, and fails closed
    (PR-4). Unowned capabilities are a *query*, never a construction rule —
    detect, don't decide (PR-3), matching how `CapabilityGraph` reports INV-14.
    """

    __slots__ = (
        "_organizations",
        "_departments",
        "_owner_of",
        "_definition_owner_of",
    )

    def __init__(
        self,
        organizations: Iterable[Organization],
        departments: Iterable[Department],
    ) -> None:
        orgs = {}
        definition_owner_of = {}
        for organization in organizations:
            if not isinstance(organization, Organization):
                raise InvalidOrganization("every member must be an Organization")
            key = organization.identity.organization_key
            if key in orgs:
                raise InvalidOrganization(
                    f"duplicate organization_key in graph: {key!r}"
                )
            orgs[key] = organization

        depts = {}
        owner_of = {}
        for department in departments:
            if not isinstance(department, Department):
                raise InvalidDepartment("every member must be a Department")
            key = department.identity.department_key
            if key in depts:
                raise InvalidDepartment(
                    f"duplicate department_key in graph: {key!r}"
                )

            parent = department.organization.organization_key
            if parent not in orgs:
                raise UnknownOrganization(
                    f"department {key!r} names organization {parent!r}, which "
                    "is not present in the graph (Freeze §4: a Department is "
                    "owned by an Organization)"
                )

            for capability_key in department.owned_capabilities:
                existing = owner_of.get(capability_key)
                if existing is not None:
                    raise ConflictingCapabilityOwnership(
                        f"capability {capability_key!r} is claimed by both "
                        f"{existing!r} and {key!r}; INV-1 admits exactly one "
                        "owning Department"
                    )
                owner_of[capability_key] = key

            # INV-2 clause 1 [E]: *"Every Agent Definition is owned by exactly
            # one Department."* Same rule as INV-1, a different owned entity.
            for definition_key in department.owned_agent_definitions:
                existing = definition_owner_of.get(definition_key)
                if existing is not None:
                    raise ConflictingAgentDefinitionOwnership(
                        f"agent definition {definition_key!r} is claimed by "
                        f"both {existing!r} and {key!r}; INV-2 admits exactly "
                        "one owning Department"
                    )
                definition_owner_of[definition_key] = key

            depts[key] = department

        self._organizations = MappingProxyType(dict(orgs))
        self._departments = MappingProxyType(dict(depts))
        self._owner_of = MappingProxyType(dict(owner_of))
        self._definition_owner_of = MappingProxyType(
            dict(definition_owner_of)
        )

    # -- queries ---------------------------------------------------------

    def organizations(self) -> Mapping[str, Organization]:
        return self._organizations

    def departments(self) -> Mapping[str, Department]:
        return self._departments

    def department(self, department_key: str) -> Department:
        """Resolve an ownership reference to its Department (INV-1)."""
        try:
            return self._departments[department_key]
        except KeyError:
            raise UnknownDepartment(
                f"no Department {department_key!r} in the graph (INV-1)"
            ) from None

    def departments_of(
        self, organization_key: str
    ) -> Tuple[DepartmentIdentity, ...]:
        """The Departments an Organization owns (Freeze §4)."""
        if organization_key not in self._organizations:
            raise UnknownOrganization(
                f"no Organization {organization_key!r} in the graph"
            )
        return tuple(
            sorted(
                department.identity
                for department in self._departments.values()
                if department.organization.organization_key == organization_key
            )
        )

    def owner_of(self, capability_key: str) -> Department:
        """The single Department owning a Capability (INV-1)."""
        owner = self._owner_of.get(capability_key)
        if owner is None:
            raise UnknownDepartment(
                f"capability {capability_key!r} has no owning Department in "
                "the graph (INV-1)"
            )
        return self._departments[owner]

    def owner_of_agent_definition(self, agent_definition_key: str) -> Department:
        """The single Department owning an Agent Definition (INV-2 clause 1).

        Resolved from the Department side only. This package holds the ratified
        `agent_definition_key` and never imports Agent (department_spec §8), so
        an Agent Definition's own view of its owner is not visible here — see
        `unowned_agent_definitions` for what that costs."""
        owner = self._definition_owner_of.get(agent_definition_key)
        if owner is None:
            raise UnknownDepartment(
                f"agent definition {agent_definition_key!r} has no owning "
                "Department in the graph (INV-2)"
            )
        return self._departments[owner]

    def agent_definitions_of(self, department_key: str) -> Tuple[str, ...]:
        """The Agent Definition keys a Department owns (Freeze §4)."""
        return tuple(sorted(self.department(department_key).owned_agent_definitions))

    def unowned_agent_definitions(
        self, agent_definition_keys: Iterable[str]
    ) -> Tuple[str, ...]:
        """Definition keys no Department claims — flagged, never raised.

        INV-2 makes an unowned Definition invalid, but this boundary detects and
        does not decide (PR-3): over a partial corpus an absent claim is
        ordinary incompleteness, and the caller supplies the keys precisely so
        that no `capability → agent` dependency is created."""
        return tuple(
            sorted(
                key
                for key in agent_definition_keys
                if key not in self._definition_owner_of
            )
        )

    # -- R-4: bind DepartmentRef to its referent --------------------------

    def resolve(
        self, capabilities: Iterable[Capability]
    ) -> Tuple[Tuple[Capability, Department], ...]:
        """Resolve every Capability's `DepartmentRef` to a real Department.

        Before realization the reference was unverifiable — any non-empty key
        was accepted. Resolution makes INV-1 checkable. Fails closed (PR-4) on
        the first reference that resolves to nothing."""
        resolved = []
        for capability in capabilities:
            if not isinstance(capability, Capability):
                raise UnknownDepartment("every member must be a Capability")
            key = capability.owning_department.department_key
            department = self.department(key)

            # INV-1 is represented on both sides of the edge. Resolving the
            # reference is not enough: the Department must also acknowledge
            # the Capability, or no Department actually owns it. Fails closed
            # (PR-4) — a contradiction is not resolved by preferring a side.
            capability_key = capability.identity.capability_key
            if capability_key not in department.owned_capabilities:
                claimant = self._owner_of.get(capability_key)
                raise DisputedCapabilityOwnership(
                    f"{capability_key!r} names department {key!r} as its "
                    f"owner, but {key!r} does not claim it"
                    + (
                        f"; {claimant!r} does"
                        if claimant is not None
                        else " and no Department in the graph does"
                    )
                    + " (INV-1: owned by exactly one Department)"
                )
            resolved.append((capability, department))
        return tuple(resolved)

    def disputed_ownership(
        self, capabilities: Iterable[Capability]
    ) -> Tuple[Tuple[str, str, Optional[str]], ...]:
        """Edges where the Capability and the Department contradict each other.

        Each entry is `(capability_key, department_named_by_the_capability,
        department_that_actually_claims_it_or_None)`. Detect, don't decide
        (PR-3): surveys the whole corpus and reports, so a reconciliation pass
        sees every contradiction rather than only the first.

        References that resolve to no Department at all are *not* reported
        here — that is `unresolved_ownership`, a different condition."""
        disputes = []
        for capability in capabilities:
            named = capability.owning_department.department_key
            department = self._departments.get(named)
            if department is None:
                continue
            capability_key = capability.identity.capability_key
            if capability_key not in department.owned_capabilities:
                disputes.append(
                    (capability_key, named, self._owner_of.get(capability_key))
                )
        return tuple(sorted(disputes))

    def unbacked_ownership_claims(
        self, capabilities: Iterable[Capability]
    ) -> Tuple[Tuple[str, str], ...]:
        """Departments claiming Capabilities no supplied Capability declares.

        Each entry is `(department_key, capability_key)`. A claim with no
        Capability behind it is reported, never raised: over a partial corpus
        it is ordinary incompleteness, and deciding which it is belongs to
        governance, not to this boundary (PR-3)."""
        declared = {
            capability.identity.capability_key for capability in capabilities
        }
        return tuple(
            sorted(
                (department_key, capability_key)
                for department_key, department in self._departments.items()
                for capability_key in department.owned_capabilities
                if capability_key not in declared
            )
        )

    def unresolved_ownership(
        self, capabilities: Iterable[Capability]
    ) -> Tuple[str, ...]:
        """Capability keys whose `DepartmentRef` resolves to no Department.

        Detect, don't decide (PR-3): surveys the whole corpus rather than
        halting on the first gap."""
        return tuple(
            sorted(
                capability.identity.capability_key
                for capability in capabilities
                if capability.owning_department.department_key
                not in self._departments
            )
        )

    def unowned_capabilities(
        self, capability_keys: Iterable[str]
    ) -> Tuple[str, ...]:
        """Capability keys with no owning Department — flagged, never raised."""
        return tuple(
            sorted(key for key in capability_keys if key not in self._owner_of)
        )
