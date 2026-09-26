# FS-07 — Full Stack Integration: Evidence

| Field | Value |
|---|---|
| **Stage** | FS-07 Full Stack Integration (Act `§18`) |
| **Tests** | `fullstack/tests/test_integration.py`: frontend units, Scenarios B and C over a real loopback socket, and the console in Chromium (12 checks) |
| **Authenticator in these tests** | the **test-only** `TokenAuthenticator` (`fullstack/tests/support.py`). Production has none until FS-DP-02 |
| **Screenshots** | `docs/fullstack/evidence/e2e/01…05` |

## Mandatory scenarios (Act `§18`)

| Scenario | Path exercised | Result |
|---|---|---|
| **A — Agent** | *User → Create Agent → Backend → AIOS Agent Capability → Persist → Result* | **BLOCKED.** Governed Agent creation is Architect-reserved (the Agent Factory); package **FS-DP-07** |
| **B — Workflow** | Browser → `POST /api/v1/runs` → authenticate, authorize, audit → `AIOSApplication.start_run` → Execution minted by the RUNNING Runtime → `WorkflowParticipatingAgent` → `WorkflowLifecycle` (defined → ready → running) → step 1: `ToolProposingAgent` → `ToolInvocationGovernance` → `docs.read` → step 2: `EngineeringIntelligenceAgent.verify` → `SUCCEEDED` → three Trace records → run record appended → result rendered | **PASS**: browser check *"scenario B"*; `OverTheWire.test_scenario_b_and_c` |
| **C — Failure** | Tool execution failure → `StepFailed` → `WorkflowLifecycle.fail` → Trace records with status `failure` → run record → backend → *"docs.read execution_failure: …"* in the console | **PASS**: browser check *"scenario C"*; `test_scenario_c_a_tool_failure_fails_the_workflow` |

Scenarios found in the actual capabilities (`§18`: *"Additional scenarios
shall be discovered"*): the non-conformant document (a successful run with
`conformant: false`), the governance refusal of an ungranted scope, and the
hostile input rendered inertly. All are tested.

## Exit determination (`§18`)

| Criterion | Result |
|---|---|
| End-to-end execution succeeds | B and C, in a browser, over a socket |
| State persists correctly | run records, Trace and audit across restarts (FS-04) |
| Traces are generated | one per acting Agent; ranges shown per run |
| Failures are observable | Scenario C in the console |
| Governance is enforced | Tool governance ledger; scope refusals in UI and API |
| Frontend reflects actual backend / AIOS state | states, steps and Traces come from the backend |
| Integration tests pass | 4 / 4 (13 unit and 12 browser checks inside) |

**FS-07: EXIT MET for Scenarios B and C. Scenario A is BLOCKED (FS-DP-07).**
