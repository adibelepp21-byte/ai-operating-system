# Implementation Correspondence Map

> **Status: DERIVED — empirical + frozen-source.** Constructed 2026-09-06,
> Cycle 17, under `ACT-CC-P10-FINAL §14 B`, `§16` and `§17`, on the authority of
> `FDE-P10-AUTONOMOUS-EXECUTION-01` Decision B (`GDR-0037`) and
> `DEL-T4.4-CF-001 §3.1 A/C`.
>
> **This map asserts no ownership binding.** It records what is *implemented*,
> what is *frozen*, and where the two touch. Binding a Platform Division to a
> subsystem is an ownership determination and is **not made here** — see `§7`.

## 0. Why this artifact exists

Every division record in `divisions/` closes with a "Not constructed" section,
and six of them name the same omission: **no binding to `native_core/`**. The
omission was correct — a binding is an ownership claim — but it left the
Platform Organization corpus with **no relationship of any kind** to the running
system, which made the corpus unfalsifiable against the repository.

`ACT-CC-P10-FINAL §16` names **Integration** and **Architecture** as
construction dimensions and directs construction of *"only what the evidence
supports."* This map is that: the correspondence surface, stated as fact, with
the ownership question left explicitly open.

**`§14 B` is what makes this constructible.** The Founder determined that *"an
incomplete Master Program Phase 10 SHALL NOT automatically imply that all
PD-01–PD-10 construction is forbidden."* Cycle 16 established the Phase 10 gate
(`E-60`); `§14 B` establishes that the gate does not reach this surface.

---

## 1. What is actually implemented — measured

**[E] Empirical, `native_core/core/`, measured 2026-09-06.** Eleven subsystem
directories; line counts include tests.

| Subsystem | Modules | Lines | Test modules |
|---|---:|---:|---:|
| `runtime` | 17 | 3,343 | 3 |
| `infrastructure` | 14 | 2,651 | 3 |
| `workflow` | 10 | 2,641 | 2 |
| `capability` | 6 | 2,449 | 2 |
| `knowledge` | 11 | 1,886 | 2 |
| `agent` | 5 | 1,870 | 2 |
| `memory` | 13 | 1,795 | 2 |
| `optimization` | 6 | 1,604 | 1 |
| `skill` | 4 | 821 | 1 |
| `governance` | 4 | 714 | 1 |
| `trace` | 4 | 634 | 1 |
| **Total** | **94** | **20,408** | **20** |

Regression at time of measurement: `native_core` **801 tests OK** (1 expected
failure, `GDR-0014`), `consumers` **276 OK**, `tools` **198 OK**.

## 2. Eleven directories, ten layers — reconciled, not a defect

`AIOS_ARCHITECTURE_FREEZE_v1.0.md §5` freezes **ten** layers:

`1 Governance · 2 Runtime · 3 Agent · 4 Capability · 5 Skill · 6 Workflow ·
7 Memory · 8 Knowledge · 9 Infrastructure · 10 Optimization`

There are **eleven** directories. The difference is `trace`, and `§5` accounts
for it directly: *"Substrate = Knowledge + Memory; **Trace is
cross-cutting/emergent** (Domain Model §3). The layer presentation does not
alter these categories."*

`native_core/core/optimization/__init__.py` states it from the implementation
side — Optimization is *"the **eleventh and last** of the frozen subsystem
boundaries."* **Ten layers plus one cross-cutting boundary = eleven.** The two
counts are consistent and neither is wrong.

## 3. A checked non-defect, disclosed

**Apparent contradiction.** `Freeze §2` lists *"Model-optimization"* among
**deferred** architecture, and `§10 Deferred Architecture (Architect Reserved)`
calls it *"external concern; **not an AIOS entity**."* Yet `native_core/core/optimization/` exists, at 1,604 lines
and layer 10 of the frozen model.

**Not a contradiction — a name collision.** The implemented `optimization`
boundary is the **governed learning loop, detect-only**: it *"observes Trace and
Memory and publishes what it observed; humans decide."* `Model-optimization` is
the tuning of ML models, correctly deferred as an external concern. Two
different referents sharing a word stem.

**Recorded rather than silently dropped**, per the false-positive discipline: a
grep-level hit that content-anchored reading eliminates is evidence about the
detector, not about the repository.

**Worth noting for its own sake:** the `optimization` docstring records that the
boundary *"depends on Governance in no way"* and *"never submits, sends,
notifies, requests, approves, promotes, authorizes, or decides. It publishes; a
consumer may later read."* The direction is deliberately inverted *"so
automation cannot acquire a decision path."* That is `Engineering Constitution
§6.2` invariant 2 — *automation may request, automation may recommend,
automation may not override governance authority* — **implemented in code, at
the level of dependency direction.**

## 4. Name correspondence — Platform Division ↔ implemented boundary

**[E] Lexical correspondence only. This is not ownership.**

| Platform Division | Corresponding boundary | Basis |
|---|---|---|
| `PD-03` Governance & Compliance | `governance` (layer 1) | name |
| `PD-04` Knowledge & Intelligence | `knowledge` (layer 8) | name |
| `PD-05` Runtime & Execution | `runtime` (layer 2) | name |
| `PD-07` Infrastructure & Platform | `infrastructure` (layer 9) | name |

**Four of ten divisions and four of eleven boundaries correspond by name.**

| No corresponding boundary (6 divisions) | No corresponding division (7 boundaries) |
|---|---|
| `PD-01` Executive Office · `PD-02` Architecture Office · `PD-06` AI Engineering · `PD-08` Security · `PD-09` Quality & Evaluation · `PD-10` Developer Experience | `agent` · `capability` · `memory` · `optimization` · `skill` · `trace` · `workflow` |

### What this asymmetry means

**The implemented architecture is not organized along Platform Division lines,
and was never intended to be.** `Freeze §5` organizes by **execution layer**;
the Platform Organization corpus organizes by **accountability unit**. These are
orthogonal decompositions of the same system, not rival ones.

**Consequence [D]:** a division cannot be validated by finding "its" module, and
the absence of a module named for a division is **not** evidence that the
division is unimplemented, ill-founded, or redundant. `PD-08 Security` having no
`security/` boundary says nothing about `PD-08`; security is a cross-cutting
concern in this architecture, as `G-03` already records.

## 5. Where the two decompositions actually join — Layer 4

**This is the structural finding of the cycle.** The join is not a name match.
It is `Freeze §5` **layer 4**, quoted verbatim:

| Layer | Purpose | Inputs | Outputs | Dependencies | Forbidden dependencies |
|---|---|---|---|---|---|
| **4 Capability** | owned ability + composition | **Department ownership** | realized ability | **Organization/Department** | cross-Dept dep without governance (INV-10) |

**The frozen layer model takes `Department` ownership as an input to the
Capability layer and declares `Organization/Department` a dependency of it.**

`Freeze §4` (Frozen Entity Definitions, Spine) states both sides:

> **Department** — *"accountability unit … owns Capabilities and Agent
> Definitions … owned by Organization … **Forbidden**: owning another
> Department's Capability (INV-1); silent cross-Department dependency
> (INV-10)."*

> **Capability** — *"a Department-owned unit of ability … **Ownership**: exactly
> one Department (INV-1) … **Forbidden**: executing itself; cross-Department
> dependency without governance (INV-10); existing with zero implementers as a
> steady state (INV-14)."*

**So the Platform Organization corpus is not decorative relative to
`native_core`.** The frozen architecture depends on there being an
accountability-unit population that owns Capabilities. `E-64` established that
the Master Program's `Department`, the Domain Model's `Platform Division`, and
this term are one entity under `ADR-0010`. **Layer 4 is where the Platform
Organization enters the running system.**

### Why the frozen text still says `Department`

**It is required to.** `ADR-0010` was a *"bounded amendment rather than global
migration"*, changing exactly five locations in one file, and states that
*"nothing else in the repository may change under this ADR."* `Department` is
the **recorded historical alias**. A future reader should **not** "correct" the
Freeze document — doing so would exceed `ADR-0010` and modify a frozen artifact.

## 6. The invariants that govern this join

**[A] `Freeze §3`, quoted verbatim from the ratified Canonical Domain Model §7.**
Five of the fifteen bear directly on the Platform Division population:

| Invariant | Text | Bearing |
|---|---|---|
| **INV-1** | *"Every Capability is owned by exactly one Department."* | No shared or unowned Capability. Any PD corpus asserting joint ownership violates it |
| **INV-2** | *"Every Agent Definition is owned by exactly one Department and implements at least one Capability."* | Agent Definitions attach to the same population |
| **INV-9** | *"Every Capability-to-Capability dependency must be explicit and must reference a specific versioned contract."* | Bears on `G-05` — inter-PD edges must be explicit and versioned, not inferred |
| **INV-10** | *"Cross-Department Capability dependencies require governance approval through the Decision-Making Process — never silent adoption."* | **Directly governs `G-05`.** Every cross-division dependency needs approval |
| **INV-14** | *"An unimplemented capability is an invalid steady state."* | A division may not hold Capabilities that nothing implements |

**`INV-10` materially constrains `G-05`.** `G-05` records five derived inter-PD
dependency edges. Under `INV-10` those edges, if they are Capability
dependencies, **require governance approval and may not be silently adopted**.
This map does not convert them into approved dependencies; it records that the
approval requirement exists and is unmet.

**`INV-14` is a live obligation, not an observation.** If any Platform Division
is recorded as owning a Capability with zero implementers, that is an *invalid
steady state* by frozen invariant. **No division record in this corpus currently
enumerates owned Capabilities**, so no violation exists today — and none can be
introduced casually later.

## 7. What is deliberately not constructed here

**No ownership binding.** This map does not assert that `PD-03` owns
`native_core/core/governance/`, nor any of the other three name
correspondences. Such a binding would:

- assign a Capability/subsystem to an accountability unit, engaging **INV-1**;
- be a **Canonical Domain Model semantic** act, withheld by
  `DEL-T4.4-CF-001 §3.2` **exclusion 9**;
- be a **cross-Division structural** act, withheld by **exclusion 10**;
- and, given `G-09`, presume a resolution of *which* population the entity has —
  six Departments or ten Platform Divisions — that no resident source supplies.

**Name correspondence is evidence toward a binding. It is not the binding.**
`Citation ≠ authority`; here, `correspondence ≠ ownership`.

Also not constructed: no `security/` boundary proposed for `PD-08`; no module
renamed; no `Department`→`Platform Division` migration in frozen text; no
Capability enumerated for any division; no `G-05` edge upgraded to approved.

## 8. What this unblocks, and what it does not

| Item | Before | After |
|---|---|---|
| `divisions/` "no binding to `native_core/`" | omission unexplained in six records | **explained and justified** — `§7` |
| `PD-07 §5` *"binding to the `infrastructure` frozen subsystem"* | UNKNOWN | **name correspondence recorded; binding still open** |
| `G-05` inter-PD edges | five derived edges, status unclear | **`INV-10` identified as the governing rule** — approval required, unmet |
| Corpus ↔ repository relationship | none | **Layer 4 identified as the join point** |
| `G-01` (eight divisions without corpora) | supply-blocked | **unchanged** — this map supplies no division content |
| `ESC-C7-01` (Volume 3/4 residency) | open | **unchanged** |
| `G-09` (six vs ten populations) | open | **unchanged, and now load-bearing** — Layer 4 depends on the population being settled |

**`G-09` is more consequential than Cycle 16 recorded it.** It is not only a
documentation conflict: `Freeze §5` layer 4 takes `Department ownership` as an
input, so the frozen architecture has a dependency on a population that two
canonical sources enumerate differently. Escalation priority raised in
`SYSTEMIC-GAP-MAP.md`.
