# FS-02 — AIOS Full Stack Architecture Blueprint

| Field | Value |
|---|---|
| **Stage** | FS-02 Full Stack Architecture (Act `§13`) |
| **Authority** | Act `§13` *"Missing application architecture required to proceed may be constructed within this Act"*; `FD-FS-001` |
| **Does not decide** | the six Architect-reserved areas (D2), nor Agent creation. Each is a decision package in `§9`, **Proposed, not ratified** |
| **Machine-readable contract** | `fullstack/backend/contract.py`; `fullstack/tests/test_api_contract.py` holds this document and the code to the same routes |

## 1. Boundary rule

```text
Frontend (application / control surface)
   ↓  HTTP + JSON, the API contract of §4 only
Backend (application / access layer)
   ↓  one adapter module: fullstack/backend/aios.py
AIOS contracts (native_core public surfaces; consumers/ agents)
   ↓
Runtime / Execution / Workflow / Tools / Trace / Knowledge / Memory
```

- The Frontend never reaches AIOS. It holds no authority: the backend decides
  every access (NC-12).
- The Backend reaches AIOS only through `aios.py`, and `aios.py` only through
  public exports (`native_core.core.<boundary>` `__all__`, `consumers.*`
  agents). It imports nothing from `tools/`.
- Nothing in `native_core/`, `consumers/` or `tools/` imports `fullstack/`.
  AIOS does not know the application exists.

## 2. Components

| Component | Responsibility | Owns | Does not own |
|---|---|---|---|
| **Frontend** `fullstack/frontend/` | The AIOS console: system, workflows and runs, tools, traces, audit | presentation state only | authority, AIOS state |
| **API** `fullstack/backend/api.py` | routing, validation, error model, security headers, static files | the HTTP contract | AIOS semantics |
| **Security** `fullstack/backend/security.py` | authenticator port, scope authorization, audit ledger | access decisions of the application | identity (FS-DP-02) |
| **AIOS adapter** `fullstack/backend/aios.py` | bootstraps and hosts one Runtime; runs catalog Workflows through agents; reads monitor, ledger, Trace | application run records | every AIOS decision: Workflow lifecycle, Tool governance, Trace authorship |
| **`docs.read` Tool** `fullstack/backend/docs_tool.py` | read a document under `docs/`, read-only | nothing | registration policy: the registry decides |

## 3. Technology

| Choice | Decision | Why |
|---|---|---|
| Backend language | Python 3.11 standard library | AIOS is stdlib-only; the adapter calls it in-process |
| HTTP interface | WSGI (`wsgiref` for local serving) | standard, dependency-free, served unchanged by any WSGI host. Which host serves it in production is FS-DP-04 |
| Frontend | static HTML, CSS and ES modules; no framework, no build step | nothing to compile or supply-chain; the roadmap's Next.js is a candidate the Deployment ADR may revisit |
| Tests | `unittest`; `node --test` for frontend modules; Playwright for the browser path | already present in the environment |
| Dependencies | **none added** | the repository declares none |

## 4. API contract v1

Base path `/api/v1`. JSON in and out. Every response carries the security
headers of `§6`.

| Method | Path | Scope | Returns |
|---|---|---|---|
| GET | `/api/v1/health` | public | liveness: `status`, Runtime state. No other data |
| GET | `/api/v1/session` | authenticated | the caller's subject and granted scopes |
| GET | `/api/v1/runtime` | `aios.observe` | Runtime identity, lifecycle state, hosted subsystems, boot time |
| GET | `/api/v1/tools` | `aios.observe` | registered Tools: key, version, lifecycle state, actions |
| GET | `/api/v1/tools/invocations` | `aios.observe` | the invocation ledger, all four dispositions |
| GET | `/api/v1/workflows` | `aios.observe` | the catalog of runnable Workflows and their input schema |
| GET | `/api/v1/runs` | `aios.observe` | every recorded run, newest first |
| GET | `/api/v1/runs/{run_id}` | `aios.observe` | one run: lifecycle states, step results, outcome or failure, Trace range |
| POST | `/api/v1/runs` | `aios.workflow.run` | starts a catalog Workflow; returns the terminal run |
| GET | `/api/v1/traces` | `aios.observe` | Trace records in append order; `offset`, `limit` |
| GET | `/api/v1/audit` | `aios.audit` | the application's access decisions; `offset`, `limit` |

**Error model.** `{"error": <code>, "detail": <text>}` with `400
invalid_request`, `401 unauthenticated`, `403 forbidden`, `404 not_found`,
`405 method_not_allowed`, `413 payload_too_large`, `503 unavailable`, `500
internal_error`. A 500 carries no traceback.

**Why a run is a Workflow of its own.** Phase 9 defines a Workflow's lifecycle
and no re-execution: a terminal Workflow *"SHALL NOT silently resume"*
(`ACT-CC-P9-001 §11.4`), and the lifecycle refuses to define an identity twice.
So each accepted run is defined as its own Workflow,
`WorkflowIdentity("<catalog key>/<run id>", <catalog version>)`. The run id is
an application identifier; no AIOS entity is added.

## 5. Workflow catalog

| Key | Version | Steps (actor · Skill) | Inputs |
|---|---|---|---|
| `document-conformance-review` | `1` | 1. `read-document`: `tool-proposing-agent` · `docs.read` — a governed invocation of the `docs.read` Tool. 2. `verify-criteria`: `engineering-intelligence-agent` · `engineering.testing` — `EngineeringIntelligenceAgent.verify` | `document`: a path under `docs/`; `criteria`: 1–20 required texts |

Each step is an Agent-Instance action and writes exactly one Trace (INV-4);
the Workflow-participating Agent writes one more for the coordination. A Tool
refusal or failure raises `StepFailed`, which drives the Workflow to `FAILED`
(Act FS-07 Scenario C). A document that does not satisfy its criteria is a
**successful** run with `conformant: false`: the work was done.

## 6. Security boundaries

- **Authentication** is a port: `Authenticator.authenticate(headers) →
  Principal | None`. The shipped default, `NoAuthenticator`, returns `None`,
  so every non-health route answers 401. The mechanism is FS-DP-02. Tests
  inject their own authenticator; production has none until FS-DP-02 is
  ratified.
- **Authorization** is by scope: each route of `§4` names one; a principal
  without it gets 403. Scopes are application vocabulary; *who holds which* is
  the authenticator's answer, and so FS-DP-02's.
- **Tool calls** still pass `ToolInvocationGovernance`. The application
  cannot reach `ToolBoundary.invoke` except through it.
- **Audit**: every authorization decision, allowed or refused, is appended to
  the audit partition: subject, method, path, scope, decision, status. No
  header, credential or request body is recorded (NC-10).
- **Headers**: `Content-Security-Policy: default-src 'self'; frame-ancestors
  'none'`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`,
  `Cache-Control: no-store` on the API.
- **Input bounds**: request bodies ≤ 64 KiB; the Tool reads only regular
  `.md` / `.txt` files under `docs/`, ≤ 2 MiB, with no traversal.

## 7. State boundaries

Summarized from FS-04 (`FS-04-DATA-AND-STATE.md`).

| State | Owner | Where |
|---|---|---|
| Runtime and Workflow lifecycle | AIOS (Runtime; Workflow boundary) | in-process, per `FD-P9-001` |
| Trace | AIOS (Trace) | append-only partition `trace` |
| Knowledge | AIOS (Knowledge) | its own partitions |
| Tool ledger | AIOS (Tools) | in-process |
| Run records | Application | append-only partition `fullstack-runs` |
| Audit | Application | append-only partition `fullstack-audit` |
| Frontend state | Browser | memory; the operator credential in `sessionStorage` |

All persistent state goes through the certified `StorageFacility`
(`LocalAppendOnlyStorage`) under one data directory given at start. **No
database is introduced** (FS-DP-01).

## 8. Integration and infrastructure requirements

Handed to the ADRs; none is decided here.

| Requirement | From | Package |
|---|---|---|
| A durable store that keeps append-only discipline for Trace, runs and audit, with backup and restore | FS-04, Trace INV-5 | FS-DP-01 Database |
| An identity provider and credential scheme mapping principals to scopes | FS-06 | FS-DP-02 Identity & Authentication |
| TLS, ingress, same-origin serving of Frontend and API | FS-08 | FS-DP-03 Networking |
| A host for the WSGI application and the static Frontend; the Runtime's lifetime (per process or per request); environment separation | FS-08, FS-10 | FS-DP-04 Deployment |
| Concurrency: independent Runtimes over one append-only store | FS-08 | FS-DP-05 Scaling |
| Logs, metrics, alerting beyond Trace and audit | FS-08, FS-09 | FS-DP-06 Observability |
| Agent creation through the application | FS-07 Scenario A | FS-DP-07 |

## 9. Decision packages (D2-A)

`docs/fullstack/decision-packages/`. Prepared by Claude, **Proposed**, for the
holder of Architect authority. Preparation is not ratification (`FD-FS-001`
D2-A).

Each package has an ADR-eligible **Part A** (the architectural question) and
a separate **Part B** (the implementation or infrastructure choice). The split
follows Engineering Constitution `§3.4`: an ADR *"may not … introduce a
technology, language, framework, or infrastructure decision."* Identifiers are
provisional; ADR numbers are the approving authority's to assign.

| Package | Area |
|---|---|
| `FS-DP-01` | Database implementation |
| `FS-DP-02` | Identity and Authentication |
| `FS-DP-03` | Networking |
| `FS-DP-04` | Deployment |
| `FS-DP-05` | Scaling |
| `FS-DP-06` | Observability implementation |
| `FS-DP-07` | Agent creation through the application surface (Agent Factory boundary) |

## 10. Exit determination (`§13`)

| Criterion | Result |
|---|---|
| Service boundaries defined | `§1`, `§2` |
| Interfaces defined | `§4`, `§5` |
| State boundaries defined | `§7` |
| Security boundaries defined | `§6` |
| Integration boundaries defined | `§1`, `§8` |
| Infrastructure requirements defined | `§8`, handed to `§9` |
| Consistent with AIOS canonical contracts | No core boundary is changed; every AIOS decision stays in its boundary (`§2`) |

**FS-02: EXIT CRITERIA MET.** Advance to FS-03.
