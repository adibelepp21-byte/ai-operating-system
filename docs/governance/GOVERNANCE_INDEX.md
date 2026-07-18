# Governance Navigation Index

## 1. Purpose

This document is a navigation and discovery layer for the AIOS governance
corpus only. It exists to help a reader locate which document already
governs a given question, without first needing to know the corpus's
tier structure or read every document to find it.

This document does not define, reinterpret, or replace any existing
governance document.

## 2. Authority Disclaimer

This Index carries zero independent governance authority. It is not
part of the Constitution §4 tier hierarchy, is not a Principle Document,
is not an Architecture Decision Record, and is not a Domain Model
artifact. Every statement in this document is a reference to content
that is authoritative elsewhere; nothing in this document is
authoritative in its own right. Where anything in this document
conflicts with the document it references, the referenced document
governs.

## 3. Repository Map

- Engineering Constitution — `docs/constitution/engineering-constitution-v1.md`
- Canonical Domain Model — `docs/architecture/domain-model/canonical-domain-model-v1.md`
- Architecture Decision Records — `docs/architecture/adr/README.md` (framework); `docs/architecture/adr/decisions/ADR-0001.md` through `ADR-0007.md`
- Organization Framework — `docs/architecture/organization/README.md`
- Agent Definition Framework — `docs/architecture/organization/agent-definitions.md`
- Execution Artifact Repository Convention (EARC) — `docs/architecture/organization/execution-artifact-repository.md`
- Skill Framework — `docs/architecture/organization/skill-framework.md`
- Workflow Framework — `docs/architecture/organization/workflow-framework.md`
- Runtime Framework — `docs/architecture/organization/runtime-framework.md`
- Tool Framework — `docs/architecture/organization/tool-framework.md`
- Glossary (navigational only; see `docs/glossary/README.md`) — points to Canonical Domain Model (entities/relationships) and Constitution Appendix A (governance roles and artifacts)
- Principles (reserved; see `docs/principles/README.md`) — not yet populated; Constitution §7–14 remains the current source
- Department and Capability instances — `docs/architecture/organization/<department-slug>/`; a populated example exists at `docs/architecture/organization/platform/`
- Agent Definition instances — `docs/architecture/organization/<department-slug>/agent-definitions/`; a populated example exists at `docs/architecture/organization/platform/agent-definitions/`
- Skill, Workflow, Runtime, and Tool instances — governed by EARC §9; unified directory named `execution-catalog`; complete repository path not yet finalized (see Section 6, below); no instance currently exists

## 4. Governance Tier Map

Per Constitution §4, governance artifacts occupy one of five tiers:

- Constitutional Tier — Engineering Constitution
- Domain Model Tier — Canonical Domain Model
- Architectural Tier — ADR-0001 through ADR-0007
- Principle Documents Tier — Organization Framework, Agent Definition Framework, EARC, Skill Framework, Workflow Framework, Runtime Framework, Tool Framework
- Implementation Tier — Department, Capability, and Agent Definition instances; Skill, Workflow, Runtime, and Tool instances (once EARC's remaining open items are resolved)

See Constitution §4 for the tier definitions and the relationships
between them. This Index does not restate them.

## 5. Decision Ownership Map

- Domain Model semantic change (entity, relationship, ownership rule, lifecycle rule, invariant) → Constitution §3.2, §3.4 + ADR process, Architect-exclusive.
- Framework documentation convention (structure, fields, validation, versioning, reference conventions) → each Framework's own Authority and Framework Ownership sections.
- Repository/reference convention for Skill, Workflow, Runtime, and Tool → EARC §3.
- Constitutional content → Constitution §16, Amendment Process, Architect-exclusive.
- Department/Capability/Agent Definition documentation convention → Organization Framework; Agent Definition Framework §3.

## 6. Open Decisions Registry

- Literal canonical-key format → EARC §9 ("Not Yet Defined"), §10 (Open Question 1)
- Complete repository path beyond the `execution-catalog` directory name → EARC §1, §7, §9, §12
- Runtime entity-vs-attribute classification → Canonical Domain Model §9; Runtime Framework §13, item 1
- ADR-0004 / ADR-0005 provenance question → Workflow Framework §13, item 1
- ADR-0005 narrative-accuracy note (Runtime lifecycle wording) → Runtime Framework §13, item 4
- "Compatibility boundaries... where applicable" ambiguity → Workflow Framework §13, item 2; Runtime Framework §13, item 3
- "Promotion" terminology ambiguity → Skill Framework §13, item 1; Tool Framework §13, item 1
- Scope of Agent Definition "permissions" → Agent Definition Framework §15, Open Architectural Question 3
- Capability versioning; cross-Department Capability implementation; Department transfer → Agent Definition Framework §15, Open Architectural Questions 1, 2, 4
- Constitution §6.1 invariant-count reference (reads "invariants 1–14" against 15 ratified invariants) → Constitution §6.1; Canonical Domain Model §7

This Index takes no position on any item listed above. Each remains open
exactly as recorded in the document cited.

## 7. Established Governance Practice

This program has, in observed practice, followed a staged sequence
across its governance changes to date — evidence review, decision/gate
review, draft, validation, editorial refinement, ratification, artifact
creation, commit, push, and post-ratification synchronization review.
This is recorded here as a description of historical practice only. No
Constitution, EARC, or Framework text codifies this sequence as a
binding requirement, and this Index does not make it one.

## 8. Explicit Exclusions

This document does not, and may never:

- Become an authority source in its own right.
- Redefine any Canonical Domain Model entity, relationship, ownership rule, lifecycle rule, or invariant.
- Restate or paraphrase any invariant, rule, or Constitutional provision.
- Introduce new requirements, obligations, or governance instruments beyond those already established in the documents it references.
- Resolve any open architectural question listed in Section 6, or any other unresolved question in the governance corpus.
- Replace, supersede, or substitute for reading any original governance document on a substantive question.
- Grant, expand, or reassign any authority, access, or modification permission.
- Name a specific technology, vendor, or model anywhere.

## 9. Status

Navigation Artifact v1.0. No independent authority. Future updates to
this document require normal Architect approval, consistent with its
own non-authoritative status — an update to this Index never itself
constitutes a governance decision; it only reflects decisions already
made elsewhere.
