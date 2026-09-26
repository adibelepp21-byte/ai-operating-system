# FS-04 — Data & State

| Field | Value |
|---|---|
| **Stage** | FS-04 Data & State (Act `§15`) |
| **Tests** | `fullstack/tests/test_data_and_state.py` (7) |
| **Store** | the certified `StorageFacility` (`LocalAppendOnlyStorage`), one append-only file per partition, under a data directory given at start. **No database is introduced** (FS-DP-01) |

## 1. Classification (Act `§15`)

| State class | Owner | Lifecycle | Storage | Access boundary | Persistent? |
|---|---|---|---|---|---|
| Runtime state | AIOS Runtime | boot → stop | in-process | `Runtime` contract | no |
| Execution state | AIOS Execution | one run | in-process | `Execution` | no |
| Workflow lifecycle state | AIOS Workflow boundary | define → terminal | in-process, by decision (`FD-P9-001 §12.4`) | `WorkflowLifecycle`, `WorkflowMonitor` | no |
| Session state (users) | — | — | none: no user session exists until FS-DP-02 | — | no |
| Trace | AIOS Trace | append, never change | partition `trace` | `TraceWriter` / `TraceReader` | **yes** |
| Knowledge | AIOS Knowledge | versioned | its own partitions (none written by this application) | Knowledge subsystem | yes |
| Memory | AIOS Memory | lifecycle | in-process | Memory subsystem | no |
| Tool invocation ledger | AIOS Tools | per Runtime | in-process (`FD-P8-001`: no persistence required) | `InvocationLedger` | no |
| Run records | Application | append at terminal state | partition `fullstack-runs`, format `fullstack.run/1` | `AIOSApplication.runs` | **yes** |
| Audit | Application | append per decision | partition `fullstack-audit`, format `fullstack.audit/1` | `AuditLedger` | **yes** |
| Configuration | Operator | per process | command line (`--data-dir`, `--host`, `--port`) | `__main__` | no |

**No generic schema** (NC-14): no `users`, `agents`, `messages` or
`documents` store exists. Only the three durable partitions are ever created
(`test_no_schema_beyond_the_classified_partitions`).

## 2. Integrity, migration, backup, recovery

| Requirement | Local store | Evidence |
|---|---|---|
| **Integrity** | append-only: persisted bytes only ever grow; a corrupt record fails the read closed (500), it is not skipped | `test_persisted_bytes_are_only_ever_appended_to`, `test_a_corrupt_record_fails_closed` |
| **Migration** | one format per record class, named in each record (`fullstack.run/1`, `fullstack.audit/1`). A later format is a successor read beside the old one, never a rewrite. No migration exists because none is needed yet | format fields in `aios.py`, `security.py` |
| **Backup** | copy the data directory | `test_a_copied_store_restores_every_record` |
| **Recovery** | start on the copy: every run, Trace and audit entry is back, and run numbering continues | same test; `test_runs_traces_and_audit_survive_a_restart` |
| **Traceability** | each run's Trace range holds exactly its own Runtime's records, across restarts | `test_each_run_maps_to_its_own_runtimes_traces` |

**In-process by design.** A restart forgets the Workflow monitor's states, and
the run records keep them (`test_workflow_lifecycle_state_is_in_process_by_design`).

## 3. Production persistence

Architect-reserved: FS-DP-01, which proposes a database *beneath*
`StorageFacility` with append-only enforced in the store itself. The Supabase
Free plan has no downloadable backups and pauses on inactivity (FS-08 `§3`).

## Exit determination (`§15`)

| Criterion | Result |
|---|---|
| State ownership established | `§1` |
| Persistence model implemented | local append-only store, tested |
| Migrations verified | one format version per class; nothing to migrate (`§2`) |
| Backup / recovery verified where applicable | local: verified. Production: **FS-DP-01** |
| Data integrity tests pass | 7 / 7 |
| State interfaces consumed by the backend | runs, traces and audit are served from the store |

**FS-04: EXIT CRITERIA MET for the local persistence model.** Production
persistence is carried to FS-08 as FS-DP-01.
