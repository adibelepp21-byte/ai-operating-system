# Execution Artifact Repository Convention

## 1. Purpose

This document establishes the governance boundary and responsibility scope
for how Skill, Workflow, Runtime, and Tool instances are recorded within
AIOS as repository artifacts.

This document does not yet define directory structure, naming convention,
or reference syntax for these instances. Those remain open, pending a
separate Architect decision evaluating the option space already identified
in the Architecture Discovery Report for this question. This document
establishes only that the shared repository-location convention for these
four entities, once decided, belongs here — rather than in the
Organization Framework, or independently invented by each entity's
eventual individual Framework.

## 2. Scope

This document governs the shared repository-location convention boundary
for exactly four Canonical Domain Model entities: Skill, Workflow,
Runtime, and Tool.

This document does not establish, and should not be read to imply, a
general rule that centrally-owned status by itself entitles any entity to
its own Principle Document. Its scope is grounded in what these four
entities specifically share (see Section 5); it does not extend to any
other current or future entity by default.

This document does not govern:

- Department, Capability, or Agent Definition instances, which remain
  governed by the Organization Framework and the Agent Definition
  Framework, per their existing Department-nested convention.
- Knowledge, Memory, Trace, Agent Instance, or any other Canonical Domain
  Model entity.
- The individual document structure, mandatory fields, or validation
  model for Skill, Workflow, Runtime, or Tool instances. This document
  owns only the shared repository-location layer common to all four, not
  their individual documentation conventions.

## 3. Authority

This document is a Principle Document under Constitution §4, sibling to
the Organization Framework and the Agent Definition Framework. Changes to
this document's own document content are made through direct
Architect-approved documentation changes — not through the Architecture
Decision Record process, which governs only Domain Model semantic changes
(Constitution §3.4, §5).

This document's own content is a documentation and repository-organization
convention, not a governance-authority artifact. It does not introduce,
redefine, or contradict any Canonical Domain Model entity, relationship,
ownership rule, lifecycle rule, or invariant, per Constitution §6.2
invariant 3.

Ownership of this repository convention does not grant modification
authority, access authority, or operational permission over any
repository artifact. Repository access and permissions are governed
separately from, and are not affected by, this document's content.

## 4. Relationship to the Constitution

This document defines and alters no Constitutional authority. Any content
in this document — including its still-pending repository convention —
remains bound absolutely by Constitution §6.2 invariant 1's prohibition on
technology, language, framework, or infrastructure decisions in governance
documents.

## 5. Relationship to the Canonical Domain Model

The Canonical Domain Model is the sole semantic authority for what Skill,
Workflow, Runtime, and Tool are, their ownership, their relationships, and
their lifecycle. This document does not reproduce, restate, or paraphrase
that content anywhere. It references the Domain Model only as
justification for grouping these four entities as one governance
question: they share an identical Ownership Rule category (§5, "owned
centrally"), a shared Lifecycle Rule governance pattern (§6, established
across ADR-0004, ADR-0005, and ADR-0007), and direct compositional
relationships among themselves (§4). Where this document requires a fact
about these entities, it cites the Domain Model section that already
establishes it; it does not independently assert Domain Model semantics.

## 6. Relationship to the Organization Framework

This document exists because the Organization Framework's own
"Filesystem Projection of Domain Model Ownership" mechanism is built
around nesting an instance inside its owning Department's directory — a
mechanism that does not apply to centrally-owned entities, which by
definition have no owning Department.

This document is a sibling to the Organization Framework's own document,
both Principle Documents under Constitution §4. The Organization
Framework's own Repository Structure section carries a minimal,
corresponding reference to this document's existence (see the
synchronization proposal accompanying this draft), without the
Organization Framework itself absorbing this document's content.

## 7. Relationship to the Agent Definition Framework

The Agent Definition Framework's own Reference Conventions (§12) currently
treat Skill and Workflow as name-only references, noting neither has its
own framework or storage convention yet. Once this document's repository
convention is decided, and separately once individual Skill and Workflow
Frameworks exist, the Agent Definition Framework's §12 will require its
own synchronization pass. That synchronization is future work and is not
performed by this document.

## 8. Governed Entities

This document applies to repository artifacts representing instances of
Skill, Workflow, Runtime, and Tool, as defined exclusively by the
Canonical Domain Model (§2). This document does not define, restate, or
paraphrase what these entities are; it only establishes where and how
artifacts representing them are recorded, once that convention is
decided.

## 9. Governance Boundary — What This Document Does Not Yet Define

This document explicitly does not yet establish:

- Directory structure or repository location for Skill, Workflow,
  Runtime, or Tool instances.
- Naming or identifier conventions for instances of these entities.
- Cross-reference syntax between these entities.
- Any distinction in treatment between Runtime and Skill/Workflow/Tool.

These remain open, tracked in Section 10, pending a dedicated future
Architect decision. This document's role is limited to establishing that
such a decision, once made, is recorded here.

## 10. Open Questions

1. **Repository organization.** How Skill, Workflow, Runtime, and Tool
   instances are organized and referenced as repository artifacts —
   including their location, internal structure, and the cross-reference
   approach between them.
2. **Runtime's relationship to this convention.** Whether Runtime's lack
   of compositional relationship to Skill, Workflow, and Tool warrants
   different treatment within whatever repository organization is
   eventually chosen, or whether uniform treatment across all four
   remains correct.
3. **Relationship to individual entity Frameworks.** How individual
   Skill, Workflow, Runtime, and Tool Frameworks, once created, would
   relate to this document's shared convention — for example, whether
   they reference it directly or restate portions of it. This question
   does not address whether or when such Frameworks are built; that is
   separate planning work outside this document's scope.

## 11. Explicit Exclusions

This document does not, and may never:

- Redefine Skill, Workflow, Runtime, Tool, or any other Canonical Domain
  Model entity, relationship, ownership rule, or lifecycle rule.
- Create new governance authority, invariants, or lifecycle states beyond
  those already ratified.
- Select or implement a storage structure, naming convention, or
  reference syntax. These remain open per Section 10.
- Modify the Organization Framework's existing Department-nested
  convention for Capability or Agent Definition instances.
- Create a Skill Framework, Workflow Framework, Runtime Framework, Tool
  Framework, or any other Framework.
- Grant modification authority, access authority, or operational
  permission over any repository artifact. Repository access and
  permissions are governed separately.
- Name a specific technology, vendor, or model anywhere.

## 12. Status

This document establishes governance boundary and responsibility scope
only. No storage structure, naming convention, or reference syntax has
been defined. No Skill, Workflow, Runtime, or Tool instance currently
exists in the repository.
