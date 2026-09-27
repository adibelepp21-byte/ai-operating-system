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
| `tools` | see `§6` |

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

Recorded in `§4a` after the push.

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

## 6. Exit determination

Recorded in `§6a` after the preview.
