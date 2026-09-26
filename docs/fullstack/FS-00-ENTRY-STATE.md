# FS-00 — Full Stack Entry State

| Field | Value |
|---|---|
| **Program** | AIOS Full Stack Development & Operationalization Program (`ACT-CC-POST-P13-AIOS-FULL-STACK-001`, Register `§60`) |
| **In force from** | `FD-FS-001` (Register `§62`), 2026-09-26 |
| **Stage** | FS-00 Full Stack Entry Gate (Act `§11`) |
| **Repository state at entry** | branch `claude/aios-activation-authority-discovery-enq7bk`, commit `5bfa33b` |
| **Prepared by** | Claude Code (Co-Founder / CEO) |

The Act's `§5.4`: *"Claude Code shall not assume that architectural existence
means implementation existence."* Every "implemented" row below names the code
that implements it and the suite that executes it. FS-01 re-executes each
executable claim through its public contract
(`fullstack/tests/test_fs01_application_surface.py`).

## 1. Entry criteria (`§11`)

| Criterion | Result | Evidence |
|---|---|---|
| This Act authorized | **MET** | `FD-FS-001` D1-A |
| Repository accessible | **MET** | clean clone, full history |
| Governance state discoverable | **MET** | Register `§1`–`§63`; the phase reader (`tools/p12_phase_authorization.py`) |

## 2. Phase and platform state

| Subject | State at entry | Source |
|---|---|---|
| P1–P9 | Realized as the eleven Native Core boundaries (`native_core/core/`) and the Phase 5–9 consumers (`consumers/`) | Blueprint `§3`; the conformance suites |
| P10, P11, P12 | Certified evidence, pinned by manifest | `AIOS_CERTIFIED_EVIDENCE_MANIFEST_INDEX_v1.0.json` |
| P13 | **CLOSED** (`FDR-G3`, Register `§40`–`§41`); certified evidence pinned | `…_INDEX_P13_v1.0.json`; `p12_phase_authorization.closures()` |
| Phase 14 | Does not exist; this program does not create it (Act `§2`, NC-21) | — |
| PD-01 … PD-10 | Platform Organization **CLOSED** (Register `§59`). PD-05 … PD-10 canonical baseline; PD-03 / PD-04 resident, not canonicalized | `platform_organization_closure_gate.py` |

## 3. Implementation inventory

Measured on the entry commit. Python 3.11 standard library only: the
repository declares **no third-party dependency** (no `requirements.txt`,
`pyproject.toml`, `package.json`, `Dockerfile` or CI configuration).

| Area | What exists | Executable? | Where |
|---|---|---|---|
| Runtime | `AIOSRuntime`: lifecycle `CREATED → INITIALIZED → RUNNING → STOPPED`, execution context, RUNNING-gated hosting of Knowledge, Memory, Tools, Workflows | **Yes**, in-process | `native_core/core/runtime/` |
| Execution | `create_execution_layer(runtime)` → `ExecutionSession`; `ExecutionConsumer` contract | **Yes**, in-process | `native_core/core/runtime/execution/` |
| Agent | `Agent` contract; `AgentDefinition` and `AgentInstance` data contracts. **Governed creation (the Agent Factory) is reserved to the Architect** | Contract yes; creation **no** | `native_core/core/agent/` |
| Concrete agents | Reference, Workflow-participating, Tool-proposing, Knowledge-consuming, Memory-consuming, Cognitive Intelligence (decomposition), Engineering Intelligence (construct, verify) | **Yes** | `consumers/` |
| Workflow | Lifecycle `DEFINED → READY → RUNNING → SUCCEEDED / FAILED`; `WorkflowMonitor`; composition of steps | **Yes**, state in-process only (`FD-P9-001 §12.4`) | `native_core/core/workflow/` |
| Tools | Registry (lifecycle authority), `ToolInvocationGovernance` (four dispositions), `ToolBoundary`, in-process ledger | **Yes**; **no concrete Tool is registered anywhere outside tests** | `native_core/core/infrastructure/tool_*` |
| Trace | `TraceRecord` (ten ratified fields), append-only `TraceWriter` / `TraceReader` | **Yes**, durable (append-only files) | `native_core/core/trace/`; `consumers/observation.py` |
| Knowledge | Repository, admission, retrieval, versioning; infrastructure-backed store | **Yes** | `native_core/core/knowledge/` |
| Memory | Lifecycle (admit, update, consolidate, expire, invalidate), retrieval, store | **Yes**, in-process | `native_core/core/memory/` |
| Governance | `GovernanceReview`, `ReviewDecision`, `HumanAuthority` | **Yes** | `native_core/core/governance/` |
| Storage | `StorageFacility`; `LocalAppendOnlyStorage` (one append-only file per partition) | **Yes** | `native_core/core/infrastructure/storage.py` |
| P13 / S-OPS | Bounded P13 cycle under recorded envelopes; S-OPS operational proof surface | **Yes**, CLI | `tools/p13/`, `tools/s_ops/` |
| Governance machinery | Gates, verifiers, probes, indexes | **Yes**, CLI | `tools/` |

## 4. What does not exist

| Absent | Consequence for the program |
|---|---|
| Any network interface: no HTTP server, socket listener or API anywhere outside tests | FS-03 builds the first one |
| Any frontend or UI | FS-05 builds the first one |
| Any database, database driver or schema | FS-04; the database itself is Architect-reserved (D2) |
| Any identity, authentication or session mechanism | FS-06; Architect-reserved (D2) |
| Any deployment, container, IaC or CI/CD configuration | FS-08; Architect-reserved (D2) |
| Any observability stack (metrics, logs, alerting) beyond Trace | FS-08; Architect-reserved (D2) |
| Any dependency manifest | FS-03 decides; the backend stays on the standard library |
| Governed Agent creation (Agent Factory) | Act FS-07 Scenario A (*"Create Agent"*) meets an Architect reservation |

## 5. Tests and build system

- **Build:** none needed; nothing is compiled or packaged.
- **Tests:** `python3 -m unittest discover`, four suites. At the last full run
  (commit `78d67e5`): `tools/tests` 1,920 · `native_core` 801 · `consumers`
  276 · `tools/bounded_exception/tests` 29, all OK.
- **Write probe:** `tools/certified_write_probe.py` runs every entry point in
  a disposable worktree and fails any certified write. New entry points must
  exit quickly when run with no arguments.

## 6. Protected roots

`tools/p12_certified_evidence_guard.protected_roots()` and the certified
evidence manifests define what may not be written. The Full Stack program
writes only to new paths: `fullstack/`, `docs/fullstack/`, new ADRs and
Register appends.

## 7. Authority map

| Class | Matters |
|---|---|
| **Built autonomously under the Act** | Application-surface code, API contract, service adapters over existing contracts, frontend, tests, documentation, in-repo configuration, read-only connector discovery |
| **Architect-reserved (D2): ADR only** | Database · Identity and Authentication · Networking · Deployment · Scaling · Observability |
| **Architect-reserved (canon)** | Agent Factory: governed creation and registration of Agent Definitions and Instances (Freeze `§13`; Blueprint `§3`) |
| **Founder-reserved** | Production release (D4-A) · Final System Acceptance (A19) · spending (D3-A) |
| **External dependency** | S-01 *AIOS Transition Manifest* (D5-A, pending supply) · any paid Vercel or Supabase capacity |

## 8. Exit determination

Act `§11` exit: *what exists · what is implemented · what is executable ·
what is missing · what is blocked · what is Founder-reserved · what can be
built autonomously* — documented in `§3`, `§3`, `§3`, `§4`, `§7`, `§7`, `§7`.

**FS-00: EXIT CRITERIA MET.** The entry map is persisted; FS-01 re-executes
its executable claims. Advance to FS-01.
