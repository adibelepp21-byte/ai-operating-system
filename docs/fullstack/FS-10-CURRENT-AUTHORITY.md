# FS-10 — Current Authority (successor layer, `FDP-010-03`)

| Field | Value |
|---|---|
| **Purpose** | states which instruments govern **current** FS-10 Production operation, so a historical record is never read as current authority (`FDP-010` `§10.2`–`§10.5`) |
| **Governs now** | **`FDP-009`** (Register `§107`, sha256 `33fecb97…`) **+ `FDP-010`** (Register `§109`, sha256 `fa1d8b12…`); **+ `FDP-011`** (Register `§117`, sha256 `5a6e5a8b…`): ESC-03 edge mechanism O-A and Founder principal P-2 **+ `FDP-012`** (Register `§124`, sha256 `5ad7f321…`): **bounded** Architect authority for FS-10 / ESC-03 only, held by Claude Code / Co-Founder; architecture selection `AD-FS10-ESC03-R1` (Register `§125`) — **selected, not implemented** |
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
| Edge (X2) — current | **X2 ACTIVE and unchanged; no bypass and no credential exist.** Current architecture: **`AD-FS10-ESC03-R1`** (selected under `FDP-012`, Register `§125`) — **O-A**: a per-session Protection Bypass for Automation, created and revoked by the account holder in Vercel, delivered by provider-side credential injection (header `x-vercel-protection-bypass`, attached by the agent proxy) to the Production alias, the serving deployment and the designated rollback target only; the client sends only the B3 bearer; the value never enters the VM, tool output, chat, logs, evidence or the repository; revocation verified by 302 without the value. Fallback: M1 in a dedicated environment. **Implementation authorized, NOT YET OCCURRED; Production is NOT yet operationally accessible**: the next steps are account-holder actions (`FS-10-FDP012-EXECUTION-RECORD.md` `§6`). ESC-03 **NOT RESOLVED**. Session runner `fullstack/deploy/oa_session.py` built; the baseline run (Register `§126`; `evidence/FS-10-OA-BASELINE-2026-10-01.json`) shows no injection: every T2 host is stopped by X2, and the B3 bearer alone does not pass |
| Architecture authority (FS-10 / ESC-03) | **bounded, not global**: Claude Code / Co-Founder under `FDP-012` `§3` (Register `§124`), FS-10 / ESC-03 only. `FD-2` remains globally **IMPLIED / OPEN / NOT RATIFIED** (`§123`); `FDP-012` does not ratify it. `APT-CD1.1-AA-001` preserved, not the basis. Release, LIVE and Final System Acceptance remain **Founder-reserved** |
| Edge (X2) — history (Register `§117`–`§123`) | **`FDP-011` O-A** (Register `§117`): a per-session automation bypass — Production only; the serving deployment and the designated verified rollback target; `FDP-010` `§13` duties; rotated every session; revoked and verified (302) at session end and on the T7 triggers; T8 evidence without the value; never standing, never public. The value may never appear in repository, documentation, evidence, logs, chat or normal tool output (T5). **ESC-03 = DECIDED, NOT RESOLVED**: S5 is blocked at that credential boundary — the connector returns the value on creation and needs it to revoke, and T5 names no secret path (`FS-10-FDP011-S4-VALIDATION-AND-ENVELOPE.md`; Register `§118`). T5 feasibility (Register `§119`): **no existing authorized secret-handling path** (`FS-10-FDP011-T5-SECRET-CUSTODY-FEASIBILITY.md`). M1 custody validation (Register `§120`): FDP-012 **not received**, not canonicalized; M1 **blocked** — G1, G3, G6, G7, G8, G10 FAIL; G2, G4, G5 UNKNOWN (`FS-10-FDP012-M1-CUSTODY-VALIDATION.md`). Provider-side credential injection (Register `§121`): **UNSELECTED**; same X2 header, but environment-wide and not designated under T5 — **Founder decision required** (`FS-10-PROVIDER-CREDENTIAL-INJECTION-EVIDENCE.md`). Decision package prepared, no decision made (`decision-packages/FS-10-PROVIDER-CREDENTIAL-INJECTION-FOUNDER-DECISION-PACKAGE.md`; Register `§122`). Architect decision also required for the trust boundary; `FD-2` (Founder ≡ Architect) is implied, not ratified. No bypass exists. The connector's fetch is not to be used on protected deployments (runbook `§15`) |
| Founder principal | **`FDP-011` D-3 (P-2)**: a separate human principal with `aios.observe`, `aios.workflow.run`, `aios.audit` (not `aios.agent.register`); not `aios-operator`; not Release or LIVE authority. **Authorized, not yet established**: needs the Founder token's custody (plaintext with the Founder only) and an X2 path for post-deploy verification |
