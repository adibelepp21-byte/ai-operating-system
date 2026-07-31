# AIOS Decision Review Methodology — Preliminary Cross-Repository Evidence Review v1.0

**Trigger:** N=3 milestone of the External Repository Validation Program (DSPy #1, LangChain #2, OpenHands #3).
**Scope (directive-bounded):** This is a **Preliminary Evidence Review**, **NOT** a final synthesis. It only: (a) identifies patterns appearing across all three repositories; (b) identifies patterns that turned out unique to one; (c) evaluates whether DR-0…DR-6 stayed consistent across three different domains; (d) evaluates AIOS leakage; (e) records new candidate methodology refinements as **[O]**.
**Prohibitions honored:** promotes nothing; changes no canonical document (Constitution, Domain Model, Principles Register, Engineering Design Standard, Methodology); enacts no refinement; adopts nothing into AIOS; treats every external repository as **evidence, not authority** (Validation Plan §2).
**Confidence:** **[E]** evidenced across the three review documents · **[A]** assumption · **[O]** open question.
**Standing limit:** single reviewer → corpus-independence demonstrable, **reviewer-independence not** (Plan §9). Nothing here is promotion evidence.

---

## 1. What This Review Is and Is Not

[E] **Is:** a first look at what three independent external corpora, each reviewed in isolation, jointly suggest — about the *method* (DR-0…DR-6) and about which observations recur. **Is not:** a conclusion that any pattern is real architecture, that any refinement should be made, or that DR-0…DR-6 is promotable. Three data points can *raise* a hypothesis; they cannot ratify one, and reviewer-independence — the one independence dimension a single reviewer cannot supply — is still absent.

[E] **The corpus spans a deliberate domain gradient** (this is why three was worth reaching):

| # | Repo | Relation to AIOS domain | Governance vocabulary present |
|---|---|---|---|
| 1 | DSPy | **Different domain** (LLM program optimization) | ~none |
| 2 | LangChain | **Overlaps AIOS execution layer** (orchestration/tools/chains) | a few (HITL approve/edit/reject) |
| 3 | OpenHands | **Overlaps execution + touches governance-adjacent** (autonomy-gating, confirmation, provenance) | the most *fragments* (still no unified layer) |

[A] The gradient is a strength for a *preliminary* look (it stress-tests the method at increasing adjacency) but also a caution: three points on a deliberately-chosen gradient are not a random sample. Repository #4+ should probe whether the gradient continues or the pattern breaks.

---

## 2. Patterns Appearing Across All Three Repositories (n=3)

[E] Recorded as recurring **evidence**, explicitly **not** promoted to AIOS patterns or principles.

- **X-1 — External dependency is isolated to a boundary layer.** DSPy `clients/`; LangChain `partners/*` (+ core with no vendor SDK); OpenHands `openhands-sdk` + pinned `litellm`. **All three localize external coupling.** Relation to AIOS: this is *already* a ratified AIOS invariant (DM inv 12). The three repos **corroborate** the wisdom of inv 12 from outside — corroboration only, never authority; inv 12 stands on its own.
- **X-2 — "Trace"/"event" is never a governance accountability ledger.** DSPy `trace` = optimization demonstrations; LangChain `tracer` = opt-in observability; OpenHands `event_store` = operational conversation history. **None is unconditional + immutable + append-only + per-action for accountability** (AIOS inv 4/5 + Constitution §14.2). This is the corpus's **strongest recurring false-cognate** and its most useful *methodology* by-product: a reviewer must always disambiguate an external "trace/event" before comparing it to AIOS Trace. The structural similarity **increased** along the gradient (name-only → structural → central-and-persistent), while the governance guarantee stayed absent — a clean illustration that structural resemblance ≠ governance equivalence.
- **X-3 — No unified governance model, but along a gradient.** None of the three has AIOS's triad (unconditional immutable per-action accountability + human-governed Memory→Knowledge promotion + ratified authority tiers). **However**, governance *fragments* increase with domain adjacency (DSPy ≈none → LangChain HITL → OpenHands confirmation-gate + provenance + local immutability). **Observation, not a claim of AIOS superiority:** governance appears to be AIOS's distinguishing concern in this corpus, and fragments of it emerge precisely as external systems approach AIOS's domain. Whether that holds is **[O]**, for #4+.

---

## 3. Patterns That Turned Out Unique to One Repository (n=1)

[E] Reaching n=3 lets us separate recurring evidence from single-repo idiosyncrasy — a key reason the directive asked for this at the milestone.

- **U-DSPy — Optimizer/`compile` separation (definition vs automatic self-improvement).** Unique; neither LangChain nor OpenHands has an automatic program-optimizer. (DSPy's whole center of mass.)
- **U-LangChain — Uniform composition primitive with an operator DSL (`Runnable`/LCEL `|`).** DSPy has composition (Module) but no operator DSL; OpenHands composes via services/injectors, not one primitive. So the earlier n=2 "uniform composition primitive" signal (R-2) is now seen as **NOT universal** — it belongs to library-shaped repos, not agent-platform-shaped ones.
- **U-OpenHands — Risk-based runtime autonomy gate (SecurityAnalyzer + ConfirmationPolicy) and provenance attribution.** Unique; no analog in DSPy or LangChain (LangChain's HITL is generic approve/edit/reject, not *risk-assessed*).

[E] **Cross-count correction (why n=3 mattered):** the n=2 signal **R-2 (uniform composition primitive)** did **not** survive to n=3 — OpenHands lacks it. This is exactly the kind of premature-pattern the milestone exists to catch: had synthesis run at N=2, R-2 might have been over-weighted. **A partial n=2 pattern that survives:** **R-5 (human gates agent autonomy at runtime)** — LangChain HITL + OpenHands confirmation — still n=2, absent in DSPy; **not** promoted, watched at #4.

---

## 4. Did DR-0…DR-6 Stay Consistent Across Three Different Domains?

[E] Yes, evidenced per-review (each §6). Consolidated:

| Step | DSPy | LangChain | OpenHands | Consistency verdict |
|---|---|---|---|---|
| DR-0 Premise | corrected 1 | corrected 2 | corrected 3 (incl. corpus-boundary) | **Consistent; workload rose with adjacency** |
| DR-1 Grounding | read source; caught name-cognate | read source; caught structural cognate | read source; caught event cognate; bounded SDK scope | **Consistent; front is load-bearing (MF-2, n=3)** |
| DR-2 Options | per-finding | per-finding | per-finding | Consistent |
| DR-3 Canonical eval | tied to invariants/PRs | tied to invariants/PRs | tied to invariants/PRs (+PR-3 tension) | Consistent |
| DR-4 Classification | needed "for-AIOS-purpose" qualifier ×3 | clean; 1 qualified Stronger | clean; needed "fragment" qualifier | **Consistent; commensurability rises with overlap (MF-1 confirmed)** |
| DR-5 Recommendation | tagged; 0 Adopt | tagged; 0 Adopt | tagged; 0 Adopt | Consistent |
| DR-6 Consistency + reserve | reserved to Architect | reserved to Architect | reserved to Architect | Consistent |

[E] **Verdict: DR-0…DR-6 held on all three domains, with no unexplained structural divergence (M-5 clean, F-2 not triggered).** Its front (DR-0/DR-1) did progressively more real work as corpora approached AIOS's domain — the method scaled *up* with risk rather than degrading. **[A]** This is a genuinely encouraging N=3 result for the *method*; it remains short of promotion (reviewer-independence absent).

---

## 5. AIOS Leakage Across the Corpus

[E] **M-6 = 0 in all three reviews.** Stage-2 (Architecture Extraction) contained no AIOS vocabulary in any review; all comparison was quarantined to Stage 3+. The number of *named cognates* rose (DSPy 1 → LangChain 3 → OpenHands 4), but **naming a cognate is leakage prevention, not leakage** — it is the mechanism by which shared vocabulary was stopped from becoming a false "Already Present." **F-1 (cannot complete without AIOS knowledge) not triggered** in any review. The corpus-independence half of the Plan's ceiling (Plan §9) is, so far, **empirically supported**; the reviewer-independence half remains structurally unmet.

---

## 6. New Candidate Methodology Refinements (all [O]; none promoted, none enacted)

[E] Carried forward from the three reviews and this cross-look. **Each is a candidate only; the methodology document is unchanged; the directive forbids promotion.**

- **[O] MF-1 (confirmed):** DR-4's Stronger/Weaker axis is unreliable **only for different-domain corpora**; reliable as domains overlap. Confirmed across N=3.
- **[O] MF-2 (now n=3):** DR-0/DR-1 are load-bearing, not ceremonial — the method's front catches real errors on every corpus.
- **[O] MF-3 (n=2):** overlapping-domain corpora warrant an explicit "domain-overlap leakage check" (shared vocabulary raises cognate risk).
- **[O] MF-4 (new, from OpenHands):** DR-4 may need a **partial-cognate/fragment qualifier** — for findings that are *fragments* of an AIOS concept (a gate ⊂ governance; provenance ⊂ accountability; frozen ⊂ immutability), neither full-match nor fully-N/A.
- **[O] MF-5 (new, from this cross-look):** the milestone itself surfaced value — an n=2 signal (R-2 uniform-composition-primitive) **failed to survive to n=3**. Candidate: the Plan could formalize that **no pattern is admissible below n=3 AND surviving at least one domain-shape change**, not merely n≥3 count. Reserved.

[E] **Explicitly NOT done:** no refinement applied; no DR step added, removed, or reworded; no new classifier introduced; the Methodology document (`AIOS_DECISION_REVIEW_METHODOLOGY_REVIEW_v1.0`) and the Validation Plan are untouched.

---

## 7. Consistency Review (this document)

- [E] **Constitution / Domain Model / Principles Register / Engineering Design Standard:** none modified; all used only as evaluation references. §6.2-inv-2, §14.2, inv 4/5/8/12, PR-1/3/4 cited, none altered.
- [E] **Methodology & Validation Plan:** unchanged; this document *reports on* them, does not revise them. Refinements remain [O].
- [E] **Three review documents:** unmodified; each remains independent evidence. This document only *reads across* them.
- [E] **Authority/Evidence Inversion:** upheld — all three repos are evidence; none is authority; no external design was adopted or copied.

**No contradiction found. No canonical change. No promotion. No synthesis.**

---

## 8. Summary and Stop

[E] Across a deliberate **domain gradient** (different-domain → execution-overlap → governance-adjacent), three independent external reviews jointly show: **(1)** three recurring evidence signals — external-dependency isolation (X-1, corroborates inv 12), "trace/event is never governance-audit" (X-2, the strongest false-cognate), and no-unified-governance-along-a-gradient (X-3); **(2)** three single-repo-unique features (DSPy optimizer, LangChain LCEL, OpenHands risk-gate), and one n=2 signal that **failed** to reach n=3 (uniform composition primitive), plus one n=2 signal still standing (human-gates-agent); **(3)** **DR-0…DR-6 held consistently across all three domains**, its front doing more work as adjacency rose; **(4)** **AIOS leakage M-6 = 0** throughout; **(5)** five candidate refinements, **all [O], none promoted, none enacted.**

[A] **Honest ceiling restated:** this is a *preliminary* look at N=3 — enough to raise and to *falsify* hypotheses (it already falsified one premature pattern), **not** enough to promote the methodology. Corpus-independence is empirically supported; reviewer-independence remains structurally unmet (Plan §9, O-1) — the sufficiency question stays reserved to the Architect.

No implementation, code, schema, API, or subsystem was produced. No external design was copied or adopted. No AIOS canonical document was created or modified. No principle or refinement was promoted. No governance event or record was fabricated. Trace store unchanged (540 records); no `execution/` file touched.

**Stopping here. Awaiting Architect authorization before repository #4 is processed.** Final synthesis remains deferred beyond this preliminary look.
