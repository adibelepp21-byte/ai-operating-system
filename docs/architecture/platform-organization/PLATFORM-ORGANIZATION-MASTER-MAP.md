# Platform Organization Master Map

> **Status: DERIVED.** `ACT-CC-P10-1 §26.1` required a Master Map reflecting the
> reconciled organizational structure. This is that map, built from resident
> evidence. **It is not the absent canonical "Platform Organization Master Map"**
> referenced across the frozen corpora, and it does not become that artifact by
> occupying the same role.

**Constructed under:** `ACT-CC-P10-1` · **Date:** 2026-09-04
**Evidence basis:** `EVIDENCE-LEDGER.md` `E-01`…`E-19`

---

## 1. The ten platform divisions

| PD | Registry name (`E-01`) | Domain label, frozen corpus (`E-04`) | Ownership evidenced | Lifecycle |
|---|---|---|---|---|
| **PD-01** | Executive — frozen `A4` header: `Official Name: Executive Office` | — | reference implementation | **NOT ACTIVATION-ELIGIBLE** (`E-15`) |
| **PD-02** | Architecture — frozen `A4` header: `Official Name: Architecture Office` | — | Architecture domain, `OA-01…OA-07` | **ACTIVE** (`E-14`, `GDR-0036`) |
| **PD-03** | Governance & Compliance | Governance | partial | not assessed |
| **PD-04** | Knowledge & Intelligence | Knowledge | partial | not assessed |
| **PD-05** | Runtime & Execution | Runtime | **owns Runtime** (`E-06`, `E-07`) | not assessed |
| **PD-06** | AI Engineering | AI Engineering | **owns implementation** (`E-08`) | not assessed |
| **PD-07** | Infrastructure & Platform | Infrastructure | **owns Infrastructure** (`E-09`) | not assessed |
| **PD-08** | Security | Security | **none** | not assessed |
| **PD-09** | Quality & Evaluation | Quality | *"Evaluate Quality"* (`E-10`) | not assessed |
| **PD-10** | Developer Experience | Developer **Enablement** — `CONFLICT` | **none** | not assessed |

**Column corrected 2026-09-05.** It was headed *"Official name"* while carrying
`MASTER_ROADMAP §5`'s compact enumeration. Only the two divisions with frozen
corpora carry a field literally named `Official Name`, and both are longer than
the registry form. **No name is decided, changed, or given precedence here** —
both forms are shown, attributed to their sources. For PD-01 and PD-02 the two
are compatible, one containing the other; **that is not true of `G-02`**, where
*Enablement* and *Experience* are not forms of each other, and `G-02` therefore
remains a conflict while this is a citation correction.

## 2. Structural rules — resident, not derived

1. **Reference, not template.** `PD-01` is the Gold Standard Reference Implementation; `PD-02`–`PD-10` follow by *"domain adaptation, not content copy"* (`E-02`).
2. **No subordination.** *"Numeric order is not full technical dependency, and dependency is not subordination — PD-02 is not a parent owner of other platforms"* (`E-03`), corroborated inside the frozen corpus: *"PD-02 tidak menjadi owner atas domain tersebut"* (`A4.md:289`).
3. **No metric imposition.** Adaptation proceeds *"tanpa memaksakan metric PD-02"* (`E-11`).
4. **Each division owns its own success criteria** (`E-05`).

**Consequence for the dependency graph (`§22.1`):** the only resident dependency
statement is a **negative** one — numeric order does not imply dependency, and
PD-02 owns nothing outside its domain. **No positive inter-PD dependency is
evidenced anywhere.** A dependency graph drawn now would be entirely inferred,
so none is drawn.

## 3. PD Maturity Matrix (`§32`)

States are not collapsed: `CONSTRUCTED ≠ RECONCILED ≠ REVIEWED ≠ VERIFIED ≠ FROZEN`.

| PD | Maturity | Basis |
|---|---|---|
| PD-01 | **REVIEWED** | 45 resident bodies; reference implementation; not activation-eligible |
| PD-02 | **VERIFIED** *(not frozen by this Act — already FROZEN by `GDR-0026`)* | 50 bodies, manifest 50/50 byte-identical, Gate PASS `GDR-0035`, ACTIVE `GDR-0036` |
| PD-03 | **CONSTRUCTED (derived)** | 79 statements; identity + partial ownership/authority |
| PD-04 | **CONSTRUCTED (derived)** | 84 statements; richest base; sole interface + lifecycle statements |
| PD-05 | **CONSTRUCTED (derived)** | ownership unambiguous, everything else absent |
| PD-06 | **CONSTRUCTED (derived)** | ownership evidenced |
| PD-07 | **CONSTRUCTED (derived)** | ownership evidenced |
| PD-08 | **CONSTRUCTED (derived, binding-open)** | owner role defined in frozen corpus; binding to CPID absent |
| PD-09 | **CONSTRUCTED (derived, binding-open)** | same pattern; role fragment only |
| PD-10 | **CONSTRUCTED (derived, name-contested)** | substance absent despite 40 references |

**Advanced from `EVIDENCE-READY`/`DISCOVERED` under `FDE-P10-FRONTIER-02`
Decision A**, which supplied established domain and primary construction target
for all ten — constraint material that did not previously exist. Records live in
`divisions/`.

**`CONSTRUCTED (derived)` is not `RECONCILED`, `REVIEWED`, `VERIFIED` or
`FROZEN`,** and asserts no canonical domain architecture: each record separates
its Established constraints from its derivations, and **5 of 40 derived Part
slots are left unfilled** where filling them would have been invention —
`PD-08` D and E, `PD-09` E, `PD-10` D and E. *(Recounted 2026-09-05; the figure
read "16 of 40", which `divisions/README.md §3`'s own enumeration contradicted.)*

## 4. Cross-PD Reconciliation Matrix (`§24`, `§25`)

> **These are reconciliation dimensions, not the evidence dimensions.**
> `EVIDENCE-LEDGER §2` measures **twelve** dimensions per division (8 × 12 = 96
> cells): Identity · Purpose · Ownership · Authority · Capability · Organization
> · Boundary · Interface · Dependency · Lifecycle · Governance · Change Control.
> The nine below serve a different purpose (`§24`, `§25` — cross-PD
> reconciliation) and are not a subset of those twelve: they **omit** Identity,
> Purpose, Organization and Change Control, and **add** Terminology, which is a
> conflict dimension rather than an evidence dimension. Recorded 2026-09-05
> because the two tables invite conflation and neither said so. **Neither matrix's
> content is altered.**

| Dimension | Result | Evidence |
|---|---|---|
| **Authority** | **PARTIAL** | Only PD-02's authority set is enumerated (`OA-01…OA-07`). PD-03/PD-04 carry fragments; five divisions carry none |
| **Ownership** | **PARTIAL** | Five divisions evidenced; **PD-08 and PD-10 have no ownership statement at all** |
| **Capability** | **MISSING** | 0 of 8 divisions carry a capability statement |
| **Interfaces** | **MISSING** | 1 statement across 8 divisions. `C8` Cross-Platform Architecture Governance exists but describes PD-02's responsibility, not a registry |
| **Dependencies** | **MISSING** | Only the negative rule (§2.2). No positive dependency evidenced |
| **Boundaries** | **PARTIAL** | The architectural boundary diagram (`E-04`) separates domains; no division defines its own boundary |
| **Lifecycle** | **PARTIAL** | Evidenced for PD-01 and PD-02 only |
| **Terminology** | **1 CONFLICT** | PD-10 Enablement/Experience (`G-02`) |
| **Governance** | **PARTIAL** | Each division owns its success criteria (`E-05`); no governance model is defined for any of the eight |

**Ownership overlap: none detected.** **Authority collision: none detected.**
Both are true because seven of ten divisions assert too little to collide — an
absence of conflict produced by absence of content, which is not the same as
coherence and is not reported as such.

**Mandatory distinctions held throughout:** `Authority ≠ Ownership` ·
`Dependency ≠ Ownership` · `Collaboration ≠ Control` · `Governance ≠ Execution`.

## 5. Organizational source ≠ organizational runtime

> **Conformance repair, 2026-09-05** — under `FDE-P10-AUTONOMOUS-EXECUTION-01
> §11`. This section previously stated that `Department` in `native_core` is
> *"a different entity"* from a Platform Division, and concluded that no bridge
> exists and that building one *"requires a twelfth boundary."* **That was
> wrong**, and it was wrong before this file was written: `ADR-0010`
> (**Approved**, Founder decision **FD-6**, `GDR-0020`) had already renamed the
> Canonical Domain Model entity to **Platform Division**, with `Department`
> recorded as its **historical alias**. The implementation's identifier was read
> as entity identity without checking the alias record. The correct state was
> determined independently by `ADE-P10-G04` (Option A); this repair brings the
> section into conformance with it and introduces no new decision.

The distinction is respected here, and the boundary between them is narrower
than this file first claimed.

**One entity, not two.** Canonical Domain Model §2: *"**Platform Division** … a
bounded, semi-autonomous unit of accountability with its own domain vocabulary.
Owns Capabilities and Agent Definitions. **Historical alias: Department** — see
ADR-0010."* The `Department` dataclass at
`native_core/core/capability/ownership.py:98` implements that entity under the
alias — its own docstring cites Freeze §4 and **INV-2**. `ADR-0010` chose
*"bounded amendment rather than global migration"*, so the alias surviving in
code is lawful and expected, not a defect.

**`PD-01`…`PD-10` are Platform Divisions.** The organizational representation
already exists in the frozen Domain Model spine. **No twelfth core boundary is
required or sought**, and the Native Core still holds *"exactly the eleven frozen
subsystem boundaries — no more"* (`E-12`).

**What is genuinely absent is instances, not a type.** **0** references to any
CPID exist across the implementation files (`E-19`, re-verified 2026-09-05:
0 hits for `PD-01`…`PD-10` across `native_core`, `consumers` and `tools`).

```text
PD-01 … PD-10          ORGANIZATIONAL SOURCE      documents, no instances
        │
        │  ← the entity type exists (Platform Division, alias Department);
        │    what is absent is any instance binding a CPID to it
        ▼
Native Core            ELEVEN FROZEN BOUNDARIES   runtime, no organization
```

**Binding a CPID to an instance would still be an architectural-tier change** →
Architecture Change Control → ADR under `Constitution §3.4` (`GDR-0032`). It is
not performed here. `G-04` is **RESOLVED**, and is no longer blocking.
