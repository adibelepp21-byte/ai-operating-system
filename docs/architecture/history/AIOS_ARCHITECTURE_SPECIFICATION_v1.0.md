# AIOS Architecture Specification v1.0

**Status:** Canonical **architectural specification** — the architectural source-of-truth for AIOS. Descriptive only. Additive; ratifies nothing new; invents no entity/relationship/concept; renames nothing; modifies no prior document.
**Role:** the final bridge — Validated Repository Corpus → Canonical Patterns → Canonical Entities → Canonical Relationships → **Architecture** → Implementation. This document reaches the *Architecture* stage; **Implementation is out of scope** (Phase 1B onward).
**Evidence sources (ONLY these):** Constitution · Canonical Domain Model · Principles Register · Decision Review Method · Validation Log · Pattern Catalog · Pattern → Entity Mapping · Canonical Relationship Model · Canonical Vocabulary. **No external repositories, no internet, no new concepts, no implementation.**
**Confidence discipline:** **[E]** stated in a ratified/prior source · **[A]** reasoned architectural abstraction · **[O]** open / Architect decision / future work. **No untagged conclusions.**
**Note on the Vocabulary source:** two vocabulary documents currently exist pending an Architect naming disposition — the earlier glossary (`AIOS_CANONICAL_VOCABULARY_v1.0.md`) and the Phase 1A.9 freeze (`AIOS_CANONICAL_VOCABULARY_FREEZE_v1.0.md`). This specification uses both as "Canonical Vocabulary"; **[O]** their consolidation/naming is reserved to the Architect and does not affect this specification's content.

---

## 0. How to Read This Specification

[A] AIOS is specified as **ten layers**. A "layer" is an *organizational grouping of responsibility*, not an implementation module and not a strict call-stack. [E] Three of the entities — **Trace, Memory, Knowledge** — are declared **cross-cutting Substrate** by the Domain Model (§8, non-private); they are presented as layers here for responsibility clarity but are **substrate**, reachable across the stack under governance. [A] The layers are an abstraction *over* the twelve ratified entities and their ratified relationships (Relationship Model §5); they add no entity.

---

## Layer 1 — Governance Layer

- **Purpose** [E]: hold authority over decisions, accountability, and the promotion of derived Memory into authoritative Knowledge (Constitution; DM inv 8; Catalog P-A1).
- **Responsibilities** [E]: **Decision authority** (Constitution §3 tiers); **Trace authority** (unconditional, immutable accountability — DM inv 4/5, §14.2); **Promotion authority** (Memory→Knowledge only via governed review — inv 8); **Review authority** (human review decisions — DR Method); **Policy boundaries** (the Constitution/Principles are the policy layer — Vocabulary §3.3, "Policy" Reserved).
- **Owned entities** [A]: none of the twelve entities exclusively; governance is a *layer/process*, not a Domain-Model entity (Mapping §5). It governs **Trace** (immutability), the **Memory→Knowledge** edge (promotion), and **Authority** (Constitution §3).
- **Allowed interactions** [E]: authorizes promotion; records decisions; reads Trace; sets validity/condition via governed review.
- **Forbidden interactions** [E]: **may not mutate Trace** (inv 5); **may not be overridden by automation** (Constitution §6.2 invariant 2); may not promote automatically (inv 8).
- **Dependencies** [A]: depends on Trace (evidence) and Memory (candidates); depended-on by every layer that changes authoritative state.
- **Ratified references** [E]: Constitution §3, §6.2, §14.2; DM inv 4/5/8; DR Method; PR-3 (Detect, Don't Decide), PR-4 (Fail Closed).
- **Evidence tag**: **[E]** (governance is the corpus's AIOS-unique layer — Log R-4, "not observed" in all ten repositories).

## Layer 2 — Runtime Layer

- **Purpose** [E]: bind an Agent Definition to execution and drive Workflow execution (DM §6; Relationship Model §5).
- **Responsibilities** [A]: **execution engine**; **workflow execution**; **scheduling**; **coordination** of Agent Instances *only via Workflow* (inv 13); **isolation** of execution (external capability only via Tool — inv 12).
- **Owned entities** [E]: **Runtime** (a *facility, not an actor* — OQ-2 interpretation, Mapping §5).
- **Allowed interactions** [E]: creates Agent Instances (DM §6); executes Workflows; each Agent-Instance action *produces exactly one Trace* (inv 4).
- **Forbidden interactions** [E]: **must not become an independent traced actor** (OQ-2); **must not own Knowledge** (Relationship §8; Knowledge is cross-cutting substrate, §8); must not enable direct agent-to-agent collaboration outside Workflow (inv 13).
- **Dependencies** [A]: depends on Agent Definitions (Layer 3), Workflows (Layer 6), Tools (Layer 9 boundary); produces Trace (Layer via substrate).
- **Ratified references** [E]: DM §6, inv 4/12/13; Mapping §7 (Runtime responsibility).
- **Evidence tag**: **[E]** entity ratified; **[A]** engine responsibilities abstracted (Catalog P-U4; R-6 shows external engines are mature — evidence corroborates, never dictates).

## Layer 3 — Agent Layer

- **Purpose** [E]: represent the definition and governed execution of agents (DM §6).
- **Responsibilities** [E]: **Agent Definition** (the template); **Agent Instance** (a runtime execution — the *only actor*); **lifecycle** (Definition → Instance, DM §6); **responsibility** that *every* Instance action is attributable to exactly one Trace (inv 4).
- **Owned entities** [E]: **Agent Definition**, **Agent Instance**.
- **Allowed interactions** [E]: an Instance *uses* Tools and Skills, *consumes* Knowledge, *writes* scoped Memory, *produces* Trace; *references* its Definition (Relationship §5).
- **Forbidden interactions** [E]: **may not modify a Trace record after write** (inv 5); **may not collaborate agent-to-agent except via Workflow/Knowledge/scoped Memory** (inv 13); **may not promote Memory to Knowledge itself** (inv 8); may not redefine a Capability (Relationship §8).
- **Dependencies** [A]: depends on Runtime (Layer 2) to be instantiated; on Capabilities/Skills (Layers 4/5) for ability.
- **Ratified references** [E]: DM §6, inv 4/8/13.
- **Evidence tag**: **[E]** entities/invariants ratified; the external "Agent" is a false cognate (Vocabulary §5 — persona/loop vs governed entity).

## Layer 4 — Capability Layer

- **Purpose** [E]: represent what a Department can do (DM §5; inv 10).
- **Responsibilities** [A]: hold **Capabilities**; govern **composition** of Capabilities from Skills/Workflows; enforce **ownership** (Department-owned, §5); enforce **boundaries** (cross-Department Capability dependencies require governance — inv 10).
- **Owned entities** [E]: **Capability** (owned by **Department**, which is owned by **Organization** — DM §5).
- **Allowed interactions** [A]: *exposes* Skills/Workflows (Relationship §5, Inferred); a cross-Department dependency proceeds *only* through governance (inv 10).
- **Forbidden interactions** [E/A]: a **Capability cannot execute itself** (it is a "what," not an actor — Relationship §8); an Agent **cannot redefine a Capability** (Relationship §8); cross-Department dependency **cannot bypass governance** (inv 10).
- **Dependencies** [A]: depends on the Organization/Department ownership hierarchy (§5); realized through Skill (Layer 5) and Workflow (Layer 6).
- **Ratified references** [E]: DM §5, inv 10.
- **Evidence tag**: **[E]** entity ratified; **[A]** Capability↔Skill/Workflow edges are *Inferred* (Relationship §5) — **[O]** their ratification reserved to the Architect.

## Layer 5 — Skill Layer

- **Purpose** [E]: provide reusable, composable units of agent ability (DM; Catalog P-U3/P-U8).
- **Responsibilities** [A]: **Skill lifecycle**; **discovery**/**registration** (Registry pattern — Catalog P-U8, a lookup *facility*, not an actor); **execution** (a Skill is used by an Agent Instance); **reuse** (composition into Workflows).
- **Owned entities** [E]: **Skill**.
- **Allowed interactions** [E/A]: *used by* Agent Instance; *contained in* Workflow (Relationship §5); registered/discovered via a registry facility.
- **Forbidden interactions** [A]: a Skill is not an actor — it **produces no independent Trace** (only the invoking Agent-Instance action does — inv 4, OQ-2); it must not hold an external dependency (that is the Tool's sole role — inv 12).
- **Dependencies** [A]: composed by Capabilities (Layer 4); executed within Agent-Instance actions (Layer 3).
- **Ratified references** [E]: DM (Skill entity); inv 4/12; Catalog P-U3/P-U8.
- **Evidence tag**: **[E]** entity ratified; **[A]** registry/discovery responsibilities abstracted from the corpus (P-U8).

## Layer 6 — Workflow Layer

- **Purpose** [E]: the governed composition and coordination of Agent-Instance actions — the sanctioned channel for multi-agent interaction (DM; inv 13).
- **Responsibilities** [A]: **workflow orchestration**; **composition** (of Skills/actions — P-U3); **execution responsibility** such that composition remains governed and each action is Traced (inv 4/13).
- **Owned entities** [E]: **Workflow**.
- **Allowed interactions** [E]: *coordinates* Agent Instances (inv 13); *contains* Skills (Relationship §5).
- **Forbidden interactions** [E]: **must not permit direct agent-to-agent collaboration outside itself** (or Knowledge / scoped Memory) — inv 13; is **not** the Runtime (Vocabulary §4, `Workflow ≠ Runtime`).
- **Dependencies** [A]: executed by Runtime (Layer 2); composes Skills (Layer 5); realizes Capabilities (Layer 4).
- **Ratified references** [E]: DM (Workflow); inv 13; Catalog P-D4/P-U6.
- **Evidence tag**: **[E]** entity/invariant ratified; external "Workflow/Pipeline" is a false cognate (Vocabulary §5 — ungoverned graph vs governed workflow).

## Layer 7 — Memory Layer

- **Purpose** [E]: hold **derived, non-authoritative** memory produced from Trace, upstream of promotion (DM §6.1, inv 8).
- **Responsibilities** [A]: **working memory** and **long-term memory** as derived records; **memory policies** (retention, scope); the **promotion boundary** — Memory is a *candidate source* for Knowledge, never authoritative itself.
- **Owned entities** [E]: **Memory** (cross-cutting Substrate, §8; derived from Trace, §6.1).
- **Allowed interactions** [E]: *reads* Trace (derivation, §6.1); is *promoted* to Knowledge **only via governed review** (inv 8); read/written in scope by Agent Instances.
- **Forbidden interactions** [E]: **must not rewrite Trace** (inv 5); **must not self-promote to Knowledge** (inv 8 — "never automatic"); must not be treated as authoritative (Vocabulary §4, `Memory ≠ Knowledge`).
- **Dependencies** [E]: depends entirely on Trace (derivation); depended-on by Governance (Layer 1) for promotion candidates.
- **Ratified references** [E]: DM §6.1, inv 5/8, §8.
- **Evidence tag**: **[E]** ratified; external "Memory" (self-editing/RAM/chat-buffer) is a high-risk false cognate — Letta *inverts* inv 8 (Log R-7).

## Layer 8 — Knowledge Layer

- **Purpose** [E]: hold governed, authoritative Knowledge entered only through promotion (DM inv 8, §8).
- **Responsibilities** [A]: **Knowledge lifecycle** (entered via governed admission/promotion); **Knowledge ownership** (cross-cutting substrate with an accountable Home Department — §5/§8); **Knowledge validation** (validity condition set by governed review).
- **Owned entities** [E]: **Knowledge** (cross-cutting Substrate, §8).
- **Allowed interactions** [E]: entered *only* via governed promotion from Memory (inv 8); *consumed* by Agent Instances (Relationship §5, Inferred).
- **Forbidden interactions** [E]: **cannot be entered/changed outside governed promotion** (inv 8); **is not** a retrieval index or vector store (Vocabulary §4, `Knowledge ≠ Vector Store/Index`).
- **Dependencies** [E]: depends on the Governance layer (promotion) and Memory (candidate source).
- **Ratified references** [E]: DM inv 8, §5, §8; Catalog P-A3 (external absent/inverted).
- **Evidence tag**: **[E]** ratified; **[A]/[O]** the versioned-identity model and admission are design-only/open (Mapping §9) — reserved to the Architect.

## Layer 9 — Infrastructure Layer

- **Purpose** [A]: provide the facilities *beneath* the entities (storage, execution substrate, external-dependency boundary), audited through the actions that invoke them — never as independent actors (OQ-2 interpretation; DM §8).
- **Responsibilities**: **Storage** [A] (persistence facility under Trace/Memory/Knowledge — Catalog P-U9); **external-dependency boundary** [E] (the **Tool** is the *only* entity permitted an external dependency — inv 12); **[O] Identity, Authentication, Networking, Database, Deployment boundary** — these have **no ratified AIOS entity** (Vocabulary §3.3/§8, Reserved) and are recorded as **reserved infrastructure concerns**, not specified here.
- **Owned entities** [E]: **Tool** (the external boundary); infrastructure facilities (non-entity).
- **Allowed interactions** [E]: a Tool holds the external dependency (inv 12); facilities are used *within* an Agent-Instance action.
- **Forbidden interactions** [E]: **only Tool may cross the vendor/external boundary** (inv 12); facilities **must not become independent traced actors** (OQ-2); infrastructure **must not own Knowledge** (Relationship §8).
- **Dependencies** [A]: used by every executing layer; owns no governance authority.
- **Ratified references** [E]: DM inv 12, §8; OQ-2 interpretation (Mapping); Catalog E-1…E-4 (ecosystem isolation).
- **Evidence tag**: **[E]** Tool/inv 12 ratified; **[O]** Identity/Auth/Networking/Deployment are **Reserved** — external "Identity/Authorization/Policy" are different-plane cognates (Vocabulary §5).

## Layer 10 — Optimization Layer

- **Purpose** [A]: the governed **learning loop** — evaluation, feedback, and improvement that feed the Memory→Knowledge promotion, without bypassing governance.
- **Responsibilities** [A]: **evaluation**; **feedback**; **improvement**; **learning loop** (Trace → Memory → governed review → Knowledge). **[O] "Model optimization"** (training/fine-tuning) has **no ratified AIOS entity** — the corpus reviewed it externally (LlamaFactory #10) as *evidence only*, governance-orthogonal; it is a **reserved** concern, not specified here.
- **Owned entities** [A]: none exclusively; operates over Trace, Memory, and the promotion edge — all under Governance (Layer 1).
- **Allowed interactions** [E]: may *detect/propose* (PR-3 Detect, Don't Decide) — e.g., propose a Memory candidate or a Questioned validity — but **decisions remain governed** (inv 8, Constitution §6.2 invariant 2).
- **Forbidden interactions** [E]: **must not decide governance** (PR-3); **must not auto-promote** (inv 8); must not mutate Trace (inv 5). Improvement *informs*, governance *decides*.
- **Dependencies** [E]: depends on Trace (evidence), Memory (derivation), Governance (promotion authority).
- **Ratified references** [E]: DM inv 8; PR-3, PR-4; §6.2.
- **Evidence tag**: **[A]** the loop is abstracted from ratified derivation/promotion; **[O]** model-optimization is reserved (external-only evidence).

---

## Cross-Layer Rules

[E]/[A] Grounded in ratified invariants and the Relationship Model.

- **Allowed dependencies** [A]: higher-responsibility layers may depend on lower facilities (execution depends on infrastructure; governance depends on Trace/Memory evidence). Capability→Skill→Workflow→Runtime→Agent-Instance is the execution realization chain (Relationship §9).
- **Forbidden dependencies** [E]: no layer may make Governance depend on execution *authority* (governance is not overridable by automation — §6.2 invariant 2); infrastructure/runtime **may not own Knowledge** (Relationship §8); execution **may not bypass promotion** to write Knowledge (inv 8).
- **Direction of information flow** [E]: **upward** — Trace → Memory → Knowledge (derivation then governed promotion; §6.1, inv 8).
- **Direction of authority** [E]: **downward** — from the Governance layer / Constitution §3 authority tiers to executing layers; automation may request/recommend but not override (§6.2 invariant 2).
- **Direction of execution** [E]: **downward** — Runtime → Agent Instance → Workflow → Skill/Tool; each action emits exactly one Trace (inv 4).
- **Direction of knowledge** [E]: **upward and gated** — knowledge only *ascends* into the Knowledge layer through the governed Memory→Knowledge promotion (inv 8); it never enters sideways or from below.
- **Direction of governance** [E]: **pervasive/top** — governance sits above execution and gates the single most important edge (promotion); Trace immutability (inv 5) constrains every layer equally.

[A] **The load-bearing boundary** (Catalog B-9≠B-12): **observability must never be conflated with accountability** — monitoring facilities (Infrastructure/Optimization) are distinct from the immutable Trace (Governance-owned). This is the corpus's highest-frequency false cognate and the specification's most important cross-layer rule.

---

## Architecture Principles

[E]/[A] Each summarized and referenced (no new principle introduced).

1. **Single Responsibility** [A] — each layer owns one coherent responsibility (design principle; corroborated by the corpus's clean-core convergence, Catalog E-4).
2. **Separation of Concerns** [A] — governance, execution, knowledge, and infrastructure are distinct layers (Relationship Model execution-half vs governance-half).
3. **Governance First** [E] — governance is atop the stack and gates authoritative change (Constitution; Catalog P-A1).
4. **Capability First** [E] — ability is Department-owned Capability, realized downward (DM §5; inv 10).
5. **Execution Isolation** [E] — agents collaborate only via Workflow/Knowledge/scoped Memory (inv 13); external capability only via Tool (inv 12).
6. **Memory before Knowledge** [E] — Knowledge is entered only by governed promotion from derived Memory (inv 8).
7. **Immutable Trace** [E] — every action produces exactly one immutable, append-only Trace record (inv 4/5, §14.2).
8. **Vendor Independence** [E] — external dependency is confined to the Tool boundary (inv 12); corroborated across all ten repos (Log R-1, n=10).
9. **Model Independence** [A] — no layer binds AIOS to a specific model/vendor; models are reached through the Tool boundary (inv 12; corpus R-1).
10. **Human Authority** [E] — automation may request/recommend but not override governance; promotion and decisions are human-governed (§6.2 invariant 2; inv 8; PR-3).

---

## Canonical Architecture Diagram (text)

[A] The canonical layering (no additional layers invented). Authority/execution flow **downward**; information/knowledge flow **upward and gated**; Trace/Memory/Knowledge are cross-cutting Substrate (§8).

```
                    ┌─────────────────────────────┐
   authority ↓      │   GOVERNANCE (Layer 1)       │   ↑ knowledge (gated)
                    │  decision · trace · promotion │
                    │  · review · policy authority  │
                    └─────────────┬───────────────┘
                                  │  gates promotion (inv 8)
   execution ↓                    ▼
        RUNTIME (2) → AGENTS (3) → CAPABILITIES (4) → SKILLS (5) → WORKFLOW (6)
                                  │  each action → exactly one Trace (inv 4)
                                  ▼
   ── cross-cutting Substrate (§8), immutable & gated ──────────────
        TRACE  ──derived──▶  MEMORY (7)  ──governed promotion (inv 8)──▶  KNOWLEDGE (8)
   ─────────────────────────────────────────────────────────────────
                                  │
        INFRASTRUCTURE (9)  [Tool = sole external boundary, inv 12]
        OPTIMIZATION (10)   [detect/propose only — governance decides, PR-3/inv 8]
```

[E] This mirrors the directive's example chain (Governance → Runtime → Agents → Capabilities → Skills → Workflow → Memory → Knowledge → Infrastructure) and the Relationship Model value chain (§9); Optimization is the governed learning loop over Trace/Memory/promotion.

---

## Implementation Boundary

[E] This document defines **architecture only.** It contains:
- **No implementation decisions**, **no APIs**, **no database schema**, **no runtime code**, **no class design**.

[O] Those belong to Phase 1B (DNA Consolidation) and onward, and are reserved to the Architect. [A] The layers, responsibilities, and cross-layer rules here are the *constraints* future implementation must satisfy — not the implementation.

---

## Consistency Review

[E] Checked against each source; introduces no rule and contradicts none.

- [E] **Constitution:** authority direction, §14.2 unconditional Trace, and §6.2 invariant 2 (human authority over automation) are used verbatim; nothing added or automated. Consistent.
- [E] **Domain Model:** every layer maps to ratified entities; inv 4/5/8/10/12/13 and §5/§6/§6.1/§8 anchor the responsibilities and forbidden interactions; no entity redefined; Substrate status (§8) preserved. Consistent.
- [E] **Principles Register:** PR-3 (Detect, Don't Decide) and PR-4 (Fail Closed) frame the Optimization/Governance boundary; no principle added or promoted. Consistent.
- [E] **Decision Review Method / Pattern Catalog / Mapping / Relationship Model / Vocabulary:** layers reuse their entities, relationships, gaps (Reserved concepts), and the B-9≠B-12 boundary unchanged; nothing silently closed. Consistent.
- [E] **Validation Log:** used read-only for corroboration context (R-1/R-4/R-6/R-7); **not modified**. Consistent.

[E] **No inconsistency found.**

---

## Open Questions (reserved to the Architect; not resolved)

- [O] Ratification of the *Inferred* relationships underlying Layers 4–6 (Capability↔Skill/Workflow; Agent↔Skill/Knowledge; Runtime↔Workflow — Relationship Model §12).
- [O] The **Reserved** infrastructure/optimization concerns (Identity, Authentication, Networking, Deployment, Model-optimization) — whether any becomes a ratified AIOS entity/layer, or stays external/reserved.
- [O] Whether Governance and Authority are entities-with-relationships or strictly layers/overlays (Mapping/Relationship open items).
- [O] Whether Memory→Knowledge needs a governed *read/consumption* path in addition to the governed write path (inv 8) — Relationship §13.
- [O] The Canonical Vocabulary naming disposition (two documents pending) and the standing reviewer-independence limit (Plan §9).
- [O] Authorization to enter Phase 1B — reserved entirely to the Architect.

---

## Closing

[E] This specification organizes AIOS as a ten-layer architecture built **entirely on the ratified entities, invariants, and relationships**, integrating the corpus evidence only as corroboration (never authority). [A] Its defining shape: **authority and execution flow downward; information and knowledge flow upward through a single governed promotion gate (inv 8); Trace is immutable substrate (inv 5); the external boundary is the Tool alone (inv 12); and human authority is never overridable by automation (§6.2 invariant 2).** [A] This is precisely the governance spine the external corpus does not have (Log R-4, n=10), placed atop the execution machinery the corpus does have. [O] All ratification, gap-closure, and progression to Phase 1B are reserved to the Architect.

**No implementation, code, API, database schema, class design, or runtime behavior was produced. No entity, relationship, or concept was invented; no canonical entity was renamed. The Constitution, Domain Model, Principles Register, Decision Review Method, Validation Log, Pattern Catalog, Pattern→Entity Mapping, Relationship Model, Canonical Vocabulary, and prior validation documents were not modified. This is a new additive architectural specification only.**
