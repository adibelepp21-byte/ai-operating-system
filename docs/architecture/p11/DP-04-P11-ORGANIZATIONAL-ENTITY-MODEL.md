# ADR / ARCHITECT DECISION — DP-04

## P11 Organizational Entity Model

| Field | Value |
|---|---|
| **Decision ID** | `DP-04` |
| **Domain** | Phase 11 — Autonomous Organization |
| **Decision Class** | Architecture / Canonical Entity Model |
| **Authority** | **Architect Reserved Authority** |
| **Status** | **`DECISION-PENDING`** |
| **Version** | 1.0 |
| **Effective Date** | *[TO BE FILLED AFTER ARCHITECT DECISION]* |
| **Architect** | *[TO BE FILLED]* |

> # ⚠ `DECISION-PENDING` — NOT ISSUED
>
> **`§14`, `§15`, `§21` and `§22` are unfilled and are the Architect's alone.**
> Everything below them is evidence prepared under delegated authority; **none of
> it is a decision.** `§23`: this status *"does NOT mean approved · accepted ·
> authorized · adopted · frozen · implemented."*
>
> **Prepared by:** Claude Code / Co-Founder · **2026-09-10**
> **Evidence sections filled:** `§4.2`, `§5`, `§6`, `§7`, `§12`, `§13`, `§19`.
> **Architect sections untouched:** `§14`, `§15`, `§21`, `§22`.

---

## Discrepancy in the supplied instrument — reported, not corrected

**`§0` states the status may change to `ISSUED` once the Architect choice *"is
explicitly entered in Section 13."*** But **`§13` is `CO-FOUNDER
RECOMMENDATION`**; the Architect's choice belongs in **`§14 EXPLICIT ARCHITECT
CHOICE`**, which `§23` then confirms by requiring *"Sections 14, 15, 21, and 22"*.

**Read literally, `§0` would place the Architect's decision inside the
Co-Founder's recommendation section.** That is exactly the confusion this
instrument exists to prevent, so it is **flagged rather than silently
renumbered** — `§13`'s content is not mine to relocate, and correcting an
Architect instrument is not a delegated act. **`§23`'s enumeration is treated as
governing**, and `§14` is left as the choice section.

---

## 1. Exact decision question

Reproduced from the instrument. The four concepts it names as requiring
resolution are **`Goal`**, **`Plan`**, **`Delegation`**, **`OrganizationalState`**.

---

## 4.2 Sixteen-item canonical reconciliation (`§4`)

Items reproduced **exactly** from the actual P11 Blueprint `§15` body, in its
order. `§4.1` forbids manufacturing an entity from entity-like terminology, and
none was manufactured.

| # | Exact `§15` concept | Canonical meaning | Frozen entity / structure | Status | Reserved? | New entity required? | Evidence | Architect decision? |
|---|---|---|---|---|---|---|---|---|
| 01 | `Organization` | hierarchy root; owns Departments | **Organization** — frozen | **FROZEN ENTITY** | no | **NO** | `Freeze §4`; `native_core/core/capability/ownership.py` | **NO** |
| 02 | `OrganizationGoal` | organizational objective | none | **UNRESOLVED — REQUIRES ARCHITECT DECISION** | **`Goal` reserved** | **UNKNOWN** | `Freeze §2` reserved list | **YES** |
| 03 | `Plan` | planned decomposition | none | **UNRESOLVED — REQUIRES ARCHITECT DECISION** | no counterpart | **UNKNOWN** | no frozen counterpart found | **YES** |
| 04 | `PlanStep` | step within a plan | none | **UNRESOLVED — REQUIRES ARCHITECT DECISION** | no counterpart | **UNKNOWN** | as `Plan` | **YES** |
| 05 | `WorkItem` | unit of organizational work | none; `WorkEntry` resolves without one | **UNRESOLVED — REQUIRES ARCHITECT DECISION** | **`Task` reserved** | **UNKNOWN** | `Freeze §2`; `WorkEntry` docstring: *"This is not a Work entity"* | **YES** |
| 06 | `Department` | accountability unit | **Department** — frozen | **FROZEN ENTITY** | no | **NO** | `Freeze §4`; `capability/ownership.py` | **NO** |
| 07 | `Capability` | Department-owned unit of ability | **Capability** — frozen | **FROZEN ENTITY** | no | **NO** | `Freeze §4` | **NO** |
| 08 | `Dependency` | relation between capabilities | — | **NON-ENTITY / CONCEPT** — a relationship | no | **NO** | `INV-9` versioned dependency; `INV-10` cross-Dept governance | **NO** |
| 09 | `Delegation` | authority passed within bounds | none | **UNRESOLVED — REQUIRES ARCHITECT DECISION** | no counterpart | **UNKNOWN** | no frozen counterpart found | **YES** |
| 10 | `Execution` | act of running work | — | **NON-ENTITY / CONCEPT** — `Freeze §5` **layer 2** | no | **NO** | `Freeze §5` layer table | **NO** |
| 11 | `Observation` | what the system noticed | **`ObservationPublication`** | **IMPLEMENTED STRUCTURE** | `Event` reserved, **but not the counterpart** | **NO** | `native_core/core/optimization/contract.py:59`; `composition.py:97` `PassiveObservationPublication` | **NO** — confirmation only |
| 12 | `Verification` | act of verifying | — | **NON-ENTITY / CONCEPT** — an activity | no | **NO** | no frozen entity; verification is performed, not held | **NO** |
| 13 | `Escalation` | boundary reached, raised | **Trace status** | **IMPLEMENTED STRUCTURE** | no | **NO** | `native_core/core/trace/record.py:31` — `VALID_STATUSES = frozenset({"success", "failure", "escalation"})`, annotated *"Domain Model §2.1"* | **NO** — confirmation only |
| 14 | `Evidence` | record supporting a claim | — | **PROJECTION / DERIVED VIEW** | `Artifact` reserved | **NO** | evidence records are produced, not a frozen entity | **NO** |
| 15 | `OrganizationalState` | organization-level state | none | **UNRESOLVED — REQUIRES ARCHITECT DECISION** | **`State-as-entity` reserved** | **UNKNOWN** | `Freeze §2`; `P12-W2` boundary — `§10` | **YES** |
| 16 | `PerformanceRecord` | record of organizational performance | **`ObservationPublication`** | **IMPLEMENTED STRUCTURE** | no | **NO** | `optimization/contract.py` | **NO** — confirmation only |

**Tally:** 3 **FROZEN** · 3 **IMPLEMENTED** · 1 **PROJECTION** · 3 **NON-ENTITY**
· **6 UNRESOLVED**.

**`§4.2`'s constraint is honoured: no concept was classified merely to eliminate a
conflict.** The six unresolved are left unresolved.

---

## 5. The twelve frozen entities (`§5`)

Reproduced from the **actual body** of `AIOS_ARCHITECTURE_FREEZE_v1.0.md §4`, as
`§5` requires — **not** from filenames, classes, or directories.

| # | Frozen entity | Canonical definition (`Freeze §4`) | Layer (`Freeze §5`) | Relationship to `§15` |
|---|---|---|---|---|
| 01 | **Organization** | *"hierarchy root … owns Departments; accountability root"* | above layer 4 | **is** item 01 |
| 02 | **Department** | *"accountability unit … owns Capabilities and Agent Definitions"* | above layer 4 | **is** item 06 |
| 03 | **Capability** | *"a Department-owned unit of ability"*; owned by *"exactly one Department (INV-1)"* | 4 | **is** item 07 |
| 04 | **Agent Definition** | *"the template of an agent; implements ≥1 Capability (INV-2)"* | 3 | not in `§15` |
| 05 | **Agent Instance** | *"a runtime execution of exactly one Definition … **the only actor**"* | 3 | not in `§15` |
| 06 | **Skill** | *"a reusable unit of ability"* | 5 | not in `§15` |
| 07 | **Workflow** | *"governed composition; the sanctioned multi-agent channel (INV-13)"* | 6 | bears on coordination, not `§15` |
| 08 | **Tool** | *"the only entity permitted a direct external/vendor dependency (INV-12)"* | 9 | not in `§15` |
| 09 | **Runtime** | *"hosts Agent Instances (INV-3); a facility, not an actor"* | 2 | not in `§15` |
| 10 | **Knowledge** | *"durable, authoritative, versioned understanding; entered only via governed promotion (INV-8)"* | 8 | not in `§15` |
| 11 | **Memory** | *"derived, provisional, retention-bounded record (INV-7)"* | 7 | bears on item 15 |
| 12 | **Trace** | *"the immutable, append-only, unconditional record of one Agent-Instance action (INV-4/5)"* | cross-cutting | **carries item 13**; underwrites item 14 |

**`§5`'s constraint respected:** their frozen status is an **input**, not a
question. Only nine of the twelve bear on `§15` at all.

---

## 6. Reserved concepts (`§6`)

| Reserved concept | Canonical location | Meaning | Implemented? | Authority | Relationship to `§15` |
|---|---|---|---|---|---|
| **`Goal`** | `Freeze §2` — *"Reserved concepts with no ratified entity"* | no ratified entity | **NO** | Architect | **item 02** |
| **`Task`** | `Freeze §2` | no ratified entity | **NO** | Architect | **item 05** |
| **`State-as-entity`** | `Freeze §2` | no ratified entity | **NO** | Architect | **item 15** |
| **`Event`** | `Freeze §2` | no ratified entity | **NO** | Architect | item 11 — **but item 11 maps to an existing publication instead** |
| **`Artifact`** | `Freeze §2` | no ratified entity | **NO** | Architect | item 14 |
| **prioritization model** | `optimization/__init__.py`, citing `optimization_spec §12/§14`, `P7-I27 Conflict B` | *"NOT implemented here — **Architect Reserved**"* | **NO** | **Architect** | bears on `P11-W2`, **not on `§15`** |
| **decision heuristics** | same | same list | **NO** | **Architect** | bears on `P11-W2` |
| **ranking model · recommendation engine · evaluation scoring · signal catalogue · optimization algorithm · promotion strategy** | same | same list | **NO** | **Architect** | bear on `W2`/`W6` |

**Verbatim, from the optimization boundary:** *"No scoring, ranking, or
recommendation surface exists, and none can be added without extending the
contract under a future authorization."*

**`§6`'s rule is honoured:** none was promoted. **`ARCHITECT-RESERVED ≠
IMPLEMENTED ≠ CANONICAL ENTITY`.**

---

## 7. Implemented / projection / non-entity reconciliation (`§7`)

### 7.1 Implemented structures — verified at definition, not by name

| Concept | Actual definition | Reconciliation |
|---|---|---|
| **`Escalation`** | `trace/record.py:30-31`: *"Ratified action outcomes (Domain Model §2.1: success / failure / escalation)"*, `VALID_STATUSES = frozenset({"success", "failure", "escalation"})` | **Escalation is a ratified Trace *status*, not an entity.** `§7`'s instruction to reconcile it with the Trace status model is satisfied: it is already there |
| **`Observation` / `PerformanceRecord`** | `optimization/contract.py:59` `class ObservationPublication(abc.ABC)`; `composition.py:97` `PassiveObservationPublication` | Both map to the **existing publication contract**. The optimization boundary *"observes Trace and Memory and publishes what it observed"* |
| **`Organization` / `Department`** | `capability/ownership.py:71`, `:98` with `OrganizationIdentity`, `DepartmentIdentity`, `OwnershipGraph` | Reconciled with the **existing capability/ownership model**, exactly as `§7.1` directs |

### 7.2 Projections (`§7.2`)

**`Evidence`** — the only item classified as a projection:

```text
SOURCE            Trace (immutable, INV-4/INV-5) + persisted records
DERIVATION RULE   select records supporting a specific claim
PROJECTION        an evidence view
CONSUMER          verification, audit, certification packages
```

**`Accountability`**, though not a `§15` item, derives the same way — Trace is
immutable and append-only, so *who decided, delegated, executed and verified* is
**reconstructable without any new entity**.

### 7.3 Non-entity concepts (`§7.3`)

`Dependency` — a **relationship** (`INV-9`, `INV-10`).
`Execution` — a **layer** (`Freeze §5` layer 2).
`Verification` — an **activity**, performed rather than held.

**The Blueprint's own words support this reading:** `§15` says *"P11 should expose,
at minimum **where applicable**, the following **conceptual entities**."*
**`CONCEPTUAL ENTITY MENTION ≠ MANDATORY RUNTIME ENTITY`**, as `§7.3` states.

---

## 8. The four unresolved concepts — evidence only, no classification proposed

**`§8` forbids silent reclassification. None is offered.** What follows is the
evidence bearing on each; the classification lines remain the Architect's.

**`Goal`** — `Freeze §2` reserves it. No frozen counterpart. No prior ADR decides
it (`§19`). Bears on `P11-W2` goal decomposition.
**Architect decision required:** *[TO BE DECIDED]*

**`Plan` / `PlanStep`** — no reserved counterpart and no frozen counterpart. The
adjacent reserved material sits in `optimization` (*prioritization model*). Could
be persistent state, transient structure, projection, or documentation artifact.
**Architect decision required:** *[TO BE DECIDED]*

**`Delegation`** — no frozen counterpart. The nearest existing semantics are
`governance`, which *"holds authority over decisions"*, decides *"nothing
automatically"* (`PR-3`) and *"fails closed"* (`PR-4`) — **but imports nothing
from Workflow, Agent, Runtime or Optimization**, which delegation must span.
**Architect decision required:** *[TO BE DECIDED]*

**`OrganizationalState`** — `State-as-entity` is reserved. Directly engages the
`P12-W2` boundary (`§10`).
**Architect decision required:** *[TO BE DECIDED]*

---

## 10. P12 boundary (`§10`)

| Information | Class |
|---|---|
| Organizational goals, plans, delegation, coordination, org-level continuity | **P11** |
| Accountability reconstruction | **P11** |
| `OrganizationalState` scoped to **one organization** | **P11 — if ratified** |
| `OrganizationalState` widened to **P4–P11** | **P12** — `P12-W2` *Unified Operational State* |
| System self-model | **P12** — `P12-W5` |

> **The line is scope, not concept.** The same mechanism is P11 at organization
> scope and P12 at system scope. **`§10` therefore requires the Architect to
> state which scope is ratified** — otherwise `P11 ORGANIZATIONAL STATE ≠ P12
> UNIFIED OPERATIONAL STATE` erodes by drift rather than by decision.

---

## 12. Consequence analysis (`§12`)

| Dimension | **A — Existing entity** | **B — Projection** | **C — Non-entity semantic** | **D — New entity** |
|---|---|---|---|---|
| Frozen architecture impact | **none** | **none** | **none** | **amends `Freeze §4`** |
| Canonical complexity | lowest | low | low | **highest** |
| Implementation impact | reuse | derivation rules required | contracts required | new surface + migration |
| Runtime impact | none | low | low | **high** |
| State architecture impact | none | none | none | **engages `P12-W2`** |
| P12 impact | none | none | none | **may pre-empt `P12-W2`** |
| Governance impact | none | none | none | **Architect authority required** |
| Evidence / traceability | existing suites | derivable from Trace | contract tests | **new negative controls required** |
| **Reversibility** | n/a | **high** — delete the view | **high** | **LOW** |
| Future integration risk | **semantic overload** if forced | derivation must stay precise | persistence may still be needed | **lowest distortion, highest cost** |

**The honest asymmetry:** A, B and C are cheap and reversible **but may distort
semantics if forced**; D is semantically cleanest **and least reversible**. `§9`
is explicit that `NO-NEW-ENTITY ≠ FORCE FIT EVERY CONCEPT`.

---

## 13. CO-FOUNDER RECOMMENDATION

> # CO-FOUNDER RECOMMENDATION — **NOT ARCHITECT DECISION**

**For the twelve resolved items: A + B + C as classified in `§4.2`.** Three are
frozen entities, three already exist as implemented structures, one is a
projection, three are relationships/layers/activities. **This needs no new
entity and creates no Freeze conflict.**

**For the four unresolved: I make no recommendation, and that is deliberate.**

`§13` invites a recommendation and `§1.1` warns that *"the Architect must not
merely approve the Co-Founder recommendation."* **Recommending on all four would
work against that warning**, because the evidence does not separate the options:

- **`Goal`, `Plan`, `OrganizationalState`** each sit on or beside a **reserved
  concept**. Recommending "projection" would be choosing the cheap option;
  recommending "new entity" would be choosing the one `§20` of the preparing Act
  forbids me to select. **Neither is evidence-driven.**
- **`Delegation`** has a real tension I can state but not resolve: its semantics
  match `governance`, and `governance`'s isolation forbids it the spanning role.
  **That is an architectural trade-off, not a fact.**

**What I do recommend is a principle**, matching `§13.1`'s preliminary text:
**prefer the minimum canonical surface that preserves semantic correctness** —
reuse where semantics genuinely match, project where derivation is exact, and
**introduce a new entity only where representation without it would distort
meaning.** Whether any of the four crosses that line is the Architect's judgement.

---

## 14. EXPLICIT ARCHITECT CHOICE

*This section MUST remain unfilled until the Architect actually decides.*

```text
ARCHITECT DECISION:
[  ] OPTION A — EXISTING-ENTITY / EXISTING-STRUCTURE RECONCILIATION
[  ] OPTION B — PROJECTION / DERIVED-MODEL APPROACH
[  ] OPTION C — EXPLICIT NON-ENTITY SEMANTIC MODEL
[  ] OPTION D — ARCHITECT-AUTHORIZED NEW ENTITY
[  ] OTHER — ONLY IF EXPLICITLY DEFINED BY ARCHITECT:
    ___________________________________________
```

**Goal** — CLASSIFICATION: *[TO BE FILLED BY ARCHITECT]* · CANONICAL HOME: *[TO BE FILLED]* · RATIONALE: *[TO BE FILLED]*
**Plan** — CLASSIFICATION: *[TO BE FILLED BY ARCHITECT]* · CANONICAL HOME: *[TO BE FILLED]* · RATIONALE: *[TO BE FILLED]*
**Delegation** — CLASSIFICATION: *[TO BE FILLED BY ARCHITECT]* · CANONICAL HOME: *[TO BE FILLED]* · RATIONALE: *[TO BE FILLED]*
**OrganizationalState** — CLASSIFICATION: *[TO BE FILLED BY ARCHITECT]* · CANONICAL HOME: *[TO BE FILLED]* · P11/P12 BOUNDARY: *[TO BE FILLED]* · RATIONALE: *[TO BE FILLED]*

## 15. ARCHITECT RATIONALE

*[TO BE FILLED BY ARCHITECT]*

## 21. EFFECTIVE DATE

*[TO BE FILLED ONLY AFTER ACTUAL ARCHITECT DECISION]*

## 22. ARCHITECT SIGNATURE

```text
Name:                [TO BE FILLED]
Role:                ARCHITECT
Decision ID:         DP-04
Decision:            [TO BE FILLED]
Date:                [TO BE FILLED]
Signature/Approval:  [TO BE FILLED]
```

---

## 19. Prove-me-wrong (`§19`)

| Test | Result |
|---|---|
| Could an existing frozen entity already provide this semantic? | **YES for 3** — Organization, Department, Capability. **No** for the four unresolved |
| Could this be only a projection? | **YES for `Evidence`.** For `Goal`/`Plan`/`OrganizationalState` — **UNKNOWN**, and not asserted |
| Could this be only a relationship? | **YES for `Dependency`** (`INV-9`/`INV-10`). Plausible for `Delegation` — **unproven** |
| Could this be only an operational state? | **YES for `Escalation`** — verified as a Trace status |
| Could this be a P12 concern? | **YES for `OrganizationalState` at system scope** — `P12-W2` |
| Could treating this as an entity violate No-New-Entity? | **YES** for all six unresolved — `Freeze §4` *"No new entity"* |
| Could refusing a new entity create semantic distortion? | **YES — and this survives.** `Delegation` has no frozen counterpart and the nearest boundary structurally cannot host it. **Forcing it into a projection may distort meaning** |
| Could an existing ADR already decide this? | **NO — searched all 29 ADRs; none decides `Goal`, `Plan`, `Delegation` or organizational state** |
| Could a frozen definition contradict the proposed classification? | **NO contradiction found** for the twelve classified items |

> ### Surviving contradiction, reported as `§19` requires
>
> **`NO-NEW-ENTITY` and semantic correctness genuinely conflict for
> `Delegation`.** Its semantics match `governance`; `governance`'s isolation
> forbids it the spanning role; no other boundary claims it; and no projection
> over Trace obviously reconstructs *authority conferred within bounds* as
> opposed to *authority exercised*.
>
> **This is the strongest case among the four for Option D — and I do not select
> it.** `§11` reserves that to the Architect and `§18 NC-05` forbids me forcing it
> the other way to satisfy the constraint.

---

## 18. Negative controls (`§18`)

```text
NC-01 recommendation treated as decision        NOT DONE — §13 labelled, §14 unfilled
NC-02 DECISION-PENDING treated as approval      NOT DONE
NC-03 silence treated as approval               NOT DONE
NC-04 entity created from a §15 mention         NOT DONE — 3 non-entity, 1 projection
NC-05 concept forced into an existing entity    NOT DONE — 6 left unresolved
NC-06 frozen architecture modified              NOT DONE
NC-07 Native Core subsystem created             NOT DONE — still exactly eleven
NC-08 DP-04 used to decide DP-03                NOT DONE — §2 scope respected
NC-09 technical necessity used as authority     NOT DONE
NC-10 implementation treated as canonical       NOT DONE — implemented ≠ canonical, §6
NC-11 projection treated as canonical entity    NOT DONE — Evidence marked projection
NC-12 concept treated as runtime entity         NOT DONE
NC-13 P11 state expanded into P12               NOT DONE — §10 boundary preserved
NC-14 DP-04 treated as P11 authorization        NOT DONE
NC-15 DP-04 treated as E11 ratification         NOT DONE
```

## 16. Affected artifacts (`§16`)

**No artifact was mutated** — `§16`: *"No artifact SHALL be mutated merely because
this decision is pending."*

| Artifact | Current | Effect of DP-04 | Authority |
|---|---|---|---|
| P11 Blueprint `§15` | Draft, conceptual | classification recorded **elsewhere**; Blueprint untouched | Founder/Architect |
| Canonical entity model | 12 frozen | **unchanged unless Option D** | Architect |
| Architecture Freeze | frozen | **unchanged unless Option D** | Architect |
| P12 boundary | `P12-W2` defined | clarified **only if** `OrganizationalState` scope is stated | Architect |
| `DP-03` | DECISION-PENDING | **takes DP-04 as input** (`§25`) | Architect |
| `DP-01` / `DP-02` | prepared | **not final** until DP-04/DP-03 issue | Founder |

## 23. Final status

> # `STATUS = DECISION-PENDING`
>
> `§23`: *"Architect decision has not yet been issued."* It does **not** mean
> approved, accepted, authorized, adopted, frozen, or implemented.
>
> **To issue:** complete `§14`, `§15`, `§21`, `§22`. Without all four, `§23`
> requires the status remain `DECISION-PENDING`.
