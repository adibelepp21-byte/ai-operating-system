# Knowledge Architecture Blueprint v3 (Canonical Draft)

**Status:** Canonical Draft — the single architectural source of truth for the AIOS Knowledge subsystem, pending final Architect ratification.
**Version:** v3.0
**Authority:** Subordinate to the ratified Engineering Constitution and Canonical Domain Model. Supersedes, as the consolidated reference, the design content of the twenty-one prior Knowledge documents under `docs/knowledge/` — those documents remain permanently retained as the audit trail of how each decision was reached (per this system's own append-only philosophy), but this Blueprint is now the document to consult for what the Knowledge architecture *is*.
**Approved by:** Architect (consolidation directive); individual decisions carry their own prior authorizations, cited per section.

**Source-naming note (honesty requirement):** the consolidation directive refers to "Knowledge Assessment," "Knowledge Blueprint v1," "Blueprint Validation Report," and "Knowledge Blueprint v2." No documents exist under those exact titles. The real corpus consolidated here comprises: the Phase 7 discovery documents (Concept Analysis, Entity Proposal, Lifecycle Discovery, Admission Boundary, Architecture Readiness — collectively the functional "Blueprint v1"), the Phase 8 governance contract documents (Governance Principles, Admission Contract, Lifecycle Contract, Ownership Model, Conflict Governance — functionally "Blueprint v2"), the evidence-closure and readiness reports (functionally the "Validation Report"), the two Architect Decision Packages/Reviews, the Consistency Review, and the Lifecycle & Conflict Authorization record. Nothing was invented to fill the naming gap.

---

## 1. Executive Summary

The Knowledge subsystem is defined by six settled architectural decisions and one newly elevated AIOS Architectural Principle. Knowledge is a durable, versioned, human-governed Substrate entity: each **version** is an immutable, separately addressable record; the **identity** is a stable correlation key, not a stored parent entity (mirroring the proven Trace ↔ Agent Instance pattern). **Lifecycle position** (Active / Superseded) and **Validity** (Confirmed / Questioned / Invalidated) are orthogonal dimensions — the former records historical position, the latter records epistemic evaluation, and conflating them is now expressly forbidden as an architectural principle. Retraction is a validity event, never a lifecycle state and never a deletion. Every admission, revision, and invalidation requires explicit governed human review. A complete consistency review against every adjacent architecture (Section 8) found **no contradictions** in the consolidated design and two genuine open items, both already tracked, neither newly created by consolidation.

---

## 2. Consolidated Blueprint v3

### 2.1 Entity Model

- **Knowledge Version** — the only stored Knowledge record. Immutable, separately addressable, permanent. Created exclusively through a governed admission or revision decision. Carries: content; full provenance (per §2.5); its identity correlation key; its lifecycle position; its validity condition history (by reference to the decision records that produced it).
- **Knowledge Identity** — a stable logical correlation key shared by every version of one piece of Knowledge. **Not a stored parent entity.** All identity-level facts (current active version, validity, ownership) are derived at read time from the version records sharing the key — exactly the proven pattern by which Agent Instance exists only through the Trace records carrying its `instance_id` (per `agent_instance.py`'s own real design) and by which `review_state()` already derives review status from multiple correlated decision records. *(Decision 1 — settled; do not reopen.)*

### 2.2 Lifecycle Model (position dimension)

Two states only, per prior authorization, reconfirmed:

- **Active** — the current version of its identity.
- **Superseded** — a version replaced by a newer version of the same identity.

Revision creates a new immutable version (the new Active); the prior version becomes Superseded. Nothing is ever modified in place; nothing is ever deleted. *(Decisions 2 and 4 — settled.)*

**Supersession ≠ conflict** (settled in the prior authorization): supersession is intra-identity (controlled change of the same Knowledge); conflict is inter-identity (different Knowledge items with contradicting claims). No shared mechanism.

### 2.3 Validity Model (epistemic dimension)

Orthogonal to lifecycle position. Three conditions *(Architect refinement — supersedes the earlier binary Valid/Invalid proposal)*:

- **Confirmed** — the default condition of an admitted version: governed review found the evidence package sufficient at admission time.
- **Questioned** — an intermediate, explicitly held condition: real evidence has surfaced that challenges this version, but no governed determination has yet been made.
- **Invalidated** — an evidence-backed, human-decided determination that this specific version is no longer trustworthy.

**Why Questioned is necessary:** without it, the model forces a false dichotomy at exactly the moment AIOS is most likely to be operating — the interval between evidence arriving and a human deciding. This system's entire real history shows that interval is where its architecture does its most important work: Tier 2 verification *flags* a stale cache entry before anything acts; `detect_conflicts()` *surfaces* disagreement without resolving it; conflict was ratified as "a condition resulting from evaluation," not an instant verdict. A binary Valid/Invalid model would compel either premature invalidation (an automated or hasty epistemic demotion — violating the human-authority principle) or silent continuation as fully Confirmed (hiding a live doubt — violating explainability). Questioned is the honest, architecturally consistent name for "a human decision is now required but has not yet occurred." It is the validity-dimension counterpart of the already-approved conflict condition, not a new kind of concept.

Validity transitions (Confirmed → Questioned, Questioned → Invalidated, Questioned → Confirmed) are each explicit governed events producing their own Trace records. Automated processes may *propose* Questioned (evidence detection); only governed human review may *set* any validity condition. *(Decisions 3, 5, 6 — settled.)*

### 2.4 Retraction

Retraction of wrongly admitted Knowledge with no replacement = the Active version's validity becoming **Invalidated** while its lifecycle position remains Active (no successor exists to supersede it). History is never deleted; auditability is fully preserved; no third lifecycle state exists. *(Decision 3 — settled.)*

### 2.5 Provenance Model (consolidated, unchanged from prior approvals)

Permanent, immutable per version: Originating Department (historical fact), Reviewing Actor of every decision touching it, the Admission/Revision/Invalidation decision Trace records, the Source Memory snapshot (captured content, never a live reference — Memory identity is deliberately unstable), and Supporting Trace references. Reassignable: **Home Department only**, and only via a new explicit reviewed record that permanently preserves every prior assignment.

### 2.6 Ownership & Authority Model (consolidated)

- Knowledge remains a cross-cutting Substrate entity, addressable from all of AIOS, never any Department's private property (Domain Model §8, reconciled explicitly in the prior authorization).
- **Home Department** = accountability point, curator, first responder for maintenance and conflict handling. Grants no exclusive access, no restriction authority, no out-of-lifecycle change authority.
- **Invalidation authority** *(Architect refinement, integrated)*: invalidation is decided by a **Human Reviewer acting under Home Department authority**. This aligns with the Canonical Domain Model on three grounds: (1) §5's home-Department accountability makes the Home Department the natural locus of answerability for a validity determination about its item; (2) §8's cross-cutting access is untouched — invalidation authority governs who may *decide*, not who may *read*; (3) invariant 8's governed-review requirement is satisfied because the decision is made by a human through review, with the Department framing supplying *whose accountability* the human acts under — the same reviewer-acts-under-authority structure the entire Human Review contract already embodies (a reviewer decides; the decision is accountable, attributed, and permanent). Reviewer ≠ owner remains in force: exercising invalidation authority does not confer ownership.
- Admission and revision authority: explicit governed human review, per the approved Admission Model (a separate admission decision layered on the proven Human Review infrastructure — Option B, settled).

### 2.7 Conflict vs. Invalidity (Architect refinement, integrated)

Two distinct concepts; never merged:

- **Conflict** = competing Knowledge (different identities) whose disagreement lacks sufficient evidence to resolve. Both items retain their own lifecycle positions and validity conditions; the conflict is preserved and surfaced, never silently resolved. Resolution, when evidence suffices, is a governed human decision. Cross-Department escalation authority remains explicitly deferred (invariant-10 analogy rejected — settled).
- **Invalidity** = an evidence-backed governed determination that one *specific version* is no longer trustworthy. It involves no second Knowledge item and no unresolved disagreement — it is a settled epistemic judgment about one record.

A conflict may *lead to* one party's invalidation once evidence suffices — but the conflict (the unresolved coexistence) and the invalidation (the resolved determination) remain different events with different records.

### 2.8 Retrieval Consequence (documented, not designed)

Retrieval now evaluates **two independent dimensions per version: lifecycle position and validity**. This is stated as an architectural consequence only. Default visibility policy — whether Superseded versions, Questioned versions, or Invalidated versions appear in results, and how — remains **explicitly open**, per the directive.

### 2.9 Admission & Promotion (consolidated, unchanged)

Memory → Candidate (`promotion.select_candidates()`, real and proven) → candidate Human Review (existing contract, unchanged) → separate Knowledge admission decision (Option B) → first version of a new identity, Active, Confirmed. Confidence/frequency inform prioritization only, never eligibility or outcome — the real, unmodified `promotion.py` pattern. Promotion remains structurally uncoupled from Knowledge (verified against the real import graph in the Consistency Review).

---

## 3. Architectural Principles Introduced by v3

**AIOS Architectural Principle — State/Condition Separation** *(elevated per Decision 6)*:

> **State describes lifecycle position. Condition describes evaluation. Epistemic conditions must never be encoded as lifecycle states.**

Grounding: this principle was applied twice independently before being named — first for conflict (ratified: "a condition resulting from evaluation, not a lifecycle state"), then for validity (this consolidation). Both applications trace to the same real precedent: this system's proven mechanisms (Tier 2 verification, `detect_conflicts()`, `evaluate_relevance()`) all *evaluate* without ever mutating the position of the thing evaluated. The principle generalizes what the codebase already does. It binds all future AIOS subsystem design, not only Knowledge.

Supporting principles carried into v3 (not new, consolidated): immutable history (append-only, no in-place change, no deletion); human authority over every governance transition; evidence-first (no mechanism built ahead of demonstrated need — reflected in the two-state lifecycle and the explicitly open items below); explainability (every transition is a permanent, attributed, citable record).

---

## 4. Decision Log (accepted decisions only)

| # | Decision | Status |
|---|---|---|
| 1 | Knowledge Version = immutable, separately addressable record; Identity = stable correlation key, not a stored parent entity (Trace ↔ Agent Instance pattern) | Settled |
| 2 | Lifecycle position (Active/Superseded) and Validity are orthogonal; validity is never a lifecycle state | Settled |
| 3 | Retraction is a validity event (Invalidated), never a lifecycle state, never a deletion, always auditable | Settled |
| 4 | Repository is append-only and versioned; revision creates a new immutable version; nothing modified in place | Settled |
| 5 | Human authority mandatory for admission, revision, and invalidation — explicit governed review, no exceptions | Settled |
| 6 | State/Condition Separation elevated to an explicit AIOS Architectural Principle | Settled |
| 7 | Validity model = Confirmed / Questioned / Invalidated (supersedes binary Valid/Invalid) | Settled (this consolidation) |
| 8 | Invalidation authority = Human Reviewer acting under Home Department authority | Settled (this consolidation, recommended direction integrated) |
| 9 | Conflict ≠ Invalidity; never merged | Settled (this consolidation) |
| 10 | Admission Model = separate admission decision on Human Review infrastructure (Option B) | Settled (prior authorization) |
| 11 | Ownership = Home Department as accountability/curation only; Knowledge remains cross-cutting per DM §8 | Settled (prior authorization) |
| 12 | Supersession ≠ conflict; intra-identity vs. inter-identity | Settled (prior authorization) |
| 13 | Invariant-10 analogy for cross-Department escalation rejected; escalation model deferred | Settled as rejected/deferred (prior authorization) |
| 14 | Archived is not a lifecycle state in v1 | Settled (prior authorization) |

---

## 5. Remaining Open Questions

Carried forward, none resolved by consolidation (consolidation resolves presentation, not evidence gaps):

1. **Revision Required trigger** — what precisely moves a version to Questioned / flags revision. [O]
2. **Conflict evidence threshold** — what suffices to resolve a conflict. [O]
3. **Cross-Department escalation authority** — deferred by explicit decision. [O]
4. **Snapshot mechanics** — field-level detail (principle settled: capture, never reference). [O]
5. **Revision signal vs. executed revision boundary.** [O]
6. **Retrieval default visibility policy** across the two dimensions — explicitly left open by this directive. [O]
7. **Conflict carry-forward across revision** — does a conflict condition on a version transfer to its successor automatically or require re-evaluation? (Surfaced in the prior decision review; unresolved.) [O]
8. **Questioned-condition authority detail** — automated detection may *propose* Questioned, but whether the Questioned condition takes effect only upon human confirmation, or provisionally upon detection pending confirmation, is a genuine sub-question of #1 not settled by the validity model itself. [O — newly stated precisely by this consolidation; previously implicit inside #1.]

---

## 6. Updated Dependency Readiness Matrix

| Area | Status | Basis |
|---|---|---|
| Admission Architecture | **READY for implementation planning** | Model settled (Option B); mechanics reuse the fully proven Human Review infrastructure; no architectural unknown remains in the admission path itself |
| Ownership Architecture | **READY for implementation planning** | Interpretation fully settled including invalidation authority; open item #3 (escalation) is explicitly deferred, not blocking |
| Lifecycle Architecture | **PARTIALLY READY** | States and versioning settled; blocked only on open question #1 (Revision trigger) for full operation |
| Validity Architecture | **PARTIALLY READY** | Model settled (three conditions); blocked on #1/#8 for transition mechanics |
| Conflict Architecture | **PARTIALLY READY** | Philosophy and conflict/invalidity distinction settled; #2, #3, #7 open |
| Repository Architecture | **READY for implementation planning** | The version-addressing blocker is resolved (Decision 1); append-only model settled; data-model design is now implementation-tier work |
| Retrieval Architecture | **PARTIALLY READY** | Two-dimension consequence documented; blocked on #6 (visibility policy) before implementation |
| Promotion Architecture | **READY** | Real, proven, unchanged, structurally uncoupled — unchanged since first assessed |

---

## 7. Updated Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Two-axis complexity (position × validity) confusing consumers/implementers | Medium | Medium | The State/Condition Separation Principle (Section 3) exists precisely to police this; every future design review checks against it |
| Questioned condition becoming a permanent parking state (never resolved to Confirmed/Invalidated) | Medium | Medium | Open question #1/#8 must define resolution expectations; flagged so the trigger design addresses dwell-time explicitly |
| Trace event-shape proliferation (admission, revision, invalidation, validity transitions, ownership reassignment) | Medium | Low-Medium | Reuse the proven collision-proofing test discipline (`test_human_review_shape_never_collides...`) for every new event shape |
| Conflict/invalidity conflation by future implementers despite the documented distinction | Low-Medium | Medium | Section 2.7's explicit never-merge rule; distinct decision records by design |
| Cross-Department escalation vacuum when the first real cross-Department conflict occurs | Low (near-term — zero real conflicts ever) / High (eventually) | Medium | Explicitly tracked deferral; do not improvise if it occurs — return to Architect |
| Implementation drifting into treating Identity as a stored entity | Low | High | Decision 1's do-not-reopen status; the Trace ↔ Agent Instance precedent is cited directly in this Blueprint as the reference pattern |

---

## 8. Complete Architecture Consistency Review

Checked, as one integrated system, against: Canonical Domain Model, Constitution, the Phase 8 contract documents (functional "Blueprint v2"), the evidence-closure/readiness reports (functional "Validation Report"), the Architect Decision Review, Execution architecture, Memory architecture, Trace architecture, the Ownership Model, Lifecycle Model, Promotion Model, Provenance Model, and Authorization Model.

- **Contradictions**: **none found.** The two previously identified tensions (Home Department vs. DM §8; invariant-10 scope) were both resolved by explicit prior Architect decisions and their resolutions are consistently reflected throughout this Blueprint. The validity refinement (three conditions) introduces no conflict with any settled decision — it slots into the orthogonal dimension Decision 2 already reserved.
- **Duplicated concepts**: none remaining in this Blueprint. The prior corpus contained deliberate overlaps (Discovery vs. Contract documents covering lifecycle twice); v3 consolidates them; the older documents remain as audit trail, not as competing authority.
- **Hidden assumptions**: one found and surfaced as open question #8 (whether Questioned takes effect on detection or on human confirmation) — previously implicit, now explicit. No others found.
- **Circular dependencies**: none. The dependency direction remains strictly Memory → Candidate → Review → Knowledge, with Promotion confirmed structurally uncoupled from Knowledge (real import-graph evidence, carried from the Consistency Review).
- **Architectural drift**: none detected — every element of this Blueprint traces to an explicit prior decision or to this directive's refinements; nothing entered by accretion.
- **Terminology inconsistencies**: one corrected during consolidation — prior documents used "Retracted/Invalidated," "validity status," and "invalidity condition" loosely; v3 fixes the vocabulary: **state** = lifecycle position only (Active/Superseded); **condition** = validity only (Confirmed/Questioned/Invalidated); "retraction" is the *event*, "Invalidated" is the resulting *condition*. No other inconsistencies found.

No problems were invented to produce findings; the review genuinely found the design coherent.

---

## 9. Migration Impact — Blueprint v2 → v3

Because no Knowledge implementation or data exists (zero Knowledge entities, `knowledge_consumed` empty on all real Trace records — verified repeatedly), **migration impact is documentation-only. No data migration exists or is needed.** The conceptual deltas from the functional "Blueprint v2" (Phase 8 corpus) to v3:

1. Binary Valid/Invalid → **Confirmed/Questioned/Invalidated** (refinement, additive).
2. Version addressing settled (was the open blocker gating Repository work).
3. Retraction settled as a validity event (was a state-set scope gap).
4. Invalidation authority settled (was open).
5. State/Condition Separation elevated from an implicit practice to a named Principle.
6. Eight-state lifecycle exploration collapsed to the ratified two states + orthogonal conditions.

Nothing in v3 invalidates any recorded real data or any prior decision — v3 narrows and settles; it does not reverse.

---

## 10. Final Architect Recommendation

Blueprint v3 is internally consistent, fully traceable to explicit decisions, and contains no unresolved contradiction. Three areas are now **READY for implementation planning** (Admission, Ownership, Repository — the last unblocked by Decision 1), and Promotion remains READY. The recommended sequence for what follows, pending Architect authorization: (1) ratify this Blueprint as canonical; (2) resolve open question #1 (Revision/Questioned trigger — the highest-leverage remaining unknown, blocking both Lifecycle and Validity operation); (3) only then authorize Repository implementation planning, which now has a settled architectural foundation to design against. No implementation is recommended or authorized by this document.

---

No code was written; no file outside `docs/knowledge/` was touched; no schema, API, or storage design was produced. Stopping here. Awaiting Architect authorization.
