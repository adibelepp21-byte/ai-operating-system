# Knowledge Governance Contract Design — Ownership Model v1.0

**Status:** Design analysis only. Introduces no new ownership rule beyond what the ratified Domain Model already states or what real repository evidence already demonstrates.
**Version:** v1.0
**Authority:** Subordinate to the ratified Canonical Domain Model §5 (Ownership Rules), which already states: *"Knowledge — Collectively owned by the Organization; each item has a home Department."* This document analyzes what that ratified rule means operationally; it does not add to it.
**Approved by:** Architect, Phase 8 — Knowledge Governance Contract Design.

---

## Organization Ownership

**Ratified position**: the Organization collectively owns all Knowledge (Domain Model §5). This is not a per-item mechanism — it is the outer boundary within which Department-level ownership operates.

**Real evidence**: none needed or expected — Organization is the single root identity (Domain Model §2), and no code in this repository has ever needed to represent it explicitly, because every real action so far has occurred beneath exactly one implicit Organization.

**Analysis**: no new rule proposed. Organization-level ownership is a ceiling, not an operational mechanism this contract needs to define further.

## Department Ownership

**Ratified position**: each Knowledge item has a home Department (Domain Model §5).

**Real evidence**: **no Department resolution mechanism exists anywhere in this system.** The Department Mapping Evidence Pass (a prior phase) found no Department field in Trace or the Execution Layer at all; `promotion.Provenance.department_status` is honestly `"unavailable"` on every real candidate — never guessed, never inferred.

**Analysis**: this is the single largest real gap in any Knowledge ownership model. No new rule can responsibly be proposed here — the ratified rule (each item has a home Department) is unimplementable today without a Department resolution mechanism that does not exist, and building one is outside this design-only phase's authorization. Any Knowledge admission contract built without resolving this would either violate the ratified ownership rule or require inventing an unevidenced workaround — neither of which this document proposes.

## Agent Ownership

**Ratified position**: the Domain Model does not describe Agents (Agent Definition or Agent Instance) as owning Knowledge — Agent Definition is owned by a Department (§5); Agent Instance is "not owned" (§5, "a transient instantiation"). Neither is described anywhere as an owner *of* Knowledge.

**Real evidence**: consistent with this — no code in this repository treats an Agent Definition or Agent Instance as a Knowledge owner. The one real Agent Definition this system has ever exercised (Governance Artifact Integrity Agent) produces candidates and evidence, and its Agent Instances produce Trace records, but nothing in the ratified model or real code assigns Knowledge ownership to either.

**Analysis**: no new rule proposed. Agents are, per the ratified model, producers of the evidence and candidates that Knowledge would be admitted from — not owners of Knowledge itself. This document does not introduce Agent-level Knowledge ownership, since no evidence or ratified text supports it.

## Human Ownership

**Ratified position**: not addressed by the Canonical Domain Model at all — the Model's ownership table (§5) lists only Department, Organization, Runtime (for Agent Instance tracking), and "owned centrally" for Skill/Tool/Runtime/Workflow. No entity in the ratified model is "owned by a human."

**Real evidence**: humans in this system act as **reviewers**, not owners — `reviewer_identity` is a required field on every real Human Review decision (6/6 real events), but nothing in `review_decision.py` or anywhere else treats a reviewer as owning the thing they reviewed. A human's role, per every real decision this arc has produced, is to exercise governance authority over content owned (per the ratified model) by a Department — never to personally own the content.

**Analysis**: no new rule proposed. Conflating "who approved this" with "who owns this" would be a new concept this document is not authorized to introduce without evidence, and no evidence supports it — every real reviewer rationale this arc has produced frames approval as a judgment about the evidence package, never as a claim of personal ownership.

---

## Who Can Create a Proposal?

**Real evidence**: `promotion.select_candidates()` — a pure, unauthenticated, read-only function — is what currently produces candidates. No human or Agent "creates a proposal" in the sense of initiating one; candidates are algorithmically identified from existing Memory. Whether a future Knowledge contract should allow a human to directly propose (bypassing candidate selection) is unaddressed by any evidence — this document does not propose introducing that capability.

## Who Can Approve?

**Real evidence**: any human supplying a valid `HumanReviewDecisionInput` with `decision="approve"` — proven by 4 real events, currently exactly one real identity. No role-based or Department-scoped restriction exists in the real contract today; `reviewer_identity` is a free-text, unauthenticated field.

**Analysis, not a new rule**: this means the *current* real contract has no ownership-based approval restriction to inherit for Knowledge admission — if Department-scoped approval authority is desired for Knowledge (as the ratified ownership model would suggest), it would be a new restriction beyond what the existing, proven contract enforces, and building it depends on Department resolution existing first (see above).

## Who Can Modify?

**Real evidence**: the `edit` decision already exists and works (1 real event, `trace-502ab65e9b0f`) — a human can supply corrected content while the original is permanently preserved. No ownership check gates this today; the same unauthenticated `reviewer_identity` field applies.

**Analysis**: whether Knowledge modification (post-admission) should reuse this exact mechanism, or require Department-scoped authority, is the same open question as approval — unresolved for the same reason (Department resolution doesn't exist).

## Who Can Retire?

**Real evidence**: the `reject` decision is the closest real precedent (1 real event) — but it has only ever been exercised on a never-admitted candidate, never on something already Active. No real precedent exists for retiring (deprecating/superseding) an already-admitted entity.

**Analysis**: no new rule proposed. This document defers to `KNOWLEDGE_LIFECYCLE_CONTRACT_v1.0.md`'s finding that Deprecated/Superseded authority is entirely unresolved.

---

## Summary

| Ownership question | Ratified position | Real evidence | New rule proposed here |
|---|---|---|---|
| Organization | Collective owner, outer boundary | None needed | No |
| Department | Home owner per item | **No resolution mechanism exists** | No — cannot be responsibly proposed without Department resolution |
| Agent | Not an owner | Consistent — Agents produce, don't own | No |
| Human | Not addressed by ratified model | Reviewers, not owners, per every real decision | No |
| Create proposal | Not addressed | Algorithmic (`select_candidates()`), not human-initiated today | No |
| Approve | Not addressed | Unauthenticated, any human, real | No new restriction proposed |
| Modify | Not addressed | Unauthenticated, real (`edit`) | No new restriction proposed |
| Retire | Not addressed | Partial precedent (`reject`, never on an Active entity) | No |

This document introduces no ownership rule beyond what the ratified Domain Model already states or what real code already demonstrates, per the phase's explicit constraint.
