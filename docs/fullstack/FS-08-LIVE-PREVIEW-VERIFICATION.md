# FS-08 — Live Preview Verification (ACT-CC-POST-P13-AIOS-FULL-STACK-003)

| Field | Value |
|---|---|
| **Instruction** | Founder instruction *"EXECUTE STEP 2: AIOS_OPERATOR_TOKENS"*, 2026-09-27: generate the operator token, configure its hash entry in Vercel **Preview** only, redeploy the Preview, verify live |
| **Founder confirmation** | `SUPABASE_SECRET_KEY` re-entered in Vercel Preview as one line (Vercel shows it updated at 2026-09-27 17:48:36 UTC by the account holder) |
| **Register** | `§84` |

## 1. Token generation

| Item | Value |
|---|---|
| Command | `python -m fullstack.backend operator-token --subject founder --scope aios.observe --scope aios.workflow.run --scope aios.audit` |
| Where | this session's sandbox. Output written to a mode-600 file in the session's scratch directory, **outside the repository**, and never printed |
| Token | 43 characters (32 random bytes, URL-safe). **Not recorded here, not committed, not sent to anyone** |
| Entry | subject `founder`; scopes `aios.audit`, `aios.observe`, `aios.workflow.run`; `sha256` of the token. Checked before use: it parses, and the token authenticates as `founder` with exactly those scopes |

## 2. Vercel configuration

| Item | Value |
|---|---|
| Project | `aios-platform` (`prj_exqF51HASzlwn5kiO4kAGJ9mHe0N`) |
| Variable | `AIOS_OPERATOR_TOKENS`, env id `NHJxyX58g2U92d0U` |
| Type · target | **sensitive** · **preview only** |
| Value | a JSON array holding the one hash entry; no plaintext |
| Mechanism | the authorized Vercel connector (`create_project_env`) |
| Production | not touched: the project has **no** Production variables (`hiddenProductionEnvCount: 0`); no Production deployment, alias or credential changed |

## 3. Redeploy and live verification

**Redeploy:** the push of `819cb3a` built Preview `dpl_FzYqCpTFmEEQZe8BH8e8ZpbUfruL`
(`aios-platform-dbaxmzhj6-adibelepp21-bytes-projects.vercel.app`; region
`icn1`; READY at 17:56 UTC), with both Preview variables present.

| # | Check (Founder instruction) | Result | Evidence |
|---|---|---|---|
| 1 | Preview reaches AIOS application code | **PASS** | `GET /api/v1/health` answered by the function (its CSP and `X-Request-Id` headers; request `99965c89270760e0`) |
| 2 | `/api/v1/health` behaves as expected | **PASS** | 200 `{"status":"ok","runtime_state":"running"}`. The Runtime now **starts on the Supabase store** with the re-entered key (before: 503 *"key contains a character that cannot be sent"*) |
| 3 | missing or invalid token rejected | **NOT VERIFIED LIVE** | every other path requested through the connector (`/api/v1/runs`, `/api/v1/runtime`, `/`) was answered by Vercel SSO (302), not by the function; locally V1–V3 pass |
| 4 | the B3 token authenticates | **NOT VERIFIED LIVE** | the connector's fetch cannot send an `Authorization` header or a POST; direct HTTP is behind Vercel SSO (302) |
| 5 | protected API access with the token | **NOT VERIFIED LIVE** | as 4 |
| 6 | Supabase persistence | **PARTIAL** | connection and Runtime start on the store: evidenced. Writes: **not yet**; `aios_records` still holds 0 rows, because no request reached a writing route |
| 7 | run creation | **NOT VERIFIED LIVE** | needs POST with the token |
| 8 | Trace and audit association | **NOT VERIFIED LIVE** | follows 7 |
| 9 · 10 | concurrent runs distinct; no duplicate identity | **NOT VERIFIED LIVE** | needs parallel POSTs; locally V2 and V5 pass (50 of 50 distinct) |
| 11 | Production untouched | **PASS** | production deployment `dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj` unchanged; no Production variables |

**Boundary reached.** The remaining checks need direct HTTP requests to the
Preview carrying `Authorization: Bearer <token>`, including POSTs. The
authorized connector cannot send those, and direct requests meet Vercel
Authentication (SSO). Getting past it means one of the following:

- a share link (the connector's `get_access_to_vercel_url`, which Vercel
  describes as a link that *"bypasses authentication"*), or
- a Protection Bypass for Automation secret, or
- turning off Vercel Authentication for Preview deployments.

Each is a change to, or a way around, deployment protection. The Founder's
instruction says *"Do NOT bypass Vercel SSO"*. None was used. A Founder
choice is required.

**The plaintext token** exists only in this session's scratch directory
(mode 600, outside the repository). It is lost when the session ends. If it
is needed later, a new token is issued and its entry replaces the current one.
