# P12-W5 — AIOS Self-Model · first construction increment

> **`P12 AUTHORIZED = TRUE`** (Founder P12 Authorization, effective 2026-09-12).
> **`P12 CONSTRUCTED = FALSE`** — `§25`: authorization produces only
> `AUTHORIZED`, and this is one increment, not a work package complete.

---

## 1. Authority trace

| Step | Basis |
|---|---|
| `W5` construction | `D1 = AUTHORIZE P12`; `§10` single bounded `W1`–`W6` mandate |
| Twelve questions | `§18`, verbatim and in order |
| Governance-index change | `§16` governance integration; `§18` requires *"What decisions are recorded?"* evidence-backed |
| No separate Act | `§36`: *"Claude shall not create a new Construction Act merely because this Founder Decision has been issued"*; `§21` no-micro-act rule |

**Nothing here was authorized by necessity.** `§23`: `NECESSITY ≠ AUTHORITY`.

---

## 2. `F-2` closed — the system can now see the decisions that govern it

`DP-01` (P11 Founder Authorization) and `DP-02` (E11 Ratification) were resident,
registered, and **invisible** to the governance index.

```text
BEFORE    records 427 · identified 92 · decisions visible 52 · DP-01 ✗ · DP-02 ✗
AFTER     records 434 · identified 94 · decisions visible 54 · DP-01 ✓ · DP-02 ✓
```

**54 of 54 registered decisions are now visible.**

### It took three edits, and the second and third were found by measurement

The class list was restated in **three** places. Adding `DP` to `IDENTIFIER_RE`
alone moved `records` 427 → 432 and left `identified`, `decisions visible` and
`DP-01` **completely unchanged** — the measurement did not move, which is what
exposed `_SUBRECORD_RE` carrying its own hardcoded copy.

Had I trusted the first edit and reported `F-2` closed, the claim would have been
false in a way no test then existing would have caught. The three lists are now
derived from one tuple, `IDENTIFIER_CLASS_NAMES`, so a class added once reaches
all three.

**This is the same defect the file already documented**: `FD` was itself missing
until `ACT-CC-R1-002`, which *"made every Founder Decision — the highest-authority
record class in the register — invisible to this index."* `DP` was the same
omission, one prefix later, and the drift that made it three edits instead of one
is now removed rather than re-documented.

---

## 3. `tools/p12_self_model.py` — the twelve questions

Built as a **new module**. `derived_views`' docstring records a `§26` prohibition
on building a Self-Model, citing `ACT-CC-R2BC-IMPL-001`, **which is not resident**.
That prohibition can be neither verified nor dismissed, so it is honoured: the
projection there stays a projection, and the self-model P12 authorizes is built
beside it, consuming it as one source among several.

| `§18` question | Status | Source |
|---|---|---|
| What am I? | `VERIFIED` | Native Core structure — 11 frozen boundaries |
| What do I own? | `VERIFIED` | governance index — 434 records, 94 identified |
| What authority do I have? | `VERIFIED` | `DP-01 §8`, `FD-P11-001 §12`, `FD-P10-005 §4`, P12 `§13` |
| What capabilities exist? | `INFERRED` | Department records — 3 declared |
| What is running? | **`UNKNOWN`** | runtime per-process, unobserved |
| What failed? | **`UNKNOWN`** | Trace stores per-`StorageFacility`, no registry |
| What is incomplete? | `INFERRED` | 28 unbridged gates, 1 open escalation |
| What is authoritative? | `VERIFIED` | source hierarchy; candidate architecture **not adopted** |
| What changed? | `VERIFIED` | Register `§4` — 6 recorded supersessions |
| What is stale? | `VERIFIED` | 17 open synchronizations |
| What do I not know? | `VERIFIED` | derived from the answers themselves |
| What decisions are recorded? | `VERIFIED` | Register — 54 |

```text
coverage: 12 questions — 8 VERIFIED · 2 INFERRED · 2 UNKNOWN
```

**The two `UNKNOWN`s are the correct answers**, not gaps in this module. They are
`F-3` and `F-4`, and filling them requires a Trace registry and runtime
observation — real `P12-W2`/`W4` construction, not a better-worded answer here.
`§23`: `MEASUREMENT ≠ PREDICTION`.

**`What do I not know?` is derived, never asserted.** It computes the unanswered
set from the model's own answers, because a hand-kept list of one's own ignorance
is the first thing to go stale — and this programme has corrected that exact class
seven times.

---

## 4. Two defects in this module, found before they shipped

**`capabilities` reported `INFERRED` over an empty tuple.** It passed the
repository root to `read_departments`, which wants the **organization** root. It
found nothing, **raised nothing**, and reported a confident-looking `INFERRED`
with `count: 0` — a guard that passes because it cannot see, wrapped in a
`try/except` that never fired. Fixed to use `ORGANIZATION_ROOT`, and the empty
case is now an explicit `UNKNOWN` with a regression test that mocks it.

**`What changed?` relabelled data as something it was not.** It returned the
staleness fact under the key `recorded_supersessions`; the value was the
open-synchronization list. Supersession is now read from the Register, which is
its authority — **6 recorded**, distinct from the **17** open synchronizations,
and a test asserts the two answers are not equal.

Both were mine, both are recorded, and both have tests written against the defect
rather than the fix.

---

## 5. A pre-existing defect surfaced and fixed

`tools/organization_catalog.py` carried ``ADR-\d{4}`` inside a **non-raw**
docstring — an invalid escape sequence Python had been deduplicating. Reordered
imports surfaced it. I first suspected my own edit; it is **pre-existing and
untouched by me**, confirmed by compiling the `HEAD` version. Ordinary bug fixing
under `§21`. Zero invalid-escape files remain across `tools/`, `native_core/` and
`consumers/`.

---

## 6. Verification

```text
native_core 801 OK (1 expected failure) · consumers 276 OK · tools 741 OK = 1818
   tools +17 — the P12-W5 conformance suite
citation 204 documents / 1096 citations / 0 errors
stale-state 503 documents / 0 stale assertions
Native Core 11 frozen · protected read 0 · staged 0 · committed 0
```

**Negative controls in the suite**, not asserted here: the self-model reports no
authority of its own; reserved matters appear as reserved and never as resolved;
no answer returns a permission; an absent source yields `UNKNOWN` with the absence
named.

---

## 7. What remains

`F-1` partially closed — 10 of 12 questions answered, 2 correctly `UNKNOWN`.
`F-2` **closed**. `F-3`, `F-4`, `F-5`, `F-6` open and **authorized**. `F-7`
external. `F-8` Founder/Architect-reserved, `D2`/`D3` conditional-blocking with no
direct dependency proven by this increment. `F-9` open, non-blocking, untouched.

```text
P12 AUTHORIZED = TRUE    P12 CONSTRUCTED = FALSE    P12 COMPLETE = FALSE
E12 NOT RATIFIED         P13 NOT AUTHORIZED         GOVERNANCE CLOSED = NO
```
