# Execution Artifact Repository Convention

## 1. Purpose

This document establishes the governance boundary and responsibility scope
for how Skill, Workflow, Runtime, and Tool instances are recorded within
AIOS as repository artifacts.

This document defines the shared repository-location convention for
these four entities. Directory structure, naming convention, and
reference syntax have since been resolved (see Section 9), following
the option-space evaluation originally identified in the Architecture
Discovery Report for this question. The literal canonical-key format and the complete repository path
beyond the directory name have since been resolved (see Section 9).
This document establishes
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
in this document — including its resolved repository convention and any
future amendment to it — remains bound absolutely by Constitution §6.2
invariant 1's prohibition on technology, language, framework, or
infrastructure decisions in governance documents.

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
name, canonical identifier model, reference syntax, canonical key
format, and repository path — has since been fully resolved (see
Section 9).

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
  Convention actually holds. The specific name and the complete
  repository path are both resolved below.
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
- **Canonical key format.** The canonical key for a Skill, Workflow,
  Runtime, or Tool instance takes the form `<entity-type>.<stable-name-slug>`,
  where `<entity-type>` is one of the entities currently governed by
  this document (§2) — `skill`, `workflow`, `runtime`, or `tool` — and
  `<stable-name-slug>` is a stable, human-readable label for the
  instance. Examples: `skill.example-skill`, `workflow.example-workflow`,
  `runtime.example-runtime`, `tool.example-tool`. This format is
  independent of its Display Name, independent of its repository
  location, and independent of its filename; it is a documentation
  reference identity only and does not define, redefine, or substitute
  for the entity identity the Canonical Domain Model establishes (§6).
  Canonical key stability is not the same as, and is never proof of,
  entity identity continuity: a canonical key may be retained across a
  documented change to the instance only to the extent that change
  constitutes interface-preserving evolution of the same entity, as
  Domain Model §6 defines it; a change that Domain Model §6 treats as
  producing a distinct entity is outside this format's stability
  guarantee, and this document takes no position on when that threshold
  is crossed — that determination remains exclusively the Canonical
  Domain Model's. Slug normalization rules and filename rules are not
  established by this format and remain a separate, later
  instance-convention decision.
- **Repository path.** The unified execution-entity directory (named
  `execution-catalog`, per the Directory name decision above) is
  located at `docs/architecture/organization/execution-catalog/`.
  Within it, the symmetric, governed-entity-labeled grouping already
  established (see Internal organization model, above) takes the form
  of one subdirectory per governed entity — `skill/`, `workflow/`,
  `runtime/`, `tool/` — applied identically and simultaneously to all
  four, consistent with, and not a modification of, that grouping
  decision. This placement does not introduce, redefine, or imply any
  Domain Model entity hierarchy, and does not change Skill, Workflow,
  Runtime, or Tool ownership as established by Domain Model §5.
  Physical containment within `docs/architecture/organization/` does
  not grant the Organization Framework ownership, authority, or
  governance over Skill, Workflow, Runtime, or Tool instances; does not
  place `execution-catalog` under Department governance; and does not
  create a parent-child governance relationship between the
  Organization Framework and this document. Repository containment is
  not governance ownership and does not establish a Domain Model
  relationship. EARC's own authority over the repository convention for
  these four entities (§2, §3) is unchanged by sharing a parent
  directory with the Organization Framework's own document;
  Organization Framework's authority remains limited to Department
  structure, per its own scope.
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

No unresolved item remains among the repository convention decisions
addressed by this amendment — the canonical identifier model, reference
model, directory name, repository path, canonical key format, and
internal organization model are each resolved (see Section 9,
"Resolved," above, as amended). This does not foreclose this document
ever containing a future open item; it reflects only the current state
of the decisions tracked in this section as of this amendment. The
Framework-specific application of the citation-only principle recorded
above was separately closed in a prior amendment: the Skill Framework's,
Workflow Framework's, Runtime Framework's, and Tool Framework's
ratifications have each demonstrated the general citation discipline
documented in this section's "Citation discipline for future
Frameworks" entry (see Section 10, Open Question 2).

Slug normalization rules and filename conventions for canonical keys
remain a separate, later instance-convention decision, not established
by this document (see Section 11).

## 10. Open Questions

1. **Repository organization specifics — CLOSED.** The specific
   directory name (`execution-catalog`), the complete repository path
   (`docs/architecture/organization/execution-catalog/`), the canonical
   identifier model, the canonical key format, the reference model, and
   the internal organization model (a symmetric grouping labeled by
   governed entity, expressed as one subdirectory per entity —
   `skill/`, `workflow/`, `runtime/`, `tool/`) have all been resolved
   (see Section 9, "Resolved," above). No item remains open under this
   question.
2. **Framework-specific application of the citation-only principle.**
   The general principle that Skill, Workflow, Runtime, and Tool
   Frameworks inherit this Convention's decisions by citation rather
   than restatement is resolved (see Section 9). Skill Framework,
   Workflow Framework, Runtime Framework, and Tool Framework have each
   since been ratified and have each demonstrated this principle in
   practice, closing this specific verification question (see Section
   9's "Citation discipline for future Frameworks" entry). This closure
   is separate from Open Question 1 above, which has itself since been
   closed (see item 1).

## 11. Explicit Exclusions

This document does not, and may never:

- Redefine Skill, Workflow, Runtime, Tool, or any other Canonical Domain
  Model entity, relationship, ownership rule, or lifecycle rule.
- Create new governance authority, invariants, or lifecycle states beyond
  those already ratified.
- Select or implement slug normalization rules or filename conventions
  for canonical keys. These remain open, deferred to a separate, later
  instance-convention decision (see Section 9).
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
the canonical key format, the reference model, the repository path,
and the general Framework relationship principle (citation rather than
restatement) have all been resolved (see Section 9).

The Framework-specific application of the citation-only principle has
separately been closed (see Section 10, Open Question 2). Slug
normalization rules and filename conventions for canonical keys remain
a separate, later instance-convention decision, not yet defined (see
Section 9, Section 11).

No Skill, Workflow, Runtime, or Tool instance currently exists in the
repository.
