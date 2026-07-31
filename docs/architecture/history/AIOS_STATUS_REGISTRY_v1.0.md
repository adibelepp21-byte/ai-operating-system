# AIOS Execution Layer — Architecture Status Registry v1.0

**Status:** Frozen Baseline
**Version:** v1.0
**Authority:** Subordinate to `AIOS_ARCHITECTURE_CONSTITUTION_v1.0.md`. This registry is the permanent, evidence-derived record of every module's classification and every open question at the moment of the Architecture Freeze v1.0 certification.
**Approved by:** Architect, Phase 6 — Architecture Baseline Formalization.
**Evidence basis:** Architecture Evidence Freeze Report, Foundation Test Coverage Hardening Report, Verification Layer Repair Report, Architecture Freeze v1.0 Report (all produced this arc), plus a fresh regression run at the time of this document's creation (288/288 `execution/tests`, 20/20 `tools/tests`, Trace corpus stable at 540 records).

---

## Frozen Modules

Certified with dedicated test coverage, behaviorally verified against real data, zero known defects as of this baseline:

`trace.py`, `trace_schema.py`, `tool.py`, `tool_executor.py`, `tool_registry.py`, `tool_contract.py`, `verification.py`, `orchestrator.py`, `agent_definition.py`, `agent_instance.py`, `runtime.py`, `workflow.py`, `skill.py`, `governance_reader.py`, `memory/extractor.py`, `memory/consumption.py`, `promotion.py`, `review_decision.py`, `memory_governance.py`, `human_review_observation.py`.

## Experimental Modules

Self-disclosed as experimental in their own docstrings, real and functional but not asserted as governed conventions:

`memory/drift_experiment.py`, `baseline_capture.py`, `execution/memory/run_*.py` (all diagnostic CLI scripts).

## Dormant Modules

Zero inbound imports from outside their own subtree, zero real Trace usage, zero tests, no evidence of real execution:

`execution/knowledge/__init__.py`, `execution/knowledge/index.py`, `execution/knowledge/loader.py`, `execution/knowledge/retrieval.py`, `execution/knowledge/run_experiment.py`.

`execution/memory/lookup.py`, `execution/memory/history.py` — each has exactly one dedicated runner script and no other consumer; not dead, but integrated into nothing else.

## Dead Modules

Zero callers anywhere in the repository, confirmed by direct import-graph inspection (not inferred):

`execution/memory/quality.py` — no runner script, no test, no consumer of any of its seven functions (`confidence_calibration`, `observation_diversity`, `recency_weighting`, `duplicate_pattern_evaluation`, `retrieval_accuracy`, `stale_memory_detection`, `cross_skill_diversity`).

## Known Risks

- **`MemoryRecord.memory_id` non-persistence.** Regenerates via `uuid4()` on every extraction; any future code that naively persists or compares it across calls would silently break. Every current consumer correctly works around this by keying on `(observation_kind, content)` instead.
- **Silent skip in `detect_conflicts()`.** A Tool without a registered `cache_key_fn` (in `tool.py::CACHE_KEY_FNS`) is invisibly excluded from conflict detection, with no error or warning. Correct-by-design today; untested against a hypothetical future Tool added without one.
- **Duplicate indexing responsibility.** `memory/consumption.py::build_input_keyed_cache()` and `memory/lookup.py::build_index()` independently index the same real Trace evidence for separate experiments, never reconciled. No current harm; a risk if either is extended without noticing the other.

## Known Unknowns

- **Multi-reviewer behavior.** All 6 real Human Review events in the corpus carry the same `reviewer_identity`. Code is proven structurally independent of the identity's value; real behavioral evidence from a second reviewer does not exist.
- **Review precedence under real multi-decision.** `review_state()`'s precedence rule (`reject` > `edited` > `approved`) has never been exercised by a real case where the same `(observation_kind, content)` received more than one real decision.
- **Organic conflict occurrence.** `detect_conflicts()` is proven correct under a real, controlled scenario; zero organic (uncontrolled) conflicts have ever been found across four independent real-corpus scans.
- **`reject`/`edit` path generalization.** Each has exactly one real instance; correctness for that instance is proven, generalization beyond it is not.
- **`retention_seconds=3600`.** An undefended experimental default, never validated as a real policy value by any evidence gathered this arc.

## Deferred Decisions

- Whether `execution/memory/quality.py` should be deleted, wired in, or left as dead code — not decided; no directive has authorized either action.
- Whether the dormant `execution/knowledge/` subtree should be revived, extended, or removed — not decided; explicitly out of scope for every phase in this arc.
- Whether `memory/consumption.py` and `memory/lookup.py`'s parallel indexing should ever be reconciled into one mechanism — flagged as architectural debt, not scheduled.
- Whether Runtime should ultimately be an entity or an attribute — this question belongs to the ratified Canonical Domain Model (§9, explicit non-goal note), not this layer; recorded here only because Runtime's Execution Layer implementation exists and would be affected by either resolution.

## Future Prerequisites

Before any future phase may begin Knowledge Admission design, per the Architecture Freeze v1.0 recommendation (READY WITH DOCUMENTED LIMITATIONS):

1. A conflict-resolution contract must be explicitly designed and authorized — no existing Human Review decision shape covers it, and building one without authorization would violate this layer's own Evolution Protocol.
2. Real evidence of multi-reviewer behavior must be gathered through normal Human Review activity — not synthesized.
3. Real evidence of review precedence under a genuine multi-decision case must be gathered through normal Human Review activity — not synthesized.
4. Continued real or controlled-experiment evidence of conflict detection should be gathered (the drift-experiment technique against additional real document pairs is a legitimate, already-demonstrated method) before treating conflict handling as fully proven.

No other prerequisite is currently known to block future Execution Layer evolution within the boundaries already frozen in this baseline.
