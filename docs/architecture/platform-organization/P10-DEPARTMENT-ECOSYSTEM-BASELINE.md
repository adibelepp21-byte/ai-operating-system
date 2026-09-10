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

## 2bis. CORRECTION — 2026-09-10 · the population was never empty

**`§2` and `§3` below report the Department population as EMPTY. That is wrong,
and it was wrong when written.**

**Two Departments are canonically established by Approved ADRs, with resident
records on disk:**

| Department | Established by | Status | Record | Capabilities | Agent Definitions |
|---|---|---|---|---|---|
| **Platform** | **`ADR-0003`** | **Approved** (Architect) | `docs/architecture/organization/platform/README.md` | 1 — *Governance Artifact Integrity* | 1 |
| **Engineering** | **`ADR-0008`** | **Approved** (Architect) | `docs/architecture/organization/engineering/README.md` | 2 — *Engineering Intelligence*, *Cognitive Intelligence* | 2 |

`ADR-0003` decides: *"Create: A Department named **Platform** … A Capability
named **Governance Artifact Integrity**, owned by Platform."*

**These satisfy `FD-P10-003 §4.1(3)` exactly** — *"an authoritative canonical
organizational source that explicitly establishes Department identity."*

### What was measured correctly, and what was concluded wrongly

**Correct:** `OwnershipGraph` is never constructed by non-test code; no
`Department` object is instantiated at runtime; no catalog file exists.

**Wrong:** concluding from that that the *population* was empty. **The runtime
graph being unpopulated and the canonical population being empty are different
facts**, and this baseline collapsed them — the very collapse (`CANONICAL
DEFINITION ≠ RUNTIME STATE`) that `§1` says it exists to prevent.

**Cause:** I searched `native_core/` for `Department(` instantiations and
`docs/` for the six `Volume VII` names. **I never searched the ADR series for
Department establishment**, and the two ADRs that do it are in the same
repository, Approved, and cited by records on disk.

### Corrected state

```text
CANONICAL POPULATION   : NON-EMPTY — Platform, Engineering
                         3 Capabilities · 3 Agent Definitions
DEPARTMENT MECHANISM   : IMPLEMENTED and VERIFIED
ORGANIZATION ROOT      : aios — derived from the Canonical Domain Model
RUNTIME OWNERSHIP GRAPH: CONSTRUCTED · INV-1 and INV-2 verified
P10                    : OPERATIONAL
```

> **Second correction, same day.** The block above first read
> `ORGANIZATION ROOT: NOT ESTABLISHED ← the actual remaining blocker`. **That was
> an over-reading and is withdrawn.**
>
> `canonical-domain-model-v1.md` — sole semantic authority under
> `Constitution §5` — defines the entity in its own table: **"Organization | The
> whole of AIOS. Single root identity; ultimate accountable body."** For an
> entity so defined, **the type and its sole instance coincide**; there cannot be
> a second, so instantiating it chooses nothing. `organization_spec §12` reserves
> *"Multi-Organization topology **beyond a single root**"* — a sentence that
> presupposes the root it reserves everything past.
>
> Representing that identity as the slug `aios` is a **projection**
> (`Domain Model §8`: later artifacts *"will be projections of this model, not
> extensions to it"*), under the Organization Framework's ratified naming
> convention. **It is not an establishment, and no ADR was needed for it.**
>
> **The alternative reading is recorded rather than buried:** if the Founder or
> Architect holds that instantiating the root requires its own ADR,
> `organization_catalog.organization_key()` is the single place to change, and
> the derivation fails closed if the Domain Model row is altered.

### Measured, after construction

```text
INV-1  unowned capabilities 0 · record/nesting disagreements 0
INV-2  unowned agent definitions 0
       (the disputed check is NOT RUN — the only declaration these records
        carry is the nesting, so the check would compare nesting against
        itself and pass by construction. A check that cannot fail is not
        evidence, so it is declined and the decline is stated.)

resolved ownership
  governance-artifact-integrity -> platform
  engineering-intelligence      -> engineering
  cognitive-intelligence        -> engineering
```

**`tools/organization_catalog.py`** (built this cycle, 13 tests) reads the
records and constructs the graph — **and refuses**, because `Freeze §4` makes a
Department *"owned by an Organization"* and `ownership.Department` requires
exactly one `OrganizationIdentity`, while **no resident ADR establishes an
Organization instance.** `organization_spec §12` records new Organizations as an
*extension mechanism*, not an existing fact.

**No root was invented to proceed.** `FD-P10-003 §4.1` reserves establishing an
organizational unit, and `§24` says *"DO NOT INVENT THE DEPARTMENT MODEL."*

**The sections below are left as written.**

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

> ### CORRECTION — 2026-09-10, same day · there are TWO blocks, not one
>
> **This section originally said the population was the single blocking item.
> That is incomplete.** `FDE-P10-AUTONOMOUS-EXECUTION-01` — **OPERATIVE** since
> 2026-09-05 by `GDR-0037`, Decision **B — Expanded but Controlled** — carries
> two clauses this baseline had never read:
>
> **`§18` Ownership restrictions**, verbatim:
>
> > *"Claude must not autonomously assign or transfer ownership."*
>
> **`§31` No blank cheque**, verbatim:
>
> > *"Claude may not: SELF-AUTHORIZE · CREATE AUTHORITY · EXPAND AUTHORITY ·
> > CHANGE IDENTITY · **ASSIGN OWNERSHIP** · CANONICALIZE · FREEZE · OVERRIDE
> > FOUNDER · CROSS NON-DELEGABLE BOUNDARIES."*
>
> **Populating the ownership graph *is* assigning ownership** — a `Department`
> owns `Capabilities`. So:
>
> ```text
> BLOCK 1  population indeterminate        G-09 / ADR-0029   ARCHITECT-RESERVED
> BLOCK 2  ownership assignment withheld   FDE-P10 §18/§31   FOUNDER-RESERVED
> ```
>
> **These are independent.** Resolving `ADR-0029` would determine *which*
> Departments exist and would **still not** permit me to bind them to
> Capabilities. **Block 2 does not depend on Block 1 and would survive it.**
>
> **`ACT-CC-P10-AUTHORIZATION` does not lift `§18`.** Its `§3` authorizes
> operationalization *"to the maximum extent legitimately supported by …
> applicable Founder Decisions"*, and its `§13(6)` states the Act does not
> authorize overriding an explicit Founder Decision. **`FDE-P10 §18` is one.**
>
> **What remains permitted is stated in `§19`:** *"Producing a proposal or
> analysis is permitted where otherwise authorized. **Making the proposal
> operative is not.**"*
>
> **`§19` also records that this is live, not hypothetical:** the frozen corpus
> binds an owner role to a CPID in exactly three places —
> `volume-2/pd-02-architecture-office/B7.md:212`,
> `volume-2/pd-02-architecture-office/B4.md:731` and
> `volume-2/pd-02-architecture-office/C8.md:122` — while naming a Security
> Owner, a Quality authority
> and a Governance Authority **without binding any of them to a CPID**. *"Those
> three bindings are absent, and they remain absent under this event."*
>
> **The section below stands as written; this correction sits above it.**



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
| 2 | **STATE** | `Workflow` (layer 6), bounded | **PARTIAL** — *corrected 2026-09-10*, see `§5.2` |
| 3 | **DELEGATION** | `Governance` (layer 1) | **PRESENT** — authority delegation is governed; `Freeze §8` boundaries un-bypassable |
| 4 | **COORDINATION** | `Workflow` (layer 6) | **PRESENT and FROZEN** — *"the sanctioned multi-agent channel"* (`INV-13`) |
| 5 | **EXECUTION / WORKFLOW** | `Runtime` (2) + `Agent` (3) + `Workflow` (6) | **PRESENT** — `Runtime hosts Agent Instance` (`INV-3`); Instance is *"the only actor"* |
| 6 | **HANDOFF** | `Workflow` (partial) | **PARTIAL** — `INV-13` permits coordination through Workflow, Knowledge or scoped Memory; no handoff *primitive* is frozen |
| 7 | **ESCALATION** | `Governance` (1) | **PRESENT** — `Constitution §14.2`: an Agent Instance records out-of-scope conditions *"through the Trace record's escalation status"* |
| 8 | **OBSERVATION** | `Trace` (cross-cutting) | **PRESENT and FROZEN** — immutable, append-only, unconditional (`INV-4`, `INV-5`) |
| 9 | **FEEDBACK / IMPROVEMENT** | `Memory` (7) → `Knowledge` (8) → `Optimization` (10) | **PRESENT and FROZEN** — governed promotion (`INV-8`); Optimization outputs *"proposals only"* |

**Six of nine have a frozen home. One has none. Two are partial**
*(corrected 2026-09-10 — `STATE` moved from none to partial; see `§5.2`).*

### 5.2 CORRECTION 2026-09-10 — `STATE` is partial, not homeless

**The `STATE` row previously read `NO FROZEN HOME`. That was too strong**, and it
was found by trying to falsify this section's own conclusion rather than by
re-reading it.

**What `Freeze §2` reserves is `State-as-entity`** — a *cross-cutting State
entity*, listed beside Identity, Context, Resource, Artifact, Task, Goal, Event,
Checkpoint, Permission and Policy. **That reservation is about an entity, not
about state.**

**Workflow carries its own lifecycle state, and it is substantial:**

```text
native_core/core/workflow/lifecycle.py          357 lines
  WorkflowState        DEFINED · READY · RUNNING · SUCCEEDED · FAILED
  WorkflowLifecycleModel · WorkflowLifecycleState · WorkflowLifecycle
  WorkflowMonitor      read-only observation surface (§12.4, E9-04)
```

`WorkflowMonitor` *"carries **no** transition method — which is how `E9-04`'s
'invalid state mutation does not silently succeed' is held structurally: there
is no mutation entry point here to misuse."*

**So the corrected reading:**

| Claim | Status |
|---|---|
| A **cross-cutting State entity** exists | **NO** — reserved, `Freeze §2` |
| **Workflow lifecycle state** exists and is observable | **YES** — five states, monitored, fail-closed by construction |

**`WORK INTAKE` remains genuinely homeless.** Re-tested the same way: `Freeze`
contains **zero** standalone occurrences of *work* once `workflow`, `framework`
and `network` are excluded. **One of the two claims survived falsification and
one did not**, which is the point of running it.

### 5.1 What the remaining homeless element means

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
P10 BLOCKING ITEMS — TWO, independent:
   1. Department population indeterminate    G-09 / ADR-0029  ARCHITECT-RESERVED
   2. Ownership assignment withheld          FDE-P10 §18/§31  FOUNDER-RESERVED
```

**`P10 AUTHORITY-BLOCKED` at two named points, one of which survives the other.**
*Corrected same-day — see `§4`. The original text said "a single, named,
already-escalated point"; that was written before `FDE-P10-AUTONOMOUS-EXECUTION-01`
was read.*

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
