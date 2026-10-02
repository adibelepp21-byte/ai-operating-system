# FD-AGENCY-001 — Decision Record, Authority Envelope and PD-01 Function Mapping

| Field | Value |
|---|---|
| **Decision** | `FD-AGENCY-001` — Founder Decision, Moriarty, 2026-10-02. **APPROVED WITH DEFERRED ORGANIZATIONAL EXPANSION** |
| **Instrument** | `docs/governance/acts/FD-AGENCY-001-FOUNDER-DECISION.md` (verbatim; content sha256 `f05c05f1406ad08105fbbb109c800fa65d471246e4296792c8985003d91ba481`). Gate as first received: `FD-AGENCY-001-FOUNDER-DECISION-GATE-AS-RECEIVED.md` (Register `§132`) |
| **Evidence base** | `AIOS-AGENCY-GOVERNANCE-ARCHITECTURE-RECONCILIATION-GATE.md` (Register `§131`), evidence E-01…E-31 |
| **Register** | `§133` |
| **This record** | the decision record and architecture / governance reconciliation (`FD-AGENCY-001 §7` steps 2–3) and the function mapping the decision directs (Q5-C steps 1–4; Q8-B). **No implementation.** Nothing was created, registered, activated or changed |

---

## 1. Dispositions as recorded

| Q | Founder selection | Operative meaning |
|---|---|---|
| Q1 | **B** | Three tiers only: Founder → Co-Founder / CEO → Agent. No Executive-Agent tier; a separate hierarchy is deferred and needs separate authorization |
| Q2 | **"B — Bounded decision rights only"** | See `§2` — label / text discrepancy **D-1**. Common floor applied |
| Q3 | **A** | Delegation stays with the Co-Founder / CEO office. No agent delegates. Agent-to-agent coordination only inside shared workflow / execution mechanisms |
| Q4 | **A** | Agents produce verification evidence, findings, status and escalations. Formal accept / reject / send-back stays with the existing authorized authority |
| Q5 | **C** | The ten-agent model is a deferred candidate direction: **CANDIDATE ONLY — NOT CANONICAL — NOT REGISTERED — NOT ACTIVATED**. Map functions first (`§4`). Luffy-as-CEO is not authorized |
| Q6 | **A** | No Role / Position entity. Role Group stays documentation terminology |
| Q7 | **A** | ESDs are internal PD-01 stewardship. They hold no authority, own no capability, and add no fourth level. **Closes `G-10` as Reading 1** (`SYSTEMIC-GAP-MAP.md` `G-10`) |
| Q8 | **B** | No new capabilities. Reconcile each documented function against the existing catalog first. Only genuine gaps go to a future decision |
| Q9 | **A** | PD-01 stays FROZEN and NOT ACTIVATION-ELIGIBLE. Documentation usable as reference evidence |

Conditions 1–9 of the instrument are recorded as binding. In short:

- no candidate created;
- the CEO identity is unchanged;
- no agent delegation authority;
- no new Role, Position, ESD, Department or Capability entity;
- connect and exercise existing mechanisms first;
- gaps return through ADR / Founder Decision;
- PD-01 frozen;
- deployment paused.

---

## 2. D-1 — Q2 label and text disagree (not resolved by this record)

In the gate as issued (`§132` instrument):

- **Q2-A** is *"YES, BOUNDED"*: agents *"may hold bounded decision rights"* through an authorized decision envelope.
- **Q2-B** is *"NO"*: agents may *"ANALYZE / PROPOSE / RECOMMEND / PROVIDE EVIDENCE but the decision remains with the authorized CEO/Founder authority."*

The decision selects **"Q2-B"** but titles it *"BOUNDED DECISION RIGHTS ONLY"*. Its text says agents *"may hold bounded decision authority only where explicitly granted within an existing authorized authority envelope"*. The consolidated table reads *"B — Bounded decision rights only"*. **The label is the template's NO; the text is the template's YES, narrowed.**

The decision rule says no decision may be inferred, so this record does not pick a reading. It applies only what **both readings share**:

| | Both readings agree | Readings differ |
|---|---|---|
| Today | **No Agent Instance holds any decision right.** No existing envelope grants one: P13-ENV-01 / P13-ENV-02 authorize the P13 loop, not Agent Instances | — |
| Excluded in all cases | governed matters, Founder-reserved matters, approval authority, CEO-reserved authority | — |
| Mechanism if ever granted | P13-style envelope-gated pattern as the reference | — |
| Future | — | Text reading: a Founder-issued envelope **may** later grant bounded (non-governed) decision classes to an agent. Label reading: never; agents only propose |
| Who would issue an envelope | the Founder in both readings. Authority-envelope definition is Founder-reserved (F02 `§19`; `§131` E-08), and FD-AGENCY-001 does not delegate it | — |

**Effect.** Nothing planned depends on D-1. No agent decision envelope will be prepared or proposed until the Founder states which reading is meant.

---

## 3. Resulting authority envelope (`FD-AGENCY-001 §10` item 4)

```text
FOUNDER (Moriarty)  — ultimate authority; reserved: A19–A21, delegation authority,
   │                  authority-envelope definition, Domain Model / Constitution change,
   │                  PD activation, Department population, deployment resume
   ▼
CO-FOUNDER / DELEGATED CEO (Claude Code) — A01–A18 unchanged; sole delegator (A10, FD-P11-001 §4.1);
   │                                        verifier (A11); accountable for delegated work
   ▼  W4 grant (bounded work; revocable)
AGENT INSTANCE — ACT within one grant on permitted capabilities;
                 DECIDE none (D-1 open for the future only); DELEGATE none;
                 VERIFY evidence only; ESCALATE raise only (closing needs HumanAuthority);
                 coordinates with other instances only through shared Workflow / Knowledge /
                 scoped Memory (Domain Model inv. 13)
   ▼
EXECUTION contract → Runtime  (never Runtime internals)
```

This replaces the `§131` matrix wherever the two differ. They differ in the Executive-Agent column:

- the column is **removed** (Q1-B);
- "Executive Agent" is now not a recognized actor, and only "Agent Instance" applies.

---

## 4. PD-01 executive function mapping (Q5-C steps 1–4; Q8-B)

**Method.** Each documented PD-01 function (B3 Capability Ownership Matrix) is read against four kinds of resident counterpart:

- resident Capabilities: `cognitive-intelligence`, `engineering-intelligence` (department `engineering`); `governance-artifact-integrity` (department `platform`);
- Agent Definitions;
- departments;
- authority structures and resident mechanisms.

**Classes.**

- **AUTHORITY COUNTERPART**: the function is held by a canonical office or reserved authority.
- **MECHANISM COUNTERPART**: a resident, tested mechanism performs it.
- **CAPABILITY COUNTERPART**: a resident Capability covers it.
- **PARTIAL**: some of the function is covered.
- **GENUINE GAP**: nothing resident covers it.

A counterpart that is a mechanism or an authority **is not a Capability**. Q8-B forbids converting it into one.

| # | PD-01 function (Owner ESD, stewardship only per Q7-A) | Resident counterpart | Class |
|---|---|---|---|
| F-01 | Strategic Leadership (ESD-01) | Founder (A20 Mission / Identity; Goal / Target) and Co-Founder / CEO A01 Executive Command | AUTHORITY COUNTERPART |
| F-02 | Strategic Planning (ESD-02) | P11-W2 planning surface `tools/planning` (Goal → Plan); `tools/planning_continuity.py` (P11-W5); CEO A01 / A04 | MECHANISM + AUTHORITY COUNTERPART |
| F-03 | Enterprise Governance (ESD-03) | Founder A21 (governance model reserved); `native_core/core/governance` (records and validates human decisions only); Governance Decision Register; Capability `governance-artifact-integrity` with its Agent Definition and 6 workflows | **CAPABILITY COUNTERPART (partial)** + MECHANISM + AUTHORITY |
| F-04 | Architecture Governance (ESD-04) | CEO A05 (bounded, C-1…C-4); ADR process (Constitution `§3.4`); `governance-artifact-integrity` workflows `pre-ratification-validation`, `terminology-audit`. FD-2 (Founder ≡ Architect) still open | AUTHORITY + PARTIAL CAPABILITY |
| F-05 | Decision Management (ESD-05) | Governance Decision Register; `native_core/core/governance/decision.py`; P13 `AuthorityGate` (envelope-gated decisions); `tools/escalation_register.py` | MECHANISM COUNTERPART |
| F-06 | Platform Alignment / Coordination (ESD-06) | CEO A07 / A08 (no ownership override); `tools/organization_catalog.py` (cross-department graph); `tools/p12_cross_platform_verification.py`; Domain Model inv. 10 (decision process for cross-division dependency) | AUTHORITY + MECHANISM COUNTERPART |
| F-07 | Organizational Development (ESD-07) | `tools/organization_catalog.py`; `tools/agent_instance_registry.py`; Agent Definitions at division discretion; Department population governed by FD-P10-003 | MECHANISM COUNTERPART (structure); population Founder-reserved |
| F-08 | Performance Management (ESD-08) | `tools/performance_evidence.py` (P11-W6 → W2); P13 evaluation / frontier; PD performance chain E1–E10 as reference | MECHANISM COUNTERPART |
| F-09 | Enterprise Assurance / Risk & Compliance (ESD-09) | **Compliance / assurance:** P12 verifiers (`tools/p12_*_verification.py`), `tools/stale_state_audit.py`, `tools/corpus_citation_audit.py`, escalation register.<br>**Risk management:** no resident risk register or risk mechanism found | **PARTIAL — risk management is a GENUINE GAP** |
| F-10 | Executive Enablement / Operations incl. Knowledge Management (ESD-10) | `native_core/core/knowledge` and `memory`; `tools/p12_knowledge_admission.py` (Founder-authorized admission); governance index; executive support is performed by the CEO office | MECHANISM COUNTERPART |

### 4.1 Candidate functions outside PD-01 (Q5-C step 3)

| Candidate function | Resident counterpart | Class |
|---|---|---|
| CFO — finance / commercial | none | **GENUINE GAP**, outside current Platform Organization |
| Creative Director — creative / content | none resident. "Creative" appears only as a Master Program Volume VI Intelligence category; Phase 5 is concept only | **GENUINE GAP**, outside |
| Client Relations — client / service | none | **GENUINE GAP**, outside |
| PR / Social — communication | none | **GENUINE GAP**, outside |
| COO — operations / production | CEO A02 / A06; W4 executor; Runtime | MECHANISM + AUTHORITY COUNTERPART |
| CTO — engineering / technology | department `engineering` (2 Capabilities, 2 Agent Definitions); CEO A05 / A06 | CAPABILITY + AUTHORITY COUNTERPART |
| People / HR (for an AI workforce) | F-07 mechanisms | MECHANISM COUNTERPART |
| Research / Strategy / Legal | F-02, F-03, F-10; **legal**: none | PARTIAL — **legal is a GENUINE GAP** |
| Project / Risk | P11 planning, W4 execution, escalation; **risk**: as F-09 | PARTIAL — risk gap as F-09 |
| CEO (Luffy) | held by the Co-Founder / CEO office | **not available**: identity reserved by the decision |

### 4.2 Genuine gaps and what each would require (Q5-C step 4)

These are determinations only. Under condition 7 each one returns to its decision route; none is started.

| Gap | Nature | What it would require | Route |
|---|---|---|---|
| GAP-A Risk management (F-09; Jinbe) | function inside PD-01's documented scope with no resident mechanism | First test whether an existing mechanism can carry it (escalation register + P13 evaluation as a risk view) before any Capability | IMPLEMENTATION DECISION within existing authority **if** an existing mechanism suffices; otherwise a Capability decision (Q8 route) |
| GAP-B Finance / commercial (CFO) | outside the Platform Organization | Organizational scope expansion; Department population (FD-P10-003); Capability; Agent Definition | **Founder Decision** (governance expansion), then ADR / Capability decision |
| GAP-C Creative / content | outside | same as GAP-B; also intersects Phase 5 Intelligence (not started) | **Founder Decision** |
| GAP-D Client relations | outside; would add an external-facing surface, which also touches deployment (paused) | same as GAP-B | **Founder Decision** |
| GAP-E PR / social | outside; external publishing; Domain Model inv. 12 (only Tool holds external dependencies) | same as GAP-B, plus a Tool for any external channel | **Founder Decision** |
| GAP-F Legal | no counterpart anywhere | same as GAP-B | **Founder Decision** |

**Finding for Q8-B.** Eight of the ten PD-01 functions already have an authority or mechanism counterpart. One (F-03) is partly covered by a resident Capability. Only **risk management** inside PD-01's scope is a genuine gap. **No PD-01 function needs to become a new Capability for the three-tier agency to operate.**

---

## 5. Authorized implementation surface (`FD-AGENCY-001 §7` step 3)

Each item is within existing authority and consistent with Q1-B…Q9-A. **Nothing below has started.** Each item would be its own validated, committed step.

| ID | Item | Authority | Decision fit |
|---|---|---|---|
| S-1 | Close the 4 W4 grants ACTIVE since 2026-09-11 (complete or revoke, with evidence) | A10, FD-P11-001 | Q3-A |
| S-2 | Connect CEO plan → W4 grant issuance (`§129` G-1) | A10, FD-P11-001 `§4.1` | Q1-B, Q3-A |
| S-3 | Founder goal intake: a Founder instrument becomes a Goal on the P11 surface (G-2). The Founder supplies the goal; the reader does not invent one | A01, A18 | Q1-B |
| S-4 | Verification evidence → **CEO** accept / reject / rework, reusing the W4 outcomes and the escalation register, with no new state machine (RC-3) | A11 | Q4-A |
| S-5 | P13 reads organizational work state (G-3) | A06, P13 envelopes | Q2 floor (P13 proposes; gate decides) |
| S-6 | Unified agency state view (read-only) | A06, A12 | — |
| S-7 | Make the sandbox runtime binding resident (instance → Execution → Runtime), Execution contract only | A02, A06 | condition 6 |

**Not on the surface:**

- RC-1 result model and RC-2 Trace instance identity, if they touch `native_core` (reserved `change.native_core`; ADR);
- continuous operation on any deployed surface (deployment paused);
- GAP-A…GAP-F;
- anything that depends on D-1.

---

## 6. Closure check (`FD-AGENCY-001 §10`)

| # | Condition | State |
|---|---|---|
| 1 | Q-1…Q-9 have explicit dispositions | YES. Q2 is explicit, but its label and text disagree (D-1) |
| 2 | Conditions recorded | YES — `§1` |
| 3 | Nothing inferred from silence | YES. D-1 is not resolved by inference |
| 4 | Resulting envelope unambiguous | **YES for today** (`§3`). The future reach of Q2 waits on D-1 |
| 5 | Architecture questions handed to the proper process | YES. G-10 closed by Q7-A:<br>• the Register entry names it under **Closes**, so `tools/platform_organization_gate.py` reports *"CLOSED by FD-AGENCY-001"* and PD-01 no longer carries REQUIRES ARCHITECT DECISION;<br>• live-state tests updated to match;<br>• the NC-13 controls keep testing pre-decision logic on a fixture with this closure removed;<br>• `SYSTEMIC-GAP-MAP.md` is **not** edited: it is part of the FD-PO-004-certified Platform Organization baseline, and an edit fails certified-evidence integrity. The Register entry is the record of closure.<br>GAP-B…F routed to Founder Decision; GAP-A to an implementation decision first |
| 6 | No implementation beyond approved scope | YES. None begun |

**State:**

- FD-AGENCY-001 is **REGISTERED · OPERATIVE**.
- The gate is **CLOSED** for Q1, Q3–Q9.
- Q2 is **OPERATIVE AT ITS COMMON FLOOR**, with the D-1 confirmation pending. This does not block anything on the implementation surface.
