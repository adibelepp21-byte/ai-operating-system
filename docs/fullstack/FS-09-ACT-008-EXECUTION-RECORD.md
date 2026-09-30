# FS-09 — Execution Record: ACT-CC-POST-P13-AIOS-FULL-STACK-008 (Final Closure)

| Field | Value |
|---|---|
| **Act** | `ACT-CC-POST-P13-AIOS-FULL-STACK-008`, *FS-09 Final Closure & FS-10 Continuation Master Act* (verbatim: `docs/governance/acts/…-008-…`) |
| **Register** | `§100` receipt · `§101` delegated decisions (Scenario A = A2; alerting = H3) · `§102` P12-W6 classification · `§103` final state |
| **Date** | 2026-09-30 |
| **Served code** | commit `d05261c`; final served deployment `dpl_EJucmiuLbgmgX1ar7SDZ25Ngp3ER` (Preview, Python 3.12 from `.python-version`, build `bld_7ijnvswek`) |
| **Evidence** | `evidence/FS-09-LIVE-PREVIEW-2026-09-30-ACT-008.json` · `…-ACT-008-REVOCATION-2026-09-30.json` · `…-BACKUP-EXPORT/MANIFEST-2026-09-30` · `…-ACT-008-P12-W6-CLASSIFICATION-…json` · `…-ACT-008-NEGATIVE-CONTROLS-…json` · `evidence/live-scripts-2026-09-30/` |

**Result: FS-09 = PASS / CLOSED.** Every `§25` criterion A to X is met (`§13`, `§11`). Declared under `§26`; it is not Production LIVE, not a Founder Release Authorization and not Operational AIOS. FS-10 is ACTIVE (`FS-10-DEPLOYMENT.md`).

## 1. What changed in this Act

| Area | Change | Where |
|---|---|---|
| Scenario A | FS-DP-07 **A2** selected (`ACT-008-DG-01`): `POST /api/v1/agent-instances`, `GET /agent-definitions`, `GET /agent-instances[/{key}]`, scope `aios.agent.register`, append-only partition `fullstack-agents`, console *Agents* view. Definitions are read, never written; a registration grants no authority | `fullstack/backend/agents.py`, `contract.py`, `api.py`, `security.py`, `frontend/`, Register `§101` |
| Alerting | **H3** re-verified as sufficient and final (`ACT-008-DG-02`); H1/H2 stay with the Founder | Register `§101`; runbook `§12.1` |
| Gate | Scenario A is *executed*, not classified; a missing check on a stale recording is BLOCKED; the revocation row needs the independent record, not a recording's own flag | `fullstack/readiness.py` |
| Documents | current-state wording reconciled (A2; Python 3.12); history kept | `§7` |

## 2. Mandatory scenarios

Each was run **locally in-process** (gate, tests, browser e2e over a socket) and **live on Preview** (`dpl_EJuc…`, commit `d05261c`).

### Scenario A — User → Create Agent → Backend → AIOS Agent Capability → Persist → Result

| | |
|---|---|
| **SETUP** | the Preview principal `founder` given scope `aios.agent.register` (`AIOS_OPERATOR_TOKENS`, hash-only, Preview scope) and redeployed; before that, the same commit refused the route |
| **ACTION** | `POST /api/v1/agent-instances {definition: engineering-intelligence-agent, instance_key: live-desk-09301849b, capabilities:[engineering-intelligence]}`; then read back, duplicate, unknown Definition, foreign capability, bad key, unknown field, six concurrent requests for one key |
| **EXPECTED** | 201 `REGISTERED`, `grants_authority: false`, persisted; later Runtime reads it identically; 409 / 400 / 400 / 400 / 400; exactly one 201 for the race; unauthenticated 401; without the scope 403 |
| **ACTUAL** | all as expected: 201; `GET` identical; `409, 400, 400, 400, 400, 404`; `[201, 409×5]`; `401` (none and invalid token); **403** `scope aios.agent.register is required` on `dpl_9Zmdw…` (same commit, principal not yet given the scope) |
| **TRACE / STATE** | the registration writes no Trace record (a registration is not an Agent action); lifecycle `REGISTERED`; the record names the authority (`ACT-008-DG-01`, FS-DP-07, A2), `created_by` and `runtime_id` |
| **DATABASE** | Preview `fullstack-agents`: 5 rows (`seq` 454, 464, 474, 484, 504), one per key, none duplicated; **Production: 0 rows** |
| **SECURITY** | 401 / 403 / valid / audit: the audit holds the allowed `founder` POSTs and the refused 401s, no credential; the browser e2e shows an observer refused with the UI bypassed |
| **EVIDENCE** | live recording checks *Scenario A: …* (7) and the 403 check; `test_agents.py` (20); console e2e (15 checks); gate row *agent creation (Scenario A)* |

Two limits, stated. The **console** was driven against a real server over a socket (Chromium, 15 checks) but **not** against the live Preview: Chromium does not trust the sandbox proxy's CA, and TLS verification is not disabled. A first run of the live script registered two keys and then crashed on one transport-level SSL EOF (no HTTP response) in a concurrent thread; the script now retries transport errors only and was re-run with fresh keys. Both attempts' registrations remain in the append-only store.

### Scenario B — User → Start Workflow → Runtime → Execution → Tool → Result

| | |
|---|---|
| **SETUP / ACTION** | `POST /api/v1/runs` `document-conformance-review` on `docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md`, criterion `INV-4`; single, 5 sequential, 8 concurrent |
| **EXPECTED / ACTUAL** | 201 `succeeded`; all 201; 8 distinct runtime-derived ids, 58 runs listed, 58 distinct (for example `run-20260930T184837Z-7ea192fc43626732-0`) |
| **TRACE / DATABASE** | the run's 3 Trace records are its own Runtime's; persisted in Supabase, read by a later Runtime (`identical=True`); Production 0 rows |
| **SECURITY / EVIDENCE** | requires `aios.workflow.run`; live checks 4–11; gate row *Scenario B* |

### Scenario C — Execution failure → Runtime → Trace → Backend → Frontend → meaningful state

| | |
|---|---|
| **ACTION** | the same run on `docs/absent.md` |
| **EXPECTED / ACTUAL** | 201 with state `failed` and reason `docs.read execution_failure: 'docs/absent.md' is not a document in the repository`; invalid input 400, unknown workflow 400, unknown run 404 |
| **TRACE / DATABASE / EVIDENCE** | the failure is a persisted run with its Trace; live check 12; console e2e scenario C; gate row *Scenario C* |

## 3. E1 environment separation

| Check | Result |
|---|---|
| Preview → Preview Supabase | the function resolves `VERCEL_ENV=preview` to `scfymftfzkpilqbgmfwv`; proven live: every write of this Act is in that store |
| Production → Production Supabase | `production` resolves to `hmljfyqycxcueulhsjae` (measured by the gate with the real resolver; no key, no deployment and no call — **a Production target is not exercised live**, because no Production key or deployment exists and none may be created here) |
| Unknown → fail closed | `UnknownEnvironment` → 503 before any key or database call; not testable live (`VERCEL_ENV` is set by the platform); verified with the real resolver in-process (`test_environment_separation.py`, 11; gate) |
| Isolation test | fresh Preview writes present in the Preview store (5 registrations, 72 runs, 273 audit entries, 204 Trace records at the end); **Production: 0 rows** before and after every suite, the rollback drill, the export and the UPDATE attempt |
| Variables | `AIOS_OPERATOR_TOKENS`, `SUPABASE_SECRET_KEY`: Preview only; none in Production |

## 4. Security and Vercel posture

| Requirement | Result |
|---|---|
| Protection ON | `ssoProtection` enabled (`all_except_custom_domains`) before, during and after; without the bypass the final deployment answers 401/302 |
| One temporary instrument | exactly **one** Protection Bypass for Automation was created (Preview project scope), because `web_fetch_vercel_url` is GET-only and sends no `Authorization` header or body; no other bypass or shareable link was created |
| Revoked and verified absent | revoke call (`regenerate: false`) → `protectionBypass: {}`; the old secret gets the same 302 as no secret on the final deployment, the branch alias and the project alias (401 for JSON clients on five hosts including the Production deployment URL); `get_project` still shows SSO protection |
| Count at closure | **0** |
| Protected API fail-closed | anonymous and invalid/malformed `Authorization` → 401 on every protected route (live checks 1–2); the unconfigured composition authenticates nobody |
| 401 / 403 / valid / audit | 401 (missing, unknown, hash-as-token, truncated, wrong scheme, no scheme, empty bearer); 403 (missing scope, live and local); valid B3 bearer → session with the four scopes; audit holds subjects and decisions, no credential |
| Secret handling | the bypass secret was generated locally into a private file and supplied to the create call, so it appears in this session's tool call (disclosed); it is in no repository file, evidence file or log (repository scan: 0 hits), and it is revoked |

## 5. Observability (L1 · M1 · alerting · readiness)

Kept separate. **L1** `fullstack.request/1` JSON line per request: `request_id`, method, route **template**, status, latency, `runtime_id`; no subject, credential, body or raw path. **M1** `fullstack/deploy/request_metrics.py` (not the historical `metrics.py`) derives count, status classes, server errors and p50/p95/max per route. **Readiness (R2)** is `GET /health`, not alerting. **Alerting** is **H3**: no automatic alert; the checks are runbook `§12.1`.

Live: the 20 requests of the Scenario A run were matched by request id against the host's runtime log, **20 of 20**, with matching method and status; M1 from those lines: 20 requests, 2xx 7, 4xx 13, 0 server errors, p95 153 ms; `{instance_key}` appears as a template, no key in any route; no credential in any line. Limit: two later log queries (a 12-request probe) timed out at the log service; the probe's ids are recorded but not matched.

## 6. Backup/restore and rollback

**Backup/restore** on current data (505 records, `seq ≤ 510`, including the registrations): export accepted record by record against the database's own SHA-256 (505/505), every partition's and the table's joined digest equal, store unchanged afterwards, credential scan clean, restored into an empty local store and into `SupabaseStorage` (in-memory PostgREST) byte-identically, a second restore refused, and the application reads 66 runs, every Trace, 245 audit entries, 189 Trace records and the registrations, the API serves them. Detail: `FS-09-BACKUP-RESTORE-DRILL.md` `§6`. The 2026-09-27 export is the historical control.

**Rollback and roll-forward** on Preview: current `dpl_EJuc…` → rolled back to `dpl_Gumff1…` (`d6afbdc`) → rolled forward. Rolled back: reachable (health 200, anonymous 401); the A2 routes answer 404 (proof of which code served); it read the newer code's run and accepted Scenario B and C; rolled forward: the newer code read the run written during the rollback and still listed the 5 registrations. This shows **data compatibility**. **Operational safety** is distinct and unchanged (runbook `§10`): below `0706446` (C1) the concurrency identity risk returns; below `215248f` (B3) the API authenticates nobody; below `200bd81` Scenario A is unavailable. Production rollback is the Founder's.

## 7. Reproducibility and documents

Python **3.12** pinned by `.python-version`; the build log reads *Using Python 3.12 from .python-version*; the project declares no dependency (the platform creates an empty `pyproject.toml`); a fresh, cache-less redeploy of the same commit (`dpl_EJuc…` from `dpl_9Zmdw…`) built and behaved identically. Stale "3.11 current" wording reconciled, history kept: `FS-09-DECISION-REGISTER.md` `§1.5`, `FS-09-READINESS-PROGRAM.md`, `FS-00-ENTRY-STATE.md`, FS-DP-07 status, decision-package README, FS-02 `§3` (already amended). The decision packages keep their text as the record of the question they asked.

## 8. P12-W6 regression

`FS-09-P12-W6-CLASSIFICATION.md` (Register `§102`): one test in `tools/` is red because verbatim Founder Acts raised the `Status:` label share by 0.0026 over its hard-coded tolerance. **RAW RESULT** preserved; **CLASSIFICATION** known classified P12 baseline guard condition; **DOES NOT BLOCK FS-09** (no FS-09 code involved; bisected and shown by counterfactual). P12 untouched.

## 9. Negative controls NC-01 … NC-20

Held: `fullstack/tests/test_negative_controls.py` (18 tests) and the live facts in `evidence/FS-09-ACT-008-NEGATIVE-CONTROLS-2026-09-30.json`. NC-07/08/09: one Production deployment (`dpl_A5Qs…`, `22c0b49`), no Production variable, 0 Production rows. NC-10: bypass count 0. The secret scan was checked to detect a real-looking secret and to ignore only deliberate fakes.

## 10. Regression

Run from a clean worktree of commit `01b1fd0` (the commit that carries these documents), by suite and by Python version. Targeted, integration, live, regression and negative-control evidence are kept apart (`§22`).

| Suite | Python 3.12 (reference) | Python 3.11 |
|---|---|---|
| native_core | 801 OK (1 expected failure) | 801 OK (1 expected failure) |
| consumers | 276 OK | 276 OK |
| bounded_exception | 29 OK | 29 OK |
| fullstack (targeted + integration, incl. security, environment separation, observability, backup/restore, agents, negative controls, browser e2e) | **289 OK** | 289 OK |
| tools | 1933 run, **1 failure**, 1 skipped (2469 s) | not run |

**Expected failures = explicitly classified historical controls only:** the `native_core` expected failure (unchanged since baseline) and the one `tools` failure, `test_the_narrower_population_is_not_better [status]`, which is the P12-W6 signal classified in `§8` (Register `§102`). **Unexpected failures = 0.**

| Kind | Evidence |
|---|---|
| Targeted | `test_agents` 20, `test_environment_separation` 11, `test_backup_current` 15, `test_negative_controls` 18, node unit tests 16+ |
| Integration | `test_integration` (browser e2e, 15 checks, over a real socket) |
| Live | `evidence/FS-09-LIVE-PREVIEW-2026-09-30-ACT-008.json` (FS-08 checks 0-12, FS-09 checks, Scenario A, rollback drill) |
| Regression | the table above |
| Negative control | NC-01..NC-20 (`§9`) |

* **Citation audit:** 94 warnings and 0 errors, the same 94 as baseline `edb3beb` (measured again after this record was added).
* **Certified-evidence integrity:** holds; `native_core/`, `consumers/` and `tools/` are unchanged since `edb3beb`; no Phase 14 path.
* **Instruments:** ACT-004 to ACT-008 are byte-identical since their receipt commits (NC-02).
* **Secret scan:** the operator token and the bypass secret appear in no file of the repository, in evidence or in history; the pattern scan finds none outside deliberate fakes (NC-11, NC-12).
* **Working tree:** clean at the declaration.

## 11. Final re-discovery (independent, on current state)

Run after the last live check, the revocation and the documents, on current state and not on the assumption that earlier work was right (`§24`).

| # | Question | Answer, with the check |
|---|---|---|
| 1 | Exact FS-09 state | gate **READY** (not a release): 30 PASS, 1 OBSERVED (latency), 0 FAIL, 0 BLOCKED, `awaiting: []` |
| 2 | Any requirement unresolved? | No. Scenario A, alerting, E1, security posture, observability, backup, rollback, reproducibility, documents: each has a row and evidence above. Residuals are limits, not open requirements (`§12`) |
| 3 | Any blocker still actionable? | No. `LIVE-REVERIFICATION` and `BYPASS-REVOCATION` are cleared by recorded evidence; nothing remains in the gate's `awaiting` |
| 4 | Stale evidence in use? | No. `git diff d05261c -- <served paths>` is empty, so the live recording covers the served tree; the 2026-09-27 export and the older recordings are labelled history and are not read by the gate |
| 5 | A current document contradicting? | Searched for A1-as-current and 3.11-as-current wording and for FS-09/FS-10 state statements: the active ones now carry a current-state banner or row (README, program, return package, decision register, readiness program, FS-DP-07 status); history is kept |
| 6 | External temporary access active? | No. Bypass count 0 (revoke response `{}`; the old secret gets the same 302 as no secret on three hosts) |
| 7 | Preview isolated from Production? | Yes. Production holds 0 rows; one Production deployment (`22c0b49`), unchanged; no Production variable |
| 8 | A mandatory scenario unproven? | No. A, B and C each have SETUP to EVIDENCE in `§2`, live and local. Not proven live: the console's Agents view against the Preview (stated) |
| 9 | An actual test failure unexplained? | No. The one failing test (`tools`, P12-W6) is explained, bisected and classified (`§8`) |
| 10 | A Founder-reserved matter used as a blocker? | No. Nothing in this record waits on the Founder to close FS-09. Production credentials, deployment and release are Founder-reserved and are not FS-09 work |
| 11 | A real blocker labelled non-blocking? | No. The P12-W6 signal was tested for being hidden FS-09 damage (bisect, counterfactual); H3's lack of an automatic alert is a stated limit of an option the architecture defines, not a failing requirement |
| 12 | Does the canonical exit gate PASS? | Yes: `python -m fullstack.readiness evaluate` reports no FAIL, no BLOCKED and nothing awaited |


## 12. Limits and residuals, all stated

* **No automatic alert** (H3): failures are found only when a person runs `§12.1`. H1/H2 need a Founder decision (spending, recipient, external service).
* **Production target not exercised live**: no Production key or deployment exists; isolation is shown by the resolver, by Production's 0 rows, and by the unchanged Production deployment.
* **Unknown environment** is verified in-process, not live.
* **The console was not driven against the live Preview** (browser and sandbox CA); it is verified against a real server over a socket.
* **P12-W6** stays red in the global runner (`§8`).
* **A 403 is shown live on the previous deployment of the same commit** (`dpl_9Zmdw…`) because, after the scope was added, one principal holds every scope.
* **Host log**: the later observability probe could not be matched (log service timeouts).
* **Backups** exist only when an operator runs one; cadence and owner wait on the Founder. No point-in-time recovery on the free plan.
* **The Founder Release Authorization is not issued**; Production is not LIVE; Final Production release stays Founder-reserved.

## 13. Gate

`python -m fullstack.readiness evaluate`: **READY, never a release** (`FD-FS-001` D4-A): 30 PASS · 1 OBSERVED · 0 FAIL · 0 BLOCKED · `awaiting: []`. Every row is listed by `python -m fullstack.readiness evaluate`; the recording it reads is `evidence/FS-09-LIVE-PREVIEW-2026-09-30-ACT-008.json` and the revocation record is `evidence/FS-09-ACT-008-REVOCATION-2026-09-30.json`.

## 14. §25 criteria

| | Criterion | Met by |
|---|---|---|
| A | all mandatory requirements verified | `§2` to `§9`, gate |
| B, C, D | Scenario A, B, C PASS | `§2` |
| E | E1 separation verified | `§3` |
| F, M | Security, access control PASS | `§4`, live checks 0-3, 403 |
| G, L | Reliability, failure handling PASS | live checks 9-12, `§2` C, gate |
| H | Backup/restore PASS | `§6` |
| I | Rollback PASS | `§6` |
| J | Reproducibility PASS | `§7` |
| K | Observability PASS | `§5` |
| N | documentation reconciled | `§7`, banners |
| O | live evidence fresh | recording covers `d05261c`; served diff empty |
| P | negative controls HELD | `§9` |
| Q | no Production mutation | Production 0 rows; one unchanged deployment |
| R | no active temporary bypass | `§4` |
| S, T, U | no BLOCKED, FAIL or UNKNOWN item | gate `awaiting: []`, 0 FAIL, 0 BLOCKED; residuals stated in `§12` |
| V | final re-discovery completed | `§11` |
| W | evidence persisted | `evidence/` |
| X | working tree clean | checked at the declaration |
