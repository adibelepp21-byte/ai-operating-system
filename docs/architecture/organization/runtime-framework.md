# Runtime Framework

## 1. Purpose

This document defines how Runtime instances are documented within AIOS: their required structure, mandatory and optional content, version representation, validation, and reference conventions.

This document does not define what a Runtime is. That is defined exclusively in the Canonical Domain Model. This document never redefines, restates, or paraphrases that content; it only describes how already-ratified content is represented and recorded.

## 2. Scope

This framework governs the documentation of Runtime instances only. It does not govern Agent Definitions, Agent Instances, Skills, Workflows, or Tools — each, if given its own framework, is a separate document. It does not govern the shared repository-location boundary for Skill, Workflow, Runtime, and Tool, which remains governed exclusively by the Execution Artifact Repository Convention (EARC).

## 3. Authority

Runtime lifecycle semantics — what versioning and governed revision mean for a Runtime — are governed exclusively by Canonical Domain Model §5 (Ownership Rules) and §6 (Lifecycle Rules), as established via ADR-0005. This document holds no authority over, and does not restate, that semantic content.

This document's own authority is limited to how already-ratified lifecycle information is represented in documentation: which fields record it, how a Version History entry is structured, and how a documented change is distinguished as compatibility-preserving versus behaviorally material for recording purposes. It does not determine what lifecycle states exist, when a transition is valid, or what governs it — those determinations remain the Domain Model's alone.

This document's own content — structure, fields, validation, versioning convention, reference conventions — is a documentation and repository-organization convention, not a governance-authority artifact. It sits within the Principle Documents tier of Engineering Constitution §4, the same positioning as the Organization Framework, the Agent Definition Framework, the Execution Artifact Repository Convention, the Skill Framework, and the Workflow Framework.

This document takes no position on whether Runtime is, or should remain, a standalone Canonical Domain Model entity. Per Domain Model §9, that question is explicitly unresolved and retained as future work; see Section 13.

## 4. Relationship to the Constitution

This framework defines and alters no Constitutional authority. Any content in this document remains bound absolutely by Constitution §6.2's prohibitions — including invariant 1 (no technology, language, framework, or infrastructure decision in governance documents) and invariant 3 (no non-Domain-Model document may introduce, redefine, or contradict Domain Model content).

## 5. Relationship to the Canonical Domain Model

The Canonical Domain Model is the sole semantic authority for what a Runtime is, its ownership, its relationship to Agent Instance, and its invariants. This document does not reproduce, restate, or paraphrase that content anywhere below. Where this framework requires a field or a validation step, it cites the Domain Model section that already requires it; it does not independently assert the requirement.

## 6. Relationship to the Execution Artifact Repository Convention

Runtime is one of four entities governed by the Execution Artifact Repository Convention's (EARC) shared repository-location boundary (EARC §2). This framework inherits, rather than duplicates, EARC's resolved decisions: the unified execution-entity directory, named `execution-catalog`, and Runtime's differentiated treatment within it — a direct sibling grouping alongside Skill, Workflow, and Tool, distinguished through its own label rather than through any difference in nesting depth, and explicitly not participating in the Workflow-contains-Skill or Skill-invokes-Tool compositional relationships (EARC §9). This framework also inherits the general Framework-relationship citation principle (EARC §9, including its "Citation discipline for future Frameworks" entry).

This framework does not itself decide, and does not attempt to decide, EARC's own repository-location convention; that convention belongs exclusively to EARC. Per EARC §9, Runtime instances are identified by a stable, human-readable canonical key and recorded within the unified execution-entity directory, organized by the symmetric grouping described above. The literal format of the canonical key remains open (EARC §9, "Not Yet Defined"). Where this document must refer to a Runtime instance's storage location or identity in concrete terms, it does so only in the abstract, pending that remaining decision.

## 7. Relationship to the Agent Definition Framework

The Agent Definition Framework describes Runtime only as an abstract requirement, stating that Runtime and Tool are the only entities permitted to name specific technology, vendors, or models, and that this field may never do so (Agent Definition Framework §8, §12). This framework does not alter that treatment; a Runtime Framework governs how Runtime itself is documented as a Framework-level artifact, not how Agent Definition Framework's own Runtime Requirements field operates.

This document has since been ratified. Agent Definition Framework §12's Runtime entry and §10's Validation Model have each since been synchronized — §12 now cites this Framework, and §10 now includes a Runtime validation bullet — mirroring the synchronization already performed for Skill and Workflow. Both were carried out as separate, direct Architect-approved documentation changes to that Framework, not performed by this document.

## 8. Document Structure Requirements

Every Runtime document follows this structure:

1. Metadata
2. Purpose / Description
3. Hosted Relationship
4. Compatibility Boundary Representation
5. Version History

This mirrors the Metadata-first, substantive-content, change-history-last pattern already established by the ADR Structure and the Agent Definition Framework's, Skill Framework's, and Workflow Framework's own Document Structure Requirements, for consistency. "Hosted Relationship" replaces Skill Framework's "Interface" and Workflow Framework's "Composed Elements," reflecting Runtime's own directionally distinct relationship (Runtime hosts Agent Instance, rather than being invoked or contained). "Compatibility Boundary Representation" mirrors Workflow Framework's field of the same name, reflecting Runtime's identical Domain Model §6 lifecycle wording.

## 9. Mandatory Document Fields

- **Name** — a documentation-level identifier used to reference this Runtime document and distinguish it from other Runtime documents across its version lineage. This field is a reference and record-keeping mechanism, not an assertion of Domain-Model-mandated semantic identity: Domain Model §2 does not enumerate a "named" requirement for Runtime the way it does for Capability, and this document does not claim otherwise. The field exists because this framework's own reference conventions (Section 14) require some stable label to cite a Runtime document by; it does not represent a Domain Model determination that Runtime identity works this way.
- **Owning designation** — Runtime is owned centrally (Domain Model §5), grouped with Skill and Tool, not by a Department. This field records that central-ownership status; it does not name an owning Department, since none exists for this entity.
- **Description** — what the execution substrate provides, per Domain Model §2. Stated only in the abstract; may not name a specific technology, vendor, or model — see Section 17.
- **Hosts Agent Instance** — a documentation field recording, by reference only, that this Runtime may host Agent Instance execution, per Domain Model §4's Runtime-hosts-Agent-Instance relationship. This field records the existence of this relationship for a given Runtime; it does not define, redefine, or describe Agent Instance's own behavior, lifecycle, or execution semantics, which remain exclusively Domain Model content and are not governed by any Framework at this time.
- **Compatibility Boundary Representation** — a documentation field recording, for this specific Runtime, the current representation of the boundary that Domain Model §6 refers to when it requires "compatibility boundaries preserved where applicable" across a version change. This field records what has been documented as this Runtime's compatibility boundary at a point in time; it does not define what "compatibility boundary" means for a Runtime as a class, does not establish criteria for what counts as preserving it, and does not interpret what "where applicable" qualifies. Any semantic interpretation remains governed exclusively by the Canonical Domain Model — see Section 13.
- **Version** — per Domain Model §6, "Versioned independently."

## 10. Optional Document Fields

- Supplementary notes or rationale.
- Cross-references to related Runtime documents.
- A note on the Agent Instance hosting relationship's scope, stated only as documentation of what has been recorded, not as an assertion of execution semantics — Domain Model §8 excludes implementation/execution-order detail from this document's authority.

## 11. Validation Model

- **Ownership validation** — central ownership recorded; no owning Department declared.
- **Hosting reference validation** — provisional only. No Runtime or Agent Instance instances currently exist; this check is aspirational until they do, and its absence is not a defect in this framework.
- **Compatibility boundary validation** — a documented version change correctly distinguishes what has been recorded as preserved from what has not, without asserting a general definition of "compatibility boundary" (Domain Model §6).
- **Technology boundary validation** — no technology, vendor, or model name appears anywhere in the document, regardless of any latitude Domain Model §8 grants Runtime's own conceptual definition — see Section 17.
- **Scope validation** — no field in this document redefines Runtime or Agent Instance; asserts a position on Runtime's entity-vs-attribute status; resolves the ADR-0005 narrative-accuracy question; or resolves the compatibility-boundary ambiguity in Section 13.

## 12. Version Representation Convention

Per Domain Model §6, a Runtime is "versioned independently; evolved through governed revisions, with compatibility boundaries preserved where applicable; behavioral drift is documented at change time," as established via ADR-0005.

This framework uses the term "compatibility boundaries... where applicable" only in the sense already present in that Domain Model §6 text, and only as already applied by the Workflow Framework to its own, textually identical lifecycle wording (Workflow Framework §12). It does not define what constitutes a compatibility boundary for a Runtime, does not establish when the qualifier "where applicable" does or does not apply, and does not resolve this ambiguity. This is recorded here as an open interpretive note, not resolved by this document — see Section 13.

Each Runtime is recorded as a single, persistent document across its whole version lineage, with prior versions retained in its Version History section, consistent with the Domain Model's characterization of Runtime as an entity "versioned independently" rather than as a series of discrete, individually-superseding records.

## 13. Explicitly Recorded Open Items

1. **Domain Model §9 — entity vs. attribute.** Domain Model §9 explicitly and currently retains Runtime as a Domain Model entity for v1.0, while leaving open, in either direction, whether Runtime should ultimately be modeled as an attribute rather than a standalone entity: "pending future evidence it needs independent governance." This framework documents Runtime's current, ratified status as an entity; it takes no position on, and does not resolve, the deferred question. Should that question ever be resolved in a way that changes Runtime's Domain Model status, this document would require a corresponding revision — the same standing possibility every Framework in this corpus already accepts for any future Domain Model change (Section 16).
2. **Technology boundary distinction.** Domain Model §8 permits Runtime, together with Tool, to name or imply specific external technology, vendors, or models at the level of the entity's own Domain Model definition. This latitude does not extend to this document. Constitution §6.2 invariant 1 binds every governance document, including this one, without an entity-specific exception; this framework's own content remains abstract throughout, consistent with the treatment Agent Definition Framework §8 already applies to its own Runtime Requirements field. See Section 17.
3. **Compatibility boundary ambiguity.** Domain Model §6 requires that Runtime version changes preserve "compatibility boundaries... where applicable," without defining what constitutes a compatibility boundary for a Runtime or what the qualifier "where applicable" scopes. This framework cites that requirement without interpreting it, using the same treatment already applied by the Workflow Framework to its own, textually identical lifecycle wording — see Section 12.
4. **ADR-0005 narrative-accuracy note.** ADR-0005, which established Runtime's Domain Model §6 lifecycle row, characterizes the adopted wording as "the lifecycle governance pattern used by centrally-owned Execution-layer entities such as Skill and Tool." Domain Model §6's actual, separately-ratified Skill/Tool row uses different wording ("interface... preserved"... "documented at promotion time") than the wording ADR-0005 adopted for Runtime ("compatibility boundaries... where applicable"... "documented at change time") — wording that instead matches Workflow's row (established by ADR-0004). This framework cites Domain Model §6 and ADR-0005 as the source of Runtime's lifecycle rule; it does not characterize, correct, or resolve this difference in ADR-0005's own narrative text, and proposes no amendment to ADR-0005.
5. **EARC repository-location decisions.** The canonical identifier model, reference model, directory name (`execution-catalog`), and internal organization model for Runtime instances have been resolved by EARC (EARC §9). The literal format of the canonical key remains undefined, per EARC §9, "Not Yet Defined." This framework does not decide it. Resolving it requires a separate EARC amendment — a distinct governance decision outside this document's scope.
6. **Agent Definition Framework synchronization.** This framework's ratification was the event Agent Definition Framework §12 and §10 both anticipated for Runtime specifically. Both sections have since been updated — §12 now cites this Framework, and §10 now includes a Runtime validation bullet — through separate, direct Architect-approved documentation changes to that Framework, not performed by, or recorded as an amendment within, this document.

Any resolution of the above, in any direction, would require action outside this document — an ADR for items touching Domain Model semantics (Constitution §3.4, §5), or a separate Architect-approved amendment for items belonging to EARC or the Agent Definition Framework.

## 14. Reference Conventions

- **Runtime** (self-reference) — Per EARC's Canonical Identifier Model and Reference Model (EARC §9), a Runtime is referenced by its canonical key, which is the authoritative reference identity; a relative Markdown link to its current repository location may additionally be included as a navigation convenience. This framework does not itself define the canonical key's literal format or resolution mechanism; it inherits EARC's decision rather than anticipating or substituting for it.
- **Agent Instance** — reference by name only, in the abstract. No Agent Instance Framework exists; this framework does not create one, and does not describe Agent Instance's own behavior or structure.

## 15. Storage Convention

Individual Runtime instances are recorded within the unified execution-entity directory, named `execution-catalog`, organized by a symmetric grouping labeled by governed entity, per EARC §9. The specific file-naming convention for individual Runtime instances is not defined here and remains governed by the Execution Artifact Repository Convention, pending resolution of the canonical key's literal format (see Section 13, item 5). This framework does not select or imply an instance storage location beyond what EARC has resolved.

This framework document itself is recorded at `docs/architecture/organization/runtime-framework.md`, a sibling to the Organization Framework, the Agent Definition Framework, the Execution Artifact Repository Convention, the Skill Framework, and the Workflow Framework, consistent with the existing placement of Principle Documents within that directory.

## 16. Framework Ownership

Changes to this document follow the same ownership model already established by the Organization Framework, the Agent Definition Framework, the Skill Framework, and the Workflow Framework: procedural mechanics — document structure, fields, validation, versioning convention, reference conventions — are owned by this document and may be updated through direct Architect-approved documentation changes. Domain Model semantics — what a Runtime, Agent Instance, or any other entity is, and their relationships and invariants — remain exclusively governed by the Canonical Domain Model and are never redefined by this document, regardless of how this document itself evolves. This includes any future change to Runtime's own Domain Model status (Section 13, item 1).

## 17. Explicit Exclusions

This framework does not, and may never:

- Redefine Runtime, Agent Instance, Skill, Workflow, Tool, or any other Canonical Domain Model entity.
- Create new invariants, ownership rules, or lifecycle states beyond those already ratified.
- Create new governance authority.
- Resolve whether Runtime should be modeled as an entity or an attribute (Domain Model §9).
- Resolve the ADR-0005 narrative-accuracy question described in Section 13.
- Resolve the "compatibility boundaries... where applicable" ambiguity described in Section 13.
- Decide EARC's open directory name, repository path, naming convention, or identifier/cross-reference syntax.
- Describe Agent Instance's own behavior, lifecycle, or execution semantics.
- Name a specific technology, vendor, or model anywhere in this document's own text, regardless of any latitude Domain Model §8 grants to Runtime's own Domain Model definition. That latitude belongs to the Canonical Domain Model's characterization of the entity; it is not inherited by this documentation-tier Framework, which remains bound without exception by Constitution §6.2 invariant 1.

## 18. Status

Ratified. Approved by the System Architect.

Required safeguards remain active: the Runtime entity-vs-attribute question (Section 13, item 1) remains unresolved; the technology-boundary distinction (Section 13, item 2) remains as stated; the compatibility-boundary ambiguity (Section 13, item 3) remains unresolved; the ADR-0005 narrative-accuracy note (Section 13, item 4) remains recorded without amending ADR-0005; EARC's canonical identifier model, reference model, directory name, and internal organization model (Section 13, item 5) have since been resolved (EARC §9), with the literal canonical-key format remaining unresolved; Agent Definition Framework synchronization (Section 13, item 6) has since been completed, as separate documentation changes to that Framework, not by this document.

No Runtime instance currently exists in the repository.
