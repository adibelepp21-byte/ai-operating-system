# FS-09 — Production Readiness Program: Discovery, Requirements and State

| Field | Value |
|---|---|
| **Direction** | Founder, 2026-09-27: *"BEGIN FS-09 PRODUCTION READINESS"*, under `ACT-CC-POST-P13-AIOS-FULL-STACK-003`, after the FS-08 PASS (Register `§86`) |
| **Register** | `§87` |
| **Nature** | a readiness program. **Not** production release, not Founder Release Authorization, not Operational AIOS |
| **Result so far** | **FS-09 NOT PASSED.** Discovery and classification complete; construction not started |
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

Evidence classes: **L** local · **P** Preview (live) · **—** none yet.

| # | Item · canonical rows | Current evidence | State | Gap | Authority to close it |
|---|---|---|---|---|---|
| 1 | **Functionality**: core functions (B), failure (C), **agent creation (A)** | B and C: L + P (FS-08 live: run `succeeded`, missing document → `failed` with reason). A: no route creates an Agent | B, C **PASS** · A **BLOCKED** | Scenario A needs a decision | **Architect: FS-DP-07.** If A1 (keep reserved) is chosen, Scenario A stays impossible while the Act calls it mandatory: **Founder** then decides whether it is a classified non-blocking residual |
| 2 | **Security**: authentication, authorization, secrets, attack surface, audit | L + P (FS-08: 401s, B3 token, headers, audit with no credential, append-only store) | **PASS** except the 403 residual | 403 evidenced locally only; one principal in Preview | authorized to verify. A second, narrower Preview principal is operator configuration: **Founder** to allow |
| 3 | **Reliability**: failure handling, recovery, **rollback**, dependency failure | failure: L + P. Recovery: L (restart) and P (a later Runtime reads the run). Dependency failure: L (no key or unreachable store → 503). Rollback: **data-compatibility tested now (L, `§4`)** | partial | a **verified rollback procedure** on a deployment (exit criterion) | authorized: procedure plus a Preview redeploy drill (`§5` A4) |
| 4 | **Performance**: required workload, latency/resources, bottlenecks | L: ~1 ms per run in-process. P: none measured | OBSERVED | **no workload requirement exists** anywhere in the canonical sources | authorized to measure on Preview. **Founder** to state a requirement, or accept OBSERVED as non-blocking |
| 5 | **Observability**: logging, metrics, tracing, alerting | tracing: L + P. Logging: the host's runtime log captures stderr (used in FS-08 diagnosis). Metrics and alerting: none | tracing **PASS** · rest **BLOCKED** | structured request log, readiness signal, alerting | **Architect: FS-DP-06** (unratified). Paid alerting is a spending decision (**Founder**, D3-A) |
| 6 | **Data integrity**: integrity, persistence | L (append-only bytes); P (Supabase writes and reads; UPDATE refused by trigger) | **PASS** | — | — |
| 7 | **Backup / recovery**: backup, recovery | none on the live store | **NOT VERIFIED** | a logical-export backup and restore drill | **authorized** (`FS-DP-01` point 6; `FS-ARCH-RAT-001` `§3.3`). The free plan has no downloadable backups and pauses after 7 days of low activity: a paid plan is a **Founder** spending decision |
| 8 | **Rollback** (exit criterion) | data compatibility L (`§4`) | **NOT VERIFIED** | procedure plus a drill | authorized (`§5` A4) |
| 9 | **Deployment reproducibility**: clean build, reproducible deployment, known artifact | P: every push builds a READY Preview from its commit (`0706446` … `25b70a5`). No build step | partial | Python runtime not pinned; networking rules unratified | **Architect: FS-DP-03** (the readiness gate blocks this row on it). Pinning the runtime version is configuration (ACT-003 `§12`) |
| 10 | **Failure handling** | L + P (FS-08 check 12; 503 fail-closed paths; malformed key named) | **PASS** | — | — |
| 11 | **Access control** | P: 401s; one principal with all scopes. L: 403 by scope | partial | live 403; who holds operator tokens in production; rotation | a second Preview principal: **Founder**. Custody of the production operator token (who holds it, how it is delivered without chat): **Founder** |
| 12 | **Operational runbook**: runbook, incident handling, recovery, monitoring, alerting, ownership | fragments only (`fullstack/README.md`) | **ABSENT** | a runbook | authorized to write. Its monitoring and alerting sections wait on FS-DP-06. **Operational ownership** (who is on call) is a **Founder** matter |
| — | **Environment separation** (ACT-003 `§19`) | Preview and a future Production would share **one** Supabase project and **one** `aios_records` table. The FS-08 test runs are already in it | **GAP (material)** | production data would mix with Preview test data | **Architect**: separation changes the ratified persistence arrangement (FS-DP-01: *"the existing AIOS Supabase project provides persistence"*). A second project costs nothing on the free plan, but adding one is still a decision. Not decided here |
| — | **Migration** | 1 migration in the repository = 1 applied (`20260927062422_aios_records`) | **PASS** for the current schema | no second environment to replay it on | follows environment separation |
| — | **Release artifact identified** (exit) | commits are known; no candidate chosen yet | pending | fixed when the gate passes | — |

## 3. The executable gate, as it reads today

`readiness.evaluate` on the current tree: **NOT PRODUCTION READY**. It awaits
FS-DP-03, FS-DP-06 and FS-DP-07. It shows FAIL for authentication, deployment
rollback, and production persistence/backup/migration, because it measures
only in-process and cannot see the FS-08 live evidence. Correcting that
(`§5` A1) is construction, not a change of standard: a row may pass only on
recorded live evidence, labelled as such.

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

## 5. Authorized construction, in order (the next actions)

| # | Action | Authority |
|---|---|---|
| A1 | Readiness gate v2: map its criteria to `§2`. Let a criterion pass on **recorded live evidence** (with its class) where it cannot be measured in-process. Keep BLOCKED where a decision is missing | ACT-003 `§4.4` |
| A2 | Backup and restore drill: logical export of `aios_records` through operator tooling; restore into a fresh store; the application reads identical runs, Trace and audit; the procedure recorded | `FS-DP-01` point 6; `FS-ARCH-RAT-001` `§3.3` |
| A3 | Operational runbook: deploy, verify, roll back, backup and restore, key and token rotation, incident steps, health checks. Monitoring and alerting marked pending FS-DP-06 | ACT-003 `§18` |
| A4 | Rollback procedure and a **Preview** drill (redeploy an earlier build and verify, then return) | ACT-003 `§18`, `§25` |
| A5 | Pin the Python runtime version for reproducible builds | ACT-003 `§12` (configuration) |
| A6 | Live Preview performance observation (latency, cold start) | needs Preview access: **Founder** (`§6`) |

## 6. Decisions surfaced

**Architect-reserved** (stop at the boundary; packages exist):

1. **FS-DP-03 Networking**: one origin, AIOS never addressable, the browser never reaches the database, backend egress only to the database; TLS/HSTS by the host; default domain first. This matches what is deployed, but is unratified.
2. **FS-DP-06 Observability**: telemetry separate from Trace and audit; one structured JSON log line per request; a readiness signal; alerting through the host or an external uptime check.
3. **FS-DP-07 Agent creation**: A1 keep reserved (Scenario A stays blocked) · A2 instance registration only · A3 full Agent Factory.
4. **Environment separation** (new, no package yet): how Production's data is kept apart from Preview's in the ratified Supabase arrangement.

**Founder-reserved:**

1. **Scenario A**: if FS-DP-07 = A1, whether a mandatory scenario may stand as a classified non-blocking residual.
2. **Performance requirement**: state one, or accept OBSERVED as non-blocking.
3. **Spending** (D3-A): paid alerting; a paid Supabase plan for downloadable backups and no pause-on-inactivity.
4. **Live access for FS-09 Preview checks**: the FS-08 bypass was scoped to that suite and revoked. FS-09 live checks (performance, 403, rollback drill) need a new, equally temporary authorization.
5. **Operator identity**: a second, narrower Preview principal for a live 403; custody and delivery of the production operator token; operational ownership (who responds to incidents).

## 7. Evidence already available from FS-08

`docs/fullstack/evidence/FS-08-LIVE-PREVIEW-2026-09-27.json` (14 of 14 PASS)
and `FS-08-FINAL-RECONCILIATION-GATE.md`. They cover authentication,
authorization (grant and anonymous refusal), secrets, headers, audit, Trace,
persistence and read-back, concurrency, failure paths, append-only
enforcement, and reproducible Preview builds.
