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

Deliberately absent, because Freeze §4 does not establish them: roles,
workforce, budgets, KPIs, lifecycle *states*, Department nesting, and
Department↔Skill/Workflow relations (Inferred, reserved).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Iterable, Mapping, Tuple

from .exceptions import (
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

    Owns Capabilities (INV-1). Ownership is held as capability *keys*, never as
    embedded Capability state. Agent Definition ownership (INV-2) is realizable
    on this surface but is a separate construction target, not built here."""

    identity: DepartmentIdentity
    organization: OrganizationIdentity
    owned_capabilities: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.identity, DepartmentIdentity):
            raise InvalidDepartment("identity must be a DepartmentIdentity")
        if not isinstance(self.organization, OrganizationIdentity):
            raise InvalidDepartment(
                "organization must be exactly one OrganizationIdentity "
                "(Freeze §4: a Department is owned by an Organization)"
            )
        if not isinstance(self.owned_capabilities, tuple):
            raise InvalidDepartment("owned_capabilities must be a tuple")
        seen = set()
        for capability_key in self.owned_capabilities:
            _require_text(capability_key, "capability_key", InvalidDepartment)
            if capability_key in seen:
                raise InvalidDepartment(
                    f"{self.identity.department_key!r} claims "
                    f"{capability_key!r} more than once; ownership is exactly "
                    "one (INV-1)"
                )
            seen.add(capability_key)


class OwnershipGraph:
    """An immutable, queryable Organization → Department ownership graph.

    Construction validates the Freeze §4 parent edge and INV-1, and fails closed
    (PR-4). Unowned capabilities are a *query*, never a construction rule —
    detect, don't decide (PR-3), matching how `CapabilityGraph` reports INV-14.
    """

    __slots__ = ("_organizations", "_departments", "_owner_of")

    def __init__(
        self,
        organizations: Iterable[Organization],
        departments: Iterable[Department],
    ) -> None:
        orgs = {}
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

            depts[key] = department

        self._organizations = MappingProxyType(dict(orgs))
        self._departments = MappingProxyType(dict(depts))
        self._owner_of = MappingProxyType(dict(owner_of))

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
            resolved.append((capability, self.department(key)))
        return tuple(resolved)

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
