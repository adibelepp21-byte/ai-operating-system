# Architect Decision Package v1.0

**Status:** Decision preparation only. No decision is made by this document.
**Version:** v1.0
**Authority:** Subordinate to `KNOWLEDGE_ADMISSION_BLOCKER_REGISTER_v1.0.md` (Blockers #1 and #2, the two highest-leverage Category C/D items) and every prior Knowledge design document this arc has produced. Prepares, does not resolve, the two decisions those documents identified as unblocking the most downstream work.
**Approved by:** Architect, Phase 10 — Knowledge Architecture Decision Gate & Conflict Evidence Expansion.

---

## Section 1: Knowledge Admission Model Decision

### Option A — Approve = Admission

A real `approve` decision on a `CandidatePackage`, using the existing Human Review contract exactly as it stands today, directly constitutes Knowledge admission.

- **Required contract changes**: none. `review_decision.py` requires zero modification.
- **Existing evidence supporting it**: 4 real `approve` events exist, all structurally sound, all with intact provenance chains. The contract's mechanics (validation-before-write, immutable snapshot, no automated decision) are fully proven.
- **Risks**: real reviewer rationale text has repeatedly, in the reviewer's own words, distinguished "this evidence package is fit to retain" from "this content is verified as true" — adopting this option retroactively reinterprets the meaning of all 4 existing real approvals without having asked the reviewer that specific question.
- **Governance implications**: collapses candidate-review authority and Knowledge-admission authority into one act — simplest governance surface, but the least separation of concerns among the three options.
- **Future migration complexity**: lowest. If this option is later found insufficient, migrating to Option B or C means introducing a new decision type without needing to first remove or reinterpret an existing one.

### Option B — Separate Knowledge Admission Decision

Candidate `approve` remains exactly what it means today. A distinct, new decision type (or a sibling contract) is required, applied only to already-approved candidates, before Knowledge admission occurs.

- **Required contract changes**: a new decision type in `HumanReviewDecisionInput.decision` (currently a closed 3-value enum) or a new, parallel contract — both require Contract Review under the Evolution Protocol.
- **Existing evidence supporting it**: none directly (no such contract exists), but the real reviewer-rationale pattern above is indirect evidence *for* preserving the distinction this option preserves.
- **Risks**: no real precedent anywhere in this system for a two-stage decision on the same content; unproven whether reviewers would find a second stage valuable or redundant; doubles review burden per candidate destined for Knowledge.
- **Governance implications**: cleanest separation of concerns — candidate quality and Knowledge durability become independently governable, potentially by different authority tiers.
- **Future migration complexity**: highest upfront cost (new contract), but most extensible afterward — a distinct decision type is easier to evolve independently (e.g., adding Department-scoped approval later) without touching the original Human Review contract at all.

### Option C — Hybrid Admission Gate

`approve` continues to mean what it means today. A lightweight admission step exists separately — e.g., a default-admission window unless a reviewer explicitly flags otherwise.

- **Required contract changes**: a new contract, structurally more complex than Option B's (must express both a default path and an explicit-override path).
- **Existing evidence supporting it**: none. This is the most structurally novel option — no real precedent in this codebase for any "opt-out"/"default" governance pattern; every real governance act this arc has produced has been explicit.
- **Risks**: a default-admission window risks tension with Domain Model invariant 8's "never automatically" language, depending on how strictly that language is read — this is a governance-text interpretation question, not an engineering one, and is not resolved by this package.
- **Governance implications**: could reduce reviewer burden at scale, but at the cost of the clearest possible reading of invariant 8.
- **Future migration complexity**: highest — combines Option B's new-contract cost with an additional default/override mechanism that would itself need governance if ever revisited.

**STATUS: ARCHITECT DECISION REQUIRED**

---

## Section 2: Department Ownership Resolution

### Option A — Knowledge Owned Directly by Department

Each Knowledge item's `owning_department` is set directly, presumably by whichever Department's Agent Definition produced the originating candidate.

- **Alignment with Canonical Domain Model**: strong — matches §5's "each item has a home Department" most literally.
- **Existing implementation support**: none. The Department Mapping Evidence Pass found no Department field anywhere in Trace or the Execution Layer; `promotion.Provenance.department_status` is honestly `"unavailable"` on every real candidate today.
- **Missing evidence**: a real, working Department-to-Agent-Definition mapping does not exist anywhere in this system to assign from — this option cannot be implemented until that mapping exists, regardless of which admission model is chosen.
- **Future complexity**: once Department resolution exists elsewhere in the system, this option is the simplest to implement — a straightforward field assignment at admission time.

### Option B — Organization-Owned with Department Steward

Knowledge remains collectively Organization-owned (per Domain Model §5's own framing), with a Department acting as steward/point-of-contact rather than sole owner.

- **Alignment with Canonical Domain Model**: also consistent — §5's exact wording is "Collectively owned by the Organization; each item has a home Department," which this option reads as two distinct facts (collective ownership, plus a steward), rather than Option A's reading of Department as the primary owner.
- **Existing implementation support**: none, same underlying gap as Option A — a steward relationship still requires resolving which Department a given item's steward should be.
- **Missing evidence**: identical to Option A — no Department resolution mechanism exists to assign a steward from.
- **Future complexity**: potentially higher than Option A if "steward" implies different authority than "owner" (e.g., a steward might recommend but an Organization-level authority approves) — this distinction itself would need further definition, which this package does not provide.

### Option C — Agent-Generated Proposal Requiring Human Assignment

An Agent Instance's candidate carries no Department assignment at creation; a human reviewer explicitly assigns the Department as part of (or alongside) the admission decision.

- **Alignment with Canonical Domain Model**: consistent with §5, and additionally consistent with this arc's standing "never guess, always confirm" discipline — Department assignment becomes an explicit human act rather than an inferred one.
- **Existing implementation support**: partial — the Human Review contract already has a real, working pattern for exactly this kind of explicit human input (e.g. `department_override`/`department_override_reason`, an existing but never-yet-used optional field pair on `HumanReviewDecisionInput`, confirmed present in the real schema and 0/6 used in any real event so far).
- **Missing evidence**: whether reviewers can reliably assign correct Department ownership without a resolution mechanism to check their assignment against — no real data exists on this since the field has never been used.
- **Future complexity**: lowest new-mechanism cost (reuses an existing, already-defined field), but shifts the burden onto every individual reviewer decision rather than solving Department resolution once, systemically.

**STATUS: ARCHITECT DECISION REQUIRED**

---

## Section 3: Decision Dependency Map

```
Architect Decision
        |
        v
Contract Definition
        |
        v
Implementation Design
        |
        v
Migration Plan
        |
        v
Execution
```

**Work blocked by the Admission Model decision (Section 1):**
- Any code path from a reviewed candidate to a Knowledge entity.
- The Lifecycle Contract's "Admitted" state (`KNOWLEDGE_LIFECYCLE_CONTRACT_v1.0.md`) — its authority and transition rules are entirely dependent on which option is chosen.
- Whether the 4 existing real `approve` events retroactively become Knowledge admissions (Option A) or remain candidate-review-only (Options B/C) — a real-data consequence, not just a future-code one.

**Work blocked by the Ownership Model decision (Section 2):**
- `owning_department` field implementation (Entity Proposal, Blocker #1).
- Department-scoped approval/modify/retire authority (Ownership Model, Blocker #14).
- Any Constitution-tier mapping for admission authority that depends on Department (Governance Principles, Blocker #3).

**Work blocked by the Conflict Resolution Model (not decided in this package — Blocker #19):**
- Completing any admission path that could encounter a real conflict — a conflict-free first implementation could proceed without this, but could not be called complete.
- The Lifecycle Contract's "Revision Required" state, which this arc's design documents note may overlap conceptually with conflict signaling.

**Work blocked by the Versioning Model (not decided in this package — Blocker #4):**
- The Entity Proposal's `version` field.
- The Lifecycle Contract's Revision stage (two structurally different approaches were identified, neither evidenced).
- Supersession (Blocker #6), which presupposes a versioning scheme to supersede *between*.

---

## Section 4: Explicit Non-Decisions

Not decided by this package, and not decided by any phase so far:

- **Lifecycle final states** — 8 states explored in `KNOWLEDGE_LIFECYCLE_CONTRACT_v1.0.md`, none selected.
- **Supersession mechanism** — confirmed entirely absent from this repository; zero real precedent.
- **Revision authority** — two structurally different approaches identified (new-version-retained vs. edit-in-place-with-audit-trail), neither evidenced.
- **Conflict resolution** — detection is proven; resolution has never been designed by any phase, including this one.
- **Versioning strategy** — no precedent anywhere in this codebase for revising one entity over time.
- **Deprecation policy** — authority tier and mechanism both unresolved.

**Reason**: each of these requires separate Architect authorization, per the Evolution Protocol's own Contract Review and Invariant Review steps (`AIOS_EVOLUTION_PROTOCOL_v1.0.md` §3–§4). This package resolves nothing beyond preparing the two decisions explicitly assigned to it.
