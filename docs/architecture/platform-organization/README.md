# Platform Organization — Construction Baseline

> **Status: DERIVED.** Not canonical. Nothing here acquires canonical status by
> being complete, internally consistent, or verified. Canonical status follows
> the applicable authority and change-control mechanism, which this baseline
> does not invoke and cannot supply.

**Track:** B — Platform Organization Construction (`PD-01`…`PD-10`), parallel to
the Main Capability Roadmap (`P1`…`P13`). **PD-01–PD-10 are not Phase 14.**
**Constructed under:** `ACT-CC-P10-1`
**Predecessor baseline:** `ACT-CC-P10-0`
**Date:** 2026-09-04

---

## 1. What this baseline is, and what it is not

`ACT-CC-P10-1` authorized construction of `PD-03`…`PD-10`. Before constructing
anything, this Act measured how much resident evidence exists to construct
*from*. The measurement governs everything below, so it is stated first.

Across **8 platform divisions × 12 required dimensions = 96 cells**, **19 cells
are fully evidenced (20%)**, **8 are partial**, and **69 are absent (72%)**.
Identity and domain purpose are evidenced for all eight. Capability,
Organization, Boundary, Dependency and Change Control are evidenced for
**none**.

```text
DIMENSION          ◆ EVIDENCED   ◐ PARTIAL   ○ ABSENT   (of 8)
Identity                8            0           0
Purpose (domain)        8            0           0
Ownership               3            3           2
Authority               0            2           6
Interface               0            1           7
Lifecycle               0            1           7
Governance              0            1           7
Capability              0            0           8
Organization            0            0           8
Boundary                0            0           8
Dependency              0            0           8
Change Control          0            0           8
                       ──           ──          ──
                       19            8          69
```

> **Corrected 2026-09-05** under `FDE-P10-AUTONOMOUS-EXECUTION-01 §11`, by
> recounting `EVIDENCE-LEDGER.md §2` — the artifact of record for this
> measurement — cell by cell. Three defects: the block listed **`Evidence`**
> where the ledger's twelve dimensions carry **`Purpose (domain)`** (`Evidence`
> is `K-13`, a **Kernel** dimension from §3.2, and does not belong in this
> list); `Ownership` and `Governance` were undercounted; and the prose said
> *"roughly 15"* against a block that summed to 17 and a ledger that counts 19.
> **The measurement is recounted, not re-decided** — no cell in the ledger
> changed, and `D-03`'s decision stands on the corrected figures.

Constructing eight full platform architectures across those dimensions would
require inventing the **72%** that is absent; **80%** of cells are not fully
evidenced. `ACT-CC-P10-1 §44` names that
outcome exactly — `NO EVIDENCE → FALSE CLOSURE` — and `§16` bars
`NEED → CREATE → DECLARE CANONICAL`.

**So this baseline constructs what the evidence supports and marks the rest
absent, per dimension, per division.** That is a smaller deliverable than eight
finished volumes and a more useful one: it is the first resident artifact set
for `PD-03`…`PD-10`, and it makes the absence precise enough to be closed
deliberately rather than discovered again later.

## 2. Artifacts

| Artifact | Function |
|---|---|
| `README.md` (this file) | Baseline, Construction Kernel, Construction Decision Log |
| `EVIDENCE-LEDGER.md` | Evidence provenance · per-PD evidence baseline across the twelve dimensions |
| `PLATFORM-ORGANIZATION-MASTER-MAP.md` | Reconciled structure · PD Maturity Matrix · Cross-PD Reconciliation Matrix |
| `SYSTEMIC-GAP-MAP.md` | Gaps derived from observed reconciliation, not assumed |
| `AUTHORITY-FRONTIER-MATRIX.md` | Per-frontier authority classification and disposition |
| `ADE-P10-G04-DECISION.md` | Architect decision resolving `G-04` (Option A) |
| `divisions/` | `README.md` + one record per CPID, `PD-01`…`PD-10` |
| `VOLUME-SECTION-STATUS-MATRIX.md` | Part/Section status for `PD-03`…`PD-10` (`ACT-CC-P10-C7 §35`) |

## 3. Construction Kernel

Derived from the two resident reference volumes — `PD-01` (45 bodies) and
`PD-02` (50 bodies, FROZEN). **The Kernel is a construction mechanism, not an
authority source** (`§11`).

**Source limitation, recorded rather than worked around.** `§11` specifies the
ingestion sequence `Volume 0 → 0.1 → 0.2 → 0.3 → PD-01`. **Volumes 0, 0.1, 0.2
and 0.3 are not resident** — referenced in three tracked files, present as
none. The Kernel is therefore derived from `PD-01` and `PD-02` alone, and every
dimension it carries is one observable in those two volumes.

### 3.1 Structural pattern (observed, both volumes)

```text
Part A — Platform Identity & Strategic Foundation
Part B — Organization
Part C — Governance
Part D — Operating
Part E — Performance
```

`PD-01`: A1–A10 · B1–B5 · C1–C10 · D1–D10 · E1–E9 (45 bodies).
`PD-02`: A1–A10 · B1–B10 · C1–C10 · D1–D10 · E1–E10 (50 bodies).

Section counts differ between the two references, so **section count is not part
of the Kernel**. The five-part spine is.

### 3.2 Kernel dimensions

| ID | Dimension | Reference anchor |
|---|---|---|
| K-01 | Identity | `A1` — Platform Identity (both volumes) |
| K-02 | Purpose | Part A |
| K-03 | Authority | `A5` — Authority & Mandate (`PD-02 A5 §5`/`§6`/`§8`/`§9`) |
| K-04 | Boundary | Part A / Part B |
| K-05 | Ownership | Part B |
| K-06 | Capability | Part B |
| K-07 | Organizational | Part B |
| K-08 | Governance | Part C (`PD-02 C2`, `C3`, `C8`) |
| K-09 | Operating | Part D (`PD-02 D8 §70` — Architecture Change Control) |
| K-10 | Performance | Part E |
| K-11 | Lifecycle | Part C / governance records |
| K-12 | Integration | `C8` — Cross-Platform Architecture Governance |
| K-13 | Evidence | manifests · review records |
| K-14 | Review | `E`-series · review records |
| K-15 | Change Control | `D8 §70`; `Constitution §3.4` → ADR |

### 3.3 Inheritance rule — resident, not invented

`AIOS_MASTER_ROADMAP_CONSOLIDATED_v1.0.md §5`:

> *"`PD-01` is the Gold Standard Reference Implementation; `PD-02`–`PD-10`
> follow by **domain adaptation, not content copy**. Numeric order is not full
> technical dependency, and dependency is **not** subordination — PD-02 is not a
> parent owner of other platforms."*

and, in the frozen `PD-02` corpus, the same rule stated for construction:
*"PD-03 hingga PD-10 dengan domain adaptation"* · *"tanpa memaksakan metric
PD-02"* (without imposing PD-02's metrics).

So the Kernel supplies **pattern**, never domain content. `COPY → RENAME →
DECLARE NEW PD` is prohibited by `§9` and was not performed.

## 4. Construction Decision Log

| ID | Decision | Evidence | Alternatives | Rationale | Authority | Result |
|---|---|---|---|---|---|---|
| **D-01** | Derive the Kernel from `PD-01`+`PD-02` only | Volumes 0–0.3 absent (3 referencing files, 0 resident) | Wait for Volume 0; reconstruct Volume 0 | Reconstruction would invent the ingestion source `§11` names. Absence recorded instead | Delegated (`§11`) | Kernel §3 |
| **D-02** | Measure evidence density before constructing | `§12`, `§21`, `§44` | Construct first, assess after | Constructing first would have produced eight documents whose evidential basis was unknown until afterwards | Delegated (`§21` G1) | §1 table |
| **D-03** | Construct evidence baselines, not eight full volumes | **19 of 96 cells fully evidenced · 8 partial · 69 absent** *(recounted 2026-09-05; was "~15")* | Full eight-volume construction | Full construction requires inventing the **72%** that is absent — `§44` `NO EVIDENCE → FALSE CLOSURE` | Delegated; the alternative exceeds authority (`§16`) | `EVIDENCE-LEDGER.md` |
| **D-04** | Status **DERIVED** on every artifact | `§27` | PROPOSED; CANONICAL | Derived from resident evidence but carrying no authority mechanism. `VERIFIED ≠ FROZEN`, `ADOPTED ≠ CANONICAL` | Delegated (`§27`) | all artifacts |
| **D-05** | Build the Gap Map from observed reconciliation | `§26.3` | Adopt a predefined twelve-domain list | No gap inventory is resident (P10-0). A predefined list would be an assumed subsystem set, which `§26.3` forbids | Delegated | `SYSTEMIC-GAP-MAP.md` |
| **D-06** | No PD advanced past `EVIDENCE-READY` | `§32` | Mark PDs `CONSTRUCTED` | `CONSTRUCTED` would assert a domain architecture that the evidence does not support | Delegated (`§32`) | Maturity Matrix |
| **D-07** | No external research used | `§14` | Adopt external organizational patterns | Internal evidence was the limiting factor, not pattern availability. External material could not have supplied AIOS domain facts | Delegated (`§14`, `§23` of P10-0) | 0 external records |

## 5. What this baseline does not do

- **No canonical status is claimed or created.** `§15`, `§16`, `§27`.
- **No PD is frozen.** `VERIFIED ≠ FROZEN` (`§18`). No freeze recommendation is made.
- **No organizational runtime is constructed.** `§4`, `§8`. The Native Core holds exactly eleven frozen boundaries and admits no twelfth, and **none is required**: `ADE-P10-G04` (Option A) determined that `Platform Division` — historical alias `Department`, per `ADR-0010` (Approved, FD-6, `GDR-0020`) — is already the Domain Model's organizational entity. What an organizational runtime would now require is an **instance binding a CPID to that existing entity**, not a new boundary. That remains an architectural-tier decision (`GDR-0032` → ACC → ADR) and is **not made here**.
- **No PD is activated.** Only `PD-02` is ACTIVE (`GDR-0036`). `PD-01` remains NOT ACTIVATION-ELIGIBLE.
- **No higher-order source is modified.** Constitution, Canonical Domain Model, Architecture Freeze, both frozen volumes, and every governance record are unchanged.
