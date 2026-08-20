# Engineering Specification — Department Subsystem

**Phase:** AIOS 5 — Engineering Specification. Implementation-neutral. **Immutable basis:** Architecture Freeze v1.0. No architecture/entity/class/API/database/protocol/message-format is added.
**Confidence:** **[E]** ratified/frozen · **[A]** engineering abstraction · **[O]** open / Architect reserved.
**Authority:** FOUNDER · `ACT-CC-F03-035` `DEC-DEPT-REALIZATION = AUTHORIZE` (R-1). Realizes the already-ratified Freeze §4 entity; ratifies nothing.

## 1. Purpose
[E] Department is an **accountability unit** that owns Capabilities and Agent Definitions (Freeze §4 Spine; INV-1, INV-2). [A] It is the referent that `DepartmentRef` has stood in for since Phase 3 (`NCIR §62`: Capability was *"built with its ownership context stubbed to governance"*).

## 2. Responsibilities
[E] Be owned by an Organization (Freeze §4). [E] Own Capabilities (INV-1) and Agent Definitions (INV-2). [E] Be accountable. [A] Resolve an ownership reference to exactly one Department.

## 3. Owned Data
[E] Department identity, its Organization parent, the set of Capabilities it owns (Freeze §4; INV-1) and the set of Agent Definitions it owns (Freeze §4; INV-2). [A] Ownership is held as identity references, never as embedded Capability or Agent Definition state — each owned entity's own boundary owns its data. [A] The two ownership sets are distinct namespaces; a key in one says nothing about the other.

## 4. Lifecycle
[E] **Governed** (Freeze §4). [A] This boundary defines no lifecycle *states*; Freeze §4 says "governed" and enumerates none, so none is invented here.

## 5. Public Interfaces (conceptual only)
[A] Conceptually exposes: (a) be identified, (b) name its Organization, (c) own Capabilities, (d) own Agent Definitions, (e) be resolved from an ownership reference. [E] Exposes **no** execution surface and **no** authority to approve its own cross-Department dependencies — approval is a governed decision taken elsewhere (INV-10; PR-3). *(No signatures/formats.)*

## 6. Internal Responsibilities
[A] Maintain identity, the Organization parent edge, the owned-Capability set and the owned-Agent-Definition set. [A] Detect ownership violations; never decide them (PR-3 — Detect, Don't Decide).

## 7. Allowed Dependencies
[E] Depends on its Organization (ownership parent; Freeze §4). [A] May reference Capability identities in order to express ownership — ownership flows downward from owner to owned, which is the Spine direction `Organization → Department → Capability`.

## 8. Forbidden Dependencies
[E] Must not own another Department's Capability (INV-1). [E] Must not permit silent cross-Department dependency (INV-10). [E] Must not execute (Freeze §4 — only Agent Instance acts). [E] Must not hold an external dependency (INV-12). [A] Must not depend on Agent, Skill, Workflow, Runtime, Trace, Memory, Knowledge, Optimization or Infrastructure.

## 9. Trace Requirements
[A] Department is not an actor and authors no Trace (Freeze §4 — Agent Instance is *"the only actor"*). [A] Changes to a Department are governed actions accountable via their governed-decision path.

## 10. Governance Constraints
[E] INV-1 — every Capability is owned by exactly one Department; a Capability resolving to zero or to more than one Department is invalid. [E] INV-2 clause 1 — every Agent Definition is owned by exactly one Department, under the same rule. [O] INV-2 clause 2 — that a Definition *implements at least one Capability* — is Agent construction discipline and is **reserved to the Architect** (`agent_spec §12`/`§13`, Agent Factory); this boundary neither checks nor assumes it. [E] INV-10 — cross-Department Capability dependencies require governance approval, never silent adoption; this boundary **detects**, and never evaluates authority (PR-3). [E] Lifecycle is governed.

## 11. Failure Behaviour
[E] Fail closed (PR-4): a Department without identity is invalid; a Department naming an unknown Organization is invalid; an ownership reference resolving to no known Department is invalid; the same Capability claimed by two Departments is an INV-1 violation and halts; the same Agent Definition claimed by two Departments is an INV-2 violation and halts; a Department claiming the same key twice in either ownership set is invalid. [A] An Agent Definition that no Department claims is **flagged, never raised** (PR-3) — over a partial corpus an absent claim is ordinary incompleteness.

## 12. Extension Points
[A] New Departments and new ownership assignments are the extension mechanism. [O] Department ↔ Skill and Department ↔ Workflow relations are **Inferred** and reserved (`capability_spec §12`).

## 13. Future Evolution
[O] Roles, workforce, budgets, KPIs and Department lifecycle *states* are **not** in Freeze §4 and are reserved to the Architect. **Agent Definition ownership (INV-2 clause 1) — RESOLVED.** Built under `ACT-CC-F03-038` on this surface as `Department.owned_agent_definitions`, held as ratified `agent_definition_key` values so that §8's prohibition on depending on Agent is preserved. [O] What remains reserved is the *other* half of the edge: an Agent Definition declaring its own owning Department, and any validation of a Definition against Capabilities (INV-2 clause 2) — both are Agent construction discipline under `agent_spec §12`/`§13`. Until that exists, ownership is single-sided and the two-sided reconciliation applied to Capabilities under `ACT-CC-F03-037` cannot be performed for Agent Definitions.

## 13A. Implementation Location — RESOLVED
[E] Native Core Blueprint §4 defines the Spine as *"**capability + the ownership context it lives in**"*, and §7 lists this ownership context among the Capability package's **allowed dependencies**: *"its Department; other Capabilities via governed versioned contracts"*. [E] `NCIR §9.6` records the Capability package's dependency as *"Department ownership (**Phase-5 stub**)"* and **[O]** *"Blocked by: Department ownership (Phase 5) for **full realization** — built with a governance stub in Phase 3."*
[E] Blueprint §4 also fixes the core region at *"exactly the eleven frozen subsystem boundaries — no more"*, and §3 admits only **core** and **shared**, with §14 barring **shared** from *"entity ownership"*. **No twelfth boundary is available, and none is needed.**
[A] **Realization location: `native_core/core/capability/ownership.py`** — inside the already-ratified Capability boundary, exactly where Blueprint §4 places the ownership context. `DepartmentRef` was its Phase-3 stub; `OwnershipGraph.resolve` binds the stub to its referent. Determined under `ACT-CC-F03-036` **Outcome A**; see `AIOS_DEPT_LOCATION_ESCALATION_v1.0.md`. **Core boundaries remain eleven.**

## 14. Open Questions
[O] Whether a Department may be nested under another Department — Freeze §4 gives Organization → Department only, so nesting is not established. [O] Department lifecycle *states*.
