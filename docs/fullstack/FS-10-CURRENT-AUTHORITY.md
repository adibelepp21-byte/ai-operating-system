# FS-10 — Current Authority (successor layer, `FDP-010-03`)

| Field | Value |
|---|---|
| **Purpose** | states which instruments govern **current** FS-10 Production operation, so a historical record is never read as current authority (`FDP-010` `§10.2`–`§10.5`) |
| **Governs now** | **`FDP-009`** (Register `§107`, sha256 `33fecb97…`) **+ `FDP-010`** (Register `§109`, sha256 `fa1d8b12…`) |
| **Machine-readable** | `FS-10-CURRENT-AUTHORITY.json` (tested by `fullstack/tests/test_current_authority.py`) |
| **Date** | 2026-10-01 |

**HISTORICAL GATE ≠ CURRENT AUTHORITY** (`FDP-010` `§10.3`).

## 1. Authority classes (`FDP-010` `§22`)

| Action | Class | Source |
|---|---|---|
| Production deployment | CEO-AUTHORIZED | `FDP-009-01` |
| Production verification | CEO-AUTHORIZED | `FDP-009` `§8` |
| Operational access | **CEO-AUTHORIZED-WITH-BOUNDARY** | `FDP-010-01`, `§13` |
| Rollback before a release | **CEO-AUTHORIZED-WITH-BOUNDARY**: operationally required; verified known-good target only; evidence | `FDP-009` `§8`, `FDP-010` `§22` |
| Rollback after a release | **CEO-AUTHORIZED-WITH-BOUNDARY**: released; operationally necessary; verified known-good target only; no governance, certified-architecture or deployment-architecture change; evidence | `FDP-010-02` (`§5.1`, `§6`) |
| Production Release | **FOUNDER-RESERVED** | `FDP-009` `§5.3`, `§10`; `FDP-010` `§14` |
| LIVE | **FOUNDER-RESERVED** | `FDP-009` `§5.4`; `FDP-010` `§14` |
| Final System Acceptance | **FOUNDER-RESERVED** | `FDP-010` `§22` |

Operational access ≠ rollback authority ≠ Production Release ≠ LIVE (`FDP-010` `§18`). No authority is inferred beyond these classes.

## 2. Historical wording, preserved and superseded for current operation

| Historical record | Wording | Status |
|---|---|---|
| `fullstack/readiness.py` — the **closed FS-09 readiness gate** (line 714) | *"Production rollback is Founder-only (FD-FS-001 D4-A)"* | **preserved unchanged** (byte-identical to its FS-09 closing state, `de47057`); historical evidence; **not current authority**. No served or operational code imports the gate |
| `FS-09-OPERATIONAL-RUNBOOK.md` `§9` | Production rollback **Founder only** (`FD-FS-001` D4-A) | kept as a labelled *History* row beneath the current row |
| `FS-09-READINESS-PROGRAM.md` row 8 | *"Production rollback is Founder-only"* | historical: closed FS-09 record, unchanged |

The old wording existed and was correct when written: `FD-FS-001` D4-A placed the release decision first. `FDP-009` changed the ordering (its `FDP-009-01` supersedes D4-A only there) and `FDP-010-02` settled rollback after a release.

## 3. Rollback target (`FDP-010` `§6`, `§7`)

| Item | Value |
|---|---|
| **Designated verified known-good target** | **`dpl_76CYCCMjZf4SvT9BLwcNDV4Hdc8T`** (`aios-platform-9dhc3bfal-…`), commit `d05261c`, built with the permanent operational principal; READY; Vercel `isRollbackCandidate: true` |
| Serving | `dpl_s8c6mTVKiQixKrjYwyqeKso1kXSv` (`aios-platform-72l8flelz-…`), commit `d05261c` |
| Verified | read-only smoke 7/7 on the target's immutable URL as `aios-operator`; it reads back a run the serving deployment wrote (same store, same principal); same code, schema, variables and region |
| Procedure | Vercel Instant Rollback (`request_rollback`) to the designated deployment **only**; then runbook `§1` and `§12.1`; evidence |
| **Not targets** | `dpl_A5Qs…` (`22c0b49`): **NOT A VALID APPLICATION ROLLBACK TARGET** (`FDP-010` `§6.1`) · `dpl_CHV72…` (no principal) · `dpl_Dfs1…` (revoked verification principal). Vercel shows all three `isRollbackCandidate: false` |
| Limit | the target runs the same commit: it restores service after a failure of the serving deployment or of its configuration; it cannot undo a defect of `d05261c` itself, because no earlier working application exists. For that, `FDP-010` `§8` applies: preserve evidence, classify, contain, escalate |

## 4. Operational principal (`FDP-010-01`)

| Item | Value |
|---|---|
| Subject | `aios-operator` — dedicated to AIOS operation; not the Founder, not the provider account, not a release authority |
| Scopes | `aios.observe`, `aios.workflow.run`, `aios.audit` (**not** `aios.agent.register`); all from the canonical model (`security.SCOPES`); no new scope |
| Representation | Production `AIOS_OPERATOR_TOKENS` holds its SHA-256 only (`0ccb723c…`); Preview does not accept it |
| Custody | the delegated CEO's execution environment, private file; never in repository, documentation, evidence, logs or chat; rotation and revocation: runbook `§15` |
| Edge (X2) | unchanged. X2 admits Vercel-authenticated members of the account and Founder-authorized, revocable mechanisms (FS-DP-03 `R2.10`). **No mechanism is authorized for the CEO's routine API operation.** `ESC-03` = **NOT RESOLVED**. `AD-FS10-ESC03` (Register `§113`–`§114`): evidence complete for authority; **ARCHITECTURE CONSTRAINED — NO AUTHORIZED MECHANISM**; candidates E-A–E-F **UNSELECTED**; **FOUNDER DECISION REQUIRED** (`FS-10-ESC03-ARCHITECTURE-DECISION.md`; `decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE.md`). Nobody can use the Production API today: the Founder passes X2 but holds no Production principal; the CEO holds `aios-operator` but cannot pass X2. The connector's fetch is not to be used on protected deployments (runbook `§15`) |
