# Organization Framework

## Purpose

This document defines how Department and Capability instances are
recorded within AIOS: their repository structure, naming convention, and
identifier policy.

This document does not define what a Department or Capability is, or
what authority governs their creation or retirement. Those are defined
exclusively in the Canonical Domain Model (entities, relationships,
ownership, lifecycle) and Engineering Constitution §3.4 (decision
authority). This document never restates that content; it only describes
where and how instances are recorded once created.

## Authority

Department and Capability creation and retirement authority is governed
exclusively by Engineering Constitution §3.4 and Canonical Domain Model
§6 (Lifecycle Rules). This document does not restate that content.

This document's own content — repository structure, naming, and
identifier conventions — is a documentation and repository-organization
convention, not a governance-authority artifact. It sits within the
Principle Documents tier of Engineering Constitution §4 (Governance
Artifact Relationship), and is maintained through direct Architect-approved
documentation changes, the same way the ADR Framework's own procedural
conventions are maintained.

## Repository Structure

Department and Capability instances are recorded under
`docs/architecture/organization/`:

```
docs/architecture/organization/
  README.md                    — this document
  agent-definitions.md         — the Agent Definition Framework
  execution-artifact-repository.md — the Execution Artifact Repository
                                      Convention
  skill-framework.md           — the Skill Framework
  workflow-framework.md        — the Workflow Framework
  runtime-framework.md         — the Runtime Framework
  tool-framework.md            — the Tool Framework
  <department-slug>/
    README.md                  — that Department's definition
    capabilities/
      <capability-slug>.md
    agent-definitions/
      <agent-definition-slug>.md
```

Each Department is recorded in its own subdirectory, containing a
`README.md` that defines it. Each Capability that Department owns is
recorded as an individual file within that Department's `capabilities/`
subdirectory, and each Agent Definition that Department owns is recorded
as an individual file within that Department's `agent-definitions/`
subdirectory, per the Agent Definition Framework.

Skill, Workflow, Runtime, and Tool instances are governed by a separate
repository convention, recorded in the Execution Artifact Repository
Convention, since these entities are owned centrally rather than by any
single Department and therefore do not fit this document's
Department-nested projection.

## Naming Convention

Department and Capability directory and file names are lowercase,
hyphenated slugs derived from their names — for example, a Department
named "Architecture" is recorded at `architecture/`; a Capability named
"Governance Artifact Maintenance" is recorded at
`capabilities/governance-artifact-maintenance.md`.

## Identifier Policy

Departments and Capabilities do not use synthetic sequential identifiers.
Per the Canonical Domain Model's own Capability entry (§2), a Capability
is a named contract — the name is the identifier. A Department's name
and a Capability's name serve as their stable, citable identity.

Department names are unique across the Organization. Capability names
are unique across the Organization as a clarity default, even though
Domain Model ownership rules only guarantee uniqueness within a single
owning Department.

## Filesystem Projection of Domain Model Ownership

The nesting of Capability files inside their owning Department's
directory is a direct filesystem projection of the Canonical Domain
Model's ownership relationship — Department **owns** Capability, and a
Capability is owned by exactly one Department. A Capability file's
location is evidence of which Department owns it; this convention does
not itself define or alter that ownership rule, it reflects it.

This convention does not define, imply, or constrain any technology,
storage mechanism, or tooling — it is a directory and naming convention
only, consistent with the Canonical Domain Model's own Architectural
Boundaries, which exclude repository layout from its authority.

## Status

One Department, Platform, has been created, owning one Capability,
Governance Artifact Integrity. Both were established by
[ADR-0003](../adr/decisions/ADR-0003.md) and are recorded per the
Repository Structure convention, above, at
`docs/architecture/organization/platform/`.
