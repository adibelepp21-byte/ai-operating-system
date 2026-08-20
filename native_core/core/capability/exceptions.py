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
