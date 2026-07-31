# AIOS Canonical Relationship Model v1.0

**Phase:** AIOS 1A.75 — inserted between Phase 1A.5 (Pattern → Entity Mapping) and Phase 1B (DNA Consolidation).
**Type:** Authorized **synthesis** artifact. **Descriptive only.** The standing "no synthesis" restriction is lifted **only** for this document. Additive; ratifies nothing; promotes nothing; creates no governance rule; changes no architecture; **does not redefine entities or alter the Domain Model**.
**Evidence sources (ONLY these):** `AIOS_CANONICAL_PATTERN_CATALOG_v1.0.md`, `AIOS_PATTERN_ENTITY_MAPPING_v1.0.md`, `AIOS_DR_VALIDATION_LOG_v1.0.md`, the ten repository validation documents, the ratified **Canonical Domain Model**, the **Constitution**, and the **Principles Register**. **No repository re-inspected; no external search; no new evidence.**
**Confidence discipline:** **[E]** directly stated in a ratified source / recorded evidence · **[A]** reasoned abstraction · **[O]** open question / Architect decision. **No untagged conclusions.**
**Status vocabulary (for this document):** **Observed** = the relationship is *stated in the ratified canon* (Domain Model / Constitution / Principles); **Inferred** = reasoned [A] from ratified invariants but not stated verbatim; **Architect Reserved** = **[O]** open, reserved.
**Entity/verb discipline:** uses only the twelve ratified Domain-Model entities and only the directive's sanctioned relationship verbs (`owns, creates, produces, consumes, uses, executes, contains, extends, depends_on, references, promotes, reads, writes, registers, exposes, coordinates`). **No entity, verb, or relationship is invented.**

---

## 1. Purpose

[A] **Why implementation should originate from relationships, not isolated entities:**
- [E] The Domain Model's force is largely *relational*: its invariants constrain **interactions** — inv 4 (Agent Instance action → Trace), inv 8 (Memory → Knowledge only via governed review), inv 12 (only Tool has external dependency), inv 13 (collaboration only via Workflow/Knowledge/scoped Memory). [A] These are properties of *edges*, not nodes; an entity built in isolation cannot enforce them.
- [A] Entities in isolation are inert; the governance guarantees live in *how they may and may not connect*. Building from relationships makes the invariants structural rather than incidental.

[A] **Why repositories cannot directly define AIOS relationships:**
- [E] Across all ten repositories, AIOS-sense governance relationships are **"not observed"** (Log R-4; Catalog P-A1): no external repo has a Memory→Knowledge promotion edge, an immutable per-action Trace edge, or a ratified authority edge. [A] The very relationships that define AIOS are absent externally; they cannot be copied, only constructed from the ratified canon.
- [E] External "relationships" are false cognates (Catalog §7): a repo's Agent→Memory edge is *auto-writing* (Letta inverts inv 8); its agent→agent edge is *free delegation* (CrewAI runs against inv 13). [A] Importing external edges would import governance inversions.

## 2. Scope

- [E] Defines **conceptual relationships only** between ratified entities.
- [E] Contains **no** implementation, architecture change, API, algorithm, runtime behavior, or governance promotion.
- [A] It explains *how ratified entities interact*; it does **not** create, rename, or re-scope any entity, and reserves all ratification to the Architect.

## 3. Relationship Philosophy

[A] The full chain, with relationships as the previously-missing bridge:

```
Evidence → Pattern → Entity → Relationship → Module → Implementation
```

[A] Phase 1A produced **Patterns** (recurrences); Phase 1A.5 produced **Entities** (candidate mapping to ratified entities). Neither yet said *how the entities connect under the invariants*. [A] **Relationships are the bridge**: they convert a set of entities into a governed system by fixing which edges are permitted, which are mandatory (e.g., inv 4), and which are forbidden (e.g., inv 8 auto-promotion). [O] Only after relationships are fixed can Modules and Implementation be responsibly derived — both reserved to later Phases.

## 4. Canonical Entity Inventory

[E] The twelve ratified Domain-Model entities. **No entity invented.** Origin = Canonical Domain Model.

| Entity | Purpose | Origin | Responsibility | Evidence | Confidence |
|---|---|---|---|---|---|
| **Organization** | Top of the governed hierarchy | DM §5 | Owns Departments; accountability root | [E] DM §5 | Strong |
| **Department** | Ownership/accountability unit | DM §5 | Owns Capabilities; bears accountability | [E] DM §5 | Strong |
| **Capability** | What a Department can do | DM | Named unit of governed ability; cross-Dept deps need governance (inv 10) | [E] DM, inv 10 | Strong |
| **Agent Definition** | The template of an agent | DM §6 | Defines an agent to be instantiated | [E] DM §6 | Strong |
| **Agent Instance** | A runtime execution of a Definition | DM §6 | The **only actor**; each action produces exactly one Trace (inv 4) | [E] DM §6, inv 4 | Strong |
| **Skill** | Reusable unit of ability | DM | Composable capability building block | [E] DM | Strong |
| **Workflow** | Governed composition of actions | DM, inv 13 | The sanctioned channel for multi-agent collaboration | [E] DM, inv 13 | Strong |
| **Tool** | External-capability boundary | DM, inv 12 | The **only** entity permitted an external dependency | [E] inv 12 | Strong |
| **Runtime** | Execution binding | DM §6 | Binds a Definition to execution; a facility, not an actor (OQ-2 interp., Mapping) | [E] DM §6; [A] Mapping | Strong |
| **Knowledge** | Governed, authoritative knowledge | DM, inv 8, §8 | Cross-cutting substrate; entered only via governed promotion | [E] DM inv 8, §8 | Strong |
| **Memory** | Derived, non-authoritative memory | DM §6.1, inv 8 | Derived from Trace; never self-promotes | [E] DM §6.1, inv 8 | Strong |
| **Trace** | Immutable accountability record | DM inv 4/5, §8 | Unconditional, append-only, one-per-action; cross-cutting substrate | [E] inv 4/5, §14.2 | Strong |

[E] Per DM §8, **Trace, Memory, and Knowledge are cross-cutting substrate** (non-private; not owned by any single Department).

## 5. Canonical Relationship Matrix

[E]/[A] Only evidence-supported relationships, using only sanctioned verbs.

| Entity A | Relationship | Entity B | Evidence | Confidence | Status |
|---|---|---|---|---|---|
| Organization | owns | Department | [E] DM §5 | Strong | Observed |
| Department | owns | Capability | [E] DM §5 | Strong | Observed |
| Department | owns | Agent Definition | [A] DM §5 ownership | Moderate | Inferred |
| Capability | exposes | Skill | [A] Mapping §5; DM | Moderate | Inferred |
| Capability | exposes | Workflow | [A] DM (Capability realized via governed composition) | Moderate | Inferred |
| Workflow | contains | Skill | [A] composition (Catalog P-U3) | Moderate | Inferred |
| Runtime | creates | Agent Instance | [E] DM §6 (Instance = runtime execution) | Strong | Observed |
| Agent Instance | references | Agent Definition | [E] DM §6 | Strong | Observed |
| Agent Instance | produces | Trace | [E] DM inv 4 | Strong | Observed |
| Workflow | coordinates | Agent Instance | [E] DM inv 13 | Strong | Observed |
| Agent Instance | uses | Tool | [E] DM inv 12 | Strong | Observed |
| Agent Instance | uses | Skill | [A] DM (Skills are agent abilities) | Moderate | Inferred |
| Agent Instance | consumes | Knowledge | [A] DM §8 (Knowledge is consumable substrate) | Moderate | Inferred |
| Tool | depends_on | (external dependency) | [E] DM inv 12 | Strong | Observed |
| Memory | reads | Trace | [E] DM §6.1 (Memory derived from Trace) | Strong | Observed |
| Memory | promotes → (via governed review) | Knowledge | [E] DM inv 8 (never automatic) | Strong | Observed |
| Capability | depends_on (cross-Department, via governance) | Capability | [E] DM inv 10 | Strong | Observed |
| Runtime | executes | Workflow | [A] Mapping (runtime binds/executes) | Moderate | Inferred |

[E] No unsupported relationship appears. [O] Any edge marked *Inferred* whose ratification matters is **Architect Reserved**.

## 6. Relationship Catalogue

[A]/[E] Each canonical relationship, individually.

- **Organization —owns→ Department.** Reason: the hierarchy root owns accountability units. [E] DM §5. Strong. Observed.
- **Department —owns→ Capability.** Reason: Capabilities are Department-scoped abilities. [E] DM §5. Strong. Observed.
- **Department —owns→ Agent Definition.** Reason: Definitions belong within the owning Department's accountability. [A] DM §5 ownership generalized. Moderate. Inferred.
- **Capability —exposes→ Skill / Workflow.** Reason: a Capability is realized through reusable Skills composed in governed Workflows. [A] Mapping §5; DM. Moderate. Inferred.
- **Workflow —contains→ Skill.** Reason: composition primitive (Catalog P-U3) assembles Skills into a Workflow. [A]. Moderate. Inferred.
- **Runtime —creates→ Agent Instance.** Reason: an Agent Instance is *a runtime execution of an Agent Definition*. [E] DM §6. Strong. Observed.
- **Agent Instance —references→ Agent Definition.** Reason: an Instance is the execution of a specific Definition (the definition is its template, not a copy — mirrors PR-5 capture at the identity level). [E] DM §6. Strong. Observed.
- **Agent Instance —produces→ Trace.** Reason: **every** Agent Instance action produces exactly one Trace record. [E] DM inv 4; Constitution §14.2 (unconditional). Strong. Observed.
- **Workflow —coordinates→ Agent Instance.** Reason: multi-agent interaction is permitted **only** via Workflow (or Knowledge / scoped Memory). [E] DM inv 13. Strong. Observed.
- **Agent Instance —uses→ Tool.** Reason: external capability is reached only through the Tool boundary. [E] DM inv 12. Strong. Observed.
- **Agent Instance —uses→ Skill.** Reason: Skills are the agent's reusable abilities. [A] DM. Moderate. Inferred.
- **Agent Instance —consumes→ Knowledge.** Reason: governed Knowledge is read by agents during action. [A] DM §8 substrate. Moderate. Inferred.
- **Tool —depends_on→ (external).** Reason: Tool is the *sole* holder of an external dependency. [E] DM inv 12. Strong. Observed.
- **Memory —reads→ Trace.** Reason: Memory is *derived from* Trace. [E] DM §6.1. Strong. Observed.
- **Memory —promotes(via governed review)→ Knowledge.** Reason: Memory becomes Knowledge **only** through governed human review, **never** automatically. [E] DM inv 8. Strong. Observed. [A] The *actor* is human governance, not Memory itself — Memory cannot self-promote.
- **Capability —depends_on(governed)→ Capability.** Reason: cross-Department Capability dependencies require governance. [E] DM inv 10. Strong. Observed.
- **Runtime —executes→ Workflow.** Reason: the runtime drives a Workflow's Agent-Instance actions. [A] Mapping. Moderate. Inferred.

[E] Verbs used are all from the sanctioned set; none invented.

## 7. Entity Responsibilities

[A] Conceptual only: owns / may create / may read / may update / must never directly modify.

| Entity | Owns | May create | May read | May update | Must NEVER directly modify |
|---|---|---|---|---|---|
| **Organization** | Departments | Departments | its hierarchy | ownership structure (governed) | Trace; Knowledge content |
| **Department** | Capabilities, Definitions | Capabilities | its Capabilities | its Capabilities (governed) | Trace; another Department's Capability (inv 10) |
| **Capability** | (its definition of ability) | — | its Skills/Workflows | — (it is a "what", not an actor) | anything (it does not execute — §8) |
| **Agent Definition** | (its template) | — | itself | itself (governed) | Trace; Capability |
| **Agent Instance** | (its execution) | Trace (by acting) | Knowledge, scoped Memory, Skills, Tools | scoped Memory (write) | **Trace after write (inv 5)**; Knowledge (except via promotion); Capability |
| **Skill** | (its logic) | — | — | — | Trace; Knowledge |
| **Workflow** | (its composition) | Agent-Instance coordination | its steps | its own composition (governed) | Trace records' content |
| **Tool** | (its external binding) | tool results | — | — | Trace; governance state |
| **Runtime** | (bindings) | Agent Instances | Definitions | — (facility, not actor) | Trace as an independent actor (OQ-2) |
| **Knowledge** | (its versions) | — | (read by agents) | **only via governed promotion (inv 8)** | itself outside governed promotion |
| **Memory** | (its derived records) | derived memory | Trace | its derived records | **Trace (inv 5)**; Knowledge directly (inv 8) |
| **Trace** | (its records) | — | (read by Memory) | **nothing — append-only (inv 5)** | **any existing record (immutable)** |

[E] The "must never modify" column is grounded in inv 5 (Trace immutable), inv 8 (Knowledge only via promotion), inv 10 (cross-Department), inv 12 (Tool boundary), §8 (substrate), and the OQ-2 interpretation (Runtime/infrastructure are facilities, not actors).

## 8. Relationship Constraints

[E]/[A] Architectural boundaries, each grounded in a ratified source. **Only supported constraints.**

- [E] **Trace must never become mutable.** Basis: DM inv 5 (Trace immutable, append-only); Constitution §14.2. Observed.
- [E] **Knowledge cannot bypass promotion.** Basis: DM inv 8 (Memory→Knowledge only via governed review, never automatic). Observed.
- [E] **Memory cannot rewrite Trace.** Basis: DM inv 5 + §6.1 (Memory is *derived from* Trace, read-only on it). Observed.
- [E] **Only Tool may hold an external dependency.** Basis: DM inv 12. Observed.
- [E] **Agent Instances may collaborate only via Workflow / Knowledge / scoped Memory.** Basis: DM inv 13. Observed.
- [E] **Cross-Department Capability dependencies require governance.** Basis: DM inv 10. Observed.
- [A] **Capability cannot execute itself.** Basis: a Capability is a Department-owned "what," not an actor; only Agent Instances act (DM §6, inv 4). Inferred.
- [A] **Runtime cannot own Knowledge.** Basis: Knowledge is cross-cutting substrate (§8), owned by no single entity; Runtime is a facility (OQ-2). Inferred.
- [A] **Agent cannot redefine Capability.** Basis: Capabilities are Department-owned (§5); agents execute, they do not own/define governance scope. Inferred.
- [E] **Facilities (Runtime, storage, infrastructure) are never independent traced actors.** Basis: OQ-2 interpretation (cited in Mapping); only Agent Instances (and human review) author Trace/decision records. Observed (interpretation).
- [A] **Observability must never be conflated with accountability.** Basis: Catalog P-U2/B-9≠B-12 — the corpus's highest-frequency false cognate; Trace (accountability) must stay distinct from any monitoring facility. Inferred (from evidence).

## 9. Interaction Lifecycle

[A] The canonical value chain, conceptual (no algorithms):

```
Capability → Skill → Workflow → Runtime → Agent Instance → Trace → Memory → Knowledge
```

- **Capability → Skill** [A]: a Department-owned Capability (§5) is realized through reusable Skills. Inferred.
- **Skill → Workflow** [A]: Skills are composed into a governed Workflow (P-U3; inv 13 is the collaboration channel). Inferred.
- **Workflow → Runtime** [A]: the Runtime binds Definitions and drives the Workflow's execution (DM §6). Inferred.
- **Runtime → Agent Instance** [E]: the Runtime creates an Agent Instance as the runtime execution of a Definition (DM §6). Observed.
- **Agent Instance → Trace** [E]: every Instance action produces exactly one immutable Trace record (inv 4/5, §14.2). Observed.
- **Trace → Memory** [E]: Memory is derived from Trace (§6.1) — read-only, never rewriting it. Observed.
- **Memory → Knowledge** [E]: Memory is promoted to Knowledge **only** via governed human review (inv 8) — the single most AIOS-distinctive transition, and the one no external repo has (Catalog P-A3). Observed.

[A] The chain's **left half** (Capability→…→Trace) is execution; its **right half** (Trace→Memory→Knowledge) is governance. The corpus (Log R-4) shows external systems implement the left half (sometimes more maturely) and stop at the execution-time human gate — AIOS's chain *continues* through the governance half.

## 10. Dependency Graph

[E]/[A] Evidence-supported edges only, grouped by kind. **No implementation dependencies.**

**Structural dependencies** (ownership/definition — DM §5/§6):
```
Organization ─owns→ Department ─owns→ Capability
Department ─owns→ Agent Definition
Capability ─exposes→ {Skill, Workflow}   [Inferred]
```

**Execution dependencies** (runtime — DM §6/inv 12/13):
```
Runtime ─creates→ Agent Instance ─references→ Agent Definition
Workflow ─coordinates→ Agent Instance ─uses→ {Tool, Skill}
Tool ─depends_on→ (external)
```

**Governance dependencies** (accountability/authority — inv 4/8/10; Constitution §3):
```
Agent Instance ─produces→ Trace            (inv 4, mandatory, unconditional)
Memory ─promotes(governed review)→ Knowledge (inv 8; human governance is the actor)
Capability ─depends_on(governed)→ Capability (inv 10, cross-Department)
Authority tiers (Constitution §3) govern which decisions may be approved  [E]
```

**Knowledge dependencies** (substrate — DM §8/§6.1):
```
Memory ─reads→ Trace ─(derived)→ Memory
Agent Instance ─consumes→ Knowledge        [Inferred]
{Trace, Memory, Knowledge} = cross-cutting substrate, non-private
```

[E] Each edge maps to a matrix row (§5). [O] Edges marked Inferred are Architect Reserved for ratification.

## 11. Consistency Review

[E] Checked against each source; introduces no rule and contradicts none.

- [E] **Constitution:** reserves ratification to the Architect (§6.2 invariant 2); §14.2 (unconditional Trace) and §3 (authority) are cited, not altered. Consistent.
- [E] **Domain Model:** every relationship/constraint maps to a ratified invariant or section (§5, §6, §6.1, §8, inv 4/5/8/10/12/13); no entity redefined, no invariant altered. Consistent.
- [E] **Pattern Catalog:** relationships align with its patterns (P-U*, P-A*) and its B-9≠B-12 boundary; nothing added/promoted. Consistent.
- [E] **Pattern → Entity Mapping:** entities and their gap-status are used unchanged (e.g., Runtime-as-facility, Knowledge admission still [O]). Consistent.
- [E] **Principles Register:** PR-1 (basis), PR-3/PR-4/PR-5 cited as constraints; none altered. Consistent.
- [E] **Validation Log:** used read-only for recurrence context; **not modified**. Consistent.

[E] **No inconsistency found.**

## 12. Architectural Readiness (for Phase 1B — DNA Consolidation)

- [E] The relationship layer now makes the invariants *relational and explicit*: the mandatory edge (inv 4), the forbidden edge (inv 8 auto-promotion), the boundary edges (inv 10/12/13), and the substrate status (§8) are all mapped with confidence and status.
- [A] Therefore AIOS is **conceptually ready to enter Phase 1B (DNA Consolidation)** — the entity + relationship layers together form the concept-level substrate DNA Consolidation would consolidate.
- [O] **Conditions reserved to the Architect:** several relationships are *Inferred* (Capability↔Skill/Workflow, Agent Instance↔Skill/Knowledge, Runtime↔Workflow) and several entity gaps persist (State/Context/Resource/Artifact/Decision have no entity — Mapping §9; Capability/infrastructure modules unbuilt; Knowledge admission open). [O] Whether these must be ratified *before* or *within* 1B is an Architect decision.
- [E] **Not assessed:** implementation readiness (out of scope).

## 13. Open Questions (reserved to the Architect; not resolved)

- [O] Should the *Inferred* edges (Capability→Skill/Workflow; Agent Instance→Skill/Knowledge; Runtime→Workflow) be ratified as canonical, or refined?
- [O] Is **Governance** itself an entity-with-relationships, or strictly a process/layer acting on the Memory→Knowledge edge? (Mapping treated it as a layer.)
- [O] What is the precise relationship of **Authority** (Constitution §3 tiers) to the entity graph — an edge, a cross-cutting overlay, or an external-to-entities construct?
- [O] Do **State/Context** (Mapping gaps) participate in relationships, or are they subsumed by Trace + scoped Memory + Runtime?
- [O] Does **Agent Instance —consumes→ Knowledge** need a governed read-path (analogous to the governed write-path inv 8), or is consumption unrestricted?
- [O] The standing **reviewer-independence** limit (Plan §9) and candidate refinements **MF-1…MF-12** remain open, not enacted.
- [O] Whether any relationship herein should be **ratified** into the Domain Model — reserved entirely to the Architect.

---

## Closing

[E] This document defines the canonical relationships among the twelve ratified AIOS entities, grounded edge-by-edge in the Domain Model, Constitution, and Principles Register, and consistent with the Pattern Catalog and Pattern→Entity Mapping. [A] Its central result: the invariants that make AIOS *AIOS* are **relational** — a mandatory Agent-Instance→Trace edge (inv 4), a governed-only Memory→Knowledge edge (inv 8), boundary edges (inv 10/12/13), and immutable substrate (inv 5, §8) — and the external corpus, which implements the execution half of the chain, has none of the governance half. [O] All ratification of Inferred edges, closure of open questions, and progression to Phase 1B are reserved to the Architect.

**No implementation, code, API, schema, algorithm, or runtime behavior was produced. No entity was invented, redefined, or re-scoped. The Domain Model, Constitution, Principles Register, Pattern Catalog, Pattern→Entity Mapping, prior validation documents, and Validation Log were not modified. No governance rule was created; no observation was promoted. This is a new additive synthesis document only.**
