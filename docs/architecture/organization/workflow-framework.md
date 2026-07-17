# Workflow Framework

## 1. Purpose

This document defines how Workflow instances are documented within AIOS: their required structure, mandatory and optional content, version representation, validation, and reference conventions.

This document does not define what a Workflow is. That is defined exclusively in the Canonical Domain Model. This document never redefines, restates, or paraphrases that content; it only describes how already-ratified content is represented and recorded.

## 2. Scope

This framework governs the documentation of Workflow instances only. It does not govern Agent Definitions, Agent Instances, Skills, Tools, or Runtime — each, if given its own framework, is a separate document. It does not govern the shared repository-location boundary for Skill, Workflow, Runtime, and Tool, which remains governed exclusively by the Execution Artifact Repository Convention (EARC).

## 3. Authority

Workflow lifecycle semantics — what creation, deprecation, versioning, and governed revision mean for a Workflow — are governed exclusively by Canonical Domain Model §5 (Ownership Rules) and §6 (Lifecycle Rules), as established via ADR-0004. This document holds no authority over, and does not restate, that semantic content.

This document's own authority is limited to how already-ratified lifecycle information is represented in documentation: which fields record it, how a Version History entry is structured, and how a documented change is distinguished as compatibility-preserving versus behaviorally material for recording purposes. It does not determine what lifecycle states exist, when a transition is valid, or what governs it — those determinations remain the Domain Model's alone.

This document's own content — structure, fields, validation, versioning convention, reference conventions — is a documentation and repository-organization convention, not a governance-authority artifact. It sits within the Principle Documents tier of Engineering Constitution §4, the same positioning as the Organization Framework, the Agent Definition Framework, the Execution Artifact Repository Convention, and the Skill Framework.

## 4. Relationship to the Constitution

This framework defines and alters no Constitutional authority. Any content in this document remains bound absolutely by Constitution §6.2's prohibitions — including invariant 1 (no technology, language, framework, or infrastructure decision in governance documents) and invariant 3 (no non-Domain-Model document may introduce, redefine, or contradict Domain Model content).

## 5. Relationship to the Canonical Domain Model

The Canonical Domain Model is the sole semantic authority for what a Workflow is, its ownership, its relationships to Agent Definition, Agent Instance, and Skill, and its invariants. This document does not reproduce, restate, or paraphrase that content anywhere below. Where this framework requires a field or a validation step, it cites the Domain Model section that already requires it; it does not independently assert the requirement.

## 6. Relationship to the Execution Artifact Repository Convention

Workflow is one of four entities governed by the Execution Artifact Repository Convention's (EARC) shared repository-location boundary (EARC §2). This framework inherits, rather than duplicates, EARC's resolved decisions: the unified execution-entity directory, Workflow's sibling grouping with Skill and Tool — reflecting the Workflow-contains-Skill relationship specifically named in EARC's own grouping rationale (EARC §9) — and the general Framework-relationship citation principle (EARC §9, including its "Citation discipline for future Frameworks" entry).

This framework does not itself decide, and does not attempt to decide, the specific directory name, repository path, instance naming convention, or identifier and cross-reference syntax that EARC leaves open (EARC §9, §10). Those remain separate governance decisions belonging exclusively to EARC. Where this document must refer to a Workflow instance's storage location, it does so only in the abstract, pending those decisions.

## 7. Relationship to the Agent Definition Framework

The Agent Definition Framework treats Workflow as a name-only reference (Agent Definition Framework §12), explicitly noting this as "a known, deliberate limitation, not an oversight." This framework's creation was the anticipated event that framework referenced. Agent Definition Framework §12 and §10 have since each been synchronized to reflect this Framework's existence, mirroring the synchronization already performed for Skill; both were carried out as separate, direct Architect-approved documentation changes to that Framework, not performed by this document.

Agent Definition Framework §15 Open Architectural Question 3 (scope of "permissions") remains open. This framework does not resolve it, and no content below should be read as taking a position on whether Agent Definition permissions ever extend beyond Skill/Workflow authorization.

## 8. Document Structure Requirements

Every Workflow document follows this structure:

1. Metadata
2. Purpose / Description
3. Composed Elements
4. Compatibility Boundary Representation
5. Version History

This mirrors the Metadata-first, substantive-content, change-history-last pattern already established by the ADR Structure and the Agent Definition Framework's and Skill Framework's own Document Structure Requirements, for consistency. "Composed Elements" and "Compatibility Boundary Representation" replace Skill Framework's "Interface" and "Permitted Invocation Context," reflecting Workflow's own, differently-worded Domain Model §6 lifecycle language and its dual relationship set.

## 9. Mandatory Document Fields

- **Name** — a documentation-level identifier used to reference this Workflow document and distinguish it from other Workflow documents across its version lineage. This field is a reference and record-keeping mechanism, not an assertion of Domain-Model-mandated semantic identity: Domain Model §2 does not enumerate a "named" requirement for Workflow the way it does for Capability, and this document does not claim otherwise. The field exists because this framework's own reference conventions (Section 14) require some stable label to cite a Workflow document by; it does not represent a Domain Model determination that Workflow identity works this way.
- **Owning designation** — Workflow is owned centrally (Domain Model §5), not by a Department. This field records that central-ownership status; it does not name an owning Department, since none exists for this entity.
- **Description** — what the explicit, inspectable composition accomplishes, per Domain Model §2. Stated only in the abstract; may not name a specific technology, vendor, or model (Domain Model §8, Constitution §6.2 invariant 1).
- **Contains Skill** — a documentation field listing, by reference only, the Skill(s) this Workflow composes, per Domain Model §4's Workflow-contains-Skill relationship. This field records which Skills are referenced; it does not redefine Skill, does not restate Skill's own documentation (governed exclusively by the Skill Framework), and may be empty if a specific Workflow's composition does not yet include any documented Skill.
- **Invokes Agent Instance** — a documentation field recording, by reference only, that this Workflow may invoke Agent Instance execution, per Domain Model §4's Workflow-invokes-Agent-Instance relationship. This field records the existence of this relationship for a given Workflow; it does not define, redefine, or describe Agent Instance's own behavior, lifecycle, or execution semantics, which remain exclusively Domain Model content and are not governed by any Framework at this time.
- **Compatibility Boundary Representation** — a documentation field recording, for this specific Workflow, the current representation of the boundary that Domain Model §6 refers to when it requires "compatibility boundaries preserved where applicable" across a version change. This field records what has been documented as this Workflow's compatibility boundary at a point in time; it does not define what "compatibility boundary" means for a Workflow as a class, does not establish criteria for what counts as preserving it, and does not interpret what "where applicable" qualifies. Any semantic interpretation remains governed exclusively by the Canonical Domain Model — see Section 13.
- **Version** — per Domain Model §6, "Versioned independently."

## 10. Optional Document Fields

- Supplementary notes or rationale.
- Cross-references to related Workflows or the Agent Definitions that specify it.
- A note on the sequencing or composition structure among contained Skills, stated only as documentation of what has been recorded, not as an assertion of execution semantics — Domain Model §8 excludes implementation/execution-order detail from this document's authority.

## 11. Validation Model

- **Ownership validation** — central ownership recorded; no owning Department declared.
- **Composition reference validation** — provisional only. No Workflow or Skill instances currently exist; this check is aspirational until they do, and its absence is not a defect in this framework.
- **Compatibility boundary validation** — a documented version change correctly distinguishes what has been recorded as preserved from what has not, without asserting a general definition of "compatibility boundary" (Domain Model §6).
- **Boundary validation** — no technology, vendor, or model name appears anywhere in the document.
- **Scope validation** — no field in this document redefines Workflow, Skill, Agent Instance, or Agent Definition; asserts a position on Agent Definition Framework §15 Q3; resolves the ADR-0004/ADR-0005 provenance question; or resolves the compatibility-boundary ambiguity in Section 13.

## 12. Version Representation Convention

Per Domain Model §6, a Workflow is "versioned independently; evolved through governed revisions, with compatibility boundaries preserved where applicable; behavioral drift is documented at change time," as established via ADR-0004.

This framework uses the term "compatibility boundaries... where applicable" only in the sense already present in that Domain Model §6 text. It does not define what constitutes a compatibility boundary for a Workflow, does not establish when the qualifier "where applicable" does or does not apply, and does not resolve this ambiguity. This is recorded here as an open interpretive note, not resolved by this document — see Section 13.

Each Workflow is recorded as a single, persistent document across its whole version lineage, with prior versions retained in its Version History section, consistent with the Domain Model's characterization of Workflow as an entity "versioned independently" rather than as a series of discrete, individually-superseding records.

## 13. Explicitly Recorded Open Items

1. **ADR-0004 / ADR-0005 provenance.** Workflow's lifecycle authority is established via Domain Model §6 and ADR-0004. ADR-0004 itself states that, should ADR-0005 be approved first, its own Lifecycle Rules content for Workflow should be understood as adopting the pattern ADR-0005 separately establishes for Runtime. The precise relationship or classification between ADR-0004 and ADR-0005 — including how this conditional, order-dependent citation should be characterized — remains an open question outside this document's authority. This framework cites Domain Model §6 and ADR-0004 as the source of Workflow's lifecycle rule; it does not characterize, classify, or resolve the ADR-0004/ADR-0005 relationship in any way.
2. **"Compatibility boundaries... where applicable" ambiguity.** Domain Model §6 requires that Workflow version changes preserve "compatibility boundaries... where applicable," without defining what constitutes a compatibility boundary for a Workflow or what the qualifier "where applicable" scopes. This framework cites that requirement without interpreting it — see Section 12.
3. **Agent Definition Framework §15 Q3 — scope of "permissions."** Whether Agent Definition's declared permissions ever extend beyond Skill/Workflow authorization remains an open question belonging to the Agent Definition Framework and, ultimately, to the Domain Model. This framework's Composed Elements field (Section 8) describes only what a Workflow itself contains or invokes; it does not address or resolve the broader permissions-scope question.
4. **EARC repository-location decisions.** The specific directory name, repository path, instance naming convention, and identifier/cross-reference syntax for Workflow instances remain undefined, per EARC §9–§10. This framework does not decide them. Resolving them requires a separate EARC amendment — a distinct governance decision outside this document's scope.
5. **Agent Definition Framework §12 and §10 synchronization.** This framework's ratification was the event Agent Definition Framework §12 and §10 both anticipated for Workflow specifically. Both sections have since been updated to reflect this Framework's existence, through separate, direct Architect-approved documentation changes to that Framework — not performed by, or recorded as an amendment within, this document.

Any resolution of the above, in any direction, would require action outside this document — an ADR for items touching Domain Model semantics (Constitution §3.4, §5), or a separate Architect-approved amendment for items belonging to EARC or the Agent Definition Framework.

## 14. Reference Conventions

- **Workflow** (self-reference) — until EARC resolves a formal identifier and cross-reference convention (Section 13, item 4), this framework provisionally references a Workflow by name only. This is not a final identifier decision and does not establish a naming or identifier convention on this framework's own authority; it is a placeholder representation pending EARC's decision, which this framework inherits once made rather than anticipating or substituting for.
- **Skill** — reference by name only, consistent with the Skill Framework's own provisional reference convention (Skill Framework §14), pending the same EARC decision.
- **Agent Instance** — reference by name only, in the abstract. No Agent Instance Framework exists; this framework does not create one, and does not describe Agent Instance's own behavior or structure.
- **Agent Definition** — reference by name and link to its Agent Definition Framework entry, where the reverse (Agent Definition → Workflow) reference already exists per Agent Definition Framework §12.

## 15. Storage Convention

The specific repository path and file-naming convention for individual Workflow instances are not defined here. They remain governed by the Execution Artifact Repository Convention, once EARC's own open items (directory name, path, naming, identifier convention) are resolved (see Section 13, item 4). This framework does not select or imply an instance storage location.

This framework document itself is recorded at `docs/architecture/organization/workflow-framework.md`, a sibling to the Organization Framework, the Agent Definition Framework, the Execution Artifact Repository Convention, and the Skill Framework, consistent with the existing placement of Principle Documents within that directory.

## 16. Framework Ownership

Changes to this document follow the same ownership model already established by the Organization Framework, the Agent Definition Framework, and the Skill Framework: procedural mechanics — document structure, fields, validation, versioning convention, reference conventions — are owned by this document and may be updated through direct Architect-approved documentation changes. Domain Model semantics — what a Workflow, Skill, Agent Instance, Agent Definition, or any other entity is, and their relationships and invariants — remain exclusively governed by the Canonical Domain Model and are never redefined by this document, regardless of how this document itself evolves.

## 17. Explicit Exclusions

This framework does not, and may never:

- Redefine Workflow, Skill, Agent Instance, Agent Definition, Tool, or any other Canonical Domain Model entity.
- Create new invariants, ownership rules, or lifecycle states beyond those already ratified.
- Create new governance authority.
- Resolve Agent Definition Framework §15 Q3 (scope of "permissions").
- Resolve the ADR-0004/ADR-0005 provenance question described in Section 13.
- Resolve the "compatibility boundaries... where applicable" ambiguity described in Section 13.
- Decide EARC's open directory name, repository path, naming convention, or identifier/cross-reference syntax.
- Describe Agent Instance's own behavior, lifecycle, or execution semantics.
- Name a specific technology, vendor, or model anywhere.

## 18. Status

Ratified. Approved by the System Architect.

Required safeguards remain active per the ratification authorization: the ADR-0004/ADR-0005 provenance question (Section 13, item 1) remains explicitly unresolved; the "compatibility boundaries... where applicable" ambiguity (Section 13, item 2) remains explicitly unresolved; Agent Definition Framework §15 Q3 (Section 13, item 3) remains open; EARC's directory name, path, naming convention, and identifier/cross-reference syntax (Section 13, item 4) remain untouched; Agent Instance receives no Framework authority through this document; the Agent Definition Framework §12/§10 synchronization pass (Section 13, item 5) has since been completed, as separate documentation changes to that Framework, not by this document.

No Workflow instance currently exists in the repository.
