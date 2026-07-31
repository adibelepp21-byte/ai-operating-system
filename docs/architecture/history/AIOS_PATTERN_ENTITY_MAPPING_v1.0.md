# AIOS Pattern → Entity Mapping v1.0

**Phase:** AIOS 1A.5 — inserted between Phase 1A (Canonical Pattern Catalog) and Phase 1B (DNA Consolidation).
**Type:** Authorized **synthesis / mapping** artifact. Descriptive only. The standing "no synthesis" restriction is lifted **only** for this document. Additive; ratifies nothing; promotes nothing; creates no governance rule; changes no architecture.
**Evidence sources (ONLY these):** `AIOS_CANONICAL_PATTERN_CATALOG_v1.0.md`, `AIOS_DR_VALIDATION_LOG_v1.0.md`, and the ten repository validation documents. **No repository was re-inspected; no new evidence introduced; no external search.**
**Confidence discipline:** **[E]** directly observed / recorded evidence · **[A]** reasoned abstraction · **[O]** open question / Architect decision. **No untagged conclusions.**
**Entity discipline:** maps patterns **only** to *already-ratified* Canonical Domain Model entities (Organization, Department, Capability, Agent Definition, Agent Instance, Skill, Workflow, Tool, Runtime, Knowledge, Memory, Trace) and named AIOS governance concepts. Where no ratified entity exists, this is recorded as a **gap** (§9) — **no entity is invented**.

---

## 1. Purpose

[A] **Why AIOS cannot be built directly from repositories:**
- [E] Every external repository was reviewed as *evidence, not authority* (Validation Plan §2, Authority/Evidence Inversion). Building from a repository would invert that — making an external design an AIOS requirement.
- [E] Across all ten repositories, AIOS-sense governance (immutable accountability, knowledge promotion, authority hierarchy) is **"not observed"** (Log R-4, Catalog P-A1). [A] A system built by copying repositories would therefore inherit *ungoverned* execution and **omit AIOS's defining layer**.
- [E] The corpus is saturated with **false cognates** (Catalog §7): `Trace`=observability, `Memory`=chat buffer/RAM, `Knowledge`=RAG index, `Role`=persona, `Checkpoint`=weights/graph-state, `Adapter`=LoRA/format. [A] Copying a repository's structure would import the *wrong semantics* under a right-sounding name.
- [E] AIOS invariants (inv 4/5/8/12/13) are governance constraints no external repo enforces. [A] They must be satisfied **by construction from canonical entities**, not retrofitted onto imported code.

[A] **Why implementation should originate from canonical entities:** building outward from ratified Domain-Model entities guarantees the governance invariants hold *by design*; external evidence then serves only to *corroborate or challenge* an entity's shape (as the catalog does), never to define it. [O] Whether this ordering is adopted as roadmap policy is reserved to the Architect.

## 2. Scope

- [E] This document **maps concepts** (pattern → entity → module → responsibility).
- [E] It **does not define implementation** (no code, class, API, schema, algorithm, or interface).
- [E] It **does not change architecture** and **does not ratify entities** — all mappings are *candidate* and reserved to the Architect.
- [A] It is a *bridge* artifact: it makes explicit the chain from collected evidence to a future, governed implementation, without taking any implementation step.

## 3. Transformation Pipeline

[A] The complete chain, with the discipline governing each transition:

```
Repository → Evidence → Pattern → Entity → Module → Implementation
```

| Transition | What it is | Discipline / gate |
|---|---|---|
| **Repository → Evidence** | [E] read real source read-only; extract observed facts | DR-0/DR-1: no AIOS-vocabulary leakage; boundary-honesty (in-corpus vs referenced); M-6=0 |
| **Evidence → Pattern** | [E] abstract recurrence across repos into a named pattern | Catalog §4–§6: recurrence-counted; false cognates named, not adopted |
| **Pattern → Entity** | [A] map a pattern to a *ratified* AIOS Domain-Model entity (or record a gap) | **This document**: map only to ratified entities; invent none; tag confidence |
| **Entity → Module** | [A] name the future implementation locus responsible for the entity | descriptive only; no classes/APIs; existing [BUILT] modules noted |
| **Module → Implementation** | [O] governed engineering that satisfies invariants by construction | **Not performed**; reserved to the Architect (future Phase) |

[E] The pipeline is *directional*: evidence flows up into patterns and entities; it never flows down as authority (a repository never dictates an entity). [A] The last two transitions (Module, Implementation) are **future work**; this document reaches only to *candidate* Entity→Module naming.

## 4. Canonical Pattern Inventory

[E] Patterns supported by evidence in the Catalog. Universal (P-U, external recurrence), AIOS-unique (P-A, external "not observed"), Boundary. The directive's §4 vocabulary is folded in and each item is marked by its evidence basis.

| Pattern (canonical) | Catalog ref | Evidence basis |
|---|---|---|
| Dependency Isolation | P-U1 | **[E]** n=10 (R-1) |
| Observability / Trace-as-monitoring | P-U2 | **[E]** n≥9 (R-3) — *false-cognate axis* |
| Composition | P-U3 | **[E]** n=4+2 (R-2) |
| Runtime / Execution | P-U4 | **[E]** ~6 |
| State | P-U5 | **[E]** ~5 |
| Event | P-U6 | **[E]** ~5 |
| Configuration | P-U7 | **[E]** ~6 |
| Registry | P-U8 | **[E]** ~5 |
| Storage | P-U9 | **[E]** ~6 |
| Human Review (execution-time) | P-U10 | **[E]** n=6+1 (R-5) |
| Extension | P-U11 | **[E]** n=10 |
| Workflow | P-D4 + P-U6 | **[E]** (graph/engine repos) |
| Memory | P-D6 + P-A3 | **[E]** external self-editing; AIOS governed |
| Knowledge | P-A3 | **[E]** external absent/inverted; AIOS-unique |
| Trace (immutable accountability) | P-A2 | **[E]** 0 external occurrences — AIOS-unique |
| Governance | P-A1 | **[E]** n=10 "not observed" — AIOS-unique |
| Authority | P-A4 | **[E]** Supabase data-plane only (R-8) — AIOS decision-plane unique |
| Human Governance (promotion) | P-A6 | **[E]** AIOS-unique layer |
| Capability | (Catalog §7 Skills/Capability cognate) | **[E]** external descriptor cognate; AIOS entity |
| Identity | (Catalog §7 Block/Identity cognate) | **[E]** external = tenant/auth (false cognate); AIOS = correlation key |
| False Cognate Boundary (observability≠accountability) | B-9 vs B-12 | **[E]** highest-frequency cognate (P-U2) |
| Context | — | **[A]/[O]** external "context" used loosely; **no canonical pattern extracted** |
| Resource | — | **[A]/[O]** appears in one engine repo only; **no canonical pattern** |
| Artifact | — | **[A]/[O]** AIOS governance-artifact concept; **not a corpus pattern** |
| Decision | — | **[A]/[O]** AIOS-internal (Decision Review Method); **no external corpus evidence** |

[E] The last four rows are recorded **without** claiming corpus evidence — the directive lists them, but the Catalog extracted no supporting pattern; they are carried as **candidate/gap** items (§9), not asserted.

## 5. Entity Mapping

[A] For every canonical pattern: candidate ratified AIOS entity, reason, confidence, evidence. **Candidate only — no ratification.**

- **Dependency Isolation → Tool** — [A] reason: the pattern of confining external coupling to one boundary *is* AIOS inv 12 (Tool = only entity with external dependency). Confidence **Strong**. **[E]** R-1 n=10; corroborates inv 12.
- **Runtime / Execution → Runtime** — [A] the engine-that-executes maps to the AIOS Runtime entity (binding an Agent Definition to execution). Confidence **Strong**. **[E]** P-U4; AIOS Runtime is [BUILT].
- **Workflow → Workflow** — [A] composition-of-governed-actions maps to the AIOS Workflow entity (inv 13). Confidence **Strong**. **[E]** P-D4/P-U6; AIOS Workflow [BUILT].
- **Composition → Workflow / Skill** — [A] the self-composing primitive maps onto AIOS's governed composition (Workflow) and reusable Skill; external composition is ungoverned. Confidence **Moderate**. **[E]** R-2 (shape-dependent).
- **State → (no ratified entity)** — [A] external "state" is closest to AIOS's PR-2 state/condition *principle*, not an entity. Confidence **Weak**. **[O]** gap (§9) — no entity invented.
- **Event → (no ratified entity; realized within Workflow/Runtime)** — [A] events are an execution mechanism, not an AIOS entity; the effects they carry are Trace-producing actions. Confidence **Weak**. **[O]** gap.
- **Configuration → Agent Definition / (Governance artifacts)** — [A] declarative specification maps to Agent Definition (defines an agent) and to governance artifacts for architectural config. Confidence **Moderate**. **[E]** P-U7.
- **Registry → Tool / Skill / Capability registries** — [A] named lookup maps onto the existing tool/skill registries; AIOS registry is a lookup facility, not an actor. Confidence **Moderate**. **[E]** P-U8; `tool_registry` [BUILT].
- **Storage → (infrastructure of Trace / Memory / Knowledge)** — [A] storage is a facility *under* entities, not an entity (per the OQ-2 interpretation: infrastructure is not a traced actor). Confidence **Moderate**. **[E]** P-U9.
- **Memory → Memory** — [A] direct, but with the boundary: AIOS Memory is derived and non-authoritative (inv 8), unlike external self-editing memory. Confidence **Strong (entity) / with caveat**. **[E]** P-D6/P-A3; AIOS Memory [BUILT].
- **Knowledge → Knowledge** — [A] direct; AIOS-unique governed/versioned Knowledge (Blueprint v3). Confidence **Strong**. **[E]** P-A3 (external absent/inverted).
- **Trace → Trace** — [A] direct; AIOS immutable per-action accountability (inv 4/5), distinct from all external observability. Confidence **Strong**. **[E]** P-A2; AIOS Trace [BUILT].
- **Governance → (governance modules; not a Domain-Model entity)** — [A] governance is a *process/layer* (Constitution), realized by review/promotion facilities, not a single entity. Confidence **Strong (as layer)**. **[E]** P-A1; `review_decision`, `promotion`, `governance_reader` [BUILT].
- **Authority → (Constitution §3 tiers; not an entity)** — [A] ratified authority tiers are a governance concept, not a Domain-Model entity. Confidence **Moderate**. **[E]** P-A4; Supabase data-plane is a different plane (R-8).
- **Human Governance / Human Review → review_decision (governed promotion)** — [A] AIOS human review governs *promotion* (inv 8), distinct from external execution-time gates (P-U10). Confidence **Strong (as distinct layer)**. **[E]** P-A6 vs R-5; `human_review_observation`, `review_decision` [BUILT].
- **Capability → Capability** — [A] direct; AIOS Department-owned Capability, distinct from external skill-descriptors. Confidence **Moderate**. **[E]** Catalog §7 cognate.
- **Identity → Knowledge Identity (Blueprint v3 correlation key)** — [A] AIOS Identity is a versioned-Knowledge correlation key, **not** the external tenant/auth "Identity" (Letta/Supabase false cognates). Confidence **Moderate**. **[E]** Catalog §7.
- **Agent (external) → Agent Definition + Agent Instance** — [A] external "agent" (persona/runtime loop) maps onto AIOS's *two* governed entities (definition vs instance). Confidence **Strong (distinction)**. **[E]** cognate across CrewAI/OpenHands/LangGraph/LlamaIndex.
- **False Cognate Boundary → (discipline, not entity)** — [A] the observability(B-9)/accountability(B-12) separation is a *design boundary* AIOS must preserve, not an entity. Confidence **Strong (as boundary)**. **[E]** P-U2 (highest-frequency cognate).
- **Context / Resource / Artifact / Decision / State / Event** — [O] **no ratified entity**; carried to Gap Analysis (§9); none invented.

## 6. Entity → Module Mapping

[A] Descriptive future-module loci. **Existing [BUILT]** = already present in the `execution/` layer per the Log/prior phases; **[O] future** = not yet built. No classes/APIs defined.

| Entity / Concept | Module (descriptive) | Status |
|---|---|---|
| Agent Definition | `agent/` (agent_definition) | **[E] [BUILT]** |
| Agent Instance | `agent/` (agent_instance) | **[E] [BUILT]** |
| Runtime | `runtime/` | **[E] [BUILT]** |
| Workflow | `workflow/` | **[E] [BUILT]** |
| Skill | `skill/` | **[E] [BUILT]** |
| Tool | `tool/` (tool, executor, registry) | **[E] [BUILT]** |
| Trace | `trace/` | **[E] [BUILT]** |
| Memory | `memory/` | **[E] [BUILT]** |
| Knowledge | `knowledge/` | **[A] partial** (Blueprint v3 designed; repository/admission [O] future) |
| Governance (review/promotion) | `governance/` (review_decision, promotion, governance_reader, memory_governance) | **[E] [BUILT]** |
| Capability | `capability/` | **[O] future** (Domain-Model entity; module not yet built) |
| Organization / Department | `organization/` | **[A] partial** (governance-artifact docs exist; runtime module [O]) |
| Registry | (within `tool/`, `skill/`) | **[E] [BUILT]** (as lookup facilities) |
| Infrastructure / Storage | `infrastructure/` | **[O] future** (facility under entities; not a traced actor per OQ-2) |
| Identity (Knowledge correlation key) | (within `knowledge/`) | **[A] design-only** (Blueprint v3) |
| Context / Resource / Artifact / Decision / State | — | **[O] no module** (no ratified entity; see §9) |

[E] The Entity→Module mapping reuses the *existing* module names where they are already [BUILT]; it invents no new entity and defines no interface.

## 7. Implementation Responsibilities

[A] Architectural responsibility only — no algorithms, interfaces, or code.

- **`agent/`** — represent an Agent Definition and instantiate governed Agent Instances; every Instance action must be attributable to exactly one Trace record (inv 4).
- **`runtime/`** — bind a definition to an execution context; a lookup/binding facility, not an independent traced actor (OQ-2 interpretation).
- **`workflow/`** — compose governed Agent-Instance actions; enforce that collaboration occurs only via Workflow/Knowledge/scoped Memory (inv 13).
- **`tool/`** — the sole locus of external dependency (inv 12); register, execute, and verify tool calls.
- **`trace/`** — produce unconditional, immutable, append-only, one-per-action accountability records (inv 4/5, §14.2); **never** an observability/monitoring facility (B-9≠B-12).
- **`memory/`** — derive non-authoritative Memory from Trace; **never** auto-promote (inv 8).
- **`knowledge/`** — hold governed, versioned Knowledge; accept promotions only via governed review; store immutable versions (Blueprint v3).
- **`governance/`** — record human review decisions, run promotion under governance, read governance state; detect, do not decide (PR-3); fail closed (PR-4).
- **`capability/`** *(future)* — represent a Department-owned Capability and its cross-department dependencies (inv 10 requires governance).
- **`organization/`** *(partial/future)* — represent Organization/Department ownership and accountability boundaries (DM §5).
- **`infrastructure/`** *(future)* — provide persistence/lookup facilities *beneath* entities; audited through the action that invokes them, never as an independent actor (OQ-2 interpretation).

[E] Each responsibility is stated as a governance/architectural obligation, not an implementation. [O] The actual construction of any module is reserved to a future authorized Phase.

## 8. Pattern Coverage Matrix

[A] Descriptive. **No repository comparison.**

| Pattern | Candidate Entity | Module | Evidence Strength | Coverage | Confidence |
|---|---|---|---|---|---|
| Dependency Isolation | Tool | `tool/` | **[E] Strong** (n=10) | Covered | Strong |
| Runtime/Execution | Runtime | `runtime/` | **[E]** ~6 | Covered | Strong |
| Workflow | Workflow | `workflow/` | **[E]** engines | Covered | Strong |
| Trace (accountability) | Trace | `trace/` | **[E] Strong** (unique) | Covered | Strong |
| Memory | Memory | `memory/` | **[E]** (with caveat) | Covered | Strong |
| Knowledge | Knowledge | `knowledge/` | **[E]** (unique) | Partial | Moderate |
| Governance | (layer) | `governance/` | **[E] Strong** (unique) | Covered | Strong |
| Human Review (promotion) | review_decision | `governance/` | **[E]** (unique layer) | Covered | Strong |
| Capability | Capability | `capability/` | **[E]** (cognate) | Not yet | Moderate |
| Composition | Workflow/Skill | `workflow/`,`skill/` | **[E]** n=4+2 | Covered | Moderate |
| Registry | (facility) | `tool/`,`skill/` | **[E]** ~5 | Covered | Moderate |
| Storage | (infrastructure) | `infrastructure/` | **[E]** ~6 | Not yet | Moderate |
| Configuration | Agent Definition | `agent/` | **[E]** ~6 | Partial | Moderate |
| Authority | (Constitution §3) | `governance/` | **[E]** (data-plane only externally) | Partial | Moderate |
| Identity | Knowledge correlation key | `knowledge/` | **[E]** (cognate) | Design-only | Moderate |
| State | — | — | **[A]** ~5 | **Gap** | Weak |
| Event | — | (within runtime/workflow) | **[A]** ~5 | **Gap** | Weak |
| Context | — | — | **[O]** none | **Gap** | Weak |
| Resource | — | — | **[O]** none | **Gap** | Weak |
| Artifact | — | — | **[O]** none | **Gap** | Weak |
| Decision | — | `governance/` (ADR/review) | **[O]** AIOS-internal | **Gap (external)** | Weak |

## 9. Gap Analysis

[E]/[A]/[O] patterns with no entity, weak evidence, or open interpretation. **No missing entity is invented.**

- [O] **State** — recurs externally (~5) but AIOS models it as a *principle* (PR-2 state/condition), not an entity. Open: whether AIOS needs a first-class State/Context entity, or whether PR-2 + Trace suffice. **No entity created.**
- [O] **Context** — used loosely externally; no canonical pattern was extracted; AIOS has no ratified Context entity. Open interpretation.
- [O] **Resource** — appears in one engine repo only; insufficient recurrence; no AIOS entity. Future validation required before any entity is considered.
- [O] **Artifact** — AIOS has a *governance-artifact* concept (Meta Model types) but no Domain-Model **Artifact** entity; mapping is ambiguous. Reserved.
- [O] **Decision** — an AIOS-*internal* concept (Decision Review Method, ADRs); the external corpus provides **no** supporting evidence. Its entity/module status is an internal-architecture question, not a corpus-derived one.
- [A] **Capability** — ratified entity exists but **no module built yet** and external evidence is only a descriptor-cognate; weak external corroboration.
- [A] **Authority** — ratified as Constitution §3 tiers, but the only external analog (Supabase) is a *different plane* (data-access); external evidence does not corroborate decision-plane authority.
- [E] **Knowledge admission / repository** — Blueprint v3 designed the versioned Knowledge model, but admission (Option B) and the repository/service remain **[O] open** (per the Knowledge design docs); coverage is partial.
- [A] **Observability vs Accountability boundary** — a *discipline* with no entity; must be preserved as AIOS builds `trace/` so it never degrades into monitoring (the corpus's highest-frequency cognate).

[O] Every gap is reserved to the Architect; none is resolved here.

## 10. Cross-Consistency Review

[E] Checked against each source; the mapping introduces no rule and contradicts none.

- [E] **Constitution:** the pipeline reserves all ratification/implementation to the Architect (§6.2 invariant 2 upheld); no authority added, nothing automated. **Consistent.**
- [E] **Canonical Domain Model:** mappings target only ratified entities; invents none; the Memory/Knowledge/Trace mappings respect inv 4/5/8/12/13. **Consistent.**
- [E] **Principles Register:** PR-1 (Evidence First) is the mapping's basis; PR-2/PR-3/PR-4/PR-5 are cited as responsibilities, not altered. **Consistent.**
- [E] **Decision Review Method:** the pipeline's transitions mirror DR-0…DR-6 discipline (premise/grounding/evaluation/reserve-to-Architect); unchanged. **Consistent.**
- [E] **Canonical Pattern Catalog:** every pattern used is drawn from it; no pattern is added or promoted. **Consistent.**
- [E] **Validation Log:** used read-only for recurrence counts; **not modified** by this document. **Consistent.**

[E] **No inconsistency found.**

## 11. Readiness Assessment (for Phase 1B — DNA Consolidation)

[A] **Readiness to *enter* Phase 1B (not implementation readiness):**
- [E] The transformation chain (Evidence→Pattern→Entity→Module→Responsibility) is now explicit and consistent with all canonical sources (§10).
- [E] The ratified Domain-Model entities have candidate module loci and stated responsibilities; the AIOS-unique layer (Governance/Trace/Knowledge-Promotion/Authority) is clearly distinguished from external patterns.
- [A] Therefore AIOS is **conceptually ready to enter DNA Consolidation** — the mapping provides the concept-level substrate DNA Consolidation would consolidate.
- [O] **Conditions the Architect must weigh before Phase 1B:** several gaps remain open (§9 — State/Context/Resource/Artifact/Decision have no ratified entity; Capability/infrastructure modules unbuilt; Knowledge admission open). [O] Whether these must be closed *before* 1B, or *within* 1B, is an Architect decision.
- [E] **Not assessed:** implementation readiness (explicitly out of scope).

## 12. Open Questions (reserved to the Architect; not resolved)

- [O] Do State/Context warrant a first-class AIOS entity, or do PR-2 + Trace + Runtime cover them?
- [O] Is there a Domain-Model **Artifact** entity distinct from governance-artifact *types*, or not?
- [O] What is the entity/module status of **Decision** (AIOS-internal; no external corpus evidence)?
- [O] Should **Resource** be admitted as an entity, or remain an infrastructure facility?
- [O] Which of the §9 gaps must close **before** Phase 1B versus **within** it?
- [O] The standing **reviewer-independence** limit (Plan §9) — does corpus-independence alone suffice to treat any mapped pattern as corroborated?
- [O] The candidate methodology refinements **MF-1…MF-12** (Log) remain open, not enacted.
- [O] Whether any candidate Entity→Module mapping herein should be **ratified** — reserved entirely to the Architect.

---

## Closing

[E] This document maps the evidence-derived canonical patterns to *already-ratified* AIOS entities and candidate future modules, establishing the transformation chain Evidence → Pattern → Entity → Module → Implementation-Responsibility **without performing implementation**. [A] Its disciplined result: the ratified entities (Agent, Runtime, Workflow, Tool, Trace, Memory, Knowledge, Capability) receive candidate module loci and governance responsibilities; several directive-listed concepts (State, Context, Resource, Artifact, Decision) have **no ratified entity** and are recorded as gaps, not invented. [O] All ratification, gap-closure, and progression to Phase 1B are reserved to the Architect.

**No implementation, code, schema, API, interface, or algorithm was produced. No prior validation document was modified. The Validation Log was not modified. No governance rule was created; no observation was promoted to a principle; the Architecture Specification was not updated. This is a new additive synthesis document only.**
