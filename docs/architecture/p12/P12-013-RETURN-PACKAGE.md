# `ACT-CC-P12-013` — Founder Decision F-16 / E12 · Post-Ratification Resolution

```text
A.  F-16 RESOLVED · E12 RATIFIED · §C = R1 · delegation AUTHORIZED
D.  E12-06 = NOT SATISFIED — 4 of 8 phases consumed by real system work
E.  §74 Part J = EVALUABLE for the first time, and it does not pass
F.  P12 NOT COMPLETE
G.  Certification NOT READY — and Founder-reserved regardless
H.  P12 NOT EXHAUSTED — ratification created a required frontier
```

**The decision did not predetermine this.** `§12`: *"The Founder Decision does
not predetermine which result the evidence will produce."* `R1` asks a stricter
question of evidence that has not changed, and the corpus answers it in the
negative. `§20` closes: *"A successful falsification must not be hidden merely
because it prevents completion."*

**And the result does not qualify the decision.** `E12 RATIFIED` stands exactly
as issued. What changed is that the acceptance boundary is now knowable, and
measuring against it produces a fail rather than a pass.

---

## A. Founder Decision Verification

`§7` of the predecessor Act and `§19.A` require the **actual decision body**,
not an identifier, filename, index, commit message, summary or ledger row.

| Check | Result |
|---|---|
| Decision body read | **yes** — `ACT-CC-P12-013` `§4`, `§5`, `§6`, `§8`, `§22`, `§23`, `§24` |
| **E12 ratification** | **`§4`: "E12 = RATIFIED"** — stated in terms, not inferred |
| **`§C` selection** | **`§5`: "R1 — CONSUMPTION BY REAL SYSTEM WORK"**, under an explicit `FOUNDER SELECTION` heading |
| Alternatives | **`§6`: `R2` = NOT SELECTED · `R3` = NOT SELECTED**, with the prohibition on combining them |
| **Delegated execution** | **`§8`: "AUTHORIZED"**, bounded by *"only the work necessary to measure and verify the consequences of this Founder Decision"* |
| Authentication | **`§23`**: Founder Decision `ISSUED` · Founder Name `Founder` · Date `17 September 2026` · Decision Status `FINAL / ISSUED` |
| Canonical persistence | **`docs/governance/acts/FD-P12-001-E12-RATIFICATION-AND-ACCEPTANCE-BOUNDARY.md`** — persisted this Act with a provenance block recording why it is ISSUED |

**Why this instrument is ISSUED and `ACT-CC-P12-012` was not.** `P12-012`'s
`§32` block came back with every checkbox `[ ]` and every field blank, and was
recorded `NO DECISION ISSUED`. Here **every decision field is answered**:
ratification stated, reading selected, alternatives explicitly not selected,
authorization granted, Founder named, date given, status `FINAL / ISSUED`. A
decision is made by its decision content. The corpus precedent runs the same
way — `FD-P10-005`'s first copy had a blank `§14` and was persisted PENDING.

**`§17` historical integrity.** `E12-RATIFICATION-DECISION-PACKAGE.md` is
**byte-identical** and its `§H` remains blank. It is the historical record of
the pre-ratification state; this instrument, not that one, carries the decision.
Nothing was rewritten to make ratification appear to pre-date it.

```text
BEFORE ACT-CC-P12-013:  E12 NOT RATIFIED · §C NOT SELECTED
AFTER  ACT-CC-P12-013:  E12 RATIFIED     · §C = R1
```

---

## B. E12 Criteria — the authoritative boundary, extracted

**Criterion under measurement:** `E12-06` — System-wide Verification.

**Canonical definition** (`E12-RATIFICATION-DECISION-PACKAGE.md §B`, from
`§19`, `§45`, `§48`): thirteen-item minimum scope; *"must test relationships,
not only isolated components"*; *"not verified merely because both surfaces
exist"*.

**Measurable interpretation — now supplied by the Founder, not proposed:**

> **`R1` — CONSUMPTION BY REAL SYSTEM WORK.** *"The relevant E12 condition is to
> be evaluated through evidence that the relevant capability/state is consumed
> by real AIOS system work."*

**Acceptance chain** (`§5`, verbatim):

```text
REAL SYSTEM WORK → REAL CONSUMPTION → OBSERVATION →
INDEPENDENT VERIFICATION → EVIDENCE → E12-06 DETERMINATION
```

**Exclusion clause** (`§5`, verbatim and load-bearing): *"The existence of a
component, provisioned capability, **demonstrator**, test fixture, or merely
callable surface is not by itself sufficient evidence of consumption by real
system work."*

**No alternative was silently combined.** `R2` and `R3` are recorded
`NOT SELECTED` in the measurement itself, and
`tools/p12_e12_acceptance.phases()` **raises** if pointed at an instrument
ratifying a reading it does not implement — a module that quietly fell back to
a broader rule would be `§9`'s prohibited fourth interpretation.

---

## C. F-13 — freshly re-derived under R1

`§7` required this and stated the Founder Decision *"does not predetermine the
result of that re-derivation"*.

| | |
|---|---|
| **Pre-decision state** (`P12-012 D`) | `RESERVED` — the canon imposed no work/demonstration distinction, and whether one would exist depended on `§C` |
| **What `R1` changes** | `§5` makes a demonstrator **explicitly insufficient**. The distinction is therefore **canonically required wherever `E12-06` acceptance is determined** — it is now load-bearing, where before it was contingent |
| **Is it satisfied where it is required?** | **YES.** `tools/p12_cross_phase_verification` has reported `exercised_only_by_a_demonstrator` since long before ratification, and `tools/p12_e12_acceptance` applies it. The `E12-06` determination in part D **turns on** that distinction and makes it correctly |
| **Where it is still absent** | `p12_self_model.running()` lists `p12-f4-runtime-observation` and `p12-f11-workflow-observation` — both demonstrator subjects — beside `p11-w1-runtime` and the W1/W2/W4 runtimes, **with no distinction**. Measured live, not assumed |
| **Is *that* now canonically required?** | **NO.** `R1` grounds that the distinction matters **for acceptance**; it does not supply a general rule for classifying an arbitrary subject. `E12-05`'s criterion is the twelve questions answered evidence-backed, and `running()` answers with a named scope. The general taxonomy remains ungrounded — `p12_cross_phase_verification`'s own comment says so: *"a list of three known artifacts, not a classification scheme"* |
| **Final classification** | **`PARTIALLY CLOSED`** — closed where `R1` makes it required (the acceptance determination); **`SOURCE-GAP`** in its general form (no canonical rule for classifying an arbitrary subject) |

**`F-13 BEFORE F-16 ≠ F-13 AFTER F-16`** — and here the label genuinely moved:
`RESERVED` → `PARTIALLY CLOSED + SOURCE-GAP`. `P12-012` is not edited.

**`§7`'s "MEASURE ONLY IF REQUIRED"** was honoured: the requirement was found,
and it was measured — that measurement is part D.

---

## D. Measurement

**Instrument:** `tools/p12_e12_acceptance.py`, which reads the ratified boundary
out of the persisted instrument by **body content** (a `§C ACCEPTANCE
INTERPRETATION` section with a `FOUNDER SELECTION`, plus `Decision Status:
FINAL / ISSUED`), never by filename.

| Phase | | Verdict under `R1` | Evidence |
|---|---|---|---|
| `P4` | Runtime | **NOT CONSUMED — demonstrator only** | crossed only by `p12-f4-runtime-observation` |
| `P5` | Intelligence | **CONSUMED BY REAL SYSTEM WORK** | Trace records authored by `engineering-intelligence-instance-001` |
| `P6` | Knowledge | **NOT CONSUMED — no execution ever recorded** | `knowledge_consumed` empty in every Trace record |
| `P7` | Memory | **NOT CONSUMED — no execution ever recorded** | `memory_consumed` empty in every Trace record |
| `P8` | Tools | **CONSUMED BY REAL SYSTEM WORK** | `tools_used`, `skills_used` on real work |
| `P9` | Workflow | **NOT CONSUMED — demonstrator only** | crossed only by `p12-f11-workflow-observation` |
| `P10` | Department | **CONSUMED BY REAL SYSTEM WORK** | delegated actor authored a Trace record |
| `P11` | Organization | **CONSUMED BY REAL SYSTEM WORK** | organizational work runtime observed |

```text
E12-06  =  NOT SATISFIED
           4 of 8 consumed by real system work
           2 not consumed — no execution ever recorded  (P6, P7)
           2 not consumed — demonstrator only           (P4, P9)
```

**Nothing was re-measured to suit the decision.** The same corpus reads
`6 exercised` to the cross-phase verifier and `4 consumed` under `R1`, because
`R1` asks a stricter question of unchanged evidence. A control pins exactly
that: `test_the_underlying_measurement_reported_these_as_exercised`.

**No work was manufactured.** `§10`'s standard — `PROVISIONED ≠ CONSUMED`,
`CALLABLE ≠ EXECUTED`, `EXECUTED ≠ REAL SYSTEM WORK` — is what produced the
fail, and inventing an execution to flip it is what `§20 F-01` exists to catch.

---

## E. `§74` — A–L reconciliation and Part J

`§14` of the predecessor forbids silently overwriting the pre-ratification
package: [`P12-74-RETURN-PACKAGE.md`](P12-74-RETURN-PACKAGE.md) is
**byte-identical**.

| Part | Pre-ratification | Changed by F-16? | Post-ratification |
|---|---|---|---|
| A–I, K, L | EVIDENCED | **no** — all re-derived fresh and unchanged | **EVIDENCED**; part I gains the `F-13` move from part C |
| **J Completion** | **NOT EVALUABLE — blocked by `F-16`** | **YES** | **EVALUABLE — and NOT SATISFIED** |

**Part J, evaluated.** `§56`'s eight completion conditions:

| `§56` condition | State | Evidence |
|---|---|---|
| REQUIREMENTS | **evidenced** | `§74 B`, `§74 I` |
| AUTHORIZED CONSTRUCTION | **evidenced** | `P12 AUTHORIZED = TRUE`; every increment cites its authority |
| OPERATIONAL EVIDENCE | **evidenced** | `§74 D`, `§74 F` |
| **VERIFICATION** | **NOT SATISFIED** | `E12-06` measured against the ratified `R1` boundary: **4 of 8** |
| INTEGRATION | **evidenced** | `§74 C`, `§74 D`, `§74 F` |
| SYSTEM INTEGRITY | **evidenced** | `§74 H`, part I below |
| FRONTIER CLASSIFICATION | **evidenced** | `§74 I`, part H below |
| **EXHAUSTION** | **NOT SATISFIED** | part H — ratification created a required frontier |

**Part J determination: NOT SATISFIED.** Two of eight conditions fail.

**The prohibited shortcut was not taken.** `§11`: `E12 RATIFIED → PART J PASS`
is forbidden; the sequence run was `E12 RATIFIED → R1 AUTHORITATIVE → MEASURE →
VERIFY → EVIDENCE → PART J DETERMINATION`, and `§20 F-06` pins that ratification
and satisfaction do not move together.

---

## F. P12 Completion

```text
P12 NOT COMPLETE
```

**This is a state change, and a determination rather than a deferral.** Before
this Act, completion was `NOT DETERMINABLE` — there was no ratified standard to
measure against. `R1` supplied one, the measurement ran, and the answer is no.

| | |
|---|---|
| Failed condition 1 | **VERIFICATION** — `E12-06 NOT SATISFIED`: `P6` and `P7` consumed by no execution ever recorded; `P4` and `P9` crossed only by demonstrators |
| Failed condition 2 | **EXHAUSTION** — part H |
| Undetermined conditions | none — all eight were evaluated |

`§12` allowed three outcomes and did not predetermine one. `§15` of the
predecessor forbids inferring completion from construction being done, tests
being green, exhaustion, or the Founder having ratified. **None of those was
used**; the determination comes from the measurement in part D.

---

## G. P12 Certification Readiness

```text
NOT READY — and FOUNDER-RESERVED regardless
```

Two independent reasons, either sufficient:

1. **Not ready** — `§13`: certification is consequent on completion, and
   completion is not achieved.
2. **Founder-reserved** — `§57` of the Blueprint and `FD §28`: *"Claude must
   prepare certification evidence but must not self-certify."*

**Remaining Founder-reserved items** unchanged by this Act: `F-17`, `F-18`,
`F-8`, `F-9`, `FDP-P10-001/-002/-003`, `ADP-P10-001`, issuance authenticity,
execution-vocabulary extension, instrument amendment, P12 certification, P13
authorization. `§16` preserved all of them; this decision created no authority
over any.

```text
E12 RATIFIED ≠ P12 COMPLETE      P12 COMPLETE ≠ P12 CERTIFIED
```

---

## H. Exhaustion — revalidated, and it flipped

`§14` forbids inheriting the prior result. Revalidation **reverses it**.

```text
P12 NOT EXHAUSTED
```

**Why.** `P12-011` and `P12-012` established `P12 EXHAUSTED` on the criterion
*"no authorized actionable P12 frontier remains"* — and at that time no
acceptance boundary existed, so nothing required `P6`/`P7` to be consumed or
`P4`/`P9` to be crossed by real work. **`R1` created that requirement.** A
frontier that did not exist before the decision exists after it.

**The remaining required frontier, precisely:**

| Field | Value |
|---|---|
| **Name** | Acquire real system work that consumes `P6` Knowledge and `P7` Memory, and real-work crossings for `P4` Runtime and `P9` Workflow |
| **Canonical requirement** | `E12-06` under the ratified `R1` boundary |
| **Required?** | **YES** — `E12-06` is a `§53` exit criterion and `§56`'s `VERIFICATION` condition depends on it |
| **Authorized by this Act?** | **NO.** `§8` bounds the delegation to *"the work necessary to measure and verify the consequences of this Founder Decision"*. Acquiring new system work is construction, not measurement |
| **Blocked?** | not by authority in principle — by the absence of a construction mandate |
| **`§19` classification** | **EXECUTABLE — REQUIRES A CONSTRUCTION MANDATE** |
| **Executed here?** | **NO.** `§9` forbids exceeding the delegated scope, and manufacturing a crossing to satisfy a metric is what `§20 F-01`/`F-03` exist to catch |

**Fresh discovery also confirms**, unchanged: no newly unblocked frontier beyond
this one, no new evidence gap, no new integration gap, no new authority
dependency, no new contradiction. `§74`'s parts A–I, K, L remain evidenced.

**`P12 EXHAUSTION ≠ P12 COMPLETION`** still holds — and now both are negative,
for the same underlying reason.

---

## I. Integrity

| | |
|---|---|
| **Protected artifacts** | `docs/program/AIOS_*` → `sha256 abfc6b09d2a14acb…`, **identical** before and after; 0 pending changes |
| Certified P10 / P11 evidence | 0 changes |
| `E12-RATIFICATION-DECISION-PACKAGE.md` | **byte-identical**, `§H` still blank |
| `P12-74-RETURN-PACKAGE.md` | **byte-identical** |
| **Native Core** | **11** |
| `§49` system controls | 13 attempted · **12 REFUSED, 1 ACCEPTED** · 0 uncontrolled |
| `§50` mutation | **8 DETECTED, 2 MISSED** |
| `§51` regression classes | **10 HELD, 0 REGRESSED**, 1 `NOT APPLICABLE` — after the defect in `O`-below was corrected |
| **Instrument falsifiability** | 28 → **29 instruments, 29 DEMONSTRATED** |
| `§52` fresh process | **8 / 8 REPRODUCED** |
| W6 STATE chain | **4 / 4 complete** |
| Citation audit | **277 documents, 1655 citations, 0 errors** |
| **Regression** | `native_core` **801 OK** — 800 PASS + **1 EXPECTED FAILURE** (pre-existing) · `consumers` **276 OK** · `tools` **1182 OK** — 1181 PASS + **1 SKIP** (pre-existing). **0 UNRELATED FAILURES · 0 NEW FAILURES.** The run taken *before* the defect below was corrected reported **4 failures**, all of them the dangling citation; the clean re-run after the fix is the figure above, and the red run is reported rather than quietly replaced |
| Repository | `HEAD` `eb5f150` → this commit; `origin` in sync; **0 files modified**, 3 added, 1 modified (`p12_negative_control_verification.py`, to register the new control) |

### Self-introduced defect — disclosed and corrected at source

| | |
|---|---|
| **Defect** | The persisted Founder instrument's provenance block cited `P12-013-RETURN-PACKAGE.md` **before that file existed** — a dangling citation |
| **Caught by** | the resident `§51` `evidence` regression class, which went **`HELD` → `REGRESSED`** on the run immediately after persistence: *"276 documents, 1646 citations, 1 errors"* |
| **Corrected** | by writing this document, which is what the citation points at. `evidence` returns to **HELD**, citations to **0 errors** |
| **Not concealed** | the control worked exactly as designed, and reporting a green suite without saying it had briefly gone red would be the `§20` failure this Act names |

---

## Falsification (`§20`)

| ID | Control | Result |
|---|---|---|
| **F-01** | false consumption claim | **HELD** — `P6`/`P7` reported not consumed, with the reason named; no execution invented |
| **F-02** | provisioned-but-not-consumed | **HELD** — `P6`/`P7` are provisioned by every real runtime and still fail; `R2` is recorded NOT SELECTED, and the module **raises** if pointed at an `R2` instrument |
| **F-03** | demonstrator-but-not-real-system-work | **HELD** — `P4`/`P9` fail on exactly this; the boundary records that demonstrators are insufficient |
| **F-04** | stale evidence | **HELD** — and this is the control that proves `NOT SATISFIED` is *measured*: on synthetic evidence where every phase is crossed by real work the verdict becomes **`SATISFIED`**; one demonstrator is enough to withhold it |
| **F-05** | non-independent verification | **HELD** — the boundary is read from the persisted instrument, not supplied by the module; no instrument → **raises**; an unissued instrument → **refused**; two issued boundaries → **refused** as *"a Founder question, not a parsing one"* |
| **F-06** | false `§74` Part J pass | **HELD** — ratification and satisfaction are pinned apart; the instrument's own `E12 RATIFICATION ≠ E12 PASS` is asserted from its body |
| **F-07** | unauthorized completion inference | **HELD** — the module reports a criterion, never a completion; 0 authority-creating functions; writes nothing |

**19 controls, all passing**, plus a registered falsifiability control that
drives the live verdict both ways.

---

## Governance Invariants (`§21`)

| Invariant | Held by |
|---|---|
| `FOUNDER DECISION ≠ DELEGATED EXECUTION` | the decision was read and persisted, never authored; `R1` was applied, never chosen |
| `RATIFICATION ≠ PASS` | `E12 RATIFIED` and `E12-06 NOT SATISFIED`, simultaneously and consistently |
| `R1 SELECTION ≠ MEASUREMENT` | the selection came from `§5`; the measurement from the corpus |
| `MEASUREMENT ≠ VERIFICATION` | measured in part D, independently falsified in `§20` |
| `VERIFICATION ≠ COMPLETION` | `§56`'s eight conditions evaluated; two fail |
| `COMPLETION ≠ CERTIFICATION` | both negative, for different reasons (parts F, G) |
| `EXHAUSTION ≠ COMPLETION` | both negative; the first flipped *because of* the second's cause |
| `F-13 PRIOR LABEL ≠ F-13 CURRENT REQUIREMENT` | re-derived; `RESERVED` → `PARTIALLY CLOSED + SOURCE-GAP` |
| `EVIDENCE ≠ AUTHORITY` · `AUTHORITY ≠ EVIDENCE` | the instrument grants the boundary; the corpus supplies the verdict; neither substitutes |
| `P12 COMPLETE ≠ P13 AUTHORIZED` | P12 is not complete, and `P13 AUTHORIZED = FALSE` regardless |
