# P12-W6 — Failure Behaviour Verification

**Scope item:** `§19` **FAILURE**, specified by Blueprint `§33`.
**Status:** [E] measured. **3 of 7 states distinguished · 2 raised only ·
2 unreachable.** Retry prohibitions: **NOT APPLICABLE**.
**Instrument:** `tools/p12_failure_verification.py`
**Conformance:** `tools/tests/test_p12_failure_verification.py` (18 tests).

---

## 1. What `§33` asks

[A] `§33`: failure behaviour must **distinguish** `RETRYABLE`, `BLOCKED`,
`REFUSED`, `FAILED`, `ESCALATED`, `SUCCEEDED`, `VERIFIED`. Retry must not create
duplicate authority, duplicate delegation, duplicate execution, orphan state, or
false success.

[C] **"Distinguish" has two halves.** A state is distinguished only if the
system can *reach* it **and** *tell it apart from the others afterwards*. A
system that raises two different exception types and writes both into the same
record shape has distinguished them in flight and lost the distinction at rest —
and it is the record, not the traceback, that anyone reads later. Every state is
therefore measured at two points: raised, and persisted.

## 2. Result

| `§33` state | Status | Persisted as |
|---|---|---|
| **RETRYABLE** | **UNREACHABLE** | — |
| **BLOCKED** | **RAISED ONLY** | escalation record (`required`, `held`) |
| **REFUSED** | **RAISED ONLY** | escalation record |
| FAILED | DISTINGUISHED | trace record `status='failure'` |
| ESCALATED | DISTINGUISHED | trace `status='escalation'` + escalation record |
| SUCCEEDED | DISTINGUISHED | trace record `status='success'` |
| **VERIFIED** | **UNREACHABLE** | — |

[E] `{'states': 7, 'distinguished': 3, 'raised_only': 2, 'unreachable': 2,
'retry': 'NOT APPLICABLE'}`

## 3. The findings

### 3.1 `RETRYABLE` — UNREACHABLE

[E] **No live retry mechanism exists.** A syntax-tree search over every non-test
module of the running system finds no function, class, or parameter implementing
retry. The only one in the repository is `_apply_retry_policy` in
`docs/architecture/history/legacy-execution/tool_executor.py`, which is
preserved history and is not reachable from the running system.

[C] Content-anchored on the AST, not on text: a comment mentioning retry is not
a retry mechanism, and a conformance control proves the search ignores one.

### 3.2 `REFUSED` — RAISED ONLY

[E] Two distinct refusal types are raised — `EscalationRequired` when a *plan*
would exceed its authority, `ExecutionRefused` when a *step* would exceed its
delegation — and `SANCTIONED_REFUSALS` names them explicitly rather than
accepting anything refusal-shaped.

[E] **The persisted `EscalationRecord` carries no field naming which one
occurred**: `escalation_id, subject, required, held, reason, authority,
raised_at`. Both types become the same record shape.

[D] So `§33`'s `REFUSED` and `ESCALATED` are distinguished at raise time and
collapse at persistence. Anyone reading the register later cannot tell a refused
step from an escalated plan.

### 3.3 `BLOCKED` — RAISED ONLY

[E] A blocked action *is* persisted, as `required` against `held` — what the
action needed versus what the actor had, which is exactly the pair that makes an
action blocked. But it is persisted under the same record shape as an
escalation, and nothing marks it `BLOCKED` rather than `ESCALATED`.

### 3.4 `VERIFIED` — UNREACHABLE

[E] The ratified Trace vocabulary is `{success, failure, escalation}`. **No
execution record can hold a verified state.** A successful run is not a verified
one, and the corpus has no way to say that an execution was checked.

[C] Widening the ratified vocabulary is **not** in scope and was not done. That
vocabulary is ratified, and `§33` does not say Trace must be the surface
carrying all seven. The finding is that **no** resident execution surface
carries `VERIFIED`, not that Trace should.

### 3.5 The five retry prohibitions — NOT APPLICABLE, not satisfied

[C] With no retry mechanism, no retry can create a duplicate. **That is the
absence of the hazard, not a control against it.** Reporting the five as
satisfied would be the cleanest possible lie, so the status is `NOT APPLICABLE`
and the detail says *"none is controlled against"*. A conformance control
asserts that the status is never `PASS`, and that introducing a retry mechanism
moves it to `UNVERIFIED` rather than to satisfied.

## 4. A defect in this instrument, disclosed

[E] On its first run this module reported **three live retry mechanisms in a
system that has none**. All three were its own functions: `retry_mechanisms`,
`_retryable`, `retry_prohibitions`. The search population included the module
performing the search.

[D] **A verifier counting itself as the capability it measures** is the same
defect class as the Self-Model answering about a corpus it had not read, and as
the mutation probe that reported a detection from an existence check. It is now
excluded from its own population, and a conformance control asserts the
exclusion so the self-match cannot return unnoticed.

[C] The first output was not a finding about the system. It was a finding about
this module, and it is recorded rather than quietly corrected.

## 5. Falsifiability in both directions

[C] Four non-distinguished states are a claim, and a checker stuck at four is
indistinguishable from one that measured nothing. Conformance controls prove the
module promotes a state the moment the system earns it:

- an escalation record carrying a refusal-type field makes `REFUSED`
  `DISTINGUISHED`;
- a Trace vocabulary containing `verified` makes `VERIFIED` `DISTINGUISHED`;
- a real retry definition is found, while a comment mentioning retry is not;
- an unreachable state is never counted toward `distinguished`.

[C] The same promotion is driven at runtime by
`p12_negative_control_verification`, so the finding cannot silently become a
constant between releases.

## 6. What this does not establish

[C] Three distinguished says three states can be reached and told apart. It does
not say they are used correctly, raised at the right times, or complete.

[C] No ratified vocabulary was widened. No record shape was changed. This record
classifies `FAILURE` truthfully; it does not close it.

---

**Suite state at this record:** `native_core` 801 (1 expected failure) ·
`consumers` 276 · `tools` 932 · total **2009**.
