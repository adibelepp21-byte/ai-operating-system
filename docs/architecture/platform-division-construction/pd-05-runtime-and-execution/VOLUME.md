# PD-05 — Runtime & Execution · Construction Volume v0.1

| Field | Value |
|---|---|
| **CPID** | `PD-05` |
| **Name** | Runtime & Execution |
| **Construction status** | CONSTRUCTED — NOT CANONICAL |
| **Canonical** | NO |
| **Frozen** | NO |
| **Activated** | NO |
| **Authority** | `ACT-CC-POST-P13-PLATFORM-ORG-003` as amended by v1.1, authorized for execution by `FD-PO-003-01` (construction *"AUTHORIZED WITH BOUNDARY"*) |
| **Verifier** | `tools/platform_division_construction.py` |

**How to read this volume.**
- Each section states the v1.1 `§20` dimension it establishes and its v1.1
  `§10` epistemic class.
- Every `Source:` or `Reference:` line quotes text that the verifier finds
  in the cited file.
- A `Reference:` informs a section but is not its source. That covers ACT-003's
  section lists, which are candidates (`§11`), and the P10 division record,
  which is derived (`§18`).
- Nothing here is canonical, frozen or activated. Nothing here binds this
  division to any implementation boundary.

---

## S1. Volume structure

**Dimension:** — · **Class:** INHERITED-PATTERN

The volume uses the Part arrangement of the reference implementation, PD-01:
Identity, Organization, Governance/Architecture, Operating, Performance. It
inherits the arrangement, not the content: no PD-01 text is reused. The v1.1
`§20` dimensions are placed within it. Whether new volumes keep A–E or take
Parts A–H is the Architect's question `C6-A1`. The arrangement here is
therefore provisional, and structure freeze waits on that decision (v1.1 `§9`).

- Reference: `docs/architecture/volume-1/pd-01-executive-office/A1.md` — "Part A — Platform Identity & Strategic Foundation"
- Reference: `docs/architecture/volume-1/pd-01-executive-office/D1.md` — "PART D — OPERATING ARCHITECTURE"
- Reference: `docs/architecture/volume-2/pd-02-architecture-office/E4.md` — "framework dapat diwariskan ke PD-03 hingga PD-10 dengan domain adaptation;"
- Reserved: C6-A1

---

# Part A — Identity & Mandate

## A1. Identity

**Dimension:** Identity · **Class:** SOURCE-DERIVED

`PD-05` is the permanent identifier. The platform registry names the division
*Runtime & Execution*. The frozen Architecture Office corpus names its domain
*Runtime* in the architectural boundary, and states that PD-02 is not its
owner.

- Source: `docs/program/AIOS_MASTER_ROADMAP_CONSOLIDATED_v1.0.md` — "`PD-05` Runtime & Execution"
- Source: `docs/architecture/volume-2/pd-02-architecture-office/A4.md` — "├── PD-05 Runtime"
- Source: `docs/architecture/volume-2/pd-02-architecture-office/A4.md` — "PD-02 tidak menjadi owner atas domain tersebut."

## A2. Boundary

**Dimension:** Boundary · **Class:** SOURCE-DERIVED

The boundary with PD-02 is stated from PD-02's side, in prose:
- **Architecture on one side, Runtime on the other.** Neither owns the
  other's domain.
- **Execution stays with PD-05.** PD-02 holds no Runtime execution authority,
  and PD-05 continues to determine operational execution within the Runtime
  domain.
- **Architecture may constrain Runtime; it does not execute it.**

The boundary with the Runtime *entity* is also sourced. The Freeze defines
Runtime as *"a facility, not an actor"*, *"owned centrally"*. So PD-05's
accountability is for the Runtime **domain**. It is not ownership of the
Runtime entity, which no Platform Division owns.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/B7.md` — "Neither owns the other's domain."
- Source: `docs/architecture/volume-2/pd-02-architecture-office/A5.md` — "Runtime Execution NONE Runtime owner"
- Source: `docs/architecture/volume-2/pd-02-architecture-office/A5.md` — "PD-05 tetap menentukan operational execution dalam domain Runtime."
- Source: `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md` — "hosts Agent Instances (INV-3); a facility, not an actor. *Ownership*: owned centrally."

## A3. Authority

**Dimension:** Authority · **Class:** DOMAIN-ADAPTATION

**Held.** Operational execution within the Runtime domain. This is the only
authority the sources give PD-05.

**Not held:**
- **Architecture authority.** It sits with PD-02, across an Architectural
  Interface.
- **Governance decisions.** The Runtime *"enforces isolation, not policy — it
  does not decide governance"*. PD-05's authority over the domain inherits that
  limit: operating the Runtime confers no governance decision.
- **Lifecycle authority over the Runtime entity.** That is the Architect's, by
  architectural decision.

The C8 §32 relationship puts the split the same way. PD-02 defines, reviews,
assesses and maintains architecture. The Runtime owner implements, operates
and maintains runtime, and the architecture relationship does not move runtime
ownership.

This section adapts the reference pattern's authority section to the one
sourced grant. It adds no authority.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/A5.md` — "PD-05 tetap menentukan operational execution dalam domain Runtime."
- Source: `docs/architecture/volume-2/pd-02-architecture-office/A6.md` — "Runtime Runtime Owner Architectural Interface"
- Source: `docs/engineering/runtime/runtime_spec.md` — "The Runtime enforces isolation, not policy — it does not decide governance."
- Source: `docs/architecture/volume-2/pd-02-architecture-office/C8.md` — "Architecture relationship tidak memindahkan runtime ownership."

## A4. Ownership

**Dimension:** Ownership · **Class:** SOURCE-DERIVED

**What the sources say.** *"PD-05 owns Runtime."* is a prose statement in the
frozen corpus. Read with the Freeze, it is domain accountability: the Runtime
entity is *"owned centrally"*. By the Domain Model, a Platform Division owns
exactly two entity types, Capability and Agent Definition, each by exactly one
division.

**PD-05's ownership is therefore:**
- the Runtime domain's accountability;
- the Capabilities it will own;
- the Agent Definitions it will own.

**It owns none of** Runtime, Skill, Workflow, Tool, Trace or Knowledge as
entities. The frozen A5 row names a *"Runtime owner"* role. Whether that role is
PD-05 is suggested by B7 and not stated, so it is not asserted here.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/B7.md` — "PD-05 owns Runtime."
- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "1. Every Capability is owned by exactly one Platform Division."
- Source: `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md` — "hosts Agent Instances (INV-3); a facility, not an actor. *Ownership*: owned centrally."

---

# Part B — Organization & Capability

## B1. Capability

**Dimension:** Capability · **Class:** BOUNDED-RECONSTRUCTION

**Candidate Capability areas.** Each is a responsibility the sources place in
the Runtime domain, not a ratified Capability. Capability creation is
*"architectural decision, architect approval"*, so none is created here.

| Candidate area | Grounding |
|---|---|
| Instance hosting | Runtime hosts Agent Instances (INV-3) |
| Execution driving | drives Workflow-governed execution |
| Execution-consumer contract | the consumer boundary Runtime owns (ADR-0019) |
| Resumable execution state | kept distinct from the immutable Trace |
| Execution failure surfacing | fail closed; stuck execution surfaced, not silently resolved |

- Source: `docs/engineering/runtime/runtime_spec.md` — "Runtime hosts Agent Instances"
- Source: `docs/engineering/runtime/runtime_spec.md` — "keep resumable execution state distinct from the immutable Trace"
- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "Created/retired via architectural decision, architect approval"
- Reserved: DM-6

## B2. Internal organization

**Dimension:** — · **Class:** RESERVED-DECISION

PD-05's internal work is described here only as the B1 **work areas**. They
are not organizational units:
- the Spine is three levels, and *"not to be deepened … without an
  architectural decision"*;
- whether a division has internal units that own Capabilities is `G-10`, open
  for PD-01 itself.

No internal unit, team or role structure is constructed.

- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "The Spine is intentionally shallow (three levels) and is not to be deepened or bypassed without an architectural decision"
- Reserved: DM-8, G-10

---

# Part C — Domain Architecture

## C1. Architecture

**Dimension:** Architecture · **Class:** SOURCE-DERIVED

The domain's architecture has one sourced invariant, the consumer boundary:

```text
Runtime
   ↓
Execution Layer
   ↓
[ExecutionConsumer]  contract owned by Runtime
   ↓
Agent / Workflow / Skill / Planner / Scheduler
```

- **Dependency is inverted.** A consumer depends on the contract, never on
  Runtime, and *"Runtime imports nothing from agent"*.
- **Coordination** happens only via Workflow (INV-13).
- **External access** happens only via Tool (INV-12).

This describes the Runtime **domain's** architecture as the resident sources
record it. The same boundary is implemented in `native_core/core/runtime/`.
That is correspondence, not a binding of this division to that code.

- Source: `docs/architecture/adr/decisions/ADR-0019.md` — "Runtime → Execution Layer → [ExecutionConsumer] → Agent / Workflow / Skill"
- Source: `docs/architecture/adr/decisions/ADR-0019.md` — "Runtime imports nothing from agent."
- Source: `docs/engineering/runtime/runtime_spec.md` — "Coordination occurs only via Workflow (INV-13); external access only via Tool (INV-12)."
- Reference: `docs/architecture/platform-organization/IMPLEMENTATION-CORRESPONDENCE-MAP.md` — "`runtime` (layer 2)"

## C2. Candidate section structure

**Dimension:** — · **Class:** DOMAIN-ADAPTATION

**CANDIDATE — not source.** ACT-003 lists a ten-section Part C for PD-05,
C1 *Runtime Architecture Constitution* … C10 *Runtime Architecture Success*.
v1.1 `§11` keeps that list a candidate: none of its titles occurs in a resident
source.

Measured against resident evidence:

| Candidate | Resident grounding | Standing |
|---|---|---|
| Execution Layer, Execution Contract | ADR-0019; the runtime spec §5 | supported |
| Runtime Context | module `context.py` exists, but **Context** is a reserved concept with no ratified entity (Freeze §2) | reserved |
| Session | module `session.py` exists (implementation correspondence) | correspondence only |
| Runtime Process, Runtime Services | no resident source | not supported |

The sectioning is adapted, not adopted: C1 above carries what is supported.
The candidate list stays a candidate until architecture review supports it
(`C6-A1`).

- Reference: `docs/governance/acts/ACT-CC-POST-P13-PLATFORM-ORG-003-PLATFORM-ORGANIZATION-CONSTRUCTION-AND-CANONICALIZATION.md` — "C5 Execution Contract Architecture"
- Source: `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md` — "**Reserved concepts** with no ratified entity — Identity, Context,"
- Reserved: C6-A1, FRZ-2

## C3. Integration

**Dimension:** Integration · **Class:** DOMAIN-ADAPTATION

| Edge | Direction | Evidence | Standing |
|---|---|---|---|
| PD-02 ↔ PD-05 | architecture interface | A6 Canonical Ownership Map: *Runtime · Runtime Owner · Architectural Interface* | sourced |
| PD-04 → PD-05 | PD-04 depends on Runtime | `X-05`, stated only in PD-04's non-resident corpus | declared, interface undefined |
| PD-07 → PD-05 | PD-05 relies on infrastructure facilities | *"May rely on infrastructure facilities beneath it"* | sourced |
| PD-06 ↔ PD-05 | execution meets implementation | no resident statement | unknown |

The interface contents of `X-05` are not defined. Evaluating cross-division
exposure under INV-10 waits on `ADP-P10-001` (ADR-0029).

- Source: `docs/architecture/volume-2/pd-02-architecture-office/A6.md` — "Runtime Runtime Owner Architectural Interface"
- Source: `docs/engineering/runtime/runtime_spec.md` — "May rely on infrastructure facilities beneath it."
- Reference: `docs/architecture/platform-organization/CROSS-PD-INTERFACE-REGISTRY.md` — "`Primary Dependencies: Runtime`"
- Reserved: ADP-P10-001

---

# Part D — Operating

## D1. Operation

**Dimension:** Operation · **Class:** DOMAIN-ADAPTATION

The domain's operating shape, adapted from the resident Runtime specification:

```text
invoked-to-host → drive Instance actions → conclude
```

Two operating rules come from the same source:
- **Fail closed.** An action whose Trace cannot be produced is not complete.
- **Surface, do not resolve.** Stuck or hung execution is detected, not
  silently resolved.

PD-05's operating responsibility is to keep execution inside those rules.
Scheduling strategy is not decided here. It is deferred and reserved
(Freeze §10).

- Source: `docs/engineering/runtime/runtime_spec.md` — "Invoked-to-host → drives Instance actions → concludes."
- Source: `docs/engineering/runtime/runtime_spec.md` — "Fail closed (PR-4): if Trace cannot be produced for an action, the action is not accountable and must not be treated as complete."
- Source: `docs/engineering/runtime/runtime_spec.md` — "Stuck/hung execution is surfaced (detect), not silently resolved."
- Reserved: FRZ-10

## D2. Lifecycle

**Dimension:** Lifecycle · **Class:** SOURCE-DERIVED

Two lifecycles, kept apart:

| Subject | Who decides | Source |
|---|---|---|
| The division itself: its creation, retirement and name | the Architect, by architectural decision | Domain Model §6 |
| Agent Definitions it owns | PD-05, at its own discretion within Capability governance | Domain Model §6 |

The division's one affirmative lifecycle discretion is over its own Agent
Definitions. It has none over the Runtime entity.

- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "Created/retired via architectural decision, architect approval"
- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "created/deprecated at Platform Division discretion within Capability governance"

---

# Part E — Performance & Evolution

## E1. Performance

**Dimension:** Performance · **Class:** BOUNDED-RECONSTRUCTION

The PD-02 performance framework may be inherited *"tanpa memaksakan metric
PD-02"*, that is, without imposing PD-02's metrics. **Candidate** measures for
the Runtime domain, each tied to a sourced rule:

| Candidate measure | Rule it measures |
|---|---|
| Trace completeness | every hosted action yields exactly one Trace |
| Fail-closed conformance | no action counted complete without its Trace |
| Consumer-boundary integrity | no Runtime → consumer dependency |
| Stuck-execution surfacing | detected, not silently resolved |

**Measurement ≠ authority.** A measure here decides nothing. No threshold is
set.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/E3.md` — "framework dapat diwariskan ke PD-03 hingga PD-10 tanpa memaksakan metric PD-02."
- Source: `docs/engineering/runtime/runtime_spec.md` — "Every hosted Agent-Instance action produces exactly one Trace record (INV-4)"

## E2. Evolution

**Dimension:** Evolution · **Class:** RESERVED-DECISION

Evolution of the Runtime domain runs through the architecture process. The
Runtime specification defers *"Scaling, isolation mechanisms, and
scheduling"* and reserves them to the Architect. Nothing here extends the
domain into them.

- Source: `docs/engineering/runtime/runtime_spec.md` — "Scaling, isolation mechanisms, and scheduling are deferred (Freeze §10) and reserved to the Architect"
- Reserved: FRZ-10

---

## R1. Reserved and unknown register

**Dimension:** — · **Class:** RESERVED-DECISION

| Item | Holder | Effect here |
|---|---|---|
| `C6-A1` | Architect | the Part arrangement is provisional (S1, C2) |
| `FRZ-2` | Architect | Runtime Context not designed: Context is a reserved concept (C2) |
| `DM-6` | Architect | no Capability created (B1) |
| `DM-8`, `G-10` | Architect | no internal units (B2) |
| `ADP-P10-001` | Architect | X-05 exposure not evaluated (C3) |
| `FRZ-10` | Architect | scheduling, scaling and isolation not designed (D1, E2) |
| `G-01` | Founder | this volume is constructed, not a supplied canonical corpus; canonicalization is not claimed |

- Reserved: C6-A1, FRZ-2, DM-6, DM-8, G-10, ADP-P10-001, FRZ-10, G-01
- Unknown: whether the frozen A5 "Runtime owner" role is PD-05 (suggested by B7, not stated)
- Unknown: the PD-05 ↔ PD-06 boundary where execution meets implementation
