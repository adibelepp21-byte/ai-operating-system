# FS-03 — Backend Foundation: Evidence

| Field | Value |
|---|---|
| **Stage** | FS-03 Backend Foundation (Act `§14`) |
| **Code** | `fullstack/backend/`: `aios.py` (AIOS adapter) · `api.py` (WSGI application) · `contract.py` (API contract v1 as data) · `security.py` · `docs_tool.py` · `__main__.py` |
| **Tests** | `fullstack/tests/test_backend_api.py` (26) · `test_api_contract.py` (3) |
| **Run locally** | `python -m fullstack.backend serve --data-dir <dir>` (loopback; every protected route answers 401 until FS-DP-02) |

## What was built, and on which contract

| Built | Calls | Decides nothing that belongs to |
|---|---|---|
| `AIOSApplication.start` | `bootstrap_runtime` → `start()`; `ToolRegistry.define/register/enable`; `ToolBoundary.register` | Runtime (hosting), Tools (lifecycle authority stays in the registry) |
| `AIOSApplication.start_run` | `create_execution_layer`; `WorkflowParticipatingAgent.participate` → `WorkflowLifecycle`; `ToolProposingAgent` → `ToolInvocationGovernance`; `EngineeringIntelligenceAgent.verify` | Workflow (lifecycle), Tool governance, Trace (each Agent authors its own) |
| Reads | `WorkflowMonitor`, `InvocationLedger`, `TraceReader`, `ToolRegistry.describe` | — |
| `docs.read` Tool | `ExternalTool` contract; returns `Success` / `Failure` | — |

The backend imports public surfaces only and nothing from `tools/`. AIOS
imports nothing from the backend (`test_fs01_application_surface`
`test_no_network_interface_exists_outside_the_full_stack` holds that no
listener exists outside `fullstack/`).

## Verification

| Evidence | Test |
|---|---|
| Every route of the contract is served, with its scope, and every scope is published | `test_every_route_and_scope_is_published` |
| A run is a real execution: the Freeze document is read through governance, verified, and three Trace records are written, one per acting Agent | `test_a_conformant_run`, `test_every_acting_agent_wrote_exactly_one_trace`, `test_the_step_actors_are_the_trace_authors` |
| A Tool failure drives the Workflow to `FAILED` with its reason | `test_scenario_c_a_tool_failure_fails_the_workflow` |
| An unexpected error still ends the Workflow lawfully, and hides its internals | `test_an_unexpected_step_error_still_ends_the_workflow` |
| Inputs are refused, not coerced: 8 invalid bodies → 400; oversize → 413; bad paging → 400 | `InputContract` |
| 404, 405 with `Allow`; 500 without internals; 503 when the Runtime is stopped | `Routing` |
| The console is served; nothing outside `frontend/` is | `StaticConsole` |

## Exit determination (`§14`)

| Criterion | Result |
|---|---|
| Backend builds | No build step; every module imports and runs under the suites |
| Required interfaces executable | All 11 routes, tested |
| Authentication / authorization boundary exists | Authenticator port, scope rule, audit (`security.py`); mechanism **FS-DP-02** |
| Core AIOS interfaces reachable through approved contracts | Runtime, Execution, Workflow, Tools, Trace: public surfaces only |
| Tests pass | 29 / 29 |
| No unresolved authorized implementation blocker | None |

**FS-03: EXIT CRITERIA MET.**
