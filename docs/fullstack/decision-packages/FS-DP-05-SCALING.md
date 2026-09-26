# FS-DP-05 — Scaling

| Field | Value |
|---|---|
| **Identifier** | `FS-DP-05` (provisional) |
| **Area** | Scaling — Freeze `§10`, Architect-reserved |
| **Status** | **PROPOSED — NOT RATIFIED** |
| **Decision owner** | Holder of Architect authority (`FD-FS-001` D2-A) |
| **Founder constraints** | No spending (D3-A) |
| **Prepared by** | Claude Code, 2026-09-26 |

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
