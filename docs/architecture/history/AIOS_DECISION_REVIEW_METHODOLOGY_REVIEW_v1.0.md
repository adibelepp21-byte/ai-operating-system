# AIOS Decision Review Methodology — Governance Review v1.0

**Status:** Architecture governance review only. Evaluates the *methodology* of the recent Architecture Decision Reviews, not their content. No code, schema, API, implementation, or modification of any ratified document.
**Version:** v1.0
**Evidence base:** the ~14 decision-review-class documents produced across this arc (Admission Model, Ownership, Lifecycle & Conflict, Version-Addressing/Retraction, Ratification, Integration, Canonical Architecture, Governance, Meta Model, Implementation Plan, OQ-2, Infrastructure Auditing, Interpretation Layer, and their decision packages).
**Confidence discipline:** **[E]** evidenced · **[A]** assumption · **[O]** open question.

---

## 1. Does the process follow PR-1 (Evidence First) consistently?

[E] **Yes, consistently — verifiably so, not by assertion.** Across the reviewed documents, every one begins by grounding in real evidence before reasoning: exact ratified text is quoted (the OQ-2 review quoted Invariant 4's precise wording; the Infrastructure review verified against real code that only two subsystems author Trace records; the Interpretation-Layer review ran an audit that *corrected the directive's own premise* from "5 interpretation examples" to "3 genuine ones"). This last case is the strongest PR-1 evidence: the method repeatedly overrode a *stated premise* with *measured evidence* — the defining behavior of Evidence First, not merely compatible with it.

[A] One honest qualification: PR-1 adherence is observed in the *outputs*. Whether the same rigor would hold under time pressure or for a reviewer other than the single author of these documents is untested (see §5, §9).

## 2. Are there implicit-but-undocumented evaluation steps?

[E] **Yes — three steps recur in practice but were never named as method:**

- **IS-1 — Premise Verification.** Before evaluating a question, the reviewer re-checks the question's own premises against evidence (the "5→3 interpretation" correction; the "only 2 subsystems trace" check; the "Blueprint v2 does not exist" flag). This is done every time but was never listed as a step.
- **IS-2 — The sixth promotion test ("adds a new rule vs. unpacks an existing one").** Used to keep immutable-history as Invariant 5, infrastructure-auditing as an interpretation not PR-6, and State/Condition as a genuine PR-2 — a consistent discriminator applied repeatedly, never formally named.
- **IS-3 — Explicit Re-evaluation Trigger on deferral.** Every deferral states a *condition* under which to revisit (the Interpretation-Layer review's "revisit when interpretation volume exceeds ADR indexing"; the conflict-escalation "revisit on first real cross-Department conflict"). Consistently done, never named as a required output.

These three are the review's genuinely *tacit* method — real, repeated, undocumented.

## 3. Are consistent criteria used to distinguish the four decision kinds?

The four kinds: (a) interpretation of existing architecture, (b) refinement, (c) new architectural decision, (d) change to ratified architecture.

[E] **Yes, a consistent discriminator is applied — and it is a single question:** *"Does this add a rule/structure not already held at a higher canonical layer?"*
- **Adds nothing new, only clarifies meaning → interpretation** (OQ-2, Infrastructure, Home-Dept/§8).
- **Adds a new rule/structure within an unratified area → new decision** (Blueprint v3 Decisions).
- **Sharpens an existing settled decision without reversing it → refinement** (Confirmed/Questioned/Invalidated refining binary validity).
- **Alters ratified text → change** (never occurred — every review explicitly refused to reopen ratified decisions).

[E] This discriminator is the same one used for principle-promotion (the "duplicate authority" test) and for the Ratification Review's canonical/historical split. **One criterion, applied across all decision kinds** — evidence of a real method, not ad-hoc classification.

## 4. Is there a recurring evaluation pattern worthy of being a Canonical Decision Review Methodology?

[E] **Yes — a stable seven-stage pattern recurs across all ~14 documents.** Extracted verbatim from practice (§6), not invented. But "worthy of *canonical* status" is answered carefully in §5 and the final verdict — recurrence in *count* is strong; recurrence in *independence* is not.

## 5. Have all prior Decision Reviews actually followed the same stages, even unnamed?

[E] **Yes in structure; [A] with one decisive caveat.** Auditing the documents, each follows the same spine (ground → options → evaluate-against-canon → evidence-tag → recommend-or-defer → consistency-check → reserve-to-Architect). The spine is genuinely invariant across topics as different as ownership models and Trace-scope interpretation.

[E] **The decisive caveat — single-author recurrence.** All ~14 documents were produced by *one reviewer* (this engineering role) in *one continuous arc*. The recurrence is real as *practice* but is **not independently rediscovered by multiple actors** — which is precisely the independence criterion the Principles Register requires (PR-1…PR-5 each cite occurrences across *different subsystems built at different times*). This methodology's occurrences are many but not independent. **This is the same evidence-shape limitation already flagged for Human Review** (6 real events, 1 reviewer identity — recurrence without independence). Intellectual honesty requires naming it identically here.

## 6. The Extracted Methodology (named and structured, not invented)

[E] **The AIOS Decision Review Methodology (observed) — seven stages, each already practiced:**

| Stage | Name | What it does | Boundary kind |
|---|---|---|---|
| DR-0 | **Premise Verification** (was tacit, IS-1) | Check the question's own premises against real evidence; correct them if wrong | Evidence |
| DR-1 | **Grounding** | Quote the exact ratified text / real code the decision touches | Evidence |
| DR-2 | **Option Enumeration** | Lay out ≥3 candidate interpretations/decisions; select none yet | Reasoning |
| DR-3 | **Canonical Evaluation** | Evaluate each option against Constitution, Domain Model, Principles, and the relevant Blueprint/Standard | Reasoning |
| DR-4 | **Classification** | Apply the single discriminator (§3): interpretation / refinement / new / change | Interpretation |
| DR-5 | **Evidence-Tagged Recommendation** | Recommend one *only if* [E] clearly supports; else leave [O]; tag every claim [E]/[A]/[O] | Recommendation |
| DR-6 | **Consistency Review + Reserve-to-Architect** | Verify no contradiction with ratified canon; state non-decisions and re-evaluation triggers (IS-3); reserve ratification to the Architect | Recommendation |

[E] This is a faithful naming of what already happened, adding no step that was not already performed. DR-0 and the IS-3 element of DR-6 are the previously-tacit steps now made explicit.

## 7. AIOS-wide, or Architecture-Decision-Review-only?

[A] **Primarily Decision-Review-scoped, with an AIOS-wide core.** The full seven-stage sequence is specific to *deciding an architectural question*. But its core — DR-0 (verify premises), DR-5 (evidence-tag, recommend only if supported), DR-6 (reserve authority) — is the same discipline already applied in *non-decision* work throughout the arc (readiness assessments, the pattern-extraction that declined to invent patterns, the refusal to fabricate a security model). So the *core discipline* is AIOS-wide (it is essentially PR-1 operationalized); the *seven-stage form* is Decision-Review-specific. Recommending the seven-stage form as AIOS-wide would over-generalize; recommending its core as AIOS-wide would merely restate PR-1.

## 8. Explicit Evidence / Reasoning / Interpretation / Recommendation boundaries

[E] The directive's own ask — make the stage boundaries explicit — is answered by the boundary-kind column in §6, and applies within *every* review:

- **Evidence** (DR-0, DR-1): what is *observed* — quoted text, measured facts, real code. No inference. Falsifiable.
- **Reasoning** (DR-2, DR-3): what *follows* from evidence — option construction and evaluation. Inference, but traceable to evidence.
- **Interpretation** (DR-4): what the evidence *means* for classification — a judgment, explicitly labeled, that could differ between reasonable reviewers.
- **Recommendation** (DR-5, DR-6): what *should* happen — always reserved to Architect ratification, never self-enacted.

[E] The methodology's integrity depends on these four never blurring. A review that presented a Recommendation as Evidence, or an Interpretation as a Fact, would violate the method. Spot-checking the arc: the [E]/[A]/[O] tagging enforces exactly this boundary at the sentence level — which is why the tagging is not decoration but the method's load-bearing mechanism.

## 9. Consistency when applied to an external open-source validation corpus

[O] **The methodology would require one real adaptation, and this is a genuine limitation, not a formality.** Stages DR-1 (Grounding in ratified text) and DR-6 (Consistency vs. ratified canon) presuppose an *internal canonical corpus that holds authority*. An external open-source repository has no such authority relative to AIOS.

[E] Two stages transfer unchanged: DR-0 (verify premises), DR-2 (options), DR-5 (evidence-tagged recommendation). The evidence-first core is corpus-agnostic.

[E] Two stages *invert their meaning*: for an external repo, the repo is **evidence, not authority**. DR-1 would ground in the repo's real code *as observed fact* (not as a rule to obey); DR-6 would check the repo *as evidence for or against an AIOS claim* (not check the repo against AIOS canon as if AIOS bound it). This inversion is exactly the Trace-vs-Memory distinction already ratified: an external corpus is like Memory (evidence, provisional, informs) not like the Domain Model (authority, binding). The methodology *can* handle external corpora, but only if this authority/evidence inversion is made explicit — otherwise it would wrongly treat external code as canonical. **This is a real prerequisite for the "AIOS validates against open-source corpora" future direction.**

## 10. Consistency Review Against Ratified Governance

- [E] **Constitution:** the methodology reserves every ratification to the Architect (DR-6) and automates no decision — consistent with §6.2 invariant 2. No contradiction.
- [E] **Canonical Domain Model:** the methodology touches no entity or invariant; it is a process over documents. No contradiction.
- [E] **Principles Register:** the methodology *is* PR-1 operationalized, plus the promotion-discipline used to build the Register itself; naming it creates no new principle and no duplicate authority. No contradiction — but see the promotion caveat below.
- [E] **Engineering Design Standard / Meta Model / Governance Reviews:** the methodology is a governance process, orthogonal to subsystem design; the Meta Model already has a "Review" type (T12) into which this methodology's *outputs* fall. No contradiction.

**No contradiction found with any ratified governance.**

## 11. Evidence-Sufficiency Verdict (the honest fork the directive demands)

[E] **The methodology is sufficiently evidenced to be NAMED and DOCUMENTED as the observed Decision Review process (this document does exactly that). It is NOT yet sufficiently evidenced to be PROMOTED to binding canonical AIOS Architecture Governance.**

The distinction rests on the same standard applied everywhere in this arc:
- **For naming/documenting:** the count-recurrence (~14 documents, one invariant spine) is more than sufficient. [E]
- **For binding promotion:** the independence criterion is not met — single author, single arc. [E] This is structurally identical to the Human Review multi-reviewer gap: recurrence without independence. Promoting a governance *methodology* to binding status on single-author evidence would be the same over-reach that keeping infrastructure-auditing as an interpretation (not PR-6) avoided.

**What is still needed before canonical promotion** (stated explicitly, per the directive):
1. [O] **Independent application** — the methodology followed by a *different* reviewer (or a future arc) producing consistent results, converting count-recurrence into independence-recurrence.
2. [O] **The external-corpus adaptation (§9)** exercised at least once, confirming the authority/evidence inversion works in practice rather than only in principle.

Until then: the methodology is **documented-and-observed**, available for use, explicitly *not* binding — the same posture the corpus uses for justified-but-not-yet-ratified additions (the Architectural Index, the dedicated Interpretation layer).

## 12. Honest Separation of Method from Habit

[E] Per the directive's demand that habit be distinguished from method: not everything repeated across the documents is *method*. Genuine method (repeated because the reasoning requires it): DR-0 through DR-6, the [E]/[A]/[O] tagging, the reserve-to-Architect close. **Mere writing habit** (repeated by style, not required by reasoning): the table-heavy formatting, the "Stopping here. Awaiting authorization" sign-off phrasing, the section-numbering conventions, the recurring "no code/schema/API was produced" footer. These are consistent but carry no methodological force — a review that used prose instead of tables would be no less rigorous. Naming them as method would inflate the methodology; they are correctly excluded from §6.

---

## Recommendation

[E] **Recommend: adopt this document as the *named, observed* AIOS Decision Review Methodology (DR-0…DR-6), available for consistent use, but do NOT promote it to binding canonical Architecture Governance until the two independence/adaptation gaps in §11 are closed.** This names and structures the proven process (the directive's explicit permission) without over-claiming, preserves the Evidence-First discipline the methodology itself embodies, and states the exact repetition still required — consistent with every prior promotion decision in this arc.

No code, schema, API, implementation, or ratified-document change was produced. No decision was reopened. The question was not silently resolved — it is answered with an explicit sufficiency fork and named prerequisites. Stopping at Architecture Governance Review. Awaiting explicit Architect authorization.
