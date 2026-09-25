# P13 v0.3 Disposition · `F-1`/`F-2` Correction Gate

**Produced under:** the standing record-keeping duty; **no new Act**
**Trigger:** `FD-P13-005` — **Option B · ACCEPT WITH MODIFICATION**, bounded to `F-1` + `F-2`
**Predecessors:** `P13-001` … `P13-011` · `v0.1` · `v0.2` · `v0.3`

> ## NO CORRECTION HAS BEEN PERFORMED
>
> ```text
> ACT-CC-P13-008   REQUIRED — DOES NOT EXIST
> v0.4             DOES NOT EXIST
> v0.1 · v0.2 · v0.3   UNTOUCHED — all three hashes re-verified
> ```

---

## 1 — The gate, checked

`FD-P13-005 §8`: *"This Founder Decision itself does not constitute the
execution Act for modifying v0.3 … a new bounded execution instrument is
required."*

| Gate step | State |
|---|---|
| `FD-P13-005` issued | **YES** — signed, `FINAL — ISSUED`, 23 Sep 2026 |
| Option B, bounded to `F-1` + `F-2` | **YES** — `§2`, `§7` |
| `ACT-CC-P13-004` · `-005` · `-006` | **SPENT** |
| `ACT-CC-P13-007` | **COMPLETE / SPENT** |
| **`ACT-CC-P13-008`** | **ABSENT** |

```text
RESULT:  STOP — CORRECTION AUTHORITY NOT ESTABLISHED
```

**Four spent instruments now sit in `docs/governance/acts/`**, three of them
titled as revision or correction Acts. None is live. `ACT-CC-P13-007 §3` states
the governing rule: *"The existence of a prior Act in the repository does not
reactivate it."*

## 2 — Preservation, re-verified

```text
v0.1  75775cbd4cdccc0404243beb815e2d52c66b44201d02b98856f8a22d08d4d5f1   MATCH
v0.2  a4095a33610e099bcc0960f27b75a5104b6ab049f065b16bcddea011b89b9c57   MATCH
v0.3  6212a7171fa22cfad23e3625ea62d3191b5ed3cc7391e5d86d6c3a9990b139e2   MATCH
```

**None appended to.** All three carry Founder-recorded hashes (`§9`); an append
breaks them. Re-verified after every write this turn.

## 3 — What the Founder accepted, and what acceptance is not

| | |
|---|---|
| **Accepted** | v0.3 as the **non-canonical working basis** for the next bounded correction (`§2`, `§4`) |
| **Not accepted as** | canonical · a P13 definition · authorization · construction · certification (`§4`) |
| **Architecture** | **neither endorsed nor rejected** — `§3` records only that the two defects lie in the *evidence apparatus*, not the substance |

`§12`: `ACCEPT WITH MODIFICATION ≠ CANONICALIZATION`.

**The acceptance rests on evidence this office produced and on defects this
office reported against its own work.** `§3` lists eleven verified conditions
and then records that the two defects are apparatus-level — which is the finding
`ACT-CC-P13-007 O-07` made, not a softening of it.

## 4 — An arithmetic observation for `ACT-CC-P13-008`

`§6` prescribes four corrected counts:

```text
UPGRADES 1 · DOWNGRADES/PRECISION GAINS 6 · CORRECTIONS 1 · STRUCTURAL 7  =  15
```

**v0.3's ledger carries 16 rows** — `L-01` … `L-16`, counted directly this turn.
The unaccounted row is **`L-02`**, which belongs to a fifth category already
present in v0.3's summary block:

```text
v0.3 line 693:   PROVENANCE STRENGTHENED, CONCLUSION UNCHANGED:  1   (L-02)
```

`L-02` is the corpus-residency change — *"did not re-read"* → *"`NOT FOUND`,
verified by direct search"* — which strengthened **how a fact is known** without
changing **what is known**. It is neither an upgrade nor a downgrade, which is
why it has its own line.

**`§6` already resolves this**, in its own words: *"or an equivalent accounting
representation that **accurately reconciles every ledger row**."* Writing only
the four prescribed numbers would leave the ledger reconciling 15 of 16 — the
very defect `F-2` exists to remove. **Retaining the fifth line satisfies `§6` as
written.**

**Stated as arithmetic, not as a correction to the decision.** Each of the four
prescribed counts is right; they simply do not enumerate the fifth category, and
the clause permitting an equivalent representation is what covers it. **This
observation is not acted on here** — acting on it is `ACT-CC-P13-008`'s work.

## 5 — `§19`'s checkbox polarity

`§19` marks `[X]` on the disposition, the artifact and the two corrections, and
leaves `[ ]` on six rows each **labelled `NOT AUTHORIZED`** — scope expansion,
canonicalization, construction, certification, `GAP-0001` closure, Native Core
modification.

Earlier records used the opposite polarity, marking `[X]` against withheld
items. **Both readings produce the same result here**: all six are not
authorized either way. Recorded so a reader comparing records does not pause
over it. **Nothing done this turn depends on the reading.**

## 6 — What `ACT-CC-P13-008` is specified to do

Already fully specified by the Founder; restated here for the gate, not
expanded.

```text
F-1  preserve the 17-item list, its classifications, and the 7 verified O5
     mappings · remove or qualify the unsupported ESTABLISHED completeness
     claim · state the enumeration is PREP-RECORD · distinguish completeness
     relative to a preparation record from completeness relative to a canonical
     P13 scope · preserve GAP-0001 OPEN/APEX · create no canonical scope by
     wording · MINIMUM textual change                              (§5)

F-2  reconcile every ledger row                                    (§6)

OUT  16 exclusions, from P13 identity redesign to certification    (§7)
VERIFY  12 checks, then a fresh Founder review gate                (§11)
OUTPUT  P13-BLUEPRINT-DRAFT-v0.4-NON-CANONICAL.md, v0.3 immutable  (§8, §10)
```

**No proposed Act body is offered.** The last one prepared (`P13-007` Part B)
was superseded when the Founder transmitted a complete body, and `§8` here names
the instrument without requesting a draft. It can be prepared on request.

## 7 — Register effect

| | |
|---|---|
| `GAP-0001` | **OPEN · APEX** — `§14`: the corrections *"do not constitute a substantive resolution of P13 identity"* |
| Register total | **28** |
| Founder-reserved | **12 listed at `§16`** · 0 decided |
| Architect-reserved | **2 at `§17`** · 0 decided |
| Native Core | **11** — `§15` |
| v0.3 | **ACCEPTED as non-canonical working basis** · returned for bounded correction |

## 8 — Exit state

```text
FD-P13-005             = ISSUED — OPTION B (F-1 + F-2 only)
v0.3 DISPOSITION       = ACCEPTED WITH MODIFICATION · NON-CANONICAL · RETAINED
CORRECTION SCOPE       = F-1 AND F-2 ONLY
CORRECTION AUTHORITY   = ACT-CC-P13-008 — REQUIRED, DOES NOT EXIST
CORRECTION EXECUTION   = NOT AUTHORIZED — STOP per §8

v0.4                   = DOES NOT EXIST
v0.1 · v0.2 · v0.3     = PRESERVED · UNMODIFIED
ACT-CC-P13-004 · -005 · -006 · -007 = ALL SPENT
GAP-0001               = OPEN · STILL THE APEX
REGISTER               = 28
P13 AUTHORIZATION      = NOT GRANTED
P13 CONSTRUCTION       = NOT AUTHORIZED
P13 CERTIFICATION      = NOT AUTHORIZED
NATIVE CORE            = 11
CANONICALIZATION       = FOUNDER RESERVED

NEXT GATE = ISSUANCE OF ACT-CC-P13-008, BY THE FOUNDER
```

**Nothing was corrected, modified, constructed, canonicalized or authorized.**
Neither `F-1` nor `F-2` was touched. No gap closed, no reserved matter decided,
no ledger recomputed in any artifact.

**This record does not authorize the next gate.**
