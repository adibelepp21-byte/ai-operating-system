# AIOS Operations — live operational state

This directory holds **live** operational state: records that are meant to
change as the system runs. It is deliberately outside every phase directory.

**Why it exists.** Until `GOAL-V2-002`, runtime observations were published into
`docs/architecture/p12/runtime-observations/`. `FD-P12-006` certified P12, so
that directory became certified evidence. An observation is a live projection
(*"these files state what was last observed"*), so each run rewrote certified
evidence. A phase's certification must freeze its evidence and nothing live.
Live state therefore lives here, where no phase certification can capture it.

| Path | What it holds | Writer | Readers |
|---|---|---|---|
| `runtime-observations/` | The latest published observation per runtime or workflow id | `tools/p12_runtime_observation.publish` (default root) | `tools/p12_runtime_observation.observations` and everything built on it (self-model *"What is running?"*, operational state, integration graph) |
| `trace-stores/` | Live durable Trace stores (`FD-FR2-001`; `GOAL-V2-002` W-1). `agency-w4-execution/` holds one record per delegated Agency step run inside a Runtime Execution, under the grant's recipient instance | `tools/w4_runtime_execution` (`TracedAction` through `trace_writer`, guarded) | `tools/p12_trace_registry` (`discover(LIVE_STORE_ROOT)`, `discover_by_origin`); `tools/p12_execution_chain_reader.verify_live`; P12-W2 `execution.recorded` (`live`, `FD-FR2-002`) |
| `execution-provenance/` | Live `ExecutionManifest`s, one per delegated Agency execution, written once (`FD-FR2-001`) | `tools/p12_execution_provenance.record(root=LIVE_MANIFEST_ROOT)` via `tools/w4_runtime_execution.record_manifest` | `tools/p12_execution_chain_reader.verify_live` / `live_summary`; P12-W2 `execution.provenance` (`live`), and through it P13 (`operational_state.executions`, `FD-FR2-002`) |
| `s-ops/` | S-OPS, the dedicated operational proof surface for E13-05 (`FDR-3`). One object, `S-OPS-01`: a scheduled window, OPEN or CLOSED. Defined in `s-ops/S-OPS-DEFINITION.md` | the operator provisioned it once. After that, only P13 wrote it, through the surface's two transitions under `P13-ENV-02`. That envelope is spent and retired (`FDR-4` `FD-B`), so nothing may write it now. It is retained as E13-05 proof evidence | P13 (`s_ops` source); anyone, via `python -m tools.s_ops.surface show` |

**How the live and certified observations relate.**
`p12_runtime_observation.observations()` reads P12's certified observations
(`docs/architecture/p12/runtime-observations/`, origin `certified-p12`) and this
live root (origin `live`). A live record supersedes a certified one for the same
id. The certified files are never written: `publish` routes through
`tools/p12_certified_evidence_guard.guard`, which refuses them. They are
verified byte-for-byte against
`docs/governance/AIOS_P12_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json`.

**How the live and certified execution chains relate (`FD-FR2-001`).** The
execution chain reader keeps two populations and never merges them:
`verify_all()` / `summary()` read P12's certified manifests against certified
records only, exactly as certified, and `verify_live()` / `live_summary()` read
the manifests here against the live trace stores, the live observations and the
Agency operational roots only. Every verdict carries its origin. The trace
registry's functions still default to P12's certified store, so the populations
the resident P12 verifiers count do not move.

**It started empty.** At the move, the certified root held two observations
written after certification, from commits `7f6120c` and `d18bac4`. Both came
from test-suite runs, not from real operation. They were not carried into this
root, and the certified files were restored to their certified bytes. The later
values remain in git history. The record is
`docs/governance/AIOS_GOAL_V2_002_P12_CERTIFICATION_INTEGRITY_RECORD_v1.0.md`.

This file carries no authority.
