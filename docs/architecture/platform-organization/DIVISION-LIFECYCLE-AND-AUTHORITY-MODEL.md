# Platform Division Lifecycle & Authority Model

> **Status: DERIVED from canonical and frozen source.** Constructed 2026-09-06,
> Cycle 21, under `ACT-CC-P10-FINAL §16` (Lifecycle, Authority), `§17`, `§19`,
> `§21`. Authority: `FDE-P10-AUTONOMOUS-EXECUTION-01` Decision B;
> `DEL-T4.4-CF-001 §3.1 A/C`.
>
> Companion to `DIVISION-OWNERSHIP-MODEL.md`. Same method, same limit:
> **model level for all ten divisions, assigning nothing to any one of them.**

## 0. Method, and why it was not tried sooner

`§34.8` recorded that the remaining `§16` dimensions had each been treated as
*per-division* — and therefore blocked at `G-01`/`ESC-C7-01` — when the general
question was answerable from resident canon. Cycle 20 proved that for
**Ownership**. This artifact applies the same method to **Lifecycle** and
**Authority**.

**Precedence.** `Engineering Constitution §4`: Constitution → **Canonical Domain
Model** → ADR Framework → Principle Documents → Glossary. The Domain Model is
therefore the governing source below, and `AIOS_ARCHITECTURE_FREEZE_v1.0.md`
records the ratified freeze of it. Where both speak, they agree; the Domain
Model is the more specific.

---

# Part A — Lifecycle

## 1. The division's own lifecycle is Architect-reserved

**[A] `canonical-domain-model-v1.md §6`, verbatim first row:**

> | **Platform Division, Capability** | *"Created/retired via **architectural
> decision, architect approval**. Capability deprecation requires a defined
> sunset path. A Capability with zero active Agent Definitions implementing it
> is an invalid steady state and must be flagged for governance review — it is
> not silently acceptable."* |

**A Platform Division is created and retired by architectural decision under
architect approval.** `Freeze §4` states the same at lower resolution —
Department *"Lifecycle: governed"* — and the Domain Model supplies the specific
gate.

**Consequence [C], and it is decisive for this corpus:** **no Platform Division
may be created, retired, renamed, split, merged or dissolved by this
delegation.** That is not a policy this corpus adopted — it is the Domain
Model's own lifecycle rule, reinforced by `DEL-T4.4-CF-001 §3.2` exclusion 9
and `Freeze §8` wall 5.

It also settles a question the corpus has carried: **`G-02`** (`PD-10` named
*Developer Enablement* in the frozen corpus, *Developer Experience* in the
registry) is a **naming question about an entity whose lifecycle is
architect-approved**. Renaming it is not available here on any reading.

## 2. What a division does control

**[A] `Domain Model §6`, row 2:**

> | **Agent Definition** | *"Versioned; created/deprecated at **Platform
> Division discretion** within Capability governance. Its version is bound to the
> Capability contract version it implements."* |

**This is the first affirmative discretion this corpus has located for a
Platform Division in canonical source.** A Division does not merely own Agent
Definitions (`INV-2`) — it **creates and deprecates** them at its own
discretion, bounded by Capability governance and by version binding.

| Entity | Who acts | Bound by |
|---|---|---|
| **Platform Division** | Architect | architectural decision |
| **Capability** | Architect | architectural decision; sunset path required for deprecation |
| **Agent Definition** | **the Platform Division** | Capability governance; version bound to the Capability contract version |

**The asymmetry is the substance of the model.** A Division has no authority
over its own existence or over the Capabilities it owns, and full discretion
over the Definitions that implement them.

## 3. The full lifecycle table

**[A] `Domain Model §6`, remaining rows, condensed without alteration of terms:**

| Entity | Lifecycle |
|---|---|
| Platform Division, Capability | architectural decision, architect approval |
| Agent Definition | versioned; Division discretion within Capability governance |
| Agent Instance | *"spawned, active, terminated — **no governance overhead per instance**"* |
| Skill / Tool | versioned independently; interface preserved; **behavioural drift documented at promotion time** |
| Runtime, Workflow | versioned independently; governed revisions; compatibility boundaries preserved |
| Knowledge | versioned; revised/superseded via review; *"not casually deleted — audit trail matters"* |
| Memory | explicit retention window — *"Promote or expire"* |
| Trace | *"Append-only. Never mutated. Retained per policy."* |

**One clause deserves separate note.** Skill/Tool: *"Because AI-implemented
Skills can drift behaviorally without an interface change, Skill/Tool version
changes that alter behavior materially should be documented at promotion time,
not just interface-checked."* **The Domain Model anticipates that an interface
check is insufficient evidence of unchanged behaviour** — the same reasoning
this corpus applies to its own verification (`a passing suite ≠ architectural
completeness`).

## 4. `INV-14` restated as a lifecycle obligation

`Domain Model §6` renders `INV-14` as procedure rather than as a bare rule: a
Capability with zero active implementers *"**must be flagged for governance
review** — it is not silently acceptable."*

**Not "invalid" — "must be flagged."** The remedy is a governance action, not an
automatic deletion. **No division record in this corpus enumerates owned
Capabilities**, so nothing is currently flaggable; the obligation attaches the
moment `G-09` is resolved and assignment begins.

---

# Part B — Authority

## 5. `governs` is not `owns`, and confers no lifecycle authority

**[C] `canonical-domain-model-v1.md §4 Relationships`, verbatim:**

> - *"**`governs` is distinct from `owns`.** They are separate relationship
>   types. Neither is an alias, a merger, or a specialization of the other."*
> - *"**`governs` does not imply ownership.** A governor may bound the discretion
>   of an entity it does not possess. `A governs B` must never be read as
>   `A owns B`."*
> - *"**`governs` does not by itself confer lifecycle authority.** Its presence
>   establishes no creation, retirement, deprecation, or unilateral mutation
>   authority. **Lifecycle authority is only what §6 already assigns.**"*

**This is the Authority dimension's governing rule, and it is stated in the
Domain Model in almost exactly the terms this corpus has been using.**
`Organization governs Platform Division` therefore establishes **no** authority
of the Organization to create, retire, deprecate or mutate a Division — that
authority sits where `§6` puts it: **architect approval**.

**It also generalizes a distinction the corpus derived independently.**
`E-79` recorded `domain accountability ≠ entity ownership` for `PD-05` and
Runtime. `Domain Model §4` states the parent form: **`governs ≠ owns`**, and
adds a third term — **neither implies lifecycle authority.**

```text
governs   ≠  owns   ≠  lifecycle authority
```

Three distinct things. Holding one implies neither of the others.

## 6. Authority direction, frozen

**[A]** `Freeze §5` layer 1, **Governance**: purpose *"authority, review,
promotion"*; dependencies **"— (top)"**; forbidden — *"may not depend on
execution **authority**; **may not be automated** (§6.2 inv 2)."*

`Freeze §6` direction summary: *"**authority ↓**, execution ↓,
information/knowledge ↑ through the single governed promotion gate (INV-8),
Trace immutable (INV-5)."*

**Authority flows downward only.** No Division acquires authority by executing,
by holding a capability, or by being depended upon. `Freeze §8` wall 3 states
the limit for automation: *"automation may request/recommend/detect; it may not
decide governance or override it."*

## 7. The authority a division actually holds

Assembled from the sources above. **This is the complete list, and it is short:**

| Holds | Source |
|---|---|
| Ownership of its Capabilities | `INV-1` |
| Ownership of its Agent Definitions | `INV-2` |
| **Creation and deprecation of Agent Definitions**, at its discretion | `Domain Model §6` |
| Accountability for Instances of its Definitions | `Freeze §4` |
| Scoping of Memory produced within it | `Freeze §4` |
| Home for Knowledge items | `Freeze §4` |

| Does **not** hold | Source |
|---|---|
| Authority over its own creation, retirement or naming | `Domain Model §6` |
| Authority over Capability creation or retirement | `Domain Model §6` |
| Any authority derived from `governs` | `Domain Model §4` |
| Ownership of Skill, Workflow, Tool, Runtime | `Freeze §4` — *"owned centrally"* |
| Anything over Trace | `Freeze §4` — *"owned by no one"* |
| Cross-division Capability dependency without approval | `INV-10` |
| Ownership of another division's Capability | `INV-1` |

## 8. How division-level work would be authorized, if it were

`AIOS_BASELINE_LIFECYCLE_v1.0.md` records the **six-stage baseline lifecycle**
by which Native Core work was authorized: **1 Implementation Authorization → 2
Implementation → 3 Automated Verification → 4 Architect Acceptance → 5 Commit &
Freeze → 6 Transport.**

**Cited for shape only.** That document *"records the baseline lifecycle as it
was operated across the Native Core program; it does not create, amend, or
delegate authority"*, and its scope is Native Core work units — **not** Platform
Divisions. **No claim is made that it governs division construction.**

What it does show is that **Stage 1 is authorization and Stage 4 is Architect
Acceptance** — construction is bracketed by two authority gates in the one
lifecycle this repository has actually operated. Any future division-construction
procedure that omitted both would be unlike anything the program has done.

## 9. What these two dimensions do not construct

No division created, retired, renamed, split or merged. No Capability created,
assigned or deprecated. No Agent Definition authored. No `G-02` rename applied.
No claim that the baseline lifecycle governs divisions. **`§16`'s Lifecycle and
Authority dimensions are answered at model level and assigned to no one** — the
same boundary as `DIVISION-OWNERSHIP-MODEL.md §8`.

**Remaining `§16` dimensions after this artifact:** Capability, Architecture,
Operation, Performance, Evolution. **Identity, Ownership, Authority, Lifecycle
and Integration are now answered at model level.**
