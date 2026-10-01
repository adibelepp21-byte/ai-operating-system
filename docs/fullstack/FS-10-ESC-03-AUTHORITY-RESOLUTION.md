# FS-10 — ESC-03 Authority Resolution Record

| Field | Value |
|---|---|
| **Act** | `ACT-CC-POST-P13-AIOS-FS10-ESC03` (verbatim: `docs/governance/acts/ACT-CC-POST-P13-AIOS-FS10-ESC03-X2-OPERATIONAL-ACCESS-AUTHORITY-RESOLUTION.md`; Register `§111` receipt, `§112` result) |
| **Date** | 2026-10-01 |
| **Result** | **ESC-03 = NOT RESOLVED — AUTHORITY REQUIRES DECISION.** Required next action: **ARCHITECT DECISION REQUIRED** (`§11`). Package: `decision-packages/FS-DP-03-R3-ESC-03-OPERATIONAL-EDGE-ACCESS.md` |
| **Implemented** | nothing that changes access. One incident-response action: the revocation of an X2 share link the connector had created (`§5.3`, SEC-OBS-02). Code-level negative controls added as tests (`§8.2`) |
| **Release / LIVE** | **PRODUCTION RELEASE = FOUNDER RESERVED · LIVE = FOUNDER RESERVED** (Act `§27`) |

Facts are observed or quoted unless marked **[INF]** (inference). **UNKNOWN** means the evidence does not establish the answer.

## 1. Question

> *"Bagaimana delegated CEO memperoleh operational access ke protected Production AIOS API melalui X2 tanpa menciptakan permanent bypass dan tanpa memperoleh Production Release / LIVE authority?"* (Act header)

That is: how the delegated CEO obtains operational access to the protected Production AIOS API through X2, without a permanent bypass and without Production Release or LIVE authority.

## 2. Canonical sources inspected

| Source | What it says on this question |
|---|---|
| `FD-FS-001` D2-A; Architecture Freeze `§10` | networking is **Architect-reserved** (cited by FS-DP-03 `R2.3`) |
| `FS-DP-03` Networking, revision 2 (`decision-packages/FS-DP-03-NETWORKING.md`) | defines **X2**: *"deployment protection on every deployment, Production included (the console is for operators only; B3 issues tokens only to operators)"* (`R2.6`); `R2.5`: *"The **Founder** holds the project settings that implement edge access (deployment protection is a Founder-held configuration in this program)"*; `R2.10`: *"X1/X2: each live check needs a Vercel login or a Founder-authorized, revocable mechanism (as at FS-08). An external uptime check (`FS-DP-06`) cannot pass X2 without one."*; `R2.3`: NC-04 *"Vercel protection is never bypassed except by an authorized mechanism"*; `R2.11` item 6: the live setting must match the decision |
| ACT-004 `§8` (Register `§93`, `ACT-004-DG-01`) | the Founder as Architect ratified **N1**; *"Where the package identifies implementation sub-options such as X1/X2, Claude is authorized to select the implementation form … provided it does not alter the architectural meaning of N1"*; *"Claude may not redefine N1"*. Register `§93`: *"Implementation form selected (`§8` delegation): edge access **X2**"* |
| ACT-004 `§56` | *"Temporary access mechanisms may be used only when legitimately authorized and must be revoked afterward."* |
| ACT-003 `§12` | *"Claude shall not: bypass Vercel access controls; circumvent SSO; use unauthorized credentials; infer access from previous access"* |
| ACT-003 `§14` | *"Authorized access may be established through: reconnected Vercel connector OR Founder-created authorized protection/access configuration … No protection bypass may be invented or executed without authorization."* |
| ACT-008 (`FS-09` closure Act) | the CEO may not *"create standing unrestricted security bypasses"* (spent Act; cited as the most recent statement of that boundary, not as live authority) |
| `FDP-009-02` `§5.5` (Register `§107`) | *"The existing X2 deployment-protection architecture remains unchanged. This Founder Decision does NOT: remove deployment protection; weaken deployment protection; create permanent bypass access; redesign the authentication architecture; create public access … **Any future architectural modification to deployment protection must use the appropriate architecture authority path.**"* `§5.6`: DEPLOYED ≠ PUBLIC ≠ RELEASED |
| `FDP-009` `§8` | CEO may not *"permanently disable deployment protection; redesign the Production access architecture"* |
| `FDP-009-03` | temporary access past X2 **for verification only**, under 14 conditions |
| `FDP-010-01` (Register `§109`) | a permanent AIOS operational principal for the CEO, least privilege, revocable, auditable; operational access ≠ release ≠ LIVE (`§4.6`, `§14`); `§4.2`: provider credentials and controls *"remain external/account-holder controls"*, never pasted into a conversation |
| `FS-DP-02` B3, Architect decision (Register `§81`) | operator bearer tokens verified against hashes. It **rejected B4** *"Vercel Authentication as the only gate"*: *"the function learns no identity, so there is no subject for audit and no scopes"* |
| `FS-10-CURRENT-AUTHORITY.md` / `.json` (Register `§110`) | operational access and rollback CEO-with-boundary; Release, LIVE, Final System Acceptance Founder-reserved |
| Runbook `§12.1`, `§15`; ownership `§6` | H3 manual checks; the CEO has no standing X2 path |
| Co-Founder V2: F04 `§26`; F06 A05, A22, A23 | A05 bounded architecture authority *"Escalate if architecture change would … override protected canonical authority"*; A22 self-expansion prohibited; A23 canonical override prohibited; F04 `§26` item 10: decisions designated Founder-only by Founder Decision are not delegated |
| Search terms (Act `§4`) | *machine identity, service principal, service-to-service, non-human*: **no canonical source uses them** for Full Stack access (corpus search; only this Act). *PD-08*: no Platform-Organization volume governs Full Stack edge access [the Full Stack decisions above are the governing chain] |
| Provider documentation (read-only, `search_vercel_documentation`) | Vercel offers, for protected deployments: Protection Bypass for Automation (`x-vercel-protection-bypass`), shareable links and **user-scoped** bypass (`/aliases/{id}/protection-bypass`, *"If [ttl is] not provided, the shareable link will never expire"*), **Trusted Sources** (`x-vercel-trusted-oidc-idp-token`, an OIDC token from a trusted issuer such as GitHub Actions or a Vercel function), Trusted IPs (`protectionMode: additional`), and `vercel curl` (*"automatic protection bypass"* for an authenticated CLI) |

## 3. X2 authority

| Element | Authority |
|---|---|
| Rule set N1 | Founder as Architect (ACT-004 `§8`) |
| Form X2 | selected by the CEO under the ACT-004 `§8` delegation (Register `§93`); **frozen since by `FDP-009-02` `§5.5`**: unchanged, and any future architectural modification of deployment protection goes through the architecture authority path |
| The project settings implementing it | Founder-held configuration (FS-DP-03 `R2.5`) |
| Who passes X2 | *"a Vercel login or a Founder-authorized, revocable mechanism"* (`R2.10`) |
| Temporary mechanism | Founder-authorized for **verification** only (`FDP-009-03`) |
| Permanent bypass | not created by any decision; excluded from what `FDP-009` grants (`§5.5`); the CEO may not create one (ACT-003 `§12`, `§14`) |

The sources are **consistent**: the CEO's ACT-004 delegation chose X2; a later Founder decision (`FDP-009`) froze it and routed any change to the architecture authority path. No contradiction was found (Act `§23`).

## 4. Current operational access of `aios-operator`

| Can | Evidence |
|---|---|
| authenticate at the **application** with exactly `aios.observe`, `aios.workflow.run`, `aios.audit` | FDP-010 evidence: session → subject `aios-operator`, three scopes |
| be refused registration (403), on Preview (401), on superseded deployments (401) | same evidence |

| Cannot | Evidence |
|---|---|
| pass X2: a request carrying the token but no X2 credential gets **302** (plain) / **401** (JSON, from the platform) | FDP-010 evidence (`token without bypass`) and Register `§108` |
| be used by the CEO for routine operation today: the CEO holds no Vercel login session it can attach headers to, and no authorized X2 mechanism exists for operation | `§5`, `§7` |

What the CEO **can** do without passing X2: the provider control plane through the connector (deploy, roll back, read configuration and logs, M1 metrics) and read-only store access (backups, runbook `§7`). Neither is API access.

## 5. Connector limitation (Act `§13`)

| Kind | Exists? | Evidence |
|---|---|---|
| **Connector capability limitation** | **yes** | `web_fetch_vercel_url` takes only a URL (no header parameter), and on an SSO-protected deployment returns the SSO **302** instead of completing the flow (06:47 UTC probes) |
| Provider control-plane limitation | **no** for the existence of mechanisms (`§2`, provider documentation); **UNKNOWN** for plan entitlement of Trusted Sources and Trusted IPs | provider docs do not state the plans in what was retrieved |
| Current configuration limitation | **yes**: no admission mechanism for a non-human caller is configured (bypass list empty; no trusted source or trusted IP observed: `trustedIps.enabled: false`; trusted-source configuration not exposed by `get_project`: **UNKNOWN**, none created by this program) | `get_project`; revocation responses |
| AIOS architecture limitation | **no**: B3 authenticates the principal once a request reaches the function (proved under FDP-009-03 access) | Register `§108`, `§110` |

### 5.3 SEC-OBS-02 re-examined (Act `§15`)

| Question | Answer |
|---|---|
| What happened | each `web_fetch_vercel_url` call on an SSO-protected deployment created a **deployment shareable link** and returned it inside the 302 `Location` (*`_vercel_share=`*). A transcript scan shows this on **six** deployments: the Production serving deployment today (2 values) and five Preview deployments on 2026-09-27 and 2026-09-30 (12 values), the earlier ones unrecorded at the time. The two explicit `get_access_to_vercel_url` calls (2026-09-27) failed (*"Vercel denied access"*) and created none |
| 1. Still active? | **No, for every value known.** Production `dpl_s8c6m…`: the latest value **revoked** (`patch_url_protection_bypass` → `{"protectionBypass":{}}`); the earlier one *"does not exist"* (superseded). The five Preview deployments: the latest value of each → *"The specified shareable link does not exist"* (404) |
| 2. Expires automatically? | **UNKNOWN for `web_fetch`.** The connector documents 23 h for `get_access_to_vercel_url`; the API's default is *never*. The 404s on links 1–4 days old are consistent with expiry or supersession; not proven which |
| 3. Accessible to external parties? | the values sat in this session's tool output (the session transcript) and nowhere else: not in the repository (scan), evidence, logs or messages to the Founder. A holder could have passed X2 on that deployment while the link lived |
| 4. Changes X2? | no: the protection setting was unchanged; a share link is a per-deployment exception for its holder |
| 5. Bypasses application authentication? | **no**: every protected route still requires a B3 bearer token; only `/health` and the static console would have been reachable |
| 6. Stored anywhere? | the session transcript only; the scratch copy used to revoke was destroyed |
| 7. Provider-side invalidation required? | done for the only link that existed; none other exists. **Correction:** Register `§110` and Release Package `§18.4` said the connector offers no revocation; it does, at the deployment level (`patch_url_protection_bypass`); its alias-level call is refused to the connector (401) |
| 8. Release readiness? | **not affected** |
| Prevention | `web_fetch_vercel_url` is **not to be used on SSO-protected deployments** (runbook `§15`); it creates an X2 exception as a side effect |

## 6. Access mechanism matrix (Act `§5`)

| # | Access mechanism | Canonical authority | Current state | Allowed (for CEO routine operation)? | Owner | Requires decision? |
|---|---|---|---|---|---|---|
| M1 | **Vercel SSO login** (human member of the account) | FS-DP-03 `R2.10` (*"a Vercel login"*); X2 | works for members; the CEO has no Vercel login session it can use with headers | yes for members; **not available to the CEO** | account holder | no (for members) |
| M2 | **Operator bearer token** (`aios-operator`) | FS-DP-02 B3 (`§81`); `FDP-010-01` | configured, verified at the application layer | yes, **after** X2 | CEO (custody), Architect (B3) | no |
| M3 | **Temporary verification bypass** | `FDP-009-03` | none active; on Production used and revoked twice under it (Register `§108`, `§110`) | **verification only** | Founder (authorized it) / CEO (operates it) | yes, for any use beyond verification |
| M4 | **Permanent / standing automation bypass** | `FDP-009-02` `§5.5` (none created; changes via architecture path); ACT-003 `§12`, `§14` | none | **no** | Architect path + Founder (`R2.5`, `R2.10`) | yes |
| M5 | **Per-session operational bypass** (created for an operating session, revoked after) | `FDP-009-03` limits temporary access to verification; `R2.10` admits *"a Founder-authorized, revocable mechanism"* | none | **no** (not authorized for operation) | Founder | yes |
| M6 | **Shareable link** (deployment or alias, with TTL) | not named by any decision; ACT-003 `§12` | none active (`§5.3`) | **no** | Founder | yes |
| M7 | **User-scoped bypass** for a CEO identity at the provider | not named; needs a provider identity for the CEO (`FDP-010` `§4.2`: provider accounts are account-holder controls) | none; the CEO has no provider identity | **no** | Founder (account, possibly seats/spending D3-A) | yes |
| M8 | **Service-to-service / machine identity: Trusted Sources (OIDC)** | not named; a new admission rule and trust boundary on deployment protection (`FDP-009` `§5.5`) | not configured (**UNKNOWN** whether the plan offers it; **UNKNOWN** whether the CEO's execution environment can obtain an OIDC token from an issuer Vercel trusts) | **no** | Architect | yes |
| M9 | **Vercel account holder through the connector** (`web_fetch_vercel_url`) | ACT-003 `§12`, `§14` (*"reconnected Vercel connector"* is an authorized access path) | authorized path, but **cannot carry `Authorization`** and does not complete SSO; creates share links as a side effect | path authorized; **functionally insufficient**; not to be used on protected deployments | provider (connector) | no decision can fix a connector capability [INF] |
| M10 | **Account holder's CLI** (`vercel curl` with a Vercel token in the CEO's environment) | `FDP-010` `§4.2` (provider credentials stay with the account holder; never through a conversation) | no token in the environment | **no** | Founder | yes |
| M11 | **Operational runtime inside the boundary** (e.g. a scheduled function calling AIOS in-process) | none; a new component and trust boundary | none | **no** | Architect | yes |
| M12 | **X2 → X1** (Production public, B3 the only gate) | `FDP-009-02` `§5.5`–`§5.6` (X2 unchanged; no public access); FS-DP-03 `R2.16` | X2 | **no** | Architect + Founder | yes |
| M13 | **Trusted IPs** | not named | off | **UNKNOWN** as an admission path (provider docs show `protectionMode: additional`, an added requirement) | Architect / Founder (plan) | yes |
| M14 | **Direct store access** (Supabase connector) | runbook `§7` (read-only export) | read-only used | read-only **yes**; writes **no** (bypass AIOS authorization and audit) | CEO (read-only) | no |
| M15 | **Provider control plane** (deploy, rollback, logs, variables) | `FDP-009` `§8`, `FDP-010` `§13` | used | yes, but it is **not API access** | CEO with boundary | no |

## 7. Authority classification (Act `§8`) — one class each, not ranked

| # | Mechanism | Classification |
|---|---|---|
| M1 | Vercel SSO login (members) | EXISTING AUTHORIZED MECHANISM (not available to the CEO) |
| M2 | Operator bearer token | EXISTING AUTHORIZED MECHANISM (application layer only) |
| M3 | Temporary verification bypass | AUTHORIZED WITH BOUNDARY (verification only) |
| M4 | Permanent / standing automation bypass | PROHIBITED (for the CEO) |
| M5 | Per-session operational bypass | FOUNDER DECISION REQUIRED |
| M6 | Shareable link | FOUNDER DECISION REQUIRED |
| M7 | User-scoped bypass for a CEO provider identity | FOUNDER DECISION REQUIRED |
| M8 | Trusted Sources (OIDC machine identity) | ARCHITECT DECISION REQUIRED |
| M9 | Connector fetch | EXTERNAL PROVIDER DEPENDENCY |
| M10 | Account holder's CLI token in the CEO environment | FOUNDER DECISION REQUIRED |
| M11 | Operational runtime inside the boundary | ARCHITECT DECISION REQUIRED |
| M12 | X2 → X1 | CONFLICT WITH CANONICAL AUTHORITY |
| M13 | Trusted IPs | UNKNOWN |
| M14 | Direct store access | AUTHORIZED WITH BOUNDARY (read-only) |
| M15 | Provider control plane | EXISTING AUTHORIZED MECHANISM (not API access) |

**No mechanism is both authorized and sufficient for routine CEO API access.** "Technically possible" (M4–M8, M10–M13) is not "authorized" (Act `§20`).

### 7.1 Act `§7` questions

| # | Question | Answer (evidence) |
|---|---|---|
| 1 | Can the operator principal authenticate through X2? | **No.** X2 precedes the application; a bearer token alone gets 302/401 (`§4`) |
| 2 | Can X2 distinguish provider authentication from application bearer authentication? | **Yes**: two layers — Vercel Authentication at the edge, B3 in the function. B3 exists because the edge gives the function no identity (FS-DP-02 B4 rejection) |
| 3 | Does X2 support a machine/service identity? | X2 **as decided** admits *"a Vercel login or a Founder-authorized, revocable mechanism"* (`R2.10`); the **provider** offers machine mechanisms (M4–M8, M13). None is authorized for operation |
| 4 | Does X2 support an authorized non-human principal? | **Not today**: only the verification bypass (`FDP-009-03`) is authorized, and only for verification |
| 5 | Does the current architecture contain such a mechanism? | **No** (`§5`, configuration) |
| 6 | Does Vercel provide a supported mechanism within the existing X2 decision? | Vercel provides mechanisms; whether one is *within* X2 is answered by `R2.10`: only if **Founder-authorized**. None is |
| 7 | Would using it require changing X2? | M4, M8, M11, M13 add an admission rule to deployment protection → an architectural modification under `FDP-009` `§5.5` [INF on M13]. M5–M7 keep the setting but add per-holder exceptions → Founder authorization (`R2.10`). M12 changes X2 itself |
| 8 | Would it require a new security architecture decision? | M8, M11: yes (a new trust boundary / identity). M4: yes (standing exception). M5–M7, M10: a Founder authorization of a mechanism, not new architecture [INF] |
| 9 | Would it create a permanent bypass? | M4: yes. M8: a standing admission rule for an issuer (not a shared secret) [INF]. M5, M6: no if time-boxed and revoked. M7, M10: standing for an identity |
| 10 | Would it expose the application publicly? | M12: yes. Others: no, unless a secret or link leaks (M4–M6) |
| 11 | Would it change Release/LIVE semantics? | **No mechanism does** (`§9`) |

## 8. Security tests B1–B10 (Act `§9`)

✓ passes · ✗ fails · △ conditional · ? UNKNOWN

| # | Mechanism | B1 X2 kept | B2 no permanent bypass | B3 least privilege | B4 revocable | B5 auditable | B6 release separate | B7 LIVE separate | B8 not public | B9 credential safety | B10 governance |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M1 | SSO login (members) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| M2 | bearer token | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| M3 | verification bypass | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | △ secret in a tool call | ✓ verification only |
| M4 | standing bypass | △ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | △ | △ | ✗ |
| M5 | per-session bypass | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | △ | ✗ (`FDP-009-03`) |
| M6 | shareable link | ✓ | △ (TTL) | ✓ | ✓ | ✓ | ✓ | ✓ | △ (URL) | ✗ (secret in a URL) | ✗ |
| M7 | user-scoped bypass | ✓ | △ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ? | ✗ (`FDP-010` `§4.2`) |
| M8 | Trusted Sources OIDC | ✓ | △ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (short-lived tokens) | ✗ until decided |
| M9 | connector fetch | ✓ | ✓ | ✓ | ✓ | ✗ (no bearer) | ✓ | ✓ | ✓ | ✗ (share links, SEC-OBS-02) | ✓ path / ✗ function |
| M10 | CLI token | ✓ | ? | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ (provider credential in session) | ✗ |
| M11 | in-boundary runtime | ? | ? | ✓ | ? | ✓ | ✓ | ✓ | ✓ | ? | ✗ until decided |
| M12 | X2 → X1 | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ |
| M13 | Trusted IPs | ? | ? | ✓ | ✓ | ✓ | ✓ | ✓ | ? | ✓ | ✗ until decided |

### 8.2 Negative controls (Act `§22`)

| NC | Control | Result | Evidence |
|---|---|---|---|
| NC-01 | cannot authorize Production Release | **PASS** | no route or handler names release/promote/deploy; release is a Founder governance state, not an operation (`test_esc03_boundaries`) |
| NC-02 | cannot activate LIVE | **PASS** | same; Vercel `live: false` |
| NC-03 | cannot bypass X2 permanently | **PASS** | no served or operational module carries a bypass, share or trusted-source header except the smoke client, which reads a temporary one from a file; `vercel.json` sets no protection; bypass list `{}`; no share link exists (`§5.3`) |
| NC-04 | cannot modify governance | **PASS** | the operator's only write is `POST /runs`; the only Tool is read-only `docs.read` |
| NC-05 | cannot modify certified roots | **PASS** | same; the certified-write barrier stays in force |
| NC-06 | cannot access unauthorized scopes | **PASS** | scopes ⊂ canonical model; registration 403 live (FDP-010 evidence) |
| NC-07 | Preview credentials refused on Production | **PASS** | 401 live (FDP-010 evidence) |
| NC-08 | Production credentials refused on Preview | **PASS** | 401 live (FDP-010 evidence) |
| NC-09 | no agent registration without the scope | **PASS** | 403 live; route requires `aios.agent.register` (test) |
| NC-10 | no new authority through implementation | **PASS** | nothing implemented that grants access; no scope, route, identity or protection change; tests and Register |

Code-level tests: `fullstack/tests/test_esc03_boundaries.py` (9). Live NC-06–NC-09 are from the same deployment's FDP-010 verification; this Act created no bypass to repeat them (Act `§14`).

## 9. Release / LIVE separation

1. Every candidate admits requests **only to the existing application**. The application exposes no release, promotion, deployment, rollback or LIVE operation (NC-01, NC-02, tested).
2. The operator's scopes are the three operational scopes; the only write runs a governed workflow with a read-only Tool (NC-04, NC-05).
3. Release and LIVE are Founder-reserved governance states (`FDP-009` `§5.3`, `§5.4`, `§10`; `FDP-010` `§14`, `§22`), not application capabilities; no edge mechanism can create them.
4. Rollback goes through the provider control plane (M15), separate from API access and separately bounded (`FDP-010-02`).

**OPERATIONAL ACCESS ≠ PRODUCTION RELEASE ≠ LIVE · X2 ACCESS ≠ PUBLIC ACCESS · TECHNICAL CAPABILITY ≠ GOVERNANCE AUTHORITY.**

## 10. Decision owner

| Matter | Owner |
|---|---|
| Any admission mechanism added to deployment protection (M4, M8, M11, M13), or changing X2 (M12) | **Architect** — the architecture authority path named by `FDP-009-02` `§5.5`; networking is Architect-reserved (`FD-FS-001` D2-A). The Architect role is held by the Founder acting as Architect (`FD-2` open, FS-DP-03) |
| A revocable mechanism admitting a holder (M5, M6), a provider identity or credential for the CEO (M7, M10) | **Founder** (`R2.5` Founder-held settings; `R2.10` *"Founder-authorized"*; `FDP-009-03` purpose; `FDP-010` `§4.2`) |
| The connector's missing header capability (M9) | **Provider** (external) |
| Operating with what is authorized (M2, M14, M15) | CEO |

## 11. Required next action

**ARCHITECT DECISION REQUIRED.**

`FDP-009-02` `§5.5` routes *"any future architectural modification to deployment protection"* to the architecture authority path; every mechanism that would give the CEO routine API access through X2 is such a modification or (M5–M7, M10) a Founder-authorized mechanism that the Architect decision would have to place within X2 (`R2.10`). Package: `decision-packages/FS-DP-03-R3-ESC-03-OPERATIONAL-EDGE-ACCESS.md`. **Not implemented.** ESC-03 stays **NOT RESOLVED** until a decision establishes a mechanism and it is implemented and verified (Act `§25`, states B or C).

Unchanged: `FDP-009`, `FDP-010`, X2, scopes, Release and LIVE boundaries; temporary bypass **NONE**; permanent bypass **NONE**.

## Note on token custody (observed during discovery)

FS-DP-02's package (`R2.11`, *"Implementation boundary (if B3 is ratified)"*) proposed *"Tokens are generated and set by the Founder; Claude never generates, sees or stores one."* The **ratified** Architect decision (Register `§81`) binds hash-only storage and no persisted plaintext; it does not carry that sentence. `FDP-010-01` (`§109`) later placed a permanent principal with the CEO. The current CEO custody of `aios-operator` therefore conflicts with no ratified text; the difference from the package's proposal is recorded here rather than left implicit.
