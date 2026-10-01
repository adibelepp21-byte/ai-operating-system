# FS-09 — AIOS Full Stack Operational Runbook

| Field | Value |
|---|---|
| **Authority** | `ACT-CC-POST-P13-AIOS-FULL-STACK-003` `§18`, `§19`; the Founder's FS-09 continuation (Workstream C) |
| **Register** | `§88` (written); `§93` (updated to the ACT-004 decisions and FS-09 live state); `§94` (2026-09-30 re-verification, alias pinning) |
| **Scope** | the deployed AIOS Full Stack: Vercel project `aios-platform` (static console and `/api/v1/*` Python function) over Supabase project `scfymftfzkpilqbgmfwv`, table `aios_records` |
| **Status** | **current as of 2026-09-30 (ACT-004 to ACT-007).** Checked against the code and the FS-09 live verification; not yet exercised in a real incident. Logging, metrics and readiness (`§12`) are implemented; **alerting is H3 (none; manual checks, `§12.1`)**, a delegated decision (Register `§98`). Duties (`§13`) follow `FS-09-OPERATIONAL-OWNERSHIP.md`. *History: until `§93` this row said monitoring and alerting were placeholders and ownership was unassigned* |
| **Is not** | a release, a Production procedure the operator may run on their own, or a readiness PASS |

**Rules for every step.** No secret value goes into chat, a commit, a document,
a log line, a screenshot or an evidence file. Production (deployment, alias,
variables, credentials) changes only on a Founder decision (`FD-FS-001` D4-A).
Vercel SSO protection is never bypassed except by a Founder-authorized,
temporary mechanism that is revoked afterwards. The store is append-only: no
step edits or deletes a record.

## 1. Startup and health

The function has no long-running process. Every request starts its own AIOS
Runtime on the store and stops it before answering (`FS-DP-04` A1). "Startup"
therefore means *a request can start a Runtime*.

| Check | How | Healthy |
|---|---|---|
| Deployment built | Vercel deployment status | `READY`; build log names the commit |
| Function and store | `GET /api/v1/health` (public route) | `200 {"status":"ok","runtime_state":"running"}` |
| Authenticated read | `GET /api/v1/runtime` with `Authorization: Bearer <operator token>` | `200`, `state: running`, a new `runtime_id` on every call |
| Console | `GET /` | `200 text/html`; `app.js`, `api.js` load |
| Readiness gate (local) | `python -m fullstack.readiness evaluate` | JSON; see `docs/fullstack/FS-09-READINESS-PROGRAM.md` |
| Runtime | the build log | *"Using Python 3.12 from .python-version"* (`FS-09-RUNTIME` P2) |
| Request log | Vercel runtime logs, query `fullstack.request/1` | one line per request (`§12`) |

Edge protection (`FS-DP-03` N1, form X2) is a project setting held by the
operator: Vercel login protection on every deployment URL
(`all_except_custom_domains`). An unauthenticated request gets `302`/`401`
**from Vercel** before AIOS runs: protection working, not a fault. Check the
setting before trusting either behaviour. *History: it was observed off on
2026-09-27 19:57Z (EXT-06), an accidental change the Founder corrected (Register
`§90`); it was on throughout the FS-09 live verification.*

## 2. Authentication failure

Mechanism: `FS-DP-02` B3 operator bearer tokens. The host holds only SHA-256
hashes, in `AIOS_OPERATOR_TOKENS`.

| Symptom | Meaning | Action |
|---|---|---|
| every protected route `401`, `/health` `200` | the token is wrong, or `AIOS_OPERATOR_TOKENS` is absent or refused | check the function log for `AIOS_OPERATOR_TOKENS <reason>; nobody is authenticated`. The reason names the fault (not JSON, an unknown key, a bad hash), never a value |
| one principal `401`, others `200` | that token's hash is not in the configuration | issue a new token (`python -m fullstack.backend operator-token …`, on the operator's own machine) and replace that entry |
| `403` | authenticated, but the scope is missing | intended least privilege; grant the scope only if the principal's role needs it |
| `409` | `POST /api/v1/agent-instances` named an instance key already registered | intended: a registration is append-only and unique by key; choose another key. A registration cannot be edited or retracted (`fullstack/backend/agents.py`) |
| token suspected exposed | — | **incident** (`§11`): remove its entry, redeploy so the function reads the new value, issue a replacement, and check the audit (`§6`) for its subject |

Rotation: add the new entry, redeploy, confirm the new token works, remove the
old entry, redeploy. The plaintext token is shown once and stored nowhere by AIOS.

## 3. Dependency failure

The function has two dependencies: the Supabase REST endpoint and the
server-side key. It fails closed. There is no filesystem fallback.

| Response (`503 unavailable`) detail | Log line (function) | Cause | Action |
|---|---|---|---|
| *persistence is not configured: the operator has not set the server-side database key* | — | no `SUPABASE_SECRET_KEY` / `SUPABASE_SERVICE_ROLE_KEY` in this environment | the operator sets it (sensitive) and redeploys. Claude never reads or creates it |
| *…contains a character that cannot be sent…; enter it again as one line* | `storage not configured: …` | the key was pasted with a line break, space, quote or non-ASCII character | re-enter it as one line; redeploy |
| *the AIOS Runtime could not start on its store* | `runtime start failed: StorageUnavailable: …` | Supabase unreachable, key rejected, or project paused (free plan pauses after 7 days of low activity) | check Supabase project status; restore a paused project from the Supabase dashboard; check the key is the project's current secret key |

Verified in-process by the readiness gate (*dependency failure fails closed*);
not induced on the live store.

## 4. Persistence failure

| Symptom | Check | Action |
|---|---|---|
| a run was created (`201`) but is missing later | `select count(*) from aios_records where partition = 'fullstack-runs'` via operator SQL | compare with the audit entry of that request (`§6`). A missing record after a `201` is a data-loss incident (`§11`) |
| `503` after start | function log `request failed after start` with a traceback | the append or read failed mid-request. Nothing is partially updated: records are appended whole or not at all |
| an attempt to change a record | the database refuses: *aios_records is append-only: UPDATE refused* | intended (triggers refuse UPDATE, DELETE and TRUNCATE). Never disable them |
| schema drift | `list_migrations` on the project against `fullstack/deploy/supabase/migrations/` | they must match (today: `20260927062422_aios_records`) |

## 5. Failed execution

A Workflow run that fails is a **state, not an error**: `201` with
`state: "failed"` and a `failure_reason` naming the Tool's reason (for example,
a missing document). Nothing is left `running`.

| Response | Meaning |
|---|---|
| `201`, `state: failed` | the run executed and failed; read `failure_reason` and `steps` |
| `400` | the request was invalid (unknown workflow, bad inputs); no run was created |
| `404` on `/runs/{id}` | no such run |
| `503` | not an execution failure: see `§3` or `§4` |

## 6. Trace and audit investigation

| Question | Where |
|---|---|
| what did a run do | `GET /api/v1/runs/{run_id}`: `steps`, `states`, `outcome`, `failure_reason` |
| which Trace records are the run's | the run's `trace` = `{runtime, runtime_from, runtime_to, count}`: its Runtime's own records, by ordinal (`FS-DP-05` C1). In code, `AIOSApplication.run_trace(run_id)`. Legacy `fullstack.run/1` runs keep a global range |
| who did what, allowed or refused | `GET /api/v1/audit` (scope `aios.audit`): `subject`, `method`, `path`, `scope`, `decision`, `status`, `request_id`. Anonymous refusals have `subject: null` |
| correlate a response with the audit and the log | the `X-Request-Id` response header = the audit entry's `request_id` = the L1 line's `request_id` |
| raw store | operator SQL: `select seq, partition, convert_from(record, 'UTF8') from aios_records order by seq` |

No credential is ever written to Trace or audit. If one is found, that is an incident (`§11`).

## 7. Backup

The free Supabase plan offers no downloadable backup (`FS-DP-01` point 6). The
backup is an **operator-run logical export** in the `fullstack.backup/1` format
(`fullstack/deploy/backup.py`).

1. Record the live digests (read-only):
   ```sql
   select partition, count(*), sum(octet_length(record)), min(seq), max(seq),
          encode(sha256(string_agg(record, '\x0a'::bytea order by seq)), 'hex')
   from aios_records group by partition;
   ```
2. Export every row in `seq` order (`select seq, partition, record from aios_records order by seq`)
   and write one `fullstack.backup/1` line per row (`backup.line_for`), with
   `position` counted per partition.
3. Check the export: `backup.summary(backup.read_file(<file>))` must give the
   same count, bytes and joined digest per partition as step 1.
4. Scan the file for credentials (the operator token, the Supabase secret-key prefix, a JWT prefix,
   `Bearer`); there must be none. Keep it with a manifest (source, time, digests,
   the file's own SHA-256), as in `docs/fullstack/evidence/FS-09-BACKUP-MANIFEST-2026-09-27.json`.

Drilled on 2026-09-27 on the Preview store: 80 records, every partition and the
whole table equal to the database's digests. **Per environment** (`FS-09-ENV` E1):
the Preview store `scfymftfzkpilqbgmfwv` and the Production store
`hmljfyqycxcueulhsjae` are exported separately and never mixed. Cadence,
retention and who runs it: `FS-09-OPERATIONAL-OWNERSHIP.md` `§4`. *History:
until `§93` these were unset.*

## 8. Restore

A restore makes a **fresh** store; it never merges into one that already holds
the exported partitions (the tool refuses).

```bash
python -m fullstack.backend backup-restore --export <file.jsonl> --data-dir <new empty dir>
python -m fullstack.backend backup-verify  --export <file.jsonl> --data-dir <that dir>
python -m fullstack.backend serve --data-dir <that dir>        # read it through the API
```

`backup-restore` exits `0` and prints `"identical": true` with the per-partition
digests, which must equal the manifest's. Then check that the runs, each run's
Trace and the audit read back (`fullstack/tests/test_backup_restore.py` does
exactly this, on every regression run).

**Boundary.** A restore makes a fresh store of the **same** environment. A
Preview export is never restored into the Production project, nor the reverse
(ACT-004 `§15`). Restoring *into* a store that still holds the partitions is
refused by design, and nothing may delete them. *History: until `§93` a live
second target waited on the environment-separation decision.*

## 9. Rollback

What rollback means here: serving an **earlier deployment's code** over the
**same** store. The store itself is never rolled back (append-only; no step deletes).

| Environment | Procedure | Who |
|---|---|---|
| Preview | redeploy the earlier commit's build (Vercel: redeploy that deployment, or push a revert to the branch), then run `§1` and a Scenario B and C run | operator; any live check needs Preview access (`EXT-03`) |
| Production (**current**, `FDP-009` `§8`, `FDP-010-02`; Register `§107`, `§109`) | Vercel Instant Rollback (`request_rollback`) to the **designated verified known-good target** only (`FS-10-CURRENT-AUTHORITY.md` `§3`); never `22c0b49` (`FDP-010` `§6.1`); never to an unverified deployment | the **CEO**, when operationally necessary, before or after a release, with evidence preserved; no governance, certified-architecture or deployment-architecture change. A rollback is not a release (`FDP-010` `§9`). Without a valid target: preserve evidence, classify, contain (`§11`), escalate (`FDP-010` `§8`) |
| *History (FS-09, superseded for current operation by `FDP-009`/`FDP-010`):* Production | Vercel Instant Rollback / promote an earlier deployment | **Founder only** (`FD-FS-001` D4-A). Never used to gain evidence |

After any rollback: `§1` health, one Scenario B run and one Scenario C run,
then compare `GET /runs` before and after. Every earlier record must still read.

**Status: drilled on Preview, 2026-09-28** (`FS-09-ACT-005-EXECUTION-RECORD.md`
`§14`): the branch alias moved from `dpl_8Znqrn818NgYy66RU7hz819t4ZTj`
(`a4a11cf`) to `dpl_EJJbGcdvDEfm4b2JQE14d1uaN2Xc` (`d64b179`) and back. Each
version read the other's records, served Scenarios B and C, kept the B3
posture (anonymous 401) and the same store and variables. A rollback below the
L1 commit loses request logs. Production rollback has not been exercised: it
is the operator's, on a Founder decision. *History: until `§93` this read NOT
VERIFIED.*

**Drilled again, 2026-09-30** (`§94`): from `dpl_FjjGC9Hg54RGzGSugwidwHdRTrwM`
(`297e8b8`) back to `dpl_6xyzjXKxqcLkVdxHZ9QnXYQ46CZ4` (`7df974a`) and forward;
same results (evidence `FS-09-LIVE-PREVIEW-2026-09-30.json`).

**Final drill, 2026-09-30 (ACT-008 `§13`)**, on the commit the gate covers
(`d05261c`, `dpl_EJucmiuLbgmgX1ar7SDZ25Ngp3ER`): current → rolled back to
`dpl_Gumff1FYuJP3L5agQrGtcwGqyY19` (`d6afbdc`) → rolled forward. Each phase was
reachable (`/health` 200, anonymous 401), read a run written by the other
version, and accepted a Scenario B run and a Scenario C run. Rolled back, the
A2 routes answered 404, which proves which code served; the five Agent
Instance registrations stayed in the store, unread there and read again after
the roll-forward. The alias was left on the final deployment. This shows **data
compatibility**; **operational safety** is the table in `§10`, unchanged by it.

**A manually assigned alias stays pinned.** After `vercel alias` / an alias
assignment, the branch alias no longer follows new pushes to the branch: on
2026-09-30 it still served `dpl_8Znqrn818NgYy66RU7hz819t4ZTj` (`a4a11cf`) two
commits later. After a rollback drill, re-assign the alias to the newest
deployment, and before any check through an alias, read which deployment it
serves (`list_deployment_aliases`, or the `dep=` field of the runtime log).

## 10. Rollback compatibility boundaries

Data compatibility, verified at FS-09 discovery: the pre-C1 code (`6e31092`)
lists and reads `fullstack.run/2` records and appends its own
`fullstack.run/1`; the current code reads the mixed store and resolves every
run's Trace. **Data compatibility does not make a rollback target safe.**

| Rolling back below | Consequence | Production-safe? |
|---|---|---|
| `0706446` (`FS-DP-05` C1) | **reintroduces the historical concurrency risk**: two Runtimes can give runs the same id, and a run's Trace range can include another run's records | **No** |
| `215248f` (`FS-DP-02` B3) | **changes the authentication posture**: the function builds no authenticator from `AIOS_OPERATOR_TOKENS`, so the API authenticates nobody (every protected route `401`) | **No** |
| `207ee77` | a malformed key is no longer named; the function fails with a generic 503 | degraded diagnosis |
| `200bd81` (`FS-DP-07` A2) | the `/agent-definitions` and `/agent-instances` routes do not exist (404) and the console has no Agents view; registrations stay in the store, unread | degraded: Scenario A is unavailable |
| `a4a11cf` (`FS-DP-06` L1) | no request log lines; Trace, audit and data unaffected | degraded observability |
| `8d088fb` (`FS-DP-01` store, `FS-DP-04` function) | no API function and no Supabase store: `/api/v1/*` does not exist, only static files are served | **No** |

**The rollback floor for any release is the release candidate itself.** A
target below a floor is not a rollback option, whatever its data compatibility.
Production today serves `22c0b49` (before this program); it is not a candidate
and is not changed by this runbook.

## 11. Incident handling

1. **Detect**: a failed `§1` check, a user report, or (after `FS-DP-06`) an alert.
2. **Classify**: availability (`§3`), authentication (`§2`), data (`§4`),
   execution (`§5`), or security (credential exposure, unexpected audit subject,
   protection disabled).
3. **Contain**, without deleting anything:
   * credential exposure: remove the entry or rotate the key, redeploy;
   * suspected bad release: stop promoting; a Production rollback is the Founder's call (`§9`, `§10`);
   * data: take a backup now (`§7`) before any other action.
4. **Investigate** with `§6`, and record the `request_id`s, run ids and times.
5. **Recover**: redeploy, rotate, restore into a fresh store for analysis (`§8`).
6. **Record**: an incident note under `docs/fullstack/` with the timeline, the
   evidence (no secret) and the decision taken; a Register entry when a decision
   was needed.

## 12. Monitoring and alerting

`FS-DP-06` as decided by ACT-004 DG-02 (Register `§93`): **L1 / M1 / R2**.
Trace and audit are unchanged and separate.

| Signal | Mechanism | Where |
|---|---|---|
| request log (L1) | one `fullstack.request/1` JSON line per request: time, `request_id`, method, route **template**, status, latency, `runtime_id`. Never a credential, body or raw path. Refusals before the Application (503) are logged too, with `runtime_id: null` | Vercel runtime logs (stdout); query `fullstack.request/1` |
| metrics (M1) | derived from L1 lines: request count, status classes, server errors, p50/p95/max latency, per route | `python -m fullstack.backend metrics --log <exported log>` |
| readiness (R2) | deployed `GET /api/v1/health` = 200 only after a Runtime started on the store; 503 otherwise | `§1` |
| alerting | **H3: none; manual checks** (Register `§98` `ACT-007-DG-02`, delegated under ACT-007). No automatic alert exists. R2 is readiness, not alerting. Failures are found by the checks in `§12.1` | `§12.1` |
| backup freshness | the date of the latest export manifest (`§7`) | the evidence directory |

### 12.1 Manual monitoring checks (H3)

There is no alert: nobody is paged, and nothing watches the service between
checks. These are the checks that stand in for one. **Residual: a failure is
found only when a person runs them** (`FS-DP-06` `R2.10`). Choosing H1 or H2
later needs the Founder's decisions on spending or an external service, on who
receives alerts, and (H2) on an edge path to `/health` that protection X2
denies; it supersedes this section.

| Check | How | A problem looks like | Then |
|---|---|---|---|
| readiness (R2) | `GET /api/v1/health` (`§1`) | anything but 200 `{"status":"ok","runtime_state":"running"}` | `§3` dependency failure, `§4` persistence failure |
| error rate (M1) | export the runtime log for the deployment (query `fullstack.request/1`), then `python -m fullstack.backend metrics --log <export>`; read `total.server_errors` and `status_classes` | `server_errors` above 0, or 4xx rising without a cause | `§11` incident handling |
| refusals before the Application | L1 lines with `runtime_id: null` and status 503 | any | `§3`, `§4` |
| backup freshness | the date of the latest export manifest (`§7`) | older than the last store change that matters | `§7` |
| temporary access | the Protection Bypass for Automation list in Vercel (Deployment Protection) | any entry not under a current Act | revoke it; `§14` |

**When:** on every verification by the executor, before and after any deploy,
rollback or restore, and by the operator at will. No schedule is imposed.
**Who:** as `FS-09-OPERATIONAL-OWNERSHIP.md` `§6`. **Not an alert:** R2 tells a
person who asks; it never tells anyone unasked.

Verified live on 2026-09-28: all 45 function requests of the FS-09 suite appear
in the host log with their `request_id`; metrics derived from those lines. The
host's own access line (`127.0.0.1 - - … "GET /api/v1/runs/run-…"`) shows raw
paths; it is the host's, not AIOS telemetry. *History: until `§93` this section
was a placeholder.*

## 13. Operator responsibilities

Defined in `FS-09-OPERATIONAL-OWNERSHIP.md` (ACT-004 `§37`): the Founder is the
operator of record and custodian of every credential; Claude Code is a
delegated executor only while an Act authorizes it. The duties:

* hold operator tokens off the repository and issue, rotate and revoke them (`§2`);
* hold each environment's Supabase key and set it on the host in its own scope only (`§3`);
* run `§1` after every deployment and before any release decision;
* take backups (`§7`) at the defined cadence, per environment, without credentials;
* keep both Supabase projects from pausing, or restore them;
* handle incidents (`§11`) and escalate (`§14`).

*History: until `§93` these were unassigned.*

## 14. Escalation boundaries

*Current since 2026-10-01: `FDP-009` (Register `§107`) and the ACT-009 classification (`FS-10-ACT-009-AUTHORITY-BOUNDARY-RECORD.md`). The table is updated in place; the rows it replaced are listed under it.*

| Matter | Decided by | Never done without that decision |
|---|---|---|
| Production deployment of the release candidate, roll-forward, rollback before a release | **CEO**, for verification only (`FDP-009-01`, `§8`) | treating a deployment as a release |
| Production release, LIVE, traffic | **Founder** (`FDP-009` `§5.3`, `§5.4`, `§10`; ACT-003 `§21`) | any release or LIVE claim |
| Production database key, Production variables, provider settings | **account holder** (external control: ACT-001 `§7.1`; ACT-003 `§13`, `§28`) | a credential passing through the session |
| permanent Production principals; rollback after a release | **UNKNOWN**, escalated (`ESC-01`, `ESC-02`) | acting on either |
| spending: paid plans, alerting, backups | **Founder** (D3-A) | any purchase or upgrade |
| temporary access past Vercel SSO | Preview: per authorizing Act. Production verification: **CEO under `FDP-009-03`** (14 conditions) | any bypass outside those; it is revoked after use and the revocation verified |
| operational ownership, backup cadence, incident owner | **CEO** (ACT-004 `§37`; ACT-009 rows O1, R, X3) | changing a Founder decision through them |
| a performance requirement | **Founder** | treating any latency as a pass/fail requirement |
| networking, observability, Agent creation, environment separation, runtime | decided by ACT-004 (Register `§93`); implemented under ACT-004/005 | changing those decisions |
| replacing H3 by H1 or H2 (`FS-DP-06`): spending, an external service, who receives alerts, an edge path | **Founder** (H3 was selected by delegation, Register `§98`) | treating R2 as an alert, or adding a monitor, a paid alert or an edge path on the delegation's strength |
| architecture beyond the ACT-004 decisions | **Architect** | a second project or table; pinning a version |
| changes to certified roots P10–P13, Phase 14 | not open | — |

*Replaced rows (until 2026-10-01):* Production deploy, promote, rollback, alias, variables, credentials → *Founder (`FD-FS-001` D4-A; ACT-003)*; temporary access past Vercel SSO → *Founder, per occasion*; operational ownership, backup cadence, incident owner → *Founder*.


## 13. Agent Instances (FS-DP-07 A2)

Scope `aios.agent.register` is held by the operator principal only; an observer
gets `403`. A registration names an existing governed Definition, an instance
key and capabilities the Definition implements, and is stored in the
append-only partition `fullstack-agents`. It **grants no authority**
(`grants_authority: false`): it is an identity, not a permission. The
application never creates, edits or retires a Definition; that stays with the
owning Platform Division (A3 is not built). Because nothing in the store is
deleted, a mistaken registration stays visible; correct it by registering a
new key and recording the reason in the Register. To add the scope to a
deployed principal, edit `AIOS_OPERATOR_TOKENS` (hash, subject, scopes) in
the Vercel scope of that environment and redeploy; never put the token itself
in a file.

## 15. Production operational principal (`FDP-010-01`)

Current authority: `FS-10-CURRENT-AUTHORITY.md` (`FDP-009` + `FDP-010`).

| Item | Rule |
|---|---|
| Principal | `aios-operator`, scopes `aios.observe`, `aios.workflow.run`, `aios.audit`; **not** `aios.agent.register`; Production only |
| Configuration | Production `AIOS_OPERATOR_TOKENS` holds `[{"subject":"aios-operator","sha256":…,"scopes":[…]}]` — the hash only. A change takes effect on the next deployment |
| Custody | the delegated CEO's execution environment, private file (mode 600). Never in repository, documentation, evidence, logs or chat. Nobody pastes a provider secret into a conversation (`FDP-010` `§4.2`) |
| Rotation (loss, suspicion, or by routine) | generate a new token locally; set the new hash (`subject` unchanged); deploy the current release commit **twice** — first the new rollback target, then the serving deployment — so the designated target always carries the current principal; verify (smoke read-only, scope 403 on `aios.agent.register`, old token 401 on the serving deployment); update `FS-10-CURRENT-AUTHORITY.*`; destroy the old token |
| Revocation | set `AIOS_OPERATOR_TOKENS` to `[]` and redeploy as above; verify the token answers 401 |
| Edge (X2) | unchanged; the CEO has no standing path through X2 (`ESC-03`). Temporary access past X2 is for verification only, under `FDP-009-03`, and is revoked and its revocation verified each time |
| Not | a release, LIVE, Founder authority, or authority to change governance or certified roots (`FDP-010` `§4.6`, `§13`) |
