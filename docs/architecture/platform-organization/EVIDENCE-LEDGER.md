# Platform Organization — Evidence Ledger

> **Status: DERIVED.** Provenance record for `ACT-CC-P10-1`. Every claim below
> cites resident source. Unknown and conflict states are retained deliberately;
> none was downgraded to improve a completion figure (`§12`).

**Constructed under:** `ACT-CC-P10-1` · **Date:** 2026-09-04
**Method:** every resident occurrence of `PD-03`…`PD-10` across all 489 tracked
`docs/` files was extracted and read — **265 statements** in total. That set is
the resident evidence base for eight of the ten platform divisions **as sampled
from the frozen `PD-02` corpus**. It was previously described as *"the complete
resident evidence base"*; **that claim was wrong and is withdrawn** — `E-20`…`E-26`
were resident and unsampled throughout. A completeness claim in this file is not
evidence of completeness.

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
| **E-13** | `Department` is the Freeze §4 accountability unit owned by exactly one Organization. **Corrected 2026-09-05** (`FDE-P10-AUTONOMOUS-EXECUTION-01 §11`): this row previously read *"— not a platform division"*, which contradicted `ADR-0010` (Approved, FD-6, `GDR-0020`). `Platform Division` **is** the entity; `Department` is its recorded historical alias, and this class implements it under that alias. See `ADE-P10-G04-DECISION.md` | `native_core/core/capability/ownership.py` | :98 | Implementation | Implementation | **RESIDENT** |
| **E-14** | `PD-02` is ACTIVE | `GDR-0036` | Register | Founder | Governance | **CANONICAL** |
| **E-15** | `PD-01` is NOT ACTIVATION-ELIGIBLE — blocking AG-03, AG-08, AG-10 | `AIOS_VOLUME_ACTIVATION_MODEL_v1.0.md` | :341 | Governance | Resident | **CANONICAL** |
| **E-16** | Volumes 0, 0.1, 0.2, 0.3 are referenced but not resident | repository | 3 referencing files, 0 files | — | Absence | **UNKNOWN** |
| **E-17** | Platform Organization Master Map and Platform Encyclopedia are referenced but not resident | repository | 11 references, 0 files | — | Absence | **UNKNOWN** |
| **E-18** | No systemic gap inventory is resident | repository | 0 matches, both phrasings | — | Absence | **UNKNOWN** |
| **E-19** | No `PD-0x` or `Volume N` reference exists anywhere in implementation | `native_core`, `consumers`, `tools` | 0 matches / 179 `.py` files | Implementation | Observation | **RESIDENT** |
| **E-20** | PD-03's canonical volume is **Parts A–H × 10 = 80 sections** — **VERIFIED against the actual bodies 2026-09-05**: 8 Part files, **80/80 section identities present**, 3,704,607 bytes | `ACT-CC-P6-070` §2.2 + direct verification | supplied-source path, **not resident** | Act record + direct | Verified | **VERIFIED / NOT RESIDENT** |
| **E-21** | **CORRECTED 2026-09-05.** Previously: *"bodies: 0 supplied, 0 resident."* **`0 resident` remains true. `0 supplied` is now misleading** — `ACT-CC-P6-070` counted only the four control artifacts before it; the **eight Part bodies exist and were verified this cycle**. What is absent is *residency*, not the bodies | `ACT-CC-P6-070` §2.2 + direct verification | — | Act record + direct | Correction | **CORRECTED** |
| **E-22** | PD-03 **`B2–B10` declare `NOT FROZEN — SOURCE GATE BLOCKED`** | `ACT-CC-P6-071` | §2 | Act record | Resident | **RESIDENT** |
| **E-23** | PD-04's supplied corpus is **30/30 sections** — `A1–A10`, `B1–B10`, `C1–C10` — across 3 files, **102,540 lines / 1,508,896 bytes**; 23 FROZEN, 2 Bounded Canonical Synthesis, 2 Bounded Canonical Reconstruction, 1 FROZEN WITH QUALIFICATION, 2 unstated. **VERIFIED against the actual bodies 2026-09-05: 30/30 sections present, byte total 1,508,896 — exact match** | `ACT-CC-P6-071` §2 + direct verification | supplied-source path, **not resident** | Act record + direct | Verified | **VERIFIED / NOT RESIDENT** |
| **E-24** | PD-04 **declared identity**: `Platform Authority: Knowledge Authority` · `Primary Responsibility: Knowledge, Context, Intelligence Assets` · `Primary Dependencies: AI Engineering, Runtime` | `ACT-CC-P6-071` | §2, Part A block | Act record | Resident | **RESIDENT** |
| **E-25** | PD-03 ↔ PD-04 ownership boundary, stated consistently from both sides, **conflict NONE**: `B1 §11` *"PD-03 tidak menjadi organizational owner atas: … Knowledge & Intelligence"*; `C8` *"PD-04 owns Knowledge Integrity … PD-03 owns Governance & Compliance and provides certification/compliance"*; `C8 §36` routes certification through PD-03 with PD-04 supplying evidence | `ACT-CC-P6-071` | §12 | Act record | Resident | **RESIDENT** |
| **E-26** | Platform Encyclopedia Volume 3 is **CITATION ONLY relative to this repository**; the four PD-03 files (780 lines) were supplied to a prior Act and are not resident | `ACT-CC-P6-070` | §2.1, :213 | Act record | Resident | **RESIDENT** |

> **`E-20`…`E-26` added 2026-09-05** under `ACT-CC-P10-C6`, harvested from
> `ACT-CC-P6-070` (590 lines) and `ACT-CC-P6-071` (567 lines) — two resident Acts
> assessing the PD-03 and PD-04 source bases. **Neither was cited anywhere in this
> corpus before now.** They were resident throughout the P10-1 construction and
> were not found, which is disclosed at `§19` of the P10 verification record.
>
> **What these entries do and do not establish.** They record *what a resident Act
> verified about* the PD-03 and PD-04 corpora. **Those corpora remain NOT
> RESIDENT** — `G-01` is unchanged. An inventory of an absent body is evidence
> about it, never a substitute for it, and no section body is reconstructed here.

| **E-27** | The `AIOS CO-FOUNDER DELEGATION CHARTER v1.0` body is **recovered and read**. Its own header: *"**Effective:** Upon Founder approval **and registration in the AIOS canonical governance source**."* Its own `§20 Canonical Status`: *"**Status: Pending Founder Approval**"* | Charter body, supplied-source path | header, §20 | Instrument | Verified | **VERIFIED — PENDING, NOT EFFECTIVE** |
| **E-28** | **No Charter approval or registration record exists.** The Delegation Register carries `DEL-T4.4-CF-001` and `DEL-F03-015-P7I99-001` only | `AIOS_DELEGATION_REGISTER_v1.0.md` | §3 | Governance | Absence | **RESIDENT** |
| **E-29** | A Volume becomes resident only by **Founder supply under a named Act**: PD-01 — *"Architect-supplied Recovery Candidate (AR-PD01-P7-REC-006)… supplied directly in the REC-006 Act"*; PD-02 — *"Authorized by: FOUNDER · ACT-CC-F03-009 · ACT-CC-F03-010"*, bodies *"supplied by the Founder as five SOURCE TRANSFER BATCH messages"*. Even the **namespace** required `ADR-0012`, Decision Owner **Architect (Founder)** | `RECOVERY-MANIFEST.md`, `RESIDENCY-MANIFEST.md`, `ADR-0012` | — | Governance | Resident | **RESIDENT** |

| **E-30** | PD-03's `A1` declares verbatim: `Platform ID: PD-03` · `Platform Name: Governance & Compliance` · **`Platform Type: Platform Division`** · **`Platform Authority: Governance Authority`** · `Status: FROZEN` · `Gold Standard Review: PASS` · `Freeze Decision: APPROVED` | Volume 3 Part A, `A1` | source body | Canonical (non-resident) | Direct read | **SOURCE-VERIFIED / NOT RESIDENT** |
| **E-31** | PD-03 `B7`–`B10` carry the literal title **"Canonical Section Identity Pending"**; `C9`, `G2` and `H10` are unresolved in the body. **The volume is internally incomplete at source**, corroborating `E-22` from the source side | Volume 3 Parts B, C, G, H | source body | Canonical (non-resident) | Direct read | **SOURCE-VERIFIED / NOT RESIDENT** |
| **E-32** | PD-04 Part B carries an interleaved `B01`–`B06` constraint series: *"No Cross-Team Ownership Without Delegation"* · *"Dependency Does Not Create Ownership"* · *"Consumer Does Not Become Owner"* · *"Quality Does Not Become Domain Owner"* · *"Evolution Does Not Become Uncontrolled"* · *"Workforce Does Not Redefine Boundary"* — the same distinctions this corpus derived independently from `MASTER_ROADMAP §5` and PD-02 | Volume 4 Part B | source body | Canonical (non-resident) | Direct read | **SOURCE-VERIFIED / NOT RESIDENT** |

| **E-33** | PD-03 `A1 §22` declares: `PRIMARY RESPONSIBILITIES: Policy · Control · Certification` · **`PRIMARY DEPENDENCIES: Architecture · Security · Quality`** · `PRIMARY OUTPUTS: Policy · Standards` · **`TECHNICAL DESIGN OWNERSHIP: NOT OWNED BY PD-03`** · `CANONICAL REFERENCE: Governance Baseline` | Volume 3 Part A, `A1` §22, §24 | source body | Canonical (non-resident) | Direct read | **SOURCE-VERIFIED / NOT RESIDENT** |
| **E-34** | PD-03 `A1 §21` enumerates what its baseline **does not** establish at `A1` level — detailed Governance Charter · Governance Authority Matrix · internal organizational structure · governance workflow · performance model · maturity target · certification lifecycle — and declines to claim them as canonical | Volume 3 Part A, `A1` §21 | source body | Canonical (non-resident) | Direct read | **SOURCE-VERIFIED / NOT RESIDENT** |
| **E-35** | PD-04 `A1` declares `CPID: PD-04` · `SOURCE-FIDELITY MODE: Bounded Canonical Synthesis` · `SOURCE SUPPORT: Strong for Identity, Bounded for Constitutional Framing` · `UNSUPPORTED AUTHORITY: NONE IDENTIFIED` · `BOUNDARY EXPANSION: NONE IDENTIFIED` | Volume 4 Part A, `A1` | source body | Canonical (non-resident) | Direct read | **SOURCE-VERIFIED / NOT RESIDENT** |

| **E-36** | Volume 3 **Part B declares `NOT FROZEN` · `BOUNDED RECORD ONLY`**, review `BLOCKED BY SOURCE IDENTITY` and `NOT COMPLETABLE FOR STRUCTURAL FREEZE`. Parts A, C, D, E, F, H declare `FROZEN`; **Part G declares `FROZEN WITH SOURCE QUALIFICATION`** | Volume 3 Parts A–H freeze records | source body | Canonical (non-resident) | Direct read | **SOURCE-VERIFIED / NOT RESIDENT** |
| **E-37** | The volume names **three section-level source gaps of its own**: `EXPLICIT PD-03 D5 SOURCE NOT LOCATED` · `LITERAL G4 BASELINE NOT FOUND` · `LITERAL COMPLETE G6 BASELINE NOT FOUND` | Volume 3 Parts D, G | source body | Canonical (non-resident) | Direct read | **SOURCE-VERIFIED / NOT RESIDENT** |
| **E-38** | Volume 3 Part G records `GOLD STANDARD REVIEW: PASS WITH RECONCILIATION REQUIRED` and **`CLAUDE CODE RECONCILIATION REQUIRED`**. **Recorded, not acted on** — a note inside a non-resident body is not an authorization | Volume 3 Part G | source body | Canonical (non-resident) | Direct read | **SOURCE-VERIFIED / NOT ACTIONABLE** |
| **E-39** | Both volumes apply a per-Part **Source-Fidelity Mode** taxonomy: *Bounded Canonical Synthesis* · *Bounded Canonical Reconstruction* · *Bounded Domain Reconstruction* · *Source-Bounded Reference-Adapted*. **No Part claims unbounded canonical status** | Volumes 3 and 4, all Parts | source body | Canonical (non-resident) | Direct read | **SOURCE-VERIFIED / NOT RESIDENT** |
| **E-40** | Volume 4 Part C names `PD-02 Architecture Office`, `PD-03 Governance & Compliance` and `PD-04 Knowledge & Intelligence` as authorities within PD-04's Knowledge Architecture | Volume 4 Part C | source body | Canonical (non-resident) | Direct read | **SOURCE-VERIFIED / NOT RESIDENT** |

| **E-41** | **CITATION CORRECTION.** *"PD-05 sebagai consumer Knowledge"* was cited in three places as **Frozen `PD-02`** evidence. **It does not occur in PD-02's corpus** — 0 hits across `volume-1` and `volume-2`. Its source is **PD-04's `Volume 4 Part C` §`C3`** (non-resident), confirmed in the recovered body and at `ACT-CC-P6-071:188`. Originated at commit `9c96ab3`; survived ten cycles | `Volume 4 C3`; `ACT-CC-P6-071:188` | source body + Act | Correction | Direct read | **CORRECTED — evidence class downgraded** |
| **E-42** | **Five inbound dependency edges propagated** to the records of the divisions named: `PD-03 → PD-02 · PD-08 · PD-09` (`E-33`); `PD-04 → PD-06 · PD-05` (`E-24`). For **PD-02 this is the first statement originating outside its own corpus**; for **PD-06, PD-08 and PD-09 it is the first evidenced relationship of any kind** | `E-24`, `E-33` | derived propagation | Construction | Verified | **CONSTRUCTED** |

| **E-43** | The **AIOS Master Program** (`AIOS_MASTER_PROGRAM_v1_0_LENGKAP.md`, 225,894 bytes) was recovered in Cycle 7, inventoried, and **never read until Cycle 12**. Its *Document Authority Structure* sets two layers — **Volume I = Constitutional (Pasal 1–8)**, **Volumes II–VIII = Strategic** — and its *Source of Truth Navigation* names `AIOS_CANONICAL_ARCHITECTURE.md` as SSOT for **Phase Definition, Dependency and Lifecycle Status** | Master Program, Document Authority Structure · Source of Truth Navigation | supplied-source path | Program (non-resident) | Direct read | **SOURCE-VERIFIED / NOT RESIDENT** |
| **E-44** | **`GDR-0001` (Founder Decision G1′) already determined the precedence question `E-43` raises.** For **repository architecture**: `AIOS_CANONICAL_ARCHITECTURE.md` is *"**not** the semantic authority; that is the Canonical Domain Model"*, and Master Program `Pasal 7–8` are *"no longer an independent constitutional source; repository artifact precedence is **Engineering Constitution §4**."* Both retain their role **within the Master Program corpus** | `AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md:181-183` | resident | **Founder Decision** | Direct read | **RESIDENT — AUTHORITATIVE** |
| **E-45** | The **External Corpus Synchronization Ledger already records** that the Master Program (I–VIII), `AIOS_CANONICAL_ARCHITECTURE.md`, ALMM, Project Governance and the Engineering Charter are *"not present in this repository and cannot be synchronized here"*, with the required changes recorded so the requirement survives | `AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md:4925-4928` | resident | Governance | Direct read | **RESIDENT** |

> **`E-43`…`E-45` added 2026-09-05** under `ACT-CC-P10-FINAL §20`, which required
> an active attempt to **falsify** the exhaustion conclusion. **The attempt
> succeeded**: a 225 KB source this corpus had inventoried and never opened.
>
> **Reading it confirmed the current posture rather than overturning it.** The
> Master Program names a different SSOT for Dependency and Lifecycle, which would
> have meant the dependency graph was drawn from the wrong source — **except that
> `GDR-0001` had already routed repository-architecture semantics to the
> Canonical Domain Model and precedence to `Engineering Constitution §4`**, which
> is what this corpus has used throughout. **The doubt is retired by a prior
> Founder decision, not by my own reasoning** (`E-44`).
>
> **`AIOS_CANONICAL_ARCHITECTURE.md` remains NOT RESIDENT** — 15 citations, 0
> files — and its ARB-002-ratified `§3.1`–`§3.4` dependency principles remain a
> valid Founder-ratified record that this corpus has never consulted, because the
> body is unavailable. **That is a genuine source gap, and it is `E-45`'s, not a
> new one.**

> **`E-41` is a correction against this corpus's own work.** The evidence class
> moved from *frozen resident* — the strongest this corpus holds — to
> *non-resident PD-04*, among the weakest. **The statement is real; its authority
> was overstated for ten cycles.**

> **`E-36`…`E-40` added 2026-09-05** — the Parts `B`–`H` / `B`–`C` harvest that
> `§19` identified as unfinished. **`E-36` confirms `E-22` from the body itself**;
> **`E-37` records three gaps the source names against itself**; **`E-38` is a
> task the source assigns to this role, which cannot be performed while the body
> is non-resident.**

> **`E-33`…`E-35` added 2026-09-05** under `ACT-CC-P10-C7 §36` (construction
> depth). **`E-33` supplies PD-03's Authority, Ownership, Dependency and
> Interface dimensions from PD-03's own corpus** — four cells the matrix recorded
> ABSENT. **`E-34` and `E-35` are the two volumes grading their own evidence**:
> each enumerates what its baseline does not support and declines to claim it.

> **`E-30`…`E-32` added 2026-09-05** under `ACT-CC-P10-C7 §7`, read **directly
> from the source bodies** rather than from an Act's report of them.
> **`E-30` is the first evidence of PD-03's authority stated by PD-03 itself**;
> every prior statement about it came from PD-02's side. `Platform Type: Platform
> Division` independently corroborates `ADR-0010` from a corpus authored outside
> this repository.

> **`E-27`…`E-29` added 2026-09-05** under `ACT-CC-P10-C7`, from the source
> recovery pass its `§7`–`§10` direct. **`E-20`, `E-21` and `E-23` were upgraded
> from *"an Act recorded this"* to *"verified against the actual bodies."***
>
> **Residency is unchanged and deliberately so.** The Volume 3 and Volume 4
> bodies exist in a supplied-source path and are **not committed**: `E-29`
> establishes that residency is conferred by Founder supply under a named Act,
> and no such Act exists for either Volume. See `ESC-C7-01`.

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
