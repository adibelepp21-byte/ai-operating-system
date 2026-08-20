# Architecture Escalation — Department Realization Location

> **ARCHITECTURE DECISION REQUIRED** under Engineering Constitution **§3.4**.
> `ACT-CC-F03-035 §13`. No architecture was invented; no boundary was created.

**Raised under:** FOUNDER · `ACT-CC-F03-035` `DEC-DEPT-REALIZATION = AUTHORIZE` · **Date:** 2026-08-20
**Status of R-1/R-2:** **COMPLETE** · **Status of R-3/R-4:** **BLOCKED — location unratified**

---

## 1. What happened

`DEC-DEPT-REALIZATION = AUTHORIZE` authorized R-1…R-4. R-1 and R-2 are complete.
R-3 was implemented at `native_core/core/department/` — 733 lines across models,
ownership graph, R-4 binding and 30 conformance tests, **all passing in
isolation**.

The **full-suite regression then failed**, on a conformance test in the
`optimization` boundary:

> `test_the_core_region_now_holds_the_eleven_frozen_boundaries` — *Items in the second set but not the first: `'department'`*

**The repository's own governance caught it.** The package was removed and the
suite returned to **498 tests OK**. `ACT-CC-F03-035 §5.1` foresaw this: R-3's
location is *"`native_core/core/department/` **or the location evidentially
determined to be the appropriate implementation location**."* The evidence
determines it is **not** that one.

## 2. Why no `native_core` location exists

| Source | Constraint |
|---|---|
| Blueprint **§4** [A] | *"The **core** region contains exactly the eleven frozen subsystem boundaries — **no more (no new entity/subsystem may be introduced)**."* |
| Blueprint **§3** [A] | The root admits a **core** region and a **shared** region, plus three cross-cutting *strategies*. **No third region.** |
| Blueprint **§14** [E] | **shared** holds *"**no** entity ownership"* — Department is an ownership entity, so it cannot go there |
| `GDR` [A] | *"Introducing a twelfth core boundary would exceed 'permitted by existing governance' and **would require a separate architectural decision under Engineering Constitution §3.4**. This authorization neither grants nor withholds that decision; **it records the constraint so it is not crossed inadvertently**."* |
| `NCIR §19` [E] | *"Out of scope, by rule: … the Spine ownership structure (Organization/Department — **reserved to Phase 5**)"* |

A resident governance record **anticipated this exact situation and recorded the
constraint in advance.** Crossing it silently would have been the failure mode it
was written to prevent.

## 3. The decision required

**Where is the already-ratified `Department` entity realized in code?**

### Option 1 — Twelfth core boundary (`native_core/core/department/`)

Requires an **Engineering Constitution §3.4 architectural decision** amending
Blueprint §4's *"exactly eleven … no more"*, plus an update to the structural
conformance test that enforces it. **Implementation already exists** (733 lines,
30 tests, green in isolation) and can be restored immediately on ratification.

*Cost:* amends a canonical structural constraint and reopens a certified,
closed-out Native Core.

### Option 2 — Realize inside the existing `capability` boundary — **no new boundary**

Blueprint §4 **[E]** already locates it: *"Spine (**capability + the ownership
context it lives in**)."* On this reading, `DepartmentRef` is not a placeholder
awaiting a sibling package — it is *the ownership context, in the boundary the
Blueprint assigned it to*. Realization means growing `Organization`/`Department`
models and the ownership graph **inside `core/capability/`**.

*Cost:* enlarges the capability boundary's responsibility. *Benefit:* amends no
canonical constraint, adds no boundary, keeps eleven at eleven, and is the
reading Blueprint §4's own words support.

### Option 3 — New non-core region

Requires amending Blueprint §3's region model. Strictly larger than Option 1 and
not recommended.

### Option 4 — Defer R-3/R-4

R-1 and R-2 stand as documentation of ratified entities. Capability keeps the
stub, which works correctly today. Phase 5 category instantiation stays blocked.

## 4. Recommendation

### RECOMMENDATION — NOT FOUNDER DECISION

**Option 2.** It is the only option that amends nothing canonical, and Blueprint
§4's Spine definition — *"capability + the ownership context it lives in"* —
appears to already answer the question in its favour. Options 1 and 3 both
require reopening a certified Native Core to add structure the Blueprint says
must not grow.

**Contrary consideration, stated fairly:** Option 2 concentrates Organization,
Department and Capability in one package, which is a larger boundary than the
other ten. If boundary symmetry matters more than constraint stability, Option 1
is the cleaner architecture and the §3.4 decision is the honest way to buy it.

## 5. What was preserved (`§13.8`)

R-1 `organization_spec` and R-2 `department_spec` are complete and committed;
`department_spec §13A` records the location as **UNRESOLVED** and points here.
The R-3/R-4 implementation is fully specified by those two specs and was
verified green in isolation; it is reconstructible from them under either
Option 1 or Option 2 without redesign.

**No code from the removed package remains in the tree.** Leaving an unplaceable
boundary in place would itself have been the violation.

## 6. Decision block

```
[ ] OPTION 1 — twelfth core boundary (requires §3.4 decision amending Blueprint §4)
[ ] OPTION 2 — realize inside the capability boundary (no canonical amendment)
[ ] OPTION 3 — new non-core region (requires amending Blueprint §3)
[ ] OPTION 4 — defer R-3/R-4
```

Decision: `____________________`  Founder/Architect: `____________________`  Date: `____________________`
