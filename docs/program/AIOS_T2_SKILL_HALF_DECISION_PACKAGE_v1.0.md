# T-2 Skill Half — `Capability ↔ Skill` · Architecture Decision Package

**Prepared under:** FOUNDER · `ACT-CC-F03-052` `DEC-F03-052 = OPTION A` · Moriarty · 26-08-2026
**Track:** Architectural Decision / Ratification · **Construction: NOT AUTHORIZED** (`§4`, `§8`)
**Outcome offered (`§9`):** the evidence supports **outcome 1 or 2**; the choice is Architect-reserved.

> **PROPOSED — NOT CANONICAL.** Nothing here ratifies a relationship, alters the
> `[O]` reservation, canonicalizes, synchronizes a specification, or touches
> source or tests. `§8` forbids reading any of that into `OPTION A`. Every
> proposal is marked **[P]**.

---

## 1. Decision consumed

```text
DEC-F03-052 = OPTION A — AUTHORIZE Architectural Decision / Ratification Track
Founder: Moriarty · Date: 26-08-2026 · Signature / Confirmation: Moriartyz
```

Exactly one option checked · attribution · date · confirmation. **VALID.**

**[O] Two observations, recorded as supplied, not corrected.** The signature
reads *"Moriartyz"*. The date reads **26-08-2026**, where the preceding Acts in
this sequence are dated 21-08-2026.

## 2. Re-read from source, not carried forward

`ACT-CC-F03-044` analysed T-2 as a whole. **That analysis is evidence, not
authority, and it is now partly out of date**: since it was written, the Workflow
half was ratified and canonicalized, Domain Model §4 gained an entry, Freeze §6
gained a row, Freeze §10 was partially discharged, and INV-2 clause 2 and INV-15
were built. Everything below was re-derived against the current repository.

## 3. Evidence — what the canonical sources say now

### 3.1 Six ratified sources exclude a direct edge

| # | Source | Statement |
|---|---|---|
| 1 | **Domain Model §4** — the ratified relationship list, parsed | Ten edges touch Capability or Skill. **None** joins them directly. |
| 2 | **Freeze §6** — frozen *Observed* relationship table | Three rows touch Capability. **No** Capability↔Skill row. |
| 3 | **Freeze §4 — Capability** | **[E]** *Allowed*: *"be implemented by Agent Definitions; depend on Capabilities…"* — Skill absent |
| 4 | **Freeze §4 — Skill** | **[E]** *Allowed*: *"be used by an Instance; be declared by Definitions."* — Capability absent |
| 5 | **Blueprint §7 — Capability package** | **[E]** *Allowed dependencies*: *"its Department; other Capabilities…"* — skill **excluded** |
| 6 | **Blueprint §9 — Skill package** | **[A]** *Allowed dependencies*: *"used by agent; composed in workflow."* — capability **excluded** |

And decisively, from the Skill specification itself:

| 7 | **`skill_spec §7`** | **[E]** *"Used by Agent Instances; composed within Workflows; declared by Agent Definitions (INV-15)."* — **three** allowed relations, Capability **not** among them |

Row 7 is `[E]`, not `[O]`. The Skill boundary's *ratified* dependency list already
enumerates what a Skill relates to, and a Capability is not on it.

### 3.2 The reservation, still open

| Source | Statement |
|---|---|
| **Freeze §10** | **[O]** *"Inferred relationships — Capability↔**Skill**; Agent-Instance↔Skill/Knowledge; Runtime↔Workflow"* — the Workflow half was discharged under `DEC-F03-046`; **the Skill half was not** |
| `capability_spec §12`, `§14` | **[O]** `Capability↔Skill` composition / ratification |
| `skill_spec §14` | **[O]** *"Skill↔Capability/Workflow composition ratification (Inferred)"* |

### 3.3 **[E] Two derived paths now connect them — and both are implemented**

```text
Path 1   Capability  ←implements—  Agent Definition  —specifies→  Skill
             (INV-2 cl.2, DM §4)              (INV-15, DM §4)

Path 2   Capability  ←realizes—    Workflow          —contains→   Skill
             (DM §4, Freeze §6)               (DM §4, Freeze §4)
```

Both legs of both paths are ratified, and **both paths were exercised
end-to-end against the built code**: Path 1 through
`AgentDefinition.implemented_capabilities` + `.specified_skills`; Path 2 through
`WorkflowRealization` + `WorkflowComposition`.

**Path 2 did not exist when `-044` was written.** Ratifying the Workflow half
*created* a second connection between Capability and Skill. The Skill half is
therefore a materially weaker candidate for a direct edge now than it was then —
the gap it would close is already spanned twice.

### 3.4 **[E] The Workflow precedent does not transfer**

`ALT-3` was chosen for the Workflow half partly because one resident source
already supplied the verb and direction: `workflow_spec §7` read *"realizes
Capabilities (Inferred, reserved)."*

**There is no equivalent for Skill.** `skill_spec` contains **no occurrence of
"realiz"** in any form — searched directly. No resident source proposes a verb,
a direction, or a shape for a Skill↔Capability edge. Adopting the mirror of
ALT-3 would mean **authoring** the semantics, not discharging a reservation over
semantics already written down.

This is the single most important asymmetry between the two halves of T-2, and
it is why symmetry with the Workflow decision is **not** by itself an argument.

## 4. Alternatives (`§4.1`–`§4.3`)

Each states the relationship, its direction, whether it is direct or derived,
and its consequences. **All are [P]; none is a recommendation.**

### 4.1 **[P] S-ALT-1 — Derived, not declared**

*A Capability stands in relation to a Skill only through an Agent Definition
that implements the Capability and specifies the Skill, or through a Workflow
that realizes the Capability and contains the Skill. No direct edge exists.*

- **Direction:** n/a — derived from four ratified edges.
- **Frozen artifacts changed:** **none.** Domain Model §4 and Freeze §6 are read
  as already complete.
- **Specification:** `capability_spec §12`/`§14` and `skill_spec §14` move `[O]`
  → `[E] derived`; Freeze §10's Skill half is discharged as *derived*.
- **Consequence:** T-2 closes fully with no new architecture. Consistent with
  rows 1–7, all of which exclude the direct edge.

### 4.2 **[P] S-ALT-2 — Direct edge `Capability composes Skill`**

- **Direction:** Capability → Skill.
- **Requires:** a Domain Model §4 entry; an amendment to **Blueprint §7's [E]**
  Capability allowed-dependency list; probably a new invariant for cardinality
  and governance.
- **Tension, unchanged from `-044` and now sharper:** Domain Model §2 defines a
  Capability as *"a stable, named, outcome-oriented contract — **what** can be
  delivered, **independent of how**"*, while a Skill is *"a discrete, reusable,
  bounded unit of **executable ability**"*. A direct edge puts the *what* in
  contact with the *how*. Rows 3 and 5 exclude it on `[E]` authority.
- **Cost:** highest of the four.

### 4.3 **[P] S-ALT-3 — Skill-side edge `Skill realizes Capability`**

- **Direction:** Skill → Capability, mirroring the ratified Workflow half.
- **Requires:** a Domain Model §4 entry; an amendment to **Blueprint §9's [A]**
  Skill allowed-dependency list; and — unlike ALT-3 — an amendment to
  **`skill_spec §7`'s [E]** allowed-relations list, which today enumerates three
  relations and would gain a fourth.
- **Support:** symmetry with `DEC-F03-045`.
- **Against:** **no resident textual precedent** (§3.4). The verb *realizes*
  would be imported from the Workflow decision by analogy, and analogy is not
  evidence. It would also make a Skill — *executable ability* — a direct
  realizer of a contract, which is closer to Workflow's role (*"an explicit,
  inspectable composition … accomplishing a multi-step outcome"*) than to a
  Skill's.

### 4.4 **[P] S-ALT-4 — Record as Not Applicable**

Ratify that no relationship exists, direct or derived. Distinguished from
S-ALT-1 only in refusing to describe the derived paths — which, unlike in
`-044`, would now leave **two** implemented paths undescribed rather than one.

### 4.5 Rejected

Inventing cardinality, ownership or lifecycle semantics for the edge — no
resident source supplies them. Implementing first and ratifying after —
forbidden by `§4`/`§8`. Importing an external composition model — resident
evidence is sufficient; **no external research was used**.

## 5. Consequences for canonical architecture (`§4.4`)

| | S-ALT-1 | S-ALT-2 | S-ALT-3 | S-ALT-4 |
|---|---|---|---|---|
| Domain Model §4 | — | **+1 edge** | **+1 edge** | — |
| Freeze §6 table | — | **+1 row** | **+1 row** | — |
| Freeze §10 Skill half | discharged as *derived* | discharged as *direct* | discharged as *direct* | closed as n/a |
| Blueprint | — | **§7 [E]** amended | **§9 [A]** amended | — |
| `skill_spec §7` **[E]** | — | — | **amended** | — |
| Entity count | 12 | 12 | 12 | 12 |
| Core boundaries | 11 | 11 | 11 | 11 |

**No alternative requires a new entity or a new boundary.**

## 6. Authority required for ratification (`§4.5`)

**[O] Architect.** Freeze §10 is explicit: each inferred relationship *"awaits an
**Architect decision** before it enters any freeze."* S-ALT-1 and S-ALT-4 need
only that. S-ALT-2 and S-ALT-3 additionally amend the Canonical Domain Model,
the Architecture Freeze and the Blueprint — and S-ALT-3 also an `[E]` clause of
`skill_spec` — each of which is Founder/Architect-reserved and beyond this
package's scope.

**I hold no constitutional authority and cannot ratify.** This package prepares
the decision; it does not make it, and no ranking among the four is offered.

## 7. Separate finding — **[D] `skill_spec` contradicts itself**

**[E]** `skill_spec §14` reads **[O]** *"Skill↔Capability/**Workflow**
composition ratification (Inferred)."* But `skill_spec §7` reads **[E]**
*"…**composed within Workflows**…"*, Domain Model §4 carries *"Workflow
**contains** Skill"*, and Freeze §4 lists *"compose Skills"* among a Workflow's
allowed relations.

**The same specification classifies Skill↔Workflow as both `[E]` and `[O]`, two
sections apart.**

This is the **exact mirror** of the finding already recorded against
`workflow_spec §14` (Track B), and it is the same root cause: the `§14` entries
bundle `Capability/Workflow` as one item, so discharging half of a bundle leaves
the other half mis-stated. **It is not created by this Act, is outside its scope
(`§4`), and was not touched.** It belongs with Track B, and resolving both
together would be one decision rather than two.

## 8. State

No canonical artifact, specification, source file or test was modified.
`native_core` **584 OK** (1 expected failure) · `tools` **20 OK** ·
`bounded_exception` **29 OK**, all unchanged. Entity count **12**, core
boundaries **11**. `Capability↔Skill` remains **[O]**. Construction remains
**NOT AUTHORIZED**.

## 9. What the successor must state (`§9`)

Exactly one of:

1. **Relationship ratified** — naming which alternative, after which a
   *separate* canonicalization gate is required (the `-046` → `-047` → `-048`
   sequence, which must not be collapsed);
2. **Relationship rejected / deferred** — Freeze §10's Skill half stays `[O]`, or
   closes as Not Applicable under S-ALT-4;
3. **Further architectural decision required.**
