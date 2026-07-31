# Knowledge Repository — Detailed Design v1.0

**Status:** Detailed Design only. No implementation, code, schema, database, API, class, pseudocode, UML, storage technology, indexing strategy, or optimization. Designs the Knowledge Repository subsystem exclusively.
**Version:** v1.0
**Authority basis:** Blueprint v3 (§2.1, Decisions 1 & 4), Canonical Domain Model (inv. 4, 5, 8; §6, §6.1), Principles Register (PR-1…PR-5), Engineering Design Standard v1.0, Reference Subsystem Engineering Model v1.0, Implementation Architecture Plan.
**Template:** follows the Engineering Design Standard §7 seventeen-section template and the Reference Model §8 design flow; the directive's 21 required items are all present and cross-referenced.
**Confidence discipline:** **[E]** evidenced · **[A]** assumption · **[O]** open question.

---

## 1. Purpose

[E] The Knowledge Repository is the subsystem that **durably stores and retrieves Knowledge versions** — nothing more. It is the canonical home for the single concern "persistence of Knowledge versions" (Ratification Review: one home per concern). Per Blueprint v3 §2.1, a Knowledge Version is "the only stored Knowledge record"; the Repository is where that storage lives.

[E] **A foundational clarification that shapes the entire design:** Knowledge is a *durable Substrate entity*, not a derived one. This is precisely what distinguishes it from Memory (Memory is recomputed, provisional, unstable-identity; Knowledge is stored, durable, stable-identity). Therefore the Repository is a **genuine durable store**, distinct from Trace — not a derived view over Trace the way Memory is. The Trace record of an admission is *the record that the admission action happened*; the Repository record is *the durable Knowledge itself*. These are two different artifacts serving two different purposes; they are not duplicate sources of truth for one fact.

## 2. Responsibilities (Repository Responsibilities — directive items 2 & 9)

The Repository is responsible for, and only for:

- **R1 — Durable storage of immutable Knowledge version records.** Once stored, a version is never altered or deleted (Domain Model inv. 5 analogue; Blueprint v3 Decision 4).
- **R2 — Address-based retrieval:** return the exact version identified by a version address.
- **R3 — Identity-based retrieval:** return the set of all versions sharing a Knowledge identity key, in their stored supersession order.
- **R4 — Structural admission-to-storage validation:** before storing, confirm a candidate version record is structurally complete (§16); refuse otherwise (fail closed).
- **R5 — Provenance-linkage preservation:** store and preserve, unaltered, the provenance each version carries (§12), including the reference to the Trace record of the action that created it.
- **R6 — Append-only enforcement:** reject any request to mutate or delete a stored version (§15).

## 3. Non-Responsibilities (directive item 3)

The Repository explicitly does **not** own, and must never absorb, the following — each named with its owning subsystem, per Reference Model §2 (Ownership Boundary):

| Not the Repository's concern | Owning subsystem |
|---|---|
| Admission decisions (whether to create a version) | Admission |
| Deciding which version is the current **Active** one | Knowledge Service (derived, not stored) |
| Evaluating **validity** (Confirmed/Questioned/Invalidated) | Governance Services / Knowledge Service |
| Conflict detection or evaluation | Governance / Memory Governance |
| Revision decisions (whether to create a new version) | Governance Services |
| Human review | Human Review Services |
| Workflow orchestration | Orchestrator / Runtime |
| Authority decisions (who may act) | The acting subsystem + Authority Enforcement |
| Ranking, filtering, or query relevance | Retrieval / Query Layer |
| Ownership *assignment* or *reassignment* | Admission / Governance (the Repository merely stores the assigned value) |

[E] **The single sharpest non-responsibility:** the Repository **evaluates nothing**. It stores immutable records and returns them by address or identity. Every evaluative question — current version, validity, conflict, relevance — is derived elsewhere from the raw material the Repository provides. This mirrors exactly how Memory Governance already derives `review_state` from Trace records without Trace itself evaluating anything.

## 4. Internal Boundaries (directive item 4)

[E] Internally the Repository divides into three concern-divisions (conceptual, per Reference Model §3 — not components-as-classes):

- **B-internal-1 — Intake:** receives a candidate version, applies structural validation (R4), refuses or accepts.
- **B-internal-2 — Durable Record Keeping:** the append-only retention of accepted version records; enforces immutability (R6).
- **B-internal-3 — Access:** address-based (R2) and identity-based (R3) retrieval of stored records.

The boundary between Intake and Record Keeping is where fail-closed validation sits (nothing unvalidated crosses into durable retention). The boundary between Record Keeping and Access is read-only (Access never modifies what Record Keeping holds).

## 5. External Boundaries (directive item 5)

[E] The Repository's external boundary is defined by what crosses it and what does not:

- **Crosses inward:** a structurally complete candidate version record (from Admission or a future Revision subsystem), carrying identity key, content, provenance, supersession linkage, and a reference to its creating action's Trace record.
- **Crosses outward:** exact version records (by address) and version sets (by identity), returned verbatim, unevaluated.
- **Never crosses:** governance decisions, validity/lifecycle evaluations, authority tokens, ranked/filtered results. A request for any of these is outside the Repository's boundary and is refused as not-its-concern (not merely failed).

[E] The external boundary aligns with the Boundary Map: the Repository sits in the Knowledge Infrastructure layer, beneath Governance and Execution infrastructure, above only Foundation/Core [BUILT] dependencies.

## 6. Dependencies (directive item 6)

| Dependency | Status | Why needed |
|---|---|---|
| Trace | [BUILT] | Provenance linkage — every version references its creating action's Trace record (R5) |
| Snapshot Management | [BUILT] | Versions arrive as captured snapshots (PR-5); the Repository stores them as-is |
| Provenance Services | [BUILT] | The provenance a version carries was assembled here before arrival |
| Validation Layer (pattern) | [BUILT] | The fail-closed validation discipline the Repository's Intake reuses (PR-4) |

[E] All dependencies are [BUILT] and reused as-is — the Repository introduces no new foundational dependency. This is the reuse-maximizing property the Implementation Plan identified for choosing the Repository first.

## 7. Dependency Direction (directive item 7)

[E] Every dependency points **downward** to Foundation/Core [BUILT] subsystems. The Repository depends on nothing in its own layer (Admission, Service) or above it (Governance, Retrieval) — those depend on *it*. This is §5-legal per the Engineering Design Standard and preserves the acyclic graph proven in the Execution Layer. **No upward dependency exists; none is permitted.**

## 8. Internal Components (conceptual only — directive item 8)

[E] Three conceptual components, matching the internal boundaries (§4), described by role only (no classes, no data structures):

- **Intake Gate** — the single entry point for a candidate version; performs structural validation; is the only place a version can enter durable retention.
- **Version Register** — the durable, append-only holder of accepted version records; the authority for "what versions exist"; enforces that nothing held is ever altered.
- **Access Reader** — the read-only responder to address and identity retrieval requests; never modifies the Register.

[E] There is deliberately **no evaluation component** — the absence is the design. A Repository with an "is-current" or "is-valid" component would have absorbed another subsystem's concern.

## 9. (Repository Responsibilities — merged into §2 above)

Per the directive's own structure, items 2 and 9 name the same responsibilities; they are enumerated once in §2 to avoid duplicate authority within this document.

## 10. Version Addressing (directive item 10)

[E] Grounded in Blueprint v3 Decision 1 (settled): **each version is a separately addressable, immutable record.** The Repository must therefore support addressing a version uniquely and permanently.

Design (conceptual, no schema):
- Every stored version has a **permanent version address** that is unique across the entire Repository and never reused, never reassigned.
- A version address, once issued, refers forever to exactly one immutable record. Retrieval by that address (R2) is deterministic and stable for all time — a property required by PR-5 (a decision elsewhere may cite a specific version address and must resolve identically forever).
- The Repository does not interpret the address beyond using it to retrieve; it encodes no meaning (no ordering, no status) into the address itself. Ordering and status are separate concerns (§11, and derived elsewhere).

[O] **Open question OQ-1 (address form):** whether the version address is opaque or structured is an *implementation-planning* decision, explicitly out of scope here (no storage technology, no indexing). Flagged, not resolved.

## 11. Identity Management (directive item 11)

[E] Grounded in Blueprint v3 Decision 1: **Knowledge Identity is a stable logical correlation key shared across versions, not a stored parent entity.** This is the Repository's most important structural rule and it directly reuses the proven Trace ↔ Agent Instance correlation pattern (PR-5 / Pattern P5).

Design:
- Every version carries its **identity key**. The Repository stores this key with the version and uses it to answer identity-based retrieval (R3).
- The Repository stores **no identity record** — there is no "Knowledge identity" row/object to look up. An identity *exists* precisely insofar as versions carrying its key exist. This is the same model by which an Agent Instance exists only through the Trace records carrying its `instance_id` (Reference Model §1; `agent_instance.py`'s real design).
- Each version (after the first for its identity) carries a **supersession linkage** to the version it supersedes (Blueprint v3 §2.2: revision "supersedes the previous version"). The Repository stores this linkage opaquely — it is data the creating subsystem supplied, not something the Repository computes or interprets. The Repository never walks the chain to decide which version is current; that derivation is the Knowledge Service's concern (§3, §17).
- [E] **Stability requirement met:** the identity key must be genuinely stable across versions (the `memory_id`-instability counter-example from the Reference Model §4 is the cautionary precedent). The key is assigned once, at first-version creation, and every subsequent version of that identity carries the identical key unchanged. The Repository preserves it verbatim; it never regenerates it.

## 12. Provenance Responsibilities (directive item 12)

[E] Per Blueprint v3 §2.5 (provenance permanence model) and PR-5:

- The Repository **stores, preserves permanently, and returns unaltered** the full provenance each version carries: Originating Department, the reviewing/creating actor, the reference to the creating action's Trace record, the source Memory snapshot, and supporting Trace references — all permanent.
- **Home Department** is the one provenance element Blueprint v3 marks reassignable — but **reassignment is not a Repository concern.** Because versions are immutable, a Home Department reassignment does not mutate an existing version; it is a separate governed record produced elsewhere. The Repository stores whatever Home Department value a version carried at creation and never changes it. The *current* Home Department is derived elsewhere (Knowledge Service) from the version's stored value plus any reassignment records — exactly as validity and lifecycle are derived, not stored-mutably.
- The Repository **captures nothing new** as provenance — provenance is assembled by Provenance Services [BUILT] before a version arrives. The Repository's role is preservation, not assembly (PR-5: capture happens at decision time, upstream; the Repository durably holds the captured result).

## 13. Trace Responsibilities (directive item 13)

[E] Per Domain Model invariant 4 and the Reference Model §4 (Trace Boundary):

- The governed action that creates a version (admission, or a future revision) is performed by **another subsystem**, which produces the Trace record for that action. The Repository does not make governed decisions, does not spawn Agent Instances, and does not orchestrate — those are explicit non-responsibilities (§3). Therefore the Repository does **not** author the admission/revision Trace record.
- The Repository's trace responsibility is **linkage integrity**: it refuses to store any version that does not carry a reference to the Trace record of the action that created it (part of §16 validation). This guarantees every durable Knowledge version is permanently traceable to the governed action that produced it — satisfying invariant 4's spirit at the Knowledge layer without the Repository itself becoming a traced actor.

[O] **Open question OQ-2 (storage-event tracing):** whether a Repository *storage write* is itself "an Agent Instance action" requiring its own distinct Trace record (invariant 4), or whether it is pure infrastructure performed *within* the caller's already-traced action and needs no separate record. This design **leans toward the latter** [A] — the Repository is infrastructure, not an Agent Instance; the caller's action is the traced action — consistent with how `TraceWriter` (also infrastructure) is not itself a separately-traced actor. But this is a genuine invariant-interpretation question flagged for the Architect, not silently resolved. It does not block the design of storage/retrieval; it affects only whether an additional record type exists.

## 14. Lifecycle Responsibilities (directive item 14)

[E] The Repository's lifecycle responsibilities are deliberately **minimal**, because lifecycle *position* (Active/Superseded) is derived, not stored-mutably:

- The Repository stores each version immutably, including its supersession linkage (§11). This is the **raw material** from which lifecycle position is derived.
- The Repository **does not assign, change, or evaluate** a version's lifecycle position. It never marks a version "Superseded" — doing so would be a mutation (forbidden) and an evaluation (not its concern). "Active" and "Superseded" are derived by the Knowledge Service from the version set + supersession linkage.
- [E] This resolves the apparent tension between "versions are immutable" and "a version *becomes* Superseded": becoming Superseded is not a change to the version record — it is a change in what the *derivation* returns once a newer version exists. The version record itself is identical before and after; only its position in the derived chain differs. The Repository stores the unchanging record; the Service derives the changing position.

## 15. Failure Modes (directive item 15)

[E] Every failure mode fails closed (PR-4):

| Failure | Repository behavior (fail closed) |
|---|---|
| Store request with incomplete structure (§16) | Refuse; store nothing partial; return an explicit validation failure |
| Store request lacking a creating-action Trace reference | Refuse (§13 linkage integrity) |
| Store request lacking a stable identity key | Refuse (§11) |
| Retrieve by a non-existent address | Explicit not-found; never a nearest-guess, never fabrication |
| Retrieve by an identity key with no versions | Explicit empty result; never a fabricated version |
| **Any** request to mutate a stored version | Refuse absolutely (append-only invariant, R6) |
| **Any** request to delete a stored version | Refuse absolutely (inv. 5 analogue) |
| A stored record found unreadable/corrupt on retrieval | Fail closed — report unreadable; never reconstruct or guess content (PR-4; the `verification.py` deleted-file lesson: unverifiable ≠ trusted) |
| Duplicate version address collision on store | Refuse — addresses are never reused (§10) |

[E] There is no failure mode whose default is "trust" or "proceed anyway." The Repository's failure posture is uniform refusal.

## 16. Validation Responsibilities (directive item 16)

[E] Before a version enters durable retention, the Intake Gate validates (structural/presence only — never governance, never quality; PR-4 fail-closed, and never evidence-quality-based per the Human Review boundary):

- Identity key present and non-empty (§11).
- Content present.
- Provenance present and complete per the §12 permanence model.
- Creating-action Trace reference present (§13).
- Supersession linkage present, **or** the version explicitly declares itself the first version of its identity (exactly one of the two — ambiguity is a validation failure, fail closed).
- Version address issuable and unique (§10).

[E] The Repository **does not validate**: whether admission was legitimate, whether content is true or high-quality, whether a conflict exists, whether the reviewer had authority — all are other subsystems' concerns (§3). Validating any of them would absorb another concern.

## 17. Interaction With Other Subsystems (directive item 17)

[E] Per Reference Model §4 (collaboration ≠ ownership; authority verified by the acting subsystem; evidence flows up, never down as authority):

- **Admission → Repository:** Admission, having made a governed admission decision (and produced its Trace record), hands the Repository a structurally complete first version to store. The Repository validates and stores; it does not re-decide admission. *Collaboration, not ownership* — Admission owns the decision; the Repository owns the storage.
- **Knowledge Service → Repository:** the Service retrieves versions (by address or identity) and *derives* current-Active position, validity, and current Home Department from what the Repository returns plus Trace records. The Repository supplies raw versions; the Service interprets. The Repository never performs the Service's derivation.
- **Retrieval → Repository (indirect):** Retrieval consumes derived, interpreted Knowledge (via the Service), applying visibility policy across the two axes — a policy that is [O] open (Blueprint v3 #6). Retrieval does **not** reach into the Repository to filter by validity/lifecycle; those dimensions are derived above the Repository. The Repository has no visibility-policy responsibility.
- **Trace ↔ Repository:** the Repository consumes Trace only as provenance linkage (a version references its creating action's Trace record); it does not write orchestration Trace records (§13). Trace remains the independent, append-only audit spine; the Repository depends on it, never the reverse.
- **Memory → Repository:** **no direct interaction, and this is deliberate.** Memory is upstream and provisional; a version's *source* Memory is captured as a snapshot at admission time (upstream, by Provenance Services) and arrives inside the version's provenance. The Repository never reads live Memory, and Memory can never override or drive Repository content (Blueprint v3: Memory cannot override Knowledge; Reference Model §4: evidence flows up, never down as authority).

## 18. Assumptions (directive item 18)

- [A] **A-1:** The creating subsystem (Admission/Revision) assembles a structurally complete version — including provenance, identity key, and Trace reference — *before* handing it to the Repository. The Repository validates presence but relies on upstream assembly for content correctness. (Consistent with the [BUILT] Provenance Services owning assembly.)
- [A] **A-2:** The identity key's stability is guaranteed by its assigner (Admission at first-version time), not enforceable by the Repository alone — the Repository preserves it but cannot verify it was *chosen* stably. (The `memory_id` lesson: stability is a property of the assigner's discipline.)
- [A] **A-3:** Deriving lifecycle/validity from versions + Trace is tractable for the Knowledge Service — assumed by analogy to the proven Memory Governance derivation, not yet demonstrated at Knowledge scale.

## 19. Risks (directive item 19)

- [E] **RK-1 — Dual-durability confusion:** because both Trace (admission snapshot) and the Repository (version record) durably hold version content, a future implementer could treat them as redundant and drop one. Mitigation: §1's explicit statement that they are different artifacts (action-record vs. durable-entity), not duplicates. Highest-consequence risk.
- [E] **RK-2 — Concern absorption:** the strong temptation to let the Repository answer "which is the current version?" (a one-line derivation) would silently absorb the Knowledge Service's concern and violate the Non-Responsibilities. Mitigation: §8's deliberate absence of an evaluation component, stated as intentional.
- [E] **RK-3 — Immutability erosion under lifecycle pressure:** the intuition that a version "becomes Superseded" invites a mutable status field. Mitigation: §14's explicit resolution (position is derived, the record is unchanging).
- [A] **RK-4 — Address permanence under future storage choices:** a later indexing/storage-technology decision (out of scope here) could threaten address permanence (§10). Mitigation: flag address permanence as a hard constraint any future implementation-planning phase must preserve.

## 20. Open Questions (directive item 20)

| # | Question | Classification | Owner |
|---|---|---|---|
| OQ-1 | Version address form (opaque vs. structured) | Resolve during implementation planning | Repository implementation planning |
| OQ-2 | Whether a Repository storage-write is a separately-traced Agent Instance action (inv. 4) | **Must resolve before implementation** — it determines whether an additional Trace record type exists | Architect (invariant interpretation) |
| OQ-3 | Whether lifecycle/validity derivation belongs entirely to the Knowledge Service or partly needs Repository-stored ordering beyond the supersession link | Resolve during Knowledge Service design | Knowledge Service design phase |
| OQ-4 (inherited) | Retrieval visibility policy across the two axes (Blueprint v3 #6) | Not a Repository question — noted for completeness | Retrieval design |

None silently resolved. OQ-2 is the one that gates Repository *implementation* (not its design), and is an Architect invariant-interpretation call.

## 21. Consistency Review (directive item 21)

- [E] **Constitution:** the Repository makes no governance decision and holds no authority (§3); it cannot violate §6.2 invariant 2. No contradiction.
- [E] **Domain Model:** append-only + no-delete (§15, R6) honors inv. 5; provenance linkage (§13) serves inv. 4; no automatic promotion into Knowledge occurs in the Repository (it stores what governed decisions produced) — inv. 8 untouched. No contradiction.
- [E] **Principles Register:** PR-1 (nothing speculative — every element traces to a settled decision or a flagged open question); PR-2 (lifecycle vs. validity kept as derived axes, never stored as one status); PR-4 (uniform fail-closed §15); PR-5 (stores captured snapshots, preserves provenance, never live-references). PR-3 (Detect-Don't-Decide) is satisfied vacuously — the Repository neither detects nor decides governance. No contradiction.
- [E] **Blueprint v3:** version-as-immutable-addressable-record (Decision 1), append-only-versioned (Decision 4), identity-as-correlation-key (Decision 1), provenance permanence (§2.5) — all implemented faithfully; nothing Knowledge-specific is redesigned. No contradiction.
- [E] **Engineering Design Standard:** all 17 template sections present; every failure fails closed; dependencies §5-legal and acyclic; decision points — the Repository has **no governed decision point** (its only "decisions" are structural validation pass/refuse, which are not governance decisions). No contradiction.
- [E] **Reference Subsystem Engineering Model:** eight boundaries identified (§2, §4, §5); Ownership/Authority boundaries fixed before Data/Trace; collaboration distinguished from ownership (§17); the deliberate absence of an evaluation component honors Single Responsibility. No contradiction.
- [E] **Implementation Architecture Plan:** the Repository is built on [BUILT] dependencies only, reused as-is; it is the root of the Knowledge Infrastructure layer, sequenced first. No contradiction.

**Contradictions found: none.** Assumptions, risks, and open questions are all surfaced explicitly above; none was silently resolved.

---

## Completeness Evaluation

[E] **The Knowledge Repository Detailed Design is sufficiently complete for future implementation planning, with one gating item.** It fully specifies the subsystem's purpose, its complete responsibility/non-responsibility split, all eight boundaries, its minimal internal structure (notably the *deliberate absence* of any evaluation component), version addressing and identity management grounded in settled Blueprint v3 decisions, provenance/trace/lifecycle/validation/failure responsibilities all consistent with every canonical source, and every inter-subsystem interaction with collaboration cleanly separated from ownership.

**The one gating item [O]:** OQ-2 (whether a Repository storage-write is a separately-traced Agent Instance action) is an Architect invariant-interpretation decision that must be resolved before *implementation* — though not before *implementation planning* — because it determines whether an additional Trace record type exists. Every other open question is resolvable during a later phase and does not gate progress.

**Remaining weaknesses (explicit):** the three [A] assumptions (§18) are reasoned, not yet demonstrated — chiefly A-3 (that Knowledge Service derivation is tractable at scale), which will only be confirmed when the Knowledge Service is designed and, later, exercised.

No implementation was begun. No Admission design was begun. No code, schema, database, API, class, pseudocode, UML, storage technology, or indexing strategy was produced. Stopping here. Awaiting explicit Architect authorization.
