# AIOS Reference Subsystem Engineering Model v1.0

**Status:** The reusable engineering blueprint every future subsystem Detailed Design follows. A structural model, not a subsystem specification. No code, schema, database, API, interface, UML, diagram, pseudocode, or implementation. Designs no concrete subsystem.
**Version:** v1.0
**Relationship to the Engineering Design Standard v1.0:** the Standard is the **contract** (the rules a design must obey); this Model is the **structure** (what a subsystem *is* and the shape every design takes). The two are complementary and non-overlapping by construction — where this Model would restate a Standard rule, it cites §-references instead (see §9's mapping).
**Authority basis:** extracted only from the ratified corpus (Constitution, Canonical Domain Model, Principles Register, Pattern Catalog, Vocabulary, Blueprint v3, Engineering Design Standard, Implementation Architecture Plan, Meta Model, Ratification Review). No architecture is invented; no canonical decision is redesigned.
**Confidence discipline:** **[E]** evidenced · **[A]** assumption · **[O]** open question.

---

## 1. Purpose — What a Subsystem Is

[E] **A subsystem is an implementation-layer unit that owns exactly one architectural concern and is governed by one or more canonical documents.** It is *not* a Canonical Domain Model entity. This distinction is load-bearing and must not blur:

- **Domain Model entities** (Department, Capability, Agent Definition, Agent Instance, Skill, Workflow, Tool, Runtime, Knowledge, Memory, Trace) are ratified semantic concepts — *what AIOS is made of* (Canonical Domain Model §2).
- **Subsystems** (Repository, Admission, Service, Retrieval, Query Layer, plus the [BUILT] Execution-Layer units) are engineering units that *implement or operate on* those entities (Implementation Architecture Plan §1). "Repository" and "Service" appear **nowhere** in the Domain Model's entity list — they are subsystem *types*, not entities. A design that treats them as entities would be introducing architecture; this Model forbids that.

**Architectural role of a subsystem [E]:** to realize a bounded concern in code while preserving every invariant, principle, and boundary the canonical layer defines. A subsystem is the smallest unit at which the Engineering Design Standard's contract is applied.

**Relationships among the named concepts (without redesign) [E]:**
- **Department** owns Capabilities and Agent Definitions (DM §5). A subsystem is not owned by a Department; it implements behavior that Agent Definitions (which *are* Department-owned) may use.
- **Capability** is the outcome contract; a subsystem may contribute to realizing a Capability but is not itself one.
- **Workflow** composes **Skills**; a **Skill** invokes a **Tool**; a **Tool** is the only entity with an external dependency (DM inv. 12). A subsystem may be invoked through this Skill→Tool path or may be infrastructure beneath it (e.g. Trace, Repository) that Skills and Tools rely on.
- **Runtime** hosts Agent Instances; a subsystem does not host — it is hosted-adjacent infrastructure or execution logic.
- **Repository** and **Service** are subsystem *types* introduced by Blueprint v3 / the Implementation Plan: a Repository persists (append-only, versioned); a Service derives/operates over persisted records. Neither is a domain entity; both are engineering realizations.

The single rule this section exists to enforce: **a subsystem design may reference domain entities but may never redefine one, and may never elevate a subsystem type into an entity.**

## 2. Engineering Boundary Model

[E] Every subsystem has eight boundaries, each identified during Detailed Design by asking one question:

| Boundary | Identifying question | Canonical basis |
|---|---|---|
| **Internal** | What concern-divisions exist *inside* this subsystem? | Single Responsibility (Standard §1) |
| **External** | Exactly where does this subsystem end and another begin? | Boundary Map (T9) |
| **Public Responsibility** | What does this subsystem guarantee to others? | Interface Standards (Standard §3) |
| **Private Responsibility** | What does it handle internally that others must not depend on? | Separation of Concerns |
| **Ownership** | Which concern does it *own* (vs. merely touch)? | Ratification Review "one home per concern" |
| **Authority** | Which of its actions are governed, and under whose authority? | Constitution §6.2 inv. 2; Blueprint v3 §2.6 |
| **Data** | What data does it own, capture (snapshot), or merely reference? | PR-5; Domain Model §6.1 |
| **Trace** | Which of its actions are Agent Instance actions requiring a Trace record? | Domain Model inv. 4 |

[E] **How boundaries are identified:** by walking these eight questions in order. The Ownership and Authority boundaries are identified *before* the Data and Trace boundaries, because what a subsystem owns and governs determines what it may persist and must trace — not the reverse. A design that fixes its data model before its ownership boundary has inverted the canonical order (this is the same error the Ratification Review caught at document scale: placement follows concern, not convenience).

## 3. Internal Engineering Structure

[E] Every subsystem's Detailed Design describes its internals through this canonical set (structure only — no components-as-classes, no data-as-schema):

- **Responsibilities** — the enumerated concern-divisions inside the Ownership boundary.
- **Internal Collaboration** — how those divisions cooperate (conceptually; not call graphs).
- **Data Flow** — how captured/referenced data moves between divisions (respecting PR-5: captured data is snapshot, not live).
- **Decision Points** — every point where a choice is made; each classified as **automated** (detection/derivation only) or **governed** (human decision) — the automated/governed split is mandatory here because it is where PR-3 is enforced or violated.
- **Validation Points** — every point where input/state is validated before a write, fail-closed (PR-4).
- **Authority Checks** — every governed decision point's authority verification and refusal-recording.
- **Failure Handling** — the fail-closed behavior at each failure, per PR-4.
- **Trace Capture** — which internal actions emit Trace records (inv. 4).
- **Provenance** — what provenance each durable output captures and its permanence.

[E] **The internal structure's organizing spine is the Decision Points list** — because a subsystem's correctness under AIOS governance is determined almost entirely by whether each decision is correctly classified automated-vs-governed. The Human Review subsystem's proven design is the reference example: its single governance decision point is structurally incapable of automation (AST-verified), and every other point is pure recording/derivation.

## 4. Interaction Model

[E] How one subsystem interacts with another:

- **Dependency direction:** downward or sideways-to-[BUILT] only; never upward (Standard §5; the real Execution Layer's acyclic graph). A subsystem interaction that would require an upward dependency is a design error, not a design choice.
- **Collaboration vs. ownership (explicitly distinguished, per the directive):** **collaboration** is one subsystem *using* another's public responsibility across a boundary; **ownership** is a subsystem *holding* a concern. Two subsystems may collaborate without either owning the other's concern — this is the normal case. A design that makes subsystem A depend on subsystem B's *internal* (private) responsibility has confused collaboration with ownership and violated B's boundary. Domain Model invariant 13 binds here: subsystems realizing Agent-Instance behavior may collaborate only through Workflow, Knowledge, or scoped Memory — never a private channel.
- **Authority verification:** when subsystem A invokes a governed action in subsystem B, B verifies authority itself (authority is not delegated across a boundary by the mere act of calling) — the orchestrator→skill authorization pattern is the [BUILT] precedent.
- **Evidence flow:** evidence moves *up* the derivation chain (Trace → Memory → Candidate → Decision → Knowledge), captured at each step (PR-5), never flowing back down as authority (Memory cannot override Knowledge).
- **Lifecycle interaction:** one subsystem's lifecycle transition may *inform* another (e.g. a new Knowledge version informs Retrieval) but may never *drive* another's governed transition automatically (PR-3).
- **Trace interaction:** every cross-subsystem governed action produces exactly one Trace record at the acting subsystem (inv. 4); the record is the shared, permanent account both sides can later cite (PR-5, §6.1).

## 5. Subsystem Engineering Lifecycle

[E] The lifecycle of *a subsystem as an engineering artifact* (distinct from Knowledge lifecycle — this governs how a subsystem is built, not what Knowledge does). Extracted from the phases the corpus already practices:

```
Proposal      — a subsystem is identified in the Implementation Architecture Plan
   ↓            (justified by canonical architecture; no invention)
Design        — a Detailed Design produced per the Engineering Design Standard template
   ↓
Review        — architectural + engineering + implementation-readiness review (§6)
   ↓
Approved      — explicit Architect authorization for this specific subsystem
   ↓
Implemented   — code written (a later phase; out of this Model's scope)
   ↓
Tested        — behavior verified (later phase)
   ↓
Maintained    — evolved under the Evolution Protocol; changes re-enter at Design
   ↓
Deprecated    — retired under governance; records retained (never deleted — inv. 5 spirit)
```

[E] This lifecycle is itself an instance of the Canonical Evolution Model's shape (proposal→review→canonical→revision→historical) applied to engineering artifacts rather than content — the same generalization the Evolution Model already claimed [A] applies beyond content. Maintenance re-enters at Design, never edits an approved design in place (Immutable Records applied to design documents, consistent with the Ratification Review's "historical, never edited").

## 6. Design Review Model

[E] Three distinct reviews, never merged, each with distinct verifiers-of-record:

| Review | Verifies | Against |
|---|---|---|
| **Architectural Review** | The design contradicts no invariant, principle, or boundary; owns exactly one concern; boundaries align to the Boundary Map | Constitution, Domain Model, Principles Register, Blueprint v3 |
| **Engineering Review** | The design used the Standard's template completely; every mandatory section present; decision points correctly classified; failure modes fail closed; dependencies legal and acyclic | Engineering Design Standard §2, §6, §7 |
| **Implementation Readiness Review** | Zero unresolved must-resolve-before-implementation open questions; all [BUILT] dependencies reused as-is; explicit per-subsystem authorization present | Engineering Design Standard §8; Implementation Architecture Plan sequencing |

[E] **Order is fixed:** Architectural → Engineering → Implementation Readiness. A design cannot pass Engineering Review if it fails Architectural Review (a technically clean design that violates an invariant is rejected first, per the Standard's own "not approvable regardless of merit"). Implementation Readiness is last because it presupposes the other two passed.

## 7. Cross-Cutting Concerns

[E] Every subsystem must explicitly address each — but **only concerns the corpus already supports** are listed (the directive's caution honored):

| Concern | Corpus support | Mandatory design obligation |
|---|---|---|
| Authority | Constitution §6.2 inv. 2; Blueprint v3 §2.6 | Every governed action names its authority |
| Validation | PR-4; `validate_decision_input` | Fail-closed, before every write |
| Provenance | PR-5; DM §6.1 | Captured, permanence specified |
| Traceability | DM inv. 4 | One Trace record per action |
| Explainability | DM §6.1; PR-5 | Every decision reconstructible from captured records |
| Failure Recovery | PR-4 | Fail closed; recovery via re-execution, never silent trust |
| Dependency Management | Standard §5; acyclic graph | Named, directional, legal |
| Observability | `observability.py`, `metrics.py` [BUILT] | Actions are inspectable via Trace-derived views |

[O] **Two concerns the directive listed are NOT fully corpus-supported — flagged, not fabricated:**
- **Security** (as distinct from Authority): the corpus has authority/authorization but no ratified *security* model (threat model, secrets, access control) — Domain Model §8 even forbids Department-scoped access restriction for Substrate entities. A subsystem design may not invent a security model; where security genuinely arises, it is an **[O] open question requiring a future architecture decision**, not an engineering obligation this Model can impose.
- General **access control**: same status — no ratified model exists; must not be invented at design time.

This is the honest boundary: the Model requires only the eight corpus-supported concerns and explicitly marks Security as an unresolved architectural prerequisite rather than pretending it is covered.

## 8. Canonical Design Flow

[E] The fixed sequence every subsystem Detailed Design follows (the actual flow the corpus implies, ordered so each step depends only on prior steps):

```
Purpose (one concern)
   ↓
Responsibilities  +  Non-Responsibilities
   ↓
Boundaries (all eight, §2 — Ownership & Authority before Data & Trace)
   ↓
Dependencies (§5-legal, acyclic)
   ↓
Internal Structure (§3 — Decision Points as spine)
   ↓
Interactions (§4 — collaboration ≠ ownership)
   ↓
Cross-Cutting Concerns (§7 — eight; Security flagged if it arises)
   ↓
Validation (§6 checkpoints)
   ↓
Failure Modes (fail closed)
   ↓
Consistency Review (vs. all canonical sources)
   ↓
Implementation Authorization (explicit, per-subsystem)
```

[E] This flow *is* the Standard's template (§7 there) arranged as a dependency-ordered sequence — same content, causal order made explicit.

## 9. Detailed Design Mapping (Standard → this Model)

Every mandatory Standard §2 section, mapped to where it lives in this engineering structure — guaranteeing one identical structure across all future designs:

| Engineering Design Standard §2 section | Home in this Model |
|---|---|
| 1 Purpose | §1 / Design Flow step 1 |
| 2 Canonical Responsibilities | §3 Responsibilities / Flow step 2 |
| 3 Non-Responsibilities | §2 Ownership Boundary / Flow step 2 |
| 4 Dependencies | §4 Interaction Model / Flow step 4 |
| 5 Inputs | §2 Data Boundary / §4 evidence flow |
| 6 Outputs | §2 Public Responsibility / §4 |
| 7 Internal Boundaries | §2 Internal Boundary / §3 |
| 8 External Boundaries | §2 External Boundary |
| 9 Failure Modes | §3 Failure Handling / §7 Failure Recovery |
| 10 Authority Rules | §2 Authority Boundary / §3 Authority Checks |
| 11 Provenance Rules | §3 Provenance / §7 |
| 12 Validation Rules | §3 Validation Points / §6 |
| 13 Traceability Rules | §2 Trace Boundary / §3 Trace Capture |
| 14 State/Condition Representation | §3 (Decision Points) + State Mgmt (Standard §4) |
| 15 Open Questions | §10 (carried per design) |

[E] Every Standard section has exactly one home; no section is unmapped; no home is empty. The two documents are now provably one structure viewed two ways (contract + shape).

## 10. Consistency Verification

- [E] **Constitution:** the Model reserves every governance decision to humans (§3 Decision Points, §7 Authority); adds no authority. No contradiction.
- [E] **Canonical Domain Model:** §1 explicitly forbids elevating a subsystem type into an entity or redefining an entity; §2/§4 project invariants 4, 5, 13 and §6.1. No contradiction.
- [E] **Principles Register:** PR-1…PR-5 are the organizing spine of §3–§7; none is added or weakened. No contradiction.
- [E] **Engineering Design Standard:** §9 maps every Standard section into this Model with no overlap or gap; the two are complementary. No contradiction.
- [E] **Blueprint v3:** the collaboration/ownership, provenance-permanence, and Home-Department-accountability rules are lifted unchanged. No contradiction.
- [E] **Implementation Architecture Plan:** the subsystem lifecycle, review model, and [BUILT]/[ARCHITECTED]/[OPEN] vocabulary are used unchanged. No contradiction.

**Explicitly identified (not silently resolved):**
- **Contradictions found:** none.
- **Assumptions discovered [A]:** that the subsystem engineering lifecycle (§5) is a valid instance of the content Evolution Model's shape — a structural analogy the Evolution Model itself already marked [A], carried forward, not newly asserted.
- **Hidden dependencies [E]:** the Model depends on the Boundary Map and Status Registry existing as living canonical documents (for External Boundary alignment and [BUILT] status) — named so they are recognized as load-bearing.
- **Engineering risks [E]:** (1) the automated-vs-governed classification of Decision Points (§3) is the highest-consequence, easiest-to-get-wrong step — a misclassification is exactly how PR-3 gets violated; flagged as the step reviewers must scrutinize most. (2) the Ownership-before-Data ordering (§2) is counter to common engineering habit (schema-first) and will require active discipline.
- **Unresolved architectural prerequisites [O]:** **Security / access-control has no ratified model** (§7) — any subsystem for which security genuinely matters cannot complete a compliant design until the Architect authorizes a security architecture decision. This is the single most significant prerequisite this review surfaces.

---

## Final Review — Sufficiency as Permanent Engineering Foundation

[E] **The Reference Engineering Model is sufficiently complete to serve as the permanent engineering foundation for all future subsystem designs, with one explicitly-bounded gap.** It defines what a subsystem is, its eight boundaries, its internal structure, its interaction rules, its own engineering lifecycle, a three-stage review model, the corpus-supported cross-cutting concerns, a fixed design flow, and a complete mapping to the Engineering Design Standard with zero unmapped sections. Every element is extracted, cited, and consistency-verified.

**The one bounded gap [O]:** Security/access-control is an unresolved architectural prerequisite, not an engineering omission — the Model correctly refuses to invent it and instead flags it as requiring a future Architect decision before any security-relevant subsystem can complete a compliant design. This does not weaken the Model for the subsystems currently on the critical path (Knowledge Repository, Admission, Service), none of which introduces a security concern beyond the already-ratified authority model.

**Remaining weaknesses (explicit):** (1) the [A] analogy in §5 (subsystem lifecycle ≈ Evolution Model shape) is reasoned, not proven across a second instance; (2) the Model's effectiveness depends on reviewers actively scrutinizing the automated-vs-governed Decision Point classification — a discipline the Model can mandate but not enforce.

**Recommended next subsystem Detailed Design:** the **Knowledge Repository** — unchanged from the Implementation Architecture Plan's recommendation, now re-confirmed against this Model's readiness criteria:
- **Architectural readiness [E]:** version-addressing settled (Blueprint v3 Decision 1); no open architecture question blocks it.
- **Engineering readiness [E]:** all its dependencies (Trace, Snapshot, Provenance, Validation) are [BUILT] and reusable as-is; it introduces no Security concern (append-only persistence under the existing authority model).
- **Dependency order [E]:** it is the root of the Knowledge Infrastructure layer; Admission and Service both depend on it.
- **Implementation risk [E]:** lowest available — append-only versioning is a pattern already proven at 540-record scale in Trace.

No concrete subsystem was designed. No code, schema, database, API, interface, diagram, or pseudocode was produced. No canonical decision was reopened. Stopping here. Awaiting explicit Architect authorization before the Knowledge Repository Detailed Design begins.
