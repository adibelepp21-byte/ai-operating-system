# FS-10 — Deployment & Operationalization

| Field | Value |
|---|---|
| **Stage** | FS-10 Deployment & Operationalization (Act `§21`) |
| **Status** | **ACTIVE — at the Founder Release Gate.** PRODUCTION DEPLOYED · PRODUCTION VERIFIED · RELEASE PACKAGE READY · **FOUNDER RELEASE AUTHORIZATION REQUIRED** |
| **Authority** | **`FDP-009`** (Register `§107`) **+ `FDP-010`** (Register `§109`); current classes in `FS-10-CURRENT-AUTHORITY.md`. The closed FS-09 gate is history, not current authority (`FDP-010-03`) |
| **Production** | release candidate **`d05261c`**: `dpl_s8c6mTVKiQixKrjYwyqeKso1kXSv` serves the Production alias behind **unchanged X2**; designated rollback target `dpl_76CYCCMjZf4SvT9BLwcNDV4Hdc8T` (same commit, verified). **Not released, not LIVE, not public** |
| **Operational access** | permanent principal `aios-operator` (`FDP-010-01`): observe, workflow.run, audit; hash only; verified with negative controls. The CEO has no authorized path through X2 for routine operation: `ESC-03` **NOT RESOLVED — ARCHITECT DECISION REQUIRED** (`FS-10-ESC-03-AUTHORITY-RESOLUTION.md`, Register `§112`) |
| **Rollback** | CEO with boundary before and after a release (`FDP-009` `§8`, `FDP-010-02`); verified known-good target established; `22c0b49` is not a target |
| **Temporary access** | **NONE** (verification bypass revoked; revocation verified on 7 hosts) |
| **Next step** | **Founder Release Authorization** (`FDP-009` `§10`; `FDP-010` `§16`) |

```text
FS-10 Preparation                    done
   → Production Deployment           done   (CEO; FDP-009-01)  d05261c
   → Production Verification         PASS   (CEO; FDP-009-03 temporary access, revoked)
   → Operational access + rollback   done   (CEO; FDP-010-01/-02; ESC-03 open, non-blocking)
   → Release Package                 READY  (CEO; evidence, not authorization)
   → Founder Release Authorization     ← here (Founder)
   → Production Release → LIVE (bounded by X2) → Operational AIOS
```

## 1. What was done under `FDP-010` (2026-10-01)

| `§17` step | Result |
|---|---|
| 1 Re-discovery | `FDP-009` `33fecb97…` and `FDP-010` `fa1d8b12…` recomputed equal to Register `§107`, `§109`; FS-09 gate byte-identical to `de47057`; Production 64 rows, `AIOS_OPERATOR_TOKENS = []` |
| 2 Documents | this document, the runbook (`§9` current rollback row, `§15` operational principal), the Release Package, `FS-10-CURRENT-AUTHORITY.*` |
| 3 Operational access | `aios-operator` (observe, workflow.run, audit), hash only in Production `AIOS_OPERATOR_TOKENS`; token held privately by the delegated CEO |
| 4 Scopes and negative controls | smoke 7/7 on the serving deployment and on the rollback target; `agent.register` → 403; Preview principal refused on Production; operator refused on Preview and on the superseded deployments; bypass alone 401; token alone 302; one Scenario B run as `aios-operator` |
| 5 Residual variable | the connector offers no delete; the variable now carries the approved principal (`FDP-010` `§11.4`), so the empty-list residual no longer exists |
| 6 FS-09 gate | unchanged; test pins it to its closing state |
| 7 Successor authority | `FS-10-CURRENT-AUTHORITY.md` / `.json`, tested (`fullstack/tests/test_current_authority.py`) |
| 8 Rollback target | `dpl_76CYCCMjZf4SvT9BLwcNDV4Hdc8T` (`d05261c`), built with the operational principal |
| 9 Rollback readiness | target READY, Vercel rollback candidate, smoke 7/7, reads the serving deployment's records; procedure in runbook `§9`; not executed (not operationally required) |
| 10 Checks | regression, citation, governance: Release Package `§16` |
| 11 Release Package | updated (`§18` there) |
| 12 | **STOP** at the Founder Release Gate |

## 2. Current frontier

**Founder Release Authorization.** Open, non-blocking: `ESC-03` — Architect decision required (package `decision-packages/FS-DP-03-R3-ESC-03-OPERATIONAL-EDGE-ACCESS.md`). Remaining: Founder Release Authorization · Production Release · LIVE · Operational AIOS.

---

# History: FS-10 after Production Verification (2026-10-01), before `FDP-010`

| Field | Value |
|---|---|
| **Stage** | FS-10 Deployment & Operationalization (Act `§21`) |
| **Status** | **ACTIVE — at the Founder Release Gate.** PRODUCTION DEPLOYED · PRODUCTION VERIFIED · RELEASE PACKAGE READY · **FOUNDER RELEASE AUTHORIZATION REQUIRED** |
| **Authority** | `FDP-009` (Register `§107`): Production deployment and verification before the Founder Release Authorization; deployment ≠ release ≠ LIVE; temporary verification access with boundary |
| **Production** | release candidate **`d05261c`** deployed: `dpl_CHV72ePvPE7doNu4WaKp93qXXu8x` serves the Production alias behind **unchanged X2**. **Not released, not LIVE, not public** |
| **Verification** | **PASS** (2026-10-01; Register `§108`): `FS-10-RELEASE-PACKAGE.md`, evidence `evidence/FS-10-PRODUCTION-VERIFICATION-2026-10-01.json` |
| **Temporary access** | **NONE**: the verification principal and the bypass were revoked and the revocation verified on 5 hosts |
| **Next step** | **Founder Release Authorization** (`FDP-009` `§10`). Then, before LIVE, permanent Production principals (`ESC-01`) |

```text
FS-10 Preparation                 done
   → Production Deployment        done   (CEO; FDP-009-01)  d05261c
   → Production Verification      PASS   (CEO; temporary access per FDP-009-03, revoked)
   → Release Package              READY  (CEO; evidence, not authorization)
   → Founder Release Authorization  ← here (Founder)
   → Production Release → LIVE (bounded by X2; ESC-01 first) → Operational AIOS
```

## 1. What was done (2026-10-01)

| Step | Result |
|---|---|
| Re-discovery | `FDP-009` registered (`§107`), fenced hash `33fecb97…` recomputed equal; served paths unchanged since `d05261c`; Production key present (Production scope, Sensitive, not decrypted); Production store 0 rows; Preview 554 |
| Temporary principal | `fs10-verification` (observe, workflow.run, audit), hash only, Production scope |
| Deployment | `d05261c` → `dpl_Dfs1Fx8P9G4QuNd1EYPSwet3VLG1`, Python 3.12, READY, alias moved; default branch not merged |
| Temporary bypass | one automation bypass, labelled |
| Verification | smoke read-only 7/7, write 10/10; 11 additional checks (scope 403, audit, headers, 405/404, X2 with and without bypass); Production store 0 → 52, Preview unchanged; 50 L1 lines, M1 0 server errors |
| Rollback readiness | candidates recorded; not performed (not operationally required) |
| Revocation | principal emptied, `d05261c` redeployed as `dpl_CHV72ePvPE7doNu4WaKp93qXXu8x`, token 401; bypass revoked, old bypass ≡ none (302/401) on 5 hosts; local credentials destroyed |
| Backup | read-only export of the Production store (64 rows), equal to the server digests |
| Release Package | `FS-10-RELEASE-PACKAGE.md` (`FDP-009` `§9`, 17 items) |

## 2. Authority map

Unchanged from the post-`FDP-009` map in the history below (`§1` there). The steps above used only CEO-AUTHORIZED-WITH-BOUNDARY actions. **Founder-reserved and not taken:** Production Release, LIVE activation, traffic, Final System Acceptance, spending. **Escalated and open:** `ESC-01` permanent Production principals (before LIVE), `ESC-02` rollback after a release.

## 3. Current frontier

**Founder Release Authorization.** Nothing further is authorized to the CEO on Production except H3 checks, read-only backups, and a rollback if operationally required (`FDP-009` `§8`).
Remaining: Founder Release Authorization · Production Release · (`ESC-01`) · LIVE · Operational AIOS.

---

# History: FS-10 as reconciled with `FDP-009` (2026-10-01), before Production Deployment

| Field | Value |
|---|---|
| **Stage** | FS-10 Deployment & Operationalization (Act `§21`) |
| **Status** | **ACTIVE — Deployment Preparation**, at the last step before Production Deployment |
| **Authority** | `FDP-009` (Founder Decision, Register `§107`): deployment and verification **before** the Founder Release Authorization; deployment ≠ release ≠ LIVE; temporary verification access with boundary. Classification of every action: `FS-10-ACT-009-AUTHORITY-BOUNDARY-RECORD.md`, as resolved by `FDP-009` (`§1` below) |
| **Production** | **not deployed, not LIVE.** Production serves `22c0b49` (before this program) and is untouched |
| **Founder Release Authorization** | **NOT YET ISSUED.** It follows Production Verification and the Release Package (`FDP-009` `§9`, `§10`) |
| **Release candidate** | **`d05261c`**: the served tree verified live on Preview at FS-09 (`dpl_EJucmiuLbgmgX1ar7SDZ25Ngp3ER`). Every later commit leaves the served paths unchanged. Identified by the CEO (`FDP-009` `§8`); approving it is the Founder's release decision |
| **Next step** | **blocked on one external action:** the Production database key (`§3` P1) |

```text
FS-10 Preparation   ← here: everything done except P1
   → Production Deployment        (CEO; FDP-009-01)
   → Production Verification      (CEO; smoke, health, integration; temporary access per FDP-009-03)
   → Release Package              (CEO; evidence, not authorization)
   → Founder Release Authorization (Founder)
   → Production Release → LIVE (bounded by X2) → Operational AIOS
```

## 1. Authority map after `FDP-009`

From the ACT-009 classification; rows changed by `FDP-009` are marked ◆.

| Action | Authority | Who |
|---|---|---|
| ◆ Production deployment of the release candidate; roll-forward | **CEO-AUTHORIZED-WITH-BOUNDARY** (`FDP-009-01`, `§8`): deployment for verification only; not a release | CEO |
| Production smoke, health and integration verification, including labelled test writes | CEO-AUTHORIZED-WITH-BOUNDARY (ACT-003 `§20`; `FDP-009` `§8`) | CEO |
| ◆ Temporary access past Vercel SSO, and a temporary verification principal | **CEO-AUTHORIZED-WITH-BOUNDARY** (`FDP-009-03`, its 14 conditions): created, used for verification only, revoked, revocation verified | CEO |
| ◆ Rollback before a release | CEO-AUTHORIZED-WITH-BOUNDARY (`FDP-009` `§8`: when operationally required) | CEO |
| Rollback after a release | **UNKNOWN** (`ESC-02`) | escalated |
| Permanent Production principals (who uses AIOS once released) | **UNKNOWN** (`ESC-01`) | escalated; needed before LIVE, not before verification |
| Production database key; Production variables; provider settings | **EXTERNAL-CONTROL** (ACT-001 `§7.1`; ACT-003 `§13`, `§28`) | account holder |
| Deployment Protection (X2); custom domain; production branch; alerting mechanism; schema | **ARCHITECT-RESERVED** (X2 decided and unchanged, `FDP-009-02` `§5.5`) | Architect |
| Release candidate identification; Release Package; monitoring (L1/M1/R2); H3 check cadence; incidents; read-only backups | CEO-AUTHORIZED / WITH BOUNDARY | CEO |
| ◆ Production Release; LIVE activation; traffic | **FOUNDER-RESERVED** (`FDP-009` `§5.3`, `§5.4`, `§10`) | Founder |
| Spending | FOUNDER-RESERVED (D3-A, standing: none) | Founder |
| Final System Acceptance | FOUNDER-RESERVED (A19), not due | Founder |

## 2. Done

| Item | State |
|---|---|
| FS-09 | PASS / CLOSED (`FS-09-ACT-008-EXECUTION-RECORD.md`); gate READY, which is not a release |
| Release candidate | `d05261c`, verified live on Preview; Python 3.12 build from `.python-version` |
| Production store | `hmljfyqycxcueulhsjae`: migration `20260928051800_aios_records` applied, schema equal to Preview, **0 rows**, append-only triggers |
| E1 wiring | `VERCEL_ENV=production` selects the Production project; unknown refuses (503); a Preview key never serves Production |
| Runbook, ownership, backup and rollback procedures | written and drilled on Preview (runbook `§7`–`§10`, `§12.1`) |
| Smoke tooling | `python -m fullstack.deploy.smoke` (`§4`) |
| Authority | ACT-009 map; `FDP-009` registered |

## 3. Pre-flight

| # | Item | State | Holder |
|---|---|---|---|
| **P1** | Production `SUPABASE_SECRET_KEY` (secret key of `hmljfyqycxcueulhsjae`) as a Vercel variable, **Production scope only**, type Sensitive | **not set** (re-discovered 2026-10-01: no Production-scope variable) | **account holder** (external control; the value never passes through the session) |
| P2 | Production `AIOS_OPERATOR_TOKENS` for verification: one temporary principal `fs10-verification`, hash only | prepared at deployment time; removed after verification (`FDP-009-03`) | CEO |
| P3 | `VERCEL_ENV=production` | set by the platform on a Production deployment | platform |
| P4 | A backup of the Production store before the release (runbook `§7`) | Production holds 0 rows; a read-only export follows verification | CEO |
| P5 | Deployment Protection | **X2, decided and unchanged**: the Production URL answers 401/302 to anyone without Vercel access | Architect (to change) |
| P6 | Release candidate | **`d05261c`** | CEO (identified); Founder (approves in the release) |
| P7 | Test writes during verification | permitted, labelled by the verification principal's subject, minimal | CEO |
| P8 | H3 check cadence | runbook `§12.1` before and after every deployment, rollback or restore, and at each verification; weekly once released | CEO |
| P9 | Rollback | before a release: the CEO, when operationally required (promote the previous deployment); after a release: `ESC-02` | CEO / escalated |
| P10 | Permanent Production principals | `ESC-01` | escalated; before LIVE |

Without P1 the Production function answers 503 to every API request (no key; runbook `§3`), so a deployment could not be verified. Deploying before P1 would change Production for no evidence; the deployment therefore follows P1.

## 4. Deployment and verification procedure

1. **Deploy** the release candidate `d05261c` as a Production-target deployment through the Vercel connector, from that commit. The repository's default branch is **not** merged (a merge would also deploy, and would carry unrelated documents).
2. **Read** the deployment: READY, build log *"Using Python 3.12 from .python-version"*, Production alias moved to it, protection unchanged.
3. **Temporary access** (`FDP-009-03`): one automation bypass and the `fs10-verification` principal, each recorded; evidence holds no secret.
4. **Verify** with `python -m fullstack.deploy.smoke` (read-only, then `--write`), plus the Production-specific checks: the run lands in the Production store and **not** in Preview (SQL on both), `VERCEL_ENV` resolution, L1 lines in the host log, the runbook `§12.1` checks.
5. **Revoke**: remove the bypass; remove the verification principal and redeploy the same commit, so the deployed function no longer accepts it; verify the bypass gives the same response as none and the token gives 401.
6. **Release Package** (`FDP-009` `§9`): candidate, commit, deployment, every check's evidence, protection state, temporary-access and revocation evidence, open issues, the result.
7. **Stop** at the Founder Release Authorization.

## 5. Smoke, health and integration plan

`fullstack/deploy/smoke.py`, tested in `fullstack/tests/test_smoke.py` (8 tests, Python 3.11 and 3.12).

| Step | Check | Profile | Writes to the store |
|---|---|---|---|
| Health | `GET /health` 200, `runtime_state: running` (R2) | read-only | no |
| Smoke | anonymous, invalid and malformed `Authorization` refused on every protected route; valid bearer authenticates; Runtime running; read routes answer; console served with its security headers | read-only | no |
| Integration | Scenario B (a run succeeds and reads back) and Scenario C (a failure is a meaningful state) | `--write` | **yes: permanent**, labelled by the subject `fs10-verification` |
| Operational verification | the runbook `§12.1` checks; a read-only export of the Production store verified against its digests | manual, runbook | no |

The tool reads secrets from files, prints none, stores none in its evidence, aborts if a response echoes a credential, and **never enables `--write` by itself**. It does not infer an environment from a host name.

## 6. Current frontier

**Production Deployment, waiting on P1** (the account holder sets the Production database key). Everything else needed to deploy and verify is in place and authorized.
Remaining: Production Deployment · Production Verification · Release Package · Founder Release Authorization · Production Release · LIVE · Operational AIOS.

---

# History: FS-10 as written at entry (2026-09-30), before ACT-009 and `FDP-009`

The text below is the document as it stood before the authority review. Its `§1`
and pre-flight over-escalated P5–P8 and mislabelled P1–P2 (ACT-009 record `§2`).
Kept unaltered as history.

| Field | Value |
|---|---|
| **Stage** | FS-10 Deployment & Operationalization (Act `§21`) |
| **Status** | **ACTIVE — Deployment Preparation** (entered 2026-09-30, automatically, on FS-09 PASS / CLOSED: `ACT-CC-POST-P13-AIOS-FULL-STACK-008` `§27`; Register `§104`) |
| **Production** | **not deployed, not LIVE.** Production serves `22c0b49` (before this program) and is untouched |
| **Founder Release Authorization** | **NOT YET ISSUED.** Construction and verification are authorized; the release to LIVE is not (`§28`) |
| **Release candidate** | not yet named. The commit whose build is promoted is the Founder's to name; the rollback floor is that commit (runbook `§10`) |

```text
FS-09 CLOSED → FS-10 START
   → Deployment Preparation   ← current frontier
   → Production Deployment  (Founder-reserved operator actions)
   → Smoke Test → Health Check → Integration Test
   → Production Verification → Operational Verification
   → Founder Release Authorization → LIVE
```

## 1. What is authorized now, and what is not

| Authorized under the parent program (built or verified here) | Founder-reserved (`FD-FS-001` D4-A; ACT-008 `§28`) |
|---|---|
| preparing and verifying the deployment path on Preview | Production credentials: the Production `SUPABASE_SECRET_KEY` and `AIOS_OPERATOR_TOKENS` |
| the smoke, health and integration tooling, and its tests | a Production deployment, promotion or alias change |
| the pre-flight checklist and the decisions the Founder must take | Production Deployment Protection settings |
| backups and restores of Preview | any Production write, including smoke records |
| evidence, runbook and ownership updates | the Founder Release Authorization, and the word LIVE |

## 2. Done at entry

| Item | State |
|---|---|
| FS-09 | PASS / CLOSED (`FS-09-ACT-008-EXECUTION-RECORD.md`); gate READY, which is not a release |
| Preview | `dpl_EJucmiuLbgmgX1ar7SDZ25Ngp3ER` (`d05261c`), Python 3.12, verified live; protection ON; no temporary bypass |
| Production store | `hmljfyqycxcueulhsjae`: migration `20260928051800_aios_records` applied, schema equal to Preview, **0 rows**, append-only triggers |
| E1 wiring | `VERCEL_ENV` selects the project; unknown refuses (503); a Preview key never serves Production |
| Runbook, ownership, backup and rollback procedures | written and drilled on Preview (runbook `§7`–`§10`, `§12.1`) |
| Smoke tooling | `python -m fullstack.deploy.smoke` (this stage, `§4`) |

## 3. Pre-flight for a Production deployment

Nothing below is done for Production. Each row says who holds it.

| # | Item | State | Holder |
|---|---|---|---|
| P1 | Production `SUPABASE_SECRET_KEY` as a Vercel variable in **Production scope only** | not set | operator, on a Founder decision |
| P2 | Production `AIOS_OPERATOR_TOKENS`: hash-only, its own principals and scopes (not the Preview principal) | not set | operator, on a Founder decision |
| P3 | `VERCEL_ENV=production` | set by the platform on a Production deployment; cannot be tested before one exists | platform |
| P4 | A backup of the Production store immediately before the release (runbook `§7`) | procedure verified on Preview; Production holds 0 rows today | operator |
| P5 | Deployment Protection for the Production host: today `ssoProtection` is on for all deployments except custom domains, so a `*.vercel.app` Production URL answers 401/302 to anyone without Vercel access | a decision | Founder |
| P6 | The release candidate commit | not named | Founder |
| P7 | Smoke write policy (`§4`) | not decided | Founder |
| P8 | Alerting: H3 means no automatic alert; who runs `§12.1` and how often once Production serves traffic | owner in the ownership model; cadence to confirm | Founder / operator |
| P9 | Rollback: Production rollback is the Founder's; the floor is the release candidate | documented | Founder |

## 4. Smoke, health and integration plan

`fullstack/deploy/smoke.py`, tested in `fullstack/tests/test_smoke.py` (8 tests, Python 3.11 and 3.12).

| Step | Check | Profile | Writes to the store |
|---|---|---|---|
| Health | `GET /health` 200, `runtime_state: running` (R2) | read-only | no |
| Smoke | anonymous, invalid and malformed `Authorization` refused on every protected route; valid bearer authenticates; Runtime running; read routes answer; console served with its security headers | read-only | no |
| Integration | Scenario B (a run succeeds and reads back) and Scenario C (a failure is a meaningful state) | `--write` | **yes: permanent** |
| Production verification | the same, against the Production URL, with the Production principal | read-only first; `--write` only on decision P7 | per P7 |
| Operational verification | the runbook `§12.1` checks run once; a backup exported and verified; the rollback floor named | manual, runbook | no |

The tool reads secrets from files, prints none, stores none in its evidence, aborts if a response echoes a credential, and **never enables `--write` by itself**: it prints the target before it writes. It does not infer an environment from a host name.

**Why P7 is a decision.** The store is append-only. A smoke run against Production leaves a run, its Trace and audit entries in Production for good. That may be acceptable (a labelled first run) or not; it is the Founder's call, not an engineering default.

## 5. Current frontier and what remains

**Current frontier: Deployment Preparation — the Founder decisions P1, P2, P5, P6, P7 and P8 (`§3`).** Until they exist, no Production step can start.

Completed in FS-10 so far: the stage entered; the boundary stated (`§1`); the smoke and health tooling built and tested; the pre-flight written.
Remaining: Production Deployment · Smoke Test · Health Check · Integration Test · Production Verification · Operational Verification · Founder Release Authorization · LIVE.

---

# History: FS-10 as written before FS-09 passed

The text below is the document as it stood when FS-10 was NOT STARTED. It is kept
as the record of the order `FD-FS-001` D4-A fixed and of the proof that remains
to be produced.

| Field | Value |
|---|---|
| **Stage** | FS-10 Deployment & Operationalization (Act `§21`) |
| **Status** | **NOT STARTED.** Nothing has been deployed anywhere |

## Why it has not started

`FD-FS-001` D4-A fixes the order:

```text
FS-09 Production Readiness PASS  →  Founder Release Decision  →  FS-10  →  Live verification  →  Operational AIOS
```

| Precondition | State |
|---|---|
| FS-09 PASS | **not met** (`FS-09-PRODUCTION-READINESS.md`) |
| Founder Release Decision | **not requested**: it follows an FS-09 PASS |
| Deployment architecture | **FS-DP-04 not ratified** |

Deploying now would be *"deploying production merely because infrastructure
exists"* (NC-24), which the Act forbids.

## Final Operational Proof (Act `§22`)

**Not produced.** It needs a deployed system. No claim of Operational AIOS is
made (Act `§31`; NC-06, NC-19).

What the local system already demonstrates is the shape the proof will take
(Act `§22`, adapted to the implemented capabilities):

```text
REQUEST (browser) → APPLICATION SURFACE (console) → BACKEND (/api/v1/runs)
→ AIOS CONTRACT (Execution, WorkflowLifecycle, ToolInvocationGovernance)
→ RUNTIME → EXECUTION → CAPABILITY (docs.read; Engineering Intelligence Testing)
→ STATE (run record) → TRACE (one per acting Agent) → RESULT → PERSISTED EVIDENCE
```

It holds locally (FS-07). The Act asks for it live, on the deployed system.
