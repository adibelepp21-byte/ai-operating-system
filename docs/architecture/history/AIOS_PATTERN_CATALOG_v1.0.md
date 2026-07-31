# AIOS Architecture Pattern Catalog v1.0

**Status:** Pattern extraction from the completed Knowledge Architecture evolution. Analysis only — no implementation, no Blueprint modification.
**Version:** v1.0
**Authority:** Subordinate to the ratified Constitution and Canonical Domain Model, and to Knowledge Architecture Blueprint v3 (treated as canonical, extracted from, never modified here).
**Confidence tags:** **[E]** evidence-backed, **[A]** assumption requiring validation, **[O]** open question.

Every pattern below was actually observed operating in this repository — none is invented to increase count. Where two candidate patterns from the directive's example list turned out to be the same underlying pattern (e.g. "State vs Condition," "Orthogonal Axes," and "Separation of Lifecycle and Validity"), they are documented once, with the merge stated.

---

## P1 — Evidence First

- **Intent:** Never design, build, or decide ahead of demonstrated need or observed fact.
- **Problem solved:** Speculative architecture that encodes assumptions as structure, which later real evidence contradicts at high migration cost.
- **Forces:** Pressure to appear complete vs. honesty about what is known; the cheapness of writing a design vs. the cost of unwinding a wrong one.
- **Solution:** Every claim in an architecture document carries an evidence tag; every mechanism is built only after a directive demonstrates need; findings classify as Proven / Observed / Unknown rather than asserted.
- **Consequences:** Slower apparent progress; large "open questions" registers; repeated "NOT READY" verdicts that are honest rather than pessimistic.
- **Benefits:** Zero speculative rework observed across this entire arc; every reversal (e.g. the fingerprint-agreement fix) was driven by real data, caught early.
- **Trade-offs:** Requires discipline to resist filling gaps with plausible assumptions; produces more documents per decision.
- **Proven in AIOS:** [E] The whole Knowledge evolution; concretely: the fingerprint generational-absence fix (real corpus data overturned a design assumption), the rejection of the 8-state lifecycle in favor of 2 states + conditions, every readiness assessment.
- **Reuse in:** Every future subsystem evolution, without exception.
- **Adoption:** Adopt as a standing AIOS Architectural Principle (already effectively is one — Constitution's own philosophy; this catalog formalizes its pattern shape).
- **Confidence:** [E]

## P2 — Unconditional, Immutable Audit Trail

- **Intent:** Every action produces exactly one permanent record; records are never edited or deleted.
- **Problem solved:** Post-hoc unexplainability; silent history rewriting; disputes about what actually happened.
- **Forces:** Storage growth and schema-evolution pressure vs. the absolute value of an uncontested historical record.
- **Solution:** Append-only writer as the sole persistence path (`TraceWriter`); production is unconditional (Domain Model invariant 4), not best-effort; schema evolution handled by read-time normalization (`trace_schema.py`), never by rewriting old records.
- **Consequences:** All derived views (Memory, review state) must be recomputed from the record, never stored authoritatively elsewhere.
- **Benefits:** 540 real records, zero mutations, zero disputes about history across the entire arc; three on-disk schema generations coexisting without breakage.
- **Trade-offs:** Read-time normalization complexity; no ability to "fix" a wrong record except by appending a correction.
- **Proven in AIOS:** [E] `trace.py` + `trace_schema.py` + every phase's corpus-integrity check.
- **Reuse in:** Knowledge Repository (already mandated by Blueprint v3 Decision 4); any future subsystem needing durable records.
- **Adoption:** Adopt.
- **Confidence:** [E]

## P3 — Human-Governed Promotion Pipeline

*(Merges the directive's "Promotion Pipeline," "Human-Governed Promotion," and "Review-before-Promotion" — one pattern observed as one mechanism.)*

- **Intent:** Content moves from a volatile layer to a durable layer only through an explicit, recorded human decision — never automatically.
- **Problem solved:** Silent accumulation of unvetted content into positions of trust.
- **Forces:** Automation's efficiency vs. governance authority; volume pressure vs. review quality.
- **Solution:** A read-only selection stage (candidates, ranked but never auto-promoted) followed by a governed human decision stage whose contract structurally cannot compute a verdict (AST-verifiable absence of decision logic).
- **Consequences:** Human review becomes the throughput bottleneck by design; the pipeline needs prioritization signals to make bounded human attention effective.
- **Benefits:** 6 real decisions with full auditability; invariant 8 held structurally, not just procedurally.
- **Trade-offs:** Does not scale without more reviewers; deliberate.
- **Proven in AIOS:** [E] `promotion.py` → `review_decision.py`, 6 real events, AST-verified boundary tests.
- **Reuse in:** Knowledge admission (settled, Blueprint v3); any future promotion between trust tiers (e.g. a future Capability-proposal flow).
- **Adoption:** Adopt.
- **Confidence:** [E]

## P4 — State/Condition Separation

*(Merges "State vs Condition," "Orthogonal Axes," "Separation of Lifecycle and Validity" — one principle, three phrasings.)*

- **Intent:** Lifecycle position (where something is in its history) and evaluation (what we currently think of it) are independent axes; never encode one as the other.
- **Problem solved:** State-machine explosion and semantic dishonesty (e.g. "Retracted" as a state conflating "is current" with "is trustworthy").
- **Forces:** The simplicity of one flat status field vs. the correctness of independent dimensions.
- **Solution:** A minimal lifecycle state set (Active/Superseded) plus orthogonal conditions (Confirmed/Questioned/Invalidated; conflict) evaluated and recorded separately.
- **Consequences:** Consumers must read two axes; the model resists collapsing them.
- **Benefits:** Applied twice independently (conflict, then validity) before being named — evidence it is a genuine recurring force, not a one-off choice.
- **Trade-offs:** Higher conceptual load for consumers; accepted deliberately in Blueprint v3.
- **Proven in AIOS:** [E] Architect Decision 4 (conflict = condition) and Decision 2/refinement (validity model), plus real precedents: `evaluate_relevance()` labels without mutating; `detect_conflicts()` flags without transitioning.
- **Reuse in:** Any future entity with both a history and an evaluation (Agent Definition versions vs. deprecation judgment; Workflow versions vs. operational health).
- **Adoption:** Adopt — already elevated to a named AIOS Architectural Principle in Blueprint v3.
- **Confidence:** [E]

## P5 — Stable Identity via Correlation Key

- **Intent:** A logical entity persists across many records by a shared key, without a stored parent record.
- **Problem solved:** The false choice between a mutable master record (violates immutability) and no cross-record identity at all.
- **Forces:** The intuition to model a "thing" as a row vs. the auditability of modeling it as its history.
- **Solution:** Every record carries the correlation key; all identity-level facts are derived at read time from the record set.
- **Consequences:** Identity-level queries are aggregations; there is no single place to "look up" the entity except through its records.
- **Benefits:** Proven twice before Knowledge adopted it: Agent Instance (exists only through Trace records carrying `instance_id`) and review state (derived from decision records sharing `(observation_kind, content)`).
- **Trade-offs:** Requires the correlation key to be genuinely stable — the anti-example is also proven: `memory_id` regenerates per extraction, so Memory deliberately *lacks* this pattern, and every consumer had to know that.
- **Proven in AIOS:** [E] `agent_instance.py` docstring + Trace corpus; `review_state()`; Blueprint v3 Decision 1.
- **Reuse in:** Knowledge (settled); any future versioned entity.
- **Adoption:** Adopt, with the explicit caveat that the key's stability must be verified, not assumed (the `memory_id` lesson).
- **Confidence:** [E]

## P6 — Append-Only Versioning

- **Intent:** Change = a new immutable version; the previous version's position changes (Superseded) but its content never does.
- **Problem solved:** In-place mutation destroying the audit trail; "what did it say before?" becoming unanswerable.
- **Forces:** Storage/UX simplicity of overwrite vs. Domain Model §6's "not casually deleted... audit trail matters."
- **Solution:** New version record per revision; supersession is intra-identity and distinct from conflict (inter-identity).
- **Consequences:** Consumers must resolve "current version" at read time; retraction needs the orthogonal validity axis (P4), since a version with no successor cannot be Superseded.
- **Benefits:** Historical correctness preserved by construction; the real `edit` decision already proved the miniature form (original + correction coexisting).
- **Trade-offs:** More records; two-step reads.
- **Proven in AIOS:** [E] Trace (event-level); the `edit` decision (`trace-502ab65e9b0f`); Blueprint v3 Decisions 1/4.
- **Reuse in:** Knowledge (settled); plausibly governance documents themselves (the Evolution Protocol already mandates retaining prior baseline versions).
- **Adoption:** Adopt.
- **Confidence:** [E]

## P7 — Capture, Don't Reference (Snapshot at Decision Time)

- **Intent:** A decision record embeds the full content it judged, never a live pointer to something recomputable or mutable.
- **Problem solved:** Decisions whose meaning silently changes when their referent changes (proven risk: candidates recomputed at T2 carry different evidence than at T1).
- **Forces:** Storage duplication vs. permanent decision integrity.
- **Solution:** `asdict()`-style full snapshot embedded in the decision's own record.
- **Consequences:** Records are larger; the snapshot is the authoritative account of what was reviewed.
- **Benefits:** Proven immune to corpus drift by a real T1→T2 test; also satisfies Domain Model §6.1 (explainability never depends on another entity's continued existence).
- **Trade-offs:** Snapshot mechanics (exact field set) need per-use design — still an open question for Knowledge (#4).
- **Proven in AIOS:** [E] `candidate_snapshot` across 6 real events + `SnapshotImmutabilityUnderCorpusDriftTest`.
- **Reuse in:** Knowledge admission/revision/invalidation records (mandated by Blueprint v3 provenance model); any future decision record.
- **Adoption:** Adopt.
- **Confidence:** [E]

## P8 — Provenance Chain

- **Intent:** Every derived artifact remains traceable, step by step, to its real sources.
- **Problem solved:** Untraceable claims; inability to audit why the system believes something.
- **Forces:** The cost of carrying source references vs. the cost of unexplainable content.
- **Solution:** Each layer records the identifiers of what it derived from (Trace IDs → Memory → Candidate → Decision), with resolution verified, and generational absence (a source field that legitimately didn't exist yet) distinguished from conflict.
- **Consequences:** Cross-referencing logic at each layer; explicit handling of historical gaps.
- **Benefits:** Chain proven unbroken across the entire real corpus, repeatedly; the one real defect found (fingerprint over-strictness) was caught precisely because the chain was checkable.
- **Trade-offs:** More metadata; the chain is only as good as its weakest captured link.
- **Proven in AIOS:** [E] `test_evidence_chain.py` and every phase's provenance verification.
- **Reuse in:** Knowledge provenance model (settled); any future derivation layer.
- **Adoption:** Adopt.
- **Confidence:** [E]

## P9 — Detect, Don't Decide

- **Intent:** Automation may find, flag, and surface; only governed human review may act.
- **Problem solved:** The slide from helpful automation into automated governance (forbidden by Constitution §6.2 invariant 2 and Domain Model invariant 8).
- **Forces:** Automation's obvious efficiency vs. the absolute human-authority boundary.
- **Solution:** Detection mechanisms return findings and never transition state: `detect_conflicts()` returns conflicts and resolves none; Tier 2 verification invalidates a cache entry (an execution concern) but never a governance judgment; the Questioned condition (Blueprint v3) is the validity-axis form — automation may propose it, humans set it.
- **Consequences:** Every detection needs a paired human pathway or its findings pile up (the "Questioned parking-state" risk in Blueprint v3's risk matrix).
- **Benefits:** The boundary held across the entire arc, including under direct pressure (the declined Phase-7 "AI Recommendation" episode).
- **Trade-offs:** Latency between detection and action is structural, not incidental.
- **Proven in AIOS:** [E] `detect_conflicts()`, Tier 2, the recommendation-refusal precedent, AST boundary tests.
- **Reuse in:** Every future subsystem containing any automated evaluation.
- **Adoption:** Adopt as a candidate standing Principle (recommended for elevation — see the consistency review).
- **Confidence:** [E]

## P10 — Fail Closed

- **Intent:** When freshness, correctness, or authorization cannot be proven, refuse rather than guess.
- **Problem solved:** Silent trust of unverifiable data (the exact real bug found and fixed in `verification.py`).
- **Forces:** Availability/continuity vs. correctness.
- **Solution:** Unverifiable = invalid: missing fingerprints fail verification; ambiguous sources classify as `"unknown"`; unresolvable department status reports `"unavailable"`; malformed decisions raise before any write.
- **Consequences:** More refusals and re-executions; honest "unknown" values propagate instead of plausible guesses.
- **Benefits:** The one real violation ever found (deleted-file fail-open) was a bug against this pattern, not a counterexample to it — and was repaired to conform.
- **Trade-offs:** Costs extra live executions when a cache can't be proven fresh.
- **Proven in AIOS:** [E] `verification.py` (including its repaired defect), `promotion.py`'s unknown-source handling, `validate_decision_input()`.
- **Reuse in:** Everywhere trust is computed.
- **Adoption:** Adopt.
- **Confidence:** [E]

## P11 — Authorization Before Invocation

- **Intent:** Check permission against the governing document before acting; record refusals as first-class events.
- **Problem solved:** Silent privilege drift; unauditable denials.
- **Forces:** Convenience of assuming permission vs. governed operation.
- **Solution:** The orchestrator checks Permitted Workflows/Skills before every dispatch; refusal produces an escalation Trace record (the denial itself is an action, unconditionally traced).
- **Consequences:** Governance documents become load-bearing runtime inputs.
- **Benefits:** Real escalation path exists and is tested; authorization is data, not code convention.
- **Trade-offs:** Requires the permission source to be maintained.
- **Proven in AIOS:** [E] `orchestrator.py` + `test_orchestrator.py` authorization-boundary tests.
- **Reuse in:** Knowledge lifecycle transitions (each will need an authority check per Blueprint v3 §2.6); any future actor-performs-action surface.
- **Adoption:** Adopt.
- **Confidence:** [E]

## P12 — Explicit Deferred Decisions

- **Intent:** An undecided question is a tracked, classified artifact — never an implicit gap.
- **Problem solved:** Silent assumption-filling; decisions made by accident during implementation.
- **Forces:** The urge to appear finished vs. the cost of implicit decisions.
- **Solution:** Open-question registers with classification (must-resolve-before-implementation / resolve-during / safe-to-defer), blast-radius reasoning, and explicit "non-decision" sections in every decision package.
- **Consequences:** Long-lived registers; deferrals must be honored (the invariant-10 analogy was *rejected and deferred*, not quietly adopted).
- **Benefits:** Eight open questions currently tracked for Knowledge, none silently resolved across ~10 documents — measurable discipline.
- **Trade-offs:** Requires re-validation that deferred items are still deferred at each phase.
- **Proven in AIOS:** [E] The Blocker Register, every decision package's non-decisions section, the honored invariant-10 deferral.
- **Reuse in:** Every future subsystem evolution.
- **Adoption:** Adopt.
- **Confidence:** [E]

## P13 — Signals Prioritize, Never Gate

- **Intent:** Computed quality signals (confidence, frequency, similarity) may order human attention; they may never determine eligibility or outcome.
- **Problem solved:** Score-based governance sneaking in through ranking mechanisms.
- **Forces:** The temptation to let a threshold "help" vs. the human-authority boundary.
- **Solution:** Ranking functions sort candidates; eligibility filters check only structural degeneracy; no comparison of a quality signal ever branches a governance outcome (AST-enforced in the review contract).
- **Consequences:** Low-confidence content still reaches humans — flagged, not filtered.
- **Benefits:** Every real candidate regardless of confidence was human-reviewable; conflict resolution by similarity score was cleanly rejectable because this pattern already existed.
- **Trade-offs:** Humans see more; mitigated by ordering.
- **Proven in AIOS:** [E] `promotion.py` (ranking vs. `is_degenerate_content()`), the Architect's rejection of confidence-decided conflicts.
- **Reuse in:** Knowledge admission prioritization (settled); any future triage surface.
- **Adoption:** Adopt.
- **Confidence:** [E]

## P14 — Readiness Classification with Evidence

- **Intent:** Readiness verdicts (READY / PARTIALLY READY / BLOCKED) are per-area, evidence-cited, and name the specific blocker.
- **Problem solved:** Vague "almost done" assessments; implementation starting against unresolved foundations.
- **Forces:** Momentum vs. honesty.
- **Solution:** Every readiness matrix row states its basis; BLOCKED rows name the exact open question; upgrades happen only when the named blocker resolves (Repository: BLOCKED on version-addressing → READY when Decision 1 settled it).
- **Consequences:** Readiness can go down as well as up when integrated review finds new gaps.
- **Benefits:** The Repository upgrade is a real, traceable example of the mechanism working end-to-end.
- **Trade-offs:** Requires maintaining the matrix across documents.
- **Proven in AIOS:** [E] The readiness matrices across the Consistency Review → Decision Review → Blueprint v3 sequence.
- **Reuse in:** Every future subsystem evolution.
- **Adoption:** Adopt.
- **Confidence:** [E]

---

## Patterns Considered and Not Extracted

- **"Dependency-driven Evolution"** (from the directive's example list): [A] real sequencing by dependency did occur (decisions ordered by what they unblock), but it is not yet distinct enough from P12+P14 combined to stand as its own pattern without inventing structure. Not extracted; revisit if a second subsystem evolution shows it as an independent force.
- **"Versioned Canonical Knowledge"**: not a reusable pattern — it is the Knowledge subsystem itself, i.e. the *composition* of P4+P5+P6+P7. Documented as a composition example, not a pattern.
- **"Explainability"**: a system property produced by P2+P7+P8 together, not an independent pattern with its own mechanism. Listed in the Quality Checklist instead, where it is enforceable.
