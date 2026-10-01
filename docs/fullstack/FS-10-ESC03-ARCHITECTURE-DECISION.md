# FS-10 — AD-FS10-ESC03: Production Operational Edge Access — Architecture Decision Record

| Field | Value |
|---|---|
| **ADR** | `AD-FS10-ESC03` (verbatim: `docs/governance/acts/AD-FS10-ESC03-PRODUCTION-OPERATIONAL-EDGE-ACCESS-ARCHITECTURE-DECISION.md`; Register `§113` receipt, `§114` result) |
| **Phase reached** | DISCOVERY ✓ · EVIDENCE ✓ (with UNKNOWNs that only a provider-side change could close) · ARCHITECT DECISION — **not made** · IMPLEMENTATION — **none** · VERIFICATION — of existing behaviour only |
| **Selection** | **UNSELECTED** (all six candidates) |
| **Final ADR state** | **ARCHITECTURE CONSTRAINED — NO AUTHORIZED MECHANISM** |
| **Founder decision required** | **YES** — `decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE.md` |
| **Evidence** | `evidence/FS-10-ESC03-ARCHITECTURE-EVIDENCE.json` (70 findings, each with its ADR `§7` class) |
| **Release / LIVE** | **PRODUCTION RELEASE = FOUNDER RESERVED · LIVE = FOUNDER RESERVED** (ADR `§28`) |

During evidence (ADR `§24`): no X2 change, bypass, identity, token, service, trust boundary or public exposure was created. Evidence classes are given in brackets: [CAN] canonical, [DV] directly verified, [PD] provider-documented, [CO] configuration observed, [INF] inferred, [UNK] unknown.

## 1. X2 canonical authority

X2 is deployment protection on every deployment, Production included [CAN: FS-DP-03 `R2.6`; ACT-004 `§8`; Register `§93`]. It admits *"a Vercel login or a Founder-authorized, revocable mechanism"* [CAN: `R2.10`]. Its settings are Founder-held configuration [CAN: `R2.5`]. Any architectural modification of deployment protection goes through the architecture authority path [CAN: `FDP-009-02` `§5.5`], and the CEO may not redesign the Production access architecture [CAN: `FDP-009` `§8`]. Temporary passage is for verification only [CAN: `FDP-009-03`]. Provider credentials and accounts remain account-holder controls [CAN: `FDP-010` `§4.2`]. **No conflict between these sources was found**; the later Founder decisions narrow the earlier ACT-004 delegation explicitly.

## 2. Current AIOS authentication

B3 authenticates `aios-operator` with exactly `aios.observe`, `aios.workflow.run`, `aios.audit` once a request reaches the function [DV]. With the token and no X2 credential, the platform answers 302/401 [DV]. Production holds **one** principal, `aios-operator` [CO]; the Vercel team has **one** member, the Founder [CO]. Hence **nobody can use the Production API today**: the Founder passes X2 but holds no Production principal; the CEO holds the principal but cannot pass X2 [INF from DV + CO].

## 3. Limitation map (ADR `§18`)

| Category | Limitation present? | Evidence |
|---|---|---|
| AIOS architecture | **no** — B3 works behind X2 | [DV] |
| X2 architecture | **by design**: admits a Vercel login or a Founder-authorized mechanism; none authorized for the CEO | [CAN] |
| Vercel provider capability | **no** for existence (bypass, share/user-scoped links, Trusted Sources, crons) | [PD] |
| Vercel account configuration | **yes**: no mechanism configured; one member; plan **unknown** | [CO] [UNK] |
| Connector capability | **yes**: `web_fetch_vercel_url` has no header parameter and stops at the SSO 302 | [DV] |
| Claude execution environment | **partly**: it *can* send any header to Production [DV]; it holds **no** token from a documented OIDC issuer [DV]; whether it can obtain one is [UNK] |
| Current application implementation | **no** | [DV] |

"The connector cannot send an `Authorization` header" proves only a connector limitation. It does **not** show that AIOS needs a new authentication architecture.

## 4. Operational requirement matrix (ADR `§15`)

| Responsibility | Required? | Existing CEO path | Direct API required? | Evidence | Authority |
|---|---|---|---|---|---|
| Observe Production | yes (`FDP-010` `§13`) | deployment state, L1 logs, M1 metrics via the control plane; store read-only | **for active probes, yes** (`/health` sits behind X2); passive observation no | [DV] | CEO |
| Run workflow | the operational principal is granted it (`FDP-010-01`) [CAN]; whether the CEO must run workflows for Operational AIOS: [UNK] | none | **yes** | [DV] | CEO with boundary |
| Read audit | yes (incident response) | store read-only (`fullstack-audit`) | no | [DV] | CEO (read-only) |
| Deployment | yes | control plane | no | [DV] | CEO (`FDP-009-01`) |
| Rollback | yes (`FDP-010-02`) | control plane (Instant Rollback) | execution **no**; post-rollback verification (runbook `§9`: health, Scenario B and C) **yes** | [CAN] [DV] | CEO with boundary |
| Recovery | yes | control plane; store read; restore (runbook `§8`) | verification after recovery **yes** | [CAN] [INF] | CEO with boundary |
| Configuration | yes | control plane | no | [DV] | CEO with boundary |
| Incident response | yes | logs, rollback, store | confirming recovery **yes** | [INF] | CEO |
| Health verification | yes (runbook `§1`, `§12.1`) | **none** | **yes** | [DV] | CEO |
| Release | — | — | — | — | **FOUNDER RESERVED** |
| LIVE activation | — | — | — | — | **FOUNDER RESERVED** |

## 5. Candidate evidence (ADR `§9`–`§14`)

**E-A — per-session bypass.** The mechanism exists and its revocation is verified [PD, DV]. `FDP-009-03` covers verification, not operation [CAN]; under current text each operating session would need a Founder authorization, or a Founder decision authorizing the procedure [INF]. No automatic expiry was found in the documentation [UNK]. Audit is available at both the provider and AIOS [DV/PD]. It changes neither public accessibility nor Release/LIVE [INF]. The value transits the executor's tool calls [DV]. Routine repetition approximates standing access [INF].

**E-B — standing bypass.** No canonical source authorizes it, and FDP-009 created none [CAN]. It admits any secret holder to the edge, with B3 behind it [PD/DV]. It adds a trust boundary (the secret holders) [INF]. The settings are Founder-held [CAN].

**E-C — Trusted Sources OIDC.**

| Question | Answer |
|---|---|
| Does the capability exist? | **yes** [PD] |
| Does AIOS need anything to use it? | no AIOS change; B3 unchanged [INF] |
| Can the current execution environment use it? | **no documented issuer token is present** [DV]; whether it can obtain one [UNK] |
| Does the current X2 configuration accept it? | [UNK] — verifiable only after configuration (forbidden in this phase) |
| Does current delegated authority permit deploying it? | **no**: it changes Founder-held protection settings [CAN] through the architecture path [CAN] |

Also: plan entitlement [UNK]; project support [UNK]; the connector cannot carry the header [DV]; a usable issuer would need an external runtime such as CI, and none exists [DV/INF].

**E-D — Vercel identity for the CEO.** This would be a human Vercel user: a team member, or a user-scoped bypass [PD]. It satisfies X2 through an interactive login [PD/INF], which would place provider credentials in the CEO's session [CAN: `FDP-010` `§4.2`]. It needs a new member; the team has one, and seats depend on the plan [CO/UNK]. Founder-administered [CAN]. Revocable [PD]. No Release/LIVE effect [INF].

**E-E — runtime inside the boundary.** None exists [DV]. Vercel crons exist and authenticate with `Authorization: Bearer CRON_SECRET` [PD], the same header B3 uses [INF]. Whether cron invocations pass Vercel Authentication is [UNK]. An in-process caller would either sidestep B3 or need the operator token moved into the function environment [INF]. On-demand triggering needs the CLI (a provider credential) or a new route [INF]. It needs new code, infrastructure and a new operational surface. The CEO may not redesign the Production access architecture [CAN].

**E-F — no new mechanism.** Deployment, rollback execution, configuration, logs and metrics, and read-only store access are executable [DV]. Active health checks, post-rollback and post-deploy verification, and workflow runs are **not** executable by the CEO [DV]. This does not block the Founder Release decision [CAN/INF]. Whether it blocks Operational AIOS depends on who is to run workflows once LIVE [UNK], and on a human principal the Founder could add through the control plane (`FDP-010` `§4.5`) [INF]. A mechanism can be added later as a successor [INF].

## 6. Security evaluation (ADR `§16`)

✓ yes / holds · ✗ no · △ conditional · ? unknown

| | S1 X2 enforced | S2 least privilege | S3 revocable | S4 auditable | S5 credential safety | S6 public exposure unchanged | S7 no new trust boundary | S8 no new identity model | S9 ownership unchanged | S10 failure behaviour |
|---|---|---|---|---|---|---|---|---|---|---|
| E-A | ✓ (exception per session) | ✓ | ✓ manual | ✓ | △ secret in tool calls | ✓ | △ per session | ✓ | ✓ | fails closed (302) when absent or revoked |
| E-B | △ standing exception | ✓ | ✓ | ✓ | △ long-lived secret | △ any holder passes the edge | ✗ | ✓ | ✓ | if leaked, edge open to holders until revoked; B3 still required |
| E-C | ✓ | ✓ | ✓ (remove issuer) | ✓ | ✓ short-lived tokens | ✓ | ✗ external issuer trusted | △ edge identity, not AIOS | ✓ | fails closed if the token is rejected [INF] |
| E-D | ✓ | ✓ | ✓ | ✓ | ✗ provider credential in session | ✓ | △ | ✗ provider identity for the CEO | △ provider administration | fails closed without login |
| E-E | ? (cron passage UNKNOWN) | △ token relocation or B3 sidestep | ? | △ | △ | ✓ | ✗ | △ | △ | a scheduled operator inside the boundary |
| E-F | ✓ | ✓ | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | unchanged: CEO API access absent |

## 7. Governance evaluation (ADR `§17`)

| | G1 Founder decision | G2 Architect decision | G3 inside CEO authority | G4 alters X2 | G5 alters app authorization | G6 new authority surface | G7 certified roots | G8 P12/P13 | G9 Native Core | G10 Release/LIVE |
|---|---|---|---|---|---|---|---|---|---|---|
| E-A | **yes** (`FDP-009-03` purpose) | yes (`§5.5` path) [INF] | no | per-session exception | no | no | no | no | no | **NO** |
| E-B | **yes** (`R2.5`, `R2.10`) | **yes** (`§5.5`) | no | **yes** | no | no | no | no | no | **NO** |
| E-C | **yes** (Founder-held settings, `R2.5`) | **yes** (`§5.5`) | no | **yes** (trusted issuer) | no | no | no | no | no | **NO** |
| E-D | **yes** (`FDP-010` `§4.2`) | yes [INF] | no | no (admits an identity) | no | no | no | no | no | **NO** |
| E-E | possibly (credential custody, CLI) [INF] | **yes** (`FDP-009` `§8`) | no | ? | **possibly** (B3 sidestep / header collision) | **yes** | no | no | no | **NO** |
| E-F | no | no | **yes** (status quo) | no | no | no | no | no | no | **NO** |

**G10 = NO for every candidate.** None is outside the ADR's scope.

## 8. Decision matrix (ADR `§19`)

| Candidate | Evidence complete | Authority class | X2 preserved | Least privilege | Revocable | Auditable | New trust boundary | Founder decision | Architect decision | Selection state |
|---|---|---|---|---|---|---|---|---|---|---|
| E-A | yes | FOUNDER DECISION REQUIRED | ✓ | ✓ | ✓ | ✓ | per session | yes | yes [INF] | **UNSELECTED** |
| E-B | yes | FOUNDER DECISION REQUIRED | △ | ✓ | ✓ | ✓ | yes | yes | yes | **UNSELECTED** |
| E-C | **no** — plan, project support, X2 acceptance and an issuer for the CEO environment UNKNOWN | FOUNDER DECISION REQUIRED (provider settings) + ARCHITECT | ✓ | ✓ | ✓ | ✓ | yes | yes | yes | **UNSELECTED** |
| E-D | partly — seats/plan UNKNOWN | FOUNDER DECISION REQUIRED | ✓ | ✓ | ✓ | ✓ | △ | yes | yes [INF] | **UNSELECTED** |
| E-E | **no** — cron passage of X2 UNKNOWN | ARCHITECT DECISION REQUIRED | ? | △ | ? | △ | yes | possibly | yes | **UNSELECTED** |
| E-F | yes | EXISTING (no change) | ✓ | ✓ | n/a | ✓ | no | no | no | **UNSELECTED** |

## 9. Candidate states (ADR `§21` vocabulary) — classifications on the evidence, not rankings

The ADR assigns these states to *"the Architect"*. For edge access that authority is the architecture path of `FDP-009-02` `§5.5`, held by the Founder acting as Architect (`FD-2` open). The states below are the classification the evidence supports. **They are not an exercise of that authority and select nothing.**

| Candidate | State supported by the evidence |
|---|---|
| E-A | FOUNDER DECISION REQUIRED |
| E-B | FOUNDER DECISION REQUIRED |
| E-C | INSUFFICIENT EVIDENCE |
| E-D | FOUNDER DECISION REQUIRED |
| E-E | INCOMPATIBLE WITH CURRENT ARCHITECTURE |
| E-F | ACCEPTABLE WITH BOUNDARY (boundary: no CEO API access; the gaps of `§4`) |

## 10. Trust boundary, security and authority impact

- **Trust boundary:** E-B, E-C and E-E add one (secret holders; an external issuer; an in-boundary operator). E-A adds one per session. E-D adds a provider identity. E-F adds none.
- **Security:** every candidate keeps B3 and the three scopes. Credential exposure per candidate: E-A a per-session secret in tool calls; E-B a long-lived secret; E-C short-lived issuer tokens; E-D a provider login in the CEO's session; E-E a credential placed in the function environment or a new trigger; E-F none. E-C and E-E have open UNKNOWN fields (`§8`).
- **Authority:** every candidate that gives the CEO API access needs a Founder decision, an Architect decision, or both. None lies within current CEO authority. E-F needs neither.

## 11. Release / LIVE firewall (ADR `§28`)

No candidate changes Release or LIVE (G10 = NO). The application exposes no release, promotion, deployment, rollback or LIVE operation (`fullstack/tests/test_esc03_boundaries.py`). **Production Release = FOUNDER RESERVED. LIVE = FOUNDER RESERVED.** Resolving ESC-03 would not constitute either authorization.

## 12. Negative controls (ADR `§27`) — for the current state (nothing implemented)

| NC | Control | Result |
|---|---|---|
| NC-01, NC-02 | no Release, no LIVE through operational access | PASS (no such route; tests) |
| NC-03 | no permanent X2 bypass | PASS (bypass list empty; no share link; no code carries one) |
| NC-04, NC-05 | no change to Founder Authority or the Governance Model | PASS (the API has no governance surface; the only write runs a workflow) |
| NC-06, NC-07 | no change to certified P12/P13 roots; no Native Core expansion | PASS (read-only Tool; certified-write barrier; no code change) |
| NC-08 | no new operator scopes | PASS (scopes ⊂ canonical model; tests) |
| NC-09, NC-10 | Preview credentials refused on Production, and the reverse | PASS (401 both ways, FDP-010 evidence) |
| NC-11 | no credential in repository, evidence, logs or chat | PASS for the repository and evidence (scans). The temporary bypass and share values of earlier steps transited tool calls only; all are revoked or non-existent |

## 13. Next authorized action

**FOUNDER DECISION REQUIRED** — as Architect, to select (or decline) a candidate, and as Founder, to authorize whatever the selected candidate needs. Package: `decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE.md`. **Implementation: NOT AUTHORIZED.** `ESC-03` stays **NOT RESOLVED**.
