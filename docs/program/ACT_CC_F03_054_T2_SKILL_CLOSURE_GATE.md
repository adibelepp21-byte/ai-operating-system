# `ACT-CC-F03-054` — T-2 SKILL HALF CLOSURE GATE (S-ALT-1)

> **DRAFT — PREPARED BY THE CO-FOUNDER OFFICE · AWAITING FOUNDER ISSUANCE.**
> Produced under `ACT-CC-F03-053 §10`. **This document confers no authority on
> itself.** Until it is issued, the `[O]` reservation stands undischarged and no
> artifact may be mutated (`ACT-CC-F03-053 §9`, `§11`).

**Predecessor:** `ACT-CC-F03-053` · **Determination consumed:** `DEC-F03-053 = S-ALT-1`
**Type:** Closure / Canonicalization Gate · **Construction authority:** NONE, and none is needed
**Prepared:** 2026-08-21 · **Repository state:** `2402da7`, tree clean

---

## §1 — What this gate is for

`DEC-F03-053` determined that a direct `Capability ↔ Skill` relationship takes
**no** semantic form: the entities are sufficiently connected by two ratified,
implemented derived paths.

`ACT-CC-F03-053 §10` requires a successor Act to **record closure** of the T-2
Skill half and confirm no construction target remains from the direct edge.

**This gate asks one question: may the six live `[O]` sites be discharged as
`derived`?**

## §2 — Why this is closure, not construction

**[E] Nothing is built by S-ALT-1.** Verified under `ACT-CC-F03-053 §3`: no
source module references a pending direct edge, and both derived paths already
run in code. The Skill half therefore closes **without any construction target**,
and this gate grants no construction authority because none is required.

**[E] No conformance test changes either.**
`test_skill_and_workflow_composition_is_not_modelled` asserts the Capability
surface names neither Skill nor Workflow. Under S-ALT-1 that becomes permanently
correct rather than provisionally correct. Its basis strengthens; its assertion
does not move. **No test may be modified under this gate.**

## §3 — The closure targets — six live sites

| # | Site | Current | After closure |
|---|---|---|---|
| C-1 | **Freeze §10** | `Capability↔**Skill**` listed as an Inferred relationship | discharged as **derived**, with the prior text preserved verbatim as it was for the Workflow half |
| C-2 | `capability_spec §12` | **[O]** *"composition is currently Inferred (reserved)"* | **[E] derived** — no direct edge; the connection runs through Agent Definition or Workflow |
| C-3 | `capability_spec §14` | **[O]** *"relationship ratification — the Skill half only"* | resolved; the remaining `§14` reservation (versioned-contract representation) **stays** |
| C-4 | `skill_spec §14` | **[O]** *"Skill↔Capability/Workflow composition ratification (Inferred)"* | see `§5` — **entangled**, and possibly out of scope |
| C-5 | **Domain Model §4** | inline note *"Capability ↔ Skill remains `[O]` reserved"* | restated as **derived**; **no relationship entry is added** — S-ALT-1 adds no edge |
| C-6 | **`NCIR §9.6`** | **Reserved [O]:** *"Capability↔Skill/Workflow (Inferred)"* | see `§5` — **entangled** |

**[E] C-5 adds no edge to Domain Model §4.** That is the defining difference
between this closure and the Workflow one: `DEC-F03-046` C-1 *added* a
relationship; S-ALT-1 adds none and only corrects a note. **Entity count stays
12, core boundaries stay 11, and the frozen relationship table gains no row.**

## §4 — Preservation constraints

Historical `[O]` records must **not** be rewritten to erase their prior state —
the discipline applied at `DEC-F03-046` C-2b. Specifically preserved:
`docs/architecture/history/` Phase-3 Authorization Review, Implementation
Readiness Review, Architecture Specification §59/§214, and Architecture Review
R-A1/C-2. Each records the reservation as it stood and remains accurate as
history.

Also unchanged: the Constitution · the Finding Register · the eleven-boundary
constraint · the twelve-entity set · every ratified relationship including the
four legs of the two derived paths · all governed exceptions.

## §5 — **[D] An entanglement the Founder should resolve before issuing this**

C-4 and C-6 **cannot be cleanly closed by a Skill-half decision alone**, because
neither states only the Skill half:

- `skill_spec §14` reads *"Skill↔**Capability/Workflow** composition
  ratification (Inferred)"* — but Skill↔Workflow is **already ratified** and
  `skill_spec §7` itself says so **[E]**. The line is internally contradictory
  *today*, independently of T-2.
- `NCIR §9.6` reads *"Capability↔**Skill/Workflow** (Inferred)"* — still bundling
  the Workflow half that `DEC-F03-046` ratified. **Stale today.**

Together with `workflow_spec §14` (recorded as **Track B**), that is **three
documents with one root cause**: entries that bundle two relationships as one
item, so discharging half a bundle leaves the other half mis-stated.

**Two ways forward, and the choice is the Founder's:**

- **(a) Narrow.** Issue this gate for **C-1, C-2, C-3, C-5 only**. C-4 and C-6
  are left to the Track B decision, which would then cover all three bundling
  defects at once. Cleanest separation; leaves two stale lines standing a while
  longer.
- **(b) Combined.** Fold Track B into this gate and close all six sites plus
  `workflow_spec §14` together, since one root cause underlies them all. Fewer
  gates; mixes a T-2 closure with a pre-existing specification defect that T-2
  did not create.

**No recommendation is offered.** Absent an explicit instruction, an executor
should take **(a)** — the narrower reading — and leave C-4 and C-6 untouched,
because it is the one that cannot exceed the determination actually made.

## §6 — Founder decision block

```text
DEC-F03-054 — T-2 Skill Half Closure

[ ] OPTION A — AUTHORIZE closure, NARROW  (C-1, C-2, C-3, C-5; C-4 and C-6 to Track B)
[ ] OPTION B — AUTHORIZE closure, COMBINED (C-1…C-6 plus workflow_spec §14)
[ ] OPTION C — DEFER closure (determination stands recorded; [O] sites unchanged)

Founder: ____________________
Date: ____________________
Signature / Confirmation: ____________________
```

Exactly one option. No default, and no closure may be inferred from the
determination alone — `ACT-CC-F03-053 §9` is explicit that the reservation is
**not** discharged until a successor gate is issued.

## §7 — Verification the executing Act must perform

Determination consumed exactly as recorded · each targeted site discharged as
**derived**, never as a new relationship · **no** entry added to Domain Model §4 ·
**no** row added to the Freeze §6 frozen table · prior text preserved at every
discharged site · historical records untouched · entity count **12** · core
boundaries **11** · **zero** source and conformance-test changes · full
regression unchanged (`native_core` 584 / `tools` 20 / `bounded_exception` 29) ·
Constitution and Finding Register hash-identical · governed exceptions untouched.

## §8 — What remains open regardless

T-12 (Knowledge admission model) · OB-01 · `DEC-AE04` · `DEC-REVOCATION` ·
`DEC-ADOPTION` · `RG-2` · `RG-3` · the `GDR-0025`/`-0026` count correction · and,
under option (a), Track B with its three bundling defects.
