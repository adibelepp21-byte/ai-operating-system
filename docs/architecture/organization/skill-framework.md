# Skill Framework

## 1. Purpose

This document defines how Skill instances are documented within AIOS: their required structure, mandatory and optional content, version representation, validation, and reference conventions.

This document does not define what a Skill is. That is defined exclusively in the Canonical Domain Model. This document never redefines, restates, or paraphrases that content; it only describes how already-ratified content is represented and recorded.

## 2. Scope

This framework governs the documentation of Skill instances only. It does not govern Agent Definitions, Agent Instances, Workflows, Tools, or Runtime — each, if given its own framework, is a separate document. It does not govern the shared repository-location boundary for Skill, Workflow, Runtime, and Tool, which remains governed exclusively by the Execution Artifact Repository Convention (EARC).

## 3. Authority

Skill lifecycle semantics — what creation, deprecation, versioning, and interface-preserving evolution mean for a Skill — are governed exclusively by Canonical Domain Model §5 (Ownership Rules) and §6 (Lifecycle Rules). This document holds no authority over, and does not restate, that semantic content.

This document's own authority is limited to how already-ratified lifecycle information is represented in documentation: which fields record it, how a Version History entry is structured, and how a documented change is distinguished as interface-preserving versus behaviorally material for recording purposes. It does not determine what lifecycle states exist, when a transition is valid, or what governs it — those determinations remain the Domain Model's alone.

This document's own content — structure, fields, validation, versioning convention, reference conventions — is a documentation and repository-organization convention, not a governance-authority artifact. It sits within the Principle Documents tier of Engineering Constitution §4, the same positioning as the Organization Framework, the Agent Definition Framework, and the Execution Artifact Repository Convention.

## 4. Relationship to the Constitution

This framework defines and alters no Constitutional authority. Any content in this document remains bound absolutely by Constitution §6.2's prohibitions — including invariant 1 (no technology, language, framework, or infrastructure decision in governance documents) and invariant 3 (no non-Domain-Model document may introduce, redefine, or contradict Domain Model content).

## 5. Relationship to the Canonical Domain Model

The Canonical Domain Model is the sole semantic authority for what a Skill is, its ownership, its relationships to Agent Definition, Agent Instance, Workflow, and Tool, and its invariants. This document does not reproduce, restate, or paraphrase that content anywhere below. Where this framework requires a field or a validation step, it cites the Domain Model section that already requires it; it does not independently assert the requirement.

## 6. Relationship to the Execution Artifact Repository Convention

Skill is one of four entities governed by the Execution Artifact Repository Convention's (EARC) shared repository-location boundary (EARC §2). This framework inherits, rather than duplicates, EARC's resolved decisions: the unified execution-entity directory, Skill's sibling grouping with Workflow and Tool, and the general Framework-relationship citation principle (EARC §9).

This framework does not itself decide, and does not attempt to decide, the specific directory name, repository path, instance naming convention, or identifier and cross-reference syntax that EARC leaves open (EARC §9, §10). Those remain separate governance decisions belonging exclusively to EARC. Where this document must refer to a Skill instance's storage location, it does so only in the abstract, pending those decisions.

## 7. Relationship to the Agent Definition Framework

The Agent Definition Framework treats Skill as a name-only reference (Agent Definition Framework §12), explicitly noting this as "a known, deliberate limitation, not an oversight." This framework's creation was the anticipated event that framework referenced. Agent Definition Framework §12 has since been synchronized to cite this Framework by name; that synchronization was carried out as a separate, direct Architect-approved documentation change to Agent Definition Framework, not performed by this document.

Agent Definition Framework §15 Open Architectural Question 3 (scope of "permissions") remains open. This framework does not resolve it, and no content below should be read as taking a position on whether Agent Definition permissions ever extend beyond Skill/Workflow authorization.

## 8. Document Structure Requirements

Every Skill document follows this structure:

1. Metadata
2. Purpose / Description
3. Interface
4. Permitted Invocation Context
5. Version History

This mirrors the Metadata-first, substantive-content, change-history-last pattern already established by the ADR Structure and the Agent Definition Framework's own Document Structure Requirements, for consistency.

## 9. Mandatory Document Fields

- **Name** — A documentation-level identifier used to reference this Skill document and distinguish it from other Skill documents across its version lineage. This field is a reference and record-keeping mechanism, not an assertion of Domain-Model-mandated semantic identity: Domain Model §2 does not enumerate a "named" requirement for Skill the way it does for Capability, and this document does not claim otherwise. The field exists because this framework's own documentation and reference conventions (Section 14) require some stable label to cite a Skill document by; it does not represent a Domain Model determination that Skill identity works this way.
- **Owning designation** — Skill is owned centrally (Domain Model §5), not by a Department. This field records that central-ownership status; it does not name an owning Department, since none exists for this entity.
- **Description** — what the discrete, bounded unit of executable ability does, per Domain Model §2. Stated only in the abstract; may not name a specific technology, vendor, or model (Domain Model §8, Constitution §6.2 invariant 1).
- **Interface** — A documentation field recording, for this specific Skill, the current representation of the boundary that Domain Model §6 refers to when it requires interface preservation across a version change. This field records what has been documented as this Skill's interface at a point in time; it does not define what "interface" means for a Skill as a class, does not establish criteria for what counts as interface-preserving versus interface-breaking, and does not interpret Domain Model §6 beyond citing that the requirement exists. Any semantic interpretation of "interface" remains governed exclusively by the Canonical Domain Model.
- **Version** — per Domain Model §6, "Versioned independently."

## 10. Optional Document Fields

- Supplementary notes or rationale.
- Cross-references to related Skills or Workflows that invoke it.
- A note on Tool(s) this Skill invokes (Domain Model §4: Skill invokes Tool), referenced by name only, consistent with Section 14 below.

## 11. Validation Model

- **Ownership validation** — the document correctly records central ownership; it does not declare an owning Department.
- **Interface-preservation validation** — a documented version change correctly distinguishes interface-preserving evolution from a behaviorally-material change requiring documentation at promotion time (Domain Model §6).
- **Boundary validation** — no technology, vendor, or model name appears anywhere in the document.
- **Scope validation** — no field in this document redefines Skill, asserts a position on Agent Definition Framework §15 Q3, or resolves the promotion-terminology question in Section 13, below.

## 12. Version Representation Convention

Per Domain Model §6, a Skill "may evolve as long as the interface is preserved," and "Skill/Tool version changes that alter behavior materially should be documented at promotion time, not just interface-checked."

This framework uses the term "promotion time" only in the sense already present in that Domain Model §6 text, describing when a Skill's version-history entry is documented. It does not resolve, and explicitly leaves open, whether this use of "promotion" is the same concept as the governed Memory-to-Knowledge promotion process (Domain Model §7 invariant 8) or a distinct, unrelated use of the same word. This ambiguity is recorded here as an open interpretive note, not resolved by this document — see Section 13.

Each Skill is recorded as a single, persistent document across its whole version lineage, with prior versions retained in its Version History section, consistent with the Domain Model's characterization of Skill as an entity "versioned independently" rather than as a series of discrete, individually-superseding records.

## 13. Explicitly Recorded Open Items

The following are known, unresolved matters this framework does not — and may not — resolve. Each is carried forward here as an open item, not a silently-assumed answer:

1. **"Promotion" terminology ambiguity.** Domain Model §6 requires that behaviorally-material Skill/Tool changes be "documented at promotion time." Domain Model §7 invariant 8 separately governs a distinct, specific "promotion" process for Memory becoming Knowledge, through governed review, never automatic. Whether the Skill/Tool lifecycle's use of "promotion time" refers to the same concept, a deliberately reused but distinct term, or an unrelated word choice, is not addressed anywhere in the ratified corpus. This framework uses the term only in citation of Domain Model §6's own language and takes no position on this question.
2. **Agent Definition Framework §15 Q3 — scope of "permissions."** Whether Agent Definition's declared permissions ever extend beyond Skill/Workflow authorization remains an open question belonging to the Agent Definition Framework and, ultimately, to the Domain Model. This framework's Permitted Invocation Context field (Section 8) describes only what invokes a given Skill; it does not address or resolve the broader permissions-scope question.
3. **EARC repository-location decisions.** The specific directory name, repository path, instance naming convention, and identifier/cross-reference syntax for Skill instances remain undefined, per EARC §9–§10. This framework does not decide them. Resolving them requires a separate EARC amendment — a distinct governance decision outside this document's scope.
4. **Agent Definition Framework §12 synchronization.** This framework's creation was the event that Agent Definition Framework §12 anticipated (per §7, above). Agent Definition Framework §12 has since been updated to reflect this framework's existence, through a separate, direct Architect-approved documentation change to that document — not performed by, or recorded as an amendment within, this document.

Any resolution of the above, in any direction, would require action outside this document — an ADR for items touching Domain Model semantics (Constitution §3.4, §5), or a separate Architect-approved amendment for items belonging to EARC or the Agent Definition Framework.

## 14. Reference Conventions

- **Skill** (self-reference, e.g. from another Skill document) — Until EARC resolves a formal identifier and cross-reference convention (Section 13, item 3), this framework provisionally references a Skill by name only. This is not a final identifier decision and does not establish a naming or identifier convention on this framework's own authority; it is a placeholder representation pending EARC's decision, which this framework inherits once made rather than anticipating or substituting for.
- **Tool** — reference by name only. A Tool Framework now exists (see `tool-framework.md`); this framework's own reference to Tool remains name-only pending the same EARC identifier and cross-reference decisions (Section 13, item 3) that govern this framework's other provisional references, not because no Tool Framework exists.
- **Workflow** — reference by name only, for the same reason.
- **Agent Definition** — reference by name and link to its Agent Definition Framework entry, where the reverse (Agent Definition → Skill) reference already exists per Agent Definition Framework §12.

## 15. Storage Convention

The specific repository path and file-naming convention for individual Skill instances are not defined here. They remain governed by the Execution Artifact Repository Convention, once EARC's own open items (directory name, path, naming, identifier convention) are resolved (see Section 13, item 3). This framework does not select or imply an instance storage location.

This framework document itself is recorded at `docs/architecture/organization/skill-framework.md`, a sibling to the Organization Framework, the Agent Definition Framework, and the Execution Artifact Repository Convention, consistent with the existing placement of Principle Documents within that directory.

## 16. Framework Ownership

Changes to this document follow the same ownership model already established by the Organization Framework and the Agent Definition Framework: procedural mechanics — document structure, fields, validation, versioning convention, reference conventions — are owned by this document and may be updated through direct Architect-approved documentation changes. Domain Model semantics — what a Skill, Tool, Workflow, Agent Definition, Agent Instance, or any other entity is, and their relationships and invariants — remain exclusively governed by the Canonical Domain Model and are never redefined by this document, regardless of how this document itself evolves.

## 17. Explicit Exclusions

This framework does not, and may never:

- Redefine Skill, Tool, Workflow, Agent Definition, Agent Instance, or any other Canonical Domain Model entity.
- Create new invariants, ownership rules, or lifecycle states beyond those already ratified.
- Create new governance authority.
- Resolve Agent Definition Framework §15 Q3 (scope of "permissions").
- Resolve the "promotion" terminology ambiguity described in Section 13.
- Decide EARC's open directory name, repository path, naming convention, or identifier/cross-reference syntax.
- Name a specific technology, vendor, or model anywhere.

## 18. Status

Ratified as an AIOS Principle Document. Approved by the System Architect.

Required safeguards remain active per the ratification authorization: EARC's open items (directory name, path, naming convention, identifier/cross-reference syntax) remain unresolved; the Agent Definition Framework §12 synchronization pass has since been completed, as a separate documentation change to that Framework, not by this document; the "promotion" terminology ambiguity (Section 13, item 1) remains unresolved; Agent Definition Framework §15 Q3 (Section 13, item 2) remains open.

No Skill instance currently exists in the repository.
