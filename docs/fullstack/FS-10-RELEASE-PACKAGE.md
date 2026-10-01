# FS-10 — Release Package (`FDP-009` `§9`)

| Field | Value |
|---|---|
| **Nature** | **Evidence. Not Founder Release Authorization** (`FDP-009` `§9`, `§10`) |
| **Prepared by** | Claude Code, CEO under `FDP-009` `§8` (Register `§107`); recorded at Register `§108`; **updated under `FDP-010` `§17` step 11 (Register `§109`, `§110`) — see `§18`** |
| **Current authority** | `FDP-009` + `FDP-010` (`FS-10-CURRENT-AUTHORITY.md`); the closed FS-09 gate is history (`FDP-010-03`) |
| **Date** | 2026-10-01 |
| **Production Verification result** | **PASS** |
| **State** | **PRODUCTION DEPLOYED · PRODUCTION VERIFIED · RELEASE PACKAGE READY · FOUNDER RELEASE AUTHORIZATION REQUIRED** |
| **Not** | released, LIVE, publicly accessible, Production accepted, or an operational AIOS. None of these is claimed or implied (`FDP-009-02` `§5.3`–`§5.6`) |
| **Release readiness** | **not blocked by rollback readiness**: a verified known-good rollback target exists (`§18.2`) |
| **Evidence** | `evidence/FS-10-FDP-010-OPERATIONAL-ACCESS-ROLLBACK-2026-10-01.json` (`§18`) · `evidence/FS-10-PRODUCTION-VERIFICATION-2026-10-01.json` (every result below, raw) · `evidence/FS-10-PRODUCTION-L1-2026-10-01.jsonl` · `evidence/FS-10-PRODUCTION-BACKUP-MANIFEST-2026-10-01.json` with `…-BACKUP-EXPORT-2026-10-01.jsonl` |

Facts are observed unless marked **[INF]** (inference).

## 1. Release candidate identity

| Item | Value |
|---|---|
| Candidate | **`d05261c`**, identified by the CEO (`FDP-009` `§8`); approving it is the Founder's |
| Why this commit | the served tree verified live on Preview at FS-09 (`dpl_EJucmiuLbgmgX1ar7SDZ25Ngp3ER`, `FS-09-ACT-008-EXECUTION-RECORD.md`) |
| No substitution | `git diff d05261c 72ad0fb` over every served path (`api`, `vercel.json`, `.python-version`, `requirements.txt`, `fullstack/__init__.py`, `fullstack/deploy/__init__.py`, `fullstack/deploy/vercel.py`, `fullstack/backend`, `fullstack/frontend`, `native_core`, `consumers`, `tools/__init__.py`, `tools/certified_write_barrier.py`) is **empty**. Later commits are documents, tests and tools outside the function |

## 2. Commit identity

`d05261cb7c02c6c489efbe5dff67ec86a22c0136` on `claude/aios-activation-authority-discovery-enq7bk` (*"FS-09 ACT-008: classify the P12-W6 regression signal (Register §102) …"*). The default branch `claude/aios-genesis-planning-hmbvlc` was **not merged** and is unchanged.

## 3. Production deployment identity

*As verified at Register `§108`. Serving now: `dpl_s8c6mTVKiQixKrjYwyqeKso1kXSv` (`§18.1`).*

| Deployment | Commit | Role | State |
|---|---|---|---|
| **`dpl_CHV72ePvPE7doNu4WaKp93qXXu8x`** (`aios-platform-p5o0g6or9-…`) | `d05261c` | **serving Production now**; alias `aios-platform-adibelepp21-bytes-projects.vercel.app`; built after the verification principal was removed | READY |
| `dpl_Dfs1Fx8P9G4QuNd1EYPSwet3VLG1` (`aios-platform-37py3evu2-…`) | `d05261c` | the deployment Production Verification ran on | READY, superseded |
| `dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj` | `22c0b49` | the Production deployment before FS-10 | READY, serves 404 (no application) |

## 4. Deployment evidence

| Check | Result |
|---|---|
| Deployed through the Vercel connector from the commit (`gitSource` sha `d05261c`, target `production`) | both builds clone *"Branch: claude/aios-activation-authority-discovery-enq7bk, Commit: d05261c"* |
| Runtime | *"Using Python 3.12 from .python-version"* in both build logs (`FS-09-RUNTIME` P2) |
| READY, alias, `aliasError` | READY in ~20 s each; Production alias moved; `aliasError: null` |
| Project domains | unchanged (`aios-platform-eight.vercel.app` still bound to this branch's Preview) |
| `project.live` | `false` |

## 5. Smoke-test evidence

`python -m fullstack.deploy.smoke` against the Production alias, the token and bypass read from private files:

| Profile | Result |
|---|---|
| read-only | **7 / 7 PASS**: health and readiness; anonymous refused on all 6 protected routes (401); 4 invalid/malformed `Authorization` forms refused (401); valid bearer authenticates as `fs10-verification`; Runtime running; 6 read routes 200; console served with its 4 security headers |
| write | **10 / 10 PASS**: the 7 above, plus Scenario B `run-20261001T053718Z-6c55fe9d86584905-0` succeeded and reads back identically, plus Scenario C (`docs/absent.md`) a `failed` run with a failure reason |

## 6. Health-check evidence

`GET /api/v1/health` → **200 `{"status":"ok","runtime_state":"running"}`** on the verification deployment (three times) and on the final deployment (eight times, during the revocation check). R2 holds.

## 7. Integration-test evidence

| Chain | Result |
|---|---|
| console → API → Native Core workflow → tool (`docs.read`) → criteria → run record → trace | Scenario B: run `succeeded`, outcome conformant 1/1; 3 trace records; read back equal |
| failure as a state | Scenario C: run `failed`, `failure_reason` *"docs.read execution_failure: 'docs/absent.md' is not a document in the repository"*; 2 trace records |
| scope enforcement | `POST /agent-instances` without `aios.agent.register` → **403** *"scope aios.agent.register is required"*; no instance created (`GET` → `[]`) |
| audit | `GET /audit` (scope `aios.audit`) → 200; entries carry `at`, `decision`, `method`, `path`, `request_id`, `scope`, `status`, `subject` |
| append-only surface | `DELETE /runs` → **405**; unknown route → **404** |

Minimal data: **no** agent instance was registered on Production (Scenario A, already proven on Preview, would have added permanent records to no verification end).

## 8. Security verification

| Check | Result |
|---|---|
| X2 deployment protection in force | without the bypass, every host answers **302** (plain) / **401** (JSON, from the platform; no application request id) — before, during and after |
| bypass alone grants nothing | bypass, no token → **401** from the application |
| token alone grants nothing | valid token, no bypass → **302** |
| security headers | API: CSP, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `X-Request-Id`, `Cache-Control: no-store`; console: all four |
| no secret echoed | every response checked by the tools; none aborted |
| no secret stored | Production store: 0 rows containing `Bearer`, `Authorization`, `protection-bypass` or the token hash; the export file: 0 of the runbook `§7` patterns |
| no secret in the repository | repository scan for the bypass value: 0 files |
| Production key | present (`SUPABASE_SECRET_KEY`, Production scope only, Sensitive), set by the account holder; **never decrypted, never read** |

## 9. Environment verification

| Check | Result |
|---|---|
| E1 resolution | the Production function wrote to **`hmljfyqycxcueulhsjae`** (0 → 64 rows) |
| Preview separation | Preview store `scfymftfzkpilqbgmfwv`: **554 rows, max seq 559** before and after — unchanged |
| Variables | Production: `SUPABASE_SECRET_KEY` (unchanged), `AIOS_OPERATOR_TOKENS` = `[]` (`§14`); Preview: both unchanged |

## 10. Database / state verification

| Check | Result |
|---|---|
| Schema | migration `20260928051800` only; triggers `aios_records_no_update_or_delete`, `aios_records_no_truncate` |
| Rows | **64**, seq **1–64 contiguous**: `fullstack-audit` 57 · `fullstack-runs` 2 · `trace` 5 |
| Content | verification data only, attributed to subject `fs10-verification` (28 records) or to no subject (refusals) |
| Backup | read-only export, every partition and the table equal to the server digests (table `782dee3e…`); manifest `FS-10-PRODUCTION-BACKUP-MANIFEST-2026-10-01.json` |

The read-only smoke profile appended 18 access-audit records: by design every protected request is audited. The tool's docstring said read-only wrote nothing; corrected (`fullstack/deploy/smoke.py`, not a served path).

## 11. Observability verification

| Check | Result |
|---|---|
| L1 | **50** `fullstack.request/1` lines in the host log for the verification window, one per application request (19 read-only + 22 write + 9 additional); **9 / 9** request ids of the additional checks matched |
| M1 | from those lines: 50 requests, `2xx` 26, `4xx` 24, **server errors 0**, latency p50 63 ms, p95 181 ms, max 404 ms; equal to the host's own counts by status |
| Levels | `info` 50; **0** warning, error or fatal on Production since 05:30 |
| H3 (runbook `§12.1`) | readiness ✓ · error rate ✓ · refusals before the Application: none (no `runtime_id: null` / 503) ✓ · backup freshness: export of 2026-10-01 ✓ · temporary access: bypass list empty ✓ |

## 12. Rollback readiness

*As at Register `§108`. Current: `§18.2` — a verified known-good target now exists.*

| Item | State |
|---|---|
| Mechanism | Vercel instant rollback / promote of a previous Production deployment (runbook `§10`, drilled on Preview in ACT-008) |
| Candidates | `dpl_Dfs1…` (same commit; built with the verification principal's hash, whose token is destroyed, so it authenticates nobody usable) — **[INF]** functionally equivalent to the current one; `dpl_A5Qs…` (`22c0b49`) serves 404: a rollback to it takes the application **offline**, it does not restore a prior working version, because none exists |
| Data | the store is append-only and independent of the deployment; a rollback leaves it untouched |
| Performed | **no**. `FDP-009` `§8` permits a rollback when operationally required; it was not |
| After a release | `ESC-02`, unresolved (Founder) |

## 13. Deployment-protection state

**X2 unchanged**: `ssoProtection` enabled, `all_except_custom_domains`; password protection off; trusted IPs off; **Protection Bypass for Automation: none** (control response `{"protectionBypass":{}}`). No custom domain. Nothing was removed, weakened or redesigned (`FDP-009-02` `§5.5`).

## 14. Temporary-access evidence (`FDP-009-03`)

| Item | Value |
|---|---|
| Principal | `fs10-verification`, scopes `aios.observe`, `aios.workflow.run`, `aios.audit` (**not** `aios.agent.register`); configured as hash `ea472a60…a0ec3` only, Production scope; the token generated locally into a mode-600 file, never printed |
| Bypass | one automation bypass, note *"FDP-009-03 TEMPORARY FS-10 Production verification; revoke after use"*; SHA-256 `4b44c951…`. Its value was generated locally and supplied to the create call, so it appears in this session's tool call (disclosed, as in ACT-008); it is in no repository file, evidence or log |
| Use | verification only, 05:36–05:39 UTC; then the revocation checks |

The 14 conditions: necessary (Production is behind X2 and has no principal) ✓ · limited to verification ✓ · temporary (~8 min) ✓ · evidenced (this package) ✓ · certified architecture unmodified ✓ · X2 unmodified ✓ · no permanent bypass ✓ · no public access ✓ · not a release ✓ · not LIVE ✓ · revoked immediately after ✓ · post-revocation verified ✓ · secrets under ACT-003 `§28` ✓ · Production data changed only by the labelled verification records ✓.

## 15. Revocation evidence

| Step | Result |
|---|---|
| Principal | `AIOS_OPERATOR_TOKENS` (Production) set to `[]`; the same commit redeployed as `dpl_CHV72…`; with the bypass still active, the token → **401** on the alias and on `dpl_CHV72…` (`/api/v1/session`, plain and JSON) |
| Bypass | revoked; control response `{"protectionBypass":{}}` |
| Verified | on **5 hosts** (Production alias, `dpl_CHV72…`, `dpl_Dfs1…`, `dpl_A5Qs…`, `aios-platform-eight`), the revoked bypass gives **exactly** the response of no bypass: plain **302**, JSON **401**, with or without the token |
| Credentials destroyed | local token and bypass files shredded; only their hashes remain |

**TEMPORARY ACCESS = NONE.**

## 16. Unresolved issue classification

*As at Register `§108`. Current status of every item: `§18.4`.*

| # | Issue | Class | Blocks release? |
|---|---|---|---|
| U-1 | **No permanent Production principal** (`ESC-01`): after revocation nobody can use the API on Production | FOUNDER-RESERVED decision; needed **before LIVE**, not before release authorization | not this gate; LIVE |
| U-2 | Rollback after a release (`ESC-02`) | UNKNOWN / Founder | not this gate |
| U-3 | No prior working Production version: rollback = offline (`§12`) | inherent to the first deployment; recorded | no |
| U-4 | `dpl_Dfs1…` retains the verification principal's **hash** | residual configuration; the token is destroyed and X2 protects the deployment | no |
| U-5 | The `AIOS_OPERATOR_TOKENS` Production variable exists, holding `[]` (the connector offers no delete) | cosmetic; equivalent to absent (nobody authenticated); the account holder may delete it | no |
| U-6 | Monitoring is H3 (manual), no alert (runbook `§12.1`, residual `R2.10`) | decided (ACT-004 / ACT-008) | no |
| U-7 | P12-W6 regression signal, classified (Register `§102`) | outside the served code | no |
| U-8 | Transport errors (TLS EOF at the sandbox proxy): the first principal-revocation probe aborted before any response and was re-run with a retry on transport errors only (4 retries, all then answered) | client-side, before any response | no |

| U-9 | The FS-09 readiness gate's criterion text still says *"Production rollback is Founder-only (FD-FS-001 D4-A)"* (`fullstack/readiness.py:714`); `FDP-009` `§8` now lets the CEO roll back before a release when operationally required | stale wording in the closed FS-09 gate (result unchanged: 30 PASS, 1 OBSERVED); `FDP-009` governs; left unedited so FS-09's closing evaluator is not altered | no |

| U-10 | `fullstack/deploy/smoke.py` (added at FS-10 entry, `b586a9b`) did not install the certified-write barrier in its `__main__` (GOAL-V2-004); found by `tools.tests.test_certified_write_closure` in this regression | **fixed** (barrier installed first, as in `fullstack/readiness.py`); the tool is not a served path; the Production runs used `-m`, which loads only `fullstack` packages, and wrote evidence only to a scratch directory outside the repository | no |

No unresolved **blocking** Production condition was found.

### Regression, citation and governance checks (2026-10-01, on the commit carrying this package)

| Check | Result |
|---|---|
| `native_core` | 801 OK (1 expected failure) on Python 3.12 and 3.11 |
| `consumers` | 276 OK on 3.12 and 3.11 |
| `tools/bounded_exception` | 29 OK on 3.12 and 3.11 |
| `fullstack` (incl. negative controls, smoke, readiness) | 297 OK on 3.12 and 3.11 |
| `tools` | 1933 run: **2 failures** — `test_certified_write_closure` (U-10, fixed; re-run 51 OK) and the P12-W6 population signal (`test_p12_governance_evidence_verification … [status]`, ratio 0.5047 against 0.4925), **classified** at Register `§102`, P12 untouched |
| Citation audit | 0 errors, 94 warnings (unchanged) |
| Readiness gate | unchanged: 30 PASS, 1 OBSERVED |
| Boundaries | no diff in served paths, `native_core`, `consumers`, `tools` (except the fix above, outside `tools`), acts, Co-Founder V2 instruments, architecture or program documents; Register append-only |

## 17. Final Production Verification result

**PRODUCTION VERIFICATION PASS.** Release candidate `d05261c` is deployed to Production (`dpl_CHV72ePvPE7doNu4WaKp93qXXu8x`) behind unchanged X2 protection. Smoke 7/7 and 10/10, health, integration, security, environment separation, state, observability and revocation all pass, and temporary access is none.

**FOUNDER RELEASE AUTHORIZATION REQUIRED.** This package does not authorize Production Release, LIVE, traffic or an operational AIOS (`FDP-009` `§10`). The Founder decides.

## 18. Update under `FDP-010` (2026-10-01; Register `§109`, `§110`)

Evidence: `evidence/FS-10-FDP-010-OPERATIONAL-ACCESS-ROLLBACK-2026-10-01.json`. Current authority: `FS-10-CURRENT-AUTHORITY.md`.

### 18.1 Operational access (`FDP-010-01`, `ESC-01` resolved)

| Item | Result |
|---|---|
| Principal | `aios-operator`; scopes `aios.observe`, `aios.workflow.run`, `aios.audit` from the canonical model; **not** `aios.agent.register`; Production only; hash `0ccb723c…` in `AIOS_OPERATOR_TOKENS` (the `FDP-010-04` empty-list residual is replaced by the approved principal; the connector offers no delete) |
| Deployments | `d05261c` rebuilt twice with it: **`dpl_76CYCCMjZf4SvT9BLwcNDV4Hdc8T`** (rollback target) then **`dpl_s8c6mTVKiQixKrjYwyqeKso1kXSv`** (serving the Production alias); Python 3.12; default branch not merged |
| Scopes verified | smoke read-only **7/7** on both, as `aios-operator` with exactly the three scopes; one Scenario B run (`run-20261001T064549Z-6ea7aa47802a7a93-0`, `requested_by: aios-operator`) |
| Negative controls | `aios.agent.register` → **403**, nothing registered · the Preview principal on Production → **401** · the operator on Preview → **401** · the operator on the superseded `dpl_CHV72…` and `dpl_Dfs1…` → **401** · bypass without token → **401** · token without bypass → **302** (X2) · unknown token → **401** |
| Audit | 107 entries, 25 attributed to `aios-operator`. One check of mine failed on its own assumption (it read the first five entries of an oldest-first list) and was corrected by paging; recorded as such |
| Custody | the delegated CEO's execution environment, private file; in no repository file, document, evidence, log or chat; rotation and revocation: runbook `§15` |

### 18.2 Rollback (`FDP-010-02`, `ESC-02` resolved)

| Item | Result |
|---|---|
| **Designated verified known-good target** | **`dpl_76CYCCMjZf4SvT9BLwcNDV4Hdc8T`** — deployable (READY), compatible (same commit, schema, variables, region and store), verified (smoke 7/7; it reads the run the serving deployment wrote, equal), immutable identity, documented (`FS-10-CURRENT-AUTHORITY.md` `§3`, runbook `§9`) |
| Vercel candidacy | `isRollbackCandidate: true` only for the target and the serving deployment; **false** for `dpl_A5Qs…` (`22c0b49`, **not a valid target**, `FDP-010` `§6.1`), `dpl_CHV72…`, `dpl_Dfs1…` |
| Procedure | Instant Rollback to the designated target only; then runbook `§1` and `§12.1`; evidence. **Not executed**: not operationally required |
| Limit | same commit: recovers from a failure of the serving deployment or its configuration; cannot undo a defect of `d05261c` itself (no earlier working application exists) — `FDP-010` `§8` containment applies |
| **Release readiness** | **not blocked by rollback readiness** (`FDP-010` `§15`) |

### 18.3 Governance reconciliation (`FDP-010-03`)

The closed FS-09 gate (`fullstack/readiness.py`) is **byte-identical** to its closing state `de47057`, its wording preserved. `FS-10-CURRENT-AUTHORITY.md`/`.json` state that `FDP-009` + `FDP-010` govern current operation and list the historical wording as superseded; the runbook keeps the old row labelled *History* under the current one; no served or operational module imports the gate or carries the wording. `fullstack/tests/test_current_authority.py` (13 tests) holds all of this.

### 18.4 Issues — current status

| # | Issue (from `§16`) | Status now |
|---|---|---|
| U-1 | no permanent Production principal | **resolved** (`FDP-010-01`; `§18.1`) |
| U-2 | rollback after a release | **resolved** (`FDP-010-02`) |
| U-3 | no prior working version; rollback = offline | **resolved for rollback readiness**: verified target of the same release (`§18.2`); the limit stands and is documented |
| U-4 | `dpl_Dfs1…` keeps the verification hash | unchanged, non-blocking; token destroyed; not a rollback candidate |
| U-5 | empty `AIOS_OPERATOR_TOKENS` | **resolved**: replaced by the approved principal (`FDP-010` `§11.4`) |
| U-6 | H3 manual monitoring | unchanged (decided) |
| U-7 | P12-W6 signal | unchanged (classified, `§102`) |
| U-8 | transport errors at the sandbox proxy | none in this run |
| U-9 | FS-09 gate rollback wording | **reconciled** (`FDP-010-03`; `§18.3`) |
| U-10 | smoke barrier install | fixed (`§108` follow-up) |
| **ESC-03** | **the CEO has no standing path through X2.** Members of the Vercel account pass X2 by login; a permanent bypass is excluded (`FDP-009` `§5.5`); temporary access is for verification only (`FDP-009-03`); the provider connector does not complete the SSO flow (302 on `/api/v1/health`). So the CEO can operate through the provider control plane (deploy, rollback, configuration, logs, read-only store access) but cannot call the AIOS API for routine operation | **open — a Founder / Architect matter** (X2 is Architect-reserved, FS-DP-03 `R2.10`: *"a Vercel login or a Founder-authorized, revocable mechanism"*). Not inferred. Non-blocking for the release decision: rollback, recovery and observation do not need the API |
| **SEC-OBS-02** | the connector's 302 carried a connector-created `_vercel_share` value (an expiring X2 share credential) in this session's tool output | classified: not reproduced anywhere; it does not pass the application's bearer check; the connector offers no revocation; the account holder may invalidate share links in the dashboard; the function is not used again on Production. Non-blocking |

### 18.5 `FDP-010` `§15` pre-requisites

| # | Requirement | State |
|---|---|---|
| 1 | permanent operational access model configured | **yes** (`§18.1`; `ESC-03` noted) |
| 2 | required operational scopes verified | **yes** |
| 3 | temporary verification credentials revoked | **yes**: bypass list empty; revoked bypass ≡ none on 7 hosts; credentials destroyed |
| 4 | no unintended operator token active | **yes**: Production accepts `aios-operator` only; superseded deployments refuse it; the verification token is destroyed |
| 5 | rollback target valid and documented | **yes** (`§18.2`) |
| 6 | current rollback authority reconciled | **yes** |
| 7 | historical FS-09 evidence immutable | **yes** (tested) |
| 8 | current FS-10 documentation points to `FDP-009`/`FDP-010` | **yes** (tested) |
| 9 | Release Package valid | **yes**: same candidate `d05261c`; served paths unchanged |
| 10 | no unresolved **blocking** security or operational condition | **none found** (`ESC-03` and `SEC-OBS-02` classified non-blocking) |

**State:** PRODUCTION DEPLOYED · PRODUCTION VERIFIED · RELEASE PACKAGE READY · **FOUNDER RELEASE AUTHORIZATION REQUIRED**. Nothing here authorizes Production Release, LIVE, traffic or an operational AIOS (`FDP-010` `§16`).

### 18.6 Checks under `FDP-010` (on `4343b64`)

| Check | Result |
|---|---|
| `native_core` · `consumers` · `tools/bounded_exception` · `fullstack` | 801 · 276 · 29 · **310** OK on Python 3.12 and 3.11 (`fullstack` adds the 13 current-authority tests) |
| `tools` | 1933 run, **1 failure**: the P12-W6 population signal, classified at Register `§102` (ratio 0.5093 against 0.4932), P12 untouched |
| Citation audit | 0 errors, 94 warnings (unchanged) |
| FS-09 readiness gate | unchanged: 30 PASS, 1 OBSERVED; file byte-identical to `de47057` |
| Mutation checks | a current "Founder-only" rollback line → test fails; an edited FS-09 gate → 2 tests fail |
| Boundaries | no diff in served paths, `native_core`, `consumers`, `tools`, the FS-09 gate, acts, Co-Founder V2 instruments, architecture or program documents; Register append-only |
| Secrets | no bypass value, share value or token plaintext in the working tree; Production records: 0 credential patterns |

## 19. Update under `ACT-CC-POST-P13-AIOS-FS10-ESC03` (2026-10-01; Register `§111`, `§112`)

Record: `FS-10-ESC-03-AUTHORITY-RESOLUTION.md`.

| Item | Status now |
|---|---|
| **ESC-03** | **NOT RESOLVED — ARCHITECT DECISION REQUIRED.** Canonical X2 authority found and consistent; no mechanism is authorized for the CEO's routine API operation; 15 mechanisms classified (record `§6`–`§8`); package `decision-packages/FS-DP-03-R3-ESC-03-OPERATIONAL-EDGE-ACCESS.md` (no option selected). **Non-blocking for the release decision** as before: rollback, recovery and observation run through the provider control plane |
| **SEC-OBS-02** | **closed.** Re-examined (record `§5.3`): the connector's fetch had created deployment shareable links on six deployments (two today, twelve values on five Preview deployments on 27 and 30 September). The only link that still existed was **revoked**; every other known value no longer exists. None was in the repository or evidence; none passed B3. **Correction of `§18.4`:** the connector *does* offer revocation at the deployment level (`patch_url_protection_bypass`); the statement that it offers none was wrong |
| Negative controls NC-01–NC-10 | **PASS** (record `§8.2`; `fullstack/tests/test_esc03_boundaries.py`) |
| Temporary / permanent bypass | **NONE / NONE** |
| Release readiness | unchanged: not blocked by rollback readiness; no unresolved **blocking** condition |

**State:** PRODUCTION DEPLOYED · PRODUCTION VERIFIED · RELEASE PACKAGE READY · **FOUNDER RELEASE AUTHORIZATION REQUIRED**. **PRODUCTION RELEASE = FOUNDER RESERVED · LIVE = FOUNDER RESERVED.**

## 20. Update under `AD-FS10-ESC03` (2026-10-01; Register `§113`, `§114`)

| Item | Status now |
|---|---|
| **ESC-03** | **NOT RESOLVED.** Evidence phase complete for authority (`FS-10-ESC03-ARCHITECTURE-DECISION.md`; 70 classified findings). Final ADR state **ARCHITECTURE CONSTRAINED — NO AUTHORIZED MECHANISM**; E-A–E-F **UNSELECTED**; **Founder decision required** (`decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE.md`). Non-blocking for the release decision |
| New finding | **nobody can use the Production API today**: the Founder passes X2 but holds no Production principal; the CEO holds `aios-operator` but cannot pass X2. Raised in the package as a related Founder question; it bears on Operational AIOS, not on the release decision |
| Implementation | none; no bypass, identity, token, service or X2 change |

**PRODUCTION RELEASE = FOUNDER RESERVED · LIVE = FOUNDER RESERVED.**
