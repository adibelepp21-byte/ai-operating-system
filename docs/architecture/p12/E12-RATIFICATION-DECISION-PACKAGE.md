# `E12` — Founder Ratification · Decision Package

> **STATUS: PREPARED FOR FOUNDER RATIFICATION. NOT ISSUED. NOT RATIFIED.**
>
> **Claude Code has not ratified anything**, has not declared any E12 criterion
> satisfied, has not declared P12 complete or certified, and has not signed as
> Founder. The decision instrument in `§H` is **deliberately blank**.
>
> `CANDIDATE E12 ≠ PROPOSED E12 ≠ PREPARED FOR RATIFICATION ≠ RATIFIED E12 ≠
> MEASURED AGAINST RATIFIED E12 ≠ P12 COMPLETE ≠ P12 CERTIFIED.`

---

## A. Why this package exists

`§53` names six exit criteria and requires each to carry **six elements** —
canonical definition, measurable interpretation, evidence source, verification
method, negative control where applicable, failure semantics — and closes:

> *"No E12 criterion may be silently invented or treated as ratified before
> canonical reconciliation."*

**None of the six currently has a measurable interpretation.** `F-15`
demonstrated the consequence: asked whether two dormant phases constitute a W6
gap, the canon could not answer, because the unit of sufficient evidence is
exactly what ratification would fix. Every remaining W6 question has the same
shape.

`§54`'s evidence matrix is `TBD` in all six rows, and `v1.1` deliberately left it
so. This package proposes filling it — **as a proposal**.

**What this office may and may not do.** `DP-01 §8` and `FD-P11-001 §12` item 9
exclude ratifying exit criteria from the delegation; `DP-02` was the Founder act
that ratified E11 after this office prepared it. The same division applies here:
**prepare, then stop.**

---

## B. The six criteria, with proposed measurable interpretations

Each canonical definition is quoted from the resident instrument. Each
**measurable interpretation is PROPOSED by this office** and has no standing
until ratified.

### `E12-01` — System Integration

| Element | Content |
|---|---|
| Canonical definition | `§14`: map `PHASE → CAPABILITY → PLATFORM → ORGANIZATION → RUNTIME → WORKFLOW → EVIDENCE → VERIFICATION`; *"Phase dan Platform Organization harus tetap dibedakan"* |
| **Proposed** interpretation | every material integration edge carries `SOURCE · TARGET · RELATIONSHIP · OWNER · AUTHORITY · CONTRACT · STATE · EVIDENCE · VERIFICATION · LIFECYCLE` (`§9` edge model) and is classified `VERIFIED/UNVERIFIED/BLOCKED/INVALID/STALE/RESERVED/N-A` |
| Evidence source | derived interface graph; organization records; delegation ledger |
| Verification method | edge-by-edge classification; no edge admitted on existence alone |
| Negative control | an edge whose two surfaces exist but which nothing crosses must classify `UNVERIFIED` |
| Failure semantics | an unclassified material edge is a failure; a `BLOCKED` or `RESERVED` edge is not |
| **Current state** | **NOT BUILT** as a work package. The interface graph exists (14 edges, acyclic) but carries none of the ten edge fields |

### `E12-02` — Unified Operational State

| Element | Content |
|---|---|
| Canonical definition | `§15`: state sources, consumers, lifecycle, staleness, conflict, reconciliation, provenance, cross-phase relationships; *"Claude tidak boleh menciptakan competing system-wide state authority"* |
| **Proposed** interpretation | for each state class, `STATE → AUTHORITATIVE SOURCE → PROJECTION → CONSUMER` is established, and no two surfaces claim authority over the same system-wide state |
| Evidence source | runtime/workflow observations; governance records; organization records |
| Verification method | conflict detection across claimed authorities; freshness classification |
| Negative control | a stale record must not read as current; an empty store must read `UNKNOWN`, never zero |
| Failure semantics | two live authorities over one state class is a failure; an `UNKNOWN` with a named absent source is not |
| **Current state** | **PARTIAL** — 3 observations across two vocabularies with freshness; no unified state model; `P12-W2` boundary still declared-and-guarded rather than built |

### `E12-03` — Governance Integration

| Element | Content |
|---|---|
| Canonical definition | `§16`: preserve `DECISION → AUTHORITY → RATIONALE → IMPLEMENTATION → VERIFICATION → CURRENT STATE`; *"Claude tidak boleh menggunakan P12 sebagai alasan untuk menyelesaikan Founder/Architect reserved matter"* |
| **Proposed** interpretation | every resident governance decision is discoverable, and at least one governance decision **constrains runtime behaviour** rather than only describing it |
| Evidence source | the Register; resident instruments; the certified-evidence guard |
| Verification method | decision visibility measured; enforcement demonstrated against a real attempt |
| Negative control | an attempt to overwrite certified evidence must be refused **loudly**, and a guard that cannot see an unguarded call site must fail its own conformance check |
| Failure semantics | a decision that constrains documents but not behaviour is unintegrated |
| **Current state** | **PARTIAL** — 54/54 registered decisions discoverable; certification enforced for phases `{10, 11}`; `F-12` closed |

### `E12-04` — Execution Integration

| Element | Content |
|---|---|
| Canonical definition | `§17`: `INTENT → DECISION → WORK → EXECUTION → OBSERVATION → VERIFICATION → EVIDENCE`; *"harus membuktikan hubungan antar-surface, bukan hanya keberadaan masing-masing subsystem"* |
| **Proposed** interpretation | at least one **real system work** execution traverses the full chain, with each stage evidenced by an execution-produced record, and `WORK` never elided |
| Evidence source | durable Trace records; published observations |
| Verification method | independent process reads the evidence; `DEMONSTRATOR ≠ SYSTEM WORK` enforced |
| Negative control | a demonstrator's traversal must not satisfy the criterion |
| Failure semantics | a chain missing `WORK` or `OBSERVATION` is incomplete regardless of test results |
| **Current state** | **PARTIAL** — durable Trace live (2 records); one real work path reaches observation, read across a process boundary (`F-10′`) |

### `E12-05` — AIOS Self-Model

| Element | Content |
|---|---|
| Canonical definition | `§18`: twelve questions answered evidence-backed; `SELF-MODEL ≠ AUTHORITY`; it *"tidak dapat mengotorisasi dirinya sendiri"* |
| **Proposed** interpretation | each of the twelve returns `VERIFIED`, `INFERRED` or `UNKNOWN` with a named source, and **reverts to `UNKNOWN` when its source is removed** |
| Evidence source | governance index; Trace registry; observation registry; organization records |
| Verification method | answer each with its source; prove reversion against emptied evidence roots |
| Negative control | no answer returns a permission; an absent source must not be filled in |
| Failure semantics | a `VERIFIED` answer that survives removal of its source is fabricated |
| **Current state** | **BUILT** — 12 questions, `10 VERIFIED · 2 INFERRED · 0 UNKNOWN`, reversion proved. `[U]` `F-13`: the answer does not distinguish work subjects from demonstration subjects |

### `E12-06` — System-wide Verification

| Element | Content |
|---|---|
| Canonical definition | `§19` thirteen-item minimum scope; `§45` *"must test relationships, not only isolated components"*; `§48` *"not verified merely because both surfaces exist"*; *"tidak boleh dianggap selesai hanya karena unit tests individual hijau"* |
| **Proposed** interpretation | **the open question `§C` puts to the Founder** |
| Evidence source | execution-produced records only |
| Verification method | per-phase exercise classification; demonstrator provenance reported |
| Negative control | against an empty evidence store, **nothing** classifies as exercised while every surface still exists |
| Failure semantics | **undetermined — see `§C`** |
| **Current state** | **PARTIAL** — cross-phase contracts addressed: `6 exercised · 2 not · 0 unknown`, with `P4`/`P9` demonstrator-only. Cross-PD interfaces, mutation, regression and fresh-process remain unbuilt at phase level |

---

## C. The question `F-15` could not answer

**Must a canonical phase be exercised for `E12-06` to be satisfied, and what
counts as exercise?**

Measured facts, not arguments:

- `P6` Knowledge and `P7` Memory are **provisioned by every real runtime** and
  **consumed by no execution ever recorded**.
- Their consumer agents are complete and conformance-tested, with **zero
  resident non-test callers**.
- The two resident work paths have no semantic need of either.

```text
PROVISIONED ≠ CONSUMED
NOT EXERCISED ≠ FAILED
ABSENCE OF EXECUTION EVIDENCE ≠ EVIDENCE THAT EXECUTION SHOULD HAVE OCCURRED
```

Three readings, none of which this office may select:

| | Reading | Consequence |
|---|---|---|
| `R1` | exercise means **consumption by real system work** | `P6`/`P7` unsatisfied; P12 must acquire work that needs them, or they stay open |
| `R2` | exercise means **provisioning by a real execution** | `P6`/`P7` satisfied today; the criterion is weaker than `§48` suggests |
| `R3` | **dormancy is legitimate** — a phase is exercised when work requires it, and absence of such work is not a defect | `P6`/`P7` classify `NOT APPLICABLE` rather than failing |

`[R]` **This office's recommendation: `R3`, bounded.** It is the only reading
consistent with `NOT EXERCISED ≠ FAILED` and with `§30`'s conditional — *"where
runtime evidence is the relevant proof"*. `R1` would make P12 completion depend
on inventing work to satisfy a metric, which `§14` of the governing Act
prohibits. `R2` would license *existence-adjacent* evidence that `§48` refuses.
**This is a recommendation, not a decision.** `RECOMMENDATION ≠ DECISION`.

---

## D. Also reserved, and not proposed here

`E12` ratification does not resolve `FDP-P10-001` Security, `FDP-P10-003`
Governance Authority, `ADP-P10-001`, or the Canonical Architecture candidate
adoption. Each remains as `D2`/`D3`/`D4` of the P12 authorization left them.

---

## E. What ratification would and would not do

Ratifying `E12` would fix the **acceptance boundary**. It would **not** declare
any criterion satisfied, P12 complete, P12 certified, or P13 authorized —
exactly as `DP-02 §10` held for E11: **`RATIFICATION ≠ PASS`.**

---

## F. Current P12 state

```text
P12 AUTHORIZED = TRUE   CONSTRUCTED = FALSE   OPERATIONAL = FALSE
VERIFIED = FALSE        EXHAUSTED = FALSE     COMPLETE = FALSE
E12 RATIFIED = FALSE    P13 AUTHORIZED = FALSE
```

## G. Open frontiers at preparation

`F-16` this package · `F-13` work vs demonstration subjects · `F-14` two work
paths publish nothing · `W1` not built · `W2` partial · `W6` partial.

---

## H. Founder decision instrument — **deliberately blank**

```text
E12 RATIFICATION:
  [  ] YES — RATIFY AS PROPOSED
  [  ] YES — RATIFY WITH MODIFICATIONS  (specify)
  [  ] NO  — DO NOT RATIFY
  [  ] DEFER

§C EXERCISE READING:
  [  ] R1 consumption by real system work
  [  ] R2 provisioning by a real execution
  [  ] R3 dormancy legitimate / NOT APPLICABLE
  [  ] OTHER (specify)

MODIFICATIONS:      ______________________________
FOUNDER RATIONALE:  ______________________________
EFFECTIVE DATE:     ______________________________
FOUNDER SIGNATURE:  ______________________________

STATUS: PENDING FOUNDER DECISION
```

**No box is ticked, no date entered, no signature present.** This office
prepared the decision and stops here.
