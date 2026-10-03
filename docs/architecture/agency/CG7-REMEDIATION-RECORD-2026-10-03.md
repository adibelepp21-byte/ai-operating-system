# CG-7 Remediation — FD-CG7-001 Executed; R-1…R-4 Verified (2026-10-03)

| Field | Value |
|---|---|
| **Decision** | `docs/governance/acts/FD-CG7-001-P12-OPERATIONAL-STATE-DISPOSITION-DECISION.md`, verbatim; content sha256 `70ae339c4502002d9b22be469d600c293a55e401ffabface43a3f9bee15932f8`. **Registered at Register `§145`.**<br>FQ-CG7-1 = **B**, FQ-CG7-2 = **A**; both *"Founder Authorization: YES"* and *"Decision Status: APPROVED"* |
| **Result** | Register `§146` |
| **Baseline** | HEAD `e59cc295c25e6f42a04a15947ca8a5c7f978567c`, captured **before** any code changed: `evidence/CG7-REMEDIATION-BASELINE-2026-10-03.json` |
| **Verification** | `evidence/CG7-REMEDIATION-VERIFICATION-2026-10-03.json`, **`all_ok: true`** |
| **Execution** | `evidence/cg7_disposition_run.py` → `evidence/CG7-DISPOSITION-RUN-2026-10-03.json`. A re-run is refused |

The sections below keep **DECISION · AUTHORIZATION · IMPLEMENTATION · EVIDENCE · VERIFICATION · REMAINING** apart.

---

## 1. Decision and authorization

| | Recorded | Registered |
|---|---|---|
| FQ-CG7-1 | B: extend A2 to P12; the nine historical grants become REVOKED / CLOSED | `§145` |
| FQ-CG7-2 | A: answer and close `9cb90fa0787a478c` without new authority; `2494015de36246fd` becomes REVOKED / CLOSED | `§145` |
| Remediation | R-1…R-4 authorized *"following successful registration"* of both decisions | after `§145` |

**Observation.** The instrument's document header reads *"Status: FOUNDER DECISION REQUIRED"*. That is its document-type status. Both decision blocks are signed and read APPROVED, and the decision blocks were treated as operative (`§145`).

## 2. Implementation (minimal; no new subsystem, lifecycle or authority)

| Item | Change | Files |
|---|---|---|
| **R-1** Full-path ledger identity | `ledger_identity(root)` is the root's full repository path, and `ledger_folder` files entries under it. Pre-R-1 basename entries stay in place, unmoved, and are attributed by their recorded `root`; another root's entry is neither honoured nor a fault. The same rule applies to escalation responses | `tools/w4_delegation.py`, `tools/escalation_register.py` |
| **R-2** P12 visibility | `delegation_catalog.all_operation_roots()` discovers every phase's roots. `operation_roots()` (W3, E11, certified P11 measurement) is **unchanged** | `tools/delegation_catalog.py` |
| **R-3** Proof-run vs current | `w4_continuity.operational_overview()` reads each root both ways (`reconstruct` / `operational_state`). Per grant it reports historical status, operational status, `executable`, and **CURRENT OPERATIONAL GRANT** vs **HISTORICAL RECORD** with the basis. An escalation is BLOCKING only behind a current grant, otherwise **OPEN — HISTORICAL**. Lifecycle words are unchanged (ACTIVE / COMPLETED / REVOKED) | `tools/w4_continuity.py` |
| **R-4** Completion compatibility | `plan_completion` accepts the P12 clause *"on completion of plan <bound plan>"*. When the root holds no evidence record for the grant, it reads exactly one P12 `ExecutionManifest` (status `success`, nothing unsatisfied, work scope covered) | `tools/w4_delegation.py` |
| **Scope enforcement** (FQ-CG7-1 constraints 5–6) | `DISPOSITION_SCOPES`: each Founder instrument reaches only its own root, grants and disposition. Anything outside is refused when recorded and reported as a fault when read. A2 is unchanged | `tools/w4_delegation.py` |
| **Sentinel-surfaced guard** | Naming the P12 root in `w4_delegation.py` brought the module into `test_p12_certified_evidence_guard`'s scan. The scan found `issue()` and `revoke()` writing without the guard. Both now refuse a certified root **before** anything is recorded, in memory or on disk. No behaviour changes outside certified roots | `tools/w4_delegation.py` |
| **Layout-bound tests** | two `test_w4_operational_ledger` lines addressed the ledger file by its basename folder; they now use `_disposition_path` | `tools/tests/test_w4_operational_ledger.py` |
| **Pre-existing regression repaired** | `test_ecosystem_relationships` has failed since my S-1 B1 commit `5be0a24`, missed by the S-1 regression set. B1 made `escalation_register` import `p12_certified_evidence_guard`, which built a real Governance → FounderDecision **code** relationship. The pin was updated with that evidence, per the test's own rule | `tools/tests/test_ecosystem_relationships.py` |
| **Docs** | ledger semantics `W4-OPERATIONAL-LEDGER.md §7` | — |
| **New tests** | `tools/tests/test_cg7_p12_remediation.py`: 22 tests, five mutations caught (identity → basename; manifest status ignored; plan-named clause ignored; executable ignoring registration; read-side scope check removed) | — |

## 3. Execution (FD-CG7-001)

Everything below was written through the existing guarded ledger functions, outside every certified root:

| Record | Where | Authority |
|---|---|---|
| Founder response to `9cb90fa0787a478c`, transcribed verbatim from the instrument's *Founder Response* block, `responded_by` *"Moriarty (Founder)"* | `operations/escalation-responses/docs/architecture/p12/w4-operations/9cb90fa0787a478c.response.json` | FQ-CG7-2 |
| `2494015de36246fd` → REVOKED (*"REVOKED / CLOSED — proof-run grant not continued …"*) | `operations/w4-dispositions/docs/architecture/p12/w4-operations/` | FQ-CG7-2 |
| `08e14bd7…`, `332d42f0…`, `522e84af…`, `632b256f…`, `84e94ea2…`, `aa591daf…`, `b304c7ec…`, `e668a317…`, `e6a3d622…` → REVOKED. Each reason states what CG-7 established about its execution; none is represented as COMPLETED | same | FQ-CG7-1 |
| `0991300404cf44d8`, `9d6bc0ad47294ef0` | **no response recorded** (none fabricated) | — |

## 4. Before / after

| Root | Before (hist. active · op. active · hist. open · op. open) | After |
|---|---|---|
| `p11/w1-operations` | 1 · 0 · 0 · 0 | 1 · 0 · 0 · 0 (byte-identical readings) |
| `p11/w4-operations` | 1 · 0 · 1 · 0 | 1 · 0 · 1 · 0 (byte-identical) |
| `p11/x-department-operations` | 2 · 0 · 0 · 0 | 2 · 0 · 0 · 0 (byte-identical) |
| **`p12/w4-operations`** | 10 · **10** · 1 · **1**, plus a spurious P11 disposition fault | 10 · **0** · 1 · **0**; 10 REVOKED; no fault |
| `p12/w3-operations` | 0 · 0 · 2 · 2 | 0 · 0 · 2 · 2, both **OPEN — HISTORICAL** (no current grant behind them) |
| `agency/…/w4-s2-plan-delegation` | 1 · 1 · 0 · 0 | unchanged |
| `agency/…/w4-s3-founder-goal` | 1 · 1 · 0 · 0 | unchanged |

`operational_overview()` after:
- current grants: `0a697039a63f4c17` (S-2) and `50367d99c2dd4708` (S-3), both unexecuted;
- blocking escalations: **none**.

## 5. Verification (`§14`)

| | Check | Result |
|---|---|---|
| A | Certified P12 bytes | tree digest `5be77e56…` **before = after**; 121 / 121 manifest; state records (55) identical; integrity no faults; certified roots git-clean |
| B | History reconstructable | historical readings of both P12 roots identical to baseline: 10 ACTIVE, 3 OPEN |
| C | Operational state | 9 + 1 REVOKED under their own instruments; `9cb90fa0` ANSWERED; `0991300404` / `9d6bc0ad` OPEN — HISTORICAL; no disposition fault in any P11 / P12 root |
| D | Ledger identity | `docs/architecture/p11/w4-operations` ≠ `docs/architecture/p12/w4-operations`. Same basename, different identity (tests R1 ×5) |
| E | Reader | historical vs current reported per grant and escalation (R3 tests; resident post-state tests) |
| F | Regression | P11 historical, operational, escalation and plan-completion readings **byte-identical** to the baseline. Suites: `§146` |
| G | Negative controls | `test_cg7_p12_remediation` covers: out-of-scope instrument, root, grant and disposition refused; an agent recorder refused; a forged entry claiming the P12 instrument elsewhere is a fault; issuing into a certified root refused with nothing recorded; an escalation cannot be answered without a human; plus the existing W4 controls (agent-issued delegation, widening) in their suites |

## 6. Remaining

- **Historical escalations** `0991300404cf44d8`, `9d6bc0ad47294ef0` stay OPEN in both readings, by decision. They are classified historical and block nothing.
- **Unexecuted grants.** Two current grants (S-2 `0a697039…`, S-3 `50367d99…`) are live and unexecuted. Executing them, or verifying their output into a CEO outcome, is S-4 territory.
- **W3 / E11 still P11-only.** `operation_roots()` was deliberately not widened (*"existing P11 behavior must remain unchanged"*). P12 is visible through `all_operation_roots()` / `operational_overview()`.
- **CG-7 O-1:** the P12 producer scripts still never terminate their grants. They cannot run into the certified root (guarded), but the source gap is open.
- **CG-7 O-3:** two CLASS D executions (`332d…`, `522e…`) stay joined by description only.
- **Pre-existing test failures** (not caused here):
  - `test_p12_governance_evidence_verification` (1): fails since before `§131`;
  - `test_e11_measurement_currency` (4): fails on a clean HEAD.

**S-4 status.** The CG-7 completion criteria are met. The P12 state no longer blocks the next agency frontier. S-4 is **unblocked but not started**; it awaits its own directive.
