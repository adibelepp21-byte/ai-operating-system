# P11 Architect Decision Packages — DP-03 and DP-04

> **Executed under `ACT-CC-P11-002`** — 2026-09-10.
> **`DP-04 = ISSUED` · `DP-03 = ISSUED` — Architect, both 2026-09-10.**
> **The P11 architectural frontier is closed. `P11 AUTHORIZATION` remains NOT
> GRANTED** — `DP-03 §0.1`.
>
> ~~`DP-03 = DECISION-PENDING`, materially narrowed.~~
> ~~`DP-03 = DECISION-PENDING` · `DP-04 = DECISION-PENDING`.~~
> Every recommendation below is labelled **`CO-FOUNDER RECOMMENDATION — NOT
> ARCHITECT DECISION`**, as `§12`/`§22` require. **No decision was taken, no
> subsystem created, no entity created, nothing built** (`§4`, `§28`).

---

## Both decisions ISSUED — the architectural frontier is closed

| Decision | Status | Outcome |
|---|---|---|
| **`DP-04`** | **ISSUED** 2026-09-10 | Option C — organizational-layer representation outside the frozen Native Core |
| **`DP-03`** | **ISSUED** 2026-09-10 | `W1`→Workflow (confirmed) · `W2`→organizational Planning surface, **mutable lifecycle** · `W3`→governed organizational record/relation · `W6`→Optimization, **detect-only** · **Native Core #12 = NOT CREATED** |

**Everything in this document below the banner is superseded where it differs.**
It is retained as the record of the preparation that preceded issuance.

### Both objections I raised were answered, not waved through

**The falsification that survived against my own recommendation** —
that a Delegation record fits the P10 pattern **but a mutable Plan does not** —
is accepted verbatim at `DP-03 §13`: *"The Architect accepts this objection as
valid."* `§8.4` resolves it by separating **persisted representation** from
**lifecycle**: `organizational record ≠ static immutable Plan`, with
`PLAN → SEQUENCE → ADAPT → REVISE` required.

**The prioritization boundary I flagged** — that `W6` is safely home in
`optimization` only while detect-only, while `W2` needs *prioritization*, which
that boundary reserves — is closed at `DP-03 §7`: *"Performance evidence may
inform Planning but does not become Planning authority."*

**My `Option C` recommendation was adopted for Delegation and deliberately not
for Planning.** That is the correct outcome: I had recommended it for both and
then reported evidence weakening it for one. **The decision followed the evidence
rather than the recommendation.**

---

## DP-04 ISSUED — what it decided, and what it leaves for DP-03

**`DP-04` is issued** (`§14` OPTION C · `§21` 2026-09-10 · `§22` signed · `§23`
`ISSUED`), persisted at
[`DP-04-P11-ORGANIZATIONAL-ENTITY-MODEL.md`](DP-04-P11-ORGANIZATIONAL-ENTITY-MODEL.md).
**It is authoritative input to DP-03** (`DP-04 §17`, `§25`), and **DP-04 is not
reopened here.**

### It answers most of DP-03's question

`DP-04 §14` selects **organizational-layer representation outside the frozen
Native Core**, and the concept-level decisions place the homes directly:

| DP-03 capability | What `DP-04` already settles | Residual DP-03 question |
|---|---|---|
| **`W2` Planning** | `§8.2` — *"Plan shall exist in the organizational layer **outside the frozen Native Core**"* | **which** surface, and its interface to the eleven |
| **`W3` Delegation** | `§8.3` — *"a governed organizational relation/record **outside the frozen Native Core**"*, with the record shape given | same, plus how it reads authority without becoming Governance |
| **`W6` Performance** | `§7` — *"represented through the existing performance/observation mechanism rather than requiring a new Native Core entity"* | **confirm** the detect-only constraint on that mechanism |
| **`W1` Coordination** | not addressed — and it needs no decision: `INV-13` **forces** it into `workflow` | **none** |

**My `Option A` recommendation is superseded by an Architect choice that reaches
the same placement by its own reasoning** — `DP-04 §11` rejects Option D
explicitly: *"Although Delegation demonstrates genuine semantic requirements,
those requirements do not justify modification of the frozen Native Core."*

### The contradiction I reported is resolved

I reported that `NO-NEW-ENTITY` and semantic correctness **genuinely conflict**
for `Delegation`, and that this was the strongest case for a new entity — which I
was forbidden to select. **`DP-04 §15` resolves it with a third position I had not
identified:**

> *"NOT COLLAPSED INTO EXISTING CORE ENTITY **AND** NOT ELEVATED INTO NEW CORE
> SUBSYSTEM **BUT** REPRESENTED AS A GOVERNED ORGANIZATIONAL CONCEPT/RELATION
> OUTSIDE THE FROZEN CORE."*

**I had framed the choice as collapse-or-elevate and found both wrong.** The
Architect's answer is that the dichotomy was false: the organizational layer can
carry the semantics without either. **That is the decision doing what `§1.1` said
it must — not merely approving what I proposed.**

### DP-03 as it now stands

> **Remaining question:** *Which organizational-layer surface outside the Native
> Core hosts Planning and Delegation, what is its interface to the eleven frozen
> boundaries, and is `W6` confirmed to the existing observation mechanism under a
> strict detect-only constraint?*

**Narrower than the original DP-03 question**, which asked *whether* a twelfth
boundary was needed. `DP-04 §9` closes that: *"This decision does NOT create …
Native Core subsystem #12."*

**`DP-03` remains a separate Architect Decision** (`DP-04 §25`) and is **not
decided here**. The material below is preserved as the record of the analysis that
preceded issuance; **where it differs from `DP-04`, `DP-04` governs.**

---

## Executive result

**Both frontiers were attacked before being packaged, and both narrowed
substantially.** My own `ACT-CC-P11-001` finding — that `P11-W2`/`W3`/`W6` have
*"no frozen subsystem home"* — **was too strong and is corrected here**:

| Capability | Prior claim | Found |
|---|---|---|
| `W1` Coordination | had a home | **Not merely available — `INV-13` *forces* it into `workflow`** |
| `W6` Performance | "no home" | **`optimization` is a strong candidate**; *"improvement opportunities"* is literally its purpose |
| `W3` Delegation | "no home" | **Split** — authority semantics belong to `governance`; the spanning role cannot live there |
| `W2` Planning | "no home" | **Survives** — and `prioritization model` is already **Architect-Reserved inside `optimization`** |

**DP-03 answer type: `DP03-D` — MULTI-HOME / DISTRIBUTED RESPONSIBILITY.**
**The three capabilities do not share one home**, which `§10.10` asked directly.

**DP-04:** of 16 conceptual entities, **3 are frozen, 3 map onto artifacts that
already exist and are implemented**, 4 are relationships or layers rather than
entities, and **4 sit on explicitly reserved concepts**. **Option D — new entity —
is not required by evidence for most of the model.**

---

# PART I — DP-03

## 1. The question (`§7`)

> **Where is the legitimate architectural home for `P11-W2` Organizational
> Planning, `P11-W3` Delegation, and `P11-W6` Organizational Performance?**

## 2. Canonical constraints, verified at source (`§2`)

| Constraint | Verbatim | Where |
|---|---|---|
| Core is closed | *"The core region contains exactly the eleven frozen subsystem boundaries — no more (**no new entity/subsystem may be introduced**)"* | Native Core Blueprint `§4` |
| A twelfth needs authority | *"Introducing a twelfth core boundary … would require a separate architectural decision under Engineering Constitution §3.4"* | Register `:760` |
| Ten frozen layers | Governance · Runtime · Agent · Capability · Skill · Workflow · Memory · Knowledge · Infrastructure · Optimization | `Freeze §5` |
| **No organizational layer exists** | Layer 4 Capability takes *"Department ownership"* as **input**; its dependency is *"Organization/Department"* | `Freeze §5` |

**The organizational context is not a layer — it is the ownership context above
layer 4.** That is why `Organization` and `Department` are implemented in
**`native_core/core/capability/ownership.py`**, verified by locating the classes.

## 3. `§10` prove-me-wrong — ten attacks, four landed

| # | Attack | Result |
|---|---|---|
| 1 | An existing subsystem already owns **planning** | **PARTIAL HIT.** `optimization` reserves *"**prioritization model** · decision heuristics · ranking model"* to the Architect — unimplemented. Planning *proper* has no owner |
| 2 | An existing subsystem owns **delegation** | **PARTIAL HIT.** `governance` *"holds authority over decisions"*, is *"never overridable by automation"*, decides *"nothing automatically"* (`PR-3`) and *"fails closed"* (`PR-4`) — the exact discipline `W3` needs |
| 3 | An existing subsystem owns **organizational performance** | **HIT.** `optimization` is the *"governed learning loop, detect-only"*, observing Trace and Memory and publishing. `W6`'s *"improvement opportunities"* **is** its purpose |
| 4 | A canonical artifact already provides an organizational home | **HIT.** `capability/ownership.py` holds `Organization`, `Department`, `OwnershipGraph` — organizational structure is **already inside a frozen boundary** |
| 5 | A prior Architect Decision resolved this | **MISS.** `ADE-P10-G04` decides Department↔PD identity, not subsystem placement |
| 6 | A P10 pattern is inheritable | **HIT.** `tools/organization_catalog.py` sits **outside** the core by explicit reasoning: *"Native Core Blueprint §4 fixes the core region at 'exactly the eleven … no more'. A loader that reads documentation is not one of them."* **Option A already has working precedent** |
| 7 | Organizational intelligence is an **orchestration layer**, not a subsystem | **STRONG.** `INV-13` makes `Workflow` *"the SOLE sanctioned multi-agent channel"*. Cross-department coordination **must** flow through Workflow or violate an invariant |
| 8 | P11 can live as an external surface without contradiction | **SUPPORTED** by attack 6 |
| 9 | P12 actually owns it | **PARTIAL.** `P12-W2` owns *Unified Operational State* — system-wide. **Organization-level state is not system-wide state**; the boundary holds |
| 10 | Do the three share one home? | **NO — they differ.** This is the finding |

**Four attacks landed against my own prior claim. The frontier is real but
narrower than I reported.**

## 4. `P11-DP03-ARCHITECTURAL-HOME-REGISTER` (`§29`)

| Capability | Current home | Candidate home | Evidence | Constraint | Authority |
|---|---|---|---|---|---|
| **W1** Coordination | `workflow` | **`workflow` — forced** | `INV-13` sole channel | Anything else **violates `INV-13`** | **none needed** |
| **W6** Performance | none | **`optimization`** | detect-only loop; `ObservationPublication` exists in `optimization/contract.py` | Must stay *"proposals only"*; may not decide (`PR-3`) | **none needed if detect-only** |
| **W3** Delegation | none | **split** — `governance` (authority) + `capability/ownership` (who may own) | governance layer 1 | `governance` *"imports nothing from … Workflow, Agent, Runtime, or Optimization"* — **it cannot span** | **ARCHITECT** |
| **W2** Planning | none | **outside core**, or reserved-in-`optimization` | `prioritization model` Architect-Reserved | Planner/Scheduler **withheld** by `FD-P9-002 §8` | **ARCHITECT** |

## 5. Option matrix (`§9`)

| Dimension | **A — Outside core** | **B — Existing boundary** | **C — New subsystem** |
|---|---|---|---|
| Architectural compliance | **PROVEN** compliant | **PROVEN** for W1/W6; **INFERRED** for W3/W2 | **PROVEN** non-compliant as-is |
| Native Core Freeze | **PROVEN** — adds no boundary | **PROVEN** — adds none | **PROVEN conflict** — `§4` *"no more"* |
| Semantic fit | **INFERRED** — organizational ≠ core concern | **PROVEN** W1 (`INV-13`), W6 (detect-only); **weak** W2 | **INFERRED** clean fit |
| Ownership clarity | **PROVEN** — P10 precedent | **UNKNOWN** for W3 — governance isolation blocks spanning | **INFERRED** clear |
| Authority impact | **PROVEN none** | **none** for W1/W6; **ARCHITECT** if W3 changes governance semantics | **ARCHITECT + possible Freeze amendment** |
| Dependency impact | low — reads records | **W1/W6 zero** — mechanisms exist | high — new edges into ten frozen layers |
| Runtime impact | outside runtime path | W1 already runtime; W6 detect-only | new runtime surface |
| Evidence / Verification | **PROVEN** — P10 pattern: 294 tool tests, negative controls | **PROVEN** — existing conformance suites extend | new suites required |
| P10 compatibility | **PROVEN** — identical shape | **PROVEN** | **UNKNOWN** |
| P12 compatibility | **INFERRED** ok | **INFERRED** ok | **UNKNOWN** — may pre-empt `P12-W2` |
| **Reversibility** | **HIGH** — delete the surface | **MEDIUM** — semantics changes are sticky | **LOW** — amends a frozen baseline |
| Complexity / Coupling | low / low | low / **rising for W3** | high / high |
| Governance risk | **low** | **medium** — a new subsystem under an old name | **high** |
| Future evolution | may need migration later | constrained by host semantics | most room |

## 6. `§8` Option B's critical test, answered

> *"Is 'fit inside existing boundary' genuinely reuse, or the creation of a new
> subsystem semantically under an old name?"*

| | Verdict |
|---|---|
| **W1 → `workflow`** | **GENUINE REUSE.** `INV-13` already names Workflow the sole multi-agent channel. Coordination is what it is *for* |
| **W6 → `optimization`** | **GENUINE REUSE** *if detect-only.* `ObservationPublication` exists. **It becomes a new subsystem in disguise the moment it ranks, scores or decides** — which optimization reserves to the Architect and `PR-3` forbids |
| **W3 → `governance`** | **NOT REUSE.** Governance is deliberately isolated and *"imports nothing from Workflow, Agent, Runtime, or Optimization."* Delegation must span exactly those. **Placing it there would be a new subsystem under an old name** |
| **W2 → any** | **NOT REUSE.** No boundary claims planning |

## 7. `§11` Decision type

> **`DP03-D` — MULTI-HOME / DISTRIBUTED RESPONSIBILITY**, with **`DP03-F`** for
> the W2/W3 residue: the Architect must choose their home.

## 8. Recommendation

> ### CO-FOUNDER RECOMMENDATION — **NOT ARCHITECT DECISION**

**W1 → `workflow`** (forced by `INV-13`) · **W6 → `optimization`, detect-only**
(reuse, no authority needed) · **W2 + W3 → Option A, outside the core**, on the
P10 precedent.

**Why A over C for the residue.** Option A has **working precedent**
(`tools/organization_catalog.py`), **needs no new authority**, and is **highly
reversible**. Option C amends a frozen baseline and is the least reversible thing
in this programme. **Reversibility should dominate while `E11` is unratified and
P11 unbuilt** — the shape may still change.

**Why not B for W3.** Governance's isolation is not incidental; it is what keeps
authority un-automatable (`Constitution §6.2` inv. 2). **Widening it to let
delegation span subsystems would weaken the boundary that `P11-W7` depends on.**

**Risks of the recommendation, stated:** an outside-core home may need migration
if P12 later unifies state; and W1/W6 reuse is only safe while W6 stays
detect-only — **the moment it prioritizes, it re-enters Architect-reserved
ground.**

## 9. Exact Architect decision required

> **Do `P11-W2` Planning and `P11-W3` Delegation take (A) a home outside the
> Native Core on the P10 precedent, (B) placement inside existing frozen
> boundaries with the semantic consequences that implies, or (C) a twelfth core
> subsystem via `Constitution §3.4`? And is `W6` confirmed to `optimization`
> under a strict detect-only constraint?**

**Artifacts affected after decision:** P11 construction layout · `optimization`
contract if W6 is confirmed · `governance` isolation if B is chosen for W3 ·
Native Core Blueprint `§4` if C · `DP-01` construction scope.

---

# PART II — DP-04

## 10. The question (`§13`)

> **How must the 16 conceptual entities of Blueprint `§15` be treated against the
> 12 frozen entities, the reserved concepts, "No new entity", and `P12` Unified
> Operational State?**

## 11. `P11-DP04-ENTITY-MODEL-REGISTER` (`§15`, `§29`)

| # | Blueprint `§15` | Frozen counterpart | Reserved counterpart | Existing artifact | Classification |
|---|---|---|---|---|---|
| 1 | `Organization` | **Organization** | — | `capability/ownership.py` | **E-FROZEN** |
| 2 | `OrganizationGoal` | — | **`Goal`** | — | **E-REQUIRES-ARCHITECT-DECISION** |
| 3 | `Plan` | — | — | — | **E-REQUIRES-ARCHITECT-DECISION** |
| 4 | `PlanStep` | — | — | — | **E-REQUIRES-ARCHITECT-DECISION** |
| 5 | `WorkItem` | — | **`Task`** | `WorkEntry` — **explicitly not an entity** | **E-REQUIRES-ARCHITECT-DECISION** |
| 6 | `Department` | **Department** | — | `capability/ownership.py` | **E-FROZEN** |
| 7 | `Capability` | **Capability** | — | `capability/` | **E-FROZEN** |
| 8 | `Dependency` | — | — | `INV-9`/`INV-10` govern it | **E-NOT-AN-ENTITY** — a relationship |
| 9 | `Delegation` | — | — | — | **E-REQUIRES-ARCHITECT-DECISION** |
| 10 | `Execution` | — | — | `Freeze §5` layer 2 | **E-NOT-AN-ENTITY** — a layer |
| 11 | `Observation` | — | `Event` | **`ObservationPublication`** in `optimization/contract.py` | **E-EXISTING** |
| 12 | `Verification` | — | — | verification is an activity | **E-NOT-AN-ENTITY** |
| 13 | `Escalation` | — | — | **`Trace.VALID_STATUSES` includes `"escalation"`** | **E-EXISTING** |
| 14 | `Evidence` | — | `Artifact` | evidence records | **E-PROJECTION** |
| 15 | `OrganizationalState` | — | **`State-as-entity`** | — | **E-REQUIRES-ARCHITECT-DECISION** |
| 16 | `PerformanceRecord` | — | — | **`ObservationPublication`** | **E-EXISTING** |

**Tally: 3 frozen · 3 existing · 1 projection · 3 not-an-entity · 6 requiring an
Architect decision.**

**The three `E-EXISTING` findings are the most useful, and each is verified at
source:**

- **`Escalation` is already a ratified Trace outcome** — `trace/record.py`:
  `VALID_STATUSES = frozenset({"success", "failure", "escalation"})`, annotated
  *"Domain Model §2.1"*. **P11 need not create it.**
- **`Observation` and `PerformanceRecord`** both map to `ObservationPublication`,
  which is implemented with a `PassiveObservationPublication` realization.

## 12. `§16` Reserved-concept test — four candidates

| | `OrganizationGoal`→`Goal` | `WorkItem`→`Task` | `OrganizationalState`→`State-as-entity` | `Observation`→`Event` |
|---|---|---|---|---|
| Counterpart frozen? | **No — reserved** | **No — reserved** | **No — reserved** | **No — reserved** |
| Counterpart an entity? | **No** — *"no ratified entity"* | **No** | **No** | **No** |
| Same semantic identity? | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | **NO** — Observation maps to an existing *publication*, not to Event |
| New representation, or new usage? | **UNKNOWN** | **usage** — `WorkEntry` resolves without an entity | **UNKNOWN** | **usage** — publication exists |
| Creates a new entity substantively? | **likely** | **no** | **likely** | **no** |

**`§16`'s instruction is honoured: where it cannot be proven, it is
`UNKNOWN / REQUIRES ARCHITECT DECISION`, and no mapping was forced.**

**Reserved ≠ forbidden-forever.** `Freeze §2` says these have *no ratified
entity*; ratifying one is an Architect act under `Constitution §3.4`, not an
impossibility.

## 13. `§17` No-new-entity hard test

> **Can P11 meet the organizational need without introducing a new entity?**

| Concept | Disposition |
|---|---|
| Organization · Department · Capability | **existing entity** |
| Coordination | **existing entity + relation** — Workflow, `INV-13` |
| Escalation | **existing entity + state** — Trace status |
| Observation · Performance | **existing artifact** — `ObservationPublication` |
| Accountability | **derived projection** — reconstructable from Trace (`INV-4`/`INV-5` immutable) |
| Work | **derived** — `WorkEntry` proves resolution without an entity |
| Dependency | **existing relation** — `INV-9`/`INV-10` |
| Evidence | **derived projection** |
| **Goal · Plan · Delegation · State** | **UNKNOWN / new entity — the residue** |
| Unified system state | **P12 concern** |

> **Answer: mostly yes — and not entirely.** Twelve of sixteen resolve to
> existing entities, relations, states, or projections. **Four do not**, and they
> are precisely `W2`/`W3`'s subject matter — which is why **DP-04's residue is
> the same residue as DP-03's**.

**`§17`'s prohibition is respected: nothing was re-categorized merely to comply
with "No new entity."** The four are left as unresolved rather than dissolved
into projections they do not obviously fit.

## 14. `§18` P12 boundary test

| Item | Class |
|---|---|
| Organizational goals, plans, delegation, coordination, org-level continuity | **P11** |
| Accountability reconstruction | **P11** |
| `OrganizationalState` as **organization-scoped** state | **P11 — if ratified** |
| `OrganizationalState` as **system-wide** state | **P12** — `P12-W2` *Unified Operational State* |
| System self-model | **P12** — `P12-W5` |
| Cross-layer integration state | **P12** |

**The line: scope, not concept.** Organization-level state is P11; the same
mechanism widened to P4–P11 is P12. **The DP-04 decision should say which scope
it ratifies**, or the boundary erodes silently.

## 15. `§19` prove-me-wrong — nine attacks, four landed

| # | Attack | Result |
|---|---|---|
| 1 | A frozen entity already satisfies a requirement | **HIT ×3** — Organization, Department, Capability |
| 2 | A prior ADR/ADE already fixed the model | **MISS** |
| 3 | A P10 entity model is inheritable | **HIT** — `WorkEntry`: *"This is not a Work entity … a resolution result, recomputed on every call"* |
| 4 | P12 canonically owns the concern | **PARTIAL** — for system-wide state only |
| 5 | An existing runtime object represents the concept | **HIT ×2** — `ObservationPublication`, Trace `escalation` status |
| 6 | Existing event/state representation | **HIT** — `WorkflowState`, 5 states |
| 7 | Some "entities" are projections/records | **HIT** — `Evidence`, `Verification`, `Dependency`, `Execution` |
| 8 | Some belong to documentation, not runtime | **PARTIAL** — `Plan`/`PlanStep` may be documentation artifacts |
| 9 | The list is conceptual, not a schema | **HIT** — `§15` says *"conceptual entities"*, *"where applicable"* |

**Attack 9 matters most: the Blueprint never claimed `§15` was a schema.**
Treating it as sixteen entity-creation requests would have manufactured a
conflict the Blueprint did not raise.

## 16. Option matrix (`§21`)

| Dimension | **A — Reuse frozen** | **B — Derived model** | **C — Extend semantics** | **D — New entity** |
|---|---|---|---|---|
| Freeze compliance | **PROVEN** | **PROVEN** | **INFERRED** | **PROVEN conflict** |
| Semantic integrity | high | high | **at risk** — attributes drift into entities | clean |
| **P11 sufficiency** | **insufficient alone** — 4 residual | **sufficient for 12/16** | possibly sufficient | sufficient |
| P12 compatibility | high | high | medium | **UNKNOWN** |
| Runtime impact | none | low — projections | medium | high |
| Ownership / Authority | clear / none | clear / none | **ambiguous** / Architect | clear / **Architect + Freeze** |
| Evidence / Verification | existing suites | extend | extend | new |
| Migration / Reversibility | none / n/a | low / **high** | medium / medium | high / **low** |
| Governance risk | low | low | **medium** | **high** |
| Future evolution | constrained | flexible | medium | most room |

## 17. Recommendation

> ### CO-FOUNDER RECOMMENDATION — **NOT ARCHITECT DECISION**

**A + B combined for the twelve; the four residual left to the Architect.**

Reuse frozen entities where they exist (3), use the artifacts that already exist
(3), express relations, layers and activities as what they are rather than as
entities (4), and derive accountability and evidence as projections over Trace
(2). **That covers twelve of sixteen with no new entity and no Freeze conflict.**

**For `Goal`, `Plan`, `Delegation`, `OrganizationalState` I make no
recommendation.** Each sits on a reserved concept or has no counterpart, and
`§20` forbids me from selecting Option D. **Their resolution is the Architect's,
and it is the same residue DP-03 leaves.**

## 18. Exact Architect decision required

> **For each of `Goal`, `Plan`/`PlanStep`, `Delegation`, and
> `OrganizationalState`: is it (A) satisfied by an existing entity or relation,
> (B) a derived projection requiring no entity, (C) an extension of an existing
> entity's semantics, or (D) a ratified new entity amending `Freeze §4`? And if
> `OrganizationalState` is ratified, is its scope organization-level (P11) or
> system-wide (P12)?**

---

# PART III — CROSS-DECISION

## 19. `§23` DP-03 ↔ DP-04 dependency

> ## **`DP-04 → DP-03`** — the entity model should be decided **first**.

**Not chosen for convenience — argued from evidence.** The residues are
**identical**: DP-03's homeless capabilities are `W2` Planning and `W3`
Delegation; DP-04's unresolved entities are `Goal`, `Plan`, `Delegation`,
`OrganizationalState` — **the subject matter of exactly those two.**

**The direction follows.** If `Delegation` resolves to a **projection** (DP-04 B),
`W3` needs no home of its own and DP-03's residue shrinks to `W2` alone. If it
resolves to a **ratified entity** (D), it needs an owning boundary and DP-03's
question sharpens. **The entity answer changes the home question; the home answer
does not change what the entities are.**

**Deciding DP-03 first risks choosing a home for something that turns out not to
exist.**

## 20. `§24` Construction impact map — **mapping only, nothing changed**

```text
DP-04 DECISION
  → entity model (4 residual)  → relationships (Trace/Workflow/ownership projections)
  → runtime representation     → P11-W2/W3 scope        → P12 boundary (state scope)
  → verification (new negative controls if any entity is ratified)

DP-03 DECISION
  → architecture (in-core vs outside)  → P11-W2/W3/W6 layout
  → runtime surfaces (optimization contract if W6 confirmed)
  → interfaces (governance isolation if B chosen for W3)
  → verification (which suite owns the new tests)
```

## 21. `§25` Founder package dependency

| Package | Affected? |
|---|---|
| **`DP-01`** P11 construction authorization | **YES — materially.** Construction *scope* differs between "outside core" and "twelfth subsystem". **`DP-01` should not be treated as final until DP-03/DP-04 are decided** |
| **`DP-02`** `E11` ratification | **YES — partially.** `E11-02` Delegation and `E11-05` Observation are measured differently depending on whether Delegation is an entity or a projection |

**`§25`'s condition is met and reported: the architectural decisions do change the
construction definition materially, so the two Founder packages are not final.**

## 22. `§26` No silent Blueprint mutation

**The Blueprint was not modified.** One conflict identified and left for the
Architect: `§15`'s sixteen "conceptual entities" include four sitting on reserved
concepts. **`§15` itself says *"conceptual"* and *"where applicable"*, so this is a
boundary to record, not a defect to correct** — and correcting it is not mine
regardless.

---

## `§32` Required negative assertions

```text
P11 CONSTRUCTION              = NOT AUTHORIZED
P11 ACTIVATION                = NOT AUTHORIZED
E11 RATIFICATION              = NOT PERFORMED
DP-03                         = NOT DECIDED — no Architect instrument exists
DP-04                         = NOT DECIDED — no Architect instrument exists
NEW SUBSYSTEM                 = NOT CREATED  (native_core still exactly eleven)
NEW ENTITY                    = NOT CREATED
NATIVE CORE FREEZE            = NOT MODIFIED
P11 BLUEPRINT                 = NOT SILENTLY MUTATED
P12                           = NOT ACTIVATED
PD                            = NOT MODIFIED
FOUNDER AUTHORITY             = NOT EXPANDED
ARCHITECT AUTHORITY           = NOT SELF-EXERCISED
PROTECTED PACKAGES            = UNTOUCHED
```

## `§33` Verification

**Source** — every architectural claim traced to an actual body: Native Core
Blueprint `§4`, `Freeze §5`/`§2`, `INV-13`, `PR-3`/`PR-4`, `optimization/__init__.py`,
`governance/__init__.py`, `workflow/__init__.py`, `trace/record.py`,
`capability/ownership.py`.
**Architecture** — Option C's conflict with `§4` is proven, not asserted.
**Authority** — Architect, `Constitution §3.4`.
**Boundary** — P11/P12/PD intact.
**Decision** — **neither DP-03 nor DP-04 was taken.** Every recommendation
carries the non-decision label.

## `§30` Status

```text
DP-03 = DECISION-PENDING     DP-04 = DECISION-PENDING
DP-01 = PREPARED — not final until DP-03/DP-04 decided
DP-02 = PREPARED — partially affected
```

**`SILENCE ≠ APPROVAL` · `RECOMMENDATION ≠ DECISION`.**
