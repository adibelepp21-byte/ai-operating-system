# Smallest Viable Architecture Proposal — Department Architecture

> # PROPOSED — NOT CANONICAL
> No architectural entity is created by this document. Ratification is
> Founder/Architecture-reserved (`ACT-CC-F03-032 §4`, `§15.4`, `§18`).

**Prepared under:** FOUNDER · `ACT-CC-F03-032 §12` · **Date:** 2026-08-20
**Trigger:** the authorized Capability construction target cannot be advanced without it

---

## 1. Completed engineering preserved (`§12.1`)

Nothing was rolled back. `native_core/core/capability/` is unchanged and green;
full suite **495 tests OK**. This proposal adds no code.

## 2. The isolated architectural dependency (`§12.2`)

```text
Phase 5 construction  →  instantiate Capability Catalog categories
                      →  every Capability needs an owner (INV-1)
                      →  the owner type is Department
                      →  Department Architecture is [O]-reserved
```

One dependency, one reservation. Everything else in the chain is ratified.

## 3. The exact gap (`§12.3`)

`capability_spec §13`, verbatim:

> **[O]** *Department Architecture (Phase 5) realizes Organization/Department/Capability ownership as a governed structure; **reserved to the Architect**.*

**What already exists:** `INV-1` (*"Every Capability is owned by exactly one
Department"*) is ratified and enforced; `models.py` defines **`DepartmentRef`**;
`CapabilityGraph` implements the dependency and cross-Department query surface
(INV-9/10/11); orphan detection implements INV-14.

**What is missing:** the **Department entity itself** — the thing `DepartmentRef`
refers to — and the Organization tree above it. AIOS currently has the *reference*
without the *referent*.

## 4. Smallest viable proposal (`§12.4`)

Ratify **Department** as a canonical entity with the minimum structure INV-1
already presupposes, and nothing more:

| Element | Content | Why minimal |
|---|---|---|
| **D-1 Identity** | A Department has a stable, unique key | `DepartmentRef` already carries exactly this; ratification names the referent |
| **D-2 Ownership relation** | A Department owns 0..n Capabilities; a Capability is owned by exactly one Department | Restates ratified **INV-1**; adds nothing |
| **D-3 Parent** | A Department belongs to exactly one Organization | The minimum needed for `Organization/Department/Capability` as `§13` words it |
| **D-4 Governance locus** | Cross-Department dependency approval attaches to the Department | Restates ratified **INV-10**; `GovernanceRecord` already models the record |

**Deliberately excluded** — none is required to unblock Capability, and each
would enlarge the frozen entity set: Department-level agents or workforce; roles;
budgets; KPIs; lifecycle states; Department↔Skill/Workflow relations
(**Inferred, reserved** — `capability_spec §12`); any Intelligence entity.

**D-1 … D-4 are restatements of already-ratified invariants plus one parent
edge.** That is the smallest change that makes INV-1 satisfiable in practice.

## 5. Affected artifacts (`§12.5`)

Canonical Domain Model (entity set + Spine) · Architecture Freeze §4 (twelve →
thirteen ratified entities) · `capability_spec §13` (reservation discharged) ·
`NCIR §2` (Spine reserved-to-Phase-5 note) · a new `department_spec` ·
potentially a new `native_core/core/department/`.

## 6. Dependency impact (`§12.6`)

`Capability → Department` already exists in code as `DepartmentRef` and in
architecture as INV-1. Ratification introduces **no new dependency direction**
and **no cycle**: Department would depend on Organization only. The existing
`Capability ⊥ Governance/Agent/Skill/Workflow/Runtime/Trace/Memory/Knowledge/
Optimization/Infrastructure` isolation, asserted by the Capability conformance
tests, is unaffected.

## 7. Implementation impact (`§12.7`)

Small. `DepartmentRef` needs no change. A `department` package would carry
identity, the parent edge, and ownership queries — the mirror of what
`CapabilityGraph` already does. **No change to any existing subsystem is implied.**

## 8. Alternatives (`§12.8`)

| # | Alternative | Assessment |
|---|---|---|
| A | **Ratify Department (this proposal)** | Smallest change that discharges the `§13` reservation |
| B | Treat `DepartmentRef` as sufficient — no entity | Leaves INV-1 referring to an unratified type; ownership stays unverifiable. Rejected on evidence |
| C | Ratify the full Organization/Department/Role/Workforce structure | Far larger than needed; contradicts *smallest viable* |
| D | Ratify **Intelligence** as an entity instead | Does not discharge the reservation — an Intelligence entity would still need a Department owner under INV-1 |

## 9. External evidence (`§12.9`, `§6`, `§11`)

| Ref | Source | Pattern | AIOS comparison | Classification |
|---|---|---|---|---|
| **EXT-04** | Backstage Software Catalog — system model, well-known relations | `Domain → System → Component`, each **owned by a Group**; relations `ownedBy` · `partOf` · `dependsOn` · `parent/children`. *"The owner … is the **singular** entity that bears ultimate responsibility"*; *"ownership should usually point to a **group** instead of an individual because teams are more stable than people"* | Singular ownership ↔ **INV-1** (*exactly one* Department) — same principle, independently arrived at. `dependsOn` ↔ INV-9/11, **already implemented** in `CapabilityGraph`. `parent/children` ↔ the D-3 parent edge. The group-not-individual rule also bears on **`OB-01`** | **ADAPT** |

**ADAPT, not ADOPT:** Backstage is a developer-portal catalog; AIOS Capability is
a constitutionally governed entity under fail-closed invariants. The *ownership
and hierarchy shape* transfers; the descriptor format, YAML schema and API do
not. **No external code, schema or naming is proposed for import.** Per `§22`,
AIOS remains the design authority and this is evidence only.

## 10. The exact decision required (`§12.10`)

**Ratify `Department` as a canonical AIOS entity with D-1 … D-4, and nothing
more?**

- **YES** → the `capability_spec §13` reservation is discharged; Capability category instantiation becomes constructible; Phase 5 opens.
- **NO** → Phase 5 remains blocked, and the block is a deliberate architectural position rather than an unexamined gap.
- **MODIFY** → state which of D-1 … D-4 to change.

Related but **separate**: `DEC-PHASE5-SEMANTICS` (Interpretation A vs B) and
`OB-01` (the actor exercising PD-02's authority). This proposal decides neither
and does not depend on either.

---

**PROPOSED — NOT CANONICAL. No entity created. No implementation written.**
