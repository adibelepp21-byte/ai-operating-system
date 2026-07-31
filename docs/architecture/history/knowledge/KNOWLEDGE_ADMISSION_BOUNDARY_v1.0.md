# Knowledge Architecture Discovery — Admission Boundary v1.0

**Status:** Design analysis only. No admission mechanism is implemented by this document.
**Version:** v1.0
**Authority:** Subordinate to the ratified Constitution's Decision-Making Process (§3) and the Canonical Domain Model's invariant 8. This document analyzes the admission boundary using only real repository evidence and the ratified governance text; it decides nothing new.
**Approved by:** Architect, Phase 7 — Knowledge Architecture Discovery.

---

## Who Creates Knowledge?

**Known**: nothing in this repository currently creates a Knowledge entity — confirmed structurally (`NegativeSafetyTest.test_cannot_write_knowledge_records` proves no Knowledge Repository module exists anywhere in the codebase) and behaviorally (zero real Knowledge entities exist, `knowledge_consumed` is empty on all 540 real Trace records).

**Known**: the *candidate* that would precede any Knowledge entity is created by `promotion.select_candidates()` — a pure, read-only function over Memory and Trace, never a write.

**Requires future contract decision**: whether "creation" of a Knowledge entity is an automatic consequence of a governed decision (e.g., `approve`), or requires a distinct write step with its own actor and authority. No evidence favors either — see `KNOWLEDGE_LIFECYCLE_DISCOVERY_v1.0.md` Stage 3.

## Who Approves?

**Known**: every real governance decision this system has ever recorded came from a human, never generated or inferred by code — proven by AST inspection of `review_decision.py` across every phase this arc, not merely policy. The one real reviewer identity on record (`MoriartyTalk`) has exercised all three decision types.

**Unknown**: whether Knowledge admission requires the same authority tier as candidate review, or a higher one. The ratified Constitution's Decision-Making Process (§3) distinguishes Constitutional, Architectural, and Implementation tiers for *governance document* decisions — whether Knowledge admission maps onto one of these tiers, or needs its own, has never been evaluated against real evidence, because no real Knowledge admission has ever occurred.

**Requires future contract decision**: whether a Department (once resolved — see Concept Analysis §4) must approve Knowledge admission for items in its own domain, consistent with Domain Model §5's Department-ownership language.

## What Evidence Is Required?

**Known, evidence-backed**: a `CandidatePackage` already carries content, full provenance (memory_id, trace_ids, agent_definition_name), and an evidence summary (source_type, confidence, occurrence_count, resolved, fingerprint) — real, tested, complete for every real review this arc conducted.

**Known, from real Human Review rationale patterns**: reviewers, when approving, have explicitly distinguished "this evidence package is fit to retain as a governance record" from "this content's truth has been independently verified" (real rationale text, e.g. the original pilot's evidence-sufficiency framing, and every subsequent approval's disclaimers about not claiming external verification). This suggests Knowledge admission evidence requirements may need to be stricter than candidate-review evidence requirements, but this is an observation about reviewer language, not a specified requirement.

**Unknown**: what evidence threshold (if any) beyond what `CandidatePackage` already carries would be required specifically for admission into durable, canonical Knowledge, as opposed to retention as a reviewed governance record. No real admission has ever occurred to calibrate this against.

## How Does Human Review Interact?

**Known, real, and load-bearing**: the existing Human Review contract already proves the mechanics work — validation-before-write, immutable snapshot capture, structural impossibility of an automated decision, all real and exercised 6 times across all 3 decision types.

**Known**: the contract's `decision` field is a closed 3-value enum (`approve`/`reject`/`edit`) with no room for a 4th, Knowledge-specific outcome without a contract change — explicitly forbidden in every phase of this arc so far.

**Requires future contract decision**: whether Knowledge admission is a new *meaning* attached to an existing `approve` (Option A in the Lifecycle Discovery document), or a wholly new decision type requiring a Human Review contract extension. Extending the contract is itself subject to the Evolution Protocol's Contract Review step (`AIOS_EVOLUTION_PROTOCOL_v1.0.md` §4) and has not been authorized by any directive in this arc.

## How Should Conflicts Eventually Be Handled?

**Known**: `memory_governance.detect_conflicts()` proves conflict *detection* is technically sound — validated against a real, controlled scenario (two real Tool calls against a genuinely edited file, correctly flagged as disagreeing). **Known**: zero organic (uncontrolled) conflicts have occurred in real data across four independent scans this arc.

**Known, explicitly out of scope so far**: conflict *resolution* has never been designed. The Memory Governance Hardening phase explicitly investigated "what happens after conflict detection" as a design-boundary-only exercise and built nothing.

**Requires future contract decision**: whether a Knowledge-layer conflict is resolved *before* admission (i.e., conflicting candidates must be reconciled at the Memory/Promotion layer, and only non-conflicting content ever reaches Knowledge admission) or *after* (i.e., two Knowledge entities can coexist in a declared-conflicting state, requiring their own resolution decision type). No evidence favors either, and — critically — no real conflict has ever existed to observe which approach a real reviewer would find natural.

---

## Summary

| Question | Known | Unknown | Requires future contract decision |
|---|---|---|---|
| Who creates? | Candidates are created by `promotion.py`; no Knowledge entity is ever created today | — | Whether creation is automatic-on-approve or a distinct step |
| Who approves? | Every decision is human-authored, structurally proven | Whether admission needs a different authority tier than candidate review | Department-scoped approval, once Department resolution exists |
| What evidence? | `CandidatePackage`'s existing evidence summary is real and complete for candidate review | Whether admission needs a stricter threshold | — |
| Human Review interaction? | The existing contract's mechanics are proven and reusable | — | Whether admission reuses `approve` or needs a new decision type |
| Conflict handling? | Detection is proven; zero organic conflicts exist to learn from | What a real reviewer would want when conflicts occur | Resolve-before-admission vs. resolve-after-admission |
