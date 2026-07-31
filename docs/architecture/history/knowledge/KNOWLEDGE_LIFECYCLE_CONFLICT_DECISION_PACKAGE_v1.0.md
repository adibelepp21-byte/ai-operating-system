# Knowledge Lifecycle & Conflict — Architect Decision Package v1.0

**Status:** Integrated architecture review and decision preparation only. No code, schema, API, storage design, or governance-document change occurs here.
**Version:** v1.0
**Authority:** Reviews `KNOWLEDGE_LIFECYCLE_CONFLICT_REVIEW_v1.0.md` as one system against the ratified Canonical Domain Model, Constitution, and proven Execution Layer patterns — not section by section.
**Evidence tags**: **[E]** evidence-backed, **[A]** assumption requiring validation, **[O]** open question.

---

## Integration Finding (read before the per-area analysis below)

Evaluating the prior review as one system, rather than five independent sections, surfaces one material tension the section-by-section review did not catch, because no single section's scope included it:

**The approved Ownership Model ("Home Department = accountability ownership") and Domain Model §8 ("Substrate entities [including Knowledge] are cross-cutting and addressable from any point in the Spine or Execution layer — they are not owned by, or private to, any single Department, Capability, or Agent") are not obviously reconciled anywhere in the approved decisions or the prior review.**

[E] Both statements are real, ratified/approved text — this is not a fabricated conflict. [A] A plausible reconciliation exists: "Home Department" could mean accountability/stewardship (who reviews, revises, and answers for an item) without meaning access-restriction (who may read or consume it) — the same distinction an accountable document owner has in many real organizations without gatekeeping readership. [O] But this reconciliation is *assumed* here, not stated anywhere in the approved Ownership Model's own condition text, which only says "Home Department = accountability ownership" without addressing access. This finding affects Decision Area 2 and Decision Area 4 below and is treated as a new, standalone risk in §4 of this package. It does not reopen the approved decision — it identifies a clarification the approved decision needs.

---

## Decision Area 1 — Knowledge Lifecycle Model

**Adopt.**

**Architectural reasoning**: append-only-versioned with a stable identity is not a new invention layered onto this system — it is the direct extension of two already-proven, already-real patterns: Trace's append-only immutability (540 real records, zero mutations across this arc's entire history) and the Human Review `edit` decision's preserve-original behavior (1 real event, `trace-502ab65e9b0f`, where original content and correction coexist permanently). Evaluated as a system with the approved Admission Model (Option B), this lifecycle gives Option B's "create" step an unambiguous target: a new Knowledge identity's first version.

**Hidden consequences identified by integrated review**:
- **Supersession vs. conflict must be kept structurally distinct.** The lifecycle model's "supersession" (a new version of the *same* identity replacing an old one) and the conflict model's "two Knowledge items may coexist while conflicting" (Decision Area 3, necessarily *different* identities, since they disagree) are two different relationships. Reviewed independently, both read as reasonable; reviewed together, an implementer could plausibly conflate "supersede" and "resolve a conflict by picking a winner" as the same mechanism. They are not — supersession operates within one identity's version chain; conflict resolution operates *between* identities. [O] This distinction is not explicit anywhere in the prior review and should be made explicit before implementation.

**Comparison against Trace immutability and Memory expiration**:
[E] Knowledge's lifecycle sits architecturally between the two: it shares Trace's immutability-of-the-past (nothing already written is ever altered) but rejects Memory's automatic expiration (Knowledge is durable by ratified definition, Memory is deliberately provisional). This is not a contradiction — it is evidence that Knowledge correctly requires a lifecycle philosophy distinct from both of its structural neighbors, not a copy of either.

### Focus Questions

1. **Does stable identity across versions correctly fit the Canonical Domain Model?** [E] Yes. Domain Model §6's "versioned" language for Knowledge presupposes one identity with multiple versions — nothing in the ratified model forbids this, and it introduces no new entity (satisfying every phase's standing "no new entities" constraint).
2. **Does append-only-versioning preserve DM §6 requirements?** [E] Yes, directly — "revised/superseded via review; not casually deleted" is satisfied literally: revision and supersession are explicit, human-reviewed acts (per the approved Admission Model), and nothing is ever deleted.
3. **Are provenance rules sufficient for future revisions?** [A] Provisionally yes, per Decision Area 2 below — but only once the Home Department reassignment mechanism (a new record, not an edit) is confirmed to apply equally to *every* provenance-adjacent change, not just ownership reassignment specifically. Not fully evidenced yet.
4. **What lifecycle states are genuinely required versus premature design?** [E]/[O] Candidate, Admitted, Active are evidence-backed as necessary (they map directly to already-proven real mechanisms). Revision Required, Deprecated, Superseded are architecture-required in principle (Domain Model §6) but their exact boundaries remain undesigned. Archived is **premature** — introduced by a recent directive with no Domain Model text distinguishing it from Deprecated; recommend treating "Archived" as *not* a genuinely required distinct state until evidence shows Deprecated is insufficient.

---

## Decision Area 2 — Provenance Permanence Model

**Adopt, with one clarification required (see Integration Finding).**

**Validation against DM §5 (ownership)**: [E] consistent — §5's "each item has a home Department" is satisfied by the Home Department field; the approved condition's Reviewer ≠ owner rule is *additional* precision §5 doesn't itself specify but doesn't contradict either.

**Validation against DM §6 (audit requirements)**: [E] fully consistent — "not casually deleted... audit trail matters" is satisfied exactly by treating every provenance element as permanent except Home Department, which is reassignable only via a new, explicit, permanently-retained record (never an edit to the old one) — this preserves full history of every past assignment, satisfying the audit requirement more strongly than a simple mutable field would.

**Relationship between provenance and ownership**: [E] cleanly separated by the approved condition itself: Originating Department is provenance (a historical fact about where something came from, akin to `agent_definition_name` in existing `Provenance` records); Home Department is ownership (a current, reassignable accountability assignment). This separation is a real strength of the approved model, not a gap.

**Additional immutable provenance elements required?** [O] One candidate, newly surfaced: the identity/rationale of whoever performs a Home Department *reassignment* should itself be a permanent, attributed record (mirroring `reviewer_identity`'s proven pattern) — not explicitly stated in the approved condition, but implied by "must remain an explicit reviewed decision." Recommend treating this as a clarification of the existing approved model, not a new decision.

---

## Decision Area 3 — Conflict Resolution Philosophy

**Adopt** (all three Adopt items); **Reject** (all three Reject items) — confirmed, not merely restated.

**Validation against Trace explainability invariant** (Domain Model §6.1, "Trace's explainability never depends on the continued existence of any Memory or Knowledge item it cites"): [E] "conflicts never silently resolved" and "conflict evidence remains preserved" both directly reinforce this invariant — a silently resolved conflict would destroy exactly the explainability §6.1 guarantees. Adoption here isn't just compatible with this invariant, it is required by it.

**Validation against Knowledge's reviewed/canonical definition**: [E] "similarity score deciding truth," "confidence automatically overriding conflict," and "Memory overriding Knowledge" all fail the same test: none involves governed human review, and Knowledge is defined (Domain Model §2, invariant 8) as existing only through governed review. Rejecting all three is not a judgment call — it follows directly from the ratified definition.

**Validation against the human judgment boundary**: [E] every rejected pattern would introduce exactly the kind of automated governance decision this entire arc has structurally forbidden (AST-proven absent from `review_decision.py` across every phase). Adopting any of them would be the first violation of that boundary in this system's history. **Reject** confirmed with maximum confidence.

---

## Decision Area 4 — Conflict Resolution Ownership

**Home Department as first-line authority: Adapt** (plausible, but needs the Integration Finding's clarification before being finalized).
**Cross-Department escalation via invariant-10 analogy: Reject as currently framed — remains Open.**

**Is the invariant-10 analogy architecturally valid?** [E] No, not as a direct analogy, and this integrated review is where that becomes visible. Invariant 10 ("Cross-Department Capability dependencies require governance approval... never silent adoption") governs a **Spine-layer, intentional, designed dependency relationship between Capabilities**. A Knowledge conflict is an **unplanned, discovered-after-the-fact disagreement between Substrate-layer content items**. These are structurally different kinds of cross-Department relationships — the invariant's purpose (preventing silent, undocumented coupling) partially overlaps in spirit, but its literal scope is Capabilities, not Knowledge. Applying it here would be exactly the "silent extension of a governance principle" this directive explicitly warns against.

**Compounding this**: Domain Model §8 explicitly states Knowledge is "not owned by, or private to, any single Department" — which sits in tension with treating conflict-resolution authority as something that needs *escalation across* Department boundaries at all. If Knowledge is genuinely not siloed by Department, the entire premise of "cross-Department escalation" may need to be framed differently than the Capability-dependency model invariant 10 addresses.

**Does Knowledge require a separate ownership escalation rule?** [O] Likely yes, but this review does not have evidence to design one. **This should remain explicitly open**, not resolved by analogy, per the directive's own instruction.

---

## Decision Area 5 — Remaining Open Questions, Classified

| # | Question | Classification | Reasoning |
|---|---|---|---|
| 1 | Revision Required trigger | **Must Resolve Before Implementation** | High blast radius (affects every Knowledge item's core lifecycle correctness); zero real evidence exists to calibrate against; deciding wrong after real Knowledge exists would require a governance-level correction, not just a code fix |
| 2 | Archived vs. Deprecated distinction | **Resolve During Implementation** | Low blast radius (affects a state label only); append-only design means this can be refined later without corrupting anything already recorded |
| 3 | Conflict evidence threshold | **Resolve During Implementation** | The structural mechanism (detect, never auto-resolve) is already Adopted and does not depend on the exact threshold value; calibration is an implementation-tier decision, not architecture-tier |
| 4 | Cross-Department escalation authority | **Must Resolve Before Implementation** | High blast radius (governance authority itself); this review found the current framing (invariant-10 analogy) invalid, and the underlying tension with Domain Model §8 must be clarified before any conflict-resolution code is written, or real decisions could be made under an authority model later found unratified |
| 5 | Snapshot mechanics | **Safe to Defer** | The architectural principle (capture, don't reference — reusing `candidate_snapshot`'s proven shape) is already Adopted; only field-level detail remains, which is ordinary implementation-tier work |
| 6 | Revision signal vs. executed Revision boundary | **Resolve During Implementation** | Medium blast radius, but append-only design means a wrong boundary is a code correction, not a data-integrity or governance problem |

---

## 1. Architecture Decision Summary

| Decision | Recommendation | Status | Reason |
|---|---|---|---|
| Append-only-versioned lifecycle with stable identity | Adopt | **Confirmed** | Direct extension of two already-proven real patterns (Trace, `edit` decision) |
| Provenance permanence (Originating Dept / Reviewing Actor permanent; Home Dept reassignable via new record) | Adopt | **Confirmed, with clarification needed** | Consistent with DM §5/§6; needs explicit reconciliation with DM §8 (see Integration Finding) |
| Conflicts never silently resolved; evidence preserved; escalation via existing Decision-Making Process | Adopt | **Confirmed** | Required by DM §6.1 and invariant 8, not merely compatible with them |
| Similarity/confidence deciding conflict outcome; Memory overriding Knowledge | Reject | **Confirmed** | Would violate the proven, AST-verified human-judgment boundary |
| Home Department as conflict-resolution authority | Adapt | **Pending clarification** | Plausible but must be reconciled with DM §8's "not owned by... any single Department" framing |
| Cross-Department escalation via invariant-10 analogy | Reject as framed | **Remains Open** | Invariant 10 is literally scoped to Capability dependencies; extending it silently is exactly what this review was told not to do |

## 2. Adoption Classification

| Pattern | Adopt / Adapt / Reject | Explanation |
|---|---|---|
| Event-sourced, append-only Knowledge lifecycle | **Adopt** | Direct reuse of Trace's proven architecture |
| Stable versioned identity | **Adapt** | Genuinely new relative to this codebase (Memory deliberately lacks this); extends a proven base, not a proven exact pattern |
| Provenance permanence table | **Adopt** | Directly derived from the approved Ownership Model's own condition |
| Conflict surfacing (never silent resolution) | **Adopt** | Reuses `detect_conflicts()`'s proven real behavior |
| Automated/scored conflict resolution | **Reject** | Contradicts the human-judgment boundary this entire arc has structurally proven |
| Home-Department-scoped conflict authority | **Adapt** | Needs the DM §8 reconciliation before being finalized |
| Invariant-10-analogy cross-Department escalation | **Reject (as framed)** | Scope mismatch — Capability dependency vs. Substrate content conflict |
| Knowledge graph readiness | **Defer** | No evidence of need yet (unchanged from the prior review) |

## 3. Implementation Readiness Impact

**PARTIALLY READY.**

The lifecycle and conflict architecture, evaluated as an integrated system, is coherent and well-grounded for everything **except** the ownership/escalation boundary — which this integrated review found to contain an unresolved tension with ratified Domain Model text (§8) that the section-by-section review did not surface. Repository implementation planning can reasonably begin for the lifecycle model and the conflict-surfacing mechanism (both cleanly Adopted, both grounded in proven real patterns) but **should not begin for anything touching conflict-resolution authority or cross-Department escalation** until the DM §8 reconciliation is explicit and the invariant-10 analogy is either replaced with a properly-scoped rule or the Architect explicitly ratifies extending it.

## 4. New Risks Discovered

**Risk 1 — Ownership/access ambiguity.**
- **Cause**: the approved Ownership Model's "Home Department = accountability ownership" is not explicitly reconciled with Domain Model §8's "not owned by, or private to, any single Department."
- **Likelihood**: certain to surface during implementation if not clarified now — any code enforcing Department-scoped access control on Knowledge would directly contradict §8.
- **Impact**: high — could require reversing an access-control implementation after real Knowledge exists, a costly migration given the append-only, immutable design philosophy.
- **Mitigation**: obtain explicit Architect confirmation that "Home Department" means accountability/stewardship only, never access restriction, before any retrieval or access-control design begins.

**Risk 2 — Supersession/conflict conflation.**
- **Cause**: both relationships ("new version supersedes old version of the same identity" vs. "two different identities coexist in conflict") were designed in separate sections of the prior review without an explicit statement that they are structurally distinct.
- **Likelihood**: moderate — a natural implementation shortcut would be to model both as "one Knowledge item points to another," which would conflate them.
- **Impact**: medium — would corrupt the meaning of the version chain if conflated, though append-only design limits permanent damage (a fix would still require a new corrective record, not data loss).
- **Mitigation**: state explicitly, in any future lifecycle contract document, that supersession is intra-identity and conflict is inter-identity, with no shared mechanism.

**Risk 3 — Cross-Department escalation authority vacuum.**
- **Cause**: this review rejects the only concrete proposal that existed (invariant-10 analogy) without a replacement.
- **Likelihood**: certain to matter the first time a real cross-Department conflict occurs.
- **Impact**: medium in the near term (no real conflict has ever occurred in this system's history, per every prior evidence-gathering phase), but high whenever it eventually does, since no authority model would exist to invoke.
- **Mitigation**: treat this as a standing, explicitly tracked open item requiring its own future decision phase, not something to improvise if and when a real conflict occurs.

## 5. Architect Approval Checklist

Only decisions requiring explicit Architect authorization before the next phase:

1. **Clarify whether "Home Department = accountability ownership" restricts access, or is stewardship-only with organization-wide access preserved per Domain Model §8.** (Blocks: conflict-resolution authority design, any future retrieval/access design.)
2. **Confirm or reject treating the versioned-identity lifecycle model (Decision Area 1) as authorized architecture to design against**, given it is the one genuinely new pattern this arc has proposed with no direct precedent.
3. **Confirm the invariant-10 analogy is rejected as a cross-Department escalation mechanism**, and decide whether to authorize a dedicated future phase to design a properly-scoped replacement, or leave it explicitly deferred.
4. **Confirm "Archived" is not a required distinct lifecycle state** (this review recommends treating it as premature, absorbed into Deprecated, pending evidence otherwise).

No implementation, schema, contract, or governance-document action follows automatically from this package. Stopping here. Awaiting Architect authorization on the items above before any further phase.
