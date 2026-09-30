# FS-09 — ACT-007 Execution Record

| Field | Value |
|---|---|
| **Act** | `ACT-CC-POST-P13-AIOS-FULL-STACK-007` — FS-09 Residual Authority, Dependency Resolution & Readiness Continuation (Register `§97`, `§98`, `§99`) |
| **Date** | 2026-09-30 |
| **Evidence** | `docs/fullstack/evidence/FS-09-ACT-007-REDISCOVERY-2026-09-30.json` |
| **FS-09 classification** | **BLOCKED**, on one named dependency: `LIVE-REVERIFICATION` (`§7`). Not PASS. Not FAIL |
| **Residuals** | **A** decided (delegated) and conforming · **B** decided (delegated) and implemented, residual stated · **C** implemented and verified, Production side not live · **D** revoked, directly verified |
| **Not** | FS-09 PASS · Production release · Production LIVE · Founder Release Authorization · Founder Acceptance · FS-10 started |

Evidence states are kept apart (ACT-007 `§13`): **DIRECTLY VERIFIED** · **OBSERVED** · **RECORDED** · **INFERRED** · **UNKNOWN** · **BLOCKED**.

## 1. What this Act changed in the picture

ACT-006 ended BLOCKED: four residuals, none closable without a decision or a permission. ACT-007 supplied both. Two of the four residuals were decisions the Founder had reserved; ACT-007 `§3` delegates them, for FS-09 and until its own terminal state. The decisions below are **delegated**, recorded as such (Register `§98`), and open to the Founder's reversal.

The price of wiring E1 is a new fact this Act had to surface rather than hide (`§7`): `fullstack/deploy/vercel.py` is served code, and changing it outgrew the live recording. One dependency now stands between the gate and READY.

## 2. Residual A — Scenario A

| | |
|---|---|
| **Authority** | ACT-007 `§3`, `§5`: bounded delegated Architect authority, FS-09 only |
| **Source** | ACT-001 `§18` (mandatory class) and `§20` (*"residual non-blocking findings classified"*); `FS-DP-07` (A1/A2/A3, `R2.3`–`R2.17`); ACT-004 `§12`–`§13`; Register `§93` DG-03; decision register `§2.1` |
| **Requirement** | *User → Create Agent → Backend → AIOS Agent Capability → Persist → Result* |
| **Options** | A1 keep reserved · A2 instance registration (needs an authority instrument extending `FD-P11-001 §7`) · A3 full Agent Factory. None invented |
| **Decision** | **A1 applies and stays in force.** It cannot execute Scenario A, by design. The only defined option that could is A2, whose precondition does not exist and is not created here. **Scenario A is classified outside the present FS-09 envelope: not executed, a non-blocking residual for the FS-09 gate** (`ACT-007-DG-01`) |
| **Implementation** | none beyond absences: no route, scope, partition, registry use or console control for Agents |
| **Verification** | DIRECTLY VERIFIED: `test_architecture_conformance.py` (10 tests, three new), gate rows *agent creation (Scenario A)* PASS and *A1: no route creates an Agent* PASS |
| **What it is not** | not a statement that Scenario A works; not Founder Acceptance; ACT-001 `§18` is not rewritten |
| **Ambiguity recorded** | ACT-004 `§12` says *"implement the A1 Agent Creation architecture … to make it operational"*, while the package defines A1 as creating none. The ratified identifier is read as the package defines it. If the Founder meant an operational creation path, that is A2 and needs its instrument |
| **The judgment to review** | classifying a *mandatory* class as a non-blocking residual is what makes this row PASS. It is the delegation's exact wording, the A1 path the package itself described (`R2.15`), and reversible; it is also the decision in this Act with the most weight, and the one most worth the Founder's own look |

## 3. Residual D — the temporary bypass

| | |
|---|---|
| **Target** | the Protection Bypass for Automation noted *"TEMPORARY FS-09 re-verification 297e8b8"* |
| **Attempt** | one load of the secret from its private file (ACT-007 `§8.3`). The classifier permitted it this time (it had denied it twice before). The revoke call followed, `regenerate: false` |
| **Result** | **the control returned `protectionBypass: {}`** (DIRECTLY VERIFIED) |
| **Protection** | `ssoProtection` enabled, `all_except_custom_domains`; password protection and trusted IPs off (DIRECTLY VERIFIED, after the revoke) |
| **Edge** | the revoked secret, sent as a header to three hosts, gets **302** exactly as no secret does: branch alias, newest Preview, `aios-platform-eight.vercel.app` (DIRECTLY VERIFIED) |
| **No replacement** | no generate call was made; the response is an empty map |
| **Secret handling** | the value appeared in this session's output when it was loaded (disclosed to the Founder); it went only to the revoke call and to the status-only header test; the private copy was shredded; it is in no repository file or commit; it is revoked |
| **Gate** | *Security: temporary access revoked* PASS, on the revocation record (`revocation_record`): control response, protection state and edge refusal, all three required |

## 4. Residual C — E1 application wiring

| | |
|---|---|
| **Implementation** | `fullstack/deploy/vercel.py` (`acab4df`): `SUPABASE_PROJECTS` keyed by `VERCEL_ENV` exactly (`preview` → `scfymftfzkpilqbgmfwv`, `production` → `hmljfyqycxcueulhsjae`). Any other value — absent, `development`, empty, `Production`, `" preview"`, `"production\n"` — raises `UnknownEnvironment` before a key is read or a database called; the function answers 503 and logs the refusal like any other. No variable overrides the project. The environment comes from the process, never from a request. Each environment's key stays a Vercel variable in its own scope |
| **Tests** | `test_environment_separation.py` (11 new) + updated `test_deployment.py`; four mutations of the resolver (fall back to preview; production pointed at preview; fold/trim the value; bypass the resolver) are each caught |
| **Preview target** | DIRECTLY VERIFIED live (partial): the wiring build `dpl_GnbHK8R7haxE6fGXpPATPHsZ8XPp` answered health 200; its L1 line carries the same `request_id`; **the Preview project's Supabase API log shows the function's `GET /rest/v1/aios_records` 200 at 17:12:46.975Z, and the Production project's log is empty**. `VERCEL_ENV` therefore resolved to `preview` on Vercel, and the Preview project answered |
| **Production target** | OBSERVED, not live: the resolver selects the Production project and a production-env function reaches only that host (recording databases). No Production deployment, key or release exists, and none was made |
| **Production isolation** | DIRECTLY VERIFIED: 0 rows; 0 API requests to the Production project in 24 h; Production deployment `22c0b49` unchanged; no Production variables |
| **Preview store** | max seq 350 before and after (345 rows): the live checks wrote nothing |
| **Stray requests** | two `GET`s to the Preview project at 17:11 from Python 3.11 returned 401: local mutation-test runs sending an invalid test key. Refused; nothing read or written |
| **Distinct states (NC-13)** | project exists ✔ · schema verified ✔ · application wiring ✔ (code, tests, Preview live) · Production deployment ✘ · Production LIVE ✘ |

## 5. Residual B — Alerting

| | |
|---|---|
| **Authority** | ACT-007 `§3`, `§6`: bounded delegated Architect authority, FS-09 only |
| **Source** | `FS-DP-06` rev 2 `R2.4`–`R2.16`; ACT-001 `§20`; ACT-003 `§19`; Register `§93` DG-02 |
| **Separation kept** | Logging L1 · Metrics M1 · Alerting · Readiness R2. **R2 = readiness and is not an alerting option** |
| **Definitions confirmed** | `R2.6`: **H1** the host's alerting if the plan provides it (possibly paid) · **H2** an external uptime check on `/health` (a third party) · **H3** none; the runbook's manual checks. Option definitions unchanged since `5941d72` (only the Status row changed, at `7df974a` and now) |
| **Selection** | **H3** (`ACT-007-DG-02`) |
| **Why not H1** | plan entitlement for alerts is not established by the documentation retrieved; this session holds no alert-rule control (the Vercel connector has none; the CLI is not authenticated); a recipient and any spend are Founder-reserved |
| **Why not H2** | a third party (Founder-reserved) and an edge path: under N1/X2 every URL answers 302 to Vercel SSO, so a monitor is reached only through a bypass or by unprotecting, both forbidden |
| **Implementation** | runbook `§12.1` *Manual monitoring checks (H3)*; ownership `§6`; the gate checks the content (`H3_MARKERS`) |
| **Drill, 2026-09-30** | readiness: health 200 · error rate: the wiring build's log, one L1 line, `server_errors` 0 · refusals before the Application: none · temporary access: empty bypass map · **backup freshness: a finding** (below) |
| **Residual** | no automatic alert; failures are found only when a person runs the checks. H1/H2 stay with the Founder |

**Finding from the drill.** The latest backup export is dated 2026-09-27. The Preview store now holds 345 rows against the ~80 exported; the rest is FS-08/FS-09 test traffic, and the Production store holds none. The runbook's check says *"older than the last store change that matters"*: nothing in the Preview store matters as production data, so no export was made (it is outside this Act). Before any Production use the check will matter.

## 6. Verification matrix (ACT-007 `§11`)

| ID | Result | Class |
|---|---|---|
| V-01 Scenario A source | ACT-001 `§18` identified | DIRECTLY VERIFIED |
| V-02 decision | A1 applies; outside the envelope (`DG-01`) | DIRECTLY VERIFIED |
| V-03 conformance | the absences hold; Scenario A not executed | DIRECTLY VERIFIED |
| V-04 FS-DP-06 | H1/H2/H3 definitions confirmed | DIRECTLY VERIFIED |
| V-05 decision | H3 (`DG-02`) | DIRECTLY VERIFIED |
| V-06 conformance | `§12.1` gate-checked; drill run; residual stated | DIRECTLY VERIFIED + OBSERVED |
| V-07 E1 selection | resolver, tests, mutations | DIRECTLY VERIFIED |
| V-08 Preview target | Preview project answered the Preview build | DIRECTLY VERIFIED (live, partial) |
| V-09 Production target | resolver + recording fakes; no deployment or key | OBSERVED, not live |
| V-10 Production data safety | 0 rows; 0 API requests in 24 h | DIRECTLY VERIFIED |
| V-11 Protection | ON | DIRECTLY VERIFIED |
| V-12 Bypass | revoked | DIRECTLY VERIFIED |
| V-13 Anonymous edge | 302 from Vercel, on three hosts | DIRECTLY VERIFIED |
| V-14 Protected API | Vercel layer 302 (verified now); AIOS 401 recorded at `297e8b8` and in local tests; **not re-measured live on the new code** | VERIFIED (edge) + RECORDED |
| V-15 FS-08 regression, live | **BLOCKED** (`LIVE-REVERIFICATION`). Local: fullstack tests OK | BLOCKED |
| V-16 FS-09 regression, live | **BLOCKED** (same). Local: OK | BLOCKED |
| V-17 negative controls | `§8` | see `§8` |
| V-18 final re-discovery | `§9` | done |

## 7. The dependency this Act created: `LIVE-REVERIFICATION`

`vercel.py` is served code. The gate counts a live recording only while `git diff <recorded commit> -- <served paths>` is clean (a rule written for exactly this, and applied to the docstring-only change in `297e8b8`). The wiring change makes the `297e8b8` recording stale. So **19 criteria that rest on the live suites are BLOCKED**, not failed: FS-08's 14 checks, FS-09's 5, the rollback drill, L1/M1 in the host log.

* **Why not re-run them:** they need access past Vercel SSO and the operator token. The only mechanism is a Protection Bypass for Automation. ACT-007 forbids creating one, and the one that existed had to be revoked.
* **Why BLOCKED, not FAIL:** ACT-007 `§15` reserves FAIL for a requirement *affirmatively tested and found unsatisfied*. A recording the code has outgrown is unverified, not failing. I changed the gate to say so (it reported FAIL before); nothing that passed before passes differently, and the stale-recording path can never pass. A test pins this.
* **What closes it:** a Founder instrument authorizing one temporary access for the re-run and its revocation, or the Founder running the suites. Then a new recording names the wiring commit and the gate reads it.

With a recording that covered the tree, the gate would read PRODUCTION READY: nothing else stands between it and that, and READY is not a release.

## 8. Negative controls (ACT-007 `§12`)

| NC | Result | Basis |
|---|---|---|
| 01 no Phase 14 | HELD | no p14 / phase-14 path |
| 02 no P13 reopened | HELD | — |
| 03 certified roots | HELD | integrity holds; `tools/` unchanged since `edb3beb` |
| 04 no Native Core expansion | HELD | `native_core/`, `consumers/` unchanged since `edb3beb` |
| 05 no Production release | HELD | `22c0b49` unchanged |
| 06 no LIVE declaration | HELD | — |
| 07 no new Vercel bypass | **HELD for Protection Bypass for Automation; QUALIFIED for shareable links** | none generated (the revoke response is an empty map). Separately, the connector's `web_fetch_vercel_url` — used for three GETs — appears to authenticate through Vercel's shareable-link mechanism (its redirect carried a `_vercel_share` token), which I learned only afterwards. It is short-lived, was not stored, and is not used again; `get_access_to_vercel_url`, documented as creating a bypass link, was never called. Evidence obtained through it is labelled |
| 08 protection not disabled | HELD | DIRECTLY VERIFIED |
| 09 no secret persisted | **HELD for persistence; exposure disclosed** | no non-hex 32-character token in any added line; private copy shredded. The value was displayed in this session's output when loaded; it is revoked |
| 10 no A-option invented | HELD | A1/A2/A3 only |
| 11 no H-option invented | HELD | H1/H2/H3 only |
| 12 R2 not relabeled | HELD | runbook and gate keep them apart |
| 13 E1 not claimed complete without evidence | HELD | `§4`: Production side not live, stated |
| 14 stores not conflated | HELD | recording-database tests; both project logs checked |
| 15 no unsupported authority inference | HELD | delegation explicit; the ACT-004 `§12` ambiguity recorded, not resolved |
| 16 no permission workaround | HELD | the one load attempt was permitted by the classifier; no other route to the secret; no other bypass |
| 17 verification ≠ Founder Acceptance | HELD | — |
| 18 exhaustion ≠ completion | HELD | `§10` |
| 19 historical evidence not rewritten | HELD | the `297e8b8` recording still says `access_revoked: false`; ACT-005/006 records stand, with a pointer |
| 20 no unrelated expansion | HELD | one source file changed in the application (`vercel.py`), plus the gate and tests |

## 9. Final re-discovery (ACT-007 `§16`)

* **What remains unresolved:** the judgment in `§2` (Founder review); the H1/H2 question (spending, recipient, an edge path); Production key/variables/deployment (FS-10); a fresh backup export.
* **What remains blocked:** `LIVE-REVERIFICATION` only.
* **What changed:** `vercel.py` (E1 selection); the gate (delegated decisions, measured wiring, revocation record, stale → BLOCKED); runbook `§12.1`; ownership `§6`; Register `§97`–`§99`; status rows of three packages; tests 197 → 233. The bypass is gone.
* **What did not change:** `native_core/`, `consumers/`, `tools/`, certified evidence, ACT-004/005/006 (byte-identical), the Production deployment, the Production store, the migrations on both stores, the Preview store's contents.
* **New evidence:** this record's evidence file. **Historical only:** the `297e8b8` recording (for the live suites), the `a4a11cf` and FS-08 recordings.
* **Authority still required:** the access instrument for `§7`; the Founder's review of the two delegated decisions.
* **Actionable work left inside this Act:** none. Every step that remains needs an instrument this Act does not contain.
* **Does the gate pass:** no (`§10`).

## 10. Gate and terminal classification

@@GATE@@

```text
ACT-007 residuals:  A decided (delegated)   B decided (delegated)   C implemented   D revoked
FS-09 gate       = BLOCKED   (one dependency: LIVE-REVERIFICATION; 0 FAIL)
FS-09 ≠ PASS     FS-10 = NOT STARTED
Production       = untouched; not released; not LIVE
```

## 11. Regression

@@REGRESSION@@

## 12. Next frontier

| Matter | Fact | Owner / authority | Dependency | Why still open | Evidence |
|---|---|---|---|---|---|
| Live re-verification | the served code changed; 19 criteria rest on live suites the new code has not faced | Founder | one temporary access, authorized and then revoked, or the Founder running the suites | ACT-007 forbids creating a bypass | `§7` |
| The two delegated decisions | A (Scenario A outside the envelope) and B (H3) were made by delegation | Founder | none | the delegation expires at this Act's terminal state; a Founder instrument can confirm or reverse them | Register `§98` |
| Alerting beyond H3 | no automatic alert | Founder | spending, a recipient, an external service, an edge path | Founder-reserved | `§5` |
| Production | no key, variable, deployment or release | Founder, FS-10 | the release sequence | outside FS-09 | `§4` |
| Backup | the export is 3 days and ~260 test records behind | operator | none | outside this Act; matters before Production use | `§5` |
