# PD-10 — (name held open) · Construction Volume v0.1

| Field | Value |
|---|---|
| **CPID** | `PD-10` |
| **Name** | held open — `G-02` (see A1) |
| **Construction status** | CANONICAL CONSTRUCTION BASELINE — CERTIFIED WITH CLASSIFIED RESIDUAL |
| **Canonical** | YES — construction baseline |
| **Certified by** | `FD-PO-004` D1-A (Founder, 2026-09-26; Register `§53`). The sections below are those verified at `5eb0eec`, unchanged; every section keeps its class (`CANONICAL-BASELINE-MANIFEST.json`) |
| **Frozen** | NO |
| **Activated** | NO |
| **Authority** | `ACT-CC-POST-P13-PLATFORM-ORG-003` as amended by v1.1, authorized for execution by `FD-PO-003-01` (construction *"AUTHORIZED WITH BOUNDARY"*) |
| **Verifier** | `tools/platform_division_construction.py` |

**How to read this volume.**
- The division is constructed under its stable identifier, `PD-10`. No final
  name is manufactured (v1.1 `§13`).
- Two names occur in resident sources. Where the text needs to refer to the
  domain, it says **the developer-facing domain**.
- Work that does not depend on the name proceeds. Work whose content the name
  would change is held.
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

**Dimension:** Identity · **Class:** RESERVED-DECISION

`PD-10` is the permanent identifier, and the identity anchor while the name is
open.

**The divergence is wider than `G-02` records.** `G-02` records two sides: the
frozen PD-02 corpus says *Developer Enablement*, and the registry says
*Developer Experience*. But the frozen corpus itself uses both names:

| Name | Where it occurs |
|---|---|
| *Developer Enablement* | frozen PD-02 A4, A6 and B1; its A6 ownership map has a *"Developer Enablement Owner"* |
| *Developer Experience* | frozen PD-02 D7 §69; the registry |

So a rule of the form "the frozen corpus governs" would not by itself settle
the name. This is recorded as evidence for `G-02`. It is not resolved.

**Who holds the decision is itself divided:**
- the gap map says the Founder (which source governs naming);
- the Domain Model makes naming a division architect approval.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/A4.md` — "└── PD-10 Developer Enablement"
- Source: `docs/architecture/volume-2/pd-02-architecture-office/D7.md` — "* Developer Experience."
- Source: `docs/program/AIOS_MASTER_ROADMAP_CONSOLIDATED_v1.0.md` — "`PD-10` Developer Experience"
- Source: `docs/architecture/platform-organization/SYSTEMIC-GAP-MAP.md` — "## G-02 — `PD-10` carries two different names in resident sources"
- Reserved: G-02, DM-6

## A2. Boundary

**Dimension:** Boundary · **Class:** SOURCE-DERIVED

This boundary does not depend on the name:
- **PD-02 may not use its internal structure to take ownership of the
  developer-facing domain.** B1 lists it among the domains that have their own
  primary owners.
- **PD-02 may collaborate with the domain.** Collaboration depends on
  architectural impact, and domain ownership stays with the platform concerned.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/B1.md` — "PD-02 dapat memiliki architectural interfaces terhadap domain tersebut tanpa menjadi organizational owner-nya."
- Source: `docs/architecture/volume-2/pd-02-architecture-office/D7.md` — "Domain ownership tetap berada pada Platform terkait."

## A3. Authority

**Dimension:** Authority · **Class:** UNKNOWN

No resident source states an authority for the developer-facing domain.
PD-02's A5 execution table, which names the owner roles of the other domains,
has no row for it. Nothing is constructed.

- Unknown: any authority held by PD-10

## A4. Ownership

**Dimension:** Ownership · **Class:** SOURCE-DERIVED

The frozen A6 ownership map lists the domain with its own *owner* and marks
PD-02's relation to it as an **Architectural Dependency**, not an interface.
PD-02 depends on the domain; it does not own it.

**Whether that owner is PD-10 is suggested by the boundary diagram and not
stated.** As a division, PD-10 owns only Capabilities and Agent Definitions.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/A6.md` — "Developer Enablement Developer Enablement Owner Architectural Dependency"
- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "1. Every Capability is owned by exactly one Platform Division."

---

# Part B — Organization & Capability

## B1. Capability

**Dimension:** Capability · **Class:** RESERVED-DECISION

The established construction target is *SDK, CLI, API, tooling,
documentation*. The two names weight it differently:
- *Enablement* suggests capability provision;
- *Experience* suggests interface quality.

So the Capability areas depend on `G-02` and are not cut. No Capability is
created in any case (`DM-6`).

- Reference: `docs/governance/acts/ACT-CC-POST-P13-PLATFORM-ORG-003-PLATFORM-ORGANIZATION-CONSTRUCTION-AND-CANONICALIZATION.md` — "PD-10 shall establish the developer-facing platform interface."
- Reserved: G-02, DM-6

## B2. Internal organization

**Dimension:** — · **Class:** RESERVED-DECISION

No internal unit is constructed (`DM-8`, `G-10`).

- Reserved: DM-8, G-10

---

# Part C — Domain Architecture

## C1. Architecture

**Dimension:** Architecture · **Class:** BOUNDED-RECONSTRUCTION

One architectural constraint holds under either name: **every external or
vendor coupling passes through Tool** (INV-12). A developer-facing surface that
reaches outside AIOS is therefore a Tool concern, not a new boundary.

**Resident developer-facing surface.** AIOS already has one: `tools/`, the
governance index, the conformance suites and the documentation corpus.

**None of it is bound to PD-10**, and no binding is drawn: correspondence is
not ownership. If a binding is later made, the existing mutual-isolation guards
between `tools/` and `consumers/` become a constraint on this domain.

- Source: `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md` — "**Tool boundary** — all external/vendor coupling passes through Tool alone (INV-12)."
- Reference: `docs/architecture/platform-organization/IMPLEMENTATION-CORRESPONDENCE-MAP.md` — "`PD-10` Developer Experience"

## C2. Candidate section structure

**Dimension:** — · **Class:** UNKNOWN

ACT-003 gives PD-10 a scope, not a section list, and says *"The exact section
names SHALL be source-derived before freeze."* No resident source supplies
them. Left unknown.

- Reference: `docs/governance/acts/ACT-CC-POST-P13-PLATFORM-ORG-003-PLATFORM-ORGANIZATION-CONSTRUCTION-AND-CANONICALIZATION.md` — "The exact section names SHALL be source-derived before freeze."
- Unknown: the Part C section structure of PD-10
- Reserved: C6-A1

## C3. Integration

**Dimension:** Integration · **Class:** SOURCE-DERIVED

| Edge | Evidence |
|---|---|
| PD-02 → developer-facing domain | A6: Architectural Dependency |
| PD-02 ↔ developer-facing domain | D7 §69: collaboration, depending on architectural impact |

No other division states an edge to PD-10.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/A6.md` — "Developer Enablement Developer Enablement Owner Architectural Dependency"
- Source: `docs/architecture/volume-2/pd-02-architecture-office/D7.md` — "Collaboration bergantung pada architectural impact."

---

# Part D — Operating

## D1. Operation

**Dimension:** Operation · **Class:** UNKNOWN

No resident source describes the domain's operation. An operating model of an
interface surface authored without source would be invention. Left unknown.

- Unknown: how the developer-facing domain is operated

## D2. Lifecycle

**Dimension:** Lifecycle · **Class:** SOURCE-DERIVED

- **The division.** Its creation, retirement and **naming** are architect
  approval. That is why the name in A1 is not settled here.
- **Its Agent Definitions.** At its discretion, within Capability governance.

- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "Created/retired via architectural decision, architect approval"
- Source: `docs/architecture/domain-model/canonical-domain-model-v1.md` — "created/deprecated at Platform Division discretion within Capability governance"

---

# Part E — Performance & Evolution

## E1. Performance

**Dimension:** Performance · **Class:** RESERVED-DECISION

This is the clearest practical cost of `G-02`:
- under *Experience*, performance would be developer outcomes;
- under *Enablement*, capability coverage.

Held until the name is decided. The PD-02 framework may be inherited without
its metrics either way.

- Source: `docs/architecture/volume-2/pd-02-architecture-office/E3.md` — "framework dapat diwariskan ke PD-03 hingga PD-10 tanpa memaksakan metric PD-02."
- Reserved: G-02

## E2. Evolution

**Dimension:** Evolution · **Class:** DOMAIN-ADAPTATION

The developer-facing domain evolves with the architecture it exposes, under
PD-02's change control. External reach grows only by new Tools, the sanctioned
extension.

- Source: `docs/engineering/infrastructure/infrastructure_spec.md` — "New Tools (external integrations) are the sanctioned extension for external capability."

---

## R1. Reserved and unknown register

**Dimension:** — · **Class:** RESERVED-DECISION

| Item | Holder | Effect here |
|---|---|---|
| `G-02` | Founder / Architect | name held open (A1); Capability areas (B1) and performance (E1) not cut |
| `DM-6` | Architect | naming and Capabilities are architect approval |
| `C6-A1`, `DM-8`, `G-10` | Architect | structure and internal units |
| `G-01` | Founder | constructed, not a supplied canonical corpus |

- Reserved: G-02, DM-6, C6-A1, DM-8, G-10, G-01
- Unknown: authority held by PD-10
- Unknown: whether the frozen A6 "Developer Enablement Owner" is PD-10
- Unknown: whether "documentation" includes the governance corpus
