# Execution Artifact Repository Convention

## 1. Purpose

This document establishes the governance boundary and responsibility scope
for how Skill, Workflow, Runtime, and Tool instances are recorded within
AIOS as repository artifacts.

This document defines the shared repository-location convention for
these four entities. Directory structure, naming convention, and
reference syntax have since been resolved (see Section 9), following
the option-space evaluation originally identified in the Architecture
Discovery Report for this question. The literal canonical-key format
and the complete repository path beyond the directory name remain open,
pending a separate, future Architect decision. This document establishes
that the shared repository-location convention for these four entities
belongs here — rather than in the Organization Framework, or
independently invented by each entity's eventual individual Framework.

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
across ADR-0004 and ADR-0005), and direct compositional
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

The Agent Definition Framework's own Reference Conventions (§12)
previously treated Skill and Workflow as name-only references, noting
neither had its own framework or storage convention yet. Skill,
Workflow, and Runtime Frameworks have since been ratified, and Agent
Definition Framework §12 (and separately, §10) has since been
synchronized to reflect each — as separate, direct Architect-approved
documentation changes to that Framework, not performed by this document.
The Tool Framework has also since been ratified; Agent Definition
Framework has no direct relationship to Tool and requires no
corresponding synchronization, consistent with Agent Definition
Framework §15's own exclusion of any direct Agent-Definition-to-Tool
relationship. This document's own repository convention — directory
name, canonical identifier model, and reference syntax — has since been
resolved (see Section 9); the literal canonical-key format and the
complete repository path beyond the directory name remain undecided
(see Section 10).

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
  model: Skill, Workflow, Tool, and Runtime instances are organized
  using a symmetric grouping, labeled by which of the four governed
  entities — Skill, Workflow, Runtime, or Tool — each instance
  represents, with one grouping level applied identically and
  simultaneously to all four, and no one of the four nested more deeply
  than another. Skill, Workflow, and Tool are structurally grouped as
  siblings, reflecting the Workflow-contains-Skill and Skill-invokes-Tool
  relationships (Domain Model §4) that connect them. Runtime is likewise
  a direct sibling grouping, distinguished from the other three through
  its own label rather than through any difference in nesting depth,
  giving the Runtime treatment decision above expression in the
  repository structure itself. This placement does not constitute a
  separate top-level repository convention, and does not imply Runtime's
  participation in the Workflow/Skill/Tool compositional relationships,
  nor does it introduce, redefine, or imply any Domain Model entity
  relationship, hierarchy, or containment structure. A depth-nested
  alternative, which would have grouped Skill, Workflow, and Tool one
  level deeper than Runtime, was considered and rejected due to the risk
  of implying a containment hierarchy the Domain Model does not
  establish at that granularity; the governing concern remains
  asymmetric nesting that would imply such a hierarchy, not the presence
  of a grouping level applied symmetrically to all four.
- **Directory/path naming approach.** The unified execution-entity
  directory's name and repository path shall be derived from this
  document's own vocabulary and scope (Section 2), rather than directly
  reusing Canonical Domain Model category terminology. A Domain-Model-derived
  naming approach was considered and rejected: the Domain Model's own
  "Execution" category (§1) comprises six entities (Agent Definition,
  Agent Instance, Skill, Workflow, Tool, and Runtime), while this
  document governs exactly four; a name drawn directly from that
  category label would risk implying a broader scope than this
  Convention actually holds. The specific name is resolved below; the
  complete repository path beyond that name remains undefined.
- **Directory name.** The unified execution-entity directory is named
  `execution-catalog`, consistent with this document's own
  EARC-vocabulary-derived naming approach and selected over alternative
  EARC-vocabulary-consistent candidates on the basis of semantic
  precision, scalability, governance consistency, ambiguity risk, and
  implementation friendliness. This name does not reuse, and is not
  derived from, Canonical Domain Model category terminology.
- **Canonical identifier model.** Each Skill, Workflow, Runtime, and Tool
  instance is identified by a stable, human-readable canonical key that
  remains fixed for the life of the instance, independent of its Display
  Name and its repository location. The canonical key is a
  documentation-level representation and citation mechanism only; it
  does not define, redefine, or substitute for entity identity or entity
  continuity, which remain governed exclusively by the Canonical Domain
  Model (§6). Canonical key uniqueness is scoped separately for each of
  the four governed entities — Skill, Workflow, Runtime, and Tool — such
  that uniqueness is required within each entity's own set of instances,
  not across all four collectively. Section 2 directly establishes that
  these four entities, individually named, are this document's governed
  scope; scoping canonical-key uniqueness to each of them separately is
  an architectural approach inferred from that governed-entity
  structure, not a requirement directly enumerated by Section 2 itself.
  The literal format of the canonical key is deferred to a separate,
  later amendment-level decision (see "Not Yet Defined," below).
- **Reference model.** The canonical key is the authoritative reference
  identity for citing a Skill, Workflow, Runtime, or Tool instance from
  another document. A relative Markdown link to the instance's current
  repository location may additionally be included as a navigation
  convenience; such a link is derived from, and subordinate to, the
  canonical key, never the source of truth for identity. The mechanism
  by which a canonical key is resolved to a repository location is not a
  governance concern of this document.
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
  Convention, the Skill Framework, the Workflow Framework, the Runtime
  Framework, and the Tool Framework.

### Not Yet Defined

This document still does not establish:

- The literal format of the canonical key established above ("Canonical
  identifier model"). Deferred to a separate, later amendment-level
  decision, pending future operational evidence and/or the first real
  entity Framework proposal, consistent with Constitution §8.
- How specific Frameworks apply the citation-only principle recorded
  above. The Skill Framework's, Workflow Framework's, Runtime
  Framework's, and Tool Framework's ratifications have each demonstrated
  the general citation discipline documented in Section 9's "Citation
  discipline for future Frameworks" entry, closing this verification
  condition for all four entities this document governs. This closure
  is separate from, and does not resolve, the literal canonical-key
  format item above, which remains open.

This remains open, tracked in Section 10, pending a dedicated future
Architect decision. This document's role is limited to establishing that
such a decision, once made, is recorded here.

## 10. Open Questions

1. **Repository organization specifics — CLOSED.** The specific
   directory name (`execution-catalog`), the canonical identifier model,
   the reference model, and the internal organization model (a symmetric
   grouping labeled by governed entity) have been resolved (see Section
   9, "Resolved," above). This closure does not resolve the literal
   format of the canonical key, which remains open, tracked in Section 9
   ("Not Yet Defined").
2. **Framework-specific application of the citation-only principle.**
   The general principle that Skill, Workflow, Runtime, and Tool
   Frameworks inherit this Convention's decisions by citation rather
   than restatement is resolved (see Section 9). Skill Framework,
   Workflow Framework, Runtime Framework, and Tool Framework have each
   since been ratified and have each demonstrated this principle in
   practice, closing this specific verification question (see Section
   9's "Citation discipline for future Frameworks" entry). This closure
   does not resolve, and is separate from, Open Question 1 above
   (directory name, repository path, naming convention, and identifier
   convention), which remain open.

## 11. Explicit Exclusions

This document does not, and may never:

- Redefine Skill, Workflow, Runtime, Tool, or any other Canonical Domain
  Model entity, relationship, ownership rule, or lifecycle rule.
- Create new governance authority, invariants, or lifecycle states beyond
  those already ratified.
- Select or implement the literal canonical-key format or the complete
  repository path beyond the directory name resolved in Section 9.
  These remain open per Section 10.
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
directory, named `execution-catalog` — Runtime's differentiated
treatment within that approach, the internal organization model (a
symmetric grouping labeled by governed entity), the directory/path
naming approach (convention-derived), the canonical identifier model,
the reference model, and the general Framework relationship principle
(citation rather than restatement) have been resolved (see Section 9).

The literal format of the canonical key and the complete repository
path beyond the directory name remain undefined (see Section 10). The
Framework-specific application of the citation-only principle has
separately been closed (see Section 10, Open Question 2).

No Skill, Workflow, Runtime, or Tool instance currently exists in the
repository.
