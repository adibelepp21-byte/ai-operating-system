# AIOS Canonical Domain Model

**Status:** Canonical
**Version:** v1.0
**Authority:** AIOS Semantic Foundation
**Approved by:** System Architect

---

## 1. Canonical Entity List

Twelve entities across four categories.

| Category | Entities |
|---|---|
| Spine | Organization, Department, Capability |
| Execution | Agent Definition, Agent Instance, Skill, Workflow, Tool, Runtime |
| Substrate | Knowledge, Memory |
| Cross-cutting | Trace |

---

## 2. Entity Definitions

| Entity | Definition |
|---|---|
| **Organization** | The whole of AIOS. Single root identity; ultimate accountable body. |
| **Department** | A bounded, semi-autonomous unit of accountability with its own domain vocabulary. Owns Capabilities and Agent Definitions. |
| **Capability** | A stable, named, outcome-oriented contract — what can be delivered, independent of how. Owned by exactly one Department. The unit that persists across model, vendor, and Agent changes. Carries dependency-governance rules (§5, §7). |
| **Agent Definition** | A stable, versioned specification: what a class of Agent does, which Capabilities it implements, which Department owns it, what behavior/permissions/Skills/Workflows it is allowed to use, and what Runtime requirements it has. Does not run — it is the design, not the process. |
| **Agent Instance** | A single, ephemeral runtime execution of an Agent Definition. Hosted by a Runtime. Has its own execution lifecycle (spawned → active → terminated), independent of the Agent Definition's own version lifecycle. Produces Trace. |
| **Skill** | A discrete, reusable, bounded unit of executable ability, invoked by an Agent Instance or Workflow. |
| **Workflow** | An explicit, inspectable composition of Skills (and possibly Agent Instance invocations) accomplishing a multi-step outcome. |
| **Tool** | An integration point to something outside AIOS's own cognition. The only entity type permitted to hold a direct external/vendor dependency. |
| **Runtime** | The execution substrate that hosts Agent Instances. The conceptual seam where model/infrastructure substitution occurs. |
| **Knowledge** | Curated, canonical, reviewed, versioned understanding. Durable; not casually deleted. |
| **Memory** | Dynamic, experiential, scoped record of what an Agent Instance has encountered. Provisional. Has a retention window — promote or expire. |
| **Trace** | The immutable, append-only, unconditional audit record of one Agent Instance action. See §2.1. |

### 2.1 Trace — Required Contents

Every Trace record contains:

- Agent Definition version (which specification was in effect)
- Agent Instance (which execution produced this)
- Runtime (what it ran on)
- Skills used
- Tools used
- Knowledge consumed (captured content, not merely a reference — see §6)
- Memory consumed (captured content, not merely a reference — see §6)
- Outputs produced
- Cost/resource metadata
- Success / failure / escalation status

### 2.2 Why Agent Definition and Agent Instance Are Separate

A stable specification and an ephemeral execution have incompatible
lifecycles: a Definition changes on a deliberate, versioned,
Department-governed cadence; an Instance is created and destroyed
constantly, sometimes many times per minute, with no governance overhead
per spawn. The split makes Agent Definition governable at the same cadence
as Capability and Department (slow, deliberate), while Agent Instance is
governed at the cadence of Runtime and Trace (constant, cheap, disposable).
This is also what makes "Agent Definition implements Capability" a
meaningful, stable statement.

---

## 3. Entity Categories

- **Spine** (tree-shaped, single ownership, slow-changing): Organization,
  Department, Capability
- **Execution** (many-to-many with Capability, fast-changing): Agent
  Definition, Agent Instance, Skill, Workflow, Tool, Runtime
- **Substrate** (graph-structured, cross-cutting, addressable from
  anywhere): Knowledge, Memory
- **Cross-cutting / emergent** (byproduct of Execution touching Substrate,
  not a subsystem in its own right): Trace

---

## 4. Relationships

- Organization **owns** Department
- Organization **governs** Department
- Department **owns** Capability
- Department **owns** Agent Definition
- Capability **depends on** Capability *(governed — see §7)*
- Agent Definition **implements** Capability
- Capability **governs** Agent Definition
- Agent Definition **specifies** Skill, Workflow (what it is
  permitted/required to use)
- Agent Instance **instantiates** Agent Definition
- Runtime **hosts** Agent Instance
- Agent Instance **invokes** Skill
- Agent Instance **invokes** Tool
- Agent Instance **follows** Workflow
- Workflow **contains** Skill
- Workflow **invokes** Agent Instance
- Skill **invokes** Tool
- Agent Instance **consumes** Knowledge
- Agent Instance **consumes** Memory
- Agent Instance **learns from** Knowledge
- Agent Instance **learns from** Memory
- Agent Instance **produces** Memory
- Agent Instance **produces** Trace *(unconditional — every action, no
  exceptions)*
- Memory **promotes to** Knowledge *(governed review only, never
  automatic)*
- Trace **references** Agent Definition, Agent Instance, Runtime, Skill,
  Tool, Knowledge, Memory
- Agent Instance **collaborates with** Agent Instance — only through a
  shared Workflow, Knowledge, or an appropriately-scoped Memory. Direct
  instance-to-instance channels do not exist in this model. A transient,
  pairwise coordination need is satisfiable as a Memory scoped to that
  pair — this does not require a new entity.

---

## 5. Ownership Rules

| Entity | Owner |
|---|---|
| Department | Organization |
| Capability | Exactly one Department |
| Agent Definition | Exactly one Department |
| Agent Instance | Not owned — a transient instantiation, tracked by Runtime, accountable to the Department that owns its Agent Definition |
| Skill / Tool / Runtime | Owned centrally |
| Knowledge | Collectively owned by the Organization; each item has a home Department |
| Memory | Owned/scoped by the Agent Instance (or Department) that produced it |
| Trace | Owned by no one — immutable, append-only, governed only by retention policy |

---

## 6. Lifecycle Rules

| Entity | Lifecycle |
|---|---|
| Department, Capability | Created/retired via architectural decision, architect approval. Capability deprecation requires a defined sunset path. A Capability with zero active Agent Definitions implementing it is an invalid steady state and must be flagged for governance review — it is not silently acceptable. |
| Agent Definition | Versioned; created/deprecated at Department discretion within Capability governance. Its version is bound to the Capability contract version it implements. |
| Agent Instance | Fastest-changing lifecycle in the model, by design: spawned, active, terminated — no governance overhead per instance. |
| Skill / Tool | Versioned independently; may evolve as long as the interface is preserved. Because AI-implemented Skills can drift behaviorally without an interface change, Skill/Tool version changes that alter behavior materially should be documented at promotion time, not just interface-checked. |
| Knowledge | Versioned; revised/superseded via review; not casually deleted — audit trail matters. |
| Memory | Has an explicit retention window. Promote or expire. Expiry does not compromise any Trace that already referenced it (§6.1). |
| Trace | Append-only. Never mutated. Retained per policy. |

### 6.1 The Trace/Memory Relationship

Trace does not merely point at Memory or Knowledge — it captures the
relevant content of what it consumed at the time of the action. Memory may
expire on its own schedule without ever compromising the explainability of
a Trace that already recorded what it needed from that Memory at
write-time. Trace's durability guarantee therefore never depends on any
other entity's continued existence.

---

## 7. Invariants Derived from the Model

1. Every Capability is owned by exactly one Department.
2. Every Agent Definition is owned by exactly one Department and
   implements at least one Capability.
3. Every Agent Instance instantiates exactly one Agent Definition and is
   hosted by exactly one Runtime.
4. Every Agent Instance action produces exactly one Trace record —
   production is unconditional, never optional.
5. Trace is immutable and append-only; once written, never edited or
   deleted.
6. Trace captures the content it references at write-time; its
   explainability never depends on the continued existence of any Memory
   or Knowledge item it cites.
7. Knowledge is durable and is not casually deleted; Memory has a bounded
   retention window.
8. Memory is promoted to Knowledge only through governed review — never
   automatically.
9. Every Capability-to-Capability dependency must be explicit and must
   reference a specific versioned contract.
10. Cross-Department Capability dependencies require governance approval
    through the Decision-Making Process — never silent adoption.
11. The full graph of Capability dependencies must remain queryable and
    observable at all times — no undocumented dependencies.
12. Tool is the only entity type permitted to hold a direct
    external/vendor dependency; no other entity may integrate with an
    outside system directly.
13. No Agent Instance may collaborate directly with another Agent Instance
    outside of a shared Workflow, Knowledge, or scoped Memory.
14. A Capability with zero active Agent Definitions implementing it is an
    invalid steady state and must be flagged for governance review.

---

## 8. Architectural Boundaries

- The Spine is intentionally shallow (three levels) and is not to be
  deepened or bypassed without an architectural decision.
- Execution-layer entities are many-to-many with Capability by design —
  this is not accidental flexibility, it is the mechanism for reuse and
  for vendor/model independence.
- Substrate entities are cross-cutting and addressable from any point in
  the Spine or Execution layer — they are not owned by, or private to, any
  single Department, Capability, or Agent.
- Runtime and Tool are the only entities permitted to name or imply
  anything about specific external technology, vendors, or models. No
  other entity's definition may reference implementation detail.
- This document defines the conceptual domain only. It does not define,
  imply, or constrain repository layout, programming languages, storage
  technology, or APIs — those are separate, later artifacts that will be
  projections of this model, not extensions to it.
- Changes to this model follow the same governance discipline as the rest
  of AIOS: this document is subject to the Constitution's Amendment
  Process.

---

## 9. Explicit Non-Goals

This model deliberately does **not** include:

- **ADR / RFC** as entities — they are process artifacts about changes to
  this model, not part of the model itself.
- **Product / Service / Platform / Ecosystem** as entities — these are
  exposure/maturity postures of a Capability, not new structural concepts.
- **Contract** as a separate entity — carried entirely within Capability's
  own definition.
- **Process** as a concept distinct from Workflow — one term, not two.
- **Policy** as a top-level entity — modeled as a category of Knowledge.
- **Message / Event** as an entity for Agent-to-Agent communication —
  collaboration is required to route through Workflow, Knowledge, or
  scoped Memory; no direct channel exists.
- **Session** as a first-class entity — represented as a scope attribute
  on Memory and Trace.
- Any resolution, in either direction, of whether Runtime should
  ultimately be an attribute rather than an entity — retained as an entity
  for v1.0 pending future evidence it needs independent governance.

---

## 10. Architectural Backlog

Deferred concepts. Not canonical entities in v1.0.

| Concept | Why it may become important | Why deferred |
|---|---|---|
| **Goal / Objective** | Needed once AIOS pursues standing, multi-step objectives spanning multiple Capability invocations over time, rather than only responding to point-in-time requests. | Current operation is invocation-scoped. Adding intent-modeling now would describe behavior the system doesn't yet exercise — premature for a minimal model. |
| **Escalation / Incident** | Needed once Agent autonomy increases to the point that "this requires human attention" must be a structural, queryable state. | Today, escalation is adequately handled procedurally via the existing Decision-Making Process plus Trace's success/failure/escalation status field — no dedicated entity required yet. |
| **Steward** | Needed if AIOS is to formally model hybrid human+AI accountability (approvals, reviews, sign-offs) rather than treat human ownership as incidental. | Current governance (architect-approved decisions) already covers accountability without a formal entity. Whether human accountability needs entity-level treatment is still an open question, not yet a demonstrated need. |
| **Cost Management System** | Needed for attributing real compute/vendor spend back to Departments and Capabilities as usage scales. | Trace already reserves a cost/resource metadata field. Sufficient until aggregation or reporting needs demonstrably outgrow a field on Trace. |
| **Knowledge Trust Scoring** | Needed once promotion volume grows large enough that a binary canonical/not-canonical gate becomes either a bottleneck or a quality risk. | Promotion is currently assumed to be a deliberate, low-volume, governed process where binary canonical status is still sufficient. |
| **Autonomous Capability Creation** | Needed only if AIOS moves toward higher autonomy where an Agent may need to propose new Capabilities rather than operate solely within architect-defined ones. | Capability creation is intentionally, not accidentally, restricted to architect-approved decisions under the current governance model. This is a deliberate constraint for the foreseeable future, not a gap. |

---

## 11. Version Declaration

- **Document**: AIOS Canonical Domain Model
- **Version**: v1.0
- **Status**: Canonical. Ratified by the System Architect.
- **Supersedes**: Canonical Domain Model v0 (proposal) and its Architecture
  Review findings, insofar as this document incorporates the three
  accepted changes (Agent Definition/Instance split, Trace/Memory boundary
  resolution, Capability dependency governance) and defers six concepts to
  the Architectural Backlog.
- **Serves as**: the semantic foundation the Engineering Constitution will
  formalize into governance language, and the reference vocabulary for all
  future ADRs, RFCs, and eventual repository architecture.
- **Future changes**: per architect constraint, any modification to this
  model must be proposed through an Architecture Decision Record (ADR).
