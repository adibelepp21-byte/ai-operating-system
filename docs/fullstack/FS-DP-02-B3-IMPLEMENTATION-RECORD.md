# FS-DP-02 B3 — Operator Bearer Tokens: Implementation and Verification Record

| Field (decision `§15`) | Value |
|---|---|
| **Decision ID (of the instrument)** | `FS-DP-02-ARCHITECT-DECISION` |
| **Parent** | FS-08-ACT-003 (`docs/fullstack/FS-08-ACT-003-EXECUTION-RECORD.md`) |
| **Option** | B3 — Operator Bearer Tokens |
| **Decision** | RATIFY |
| **Authority** | Architect (Moriarty); instrument `docs/governance/acts/FS-DP-02-ARCHITECT-DECISION-RATIFY-B3-OPERATOR-BEARER-TOKENS.md`, Register `§81`. The text is preserved as received |
| **Implementation** | the commit that adds this record (`git log -- docs/fullstack/FS-DP-02-B3-IMPLEMENTATION-RECORD.md`) |
| **Final status** | **B3 LOCAL IMPLEMENTATION = COMPLETE · B3 LOCAL VERIFICATION = PASS · B3 LIVE PREVIEW VERIFICATION = BLOCKED** (EXT-03, and no token hashes configured for Preview) |

`ARCHITECT DECISION ≠ IMPLEMENTATION ≠ VERIFICATION` (decision `§14`).

## 1. Discovery before change (decision `§7`)

| Read | Finding |
|---|---|
| package `FS-DP-02` rev. 2 | B3 = *"the host stores only its SHA-256 hash with a subject and scopes (`AIOS_OPERATOR_TOKENS`)"*; *"a drop-in `Authenticator`"*; boundary `§R2.11`: one `Authenticator` in `security.py` and its composition in `vercel.py` and `__main__.py`; scopes, `authorize`, audit, console and CSP unchanged |
| request path | `Application` → `_authenticate` (fails closed on an exception) → `authorize(principal, scope)` → audit → handler (`api.py`) |
| protected routes | every route of `contract.ROUTES` but `GET /api/v1/health` names a scope |
| token handling | the console sends `Authorization: Bearer <credential>` from `sessionStorage` (`frontend/api.js`); the shipped compositions used `NoAuthenticator`; tests used a test-only plaintext token map |
| minimum surface | one authenticator plus its configuration parser, two composition points, tests. No public contract changes |

**Configuration format.** The package names the content (a hash, a subject
and scopes) but no syntax. The syntax chosen is the smallest that carries
exactly that content: a JSON array of `{"subject", "sha256", "scopes"}`.
`scopes` defaults to `aios.observe` (the package's least-privilege rule). Any
other key is refused, so a plaintext token cannot be configured by mistake.

## 2. What was built

| File | Change |
|---|---|
| `fullstack/backend/security.py` | `OperatorTokenAuthenticator`, `parse_operator_tokens`, `token_sha256`. It accepts only `Bearer <RFC 6750 b64token>` (the scheme is case-insensitive, as HTTP defines it). It hashes the presented token and compares it with **every** configured hash through `hmac.compare_digest`, with no early exit. A configuration that does not parse exactly is refused whole and authenticates nobody; the reason is kept, never the value |
| `fullstack/deploy/vercel.py` | `authenticator_from_environment` reads `AIOS_OPERATOR_TOKENS` when the function loads. A refused configuration is logged by its reason only |
| `fullstack/backend/__main__.py` | `serve` uses the same authenticator. `operator-token` prints a new 32-byte random token once and its hash entry; it writes nothing |
| `fullstack/readiness.py` | the "secrets not exposed" check verifies the B3 posture. The authentication criterion stays **FAIL** until a live deployment evidences it |
| tests | `test_fs_dp_02_b3.py` (19 tests). The whole fullstack suite now authenticates through the production authenticator, configured with the hashes of the obviously fake test tokens. The test-only plaintext token map was removed |

Unchanged: `Principal`, the scopes, `authorize`, the audit ledger and its
format, every route, the console, the CSP, `native_core/`, `consumers/`,
`tools/`, the schema and migration, `vercel.json`.

## 3. Verification (decision `§9`)

| ID | Verification | Evidence | Result |
|---|---|---|---|
| V1 | missing bearer token | `V1MissingCredential`: every protected route of the contract answers 401; no run created | **PASS** |
| V2 | invalid bearer token | `V2InvalidCredential`: unknown token, case variant, truncated, extended, and the hash presented as a token all get 401 | **PASS** |
| V3 | malformed bearer token | `V3MalformedCredential`: 15 malformed headers (empty, scheme only, double space, trailing space or newline, Basic, no scheme, two credentials, non-ASCII, 600 chars, NUL, padding only) all get 401 `unauthenticated`, never 500 | **PASS** |
| V4 | valid operator token | `V4ValidCredential`: 201 on a run, the session names the subject and exact scopes, audit records the subject | **PASS** |
| V5 | protected route enforcement | `V5ProtectedRouteEnforcement`: the only public route is health, and it returns only `status` and `runtime_state` | **PASS** |
| V6 | no plaintext token persistence | `V6NoPlaintextPersistence`: a `token` key (even beside a valid hash), a plaintext in `sha256`, upper-case hex and unknown keys are refused. The authenticator holds hashes and principals only. `operator-token` writes no file | **PASS** |
| V7 | fail closed | `V7FailClosed`: 10 bad configurations authenticate nobody and never quote the value; one bad entry refuses the whole configuration; a refused request reaches no handler (0 runs, 0 Trace) | **PASS** |
| V8 | console flow | `V8ConsoleFlow`, and `test_integration.ConsoleInABrowser` (Chromium) now running through B3: sign in with the token, run, fail, list, audit | **PASS** |
| V9 | no unauthenticated bypass | `V9NoSideDoor`: other headers (`X-Gate-Principal`, `X-Forwarded-User`, `X-AIOS-Token`, `Cookie`, `Proxy-Authorization`), query tokens, other methods and path forms grant nothing | **PASS** |
| V10 | Full Stack regression | `§4` | see `§4` |
| V11 | governance regression | `§4` | see `§4` |
| V12 | certified-root integrity | `§4` | see `§4` |
| V13 | security negative controls | `§5` | see `§5` |
| V14 | Preview authentication | **BLOCKED**: the Preview is behind Vercel SSO (EXT-03), and no token hashes are configured for Preview | **BLOCKED** |

**Security properties (`§8`):** S1 = V1; S2 = V2; S3 = V3; S4 = V4; S5 = V6;
S6 = V5 plus `test_security.ProductionPosture`; S7 = V7 plus
`test_security.test_a_failing_authenticator_authenticates_nobody`; S8 = V8;
S9 = V9; S10 = `S10SecretBoundary`: neither token nor hash appears in
storage, any response, stdout or stderr, and no real hash or
`AIOS_OPERATOR_TOKENS=` value is tracked under `fullstack/`, `api/` or
`vercel.json`. All **PASS**, locally.

**Mutation checks** (each reverted, bytecode caches cleared after each):

| Mutation of `security.py` | Tests failing |
|---|---|
| any bearer becomes the first principal | 12 |
| a plaintext `token` key accepted | 1 (after the test was tightened: at first it survived, because its case also lacked `sha256`) |
| a bad entry skipped instead of refusing the whole configuration | 4 |
| the token written to stderr | 3 |
| an alternate header honoured | 1 |
| prefix match instead of full match | 4 |

## 4. Regression

**Clean full run** (bytecode caches cleared, no edits during the run):

| Suite | Result |
|---|---|
| `native_core` | 801 · OK (1 expected failure, unchanged) |
| `consumers` | 276 · OK |
| `tools/bounded_exception` | 29 · OK |
| `fullstack` | 134 · **1 failure**: `S10SecretBoundary.test_no_real_token_hash_is_committed` |
| `tools` | 1933 · **1 failure**: `test_governance_index.test_no_identifier_is_indexed_twice` (1 skipped) |

Both failures were defects in this change, not in the product. Both were
fixed, not suppressed:

1. **The S10 scan matched its own file.** Once staged, the test file is
   tracked, and its `assertNotIn("AIOS_OPERATOR_TOKENS=", …)` literal
   contained the text it forbids. The needle is now built by concatenation.
   The check itself is unchanged.
2. **A duplicate identifier.** This record's first row was labelled
   *Decision ID*, which the governance index reads as this record's own
   identifier. That duplicated the instrument's. The row is now labelled
   *Decision ID (of the instrument)*; the value is unchanged.

**After the fixes:** `fullstack` 134 · OK. The governance, certification and
P12 modules: 182 · OK. The 47 modules that read the Register, acts and
records: see `§7`. Citation audit: 0 errors, 94 warnings (baseline).
Certified-root integrity (V12): P10 36, P11 58, P12 121, P13 1 files intact;
no faults; certified phases `{10, 11, 12, 13}`, no anomalies; P13 closed.
The P12 predecessor guard passes at this corpus state, as recorded at
FS-DP-05; its classification is unchanged.

## 5. Negative controls (decision `§10`)

| Control | Result |
|---|---|
| NC-01 Native Core #12 · NC-02 Native Core #11 | **HELD**: `native_core/` unchanged |
| NC-03 certified P1–P13 roots · NC-04 P13 · NC-05 Phase 14 | **HELD**: 0 files under `docs/architecture/` or `tools/`; P10–P13 integrity verified (`§4`) |
| NC-06 · NC-07 authority expansion | **HELD**: nothing ratified, certified or released by Claude Code |
| NC-08 multi-user identity | **HELD**: operator principals only; no identity in the Domain Model; no sign-up, sessions or identity store |
| NC-09 Supabase Auth | **HELD**: not used |
| NC-10 authorization redesign | **HELD**: `authorize` and the scopes unchanged; V4 shows scopes still decide |
| NC-11 persistence architecture | **HELD**: no store, schema or migration change; configuration lives in the host environment |
| NC-12 protected-route bypass | **HELD**: V1, V5, V9 |
| NC-13 plaintext tokens persisted | **HELD**: V6 |
| NC-14 credentials in logs or responses | **HELD**: S10 |
| NC-15 unrelated Full Stack contracts | **HELD**: routes, formats, console and CSP unchanged |
| NC-16 Preview → Production release | **HELD**: nothing deployed to production |

## 6. Re-discovery (decision `§16`)

| Question | Finding |
|---|---|
| new dependency | none (stdlib `hashlib`, `hmac`) |
| new authority question | **none requiring escalation now**. The instrument names no initial principals or grants, token lifetime, or whether Preview and Production share principals. The implementation fixes none of them: they are the operator's configuration (package `§R2.14`) |
| new security boundary | the bearer token is the credential; its holder is the principal. The console keeps it in `sessionStorage`, as before. HTTPS only on Vercel |
| architectural conflict · scope expansion | none |
| regression | none (`§4`) |
| new external dependency for FS-08 | **yes: `AIOS_OPERATOR_TOKENS` for Preview.** The Founder issues a token (`python -m fullstack.backend operator-token …`) and sets its entry in Vercel as a sensitive Preview variable. The token goes into the console, never into chat |

## 7. Final targeted re-run

The 47 `tools` modules that read the Register, acts and records, on the final
tree: **1160 run, 1 failure**. The failure is
`test_e11_measurement_currency` (`tools.stale_state_audit`), the
**pre-existing latent test-order weakness** classified in
`ACT-CC-POST-P13-AIOS-FULL-STACK-003` `§17`. It appears only when a subset is
run, and it passed in the full `tools` run above (`§4`). It is not caused by
this change and was not modified.

## 8. Preview observations after `215248f` (2026-09-27)

| Observation | Evidence | Meaning |
|---|---|---|
| The Preview of `215248f` (`dpl_BcWaYPR7rAvWDkwkJbY3aGa14hc9`) is READY in `icn1` | Vercel deployment record | the B3 code builds and deploys from the commit |
| Through the connector, `GET /api/v1/health` reached **the function itself**: 503 JSON with the adapter's own headers (CSP, `X-Request-Id`), not the Vercel SSO redirect seen before | `web_fetch_vercel_url`, 17:38:47 UTC | **EXT-03: the Preview is now reachable** by the authorized connector. No protection setting was changed by Claude Code |
| The 503 is *"the AIOS Runtime could not start on its store"*; the function log reads `StorageUnavailable: database call failed (ValueError)` | runtime log of that deployment | the database call failed **before** reaching Supabase |
| Locally, with fake keys, only a key with a **line break inside it** makes the transport raise a bare `ValueError`. Non-ASCII, spaces, tabs and quotes fail differently | reproduction with `urllib_transport` | the configured `SUPABASE_SECRET_KEY` value most likely has a line break in the middle. The value was not read |
| `AIOS_OPERATOR_TOKENS` is not configured for Preview | project env list | even with a working store, no request would authenticate yet |

**Adapter repair** (`ACT-CC-POST-P13-AIOS-FULL-STACK-003` `§12`, configuration
and deployment-adapter errors): `storage_from_environment` now refuses a key
containing anything but the characters a Supabase key is made of. The function
answers 503 with *"the server-side database key contains a character that
cannot be sent … enter it again as one line"*, never quoting the value, and
makes no database call. Test:
`test_a_malformed_key_is_named_as_such_and_never_quoted`. Persistence semantics
are unchanged (FS-DP-01).
