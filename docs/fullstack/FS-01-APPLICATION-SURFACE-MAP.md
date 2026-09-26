# FS-01 — AIOS Application Surface Map

| Field | Value |
|---|---|
| **Stage** | FS-01 AIOS Application Discovery (Act `§12`) |
| **Question** | What can AIOS actually expose and execute? |
| **Executable evidence** | `fullstack/tests/test_fs01_application_surface.py`: 12 tests, each running one row through its public contract or checking one absence against the code |
| **Sources** | Canonical contracts (`native_core/core/*`), existing implementation (`consumers/`, `tools/`), the roadmap S-02 (`docs/governance/source-supply/full-stack/`) |

The Act's rule for API design (`§12`) is applied row by row:

```text
Canonical Contract → Existing Implementation → Required Interface → API Contract
```

## 1. Executable capabilities

Each row is executed by the named test on a real, RUNNING Runtime.

| Capability | Canonical contract | Implementation | Test |
|---|---|---|---|
| Runtime lifecycle and status | `Runtime` (`runtime/contract.py`) | `AIOSRuntime`, `bootstrap_runtime` | `test_runtime_lifecycle` |
| Execution session | `Execution` (`runtime/execution/contract.py`) | `create_execution_layer` | `test_execution_is_minted_by_the_running_runtime` |
| Agent-Instance action → one durable Trace | `Agent`; `TraceRecord` (INV-4/5) | `consumers/observation.TracedAction`; `TraceWriter` over `LocalAppendOnlyStorage` | `test_an_agent_action_writes_exactly_one_durable_trace` |
| Workflow execution, success and failure | `WorkflowLifecycle`, `WorkflowMonitor` (`FD-P9-001`) | `WorkflowParticipatingAgent` | `test_workflow_lifecycle_success_and_failure` |
| Governed Tool invocation | `ToolInvocationGovernance` (`FD-P8-001`) | `ToolProposingAgent` | `test_tool_governance_distinguishes_four_outcomes` |
| Decomposition of work into ordered sub-steps | `Agent` (`E5-2`) | `CognitiveIntelligenceAgent` | `test_cognitive_decomposition` |
| Artifact verification against stated criteria | `Agent` (`E5-3`, Testing) | `EngineeringIntelligenceAgent` | `test_engineering_verification` |
| Knowledge and Memory hosted by Runtime | `Runtime.knowledge`, `Runtime.memory` | composition roots | `test_knowledge_and_memory_are_hosted_while_running` |

## 2. Non-executable architectural claims

Named in the architecture or the roadmap, **not implemented**. None is built
by redefining a core boundary (NC-01).

| Claim | Why it is not executable | Class |
|---|---|---|
| Governed creation of Agent Definitions and Instances (the Agent Factory) | Reserved to the Architect (Freeze `§13`; Blueprint `§3`). The `agent` boundary exports the contract only (`test_the_agent_boundary_offers_no_governed_creation`). `tools/agent_instance_registry.py` exists, but its authority is `FD-P11-001 §7`, scoped to P11-W4 | **Architect-reserved** |
| Persistent Workflow state across processes | `FD-P9-001 §12.4`: lifecycle state is in-process; *"need not introduce a database … persistence engines"* | By design |
| Any concrete Tool | None is registered outside tests (`test_no_concrete_tool_is_registered_outside_tests`) | Gap; buildable (§5) |
| Network API, events, sessions for users | No listener exists (`test_no_network_interface_exists_outside_the_full_stack`) | Gap; buildable (FS-03) |
| Database | No driver or schema (`test_no_database_driver_exists`) | **Architect-reserved** (D2) |
| Identity, authentication, user roles | No entity is ratified (Freeze `§10`) | **Architect-reserved** (D2) |
| Deployment, networking, scaling, observability stack | Freeze `§10` | **Architect-reserved** (D2) |
| Trace status `escalation` | Ratified vocabulary with no producer (`consumers/observation.py`) | Recorded finding, unchanged |

## 3. Application surfaces

What an application layer can expose today without inventing semantics.

| Surface | Reads | Acts | Backing contract |
|---|---|---|---|
| System / Runtime | identity, lifecycle state, hosted subsystems | — | `Runtime` |
| Workflows | catalog of runnable compositions; runs, lifecycle states, outcomes | **start a run** | `WorkflowLifecycle`, `WorkflowMonitor`, `WorkflowParticipatingAgent` |
| Tools | registered Tools, lifecycle state, contract; invocation ledger | via Workflow steps only | `ToolRegistry`, `InvocationLedger` |
| Traces | every Trace record, in append order | — | `TraceReader` |
| Governance / audit | the application's own access decisions | — | application audit ledger (FS-06) |
| Knowledge, Memory | hosted-subsystem availability | — | `Runtime.knowledge`, `Runtime.memory` |
| Agents | the Agent Instances that act in a Workflow, as named by its steps and its Traces | **create: no** (Agent Factory reserved) | `AgentInstanceRef`; Trace `agent_instance` |

## 4. Required interfaces

| Interface | Needed for | Built in |
|---|---|---|
| AIOS contract adapter: one module holding the Runtime and calling contracts | every surface | FS-03 `fullstack/backend/aios.py` |
| HTTP API with a published contract | Frontend, external clients | FS-03 `fullstack/backend/api.py` |
| Authenticator port + scope authorization | every non-health route (NC-11) | FS-03 / FS-06 `security.py`; mechanism FS-DP-02 |
| Durable run and audit records | runs after restart; audit evidence | FS-04, over the certified `StorageFacility` |
| One concrete Tool | a Workflow that reaches a Tool (Act FS-07 Scenario B) | FS-03 `docs_tool.py` |

## 5. Implementation gaps, classified

| Gap | Class | Disposition |
|---|---|---|
| No network API | Buildable under the Act | FS-03 |
| No frontend | Buildable | FS-05 |
| No concrete Tool | Buildable: a read-only Tool confined to `docs/`, registered by the application's composition as operator configuration, invoked only through governance | FS-03 |
| No persistent application records | Buildable over the existing append-only `StorageFacility`; **no database** is introduced | FS-04 |
| Authentication mechanism | **Architect-reserved** | FS-DP-02; the backend ships a port that refuses every request |
| Database for production | **Architect-reserved** | FS-DP-01 |
| Networking, deployment, scaling, observability | **Architect-reserved** | FS-DP-03 … FS-DP-06 |
| Agent creation from the application | **Architect-reserved** | FS-DP-07 |

## 6. Findings on the roadmap source (S-02)

- The roadmap calls its decomposition *"candidate"*, *"belum saya anggap
  sebagai final architecture"*. It is used as sequence and intent, not as
  architecture.
- It states that AIOS sources record Supabase as *"Third Party / Wave
  Production"*, citing a conversation marker (`fileciteturn2file4`) that
  resolves to nothing in the repository. The only Supabase document in the
  repository is historical external-evidence research
  (`history/research/AIOS_DR_VALIDATION_SUPABASE_v1.0.md`): *"No Adopt, No
  Reject"*. The claim is recorded as **unverified**; D3-A's naming of Supabase
  rests on the Founder's decision, not on it.
- Its principle, *"Frontend tidak boleh berbicara langsung dengan Runtime
  internals"*, matches the Act's boundary rule (`§13`) and is adopted.

## 7. Exit determination (`§12`)

| Criterion | Result |
|---|---|
| Executable capabilities identified | §1 |
| Non-executable architectural claims identified | §2 |
| Application surfaces identified | §3 |
| Required interfaces identified | §4 |
| Implementation gaps classified | §5 |
| No unresolved authorized discovery task remains | None remains |

**FS-01: EXIT CRITERIA MET.** Advance to FS-02.
