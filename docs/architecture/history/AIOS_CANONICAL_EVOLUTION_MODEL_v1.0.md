# AIOS Canonical Evolution Model v1.0

**Status:** Generalization of the content-evolution lifecycle discovered during the Knowledge Architecture arc into a reusable AIOS model. Analysis only — describes a pattern, mandates no implementation.
**Version:** v1.0
**Authority:** Subordinate to the Canonical Domain Model and Constitution. Extracted from Blueprint v3 and the real Execution Layer; generalized only where evidence supports it, per the Evidence First principle.
**Confidence tags:** **[E]** evidence-backed, **[A]** assumption requiring validation, **[O]** open question.

---

## Scope and Honesty Note

[E] This model generalizes how **content earns, holds, and loses trusted status** in AIOS. The full pipeline is proven end-to-end only up to the Review stage (real: 540 Trace records → 370 Memories → 368 candidates → 6 real decisions); the Canonical/Revision/Retraction stages are settled *architecture* (Blueprint v3) with zero real instances yet. [A] Its applicability to non-content subsystems (Workflow definitions, Agent Definitions, Capabilities) is a structural argument, not yet demonstrated — stated per stage below, never assumed silently. The model deliberately does **not** claim every AIOS subsystem must use every stage.

## The Model

```
Observation → Aggregation → Candidate → Review → Canonical → Revision ⟲
                                            │         │
                                            ▼         ▼
                                        Declined   Historical (Superseded)
                                                      │
                                        (orthogonal) Retraction = validity event,
                                                      not a stage
```

A deliberate departure from the directive's example stage list: **Retraction is not a stage.** Modeling it as one would violate the State/Condition Separation Principle this same arc established — retraction is a validity event that can strike a Canonical item at any time, not a position in the sequence. Similarly, "Replacement" is not a distinct stage: it is Revision viewed from the successor's side. The model keeps the stage list minimal on evidence, not maximal on symmetry.

---

## Stage 1 — Observation

- **Purpose:** Capture what actually happened or was actually encountered, raw, at execution time.
- **Entry criteria:** A real execution produced a finding. Nothing else — observation is unconditional where Trace is involved (invariant 4).
- **Exit criteria:** None required — most observations correctly never go anywhere further. Progression is the exception, not the rule ([E]: 540 records → only 6 ever reached a decision).
- **Ownership:** None (Trace is owned by no one — Domain Model §5).
- **Lifecycle transitions:** None — an observation is an immutable event, not a stateful entity.
- **Typical Trace events:** The action record itself, carrying `outputs.evidence`.
- **Relationship to Memory:** Source material.
- **Relationship to Knowledge:** Ancestral only — several stages removed, never direct (invariant 8).
- **Future subsystems:** [E] Universal — every subsystem already produces observations via Trace, today.

## Stage 2 — Aggregation

- **Purpose:** Derive reusable, deduplicated signals from many observations (Memory, in the proven instance).
- **Entry criteria:** Recurring or extractable structure across observations.
- **Exit criteria:** Selection as a Candidate — or expiry (the aggregation layer is deliberately provisional and retention-bounded).
- **Ownership:** Scoped to the producing instance/layer; deliberately no stable identity ([E]: `memory_id` regenerates — a feature at this stage, since nothing durable should attach here).
- **Lifecycle transitions:** Fresh → stale (computed, time-based) — the only stage where automatic, time-based decay is legitimate, because nothing here is governed content yet.
- **Typical Trace events:** None of its own — aggregation is recomputed, not acted.
- **Relationship to Memory:** This *is* Memory's stage in the proven instance.
- **Relationship to Knowledge:** Feeds candidate selection; never skips ahead.
- **Future subsystems:** [A] Applies where a subsystem accumulates experience (e.g. Workflow execution statistics); not obviously applicable to purely-authored artifacts (a Capability contract is written, not aggregated) — the model does not force this stage on them.

## Stage 3 — Candidate

- **Purpose:** Identify which aggregated content merits scarce human attention, ranked but never gated by quality signals (P13).
- **Entry criteria:** Passes structural eligibility only (non-degeneracy) — never a confidence threshold.
- **Exit criteria:** Presented for Review, or simply recomputed away (candidates are stateless projections).
- **Ownership:** None — selection is a pure, read-only computation ([E]: `select_candidates()`).
- **Lifecycle transitions:** None — a candidate is a projection, not a stored entity.
- **Typical Trace events:** None for selection itself (read-only); the *presentation* to a reviewer may be recorded.
- **Relationship to Memory:** A ranked view over it, with provenance reconstructed.
- **Relationship to Knowledge:** The admission pipeline's input.
- **Future subsystems:** [A] Any subsystem with more raw material than review capacity — plausibly universal wherever Stage 2 exists.

## Stage 4 — Review

- **Purpose:** The governed human decision — the only gate through which content changes trust tier (invariant 8; P3, P9).
- **Entry criteria:** A candidate plus an explicit human engagement; all required decision fields human-supplied, placeholders rejected, fail-closed validation.
- **Exit criteria:** A recorded decision: approve / reject / edit (proven), and — for entities with an admission tier — the separate admission decision (settled, unexercised).
- **Ownership:** The reviewer owns the *decision* accountability (attributed, permanent); never the content (Reviewer ≠ owner).
- **Lifecycle transitions:** Candidate → Declined (terminal for that content, [E]: 1 real reject) or → Canonical (via admission).
- **Typical Trace events:** The proven 3-record shape (spawn / decision / terminate) with full snapshot capture.
- **Relationship to Memory:** Judges a snapshot of it; immune to its later drift ([E]: corpus-drift test).
- **Relationship to Knowledge:** The threshold of it.
- **Future subsystems:** [E] The mechanics are subsystem-agnostic already — the review contract judges a snapshot, whatever produced it.

## Stage 5 — Canonical

- **Purpose:** Durable, versioned, trusted status — the content is now a governed artifact (Knowledge's Active+Confirmed, in the settled instance).
- **Entry criteria:** An explicit admission decision (settled: separate from approval).
- **Exit criteria:** Revision (→ successor becomes Canonical, this version → Historical) — or, orthogonally, a validity event (Questioned/Invalidated) that changes trust *without* changing stage.
- **Ownership:** Collective (Organization) with a Home accountability point; cross-cutting access preserved (§8).
- **Lifecycle transitions:** Active → Superseded, only via governed Revision.
- **Typical Trace events:** Admission record; validity-transition records; ownership-reassignment records.
- **Relationship to Memory:** Decoupled — canonical content never depends on Memory's continued existence (capture-don't-reference).
- **Relationship to Knowledge:** This *is* Knowledge's stage in the settled instance.
- **Future subsystems:** [A] Structurally, Agent Definitions, Workflow definitions, and Capability contracts are *already* canonical-stage artifacts (versioned, governed, durable — Domain Model §6) that arrived without passing through Stages 1–3; the model accommodates authored-not-promoted entry, but this dual entry path is an observation, not yet a designed mechanism. [O] Whether authored artifacts should eventually adopt the same versioned-identity mechanics as Knowledge is open.

## Stage 6 — Revision (cyclic)

- **Purpose:** Controlled change of canonical content — a new version, never an edit.
- **Entry criteria:** A governed human decision to revise ([O]: the trigger — open question #1 — remains the model's single largest operational unknown, honestly carried here).
- **Exit criteria:** New version admitted (→ Canonical); prior version → Historical.
- **Ownership:** Unchanged by revision; reassignment is its own separate governed event.
- **Lifecycle transitions:** The only path that moves a Canonical version to Historical.
- **Typical Trace events:** Revision decision with snapshot of both the judged state and the new content.
- **Relationship to Memory:** New evidence (often via Memory) may *motivate* revision but never executes it (P9).
- **Relationship to Knowledge:** Settled architecture, zero real instances.
- **Future subsystems:** [E] Governance documents already revise through governed process (Constitution's own Amendment Process) — the pattern precedes Knowledge; Knowledge adds the versioned-identity mechanics.

## Stage 7 — Historical (Superseded)

- **Purpose:** Permanent, inspectable retention of no-longer-current versions — the audit trail's steady state.
- **Entry criteria:** Superseded by revision.
- **Exit criteria:** None — terminal by design ("not casually deleted").
- **Ownership:** Frozen as recorded; Home Department accountability persists for answerability about the past.
- **Lifecycle transitions:** None.
- **Typical Trace events:** None of its own — becoming Historical is a consequence recorded in the successor's revision event.
- **Relationship to Memory:** None remaining.
- **Relationship to Knowledge:** The version-chain's tail; [O] retrievability of Historical versions is the open Retrieval-visibility question (#6/#9).
- **Future subsystems:** [E] Trace already lives permanently in this posture; prior baseline documents are retained the same way (Evolution Protocol §8).

---

## Orthogonal Overlay: Validity (not a stage)

Confirmed / Questioned / Invalidated apply to Canonical-stage (and Historical) versions independently of stage position — including Retraction (Invalidated with no successor, stage unchanged). Automated detection may propose Questioned; only governed review sets any condition. This overlay is what keeps the stage model small: without it, every trust nuance would demand a new stage, which is precisely the failure the State/Condition Separation Principle exists to prevent.

## What This Model Does Not Claim

- [A] That every subsystem uses every stage (authored artifacts enter at Canonical; some observations never aggregate).
- [O] Whether the model applies to *behavioral* evolution (e.g., an Agent Definition's capability drift) as opposed to *content* evolution — no evidence either way.
- [O] The Revision trigger, Retrieval visibility of Historical/Questioned content, and cross-Department escalation — carried forward from Blueprint v3 unchanged, resolved by real usage or future Architect decision, not by this model.
