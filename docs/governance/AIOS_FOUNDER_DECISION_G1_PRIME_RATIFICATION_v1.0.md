# AIOS Founder Decision G1′ — Corpus Relationship Ratification

> **SUPERSEDED — HISTORICAL RECORD.** The authoritative record of Founder
> Decision G1′ is **GDR-0001** in the permanent governance history:
> `docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md`.
>
> This document is the **original standalone recording** made on 2026-07-30
> and is retained unaltered in substance as a historical artifact, per the
> repository's append-only discipline (ADR Framework: *"Every terminal state
> … is retained indefinitely as permanent record"*). It is superseded, not
> withdrawn: the decision it records remains ratified and in force.
>
> Four wording corrections were applied on 2026-07-30 under a targeted Founder
> refinement instruction, narrowing statements that had exceeded the scope of
> the decision. They are itemised in §14, below. No governance meaning was
> changed beyond that narrowing.

**Status:** Superseded by GDR-0001 (record location only; the decision remains Ratified and in force)
**Version:** v1.0
**Decision Identifier:** G1′
**Tier:** Constitutional Tier (Engineering Constitution §3.1)
**Decided by:** Founder / Program Owner of AIOS
**Recorded by:** AI Systems Engineer, under explicit Founder execution authorization
**Authority Disclaimer:** This document records a decision; it does not make
one, and it carries no independent governance authority. Where anything here
appears to conflict with the Engineering Constitution or the Canonical Domain
Model, those documents govern.

---

## 1. Purpose

This document is the durable record of Founder Decision **G1′ — Corpus
Relationship**, the Constitutional-Tier decision resolving the authority
relationship between the AIOS repository governance corpus and the AIOS
Master Program corpus.

It exists because Engineering Constitution §3.1 places *"changes to the
authority relationship among AIOS's governance artifacts (Section 4)"* at
Constitutional Tier, reserved to *"the Architect, exclusively"*, and because
Engineering Constitution §16 requires that constitutional acts be recorded
rather than left to memory or inference.

This document creates no entity, alters no invariant, and amends no
governance text.

---

## 2. Decision Statement (verbatim)

The Founder's election is recorded here without reinterpretation,
substitution, or paraphrase.

> ## G1′ — Corpus Relationship
>
> **Selected Option: OPTION A**
>
> The repository ratified pair:
>
> - `docs/constitution/engineering-constitution-v1.md`
> - `docs/architecture/domain-model/canonical-domain-model-v1.md`
>
> together with their Architect-approved ADR series (`ADR-0001` ...
> `ADR-0007`) are hereby recognized as the **original and authoritative AIOS
> Constitution and Canonical Domain Model** referred to by Master Program
> Volume I §7.1.
>
> Accordingly:
>
> - Volume I Pasal 1–6 are confirmed as a consolidation of those original
>   governance documents.
> - The repository Constitutional corpus becomes the constitutional and
>   semantic authority for repository governance.
> - Repository projections (Architecture Freeze, Blueprint, Relationship
>   Model, Roadmap, Engineering Specifications, implementation) remain
>   governed by that Constitutional pair.
> - The Master Program continues as the strategic planning and governance
>   program above execution, but no longer functions as an independent
>   constitutional source for repository architecture.
> - Any inconsistencies identified during validation are treated as
>   governance synchronization work, **not** implementation defects.
>
> This decision is final unless explicitly amended through the
> constitutional amendment process.

---

## 3. Authority Basis

| Element | Basis |
|---|---|
| Tier | Engineering Constitution §3.1 — Constitutional Tier: *"amendments to this Constitution; changes to constitutional principles and constitutional invariants; changes to the authority relationship among AIOS's governance artifacts (Section 4)."* |
| Holder | Engineering Constitution §3.1 — *"the Architect, exclusively."* |
| Delegability | Engineering Constitution §16 — *"Amendment authority rests exclusively with the Architect. No delegation of amendment authority is permitted under any circumstance."* §3.2 additionally bars delegation of Constitution amendments and Domain Model semantic changes. |
| Instrument | Not an ADR. The ADR Framework's Validation Model requires *"Boundary validation — confirms the ADR does not reach into Constitutional Tier territory."* A Constitutional-Tier decision therefore cannot be recorded as an ADR without failing that validation. |
| Recording obligation | Engineering Constitution §16 requires a written rationale, explicit Architect approval, and a recorded change entry. §14.1 requires that *"any point at which approval was required and sought must be recorded in the artifact under review, not left to memory or inference."* |

---

## 4. Question Answered

Prior governance review reduced a twelve-item Architect decision surface
(D1–D12) to five (M1–M5), then to two (G1, G2), then to one. The single
remaining matter was recorded as:

> Do the repository's ratified pair — `engineering-constitution-v1.md` and
> `canonical-domain-model-v1.md`, both *Status: Canonical · Approved by:
> System Architect*, together with the Architect-Approved ADR-0001…ADR-0007
> series that amends them and the Architecture Freeze / Native Core Blueprint
> / Canonical Relationship Model / Native Core Implementation Roadmap
> projected from them — stand as the AIOS Constitution and Canonical Domain
> Model that Master Program Volume I §7.1 requires Pasal 1–6 to be validated
> against?

The Founder answered **YES** (Option A).

---

## 5. Evidence of Record

The evidence on which the decision was presented, recorded here so the
reasoning survives independently of the review that produced it.

| # | Evidence |
|---|---|
| 1 | `engineering-constitution-v1.md` header: *Status: Canonical · Approved by: System Architect.* Preamble: *"This Constitution is the highest-authority governance document of the AI Operating System (AIOS). Where any other document, decision, or practice conflicts with this Constitution, this Constitution prevails."* |
| 2 | `canonical-domain-model-v1.md` header: *Status: Canonical · Approved by: System Architect.* §11: *"Ratified by the System Architect."* |
| 3 | The two are a mutually-referencing ratified pair. Canonical Domain Model §11: *"Serves as: the semantic foundation the Engineering Constitution has formalized into governance language."* Engineering Constitution §5: *"The Canonical Domain Model is the sole semantic authority of AIOS."* |
| 4 | Master Program Volume I §1.1: an Engineering Constitution existed before Volume I was written; Volume I's work was *"konsolidasi, bukan penciptaan ulang."* |
| 5 | Master Program Volume I §7.1: the source Engineering Constitution *"belum pernah dikirim dalam bentuk teks penuh"*, and Pasal 1–6 *"perlu divalidasi terhadap dokumen constitution asli, jika ada."* Volume I §8 marks the corresponding Phase 0 exit criterion *"Sebagian."* |
| 6 | Architecture Review Log ARB-001 certified Master Program Volume I **Pasal 7–8 only**; Pasal 1–6 lie outside that certified scope. |
| 7 | `docs/architecture/AIOS_ARCHITECTURE_CONSTITUTION_v1.0.md` self-subordinates and names the pair: *"Subordinate to, and never in conflict with, the ratified `engineering-constitution-v1.md` and `canonical-domain-model-v1.md`."* Its §6.3 adds: *"Where the ratified Constitution or Canonical Domain Model speaks to a question … those documents are authoritative and this layer's code defers to them."* |
| 8 | The ADR-0001…ADR-0007 series is Architect-Approved and operative on the Canonical Domain Model itself: ADR-0001 and ADR-0002 amended its text; ADR-0003 created the Platform Department and the Governance Artifact Integrity Capability; ADR-0004 fixed Workflow ownership; ADR-0007 authored the wording of invariant 15. |
| 9 | Canonical Domain Model §8: *"This document defines the conceptual domain only. It does not define, imply, or constrain repository layout, programming languages, storage technology, or APIs — those are separate, later artifacts that will be projections of this model, not extensions to it."* |
| 10 | Exhaustive lexical scan of the repository `docs/` tree returns **zero** occurrences of *Pasal*, *Master Program*, *ALMM*, *Canonical Architecture.md*, or *Volume I/II/III*. No repository document asserts an authority relationship that this decision contradicts. |

---

## 6. Standing Changes

### 6.1 Artifacts whose standing is CONFIRMED (no content change)

| Artifact | Standing after G1′ |
|---|---|
| `docs/constitution/engineering-constitution-v1.md` | The AIOS Constitution. Constitutional authority for repository governance. |
| `docs/architecture/domain-model/canonical-domain-model-v1.md` | The AIOS Canonical Domain Model. Sole semantic authority. |
| `docs/architecture/adr/README.md` | The ADR Framework, third in the Constitution §4 hierarchy. |
| `docs/architecture/adr/decisions/ADR-0001.md` … `ADR-0007.md` | Approved; unchanged; lineage intact. |
| `AIOS_ARCHITECTURE_FREEZE_v1.0.md`, `AIOS_NATIVE_CORE_BLUEPRINT_v1.0.md`, `AIOS_CANONICAL_RELATIONSHIP_MODEL_v1.0.md`, `AIOS_NATIVE_CORE_IMPLEMENTATION_ROADMAP_v1.0.md` | Projections of the Constitutional pair, per Canonical Domain Model §8. Governed by it. Unchanged. |
| The eleven Engineering Specifications under `docs/engineering/` | Projections. Governed by the Constitutional pair. Unchanged. |
| `native_core/` implementation | Governed by the Constitutional pair. Unchanged. |
| `docs/governance/AIOS_IMPLEMENTATION_CONSTITUTION_v1.0.md` | Subordinate to the Constitutional pair. Unchanged. |
| `docs/architecture/AIOS_ARCHITECTURE_CONSTITUTION_v1.0.md` | Execution Layer baseline record. Its self-declared subordination is confirmed correct. Unchanged. |

### 6.2 Artifacts whose standing CHANGES

| Artifact | Standing before | Standing after G1′ |
|---|---|---|
| Master Program Volume I, Pasal 1–6 | Presented as constitutional articles; self-flagged unvalidated (§7.1); Phase 0 criterion *"Sebagian"* | Confirmed as a **consolidation** of the original governance documents named in §2 above. Volume I §7.1's validation request is answered. |
| Master Program Volume I, Pasal 7–8 | Certified precedence and status-hierarchy rules (ARB-001) | **For repository architecture**, no longer an independent constitutional source; repository artifact precedence is Engineering Constitution §4. Within the Master Program corpus, Pasal 7–8 continue to operate as before. |
| `AIOS_CANONICAL_ARCHITECTURE.md` | Self-declared SSOT for Entity, Ownership, Dependency, Lifecycle, Relationship | **For repository architecture**, not the semantic authority; that is the Canonical Domain Model. Its ARB-002-ratified §3.1–§3.4 dependency principles remain a valid Founder-ratified record of the dependency direction the implementation follows. Its role within the Master Program corpus is unchanged by G1′. |
| Master Program Volumes II–VIII | Strategic planning and program-governance corpus | **Unchanged.** G1′ made no determination about these volumes. They continue to function as the strategic planning and program-governance corpus. |
| ALMM, Project Governance, Engineering Charter | Governance Layer under Pasal 7 | **Unchanged.** G1′ made no determination about these documents. For questions of repository governance the Constitutional pair is authoritative; G1′ decided nothing about their standing in program governance. |

### 6.3 Derived resolutions now fixed by G1′

Each of the following was previously classified **Derived** — determined by
G1′ and requiring no separate decision. Recording their resolution:

| Question | Resolution under Option A |
|---|---|
| Governing precedence scheme | Engineering Constitution §4 — Constitution → Canonical Domain Model → ADR Framework → Principle Documents → Glossary. |
| Canonical entity set | Canonical Domain Model §1 — twelve entities in four categories. |
| Trace ownership | Cross-cutting / emergent (Canonical Domain Model §3); owned by no one (§5). Not a sub-entity of Memory. |
| Workflow ownership | Owned centrally (Canonical Domain Model §5; ADR-0004, Approved). |
| Capability standing | A first-class canonical entity (Canonical Domain Model §1), Department-owned (§5), carrying invariants 1, 9, 10, 11, 14. |
| Governing ADR framework | `docs/architecture/adr/` — the repository ADR series, under Engineering Constitution §3.4. |
| Boundary/layer enumerations (ten layers, eleven modules, nine boundaries, eight layers) | Multiple **projections** of one model, expressly permitted by Canonical Domain Model §8. Not competing taxonomies and not a conflict. |
| Native Core build sequence | Governed by repository projections (Architecture Freeze §13; Native Core Implementation Roadmap). The Roadmap §18 reservation is exercised by this decision in favour of the sequence already executed and recorded (Phases 4.0–4.6). |
| GDC-001 routing (Definition→Instance multiplicity) | Domain Model semantics under Engineering Constitution §5; non-delegable (§3.2); requires an ADR under §3.4 if actioned. Remains open backlog, non-blocking. |
| GDC-002 (Agent↔Runtime mechanism) | Closed as obsolete. The dependency direction is ratified by Architecture Review Log ARB-002 and Master Program Volume V §8.2 ADR-001, and the implementation matches it. |

---

## 7. Explicitly Not Changed

- No entity, relationship, invariant, ownership rule, or lifecycle rule in the
  Canonical Domain Model is created, altered, or removed.
- No text in the Engineering Constitution is amended. Engineering Constitution
  §16: *"This Constitution may not be amended by implication."* This decision
  recognises the Constitution; it does not amend it.
- No historical ADR content is rewritten. ADR-0001…ADR-0007 retain their
  Approved status, their text, and their status histories.
- No Python source file is created, modified, or deleted. No implementation
  change is required or performed by this decision.
- No frozen or ratified document is edited.
- No prior deliverable is overwritten. This is a new, additive record.

---

## 8. External Corpus Synchronization Required

The Master Program corpus, `AIOS_CANONICAL_ARCHITECTURE.md`, ALMM, Project
Governance, and the Engineering Charter are **not present in this
repository**. They cannot be synchronized here. The following changes are
required in whatever location that corpus is maintained, and are recorded
here so the requirement is not lost:

| # | Document | Section | Required synchronization |
|---|---|---|---|
| S-1 | Master Program Volume I | §7.1 | Record that the requested validation against the original Engineering Constitution is answered by G1′, naming the two repository documents. |
| S-2 | Master Program Volume I | §8 | The Phase 0 exit criterion *"Engineering Constitution terdokumentasi formal — Sebagian"* is now satisfiable; its blocking note (*"perlu validasi terhadap dokumen sumber"*) is discharged. |
| S-3 | Master Program Volume I | Pasal 7 | Record that, **for repository architecture**, Pasal 7's precedence table is not an independent constitutional source; repository artifact precedence is Engineering Constitution §4. Pasal 7's operation within the Master Program corpus is unchanged. |
| S-4 | Master Program Volume I | Pasal 3 | Record the divergence identified during validation: Pasal 3's eight-layer chain omits **Capability** and **Workflow**, which Architecture Freeze §5 carries as frozen layers 4 and 6. Governance synchronization work, not an implementation defect. |
| S-5 | `AIOS_CANONICAL_ARCHITECTURE.md` | SSOT statement, §1, §2.1 | Record that it is not the semantic authority for repository architecture. Specifically: Trace is cross-cutting, not a Memory sub-entity; Workflow is centrally owned per ADR-0004, not Agent-owned; Capability is a first-class canonical entity. |
| S-6 | `AIOS_CANONICAL_ARCHITECTURE.md` | §7, §14 | The open Agent Instance status conflict is superseded by fact: Phases 4.0–4.6 are implemented and Phase 4.6 is closed. |
| S-7 | Master Program Volume VIII | §10.1 Artifact Registry | The Registry omits the repository Constitutional corpus, the ADR series, and the repository projections. Under G1′ these are authoritative and must be registered. |
| S-8 | Master Program Volume V | §5 Decision Log | Add the G1′ entry, per Volume V §6.2 and Volume VIII §2.2 same-day recording discipline. |
| S-9 | Master Program Volume II | §9.2 dashboard; Volume II Progress Tracker | *"AI Runtime (Phase 4) — 0%"* is superseded by fact. Update on Gate 4 certification. |
| S-10 | Architecture Review Log | new entry | Record G1′ as a Founder decision, per the Log's stated function as validation history. |

**S-1 … S-10 are governance synchronization work, not implementation
defects**, per the Founder's decision text.

---

## 9. Decision Log Entry

| Date | Decision | Tier | Decided by | Artifacts affected | Rationale (summary) |
|---|---|---|---|---|---|
| 2026-07-30 | **G1′ — Corpus Relationship: Option A.** The repository ratified pair and its ADR series are the original and authoritative AIOS Constitution and Canonical Domain Model referred to by Master Program Volume I §7.1. | Constitutional | Founder / Program Owner | Standing of Master Program Volume I Pasal 1–8 and `AIOS_CANONICAL_ARCHITECTURE.md`; confirmation of the repository corpus | Volume I §7.1 records Pasal 1–6 as a consolidation of a pre-existing Engineering Constitution never supplied to it, and requests validation against the original. The repository pair carries *Status: Canonical · Approved by: System Architect*, is mutually self-referencing, and supports a live Architect-approved ADR mechanism operating on the Domain Model itself. |

---

## 10. Ratification History

| Date | Event | Actor |
|---|---|---|
| 2026-07-29 | Governance review identifies the corpus-relationship question and reduces the Architect decision surface from twelve items to five | AI Systems Engineer |
| 2026-07-30 | Adversarial audit reduces five to two (G1, G2) | AI Systems Engineer |
| 2026-07-30 | Full-corpus validation eliminates G2 as derived; surface reduced to one (G1′) | AI Systems Engineer |
| 2026-07-30 | Decision surface validation confirms no remaining evidence gap can alter G1′ | AI Systems Engineer |
| 2026-07-30 | Founder Decision Package presented with Option A and Option B | AI Systems Engineer |
| 2026-07-30 | **Founder elects Option A. Decision ratified.** | Founder / Program Owner |
| 2026-07-30 | Decision recorded in this document under explicit Founder execution authorization | AI Systems Engineer |

---

## 11. Status History

| Status | Date | Note |
|---|---|---|
| Proposed | 2026-07-30 | Presented as G1′ in the Founder Decision Package, with Option A and Option B, evidence, consequences and implementation impact for each |
| **Ratified** | 2026-07-30 | Founder elected Option A. Binding and active immediately. Final unless amended through the constitutional amendment process (Engineering Constitution §16) |

---

## 12. Integrity Verification

- **Files created:** 1 — this document.
- **Files modified:** 1 — `docs/governance/GOVERNANCE_INDEX.md` (navigation entry only; that document carries zero independent governance authority by its own §2).
- **Python files created, modified, or deleted:** 0.
- **`execution/` changes:** 0.
- **Frozen or ratified documents modified:** 0.
- **Historical ADR content rewritten:** 0.
- **Prior deliverables overwritten:** 0. Collision check performed before writing; the path was free.
- **Historical material deleted:** none.
- **Regression:** 78/78 pass, unchanged before and after.
- **Commit status:** not committed, not pushed.

---

## 13. Closing

This document records Founder Decision G1′ and nothing else. It creates no
entity, amends no governance text, redesigns no architecture, and authorises
no implementation. The repository Constitutional corpus is confirmed, not
altered. For repository governance, the Engineering Constitution and the
Canonical Domain Model are the constitutional and semantic authority; the
Master Program continues to function as the strategic planning and
program-governance corpus. G1′ made no determination about the Master Program
beyond repository governance and repository architecture.

**No implementation, code, API, class, schema, or architecture change was
produced. The Engineering Constitution, Canonical Domain Model, ADR Framework,
ADR-0001 through ADR-0007, Architecture Freeze, Native Core Blueprint,
Canonical Relationship Model, Native Core Implementation Roadmap, Engineering
Specifications, and Implementation Constitution were not modified. This is a
new additive governance record only.**

---

## 14. Amendment Record — 2026-07-30 Wording Narrowing

Applied under a targeted Founder refinement instruction. The Founder decision
itself was **not** reopened, reinterpreted, or altered. Four statements in
this document had characterised the Master Program more broadly than G1′
decided; each is narrowed to the decided scope. The Founder's own decision
text in §2 is verbatim and was **not** touched.

| # | Location | Before | After | Why the revision is more accurate |
|---|---|---|---|---|
| W-1 | §6.2, Pasal 7–8 row | *"Retained as strategic-programme precedence rules. No longer an independent constitutional source for repository architecture."* | *"**For repository architecture**, no longer an independent constitutional source … Within the Master Program corpus, Pasal 7–8 continue to operate as before."* | The original led with a global re-characterisation before the scoping clause. The revision puts the scope first and states positively that Pasal 7–8 are unaffected elsewhere — which G1′ did not decide either way. |
| W-2 | §6.2, `AIOS_CANONICAL_ARCHITECTURE.md` row | *"A strategic-programme architecture view. Not the semantic authority for repository architecture."* | *"**For repository architecture**, not the semantic authority … Its role within the Master Program corpus is unchanged by G1′."* | *"A strategic-programme architecture view"* reclassified the document globally. G1′ determined only that it is not the semantic authority **for repository architecture**. |
| W-3 | §6.2, Volumes II–VIII and ALMM/Governance/Charter rows | *"Unchanged in function: strategic planning and governance programme above execution"* / *"subordinate to the Constitutional pair on any question the Constitution or Domain Model speaks to"* | *"**Unchanged.** G1′ made no determination about these volumes/documents."* plus, for the second row, *"For questions of repository governance the Constitutional pair is authoritative; G1′ decided nothing about their standing in program governance."* | *"subordinate … on any question"* asserted a general subordination the Founder did not decide. The revision records the absence of a determination rather than inferring one. |
| W-4 | §13 Closing | *"the Master Program corpus continues as the strategic planning and governance programme above execution"* | *"For repository governance, the Engineering Constitution and the Canonical Domain Model are the constitutional and semantic authority; the Master Program continues to function as the strategic planning and program-governance corpus. G1′ made no determination about the Master Program beyond repository governance and repository architecture."* | The original stated a global standing for the whole corpus. The revision states exactly the two things G1′ decided, and explicitly bounds the decision. |

Also revised for the same reason: **S-3** in §8, which carried the W-1 wording.

**Confirmation:** no governance meaning changed beyond this narrowing. No
authority was extended, reduced, or transferred. No implementation artifact
was modified. The decision recorded in §2 remains ratified and in force.
