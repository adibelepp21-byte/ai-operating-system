# AIOS DNA Library v1.0

**Phase:** AIOS 1B — DNA Consolidation.
**Type:** Implementation-neutral **architectural DNA** extracted from the validated corpus and mapped to canonical AIOS building blocks. **Not implementation.** Additive; invents no entity/relationship; modifies no prior document.
**What "DNA" means here** [A]: reusable *architectural ideas* — design patterns, decisions, structural/execution/state/memory/knowledge/workflow/capability/optimization/infrastructure models, trade-offs, constraints, failure modes. **DNA is not code, API, class structure, or naming** — none of those is copied.
**Evidence scope (ONLY these):** the ten Repository Validation documents · Validation Log · Pattern Catalog · Pattern → Entity Mapping · Canonical Relationship Model · Canonical Vocabulary Freeze · Architecture Specification · Architecture Review. **No internet, no new repositories, no implementation.**
**Confidence discipline:** **[E]** stated in a source · **[A]** reasoned abstraction · **[O]** open / reserved to the Architect. **No untagged conclusions.**
**Standing governance frame** [E]: across all ten repositories, AIOS-sense governance is "not observed" (Log R-4). [A] Therefore **every external DNA entry below is reusable by AIOS only when placed *under governance*** — the corpus supplies the execution half of the chain; AIOS supplies the governance half (Architecture Specification; Relationship Model §9).

---

## Part I — Per-Repository DNA

### 1. DSPy
- **Repository** [E]: DSPy — LLM program optimization (compile/teleprompt).
- **Purpose** [E]: build and *automatically optimize* LLM programs.
- **Core DNA** [E]: separation of a *declared program* from its *automatic optimizer*; declarative intent (signature) with realization deferred to an adapter boundary; self-composing modules.
- **Architectural Pattern** [A]: **definition/optimization separation** + declarative-over-imperative.
- **Strengths** [E]: clean separation of "what" from "how it improves"; composability.
- **Weaknesses** [E, for AIOS]: optimization is *automatic and ungoverned*.
- **Trade-offs** [A]: automation vs control.
- **AIOS Relevance** [A]: the definition/tuning split rhymes with AIOS's definition/execution split — but AIOS governs the improvement edge (inv 8).
- **Mapped AIOS Layer** [A]: Optimization (L10).
- **Mapped AIOS Entity** [A]: Agent Definition (declarative form); none for the optimizer.
- **Mapped Building Block** [A]: B-2 Composition; B-6 Configuration.
- **Dependencies** [E]: external LM clients (isolated boundary).
- **Reusable Concepts** [A]: declare behavior separately from its improvement; defer realization to a boundary.
- **NOT adopted** [E]: **automatic self-improvement** — it would violate inv 8 (governed promotion) and PR-3 (Detect, Don't Decide).
- **Future evolution potential** [O]: a *governed* optimization loop where improvement proposals are detected but human-decided.
- **Evidence** [E]: `AIOS_DR_VALIDATION_DSPY_v1.0`.

### 2. LangChain
- **Purpose** [E]: agent/LLM application framework.
- **Core DNA** [E]: a **uniform composition primitive** (compose units into larger units); tools treated as composable units; an adapter boundary isolating LM I/O format; per-vendor package isolation.
- **Architectural Pattern** [A]: uniform composition + vendor isolation.
- **Strengths** [E]: one composition model for everything; clean external-dependency isolation.
- **Weaknesses** [E]: observability ("tracer") is a false cognate for accountability; composition is ungoverned.
- **Trade-offs** [A]: flexibility vs governance.
- **AIOS Relevance** [A]: composition maps to Workflow; vendor isolation corroborates inv 12.
- **Mapped Layer** [A]: Runtime/Workflow (L2/L6).
- **Mapped Entity** [A]: Workflow; Tool.
- **Mapped Building Block** [A]: B-2 Composition; B-1 Dependency Boundary.
- **Dependencies** [E]: partner packages (isolated).
- **Reusable Concepts** [A]: a single composition abstraction; a dedicated LM-format boundary.
- **NOT adopted** [E]: tracer-as-Trace; ungoverned composition.
- **Future evolution** [O]: a governed composition surface whose every step is Traced (inv 4).
- **Evidence** [E]: `AIOS_DR_VALIDATION_LANGCHAIN_v1.0`.

### 3. OpenHands
- **Purpose** [E]: autonomous coding-agent platform (control-center; runtime in external SDK).
- **Core DNA** [E]: an **execution lifecycle with explicit runtime states** (incl. a stuck state); a **risk-based confirmation policy** + pluggable analyzer gating agent actions; an operational event store; launch provenance; a thin control-center over an external runtime.
- **Architectural Pattern** [A]: runtime lifecycle + human-confirmation gate.
- **Strengths** [E]: explicit lifecycle states; runtime autonomy-gating with human confirmation.
- **Weaknesses** [E]: the analyzer *lets an LLM decide* confirmation (conflicts with PR-3); event store is observability, not accountability.
- **Trade-offs** [A]: pre-action machine-judged gating vs post-hoc governed record.
- **AIOS Relevance** [A]: lifecycle states inform Runtime/Agent layers; the human gate is an execution-time gate (not promotion governance).
- **Mapped Layer** [A]: Runtime/Agent (L2/L3).
- **Mapped Entity** [A]: Agent Instance; Runtime.
- **Mapped Building Block** [A]: B-3 Runtime; B-10 Human-Interaction Gate.
- **Dependencies** [E]: external agent SDK (boundary).
- **Reusable Concepts** [A]: explicit runtime lifecycle states (incl. stuck-detection); a human gate on autonomy.
- **NOT adopted** [E]: **LLM-decided confirmation** (PR-3, §6.2 invariant 2); event-store-as-Trace.
- **Future evolution** [O]: a human gate that is *detect-then-govern*, with the machine proposing risk, never deciding it.
- **Evidence** [E]: `AIOS_DR_VALIDATION_OPENHANDS_v1.0`.

### 4. Letta (MemGPT)
- **Purpose** [E]: long-term-memory agent platform.
- **Core DNA** [E]: **tiered memory** (in-context / archival / recall) with explicit **context-window management**; memory carrying provenance + visibility scope; versioned memory-edit history.
- **Architectural Pattern** [A]: tiered memory + context-window paging.
- **Strengths** [E]: mature context-window management; tiered memory.
- **Weaknesses** [E]: memory is **self-edited autonomously** — a direct **inversion of inv 8** (Memory→Knowledge must be governed); no Memory/Knowledge boundary.
- **Trade-offs** [A]: adaptivity vs governed accountability.
- **AIOS Relevance** [A]: the *tiering and context-window* idea is reusable **only** with AIOS's governed Memory→Knowledge boundary intact.
- **Mapped Layer** [A]: Memory/Knowledge (L7/L8).
- **Mapped Entity** [A]: Memory (derived); Knowledge (as the governed destination Letta lacks).
- **Mapped Building Block** [A]: B-8 Storage; B-13 Knowledge Promotion Gate (as the *missing* piece Letta inverts).
- **Dependencies** [E]: vector + relational storage (isolated).
- **Reusable Concepts** [A]: tiered/working-vs-long-term memory; context-window budgeting.
- **NOT adopted** [E]: **autonomous self-editing memory** (inverts inv 8); the absence of a Memory/Knowledge boundary.
- **Future evolution** [O]: tiered memory whose promotion to Knowledge is human-governed.
- **Evidence** [E]: `AIOS_DR_VALIDATION_LETTA_v1.0`.

### 5. Haystack
- **Purpose** [E]: RAG / retrieval-and-pipeline framework.
- **Core DNA** [E]: a **type-checked component DAG** (connections validated at wiring time); a content-addressed document unit; a pluggable store protocol with a duplicate policy; dense/sparse/hybrid retrieval; **dataflow-role separation** (retriever vs generator vs store).
- **Architectural Pattern** [A]: typed dataflow-DAG composition + retrieval.
- **Strengths** [E]: a mature typed composition engine (a scope-qualified strength).
- **Weaknesses** [E]: documents are mutable/overwritable (would violate inv 5 if mapped to Trace/Knowledge); "trace" is observability.
- **Trade-offs** [A]: retrieval flexibility vs immutability/governance.
- **AIOS Relevance** [A]: typed composition informs Workflow; its retrieval is *not* AIOS Knowledge.
- **Mapped Layer** [A]: Workflow/Knowledge (L6/L8).
- **Mapped Entity** [A]: Workflow.
- **Mapped Building Block** [A]: B-2 Composition.
- **Dependencies** [E]: integration packages (mostly isolated; one vendor in core).
- **Reusable Concepts** [A]: **edge-type-checking at composition time**; dataflow-role separation.
- **NOT adopted** [E]: **mutable-overwrite storage** as a model for immutable Trace/Knowledge (inv 5); retrieval-as-Knowledge.
- **Future evolution** [O]: compile-time validation of governed Workflow connections.
- **Evidence** [E]: `AIOS_DR_VALIDATION_HAYSTACK_v1.0`.

### 6. CrewAI
- **Purpose** [E]: multi-agent orchestration (role-playing agents, delegation).
- **Core DNA** [E]: **multi-agent coordination** (a team + tasks + a sequential/hierarchical process); an event-driven flow; a per-task **human-input + guardrail** gate; component identity fingerprints and access-config fragments.
- **Architectural Pattern** [A]: multi-agent coordination + per-task human gate.
- **Strengths** [E]: rich multi-agent coordination expressiveness (scope-qualified strength).
- **Weaknesses** [E]: **free agent-to-agent delegation runs against inv 13** (collaboration must go via Workflow/Knowledge/scoped Memory).
- **Trade-offs** [A]: collaborative autonomy vs governed collaboration boundaries.
- **AIOS Relevance** [A]: multi-agent coordination is reusable **only** channeled through Workflow (inv 13).
- **Mapped Layer** [A]: Agent/Workflow (L3/L6).
- **Mapped Entity** [A]: Agent Instance; Workflow.
- **Mapped Building Block** [A]: B-2 Composition; B-10 Human-Interaction Gate.
- **Dependencies** [E]: vendor extras + tool packages (isolated).
- **Reusable Concepts** [A]: coordinating multiple agents on decomposed tasks; per-step output validation (guardrail).
- **NOT adopted** [E]: **free agent-to-agent delegation** (inv-13 conflict); `Role`-as-authority (it is a persona).
- **Future evolution** [O]: multi-agent coordination expressed as governed Workflows with Traced hand-offs.
- **Evidence** [E]: `AIOS_DR_VALIDATION_CREWAI_v1.0`.

### 7. LlamaIndex
- **Purpose** [E]: RAG / indexing data framework.
- **Core DNA** [E]: a **structured content-representation graph** (source→chunk units linked by prev/next/parent/child, content-hashed); an index abstraction over units; a composed storage context; a retriever→synthesizer→query pipeline; human-in-the-loop via workflow events.
- **Architectural Pattern** [A]: structured-representation graph + retrieval pipeline.
- **Strengths** [E]: a rich structured representation of content (scope-qualified strength).
- **Weaknesses** [E]: governance-orthogonal (all governance "not observed"); "Knowledge"=graph index, "Memory"=chat buffer (cognates).
- **Trade-offs** [A]: representational richness vs governance-neutrality.
- **AIOS Relevance** [A]: the structured-relationship-graph idea could inform *governed Knowledge* representation.
- **Mapped Layer** [A]: Knowledge/Infrastructure (L8/L9).
- **Mapped Entity** [A]: Knowledge (as a governed destination); storage facilities.
- **Mapped Building Block** [A]: B-8 Storage; B-2 Composition.
- **Dependencies** [E]: large isolated integration set (one vendor in core).
- **Reusable Concepts** [A]: content-addressed units; explicit inter-unit relationship graph; composed multi-store context.
- **NOT adopted** [E]: index-as-Knowledge; chat-buffer-as-Memory.
- **Future evolution** [O]: a relationship-graph representation *inside* governed, versioned Knowledge.
- **Evidence** [E]: `AIOS_DR_VALIDATION_LLAMAINDEX_v1.0`.

### 8. LangGraph
- **Purpose** [E]: low-level stateful graph-orchestration engine.
- **Core DNA** [E]: a **bulk-synchronous superstep execution model** over a node/edge graph; **typed state channels with reducers**; **durable checkpointing** (resumption / time-travel); a long-term store; an interrupt-based human gate.
- **Architectural Pattern** [A]: superstep graph execution + durable state.
- **Strengths** [E]: a rigorous, resumable execution engine (scope-qualified strength); explicit typed state.
- **Weaknesses** [E]: its "checkpoint" is a **rewritable/forkable** state history — the structural *opposite* of an immutable Trace (inv 5).
- **Trade-offs** [A]: resumability/time-travel vs immutability.
- **AIOS Relevance** [A]: the superstep engine and typed-state model inform Runtime/Workflow — but AIOS's Trace must remain immutable and *separate* from resumable state.
- **Mapped Layer** [A]: Runtime/Workflow (L2/L6).
- **Mapped Entity** [A]: Runtime; Workflow.
- **Mapped Building Block** [A]: B-3 Runtime; B-4 State Model; B-5 Event.
- **Dependencies** [E]: model-agnostic core; separate checkpoint backends.
- **Reusable Concepts** [A]: superstep execution; typed state channels with explicit reducers; resumable execution.
- **NOT adopted** [E]: **checkpoint-as-Trace** (rewritable history); ungoverned graph.
- **Future evolution** [O]: a superstep runtime whose *resumable state* is distinct from the *immutable Trace* it emits per action.
- **Evidence** [E]: `AIOS_DR_VALIDATION_LANGGRAPH_v1.0`.

### 9. Supabase
- **Purpose** [E]: Postgres-centric backend-as-a-service (auth/RLS/realtime/storage/edge).
- **Core DNA** [E]: **fine-grained runtime data-access authorization** (identity → role → row-level policy); an activity audit log; ordered forward migrations; multi-tenant isolation; independently-versioned services behind a gateway.
- **Architectural Pattern** [A]: data-plane authorization + service isolation.
- **Strengths** [E]: the corpus's first *genuine authorization* mechanism (scope-qualified strength).
- **Weaknesses** [E]: it operates on the **data-access plane**, a *different plane* from AIOS decision/knowledge governance; its "audit" is a mutable activity log.
- **Trade-offs** [A]: data-security granularity vs decision-plane governance.
- **AIOS Relevance** [A]: the *idea* of fine-grained, declarative access authorization could inform AIOS's Authority — but at the correct (decision/knowledge) plane, not data rows.
- **Mapped Layer** [A]: Infrastructure/Governance (L9/L1).
- **Mapped Entity** [A]: Tool (external boundary); Authority (analogous, different plane).
- **Mapped Building Block** [A]: B-1 Dependency Boundary; B-11 Governance / B-14 Authority Hierarchy (as a *different-plane analog*).
- **Dependencies** [E]: services as isolated pinned images.
- **Reusable Concepts** [A]: declarative, fine-grained authorization; ordered forward migrations; service isolation.
- **NOT adopted** [E]: RLS-as-AIOS-authority (different plane); activity-log-as-Trace.
- **Future evolution** [O]: declarative authority policies at AIOS's decision/knowledge plane.
- **Evidence** [E]: `AIOS_DR_VALIDATION_SUPABASE_v1.0`.

### 10. LlamaFactory
- **Purpose** [E]: LLM fine-tuning/training framework.
- **Core DNA** [E]: a **config-driven training pipeline** (declarative args → stage dispatch → lifecycle: prepare → train → adapt → merge → quantize → export → evaluate); **per-feature optional-dependency isolation**; artifact provenance (adapter→base lineage, revision pinning); experiment tracking.
- **Architectural Pattern** [A]: config-driven lifecycle pipeline + optional-dependency isolation.
- **Strengths** [E]: mature config-driven orchestration of a complex lifecycle (scope-qualified strength); strong dependency isolation; artifact reproducibility lineage.
- **Weaknesses** [E]: governance-orthogonal; `Adapter`/`Checkpoint`/`Merge` are corpus-overloaded terms.
- **Trade-offs** [A]: training capability vs governance-neutrality.
- **AIOS Relevance** [A]: config-driven lifecycle orchestration + optional-dependency isolation inform Optimization/Infrastructure; **model-optimization itself is a reserved, external concern**.
- **Mapped Layer** [A]: Optimization/Infrastructure (L10/L9).
- **Mapped Entity** [A]: none (training is external); Tool boundary.
- **Mapped Building Block** [A]: B-6 Configuration; B-1 Dependency Boundary.
- **Dependencies** [E]: per-feature optional extras (strongly isolated).
- **Reusable Concepts** [A]: declarative config drives a staged lifecycle; per-capability optional dependencies; artifact provenance/reproducibility lineage.
- **NOT adopted** [E]: model-optimization as an AIOS entity (**[O] reserved**); the `Checkpoint` term (do-not-adopt).
- **Future evolution** [O]: a governed, reproducible improvement lifecycle whose artifacts carry provenance and whose promotion is human-governed.
- **Evidence** [E]: `AIOS_DR_VALIDATION_LLAMAFACTORY_v1.0`.

---

## Part II — Cross-Repository DNA Matrix

[E] Recurrences from the Validation Log (R-1…R-8) and per-repo DNA. **Recurrence is evidence, not a mandate.**

| DNA Pattern | Observed In | Mapped Layer | Mapped Entity | Mapped Building Block | Confidence |
|---|---|---|---|---|---|
| Dependency isolation | all 10 (R-1) | Infrastructure (L9) | Tool | B-1 | **Strong** |
| Observability ≠ accountability (Trace is unique) | all (R-3) | Governance (L1) | Trace (distinct) | B-9 vs B-12 | **Strong** |
| No unified governance (AIOS-distinctive) | all (R-4) | Governance (L1) | Governance/Trace/Knowledge/Authority | B-11/B-12/B-13/B-14 | **Strong** |
| Composition primitive | DSPy, LangChain, Haystack, LangGraph (+CrewAI/LlamaIndex partial) (R-2) | Workflow (L6) | Workflow | B-2 | **Moderate** |
| Execution engine (scope-Stronger) | LangChain, Haystack, CrewAI, LlamaIndex, LangGraph (R-6) | Runtime (L2) | Runtime | B-3 | **Moderate** |
| Human gate on autonomy (execution-time) | LangChain, OpenHands, Letta, CrewAI, LlamaIndex, LangGraph (R-5) | Agent/Governance (L3/L1) | Agent Instance | B-10 | **Moderate** |
| Typed state model | LangGraph (+OpenHands/CrewAI states) | Runtime (L2) | Runtime | B-4 | **Moderate** |
| Storage abstraction | Letta, Haystack, LlamaIndex, LangGraph, CrewAI, Supabase | Infrastructure (L9) | (substrate) | B-8 | **Moderate** |
| Config-driven orchestration | LlamaFactory, CrewAI, Haystack, LangGraph, DSPy | Optimization/Runtime | Agent Definition | B-6 | **Moderate** |
| Structured content representation | LlamaIndex (+Haystack) | Knowledge (L8) | Knowledge | B-8/B-2 | **Moderate** |
| Fine-grained authorization (different plane) | Supabase (R-8) | Governance/Infra (L1/L9) | Authority | B-14 | **Weak** |
| Governance inversion (anti-pattern) | Letta (inv 8), CrewAI (inv 13) (R-7) | Governance (L1) | Memory/Workflow | B-13/(inv 13) | **Weak (anti-pattern)** |

[A] **The matrix's shape:** the *execution/composition/state/storage/config* DNA is broadly reusable (Moderate–Strong); the *governance* DNA is **AIOS-distinctive** (external absence is the Strong signal); the *inversion* rows are **anti-patterns** — DNA of what AIOS must *not* do.

---

## Part III — Canonical AIOS DNA (implementation-neutral)

[A] Derived DNA, each: Definition · Purpose · Originating evidence · Architectural responsibility · Future implementation responsibility ([O], reserved). **No implementation.**

### Governance DNA
- **Definition** [A]: authority, review, and promotion over decisions and knowledge, above execution, never overridable by automation.
- **Purpose** [E]: enforce inv 8 (governed promotion), Constitution §3 (authority), §6.2 (human authority).
- **Originating evidence** [E]: **absent in all 10 repos** (R-4) — the defining AIOS gap the corpus proves.
- **Architectural responsibility** [E]: gate the Memory→Knowledge edge; own decision/review authority.
- **Future implementation responsibility** [O]: a governance layer that detects-but-does-not-decide (PR-3), fails closed (PR-4).

### Immutable-Trace DNA
- **Definition** [A]: an unconditional, append-only, exactly-one-per-action accountability record — categorically distinct from any observability/log/checkpoint.
- **Purpose** [E]: inv 4/5, §14.2.
- **Originating evidence** [E]: every external "trace/event/log/checkpoint/audit" was *observability*, never this (R-3, the corpus's strongest false cognate).
- **Architectural responsibility** [E]: be the sole permanent source of truth; feed all derivation.
- **Future implementation responsibility** [O]: a write-once accountability substrate, separated from resumable state and monitoring.

### Knowledge DNA
- **Definition** [A]: governed, versioned, authoritative knowledge entered only through review.
- **Purpose** [E]: inv 8, §8.
- **Originating evidence** [E]: external "knowledge" was RAG index / no-boundary store / graph structure (Haystack, LlamaIndex, Letta) — never governed; Letta *inverts* the boundary.
- **Architectural responsibility** [E]: hold authoritative knowledge; accept entries only via promotion.
- **Future implementation responsibility** [O]: a versioned, admission-gated knowledge store (admission model **[O]** open).

### Memory DNA
- **Definition** [A]: derived, non-authoritative, tier-able memory produced from Trace, upstream of governed promotion.
- **Purpose** [E]: §6.1, inv 8.
- **Originating evidence** [E]: tiered/context-window memory (Letta) — reusable *only* with the governed boundary Letta lacks.
- **Architectural responsibility** [E]: derive from Trace; never self-promote; never rewrite Trace.
- **Future implementation responsibility** [O]: tiered derived memory with a governed promotion boundary.

### Execution DNA
- **Definition** [A]: a runtime that binds definitions to instances and drives governed composition, emitting one Trace per action.
- **Purpose** [E]: DM §6, inv 4/13.
- **Originating evidence** [E]: superstep engine + lifecycle states (LangGraph, OpenHands); uniform composition (LangChain).
- **Architectural responsibility** [E]: execute; isolate; produce Trace; coordinate only via Workflow.
- **Future implementation responsibility** [O]: an execution engine whose resumable state is distinct from immutable Trace.

### Workflow DNA
- **Definition** [A]: the governed composition and coordination channel for multi-agent action.
- **Purpose** [E]: inv 13.
- **Originating evidence** [E]: composition primitives + multi-agent coordination (LangChain, Haystack, CrewAI, LangGraph) — CrewAI's *free* delegation is the anti-pattern.
- **Architectural responsibility** [E]: be the *only* sanctioned collaboration channel; each step Traced.
- **Future implementation responsibility** [O]: governed, type-validated workflow composition with Traced hand-offs.

### Capability DNA
- **Definition** [A]: a Department-owned unit of ability, cross-Department dependencies governed.
- **Purpose** [E]: DM §5, inv 10.
- **Originating evidence** [E]: external "capability/skill" was a descriptor cognate; ownership/governance absent.
- **Architectural responsibility** [E]: own ability; require governance for cross-Department dependency.
- **Future implementation responsibility** [O]: a governed capability model with ownership boundaries.

### Skill DNA
- **Definition** [A]: a reusable, composable, discoverable unit of ability — a facility, not a traced actor.
- **Purpose** [E]: DM (Skill); inv 4/12; registry pattern (P-U8).
- **Originating evidence** [E]: registries/skill descriptors (CrewAI, Haystack).
- **Architectural responsibility** [E]: be composed into Workflows; produce no independent Trace; hold no external dependency.
- **Future implementation responsibility** [O]: a discoverable, reusable skill unit under the Tool/Trace boundaries.

### Agent DNA
- **Definition** [A]: a governed definition and its instance — the only actor, every action accountable.
- **Purpose** [E]: DM §6, inv 4/13.
- **Originating evidence** [E]: external "agent" was persona/loop (CrewAI, OpenHands, LangGraph) — ungoverned.
- **Architectural responsibility** [E]: act only via Workflow/Tool/scoped Memory; produce exactly one Trace per action.
- **Future implementation responsibility** [O]: a governed agent definition/instance model with mandatory Trace.

### Optimization DNA
- **Definition** [A]: a *governed* improvement loop — detect/propose improvements from Trace/Memory; humans decide promotion.
- **Purpose** [E]: inv 8, PR-3.
- **Originating evidence** [E]: automatic optimization (DSPy) and config-driven training (LlamaFactory) — reusable *only* as detect-then-govern; their automation is the anti-pattern.
- **Architectural responsibility** [E]: inform, never decide governance; never auto-promote; never mutate Trace.
- **Future implementation responsibility** [O]: a governed learning loop with provenance-carrying, human-promoted improvements (model-optimization itself **[O]** reserved/external).

### Infrastructure DNA
- **Definition** [A]: facilities beneath the entities (storage, execution substrate, the single external boundary), audited through the actions that invoke them — never independent actors.
- **Purpose** [E]: inv 12, §8, OQ-2 interpretation.
- **Originating evidence** [E]: dependency isolation (all 10, R-1); service/optional-dependency isolation (Supabase, LlamaFactory).
- **Architectural responsibility** [E]: confine external dependency to the Tool; provide storage under substrate; own no governance.
- **Future implementation responsibility** [O]: isolated facilities with the Tool as the sole external boundary (Identity/Auth/Networking/Deployment **[O]** reserved).

---

## Part IV — Implementation Boundary

[E] This document still contains **NO implementation.** Explicitly: **no APIs, no schemas, no runtime code, no classes, no file structure, no programming-language decisions.** [A] The DNA entries are *architectural responsibilities and reusable ideas*, expressed neutrally; **future implementation responsibilities are tagged [O]** and reserved to a later phase and the Architect.

---

## Part V — Consistency & Integrity Note

- [E] Every per-repository entry cites its validation document; every cross-repo row cites a Validation-Log recurrence; every canonical-DNA entry cites a ratified invariant/principle or the Architecture Specification/Relationship Model.
- [E] No external implementation, API, class structure, or naming was copied — only architectural ideas, with each mapped to an AIOS layer/entity/building block and its governance caveat.
- [E] No prior document was modified; only this additive DNA Library was created.

---

## Closing

[A] The DNA Library distills the corpus into reusable, implementation-neutral architecture: the external ecosystem supplies mature **execution, composition, state, storage, config, and representation** DNA; AIOS supplies the **governance, immutable-Trace, knowledge-promotion, and authority** DNA the corpus lacks — and marks the two governance **inversions** (Letta/inv-8, CrewAI/inv-13) as anti-patterns to avoid. [A] Every reusable external concept is admissible **only under governance**. [O] All future-implementation responsibilities, the reserved concerns, and progression to **Phase 2 (Architecture Freeze)** are reserved to the Architect.

**No implementation, code, API, schema, class design, file structure, or language decision was produced. No external implementation or naming was copied. No entity or relationship was invented. The ten validation documents, Validation Log, Pattern Catalog, Pattern→Entity Mapping, Relationship Model, Vocabulary documents, Architecture Specification, and Architecture Review were not modified. This is a new additive DNA Library document only.**
