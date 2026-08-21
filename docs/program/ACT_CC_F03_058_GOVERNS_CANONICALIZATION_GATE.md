# `ACT-CC-F03-058` — `governs` CANONICALIZATION GATE

> **DRAFT — PREPARED BY THE CO-FOUNDER OFFICE · AWAITING FOUNDER ISSUANCE.**
> Produced under `ACT-CC-F03-057 §8.9`. **This document confers no authority on
> itself.** Until issued, `governs` semantics are ratified but **not
> canonicalized**, and construction remains unauthorized.

**Predecessor:** `ACT-CC-F03-057` · **Decision consumed:** `DEC-F03-057 = OPTION A — RATIFY`
**Type:** Canonicalization Gate · **Construction authority:** NONE
**Prepared:** 2026-08-21 · **Repository state:** `46f17c4`, tree clean

---

## §1 — What this gate is for

`DEC-F03-057` ratified the **meaning** of `governs`. Ratified semantics are not
yet canonical: they live in a decision record, not in the canonical architecture.

**This gate asks: where does the ratified definition land, and do the two
`governs` edges enter the frozen relationship table?**

## §2 — Where relationship terminology canonically belongs

**[E]** `docs/glossary/README.md` states the rule directly:

> *"Canonical terminology for AIOS is defined in two places: **The Canonical
> Domain Model — entities and relationships.** Engineering Constitution
> Appendix A — governance roles and artifacts."*

**A relationship verb therefore belongs in the Canonical Domain Model** — not the
glossary, not the Freeze, not a specification. That answers the *where* from
resident authority rather than preference.

**[A] Note the second clause.** `governs` names an authority relation, and
Constitution Appendix A holds *"governance roles and artifacts."* Whether any part
of this definition also belongs there is a question this gate should put to the
Architect, **not** assume. The Constitution is the most protected artifact in the
program.

## §3 — The canonicalization targets

| # | Target | Change | Notes |
|---|---|---|---|
| **G-1** | **Canonical Domain Model** | record the ratified definition of `governs` and the `owns` / `governs` distinction, where §4's two edges already sit | The natural home per `§2`. **Additive** — no edge added, none removed |
| **G-2** | **Architecture Freeze §6** — frozen *Observed* relationship table | **decide** whether the two `governs` edges enter it | **See `§4` — this is a real decision, not a formality** |
| **G-3** | **Constitution Appendix A** | **decide** whether a governance-authority term belongs there | **Architect only.** Default: **no change** |

## §4 — **[D] G-2 is a genuine decision, and the gate must not presume it**

Freeze §6's frozen table currently holds **ten** relationship rows: `owns` ×2,
`hosts`, `produces`, `coordinates`, `uses`, `derived-from`, `promoted-to`,
`depends-on`, and `realizes`. **Neither `governs` edge is among them**, though
both are ratified in Domain Model §4.

Two readings, and the evidence does not settle between them:

- **(a) Add both rows.** Freeze §6 holds *"the **Observed** canonical
  relationships … frozen"*, and both edges are stated in the ratified Domain
  Model — which is exactly what the Relationship Model's vocabulary calls
  **Observed**. On that reading their absence is an omission, and `DEC-F03-046`
  set the precedent by adding `Workflow realizes Capability`.
- **(b) Add neither.** The Freeze table's columns are *Allowed direction*,
  *Forbidden direction*, *Ownership*, *Lifecycle implication*. Under
  `DEC-F03-057` interpretations **3** and **4**, `governs` confers no lifecycle
  authority and creates no dependency — so three of four columns would read
  *"none"* or *"unchanged"*, and the row would assert little. Interpretation **5**
  also leaves the Organization edge's concrete bounds undefined, so its
  *Forbidden direction* cannot be stated without inventing one.

**[A] Reading (b) has the stronger evidential footing** — a frozen row that
cannot state its own forbidden direction without invention would breach
interpretation 6 (*no additional semantics may be inferred*). **But this is the
Architect's call, and the gate presents both rather than deciding.**

## §5 — Hard boundaries for the executing Act

**May:** record the ratified definition at G-1; act on G-2 and G-3 **only** as
this gate's decision block directs; preserve all prior text additively.

**Must not:** add, remove or alter **any** relationship edge in Domain Model §4 ·
create `CapabilityRef` or any Capability import in `core/agent/` · state concrete
bounds for `Organization governs Platform Division` · touch specifications,
source or tests · perform construction · infer semantics beyond the six ratified
interpretations.

**Entity count must remain 12; core boundaries 11.**

## §6 — Founder / Architect decision block

```text
DEC-F03-058 — governs Canonicalization

G-1  Record the ratified definition in the Canonical Domain Model
     [ ] AUTHORIZE      [ ] DEFER

G-2  Add the two governs edges to the Architecture Freeze §6 frozen table
     [ ] ADD BOTH       [ ] ADD NEITHER      [ ] DEFER

G-3  Record a governance-authority term in Constitution Appendix A
     [ ] AUTHORIZE      [ ] NO CHANGE (default)

Founder / Architect: ____________________
Date: ____________________
Confirmation: ____________________
```

Each line requires an explicit mark. **No default may be inferred**, G-3's
stated default included — it must still be marked.

## §7 — Successor sequence, not collapsible (`ACT-CC-F03-057 §9`)

```text
Canonicalization → Specification Synchronization Gate → Specification
Synchronization → Construction Gate → Construction → Verification
```

**The construction target waiting at the end is already identified and needs no
new semantic choice:** `AgentDefinition.implemented_capabilities` is
`Tuple[str, ...]` — capability keys carrying **no version** — while Domain Model
§6 requires an Agent Definition's version be *"bound to the Capability contract
version it implements."* Single boundary, `core/agent/` only. It is **not**
authorized by this gate.

## §8 — Out of scope

T-12 · OB-01 · PD-02 activation · `DEC-AE04` · `DEC-REVOCATION` ·
`DEC-ADOPTION` · `RG-2` · `RG-3` · the `GDR-0025`/`-0026` count correction · the
concrete bounds of `Organization governs Platform Division`.
