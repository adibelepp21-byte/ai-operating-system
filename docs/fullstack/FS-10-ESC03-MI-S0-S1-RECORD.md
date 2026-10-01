# FS-10 — Master Instruction S0 Re-discovery and S1 ESC-03 Authority Analysis

| Field | Value |
|---|---|
| **Instruction** | Master Instruction *"AIOS FS-10 — ESC-03 Authority Resolution → Founder Decision → FDP-010 Completion → FS-10 Final Reconciliation"* (verbatim: `docs/governance/acts/MI-FS10-ESC03-FDP010-FS10-FINAL-RECONCILIATION-MASTER-INSTRUCTION.md`; sha256 `549c39eb…`; Register `§115` receipt, `§116` result) |
| **States executed** | **S0** (re-discovery) → **S1** (authority analysis) → **S2** (Founder Decision preparation) → **S3** (hard stop) |
| **States not entered** | S4–S9: their entry condition (an explicit Founder Decision) does not exist (MI `§4`, `§10`) |
| **S1 exit** | **S1-B — FOUNDER DECISION REQUIRED** |
| **§7 capability check** | **B** — mechanism selection/authorization for an already-authorized capability |
| **Package** | `decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE-COMPLETE.md` (23 elements of MI `§9`) |
| **Terminal state** | **FOUNDER DECISION REQUIRED · EXECUTION PAUSED · NO IMPLEMENTATION AUTHORIZED** |
| **Release / LIVE** | **PRODUCTION RELEASE = NOT AUTHORIZED · LIVE = NOT ACTIVE** |
| **Date** | 2026-10-01 |

Evidence classes: [CAN] canonical · [DV] directly verified · [PD] provider-documented · [IO] implementation-observed · [TE] test evidence · [UNK] unknown · [INF] inferred.

## 1. S0 — sources inspected

| Source | State found | Check |
|---|---|---|
| `FDP-009` | CANONICAL, Register `§107` | content sha256 `33fecb97…` found in the Register [DV] |
| `FDP-010` | CANONICAL, Register `§109`; execution `§110` | sha256 `fa1d8b12…` found in the Register [DV] |
| ESC-03 Authority Resolution Act | Register `§111` receipt, `§112` result | sha256 `b09e56ed…` [DV]; record `FS-10-ESC-03-AUTHORITY-RESOLUTION.md` |
| `AD-FS10-ESC03` | Register `§113` receipt, `§114` result: ARCHITECTURE CONSTRAINED — NO AUTHORIZED MECHANISM; E-A–E-F UNSELECTED | sha256 `d10a16af…` [DV]; record `FS-10-ESC03-ARCHITECTURE-DECISION.md` |
| This Master Instruction | Register `§115` | sha256 `549c39eb…`; the persisted fence is byte-equal to the received text [DV] |
| FS-10 Current Authority | `FS-10-CURRENT-AUTHORITY.md` / `.json`; ESC-03 NOT RESOLVED | tests `test_current_authority.py` [TE] |
| FS-10 Deployment / Release Package | `FS-10-DEPLOYMENT.md`; `FS-10-RELEASE-PACKAGE.md` `§1`–`§20` | consistent with the above [DV] |
| X2 canonical authority | FS-DP-03 `R2.5`, `R2.6`, `R2.10`; ACT-004 `§8`; `FDP-009-02` `§5.5`; `FDP-009` `§8`; `FDP-009-03`; `FDP-010` `§4.2` | no conflict between them (ADR `§1`) [CAN] |
| B3 | `fullstack/backend/security.py`; bearer → SHA-256 lookup in `AIOS_OPERATOR_TOKENS`; scopes from `security.SCOPES` | tests [TE] |
| Historical FS-09 gate | `fullstack/readiness.py` | byte-identical to `de47057` [DV] |
| Git | branch `claude/aios-activation-authority-discovery-enq7bk`; HEAD `e46e3e7` before this work; only the MI file and Register `§115` uncommitted at S0 | [DV] |

## 2. S0 — fresh Production evidence (read-only, 2026-10-01)

| Item | Observation | Class |
|---|---|---|
| Project `aios-platform` | `ssoProtection` enabled, `all_except_custom_domains`; `passwordProtection` off; `trustedIps` off, no addresses; `live: false`; `updatedAt` `1790837188645` (unchanged since FDP-010 execution) | [DV] |
| Protection bypass / share links | none configured (no bypass entry in the project; share links revoked earlier, `§112`) | [DV] |
| Production environment variables | `AIOS_OPERATOR_TOKENS` (comment: FDP-010-01 `aios-operator`, hash only) and `SUPABASE_SECRET_KEY`; both `sensitive`, not decrypted | [DV] |
| Preview environment variables | separate `AIOS_OPERATOR_TOKENS` and `SUPABASE_SECRET_KEY` | [DV] |
| Production deployments | serving `dpl_s8c6m…` (`d05261c`, READY, rollback candidate) · designated rollback target `dpl_76CYC…` (`d05261c`, READY, rollback candidate) · `dpl_CHV72…`, `dpl_Dfs1…`, `dpl_A5Qs…` (`22c0b49`) **not** rollback candidates | [DV] |
| Latest project deployment | `dpl_2ygAT…`, target *preview* (the branch push of `e46e3e7`); not Production | [DV] |
| Production store (`hmljfyqycxcueulhsjae`) | `public.aios_records` = 118 rows (unchanged) | [DV] |
| Edge, 11:18:48Z | `GET /api/v1/health` on the Production alias and on `dpl_s8c6m…`: **302** without credentials; **302** with the `aios-operator` bearer and no X2 credential | [DV] |

The token was read from its private file (mode `600`) inside the request; its value was not printed, logged or stored.

## 3. S0 — current-state map

| Class | Items |
|---|---|
| **Canonical** | Constitution and governance baseline (unchanged); `FDP-009`; `FDP-010` (`-01`…`-04`); X2 (FS-DP-03 `R2.*`); B3 (FS-DP-02); Register `§1`–`§115` |
| **Historical** | the closed FS-09 readiness gate (`fullstack/readiness.py`, byte-identical to `de47057`) and its *"Founder-only"* rollback wording; FS-09 runbook `§9` *History* row; FS-09 readiness program row 8; earlier `FS-10-DEPLOYMENT.md` heads (kept under *History*); the temporary FDP-009-03 verification access (created, used, revoked) |
| **Current** | `FS-10-CURRENT-AUTHORITY.md`/`.json` (successor layer, `FDP-010-03`); `FS-10-DEPLOYMENT.md` head; runbook `§9` current row and `§15`; Release Package `§18`–`§20` |
| **Implementation** | served commit `d05261c` (B3, three-scope operator, read-only `docs.read` tool, no release/LIVE route); `smoke.py` (reads a bypass from a file when one is supplied; holds none) |
| **Verified** | ESC-01: `aios-operator` exists, hash-only, three scopes, `agent.register` refused (403), Preview↔Production refusals (401) — FDP-010 evidence; ESC-02: designated target `dpl_76CYC…` verified, invalid targets excluded; X2 intact (this S0); store unchanged (this S0) |
| **Unresolved** | **ESC-03** — no authorized mechanism carries `aios-operator` through X2; Production API usable by nobody today |
| **Founder-reserved** | Production Release; LIVE; Final System Acceptance; Founder Release Authorization; X2 settings (`R2.5`); admission mechanisms (`R2.10`); provider identities and credentials (`FDP-010` `§4.2`) |
| **Architect-reserved** | deployment-protection architecture changes (`FDP-009-02` `§5.5`); Production access architecture redesign (`FDP-009` `§8`). With `FD-2` open, the Founder holds the Architect role |
| **CEO-authorized** | Production deployment and verification (`FDP-009-01`, `§8`); operational capability: observe, operate, procedures, incident response, bounded rollback, recovery, credential rotation, configuration, evidence, current docs (`FDP-010` `§13`) |

### 3.1 Starting assertions of MI `§3` against re-discovery

| Assertion | Re-discovered |
|---|---|
| ESC-01 = RESOLVED | **confirmed** (`FDP-010-01`; principal present in Production, hash only) |
| ESC-02 = RESOLVED WITH BOUNDARY | **confirmed** (`FDP-010-02`; designated target READY and a rollback candidate) |
| FDP-009 = CANONICAL; FDP-010 = FOUNDER DECIDED / CANONICAL | **confirmed** (hashes in the Register) |
| B3 = ESTABLISHED | **confirmed** (served code; tests) |
| X2 = PRESERVED | **confirmed** (SSO on; 302 at 11:18Z) |
| ESC-03 = UNRESOLVED | **confirmed** |
| Production Operational API Usability = BLOCKED BY ESC-03 | **confirmed** (302 with the operator bearer) |
| Production Release = NOT AUTHORIZED; LIVE = NOT ACTIVE | **confirmed** (`live: false`; no Founder Release Authorization in the Register) |

### 3.2 S0 exit

**CURRENT STATE VERIFIED** + **NO UNRESOLVED PRECEDENCE CONFLICT.** The X2 sources narrow one another explicitly (later Founder decisions over ACT-004's delegation); no two sources conflict without a precedence rule (ADR `§1`). → **S1**.

## 4. S1 — candidate classification (MI `§6`)

Nothing below ranks or selects a candidate. Fields are the ten MI `§6` classes.

| Field | E-A per-session bypass | E-B standing bypass | E-C Trusted Sources OIDC | E-D Vercel identity | E-E runtime inside boundary | E-F no new mechanism |
|---|---|---|---|---|---|---|
| **Canonical authority** | `FDP-009-03`: temporary access for verification only; not for operation | none authorizes it; `FDP-009-02` `§5.5`: FDP-009 creates no permanent bypass | `R2.5` Founder-held settings; `§5.5` architecture path | `FDP-010` `§4.2` provider identities are account-holder controls | `FDP-009` `§8` no CEO redesign of Production access architecture | `FDP-010` `§13` (control plane operations); no change |
| **Direct evidence** | created, used, revoked under FDP-009-03; revocation verified (302 after) | none (never created) | no OIDC issuer token present in the CEO environment | team has one member | no in-boundary runtime exists | deploy, rollback, config, logs, metrics, read-only store executable; health checks, post-rollback verification, workflow runs **not** executable by the CEO |
| **Provider evidence** | Protection Bypass for Automation exists; revoked by API call; no automatic expiry found | same mechanism, long-lived | Trusted Sources accepts `x-vercel-trusted-oidc-idp-token` from listed issuers (GitHub Actions, GitLab, Vercel functions) | members / user-scoped access admitted by Vercel Authentication | crons send `Authorization: Bearer CRON_SECRET` | — |
| **Implementation evidence** | `smoke.py` reads a bypass from a file; carries none | same carrier possible; none present | no AIOS change needed; B3 unchanged | no AIOS change | cron header collides with the B3 header; in-process call would sidestep B3 or relocate the token | none |
| **Test evidence** | NC-03 test: `smoke.py` is the only carrier; `vercel.json` has no protection keys | same | — | — | — | `test_esc03_boundaries.py` (12) |
| **Unknown** | automatic expiry | — | plan entitlement; project support; X2 acceptance; an issuer usable by the CEO environment | plan / seats; whether the CEO environment can hold a Vercel session | whether cron invocations pass X2 | who runs workflows once LIVE |
| **Authority required** | Founder (extends `FDP-009-03` from verification to operation); Architect path [INF] | Founder (`R2.5`, `R2.10`) + Architect (`§5.5`) | Founder (`R2.5`) + Architect (`§5.5`); plus an external issuer runtime | Founder (`§4.2`) | Architect (`FDP-009` `§8`); Founder for credential custody [INF] | none |
| **Security implication** | per-session secret transits tool calls; fails closed when revoked | long-lived secret admits any holder to the edge (B3 still required) | no shared secret; trusts an external issuer | provider login credential in the CEO session | new operational surface; credential in the function environment or B3 sidestep | none added; CEO API access absent |
| **Release / LIVE implication** | **none** (G10 = NO) | **none** | **none** | **none** | **none** | **none** |
| **Implementation requirement** | create → use → revoke → verify → evidence, each session | create once; rotation; revocation; leak response | provider config + issuer runtime + trust config | Founder adds identity in the dashboard; login custody | new code, cron/trigger, credential placement; Architect record | documentation only |

## 5. S1 — capability authority check (MI `§7`)

**Answer: B — selection/authorization of a mechanism implementing an already-authorized capability.** Established by canonical text, not assumed:

| Element | Source | Text | Conclusion |
|---|---|---|---|
| Capability | `FDP-010` `§4.1` | *"Permanent Production operational access is authorized as an **operational capability**, not as Release or LIVE authority."* — model: *Production Access Control → Delegated Operational Access → CEO / AIOS Operational Scope* | the capability is **authorized** [CAN] |
| Capability (content) | `FDP-010` `§13` | the CEO may *"observe Production; operate Production; execute authorized operational procedures; … perform authorized rollback; perform recovery …"* | its content is **defined** [CAN] |
| Principal | `FDP-010-01` `§4.3`; Register `§110` | `aios-operator`, three scopes | **implemented and verified** [DV] |
| Mechanism at the edge | FS-DP-03 `R2.5`, `R2.10` | X2 admits *"a Vercel login or a Founder-authorized, revocable mechanism"*; settings Founder-held | **not authorized for the CEO** [CAN] |
| Mechanism (architecture) | `FDP-009-02` `§5.5`; `FDP-009` `§8` | protection changes via the architecture path; no CEO redesign | **Architect authority (Founder, `FD-2` open)** [CAN] |
| Existing temporary mechanism | `FDP-009-03` | temporary access for verification only | **does not reach operation** [CAN] |
| Provider controls | `FDP-010` `§4.2` | provider credentials and security controls remain account-holder controls | E-D needs the account holder [CAN] |

FDP-010 does not name X2, a bypass or an admission mechanism. Reading the `§4.1` capability as authorizing a specific mechanism would manufacture a capability authority from an implementation requirement (MI `§7`). It is therefore **not A** (the capability needs no new authorization) and **not C**.

## 6. S1 exit

| Exit | Applies? | Reason |
|---|---|---|
| S1-A existing authorized mechanism | **no** | the only mechanism ever authorized (`FDP-009-03`) is verification-only |
| **S1-B Founder decision required** | **yes** | the mechanism needs Founder authority (`R2.5`, `R2.10`, `§4.2`); its architecture component is held by the Founder as Architect (`FD-2` open), so one Founder instrument can carry both |
| S1-C Architect decision required | no (subsumed) | the Architect component is not separable from Founder-held settings; Founder authority is required in every candidate that grants CEO API access |
| S1-D insufficient / conflicting evidence | **no** | the evidence establishes the **authority** question; the open UNKNOWNs (E-C, E-D, E-E) concern provider feasibility, and are disclosed in the package |

→ **S2** (package: `decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE-COMPLETE.md`) → **S3 hard stop.**

## 7. S3 — hard stop

```text
FOUNDER DECISION REQUIRED
EXECUTION PAUSED
NO IMPLEMENTATION AUTHORIZED
```

Not done, and not to be done before an explicit Founder Decision (MI `§10`): selecting, implementing, configuring or canonicalizing an option; treating silence, conversation, technical necessity, a remaining candidate or "no objection" as approval.
