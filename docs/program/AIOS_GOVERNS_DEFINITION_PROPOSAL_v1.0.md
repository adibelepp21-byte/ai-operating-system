# `governs` — Architectural Definition Investigation & Proposal

**Prepared under:** FOUNDER · `ACT-CC-F03-055` `DEC-F03-055 = OPTION A` · `§8`–`§10`
**Result:** **RESIDENT CANONICAL AUTHORITY IS INSUFFICIENT** — escalated at the exact semantic decision (`§10`)

> **PROPOSED — NOT RATIFIED.** `§10`: *"Claude Code may propose a definition of
> `governs`, but may NOT silently ratify it."* Nothing here is adopted, and no
> artifact was changed by this document.

---

## 1. What the edges are

Canonical Domain Model §4 carries two:

```text
Organization  —governs→  Platform Division
Capability    —governs→  Agent Definition
```

## 2. Evidence sweep — where `governs` is, and is not

| Source | Result |
|---|---|
| **Domain Model §4** | **present** — the only place either edge appears |
| **Domain Model §2** (entity definitions) | **absent** — neither the Organization nor the Capability definition mentions governing |
| **Architecture Freeze §4** (entity entries) | **absent** from every *Allowed* / *Responsibility* list |
| **Architecture Freeze §6** (frozen *Observed* relationship table) | **absent** — parsed the Relationship column across all rows: **zero** `governs` rows |
| **Canonical Relationship Model §5** (the matrix) | **absent** — parsed the Relationship column: **zero** `governs` edges, neither Observed, Inferred, nor Architect Reserved |
| **Blueprint** | **absent** from every package's responsibilities and dependencies |
| **`native_core`** | **unmodelled** — the two textual hits are prose inside comments (`definition.py:215`, `composition.py:8`), not modelling |

**[E] The decisive fact.** The Canonical Relationship Model §5 states of itself:
*"Only evidence-supported relationships, using only sanctioned verbs"*, *"No
unsupported relationship appears"*, and *"Verbs used are all from the sanctioned
set; none invented."* It maps **eighteen** edges. **`governs` is not among them.**

So `governs` appears in the ratified Domain Model but was **never carried into
the frozen relationship table, and never mapped by the synthesis that catalogued
every evidence-supported relationship.** It is a ratified edge with no ratified
meaning.

## 3. `§9` — OWNS vs GOVERNS

Every cell is **Canonical**, **Inferred**, or **Unknown**. **No value is invented
to complete the table.**

| Property | OWNS | GOVERNS |
|---|---|---|
| Resource/domain ownership | **Canonical** — Domain Model §5 *Ownership Rules* assigns an owner to every entity | **Unknown** |
| Authority | **Inferred** — `[A]`; Domain Model §5 is titled *Ownership*, and no clause equates owning with authority | **Unknown** |
| Accountability | **Canonical** — Organization is the *"ultimate accountable body"*; a Platform Division is *"a bounded, semi-autonomous unit of **accountability**"* (DM §2) | **Unknown** |
| Policy control | **Unknown** | **Unknown** |
| Lifecycle authority | **Canonical, and it does *not* rest with the owner** — DM §6: Platform Division and Capability are *"created/retired via architectural decision, **architect approval**"* | **Unknown** |
| Decision authority | **Unknown** | **Unknown** |
| Oversight | **Unknown** | **Unknown** |
| Exclusive relationship | **Canonical** — *"exactly one"* (INV-1; INV-2 clause 1; DM §5) | **Unknown** |
| Multiple governors | **Canonical — excluded** for owning (*exactly one*) | **Unknown** |
| Transfer semantics | **Unknown** | **Unknown** |

**Ten of ten `GOVERNS` cells are Unknown.** One `OWNS` row is worth flagging on
its own: **lifecycle authority does not follow ownership** — DM §6 places it with
*architect approval*, not with the owner. Any future definition of `governs` that
assumes owning implies lifecycle control would contradict that.

## 4. `§8`'s ten questions — answered from evidence only

1. **What does `governs` mean?** **Unknown.** No canonical source defines it.
2. **How does it differ from `owns`?** **Unknown.** `Organization governs Platform Division` sits directly beside `Organization owns Platform Division` in the same list, with nothing distinguishing them. That adjacency is the strongest available hint that they are *meant* to differ — but a hint is not a definition.
3. **Does it confer authority?** **Unknown.**
4. **Lifecycle control?** **Unknown** — and note §3: lifecycle authority does not follow *ownership*, so it cannot be inherited by analogy.
5. **Policy/control authority?** **Unknown.**
6. **Can an entity govern what it does not own?** **Unknown** — though `Capability governs Agent Definition` is suggestive: a Capability owns no Agent Definition (a **Platform Division** does, INV-2 cl.1), so this edge *would* be governance without ownership. **Suggestive, not decisive.**
7. **Can multiple entities govern one target?** **Unknown.**
8. **Decision authority, oversight authority, or both?** **Unknown.**
9. **Does it affect dependency direction?** **Partly answerable.** `Capability governs Agent Definition` runs **Capability → Agent Definition**, a direction Blueprint §7's `[E]` allowed-dependency list for the Capability package **excludes** (*"its Department; other Capabilities"*). So either the edge is not a package dependency, or Blueprint §7 would need amending. **This is a real, concrete consequence.**
10. **What implementation representation?** **Undeterminable** until 1–8 are answered.

## 5. `§10` — GOVERNS DEFINITION PROPOSAL

**Term:** `governs`
**Subject / Object:** `Organization → Platform Division`; `Capability → Agent Definition`
**Semantic meaning:** **[O] CANNOT BE PROPOSED FROM RESIDENT EVIDENCE.**
**Difference from `owns`:** **[O] Unknown** — see §3.
**Authority implications:** **[O] Unknown.**
**Lifecycle implications:** **[O] Unknown** — and not inheritable from `owns` (§3).
**Multiplicity:** **[O] Unknown.**
**Dependency implications:** **[A]** For `Capability governs Agent Definition`, the direction contradicts Blueprint §7's `[E]` list unless the edge is non-dependency-bearing (§4.9).
**Canonical evidence:** Domain Model §4 — the edges exist. **That is the whole of it.**

**Open architectural question — the exact point requiring Architect authority:**

> **What does `governs` denote, such that it is distinct from `owns`; and does
> `Capability governs Agent Definition` confer a dependency, or only an
> accountability relation that creates no package edge?**

**[E] I am stopping precisely here and nowhere earlier.** Every question that
resident evidence *can* answer has been answered above; only the semantic core
is escalated. Proposing a meaning would be inventing architecture, which `§19.1`
forbids.

## 6. `§10` closing instruction observed

> *"Do not block unrelated construction merely because `governs` is unresolved."*

Honoured. `governs` is **not** treated as a general blocker. But it is the
**only** thing standing between the program and its next construction target —
see the closure report `§8`: all **26** ratified Domain Model edges were checked,
and the two `governs` edges are the **only** ones with no modelling. Their being
blocked is therefore not incidental; it is the frontier.
