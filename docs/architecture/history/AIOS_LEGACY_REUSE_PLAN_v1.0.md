# AIOS Legacy Reuse Plan v1.0

**Phase:** AIOS 2.97 — Legacy Asset Extraction & Reuse Plan. The **official plan** for what the existing implementation contributes to Phase 3 (Native Core). **Read-only / classification only.**
**Stance** [A]: this document implements nothing, refactors nothing, renames nothing, rewrites nothing, and modifies no code. It assigns each legacy asset exactly one reuse disposition, grounded in the frozen architecture and the Phase 2.96 Conformance Audit.
**Basis** [E]: the Legacy Implementation Conformance Audit v1.0 found **no invariant violation** in any module read; the legacy corpus is **conformant-in-spirit but LEGACY in status** — pre-freeze experimental/harness code, not built under the Implementation Constitution.
**Evidence (ONLY these):** Architecture Freeze v1.0 · Implementation Constitution v1.0 · Native Core Blueprint v1.0 · 11 Engineering Specifications · Legacy Implementation Conformance Audit v1.0 · Implementation Readiness Review v1.0 · DNA Library v1.0 · Architecture Specification v1.0.
**Tagging (never mixed):** **[E]** evidence from the documents above · **[A]** planning analysis · **[O]** Architect decision required.

---

## 1. Purpose

[A] To produce the **official Legacy Reuse Plan**: to decide, before any Phase 3 code is written, exactly which legacy implementation assets are inherited and in what form — Canonical Reference, Reusable Design, Reusable Behaviour, Reusable Test, Historical Evidence, or Phase 3 Rewrite Target — without touching a line of implementation.
[E] It follows directly from the Conformance Audit's dispositions (KEEP / MODIFY / QUARANTINE / REMOVE / REBUILD) and the Readiness Review's condition 2 (the pre-existing `execution/` implementation must be dispositioned before a conformant Phase 3 begins).
[A] The plan converts "the legacy code conforms" into "here is precisely what Phase 3 may stand on, and under what governance."

## 2. Scope

[E] **In scope:** every implementation asset inventoried in the Conformance Audit — `execution/**/*.py` (modules, helpers, runtime, bootstrap, tests), `tools/validators/*`, and the on-disk data corpora (`traces/`, `memory/records/`, `baseline/`).
[E] **Out of scope, by rule:** modifying, renaming, refactoring, or rewriting any file; producing implementation; beginning Phase 3.
[A] This is a **classification** deliverable. Each asset receives exactly one disposition; the decision to act on any disposition is reserved to the Architect.

## 3. Evidence

[E] Documents used, and what each contributes:

| Document | Contribution to this plan |
|---|---|
| Architecture Freeze v1.0 | frozen entities, invariants, boundaries, layers (the conformance target) |
| Implementation Constitution v1.0 | the governance that any reused code must be re-ratified under |
| Native Core Blueprint v1.0 | the eleven core package boundaries each asset maps into |
| 11 Engineering Specifications | the per-subsystem contracts a reused module must satisfy |
| Legacy Implementation Conformance Audit v1.0 | per-module classification and evidence (the direct input) |
| Implementation Readiness Review v1.0 | Phase-3 conditions (Knowledge admission model; `execution/` disposition) |
| DNA Library v1.0 | which reusable ideas are governed-only; the two anti-patterns |
| Architecture Specification v1.0 | the ten-layer model behind the package mapping |

[E] No source code is re-read in this phase; module facts are inherited from the Conformance Audit (which read them directly).

## 4. Legacy Asset Inventory

[E] Assets, grouped, with the nine required attributes (canonical subsystem · frozen entity · engineering spec · Blueprint package · current classification · future disposition · reuse confidence · governance caveat · implementation risk). Dispositions are defined in §11.

| Asset / group | Subsystem · Entity · Spec · Blueprint pkg | Audit classification | Disposition | Reuse conf. |
|---|---|---|---|---|
| `trace_schema.py` | Trace · Trace · trace_spec · Trace | CONFORMANT | **CANONICAL_REFERENCE** | High |
| `trace.py` | Trace · Trace · trace_spec · Trace | PARTIALLY CONFORMANT | **REUSE_AFTER_CONFORMANCE** | Medium |
| `agent_instance.py`, `agent_definition.py` | Agent · Agent Def/Instance · agent_spec · Agent | CONFORMANT | **CANONICAL_REFERENCE** | High |
| `runtime.py` | Runtime · Runtime · runtime_spec · Runtime | CONFORMANT | **CANONICAL_REFERENCE** | High |
| `orchestrator.py` | Runtime/Workflow · Agent-Instance action · runtime/workflow spec · Runtime/Workflow | CONFORMANT | **CANONICAL_REFERENCE** | High |
| `workflow.py` | Workflow · Workflow · workflow_spec · Workflow | CONFORMANT | **REUSE_AFTER_CONFORMANCE** | High |
| `skill.py` | Skill · Skill · skill_spec · Skill | CONFORMANT | **REUSE_AFTER_CONFORMANCE** | High |
| `tool.py`, `tool_executor.py`, `tool_registry.py`, `tool_contract.py` | Infra/Tool · Tool · infrastructure_spec · Infrastructure | CONFORMANT | **REUSE_AFTER_CONFORMANCE** | High |
| `verification.py` | Infra · (Tool support) · infrastructure_spec · Infrastructure | CONFORMANT | **REUSE_AS_IS** | Medium |
| `promotion.py` | Optimization→Governance · Memory→Knowledge candidate · optimization/governance spec · Optimization/Governance | CONFORMANT | **CANONICAL_REFERENCE** | High |
| `memory_governance.py` | Governance · Memory/Knowledge boundary · governance_spec · Governance | CONFORMANT | **CANONICAL_REFERENCE** | High |
| `review_decision.py` | Governance · Trace of Governance Event · governance/trace spec · Governance | CONFORMANT | **CANONICAL_REFERENCE** | High |
| `human_review_observation.py` | Governance · (observation) · governance_spec · Governance | CONFORMANT | **REUSE_AS_IS** | Medium |
| `observability.py`, `metrics.py` | Optimization · (telemetry) · optimization_spec · Optimization | CONFORMANT | **REUSE_AFTER_CONFORMANCE** | Medium |
| `governance_reader.py` | Shared facility · (primitive) · — · shared | CONFORMANT | **REUSE_AS_IS** | Medium |
| `memory/extractor.py` + `memory/*` experiments | Memory · Memory · memory_spec · Memory | LEGACY | **REIMPLEMENT** | Low |
| `knowledge/*` | Knowledge · Knowledge · knowledge_spec · Knowledge | LEGACY | **REIMPLEMENT** | Low |
| `baseline_capture.py`, `run_*.py` runners | (harness) · — · — · — | LEGACY | **HISTORICAL_ONLY** | Low |
| `execution/tests/*` | (tests) · — · — · — | LEGACY | **REUSE_AFTER_CONFORMANCE** (as conformance tests) | Medium |
| `tools/validators/*`, `validate_execution_catalog.py` | Repo tooling (different plane) · — · — · — | CONFORMANT | **REUSE_AS_IS** | High |
| `traces/` (540 records), `memory/records/`, `baseline/` | Trace/Memory corpora | CONFORMANT (evidence) | **HISTORICAL_ONLY** | — |

## 5. Canonical Reference Assets

[A] Assets whose **design is a correct expression of the frozen architecture** and should anchor Phase 3 as the reference to build to (disposition CANONICAL_REFERENCE):
- **Trace accountability shape** — `trace_schema.py` (honest multi-generation normalization) and the append-only/immutable `TraceRecord` discipline. [E] Embodies INV-4/5/6.
- **Governance spine** — `promotion.py` (detect-only ranking, one-directional imports), `memory_governance.py` (human-reject absolute), `review_decision.py` (records but never makes decisions; capture-at-write). [E] Embody INV-8, PR-3, PR-4, INV-6.
- **Execution path** — `orchestrator.py` (one Trace per action; fail-closed permitted-set authorization; no agent-to-agent). [E] Embodies INV-4, INV-13, §14.2.
- **Facility discipline** — `runtime.py` (facility, not scheduler), `agent_instance.py`/`agent_definition.py` (ephemeral instance; permitted-set). [E] Embody INV-3, OQ-2.
[A] Canonical Reference means: **the Native Core is built to match these designs' governance properties**, re-ratified under the Implementation Constitution — not necessarily by copying the files verbatim. [O] Verbatim adoption vs. re-authoring is the Architect's choice.

## 6. Directly Reusable Assets

[A] Assets recommended for reuse **essentially as-is** (disposition REUSE_AS_IS), because they are read-only, self-contained, and carry no unratified convention that must change first:
- `verification.py` — the isolated fingerprint/verify layer (no external dependency; inert until a cache is attached).
- `human_review_observation.py` — read-only descriptive measurement of real review events.
- `governance_reader.py` — shared read-only document parsing.
- `tools/validators/*` + `validate_execution_catalog.py` — read-only repo-governance tooling on a different plane from the runtime entities.
[E] Reuse confidence for the tooling is High (the Conformance Audit found it "no file is ever modified"). [A] REUSE_AS_IS still requires the standard Phase-3 conformance review (Implementation Constitution §10), but no design change is anticipated.

## 7. Reusable Behaviour

[A] Assets whose **behaviour** (not necessarily their exact form) should be inherited, but only **after conformance re-ratification** under the frozen specs (disposition REUSE_AFTER_CONFORMANCE):
- **Tool boundary behaviour** — `tool.py`/`tool_executor.py`/`tool_registry.py`/`tool_contract.py`: the request/execution/evidence/failure separation and inert extension points. Caveat [E]: currently holds **no** external dependency, so INV-12 is satisfied trivially; promoting it as the real Tool boundary requires ratifying how an actual external dependency is confined (infrastructure_spec §13; Freeze §10 reserved).
- **Workflow/Skill execution behaviour** — `workflow.py`/`skill.py`: document-order execution and permitted-set dispatch. Caveat [E]: retry/branching/scheduling are explicitly unaddressed and must not be silently invented (workflow_spec §12/§14).
- **Telemetry behaviour** — `observability.py`/`metrics.py`: strict Trace→Observability→Metrics one-directional derivation, separated from accountability (Freeze AD-8).
[A] REUSE_AFTER_CONFORMANCE means: the behaviour is a strong starting point, but a governed conformance pass (naming, dependency, Trace, spec compliance — Implementation Constitution §9/§10) must pass **before** it enters the Native Core.

## 8. Reusable Tests

[A] The existing test suite (`execution/tests/*`, 21 modules) is disposition **REUSE_AFTER_CONFORMANCE**, re-based as **conformance tests** (Blueprint §27):
- [E] They currently assert the harness's own experimental shapes (Conformance Audit LR-8), so they must be re-anchored to assert the **frozen invariants** — exactly one Trace per action (INV-4), Trace never mutates (INV-5), Memory never self-promotes (INV-8), only Tool crosses the external boundary (INV-12), no agent-to-agent (INV-13).
- [A] Their **coverage map** (which behaviours are exercised) is directly reusable as a checklist; their **assertions** need re-ratification to the frozen contract rather than the current shapes.
[O] Whether the re-based tests are authored fresh or migrated is reserved to the Architect.

## 9. Historical Assets

[A] Assets whose value is **evidence of what happened**, not code to run in Phase 3 (disposition HISTORICAL_ONLY):
- **Trace corpus** — `execution/traces/` (540 records). [E] Immutable append-only records (INV-5); they are audit evidence and must not be modified or removed. They document the harness's real behaviour but are not a Native-Core input.
- **Memory/baseline corpora** — `execution/memory/records/`, `execution/baseline/` (17 snapshots): evidence of the experiments' measured findings.
- **Experiment/report runners** — `baseline_capture.py`, `run_*.py`: they produced the evidence; their purpose is served. [A] Keep as history; do not carry into the Native Core.
[A] HISTORICAL_ONLY is distinct from ARCHIVE: these remain in place as evidence; no asset in this plan is dispositioned ARCHIVE or REMOVE (an auditor deletes nothing; the Trace corpus in particular is protected by INV-5).

## 10. Assets Requiring Reimplementation

[A] Assets that **self-describe as experiments** and are not the frozen entity, hence must be **rebuilt under the frozen specs** in Phase 3 (disposition REIMPLEMENT):
- **`memory/*` experiment layer** — rebuilt under `memory_spec` as the governed derived-memory boundary (derive from Trace; bounded retention; never self-promote; never rewrite Trace).
- **`knowledge/*` retrieval experiment** — rebuilt under `knowledge_spec` **after** the reserved **Knowledge admission model** is decided (Readiness Review §18 condition 1; Freeze §10). [E] The current modules explicitly create "no Knowledge entity, storage convention, or promotion pipeline."
[A] REIMPLEMENT reuses the **design lessons** (tiered memory, content-addressed representation, retrieval structure — DNA Library Letta/LlamaIndex entries) as governed ideas, not the experimental code. [O] The admission-model decision gates the Knowledge rebuild.

## 11. Reuse Matrix

[A] The six dispositions and their meaning:

| Disposition | Meaning | Assets |
|---|---|---|
| **CANONICAL_REFERENCE** | design is a correct expression of the frozen architecture; Native Core is built to match it | Trace shape (`trace_schema.py`); governance spine (`promotion`, `memory_governance`, `review_decision`); execution path (`orchestrator`); facilities (`runtime`, `agent_instance`, `agent_definition`) |
| **REUSE_AS_IS** | read-only, self-contained, no unratified convention to change first (standard conformance review still applies) | `verification.py`, `human_review_observation.py`, `governance_reader.py`, `tools/validators/*` |
| **REUSE_AFTER_CONFORMANCE** | strong behaviour; must pass a governed conformance pass before entering the Native Core | `trace.py`, `workflow.py`, `skill.py`, Tool group, `observability.py`/`metrics.py`, `execution/tests/*` |
| **REIMPLEMENT** | self-described experiment; rebuild under the frozen spec | `memory/*`, `knowledge/*` |
| **HISTORICAL_ONLY** | evidence of what happened; not a Native-Core input | `traces/`, `memory/records/`, `baseline/`, `baseline_capture.py`, `run_*.py` |
| **ARCHIVE** | (none) | — |

[E] No asset is dispositioned ARCHIVE or REMOVE. [A] Every asset from the Conformance Audit inventory is accounted for exactly once.

## 12. Dependency Impact

[A] Reuse must preserve the frozen dependency graph (Blueprint §20/§21). Observed legacy dependency facts (Conformance Audit §7) and their Phase-3 implication:
- [E] `trace.py` imports nothing from memory/knowledge/optimization → Trace remains a sink; **safe** to reference first.
- [E] `promotion.py`/`observability.py`/`metrics.py` are strictly one-directional over Trace → reusing them introduces **no** forbidden import.
- [A] **Initialization-order fit** (Blueprint §23): the CANONICAL_REFERENCE assets sit at the base of the order (infrastructure → trace → memory → governance → …), so adopting them first respects Fail-Closed bootstrap.
- [A] **Coupling caveat:** `review_decision.py` imports `agent_definition`, `runtime`, `agent_instance`, `trace`, and `promotion.CandidatePackage`. Reusing it pulls those five in together — consistent with the frozen graph, but it means the governance-record path and the execution path share primitives; the Phase-3 conformance pass must confirm this shared use stays within permitted edges.
- [E] Tool group holds **no** external dependency today; the dependency impact of a *real* external Tool is deferred (infrastructure_spec §13; reserved).

## 13. Risk Assessment

[A] Risks specific to reusing legacy assets (distinct from the general Phase-3 risks in the Readiness Review):

| ID | Risk | Severity | Mitigation recommendation [A] |
|---|---|---|---|
| RU-1 | A CANONICAL_REFERENCE asset is copied verbatim and thereby imports an **unratified convention** (e.g. JSON-Lines Trace storage) as if frozen | High | Adopt the **design/governance properties**, ratify the convention separately (trace_spec); do not equate reference with ratification |
| RU-2 | REUSE_AFTER_CONFORMANCE assets enter the Native Core **without** the conformance pass actually running | High | Gate promotion on Implementation Constitution §9/§10; fail closed if the pass is skipped |
| RU-3 | REIMPLEMENT lessons drift into **re-adopting the experimental code** rather than rebuilding under spec | Medium | Treat `memory/*` and `knowledge/*` as DNA (ideas), not code, per DNA Library governance frame |
| RU-4 | `trace.py`'s empty `knowledge_consumed`/`memory_consumed` capture is inherited, yielding **incomplete provenance** | Medium | Complete full-provenance capture under trace_spec before REUSE_AFTER_CONFORMANCE clears (Conformance Audit LR-3) |
| RU-5 | Knowledge rebuild proceeds **before** the reserved admission model is decided | High | Block the `knowledge/*` REIMPLEMENT on Readiness Review §18 condition 1 |
| RU-6 | Historical corpora are **modified or pruned**, damaging immutable evidence | Medium–High | HISTORICAL_ONLY assets are read/retain-only; `traces/` is protected by INV-5 |
| RU-7 | Re-based tests **lock in** current shapes instead of frozen invariants | Medium | Re-anchor assertions to invariants (Blueprint §27) before reuse |

[A] None of these is a present violation; all are **reuse-process** risks to govern during Phase 3.

## 14. Phase 3 Starting Point

[A] The recommended, evidence-grounded starting posture for Phase 3 (subject to Architect authorization):
1. [A] **Anchor on the CANONICAL_REFERENCE governance spine and Trace shape** — build the Native Core Trace, Governance (promotion/review), and execution-path boundaries to match these designs' governance properties, re-ratified under the Implementation Constitution.
2. [A] **Bring REUSE_AFTER_CONFORMANCE behaviour through the conformance gate** (Trace storage + full provenance, Workflow/Skill, Tool boundary, telemetry, tests) before it becomes Native Core.
3. [A] **Defer the REIMPLEMENT boundaries** (`memory/*`, `knowledge/*`) until their specs — and, for Knowledge, the admission model — are ready; rebuild under spec, reusing only the DNA.
4. [A] **Keep HISTORICAL_ONLY corpora** as immutable evidence; do not build on the experiment runners.
[E] This starting point satisfies the Readiness Review's condition 2 (the `execution/` implementation is now dispositioned) and keeps every un-audited or experimental asset out of the conformant core.
[O] The authorization to begin Phase 3, and the disposition of every reserved item, remain the Architect's.

## 15. Open Questions

[O] Reserved to the Architect:
- [O] For each CANONICAL_REFERENCE asset: **verbatim adoption vs. re-authoring** to match the reference.
- [O] Ratification of the Trace storage convention and full-provenance capture before `trace.py` clears REUSE_AFTER_CONFORMANCE.
- [O] The **Knowledge admission model** (gates the `knowledge/*` REIMPLEMENT).
- [O] Whether the untracked `execution/` tree is brought under version control, and when.
- [O] Retention/quarantine policy for the HISTORICAL_ONLY corpora.
- [O] Realization of Department ownership (INV-1/2), unresolved in the legacy code — reserved to Phase 5.

## 16. Integrity Verification

[E] Post-write verification for this read-only planning document:
- **Files created:** 1 — `docs/architecture/AIOS_LEGACY_REUSE_PLAN_v1.0.md` (this document).
- **File modifications:** 0 — no implementation, no code, no rename, no refactor, no rewrite.
- **Python changes:** 0 — no `.py` read-and-written; no `.py` modified.
- **execution/ changes:** 0 — not touched (read-only classification, using inherited audit facts).
- **Architecture / engineering / governance documents modified:** 0.
- **Trace count:** 540 — unchanged.
- **Commit status:** not committed, not pushed.

[A] This plan changed no implementation, renamed nothing, refactored nothing, and rewrote nothing. **It classified only.**

---

## Closing

[A] This Legacy Reuse Plan converts the Conformance Audit's finding — that the pre-freeze implementation conforms to the frozen invariants but is LEGACY in status — into an official, per-asset inheritance decision. The governance spine, Trace shape, execution path, and facility modules are **Canonical Reference** the Native Core is built to match; the Tool/Workflow/Skill/telemetry behaviour and the tests are **Reusable After Conformance**; a handful of read-only modules and the repo tooling are **Directly Reusable**; the memory and knowledge experiments are **Reimplement** targets under their frozen specs; and the Trace/experiment corpora are **Historical evidence** to retain, never to build on. No asset is archived or removed, and nothing is inherited without passing the Implementation Constitution's conformance gate. [O] Every promotion, ratification, reimplementation, and the start of Phase 3 remain reserved to the Architect. **This plan does not begin Phase 3.**

**No file was modified, renamed, refactored, or rewritten; no implementation was produced; no architecture, engineering, or governance document was modified. This is a new additive, read-only planning document only.**
