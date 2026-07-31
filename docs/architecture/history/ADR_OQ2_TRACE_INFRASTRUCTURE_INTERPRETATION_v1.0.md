# ADR — OQ-2: Trace / Infrastructure Interpretation of Invariant 4 v1.0

**Status:** Architectural Decision Review. Determines the correct interpretation of Domain Model Invariant 4 for infrastructure operations. No implementation, schema, API, code, pseudocode, or subsystem redesign. Modifies no existing design.
**Version:** v1.0
**Scope:** OQ-2 only — "Is a Knowledge Repository storage-write a separately-traced Agent Instance action under Invariant 4?" — generalized to its real form: *how Invariant 4 applies to infrastructure operations across AIOS.*
**Confidence discipline:** **[E]** evidenced · **[A]** assumption · **[O]** open question.

---

## 1. The Exact Ratified Text Under Interpretation

- [E] **Domain Model Invariant 4:** "Every **Agent Instance action** produces exactly one Trace record — production is unconditional, never optional."
- [E] **Domain Model, Agent Instance:** "A single, ephemeral **runtime execution of an Agent Definition**. Hosted by a Runtime. Has its own execution lifecycle (spawned → active → terminated)... **Produces Trace.**"
- [E] **Domain Model, Trace:** "the immutable, append-only, unconditional audit record of **one Agent Instance action**."
- [E] **Constitution §14.2 (Operational AI Agents):** "Produce a Trace for every action, without exception."

[E] **The decisive textual fact:** Invariant 4's subject is not "every operation" or "every write" — it is "every **Agent Instance action**." Invariant 4 does not say infrastructure produces Trace; it says *Agent Instance actions* produce Trace. The interpretation question is therefore prior to OQ-2 as posed: **is a Repository storage-write an Agent Instance action at all?** If it is not, Invariant 4 does not reach it, and OQ-2's "should it be separately traced" question is answered by the scope of the invariant, not by a new rule.

## 2. Questions Answered

**Q1 — What exactly qualifies as an Agent Instance action?**
[E] An action performed by *a runtime execution of an Agent Definition* (the ratified Agent Instance definition). It has the Agent Instance's spawned→active→terminated lifecycle context; it is a thing an *agent* does. In the real [BUILT] system, an Agent Instance action is what `orchestrator.run()` and `review_decision.record_decision()` perform: a spawned instance, bound to a Runtime, executing on behalf of an Agent Definition, producing evidence. The Trace record's own required fields (`agent_definition_name`, `agent_instance_id`, `runtime`) confirm this — a Trace record is *shaped* to describe an Agent Instance's action; it has no coherent meaning for an actorless infrastructure call.

**Q2 — Is infrastructure activity itself an Agent Instance?**
[E] **No.** Infrastructure (Trace's `TraceWriter`, the Repository's storage) is not "a runtime execution of an Agent Definition." It has no Agent Definition, no instance lifecycle, no Runtime binding of its own. The [BUILT] `agent_instance.py` and `TraceWriter` are two different categories: one is an actor, the other is a facility the actor uses. `TraceWriter` is real, tested infrastructure and is demonstrably **not** itself an Agent Instance.

**Q3 — Is Repository persistence an execution action or an internal infrastructure responsibility?**
[E] An **internal infrastructure responsibility**, per the Repository Detailed Design §3 (workflow orchestration and authority decisions are explicit non-responsibilities) and §8 (the Repository has no evaluation/decision component). Persistence is a facility the *creating* subsystem's action uses, not an action the Repository performs as an agent.

**Q4 — Should infrastructure operations create independent Trace records?**
[E] Answered structurally by Q1–Q3: if infrastructure is not an Agent Instance, Invariant 4 does not require it to. Whether it nonetheless *should* is the options analysis (§4). **The strongest single argument is infinite regress** (§3, RG-1 below).

**Q5 — If infrastructure operations are independently traced, what consequences follow?**
[E] (a) An **infinite-regress problem** for Trace's own writer; (b) a **proliferation** of low-value records (every storage write, every read?) diluting the audit corpus; (c) a **category error** in the Trace record itself (what `agent_definition_name` does a Repository write carry?); (d) a new, ratified expansion of what "Agent Instance action" means — a Domain Model change, which this review is not authorized to make.

**Q6 — If infrastructure operations are not independently traced, what preserves auditability?**
[E] **Provenance linkage** (Repository Design §13): every stored version references the Trace record of the *governed action that created it*. The governed action (admission/revision) IS an Agent Instance action and IS traced (one record, Invariant 4 satisfied). The storage is auditable *through* that record, plus the durable version itself. Auditability is preserved without the storage being a separate traced actor — exactly how `TraceWriter.write()` is auditable (the record it writes describes the agent action) without `TraceWriter` tracing itself.

**Q7 — Which interpretation is most consistent with the principles?**
[E] Tabulated in §5. Summary: the "infrastructure is not a separately-traced Agent Instance" interpretation is consistent with all of Evidence First, Fail Closed, Capture-Don't-Reference, Trace immutability, Provenance, and Separation of Concerns; the "independently traced" interpretation strains Separation of Concerns and creates the regress.

## 3. The Regress Argument (RG-1) — the pivotal evidence

[E] If Invariant 4 were interpreted to require that *every infrastructure persistence operation* produces its own Trace record, then **`TraceWriter.write()` — the operation that writes a Trace record — would itself require a Trace record**, whose writing would require another Trace record, ad infinitum. The real [BUILT] system does not do this and cannot: `TraceWriter` writes Trace records for Agent Instance actions and produces no record *of its own writing*. Therefore Invariant 4 **already, in the ratified running system, does not cover infrastructure persistence operations** — not as a new decision, but as an existing, necessary fact. Any interpretation that would trace Repository persistence as an Agent Instance action must either exempt `TraceWriter` (special-casing, unprincipled) or accept infinite regress (impossible). This is close to decisive.

## 4. Options (three interpretations, none selected prematurely)

### Option A — Infrastructure persistence is NOT an Agent Instance action; not independently traced. Auditability via provenance linkage.
- **Strengths:** [E] avoids RG-1 entirely; matches the ratified Agent Instance definition (Q1–Q2); matches the [BUILT] `TraceWriter` precedent exactly; keeps the audit corpus meaningful (records describe agent actions); zero new record types; Separation of Concerns intact (the Repository stays storage-only).
- **Weaknesses:** [A] relies on provenance-linkage discipline being enforced (Repository Design §16 already mandates refusing versions lacking a creating-action Trace reference); a naive reader might think "the storage moment" is unaudited (it is audited, through the creating action + the durable version, just not as its own record).
- **Consistency with canonical architecture:** [E] full — Domain Model, Trace Architecture, Repository Design, Engineering Standard all consistent.
- **Future scalability:** [E] excellent — infrastructure can grow without multiplying Trace volume.
- **Implementation implications:** none new — the Repository stores; the creating subsystem traces.
- **Audit implications:** [E] every version remains fully auditable to its governed origin; the audit spine stays actor-scoped and legible.
- **Engineering complexity:** lowest.

### Option B — Repository persistence IS an Agent Instance action; independently traced.
- **Strengths:** a literal, maximal reading of "Trace for every action"; a very granular audit trail of storage events.
- **Weaknesses:** [E] triggers RG-1 (must special-case `TraceWriter` or accept regress); forces a category error (a Repository write has no Agent Definition/Runtime); requires either the Repository to spawn Agent Instances (violating its §3 non-responsibilities: no orchestration, no authority) or a redefinition of "Agent Instance action" (a Domain Model change, out of scope); dilutes the audit corpus with actorless records.
- **Consistency:** [E] **contradicts** the Agent Instance definition, the Repository Design's non-responsibilities, and (via regress) the running Trace Architecture. Multiple contradictions.
- **Future scalability:** [E] poor — Trace volume grows with every infrastructure op.
- **Implementation implications:** the Repository would need orchestration/instance-spawning it is explicitly forbidden.
- **Audit implications:** superficially richer, actually noisier and category-confused.
- **Engineering complexity:** highest.

### Option C — Not independently traced, AND the creating action's Trace record explicitly captures the storage outcome.
- **Description:** Option A, refined — the governed action's single Trace record (admission/revision) records, within its own outputs, that a version was durably stored and at which address. One Trace record per governed action (Invariant 4 satisfied), and the storage outcome is captured *inside* it (Capture-Don't-Reference applied).
- **Strengths:** [E] all of Option A's strengths, plus the storage outcome is explicitly present in the audit record rather than only inferable from the version's back-reference; strengthens PR-5 (the creating action captures its own consequence).
- **Weaknesses:** [A] requires the creating subsystem (Admission/Revision) to receive the storage outcome back from the Repository and include it — a minor coupling, already implied by any store-then-record sequence; touches Admission's future design, not the Repository's.
- **Consistency:** [E] full — same as Option A, with an added PR-5 reinforcement; no contradiction.
- **Future scalability:** [E] excellent.
- **Implementation implications:** a note for the future Admission design (the storage outcome flows back into the admission Trace record); none for the Repository beyond returning the outcome it already produces.
- **Audit implications:** [E] strongest of the three — auditability via *both* the creating record's explicit capture *and* the version's provenance back-reference (bidirectional).
- **Engineering complexity:** low (marginally above A).

## 5. Principle-Consistency Matrix

| Principle | Option A | Option B | Option C |
|---|---|---|---|
| Evidence First (PR-1) | [E] consistent — no speculative record type | strained — invents actorless records with no demonstrated need | [E] consistent |
| Fail Closed (PR-4) | [E] consistent | neutral | [E] consistent |
| Capture, Don't Reference (PR-5) | consistent (version back-references creating record) | neutral | [E] **strongest** — creating record captures the outcome directly |
| Trace immutability (inv. 5) | [E] consistent | [E] regress threatens the writer | [E] consistent |
| Provenance | [E] linkage preserved | over-recorded | [E] bidirectional, strongest |
| Separation of Concerns | [E] Repository stays storage-only | [E] **violated** — Repository would orchestrate/spawn | [E] preserved |

## 6. Per-Option Consistency Review (contradictions explicit)

- **Option A vs. Constitution / Domain Model / Trace Arch / Repository Design / Engineering Standard:** [E] **no contradiction with any.**
- **Option B vs. same:** [E] **contradicts** — the Domain Model Agent Instance definition (infrastructure is not an agent), the Repository Design §3 (no orchestration/authority), and the Trace Architecture (RG-1 regress). Three contradictions.
- **Option C vs. same:** [E] **no contradiction with any**; adds a forward-note to the (future, unstarted) Admission design without redesigning it here.

## 7. Recommendation

[E] **The evidence clearly supports one interpretation. Recommended: the interpretation underlying Options A/C — infrastructure persistence is NOT an Agent Instance action and is not independently traced; auditability is preserved by provenance linkage, and (Option C's refinement) is strengthened by having the creating governed action's Trace record explicitly capture the storage outcome.**

The recommendation rests on convergent, mutually-reinforcing evidence, not a single argument:
1. [E] **Textual scope:** Invariant 4 governs "Agent Instance actions," and the ratified Agent Instance definition excludes infrastructure (Q1–Q3).
2. [E] **Regress (RG-1):** the contrary interpretation is logically impossible without special-casing Trace's own writer.
3. [E] **[BUILT] precedent:** `TraceWriter` already operates exactly this way in the real, tested system.
4. [E] **Principle convergence:** A/C are consistent with all six governing principles; B violates Separation of Concerns and strains Evidence First.
5. [E] **Zero contradictions** for A/C against every canonical source; three for B.

**Between A and C:** [A] Option C is marginally preferable because it makes the storage outcome explicit in the audit record (reinforcing PR-5 and giving bidirectional auditability) at negligible cost — but the choice between A and C is properly a **future Admission-design decision** (it concerns what the admission Trace record captures), not a Repository decision and not required to resolve OQ-2. **OQ-2 itself is resolved by the shared interpretation: the Repository storage-write is not a separately-traced Agent Instance action.**

**Scope honesty:** this review *recommends an interpretation*; ratifying it as the canonical reading of Invariant 4 — which has AIOS-wide consequences beyond the Repository (it governs how *all* future infrastructure relates to Invariant 4) — is the Architect's decision. The recommendation is clear and evidence-backed; the ratification is reserved.

[O] **One consequence flagged for the Architect's awareness, not resolved here:** ratifying this interpretation establishes, corpus-wide, that "Agent Instance action" is the precise and *limiting* subject of Invariant 4 — infrastructure facilities (Trace writer, Repository, and future stores) are outside its scope and audited *through* the agent actions that invoke them. This is the correct and already-operative reading, but stating it canonically is a small generalization of Invariant 4's application that the Architect should ratify consciously, since it will bind every future infrastructure subsystem.

---

## 8. If the Architect Declines to Ratify

[E] If the evidence is judged insufficient, OQ-2 remains **unresolved** and the Repository's *implementation* (not its design, which is complete) stays gated — exactly as the Repository Detailed Design's completeness evaluation already states. No forcing function requires resolution before the Knowledge Service or Admission *design* phases; only Repository *implementation* is gated. This review does not itself resolve OQ-2 — it recommends the resolution the evidence supports and reserves ratification to the Architect.

---

No implementation, schema, API, code, pseudocode, or subsystem redesign was produced. Trace, Runtime, and the Repository Design are unmodified. Stopping here. Awaiting explicit Architect authorization to ratify the recommended interpretation (or to leave OQ-2 open).
