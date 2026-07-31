# AIOS Principles Register v1.0

**Status:** Canonical home for AIOS architectural principles — the Principle layer identified as missing by the Canonical Architecture Review. Architecture governance document; no code, schema, API, or implementation.
**Version:** v1.0
**Authority:** Subordinate to the ratified Constitution and Canonical Domain Model. This Register does not outrank a Domain Model invariant or a Constitutional rule — where a rule is already an invariant (e.g. immutable Trace, human-governed promotion), it stays an invariant and is *not* duplicated here. A Principle is a cross-subsystem architectural rule that is not itself a ratified invariant but has been independently rediscovered enough times, and is stable enough, to bind future design.
**Confidence discipline:** **[E]** evidence-backed · **[A]** assumption · **[O]** open question.

---

## What Qualifies as an AIOS Principle

A candidate must meet **all five** criteria (the threshold established across the prior reviews):

1. **Independently rediscovered** — applied in ≥2 contexts that did not derive from one another.
2. **Evidenced from real AIOS evolution** — occurrences are real code, real tests, or ratified decisions, not proposals.
3. **No contradiction with the Canonical Domain Model.**
4. **No conflict with Blueprint v3.**
5. **General beyond the Knowledge subsystem.**

A rule that is already a Domain Model invariant is **not** a Principle here — it already binds at a higher layer. This is why "immutable/append-only history" and "human-governed promotion" appear in the relationships of the principles below but are not themselves registered: they are invariants 5 and 8.

---

## Registered Principles

### PR-1 — Evidence First

- **Definition:** No architecture, mechanism, or decision is produced ahead of demonstrated need or observed fact; every claim carries its evidence status.
- **Intent:** Prevent speculative structure that encodes assumptions later contradicted by real data at high unwind cost.
- **Rationale:** The cheapest place to be wrong is before building; this principle forces wrongness to surface as an open question rather than as shipped structure.
- **Evidence [E]:** The fingerprint generational-absence fix (real corpus overturned a design assumption); the 8-state lifecycle collapsed to 2 states + conditions; every "NOT READY" verdict that refused to fabricate readiness; the Constitution's own stated philosophy.
- **Independent occurrences [E]:** (1) Execution Layer evidence-gating across every tier; (2) the Knowledge readiness assessments; (3) the pattern-extraction discipline (declining to invent patterns). Three independent contexts.
- **Scope:** All AIOS design and decision work.
- **Non-applicable cases:** None identified — it governs process, not a subsystem, so it has no structural exception. [A] The one tension is time pressure, which is a governance choice, not an exception to the principle.
- **Relationship to patterns:** Was catalogued as P1; this Register is its correct home. P12 (Explicit Deferred Decisions) and P14 (Readiness with Evidence) are its documentation-discipline expressions.
- **Relationship to Domain Model:** Consistent with the Model's own "conceptual domain only, projections not extensions" discipline (§8).
- **Relationship to Blueprint v3:** Blueprint v3's large open-question registers and its refusal to design Retrieval policy are direct applications.
- **Architectural consequences:** Slower apparent progress; large open-question registers; honest readiness verdicts.
- **Known tradeoffs:** More documents per decision; requires discipline against plausible assumption-filling.
- **Confidence:** [E] High.
- **Open questions:** None.

### PR-2 — State/Condition Separation

- **Definition:** Lifecycle position (where a record sits in its history) and evaluation (what the system currently holds about it) are independent axes; an epistemic condition must never be encoded as a lifecycle state.
- **Intent:** Prevent state-machine explosion and the semantic dishonesty of a single flat status conflating "is current" with "is trustworthy."
- **Rationale:** These two questions have genuinely independent answers (a Superseded version may have been valid; an Active version may be Invalidated); collapsing them forces one answer to lie.
- **Evidence [E]:** Architect Decision 4 (conflict = condition, not a state); the validity model (Confirmed/Questioned/Invalidated as conditions orthogonal to Active/Superseded); the real precedents `evaluate_relevance()` (labels without mutating position) and `detect_conflicts()` (flags without transitioning).
- **Independent occurrences [E]:** (1) conflict handling; (2) validity/retraction; (3) Memory relevance labelling in real code — three independent applications, two of them predating the principle's naming.
- **Scope:** Any AIOS entity that has both a history and an evaluation.
- **Non-applicable cases [E]:** Entities with no evaluation dimension (a pure event like a Trace record has only position, no condition) — the principle is vacuously satisfied, not violated.
- **Relationship to patterns:** Was catalogued as P4; this is its correct home.
- **Relationship to Domain Model:** Extends, without contradicting, the Model's lifecycle rules (§6) by clarifying what a lifecycle state may and may not encode.
- **Relationship to Blueprint v3:** The foundation of §2.2/§2.3's two-axis model; already named as a principle in Blueprint v3 §3 — this Register relocates that naming to its correct layer.
- **Architectural consequences:** Consumers read two axes; minimal state sets become achievable.
- **Known tradeoffs:** Higher conceptual load for consumers, accepted deliberately.
- **Confidence:** [E] High.
- **Open questions:** None (the Questioned-effect timing is a Blueprint-v3 open question, not a principle-level one).

### PR-3 — Detect, Don't Decide

- **Definition:** Automation may find, flag, verify, and surface; only governed human review may make or change a governance decision.
- **Intent:** Hold the line between helpful automation and automated governance, which Constitution §6.2 invariant 2 forbids.
- **Rationale:** Detection and decision are separable; keeping them separate preserves human authority without sacrificing automated assistance.
- **Evidence [E]:** `detect_conflicts()` returns conflicts and resolves none; Tier 2 verification invalidates a *cache entry* (execution concern) but never a governance judgment; the Questioned condition (automation proposes, humans set); the declined Phase-7 "AI Recommendation."
- **Independent occurrences [E]:** Four — conflict detection, evidence verification, the validity-proposal design, and the recommendation-refusal precedent — spanning Execution and Knowledge subsystems.
- **Scope:** Every AIOS surface containing automated evaluation feeding a governance decision.
- **Non-applicable cases [E]:** Purely-execution decisions with no governance content (e.g. a cache invalidation, which Tier 2 *does* perform automatically) — these are not governance decisions and the principle does not restrict them. The boundary is "governance decision," precisely.
- **Relationship to patterns:** Was catalogued as P9.
- **Relationship to Domain Model:** Directly serves invariant 8 ("never automatically") and the human-authority spirit throughout.
- **Relationship to Blueprint v3:** The design basis for automation proposing (never setting) validity conditions.
- **Architectural consequences:** Every detector needs a paired human pathway or its findings accumulate (the "Questioned parking-state" risk).
- **Known tradeoffs:** Structural latency between detection and action.
- **Confidence:** [E] High.
- **Open questions:** None.

### PR-4 — Fail Closed

- **Definition:** When freshness, correctness, or authorization cannot be positively proven, refuse rather than guess.
- **Intent:** Prevent silent trust of unverifiable data or unproven authority.
- **Rationale:** An honest "unknown/refused" is recoverable; a silent wrong "yes" is not.
- **Evidence [E]:** `verification.py` (missing fingerprint fails verification — and the one real violation, the deleted-file fail-open, was fixed *to conform*, confirming the principle rather than contradicting it); ambiguous source → `"unknown"`; unresolvable department → `"unavailable"`; malformed decision → raises before any write.
- **Independent occurrences [E]:** Four — verification, promotion source-classification, department-status, decision validation — and a fifth as the corrective direction of a real repaired bug.
- **Scope:** Everywhere trust or authorization is computed.
- **Non-applicable cases [A]:** Contexts where a safe default genuinely exists and is documented (e.g. an empty flag list is a real "no flags," not a refusal) — the principle applies to *unprovable* states, not to legitimately-empty ones. The distinction was itself the subject of a real test false-positive that was corrected (`review_flags is None` vs. `== []`).
- **Relationship to patterns:** Was catalogued as P10.
- **Relationship to Domain Model:** Reinforces auditability (§6) — a refusal is explainable; a silent guess is not.
- **Relationship to Blueprint v3:** Underlies the validity model's refusal to auto-confirm and the admission contract's validate-before-write.
- **Architectural consequences:** More refusals and live re-executions; honest "unknown" values propagate.
- **Known tradeoffs:** Extra work when a fast path can't be proven safe.
- **Confidence:** [E] High.
- **Open questions:** None.

### PR-5 — Capture, Don't Reference

- **Definition:** A decision or durable record embeds the full content it depended on at the moment it was made, never a live pointer to something recomputable or mutable.
- **Intent:** Guarantee that a record's meaning cannot silently change when its referent later changes.
- **Rationale:** Explainability that depends on another entity's continued, unchanged existence is not durable explainability.
- **Evidence [E]:** Domain Model §6.1 (Trace captures referenced content at write time); `candidate_snapshot` across 6 real events; the real T1→T2 corpus-drift test proving a recorded decision is immune to later recomputation; Blueprint v3's provenance model (source Memory captured as a snapshot, never a live reference).
- **Independent occurrences [E]:** Three — the Trace/Memory relationship (ratified at DM level), Human Review snapshots, and the Blueprint v3 Knowledge provenance design.
- **Scope:** Any durable record that references volatile or recomputable data.
- **Non-applicable cases [E]:** References to genuinely immutable targets (one Trace record citing another by ID) — the referent cannot change, so a reference is safe; capture would be redundant. This is exactly why Trace-to-Trace references are IDs while Trace-to-Memory content is captured.
- **Relationship to patterns:** Was catalogued as P7.
- **Relationship to Domain Model:** Elevates §6.1 (stated for Trace) to a general principle, consistent with it.
- **Relationship to Blueprint v3:** The basis of the snapshot requirement across admission/revision/invalidation records.
- **Architectural consequences:** Larger records; the snapshot is the authoritative account of what was judged.
- **Known tradeoffs:** Storage duplication; snapshot field-set needs per-use design (Blueprint v3 open question #4).
- **Confidence:** [E] High.
- **Open questions:** None at principle level.

---

## Candidate (Not Promoted)

### Signals Prioritize, Never Gate

- **Definition:** Computed quality signals may order human attention; they may never determine eligibility or outcome.
- **Status: Keep Candidate.** [A] Two real occurrences (`promotion.py` ranking-vs-eligibility; the rejection of confidence-decided conflicts), but both are promotion-adjacent — they do not yet demonstrate the *subsystem-independent* rediscovery the threshold requires. Remains Pattern P13. Promote when a third, non-promotion occurrence appears.
- **Confidence:** [A] Medium.

---

## Non-Promotions (Explicitly Declined)

- **Immutable/Append-Only History** — already Domain Model invariant 5; registering it here would create duplicate authority. Not promoted.
- **Human-Governed Promotion** — already Domain Model invariant 8; patterns P3/P9 are its mechanism. Not promoted.
- **Explicit Deferred Decisions / Readiness with Evidence** — documentation disciplines (Quality Checklist items 14/17), not structural principles. Remain patterns/gates.

---

No document was modified to create this Register (cross-reference updates to Blueprint v3 §3 and the Pattern Catalog are *recommended* in the companion Governance Review, not performed here). No code, schema, or implementation. Awaiting Architect authorization for the cross-reference updates.
