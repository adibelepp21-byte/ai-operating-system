# Knowledge Governance Contract Design — Admission Contract v1.0

**Status:** Design analysis only. No model is selected. No contract is implemented.
**Version:** v1.0
**Authority:** Subordinate to `KNOWLEDGE_GOVERNANCE_PRINCIPLES_v1.0.md` and the ratified Domain Model invariant 8. Extends the two admission options first identified in Phase 7's Lifecycle Discovery document into a full comparative analysis, per this phase's directive.
**Approved by:** Architect, Phase 8 — Knowledge Governance Contract Design.

---

## Model A — Human Review `approve` Becomes Knowledge Admission

A real `approve` decision on a `CandidatePackage`, using the existing Human Review contract exactly as it stands today, directly constitutes (or immediately triggers) Knowledge admission. No new decision type.

**Advantages**
- Zero new contract required — `review_decision.py` already works, proven across 6 real decisions.
- No new authority question — the same reviewer authority that already governs candidate approval would govern admission.
- Fastest path to a working Knowledge pipeline, reusing everything this arc has already validated.

**Risks**
- Conflates two potentially different judgments. Real reviewer rationale text (all 4 real `approve` events) has repeatedly hedged: *"this approval only states the evidence package is fit to retain... not that the content has been verified externally"* (paraphrased pattern from the real corpus). Treating `approve` as Knowledge admission would silently upgrade every past approval's meaning without the reviewer having been asked that question.
- No way to approve a candidate as "good enough to keep as a governance record" without also admitting it to Knowledge — removes a distinction reviewers have organically been making in their own words.

**Required changes**
- None to the contract itself. A downstream consumer would need to treat every real `approve` event (retroactively, for the 4 that already exist, and going forward) as a Knowledge admission trigger — a semantic decision about existing data, not a code change, but a governance decision with real consequences for the 4 already-recorded approvals.

**Missing evidence**
- Whether a reviewer, asked explicitly "does approve mean admit to Knowledge," would have decided differently on any of the 4 real approvals. Unknowable retroactively without asking.

---

## Model B — Separate Knowledge Admission Decision

Candidate `approve` remains exactly what it means today. A distinct, new decision type (new value or new contract) is required, applied only to already-approved candidates, before Knowledge admission occurs.

**Advantages**
- Preserves the real, already-observed distinction reviewers have been drawing in their own language without being asked to.
- More conservative — consistent with invariant 8's "governed review" language being read as requiring deliberate action, not an automatic byproduct of an earlier, differently-scoped decision.
- Does not retroactively reinterpret any of the 4 existing real `approve` events.

**Risks**
- Requires a new contract — the `HumanReviewDecisionInput.decision` enum (currently `approve`/`reject`/`edit`) would need extension or a sibling contract, both explicitly forbidden without separate Architect authorization under the Evolution Protocol.
- Adds review burden — every candidate destined for Knowledge would need two real human judgments instead of one, unproven whether reviewers would find this valuable or redundant.
- No real precedent anywhere in this system for a two-stage decision on the same underlying content.

**Required changes**
- A new decision type or a new, Knowledge-specific contract (structurally similar to `HumanReviewDecisionInput` but distinct), and a new Trace event shape for it — both require Contract Review under the Evolution Protocol before any implementation.

**Missing evidence**
- Whether real reviewers would engage meaningfully with a second decision step, or treat it as a rubber stamp — no data exists on reviewer behavior across a two-stage process anywhere in this system.

---

## Model C — Hybrid Model

`approve` continues to mean what it means today (evidence-package sufficiency for retention). A Knowledge admission step exists separately, but is lightweight — e.g., a batch or periodic act rather than a per-candidate decision, or one that defaults to admission unless a reviewer explicitly flags otherwise within some window.

**Advantages**
- Avoids doubling per-candidate review burden (Model B's risk) while preserving the real distinction reviewers already draw (Model A's risk).
- Could reuse existing infrastructure (Trace, Human Review's snapshot-immutability pattern) for the lightweight step without a full second review contract.

**Risks**
- "Defaults to admission unless flagged" risks drifting toward automatic promotion — directly in tension with invariant 8's "never automatically," unless the default-admission window itself requires an explicit human confirmation step, which would then resemble Model B again.
- The most structurally novel of the three options — no real precedent in this codebase for any "opt-out" or "default" governance pattern; every real governance act this arc has produced has been explicit, not a default.

**Required changes**
- A new contract, likely more complex than Model B's (needs to express both the lightweight default path and the explicit-flag override path) — highest design cost of the three.

**Missing evidence**
- Whether a default-admission pattern is even compatible with invariant 8's "never automatically" language without further Architect interpretation — this is as much a governance-text question as an engineering one, and this document is not authorized to resolve it.

---

## Comparison Summary

| | Model A | Model B | Model C |
|---|---|---|---|
| New contract required | No | Yes | Yes (more complex) |
| Preserves existing `approve` meaning | No | Yes | Yes |
| Review burden | Lowest | Highest | Medium |
| Risk of drifting toward automatic promotion | Low | Lowest | Highest |
| Real precedent in this codebase | Strong (reuses proven contract) | Partial (extends proven pattern) | Weakest (novel pattern) |

No model is recommended over another. Selecting one requires either real evidence this system does not yet have (how reviewers actually respond to a two-stage or default-admission process) or an Architect decision on how strictly invariant 8's "never automatically" language constrains Model C — neither of which this design phase is authorized to produce.
