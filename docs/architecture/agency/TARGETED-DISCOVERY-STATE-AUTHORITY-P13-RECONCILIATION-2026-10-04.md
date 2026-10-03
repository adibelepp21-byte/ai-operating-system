# Targeted Discovery — State Authority, P13 Change Boundary & Agency Frontier Reconciliation

| Field | Value |
|---|---|
| **Directive** | `docs/governance/acts/DIR-AIOS-AGENCY-TD-STATE-AUTHORITY-P13-RECONCILIATION.md` (verbatim; content sha256 `e9a6bd6d62b7286cf5bc55814f7d01a08fee009190725a7e2537b12c3b9b8467`). Register `§155` (receipt), `§156` (result). The directive names this record 2026-10-04; the session date is 2026-10-03 |
| **Mode** | READ-ONLY. P12-W2, P13, W3, Agency state, delegations, plans, Runtime, Trace, governance and deployment are untouched. The Register received only its receipt and result entries; no existing entry was edited |
| **Evidence** | • Baseline: `evidence/td_state_authority_baseline.py` → `evidence/TD-STATE-AUTHORITY-BASELINE-2026-10-04.json` (`a7a0860`, before discovery).<br>• Discovery: `evidence/td_state_authority_discovery.py` (READ-ONLY EVIDENCE TOOL) → `evidence/TD-STATE-AUTHORITY-DISCOVERY-2026-10-04.json`, **all_ok**.<br>• 22 surfaces equal to baseline (only this record's folder differs). A second process reproduces the overview and the P12-W2 delegation entry |
| **Outcomes** | **K-7-B** · **K-8-B** (a direct Agency source would be K-8-C) · labels S-1…S-4 **L-A**, S-5 / S-6 **L-B**, S-7 **L-D** |
| **Next gate** | **FOUNDER DECISION REQUIRED**: one isolated question, FQ-TD-1 (`§R`) |

---

## A. S-6 baseline

S-6 (`§154`) left this position:
- the Agency chain is continuous through Plan Outcome;
- FR-1 (operational state → canonical state → executive re-discovery) is the next frontier by dependency;
- FR-2 (Runtime / Trace), FR-3 (continuous operation) and FR-4 (organizational scope) are reported separately;
- K-7, K-8 and the `§5` label reuse are open.

Nothing in S-1 … MR-S5-1 is reopened here. No new evidence contradicts them.

## B. K-7 State authority analysis

| Source | Purpose | Authority source | Inputs | State model | Scope | Certification | Current / historical | Consumers | Update | Re-discovery role |
|---|---|---|---|---|---|---|---|---|---|---|
| **P12-W2 Unified Operational State** (`tools/p12_operational_state.py`) | *"the system-wide integration layer"* | P12 Authorization D7 and `§15` (Founder); certified P12 Blueprint `§13`–`§19` | 8 declared sources. `delegation.granted` reads 4 P11 / P12 roots *"as stored"* | per entry `CURRENT` / `STALE` / `UNKNOWN`; `is_authority()` always False | P11 + P12 roots. **No Agency root; no live ledger** | P12 certified (FD-P12-006); its record `P12-W2-UNIFIED-OPERATIONAL-STATE.md` is certified evidence. Code is supporting implementation | presents record status as `CURRENT` | **P12 verifiers / measurements only**; no other resident consumer | re-derived on every call | none today. The certified P13 Blueprint names it a P13 input; the code does not wire it (`§F`) |
| **P13 executive state** (`tools/p13/state.py`) | OBSERVE / UNDERSTAND | P13-018; P13-ENV-01 item 2; FDR-G2 C8 | memory, self-model, integrity, native core, corpus, knowledge, authority, remembered, S-OPS | `Fact` with VERIFIED / INFERRED / UNKNOWN | governance / certification facts. **No Agency state** | P13 certified (FDR-7); only the Blueprint is in the certified root | escalations read with the register's **historical** rule (via the P12 self-model) | P13 cycle | per cycle (by hand; last 2026-09-24) | the only resident RE-DISCOVER stage |
| **W3 organizational projection** (`tools/delegation_reconciliation.py`) | organizational representation of grants | DP-01 `§3` W3; FD-P11-001 `§20` | P11 roots only (`operation_roots()`) | representation role CURRENT / HISTORICAL. *"W3 never states a delegation status"* | P11, **fixed by FD-CG7-001 R-2** (W3, E11 and certified P11 measurements read it) | P11 machinery | role only, not lifecycle | organization catalog | rotation by generator | none |
| **S-1 live operational ledger** (`w4_delegation.record_disposition` / `read_dispositions`) | **current terminal disposition of delegations** | Founder **A2** (`§136`), **B1** (`§137`); FD-CG7-001 FQ-CG7-1 / 2; FD-P11-001 `§15.2` | dispositions and responses, hash-bound to records | `COMPLETED` / `REVOKED`; responses `ANSWERED` | every root (`DISPOSITION_SCOPES`) | operational, outside certified roots | **current** by Founder decision | `w4_continuity`, `plan_outcome` | append-only, delegator-only | input |
| **CG-7 operational overview** (`w4_continuity.operational_overview`) | historical **and** operational reading per grant / escalation | FD-CG7-001 **R-2 / R-3** | `all_operation_roots()`; `reconstruct` + `operational_state` | CURRENT OPERATIONAL GRANT / HISTORICAL RECORD; BLOCKING / HISTORICAL / ANSWERED | every phase | operational reader | both, labelled | **none resident** (evidence scripts only) | on read | could serve one; serves none |
| **S-4 plan outcome** (`w4_delegation.plan_outcome`) | plan-step outcome per goal | FD-P11-001 `§15.2`; S-4 (`§148`) | planning surface + grants + ledger | derived step and plan completion; founder acceptance NOT RECORDED | one surface, root given by the caller | operational reader | derived current | **none resident** | on read | — |
| **MR-S5-1 decision provenance** | which decision closed a grant | MR-S5-1 (`§152`) | ledger fields | ACCEPT / REWORK / REJECT; EXPLICIT / LEGACY | as ledger | operational | current | `plan_outcome` | append-only | — |
| **Governance baseline / canonical architecture** | — | — | — | the certified P12 Blueprint `§17`: `STATE → AUTHORITATIVE SOURCE → PROJECTION → CONSUMER`; a two-surface claim is a *"STATE AUTHORITY CONFLICT"* to be resolved or escalated. `§19`: detect *"historical state presented as current"* | — | certified P12 | — | — | — | — |

## C. State reader comparison (one population, four readings)

| Item | P12-W2 | P13 | W3 | Operational (A2 / CG-7) |
|---|---|---|---|---|
| Active grants | **34 grants, 14 active**, entry status `CURRENT` | (no delegation fact) | 4 CURRENT projections | **2 active** (`0a697039a63f4c17`, `50367d99c2dd4708`) |
| The 14 "active" | **all 14 are operationally COMPLETED or REVOKED** (`p12_w2_active_that_are_operationally_closed`) | — | 4 of them are W3's CURRENT | closed by A2 / B1 / FQ-CG7-1 |
| The 2 truly live | **counted 0 of 2**: Agency roots are outside `DELEGATION_ROOTS` | — | **not projected** | live, unexecuted |
| Escalations open | 4 records (no open / answered split) | **4 open** | — | 2 open-historical, 2 answered, **0 blocking** |
| Conflicts the surface itself detects | 0. The live ledger is not a declared source, so nothing contradicts it | — | — | — |

## D. Current vs historical reconciliation (directive `§5`)

| Divergence | Classification | Evidence |
|---|---|---|
| P12-W2 14 active vs 2 | **G — architectural drift** (secondary: **A** stale reader; scope separation not documented in the P12-W2 contract) | P12-W2's `delegation.granted` contract still says *"ACTIVE / REVOKED / SUPERSEDED, derived from records"* and owns *"operational grants and their lifecycle"*. After it was declared, the Founder moved the **current terminal disposition** into the live ledger (A2), and FD-CG7-001 extended it to P12. The contract never followed. The result is exactly what the certified P12 Blueprint `§19` says W2 must detect: *historical state presented as current* |
| P13 4 vs 2 / 0 | **C — historical reader** (secondary: G) | P13 reads `open_escalations` through the P12 self-model with the register's own rule. The response ledger is opt-in (A2 / B1), and S-1 review M-2 documented that historical readers keep the historical view. P13 presents it as a VERIFIED current fact |
| W3 4 CURRENT vs closed; 2 live unprojected | **B — different legitimate state domain** (secondary: C) | W3's CURRENT is a representation role, and W3 *"never states a delegation status"*. Its P11-only population is **documented and decided**: FD-CG7-001 R-2, `delegation_catalog` docstring |
| Any **E — conflicting authority**? | **none found** | No two surfaces claim authority over the same state. P12-W2 asserts none (`is_authority()` False, D7: *"must not take over domain-specific state ownership"*). The operational overview *"writes nothing and holds no state of its own"*. The ledger records disposition by Founder instrument |

## E. K-7 authority conclusion — **K-7-B**

**Existing state mechanisms are complementary, not competing. An explicit integration contract is required.**

| Role | Owner | Basis |
|---|---|---|
| **Domain owner** of the current terminal disposition of delegations, and of escalation responses | the **live operational ledger**, read by the existing delegation readers | A2 *"record the current terminal disposition"*; *"the existing delegation state reader **may** honor this live operational state"*; B1; FD-CG7-001 |
| **System-wide integration layer** | **P12-W2** | P12 D7: *"P12-W2 IS THE SYSTEM-WIDE INTEGRATION LAYER"*; *"must not take over domain-specific state ownership"*; *"no two competing system-wide state authorities"* |

The missing piece is the **contract between them**. Today P12-W2's declared delegation and escalation sources do not name the live ledger, the response ledger or the Agency roots. Under certified P12 `§17`, the contract would be:

> **STATE** — current delegation lifecycle
> → **AUTHORITATIVE SOURCE** — certified records (history) + the A2 ledger (current)
> → **PROJECTION** — P12-W2, distinguishing CURRENT from HISTORICAL as certified `§14` requires
> → **CONSUMER** — P13

**No-competing-state-model test (directive `§6`).**

| Option | Verdict |
|---|---|
| A **new** Agency state view | would duplicate P12-W2's role and create a second *"current"*, against P12 D7, FD-CG7-001 R-2 and P12 `§15`. **Excluded** |
| Routing FR-1 through P12-W2 | is the existing owner of the system-wide role. FR-1 is **an integration contract on an existing mechanism**, not an architectural gap. K-7-D does not apply |

The contract touches only the **source and semantics** columns. The **provider** column stays `UNRESOLVED (F-17)`, which remains a separate, Founder-reserved Phase ↔ PD question.

## F. K-8 P13 certification boundary

| # | Question | Answer (evidence) |
|---|---|---|
| 1 | What was certified? | The **P13 canonical architecture**: `docs/architecture/p13/AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md` is the sole file of the certified manifest (FDR-7 FDQ-7.3 / 7.4; certified commit `6ada59b`) |
| 2 | What was merely implemented? | `tools/p13/*`, the cycle, tests and `docs/operations/p13` records. FDR-7 `§5`: *"Supporting implementation … remain[s] outside the certified architecture root."* (FDR-7 accepted the evidenced implementation as satisfying acceptance; the code is not in any certified manifest) |
| 3 | Source files in the certified semantic boundary | **none**. The boundary is semantic: Blueprint contracts C-01…, `§3` components, the `§4` integration map, `§5` authority, `§7` E13 criteria |
| 4 | *"Supporting-code maintenance"*, in the actual source | FDR-G1 `§8`: *"a supporting-code change that does NOT alter certified architectural meaning remains subject to existing maintenance authority"*. `§9` lists non-material tooling maintenance, test maintenance, **supporting implementation repair**, integrity tooling and operational maintenance |
| 5 | Explicitly permitted after closure | FDR-G2 `§8`, *"where already authorized"*: evidence-only P13 cycles, integrity verification, **system rediscovery**, frontier observation, bounded maintenance, supporting-code maintenance, documentation maintenance, governance analysis, controlled future evolution |
| 6 | What would alter P13 scope | anything outside the certified `§4` integration map or `§10` scope. The map **excludes** *"Workflow, Tool, Agent, Organization (beyond delegations), Runtime — no E13 criterion requires them — not built (`D06`)"* |
| 7 | What would alter certified semantics | FDR-G1 `§9`, presumed material: certified contracts, **interfaces**, scope, acceptance semantics, authority model, **certified dependencies** |
| 8 | What needs Founder certification | any material change: successor Blueprint → verification → Founder certification (FDR-G1; FDR-G2 `§10`). FDR-G1 `§8`: *"If uncertain, the change MUST be escalated rather than classified opportunistically as maintenance."* |
| 9 | Is adding an operational-state source maintenance or evolution? | **It depends on the source.**<br>• **P12-W2:** the certified `§4` map already names *"P12 self-model / operational state → P13 … `tools.p12_operational_state.project()` … consumed"*, but the code never imports it (`p13_code_imports_p12_operational_state: false`; the P12-W5 record (`AIOS_P10_AUTONOMOUS_EXECUTION_VERIFICATION_v1.0.md` `§135.3`) measured P12-W2's non-test consumers as NONE). Wiring it is **implementation conformance repair** inside certified semantics.<br>• **A direct Agency source** (`w4_continuity`, `plan_outcome`, ledgers): outside the map, a new certified dependency, so **architecture evolution** |

## G. P13 source classification

| P13 source | Class | Basis |
|---|---|---|
| `memory` (MemoryReader over Trace) | IMPLEMENTATION of a CANONICAL / CERTIFIED interface; data is HISTORICAL (Trace) | Blueprint `§4` row 1 |
| `self_model` (P12 self-model, 12 answers) | CERTIFIED interface (`§4` row 2); DERIVED VIEW. Escalations: HISTORICAL semantics | `§4` |
| `integrity` | CERTIFIED interface; SUPPORTING CODE (`certified_evidence_integrity`) | `§4` row 3 |
| `native_core` | IMPLEMENTATION; DERIVED VIEW (boundary listing) | `§3` |
| `corpus` | SUPPORTING CODE (audits, governance index); DERIVED VIEW | E13-02 / 06 |
| `knowledge` | CERTIFIED conditional interface; OPERATIONAL DATA (admitted Knowledge) | `§4` row 7 |
| `authority` | CERTIFIED (`§5` envelopes); OPERATIONAL DATA (Delegation Register, envelopes) | `§5` |
| `remembered` | IMPLEMENTATION; HISTORICAL (INFERRED Memory) | `§3` |
| `s_ops` | IMPLEMENTATION added under FDR-3 / FDR-4 (Blueprint `§14`–`§15`); OPERATIONAL DATA (retired surface, historical) | `§15` |
| *(named, not wired)* P12-W2 `project()` | **CERTIFIED interface without implementation** | `§4` row 2 |

**Can Agency operational state become a P13 source?**
- **Yes, through P12-W2**: certified interface; consumption is maintenance once P12-W2 projects it.
- **Not directly**: certified-map change; Founder certification.
- The Blueprint's mention of *"operational state"* is not read as permission to modify P13. What permits wiring P12-W2 is the specific certified `§4` interface row naming that function, together with FDR-G1's repair class.

## H. K-8 authority conclusion — **K-8-B**

**P13 may consume an existing state surface without changing certified semantics.**
- The surface is P12-W2, through the interface the certified Blueprint `§4` already names.
- The observe basis is P13-ENV-01 item 2 (*"authorized reading of AIOS state and evidence"*).
- The authority is FDR-G1 `§8`–`§9` supporting implementation repair.

**K-8-C** applies only to the alternative of a direct Agency source.

**Caveat (dependency, not authority).** Wiring P13 to P12-W2 **today** would import the drifted view: 14 "active" grants, all closed. K-8-B therefore becomes useful only after the K-7-B contract exists (`§J`, `§R`).

## I. FD-AGENCY-001 `§5` label reconciliation

**History.**
- `FD-AGENCY-001` (the Founder instrument) defines **no** S-items (`founder_instrument_defines_s_items: false`).
- The sequence S-1 … S-7 was first defined in the CEO's decision record `FD-AGENCY-001-DECISION-RECORD.md` `§5`, registered at `§133` (*"implementation surface S-1…S-7, none started"*, 2026-10-02, `3eb12bc`).
- The Founder's S-1 directive (*"Do not expand S-1 into S-2–S-7"*) and S-2 directive (*"start S-3, S-4, S-5, S-6, or S-7"*) cite that sequence.
- The S-5 (`§149`) and S-6 (`§153`) directives assign different work to the same labels.
- No Register entry renames or supersedes a `§5` item (`explicit_supersession_or_rename_in_register: false`).

| Label | FD-AGENCY-001 `§5` item | Later Founder directive | Implementation | Classification |
|---|---|---|---|---|
| S-1 | close the 4 W4 grants | S-1 Delegation Closure (`§135`) | complete (`§138`) | **L-A** same work |
| S-2 | CEO plan → W4 grant | S-2 Plan-to-Delegation (`§139`) | complete | **L-A** |
| S-3 | Founder goal intake | S-3 Founder Goal → CEO Planning (`§141`) | complete | **L-A** |
| S-4 | verification → CEO accept / reject / rework | S-4 Evidence → Decision → Plan Outcome (`§148`), completed for REJECT by MR-S5-1 (`§152`) | complete | **L-A** |
| S-5 | P13 reads organizational work state (G-3) | S-5 Disposition Semantics Discovery | `§5` item **not started** | **L-B** different work, label reused; not superseded |
| S-6 | unified Agency state view | S-6 Systemic Frontier Discovery | `§5` item **not started**. It is the substance of FR-1 / K-7-B | **L-B**; not superseded |
| S-7 | resident runtime binding | none yet | not started (FR-2) | **L-D**: no collision yet; the label is exposed to the same reuse |

**Exact minimum correction (reported, not applied; directive `§12`).**
- One appended Register entry, with no edit to `§133`, the decision record or any act.
- It would give the three unstarted `§5` items stable identifiers that cannot collide with directive sequence numbers, for example `FD-AGENCY-001 §5 item 5`, `item 6` and `item 7`.
- It would state that the Founder directives S-5 and S-6 denote other work.

The `§5` surface is a CEO reconciliation record whose items rest on A06 / A12 / A02 authority, not on their labels, so its standing does not depend on the label. **No Founder clarification is needed for the labels themselves (L-E not required).**

## J. FR-1 dependency analysis

| Edge | Exists | Connected | Authorized | Observable | Reconstructable | Verified | Absence |
|---|---|---|---|---|---|---|---|
| Agency operational state (ledger, plans, overview) | yes | yes (internally) | yes (A2, B1, FD-CG7-001, FD-P11-001 `§15.2`) | yes (operational overview, `plan_outcome`) | yes | yes (S-1 … MR-S5-1) | — |
| → authoritative state surface (P12-W2) | P12-W2 yes; edge **no** | **no** | **undetermined** (`§R`) | no | n/a | no | **technical and authority** |
| → P13 / executive state | interface named in the certified Blueprint; code **no** | **no** | **yes** (K-8-B) | no | n/a | no | **technical only**, but useless before the previous edge |
| → executive re-discovery | yes (`frontier.py`) | yes | yes (FDR-G2 C8) | yes | yes | yes (11 cycles; none since 2026-09-24) | — |
| → next CEO action | P13 proposes; Agency actions (`issue.delegation`) RESERVED for P13 | partial by design (Q3-A) | yes: P13 proposes or escalates, the CEO acts | yes | yes | yes | — (by design) |

**Result.** The only edge with an **authority** absence is *operational state → P12-W2*. The P13 edge is a technical absence, authorized but dependent on it.

## K. FR-2 dependency analysis

| Direction | Finding |
|---|---|
| Operational state → Runtime / Trace | no dependency: the S-chain needs nothing from Trace to decide |
| Runtime / Trace → operational state | FR-2 would produce Trace records. P12-W2 already has an `execution.recorded` source, and P13 already has a Memory source over Trace stores, but both read **only the certified P12 Trace root**. FR-2 has its own blocker: residency of a live Trace store, plus RC-2 reserved |

**Classification:** an **independent future frontier** for construction. Its **executive visibility** depends on the FR-1 P12-W2 → P13 edge, or on Trace-store residency. The dependency runs FR-2 → FR-1 for observability only.

## L. FR-3 dependency analysis

These states can be **derived without changing state**, by composing existing readers in the evidence tool:
- COMPLETED: 7;
- REVOKED: 34;
- PENDING (live, not executed): 2, the S-2 and S-3 grants;
- BLOCKED: 0;
- WAITING: 1, `founder-s4-rework / report-continuity-elements`, an open delegated step with no grant;
- HISTORICAL / LIVE: through the overview classification.

**No resident reader names PENDING or WAITING** (`state_words_in_resident_readers` empty). The two roots holding pending grants report *"NO BLOCKING CONDITION — prior state is coherent"*.

**FR-3 requires FR-1.** A cadence would act on the executive view, which today presents 14 closed grants as active and answered escalations as open. FR-3 also stays Founder-gated (autonomous cadence; deployment PAUSED).

## M. FR-4 dependency analysis

*Function → capability → agent → current operational state* **is representable now** by composition (catalog chain + instance records + overview):

| Capability | Department | Instances | Live grants |
|---|---|---|---|
| `engineering-intelligence` | engineering | 2 | 2 |
| `cognitive-intelligence` | engineering | 0 | 0 |
| `governance-artifact-integrity` | platform | 1 | 0 |

FR-4 is **not technically dependent** on FR-1. Its system-wide visibility would flow through the same P12-W2 contract. The candidate functions (finance, creative, legal, client relations, PR / social) stop at the Founder boundary (FD-AGENCY-001 GAP-B…F). Not examined further.

## N. Existing-mechanism exhaustion (`§17`)

| # | Mechanism | Finding |
|---|---|---|
| 1 | P12-W2 | the system-wide layer; drifted delegation and escalation contract |
| 2 | P13 | certified to consume P12-W2; not wired |
| 3 | W3 | separate domain, population fixed by R-2 |
| 4 | S-1 ledger | domain owner of current disposition |
| 5 | S-4 `plan_outcome` | derived plan state; no resident caller |
| 6 | MR-S5-1 provenance | explicit decisions |
| 7 | other readers (`reconstruct`, `operational_state`, overview) | readers, not authorities |
| 8 | P13 self-model | historical escalation rule |
| 9 | organizational projections | W3; organization catalog |
| 10 | provenance | `plan_provenance`; execution manifests |
| 11 | Runtime / Trace | certified Trace root only |
| 12 | governance | P12 D7 / `§15`; A2; B1; FD-CG7-001; FDR-G1; FDR-G2; FDR-7; P13-ENV-01; F-17 |

**No new mechanism is necessary.** FR-1 is an integration contract on P12-W2 plus an already-certified P13 interface.

## O. Negative controls

| # | Control | Result |
|---|---|---|
| N1 | no P13 modification | `tools/p13`, envelopes and the certified P13 root digests equal |
| N2 | no P12-W2 modification | all `tools/p12_*.py` digests equal |
| N3 | no W3 modification | organization tree and state-reader digests equal |
| N4 | no Agency state mutation | operational digest equal |
| N5 | no delegation mutation | operational digest and certified digests equal |
| N6 | no plan mutation | operational digest equal (planning states included) |
| N7 | no Agent creation | instance-record digest equal |
| N8 | no Capability creation | catalog digest equal |
| N9 | no authority expansion | governance digest equal (except Register and acts); delegator unchanged |
| N10 | no Founder Decision inferred from silence | the only new act is this directive's verbatim record |
| N11 | no deployment activation | `vercel.json` and `fullstack` digests equal |
| N12 | no competing state model | all code digests equal; no reader added; the classifications live in the evidence script only |

All 12 held.

## P. Integrity verification

- Run changed nothing (before = after).
- All 22 surfaces equal the baseline: certified P11 / P12 / P13 / platform-organization / `docs/operations`, operational, Agent registry, capability catalog, candidates, governance, P13 code, envelopes, state readers, P12 code, all code, deployment, root entry points.
- Register only appended. Directive act unchanged.
- Certified-evidence integrity: no faults. Certified roots git-clean.
- Fresh-process reconstruction identical.

## Q. Remaining unknowns

| ID | Unknown | Why it matters |
|---|---|---|
| U-1 | whether the K-7-B contract is FDR-G1 maintenance or a certified P12 change | the only authority absence on FR-1 (`§R`) |
| U-2 | whether post-P13 Agency roots fall inside P12's *"system-wide"* population. P12 is a certified, closed phase; D7 says system-wide unified state *"belongs to P12"* | part of FQ-TD-1 |
| U-3 | how P12-W2 can add the current view without moving the population that certified P12 verifiers read (provenance, failure, workflow, governance join all use `DELEGATION_ROOTS`) | design constraint for any contract (R-2 precedent) |
| U-4 | whether P13's escalation fact should honour B1 / FQ-CG7-2 responses. The certified interface is `open_escalations`; the response ledger is opt-in | follows from the same contract, through P12-W2's `escalation.raised` |
| U-5 | the F-17 provider column | unchanged and Founder-reserved; the contract must leave it UNRESOLVED |

## R. Authority / Founder decisions required

**FQ-TD-1 — the classification and route of the P12-W2 ↔ live-operational-ledger integration contract.**

- **Why it is the Founder's.** FDR-G1 `§9` presumes changes to certified interfaces and dependencies material, and `§8` requires escalation when the maintenance / change boundary *"cannot be established confidently"*.
- **The argument both ways:**
  - The change *implements* certified P12 semantics (`§14`, `§17`, `§19`) and A2's *"may honor"*.
  - It also changes the declared source contract described in certified P12 evidence (`P12-W2-UNIFIED-OPERATIONAL-STATE.md` `§3`), and may extend P12's population to post-P13 roots (U-2).
- **Result.** The boundary cannot be established confidently from the record, so the rule sends it to the Founder.

| Option | Meaning | Consequence |
|---|---|---|
| **A** (CEO recommendation) | Classify it as FDR-G1 implementation maintenance:<br>• P12-W2 projects the A2 / FD-CG7-001 ledger and the Agency roots, CURRENT vs HISTORICAL;<br>• the populations read by certified P12 verifiers are unchanged;<br>• F-17 is untouched | then P13 → P12-W2 wiring (K-8-B) completes FR-1 as **minimal integration construction** |
| B | A certified P12 architecture change | successor P12-W2 contract → verification → Founder certification before construction |
| C | P13 reads Agency state directly | certified P13 change (K-8-C), successor Blueprint → certification. P12-W2 stays historical, so two *"current"* views exist (against P12 D7) |
| D | Defer FR-1 | executive state stays historical. FR-3 stays blocked |

Nothing else needs the Founder for FR-1:
- K-8-B is within authority;
- the labels need only the reported Register note (`§I`);
- FR-2, FR-3 and FR-4 keep the gates already recorded.

## S. Recommended next gate — **FOUNDER DECISION REQUIRED**

FQ-TD-1 is a Founder-reserved classification under FDR-G1 `§8`–`§9`, and it blocks the only edge of FR-1 that lacks authority.

**Why not another type:**
- *Targeted discovery continues:* further discovery cannot settle a boundary the instruments assign to the Founder when it is uncertain.
- *Minimal integration construction:* the necessary first edge is not authorized yet. K-8-B alone would wire P13 to a drifted view.
- *FR-1 not the correct frontier:* no other dependency precedes it.

**Nothing was constructed.** FR-1 stays a DISCOVERED FRONTIER until FQ-TD-1 is answered.
