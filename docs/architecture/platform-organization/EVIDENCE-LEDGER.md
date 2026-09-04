# Platform Organization — Evidence Ledger

> **Status: DERIVED.** Provenance record for `ACT-CC-P10-1`. Every claim below
> cites resident source. Unknown and conflict states are retained deliberately;
> none was downgraded to improve a completion figure (`§12`).

**Constructed under:** `ACT-CC-P10-1` · **Date:** 2026-09-04
**Method:** every resident occurrence of `PD-03`…`PD-10` across all 489 tracked
`docs/` files was extracted and read — **265 statements** in total. That set is
the complete resident evidence base for eight of the ten platform divisions.

---

## 1. Evidence Ledger

| ID | Claim | Source | Location | Authority | Type | Status |
|---|---|---|---|---|---|---|
| **E-01** | Ten platform divisions exist, with official names | `AIOS_MASTER_ROADMAP_CONSOLIDATED_v1.0.md` | §5 Platform registry, :71–75 | Program | Resident | **AUTHORITATIVE** |
| **E-02** | `PD-01` is the Gold Standard Reference Implementation; `PD-02`–`PD-10` follow by *"domain adaptation, not content copy"* | same | §5, :76–77 | Program | Resident | **AUTHORITATIVE** |
| **E-03** | *"Numeric order is not full technical dependency, and dependency is **not** subordination — PD-02 is not a parent owner of other platforms"* | same | §5, :78–79 | Program | Resident | **AUTHORITATIVE** |
| **E-04** | Domain roster naming PD-03…PD-10 | `volume-2/pd-02-architecture-office/A4.md` | :281–288 | **FROZEN corpus** | Resident | **CANONICAL** |
| **E-05** | Each PD owns its own domain success criteria | `volume-1/pd-01-executive-office/C10.md` | :85–92 | PD-01 reference | Resident | **AUTHORITATIVE** |
| **E-06** | *"PD-05 owns Runtime."* | `volume-2/.../B7.md` | :212 | **FROZEN** | Resident | **CANONICAL** |
| **E-07** | *"PD-05 tetap menentukan operational execution dalam domain Runtime."* | `volume-2/.../A5.md` | :703 | **FROZEN** | Resident | **CANONICAL** |
| **E-08** | *"PD-06 owns implementation."* | `volume-2/.../B4.md` | :731 | **FROZEN** | Resident | **CANONICAL** |
| **E-09** | *"PD-07 tetap memiliki ownership atas Infrastructure."* | `volume-2/.../C8.md` | :122 | **FROZEN** | Resident | **CANONICAL** |
| **E-10** | *"PD-09 — Evaluate Quality"* | `volume-2/.../C8.md` | :303 | **FROZEN** | Resident | **CANONICAL** |
| **E-11** | *"PD-03 hingga PD-10 dengan domain adaptation"* · *"tanpa memaksakan metric PD-02"* | `volume-2/.../E4.md`, `D4.md` | :1431, :1125 | **FROZEN** | Resident | **CANONICAL** |
| **E-12** | Native Core holds *"exactly the eleven frozen subsystem boundaries — no more"* | `AIOS_NATIVE_CORE_BLUEPRINT_v1.0.md` | :31 | Canonical Architecture | Resident | **CANONICAL** |
| **E-13** | `Department` is the Freeze §4 accountability unit owned by exactly one Organization — not a platform division | `native_core/core/capability/ownership.py` | :98 | Implementation | Implementation | **RESIDENT** |
| **E-14** | `PD-02` is ACTIVE | `GDR-0036` | Register | Founder | Governance | **CANONICAL** |
| **E-15** | `PD-01` is NOT ACTIVATION-ELIGIBLE — blocking AG-03, AG-08, AG-10 | `AIOS_VOLUME_ACTIVATION_MODEL_v1.0.md` | :341 | Governance | Resident | **CANONICAL** |
| **E-16** | Volumes 0, 0.1, 0.2, 0.3 are referenced but not resident | repository | 3 referencing files, 0 files | — | Absence | **UNKNOWN** |
| **E-17** | Platform Organization Master Map and Platform Encyclopedia are referenced but not resident | repository | 11 references, 0 files | — | Absence | **UNKNOWN** |
| **E-18** | No systemic gap inventory is resident | repository | 0 matches, both phrasings | — | Absence | **UNKNOWN** |
| **E-19** | No `PD-0x` or `Volume N` reference exists anywhere in implementation | `native_core`, `consumers`, `tools` | 0 matches / 179 `.py` files | Implementation | Observation | **RESIDENT** |

**External evidence: none.** No external repository or pattern was consulted
(`§14`). Internal evidence was the limiting factor, and no external source could
have supplied AIOS domain facts.

## 2. Per-PD evidence baseline

Twelve dimensions per division. **`EVIDENCED`** cites resident source;
**`ABSENT`** means no resident statement exists — not that the fact is untrue.

### Legend

`◆` evidenced · `◐` partial — named but not defined · `○` absent

| Dimension | PD-03 | PD-04 | PD-05 | PD-06 | PD-07 | PD-08 | PD-09 | PD-10 |
|---|---|---|---|---|---|---|---|---|
| Identity | ◆ | ◆ | ◆ | ◆ | ◆ | ◆ | ◆ | ◆ |
| Purpose (domain) | ◆ | ◆ | ◆ | ◆ | ◆ | ◆ | ◆ | ◆ |
| Ownership | ◐ | ◐ | ◆ | ◆ | ◆ | ○ | ◐ | ○ |
| Authority | ◐ | ◐ | ○ | ○ | ○ | ○ | ○ | ○ |
| Capability | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Organization | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Boundary | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Interface | ○ | ◐ | ○ | ○ | ○ | ○ | ○ | ○ |
| Dependency | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Lifecycle | ○ | ◐ | ○ | ○ | ○ | ○ | ○ | ○ |
| Governance | ◐ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Change Control | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| **evidence lines** | **79** | **84** | **11** | **11** | **9** | **7** | **8** | **40** |

### PD-03 — Governance & Compliance
**Identity** `E-01`, `E-04` · **Ownership/Authority** partial — 3 authority-bearing
and 3 ownership-bearing statements, all describing PD-03's *relationship to
PD-02*, none defining PD-03's own model · **Success criteria** owned by PD-03
(`E-05`) · everything else **ABSENT**.

### PD-04 — Knowledge & Intelligence
**Identity** `E-01`, `E-04` · richest evidence base (84 lines), including 6
authority-bearing and 7 ownership-bearing statements, plus the single resident
interface and lifecycle statements across all eight divisions · still **no**
capability, boundary, dependency or change-control definition.

### PD-05 — Runtime & Execution
**Ownership evidenced and unambiguous:** *"PD-05 owns Runtime"* (`E-06`) and
*"PD-05 tetap menentukan operational execution dalam domain Runtime"* (`E-07`),
both from the frozen corpus. **All other dimensions ABSENT** — 11 lines total.
The division with the clearest mandate and the least definition.

### PD-06 — AI Engineering
*"PD-06 owns implementation"* (`E-08`). Identity and ownership only.

### PD-07 — Infrastructure & Platform
*"PD-07 tetap memiliki ownership atas Infrastructure"* (`E-09`). Identity and
ownership only.

### PD-08 — Security
**Weakest evidence base — 7 lines.** Identity (`E-01`, `E-04`) and success-criteria
ownership (`E-05`). **No ownership, authority, capability, boundary, interface,
dependency, lifecycle, governance or change-control statement exists anywhere in
the corpus.** For a security division this absence is itself the finding.

### PD-09 — Quality & Evaluation
*"PD-09 — Evaluate Quality"* (`E-10`) — a role fragment, not a definition. 8 lines.

### PD-10 — Developer Experience
40 lines, but almost all are the *adaptation rule* (`E-11`) restating
`PD-03…PD-10` as a range rather than saying anything about PD-10 specifically.
Identity evidenced; substance **ABSENT**. **The reference count is misleading and
would have read as strength without content anchoring.**

## 3. Conflicts

**One, and it is narrower than it first appeared.** `E-04` is an *architectural
boundary diagram* in the frozen corpus carrying short domain labels; `E-01` is a
*platform registry* carrying official names. Most differences are therefore
short-form against full-form — `Governance` / `Governance & Compliance`,
`Knowledge` / `Knowledge & Intelligence`, `Infrastructure` / `Infrastructure &
Platform`, `Quality` / `Quality & Evaluation` — which is label brevity in a
diagram, not disagreement. Classifying those as conflicts would have inflated
the finding.

**`PD-10` is the exception and a genuine divergence:** the frozen corpus says
*"Developer **Enablement**"*, the registry says *"Developer **Experience**"*.
Neither is a truncation of the other.

**Not resolved here.** `§6.1` bars inventing precedence, and no resident source
establishes whether the frozen `PD-02` roster or the program registry governs
platform naming. Recorded as **`CONFLICT`**; see `SYSTEMIC-GAP-MAP.md` `G-02`.

**Corroboration found in the same diagram, worth recording:** `A4.md:289`
closes the roster with *"PD-02 tidak menjadi owner atas domain tersebut"* —
PD-02 is not the owner of those domains. That is `E-03`'s non-subordination rule
stated independently inside the **frozen** corpus, so the rule rests on two
sources of different authority rather than one.
