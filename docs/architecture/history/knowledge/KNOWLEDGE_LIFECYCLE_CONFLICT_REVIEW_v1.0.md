# Knowledge Lifecycle & Conflict Resolution — Architecture Review v1.0

**Status:** Architecture review and recommendation only. No code, schema, API, storage design, or governance-document change occurs here.
**Version:** v1.0
**Authority:** Subordinate to the ratified Canonical Domain Model and Constitution. Built on the now-approved baseline: **Knowledge Admission Model = Option B** (separate admission decision, layered on existing Human Review infrastructure) and **Knowledge Ownership Model = Option C with condition** (Originating Department = provenance/history; Home Department = accountability ownership; Reviewer ≠ automatic owner; ownership assignment must remain an explicit reviewed decision).
**Evidence tags**: **[E]** evidence-backed, **[A]** assumption requiring validation, **[O]** open question.

---

## 1. Decision Context

Two approved baseline decisions now exist. This review determines the architectural principles — not the implementation — for how a Knowledge item behaves once admitted (Lifecycle) and how AIOS should treat disagreement between Knowledge items, Memory, and evidence (Conflict Resolution). Every finding below is evaluated against the ratified Domain Model, the Constitution, and real, already-proven patterns in this codebase (Trace's append-only model, the Human Review `edit` decision's preserve-original behavior, `memory_governance.detect_conflicts()`'s surface-never-resolve behavior) rather than invented from first principles.

---

## Part 1 — Knowledge Lifecycle Review

### 1. Knowledge Creation Lifecycle

**Current architectural understanding**: Memory → Candidate → Admission Decision (Option B, now approved) → Knowledge Creation → Versioning → Supersession → Retirement.

**Is this consistent with Domain Model §6 ("revised/superseded via review; not casually deleted")?**
[E] Yes. Every step in this pipeline funnels through governed human review before any Knowledge state exists at all, and nothing in it proposes deletion — only creation, versioning, and supersession, all human-decided. **Adopt.**

**Does append-only-versioned remain the correct lifecycle model?**
[E] Yes, and it is the best-evidenced choice available: Trace's append-only model is proven at real scale (540 records, zero mutations across this entire arc), and the real `edit` decision (`trace-502ab65e9b0f`) already demonstrates, in miniature, exactly this pattern — original preserved, correction added as a new, separate, permanent record, nothing overwritten. Extending this to Knowledge is not a new invention; it is the same proven pattern at entity scale. **Adopt.**

**What lifecycle states are required?**
[E]/[A] Building on the 8-state exploration in `KNOWLEDGE_LIFECYCLE_CONTRACT_v1.0.md`, re-evaluated now that Admission Model B is fixed: **Candidate** [E, strong real precedent] → **Admitted** [A, now a real, distinct decision under Option B] → **Active** [E, structurally simple, mirrors Memory's "fresh" state] → **Revision Required** [O, exact trigger undefined] → **Deprecated** [partial E via the real `reject` precedent, never yet applied to an Active entity] → **Superseded** [O, zero real precedent anywhere in this repository, confirmed by direct search in a prior phase] → **Archived/Retired** [O, newly introduced by this directive; not previously explored — see below].

**Archival vs. Deprecation — newly surfaced ambiguity**: [O] this directive introduces "archival" as distinct from every prior document's "deprecated"/"superseded" pair. No evidence in the Domain Model or this codebase distinguishes them. Recommend treating this as a genuinely open question rather than assuming a distinction exists — Domain Model §6's language ("not casually deleted") is satisfied by either a Deprecated or an Archived state equally; nothing ratified requires both.

**Which transitions require human authority?**
[E] All of them, without exception, per invariant 8 extended by the standing no-automation-over-governance principle this entire arc has held (proven by every AST-verified test on `review_decision.py`). **Adopt** unconditionally.

**Which transitions can be automated?**
[E] None of the state transitions themselves — but *detection* that a transition may be warranted can and should be automated, exactly matching `detect_conflicts()`'s real, proven architecture: automated detection, human-decided action. This distinction (detect vs. decide) is itself a reusable pattern, not a new one. **Adopt.**

**Where should Trace records be produced?**
[E] At every lifecycle transition, exactly one Trace record each — this is not a new design choice, it is a direct, mandatory consequence of Domain Model invariant 4 ("every Agent Instance action produces exactly one Trace record — production is unconditional"). **Adopt.**

**What provenance must survive across lifecycle transitions?**
[E] A full, self-contained snapshot at each transition moment — reusing the exact `candidate_snapshot` pattern already proven in Human Review (immutable, `asdict()`-captured, never a live reference). This directly satisfies Domain Model §6.1's requirement that Trace's explainability never depend on the continued existence of anything it references. **Adopt.**

**Missing lifecycle boundaries identified**: [O] the boundary between "Revision Required" (a signal) and an actual executed "Revision" (a new version) is not cleanly separated anywhere in the source material for this review — this needs explicit definition before implementation, not assumed.

---

### 2. Knowledge Revision Model

**How should a Knowledge item evolve after creation?**
[E]/[A] Best-evidenced answer: reuse the real `edit` decision's proven shape — original content preserved untouched, a new, explicit, human-authored revision recorded separately, nothing overwritten. **Adapt** (the pattern is proven at candidate scale; applying it at entity scale is a reasonable, evidence-grounded extension, not a leap).

**What triggers revision?**
[O] Genuinely unresolved. Three plausible triggers exist with no evidence favoring one: new contradicting evidence (automated detection + human decision, per `detect_conflicts()`'s pattern), human-initiated review, or an evidence-verification failure (Tier 2-style fingerprint mismatch applied at the Knowledge layer). No real Knowledge entity has ever existed to observe which of these actually occurs in practice.

**How should old versions relate to new versions?**
[E]/[A] An explicit backward link (supersedes/superseded-by), with the old version retained permanently and marked, never deleted — consistent with the append-only-versioned conclusion above. **Adopt** the general shape; **Defer** the concrete field design (explicitly out of scope for this design-only review).

**Should revisions create new identities or new versions of the same identity?**
[E] **New versions of the same, stable identity.** This is a clean, evidence-grounded conclusion, not a preference: Domain Model §6 requires Knowledge be "versioned" — versioning presupposes one persistent identity across versions, which is structurally the opposite of Memory's deliberately unstable identity (`memory_id` regenerates every extraction, a proven, documented, load-bearing property of Memory throughout this entire arc). Knowledge needs precisely what Memory was deliberately built without. **Adopt.**

**How should historical correctness be preserved?**
[E] Via the same durability principle Trace and the `edit` decision already prove in this codebase — nothing overwritten, everything permanently inspectable. **Adopt.**

---

### 3. Knowledge Expiration vs. Revision

**Is there any scenario where Knowledge should expire (like Memory)?**
[E] No — direct contradiction with Domain Model §6's explicit "durable... not casually deleted" language. Memory's retention-window expiry model is deliberately *not* what Knowledge is defined to be. **Reject** "Knowledge expires automatically like Memory."

**Should stale Knowledge exist?**
[E] Yes, in the sense of remaining visible and queryable while flagged (e.g. "Revision Required"), never silently hidden — this matches the standing "never silently resolve, always surface" principle `detect_conflicts()` already proves in real code. **Adopt.**

**How should outdated Knowledge be represented?**
[A] A status field distinguishing Active from Revision-Required/Deprecated, not removal or silent suppression — follows directly from the above, but the field's concrete shape is undecided (design-only scope).

---

### 4. Knowledge Provenance Lifecycle

Evaluated directly against the now-approved Ownership Model's explicit distinction (Originating Department = provenance; Home Department = accountability, reassignable only via explicit reviewed decision):

| Provenance element | Permanent? | Can it change? | Reasoning |
|---|---|---|---|
| Originating Department | [E] Yes | No | A historical fact, per the approved condition — matches Trace's own immutability principle |
| Reviewing Actor (per decision) | [E] Yes | No | Matches `reviewer_identity`'s already-proven real pattern — a past decision's actor cannot un-happen |
| Home Department | [A] Current value only | **Yes**, but only via an explicit, new, reviewed reassignment record | The one deliberately changeable element, per the approved condition — reassignment must itself be a new Trace record, never an edit to the old one, preserving full history |
| Admission Decision record | [E] Yes | No | It is a Trace record — permanent and immutable by invariant 5 |
| Source Memory | [O]/[E] The *snapshot*, yes; a *live reference*, no | N/A | Memory has no stable identity (proven, this arc's central Memory finding) — what must be captured is a snapshot at admission time, exactly like `candidate_snapshot`, never a live pointer back to recomputable Memory |
| Supporting Trace references | [E] Yes | No | Trace records never disappear, per invariant 5 — references remain valid permanently |

**Which must never disappear?** Everything above except that Home Department's *current* value is reassignable — but every past Home Department assignment must remain permanently visible, mirroring Trace's own full-history-preservation principle exactly.

---

## Part 2 — Knowledge Conflict Resolution Review

### 1. Conflicting Knowledge Items ("Strategy X works" vs. "Strategy X fails" under the same condition)

**Can both exist?**
[E] Yes — matches the proven `detect_conflicts()` philosophy of surfacing, never silently resolving or blocking. Nothing in the ratified Domain Model prohibits two Knowledge items existing in a declared-conflicting state. **Adopt.**

**Should one supersede another?**
[A] Only through an explicit, human, reviewed decision — never automatically, per invariant 8's spirit extended to conflict resolution by direct analogy.

**Who decides?**
[A] Under the approved Ownership Model, first-line authority plausibly rests with the Home Department accountable for the conflicting item(s) — see §4 below for the full analysis.

**What evidence is required?**
[O] Unresolved — no real admission or conflict has ever occurred to observe what a real reviewer would actually want here.

---

### 2. Conflicting Memory → Knowledge Promotion (Memory cluster A supports a claim, cluster B contradicts it)

**Should conflict block admission?**
[A] Not an outright block, but it should force the candidate through explicit escalated human attention rather than the ordinary admission path — mirroring `detect_conflicts()`'s real behavior of surfacing without silently blocking or silently passing through.

**Should it create review escalation?**
[E] Yes. This is directly, strongly grounded in ratified text: Domain Model §10's Architectural Backlog entry on "Escalation/Incident" states escalation is *already* "adequately handled procedurally via the existing Decision-Making Process plus Trace's success/failure/escalation status field" — this is not a new mechanism to invent, it is an existing, ratified mechanism to reuse. **Adopt.**

**Should confidence ranking decide?**
[E] No. Direct contradiction of the already-proven real pattern: `promotion.py`'s confidence/occurrence signals have never gated eligibility, only prioritized ranking, across this entire arc's history. Allowing confidence to *decide* a conflict outcome would also contradict invariant 8's never-automatically language. **Reject.**

---

### 3. Knowledge vs. External Evidence Conflict (existing Knowledge conflicts with new Trace/Memory)

**Does Knowledge remain authoritative?**
[A] Yes, by default, until a governed revision or deprecation decision changes it — consistent with the durability principle throughout this review.

**Does new evidence trigger review?**
[E] Yes — mirrors Tier 2 Evidence Verification's own real, proven, live-tested pattern: a fingerprint mismatch triggers re-verification, never silent override, never silent dismissal. Applying the same shape at the Knowledge layer (new evidence → flag for review, never automatic action) is a direct reuse, not a new pattern. **Adopt.**

**Can Memory override Knowledge?**
[E] No. Direct contradiction of Domain Model §6.1's explicit principle that Trace's (and by the same reasoning, Knowledge's) durability guarantee must never depend on any other entity's continued existence — Memory is explicitly the more volatile, provisional entity; allowing it to silently override the more durable one would invert the ratified hierarchy. **Reject.**

---

### 4. Conflict Resolution Ownership

[A] Under the approved Ownership Model, recommend: the **Home Department** holds first-line conflict-resolution authority for conflicts entirely within its own accountability scope. For conflicts spanning two different Home Departments, recommend escalation through the existing Decision-Making Process, by direct analogy to Domain Model invariant 10 ("Cross-Department Capability dependencies require governance approval... never silent adoption") — noting explicitly that invariant 10 is literally scoped to Capability dependencies, not Knowledge conflicts, so this extension is **[A]**, an analogy-based assumption requiring explicit Architect ratification, not a literal reading of ratified text.

---

## Part 3 — Architecture Patterns

| Pattern | Principle | Why it fits AIOS | Recommendation | Domain Model alignment |
|---|---|---|---|---|
| Event sourcing | Every state change is a new, permanent, immutable event | **[E]** This is not a pattern to adopt — it is the pattern Trace already *is*, proven at 540-record real scale with zero mutations | **Adopt**, unchanged, for the Knowledge lifecycle | Directly matches Domain Model §7 invariant 5 |
| Versioned entity model (stable identity + version chain) | One persistent identity, many ordered versions | **[E]/[A]** No real precedent exists yet in this codebase for *entity-level* versioning (only independent event append) — this is genuinely new relative to what's built, though it extends a proven base | **Adapt** — the single largest net-new pattern this review identifies | Required by Domain Model §6's "versioned" language for Knowledge specifically |
| Provenance chains | Every derived artifact traces back to its real source | **[E]** Proven unbroken across this arc's entire history (Trace→Memory→Candidate→Decision) | **Adopt**, unchanged, for Knowledge | Domain Model §6.1 |
| Human-in-the-loop governance | No automated decision anywhere in the governance path | **[E]** The single most proven pattern in this codebase — AST-verified absence of automated decision logic across every phase | **Adopt**, unconditionally | Invariant 8, Constitution §6.2 invariant 2 |
| Conflict escalation | Surface conflicts through the existing Decision-Making Process rather than a new mechanism | **[E]** Directly grounded in ratified Domain Model §10 text, not invented | **Adopt** | Domain Model §10 (Architectural Backlog, Escalation/Incident) |
| Evidence-weighted automated resolution | Let a confidence/similarity score decide an outcome | **[E]** Directly contradicts the proven "prioritization only, never eligibility or decision" pattern used everywhere in this codebase | **Reject** | Invariant 8 |
| Knowledge graph readiness (many-to-many relational design from the start) | Design Knowledge with rich graph relationships up front | **[O]** No evidence either way; Domain Model neither mandates nor forbids it; no real usage pattern exists yet to justify the complexity | **Defer** | Constitution's engineering principle against building ahead of demonstrated need |

---

## Part 4 — Knowledge Lifecycle Decision Package v1.0

### 1. Decisions Already Resolved
- Knowledge Admission Model: **Option B** (approved).
- Knowledge Ownership Model: **Option C with condition** (approved) — Originating Department = provenance, Home Department = accountability, Reviewer ≠ owner, reassignment always explicit and reviewed.

### 2. Decisions Recommended (this review)
- Append-only-versioned lifecycle with a **stable Knowledge identity** — **Adopt**.
- Revision reuses the real `edit` decision's preserve-original pattern — **Adapt**.
- Knowledge never automatically expires; only governed deprecation/supersession ends Active trust — **Adopt** the principle, **Reject** automatic time-based expiry.
- Provenance permanence table (§4 above) — **Adopt**.
- Conflicts are never silently resolved; always surfaced/escalated — **Adopt**.
- Confidence/similarity scores never decide eligibility, admission, or conflict outcomes — **Reject** as a decision mechanism (retained only as prioritization input, already proven elsewhere).
- Memory cannot override Knowledge automatically — **Reject**.
- Event-sourcing/append-only base — **Adopt**.
- Versioned-identity pattern — **Adapt** (flagged as the single largest genuinely new pattern).
- Human-in-the-loop for every lifecycle and conflict decision — **Adopt**, unconditionally.
- Knowledge graph readiness — **Defer**.

### 3. Remaining Open Questions
- Exact trigger definition for "Revision Required" [O].
- Whether Archival is architecturally distinct from Deprecated, or the same concept under two names [O].
- What evidence threshold conflict resolution requires before a decision can be made [O].
- Cross-Department conflict escalation authority — currently only an analogy to invariant 10, not ratified for this purpose [A, requires explicit Architect ratification].
- Source-Memory snapshot mechanics detail — design principle adopted, concrete shape deferred [O].
- The precise boundary between a "Revision Required" signal and an executed "Revision" [O].

### 4. Risks
- The versioned-identity pattern is the primary implementation risk once building begins — unlike nearly everything else in this review, it has no direct real precedent in this codebase to build from, only a proven base (event sourcing) to extend.
- Cross-Department conflict escalation, if implemented on the current analogy-based assumption without explicit ratification, risks applying invariant 10 outside its literally ratified scope.
- "Revision Required" and "Revision" remaining conflated in implementation would blur the detect-vs-decide separation this review otherwise establishes cleanly.

### 5. Dependency Impact
- The concrete lifecycle state set (still open) blocks any conflict-resolution implementation, since conflict outcomes need defined states to transition between.
- The provenance permanence table depends on the Ownership Model being fixed — now resolved, this is unblocked.
- The versioned-identity decision must be settled before any admission implementation begins, since Option B's "create" step must know whether it is creating a first version of a new identity or something else.

### 6. Recommended Next Architectural Decision Order
1. Finalize the concrete lifecycle state set and per-state transition authority (building directly on this review's append-only-versioned conclusion and the 8-state exploration already on record).
2. Decide the Revision trigger mechanism.
3. Decide the conflict-resolution evidence threshold.
4. Only then: an implementation design phase — not authorized by this review.

---

No code, schema, API, storage design, or governance document was created or modified. Stopping here per the directive. Awaiting Architect authorization before any further phase.
