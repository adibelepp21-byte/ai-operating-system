# FS-DP-05 — Scaling

| Field | Value |
|---|---|
| **Identifier** | `FS-DP-05` (provisional) |
| **Area** | Scaling — Freeze `§10`, Architect-reserved |
| **Status** | **PROPOSED — NOT RATIFIED** |
| **Decision owner** | Holder of Architect authority (`FD-FS-001` D2-A) |
| **Founder constraints** | No spending (D3-A) |
| **Prepared by** | Claude Code, 2026-09-26; **Revision 2** 2026-09-27 (below), under `ACT-CC-POST-P13-AIOS-FULL-STACK-002` `§12` |

## Context

- Locally, one process serves requests one at a time, and a lock serializes
  runs against the single Runtime.
- Under FS-DP-04 A1, concurrent requests each get their own Runtime. The only
  shared state is the database, whose `seq` column gives one global append
  order (FS-DP-01 Part B).
- No workload requirement has been stated. FS-09 measures latency on the
  current workflow instead of assuming one.

## Part A — Architectural decision (ADR-eligible)

**Recommended:** AIOS scales by **independent Runtimes over one append-only
store**. No Runtime shares in-process state with another; ordering comes from
the store. No coordination layer, queue or scheduler is introduced: the
Runtime contract excludes them (`runtime/contract.py`).

## Part B — Implementation decision (not ADR-eligible)

- The host's default concurrency; no autoscaling configuration of our own.
- Database connections through the provider's pooler; one connection per
  request.
- A request-rate limit on `POST /api/v1/runs` at the edge or in the backend.
- Reassess when a workload requirement exists.

## Until decided

Single process, serialized runs.

## Exact decision required

- [ ] Part A: as written · amended
- [ ] Part B: as written · amended
- [ ] Decided as: Architect · Founder as Architect

---

## Revision 2 (2026-09-27): concurrency, after FS-DP-04 A1 was ratified

The first revision assumed runs were serialized. FS-DP-04 A1 (a Runtime per
request) removed that lock, and the implementation showed what follows. The
revision is **proposed; Claude does not ratify it** (Act NC-01, NC-07).

### R2.1 Observed behaviour

A run's number is the count of durable run records plus one, read when the
Runtime starts (`fullstack/backend/aios.py`, `start_run`). Under A1, two
requests whose Runtimes both start before either appends a run take **the
same number**.

| Evidence | Where |
|---|---|
| Reproduced, deterministic: two Runtimes over one store both mint `run-00001`; `GET /api/v1/runs/run-00001` then returns the second, and the first cannot be addressed by id | `fullstack/tests/test_deployment.py`, `TheConcurrencyFinding.test_the_finding_reproduces` |
| The property that should hold, recorded as an expected failure until a ratified fix | `test_concurrent_requests_mint_distinct_run_ids` |
| Live exposure today: **none**. No request is authenticated (FS-DP-02), so no run can be created on the deployment | `§R2.6` |

### R2.2 Discovery (Act `§12.3`)

| Subject | Finding |
|---|---|
| Run identity | `run-NNNNN` from a count read at start. It is also part of the Workflow identity (`document-conformance-review/run-NNNNN`) |
| Sequence generation | The store's `seq` is a global, strictly increasing identity (gaps possible). `StorageFacility.append` returns nothing, so no caller can learn it |
| Persistence semantics | Each append is one atomic INSERT. There is no multi-record transaction, and the contract offers none |
| Transaction boundaries | One run appends 3 Trace records, 1 run record and 1 audit entry (2 Trace records if it fails). They are separate. A request that dies mid-run leaves Trace without a run record: Trace, the source of truth, is kept; the application summary is missing |
| Trace range | The run record's Trace range `{from, to}` is positions counted before and after the run. A concurrent run's Trace can fall inside it. Each Trace record carries `runtime`, which under A1 is unique to the request, so a run's Trace can be selected exactly |
| Idempotency | `POST /api/v1/runs` is not idempotent |
| Retry | `SupabaseStorage` never retries. A client retry after a timeout creates a second run. An append whose response is lost raises, so the request fails although the row may exist |
| Request and Runtime lifecycle | One Runtime per request, stopped before the response (FS-DP-04 A1) |
| Deployment concurrency | The host may run invocations in parallel, in separate instances or in one. The adapter builds every object per request; a scan found no module-level mutable containers in `native_core/core` or `consumers` |
| State ownership | Trace: the acting Agents. Runs and audit: the application. All three are partitions of one store |
| Scaling | Each request reads whole partitions (runs to count; Trace to page; audit to page), so cost grows with history. No workload requirement exists |
| Failure recovery | Nothing automatic. Records are immutable; a correction is a successor record |

### R2.3 Affected contracts

- Run record `fullstack.run/1`: `run_id`, and `trace.{from,to,count}`.
- API v1: the **value** of `{run_id}` (the route pattern `[A-Za-z0-9-]{1,64}` is unchanged).
- The Workflow identity key built from the run id.
- The console, which shows run ids.
- Not affected: `StorageFacility`, the Runtime contract, Trace records, the schema.

### R2.4 Candidate resolution patterns

| # | Pattern | Assessment |
|---|---|---|
| **C1** | **Identity from the Runtime, not from a count.** `run_id` is derived from the request's Runtime boot identity (time plus at least 64 random bits), unique by construction. Order is the store's append order; any ordinal shown is computed when reading and is not an identity. A run's Trace is selected by its `runtime` field, not by position. A new run format `fullstack.run/2` is read beside `/1` (FS-04 `§4` successor rule) | No store coordination, no provider feature, no contract change beneath the application. Changes the run-id value format and the run record format |
| C2 | Identity assigned by the store (its `seq`) | Needs `append` to return a position: a `StorageFacility` change in `native_core`, not delegable. Or a Supabase sequence called directly: provider-defined semantics (Act NC-08). **Rejected** |
| C3 | Serialize run creation (a database advisory lock, or a host concurrency of 1) | Makes the provider define AIOS semantics (NC-08); the host setting is not available as a guarantee. **Rejected** |
| C4 | Detect duplicates after appending and supersede them | Duplicates stay in an append-only store; a second record is needed to explain the first. **Rejected** |
| C5 | Keep the current behaviour under a stated single-writer constraint | Acceptable only while one principal uses one console at a time. A fallback, not a resolution |

Sub-decisions, independent of the choice above:

- **Idempotency.** I1: none; a client that times out lists runs before
  retrying (recommended now). I2: an optional idempotency key recorded in the
  run record. Its check is itself a read-then-append race unless C1-style
  identity is used, so it would come later.
- **Partial runs.** Recommended: accept that Trace can exist without a run
  record, and show it as such. A request cannot make five appends atomic
  without a store transaction the contract does not offer.

### R2.5 Proposed Part A (ADR-eligible)

*AIOS scales by independent Runtimes over one append-only store. Anything a
Runtime creates takes its identity from that Runtime's own identity, never
from a count read from the store. Order is the store's append order.*

**Recommendation: C1 + I1 + accept partial runs.** Part B as in revision 1
(host default concurrency; no autoscaling of our own; a rate limit on
`POST /api/v1/runs` when FS-DP-02 opens run creation).

### R2.6 Dependencies and order

- **FS-DP-02 → exposure.** The finding becomes live the moment an
  authenticator lets run requests through. FS-DP-05 must therefore be
  decided **before or with** the FS-DP-02 implementation. Neither decision
  depends on the other's content, so both packages go to the Architect now
  (Act `§13`).
- **EXT-05, EXT-03 → live verification** of whatever is chosen.

### R2.7 Implications

| | C1 |
|---|---|
| Persistence | no schema change; new run records use format `/2`; `/1` records stay as they are and are still read |
| Scaling | removes the only read-then-write race in the application |
| Runtime | none: the Runtime already has a unique identity under A1 |
| Failure | a failed or partial run keeps a unique identity |

### R2.8 Verification after ratification

1. `test_concurrent_requests_mint_distinct_run_ids` passes; its
   `expectedFailure` marker is removed.
2. A threaded test: N parallel run requests over one store give N distinct
   ids, N run records, and Trace attributed to the right run.
3. `/1` records written before the change are still listed and addressable.
4. Full regression.
5. Live, once FS-DP-02, EXT-05 and EXT-03 allow: two parallel `POST
   /api/v1/runs` against the preview.

### R2.9 Exact decision required

- [ ] Part A: as proposed in `§R2.5` · amended · other
- [ ] Resolution: C1 · C5 (constraint) · other
- [ ] Idempotency: I1 · I2
- [ ] Partial runs: accepted as described · other
- [ ] Part B: as in revision 1 · amended
- [ ] Decided as: Architect · Founder as Architect
