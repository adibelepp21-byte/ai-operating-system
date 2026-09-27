# FS-08 Continuation — Return Package for `ACT-CC-POST-P13-AIOS-FULL-STACK-002`

| Field | Value |
|---|---|
| **Act** | `docs/governance/acts/ACT-CC-POST-P13-AIOS-FULL-STACK-002-FS-08-CONTINUATION.md` · Register `§70` |
| **Authority used** | Only authority that already existed: `FD-FS-001` D2-A (prepare decision packages), `FS-ARCH-RAT-001` `§7` and `§13` (verify, re-discover). The Act's stated status is *"PROPOSED FOR FOUNDER AUTHORIZATION"*; no step below depends on it |
| **Date** | 2026-09-27 |

Evidence classes follow the Act's `§25`: **Observed**, **Verified**,
**Inferred**, **Proposed**, **Ratified**, **Implemented**, **Blocked**,
**Failed**.

## A. Executive result

| Item | Status |
|---|---|
| Act status | **EXHAUSTED_WITH_CLASSIFIED_REMAINDER**. Every action Claude could take has been taken; the Act resumes when an input in `§K` or `§I` arrives |
| FS-08 | **BLOCKED** (final gate `§M`) |
| Workstream A | **BLOCKED**: EXT-05 and EXT-03 unchanged since `§69` |
| Workstream B | **PROPOSED**: FS-DP-02 and FS-DP-05 revision 2 prepared and routed to the Architect; neither ratified |
| Final gate result | **B. BLOCKED** (`§21`) |

## B. External dependency report

Re-discovered on 2026-09-27, after the Act was received:

| Dependency | Status | Evidence |
|---|---|---|
| **EXT-05**: server-side Supabase key in the Preview environment | **Blocked** | `filter_project_envs` on `aios-platform`: `envs: []` (names only; nothing decrypted) |
| **EXT-03**: access to preview deployments | **Blocked** | `web_fetch_vercel_url` on the preview: *"Vercel denied access to this deployment"*; direct requests redirect to Vercel SSO (`FS-08-DEPLOYMENT-EVIDENCE.md` `§4`) |

Neither can be cleared by Claude. The Act forbids inventing a credential
(NC-02) or bypassing deployment protection (NC-04); both need the Founder.

## C. Architecture report

| | FS-DP-02 Identity and Authentication | FS-DP-05 Scaling and concurrency |
|---|---|---|
| Package | `decision-packages/FS-DP-02-IDENTITY-AND-AUTHENTICATION.md`, revision 2 | `decision-packages/FS-DP-05-SCALING.md`, revision 2 |
| Discovery | the port, scopes and audit as built; the console's bearer credential; CSP same-origin; stateless per request; Supabase Auth signs ES256, which the standard library cannot verify; Vercel SSO passes no identity (inferred) | run numbers from a count; `seq` not visible through the contract; no multi-record transaction; positional Trace ranges; non-idempotent `POST`; no retries; no shared in-process state |
| Options | B3 operator tokens · B1a/B1b Supabase Auth · B2 WorkOS (unnamed) · B4 rejected | C1 identity from the Runtime · C2, C3, C4 rejected · C5 constraint only |
| Recommendation | A1 + **B3 first** | **C1** + I1 + partial runs accepted |
| Decision | **not ratified** | **not ratified** |
| Authority | Architect (Freeze `§10`); WorkOS naming would be the Founder's | Architect (Freeze `§10`) |
| Implementation | none: `NoAuthenticator` stays the shipped default | none: behaviour unchanged |
| Verification | none possible before a decision | the finding is reproduced by a test, and the target property is recorded as an expected failure |
| Dependency | opens run creation, so it needs FS-DP-05 decided before or with it | exposed only once FS-DP-02 admits requests |

## D. Implementation report

| Change | Purpose |
|---|---|
| `fullstack/tests/test_deployment.py`: `TheConcurrencyFinding` | reproduces the FS-DP-05 finding (`test_the_finding_reproduces`) and records the property a fix must meet (`test_concurrent_requests_mint_distinct_run_ids`, expected failure) |
| the two decision packages, revision 2 | `§C` |
| the Act, verbatim; Register `§70`; this record | governance |

No application behaviour changed. No migration, no configuration and no
provider setting changed.

## E. Verification report

| Suite | Result |
|---|---|
| `fullstack` | 109 OK, 1 expected failure (the concurrency property) |
| `native_core` | 801 OK, 1 expected failure (unchanged) |
| `consumers` | 276 OK |
| `tools/bounded_exception` | 29 OK |
| `tools` | 1920 OK, 1 skipped |
| Citation audit | 0 errors; warnings unchanged at 94 |

Live tests: **none possible** (`§B`).

## F. Re-discovery report

| Surface | State |
|---|---|
| Repository | branch `claude/aios-activation-authority-discovery-enq7bk`; certified roots, `native_core/`, `consumers/`, `tools/` unchanged |
| Vercel | project `aios-platform`: no environment variables; latest preview `dpl_9yRhRm9SXkT5d9XBrh2DozxvoXYH` (READY, from `b2d3bbd`); earlier preview `dpl_drGHDofUQdk1SgNhTzDSEwSTDunU` READY; production `dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj` from `22c0b49`, **unchanged** |
| Supabase | `aios_records` exists and holds **0 rows**: no deployment has written, which matches EXT-05 |
| Readiness gate | unchanged from `§69`: NOT PRODUCTION READY |

## G. Governance report

- Register `§70`: the Act received, its stated status, and this execution.
- Architect decisions recorded: **none new**. FS-DP-02 and FS-DP-05 await one.
- External dependency classifications: EXT-03, EXT-05 (`§B`).
- Unresolved authority boundaries: authentication (Architect), concurrency
  (Architect), release (Founder, D4-A), the Act's own authorization record
  (Founder).

## H. Remaining work

All of it waits on an input:

1. After EXT-05: verify connectivity, persistence, failure handling and secret
   non-exposure through the deployed function (Act `§7.3`).
2. After EXT-03: verify the static console, the function, headers, refusal,
   health (Act `§8.3`).
3. After FS-DP-05 is ratified: implement, un-mark the expected failure, add the
   threaded test, regress.
4. After FS-DP-02 is ratified: implement the authenticator; for B3 the Founder
   sets the token hashes (a new external dependency); then the live success
   path, Trace and audit.
5. The final FS-08 gate again; FS-09 only on PASS.

## I. Blockers

| Blocker | Class | Owner |
|---|---|---|
| EXT-05 | external dependency | Founder |
| EXT-03 | external dependency | Founder |
| FS-DP-02 | Architect-reserved | Architect |
| FS-DP-05 | Architect-reserved | Architect |

## J. Residual risks

| Risk | Note |
|---|---|
| Concurrency | duplicate run ids once runs are admitted (`FS-DP-05` R2.1) |
| Authentication | none exists; the whole API is closed, which is safe but untestable live |
| Provider limitations | Supabase free plan pauses after inactivity and has no downloadable backups; Vercel rollback to a specific deployment is documented as Pro/Enterprise |
| Backup and recovery | no drill yet (FS-09 criterion) |
| Observability | FS-DP-06 not ratified; logs are not readable through the connector (EXT-03) |
| Deployment access | previews cannot be verified by Claude (EXT-03) |
| Security | refused requests grow the audit table without limit on a public URL (FS-DP-03, FS-DP-06) |
| Operational dependencies | the Python runtime serving this WSGI callable is still inferred, not confirmed |
| INV-12 reading | open Architect observation (`FS-08-DEPLOYMENT-EVIDENCE.md` `§5`) |

## K. Founder decisions and actions required

1. **The Act's authorization record.** It is stated as proposed. Nothing so
   far needed it; the auto-advance to FS-09 (`§34` item 8) is already covered
   by `FS-ARCH-RAT-001` `§14`.
2. **EXT-05**: set `SUPABASE_SECRET_KEY` for Preview in `aios-platform`.
3. **EXT-03**: re-authorize the Vercel connection for team
   `adibelepp21-bytes-projects`, or give Claude another authorized way into
   previews.

Architect decisions (FS-DP-02, FS-DP-05) are listed in `§I`; they are not the
Founder's unless FD-2 (Founder ≡ Architect) is decided.

## L. Exhaustion state

**EXHAUSTED_WITH_CLASSIFIED_REMAINDER.** FS-08 is BLOCKED, not FAIL: nothing
in Claude's repair authority is failing. No claim of FS-08 PASS, Production
Ready, Production Released or Operational AIOS.

## M. Final FS-08 reconciliation gate (Act `§20`)

| Item | Status | Class |
|---|---|---|
| 20.1 Vercel project verified | yes: project, settings, no env vars | Observed |
| 20.1 Preview deployment verified | READY only | Observed; **not verified** |
| 20.1 Static frontend verified | no | Blocked (EXT-03) |
| 20.1 Python function verified | no | Blocked (EXT-03) |
| 20.1 Deployment configuration verified | locally (`TheVercelConfiguration`); region `icn1` accepted by the platform | Verified locally · Observed |
| 20.2 Supabase project verified | yes | Verified |
| 20.2 Persistence adapter verified | locally, on both backends | Verified locally |
| 20.2 Schema verified | yes, live | Verified |
| 20.2 Persistence verified | live in SQL; not through the deployed function | Verified (SQL) · Blocked (function, EXT-05) |
| 20.2 Failure behaviour verified | locally | Verified locally |
| 20.2 Security controls verified | live privileges, triggers, RLS | Verified |
| 20.3 Full Stack → AIOS contracts | locally | Verified locally |
| 20.3 Runtime invocation | locally, per request | Verified locally |
| 20.3 State persistence | locally across request boundaries | Verified locally |
| 20.3 Trace / audit | locally | Verified locally |
| 20.3 Security refusal | locally | Verified locally |
| 20.3 Failure path | locally | Verified locally |
| 20.4 EXT-03 | unresolved | Blocked, external |
| 20.4 EXT-05 | unresolved | Blocked, external |
| 20.5 FS-DP-02 disposition recorded | proposed, routed | Proposed |
| 20.5 FS-DP-05 disposition recorded | proposed, routed | Proposed |
| 20.5 Required Architect decisions persisted | none received | — |
| 20.5 Ratified architecture implemented | n/a | — |
| 20.6 Certified roots unchanged | yes | Verified (diff) |
| 20.6 No unauthorized governance change | yes | Verified |
| 20.6 No authority expansion | yes | Verified |
| 20.6 Full regression passes | yes | Verified (`§E`) |
| 20.6 Citation / evidence integrity | yes | Verified (`§E`) |
| 20.6 Repository clean and reproducible | yes, after the commit that carries this record | Verified |

**Result: B. BLOCKED.** Named blockers in `§I`.

## N. Addendum: Founder authorization and Architect routing (2026-09-27)

The Founder authorized the Act (`acts/ACT-CC-POST-P13-AIOS-FULL-STACK-002-FOUNDER-AUTHORIZATION.md`,
Register `§71`). That settles `§K` item 1. It is an **Act authorization**,
not an architecture ratification.

| Item | Now |
|---|---|
| Act | **FOUNDER AUTHORIZED** |
| FS-DP-02 revision 2 | **routed**; awaiting Architect decision (package `§R2.13`) |
| FS-DP-05 revision 2 | **routed**; awaiting Architect decision (package `§R2.13`) |
| EXT-05, EXT-03 | re-checked on receipt: still **blocked** |
| Readiness gate | still reads only FS-DP-01 and FS-DP-04 as ratified |
| FS-08 | **BLOCKED** |
| Act state | **EXHAUSTED_WITH_CLASSIFIED_REMAINDER**: it continues when an Architect decision is registered or when EXT-03 or EXT-05 is cleared |

**Correction to `§E`.** The `tools` result there (1920 OK) was measured while
the Act file was untracked. On the committed tree one test fails:
`test_the_narrower_population_is_not_better` [status]. Committing verbatim
Founder acts moved a P12-W6 corpus measurement over its limit. It is
recorded, frozen and escalated in Register `§71`. Until the Founder decides,
the FS-08 gate criterion *"Full regression passes"* is **not met**; this is
one more reason FS-08 is BLOCKED, not a new failure of the application.

## O. `FD-P12-007`: the P12 population guard as a classified exception

`FD-P12-007` (Register `§73`) classifies the one `tools` failure,
`test_the_narrower_population_is_not_better` [status], as an **expected,
classified governance signal**, not a code defect. It lets FS-08 treat it as
a **CLASSIFIED EXCEPTION** (D4 R2) under twelve conditions. The FS-08 gate
therefore now has four outcomes: **PASS · FAIL · BLOCKED · CLASSIFIED
EXCEPTION**.

| D4 condition | Status | Evidence |
|---|---|---|
| 1 · the guard still runs | met | unchanged file; collected in every `tools` run |
| 2 · the failure stays visible | met | `tools` reports FAILED (failures=1) |
| 3 · not skipped · 4 · not suppressed · 5 · not turned into a pass | met | the successor checks the predecessor carries no skip or expected-failure marker, and pins its bytes |
| 6 · the test implementation works correctly | met | its arithmetic passes on the certified W6 figures and fails only on the inversion (`P12-POPULATION-GUARD-SUCCESSOR.md` `§4` items 8–9); its 16 sibling controls pass |
| 7 · historical P12 evidence immutable | met | manifest `verify()` holds; 0 files changed under `docs/architecture/p12/` |
| 8 · successor lifecycle recorded | met | `P12-POPULATION-GUARD-SUCCESSOR.md`; Register `§73` |
| 9 · exception recorded in FS-08 evidence | met | this section |
| 10 · every other required suite passes | met | Register `§73` regression row |
| 11 · no unrelated regression hidden | met | the exception names one test id and one subtest; any other failure is outside it |
| 12 · the FS-08 gate records the exception explicitly | met | the row below |

**Gate row, replacing *"20.6 Full regression passes"* in `§M`:**

| Item | Status | Class |
|---|---|---|
| 20.6 Full regression | **CLASSIFIED EXCEPTION**: every suite passes except the P12 population guard, classified by `FD-P12-007` | Verified · Classified |

**FS-08 remains BLOCKED** by EXT-03, EXT-05, FS-DP-02 and FS-DP-05. The
exception does not close FS-08 on its own (`FD-P12-007` `§20`). The best
FS-08 can now reach is **PASS WITH CLASSIFIED EXCEPTION**, once every other
condition is met.
