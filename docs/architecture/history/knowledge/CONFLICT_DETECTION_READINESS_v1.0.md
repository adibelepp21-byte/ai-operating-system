# Conflict Detection Readiness v1.0

**Status:** Read-only analysis. No conflict logic modified.
**Version:** v1.0
**Authority:** Subordinate to `AIOS_ARCHITECTURE_CONSTITUTION_v1.0.md`. Analyzes `execution/memory_governance.py::detect_conflicts()` and its supporting mechanisms as they exist today.
**Approved by:** Architect, Phase 9 — Knowledge Admission Evidence Closure & Contract Readiness Assessment.

---

## What Is Inspected

`memory_governance.detect_conflicts()`; `tool.py::CACHE_KEY_FNS` (cache-key registration); `execution/memory/drift_experiment.py` and `execution/memory/run_drift_experiment.py` (the real, controlled drift scenario); `execution/tests/test_memory_governance.py::ConflictHandlingTest` (the existing conflict tests).

## Conflict Classes Currently Detectable

**One class, proven real**: two memories that reduce to the same Tool-derived "subject" (via that Tool's own registered `cache_key_fn`, e.g. `(tool_key, reference_target, expected_reference)` for the cross-reference Tool) but disagree on the boolean `resolved` outcome. Proven via a real, controlled experiment: a genuine file edit between two real Tool calls produces two memories with the same subject key and different `resolved` values, correctly flagged.

## Conflict Classes Currently Undetectable

- **Heuristic-sourced conflicts.** Any evidence with no `tool_key` (all heuristic-only Skills: authority-boundary-check, staleness-detection, and the heuristic branch of citation-discipline-verification) is unconditionally skipped by `_subject_key_and_resolved()`, confirmed by `test_heuristic_sourced_memories_never_produce_conflicts`. There is no mechanism at all for two heuristic flags to be recognized as conflicting.
- **Cross-Tool or cross-`observation_kind` conflicts.** The subject key is derived entirely from one Tool's own parameter names; two different Tools (or two different Skills using the same Tool differently) producing seemingly-related but structurally different evidence about the same real-world subject have no shared key and cannot be matched.
- **Semantic/textual conflicts with no shared identifying parameter.** Two pieces of content that say opposite things in different words, with no common `reference_target`/`document_path`-style parameter to key on, are invisible to this mechanism entirely. (The `terminology_confusion_flag` similarity technique exists elsewhere in this codebase, but is not wired into conflict detection.)
- **Unregistered-Tool blind spot.** Any Tool without a registered `cache_key_fn` is silently excluded — currently a non-issue (100% of the 3 real Tools are registered), but structurally unenforced against a future Tool added without one.
- **Knowledge-vs-evidence conflicts.** Categorically untestable — no Knowledge entity exists anywhere in this system to conflict with anything.

## Coverage Sufficiency for Future Knowledge Admission Design

**Not sufficient, assessed honestly.** The one proven class (same-Tool, same-subject-key, differing boolean `resolved`) is narrow by construction — a true/false disagreement about one specific, parameter-identified check. A future Knowledge Admission design will very plausibly need to detect a richer class of conflict: two admitted (or candidate) pieces of *textual* Knowledge asserting incompatible things about a broader subject, not merely two Tool calls disagreeing on a boolean. No evidence gathered anywhere in this repository demonstrates this richer class is detectable by the current mechanism, because the current mechanism was never designed for it — it was built and validated specifically for the Memory-layer, Tool-call-disagreement case.

## Can Additional Controlled Experiments Add Meaningful Evidence Without a Contract Change?

**Yes, at least one concrete gap is addressable this way, found during this inspection**: the real controlled conflict experiment that exists today (`ConflictHandlingTest::test_real_controlled_conflict_is_detected`) exercises exactly one of the three real registered Tools — `tool.cross-reference-link-validator-interface`. Neither `tool.document-structure-parser-interface` nor `tool.text-similarity-comparison-interface` has ever been exercised in a real controlled conflict scenario. Running the same technique (real file edit between two real calls) against either of the other two Tools would add real evidence of generalization, using only existing APIs — no contract change required.

**No, the broader coverage gaps cannot be closed this way**: heuristic-sourced conflict detection, cross-Tool/cross-kind matching, and semantic/textual conflict detection are not narrow evidence gaps addressable by running the existing mechanism against new data — they are capability gaps in the mechanism itself, requiring new design (and likely new code) to even begin generating relevant evidence.

---

## Summary

| Question | Answer |
|---|---|
| What is detectable today? | Same-Tool, same-subject-key, boolean-`resolved` disagreement — one narrow class |
| What is undetectable today? | Heuristic conflicts, cross-Tool/cross-kind conflicts, semantic/textual conflicts, unregistered-Tool gaps, Knowledge-layer conflicts entirely |
| Sufficient for Knowledge Admission design? | No — the proven class is narrower than what Knowledge-layer conflicts will plausibly require |
| Can controlled experiments close any gap without a contract change? | Yes, one: extending the existing controlled-experiment technique to the two untested real Tools. Everything broader requires new design, not new evidence. |
