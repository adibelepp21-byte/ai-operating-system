# Knowledge Architecture Discovery — Lifecycle Discovery v1.0

**Status:** Design exploration only. No lifecycle is selected or implemented by this document.
**Version:** v1.0
**Authority:** Subordinate to the ratified Canonical Domain Model §6 ("Versioned; revised/superseded via review; not casually deleted") and invariant 8 ("promoted... only through governed review — never automatically"). This document explores possible concrete lifecycles consistent with those requirements; it selects none of them.
**Approved by:** Architect, Phase 7 — Knowledge Architecture Discovery.

---

## Why No Lifecycle Is Selected Here

Selecting a final lifecycle would require evidence this repository does not yet have: at least one real admission, at least one real revision, and at least one real deprecation or supersession, observed against real data — the same evidence-first discipline every other governed mechanism in this system was built under (Human Review's contract was not finalized until a real pilot exercised it; Memory Governance's trust model was not finalized until real approve/reject/edit data existed). No Knowledge entity has ever been created, so no lifecycle transition has ever been observed. What follows is an exploration of plausible stages, each graded by how much real precedent already exists for it.

## Stage 1: Candidate

**Real precedent: strong.** `promotion.CandidatePackage` already exists, is real, tested, and has been the direct input to every real Human Review decision this arc produced (6/6 real events). A Knowledge lifecycle's "Candidate" stage would very plausibly be exactly this — Memory that has been ranked and packaged for review, nothing more.

**Alternative considered**: a Knowledge-specific candidate shape, distinct from `CandidatePackage`. No evidence supports this being necessary — the existing shape already carries content, provenance, and evidence summary, everything a reviewer has needed so far.

## Stage 2: Review

**Real precedent: strong.** The Human Review contract (`review_decision.py`) is real, exercised 6 times, covering all three decision types (`approve`, `reject`, `edit`). Whether Knowledge admission requires this exact same review contract, or a distinct one layered on top, is the central open question of `KNOWLEDGE_ADMISSION_BOUNDARY_v1.0.md`.

**Alternative considered**: a two-stage review (first for Memory-candidate quality, second specifically for Knowledge admission). No evidence exists either way — this would be a new decision type never yet built or exercised.

## Stage 3: Admission

**Real precedent: none.** No code path in this repository ever writes a Knowledge entity. This stage is entirely hypothetical. Two structurally different approaches are plausible, neither evidenced:

- **Option A — admission is implicit in `approve`.** A real `approve` decision on a candidate directly becomes (or immediately produces) a Knowledge entity. Simple, but conflates "this evidence package is fit to retain as a governance record" (what `approve` currently, provably means, per every real rationale recorded so far) with "this understanding is now canonical and durable" (a materially stronger claim).
- **Option B — admission is a distinct, later step.** `approve` remains what it means today; a separate, explicit admission decision (possibly requiring different authority, per Constitution §3's tiers) promotes an approved candidate into Knowledge. More conservative, consistent with invariant 8's emphasis on governed review being deliberate, but adds a contract this system has never had.

Neither option has evidence favoring it over the other. This is a genuine open design question, not a gap this document is authorized to close.

## Stage 4: Active

**Real precedent: none, but structurally simple.** If Knowledge exists, "Active" is presumably its default steady state — the analogue of Trace records simply existing, or Memory being "fresh" per `evaluate_relevance()`. No open question here beyond what "Active" would need to expose to a consumer, which depends entirely on unresolved retrieval questions (Concept Analysis §3, "retrieval result").

## Stage 5: Revision

**Real precedent: none.** No entity in this system has ever been revised in place — Trace is append-only by design (no revision, only new records); Human Review decisions are likewise one-shot events. Knowledge would be the first entity requiring "the same thing, updated" semantics. Two approaches are plausible:

- **Revision as a new version, old version retained** (Trace's own append-only philosophy, extended to Knowledge) — consistent with Domain Model §6's "not casually deleted."
- **Revision as an edit in place with an audit trail** — closer to how `review_decision.py`'s `edit` decision already works for a single candidate (original preserved, correction stored separately, never overwriting).

The second option has a closer real precedent in this codebase (the `edit` decision's proven immutability-preserving pattern) but has never been exercised at Knowledge-entity scale, only at single-review scale.

## Stage 6: Deprecation

**Real precedent: partial.** The Human Review contract's `reject` decision proves this system can express "this should not be trusted/retained" as a real, human-authored, permanent record. Whether Knowledge deprecation reuses this exact mechanism, or needs its own (since deprecating an already-admitted Knowledge entity is a different act than rejecting a never-admitted candidate), is unresolved.

## Stage 7: Supersession

**Real precedent: none.** Searched explicitly during Phase 5 (Knowledge Admission Evidence Acquisition) — the only textual hit for "supersession" anywhere in this repository was a docstring in the dormant `execution/knowledge/retrieval.py` explicitly disclaiming that it models this. No mechanism, no data, no real case exists.

---

## Summary Table

| Stage | Real precedent | Selection status |
|---|---|---|
| Candidate | Strong (`CandidatePackage`, 6 real reviews) | Not selected — documented as most-evidenced option |
| Review | Strong (real Human Review contract, all 3 decision types) | Not selected — open question of reuse vs. new contract |
| Admission | None | Not selected — two structurally different options, no evidence favoring either |
| Active | None (structurally simple) | Not selected |
| Revision | None (partial pattern from `edit`) | Not selected — two options, one with closer precedent |
| Deprecation | Partial (`reject` pattern) | Not selected |
| Supersession | None | Not selected — explicitly confirmed absent from this repository |

No alternative is recommended over another in this document. This is intentional — selecting a final lifecycle requires the evidence this repository does not yet have.
