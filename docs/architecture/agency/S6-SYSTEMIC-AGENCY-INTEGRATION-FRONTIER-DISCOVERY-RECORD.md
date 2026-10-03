# S-6 — Systemic Agency Integration Frontier Discovery & Exhaustion Gate: Record

| Field | Value |
|---|---|
| **Directive** | `docs/governance/acts/DIR-AIOS-AGENCY-S6-SYSTEMIC-INTEGRATION-FRONTIER-DISCOVERY.md` (verbatim; content sha256 `b5342ebe1e954cf60cc4d516bedd0e9db8fd184b662a9fd4a434d1762a2466e0`). Register `§153` (receipt), `§154` (result) |
| **Mode** | READ-ONLY. No code, schema, capability, Agent, delegation, plan, escalation, lifecycle, governance instrument, certified evidence or deployment state was changed |
| **Evidence** | • Baseline: `evidence/s6_baseline.py` → `evidence/S6-BASELINE-2026-10-03.json`, captured at `8625d94` before discovery.<br>• Discovery: `evidence/s6_frontier_discovery.py` (READ-ONLY EVIDENCE TOOL) → `evidence/S6-FRONTIER-DISCOVERY-2026-10-03.json`, **all_ok**. It rebuilds every fact below from files in a fresh process, runs the negative controls in memory, and compares 18 surfaces with the baseline: all equal. A second process yields the identical operational overview |
| **Answer (`§29`)** | The Agency chain is continuous from Founder Goal to Plan Outcome. It stops being demonstrably continuous **after** the outcome:<br>• the operational truth that S-1 … MR-S5-1 produced (live ledger, explicit decisions, plan outcomes) is read by none of the canonical state consumers (P12-W2 Unified Operational State, P13, W3);<br>• those consumers still report the historical view;<br>• no resident reader assembles plan state across roots.<br>The obstacle is a **disconnected existing mechanism with an unresolved authority route**, not a missing mechanism. A second, independent frontier: governed Agency execution never enters the Runtime or Trace |
| **Next gate (`§25` O)** | **TARGETED DISCOVERY REQUIRED**, scoped to the authority route for FR-1 (`§O`). Nothing constructed |

---

## A. S-1 → S-5 baseline

| Stage | Proven (Register) | Outside its boundary (what this gate examined) |
|---|---|---|
| S-1 Delegation lifecycle (`§135`–`§138`) | grant closure by operational disposition (A2 live ledger) with historical records untouched; human-only escalation response (B1) | who **reads** the operational view. Historical readers kept the historical view on purpose (S-1 review M-2) |
| S-2 Plan → Delegation (`§139`) | `issue_from_plan`; plan provenance on the grant; fresh-process reconstruction | grant **execution** (`0a697039a63f4c17` issued, never executed); in-process registries (S2-2) |
| S-3 Founder Goal → CEO → Agent (`§140`–`§141`) | verbatim Founder instrument → verified Goal → CEO plan → grant to an existing instance | execution of `50367d99c2dd4708` (never executed); candidate functions outside capability (S3-6) |
| S-4 Result → Verification → CEO Decision → Plan Outcome (`§147`–`§148`) | `persist_evidence`, `plan_completion`, `review_result`, `plan_outcome` | REJECT (→ S-5); where the outcome **goes** (state, observation, re-discovery); runtime (`perform` is caller-supplied) |
| S-5 / MR-S5-1 (`§149`–`§152`) | ACCEPT / REWORK / REJECT explicit and reconstructable without reason text | the same downstream boundary as S-4 |

**Two sequences share labels.** The FD-AGENCY-001 decision record `§5` defined an authorized surface S-1 … S-7. The S-1 and S-2 directives cite it (*"S-2–S-7"*). The S-5 and S-6 directives then reused the labels for different work. Three `§5` items have **no resident code** (evidence `fd_agency_001_section_5_items_not_started`), and the Register records none of them as superseded:
- *"S-5: P13 reads organizational work state"*;
- *"S-6: Unified agency state view"*;
- *"S-7: make the sandbox runtime binding resident"*.

They are the frontier below (SG-12).

## B. Current Agency system map (actual, from files)

```text
FOUNDER ──verbatim act + Register hash──▶ GOAL ──V2 A01──▶ CEO PLAN            [S-3]  persisted per root
CEO PLAN ──delegation_requirements → issue_from_plan──▶ GRANT                   [S-2]
GRANT ──capability ⊆ instance permits──▶ AGENT INSTANCE (engineering-intelligence-instance-001)
AGENT ──W4Executor (per-step authority) · perform = agent.verify(...) directly──▶ RESULT
        ✗ no Execution / Runtime   ✗ no Trace   ✗ no Workflow (single agent; INV-13 not engaged)
RESULT ──persist_evidence──▶ EVIDENCE ──plan_completion──▶ VERIFICATION (derived)  [S-4]
VERIFICATION ──review_result (delegator only)──▶ CEO DECISION (explicit)        [MR-S5-1]
CEO DECISION ──live ledger + plan revision──▶ PLAN OUTCOME (derived)            [S-4]
PLAN OUTCOME ──planning.state.json + ledger, per root──▶ STATE
STATE ──operational_overview (grants, escalations) · plan_outcome (one surface, root given by caller)──▶ ?
        ✗ P12-W2 Unified Operational State: P11/P12 roots, records "as stored"
        ✗ P13 StateUnderstanding: no Agency source; escalations read historically
        ✗ W3 organizational projection: P11 roots, historical
RE-DISCOVERY: performed by hand (one verification script per gate). P13's RE-DISCOVER does not see Agency work
```

Live state, read by the tool:

| Item | State |
|---|---|
| Operationally active grants | 2, both executable and unexecuted: S-2 `0a697039a63f4c17`, S-3 `50367d99c2dd4708` |
| Open goals | 3:<br>• `agency-s2-ledger-rule-verification`, 2 open steps;<br>• `founder-s3-connect-goal-to-planning`, 3 open steps;<br>• `founder-s4-rework`, 2 open steps; its rework step has **no grant** |
| Completed goals | 4 (`founder-s4-accept` and the three MR-S5-1 goals) |
| Decisions | 5 explicit, 16 legacy |
| Escalations | 2 OPEN-historical (P12 w3, kept by decision under FD-CG7-001); 2 answered; **0 blocking** |

## C. Interface matrix

| # | Boundary | Status | Evidence |
|---|---|---|---|
| 1 | Founder → Goal | **CONNECTED** | `founder_goal_refusal`; S-3 / MR-S5-1 goals cite their registered acts |
| 2 | Goal → CEO → Plan | **CONNECTED** | `adopt` with V2 A01 provenance; `planning_continuity` |
| 3 | Plan → Capability | **PARTIAL** | `PlanStep` carries no capability. The delegator names `capability_scope` at issue, and `issue()` checks it against the instance (N2 refused `risk-management`). `organization_catalog.resolve_work_entry` exists, but only tests call it |
| 4 | Capability → Delegation | **CONNECTED** | `issue()` refuses a scope beyond the instance's permitted surface |
| 5 | Delegation → Agent | **CONNECTED** (in-process) | grants to `engineering-intelligence-instance-001`; registries are in-process, so a fresh process re-registers in memory to continue (S2-2) |
| 6 | Agent → Workflow | **PARTIAL** | single-agent work runs without a Workflow (INV-13 applies to coordination). Multi-agent W1 / cross-department runs used `plan_to_workflow` (P11). They predate S-4 and never reach a CEO decision |
| 7 | Workflow / Execution → Runtime | **DISCONNECTED** (Agency chain) | no resident binder: `resident_binder_w4_to_execution_layer` = {}. The S-4 and MR-S5-1 runs call `agent.verify` directly. P12-W4 *published* a RUNNING observation with no Runtime lifecycle. W1 drove the resident Runtime through a `coordinate` callback supplied by its root entry script |
| 8 | Runtime → Result | **PARTIAL** | the result is `ExecutionOutcome` plus the evidence record. `participate` returns `None` (*"no result model is ratified"*). No Agency result is in any Trace store |
| 9 | Result → Verification | **CONNECTED** (derived) | `plan_completion` |
| 10 | Verification → CEO Decision | **CONNECTED** | `review_result`; explicit provenance (MR-S5-1) |
| 11 | Decision → Plan Outcome | **CONNECTED** (derived) | `plan_outcome`; decision faults none |
| 12 | Plan Outcome → State | **PARTIAL** | persisted per root and reconstructable. No resident reader **finds** the planning surfaces: `planning_surface_discovery_in_tools` = {}. Each is opened by a hard-coded path in an evidence script |
| 13 | State → Observability | **DISCONNECTED** | the canonical consumers read the historical view, and the operational view has no canonical consumer (`§G`, `§H`) |
| 14 | Observability → Re-discovery | **DISCONNECTED** | P13, the only resident RE-DISCOVER stage, reads no Agency state (`source_reads_agency_state` all false). Its last cycle is `20260924T164519`, before S-1 |
| 15 | Escalation → Founder | **CONNECTED** (by hand) | human-only response (`HumanAuthority`); the answer re-enters as a new instrument |
| 16 | Continuous operation | **MISSING** (governance) | `list_triggers` returned none (2026-10-03); P13 *"runs when it is run"* |

## D. Capability reconciliation

| Capability | Exists | Executable | Integrated | Observable | Organizationally owned |
|---|---|---|---|---|---|
| `engineering-intelligence` | yes | yes | **yes** (the whole S-chain) | evidence files only: **no Trace** for Agency work | engineering (ADR-0008) |
| `cognitive-intelligence` | yes | yes (C4) | **no**: 0 instances, 0 grants | no | engineering |
| `governance-artifact-integrity` | yes (defined) | no realizing consumer (tooling performs it) | P11 grants | P11 evidence | platform (ADR-0003) |

**Result.** The next frontier is not *capability missing*. In the Agency chain the one integrated capability is executable and decided upon, but not observable through the canonical state or Trace. That is integration, not capability.

The candidate functions (finance, creative, legal, client relations, PR / social) remain C0 and **organizational** (FD-AGENCY-001 GAP-B…F, Founder). Risk remains a capability-gap candidate to be tested against existing mechanisms first (GAP-A).

## E. Agent reconciliation (`§10`)

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | receive bounded work | yes | 9 Agency grants; per-step re-check |
| 2 | execute it | yes | `W4Executor` outcomes |
| 3 | return a result | yes, as outcome plus evidence | `persist_evidence` |
| 4 | result verified | yes, derived | `plan_completion` |
| 5 | CEO dispositions it | yes | `review_result`; N8: an agent reviewer is refused |
| 6 | resulting state reconstructable | yes, per root | fresh-process digest equal |
| 7 | capability binding reconstructable | yes | the instance record on disk (definition, permitted capabilities) plus the organization catalog |
| 8 | organizational purpose without Role / Position | yes: instance → definition → capability → department | `organization_catalog` (7 closed chains, 0 defects) |

The candidate Executive Agents are not needed for any of the eight. Their absence is a **decision** (FD-AGENCY-001 Q1-B, Q5-C), not a frontier. No instance is named after a candidate (N7).

## F. Workflow / runtime reconciliation

**Three proven execution paths exist, and no two of them meet:**

| Path | Has | Lacks |
|---|---|---|
| **S-chain** (S-2 … MR-S5-1) | grant, `W4Executor`, evidence, verification, **CEO decision**, plan outcome | Execution contract, Runtime, Trace, observation |
| **P12-W4** (`p12_w4_integrated_execution.py`) | grant, Trace (`TracedAction`), runtime **observation** by declared label, execution manifest, independent chain reader | `W4Executor`, CEO decision, plan outcome. The Runtime lifecycle is published, not hosted |
| **W1** (`w1_coordination_proof.py`) | plan → Workflow composition → resident Runtime via a caller-supplied `coordinate`; `W4Executor` | CEO decision, plan outcome. Stub performer for `governance-corpus-health-check` |

**The S-1 historical finding.** *"Delegated work initially did not enter a hosted Runtime"* is **STILL OPEN** for the governed Agency chain. It is **partially closed** historically by W1 (runtime) and P12-W4 (trace), on paths that never carried a CEO decision.

**Workflow.**
- Plans reach Workflows through `prepare_for_workflow` / `plan_to_workflow.compose` (CONNECTED, P11).
- The Workflow lifecycle (`DEFINED … SUCCEEDED / FAILED`) is distinct from the execution outcome and the plan state.
- No reader returns a Workflow's terminal state to `plan_outcome`. W1 records it only inside its own evidence.
- Ownership: Workflows are owned through agent definition → capability → department.
- Four catalog Workflows remain C2.

**Remaining uncertainty.**
- The Trace store root is inside certified P12 (`trace_store_root_certified: true`), and `p12_trace_registry` discovers stores only there. A live Agency Trace therefore has no lawful resident store yet.
- The Trace identity is the definition key, not the instance or the delegation (RC-2, a reserved `native_core` change).

## G. State / provenance reconciliation

| Kind | Items |
|---|---|
| **Explicit (persisted)** | Goals and plans (`planning.state.json`, supersession, origin, authority). Grants. Evidence. Dispositions with `decision` / `resulting_plan` / `rework_target`. Escalations and responses |
| **Derived (on read)** | verification; plan completion; executable / current vs historical; legacy decision; the open steps of a plan |
| **Historical** | certified P11 / P12 grant and escalation records (never rewritten) |
| **Operational** | the live ledger (dispositions, responses) outside certified roots |

- **Fresh-process reconstruction:** yes, per root. **Stale vs current:** distinguished by `operational_overview` only.
- **Completion hierarchy holds:**
  - a completed plan does not change the Goal, which has no status;
  - ACCEPT does not imply Founder acceptance (`founder_acceptance` NOT RECORDED on every goal);
  - no reader promotes plan completion to goal, phase or system completion.

**The divergence (SG-1).** Three canonical state consumers report the historical view as current:

| Canonical consumer | Reports | Operational truth |
|---|---|---|
| **P12-W2 Unified Operational State** (`tools/p12_operational_state.py`, *"the canonical integration surface for system-wide Unified Operational State"*) | `delegation.granted` = **34 grants, 14 active**, status CURRENT. It reads P11 / P12 roots *"as stored"* and never reads the live ledger | **2 active**, both in Agency roots it does not read (`operational_active_visible_to_canonical` = []) |
| **P13 StateUnderstanding** (via the P12 self-model) | open escalations `0991…`, `23f315ba…`, `9cb90fa0…`, `9d6b…` (4). The certified P13 Blueprint `§3` names *"operational state"* among its sources | 2 open (historical), **0 blocking**; `23f315ba` and `9cb90fa0` answered by the Founder (B1, FQ-CG7-2) |
| **W3 organizational projection** (`tools/delegation_reconciliation.py`) | 4 CURRENT projections: `4313bd22` (REVOKED), `4daebea9`, `0f7ac078`, `a437cdbb` (COMPLETED) | the 2 live grants are **not projected** |

None of the S-1, CG-7, S-4, S-5 or MR-S5-1 records considers P12-W2. CG-7 R-2 deliberately kept `operation_roots()` P11-only for certified measurements, and P12-W2's consumers are seven P12 verifiers.

## H. Observability reconciliation (`§14`)

*"What is the Agency doing right now, why, what is blocked, what completed, what next?"* can be answered from persisted evidence, but **only by manual reconciliation**:
1. run `operational_overview` (grants, escalations);
2. then restore each planning surface by a path the caller must already know, and run `plan_outcome` on it;
3. then discount what P12-W2, P13 and W3 report.

The honest answer, assembled this way:
- **Doing:** nothing is executing.
- **Waiting:** 2 live grants and 3 open goals.
- **Blocked:** nothing.
- **Completed:** 4 goals.
- **Next:** not represented anywhere.

**Pending work is not represented as pending.** Both roots holding a live, unexecuted grant report *"NO BLOCKING CONDITION — prior state is coherent"* (`roots_with_live_grants_reported_coherent`). An open delegated step with no grant (S-4 rework) is visible only inside `plan_outcome`.

**Single coherent view: no.** Multiple readers, and the canonical ones disagree with the operational one.

## I. Failure / recovery reconciliation

| Condition | Detected | Represented | Recoverable | Observable | Verified |
|---|---|---|---|---|---|
| Agent / execution failure | yes (`FAILURE` outcome) | evidence | REWORK / REJECT | evidence + `plan_outcome` | MR-S5-1 P2, P3 |
| Verification failure | yes (`plan_completion`) | derived | REWORK (ACCEPT refused) | `plan_outcome` | S-4, MR-S5-1 |
| Delegation refusal (out of scope) | yes (`ExecutionRefused`) | escalation record | human response only | register + overview | P11 `23f315ba`, P12 |
| Capability mismatch | yes, at issue | refusal | re-issue in scope | none persisted (refused before write) | N2 |
| Escalation | yes | `OPEN` / `ANSWERED` + live ledger | Founder response | operational view only; P13 sees the historical view | B1, FQ-CG7-2 |
| Plan revision | yes | `REVISED` + supersession | — | `plan_outcome` | S-4, MR-S5-1 |
| Stale delegation (live, unexecuted) | **no** | ACTIVE | — | reported as coherent | this gate |
| Stale plan (open step, no grant) | partly | open step | — | `plan_outcome` only | this gate |
| Missing recipient | yes | *"recipient not REGISTERED: nothing can execute"* | — | overview | CG-7 |
| Missing evidence | yes | *"0 evidence records"*; hash checks | — | `read_dispositions` | S-4, MR-S5-1 |

Recovery beyond escalation (retry) and replanning stay P13 **residual frontier** (`GAP-0018`, `GAP-0017`; P13-017). They are not reopened here.

## J. Re-discovery reconciliation

| After | Re-discovery |
|---|---|
| Delegation completion · verification · ACCEPT · REWORK · REJECT · plan revision | **MANUALLY PERFORMED**: one verification script per gate (`s2_` … `mr_s5_1_verification.py`), run by the CEO session |
| Escalation resolution | **MANUALLY PERFORMED** (CG-7 / S-1 verifications) |
| Capability failure | **UNVERIFIED**: no Agency path has met one |
| System level | **REAL but scoped away**: P13 RE-DISCOVER (`frontier.py`) runs on governance and certification facts. It has 11 cycles, the last on 2026-09-24, and no Agency source |

`FDR-G2` C8 lists *"system rediscovery"* among governed post-closure operation. It has not been performed by any resident mechanism over Agency state.

## K. Governance reconciliation

| # | Question (`§18`) | Finding |
|---|---|---|
| K-1 | silent authority expansion | **none found** |
| K-2 | implied ownership | none. W3 never states lifecycle |
| K-3 | agent decision rights | none: `review_result` refuses any reviewer but the delegator (N8). Decision authority is asserted by identity string and enforced by code-path separation: `consumers/` imports nothing from `tools/`. No violation; recorded as the enforcement model |
| K-4 | agent delegation rights | none (N9) |
| K-5 | Founder Reserved Authority changed | no. `issue.delegation` is still RESERVED in P13 |
| K-6 | CEO decision ≡ Founder acceptance | no. Every outcome reads `founder_acceptance: NOT RECORDED` |
| K-7 | **competing state model** | **open question, not a violation.** P12-W2 Authorization `§15` (as cited in `tools/p12_operational_state.py`) (*"Claude tidak boleh menciptakan competing system-wide state authority"*) and FD-CG7-001 R-2 (*"Do not create a second competing state model"*) both stand. Today the operational overview (R-2 / R-3) and P12-W2 disagree on what is current. Which surface is authoritative for current Agency state has not been decided |
| K-8 | changing the canonical consumers | P12-W2 feeds seven certified P12 verifiers (FDR-G1: successor, not in place). P13 is closed: FDR-G2 `§9` allows non-material maintenance that does not alter *"P13 scope"*; `§10` sends material change to Founder certification. Which side a new P13 source falls on is **not established** |

## L. Systemic gap register

| ID | Description | Primary | Affected boundary | Existing mechanism | Evidence | Current state | Dependency | Authority required | Construction? |
|---|---|---|---|---|---|---|---|---|---|
| **SG-1** | Canonical state consumers report the historical view; operational truth reaches none of them (secondary: DRIFTED, DUPLICATED, OBSERVABILITY) | **DISCONNECTED** | State → Observability | P12-W2 `p12_operational_state`; P12 self-model; W3 `delegation_reconciliation`; `w4_continuity.operational_overview` (R-2 / R-3) | `canonical_state`, `p13`, `w3` | 14 vs 2 active; 4 vs 0 blocking; 4 stale CURRENT projections | SG-2, SG-3, SG-7, any executive next action over Agency work | **undetermined** (K-7, K-8) | yes, route undetermined |
| **SG-2** | Executive re-discovery (P13) does not see Agency work (secondary: OBSERVABILITY) | **DISCONNECTED** | Observability → Re-discovery | P13 `StateUnderstanding` (Blueprint names operational state); FDR-G2 C8 | `p13` | 0 Agency sources; last cycle 2026-09-24 | SG-1 (which state to read) | FDR-G2 `§9` vs `§10`; P13-ENV-01 item 2 | yes, route undetermined |
| **SG-3** | Plan state not discoverable as one state; `plan_outcome` has no resident caller (secondary: OBSERVABILITY) | **STATE GAP** | Plan Outcome → State | `planning_continuity.persisted_goals`; `all_operation_roots` discovery pattern; `plan_outcome` | `readers` | 3 surfaces, found only by evidence scripts | SG-1 (must not become a competing model) | FD-AGENCY-001 `§5` (A06 / A12), subject to K-7 | yes (read-only composition) |
| **SG-4** | Pending work not represented as pending (secondary: STATE) | **OBSERVABILITY GAP** | State → Observability | `continuation_conditions` | `roots_with_live_grants_reported_coherent` | 2 roots "coherent" with live unexecuted grants | SG-3 | within reader maintenance, subject to K-7 | yes (reader) |
| **SG-5** | Governed Agency execution does not enter Execution / Runtime / Trace (secondary: INTEGRATION, EVIDENCE) | **DISCONNECTED** | Execution → Runtime → Trace | Execution contract (`create_execution_layer`, `participate`); `TracedAction`; `p12_trace_registry`; W1 `coordinate` | `runtime_trace` | 0 of 9 Agency grants in any Trace / observation / P13 record | Memory → performance evidence → planning; P13 Memory source | FD-AGENCY-001 `§5` S-7 (A02 / A06, Execution contract only); certified Trace store root | yes |
| **SG-6** | Trace identity is the definition key, not instance / delegation | **PROVENANCE GAP** | Runtime → Result | `TracedAction` | `trace_identity_in_participate` | unchanged since the 2026-10-02 integrity test | SG-5 | `change.native_core` reserved / ADR (RC-2) | yes, reserved |
| **SG-7** | No continuous operation; live grants stay dormant (secondary: MISSING) | **GOVERNANCE GAP** | whole loop | P13 cycle; Routines | `list_triggers` = [] | 2 dormant grants, 3 open goals | SG-1, SG-2 (a cadence over a view that misstates state would act on it) | Founder (autonomous cadence; deployment PAUSED) | not now |
| **SG-8** | Plan → Capability chosen by the delegator; `resolve_work_entry` unused | **PARTIAL** | Plan → Capability | `organization_catalog.resolve_work_entry` | `§C` row 3 | checked at issue | — | none | optional |
| **SG-9** | Instance and delegation registries are in-process (S2-2) | **PARTIAL** | Delegation → Agent | `AgentInstanceRegistry(None)` re-registration | MR-S5-1 run | works; pattern-dependent | — | none | optional |
| **SG-10** | `cognitive-intelligence` never integrated; `governance-artifact-integrity` has no consumer | **INTEGRATION GAP** | Capability → Agent | instance registry; tooling | Capability Discovery CG-2 / CG-3 | unchanged | — | CEO (`§7`); ADR-0003 owner | when a goal needs it |
| **SG-11** | Finance, creative, legal, client relations, PR / social; risk | **GOVERNANCE GAP** (risk: CAPABILITY GAP candidate) | Agent → Organizational function | none / escalation + P13 for risk | FD-AGENCY-001 `§4.2` | unchanged | — | Founder (GAP-B…F); GAP-A first tested | not now |
| **SG-12** | FD-AGENCY-001 `§5` items S-5 / S-6 / S-7 relabelled by later directives; unstarted; not superseded | **DRIFTED** (secondary: PROVENANCE) | Governance → Agency | the `§5` record | `fd_agency_001_section_5_items_not_started` | three items open under reused labels | SG-1, SG-2, SG-3, SG-5 rest on them | clarification of standing (record-level) | no |

## M. Frontier candidates (not ranked)

| Frontier | Gaps | A Materiality | B Current dependency | C Existing-mechanism coverage | D Integration depth | E Evidence strength | F Authority requirement | G Blocking effect | H Construction complexity |
|---|---|---|---|---|---|---|---|---|---|
| **FR-1** Operational truth → canonical state → executive re-discovery | SG-1…SG-4, SG-12 | HIGH: the loop's closing arc | HIGH: SG-7, any executive next action and the `§14` question depend on it | HIGH: every reader exists | MEDIUM: composition across P12-W2, P13, W3 and the operational overview | HIGH: measured disagreements (14 / 2, 4 / 0) | **UNKNOWN**: K-7, K-8 | HIGH: no current-state answer without manual reconciliation | LOW–MEDIUM (read-only) |
| **FR-2** Governed execution → Runtime / Trace | SG-5, SG-6 | MEDIUM: evidence exists without Trace | MEDIUM: Memory, performance and learning loops depend on it | HIGH (contract, `TracedAction`, registry) | MEDIUM | HIGH: 0 / 9 grants traced | MEDIUM: `§5` S-7 in authority; certified Trace root and RC-2 reserved | LOW for the decision loop; HIGH for Memory / learning | MEDIUM |
| **FR-3** Continuous operation | SG-7 | HIGH | depends on FR-1 | MEDIUM (P13 cycle; Routines) | LOW | HIGH | HIGH (Founder) | HIGH for autonomy | LOW technically |
| **FR-4** Organizational / capability scope | SG-10, SG-11 | MEDIUM | none for the engineering loop | LOW for new functions | — | HIGH | HIGH (Founder) | none for the current loop | — |

**Dependency statement (`§26`).**
- **FR-1 is the next material frontier.** The evidence shows that the operational state produced by S-1 … MR-S5-1 is **disconnected** from every canonical state consumer and from the only resident re-discovery stage (SG-1, SG-2), and is not discoverable as one state (SG-3). FR-3 depends on it, as does any executive next action over Agency work and the observability question of `§14`.
- **FR-2 is materially unresolved but independent of FR-1.** The readers can read W4 records directly, without Trace. It is reported separately (`§28`).
- **FR-3 and FR-4 are governance-gated** and do not precede FR-1.

## N. Exhaustion result

Searched before any gap was declared (`§22`):

| # | Area | What was searched |
|---|---|---|
| 1 | Canonical architecture | Constitution / Freeze INV-13 / INV-15; P13 Blueprint `§3` (sources); P12 `§13`–`§20` (Unified Operational State) |
| 2 | Contracts | `PlanStep`; `issue` / `issue_from_plan`; Execution contract; `ExecutionOutcome`; P13 envelopes |
| 3 | Capabilities | organization catalog; Capability Discovery (2026-10-03) |
| 4 | Agent mechanisms | instance registry; consumers; `participate` / `verify` |
| 5 | Workflow mechanisms | `plan_to_workflow`; `prepare_for_workflow`; W1 / cross-department runs; execution catalog |
| 6 | Runtime mechanisms | `native_core/core/runtime/execution`; `p12_runtime_observation`; `LocalExecutionSubstrate` (via Capability Discovery) |
| 7 | State readers | `reconstruct`, `operational_state`, `operational_overview`, `plan_outcome`, `planning_continuity`, `p12_operational_state`, `p12_self_model`, `delegation_reconciliation`, `delegation_catalog` |
| 8 | Provenance | `plan_provenance`; decision provenance; execution manifests; Trace |
| 9 | Governance | FD-AGENCY-001; FD-CG7-001 R-2 / R-3; FDR-G1; FDR-G2 C8 / `§9` / `§10`; P13-ENV-01; P12-W2 Authorization `§15` |
| 10 | Tests | 90 suites at `§152` |
| 11 | P13 patterns | `Source`, `StateUnderstanding`, `Frontier`, catalog RESERVED |
| 12 | S-1 → S-5 mechanisms | all of the above |

**Exhausted.** No gap above is classified as a missing mechanism except the governance-gated SG-7 (no trigger) and SG-11 (no function). Every other gap is a disconnected, partial or drifted **existing** mechanism (N12).

The remaining material unknowns are named, not resolved:
- K-7: which state surface is authoritative;
- K-8: whether a P13 source is maintenance or evolution;
- whether the `§5` items keep their standing under the reused labels (SG-12).

## O. Recommended next gate

**TARGETED DISCOVERY REQUIRED**, scoped to FR-1's authority route:

1. Which surface may carry current Agency state as the system-wide view without becoming a *competing* model (P12-W2 Authorization `§15`; FD-CG7-001 R-2): P12-W2 (a certified-measurement consumer, so FDR-G1 successor), the R-2 / R-3 operational overview, or both by delegation of one to the other.
2. Whether a P13 source over Agency state is FDR-G2 `§9` maintenance or `§10` architecture evolution, given that the certified Blueprint already names *"operational state"* as a source.
3. The standing of the FD-AGENCY-001 `§5` items under the reused labels.

**Possible outcomes of that discovery:**
- INTEGRATION CONSTRUCTION MAY BE AUTHORIZED (an in-authority route exists); or
- FOUNDER DECISION REQUIRED (only certified evolution is lawful).

FR-2 needs its own targeted discovery later (Trace store residency; S-7 binding; RC-2 reserved).

**Why not another type:**
- *No material frontier:* SG-1 is measured.
- *Founder decision:* an in-authority route has not been disproven.
- *Minimal remediation / construction:* the authority route is undetermined, and a competing-state prohibition is in force.

**S-6 is EXHAUSTED → REPORTED → STOPPED.** Nothing was constructed, delegated, revoked, answered or activated. Deployment stays PAUSED.

## Negative controls (`§23`) and integrity (`§24`)

| # | Control | Result |
|---|---|---|
| N1 | no new Agent | instance-record digest equal to baseline (8 files) |
| N2 | no new Capability | catalog digest equal; a `risk-management` scope is refused at issue |
| N3 | no new canonical entity | governance digest equal (except Register and this directive's act); Register only appended |
| N4 | no delegation issued | operational digest equal (49 files) |
| N5 | no operational state change | as N4 |
| N6 | no certified change | P11 / P12 / P13 / platform-organization / `docs/operations` digests equal; integrity no faults; git-clean |
| N7 | candidates not activated | candidates digest equal; `monkey-d-luffy` refused as recipient; no instance named after a candidate |
| N8 | no agent decision authority | refused (`review_result`, agent reviewer) |
| N9 | no agent delegation authority | refused (`issue_from_plan`, agent delegator) |
| N10 | Founder / CEO authority unchanged | `AUTHORIZED_DELEGATOR` unchanged; a decision outside the three is refused |
| N11 | no deployment change | `vercel.json` and `fullstack` digests equal |
| N12 | no missing artifact read as a missing capability | `§N`; each gap names its existing mechanism, and the tool checks that each exists |

All code digests (`tools`, `native_core`, `consumers`, `api`, `fullstack`, root entry points) are equal to the baseline.

**Writes by S-6:**
- this record;
- the verbatim act;
- the two evidence scripts and their two JSON outputs;
- Register `§153` and `§154`.
