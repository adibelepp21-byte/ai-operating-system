# FS-DP-06 — Observability Implementation

| Field | Value |
|---|---|
| **Identifier** | `FS-DP-06` (provisional) |
| **Area** | Observability implementation — Freeze `§10`, Architect-reserved |
| **Status** | **RATIFIED — L1 / M1 / R2**, by the Founder as Architect in `ACT-CC-POST-P13-AIOS-FULL-STACK-004` `§10` (Register `§93`, `ACT-004-DG-02`). R2 is the readiness signal (`R2.6`). **Alerting (H1–H3) is not decided** (ACT-004 labels R2 "Alerting"; reconciled under ACT-005, Register `§92`). Revision 2 (below) is the package as reviewed (`§89`) |
| **Decision owner** | Holder of Architect authority (`FD-FS-001` D2-A) |
| **Founder constraints** | Vercel, Supabase; no spending (D3-A) |
| **Prepared by** | Claude Code, 2026-09-26; **Revision 2** 2026-09-27 (below), on the Founder's *"FS-09 — DECISION PACKAGE PREPARATION"* |

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

Health, audit, Trace and run records exist. The local server prints the
standard library's plain access line to stderr; there are no structured
logs, metrics or alerting.

## Exact decision required

- [ ] Part A: as written · amended
- [ ] Part B: as written · amended
- [ ] Decided as: Architect · Founder as Architect

## Revision 2 (2026-09-27): FS-09 Architect review package

Revision 1 above is unchanged. This revision keeps **five mechanisms separate**:
Trace, Audit, Logging, Metrics and Alerting. None is folded into another, and
the decision is taken per mechanism.

### R2.1 Decision ID

`FS-DP-06` (provisional), revision 2. Register `§89`.

### R2.2 Exact architectural question

How the service's **operational behaviour** is recorded and acted on
(logging, metrics, alerting), and how those three stay separate from each
other and from the two accountability records AIOS already keeps (Trace and
Audit): what each may contain, where it lives, how long, and who owns it.

### R2.3 Canonical sources

| Source | What it requires |
|---|---|
| `FD-FS-001` D2-A; Freeze `§10` | observability implementation is Architect-reserved |
| Freeze **AD-8** | *observability is not accountability*: nothing operational is written into Trace |
| INV-4 | each acting Agent authors its own Trace record, once |
| ACT-001 `§20` | Observability: logging, metrics, tracing, alerting |
| ACT-003 `§19` | monitoring, alerting, operational ownership |
| `FS-DP-02` B3 decision | *"Secrets MUST NOT be committed into … logs"* |
| `FD-FS-001` D3-A | no spending without the Founder |

### R2.4 Current implementation state, per mechanism

| Mechanism | Purpose | Owner | Exists today | Where it lives | Verified |
|---|---|---|---|---|---|
| **Trace** | what an Agent Instance did (accountability) | AIOS | yes: `TraceWriter`/`TraceReader`, partition `trace`; a run's own records by Runtime and ordinal (`FS-DP-05` C1) | append-only store | L + P (FS-08) |
| **Audit** | who was allowed or refused what (access accountability) | application | yes: `AuditLedger`, partition `fullstack-audit`: subject, method, path, scope, decision, status, `request_id`; no credential | append-only store | L + P |
| **Logging** | what the service did, operationally | operations | **partial, unstructured.** Five stderr lines only: `AIOS_OPERATOR_TOKENS <reason>; nobody is authenticated`; `storage not configured: …`; `runtime start failed: …`; `request failed after start` + traceback; `[<request id>] internal error on <method> <path>` + traceback. No per-request line in the deployment. Locally, `wsgiref` prints an access line | host function log (Vercel runtime logs). Retention is the host plan's, **not established** | the lines were used in FS-08 diagnosis |
| **Metrics** | how much, how fast, how often it fails | operations | **none** | — | — |
| **Alerting** | tell someone when it breaks | operations | **none.** Runbook `§1` has manual checks | — | — |

Noted facts:

* In the deployed composition, `GET /api/v1/health` answers 200 only after a Runtime started on the store (otherwise 503). So a liveness 200 already implies the store was reachable for that request. Locally it does not.
* Since 2026-09-27 19:57Z the Previews are reachable without Vercel login (`FS-DP-03` revision 2 `R2.4`), which matters for alerting reachability.

### R2.5 Authority required

**Architect** (or the Founder acting as Architect) for the mechanisms and
their separation. **Founder** for any paid product (D3-A), any external
monitoring service (a new third party), and who receives alerts
(`OPERATIONAL-OWNERSHIP`).

### R2.6 Available options (per mechanism; separation preserved in every one)

**Part A: separation rule** (revision 1): *as written* (three operational
streams separate from Trace and Audit; no credentials, request bodies or
document contents in telemetry) · *amended*.

| Mechanism | Options |
|---|---|
| **Trace** | **unchanged** in every option. No telemetry field is added to a Trace record |
| **Audit** | **unchanged** in every option. The audit is not used as a request log, even though it records every access decision |
| **Logging** | **L1** one structured JSON line per request to stdout (time, `request_id`, method, route template, status, latency, `runtime_id`), collected by the host · **L2** formalize today's error-only lines (fixed prefixes, no per-request line) · **L3** no application logging beyond the host's own |
| **Metrics** | **M1** derived from L1 lines by the host or a collector; no separate emitter · **M2** emitted by the application (counters, latency histograms) in OpenTelemetry-compatible form to a collector · **M3** none; manual analysis of logs |
| **Alerting** | **H1** the host's alerting, if the plan provides it (possibly paid) · **H2** an external uptime check on `/api/v1/health` (a third party) · **H3** none; the runbook's manual checks |
| **Readiness signal** | **R1** health reports store reachability explicitly (a field) · **R2** keep today's implicit meaning (deployed 200 implies the store started) and document it |

### R2.7 Architectural consequences

* L1 adds one output per request in the API layer. Trace and Audit are unchanged.
* M2 adds a telemetry emitter and, in production, a collector: a new runtime dependency (the stack is standard-library only today).
* M1 keeps the application emitter-free; metrics quality depends on the host.
* H2 puts an external party on the monitoring path, which needs edge reachability (`FS-DP-03`).
* R1 changes the `/health` response contract (an added field); R2 changes nothing.

### R2.8 Data and state consequences

* Logging, metrics and alerting live **outside** the AIOS store. No option
  writes telemetry into `aios_records`: that would break AD-8 and grow an
  append-only table with operational data. It is excluded from every option.
* Host logs are ephemeral: retention depends on the plan and is not established.
  Anything that must outlive them (incidents) goes into a written incident
  record (runbook `§11`), not into Trace or Audit.
* `request_id` is the only join key between a log line and an audit entry.

### R2.9 Security consequences

* A log line never carries the Authorization header, a token or a token hash,
  a request body, a document's contents or the database key. The route
  **template** is logged, not the raw path (a raw path could carry an identifier).
* Access to host logs is access to operational data: Vercel team members only.
* H2 exposes only `/health` status to the third party.
* Today's traceback lines can include exception messages. The existing code
  never formats the key or token into them, and L1/L2 keep that rule under test.

### R2.10 Operational consequences

* L1 plus M1 give request volume, error rate and latency without new
  infrastructure. Retention limits how far back an incident can be examined.
* Alerting (H1, H2) needs a recipient: `OPERATIONAL-OWNERSHIP` (Founder).
* H3 means failures are found only by people. Runbook `§12` stays a placeholder.

### R2.11 Verification requirements

1. **Separation tests**: a request adds exactly one log line (L1) and changes neither the number nor the content of Trace records; audit entries are unchanged by logging.
2. **Redaction tests**: with a known fake token, body and document, no log line contains any of them (a mutation check that a leaking logger is caught).
3. Field schema test for L1; route template, not raw path.
4. Live: the Preview's runtime logs (read through the connector) show the lines for a known `request_id`, matching its audit entry.
5. Alerting (H1/H2): an induced failure on a Preview raises an alert to the recorded owner (needs Preview access and an owner).
6. The readiness gate's *logging, metrics, alerting* row changes from BLOCKED only after 1–5 are recorded.

### R2.12 Rollback implications

Logging, metrics and alerting code rolls back with its commit, with no data
consequence (nothing is written to the store). A rollback below the logging
change silently removes the operational record, so the rollback procedure
(runbook `§9`) must name that effect. An external monitor must be disabled
separately.

### R2.13 Explicit non-scope

No change to Trace or Audit format or content. No telemetry in the AIOS
store. No paid product. No third-party monitor. No code is written by this
package.

### R2.14 Dependencies

| On | Why |
|---|---|
| `FS-DP-03` | edge access decides whether an external check (H2) can reach `/health` |
| `OPERATIONAL-OWNERSHIP` (Founder) | alert recipients; log review |
| Founder spending (D3-A) | H1 on a paid plan; M2 with a paid collector |
| `FS-09-ENV` | per-environment logs and alerts once Preview and Production are separate |

### R2.15 Whether it blocks FS-09

**Yes.** Gate row *Observability: logging, metrics, alerting* is BLOCKED on it.
Tracing already passes and is not part of this decision.

### R2.16 Analytical recommendation (**UNRATIFIED**)

> *Not a decision. Stands only as analysis until the Architect decides.*
> Part A as written; Trace and Audit unchanged; **L1** logging; **M1** metrics
> derived from L1; **R2** readiness, documented; alerting decided with
> `FS-DP-03` and the Founder's ownership decision (H2 if the edge allows a
> monitor, else H1 or H3 with the residual stated).

### R2.17 Exact decision required

- [ ] Part A: as written · amended
- [ ] Logging: L1 · L2 · L3
- [ ] Metrics: M1 · M2 · M3
- [ ] Alerting: H1 · H2 · H3
- [ ] Readiness signal: R1 · R2
- [ ] Decided as: Architect · Founder as Architect

