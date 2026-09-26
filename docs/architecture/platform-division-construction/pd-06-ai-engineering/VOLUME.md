# PD-06 — AI Engineering · Construction Volume v0.1

| Field | Value |
|---|---|
| **CPID** | `PD-06` |
| **Name** | AI Engineering |
| **Construction status** | CANONICAL CONSTRUCTION BASELINE — CERTIFIED WITH CLASSIFIED RESIDUAL |
| **Canonical** | YES — construction baseline |
| **Certified by** | `FD-PO-004` D1-A (Founder, 2026-09-26; Register `§53`). The sections below are those verified at `5eb0eec`, unchanged; every section keeps its class (`CANONICAL-BASELINE-MANIFEST.json`) |
| **Frozen** | NO |
| **Activated** | NO |
| **Authority** | `ACT-CC-POST-P13-PLATFORM-ORG-003` as amended by v1.1, authorized for execution by `FD-PO-003-01` (construction *"AUTHORIZED WITH BOUNDARY"*) |
| **Verifier** | `tools/platform_division_construction.py` |

**How to read this volume.**
- Each section states its v1.1 `§20` dimension and its `§10` epistemic class.
- Every quotation on a `Source:` or `Reference:` line is verified against the
  cited file.
- ACT-003's scope list and the P10 division record appear only as
  references.
- Certified as the canonical construction baseline by `FD-PO-004` D1-A.
  Certification preserves every class. It resolves no UNKNOWN or
  RESERVED-DECISION section, and freezes and activates nothing.
  Statements of status inside sections describe the state at construction.

---

## S1. Volume structure

**Dimension:** — · **Class:** INHERITED-PATTERN

The volume inherits the Part arrangement of PD-01 (Identity, Organization,
Architecture, Operating, Performance), not its content. The arrangement is
provisional pending `C6-A1`.

- Reference: `docs/architecture/volume-1/pd-01-executive-office/A1.md` — "Part A — Platform Identity & Strategic Foundation"
- Reference: `docs/architecture/volume-2/pd-02-architecture-office/E4.md` — "framework dapat diwariskan ke PD-03 hingga PD-10 dengan domain adaptation;"
- Reserved: C6-A1

---

# Part A — Identity & Mandate

## A1. Identity

**Dimension:** Identity · **Class:** SOURCE-DERIVED

`PD-06` is the permanent identifier. The registry and the frozen architectural
boundary both use the same name: *AI Engineering*.

- Source: `docs/program/AIOS_MASTER_ROADMAP_CONSOLIDATED_v1.0.md` — "`PD-06` AI Engineering"
- Source: `docs/architecture/volume-2/pd-02-architecture-office/A4.md` — "├── PD-06 AI Engineering"

## A2. Boundary

**Dimension:** Boundary · **Class:** SOURCE-DERIVED

The sharpest boundary in the Platform Organization is the one between
architecture and implementation. It is stated from both sides of PD-02's own
corpus:

```text
PD-02  architecture: may review, constrain, approve;
       may not compel implementation execution
PD-06  implementation: executes;
       bounded by architecture it does not set
```

The review relationship *"does not create organizational subordination"*.
When an Architecture Standard needs several divisions, each keeps a different
responsibility: PD-02 defines, PD-06 implements, and Quality evaluates.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/B4.md` — "The relationship does not create organizational subordination."
- Source: `docs/architecture/volume-2/pd-02-architecture-office/D8.md` — "PD-02 tidak menjadi implementation owner hanya karena mengontrol architecture change."
- Source: `docs/architecture/volume-2/pd-02-architecture-office/A5.md` — "memaksa implementation execution;"
- Source: `docs/architecture/volume-2/pd-02-architecture-office/C8.md` — "├── PD-06 — Implement AI Engineering"

## A3. Authority

**Dimension:** Authority · **Class:** DOMAIN-ADAPTATION

**Held: implementation execution within AI Engineering.** PD-02 holds none of
it and cannot compel it through Architecture Override.

**Not held:**
- architectural review, which sits with PD-02;
- authority over any other division's domain.

The frozen A5 row names an *"AI Engineering owner"*. Whether that role is PD-06
is suggested by adjacency and not stated. It is not asserted.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/A5.md` — "AI Engineering Execution NONE AI Engineering owner"
- Source: `docs/architecture/volume-2/pd-02-architecture-office/B4.md` — "AT-03 owns architectural review."

## A4. Ownership

**Dimension:** Ownership · **Class:** SOURCE-DERIVED

*"PD-06 owns implementation."* That is the frozen prose statement. Under the
Domain Model, a division's entity ownership is Capabilities and Agent
Definitions, each by exactly one division. Skill is *"owned centrally"*, so
AI Engineering owns no Skill as an entity.

**The scope of "implementation" is not stated.** At its widest reading it
would reach into every other division's domain and contradict their ownership.
So the scope is recorded as unknown, and the narrow reading is used: the
implementation of AI Engineering's own work.

C8 §33 narrows the scope without settling it. It places AI Engineering's
*"implementation responsibility"* on one path: Architecture → AI Architecture
→ AI Engineering → Implementation. PD-02 keeps architectural coherence on that
path.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/B4.md` — "PD-06 owns implementation."
- Source: `docs/architecture/volume-2/pd-02-architecture-office/C8.md` — "AI Engineering memiliki implementation responsibility."
- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "2. Every Agent Definition is owned by exactly one Platform Division and implements at least one Capability."
- Source: `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md` — "a reusable unit of ability. *Ownership*: owned centrally."

---

# Part B — Organization & Capability

## B1. Capability

**Dimension:** Capability · **Class:** BOUNDED-RECONSTRUCTION

**Candidate Capability areas.** ACT-003's scope list for PD-06 (agent
framework, AI components, engineering architecture) is a reference. It is
not source. The candidate areas are bounded by what the sources allow a
division to own:

| Candidate area | Bound |
|---|---|
| Agent Definition engineering | Agent Definitions are owned by exactly one division; created or deprecated *"within Capability governance"* |
| Implementation of architecture standards | PD-06 implements; PD-02 defines; Quality evaluates (C8 §18) |
| AI component engineering | no resident source: area named only by ACT-003 and the P10 record |

None is a ratified Capability. Creation is architect approval (`DM-6`).

- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "created/deprecated at Platform Division discretion within Capability governance"
- Reference: `docs/governance/acts/ACT-CC-POST-P13-PLATFORM-ORG-003-PLATFORM-ORGANIZATION-CONSTRUCTION-AND-CANONICALIZATION.md` — "PD-06 shall establish the AI Engineering domain."
- Reserved: DM-6

## B2. Internal organization

**Dimension:** — · **Class:** RESERVED-DECISION

The frozen B4 diagram places an *"Implementation Team"* below PD-06. That
names a working group in PD-02's review flow. It does not make that group an
entity. No internal unit is constructed: the Spine is three levels (`DM-8`),
and internal Capability ownership is open (`G-10`).

- Source: `docs/architecture/volume-2/pd-02-architecture-office/B4.md` — "Implementation Team"
- Reserved: DM-8, G-10

---

# Part C — Domain Architecture

## C1. Architecture

**Dimension:** Architecture · **Class:** DOMAIN-ADAPTATION

The domain architecture is the architecture → implementation → evaluation
chain, adapted to PD-06's side of it:

```text
Architecture Standard (PD-02 defines)
        ↓ architectural review, no subordination
Implementation (PD-06 executes)
        ↓
Quality evaluation (a Quality owner evaluates)
```

**Where the implementation lands.** The frozen subsystems `agent` and `skill`
exist in `native_core/core/`. **Neither corresponds to PD-06 by name.** The
correspondence map records that absence as expected, not as a gap. No binding
is drawn.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/C8.md` — "Masing-masing tetap memiliki responsibility yang berbeda."
- Reference: `docs/architecture/platform-organization/IMPLEMENTATION-CORRESPONDENCE-MAP.md` — "`PD-06` AI Engineering"

## C2. Candidate section structure

**Dimension:** — · **Class:** UNKNOWN

ACT-003 gives PD-06 no section list, only a scope, so there is no candidate
list to measure. The Part C section structure is unknown. It is left open,
not filled by symmetry with other volumes (v1.1 `§9`, `§17`).

- Reference: `docs/governance/acts/ACT-CC-POST-P13-PLATFORM-ORG-003-PLATFORM-ORGANIZATION-CONSTRUCTION-AND-CANONICALIZATION.md` — "Part C SHALL establish the engineering architecture required for:"
- Unknown: the section structure of PD-06 Part C
- Reserved: C6-A1

## C3. Integration

**Dimension:** Integration · **Class:** DOMAIN-ADAPTATION

| Edge | Evidence | Standing |
|---|---|---|
| PD-02 ↔ PD-06 | A6: *AI Engineering · AI Engineering Owner · Architectural Interface* | sourced |
| PD-04 → PD-06 | `X-04`, stated only in PD-04's non-resident corpus | declared, interface undefined |
| PD-06 → Quality | C8 §18 shared-responsibility chain | sourced (the Quality owner is unbound, `FDP-P10-002`) |
| PD-05 ↔ PD-06 | none | unknown |

- Source: `docs/architecture/volume-2/pd-02-architecture-office/A6.md` — "AI Engineering AI Engineering Owner Architectural Interface"
- Reference: `docs/architecture/platform-organization/CROSS-PD-INTERFACE-REGISTRY.md` — "`Primary Dependencies: AI Engineering`"
- Reserved: ADP-P10-001, FDP-P10-002

---

# Part D — Operating

## D1. Operation

**Dimension:** Operation · **Class:** BOUNDED-RECONSTRUCTION

A **candidate** operating cycle, bounded by the sourced chain in C1:

```text
receive architecture standard → implement → submit to architectural review
      → hand to evaluation → integrate
```

Two rules come from the sources:
- architectural review is PD-02's (AT-03), and PD-02 cannot compel the
  execution;
- evaluation is not PD-06's.

The cycle's internal steps are reconstruction.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/B4.md` — "AT-03 owns architectural review."

## D2. Lifecycle

**Dimension:** Lifecycle · **Class:** SOURCE-DERIVED

- **The division.** Creation, retirement and naming are architect approval.
- **Its Agent Definitions.** They are at PD-06's discretion within Capability
  governance, and each is versioned and bound to the Capability contract version
  it implements.

- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "Created/retired via architectural decision, architect approval"
- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "Its version is bound to the Capability contract version it implements."

---

# Part E — Performance & Evolution

## E1. Performance

**Dimension:** Performance · **Class:** BOUNDED-RECONSTRUCTION

**Candidate** measures, inheriting PD-02's framework without its metrics:
- conformance of implementation to the architecture standard;
- Agent Definitions each implementing at least one Capability;
- no Capability with zero active implementing Agent Definitions left
  unflagged.

The last is a Domain Model rule: such a state *"must be flagged for
governance review"*. No threshold is set.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/E3.md` — "framework dapat diwariskan ke PD-03 hingga PD-10 tanpa memaksakan metric PD-02."
- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "must be flagged for governance review"

## E2. Evolution

**Dimension:** Evolution · **Class:** DOMAIN-ADAPTATION

AI Engineering evolves by implementing architecture that changes through
PD-02's change control. Controlling architecture change does not make PD-02
the implementation owner (D8, translated). Model optimization is not an AIOS entity (Freeze
§10), so it is not an evolution path this volume opens.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/D8.md` — "PD-02 tidak menjadi implementation owner hanya karena mengontrol architecture change."
- Source: `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md` — "**Model-optimization** — external concern; not an AIOS entity"
- Reserved: FRZ-10

---

## R1. Reserved and unknown register

**Dimension:** — · **Class:** RESERVED-DECISION

| Item | Holder | Effect here |
|---|---|---|
| `C6-A1` | Architect | the Part arrangement and Part C structure stay open (S1, C2) |
| `DM-6`, `DM-8`, `G-10` | Architect | no Capability and no internal unit created (B1, B2) |
| `ADP-P10-001` | Architect | X-04 exposure not evaluated |
| `FDP-P10-002` | Founder | the Quality owner in the C8 chain is unbound |
| `FRZ-10` | Architect | model optimization stays outside the domain |
| `G-01` | Founder | constructed, not a supplied canonical corpus |

- Reserved: C6-A1, DM-6, DM-8, G-10, ADP-P10-001, FDP-P10-002, FRZ-10, G-01
- Unknown: the scope of "PD-06 owns implementation"
- Unknown: whether the frozen A5 "AI Engineering owner" role is PD-06
- Unknown: the PD-05 ↔ PD-06 boundary
