# P12-W1 — Phase ↔ PD map reconciliation

> **A new record, not an edit.** The map it reconciles is now protected: P10 is
> certified and `platform-organization/` is its evidence root. The `F-12`
> doctrine applies — *execute freely, persist new evidence to a new location
> rather than rewriting the record certification froze.*
>
> `historical rewrite = 0` · `P12 CONSTRUCTED = FALSE` · `E12 RATIFIED = FALSE`.

---

## 1. `E12-01` was not "NOT BUILT" — I was wrong

My `E12` package recorded `E12-01 System Integration — NOT BUILT`.

`§14` requires: *"Claude **wajib** memetakan `PHASE → CAPABILITY → PLATFORM →
ORGANIZATION → RUNTIME → WORKFLOW → EVIDENCE → VERIFICATION`"* and states
*"Canonical source mensyaratkan explicit Phase ↔ PD capability/dependency
mapping."*

**That artifact is resident and has been since 2026-09-09.**
`PHASE-PD-CAPABILITY-AND-DEPENDENCY-MAP.md` answers the six required questions
*for every phase*, with `UNKNOWN` where unmeasurable and a stated reason for
each.

**The canonical requirement is satisfied. What is stale is three of its rows.**
Reporting `NOT BUILT` was a failure to look before classifying — the error this
programme keeps correcting, made in the document that proposes how to measure
everything else.

---

## 2. The headline finding survives, and that is the substantive result

The map's `§2`: *"zero resident sources assign a Phase to a PD as its
provider."*

**Re-tested against the whole corpus today, including everything P11 and P12
added: still zero.** No instrument issued since — `DP-01`, `FD-P11-001`, `DP-02`,
`FD-P11-002`, the P12 authorization — assigns a Phase to a PD as provider.

The map's negative result is therefore **current**, not merely historical. That
matters more than the three stale rows: the `Provider PD` column is `UNKNOWN` for
every phase because nothing has ever established the relation, and P12's
integration work has not changed it.

---

## 3. Three rows superseded by later fact

| Row | As written 2026-09-09 | Current state | Superseded by |
|---|---|---|---|
| `P10` | **"AUTHORITY-BLOCKED — no Phase 10 authorization instrument exists"** | authorized **and certified** | `ACT-CC-P10-AUTHORIZATION-v1.0.md` (resident); `FD-P10-005 §16` |
| `P11` | *"gated behind P10"* | **CERTIFIED / COMPLETE** | `FD-P11-002 §1` |
| `P12` | *"gated P4–P11"* | **AUTHORIZED**, partially constructed | P12 Authorization `§35` |

**The original rows were accurate on their date.** `P10`'s row is the sharpest
case: *"no Phase 10 authorization instrument exists"* was true when written and
is false now, and the map has no mechanism to notice. That is
`HISTORICAL EVIDENCE ≠ CURRENT STATE` with a date attached.

**Nothing above edits the map.** It is superseded-in-place by this record, which
is how a frozen evidence root is supposed to be updated.

---

## 4. The `Workflow` column, re-measured

Every phase row carries `—` for Workflow except `P9`, which carries *"the Phase
itself"*. Current state adds one measurable fact: a real Workflow lifecycle has
been driven and externally observed (`F-11`), and a real coordination Workflow
has performed work under a delegation (`F-10′`).

That does **not** fill the column. The column asks *which workflow invokes the
phase's capability*, and no Phase → PD provider relation exists to invoke
anything through. **The blank is downstream of `§2`, not independent of it.**

---

## 5. A defect in my own guard, found by this reconciliation

Reading the map required establishing whether `platform-organization/` is
protected. It was **not** — and P10 is certified.

`protected_roots()` mapped phase `N` to `docs/architecture/p{N}`. There is no
`docs/architecture/p10/`; P10's certified evidence, including
`E10-VERIFICATION-AND-P10-CERTIFICATION-PACKAGE.md`, lives under
`platform-organization/`. The loop's `if root.is_dir()` **silently skipped** the
phase and reported success.

**A certified phase's evidence sat unprotected while the guard reported it was
guarding everything.** That is the "guard that passes because it cannot see"
shape, committed inside the guard built to prevent it — the third time I have
written this defect and the second time inside its own countermeasure.

**Corrected:**

- `PHASE_EVIDENCE_ROOTS` declares roots that do not follow the convention —
  **declared, because it cannot be derived**: neither `FD-P10-005` nor
  `FD-P11-002` names a path in its body, and inferring one from identifier
  density is the guess this module refuses.
- An unresolvable certified phase now **raises** `CertificationUndeterminable`
  instead of being skipped.
- A conformance test asserts every certified phase resolves to exactly one root,
  so the declaration is **verified rather than remembered**.

```text
BEFORE   protected: docs/architecture/p11
AFTER    protected: docs/architecture/platform-organization
         protected: docs/architecture/p11
```

Nothing broke: no resident module writes into `platform-organization`; the
citation auditor only reads it.

---

## 6. Verification

```text
native_core 801 OK (1 expected failure) · consumers 276 OK · tools 815 OK = 1892
citation 217 documents / 1162 citations / 0 errors · stale-state 512 / 0
   tools +4 — certified-phase root resolution
protected roots 2 (was 1) · historical rewrite 0 · Native Core 11
E12 RATIFIED = FALSE — nothing here depends on it
```

## 7. Frontier

| ID | Status |
|---|---|
| `E12-01` mapping requirement | **SATISFIED** by a resident artifact — my `NOT BUILT` corrected |
| `F-17` | **OPEN** — `Provider PD` is `UNKNOWN` for every phase because no source establishes the relation. Re-confirmed current, not inherited. Assigning one would be an **Architect/Founder** act, not construction |
| `F-16` | OPEN — Founder-reserved; untouched |

**`F-17` is a boundary, not a task.** The map's `§2` tested the inference and it
was *"rejected on the record"*. Filling the column requires an authority this
office does not hold.
