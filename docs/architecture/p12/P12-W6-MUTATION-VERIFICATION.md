# P12-W6 — Phase-Level Mutation Verification

**Scope item:** `§19` **MUTATION**, specified by Blueprint `§50`.
**Status:** [E] measured. Ten mutations, nine attempted, seven detected, two
missed, one with no surface to mutate.
**Instrument:** `tools/p12_mutation_verification.py`
**Conformance:** `tools/tests/test_p12_mutation_verification.py` (21 tests).

---

## 1. What `§50` asks

[A] `§50`: *"Mutation tests shall deliberately attempt to violate critical
contracts."* It then lists ten under the heading **Examples**, and states the
expected result as `VIOLATION DETECTED` / `ACTION REJECTED / BLOCKED /
ESCALATED`.

[C] The ten are **examples**, not a closed set. This record covers those ten
and claims nothing about mutations `§50` does not name.

## 2. Why `ATTEMPTED` is reported separately from `DETECTED`

[C] A mutation suite that returns ten detections is indistinguishable from one
that attempts nothing. Every function here performs the violation against a
real detector and reports what came back; `attempted` is carried through the
result type and printed on every line, so an unexercised control cannot be read
as a passing one.

[C] **A `MISSED` result is a finding about the system, not a failure of this
suite.** No mutation was rewritten to turn a miss into a detection.

[C] Nothing resident is mutated. Certified evidence is protected by `F-12` and
is not written. Where a mutation needs a mutable subject, the subject is copied
to a temporary directory first; a conformance test asserts that a full run
leaves the resident organization tree byte-unchanged in its reported defects.

## 3. Result

| `§50` mutation | Status | Attempted | What actually happened |
|---|---|---|---|
| remove authority | DETECTED | yes | `W4DelegationRegistry.issue` refuses a delegator other than the one `FD-P11-001 §4.1` names |
| alter provenance | DETECTED | yes | `reconcile` reports `provenance-mismatch` for a projection naming an actor other than the grant's recipient |
| change owner | DETECTED | yes | `organization_catalog.report()["inv1_disputed"]` reports a capability whose stated Owner contradicts its nesting |
| inject stale state | DETECTED | yes | a `RUNNING` observation older than the liveness horizon is refused as evidence of current state |
| forge actor | DETECTED | yes | a delegation to an unregistered Agent Instance is refused (`§6.1`) |
| **forge decision** | **MISSED** | yes | a planted certification statement is accepted |
| break workflow | DETECTED | yes | an illegal lifecycle transition (`defined → succeeded`) is refused |
| **duplicate delegation** | **MISSED** | yes | two `ACTIVE` grants of one capability to one recipient produce no defect |
| alter state authority | UNAVAILABLE | **no** | there is no state-authority surface to plant a competing claim on |
| change frozen boundary | DETECTED | yes | the boundary-count detector reports 12, not 11 |

[E] `{'mutations': 10, 'attempted': 9, 'detected': 7, 'missed': 2,
'unavailable': 1, 'missed_mutations': ('forge decision', 'duplicate delegation')}`

## 4. The three findings

### 4.1 `forge decision` — MISSED

[E] The certified-evidence guard (`F-12`) determines which phases are certified
by reading certification **statements** out of instrument bodies. A body
containing such a statement is therefore sufficient to make the guard treat a
phase as certified. The guard cannot distinguish an instrument the Founder
issued from one that merely contains the sentence.

[D] This is a real limit on `F-12`, and it is a limit of the **class** the guard
belongs to: every reader in this corpus that derives authority from prose is
exposed to it. Closing it requires an authority signal outside the body — which
is a governance question, not an engineering one.

[U] Not closed. Recorded as an open finding.

### 4.2 `duplicate delegation` — MISSED

[E] `reconcile` detects **duplicated representation** — two `CURRENT`
projections of one grant — and the probe exercises that case first as its own
control, so the null result below is a measurement and not a probe that failed
to run.

[E] It does **not** detect **duplicated delegation**: two independent `ACTIVE`
grants conveying the same capability to the same recipient instance produce an
empty defect list.

[D] The two are different mutations. `§50` names the second. The projection
store is keyed per recipient instance, so the duplicate grant cannot acquire a
competing `CURRENT` record — which is why the shape is invisible rather than
contradictory.

[U] Not closed. Recorded as an open finding.

### 4.3 `alter state authority` — UNAVAILABLE, not MISSED

[E] `P12-W2` unified operational state is not built. There is no
state-authority surface on which two competing claims could be planted.

[C] This is reported as **not attempted**. Reporting it as attempted-and-missed
would assert that a detector was exercised and stayed silent; nothing was
exercised. The absence is the finding, and it is recorded as an absence.

## 5. Three defects in this instrument, disclosed

[C] Per standing discipline, defects in my own verification code are disclosed,
never silently corrected.

1. **`alter provenance` verified nothing.** The first version checked that
   `'provenance-mismatch'` was a declared defect kind and reported `DETECTED`.
   That is Blueprint `§48` exactly — *"A relationship is not considered verified
   merely because both surfaces exist"* — inside the module built to refuse it.
   It now plants a contradicting projection, runs `reconcile`, and carries an
   unmutated control proving the detector is silent before the mutation.

2. **`change owner` asserted a conclusion it had not measured.** The first
   version read a Department record, confirmed it had an `Owner` section,
   mutated nothing, and reported *"no resident detector compares a Department's
   declared owner against an independent authority"*. **That statement was
   false.** `organization_catalog._owner_disagreements` compares a capability
   record's stated Owner against the Department directory holding it. The
   mutation now runs against a full copy of the tree, and it is **DETECTED**.

3. **The classifier counted unapplied mutations as undetected ones.** `verify()`
   mapped `attempted=False, detected=False` to `MISSED`. An unapplied mutation
   is not an undetected mutation, and the conflation is the same error in
   mirror image as the one this module exists to catch. It now maps to
   `UNAVAILABLE`, with a conformance test holding the distinction closed.

[E] Two earlier `UNAVAILABLE` results — `remove authority` and `forge actor` —
were my own API error: I imported `W4Delegator`, which does not exist. The real
class is `W4DelegationRegistry`. Both are now attempted, and both are
`DETECTED`. They were never findings about the system.

## 6. Controls this suite carries

[C] Seven detections is also what a suite that attempts nothing and returns
`DETECTED` would report. The conformance suite establishes what tells them
apart:

- a mutation returning `attempted=True, detected=False` is reported as `MISSED`
  and appears in `missed_mutations` — **the suite can report failure**;
- the live run is asserted to contain at least one `MISSED` result;
- a mutation that raises is `UNAVAILABLE`, never `DETECTED`;
- the delegation fixture is asserted to be otherwise valid, so each refusal is
  caused by the mutation and not by a malformed request;
- `alter provenance` is asserted not to be an existence check;
- a full `verify()` run is asserted to leave the resident tree's reported
  defects unchanged.

## 7. What this does not establish

[C] `§50`'s ten are examples. Seven detections establish that seven named
contracts refuse seven named violations by the paths exercised here. They do
not establish that the system is resistant to mutation generally, that
unnamed mutations are detected, or that a detector that fires on a synthetic
input would fire on a corrupted resident one.

[C] This record closes no frontier and ratifies nothing. `E12` remains prepared
and not ratified (`F-16`, Founder-reserved).

---

**Suite state at this record:** `native_core` 801 (1 expected failure) ·
`consumers` 276 · `tools` 857 · total **1934**.
