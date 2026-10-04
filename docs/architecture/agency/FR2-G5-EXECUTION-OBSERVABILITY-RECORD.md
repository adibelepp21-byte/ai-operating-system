# FR-2 G5 — Agency Execution Observability Through P12-W2 (FD-FR2-002): Record

| Field | Value |
|---|---|
| **Authority** | `docs/governance/acts/FD-FR2-002-AGENCY-EXECUTION-OBSERVABILITY-THROUGH-P12-W2.md` (verbatim; content sha256 `6bcb5752130b1382086cdca59fe0c5f73bbc34156e728892551d405ae9bb2900`): FQ-FR2-G5 = **Option A**. Register `§165` (decision), `§166` (this result). Predecessor: FR-2 (`FR2-RUNTIME-TRACE-INTEGRATION-RECORD.md`, `§164`) |
| **Result** | **G5 CONSTRUCTED / VERIFIED.** P13 now observes Agency execution, and only through P12-W2:<br>Agency Runtime / Trace / Manifest → P12-W2 `execution.provenance` (live population) → P13 `operational_state.executions`<br>P13 reads no Agency Trace, Runtime or manifest store. Every `§8` item (1–14) and every `§9` negative control (N1–N10) holds in a fresh process. No `§10` stop condition was reached |
| **Evidence** | • Baseline: `evidence/g5_baseline.py` → `evidence/G5-BASELINE-2026-10-04.json`, captured at `f1014b9` before any code changed.<br>• Verification: `evidence/g5_verification.py` → `evidence/G5-VERIFICATION-2026-10-04.json`, **all_ok**, fresh process.<br>• Tests: `tools/tests/test_g5_execution_observability.py` (20; 8 code mutations, all caught) |
| **Code changed** | • `tools/p12_operational_state.py`: the two execution projections.<br>• `tools/p13/state.py`: one mapping entry in the existing `operational_state` source.<br>Nothing else. The P12-W2 contract (8 sources, declared fields, provider `UNRESOLVED (F-17)`), Runtime, Trace, `ExecutionManifest`, the Execution Contract, the chain reader and P13's other sources are unchanged |

---

## A. What was built

**P12-W2 `execution.provenance`** keeps its certified value exactly (`manifests` 5, `statuses` `[failure, success]`). It labels that value `origin: certified-p12` and adds `live`, origin `live`, read paths named.

For each live Agency execution, the `live` section carries:

| `§4` item | Field | Read through (owner's own reader) |
|---|---|---|
| Execution identity | `execution_id`, `manifest` | `p12_execution_provenance.manifests(LIVE_MANIFEST_ROOT)` |
| Agent Instance | `agent_instance` | the manifest |
| Delegation | `delegation_id` | the manifest |
| Runtime participation | `runtime.runtime_id`, `observed`, `state`, `classification` | `p12_runtime_observation.observations` (origin `live`) |
| Trace / Manifest existence | `trace.store`, `ordinal`, `joined`; `manifest` | the manifest; the chain reader's `DELEGATION→EXECUTION` edge |
| Result availability, outcome | `result.available`, `result.status` | the manifest |
| Provenance | `provenance` (JOINED / DANGLING), `edges` (7), `valid_agency_execution` | `p12_execution_chain_reader.verify_live` (the independent reader) |
| Active / completed | `temporal` (CURRENT / HISTORICAL), `completed`; lists `active`, `completed` | Runtime classification: LIVE ⇒ CURRENT. COMPLETED requires TERMINATED **and** a joined chain |
| Historical vs current | `temporal` | the same |

A live Runtime that no manifest names is reported apart, as `unbound_live_runtimes`. It is never an Agency execution (N6).

**P12-W2 `execution.recorded`** keeps its certified value exactly (16 records, 7 stores, 7 failures) and adds `live`: the live Trace stores read through the same registry. The two populations are never summed.

**P13** gains `operational_state.executions`, mapped from `execution.provenance` by the existing `operational_state` source (`FD-FR1-001`). It is VERIFIED when P12-W2 reads CURRENT, and its source names *"P12-W2 execution.provenance"*.

**What P12-W2 does not do.** It does not own Runtime or Trace, and it does not decide whether an execution's provenance holds: the independent chain reader decides that. It does not repeat the delegation's current disposition either; that belongs to `delegation.granted` (`FD-TD-001`), and a second reading would be a second authority.

## B. On the repository

| Reading | Value |
|---|---|
| P12-W2 `execution.provenance` | certified: 5 manifests, statuses `[failure, success]`, unchanged |
| P12-W2 `execution.provenance.live` | 1 execution: `agency-2adef08b8efa4549-verify-runtime-path-mechanisms`<br>• instance `engineering-intelligence-instance-001`, grant `2adef08b8efa4549`;<br>• Runtime `agency-runtime-2adef08b8efa4549` observed STOPPED → TERMINATED;<br>• Trace `agency-w4-execution#0` joined; result `success`;<br>• provenance **JOINED** 7 / 7;<br>• **HISTORICAL**, **completed**.<br>`active` [], `unbound_live_runtimes` [] |
| P12-W2 `execution.recorded` | certified: 16 records, 7 stores, 7 failures, unchanged. Live: 1 store `agency-w4-execution`, 1 record, 0 failures |
| P13 `operational_state.executions` | VERIFIED, *"P12-W2 execution.provenance (CURRENT)"*, carrying the same live execution; identical in a fresh process |
| P13 `operational_state.delegations` / `.escalations` | identical to the G5 baseline (N10) |

## C. `FD-FR2-002 §8` verification

`evidence/G5-VERIFICATION-2026-10-04.json`: **all_ok**.

| # | Item | Result |
|---|---|---|
| 1 | Agency Runtime execution intact | ✔ Runtime id observed |
| 2 | Agency Trace intact | ✔ Trace joined; store present |
| 3 | Agency Manifest intact | ✔ |
| 4 | P12-W2 observes it through its projection | ✔ CURRENT entry; instance, grant, result, outcome |
| 5 | P13 receives it through P12-W2 | ✔ VERIFIED, source P12-W2 `execution.provenance` |
| 6 | P13 reads no Agency Runtime / Trace store | ✔ no import of the observation, chain, provenance or hosting modules; no live path in P13 code; P13 Memory still reads the certified trace stores only |
| 7 | Live and certified distinguishable | ✔ `origin` on both populations of both projections |
| 8 | Historical not presented as current | ✔ HISTORICAL; not in `active`; in `completed` |
| 9 | Certified P12 populations intact | ✔ certified values of both projections, chain verdicts, trace population, manifests, verifier populations and verdicts all identical to baseline |
| 10 | FR-1 state observation unchanged | ✔ both P13 FR-1 facts identical to baseline |
| 11 | 7-link provenance 7 / 7 JOINED | ✔ |
| 12 | Fresh-process reconstruction | ✔ P13 in a separate process: VERIFIED, JOINED, HISTORICAL, completed |
| 13 | Independent consumer measurement recognizes P12-W2 → P13 | ✔ P13 a measured and observed consumer; 0 disagreements; measurement identical to baseline (no new consumer) |
| 14 | No second execution-state authority | ✔ 8 sources, contract identical, no conflict, no entry is authority. `operational_state` is the only P13 source carrying execution |

## D. Negative controls (`§9`)

| # | Control | Established by |
|---|---|---|
| N1 | P13 direct access to Agency Trace rejected | AST and text scan of `tools/p13`. P13 Memory reads `paths.trace_stores` = the certified store, without the Agency store |
| N2 | P13 direct access to the Agency Runtime store rejected | the same scan (no observation module, no live root) |
| N3 | P12-W2 cannot fabricate an execution | No manifest ⇒ no execution (sandbox: Runtime and Trace without a manifest lists nothing). A manifest whose Trace is missing ⇒ DANGLING, not valid, not completed |
| N4 | Historical not presented as current | TERMINATED ⇒ HISTORICAL; a STALE Runtime ⇒ HISTORICAL, not active; only a LIVE Runtime ⇒ CURRENT |
| N5 | A result without Runtime / Trace is not Runtime execution | A direct `W4Executor` run lists nothing. The pre-FR-2 Agency results (e.g. `3cc612275a914c2c`) are absent |
| N6 | A Runtime without instance provenance is not Agency execution | An unbound live Runtime is listed only under `unbound_live_runtimes`. A fabricated Trace actor ⇒ DELEGATION→EXECUTION DANGLING, not valid |
| N7 | Certified evidence not mutated | certified surfaces byte-identical; integrity faults 0; certified git status clean |
| N8 | Live evidence does not enter the certified population | certified values unchanged after a live execution; the live execution is absent from the certified manifests |
| N9 | No second current execution-state authority | as `§8` 14 |
| N10 | FR-1 operational state unchanged | as `§8` 10 |

**Mutations** (each applied in a throwaway worktree, then the G5 suite run):

| # | Mutation | Result |
|---|---|---|
| G1 | Every listed execution called valid | 2 failures |
| G2 | Every execution called current | 3 failures |
| G3 | Live counted into the certified population | 2 failures |
| G4 | Completion without a joined chain | 1 failure |
| G5 | Provenance not taken from the chain reader | 1 failure |
| G6 | A bound live Runtime also reported as unbound | 1 failure. It survived the first pass, so I added a test of a bound live Runtime |
| G7 | P13 imports the runtime observation module (direct read) | 1 failure |
| G8 | P13 drops the P12-W2 execution mapping | 1 failure, 3 errors |

## E. Boundaries (`§10`)

| Stop condition | Reached? |
|---|---|
| P12-W2 certified semantics change | No. Declared contract identical (8 sources, read paths, owners, freshness, provider). Certified values of both projections identical. The live population is added beside them and labelled |
| P12-W2 ownership change | No. It reads owners' readers; provenance is decided by the chain reader |
| P13 certified source architecture change | No. One mapping entry in the existing `operational_state` source (FD-FR1-001); no new source, no new reader |
| New projection subsystem | No. The two existing projections were extended |
| Direct P13 access to live Trace | No (N1, N2) |
| Trace schema, Execution Contract, Runtime persistence change | No |
| New authority | No |
| Certified evidence semantics change | No |

## F. Residual, still open (`§7`, `§11`)

| Gap | State |
|---|---|
| G3: Runtime state persistence | Unchanged. An in-flight execution has no provenance until its manifest is written (after its Runtime stops), so while it runs P12-W2 can show its Runtime only as an *unbound* live Runtime, never as an Agency execution. That follows from G3, and G5 does not resolve it |
| G6: Trace status semantics | Unchanged |
| G7: Trace escalation production | Unchanged |

These are not FR-2 failures (`§11`). FR-2 Runtime / Trace integration and G5 observability are valid independently of them.

## G. Tests and regression

| Suite | Result |
|---|---|
| `test_g5_execution_observability` | 20 OK |
| P12-W2, FR-1, P13 (×3), state verification, consumer measurement, self-model, E12, negative control, integration graph, FR-2 | OK |
| **Complete regression** | **96 suites, 3602 tests** (= FR-2's 3582 + 20 G5): `tools/tests` 92 / 2112; `consumers` 276 OK; `bounded_exception` 29 OK; `fullstack` 384; `native_core` 801 OK.<br>The only failures are pre-existing and unchanged since FR-2: `test_e11_measurement_currency` 2; `test_p12_governance_evidence_verification` 1; `fullstack` NC-04, NC-05, NC-19 |
