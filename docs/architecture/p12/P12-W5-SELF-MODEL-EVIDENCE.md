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

## 8. `ACT-CC-P12-007` — the phase authorization state enters the authority surface

[E] `ACT-CC-P12-006` measured `tools/p12_system_negative_controls.py`'s `§49`
control `unauthorized P13 authorization` as **`ACCEPTED`**, with the live
detail: *"no resident surface states P13's authorization status, so nothing
would contradict a claim that it is authorized."*

[D] The diagnosis, and the reason this is a `W5` increment rather than a `W3`
one: `authority()` listed `"phase authorization"` in `founder_reserved` — it
named **who holds** the authority and said nothing about **what was decided**
under it. Those are different facts, and only the second contradicts a false
claim.

### 8.1 The source is the decision body, not a constant

[A] `ACT-CC-P12-007 §3` forbids relying on a filename, identifier, registry
row or prior package, and fixes the chain:

```text
ACTUAL FOUNDER DECISION BODY → ACTUAL P13 AUTHORIZATION STATE → SELF-MODEL
```

[C] `tools/p12_phase_authorization.py` reads
`P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md §37 FINAL STATE TRANSITION`,
which states, as a structured block:

```text
P11            P12                        P13
CERTIFIED =    AUTHORIZED = TRUE          AUTHORIZED = FALSE
TRUE           CONSTRUCTED = FALSE
               OPERATIONAL = FALSE
               VERIFIED = FALSE
               EXHAUSTED = FALSE
               COMPLETE = FALSE
               CERTIFIED = FALSE
```

[E] The instrument is **discovered by its body**, not named by path: the
curated `docs/governance/acts/` root is scanned, and an instrument counts only
if it carries a `FINAL FOUNDER DECISION` section whose own body reads
`Status: ISSUED` **and** a `FINAL STATE TRANSITION` section. Exactly one
resident file qualifies. The superseded
`P12-AUTHORIZATION-FOUNDER-DECISION-PACKAGE-PENDING.md` carries **no**
state-transition section at all, so the determination rests on body content,
not on the word `ISSUED` in a filename.

[E] Issuance is read from inside the decision section because the instrument
**contradicts itself**: line 97 carries stale template text
`Status: PENDING FOUNDER DECISION`, and `§35`'s own body carries
`Status: ISSUED`. `issuance_contradiction()` reports the stale header rather
than quietly winning the argument, so a reader who disagrees with the
persisted determination can see exactly what was overruled.

### 8.2 Unstated is not `FALSE`

[D] The Founder states seven dimensions for P12 and **one** for P13. The six
P13 does not carry are reported as `unstated_dimensions`, never as `False`.
An unauthorized phase is very probably not constructed; *probably* is not a
state a self-model may report. `§9` forbids inferring authorization state, and
the prohibition runs in both directions. For the same reason `P11`, which
states only `CERTIFIED = TRUE`, reports `authorized: None` — **undeterminable,
which is not unauthorized**.

### 8.3 The control now tests a property rather than a spelling

[E] What `§49`'s control was:

```python
if "NOT AUTHORIZED" in value.upper() or "P13" in value:
    return True, True, ...
```

[D] The second clause makes the first dead code: **any** appearance of three
characters reported the system as refusing. The Founder instrument defeats it
twice over — `§38` writes `P12 ≠ P13` as three consecutive lines, and the token
appears in prose throughout. A control a mention satisfies measures spelling.

[C] The control now refuses only when *all* of: a **structured** entry exists
for the entity; its `authorized` is an explicit boolean (`None` is
undeterminable and is **not** read as `False`); that boolean is `False`;
provenance resolves to a real file; and
`tools/p12_phase_authorization_verifier.py` — which imports nothing from the
module that produced the value — independently agrees on all six of `§14`'s
checks. Any failure yields `ACCEPTED`, and
`tools/tests/test_p12_phase_authorization.py` drives it there **six ways** so
the outcome stays measured rather than asserted.

### 8.4 Independent verification

[E] `§14` forbids `writer → same writer helper → self-confirming verifier`.
The verifier derives the Founder-stated state **from the instrument by its own
parse** — locating the block by heading boundaries rather than by splitting the
file into sections — and compares that against what the self-model reports.
Independence is AST-enforced, the discipline
`tools/p12_governance_join_reader.py` already carries.

[E] Its fourth check is the one `AuthorityProvenance` deliberately declines to
make. That type's docstring: *"a resolved citation proves the pointer is real,
not that the cited source supports the claim made about it."*
`provenance supports the claim` reads the cited section of the cited file and
confirms the claimed state is written there. A forged report citing a record
that exists but does not state it fails three of six checks — demonstrated, not
asserted, by `p12_negative_control_verification._phase_authorization_verifier`.

### 8.5 What this does not do

[D] `P13 AUTHORIZED = FALSE` is now **reported**. It was already **true**. No
authority was created, widened, or resolved:

```text
SELF-MODEL REPRESENTATION ≠ AUTHORIZATION
P13 STATUS ≠ P13 AUTHORIZATION ≠ P13 CONSTRUCTION
```

The `false certification` control is **untouched and Founder-reserved**; it
remains `ACCEPTED`, and `§49` is not closed by this increment moving one
control. `F-16`, `F-17`, `F-18`, the `W3` broader-chain authority gap and the
`W6` consumer-measurement finding are all unchanged.
