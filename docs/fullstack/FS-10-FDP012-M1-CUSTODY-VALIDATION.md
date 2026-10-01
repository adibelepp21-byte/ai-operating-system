# FS-10 — FDP-012 M1 Credential Delivery & Custody Validation

| Field | Value |
|---|---|
| **Instruction** | Master Instruction *"AIOS FS-10 — FDP-012 Credential Delivery & Custody Validation"* (verbatim: `docs/governance/acts/MI-FS10-FDP012-CREDENTIAL-DELIVERY-CUSTODY-VALIDATION.md`; sha256 `e560cb24…`; Register `§120`) |
| **FDP-012** | **NOT RECEIVED** — the instruction refers to it, but its decision text is not in the message or anywhere in the repository. **Not validated, not canonicalized, not registered** (`§3`) |
| **M1 gates** | 7 PASS · **6 FAIL** (G1, G3, G6, G7, G8, G10) · **3 UNKNOWN** (G2, G4, G5) |
| **Final state** | **STATE B — BLOCKED — TELEMETRY / LOGGING / SESSION ISOLATION** |
| **O-A / ESC-03 / FDP-010 / FS-10** | authorized, NOT IMPLEMENTED / NOT RESOLVED / NOT COMPLETE / NOT READY |
| **Release / LIVE** | **RELEASE NOT AUTHORIZED · LIVE NOT ACTIVE** |
| **Date** | 2026-10-01 |

No real bypass was created, obtained, installed, used or revoked. No secret was set, printed, transmitted or stored. FDP-011, X2, B3 and Production are unchanged. No synthetic-value test was run: M1 variables can be set only by the account holder in the environment dialog, and no tool here can set one (`§4`).

Evidence classes: [CAN] canonical · [DV] directly verified · [PD] provider-documented · [TE] test evidence · [INF] inferred · [UNK] unknown.

## 1. Scope

This record covers two questions (MI `§0`, `§6`):
1. Is the FDP-012 decision valid, and can it be canonicalized?
2. Can the M1 environment-variable path deliver and hold the O-A bypass value for one operating session under FDP-011 T5 and `FDP-010` `§11.4`?

Each of the sixteen gates is evaluated **as the MI defines it**. FDP-012's own text, once received, must be checked against these results.

## 2. Canonical authority

| Instrument | State |
|---|---|
| `FDP-009` `33fecb97…` (`§107`) | canonical, unchanged [DV] |
| `FDP-010` `fa1d8b12…` (`§109`) | canonical; NOT COMPLETE [DV] |
| `FDP-011` `5a6e5a8b…` (`§117`) | canonical, unchanged: O-A authorized; T5 custody [DV] |
| T5 feasibility record (`§119`) | preserved unchanged as historical evidence; one correction recorded here (`§4.1`) |
| X2 | SSO on (`all_except_custom_domains`), no bypass, no trusted IPs; project `updatedAt` `1790837188645` [DV] |
| B3 | unchanged; `aios-operator` three scopes [DV] |
| Production | serving `dpl_s8c6m…`; designated rollback target `dpl_76CYC…` [DV] |
| Release Package | `§22` current [DV] |

## 3. FDP-012 validation

| Check | Result |
|---|---|
| Decision text present? | **NO.** The session transcript holds this Master Instruction, which *describes* FDP-012's scope (MI `§4`), but no FDP-012 decision instrument. The repository and Register contain no FDP-012 record; the Register mentions it only in `§119` (*"no FDP-012"*) [DV] |
| Conflicts, ambiguity, missing authority | **cannot be assessed** without the text |
| Canonicalization | **NOT PERFORMED.** The MI's description of FDP-012 is not the decision. Persisting it as FDP-012 would manufacture a Founder Decision (MI `§2`: *"Do not silently rewrite FDP-012"*; standing rule: a Founder Decision is never inferred) |
| Consequence | AUTHORITY PASS **not reached** for M1 (MI `§25`). Independently, the M1 gates below do not pass |

## 4. M1 mechanism description

The cloud-environment variable [PD: Claude Code docs, *Configure cloud environments*, *Set environment variables*]:
- The account holder enters `KEY=value` lines in the environment dialog at claude.ai/code. There is no other entry point, and no tool in this session can set one [DV: toolset — `list_environments` is read-only].
- Delivery: *"A session reads the environment's values into ordinary environment variables that any command Claude runs can read, except `OTEL_*` variables."*
- When values are read: *"when you create it and again each time Claude Code starts in the session's VM afterward"* — on restore after idle, or on rebuild after reclaim.
- Edits and removal: *"an existing session … keeps the values it last read until its VM is next restored or rebuilt."*
- Visibility: *"Anyone who uses the environment can read the values."* The dialog *"warns against putting secrets there."*
- This session's environment: `env_01X4j1qVyxMRoTsGvotFpwue` (*"MoriartyContent plan"*), personal, Anthropic-hosted; it has also held one other (archived) session [DV].

### 4.1 Correction to the T5 feasibility record (Register `§119`, M3)

`§119` recorded proxy-side credential injection (M3) as *"platform-managed; no user-configurable route documented"*, based on `/root/.ccr/README.md`. The provider documentation does describe a user-configurable route: **API credentials**. On Pro and Max plans, the account holder stores a key on the environment, and *"Anthropic's agent proxy adds the key to requests for the hosts you list, after each request leaves the session's VM. The key never reaches Claude, the commands it runs, or the session's environment variables."*
- Custom header names are supported.
- The value cannot be viewed after saving.
- It applies *"in every session that runs in the environment … until you delete it"*.
- It is not available on Team or Enterprise plans; this account's plan is [UNK].

This mechanism is **not M1**. It is **outside FDP-012's scope as described** (MI `§4`), and it is recorded here only as a correction of fact: not evaluated against the gates, not ranked, not selected. `§119` stays unchanged as historical evidence.

## 5. G1–G16 results

| Gate | Result | Basis |
|---|---|---|
| **G1** Creation boundary | **FAIL** | Creating the variable leaves the plaintext stored provider-side, shown to *"anyone who uses the environment"*, and placed in every session's environment. The Founder does not remain sole custodian. The provider advises against secrets here [PD] |
| **G2** Delivery boundary | **UNKNOWN** | Founder's browser → claude.ai → VM process environment. Not necessarily via chat or tool output. Anthropic-side tracing and telemetry and the provider's storage path are undocumented [UNK] |
| **G3** Secret visibility | **FAIL** | Any command Claude runs can read, enumerate or print it [PD]. Exposure is prevented only by conduct, not by a control |
| **G4** Telemetry isolation | **UNKNOWN → HARD STOP** | `CCR_ENABLE_TRACING=true`, `CLAUDE_CODE_DEBUG=true`, `ENV_MANAGER_ENABLE_DIAG_LOGS=true`, a telemetry socket present [DV]; what they capture of a new variable is undocumented [UNK]. The user-configurable OTEL export is opt-in and not configured (no `OTEL_*` variables) [DV/PD]. Absence of earlier leakage is not evidence (MI `§10`) |
| **G5** Logging isolation | **UNKNOWN → HARD STOP** | AIOS components pass by inspection (`§8`). Vercel request/runtime logging of the `x-vercel-protection-bypass` header is undocumented [UNK] |
| **G6** Process isolation | **FAIL** | Every command, subagent, test runner and background task in the session inherits it [PD; DV: the regression suites run as background commands in this session] |
| **G7** Session isolation | **FAIL** | Environment-scoped. Every session created, or restored from idle, in the environment while the variable is set reads it; no enforceable control [PD] |
| **G8** Routine execution isolation | **FAIL** | No Routine exists now [DV: `list_triggers` empty], but Routines use environments [PD] and nothing prevents one. Unrelated work inside the operating session inherits it (G6) |
| **G9** Lifetime control | **PASS** for the stage sequence, **conditional on G10** | Create (Founder, Vercel dashboard) → install (Founder, dialog) → new session → operate → stop → revoke (Founder, dashboard) → verify revocation (CEO, 302) → remove (Founder, dialog) → verify removal (`§13`). The last stage fails in G10 |
| **G10** Removal | **FAIL** | Removal reaches new sessions, but *"an existing session … keeps the values it last read until its VM is next restored or rebuilt"* [PD]. The operating session keeps the (revoked) value. The CEO cannot pause or reclaim its own VM [PD: *"you can't pause it yourself"*] |
| **G11** Revocation | **PASS** | The account holder revokes in Vercel's Deployment Protection settings [PD]; no value crosses chat or tool output. The connector path stays prohibited (T5) |
| **G12** Revocation verification | **PASS** (design; prior evidence) | A request carrying the value read from the environment, never printed, must answer 302. The same control passed under FDP-009-03 [DV, Register `§108`] |
| **G13** Evidence safety | **PASS** (AIOS tooling) | `smoke.py` records check, result and evidence text only; it raises `SecretEchoed` if a response echoes a credential; no headers are recorded [DV: code]. T8 fields need no value |
| **G14** B3 compatibility | **PASS** | O-A acts at the edge only; B3 unchanged. Bypass alone → 401; token alone → 302; `agent.register` → 403; Preview↔Production → 401 [DV, FDP-010 evidence] |
| **G15** X2 compatibility | **PASS** | Without bypass → 302; with bypass → reaches B3; after revocation → 302 [DV, FDP-009-03 / FDP-010]. X2 stays enabled; no trusted IP; nothing permanent or public |
| **G16** Release / LIVE firewall | **PASS** | No release, LIVE, promotion or deployment route [TE: `test_esc03_boundaries.py`] |

## 6. Evidence source for each gate

| Gate | Source |
|---|---|
| G1, G3, G6, G7, G10 | code.claude.com/docs/en/cloud-environments (*Set environment variables*; *Organization-shared environments*; *Environment caching*), fetched 2026-10-01 |
| G2, G4 | environment variable names and flag values (no secret values) [DV]; code.claude.com/docs/en/monitoring-usage (*Telemetry from cloud sessions*) [PD]; undocumented internal channels [UNK] |
| G5 | `fullstack/backend/api.py`, `telemetry.py`, `fullstack/deploy/smoke.py` [DV]; Vercel documentation search (no header-logging statement found) [UNK] |
| G8 | `list_triggers` → none [DV]; cloud-environments documentation (Routines use environments) [PD] |
| G9, G11 | Vercel documentation: bypass generated and managed in Deployment Protection settings; no automatic expiry [PD] |
| G12, G14, G15 | Register `§108`, `§110`; `evidence/FS-10-FDP-010-OPERATIONAL-ACCESS-ROLLBACK-2026-10-01.json` [DV] |
| G13, G16 | code and tests [DV/TE] |

## 7. Telemetry analysis

Three channels:
1. **User-configurable OTEL export.** Opt-in, and not configured here [DV]. When on, tool details and content are redacted unless `OTEL_LOG_TOOL_DETAILS` / `OTEL_LOG_TOOL_CONTENT` are set [PD].
2. **Anthropic-internal tracing and telemetry.** `CCR_ENABLE_TRACING`, the `SBX_TELEMETRY_SOCKET` socket. Content and handling of environment values are undocumented [UNK].
3. **Debug and diagnostic logs.** An existing injected secret was not found in about 290 diagnostic logs or in the transcript (Register `§119`) [DV]. Per MI `§10`, this absence is **not** proof for a new variable.

**G4 = UNKNOWN.**

## 8. Logging analysis (AIOS)

- **Request log.** `api.py` `_log`: one L1 line per request with method, route template, status, latency and runtime ID — no headers, no environment.
- **Errors.** Internal errors print a traceback (no environ dump).
- **Authentication.** `_authenticate` builds a header map in memory and logs nothing; exceptions fail closed silently.
- **Telemetry module.** `telemetry.line` serializes fixed fields only.
- **Smoke tool.** `smoke.py` sends the headers, never prints them, and aborts on an echoed credential.

The provider side is open: whether Vercel request or runtime logs record the bypass header is [UNK]. **G5 = UNKNOWN.**

## 9. Process inheritance analysis

The variable is part of the session's process environment for every command Claude runs, except `OTEL_*` [PD]. This includes test runners, background suites, subagents and helper scripts in the same VM [INF from PD; DV: this session runs regression suites as background commands]. No mechanism limits it to one operational context. **G6 = FAIL.**

## 10. Session isolation analysis

The variable belongs to the environment, not to a session [PD]:
- every session created in the environment while it is set reads it;
- so does every existing session whose VM restores from idle during that window;
- this environment has held another session [DV], and Routines can start sessions in an environment [PD];
- no control limits the window to the one authorized O-A session.

**G7 = FAIL.**

## 11. Routine execution analysis

No Routine is configured on the account today [DV]. Routines can target an environment [PD], and work inside the operating session (suites, subagents, background commands) inherits the variable (`§9`). **G8 = FAIL.**

## 12. Lifetime analysis

The stage sequence can be run with Founder actions at both ends (create and revoke in the Vercel dashboard; install and remove in the environment dialog). The CEO verifies revocation by a 302. Automatic expiry is not assumed (none documented). The sequence breaks at *verify removal*, because the operating VM keeps its copy (`§13`). **G9 = PASS only for the stage sequence; it cannot complete while G10 fails.**

## 13. Removal analysis

Removing the variable affects new sessions, and existing ones only after their VM restores or rebuilds [PD]. The operating session keeps the (revoked) value in its process environment until then. The CEO cannot pause or reclaim its own VM [PD], and an `unset` lasts only for one command [INF]. Removal can be confirmed for **new** sessions (by name, without the value), not for the operating one. **G10 = FAIL.**

## 14. Revocation analysis

The account holder revokes the bypass in Vercel's Deployment Protection settings; no value passes through chat or tool output [PD]. The connector's `revoke` needs the value and stays prohibited (T5). Verification is a request carrying the variable's value, never printed: 302 expected. **G11 PASS, G12 PASS.**

## 15. Evidence safety analysis

T8 fields (session, subject, purpose, times, deployment, operations, run IDs, results, revocation and its verification, final state) need no value. `smoke.py` emits none, and aborts on an echo. **G13 PASS** for AIOS tooling. The transcript stays safe only while no command prints the variable, which is the G3 failure.

## 16. X2 compatibility

Without O-A: 302 (re-verified 2026-10-01T11:18Z, Register `§116`). With an automation bypass: the request reaches B3. After revocation: 302 (FDP-009-03 evidence). X2 settings are unchanged. **PASS.**

## 17. B3 compatibility

Scopes `aios.observe`, `aios.workflow.run`, `aios.audit` work as authorized; `aios.agent.register` gives 403; invalid token or wrong environment gives 401; bypass without token gives 401 (FDP-010 evidence). No scope change. **PASS.**

## 18. Release / LIVE separation

O-A confers no Release, LIVE, Founder Release Authorization, traffic or public-exposure authority. The application has no such route (tests). **PASS.**

## 19. Hard-stop determination

| MI `§24` condition | Triggered |
|---|---|
| Telemetry behavior UNKNOWN | **yes** (G4) |
| Logging behavior UNKNOWN | **yes** (G5, provider side) |
| Another session inherits the secret uncontrollably | **yes** (G7) |
| Process inheritance cannot be limited | **yes** (G6 FAIL) |
| Removal behavior: old session keeps the value | **yes** (G10) |
| New authority required | **yes** — FDP-012 not received; nothing is canonical for M1 |
| Secret must enter tool output or chat | no |
| B3 / X2 weakened; standing bypass; public exposure; Release/LIVE affected | no |

## 20. Final state

```text
STATE B — BLOCKED — TELEMETRY / LOGGING / SESSION ISOLATION
```

Concurrent findings:
- **FDP-012 not received**, so it was not canonicalized.
- G1, G3 and G10 are also credential-custody failures.

FDP-011 remains canonical. O-A remains authorized but **NOT IMPLEMENTED**. ESC-03 remains **NOT RESOLVED**, FDP-010 **NOT COMPLETE**, and FS-10 **NOT READY**.

## 21. Exact next authorized action

None that changes state. No real credential may be used (MI `§32`). Unresolved items, by kind:

| Item | Kind | Needed from |
|---|---|---|
| FDP-012 decision text | **authority** — the decision itself, for validation and canonicalization | Founder |
| G1, G3, G6, G7, G8, G10 | **provider capability** — M1 is by design environment-scoped, readable by every command, and kept by a running VM after removal | provider (a session-scoped, non-readable injection), or a different custody mechanism under separate authority |
| G4, G2 | **evidence** — Anthropic-internal tracing and telemetry handling of environment values | provider documentation |
| G5 | **evidence** — Vercel logging of the bypass header | provider documentation |

The API-credential mechanism (`§4.1`) is recorded as a fact. Whether to consider it is outside FDP-012's described scope, and is not selected or ranked here.
