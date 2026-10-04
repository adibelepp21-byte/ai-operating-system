# FR-2 — Governed Execution → Runtime / Trace Integration: Discovery Record

| Field | Value |
|---|---|
| **Authority** | `docs/governance/acts/DIR-AIOS-AGENCY-FR2-RUNTIME-TRACE-DISCOVERY.md` (verbatim; content sha256 `ddacbde606f47007f0dbc7d0385b2306715e5095fcbd36a4bb7fdfbed8e64853`). Register `§161` (receipt), `§162` (this result) |
| **Mode** | READ-ONLY. Nothing was constructed, wired, registered, delegated or executed in production. Every probe ran in a temporary directory, and every write it made went through the resident writers into that directory |
| **Result** | **FR-2 — FOUNDER DECISION REQUIRED** (`§U`). FQ-FR2-1 is in `§U.3`.<br>• Runtime, Execution Layer, Trace, `TracedAction`, `ExecutionManifest` and the execution chain reader all exist. Together they can bind Agent Instance + Delegation + Execution + Result: the counterfactual gives **7 / 7 JOINED** on a real Agency grant.<br>• Agency execution does not enter them.<br>• Every reader that can verify the join reads only **certified** roots. Integrating would extend certified readers and populations, which is an R8 boundary the CEO may not classify alone (FDR-G1 `§9`) |
| **Evidence** | • Baseline: `evidence/fr2_baseline.py` → `evidence/FR2-BASELINE-2026-10-04.json`, captured at `eae77bc` before discovery.<br>• Discovery: `evidence/fr2_runtime_trace_discovery.py` → `evidence/FR2-RUNTIME-TRACE-DISCOVERY-2026-10-04.json`, **all_ok**.<br>• Both scripts load P12-W2 with `importlib.import_module`, the disclosed verifier pattern, so neither enters the P12 consumer measurement (`§T`) |

**The success question** (directive, *FR-2 Success Condition*), answered:

> *When an AIOS Agency Agent performs delegated work, exactly what execution path does that work take?*
> `W4Executor.execute_plan(plan, perform)` calls a caller-supplied `perform` as a plain Python call, then `persist_evidence` writes the evidence beside the grant.

> *Does it enter the canonical Runtime boundary?*
> **No.** No Runtime, Execution Layer or `ExecutionContext` is involved.

> *What Trace records it?*
> **None.**

> *How is that Trace bound to Agent Instance + Delegation + Execution + Result?*
> It is not, because no Trace exists. Instance, Delegation and Result are bound by the **evidence file**: `delegation_id`, `agent_instance` and `outcomes`.

> *Can the complete chain be reconstructed after the process is gone?*
> **Partially.** Goal → plan → grant → instance → evidence → CEO decision reconstructs from persisted files. Runtime and Trace links cannot, because they were never produced.

---

## A. Discovery Baseline

`evidence/FR2-BASELINE-2026-10-04.json` was captured before any discovery code ran.

| Item (`§23`) | Captured |
|---|---|
| 1. Commit | `eae77bc20669c71368156145bc41455baf10a8a5` (FR-1 complete) |
| 2. Certified hashes | 32 surface digests. They cover:<br>• certified roots `docs/architecture/{p11,p12,p13,platform-organization}` and `docs/operations`;<br>• the Agency operational roots and the agent registry;<br>• all code trees (`tools`, `native_core`, `consumers`, `api`, `fullstack`, root `*.py`);<br>• governance (except the Register and the newly received acts);<br>• runtime / trace code (`native_core/core/{runtime,trace,agent,workflow,memory}` and the tool / consumer list);<br>• the stores `p12/trace-stores`, `p12/execution-provenance`, `operations/runtime-observations` and `operations/p13/trace` |
| 3. Runtime / Execution / Trace test baseline | The resident suites are unchanged since FR-1's full regression (`§160`): 91 suites, 2332 tests. Re-run after this record (`§T`) |
| 4. P12 / P13 state | P12 verifier populations and verdicts; P13 facts including `operational_state.*` |
| 5. Agency provenance | The live ledger overview digest; grants `3cc612275a914c2c`, `d497e284f2c14aee` and `0a697039a63f4c17` |
| 6. Consumer measurement | 4 consumers / 5 importers; independent verifier 4 / 4 AGREE |
| 7. Known pre-existing failures | `test_e11_measurement_currency` (4); `test_p12_governance_evidence_verification` (1) |

## B. Existing Execution Architecture

There are **two** execution architectures in the repository. They have never been joined for Agency work.

| Path | Shape | Where it is used |
|---|---|---|
| **Native Runtime path** (P10 / P12) | `create_runtime(id, storage, substrate)` → `substrate.provision()` → `runtime.start()` → `create_execution_layer(runtime)` → `Execution` with `ExecutionContext(runtime_id, execution_sequence)` → `ExecutionConsumer.participate(execution)` → `TracedAction` writes **one** `TraceRecord` (INV-4) | • `aios_corpus_health_run.py`<br>• `cross_department_coordination_proof.py`<br>• `w1_coordination_proof.py`<br>• `fullstack/backend/aios.py`<br>• the P12-W4 integrated-execution proof (`p12_w4_integrated_execution.py`), which adds `ExecutionManifest` |
| **Agency W4 path** (FD-P11-001 / S-1 … S-5) | • `W4Executor(delegation, registry)` re-checks the grant and instance per step (`tools/w4_execution.py:103`).<br>• `execute_plan(plan, perform)` calls `perform(step)` directly.<br>• `ExecutionOutcome(step, status, detail, delegation_id, instance_key, at)`.<br>• `persist_evidence(root, …)` writes the evidence beside the grant (`tools/w4_execution.py:196`) | • `mr_s5_1_decisions_run.py`<br>• `s4_plan_outcome_run.py`<br>• `w1_*_run.py`<br>• `w4_first_run.py`<br>• `p12_w3_governance_escalation.py` |

**Proven by probe** (`probe.path_b_direct_call`): the Agency path produced 14 results, **0** Trace records, and no Runtime was involved.

## C. Runtime Inventory

| Element | Exists | Evidence |
|---|---|---|
| Runtime lifecycle CREATED → INITIALIZED → RUNNING → STOPPING → STOPPED | **PROVEN** | Path A: `RuntimeState.RUNNING` during the run, `STOPPED` after |
| Substrate gate | **PROVEN** | `start()` refuses until `substrate.provision()` (*"execution substrate is not available"*) |
| Execution Layer, RUNNING-only | **PROVEN** | After stop, `create_execution_layer` is *refused: RuntimeNotRunning* |
| Execution identity | **PARTIAL** | `ExecutionContext` = `{runtime_id, execution_sequence}` only. `execution_id_ratified` false: no ratified execution ID |
| Execution result model | **ABSENT by design** | `participate()` returns `None`. *"No execution-result model is ratified"* (`native_core/core/runtime/execution/consumer.py:64`) |
| Runtime persistence | **PARTIAL** | `p12_runtime_observation.publish(runtime_id, state)` persists observations:<br>• live root `docs/operations/runtime-observations` (GOAL-V2-002; currently empty);<br>• certified root `docs/architecture/p12/runtime-observations`, read as history.<br>Runtime state is otherwise process-local |
| Runtime ownership | **PROVEN** | PD-05: Runtime is *"owned centrally"*; Trace is *"owned by no one"* (`PD-05-runtime-and-execution.md:128`). There is no ambiguity to escalate: both are platform primitives, not division-owned |

## D. Execution Contract Inventory

| Contract | Elements | Agency participation |
|---|---|---|
| Native `ExecutionContext` / `ExecutionConsumer` | `runtime_id`, `execution_sequence`; `participate(execution) -> None` | **None** |
| `TraceRecord` (10 fields) | `agent_definition_version`, `agent_instance`, `runtime`, `skills_used`, `tools_used`, `knowledge_consumed`, `memory_consumed`, `outputs`, `cost_resource_metadata`, `status` ∈ {success, failure, escalation}. **No delegation field** | **None** |
| `ExecutionManifest` (`tools/p12_execution_provenance.py:67`) | 23 fields over 12 contract elements: intent, decision, work, actor, authority, scope, execution, observation, verification, evidence, provenance, lifecycle. Includes `delegation_id`, `agent_instance`, `trace_store` + `trace_ordinal`, `runtime_id`, `outcome`. `record()` is guarded and never overwrites | **None.** Only the P12-W4 proof and the negative-control verifier construct one. The probe built one for an Agency grant: `manifest_contract_complete` **true** |
| Agency W4 contract | `W4Delegation` + `ExecutionOutcome` + the evidence file (keys: `agent_instance`, `authority_chain`, `criteria`, `delegation_id`, `escalations`, `executed_at`, `outcomes`, `performed_by`, `plan`, `subject`) | **Full.** This is the contract Agency uses |

**Classification:** the Execution Contract is not **used** by Agency. It is not **insufficient**: `ExecutionManifest` already carries every binding FR-2 asks for (G4 and G6 are narrow contract gaps, `§Q`). No Execution Contract semantic change is needed.

## E. Agent Instance Binding

| Surface | Identity recorded | Classification |
|---|---|---|
| Grant `recipient_instance` | `engineering-intelligence-instance-001` | **DIRECT**; instance record PERSISTED in the agent registry |
| `W4Executor` | re-checks `registry.get(recipient).lifecycle == REGISTERED` every step | **DIRECT** |
| Evidence `agent_instance` / `performed_by` | the instance key | **DIRECT** |
| `EngineeringIntelligenceAgent.participate` → Trace | **`engineering-intelligence-agent`**, the **definition** key, not the instance (probe `trace_agent_instance`) | **CONTRACT GAP (G4).** RC-2 at the consumer level. It is avoidable without changing the consumer: `TracedAction(writer, agent_instance=<instance key>, runtime=…)` records the instance (Path A′) |
| `TracedAction` with a fabricated key | accepted: `fabricated-instance-999` was recorded | The trace layer does **not** validate instances (G8). Enforcement happens at the join: the chain reader makes DELEGATION→EXECUTION **DANGLING** (N10) |

## F. Delegation → Execution Mapping

| Grant | Execution | Classification |
|---|---|---|
| `3cc612275a914c2c` (MR-S5-1 P1) | `executed_at` 2026-10-03T12:49:49Z; evidence names the `delegation_id` | **DIRECT** |
| `d497e284f2c14aee` (MR-S5-1 P2) | `executed_at` 2026-10-03T12:49:50Z | **DIRECT** |
| `0a697039a63f4c17` (S-2) | never executed | **MISSING** (correctly: the grant is live and unexecuted) |

There is no **execution ID**. An execution is identified only by (`delegation_id`, `executed_at`). This is sufficient for the W4 path, but it does not join to any Runtime `execution_sequence` (`§G`).

## G. Execution → Runtime Mapping

**Agency → Runtime: MISSING for every grant.** No record (evidence, ledger, observation, manifest, Trace) carries a `runtime_id` or an `execution_sequence` for any Agency execution.

| Representative chain field | Value |
|---|---|
| `runtime` | `null`: *"MISSING (no runtime id, execution sequence or observation in any record)"* |

**Probe, Path A** (temp only): the same Engineering Intelligence work hosted in a real Runtime.
- Context: `{runtime_id: "fr2-probe-runtime", execution_sequence: 0}`.
- Runtime state RUNNING; `participate` returned `None`.

So the Runtime **can** host the work. It is not wired to (G1, R3).

## H. Runtime → Trace Mapping

| Path | Trace |
|---|---|
| Agency W4 (B) | **0 records** |
| Runtime-hosted participate (A) | **1 record**, INV-4 holds:<br>• `runtime` = `fr2-probe-runtime`;<br>• `agent_instance` = the definition key (G4);<br>• `status` success;<br>• `outputs` null |
| Runtime-hosted `TracedAction` with the instance key (A′) | **1 record per action**, actor = `engineering-intelligence-instance-001` |

**Not in the Trace:**
- `execution_sequence` (`fresh_process.execution_sequence_in_trace` false);
- `delegation_id` (`TraceRecord` has no such field).

The Trace binds **instance + runtime**. Delegation joins only through `ExecutionManifest` (`trace_store` + `trace_ordinal` + `delegation_id`).

## I. Trace → Result Mapping

| Finding | Evidence |
|---|---|
| The Trace does not carry the result | `outputs` null; 14 verification results held **in memory only** (`verification_results_held_in_memory_only` 14) |
| Trace status reflects **participation**, not outcome | With verification **unsatisfied**, the Trace status was still `success` (`path_a_unsatisfied_verification_trace_status`). This is G6 (R4) |
| Result is bound elsewhere | • W4 path: `ExecutionOutcome` → evidence `outcomes`.<br>• Manifest path: `outcome` + `status` fields |

Result ≠ Trace (N6).

## J. Result → Verification Mapping

| Grant | Result | Verification | CEO decision |
|---|---|---|---|
| `3cc612275a914c2c` | success, 14 / 14 elements carried | **DERIVED** (`plan_completion` over the evidence) | **ACCEPT** (DIRECT, live ledger) |
| `d497e284f2c14aee` | failure (*"3 of 14 elements carried"*) | **DERIVED** | **REWORK** (DIRECT) |
| `0a697039a63f4c17` | — | MISSING | none yet |

`result_producer` is: caller-supplied `perform` → `W4Executor` `ExecutionOutcome` → `persist_evidence`. Verification and decision are the S-4 / S-5 mechanisms, already integrated.

## K. Full Provenance Chain

For the executed grant `3cc612275a914c2c`:

| Link | Status |
|---|---|
| Founder goal | **PERSISTED** (`planning.state.json`; the goal cites its act) |
| Plan | **TEXTUAL** (parsed from the grant's `lifecycle_boundary` by `_bound_plan`) |
| Plan step | **DIRECT** (grant `work_scope`) |
| Agent Instance | **DIRECT** |
| Delegation | **DIRECT** |
| Execution | **DIRECT** (no execution ID) |
| **Runtime** | **MISSING** |
| **Trace** | **MISSING** |
| Result | **DIRECT** |
| Verification | **DERIVED** |
| CEO decision | **DIRECT** |

**The existing seven-edge chain reader** (`tools/p12_execution_chain_reader.verify_manifest`), applied to a real manifest for the Agency grant written by the real `record()` into a temp root:

| Run | INTENT→DECISION | DECISION→WORK | WORK→DELEGATION | DELEGATION→EXECUTION | EXECUTION→OBSERVATION | OBSERVATION→VERIFICATION | VERIFICATION→EVIDENCE |
|---|---|---|---|---|---|---|---|
| Resident `DELEGATION_DIRS` | JOINED | JOINED | **DANGLING** | **DANGLING** | JOINED | JOINED | JOINED |
| Counterfactual: Agency root added | JOINED | JOINED | JOINED | JOINED | JOINED | JOINED | JOINED |
| Fabricated actor | JOINED | JOINED | JOINED | **DANGLING** | JOINED | JOINED | JOINED |

**Why it dangles:** `DELEGATION_DIRS` (`tools/p12_execution_chain_reader.py:41`) lists only:
- `p11/w1-operations`
- `p11/w4-operations`
- `p11/x-department-operations`
- `p12/w4-operations`

It does not list the Agency operational roots where every S-1 … MR-S5-1 grant lives.

**Conclusion:** the full chain is **achievable with existing mechanisms**, but is **not produced** today.

On the repository, the reader still JOINs its own 5 manifests (`p12-w4-integrated-execution-001..005`), all certified.

## L. Failure / Recovery Findings

| Case | Finding |
|---|---|
| Agency step failure | **Captured**: `perform` raising becomes a `FAILURE` outcome (`tools/w4_execution.py`); P2 shows a persisted failure and a REWORK decision |
| Out-of-scope step | Recorded as `ESCALATION` and the run continues (`§27`) |
| Runtime not running | `create_execution_layer` refused (RuntimeNotRunning). **PROVEN** |
| Trace on failure | The P12-W4 failure store exists (`p12-w4-integrated-execution-failure`, 1 record), so failure traces are supported. Agency failures produce **no** Trace |
| Trace escalation status | Declared in `TraceRecord`, but `TracedAction` never produces it (`consumers/observation.py`). This is G7 |
| Interrupted runtime | A runtime that dies without publishing a terminal state reads **STALE** after 30 s (`LIVE_HORIZON_SECONDS`), never LIVE. This is the existing protection |

## M. Fresh-Process Reconstruction

| Item | After the original process exits |
|---|---|
| Trace records | **Survive.** Re-read by `TraceReader` in a fresh process |
| Runtime state | **PROCESS-LOCAL.** Nothing persists unless `publish()` is called |
| `execution_sequence` | **Lost.** Not in the Trace, the evidence or the observation |
| Agency evidence, ledger, decisions | **Survive** (S-4 / S-5 / FR-1 evidence) |
| Agency Runtime / Trace links | **Not reconstructable.** They were never produced |

N11 holds: process-local runtime state is not accepted as persistent provenance anywhere.

## N. P13 / Observability Reconciliation

| Item | Finding |
|---|---|
| P13 memory Trace stores seen | • `aios-corpus-health` 7<br>• `p12-live-verification` 1<br>• `p12-w1-integration-edge` 1<br>• `p12-w2-state-transition` 1<br>• `p12-w4-integrated-execution` 3<br>• `p12-w4-integrated-execution-failure` 1<br>• `p13` 11<br>• `w4-conformance-verification` 2 |
| P13 Trace root | `docs/architecture/p12/trace-stores`, which is **certified** |
| Agency grants in any Trace, manifest or observation | **none** |
| Live observations | **none** (`docs/operations/runtime-observations` empty) |
| Agency state visible to P13 | yes, via FR-1: `operational_state.delegations` / `.escalations` through P12-W2 |

**P13 sees Agency *state* (delegation disposition). It sees no Agency *execution*.**

P13 claims no Runtime observation of Agency, so N9 holds. Once Agency traces exist, P13 would see them only if its trace source also reads a live root (G5, R6). That edge rides the existing P13 trace-store source and does not depend on FR-1.

## O. Canonical / Certified / Operational / Derived Classification

| Surface | Canonical | Certified | Operational | Derived | Historical |
|---|---|---|---|---|---|
| `native_core` Runtime / Execution Layer | ✔ (frozen) | ✔ (P10) | — | — | — |
| `TraceRecord` / `TraceWriter` / `TraceReader` | ✔ | ✔ | — | — | — |
| `p12/trace-stores` | — | ✔ | — | — | ✔ |
| `p12/execution-provenance` (manifests) | — | ✔ | — | — | ✔ |
| `p12/runtime-observations` | — | ✔ | — | — | ✔ |
| `operations/runtime-observations` | — | — | ✔ (live; empty) | — | — |
| Agency operational roots (grants, evidence) | ✔ for delegation | — | ✔ | — | — |
| Live ledger (`operational_overview`) | ✔ for current disposition (A2) | — | ✔ | — | — |
| P12-W2 projection | — | ✔ (contract) | — | ✔ | — |
| P13 facts | — | ✔ (Blueprint) | — | ✔ | — |
| Chain reader verdict | — | ✔ | — | ✔ | — |

**Authoritative source for each question:**

| Question | Authoritative source |
|---|---|
| Execution identity | none ratified. Agency uses (`delegation_id`, `executed_at`); Runtime uses (`runtime_id`, `execution_sequence`). They do not join |
| Runtime lifecycle | the Runtime object (process-local) plus observations (`publish`) |
| Trace | `TraceWriter` / `TraceReader` stores |
| Result | Agency evidence `outcomes`; the manifest `outcome` on the P12 path |
| Failure | the same as Result |
| Delegation | the Agency grant record (FD-P11-001 delegator); current disposition from the live ledger (A2) |
| State | the live ledger → P12-W2 (FR-1) |
| Observability | P13 over P12-W2 and Trace stores |

**N7 holds:** P12-W2 declares `execution.recorded` as class EXECUTION with freshness *"historical"*. The delegation owner is unchanged. Trace does not become state authority.

## P. Existing-Mechanism Search Exhaustion

Searched with AST / text callers across `tools`, `native_core`, `consumers`, `api`, `fullstack`, root entry points and evidence scripts (`inventory.callers`):

| Mechanism | Found | Agency use |
|---|---|---|
| `create_execution_layer(` | 6 sites: corpus-health, coordination proofs, fullstack backend, composition, capability discovery | none |
| `TracedAction(` | 10 sites: 7 consumer agents, corpus-health, trace-durability proof, P12-W4 | none |
| `ExecutionManifest(` | 2 sites: P12-W4 proof, negative-control verifier | none |
| `persist_evidence(` | 3 sites: `w4_execution`, S-4 run, MR-S5-1 run | **all Agency** |
| `W4Executor(` | 9 sites | **all Agency** |
| Trace registry / chain reader / observation publisher | 1 each | read certified roots only. The observation reader also merges the live root |
| Closest existing precedent | `aios_corpus_health_run.py`: Runtime-hosted with `TracedAction` and `AGENT_INSTANCE="engineering-intelligence-instance-001"`, but **no delegation and no manifest**.<br>`p12_w4_integrated_execution.py`: Runtime + `TracedAction` + manifest + chain reader, all JOINED, but over **P12** delegations, not Agency ones | — |

**Exhausted.** No existing caller combines `W4Executor` with a Runtime-hosted execution. Every component the combination needs exists.

## Q. Gap Register

| # | Gap | Class | Evidence | Resolvable by existing mechanism? |
|---|---|---|---|---|
| G1 | The Agency W4 path bypasses Runtime and Trace (`perform` is a direct call) | **R3** Integration | Path B: 0 traces, no runtime | Yes: Runtime + `TracedAction` + `ExecutionManifest`, as P12-W4 already does |
| G2 | Every verifying reader reads only certified roots:<br>• trace registry `STORE_ROOT`;<br>• `MANIFEST_ROOT`;<br>• chain reader `MANIFESTS` / `TRACE_STORES` / `OBSERVATIONS`;<br>• P13 `trace_stores`.<br>`DELEGATION_DIRS` excludes the Agency roots. There is no live trace or manifest root | **R8** Certified boundary | `roots_certified`; the counterfactual 7 / 7 vs the resident DANGLING | Yes, technically: the GOAL-V2-002 live / certified split pattern (`tools/p12_runtime_observation.py:60-87`). But it extends certified readers and populations, so it is **Founder-reserved** (FDR-G1 `§9`) |
| G3 | Runtime state and `execution_sequence` are process-local; the live observation root is empty | **R5** Persistence | fresh-process probe | Yes: `publish()` to the live root (already live, not certified) and the manifest `runtime_id` |
| G4 | `participate` traces the definition key, not the instance (RC-2) | **R4** Contract | probe `trace_agent_instance` | Yes, without consumer change: `TracedAction(agent_instance=<recipient>)`, the P12-W4 / corpus-health shape |
| G5 | P13 sees only certified Trace stores | **R6** Observability | `§N` | Rides G2's reader extension |
| G6 | Trace status reflects participation, not verification outcome | **R4** Contract | unsatisfied verification gives `success` | Yes: the outcome is carried by the manifest `outcome` / `status` and by the evidence. Recorded as a limit; no Trace semantic change proposed |
| G7 | The Trace `escalation` status has no producer | **R4** Contract (minor) | `consumers/observation.py` | W4 escalations stay in evidence and ledger. Not required for FR-2 |
| G8 | The trace layer accepts a fabricated actor | **R4** Contract (minor) | Path A′ | Enforced at the join (N10); `W4Executor` also refuses an unregistered recipient before any work |

**No R9.** No TRUE SYSTEM GAP survives the search. No R7: authority for Agency execution exists (FD-P11-001 / FD-AGENCY-001). What is missing is a Founder ruling on the certified boundary (R8).

**Material unknowns** (explicit):
- U1: whether P13's Blueprint `§4` trace-store interface is read as "certified stores" or as "the Trace stores". This is the same interpretive question as FR-1, so it rides FQ-FR2-1.
- U2: the cost / latency of Runtime-hosting each W4 step. Not measured; no production run is allowed in this gate.

## R. Frontier Classification

| Compared against (`§21`) | Relation to FR-2 |
|---|---|
| S-1 delegation lifecycle; S-2 plan → delegation; S-3 goal → CEO → agent | Upstream links, integrated. FR-2 starts where they end |
| S-4 evidence → CEO decision → plan outcome | Result / verification / decision links, integrated (`§J`) |
| S-5 decision provenance | Integrated; the CEO decision is DIRECT |
| S-6 systemic discovery | Named Runtime / Trace as an open frontier; FR-2 confirms it and narrows it |
| TD state-authority discovery | Fixed the state authority (A2 live ledger). FR-2 keeps Trace non-authoritative (N7) |
| FR-1 | Delivers Agency *state* to P13. FR-2 is Agency *execution*. They are independent; only P13 visibility of traces is adjacent (G5) |
| PD-05 | Runtime is owned centrally and Trace by no one. No ownership ambiguity |
| P13 | Observes certified traces only (G5) |

| `§21` question | Answer |
|---|---|
| 1. genuinely new | **No.** Every mechanism exists |
| 2. already solved elsewhere | **Yes, for P12 delegations** (P12-W4: 5 manifests, all JOINED) |
| 3. partially solved | **Yes.** Agency's chain is DIRECT up to execution and from result onward, MISSING across Runtime / Trace |
| 4. duplicated by another mechanism | **Partly.** The W4 evidence file duplicates the manifest's instance / delegation / result binding without the Runtime / Trace links |
| 5. blocked by a certified boundary | **Yes.** G2 (R8) |
| 6. executable but unused by Agency | **Yes.** G1 (R3) |

**Classification:** FR-2 is a **correctly identified** frontier (not misclassified). It is an integration frontier whose smallest resolution crosses a certified reader boundary.

**Smallest integration frontier** (what a future construction gate would do; nothing here is built):
1. The Agency W4 `perform` runs inside a Runtime-hosted Execution. A `TracedAction` is written under the grant's `recipient_instance` and the runtime id, and the runtime publishes its observation to the **live** root.
2. Each executed step records one `ExecutionManifest` with `delegation_id`, `trace_store` + `trace_ordinal`, `runtime_id` and `outcome`, written to a **live** manifest root.
3. The existing readers read live **and** certified roots, with origin labelled, the way `p12_runtime_observation` already does since GOAL-V2-002:
   - trace registry and P13 trace source: live + certified trace stores;
   - chain reader: `MANIFESTS` / `TRACE_STORES` / `OBSERVATIONS` live + certified, and `DELEGATION_DIRS` += the Agency operational roots.
4. No change to `native_core`, `TraceRecord`, `ExecutionContext`, `ExecutionManifest` fields, chain-edge rules or P12-W2 ownership.

Item 1 alone (writing without step 3) would produce traces that **no** verifier can join. That is Option C, and it is why the frontier is not CEO-classifiable maintenance on its own.

## S. Negative-Control Results

All 12 were **tested and PASS** (`negative_controls`):

| # | Control | How it was established |
|---|---|---|
| N1 | No Runtime claim without Runtime evidence | Path B: no runtime, and no record claims one; every Agency chain reads `runtime` MISSING |
| N2 | A direct call is not labelled Runtime execution | Path B is classified "direct", 0 traces |
| N3 | A capability or definition name is not an instance | The definition key in the `participate` trace is not accepted as the grant recipient |
| N4 | Delegation is not inferred from agent identity | The Trace has no delegation field. Delegation joins only via the manifest; the resident reader DANGLES without the Agency root |
| N5 | Execution is not inferred from result | S-2 has no evidence, so execution is MISSING; no execution is inferred from a result |
| N6 | Result is not Trace | Trace `outputs` null; the result lives in evidence / manifest |
| N7 | Trace is not authoritative state | P12-W2 `execution.recorded` is EXECUTION / historical; delegation owner unchanged |
| N8 | Historical is not presented as current | Certified `STORE_ROOT` is history; the live observation root is empty, so nothing is LIVE |
| N9 | P13 claims no Runtime observation of Agency | No Agency grant in any P13-visible Trace, manifest or observation |
| N10 | A fabricated instance is not a valid Runtime actor | The chain reader makes DELEGATION→EXECUTION DANGLING for `fabricated-instance-999` |
| N11 | Process-local state is not persistent provenance | Runtime state does not survive a fresh process; nothing treats it as provenance |
| N12 | No certified boundary changed silently | Certified surfaces are byte-identical; this record **escalates** G2 instead of classifying it as maintenance |

## T. Integrity Verification

| Check | Result |
|---|---|
| 32 surfaces vs baseline | Re-run after this record was written: 31 equal. The only difference is `agency_records:docs/architecture/agency/*.md`, which is this record and the one change the tool declares as expected. `surfaces_changed_vs_baseline` `[]` |
| The run changed nothing | `run_changed_nothing` **true** |
| Certified git status (`p11`, `p12`, `p13`, `platform-organization`, `docs/operations`) | **(clean)** |
| `certified_evidence_integrity.verify()` | **0 faults** |
| Register | only appended (`§161`, `§162`) |
| Evidence tool is not a consumer | P12-W2 loaded by `importlib.import_module`. Consumer measurement still reads 4 / 5 (`test_p12_consumer_measurement`, `test_p12_state_verification` re-run after this record) |
| Temp writes | `ExecutionManifest` / `record()`, `publish()` and `TraceWriter` all wrote to `tempfile` roots only. Chain-reader roots were mock-patched to temp. No repository root received a write |

## U. Final Disposition

### U.1 Disposition

> **FR-2 — FOUNDER DECISION REQUIRED**

| `§26` candidate | Why it does not apply |
|---|---|
| EXISTING / INTEGRATED | Agency execution is not Runtime-hosted and not traced (G1) |
| EXISTING / DISCONNECTED or PARTIAL / INTEGRATION FRONTIER | The mechanisms exist and the smallest frontier is defined (`§R`). But the frontier requires extending certified readers and populations (G2). FDR-G1 `§9`: certified interfaces and dependencies are presumed material, and *"if uncertain … MUST be escalated"*. A `§28` stop: *"certified architecture boundary"*, *"requirement to alter certified verifier semantics"* (populations) |
| TRUE GAP | No R9; the existing-mechanism search is exhausted with every component found |
| FRONTIER MISCLASSIFIED | Runtime / Trace is the correct next frontier (`§R`) |

### U.2 Exhaustion (`§27`)

| Condition | Met in |
|---|---|
| 1. Path traced | `§B` |
| 2. Runtime participation disproven with evidence | `§G` |
| 3. Contract classified | `§D` |
| 4. Instance traced | `§E` |
| 5. Delegation → Execution | `§F` |
| 6. Execution → Result | `§I` / `§J` |
| 7. Trace classified | `§H` |
| 8. Lifecycle | `§C` |
| 9. Fresh process | `§M` |
| 10. P13 | `§N` |
| 11. Ownership | `§O` |
| 12. Search | `§P` |
| 13. Gap classes | `§Q` |
| 14. Unknowns explicit | `§Q` U1, U2 |
| 15. Controls | `§S` |
| 16. No unexplained frontier | `§R` |

### U.3 FQ-FR2-1 — escalation (`§28`)

**QUESTION**

May the existing certified readers be extended to read live Agency execution, so that Agency W4 execution can be Runtime-hosted and Trace-bound through existing mechanisms? This covers:
- live trace and manifest roots;
- the chain reader's `DELEGATION_DIRS` including the Agency operational roots;
- the P13 trace source reading live trace stores.

**EVIDENCE**
- `§K` counterfactual: 7 / 7 JOINED.
- `§Q` G1–G5: resident DANGLING; roots all certified (`roots_certified`); P13 sees certified stores only.

**EXISTING AUTHORITY**
- FD-P11-001 and FD-AGENCY-001 authorize Agency execution itself.
- GOAL-V2-002 C-2 / C-7 set the live / certified split precedent, already applied in code to runtime observations.
- FDR-G1 `§8–9` and FDR-G2 `§8–10` govern maintenance vs certified change.
- P12 D7: P12-W2 owns no domain state.
- FD-FR1-001 is the precedent for registering a new observed consumer.

**OPTIONS**

| Option | What it means | Consequence |
|---|---|---|
| **A** *(recommended)* | Authorize, as FDR-G1 maintenance on the GOAL-V2-002 precedent:<br>• live trace and manifest roots under `docs/operations`;<br>• the certified readers named above read live + certified, origin-labelled, with certified populations keeping their meaning;<br>• `DELEGATION_DIRS` += the Agency operational roots;<br>• Agency W4 `perform` runs in a Runtime-hosted Execution with `TracedAction` under the recipient instance, publishing an observation and recording an `ExecutionManifest`.<br>No `native_core`, `TraceRecord`, `ExecutionContext`, manifest-field or chain-rule change. Certified bytes untouched | • Closes G1–G5 with existing mechanisms.<br>• Independently verifiable (chain reader) and observable (P13).<br>• Pinned P12 tests that count stores, manifests or delegation dirs would move as **data**, not semantics. Same handling as FR-1: disclosed, never hidden |
| B | Treat it as a certified successor change (new P12 / P13 certification cycle) | Strongest assurance, but slowest. It re-opens certified phases for an integration that uses only existing mechanisms |
| C | Agency writes traces and manifests to live roots **without** reader extension | No certified reader touched, but nothing can verify or observe the chain. The trace exists but is unjoinable. Not recommended |
| D | Defer | Agency execution remains untraced. S-1 … FR-1 are unaffected |

**RECOMMENDATION**

**Option A.** It is the smallest frontier (`§R`). It reuses only resident mechanisms, follows a precedent already in the code (`tools/p12_runtime_observation.py:60-87`), and keeps certified evidence byte-identical.

**CONSEQUENCE**

On A, an FR-2 construction gate would:
- add no new subsystem;
- add a verification baseline like FR-1's;
- add tests that fail if Agency execution bypasses the Runtime, traces a definition key, or dangles at the join.

**FOUNDER DECISION REQUIRED:** FQ-FR2-1 (A / B / C / D).

No construction was performed in this gate, and none begins without the decision.
