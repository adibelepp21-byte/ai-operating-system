# AIOS Native Core Blueprint v1.0

**Phase:** AIOS 2.75 — Native Core Blueprint. The final architectural-planning layer before coding. **Not implementation.**
**Immutable basis:** Architecture Freeze v1.0 (immutable). This blueprint describes how the frozen architecture becomes a *source tree*, while remaining **completely implementation-neutral** — no code, APIs, classes, interfaces, schemas, databases, protocols, function names, framework or language assumptions, or code examples.
**Grounded ONLY in:** Constitution · Canonical Domain Model · Principles Register · Decision Review Method · Architecture Freeze · Engineering Specifications · Native Design · DNA Library. Repositories appear only as historical evidence **[E-hist]**.
**Confidence:** **[E]** ratified/frozen · **[A]** architectural planning abstraction · **[O]** open / Architect reserved. **No untagged conclusions.**
**Reading note** [A]: "package", "module", and "source tree" below denote **architectural module boundaries** — conceptual units of the future source, named after the frozen subsystems. No file name, extension, language, or packaging mechanism is implied.

---

## 1. Purpose
[A] To give every future code file one authoritative construction guide: which module boundary it belongs to, what that boundary owns, and which dependencies/imports it may and may not have. [E] The blueprint translates the frozen invariants and the engineering specifications into source-tree *organization and rules*, without deciding any implementation.

## 2. Native Source Tree Philosophy
[A] The source tree mirrors the **frozen architecture one-to-one**: one module boundary per frozen subsystem, arranged so the dependency directions of the architecture (Freeze §6) become **import directions** in the tree. [A] Three principles govern the tree: **the tree encodes the invariants** (a forbidden dependency is a forbidden import); **each boundary owns one responsibility** (Single Responsibility); **governance and accountability boundaries are un-crossable in code** (Trace immutability, promotion gate, Tool boundary). [E] No boundary may exist that has no ratified basis.

## 3. Root Source Tree
[A] Conceptually, the root organizes into: a **core** region (the eleven frozen subsystems), a **shared** region (cross-boundary primitives), and three cross-cutting *strategies* (registry, manifest, bootstrap). [A] Presented as a conceptual hierarchy (names only; no files/extensions):
```
core/
    trace/            memory/           knowledge/
    governance/       runtime/          agent/
    capability/       skill/            workflow/
    infrastructure/   optimization/
shared/
(registry strategy · manifest strategy · bootstrap strategy — described, not a folder mandate)
```
[E] Each `core/<subsystem>` boundary corresponds to a frozen subsystem and its engineering spec. [O] The exact on-disk layout (nesting, grouping) is an implementation decision reserved to Phase 3.

## 4. Core Package Structure
[A] The **core** region contains exactly the eleven frozen subsystem boundaries — no more (no new entity/subsystem may be introduced). [A] Each boundary is *self-contained* for its responsibility and communicates with others only along permitted dependency edges (Freeze §6). [E] The four Domain-Model categories organize the core conceptually: Spine (capability + the ownership context it lives in), Execution (runtime, agent, skill, workflow, and the Tool boundary in infrastructure), Substrate (memory, knowledge), Cross-cutting (trace).

## 5–15. Package Definitions
[A] Each package below states: Purpose · Ownership · Responsibilities · Allowed Dependencies · Forbidden Dependencies · Future Extension Points · Governance Constraints — grounded in its engineering spec and the frozen invariants.

### 5. Governance Package
- **Purpose** [E]: authority over decisions and the Memory→Knowledge promotion (Freeze §8; INV-8).
- **Ownership** [A]: governs the promotion edge and authority; owns no execution entity (Mapping §5).
- **Responsibilities** [E]: decision/review/promotion authority; detect-and-surface only (PR-3).
- **Allowed dependencies** [E]: reads trace, reads memory, directs knowledge admission.
- **Forbidden dependencies** [E]: must not be dependent on or overridable by execution authority (§6.2 invariant 2); must not mutate trace (INV-5); no external dependency (INV-12).
- **Future extension** [O]: authority tiers, delegation records (ADR framework) — reserved.
- **Governance constraints** [E]: automation may not decide (PR-3); non-delegable decisions per Constitution §3.2.

### 6. Runtime Package
- **Purpose** [E]: host Agent Instances; drive execution (INV-3; §L2).
- **Ownership** [A]: owns transient hosting state; owns no Knowledge, no Trace record.
- **Responsibilities** [E]: create Instances; ensure one Trace per action (INV-4); keep resumable state distinct from Trace.
- **Allowed dependencies** [A]: agent, workflow, and the Tool boundary (infrastructure).
- **Forbidden dependencies** [E]: knowledge ownership; independent Trace authorship (OQ-2); enabling agent-to-agent outside workflow (INV-13); non-Tool external dependency (INV-12).
- **Future extension** [O]: scheduling/isolation/lifecycle-states — reserved.
- **Governance constraints** [E]: coordination only via workflow; external only via Tool.

### 7. Capability Package
- **Purpose** [E]: Department-owned units of ability (INV-1).
- **Ownership** [E]: each Capability owned by exactly one Department.
- **Responsibilities** [E]: explicit versioned dependencies (INV-9); queryable dependency graph (INV-11); no orphan capabilities (INV-14).
- **Allowed dependencies** [E]: its Department; other Capabilities via governed versioned contracts (INV-9/10).
- **Forbidden dependencies** [E]: self-execution; ungoverned cross-Department dependency (INV-10); undocumented dependency (INV-11); external dependency (INV-12).
- **Future extension** [O]: Capability↔Skill/Workflow composition (Inferred) — reserved.
- **Governance constraints** [E]: cross-Department dependency requires governance (INV-10).

### 8. Agent Package
- **Purpose** [E]: Agent Definition (template) and Agent Instance (the only actor) (INV-2/3).
- **Ownership** [E]: Definitions owned by one Department; Instances not owned (transient, accountable to that Department).
- **Responsibilities** [E]: implement ≥1 Capability (INV-2); may declare 0+ Skills/Workflows (INV-15); each Instance action → one Trace (INV-4).
- **Allowed dependencies** [A]: runtime, capability, skill, workflow, tool, knowledge (consume), memory (scoped write).
- **Forbidden dependencies** [E]: mutate trace (INV-5); direct agent-to-agent outside sanctioned channels (INV-13); redefine capability; non-Tool external dependency (INV-12).
- **Future extension** [O]: Agent Factory (Phase 4) — reserved.
- **Governance constraints** [E]: agents propose, never decide promotion (INV-8; PR-3).

### 9. Skill Package
- **Purpose** [E]: reusable units of ability (INV-15).
- **Ownership** [E]: owned centrally.
- **Responsibilities** [A]: composable, discoverable ability; a facility, not an actor.
- **Allowed dependencies** [A]: used by agent; composed in workflow.
- **Forbidden dependencies** [E]: external dependency (INV-12); independent Trace (INV-4).
- **Future extension** [O]: registry/discovery discipline — reserved.
- **Governance constraints** [A]: skills execute ability; do not govern.

### 10. Workflow Package
- **Purpose** [E]: governed composition; sole multi-agent channel (INV-13).
- **Ownership** [E]: owned centrally.
- **Responsibilities** [A]: coordinate Instances; compose Skills; each step Trace-producing (INV-4).
- **Allowed dependencies** [A]: executed by runtime; composes skill.
- **Forbidden dependencies** [E]: collaboration outside itself/knowledge/scoped memory (INV-13); external dependency (INV-12); being the runtime (Workflow ≠ Runtime).
- **Future extension** [O]: composition validation — reserved.
- **Governance constraints** [E]: free agent-to-agent delegation is a rejected anti-pattern (Freeze AD-9).

### 11. Memory Package
- **Purpose** [E]: derived, non-authoritative memory from Trace (INV-7/8; §6.1).
- **Ownership** [E]: scoped by the producing Agent Instance/Department.
- **Responsibilities** [E]: derive from trace; bounded retention; surface promotion candidates (proposals only).
- **Allowed dependencies** [E]: reads trace.
- **Forbidden dependencies** [E]: write/rewrite trace (INV-5); write knowledge directly (INV-8); external dependency (INV-12).
- **Future extension** [O]: tiered memory (governed) — reserved.
- **Governance constraints** [E]: promotion only via governed review (INV-8); ranking may prioritize, never gate (PR-3).

### 12. Knowledge Package
- **Purpose** [E]: durable, authoritative, versioned knowledge via governed promotion (INV-7/8).
- **Ownership** [E]: collectively owned by the Organization; each item a home Department.
- **Responsibilities** [A]: versioned records; validity conditions from governed review; preserve prior versions.
- **Allowed dependencies** [E]: governance (promotion), memory (candidates).
- **Forbidden dependencies** [E]: entry outside promotion (INV-8); ownership by runtime/infrastructure; external dependency (INV-12).
- **Future extension** [O]: admission model, versioned repository, consumption path — reserved (Freeze §10).
- **Governance constraints** [E]: cannot bypass promotion (INV-8).

### 13. Trace Package
- **Purpose** [E]: immutable, append-only, unconditional per-action record (INV-4/5/6).
- **Ownership** [E]: owned by no one; governed by retention policy only.
- **Responsibilities** [E]: one record per action, unconditionally; write-once; capture at write-time (PR-5/INV-6); serve derivation reads.
- **Allowed dependencies** [A]: only an infrastructure storage facility beneath it.
- **Forbidden dependencies** [E]: memory, knowledge, optimization (they derive from trace); external dependency (INV-12).
- **Future extension** [O]: retention policy, audit export — reserved.
- **Governance constraints** [E]: immutability and unconditional production are governance guarantees (INV-4/5; §14.2).

### 14. Infrastructure Package
- **Purpose** [E]: facilities beneath entities + the single external boundary (Tool) (INV-12; OQ-2).
- **Ownership** [A]: facility-level; Tool owned centrally.
- **Responsibilities** [E]: confine all external coupling to Tool (INV-12); provide storage under substrate; provide execution substrate.
- **Allowed dependencies** [A]: used by trace/memory/knowledge (storage), runtime (substrate), agent (tool).
- **Forbidden dependencies** [E]: any non-Tool external dependency (INV-12); owning knowledge; independent Trace authorship (OQ-2).
- **Future extension** [O]: **reserved/deferred** — Identity, Authentication, Networking, Database impl, Deployment, Scaling, Observability impl (Freeze §10).
- **Governance constraints** [A]: infrastructure serves; never governs.

### 15. Optimization Package
- **Purpose** [E]: governed learning loop — detect/propose only (PR-3; INV-8).
- **Ownership** [A]: owns non-authoritative evaluation signals/candidates.
- **Responsibilities** [A]: observe trace/memory; propose candidates/conditions to governance.
- **Allowed dependencies** [E]: reads trace, reads memory; submits to governance.
- **Forbidden dependencies** [E]: decide governance (PR-3); auto-promote (INV-8); mutate trace (INV-5); external dependency (INV-12).
- **Future extension** [O]: model-optimization is external/reserved (Freeze §10).
- **Governance constraints** [E]: informs; never decides.

## 16. Shared Components
[A] A **shared** region holds only cross-boundary *primitives* that carry no subsystem responsibility (e.g., common value notions, confidence-tagging conventions, error/failure signaling concepts). [E] Shared components may hold **no** external dependency (INV-12), **no** governance authority, and **no** entity ownership. [A] Shared is a *sink* in the dependency graph: everything may depend on shared; shared depends on nothing in core. [O] Its exact contents are reserved to Phase 3.

## 17. Registry Strategy
[A] Registries (e.g., for Skills, Tools) are **lookup facilities, not actors** (Pattern Catalog P-U8; OQ-2). [E] A registry authors no independent Trace and holds no external dependency; it registers and resolves by name within its owning boundary. [A] Registration is a facility beneath governance; discovery never bypasses a subsystem's dependency rules. [O] Registry scope/discipline reserved.

## 18. Manifest Strategy
[A] A **manifest** is a declarative description of what a module boundary *is and declares* (its subsystem, its owned responsibilities, its declared dependencies) — used for governance visibility (INV-11: dependencies must remain queryable). [E] Manifests declare; they do not execute and hold no authority. [O] Manifest form/content is reserved (no schema/format defined here).

## 19. Bootstrap Strategy
[A] Bootstrap is the *ordered establishment* of module boundaries so that no boundary is available before its dependencies. [A] It performs no governance decision and creates no entity; it only makes boundaries ready in dependency order (§23). [E] Bootstrap must respect Fail Closed (PR-4): if a required lower boundary is unavailable, higher boundaries do not start. [O] Bootstrap mechanism reserved.

## 20. Dependency Rules
[E] Dependencies follow the frozen directions (Freeze §6):
- **Downward (allowed):** governance → (reads) trace/memory; execution → infrastructure facilities; runtime → agent/workflow/tool.
- **Upward, gated (allowed):** trace → memory (derivation) → knowledge (governed promotion only, INV-8).
- **Forbidden:** trace → memory/knowledge/optimization; memory → trace-write (INV-5); execution → knowledge-write bypassing promotion (INV-8); any non-Tool → external (INV-12); execution-authority → governance (§6.2 invariant 2); any → self-executing capability.
[A] Every forbidden dependency above is also a forbidden import (§21).

## 21. Import Rules
[A] Import direction **is** dependency direction. [E] Concretely: the **trace** boundary imports nothing from memory/knowledge/optimization; only the **infrastructure/Tool** boundary may import external-facing facilities (INV-12); the **governance** boundary is never imported *as an authority* by execution (§6.2 invariant 2); **shared** is importable by all and imports no core boundary. [A] A cyclic import between core boundaries is prohibited (the dependency graph is acyclic — Architecture Review §4). [O] Import-enforcement mechanism is an implementation choice reserved to Phase 3.

## 22. Ownership Rules
[E] Ownership follows Domain Model §5 exactly: Organization owns Departments; Departments own Capabilities and Agent Definitions; Skills/Tools/Runtime/Workflow owned centrally; Knowledge collectively owned with a home Department; Memory scoped to the producer; Trace owned by no one. [A] A module boundary's *code ownership* mirrors its entity ownership — no boundary may own data an entity does not own.

## 23. Initialization Order
[A] Grounded in the dependency graph (a defensible order; exact mechanism reserved):
1. **infrastructure facilities** (storage/substrate beneath everything).
2. **trace** (foundation; depends only on a storage facility).
3. **memory** (derives from trace).
4. **governance** (reads trace/memory; gates promotion).
5. **knowledge** (entered via governance).
6. **capability / skill / workflow** (composition units).
7. **agent** (definitions/instances).
8. **runtime** (hosts instances; drives workflows).
9. **optimization** (observes; proposes) — last.
[E] Order respects Fail Closed (PR-4): nothing higher initializes without its lower dependencies. [O] Exact sequencing reserved to Phase 3.

## 24. Layer Interaction
[E] Interactions occur only along permitted edges (Freeze §6; Relationship Model): runtime creates agent instances; workflow coordinates them (INV-13); instances produce trace (INV-4), use tools (INV-12), consume knowledge, write scoped memory; memory feeds governed promotion into knowledge (INV-8); governance reads trace/memory and gates promotion; optimization proposes to governance. [A] No interaction crosses a forbidden edge; observability never crosses into accountability (Freeze AD-8).

## 25. Extension Strategy
[E] Extension happens *within* a boundary's rules, never by adding a new entity or crossing an invariant: new Tools (external capability, INV-12), new Skills/Workflows (INV-15), new Capabilities (governed, INV-9/10), new evaluation signals (detect-only, PR-3). [A] Any extension requiring a frozen invariant/entity/boundary change is **out of bounds** until governance amends the architecture (Freeze §9). [O] The Reserved concerns (§14) enter only by governed ratification.

## 26. Module Isolation Rules
[E] Each boundary is isolated: it exposes only its permitted interactions and hides its internals; it holds no forbidden dependency; it authors Trace only where it *is* the acting Agent-Instance path (facilities author none — OQ-2). [A] Isolation is what makes the invariants locally enforceable — a boundary cannot violate an invariant it cannot reach. [E] The five governance boundaries (Freeze §8) are un-crossable in code.

## 27. Testing Philosophy
[A] Testing is **conformance to the frozen architecture**, not implementation detail: tests assert that invariants hold (e.g., an action always yields exactly one Trace, INV-4; Trace never mutates, INV-5; Memory never self-promotes, INV-8; only Tool crosses the external boundary, INV-12; no agent-to-agent outside Workflow, INV-13). [E] Evidence First (PR-1): tests verify observed behavior against ratified invariants. [O] Test framework, structure, and mechanics are reserved to Phase 3 (no framework assumed here).

## 28. Future Expansion Strategy
[O] Expansion proceeds by *governed phases*, not ad-hoc growth: Phase 3 (Native Core) builds the eleven boundaries to their specs; Phase 4 (Agent Factory) adds governed agent construction; Phase 5 (Department Architecture) realizes ownership structure. [A] Each new boundary must first have a ratified basis; deferred concerns (§14) await Architect ratification.

## 29. Implementation Boundary
[E] This blueprint contains **no** implementation: no code, APIs, classes, interfaces, schemas, databases, protocols, function names, framework or language assumptions, or code examples. [A] It defines *where* code will live and *what rules* it must obey; it does not write it. Implementation begins only in Phase 3, under Architect authorization, and must conform to this blueprint and the Freeze.

## 30. Consistency Review
- [E] **Architecture Freeze:** the tree mirrors the twelve entities, ten layers, and frozen boundaries; no invariant is weakened; no new entity/subsystem introduced. Consistent.
- [E] **Engineering Specifications:** each package corresponds to its spec's purpose, dependencies, and constraints. Consistent.
- [E] **Domain Model / Constitution / Principles:** ownership (§5), invariants (§7), authority (§3/§6.2), and PR-1/3/4/5 are reproduced as tree rules, unaltered. Consistent.
- [E] **Native Design / DNA Library:** the governance spine and observability≠accountability boundary are encoded as import/isolation rules; the two inversions remain rejected. Consistent.
- [E] **No inconsistency found; no prior document modified.**

## 31. Readiness Assessment
- [A] **Blueprint readiness — READY:** the source-tree organization, dependency/import/ownership rules, initialization order, isolation, and extension strategy are defined and consistent with the frozen architecture; every future code file now has an authoritative home and rule-set.
- [A] **Implementation readiness — CONDITIONALLY READY:** Phase 3 may build the eleven core boundaries against their specs; the deferred/Inferred items (§14; Capability↔Skill/Workflow) must first pass governance and may not be silently implemented.
- [O] **Reserved to the Architect:** exact on-disk layout, registry/manifest/bootstrap mechanisms, test framework, and any deferred concern — none defined here. Authorization to begin Phase 3 is reserved.

---

## Closing
[A] This blueprint converts the frozen architecture into an implementation-neutral construction guide: eleven core module boundaries mirroring the frozen subsystems, a dependency/import graph that *is* the invariant set, ownership mirroring the Domain Model, an initialization order that respects Fail Closed, and an extension strategy that cannot cross a frozen boundary. [E-hist] The validated corpus appears only as history behind the reusable ideas (registries as facilities, single external boundary, observability separated from accountability). [O] All mechanisms, layouts, and the start of Phase 3 are reserved to the Architect.

**No implementation, code, API, class, interface, schema, database, protocol, function name, framework assumption, language assumption, or code example was produced. No new entity, subsystem, or invariant was introduced; no canonical entity was renamed. The Constitution, Domain Model, Principles Register, Decision Review Method, Architecture Freeze, Engineering Specifications, Native Design, DNA Library, and all prior documents were not modified. This is a new additive blueprint document only.**
