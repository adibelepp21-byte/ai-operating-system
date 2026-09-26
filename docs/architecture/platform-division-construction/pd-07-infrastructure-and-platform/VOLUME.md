# PD-07 — Infrastructure & Platform · Construction Volume v0.1

| Field | Value |
|---|---|
| **CPID** | `PD-07` |
| **Name** | Infrastructure & Platform |
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
- ACT-003's Part C list is a candidate. Section C2 measures it and finds that
  several of its sections fall inside architecture the Freeze reserves to the
  Architect.
- Certified as the canonical construction baseline by `FD-PO-004` D1-A.
  Certification preserves every class. It resolves no UNKNOWN or
  RESERVED-DECISION section, and freezes and activates nothing.
  Statements of status inside sections describe the state at construction.

---

## S1. Volume structure

**Dimension:** — · **Class:** INHERITED-PATTERN

The volume inherits PD-01's Part arrangement, not its content. The
arrangement is provisional pending `C6-A1`.

- Reference: `docs/architecture/volume-1/pd-01-executive-office/A1.md` — "Part A — Platform Identity & Strategic Foundation"
- Reserved: C6-A1

---

# Part A — Identity & Mandate

## A1. Identity

**Dimension:** Identity · **Class:** SOURCE-DERIVED

`PD-07` is the permanent identifier. The registry names it *Infrastructure &
Platform*, and the frozen architectural boundary names its domain
*Infrastructure*.

**One reading of "Platform" is excluded.** It cannot mean a `Platform`
entity. The Domain Model treats Platform as an *"exposure/maturity posture of a
Capability"*, not a structural concept. Whether the name denotes one domain or
two stays unknown (R1).

- Source: `docs/program/AIOS_MASTER_ROADMAP_CONSOLIDATED_v1.0.md` — "`PD-07` Infrastructure & Platform"
- Source: `docs/architecture/volume-2/pd-02-architecture-office/A4.md` — "├── PD-07 Infrastructure"
- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "exposure/maturity postures of a Capability, not new structural concepts."

## A2. Boundary

**Dimension:** Boundary · **Class:** SOURCE-DERIVED

The boundary against architecture is stated in prose:
- PD-02 has an architectural *dependency* on Infrastructure;
- PD-07 *retains* ownership of Infrastructure;
- PD-02 may not hold infrastructure execution;
- the Infrastructure owner stays accountable for the implementation domain
  (C8 §34).

A second boundary binds this division as no other is bound: *"infrastructure
facilities are never independent actors — not for tracing, not for
governance, not for authority."* The division may own a domain. The
facilities in that domain are never actors.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/C8.md` — "PD-02 memiliki architectural dependency terhadap Infrastructure."
- Source: `docs/architecture/volume-2/pd-02-architecture-office/C8.md` — "PD-07 tetap memiliki ownership atas Infrastructure."
- Source: `docs/architecture/volume-2/pd-02-architecture-office/A3.md` — "memiliki infrastructure execution;"
- Source: `docs/architecture/volume-2/pd-02-architecture-office/C8.md` — "Infrastructure owner tetap accountable terhadap implementation domain."
- Source: `docs/architecture/history/AIOS_INFRASTRUCTURE_AUDITING_PRINCIPLE_REVIEW_v1.0.md` — "infrastructure facilities are never independent actors — not for tracing, not for governance, not for authority."

## A3. Authority

**Dimension:** Authority · **Class:** DOMAIN-ADAPTATION

**Held: infrastructure execution.** PD-02 holds none of it.

**Not held: governance.** *"Infrastructure serves; it does not govern."*
Whatever authority PD-07 holds as a division never passes to a facility.

ACT-003 speaks of *"infrastructure/platform authority"*. No resident source
states such an authority beyond execution and domain ownership, so none is
constructed.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/A5.md` — "Infrastructure Execution NONE Infrastructure owner"
- Source: `docs/engineering/infrastructure/infrastructure_spec.md` — "Infrastructure serves; it does not govern."
- Reference: `docs/governance/acts/ACT-CC-POST-P13-PLATFORM-ORG-003-PLATFORM-ORGANIZATION-CONSTRUCTION-AND-CANONICALIZATION.md` — "PD-07 shall establish infrastructure/platform authority and foundational services."

## A4. Ownership

**Dimension:** Ownership · **Class:** SOURCE-DERIVED

PD-07 retains ownership of the Infrastructure **domain**. Its entity ownership
is what any division's is: Capabilities and Agent Definitions.

**Tool** is *"owned centrally"*, although it is the only entity allowed a
direct external dependency. So the division that owns the Infrastructure domain
does not own the Tool entity.

Facility state is *"non-entity"*: there is nothing in it to own as an entity.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/C8.md` — "PD-07 tetap memiliki ownership atas Infrastructure."
- Source: `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md` — "**the only entity permitted a direct external/vendor dependency** (INV-12). *Ownership*: owned centrally."
- Source: `docs/engineering/infrastructure/infrastructure_spec.md` — "Facility-level state (storage handles, substrate) — non-entity."

---

# Part B — Organization & Capability

## B1. Capability

**Dimension:** Capability · **Class:** BOUNDED-RECONSTRUCTION

**Candidate Capability areas**, from the infrastructure specification's
responsibilities:

| Candidate area | Grounding |
|---|---|
| Persistence facilities | *"Provide persistence facilities under Trace/Memory/Knowledge"* |
| Execution substrate | *"provide the execution substrate"* |
| External-boundary confinement | *"Confine all external/vendor coupling to the Tool boundary (INV-12)"* |

None is a ratified Capability (`DM-6`). *"Foundational platform services"*
beyond these is not enumerated by any resident source.

- Source: `docs/engineering/infrastructure/infrastructure_spec.md` — "Provide persistence facilities under Trace/Memory/Knowledge; provide the execution substrate."
- Source: `docs/engineering/infrastructure/infrastructure_spec.md` — "Confine all external/vendor coupling to the Tool boundary (INV-12)."
- Reserved: DM-6

## B2. Internal organization

**Dimension:** — · **Class:** RESERVED-DECISION

No internal unit is constructed. The Spine is three levels (`DM-8`), and
internal Capability ownership is open (`G-10`). The B1 areas are work areas
only.

- Reserved: DM-8, G-10

---

# Part C — Domain Architecture

## C1. Architecture

**Dimension:** Architecture · **Class:** SOURCE-DERIVED

Infrastructure sits **beneath** the entities:

```text
Agent Instance action
      ↓ invokes
facility (storage · execution substrate · Tool boundary)
      ↓ accountable only through the invoking action
no independent Trace · no governance decision · no authority
```

It exposes storage to the substrate subsystems, the Tool boundary for
external access, and the execution substrate to Runtime. It exposes no
governance capability.

- Source: `docs/engineering/infrastructure/infrastructure_spec.md` — "Infrastructure provides facilities *beneath* the entities"
- Source: `docs/engineering/infrastructure/infrastructure_spec.md` — "Exposes **no** external access outside Tool (INV-12) and **no** governance capability."
- Reference: `docs/architecture/platform-organization/IMPLEMENTATION-CORRESPONDENCE-MAP.md` — "`infrastructure` (layer 9)"

## C2. Candidate section structure

**Dimension:** — · **Class:** RESERVED-DECISION

**CANDIDATE — not source.** ACT-003 lists C1 *Infrastructure Architecture
Constitution* … C10 *Infrastructure Architecture Success*. Measured against the
Freeze:

| Candidate | Standing |
|---|---|
| C3 Compute Architecture | touches **Deployment** and **Scaling**: Architect-reserved (Freeze §10) |
| C4 Storage Architecture | persistence facilities are sourced; **Database implementation** is Architect-reserved |
| C5 Network / Service Architecture | **Networking** is Architect-reserved |
| C9 Infrastructure Reliability Architecture | **Observability implementation** is Architect-reserved |
| C6 Resource Architecture | **Resource** is a reserved concept with no ratified entity (Freeze §2) |
| C7 Platform Service Architecture | "Platform" is not a structural concept (A1) |
| C1, C2, C8, C10 | no resident source beyond C1 above |

**Five of the ten candidate sections fall wholly or partly inside reserved
architecture or reserved concepts.** Building them would design what the Freeze reserves. So the
structure is not adopted, and those sections stay reserved.

- Reference: `docs/governance/acts/ACT-CC-POST-P13-PLATFORM-ORG-003-PLATFORM-ORGANIZATION-CONSTRUCTION-AND-CANONICALIZATION.md` — "C3 Compute Architecture"
- Source: `docs/engineering/infrastructure/infrastructure_spec.md` — "Identity, Authentication, Networking, Database implementation, Deployment, Scaling, Observability implementation — each named as a boundary, **not defined**, reserved to the Architect."
- Source: `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md` — "Resource, Artifact, Task, Goal, Event, Checkpoint, Permission, Policy"
- Reserved: FRZ-10, FRZ-2, C6-A1

## C3. Integration

**Dimension:** Integration · **Class:** SOURCE-DERIVED

The integration edges are sourced from the infrastructure specification:
- **Trace, Memory and Knowledge** use it for storage.
- **Runtime** uses it as its substrate.
- **Agent Instances** use it through Tool.

On the architecture side, the A6 map records an Architectural Interface
between PD-02 and the Infrastructure owner.

- Source: `docs/engineering/infrastructure/infrastructure_spec.md` — "Used by Trace/Memory/Knowledge (storage), Runtime (substrate), and Agent Instances (Tool)."
- Source: `docs/architecture/volume-2/pd-02-architecture-office/A6.md` — "Infrastructure Infrastructure Owner Architectural Interface"

---

# Part D — Operating

## D1. Operation

**Dimension:** Operation · **Class:** SOURCE-DERIVED

A facility is provisioned, used within an action, and released. It is
*"always subordinate to the invoking action"*.

A failed facility fails closed: the invoking action halts accountably, and
external failures surface through the Tool boundary, not silently.

- Source: `docs/engineering/infrastructure/infrastructure_spec.md` — "Facilities are provisioned, used within actions, and released — always subordinate to the invoking action."
- Source: `docs/engineering/infrastructure/infrastructure_spec.md` — "a failed facility causes the invoking action to halt accountably"

## D2. Lifecycle

**Dimension:** Lifecycle · **Class:** SOURCE-DERIVED

- **The division.** Created, retired and named by architect approval.
- **Its Agent Definitions.** At its discretion, within Capability governance.
- **Facilities.** Provisioned, used and released: this is the facility
  lifecycle in D1, not an entity lifecycle.

- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "Created/retired via architectural decision, architect approval"
- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "created/deprecated at Platform Division discretion within Capability governance"

---

# Part E — Performance & Evolution

## E1. Performance

**Dimension:** Performance · **Class:** BOUNDED-RECONSTRUCTION

**Candidate** measures, inheriting PD-02's framework without its metrics:
- **Fail-closed conformance.** A failed facility halts the invoking action.
- **External-coupling confinement.** No non-Tool external dependency.
- **Actor-freedom.** No facility produces independent Trace, makes a
  governance decision or holds authority.

Availability and scaling measures are not constructed: they sit inside
reserved Scaling and Observability implementation. No threshold is set.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/E3.md` — "framework dapat diwariskan ke PD-03 hingga PD-10 tanpa memaksakan metric PD-02."
- Reserved: FRZ-10

## E2. Evolution

**Dimension:** Evolution · **Class:** SOURCE-DERIVED

The sanctioned extension is **new Tools**, for external capability. Storage
and substrate backends are replaceable beneath the entities. Everything
Freeze §10 names stays reserved until the Architect decides it.

- Source: `docs/engineering/infrastructure/infrastructure_spec.md` — "New Tools (external integrations) are the sanctioned extension for external capability."
- Source: `docs/engineering/infrastructure/infrastructure_spec.md` — "Storage/substrate backends are replaceable beneath the entities."

---

## R1. Reserved and unknown register

**Dimension:** — · **Class:** RESERVED-DECISION

| Item | Holder | Effect here |
|---|---|---|
| `FRZ-10` | Architect | Compute (Deployment, Scaling), Networking, Database implementation and Observability implementation not designed (C2, E1) |
| `FRZ-2` | Architect | Resource not designed: a reserved concept (C2) |
| `C6-A1` | Architect | the Part arrangement is provisional |
| `DM-6`, `DM-8`, `G-10` | Architect | no Capability and no internal unit created |
| `G-01` | Founder | constructed, not a supplied canonical corpus |

- Reserved: FRZ-10, FRZ-2, C6-A1, DM-6, DM-8, G-10, G-01
- Unknown: whether "Infrastructure & Platform" names one domain or two
- Unknown: what "foundational platform services" enumerates beyond B1
- Unknown: the PD-05 ↔ PD-07 boundary where runtime meets substrate
