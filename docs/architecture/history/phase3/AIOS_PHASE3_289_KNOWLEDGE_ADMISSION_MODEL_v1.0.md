# AIOS Phase 3.289 — Knowledge Admission Model v1.0

**Phase:** AIOS 3.289 — Knowledge Admission Model. **Architecture-governance decision only.** No implementation, no Python, no Knowledge source/storage/API/tests. This document resolves the reserved admission-model item (knowledge_spec §4/§14; Freeze §10; Implementation Readiness Review §18 condition 1) **within** the frozen architecture, introducing no new entity, authority, dependency, subsystem, invariant, or terminology.
**Immutable basis** [E]: Architecture Freeze v1.0 · Canonical Domain Model · Native Core Blueprint · Constitution · governance_spec · knowledge_spec. Every frozen invariant is preserved; nothing above this document is modified.
**Tagging (never mixed):** **[E]** evidence from the frozen sources · **[A]** architecture design (the governed decision) · **[O]** reserved to the Architect / later governed decision.

---

## 0. Purpose & Non-Change Statement

[A] To define **how a Memory candidate becomes durable, authoritative Knowledge** — the admission lifecycle, gate, and policies — so that a future Knowledge subsystem can be built with no ambiguity, while every frozen invariant holds.
[E] Knowledge is entered **only** through governed promotion (INV-8); it is durable and not casually deleted (INV-7). This document changes no architecture: it selects, among the design-open options the frozen documents left [O], the model consistent with the frozen invariants and the already-built Trace → Memory → Governance chain.

## 1. Admission Lifecycle

[E] The lifecycle is exactly the one knowledge_spec §4 fixes, with no added states:
```
Memory candidate  →  governed review (human decision)  →  [authorized approve] → Active Knowledge version
                                                        →  [reject]            → not admitted (remains a candidate/observation)
Active version  →  (governed revision)  →  new Active version + prior version Superseded (retained)
```
[A] Named states, all pre-existing (Domain Model §6; knowledge_spec §4): **Candidate** (a Memory observation), **Active version** (admitted, canonical), **Superseded version** (replaced by a later governed revision, retained), and the non-state outcome **not admitted** (a rejected/unauthorized candidate is simply still a candidate). No "draft", "pending-auto", or "provisional-knowledge" state exists — a thing is either a Memory candidate or admitted Knowledge, never a half-authoritative intermediate (fail closed).

## 2. Candidate Eligibility

[E] The **only** candidate source is Memory (knowledge_spec §7; Blueprint §12). A candidate is a Memory promotion candidate — a surfaced, non-authoritative observation `(scope, observed_content, occurrence_count)` (the existing `PromotionCandidate`).
[A] **Eligibility to be reviewed is unconditional** (Detect, Don't Decide — PR-3): Memory surfaces every distinct observation, gating nothing; `occurrence_count` may prioritise a reviewer's attention but never qualifies or disqualifies a candidate.
[E] **Eligibility to be admitted is not automatic** — it requires governed authorization (INV-8). [A] Consistent with the Domain Model's deliberate choice that promotion is a **binary, low-volume, governed** decision (Knowledge Trust Scoring is explicitly deferred, Domain Model §"Deferred"), there is **no** confidence threshold, ML ranking, or automated eligibility filter — none may gate admission (PR-3).

## 3. Human Approval Requirements

[E] Admission requires a **human** governed-review decision to approve promotion; automation may propose candidates and surface conditions but may never admit (INV-8; PR-3; Constitution §6.2 invariant 2).
[A] Concretely, admission requires the Governance subsystem's promotion authorization to be **True**, which (per the built Governance boundary, Phases 3.28/3.286/3.288) is granted only by a **provenance-verified human decision carrying `HumanAuthority`**, with a human `reject` absolute and the default deny. No new authority is introduced — this is the ratified decision authority of Constitution §3, exercised by Governance.

## 4. Promotion Gate

[E] There is exactly **one** gate on the Memory→Knowledge edge: the Governance subsystem's **promotion authorization** (the frozen governed-review boundary; Freeze §8; INV-8).
[A] Knowledge admits a candidate **if and only if** Governance authorizes that candidate's promotion (`promotion_authorized(candidate)` is True). **Knowledge itself makes no admission decision** — it consumes the governance signal and records the durable authoritative outcome. This preserves the chain **Trace → Memory → Governance → Knowledge** and creates no authority in Knowledge (no authority inversion). [E] The gate is fail-closed: default deny (§5, §15).

## 5. Rejection Semantics

[E] A human `reject` is **absolute**: the candidate is **not** admitted, no Knowledge is created, and nothing is deleted (knowledge_spec §11; the built reject-absolute rule).
[A] A rejected candidate **remains a candidate/observation** — never silently authoritative (knowledge_spec §11). A recorded reject permanently denies *that* promotion decision; it is not overridden by a later approve on the same evidence (reject absolute). A new governed review over **new evidence** is a distinct decision (see §10). Rejection produces no version and no deletion.

## 6. Conflict Handling

[A] A conflict is two candidates that disagree, or a candidate that contradicts an existing Active version. Because the Domain Model fixes **binary canonical status** and defers trust scoring, conflict is resolved by **governed human review**, never automatically (PR-3): a conflicting candidate does **not** auto-supersede canonical Knowledge.
[A] Flow: Memory may surface the conflicting observations as candidates (conflict-detection signals are [O] reserved — memory_spec §14); Governance/human decides which, if any, is admitted or which Active version is revised. No automatic arbitration, no automated tie-break, no ranking decides — only a human governed decision (INV-8; §6.2 invariant 2). Absent a governed decision, the existing Active version stands unchanged (fail closed).

## 7. Canonical Replacement Rules

[E] Replacement is a **governed revision** that admits a new Active version and marks the prior Active version **Superseded** — the prior version is **preserved, never overwritten or deleted** (INV-7; knowledge_spec §6).
[A] Replacement requires the **same** governed authorization as admission (a human approve via Governance). Only the governed review may designate a new canonical (Active) version; nothing in execution, Memory, or automation may replace canonical Knowledge (INV-8). At most one Active version is canonical for a given Knowledge item at a time; superseded versions remain as the audit trail.

## 8. Versioning Policy

[E] Change means a **new version, never an in-place edit** (knowledge_spec §6; Domain Model §6: "Versioned; revised/superseded via review"). Each admission and each governed revision creates a new version; prior versions are retained (audit trail matters — Domain Model §6).
[A] Each version carries a **binary canonical status** (Active or Superseded) and governed **validity conditions** set by the review (knowledge_spec §6) — no trust score (deferred). [O] The **version-identifier scheme** and **versioned-repository discipline** are reserved (Implementation Constitution §13; Freeze §10; Architecture Review R-A4) — a later governed implementation decision, not fixed here.

## 9. Supersession (Governed)

[E] Knowledge is **durable and not casually deleted** (INV-7); "not casually deleted — audit trail matters" (Domain Model §6).
[A] Superseding a version is a **governed decision** that marks that version **Superseded** through governed review; the record is **retained**, never physically deleted. Supersession requires governance authority (a human governed decision); there is **no automatic supersession** and no execution-driven deletion. A **Superseded (retained)** version is not erased — mirroring the built Governance discipline that a decision, once recorded, is permanent. (This is the canonical Knowledge lifecycle vocabulary — "Superseded", per Domain Model §6 and knowledge_spec §4; the frozen term "deprecation" applies to Capability/Agent Definition, not Knowledge.)

## 10. Re-evaluation Policy

[A] A rejected or superseded candidate **may be re-submitted** for a **new** governed review when **new evidence** (new Memory observations) exists. Re-evaluation is a distinct governed decision producing a new outcome — it does **not** override a prior human `reject` (reject absolute); it is a fresh decision over fresh evidence.
[E] Until a new authorized approve exists, the default remains **deny** (PR-4). [A] Re-evaluation introduces no automatic promotion and no automated reconsideration loop — reconsideration is human-initiated and human-decided (PR-3; §6.2 invariant 2).

## 11. Trace Relationship

[E] Admission and revision are **governed decisions**, accountable through the acting reviewer/Instance path that authors them (INV-4 applies to that acting path; knowledge_spec §9). Knowledge **storage is a facility, not an independent traced actor** (OQ-2).
[A] Knowledge derives its authority from **Trace-derived Memory candidates** (evidence captured at write-time, INV-6) plus the **governed decision** (recorded by Governance). Knowledge **never writes or mutates Trace** (INV-5); Trace is strictly upstream evidence. The full Agent-Instance acting-path Trace of a governed decision attaches when Agent/Runtime exist ([O] reserved — governance_spec §9; the current Governance records decisions as its own §3 audit data).

## 12. Memory Relationship

[E] Memory is the **sole candidate source** (knowledge_spec §7); candidates are Memory observations, provisional and non-authoritative. Memory **never self-promotes** (INV-8).
[A] Knowledge **reads candidates** only through the governed surface (Governance surfaces Memory candidates for review); Knowledge **never modifies, writes, or mutates Memory**. Memory remains derive-on-read and recomputable from Trace; admission neither persists into Memory nor changes it.

## 13. Governance Relationship

[E] Knowledge **depends on Governance (promotion authority) and Memory (candidate source)** — exactly Blueprint §12 and knowledge_spec §7; no new dependency. Governance **decides**; Knowledge **records the durable authoritative outcome** of an authorized decision.
[A] Knowledge holds **no authority of its own** — it cannot admit, revise, or supersede a version without a Governance authorization (no authority inversion). Governance cannot be overridden by, or made dependent on, Knowledge or execution (governance_spec §8; §6.2 invariant 2). The direction is strictly **Governance → (authorizes) → Knowledge**; Knowledge → Governance is a read of the authorization signal only.

## 14. Knowledge Immutability

[E] A Knowledge **version, once admitted, is immutable**: change means a **new version**, never an in-place edit (knowledge_spec §6). Prior versions are preserved (INV-7).
[A] Distinction (no terminology drift): **Trace** is immutable *append-only per action* (INV-5); **Knowledge** is *durable, versioned, and superseded-not-deleted* (INV-7). Both forbid in-place mutation and deletion of the record, by different frozen invariants. An Active version's content and its governed validity conditions are fixed at admission; a revision produces a new version and supersedes (retains) the old one.

## 15. Fail-Closed Behaviour

[E] **Absence or non-authorization of a promotion decision ⇒ no Knowledge is created or changed** (knowledge_spec §11; PR-4). An unadmitted candidate remains a candidate, never silently authoritative.
[A] Concretely: Knowledge treats any non-`True` promotion authorization as **deny**; ambiguous or missing authority halts (creates/changes nothing); the default state of any candidate is **not Knowledge**. [A] Post-F-G1/F-H1, the governance authorization signal is provenance-verified and its recorded snapshots are immutable — Knowledge must still consume the signal fail-closed (verify authorization is affirmatively True, never infer admission from mere candidate existence). Persistent cross-process integrity of that signal is reserved to Identity/Auth ([O], §16).

## 16. Reserved Items

[O] Deliberately not decided here (each a later governed decision):
- Version-identifier scheme; versioned-repository discipline (Freeze §10; Impl Constitution §13).
- The **read/consumption path** — whether Knowledge consumption itself needs governance (Relationship Model §13; knowledge_spec §14).
- Storage-facility choice beneath Knowledge (knowledge_spec §7; Freeze §10).
- Validity-condition catalogue; conflict-detection signals (memory_spec §14).
- **Knowledge Trust Scoring** — deferred by the Domain Model (binary canonical status suffices now).
- **Policy as a category of Knowledge** — deferred by the Domain Model; not modeled here.
- Persistent cross-process trust of the promotion signal — reserved to **Identity/Authentication** (Freeze §10); process-scoped fail-closed trust is current.
- The Agent-Instance acting-path Trace of a governed decision (governance_spec §9 — Agent/Runtime out of scope).
- F-H2 (in-process isolation) and F-G2 (content-key robustness) — carried, out of scope.

## 17. Explicit Mapping

[E]

| This model's decision | Frozen source |
|---|---|
| Entry only via governed promotion; never automatic | **INV-8**; knowledge_spec §1/§5/§10; Blueprint §12 |
| Durable; not casually deleted; superseded-not-deleted | **INV-7**; Domain Model §6; knowledge_spec §2 |
| Human decides; automation may propose/surface only | **Constitution §3, §6.2 invariant 2**; PR-3; governance_spec §10 |
| Single promotion gate = Governance authorization | **Freeze §8**; governance_spec §1/§2/§5; Blueprint §5 |
| Candidate source = Memory; non-authoritative | Domain Model §5; knowledge_spec §7; memory_spec |
| Candidate/Active/Superseded lifecycle | knowledge_spec §4; Domain Model §6 |
| Versioned; new version not in-place edit; preserve prior | knowledge_spec §6; Domain Model §6 |
| Binary canonical status; no trust scoring | Domain Model §"Deferred" (Knowledge Trust Scoring) |
| Fail closed: no authorization ⇒ no Knowledge | **PR-4**; knowledge_spec §11 |
| Knowledge storage a facility, not a traced actor | **OQ-2**; knowledge_spec §9 |
| Dependencies: Governance + Memory (+ storage facility) | Blueprint §12; knowledge_spec §7 |
| Knowledge never mutates Trace/Memory; no authority | INV-5; knowledge_spec §8; governance_spec §8 |

## 18. Validation Summary

[A] Verified against the required checks:
- **No architecture drift** — no entity, layer, boundary, or relationship is added or changed; only the reserved admission-model [O] is resolved within existing structure.
- **No invariant drift** — INV-7, INV-8, INV-5, INV-6, PR-3, PR-4, §6.2 invariant 2, OQ-2 are cited and preserved; none is added, weakened, or redefined.
- **No dependency change** — Knowledge → Governance + Memory (+ storage facility), exactly Blueprint §12 / knowledge_spec §7; no reverse or new dependency.
- **No authority inversion** — Governance authorizes; Knowledge records; Knowledge holds no admission authority; automation admits nothing.
- **No terminology conflict** — Candidate, Admission, Active/Superseded version, Promotion, Revision, Supersession are used per Domain Model / knowledge_spec; the Knowledge lifecycle vocabulary is exactly {Candidate, Active, Superseded} (no "deprecation" for Knowledge — that term is reserved for Capability/Agent Definition); consistent with Vocabulary Freeze (Memory≠Knowledge, Promotion = governed Memory→Knowledge, Authority = decision authority).
- **No duplication; one authoritative definition** — this document defines only the admission *model* (the reserved [O]); it does not restate or fork the Domain Model, Freeze, or specs, which remain the single authority for entities/invariants.

## 19. Integrity Verification

[E]
- **Files created:** 1 — this document (`docs/architecture/AIOS_PHASE3_289_KNOWLEDGE_ADMISSION_MODEL_v1.0.md`). **Files modified:** 0.
- **Python / Native Core modified:** none — no implementation, no Knowledge source/storage/API/tests.
- **Architecture Freeze / Domain Model / Blueprint / Constitution / Engineering Specs modified:** none — the only tracked working-tree diff (`governance-artifact-integrity-agent.md`) predates this session and was not touched.
- **execution/ untouched; Trace corpus unchanged (540).**
- **Collision check:** the deliverable path was FREE before writing.
- **Commit status:** nothing staged, nothing committed, nothing pushed.

## 20. Readiness Assessment

- [A] **Admission model — DEFINED and frozen-invariant-consistent.** A future Knowledge subsystem can be built to this model: admit a candidate iff Governance authorizes it; version rather than edit; supersede-not-delete; fail closed on non-authorization; human-decided throughout.
- [A] **Knowledge implementation readiness — CONDITIONAL:** the model is ready; implementation additionally requires the [O] reserved items to be decided *when built* (version-identifier scheme, versioned-repository discipline, storage facility, consumption path) — these are implementation-tier decisions under this model, not blockers to the model itself.
- [O] **Ratification of this model into canon, and authorization to begin Knowledge implementation (Phase 3.29), are reserved to the Architect.** This document begins no implementation.

---

## Closing

[A] This Knowledge Admission Model resolves the reserved admission question strictly within the frozen architecture: Knowledge admits a Memory candidate **only** on a human-authorized governed promotion (INV-8), is **versioned rather than edited** and **superseded rather than deleted** (INV-7), resolves conflicts and version supersession by **governed human decision** (PR-3; §6.2 invariant 2), and **fails closed** on any absence of authorization (PR-4). It introduces no new entity, authority, dependency, subsystem, invariant, or terminology, preserves the Trace → Memory → Governance → Knowledge chain, and places no authority in Knowledge itself. [O] Every reserved item, the model's ratification, and the authorization to begin Knowledge implementation remain the Architect's.

**No implementation, Python, Knowledge source, storage, API, or test was produced. No Architecture Freeze, Domain Model, Blueprint, Constitution, Engineering Specification, Vocabulary, or DNA Library was modified. No new entity, authority, dependency, subsystem, invariant, or terminology was introduced. execution/ is untouched and the Trace corpus is unchanged (540). This is a single additive, architecture-only decision document. Phase 3.29 is not begun.**
