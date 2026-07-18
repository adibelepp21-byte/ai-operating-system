# Tool Framework

## 1. Purpose

This document defines how Tool instances are documented within AIOS: their required structure, mandatory and optional content, version representation, validation, and reference conventions.

This document does not define what a Tool is. That is defined exclusively in the Canonical Domain Model. This document never redefines, restates, or paraphrases that content; it only describes how already-ratified content is represented and recorded.

## 2. Scope

This framework governs the documentation of Tool instances only. It does not govern Agent Definitions, Agent Instances, Skills, Workflows, or Runtime — each, if given its own framework, is a separate document. It does not govern the shared repository-location boundary for Skill, Workflow, Runtime, and Tool, which remains governed exclusively by the Execution Artifact Repository Convention (EARC).

## 3. Authority

Tool lifecycle semantics — what versioning, governed revision, and interface-preserving evolution mean for a Tool — are governed exclusively by Canonical Domain Model §5 (Ownership Rules) and §6 (Lifecycle Rules). This document holds no authority over, and does not restate, that semantic content.

This document's own authority is limited to how already-ratified lifecycle information is represented in documentation: which fields record it, how a Version History entry is structured, and how a documented change is distinguished as interface-preserving versus behaviorally material for recording purposes. It does not determine what lifecycle states exist, when a transition is valid, or what governs it — those determinations remain the Domain Model's alone.

Tool's exclusivity as the only entity type permitted to hold a direct external/vendor dependency is governed exclusively by Canonical Domain Model §7 invariant 12. This document cites that invariant; it does not restate, interpret, or expand it.

This document's own content — structure, fields, validation, versioning convention, reference conventions — is a documentation and repository-organization convention, not a governance-authority artifact. It sits within the Principle Documents tier of Engineering Constitution §4, the same positioning as the Organization Framework, the Agent Definition Framework, the Execution Artifact Repository Convention, the Skill Framework, the Workflow Framework, and the Runtime Framework.

## 4. Relationship to the Constitution

This framework defines and alters no Constitutional authority. Any content in this document remains bound absolutely by Constitution §6.2's prohibitions — including invariant 1 (no technology, language, framework, or infrastructure decision in governance documents) and invariant 3 (no non-Domain-Model document may introduce, redefine, or contradict Domain Model content).

Constitution §13 (Security Principles) separately addresses Tool boundary exclusivity. This document cites that provision as additional Constitutional grounding for Tool's distinct status among Execution-layer entities; it does not restate, interpret, or expand §13's content, and does not treat this citation as granting any authority beyond what §13 itself already establishes.

## 5. Relationship to the Canonical Domain Model

The Canonical Domain Model is the sole semantic authority for what a Tool is, its ownership, its relationships to Agent Instance and Skill, and its invariants — including invariant 12, its exclusive external/vendor-dependency permission. This document does not reproduce, restate, or paraphrase that content anywhere below. Where this framework requires a field or a validation step, it cites the Domain Model section that already requires it; it does not independently assert the requirement.

## 6. Relationship to the Execution Artifact Repository Convention

Tool is one of four entities governed by the Execution Artifact Repository Convention's (EARC) shared repository-location boundary (EARC §2). This framework inherits, rather than duplicates, EARC's resolved decisions: the unified execution-entity directory, Tool's sibling grouping with Skill and Workflow — reflecting the Skill-invokes-Tool relationship named in EARC's own grouping rationale (EARC §9) — and the general Framework-relationship citation principle (EARC §9, including its "Citation discipline for future Frameworks" entry).

This framework does not itself decide, and does not attempt to decide, EARC's own repository-location convention; that convention belongs exclusively to EARC. Per EARC §9, as amended by EARC Amendment v1.1, Tool instances are identified by a canonical key of the form `tool.<stable-name-slug>` and recorded within the unified execution-entity directory, located at `docs/architecture/organization/execution-catalog/tool/`. Slug normalization rules and filename conventions for individual Tool instances remain a separate, later instance-convention decision, not established by EARC or by this document. Where this document must refer to a Tool instance's storage location or identity in concrete terms beyond the resolved canonical key format and repository path, it does so only in the abstract, pending that remaining decision.

## 7. Relationship to the Agent Definition Framework

The Agent Definition Framework does not reference Tool directly. Its own Explicit Exclusions (Agent Definition Framework §15) state that the Domain Model's only ratified path to Tool is through Skill, and that Agent Definition Framework may never state or imply a direct Agent-Definition-to-Tool relationship. Consistent with this, Agent Definition Framework §12 (Reference Conventions) and §10 (Validation Model) contain no Tool-related entry.

This framework's ratification does not create, and does not require, any synchronization to the Agent Definition Framework. No relationship exists between the two documents beyond both being Principle Documents under Constitution §4.

## 8. Document Structure Requirements

Every Tool document follows this structure:

1. Metadata
2. Purpose / Description
3. Interface
4. Version History

This mirrors the Metadata-first, substantive-content, change-history-last pattern already established by the ADR Structure and the Agent Definition Framework's, Skill Framework's, Workflow Framework's, and Runtime Framework's own Document Structure Requirements, for consistency. This structure follows the Skill Framework's shape rather than Workflow Framework's or Runtime Framework's, since Tool shares Skill's Domain Model §6 lifecycle wording ("interface preserved"... "documented at promotion time"), not Workflow's or Runtime's "compatibility boundaries... where applicable" wording. Unlike Skill Framework, Workflow Framework, and Runtime Framework, no relationship field is included in this structure or in Section 9, below: Domain Model §4 gives Tool no outgoing relationship of its own — Tool is invoked by Agent Instance and by Skill, but does not invoke, contain, or host anything itself. Consistent with the established pattern across all three precedents, incoming "invoked by" relationships are documented only as optional cross-references (Section 10), never as mandatory fields.

## 9. Mandatory Document Fields

- **Name** — a documentation-level identifier used to reference this Tool document and distinguish it from other Tool documents across its version lineage. This field is a reference and record-keeping mechanism, not an assertion of Domain-Model-mandated semantic identity: Domain Model §2 does not enumerate a "named" requirement for Tool the way it does for Capability, and this document does not claim otherwise. The field exists because this framework's own reference conventions (Section 14) require some stable label to cite a Tool document by; it does not represent a Domain Model determination that Tool identity works this way.
- **Owning designation** — Tool is owned centrally (Domain Model §5), grouped with Skill and Runtime, not by a Department. This field records that central-ownership status; it does not name an owning Department, since none exists for this entity.
- **Description** — what the integration point provides, per Domain Model §2. Stated only in the abstract; may not name a specific technology, vendor, or model — see Section 17.
- **Interface** — a documentation field recording, for this specific Tool, the current representation of the boundary that Domain Model §6 refers to when it requires interface preservation across a version change. This field records what has been documented as this Tool's interface at a point in time; it does not define what "interface" means for a Tool as a class, does not establish criteria for what counts as interface-preserving versus interface-breaking, and does not interpret Domain Model §6 beyond citing that the requirement exists. Any semantic interpretation of "interface" remains governed exclusively by the Canonical Domain Model.
- **Version** — per Domain Model §6, "Versioned independently."

## 10. Optional Document Fields

- Supplementary notes or rationale.
- Cross-references to Skill(s) or Agent Instance(s) that invoke this Tool (Domain Model §4: Agent Instance invokes Tool; Skill invokes Tool), referenced by name only, consistent with Section 14 below.
- A note recording the existence of an external/vendor dependency relationship in abstract terms, never naming a specific technology, vendor, or model — see Section 17.

## 11. Validation Model

- **Ownership validation** — the document correctly records central ownership; it does not declare an owning Department.
- **Interface-preservation validation** — a documented version change correctly distinguishes interface-preserving evolution from a behaviorally-material change requiring documentation at promotion time (Domain Model §6).
- **External dependency boundary validation** — no field in this document redefines or interprets Domain Model §7 invariant 12; the document does not imply any other entity may hold a direct external/vendor dependency.
- **Technology boundary validation** — no technology, vendor, or model name appears anywhere in the document, regardless of any latitude Domain Model §8 grants Tool's own conceptual definition — see Section 17.
- **Scope validation** — no field in this document redefines Tool, asserts a position on the promotion-terminology question in Section 13, or implies a direct Tool-to-Agent-Definition relationship.

## 12. Version Representation Convention

Per Domain Model §6, a Tool "may evolve as long as the interface is preserved," and "Skill/Tool version changes that alter behavior materially should be documented at promotion time, not just interface-checked."

This framework uses the term "promotion time" only in the sense already present in that Domain Model §6 text, describing when a Tool's version-history entry is documented, using the same treatment already applied by the Skill Framework to its own, textually identical lifecycle wording (Skill Framework §12). It does not resolve, and explicitly leaves open, whether this use of "promotion" is the same concept as the governed Memory-to-Knowledge promotion process (Domain Model §7 invariant 8) or a distinct, unrelated use of the same word. This ambiguity is recorded here as an open interpretive note, not resolved by this document — see Section 13.

Each Tool is recorded as a single, persistent document across its whole version lineage, with prior versions retained in its Version History section, consistent with the Domain Model's characterization of Tool as an entity "versioned independently" rather than as a series of discrete, individually-superseding records.

## 13. Explicitly Recorded Open Items

1. **"Promotion" terminology ambiguity.** Domain Model §6 requires that behaviorally-material Skill/Tool changes be "documented at promotion time." Domain Model §7 invariant 8 separately governs a distinct, specific "promotion" process for Memory becoming Knowledge, through governed review, never automatic. Whether the Skill/Tool lifecycle's use of "promotion time" refers to the same concept, a deliberately reused but distinct term, or an unrelated word choice, is not addressed anywhere in the ratified corpus. This framework uses the term only in citation of Domain Model §6's own language and takes no position on this question, using the same treatment already applied by the Skill Framework to its own, textually identical lifecycle wording.
2. **Technology boundary distinction.** Domain Model §8 permits Tool, together with Runtime, to name or imply specific external technology, vendors, or models at the level of the entity's own Domain Model definition. This latitude does not extend to this document. Constitution §6.2 invariant 1 binds every governance document, including this one, without an entity-specific exception; this framework's own content remains abstract throughout, using the same treatment already applied by the Runtime Framework to its own, identical latitude (Runtime Framework §13, item 2). See Section 17.
3. **External/vendor dependency exclusivity.** Domain Model §7 invariant 12 establishes that Tool is the only entity type permitted to hold a direct external/vendor dependency. This framework cites that invariant as the source of Tool's distinct status; it does not restate, interpret, or expand what "direct external/vendor dependency" means, and does not describe any specific dependency a real Tool instance might hold beyond the abstract Description and Interface fields (Section 9).
4. **EARC repository-location decisions.** The canonical identifier model, reference model, directory name (`execution-catalog`), repository path (`docs/architecture/organization/execution-catalog/`), canonical key format (`tool.<stable-name-slug>`), and internal organization model for Tool instances have all been resolved by EARC, as amended by EARC Amendment v1.1 (EARC §9). Slug normalization rules and filename conventions for individual Tool instances remain undefined, deferred to a separate, later instance-convention decision. This framework does not decide them. Resolving them requires a separate governance decision outside this document's scope.

Any resolution of the above, in any direction, would require action outside this document — an ADR for items touching Domain Model semantics (Constitution §3.4, §5), or a separate Architect-approved amendment for items belonging to EARC.

## 14. Reference Conventions

- **Tool** (self-reference) — Per EARC's Canonical Identifier Model and Reference Model (EARC §9), a Tool is referenced by its canonical key, which is the authoritative reference identity; a relative Markdown link to its current repository location may additionally be included as a navigation convenience. This framework does not itself define the canonical key's literal format or resolution mechanism; it inherits EARC's decision rather than anticipating or substituting for it.
- **Skill** — reference by canonical key, consistent with the Skill Framework's own reference convention (Skill Framework §14).
- **Agent Instance** — reference by name only, in the abstract. No Agent Instance Framework exists; this framework does not create one, and does not describe Agent Instance's own behavior or structure.

## 15. Storage Convention

Individual Tool instances are recorded within the unified execution-entity directory, located at `docs/architecture/organization/execution-catalog/tool/`, per EARC §9 as amended by EARC Amendment v1.1. The specific file-naming convention for individual Tool instances is not defined here and remains governed by the Execution Artifact Repository Convention, pending a separate, later instance-convention decision on slug normalization and filename rules (see Section 13, item 4). This framework does not select or imply an instance storage location beyond what EARC has resolved.

This framework document itself is recorded at `docs/architecture/organization/tool-framework.md`, a sibling to the Organization Framework, the Agent Definition Framework, the Execution Artifact Repository Convention, the Skill Framework, the Workflow Framework, and the Runtime Framework, consistent with the existing placement of Principle Documents within that directory.

## 16. Framework Ownership

Changes to this document follow the same ownership model already established by the Organization Framework, the Agent Definition Framework, the Skill Framework, the Workflow Framework, and the Runtime Framework: procedural mechanics — document structure, fields, validation, versioning convention, reference conventions — are owned by this document and may be updated through direct Architect-approved documentation changes. Domain Model semantics — what a Tool, Skill, Agent Instance, or any other entity is, and their relationships and invariants — remain exclusively governed by the Canonical Domain Model and are never redefined by this document, regardless of how this document itself evolves.

## 17. Explicit Exclusions

This framework does not, and may never:

- Redefine Tool, Skill, Agent Instance, Agent Definition, Workflow, Runtime, or any other Canonical Domain Model entity.
- Create new invariants, ownership rules, or lifecycle states beyond those already ratified.
- Create new governance authority.
- Resolve the "promotion" terminology ambiguity described in Section 13.
- Restate, interpret, or expand Domain Model §7 invariant 12.
- Decide, redefine, or override EARC's directory name, repository path, canonical key format, naming convention, or identifier/cross-reference syntax — these remain exclusively EARC's authority (EARC §9), including any item EARC leaves for future instance-convention decision.
- State or imply a direct Tool-to-Agent-Definition relationship.
- Name a specific technology, vendor, or model anywhere in this document's own text, regardless of any latitude Domain Model §8 grants to Tool's own Domain Model definition. That latitude belongs to the Canonical Domain Model's characterization of the entity; it is not inherited by this documentation-tier Framework, which remains bound without exception by Constitution §6.2 invariant 1.

This document is a documentation-tier Principle Document only. The Canonical Domain Model remains the sole semantic authority for Tool. The Execution Artifact Repository Convention retains exclusive authority over Tool's repository-location decisions; nothing in this document diminishes, bypasses, or anticipates that authority.

## 18. Status

Ratified. Approved by the System Architect.

Required safeguards remain active: the "promotion" terminology ambiguity (Section 13, item 1) remains unresolved; the technology-boundary distinction (Section 13, item 2) remains as stated; Domain Model §7 invariant 12 (Section 13, item 3) remains cited without interpretation or expansion; EARC's canonical identifier model, reference model, directory name, canonical key format, repository path, and internal organization model (Section 13, item 4) have since been resolved (EARC §9, as amended by EARC Amendment v1.1), with slug normalization rules and filename conventions remaining deferred to a separate, later instance-convention decision. No Agent Definition Framework synchronization is created or required by this ratification.

No Tool instance currently exists in the repository.
