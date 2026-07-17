# Agent Definition Framework

## 1. Purpose

This document defines how Agent Definitions are documented within AIOS:
their required structure, mandatory and optional content, version
representation, validation, and storage.

This document does not define what an Agent Definition is. That is
defined exclusively in the Canonical Domain Model. This document never
redefines, restates, or paraphrases that content; it only describes how
already-ratified content is represented and recorded.

## 2. Scope

This framework governs the documentation of Agent Definition instances
only. It does not govern Agent Instances, Skills, Workflows, Tools, or
Runtime — each, if ever given its own framework, would be a separate
document. It does not govern Department or Capability instances, which
remain governed by the Organization Framework.

## 3. Authority

Agent Definition creation, deprecation, and lifecycle authority is
governed exclusively by Canonical Domain Model §6 (Lifecycle Rules),
which places this authority at Department discretion within Capability
governance. This is consistent with Constitution §3.3's Implementation
Tier, though that consistency is this document's own interpretation, not
a direct textual statement in §3.3 itself; Domain Model §6 remains the
direct and sufficient source this document relies on. This document does
not restate that authority; it only describes how the resulting Agent
Definitions are documented once created.

This document's own content — structure, fields, validation, versioning
convention, storage — is a documentation and repository-organization
convention, not a governance-authority artifact. It sits within the
Principle Documents tier of Engineering Constitution §4, the same
positioning as the ADR Framework and the Organization Framework.

## 4. Relationship to the Constitution

This framework defines and alters no Constitutional authority. Decision
tiers, delegation, and the AI Collaboration Principles governing both
meta-level contributors and operational agents remain governed
exclusively by Constitution §3 and §14. Any content in this framework
touching Runtime requirements is bound absolutely by Constitution §6.2's
prohibition on technology, language, framework, or infrastructure
decisions in governance documents — without exception, and without a
carve-out for Agent Definition despite Runtime being the entity where
this constraint is most tempting to relax.

## 5. Relationship to the Canonical Domain Model

The Canonical Domain Model is the sole semantic authority for what an
Agent Definition is, its ownership, its relationships to Department,
Capability, Skill, Workflow, Runtime, and Trace, and its invariants. This
document does not reproduce, restate, or paraphrase that content anywhere
below. Where this framework requires a field or a validation step, it
cites the Domain Model section that already requires it; it does not
independently assert the requirement.

## 6. Relationship to the Organization Framework

This framework extends, rather than duplicates, the Organization
Framework's repository structure. Agent Definition instances are
recorded nested within their owning Department's existing directory,
alongside that Department's Capabilities. This framework document is a
sibling to the Organization Framework's own document, both Principle
Documents under Constitution §4. Where the Organization Framework already
states a convention (naming, no-synthetic-identifier policy), this
document follows it rather than restating it independently.

## 7. Document Structure Requirements

Every Agent Definition document follows this structure:

1. Metadata
2. Purpose / Description
3. Owning Department
4. Implemented Capability
5. Behavior and Permissions
6. Permitted Skills
7. Permitted Workflows
8. Runtime Requirements
9. Version History

This mirrors the Metadata-first, substantive-content, change-history-last
pattern already established by the ADR Structure, for consistency.

## 8. Mandatory Document Fields

The following fields are mandatory. Seven originate directly from the
Canonical Domain Model's own Agent Definition entry (§2), which names
each as a constituent part of what the entity is — this framework
enumerates them, it does not invent them. The eighth, Name, is grounded
differently; see below.

- **Name** — the Agent Definition's stable identity across its version
  lineage. This is not a term §2 uses directly for Agent Definition
  (contrast Capability's own definition, which explicitly uses the word
  named). It is required on architectural-identity and citability
  grounds instead: invariant 2's ownership counting and §2.1's Trace
  requirement to reference the specification in effect both presuppose a
  stable way to individually identify an Agent Definition. This field's
  grounding is therefore inferential, not a direct §2 enumeration.
- **Owning Department** — exactly one, per Domain Model §5 (Ownership
  Rules) and §7 invariant 2.
- **Implemented Capability** — at least one, per §7 invariant 2.
- **Behavior and Permissions** — what the class of Agent does and is
  authorized to do, per §2.
- **Permitted Skills** — Agent Definition is permitted to use only the
  Skills it specifies, per the specifies relationship in Domain Model
  §4. Per Domain Model §7 invariant 15, Permitted Skills may contain
  zero entries; an empty declaration is a valid architectural state, and
  no minimum cardinality is required.
- **Permitted Workflows** — same treatment as Skills, per the same §4
  relationship. Per Domain Model §7 invariant 15, Permitted Workflows
  may contain zero entries; an empty declaration is a valid
  architectural state, and no minimum cardinality is required.
- **Runtime Requirements** — stated only in the abstract. Per Domain
  Model §8, Runtime and Tool are the only entities permitted to name
  specific technology, vendors, or models; this field may never do so.
- **Version** — per §6, "Versioned."

## 9. Optional Document Fields

The following are framework conveniences, not required by the Domain
Model, and must be clearly distinguished from the mandatory fields above:

- Supplementary notes or rationale.
- Cross-references to related Agent Definitions.
- A "superseded by" pointer, used only if this entire Agent Definition —
  not a version of it — is retired in favor of a differently-named Agent
  Definition. This does not apply to ordinary version progression, which
  is recorded in Version History, not through this field.

## 10. Validation Model

- **Ownership validation** — the declared owning Department exists, per
  its Organization Framework entry.
- **Capability validation** — the declared implemented Capability exists
  and is owned by a real Department. Whether it must be the same
  Department that owns the Agent Definition is an open question — see
  Section 15.
- **Skill reference validation** — a Skill Framework now exists (see
  `skill-framework.md`), but instance-level validation remains
  provisional: no Skill instances exist yet, and the storage,
  identifier, and naming conventions such validation would depend on
  remain governed by EARC and unresolved (EARC §9–§10). This check's
  absence is not a defect in this framework, and nothing here resolves
  those EARC decisions. Per Domain Model §7 invariant 15, zero Skills is
  a valid state; once this validation becomes operative, it must
  recognize this as compliant, not flag it as incomplete.
- **Workflow reference validation** — a Workflow Framework now exists
  (see `workflow-framework.md`), but instance-level validation remains
  provisional: no Workflow instances exist yet, and the storage,
  identifier, and naming conventions such validation would depend on
  remain governed by EARC and unresolved (EARC §9–§10). This check's
  absence is not a defect in this framework, and nothing here resolves
  those EARC decisions. Per Domain Model §7 invariant 15, zero Workflows
  is a valid state; once this validation becomes operative, it must
  recognize this as compliant, not flag it as incomplete.
- **Version validation** — the documented version correctly indicates
  which Capability state it aligns with, per the convention in Section
  11.
- **Boundary validation** — no technology, vendor, or model name appears
  anywhere in the document.

## 11. Version Representation Convention

Per Domain Model §6, an Agent Definition's version is bound to the
Capability contract version it implements. The Domain Model does not
establish that Capability itself carries a formal version number — its
Lifecycle Rules table marks Knowledge, Skill/Tool, and Agent Definition
as "Versioned," and does not mark Capability the same way.

Because of this, an Agent Definition's Version History entries document
which Capability state they align with by referencing the Architecture
Decision Record that most recently defined or changed the governing
Capability, rather than presuming an independent Capability version
number the Domain Model does not establish. This is a procedural
workaround using an already-ratified mechanism (ADR references), not a
resolution of the underlying gap — see Section 15.

Each Agent Definition is recorded as a single, persistent document across
its whole version lineage — not as a separate file per version — with
prior versions retained in its Version History section. This is
consistent with the Domain Model's characterization of Agent Definition
as an evolving, versioned specification, rather than as a series of
discrete, individually-superseding records the way ADRs are.

## 12. Reference Conventions

- **Department** — reference by name and link to its Organization
  Framework entry.
- **Capability** — reference by name and link to its Capability file
  under the owning Department's `capabilities/` directory.
- **Skill** — reference by name only. A Skill Framework now exists (see
  `skill-framework.md`), but individual Skill instance storage location,
  naming convention, and identifier/cross-reference syntax remain
  undefined pending the Execution Artifact Repository Convention (EARC
  §9–§10); no Skill instances currently exist. This treatment may be
  strengthened once those EARC decisions are made.
- **Workflow** — reference by name only. A Workflow Framework now exists
  (see `workflow-framework.md`), but individual Workflow instance
  storage location, naming convention, and identifier/cross-reference
  syntax remain undefined pending the Execution Artifact Repository
  Convention (EARC §9–§10); no Workflow instances currently exist. This
  treatment may be strengthened once those EARC decisions are made.
- **Runtime** — described only as an abstract requirement. Never a
  specific technology, vendor, or model name, per Domain Model §8 and
  Constitution §6.2.

## 13. Storage Convention

This framework document is recorded at
`docs/architecture/organization/agent-definitions.md`, a sibling to the
Organization Framework's own document.

Agent Definition instances are recorded at:

```
docs/architecture/organization/<department-slug>/agent-definitions/<agent-definition-slug>.md
```

nested inside the owning Department's existing directory, alongside its
`capabilities/` directory, per the Organization Framework's established
per-Department structure. Naming follows the Organization Framework's
existing convention: lowercase, hyphenated slugs. No synthetic
identifier is used — consistent with the Organization Framework's
identifier policy, the Agent Definition's name is its identifier; version
is a separate, distinct field, not a distinct identifier.

## 14. Framework Ownership

Changes to this document follow the same ownership model already
established by the ADR Framework: procedural mechanics — document
structure, fields, validation, versioning convention, storage — are
owned by this document and may be updated through direct
Architect-approved documentation changes. Domain Model semantics — what
an Agent Definition, Capability, Department, Skill, Workflow, Runtime, or
Trace is, and their relationships and invariants — remain exclusively
governed by the Canonical Domain Model and are never redefined by this
document, regardless of how this document itself evolves.

## 15. Explicit Exclusions

This framework does not, and may never:

- Redefine Agent Definition, Capability, Department, Runtime, Skill,
  Workflow, or Trace. All are defined exclusively in the Canonical Domain
  Model.
- Create new invariants, ownership rules, or lifecycle states beyond
  those already ratified.
- Create new governance authority. Agent Definition creation and
  deprecation remain Department discretion within Capability governance,
  per Domain Model §6 — consistent with, though not directly established
  by, Constitution §3.3's Implementation Tier, per the same interpretive
  distinction drawn in Section 3 — unchanged by this document.
- Include Agent Instance runtime content, execution state, or Trace
  content. These belong exclusively to Agent Instance and Trace.
- State or imply a direct Agent-Definition-to-Tool relationship. The
  Domain Model's only ratified path to Tool is through Skill.
- Name a specific technology, vendor, or model anywhere.

### Open Architectural Questions

The following are known, unresolved gaps in the ratified Domain Model
that this framework cannot resolve, because doing so would assert new
Domain Model semantics reserved to that document alone (Constitution
§6.2 invariant 3). Each is carried forward here as an open question, not
a silently-assumed answer:

1. **Capability versioning.** Whether Capability itself should carry a
   formal version number, to make "the Capability contract version"
   (Domain Model §6) fully precise rather than approximated through ADR
   references (Section 11).
2. **Cross-Department Capability implementation.** Whether an Agent
   Definition may implement a Capability owned by a different Department
   than the one owning the Agent Definition. The Domain Model is silent;
   this framework adopts no binding position.
3. **Scope of "permissions."** Whether Agent Definition's declared
   permissions may ever extend beyond Skill/Workflow authorization —
   for example, into Knowledge or Memory access scoping, which the
   Domain Model currently attaches only to Agent Instance, not Agent
   Definition.
4. **Department transfer.** Whether an existing Agent Definition's
   owning Department can ever change outside of version evolution. The
   Domain Model does not address this.
5. **Minimum Skill/Workflow count.** Resolved by ADR-0007 — see Domain
   Model §7 invariant 15. An Agent Definition may specify zero or more
   Skills and zero or more Workflows; no minimum cardinality is required
   for either.

Any of the remaining open questions above, if resolved, would require a
Canonical Domain Model Architecture Decision Record — never a change to
this framework alone.
