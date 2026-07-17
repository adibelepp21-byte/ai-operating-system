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

## 9. Governance Boundary — Resolved and Remaining Decisions

### Resolved

The Architect has approved the following:

- **Repository organization approach.** Skill, Workflow, Runtime, and
  Tool instances are organized within a single, unified execution-entity
  directory, rather than separate directories per entity or another
  structural approach.
- **Runtime treatment.** Runtime receives differentiated treatment within
  this shared convention. Runtime remains one of the four entities
  governed by this document and is recorded within the same unified
  directory as Skill, Workflow, and Tool; its treatment must not
  represent or imply that Runtime participates in the
  Workflow-contains-Skill or Skill-invokes-Tool compositional
  relationships (Domain Model §4), which it does not share. Runtime
  hosts Agent Instance (§4) — a relationship structurally distinct from
  composition.
- **Internal organization model.** Within the unified execution-entity
  directory, the internal organization follows a Runtime-distinguished
  model, implemented as a flat, sibling-level structure: Skill, Workflow,
  Tool, and Runtime each occupy a direct sibling position within the
  unified directory, with no additional nesting depth introduced for any
  of the four. Skill, Workflow, and Tool are structurally grouped as
  siblings, reflecting the Workflow-contains-Skill and Skill-invokes-Tool
  relationships (Domain Model §4) that connect them. Runtime is likewise
  a direct sibling, distinguished from the other three through labeling
  rather than through nesting depth, giving the Runtime treatment
  decision above expression in the repository structure itself. This
  placement does not constitute a separate top-level repository
  convention, and does not imply Runtime's participation in the
  Workflow/Skill/Tool compositional relationships. A depth-nested
  alternative, which would have grouped Skill, Workflow, and Tool one
  level deeper than Runtime, was considered and rejected due to the risk
  of implying a containment hierarchy the Domain Model does not
  establish at that granularity.
- **Directory/path naming approach.** The unified execution-entity
  directory's name and repository path shall be derived from this
  document's own vocabulary and scope (Section 2), rather than directly
  reusing Canonical Domain Model category terminology. A Domain-Model-derived
  naming approach was considered and rejected: the Domain Model's own
  "Execution" category (§1) comprises six entities (Agent Definition,
  Agent Instance, Skill, Workflow, Tool, and Runtime), while this
  document governs exactly four; a name drawn directly from that
  category label would risk implying a broader scope than this
  Convention actually holds. The specific name and path remain
  undefined, below.
- **Framework relationship — general principle.** Future Skill,
  Workflow, Runtime, and Tool Frameworks, once created, shall inherit
  this Convention's decisions by citation rather than by restatement,
  wherever this Convention already defines the canonical rule. This is a
  procedural principle only; it does not define how any specific future
  Framework applies it, and Framework-specific application remains
  deferred until a real Framework proposal exists (see Section 10).
- **Citation discipline for future Frameworks.** Any future Skill,
  Workflow, Runtime, or Tool Framework, and any other future Principle
  Document, satisfies Constitution §6.2 invariant 3 by citing — never
  restating or paraphrasing — the Constitution, the Canonical Domain
  Model, and any other Principle Document wherever it relies on content
  those documents already establish. Where a Framework's own field or
  requirement is grounded only inferentially, rather than by direct
  textual enumeration in the Domain Model, the Framework should say so
  explicitly, rather than presenting an inferential grounding as if it
  were a direct citation. This records no new authority; it documents,
  for future Framework authors, the discipline already demonstrated by
  the Organization Framework, the Agent Definition Framework, this
  Convention, the Skill Framework, and the Workflow Framework.

### Not Yet Defined

This document still does not establish:

- The specific directory name or repository path for the unified
  execution-entity directory. The naming approach itself is resolved
  (see Resolved, above); the literal name and path are not.
- A shared naming convention for instances of these entities.
  Intentionally deferred: this decision is coupled with the
  still-undecided identifier convention, below, and deciding one without
  the other risks an inconsistent outcome.
- An identifier convention and cross-reference syntax for these
  entities. Deferred pending future operational evidence and/or the
  first real entity Framework proposal, consistent with Constitution §8.
- How any specific future Runtime or Tool Framework applies the
  citation-only principle recorded above. The Skill Framework's and
  Workflow Framework's ratifications each provided triggering evidence
  this item anticipated, and the general citation discipline is now
  documented in Section 9's "Citation discipline for future Frameworks"
  entry, demonstrated in practice by both. Each future Framework must
  still follow that principle; this item remains open only insofar as
  Runtime and Tool Frameworks have not yet been created to confirm the
  general discipline holds for them in practice.

These remain open, tracked in Section 10, pending dedicated future
Architect decisions. This document's role is limited to establishing that
such decisions, once made, are recorded here.

## 10. Open Questions

1. **Repository organization specifics.** Within the approved unified
   execution-entity directory, its approved convention-derived naming
   approach, and its approved flat, Runtime-distinguished internal
   organization model (see Section 9), the following remain open: (a)
   the specific directory name and repository path; (b) a shared naming
   convention for instances of these entities — intentionally deferred
   because it is coupled with the still-undecided identifier convention,
   below; (c) an identifier convention and cross-reference syntax —
   deferred pending future operational evidence and/or the first real
   entity Framework proposal.
2. **Framework-specific application of the citation-only principle.**
   The general principle that future Skill, Workflow, Runtime, and Tool
   Frameworks inherit this Convention's decisions by citation rather
   than restatement is resolved (see Section 9). How any specific future
   Framework applies that principle in practice remains open, deferred
   until a real Framework proposal exists. This question does not
   address whether or when such Frameworks are built; that is separate
   planning work outside this document's scope.

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

This document establishes governance boundary and responsibility scope.

The repository organization approach — a unified execution-entity
directory — Runtime's differentiated treatment within that approach, the
internal organization model (a flat, Runtime-distinguished structure),
the directory/path naming approach (convention-derived), and the general
Framework relationship principle (citation rather than restatement) have
been resolved (see Section 9).

The specific directory name, repository path, instance naming
convention, identifier convention, cross-reference syntax, and the
Framework-specific application of the citation-only principle remain
undefined (see Section 10).

No Skill, Workflow, Runtime, or Tool instance currently exists in the
repository.
