# PD-08 — Security · Construction Volume v0.1

| Field | Value |
|---|---|
| **CPID** | `PD-08` |
| **Name** | Security |
| **Construction status** | CONSTRUCTED — NOT CANONICAL |
| **Canonical** | NO |
| **Frozen** | NO |
| **Activated** | NO |
| **Authority** | `ACT-CC-POST-P13-PLATFORM-ORG-003` as amended by v1.1, authorized for execution by `FD-PO-003-01` (construction *"AUTHORIZED WITH BOUNDARY"*) |
| **Binding** | Security Owner → PD-08 is **not made**: `FDP-P10-001`, Founder-reserved and open |
| **Verifier** | `tools/platform_division_construction.py` |

**How to read this volume.**
- The frozen corpus defines a **Security owner** role in detail. It never
  states which division holds it.
- This volume keeps the two apart:
  - it describes the Security **domain** and the role's sourced properties;
  - it attributes neither to PD-08.
- The binding is the Founder's (`FDP-P10-001`). Under the Founder's P12
  policy D2 it is conditional-blocking: only work that depends on the binding
  waits. That is A3 and A4. The rest proceeds (v1.1 `§16` F-3).
- Nothing here is canonical, frozen or activated.

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

`PD-08` is the permanent identifier. The registry and the frozen architectural
boundary both use the name *Security*. The boundary diagram's entry is a
label, not an ownership statement.

- Source: `docs/program/AIOS_MASTER_ROADMAP_CONSOLIDATED_v1.0.md` — "`PD-08` Security"
- Source: `docs/architecture/volume-2/pd-02-architecture-office/A4.md` — "├── PD-08 Security"

## A2. Boundary

**Dimension:** Boundary · **Class:** SOURCE-DERIVED

The Security domain's boundary against architecture is sourced:
- PD-02 may not take over security authority, even by Architecture Override;
- PD-02 may not take over security execution;
- Security can be an **architectural interface**: PD-02 may set architectural
  requirements within its own domain authority, while the Security owner keeps
  security domain responsibility.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/A5.md` — "mengambil alih security authority;"
- Source: `docs/architecture/volume-2/pd-02-architecture-office/A3.md` — "mengambil alih security execution;"
- Source: `docs/architecture/volume-2/pd-02-architecture-office/C8.md` — "PD-02 dapat menetapkan architectural requirements dalam domain authority."
- Source: `docs/architecture/volume-2/pd-02-architecture-office/C8.md` — "Security owner tetap memiliki security domain responsibility."

## A3. Authority

**Dimension:** Authority · **Class:** RESERVED-DECISION

**The role's sourced properties.** The Security owner holds Security Execution;
PD-02 holds none of it.

**Whether PD-08 holds that execution and that responsibility** is the binding
question `FDP-P10-001`: the Founder binds the role to PD-08 or records
deliberate non-binding. Until then, this volume gives PD-08 **no** security
authority.

A division's identity is not proof of authority (ACT-003 `§5.3`, a reference).

- Source: `docs/architecture/volume-2/pd-02-architecture-office/A5.md` — "Security Execution NONE Security owner"
- Source: `docs/architecture/platform-organization/POST-P10-TRANSITION-REGISTER.md` — "Bind `Security Owner → PD-08`, or record deliberate non-binding"
- Reference: `docs/governance/acts/ACT-CC-POST-P13-PLATFORM-ORG-003-PLATFORM-ORGANIZATION-CONSTRUCTION-AND-CANONICALIZATION.md` — "PD-08 identity SHALL NOT itself be treated as proof of authority."
- Reserved: FDP-P10-001

## A4. Ownership

**Dimension:** Ownership · **Class:** RESERVED-DECISION

A5 names the Security owner as the holder of security domain responsibility.
PD-08's ownership of the Security **domain** follows only if the role is bound
to PD-08, which is `FDP-P10-001`.

**What holds either way.** As a division, PD-08 would own only Capabilities and
Agent Definitions. *Permission* is a reserved concept with no ratified entity,
so there is no permission entity to own.

- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "1. Every Capability is owned by exactly one Platform Division."
- Source: `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md` — "**Reserved concepts** with no ratified entity"
- Reserved: FDP-P10-001, FRZ-2

---

# Part B — Organization & Capability

## B1. Capability

**Dimension:** Capability · **Class:** BOUNDED-RECONSTRUCTION

**Candidate areas.** They come from the established construction target
(*architecture, access, protection, controls*), cut back by what the Freeze
reserves:

| Candidate area | Standing |
|---|---|
| Security architecture, as an architectural interface with PD-02 | supported (C8 §35) |
| Protection of the load-bearing walls: the Tool boundary and the Human-Authority boundary | supported (Freeze §8); cross-cutting, not owned |
| Access | **reserved**: Identity and Authentication are deferred architecture; Permission is a reserved concept |
| Controls | unknown: may overlap PD-03's compliance controls |

None is a ratified Capability (`DM-6`).

- Source: `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md` — "**Tool boundary** — all external/vendor coupling passes through Tool alone (INV-12)."
- Source: `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md` — "**Identity** (as a general/auth concept), **Authentication**, **Networking**, **Deployment**, **Scaling** — no ratified entity"
- Reserved: DM-6, FRZ-10, FRZ-2

## B2. Internal organization

**Dimension:** — · **Class:** RESERVED-DECISION

No internal unit is constructed (`DM-8`, `G-10`).

- Reserved: DM-8, G-10

---

# Part C — Domain Architecture

## C1. Architecture

**Dimension:** Architecture · **Class:** SOURCE-DERIVED

The domain's sourced architecture is the three-layer interface:

```text
Architecture
     ↕
Security Architecture
     ↕
Security Domain
```

Two frozen walls are security-relevant and **cross-cutting**. No division owns
them, and they cannot be bypassed:
- the **Tool boundary**: external coupling only through Tool;
- the **Human-Authority boundary**: automation may request, recommend or
  detect; it may not decide governance.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/C8.md` — "Security dapat menjadi architectural interface."
- Source: `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md` — "**Human-Authority boundary** — automation may request/recommend/detect; it may not decide governance or override it"

## C2. Candidate section structure

**Dimension:** — · **Class:** RESERVED-DECISION

**CANDIDATE — not source.** ACT-003 lists C1 *Security Architecture
Constitution* … C10 *Security Architecture Success*. Measured:

| Candidate | Standing |
|---|---|
| C3 Identity & Access Architecture | **Identity** and **Authentication** are Architect-reserved (Freeze §10); **Permission** is a reserved concept (Freeze §2) |
| C6 Security Context Architecture | **Context** is a reserved concept (Freeze §2) |
| C8 Security Integrity & Governance Interface | supported as an interface only: the Security ↔ Architecture interface (C8 §35). The Governance side is PD-03's, non-resident, and its authority unbound (`FDP-P10-003`) |
| C4 Protection, C5 Security Control, C7 Detection / Response | no resident source; *detect* is sourced only as a limit on automation (Freeze §8) |
| C1, C2, C9, C10 | no resident source |

Two candidates fall in reserved architecture, and one is only an interface.
The list is not adopted.

- Reference: `docs/governance/acts/ACT-CC-POST-P13-PLATFORM-ORG-003-PLATFORM-ORGANIZATION-CONSTRUCTION-AND-CANONICALIZATION.md` — "C3 Identity & Access Architecture"
- Reserved: FRZ-10, FRZ-2, FDP-P10-003, C6-A1

## C3. Integration

**Dimension:** Integration · **Class:** DOMAIN-ADAPTATION

| Edge | Evidence | Standing |
|---|---|---|
| PD-02 ↔ Security owner | A6: *Security · Security Owner · Architectural Interface* | sourced; the owner unbound |
| PD-03 → PD-08 | `X-02`, stated only in PD-03's non-resident corpus | declared, interface undefined |
| PD-03 controls ↔ PD-08 controls | none | unknown |

- Source: `docs/architecture/volume-2/pd-02-architecture-office/A6.md` — "Security Security Owner Architectural Interface"
- Reference: `docs/architecture/platform-organization/CROSS-PD-INTERFACE-REGISTRY.md` — "`PRIMARY DEPENDENCIES: Security`"
- Reserved: ADP-P10-001, ESC-C7-01

---

# Part D — Operating

## D1. Operation

**Dimension:** Operation · **Class:** UNKNOWN

No resident source describes how security is operated. A security operating
model authored without source is a security design from nothing. So it is left
unknown, not reconstructed. The only operating limits that are sourced are
general:
- automation may detect but may not decide governance;
- external coupling passes through Tool.

- Unknown: how the Security domain is operated
- Source: `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md` — "**Human-Authority boundary** — automation may request/recommend/detect; it may not decide governance or override it"

## D2. Lifecycle

**Dimension:** Lifecycle · **Class:** SOURCE-DERIVED

- **The division.** Created, retired and named by architect approval.
- **Its Agent Definitions.** At its discretion, within Capability governance.

The binding in A3 has its own lifecycle: it is the Founder's to make.

- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "Created/retired via architectural decision, architect approval"
- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "created/deprecated at Platform Division discretion within Capability governance"

---

# Part E — Performance & Evolution

## E1. Performance

**Dimension:** Performance · **Class:** UNKNOWN

Security performance is not reconstructed: measuring a security posture that
has no sourced operating model would invent both. The PD-02 framework may be
inherited without its metrics once D1 has a source.

- Unknown: security performance measures
- Source: `docs/architecture/volume-2/pd-02-architecture-office/E3.md` — "framework dapat diwariskan ke PD-03 hingga PD-10 tanpa memaksakan metric PD-02."

## E2. Evolution

**Dimension:** Evolution · **Class:** RESERVED-DECISION

The domain can evolve only through two decisions:
- **the Founder's binding decision** (`FDP-P10-001`);
- **the Architect's deferred architecture** (Identity, Authentication:
  `FRZ-10`).

Nothing here pre-empts either.

- Reserved: FDP-P10-001, FRZ-10

---

## R1. Reserved and unknown register

**Dimension:** — · **Class:** RESERVED-DECISION

| Item | Holder | Effect here |
|---|---|---|
| `FDP-P10-001` | Founder | A3, A4, E2: no security authority or domain ownership given to PD-08 |
| `FRZ-10`, `FRZ-2` | Architect | Identity, Authentication, Permission and Context not designed (B1, C2) |
| `FDP-P10-003`, `ESC-C7-01` | Founder | the Governance side of the security interface cannot be read |
| `C6-A1`, `DM-6`, `DM-8`, `G-10`, `ADP-P10-001` | Architect | structure, Capabilities, internal units, cross-division exposure |
| `G-01` | Founder | constructed, not a supplied canonical corpus |

- Reserved: FDP-P10-001, FRZ-10, FRZ-2, FDP-P10-003, ESC-C7-01, C6-A1, DM-6, DM-8, G-10, ADP-P10-001, G-01
- Unknown: whether PD-08 "controls" and PD-03 compliance controls are one boundary
- Unknown: the security operating and performance model
