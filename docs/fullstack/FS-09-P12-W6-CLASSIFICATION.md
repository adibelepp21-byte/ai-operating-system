# FS-09 — P12-W6 Regression Signal: Classification

Under `ACT-CC-POST-P13-AIOS-FULL-STACK-008` `§15` (Register `§102`). P12 is untouched. Raw evidence: `evidence/FS-09-ACT-008-P12-W6-CLASSIFICATION-2026-09-30.json`.

## RAW RESULT

`python3 -m unittest tools.tests.test_p12_governance_evidence_verification` → 17 tests, **1 failure**:

```text
FAIL: test_the_narrower_population_is_not_better [status]
AssertionError: 0.49523809523809526 not less than or equal to 0.49260450160771707
```

The test compares, per governance element, the share of *Founder Acts*
(`docs/governance/acts/`) carrying a label with the share in the whole corpus,
and requires the Acts' share to be at most the corpus share **+ 0.2**. For
`Status:` the Acts carry 52 of 105 (0.4952); the corpus 182 of 622 (0.2926; limit
0.4926). The limit is exceeded by 0.0026. The other four elements pass.

## Where it came from

| Commit | Change | Result |
|---|---|---|
| `ab18082^` | | 17 OK |
| `ab18082` | adds the verbatim Founder Act ACT-006 (a docs file) and Register `§95` | **1 failure** |
| `3182510` | adds ACT-007 verbatim | 1 failure |
| `d6afbdc` | adds ACT-008 verbatim | 1 failure |

Counterfactual, in a scratch worktree only: `HEAD` with the three verbatim Acts
removed → 17 OK. ACT-006 and ACT-007 each open with a `Status` line (the
Founder's text, persisted verbatim as the Act instructs). No file under
`fullstack/`, `native_core/` or `tools/` changed in those commits.

## CLASSIFICATION

**A known classified P12 baseline guard condition**: a hard-coded population
ratio tolerance in a P12 verification test, exceeded because the governance
corpus grew by legitimate, verbatim Founder Acts. It is **not** an FS-09
failure, **not** a test-harness integration defect (the test runs correctly and
measures what it says), and **not** a new system regression (no behaviour
changed; the measured fact is a label share in documents).

"Known": it was recorded as `F-1` at ACT-006 and reproduced by bisection here.
Caveat stated plainly: nobody ratified it as an accepted P12 exception; it is
classified, not waived, and the test stays red in the global runner.

## WHY IT DOES NOT BLOCK FS-09

1. `§15.3` and the Act's `§27` rule: *only an actual FS-09 failure blocks FS-09*.
   No FS-09 code, configuration, deployment or evidence is involved (bisect and
   counterfactual above).
2. The failure cannot be removed by any FS-09 action without a forbidden one:
   dropping or rewording the Founder's Acts, widening the tolerance, or
   changing the P12 population would each alter P12 or game the guard (`§15.1`).
3. P12's certified evidence is intact (the integrity check passes; recorded in
   the execution record).

**Owner of the remedy:** the P12 / governance owner (Founder authority over the
certified root). It will recur with each further Act carrying a `Status` label.
Nothing was deleted, renamed, relaxed or suppressed.
