# MR-S5-1 — Minimal Decision Provenance Remediation: Record

| Field | Value |
|---|---|
| **Directive** | `docs/governance/acts/DIR-AIOS-AGENCY-MR-S5-1-DECISION-PROVENANCE.md` (verbatim; content sha256 `809b7dfd342d5f9be0e9817222929b7ae93e116e6c9b3ef3ceb34aa222c95ec3`). Register `§151` (receipt), `§152` (result) |
| **Closure** | **COMPLETE / VERIFIED.** G-S4-1 → CLOSED · G-S4-2 → CLOSED · G-S4-3 → CLOSED / NO REMEDIATION REQUIRED |
| **Evidence** | • Baseline: `evidence/MR-S5-1-BASELINE-2026-10-03.json` (HEAD `fa877e8`, captured before any change).<br>• Run: `evidence/mr_s5_1_decisions_run.py` → `operations/w4-s4-plan-outcome/mr-s5-1-run.result.json`.<br>• Verification: `evidence/mr_s5_1_verification.py` → `evidence/MR-S5-1-VERIFICATION-2026-10-03.json` (**all_ok**, fresh process).<br>• Tests: `tools/tests/test_mr_s5_1_decision_provenance.py` (17; seven mutations caught) |

---

## A. Baseline

| Item | Value |
|---|---|
| Commit | `fa877e8b2d6e4526b45370848defc620e8dc8ed6` |
| Certified digests | P11 58 files `45e0a817…` · P12 122 files `5be77e56…` · P13 `2025fe9b…` · platform-organization 36 files `982c3705…` · `docs/operations` 16 files `e0051b8f…` |
| Hashed for comparison | 146 acts; capability catalog (46 files) |
| Operational ledger | 16 dispositions, all legacy (S-1 4, CG-7 10, S-4 2) |
| Test baseline | agency suites 148 tests OK. Last full regression: only the two pre-existing failures (`test_e11_measurement_currency` 4, `test_p12_governance_evidence_verification` 1) |

## B. Construction: what existing mechanism was extended

No new record type, store, reader, subsystem, lifecycle or plan state. Everything is in `tools/w4_delegation.py`:

| Existing mechanism | Extension |
|---|---|
| `review_result` (the delegator's decision writer, S-4) | adds REJECT. Requires, before anything changes:<br>• ACCEPT: verification met;<br>• REWORK: a result whose verification is **not** met, `rework_steps`, and a `rework_target` that is a **delegated** step of them;<br>• REJECT: a result, no target, and any revision omitting the step |
| `record_disposition` (the S-1 operational ledger record) | optional `provenance`. The record gains `decision`, `resulting_plan` and `rework_target`, validated before writing. A decided `REVOKED` also binds the result's evidence (sha256) |
| `read_dispositions` (the existing reader) | validates provenance when present (`decision_fault`). Checks the evidence hash whenever evidence is recorded |
| `plan_outcome` (the S-4 reader) | reports `decision` and `decision_provenance` (EXPLICIT or LEGACY), `resulting_plan`, `rework_target`, `reworks` (the grant a rework step redoes) and `decision_faults` (plan / step relationships against the chain) |

`DECISIONS = (ACCEPT, REWORK, REJECT)` is closed. CANCEL, ABANDON, DROP, TERMINATE, FAILED and BLOCKED are refused.

## C. Decision provenance (live records, read without the reason field)

| Path | Grant | Disposition | `decision` | `resulting_plan` | `rework_target` |
|---|---|---|---|---|---|
| P1 | `3cc612275a914c2c` | COMPLETED | ACCEPT | `founder-mr-s5-1-accept-plan-0` | null |
| P2 | `d497e284f2c14aee` | REVOKED | **REWORK** | `founder-mr-s5-1-rework-plan-0+1` | `{plan: …-rework-plan-0+1, step: report-continuity-elements}` |
| P2 | `86d74cf0b6d14856` | COMPLETED | ACCEPT | `founder-mr-s5-1-rework-plan-0+1` | null |
| P3 | `c7e5e03a5a664230` | REVOKED | **REJECT** | `founder-mr-s5-1-reject-plan-0+1` | null |
| P3 | `ef2fa9ef2c004955` | COMPLETED | ACCEPT | `founder-mr-s5-1-reject-plan-0+1` | null |

## D. Plan provenance

- Every `resulting_plan` is a version on its goal's chain (`decision_faults`: none for all five goals).
- For P2 and P3 the resulting plan is the revision; its `supersedes` and `origin REVISED` are Planning's own fields.

## E. Rework provenance

`plan_outcome` links the rework step back to the work it redoes, structurally:

```text
founder-mr-s5-1-rework-plan-0+1 / report-continuity-elements
   reworks → plan founder-mr-s5-1-rework-plan-0 · step verify-continuity-elements · grant d497e284f2c14aee
```

- The target is checked to be a **delegated** step of the **resulting** plan, which must be a revision of the bound plan.
- Identity is (plan version, step key). Keys are unique within a plan (`plan.py:107`).
- No step name is interpreted.

## F. Legacy compatibility

| Records | Read as | Rewritten? |
|---|---|---|
| S-1 (4), CG-7 (10), S-4 (2) | legacy `COMPLETED` → ACCEPT (*"LEGACY (derived: COMPLETED ⇒ ACCEPT)"*); legacy `REVOKED` → *"LEGACY (REVOKED: decision not recorded)"* | none, and no fault. `git diff fa877e8 -- …/w4-dispositions …/escalation-responses` is empty |

**Not fabricated:** S-4's REWORK `9925366405d44af8` carries no decision field and stays *decision not recorded*. Its plan stays open (`founder-s4-rework`), exactly as S-4 left it.

## G. Positive tests

| # | Path | Live | Test |
|---|---|---|---|
| P1 | ACCEPT | `tools/w4_delegation.py` 14/14 → ACCEPT → plan **completed** | `P1_Accept` |
| P2 | REWORK | `tools/w4_continuity.py` 3/14, genuine → REWORK → revised plan with exact target → target performed (*"3 of 14 elements carried (reported)"*) → ACCEPT → plan **completed** | `P2_Rework` |
| P3 | REJECT | `tools/w4_execution.py` 4/14 → REJECT (*an execution module does not hold the delegation record; not redone*) → revised plan without the step → different work (`tools/w4_delegation.py` 14/14) → ACCEPT → plan **completed** | `P3_Reject` (with and without revision) |

## H. Negative controls

| # | Control | Result |
|---|---|---|
| N1 | Agent cannot write a CEO decision | refused at `review_result` and at `record_disposition`; nothing written |
| N2 | Agent cannot self-ACCEPT | refused |
| N3 | Agent cannot self-REJECT | refused |
| N4 | ACCEPT without valid verification | refused (no result; failed result) |
| N5 | REWORK without a resulting plan | refused: *"must say what the work is sent back as"*. A record without `resulting_plan` faults |
| N6 | REWORK without a valid target | refused: absent, unknown, or not delegated. REWORK on a verifying result is refused too |
| N7 | Target in another plan | refused at write (*"belongs to plan"*); a bad relationship on read is a decision fault |
| N8 | REJECT cannot become REWORK | refused: a REJECT target, or a REJECT revision containing the step (*"redoing the same work is REWORK"*); mismatched decision / disposition pairs fault |
| N9 | Historical records not rewritten | grant and evidence bytes unchanged by decisions; append-only; legacy ledger unchanged |
| N10 | Certified evidence not mutated | delegator review refused on certified roots; a ledger inside certified evidence refused before any directory exists; certified digests unchanged |
| N11 | Reconstruction without reason text | fresh subprocess and the verification read decisions with `reason` removed |
| N12 | Founder authority unchanged | `founder_acceptance` NOT RECORDED; no Founder parameter; the decision set is fixed at three |

## I. Fresh process

`mr_s5_1_verification.py` runs as a separate process. It reads every disposition in every operational root **with the `reason` field removed**:
- 5 explicit decisions, each equal to the run log;
- 16 legacy decisions;
- plan outcomes from the restored surface: all three MR-S5-1 goals completed;
- one rework link;
- no faults.

The test `test_n11_…` repeats this in a subprocess for all three decisions.

## J. Mutation tests (temporary copies)

| Mutated | Detected as |
|---|---|
| decision removed | *"decision None is not one of …"* |
| decision changed to ACCEPT on a REVOKED | *"is recorded as 'REVOKED'"* |
| resulting plan removed | *"names no resulting plan"* |
| rework target removed | *"REWORK names no rework target"* |
| target in another plan | *"belongs to plan"* |
| target → a CEO step / plan not on the goal | `decision_faults` |
| verification evidence changed | *"evidence record changed"* |

Code mutations (seven, each caught by the suite): target-plan check, REJECT-redo check, REWORK-finding check, reader validation, target-delegated check, REVOKED evidence binding, rework link.

## K. Regression

The S-4 suite was adapted to the stricter contract only:
- REWORK now names its target;
- `decision` is structural and the reason moved to `reason`;
- *"no REJECT"* became *"a decision outside the three is refused"*.

Full regression: 90 suites, 2313 tests. 88 suites OK. The only failures are the two pre-existing ones:
- `test_e11_measurement_currency`: 4, entry-point symbol currency;
- `test_p12_governance_evidence_verification`: 1, population status.

Neither touches `tools/w4_delegation.py`; both failed at baseline `fa877e8`. Recorded at Register `§152`.

## L. Integrity

| Invariant | Result |
|---|---|
| Certified P11 / P12 / P13 / platform-organization / `docs/operations` | digests equal to baseline |
| Founder records (acts) | unchanged (only this directive's verbatim act added) |
| Capability catalog | unchanged |
| Agent registry | no instance record changed or added (the run registered the existing instance **in memory**; its on-disk record hash is unchanged) |
| Integrity faults | none |
| Certified roots | git-clean |
| Authority | unchanged (FD-P11-001 §15.2; V2 A09 / A11; agents none) |
| Deployment | PAUSED |

## M. Remaining findings (discovered during construction)

1. **First run attempt withdrawn before commit.** I first ran P1–P3 in a new root, which wrote a new instance-registration record. That conflicts with `§24` (*Agent registry unchanged*), so I deleted the root and its ledger entries, all uncommitted and minutes old. I re-ran in the S-4 root, where the instance is already registered, registering it in memory only.
2. **Historical S-4 tools describe the pre-MR-S5-1 API.**
   - `s4_plan_outcome_run.py` calls REWORK without `rework_target`; it refuses to re-run by design.
   - `s4_verification.py` compares outcomes with the S-4 run JSON, whose `plan_outcome` shape predates the new keys.
   - Both remain the record of what ran. Re-running them now would reflect the extended reader.
3. **S-4's own REWORK stays open.** `founder-s4-rework` keeps its unperformed rework step and no explicit decision (legacy). It was not completed or relabelled here.
