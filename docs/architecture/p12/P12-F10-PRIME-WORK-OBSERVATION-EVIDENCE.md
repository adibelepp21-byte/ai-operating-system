# P12-W4 `F-10′` — the work ↔ observation relationship, proven with real work

> **`F-10′ CLOSED — VERIFIED`.** `P12 CONSTRUCTED = FALSE` — a frontier result
> is not a phase result. `historical rewrite = 0` · `native_core changes = 0`.

---

## 1. Actual body — and a correction to my own attribution

I attributed `F-10′` to `W6` (`§45`, `§48`). Reading `§19`'s **minimum
verification scope** shows the attribution was weaker than claimed:

```text
CROSS-PHASE CONTRACTS · CROSS-PD INTERFACES · RUNTIME · WORKFLOW · GOVERNANCE
STATE · EVIDENCE · PROVENANCE · FAILURE · NEGATIVE CONTROLS · MUTATION
REGRESSION · FRESH PROCESS
```

**`OBSERVATION` is not in that list.** The requirement lives in **`§17` W4**, and
it is imperative:

> *"P12 execution integration **harus membuktikan hubungan antar-surface**, bukan
> hanya keberadaan masing-masing subsystem."*

— must **prove the relationship between surfaces**, not merely that each
subsystem exists. The canonical chain places `OBSERVATION` between `EXECUTION`
and `VERIFICATION`, so an execution that skips it has not completed the chain.

**The gap was real; my grounding for it was not.** `§48` supports the reading but
never names observation. Corrected here rather than left to stand because the
clause a frontier rests on determines what would close it.

---

## 2. What was insufficient, restated exactly

Every observation surface was reached only by a proof written to demonstrate it.
A demonstrator performs no work, so it establishes that a surface **functions**
and can never establish that the system's work **reaches** it.

```text
DEMONSTRATOR ≠ SYSTEM WORK
```

---

## 3. What was done

`w1_coordination_proof.py` — the **resident W1 work path**, which drives a real
`AIOSRuntime` through a real `Workflow` with a real participating Agent — now
publishes observation from inside the work itself. Two publishes while `RUNNING`
(after start, and after the coordination completes), one after `stop()`.

`p12_w4_observed_work_proof.py` runs that path with **`persist=False`**,
importing `perform` and `coordinate` rather than reimplementing them. Had it
reimplemented the work it would have become another demonstrator — the exact
failure it exists to avoid.

**`persist=False` is what `F-12` bought.** The guard refuses *writes*, not
*executions*, so the work can run without rewriting certified P11 evidence. The
ordering the previous increment predicted held: `F-12` had to close first.

---

## 4. The proof

```text
real system work
  act ACT-CC-P11-011 · goal w1-coordination-proof · delegation ACTIVE
  proof_level REAL-RUNTIME · runtime_id p11-w1-runtime
  completed_steps ['review-open-items', 'summarize-diffs']
  observation_published True

independent process reading the observation
  found True · runtime_id p11-w1-runtime · state STOPPED · TERMINATED
  writer_pid 822 · observer_pid 823

real work performed              True
work reached observation surface True
crossed a process boundary       True  (written by 822, read by 823)
```

Real coordination work was performed, its runtime reached the observation
surface, and a **different process** read it back.

---

## 5. What is *not* claimed, and the measurement that decided it

The first version started a poller **before** the work and waited for a live
catch. It never caught one. The reason is measured, not guessed:

```text
+   0.0 ms   RuntimeState.RUNNING
+   0.6 ms   RuntimeState.RUNNING     (after the coordination completed)
+   0.9 ms   RuntimeState.STOPPED
RUNNING window = 0.9 ms
```

**No external poller can reliably sample a 0.9 ms window.** Widening it by
holding the runtime open would manufacture the observability under test, and the
governing Act says plainly: *"do not fake a long-running process."*

So the claim is narrowed to what the evidence supports:

```text
LIVE CATCH ≠ WORK ↔ OBSERVATION RELATIONSHIP
```

The relationship `§17` requires is proven. A live external catch of this work is
**not achievable at its duration**, and that is a property of the work, not a
missing capability. A test asserts the proof does not later acquire the
overclaim.

---

## 6. Defects in this increment

| Defect | Class |
|---|---|
| `F-10′` attributed to `W6 §45/§48`; `OBSERVATION` absent from `§19` scope | **INTRODUCED** (mine, prior Act) · **CORRECTED** · the gap survives on `§17` |
| First proof asserted a live catch and failed | **TRANSIENT** · replaced by a measured, narrower claim |
| `evidence["coordination_facts"]` — wrong key; facts live under `coordination` | **TRANSIENT** · my probe error, corrected by reading the structure |

---

## 7. Negative controls

| Attack | Result |
|---|---|
| certified P11 evidence written during an observed run | **HELD** — `persist=False`; `git` shows zero p11 changes |
| `F-12` guard bypassed or weakened to enable this | **HELD** — guard still refuses; `w1_coordination_proof.py` with persist still exits 1 |
| observation written into a certified root | **HELD** — `is_protected(OBSERVATION_ROOT/…)` is false |
| terminated observation reported as running | **HELD** — `p11-w1-runtime` appears in `terminated`, never in `live_by_kind` |
| work path silently losing its publish calls | **HELD** — AST test requires ≥ 2 `publish` calls |
| the entry point reimplementing the work | **HELD** — imports `perform`/`coordinate`; test asserts the work path uses a real participating Agent |

`attempted 6 · held 6 · missed 0`.

---

## 8. Fresh rediscovery

| ID | Frontier | Status |
|---|---|---|
| `F-10′` | work ↔ observation relationship | **CLOSED — VERIFIED** |
| `F-13` | W5's observed population was entirely demonstrators | **NARROWED** — it now contains real work (`p11-w1-runtime`), 1 of 3 subjects. The model still does not distinguish work subjects from demonstration subjects, and inventing that taxonomy is not canonically grounded, so it stays open and small |
| `F-14` | `cross_department_coordination_proof.py` and `w4_first_execution.py` publish nothing | **OPEN — NON-BLOCKING.** Per-path coverage was established as *not canonically required*; recorded so the residue is visible rather than absorbed into the closure |

**The programme hypothesis now has a counter-example.** *"Capability reached only
by its own demonstrator"* held across three surfaces; it no longer holds
universally — one real work path reaches the observation surface. It remains
accurate for the majority and is retained as a systemic finding, not promoted to
a rule and not quietly dropped.

---

## 9. Verification

```text
native_core 801 OK (1 expected failure) · consumers 276 OK · tools 798 OK = 1875
citation 212 documents / 1147 citations / 0 errors · stale-state 508 / 0 assertions
   tools +9 — work ↔ observation conformance
certified evidence: p11 git changes 0 · guard intact (proof still exits 1)
native_core changes 0 · Native Core 11 frozen · protected read 0 / staged 0
```
