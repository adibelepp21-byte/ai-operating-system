# AIOS Agency Governance & Architecture Reconciliation Gate

| Field | Value |
|---|---|
| **Instruction** | `docs/governance/acts/DIR-AIOS-AGENCY-GOVERNANCE-ARCHITECTURE-RECONCILIATION-GATE.md` (verbatim; content sha256 `b4d5cfc091d81c2834589acd5db230015ec1f4e2e4e14da228a77df158efb776`). Receipt: Register `§131` |
| **Follows** | `AIOS-EXECUTIVE-AGENCY-INTEGRITY-TEST.md` (Register `§130`) · `AIOS-AGENCY-CURRENT-STATE-MAP.md` (Register `§129`) |
| **Mode** | Read-only reconciliation. Nothing was implemented, registered, activated or created. No Agent, Role, Department, ESD binding, delegation, envelope or Founder Decision was produced |
| **Actor** | Claude Code — AIOS Co-Founder + Delegated CEO (`ACT-CFV2-CEO-001-A`, `DEL-CFV2-CEO-001`), acting under A03 Discovery, A04 Work Classification and A16 Escalation Determination |
| **Gate result** | **DECISION REQUIRED** (`§28` critical stop). Executive-Agent **DECIDE** and **DELEGATE** authority, and the standing of an Executive Agent as an organizational actor distinct from an executing Agent Instance, are not established by any instrument. The precise questions are in OUTPUT 6. Everything else is classified |
| **Candidates** | Luffy, Nami, Zoro, Usopp, Robin, Franky, Chopper, Sanji, Jinbe, Brook: **CANDIDATE ONLY — NOT CANONICAL**. Used as paper fixtures in `§9` only |

---

## 0. Evidence index

Every finding below cites one of these. Line numbers are at commit `de46b56`.

| ID | Source | What it establishes |
|---|---|---|
| E-01 | `docs/constitution/engineering-constitution-v1.md:103` | The Canonical Domain Model is amended only through an ADR approved under `§3.4` |
| E-02 | `docs/constitution/engineering-constitution-v1.md:116`–`118` (`§6.2` inv. 2–4) | Automation may request and recommend, not override governance authority. Only the Domain Model may define an entity. No higher-tier exercise of lower-tier authority |
| E-03 | `docs/architecture/domain-model/canonical-domain-model-v1.md` `§1`, `§10` | Twelve ratified entities, **no Role**. `Steward` is a backlog candidate: *"Whether human accountability needs entity-level treatment is still an open question"* |
| E-04 | same, `:169` | Agent Instance: *"Not owned — a transient instantiation … accountable to the Platform Division that owns its Agent Definition"* |
| E-05 | same, `:230` (invariant 13) | *"No Agent Instance may collaborate directly with another Agent Instance outside of a shared Workflow, Knowledge, or scoped Memory"* |
| E-06 | `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md:77` | *"The twelve ratified entities … **No new entity.**"* |
| E-07 | `docs/governance/AIOS_COFOUNDER_V2_REGISTRATION_AND_ACTIVATION_RECORD_v1.0.md:414`–`436` | A01–A23. A09 Operational Decisions AUTHORIZED. A10 Contributor Delegation AUTHORIZED WITH BOUNDARY. A11 Verification AUTHORIZED. A19–A21 RESERVED (Founder). A22, A23 PROHIBITED |
| E-08 | same, `:222`–`229` (`RD-03`) | A10 assigns **work, not approval authority**. F02 `§19` reserves *"delegation authority"* and *"authority envelope definition"* to the Founder. F04 `§16`: *"Delegation is a mechanism for execution, not a mechanism for multiplying authority."* The CEO stays accountable |
| E-09 | same, `:440`, `:450`–`452` | *"UNKNOWN AUTHORITY is not AUTHORIZED."* Boundaries `C-5` (no action from automation or inferred permission), `C-6`, `C-7` |
| E-10 | `docs/governance/acts/FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md:188` (`§4.1`) | Claude Code, as Delegated Co-Founder / Executive, is **the** authorized W4 delegator |
| E-11 | same, `:448` (`§14`), `:482` (`§15`) | No self-authorization. Accountability chain: Agent Instance (execution) → Claude Code (delegated operational) → Founder (ultimate) |
| E-12 | same, `§5` | The Founder rejects *"Engineering … automatically becomes W4 delegator"* |
| E-13 | `tools/w4_delegation.py:64`, `:192`, `:286` | `AUTHORIZED_DELEGATOR = "Claude Code / AIOS Co-Founder"`. Any other delegator is refused. `revoke` exists. No completion transition |
| E-14 | `tools/agent_instance_registry.py:141`, `:198`, `:237` | Registration carries `permitted_capabilities`, `created_by`, `authority`, `accountable_to` (≠ the instance itself). `retire` exists |
| E-15 | `tools/w4_execution.py:55`–`58` | Outcomes are `success` / `failure` / `escalation` only. Delegation, lifecycle and work scope re-checked per step |
| E-16 | `tools/escalation_register.py:251`, `:270` | Closing an escalation requires a `HumanAuthority` |
| E-17 | `tools/p13/model.py` `ActionProposal`, `GateDecision`; `tools/p13/authority.py` `Envelope`, `AuthorityGate` | P13 proposes; only `AuthorityGate.decide` produces a decision, and only from a Register-recorded envelope. *"P13 cannot issue authority to itself"* |
| E-18 | `tools/p13/catalog.py:237` | `issue.delegation` is a reserved action type with no executor |
| E-19 | `consumers/__init__.py:37`–`38` | A consumer *"holds no governance authority, authors no Trace, and grants itself nothing: being handed a bound `Execution` is 'entry, not authority'"* |
| E-20 | `docs/architecture/volume-1/pd-01-executive-office/B2.md:9` | ESDs are classified *"Organizational Structure Architecture"* inside PD-01 |
| E-21 | `docs/architecture/volume-1/pd-01-executive-office/B3.md:96`–`109` | Capability Ownership Matrix: ten Capabilities, the `Owner` column naming ESD-01…ESD-10 |
| E-22 | `docs/architecture/volume-1/pd-01-executive-office/B5.md:17`, `:37`, `:443`, `:460`–`470`, `:611` | Role Groups are *"the final organizational structure layer before workforce roles"*. A Role Group *"does not define an individual person"*. Role Groups *"are not individual positions"*. Role Groups may be implemented by Human, AI Agent or Hybrid roles. INV-B06: *"Organization architecture must not transfer authority that has not been granted through the governance model."* |
| E-23 | `docs/architecture/volume-1/pd-01-executive-office/C1.md:150`–`162` | Governance levels: Sub Division → *"Head of Sub Division"*. Individual → *"Assigned Role sesuai delegasi"* |
| E-24 | `docs/architecture/volume-1/pd-01-executive-office/C3.md:70`–`86`, `:139` | DP-01 Authority Before Delegation. DP-03/DP-04 ownership and accountability retained. Delegated authority never exceeds the delegator's |
| E-25 | Parts `A5`, `C1`–`C10`, `D1`–`D10` of PD-01 Volume 1 | **No section names any ESD.** `grep -c "ESD-"` returns 0 for each |
| E-26 | `docs/architecture/platform-organization/SYSTEMIC-GAP-MAP.md:245` (`G-10`) | Sub Division, Team and Role Group are not ratified entities. Two readings of ESD capability ownership, neither adopted. OPEN — FOUNDER / ARCHITECT RESERVED |
| E-27 | `docs/architecture/platform-organization/IMPLEMENTATION-CORRESPONDENCE-MAP.md:113`, `:186`–`206` | PD-01 has no corresponding implemented boundary. No ownership binding is drawn; it would be a Domain-Model semantic act and a cross-Division structural act |
| E-28 | `docs/governance/AIOS_VOLUME_ACTIVATION_MODEL_v1.0.md` `§10` | PD-01 Activation NOT EXECUTED. PD-01 NOT ACTIVATION-ELIGIBLE. Activation Authority FOUNDER-RESERVED |
| E-29 | Register, `FD-P10-003` (Decision A) | Department population *"shall not be invented by Claude Code"*. PD-01…PD-10 are not Departments merely because they exist |
| E-30 | `python3 -m tools.organization_catalog` (run 2026-10-02) | Resident organization: departments `engineering`, `platform`. Capabilities `cognitive-intelligence`, `engineering-intelligence`, `governance-artifact-integrity`, each with one Agent Definition. **No PD-01 capability is resident** |
| E-31 | `docs/architecture/agency/evidence/AGENCY-E2E-SANDBOX-2026-10-02.json` | Sandbox path: an over-capability delegation is refused, a bounded delegation executes through the Execution contract, escalation works, state is rebuilt from files. Accept / reject / rework existed only in test code |

---

## OUTPUT 1 — Governance Reconciliation Report

### 1.1 Current authority (as found, not assumed)

```text
CONSTITUTION ──► FOUNDER (Moriarty) ──► CO-FOUNDER + DELEGATED CEO (Claude Code)
                  ultimate human           V2 REGISTERED · VERIFIED · ACTIVE
                  governance authority     ACT-CFV2-CEO-001-A · DEL-CFV2-CEO-001
                                                     │
                                                     │ FD-P11-001 §4.1  (W4 delegator)
                                                     ▼
                                           AGENT INSTANCE  (execution only)
```

- **Co-Founder V2 is canonical and active.** This is not just "Founder Approved". It has a registration, verification, activation id and an ACTIVE delegation (E-07). Precedence step 7 is therefore an operative instrument.
- **Founder Reserved Authority is unambiguous.** It covers:
  - A19 Final System Acceptance; A20 Mission / Identity; A21 Governance Model;
  - delegation authority and authority-envelope definition (F02 `§19`, E-08);
  - Domain Model change (C-2, E-01, E-02);
  - Platform Division activation (E-28);
  - Department population (E-29);
  - Constitution amendment (C-1).
- **CEO authority (A01–A18) is exercised by one office, the Claude Code / Co-Founder office.** No instrument extends any A-item to another actor:
  - A10 lets that office assign **work** to contributors and agents, but not approval authority (E-08);
  - A22 prohibits authority self-expansion.
- **Employee (Agent Instance) authority is execution authority:**
  - within one W4 grant (E-10, E-13);
  - on its permitted capabilities (E-14);
  - re-checked at every step (E-15);
  - with no governance authority (E-19).

### 1.2 Existing authority mechanisms (resident, implemented)

| Mechanism | Grants | To whom | Evidence |
|---|---|---|---|
| W4 delegation grant | bounded work, revocable | Agent Instance (recipient) | E-13 |
| Agent Instance registry | existence and permitted capabilities | Agent Instance | E-14 |
| W4 executor | per-step re-check, three outcomes | — (enforcement) | E-15 |
| Escalation register | open by anyone; close by `HumanAuthority` only | Founder / human | E-16 |
| P13 authority gate | decision from a recorded envelope only | the P13 executive loop | E-17 |
| Governance delegation register | `DEL-CFV2-CEO-001` | Co-Founder office | E-07 |

### 1.3 Executive Agent authority gap

There is **no "executive" class anywhere in resident mechanisms or instruments**. An Executive Agent is today indistinguishable from any Agent Instance: it can receive a bounded W4 grant and execute it. It cannot:

- **delegate**: refused by code (E-13) and by instrument (E-10, E-12);
- **decide** governed matters (E-02, E-16, E-17);
- **verify-and-accept** delegated results, since no resident accept / reject / rework mechanism exists (E-31).

No instrument defines an authority envelope for an Agent Instance beyond one grant. Defining one is Founder-reserved (E-08).

### 1.4 Conflicts and ambiguities found

| # | Ambiguity | Sources | Disposition |
|---|---|---|---|
| K-1 | **Agent Instance accountability has two axes.** It is *"accountable to the Platform Division that owns its Agent Definition"* (E-04). In W4 it is accountable to the delegator Claude Code, then the Founder (E-11, and the registry's `accountable_to`, E-14). | Domain Model vs. FD-P11-001 | **Not a contradiction.** One is organizational ownership and the other is delegated-operational accountability. FD-P11-001 is a Founder Decision and does not redefine the entity. Recorded so that a future Executive-Agent design does not collapse the two |
| K-2 | **ESD-level authority has no holder.** PD-01 names a *"Head of Sub Division"* (E-23), but no section of A5, C or D assigns authority to any ESD (E-25). | PD-01 C1 vs. A5/C/D | Open. This belongs with G-10 (E-26) |
| K-3 | **Role Groups claim AI-Agent compatibility** (E-22), but individual roles are deferred to *"later workforce and operating architecture"*. No such architecture is resident. | PD-01 B5 | Open. No instrument makes an AI Agent the holder of a role |
| K-4 | **The candidate executive diagram (`§19` of the instruction) puts Executive Agents between the CEO and Employees.** Canon has the CEO office delegating directly to Agent Instances (E-10). An intermediate agent → agent delegation would also meet Domain Model invariant 13 (E-05) unless it is mediated by a shared Workflow. | instruction vs. FD-P11-001, Domain Model | The diagram is **not canonical** and is not adopted (instruction `§19`) |

---

## OUTPUT 2 — ESD / Role / Capability / Agent Model (actual, evidence-only)

### 2.1 What actually exists, by layer

```text
DOCUMENTATION LAYER (PD-01 Volume 1 — FROZEN · NOT ACTIVATED · NOT ACTIVATION-ELIGIBLE)
  PD-01 Executive Office
   └─ ESD-01…ESD-10            "Organizational Structure Architecture" (E-20); not an entity (E-26)
       └─ Capability ×10       B3 matrix, Owner = ESD (G-10 OPEN) (E-21)
           └─ Team ×N          B4; not an entity
               └─ Role Group ×20   B5; "not individual positions" (E-22); not an entity
                   └─ (individual role)   NOT DEFINED — deferred to later architecture

                    ╳  no binding exists between these two layers  (E-27, E-30)

RESIDENT LAYER (implemented, executed, verified)
  Organization "aios"
   └─ Department / Platform Division   engineering · platform   (E-30)
       └─ Capability                    3 resident               (Domain Model inv. 1)
           └─ Agent Definition          implements ≥1 Capability (inv. 2; E-30)
               └─ Agent Instance        permitted_capabilities, accountable_to (E-14)
                   └─ W4 Grant          objective · capability_scope · work_scope ·
                                        accountable_party · verification_requirement ·
                                        escalation_condition · termination  (E-13)
                       └─ Execution contract → Runtime   (E-19, E-31)
```

### 2.2 The requested chain, filled only with what was found

```text
ESD                    documentation construct inside PD-01 (no entity; G-10 OPEN)
 ↓  ╳  NO RESIDENT LINK
CAPABILITY             Domain-Model entity (resident: 3; PD-01's 10 are documentation only)
 ↓  Agent Definition.implemented_capabilities   (EXISTING CANONICAL, implemented)
AGENT DEFINITION
 ↓  Agent Instance registry (permitted_capabilities ⊆ definition)
AGENT INSTANCE
 ↓  W4 grant (objective + work_scope = the "responsibility" of one assignment)
WORK
```

- **Role**: no node. Role Group exists only in documentation, above the missing link.
- **Responsibility** has two homes, and neither is an entity:
  - in documentation, the B3 Capability *"Primary Responsibilities"*;
  - at run time, the per-assignment objective and `work_scope` of a W4 grant.
- **Authority, decision rights, delegation rights** for an agent: no node beyond the single W4 grant.
- **Accountability**: `accountable_party` on the grant (E-13) and `accountable_to` on the instance (E-14), ending at the Founder (E-11).

### 2.3 Role decision (`§9`)

**ROLE = NON-CANONICAL DESCRIPTOR**

| Model | Test | Result |
|---|---|---|
| A — Role as existing entity | needs canonical identity, lifecycle, ownership, capability binding, authority semantics | **Rejected.** Not among the twelve entities (E-03); *"No new entity"* (E-06); only the Domain Model may introduce one (E-02 inv. 3) |
| B — Role as organizational binding (Agent + Position/ESD + Capability + Responsibility) | each component must exist and be bound | **Partially present, not established.** Agent + Capability + Responsibility are bound **per assignment** by Agent Definition + W4 grant. The **Position/ESD** component has no resident representation (E-27, E-30) |
| C — Role not required | existing mechanisms suffice; Role is metadata | **Holds for execution.** Every executed path in E-31 ran without Role |

Classification of the residual: whether AIOS **wants** a formal position or role binding is a Domain Model question. The nearest candidate is the `Steward` backlog entry (E-03), and the route is an ADR (E-01). It is **not** required to run the agency path that exists. → ARCHITECTURE DECISION REQUIRED *only if* that is pursued (OUTPUT 6, Q-6).

---

## OUTPUT 3 — Executive Authority Matrix

### 3.1 Seven primitives × four actors

| Primitive | Founder | Co-Founder / CEO | Executive Agent | Employee Agent |
|---|---|---|---|---|
| **ACT** | AUTHORIZED (ultimate) | AUTHORIZED — A01, A02, A06, within Founder Goal / Target | **BOUNDED** — only as a W4 recipient, within one grant (E-13, E-14) | BOUNDED — same mechanism |
| **DECIDE** | AUTHORIZED; FOUNDER RESERVED matters | AUTHORIZED — A09 operational, A05 bounded architecture (C-1…C-4) | **NOT AUTHORIZED** for governed or approval decisions (E-02, E-08, E-16). Operational decision rights: **UNKNOWN → DECISION REQUIRED** (Q-2) | NOT AUTHORIZED |
| **DELEGATE** | AUTHORIZED (delegation authority reserved, E-08) | AUTHORIZED WITH BOUNDARY — A10 work only (RD-03). Sole W4 delegator (E-10) | **NOT AUTHORIZED** — refused in code (E-13) and instrument (E-10, E-12). Any change: **FOUNDER DECISION** (Q-3) | NOT AUTHORIZED |
| **VERIFY** | AUTHORIZED (A19 final acceptance) | AUTHORIZED — A11; integrate only after verification (RD-03) | **CONDITIONAL** — may produce verification *evidence* inside a grant (E-31 proved check results). Accept / reject / rework authority: **UNKNOWN → DECISION REQUIRED** (Q-4) | CONDITIONAL — evidence only |
| **ESCALATE** | receives; closes by `HumanAuthority` (E-16) | AUTHORIZED — A16 | **AUTHORIZED** to raise (open) via W4 `escalation` outcome; never to close (E-15, E-16) | AUTHORIZED to raise; never to close |
| **EXECUTE** | — (not an executor role) | AUTHORIZED — A02, A06 | BOUNDED — Execution contract only, never Runtime internals (E-19) | BOUNDED — same |
| **APPROVE** | FOUNDER RESERVED (strategic, governance, Constitution, final) | approval within A05 / A09 only; approval authority **not** sub-delegable (RD-03) | **NOT AUTHORIZED** | NOT AUTHORIZED |

### 3.2 `§18` Governance Decision Matrix

| Authority | CEO / Co-Founder | Executive Agent | Employee Agent | Status |
|---|---|---|---|---|
| Receive Work | AUTHORIZED (Founder Goal / Target, A01) | BOUNDED (W4 grant) | BOUNDED (W4 grant) | EXISTING CANONICAL |
| Act | AUTHORIZED | BOUNDED | BOUNDED | EXISTING CANONICAL (execution); "executive act" beyond a grant: GOVERNANCE DECISION REQUIRED |
| Decide | AUTHORIZED (A09; A05 bounded) | UNKNOWN | NOT AUTHORIZED | FOUNDER DECISION REQUIRED (Q-2) |
| Delegate | AUTHORIZED WITH BOUNDARY (A10) | NOT AUTHORIZED | NOT AUTHORIZED | FOUNDER DECISION REQUIRED (Q-3) |
| Execute | AUTHORIZED | BOUNDED | BOUNDED | EXISTING CANONICAL |
| Verify | AUTHORIZED (A11) | CONDITIONAL (evidence only) | CONDITIONAL (evidence only) | GOVERNANCE DECISION REQUIRED (Q-4) |
| Escalate | AUTHORIZED (A16) | AUTHORIZED (raise only) | AUTHORIZED (raise only) | EXISTING CANONICAL |
| Approve Strategic Change | NOT AUTHORIZED beyond A01 envelope | NOT AUTHORIZED | NOT AUTHORIZED | FOUNDER RESERVED |
| Change Governance | NOT AUTHORIZED (A21) | NOT AUTHORIZED | NOT AUTHORIZED | FOUNDER RESERVED |
| Change Constitution | NOT AUTHORIZED (C-1) | NOT AUTHORIZED | NOT AUTHORIZED | FOUNDER RESERVED |
| Final Acceptance | NOT AUTHORIZED (A15 is not final; A19) | NOT AUTHORIZED | NOT AUTHORIZED | FOUNDER RESERVED |

### 3.3 Accountability chain (`§15`) — current canon

| Question | Answer | Evidence |
|---|---|---|
| Who decides? | Founder (reserved); Co-Founder / CEO (A09, A05 bounded) | E-07, E-08 |
| Who acts? | Co-Founder / CEO; Agent Instances within a grant | E-10, E-13 |
| Who delegates? | Co-Founder / CEO office only | E-10, E-13 |
| Who executes? | Agent Instance via the Execution contract | E-15, E-19 |
| Who verifies? | Co-Founder / CEO (A11); final acceptance Founder (A19) | E-07, E-08 |
| Who remains accountable? | Delegator (Claude Code), then Founder; delegation ≠ transfer of accountability | E-11, E-24 |
| Who escalates? | Any actor raises; only `HumanAuthority` closes | E-15, E-16 |
| Who reports? | Co-Founder / CEO (A18 Founder Review Interface) | E-07 |

The candidate four-tier diagram in instruction `§19` is **not endorsed**. Canon supports **three** tiers: Founder → Co-Founder / CEO → Agent Instance → Execution. A middle "Executive Agent" tier with delegated authority has no instrument.

---

## OUTPUT 4 — Architecture Reconciliation

### 4.1 Can Agency be formed from existing AIOS + binding + activation + integration?

**For the three-tier agency (Founder → CEO office → Agent Instances): YES.** No new architectural domain is needed:

- every link has a resident mechanism (E-13…E-17, E-31);
- what remains is binding, integration and contract reconciliation (the `§130` gaps).

```text
AGENCY (three-tier) = ORGANIZATIONAL ACTIVATION / INTEGRATION
```

**For a four-tier agency with Executive Agents that decide, delegate and verify: NOT DETERMINABLE from current canon.** This is not because a mechanism is missing:

- **Decide**: the P13 pattern of proposal → `AuthorityGate` → recorded envelope → decision (E-17) is a resident, reusable mechanism for bounded automated decisions, *if* an envelope is issued.
- **Delegate**: the W4 grant model already carries delegator, recipient, scope, lifecycle, verification, escalation, accountability and termination. Only the delegator identity is fixed (E-13).
- **Verify**: `verification_requirement` is carried on every grant. The binding to an accept / reject / rework outcome is missing.

What is missing is **authority**: an envelope, a second delegator, decision rights. Defining authority is Founder-reserved (E-08). So the blocker is governance, not architecture.

### 4.2 What cannot be represented today

| Requirement | Representable? | Why / why not |
|---|---|---|
| Agent "occupies" an ESD | **No** | ESD is not an entity (E-26), PD-01 is not activated (E-28) and its capabilities are not resident (E-30). A binding would be a Domain-Model and cross-Division act (E-27) |
| Agent holds a Role | **No** | Role is not an entity. Role Group is documentation (`§2.3`) |
| Agent → Agent delegation | **Not without change** | The delegator is fixed (E-13). Invariant 13 requires mediation by a shared Workflow, Knowledge or scoped Memory (E-05) |
| Agent bounded decision | **Mechanism yes, authority no** | P13 gate pattern (E-17); no envelope for an Agent Instance |
| Agent verification → acceptance | **Contract gap** | Only test code in E-31 |

### 4.3 Architecture verdict

| Item | Classification |
|---|---|
| Agent / Capability / Agent Definition / Agent Instance / Execution / Runtime / Trace / Escalation | EXISTING — REUSABLE |
| CEO intake → plan → W4 grant → executor → outcome → escalation | EXISTING — BINDING REQUIRED (`§130` G-1, G-2) |
| Verification → accept / reject / rework; result model; Trace instance identity | EXISTING — CONTRACT RECONCILIATION |
| Continuous operation; unified state view | EXISTING — ACTIVATION REQUIRED / BINDING REQUIRED |
| PD-01 activation | FOUNDER RESERVED; PD-01 not activation-eligible (E-28) |
| ESD semantics (G-10); PD capabilities ↔ resident population (G-09 / FD-P10-003) | ARCHITECTURE DECISION REQUIRED |
| Executive-Agent decide / delegate / verify-accept authority | GOVERNANCE DECISION REQUIRED (Founder-reserved envelope) |
| Role entity | not required; ARCHITECTURE DECISION only if wanted |
| TRUE ARCHITECTURAL GAP | **None found** |

---

## OUTPUT 5 — Post-Gate Work Classification

Classified only. **None of these items has been started.**

| Class | Item | Authority basis (existing) | Precondition |
|---|---|---|---|
| **ACTIVATE** | Continuous operation of the three-tier loop (scheduled cycle instead of manual triggers) | A02, A06 within envelope; any Production surface stays under the deployment pause | Founder lifts or scopes the deployment pause for this |
| **BIND** | B-1 CEO plan → W4 grant issuance (`§129` G-1), within FD-P11-001 | A10 + FD-P11-001 `§4.1` | none for the CEO office as delegator |
| | B-2 Founder instrument → Goal intake (G-2) | A01, A18 | Founder confirms the intake form (a Goal is Founder-originated) |
| | B-3 P13 reads organizational work state (G-3) | A06, P13-018 envelope | — |
| | B-4 Grant closure: complete or terminate the 4 ACTIVE grants since 2026-09-11 (G-4) | A10, FD-P11-001 | — |
| **INTEGRATE** | Unified agency state view (CC-7); runtime binder (sandbox `perform` → resident) | A02, A06, A14 | — |
| **RECONCILE CONTRACT** | RC-1 result model (`participate` returns nothing) | A05 bounded; native_core contract change is `change.native_core`, a reserved P13 type | Architect / Founder if native_core is touched |
| | RC-2 Trace carries the Agent Instance identity | same | same |
| | RC-3 `verification_requirement` → accept / reject / rework / escalate, **without a new state machine**: reuse W4 outcomes + escalation | A11 (CEO verifies) | — for the CEO as verifier; Q-4 for an agent verifier |
| **GOVERNANCE DECISION** | Q-1 … Q-5 (OUTPUT 6) | Founder | — |
| **ARCHITECTURE DECISION** | Q-6 Role / position binding; Q-7 ESD semantics (G-10); Q-8 PD capability population (G-09) | Founder / Architect (FD-2 open) via ADR (E-01) | — |
| **IMPLEMENT** | Only after the item above it is authorized. **Nothing is implementation-ready for executive agents.** For the three-tier agency, B-1…B-4 and RC-3 (CEO verifier) are within existing authority | — | — |

---

## OUTPUT 6 — Blocked Decisions

Claude Code must not take these without the stated authority. Each one is a **DECISION REQUIRED** with its precise question.

| ID | Precise question | Decider | Why blocked | Evidence |
|---|---|---|---|---|
| **Q-1** | Shall AIOS recognize an "Executive Agent" as an organizational actor distinct from an executing Agent Instance? If so, under which instrument, and as an Agent Instance with an authority envelope or as something else? | **Founder** | Authority-envelope definition is Founder-reserved. A22 forbids self-expansion. A consumer grants itself nothing | E-08, E-07, E-19 |
| **Q-2** | May an Agent Instance hold **decision rights**? If so, which decision classes (operational only?), under which envelope? Shall the P13 proposal → `AuthorityGate` → recorded-envelope pattern be the required mechanism? | **Founder** | Automation may not override governance authority. Decisions on governed matters need `HumanAuthority` | E-02, E-16, E-17 |
| **Q-3** | May anyone other than the Co-Founder / CEO office be a W4 delegator? If so: work only (RD-03 analogue), which capabilities, how many levels? Confirm that a delegated agent may delegate only within its own envelope, fail-closed | **Founder** | FD-P11-001 `§4.1` fixes the delegator. `§5` rejects automatic delegators. Delegation authority is reserved. Invariant 13 constrains agent → agent interaction | E-10, E-12, E-13, E-08, E-05 |
| **Q-4** | May an Agent Instance **accept / reject / rework** delegated results, or only produce verification evidence for the CEO office (A11) to act on? | **Founder** | A11 sits with the CEO office. Integration only after CEO verification (RD-03) | E-07, E-08, E-31 |
| **Q-5** | Is the candidate executive model (10 roles, four tiers) a target to pursue? If so, does it require **governance expansion** for functions with no canonical counterpart (CFO, Creative, Client Relations, PR / Social)? | **Founder** | Candidate actors cannot create governance. Mission and governance model are reserved (A20, A21) | instruction `§2`, `§16`–`§17`; E-07 |
| **Q-6** | Shall AIOS model a position / role binding (Agent ↔ ESD / Role Group ↔ responsibility) as a Domain-Model entity or relationship? The nearest backlog candidate is `Steward` | **Founder / Architect via ADR** (FD-2 open) | Only the Domain Model defines entities. *"No new entity"* | E-01, E-02, E-03, E-06 |
| **Q-7** | G-10: are ESDs internal stewardship inside PD-01 (Reading 1) or capability-owning units (Reading 2)? | **Founder / Architect** | OPEN — FOUNDER / ARCHITECT RESERVED | E-26 |
| **Q-8** | Shall PD-01's ten capabilities become resident Domain-Model Capabilities? If so, owned by which Department / Platform Division under FD-P10-003? | **Founder** (population) / Architect (ADR) | Claude Code may not invent Department population or draw ownership bindings | E-27, E-29, E-30 |
| **Q-9** | Shall PD-01 be made activation-eligible and activated? | **Founder** | Activation authority is Founder-reserved. PD-01 is not activation-eligible | E-28 |
| — | Also held, unchanged: Constitution (C-1), governance model (A21), final acceptance (A19), mission / identity (A20), deployment resume (`§129`), FD-2 | Founder | reserved | E-07 |

---

## AD-01 … AD-14 — explicit answers

| AD | Question | Answer | Classification |
|---|---|---|---|
| AD-01 | Canonical status of an Executive Sub Division? | A documentation construct (*"Organizational Structure Architecture"*) inside frozen, non-activated PD-01. It is not a Domain-Model entity.<br>• Owner: PD-01, as the document owner.<br>• Authority: none assigned (E-25).<br>• Capability: B3 "Owner" column, semantics open (G-10).<br>• Role groups: 2 each (B5).<br>• No runtime binding.<br>• Cannot be occupied by an Agent, and is not an organizational actor | **ARCHITECTURE DECISION REQUIRED** (Q-7) |
| AD-02 | Is an Executive Agent a legitimate organizational actor? | As an **executing** Agent Instance: yes. As an **executive** actor with its own authority: no instrument establishes it | **FOUNDER DECISION REQUIRED** (Q-1) |
| AD-03 | Is Role a canonical entity? | **No.** ROLE = NON-CANONICAL DESCRIPTOR | **EXISTING CANONICAL** (the canonical state is "not an entity") |
| AD-04 | If not an entity, how is Role represented? | As descriptive metadata. Its operative content is carried by:<br>• the Agent Definition's implemented capabilities;<br>• each W4 grant's objective, work scope and accountable party.<br>Role Group exists in documentation only | **EXISTING BUT NEEDS RECONCILIATION**; a formal binding → Q-6 |
| AD-05 | How does Role / Responsibility bind Capability? | In documentation:<br>• B3 Capability *"Primary Responsibilities"*;<br>• B5 Capability → Primary Role Group.<br>At run time: the W4 grant's `capability_scope` and `work_scope`. The documentation side has no resident link (E-30) | **ARCHITECTURE DECISION REQUIRED** (Q-7, Q-8) |
| AD-06 | How does Capability bind Agent? | Agent Definition implements ≥1 Capability (inv. 2). Instance `permitted_capabilities`. Grant `capability_scope`, enforced fail-closed (E-31 stage 4a) | **EXISTING CANONICAL** (implemented) |
| AD-07 | Can an Executive Agent Act? | **BOUNDED.** ACT = perform authorized organizational action within a grant's scope, capability, work, authority and constraints. No implicit access by virtue of an "executive" label | **EXISTING CANONICAL** (execution); executive action beyond a grant → Q-1 |
| AD-08 | Can an Executive Agent Decide? | **Not authorized** for governed or approval decisions. Operational decision rights **UNKNOWN**. **DO NOT IMPLEMENT** | **GOVERNANCE DECISION REQUIRED** — Founder (Q-2) |
| AD-09 | Can an Executive Agent Delegate? | **No** (code and instrument refuse it) | **FOUNDER DECISION REQUIRED** (Q-3) |
| AD-10 | Can an Executive Agent Verify? | It can produce verification evidence within a grant. Accept / reject / rework is **not resident** (test-proven ≠ resident) and not authorized for agents | **GOVERNANCE DECISION REQUIRED** (Q-4); the contract → RC-3 |
| AD-11 | Executive Agent authority envelope? | Today: exactly one W4 grant on permitted capabilities, revocable, escalation raise-only, no decide, no delegate, no approve | **EXISTING CANONICAL** as the floor; anything wider → Q-1…Q-4 |
| AD-12 | Who is accountable for delegated work? | The delegator (Claude Code / Co-Founder office), then the Founder. The instance holds execution accountability only. Delegation never transfers ultimate accountability | **EXISTING CANONICAL** (E-11, E-24) |
| AD-13 | What stays Founder-reserved? | A19–A21, delegation authority and authority-envelope definition, Domain Model and Constitution change, PD activation, Department population, deployment resume, FD-2 | **EXISTING CANONICAL** |
| AD-14 | Is the candidate 10-agent model compatible? | Not as canonical actors (`§9` below) | **FOUNDER DECISION REQUIRED** (Q-5), with Q-6…Q-9 for any ESD binding |

---

## 9. Candidate executive mapping (fixtures only — nothing created)

Question asked of each: *if realized one day, does AIOS today provide a canonical organizational binding for it?*

| Candidate | Candidate role | Nearest PD-01 documentation | Resident capability? | Canonical binding today |
|---|---|---|---|---|
| Luffy | CEO | ESD-01 Executive Leadership | No | **None.** The CEO function is canonically held by the Co-Founder office (E-07). Seating an agent there would change CEO authority, which the instruction (`§2`) forbids |
| Nami | CFO | — (no finance ESD) | No | None — **outside current Platform Organization** |
| Zoro | COO | ESD-10 Executive Operations / ESD-06 Platform Coordination (partial) | No | None (documentation overlap only) |
| Usopp | Creative Director | — | No | None — **outside** |
| Robin | Research / Strategy / Legal | ESD-02 Strategic Planning, ESD-03 Enterprise Governance, ESD-09 Risk & Compliance (split across three) | No | None (documentation overlap; one candidate spans three ESDs) |
| Franky | CTO | ESD-04 Architecture Governance (partial); engineering sits outside PD-01 | Partly: `engineering` department, 2 capabilities (E-30) | None as executive. Resident engineering Agent Definitions exist only as **employees** |
| Chopper | People / HR | ESD-07 Organizational Development (partial) | No | None (documentation overlap only) |
| Sanji | Client Relations | — | No | None — **outside** |
| Jinbe | Project / Risk | ESD-09 Risk & Compliance, ESD-08 Performance Management (partial) | No | None (documentation overlap only) |
| Brook | PR / Social | — | No | None — **outside** |

**Result.**

- Six candidates overlap PD-01 documentation, partially or across several ESDs. Four (CFO, Creative, Client Relations, PR / Social) have no canonical counterpart.
- No candidate has a resident binding as an executive.
- The model would need governance expansion and architecture decisions (Q-5…Q-9).
- Per instruction `§17`, the candidate model must adapt to canon. It is not forced.

---

## 10. Gate exit conditions (`§27`)

| # | Condition | Met? |
|---|---|---|
| 1 | Executive Agent authority classified | YES — OUTPUT 3 |
| 2 | Founder authority unambiguous | YES — `§1.1`, AD-13 |
| 3 | Co-Founder / CEO authority reconciled with canonical state | YES — V2 ACTIVE, A01–A23 |
| 4 | ESD semantic status determined | YES — determined *as* a documentation construct with G-10 open; the open part is routed (Q-7) |
| 5 | Role status determined | YES — NON-CANONICAL DESCRIPTOR |
| 6 | Role → Responsibility → Capability mapped | YES — `§2.2`, AD-05 |
| 7 | Capability → Agent mapped | YES — AD-06 |
| 8–11 | Act / Decide / Delegate / Verify determined | YES — determined, with Decide, Delegate and Verify-accept as DECISION REQUIRED |
| 12 | Accountability chain determined | YES — `§3.3` |
| 13 | Candidate model tested | YES — `§9` |
| 14 | Unresolved issues classified | YES — OUTPUT 5, OUTPUT 6 |
| 15 | No material unknown that could change the conclusion | **YES, with one qualification.** The remaining unknowns (Q-1…Q-9) are decisions, not missing evidence. No further discovery would change them. Each is assigned to its authority |

**Gate state: CLOSED WITH DECISION REQUIRED.**

- The three-tier agency (Founder → Co-Founder / CEO → Agent Instances) is **activation / binding / integration** on existing mechanisms, within existing authority. It is still subject to the deployment pause for any Production surface.
- The Executive-Agent tier is **blocked on Founder decisions Q-1…Q-5**. Any ESD or Role binding is blocked on architecture decisions Q-6…Q-9.
- No new subsystem is indicated, and no true architectural gap was found.
