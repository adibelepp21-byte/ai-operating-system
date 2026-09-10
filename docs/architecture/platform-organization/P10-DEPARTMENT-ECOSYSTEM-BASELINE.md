# P10 — Department Ecosystem · Entry & Operational Baseline

> **Authority:** `ACT-CC-P10-AUTHORIZATION` (Founder-issued, 2026-09-10) —
> the Phase 10 authorization instrument recorded as absent at `VERIFICATION §62.3`.
> **Executed under** `ACT-CC-AIOS-DECISION-INTAKE-…-GATE-v1.0` as the continuation
> mechanism (`ACT §23`).
>
> **`ACT §26`: `P10 AUTHORIZED ≠ P10 COMPLETE`.** This baseline records what
> Phase 10 **is**, measured, on the day authorization arrived.

---

## 1. The distinction this baseline is built to preserve

`ACT §5`, verbatim:

```text
PD-01 … PD-10 = PLATFORM ORGANIZATION
                SOURCE / DEFINITION / CONSTRUCTION SURFACE

P10           = DEPARTMENT ECOSYSTEM
                OPERATIONALIZATION / ORGANIZATIONAL RUNTIME
```

and: *"PD documentation shall not be treated as proof that the corresponding
organizational runtime is already operational."*

**`CANONICAL DEFINITION ≠ RUNTIME STATE`.** Everything below is a measurement of
which side of that line each element actually sits on.

## 2. Measured state of the Department entity

**Read from source, not from prior conclusions** (`ACT §27.5`).

| Layer | State | Evidence |
|---|---|---|
| **Entity** — ratified | **FROZEN** | `Freeze §4` Spine: *"accountability unit … owns Capabilities and Agent Definitions"*, `INV-1`, `INV-2` |
| **Engineering spec** | **RESIDENT** | `docs/engineering/department/department_spec.md`, 56 lines, authority `ACT-CC-F03-035 DEC-DEPT-REALIZATION = AUTHORIZE` |
| **Implementation location** | **RESOLVED** | `department_spec §13A` — `native_core/core/capability/ownership.py`, because Blueprint `§4` fixes the core at *"exactly the eleven frozen subsystem boundaries — no more"* |
| **Realization** | **IMPLEMENTED** | `ownership.py`, **520 lines** — `Organization`, `Department`, `DepartmentIdentity`, `OwnershipGraph` with resolve · disputed · unbacked · unowned queries |
| **Conformance** | **VERIFIED** | `test_ownership_conformance.py`, **58 tests**; `INV-1` ×6, `INV-2` ×4; negative controls present (two departments claiming one Capability **fails closed**) |
| **Population** | **EMPTY** | **Zero `Department` instances anywhere outside `ownership.py` and its tests.** `OwnershipGraph(` is **never constructed by non-test code**. No resident Department/Organization catalog or data file exists |

## 3. THE FINDING

```text
DEPARTMENT MECHANISM   : IMPLEMENTED and VERIFIED
DEPARTMENT POPULATION  : EMPTY
ORGANIZATIONAL RUNTIME : NOT OPERATIONAL
```

**The organization exists as a capability of the system, not as an instance of
one.** Every part that could be built without knowing *which* Departments exist
has been built and proven. Nothing that requires knowing has been.

**This is not a defect.** It is the exact shape a correctly-sequenced system
takes when its mechanism is complete and its population is reserved.

## 4. What blocks the central P10 action, precisely

**Populating the ownership graph requires the Department population.** That is
`G-09` — OPEN, **FOUNDER / ARCHITECT RESERVED** since 2026-09-06, and carried by
**`ADR-0029`** (Proposed, not Approved).

| Source | Members | Count |
|---|---|---|
| `Master Program Volume VII §3` | Executive Office · Engineering · Finance · Research · Marketing · Content | **6** |
| Platform Organization | `PD-01` … `PD-10` | **10** |

**`INV-1` requires *"exactly one Department"* to own each Capability.** A
population that is not determinate cannot satisfy an invariant stated over its
members — which is why `ownership.py` is complete and empty rather than
partially populated.

### 4.1 New evidence from this Act — `ADR-0029` is narrowed, not resolved

`ACT §5` establishes a **direction** that was not previously in evidence:

```text
PD-01 … PD-10 → ORGANIZATIONAL SOURCE → P10 → ORGANIZATIONAL
OPERATIONALIZATION → DEPARTMENT ECOSYSTEM
```

**The Platform Divisions are the organizational *source* for the Department
Ecosystem.** That is materially relevant to `ADR-0029` and did not exist when
the ADR was drafted.

**It does not decide the ADR.** `ACT §5`'s `PD ≠ P10` is a statement about
**Platform Division versus Phase**, not about Platform Division versus
Department, and it does not address the six-name Master Program list.
**`NARROWED ≠ RESOLVED`**, and `ACT §11` forbids inventing the decision.

**`ADR-0029` is updated with this evidence and remains Proposed.**

## 5. `§6.2` operationalization chain, mapped to frozen boundaries

`ACT §6.2` names nine elements. Each is mapped to the frozen boundary that
already owns it, or marked as having none. **No new entity or boundary is
proposed** — `Freeze §4` states *"No new entity"* and Blueprint `§4` fixes the
core at eleven.

| # | Element | Frozen home | State |
|---|---|---|---|
| 1 | **WORK INTAKE** | — | **NO FROZEN HOME.** `Freeze §2` reserves Task/Goal/Event as *"reserved concepts with no ratified entity"* |
| 2 | **STATE** | — | **NO FROZEN HOME.** `Freeze §2`: *State-as-entity* is a reserved concept; `§10` defers it |
| 3 | **DELEGATION** | `Governance` (layer 1) | **PRESENT** — authority delegation is governed; `Freeze §8` boundaries un-bypassable |
| 4 | **COORDINATION** | `Workflow` (layer 6) | **PRESENT and FROZEN** — *"the sanctioned multi-agent channel"* (`INV-13`) |
| 5 | **EXECUTION / WORKFLOW** | `Runtime` (2) + `Agent` (3) + `Workflow` (6) | **PRESENT** — `Runtime hosts Agent Instance` (`INV-3`); Instance is *"the only actor"* |
| 6 | **HANDOFF** | `Workflow` (partial) | **PARTIAL** — `INV-13` permits coordination through Workflow, Knowledge or scoped Memory; no handoff *primitive* is frozen |
| 7 | **ESCALATION** | `Governance` (1) | **PRESENT** — `Constitution §14.2`: an Agent Instance records out-of-scope conditions *"through the Trace record's escalation status"* |
| 8 | **OBSERVATION** | `Trace` (cross-cutting) | **PRESENT and FROZEN** — immutable, append-only, unconditional (`INV-4`, `INV-5`) |
| 9 | **FEEDBACK / IMPROVEMENT** | `Memory` (7) → `Knowledge` (8) → `Optimization` (10) | **PRESENT and FROZEN** — governed promotion (`INV-8`); Optimization outputs *"proposals only"* |

**Six of nine have a frozen home. Two have none. One is partial.**

### 5.1 What the two homeless elements mean

**`WORK INTAKE` and `STATE` are not missing implementation — they are
`Freeze §2` reserved concepts and `§10` deferred architecture, both
Architect-reserved.** Building either would introduce an entity into a model
that says *"No new entity"*.

**Measured in code, consistent with the above:**

```text
intake    0 non-test modules       observation   25
feedback  0                        coordination   8
improve   0                        delegation    10
handoff   1                        escalation     1
```

**The zeros fall exactly on the two elements with no frozen home**, and the
counts fall exactly on the six that have one. **The architecture and the
implementation agree about what does not exist.**

## 6. P10 state, classified (`ACT §21`)

| Element | Classification |
|---|---|
| Department entity, spec, realization, conformance | **ALREADY-SOLVED** |
| Department population | **ARCHITECT-RESERVED** — `G-09` / `ADR-0029` |
| Ownership-graph construction from a population | **BLOCKED** — depends on the above |
| `WORK INTAKE`, `STATE` | **ARCHITECT-RESERVED** — `Freeze §2`/`§10` deferred |
| `HANDOFF` primitive | **UNKNOWN WITH DOCUMENTED BASIS** — `INV-13` permits the paths; no primitive is frozen |
| `DELEGATION`, `COORDINATION`, `EXECUTION`, `ESCALATION`, `OBSERVATION`, `FEEDBACK` | **ALREADY-SOLVED** — frozen and implemented |
| Cross-PD interface definition | **SOURCE-BLOCKED** — `ESC-C7-01`, non-resident Volume 1/2 corpora |
| Phase↔PD provider relation | **NOT-A-GAP** — the inference was tested and **rejected** by `ACT-CC-P6-071 §12` |

## 7. P10 verdict under `ACT §28` vocabulary

```text
P10 AUTHORIZED   — yes, by ACT-CC-P10-AUTHORIZATION
P10 CONSTRUCTED  — the mechanism was already constructed and verified
P10 OPERATIONAL  — NO. Population empty; organizational runtime not started.
P10 BLOCKING ITEM — ONE: the Department population (ADR-0029)
```

**`P10 AUTHORITY-BLOCKED` at a single, named, already-escalated point.**

**No readiness is manufactured** (`ACT §11`, `§24`). **No population was
invented to make the graph non-empty** — inventing one would breach `INV-1` the
moment a Capability resolved to a Department that no authority had established.

## 8. What this baseline changes

**Before:** P10 was described as blocked by Phase 9 immaturity — a claim
`FD-P9-002` falsified — and the Platform Organization corpus was the only P10
artifact.

**Now:** P10 is authorized, its mechanism is measured as complete and verified,
its population is measured as empty, and **exactly one reserved decision stands
between the two.** The distinction `ACT §5` requires — definition versus runtime
state — is no longer a caution in a document; **it is a measurement with numbers
on both sides.**
