# `ACT-CC-P13-008` — Execution Record

**Authority:** [`ACT-CC-P13-008`](../../governance/acts/ACT-CC-P13-008-V0-3-F1-F2-BOUNDED-CORRECTION-ACT.md) — Founder-issued, FINAL, 23 September 2026
**Result:** `COMPLETE` · `F-1 CORRECTED` · `F-2 CORRECTED` · `EXHAUSTED`

---

## 1–3 — Baseline and hashes (`§25.1`–`§25.3`)

```text
v0.3 REQUIRED  6212a7171fa22cfad23e3625ea62d3191b5ed3cc7391e5d86d6c3a9990b139e2
v0.3 ACTUAL    6212a7171fa22cfad23e3625ea62d3191b5ed3cc7391e5d86d6c3a9990b139e2  MATCH
v0.4 SHA256    00efeeae60a1510ce0e975867f84eb6147d5d97cf01e81d2d163dfb3c9928538
```

Verified **before** any modification (`§4`); `STOP — BASELINE INTEGRITY FAILURE`
not taken. `ACT-CC-P13-008` confirmed the active authority; `-004`, `-005`,
`-006`, `-007` all SPENT and none reused (`NC-06`).

## 4 — `F-1` correction (`§25.4`, `§7`, `§8`)

**Was**, inside the `ESTABLISHED` block:

```text
ESTABLISHED   the seventeen-item list is complete again
```

**Now:**

```text
ESTABLISHED   all seventeen items of the PREPARATION-RECORD enumeration are
              represented again — three were absent from v0.2's table

NOT ESTABLISHED   that seventeen is the canonical P13 scope, or that the
                  enumeration is complete against any canonical definition
```

plus a short note stating `17-ITEM PREPARATION-RECORD ENUMERATION ≠ CANONICAL
P13 SCOPE` and that P13's canonical scope remains `UNKNOWN` within `GAP-0001`.

**`§8` preservation checks — all held.** The seventeen items remain; the
classifications remain; the seven verified mappings remain (`§O5.1` **verified
byte-identical**); no scope redefined; `GAP-0001` untouched; nothing
`UNKNOWN` became fact.

**The correction only weakens.** It replaces a completeness assertion with a
representation statement and adds a denial.

## 5–7 — `F-2` correction and the 16-row reconciliation (`§25.5`–`§25.7`)

| Category | Count | Rows |
|---|---|---|
| UPGRADES | **1** | `L-13` |
| DOWNGRADES / PRECISION GAINS | **6** | `L-01` `L-03` `L-04` `L-11` `L-14` `L-16` |
| CORRECTIONS | **1** | `L-15` |
| STRUCTURAL | **7** | `L-05` `L-06` `L-07` `L-08` `L-09` `L-10` `L-12` |
| **PROVENANCE STRENGTHENED, CONCLUSION UNCHANGED** | **1** | **`L-02`** |
| **TOTAL ACCOUNTED** | **16** | **= ROWS PRESENT** |

**The categorisation was derived from each row's own direction column**, not
read off `§10`'s numbers, and returned `§10`'s figures independently.

`L-02` is retained in its own fifth category and was **not** forced into
another (`§9.1`, `NC-17`). Row-level facts unchanged — only the summary was
stale.

## 8 — Diff summary (`§25.8`)

```text
CHANGED   header (version + authority) · §O5.4 (F-1) · ledger summary (F-2)
          · the prose beneath the counter · new §C · exit state
UNCHANGED O1 O2 O3 O4 O6 O7 O8 O9 O10 §N §S §R §D §Q — all byte-identical
          §O5.1 seven-mapping table — byte-identical
          §O5.2 remaining-ten table — byte-identical
```

### A judgment recorded, not slipped in

`§11` fixes the invariant at `COUNT(L-01 … L-16) = SUM = 16`. **Adding
`L-17`/`L-18` rows for these two corrections would make the ledger reconcile
18 and break that invariant.** The corrections are therefore recorded in a new
**`§C`** section, explicitly outside the `L-` series, leaving the sixteen-row
reconciliation exactly as `§10` prescribes. The reasoning is stated in `§C`
itself rather than left to be inferred.

## 9–10 — Architectural preservation and `O5` (`§25.9`, `§25.10`)

```text
§12 protected sections   14 compared · 0 differ
§O5.1 seven mappings     IDENTICAL — not re-touched
§O5.2 remaining ten      IDENTICAL
```

## 11 — Falsification (`§25.11`, `§19`)

| Test | Result |
|---|---|
| `F-TEST-01` 17 still implies canonical complete scope | **FAILED to falsify** — every surviving mention denies it |
| `F-TEST-02` arithmetic mismatch | **FAILED to falsify** — 16 = 16 = 16 |
| `F-TEST-03` unaccounted row | **FAILED to falsify** — NONE |
| `F-TEST-04` double-counted row | **FAILED to falsify** — NONE |
| `F-TEST-05` `L-02` absorbed | **FAILED to falsify** — its line is present verbatim |
| `F-TEST-06` change outside `F-1`/`F-2` | **FAILED to falsify** — 14/14 identical |
| `F-TEST-07` v0.4 acquired canonical status | **FAILED to falsify** — `NON-CANONICAL` ×4, `GAP-0001 OPEN` |

### A false positive in my own first pass, disclosed

**`F-TEST-02`/`04` initially reported a mismatch and two double-counted rows.**
That result was **wrong, and it was mine**: the first parser counted the
`LEDGER ROWS PRESENT: 16` header as a sixth category and read the range
notation `(L-01 … L-16)` as citing those two ids a second time.

Re-run with the header and range excluded, the invariant holds exactly. **Both
runs are reported.** A falsification tool that reports a defect which does not
exist is itself a defect worth stating — and the correct response was to
re-examine the tool, not to accept whichever answer was convenient.

## 12 — Negative controls (`§25.12`, `§20`)

```text
NC-01 … NC-20     HELD 20 · FAILED 0 · NOT EXERCISED 0 · UNKNOWN 0
```

`NC-16` — *no preparation record converted into canonical scope* — is the one
`F-1` exists to protect, and v0.4 now states the non-equivalence explicitly.

## 13–16 — Preservation, Native Core, `GAP-0001`, authority (`§25.13`–`§25.16`)

```text
v0.1  75775cbd…d5f1  UNMODIFIED      v0.2  a4095a33…9c57  UNMODIFIED
v0.3  6212a717…39e2  UNMODIFIED — re-verified after every write and after commit
NATIVE CORE  11  (measured)          GAP-0001  OPEN · APEX
AUTHORITY    ACT-CC-P13-008 alone; 12 Founder + 2 Architect matters, 0 decided
```

## 17 — Re-discovery (`§25.17`, `§22`)

| Probe | Finding |
|---|---|
| New epistemic ambiguity? | **None.** `F-1`'s replacement adds a denial rather than a claim |
| New arithmetic inconsistency? | **None** — re-verified after the correction |
| Accidental architectural modification? | **None** — 14/14 identical |
| Status drift? | **None** — `NON-CANONICAL` throughout |
| Authority drift? | **None** — sole authority cited is this Act |
| New material defect? | **None.** The only anomaly was the parser false positive, which is in the tooling, not the artifact |

## 18 — Exhaustion (`§25.18`, `§23`)

```text
EXHAUSTED
```

**Clean, and claimed only because no `F-1`/`F-2` defect remains undisclosed**
(`§23`). Both corrections are applied and independently verified; the
invariant holds; no remainder falls inside this Act's scope.

Matters outside this Act — the corpus, the two compound-citation halves,
`GAP-0001`, twelve Founder and two Architect reserved matters — are unchanged
and were never this Act's to exhaust.

## 19–20 — Commit and next gate (`§25.19`, `§25.20`)

Commit recorded in this record's own commit.

```text
NEXT GATE = FRESH FOUNDER REVIEW OF v0.4        (FD-P13-005 §11)
```

---

## `§25`'s required distinctions

**WHAT WAS VERIFIED** — v0.3 baseline; all three predecessor hashes; the 16-row
reconciliation across five categories; `§12`'s fourteen sections byte-identical;
`§O5.1` and `§O5.2` byte-identical; Native Core 11.

**WHAT WAS NOT VERIFIED** — nothing within scope was left unverified. Matters
outside `F-1`/`F-2` were not re-examined and were not meant to be.

**WHAT WAS DOWNGRADED** — the `§O5.4` completeness claim, from an
`ESTABLISHED` assertion to a representation statement plus an explicit denial.

**WHAT EVIDENCE REMAINS MISSING** — unchanged from v0.3: the P13 corpus, and the
corpus halves of `V-5` and `V-7`.

**WHAT WAS NOT TOUCHED** — v0.1, v0.2, v0.3; every architectural section; the
seven `O5` mappings; Native Core; the register; all reserved matters.

**WHAT AUTHORITY REMAINS REQUIRED** — a fresh Founder review of v0.4, then a
separate Founder decision for any canonicalization. Construction, Native Core
change, `AD-P13-001` and `FD-2` are all untouched.

---

```text
ACT-CC-P13-008   = COMPLETE · SPENT
F-1 · F-2        = CORRECTED           v0.4 = NON-CANONICAL
v0.1 · v0.2 · v0.3 = PRESERVED · UNMODIFIED
GAP-0001 = OPEN · APEX   REGISTER = 28   NATIVE CORE = 11
P13 AUTHORIZATION / CONSTRUCTION / CERTIFICATION = NOT GRANTED
```
