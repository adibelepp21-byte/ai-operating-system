# FS-10 — Deployment & Operationalization

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
