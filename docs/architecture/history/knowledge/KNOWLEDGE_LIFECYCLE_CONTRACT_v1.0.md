# Knowledge Governance Contract Design — Lifecycle Contract v1.0

**Status:** Design analysis only. No state machine is implemented. No state is finalized.
**Version:** v1.0
**Authority:** Subordinate to `KNOWLEDGE_GOVERNANCE_PRINCIPLES_v1.0.md` and Phase 7's `KNOWLEDGE_LIFECYCLE_DISCOVERY_v1.0.md`, which first identified these stages informally; this document defines each formally, per this phase's directive, without selecting a final lifecycle.
**Approved by:** Architect, Phase 8 — Knowledge Governance Contract Design.

---

## Candidate

**Meaning**: content identified by `promotion.select_candidates()` as worth human attention — real, tested, exercised 368 times against the current corpus.
**Allowed transitions**: → Under Review (when a human begins evaluating it, informally — this system has no explicit "review started" event today, only the final decision).
**Authority required**: none — Promotion is read-only and requires no authorization to compute.
**Unknowns**: whether "Candidate" should be a durable, addressable state at all, given Memory's lack of stable identity (a candidate recomputed tomorrow may have different evidence attached even for identical content, per the generational-fingerprint-absence finding this arc already documented).

## Under Review

**Meaning**: a human reviewer is actively evaluating a candidate.
**Allowed transitions**: → Admitted, → Rejected, → (candidate remains Candidate if review is abandoned, per today's real behavior — nothing in `review_decision.py` requires a review to conclude).
**Authority required**: the human reviewer authority already exercised in this system (currently one real identity, `MoriartyTalk`).
**Unknowns**: this system has no real "review started" record today — only the final decision is ever written to Trace. Whether Knowledge governance needs an explicit "Under Review" Trace event (to prevent, e.g., two reviewers unknowingly reviewing the same candidate) is unaddressed by any evidence, since multi-reviewer behavior has never been observed at all.

## Admitted

**Meaning**: a real governance decision has brought this content into Knowledge, per whichever admission model (`KNOWLEDGE_ADMISSION_CONTRACT_v1.0.md`) is eventually chosen.
**Allowed transitions**: → Active (immediately, or after some unaddressed step).
**Authority required**: per the Admission Contract analysis — either the existing Human Review authority (Model A) or a new, undefined authority (Models B/C).
**Unknowns**: everything about this state depends entirely on which admission model is eventually selected — no real precedent exists for any of the three.

## Active

**Meaning**: the steady state of a durable, currently-trusted Knowledge entity, consumable by an Agent Instance (Domain Model §4's Agent-Instance-consumes-Knowledge relationship).
**Allowed transitions**: → Revision Required, → Deprecated, → Superseded.
**Authority required**: none to *remain* Active — this is a passive state, analogous to a Memory record being "fresh."
**Unknowns**: what "consumable" concretely means (what field a consumer reads, whether retrieval is involved) is unaddressed — the dormant `execution/knowledge/retrieval.py` prototype indexes real Documents, not a hypothetical Knowledge-entity store, and has never been consumed by any Trace record.

## Revision Required

**Meaning**: a signal that an Active Knowledge entity's content may no longer be accurate or complete, without yet asserting it is false (a weaker claim than Deprecated).
**Allowed transitions**: → Active (once revised), → Deprecated (if revision reveals the entity should not have been trusted).
**Authority required**: unaddressed — could plausibly be raised by any Agent Instance encountering contradicting evidence (analogous to `memory_governance.detect_conflicts()`'s detection-without-resolution pattern) or only by human review.
**Unknowns**: whether this state should exist as distinct from Active at all, or whether "requires revision" is better expressed as a conflict flag (per `KNOWLEDGE_CONFLICT_GOVERNANCE_v1.0.md`) rather than a lifecycle state — genuinely unresolved, no evidence either way.

## Deprecated

**Meaning**: this Knowledge entity should no longer be trusted or consumed, but is retained permanently for audit purposes (Domain Model §6: "not casually deleted").
**Allowed transitions**: terminal, unless → Superseded (if a replacement is later admitted).
**Authority required**: plausibly analogous to the existing `reject` decision's authority, per Phase 7's Lifecycle Discovery finding — the closest real precedent this system has for "this should not be trusted," though never yet exercised on an already-admitted entity rather than a never-admitted candidate.
**Unknowns**: whether deprecating an Active Knowledge entity requires the same authority as admitting one, or a higher tier (deprecating something already relied upon plausibly carries more consequence than declining to admit a new candidate) — unaddressed.

## Superseded

**Meaning**: a newer Knowledge entity has formally replaced this one.
**Allowed transitions**: terminal.
**Authority required**: unaddressed — searched explicitly this arc (Phase 5's corpus search); zero real mechanism or precedent exists anywhere in this repository.
**Unknowns**: the entire concept is unevidenced. Whether supersession requires a bidirectional link (old entity points to new, new entity points to old) or a one-directional one; whether a superseded entity remains queryable the same way a deprecated one does — all open.

## Rejected

**Meaning**: a candidate was evaluated and explicitly declined admission — never became Knowledge at all (distinct from Deprecated, which applies to something that *was* Active).
**Allowed transitions**: terminal (does not re-enter Candidate automatically — matches the real Human Review contract's behavior today, where a `reject` decision is a permanent Trace record, and nothing currently allows a rejected candidate to be re-submitted for a fresh decision without ambiguity about how the two decisions coexist).
**Authority required**: the existing Human Review `reject` authority — **the only state in this entire lifecycle with a real, exercised precedent** (1 real event, `trace-19f71086dd74`).
**Unknowns**: whether a Rejected candidate can ever be re-reviewed (per the review-precedence unknown already documented in the Memory Governance Hardening report — 0 real multi-decision cases exist to observe this against).

---

## Summary Table

| State | Real precedent | Authority clarity |
|---|---|---|
| Candidate | Strong (`CandidatePackage`, real) | Clear (none needed) |
| Under Review | None (no explicit Trace event today) | Clear (existing reviewer authority) |
| Admitted | None | Unresolved (depends on admission model) |
| Active | None (structurally simple) | Clear (passive) |
| Revision Required | None | Unresolved |
| Deprecated | Partial (`reject` pattern) | Partially clear, tier unresolved |
| Superseded | None — confirmed entirely absent from this repository | Fully unresolved |
| Rejected | **Strong — 1 real event** | Clear (existing `reject` authority) |

No lifecycle is finalized by this document.
