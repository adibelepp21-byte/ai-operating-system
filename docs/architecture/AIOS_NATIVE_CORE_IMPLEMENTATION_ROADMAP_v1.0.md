# AIOS Native Core Implementation Roadmap v1.0

**Phase:** AIOS 2.98 — Native Core Implementation Roadmap. **Planning only.** The authoritative implementation sequence that bridges the frozen architecture into Phase 3.
**Stance** [A]: this document implements nothing, writes no Python, refactors nothing, changes no architecture, and revises no prior document. It defines build order, dependency order, governance gates, prerequisites, validation gates, and legacy reuse points — and nothing more.
**Derivation rule** [E]: the sequence is derived **Architecture → Dependencies → Governance → Conformance**, never from convenience or speed. It optimizes for **architectural safety**.
**Authoritative order (highest first)** [E]: Architecture Freeze → Implementation Constitution → Native Core Blueprint → Engineering Specifications (11) → Legacy Conformance Audit → Legacy Reuse Plan → Implementation Readiness Review → Architecture Specification → Relationship Model → Vocabulary Freeze → DNA Library → Domain Model → Constitution. No document is redefined.
**Tagging (never mixed):** **[E]** evidence from the sources above · **[A]** roadmap analysis · **[O]** Architect decision required.

---

## 1. Purpose

[A] To produce the **official, evidence-based implementation sequence** for the Native Core — so that Phase 3, when authorized, builds the eleven frozen subsystems in an order that upholds every invariant at every step, with a Fail-Closed governance gate between stages. [E] It is required because the Readiness Review found the architecture READY-WITH-CONDITIONS and the Reuse Plan dispositioned the legacy assets; what remains before building is the **order and the gates**.
[A] The roadmap converts the frozen dependency graph into a buildable sequence without authorizing any build.

## 2. Scope

[E] **In scope:** the build order, dependency order, per-subsystem roadmap, governance gates, validation strategy, legacy-reuse points, staged structure, and risks for the **eleven Native-Core boundaries** (Blueprint §4).
[E] **Out of scope, by rule:** any implementation, Python, refactor, architecture change, or document revision; the Spine ownership structure (Organization/Department — reserved to Phase 5); the deferred infrastructure concerns (Freeze §10); beginning Phase 3.
[A] Deliverable is a **sequence and its gates**, not code.

## 3. Evidence Base

[E] Each source's role:

| Source | Role in the roadmap |
|---|---|
| Architecture Freeze v1.0 | frozen entities/invariants/boundaries — the conformance target |
| Implementation Constitution v1.0 | the governance gate every stage must pass |
| Native Core Blueprint v1.0 | §20–§23 dependency/import/initialization order — **the spine of the sequence** |
| Engineering Specifications (11) | per-subsystem contracts and completion criteria |
| Legacy Conformance Audit v1.0 | per-module conformance evidence |
| Legacy Reuse Plan v1.0 | per-asset dispositions (CANONICAL_REFERENCE … REIMPLEMENT) |
| Implementation Readiness Review v1.0 | Phase-3 conditions (Knowledge admission model; `execution/` disposition) |
| Relationship Model / Vocabulary Freeze / DNA Library / Domain Model / Constitution | Observed relationships, canonical terms, governed DNA, ownership, authority |

## 4. Architectural Foundations

[E] The sequence rests on four frozen facts:
1. **Dependency directions** (Freeze §6): authority ↓, execution ↓, knowledge ↑ through the single governed promotion gate (INV-8); Trace immutable (INV-5).
2. **Trace is a sink** (Blueprint §13/§21): it depends only on a storage facility; everything else derives from it.
3. **The graph is acyclic** (Blueprint §21; Architecture Review §4): a total build order exists.
4. **Five un-bypassable governance boundaries** (Freeze §8): Trace, Knowledge-Promotion, Human-Authority, Tool, Governance — each must hold from the first stage that can reach it.

## 5. Roadmap Philosophy

[A] Five governing rules for the sequence:
- **Architecture before convenience** [E]: order follows the frozen dependency graph, not build ease.
- **A subsystem is built only after everything it depends on** [E: Blueprint §20/§23].
- **A subsystem is built only after the governance boundary it touches is enforceable** [E: Freeze §8].
- **No stage completes without a Fail-Closed governance gate** [E: Impl Constitution §10; PR-4].
- **Legacy is reused only through its disposition** [E: Reuse Plan] — CANONICAL_REFERENCE anchors, REUSE_AFTER_CONFORMANCE passes the gate first, REIMPLEMENT rebuilds under spec, HISTORICAL_ONLY is never built upon.

## 6. Native Core Overview

[E] The eleven boundaries (Blueprint §4) and their Domain-Model category:
- **Cross-cutting:** Trace.
- **Substrate:** Memory, Knowledge.
- **Governance:** Governance, Optimization (detect-only).
- **Execution:** Runtime, Agent, Skill, Workflow, and the Tool boundary within Infrastructure.
- **Facility:** Infrastructure.
[A] Spine (Organization/Department/Capability): Capability is in the Native Core; Organization/Department ownership is realized in Phase 5 (Freeze §13) — so Capability is built with its ownership context stubbed to governance, not to a full Department structure.

## 7. Complete Implementation Order

[E] The evidence-based order is the Blueprint §23 initialization order (grounded in the dependency graph), refined into eleven named build positions:

```
1. Infrastructure (facilities + Tool boundary)
2. Trace
3. Memory
4. Governance
5. Knowledge
6. Capability
7. Skill
8. Workflow
9. Agent
10. Runtime
11. Optimization
```

[A] **Note on the directive's illustrative order:** the example (Infrastructure → Trace → Governance → Runtime → Capability → Skill → Workflow → Agent → Memory → Knowledge → Optimization) front-loads Runtime and defers Memory/Knowledge. This roadmap instead follows **Blueprint §23**, because the frozen data/authority dependencies place **Memory before Governance** (Governance reads Memory candidates) and **Knowledge immediately after Governance** (Knowledge is entered only via the governed promotion gate). Following the graph rather than the execution-centric grouping is the architectural-safety optimization the directive requires. [E] Both agree on Infrastructure→Trace first and Optimization last.

### Justified transitions

[A] Each transition states: why-first · invariant · dependency · what-becomes-possible · what-stays-forbidden.

- **∅ → Infrastructure** [E]: nothing precedes facilities; they sit beneath the entities (Freeze §5 L9). *Invariant:* INV-12 (Tool is the sole external boundary) must exist before anything external is touched. *Enables:* a storage facility for Trace and the Tool boundary. *Forbidden:* any non-Tool external dependency; owning Knowledge.
- **Infrastructure → Trace** [E]: Trace depends only on a storage facility (Blueprint §13/§23). *Invariant:* INV-4/5/6. *Enables:* an immutable, append-only, unconditional record for every later action. *Forbidden:* editing/deleting/optional Trace.
- **Trace → Memory** [E]: Memory derives from Trace (Freeze §6). *Invariant:* INV-7/8. *Enables:* provisional, bounded, non-authoritative derivation and promotion candidates. *Forbidden:* Memory writing Trace; self-promotion.
- **Memory → Governance** [E]: Governance reads Trace and Memory candidates and gates promotion (Blueprint §5/§23). *Invariant:* INV-8; §6.2 invariant 2. *Enables:* the human decision authority and the promotion gate. *Forbidden:* automation deciding; execution overriding governance.
- **Governance → Knowledge** [E]: Knowledge is entered only via the governed promotion gate (INV-8). *Invariant:* INV-7/8. *Enables:* durable, versioned, authoritative Knowledge. *Forbidden:* any entry to Knowledge outside promotion.
- **Knowledge → Capability** [A]: Capabilities name governed abilities and declare versioned, queryable dependencies (INV-9/10/11); their governance context must exist first. *Invariant:* INV-1/9/10/11/14. *Enables:* owned, governed units of ability. *Forbidden:* ungoverned cross-Department dependency; orphan capability.
- **Capability → Skill** [E]: Skills are reusable abilities composed under Capabilities (Freeze §5 L5). *Invariant:* INV-15, INV-12 (no external dep), INV-4 (no independent Trace). *Enables:* composable, discoverable ability units. *Forbidden:* Skill holding external dependency or authoring independent Trace.
- **Skill → Workflow** [E]: Workflow composes Skills and is the sole multi-agent channel (INV-13). *Invariant:* INV-13, INV-4. *Enables:* governed composition with each step Trace-producing. *Forbidden:* collaboration outside Workflow/Knowledge/scoped Memory.
- **Workflow → Agent** [E]: Agent Definitions declare Capabilities/Skills/Workflows (INV-2/15); Agent Instances are the only actors (INV-3/4). *Invariant:* INV-2/3/4/13/15. *Enables:* the only actor, each action → one Trace. *Forbidden:* agent-to-agent outside Workflow; mutating Trace.
- **Agent → Runtime** [E]: Runtime hosts Agent Instances and drives execution (INV-3), producing Trace per action. *Invariant:* INV-3/4; OQ-2. *Enables:* execution of governed compositions as Trace-producing actions. *Forbidden:* Runtime owning Knowledge or being an independent traced actor.
- **Runtime → Optimization** [E]: Optimization observes Trace/Memory and proposes to Governance — last, because it depends on all of them (Blueprint §23). *Invariant:* PR-3; INV-8. *Enables:* a governed, detect-only learning loop. *Forbidden:* deciding governance; auto-promotion; mutating Trace.

[A] **Agent↔Runtime mutual reference** is resolved by building Runtime as a *facility that discovers Agent Definitions dynamically* (as the legacy `runtime.py` already does) — so Runtime need not statically know concrete definitions at construction; it hosts whatever Agent Definitions exist. This keeps the graph acyclic in code.

## 8. Dependency Graph

[E] Build-time dependencies (each subsystem → what it requires):

```
Infrastructure → (none)
Trace          → Infrastructure(storage)
Memory         → Trace
Governance     → Trace, Memory
Knowledge      → Governance
Capability     → Governance(ownership context)
Skill          → Capability, Infrastructure(registry facility)
Workflow       → Skill, (Runtime at execution time)
Agent          → Capability, Skill, Workflow, Runtime, Trace, Tool
Runtime        → Agent Definition (dynamically), Trace, Workflow
Optimization   → Trace, Memory, Governance
```

[A] **Acyclicity:** the only apparent cycles (Agent↔Runtime, Workflow↔Runtime) are execution-time coordination edges, not build-time construction edges; resolved by dynamic discovery (§7). Trace remains a pure sink. [E] Matches Blueprint §21 (acyclic core).

## 9. Subsystem Roadmaps

[A] Each subsystem, in build order, with the full attribute set. *Priority* = build position (§7). *Reuse* cites the Reuse Plan disposition.

### 9.1 Infrastructure
- **Purpose** [E]: facilities beneath entities + the single external boundary (Tool). **Entity:** Tool. **Layer:** L9. **Spec:** infrastructure_spec. **Blueprint pkg:** Infrastructure. **Priority:** 1.
- **Prerequisites** [E]: none (base). **Dependencies:** none. **Governance gates:** Tool boundary (INV-12). **Invariants:** INV-12. **Principles:** Fail Closed (PR-4), Single Responsibility.
- **Legacy assets** [E]: `tool*.py`, `verification.py` — REUSE_AFTER_CONFORMANCE / REUSE_AS_IS (Reuse Plan §6/§7). **Reuse:** behaviour after conformance.
- **Validation** [A]: no non-Tool external dependency; storage facility supports append-only Trace. **Deliverables:** storage facility, Tool boundary, execution substrate (all spec-conformant, no design change to invariants). **Completion:** INV-12 test passes; facilities author no Trace (OQ-2).
- **Blocked by** [E]: Architect authorization; Tool external-dependency confinement decision (Freeze §10). **Enables:** Trace storage; all external access. **Risks:** promoting a real external Tool before its confinement is ratified. **Reserved** [O]: Identity/Auth/Networking/Deployment/Scaling/Database/Observability implementations.

### 9.2 Trace
- **Purpose** [E]: immutable, append-only, unconditional per-action record. **Entity:** Trace. **Layer:** cross-cutting. **Spec:** trace_spec. **Pkg:** Trace. **Priority:** 2.
- **Prerequisites** [E]: Infrastructure storage. **Dependencies:** Infrastructure. **Gates:** Trace boundary (INV-4/5). **Invariants:** INV-4/5/6. **Principles:** Capture-Don't-Reference (PR-5).
- **Legacy** [E]: `trace_schema.py` CANONICAL_REFERENCE; `trace.py` REUSE_AFTER_CONFORMANCE (storage convention + full-provenance capture must be ratified — Reuse Plan §5/§7; Audit LR-2/LR-3).
- **Validation** [A]: exactly one record per action; write-once; capture-at-write; `knowledge_consumed`/`memory_consumed` fully captured. **Deliverables:** Trace record shape + append-only writer (spec-conformant). **Completion:** INV-4/5/6 tests pass.
- **Blocked by** [O]: Trace storage-convention ratification. **Enables:** Memory, Governance, Optimization, every traced action. **Risks:** inheriting empty consumption capture (LR-3). **Reserved** [O]: retention policy, audit export.

### 9.3 Memory
- **Purpose** [E]: derived, non-authoritative, retention-bounded record from Trace. **Entity:** Memory. **Layer:** L7. **Spec:** memory_spec. **Pkg:** Memory. **Priority:** 3.
- **Prerequisites** [E]: Trace. **Dependencies:** Trace (read only). **Gates:** Knowledge-Promotion boundary (upstream). **Invariants:** INV-5 (never write Trace), INV-7 (bounded), INV-8 (never self-promote). **Principles:** PR-3.
- **Legacy** [E]: `memory/*` REIMPLEMENT (Reuse Plan §10) — rebuild under memory_spec; reuse tiered-memory DNA (Letta), not the experiment code.
- **Validation** [A]: derives from Trace only; never rewrites Trace; surfaces candidates as proposals. **Deliverables:** governed derived-memory boundary. **Completion:** INV-5/7/8 tests pass; no promotion path.
- **Blocked by** [E]: Trace complete. **Enables:** Governance promotion candidates; Optimization signals. **Risks:** re-adopting experiment code instead of rebuilding (RU-3). **Reserved** [O]: tiered-memory model.

### 9.4 Governance
- **Purpose** [E]: authority over decisions and the Memory→Knowledge promotion. **Entity:** Governance (layer; not a DM entity). **Layer:** L1. **Spec:** governance_spec. **Pkg:** Governance. **Priority:** 4.
- **Prerequisites** [E]: Trace, Memory. **Dependencies:** Trace/Memory (read); directs Knowledge admission. **Gates:** Human-Authority + Knowledge-Promotion + Governance boundaries (Freeze §8). **Invariants:** INV-8; §6.2 invariant 2. **Principles:** PR-3 (Detect Don't Decide), PR-4.
- **Legacy** [E]: `promotion.py`, `memory_governance.py`, `review_decision.py` CANONICAL_REFERENCE; `human_review_observation.py` REUSE_AS_IS (Reuse Plan §5/§6).
- **Validation** [A]: automation proposes, humans decide; human reject absolute; capture-at-write. **Deliverables:** decision/review/promotion authority; the promotion gate. **Completion:** no automatic promotion; §6.2 invariant 2 upheld under test.
- **Blocked by** [E]: Memory complete. **Enables:** Knowledge admission; Optimization's proposal sink. **Risks:** automation acquiring a decision path (Critical). **Reserved** [O]: authority tiers, delegation records.

### 9.5 Knowledge
- **Purpose** [E]: durable, authoritative, versioned knowledge via governed promotion. **Entity:** Knowledge. **Layer:** L8. **Spec:** knowledge_spec. **Pkg:** Knowledge. **Priority:** 5.
- **Prerequisites** [E]: Governance. **Dependencies:** Governance (promotion), Memory (candidates). **Gates:** Knowledge-Promotion boundary. **Invariants:** INV-7/8. **Principles:** Governance First.
- **Legacy** [E]: `knowledge/*` REIMPLEMENT (Reuse Plan §10) — rebuild under knowledge_spec **after** the admission model is decided.
- **Validation** [A]: entry only via promotion; prior versions preserved. **Deliverables:** versioned, admission-gated Knowledge store. **Completion:** no unguided write path; INV-8 test passes.
- **Blocked by** [O]: **Knowledge admission model** (Readiness Review §18 condition 1; Freeze §10). **Enables:** Agent Knowledge consumption. **Risks:** building before admission model decided (RU-5, High). **Reserved** [O]: admission model, versioned-repository discipline, consumption path.

### 9.6 Capability
- **Purpose** [E]: Department-owned units of ability with explicit versioned dependencies. **Entity:** Capability. **Layer:** L4. **Spec:** capability_spec. **Pkg:** Capability. **Priority:** 6.
- **Prerequisites** [E]: Governance context. **Dependencies:** Department ownership (Phase-5 stub), governed versioned contracts. **Gates:** Governance boundary (INV-10). **Invariants:** INV-1/9/10/11/14. **Principles:** Capability First, Evidence First.
- **Legacy** [E]: none directly (the legacy harness has one real Agent Definition; Capability realization is minimal). **Reuse:** none / new under spec.
- **Validation** [A]: single-Department ownership; explicit, queryable, versioned dependencies; no orphan. **Deliverables:** governed capability model. **Completion:** INV-1/9/10/11/14 tests pass.
- **Blocked by** [O]: Department ownership (Phase 5) for full realization — built with a governance stub in Phase 3. **Enables:** Agent Definitions implementing Capabilities. **Risks:** cross-Department dependency without governance. **Reserved** [O]: Capability↔Skill/Workflow (Inferred).

### 9.7 Skill
- **Purpose** [E]: reusable, composable units of ability — facilities, not actors. **Entity:** Skill. **Layer:** L5. **Spec:** skill_spec. **Pkg:** Skill. **Priority:** 7.
- **Prerequisites** [E]: Capability, Infrastructure (registry facility). **Dependencies:** used by Agent; composed in Workflow. **Gates:** Tool boundary, Trace boundary. **Invariants:** INV-15, INV-12, INV-4. **Principles:** Single Responsibility.
- **Legacy** [E]: `skill.py` REUSE_AFTER_CONFORMANCE (Reuse Plan §7).
- **Validation** [A]: no external dependency; no independent Trace. **Deliverables:** discoverable Skill unit under Tool/Trace boundaries. **Completion:** INV-12/15 tests pass.
- **Blocked by** [E]: Capability. **Enables:** Workflow composition; Agent Skill declaration. **Risks:** Skill acquiring external dependency (INV-12). **Reserved** [O]: registry/discovery discipline.

### 9.8 Workflow
- **Purpose** [E]: governed composition; the sole multi-agent channel. **Entity:** Workflow. **Layer:** L6. **Spec:** workflow_spec. **Pkg:** Workflow. **Priority:** 8.
- **Prerequisites** [E]: Skill (composed); Runtime at execution time. **Dependencies:** Skill; executed by Runtime. **Gates:** the INV-13 collaboration boundary. **Invariants:** INV-13, INV-4. **Principles:** Governance First.
- **Legacy** [E]: `workflow.py` REUSE_AFTER_CONFORMANCE (Reuse Plan §7).
- **Validation** [A]: coordination only within Workflow/Knowledge/scoped Memory; each step Trace-producing; retry/branching not silently invented. **Deliverables:** governed, checkable composition. **Completion:** INV-13/4 tests pass.
- **Blocked by** [E]: Skill. **Enables:** Agent coordination; the only sanctioned multi-agent path. **Risks:** free agent-to-agent delegation (AD-9 anti-pattern). **Reserved** [O]: composition validation, failure-recovery model.

### 9.9 Agent
- **Purpose** [E]: Agent Definition (template) + Agent Instance (the only actor). **Entity:** Agent Definition/Instance. **Layer:** L3. **Spec:** agent_spec. **Pkg:** Agent. **Priority:** 9.
- **Prerequisites** [E]: Capability, Skill, Workflow, Runtime, Trace, Tool. **Dependencies:** all execution boundaries. **Gates:** Trace boundary; INV-13. **Invariants:** INV-2/3/4/13/15. **Principles:** Immutable Trace, Human Authority.
- **Legacy** [E]: `agent_instance.py`, `agent_definition.py` CANONICAL_REFERENCE (Reuse Plan §5).
- **Validation** [A]: implements ≥1 Capability; each Instance action → one Trace; no agent-to-agent; ephemeral Instance. **Deliverables:** governed definition/instance model with mandatory Trace. **Completion:** INV-2/3/4/13/15 tests pass.
- **Blocked by** [E]: Capability/Skill/Workflow/Runtime facility. **Enables:** actual traced execution. **Risks:** direct instance-to-instance coupling. **Reserved** [O]: Agent Factory (Phase 4).

### 9.10 Runtime
- **Purpose** [E]: host Agent Instances; drive execution as Trace-producing actions. **Entity:** Runtime. **Layer:** L2. **Spec:** runtime_spec. **Pkg:** Runtime. **Priority:** 10.
- **Prerequisites** [E]: Agent Definition (dynamically), Trace, Workflow. **Dependencies:** Agent, Workflow, Tool. **Gates:** OQ-2 (facility, not actor). **Invariants:** INV-3/4. **Principles:** Single Responsibility.
- **Legacy** [E]: `runtime.py` CANONICAL_REFERENCE; `orchestrator.py` CANONICAL_REFERENCE (Reuse Plan §5).
- **Validation** [A]: facility only; one Trace per action; resumable state distinct from Trace. **Deliverables:** execution engine binding definitions to instances. **Completion:** INV-3/4 tests pass; no Knowledge ownership.
- **Blocked by** [E]: Agent. **Enables:** end-to-end governed execution. **Risks:** conflating resumable state with immutable Trace (checkpoint-as-Trace). **Reserved** [O]: scheduling/isolation/lifecycle-states.

### 9.11 Optimization
- **Purpose** [E]: governed learning loop — detect/propose only. **Entity:** (none; detect-only). **Layer:** L10. **Spec:** optimization_spec. **Pkg:** Optimization. **Priority:** 11 (last).
- **Prerequisites** [E]: Trace, Memory, Governance. **Dependencies:** Trace/Memory (read), Governance (propose to). **Gates:** Human-Authority + Knowledge-Promotion. **Invariants:** INV-8, INV-5. **Principles:** PR-3, PR-4.
- **Legacy** [E]: `observability.py`, `metrics.py` REUSE_AFTER_CONFORMANCE; `promotion.py` CANONICAL_REFERENCE (Reuse Plan §5/§7).
- **Validation** [A]: informs, never decides; never auto-promotes; never mutates Trace. **Deliverables:** detect-only evaluation/proposal layer. **Completion:** PR-3 upheld; no decision path under test.
- **Blocked by** [E]: Governance complete. **Enables:** governed improvement proposals. **Risks:** automation acquiring a decision (Critical). **Reserved** [O]: model-optimization (external); evaluation-signal catalogue.

## 10. Governance Gates

[E] A **mandatory governance gate** sits at the exit of every stage (§14). Each gate verifies seven things and **defaults to FAIL CLOSED** (Impl Constitution §10; PR-4):

| Gate check | What it confirms |
|---|---|
| Architecture Conformance | affected frozen entities/invariants/boundaries cited and hold (Freeze) |
| Blueprint Conformance | boundary maps 1:1 to a frozen subsystem; import direction = dependency direction (Blueprint §20/§21) |
| Engineering Spec Conformance | the subsystem's spec responsibilities and forbidden dependencies are satisfied |
| Implementation Constitution Conformance | naming/dependency/ownership/Trace rules pass; change correctly classified (§4–§10) |
| Invariant Verification | the stage's required invariants pass their conformance tests (Blueprint §27) |
| Dependency Verification | no forbidden import; graph still acyclic |
| Failure Behaviour | **FAIL CLOSED** — if any check is uncertain, the stage does not pass and the next stage does not begin |

[A] A gate is passed by **governed human review** (PR-3; §6.2 invariant 2); automation may detect and propose gate findings but may not pass the gate.

## 11. Legacy Integration Plan

[A] Per subsystem, the legacy reuse points (from the Reuse Plan), by disposition:

| Subsystem | CANONICAL_REFERENCE | REUSE_AS_IS | REUSE_AFTER_CONFORMANCE | REIMPLEMENT | HISTORICAL_ONLY |
|---|---|---|---|---|---|
| Infrastructure | — | `verification.py` | Tool group | — | — |
| Trace | `trace_schema.py` | — | `trace.py` | — | `traces/` corpus |
| Memory | — | — | — | `memory/*` | `memory/records/` |
| Governance | `promotion`, `memory_governance`, `review_decision` | `human_review_observation` | — | — | — |
| Knowledge | — | — | — | `knowledge/*` | — |
| Capability | — | — | — | (new under spec) | — |
| Skill | — | — | `skill.py` | — | — |
| Workflow | — | — | `workflow.py` | — | — |
| Agent | `agent_instance`, `agent_definition` | — | — | — | — |
| Runtime | `runtime`, `orchestrator` | — | — | — | — |
| Optimization | `promotion` (shared) | — | `observability`, `metrics` | — | `baseline/` |
| (cross) | — | `governance_reader`, `tools/validators/*` | `execution/tests/*` | — | `run_*`, `baseline_capture` |

[E] No asset is ARCHIVE/REMOVE (Reuse Plan §11). CANONICAL_REFERENCE = build to match; REUSE_AFTER_CONFORMANCE = pass the gate first; REIMPLEMENT = rebuild under spec (reuse DNA, not code); HISTORICAL_ONLY = never build upon.

## 12. Validation Strategy

[A] Validation is **conformance to the frozen architecture**, not implementation detail (Blueprint §27):
- **Per-subsystem** [E]: the invariant tests named in §9 (e.g. INV-4 one-Trace-per-action, INV-5 no-mutation, INV-8 no-self-promotion, INV-12 single-external-boundary, INV-13 no-agent-to-agent).
- **Per-stage** [E]: the seven-check governance gate (§10), Fail Closed.
- **Cross-cutting** [A]: the acyclic-import check and the external-dependency sweep (the same evidence method used in the Conformance Audit) re-run at each gate.
- **Test provenance** [E]: `execution/tests/*` are re-based to assert frozen invariants (Reuse Plan §8) before they count as validation.
[E] Default everywhere: **FAIL CLOSED** (PR-4).

## 13. Risk Assessment

[A] Risks by class; each with cause · impact · mitigation · severity.

| Class | Risk | Cause | Impact | Mitigation | Severity |
|---|---|---|---|---|---|
| Dependency | Building a subsystem before its dependency | order not enforced | forbidden import; broken invariant | gate's Dependency Verification; follow §7 strictly | High |
| Dependency | Agent↔Runtime cycle in code | static cross-reference | non-acyclic graph | Runtime discovers definitions dynamically (§7) | Medium |
| Governance | Automation acquires a decision path | convenience in Governance/Optimization | human authority defeated (§6.2 inv 2) | PR-3 gate; detect-only; Fail Closed | **Critical** |
| Governance | Knowledge built before admission model | reserved item unresolved | ungoverned Knowledge entry | block §9.5 on Readiness Review §18 cond. 1 | High |
| Reuse | CANONICAL_REFERENCE copied with unratified convention | reference mistaken for ratification | unratified Trace storage in core | ratify convention separately (RU-1) | High |
| Reuse | REUSE_AFTER_CONFORMANCE skips the gate | schedule pressure | unverified code in core | gate mandatory; Fail Closed (RU-2) | High |
| Reuse | REIMPLEMENT re-adopts experiment code | DNA/code confusion | experimental code in core | rebuild under spec; DNA = ideas (RU-3) | Medium |
| Architecture | A later stage redefines a frozen item | drift | freeze violated | Architecture Conformance gate; change → §3 governance | High |
| Architecture | Deferred infra implemented as if frozen | scope creep | architecture invented outside governance | reserved-item boundary (Readiness Review §18 cond. 3) | Medium |
| Implementation | Trace made conditional/optional | performance pressure | silent unaccountable action | INV-4 test; unconditional production | **Critical** |
| Implementation | Checkpoint/resumable-state = Trace | Runtime state modeling | rewritable "accountability" | separate immutable Trace from resumable state | High |

## 14. Implementation Stages

[A] Six architectural implementation stages (not Agile iterations). Each ends with a governance gate (§10) and an **Architect authorization point** (§17). No stage begins before the prior stage's gate passes.

- **Stage I — Foundation Substrate.** *Purpose:* establish facilities and the accountability record. *Subsystems:* Infrastructure, Trace. *Dependencies satisfied:* storage, Tool boundary, immutable Trace. *Outputs:* Trace record + append-only writer; Tool boundary. *Reviews:* Architecture/Blueprint/Spec/Constitution + INV-4/5/6/12. *Exit:* INV-4/5/6/12 tests pass; no external dependency outside Tool. *Authorization:* Architect gate before Stage II.
- **Stage II — Derivation & Authority.** *Purpose:* derived memory and the governance/promotion gate. *Subsystems:* Memory, Governance. *Dependencies:* Trace present. *Outputs:* governed derived-memory boundary; decision/review/promotion authority. *Reviews:* INV-7/8; §6.2 invariant 2; PR-3. *Exit:* no automatic promotion; human authority upheld. *Authorization:* Architect gate before Stage III.
- **Stage III — Authoritative Substrate.** *Purpose:* governed Knowledge. *Subsystems:* Knowledge. *Dependencies:* Governance present; **admission model decided**. *Outputs:* admission-gated versioned Knowledge. *Reviews:* INV-7/8. *Exit:* no unguided write path. *Authorization:* Architect gate + admission-model decision before Stage IV.
- **Stage IV — Composition.** *Purpose:* governed ability and composition. *Subsystems:* Capability, Skill, Workflow. *Dependencies:* governance context; registry facility. *Outputs:* capability model; Skill units; governed Workflow. *Reviews:* INV-1/9/10/11/12/13/14/15. *Exit:* INV-13 holds; no external dep in Skill. *Authorization:* Architect gate before Stage V.
- **Stage V — Actors & Hosting.** *Purpose:* the only actor and its host. *Subsystems:* Agent, Runtime. *Dependencies:* composition present. *Outputs:* governed Agent definition/instance; execution engine. *Reviews:* INV-2/3/4/13/15; OQ-2. *Exit:* one Trace per action; no agent-to-agent; Runtime owns no Knowledge. *Authorization:* Architect gate before Stage VI.
- **Stage VI — Governed Learning.** *Purpose:* detect-only improvement. *Subsystems:* Optimization. *Dependencies:* Trace/Memory/Governance present. *Outputs:* detect-only proposal layer. *Reviews:* PR-3; INV-8/5. *Exit:* no decision path; no auto-promotion. *Authorization:* Architect closeout of Native Core.

## 15. Exit Criteria

[A] The Native Core is complete when **all** hold [E: derived from Freeze/Blueprint/specs]:
- Every one of the eleven boundaries exists, spec-conformant, in the frozen dependency graph.
- All six stage gates passed Fail-Closed governed review.
- The invariant test suite (INV-1…INV-15, §14.2) passes; the graph is acyclic; the external-dependency sweep is empty outside Tool.
- Every reused legacy asset entered only through its disposition; no REIMPLEMENT target was adopted as experiment code; no HISTORICAL_ONLY asset was built upon.
- No frozen item was redefined; every change traced to a frozen invariant/entity/boundary.
[O] Declaration of completion is the Architect's.

## 16. Readiness Assessment

- [A] **Roadmap readiness — READY:** the build order, dependency graph, per-subsystem roadmaps, gates, legacy-integration points, and staged structure are defined and consistent with the frozen architecture and the Reuse Plan.
- [A] **Implementation readiness — CONDITIONALLY READY:** Phase 3 may build in this order **once** the Architect authorizes it and resolves the gating conditions (Knowledge admission model before Stage III; `execution/` disposition already provided by the Reuse Plan; test framework and on-disk layout — reserved implementation choices).
- [O] **Reserved to the Architect:** authorization to begin; the admission model; the reserved implementation mechanisms; and each stage's authorization point.

## 17. Architect Authorization Points

[O] Explicit points where Phase 3 halts for the Architect:
1. [O] **Before Stage I** — authorize the start of Phase 3 and the Trace storage-convention ratification.
2. [O] **Before Stage III** — decide the **Knowledge admission model**.
3. [O] **At each stage gate (I→II→III→IV→V→VI)** — authorize progression only after the Fail-Closed gate passes.
4. [O] **Before any deferred/Inferred item** — separate ratification (Freeze §10; Inferred relationships).
5. [O] **Native Core closeout** — declare completion and authorize Phase 4 (Agent Factory).

## 18. Open Questions

[O] Reserved to the Architect:
- [O] Whether to follow Blueprint §23 order (this roadmap) or an alternative the Architect prefers.
- [O] The Knowledge admission model (gates Stage III).
- [O] Verbatim adoption vs. re-authoring of CANONICAL_REFERENCE assets (Reuse Plan §15).
- [O] Test framework, on-disk layout, registry/manifest/bootstrap mechanisms (reserved implementation choices).
- [O] Whether the untracked `execution/` tree is version-controlled, and when.
- [O] Department ownership realization (INV-1/2), reserved to Phase 5, and its stub form in Stage IV.

## 19. Integrity Verification

[E] Post-write verification for this planning document:
- **Files created:** 1 — `docs/architecture/AIOS_NATIVE_CORE_IMPLEMENTATION_ROADMAP_v1.0.md` (this document).
- **Python modified:** 0 — no code produced or changed.
- **execution/ changes:** 0 — not touched.
- **Architecture / engineering / governance documents modified:** 0.
- **Previous deliverable overwritten:** none — collision check was FREE; additive only.
- **Trace count:** 540 — unchanged.
- **Commit status:** not committed, not pushed.

[A] This roadmap implemented nothing, wrote no Python, refactored nothing, changed no architecture, and revised no prior document. **It sequenced only.**

## 20. Conclusion

[A] This roadmap defines the **official, architecturally-safe implementation sequence** for the Native Core: eleven subsystems built in the Blueprint §23 dependency order — Infrastructure → Trace → Memory → Governance → Knowledge → Capability → Skill → Workflow → Agent → Runtime → Optimization — across six architectural stages, each closed by a mandatory Fail-Closed governance gate, each drawing on legacy assets only through their ratified disposition. The order is derived from architecture, dependencies, governance, and conformance — never convenience or speed. [O] It authorizes no implementation; Phase 3 begins only on explicit Architect authorization, and every stage halts for the Architect at its gate.

**No implementation was produced; no Python was written; no file was refactored or renamed; no architecture, engineering, or governance document was modified; no prior deliverable was overwritten. This is a new additive, planning-only document. This roadmap does not begin Phase 3.**
