# Knowledge Admission Blocker Register v1.0

**Status:** Classification only. No blocker is resolved by this document.
**Version:** v1.0
**Authority:** Subordinate to all ten Knowledge design documents reviewed below. This register does not introduce any new unknown — it classifies every one already identified across them.
**Approved by:** Architect, Phase 9 — Knowledge Admission Evidence Closure & Contract Readiness Assessment.

---

## Category Legend

- **A — Can be solved by additional evidence.** No contract or code change needed; more real (or legitimately controlled) data would close the gap.
- **B — Requires real-world usage.** Cannot be forced or simulated; requires an event this system doesn't control (a second reviewer, an organic conflict, a real multi-decision case).
- **C — Requires Architect contract authorization.** A design/contract decision must be made before any further evidence or implementation is meaningful.
- **D — Requires implementation.** A concrete mechanism must be built; no amount of evidence or decision-making alone closes it.

---

## Register

| # | Blocker | Source document(s) | Category |
|---|---|---|---|
| 1 | Department ownership resolution mechanism does not exist anywhere in this system | Concept Analysis §4; Governance Principles (Authority Hierarchy); Ownership Model (Department Ownership) | **D** |
| 2 | Knowledge admission model selection (reuse `approve` / distinct decision / hybrid) | Admission Boundary; Admission Contract (Models A/B/C); Lifecycle Discovery Stage 3 | **C** |
| 3 | Whether "governed review" for Knowledge maps onto an existing Constitution Decision-Making tier | Concept Analysis §4; Governance Principles (Authority Hierarchy) | **C** |
| 4 | Knowledge entity versioning mechanism (no precedent in this codebase for revising one entity over time) | Entity Proposal (`version` field); Concept Analysis §1 | **C**, then **D** once decided |
| 5 | Concrete lifecycle state set (Candidate → ... → Superseded) — 8 states explored, none selected | Lifecycle Discovery; Lifecycle Contract | **C** |
| 6 | Supersession mechanism — confirmed entirely absent, zero real precedent | Lifecycle Discovery Stage 7; Lifecycle Contract (Superseded state); Conflict Governance | **C**, then **D** |
| 7 | Revision-in-place vs. new-version-retained mechanism | Lifecycle Discovery Stage 5 | **C** |
| 8 | Deprecation authority tier (same as admission, or higher) | Lifecycle Discovery Stage 6; Lifecycle Contract (Deprecated state) | **C** |
| 9 | Whether an explicit "Under Review" Trace event is needed (today only the final decision is recorded) | Lifecycle Contract (Under Review state) | **C**, then **D** |
| 10 | Real evidence of review precedence under a genuine multi-decision case | Lifecycle Discovery; Multi-Decision Readiness Assessment | **B** |
| 11 | Real evidence of multi-reviewer behavior (only 1 identity exists in the corpus) | Admission Boundary; Ownership Model; Conflict Governance (reviewer disagreement); Multi-Decision Readiness Assessment | **B** |
| 12 | Real evidence of `reject`/`edit` path generalization beyond n=1 each | Architecture Readiness (Unknown Areas) | **B** |
| 13 | Evidence threshold required for Knowledge admission specifically, vs. candidate-review sufficiency | Admission Boundary ("What Evidence Is Required?") | **A**, bounded by **C** — more evidence can inform this, but final threshold is a decision |
| 14 | Department-scoped approval/modify/retire authority | Ownership Model ("Who Can Approve/Modify/Retire?") | **D** — blocked entirely on Blocker #1 |
| 15 | Conflict detection generalizing beyond the one real-tested Tool (cross-reference-link-validator) to the other two real Tools | Conflict Detection Readiness | **A** — directly addressable via controlled experiment, no contract change |
| 16 | Conflict detection generalizing to durable, source-decoupled Knowledge entities (not just live Memory) | Conflict Governance; Conflict Detection Readiness | **D** |
| 17 | Broader conflict classes (heuristic-sourced, cross-Tool, semantic/textual) — entirely undetectable by the current mechanism | Conflict Detection Readiness | **D** |
| 18 | Organic (uncontrolled) conflict occurrence — zero in 4 independent real-corpus scans | Architecture Readiness; Organic Conflict Report (prior phase) | **B** |
| 19 | Conflict resolution contract (detection exists; resolution does not) | Architecture Readiness; Admission Boundary; Conflict Governance | **C**, then **D** |
| 20 | Re-verification cadence/trigger for an Active Knowledge entity whose source evidence changes | Conflict Governance ("When Evidence Changes") | **C** |
| 21 | Who/what may assert an Active Knowledge entity has become false | Conflict Governance | **C** |
| 22 | Entire cross-reviewer disagreement handling model | Conflict Governance ("When Reviewers Disagree") | **B**, then **C** once a real case exists to design against |
| 23 | Retrieval metadata requirements for a Knowledge entity, if any, distinct from full-text Document indexing | Entity Proposal (`retrieval_metadata`) | **A/D** — genuinely unknown pending discovery; likely resolves to D once scoped |

---

## Category Summary

| Category | Count | Meaning |
|---|---|---|
| A (evidence-closeable) | 3 (#13 partial, #15, #23 partial) | Only #15 is cleanly, fully in this category |
| B (real-world usage required) | 6 (#10, #11, #12, #18, #22 partial) | The largest single group by count |
| C (Architect decision required) | 12 | The largest group by weight — most blockers are decisions, not evidence gaps |
| D (implementation required) | 7 (several overlapping with C as "then D") | Concentrated heavily around Department resolution (#1, #14) and conflict resolution (#16, #17, #19) |

**Observation**: only one blocker (#15) is a clean, fully evidence-closeable gap with no contract or implementation dependency. The overwhelming majority of what stands between this repository and Knowledge Admission is decision-making (Category C) and implementation (Category D), not observation. This matches, and sharpens, the standing conclusion of every prior readiness assessment this arc has produced: further passive evidence-gathering has diminishing returns from here.
