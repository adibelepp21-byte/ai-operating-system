# FR-1 — Operational State Integration (FD-TD-001): Record

| Field | Value |
|---|---|
| **Authority** | `docs/governance/acts/FD-TD-001-P12-W2-LIVE-LEDGER-INTEGRATION-CLASSIFICATION.md` (verbatim; content sha256 `8cd046d46b633becd1033da5b305d09369e1a3d669445b08877e4c2cc67bc060`): FQ-TD-1 = **Option A**. Register `§157` (decision), `§158` (this result) |
| **Result** | **FR-1 PARTIALLY CONSTRUCTED → STOPPED AT A CERTIFIED BOUNDARY → FOUNDER DECISION REQUIRED** (FQ-FR1-1, `§I`).<br>• **Live ledger → P12-W2:** built and verified.<br>• **P12-W2 → P13:** not constructed. Wiring it requires changing a certified P12 verifier population, a `§4` / `§8` stop the CEO may not classify |
| **Evidence** | • Baseline: `evidence/fr1_baseline.py` → `evidence/FR1-BASELINE-2026-10-03.json`, captured before any code changed (`a046f9c`).<br>• Verification: `evidence/fr1_verification.py` → `evidence/FR1-VERIFICATION-2026-10-03.json`, **all_ok**, fresh process.<br>• Tests: `tools/tests/test_fr1_operational_state_integration.py` (13; 4 code mutations caught) |
| **Code changed** | `tools/p12_operational_state.py` only, plus the new test file. No other module, store, source, capability, Agent or authority |
| **Completion (FD-FR1-001)** | **FR-1 COMPLETE / VERIFIED** (`§K`; Register `§159` decision, `§160` result).<br>• FQ-FR1-1 = Option A: P13 is wired to P12-W2 and registered as an observed consumer in the certified consumer-evidence harness.<br>• The record above `§K` is kept as the history of the stop |

---

## A. What was built (live operational ledger → P12-W2)

**Changed: two projections in the existing P12-W2 surface, and their declared freshness text.**

| Projection | Now projects | Read through |
|---|---|---|
| `delegation.granted` | the grant records as **history**, and the ledger's disposition as **current**:<br>• `current` (executable grants);<br>• `active` = their count;<br>• `historical.completed` / `revoked`;<br>• `historical.recorded_active_not_current`.<br>A ledger disposition fault makes the entry `CONFLICTING`, never CURRENT | `w4_continuity.operational_overview()`, the reader FD-CG7-001 R-2 / R-3 authorized, over `all_operation_roots()` |
| `escalation.raised` | keeps the historical join (`records`, `joined_by_*`) and adds:<br>• `blocking` (open behind a current grant);<br>• `open_historical`;<br>• `answered` (B1 / FQ-CG7-2 responses) | the same reader |

**Unchanged, verified:**

| Item | State |
|---|---|
| Declared contract of both sources | state class, semantics (`SOURCE-OF-TRUTH`), owner (*"FD-P11-001 authorized delegator"*, *"escalation register"*), portion (*"operational grants and their lifecycle"*), read path, **provider `UNRESOLVED (F-17)`** |
| Number of sources | 8 |
| `is_authority()` | False |
| Write path | none |

- **Ownership:** the ledger stays the owner. P12-W2 reads the owner's reader and copies none of its rules.
- **Freshness:** one ledger reading is shared within a single `project()` pass, so both entries describe the same instant. The next call re-derives everything; nothing is cached across calls.

**Not changed:**
- the certified verifier populations: `p12_provenance_verification.DELEGATION_ROOTS`, `delegation_catalog.operation_roots()`, W3 projections, `p12_failure_verification.escalation_join()`;
- P13, the P12 self-model and W3;
- any certified evidence.

## B. Before → after (P12-W2, the system-wide layer)

| Reading | Before (`§156`) | After |
|---|---|---|
| `delegation.granted` | `{"grants": 34, "active": 14}`, CURRENT. All 14 were operationally closed | `active: 2`; `current: [0a697039a63f4c17, 50367d99c2dd4708]`; history: 7 completed, 34 revoked, 21 recorded-ACTIVE-not-current (the 14 among them) |
| `escalation.raised` | `{"records": 4, …}`, no open / answered split | the same join, plus `blocking: []`, `open_historical: [0991…, 9d6b…]`, `answered: [23f315ba…, 9cb90fa0…]` |
| P12-W2 verifier (9 checks) | 9 VERIFIED | **9 VERIFIED** (identical) |
| P12-W2 summary | 8 sources, 8 current, 0 conflicts | identical |

## C. FD-TD-001 `§7` verification

| # | Requirement | Result |
|---|---|---|
| 1 | the 14 stale ACTIVE no longer presented as current | **PASS**: none in `current`; all in `recorded_active_not_current` |
| 2 | the 2 live grants represented | **PASS** |
| 3 | historical completed / revoked stay historical | **PASS**: counts equal the ledger's; operational digest equal to baseline |
| 4 | blocking vs historical / non-blocking escalation semantics | **PASS**: `blocking` equals the owner's classification. P13's `escalations.open` (P12 self-model, certified W5 semantics) is unchanged |
| 5 | P12 certified evidence byte-identical | **PASS**: certified digests equal; integrity no faults; git-clean |
| 6 | **P13 receives state through P12-W2** | **BLOCKED, not constructed** (`§E`) |
| 7 | fresh-process reconstruction | **PASS**: a second interpreter yields the identical projection |
| 8 | P11 / S-1 … MR-S5-1 behaviour intact | **PASS**:<br>• certified-verifier populations, verifier verdicts and the state-chain summary equal the baseline;<br>• the operational-overview digest is equal;<br>• P13's observed facts are unchanged;<br>• regression `§H` |
| 9 | no second current-state authority | **PASS**: one surface, 8 sources, 0 conflicts. The changed code is exactly `tools/p12_operational_state.py` and its test |
| 10 | authority and delegation boundaries unchanged | **PASS**: governance and envelopes equal; delegator unchanged; `issue.delegation` still RESERVED |

**`§3` must-nots:** all held:
- F-17 untouched;
- ownership unchanged;
- verifier populations unchanged;
- no Agent, capability, store or subsystem;
- no direct Agency → P13;
- the certified consumer measurement agrees;
- the P13 certified root is unchanged.

## D. Tests

`test_fr1_operational_state_integration.py`, 13 tests:
- the 14 / 2 / historical / escalation readings on the live repository;
- the declared contract and F-17;
- the certified verifier populations;
- no write path;
- no Agency reader in P13;
- synthetic ledgers: closed → history, a fault → CONFLICTING, blocking vs historical vs answered;
- one reading per pass, a fresh one per call;
- fresh process.

Four code mutations were run, and each was caught: current read from stored status; answered unfiltered; disposition faults ignored; the ledger cached across calls.

## E. The stop: P12-W2 → P13

I wired P13 exactly as the certified Blueprint `§4` names it: a `StateUnderstanding` source calling `tools.p12_operational_state.project()`. It worked (P13 observed the 2 current grants as VERIFIED facts). Then the certified P12 consumer machinery reacted:

| Certified mechanism | Effect of the P13 import |
|---|---|
| `p12_state_verification.consumers_of` (AST measurement, `ACT-CC-P12-008`) | `tools/p13/state.py` becomes a measured consumer |
| `p12_consumer_evidence_verifier` (independent dynamic verifier, `§4.1.C`) | **DISAGREES**: P13 is *"invented"*, because its `CANDIDATES` population does not contain it |
| `test_p12_state_verification` | the pinned consumer set changes. The pin's own rule: *"if a consumer has been wired, the STATE item's classification must be updated rather than this control relaxed"* |
| `test_p12_consumer_measurement` | the pinned importer count changes (4 → 5) |

To make the measurement agree, I would have to add P13 to the verifier's candidate population and update two pinned certified-consumer controls and the STATE consumer classification. That is what `ACT-CC-P12-019` did, under its own Act, when `p12_e12_measurement` became a consumer.

**That is a change to a certified P12 verifier population**, which FD-TD-001 `§4` names and forbids the CEO to classify as maintenance. So I **stopped there and reverted the P13 wiring** (`tools/p13/state.py` and the three P13 test edits are byte-identical to HEAD).

**Rejected workaround.** P13 could import P12-W2 by `importlib`, so the AST measurement would not see it. That would hide a **genuine** consumer from a certified measurement whose purpose is to find consumers (`§16`: *"each claimed consumer requires evidence that it actually consumes the state"*). Not done.

## F. Defect found and repaired (mine, pre-existing since S-6)

| Item | Detail |
|---|---|
| What happened | My read-only evidence scripts `s6_frontier_discovery.py` (S-6, `a7a0860`) and `td_state_authority_discovery.py` (TD, `a046f9c`) imported P12-W2 normally. The repository-wide consumer measurement counted them, so `test_p12_state_verification` and `test_p12_consumer_measurement` have **failed since the S-6 commit** |
| Why it was missed | the S-6 and TD regressions ran the doc-sensitive suites only |
| Repair | every evidence script now reads P12-W2 **as data**, through `importlib` and with a disclosure comment. This is the pattern the certified P12-W2 verifier itself discloses (an evidence tool measures the surface; it is not a consumer) |
| Result | the consumer measurement is back to its certified pins: 3 consumers, 4 importers; the independent verifier AGREES |
| Disclosure | the S-6 and TD scripts' bytes differ from the `script_sha256` recorded in their JSON outputs. The outputs were produced by the earlier versions (git history), and the measured behaviour is identical |

## G. Integrity

| Surface | Result |
|---|---|
| Certified P11 / P12 / P13 / platform-organization / `docs/operations` | equal to baseline |
| Agent registry, capability catalog, candidates, governance, envelopes | equal to baseline |
| Deployment | equal to baseline; PAUSED |
| Non-`tools` code | equal to baseline |
| Integrity | no faults |
| Certified roots | git-clean |

## H. Regression

Full run after the revert: **91 suites, 2326 tests, 89 suites OK.** The only failures are the two pre-existing ones (`test_e11_measurement_currency` 4, `test_p12_governance_evidence_verification` 1).

`test_p12_state_verification` and `test_p12_consumer_measurement`, which had failed since S-6 (`§F`), **pass again**. `test_p12_e12_measurement` 26 / 26 OK. Recorded at Register `§158`.

## I. Founder decision required — FQ-FR1-1

**May the CEO register `tools/p13/state.py` as an observed consumer of P12-W2 in the certified P12 consumer-evidence harness?** That is:
- add `("tools.p13.state", "_operational_state")` to `CANDIDATES`;
- update the two pinned consumer controls and the STATE consumer classification, as `ACT-CC-P12-019` did for `p12_e12_measurement`;
- then wire P13 to P12-W2 through the interface the certified P13 Blueprint `§4` already names.

| Option | Meaning | Consequence |
|---|---|---|
| **A** (CEO recommendation) | Authorize the registration as part of FR-1 under FD-TD-001 | P13 receives Agency state through P12-W2. The consumer measurement stays honest: P13 is observed, not hidden. FR-1 completes, and `§7` item 6 can be verified |
| B | Treat it as a certified P12 change | successor P12 verification baseline → Founder certification before wiring |
| C | Leave P13 unwired | the system-wide layer is now correct (`§B`), but executive re-discovery still reads the historical self-model view |

## J. Residuals

- **P13 escalation fact:** P13's own `escalations.open` fact (P12 self-model, certified W5) still uses the register's historical rule. It is unchanged by design. With Option A, P13 would also carry P12-W2's blocking / historical / answered split.
- **Cost:** `project()` now costs about 9 s, mostly the operational overview (about 7.6 s per reading).
- **Other readers:** W3 and the P13 self-model keep their historical scope, as decided (FD-CG7-001 R-2; S-1 M-2).

---

## K. Completion under FD-FR1-001 (FQ-FR1-1 = A)

**Authority:** `docs/governance/acts/FD-FR1-001-P13-CONSUMER-REGISTRATION-AND-P12-W2-INTEGRATION.md` (verbatim; content sha256 `85edece762972c74eea5a80935b26eda8a12b7534996684a6cc7038fa1c88a96`), Register `§159`.

**Built, exactly the `§2` scope:**

| # | `§2` item | Change |
|---|---|---|
| 1 | register P13 as an observed consumer | `tools/p12_consumer_evidence_verifier.py`: one line added to `CANDIDATES`, `("tools.p13.state", "_operational_state")`, with a comment citing FD-FR1-001 and the `ACT-CC-P12-019` precedent. No check, scanner or meaning changed |
| 2 | update the pinned consumer tests | • `test_p12_state_verification`: consumer set 3 → 4 (`tools/p13/state.py`).<br>• `test_p12_consumer_measurement`: importer count 4 → 5.<br>Both docstrings say why the pin moved |
| 3 | update the STATE consumer classification | It is **computed**, not declared: `p12_state_verification._link_consumer`. It moves by itself from *"3 evidenced consumer(s) of 4 importer(s)"* to *"4 … of 5"* and stays **SATISFIED**. No separate declared classification exists to edit |
| 4 | wire P13 to the certified P12-W2 interface | `tools/p13/state.py`: source `operational_state` calls `tools.p12_operational_state.project()`, the interface the certified Blueprint `§4` names, with a static `from tools import p12_operational_state as w2`.<br>• Facts: `operational_state.delegations` / `operational_state.escalations`. Only a CURRENT W2 entry is VERIFIED; anything else is INFERRED; absence is UNKNOWN.<br>• The entry takes defaults so the harness can drive it with no arguments.<br>• Three P13 test files exclude this slow source from their fast source sets, as they already exclude `self_model` and `corpus` |
| 5 | verify the independent measurement recognizes P13 | AST measurement: P13 is a consumer and importer. The independent dynamic verifier **observes** P13 reading the resident sources: 4 / 4 checks AGREE, 0 DISAGREE |

**Honest measurement (`§4`).**
- P13's import is static and visible.
- The scanner (`p12_state_verification.py`) is byte-identical.
- No check of the independent verifier changed.
- No parallel measurement exists.

These tests would fail if P13 were hidden or unregistered:

| Test | Catches |
|---|---|
| `test_p13_binds_the_surface_statically_not_by_name` | P13's import replaced with a by-name load |
| `test_p13_is_an_importer_and_an_evidenced_consumer` | P13 dropped from the AST measurement |
| `test_the_independent_verifier_agrees_with_the_measurement` | an unregistered consumer (verifier DISAGREES) |

**Verification (`§6` / `§8`).** `evidence/fr1_completion_verification.py` → `evidence/FR1-COMPLETION-VERIFICATION-2026-10-03.json`, **all_ok**, fresh process, against `evidence/FR1-COMPLETION-BASELINE-2026-10-03.json` (captured before P13 was wired).

| # | `§6` item | Result |
|---|---|---|
| 1 | W2 current vs historical delegation | PASS: 2 current; the 14 stale in history |
| 2 | W2 blocking vs historical / answered | PASS |
| 3 | P13 receives state through P12-W2 | **PASS**: `operational_state.delegations` VERIFIED, current `[0a697039…, 50367d99…]`, source *"P12-W2 delegation.granted"* |
| 4 | the certified measurement recognizes P13 | **PASS**: consumer and importer; independent verifier observed; CONSUMER link SATISFIED |
| 5 | existing certified verifiers valid | PASS: the P12-W2 verifier, state-chain link statuses and verdicts equal the baseline |
| 6 | source populations unchanged | PASS: `DELEGATION_ROOTS`, `operation_roots()`, W3, escalation join equal |
| 7 | no direct Agency → P13 | PASS: no Agency reader name in `tools/p13` |
| 8 | fresh-process reproduction | PASS |
| 9 | S-1 … MR-S5-1 intact | PASS: operational-overview digest equal; P13's `escalations.open` unchanged |
| 10 | no new current-state authority | PASS: the changed code is exactly the eight files listed; 0 conflicts; authority unchanged |

**Data change vs certified semantic change (`§8`).**

| Data changes (expected, by the authorized wiring) | Certified semantics (all unchanged) |
|---|---|
| • consumers 3 → 4<br>• importers 4 → 5<br>• one harness candidate added<br>• CONSUMER link detail 3 / 4 → 4 / 5 (status SATISFIED both)<br>• two P13 facts added | • certified roots byte-identical, including the P13 Blueprint<br>• the scanner unchanged<br>• the verifier's diff is the one added registration<br>• its checks the same<br>• state-chain link statuses the same<br>• the P12-W2 contract and code unchanged since FR-1<br>• populations and verdicts the same<br>• governance and envelopes the same |

**Tests.**
- `test_fr1_operational_state_integration`: 19 tests.
- Seven code mutations, each caught:
  - W2: current read from stored status; answered unfiltered; faults ignored;
  - P13: everything VERIFIED; reads an Agency reader directly; hides the import by name;
  - the consumer left unregistered.
- The regression is recorded at Register `§160`.

**Evidence correction (`§7`).** `evidence/EVIDENCE-CORRECTION-2026-10-03-SCRIPT-HASHES.md`.
- **How:** the S-6, TD and FR-1-baseline outputs were reproduced by the current scripts in worktrees at their original states.
- **Result:** 0 differences in any finding. The originals are preserved; the corrected outputs sit beside them as `.CORRECTED.json`.

**Residuals.**
- P13's own `escalations.open` (P12 self-model, certified W5 semantics) still uses the historical rule. P13 now *also* observes P12-W2's blocking / historical / answered split, from the system-wide layer.
- No P13 cycle was run, so nothing was written to `docs/operations/p13`. P13 observation was verified by `StateUnderstanding.observe()`, which is read-only.
- `project()` costs about 9 s per call.
