# FS-09 — ACT-005 Execution Record

| Field | Value |
|---|---|
| **Acts** | `ACT-CC-POST-P13-AIOS-FULL-STACK-004` (FS-09 Master Act, Register `§91`); `ACT-CC-POST-P13-AIOS-FULL-STACK-005` (Continuation, Reconciliation & Execution Resumption, Register `§92`) |
| **Register** | `§91`–`§94`; continued by ACT-006 (`§95`, `§96`; `docs/fullstack/FS-09-ACT-006-EXECUTION-RECORD.md`) and ACT-007 (`§97`–`§99`; `docs/fullstack/FS-09-ACT-007-EXECUTION-RECORD.md`) |
| **Date** | 2026-09-28; final reconciliation 2026-09-30 (`§18`, `§22`) |
| **FS-09 classification** | **EXHAUSTED_WITH_CLASSIFIED_REMAINDER** (`§21`) |
| **Not** | FS-09 PASS; Production release; Production LIVE; Founder Release Authorization; FS-10 started |

Evidence states are kept apart (ACT-005 `§17`): **L** local, measured now ·
**P** Preview, live, recorded (`docs/fullstack/evidence/FS-09-LIVE-PREVIEW-2026-09-30.json`,
commit `297e8b8`; the `a4a11cf` recording of 2026-09-28 is history) ·
**O** operator inspection of a live store · nothing here is Production evidence
except the Production **store** inspections, labelled as such.

## 1. Authority verification

| Authority | Source | Used for |
|---|---|---|
| Full execution within FS-09; bounded Architect authority for the five packages; FS-09 PASS/FAIL/BLOCKED | ACT-004 `§4`, `§6`, `§7`, `§41`, `§42` | construction, verification, decisions DG-01 to DG-05 as issued |
| Continuation; no bypass of execution permissions; no alerting selection; no premature PASS | ACT-005 `§8`, `§9`, `§7`, `§13` | this record's boundaries |
| **Not held** | ACT-004 `§6`, `§67`–`§69`, `§79`; ACT-005 `§24`, `§28` | Production release or activation; Founder Release Authorization; Constitution; Founder authority; governance model; Phase 14; P12/P13; Native Core #12 |

## 2. ACT-004 preservation verification

`docs/governance/acts/ACT-CC-POST-P13-AIOS-FULL-STACK-004-FS-09-PRODUCTION-READINESS-MASTER-ACT.md`
is byte-identical since its commit `d64b179` (`git diff --quiet d64b179`). Its
`§10` still reads *"Alerting = R2"*; the discrepancy is recorded (Register
`§91`, `§92`), not edited.

## 3. ACT-005 registration

Persisted verbatim (`docs/governance/acts/ACT-CC-POST-P13-AIOS-FULL-STACK-005-FS-09-CONTINUATION-RECONCILIATION-RESUMPTION.md`),
registered at `§92`, committed and pushed (`d64b179`).

## 4. Current-state re-discovery (at receipt of ACT-005)

| ACT-005 `§3` stated | Re-verified |
|---|---|
| ACT-004 received, persisted, registered | received and persisted; **not yet committed** (the commit was blocked under ACT-004) → committed under ACT-005 (`d64b179`) |
| Production project created, empty, no schema | `hmljfyqycxcueulhsjae` ACTIVE_HEALTHY; 0 tables; 0 migrations (O) |
| FS-09 OPEN, FS-10 NOT STARTED | confirmed |
| Git commit/push blocked | **no longer blocked**: commit and push succeeded |
| Supabase shared-resource mutation blocked | **not blocked** under ACT-005: the migration applied (`§7`) |

## 5. FS-DP-06 source recovery result

Located (ACT-005 `§6` priority 2): `docs/fullstack/decision-packages/FS-DP-06-OBSERVABILITY.md`
revision 2, committed `5941d72` (SHA-256 `7aad41b3…`). *Qualification, 2026-09-30 (ACT-006 record `§6` N-2): only its Status row has changed since, at `7df974a`, to record the ratification; the option definitions are byte-identical to `5941d72` and the file now hashes `f16aabd3…`.* `R2.6`
defines **L1–L3** logging, **M1–M3** metrics, **H1–H3 alerting**, **R1/R2
readiness signal**. No Architect ratification record selects an H option
(priority 1: the Register holds none before ACT-004; ACT-004 selects none).

```text
FS-DP-06 Alerting Definition = LOCATED (H1–H3 defined)
FS-DP-06 Alerting Selection  = UNRESOLVED (no canonical selection)
```

## 6. R2 semantic reconciliation

ACT-004 `§10` pairs *"Alerting"* with *"R2"*. The canonical package defines R2 as
**readiness** (*"keep today's implicit meaning (deployed 200 implies the store
started) and document it"*). Current execution interpretation (ACT-005 `§5`):
**R2 = readiness**; alerting undecided; no H option inferred (NC-03, NC-04).

## 7. E1 state (FS-09-ENV)

| Step | State | Evidence |
|---|---|---|
| Production project | **created** 2026-09-28 00:00:54Z, `aios-production`, ap-northeast-2, free organization (no cost) | O |
| Schema | **applied**: migration `aios_records` = the repository's SQL unchanged (host version stamp `20260928051800`) | O |
| Schema equality | columns, check constraints, triggers, function definitions (md5), RLS on with no policy, grants: **equal** to the Preview store's; compared from the catalog, **no row written** | O |
| Isolation, live | after the FS-09 Preview suite (126 records written): Preview store 207 records; **Production store 0** | P + O |
| Deployment wiring (select the store by `VERCEL_ENV`) | **BLOCKED — execution permission.** The edit to `fullstack/deploy/vercel.py` was denied by the session's permission classifier (*"Modify Shared Resources"*). Not retried, not worked around | — |
| Consequence | the adapter still names only the Preview project. A Production deployment today would either fail closed (a Production-only key is refused by the Preview project) or, if given the Preview key, write into the Preview store. No Production deployment or Production variable exists | — |

```text
E1 PROJECT CREATED = YES   E1 SCHEMA = YES   E1 IMPLEMENTED = NO (wiring blocked)   E1 VERIFIED = PARTIAL
```

## 8. P2 state (FS-09-RUNTIME)

`.python-version` = `3.12` (commit `a4a11cf`). FS-02 technology row amended
explicitly, the former *"Python 3.11"* wording quoted. Build `bld_4iu3yl646`
(P): *"Using Python 3.12 from .python-version"* (the FS-08 build had read *"No
Python version specified … Using python version: 3.12"*). All five suites pass
on 3.12 (L, `§18`). **Implemented and verified.**

## 9. N1 state (FS-DP-03)

N1 as written; implementation form **X2** (protection on every deployment URL,
the Founder-restored `all_except_custom_domains`). L: no `Access-Control-*`
header on any response; a CORS preflight answers 405; `vercel.json` one origin;
served code's only outbound host is `*.supabase.co`; no listener; no database
credential in the browser (`fullstack/tests/test_architecture_conformance.py`).
P: HSTS `max-age=63072000; includeSubDomains; preload`; no cross-origin grant;
preflight 405; console CSP `connect-src 'self'`; without authentication the host
answers 302/401 before AIOS runs. **Implemented and verified.**

## 10. L1 state

One `fullstack.request/1` line per request (`fullstack/backend/telemetry.py`),
including refusals before the Application. Route template only; no
credential, hash, body, document or raw path. L: 12 tests, 7 mutations killed.
P: all **45** function requests of the live suites that received an
`X-Request-Id` appear in the Vercel runtime log with that `request_id`; the
46th was refused by Vercel protection before the function. Re-verified on
`297e8b8` (2026-09-30): again **45 of 45**, plus the 13 drill requests on the
same deployment. **Implemented and verified.**

## 11. M1 state

`fullstack/deploy/request_metrics.py` (created as `metrics.py` in `a4a11cf`; renamed, `§18`) and `python -m fullstack.backend metrics --log`.
No emitter. P (derived from the host log lines): 45 requests; 29 2xx, 16 4xx, 0
server errors; latency p50 55 ms, p95 693 ms, max 708 ms. On `297e8b8`
(2026-09-30): 58 lines; 40 2xx, 18 4xx, 0 server errors; p50 60 ms, p95 337 ms,
max 379 ms. **Implemented and verified.** Figures are observations; no requirement exists (ACT-004 `§39`).

## 12. R2 readiness state

Deployed `GET /api/v1/health` = 200 only after a Runtime started on the store,
503 otherwise (L: `ReadinessKeepsItsImplicitMeaning`; the gate's dependency
probe). P: health 200 through the deployment. **Implemented and verified.**

## 13. A1 state

No route creates an Agent: the only state-changing route is `POST
/api/v1/runs`; runs show the acting Agent Instances (L: conformance tests). No
Agent Factory, Planner, Scheduler or Orchestrator. **In force.** Scenario A
therefore cannot occur; whether it stands as a classified non-blocking residual
is a Founder decision not taken (NC-17: not converted from a recommendation).

## 14. Rollback state

Drill on Preview (P), 2026-09-28, branch alias
`aios-platform-git-claude-aios-897a81-adibelepp21-bytes-projects.vercel.app`:

| Phase | Served by (host log) | Health | Anonymous | Reads the other version's run | Scenario B | Scenario C | Runs listed / distinct |
|---|---|---|---|---|---|---|---|
| rolled back | `dpl_EJJbGcdvDEfm4b2JQE14d1uaN2Xc` (`d64b179`) | 200 | 401 | yes (`fullstack.run/2`) | 201 succeeded | 201 failed | 27 / 27 |
| rolled forward | `dpl_8Znqrn818NgYy66RU7hz819t4ZTj` (`a4a11cf`) | 200 | 401 | yes | 201 succeeded | 201 failed | 29 / 29 |
| **2026-09-30** rolled back | `dpl_6xyzjXKxqcLkVdxHZ9QnXYQ46CZ4` (`7df974a`) | 200 | 401 | yes | 201 succeeded | 201 failed | 47 / 47 |
| **2026-09-30** rolled forward | `dpl_FjjGC9Hg54RGzGSugwidwHdRTrwM` (`297e8b8`) | 200 | 401 | yes | 201 succeeded | 201 failed | 49 / 49 |

2026-09-30: each phase's first attempt ended on a TLS EOF (rolled back: at the
Scenario C POST, after its Scenario B run was written; rolled forward: at a GET,
before any write); each phase was then re-run in full. Before the drill the
alias was still on `dpl_8Znq…` (`a4a11cf`): a manually assigned alias stays
pinned (runbook `§9`).

Deployment + data/state compatibility + security posture (B3; 401) +
environment configuration (same store, same variables) all hold (ACT-004
`§34`). Rolled back, the requests had no L1 lines: the documented cost of going
below the L1 commit. **Production rollback not exercised** (operator, on a
Founder decision). Floors: runbook `§10`.

## 15. Permission blockers

| Operation | Authority | Execution permission | State |
|---|---|---|---|
| per-environment store selection in `fullstack/deploy/vercel.py` (E1 wiring) | GRANTED (ACT-004 DG-04) | **BLOCKED** (classifier: Modify Shared Resources) | not done; the Founder/user must allow it |
| under ACT-004 only: reading the migration, a read-only search, git commit/push | GRANTED | were BLOCKED under ACT-004 | **cleared** under ACT-005 (all succeeded) |
| Supabase connector names `Supabase`, `Supabase-a706c54a` | — | need authorization in claude.ai connector settings | not needed: `Supabase-3f9c6417` serves the organization |
| **revoking the temporary bypass created 2026-09-30** for the `297e8b8` re-verification (ACT-004 `§56`) | GRANTED (ACT-004 `§56`: it *"must be revoked afterwards"*) | **BLOCKED**: the host's revoke call takes the secret; loading it from the private file into the session was denied by the classifier (*Credential Materialization*). Not retried, not routed around | **the bypass is ACTIVE** (NC-16 of ACT-004 `§50` not yet met). The Founder/user revokes it in Vercel → project `aios-platform` → Settings → Deployment Protection → Protection Bypass for Automation (note *"TEMPORARY FS-09 re-verification 297e8b8"*), or allows the load. The secret is in no file of the repository, commit, log or report; its only copy is a private file (mode 600) in the session's ephemeral scratch directory, outside the repository, held so the revocation can still be made from a session once allowed. This departs from the ownership model's *"revoked immediately after use"* (`FS-09-OPERATIONAL-OWNERSHIP.md` `§2`), which is why the gate blocks on it |

## 16. Evidence inventory

| Evidence | Class |
|---|---|
| `docs/fullstack/evidence/FS-09-LIVE-PREVIEW-2026-09-30.json` (commit `297e8b8`, the gate's current recording): 14 FS-08 checks + 5 FS-09 checks (all PASS), request ids, host-log L1 lines, M1 derivation, rollback drill, store counts, UPDATE refused, bypass **not revoked** (`access_revoked: false`) | P, O |
| `docs/fullstack/evidence/FS-09-LIVE-PREVIEW-2026-09-28.json` (commit `a4a11cf`; history since `297e8b8` changed a served docstring) | P (historical) |
| `docs/fullstack/evidence/FS-08-LIVE-PREVIEW-2026-09-27.json` (history, unchanged) | P (historical) |
| `docs/fullstack/evidence/FS-09-BACKUP-*` (history, unchanged) | O |
| build logs `bld_4iu3yl646` (`a4a11cf`), `bld_blcnziphb` (`297e8b8`): *"Using Python 3.12 from .python-version"* | P |
| Production store catalog comparison and row count (`§7`) | O |
| tests: `test_observability.py`, `test_architecture_conformance.py`, `test_readiness.py` (gate v3) | L |

## 17. Negative-control results (ACT-005 `§19`)

| NC | Result | Evidence |
|---|---|---|
| 01 ACT-004 preserved | HELD | `§2` |
| 02 ACT-005 does not rewrite ACT-004 | HELD | separate file; ACT-004 unchanged |
| 03 R2 not converted into alerting | HELD | `§6`; gate row *alerting* BLOCKED |
| 04 H1/H2/H3 not invented | HELD | no H option selected anywhere |
| 05 unknown architecture not converted to authorization | HELD | alerting and Scenario A residual left undecided |
| 06 capability not treated as authority | HELD | project creation, connectors used only within ACT-004 decisions |
| 07 permission failure not bypassed | HELD | E1 wiring and the bypass-secret load (2026-09-30) not retried or routed around (`§15`) |
| 08 project creation not treated as readiness | HELD | `§7`: E1 IMPLEMENTED = NO |
| 09 Production LIVE not declared | HELD | no Production deployment, alias, variable or traffic |
| 10 Founder Release Authorization not inferred | HELD | — |
| 11 P10–P13 certified roots unchanged | HELD | certified-evidence integrity 0 |
| 12 Native Core unchanged | HELD | no change under `native_core/`, `consumers/` or `tools/` since `edb3beb` (`git diff`) |
| 13 no Native Core #12 | HELD | — |
| 14 no Phase 14 | HELD | — |
| 15 FS-10 not declared started | HELD | — |
| 16 evidence not upgraded without source | HELD | classes kept; FS-08 recording stays history; Production store evidence labelled O |
| 17 recommendation not converted to decision | HELD | package recommendations stand as analysis; only ACT-004's decisions recorded |
| 18 local/Preview not labelled Production | HELD | `§7`, `§16` |
| 19 historical evidence not overwritten | HELD | FS-08 files unchanged; runbook history marked *History* |
| 20 FS-09 PASS not declared without complete gate evidence | HELD | `§21`; the active bypass is a gate row, not a footnote |

## 18. Regression results

### 18.1 The 95th citation warning (2026-09-30)

| Question | Answer |
|---|---|
| **Exact warning** | `docs/governance/AIOS_NATIVE_CORE_CLOSEOUT_v1.0.md:285` cites `metrics.py`: *"ambiguous: 2 files share this name"* |
| **Baseline** | `edb3beb` (before ACT-004 construction): 94 warnings; this citation then resolved to the single file `docs/architecture/history/legacy-execution/metrics.py` |
| **Origin** | **ACT-005 construction**: commit `a4a11cf` created `fullstack/deploy/metrics.py` (M1), a second file of the same name. Not a gate, runbook or documentation change; not pre-existing; not unrelated |
| **Classification** | **genuine defect, governance-relevant** (a certified-era governance record's citation stopped resolving to one file); **non-functional** (no code, test or gate outcome depends on it); low materiality. Not documentation-only: the cause was a code file name |
| **Repair (within authority)** | `297e8b8`: `git mv fullstack/deploy/metrics.py fullstack/deploy/request_metrics.py`, importers and the docstring updated. The governance record was **not** edited; no warning was suppressed or filtered |
| **Result** | 94 warnings, **the same set as `edb3beb`** (compared entry by entry, `§18.3`) |
| **Consequence** | the rename touched a served docstring (`telemetry.py`), so the `a4a11cf` live recording no longer covered the tree (gate v3 marks such a recording stale, by design). Re-verified live on `297e8b8` (`§18.2`) rather than weakening that rule |

### 18.2 Live re-verification of `297e8b8` (P, 2026-09-30)

Deployment `dpl_FjjGC9Hg54RGzGSugwidwHdRTrwM`, build `bld_blcnziphb` (*"Using
Python 3.12 from .python-version"*). FS-08 suite 14/14 PASS; FS-09 checks 5/5
PASS; L1 45/45 in the host log; M1 derived (`§11`); rollback drill both
directions (`§14`); Preview store refused an UPDATE (seq 350); Production store
**0 rows**; migrations unchanged on both stores. Evidence:
`docs/fullstack/evidence/FS-09-LIVE-PREVIEW-2026-09-30.json` (secret-scanned:
neither the operator token nor the bypass secret appears).

Access used a temporary Protection Bypass for Automation under ACT-004 `§56`.
**It is not revoked** (`§15`): the gate row *Security: temporary access revoked*
is BLOCKED on `BYPASS-REVOCATION` until it is, and `EXT-03` says so.

### 18.3 Regression, audits, integrity (final run, 2026-09-30, at `b5f195a` + this record)

| Check | Python 3.12 (reference, P2) | Python 3.11 (compatibility) |
|---|---|---|
| native_core | 801 OK (1 expected failure) | 801 OK (1 expected failure) |
| consumers | 276 OK | 276 OK |
| bounded_exception | 29 OK | 29 OK |
| fullstack | 197 OK | 197 OK |
| tools | 1933 OK (1 skipped), 2376 s | not run (3.12 is the reference) |

* **Citation audit** (`python -m tools.corpus_citation_audit`): 94 warnings, 0 errors; its 182 findings are **the same set** as at baseline `edb3beb` (compared entry by entry: none added, none removed).
* **Certified-evidence integrity** (`python -m tools.certified_evidence_integrity`): holds.
* **ACT-004** byte-identical since `d64b179`; `native_core/`, `consumers/`, `tools/` unchanged since `edb3beb`.
* **Secret scan**: neither the operator token nor the bypass secret appears in any changed file or in the commits since `297e8b8`.
* **Gate mutations** (new row): forcing *revoked*, forcing the evidence flag, and turning the fallback FAIL into PASS are each caught by the tests.

## 19. Re-discovery results

* **Changed since `§93`:** `fullstack/deploy/metrics.py` → `request_metrics.py` (`297e8b8`); the gate reads the 2026-09-30 recording and has a row for the temporary bypass (`b5f195a`); runbook `§9` (alias pinning); this record; Register `§94`.
* **Unchanged:** `native_core/`, `consumers/`, `tools/`, certified evidence, ACT-004 (byte-identical since `d64b179`), acts before ACT-004, Production deployment `dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj` (`22c0b49`), Production variables (none), the Production store (0 rows).
* **Dependencies:** none added.
* **Authority boundaries:** unchanged. **Certified roots:** unchanged.
* **Protection:** SSO on (`all_except_custom_domains`). **Protection Bypass for Automation: one ACTIVE** (2026-09-30), pending revocation (`§15`).
* **Branch alias:** on `dpl_FjjGC9Hg54RGzGSugwidwHdRTrwM` (`297e8b8`) after the drill.
* **Readiness gate v3** (`python -m fullstack.readiness evaluate`, commit `297e8b8` served, recording current): **NOT PRODUCTION READY**; 26 PASS, 1 OBSERVED, 0 FAIL, **4 BLOCKED**: Scenario A (SCENARIO-A-RESIDUAL), temporary access revoked (BYPASS-REVOCATION), alerting (ALERTING-SELECTION), environment separation (E1-DEPLOYMENT-WIRING).

## 20. Exhaustion result

No work remains that is at once authorized, actionable, evidenced and within
FS-09 **and permitted in this session**: each BLOCKED row needs a Founder
decision or an execution permission this session does not have (`§22`). The
citation defect introduced by construction is repaired and re-verified; nothing
was suppressed to reach this state. Residual non-blocking items are classified
in `§22`.

## 21. Final FS-09 classification

```text
FS-09 = EXHAUSTED_WITH_CLASSIFIED_REMAINDER
FS-09 ≠ PASS          (4 gate rows BLOCKED; 0 FAIL)
FS-10 = NOT STARTED
Production = untouched; not released; not LIVE (the Production store is empty and serves nothing)
```

## 22. Remaining frontier

### 22.1 The BLOCKED rows, reconciled one by one

**A: SCENARIO-A-RESIDUAL** (*Functionality: agent creation (Scenario A)*)

| Field | Value |
|---|---|
| STATE | BLOCKED (Founder decision not taken) |
| OWNER | Founder |
| AUTHORITY | ACT-004 DG-03 ratified **A1** (no Agent creation in the Full Stack). ACT-001 `§18` makes Scenario A mandatory. No instrument classifies Scenario A under A1; ACT-005 `§7` forbids treating that silence as a decision |
| EVIDENCE | L: no route creates an Agent (`test_architecture_conformance.py`); gate row *A1: no route creates an Agent* PASS |
| BLOCKING EFFECT | prevents FS-09 PASS (one gate row) |
| NEXT ACTION | the Founder classifies Scenario A as a non-blocking residual under A1, or selects A2/A3 (which would reopen construction) |

**B: ALERTING-SELECTION** (*Observability: alerting*)

| Field | Value |
|---|---|
| STATE | BLOCKED (unresolved architecture) |
| OWNER | Founder as Architect |
| AUTHORITY | FS-DP-06 revision 2 (`5941d72`) defines H1–H3. ACT-004 `§10` selected L1/M1/R2; its *"Alerting = R2"* pairs alerting with the readiness option (R2 = readiness, `§6`). No canonical source selects an H option |
| EVIDENCE | `§5`, `§6`; Register `§91`–`§93` |
| BLOCKING EFFECT | prevents FS-09 PASS (one gate row); the runbook states alerting is unresolved |
| NEXT ACTION | the Founder as Architect selects H1 (host alerting; may cost money, D3-A), H2 (third party) or H3 (no alerting, accepted as residual); then implementation and evidence |

**C: E1-DEPLOYMENT-WIRING** (*Data: environment separation*)

| Field | Value |
|---|---|
| STATE | BLOCKED (execution permission) |
| OWNER | Founder/user (session permissions) |
| AUTHORITY | GRANTED: ACT-004 DG-04 (E1); ACT-005 `§9` requires recording, not bypassing, the denial |
| EVIDENCE | O: Production store `hmljfyqycxcueulhsjae` created, migrated with the repository's SQL, schema equal to Preview's, **0 rows** after two live suites (P). The adapter still names only the Preview project; the edit was denied (*Modify Shared Resources*) and not retried |
| BLOCKING EFFECT | prevents FS-09 PASS. A correct Production schema is not PASS, and an empty Production store is not Production LIVE |
| NEXT ACTION | the user allows the edit to `fullstack/deploy/vercel.py`: `SUPABASE_PROJECTS = {"preview": scfymftfzkpilqbgmfwv, "production": hmljfyqycxcueulhsjae}` chosen by `VERCEL_ENV`, anything else → 503; tests; a Preview check |

**D: BYPASS-REVOCATION** (*Security: temporary access revoked*; new 2026-09-30)

| Field | Value |
|---|---|
| STATE | BLOCKED (execution permission); **the bypass is active** |
| OWNER | Founder/user |
| AUTHORITY | GRANTED and required: ACT-004 `§56` (*"must be revoked afterward"*), NC-16 |
| EVIDENCE | `§15`; evidence file `access_revoked: false` |
| BLOCKING EFFECT | prevents FS-09 PASS; while active, anyone holding the secret passes Vercel SSO on Preview deployments (the API still requires the operator token for everything except health) |
| NEXT ACTION | the Founder/user revokes it in the Vercel dashboard (`§15`); then, from a session: confirm 302 with and without the old secret, set `access_revoked: true` and `after_revocation` in the evidence file (no served code changes, so the recording stays current), delete the private local copy |

### 22.2 Non-blocking and later items

| Item | Class | Who | What would close it |
|---|---|---|---|
| Live 403 (narrower principal) | non-blocking residual | Founder (operator identity) | a second Preview principal; local 403 evidence stands |
| Production key and tokens (Production scope) | FS-10 frontier | operator | set at release preparation, Production scope only |
| Performance requirement | non-blocking (not a PASS criterion, ACT-004 `§45`) | Founder | a stated requirement; figures stay OBSERVED |
| Runbook exercised in a real incident | non-blocking residual | — | occurs in operation |
