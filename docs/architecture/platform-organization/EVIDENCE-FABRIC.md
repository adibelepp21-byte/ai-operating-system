# Evidence Fabric — link integrity

> **Required by:** `ACT-CC-AIOS-FULL-SYSTEM-RESOLUTION-AND-AUTONOMOUS-CONTINUATION-GATE-v1.0 §25`;
> candidate v2.0 `§28`. **Built 2026-09-09.**
>
> `ACT §25` names an eleven-node chain and calls it *"the connective fabric."*
> **This artifact tests each adjacent link against frozen resident evidence and
> records which ones actually exist.** It does not assert a link that no source
> establishes.

---

## 0. Method

For each adjacent pair in the `§25` chain, the question is narrow and checkable:

> **Does a resident, frozen or ratified source establish a relation between
> these two, in a form that can be cited?**

**Mention counts are not evidence.** An early draft of this artifact ranked the
links by how many documents mention each node — a measure under which every link
looked strong, including the ones with no relation at all. That method was
discarded before it reached the page; what follows cites `Freeze §4`/`§5`/`§6`
relation rows and entity definitions, or records `UNKNOWN`.

## 1. Link table

| # | Link | Establishing source | Strength |
|---|---|---|---|
| 1 | **Constitution ↕ Architecture** | `Constitution §4` — five-artifact hierarchy, *"Authority flows downward"*; `Freeze §1` — after the freeze *"architectural change requires formal governance"* | **ESTABLISHED** |
| 2 | **Architecture ↕ Governance** | `Freeze §8` Frozen Governance Boundaries *"cannot be bypassed by any implementation"*; `Constitution §6.2` inv. 2 | **ESTABLISHED** |
| 3 | **Governance ↕ Runtime** | `Freeze §5` layer 1 Governance *"may not be automated"*; layer 2 Runtime *"may not own Knowledge; may not be an independent traced actor"*; `Freeze §4` Runtime — *"a facility, not an actor"* | **ESTABLISHED** |
| 4 | **Runtime ↕ Intelligence** | — | **UNKNOWN — see `§2`** |
| 5 | **Intelligence ↕ Knowledge** | — | **UNKNOWN — see `§2`** |
| 6 | **Knowledge ↕ Memory** | `Freeze §6` — *"Memory promoted-to Knowledge: Memory→(governed review)→Knowledge (`INV-8`); **forbidden**: Memory→Knowledge automatic"* | **ESTABLISHED — strongest link in the chain** |
| 7 | **Memory ↕ Tools** | — | **UNKNOWN** — no frozen relation pairs them |
| 8 | **Tools ↕ Workflow** | Indirect only: `Freeze §6` *"Agent Instance uses Tool (`INV-12`)"* and *"Workflow coordinates Instances (`INV-13`)"*. **The pair meets through Agent Instance, not directly** | **INDIRECT** |
| 9 | **Workflow ↕ Department** | `Freeze §6` *"Workflow realizes Capability"*; `Freeze §4` Capability owned by *"exactly one Department (`INV-1`)"* | **INDIRECT — and blocked by `G-09`** |
| 10 | **Department ↕ Organization** | `Freeze §6` *"Organization owns Department — down; Ownership: Org→Dept; governed"* | **ESTABLISHED** |

**Four established · two indirect · four unknown.**

## 2. The finding — `Intelligence` is not in the frozen architecture at all

**Measured:** the string `Intelligence` occurs **0 times** in `Freeze §4`
(Frozen Entity Definitions) and **0 times** in `Freeze §5` (Frozen Layer Model).

**It is neither a frozen entity nor a frozen layer.** The nearest frozen concept
is `Optimization` — `Freeze §5` layer 10, *"governed learning loop"*, output
*"proposals only"*, forbidden from *"deciding governance (PR-3)"* and
*"auto-promote (`INV-8`)"* — and `Freeze §2` places **Model-optimization**
explicitly **OUTSIDE the freeze**, `§10` Architect-reserved.

**So links 4 and 5 are unknown for a structural reason, not for want of
searching:** the chain names a node the frozen architecture does not define.
`P5 Intelligence Ecosystem` is a **Phase**, and a Phase is not an entity.

```text
PHASE NAME  ≠  FROZEN ENTITY  ≠  FROZEN LAYER
```

**This is recorded, not repaired.** Introducing `Intelligence` as an entity
would be a Canonical Domain Model amendment — `Constitution §6.2` invariant 3,
reserved, and `Freeze §4` states *"No new entity."*

## 3. Where the fabric is weakest, and what that predicts

```text
Constitution ── Architecture ── Governance ── Runtime ──╳── Intelligence ──╳── Knowledge
                                                                                 │
Organization ── Department ~~ Workflow ~~ Tools ──╳── Memory ────────────────────┘
   strong         G-09        indirect            unknown        strong
```

**Both ends of the chain are frozen and citable. The middle — Runtime through
Memory by way of Intelligence and Tools — is where four of the ten links have no
establishing source.** That region is exactly `P5`–`P8`. *Corrected 2026-09-10:* those Phases are
**CERTIFIED / COMPLETE** by `FD-P5-001`, `FD-P6-002`, `FD-P7-003` and
`FD-P8-002`. **The earlier claim that their maturity was equally unestablished
was false.** The fabric finding survives and sharpens: the region with the least
**frozen architecture** is **certified complete at the Phase level** — so phase
certification and frozen-architecture coverage are **independent**, and this is
the clearest evidence in the corpus that they are.

> **Corrected 2026-09-10.** This paragraph previously read: *"The fabric
> measurement and the Phase-state measurement agree … the part of AIOS with the
> least frozen architecture is the part whose Phase state is least evidenced."*
> **The second half was false** — `P5`–`P8` are certified complete. The
> measurements do not agree; they **diverge**, and the divergence is the more
> useful result: **the region with the least frozen architecture is the region
> most completely certified at the Phase level.** Phase certification and
> frozen-architecture coverage are independent axes, and treating one as
> evidence about the other is what produced the original error.

## 4. What this artifact does not claim

It does not assert that an `UNKNOWN` link is absent from the system — only that
**no resident source establishes it**. It does not treat `INDIRECT` as
`ESTABLISHED`. It does not propose `Intelligence` as an entity. And it does not
convert the `Workflow ↕ Department` link to established, because `G-09` leaves
the owning population undetermined and `ADR-0029` reserves that question.
