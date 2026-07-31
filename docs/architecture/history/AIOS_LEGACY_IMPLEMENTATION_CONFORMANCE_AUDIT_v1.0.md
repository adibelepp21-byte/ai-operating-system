# AIOS Legacy Implementation Conformance Audit v1.0

**Phase:** AIOS 2.96 — Legacy Implementation Conformance Audit. **Read-only** architectural conformance audit of the existing implementation against the frozen AIOS architecture.
**Auditor stance** [A]: independent architecture auditor. This document fixes nothing, refactors nothing, renames nothing, designs no replacement, proposes no architectural change, creates no ADR, and modifies no file. It classifies existing implementation against frozen authority and records evidence.
**Authoritative order (highest first)** [E]: Architecture Freeze → Implementation Constitution → Native Core Blueprint → Engineering Specifications → Architecture Specification → Relationship Model → Vocabulary Freeze → Domain Model → Constitution. Engineering documents are implementation contracts; existing code may never redefine them.
**Tagging (never mixed):** **[E]** evidence read directly from code/canon · **[A]** auditor analysis · **[O]** Architect decision required.

---

## 1. Purpose

[A] To determine, on evidence, whether the existing implementation — the untracked `execution/` tree, its tests, and the `tools/` validators — **conforms** to the frozen AIOS architecture, and to classify each module so the Architect can decide its disposition before Phase 3.
[E] This audit was triggered by a finding in the Phase 2.95 Implementation Readiness Review (§14 RISK-10; §18 condition 2): implementation already exists that predates the completed governance foundation and had not been audited for conformance.
[A] The audit answers, per module: does it conform, partially conform, violate, or is it undetermined — and what should happen to it.

## 2. Scope

[E] **In scope:** every `.py` file under `execution/` (implementation, helpers, bootstrap, runtime code, and tests) and under `tools/` (catalog validators); the on-disk Trace corpus; module docstrings and behaviour.
[E] **Out of scope, by rule:** modifying, renaming, refactoring, or fixing any file; creating implementation; proposing architecture; creating ADRs; updating any document; beginning Phase 3.
[A] The audit is **read-only**. Its only product is this report.

## 3. Audit Methodology

[A] (a) Mandatory collision check on the deliverable path (FREE). (b) Full inventory of implementation artifacts. (c) Direct reading of the invariant-critical modules in full (trace, trace_schema, agent_instance, runtime, promotion, memory_governance, review_decision, workflow, tool, tool_executor, orchestrator, observability). (d) Docstring + targeted-body reading of the remaining modules. (e) Two cross-cutting evidence sweeps: an external/vendor/network-import sweep across all of `execution/` (INV-12), and a Knowledge write-path sweep (INV-8). (f) Per-module mapping to the frozen architecture. (g) Per-module verification against the ten directive checks. (h) Classification and disposition.
[E] Evidence-first (PR-1): every finding cites the code read or a sweep result; no finding rests on assumption.

## 4. Corpus Audited

[E] **Implementation modules read in full:** `execution/trace.py`, `trace_schema.py`, `agent_instance.py`, `runtime.py`, `promotion.py`, `memory_governance.py`, `review_decision.py`, `workflow.py`, `tool.py`, `tool_executor.py`, `orchestrator.py`, `observability.py`.
[E] **Read by docstring + targeted sweep:** `agent_definition.py`, `skill.py`, `governance_reader.py`, `human_review_observation.py`, `verification.py`, `metrics.py`, `tool_contract.py`, `tool_registry.py`, `baseline_capture.py`, `memory/extractor.py`, `memory/consumption.py`, `memory/*` experiment modules, `knowledge/*`, `tools/validators/*`.
[E] **Sweeps:** external-import sweep over `execution/**/*.py` → **zero** matches; Knowledge write-path sweep over `execution/knowledge/` → **zero** writes.
[E] **Trace corpus:** 540 records across 135 `execution/traces/*.jsonl` files.

## 5. Implementation Inventory

[E] Counts (excluding `__pycache__`):
- `execution/` top-level implementation modules: ~34 `.py`.
- `execution/tests/`: 21 test modules.
- `execution/knowledge/`: 4 modules (+ runner). `execution/memory/`: 13 modules (extractors + experiment runners).
- `tools/`: 1 CLI + 13 validator modules + 1 test module.
- Data: `execution/traces/` (135 files, 540 records), `execution/memory/records/` (2 files), `execution/baseline/` (17 JSON snapshots).

[A] **Character of the corpus:** the vast majority of modules self-describe as **experiments / harness code**, explicitly "not a Framework" and "not an implementation of the [entity]" (verbatim in `memory/extractor.py`, `knowledge/*`, `memory/consumption.py`). This is pre-freeze prototype and evidence-gathering code, not a claimed Native Core.

## 6. Module Mapping Table

[A] Each module/group mapped to its frozen subsystem, layer, entity, spec, and governing invariants.

| Module / group | Subsystem (canonical owner) | Layer | Frozen entity | Engineering spec | Key invariants |
|---|---|---|---|---|---|
| `trace.py`, `trace_schema.py` | Trace (owned by no one) | L-Trace | Trace | trace_spec | INV-4, INV-5, INV-6 |
| `agent_definition.py` | Agent (Dept-owned Definition) | L3 Agent | Agent Definition | agent_spec | INV-2, INV-15 |
| `agent_instance.py` | Agent (transient) | L3 Agent | Agent Instance | agent_spec | INV-3, INV-4, INV-13 |
| `runtime.py` | Runtime (central) | L2 Runtime | Runtime | runtime_spec | INV-3, OQ-2 |
| `workflow.py` | Workflow (central) | L6 Workflow | Workflow | workflow_spec | INV-13, INV-4 |
| `skill.py` | Skill (central) | L5 Skill | Skill | skill_spec | INV-4, INV-12, INV-15 |
| `tool.py`, `tool_executor.py`, `tool_registry.py`, `tool_contract.py`, `verification.py` | Infrastructure / Tool boundary | L9 Infra | Tool | infrastructure_spec | INV-12 |
| `orchestrator.py` | Runtime/Workflow execution path | L2/L6 | Agent Instance action | runtime/workflow spec | INV-4, INV-13, §14.2 |
| `memory/extractor.py`, `memory/*` | Memory (scoped) | L7 Memory | Memory | memory_spec | INV-5, INV-7, INV-8 |
| `promotion.py` | Optimization→Governance (detect-only) | L10→L1 | Memory→Knowledge candidate | optimization/governance spec | INV-8, PR-3 |
| `memory_governance.py` | Governance view over Memory | L1 Governance | Memory/Knowledge boundary | governance_spec | INV-8 |
| `review_decision.py` | Governance (human review record) | L1 Governance | Trace of a Governance Event | governance/trace spec | INV-4, INV-6, INV-8, PR-4 |
| `human_review_observation.py` | Governance observation (read-only) | L1 Governance | (observation, not entity) | governance_spec | PR-3 |
| `knowledge/*` | Knowledge retrieval experiment | L8 Knowledge | Knowledge (consumption only) | knowledge_spec | INV-7, INV-8 |
| `observability.py`, `metrics.py` | Optimization/observability (read-only) | L10 | (telemetry, not Trace) | optimization_spec | AD-8, PR-3 |
| `governance_reader.py` | Shared read-only doc parsing | (facility) | (shared primitive) | — | — |
| `baseline_capture.py`, `run_*.py` | Experiment/report runners | (harness) | — | — | — |
| `tools/validators/*`, `validate_execution_catalog.py` | Repo-governance tooling (different plane) | (tooling) | — | — | read-only |

## 7. Dependency Conformance

[E] **External/vendor/network dependencies (INV-12):** an import sweep across all of `execution/**/*.py` returned **zero** matches for `requests`/`urllib`/`http`/`httpx`/`socket`/`openai`/`anthropic`/`boto3`/`google`/`langchain`/`llama`/`torch`/`psycopg`/`sqlalchemy`/`redis`/etc. `tool.py` states it directly: "Tool remains the sole entity permitted a direct external dependency … this implementation still holds none — it only reads local repository files." **INV-12: upheld** (trivially — the whole implementation is offline/local).
[E] **Dependency direction (Blueprint §20/§21):** the modules declare and honour one-directional layering: `promotion.py` "Never imports execution.trace, execution.orchestrator, execution.tool, execution.skill, execution.workflow, or execution.agent_definition"; `metrics.py` reads only `observability.py` ("Trace → Observability → Metrics … strict and one-directional"); `observability.py` is a "pure Trace reader" with "no call site inside orchestrator.py, skill.py, or tool.py." **No forbidden import observed.**
[A] **Trace as a sink:** `trace.py` imports nothing from memory/knowledge/optimization; memory/observability/metrics/promotion read Trace, never write it — matching the frozen acyclic graph (Blueprint §21). **Dependency conformance: PASS** for every module read.

## 8. Governance Conformance

[E] **Trace immutability & unconditionality (INV-4/5; §14.2):** `TraceWriter.write()` "only ever appends a new line"; `TraceRecord` is a `frozen=True` dataclass; `orchestrator.run()` writes a Trace record for spawn, every skill action, every escalation, and terminate — production is unconditional. No edit/delete path exists. **Upheld.**
[E] **Capture-at-write (INV-6; PR-5):** `review_decision.record_decision()` stores the full `CandidatePackage` snapshot via `asdict` "captured permanently at record time," explicitly because `select_candidates()` is recomputable and a bare reference "could resolve to different facts later." **Upheld.**
[E] **Memory→Knowledge promotion (INV-8):** `promotion.py` "makes no promotion decision, approves nothing … only reads Memory and Trace and produces a ranked … package for a human"; `memory_governance.trust_decision()` makes a human `reject` "absolute … matching Domain Model invariant 8's 'never automatic' spirit"; `review_decision.py` "records an already-made human judgment; it never makes one." **No automatic promotion path exists. Upheld.**
[E] **Knowledge unguided writes (INV-8):** write-path sweep over `execution/knowledge/` returned **zero** writes; `knowledge/*` is read-only retrieval "without creating any Knowledge entity, storage convention, or promotion pipeline." **No unguided Knowledge write path exists.**
[E] **Human authority over automation (§6.2 invariant 2; PR-3):** `human_review_observation.py` "never scores reviewer quality, never infers correctness, never suggests or ranks a decision"; `observability.py`/`metrics.py` derive telemetry only. **No automation decides or overrides governance.**
[E] **Agent-to-agent (INV-13):** `orchestrator.run()` spawns exactly one Agent Instance per run and drives Workflow→Skill→Tool; there is **no** agent-to-agent messaging channel anywhere. Coordination is only through Workflow, Trace, and governed review. **Upheld.**
[E] **Observability ≠ accountability (Freeze AD-8):** `observability.py` "Never writes execution behavior … a pure Trace reader"; telemetry is categorically separate from Trace. **Upheld.**
[E] **Fail-closed authorization (§14.2; PR-4):** `orchestrator.py` refuses a Workflow/Skill not in the Agent Definition's Permitted list and records it as an `escalation` Trace; `review_decision.validate_decision_input()` "fail[s] closed with a complete explanation," writing nothing to Trace on invalid input. **Upheld.**

## 9. Invariant Conformance

[E] Per-invariant result from the code read:

| Invariant | Result | Evidence |
|---|---|---|
| INV-3 (one Definition, one Runtime) | **Conforms** | `agent_instance.spawn()` binds one definition + one runtime; `runtime.bind_runtime()` selects exactly one |
| INV-4 (one Trace per action, unconditional) | **Conforms** | `orchestrator.run()` writes a record per action; no conditional skip |
| INV-5 (Trace immutable/append-only) | **Conforms** | append-only writer; `frozen` record; no edit/delete path |
| INV-6 (capture at write-time) | **Conforms** | full candidate snapshot persisted in `review_decision.py` |
| INV-7 (Knowledge durable / Memory bounded) | **Conforms (as experiment)** | `memory_governance` treats 100% of corpus "stale" under a 1-hour retention window; Knowledge modules read-only |
| INV-8 (governed promotion, never automatic) | **Conforms** | no automatic Memory→Knowledge path; human reject absolute |
| INV-12 (Tool sole external boundary) | **Conforms (trivially)** | zero external imports anywhere |
| INV-13 (no agent-to-agent outside Workflow) | **Conforms** | no agent-to-agent channel; single instance per run |
| INV-2/15 (Definition implements Capability; 0+ Skills/Workflows) | **Conforms** | `agent_definition.py` exposes Permitted Skills/Workflows for authorization |
| §14.2 / PR-4 (fail closed) | **Conforms** | escalation records; validation writes nothing on failure |

[A] **No invariant violation was found in any module read.** The behavioural conformance is unusually strong for pre-freeze code, and is achieved with disclosed limitations rather than hidden ones.

## 10. Subsystem Findings

[E] **Trace** — behaviourally conformant; storage is explicitly a "disposable implementation choice, not a ratified convention," and `schema_version`/`duration_ms` evolution is an admitted experiment. `new_record()` hardcodes `knowledge_consumed=()`/`memory_consumed=()` — a **[A] partial-capture limitation**, not a violation.
[E] **Runtime** — a thin facility ("not a scheduler … no allocation, no scoring"); reads governance descriptors. Conformant to OQ-2 (facility, not independent actor).
[E] **Agent** — Instance faithfully ephemeral (never persisted); Definition surfaces permitted-set for authorization. Conformant.
[E] **Workflow** — treats document order as execution order, disclosed as an implementation-tier choice, not a governance assertion. Conformant.
[E] **Tool / Infrastructure** — three local-file adapters; no external dependency; retry/timeout/telemetry are explicit no-op extension points. Conformant.
[E] **Memory** — extractor and governance are read-only, derived, non-authoritative; self-described as experiments. Conformant-in-spirit; **[A] not the frozen Memory boundary**.
[E] **Knowledge** — retrieval-only experiment; no entity, no promotion path, no writes. Conformant-in-spirit; **[A] not the frozen Knowledge boundary**.
[E] **Governance** — `promotion`/`memory_governance`/`review_decision`/`human_review_observation` collectively realise detect-then-govern with humans deciding. Strongly conformant.
[E] **Optimization/observability** — read-only telemetry; separated from Trace. Conformant.
[E] **`tools/` validators** — read-only repo-governance tooling ("no file is ever modified"); a different plane from AIOS runtime entities. Conformant as tooling.

## 11. Risk Assessment

[A] Risks bearing on building Phase 3 on or beside this legacy code:

| ID | Risk | Severity | Evidence/Reason |
|---|---|---|---|
| LR-1 | Legacy code is adopted as the Native Core **without re-ratification** under the Implementation Constitution | **High** | Most modules self-describe as experiments/harness, not entity implementations; they were built before the freeze/constitution existed |
| LR-2 | Disposable Trace storage convention (JSON-Lines) is mistaken for a **ratified** Trace Framework | Medium | `trace.py` explicitly disclaims ratification; a future Trace Framework is reserved |
| LR-3 | Trace `knowledge_consumed`/`memory_consumed` hardcoded empty → **incomplete provenance** if promoted as-is | Medium | `trace.new_record()` sets both to `()` |
| LR-4 | Experiment runners that write to `execution/traces/` and `memory/records/` **co-mingle** experiment output with the accountability corpus | Medium | multiple `run_*.py`/experiment modules write records |
| LR-5 | `schema_version` normalization masks **three real on-disk generations**, risking silent misread if a fourth appears | Low | `trace_schema.py` normalizes three generations by hand |
| LR-6 | `knowledge/*` retrieval treated as the frozen Knowledge boundary (it is not) | Medium | modules disclaim being the entity; admission model is still reserved |
| LR-7 | Department is unresolved everywhere (`department_status="unavailable"`) → ownership mapping absent (INV-1/2 realization deferred) | Low | `promotion.py` reports it honestly |
| LR-8 | Tests encode current experimental behaviour; may **lock in** conventions not yet ratified | Low | 21 test modules assert on the harness's own shapes |

[A] None of these is an invariant violation; all concern **status** (legacy/experimental vs frozen Native Core), not correctness.

## 12. Legacy Classification Matrix

[A] Exactly one classification per module/group. Definitions: **CONFORMANT** = upholds its invariants, structurally sound; **LEGACY** = conforms in spirit but is pre-freeze experimental/harness code not built under the Implementation Constitution; **PARTIALLY CONFORMANT** = conforms with a disclosed limitation; no module was found NON-CONFORMANT, QUARANTINE(dangerous), or UNDETERMINED.

| Module / group | Classification | Basis |
|---|---|---|
| `trace.py` | **PARTIALLY CONFORMANT** | append-only/immutable (conforms) but unratified storage + empty knowledge/memory-consumed (LR-2/LR-3) |
| `trace_schema.py` | CONFORMANT | honest multi-generation normalization; read-only |
| `agent_instance.py`, `agent_definition.py`, `runtime.py` | CONFORMANT | faithful to Domain Model §4/§5/§6; facility/ephemeral discipline |
| `workflow.py`, `skill.py`, `orchestrator.py` | CONFORMANT | unconditional Trace, fail-closed authorization, no agent-to-agent |
| `tool.py`, `tool_executor.py`, `tool_registry.py`, `tool_contract.py`, `verification.py` | CONFORMANT | no external dependency; extension points inert |
| `promotion.py`, `memory_governance.py`, `review_decision.py`, `human_review_observation.py` | CONFORMANT | detect-then-govern; human authority absolute; capture-at-write |
| `observability.py`, `metrics.py`, `governance_reader.py` | CONFORMANT | read-only, one-directional, separated from Trace |
| `memory/extractor.py` + `memory/*` experiments | **LEGACY** | self-described experiment; not the frozen Memory boundary |
| `knowledge/*` | **LEGACY** | self-described retrieval experiment; not the frozen Knowledge boundary |
| `baseline_capture.py`, `run_*.py` report/experiment runners | **LEGACY** | harness/evidence scripts; not Native Core |
| `execution/tests/*` | **LEGACY** | assert current experimental shapes; re-baseline under Phase 3 |
| `tools/validators/*`, `validate_execution_catalog.py` | CONFORMANT | read-only repo tooling; different plane |
| Trace corpus (`traces/`), `memory/records/`, `baseline/` | CONFORMANT (as evidence) | immutable append-only records; valuable audit evidence |

## 13. KEEP list

[A] Recommended to KEEP as conformant reference/evidence (final decision [O] Architect):
- The behaviourally-conformant core entity modules: `trace_schema.py`, `agent_instance.py`, `agent_definition.py`, `runtime.py`, `workflow.py`, `skill.py`, `orchestrator.py`, the Tool group, and the Governance group (`promotion`, `memory_governance`, `review_decision`, `human_review_observation`).
- `observability.py`, `metrics.py`, `governance_reader.py`.
- The Trace corpus and baselines as **audit evidence** (immutable; do not delete).
- `tools/validators/*` as read-only repo tooling.

## 14. MODIFY list

[A] Recommended to require governed treatment **before promotion** to Native Core (no modification performed here; disposition [O] Architect):
- `trace.py` — the Trace storage convention and the `knowledge_consumed`/`memory_consumed` empty-capture must be **ratified/completed under the frozen Trace spec** before this becomes the Native Core Trace (LR-2, LR-3). Until then it is legacy reference.
- `trace_schema.py` — the three-generation normalization should be re-derived under a ratified schema discipline if Trace is promoted (LR-5).

## 15. QUARANTINE list

[A] Recommended to isolate from the Native Core build so experiment output does not co-mingle with the accountability corpus (disposition [O] Architect):
- The experiment runners and their outputs: `memory/*` experiment/`run_*` modules, `knowledge/*` experiment runners, `baseline_capture.py`, and the `execution/memory/records/` + `execution/baseline/` outputs.
- [A] "Quarantine" here means **fence off during Phase 3**, not delete — the evidence remains valuable.

## 16. REMOVE list

[A] **None.** [E] An auditor deletes nothing, and no module was found to be a danger requiring removal; the Trace corpus in particular is immutable evidence (INV-5) and must not be removed. [O] Any removal decision is reserved to the Architect.

## 17. REBUILD list

[A] Recommended to be **rebuilt under the frozen Engineering Specs in Phase 3** rather than promoted as-is, because they self-describe as experiments and are not the frozen entity (no replacement designed here; disposition [O] Architect):
- `execution/knowledge/*` → rebuilt under the frozen Knowledge spec **after** the reserved Knowledge admission model is decided (Readiness Review §18 condition 1).
- `execution/memory/*` experiment layer → rebuilt under the frozen Memory spec as the governed derived-memory boundary.
- `execution/tests/*` → re-baselined as conformance tests asserting the frozen invariants (Blueprint §27), rather than current experimental shapes.

## 18. Overall Readiness

[A] The legacy implementation is **conformant-in-spirit but LEGACY in status**: across every module read, **no invariant is violated**, external dependencies are absent (INV-12), Trace is immutable and unconditional (INV-4/5), Memory never self-promotes (INV-8), Knowledge takes no unguided writes, there is no agent-to-agent channel (INV-13), and automation never decides governance (§6.2 invariant 2). However, the corpus is largely **pre-freeze experimental/harness code that explicitly disclaims being the frozen entities**, and it was not built under the Implementation Constitution.
[A] **Net:** this code is a strong conformant **reference and evidence base**, not a drop-in Native Core. Phase 3 should proceed **under the frozen contract**, treating this implementation as legacy to be re-ratified/rebuilt module-by-module (§13–§17) — not silently adopted, and not discarded.
[O] Whether any legacy module is promoted, modified, quarantined, or rebuilt is reserved to the Architect.

## 19. Open Questions

[O] Reserved to the Architect:
- [O] Which KEEP modules (if any) are promoted into the Native Core, and under what re-ratification (§13/§14).
- [O] The Trace storage convention and full-provenance capture (`knowledge_consumed`/`memory_consumed`) — ratify or replace (LR-2/LR-3).
- [O] The Knowledge admission model (still reserved; blocks a conformant Knowledge rebuild — Readiness Review §18 condition 1).
- [O] Disposition of the Trace/experiment corpus co-mingling (LR-4): retention/quarantine policy.
- [O] Whether the untracked `execution/` tree is brought under version control, and at what point.
- [O] Realization of Department ownership (INV-1/2), currently unresolved everywhere (LR-7) — reserved to Phase 5.

## 20. Integrity Verification

[E] Post-write verification for this read-only audit:
- **Files created:** 1 — `docs/architecture/AIOS_LEGACY_IMPLEMENTATION_CONFORMANCE_AUDIT_v1.0.md` (this document).
- **No Python modified:** [E] no `.py` created or modified; the audit only read `.py` files; the repo tracks zero `.py`.
- **execution/ untouched:** [E] read-only; entirely untracked; not modified (no write, rename, or delete).
- **No architecture document modified:** [E] confirmed — only this new file added under `docs/architecture/`.
- **No engineering document modified:** [E] confirmed — `docs/engineering/` untouched.
- **No governance document modified:** [E] confirmed — `docs/governance/` untouched.
- **Trace count:** [E] 540 records — unchanged (no execution artifact written).
- **Commit status:** [E] not committed, not pushed.

[A] This audit fixed nothing, refactored nothing, renamed nothing, designed no replacement, proposed no architectural change, created no ADR, and modified no document. **It classified only.**

---

## Closing

[A] The existing implementation **conforms to the frozen AIOS invariants** wherever it was read — an unusually disciplined pre-freeze harness that upholds immutable Trace, governed promotion, the single (empty) Tool boundary, no agent-to-agent coupling, and human authority over automation, all with disclosed rather than hidden limitations. Its correct status, however, is **LEGACY**: experimental and harness code, not the frozen Native Core, and not built under the Implementation Constitution. It should be treated as conformant reference and evidence — kept, selectively re-ratified, quarantined from the Phase-3 build where it is experimental, and rebuilt under the frozen specs where it disclaims being the entity — with every promotion, modification, quarantine, removal, and rebuild decision reserved to the Architect. [O] This audit does not begin Phase 3.

**No file was modified, renamed, refactored, or fixed; no implementation, API, or replacement was designed; no architecture was changed; no ADR was created; no architecture, engineering, or governance document was modified. This is a new additive, read-only audit document only.**
