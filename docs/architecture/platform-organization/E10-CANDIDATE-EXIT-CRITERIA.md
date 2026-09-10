# E10 — Candidate Measurable Phase 10 Exit Criteria

> **Status: SUPERSEDED BY RATIFICATION — 2026-09-10.**
> The Founder ratified measurable Phase 10 exit criteria in
> [`FD-P10-004`](../../governance/acts/FD-P10-004-RATIFICATION-OF-MEASURABLE-PHASE-10-EXIT-CRITERIA.md),
> Status `DECIDED`. **That Decision, not this document, is the measuring
> instrument.** `FD-P10-004` ratifies six criteria under the same identifiers
> `E10-01`…`E10-06`, in the Founder's own and **broader** wording — it adds
> falsification testing to `E10-01`, the Agent-Instance misclassification
> exclusion to `E10-02`, and nine sub-conditions to `E10-06`, none of which
> this document contained. **Where the two differ, `FD-P10-004` governs
> absolutely**, and this file is retained only as the record of what was
> proposed. Verification against the ratified text is recorded in
> [`E10-VERIFICATION-AND-P10-CERTIFICATION-PACKAGE.md`](E10-VERIFICATION-AND-P10-CERTIFICATION-PACKAGE.md).
>
> **Its original status, unaltered:** **PROPOSED — NOT RATIFIED.** Prepared
> under `ACT-CC-P10-003 §17.5` (*"prepare the smallest decision-ready
> package"*). **2026-09-10**
>
> **Ratification authority: Program Owner (Moriarty)** — `Master Program
> Volume V §3`: *"Exit criteria Phase 5-13 **disahkan menjadi kriteria terukur**
> | **Pemilik Program (Moriarty)**."* **This document does not ratify anything
> and is not a decision.**

---

## 1. Why this package exists

`ACT-CC-P10-003` asked for the P10 completion boundary to be **proved from
authoritative sources**. It was — `P10-COMPLETION-BOUNDARY.md` records
**9/9 Blueprint `P10 Exit` criteria** and **10/10 `P10-W8` minimum integration
tests** satisfied.

**And P10 still cannot be declared complete**, because the Blueprint says
*"complete **hanya jika**"* — **only if**, a necessary condition. The sufficient
condition is set elsewhere, and the search for it produced a precise answer.

### 1.1 Every prior phase has ratified measurable criteria. P10 has none.

| Phase | Measurable criteria | Count |
|---|---|---:|
| P5 | `E5-1` … `E5-6` | 6 |
| P6 | `E6-01` … `E6-03` | 3 |
| P7 | `E7-01` … `E7-05` | 5 |
| P8 | `E8-01` … `E8-05` | 5 |
| P9 | `E9-01` … `E9-05` | 5 |
| **P10** | **none — `E10` has zero occurrences repository-wide** | **0** |

**`Volume VIII §3` fixes the sequence:** dependencies at required status →
**exit criteria ratified as measurable** → Progress Tracker updated. And
`FD-P9-002` certified Phase 9 by determining *"`E9-01` through `E9-05` stand
SATISFIED / PASS"*.

**So the missing instrument is named, its author is named, and its form has a
five-phase precedent.** That is a materially better answer than *"no resident
instrument states the sufficient condition"*, which is where the previous cycle
stopped.

## 2. Candidate criteria — derived, not invented

**Each is derived from the Blueprint's own `P10 Exit` list**, expressed in the
measurable form `E9-01`…`E9-05` established. **Evidence already measured is
attached** so ratification can be assessed against fact rather than promise.

| ID | Candidate criterion | Evidence already measured | Would stand |
|---|---|---|---|
| **`E10-01`** | **Department Identity & Population** — the canonical Department population is explicitly established by authoritative source, each with identity, scope, responsibilities and explicit exclusions; no Department exists without an establishing instrument | 2 Departments, `ADR-0003` / `ADR-0008` both **Approved**; records carry all four sections; `P10-W1` determination records the lineage for every inclusion **and exclusion** | **PASS** |
| **`E10-02`** | **Ownership Integrity** — every Capability resolves to exactly one accountable Department (`INV-1`); every Agent Definition to exactly one (`INV-2`); no Capability exists with zero implementers (`INV-14`) | `OwnershipGraph` constructs from records: **0 unowned Capabilities · 0 unowned Agent Definitions · 0 record/nesting disagreements · 0 unimplemented Capabilities** | **PASS** |
| **`E10-03`** | **Work Entry & Capability Selection** — work naming a Capability resolves to its accountable Department and implementing Agent Definition; an unresolvable Capability fails closed | `resolve_work_entry()` — 3/3 Capabilities resolve; unknown Capability raises; **no Work entity introduced** (`Freeze §4`), asserted by test | **PASS** |
| **`E10-04`** | **Department → Execution Continuity** — the chain Department → Capability → Agent Definition → authorized execution path is unbroken and the execution path is the certified one, not a duplicate | `w4_chain` **3 links / 0 defects**; execution proceeds through the `E9-03` runtime-mediated path certified under `FD-P9-002` | **PASS** |
| **`E10-05`** | **Organizational Boundary Integrity** — Departments do not execute, do not own another Department's Capability, and do not acquire authority through implementation | `Freeze §4` forbids Department execution; `INV-1`/`INV-10` enforced by the frozen graph; negative controls present (two Departments claiming one Capability **fails closed**) | **PASS** |
| **`E10-06`** | **Evidence & Verification** — every claim above is reproducible from the repository by a checker that can fail, with negative controls | 272 tool tests · 801 native_core (1 expected failure) · 276 consumers; 5 validators; 3 auditors; **negative controls planted for every new checker this cycle** | **PASS** |

**Six candidates, all measurable, all currently evidenced as PASS.**

## 3. What this package deliberately does not do

**It does not ratify.** `Volume V §3` reserves that to the Program Owner, and
`ACT §17` forbids self-authorization. `P5-4`'s precedent is exactly this shape —
*"Review of measurable Phase 5 exit criteria is **prepared, not finalized**."*

**It does not claim the six are the right six.** They are derived from the
Blueprint's nine `P10 Exit` items and compressed into measurable form; the
Program Owner may add, remove, reword, or reject any of them. **Three of the
Blueprint's nine — workflow, coordination, verification — are folded into
`E10-04` and `E10-06` rather than given their own criteria**, because Phase 9
already certified them and `FD-P9-002 §8` bars re-opening what certification
settled.

**It does not declare P10 complete.** Even with all six ratified and passing,
completion would be a **Founder certification decision** in the `FD-P9-002`
shape — a separate instrument, which `FD-P10-003 §16` keeps separate from
`VERIFIED`.

## 4. The exact decision required

> **Ratify measurable Phase 10 exit criteria under `Volume V §3`** — these six,
> a modified set, or a different set entirely.

**Smallest sufficient action.** Nothing else in P10 is waiting on construction,
authority-over-construction, or a missing source. **This one instrument is what
converts a set of satisfied necessary conditions into a testable sufficient
one.**

## 5. What continues regardless

`AR-002`/`AR-003` (Security and Quality owner-to-CPID bindings, both options
drafted at `G-03`), `AR-004` (Governance Authority, expressly withheld),
`ADR-0029` (Department/Platform-Division semantics), and `AR-005` (`Volume VII`
supply). **None of the four blocks P10 construction**, and none is affected by
this package.
