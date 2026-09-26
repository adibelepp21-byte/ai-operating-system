# FS-DP-04 — Deployment

| Field | Value |
|---|---|
| **Identifier** | `FS-DP-04` (provisional) |
| **Area** | Deployment — Freeze `§10`, Architect-reserved |
| **Status** | **PROPOSED — NOT RATIFIED** |
| **Decision owner** | Holder of Architect authority (`FD-FS-001` D2-A) |
| **Founder constraints** | Vercel hosting; no spending (D3-A); production release only by a separate Founder decision (D4-A) |
| **Prepared by** | Claude Code, 2026-09-26 |

## Context

- The backend is a WSGI application holding **one AIOS Runtime per process**.
  The Runtime's in-process state (Workflow lifecycle, Tool ledger, Memory) is
  in-process by AIOS decision (`FD-P9-001 §12.4`).
- A serverless host starts and stops processes per demand. A Runtime would
  live for one invocation or a short warm period, not for the life of the
  service.

## Part A — Architectural decision (ADR-eligible)

**Question.** What is the Runtime's lifetime in a deployed AIOS?

| Option | Statement | Assessment |
|---|---|---|
| **A1** | **Request-scoped Runtime.** Each request that acts bootstraps a Runtime, runs, persists Trace and records, and stops it. Runtime identity is unique per boot | Lawful under the Runtime contract (`CREATED → … → STOPPED`). In-process views (Tool ledger, live monitor) cover one request only; every durable record is in the database |
| A2 | Long-lived Runtime in a persistent process | Needs a host with persistent processes. Vercel does not provide one; another provider would need a Founder naming and possibly spending |

The choice of host must not reshape AIOS (NC-13). **A1 does not**: it uses
the lifecycle as specified. **Recommendation: A1**, with the consequence
recorded: *"what the Runtime currently holds"* is per-request, and the
console reads history from durable records.

## Part B — Implementation decision (not ADR-eligible)

1. **Vercel**: the Frontend as static assets; the backend as a Python
   function serving the WSGI application; one project; environment variables
   for secrets.
2. **Environments**: Preview deployments = staging, from branches. Production
   only after the Founder release decision (D4-A). Production deployment
   protection kept on.
3. **Build**: no build step; the artifact is the repository tree at a
   commit. The release artifact is identified by commit SHA.
4. **Rollback**: promote the previous deployment (instant rollback).
5. **Before deciding, confirm on the account** (FS-08 discovery): plan terms
   (the free plan's permitted use), function duration and size limits, and
   whether the Python runtime serves this WSGI application unchanged.

## Until decided

Nothing is deployed. The backend runs locally
(`python -m fullstack.backend serve`).

## Exact decision required

- [ ] Part A: A1 · A2 (with a Founder naming of another host)
- [ ] Part B: as written · amended
- [ ] Decided as: Architect · Founder as Architect
