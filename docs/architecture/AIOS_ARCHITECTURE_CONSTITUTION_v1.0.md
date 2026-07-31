# AIOS Execution Layer — Architecture Constitution v1.0

**Status:** Frozen Baseline
**Version:** v1.0
**Scope:** The Execution Layer implementation under `execution/` (Trace, Memory, Human Review, Promotion, Evidence Verification, Tool Execution, Runtime, Governance reading, and the dormant Knowledge prototype).
**Authority:** Subordinate to, and never in conflict with, the ratified `docs/constitution/engineering-constitution-v1.md` and `docs/architecture/domain-model/canonical-domain-model-v1.md`. This document does not restate, redefine, or supersede either — it records, as a permanent reference point, what the Execution Layer's own architecture actually is, as proven by the Architecture Freeze v1.0 certification.
**Approved by:** Architect, Phase 6 — Architecture Baseline Formalization.

This document contains no invented capability. Every statement below is drawn from the repository as it existed at the time of the Architecture Freeze v1.0 certification, evidenced by a passing regression suite (288/288 `execution/tests`, 20/20 `tools/tests`) and a stable real Trace corpus (540 records).

---

## 1. Architecture Identity

The Execution Layer is the concrete, code-level implementation of a subset of the Canonical Domain Model's Execution and Substrate entities: Trace (unconditional, append-only), Memory (derived, provisional), Human Review (the Governance Event/Execution Event split), Promotion (candidate selection for review), Evidence Verification (Tier 2, fail-closed cache trust), Tool Execution, Runtime binding, and governance-document reading. It is explicitly experimental in several of its components (self-disclosed in their own docstrings) and explicitly not a claim that any Domain Model entity is fully, permanently implemented.

## 2. System Purpose

To exercise, with real code against real data, whether the Canonical Domain Model's Execution-layer relationships (Agent Definition → Agent Instance → Trace; Agent Instance → Memory; Memory → governed review → Knowledge) hold operational value and can be implemented without violating the Model's own invariants — before any of it is proposed as a ratified convention.

## 3. Core Principles

1. **Evidence before assumption.** No component in this layer was built ahead of a directive demonstrating the need for it, and no report in this arc classified a capability as proven without a real, reproducible test or a real corpus observation.
2. **Fail closed, not open.** Where a component cannot prove freshness, correctness, or authorization, it refuses rather than guesses (Evidence Verification's fingerprint mismatch handling; Human Review's validation-before-write; Promotion's `"unknown"` source classification when evidence disagrees).
3. **Human governance authority is structurally, not just procedurally, protected.** The Human Review boundary (§9 below) is enforced by static analysis of the code itself, not only by directive.
4. **Small, explicit state over scoring.** Where a lifecycle or trust question arose (Memory Governance's `review_state`/`trust_decision`), the resolution was a small set of explicit states with one override rule, not a weighted or invented scoring system.

## 4. Architectural Invariants

Certified in the Architecture Freeze v1.0 report; restated here as the frozen baseline:

1. Trace is append-only — enforced by `TraceWriter.write()`'s exclusively-append file mode; never violated in real execution (540/540 records).
2. Memory is derived-only, with no stable identity across extraction runs (`memory_id` regenerates via `uuid4()` every call) — a designed property, not a defect, and the reason every consumer of Memory (Human Review, Memory Governance) keys on `(observation_kind, content)` instead.
3. Human Review never computes a decision — proven by AST inspection of `review_decision.py` (no comparison, arithmetic, or ranking against evidence-quality fields), not merely documented.
4. A recorded `HumanReviewDecisionInput.candidate_snapshot` is immutable once written — proven by a real corpus-drift test (a snapshot recorded at T1 remains unchanged when the same underlying data is re-extracted at T2 with different values).
5. Evidence Verification fails closed on an unverifiable cache entry — the one instance in this codebase's history where this invariant was violated in real code (a deleted-file cache entry was incorrectly trusted) was found through dedicated test coverage and repaired under explicit, scoped authorization; the repair is validated end-to-end, not just at the unit level.
6. Promotion and Conflict Detection are both read-only — neither module contains a write path.
7. A real human `reject` decision is an absolute trust override in Memory Governance, regardless of freshness; a real `approve` or `edit` decision never exempts a Memory record from later staleness detection — both proven at full real-corpus scale, not only in a single controlled case.

## 5. Ownership Boundaries

Every module in the Execution Layer owns exactly the data structure it defines, with no shared mutable state between modules:

- `trace.py` owns `TraceRecord` and the on-disk `.jsonl` corpus.
- `memory/extractor.py` owns `MemoryRecord` — computed, never persisted as a governed record.
- `promotion.py` owns `CandidatePackage` — computed from Memory and Trace, written nowhere.
- `review_decision.py` owns `HumanReviewDecisionInput` and is the sole writer of `human_review_decision_recorded` Trace events.
- `memory_governance.py` owns no data at all — it is a pure derivation layer over Memory and Trace, producing labels (`review_state`, `trust_decision`, conflicts) that are never stored.
- `verification.py` and `tool_executor.py` jointly own cache-trust decisions for an externally-supplied, in-process cache; neither owns persistent storage.

No module in this layer reaches into another module's owned data structure to mutate it directly. Cross-module interaction is exclusively through each module's own public functions.

## 6. Source-of-Truth Hierarchy

1. **Trace** is the sole permanent, append-only source of truth for everything that has actually happened — every other structure in this layer (Memory, Promotion candidates, Human Review derivations) is a computed view over Trace, never an independent record of fact.
2. **The real, on-disk Trace corpus** is the only evidence this layer's reports are permitted to cite as "real" — every phase in this arc that produced a report drew its numbers from `load_trace_records()` against the actual corpus, not from memory of prior reports.
3. Where the ratified Constitution or Canonical Domain Model speaks to a question (entity definitions, governance authority, decision-making tiers), those documents are authoritative and this layer's code defers to them; this layer never asserts a competing definition.

## 7. Mutation Rules

- The only mutation this layer performs against permanent state is `TraceWriter.write()` — an append, never an edit or delete.
- `Memory`, `CandidatePackage`, and every Memory Governance derivation are recomputed fresh on every call; "mutation" does not apply to them because nothing is ever held to mutate.
- A `HumanReviewDecisionInput.candidate_snapshot`, once embedded in a written Trace record, is never subsequently altered by any code path — confirmed structurally (frozen dataclass) and behaviorally (corpus-drift test).
- No module outside `trace.py` is permitted to open a Trace file for writing. This is enforced by convention (every write path in this layer routes through `TraceWriter`) and verified by the regression suite's real-corpus mutation checks after every read-only operation.

## 8. Persistence Rules

- Exactly one real, permanent persistence mechanism exists in this layer: the append-only `.jsonl` Trace corpus under `execution/traces/`.
- `memory.MemoryStore` exists as a disposable, explicitly experimental convenience and is used by no governance path — its presence does not constitute a second source of truth.
- No component in this layer persists a Memory record, a Promotion candidate, or a Memory Governance derivation to disk. All are ephemeral, in-process values, recomputed on demand.

## 9. Governance Rules

- Every real Human Review decision (`approve`/`reject`/`edit`) originates exclusively from explicit, human-authored input to `record_decision()`; the module contains no path capable of generating, inferring, or recommending a decision, proven by static analysis, not by policy alone.
- A `reject` decision is an absolute override in downstream trust computation; `approve` and `edit` are not freshness exemptions.
- No automated recommendation, ranking, scoring, or "advisory verdict" of any kind exists anywhere in this layer — every attempt to introduce one during this arc's history was declined and replaced with strictly evidence-only reporting.
- Automation (including this layer's own stop-hook feedback mechanism) may request or recommend; it may never substitute for explicit Architect authorization naming an exact scope, per the ratified Constitution's own invariant on this point.

## 10. Forbidden Behaviors

The following are structurally absent from this layer as of the frozen baseline, and their introduction would constitute a new architectural phase requiring the Evolution Protocol (`AIOS_EVOLUTION_PROTOCOL_v1.0.md`):

- A Knowledge Repository, Knowledge Admission pipeline, or any Knowledge persistence/promotion mechanism.
- Conflict resolution logic of any kind (detection exists; resolution does not).
- Any automated or autonomous decision-making, learning, self-modification, retrieval optimization, or reflection capability.
- Any code path in Human Review capable of computing, inferring, or suggesting a governance decision.
- Any mutation of a written Trace record, or any persistence mechanism outside `TraceWriter`.
