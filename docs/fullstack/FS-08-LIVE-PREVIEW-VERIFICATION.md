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

(recorded below, after the Preview built from the commit that adds this record)
