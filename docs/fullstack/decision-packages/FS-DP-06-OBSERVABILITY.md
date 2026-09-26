# FS-DP-06 — Observability Implementation

| Field | Value |
|---|---|
| **Identifier** | `FS-DP-06` (provisional) |
| **Area** | Observability implementation — Freeze `§10`, Architect-reserved |
| **Status** | **PROPOSED — NOT RATIFIED** |
| **Decision owner** | Holder of Architect authority (`FD-FS-001` D2-A) |
| **Founder constraints** | Vercel, Supabase; no spending (D3-A) |
| **Prepared by** | Claude Code, 2026-09-26 |

## Context

- **Observability is not accountability** (Freeze AD-8). Trace is the
  accountability record of Agent-Instance actions; it is not a log, event or
  metric, and nothing operational may be written into it.
- The backend already produces: the health route; the audit ledger of access
  decisions; Trace; run records with state history.
- It has no request log, no metrics and no alerting.

## Part A — Architectural decision (ADR-eligible)

**Recommended:** operational telemetry is **separate from Trace and from
audit**, and never carries credentials, request bodies or document contents.
Three streams, three purposes:

| Stream | Purpose | Owner |
|---|---|---|
| Trace | what an Agent Instance did | AIOS |
| Audit | who was allowed or refused what | application |
| Telemetry | how the service is behaving: requests, latency, errors | operations |

## Part B — Implementation decision (not ADR-eligible)

1. One structured JSON log line per request to stdout: request id, method,
   route, status, latency. Collected by the host's runtime logs.
2. A readiness signal beside liveness: health reports the Runtime state and
   whether the store is reachable.
3. Alerting: the host's built-in facilities if the plan includes them;
   otherwise an external uptime check on `/api/v1/health` (an external
   dependency). Paid alerting is a spending decision.
4. OpenTelemetry-compatible naming, so a collector can be added later
   without changing the log shape.

## Until decided

Health, audit, Trace and run records exist; request logs, metrics and
alerting do not.

## Exact decision required

- [ ] Part A: as written · amended
- [ ] Part B: as written · amended
- [ ] Decided as: Architect · Founder as Architect
