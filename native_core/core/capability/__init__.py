"""
Capability boundary (Native Core Blueprint §3 root tree, §7 Capability Package;
capability_spec; Domain Model §1/§2/§5/§6/§7; Freeze §5 layer 4,
INV-1/INV-9/INV-10/INV-11/INV-14).

Capability is one of the **eleven frozen subsystem boundaries** — Blueprint §3
fixes the tree as `core/{trace, memory, knowledge, governance, runtime, agent,
capability, skill, workflow, infrastructure, optimization}`, and §4 states the
core region *"contains exactly the eleven frozen subsystem boundaries — no
more."* No entity or subsystem is introduced here.

Domain Model §2 [E]: a Capability is *"a stable, named, outcome-oriented
contract — what can be delivered, independent of how. Owned by exactly one
Department."* It is a **Spine** entity (§1/§3), not an Execution entity: it
does not run, does not act, and authors no Trace (capability_spec §9).

What this boundary realizes, per capability_spec §2 and Roadmap §9.6:

    Capability  —owned by→  exactly one Department          (INV-1)
                —declares→  explicit, versioned dependencies (INV-9)
                            governed when cross-Department   (INV-10)
                —forms→     a queryable, observable graph    (INV-11)
                —flags→     zero-implementer capabilities    (INV-14)

Public surface:
  - models:     DepartmentRef · CapabilityIdentity · GovernanceRecord ·
                CapabilityDependency · Capability
  - graph:      CapabilityGraph
  - exceptions: CapabilityError · InvalidCapability ·
                InvalidCapabilityDependency ·
                UndocumentedCapabilityDependency ·
                UngovernedCrossDepartmentDependency

NOT implemented here, and reserved by the frozen architecture:
  - **Capability↔Skill/Workflow composition** — Freeze §10 lists it among the
    Inferred relationships; Blueprint §7 marks it *"Future extension [O] …
    reserved"*; capability_spec §12 repeats it. Not modelled.
  - **Department realization** — Department has no Native Core boundary in
    Blueprint §3. Roadmap §9.6 builds Capability against a *governance stub*;
    full realization is reserved (Freeze §13; capability_spec §13).
  - **Capability instances** — creating one changes *Department and Capability
    structure*, which Constitution §3.4 reserves to an Architecture Decision
    Record (precedent: ADR-0003). None is created here.
  - **Execution of any kind** — capability_spec §5/§8 and Freeze §4: a
    Capability *"must not execute itself."*

Ownership: this boundary owns **only the governed capability model** — the
Capability contract, its ownership reference, its versioned dependency
contracts, and their graph. Agent owns definition and instance identity ·
Runtime owns hosting · Execution owns the execution boundary · Knowledge owns
semantics · Memory owns promotion candidates · Governance owns authority ·
Trace owns history · Infrastructure owns facilities. No ownership transfer.

Dependencies: stdlib only. capability_spec §7 permits dependence on its
Department (ownership) and on other Capabilities via explicit, versioned,
governed contracts — nothing else. This package imports nothing from
Governance, Agent, Skill, Workflow, Runtime, Execution, Trace, Memory,
Knowledge, Optimization, or Infrastructure, and holds no external dependency
(INV-12).
"""

from .ownership import (
    Department,
    DepartmentIdentity,
    Organization,
    OrganizationIdentity,
    OwnershipGraph,
)
from .exceptions import (
    CapabilityError,
    ConflictingCapabilityOwnership,
    InvalidCapability,
    InvalidCapabilityDependency,
    InvalidDepartment,
    InvalidOrganization,
    UndocumentedCapabilityDependency,
    UngovernedCrossDepartmentDependency,
    UnknownDepartment,
    UnknownOrganization,
)
from .graph import CapabilityGraph
from .models import (
    Capability,
    CapabilityDependency,
    CapabilityIdentity,
    DepartmentRef,
    GovernanceRecord,
)

__all__ = [
    "Capability",
    "CapabilityDependency",
    "CapabilityError",
    "CapabilityGraph",
    "CapabilityIdentity",
    "ConflictingCapabilityOwnership",
    "Department",
    "DepartmentIdentity",
    "DepartmentRef",
    "GovernanceRecord",
    "InvalidCapability",
    "InvalidCapabilityDependency",
    "InvalidDepartment",
    "InvalidOrganization",
    "Organization",
    "OrganizationIdentity",
    "OwnershipGraph",
    "UndocumentedCapabilityDependency",
    "UngovernedCrossDepartmentDependency",
    "UnknownDepartment",
    "UnknownOrganization",
]
