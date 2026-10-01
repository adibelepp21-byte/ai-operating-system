# FS-10 — ESC-03 Founder Decision Package (complete, Master Instruction `§9`)

| Field | Value |
|---|---|
| **Prepared under** | Master Instruction FS-10 ESC-03 → FDP-010 → FS-10 (Register `§115`), state **S2**; follows `AD-FS10-ESC03` (Register `§113`–`§114`) |
| **Status** | **PREPARED — AWAITING FOUNDER.** This is a decision package, **not** a Founder Decision Record. Every candidate is **UNSELECTED**. Nothing is implemented or configured |
| **Predecessor** | `FS-10-ESC03-FOUNDER-DECISION-PACKAGE.md` (AD-FS10-ESC03 `§22`): kept unchanged as the earlier preparation; this package contains it and adds the elements MI `§9` requires |
| **S0 / S1 record** | `../FS-10-ESC03-MI-S0-S1-RECORD.md` |
| **Release / LIVE** | **unaffected by every option. PRODUCTION RELEASE = FOUNDER RESERVED · LIVE = FOUNDER RESERVED** |

Evidence classes: [CAN] canonical · [DV] directly verified · [PD] provider-documented · [IO] implementation-observed · [TE] test evidence · [UNK] unknown · [INF] inferred.

Options are listed in the fixed order E-A … E-F, as used since FS-DP-03-R3. The order carries no ranking.

---

## 1. Decision ID

**Proposed identifier: `FDP-011`** — the next unused number of the FDP series (`FDP-009` at Register `§107`, `FDP-010` at `§109`; no `FDP-011` exists in the repository). It is a proposal only: no Register number is reserved, and the Founder may issue the decision under any identifier (MI `§25`). Subject: *FS-10 ESC-03 — Production Operational Edge Access (X2 admission of the delegated CEO's operational principal).*

## 2. Context

`FDP-010-01` authorized permanent Production operational access as an operational capability and created `aios-operator`. That principal works once a request reaches the function (B3), but X2 stops every request that is neither a Vercel login nor a Founder-authorized mechanism. No mechanism is authorized for the CEO. The Founder passes X2 but holds no Production principal. **Nobody can use the Production API today.** The Master Instruction targets *"ESC-03 = RESOLVED"*, and it requires the access path to be *"genuinely usable, not merely documented"* (MI `§13`). It also forbids manufacturing the decision that path needs (MI `§1`, `§10`).

## 3. Existing canonical authority

| Source | Content | Bearing |
|---|---|---|
| `FDP-010` `§4.1` | permanent Production operational access is authorized as an operational capability | **capability: authorized** |
| `FDP-010` `§4.3`, `§13` | the operational principal; the CEO may observe and operate Production | capability content |
| `FDP-010` `§4.2` | provider credentials, accounts and security controls stay account-holder controls; no provider secret into a conversational channel | E-D; credential paths |
| `FDP-010` `§11.4` | no plaintext token in repository, documentation, evidence, logs or chat | custody of any new secret |
| FS-DP-03 `R2.5` | protection settings are Founder-held | every edge change |
| FS-DP-03 `R2.10` | X2 admits *"a Vercel login or a Founder-authorized, revocable mechanism"* | the decision's object |
| FS-DP-03 `R2.6`; ACT-004 `§8` | X2 on every deployment, Production included | X2 stays |
| `FDP-009-02` `§5.5` | protection changes via the architecture authority path; FDP-009 creates no permanent bypass | Architect component (Founder, `FD-2` open) |
| `FDP-009` `§8` | the CEO may not redesign the Production access architecture | E-E |
| `FDP-009-03` | temporary access past X2 for verification only | E-A (as it stands) |
| ACT-003 `§12` | no bypass of Vercel access controls, SSO circumvention or unauthorized credentials | all |
| MI `§30` | no permanent X2 bypass or public exposure without explicit authority | E-B; any public option |

## 4. Current verified state (2026-10-01, S0)

| Item | State | Class |
|---|---|---|
| X2 | Vercel Authentication on, `all_except_custom_domains`; no bypass, no share link, no trusted IPs | [DV] |
| Edge, 11:18:48Z | 302 without credentials; 302 with the `aios-operator` bearer (alias and serving deployment) | [DV] |
| Production serving | `dpl_s8c6m…`, `d05261c` | [DV] |
| Rollback target | `dpl_76CYC…` (designated, verified); `22c0b49` excluded | [DV] |
| Production principal | `aios-operator`, hash-only, `aios.observe` · `aios.workflow.run` · `aios.audit` | [DV] |
| Store | 118 rows | [DV] |
| ESC-01 / ESC-02 | resolved (ESC-02 with boundary) | [CAN]/[DV] |
| ESC-03 | **not resolved** | [CAN]/[DV] |
| Release / LIVE | not authorized / not active (`live: false`) | [DV] |

## 5. Evidence inventory

| Artifact | Content |
|---|---|
| `evidence/FS-10-ESC03-ARCHITECTURE-EVIDENCE.json` | 70 classified findings (common + E-A … E-F) |
| `FS-10-ESC03-ARCHITECTURE-DECISION.md` | ADR: X2 authority, limitation map, requirement matrix, S1–S10, G1–G10, decision matrix |
| `FS-10-ESC-03-AUTHORITY-RESOLUTION.md` | authority matrix M1–M15, B1–B10, NC-01–NC-10 |
| `evidence/FS-10-FDP-010-OPERATIONAL-ACCESS-ROLLBACK-2026-10-01.json` | principal creation, scope refusals, Preview↔Production refusals, rollback target verification |
| `evidence/FS-10-PRODUCTION-VERIFICATION-2026-10-01.json` | FDP-009 Production verification (temporary access, revoked) |
| `FS-10-ESC03-MI-S0-S1-RECORD.md` | this instruction's S0 fresh evidence and S1 classification |
| `fullstack/tests/test_esc03_boundaries.py`, `test_current_authority.py` | code-level negative controls and authority pins |

## 6. Directly verified facts

1. B3 authenticates `aios-operator` with exactly three scopes once a request reaches the function.
2. X2 answers 302 to the operator bearer without an X2 credential (11:18:48Z).
3. A Protection Bypass for Automation was created, used and revoked under `FDP-009-03`; after revocation the edge returned 302.
4. The CEO's environment can send arbitrary HTTP headers to Production.
5. The Vercel connector's fetch has no header parameter and stops at the SSO redirect.
6. No OIDC issuer token is present in the CEO's environment.
7. The Vercel team has one member (the Founder).
8. No in-boundary runtime (cron, scheduled function) exists.
9. Through the control plane the CEO can deploy, roll back, configure, and read logs and metrics; the store is readable read-only. The CEO cannot run `/api/v1/health`, post-rollback verification (runbook `§9`) or workflows.
10. `agent.register` is refused to `aios-operator` (403); Preview credentials are refused in Production and the reverse (401).

## 7. Provider-documented facts

1. Protection Bypass for Automation: a project secret sent as `x-vercel-protection-bypass`; created and revoked through the project's protection-bypass API.
2. Shareable and user-scoped links exist; a link can be revoked at deployment level.
3. Trusted Sources: Vercel Authentication can accept `x-vercel-trusted-oidc-idp-token` from listed issuers (GitHub Actions, GitLab, Vercel functions).
4. Team members (Vercel logins) pass Vercel Authentication.
5. Vercel crons invoke a path with `Authorization: Bearer CRON_SECRET`.
6. Trusted IPs exist as a separate protection feature.

## 8. Implementation-observed facts

1. `fullstack/deploy/smoke.py` is the only module that can send an X2 credential; it reads one from a file at run time and holds none (NC-03 test).
2. `vercel.json` sets no protection key.
3. The application exposes no release, promotion, deployment, rollback or LIVE route; the operator's only write is `start_run`; the only tool, `docs.read`, is read-only.
4. B3 reads `Authorization: Bearer`; a cron's `CRON_SECRET` bearer would arrive on the same header.

## 9. Unknowns

| Unknown | Affects | Closable how |
|---|---|---|
| automatic expiry of an automation bypass | E-A, E-B | provider documentation / support |
| plan entitlement and project support for Trusted Sources; X2 acceptance of it | E-C | only by configuring it (needs authority) |
| an OIDC issuer usable from the CEO's environment | E-C | external runtime (e.g. CI) — not present |
| plan, seats, and whether the CEO's environment can hold a Vercel session | E-D | Founder's account view |
| whether cron invocations pass X2 | E-E | only by configuring a cron (needs authority) |
| who runs workflows once LIVE | E-F; scope of all options | Founder |

## 10. Authority classification

| Question | Class |
|---|---|
| Capability (CEO operational access to Production) | **AUTHORIZED** — `FDP-010-01` `§4.1`, `§13` [CAN] |
| Mechanism carrying the principal through X2 | **FOUNDER DECISION REQUIRED** — `R2.5`, `R2.10`; `FDP-010` `§4.2` |
| Architecture component of that mechanism | **ARCHITECT** — `FDP-009-02` `§5.5`, `FDP-009` `§8`; held by the Founder (`FD-2` open) |
| MI `§7` answer | **B** (mechanism for an authorized capability) — `FS-10-ESC03-MI-S0-S1-RECORD.md` `§5` |
| Within current CEO authority | only E-F (no change) |

## 11. Candidate mechanisms

| ID | Mechanism | What passes X2 | Evidence complete |
|---|---|---|---|
| **E-A** | per-session X2 bypass | an automation-bypass secret created for one operating session, revoked at its end | yes (expiry UNKNOWN) |
| **E-B** | standing X2 bypass | a long-lived automation-bypass secret held by the CEO | yes |
| **E-C** | Trusted Sources OIDC | a short-lived token from a trusted external issuer | **no** (`§9`) |
| **E-D** | Vercel identity for the CEO | a provider login (member or user-scoped) | partly (`§9`) |
| **E-E** | runtime inside the boundary | an in-deployment scheduled or triggered caller | **no** (`§9`) |
| **E-F** | no new mechanism | nothing (CEO uses the control plane and read-only store) | yes |

All six: **UNSELECTED**.

## 12. Security implications

| | Secret / credential | Trust boundary added | Revocation | Failure mode |
|---|---|---|---|---|
| E-A | per-session secret; transits tool calls | per session | manual, per session; verified by 302 | fails closed when absent or revoked |
| E-B | long-lived secret | holders of the secret | manual; rotation duty | if leaked, edge open to holders until revoked; B3 still required |
| E-C | short-lived issuer tokens; no shared secret | the external issuer | remove issuer | fails closed on rejection [INF] |
| E-D | provider login in the CEO session (`FDP-010` `§4.2`) | a provider identity | remove member / access | fails closed without login |
| E-E | credential in the function environment, or B3 sidestepped | an in-boundary operator | remove cron/trigger | runs on schedule inside the boundary |
| E-F | none | none | n/a | CEO API access stays absent |

Every option keeps B3 and the three operator scopes.

## 13. Governance implications

| | Changes X2 | Founder-held settings touched | Architect record needed | New authority surface | Extends an existing decision |
|---|---|---|---|---|---|
| E-A | per-session exception | yes | yes [INF] | no | `FDP-009-03` (verification → operation) |
| E-B | standing exception | yes | yes | no | — (MI `§30`: needs explicit authority) |
| E-C | trusted issuer | yes | yes | no | — |
| E-D | admits an identity | provider administration | yes [INF] | no | — |
| E-E | ? (UNKNOWN) | possibly | yes | **yes** | — |
| E-F | no | no | no | no | — |

None touches the Constitution, Founder authority, governance model, certified P12/P13 roots, Native Core or Phase 14.

## 14. Operational implications

| Responsibility | E-A | E-B | E-C | E-D | E-E | E-F |
|---|---|---|---|---|---|---|
| active health checks (runbook `§1`, `§12.1`) | per session | yes | while issuer works | while logged in | scheduled only | **no** |
| post-rollback / post-deploy verification (runbook `§9`) | per session | yes | yes | yes | scheduled only | **no** (human needed) |
| workflow runs | per session | yes | yes | yes | if triggered | **no** |
| deploy, rollback execution, config, logs, store read | control plane (unchanged) | same | same | same | same | same |
| per-use overhead | create + revoke + verify each session | rotation | issuer runtime | login | runtime maintenance | none |

## 15. Release / LIVE boundary implications

No option adds or changes a release, promotion, deployment or LIVE operation (G10 = NO for all; the application has no such route [TE]). Resolving ESC-03 by any option is **not** Production Release, LIVE, public operational activation, traffic activation or Founder Release Authorization (MI `§15`). After any option: **PRODUCTION RELEASE = FOUNDER RESERVED · LIVE = FOUNDER RESERVED**.

## 16. Exact Founder Decision Question

> **Q1.** Which mechanism, if any, does the Founder authorize to carry the delegated CEO's Production operational principal (`aios-operator`) through X2 to the Production AIOS API — and on what scope, duration, custody, rotation, revocation and evidence terms?
>
> **Q2 (related).** Is a human Production principal to exist for the Founder, and if so, with which canonical scopes?

## 17. Decision options

**D-1 — mechanism (Q1), as Founder and as Architect:**

| Option | Meaning |
|---|---|
| O-A | E-A per-session bypass |
| O-B | E-B standing bypass |
| O-C | E-C Trusted Sources OIDC |
| O-D | E-D Vercel identity for the CEO |
| O-E | E-E runtime inside the boundary |
| O-F | E-F no new mechanism |
| O-G | another mechanism, or a combination, stated by the Founder |
| O-H | defer |

**D-2 — terms (Q1), required for O-A … O-E and O-G:**

| Term | To be stated |
|---|---|
| T1 environment | Production only, or also Preview |
| T2 deployments | serving deployment, designated rollback target, all Production deployments |
| T3 purpose | all `FDP-010` `§13` duties, or a subset (e.g. health and post-rollback verification only) |
| T4 duration | per session · time-limited · standing until revoked |
| T5 creation and custody | who creates the credential (Founder in the dashboard, or CEO through the provider API); where it is held; whether its transit through the executor's tool output is acceptable under `FDP-010` `§11.4` |
| T6 rotation | interval or trigger |
| T7 revocation | triggers; verification required (302 after revocation) |
| T8 evidence | what is recorded per use (never the value) |
| T9 relation to `FDP-009-03` | superseded, extended, or left separate |

**D-3 — Founder principal (Q2):** P-1 none · P-2 yes, with stated scopes from `security.SCOPES` · P-3 defer.

## 18. Consequences of each option

| Option | ESC-03 | FDP-010 under MI `§21` | Next MI state |
|---|---|---|---|
| O-A | resolved under the stated terms, once implemented and verified | item 4 satisfiable per session | S4 → S5 … S9 |
| O-B | resolved, once implemented and verified | item 4 satisfiable | S4 → S5 … S9 |
| O-C | decided; implementation must first close the `§9` UNKNOWNs; if one fails, back to the Founder (H3/H8) | item 4 conditional on those UNKNOWNs | S4 → S5 (evidence first) |
| O-D | decided; depends on a seat and on the CEO environment holding a Vercel session (UNKNOWN) | conditional | S4 → S5 (Founder adds the identity) |
| O-E | decided; requires an architecture record and new code; cron passage UNKNOWN | conditional | S4 → S5 (architecture first) |
| O-F | **decided as "no CEO API access"** | item 4 (*"operational Production API access is genuinely usable"*) **fails** → **FDP-010 = NOT COMPLETE**; MI `§22` ready state not reachable under that criterion | S4 (record) → stop |
| O-G | as stated | as stated | S4 → per statement (H11 if ambiguous) |
| O-H | stays **NOT RESOLVED** | **NOT COMPLETE** | remain at S3 |

D-3: P-2 gives the Founder an API principal, reachable through X2 by the Founder's Vercel login [INF]; P-1/P-3 leave the Founder without one. D-3 does not change ESC-03.

## 19. Required implementation scope after decision

| Option | Scope (S5–S7), within the stated terms only |
|---|---|
| O-A | per session: create bypass → place in a private file (mode `600`) → operate via the smoke/operator client → revoke → verify 302 → evidence without the value; runbook `§15` procedure; tests (carrier list) |
| O-B | create once; custody file; rotation schedule; revocation and leak procedure; runbook; tests; evidence |
| O-C | verify plan/project support; establish the issuer runtime; configure Trusted Sources; client sends the OIDC header plus the B3 bearer; tests; evidence |
| O-D | the Founder adds the identity (dashboard); CEO login custody; client path; evidence |
| O-E | architecture record; in-boundary caller design (header collision with B3, credential placement); code; tests; evidence |
| O-F | documentation only: ESC-03 recorded as decided "no mechanism"; runbook gaps assigned to a human |
| O-G | as stated |
| O-H | none |

For every option except O-F and O-H, S7 runs MI `§14` positive and negative controls and the `§16` chain with fresh evidence.

## 20. Explicit non-decisions

This package, and a decision on it, does **not** decide: Production Release; LIVE; Founder Release Authorization; Final System Acceptance; public exposure or removal of X2; a change to operator scopes or to `aios.agent.register`; a change to `FDP-009` or `FDP-010` other than what T9 states; the rollback target; the historical FS-09 gate; Constitution, Mission, governance model or Founder authority; Native Core #12; Phase 14; P12/P13 or Platform Organization. It does not authorize the Vercel connector's share-link fetch on protected deployments (runbook `§15`) unless stated.

## 21. Negative controls (to hold after any implementation)

| NC | Control | Verification |
|---|---|---|
| NC-1 | unauthenticated request refused | 302/401 |
| NC-2 | operator bearer without the authorized X2 credential refused | 302 |
| NC-3 | missing scope / wrong scope refused | 401/403 |
| NC-4 | `aios.agent.register` refused to `aios-operator` | 403 |
| NC-5 | Preview principal → Production refused; Production principal → Preview refused | 401 |
| NC-6 | revoked X2 credential refused | 302 |
| NC-7 | no release, LIVE, promotion or deployment route | tests |
| NC-8 | no permanent bypass unless T4 states one | project state |
| NC-9 | no public exposure | project state |
| NC-10 | no credential in repository, documentation, evidence, logs or chat | scans |
| NC-11 | FS-09 gate byte-identical; certified roots unchanged | tests |

## 22. Evidence references

`docs/fullstack/evidence/FS-10-ESC03-ARCHITECTURE-EVIDENCE.json` · `docs/fullstack/FS-10-ESC03-ARCHITECTURE-DECISION.md` · `docs/fullstack/FS-10-ESC-03-AUTHORITY-RESOLUTION.md` · `docs/fullstack/FS-10-ESC03-MI-S0-S1-RECORD.md` · `docs/fullstack/evidence/FS-10-FDP-010-OPERATIONAL-ACCESS-ROLLBACK-2026-10-01.json` · `docs/fullstack/evidence/FS-10-PRODUCTION-VERIFICATION-2026-10-01.json` · `docs/fullstack/FS-10-CURRENT-AUTHORITY.json` · `fullstack/tests/test_esc03_boundaries.py` · Register `§107`–`§116`.

## 23. Canonicalization requirements

A decision answers this package only if it is an explicit Founder instrument (not silence, conversation, inferred intent or "no objection"; MI `§1`, `§10`) that states:

1. its identifier (`§1` proposes `FDP-011`);
2. D-1: one option (O-A … O-H);
3. D-2: terms T1–T9 for the option chosen, where `§17` requires them;
4. D-3: P-1, P-2 (with scopes) or P-3;
5. that Release and LIVE remain Founder-reserved (or nothing to the contrary).

On receipt (MI `§11`, S4): persist verbatim in a four-backtick `text` fence; compute the content hash; register at the next Register number; re-discover the record; check for conflict with a later or higher authority; derive the implementation envelope from the text alone. If its operative meaning is ambiguous: **STOP (H11)**.

---

## Founder decision form

- [ ] **D-1** O-A · O-B · O-C · O-D · O-E · O-F · O-G (stated) · O-H
- [ ] **D-2** T1 … T9 (for the option chosen)
- [ ] **D-3** P-1 · P-2 (scopes: …) · P-3
