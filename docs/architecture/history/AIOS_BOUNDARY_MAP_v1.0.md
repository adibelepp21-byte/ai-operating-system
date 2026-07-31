# AIOS Execution Layer — Architecture Boundary Map v1.0

**Status:** Frozen Baseline
**Version:** v1.0
**Authority:** Subordinate to the ratified Engineering Constitution and Canonical Domain Model. Boundaries recorded here are evidence-derived from the real `execution/` codebase as of the Architecture Freeze v1.0 certification, not design intentions.
**Approved by:** Architect, Phase 6 — Architecture Baseline Formalization.

---

## Trace

- **Inputs:** An `AgentInstance` and bound `Runtime` object, optional `workflow`/`skills_used`/`tools_used`/`inputs`/`outputs`/`status`/`duration_ms`.
- **Outputs:** A `TraceRecord` (frozen dataclass), appended as one JSON line to a run-scoped `.jsonl` file.
- **Ownership:** `trace.py` exclusively. No other module defines or writes this shape.
- **Allowed dependencies:** None internal — a Layer 0 leaf module.
- **Forbidden dependencies:** Trace must never depend on Memory, Human Review, Promotion, or any higher-layer module — enforced simply by the fact that `trace.py` imports nothing from `execution/` at all.
- **Mutation authority:** None. `TraceWriter.write()` is the only method capable of touching the corpus, and it only ever appends.
- **Persistence authority:** Sole real persistence mechanism in this entire layer — `execution/traces/*.jsonl`.

## Memory

- **Inputs:** Trace records (real, on-disk, or supplied directly for testing).
- **Outputs:** `MemoryRecord` tuples — computed, not persisted.
- **Ownership:** `memory/extractor.py` exclusively.
- **Allowed dependencies:** `trace_schema.py` only.
- **Forbidden dependencies:** Memory must never depend on Human Review, Promotion, or Memory Governance — enforced by the module's own import list (confirmed unchanged across every phase this arc).
- **Mutation authority:** None — pure function, recomputed fresh on every call, proven by dedicated non-mutation tests.
- **Persistence authority:** None by default. `memory.MemoryStore` exists as an explicitly disposable convenience, used by no governance path.

## Human Review

- **Inputs:** `HumanReviewDecisionInput` — explicit, human-authored `decision`, `reviewer_identity`, `rationale`, `timestamp`, and (conditionally) `edited_content`, plus an immutable `candidate_snapshot`.
- **Outputs:** Exactly 3 real Trace records (spawn, decision, terminate) per call, mirroring `orchestrator.run()`'s own real pattern.
- **Ownership:** `review_decision.py` exclusively — sole writer of `human_review_decision_recorded` events.
- **Allowed dependencies:** `agent_definition.py`, `agent_instance.py`, `runtime.py`, `trace.py`, and `promotion.py` (type reference to `CandidatePackage` only).
- **Forbidden dependencies:** No dependency on `skill.py` or `workflow.py` — recording a review decision is deliberately not routed through the Skill/Workflow abstraction. No dependency on Memory Governance (the reverse direction is the only real one — Memory Governance reads Human Review's Trace output, never the other way).
- **Mutation authority:** None beyond the append-only Trace write. The `candidate_snapshot` embedded in a written record is never altered by this module or any other, proven by a real corpus-drift test.
- **Persistence authority:** Via Trace only — no independent storage.

## Promotion

- **Inputs:** Memory records and Trace records (for provenance cross-reference).
- **Outputs:** `CandidatePackage` tuples, ranked (tool > heuristic > model_generated > unknown source, then confidence, then occurrence, then recency) — a pure tie-break ordering, never a weighted score.
- **Ownership:** `promotion.py` exclusively.
- **Allowed dependencies:** `memory/extractor.py` only (for the `MemoryRecord` type and Trace loading).
- **Forbidden dependencies:** Explicitly never imports `trace.py` (writer), `orchestrator.py`, `tool.py`, `skill.py`, `workflow.py`, or `agent_definition.py` — this module has no path to touch any governance document, by design, stated in its own docstring.
- **Mutation authority:** None — makes no promotion decision, approves nothing, rejects nothing, writes nothing.
- **Persistence authority:** None.

## Verification

- **Inputs:** A cached fingerprint (or `None`) and the current call's parameters.
- **Outputs:** A boolean trust decision (`verify()`); a fingerprint tuple or `None` (`compute_fingerprint()`).
- **Ownership:** `verification.py` exclusively, consumed only by `tool_executor.py`.
- **Allowed dependencies:** None internal — a Layer 0 leaf module (standard library only: `hashlib`, `pathlib`).
- **Forbidden dependencies:** Tool adapters never import this module and never know it exists, by design — verification is invisible to the Tool implementations it protects.
- **Mutation authority:** None.
- **Persistence authority:** None — operates only on an externally-supplied, in-process cache dict it does not own.

## Tool Execution

- **Inputs:** A `ToolRequest` (canonical key, action, parameters), an optional externally-supplied cache.
- **Outputs:** An `ExecutorResult` / `ToolExecution` carrying both raw adapter output and a normalized response, plus verification metadata (`fingerprint`, `from_cache`, `verification_status`).
- **Ownership:** `tool.py` (public entry point + 3 real adapters), `tool_executor.py` (execution + cache/verification integration), `tool_registry.py` (adapter discovery).
- **Allowed dependencies:** `governance_reader.py`, `verification.py`, `tool_contract.py`, `tool_registry.py`.
- **Forbidden dependencies:** Tool Execution never depends on Trace, Memory, Human Review, or Promotion — it is consumed by higher layers (Skill, Memory Consumption), never the reverse.
- **Mutation authority:** Only over an externally-injected cache dict, and only additively/invalidation-wise (no silent overwrite of a valid entry without an explicit fingerprint mismatch).
- **Persistence authority:** None — the cache it may mutate is always supplied by, and owned by, its caller.

## Runtime

- **Inputs:** An Agent Definition's name, an optional explicit selector.
- **Outputs:** A bound Runtime object referencing a real, on-disk Runtime catalog document.
- **Ownership:** `runtime.py` exclusively.
- **Allowed dependencies:** `governance_reader.py` only.
- **Forbidden dependencies:** No dependency on Agent Instance, Trace, or any execution-result module — Runtime binding is a pure lookup step, resolved before any instance or Trace record exists.
- **Mutation authority:** None — read-only against real governance documents, confirmed by a dedicated read-only test.
- **Persistence authority:** None.

## Governance (document reading)

- **Inputs:** A file path to a real governance document.
- **Outputs:** Parsed text, Canonical Key, Version, section body/links.
- **Ownership:** `governance_reader.py` exclusively — deliberately not imported from, or coupled to, `tools/validators/` (a differently-purposed, independent implementation-tier layer per its own docstring).
- **Allowed dependencies:** None internal — a Layer 0 leaf module (standard library `re`, `pathlib` only).
- **Forbidden dependencies:** Never writes to any document it reads.
- **Mutation authority:** None.
- **Persistence authority:** None.

## Knowledge Prototype

- **Inputs:** A free-text query string.
- **Outputs:** `RetrievalHit` / `EvidenceReference` tuples pointing into `docs/`.
- **Ownership:** `execution/knowledge/*` — a fully self-contained subtree.
- **Allowed dependencies:** Only within its own subtree (`index.py`, `loader.py`).
- **Forbidden dependencies:** No module outside `execution/knowledge/` imports into it, and it imports nothing from the rest of the Execution Layer — confirmed structurally isolated. It has no path to Trace, Memory, Human Review, or any governed write.
- **Mutation authority:** None.
- **Persistence authority:** None — read-only over `docs/`, nothing cached to disk. It creates no Knowledge entity, storage convention, or promotion pipeline, by explicit, self-disclosed design.
