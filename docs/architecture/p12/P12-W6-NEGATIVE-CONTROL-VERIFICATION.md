# P12-W6 — Negative Controls

**Scope item:** `§19` **NEGATIVE CONTROLS**.
**Status:** [E] measured. Ten P12 verification instruments, **ten negatives
demonstrated at runtime**, zero cited.
**Instrument:** `tools/p12_negative_control_verification.py`
**Conformance:** `tools/tests/test_p12_negative_control_verification.py` (17 tests).

---

## 1. A correction first

[C] After committing `§51` regression verification I wrote that it was the last
W6 item buildable without a reserved boundary. **That was wrong.** `§19` lists
**thirteen** minimum scope items. Five were built: `CROSS-PHASE CONTRACTS`,
`CROSS-PD INTERFACES`, `MUTATION`, `REGRESSION`, `FRESH PROCESS`. **Eight were
not**, and none of the eight touches a reserved boundary.

[C] The error is the one this programme names `EXHAUSTION ≠ EXHAUSTION OF WHAT
I HAPPENED TO BUILD`. It was found by re-reading `§19` from source rather than
from my own prior report — which is Rule 0, and the reason Rule 0 exists.

This record closes the sixth: `NEGATIVE CONTROLS`.

## 2. What this scope asks, and why it is not MUTATION or REGRESSION

[A] `§19` lists `NEGATIVE CONTROLS` as a verification scope of its own, beside
`MUTATION` and `REGRESSION`. It closes: *"P12-W6 tidak boleh dianggap selesai
hanya karena unit tests individual hijau."*

[C] The question is about the **verifiers**, not the system. `MUTATION` asks
whether the system detects a violation. `REGRESSION` asks whether behavior was
lost. `NEGATIVE CONTROLS` asks something prior to both: **can each verification
instrument report a negative result at all?** An instrument that structurally
cannot fail is not a verifier — it is a formatted assertion, and its green
output carries no information about anything.

[C] **Every negative here is driven at runtime, in this process.** Citing an
instrument's own conformance suite would establish only that two surfaces exist
(`§48`), and would let an instrument that has since lost the ability to fail
keep a demonstration it no longer earns.

## 3. Result

| Instrument | Negative sought | Driven how | Status |
|---|---|---|---|
| `p12_runtime_observation` | cannot answer what is running | empty observation root | DEMONSTRATED |
| `p12_trace_registry` | nothing has run | empty store root | DEMONSTRATED |
| `p12_certified_evidence_guard` | certification undeterminable | evidence-root map emptied | DEMONSTRATED |
| `p12_cross_phase_verification` | a phase is NOT EXERCISED | live corpus: 2 of 8 | DEMONSTRATED |
| `p12_cross_pd_verification` | the registry is UNAVAILABLE | registry path removed | DEMONSTRATED |
| `p12_fresh_process_verification` | a stage DIVERGED | subprocess answers differently: 8 of 8 | DEMONSTRATED |
| `p12_mutation_verification` | a mutation is MISSED | live corpus: 2 of 10 | DEMONSTRATED |
| `p12_regression_verification` | a class REGRESSED | a control removed from the inventory | DEMONSTRATED |
| `p12_self_model` | a question answers UNKNOWN | empty root: 3 of 3 store-backed | DEMONSTRATED |
| `governance_index` | a source is stale | source bytes changed after build | DEMONSTRATED |

[E] `{'instruments': 10, 'demonstrated': 10, 'not_demonstrated': 0,
'unavailable': 0}`

[C] Every module-level constant altered to drive a negative is restored in a
`finally` block, and conformance controls assert the restoration by re-running
the instrument afterwards and checking it reports its live value again.

## 4. The finding: the Self-Model's `root` parameter had no effect

[E] Three Self-Model questions — *what capabilities exist*, *what is running*,
*what failed* — accepted a `root` argument and ignored it. They read the other
modules' root constants directly. Pointed at an empty directory they returned
answers **byte-identical to the live ones**: `failed` reported `failures: 1`
about a directory containing nothing.

[D] This made the Self-Model impossible to isolate, and made any claim that it
had been verified *against* a given corpus unfalsifiable — the answer would have
been the same for any corpus, including none.

[D] **It is the same defect `p12_cross_phase_verification` carried**, where
evidence roots were bound as default arguments at import. Fixing that instance
did not generalize, and nothing resident could see the second instance. That is
precisely why `§19` lists this scope separately.

[E] **Fixed.** The three questions now derive their store root from the `root`
they are given. Against an empty root all three answer `UNKNOWN`. A root that
has been explicitly redirected outside the repository is honored as given — that
is how the resident suites isolate these questions, and re-basing it would have
broken them.

[E] **The live measurement did not change:** `{questions: 12, verified: 10,
inferred: 2, unknown: 0}`, before and after. The numbers recorded in
`P12-W5-SELF-MODEL-EVIDENCE.md` were correct. What was wrong was not the value
but the ability to challenge it.

## 5. Two further observations, recorded and not fixed

[E] Six Self-Model questions raise rather than answering `UNKNOWN` when given a
root that is not a git repository. [D] A non-repository is arguably outside the
contract, so this is recorded rather than treated as a defect; it is reported in
the instrument's own output so it cannot be lost.

[E] `authority` and `authoritative` are answered from declared constants and no
corpus can change them. [C] They are left root-independent deliberately. Faking
a dependency to make them look isolable would be manufacturing the property this
scope exists to measure.

## 6. Why ten DEMONSTRATED is not self-certifying

[C] Ten `DEMONSTRATED` is what a module returning a constant would print. The
conformance suite establishes:

- a control returning a non-negative is reported `NOT DEMONSTRATED` and named in
  `undemonstrated_instruments`;
- a control that raises is `UNAVAILABLE`, never `DEMONSTRATED`, and is still
  counted as not demonstrated;
- **every resident `tools/p12_*.py` module is covered or explicitly exempt** —
  a verifier added later and left uncovered fails this control, so the
  population cannot silently narrow;
- each constant altered during a negative is asserted restored, and the
  instrument asserted to report its live value again afterwards;
- the Self-Model's three store-backed questions are asserted to answer `UNKNOWN`
  against an empty root **and** to differ from their live answers — the second
  assertion is the one that would have caught the original defect.

## 7. What this does not establish

[C] That an instrument *can* report a negative says nothing about whether its
positive results are correct. A verifier that fails on demand can still measure
the wrong thing. This scope establishes that ten instruments are falsifiable, not
that they are right.

[C] `EIGHT of §19's THIRTEEN scope items remain`: `RUNTIME`, `WORKFLOW`,
`GOVERNANCE`, `STATE`, `EVIDENCE`, `PROVENANCE`, `FAILURE` — and this one now
closed, leaving seven. None is Founder- or Architect-reserved.

[C] This record closes no frontier and ratifies nothing. `E12` remains prepared
and not ratified (`F-16`, Founder-reserved).

---

**Suite state at this record:** `native_core` 801 (1 expected failure) ·
`consumers` 276 · `tools` 896 · total **1973**.
