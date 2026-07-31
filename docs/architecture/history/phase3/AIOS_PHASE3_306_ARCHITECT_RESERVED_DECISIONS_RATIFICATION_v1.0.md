# AIOS Phase 3.306 — Architect Reserved Decisions Ratification (Knowledge Stage V Gate) v1.0

**Type:** Architecture Decision Record (ADR). **Architecture-decision phase only** — no implementation, no Python, no Native Core change, no test, no API, no package, no storage, no commit, no push. This ADR resolves **exactly** the four Architect-reserved decisions (D1–D4) surfaced by Phase 3.305, strictly within the frozen architecture. It introduces no entity, subsystem, authority, dependency, invariant, or terminology.
**Rule 0:** all prior reports treated as untrusted navigation; frozen sources re-read directly this phase (`knowledge_spec`, 3.289 Admission Model, Relationship Model, Blueprint, Domain Model, Freeze invariant text).
**Tagging (never mixed):** **[E]** evidence from a frozen source · **[A]** architectural deduction within frozen constraints · **[O]** reserved future work. Every architectural assertion cites at least one frozen source.

---

## 1. Purpose

[A] To ratify, as canonical architecture, the four reserved decisions that gate a drift-free Stage V (Knowledge implementation): **D1 Version Identifier Scheme · D2 Version Repository Discipline · D3 Storage Strategy · D4 Retrieval/Consumption Boundary**. [E] Each was left design-open by the frozen sources (Freeze §10; knowledge_spec §12–§14/§16; Blueprint §12 "Future extension [O]: admission model, versioned repository, consumption path — reserved"). This ADR selects, among those open options, the one architecture consistent with every frozen invariant and the already-built, certified chain **Trace → Memory → Governance**. It designs no implementation and chooses no technology.

## 2. Sources Consulted (re-read directly)

[E] Architecture Freeze v1.0 (INV-4/5/6/7/8/12, OQ-2, §8 Governance authority, §10 reserved Identity/Auth) · Implementation Constitution (§3 tiers, §6.2 invariant 2, §13 reserved identifiers) · Native Core Blueprint (§5 Governance, §11 Memory, §12 Knowledge, §14 Infrastructure) · Canonical Domain Model (§5 ownership, §6 Knowledge versioning, §8 Knowledge consumable) · Canonical Relationship Model (Knowledge update-only-via-promotion; Agent Instance consumes Knowledge) · Vocabulary Freeze · governance_spec (§3 owned decision data) · knowledge_spec (§1–§14) · Phase 3.289 Admission Model · 3.295 Independent Audit · 3.296 Terminology Hardening · 3.305 Readiness Review (reserved-decision matrix).

---

## 3. Decision D1 — Version Identifier Scheme

**Decision.** [A] A Knowledge **Version** is identified by the pair **`(knowledge_item_key, version_sequence)`**:
- **`knowledge_item_key`** — a stable, governance-assigned canonical key for a Knowledge *item*, constant across all that item's versions. Basis: [E] Knowledge is "collectively owned by the Organization, each item with a home Department" (Domain Model §5; knowledge_spec §3); a governance-assigned canonical key has frozen precedent (the Tool boundary's governance-assigned `canonical_key`).
- **`version_sequence`** — a monotonic, governance-assigned ordinal, incremented once per governed admission/revision of that item. Basis: [E] "Versioned; revised/superseded via review… change means a new version, never an in-place edit" (Domain Model §6; knowledge_spec §6; 3.289 §8).

- **Identity scope** [A]: per Knowledge item within one Organization; the home Department is accountable (Domain Model §5).
- **Uniqueness** [A]: `knowledge_item_key` is unique within the Organization; `(knowledge_item_key, version_sequence)` is globally unique.
- **Immutability** [E/A]: once assigned at admission, a version's identifier is never reused, reassigned, or mutated (INV-7 durability; knowledge_spec §6 "never in-place edit").
- **Replacement behavior** [A]: a governed revision mints a **new** identifier `(same_item_key, next_sequence)`; it never edits or reuses the prior identifier (3.289 §7/§8).
- **Supersession relationship** [A]: the newer version identity supersedes the prior; the prior identifier permanently, immutably references the retained **Superseded** version. At most one **Active** version exists per `knowledge_item_key` at a time (3.289 §7).

[A] The scheme uses **no hash, signature, trust score, UUID mandate, crypto, or external service** — the identifier encodes only ownership-scoped identity and governed ordering. It is authority- and content-independent, so provenance can attach later (§11) without changing any version identity. [O] The concrete lexical form of the key and ordinal (string format, allocation mechanism) is an implementation-tier detail, not fixed here.

## 4. Decision D2 — Version Repository Discipline

**Decision.** [A] Knowledge versions live in an **append-only version record set per Knowledge item**, governed:
- **Immutable version storage** [E]: each admitted version is an immutable record; a change is a new record, never an edit (knowledge_spec §6; Blueprint §12 "preserve prior versions").
- **Superseded retention** [E]: superseded versions are retained permanently, never deleted (INV-7; Relationship Model: Knowledge must never modify itself outside governed promotion; Domain Model §6 "not casually deleted — audit trail matters").
- **Replacement rules** [A]: a governed revision **appends** a new version record and records a governed decision designating it **Active**. Canonical status (Active/Superseded) is **derived from the append-only governed-decision sequence** — the latest governed-admitted version of an item is Active, all priors Superseded — and is **not** a mutable field edited on an old record. This mirrors the already-built Governance discipline (authorization derived from an append-only, provenance-verified decision record), so **supersession needs no in-place modification** of any prior version.
- **Audit visibility** [E]: the full version history is retained and inspectable as the audit trail (Domain Model §6).
- **Retrieval guarantees** [A]: the current Active version is unambiguously resolvable (exactly one per item — 3.289 §7); every Superseded version remains retrievable.

[E/A] **INV-7 preserved; no deletion; no in-place modification** — both the version content and its governed validity conditions are fixed at admission (3.289 §14).

## 5. Decision D3 — Storage Strategy

**Decision (architectural contract only).** [A]
- **Logical storage boundary** [E]: Knowledge persists through an **Infrastructure storage facility beneath it** (Blueprint §14 "used by trace/memory/knowledge (storage)"; knowledge_spec §7 "may rely on a storage facility beneath it"), in a **Knowledge-owned partition that is separate from the Trace partition, separate from Governance's decision partition, and separate from Memory** (Memory is derive-on-read and non-persistent — memory_spec; 3.289 §12).
- **Ownership** [E]: the Knowledge subsystem owns its version records (the data); the storage facility is Infrastructure and **owns no Knowledge** (infrastructure_spec §8; Blueprint §14). Precedent: Governance owns its decision partition while Infrastructure provides the facility (governance_spec §3).
- **Dependency direction** [E]: **Knowledge → storage facility** (downward only); Infrastructure never depends on Knowledge; storage is a facility, **not an independent traced actor** (OQ-2).
- **Persistence expectations** [E/A]: durable (INV-7); append-only version records; **no delete, no in-place edit**; content and governed validity conditions immutable once admitted.

[E] **Identity/Auth compatible**: the storage contract holds no authority and no secret; the persistent, cross-process trust anchor over provenance is reserved to Identity/Authentication (Freeze §10) and can attach without changing this contract. [O] **No database or backend technology is chosen** — that remains an implementation-tier decision beneath this contract (the facility backend is replaceable, per the Infrastructure storage abstraction already built).

## 6. Decision D4 — Retrieval / Consumption Boundary

**Decision.** [A]
- **Who may consume** [E]: **Agent Instances** consume Knowledge (Domain Model §8; Blueprint — Agent Instance allowed dependency "knowledge (consume)"; Relationship Model "Agent Instance consumes Knowledge"). No consumer exists in the Native Core yet (Agent/Runtime reserved).
- **How Knowledge is located** [A]: by `knowledge_item_key` (D1), then version resolution.
- **Version lookup rules** [A]: a default read resolves the current **Active** version (exactly one — 3.289 §7). **Superseded** versions are retrievable only on an explicit `(knowledge_item_key, version_sequence)` request, are always marked Superseded, and are read-only.
- **Does Governance participate in reads / do reads require authorization** [E]: **No.** The frozen governed gate is on the **update/promotion** edge only — "Knowledge … **may update only via governed promotion (INV-8)**" (Relationship Model), and Governance "directs knowledge **admission**" (Blueprint §5). Knowledge is **consumable substrate** (Domain Model §8), read by agents with no governance gate cited. Therefore **reads are not governance-gated and Governance does not participate in reads.** Fail-closed still holds: only admitted (Active/Superseded) versions exist to read; a non-admitted candidate is not Knowledge and cannot be read as Knowledge (3.289 §15).
- **Does retrieval always return Active** [A]: yes by default; historical (Superseded) versions are exposed only on explicit versioned request, read-only, clearly labeled Superseded.

[O] **Reserved to Identity/Authentication:** *per-consumer* read authorization (which principal may consume which Knowledge) is a future Identity/Auth concern (Freeze §10); it may be layered on later **without changing** this boundary, because the baseline architectural decision is that Knowledge reads are not governed by the promotion authority. [A] No API, signature, Runtime assumption, or interface is defined here.

---

## 7. Dependency Validation

[E/A] Post-decision dependency edges for Knowledge: **Knowledge → Memory** (candidate source), **Knowledge → Governance** (read of the promotion-authorization signal), **Knowledge → Infrastructure storage facility** — exactly Blueprint §12 / knowledge_spec §7. Adding these to the certified DAG (`governance→memory`, `governance→infrastructure`, `memory→trace`, `trace→infrastructure`) yields:
- **No cycle** — nothing depends on Knowledge; Governance/Memory/Trace/Infrastructure do not reference it.
- **No dependency inversion / reverse edge** — Knowledge→Governance is a read of the signal, not a Governance dependency on Knowledge (governance_spec §8; §6.2 inv 2).
- **No Trace coupling** (D1–D4 never read/write Trace directly — 3.289 §11), **no Runtime/Agent/Execution coupling** (those don't exist; consumption by Agent Instances is reserved).
⇒ The graph remains an acyclic, strictly-downward DAG.

## 8. Authority Validation

[E] **One authority path, unchanged:** Human `HumanAuthority` → Governance `record_decision` → `promotion_authorized` (provenance-verified, reject-absolute, default-deny) → Knowledge admission (iff True) → Knowledge Version. [A] **No authority inversion:** Knowledge holds no admission/revision/supersession authority (D1–D4 all consume the Governance signal; 3.289 §13). **No hidden authority:** reads are not an authority (D4); the version identifier and repository (D1/D2) encode governed ordering, not authority; storage (D3) holds none. Automation admits nothing (§6.2 invariant 2; PR-3).

## 9. Lifecycle Validation

[E] The Knowledge lifecycle remains **exactly**:
```
Candidate  →  Governed Review  →  Active  →  Superseded
```
(3.289 §1; knowledge_spec §4). [A] D1–D4 add **no** lifecycle state: D1 identifies versions, D2 retains them, D3 persists them, D4 reads them — none introduces Archive, Historical, Deprecated, Retired, Soft-Delete, Tombstone, Confidence, Trust-Score, Ranking, or Probability. "not admitted" remains a non-state outcome of a rejected candidate. "Superseded (retained)" is the sole terminal designation; "deprecation" stays reserved to Capability/Agent Definition (3.289 §9).

## 10. Invariant Validation

[E/A] Per decision:
- **INV-4** (unconditional Trace per action) — untouched; the decision-Trace via the Agent-Instance acting path stays reserved (§12).
- **INV-5** (Trace immutable) — D1–D4 never write/mutate Trace.
- **INV-6** (capture at write-time) — Knowledge authority derives from Trace-captured Memory candidates + the governed decision; reads don't depend on later state.
- **INV-7** (durable, not casually deleted) — D2/D3 append-only, retain Superseded, no deletion/edit.
- **INV-8** (promotion only via governed review) — D1–D4 create/replace versions only on a Governance authorization; reads are not a promotion.
- **INV-12** (single external boundary) — storage is a local Infrastructure facility; Knowledge holds no external dependency.
- **PR-3 / PR-4** — no automated gate on candidates; fail-closed (no authorization ⇒ no version; only admitted versions readable).
- **OQ-2** — Knowledge storage is a facility, not an independent traced actor.
- **§6.2 invariant 2** — automation may propose/surface, never admit.
⇒ **No invariant violated; no new subsystem; no Trace/Memory/Governance mutation.**

## 11. Compatibility With Future Identity/Auth

[E/A] Every decision is Identity/Auth-forward-compatible: version identifiers (D1) encode no principal or secret; the repository (D2) records governed ordering, not identity; storage (D3) holds no authority and no trust anchor; read authorization (D4) is explicitly deferred to Identity/Auth. [E] The persistent cross-process trust anchor over the promotion signal remains reserved to Identity/Authentication (Freeze §10); today's process-scoped, fail-closed trust is unchanged and correct. Identity/Auth can later attach principal-level read control and persistent provenance **without altering** any of D1–D4.

## 12. Reserved Future Decisions

[O] Still reserved (out of scope here; each a later governed/implementation decision):
- Concrete lexical form + allocation mechanism of `knowledge_item_key` / `version_sequence` (implementation-tier under D1).
- Storage backend technology beneath the D3 facility contract.
- Validity-condition catalogue; conflict-detection signals (memory_spec §14).
- Per-consumer read authorization and persistent provenance — **Identity/Authentication** (Freeze §10).
- The Agent-Instance acting-path Trace of a governed decision (governance_spec §9 — Agent/Runtime out of scope).
- Knowledge Trust Scoring and Policy-as-Knowledge — deferred by the Domain Model.

## 13. Cross-reference Matrix

[E]

| Decision element | Frozen source |
|---|---|
| Knowledge collectively owned; home Department (D1 scope) | Domain Model §5; knowledge_spec §3 |
| Versioned; new version not in-place edit (D1/D2/D4) | Domain Model §6; knowledge_spec §6 |
| At most one Active; supersede-not-delete (D1/D2) | 3.289 §7; INV-7 |
| Preserve prior versions (D2) | Blueprint §12; knowledge_spec §6 |
| Storage facility beneath Knowledge; Infra owns no Knowledge (D3) | Blueprint §14; knowledge_spec §7; infrastructure_spec §8 |
| Storage is a facility, not a traced actor (D3) | OQ-2; knowledge_spec §9 |
| Update only via governed promotion (D2/D4 authority) | Relationship Model; Blueprint §5; INV-8 |
| Knowledge is consumable substrate, read by agents (D4) | Domain Model §8; Blueprint (Agent Instance "knowledge (consume)") |
| Fail closed: no authorization ⇒ no Knowledge (D2/D4) | PR-4; knowledge_spec §11; 3.289 §15 |
| Identity/Auth reserved (D3/D4/§11) | Freeze §10; 3.289 §16 |
| Lifecycle Candidate→Active→Superseded (D-all) | knowledge_spec §4; Domain Model §6 |

## 14. Integrity Verification

[E]
- **Files created:** 1 — this ADR (`docs/architecture/AIOS_PHASE3_306_ARCHITECT_RESERVED_DECISIONS_RATIFICATION_v1.0.md`). **Files modified:** 0. **Collision status:** path was FREE.
- **Python modified:** none. **Native Core modified:** none (`native_core/` untouched/untracked; no source diff). **Tests executed/created:** none. **Packages/storage/APIs created:** none.
- **Frozen documents modified:** none (Freeze/Domain Model/Blueprint/Relationship Model/Vocabulary/Constitution/specs untouched). **Knowledge package:** still absent.
- **execution/ touched:** no. **Staged:** 0. **Committed:** none. **Pushed:** none.

[E] **No implementation, code, API, package, storage, or test was produced. This ADR is the sole artifact.**

## 15. Final Verdict

**VERDICT: `READY`.** [A] The four reserved decisions D1–D4 are resolved **within the frozen architecture** with zero authority inversion, zero dependency inversion, zero lifecycle drift, zero terminology drift, zero invariant violation, no new subsystem, no hidden authority, and no Trace/Memory/Governance mutation (§§7–10). The Knowledge lifecycle is exactly Candidate → Governed Review → Active → Superseded. With these decisions recorded, the architecture provides an unambiguous, frozen-consistent contract for Stage V; the only remaining items (§12) are implementation-tier or belong to the reserved Identity/Auth layer and do not block a drift-free start.

[O] Formal ratification of this ADR into canon and the authorization to begin Stage V (Knowledge implementation) remain the Architect's. **This phase begins no implementation.**

---

## Mandatory Stop

[A] ADR complete. I am halting. I will not begin Knowledge implementation, scaffold packages, write Python, generate tests, redesign architecture, modify any frozen document, commit, or push. Awaiting explicit Architect authorization.
