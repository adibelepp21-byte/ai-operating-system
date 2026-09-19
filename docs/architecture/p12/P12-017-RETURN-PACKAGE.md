# `FD-P12-003` — consumption report

**STOP-B at the decision-consumption boundary. The instrument is signed; its
five decisions are unfilled.**

---

## A. Executive Result

`FD-P12-003 §24.14` instructs:

> *"If any selection or acceptance boundary in this record is syntactically
> incomplete, contradictory, or cannot be reconciled to the actual canonical
> E12 package, **STOP at that decision-consumption boundary and report the
> exact conflict rather than inventing a value.**"*

`§4`–`§8` — the five sections that carry the decisions — arrived as template
placeholders. **Ten unfilled fields: five `Founder selects:` and five
`Acceptance Boundary:`.** So the chain `§16` fixes cannot start:

```text
FD-P12-003  →  E12-01…E12-05  →  MEASUREMENT  →  VERIFICATION
            →  §54  →  §74-J  →  P12 COMPLETION DETERMINATION
   ✗ stops here
```

```text
E12-01 … E12-05   =  UNRESOLVED (5 of 5)
ACCEPTANCE BOUNDARY = UNAVAILABLE
§54 RECONCILIATION  = UNCHANGED — five Requirement cells remain FOUNDER RESERVED
§74-J               = UNCHANGED — §16 forbids backfilling before the chain runs
P12 COMPLETION      = NOT COMPLETE — same blocker as ACT-CC-P12-016
P12 CONSTRUCTION    = ACTUALLY EXHAUSTED — unchanged (§18)
```

**No value was invented, and no interpretation was selected.**

---

## B. Source-of-truth reading (`§3`)

Actual bodies read before anything was persisted or consumed:

| Source | What was read |
|---|---|
| `FD-P12-003` as issued | the full body, verbatim, including `§4`–`§8`'s placeholders |
| `E12-RATIFICATION-DECISION-PACKAGE.md` | `§B`'s six criterion blocks, `§D`, `§E`, `§H`'s blank instrument |
| `FD-P12-001` | `§4` `E12 = RATIFIED`, `§5` `§C = R1` — the one interpretation already ratified |
| Blueprint v1.0 | `§53`, `§54`, `§56`, `§57`, `§74` |
| `ACT-CC-P12-016` return package | the frontier this decision addresses |

Nothing was established from a filename, identifier, index row, previous ledger,
previous Return Package, search result or inferred interpretation.

---

## C. The exact conflict

Each of `§4`–`§8` reads, verbatim:

```text
Founder selects:

E12-0n
→ [INSERT THE EXACT EXISTING PROPOSED INTERPRETATION IDENTIFIER/TEXT
   FROM E12-RATIFICATION-DECISION-PACKAGE.md]

Founder Decision: RATIFIED

Acceptance Boundary:

[INSERT THE EXACT ACCEPTANCE BOUNDARY CORRESPONDING
TO THE FOUNDER-SELECTED EXISTING INTERPRETATION]
```

| Criterion | `Founder selects:` | `Acceptance Boundary:` | State |
|---|---|---|---|
| `E12-01` | `[INSERT …]` | `[INSERT …]` | **UNRESOLVED** |
| `E12-02` | `[INSERT …]` | `[INSERT …]` | **UNRESOLVED** |
| `E12-03` | `[INSERT …]` | `[INSERT …]` | **UNRESOLVED** |
| `E12-04` | `[INSERT …]` | `[INSERT …]` | **UNRESOLVED** |
| `E12-05` | `[INSERT …]` | `[INSERT …]` | **UNRESOLVED** |

`§22`'s FINAL STATE BLOCK records each as `RATIFIED` and `§23` is signed. **The
authentication is complete and the content is a blank form.** The instrument is
persisted exactly as issued —
[`FD-P12-003-E12-01-05-MEASURABLE-INTERPRETATION.md`](../../governance/acts/FD-P12-003-E12-01-05-MEASURABLE-INTERPRETATION.md)
— and recorded `PENDING FOUNDER SELECTION`, on the precedent `FD-P10-005`'s
first copy set.

---

## D. Why the sole candidate was not adopted

This is the part worth stating plainly, because the shortcut was available and
easy.

`E12-RATIFICATION-DECISION-PACKAGE.md §B` proposes **exactly one** interpretation
per criterion:

| | Proposed interpretation (`§B`, quoted) |
|---|---|
| `E12-01` | *"every material integration edge carries `SOURCE · TARGET · RELATIONSHIP · OWNER · AUTHORITY · CONTRACT · STATE · EVIDENCE · VERIFICATION · LIFECYCLE` (`§9` edge model) and is classified `VERIFIED/UNVERIFIED/BLOCKED/INVALID/STALE/RESERVED/N-A`"* |
| `E12-02` | *"for each state class, `STATE → AUTHORITATIVE SOURCE → PROJECTION → CONSUMER` is established, and no two surfaces claim authority over the same system-wide state"* |
| `E12-03` | *"every resident governance decision is discoverable, and at least one governance decision **constrains runtime behaviour** rather than only describing it"* |
| `E12-04` | *"at least one **real system work** execution traverses the full chain, with each stage evidenced by an execution-produced record, and `WORK` never elided"* |
| `E12-05` | *"each of the twelve returns `VERIFIED`, `INFERRED` or `UNKNOWN` with a named source, and **reverts to `UNKNOWN` when its source is removed**"* |

So an "obvious" value exists for every bracket, and filling them would look like
transcription. It is not transcription — `§B` states the proposals *"have no
standing until ratified"*, and `§11` forbids this office to **choose · rank ·
recommend · merge · hybridise · substitute** an interpretation. Adopting the
only candidate engages at least three of those six.

```text
ONE CANDIDATE ≠ A SELECTION      A FORM ≠ A DECISION
RECOMMENDATION ≠ DECISION        SILENCE ≠ APPROVAL
```

`§B`'s `Current state` cells are also **stale** relative to the corpus — they
record `E12-01 CORRECTED`, `E12-02 PARTIAL`, `E12-04 PARTIAL (2 Trace records)`,
`E12-06 PARTIAL (6 exercised · 2 not)`, all written before `ACT-CC-P12-014`,
`-015` and `-016`. They are **not rewritten** (`§14`); a Founder filling `§4`–`§8`
should know the proposals are current and their state cells are not.

---

## E. What was executed, under `§9` and `§12`

`§9` authorizes eleven actions; `§12` confirms none of them needs a Micro-Act.
The ones that were possible were performed:

| `§9` step | Done? | Evidence |
|---|---|---|
| 1 read the issued decision body | **yes** | verbatim, `§4`–`§8` included |
| 2 extract the five ratified boundaries | **impossible** | there are none to extract |
| 3 persist the decision lineage | **yes** | the instrument, persisted as issued with a provenance block |
| 4 measure `E12-01`…`E12-05` | **blocked** | no boundary to measure against |
| 5 perform required verification | **blocked** | same |
| 6 update the evidence matrix | **blocked** | same |
| 7 reconcile `§54` | **no change possible** | see `G` |
| 8 reconcile `§74-J` | **forbidden before the chain runs** | `§16` |
| 9 determine P12 completion | **unchanged** | see `I` |
| 10 fresh post-decision discovery | **yes** | see `J` |
| 11 continue newly exposed work if authorized | **yes, one item** | see `J` |

**One new instrument, built because `§19` requires the chain to be falsifiable
and there must be something to falsify.** `tools/p12_e12_criteria.py` reads the
instrument on every call, extracts each criterion's selection and boundary,
refuses a placeholder, rejects a selection that does not correspond to `§B`, and
**raises rather than returning a partial map**. It carries no interpretation of
its own, no default and no fallback — asserted by AST: none of `§B`'s
distinguishing phrases appears as a literal anywhere in the module body.

Live output:

```text
E12-01  UNRESOLVED  the selection and the acceptance boundary are an unfilled
                    template placeholder; a form is not a decision
E12-02  UNRESOLVED  …
E12-03  UNRESOLVED  …
E12-04  UNRESOLVED  …
E12-05  UNRESOLVED  …

ACCEPTANCE BOUNDARY UNAVAILABLE
```

The refusal is mechanised, not asserted. It will report `RESOLVED` the moment
`§4`–`§8` are filled, and nothing else will need to change.

---

## F. Falsification — `§19` `F-01` … `F-06`

Each control drives the reader against a **filled** instrument as well, because
five `UNRESOLVED` on the live corpus is also what a reader that parsed nothing
would print. **20 tests, all passing** —
`tools/tests/test_p12_e12_criteria.py`.

| | Attempt | Expected | Result |
|---|---|---|---|
| **F-01** | substitute an unselected interpretation into all five sections | `REJECTED` | **5 / 5 `REJECTED`** against `§B`; `boundaries()` raises |
| **F-02** | remove or invalidate the decision record | `ACCEPTANCE BOUNDARY UNAVAILABLE` | raises on an absent instrument, on the **live** unfilled one (`5 of 5`), and on two competing instruments (*"which governs is a Founder question"*) |
| **F-03** | alter the boundary in a lower-level artifact | lower authority rejected | a filled instrument planted **outside** the curated governance root supplies nothing; a sentinel boundary value proves the returned text comes from the instrument and nowhere else |
| **F-04** | evidence while the boundary is unmet | `NOT SATISFIED` | exercised on `E12-06`, the only criterion with a ratified boundary: abundant evidence, no crossing → `NOT SATISFIED`. The reader itself returns **no result at all** — no `SATISFIED` literal exists in it |
| **F-05** | declare satisfaction without measurement evidence | `NOT VERIFIED` | `measurable: True` on a filled instrument says a measurement is now *possible* and carries no result; the summary exposes no `satisfied` or `result` key to carry one |
| **F-06** | cause the implementation to select an interpretation | `REJECTED` / governance control | no function named `select/choose/pick/rank/ratify/adopt/default/resolve/infer/assume/merge/combine`; the module writes nothing; **and the sole-candidate control**: the package offers exactly one proposal per criterion and the reader still refuses |

Registered in the resident falsifiability ledger: **`33 / 33` instruments
`DEMONSTRATED`**, this one included, with the control driving it both ways.

---

## G. `§54` reconciliation

**No cell changed, and none could.** `§15` requires the distinction
`EVIDENCE COMPLETE ≠ SATISFIED` to be preserved, and it is: the evidence and
verification columns for all five criteria are resident and measured, and the
`Requirement` cells are what is missing.

| Row | `Requirement` | Classification |
|---|---|---|
| `E12-01` | `TBD` — `FD-P12-003 §4` unfilled | **FOUNDER RESERVED** |
| `E12-02` | `TBD` — `§5` unfilled | **FOUNDER RESERVED** |
| `E12-03` | `TBD` — `§6` unfilled | **FOUNDER RESERVED** |
| `E12-04` | `TBD` — `§7` unfilled | **FOUNDER RESERVED** |
| `E12-05` | `TBD` — `§8` unfilled | **FOUNDER RESERVED** |
| `E12-06` | supplied by `FD-P12-001 §5` | **SATISFIED** — 8 / 8, re-verified this Act |

Blueprint `§54` is a canonical source and was **not edited**.

---

## H. `§74-J`

**Unchanged, and deliberately not touched.** `§16`: *"Claude Code shall
re-evaluate `§74-J` only after the five Founder decisions have been consumed…
No completion result may be backfilled before this chain is executed."*

[`P12-74-PART-J-COMPLETION-EVIDENCE.md`](P12-74-PART-J-COMPLETION-EVIDENCE.md)
stands as written under `ACT-CC-P12-016`: seven of `§56`'s eight completion
conditions evidenced, `REQUIREMENTS` not established. This decision did not
establish it.

---

## I. P12 completion state

```text
P12 COMPLETION = NOT COMPLETE
```

Unchanged from `ACT-CC-P12-016`, with the identical blocker: `§56`'s
`REQUIREMENTS` condition needs `§53`'s measurable interpretations, and five of
six remain unratified.

`§17` anticipated this exactly: **`FD-P12-003 ISSUED ≠ P12 COMPLETE`.** The
instrument being issued did not move completion, and the instrument being
*unfilled* did not move it either.

```text
P12 CERTIFICATION = RESERVED (§57) — NOT READY
```

---

## J. Fresh post-decision discovery (`§18`)

Performed after consumption, against current state rather than the prior
inventory.

| Candidate exposed by this decision | Verdict |
|---|---|
| Read, verify and persist the decision lineage (`§9.1`–`§9.3`) | **ACTUALLY ACTIONABLE → executed** |
| A falsifiable consumption reader (`§19` needs a chain to falsify) | **ACTUALLY ACTIONABLE → executed** (`tools/p12_e12_criteria.py`, 20 tests, registered control) |
| Measurement of `E12-01`…`E12-05` (`§9.4`–`§9.6`) | **BLOCKED** — no acceptance boundary exists |
| `§54` / `§74-J` reconciliation (`§9.7`, `§9.8`) | **BLOCKED** by the same, and `§16` forbids backfilling |
| Everything classified by `ACT-CC-P12-016` `P` | **re-verified, unchanged** |
| New requirement · integration gap · contradiction · completion dependency | **none found** |

```text
P12 CONSTRUCTION FRONTIER = ACTUALLY EXHAUSTED   (§18, preserved)
AUTHORIZED ACTIONABLE FRONTIER = ZERO, after the two closures above
```

---

## K. Three further conflicts, reported and not resolved

1. **`§22` states `F-18: UNCHANGED / FOUNDER-RESERVED`.** `F-18` is
   **Architect-reserved** under `ADR-0029`, as `ACT-CC-P12-016 §P` recorded and
   the corpus holds. Which authority reserves `F-18` is not this office's to
   settle. It is untouched under either reading, so nothing turns on it here —
   but a future decision routed to the wrong authority would.
2. **`§23` dates the instrument `17-08-2026`.** Under either reading that
   precedes `ACT-CC-P12-016` — the gate `§1` names as its predecessor — and
   precedes `FD-P12-001` and `FD-P12-002`, both `17 September 2026`. The date
   is preserved as written and no ordering was inferred from it.
3. **`§23` names the Founder "Moriarty"**, where `FD-P12-001 §23` and
   `FD-P12-002 §35` name **"Founder"**. Recorded without inference: this office
   does not adjudicate human identity, and no consequence was drawn. It is
   noted because `tools/p12_knowledge_admission.py` reads `HumanAuthority`
   out of an instrument body, so reviewer identity is load-bearing elsewhere.

None of the three was resolved, worked around, or allowed to change a
classification.

---

## L. Boundary integrity

| | |
|---|---|
| Interpretation selected by this office | **none** — `CLAUDE INTERPRETATION AUTHORITY: NONE`, observed |
| Interpretation invented, combined, ranked or recommended | **none** |
| `§4`–`§8` placeholders | **left exactly as issued**; the instrument is not repaired |
| Blueprint `§53` / `§54` | **not edited** |
| `E12-RATIFICATION-DECISION-PACKAGE.md` | **not edited**; its stale `Current state` cells preserved (`§14`) |
| `§74-J` | **not backfilled** (`§16`) |
| `F-16` / `E12-06` | `FD-P12-001` read, never extended |
| `F-17` · `F-18` · `§57` · `P13` | **unchanged, not self-authorized** |
| Autonomous runtime | **none.** `11 / 11` root entry points `HAND-INVOKED ONLY` |
| Native Core | **11**, unchanged |
| Protected artifacts | `docs/program/AIOS_*` `sha256 abfc6b09d2a14acb8c23c16474b523735d3a0a2fb0884936ba9f0a4d0033d706`, identical; `git status` reports `0` changes |
| Micro-Act | none created (`§12`) |
| Historical evidence | not rewritten (`§14`) |

## M. Repository integrity

| | |
|---|---|
| Files created | `tools/p12_e12_criteria.py` · `tools/tests/test_p12_e12_criteria.py` · `docs/governance/acts/FD-P12-003-E12-01-05-MEASURABLE-INTERPRETATION.md` · this package |
| Files modified | `tools/p12_negative_control_verification.py` (one new control) |
| Files **not** changed | `native_core/**` · `docs/program/**` · `docs/architecture/p11/**` · every Blueprint · `E12-RATIFICATION-DECISION-PACKAGE.md` · `FD-P12-001` · `FD-P12-002` · every prior return package |
| Test suites | `tools` **OK** · `native_core` **OK** (1 expected failure) · `consumers` **OK** |
| Instrument falsifiability | **`33 / 33` DEMONSTRATED** |
| `§49` system negative controls | `13` — `12 REFUSED · 1 ACCEPTED` (`false certification`, Founder-reserved) |
| Regression | `11` classes — `10 HELD · 0 REGRESSED · 1 UNANCHORED` (`quality`, `NOT APPLICABLE`) |
| Citation audit | `0` errors |
| Fresh-process verification | `8 / 8` reproduced, `0` diverged |
| `E12-06` | `SATISFIED` — 8 / 8, re-verified |
| W1 integration | `7 VERIFIED · 0 UNVERIFIED · 1 RESERVED` |
| `§46` matrix | `49 / 80` cells measured |

---

## N. What is required to consume this instrument

For each of `E12-01`…`E12-05`, `§4`–`§8` need their two fields filled:

```text
Founder selects:
  E12-0n
  → <the selected interpretation — e.g. RATIFY AS PROPOSED, or the §B text>

Acceptance Boundary:
  <the boundary the selected interpretation establishes>
```

`E12-RATIFICATION-DECISION-PACKAGE.md §H`'s own instrument frames the choice as
`RATIFY AS PROPOSED` / `RATIFY WITH MODIFICATIONS (specify)` / `DO NOT RATIFY` /
`DEFER`. Which of those applies to each criterion is the Founder's to state.

Once stated, `tools/p12_e12_criteria.py` will report `RESOLVED` and the chain in
`§16` runs without further authority: measurement, independent verification,
`§54`, `§74-J`, and the P12 completion determination.

```text
FOUNDER SELECTS  →  ACCEPTANCE BOUNDARY  →  CLAUDE MEASURES
```

This office did not run that chain backwards.
