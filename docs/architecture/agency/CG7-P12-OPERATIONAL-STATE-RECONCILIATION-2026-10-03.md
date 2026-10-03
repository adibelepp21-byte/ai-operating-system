# CG-7 — P12 Operational State Reconciliation (2026-10-03)

| Field | Value |
|---|---|
| **Directive** | `docs/governance/acts/DIR-AIOS-CG7-P12-OPERATIONAL-STATE-RECONCILIATION-GATE.md` (verbatim; content sha256 `083b9fb5dcb8c35e6a9aab3762ac03cbdce8a7dbcc89ced230b92eecd1d1d133`). Register `§144` |
| **Mode** | READ-ONLY. Nothing was issued, revoked, completed, answered, closed, moved, registered or rewritten. S-4 not started |
| **Evidence** | `evidence/cg7_p12_state_reconciliation.py`, a **READ-ONLY EVIDENCE TOOL** that nothing imports. Its output is `evidence/CG7-P12-STATE-RECONCILIATION-2026-10-03.json` |
| **Integrity** | Before any reader ran, the tool hashed:<br>• 122 P12 files;<br>• 55 grant / escalation / response / instance / disposition / join records repository-wide;<br>• the Register and the P12 manifest.<br>It hashed them again after every reader ran. **BEFORE = AFTER** (`changed`: none). P12 manifest: 121 / 121 entries match. Certified evidence integrity: no faults. Certified roots git-clean before and after |
| **Result** | Discovery exhausted. One grant (`2494015d`) and its escalation (`9cb90fa0`) are **live by the directive's own test**. Nine grants and two escalations are **historical proof state** that the readers still present as current. Separation without changing certified bytes is **possible**: the S-1 mechanism already does it for P11. Extending it to P12 needs **Founder authority**, plus a **reader fix** first |

**Terms used** (`§15`):

| Term | Meaning here |
|---|---|
| ACTIVE | the `status` field in the record |
| LIVE | the directive's five-part test (`§6C`): an ACTIVE record, a current operational reader, valid authority, a valid recipient and a non-terminated state, all true |
| REGISTERED | a persisted instance record in the root that holds the grant. The registries are in-process only (S2-2), and a fresh process sees only persisted records |
| CURRENT | what an operational reader today would act on |

---

## A. P12 State Inventory

### A.0 Baseline (`§5`)

```text
P12 BASELINE
Commit:                ee7f6de37d6ae8b9d55da365265a8f9b03c706eb
Certified files:       docs/architecture/p12/** — 122 files; certified by FD-P12-006
                       (manifest AIOS_P12_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json, 121 entries,
                       certified commit 6968c6e, 2026-09-18). The one file outside the manifest
                       is AIOS-P12-FINAL-CERTIFICATION-AND-P13-TRANSITION-HANDOFF-RECORD.md
                       (added by e5ac0f5, ACT-CC-P12-028, after the certified commit). It is
                       inside the protected root
Certified bytes/hash:  tree digest 5be77e5634d78b237fc7a5ab781c7e0d754f76ccb4e791284349efc0c7a15cf9
                       (sha256 over the per-file sha256 map); 121/121 manifest hashes match
Operational folders:   docs/architecture/p12/w4-operations, docs/architecture/p12/w3-operations.
                       Both are INSIDE the certified root (is_protected = True)
ACTIVE grants:         10 (all in w4-operations)
OPEN escalations:      3 (w4: 9cb90fa0787a478c · w3: 0991300404cf44d8, 9d6bc0ad47294ef0)
Readers used:          w4_continuity.reconstruct · w4_continuity.operational_state ·
                       w4_delegation.read_dispositions / plan_completion ·
                       EscalationRegister.open_escalations / status ·
                       delegation_catalog.operation_roots · p12_execution_chain_reader.summary ·
                       p12_provenance_verification.summary · p12_failure_verification.escalation_join
```

**"Certified folder" was tested, not assumed.**
- Every grant, escalation, join, instance and evidence file in both operations folders is a **manifest entry** with a matching hash.
- Every one was created by exactly one commit and never touched again.
- All seven creating commits are ancestors of the certified commit `6968c6e`.
- The operational records are therefore certified historical bytes. The open question is whether any of them is *also* current state (`§D`).

### A.1 Surfaces

| Surface | Contents |
|---|---|
| P12 certified surfaces | `docs/architecture/p12/**` (122 files) |
| P12 operational surfaces | none outside the certified root. The live S-1 ledgers (`agency/operations/w4-dispositions/`, `agency/operations/escalation-responses/`) hold **no P12 entry** |
| Grant records | 10 × `p12/w4-operations/*.delegation.json` |
| Escalation records | `p12/w4-operations/9cb90fa0787a478c.escalation.json`; `p12/w3-operations/0991300404cf44d8.escalation.json`, `9d6bc0ad47294ef0.escalation.json`. Each has a `*.governance-join.json` beside it |
| Agent registries | `AgentInstanceRegistry` / `W4DelegationRegistry`, in-process. One persisted P12 instance record: `engineering-intelligence-instance-p12w3-005-001.instance.json` |
| Capability registries | `tools/organization_catalog.read_departments()`: `engineering-intelligence` (**C6**, Capability Discovery gate, `§143`) |
| State readers | listed in the baseline above |
| Execution evidence | 5 execution manifests in `p12/execution-provenance/`; trace stores in `p12/trace-stores/` (`p12-w4-integrated-execution` holds 3 records, the others 1 each); `p12/w4-operations/first-execution.evidence.json` |

---

## B. Grant Reconciliation

**Common to all ten** (each item checked per record in the JSON `grants`):

| Property | Finding |
|---|---|
| Delegator | `Claude Code / AIOS Co-Founder`, equal to `AUTHORIZED_DELEGATOR` (the CEO) |
| Authority | `FD-P11-001 §9`; the citation resolves (`authority_citation.refusal` → none) |
| Capability | `engineering-intelligence` (C6), within `engineering-intelligence-agent` v1.0 |
| Record shape | key set identical to what `W4DelegationRegistry.issue` emits today |
| Never modified since creation | one commit each |
| Escalation response | none beside the record; none in the live ledger |
| Revocation fields | none |

**Creation mechanism.**
- The sanctioned issuer `W4DelegationRegistry.issue` was called by a named producer script that writes into this root.
- `issue()` refuses an unregistered recipient (`tools/w4_delegation.py:217`). Each persisted grant therefore proves its recipient **was registered in the issuing process**.

### B.1 The ten grants

| Grant | Producer → plan | Created | Recipient (instance status) | Execution evidence | Escalation | Live? | Valid? | Classification |
|---|---|---|---|---|---|---|---|---|
| `e668a317fa494342` | `p12_w4_integrated_execution.py 001` → `p12-w4-integrated-execution-plan-0` | `a79ef24` 2026-09-12 | `engineering-intelligence-instance-001`: registered in-process only (`AgentInstanceRegistry(root=None)`); **no record in this root** | manifest `…-001`, **success** 14/14, trace store `p12-w4-integrated-execution` #1, chain **JOINED** | — | **NO** | YES | **HISTORICAL ONLY** |
| `b304c7ecb1024454` | same, run `002` → `…-failure-plan-0` | `e9a042b` 2026-09-12 | same | manifest `…-002`, **failure** 5/14 (the subject deliberately lacks the elements), trace `…-failure` #0, JOINED | — | NO | YES | **HISTORICAL ONLY** |
| `84e94ea2f001444d` | run `003` → `p12-w2-state-transition-plan-0` | `fcfcc1d` 2026-09-12 | same | manifest `…-003`, failure 4/14, trace `p12-w2-state-transition` #0, JOINED | — | NO | YES | **HISTORICAL ONLY** |
| `08e14bd7aa584ea5` | run `004` → `p12-w1-integration-edge-plan-0` | `a13cf95` 2026-09-12 | same | manifest `…-004`, failure 3/14, trace `p12-w1-integration-edge` #0, JOINED | — | NO | YES | **HISTORICAL ONLY** |
| `632b256f8335434f` | run `005` → `p12-live-verification-plan-0` | `9d3ea4f` 2026-09-18 (FD-P12-006 live verification `§11`) | same | manifest `…-005`, failure 3/14, trace `p12-live-verification` #0, JOINED | — | NO | YES | **HISTORICAL ONLY** |
| `332d42f021764ab6` | run `001` → `p12-w4-integrated-execution-plan-0` | `a79ef24` 2026-09-12, 24 s before `e668…` | same | **no manifest**. A trace record (#0) was co-created in the same commit, but trace records carry no delegation id, so the join is **UNVERIFIED**. P12 classified this execution `CLASS D`, *"the run before manifests existed"* (`P12-027-SECTION-6-7-FRONTIER-DETERMINATION.md §5`) | — | NO | YES | **HISTORICAL ONLY** (execution join UNKNOWN by id) |
| `522e84af52444890` | run `001` again (plan key unique to run `001`) | `9d3ea4f` 2026-09-18 15:53:31, 5 s after the live test started | same | **no manifest**. A trace record (#2) was co-created; join by id **UNVERIFIED**. `P12-LIVE-OPERATIONAL-VERIFICATION-RECORD.md §D.2` describes this run: the default `001` was re-invoked, `record()` refused the duplicate manifest, and the delegation was already persisted (*"the `§28` chain is not atomic"*) | — | NO | YES | **HISTORICAL ONLY** (execution join UNKNOWN by id) |
| `aa591daf55ca4714` | `p12_w3_governance_escalation.py` → `p12-w3-governance-escalation-plan-0` | `a094f2c` 2026-09-16 (P12-003) | `engineering-intelligence-instance-p12w3-001`: in-process only; **no record anywhere** | `W4Executor` ran the plan: the in-scope step was performed by a stub (*"satisfied by delegation issuance"*), and the out-of-scope step was refused | `0991300404cf44d8` (structural join) | NO | YES | **HISTORICAL ONLY** |
| `e6a3d622cfb54b4f` | same producer and plan, re-run | `9d3ea4f` 2026-09-18 (live verification) | same | same shape | `9d6bc0ad47294ef0` | NO | YES | **HISTORICAL ONLY** |
| `2494015de36246fd` | `p12_w3_resident_wiring_proof.py` → `tools/w4_first_run.run(OPERATIONS=p12/w4-operations)` → `w4-first-execution-proof-plan-0` | `0f39339` 2026-09-16 (P12-005) | `engineering-intelligence-instance-p12w3-005-001`: **REGISTERED, persisted in this root** (created by the CEO under `FD-P11-001 §7`, lifecycle `REGISTERED`, not retired) | `first-execution.evidence.json`: `verify-delegation-elements` **success** 14/14; `report-conformance` **escalation** | `9cb90fa0787a478c` | **YES** | YES | **LIVE / VALID** |

**Why nine are "not live".** Each fails at least one part of the five-part test:
- **Valid recipient: NO.** No persisted registration of its recipient exists in the root that holds it, so a fresh process cannot execute against it. The `w3` reader states this directly: *"NO LIVE AGENT INSTANCE — nothing may execute"*.
- **Non-terminated: NO or UNKNOWN.** Each was bound to *"one execution of plan …"*. That one execution happened for seven of the nine (manifest-joined or escalation-joined); for `332d…` and `522e…` the execution is documented only by description.

The *ACTIVE* status in these records is the **unrecorded end of a proof run**. The producers never terminate their grants, and `p12_w3_resident_wiring_proof.py` says other P12 evidence *"depends on staying `ACTIVE`"*.

**Why `2494015d` is live.** All five parts are true:
- ACTIVE record;
- the operational reader reports it active;
- authority resolves;
- the recipient is persisted and REGISTERED in the same root;
- the termination condition (*"on completion of the bound plan, or on revocation by the authorized delegator"*) is unmet: the plan did not complete, because step 2 escalated, and no revocation exists.

It is the exact twin of the P11 pair `4313bd22` / `23f315ba` that the Founder settled under B1 (`§137`).
- It is **blocked**: its open escalation stops further work under it.
- It **cannot advance in place**: its root is write-protected, and any re-run of the producer into this root is refused by `p12_certified_evidence_guard`.

### B.2 Recipient / instance reconciliation (`§7`)

| Recipient | Grants | Case | Evidence |
|---|---|---|---|
| `engineering-intelligence-instance-001` | 7 | **B**: existed historically (registered in-process at issuance, proven by `issue()`'s check), not live in this root | producer: `AgentInstanceRegistry(root=None).register(...)` then `issue(...)`. The same key is persisted in **other** roots (P11 `w4`, P11 `x-department`, S-2, S-3) as separate per-root registrations, so **Case A does not hold**: no registry is global |
| `engineering-intelligence-instance-p12w3-001` | 2 | **B** | producer `p12_w3_governance_escalation.py`: `AgentInstanceRegistry(root=None)`; persisted nowhere |
| `engineering-intelligence-instance-p12w3-005-001` | 1 | **A**, in the same root | `p12/w4-operations/engineering-intelligence-instance-p12w3-005-001.instance.json` |

- **Not Case C:** the registry model predates P12 (P11).
- **Not Case D:** issuance refuses unregistered recipients.
- **Not Case E:** the evidence suffices.

The Capability Discovery finding *"9 of the 10 P12 grants name agent instances that have no instance record in that folder"* is **independently confirmed**.

### B.3 Capability validity (`§8`)

All ten cite `engineering-intelligence`: **C6**, from the prior gate, not upgraded here. Execution is shown **per grant** by its own evidence (`§B.1`), not inferred from the capability level:
- confirmed for 8;
- UNKNOWN by id for 2.

---

## C. Escalation Reconciliation

| Escalation | Origin (verified) | Issuer / actor | Authority cited | Related grant | Reason (from the producer, not only the text) | Created | Response | Current reader | Live? | Valid? | Classification |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `9cb90fa0787a478c` (`w4`) | `tools/w4_first_run.run` driven by `p12_w3_resident_wiring_proof.py` (ACT-CC-P12-005); refusal by `W4Executor`, recorded by `record_refusals`, joined by `join_refusals_to_grants` | system (`W4Executor`) in a run under grant `2494015d` | `FD-P11-001 §9` | `2494015d` (structural join) | deliberately reproduced out-of-scope refusal: the producer passes `work_scope=("verify-delegation-elements",)` explicitly so that `report-conformance` is refused | `0f39339` 2026-09-16 | none beside the record; none in the live ledger | OPEN (historical **and** operational) | **YES**: it blocks the only live grant | YES | **OPEN / LIVE** |
| `0991300404cf44d8` (`w3`) | `p12_w3_governance_escalation.py` (P12-003, W4-GAP-008 proof) | system (`W4Executor`) | `FD-P11-001 §9` | `aa591daf` | deliberately out-of-scope step `report-governance-join-proof`, a proof of the structural join | `a094f2c` 2026-09-16 | none | OPEN; same root reports *"NO LIVE AGENT INSTANCE — nothing may execute"* | **NO**: its grant's recipient was never persisted, so no work can resume under it | YES | **OPEN / HISTORICAL** |
| `9d6bc0ad47294ef0` (`w3`) | same producer, re-run in the FD-P12-006 live verification (`9d3ea4f`) | system (`W4Executor`) | `FD-P11-001 §9` | `e6a3d622` | same | `9d3ea4f` 2026-09-18 | none | same | **NO** | YES | **OPEN / HISTORICAL** |

**Authority required to answer any of the three:**
- `EscalationRegister.record_response` accepts only a `HumanAuthority`: *"automation cannot close an escalation"*.
- For a certified root, B1 routes the response to the live ledger.
- The precedent responder is the Founder (B1, `§137`).

**Prior status.** The post-P13 baseline report already recorded all three as *"separate and unanswered"*. It judged them non-blocking **by inference only**: FD-P12-006 certified P12 with them resident, and no Founder text says they are non-blocking.

---

## D. Certified / Operational Separation Map

```text
CERTIFIED HISTORICAL (FD-P12-006; byte-guarded)
    docs/architecture/p12/**  — 122 files, including:
      w4-operations/  10 grants · 1 escalation + join · 1 instance · first-execution evidence
      w3-operations/  2 escalations + joins
      execution-provenance/ · trace-stores/ · runtime-observations/ …
    readers: reconstruct(), EscalationRegister, p12_execution_chain_reader,
             p12_provenance_verification, p12_failure_verification

OPERATIONAL CURRENT (outside every certified root)
    agency/operations/w4-dispositions/        — S-1 A2 ledger: P11 entries only
    agency/operations/escalation-responses/   — S-1 B1 ledger: P11 entry only
    agency/operations/w4-s2-plan-delegation/, w4-s3-founder-goal/  — live roots
    reader: operational_state() = reconstruct() + those ledgers

OVERLAP / MIXING
    p12/w4-operations, p12/w3-operations: one set of bytes is BOTH certified evidence AND
    the only lifecycle source for those grants and escalations. No P12 entry exists in
    the operational ledgers, so operational_state() can only repeat the historical
    status. It calls 10 grants ACTIVE and raises "MORE THAN ONE LIVE GRANT FOR ONE
    INSTANCE", although 9 cannot execute.
```

| Surface | Historical | Operational | Mixed | Evidence |
|---|---|---|---|---|
| Grant state (`p12/w4-operations`) | YES | YES (as read by `operational_state`) | **YES** | 10 manifest entries; `operational_state` returns all 10 ACTIVE with no P12 disposition |
| Escalation state (`p12/w3`, `p12/w4`) | YES | YES | **YES** | `EscalationRegister.open_escalations` = 3; no response anywhere |
| Agent registry | NO persisted P12 registry beyond one instance record | in-process only | NO (absent rather than mixed) | `AgentInstanceRegistry(root=None)` in both W4 / W3 producers |
| Execution state (trace stores, manifests, evidence) | YES | NO | NO | write-once, joined by `p12_execution_chain_reader` (5 / 5 JOINED) |
| Evidence | YES | NO | NO | manifest hashes 121 / 121 |

**Can operational state be separated without changing certified bytes? YES.** The evidence is that this exact separation already runs for P11:
- S-1 A2 / B1 record dispositions and responses **outside** the certified root;
- each entry is bound to the certified record's sha256;
- `operational_state()` honours them, while `reconstruct()` keeps the historical reading;
- every certified P11 byte is unchanged (S-1 closure review R4; integrity "no faults" here).

The separation boundary is:

| Side | Location | Notes |
|---|---|---|
| Certified historical | `docs/architecture/p12/**` | unchanged |
| Operational current | the existing live ledgers | one entry per P12 grant / escalation, hash-bound to the certified record, keyed by **full root path** |

**Two things stand in the way. Neither is a byte change.**
1. **Authority.** A2's text is scoped to P11 (*"Maintain the certified P11 delegation records … outside the certified P11 evidence boundary"*), and the ledger's recording authority is `FD-AGENCY-001 S-1 Q-S1-A (A2)`.
2. **The ledger's folder key (finding R-1, below).** A P12 entry would land in the same folder as P11's.

The separation was **not implemented**.

---

## E. State Reader Findings

| Reader | Input | Output for P12 | Historical aware | Operational aware | Conflation risk | Verdict |
|---|---|---|---|---|---|---|
| `w4_continuity.reconstruct` | the root's records | 10 ACTIVE; 1 / 2 OPEN | YES (by design: the record as written) | NO | low; documented as the historical reading | **CORRECT** |
| `w4_continuity.operational_state` (S-1) | `reconstruct` + live ledgers | 10 ACTIVE; 1 / 2 OPEN; duplicate-active condition; **plus a spurious disposition fault** (R-1) | YES | partial: honours ledgers, has no P12 entries, cannot tell proof state from current state | **HIGH**: what the Capability Discovery gate reported as live state | **MISLEADING** for P12 (R-1, R-3) |
| `read_dispositions` | `LIVE_LEDGER / Path(root).name` | fault: *"4313bd22…disposition.json: recorded for root 'docs/architecture/p11/w4-operations'; its delegation record is missing"* | — | — | P11 and P12 share the basename `w4-operations` | **MISLEADING** (R-1) |
| `w4_delegation.plan_completion` | `*.evidence.json` in the root; clause text *"completion of the bound plan"* | `met = False` for all 10. For 8, *"termination condition does not name completion of the bound plan"*; P12 phrases it *"on completion of plan <key>"* and its evidence is a manifest elsewhere | — | — | cannot judge P12-format grants | **PARTIAL** (R-4) |
| `EscalationRegister.open_escalations` / `status` | root files + live response ledger | OPEN × 3 | YES | YES (B1 ledger) | none: it says OPEN, not that work is waiting | **CORRECT** |
| `delegation_catalog.operation_roots` (→ W3 `delegation_reconciliation`, `e11_measurement`) | `docs/architecture/p11/**` only | P12 **not seen** | — | — | P12 state invisible to W3 / E11; the origin of the earlier undercount | **STALE** (scope inherited from P11; R-2) |
| `p12_execution_chain_reader.summary` | manifests + `DELEGATION_DIRS` incl. P12 | 5 manifests, 5 JOINED | YES | NO (not its purpose) | none | **CORRECT** |
| `p12_provenance_verification.summary` | `DELEGATION_ROOTS` incl. P12 | 19 executions, 8 joined, `NOT ASSEMBLABLE` | YES | NO | none | **CORRECT** (records the CLASS D population) |
| `p12_failure_verification.escalation_join` | `docs/architecture/**/*.escalation.json` | 4 records; 3 joined by the governance surface | YES | NO | none | **CORRECT** |

**Why "10 ACTIVE / 3 OPEN" appears in current state.**
- The prior gate's script read every W4 root with `operational_state()`.
- For P12, that reader has nothing to apply but the historical bytes.
- Its contract is *historical status unless a valid disposition exists*. Nothing in it distinguishes a proof run's leftover grant from a current one.
- This is a **documented behaviour plus a scope gap**, not a defect in the bytes. The basename collision (R-1) is a defect.

### E.1 S-1 boundary versus P12 (`§13`)

| | S-1 | P12 |
|---|---|---|
| Population | exactly 4 grants in `p11/{w1,w4,x-department}-operations` (S-1 record, *"Scope … the four W4 grants ACTIVE since 2026-09-11"*) + escalation `23f315ba` | 10 grants + 3 escalations in `p12/{w4,w3}-operations` |
| Discovery | `delegation_catalog.operation_roots()`, P11 only | not reached by that discovery |
| Authority | A2 / B1: Founder text names P11 explicitly | none |
| Timing | S-1 2026-10-02 (Register `§135`–`§138`) | all P12 state created 2026-09-12…18, before S-1, and certified 2026-09-18 |
| Intentionally outside? | **Not stated either way**; the omission follows from the P11-only discovery | — |
| Applies conceptually? | **YES**: the same certified-ledger condition (S-1 C-3) and the same mechanism | — |

S-1 is not reinterpreted. Its result stands for its four grants.

**Correction to `§143`.** That entry said the ten P12 ACTIVE grants *"were not counted anywhere"*. That is **wrong**:
- P12's own records counted them in aggregate: *"31 grants, 11 active"* (P12-011, P12-74 = the P11 24 / 4 plus the P12 7 / 7 at that date).
- `first-execution.evidence.json` names them in `prior_state`.

What was missing was a **per-grant classification**, which this gate now supplies.

---

## F. Decision-Ready Findings

| Q | Answer |
|---|---|
| **Q1** What are the 10 grants? | CEO-issued W4 delegations to `engineering-intelligence`, minted by P12 construction proofs (P12-W1/W2/W4 integrated execution, P12-003 / P12-005 escalation-join proofs, and the FD-P12-006 live verification). They were certified as P12 evidence. The producers never terminate their grants |
| **Q2** Who or what issued them? | The CEO (`Claude Code / AIOS Co-Founder`) under `FD-P11-001 §9`, through `W4DelegationRegistry.issue`. The producer for each is named in `§B.1`. **Provenance VERIFIED** for 8 (producer + commit + id-joined artifact). For 2 (`332d…`, `522e…`) producer and commit are verified, but the specific run is documented **by description only** (CLASS D; live-verification D.2) |
| **Q3** Still live? | **One** (`2494015d`), by every part of the five-part test, and blocked by its open escalation. **Nine are not**: no registered recipient in their root, and their single bound execution has occurred or is documented as occurred |
| **Q4** Valid under current authority and capability? | **YES, all ten.** The delegator is still the authorized constant, `FD-P11-001 §9` still resolves, and `engineering-intelligence` is C6 within its definition. *Valid ≠ live*: validity is why `2494015d` still counts |
| **Q5** What are the 3 escalations? | Real refusals by `W4Executor` of **deliberately out-of-scope proof steps** (`report-conformance`, `report-governance-join-proof`), structurally joined to their grants |
| **Q6** Still operationally open? | `9cb90fa0`: **YES** (OPEN / LIVE; blocks `2494015d`). `0991300404`, `9d6bc0ad`: open in the record, but **no work can resume** under them (OPEN / HISTORICAL) |
| **Q7** Historical vs current | Historical: all 122 P12 files, including all 13 records. Current: only `2494015d` + `9cb90fa0` meet the live test. No P12 state exists outside the certified root |
| **Q8** Where mixed? | `p12/w4-operations` and `p12/w3-operations`: the certified bytes are the only lifecycle source, and `operational_state()` reads them as current (`§D`) |
| **Q9** Separable without changing certified bytes? | **YES**: the S-1 A2 / B1 pattern, already proven on P11. Blocked by (i) authority scoped to P11 and (ii) the basename-keyed ledger folder (R-1) |
| **Q10** Remediation (classified, **not executed**) | **READER RECONCILIATION REQUIRED**: R-1 key the live ledgers by full root path; R-2 `operation_roots()` P11-only (W3 / E11 blind to P12); R-3 the operational reader cannot distinguish an un-dispositioned proof grant from a current one; R-4 `plan_completion` reads only P11-format evidence and phrasing.<br>**OPERATIONAL LEDGER SEPARATION REQUIRED** for P12, using the existing mechanism, after R-1.<br>**FOUNDER DECISION REQUIRED** for the authority to record P12 dispositions and to answer `9cb90fa0` (`§G`).<br>Nothing else: the bytes are intact, and no grant or escalation is malformed |

**Findings register:**

| ID | Finding | Class |
|---|---|---|
| R-1 | `LIVE_LEDGER` and `LIVE_RESPONSES` key folders by `Path(root).name`. `p11/w4-operations` and `p12/w4-operations` collide, so the P12 operational reading shows P11's `4313bd22` disposition as a fault. It **fails closed** (nothing wrongly honoured), but the fault is spurious. A P12 entry would share P11's folder. *This is my own S-1 implementation* | **DEFECT** (reader) |
| R-2 | `delegation_catalog.operation_roots()` covers P11 only, so W3 and E11 never see P12 or the agency roots | reader scope (carried as CG-6) |
| R-3 | The operational reader cannot express "proof grant, bound execution done, never terminated" | reader semantics |
| R-4 | `plan_completion` recognizes only `*.evidence.json` and the clause *"completion of the bound plan"* | reader scope |
| O-1 | The P12 producers (`p12_w4_integrated_execution.py`, `p12_w3_governance_escalation.py`) issue grants and never end them. This source-gap (*"no canonical prohibition on duplicate active grants"*, P12-006 / P12-74) is still open | observation |
| O-2 | `first-execution.evidence.json` records `"act": "ACT-CC-P11-008"` (the `w4_first_run` module constant) for a run performed under ACT-CC-P12-005 | observation (label carried by the module, not by the run) |
| O-3 | Two executions (`332d…`, `522e…`) are joined to their grants only by commit co-occurrence and description. P12 already classified them CLASS D, *never-rewrite-history* | evidence limitation |

---

## G. Authority / Founder Decision Queue

Only items whose evidence shows existing authority is insufficient.

| # | Question | Evidence | Why existing authority is insufficient | Decision required |
|---|---|---|---|---|
| FQ-CG7-1 | May the operational ledger record **terminal dispositions for P12 certified grants**, as A2 does for P11? | `§B`: 9 grants historical only, 1 live; `§D` separation proven; A2 Founder text *"…certified P11 delegation records … outside the certified P11 evidence boundary"* | Revocation belongs to the delegator (`FD-P11-001 §29`), but the record is in a certified root (FD-P12-006; the guard refuses the write). The only non-certified recording path is the A2 ledger, whose authority is P11-scoped. Writing P12 entries now would extend a Founder decision by inference | Extend (or not) A2's scope to P12, and say what disposition the nine proof grants take (e.g. COMPLETED where the evidence establishes completion, otherwise REVOKED with reason) |
| FQ-CG7-2 | How is the **live pair `2494015d` / `9cb90fa0`** to end? | `§B.1`, `§C`: all five live tests true; blocked; the exact twin of the P11 pair settled under B1 | `record_response` requires a `HumanAuthority`; the CEO cannot answer an escalation. The B1 precedent is a Founder response | A Founder response to `9cb90fa0` (as in B1), with a disposition for `2494015d` under FQ-CG7-1 |

**Not queued** (the evidence does not require the Founder):
- the two historical escalations `0991300404` / `9d6bc0ad`: nothing can resume under them. They can stay OPEN / HISTORICAL without operational consequence, and answering them is optional under the same B1 route;
- R-1…R-4: reader corrections within existing implementation authority, to be scheduled by a later directive, not this read-only gate.

---

## Negative controls (`§16`)

| # | Control | Held | Evidence |
|---|---|---|---|
| 1 | No grant modified | YES | 10 grant hashes BEFORE = AFTER |
| 2 | No escalation modified | YES | 3 escalation + 3 join hashes BEFORE = AFTER |
| 3 | No certified file modified | YES | 122 P12 files BEFORE = AFTER; manifest 121 / 121; integrity no faults; git-clean |
| 4 | No instance registered | YES | instance records unchanged (hashed set). The shape probe used an in-memory registry with root `None` |
| 5 | No capability created | YES | no catalog or ADR file touched |
| 6 | No authority expanded | YES | Register hash unchanged during the run; no act created except this directive's verbatim record |
| 7 | No delegation issued | YES | delegation-record set unchanged. The shape probe issued in memory only (root `None`), and nothing was persisted |
| 8 | No delegation revoked | YES | same |
| 9 | No operational state normalized | YES | live ledgers unchanged (hashed); nothing reclassified in any store |
| 10 | No historical evidence rewritten | YES | as 3 |

**Gate status: DISCOVERY EXHAUSTED → REPORTED → STOPPED.** All eleven `§25` conditions are met. The only remaining unknowns are the id-level joins of two CLASS D executions, and these cannot be resolved without retroactive attribution.
