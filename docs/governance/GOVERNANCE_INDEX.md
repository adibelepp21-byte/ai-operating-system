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
- Architecture Decision Records — `docs/architecture/adr/README.md` (framework); `docs/architecture/adr/decisions/ADR-0001.md` through `ADR-0028.md`. **26 carry an Approved or COMPLETE status; `ADR-0015` and `ADR-0017` remain `Proposed`**, each recording that the finding is delegated while the corrective action is Founder-reserved
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
- Governance Decision Register (permanent, append-only history of governance decisions that are not ADRs — principally Constitutional Tier decisions, which the ADR Framework's Validation Model excludes from the ADR instrument) — `docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md`; current entries: **GDR-0001 through GDR-0037** — beginning with GDR-0001 (Founder Decision G1′, Corpus Relationship) and GDR-0002 (Gate 4 Certification, Phase 4), and most recently GDR-0037 (Founder issuance of `FDE-P10-AUTONOMOUS-EXECUTION-01`)
- Superseded governance artifacts (retained as historical record, never deleted) — `docs/governance/AIOS_FOUNDER_DECISION_G1_PRIME_RATIFICATION_v1.0.md`, the original standalone recording of G1′, superseded by GDR-0001
- Delegation Register (append-only record of scoped delegations) — `docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md`; entries `DEL-T4.4-CF-001` and `DEL-F03-015-P7I99-001`
- Appointment Register (append-only record of role appointments and their activation) — `docs/governance/AIOS_APPOINTMENT_REGISTER_v1.0.md`; entry `APT-CD1.1-AA-001`
- Finding Register (permanent, append-only) — `docs/governance/AIOS_FINDING_REGISTER_v1.0.md`
- Volume Activation Model — `docs/governance/AIOS_VOLUME_ACTIVATION_MODEL_v1.0.md`; PD-02 activation gate criteria proposals `AIOS_PD02_ACTIVATION_GATE_CRITERIA_PROPOSAL_v0.1`–`v0.4` and `AIOS_PD02_FOUNDER_DECISION_PACKAGE_v1.0.md`
- Baseline Lifecycle, Maintenance Baseline MB-01, Native Core Closeout, Implementation Constitution — `docs/governance/AIOS_BASELINE_LIFECYCLE_v1.0.md`, `AIOS_MAINTENANCE_BASELINE_MB-01_v1.0.md`, `AIOS_NATIVE_CORE_CLOSEOUT_v1.0.md`, `AIOS_IMPLEMENTATION_CONSTITUTION_v1.0.md`
- Founder Decision Events — `docs/governance/AIOS_P10_AUTONOMOUS_EXECUTION_FOUNDER_EVENT_PROPOSAL_v1.0.md` (`FDE-P10-AUTONOMOUS-EXECUTION-01`, ISSUED and OPERATIVE from 05-09-2026; register record GDR-0037)
- Platform Division corpora — `docs/architecture/volume-1/pd-01-executive-office/` (45 bodies) and `docs/architecture/volume-2/pd-02-architecture-office/` (50 bodies, `Status: FROZEN`)
- Platform Organization construction artifacts — `docs/architecture/platform-organization/`, including `divisions/PD-01`–`PD-10`. **Every artifact there is self-declared `DERIVED`.** This Index records that self-declared status and assigns none: derived construction artifacts are not placed in the Section 4 tier map

## 4. Governance Tier Map

Per Constitution §4, governance artifacts occupy one of five tiers:

- Constitutional Tier — Engineering Constitution
- Domain Model Tier — Canonical Domain Model
- Architectural Tier — ADR-0001 through ADR-0028 (`ADR-0015` and `ADR-0017` are `Proposed`, not Approved)
- Principle Documents Tier — Organization Framework, Agent Definition Framework, EARC, Skill Framework, Workflow Framework, Runtime Framework, Tool Framework
- Implementation Tier — Department, Capability, and Agent Definition instances; Skill, Workflow, Runtime, and Tool instances (once EARC's remaining open items are resolved)

Registers (Governance Decision, Delegation, Appointment, Finding) record
decisions taken under the tiers above; they are recording instruments, and this
Index assigns them no tier of their own. Derived construction artifacts —
`docs/architecture/platform-organization/` — are likewise not placed in this map.

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

**Synchronization note — 2026-09-05.** Sections 3 and 4 had drifted materially:
the ADR range read `ADR-0001` through `ADR-0009` against 28 resident ADRs, and
the Governance Decision Register was recorded as holding two entries against 37.
The Delegation Register, Appointment Register, Finding Register, Volume
Activation Model, both Platform Division corpora, and the Platform Organization
construction artifacts were absent entirely. This is the condition
`AIOS_FINDING_REGISTER` classifies as **Category C — Governance Status Drift**,
whose *"correction is documentation synchronization."*

**Only synchronization was performed.** No open item in Section 6 was resolved,
no terminology was migrated, no artifact was assigned a tier it did not already
hold, and no position was taken on any substantive question. Performed under
`DEL-T4.4-CF-001 §3.1 C` (documentation), within
`FDE-P10-AUTONOMOUS-EXECUTION-01`.

**One interpretive question is recorded rather than resolved:** Section 9 below
requires *"normal Architect approval"* for updates to this Index, while also
stating that an update *"never itself constitutes a governance decision."* Whether
the Architecture Authority appointment (`APT-CD1.1-AA-001`, whose Constitutional
authority is **NONE**) satisfies *"Architect"* here is **UNKNOWN and was not
inferred**. This edit proceeded only on the half Section 9 itself describes as a
non-decision — reflecting records already made elsewhere. Any update that would
take a position on a substantive question was **not** performed and remains
outside this reading.

Navigation Artifact v1.0. No independent authority. Future updates to
this document require normal Architect approval, consistent with its
own non-authoritative status — an update to this Index never itself
constitutes a governance decision; it only reflects decisions already
made elsewhere.
