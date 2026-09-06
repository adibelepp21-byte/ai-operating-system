# Platform Division Ownership Model

> **Status: DERIVED from frozen source.** Constructed 2026-09-06, Cycle 20,
> under `ACT-CC-P10-FINAL §16` (Ownership dimension), `§17`, `§19` and `§21`, on
> `FDE-P10-AUTONOMOUS-EXECUTION-01` Decision B and `DEL-T4.4-CF-001 §3.1 A/C`.
>
> **Every statement here is quoted or directly derived from
> `AIOS_ARCHITECTURE_FREEZE_v1.0.md §2`–`§6`.** Nothing is invented, and no
> division is assigned anything.

## 0. What this answers, and what it cannot

`ACT-CC-P10-FINAL §16` names **Ownership** among the construction dimensions.
Ten cycles have recorded Ownership as *evidenced for 3 divisions, partial for 3,
absent for 2* — because the corpus looked for **per-division** ownership
statements, which are supply-blocked at `G-01` and `ESC-C7-01`.

**The general question was answerable all along.** `Freeze §4` ratifies twelve
entities, each with an explicit *Ownership* clause. Together these state
precisely **what any Platform Division owns, what it does not, and what is owned
by no one** — for every division, without naming any.

**This is the Ownership dimension at model level.** It does not tell us which
Capabilities `PD-05` owns; it tells us what it would mean for `PD-05` to own
one, and what `PD-05` may never own.

**Terminology.** `Freeze §4` uses `Department`. Under `ADR-0010` that is the
**recorded historical alias** of `Platform Division` for the same entity
(`E-64`). The frozen text is quoted **verbatim and unaltered** — `ADR-0010` is a
bounded amendment and *"nothing else in the repository may change under this
ADR."*

---

## 1. What a Platform Division owns

**[A] `Freeze §4`, Spine.** *Department — "accountability unit. **Responsibility**:
owns Capabilities and Agent Definitions. **Ownership**: owned by Organization;
owns Capabilities/Agent Definitions."*

| Owned | Cardinality | Source |
|---|---|---|
| **Capability** | *"exactly one Department"* per Capability | `INV-1` |
| **Agent Definition** | *"exactly one Department"* per Definition | `INV-2` |

**Exactly two entity types.** Both are owned exclusively — no shared ownership,
no unowned instance of either.

### Two further relations that are not ownership

| Entity | Relation to the Division | Frozen wording |
|---|---|---|
| **Agent Instance** | **not owned** | *"not owned — transient, **accountable to the Department owning its Definition**"* |
| **Memory** | **scoped**, not owned outright | *"scoped by the producing Agent Instance/Department"* |
| **Knowledge** | **home**, not owned outright | *"collectively by the Organization, **each item with a home Department**"* |

**`Accountability ≠ ownership`, and `home ≠ ownership`.** Knowledge is owned
*collectively by the Organization*; a Division holds only the *home* of an item.
A Division is *accountable for* Instances of its Definitions without owning them,
because an Instance is transient and *"the only actor."*

## 2. What no Platform Division owns

**[A] `Freeze §4`, Execution + Cross-cutting.** Five entities are owned
**centrally** — that is, not by any Division:

| Entity | Frozen ownership clause |
|---|---|
| **Skill** | *"owned centrally"* |
| **Workflow** | *"owned centrally"* |
| **Tool** | *"owned centrally"* |
| **Runtime** | *"owned centrally"* |
| **Organization** | the hierarchy root — *"owns Departments"* |

And one is owned by **no one at all**:

> **Trace** — *"**owned by no one** — governed only by retention policy."*

**Consequence [D]:** a Platform Division corpus that claimed ownership of the
Skill, Workflow, Tool, Runtime or Trace **entity** would contradict frozen canon.

### The one case that needs stating precisely

**Checked, not assumed.** A sweep of `divisions/` for ownership claims over
these five entities returns one recurring hit, and it is a real terminology
collision rather than a violation.

`PD-05-runtime-and-execution.md:22` quotes the **frozen** `PD-02` corpus:

> `PD-02 B7:212` — ***"PD-05 owns Runtime."***

**Two frozen sources use "owns Runtime" in two different senses.**
`Freeze §4` says the **Runtime entity** is *"owned centrally"* and is *"a
facility, not an actor."* `PD-02 B7:212` says the **Runtime domain** is PD-05's
organizational accountability.

**The corpus already drew this distinction, before this artifact existed.**
`PD-05`'s own record reads: *"an **organizational division** that owns the
Runtime **domain**"*, and carries the separation explicitly —

```text
owns the Runtime DOMAIN        implements runtime BEHAVIOUR
```

**That reconciliation is correct and is confirmed here from `Freeze §4`.**
`Domain accountability ≠ entity ownership`. A Division may be accountable for
the Runtime domain while the Runtime entity is owned centrally; the two
statements do not compete.

**Recorded as a latent collision [U].** A future reader who takes *"PD-05 owns
Runtime"* as **entity** ownership would contradict frozen canon. `PD-05`'s
record already guards against this; **no other division record makes an
ownership claim over any of the five centrally-owned entities.**

`PD-05` also already flags the adjacent open question: whether the *"Runtime
owner"* role at `A5:327` and `B7:212`'s ownership statement refer to the same
thing is *"strongly suggested and not stated — and suggestion is not
evidence."*

## 3. The complete ownership map

```text
Organization ──owns──▶ Platform Division ──owns──▶ Capability      (INV-1, exactly one)
                              │            └─owns──▶ Agent Definition (INV-2, exactly one)
                              │
                              ├─accountable-for──▶ Agent Instance   (not owned, transient)
                              ├─scopes───────────▶ Memory           (with the producing Instance)
                              └─is-home-of───────▶ Knowledge item   (Organization owns collectively)

owned centrally, by no Division:  Skill · Workflow · Tool · Runtime
owned by no one:                  Trace
```

**Direction, frozen (`Freeze §6`):** *"authority ↓, execution ↓,
information/knowledge ↑ through the single governed promotion gate (INV-8),
Trace immutable (INV-5)."*

## 4. What a Division is forbidden

**[C] `Freeze §4`, Department entity, verbatim:**

> *Forbidden* [E]: **owning another Department's Capability (INV-1)**; **silent
> cross-Department dependency (INV-10)**.

Two prohibitions, and both bear directly on open items in this corpus:

- **`INV-1`** bars a Division from owning another's Capability. Combined with
  `G-09` — two canonical sources enumerating six vs ten Divisions — **`INV-1`
  cannot currently be evaluated at all**, because "another Department" does not
  identify a member of a determinate set.
- **`INV-10`** bars *silent* cross-Division dependency. `G-05` records five
  derived inter-PD edges. `Freeze §2` places **Inferred relationships explicitly
  outside the freeze**, marked **`[O]` — Architect-reserved**, *"not frozen"*.

## 5. Constraints the Organization itself carries

**[A]** *Organization — "hierarchy root … accountability root. **Forbidden**
[A]: acting as an executor; mutating Trace."*

**The accountability root may not execute.** Only an Agent Instance acts —
*"the only actor"* — and every action produces *"exactly one Trace"*
unconditionally (`INV-4`).

**Consequence [D] for `PD-01 Executive Office`:** whatever an Executive Office
is, it cannot be the Organization acting, because the Organization is forbidden
to act as an executor. **Not resolved here** — `PD-01` is an integration record,
and `G-09` leaves the Executive Office name shared between two populations.
**Recorded as a constraint any future `PD-01` construction must satisfy.**

## 6. Two of PD-03's own domain terms are reserved non-entities

**[A] `Freeze §2`, Explicitly OUTSIDE the freeze:**

> **Reserved concepts with no ratified entity** — *Identity, Context,
> State-as-entity, Resource, Artifact, Task, Goal, Event, Checkpoint,
> **Permission**, **Policy*** (Vocabulary Freeze §3.3).

`E-56` records PD-03's canonical domain as *"Policy · Standards · Approval ·
Control · Certification · Compliance."*

**`Policy` is a PD-03 domain concern and simultaneously a reserved concept with
no ratified entity.** So is `Permission`.

**This is not a contradiction, and must not be reported as one.** A Division may
*govern a domain* without that domain being an entity in the Domain Model. PD-03
governs policy as subject matter; there is no `Policy` **entity** to own,
instantiate, or relate. The distinction is exactly `E-56`'s own principle:
*"Governance responsibility is distinct from execution ownership."*

**The operative constraint [C]:** **no `Policy` or `Permission` entity may be
constructed for PD-03 or any Division.** Both are Architect-reserved
(`Vocabulary Freeze §3.3`). A future PD-03 volume that introduced a `Policy`
entity would create an unratified thirteenth entity — `Freeze §4` states **"No
new entity."**

## 7. The one open cardinality question

**`INV-15` — "Minimal cardinality"**, rationale *"Over-specifying relationships
ahead of need"*, risk *"Premature rigidity."* `Freeze §4` applies it to Agent
Definition: *"may declare 0+ Skills and 0+ Workflows (INV-15)."*

**No frozen source states how many Capabilities a Division must own.** `INV-14`
bars a Capability from *"existing with zero implementers as a steady state"*,
but nothing bars a **Division** from owning zero Capabilities.

**[U] Unresolved, and deliberately not decided:** whether a Platform Division
owning zero Capabilities is a valid steady state. `INV-15` counsels against
specifying ahead of need, so **this corpus specifies nothing.** Recorded because
it will matter the moment `G-09` is decided and Capability assignment begins.

## 8. What this constructs, and what it does not

**Constructs:** the Ownership dimension of `ACT-CC-P10-FINAL §16` at **model
level**, applicable to all ten Platform Divisions, entirely from frozen source.

**Does not construct:** any per-division ownership assignment. Not one
Capability, Agent Definition, Knowledge home, or Memory scope is assigned to any
Division. Those are `G-01`/`ESC-C7-01` (supply) and `G-09` (which population),
and `Freeze §8` wall 5 puts Domain-Model change under the governance process,
*"not delegable."*

**The dimension is now answered as far as authority and evidence allow.** What
remains is not analysis — it is a decision and a supply, neither of which is
mine.
