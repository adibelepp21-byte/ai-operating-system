# Phase 5 Semantic Reconciliation & `DEC-PHASE5-SEMANTICS`

**Prepared under:** FOUNDER · `ACT-CC-F03-031 §7`, `§8` · **Date:** 2026-08-20
**Consolidates:** `§12.3` and `§12.6` (the Founder Decision Package is §4 below)

---

## 1. The question

Does "Phase 5 — Intelligence Ecosystem" denote a **new architectural entity**, or
the **collection of Capability categories** already named by the Capability
Catalog?

## 2. The distinctions the Act requires be held apart (`§7`)

```text
Capability category  ≠  Intelligence architectural entity  ≠  Planner  ≠  Scheduler  ≠  Execution Orchestrator
```

All five are kept separate throughout. Nothing below merges them.

## 3. Evidence

### 3.1 Supporting Interpretation B (Intelligence = Capability categories)

- The Master Program's **Capability Catalog** enumerates Cognitive · Engineering · Mathematical · Quantitative · Scientific · Strategic · Domain Intelligence.
- The consolidated Master Roadmap `§11` states Phase 5 scope *"termasuk capability categories yang berada dalam Capability Catalog"* and cites the Catalog as the source.
- **Capability is fully ratified**: Architecture Freeze **21** occurrences, Canonical Domain Model **26**, an engineering specification, and a built, tested subsystem.

### 3.2 Against Interpretation B — the decisive counter-evidence

`capability_spec §13 Future Evolution`, verbatim:

> **[O]** *Department Architecture (**Phase 5**) realizes Organization/Department/Capability ownership as a governed structure; **reserved to the Architect**.*

A Capability is *"owned by exactly one Department"* (INV-1). Instantiating
Catalog categories as Capabilities therefore requires the **Department
Architecture** — which the Capability specification itself **reserves to the
Architect and locates in Phase 5**.

Two further reservations in the same spec:

> `§12` **[O]** *Capability↔Skill/Workflow composition is currently **Inferred (reserved)**.*
> `§14` **[O]** *Versioned-contract representation — **reserved; no format defined here**.*

### 3.3 Against Interpretation A

**"Intelligence" has 0 occurrences in the Architecture Freeze and 0 in the
Canonical Domain Model.** It is not a ratified entity, is not among the twelve,
and has no engineering specification. Interpretation A would require ratifying a
new canonical entity — `§18` Founder/Architecture-reserved.

## 4. `DEC-PHASE5-SEMANTICS` — Founder Decision Package (`§8`)

**1. Exact question.** Is Phase 5 "Intelligence Ecosystem" (A) a new architectural
entity to be ratified, or (B) the Capability categories of the Capability Catalog
realized through the existing Capability entity?

**2. Source evidence.** Capability Catalog; Master Roadmap `§11`; `capability_spec`
`§1`, `§13`; Architecture Freeze `§2`, `§4`; Canonical Domain Model.

**3. Conflicting evidence.** The roadmap points to B. The Capability specification
blocks B's execution path by reserving Department Architecture to the Architect.
Neither source ratifies A. **Interpretation B is therefore *supported in meaning*
but *not executable* on current architecture — the conflict is real and is not
resolvable by engineering.**

**4. Interpretation A — Intelligence as a new architectural ecosystem/entity.**
Requires ratifying a new canonical entity, its ownership, dependencies,
invariants and specification.

**5. Interpretation B — Intelligence as Capability categories.** Requires no new
entity, but **does** require ratifying the reserved **Department Architecture**
before any category can be instantiated, because INV-1 requires a Department owner.

**6. Architectural consequences.** A: the twelve ratified entities become
thirteen; every downstream invariant must be re-examined. B: the entity set is
unchanged; the Organization/Department Spine moves from reserved to ratified.

**7. Dependency consequences.** A: a new dependency surface with no current
consumers. B: Capability gains a Department owner; `Capability↔Skill/Workflow`
remains Inferred and reserved under either.

**8. Implementation consequences.** A: a new `native_core` subsystem, a twelfth.
B: **no new subsystem** — `core/capability/` already implements INV-1/9/10/11/14
and passes its completion criterion; the work becomes populating governed data
under a ratified Department structure.

**9. Risks.** A risks entity proliferation and re-opening the frozen entity set.
B risks nothing architecturally new but is **blocked until Department
Architecture is ratified** — and that ratification is itself the larger decision.
Choosing neither leaves Phases 5–13 unstartable.

**10. Recommendation.** **Interpretation B**, on three grounds: it is what the
Founder-supplied roadmap says; it adds no entity to a deliberately frozen set;
and the Capability subsystem it relies on is already built, specified and green.
**The recommendation is that B is the better reading — not that B is executable
today.** Under B the real next decision becomes ratification of Department
Architecture, which is the same decision either way and is `§18`-reserved.

**This recommendation is not a decision and was not applied to anything.**

**11. Exact Founder action required.** State one of:
- *"Phase 5 Intelligence = Capability categories (Interpretation B)"* — and, separately, whether Department Architecture ratification is authorized; or
- *"Intelligence is a new architectural entity (Interpretation A)"* — which opens an entity-ratification path; or
- a third reading, stated.

## 5. Status

`DEC-PHASE5-SEMANTICS` = **OPEN — FOUNDER DECISION REQUIRED.** No interpretation
was adopted, inferred, defaulted, or acted upon.
