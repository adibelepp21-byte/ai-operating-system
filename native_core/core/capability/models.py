"""
Capability domain model — IMMUTABLE DATA CONTRACTS (Blueprint §7 Capability
Package; capability_spec §1–§8; Freeze INV-1/INV-9/INV-10; Domain Model
§1/§2/§5/§6/§7).

Declares the canonical **Capability**: a Department-owned unit of governed
ability. Domain Model §2 [E]: *"A stable, named, outcome-oriented contract —
what can be delivered, independent of how. Owned by exactly one Department."*

**Not abstract.** Capability is descriptive, not behavioural — capability_spec
§9: *"The Capability itself is not an actor and authors no Trace."* These are
frozen dataclasses following the established Native Core convention
(`VersionIdentity`, `RuntimeContext`, `AgentDefinition`). `__post_init__`
performs *structural* fail-closed validation only (PR-4), never domain logic
and never authority evaluation.

Contracts declared here:

  - `DepartmentRef` — a reference to the owning Department. **A stub, by
    design.** Roadmap §9.6 [E]: *"Department ownership (Phase-5 stub)"* and
    *"Blocked by [O]: Department ownership (Phase 5) for full realization —
    built with a governance stub."* Department is a Domain Model entity but
    has no Native Core boundary in Blueprint §3; realizing it is reserved
    (Freeze §13; capability_spec §13). This carries the ownership reference
    that INV-1 requires and nothing more.

  - `CapabilityIdentity` — `(capability_key, capability_version)`. INV-9 [E]
    requires a dependency to *"reference a specific versioned contract"*, so
    identity carries a version. **No version format is imposed**:
    capability_spec §14 leaves *"Versioned-contract representation (reserved —
    no format defined here)"* open, so the version is an opaque non-empty
    string.

  - `GovernanceRecord` — the record of a governed decision made elsewhere.
    capability_spec §3 [A]: *"Cross-Department dependencies are governed
    records (INV-10)."* This boundary **requires the record's presence and
    never evaluates authority** — Capability may not depend on Governance
    (capability_spec §7 restricts dependencies to its Department and other
    Capabilities). Detect, don't decide (PR-3).

  - `CapabilityDependency` — one explicit, versioned dependency edge, with an
    optional governance record attached for the cross-Department case.

  - `Capability` — identity plus exactly one owning Department plus its
    declared dependencies.

Deliberately ABSENT — no execution, no `execute`/`run`/`invoke`/`realize`, no
Agent Definition reference, no Skill or Workflow composition, no Trace, no
lifecycle state machine, no registry, no persistence, no external dependency.
capability_spec §8 [E]: *"Must not execute itself (Freeze §4)."* §5 [E]:
*"Exposes **no** capability to execute itself."* Freeze §10 and Blueprint §7
reserve Capability↔Skill/Workflow composition as Inferred; it is not modelled.

**Deliberately not prohibited:** self-dependency and dependency cycles. No
ratified source forbids either, and inventing a prohibition would add
architecture. Recorded rather than assumed.

Dependencies: stdlib only. This module imports nothing from Governance, Agent,
Skill, Workflow, Runtime, Trace, Memory, Knowledge, Optimization, or
Infrastructure (capability_spec §7/§8; INV-12).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from .exceptions import InvalidCapability, InvalidCapabilityDependency


def _require_text(value: object, label: str, error: type) -> None:
    """Fail closed on anything that is not a non-empty string (PR-4)."""
    if not isinstance(value, str) or not value.strip():
        raise error(f"{label} must be a non-empty string")


@dataclass(frozen=True)
class DepartmentRef:
    """Reference to the Department that owns a Capability.

    A governance stub per Roadmap §9.6, carrying only the ownership reference
    INV-1 requires. It models no Department behaviour, ownership hierarchy, or
    accountability structure — those are reserved (capability_spec §13)."""

    department_key: str

    def __post_init__(self) -> None:
        _require_text(self.department_key, "department_key", InvalidCapability)


@dataclass(frozen=True, order=True)
class CapabilityIdentity:
    """The stable identity of a Capability: its key and its contract version.

    Frozen, hashable and comparable. The version is opaque — capability_spec
    §14 reserves the versioned-contract representation, so no scheme is
    imposed here."""

    capability_key: str
    capability_version: str

    def __post_init__(self) -> None:
        _require_text(self.capability_key, "capability_key", InvalidCapability)
        _require_text(
            self.capability_version, "capability_version", InvalidCapability
        )


@dataclass(frozen=True)
class GovernanceRecord:
    """Record of a governed decision taken outside this boundary.

    Carries the reference only. This boundary asserts the record's *presence*
    where INV-10 requires it and never interprets, evaluates, or grants
    authority — automation may detect, never decide (PR-3; Constitution §6.2
    invariant 2)."""

    decision_reference: str

    def __post_init__(self) -> None:
        _require_text(
            self.decision_reference, "decision_reference", InvalidCapability
        )


@dataclass(frozen=True)
class CapabilityDependency:
    """One explicit, versioned Capability-to-Capability dependency (INV-9).

    `governance` carries the governed record required when the dependency
    crosses Department ownership (INV-10). Whether it is required is a
    property of the two Departments involved and is therefore evaluated where
    both are known — in `CapabilityGraph`, not here."""

    depends_on: CapabilityIdentity
    governance: Optional[GovernanceRecord] = None

    def __post_init__(self) -> None:
        if not isinstance(self.depends_on, CapabilityIdentity):
            raise InvalidCapabilityDependency(
                "depends_on must be a CapabilityIdentity "
                "(INV-9: explicit, versioned contract)"
            )
        if self.governance is not None and not isinstance(
            self.governance, GovernanceRecord
        ):
            raise InvalidCapabilityDependency(
                "governance must be a GovernanceRecord when present (INV-10)"
            )


@dataclass(frozen=True)
class Capability:
    """A Department-owned unit of governed ability.

    Owned by exactly one Department (INV-1) and carrying its explicit,
    versioned dependencies (INV-9). Descriptive only — it does not execute,
    is not an actor, and authors no Trace (capability_spec §5/§9)."""

    identity: CapabilityIdentity
    owning_department: DepartmentRef
    dependencies: Tuple[CapabilityDependency, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.identity, CapabilityIdentity):
            raise InvalidCapability("identity must be a CapabilityIdentity")
        if not isinstance(self.owning_department, DepartmentRef):
            raise InvalidCapability(
                "owning_department must be exactly one DepartmentRef (INV-1)"
            )
        if not isinstance(self.dependencies, tuple):
            raise InvalidCapability("dependencies must be a tuple")
        for dependency in self.dependencies:
            if not isinstance(dependency, CapabilityDependency):
                raise InvalidCapabilityDependency(
                    "every dependency must be a CapabilityDependency (INV-9)"
                )
            # capability_spec §7 [E]: a Capability depends on its Department
            # and on *other* Capabilities. A dependency on itself is not a
            # dependency on another Capability, so it fails closed (PR-4).
            # Checked here rather than in CapabilityGraph because it is an
            # intra-Capability fact, visible without the rest of the graph.
            if dependency.depends_on.capability_key == self.identity.capability_key:
                raise InvalidCapabilityDependency(
                    f"{self.identity.capability_key!r} declares a dependency on "
                    "itself; capability_spec §7 admits dependencies on *other* "
                    "Capabilities only"
                )
