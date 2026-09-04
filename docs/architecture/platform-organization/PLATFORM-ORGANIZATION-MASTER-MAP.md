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

| PD | Official name (`E-01`) | Domain label, frozen corpus (`E-04`) | Ownership evidenced | Lifecycle |
|---|---|---|---|---|
| **PD-01** | Executive | — | reference implementation | **NOT ACTIVATION-ELIGIBLE** (`E-15`) |
| **PD-02** | Architecture | — | Architecture domain, `OA-01…OA-07` | **ACTIVE** (`E-14`, `GDR-0036`) |
| **PD-03** | Governance & Compliance | Governance | partial | not assessed |
| **PD-04** | Knowledge & Intelligence | Knowledge | partial | not assessed |
| **PD-05** | Runtime & Execution | Runtime | **owns Runtime** (`E-06`, `E-07`) | not assessed |
| **PD-06** | AI Engineering | AI Engineering | **owns implementation** (`E-08`) | not assessed |
| **PD-07** | Infrastructure & Platform | Infrastructure | **owns Infrastructure** (`E-09`) | not assessed |
| **PD-08** | Security | Security | **none** | not assessed |
| **PD-09** | Quality & Evaluation | Quality | *"Evaluate Quality"* (`E-10`) | not assessed |
| **PD-10** | Developer Experience | Developer **Enablement** — `CONFLICT` | **none** | not assessed |

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
| PD-03 | **EVIDENCE-READY** | 79 statements; identity + partial ownership/authority |
| PD-04 | **EVIDENCE-READY** | 84 statements; richest base; sole interface + lifecycle statements |
| PD-05 | **EVIDENCE-READY** | ownership unambiguous, everything else absent |
| PD-06 | **EVIDENCE-READY** | ownership evidenced |
| PD-07 | **EVIDENCE-READY** | ownership evidenced |
| PD-08 | **DISCOVERED** | identity only; 7 statements; no ownership anywhere |
| PD-09 | **DISCOVERED** | identity + role fragment; 8 statements |
| PD-10 | **DISCOVERED** | identity contested; substance absent despite 40 references |

**No division was advanced to `CONSTRUCTED`.** `CONSTRUCTED` would assert a
domain architecture, and for eight divisions no such architecture is evidenced
(`D-06`).

## 4. Cross-PD Reconciliation Matrix (`§24`, `§25`)

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

The distinction is not merely respected here; it is **enforced by the frozen
architecture**. The Native Core holds *"exactly the eleven frozen subsystem
boundaries — no more"* (`E-12`), and **0** references to any platform division
exist across 179 implementation files (`E-19`). `Department` in
`native_core/core/capability/ownership.py` is the Architecture Freeze §4
accountability unit — a different entity (`E-13`).

```text
PD-01 … PD-10          ORGANIZATIONAL SOURCE      documents, no runtime
        │
        │  ← no bridge exists; building one requires a twelfth boundary
        ▼
Native Core            ELEVEN FROZEN BOUNDARIES   runtime, no organization
```

**Any organizational runtime is therefore an architectural-tier change** →
Architecture Change Control → ADR under `Constitution §3.4` (`GDR-0032`).
Outside this Act (`§8`), and recorded as `G-04`.
