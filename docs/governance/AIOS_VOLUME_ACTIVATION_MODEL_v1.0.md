# AIOS Volume Activation Model

**Version:** v1.0
**Status:** Canonical — governance machinery
**Authority:** Founder · `ACT-CC-F03-014`
**Recorded by:** Claude Code / Co-Founder (Construction Phase)
**Date:** 2026-08-16
**Scope:** PD-01 (Volume 1) · PD-02 (Volume 2)
**Activation performed by this document:** **NONE**

---

## 1. Purpose

This document exists so the repository can answer, without relying on
conversation memory: what makes a Volume eligible for activation, who may
authorize it, and how integrated review, freeze, eligibility and authorization
relate.

**It records governance machinery. It activates nothing and freezes nothing.**

Where an authoritative source establishes a rule, this document cites it. Where
no source exists, it records a **GOVERNANCE GAP** rather than inventing one.

---

## 2. Canonical lifecycle

```text
SOURCE / CORPUS → RESIDENCY → SECTION VALIDATION → INTEGRATED VOLUME REVIEW
   → FREEZE ELIGIBILITY → FREEZE → ACTIVATION ELIGIBILITY → ACTIVATION GATE
   → FOUNDER ACTIVATION AUTHORIZATION → ACTIVATED
```

### Mandatory semantic distinctions

```text
Designation ≠ Residency                Integrated Review ≠ Freeze
Residency ≠ Validation                 Freeze ≠ Activation Eligibility
Section PASS ≠ Integrated Review PASS  Activation Eligibility ≠ Activation Authorization
Activation Authorization ≠ Activation execution
Activation ≠ AIOS Completion
```

No two states may be collapsed because they are operationally adjacent.

---

## 3. Lifecycle transitions — evidence status

Each transition is classified by whether resident evidence establishes it.

| # | Transition | Evidence | Status |
|---|---|---|---|
| T1 | Source → Residency | PD-01 `RECOVERY-MANIFEST` · PD-02 `RESIDENCY-MANIFEST` (50/50 byte-identical) | **ESTABLISHED** |
| T2 | Residency → Section Validation | Body metadata `Gold Standard Review: PASS` — PD-01 20/45 · PD-02 48/50 | **ESTABLISHED** |
| T3 | Section Validation → Integrated Review | `ACT-CC-REM-003.0 §6`: section-level claims *"do not constitute Volume-level freeze"* | **ESTABLISHED** |
| T4 | Integrated Review → Freeze Eligibility | PD-01 manifest: `Volume 1 Freeze Gate \| NOT APPROVED (P7-I99 re-gate outstanding)`; roadmap `REM-003 → P7-I99 → V1 Freeze` | **ESTABLISHED — but not the only route (see §4)** |
| T5 | Freeze Eligibility → Freeze | `GDR-0017` (FD-4) | **ESTABLISHED** |
| T6 | **Freeze → Activation Eligibility** | **none found** | **⚠ GOVERNANCE GAP — NOT SELF-AUTHORIZED** |
| T7 | Activation Eligibility → Activation Gate | `ACT-CC-F03-014 §3` | **ESTABLISHED (this Act)** |
| T8 | Activation Gate → Founder Authorization | `ACT-CC-F03-014 §3` | **ESTABLISHED (this Act)** |
| T9 | Authorization → Activated | `ACT-CC-F03-014 §3` | **ESTABLISHED (this Act)** |

---

## 4. P7-I99 → Freeze: established, but **not exclusive**

Resident evidence shows P7-I99 is the integrated review and freeze gate for
Volume 1. It also shows that **Volume 1 reached `FROZEN` without it**:

> `GDR-0017`: *"**P7-I99 was not executed and did not produce this freeze.** The
> Founder determined the lifecycle state directly."*

Therefore two routes to Freeze exist in the record:

| Route | Mechanism | Precedent |
|---|---|---|
| **R-A** | P7-I99 returns `APPROVED FOR FREEZE` | Never achieved — 2 runs, both `NOT APPROVED` |
| **R-B** | Founder determines the lifecycle state directly | `GDR-0017` (FD-4) — Volume 1 |

**A frozen Volume is therefore not evidence that its integrated review passed.**
Volume 1 is `FROZEN` (lifecycle, R-B) **and** its freeze gate is `NOT APPROVED`
(review, R-A). Both are true; they answer different questions.

---

## 5. PD-01 P7-I99 — provenance reconstruction

Bounded source reconstruction was performed across the repository **and** the
session transcript. Results are separated into recovered fact and unrecovered
gap. **Nothing was inferred, and the PD-02 requirement set was not substituted.**

### 5.1 Recovered — established by resident evidence

| # | Fact | Source |
|---|---|---|
| 1 | P7-I99 is the integrated architecture review **and freeze gate** for Volume 1 | PD-01 manifest `:281` |
| 2 | It is sequenced **after** REM-003 | `REM-003.0:92`, `:118` |
| 3 | It **ran twice**; both runs returned `NOT APPROVED FOR FREEZE` | `REM-003.0:92` |
| 4 | Its blockers were the REM-003 remediation targets | `REM-003.0:92` |
| 5 | Its result vocabulary is `APPROVED FOR FREEZE` / `NOT APPROVED FOR FREEZE` | `REM-003.0:92`, manifest `:208` |
| 6 | Current status: **HOLD**, re-gate outstanding | `GDR:2265–2266`, manifest `:281` |
| 7 | Authority to execute it is **excluded** from the Co-Founder appointment | Appointment Register `§3.2` exclusion **22** |
| 8 | Section-level `PASS` / `FROZEN` claims do **not** satisfy it | `REM-003.0:100` |

### 5.2 Unrecovered — **NOT RECOVERABLE**

| # | Missing | Search performed | Result |
|---|---|---|---|
| 1 | The Volume 1 requirement set (R1…Rn) | Full repository grep · full transcript (2,387 `P7-I99` occurrences) | **0** — every requirement-bearing context refers to the **Volume 2** set |
| 2 | Volume 1 pass/fail criteria | same | **0** |
| 3 | Volume 1 classification model | same | **0** |
| 4 | Volume 1 eligibility logic | same | **0** |

### 5.3 Authority impact

PD-01 cannot pass an integrated review whose requirements do not exist in any
recoverable source. Substituting the PD-02 R1–R11 set is **prohibited** — the
Volume 2 set is domain-adapted and its historical identity with the Volume 1 set
is unproven. Authoring a replacement set would be inventing substantive
criteria, then grading PD-01 against them.

### 5.4 Minimum Founder decision required

Exactly one of:

| Option | Effect |
|---|---|
| **A** | Founder supplies the Volume 1 P7-I99 requirement set → PD-01 integrated review becomes executable |
| **B** | Founder rules the Volume 2 R1–R11 set applies to Volume 1 → PD-01 review executable under that set |
| **C** | Founder defines PD-01 activation eligibility **without** an integrated-review requirement, relying on the direct-lifecycle route (R-B) already exercised in `GDR-0017` |
| **D** | Founder defers PD-01 activation |

**GOVERNANCE GAP — NOT SELF-AUTHORIZED.**

---

## 6. Activation Gate — criteria classification

Criteria are classified by source, per `ACT-CC-F03-014`. Category **C** items are
gaps; category **D** items are Founder-reserved. Neither may be promoted to
category **A** by implementation convenience.

| ID | Criterion | Category | Source / status |
|---|---|---|---|
| AG-01 | Identity / residency integrity | **A** source-backed | Manifests; ADR-0012 for Volume 2 namespace |
| AG-02 | Corpus completeness | **A** | PD-01 45/45 manifest; PD-02 50/50 manifest |
| AG-03 | Integrated architecture review | **A** for PD-02 (`ACT-CC-F03-007`) · **C GAP** for PD-01 (§5) | — |
| AG-04 | Material findings resolved | **A** | `ACT-CC-VAL-001` + GDR dispositions |
| AG-05 | Authority integrity | **A** | Constitution §3.2 · `DEL-T4.4-CF-001` · Appointment Register |
| AG-06 | Traceability / evidence integrity | **B** derived check | Mechanical verification of AG-01…AG-05 |
| AG-07 | Freeze eligibility / freeze state | **A** | `GDR-0017` · PD-01 manifest · §4 above |
| AG-08 | Activation-specific readiness | **C GAP** | No resident source defines what activation *does* (§3 T6) |
| AG-09 | Governance separation | **A** | `ACT-CC-F03-006` · `ACT-CC-F03-014` |
| AG-10 | Founder activation authorization | **D** Founder-reserved | `ACT-CC-F03-014 §3` |

---

## 7. Volume-specific gates

Shared primitives are reused only where source-authorized. Domain-specific
requirements are **not** flattened for symmetry.

### 7.1 PD-01 — Executive Office (Volume 1)

| Criterion | Required state | Current | Blocking |
|---|---|---|---|
| AG-01 identity/residency | corpus at `volume-1/pd-01-executive-office/` | **45/45 resident** | no |
| AG-02 completeness | A10 · **B5** · C10 · D10 · E10 = 45 | **PASS** — Part B is 5 by design (`END OF PART B — B1–B5`) | no |
| AG-03 integrated review | P7-I99 (Volume 1) result | **NOT APPROVED** ×2; **requirement set unrecoverable** | **YES** |
| AG-04 findings | material findings dispositioned | F-01/02/03/07/09/11 resolved; **F-05 non-blocking**; F-12 UNKNOWN; **F-14 superseded** | no |
| AG-05 authority | valid bounded authority | `DEL-T4.4-CF-001` ACTIVE | no |
| AG-07 freeze | freeze state known | **FROZEN** via R-B (`GDR-0017`); gate `NOT APPROVED` via R-A | see §4 |
| AG-08 activation readiness | defined | **GAP** | **YES** |
| AG-10 authorization | Founder authorization issued | **NOT ISSUED** | **YES** |

**PD-01 = NOT ACTIVATION-ELIGIBLE.** Blocking: AG-03, AG-08, AG-10.

### 7.2 PD-02 — Architecture Office (Volume 2)

| Criterion | Required state | Current | Blocking |
|---|---|---|---|
| AG-01 identity/residency | corpus at `volume-2/pd-02-architecture-office/` | **50/50**, byte-identical, ADR-0012 | no |
| AG-02 completeness | A10·B10·C10·D10·E10 = 50 | **PASS** | no |
| AG-03 integrated review | P7-I99 Volume 2 R1–R11 | **requirement set RESIDENT** (`ACT-CC-F03-007`); **review NOT RUN** | **YES** |
| AG-04 findings | B-07 and Phase D findings resolved | ADR-0010/0011/0012; F-D1/F-D2/F-D3 resolved | no |
| AG-05 authority | Architecture Authority designated | **DESIGNATED**, activation HELD (`GDR-0019`) | see note |
| AG-06 traceability | chain reconstructible | `ACT-CC-F03-006/007` resident | no |
| AG-07 freeze | Volume-level freeze | **NOT FROZEN** — 23 section-level claims are **not** Volume freeze | no |
| AG-08 activation readiness | defined | **GAP** | **YES** |
| AG-10 authorization | Founder authorization issued | **NOT ISSUED** | **YES** |

**PD-02 = NOT ACTIVATION-ELIGIBLE.** Blocking: AG-03 (review not run), AG-08, AG-10.

**AG-05 note.** `GDR-0019 §4`'s evidence gate — which forced the activation hold
because no repository body named PD-02 as Architecture Office or as an authority
holder — is now satisfiable: 56 files contain "Architecture Office", 50/50 bodies
declare `Platform ID: PD-02`, and `A1` declares `Platform Authority: Architecture
Authority`. **Lifting the hold requires a governance act and has not been done.**

---

## 8. Open governance gaps

| ID | Gap | Category | Resolution required from |
|---|---|---|---|
| GG-1 | Freeze → Activation Eligibility has no resident basis (T6) | GOVERNANCE GAP | Founder |
| GG-2 | AG-08 — no source defines what activation confers or requires | GOVERNANCE GAP | Founder |
| GG-3 | PD-01 P7-I99 requirement set unrecoverable (§5.4 options A–D) | GOVERNANCE GAP | Founder |
| GG-4 | Appointment Register `§3.2` exclusion 22 bars P7-I99 execution; later Acts authorize it. The register was never amended | AUTHORITY-RECORD GAP — same pattern as G-1 | Founder |

**None of these is self-authorized. None is closed by this document.**

---

## 9. Answers this model provides

| Question | Answer |
|---|---|
| What makes PD-01 eligible? | AG-01…AG-10 §7.1 — currently blocked at AG-03, AG-08, AG-10 |
| What makes PD-02 eligible? | AG-01…AG-10 §7.2 — currently blocked at AG-03, AG-08, AG-10 |
| Who may authorize activation? | **Founder only** — `ACT-CC-F03-014 §3` |
| P7-I99 ↔ Freeze? | P7-I99 is the freeze gate, but freeze is also reachable by direct Founder lifecycle determination (§4) |
| Freeze ↔ Activation Eligibility? | **Undefined — GG-1** |
| Eligibility vs Authorization? | Eligibility is evidence; authorization is a Founder decision |
| Volume passes its gate, no Founder authorization? | **The Volume remains NOT ACTIVATED** |

---

## 10. Status

```text
PD-01 Activation ......... NOT EXECUTED       PD-01 Freeze ... FROZEN (lifecycle, GDR-0017)
PD-02 Activation ......... NOT EXECUTED       PD-02 Freeze ... NOT FROZEN
PD-02 P7-I99 ............. NOT EXECUTED
Activation Authority ..... FOUNDER-RESERVED
AIOS ..................... NOT COMPLETE
```
