# `ACT-CC-F03-056` — ARCHITECTURAL DEFINITION PACKAGE · `governs`

**Executed under:** FOUNDER · `ACT-CC-F03-056` · **OPTION A — Architectural Definition Track** · Moriarty · 21-08-2026
**Result:** **CASE A — semantics sufficiently defined for ratification** (`§9`)
**Construction:** **NONE PERFORMED, NONE AUTHORIZED** (`§12`)

> **PROPOSED — NOT RATIFIED.** `§5` forbids canonicalizing, changing any
> specification, source or test, or treating this assessment as ratification.
> **Nothing was changed.** The successor is a Ratification Gate, not construction.

---

## 1. Canonical evidence inventory (`§8.1`)

| # | Source | Bearing |
|---|---|---|
| E-1 | **Domain Model §4** | carries both edges: `Organization **governs** Platform Division`, `Capability **governs** Agent Definition` |
| E-2 | **Domain Model §6** — Agent Definition row | **[E]** *"Versioned; created/deprecated at Platform Division discretion **within Capability governance**. Its version is **bound to the Capability contract version it implements**."* |
| E-3 | **Domain Model §6** — Platform Division / Capability row | **[E]** *"Created/retired via architectural decision, **architect approval**."* |
| E-4 | **Domain Model §2** — Organization | **[E]** *"The whole of AIOS. Single root identity; **ultimate accountable body**."* |
| E-5 | **Domain Model §2** — Platform Division | **[E]** *"A bounded, **semi-autonomous** unit of accountability with its own domain vocabulary. **Owns** Capabilities and Agent Definitions."* |
| E-6 | **Domain Model §2** — Capability | **[E]** *"a stable, named, outcome-oriented **contract** … **Carries dependency-governance rules**."* |
| E-7 | **Freeze INV-10** | **[E]** *"Cross-Department Capability dependencies require **governance approval** through the Decision-Making Process — never silent adoption."* |
| E-8 | **Freeze INV-8** | **[E]** Memory → Knowledge *"only through **governed review** — never automatic."* |
| E-9 | **Freeze INV-14** | **[E]** a zero-implementer Capability *"must be **flagged for governance review**."* |
| E-10 | **Domain Model §5** *Ownership Rules* | **[E]** assigns exactly one owner per owned entity |

**Negative evidence, equally load-bearing:** the verb `governs` is **absent** from
Freeze §4, Freeze §6's frozen relationship table (parsed: zero rows), the
Blueprint, and the **Canonical Relationship Model §5** — the synthesis that maps
eighteen edges *"using only sanctioned verbs … none invented."*

## 2. Current semantic state (`§8.2`)

`governs` is **ratified as an edge** (E-1) and **undefined as a verb** — no source
states its meaning directly. **But its operational content is stated indirectly**,
and that is what E-2 through E-9 supply.

## 3. `owns` — semantic baseline (`§8.3`)

**[E]** `owns` is **possession with exclusivity and accountability**: Domain Model
§5 assigns exactly one owner to each owned entity (E-10); INV-1 and INV-2 clause 1
fix *"exactly one"*; a Platform Division is *"a unit of **accountability**"* (E-5).

**[E] What `owns` does *not* confer: lifecycle authority.** E-3 places creation
and retirement of a Platform Division and a Capability with **architect
approval** — not with the owner. This is the single most important control in
this analysis: it forecloses defining `governs` by analogy to owning.

## 4. `governs` — candidate semantics (`§8.4`)

**[P] PROPOSED DEFINITION**

> **`A governs B`** — **A bounds the discretion exercised over B, without
> possessing B.** The owner of B retains the discretion to act; the governor
> constrains the conditions under which that discretion is valid. Governance is
> a **constraint and approval relation**, never a possession relation.

**Derivation, entirely from resident text — not analogy, not import:**

**E-2 is the decisive sentence.** For `Capability governs Agent Definition`, the
Domain Model states all three roles in one line:

| Role | Who | Text |
|---|---|---|
| **Owner acts** | Platform Division | *"created/deprecated at **Platform Division discretion**"* |
| **Governor bounds** | Capability | *"**within Capability governance**"* |
| **The concrete bound** | — | *"its version is **bound to the Capability contract version it implements**"* |

Ownership supplies the discretion; governance supplies its limits. **The two are
named separately in the same clause and do not collapse.**

**The pattern is uniform across canon.** Every `govern*` usage in the ratified
sources denotes a **gate, review, approval or cadence constraint** on an action —
INV-10 *"governance **approval**"* (E-7), INV-8 *"governed **review**"* (E-8),
INV-14 *"flagged for governance **review**"* (E-9), and E-6's Capability
*"carries dependency-**governance rules**."* **Not one usage denotes possession.**

## 5. Explicit distinction (`§8.5`, Q2, Q7)

| Property | `owns` | `governs` |
|---|---|---|
| Possession | **Yes** — Canonical (E-10) | **No** — Canonical by absence; no source assigns possession to a governor |
| Exclusivity | **Exactly one** — Canonical (INV-1/2) | **Unknown** — no source states multiplicity |
| Accountability | **Yes** — Canonical (E-4, E-5) | **Yes** — Canonical (E-4: Organization is the *ultimate accountable body*) |
| Control over the act | **No** — the owner *performs*, not permits | **Yes** — Canonical (E-2, E-7, E-8) |
| Lifecycle authority | **No** — Canonical (E-3: architect approval) | **Bounding only** — Canonical (E-2: the owner creates/deprecates *within* governance) |
| Decision rights | **Discretion to act** — Canonical (E-2) | **Right to constrain / approve** — Canonical (E-7) |

**Q7 — `governs` is not an alias for `owns`.** Three independent proofs:
**(i)** Domain Model §4 lists `Organization owns Platform Division` **and**
`Organization governs Platform Division` as **separate edges** — an alias would
be redundant in a list that elsewhere avoids redundancy. **(ii)** E-2 names owner
and governor as **different entities** for the same act — the Platform Division
owns and acts, the Capability governs. **(iii)** A Capability **owns nothing**
(E-10 gives Agent Definitions to the Platform Division), yet it governs — so
governance without ownership is not merely possible, it is the ratified case.

## 6. Dependency implications (`§8.6`, Q4)

**[P] `Capability governs Agent Definition` creates NO package dependency.**

**Why the relationship is representable without a boundary import:** E-2 states
the constraint **as a property of the governed entity** — *"**its** version is
bound to the Capability contract version **it** implements."* The obligation sits
on the Agent Definition. So the edge is expressed where it is already expressed:
`AgentDefinition.implemented_capabilities`. The Capability boundary need not
reference Agent Definitions at all.

This preserves **Blueprint §7's `[E]`** allowed-dependency list for the Capability
package (*"its Department; other Capabilities"*) **without amendment** — resolving
the tension flagged in `ACT-CC-F03-055`, which noted the edge ran in a direction
that list excludes. **Under this definition, no amendment is needed:** the arrow
in Domain Model §4 denotes an accountability/constraint relation, not an import.

## 7. Lifecycle implications (`§8.7`, Q5)

**[P] `governs` confers no independent lifecycle authority.** E-3 keeps creation
and retirement with **architect approval**; E-2 keeps the act with the **owner's
discretion**. Governance **bounds** that act and does not replace either. Existing
canonical lifecycle authority is therefore untouched, exactly as `§6`'s Q5
requires when the answer is negative.

## 8. Treatment of both ratified edges (`§8.8`, Q3, Q6)

**[P] Uniform semantics; different concrete bounds.**

| Edge | Governed party's discretion | Bound imposed | Evidence |
|---|---|---|---|
| `Capability governs Agent Definition` | Platform Division creates/deprecates Definitions | version bound to the implemented Capability contract version | **E-2 — explicit** |
| `Organization governs Platform Division` | the Division is *"**semi-autonomous**"* (E-5) | the bounds within which that autonomy holds; the Organization is the *"ultimate accountable body"* (E-4) | **E-4 + E-5 — the word *semi-autonomous* presupposes a bounding party, but the concrete bounds are not enumerated** |

**Q3 — direction:** `A governs B` means **A holds constraining authority and
ultimate accountability over B's governed acts**; it does **not** mean A possesses
B or performs B's acts.

**[O] One residual gap, stated rather than papered over.** For the Organization
edge, the *concrete* bounds are **not enumerated** in any resident source. The
semantics are defined; the specific constraints are not. This does not block
ratification of the *meaning*, and it does not block the Capability edge, whose
bound E-2 states exactly.

## 9. Construction impact (`§8.9`, Q8)

**What must be built — one thing, and it is already ratified:**

**[E] The Domain Model §6 version binding is unimplemented.**
`AgentDefinition.implemented_capabilities` is `Tuple[str, ...]` — **capability
keys only, carrying no Capability version** — while E-2 requires the Definition's
version be *"bound to the Capability **contract version** it implements."*

| Question | Answer |
|---|---|
| What must be built | the version binding on the Agent Definition side |
| What must **not** be built | any Capability-side reference to Agent Definitions; any `governs` object, registry or graph; the Organization edge's concrete bounds (§8) |
| Boundary involved | **`core/agent/` only** |
| Graph-level only? | **No** — it is a field-level constraint on an existing field |
| Domain object / reference needed? | **No** new object; the existing `implemented_capabilities` would carry a version alongside the key |
| Specification change needed? | **Yes** — `agent_spec` and `capability_spec` would record the binding |
| Conformance guard needed? | **Yes** — that a Definition names a *versioned* Capability contract |

**[E] `Organization governs Platform Division` yields no construction target**
under this definition — its bounds are unenumerated (§8), so there is nothing
determinate to build. It is an accountability relation, like the T-2 Skill half.

## 10. Unresolved questions (`§8.10`)

1. **[O]** The concrete bounds of `Organization governs Platform Division` are
   unenumerated. **Does not block** ratifying the verb's meaning.
2. **[O]** Multiplicity — may two entities govern one target? No source states it.
   **Does not block** either ratified edge, each having exactly one governor.

## 11. Recommended successor decision (`§8.11`, `§9`)

**CASE A — `governs` semantics are sufficiently defined for ratification.**

The successor is a **Ratification Gate** putting §4's definition, §5's
distinction, §6's dependency finding and §7's lifecycle finding to the
Architect. **No canonicalization, specification change or construction may
precede it** (`§10`).

**[A] If ratified, the pipeline reopens immediately**: the version binding in §9
is a ratified, bounded, single-boundary construction target — the first in some
time that requires no new semantic choice.

## 12. Verification that no construction occurred (`§8.12`, `§12`)

| Check | Result |
|---|---|
| Source / test files changed | **0** |
| Canonical artifacts changed | **0** — Domain Model, Freeze, Blueprint, Relationship Model, Constitution, Finding Register all **hash-identical** |
| Specifications changed | **0** |
| Governance registers mutated | **0** |
| Ratification performed | **none** — this package proposes |
| `native_core` · `tools` · `bounded_exception` | **584** · **20** · **29 OK**, unchanged |
| Entity count · core boundaries | **12** · **11** |
| External semantics imported (`§7`) | **none** — every element derives from E-1…E-10 |
