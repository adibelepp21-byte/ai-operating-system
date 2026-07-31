# AIOS Engineering Design Standard v1.0

**Status:** The canonical engineering standard every future subsystem Detailed Design must follow. Standards only — no code, schema, API, class diagram, database design, pseudocode, or implementation. Not subsystem-specific: it defines *how* designs are produced, not *what* any subsystem is.
**Version:** v1.0
**Authority basis:** extracted from — never additive to — the Constitution, Canonical Domain Model (invariants 1–15), Principles Register (PR-1…PR-5), Blueprint v3, and the Implementation Architecture Plan. Every rule below cites the canonical source that already implies it; no rule invents architecture.
**Confidence discipline:** **[E]** evidenced · **[A]** assumption · **[O]** open question.

---

## 0. What This Document Is

[E] This Standard is the **engineering contract** for the Detailed Design phase — the phase the Implementation Architecture Plan §6 places *after* Implementation Planning and *before* Implementation. It binds every future Detailed Design (Repository, Admission, Service, Retrieval, Runtime, …). It adds no architecture; it makes the architecture's already-implied engineering constraints explicit and enforceable.

A Detailed Design that violates this Standard is not approvable, regardless of its technical merit — the same way a governance decision that violates an invariant is not valid regardless of its content.

---

## 1. Design Principles (extracted, not invented)

Every principle below is already ratified elsewhere; this section binds it specifically to design work.

| Principle | Design obligation | Canonical source |
|---|---|---|
| **Evidence First (PR-1)** | A design may specify only what a demonstrated need requires; speculative structure is rejected. Unknowns are recorded as open questions, never filled with plausible assumptions. | PR-1 |
| **Fail Closed (PR-4)** | Every design's failure modes must default to refusal, never to silent trust or a guessed value. | PR-4; `verification.py`, `validate_decision_input` |
| **Detect, Don't Decide (PR-3)** | No design may place a governance decision on an automated path; automation may detect/propose only. | PR-3; Constitution §6.2 inv. 2 |
| **State/Condition Separation (PR-2)** | Any design with both a history and an evaluation must represent them as two independent axes. | PR-2 |
| **Capture, Don't Reference (PR-5)** | Any durable record referencing volatile data must capture a snapshot, never a live pointer. | PR-5; Domain Model §6.1 |
| **Single Responsibility** | Each subsystem owns exactly one concern (the Ratification Review's "one canonical home per concern" applied at subsystem level). | Ratification Review; Boundary Map |
| **Explicit Dependencies** | Every dependency is named and directional; no hidden coupling. | Implementation Plan §1; the real Execution Layer's acyclic import graph |
| **Immutable Records** | Any record a design persists is append-only; never mutated or deleted. | Domain Model inv. 5; Blueprint v3 Decision 4 |
| **Separation of Concerns** | A design must not absorb a responsibility another subsystem canonically owns. | Boundary Map |
| **Traceability (unconditional)** | Every subsystem action that constitutes an Agent Instance action produces exactly one Trace record. | Domain Model inv. 4 |
| **Authority Before Action** | Every governed transition checks authority before acting and records refusal as a first-class event. | `orchestrator.py` pattern; Constitution §6.2 |

## 2. Subsystem Design Rules — Mandatory Content

Every subsystem Detailed Design **must** specify all of the following. A design missing any section is incomplete by definition.

1. **Purpose** — the single concern it owns (Single Responsibility).
2. **Canonical Responsibilities** — enumerated; each traceable to a governing canonical document.
3. **Non-Responsibilities** — what it explicitly does *not* own (prevents concern-absorption); names the subsystem that owns each excluded concern.
4. **Dependencies** — named, directional, each classified [BUILT]/[ARCHITECTED]/[OPEN] per the Implementation Plan; must obey §5's direction rules.
5. **Inputs** — every input, its source subsystem, and whether it is captured (snapshot) or referenced (per PR-5).
6. **Outputs** — every output and its consumer subsystem(s).
7. **Internal Boundaries** — the concern-divisions inside the subsystem.
8. **External Boundaries** — exactly where this subsystem ends and another begins (must align with the Boundary Map).
9. **Failure Modes** — every failure and its fail-closed behavior (PR-4); no failure may default to trust.
10. **Authority Rules** — which actions are governed, who/what may perform each, and how refusal is recorded (§ Authority Before Action).
11. **Provenance Rules** — what provenance the subsystem captures, which elements are permanent vs. reassignable, per Blueprint v3 §2.5's permanence model where applicable.
12. **Validation Rules** — what is validated, when (before any write), and that validation is fail-closed and never evidence-quality-based where governance is involved.
13. **Traceability Rules** — which subsystem actions produce Trace records (inv. 4) and that no such action is untraced.
14. **State/Condition Representation** — if the subsystem has both, the two independent axes (§4).
15. **Open Questions** — every unresolved item, classified (must-resolve-before-implementation / resolve-during / defer), per the Quality Checklist.

## 3. Interface Standards (without defining APIs)

Every subsystem interface — conceptually, not as an API — **must document**:

- **What it accepts** — the meaning and source of each input, and whether the interface captures or references it.
- **What it returns** — the meaning of each output, and explicitly whether any output is or is not a governance verdict (PR-3: no interface may return a computed governance decision).
- **What it guarantees** — the invariants the interface upholds for its caller (e.g. "the returned snapshot is immutable," "a refusal is always recorded").
- **What it refuses** — the conditions under which it fails closed, and the form of that refusal (PR-4).
- **What it never does** — explicit non-guarantees, especially any governance decision it will not make (PR-3), any mutation it will not perform (inv. 5), and any concern it will not absorb.
- **Authority context** — under whose authority its governed operations act (Blueprint v3 §2.6 for Knowledge; the Agent Definition's permissions for execution).

No interface documentation may specify method signatures, parameter types, serialization, or transport — those are Implementation-phase artifacts, out of scope here.

## 4. State Management Rules (conceptual, no schema)

How each cross-cutting concern must be represented in any design that touches it:

- **Lifecycle (state):** position only, from a minimal, evidence-justified state set; new states require demonstrated need (Blueprint v3's 8→2 collapse is the precedent). Lifecycle transitions are governed and traced.
- **Condition (evaluation):** represented on an axis independent of lifecycle (PR-2); may be proposed by automation, set only by governed review (PR-3).
- **Provenance:** captured as snapshots at decision time (PR-5); permanence per the applicable permanence model; never a live reference to recomputable data.
- **Identity:** a stable correlation key shared across records, never a stored mutable master; a design must verify its chosen key is genuinely stable (the `memory_id` counter-example is the cautionary precedent).
- **Versioning:** change = a new immutable version under a stable identity; never in-place mutation (inv. 5; Blueprint v3 Decision 4).
- **Authority:** represented as an explicit, checkable property of a governed action, human-held for every governance decision (Constitution §6.2 inv. 2); never derived from a score, signal, or automated proposal.
- **Traceability:** every Agent Instance action → exactly one Trace record (inv. 4), unconditional; a design may not make traceability optional or conditional.

## 5. Dependency Rules

**Allowed directions** [E], consistent with the real Execution Layer's proven acyclic graph and the Canonical Architecture Map:

- A subsystem may depend on **Foundation** and **Core Infrastructure** ([BUILT]) freely.
- Knowledge Infrastructure may depend on Foundation/Core; not on Governance/Execution above it.
- Governance Infrastructure may depend on Knowledge Infrastructure and below; not on Retrieval/Query.
- Every dependency points **downward or sideways-to-already-built**, never upward toward a less-foundational layer.

**Prohibited dependencies** [E]:

- No subsystem may depend on a subsystem in a higher layer (would create a cycle).
- No subsystem may depend on Memory as an authority (Memory is provisional; it may inform, never govern — Domain Model §6; Blueprint v3's "Memory cannot override Knowledge").
- No subsystem may depend on a governance decision being computable (PR-3).
- No Knowledge subsystem may introduce Department-scoped access dependency (Blueprint v3 §2.6 / DM §8 — Home Department is accountability, not access control).
- No subsystem may depend on Trace being mutable (inv. 5).

**Domain Model consistency** [E]: these directions are the design-level projection of the Domain Model's own layering (Spine → Execution → Substrate, with Trace cross-cutting and append-only). Invariant 13 (no direct Agent-Instance-to-Agent-Instance collaboration outside Workflow/Knowledge/scoped Memory) binds any design proposing inter-subsystem coordination: it must route through one of those, never a private channel.

## 6. Validation Requirements — Mandatory Checkpoints

A subsystem design may be considered complete only when **all** of the following are satisfied and documented:

1. **Responsibility singularity** — the design owns exactly one concern; non-responsibilities enumerated.
2. **Dependency legality** — every dependency obeys §5; the design's dependency set is acyclic against the current graph.
3. **Invariant compliance** — the design is checked against Domain Model invariants 4, 5, 8 (and any others it touches) with the check recorded.
4. **Principle compliance** — checked against PR-1…PR-5 with the check recorded.
5. **Authority completeness** — every governed action names its authority and its refusal-recording.
6. **Failure-mode completeness** — every failure has a documented fail-closed behavior.
7. **Provenance completeness** — every durable record's provenance capture is specified per PR-5.
8. **Traceability completeness** — every action's Trace production is specified per inv. 4.
9. **Open-question classification** — every unknown is classified; no unclassified unknown remains.
10. **Boundary alignment** — the design's external boundaries match the Boundary Map with no overlap into another subsystem's concern.

These checkpoints are the Quality Checklist (T10) specialized to Detailed Design.

## 7. Canonical Detailed Design Template

Every future subsystem Detailed Design must use this structure (section numbers fixed for cross-referenceability):

```
[Subsystem] Detailed Design v[n]
  Status / Version / Authority basis / Evidence tags
  1. Purpose (single concern)
  2. Canonical Responsibilities  (each → governing document)
  3. Non-Responsibilities        (each → owning subsystem)
  4. Dependencies                (named, directional, [BUILT]/[ARCHITECTED]/[OPEN])
  5. Inputs                      (source; captured vs. referenced)
  6. Outputs                     (consumer; governance-verdict? explicitly no)
  7. Internal Boundaries
  8. External Boundaries         (aligned to Boundary Map)
  9. Failure Modes               (each fail-closed)
 10. Authority Rules             (governed actions; refusal recording)
 11. Provenance Rules            (permanence; capture-not-reference)
 12. Validation Rules            (before-write; fail-closed)
 13. Traceability Rules          (one Trace record per action)
 14. State / Condition Representation (two axes if applicable)
 15. Open Questions              (classified)
 16. Validation Checkpoint Results (§6, all ten, recorded)
 17. Consistency Review          (vs. Constitution, DM, Principles, Blueprint v3, Implementation Plan)
```

No template section may be omitted; a section that is genuinely not-applicable must say so and say why (never left blank).

## 8. Engineering Readiness Checklist (before implementation may begin)

Implementation of a subsystem may begin only when its Detailed Design has:

- [ ] Used the §7 template with no omitted section.
- [ ] Passed all ten §6 validation checkpoints, each recorded.
- [ ] Zero unresolved *must-resolve-before-implementation* open questions (resolve-during and defer are permitted to remain).
- [ ] A recorded consistency review (§7 section 17) showing no contradiction with Constitution, Domain Model, Principles Register, Blueprint v3, or Implementation Architecture Plan.
- [ ] Explicit Architect authorization for that specific subsystem's implementation (per the standing rule that automation/stop-hooks are not authorization).
- [ ] Confirmation that all its [BUILT] dependencies are reused as-is (not re-implemented) and all [ARCHITECTED] dependencies are themselves already designed or being designed in the authorized sequence.

A design that satisfies this checklist is *implementation-ready*; one that does not is not, regardless of merit.

---

## 9. Consistency Review — This Standard vs. Canonical Architecture

Verifying the Standard introduces no contradiction:

- [E] **Constitution:** the Standard's Authority-Before-Action and Detect-Don't-Decide rules restate §6.2 invariant 2; it adds no authority and reserves every governance decision to humans. No contradiction.
- [E] **Canonical Domain Model:** the Standard's Immutable Records, Traceability, and dependency rules are direct projections of invariants 4, 5, 8, 13; §5 mirrors the Model's own layering. No contradiction.
- [E] **Principles Register:** §1 binds PR-1…PR-5 verbatim to design work; it neither adds a principle nor weakens one. No contradiction.
- [E] **Blueprint v3:** the State/Condition, provenance-permanence, and Home-Department-accountability-not-access rules are lifted directly from Blueprint v3; the Standard generalizes them to all subsystems without altering the Knowledge-specific settled decisions. No contradiction.
- [E] **Implementation Architecture Plan:** the Standard uses the Plan's [BUILT]/[ARCHITECTED]/[OPEN] vocabulary, its layer ordering, and its phase distinction unchanged; the Readiness Checklist enforces the Plan's sequencing. No contradiction.
- [O] **One honest boundary:** the Standard governs *how* designs are produced; it cannot guarantee a future design's *content* is correct — only that a non-compliant design is rejectable. This is a scope statement, not a contradiction.

**Verdict [E]:** the Engineering Design Standard contradicts no canonical document. It is a faithful, additive-only projection of already-ratified architecture into the Detailed Design phase.

---

No code, schema, API, class diagram, database design, or pseudocode was produced. No subsystem was designed. No ratified decision was reopened. This Standard is now the engineering contract for every future Detailed Design. Stopping here. Awaiting Architect authorization before any subsystem design begins.
