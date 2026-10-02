# AIOS Agency — Current-State Map (Discovery, v1)

| Field | Value |
|---|---|
| **Directive** | `acts/DIR-AIOS-DEPLOYMENT-PAUSE-AND-AGENCY-CONSTRUCTION.md` (verbatim; content sha256 `d5d29f9b…`; Register `§129`) |
| **Executor** | Claude Code — Co-Founder + Delegated CEO (`DEL-CFV2-CEO-001`, ACTIVE) |
| **Date** | 2026-10-02 |
| **Method** | Read-only discovery of code, resident records and live records; commands re-run where cited. Nothing constructed |
| **Deployment** | **PAUSED / DEFERRED** (directive `§1`). FS-10 state frozen as recorded at Register `§126`–`§128` and in the M1 evidence |

Status vocabulary (directive `§5`): EXISTING · FRAGMENTED · BLUEPRINT_ONLY · IMPLEMENTED · EXECUTABLE · INTEGRATED · OBSERVABLE · VERIFIED · CANONICAL · UNKNOWN · MISSING. A status is never inferred from documentation alone.

## 1. Agency definition

Here, "Agency" means the AIOS architecture **behaving as an organization**. It can:
- take a goal;
- decide, delegate and execute under recorded authority;
- observe, record and verify the result;
- keep state and choose the next action;
- escalate to the Founder when authority runs out.

The directive's living loop (`§7`) is the acceptance test. An organization chart is not.

## 2. Source and authority basis

| Layer | Instrument (as resident) |
|---|---|
| Constitution / Freeze | `docs/architecture/AIOS_ARCHITECTURE_CONSTITUTION_v1.0.md`, `AIOS_ARCHITECTURE_FREEZE_v1.0.md` (INV-1…15; INV-13: Workflow is the sole channel for multi-agent coordination) |
| Founder decisions | Governance Decision Register; P10 `FD-P10-003` (ownership instantiation); P11 `FD-P11-001` (W4 delegation and Agent Instance authorization), `DP-01`…`DP-04`; P13 `P13-018`, `FDR-3`; Platform Organization `FD-PO-004` |
| Delegation to CEO | `DEL-CFV2-CEO-001` (Co-Founder + Delegated CEO, Charter `§33` A01–A18) — ACTIVE (`tools.governance_delegation_register`) |
| This directive | Discovery and in-authority construction only; `§11`: necessary ≠ authorized |

## 3. Organizational structure

| Level | Documented | Instantiated (resident records read by `tools.organization_catalog`) |
|---|---|---|
| Organization | AIOS | 1 |
| Platform Divisions | **10** canonical volumes, PD-01 Executive Office … PD-10 Developer Experience (closed under `FD-PO-004`) | not instantiated as organizational records |
| Departments | — | **2**: `engineering`, `platform` |
| Capabilities | — | **3**: cognitive-intelligence, engineering-intelligence (engineering); governance-artifact-integrity (platform) |
| Ownership graph | Domain Model | built from records, **0 defects** |

**Status:** structure CANONICAL as documentation (10 divisions). Structure INSTANTIATED for 2 departments and 3 capabilities only. **FRAGMENTED** between the two.

## 4. Actor inventory

| Actor | Evidence | Status |
|---|---|---|
| Founder | `native_core/core/governance/authority.py` `HumanAuthority`; Founder decisions in the Register | EXISTING, CANONICAL |
| Co-Founder + Delegated CEO (Claude Code) | `DEL-CFV2-CEO-001` ACTIVE | CANONICAL. The executive behaviour is P13 (`§9`); acting as CEO is session-bound (no persistent executive process) |
| Agent Definitions | cognitive-intelligence-agent, engineering-intelligence-agent, governance-artifact-integrity-agent (`docs/architecture/organization/*/agent-definitions`) | IMPLEMENTED (3) |
| Agent Instances | `engineering-intelligence-instance-001`, `governance-artifact-integrity-instance-001` (`docs/architecture/p11/*-operations/*.instance.json`, 4 records) | EXECUTABLE, VERIFIED in P11 runs |
| Resident consumers | `consumers/*_agent.py` (reference, cognitive, engineering, knowledge, memory, tool, workflow) | IMPLEMENTED; each proves one phase milestone |
| S-OPS actor | `tools/s_ops/surface.py`, `P13-ENV-02` | EXECUTABLE (2 transitions on 1 proof object) |
| `aios-operator` | fullstack B3 principal | operational principal of the paused deployment |
| Contributors / Workers | no resident definition distinct from Agent Instance | **UNKNOWN** (not in the canonical model as a separate actor) |

## 5. Capability inventory

| Capability | Owner | Executable path | Status |
|---|---|---|---|
| Cognitive Intelligence (decomposition ≥ 2 ordered sub-steps) | engineering | `consumers/cognitive_intelligence_agent.py` | IMPLEMENTED, VERIFIED (E5-2); declares **no Workflow** (valid, INV-15) |
| Engineering Intelligence (Coding, Testing) | engineering | `consumers/engineering_intelligence_agent.py`; W4 runs | EXECUTABLE, VERIFIED |
| Governance Artifact Integrity | platform | 6 Workflows (conformance review, corpus health, synchronization, post-amendment sweep, pre-ratification validation, terminology audit) | IMPLEMENTED; W1 / cross-Department runs VERIFIED |
| Knowledge retrieve/update | — | `consumers/knowledge_agent.py`, `native_core/core/knowledge` | IMPLEMENTED, VERIFIED (P6) |
| Memory | — | `native_core/core/memory`, `consumers/memory_agent.py` | IMPLEMENTED, VERIFIED (P7) |
| Governed Tool invocation | — | `consumers/tool_agent.py` | IMPLEMENTED, VERIFIED (P8) |
| Runtime-hosted Workflow execution | — | `consumers/workflow_agent.py`; `fullstack/backend/aios.py` | EXECUTABLE, VERIFIED (P9; FS-09 suites) |

## 6. Authority inventory

| Authority | Mechanism | Status |
|---|---|---|
| Founder-reserved matters | Register; P13 `RESERVED` action types (code / governance / certified-evidence / constitution change, `issue.delegation`, `admit.knowledge`, `grant.authority`, `expand.envelope`, `external.action`, `review.consequence`) | CANONICAL, enforced in code (`tools/p13/catalog.py`) |
| CEO executive envelope | `P13-ENV-01` (read-only verifications, evidence, escalation), `P13-ENV-02` (S-OPS) | EXECUTABLE, re-checked every cycle (`tools/p13/authority.py`) |
| Operational delegation to agents | `FD-P11-001` → authorized W4 delegator → Agent Instance (`tools/w4_delegation.py`; delegated ≤ delegator ∩ scope ∩ canon) | EXECUTABLE, VERIFIED |
| Organizational (unit-to-unit) delegation | `tools/delegation_catalog.py` (W3) | IMPLEMENTED; population **0** by design (no unit-level delegator) |
| Escalation | `tools/escalation_register.py` (append-only, never an approval) | EXECUTABLE; 4 records, all citing a resolving Founder Decision |

## 7. Delegation model

```text
FOUNDER → FD-P11-001 → AUTHORIZED W4 DELEGATOR → AGENT INSTANCE → BOUNDED DELEGATION → W4 EXECUTION
```

- **Agent → Agent:** only through a Workflow (INV-13; `native_core/core/workflow/coordination.py` forbids direct collaboration). **Agent → Worker:** UNKNOWN (no separate worker).
- **Return / report:** an evidence record per operation (`*/first-execution.evidence.json` and equivalents); escalation records.
- **Live records:** 24 delegations (20 REVOKED, **4 ACTIVE**), last issued 2026-09-11.
- **CEO-loop → delegation:** **NOT CONNECTED.** P13 lists `issue.delegation` as RESERVED with no executor (Blueprint `§5.2`), so the executive loop cannot start a delegation.

## 8. Work lifecycle

| Stage | Mechanism | Status |
|---|---|---|
| Intake (goal from the Founder) | `tools/planning/goal.py` (`Goal`; *"does not create authority by itself"*) | **FRAGMENTED**: the concept exists, but goals are authored inside proof scripts (`tools/w4_first_run.py` `_plan()`); no intake from Founder instruments or any queue |
| Classification / ownership | ownership graph; `organization_catalog.resolve_work_entry` | IMPLEMENTED |
| Planning (PLAN → SEQUENCE → ADAPT → REVISE) | `tools/planning/` surface; continuity `tools/planning_continuity.py` (persists goals) | EXECUTABLE |
| Assignment (Plan → Workflow step → Agent Instance + Skill) | `tools/plan_to_workflow.py` (refuses rather than invents) | EXECUTABLE, VERIFIED |
| Execution | `tools/w4_execution.py` PLAN → DELEGATE → EXECUTE → OBSERVE → VERIFY → ADAPT → CONTINUE / ESCALATE, authority checked at **each step** | EXECUTABLE, VERIFIED |
| Completion / closure | delegation terminates "on completion of the bound plan, or revocation" | **FRAGMENTED**: 4 grants still ACTIVE with no automatic termination applied (`§20`) |

## 9. Execution model

- **Executive (CEO) cycle:**
  - `tools/p13/cycle.py` runs OBSERVE → UNDERSTAND → EVALUATE → REASON → PROPOSE → AUTHORITY CHECK → EXECUTE IF AUTHORIZED → VERIFY → LEARN/EVOLVE → RE-DISCOVER → RECORD.
  - It is deterministic (no model) and bounded to one execution per cycle.
  - It has 11 live cycles (`docs/operations/p13/cycles/`, latest 2026-09-24) and is certified.
- **Organizational cycle:** W4 (above), plus W1 PLAN → WORKFLOW → COORDINATION and the cross-Department run. Root entry points: `w1_coordination_proof.py`, `cross_department_coordination_proof.py`, `w4_first_execution.py`, `p12_w4_integrated_execution.py`.
- **Runtime substrate:**
  - `native_core/core/runtime` (lifecycle, discovery, hosting catalog);
  - `native_core/core/workflow` (lifecycle, `WorkflowMonitor`, coordination);
  - the application adapter `fullstack/backend/aios.py` (paused frontier).
- **Trigger:** every run starts **by hand** (script or session). **Continuous operation: MISSING** — no scheduler, Routine or resident process (`list_triggers` = none).

## 10. State model

| State | Where | Status |
|---|---|---|
| Work / plan state | planning surface; `planning_continuity` | EXECUTABLE (persisted) |
| Delegation / execution state | `docs/architecture/p11/*-operations/*.json`; `tools/w4_continuity.py` reconstructs from files only (missing · stale · duplicate · revoked · superseded · incomplete · failed · escalated · completed) | EXECUTABLE, VERIFIED (P11-W5) |
| Executive state | `docs/operations/p13/cycles`, `trace` | EXECUTABLE, VERIFIED |
| Runtime / workflow lifecycle | native core lifecycles; durable Trace | IMPLEMENTED, OBSERVABLE |
| Decision state | Governance Decision Register; Founder Decision Surface (E13-05) | CANONICAL |
| One organizational state view (all of the above) | — | **MISSING** as a single current view; parts are read separately by P13 sources and the organization catalog |

## 11. Communication / handoff model

| Handoff | Mechanism | Status |
|---|---|---|
| Plan → Workflow | `plan_to_workflow` | EXECUTABLE, VERIFIED |
| Agent ↔ Agent | Workflow only (INV-13) | CANONICAL, enforced |
| Cross-Department | `tools/w1_cross_department_run.py` | EXECUTABLE, VERIFIED (E11-04) |
| Result → Planning | `tools/performance_evidence.py` (P11-W6 → W2) | IMPLEMENTED |
| Escalation → Founder | escalation register → Founder Decision Surface | EXECUTABLE; the Founder's answer re-enters only as a new instrument (by hand) |
| CEO ↔ organizational loop | — | **NOT CONNECTED** (`§7`) |

## 12. Observation model

- Trace: native core trace, `consumers/observation.py` (agent action → durable Trace), `p12_runtime_observation_proof.py` and `p12_trace_durability_proof.py`.
- Workflow: `WorkflowMonitor` read from another process (`p12_workflow_observation_proof.py`).
- Executive observation of organizational facts: the P13 state sources.

**Status:** OBSERVABLE, VERIFIED (P12).

## 13. Evidence model

- Per-run evidence records.
- P13 cycle records and P13 Trace, verified by the `verify.p13_evidence` action.
- Certified evidence manifests (P10–P13), with integrity checked by `tools/certified_evidence_integrity`.
- Decision evidence in the Register.

**Status:** VERIFIED, CANONICAL.

## 14. Failure / recovery model

- **Detection and refusal:** the authority gate, W4 per-step checks and `DirectCollaborationForbidden` fail closed.
- **Escalation:** the append-only register.
- **Recovery:** state reconstruction (`w4_continuity`), and stale-grant revocation in `w4_first_run._revoke_stale_grants`.
- **Status:** IMPLEMENTED.
- **Automatic retry:** absent by design (`review.consequence` is reserved; *"never retried blindly"*).
- **Repair of leftover ACTIVE grants:** not applied (`§20`).

## 15. Organizational memory and learning

| Function | Mechanism | Status |
|---|---|---|
| Memory from execution | trace → memory records → promotion candidates (`native_core/core/memory`) | IMPLEMENTED, VERIFIED |
| Knowledge admission | `native_core/core/knowledge`; in P13, `admit.knowledge` is RESERVED | IMPLEMENTED; executive admission reserved |
| Learning | `native_core/core/optimization`: governed learning loop, **detect-only** by design (PR-3); P13 `evolution.py` proposes, never acts | IMPLEMENTED as designed (proposal-only) |
| Decisions and history | Register, acts, evidence | CANONICAL |
| Measured connectivity | `tools.ecosystem_relationships`: Knowledge → Memory → Intelligence → Capability → Workflow → Organization → Governance → FounderDecision = CODE 4, DATA 2, MEDIATED 1, **NOT CONNECTED 0** | INTEGRATED (measured 2026-10-02) |

## 16. Governance boundaries

Founder-reserved actions are refused or escalated in code (`§6`). `DELEGATION ≠ AUTHORITY CREATION` is enforced as an intersection (`w4_delegation`). `PLAN READINESS ≠ AUTHORIZATION`: authority is re-checked at every step. `MEMORY ≠ AUTHORITY`: recovered grants are re-validated. **Status:** CANONICAL, enforced.

## 17. Living Agency Loop — end-to-end

| Loop link (directive `§7`) | Present as | Status |
|---|---|---|
| FOUNDER → GOAL | Founder instruments; `Goal` object | **FRAGMENTED** (no intake binding) |
| GOAL → CEO: UNDERSTAND / CLASSIFY / DECIDE | P13 cycle (state, evaluation, reasoning, next action, authority gate) | EXECUTABLE, VERIFIED. Its sources are governance and certification facts, not work items |
| CEO → DELEGATE | W4 delegation exists; P13 `issue.delegation` is reserved | **NOT CONNECTED** (governance-reserved) |
| DELEGATE → AGENT EXECUTE | W4 / W1 / cross-Department | EXECUTABLE, VERIFIED (runs 2026-09-11) |
| EXECUTE → OBSERVE → REPORT | Trace, monitor, evidence records | OBSERVABLE, VERIFIED |
| REPORT → VERIFY | W4 verify stage; P13 verify actions | EXECUTABLE |
| VERIFY → UPDATE STATE | W4 / P11 records; P13 records | EXECUTABLE |
| STATE → CEO → NEXT ACTION | P13 reads its sources; W4 adaptation is proposed back to planning | **PARTIAL**: P13 does not read W4 work state as a work queue |
| → ESCALATION → FOUNDER | escalation register; Founder Decision Surface | EXECUTABLE |
| CONTINUOUS OPERATION | — | **MISSING** (manual triggers only) |

**The organizational loop (W4) and the executive loop (P13) each run end to end. The links between them, Founder intake and continuous operation, are not there.**

## 18. Blueprint → implementation matrix

| Blueprint element | Implemented by | Status |
|---|---|---|
| 11 Native Core subsystems | `native_core/core/*` (≈ 10,000 LOC; 801 tests) | IMPLEMENTED, VERIFIED, CANONICAL (closeout) |
| Department ecosystem (P10) | `tools/organization_catalog.py` | INTEGRATED for 2 departments |
| Autonomous organization (P11 W1–W6) | `tools/planning`, `plan_to_workflow`, `w1_*`, `w4_*`, `escalation_register`, `performance_evidence`, `planning_continuity` | EXECUTABLE, VERIFIED |
| Integration (P12) | `p12_*` proofs, `tools/p12_*` verifiers | VERIFIED, certified |
| Executive intelligence (P13) | `tools/p13/*` | VERIFIED, certified, closed |
| Platform Organization PD-01…PD-10 | canonical volumes | **BLUEPRINT_ONLY** as organizational units (except the overlap with the 2 departments) |
| PD-01 Executive Office as organizational unit | — | BLUEPRINT_ONLY; the executive behaviour is P13, not bound to a PD-01 record |

## 19. Current-state matrix (summary)

| Dimension (directive `§6`) | Status |
|---|---|
| A Identity | CANONICAL |
| B Actors | Founder, CEO, 3 definitions and 4 instances EXISTING; workers UNKNOWN |
| C Capability | 3 owned capabilities INTEGRATED; 7 divisions not instantiated |
| D Authority | CANONICAL, enforced |
| E Work | FRAGMENTED (intake, closure) |
| F State | EXECUTABLE per loop; unified view MISSING |
| G Delegation | EXECUTABLE (W4); CEO-initiated NOT CONNECTED |
| H Handoff | EXECUTABLE, except CEO ↔ organization |
| I Execution | EXECUTABLE, manual trigger |
| J Observation | OBSERVABLE, VERIFIED |
| K Evidence | VERIFIED, CANONICAL |
| L Recovery | IMPLEMENTED; leftover ACTIVE grants not reconciled |
| M Memory / learning | IMPLEMENTED (learning detect-only by design) |
| N Governance | CANONICAL, enforced |

## 20. Disconnected components

1. **P13 executive loop ↔ W4 organizational loop:** `issue.delegation` is reserved, and P13 has no source reading W4 work state.
2. **Founder instruments ↔ planning `Goal`:** no intake.
3. **PD-01 Executive Office (documented) ↔ P13 (behaviour):** no organizational binding.

## 21. Fragmented components

1. Work closure. Delegations terminate "on completion of the bound plan", but nothing applies the termination. Four grants remain ACTIVE since 2026-09-11.
2. Organizational structure: 10 canonical divisions against 2 instantiated departments.
3. State: per-loop stores, no single organizational state view.

## 22. Unverified components

- The 4 ACTIVE delegations: whether their bound plans completed (`w4_continuity` can derive it; not run for this map).
- Resident consumers other than the Engineering and Governance agents: never driven by a delegation, only by their phase proofs.
- The fullstack application path: verified on Preview and Production, but on the paused frontier.

## 23. True missing capabilities

| Capability | Reconciled against | Finding |
|---|---|---|
| Continuous operation (a recurring trigger for the cycles) | P13 cycle, W4 loop, Claude Code Routines (`list_triggers`: none), fullstack runtime | **TRUE GAP.** The loops exist; nothing runs them on a cadence. Building one is mostly activation, but autonomous cadence is a governance question (`§25`) |

Every other apparent gap reconciles to existing capability: it is disconnected, fragmented or unverified, not missing.

## 24. Integration gaps

| Gap | What exists | What is missing |
|---|---|---|
| G-1 CEO → delegation | P13 gate and next action; W4 delegation | an executable path. Reserved by Blueprint `§5.2` ("no envelope can make it executable") |
| G-2 Founder goal intake | `Goal`, planning surface; Founder instruments | a reader that turns an authorized Founder instrument into a declared Goal, with its authority citation |
| G-3 Organizational state → executive | `w4_continuity`, `organization_catalog` | a P13 source that reads organizational work state (read-only) |
| G-4 Work closure | termination conditions, `_revoke_stale_grants` | applying termination when a bound plan completes |

## 25. Construction candidates (classified, directive `§13`)

| # | Candidate | Classification | Proceeds autonomously? |
|---|---|---|---|
| CC-1 | Reconcile the 4 ACTIVE delegations: derive plan state with `w4_continuity`; revoke those whose plan completed, with the reason | VERIFICATION REQUIRED → REPAIR REQUIRED | **Yes**: read is in authority; revocation by the authorized delegator per `FD-P11-001 §29` |
| CC-2 | P13 read-only source for organizational work state (G-3) | INTEGRATION REQUIRED | **Yes, if** the P13 envelope `P13-ENV-01` admits a new read-only source. Otherwise GOVERNANCE DECISION REQUIRED (to verify before building) |
| CC-3 | Founder-instrument → `Goal` intake (G-2) | IMPLEMENTATION REQUIRED | **To verify:** `DP-01 §3 W2` authorizes the planning surface. Who may *declare* a Goal from a Founder instrument is not established. Treat as GOVERNANCE DECISION REQUIRED until shown |
| CC-4 | CEO-initiated delegation (G-1) | **FOUNDER DECISION REQUIRED** (reserved action type) | No |
| CC-5 | Continuous operation cadence (`§23`) | ACTIVATION REQUIRED + GOVERNANCE DECISION REQUIRED (autonomous cadence) | No |
| CC-6 | Instantiate further Platform Divisions as Departments | GOVERNANCE / FOUNDER DECISION REQUIRED (`FD-P10-003` scope; `FD-PO-004`) | No |
| CC-7 | Unified organizational state view | INTEGRATION REQUIRED (read-only composition of existing readers) | **Yes** (read-only; no new authority) |
| CC-8 | Learning beyond detect-only | EXISTING — NO BUILD (detect-only is the governed design, PR-3) | n/a |

## 26. Unknowns

- U-1: whether a "Worker" or "Contributor" actor distinct from an Agent Instance is intended (no resident definition).
- U-2: whether `P13-ENV-01` admits a new read-only source without a new envelope (CC-2).
- U-3: who may declare a Goal from a Founder instrument (CC-3).
- U-4: plan completion of the 4 ACTIVE grants (CC-1).

## 27. Evidence register

| # | Evidence | Obtained |
|---|---|---|
| E-1 | native core subsystem inventory (files, LOC, tests) | code read, 2026-10-02 |
| E-2 | `tools/p13/catalog.py` RESERVED types incl. `issue.delegation`; executable types | code read |
| E-3 | `docs/operations/p13/cycles`: 11 records, latest `20260924T164519` | listing |
| E-4 | P11 records: 24 delegations (4 ACTIVE / 20 REVOKED), 4 instances, 1 escalation in w4-operations; latest 2026-09-11 | file parse |
| E-5 | `python -m tools.organization_catalog`: 2 departments, 3 capabilities, 3 agent definitions, 7 closed chains, 0 defects | run 2026-10-02 |
| E-6 | `python -m tools.ecosystem_relationships`: CODE 4 · DATA 2 · MEDIATED 1 · NOT CONNECTED 0 | run 2026-10-02 |
| E-7 | `python -m tools.governance_delegation_register`: `DEL-CFV2-CEO-001` ACTIVE | run 2026-10-02 |
| E-8 | `tools/w4_first_run.py` `_plan()`: Goal and Plan authored in code | code read |
| E-9 | `list_triggers`: none; no resident scheduler | tool call 2026-10-02 |
| E-10 | Active delegation termination terms: "on completion of the bound plan, or revocation"; no expiry | file parse |

## 28. Final conclusion

AIOS is not blueprint-only:
- Its **organizational loop** (plan → bounded delegation → agent execution through a Workflow → observation → verification → escalation → persisted, reconstructable state) is **implemented, executed and verified**.
- So is its **executive loop** (observe → reason → propose → authority check → bounded execution → verify → record).

It is **not yet a living organization**, for four evidenced reasons:
1. The executive loop **cannot delegate** (G-1, Founder-reserved).
2. **No Founder goal enters** the planning surface (G-2).
3. The executive loop **does not see organizational work state** (G-3).
4. **Nothing runs** either loop on its own (`§23`).

Every gap except the last is an integration or activation gap, not a missing subsystem. No new subsystem is indicated.

**Next (within authority):** CC-1 and CC-7. Before CC-2 and CC-3, verify the authority questions U-2 and U-3. CC-4, CC-5 and CC-6 need Founder decisions.
