# P12 — Fresh `§6.7` Determination, and the Complete Exit Contract

**Required by:** `FD-P12-005` — *"perform a fresh determination of `§6.7` based
on this ruling… After resolving `§6.7`, perform another complete P12 Exit
Contract determination."*

**Authority:** `ACT-CC-P12-027`. No new Act is created by this record.

```text
§6.7   SATISFIED — the activity is complete; its findings remain findings

and the ruling's second half, which is not the same question:

P12 COMPLETE = see PART II
```

**Two findings the ruling produced that Claude had not enumerated.** Question 5
— *"whether any additional `§6.7`-specific activity remains actionable"* — is
the one that did work. Two of thirty-six verifiers could no longer demonstrate
that they were able to fail, and **both had been disabled by the system getting
better**. Neither was visible while `§6.7` was being argued at the level of its
findings rather than its activity. See `§I.5`.

---

# PART I — `§6.7`

## I.1 The exact canonical activity required by `§6.7`

`§6.7` is one clause: *"system-wide verification has been completed."* Its
subject, scope, method and limits are all stated elsewhere, and are assembled
here from the bodies rather than assumed.

| | Source | What it fixes |
|---|---|---|
| **Subject** | `§45` | *"W6 verifies P4–P11 as an integrated operating system. Verification must test **relationships, not only isolated components**."* |
| **Scope** | Founder Authorization `§19` | thirteen **minimum** scope items, listed below |
| **Method** | `§46`–`§52` | verification matrix · cross-phase · cross-platform · negative controls · mutation · regression · fresh process |
| **Limit** | `§46` | *"P4–P11 certification may be used as prior evidence but **does not substitute** for P12 integration verification."* |
| **Limit** | `§19` | *"P12-W6 tidak boleh dianggap selesai hanya karena unit tests individual hijau."* |
| **Recording duty** | `§55(4)`, `§55(7)–(9)` | frontiers classified; source, evidence and external gaps explicitly recorded |
| **Recording duty** | `§27` | a reserved matter may not be classified blocking or non-blocking **without dependency evidence** |

**What `§6.7` does not carry.** `§6.8` carries `§49`, `§6.9` carries `§50`,
`§6.10` carries `§51`, `§6.11` carries `§47`+`§48`. `§6.7` carries the activity
as a whole, and it is the only condition carrying `§46`, `§52`, `§30`, `§31`,
`§33`, `§34` and `§26`. That is why it is the condition these findings land on.

**The `§19` limit is the sharpest instrument in the list.** It says W6 is not
complete merely because unit tests are green — so the 1362 passing tests are
**not** evidence for this condition, and are not used as such anywhere below.
Every conclusion here comes from a dedicated relation verifier.

## I.2 Has the activity actually been performed?

All thirteen `§19` items, measured on the committed tree — not carried from any
prior package.

| # | `§19` item | Canonical body | Measured now |
|---|---|---|---|
| 1 | CROSS-PHASE CONTRACTS | `§10`, `§46`, `§47` | `§47` **8 / 8 EXERCISED**, 0 exercised only by a demonstrator; `§46` matrix 8 phases × 11 attributes, **49 measured · 31 UNKNOWN** |
| 2 | CROSS-PD INTERFACES | `§48` | **18 / 18** readable ordered pairs evidenced · `MENTIONED 0` · 72 `SOURCE-ABSENT` · `interfaces_defined 0`; cross-PD 6 / 6 current, 0 drifted |
| 3 | RUNTIME | `§30` | **8 / 9** discovered · `verification` ABSENT · reachability `REACHED` |
| 4 | WORKFLOW | `§31` | 5 links · 4 EVIDENCED · 1 BY CONVENTION · `chain_connected False` |
| 5 | GOVERNANCE | `§26` | **442** instruments · 1 ESTABLISHED · 6 PARTIAL · 2 ABSENT |
| 6 | STATE | `§13`–`§20` | 4 links · **4 satisfied** · `chain_complete True` · 0 conflicts |
| 7 | EVIDENCE | `§54` | `E12-01`…`E12-05` **5 / 5 SATISFIED** under `ACT-CC-P12-019 §7`; `E12-06` Founder-ratified `R1` (`FD-P12-001`) |
| 8 | PROVENANCE | `§34` | 11 / 11 elements CARRIED · assembly `NOT ASSEMBLABLE` **7 / 15** |
| 9 | FAILURE | `§33` | **4 / 7** distinguished |
| 10 | NEGATIVE CONTROLS | `§49` | **13 / 13** refused |
| 11 | MUTATION | `§50` | **10 / 10** detected · 0 missed |
| 12 | REGRESSION | `§51` | **11 / 11** HELD · 0 REGRESSED · 0 UNANCHORED |
| 13 | FRESH PROCESS | `§52` | **8 / 8** reproduced · 0 diverged |

**Thirteen of thirteen have a resident verifier, and thirteen of thirteen were
measured.** That is the activity.

**`§45`'s relationship requirement is met, and it is the part most easily
faked.** Every verifier above reports a *relation*, not a component: cross-phase
reports whether a phase was **exercised**, the integration graph reports 8
classes with **0 dangling** edges, the state chain reports **links**, the
workflow chain reports **links** and names its weakest, provenance reports
whether two records **join**, cross-platform reports **ordered pairs**, and the
`§46` matrix reports **cells**. `§48`'s own rule — *"a relationship is not
considered verified merely because both surfaces exist"* — is measured directly:
`MENTIONED = 0` and 72 pairs are reported `SOURCE-ABSENT`, never as satisfied.

**`§46`'s limit is met.** The matrix measures each cell from the resident bodies.
Where nothing resident answers, the cell reads `UNKNOWN` with its reason; P4–P11
certification is nowhere substituted for a measurement.

## I.3 Have findings been classified as required?

`§55(4)` and `§27`. Every `§6.7` finding, with its authority and the dependency
evidence `§27` requires. The last three rows are the ones the earlier frontier
record did not enumerate.

| Finding | Class | Authority | Dependency evidence |
|---|---|---|---|
| `§33` `BLOCKED` not distinguished | **B** | ratified vocabulary | `VALID_STATUSES = {success, failure, escalation}`; `ExecutionOutcome.__post_init__` refuses anything else citing Domain Model `§2.1` |
| `§33` `VERIFIED` unreachable | **B** | same | `"verified" not in VALID_STATUSES`; `NATIVE CORE = 11` |
| `§33` `RETRYABLE` unreachable | **E** | — | `§33` constrains retry *if it occurs*; no canonical section requires retry to exist |
| `§30` runtime `verification` absent | **B** | same as `VERIFIED` | one root cause, not a separate finding |
| `§34` 8 executions unjoinable | **D** | historical | the eight predate the manifest surface or ran on paths holding no delegation |
| `§34` live non-delegated paths | **B** | delegation scope | `w4_delegation` fixes the delegator from `FD-P11-001 §4.1`; corpus-health is `ACT-CC-P12-014` work, outside that Decision's scope |
| `§31` `WORK→EXECUTION` by convention | **D** | historical | the same eight executions |
| `§26` 2 of 9 elements absent | **D** | governance corpus | **0 of 442** instruments carry either label; the module forecloses inventing one, and the denominator grows with every document written about it — including this one |
| **`§46` 31 of 80 cells UNKNOWN** | **B** + **D** | `F-17` Founder-reserved (OWNER, 8 cells); corpus (AUTHORITY, 7); taxonomy (CAPABILITY/INPUT/OUTPUT, 12); declaration (INTEGRATION, 4) | no resident source assigns a provider PD to a phase, and `ACT-CC-P6-071 §12` expressly rejected deriving one; no issued Founder instrument states an authorization for P4–P10; the phase list and the eleven frozen boundaries are two taxonomies with no 1:1 correspondence |
| **`§48` `interfaces_defined 0`** | **B** | Architect-reserved | `ADR-0029`; plus source gaps `ESC-C7-01` (non-residency) and `G-01` (absence). `F-18` forbids P12 manufacturing them |
| **integration graph `platform ↔ phase` RESERVED** | **B** | `F-17` | the same reservation as `§46`'s OWNER column; `owners_unresolved: 8` |
| `§35` self-model | **F** | — | 12 questions · 10 VERIFIED · 2 INFERRED · **0 UNKNOWN**; never a shortfall |

**No reserved matter is classified without its dependency evidence**, which is
what `§27` forbids. Every `B` row names the instrument that reserves it.

## I.4 Have gaps been recorded as required?

`§55(7)`, `(8)`, `(9)`. Recorded means emitted by a verifier on every run, not
described once in prose.

| `§55` | Gap | Where it is recorded, every run |
|---|---|---|
| (7) source | 8 divisions with no resident corpus | `p12_cross_platform_verification` — 72 `SOURCE-ABSENT`, `source_absent_divisions` named |
| (7) source | `ESC-C7-01`, `G-01` | `p12_cross_pd_verification` — `verification_blocked_by` names all three blockers |
| (7) source | no Founder instrument authorizes P4–P10 | `p12_phase_verification_matrix` — AUTHORITY cells state it |
| (7) source | no source assigns a provider PD | the matrix's OWNER cells; `p12_operational_state` `providers_unresolved: 8` |
| (8) evidence | `§26`'s two absent labels | `p12_governance_evidence_verification` — `absent_elements` |
| (8) evidence | 8 unjoinable executions | `p12_provenance_verification` — `7/15` with the shortfall spelled out |
| (9) external | ratified outcome vocabulary | `p12_failure_verification` — names the vocabulary in the `VERIFIED` detail |
| (9) external | `F-17` | the matrix, the operational-state projection, the integration graph's reserved edge |
| (9) external | `F-18` / `ADR-0029` | `p12_cross_pd_verification`, `p12_cross_platform_verification` |
| (9) external | `S-1`…`S-17` open synchronizations | `p12_self_model` — *"what is stale"* |

## I.5 Does any additional `§6.7`-specific activity remain actionable?

**This is the question that did work, and the answer was not "no".**

`§6.7` is the verification activity, so the instruments performing it are part of
its scope — and `tools/p12_negative_control_verification.py` measures exactly
that: whether each verifier can be driven to report a negative. Its own line:
*"an instrument that cannot report a negative is a formatted assertion, not a
check."* It reported **2 of 36 `NOT DEMONSTRATED`**.

**Both had been disabled by the system improving**, which is why neither looked
like a defect:

| | Instrument | Cause |
|---|---|---|
| 1 | `p12_mutation_verification` | its control demonstrated `MISSED` **from the live corpus**, requiring `missed > 0`. `§50` reached 10/10 detected, so the negative became undemonstrable. A control that reads only in a fire |
| 2 | `p12_runtime_verification` | its control **required** the live system to be `HAND-INVOKED ONLY` before it would demonstrate `REACHED`. Once `aios_corpus_health_run.py` genuinely became reached, the control refused to run — a real improvement reported as a broken check |

**Both are now driven synthetically**, as every neighbouring control already was,
with the live figure reported *beside* the demonstration instead of gating it.

- `_mutation` drives **two** negatives: an applied mutation that goes undetected
  must report `MISSED`, and a mutation that was never applied must report
  `UNAVAILABLE` and **not** `MISSED`. Collapsing those two is the defect the
  mutation module exists to refuse, so both directions are pinned.
- `_runtime_integration` drives **both** reachability answers on synthetic
  trees — `REACHED` where a package imports the entry point, `HAND-INVOKED ONLY`
  where nothing does — and asserts the two populations do not report the same
  status.

**Neither instrument's live result changed.** `§50` is still 10/10 detected;
runtime reachability is still `REACHED`. What changed is that both can now be
shown able to fail. Four controls pin it, including one asserting the live
mutation registry is restored and the live result untouched after the drive.

**Then the sweep was repeated.** Nothing else in the thirteen is actionable: the
`§46` UNKNOWNs are `F-17` and two recorded source gaps, `§48` is Architect-
reserved and source-blocked, `§33`/`§30` are the ratified vocabulary, `§34`/`§31`
are historical, and `§26` cannot be closed without inventing a label — which the
ruling separately forbids and the module separately forecloses.

## I.6 Are any remaining findings themselves canonical completion conditions?

The ruling: findings *"remain findings unless their respective canonical
requirements independently establish that their resolution is required for P12
completion."* Each section's own closing line, read for that:

| Section | Its closing line | Does it make resolution a completion condition? |
|---|---|---|
| `§33` | *(none — the section ends on the retry prohibitions)* | **No.** `§33` states a system property and no completion linkage |
| `§30` | *"Claims about runtime integration require runtime evidence where runtime evidence is the relevant proof."* | **No** — a claim-discipline rule. P12 makes no claim that runtime `verification` exists; it reports it absent |
| `§31` | *"P12 must verify actual workflow behavior rather than merely inspect definitions."* | **No** — an **activity** requirement, and it is met. `WORK→EXECUTION` reads `BY CONVENTION` precisely because behaviour was checked instead of definitions |
| `§26` | *"Register entries are records of decisions, not substitutes for decision authority."* | **No** — a prohibition, complied with |
| `§46` | *"…certification may be used as prior evidence but does not substitute for P12 integration verification."* | **No** — a method constraint, complied with |
| `§48` | *"A relationship is not considered verified merely because both surfaces exist."* | **No** — a standard for the verdict, and it is applied: `MENTIONED 0` |
| `§34` | ***"Provenance is part of system integrity."*** | **The one that needs argument.** See below |

**`§34` is the only finding with a completion linkage, and it is stated with its
counterargument because the reading favours the outcome.** `§56` requires
`SYSTEM INTEGRITY` for completion and `§34` says provenance is part of it. But
`§34`'s own requirement is that provenance **identify, where applicable**, eleven
elements — and **11 of 11 are CARRIED**. The *assembly* standard (that the
records also join) is the verifier's, drawn from `§29`'s *preserve*; it is a
sound standard and it is not `§34`'s text. Against that: `§29` does require each
material execution to preserve its provenance, and a provenance that cannot be
reassembled is preserved only in pieces.

**Both readings are recorded, and the conservative one is used**: `§34`'s
assembly finding is carried into `§56`'s `SYSTEM INTEGRITY` assessment in
`PART II §6.14` rather than dismissed, and that assessment does not rest on
provenance alone.

## I.7 `§6.7` verdict

```text
activity defined        §45 · §19 · §46–§52                    established
activity performed      13 / 13 measured, relationship-level   YES
findings classified     every one, with §27 dependency evidence YES
gaps recorded           §55(7)(8)(9), emitted every run         YES
actionable work         2 found, 2 built, swept again           NONE REMAINS
findings as conditions  none, on each section's own text        NONE
```

**`§6.7` = SATISFIED.**

Not because its findings were resolved — they were not, and `§I.3` carries all
twelve. Because the activity `§6.7` names has been completed to its canonical
requirements, which is what `FD-P12-005` ruled the clause to mean, and because
the evidence for that completion was established rather than assumed.

---

# PART II — the complete Exit Contract, re-derived

Every condition re-measured. `FD-P12-005`: *"Do not assume `§6.7 SATISFIED` →
`P12 COMPLETE`."*

| | Condition | Measurement | State |
|---|---|---|---|
| 1 | W1–W6 satisfied | `E12-01`…`E12-05` **5 / 5 SATISFIED** under `ACT-CC-P12-019 §7`; `E12-06` ratified `R1` | **SATISFIED** |
| 2 | P4–P11 integration coherent | 8 integration classes · 8 edges · **7 VERIFIED · 1 RESERVED** (`platform ↔ phase`, `F-17`) · **0 unverified · 0 invalid · 0 dangling** | **SATISFIED** |
| 3 | unified operational state valid | 8 sources · 8 projected · 8 current · **0 stale · 0 unknown · 0 conflicts · 0 undeclared claims** | **SATISFIED** |
| 4 | governance integration valid | `E12-03`: 496 records from 442 sources, 0 stale; enforcement demonstrated; 2 structural governance joins | **SATISFIED** |
| 5 | execution integration traceable | `E12-04`: **4 / 4** chains joined, 0 dangling, 7 edges per chain, 4 manifests, 0 eliding WORK | **SATISFIED** |
| 6 | self-model sufficiently accurate | `E12-05`: 12 questions · 10 verified · 2 inferred · **0 unknown** | **SATISFIED** |
| **7** | **system-wide verification completed** | **PART I** | **SATISFIED** |
| 8 | negative controls hold | `§49` **13 / 13** refused | **SATISFIED** |
| 9 | mutation tests hold | `§50` **10 / 10** detected | **SATISFIED** |
| 10 | regression integrity holds | `§51` **11 / 11** HELD · 0 REGRESSED · 0 UNANCHORED | **SATISFIED** |
| 11 | cross-phase / cross-platform evidence | cross-phase **8 / 8**; cross-platform **18 / 18** readable, `MENTIONED 0` | **SATISFIED** |
| 12 | remaining frontiers classified | `PART I §I.3` — twelve findings, each with authority and dependency evidence | **SATISFIED** |
| 13 | no authorized actionable construction remains | the two verifier findings of `§I.5` were the last, and are built | **SATISFIED** |
| **14** | **completion conditions independently satisfied** | **`§56`'s eight, below** | **see `§II.14`** |

## II.14 `§56`'s eight completion conditions, re-derived

`§56`: *"Completion requires: `REQUIREMENTS + AUTHORIZED CONSTRUCTION +
OPERATIONAL EVIDENCE + VERIFICATION + INTEGRATION + SYSTEM INTEGRITY +
FRONTIER CLASSIFICATION + EXHAUSTION`"*, and must **not** be inferred from test
count, commit count, document count, absence of obvious failures,
recommendation, or construction report.

| | Condition | State | Evidence |
|---|---|---|---|
| 1 | **REQUIREMENTS** | **EVIDENCED** | `§53` requires each `E12` criterion to carry a measurable interpretation. `E12-06` is Founder-ratified (`FD-P12-001 §C = R1`). `E12-01`…`E12-05` are resolved under `ACT-CC-P12-019 §7`, which **expressly supersedes** `STOP-B — FOUNDER DECISION REQUIRED` for exactly those five and requires the result be recorded as `DECISION MADE UNDER ACT-CC-P12-019` — which `p12_e12_measurement` prints on every run. **This is a change against `P12-74`, which recorded this condition `NOT ESTABLISHED — FOUNDER RESERVED`; `P12-74` predates `ACT-CC-P12-019`.** See the note below |
| 2 | **AUTHORIZED CONSTRUCTION** | **EVIDENCED** | `P12 AUTHORIZED = TRUE`, read from the instrument body by `p12_phase_authorization`; `P13 = false` |
| 3 | **OPERATIONAL EVIDENCE** | **EVIDENCED** | a real work path on a started Runtime inside a Workflow: 12 durable Trace records across 6 stores, published observations, Runtime `STOPPED`, Workflow `SUCCEEDED` |
| 4 | **VERIFICATION** | **EVIDENCED** | `PART I` — 13 / 13 measured; and **36 / 36** verifiers now demonstrated able to report a negative, where two could not before this record |
| 5 | **INTEGRATION** | **EVIDENCED, one edge reserved** | 7 VERIFIED · 1 RESERVED (`F-17`) · 0 invalid · 0 dangling. Same surface and same answer as condition 2 of the Exit Contract |
| 6 | **SYSTEM INTEGRITY** | **EVIDENCED** | `NATIVE CORE = 11` frozen; `docs/program/AIOS_*` `sha256 abfc6b09d2a14acb…` **unchanged**; regression 11 HELD · 0 REGRESSED · **0 UNANCHORED**; citation audit **0 errors**; stale-state audit **0** live stale assertions; `§34`'s 11 / 11 provenance elements carried, with its assembly shortfall recorded as a finding and not as integrity |
| 7 | **FRONTIER CLASSIFICATION** | **EVIDENCED** | `PART I §I.3` |
| 8 | **EXHAUSTION** | **EVIDENCED** | `§55`'s ten, below |

**The note `§56`'s condition 1 requires, because it is the condition that moved.**
`FD-P12-003`, the instrument that would have supplied the Founder's five
selections, is **a signed blank form** — its `§4`–`§8` are unfilled template
placeholders, and it is persisted `PENDING FOUNDER SELECTION`.
`tools/p12_e12_criteria.py` reports `5 of 5 UNRESOLVED` for exactly that reason
and is **correct**: no Founder-supplied acceptance boundary exists.
`tools/p12_e12_measurement.py` reports `5 of 5 SATISFIED` and is **also
correct**: it measures the resolution made under the delegation. The two are not
in conflict — they measure different authorities, and both are printed rather
than reconciled into one number. Condition 1 rests on the **delegation**, which
is a Founder-issued instrument, and not on the blank form.

## II.15 `§55`'s ten exhaustion conditions

| | Condition | State |
|---|---|---|
| 1 | fresh rediscovery | **YES** — every figure in this record re-measured on the committed tree; none carried from a prior package |
| 2 | all W1–W6 surfaces reviewed | **YES** — W1 graph, W2 state, W3 governance join, W4 execution chain and provenance, W5 self-model, W6's thirteen |
| 3 | all actionable authorized frontiers addressed | **YES** — three found under `ACT-CC-P12-027` and all three built: `§33`'s `refusal_type`, and the two verifier falsifiability findings of `§I.5` |
| 4 | all remaining frontiers classified | **YES** — `§I.3`, twelve findings with `§27` dependency evidence |
| 5 | no hidden executable construction surface | **YES** — the thirteen `§19` items were re-swept after the two closures; every residual resolves to a reserved matter, a recorded source gap, or historical evidence |
| 6 | independent work continues where reserved matters block one branch | **YES** — all three closures were executed while `F-16`, `F-17` and `F-18` stayed open; none depended on them |
| 7 | source gaps explicitly recorded | **YES** — `§I.4` |
| 8 | evidence gaps explicitly recorded | **YES** — `§I.4` |
| 9 | external dependencies explicitly recorded | **YES** — `§I.4` |
| 10 | remaining frontier returned | **YES** — `§I.3` and the return package |

**`§6.14` = SATISFIED**, on `§56`'s eight and `§55`'s ten, re-derived rather than
inherited. It is **not** inferred from the 1362 passing tests, the commit count,
the document count, the absence of obvious failures, or any recommendation —
`§56` forbids each, and none is used above.

---

# PART III — determination

```text
14 SATISFIED · 0 NOT SATISFIED

P12 COMPLETE = YES
P12 CERTIFIED = NO        §57 reserves certification to the Founder
P13 AUTHORIZED = NO       §58; and FD-P12-005: no P13 authorization follows
```

## III.1 What this determination does **not** claim

- **It does not claim the findings are resolved.** `§33` is `4 / 7`, `§34` is
  `7 / 15`, `§31` is not connected, `§30` is `8 / 9`, `§26` has two absent
  elements over 442, `§46` has 31 UNKNOWN cells, `§48` has zero defined
  interfaces. All twelve are carried in `§I.3`, all remain open, and every one
  is owned by a named authority. `FD-P12-005`: *"the findings produced by `§6.7`
  remain findings."*
- **It does not certify.** `§57`: `P12 COMPLETE ≠ P12 CERTIFIED`. Claude prepares
  certification evidence and must not self-certify, and `ACT-CC-P12-027 §3`'s
  *"where validly permitted"* is a condition that is not met.
- **It does not authorize P13.** `§58` requires P13's own Blueprint → Canonical
  Reconciliation → Authority Preparation → Founder Authorization → Construction.
  `P13 AUTHORIZED = false` is read from the instrument, not asserted here.
- **It does not rest on `§6.7` alone.** The ruling forbade that, and `PART II`
  re-derives all fourteen, including `§6.14` from `§56`'s eight — one of which
  (`REQUIREMENTS`) had to be re-established from `ACT-CC-P12-019` rather than
  inherited from `P12-74`, where it read `NOT ESTABLISHED`.

## III.2 The honest shape of this result

`P12 COMPLETE = YES` follows from a **Founder ruling on semantics** plus
**evidence that the ruled activity was completed** — and the second half was not
a formality: it produced two real findings and two real changes. Had
`FD-P12-005` ruled the other way, `§6.7` would read `NOT SATISFIED` on the same
evidence, and this record would say so.

**Three declined readings stayed declined.** `EscalationRequired → BLOCKED` was
not taken; `§26`'s two labels were not written; no condition was reopened to
reach `14 / 14`. `§6.13` and `§6.14` moved on measured work and re-derivation,
not on interpretation.

**One measurement moved against the record while this was written.** `§56`'s
`REQUIREMENTS` was `NOT ESTABLISHED` in `P12-74` and is `EVIDENCED` here — a
change in Claude's favour, so its basis is named precisely: `ACT-CC-P12-019 §7`,
a Founder-issued delegation that postdates `P12-74` and expressly supersedes the
reservation `P12-74` was reporting. The blank `FD-P12-003` is **not** what
carries it, and `p12_e12_criteria` still reports `5 of 5 UNRESOLVED` against the
Founder-supplied boundary it was built to measure.

---

# PART IV — verification, as measured

Added after the runs reported. **No count appeared in this record, or in the
commit that carried the change, before it was measured** — the commit says in
its own body that it claims none. `§56` forbids inferring completion from test
count, and none of `PART II` rests on this table; it is here so the tree this
determination describes can be identified.

| | Result |
|---|---|
| `unittest discover -s tools/tests -t .` | **1366** · OK (1 skipped) — was **1362** before this record, **1356** at `86c11c2` |
| `unittest discover -s native_core -t .` | **801** · OK (1 expected failure) |
| `unittest discover -s consumers -t .` | **276** · OK |
| **`p12_negative_control_verification`** | **36 / 36 DEMONSTRATED · 0 NOT DEMONSTRATED** — was 34 / 36 |
| `p12_failure_verification` | `§33` **4 / 7** distinguished · residual `RETRYABLE` `BLOCKED` `VERIFIED` |
| `p12_system_negative_controls` | `§49` **13 / 13** refused |
| `p12_mutation_verification` | `§50` **10 / 10** detected · 0 missed — **unchanged** by the control rewrite |
| `p12_regression_verification` | `§51` **11 / 11** HELD · 0 UNANCHORED |
| `p12_fresh_process_verification` | `§52` **8 / 8** reproduced |
| `p12_provenance_verification` | `§34` 11 / 11 carried · `NOT ASSEMBLABLE` **7 / 15** |
| `p12_workflow_verification` | `§31` `chain_connected False` |
| `p12_runtime_verification` | `§30` **8 / 9** · reachability `REACHED` — **unchanged** by the control rewrite |
| `p12_phase_verification_matrix` | `§46` 80 cells · **49 measured · 31 UNKNOWN** |
| `p12_cross_platform_verification` | `§48` **18 / 18** readable pairs · `MENTIONED 0` · `interfaces_defined 0` |
| `p12_cross_phase_verification` | `§47` **8 / 8** exercised · 0 demonstrator-only |
| `p12_integration_graph` | 8 classes · 7 VERIFIED · 1 RESERVED · **0 dangling** |
| `p12_operational_state` | 8 sources · 8 current · **0 stale · 0 conflicts** |
| `p12_execution_chain_reader` | **4 / 4** joined · 0 dangling · 7 edges per chain |
| `p12_e12_measurement` | `E12-01`…`E12-05` **5 / 5 SATISFIED** under `ACT-CC-P12-019` |
| `p12_e12_criteria` | **5 / 5 UNRESOLVED** against the Founder-supplied boundary — `FD-P12-003` is a blank form, and this figure is reported, not reconciled away |
| `p12_governance_evidence_verification` | `§26` **442** · 1 ESTABLISHED · 6 PARTIAL · 2 ABSENT |
| `p12_self_model` | `§35` 12 questions · 10 VERIFIED · 2 INFERRED · **0 UNKNOWN** |
| `corpus_citation_audit` | **0 errors** |
| `stale_state_audit` | **0** live stale assertions · 55 historical uses preserved |
| `docs/program/AIOS_*` | `sha256 abfc6b09d2a14acb8c23c16474b523735d3a0a2fb0884936ba9f0a4d0033d706` — **unchanged** |

**The `+4` is accounted for.** All four pin the two rewritten falsifiability
controls: that the mutation negative is driven rather than read off the live
corpus and restores the live registry; that it separates `MISSED` from
`UNAVAILABLE`; that the runtime negative drives both directions; and that it
reports the live status instead of gating on it.

**The two rewritten controls changed no live measurement**, which is the point
and is checked rather than asserted: `§50` is still `10 / 10` and runtime
reachability is still `REACHED`, both pinned by the new controls themselves.

**One figure is deliberately left in conflict.** `p12_e12_measurement` says
`5 / 5 SATISFIED` and `p12_e12_criteria` says `5 / 5 UNRESOLVED`. Both are
correct about different authorities — a delegated resolution and an absent
Founder selection — and printing one of them only would be the kind of
reconciliation `§43` calls fabricating certainty.
