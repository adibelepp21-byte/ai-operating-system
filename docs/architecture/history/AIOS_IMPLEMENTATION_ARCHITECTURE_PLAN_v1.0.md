# AIOS Implementation Architecture Plan v1.0

**Status:** Implementation Architecture Planning — the bridge from the Canonical Architecture phase to the Engineering phase. Planning only: no code, schema, API, database design, class design, implementation proposal, or pseudocode.
**Version:** v1.0
**Authority basis:** Blueprint v3 (canonical Knowledge architecture), Principles Register PR-1…PR-5, Canonical Domain Model (invariants 1–15), Constitution, the frozen Execution Layer v1.0 baseline, and the Canonical Ratification Review's minimum-set finding. Every subsystem below is justified by one of these; none is invented.
**Confidence discipline:** **[E]** evidenced · **[A]** assumption · **[O]** open question.

---

## 0. The Single Most Important Planning Fact

[E] **AIOS is not a greenfield.** Roughly half the subsystems the directive lists **already exist, are implemented, tested, and frozen at v1.0** (the Execution Layer: Trace, Memory, Promotion, Human Review, Evidence Verification, Snapshot, Provenance, Authority Enforcement, Validation — 288/288 + 20/20 tests, 540 real Trace records). The remaining subsystems (Knowledge Repository, Admission, Knowledge Service, Retrieval, Query Layer) are **architected in Blueprint v3 but not implemented**. This plan's central job is therefore **integration and extension, not construction from zero** — which directly serves the reuse-maximizing mandate. Every planning decision below distinguishes **[BUILT]** (frozen, reuse as-is), **[ARCHITECTED]** (Blueprint v3 settled, ready to plan detailed design), and **[OPEN]** (architecture has an unresolved question blocking it).

---

## 1. Subsystem Inventory (justified by canonical architecture only)

| Subsystem | Status | Governing canonical document(s) | Justification |
|---|---|---|---|
| Trace Integration | **[BUILT]** | Domain Model inv. 4–6; `trace.py` | Frozen v1.0; the audit spine |
| Provenance Services | **[BUILT]** | PR-5; Domain Model §6.1; `promotion.py` provenance | Chain proven end-to-end |
| Snapshot Management | **[BUILT]** | PR-5; `review_decision.py` `candidate_snapshot` | Capture-don't-reference, proven |
| Validation Layer | **[BUILT]** | PR-4; `review_decision.validate_decision_input` | Fail-closed, proven |
| Authority Enforcement | **[BUILT]** | PR-11 pattern; Constitution §6.2; `orchestrator.py` | Permitted-Skill/Workflow checks + escalation Trace |
| Promotion | **[BUILT]** | Domain Model inv. 8; `promotion.py` | Candidate selection, read-only, proven |
| Human Review Services | **[BUILT]** | Domain Model inv. 8; PR-3; `review_decision.py` | 6 real decisions, all 3 types |
| Evidence Verification | **[BUILT]** | PR-4; `verification.py` (Tier 2) | Drift-tested, one defect found & fixed |
| Memory Governance | **[BUILT]** | PR-2; `memory_governance.py` | review_state/trust/conflict detection |
| Knowledge Repository | **[ARCHITECTED]** | Blueprint v3 §2.1, Decision 4 | Append-only versioned store; version-addressing settled (Decision 1) |
| Knowledge Admission | **[ARCHITECTED]** | Blueprint v3 §2.9, Decision 10 | Separate admission decision on Human Review infra |
| Knowledge Service | **[ARCHITECTED]** | Blueprint v3 §2.1–§2.7 | The lifecycle/validity/ownership operations over versions |
| Governance Services (validity/invalidation/reassignment) | **[ARCHITECTED, partly OPEN]** | Blueprint v3 §2.3–§2.6 | Admission ready; Revision trigger (#1) and validity-effect (#8) OPEN |
| Retrieval | **[OPEN]** | Blueprint v3 §2.8 | Two-dimension consequence documented; visibility policy (#6) unresolved |
| Query Layer | **[OPEN]** | Blueprint v3 §2.8 | Depends entirely on Retrieval's open policy |
| Runtime Integration | **[BUILT]** | Domain Model §2; `runtime.py` | Binding proven; extension needed only if Knowledge consumption is wired |
| Conflict Resolution | **[OPEN]** | Blueprint v3 §2.7 | Detection built; resolution never designed; cross-Dept escalation deferred |

Subsystems the directive listed that are **not** separate subsystems here, with justification: "Governance Services" is not one subsystem but a family (admission/validity/reassignment operations) — split above to keep readiness honest. No subsystem was invented; "Query Layer" and "Retrieval" are kept distinct because Blueprint v3 §2.8 treats retrieval-of-content and evaluation-of-two-dimensions as separable concerns.

## 2. Per-Subsystem Detail (the [ARCHITECTED] and [OPEN] set — the actual planning surface)

The [BUILT] subsystems need no planning beyond "reuse as-is"; detail below covers only what must be *built*.

### Knowledge Repository [ARCHITECTED]
- **Purpose:** durable, append-only, versioned store of Knowledge Versions.
- **Canonical responsibilities:** persist immutable versions; correlate versions by stable identity key; never mutate or delete (Decision 4, PR-5, inv. 5-analogue).
- **Dependencies:** Trace Integration [BUILT] (every write produces a Trace record, inv. 4); Snapshot Management [BUILT]; Provenance Services [BUILT].
- **Required architectural inputs:** the version-addressing model (Decision 1 — settled); the provenance permanence table (Blueprint v3 §2.5 — settled).
- **Expected outputs:** addressable, immutable version records; a resolvable identity→versions correlation.
- **Governed by:** Blueprint v3 §2.1/Decision 1/Decision 4; Domain Model §6.
- **Blocked by open question?** **No.** Version-addressing (the former blocker) is settled. **Ready for detailed design.**

### Knowledge Admission [ARCHITECTED]
- **Purpose:** the governed decision that creates a Knowledge identity's first version.
- **Canonical responsibilities:** a separate admission decision layered on Human Review infrastructure (Decision 10); produces Active + Confirmed first version; captures full snapshot + provenance.
- **Dependencies:** Human Review Services [BUILT]; Knowledge Repository [ARCHITECTED]; Promotion [BUILT].
- **Required inputs:** the approved admission model (Option B — settled); the ownership assignment mechanism (Ownership Model Option C, `department_override` field — [BUILT], unused).
- **Expected outputs:** a first Knowledge Version; an admission Trace record.
- **Governed by:** Blueprint v3 §2.9, Decision 10; Domain Model inv. 8.
- **Blocked by open question?** **No** for the admission act itself. **Ready for detailed design**, sequenced after Repository.

### Knowledge Service [ARCHITECTED]
- **Purpose:** the operations that read/derive Knowledge state (current version, validity, ownership) from the version records — the read-side of PR-5's correlation model.
- **Canonical responsibilities:** resolve identity→current-Active-version; expose lifecycle position and validity condition as two independent axes (PR-2); never store derived state authoritatively (mirrors Memory's recompute-don't-store).
- **Dependencies:** Knowledge Repository [ARCHITECTED].
- **Governed by:** Blueprint v3 §2.1–§2.3.
- **Blocked?** **No** for read/derive of Active+Confirmed state. **Ready** after Repository + Admission.

### Governance Services — Validity / Invalidation / Reassignment [ARCHITECTED, partly OPEN]
- **Purpose:** the governed transitions on existing versions (Confirmed↔Questioned↔Invalidated; Home Department reassignment).
- **Canonical responsibilities:** each transition = a governed human decision + Trace record (PR-3, inv. 4); invalidation authority = Human Reviewer under Home Department (Blueprint v3 §2.6); automation may propose Questioned, never set it (PR-3).
- **Blocked by open question?** **Partially.** Invalidation and reassignment are settled and buildable. **The Questioned-transition trigger (#1) and the detection-vs-confirmation effect (#8) are OPEN** — the *proposing* path can be planned, but the *effecting* rule cannot be detailed-designed until #8 resolves.

### Retrieval [OPEN]
- **Purpose:** find and return Knowledge relevant to a query, evaluating two dimensions (lifecycle, validity).
- **Blocked by open question?** **Yes — #6 (default visibility policy).** The *mechanism* (two-axis evaluation) is architected; the *policy* (which lifecycle/validity states appear by default) is explicitly unresolved. **Not ready for detailed design.** [E] Also: the only existing Retrieval code (`execution/knowledge/retrieval.py`) is a dormant document-search prototype with zero real Knowledge consumers — not a foundation, a placeholder.

### Query Layer [OPEN]
- Depends entirely on Retrieval; inherits its block. **Not ready.**

### Conflict Resolution [OPEN]
- Detection [BUILT]; resolution never designed; cross-Department escalation authority explicitly deferred (invariant-10 analogy rejected). **Not ready; not on the critical path** — a first, conflict-free Knowledge pipeline can operate without it (zero organic conflicts have ever occurred).

## 3. Implementation Dependency Graph

```
FOUNDATION [BUILT — reuse as-is, no work]
  Trace · Provenance · Snapshot · Validation · Authority Enforcement
        │
        ▼
CORE INFRASTRUCTURE [BUILT — reuse as-is]
  Memory · Memory Governance · Promotion · Human Review · Evidence Verification · Runtime
        │
        ▼
KNOWLEDGE INFRASTRUCTURE [ARCHITECTED — first real build target]
  Knowledge Repository ──► Knowledge Admission ──► Knowledge Service
        │
        ▼
GOVERNANCE INFRASTRUCTURE [ARCHITECTED, partly OPEN]
  Validity/Invalidation/Reassignment  (invalidation+reassignment ready;
                                        Questioned-transition OPEN on #1/#8)
        │
        ▼
EXECUTION INFRASTRUCTURE [OPEN]
  Retrieval (blocked on #6) ──► Query Layer (inherits block)
        │
        ▼
INTEGRATION
  Runtime↔Knowledge consumption wiring (knowledge_consumed currently empty on all 540 records)
        │
        ▼
OPERATIONAL READINESS
  Conflict Resolution (deferred) + full lifecycle exercised end-to-end with real usage
```

[E] **The graph is acyclic and its lower two-thirds already exist.** The genuine build frontier is exactly one layer: Knowledge Infrastructure (Repository → Admission → Service), all three [ARCHITECTED] and unblocked.

## 4. Implementation Readiness Assessment

| Subsystem | Readiness | Evidence |
|---|---|---|
| Trace, Provenance, Snapshot, Validation, Authority, Memory, Memory Governance, Promotion, Human Review, Evidence Verification, Runtime | **READY (already built)** | [E] Frozen v1.0, 288+20 tests passing, 540 real records |
| Knowledge Repository | **READY (for detailed design)** | [E] Version-addressing settled (Decision 1); all dependencies [BUILT] |
| Knowledge Admission | **READY (for detailed design)** | [E] Model settled (Option B); reuses Human Review infra; ownership field exists |
| Knowledge Service | **READY (for detailed design)** | [E] Read/derive of Active+Confirmed state fully specified (PR-2, Blueprint §2.1–2.3) |
| Governance: Invalidation, Reassignment | **PARTIALLY READY** | [E] Authority settled (§2.6); buildable — but naturally sequenced after Service exists |
| Governance: Questioned-transition | **BLOCKED** | [O] Open questions #1 (trigger) and #8 (effect timing) unresolved |
| Retrieval | **BLOCKED** | [O] Open question #6 (visibility policy); [E] no real foundation exists |
| Query Layer | **BLOCKED** | [E] Inherits Retrieval's block |
| Conflict Resolution | **BLOCKED (and deferred)** | [E] Never designed; cross-Dept escalation deferred; off critical path |
| Runtime↔Knowledge integration | **PARTIALLY READY** | [E] Runtime built; wiring waits on Knowledge Service existing to consume |

## 5. Recommended Implementation Sequence (minimize risk, maximize reuse)

Ordered so each step depends only on [BUILT] or already-sequenced [ARCHITECTED] subsystems, and each unblocked step precedes any blocked one:

1. **Knowledge Repository** — the foundation of everything Knowledge; unblocked; maximal reuse of Trace/Snapshot/Provenance [BUILT]. Lowest risk (append-only, a pattern proven at 540-record scale).
2. **Knowledge Admission** — reuses Human Review infrastructure almost wholesale; produces the first real Knowledge Version, which is the first real evidence the whole architecture actually works end-to-end.
3. **Knowledge Service (read/derive)** — makes admitted Knowledge usable; no new governance surface.
4. **Governance: Invalidation + Reassignment** — the settled subset of governance operations; adds the validity axis's decided transitions.
5. **[GATE] Resolve open question #1 (Revision/Questioned trigger) and #8 (effect timing)** — an *architecture decision*, not implementation; must precede any Questioned-transition build.
6. **Governance: Questioned-transition** — only after step 5's gate.
7. **[GATE] Resolve open question #6 (Retrieval visibility policy)** — architecture decision.
8. **Retrieval → Query Layer** — only after step 7.
9. **Runtime↔Knowledge integration** — wire real Knowledge consumption (first non-empty `knowledge_consumed`).
10. **Conflict Resolution** — last, deferred, off critical path until a real conflict or explicit authorization.

[E] **Risk-minimizing property:** steps 1–4 require *zero* new architecture decisions — they build only settled architecture on [BUILT] foundations. The first architecture gate (step 5) does not block the first four builds, so real implementation evidence accrues *before* any remaining open question must be answered — exactly the Evidence First principle (PR-1) applied to sequencing.

## 6. Explicit Phase Distinction

The directive requires these never be mixed. This document is **exactly one** of them:

| Phase | Definition | This document? | Where it lives |
|---|---|---|---|
| **Architecture Decisions** | What must be true (invariants, principles, settled models) | Cites, does not make | Constitution, Domain Model, Principles Register, Blueprint v3, ADRs |
| **Implementation Planning** | Which subsystems, what order, what readiness | **← THIS DOCUMENT** | This plan |
| **Detailed Design** | How a subsystem is structured (schema, class, API) | **Explicitly excluded** | Future, per-subsystem, post-authorization |
| **Implementation** | Writing the code | Excluded | Future |
| **Testing** | Verifying behavior | Excluded | Future |

[E] This plan names *no* schema, class, API, or code — it stops precisely at the Planning/Design boundary, per the constraints.

## 7. Consistency Review — Roadmap vs. Canonical Architecture

Verifying the roadmap violates no principle, invariant, or Constitution rule:

- [E] **Domain Model invariant 4 (one action → one Trace record):** every planned build step's operations (admission, validity transition, reassignment) are specified to produce Trace records; the sequence never introduces an untraced action. **No violation.**
- [E] **Invariant 5 (Trace immutable/append-only):** the Repository is planned as append-only versioned (Decision 4); no step mutates Trace. **No violation.**
- [E] **Invariant 8 (Memory→Knowledge only via governed review):** admission (step 2) is a governed human decision; no step automates promotion into Knowledge. **No violation.**
- [E] **PR-1 Evidence First:** the sequence deliberately front-loads the four unblocked builds so real evidence precedes the open-question gates — the roadmap *embodies* the principle rather than merely complying with it. **No violation.**
- [E] **PR-2 State/Condition Separation:** Knowledge Service and Governance are planned as two independent axes (lifecycle, validity); no step collapses them. **No violation.**
- [E] **PR-3 Detect, Don't Decide:** the Questioned-transition is explicitly gated (step 5/6) precisely because automation may only propose it; no step lets automation set a governance condition. **No violation.**
- [E] **PR-4 Fail Closed:** the Validation Layer [BUILT] is reused ahead of every write; no step introduces a trust-by-default path. **No violation.**
- [E] **PR-5 Capture, Don't Reference:** Repository and Admission reuse Snapshot Management; provenance is captured, not referenced. **No violation.**
- [E] **Constitution §6.2 invariant 2 (automation may not override governance authority):** every governance transition in the roadmap is human-decided; the gates at steps 5 and 7 are *architecture decisions reserved to the Architect*, not automated. **No violation.**
- [E] **Ownership reconciliation (Blueprint v3 §2.6, DM §8):** the roadmap treats Home Department as accountability-only; no step introduces Department-scoped access control. **No violation.**
- [O] **One honest caveat:** steps 5–8 depend on architecture decisions (#1, #6, #8) not yet made — the roadmap does not *violate* them, but it *cannot be completed* without them. This is correctly represented as gates, not as buildable steps. The roadmap is complete and consistent *up to* those gates.

**Consistency verdict [E]:** the roadmap violates no invariant, principle, or Constitution rule. Its blocked portions are honestly gated behind the exact open architecture decisions that must precede them, and its unblocked portion (steps 1–4) is fully consistent and buildable today.

---

## Summary for the Architect

[E] The genuine implementation frontier is **one layer — Knowledge Infrastructure (Repository → Admission → Service)** — all [ARCHITECTED], all unblocked, all building on a frozen, tested foundation. Four implementation steps require **zero new architecture decisions**; the remaining steps are honestly gated behind three open architecture questions (#1, #6, #8) that this plan does not resolve and does not need to resolve to begin. The recommended next action, when the Architect authorizes it, is **Detailed Design of the Knowledge Repository** — the single lowest-risk, highest-reuse, fully-unblocked build target.

No code, schema, API, database, class, or pseudocode was produced. No implementation was begun. No ratified decision was reopened. This is the bridge document; the far side of the bridge awaits explicit Architect authorization.
