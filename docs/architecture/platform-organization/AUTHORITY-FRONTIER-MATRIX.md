# Authority Frontier Matrix — G-01 … G-08

> **Status: DERIVED.** An authority *classification*, not a resolution. Nothing
> here decides a reserved matter, and no frontier is reported resolved because an
> artifact was created (`§30`).

**Constructed under:** `ACT-CC-FRONTIER-01` · **Date:** 2026-09-04
**Frontier source:** `ACT-CC-P10-1` → `SYSTEMIC-GAP-MAP.md`

---

## 1. Source Recovery Record (`§9`, `§18`) — exhausted, and negative

`§9` gives recovery priority over reconstruction. It was executed first, across
the **entire history**, not the working tree.

| Search | Scope | Result |
|---|---|---|
| Volume 0 / 0.1 / 0.2 / 0.3 | all refs, all commits | **0 paths ever existed** |
| `PD-03`…`PD-10` corpora | all refs, all commits | **0 paths ever existed** |
| Master Map · Encyclopedia · gap inventory | all refs, all commits | **0** — only this Act's own derived artifacts |
| Deletions in `docs/architecture` | full history | **0 — nothing was ever deleted** |
| Renames in `docs/architecture` | full history | 51, all `volume-1/pd-02-…` → `volume-2/pd-02-…` |

**220 commits · 678 distinct paths ever added · 0 deletions.**

### Disposition under `§18`

The absent material is **`REFERENCED BUT NEVER CREATED`** — not deleted, moved,
renamed, historical, or external. The frozen corpora reference a Platform
Encyclopedia and a Master Map that were never written; `§11` of `ACT-CC-P10-1`
named an ingestion sequence whose volumes were never created.

**This changes the resolution path.** Recovery cannot help, so `B. SOURCE
RECOVERY` is unavailable for G-01, G-06 and G-07 — the classification P10-1's
wording invited. **Recovery was attempted and failed; it was not skipped.**

### The established supply mechanism, recovered instead

Both resident PD corpora document how a PD corpus actually arrives:

- **PD-02** — *"The canonical bodies were supplied by the Founder as five `SOURCE TRANSFER BATCH` messages and confirmed complete by the Founder statement `PD-02 A1-E10 COMPLETE`"*, authorized by `ACT-CC-F03-004` (`RESIDENCY-MANIFEST.md:18–21`).
- **PD-01** — *"Architect-supplied Recovery Candidate (`AR-PD01-P7-REC-006`)… supplied directly in the REC-006 Act"* (`RECOVERY-MANIFEST.md:18–26`).

A PD corpus enters by **Founder or Architect source transfer under an
authorizing Act**. That is the precedent, twice, and it is why G-01 is Founder
Action rather than a research task.

## 2. Authority sources (`§4`) — established, not restated

| Matter | Applicable source | Holder | Status |
|---|---|---|---|
| Constitutional tier | `Constitution §3.1`, `§16` | **Architect exclusively**; no delegation permitted | resident |
| Architectural tier | `Constitution §3.2`, `§3.4` → ADR | Architect, boundedly delegable | resident |
| Implementation tier | `Constitution §3.3` | executor | resident |
| **Architecture Authority role** | `APT-CD1.1-AA-001` | **Claude Code / Co-Founder** | **APPOINTED · ACTIVE** (Founder, 2026-08-15) — Constitutional authority **NONE**, amendment authority **NONE**, self-authorization **PROHIBITED**, Founder override **PRESERVED**, **28 explicit exclusions** |
| Volume lifecycle / activation | `GDR-0016`, `GDR-0023`, `GDR-0026 §1` | **Founder-reserved** | resident |
| Platform naming | — | **not established by any resident source** | **absent** |
| Frozen boundary set | `AIOS_NATIVE_CORE_BLUEPRINT` :31 — *"exactly the eleven … no more"* | ratified freeze | resident |

**Two things kept separate that are easily conflated.** The **Architecture
Authority role** (`APT-CD1.1-AA-001`) is appointed, active, and exercisable
within `§3.1`'s ten scopes. **`OB-01`** — *"Through which **actor** is PD-02's
operative authority exercised? A Platform Division is an organizational unit, not
an actor"* — is a different question about the platform division, and remains
**open**. `GDR-0027` is explicit: *"OB-01 does not block the enumeration above;
it blocks **exercise**, not **definition**."*

**Consequence, surfaced here for the first time:** PD-02's activation made
`OA-01…OA-07` *effective* (`OA-07`), and `OB-01` means there is still no
determined actor through which the platform exercises them. Not a contradiction —
`GDR-0027` anticipated exactly this — but it is the reason G-04 matters, and it
belongs on the record.

## 3. Authority Frontier Matrix (`§11`)

Decide / execute / canonicalize / freeze / change are kept distinct (`§11`, `§12`).

| Frontier | Missing evidence | Who may **decide** | Who may **execute** | Who may **canonicalize** | Who may **freeze** | Primary path |
|---|---|---|---|---|---|---|
| **G-01** PD-03…PD-10 corpora | the corpora themselves | **Founder** | Founder (transfer) → Co-Founder (residency) | Founder | Founder | **D — FOUNDER** |
| **G-02** PD-10 naming | precedence rule: frozen corpus vs registry | **Founder** | Co-Founder | Founder | n/a | **D — FOUNDER** |
| **G-03** PD-08 Security | ownership · authority · boundary | **Founder** (source) → **Architect** (boundary) | Co-Founder | Founder | Founder | **D — FOUNDER** |
| **G-04** Org ↔ Runtime bridge | whether organizational runtime is intended | **Architect** (`§3.1 A/C/D`) | Architect / Co-Founder | Architect via ADR | Founder | **C — ARCHITECT · DECIDED** `ADE-P10-G04`, Option A, 2026-09-05. No twelfth boundary required |
| **G-05** Dependency evidence | positive dependency statements | Founder | — | Founder | n/a | **D — FOUNDER** *(dependent on G-01)* |
| **G-06** Volume 0–0.3 | the volumes, or confirmation they are unneeded | **Founder** | Founder (supply) | Founder | n/a | **D — FOUNDER** |
| **G-07** Master Map · Encyclopedia · gap inventory | the canonical artifacts | **Founder** | Co-Founder (derived, done) | Founder | Founder | **D — FOUNDER** |
| **G-08** reference count ≠ definition | none | **Co-Founder** | Co-Founder | n/a | n/a | **A — EXISTING AUTHORITY** |

```text
A  EXISTING AUTHORITY  1      C  ARCHITECT  1      E  BLOCKED  0
D  FOUNDER             6  (one of them dependent on another)
```

**No frontier is BLOCKED.** Every one has an identifiable authority holder —
which is the outcome `§26` asks for, and is not the same as every frontier being
closeable.

## 4. Per-frontier disposition (`§30`)

### G-01 — **READY FOR FOUNDER**
Recovery exhausted (§1). Derived definitions exist (`EVIDENCE-LEDGER.md`) but
canonicalizing them needs authority this Act withholds (`§29`). **Action taken:**
recovery search, supply-mechanism recovery. **Not taken:** construction of
canonical PD definitions — `§13` bars converting insufficient evidence into
canonical definitions to close the frontier. **Decision required:** transfer the
eight corpora, or authorize derived definitions with a named canonical status.

### G-02 — **READY FOR FOUNDER**
Content-anchored per `§14`. The frozen `A4` roster is a **boundary diagram** with
short labels; `MASTER_ROADMAP §5` is a **registry** with official names. Most
differences are brevity. **`PD-10` alone diverges genuinely** — *Enablement* vs
*Experience*, neither a truncation. **No resident source establishes precedence
between a frozen corpus and the program registry**, and `§6.1` bars inventing it,
so no name was selected by technical judgment. **The durable output is the
precedence rule, not the name.**

### G-03 — **READY FOR FOUNDER**
Structurally identical to G-01, with the finding intact: **every other division
that has an ownership statement has one because some frozen section needed to
disclaim ownership *to* it — no section ever needed to for Security.** `§15`
bars declaring a Security authority, ownership model, or boundary because one
appears necessary. **None was declared.**

### G-04 — **DECIDED** *(was READY FOR ARCHITECT)*

> **Conformance repair, 2026-09-05** — under `FDE-P10-AUTONOMOUS-EXECUTION-01
> §11`. The disposition below was accurate when written and is retained
> unaltered; it is superseded, not corrected. The question it poses was answered
> **YES** by `ADE-P10-G04` (Option A, Architect, `APT-CD1.1-AA-001`): `Department`
> is the historical alias of `Platform Division` per `ADR-0010`, so the
> representation already exists, **no bridge and no twelfth boundary are
> required**, and the Founder-escalation branch below never triggers. No new
> decision is made by this note.

The only frontier where the deciding authority is one **I hold**
(`APT-CD1.1-AA-001`, `§3.1 A/C/D`). The architecture question is prior to any
construction: **does `Department` — already resident in
`native_core/core/capability/ownership.py` as the Freeze §4 accountability unit —
already serve as the organizational representation?** If yes, no bridge and no
twelfth boundary is needed. If no, a twelfth core boundary is required, and that
**amends the ratified freeze** — beyond the appointment, whose amendment
authority is **NONE**, and therefore Founder.

**Not decided here** — and correctly so: `§29` expressly withheld "resolve G-04
architecturally", and `§16` barred constructing the bridge because it is
necessary. It was decided afterwards, under its own authority, at
`ADE-P10-G04`. **Prepared:** the
question, the two outcomes, and the escalation trigger.

### G-05 — **READY FOR FOUNDER, dependent on G-01**
Investigated per `§17`: the only resident dependency statements are **negative** —
numeric order is not dependency, dependency is not subordination, *"PD-02 tidak
menjadi owner atas domain tersebut"*. **No positive dependency exists to
surface.** No dependency was declared from apparent logical relation. Nothing is
executable until corpora exist.

### G-06 — **READY FOR FOUNDER** (low severity)
`§18` disposition: **REFERENCED BUT NEVER CREATED**. The Kernel was derived from
`PD-01`/`PD-02` without them, so the practical need is low; the decision is
supply-or-confirm-unneeded. **No document was recreated from memory.**

### G-07 — **READY FOR FOUNDER**
Never existed anywhere (§1). Derived substitutes for all three were produced
under `ACT-CC-P10-1` and each **disclaims being the canonical artifact it
replaces**. Decision: are the derived artifacts the intended objects, or
placeholders for canon still to be supplied?

### G-08 — **RESOLVED**
`§20` validated: the finding is **methodological only**, and is recorded in
`SYSTEMIC-GAP-MAP.md` as a measurement hazard. **No new canonical framework was
created**, as `§20` requires. Within existing authority; closed.

## 5. Construction-Authority Action List (`§25.7`)

Executable now, no further authority required:

1. **G-08** — done.
2. Residency work for any corpus the Founder transfers — manifest, hashes, structural verification. Precedent: both existing manifests.
3. Continued derived analysis under an authorizing Act.

**Not executable at any effort level:** G-01, G-02, G-03, G-05, G-06, G-07 —
each needs source or a decision only the Founder can supply. G-04 needs an
architecture decision that may then need the Founder.

## 6. Frontier Dependency Map (`§25.8`)

```text
G-01  PD corpora ──┬──> G-03  Security definition
                   ├──> G-05  dependency evidence
                   └──> G-02  naming (partially — registry may settle it)

G-04  org↔runtime ──> P10 operationalization      (independent of G-01)
G-06, G-07 ──────────> independent, low severity
G-08 ────────────────> resolved
```

**G-01 is the root.** Three frontiers resolve or shrink the moment it does.
**G-04 is independent** — it can be decided now, and is the only one that can.
