# FS-DP-04 — Deployment

| Field | Value |
|---|---|
| **Identifier** | `FS-DP-04` (provisional) |
| **Area** | Deployment — Freeze `§10`, Architect-reserved |
| **Status** | **RATIFIED**: Part A **A1 — per request**; Part B **B1 — static frontend + Python API function**, by `FS-ARCH-RAT-001`, Architect (Moriarty), 2026-09-27; Register `§68` |
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

## Facts found in FS-08 discovery (2026-09-26)

- One Vercel team exists, with one unrelated project. No AIOS project exists.
  The connector did not report the plan tier.
- Vercel's documentation shows WSGI entrypoints for its Python runtime
  (Django and Flask guides; `[tool.vercel] entrypoint = "module:app"`).
  Whether a framework-free WSGI callable like the backend's `Application` is
  served unchanged is **inferred, not confirmed**; a preview deployment would
  confirm it.
- Rolling back to a *specific* older deployment is documented as a Pro or
  Enterprise feature. What the team's plan allows must be confirmed before
  point 4 above is relied on.

## Facts found in the FS-08 Vercel & Supabase execution (2026-09-27)

- A Vercel project exists: `aios-platform` (`prj_exqF51HASzlwn5kiO4kAGJ9mHe0N`),
  bound to this repository, no framework preset, no environment variables,
  SSO on deployment URLs.
- Its production deployment (`dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj`, commit
  `22c0b49`) answers **Vercel's platform 404** on every path. That source holds
  no `fullstack/` and no entrypoint Vercel recognizes. Even the current branch
  has no Vercel entrypoint (`FS-08-VERCEL-SUPABASE-EXECUTION.md` `§C`).
- **Production is the repository's default branch.** Every merge into it
  deploys to the public production alias, so merging *is* releasing unless the
  production branch is changed.

**The questions, sharpened.** The adapter cannot be written without answering
them:

1. **Runtime lifetime (Part A).** Per request (A1), or per warm function
   instance? A1 stays recommended. A per-instance Runtime would share
   in-process state between unrelated requests for an unknown period, which
   Part A is meant to decide, not the adapter.
2. **Shape (Part B).** One Python function serving the API and the console,
   or the static console served by Vercel plus a function for `/api/v1/*`?
   Recommended: static console plus one function, which keeps the frontend off
   the function path.
3. **Store.** It depends on FS-DP-01: nothing deployable persists without it.
4. **Release control (Founder, D4-A).** A dedicated production branch, so
   merging to the default branch stops releasing?

## Decision (2026-09-27)

Ratified by `FS-ARCH-RAT-001` (Register `§68`): a Runtime per request (A1);
the console as static assets and the API as one Python function (B1). The
release-control question (point 4 above) is the Founder's and is not decided:
production is still the default branch, so nothing is merged to it.

**Implemented** (`docs/fullstack/FS-08-DEPLOYMENT-EVIDENCE.md`):
`api/index.py` → `fullstack/deploy/vercel.py` (one Runtime per request over
`SupabaseStorage`, no filesystem fallback) and `vercel.json` (static console
from `fullstack/frontend`, `/api/v1/*` to the function, the backend's page
headers on static responses, function region `icn1` beside the database).

## Exact decision required

- [ ] Part A: A1 · A2 (with a Founder naming of another host)
- [ ] Part B: as written · amended
- [ ] Decided as: Architect · Founder as Architect
