# T-2 — Capability ↔ Skill/Workflow · Architecture Decision Package

**Prepared under:** FOUNDER · `ACT-CC-F03-044` `DEC-F03-044 = OPTION A` · Moriarty · 21-08-2026
**Delivered as:** the `ACT-CC-F03-045` decision-track output (`§19`)
**Result:** **STATE A — RATIFICATION-READY** (`§12`)

> **PROPOSED — NOT CANONICAL.** `ACT-CC-F03-044 §8` [E]: T-2 *"does not become
> `[E]` Canonical merely because Option A is selected."* Nothing here ratifies a
> relationship, alters T-2's `[O]` status, or authorizes construction (`§13`).
> Every proposal below is marked **[P]** and requires Architect ratification.

---

## 1. Decision consumed

```text
DEC-F03-044 = OPTION A — AUTHORIZE T-2 ARCHITECTURAL DECISION TRACK
Founder: Moriarty · Date: 21-08-2026 · Signature / Confirmation: Moriarty
```

`§18` validity: one option selected · attribution · date · confirmation. **VALID.**
**[O]** The `§17` duplicate block remains unchecked and undated; `§21` carries the
filled decision. Recorded, not corrected.

## 2. Evidence sweep (`§11`) — read from source, not from prior reports

| # | Source | Statement bearing on T-2 |
|---|---|---|
| 1 | **Canonical Domain Model §4** — the ratified relationship list, 24 entries | Contains **`Agent Definition implements Capability`** and **`Agent Definition specifies Skill, Workflow`** *(what it is permitted/required to use)*. Contains **no** `Capability → Skill` and **no** `Capability → Workflow` relationship. |
| 2 | **Freeze §4 — Capability** | **[E]** *Allowed*: *"be implemented by Agent Definitions; depend on Capabilities via governed, versioned contracts."* Skill and Workflow are **not** among them. |
| 3 | **Freeze §4 — Skill** | **[E]** *Allowed*: *"be used by an Instance; **be declared by Definitions**."* Capability is **not** among them. |
| 4 | **Freeze §4 — Workflow** | **[E]** *Allowed*: *"coordinate Instances; compose Skills."* Capability is **not** among them. |
| 5 | **Blueprint §7 — Capability package** | **[E]** *Allowed dependencies*: *"its Department; other Capabilities via governed versioned contracts."* Skill and Workflow are **excluded**. |
| 6 | **Blueprint — Agent package** | **[A]** *Allowed dependencies*: *"runtime, **capability, skill, workflow**, tool, knowledge, memory."* Agent is the one package permitted to see all three. |
| 7 | **Freeze INV-15** | **[E]** *"An Agent Definition may specify zero or more Skills and zero or more Workflows … No minimum cardinality is required."* |
| 8 | **Freeze INV-2** | **[E]** *"…and implements at least one Capability."* |
| 9 | **Freeze §10** | **[O]** *"Inferred relationships — Capability↔Skill/Workflow…"*; *"**not frozen**"*; *"named as a boundary, **not defined**; each awaits an **Architect decision before it enters any freeze**."* |
| 10 | `capability_spec §12`, `§14` | **[O]** *"Capability↔Skill/Workflow composition is currently Inferred (reserved)"*; *"relationship ratification"* |
| 11 | `skill_spec §14` | **[O]** *"Skill↔Capability/Workflow composition ratification (Inferred)."* |
| 12 | `workflow_spec §7` | **[E]** *"Executed by Runtime; composes Skills; **realizes Capabilities (Inferred, reserved)**."* — the only resident source proposing a **verb and direction** |
| 13 | `workflow_spec §14` | **[O]** *"Workflow↔Capability/Skill and Runtime↔Workflow relationships (Inferred)."* |
| 14 | `NCIR §9.6` | **[O]** *Reserved*: *"Capability↔Skill/Workflow (Inferred)."* |
| 15 | ADR / GDR | No ADR or GDR ratifies, defines, or constrains this relationship. |

## 3. `§9` determinations

**§9.1 — What resident sources say.** Fifteen sources. Five of them (rows 1–5)
are *ratified* and each **excludes** a direct Capability↔Skill/Workflow edge from
the entity's allowed relations. Six (rows 9–14) mark the edge **[O] Inferred /
reserved**. One (row 12) supplies a candidate verb — *"realizes"* — but tags it
Inferred.

**§9.2 — What portion is already explicitly defined.** **[E] The connection
between Capability and Skill/Workflow already exists as a two-hop path built
entirely from ratified edges:**

```text
Capability  ←implements—  Agent Definition  —specifies→  Skill, Workflow
   (INV-2 clause 2, DM §4)              (INV-15, DM §4)
```

Both legs are ratified in the Domain Model's relationship list and in Freeze
invariants. Blueprint places the Agent package as the only one permitted to
depend on capability, skill and workflow together (row 6) — the architecture
already designates Agent Definition as the meeting point.

**§9.3 — What remains genuinely undefined.** Only the **direct** edge: whether
Capability and Skill/Workflow stand in a relationship *not mediated by an Agent
Definition*, and if so its verb, direction, cardinality, ownership, lifecycle and
validation. Freeze §10 states these are *"named as a boundary, not defined."*

**§9.4 — What ratification would require.** Depends entirely on the alternative
chosen — see §4. ALT-1 requires none; ALT-2 requires the most.

**§9.5 — Can T-2 be ratified without changing frozen entities?** **[A] Yes, under
ALT-1 or ALT-4 — no.** Under ALT-2 or ALT-3, Domain Model §4's relationship list
would gain an entry, which is a change to a frozen artifact and is
Architect/Founder-reserved.

**§9.6 — Viable alternatives.** Four, enumerated in §4.

**§9.7 — Smallest ratification.** **[P]** ALT-1 — see §4.1.

**§9.8 — Downstream construction depending on T-2.** **[A] Very little, and less
than expected.** Skill and Workflow are already implemented subsystems among the
eleven boundaries. INV-15 realization (below) is **independently ratified** and
does **not** depend on T-2. No resident construction target was found that is
blocked by T-2 specifically.

## 4. Alternatives (`§12` STATE A)

### 4.1 ALT-1 — **[P]** The relationship is *derived*, not declared

**Definition proposed:** *A Capability stands in relation to a Skill or Workflow
only through an Agent Definition that implements the Capability and specifies the
Skill or Workflow. No direct edge exists; the association is computed from the
two ratified edges.*

- **Invariant impact:** none. INV-2, INV-13, INV-15 unchanged.
- **Specification impact:** `capability_spec §12`/`§14`, `skill_spec §14`,
  `workflow_spec §14` would move from **[O] Inferred** to **[E] derived**;
  `workflow_spec §7`'s *"realizes Capabilities"* would be restated as derived.
- **Implementation consequences:** none required. A query could later compose the
  two edges without any new dependency, since the Agent package already may see
  all three (row 6).
- **Frozen-artifact change:** **none** — Domain Model §4 gains no entry; it is
  read as already complete.
- **Why it fits the evidence:** rows 1–5 exclude the direct edge on **five**
  ratified sources. Domain Model §4 enumerates relationships as fine-grained as
  *"Skill invokes Tool"*, so its omission of a Capability↔Skill edge reads as
  deliberate rather than as an oversight.

### 4.2 ALT-2 — **[P]** Direct declared edge `Capability composes Skill/Workflow`

- **Requires:** a new Domain Model §4 relationship; an addition to Blueprint §7's
  Capability *allowed dependencies*, which today **exclude** skill and workflow;
  probably a new invariant for cardinality and governance.
- **Tension to disclose:** Domain Model §2 defines Capability as *"a stable,
  named, outcome-oriented contract — **what** can be delivered, **independent of
  how**."* A Skill is *"a discrete, reusable, bounded unit of **executable
  ability**"*. A direct edge places the *what* in contact with the *how*.
- **Cost:** highest. Changes two frozen artifacts.

### 4.3 ALT-3 — **[P]** Workflow-side edge `Workflow realizes Capability`

- **Requires:** a new Domain Model §4 relationship. **Does not** require changing
  Blueprint §7's Capability package, since the direction is Workflow → Capability.
- **Support:** `workflow_spec §7` already carries this exact phrasing, which makes
  it the only alternative with a resident textual precedent.
- **Gap:** says nothing about Skill, so `skill_spec §14` would remain reserved —
  T-2 would be only half closed.

### 4.4 ALT-4 — **[P]** Record as *Not Applicable*

Ratify that no relationship exists, direct or derived. **Rejected as a
recommendation** — it contradicts `workflow_spec §7`'s *"realizes Capabilities"*
and would leave the two-hop path undescribed, but it is listed because the
Architect may prefer an explicit negative.

### 4.5 Rejected alternatives

- **Inventing cardinality, ownership or lifecycle semantics** for the edge — `§6`
  forbids assuming any of them, and no resident source supplies them.
- **Implementing first and ratifying after** — `§5` and `§10` forbid converting
  `[O]` into `[E]` by implementation.
- **Importing an external composition model** — `§14`; resident evidence was
  sufficient, so **no external research was used**.

## 5. Authority required for ratification (`§12`)

**[O] Architect.** Freeze §10 is explicit: each inferred relationship *"awaits an
**Architect decision** before it enters any freeze."* ALT-1 and ALT-4 need only
that. ALT-2 and ALT-3 additionally amend the Canonical Domain Model — and ALT-2
also Blueprint §7 — which is Founder/Architect-reserved beyond this package's
scope. **No recommendation among the four is offered as a decision, and none may
be read as one.**

## 6. Separate finding — **not T-2**, recorded not acted on

**[E] INV-15 is ratified and unimplemented.** Freeze INV-15 and Domain Model §4
both establish that an Agent Definition *specifies* zero or more Skills and
Workflows. `AgentDefinition` currently carries `agent_definition_key`,
`agent_definition_version`, `owning_department_key`, `implemented_capabilities` —
**no Skill or Workflow declaration**.

This is the same shape as INV-2 clause 2 before `ACT-CC-F03-040`: ratified
architecture, unbuilt. **It is not T-2** — T-2 is the *direct* edge; this is the
Agent-side edge, already ratified. It is **not** opened, proposed or built here;
`§10` bars creating Skill or Workflow implementation, and `§13` bars construction.
Recorded so it is not mistaken for part of T-2 and not lost.

## 7. Verification and state

No code, test, specification or governance artifact was modified. `capability_spec
§12`/`§14`, `skill_spec §14`, `workflow_spec §14` and Freeze §10 all remain
**[O]**, unnarrowed.

| Check | Result |
|---|---|
| `native_core` · `tools` · `bounded_exception` | **566 / 20 / 29 OK**, unchanged |
| Core boundary count | **11** |
| Protected canonical artifacts | hash-identical |
| Conformance tests modified | **0** (`§15` disclosure list empty) |
| Governance mutations | **0** |
| T-2 `[O]` status | **unchanged** |
| Construction performed | **none** (`§13`) |
| External research | **NOT USED** (`§14`) |
| `§16` governance items | untouched |
