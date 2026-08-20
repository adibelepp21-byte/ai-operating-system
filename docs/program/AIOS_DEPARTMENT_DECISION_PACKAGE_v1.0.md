# `DEC-DEPT-REALIZATION` — Department Ownership Realization

> **PROPOSED — NOT CANONICAL.** Ratification and construction authorization are
> Founder/Architecture-reserved (`ACT-CC-F03-033 §1`, `§21`). Nothing here is
> adopted, and no entity is created.

**Prepared under:** FOUNDER · `ACT-CC-F03-033 §11` · **Date:** 2026-08-20
**Supersedes:** `AIOS_DEPARTMENT_ARCHITECTURE_PROPOSAL_v0.1.md` — **which was wrong on its central claim**

---

## 0. Correction to the v0.1 proposal — read this first

`AIOS_DEPARTMENT_ARCHITECTURE_PROPOSAL_v0.1.md`, produced under `ACT-CC-F03-032`,
asserted that **Department is not a ratified entity** and proposed ratifying it.
**That is false.** Exhaustive evidence recovery under `§7` establishes:

> **Architecture Freeze §4 ratifies exactly twelve entities. `Organization` and
> `Department` are the first two of them.**

```
Organization · Department · Capability · Agent Definition · Agent Instance ·
Skill · Workflow · Tool · Runtime · Knowledge · Memory · Trace
```

Freeze §4 Spine, verbatim **[E]**:

> **Organization** — *Def*: hierarchy root. *Responsibility*: **owns Departments**; accountability root. *Ownership*: owns Departments. *Lifecycle*: governed. *Dependencies*: none above it.
>
> **Department** — *Def*: accountability unit. *Responsibility*: **owns Capabilities and Agent Definitions**. *Ownership*: **owned by Organization**. *Forbidden*: owning another Department's Capability (INV-1); silent cross-Department dependency (INV-10). *Lifecycle*: governed.

**How the error arose.** I read `capability_spec §13` — *"Department Architecture
(Phase 5) realizes Organization/Department/Capability ownership as a governed
structure; reserved to the Architect"* — and treated the reservation as covering
the **entity**. It covers the **realization**. I did not then search the Freeze's
own entity list, which would have settled it immediately. The v0.1 file is
retained as provenance and is superseded, not deleted.

**Why this matters to you:** the decision changes from *"ratify a new entity"* —
a Domain-Model-touching architectural act — to *"authorize construction of
already-ratified architecture."* Materially smaller, and a different kind of act.

**Consequently D-1 … D-4 are withdrawn as proposals.** All four are already
ratified:

| v0.1 element | Actual status |
|---|---|
| D-1 identity | **RATIFIED** — Department is Freeze §4 entity #2 |
| D-2 INV-1 ownership relation | **RATIFIED** — *"owns Capabilities and Agent Definitions"* |
| D-3 parent edge to Organization | **RATIFIED** — *"owned by Organization"* / *"owns Departments"* |
| D-4 INV-10 governance locus | **RATIFIED** — *"Forbidden: silent cross-Department dependency (INV-10)"* |

## A. Decision ID

**`DEC-DEPT-REALIZATION`**

## B. Question

**Is the Phase-5 realization of Department ownership authorized — that is, may an
engineering specification and a `native_core` implementation be built for the
already-ratified `Organization` and `Department` entities?**

This is a **construction authorization**, not an entity ratification.

## C. Existing evidence (`§7` classification)

| Evidence | Class |
|---|---|
| Freeze §4 ratifies Organization and Department as 2 of 12 entities, with responsibility, ownership, allowed, forbidden and lifecycle | **EXPLICIT** |
| INV-1 *"Every Capability is owned by exactly one Department"* | **EXPLICIT** |
| INV-10 cross-Department dependency requires governance | **EXPLICIT** |
| `capability_spec §13`: realization *"reserved to the Architect"* | **EXPLICIT** (a reservation) |
| `NCIR §19`: *"the Spine ownership structure (Organization/Department — **reserved to Phase 5**)"* | **EXPLICIT** |
| `NCIR §62`: Capability *"built with its ownership context **stubbed to governance**, not to a full Department structure"* | **EXPLICIT** |
| `NCIR §166`: *"**Blocked by [O]: Department ownership (Phase 5) for full realization** — built with a governance stub in Phase 3"* | **EXPLICIT** |
| `NCIR §311`: *"[O] **Department ownership realization** (INV-1/2), reserved to Phase 5, and its stub form in Stage IV"* | **EXPLICIT** |
| `DepartmentRef` docstring: *"A governance stub per Roadmap §9.6, carrying only the ownership reference INV-1 requires"* | **EXPLICIT** (implementation) |
| No `department_spec` or `organization_spec` among the 11 engineering specs | **NOT ESTABLISHED** |
| No `native_core/core/department/` or `/organization/` | **NOT ESTABLISHED** |

**The reservation is consistent across four independent resident sources and is
about realization, never about the entity.** `DepartmentRef` is not a gap — it is
the stub the architecture explicitly called for.

## D. Affected invariants

**INV-1** — currently satisfiable only by reference: `DepartmentRef` asserts *a*
Department key with no referent to validate against. **INV-10** — enforced
correctly today by key comparison in `CapabilityGraph`, which needs no Department
entity. **INV-2** (Agent Definition owned by exactly one Department) —
`NCIR §311` pairs INV-1 and INV-2 in the same reservation.

**No invariant is violated by the current stub.** Realization would let INV-1 and
INV-2 be validated against a real owner rather than an unverified key.

## E. Proposed minimum surface — **withdrawn and replaced**

Nothing architectural is proposed. What is proposed is a **construction scope**,
bounded by Freeze §4's existing definitions and nothing more:

| # | Scope item | Bounded strictly by |
|---|---|---|
| **R-1** | `department_spec` engineering specification | Freeze §4 Department entry, in the form of the existing 11 specs |
| **R-2** | `organization_spec` engineering specification | Freeze §4 Organization entry |
| **R-3** | `native_core/core/department/` — identity, Organization parent, ownership queries | R-1; mirrors the existing `CapabilityGraph` shape |
| **R-4** | Bind `DepartmentRef` to the realized Department | INV-1 validation against a referent |

**Excluded, and each excluded on evidence:** agents, roles, budgets, KPIs,
Department lifecycle *states* (Freeze says only *"Lifecycle: governed"*),
Department↔Skill/Workflow (**Inferred, reserved** — `capability_spec §12`),
Intelligence, Planner, Scheduler, Orchestrator, any new authority domain.

## F. Alternatives

| # | Option | Assessment |
|---|---|---|
| **1** | **Defer / no change** | Valid and costless today. Capability, Agent Definition and the whole Native Core work correctly on the stub. Phase 5 category instantiation stays blocked |
| **2** | **Authorize R-1 … R-4** (minimum realization) | Discharges the reservation exactly as `NCIR §311` frames it. No entity created, no invariant changed |
| **3** | **Materially expanded** — roles, lifecycle states, workforce, KPIs | Exceeds Freeze §4's definitions; each addition would be a genuine new architectural element requiring its own ratification |
| **4** | **Realize Organization only** | Insufficient — INV-1 binds Capability to *Department*, not Organization |

## G. Impact analysis

**Capability** — no change required. `DepartmentRef` keeps its shape; R-4 adds
validation against a referent. Its completion criterion (INV-1/9/10/11/14) is
unaffected and still met. **Organization** — moves from ratified-but-unrealized
to realized. **Domain Model** — **no change**; Platform Division (historical
alias Department, per `ADR-0010`/`ADR-0011`) already carries *"Owns Capabilities
and Agent Definitions."* **Architecture Freeze** — **no change**; the entity set
stays at twelve. **Native Core** — one new package; no existing subsystem
modified; `Capability ⊥ Governance/Agent/Skill/Workflow/Runtime/Trace/Memory/
Knowledge/Optimization/Infrastructure` isolation preserved, since Department sits
above Capability in the Spine, not beside it. **Phase 5** — unblocks category
instantiation, *if* `DEC-PHASE5-SEMANTICS` also resolves. **Downstream roadmap**
— Phases 6–9 sit behind Phase 5. **Governance** — no new authority, no new
governance semantics; INV-10 enforcement is unchanged.

## H. External research

| Ref | Source | Pattern | AIOS correspondence | Difference | Treatment |
|---|---|---|---|---|---|
| **EXT-04** | Backstage software catalog — system model, well-known relations | `Domain → System → Component`, each **owned by a Group**; `ownedBy` · `partOf` · `dependsOn` · `parent/children` | Singular group ownership ↔ **INV-1** *exactly one* Department; `parent/children` ↔ Organization→Department, already in Freeze §4; `dependsOn` ↔ INV-9/11, already implemented | Backstage is a developer-portal catalog with a YAML descriptor and API; AIOS Department is a constitutionally governed accountability unit under fail-closed invariants | **ADAPT** |

**No new external research was required for this package** — the correction came
entirely from resident evidence. Per `§9`, **ADAPT is an engineering
classification and ADOPT is a governance decision**; no ADOPT is asserted, and no
external schema, naming or code is proposed for import.

## I. Recommendation

### RECOMMENDATION — NOT FOUNDER DECISION

**Option 2 — authorize R-1 … R-4.** Grounds: the entities are already ratified,
so nothing architectural is created; four independent resident sources frame the
reservation as being about realization and place it in Phase 5, which is where
the program now is; the scope is bounded by Freeze §4's existing text; and
`DepartmentRef` was *designed* as a stub awaiting exactly this.

**Contrary consideration, stated fairly:** Option 1 costs nothing today. Nothing
is broken, no invariant is violated, and the Native Core is complete and green
without it. If Phase 5 is not actually the next priority, deferring is the
cheaper and equally defensible choice.

## J. Founder decision block

```
[ ] ADOPT AS PROPOSED      — authorize R-1 … R-4
[ ] ADOPT WITH AMENDMENT   — state which of R-1 … R-4 changes
[ ] REJECT                 — realization not authorized; Phase 5 stays blocked
[ ] DEFER                  — state the condition that would reopen it
```

Decision: `____________________`  Founder: `____________________`  Date: `____________________`

---

## Related but separate

`DEC-PHASE5-SEMANTICS` (Interpretation A vs B) and `OB-01` (the actor exercising
PD-02's authority) are independent of this decision and are not resolved here.
Note that under **either** Phase 5 interpretation, Department realization is
required — so this decision is not contingent on that one.
