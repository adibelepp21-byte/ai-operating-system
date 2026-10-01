# FS-10 — FDP-011 T5 Secret-Custody Feasibility Verification

| Field | Value |
|---|---|
| **Instruction** | *"AIOS FS-10 — FDP-011 T5 Secret-Custody Feasibility Verification"* (verbatim: `docs/governance/acts/MI-FS10-FDP011-T5-SECRET-CUSTODY-FEASIBILITY-VERIFICATION.md`; sha256 `c5754210…`; Register `§119`) |
| **Final state** | **C. NO EXISTING AUTHORIZED SECRET-HANDLING PATH** |
| **O-A** | authorized (`FDP-011`, Register `§117`), **NOT IMPLEMENTED** |
| **ESC-03 / FDP-010 / FS-10** | NOT RESOLVED / NOT COMPLETE / NOT READY |
| **Release / LIVE** | **RELEASE NOT AUTHORIZED · LIVE NOT ACTIVE** |
| **Date** | 2026-10-01 |

During this verification no bypass was created, obtained or revoked. No secret was generated, set, transmitted, printed, logged or persisted. `FDP-011`, X2 and B3 were not changed. The one check that touched an existing platform secret compared it in-process and printed only `True`/`False` (`§9`).

Evidence classes: [CAN] canonical · [DV] directly verified · [PD] provider-documented · [INF] inferred · [UNK] unknown.

## 1. Scope

Can an **existing** secret-handling path carry a Protection Bypass for Automation value from its creation to the CEO's execution environment, for one operating session, and then to its revocation, in a way that satisfies `FDP-011` T5 and `FDP-010` `§11.4` without modifying either? A separate question (`§11`) asks whether B3 already provides a method for creating and holding the Founder's P-2 credential.

## 2. Canonical constraints

| Source | Constraint |
|---|---|
| `FDP-011` T5 | created through the provider control plane **by the authorized account holder**; never committed, in source, documentation, evidence, logs, chat or **normal tool output**; **not retained after the session**; custody within **an authorized secure execution/secret-handling path**; the value never in decision records, Register entries, execution records or evidence; tool-output transmission only if `FDP-010` `§11.4` explicitly permits it |
| `FDP-011` T4, T6, T7 | per session; rotate every session; revoke at session end and on triggers; **independent verification** of revocation (302) |
| `FDP-011` constraint 10 | behaviour not established by evidence is verified first, not inferred |
| `FDP-010` `§11.4` | no plaintext token in repository, documentation, evidence, logs or chat |
| `FDP-010` `§4.2` | provider credentials stay account-holder controls; no provider secret pasted into a conversational channel |
| Vercel connector rule | never decrypt environment values (connector instruction; runbook `§15`) |

## 3. Provider facts (preserved, not re-tested)

| Fact | Class |
|---|---|
| Bypass creation through the connector returns the value (`protectionBypass` is keyed by the secret); `generate.secret` lets the caller supply it, which puts it in tool input | [DV earlier; PD] |
| Revocation requires the value (`revoke.secret`, required) | [PD] |
| No automatic expiry is documented for automation bypasses (only shareable links take a `ttl`) | [PD] |
| `FDP-011` makes explicit revocation and verification mandatory; a standing bypass is not authorized | [CAN] |
| Vercel can expose a bypass inside deployments as `VERCEL_AUTOMATION_BYPASS_SECRET` (`update.isEnvVar`) | [PD] |

## 4. Existing secret-handling mechanisms investigated

| # | Mechanism | Exists here? |
|---|---|---|
| M1 | Cloud-environment variable (environment settings, *"Edit"*) | yes — documented for this environment type [DV: environment documentation] |
| M2 | Session-scoped secret injection (one session only) | **not found**: the `create_session` tool has no variable parameter [DV: tool schema]; no session-level secret is documented [UNK] |
| M3 | Platform credential injection at the egress proxy (as used for the platform's own credentials) | for the platform's own credentials only [INF]; no user-configurable form documented [DV: `/root/.ccr/README.md`] |
| M4 | Private file in the execution environment (runbook `§15` custody, mode `600`) | yes, for values **generated inside** the environment |
| M5 | Vercel connector create / revoke | yes — excluded by `FDP-011` T5 (Register `§118`) |
| M6 | Vercel deployment variable `VERCEL_AUTOMATION_BYPASS_SECRET` | yes, inside deployments only |
| M7 | Vercel dashboard, by the account holder | yes |
| M8 | GitHub Actions repository secrets | the repository has **no** `.github/workflows` [DV] |
| M9 | Supabase store / vault | yes (database) |
| M10 | Chat / conversational channel | — |
| M11 | Another canonical AIOS secret path | B3 issuance (`operator-token`) exists for **B3 tokens** only [CAN: runbook `§2`]; none for provider secrets |

## 5. Evidence for each mechanism (A–H)

| # | A Creation | B Custody (plaintext) | C Delivery to the execution environment | D Visibility | E Lifetime | F Destruction | G Access isolation | H Auditability |
|---|---|---|---|---|---|---|---|---|
| M1 | Founder, in the environment settings; **no tool here can set it** [DV: toolset — `list_environments` is read-only] | claude.ai environment configuration (server side) and the container's process environment | injected into the process environment of a **new** session; a running session does not receive it [DV: documentation *"A new session picks it up"*] | tool output, terminal, chat, transcript: **only if a command prints it**. Logs: injected values not found in the transcript or ~290 diagnostic logs (`§9`) [DV]. Telemetry: a telemetry socket exists; content **not inspectable** [UNK]. Who can view the stored value in the settings UI: [UNK] | **environment-scoped**: persists across sessions until removed [INF from documentation] | the Founder removes it in settings; the container's copy ends when the container is reclaimed | **every** session started in this environment (`env_01X4j1qVyxMRoTsGvotFpwue`, *"MoriartyContent plan"*) while it is set receives it, including Routine-fired sessions; inside a container every process inherits it [DV: environment model; INF] | yes — AIOS audit records the B3 subject; Vercel logs the request; the value is not needed |
| M2 | — | — | none found | — | — | — | — | — |
| M3 | the platform | proxy side; the container holds a 14-character placeholder for each platform credential (`GH_TOKEN`, `AWS_SECRET_ACCESS_KEY`, `CLOUDSDK_AUTH_ACCESS_TOKEN`) [DV: lengths only] [INF: proxy-side injection] | added at the proxy, never in the container [INF] | value never in the container [INF] | platform-managed | platform-managed | platform-managed | platform-managed |
| M4 | inside the environment (e.g. `aios-operator` token, generated locally and never printed) | private file (`600`) | **none** for a value that originates at Vercel: the only routes in are M5 (tool output) or M10 (chat) | none if never printed | until deleted; the container is ephemeral | delete/shred | the container only | yes |
| M5 | CEO via connector | Vercel + tool output | tool output | **tool output and transcript** | — | revoke needs the value in tool input | — | — |
| M6 | Vercel | deployment runtime environment | reaching it from the execution environment needs a decrypting read (tool output; prohibited) | — | — | — | — | — |
| M7 | Founder (account holder) | Vercel + Founder's screen | **none** by itself | dashboard only | until revoked | Founder revokes in the dashboard | account members | Vercel audit log [PD] |
| M8 | Founder | GitHub | only to workflow runs, not to this environment | masked in Actions logs [INF] | until removed | Founder | workflow runs | Actions logs |
| M9 | anyone with store write | database | read via SQL → **tool output** | tool output | until deleted | delete | database users | yes |
| M10 | — | chat | chat | **chat** | — | — | — | — |

## 6. T5 compliance matrix

✓ satisfied · ✗ violated · △ only with a boundary or Founder action · ? unknown

| T5 clause | M1 | M3 | M4 | M5 | M6 | M7 | M8 | M9 | M10 |
|---|---|---|---|---|---|---|---|---|---|
| created through the control plane by the account holder | ✓ (M7 + M1) | n/a | ✗ (origin is Vercel) | ✗ (CEO creates) | ✓ | ✓ | ✓ (M7 + M8) | ✗ | — |
| not in repository / code / docs / evidence | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| not in logs | ✓ observed; telemetry ? | ✓ | ✓ | ✗ (transcript) | ✗ | ✓ | ✓ | ✗ | ✗ |
| not in chat | ✓ | ✓ | ✓ | ✗ | — | ✓ | ✓ | ✗ | ✗ |
| not in normal tool output | △ (no printing; never `-v`/tracing) | ✓ | ✓ | ✗ | ✗ | ✓ | ✓ | ✗ | — |
| not retained after the session | △ (Founder removes the variable after every session) | — | ✓ | — | ✗ | ✓ after revoke | △ | ✗ | ✗ |
| *authorized* secure path | **? — not designated by any canonical instrument** | not available | — | prohibited | prohibited | creation only | not available | — | prohibited |
| delivers to the execution environment | ✓ (new session) | ✗ (no user route) | ✗ | ✓ | ✗ | ✗ | ✗ | ✓ | ✓ |

## 7. FDP-010 `§11.4` compliance

M1 keeps the plaintext out of the repository, documentation, evidence and chat. Logs: none observed (`§9`), telemetry unknown. M5, M9 and M10 place it in the transcript (a log) or chat → **violate**. M4, M7 and M8 comply, but none of them delivers the value. M3 would comply, but has no user route.

## 8. Session lifetime analysis

T4 and T6 require the value to live for **one operating session**. M1 is **environment-scoped**, not session-scoped. One operating session would run as follows:
1. The Founder creates a bypass in the Vercel dashboard (M7).
2. The Founder sets the variable in the environment settings (M1).
3. A **new** session is started; the running session cannot receive the value.
4. The CEO operates, then verifies revocation after the Founder revokes in the dashboard (M7).
5. The Founder removes the variable (M1).

While it is set, every new session in the environment receives it (including Routine-fired ones). This session's environment has held other sessions (one more, archived, is listed). A dedicated environment would narrow that, but creating one is a configuration change outside this verification. No existing mechanism provides **session-scoped** injection (M2 not found).

## 9. Leakage analysis

| Channel | Finding |
|---|---|
| Transcript (`*.jsonl`, 138 MB) | an injected platform secret (`CLAUDE_CODE_MESSAGING_TOKEN`) was compared in-process: **not present** [DV] |
| Diagnostic logs (`/tmp/claude-code-*.diag.log`, `/tmp/environment-manager-*.diag.log`, ~290 files) | same check: **not present** [DV]. The environment-manager log records counts and lengths (`max_env_len`), not values (sample inspected with long strings masked) |
| Debug / tracing | `CLAUDE_CODE_DEBUG`, `CCR_ENABLE_TRACING`, `ENV_MANAGER_ENABLE_DIAG_LOGS` are on [DV]; what they would capture of a **new** variable: not provable without setting one [UNK] |
| Telemetry | `SBX_TELEMETRY_SOCKET` exists; content not inspectable [UNK] |
| Tool output | any command that prints the variable, a verbose HTTP client (`curl -v` prints request headers), or shell tracing (`set -x`) would expose it; avoiding this is a usage discipline, not a technical control [INF] |
| Settings UI / server-side storage | who can read a stored variable value: [UNK] |

## 10. Revocation compatibility

Revocation needs the value (`§3`). Through the connector that puts the value in tool input (M5, excluded). The only compliant revocation is **by the account holder in the dashboard** (M7). Its **independent verification** (T7) can be done by the CEO without exposure: a request with the variable's value (never printed) must return 302 after revocation. So revocation is compatible with M1 + M7 only if the account holder revokes, and the CEO verifies.

## 11. P-2 custody boundary

| Question | Finding |
|---|---|
| Existing method for creating a B3 credential | **yes, canonical** — `python -m fullstack.backend operator-token --subject <name> --scope …` *"is for the operator, on their own machine: it prints a new random token once … and the configuration entry holding only its hash … Nothing is written to disk"* (`fullstack/backend/__main__.py`; runbook `§2`: *"stored nowhere by AIOS"*) [CAN/DV] |
| Custody | the plaintext exists only on the Founder's machine; the host holds the SHA-256 only (B3) |
| What crosses to the CEO | the **entry** (`subject`, `sha256`, `scopes`), which contains no secret |
| Remaining dependencies | (a) the Founder runs the command on their own machine, with scopes `aios.observe`, `aios.workflow.run`, `aios.audit`; (b) the Production change takes effect on redeploy, and its post-deploy verification (runbook `§15`) needs an X2 path, i.e. O-A |
| Classification | **EXISTING AUTHORIZED** (creation and custody); deployment and verification **dependent on O-A** |

No Founder token was requested, received, created, stored or tested.

## 12. Classification of each mechanism

Not ranked; nothing selected.

| # | Mechanism | Classification |
|---|---|---|
| M1 | Cloud-environment variable | **REQUIRES FOUNDER DECISION** — no canonical instrument designates it as T5's *"authorized secure execution/secret-handling path"*; it is environment-scoped, not session-scoped; it needs Founder actions in every session (create, set, revoke, remove); and telemetry and settings visibility are UNKNOWN |
| M2 | Session-scoped secret injection | **INSUFFICIENT EVIDENCE** — no such mechanism found |
| M3 | Proxy-side credential injection | **PROVIDER DEPENDENCY** — platform-managed; no user-configurable route documented |
| M4 | Private file in the environment | **INCOMPATIBLE WITH FDP-011 T5** as a delivery path (no compliant way in); valid custody for locally generated B3 tokens |
| M5 | Connector create / revoke | **PROHIBITED** (`FDP-011` T5; Register `§118`) |
| M6 | `VERCEL_AUTOMATION_BYPASS_SECRET` in deployments | **INCOMPATIBLE WITH FDP-011 T5** (reaching it needs a decrypting read into tool output) |
| M7 | Vercel dashboard (account holder) | **AUTHORIZED WITH BOUNDARY** — T5's creation and revocation path; delivers nothing to the execution environment |
| M8 | GitHub Actions secrets | **REQUIRES ARCHITECT DECISION** — would move the operating session into another runtime; none exists (`FDP-009` `§8`) |
| M9 | Supabase store / vault | **INCOMPATIBLE WITH FDP-011 T5** (read via tool output) |
| M10 | Chat | **PROHIBITED** (`FDP-010` `§4.2`, `§11.4`; T5) |
| M11 | Other canonical AIOS path | none for provider secrets; B3 issuance is **EXISTING AUTHORIZED** for B3 tokens only |

## 13. Final state

```text
C. NO EXISTING AUTHORIZED SECRET-HANDLING PATH
```

No path is proven to satisfy, at once, FDP-011 T5, `FDP-010` `§11.4`, session isolation, non-disclosure, controlled lifetime and revocation compatibility (MI `§7`).
- M7 is the T5 creation and revocation path, but delivers nothing.
- M1 delivers, but is not designated as authorized, is environment-scoped rather than session-scoped, and has open UNKNOWNs (telemetry, settings visibility).
- Every other delivery route is prohibited or incompatible.

**O-A remains authorized but NOT IMPLEMENTED. ESC-03 NOT RESOLVED. FDP-010 NOT COMPLETE. FS-10 NOT READY.**

## 14. Exact remaining blocker

| # | Unresolved | Kind | Holder |
|---|---|---|---|
| B-1 | No canonical instrument designates a delivery path as T5's *"authorized secure execution/secret-handling path"* for the bypass value | **authority** | Founder |
| B-2 | No existing mechanism injects a secret for **one session only**; the available one (M1) is environment-scoped | **provider dependency** (platform) or acceptance of environment scope (authority) | platform / Founder |
| B-3 | Telemetry content and settings-UI visibility of an environment variable are not verifiable without setting a secret | **evidence** (provider side) | platform / Founder (can view own settings) |
| B-4 | Every operating session needs account-holder actions: create and revoke in the dashboard; set and remove the variable; start a new session | **operational dependency** on the Founder | Founder |
| B-5 | P-2 deployment and verification depend on O-A | **dependency** | — |

## 15. Next authorized action

None that changes state. Within current authority:
- keep O-A unimplemented and ESC-03 open;
- keep X2, B3 and Production unchanged;
- keep the Release and LIVE firewall.

This record states the unresolved items (`§14`) without proposing a Founder Decision (instruction `§7`). P-2 credential creation, when it proceeds, has an existing canonical method (`§11`).
