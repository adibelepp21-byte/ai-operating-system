# P12-W6 — Phase-Level Regression Verification

**Scope item:** `§19` **REGRESSION**, specified by Blueprint `§51`.
**Status:** [E] measured. Eleven classes: ten `HELD`, one `UNANCHORED`, zero
`REGRESSED`. Structural comparison against the P11 certification commit:
**0 controls removed, 0 weakened.**
**Instrument:** `tools/p12_regression_verification.py`
**Conformance:** `tools/tests/test_p12_regression_verification.py` (22 tests).

---

## 1. What `§51` asks, and the word it turns on

[A] `§51`: *"P12 must demonstrate that integration has not silently broken valid
P4–P11 behavior."* It names eleven regression classes: functional, authority,
governance, state, runtime, workflow, evidence, provenance, boundary, security,
quality.

[C] The operative word is **silently**. A green suite is not the evidence asked
for. A control that was deleted, renamed, or stripped of its assertions also
reports green — and reports it more quietly than a failure would. `1934` passing
tests cannot distinguish *"every P4–P11 behavior still holds"* from *"the tests
that would have caught the breakage are gone."*

## 2. Two verifications, deliberately kept apart

### 2.1 Structural — exhaustive, and immune to a wrong mapping

[E] The full inventory of declared controls at the **P11 certification commit**
`98c0a1e` (*"Persist FD-P11-002: P11 is certified"*) is compared to the
inventory now. Everything after that commit is P12 integration work, which is
exactly the interval `§51` asks about.

| | |
|---|---|
| Controls at `98c0a1e` | **2089** |
| Controls now | **2222** |
| Removed | **0** |
| Weakened | **0** |
| Status | **HELD** |

[C] This comparison is exhaustive over the repository and needs no assignment of
controls to classes, so **no mapping error can hide a case from it**. A renamed
control reads as removed, which is correct: renaming is how a control disappears
while the total goes up.

[C] "Weakened" counts assertion calls, bare `assert`, and `with` blocks. The
last is included because `assertRaises` is usually written as a context manager,
and a control that loses its `with self.assertRaises(...)` has lost its entire
point while keeping its name and its green result.

[D] **On the two different totals.** `2222` counts *declared* control methods
read from source; the runners report `1934` *executed* tests. A parameterized
control runs more than once and an undiscovered module runs not at all. They
measure different things and are not reconciled here — reporting either as the
other would be a fabricated equivalence.

### 2.2 Behavioural — one named anchor per class

| `§51` class | Status | Anchor | Measured now |
|---|---|---|---|
| functional | HELD | inventory diff | 2089 → 2222, 0 removed, 0 weakened |
| authority | HELD | `w4_delegation.issue` | an unauthorized delegator is refused |
| governance | HELD | `GovernanceIndex.stale_sources` | 436 records from 516 sources, 0 stale |
| state | HELD | `stale_state_audit.audit` | 515 documents, 0 live stale assertions, 55 preserved as history |
| runtime | HELD | `p12_runtime_observation.what_is_running` | a stale `RUNNING` record is refused as current |
| workflow | HELD | Native Core workflow lifecycle | `defined → succeeded` is refused |
| evidence | HELD | `corpus_citation_audit.audit` | 1170 citations, 0 errors |
| provenance | HELD | `AuthorityProvenance` | an unresolvable citation is refused |
| boundary | HELD | `derived_views._boundaries` | exactly 11 frozen subsystems |
| security | HELD | `p12_certified_evidence_guard.guard` | a write under certified evidence is refused |
| **quality** | **UNANCHORED** | — | no resident quality gate exists |

[C] `HELD` means *this named check produced this value now*. It does **not** mean
the class is free of regression. **A class is only as covered as its anchor**,
and a conformance control asserts that no `HELD` result may exist without a named
anchor, so the claim always stays falsifiable.

## 3. The finding: `quality` is UNANCHORED

[E] There is no linter configuration, no formatter configuration, no coverage
threshold, and no CI workflow in this repository. `§51` names a quality
regression class; nothing resident measures quality.

[C] Reported `UNANCHORED`, never `HELD`. **A class whose anchor does not exist
has not held — it has not been looked at.** Reporting it as held would be the
error this programme keeps correcting: a control reported as passing because
nothing exercised it.

[U] Open. Building a quality gate is construction, not verification, and `§51`
asks whether quality has regressed — a question with no prior value to regress
from.

## 4. Why ten HELD is not self-certifying

[C] Ten `HELD` is exactly what a module that checks nothing would print. The
conformance suite makes each anchor drift on demand:

- every one of the eleven classes is driven to `REGRESSED` by substituting a
  failing anchor, and the class is named in `regressed_classes`;
- the structural comparison detects a removed control, a weakened control, and
  a **renamed** control — the last against an inventory that grew;
- growth alone is asserted *not* to be a regression, so the check is not simply
  counting;
- the assertion weight of a control with `with self.assertRaises(...)` is
  asserted greater than the same control with it stripped;
- the boundary anchor is run against a synthetic twelve-subsystem tree and
  drifts;
- a `None` anchor is `UNANCHORED` and an anchor that raises is `UNAVAILABLE` —
  neither is ever counted as `HELD`;
- the baseline is asserted to be the commit whose subject names `FD-P11-002`.

## 5. Three defects in this instrument, disclosed

[C] Defects in my own verification code are disclosed, never silently corrected.

1. **Three anchors were written against APIs I had not read.**
   `governance_index.read_register`, `stale_state_audit.audit()["stale"]`, and
   `corpus_citation_audit.audit()` with no arguments do not exist as written.
   All three returned `UNAVAILABLE` on the first run. They were fixed against
   the real signatures and all three now run. They were never findings about
   the system — they were findings about me, the same class of error as the
   `W4Delegator` import in the mutation suite.

2. **The governance anchor originally only checked that parsing succeeded.**
   Parsing succeeds for an instrument that was edited after being indexed. The
   anchor now calls `stale_sources`, which recomputes each instrument's hash
   against the one recorded at build — the check that can actually see the
   silent breakage `§51` names.

3. **A resident guard flagged this module, and the explanation flagged it
   again.** `test_line_numbering_coherence` scans for the shape of a
   `path:line` locator; an interpolated git revision spec has the same shape.
   Nothing in this module computes a line number, so the spec is now built by
   concatenation — and the comment explaining that had to be rewritten, because
   the guard reads raw text and matched the literal in the comment too. **The
   guard was not loosened and this module was not falsely declared an emitter.**
   A locator guard that fails closed errs in the right direction.

## 6. A resident guard caught this module, for the seventh time

[E] `test_the_declared_p11_surface_set_is_complete` failed on the run that
created `tools/p12_regression_verification.py`. Declared rather than exempted:
the module reads the planning surface to check that an unresolvable citation is
still refused, and that control would be worthless if the module could itself
hold an unverified provenance.

## 7. What this does not establish

[C] Zero removed and zero weakened establishes that no control present at P11
certification has been lost. It does **not** establish that P4–P11 behavior is
correct, that the controls were adequate at the baseline, or that a behavior
nobody ever encoded as a control still holds.

[C] Ten anchors establish that ten named checks produce ten named values now.
They do not establish that the eleven `§51` classes are exhaustively covered.

[C] This record closes no frontier and ratifies nothing. `E12` remains prepared
and not ratified (`F-16`, Founder-reserved).

---

**Suite state at this record:** `native_core` 801 (1 expected failure) ·
`consumers` 276 · `tools` 879 · total **1956**.
