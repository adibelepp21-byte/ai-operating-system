<!-- PROVENANCE BLOCK — added at persistence, NOT part of the supplied artifact. -->

> # ISSUED — Architect Decision, 2026-09-10
>
> **`§14` OPTION C · `§21` 2026-09-10 · `§22` ISSUED BY ARCHITECT · `§23` STATUS: ISSUED.**
> All five sections `§0` requires — `§14`, `§15`, `§21`, `§22`, `§23` — are complete.
>
> **The decision is the Architect's.** My prepared instrument recommended on
> twelve of sixteen concepts and **declined to recommend on the four unresolved**;
> the Architect decided all four. `§1.1` of the pending instrument warned that
> *"the Architect must not merely approve the Co-Founder recommendation"*, and the
> issued decision does not — **it resolves the contradiction I could only report.**
>
> ---
>
> ## Supersession of the PENDING copy — disclosed
>
> | | `sha256` | Status | `§14` |
> |---|---|---|---|
> | First | `b6ef9669c330…` | `DECISION-PENDING` | unfilled |
> | **Second — operative** | `cfe6c573b032e807…` | **`ISSUED`** | **OPTION C, all four concepts decided** |
>
> **The issued text is a rewrite, not a countersignature** — 17 632 bytes against
> 25 864. The same pattern as `FD-P10-005`: the deliberative scaffolding is
> replaced by a decision taken. **The PENDING copy is preserved in git history**
> and superseded, not deleted.
>
> ---
>
> ## Source verification performed before acting on it
>
> `§3.5` and `§15` rest on a claim about **PD-01**. Verified at source rather
> than accepted:
>
> - **`Governance ≠ Execution`** is in PD-01's own volume —
>   `docs/architecture/volume-1/pd-01-executive-office/A1.md:94` and `A10.md:201`.
> - **All five distinctions together**, verbatim, at
>   `docs/program/AIOS_GAP_CLOSURE_P10_P13_CONSTRUCTION_ROADMAP_v1.0.md:370`:
>   *"Governance ≠ Execution · Authority ≠ Ownership · Delegation ≠ Transfer of
>   Ultimate Accountability · Coordination ≠ Ownership · Compliance ≠ Operational
>   Execution."*
>
> **The claim holds.** One attribution nuance recorded for accuracy: the decision
> attributes the full set to PD-01, and the complete block is resident in the Gap
> Closure Roadmap while PD-01's volume carries part of it. **Both are resident and
> the substance is verified** — this is a citation-precision note, not a defect.
>
> ---
>
> **Supplied by:** Architect · **Persisted by:** Claude Code / Co-Founder
> **Persisted:** 2026-09-10 · **Status (its own):** ISSUED
>
> **VERBATIM COPY.** Recovered from the session transcript, the primary record —
> **not reconstructed**. `sha256` of the recovered body, excluding the single
> trailing newline this file appends:
> `cfe6c573b032e807b61d85ed6c3b9db9c84b30d61cac01d5d05e48569f5dab4d`
>
> ---
>
> ## What this decision does NOT do — from its own text
>
> `§2`: does **not** authorize P11 construction, `E11` ratification, P12
> construction, Native Core modification, a new subsystem, or **DP-03**.
> `§25`: P11 authorization and `E11` ratification **remain separate Founder
> Decisions**; DP-03 **remains a separate Architect Decision**.
> `§26`: `ARCHITECT DECISION ≠ FOUNDER AUTHORIZATION`.

---

ADR / ARCHITECT DECISION

DP-04 — P11 Organizational Entity Model

Document Type: Architect Decision Record
Decision ID: DP-04
Phase: P11 — Autonomous Organization
Status: ISSUED
Decision Authority: Architect
Effective Date: 2026-09-10

⸻

§0 — DECISION STATUS RULE

This document constitutes an actual Architect Decision.

The Architect Decision becomes authoritative upon completion of:

* §14 — Architect Choice
* §15 — Architect Rationale
* §21 — Effective Date
* §22 — Architect Signature
* §23 — Final Status

No implementation may treat a prior recommendation, analysis, candidate model, or decision package as equivalent to this issued decision.

⸻

§1 — EXACT DECISION QUESTION

§1.1

How shall the P11 organizational conceptual model represent Goal, Plan, Delegation, and OrganizationalState while remaining semantically correct, preserving the frozen Native Core boundary, respecting the No-New-Entity constraint, and maintaining the P11 → P12 boundary?

Specifically:

1. Which P11 concepts are canonical organizational concepts?
2. Which concepts are already represented by frozen or implemented AIOS structures?
3. Which concepts are projections rather than independent entities?
4. Which concepts may exist outside Native Core?
5. Does P11 require creation of a new Native Core entity or subsystem?
6. How shall the model preserve authority, accountability, governance, execution, and organizational semantics without silently modifying frozen architecture?

⸻

§2 — DECISION SCOPE

This decision covers the organizational entity/concept model required for P11.

It does NOT:

* authorize P11 construction;
* authorize E11 ratification;
* authorize P12 construction;
* modify the Constitution;
* modify Founder Reserved Authority;
* create a new Founder authority;
* modify the frozen Native Core;
* authorize a new Native Core subsystem;
* decide DP-03;
* authorize runtime implementation by itself.

DP-03 remains a separate Architect Decision and shall consume this decision as authoritative input.

⸻

§3 — AUTHORITATIVE SOURCE BASIS

The decision is based on the verified architectural evidence that:

1. P11 is the Autonomous Organization layer built above the P10 Department Ecosystem.
2. P11 explicitly requires:
    * planning;
    * delegation;
    * execution;
    * coordination;
    * observation;
    * verification;
    * escalation;
    * accountability.
3. P12 is the integration phase for P4–P11 and explicitly owns Unified Operational State.
4. Platform Organization distinguishes authority, ownership, execution, governance, coordination, and delegation.
5. PD-01 establishes the organizational pattern and explicitly preserves:
    * separation of authority and execution;
    * Authority ≠ Ownership;
    * Delegation ≠ Transfer of Ultimate Accountability;
    * Coordination ≠ Ownership;
    * Governance ≠ Execution.
6. The frozen Native Core currently has exactly eleven subsystem boundaries.
7. The verified architectural freeze does not authorize creation of an additional Native Core subsystem through this decision.

P11 requirements are explicitly documented as organizational capabilities, including planning and delegation.

The P12 boundary explicitly assigns Unified Operational State to P12-W2.

PD-01 explicitly establishes the distinction between authority, ownership, delegation, coordination, governance, and execution.

⸻

§4 — CANONICAL RECONCILIATION OF P11 CONCEPTUAL MODEL

The previously verified reconciliation produced:

3 FROZEN
3 IMPLEMENTED
1 PROJECTION
3 NON-ENTITY
6 UNRESOLVED
----------------
16 CONCEPTUAL ITEMS

This 16-item inventory is treated as a conceptual reconciliation surface, not as a requirement that all sixteen become runtime entities.

The phrase “conceptual entity” shall therefore not be interpreted as:

concept mentioned in Blueprint
        ↓
mandatory runtime entity

Instead:

P11 conceptual model
        ↓
semantic classification
        ↓
frozen entity / implemented structure /
projection / non-entity / organizational concept

No entity shall be manufactured merely to make the count complete.

⸻

§5 — FROZEN ENTITY MODEL

The twelve previously verified frozen organizational/core entities remain unchanged.

This decision does NOT:

* rename them;
* split them;
* merge them;
* create successors;
* create a twelfth Native Core subsystem;
* reinterpret the Architecture Freeze.

The existing frozen model remains authoritative.

⸻

§6 — RESERVED CONCEPTS

The following concepts remain architectural concepts requiring explicit semantic placement:

* Goal
* Plan
* Delegation
* OrganizationalState

Their semantic necessity does not by itself constitute authority to create a new Native Core entity.

⸻

§7 — IMPLEMENTED / PROJECTION / NON-ENTITY CLASSIFICATION

The previously verified implementation findings remain valid:

Escalation

Escalation is represented as a ratified Trace status rather than an independent organizational entity.

Observation

Observation is represented through the existing observation publication mechanism.

PerformanceRecord

Performance information is represented through the existing performance/observation mechanism rather than requiring a new Native Core entity.

Organizational State

Organizational state shall not be elevated into a separate P11 Native Core entity.

It shall remain compatible with the P12 Unified Operational State boundary.

⸻

§8 — FOUR UNRESOLVED CONCEPTS

§8.1 Goal

Architect Decision:

Goal is a legitimate P11 organizational concept.

It shall not be created as a new Native Core subsystem/entity.

Its purpose is to represent organizational intent that can be decomposed and translated into plans and executable organizational work.

Therefore:

GOAL
  ↓
P11 ORGANIZATIONAL CONCEPT
  ↓
PLAN

Goal does not create authority by itself.

A Goal cannot:

* expand Founder authority;
* expand constitutional authority;
* self-authorize;
* override governance;
* override architecture;
* create permissions.

⸻

§8.2 Plan

Architect Decision:

Plan is a legitimate P11 organizational concept.

Plan shall exist in the organizational layer outside the frozen Native Core.

Plan represents the structured decomposition and sequencing of organizational work.

Its semantics include:

* decomposition;
* sequencing;
* dependency awareness;
* execution preparation;
* adaptation.

Plan does not constitute authority.

Therefore:

GOAL
  ↓
PLAN
  ↓
DELEGATION
  ↓
EXECUTION

A Plan cannot authorize itself.

⸻

§8.3 Delegation

Architect Decision:

Delegation is a first-class P11 organizational concept represented as a governed organizational relation/record outside the frozen Native Core.

This is the critical architectural decision.

Delegation shall NOT:

* become Governance;
* become Ownership;
* become Execution;
* become a replacement for authority;
* transfer ultimate accountability;
* create authority that does not already exist;
* expand constitutional or Founder authority.

Delegation records:

AUTHORITY SOURCE
        ↓
AUTHORIZED SCOPE
        ↓
DELEGATED ACTOR / UNIT
        ↓
BOUNDARY
        ↓
ACCOUNTABILITY
        ↓
VERIFICATION

The organizational layer may therefore represent:

A delegates B
for capability/work X
within authority boundary Y
under accountability condition Z

without introducing another Native Core subsystem.

This resolves the previously identified architectural conflict.

The correct interpretation is:

Delegation semantics
        ≠
Governance entity
Delegation semantics
        ≠
Execution entity
Delegation semantics
        ≠
new Native Core subsystem

Instead:

P11 ORGANIZATION
       │
       └── DELEGATION RELATION / RECORD
                    │
                    ├── authority boundary
                    ├── scope
                    ├── actor
                    ├── accountability
                    └── verification

This preserves the frozen architecture while retaining semantic correctness.

⸻

§8.4 OrganizationalState

Architect Decision:

OrganizationalState is NOT an independent P11 Native Core entity.

It shall be treated as a bounded organizational state projection whose eventual system-wide representation belongs to the P12 integration model.

Therefore:

P11
ORGANIZATIONAL STATE
        ↓
bounded organizational projection
        ↓
P12 UNIFIED OPERATIONAL STATE

P11 may expose the state necessary for organizational continuity and operation.

P11 shall not independently create a competing system-wide state authority.

⸻

§9 — NO-NEW-ENTITY CONSTRAINT

The No-New-Entity constraint remains in force.

This decision does NOT create:

* Native Core entity #13;
* Native Core subsystem #12;
* Governance subsystem;
* Delegation subsystem inside Native Core;
* independent P11 state subsystem.

The architectural solution is therefore:

SEMANTIC REQUIREMENT
        ↓
ORGANIZATIONAL DOMAIN CONCEPT
        ↓
OUTSIDE FROZEN NATIVE CORE
        ↓
NO NEW CORE SUBSYSTEM

The constraint is preserved without forcing semantic concepts to disappear.

⸻

§10 — P12 BOUNDARY

P11 owns organizational behavior.

P12 owns system-wide integration.

Therefore:

P11
├── Goal
├── Plan
├── Delegation
├── Organizational coordination
├── Organizational execution
├── Organizational observation
└── Organizational performance
              ↓
P12
└── Unified Operational State

P11 must not establish an alternative system-wide operational state that competes with P12.

P12 remains the integration layer for P4–P11.

⸻

§11 — OPTIONS CONSIDERED

Option A — Force all concepts into existing frozen entities

Rejected.

Reason:

It risks semantic distortion, especially for Delegation.

Delegation is not equivalent to Governance, Ownership, Execution, or Coordination.

⸻

Option B — Treat all unresolved concepts as projections

Rejected as a universal solution.

OrganizationalState is appropriately projection-oriented, but treating Goal, Plan, and Delegation merely as incidental projections would weaken the semantic model required by P11.

⸻

Option C — Place required organizational concepts outside Native Core

SELECTED.

This preserves:

* semantic correctness;
* Native Core freeze;
* organizational extensibility;
* P11 scope;
* P12 integration boundary;
* authority separation.

⸻

Option D — Create a new Native Core entity/subsystem

Rejected.

Although Delegation demonstrates genuine semantic requirements, those requirements do not justify modification of the frozen Native Core.

The organizational layer can represent the required semantics without adding another Native Core subsystem.

⸻

§12 — CONSEQUENCE MATRIX

Concern	Consequence
Native Core	Remains frozen
Number of Native Core subsystems	Remains 11
Goal	P11 organizational concept
Plan	P11 organizational concept
Delegation	First-class organizational relation/record
OrganizationalState	Bounded projection; P12 integration concern
Governance	Remains separate
Ownership	Remains separate
Execution	Remains separate
Accountability	Remains attached to delegation/execution semantics
P12	Remains owner of unified system-wide state
DP-03	May now use this decision as authoritative input
P11 construction	Still requires separate Founder authorization
E11	Still requires Founder ratification

⸻

§13 — CO-FOUNDER RECOMMENDATION

The Co-Founder recommendation is accepted in principle where consistent with this decision:

Prefer the minimum canonical surface that preserves semantic correctness.

Architectural interpretation:

Do not create a new frozen-core structure when the required organizational semantics can be represented correctly in the organizational layer.

The recommendation does not itself constitute authority.

This section is subordinate to §14–§23.

⸻

§14 — ARCHITECT CHOICE

THE ARCHITECT CHOOSES OPTION C — ORGANIZATIONAL-LAYER REPRESENTATION OUTSIDE THE FROZEN NATIVE CORE.

Concept-level decisions:

Goal

P11 organizational concept.

Plan

P11 organizational concept.

Delegation

First-class P11 organizational relation/record outside Native Core.

OrganizationalState

Bounded P11 projection with P12 Unified Operational State as the system-wide integration boundary.

No new Native Core entity or subsystem is authorized.

No modification to the Architecture Freeze is authorized.

⸻

§15 — ARCHITECT RATIONALE

The architecture must satisfy two constraints simultaneously:

SEMANTIC CORRECTNESS
        +
ARCHITECTURAL INTEGRITY

Eliminating Delegation as a concept merely to satisfy No-New-Entity would be architecturally incorrect because P11 explicitly requires delegation, authority boundaries, accountability, delegation tracking, and delegation verification.

Conversely, creating a new Native Core subsystem solely because Delegation is semantically important would violate the existing frozen architecture.

The correct solution is therefore a third position:

NOT COLLAPSED
INTO EXISTING CORE ENTITY
AND
NOT ELEVATED
INTO NEW CORE SUBSYSTEM
BUT
REPRESENTED AS
A GOVERNED ORGANIZATIONAL CONCEPT/RELATION
OUTSIDE THE FROZEN CORE

This is especially important because PD-01 explicitly preserves:

Governance ≠ Execution
Authority ≠ Ownership
Delegation ≠ Transfer of Ultimate Accountability
Coordination ≠ Ownership

The decision therefore preserves the architecture rather than weakening it.

⸻

§16 — AFFECTED ARTIFACTS

This decision affects the semantic interpretation of:

1. P11 Roadmap / PRD / Construction Blueprint
2. P11-W2 Organizational Planning
3. P11-W3 Delegation
4. P11-W4 Autonomous Execution
5. P11-W5 Organizational Memory
6. P11-W6 Organizational Performance
7. P11-W7 Human Governance Boundary
8. P11 organizational state model
9. P11 → P12 integration boundary
10. DP-03 architecture placement decision

No frozen Native Core artifact is authorized for mutation by this decision.

⸻

§17 — CONSEQUENCE RULE

After issuance:

DP-04
  ↓
AUTHORITATIVE P11 ENTITY / CONCEPT MODEL
  ↓
DP-03
  ↓
P11 AUTHORIZATION PACKAGE
  ↓
E11 RATIFICATION PACKAGE
  ↓
CONSTRUCTION

DP-03 must treat this decision as authoritative input.

DP-03 shall not reopen the already-decided question of whether Goal, Plan, Delegation, and OrganizationalState are semantically required concepts.

DP-03 may only determine their architectural home/interface according to the remaining DP-03 question.

⸻

§18 — NEGATIVE CONTROLS

The following transformations are prohibited:

Delegation
   ↓
Governance authority
Delegation
   ↓
Transfer of ultimate accountability
Goal
   ↓
Self-authorization
Plan
   ↓
Automatic authority
Performance
   ↓
Strategy authority
OrganizationalState
   ↓
Competing system-wide state authority
P11 organizational concept
   ↓
automatic Native Core subsystem
DP-04
   ↓
automatic P11 authorization

⸻

§19 — PROVE-ME-WRONG CONDITION

This decision shall be revisited only if authoritative evidence demonstrates that:

1. the organizational layer cannot represent Delegation with sufficient semantic integrity;
2. an existing constitutional or architectural instrument explicitly requires Delegation to be a Native Core subsystem;
3. P12 Unified Operational State cannot safely integrate the organizational state projection;
4. an existing frozen entity is semantically incapable of supporting the selected organizational model;
5. a higher-authority Architect Decision or constitutional instrument contradicts this decision.

Absent such evidence, the decision stands.

⸻

§20 — DECISION INTEGRITY

The following distinctions are mandatory:

CONCEPT ≠ ENTITY
ENTITY ≠ NATIVE CORE SUBSYSTEM
ORGANIZATIONAL CONCEPT ≠ GOVERNANCE AUTHORITY
DELEGATION ≠ AUTHORITY CREATION
DELEGATION ≠ ACCOUNTABILITY TRANSFER
STATE PROJECTION ≠ SYSTEM-WIDE STATE AUTHORITY
ARCHITECT DECISION ≠ FOUNDER AUTHORIZATION

No implementation may reinterpret this ADR to expand its authority.

⸻

§21 — EFFECTIVE DATE

2026-09-10

This decision is effective upon issuance.

⸻

§22 — ARCHITECT SIGNATURE

Architect: AIOS Architect
Decision: DP-04
Signature: ISSUED BY ARCHITECT
Date: 2026-09-10

⸻

§23 — FINAL STATUS

STATUS: ISSUED

The DP-04 Architect Decision is authoritative for the P11 organizational entity/concept model.

⸻

§24 — ISSUED DECISION RECORD

Canonical decision:

P11 shall represent Goal and Plan as organizational concepts outside the frozen Native Core; Delegation shall be a first-class governed organizational relation/record outside the frozen Native Core; OrganizationalState shall be a bounded organizational projection whose system-wide integration belongs to P12 Unified Operational State. No new Native Core entity or subsystem is authorized by DP-04.

⸻

§25 — POST-ISSUANCE RULE

Claude Code may now use DP-04 as authoritative architectural input.

Claude Code shall:

* not reopen DP-04;
* not create a new Native Core subsystem;
* not silently modify the Architecture Freeze;
* not convert Delegation into Governance;
* not treat Goal or Plan as authorization;
* not create a competing P11 system-wide state authority;
* carry DP-04 forward into DP-03;
* identify only genuinely remaining architectural questions.

DP-03 remains a separate Architect Decision.

P11 authorization remains a separate Founder Decision.

E11 ratification remains a separate Founder Decision.

⸻

§26 — GOVERNING INVARIANTS

FROZEN ARCHITECTURE REMAINS FROZEN
P11 ORGANIZATIONAL SEMANTICS REMAIN EXPRESSIBLE
DELEGATION REMAINS DISTINCT FROM GOVERNANCE
DELEGATION DOES NOT TRANSFER ULTIMATE ACCOUNTABILITY
GOAL DOES NOT CREATE AUTHORITY
PLAN DOES NOT CREATE AUTHORITY
ORGANIZATIONAL STATE DOES NOT COMPETE WITH P12 UNIFIED STATE
P11 ≠ P12
ARCHITECT DECISION ≠ FOUNDER AUTHORIZATION
AUTHORITY ≠ OWNERSHIP
GOVERNANCE ≠ EXECUTION
CONCEPT ≠ ENTITY
ENTITY ≠ NATIVE CORE SUBSYSTEM

END OF DP-04 — ISSUED
