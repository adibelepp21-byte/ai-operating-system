# Capability Discovery & Reconciliation Gate — Result (2026-10-03)

| Field | Value |
|---|---|
| **Directive** | `docs/governance/acts/DIR-AIOS-CAPABILITY-DISCOVERY-RECONCILIATION-GATE.md` (verbatim; content sha256 `b7612a3fef0cbb5856f82f2b04c7121c0b1d3fa5635692c6c40e4a89a991102d`). Register `§142` (receipt), `§143` (result) |
| **Nature** | Read-only discovery and reconciliation. No capability, entity, Agent Instance, Department, Role/Position, authority or delegation authority created. PD-01 and the candidates are not activated. Deployment stays PAUSED. S-4 not started |
| **Evidence** | `evidence/capability_discovery.py` → `evidence/CAPABILITY-DISCOVERY-2026-10-03.json` (read-only; live probes run on a temporary runtime; negative controls in memory; nothing written outside the JSON). The consumer test suites (`consumers/tests`, 276 tests) were run: **OK** |
| **Baselines** | FD-AGENCY-001 decision record `§4`–`§4.2`; S-1 (`§138`), S-2 (`§139`), S-3 (`§141`) |

**Scale.**

| Level | Meaning | Rule applied here |
|---|---|---|
| C0 | NOT FOUND | nothing anywhere |
| C1 | DOCUMENTED ONLY | named in prose; no canonical definition |
| C2 | ARCHITECTURALLY DEFINED | canonical definition (ADR, catalog, contract), no realizing code |
| C3 | IMPLEMENTED | realizing code exists |
| C4 | EXECUTABLE | invoked through its lawful interface and produced its result (live probe or test run, this gate) |
| C5 | INTEGRATED | wired into the authority path (instance, grant, plan, workflow) |
| C6 | OBSERVABLE / VERIFIED | an evidence record shows it performed, and that record is reconstructable |

A level is claimed only where this gate's evidence shows it. *Named in an evidence file* is not *performed*: two skills and one workflow appear in evidence only as coordinated step names, and are classed accordingly.

**What counts as a Capability.** Under the Domain Model, a Capability is an ADR-established unit owned by a Department. Native Core subsystems, consumers and repository tools are **platform mechanisms**. They are inventoried (Q8-B: a mechanism is never converted into a Capability), but they are not Capabilities.

---

## A. Capability Inventory

### A.1 Canonical Capabilities (Domain Model)

`tools/organization_catalog.read_departments()` lists exactly three:

| Capability | Dept / ADR | Agent Definition | Realizing consumer | Live probe (this gate) | Instances | Grants (active) | Evidence records | Level |
|---|---|---|---|---|---|---|---|---|
| `engineering-intelligence` | engineering / ADR-0008 | `engineering-intelligence-agent` | `consumers/engineering_intelligence_agent.py` | **success**: `participate(create_execution_layer(RUNNING runtime))` | `engineering-intelligence-instance-001`, `engineering-intelligence-instance-p12w3-005-001` | 23 (14) | P11 w4 first execution; P11 cross-department; P12 w4 first execution | **C6** |
| `cognitive-intelligence` | engineering / ADR-0008 | `cognitive-intelligence-agent` | `consumers/cognitive_intelligence_agent.py` | **success**: three SubSteps (draft / review / publish) | **none, ever** | 0 | none | **C4**: executable, never integrated |
| `governance-artifact-integrity` | platform / ADR-0003 | `governance-artifact-integrity-agent` | **none** | **not possible**: no consumer realizes it | `governance-artifact-integrity-instance-001` | 13 (2) | P11 W1 coordination; P11 cross-department | **C2** as a realized Capability. The **authority path** around it is C5 / C6. Its cross-department step was performed by `tools/corpus_citation_audit.py`, which is repository tooling, not a realizing consumer |

### A.2 Platform mechanisms (not Capabilities)

| Mechanism | Code | Level | Basis |
|---|---|---|---|
| Founder Goal verification | `tools/authority_citation.founder_goal_refusal` | C6 | S-3 run + fresh-process verification |
| CEO planning surface | `tools/planning`, `tools/planning_continuity.py` | C6 | S-2 / S-3 roots rebuilt from file |
| Plan → delegation (delegator only) | `tools/w4_delegation.issue_from_plan`, `plan_provenance` | C6 | S-2 / S-3 grants |
| W4 delegation and instance registry | `tools/w4_delegation.py`, `tools/agent_instance_registry.py` | C6 | 36 grant records; **registries are in-process only** (S2-2) |
| W4 execution | `tools/w4_execution.W4Executor` | C6 | P11 / P12 first-execution evidence; NC-10 this gate |
| Continuity / reconstruction, live ledgers | `tools/w4_continuity.py` (`reconstruct`, `operational_state`) | C6 | `§A.4` below |
| Escalation register | `tools/escalation_register.py` | C6 | 4 escalations on file; B1 response ledger |
| Native Core runtime / execution layer / substrate | `native_core/core/runtime`, `LocalExecutionSubstrate` | C6 | live probes this gate; P11 / P12 runs |
| Native Core tool subsystem | `native_core/core/infrastructure` (ToolBoundary, ToolRegistry, ToolInvocationGovernance, ToolSubsystem) | C4 | consumer suite (`tool_agent`). Only one resident `ExternalTool`: `fullstack/backend/docs_tool.py` `DocsReadTool` |
| Platform consumers | `knowledge_agent` (P6), `memory_agent` (P7), `tool_agent` (P8), `reference_agent` | C4 | 276 consumer tests OK |
| Workflow participation | `consumers/workflow_agent.py` | C6 | P11 W1 / cross-department runs |
| Observation | `consumers/observation.py` (`TracedAction`) | C6 | P12 corpus-health run (`aios_corpus_health_run.py`) |
| Governance tooling | `tools/corpus_citation_audit.py`, `tools/stale_state_audit.py`, governance index, `tools/certified_evidence_integrity.py` | C6 | run at every gate; the P12 corpus-health run is traced under `engineering-intelligence-instance-001` |
| Decision records / P13 evaluation | `native_core/core/governance/decision.py`, `tools/p13` | C6 | P13 certification evidence |
| Performance evidence | `tools/performance_evidence.py` | C4 | own suite |
| Organization catalog | `tools/organization_catalog.py` | C6 | this gate's catalog read |

### A.3 Execution catalog (`docs/architecture/organization/execution-catalog/`)

| Kind | Entry | Level | Note |
|---|---|---|---|
| workflow | `cross-department-artifact-conformance-review` | **C6** | real performers (P11 cross-department evidence) |
| workflow | `governance-corpus-health-check` | **C5** | the W1 run used a stub performer: evidence reads *"coordinated … via the sanctioned Workflow surface"*. The lifecycle is proven; the substance was not performed in that run |
| workflow | `governance-synchronization-review`, `post-amendment-consistency-sweep`, `pre-ratification-validation`, `terminology-audit` | **C2** | no code, no evidence |
| skill | `artifact-conformance-verification`, `citation-discipline-verification` | **C6** | substance performed (cross-department) |
| skill | `open-item-tracking-review`, `governance-artifact-diff-summary` | **C5** | coordination step names only (W1) |
| skill | `authority-boundary-check`, `correction-proposal-drafting`, `duplicate-content-detection`, `governance-cross-reference-scan`, `section-numbering-consistency-check`, `staleness-detection`, `terminology-consistency-scan` | **C2** | no evidence. `staleness-detection` is cited only in a docstring (`tools/plan_to_workflow.py`); its substance exists as `tools/stale_state_audit.py` without a binding |
| tool interface | `cross-reference-link-validator-interface`, `document-structure-parser-interface`, `repository-content-search-interface`, `text-similarity-comparison-interface`, `version-control-diff-interface` | **C2** | no binding to the Native Core tool subsystem; no evidence |
| runtime substrate | `batch-governance-review-substrate`, `interactive-governance-session-substrate`, `textual-reasoning-execution-substrate` | **C2** | none bound by name; `LocalExecutionSubstrate` (C6) is the only resident substrate |

### A.4 Live operational state (material finding, reported as found)

The script read every folder holding W4 records twice:
- **historically**, with `reconstruct(root)`;
- **operationally**, with `operational_state(root)`, which honours the S-1 A2 / B1 ledgers.

| Root | Historical | Operational |
|---|---|---|
| `p11/w1-operations` | 1 ACTIVE | 0 active; `4daebea9` COMPLETED |
| `p11/w4-operations` | 1 ACTIVE; `23f315ba` OPEN | 0 active; `4313bd22` REVOKED; `23f315ba` answered (B1) |
| `p11/x-department-operations` | 2 ACTIVE | 0 active; `0f7ac078`, `a437cdbb` COMPLETED |
| `agency/operations/w4-s2-plan-delegation` | 1 ACTIVE | `0a697039a63f4c17` ACTIVE, unexecuted (S-2) |
| `agency/operations/w4-s3-founder-goal` | 1 ACTIVE | `50367d99c2dd4708` ACTIVE, unexecuted (S-3) |
| **`p12/w4-operations`** | **10 ACTIVE**; `9cb90fa0787a478c` OPEN | **unchanged: 10 ACTIVE, 1 OPEN**. Condition: *"MORE THAN ONE LIVE GRANT FOR ONE INSTANCE"* (7 to `engineering-intelligence-instance-001`, 2 to `engineering-intelligence-instance-p12w3-001`, 1 to `engineering-intelligence-instance-p12w3-005-001`). Only the last has an instance record in that root |
| **`p12/w3-operations`** | `0991300404cf44d8`, `9d6bc0ad47294ef0` OPEN | unchanged |

**Correction.**
- The earlier count of *"4 ACTIVE delegations"* (CURRENT-STATE-MAP CC-1, gate B-4) and the S-1 population were drawn from P11 operation-root discovery (`operation_roots()`), which does not see P12. That count was incomplete.
- The three P12 escalations were already recorded as *OPEN, non-blocking by inference only* (post-P13 baseline report, *"The four escalations"*).
- The **ten P12 ACTIVE grants** were not counted anywhere. All ten are bound to P12 proof plans (`p12-w1-…`, `p12-w2-…`, `p12-w3-…`, `p12-w4-…`, `p12-live-verification-…`, `w4-first-execution-proof-…`) dated 2026-09-12 to 09-18.
- They sit in a **certified** root (`p12_certified_evidence_guard`), so the S-1 C-3 condition applies to them as it did to P11.
- Nothing was changed.

---

## B. PD-01 Reconciliation Matrix

Re-read against the FD-AGENCY-001 decision record `§4`. PD-01 itself stays **C1 / frozen** (condition 7). Its functions are stewardship descriptions, not Capabilities.

| # | PD-01 function | Resident counterpart (verified this gate) | Level of counterpart | Gap type | Change vs `§4` |
|---|---|---|---|---|---|
| F-01 | Strategic Leadership | Founder (A20; Goal / Target) and CEO A01; Founder Goal verification | authority + C6 mechanism | **NO GAP** (AUTHORITY counterpart) | none |
| F-02 | Strategic Planning | `tools/planning` + continuity; CEO A01 / A04 | C6 | **NO GAP** | none |
| F-03 | Enterprise Governance | Founder A21; Register; governance tooling (C6); Capability `governance-artifact-integrity` **C2 (no consumer)** | C6 tooling; capability C2 | **INTEGRATION GAP**: the canonical capability has no realizing consumer, while its substance runs as tooling | **refined**: `§4` "capability counterpart (partial)" is a defined Capability whose work is done by tooling, not a realized Capability |
| F-04 | Architecture Governance | CEO A05 (bounded); ADR process; workflows `pre-ratification-validation`, `terminology-audit` **C2** | authority; workflows C2 | **EXECUTION GAP** (workflows defined, never run) + **GOVERNANCE** (FD-2 Founder ≡ Architect still open) | **refined**: `§4` "partial capability" rests on C2 definitions only |
| F-05 | Decision Management | Register; `decision.py`; P13 AuthorityGate; escalation register | C6 | **NO GAP** | none |
| F-06 | Platform Alignment / Coordination | CEO A07 / A08; organization catalog; cross-platform verification | C6 | **NO GAP** | none |
| F-07 | Organizational Development | organization catalog, instance registry; population Founder-reserved (FD-P10-003) | C6 (structure) | **ORGANIZATIONAL** (population reserved), mechanism NO GAP | none |
| F-08 | Performance Management | `performance_evidence.py` (C4); P13 evaluation (C6) | C4 / C6 | **OBSERVABILITY GAP** (minor): performance evidence is not fed by post-P11 roots | **refined** |
| F-09 | Enterprise Assurance / Risk & Compliance | assurance and compliance: P12 verifiers, audits, escalation register (C6). **Risk:** nothing found (no risk register, no risk mechanism in `tools/`, `native_core/`, `consumers/`) | C6 / **C0** | assurance NO GAP · **risk: TRUE CAPABILITY GAP candidate** (GAP-A) | confirmed |
| F-10 | Executive Enablement / Knowledge | Native Core knowledge / memory (C4 consumers), knowledge admission, governance index | C4–C6 | **NO GAP** | none |

**Result.**
- Eight functions have an authority or mechanism counterpart (confirmed).
- F-03 and F-04 are **overstated in `§4`**: what was counted as capability coverage is a C2 definition. Their working coverage comes from tooling and authority.
- Risk management remains the only PD-01-internal true gap candidate.
- No PD-01 function needs to become a new Capability for the three-tier agency to operate (Q8-B finding stands).

---

## C. Agency Capability Map (proven links only)

```text
FOUNDER ──(registered verbatim act; founder_goal VERIFIED)──▶ CEO PLAN            [C6  S-3]
CEO PLAN ──(delegation_requirements → issue_from_plan; delegator = CEO)──▶ GRANT  [C6  S-2, S-3]
GRANT ──▶ engineering-intelligence-instance-001 / -p12w3-005-001
          (engineering-intelligence-agent · capability engineering-intelligence)  [C6]
INSTANCE ──(W4Executor: in-scope success / out-of-scope escalation)──▶ EVIDENCE   [C6  P11 w4, P12 w4]
EVIDENCE ──(reconstruct / operational_state)──▶ CEO-readable state                [C6]
ESCALATION ──(human response only; B1 ledger)──▶ ANSWERED                          [C6  23f315ba]
```

**Not active (shown so that nothing is read as live):**

| Link | State |
|---|---|
| S-2 / S-3 grants → execution | **issued, not executed** |
| execution → verification → CEO acceptance of the outcome as a plan step result | **not resident** (S-4 territory; not started) |
| `cognitive-intelligence` → any instance | **none** (C4 only) |
| `governance-artifact-integrity` → realizing consumer | **none** (work done by tooling under its grant) |
| catalog workflows / skills / tools / substrates at C2 | **not wired** |
| any candidate → anything | **none** |
| agent → agent, agent → delegation, agent → decision | **refused** (NC-2, NC-9; FD-AGENCY-001 Q2-A) |

---

## D. Candidate Executive Mapping

All ten: **CANDIDATE ONLY — NOT CANONICAL — NOT REGISTERED — NOT ACTIVATED** (Q5-C). No instance record anywhere is named after a candidate.

| Candidate | Function | Proven resident counterpart | Level | Gap type |
|---|---|---|---|---|
| Monkey D. Luffy | CEO / Executive Leadership | held by the Co-Founder / CEO office; **not available** (identity reserved) | — | **REQUIRES FOUNDER AUTHORITY** (NC-8 refused) |
| Nami | CFO / Finance | none | C0 | **ORGANIZATIONAL** (outside Platform Organization; GAP-B) → capability gap consequential |
| Roronoa Zoro | COO / Production | W4 delegation / execution, runtime, CEO A02 / A06 | C6 mechanisms | **NO CAPABILITY GAP** (mechanism + authority) |
| Usopp | Creative Director | none ("Creative" is a Volume VI category only) | C0 / C1 | **ORGANIZATIONAL** (GAP-C) |
| Nico Robin | Research & Strategy / Legal | planning (C6), knowledge / memory (C4), `cognitive-intelligence` (C4, never integrated); **legal: none** | C4–C6 / C0 | **PARTIAL**: INTEGRATION (cognitive) + **ORGANIZATIONAL** for legal (GAP-F) |
| Franky | CTO / Engineering | `engineering-intelligence` | **C6** | **NO CAPABILITY GAP**; no candidate instance (by design) |
| Tony Tony Chopper | HRD / People (AI workforce) | organization catalog, instance registry | C6 | **NO CAPABILITY GAP**; population is **ORGANIZATIONAL** (Founder-reserved) |
| Sanji | Hospitality / Client Relations | none | C0 | **ORGANIZATIONAL** (GAP-D; external surface, deployment paused) |
| Jinbe | PM / Risk | planning, W4, escalation (C6); **risk: none** | C6 / C0 | **PARTIAL**: risk = TRUE CAPABILITY GAP candidate (GAP-A) |
| Brook | PR / Social | none | C0 | **ORGANIZATIONAL** (GAP-E; external Tool needed) |

---

## E. True Gap Register

| ID | Gap | Type | Evidence | Route (determination only; nothing started) |
|---|---|---|---|---|
| CG-1 | Risk management (F-09; Jinbe) | **TRUE CAPABILITY** (candidate) | no risk register or mechanism anywhere | First test whether the escalation register plus P13 evaluation can carry a risk view (`§4.2` GAP-A); if not, a Capability decision. Founder / Architect |
| CG-2 | `cognitive-intelligence` never integrated | **INTEGRATION** | C4: probe OK; 0 instances, 0 grants, 0 evidence | creating an instance is CEO authority under FD-P11-001 `§7`, but forbidden by this gate (`§14`); for a later step |
| CG-3 | `governance-artifact-integrity` has no realizing consumer | **INTEGRATION** | 0 consumers; work performed by `tools/corpus_citation_audit.py` under its grant | binding existing tooling as its consumer, or recording tooling as the lawful realization. ADR-0003 owner decision |
| CG-4 | 4 workflows, 7 skills, 5 tool interfaces, 3 substrates defined only | **EXECUTION** | C2: no code, no evidence | none needed now. Several have tooling equivalents (`stale_state_audit` ↔ `staleness-detection`) |
| CG-5 | `governance-corpus-health-check` and two skills only lifecycle-proven | **EXECUTION** | stub performer in W1 evidence | real performer run, when a goal requires it |
| CG-6 | Post-P11 roots and P12 live state are invisible to `operation_roots()`, W3 and E11 | **OBSERVABILITY** | S2-3; this gate's `§A.4` | S-6 territory (unified state view, CC-7) |
| CG-7 | **10 ACTIVE grants + 3 OPEN escalations in certified P12 roots** | **GOVERNANCE** (state disposition) | `§A.4`; certified root, so the S-1 C-3 condition applies | **REQUIRES FOUNDER AUTHORITY**: the A2 / B1 decisions covered P11 only. Extending the live ledger's disposition to P12 grants and answering P12 escalations needs a Founder decision. Not acted on |
| CG-8 | 9 of the 10 P12 grants name instances with no instance record in that root (`engineering-intelligence-instance-001`, `engineering-intelligence-instance-p12w3-001`) | **OBSERVABILITY** | proof runs registered instances in-process (S2-2 / S3-5) | reported with CG-7 |
| CG-9 | Instance registry accepts any well-formed name; the candidate boundary is governance-enforced (S3-4) | **GOVERNANCE** (minor) | S-3 finding | none required; FD-AGENCY-001 conditions 1 and 5 hold |
| CG-10 | Finance, creative, client relations, PR / social, legal | **ORGANIZATIONAL** | C0 | **Founder Decision** (scope expansion), then ADR / Capability (`§4.2` GAP-B…F) |
| CG-11 | Verification result → CEO acceptance as a plan outcome | **INTEGRATION** | not resident (`§C`) | S-4 (not started) |
| CG-12 | FD-2 (Founder ≡ Architect) open, affecting F-04 | **GOVERNANCE** | `§4` F-04 | Founder |

**Not gaps (rejected candidates):**
- Strategic leadership and planning, decision management, coordination, organizational structure, assurance and knowledge each have a C6 counterpart: **NO GAP**.
- COO, CTO and HR(AI) functions: **NO CAPABILITY GAP**.
- The absence of candidate instances is by decision (Q5-C), not a gap.

---

## F. Negative Control Evidence

These were run in memory through the existing lawful interfaces; nothing was written (`negative_controls` in the JSON).

| # | Control | Result |
|---|---|---|
| 1 | Agent cannot hold a capability beyond its definition | refused: `InstanceRegistrationError` |
| 2 | Holding a capability gives no authority to delegate | refused: `DelegationError` |
| 3 | Candidate name is neither canonical nor a recipient | refused: `DelegationError` |
| 4 | Capability not authorized for the recipient | refused: `DelegationError` |
| 5 | Documented-only (C2) capability is not delegable | refused: `DelegationError` |
| 6 | A missing capability is not auto-created | catalog unchanged after the probe (`true`) |
| 7 | A capability cannot change governance (agent answering an escalation) | refused: `EscalationRegisterError` |
| 8 | Luffy is not the CEO (candidate label as delegator) | refused: `DelegationError` |
| 9 | Agent cannot delegate to an agent | refused: `DelegationError` |
| 10 | Capability boundary not bypassed in execution | in-scope step `success`; out-of-scope step **escalation** |

All ten held. Certified evidence integrity reports no faults, and the certified roots are git-clean.

---

## G. Reconciliation Conclusion

| Heading | Finding |
|---|---|
| **WHAT EXISTS** | 3 canonical Capabilities. A complete Founder → CEO → Agent authority path (S-1…S-3). Native Core runtime, execution, tool, knowledge and memory subsystems. Governance tooling. The execution catalog (6 workflows, 11 skills, 5 tool interfaces, 3 substrates) |
| **PARTIAL** | `governance-artifact-integrity` (defined, governed, performed by tooling, no consumer). F-03 / F-04 coverage. Robin and Jinbe functions. Two skills and one workflow proven only as lifecycle |
| **ONLY DOCUMENTED** | PD-01 (frozen) and its stewardship functions. The ten candidates. 4 workflows, 7 skills, 5 tool interfaces, 3 substrates (C2). Risk / finance / legal / creative / client / PR as named functions |
| **EXECUTABLE** | `cognitive-intelligence` (C4). Platform consumers knowledge / memory / tool / reference. `performance_evidence` |
| **INTEGRATED** | `engineering-intelligence` (C6). Planning → delegation → instance → execution → evidence → reconstruction. Escalation with human-only response. Founder Goal verification. Two catalog workflows and four skills |
| **MISSING** | Risk management (CG-1). Legal, finance, creative, client relations and PR / social (CG-10). A resident outcome-acceptance link (CG-11) |
| **NOT A CAPABILITY GAP** | Executive leadership (authority), planning, decision management, coordination, organizational structure, assurance, knowledge, COO / CTO / HR(AI) functions. The integration, execution and observability items CG-2…CG-6 and CG-8 |
| **REQUIRES FOUNDER AUTHORITY** | CG-7: disposition of the 10 P12 ACTIVE grants and 3 P12 OPEN escalations in certified roots. CG-10: organizational scope expansion. CG-12: FD-2. CG-1 (Founder / Architect), if no existing mechanism suffices. Any CEO-identity question (Luffy). Any activation of PD-01, candidates or deployment |

**Main determination.** AIOS does not lack the capability to run its three-tier agency for engineering work. What it lacks is:
- **integration** of what already exists: `cognitive-intelligence`, `governance-artifact-integrity`, the outcome-acceptance link;
- **observability** across all roots;
- **Founder decisions** on organizational scope and on the P12 live state.

"NOT FOUND ≠ NEW CAPABILITY REQUIRED" holds: the only true capability gap candidate is risk management, and even that must first be tested against existing mechanisms.

**Gate status: EXHAUSTED → REPORTED → STOPPED.**
- Nothing built, activated or delegated.
- Governance unchanged.
- This result is the input to S-4; S-4 is not started.
