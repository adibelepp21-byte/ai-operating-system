# AIOS Decision Review Method — Validation Plan (External Corpus) v1.0

**Status:** Validation plan only. No code, schema, API, database, pseudocode, or implementation. Modifies no ratified document. Reopens no decision. Introduces no new rule.
**Version:** v1.0
**Standing of the methodology under test:** per Architect authorization, **DR-0…DR-6 is a *documented working methodology*, not Canonical Governance and not an AIOS Architectural Principle.** This plan defines how it earns — or fails to earn — promotion, by application to external open-source corpora.
**Governing constraint:** Evidence First (PR-1) remains the primary rule throughout.
**Confidence discipline:** **[E]** evidenced · **[A]** assumption · **[O]** open question.

---

## 1. Purpose of Validation

[E] The Methodology Governance Review established that DR-0…DR-6 recurs strongly in *count* (~14 AIOS documents) but not in *independence* (single author, single arc). This plan closes exactly that gap. Its purpose:

- To determine whether DR-0…DR-6 produces **consistent, evidence-disciplined decision reviews when applied to corpora that AIOS did not author and does not govern** — i.e., whether the methodology is a real transferable method or an artifact of the AIOS context that produced it.
- To convert *count-recurrence* into *independence-recurrence* — the specific criterion the Principles/Governance promotion standard requires and which single-arc AIOS work cannot supply.

[E] **What this validation is NOT:** it is not a validation of AIOS's architectural decisions, not a benchmark of the external repositories, and not a quality judgment of that external code. The external repository is **evidence, not subject** — the methodology is what is under test, exercised *through* the repository.

## 2. The Authority/Evidence Inversion (foundational to the whole plan)

[E] Carried directly from the Methodology Review §9, because every criterion below depends on it: when DR-0…DR-6 is applied to an external repository, the repository is treated **as Memory-like evidence, never as Domain-Model-like authority.** Concretely:

- **DR-1 (Grounding)** grounds in the external repo's *real observed content* as *fact* — never as a rule the review must obey.
- **DR-6 (Consistency)** checks the review's own reasoning for internal consistency and against *the methodology's own rules* — **not** against AIOS canon (AIOS does not govern external code) and **not** against the external repo as if it were authoritative.

[A] This inversion is reasoned from the ratified Trace/Memory distinction; it has never itself been exercised in practice. Its correct functioning is one of the things this validation must prove ([O] until then).

## 3. Corpus-Independence Requirements (constraints 6 & 5)

[E] The validation process must be usable on **any** repository. Therefore it must not depend on:

- **Graphify** — no dependency on any specific tooling, parser, or graph representation. The methodology operates on *observed repository content*, however observed; the observation mechanism is out of scope and must not be assumed.
- **AIOS** — no dependency on AIOS canon, entities, invariants, or documents. A reviewer with no knowledge of AIOS must be able to apply DR-0…DR-6 to a repository using only the repository itself plus the methodology's stated stages.
- **Any domain** — no assumption about language, framework, size, or purpose of the repository.

[E] **Test of independence-by-construction:** if any validation criterion below can only be satisfied using AIOS-specific knowledge, that criterion is itself AIOS-dependent and must be rejected. Every criterion in §5–§8 is written to be checkable by a reviewer who knows only "the DR-0…DR-6 stages" and "the repository in front of them."

## 4. What Must Be Proven for Promotion to Canonical Governance

[E] Promotion requires demonstrating **all** of the following; failing any one leaves the methodology documented-but-not-promoted:

- **P-1 Independence:** DR-0…DR-6 produces coherent reviews on ≥N external repositories that share no authorship, domain, or governance with AIOS. (N is a success-criterion parameter, §5.)
- **P-2 Consistency:** the *same* methodology, applied to *different* repositories, yields reviews with the *same stage structure and the same evidence-discipline*, not divergent ad-hoc analyses.
- **P-3 Premise-Verification transfer (DR-0):** the methodology catches at least one real false or unverifiable premise in an external review (proving DR-0 works without AIOS context).
- **P-4 Boundary integrity:** the Evidence / Reasoning / Interpretation / Recommendation boundaries (Methodology Review §8) remain crisp on external corpora — no external review blurs an interpretation into a fact or a recommendation into evidence.
- **P-5 Inversion correctness (§2):** external repositories are demonstrably treated as evidence, never as authority, in every external review.
- **P-6 Reviewer-independence (the hardest):** [O] ideally, a *different reviewer* applies the methodology and reaches structurally consistent results. Whether single-reviewer/multi-corpus evidence is *sufficient*, or multi-reviewer evidence is *required*, is itself an open question the Architect must judge — flagged, not resolved here (it mirrors the unresolved Human-Review multi-reviewer question).

## 5. Success Criteria

[E] Stated as checkable conditions, parameterized where the threshold is an Architect judgment (marked [A]/[O]):

| # | Success criterion | Threshold |
|---|---|---|
| SC-1 | DR-0…DR-6 applied end-to-end to an external repo without invoking AIOS knowledge | Binary: achieved or not, per review |
| SC-2 | The seven stages are all present and in order in each external review | Binary per review |
| SC-3 | Every claim in each external review carries an [E]/[A]/[O] tag; spot-audit finds tags honestly applied | Binary per review |
| SC-4 | ≥1 external review catches a real false/unverifiable premise (P-3) | At least once across the corpus set |
| SC-5 | Across ≥N distinct external repos, the reviews are structurally consistent (P-2) | [A] N to be set by Architect; a reasoned starting point is **3 independent repos of differing domain/language** |
| SC-6 | The authority/evidence inversion (§2) holds in every external review (P-5) | Binary per review |
| SC-7 | Boundary integrity (P-4) holds — no blurred stage boundary | Binary per review |

[A] **On N:** three independent repositories is proposed as the minimum that would establish independence beyond a single lucky fit, by analogy to the "≥2 independent occurrences" bar used for patterns and the desire for one margin beyond it. The Architect sets the final N; this is not silently resolved.

## 6. Evaluation Metrics

[E] Descriptive metrics only — measured, never scored into a verdict automatically (Detect-Don't-Decide: the metrics inform the Architect's promotion judgment; they do not compute it):

- **M-1 Stage completeness:** fraction of the seven stages present per external review (target: 7/7).
- **M-2 Tag coverage:** fraction of claims carrying an [E]/[A]/[O] tag (target: 100%).
- **M-3 Tag honesty (audited):** fraction of [E] tags that cite a real observable in the repo, vs. tags that are actually [A] mislabeled (target: 0 mislabels; measured by spot-audit).
- **M-4 Premise corrections:** count of DR-0 premise corrections across the corpus (P-3 needs ≥1).
- **M-5 Structural divergence:** a qualitative record of any way two external reviews diverged in structure despite the same methodology (target: none unexplained).
- **M-6 AIOS-leakage incidents:** count of places an external review relied on AIOS-specific knowledge (target: 0 — any >0 is a corpus-independence failure).

## 7. Evidence to Be Collected

[E] Per external repository reviewed:

- The external review document itself (a DR-0…DR-6 application to that repo).
- A record of which premises DR-0 verified and any it corrected (M-4).
- The [E]/[A]/[O] tag audit result (M-2, M-3).
- An explicit note of any AIOS knowledge that was needed (M-6) — honestly recorded even when it indicates failure.
- A statement of how the repository was treated as evidence-not-authority (P-5), with the specific reasoning.

[E] All collected evidence is stored as **new, additive records** (see §10) — never by editing this plan, the methodology document, or any canonical document.

## 8. Failure Criteria

[E] The methodology is judged **not ready for promotion** (and remains documented-only) if any of the following occur:

- **F-1:** an external review cannot be completed without AIOS knowledge (M-6 > 0) — proves the methodology is AIOS-dependent, not transferable.
- **F-2:** two external reviews of comparable questions diverge in *structure* with no evidence-based reason (M-5) — proves the method is not consistent, only stylistic.
- **F-3:** the [E]/[A]/[O] boundary blurs on external corpora (M-3 mislabels > 0, or P-4 violated) — proves the discipline was AIOS-context-dependent.
- **F-4:** the authority/evidence inversion fails — an external repo is treated as authoritative (P-5 violated) — proves the method silently imports AIOS's internal-corpus assumption.
- **F-5:** DR-0 never catches a false premise across the corpus (P-3 unmet) — leaves premise-verification transfer unproven (a *weak* failure: inconclusive rather than disproven; [O]).

[E] **Failure is a valid, valuable outcome** — it prevents promoting a methodology that only works in its birth context. Per Evidence First, a documented failure is a successful validation of *the plan*, even as it denies promotion to *the methodology*.

## 9. Evidence Independence Assessment (constraint 7)

[E] The core question: how does one *prove* a methodology works on a corpus genuinely different from AIOS, rather than proving only that its author can re-apply it?

**Dimensions of independence that must all be satisfied for a corpus to count as "genuinely different":**

| Independence dimension | What makes it genuine | How to verify |
|---|---|---|
| **Authorship independence** | AIOS engineers did not write the repo | Public provenance of the external repo |
| **Domain independence** | The repo's problem domain is unrelated to AIOS's (governance/execution) | The repo's own stated purpose |
| **Governance independence** | The repo is not bound by AIOS canon | Trivially true for any external repo |
| **Structural independence** | The repo's architecture was not shaped by AIOS patterns | Inspection of the repo's own design |
| **Reviewer independence** | [O] ideally the reviewer is not the methodology's author | Requires a second reviewer — currently unavailable; flagged |

[E] **The strongest achievable independence with a single reviewer is four of five dimensions** (authorship, domain, governance, structural). **Reviewer independence is the one dimension a single-author validation structurally cannot supply** — exactly the limitation the Methodology Review already named. Therefore:

[E] **Honest ceiling of this validation:** applying DR-0…DR-6 to external repos can prove **corpus-independence** (the method is not AIOS-content-dependent) — a real and necessary result. It **cannot, by itself, prove reviewer-independence** (that a *different mind* applying the method reaches consistent results). 

[O] **Consequently, the Architect faces a genuine judgment this plan does not resolve:** whether corpus-independence across N external repos is *sufficient* evidence for promotion, or whether reviewer-independence is *also required*. This is the same shape as the unresolved Human-Review multi-reviewer question, and it is marked [O] rather than decided. The validation can deliver everything except reviewer-independence; whether that is enough is reserved to the Architect.

## 10. How Validation Results Are Recorded Without Changing Architecture (constraint 4/8)

[E] Every validation result is an **additive record**, following the corpus's own append-only discipline:

- Each external review is a new document (e.g. `AIOS_DR_VALIDATION_<repo>_v1.0.md`), never an edit to this plan or the methodology.
- A running **validation log** (a new, living record) accumulates the metrics (§6) across reviews — analogous to a Status Registry, descriptive only.
- The methodology document (DR-0…DR-6) is **not edited** by validation outcomes; if promotion is eventually earned, that is a *separate, future Architect decision* recorded in its own document — this plan does not pre-authorize it.
- No architectural decision is reopened by any validation result; a result can only *inform a future promotion decision*, never *enact* one (Detect-Don't-Decide; reserve-to-Architect).

## 11. Consistency Review Against Canonical Documents

- [E] **Constitution:** the plan reserves promotion to the Architect, automates no decision, and reopens nothing (§6.2 invariant 2 upheld). No contradiction.
- [E] **Canonical Domain Model:** the plan touches no entity or invariant; the authority/evidence inversion (§2) is *derived from* the ratified Trace/Memory distinction, not a new rule. No contradiction.
- [E] **Principles Register:** the plan is PR-1 (Evidence First) operationalized as a validation design; it introduces no principle and no duplicate authority. No contradiction.
- [E] **Engineering Design Standard / Reference Engineering Model:** the plan governs a governance methodology, not a subsystem design; orthogonal. No contradiction.
- [E] **Meta Model / Ratification Review:** validation reviews are T12 (Review) outputs and the log is a T11 (Registry); both fit existing types with no new artifact type. No contradiction.
- [E] **DR-0…DR-6 Methodology document:** unmodified; this plan tests it, does not alter it. No contradiction.

**No decision reopened. No code changed. No implementation designed. No new rule introduced.** Verified against each source above.

## 12. Assumptions and Open Questions (not self-resolved)

- [A] **A-1:** three independent external repos (SC-5) is a reasonable minimum N — reasoned by analogy, not proven; Architect sets final N.
- [A] **A-2:** the authority/evidence inversion (§2) will function correctly in practice — reasoned from Trace/Memory, never exercised.
- [O] **O-1:** whether corpus-independence without reviewer-independence is *sufficient* for promotion — the central unresolved judgment (§9), reserved to the Architect.
- [O] **O-2:** whether DR-0's premise-verification transfers without AIOS context (P-3) — provable only by running the validation.
- [O] **O-3:** the observation mechanism for external repos (how repository content is surfaced to the reviewer) is deliberately out of scope and unspecified — it must remain tool-agnostic (§3), but *which* tool-agnostic means will be used is unresolved and must not be assumed to be any specific system.

---

## Summary

[E] This plan defines how the documented DR-0…DR-6 methodology can earn promotion to Canonical Governance by application to external open-source corpora — establishing success criteria (SC-1…SC-7), metrics (M-1…M-6), evidence to collect (§7), failure criteria (F-1…F-5), and an additive, non-destructive recording scheme (§10). Its Evidence Independence Assessment (§9) is honest about the ceiling: single-reviewer validation can prove **corpus-independence** but structurally **cannot prove reviewer-independence**, leaving whether the former suffices as an explicit [O] for the Architect. Nothing canonical is changed; no decision reopened; no rule introduced; every unproven assumption is tagged [A]/[O] rather than resolved.

No code, schema, API, database, pseudocode, or implementation was produced. Stopping after the document. Awaiting the next authorization (and the first external repository).
