# AIOS Canonical Vocabulary v1.0

**Phase:** AIOS 1A.9 — Canonical Vocabulary & Glossary. The **final synthesis before Phase 1B (DNA Consolidation)**.
**Type:** Authorized **descriptive** synthesis. Freezes AIOS terminology so every future document uses one canonical language. Additive; ratifies nothing new; invents no entity/relationship/architecture; renames nothing; modifies no prior document.
**Evidence sources (ONLY these):** Constitution · Canonical Domain Model · Principles Register · Decision Review Method · Validation Log · the ten repository validation documents · `AIOS_CANONICAL_PATTERN_CATALOG_v1.0.md` · `AIOS_PATTERN_ENTITY_MAPPING_v1.0.md` · `AIOS_CANONICAL_RELATIONSHIP_MODEL_v1.0.md`. **Nothing else. No external repositories, no internet, no new evidence.**
**Confidence discipline:** **[E]** observed / stated in a ratified or prior source · **[A]** reasoned abstraction · **[O]** Architect decision / future work. **No untagged conclusions.**
**Status vocabulary:** **Ratified** = defined in the ratified canon (Constitution / Domain Model / Principles); **Observed** = consistently used across prior synthesis docs but not a ratified entity; **Architect Reserved** = **[O]** term deliberately *not* defined here (no ratified basis; reserved).

---

## 1. Purpose

[A] **Why language consistency is required before implementation:**
- [E] The corpus's single highest-frequency failure mode is the **false cognate** (Catalog §7; Log R-3, n≥9): the same word (`Trace`, `Memory`, `Knowledge`, `Role`, `Checkpoint`, `Adapter`) carries incompatible meanings across systems. [A] Without a frozen canonical vocabulary, implementation would silently import a repository's meaning under an AIOS name — the exact error DR-1 exists to prevent.
- [E] AIOS's invariants are relational and word-bound: inv 4 ("Agent Instance action → Trace"), inv 8 ("Memory → Knowledge via governed review") only hold if `Trace`, `Memory`, and `Knowledge` mean exactly one thing (Relationship Model §5–§8). [A] Ambiguous terms would make the invariants unenforceable.
- [A] A shared canonical language is the precondition for DNA Consolidation: Phase 1B can only consolidate what is unambiguously named.

## 2. Scope

- [E] This document defines **terminology only** — names, definitions, and their relation to ratified entities/patterns/relationships.
- [E] It defines **no behavior, no implementation, no architecture, no API, no algorithm.**
- [A] It is a *dictionary and boundary*, not a specification. All ratification of Reserved terms is the Architect's.

## 3. Canonical Vocabulary

[E]/[A] For each term: Definition · Purpose · Related Entity · Related Pattern · Related Relationship · Evidence Source · Confidence · Status.

### 3.1 Ratified Domain-Model Entities (Status: **Ratified**)

| Term | Definition (canonical) | Related Pattern | Related Relationship | Evidence | Conf. |
|---|---|---|---|---|---|
| **Organization** | The top of the governed hierarchy; accountability root | (Org layer) | owns Department | [E] DM §5 | Strong |
| **Department** | An ownership/accountability unit under an Organization | Ownership | owns Capability/Agent Definition | [E] DM §5 | Strong |
| **Capability** | A named, Department-owned ability | Capability (Catalog) | exposes Skill/Workflow; cross-Dept dep needs governance (inv 10) | [E] DM, inv 10 | Strong |
| **Agent Definition** | The template of an agent | Configuration | referenced by Agent Instance | [E] DM §6 | Strong |
| **Agent Instance** | A runtime execution of an Agent Definition; the **only actor** | Runtime/Execution | produces Trace (inv 4); coordinated by Workflow (inv 13); uses Tool/Skill; consumes Knowledge | [E] DM §6, inv 4/13 | Strong |
| **Workflow** | A governed composition of Agent-Instance actions | Workflow/Composition | coordinates Agent Instances (inv 13) | [E] DM, inv 13 | Strong |
| **Runtime** | The execution binding of a Definition; a **facility, not an actor** | Runtime | creates Agent Instance; executes Workflow | [E] DM §6; [A] Mapping (OQ-2) | Strong |
| **Skill** | A reusable unit of agent ability | Composition/Registry | used by Agent Instance; contained in Workflow | [E] DM | Strong |
| **Tool** | The **only** entity permitted an external dependency | Dependency Isolation | used by Agent Instance; depends_on external (inv 12) | [E] inv 12 | Strong |
| **Memory** | Derived, **non-authoritative** memory, produced from Trace | Memory | reads Trace (§6.1); promoted to Knowledge only via governed review (inv 8) | [E] DM §6.1, inv 8 | Strong |
| **Knowledge** | Governed, authoritative knowledge; cross-cutting substrate | Knowledge | entered only via governed promotion (inv 8); consumed by Agent Instances | [E] DM inv 8, §8 | Strong |
| **Trace** | The **immutable, append-only, one-per-action** accountability record | Trace (accountability) | produced by Agent Instance (inv 4); read by Memory | [E] inv 4/5, §14.2 | Strong |

### 3.2 Governance & Process Concepts (Status: **Ratified**, unless noted)

| Term | Definition | Related Entity | Evidence | Conf. | Status |
|---|---|---|---|---|---|
| **Governance** | The layer/process that authorizes, promotes, and holds accountable — over decisions and knowledge | (layer; not a DM entity — Mapping §5) | [E] Constitution; Catalog P-A1 | Strong | Ratified (layer) |
| **Authority** | Ratified decision tiers governing what may change and who may approve | (Constitution §3) | [E] Constitution §3 | Strong | Ratified |
| **Review** | The governed human evaluation that decides a promotion/decision | Memory→Knowledge (inv 8); review_decision | [E] DM inv 8; DR Method | Strong | Ratified |
| **Promotion** | The governed transition of Memory into Knowledge (never automatic) | Memory → Knowledge (inv 8) | [E] DM inv 8 | Strong | Ratified |
| **Decision** | A recorded architectural decision (ADR / Decision-Review output) | (governance artifact; no DM entity — Mapping §9) | [E] DR Method; Constitution §3 | Moderate | Ratified (as ADR/process) |
| **Observation** | A *governance observation* (e.g. human-review observation) — **not** execution observability | review/governance | [E] DR Method; validation docs | Moderate | Observed |
| **Constraint** | An invariant/principle that bounds permitted interactions | Domain-Model invariants; Principles | [E] DM invariants; Principles | Strong | Ratified |
| **Responsibility** | The architectural obligation an entity/module bears | (Mapping §7; Relationship §7) | [E] Mapping/Relationship | Moderate | Observed |
| **Ownership** | The relation by which Organization/Department hold accountability | Organization/Department (DM §5) | [E] DM §5 | Strong | Ratified |
| **Lifecycle** | The governed progression of an entity (e.g. Definition → Instance) | DM §6 | [E] DM §6 | Strong | Ratified |
| **Execution** | The act of an Agent Instance running under a Runtime | Agent Instance/Runtime | [E] DM §6 | Strong | Ratified |

### 3.3 Terms Reserved (Status: **Architect Reserved [O]** — no ratified basis; not defined here)

[O] These appear in the minimum list but have **no ratified AIOS definition**; per the Mapping's Gap Analysis (§9), no entity was invented. Each is reserved.

| Term | Why reserved | Evidence | Status |
|---|---|---|---|
| **Context** | No ratified entity; possibly subsumed by Trace + scoped Memory + Runtime | [O] Mapping §9 | Architect Reserved |
| **State** | AIOS models state via PR-2 (state/condition) as a *principle*, not an entity | [O] Mapping §9; PR-2 | Architect Reserved |
| **Resource** | Appears in one engine repo only; no AIOS entity | [O] Mapping §9; Catalog | Architect Reserved |
| **Artifact** | Governance-artifact *types* exist (Meta Model), but no Domain-Model **Artifact** entity | [O] Mapping §9 | Architect Reserved |
| **Task** | No ratified Task entity; nearest is a Workflow step | [O] Mapping; Catalog (CrewAI cognate) | Architect Reserved |
| **Goal** | No ratified entity (external agent-goal cognate) | [O] validation docs (CrewAI) | Architect Reserved |
| **Event** | An execution mechanism (Catalog P-U6), not an AIOS entity; effects are Trace-producing actions | [O] Catalog P-U6; Relationship §5 | Architect Reserved |
| **Checkpoint** | **Not an AIOS term** — a false cognate (graph-state / model-weights). AIOS has no Checkpoint | [O] Catalog §7 (LangGraph/LlamaFactory) | Architect Reserved (do-not-adopt) |
| **Permission** | AIOS expresses access via **Authority** (Constitution §3), not a "Permission" entity | [O] Catalog §7 (Supabase RBAC cognate) | Architect Reserved |
| **Policy** | AIOS's policy layer is the **Constitution/Principles**, not a "Policy" entity (Supabase RLS is a different-plane cognate) | [O] Catalog §7; Constitution | Architect Reserved |
| **Identity** | Used in the Mapping as the *Knowledge correlation key* (design-only); external "Identity" = tenant/auth (false cognate) | [O] Mapping §5/§9 | Architect Reserved |

[A] Reserving these is the point: freezing the canonical language means **explicitly not** granting undefined terms first-class status until the Architect ratifies them.

## 4. Forbidden Synonyms

[E] Each pairing is a *distinction the corpus proved must hold*; treating either side as a synonym of the other is a governance error.

- **Memory ≠ Knowledge** [E] — derived/non-authoritative vs governed/authoritative (inv 8). Conflation = auto-promotion (Letta's inv-8 inversion).
- **Trace ≠ Log** [E] — immutable per-action accountability vs mutable monitoring (Catalog P-U2; B-9≠B-12).
- **Trace ≠ Callback / Event / Checkpoint** [E] — accountability vs observability/state-snapshot (LangChain callback, LangGraph checkpoint).
- **Knowledge ≠ Vector Store / Index** [E] — governed knowledge vs retrieval structure (Haystack/LlamaIndex).
- **Capability ≠ Skill** [E] — a Department-owned "what" vs a reusable "how".
- **Skill ≠ Tool** [E] — an ability vs the external-dependency boundary (inv 12).
- **Agent ≠ Capability** [E] — an actor (Instance) vs an owned ability.
- **Role ≠ Authority** [E] — persona/RBAC-principal (CrewAI/Supabase) vs ratified decision authority (Constitution §3).
- **Checkpoint ≠ Trace** [E] — rewritable state/weight snapshot vs immutable accountability.
- **Workflow ≠ Runtime** [E] — governed composition vs execution binding/facility.
- **Approval ≠ Promotion** [A] — execution-time human gate (R-5) vs governed Memory→Knowledge promotion (inv 8).
- **Audit / Provenance ≠ Trace** [A] — activity log / reproducibility lineage (Supabase/LlamaFactory) vs governed accountability.
- **Adapter, Merge** [E] — corpus-overloaded (LoRA weights / format / weight-arithmetic); **not AIOS terms**.

## 5. False Cognate Dictionary

[E] Consolidated from Catalog §7 and the ten validation documents.

| Term | Repository (external meaning) | AIOS meaning | Risk | Mitigation |
|---|---|---|---|---|
| **Trace** | DSPy demos; LangChain/Haystack/LlamaIndex observability spans | immutable per-action accountability (inv 4/5) | **High** | read the persistence *contract*; classify Not Applicable |
| **Event / Event-store** | OpenHands/CrewAI operational history | governed action record | High | verify mutability/optionality/purpose |
| **Checkpoint** | LangGraph graph-state; LlamaFactory model-weights | (neither) | **High (polysemy)** | re-derive per repo (MF-12); AIOS adopts no Checkpoint |
| **Memory** | Letta self-editing store; LlamaIndex chat buffer; Haystack/LangGraph RAM | derived, non-authoritative, promoted only via review (inv 8) | High | distinguish auto-memory from governed Memory |
| **Knowledge** | Haystack/LlamaIndex RAG index; Letta no-boundary store | governed, versioned, human-promoted | High | check for a promotion boundary (usually absent) |
| **Adapter** | LangChain/Haystack I/O format; LlamaFactory LoRA weights | (no AIOS entity) | High | re-derive per repo |
| **Role** | CrewAI persona; Supabase RBAC principal | Department/Definition-scoped authority | High | persona = false; RBAC = different plane |
| **Policy / Authorization / Audit** | Supabase RLS / activity log (data-access plane) | governance over decisions/knowledge | High | plane distinction (data-access vs decision) |
| **Approval / Human Review** | LangChain/OpenHands/CrewAI/LangGraph execution gate | governed knowledge-promotion decision (inv 8) | Medium | layer distinction (execution vs promotion) |
| **Provenance** | OpenHands/LlamaFactory reproducibility lineage | governance provenance | Medium | artifact-lineage vs accountability |
| **Skills / Capability** | CrewAI/Haystack capability descriptor | governed Capability (Department-owned) | Medium | descriptor vs governed entity |
| **Identity / Organization** | Letta/Supabase tenant/auth principal | Knowledge correlation key / hierarchy root | High | entity-name collision; re-derive |
| **Pipeline / Workflow** | Haystack DAG; LangGraph/CrewAI engine | governed, Traced action composition (inv 4/13) | Medium | ungoverned graph vs governed workflow |
| **Merge** | LlamaFactory weight arithmetic | (n/a) | Medium | weight-fold vs governance |

[A] **Meta:** "Governance" is itself a cognate — external governance-family words (policy, authorization, audit, role) are *real but different-plane* (Supabase) or *absent* (others), never AIOS decision/knowledge governance.

## 6. Vocabulary Dependency Graph

[A] Conceptual dependency only (from Relationship Model §9):

```
Organization → Department → Capability
                                 ↓ exposes
                      Skill → Workflow → Runtime → Agent Instance
                                                        ↓ produces
                                                      Trace  ── immutable (inv 5)
                                                        ↓ reads
                                                      Memory
                                                        ↓ promotes (governed review, inv 8)
                                                      Knowledge
```

[E] Left/top = Organization + Execution vocabulary; the **Trace → Memory → Knowledge** tail = the governance/improvement vocabulary that no external repo possesses (Catalog P-A2/P-A3). [A] No implementation dependency is implied.

## 7. Vocabulary Layering

[A] Canonical terms grouped by layer (a term may anchor one layer and relate to others):

- **Organization layer** — Organization, Department, Capability, Ownership, Lifecycle.
- **Execution layer** — Agent Definition, Agent Instance, Runtime, Workflow, Skill, Tool, Execution. *(Reserved: Task, Event, State, Context.)*
- **Knowledge layer** — Knowledge, Memory, Trace, Identity(reserved), Observation.
- **Infrastructure layer** — Runtime (as facility), Tool boundary, Storage. *(Reserved: Resource, Checkpoint(do-not-adopt).)*
- **Improvement layer** — Promotion, Review, the Memory→Knowledge loop (the governed learning path).
- **Governance layer** — Governance, Authority, Review, Promotion, Decision, Constraint, Responsibility. *(Reserved: Policy, Permission.)*

[E] The layering matches the Relationship Model's execution-half vs governance-half split and the Catalog's universal-vs-AIOS-unique split. [A] It introduces no new structure.

## 8. Reserved Vocabulary

[O] Terms intentionally **not** defined as first-class canonical language (see §3.3), with reason:

- **Context, State** — candidate concepts; may be covered by Trace + scoped Memory + Runtime + PR-2. Reserved until the Architect decides whether a first-class entity is needed.
- **Resource, Artifact** — insufficient ratified basis (Resource: single-repo evidence; Artifact: governance-artifact *types* exist but no Domain-Model entity).
- **Task, Goal** — external agent vocabulary; nearest AIOS notion is a Workflow step / a Capability's intent; no ratified entity.
- **Event** — an execution mechanism, not an entity; its effects are Trace-producing actions.
- **Checkpoint** — a false cognate; **AIOS deliberately adopts no Checkpoint term**.
- **Permission, Policy** — subsumed by Authority (Constitution §3) and the Constitution/Principles as the policy layer; no separate entity.
- **Identity** — held as the Knowledge correlation-key concept (Mapping, design-only); the general/tenant/auth sense is a false cognate and is not adopted.

[A] Reserving is a *positive* act of vocabulary freezing: these terms may be *used descriptively* but are **not** first-class canonical entities until ratified.

## 9. Consistency Review

[E] Checked against each source; no term contradicts any.

- [E] **Constitution:** Authority/Governance/Decision/Review terms are used exactly as the Constitution frames them (§3, §6.2, §14.2); nothing added or automated. Consistent.
- [E] **Domain Model:** the twelve entities are defined verbatim to their ratified meaning; inv 4/5/8/10/12/13 and §5/§6/§6.1/§8 anchor the definitions; no entity renamed or re-scoped. Consistent.
- [E] **Relationship Model:** the dependency graph (§6) and layering (§7) reproduce its lifecycle (§9) and matrix (§5) without change. Consistent.
- [E] **Pattern Catalog:** false cognates (§5) and the observability≠accountability boundary are carried unchanged; no pattern added/promoted. Consistent.
- [E] **Pattern → Entity Mapping:** the Reserved terms (§3.3/§8) match its Gap Analysis (§9) exactly; no gap silently closed. Consistent.
- [E] **Principles Register / DR Method:** PR-1…PR-5 and DR-0…DR-6 cited as basis, unaltered. Consistent.
- [E] **Validation Log:** used read-only; **not modified**. Consistent.

[E] **No inconsistency found.**

## 10. Readiness Assessment

- [E] AIOS now has a **single canonical vocabulary**: twelve ratified entities defined verbatim, governance/process concepts anchored to the Constitution/Principles, an explicit forbidden-synonym set, a consolidated false-cognate dictionary, and an explicit Reserved list that refuses first-class status to undefined terms.
- [A] This constitutes a **stable canonical language suitable for entering Phase 1B (DNA Consolidation)** — every prior synthesis (Catalog, Mapping, Relationship Model) can now be read under one terminology without cognate drift.
- [O] **Not authorized here:** entry into Phase 1B is **reserved to the Architect**. Open items that the Architect may wish to close first: the Reserved terms (§8), the Inferred relationships (Relationship Model §12), and the standing reviewer-independence limit (Plan §9).
- [E] **Not assessed:** implementation readiness (out of scope).

---

## Closing

[E] This document freezes AIOS terminology from the ratified canon and the three prior synthesis artifacts, without inventing, renaming, or ratifying anything. [A] Its core discipline: the twelve entities and the governance concepts are defined verbatim; the corpus's dangerous cognates are quarantined into a forbidden-synonym set and a false-cognate dictionary; and every undefined term (State, Context, Resource, Artifact, Task, Goal, Event, Checkpoint, Permission, Policy, Identity) is **explicitly Reserved**, not silently adopted. [O] Ratification of Reserved terms and progression to Phase 1B are reserved entirely to the Architect.

**No implementation, code, API, schema, or algorithm was produced. No entity, relationship, or architecture was invented; no canonical entity was renamed. The Constitution, Domain Model, Principles Register, Pattern Catalog, Pattern→Entity Mapping, Relationship Model, prior validation documents, and Validation Log were not modified. This is a new additive synthesis document only.**
