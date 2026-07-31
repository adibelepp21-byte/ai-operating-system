# Architect Decision Review — AIOS Knowledge Layer v1.0

**Status:** Decision recommendation only. No implementation, contract, schema, or governance-document change occurs here. Awaiting Architect authorization before any action follows from this review.
**Version:** v1.0
**Authority:** Subordinate to the ratified Canonical Domain Model and Constitution. Evaluates `ARCHITECT_DECISION_PACKAGE_v1.0.md`'s two open decisions using real repository evidence.
**Sources used**: `docs/architecture/domain-model/canonical-domain-model-v1.md`; the ten Phase 7/8 Knowledge design documents; `docs/knowledge/ARCHITECT_DECISION_PACKAGE_v1.0.md`; `docs/knowledge/KNOWLEDGE_ADMISSION_BLOCKER_REGISTER_v1.0.md`; `docs/knowledge/CONFLICT_DETECTION_READINESS_v1.0.md`; `docs/knowledge/MULTI_DECISION_READINESS_ASSESSMENT_v1.0.md`; real code (`review_decision.py`, `promotion.py`, `memory_governance.py`); the real Trace corpus (540 records, 6 real Human Review decisions).
**Note on scope**: the directive references an "Existing Knowledge Architecture Blueprint v2." No document by this name or description exists anywhere in the repository (searched directly). This review does not use it and does not invent its content — flagged here per this arc's standing practice of reporting contradictions before acting on them.
**Evidence tags**: **[E]** evidence-backed, **[A]** assumption requiring validation, **[O]** open/unknown.

---

## 1. Architect Decision Summary

Two decisions are reviewed: the Knowledge Admission Model and the Knowledge Ownership Model. Both were left unresolved in `ARCHITECT_DECISION_PACKAGE_v1.0.md` with `STATUS: ARCHITECT DECISION REQUIRED`. This review evaluates each against real evidence and issues a recommendation for each — but a recommendation is not an authorization. No code, contract, or schema changes occur as a result of this document; both remain pending explicit Architect approval.

---

## 2. Knowledge Admission Model — Full Review

### Restated Architectural Problem

Domain Model invariant 8 requires Memory be promoted to Knowledge "only through governed review — never automatically." The Human Review contract (`review_decision.py`) already implements governed review for *candidates* — but nothing in this system today defines what act constitutes admission specifically *into Knowledge*, as distinct from a candidate simply being marked `approve`.

### Options (restated from the Decision Package)

**A — Approve = Admission.** **B — Separate Knowledge Admission Decision.** **C — Hybrid Admission Gate.**

### Evaluation Against Criteria

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Domain Model compatibility | [E] Satisfies invariant 8's literal text (a human decision occurs) but risks reinterpreting real `approve` events beyond their evidenced meaning | [E] Most literal match to invariant 8 — a distinct "governed review" act for the distinct claim of durability/canonicity | [A] Risks tension with "never automatically" if any default-admission path is read broadly |
| Ownership boundaries | [O] No interaction — orthogonal to admission model | [O] No interaction | [O] No interaction |
| Lifecycle implications | [E] Collapses Candidate→Admitted into one step (per `KNOWLEDGE_LIFECYCLE_CONTRACT_v1.0.md`) | [E] Preserves the Candidate→Under Review→Admitted separation the Lifecycle Contract already explored | [A] Requires a lifecycle concept (default/window) with zero precedent in this system |
| Trace explainability | [E] Every real `approve` Trace record would need reinterpretation as a dual-purpose event — reduces per-record clarity of *which* judgment was made | [E] Each Trace record continues to represent exactly one judgment, matching the "one action, one Trace record" invariant's spirit of unambiguous records | [A] A default-path admission would produce *no* explicit Trace record for the actual admission moment — in tension with unconditional Trace production |
| Memory separation principles | [E] No interaction — Memory's derived-only nature is unaffected by any option | [E] Same | [E] Same |
| Human review requirements | [E] Reuses existing contract exactly, zero new requirement | [A] Requires reviewers to engage with a second decision — untested whether this is valued or treated as a rubber stamp | [A] Requires reviewers to actively opt out within an unspecified window — untested |
| Future scalability | [A] Simplest to scale (no added step) but scales a conflation, not a clean concept | [E] Scales cleanly — each new admission is one more of the same, already-proven event shape | [A] Scaling a default-with-override pattern requires defining the override window's scale behavior, unevidenced |
| Migration risk | [E] Lowest risk *to build*, highest risk *to unwind* (4 real approvals would need retroactive reinterpretation either way this is resolved) | [E] No retroactive reinterpretation needed — existing approvals remain exactly what they are | [A] Highest combined risk — inherits A's retroactive question for anything already defaulted, plus B's new-contract cost |
| Implementation complexity | [E] Zero — no code change | [E] Moderate — one new decision type or sibling contract, reusing proven validation/snapshot patterns | [A] Highest — a new contract plus a temporal/default mechanism this codebase has never built anything analogous to |

### Admission Model Sub-Questions (Directive Section A)

**What qualifies as a candidate for Knowledge promotion?**
[E] Only an already-`approve`d `CandidatePackage` — real evidence shows `reject` is an explicit refusal (1 real event) and should not proceed further under any option. [O] Whether an `edit`-decided candidate (1 real event) should use its original or `edited_content` if later admitted is genuinely unresolved — no evidence addresses this, since no admission has ever occurred.

**Memory-signal driven / Human-curated / Capability-domain driven / Hybrid?**
[E] Pure Memory-signal-driven (automatic) is foreclosed outright by invariant 8's explicit "never automatically." [E] Capability/domain-driven is not currently evaluable — Capability is classified **Not Implemented** in `AIOS_DOMAIN_MODEL_v1.0.md`, so no code path could implement this today. [E] Human-curated is the only option with a fully proven real mechanism (6/6 real decisions, structurally guaranteed non-automated). **Recommendation: Human-curated, informed by Memory signals for prioritization only** — a hybrid in the specific, already-evidenced sense that `promotion.py` already ranks candidates by confidence/occurrence/source-type without ever using those signals to bypass human decision.

**Should confidence/frequency influence eligibility or only prioritization?**
[E] Real code precedent already answers this: `promotion.py`'s `is_degenerate_content()` filters only on structural degeneracy (length, heading fragments) — never on confidence or occurrence count. Every real candidate, regardless of confidence, has always been eligible for human review; confidence and occurrence only ever affect ranking order. **Recommendation: prioritization only, never eligibility** — this is not a new design choice, it is consistency with an already-proven, unmodified pattern.

**Preserving "Memory never automatically becomes Knowledge"?**
[E] Both Option A and Option B satisfy this literally (a human decision is always required). [E] Option B satisfies it more robustly in spirit, because the specific decision being made is unambiguously "admit to Knowledge," not a decision made for one purpose (candidate retention) silently repurposed for another (durable canonical status).

### Recommendation

**Recommend Option B — Separate Knowledge Admission Decision**, specifically as a new decision type layered on the existing, proven Human Review infrastructure (reusing validation-before-write and immutable-snapshot patterns, not inventing new mechanics) rather than a wholly new contract from scratch.

**Reasoning, strictly from evidence**: real reviewer rationale text across multiple real `approve` events has organically, repeatedly drawn the exact distinction Option B preserves and Option A would erase. This is not a hypothetical preference — it is what the one real reviewer this system has ever had has actually written, unprompted, in every real approval. Option C's benefits are speculative (reduced review burden) while its risks are the most evidenced-against of the three (temporal defaults, contradicts explicit-only-governance precedent, no Trace-clarity guarantee at the actual admission moment).

**This is a recommendation, not an authorization.** No contract change occurs as a result of this document.

---

## 3. Knowledge Ownership Model — Full Review

### Restated Architectural Problem

Domain Model §5 requires each Knowledge item have a home Department, within Organization-level collective ownership. No Department resolution mechanism exists anywhere in this Execution Layer — `promotion.Provenance.department_status` is honestly `"unavailable"` on every one of the 370 real memories in the corpus today.

### Options (restated)

**A — Department-owned directly.** **B — Organization-owned with Department steward.** **C — Agent-generated proposal requiring Human assignment.**

### Evaluation Against Criteria

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Domain Model compatibility | [E] Most literal reading of §5's "home Department" | [E] Also valid — §5's "collectively owned by the Organization" clause supports a steward reading equally | [E] Compatible — assignment mechanism, not ownership philosophy; doesn't contradict either §5 clause |
| Ownership boundaries | [O] Requires a real Department resolution mechanism that does not exist — **identical blocker for A and B** | [O] Same blocker | [E] No blocker — reuses the real, already-defined `department_override`/`department_override_reason` field pair, unused (0/6) but present and validated in `review_decision.py` today |
| Lifecycle implications | [O] Unaddressed — no real precedent for Department-scoped lifecycle authority anywhere in this system | [O] Same | [A] Curator (reviewer) accountability is real and precedented (`reviewer_identity`, 6/6 real events); Department-level lifecycle authority remains equally unaddressed |
| Trace explainability | [O] Would require a new Trace field or convention — unevidenced | [O] Same | [E] Fits the existing Trace record shape exactly — `department_override` already has a real, tested slot in the real `human_review_decision_recorded` event |
| Memory separation principles | [E] No interaction | [E] No interaction | [E] No interaction |
| Human review requirements | [O] Requires the reviewer (or an unspecified other actor) to know/derive the correct Department — mechanism unspecified | [O] Same | [E] Requires the reviewer to explicitly type a Department identifier — same unauthenticated-free-text pattern `reviewer_identity` already safely uses |
| Future scalability | [A] Scales well **once** Department resolution exists — but that is a separate, unscheduled implementation project | [A] Same | [A] Scales adequately at low volume (matches this arc's real corpus scale); accuracy at higher volume without a resolution mechanism to validate against is untested |
| Migration risk | [E] Cannot be implemented at all until Department resolution exists — not a risk so much as a hard block | [E] Same hard block | [E] Lowest — buildable today with zero new implementation, and can be superseded later once real Department resolution exists without needing to unwind anything structural |
| Implementation complexity | [E] Requires building Department resolution first (unscheduled, out of scope of any phase so far) | [E] Same | [E] Zero new code — the field already exists |

### Ownership Model Sub-Questions (Directive Section B)

**Relationship between Organization / Department / Agent Instance provenance / Reviewer responsibility?**
[E] Agent Instance provenance is real and already tracked (`Provenance.agent_definition_name`, present on every real candidate). [E] Reviewer responsibility is real and tracked (`reviewer_identity`, required on every real decision). [O] Department's relationship to either remains entirely unresolved — no code path connects an Agent Definition to a Department today.

**Origin-based / Domain-based / Curator-based / Hybrid?**
[E] Origin-based (deriving Department from the producing Agent Definition) and Domain-based (deriving from Capability) both require infrastructure that does not exist (Department mapping, Capability implementation — the latter confirmed Not Implemented). [E] Curator-based (a human explicitly assigns it) is the only option exercisable with real, existing infrastructure. **Recommendation: Curator-based, i.e. Option C**, as an explicit, disclosed interim model — not necessarily the permanent one.

**How does ownership affect revision authority, retrieval visibility, accountability, and future lifecycle?**
[E] Accountability is the one sub-question Option C answers today with real precedent: the assigning reviewer's identity is captured exactly as `reviewer_identity` already is, giving a real accountable human even without a real Department resolution mechanism. [O] Revision authority, retrieval visibility, and lifecycle implications of ownership are all unaddressed by any option — none has ever been exercised, and this review does not resolve them.

### Recommendation

**Recommend Option C — Agent-generated proposal requiring Human assignment**, explicitly as an interim, disclosed model, not a permanent architectural conclusion.

**Reasoning, strictly from evidence**: Options A and B are not merely harder to implement — they are currently un-implementable, full stop, because the Department resolution mechanism that is a Domain-Model-required prerequisite for adequately either does not exist anywhere in this Execution Layer, and building it is outside this review's scope. Option C is the only one of the three that can be exercised today using infrastructure that already exists, is already tested, and already follows this arc's established never-guess discipline (explicit human input, same pattern as `reviewer_identity`). This recommendation is explicitly **not** a claim that Curator-based ownership is philosophically superior to Department-based ownership — it is a claim that it is the only one evidence-buildable without first solving a separate, larger, unscheduled problem.

**This is a recommendation, not an authorization.**

---

## 4. Decision Matrix (Summary)

| Decision | Options | Strongest evidence-backed choice | Why |
|---|---|---|---|
| Admission Model | A / B / C | **B** | Preserves the real distinction reviewers have organically drawn; no retroactive reinterpretation of real data; lowest Trace-clarity cost |
| Ownership Model | A / B / C | **C** | Only option buildable without first solving the unscheduled Department-resolution problem; reuses real, already-tested infrastructure |

---

## 5. Consequence Analysis

### If Admission Model B is adopted:

**Unlocked**: a clean, distinct Trace event for Knowledge admission; the ability to admit some approved candidates and not others without touching the meaning of `approve`; a natural place to later attach Department assignment (Ownership) and evidence-threshold calibration (Blocker #13) without re-opening the Human Review contract itself.

**Constrained**: every future admission requires two real human decisions per candidate instead of one — a real, ongoing review-burden cost with no data yet on whether reviewers find this valuable.

**Future decisions depending on this choice**: the Lifecycle Contract's "Admitted" state design (its authority requirement is defined relative to whichever admission model is chosen); the eventual evidence-threshold decision (Blocker #13) attaches naturally to this new decision type rather than to `approve`.

### If Ownership Model C is adopted:

**Unlocked**: Knowledge admission (once its own model is decided) does not need to wait on Department resolution being built — `department_override` already exists and can be exercised as soon as an admission decision type exists.

**Constrained**: ownership data quality depends entirely on individual reviewer accuracy, with no systemic validation — a real, disclosed, accepted limitation until Department resolution exists separately.

**Future decisions depending on this choice**: if a real Department resolution mechanism is later built, a migration question arises — whether to retroactively reconcile curator-assigned Departments against it, or treat them as a permanently valid historical record (consistent with this system's append-only philosophy). This migration question is not resolved here.

---

## 6. Updated Open Question Register

Building on `KNOWLEDGE_ADMISSION_BLOCKER_REGISTER_v1.0.md`, with this review's tags applied:

| # | Question | Tag | Status after this review |
|---|---|---|---|
| 1 | Admission Model selection | Was [C]-required | **Recommendation issued (B)** — still requires Architect authorization |
| 2 | Ownership Model selection | Was [C]-required | **Recommendation issued (C)** — still requires Architect authorization |
| 3 | Whether an `edit`-decided candidate uses original or `edited_content` if admitted | [O] | Newly surfaced by this review, unresolved |
| 4 | Whether reviewers will treat a second (admission) decision as meaningful or as a rubber stamp | [A] | Unresolved — requires real usage under Model B, if authorized |
| 5 | Department resolution mechanism itself | [O] / Category D | Unchanged — out of scope for both this review and the option it recommends |
| 6 | Migration path if Department resolution is later built (reconcile curator assignments or not) | [O] | Newly surfaced by this review, unresolved |
| 7 | Evidence threshold for admission specifically (Blocker #13) | [A] | Now has a natural attachment point (the new admission decision) if Model B is authorized |

All other items from the prior Blocker Register (#3–#12, #14–#23) are unaffected by this review and remain exactly as classified there.

---

## 7. Implementation Readiness Impact

Two of the twelve Category-C (Architect-decision) blockers now carry an evidence-based recommendation rather than three undifferentiated alternatives each. This **narrows** the design space materially but does **not** change the standing readiness conclusion: Knowledge Admission remains **NOT READY**, because a recommendation is not an authorization, and even with both decisions authorized, Blocker #5 (lifecycle state set), #6 (supersession), #19 (conflict resolution), and several others remain fully open regardless of how these two decisions land.

---

No implementation, contract, schema, or governance-document change has occurred. Awaiting Architect authorization on both recommendations before any further phase.
