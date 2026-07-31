# Knowledge Governance Contract Design — Conflict Governance v1.0

**Status:** Design analysis only. No conflict resolution mechanism is implemented.
**Version:** v1.0
**Authority:** Subordinate to `KNOWLEDGE_GOVERNANCE_PRINCIPLES_v1.0.md`'s conflict-visibility principle and to the real, tested `memory_governance.detect_conflicts()` mechanism, which this document analyzes the implications of extending to Knowledge — without designing that extension.
**Approved by:** Architect, Phase 8 — Knowledge Governance Contract Design.

---

## When Two Knowledge Claims Conflict

**Known**: at the Memory layer, conflict *detection* is real and proven — `memory_governance.detect_conflicts()` correctly identifies two memories that resolve to the same Tool-derived subject but disagree on outcome, validated against a real, controlled scenario (a genuine file edit between two real Tool calls). **Known**: zero organic conflicts have occurred in real data across four independent scans of the entire real corpus this arc.

**Unknown**: whether the same detection technique (matching on a Tool's registered cache key) generalizes to Knowledge entities, which — unlike Memory — would not necessarily retain a live link back to the Tool call that originally produced their content, per the durability principle in `KNOWLEDGE_GOVERNANCE_PRINCIPLES_v1.0.md` ("Knowledge does not read Memory directly at consumption time").

**Requires future contract decision**: whether two conflicting Knowledge entities can both exist simultaneously in a declared-conflicting state (requiring a resolution decision type), or whether conflicts must be resolved before either candidate is ever admitted (making post-admission Knowledge-to-Knowledge conflict structurally impossible by construction). Phase 7's Admission Boundary document already posed this as an open question; it remains open here, with no new evidence to resolve it.

## When Evidence Changes

**Known**: the Evidence Verification Layer (Tier 2) already proves this exact scenario is detectable and handleable at the Tool-call level — a real drift experiment demonstrated a genuine file edit correctly invalidating a stale cache entry and triggering live re-verification, with the one real defect found in this mechanism (a deleted-file fail-open gap) already found and repaired.

**Unknown**: whether an Active Knowledge entity should be automatically re-verified against its original source evidence on some schedule, on every consumption, or only on manual trigger — no real Knowledge entity has ever existed to observe any of these patterns against.

**Requires future contract decision**: whether "evidence changed" should transition a Knowledge entity to "Revision Required" (per `KNOWLEDGE_LIFECYCLE_CONTRACT_v1.0.md`) automatically, or only flag it for human attention — automatic transition risks tension with invariant 8's "never automatically" language if read broadly (though that invariant is about *promotion into* Knowledge specifically, not necessarily about *state changes within* an already-admitted entity; this distinction itself is unresolved).

## When a Previous Knowledge Item Becomes False

**Known**: the real `reject` decision proves this system can express "this should not be trusted" as a permanent, human-authored record — but only ever exercised on a candidate that was never admitted, never on something already Active and relied upon.

**Unknown**: whether "becomes false" should route to Deprecated (permanent, no successor) or Superseded (permanent, with a successor) — both states exist only as design discussion in `KNOWLEDGE_LIFECYCLE_CONTRACT_v1.0.md`, neither has any real precedent.

**Requires future contract decision**: who or what can assert "this Knowledge item is now false" — a human reviewer (consistent with every real governance act this arc has produced), an automated evidence-verification failure (would need careful scoping to avoid becoming an automatic decision, forbidden by the standing no-automation-over-governance principle), or some hybrid where automation flags and a human confirms (closest to this system's existing pattern, e.g. how `detect_conflicts()` flags without resolving).

## When Reviewers Disagree

**Known**: **zero real evidence exists.** Exactly one reviewer identity (`MoriartyTalk`) has ever recorded a real Human Review decision — 6/6 events, all attributable to the same person. There has never been a second reviewer, so there has never been a disagreement to observe.

**Known**: the code paths that would need to handle this (`review_state()`'s precedence logic: `reject` > `edited` > `approved`) are proven structurally independent of *who* the reviewer is (re-verified this arc via both text search and AST inspection of `memory_governance.py`) — but this proves the code doesn't discriminate by identity, not that the precedence rule itself produces a sensible outcome when two *different* people genuinely disagree.

**Unknown**: everything about actual disagreement-handling behavior — whether a second reviewer's `reject` should override a first reviewer's `approve` (today's precedence rule would say yes, but this rule has never been tested against a real cross-reviewer disagreement, only a same-reviewer duplicate-submission scenario that was declined and never written), whether disagreement should itself become a visible governance signal (analogous to a conflict), or whether it requires escalation to a higher authority tier per the Constitution's Decision-Making Process.

**Requires future contract decision**: the entire cross-reviewer disagreement handling model — this cannot be responsibly designed without at least one real instance of it occurring, which this system has never had.

---

## Summary

| Scenario | Known | Unknown | Requires future contract decision |
|---|---|---|---|
| Two Knowledge claims conflict | Detection mechanism proven at Memory layer; zero organic conflicts observed | Whether detection generalizes to durable, source-decoupled Knowledge entities | Resolve-before-admission vs. coexist-and-resolve-later |
| Evidence changes | Tier 2 verification proven live, one defect found and repaired | Re-verification cadence/trigger for an Active Knowledge entity | Automatic vs. flag-only transition to Revision Required |
| Previous Knowledge becomes false | `reject` proves the expressive mechanism exists, never used on an Active entity | Deprecated vs. Superseded routing | Who/what may assert falsity |
| Reviewers disagree | Code is provably reviewer-identity-independent | Everything about actual behavior — zero real instances ever | The entire disagreement-handling model |

Every scenario in this document terminates in an open question. This is the expected, evidence-honest outcome of a design-only phase analyzing a capability (Knowledge) that has never been implemented, applied to a governance dimension (conflict) that has never organically occurred in this system's real history.
