# AIOS Architecture Quality Checklist v1.0

**Status:** The checklist every future AIOS architecture document must satisfy before Architect approval.
**Version:** v1.0
**Authority:** Extracted from the review discipline actually practiced across the Knowledge Architecture evolution — every item below corresponds to a check that was really performed (and in several cases really caught something) during that arc. No item is speculative.

Format per item: why it exists · how it is evaluated · pass criteria · failure example (real where one exists).

---

## 1. Canonical Domain Model Consistency
- **Why:** The Domain Model is the ratified semantic foundation; silent divergence corrupts every downstream artifact.
- **How:** Cite the specific §/invariant for every entity, ownership, or lifecycle claim; check no entity is renamed, merged, or invented.
- **Pass:** Every model-touching claim carries a real citation; zero uncited redefinitions.
- **Failure example (real):** the invariant-10 analogy for Knowledge conflict escalation — extending a Capability-scoped invariant by analogy; caught and rejected.

## 2. Constitution Consistency
- **Why:** Governance authority rules (esp. §6.2 invariant 2 — automation may not override governance authority) bind all subsystems.
- **How:** Verify no proposed mechanism lets automation make, or effectively make, a governance decision.
- **Pass:** Every governance transition has an explicit human decision point; automation only detects/proposes.
- **Failure example (real):** the Phase-7 "AI Recommendation" (recommend_approve/reject) — proposed, objected to, and replaced with an evidence-only assessment.

## 3. Ownership Consistency
- **Why:** Ownership claims drift easily between accountability, access, and authority — three different things.
- **How:** For every ownership statement, ask: accountability, access, or decision authority? Check against Domain Model §5 *and* §8 together (not §5 alone).
- **Pass:** Each ownership claim names which of the three it grants; no exclusive-access implication for cross-cutting Substrate entities.
- **Failure example (real):** "Home Department = accountability ownership" initially unreconciled with §8's "not owned by any single Department" — caught by integrated review, resolved by explicit Architect interpretation.

## 4. Lifecycle Consistency
- **Why:** Lifecycle states multiply without evidence; states and conditions conflate.
- **How:** Verify every proposed state has a demonstrated need; apply the State/Condition Separation Principle to every status-like field.
- **Pass:** Minimal state set, each state evidence- or architecture-required; no epistemic condition encoded as a state.
- **Failure examples (real):** "Archived" (rejected — no evidence distinguishing it from Superseded); "Retracted" as a state (rejected — validity is orthogonal).

## 5. Authorization Consistency
- **Why:** Every transition needs a defined authority, or implementation improvises one.
- **How:** For each proposed transition, name who may perform it and under what authority; check the reviewer≠owner distinction is preserved.
- **Pass:** A complete transition→authority table; no transition with "TBD" authority enters implementation.
- **Failure example (real):** deprecation authority tier left unaddressed across two documents — caught and registered as a must-resolve open question rather than silently defaulted.

## 6. Traceability
- **Why:** Domain Model invariant 4 makes Trace production unconditional; designs that skip it break the audit spine.
- **How:** Verify every proposed action/transition produces exactly one Trace record; check new event shapes against collision-proofing (distinct from every existing shape).
- **Pass:** One record per transition, shape-collision test planned; no "silent" transitions.
- **Failure example (constructed, from a real risk): a default-admission window (rejected Option C) would have produced no explicit Trace record at the actual admission moment.

## 7. Explainability
- **Why:** A decision whose basis can't be reconstructed later is ungovernable (Domain Model §6.1).
- **How:** For every decision record, check it embeds what was judged (snapshot), who judged (attributed actor), and why (rationale field).
- **Pass:** All three present by design; explainability survives the deletion/expiry of every referenced entity.
- **Failure example (real, caught early):** candidate review initially considered referencing live candidates — rejected because recomputation would change what the decision "meant"; snapshot capture adopted instead.

## 8. Provenance
- **Why:** Derived content without a verifiable source chain cannot be audited or corrected.
- **How:** Trace the full derivation chain for every artifact; verify each link resolves against real data; distinguish generational absence from conflict.
- **Pass:** Chain resolves end-to-end in a real test; absence-vs-conflict handling explicit.
- **Failure example (real):** the fingerprint agreement check initially treated generational absence (`None`) as disagreement, misclassifying 7 real candidates — caught by running against real data.

## 9. Version Compatibility
- **Why:** New readers must tolerate every real generation of existing records; old records are never rewritten.
- **How:** Enumerate the real on-disk generations; verify read-time normalization covers each; test against the actual corpus, not synthetic fixtures alone.
- **Pass:** A real-corpus normalization test passes for every generation.
- **Failure example (real, prevented):** three distinct Trace `outputs` generations exist on disk; `trace_schema.normalize_record()` was validated against all of them.

## 10. Migration Impact
- **Why:** Every change lands on existing real data or existing meanings; silent reinterpretation is a migration.
- **How:** State explicitly what existing data/meaning changes; distinguish documentation-only from data migrations; check for retroactive reinterpretation.
- **Pass:** A migration-impact section exists, even if its content is "none — no data exists."
- **Failure example (real, avoided):** admission Option A would have retroactively reinterpreted 4 real `approve` events as Knowledge admissions — identified as a migration consequence and weighed before deciding.

## 11. Dependency Analysis
- **Why:** Decisions block other decisions; implementing against an unresolved prerequisite wastes work.
- **How:** Build the decision/subsystem dependency map; verify ordering (what must resolve first).
- **Pass:** A dependency map exists and the recommended sequence follows it.
- **Failure example (real, caught):** Repository design was BLOCKED on version-addressing — the dependency was named before any design began, not discovered mid-implementation.

## 12. Circular Dependency
- **Why:** Cycles make layering unenforceable and reasoning unstable.
- **How:** Derive the import/derivation graph from real source (not from memory of it); verify strict direction.
- **Pass:** Zero cycles in the real graph; derivation direction stated (e.g. Memory → Candidate → Review → Knowledge, never backward).
- **Failure example:** none real — the Execution Layer graph was verified acyclic repeatedly; kept as a check precisely because it was verified, not assumed.

## 13. Architectural Drift
- **Why:** Content accretes across many documents; later documents can quietly diverge from decided positions.
- **How:** Trace every claim in a consolidated document to an explicit prior decision or current directive; flag anything that entered "by accretion."
- **Pass:** Full traceability of every position to a decision; a consolidation states its sources honestly (including naming mismatches).
- **Failure example (real):** the directive-referenced "Knowledge Architecture Blueprint v2" did not exist under that name — flagged rather than silently invented, and the real source corpus mapped explicitly.

## 14. Open-Question Classification
- **Why:** Unclassified unknowns become accidental implementation decisions.
- **How:** Every [O] item is classified (must-resolve-before / resolve-during / safe-to-defer) with blast radius, evidence availability, and dependency impact.
- **Pass:** No unclassified open question; deferrals honored in later phases.
- **Failure example (real, prevented):** the "Questioned takes effect on detection or on confirmation" assumption was implicit inside another question — surfaced and registered explicitly during consolidation.

## 15. Evidence Quality
- **Why:** [E]/[A]/[O] tags are only useful if honestly applied; assumption-inflation is the failure mode.
- **How:** Spot-check tags: does each [E] cite a real mechanism, test, or corpus fact? Is anything tagged [E] on the strength of one instance (should be "Observed," not "Proven")?
- **Pass:** Every [E] has a citable real basis; n=1 findings are labeled as such.
- **Failure example (real, correct usage):** reject/edit paths held at "Observed (n=1)" across multiple reports rather than promoted to "Proven."

## 16. Risk Analysis
- **Why:** Risks discovered during review are cheap; the same risks discovered in production are not.
- **How:** A risk matrix with cause, likelihood, impact, mitigation — only evidence-supported risks (no invented findings).
- **Pass:** Each risk traces to a real observation; mitigations are concrete.
- **Failure example (real, correct usage):** the "Questioned as permanent parking state" risk was registered with its mitigation hook (trigger design must address dwell time) rather than left implicit.

## 17. Implementation Readiness
- **Why:** "Ready" without evidence starts implementation against unresolved foundations.
- **How:** Per-area READY / PARTIALLY READY / BLOCKED verdicts, each with a stated basis; BLOCKED names its exact blocker.
- **Pass:** Every verdict cites its basis; upgrades happen only when the named blocker demonstrably resolves.
- **Failure example (real, correct usage):** Repository moved BLOCKED → READY only when Decision 1 settled version-addressing — a traceable, criterion-based upgrade.
