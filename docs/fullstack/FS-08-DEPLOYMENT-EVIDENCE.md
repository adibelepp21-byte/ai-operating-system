# FS-08 — Deployment Evidence: FS-ARCH-RAT-001 Implemented

| Field | Value |
|---|---|
| **Stage** | FS-08 Infrastructure & Cloud, continued after `FS-ARCH-RAT-001` (Register `§68`) |
| **Authority** | `ACT-CC-POST-P13-AIOS-FULL-STACK-001` + `FD-FS-001` + `FS-ARCH-RAT-001` `§13`: implement, verify, deploy a preview, re-discover. No Micro-Act was created |
| **Ratified architecture** | FS-DP-01 Option A: Supabase `scfymftfzkpilqbgmfwv` behind `StorageFacility`. FS-DP-04 A1 per request; B1 static frontend + Python API function |
| **Spending** | none. No plan changed on either provider |
| **Secrets** | none read, created, logged or recorded |

## 1. What was built

```text
Browser ──► Vercel static (fullstack/frontend)                 console, page headers
        └─► /api/v1/* ──► api/index.py ──► fullstack/deploy/vercel.py
                              one request = one Runtime (A1), then stopped
                          ──► Application (API v1, unchanged) ──► AIOSApplication
                          ──► AIOS public contracts ──► StorageFacility
                          ──► SupabaseStorage ──HTTPS──► aios_records (scfymftfzkpilqbgmfwv)
```

| Part | File | What it does |
|---|---|---|
| Store | `fullstack/backend/supabase_storage.py` | `SupabaseStorage(StorageFacility)`: append, read in append order, list partitions; nothing else. Stdlib HTTPS to PostgREST. Fails closed; the key goes only into two request headers |
| Schema | `fullstack/deploy/supabase/migrations/20260927062422_aios_records.sql` | One table `aios_records(seq, partition, record bytea)`, one listing function, one mutation guard. RLS on, no policy. `service_role` may SELECT and INSERT only |
| Composition | `fullstack/backend/aios.py` | `AIOSApplication` accepts a `StorageFacility`; with none it uses the local store as before |
| Function | `api/index.py` → `fullstack/deploy/vercel.py` | Per request: build the store, start a Runtime, serve through the unchanged `Application`, stop. No key → 503. Unreachable store → 503. No filesystem fallback |
| Hosting | `vercel.json` | Static console from `fullstack/frontend`; `/assets/*` rewritten to it; `/api/v1/*` to the function; the backend's page headers on static responses; region `icn1` (Seoul), beside the database in `ap-northeast-2` |

**Unchanged:** `native_core/`, `consumers/`, `tools/`, every certified root,
API contract v1, the authentication port (`NoAuthenticator`), scopes, audit,
the console.

### How the schema follows the contract

| `StorageFacility` (`native_core/core/infrastructure/storage.py`) | Schema |
|---|---|
| `append(partition, record: bytes)` | one row `(partition, record bytea)` |
| `read(partition)` in append order | `seq bigint generated always as identity`; ordered reads by `(partition, seq)` |
| `partitions()` | `aios_partitions()`, byte order like the local backend |
| no edit, no delete | UPDATE/DELETE/TRUNCATE not granted; a trigger refuses them even for the owner |
| a record has no raw newline (local backend) | check constraint, so either store exports to the other without loss |

Not created: any table for users, agents, messages, documents, runs or
Trace. Runs, Trace and audit are partitions whose records keep their own
formats (`fullstack.run/1`, Trace mappings, `fullstack.audit/1`).

## 2. Local verification

| Suite | Result |
|---|---|
| `fullstack` | 107 tests OK (79 before, +28 in `fullstack/tests/test_deployment.py`) |
| `native_core` | 801 OK (1 expected failure, unchanged) |
| `consumers` | 276 OK |
| `tools/bounded_exception` | 29 OK |
| `tools` | 1920 OK (1 skipped), before the commit and again on `8d088fb` |

`fullstack/tests/test_deployment.py` holds:

- **the contract on both backends**: the same assertions run against
  `LocalAppendOnlyStorage` and `SupabaseStorage` (append order, bytes
  unchanged, partition listing, refusals, no edit or delete offered);
- **fail closed**: wrong key, unreachable database, refused append, use before
  provisioning; the key never appears in an error, a URL or `repr`;
- **per request (A1)**: a run made by one request is read by the next, which
  has a different Runtime identity; run numbering continues across requests;
  a failed run is durable; the store is the only state;
- **security unchanged**: 401 anonymous, 403 without scope, audit of refusals,
  API headers; the shipped function authenticates nobody;
- **no fallback**: without a key every API route answers 503; with the
  database down, 503 and no file written;
- **configuration**: static headers equal the backend's constants; one
  function; the entrypoint installs the certified-write barrier first; no key
  in any committed file;
- **migration**: one table, two functions, three columns; no generic table; no
  UPDATE/DELETE/TRUNCATE grant; no policy.

The database is replaced in these tests by an in-memory model of PostgREST.
The live database is verified in `§3`.

## 3. Supabase verification (live)

Record: `docs/fullstack/evidence/FS-08-SUPABASE-VERIFICATION-2026-09-27.json`.

- Before: project ACTIVE_HEALTHY, no tables, no migrations.
- Migration `20260927062422 aios_records` applied: success.
- One verification transaction, rolled back by design: `service_role`
  appends and reads bytes unchanged in order; UPDATE, DELETE and TRUNCATE are
  refused for `service_role` (no privilege) **and for the owner** (trigger);
  `anon` and `authenticated` can neither read, append, nor list partitions;
  a newline record, a `../x` partition and an explicit `seq` are refused.
- After: 0 rows, RLS on, 0 policies, API grants only `service_role` SELECT and
  INSERT.
- Advisors: security, one INFO (`rls_enabled_no_policy`, intended);
  performance, none.

**Not verified live:** an HTTPS read or append with the server-side key. The
key is not available to Claude and was not created (the Act: *"Do not create
missing secrets merely to make deployment pass."*). This is EXT-05.

## 4. Preview deployment

Pushing `8d088fb` to this branch deployed a preview through the project's Git
integration. Nothing was promoted, and nothing was merged to the default
branch.

| Fact | Value | Source |
|---|---|---|
| Deployment | `dpl_drGHDofUQdk1SgNhTzDSEwSTDunU` | `list_deployments`, `get_deployment` |
| Commit · branch | `8d088fb` · `claude/aios-activation-authority-discovery-enq7bk` | same |
| Target | **preview** (`target: null`) | same |
| State | **READY**; the build took about 15 s | same |
| Type · region | `LAMBDAS` · **`icn1`**, as `vercel.json` sets | same |
| Production | unchanged: `dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj` from `22c0b49` | `list_deployments` |
| Environment variables | **none** on the project, so no server-side key (EXT-05) | `filter_project_envs` (names only) |
| Protection | SSO on every deployment URL except custom domains | `get_project` |

**Live verification of the preview: NOT PERFORMED.**

| Attempt | Result |
|---|---|
| `GET /`, `GET /api/v1/health` from this environment | `302` to `vercel.com/sso-api`: Vercel Authentication, before the deployment |
| `GET /assets/app.js` from this environment | timed out after 20 s, no response |
| Connector `web_fetch_vercel_url` (with and without team) | *"Vercel denied access to this deployment"* |
| Connector `get_access_to_vercel_url` (share link) | denied |
| Connector build logs (`list_deployment_events`) | `403`: *"You must re-authenticate to this scope"* |

So there is **no evidence** that the static console is served, that the
Python function starts on Vercel's runtime, that the rewrites route, or that
the page headers are applied. A READY state shows only that the build
finished. The Python runtime serving this framework-free WSGI callable
remains **inferred, not confirmed**.

Even with access, the API would answer `503 unavailable` on every route:
there is no key (EXT-05), and the function has no fallback, by design. A
successful workflow cannot be run live until FS-DP-02 gives an authenticator,
because the shipped function authenticates nobody.

## 5. Observations for the Architect

1. **INV-12 reading.** INV-12 reserves direct external dependencies to Tool,
   and the Freeze lists *"any non-Tool external dependency"* as forbidden for
   Infrastructure. `FS-ARCH-RAT-001` places a Supabase adapter behind
   `StorageFacility`, as FS-DP-01 A1 proposed, under the Architect's reserved
   authority over *Database implementation* (Freeze `§10`). It was implemented
   as ratified: in the application layer, with `native_core` unchanged and the
   backend replaceable. If the Architect reads INV-12 as excluding it, the
   adapter can be removed without changing any record format.
2. **Concurrency (FS-DP-05, not ratified).** Per request, run numbers come
   from the count of durable run records. Two concurrent run requests could
   take the same number, and a run's Trace range could include another run's
   records. This cannot happen live today, because no request is
   authenticated (FS-DP-02). It must be settled before FS-DP-02 opens run
   creation.
3. **Refusals are audited durably.** Every refused request to a protected
   route appends an audit entry. On a public URL, anonymous traffic grows the
   table. Vercel's deployment protection covers previews; production needs
   FS-DP-03 and FS-DP-06 to decide limits.
4. **Frontend tests are served.** The static output directory is
   `fullstack/frontend`, so its `tests/` files are publicly readable. They hold
   no secret; a build step would remove them, and none is used.

## 6. FS-08 re-discovery and exit determination

Against `FS-ARCH-RAT-001` `§15`:

| Criterion | Status | Evidence |
|---|---|---|
| Vercel deployment surface exists | **MET** | preview `dpl_drGHDofUQdk1SgNhTzDSEwSTDunU` READY |
| Static frontend reachable | **NOT EVIDENCED** | SSO; connector denied (EXT-03) |
| Python API function reachable | **NOT EVIDENCED** | same |
| API invokes existing Full Stack contracts | **MET locally** | `ThePerRequestFunction` tests; unchanged `Application` |
| AIOS public contracts remain the integration boundary | **MET** | the adapter imports `fullstack.backend` only; `native_core`, `consumers` unchanged |
| Supabase persistence adapter operational | **MET locally; live schema verified** | contract tests on both backends; `§3`. Not over HTTPS with the key (EXT-05) |
| Evidence-backed schema exists | **MET** | migration `20260927062422`; `§1` table |
| Persistent state survives restart / request boundaries | **MET locally** | `test_state_crosses_request_boundaries_only_through_the_database`. Not live |
| Function-local memory is not durable state | **MET** | no local store in the adapter; `test_the_adapter_never_names_a_local_store`; 503 with no fallback |
| Security behaviour preserved | **MET locally** | 401, 403, audit, headers in the function tests |
| Trace / audit preserved | **MET locally** | Trace and audit partitions in the store after a run |
| Failure handling verified | **MET locally** | failed run durable; no key → 503; database down → 503 |
| Certified-write protection preserved | **MET** | `api/index.py` imports `tools` first; `tools` suite (1920) OK |
| Preview / live verification completed | **NOT MET** | `§4` |
| No unauthorized certified-root modifications | **MET** | diff touches no certified root |
| Full regression suites pass | **MET** | `§2` |
| FS-08 re-discovery completed | **MET** | `§3`, `§4` |
| No unresolved blocker within FS-08 scope | **NOT MET** | EXT-03, EXT-05 |

**FS-08: NOT CLOSED.** The implementation and the database are in place;
the live half of the evidence is missing. Per `§14`, a FAIL leads to
self-repair, but nothing left is repairable by Claude:

| Blocker | Why Claude cannot clear it | Who clears it |
|---|---|---|
| EXT-05: no server-side key in Vercel | the Act forbids creating a secret to make deployment pass; the connector does not expose secret keys | the Founder: set `SUPABASE_SECRET_KEY` (a secret key of `scfymftfzkpilqbgmfwv`) for **Preview**, then redeploy |
| EXT-03: preview unreachable | SSO protects every deployment URL; the connector is denied the team's scope for previews, logs and share links | the Founder: re-authorize the Vercel connection for team `adibelepp21-bytes-projects`, or open the preview themselves |
| Successful workflow live | no authenticator exists (FS-DP-02 not ratified) | the Architect |

**FS-09 is not entered.** No claim of Production Ready, Production Released
or Operational AIOS.
