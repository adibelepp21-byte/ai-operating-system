# FR-2 — Agency Runtime & Trace Integration (FD-FR2-001): Record

| Field | Value |
|---|---|
| **Authority** | `docs/governance/acts/FD-FR2-001-AGENCY-RUNTIME-TRACE-INTEGRATION-AUTHORIZATION.md` (verbatim; content sha256 `054fb8a2a33add3724c365087309da61be137247832d8c17f0ba5d0cbb2ac38d`): FQ-FR2-1 = **Option A**, bounded FDR-G1 maintenance on the GOAL-V2-002 live / certified precedent. Register `§163` (decision), `§164` (this result). Predecessor: FR-2 discovery (`FR2-RUNTIME-TRACE-DISCOVERY-RECORD-2026-10-04.md`, `§161`–`§162`) |
| **Result** | **FR-2 CONSTRUCTED / VERIFIED.** Delegated Agency work now runs through the existing path: Agent Instance → Delegation → `W4Executor` → Execution Contract (`Agent` / `ExecutionConsumer`) → Execution Layer → Runtime → `TracedAction` Trace + `ExecutionManifest` → Result → Verification → CEO Decision → Plan Outcome.<br>• One real execution (`2adef08b8efa4549`) took that path. The independent chain reader joins **7 / 7** edges for it from persisted bytes, in a fresh process.<br>• Every `FD-FR2-001 §12` item holds.<br>• No `§13` stop condition was reached |
| **Evidence** | • Baseline: `evidence/fr2c_baseline.py` → `evidence/FR2C-BASELINE-2026-10-04.json`, captured at `2571089` before any code changed.<br>• The execution: `evidence/fr2_runtime_execution_run.py`; its result `operations/w4-s4-plan-outcome/fr2-runtime-run.result.json`.<br>• Verification: `evidence/fr2c_verification.py` → `evidence/FR2C-VERIFICATION-2026-10-04.json`, **all_ok**, fresh process.<br>• Tests: `tools/tests/test_fr2_runtime_trace_integration.py` (36; 10 code mutations, all caught) |
| **Code changed** | • New: `tools/w4_runtime_execution.py` (the authority side) and `agency_runtime_execution.py` at the repository root (the Agent side and its binding). Together they are the integration; there is no new subsystem.<br>• Extended, certified answers unchanged: `tools/p12_execution_chain_reader.py`, `tools/p12_trace_registry.py`, `tools/p12_execution_provenance.py`.<br>• `native_core`, `consumers`, P12-W2, P13 and the served tree are **unchanged** (byte-identical to the baseline) |

---

## A. What was built

```text
Agent Instance ── Delegation ── W4Executor (grant, instance and scope re-checked per step)
                                     │
Runtime (RUNNING) ─► create_execution_layer ─► Execution (runtime_id, execution_sequence)
                                     │
               DelegatedStep(Agent).participate(execution)        ← the Execution Contract
               (agency_runtime_execution.py; injected into tools/w4_runtime_execution.py)
                                     │
                 TracedAction(writer, agent_instance=<grant recipient>, runtime=<Execution's runtime>)
                                     │
                                  perform(step)                    ← the delegated work
```

The integration has five parts. `DelegatedStep` is in `agency_runtime_execution.py` at the root; the rest is in `tools/w4_runtime_execution.py`. Each is a use of an existing mechanism:

| Part | What it does | Existing mechanisms used |
|---|---|---|
| `DelegatedStep(Agent)` | Takes part in one `Execution`. Refuses anything that is not a real `Execution` whose Runtime is RUNNING. Runs `perform` inside a `TracedAction` under the grant's recipient instance and the Execution's runtime id | `Agent` (an `ExecutionConsumer`), `Execution` / `ExecutionContext`, `TracedAction`, `W4Executor.execute_step` |
| `RuntimeHostedExecutor` | Takes the participant **by injection** and requires it to be a native-core `Agent`. Builds a **fresh** `Execution` for each step, then lets the step participate. `execute_plan` keeps W4's rule: a refused step is recorded as an escalation and the remaining authorized work continues | `create_execution_layer` (RUNNING-only), `W4Executor` |
| `hosted_runtime` | Starts a real Runtime through the composition roots. Publishes its observation at RUNNING and at STOPPED, under its own id | `build_default_infrastructure`, `create_runtime`, the Runtime lifecycle, `p12_runtime_observation.publish` |
| `run_hosted_plan` | The hosted **run path**. It executes a plan through `RuntimeHostedExecutor`, then routes `report.refusals` through the one existing wiring, so each refusal becomes an organizational escalation joined to its grant. Like `W4Executor`, the executor itself keeps no handle on persistence | `join_refusals_to_grants` (`ACT-CC-P12-005`), the same call `tools/w4_first_run.py` and the `tools/w1_*_run.py` paths make |
| `record_manifest` / `trace_writer` | Writes the existing `ExecutionManifest` (no new field) to the live root; opens a live Trace store. Both refuse a certified root through the guard | `ExecutionManifest`, `record()`, `TraceWriter`, `LocalAppendOnlyStorage`, `p12_certified_evidence_guard.guard` |

**Boundary (`§3`).** The delegated step reaches the Runtime only through the `Execution` it is handed. It reads the runtime id and execution sequence from the Execution's context. The Runtime is driven only through its public lifecycle and the composition roots.

**Identity (`§6`; G4).** The Trace actor is the grant's `recipient_instance`. `TracedAction` already takes the instance as an argument, so G4 is resolved **within the existing mechanism**. `EngineeringIntelligenceAgent.participate`, which traces its definition key, is not used on this path and was not changed. No Trace Domain Model field changed.

**What is traced, and when.**
- Authorization comes first. `W4Executor.execute_step` re-checks the grant, the instance and the scope. A refusal raises before any work is done, so work that did not happen writes no Trace.
- Only `perform` runs inside the `TracedAction`, so the Trace record is the action itself.
- Status uses the existing mapping: `perform` returns → `success`; `perform` raises → `failure`, and W4 records the same FAILURE.

## B. Readers extended (`§5`)

| Reader | Extension | Certified semantics |
|---|---|---|
| `p12_execution_chain_reader` | Adds a **live** population:<br>• `LIVE_MANIFESTS` / `LIVE_TRACE_STORES` / `LIVE_OBSERVATIONS` (`docs/operations/…`);<br>• the Agency grants, found by shape beneath `docs/architecture/agency/operations`.<br>`verify_manifest(payload, origin)` resolves each reference against **that population's roots only**. `verify_live()` / `live_summary()` are new, and every `ChainVerdict` carries its `origin` | `verify_all()` / `summary()` still read P12's certified manifests against certified records. They return the same verdicts as at baseline: 5 / 5 JOINED, edge details identical. A live manifest cannot be completed by certified records, nor a certified one by live records (both tested) |
| `p12_trace_registry` | `LIVE_STORE_ROOT` (`docs/operations/trace-stores`); `discover_by_origin()` keeps both populations under their origins | Every function still defaults to `STORE_ROOT`. `what_has_run()` is identical to baseline (16 records); the live store is absent from it |
| `p12_execution_provenance` | `LIVE_MANIFEST_ROOT` (`docs/operations/execution-provenance`) | `record()` and `manifests()` keep the certified default. `record()` still refuses the certified root |

No reader merges live and certified authority. Domain ownership is unchanged. The chain reader still imports nothing from the writer, and the independent consumer verifier is untouched.

## C. The authorized execution (`§2`, `§12` Provenance)

`evidence/fr2_runtime_execution_run.py` runs once, in the S-4 operational root (as MR-S5-1 did). It runs under existing authority only:
- the instance is registered in memory, and its record on disk is not written;
- the grant is issued by the authorized delegator under `FD-P11-001 §9`;
- the CEO decides under FD-AGENCY-001 Q4-A.

| Link | Value | Persisted in |
|---|---|---|
| Founder Goal | `founder-fr2-runtime-trace`: *"The existing provenance model must be used rather than replaced."* A verbatim line of `FD-FR2-001 §2`, accepted by `founder_goal_refusal` | `planning.state.json` |
| Plan | `founder-fr2-runtime-trace-plan-0` (CEO, V2 A01): the delegated step, then the CEO review | `planning.state.json` |
| Plan Step | `verify-runtime-path-mechanisms` | the plan; the grant's `work_scope` |
| Delegation | **`2adef08b8efa4549`**: delegator Claude Code / AIOS Co-Founder, `FD-P11-001 §9`, bound to the plan | `2adef08b8efa4549.delegation.json` |
| Agent Instance | `engineering-intelligence-instance-001` (REGISTERED; definition `engineering-intelligence-agent` 1.0) | the root's instance record (unchanged) |
| Execution | outcome `success`, *"8 of 8 mechanisms used"* | `2adef08b8efa4549.evidence.json` |
| Runtime | `agency-runtime-2adef08b8efa4549`, `execution_sequence` 0. Observed RUNNING, then STOPPED (origin `live`) | evidence `runtime`; `docs/operations/runtime-observations/` |
| Trace | `agency-w4-execution#0`: actor `engineering-intelligence-instance-001`, runtime `agency-runtime-2adef08b8efa4549`, status `success` | `docs/operations/trace-stores/agency-w4-execution/trace` |
| Manifest | `agency-2adef08b8efa4549-verify-runtime-path-mechanisms`: goal, plan, grant, instance, Trace position, runtime, outcome | `docs/operations/execution-provenance/` |
| Result | `EngineeringIntelligenceAgent.verify` against `tools/w4_runtime_execution.py` as it stood at the run (`521a976`): 8 of 8 named mechanisms present | evidence `criteria`; manifest `outcome` |
| Verification | `plan_completion` **met** | derived from the evidence |
| CEO Decision | **ACCEPT** → COMPLETED (`FD-P11-001 §15.2`; V2 A09 / A11; operational, not Founder acceptance) | live ledger `w4-dispositions/…/2adef08b8efa4549.disposition.json` |
| Plan Outcome | **completed**; decision faults none | `plan_outcome`; `fr2-runtime-run.result.json` |

**The work was real.** The Engineering Intelligence instance checked that the integration module uses each existing mechanism the Goal names. The result was whatever the module carries; nothing chose it.

**Dry run.** Before the real run, the whole script ran once in a throwaway git worktree, which was then removed. The repository was not touched.

## D. `FD-FR2-001 §12` verification

`evidence/FR2C-VERIFICATION-2026-10-04.json` (fresh process): **all_ok**.

| `§12` area | Item | Result |
|---|---|---|
| Runtime | Agency work actually enters Runtime | ✔ runtime id + execution sequence in the evidence; live observation present |
| | Runtime participation evidenced | ✔ Trace runtime = manifest runtime = observation subject |
| | Direct function-call bypass prevented | ✔ the authority side never calls `perform`; the Agent calls it exactly once, inside its `TracedAction`, inside `participate`. A stopped Runtime refuses (`RuntimeNotRunning`); an imitation Execution is refused (`TypeError`); a participant that is not an `Agent` is refused; 0 `perform` calls |
| Trace | Produced by the existing mechanism | ✔ `TracedAction` → `TraceWriter` |
| | Identifies the actual Agent Instance | ✔ the grant recipient = the instance record; ≠ definition key |
| | Associated with the execution | ✔ manifest and evidence name the same `store#ordinal` |
| | Associated with the Runtime observation | ✔ |
| Manifest | Produced by the existing mechanism | ✔ existing schema only, live root |
| | Goal / Plan / Delegation / Instance / Execution / Trace reconstructable | ✔ chain reader JOINED |
| Provenance | Founder Goal → Plan → Plan Step → Delegation → Agent Instance → Execution → Runtime → Trace → Result → Verification → CEO Decision → Plan Outcome | ✔ each link (`§C`), and the 7-edge chain in a **fresh process** |
| Observability | Existing readers observe live Agency execution | ✔ `verify_live()`; `discover_by_origin()[live]` |
| | Certified historical evidence remains distinguishable | ✔ certified chain verdicts, trace population and manifests identical to baseline; every certified verdict carries origin `certified-p12` |
| | P13 does not acquire a second state authority | ✔ P13 and P12-W2 code unchanged; P12-W2 contract identical; its execution projections unchanged |

## E. Negative controls (`§12`) and mutations

| Control | Established by |
|---|---|
| Direct function execution cannot masquerade as Runtime execution | A plain `W4Executor` call writes no Trace. A manifest pointing at a Trace or observation that is not there DANGLES at EXECUTION and OBSERVATION |
| A fabricated Agent Instance cannot pass provenance verification | A grant to an unregistered instance is refused at issue. The real chain with only the Trace actor replaced by `fabricated-instance-999` → DELEGATION→EXECUTION **DANGLING** |
| An Agent Definition cannot substitute for the Agent Instance | The same, with the definition key `engineering-intelligence-agent` → **DANGLING** |
| Hidden P13 / reader dependencies cannot bypass consumer measurement | The integration and the run script import nothing from P12-W2 or P13 (AST). Consumer measurement identical to baseline: 4 consumers, 5 importers, independent verifier 4 / 4 AGREE |
| Certified historical evidence cannot be mutated | Certified surfaces byte-identical; integrity faults 0; certified git status clean. The trace writer and `record()` refuse certified roots, and the trace writer refuses **before** touching storage. The process-wide barrier also refuses independently |
| Live data cannot silently become certified data | A live manifest verified as certified does not join. It is absent from `verify_all()`; `record()` refuses to write it as certified |

**Mutations** (each applied in a throwaway worktree of the final layout, then the FR-2 suite run):

| # | Mutation | Result |
|---|---|---|
| M1 | Trace the definition key | 2 failures |
| M2 | Call `perform` directly (bypass the Execution) | 1 failure, 6 errors |
| M3 | Participant accepts any object as the Execution | 1 error |
| M3b | Authority side accepts a participant that is not an `Agent` | 1 error |
| M4 | Resolve the live chain on certified roots | 3 failures |
| M5 | Merge live into the certified population | 1 failure |
| M6 | Trace writer without the guard | 1 failure, caught by the guard-order test. The first pass survived because the process-wide barrier refused the same write; the test was added so the guard itself is held |
| M7 | Hidden P12-W2 import in the integration | 2 failures |
| M8 | Trace refused steps too | 5 failures |
| M9 | Refusals not routed to escalations | 1 failure |

## F. Data changes, separated from certified semantics

| Changed (data, expected) | Detail |
|---|---|
| `docs/operations/trace-stores/`, `docs/operations/execution-provenance/` | new live roots, one record each |
| `docs/operations/runtime-observations/` | one observation (`agency-runtime-2adef08b8efa4549`, STOPPED) |
| `docs/operations/README.md` | the two live roots and the two-population rule, documented |
| Agency S-4 root | the grant, the evidence, `planning.state.json` (the FR-2 goal and plan), `fr2-runtime-run.result.json`; the live-ledger disposition |
| P12-W2 `runtime.observed` | Reads the live observation root since GOAL-V2-002. It now lists 11 observations, adding the Agency runtime as TERMINATED; nothing is LIVE and every earlier entry is unchanged. This is existing observability seeing the Agency runtime, through an existing interface |

**Unchanged (certified semantics):**
- certified roots `p10`, `p11`, `p12`, `p13`, `platform-organization`, byte-identical;
- the chain reader's certified verdicts;
- the trace registry's certified population;
- certified manifests;
- the P12-W2 contract (8 sources, provider `UNRESOLVED (F-17)`) and its execution projections;
- P13;
- consumer measurement;
- `native_core`, `consumers`, the Execution Contract, `TraceRecord`, the `ExecutionManifest` schema, the chain-edge rules;
- authority; deployment PAUSED.

## G. Boundaries and stop conditions (`§11`, `§13`)

| `§13` stop condition | Reached? |
|---|---|
| New Runtime / Trace subsystem | No: existing Runtime, Execution Layer, `TracedAction`, `TraceWriter` |
| Execution Contract semantics change | No: `participate(execution) -> None`, unchanged |
| Trace Domain Model field change | No |
| Certified verifier semantics change | No: certified functions return the same answers; new answers are new functions with origin `live` |
| Certified architecture or P13 certified architecture change | No |
| Runtime ownership change | No: central; driven through its own lifecycle |
| New authority | No: FD-P11-001 §9, FD-AGENCY-001 Q4-A, the existing instance |
| Persistent execution identity needing a new mechanism | No. Persisted through existing writers: evidence `details`, manifest, observation |
| Live / certified separation needing a certified-semantic change | No: two populations, separately resolved |

`§11`: no new subsystem, capability, Agent or delegation authority. One grant was issued under the existing authority, for the Founder Goal quoted from this decision. Deployment remains PAUSED.

## H. Gap register after construction

| Gap | Before | Now |
|---|---|---|
| G1 (R3) Agency bypasses Runtime / Trace | open | **Closed for the authorized path.** `RuntimeHostedExecutor` is that path. The plain `W4Executor` remains for existing callers, and its runs cannot join a chain (`§E`) |
| G2 (R8) certified-only readers | open | **Closed:** live population read beside the certified one, never merged |
| G4 (R4) definition key traced | open | **Closed for the Agency path** within the existing mechanism. The native consumer is unchanged |
| G8 fabricated actor accepted at write | open | The Agency path never writes for an unregistered or retired instance: W4 refuses first. `TracedAction` itself still accepts any actor; the join rejects it |
| **G3** (R5) Runtime state / execution sequence | acknowledged | **Residual (`§14`).** The Runtime object is not reconstructable after its process. What persists is its observation and, in the evidence, its id and execution sequence, through existing writers. Runtime persistence was not redesigned |
| **G5** (R6) P13 execution visibility | acknowledged | **Residual.** P13 sees Agency *state* (FR-1) but not Agency *execution*:<br>• P12-W2 `execution.recorded` / `execution.provenance` read the certified roots by their declared contract;<br>• P13's trace source reads the certified store.<br>Reaching P13 would change the P12-W2 declared read paths or the P13 source model, which `§10` / `§13` reserve. Not required by `§12`; returned as the next frontier |
| **G6** (R4) Trace status vs verification | acknowledged | **Residual for the native consumer** (unchanged). On the Agency path the Trace status equals the W4 outcome by the existing mapping. The CEO's verification remains separate (`plan_completion`), as it should |
| **G7** escalation status has no producer | acknowledged | **Residual.** `TracedAction` unchanged; a refused step is not traced and is recorded as an escalation in W4 evidence |

## I. Tests and regression

| Suite | Result |
|---|---|
| `test_fr2_runtime_trace_integration` | 36 OK: Runtime participation, no bypass, Trace identity, manifest and chain, live / certified separation, no hidden consumer, the authorized execution read back (including fresh process) |
| Neighbouring suites (P12 chain, trace registry, certification integrity, certified-write closure, FR-1, MR-S5-1, W4 plan outcome, Founder goal, E12 measurement, integration graph, state verification, consumer measurement, CG7, guard, self-model) | OK |
| `test_escalation_subject_integrity` | 41 OK, with its population extended by one (`§I.1`) |
| `test_p11_governance_boundary` | 26 OK, with its declared surface set extended by one (`§I.1`) |
| `test_e11_measurement_currency`, `test_p12_runtime_verification` | at HEAD: 2 pre-existing failures (`aios_corpus_health_run.py` symbol check); OK (`§I.1` items 5–6) |
| **Complete regression** | **95 suites, 3582 tests**: `tools/tests` 91 / 2092; `consumers/tests` 276 OK; `tools/bounded_exception/tests` 29 OK; `fullstack/tests` 384; `native_core` 801 OK.<br>• Comparable to FR-1's figure (`tools` + `consumers`, 2332): **2368 = 2332 + 36 FR-2 tests**.<br>• The only failures at HEAD are pre-existing, each also failing at the construction baseline `2571089`:<br>  – `test_e11_measurement_currency`: 2. There were 4 at baseline; two are masked by import order, not fixed;<br>  – `test_p12_governance_evidence_verification`: 1;<br>  – `fullstack` NC-04, NC-05, NC-19: 3 |

### I.1 What the regression caught

The first full regression found one new failure: `test_escalation_subject_integrity` → `test_the_list_covers_every_production_execution_path`. That control (`ACT-CC-P11-015 §19`) discovers, from source, every production module that constructs a `W4Executor`. It requires each one's refusals to reach organizational state through `join_refusals_to_grants`, and it found `tools/w4_runtime_execution.py`.

The control was right. The hosted path is now the authorized Agency execution path, and its refusals were reaching only the W4 report.
- **Fix:** `run_hosted_plan`, the hosted run path, routes `report.refusals` through the existing wiring.
- **Control:** the module was added to the control's population, so every one of the control's checks now applies to it. The population was extended, not narrowed. The module was not hidden from the scan, and no check was weakened.
- **Test:** `test_the_hosted_run_path_makes_refusals_organizational_escalations` covers it.

The same regression found a second one: `test_p11_governance_boundary` → `test_the_declared_p11_surface_set_is_complete`. Every module under `tools/` that imports the planning package is a P11 handoff surface and must be declared. `tools/w4_runtime_execution.py` imports it, and authority crosses it (it cites `FD-P11-001 §9` when it routes refusals). It was declared in `P11_SURFACES`, as the guard's earlier catches were. The boundary's other checks over declared surfaces now run on it and pass, including *"every authority field crossing a boundary is a verified citation"*.

The complete regression, run across `consumers/tests` and `fullstack/tests` as well, found two more:

1. **The `tools/` ↔ `consumers/` boundary.** `consumers/tests/test_reference_agent.py` asserts that nothing under `tools/` imports `consumers`, and three consumer suites assert the reverse. `tools/w4_runtime_execution.py` imported `consumers.observation.TracedAction`. This is the same violation `tools/w4_first_run.py` once made, and it was resolved the same way:
   - the authority side takes its participant by injection and requires a native-core `Agent`;
   - the Agent side (`DelegatedStep`, which uses `TracedAction`) lives outside both regions, at the repository root (`agency_runtime_execution.py`), as `w4_first_execution.py` and `p12_w4_integrated_execution.py` do.
2. **The served tree.** The first placement of `DelegatedStep` was `consumers/delegated_step.py`. `fullstack/readiness.py` counts every module under `consumers/` as served code, so that file made the paused deployment's recorded Preview verification stale. The release gate then reported BLOCKED pending live re-verification (`fullstack` NC-16 / 18 / 20). `FD-FR2-001 §11` keeps deployment paused, and FR-2 changes nothing the deployment serves. The file was removed, the class moved to the root binding, and a test now asserts that the served tree is unchanged since the construction baseline.

Two more came from the root binding:

5. **Entry-point currency.** `test_e11_measurement_currency` treats every root `*.py` as a region-joining entry point, so it must define `main()`, and its imports from `tools` / `consumers` must still resolve.
   - `agency_runtime_execution.py` now has a read-only `main()`: it reports the live Agency execution chains and executes nothing.
   - It imports `from tools.w4_runtime_execution import …`, the form the check can verify.
   - The suite's remaining failures are its pre-existing ones. There are 2 now against 4 at the baseline only because importing this module happens to load `tools.p12_runtime_observation` first. That masks two of the four; it does not fix them.
6. **Reachability.** `p12_runtime_verification.reachability()` counts any non-test, non-root importer of a root entry point as *the system reaching a runtime*. My verification script imported the binding statically and moved that count from 1 to 2. An evidence tool must not enter the measurement it reads (the FR-1 lesson), so it now loads the binding by name. The count is 1 again.

After all six fixes, every control named here passes. The only failures left are the pre-existing ones (`§I`).

The one authorized execution (`§C`) ran a single in-scope step through `execute_step`, as MR-S5-1 did, and raised no refusal. It ran with the first layout (`tools/w4_runtime_execution.py` at `521a976`, holding `DelegatedStep` itself). The relayout moved that class unchanged in behaviour, and the mutation suite and verification were re-run on the final layout. The run's records are unchanged. Its script is kept byte-identical as the executed artifact. It refuses a second run before reaching any API it calls, so it is never run against the new layout.

## J. Next frontier

**FR-2 is complete within its authorization.** The frontier it leaves is G5: P13 observation of Agency **execution**. It would mean either:
- (a) P12-W2's execution projections reading the live population beside the certified one, labelled, and P13 mapping them; or
- (b) P13's trace source reading live stores.

Both change a certified P12-W2 declared contract or the P13 source model. That is a Founder decision under `FD-FR2-001 §10` / `§13`; it was not taken here.
