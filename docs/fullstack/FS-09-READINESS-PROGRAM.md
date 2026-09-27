# FS-09 — Production Readiness Program: Discovery, Requirements and State

| Field | Value |
|---|---|
| **Direction** | Founder, 2026-09-27: *"BEGIN FS-09 PRODUCTION READINESS"*, under `ACT-CC-POST-P13-AIOS-FULL-STACK-003`, after the FS-08 PASS (Register `§86`) |
| **Register** | `§87` (discovery); `§88` (authorized construction: this matrix updated, `§8`) |
| **Nature** | a readiness program. **Not** production release, not Founder Release Authorization, not Operational AIOS |
| **Result so far** | **FS-09 OPEN — NOT PASSED.** Authorized construction done (`§8`): gate v2, backup/restore drill, runbook, decision register. Six decisions and one verification gap remain (`§9`). FS-10 NOT STARTED |
| **Earlier record** | `FS-09-PRODUCTION-READINESS.md` (gate on `c4b9636`, before FS-08) stays as the historical first evaluation |

## 1. Canonical sources

| Source | What it requires |
|---|---|
| `ACT-CC-POST-P13-AIOS-FULL-STACK-001` `§20` | the gate: Functionality (core functions; required end-to-end scenarios), Security (authentication, authorization, secrets, attack surface, audit), Reliability (failure handling, recovery, rollback), Performance (required workload behaviour; latency/resource observations; bottlenecks), Observability (logging, metrics, tracing, alerting), Data (integrity, persistence, backup, recovery, migration), Reproducibility (clean build, reproducible deployment, known artifact). *"ALL REQUIRED CRITERIA PASS → PRODUCTION READY"*. **Exit:** evidence persisted; all blocking findings resolved; residual non-blocking findings classified; **rollback procedure verified**; release artifact identified |
| same Act `§18` | Scenarios A (Agent), B (Workflow), C (Failure) are **mandatory** end-to-end classes |
| `ACT-CC-POST-P13-AIOS-FULL-STACK-003` `§19`, `§32` | adds reliability under dependency failure, environment separation, configuration, runbook, incident handling, access control, monitoring, alerting, operational ownership; *"no unverified migrations / configuration / routes / authentication / persistence / rollback"* before release |
| `FD-FS-001` D4-A | a PASS leads to a release **package**; release waits for the Founder's decision |
| `FS-DP-01` point 6 (ratified by `FS-ARCH-RAT-001`) | free plan: no downloadable backups, so an **operator-run logical export** is the fallback; *"a restore drill is an FS-09 criterion"*. `FS-ARCH-RAT-001` `§3.3`: *"test available backup/restore mechanisms"* is authorized |
| `fullstack/readiness.py` | the executable gate. It still reflects the pre-FS-08 state (`§3`) |

## 2. Requirements matrix (the Founder's 12 items, mapped to the canonical rows)

Evidence classes: **L** local, measured now · **P** Preview live, recorded at FS-08 (commit `6469269`, historical; still covers the served code) · **O** operator-recorded on the live store · **LR** local, recorded once · **—** none yet. Updated at `§88`; the gate's own row names are in `§3`.

| # | Item · canonical rows | Current evidence | State | Gap | Authority to close it |
|---|---|---|---|---|---|
| 1 | **Functionality**: core functions (B), failure (C), **agent creation (A)** | B and C: L + P (FS-08 live: run `succeeded`, missing document → `failed` with reason). A: no route creates an Agent | B, C **PASS** · A **BLOCKED** | Scenario A needs a decision | **Architect: FS-DP-07.** If A1 (keep reserved) is chosen, Scenario A stays impossible while the Act calls it mandatory: **Founder** then decides whether it is a classified non-blocking residual |
| 2 | **Security**: authentication, authorization, secrets, attack surface, audit | L + P (FS-08: 401s, B3 token, headers, audit with no credential, append-only store) | **PASS**; 403 residual stated | 403 evidenced locally only; one principal in Preview | a live 403 needs a second, narrower Preview principal and Preview access: **Founder** (register `§2.4`, `§2.5`) |
| 3 | **Reliability**: failure handling, recovery, **rollback**, dependency failure | failure: L + P. Recovery: L + P. Concurrency (C1): P. Dependency failure: L (gate: no key → 503, unreachable store → 503). Rollback: data compatibility LR only | failure, recovery, dependency **PASS** · rollback **NOT VERIFIED (FAIL)** | a rollback drill on a deployment; floors documented (runbook `§10`) | authorized; the Preview drill needs Preview access: **Founder** (`§2.4`) |
| 4 | **Performance**: required workload, latency/resources, bottlenecks | L: ~1 ms per run in-process. P: none measured | **OBSERVED** | **no canonical workload or latency requirement exists**; none is invented | **Founder**: state a requirement, or accept OBSERVED as non-blocking (register `§2.2`). Live measurement needs Preview access |
| 5 | **Observability**: logging, metrics, tracing, alerting | tracing: L + P. Logging: the host's function log (stderr). Metrics and alerting: none | tracing **PASS** · rest **BLOCKED** | structured request log, readiness signal, alerting | **Architect: FS-DP-06** (register `§1.2`); runbook `§12` is a placeholder. Paid alerting: **Founder** |
| 6 | **Data integrity**: integrity, persistence | L (append-only bytes) + P (Supabase writes and reads; UPDATE refused) | **PASS** | — | — |
| 7 | **Backup / recovery**: backup, recovery | **O**: logical export of all 80 live records, equal to the database's digests; **L**: restored into fresh stores, byte-identical, read by the application and the API (`FS-09-BACKUP-RESTORE-DRILL.md`) | **PASS** (drill) | cadence and owner unset; no restore into a second live project | cadence/owner: **Founder** (`§2.3`). A live restore target: **Architect** (`ENVIRONMENT-SEPARATION`) |
| 8 | **Rollback** (exit criterion) | data compatibility LR (`§4`); procedure written (runbook `§9`, `§10`) | **NOT VERIFIED** | a rollback exercised on a deployment | authorized; needs Preview access (**Founder**, `§2.4`). Production rollback is Founder-only |
| 9 | **Deployment reproducibility**: clean build, reproducible deployment, known artifact | P: every push builds a READY Preview. The FS-08 Preview ran **Python 3.12** (host default, unpinned); every local run is 3.11 | known artifact **PASS** · runtime pin **BLOCKED** · reproducible deployment **BLOCKED** | the runtime version is ambiguous (FS-02 says 3.11; the host ran 3.12; 3.11 availability not established). **Not pinned** | **Architect**: `PYTHON-RUNTIME-VERSION` (register `§1.5`) and **FS-DP-03** (`§1.1`) |
| 10 | **Failure handling** | L + P (FS-08 check 12; 503 fail-closed paths; malformed key named) | **PASS** | — | — |
| 11 | **Access control** | P: 401s; one principal with all scopes. L: 403 by scope | **PASS** with the 403 residual | live 403; production operator token custody; rotation (runbook `§2`) | **Founder** (`§2.5`) |
| 12 | **Operational runbook**: runbook, incident handling, recovery, monitoring, alerting, ownership | `FS-09-OPERATIONAL-RUNBOOK.md`: all 14 required sections; checked by the gate | runbook **PASS** (written; not yet exercised in an incident) · ownership **BLOCKED** | monitoring and alerting wait on FS-DP-06; owner unset | **Founder**: `OPERATIONAL-OWNERSHIP` (`§2.3`) |
| — | **Environment separation** (ACT-003 `§19`) | Preview and a future Production would share **one** Supabase project and **one** `aios_records` table; 80 FS-08 records are already in it and can never be removed | **BLOCKED** | production data would mix with Preview test data | **Architect**: `ENVIRONMENT-SEPARATION` (register `§1.4`, options E1–E6). Nothing created |
| — | **Migration** | L: 1 migration in the repository; O: the same 1 applied on the live store (re-checked 2026-09-27) | **PASS** for the current schema | never replayed on a second environment | follows environment separation |
| — | **Release artifact identified** (exit) | commits are known; no candidate chosen yet | pending | fixed when the gate passes | — |

## 3. The executable gate, as it reads today

*At discovery (`§87`)* the gate measured only in-process and showed FAIL for
authentication, deployment rollback and production persistence/backup/migration,
because it could not see the FS-08 live evidence.

*Gate v2 (`§88`)*: `python -m fullstack.readiness evaluate` → **NOT PRODUCTION
READY**. Each criterion names its evidence class. A criterion that needs the
deployment passes only on the recorded Preview checks it names, and only while
the code the Preview serves is unchanged since commit `6469269` (checked with
`git diff` on every run; unchanged today). The recording is never re-labelled as local.

| Status | Criteria |
|---|---|
| **PASS** (18) | Scenario B · Scenario C · authentication · authorization (403 residual) · secrets · attack surface · audit · failure handling · dependency failure · recovery · concurrent identities (C1) · tracing · integrity · persistence · backup and restore · migration · runbook · known artifact |
| **OBSERVED** (1) | performance (local latency; no requirement) |
| **FAIL** (1) | rollback of a deployment: NOT VERIFIED |
| **BLOCKED** (6) | Scenario A (FS-DP-07) · logging/metrics/alerting (FS-DP-06) · environment separation (ENVIRONMENT-SEPARATION) · operational ownership (OPERATIONAL-OWNERSHIP) · runtime version pinned (PYTHON-RUNTIME-VERSION) · reproducible deployment (FS-DP-03) |

## 4. Rollback data compatibility (verified in this discovery)

The pre-C1 code (`6e31092`) was run against a store written by the current
code (`fullstack.run/2`):

| Step | Result |
|---|---|
| old code lists and reads new-format runs by id | yes |
| old code appends its own `fullstack.run/1` run | yes, distinct id |
| current code, rolled forward, reads the mixed store and resolves every run's Trace | yes |

**Runbook constraint:** a rollback **below** `0706446` (C1) brings back
duplicate run ids under concurrency. One below `215248f` (B3) brings back an
API that authenticates nobody. The rollback floor for any release is the
release candidate itself.

## 5. Authorized construction, in order (status at `§88`)

| # | Action | Authority | Status |
|---|---|---|---|
| A1 | Readiness gate v2: evidence classes; recorded live evidence recognized, never relabelled | ACT-003 `§4.4` | **done** (`§3`) |
| A2 | Backup and restore drill | `FS-DP-01` point 6; `FS-ARCH-RAT-001` `§3.3` | **done**: `FS-09-BACKUP-RESTORE-DRILL.md` |
| A3 | Operational runbook | ACT-003 `§18` | **done**: `FS-09-OPERATIONAL-RUNBOOK.md` (monitoring and alerting are placeholders pending FS-DP-06) |
| A4 | Rollback procedure and a **Preview** drill | ACT-003 `§18`, `§25` | procedure **done** (runbook `§9`, `§10`); drill **not run**: needs Preview access (**Founder**) |
| A5 | Pin the Python runtime version | ACT-003 `§12` | **stopped at the ambiguity**: FS-02 says 3.11, the host ran 3.12, 3.11 availability not established. Nothing pinned (`FS-09-DECISION-REGISTER.md` `§1.5`) |
| A6 | Live Preview performance observation | needs Preview access: **Founder** | not run |

## 6. Decisions surfaced

Recorded in full, with question, source, authority, options, impact and
blocker status, in **`FS-09-DECISION-REGISTER.md`**. No option is chosen there.

**Architect:** FS-DP-03 Networking · FS-DP-06 Observability · FS-DP-07 Agent
creation · ENVIRONMENT-SEPARATION · PYTHON-RUNTIME-VERSION.

**Founder:** Scenario A as a residual (if FS-DP-07 = A1) · a performance
requirement · operational ownership (including backup cadence) · live access
for FS-09 checks · operator identities · spending · release (not due).

## 7. Evidence already available from FS-08

`docs/fullstack/evidence/FS-08-LIVE-PREVIEW-2026-09-27.json` (14 of 14 PASS)
and `FS-08-FINAL-RECONCILIATION-GATE.md`. They cover authentication,
authorization (grant and anonymous refusal), secrets, headers, audit, Trace,
persistence and read-back, concurrency, failure paths, append-only
enforcement, and reproducible Preview builds.

## 8. Authorized construction (`§88`)

| Workstream | Delivered | Evidence |
|---|---|---|
| A — gate v2 | `fullstack/readiness.py`: evidence classes `local-current`, `preview-recorded`, `operator-recorded`, `local-recorded`; the FS-08 file read, never written; a stale recording or a missing check fails the criterion; the drill re-run on each evaluation; the runbook's sections checked | `fullstack/tests/test_readiness.py` (23 tests; mutation-checked) |
| B — backup/restore | `fullstack/deploy/backup.py` (format `fullstack.backup/1`); `backup-restore` and `backup-verify` in `python -m fullstack.backend`; the live export and manifest | `FS-09-BACKUP-RESTORE-DRILL.md`; `docs/fullstack/evidence/FS-09-BACKUP-*.json*`; `fullstack/tests/test_backup_restore.py` (23 tests; mutation-checked) |
| C — runbook | `FS-09-OPERATIONAL-RUNBOOK.md`, 14 sections, both rollback floors stated as not production-safe | the gate's runbook row |
| D — runtime pin | not pinned; the ambiguity recorded | decision register `§1.5` |
| E — decisions | `FS-09-DECISION-REGISTER.md` | — |

Production untouched. No project, database or table created. No secret in any file.

## 9. Exact blockers to FS-09 PASS

1. **FS-DP-03** ratified (Architect), then verified on the Preview.
2. **FS-DP-06** ratified (Architect), then implemented and verified.
3. **FS-DP-07** decided (Architect); if A1, the Founder classifies Scenario A as a residual.
4. **ENVIRONMENT-SEPARATION** decided (Architect), then implemented, with the migration replayed and a restore drill on the new target if one is created.
5. **PYTHON-RUNTIME-VERSION** decided (Architect), then pinned and the Preview re-verified on it.
6. **OPERATIONAL-OWNERSHIP** decided (Founder), including backup cadence.
7. **Rollback verified** on a deployment: a Preview drill, which needs a Founder-authorized temporary Preview access.
8. The performance position (Founder): a requirement to measure, or OBSERVED accepted as non-blocking.
9. The residuals classified as non-blocking at the gate: the live 403, dependency failure exercised in-process only, and the runbook not yet exercised in an incident.

FS-09 remains **OPEN**. FS-10 remains **NOT STARTED**.
