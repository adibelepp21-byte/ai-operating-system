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

---

# Part II — the other three regions, and the frozen rules that bind them

**Added 2026-09-06, Cycle 18.** Part I measured `native_core/` only. `§31.11` of
the verification record named `consumers/` and `tools/` as unmeasured. They are
measured here.

## 9. The four top-level regions — measured

**[E] Empirical, 2026-09-06.**

**Basis, stated because Part I used a different one:** files exclude test
modules and `__pycache__`; `__init__.py` is counted (it carries the boundary
docstrings). Lines are raw `wc -l`.

| Region | Files | Lines | With tests | Role (from each region's own source) |
|---|---:|---:|---:|---|
| `native_core/` | 90 | 10,127 | 121 / 20,517 | The eleven frozen subsystem boundaries |
| `tools/` | 25 | 3,075 | 34 / 5,581 | Repository tooling, validators, catalog readers |
| `consumers/` | 9 | 1,691 | 24 / 5,532 | Concrete implementations of Native Core contracts |
| `docs/` | — | — | — | Governance, architecture, and derived corpora |

> **Reconciling with Part I.** `§1` reported **94 modules / 20,408 lines** for
> `native_core`. That counted the **eleven subsystem directories**, excluded
> `__init__.py` from the module count, and **included** tests in the line count.
> The region total here is **20,517** with tests; the 109-line difference is
> `native_core/__init__.py` and `shared/`, which sit outside the eleven
> boundaries. **Both figures are correct for their stated scope**; the bases
> differed, which is why the basis is now stated. Part I's per-subsystem table
> is unchanged and remains the finer measurement.

### `consumers/` — and a correspondence this map declines to draw

`consumers/__init__.py` states the region's purpose: *"concrete implementations
of Native Core contracts must live outside the contract boundaries they
implement"*, authorized by `DEC-P6-042`. Its dependency direction is the point:

> `consumers/` ──depends on──▶ `native_core` (public contracts)
> `native_core/` ──never──▶ `consumers/`
>
> *"The core must never learn that a consumer exists."*

**Two module names invite a false correspondence.**
`cognitive_intelligence_agent.py` and `engineering_intelligence_agent.py` match
two of the **eight Intelligence categories** in `Master Program Volume VI §3`
(Cognitive, Engineering, Mathematical, Quantitative, Scientific, Strategic,
Creative, Language).

**That correspondence is not drawn, and the reason is in the region's own
docstring.** These are *"`ExecutionConsumer` realizations"* — implementations of
a core contract. Nothing establishes them as **Phase 5 Intelligence Ecosystem**
deliverables, and `Master Program Volume II §4.3` records Phase 5 as *"Konsep
selesai, implementasi belum dimulai."*

**Reporting "2 of 8 Intelligence categories implemented" would be exactly the
`E-41` failure**: a name match presented as a claim about what the source says.
The name match is recorded; the status claim is not made.

**One more line from that docstring, which belongs in this corpus:** a consumer
*"owns only its own behaviour. It holds no governance authority, authors no
Trace, and grants itself nothing"* — being handed a bound `Execution` is
***"entry, not authority."*** `Capability ≠ Authority`, written into the
region that receives the capability.

### `tools/` — two different things are called "the governance index"

| | `tools/governance_index.py` | `docs/governance/GOVERNANCE_INDEX.md` |
|---|---|---|
| Kind | Code, 817 lines — a JSON discovery aid | A canonical Markdown index, 110 lines |
| Authorized by | `ACT-CC-P6-066-R2` | `GOVERNANCE_INDEX §9` |
| Maintenance | Regenerated by running it | *"normal Architect approval"* required |
| Bears on | discovery speed | **`B-7`** |

The tool's own header states the discipline this corpus works under, in its own
words:

> `INDEX != AUTHORITY` · `INDEX != CANONICAL SOURCE` ·
> `INDEX != GOVERNANCE DECISION` · `CHRONOLOGY != SUPERSESSION` ·
> `RETRIEVAL != AUTHORIZATION`

and it *"never rewrites a source record, never infers a missing field, and never
derives supersession from dates. A field the source does not state is reported
as `ABSENT` — never filled in."*

## 10. `B-7` quantified

`B-7` has been carried for many cycles as "the Governance Index is stale."
**It is now measured.** The tool reports **358 governance records across 311
sources**. Against that:

| Record class | Exists in repository | Enumerated by `GOVERNANCE_INDEX.md` | Unlisted |
|---|---:|---:|---:|
| GDR entries | **37** (`### GDR-0001`…`GDR-0037`) | **2** (`GDR-0001`, `GDR-0002`) | **35** |
| ADR decisions | **28** files | **9** — stated as the range *"`ADR-0001.md` through `ADR-0009.md`"* | **19** |
| Acts (`docs/governance/acts/`) | **25** files | **0** | **25** |

**The index enumerates a small and precisely-known fraction of the governance
record.**

**No edit is made, and none may be.** `GOVERNANCE_INDEX §9` requires *"normal
Architect approval"*; `ACT-CC-CD1.1:172` records *"Did not: … modify the
Governance Index"* in the Act that created the Architecture Authority
appointment; and `VF-4` is this corpus's one overreach, committed by editing
this exact file and reverted byte-identical. **Architecture Authority ≠
Architect.**

**What changes is the escalation, not the file.** `B-7` now carries exact
figures an Architect can act on without re-deriving them.

### A detector defect, disclosed

The first count of GDR entries returned **0**, because the pattern assumed `##`
headings where the register uses `###`. **A false zero, caught before it was
recorded as a finding.** Corrected count: 37. Disclosed rather than silently
fixed, per the standing rule on defects in this corpus's own verification code.

## 11. The frozen rules that bind the accountability-unit population

`Freeze §6` freezes the *Observed* relationships — **and explicitly does not
freeze inferred ones**: *"Inferred relationships are NOT frozen (§2;
reserved)."* Four rows bear on this corpus:

| Relationship | Allowed | Forbidden | Ownership |
|---|---|---|---|
| **Organization owns Department** | down | — | `Org→Dept` |
| **Department owns Capability** | down | `Dept→other-Dept Capability` | `Dept→Cap` (INV-1) |
| **Capability depends-on Capability** | governed, versioned (INV-9/10) | **silent / cross-Dept ungoverned** | per-Cap |
| **Memory promoted-to Knowledge** | via governed review (INV-8) | automatic | **Knowledge home-Dept** |

**`Freeze §6` direction summary, frozen:** *"authority ↓, execution ↓,
information/knowledge ↑ through the single governed promotion gate (INV-8),
Trace immutable (INV-5)."*

**Two consequences for this corpus.**

**(a) `G-05`'s derived edges are inferred relationships.** `Freeze §6` says
inferred relationships are **not frozen** and are **reserved**. So the five
edges are not merely unapproved under `INV-10` (`E-69`) — the category they
belong to is explicitly reserved. **This strengthens the existing restraint
rather than loosening it.**

**(b) Knowledge has a home Department.** The Memory→Knowledge row assigns
ownership *"Knowledge home-Dept."* That is an ownership statement touching
`PD-04 Knowledge & Intelligence` — **and it is not acted on**, for the same
reason as `§7`: which population supplies the "Dept" is `G-09`, unresolved.

## 12. The five load-bearing walls

`Freeze §8` freezes five boundaries that *"cannot be bypassed by any
implementation"* — *"the load-bearing walls of AIOS. Bypassing any one collapses
a defining guarantee."*

1. **Trace boundary** — every action produces one immutable record,
   unconditionally (INV-4/5).
2. **Knowledge-Promotion boundary** — Knowledge entered only via governed
   review (INV-8); *"no optimization or automation may cross it."*
3. **Human-Authority boundary** — *"automation may request/recommend/detect; it
   may not decide governance or override it"* (`Constitution §6.2 invariant 2`;
   `PR-3`).
4. **Tool boundary** — all external coupling passes through Tool alone (INV-12).
5. **Governance boundary** — *"architectural change and Domain-Model change
   require the governance process (Constitution §3; INV-10); **not delegable
   where the Constitution says non-delegable (§3.2)**."*

**Wall 5 is an independent frozen confirmation of this corpus's central
restraint.** `G-09` is a Domain-Model change. `Freeze §8` states — in ratified,
frozen architecture rather than in a delegation instrument — that such a change
*requires the governance process* and is *not delegable*. The conclusion this
corpus reached from `DEL-T4.4-CF-001 §3.2` exclusion 9 is reached again, from a
different document, by a different route.

**Wall 3 is the rule under which the repository's stop-hook prompt is declined
each turn**, and `Freeze §7` lists it among the twelve Frozen Native Principles
as **4. Human Authority**, beside **9. Detect, Don't Decide**.

## 13. Part II — what is still not constructed

No ownership binding (unchanged from `§7`). No Capability enumerated for any
division. No `G-05` edge upgraded — and `§11(a)` gives a second reason not to.
No Knowledge home-Department assigned. **No edit to `GOVERNANCE_INDEX.md`.** No
Intelligence-category status claim from a consumer module name.
