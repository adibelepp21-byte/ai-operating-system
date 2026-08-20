"""
Capability boundary exceptions (Blueprint §7 Capability Package; capability_spec
§8/§11; Freeze INV-1/INV-9/INV-10/INV-11).

Fail Closed (PR-4; capability_spec §11): *"an ungoverned or undocumented
dependency is invalid."* Every condition the specification names as invalid
raises here rather than being coerced into a usable value.

Deliberately ABSENT: no exception for a zero-implementer Capability. INV-14
and capability_spec §10 require that condition to be **flagged for governance
review**, not raised — Detect Don't Decide (PR-3). It is surfaced as a returned
value by the dependency graph, never as an error.
"""

from __future__ import annotations


class CapabilityError(Exception):
    """Base for every Capability boundary failure."""


class InvalidCapability(CapabilityError):
    """Raised when a Capability cannot be constructed accountably.

    Covers the structural conditions the specification fixes: a Capability
    must carry an identity and must be owned by exactly one Department
    (INV-1; capability_spec §2)."""


class InvalidCapabilityDependency(CapabilityError):
    """Raised when a Capability-to-Capability dependency is not explicit or
    not versioned.

    INV-9: *"Every Capability-to-Capability dependency must be explicit and
    must reference a specific versioned contract."*

    Also raised when a Capability declares a dependency on itself:
    capability_spec §7 admits dependencies on *other* Capabilities only."""


class UndocumentedCapabilityDependency(CapabilityError):
    """Raised when a declared dependency names a Capability absent from the
    graph being assembled.

    INV-11: *"The full graph of Capability dependencies must remain queryable
    and observable at all times — no undocumented dependencies."*"""


class UngovernedCrossDepartmentDependency(CapabilityError):
    """Raised when a dependency crosses Department ownership without a
    governance record.

    INV-10: *"Cross-Department Capability dependencies require governance
    approval through the Decision-Making Process — never silent adoption."*
    capability_spec §3 records such approvals as governed records carried on
    the dependency; this boundary requires the record's presence and never
    evaluates authority itself (PR-3)."""


class InvalidOrganization(CapabilityError):
    """Raised when an Organization is malformed.

    Freeze §4: Organization is the hierarchy root and the accountability root;
    an Organization without identity is the root of nothing."""


class InvalidDepartment(CapabilityError):
    """Raised when a Department is malformed.

    Freeze §4: Department is an accountability unit owned by an Organization
    that owns Capabilities (INV-1) and Agent Definitions (INV-2)."""


class UnknownOrganization(CapabilityError):
    """Raised when a Department names an Organization absent from the graph.

    department_spec §11: an unresolvable parent fails closed — the parent edge
    is meaningless without its referent."""


class UnknownDepartment(CapabilityError):
    """Raised when an ownership reference resolves to no known Department.

    INV-1: *"Every Capability is owned by exactly one Department."* A reference
    resolving to zero Departments is not ownership."""


class ConflictingCapabilityOwnership(CapabilityError):
    """Raised when two Departments claim the same Capability.

    INV-1, and Freeze §4's explicit prohibition on a Department *"owning
    another Department's Capability"*. Exactly one, never two."""


class DisputedCapabilityOwnership(CapabilityError):
    """Raised when the two sides of an ownership edge disagree.

    INV-1 is represented twice — a Capability names its owner through
    `DepartmentRef`, and a Department names what it owns through
    `owned_capabilities`. When one side asserts an edge the other does not
    acknowledge, *"owned by exactly one Department"* is not satisfied: the
    Capability is owned by zero Departments that agree it is theirs.

    Distinct from `ConflictingCapabilityOwnership`, which is two Departments
    claiming one Capability. This is the two representations contradicting
    each other about a single edge."""
