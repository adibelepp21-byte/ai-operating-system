# AIOS Canonical Architecture Review v1.0

**Status:** Whole-corpus architectural review. Analysis and synthesis only — no code, schema, storage model, API, restructuring, automation, or new architecture. No existing document is modified.
**Version:** v1.0
**Question this review answers:** Does AIOS now possess *one coherent architectural language*, or several partially overlapping ones?
**Evidence discipline:** **[E]** directly evidenced · **[A]** reasoned assumption · **[O]** genuinely unresolved. Every existing document is treated as architectural evidence, not independent truth.

**Corpus inventory (verified):** `docs/constitution/` (1 ratified Constitution) · `docs/architecture/domain-model/` (1 ratified Canonical Domain Model) · `docs/architecture/adr/` (framework + 7 ADRs) · `docs/architecture/` (10 AIOS-level documents) · `docs/knowledge/` (22 documents). ~42 architecture/governance documents in total.

---

## 1. Architectural Coherence Review

**Verdict: one architecture, described across many documents — not multiple competing architectures.** [E] Every document traces its authority to the same two ratified roots (Constitution, Canonical Domain Model); every derived position cites a prior decision rather than asserting independently; no document contradicts a ratified decision. The corpus is one architecture with an archival problem, not two architectures with a reconciliation problem.

Findings, each evidenced, none invented:

- [E] **Duplicated concept (structural): the State/Condition Separation Principle** lives in Blueprint v3 §3 (a subsystem document) *and* as Pattern P4 (Catalog) *and* as the Evolution Model's validity overlay — one AIOS-wide rule, three homes. Carried forward from the Integration Review; still the corpus's single genuine structural duplication.
- [E] **Terminology overload: "Constitution."** Two documents carry the title — the ratified `engineering-constitution-v1.md` and the Phase 6 `AIOS_ARCHITECTURE_CONSTITUTION_v1.0.md` (Execution-Layer scope, explicitly subordinate). Newly surfaced by this review's inventory pass. Low active-confusion risk (the Phase 6 document states its subordinate scope in its own header) but a real title collision on the corpus's most authority-laden word. Recommendation: the Phase 6 document would read more safely as an "Execution Layer Architecture Charter" or similar at a future revision; not modified now.
- [E] **Terminology overloads (confirmed, carried): "Canonical" (4 senses), "Repository" (Knowledge vs. git), "Review" (governed human review vs. architecture-review process).** All qualification issues, not concept confusion — usage is contextually unambiguous in every real instance checked.
- [E] **Conflicting concepts: none found.** The two historical tensions (Home Department vs. DM §8; invariant-10 scope) were both resolved by explicit Architect decision and are reflected consistently everywhere since.
- [E] **Circular definitions: none.** Vocabulary → Catalog is the only cross-reference among the extraction documents and is one-directional.
- [E] **Concepts that should merge:** the three homes of State/Condition Separation should resolve to one (a Principles Register — §6). No other merge justified.
- [E] **Concepts that should remain separate:** supersession (intra-identity) vs. conflict (inter-identity); validity (condition) vs. lifecycle (state); approval vs. admission. All three separations are load-bearing and correctly maintained.
- [E] **Hidden assumption (still tracked):** whether the Questioned condition takes effect on detection or on human confirmation (Blueprint v3 open question #8). No new hidden assumptions found in this pass.
- [E] **Architectural drift: none detected** — every position is traceable to a decision; nothing entered by accretion.

## 2. Canonical Layer Analysis

Layer-placement of each major concept, with relocation recommended only on evidence:

| Concept | Current layer | Correct layer? |
|---|---|---|
| Entity definitions (Knowledge, Memory, Trace, …) | Domain Model | [E] Correct |
| Invariants 1–15 | Domain Model | [E] Correct |
| Governance authority, decision tiers | Constitution | [E] Correct |
| Knowledge subsystem architecture | Blueprint v3 | [E] Correct |
| Reusable mechanisms (P1–P14) | Pattern Catalog | [E] Correct |
| Term definitions | Vocabulary | [E] Correct |
| Approval gates | Quality Checklist | [E] Correct |
| Content-evolution sequence | Evolution Model | [E] Correct |
| **State/Condition Separation** | **Blueprint v3 §3** | **[E] WRONG layer** — an AIOS-wide Principle housed in a subsystem document; belongs in a Principles layer that does not yet exist |
| Evidence First | Implicit (Constitution philosophy + P1) | [A] Under-placed — behaves as a Core Principle but has no formal Principle-layer home |
| Individual architectural decisions (~14 across the Knowledge arc) | Bespoke decision packages | [E] Ambiguous layer — a real ADR framework exists (7 ADRs) but these decisions bypassed it (§6) |

One relocation is evidence-justified: **State/Condition Separation → a future AIOS Principles Register.** All other concepts are correctly placed.

## 3. Principle Validation

AIOS standard for a Principle: independently rediscovered · used multiple times · subsystem-independent · stable · unlikely to change.

| Principle | Independent rediscoveries | Verdict |
|---|---|---|
| Evidence First | Constitution philosophy; every phase; P1 | **Promote** [E] — meets all five criteria; formal naming is recognition, not creation |
| State/Condition Separation | Conflict decision; validity decision; Evolution overlay | **Promote** [E] — already Architect-elevated; needs correct home, not re-justification |
| Detect, Don't Decide | Tier 2 verification; `detect_conflicts()`; Questioned design; recommendation-refusal | **Promote** [E] — four subsystem-independent occurrences |
| Fail Closed | `verification.py`; promotion unknown-handling; decision validation; survived a real violation as a bug-fix | **Promote** [E] — the bug-fix is strong evidence the principle is real and enforced |
| Capture, Don't Reference | DM §6.1 (Trace); `candidate_snapshot`; Blueprint v3 provenance | **Promote** [E] — three occurrences, one already ratified at DM level |
| Signals Prioritize, Never Gate | `promotion.py` ranking; confidence-decides-conflict rejection | **Keep Candidate** [A] — two occurrences, both promotion-adjacent; needs a third independent context |
| Immutable/Append-Only History | Trace invariant 5; Blueprint Decision 4; Evolution Protocol §8 | **Already a Domain Model invariant** — not re-promoted; it outranks the Principle layer |
| Human-Governed Promotion | Invariant 8 | **Already a Domain Model invariant** — patterns P3/P9 are its mechanism |

Five promotions recommended (Evidence First, State/Condition Separation, Detect-Don't-Decide, Fail Closed, Capture-Don't-Reference); one candidate held; the two already-invariant items correctly left where they outrank. **These are Architect decisions; this review recommends, does not enact.**

## 4. Pattern Validation

| Pattern | Verdict |
|---|---|
| P1 Evidence First | [E] Actually a Principle (see §3) — currently double-homed as pattern and principle; resolves when promoted |
| P2 Immutable Audit Trail | [E] Canonical |
| P3 Human-Governed Promotion | [E] Canonical |
| P4 State/Condition Separation | [E] Actually a Principle — resolves on promotion |
| P5 Stable Identity via Correlation Key | [E] Canonical |
| P6 Append-Only Versioning | [E] Canonical |
| P7 Capture, Don't Reference | [E] Actually a Principle candidate (see §3) |
| P8 Provenance Chain | [E] Canonical |
| P9 Detect, Don't Decide | [E] Actually a Principle (see §3) |
| P10 Fail Closed | [E] Actually a Principle (see §3) |
| P11 Authorization Before Invocation | [E] Canonical |
| P12 Explicit Deferred Decisions | [E] Canonical (documentation discipline) |
| P13 Signals Prioritize, Never Gate | [E] Canonical pattern; principle-candidate |
| P14 Readiness with Evidence | [E] Canonical (documentation discipline) |

- **Missing abstractions (evidence-backed, ≥2 independent occurrences):** Read-Time Normalization and Controlled Isolated Experiment — both carried from the Integration Review's §7, both still justified, neither yet added (no rewrite authorized). No new missing pattern found in this pass.
- **Premature abstractions: none** — the Catalog already declined the weak candidates (Dependency-driven Evolution, two-phase-confirmation) explicitly.
- **Key structural observation:** [E] **five of the fourteen catalog "patterns" are actually Principles** (P1, P4, P7, P9, P10). This is not an error in the Catalog — it is evidence that the Principle layer was missing when the Catalog was written, so principles were filed as the nearest available thing. Creating the Principle layer (§6) cleanly resolves five entries at once.

## 5. Vocabulary Integrity Review

- [E] **Sufficient for near-term evolution.** 31 terms, one authoritative definition each, is/is-not/relationships/mistake per term; the state/condition/validity vocabulary is used identically corpus-wide.
- [E] **Overloaded words:** "Canonical," "Repository," "Review," "Constitution" (§1) — recommend qualification notes at next revision, not redefinition.
- [E] **Synonyms / ambiguous / conflicting: none beyond the overloads above.**
- [A] **Missing canonical terms** (candidates, not yet added): **Principle** and **Charter/Register** are used across the corpus but are not themselves defined in the Vocabulary — a gap that becomes material the moment a Principles Register exists. **Home Department** and **Originating Department** are defined in Blueprint v3 but not lifted into the Vocabulary. Recommend adding at the next Vocabulary revision, once the Principles decision (§3) lands.

## 6. Documentation Architecture Review

This is the corpus's genuine weak dimension — unchanged conclusion from the Integration Review, sharpened here.

- [E] **Does documentation scale?** No, not as-is. ~42 documents from one subsystem evolution; a second at the same rate compounds the problem.
- [E] **Multiple sources of truth?** One structural instance (State/Condition Separation, three homes); one decision-recording ambiguity (decision-packages vs. the real ADR framework). Otherwise single-source.
- [E] **Clear navigation paths?** No — zero index, zero supersession markers. Verified: none of the 21 consolidated Knowledge documents carries a "consolidated into Blueprint v3" header; a reader landing on the Phase 8 Lifecycle Contract sees an 8-state model with no signal it was collapsed to 2. The consolidation directive's own misnaming ("Blueprint v2") is direct evidence navigation is already failing.
- [E] **Which are canonical vs. historical?** Currently undocumented. On the evidence, the canonical set is: Constitution, Canonical Domain Model, the 7 ADRs, Blueprint v3, and the six AIOS-level extraction/baseline documents (Pattern Catalog, Vocabulary, Quality Checklist, Evolution Model, Boundary Map, Evolution Protocol, Status Registry). The ~21 pre-consolidation Knowledge documents and the review/decision-package documents are **historical audit trail** — correct and valuable as such, but unmarked.
- [E] **Which should never be edited again?** The audit-trail documents (they record how a decision was reached at a point in time — editing them would corrupt the record, exactly the Trace principle applied to governance docs). This is an unstated but strongly implied rule the corpus already lives by and should make explicit.

## 7. AIOS Architectural Maturity Assessment

| Dimension | Rating | Evidence |
|---|---|---|
| Domain Model | **Mature** | Ratified, stable, 15 invariants, zero reversals across the arc |
| Execution | **Mature** | Frozen v1.0 baseline; 288/288 + 20/20 tests; one real defect found and repaired |
| Memory | **Stable** | Real, tested, governed; deliberately-unstable identity understood and worked around consistently |
| Knowledge | **Emerging** | Architecture settled through Blueprint v3; zero implementation, zero real instances |
| Trace | **Mature** | 540 real records, zero mutations, three schema generations coexisting |
| Governance | **Stable** | Human-authority boundary held structurally across the entire arc, including under pressure |
| Documentation | **Emerging** | Per-document discipline is Mature; corpus-level navigation/supersession is missing — the one dimension holding the whole below Stable |
| Principles | **Emerging** | Five real principles exist but only two are formally elevated and none has a proper home |
| Patterns | **Stable** | 14 evidence-backed patterns; five mis-layered as patterns rather than principles |
| Vocabulary | **Stable** | 31 authoritative terms; small overloads and a few missing terms |
| Evolution | **Stable** | Evolution Model + Quality Checklist + Evolution Protocol give a proven, reusable path |

## 8. Remaining Unknowns (genuine, evidence-insufficient only)

Carried from Blueprint v3, none reopened, none invented: [O] Revision Required trigger (#1) · [O] conflict evidence threshold · [O] cross-Department escalation authority · [O] Retrieval visibility policy across the two dimensions · [O] Questioned-effect-on-detection-vs-confirmation (#8) · [O] whether the Evolution Model applies to behavioral (not only content) evolution. No new architectural unknown surfaced by this review.

## 9. Next Architectural Milestone (exactly one)

**Establish the AIOS Principles layer — an AIOS Principles Register — and relocate the five validated principles into it.**

Why this one, against the stated criteria:
- **Highest leverage:** [E] resolves the corpus's single structural defect (State/Condition Separation mis-homed), cleanly re-layers five of fourteen catalog patterns, and gives Evidence First a formal home — one action, multiple defects closed.
- **Lowest speculation:** [E] every principle it would register already has ≥2 independent real occurrences; it invents nothing.
- **Naturally follows current maturity:** [E] the Principle layer is the one architectural layer the corpus references but does not have; its absence is why principles were filed as patterns.
- **Does not reopen completed work:** [E] it relocates and formalizes existing, validated content; it changes no ratified decision.

Explicitly **not** recommended as the next milestone: the Architectural Index and supersession markers (higher archival value but lower architectural leverage — they organize, they don't resolve a structural defect); ADR reconciliation (a governance decision, better made by the Architect directly than produced as an architecture document); any implementation.

## 10. Final Consistency Verdict

**Is AIOS now internally architecturally consistent? — Mostly Yes.** [E]

Not an unqualified "Yes" solely because of one structural defect (a binding AIOS-wide principle housed in a subsystem document, with five principles mis-layered as patterns) and the documentation-navigation gap. Neither is a *contradiction* — the architecture describes one coherent system with one vocabulary and zero reversed decisions — they are *placement and archival* defects, both closable by the single milestone in §9 plus the documentation-governance recommendations already on record. Nothing in the corpus describes a *different* architecture than any other part.

- **Major strengths:** [E] one architecture from two ratified roots; zero reversed decisions across a full subsystem evolution; a human-authority boundary held structurally, not just procedurally; an evidence discipline that demonstrably caught its own errors early (fingerprint handling, the §8 tension, the verification defect); a proven, reusable evolution path.
- **Remaining weaknesses:** [E] the missing Principle layer (five mis-layered principles, one mis-homed binding rule); corpus-level navigation (no index, no supersession markers); the decision-package/ADR ambiguity.
- **Architectural debt:** [E] low and localized — the Principle-layer defect is the whole of it; everything else is placement, not design.
- **Documentation debt:** [A] moderate and compounding — per-document quality is high, but the corpus lacks the index, supersession markers, and canonical/historical labeling that keep a 40-document set navigable, and the debt grows with each future subsystem.
- **Confidence level:** [E] **High** for the coherence and maturity findings (they rest on direct corpus inspection and the full arc's real evidence); **Medium** for the documentation-scalability projection (it reasons from one subsystem's growth rate to future rates — [A], not yet observed across a second subsystem).

---

No document was modified. No architecture was created. No implementation was performed. No ratified decision was reopened. Stopping here. Awaiting Architect authorization.
