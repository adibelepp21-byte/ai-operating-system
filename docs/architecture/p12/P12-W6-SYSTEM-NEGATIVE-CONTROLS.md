# P12-W6 — System Negative Controls (`§49`)

**Scope item:** `§19` **NEGATIVE CONTROLS**, specified by Blueprint `§49`.
**Status:** [E] measured. **13 attempted · 11 refused · 2 accepted · 0
uncontrolled.**
**Instrument:** `tools/p12_system_negative_controls.py`
**Conformance:** `tools/tests/test_p12_system_negative_controls.py` (17 tests).

---

## 1. The scope item this closes, and the one it does not

[A] `§49` names **thirteen mandatory negative controls**, each an illegitimate
action the system must refuse. It closes: *"Negative controls are integrity
evidence, not an independent capability dimension."*

[C] `§127.2` reopened this scope item after recording it closed. The earlier
record, `P12-W6-NEGATIVE-CONTROL-VERIFICATION.md`, verified that **verifiers can
report a negative** — required independently by `ACT-CC-P12-W6-CONTINUATION-001
§18`, and not what `§49` asks. Both are real; they are different questions, and
they now live in different modules so neither can stand in for the other. A
conformance control asserts the two populations are not the same set.

## 2. Every control is attempted

[C] `ATTEMPTED` is reported separately from `REFUSED`. A control reported as
holding because the illegitimate path was never exercised is the defect this
programme keeps correcting.

[C] Where `§49` overlaps `§50`, the attempt is **made here too, not cited**. A
citation establishes that an attempt succeeded once; it does not establish that
the refusal still holds.

[C] Nothing resident is mutated. The plan, goal, delegation and registry used to
provoke refusals are constructed in temporary directories or in memory.

## 3. Result

| `§49` control | Status | What refused it |
|---|---|---|
| self-authorization | REFUSED | `DelegationRequirement.as_delegation_record()` — *"Planning cannot author a delegation record"* |
| authority expansion | REFUSED | `issue()` intersection against the instance's permitted surface |
| governance bypass | REFUSED | `EscalationRequired` — adapting would need authority the plan does not hold |
| invalid provenance | REFUSED | `AuthorityProvenance` — a citation that does not resolve |
| fabricated actor | REFUSED | `§6.1` — delegation to an unregistered Agent Instance |
| unauthorized delegation | REFUSED | `§4.1` — a delegator the Founder Decision did not name |
| unauthorized state mutation | REFUSED | `CertifiedEvidenceProtected` — write under certified evidence |
| unauthorized architecture mutation | REFUSED | boundary count reports 12, not 11 |
| **unauthorized P13 authorization** | **ACCEPTED** | nothing |
| false completion | REFUSED | the resident answer to *what is incomplete* contradicts the claim |
| **false certification** | **ACCEPTED** | nothing |
| stale-state acceptance | REFUSED | stale `RUNNING` refused as evidence of current state |
| historical-as-current substitution | REFUSED | 6 superseded claims registered, 55 historical uses distinguished, 0 standing as current |

[E] `{'controls': 13, 'attempted': 13, 'refused': 11, 'accepted': 2,
'uncontrolled': 0}`

## 4. The two findings

### 4.1 `unauthorized P13 authorization` — ACCEPTED

[E] **No resident surface states P13's authorization status.** The Self-Model's
authority answer does not mention P13, so a claim that P13 is authorized would
contradict nothing the system holds.

[D] P13 being unauthorized is stated in Founder instruments and repeated
throughout this master record — in prose. It is not a value any consumer can
read, which is the same shape as the `§26` governance finding: the fact is
established for a human reader and absent for every consumer.

[C] Not closed here. Making P13's status machine-readable means adding a
programme-state surface, and `ACT §26` forbids a W6 implementation from
establishing authority by convention. **Recorded as a finding.**

### 4.2 `false certification` — ACCEPTED

[E] The certified-evidence guard reads certification statements out of
instrument bodies, so a body containing such a statement is sufficient to make
it treat a phase as certified. Independently reproduced here, not carried over
from `§124`.

[D] Unchanged since first found, and it remains a governance question rather
than an engineering one: closing it needs an authority signal outside the body.

## 5. Two defects in this instrument, disclosed

[C] Both were in the first run, and one of them is the precise failure this
module exists to detect.

1. **A probe's own exception was reported as a refusal.** `_governance_bypass`
   caught `Exception` broadly. The probe called an API that does not exist
   (`surface.plans()`), raised `AttributeError`, and the control was reported
   **REFUSED**. A governance-bypass control passing because the probe crashed is
   a false pass, and a false pass on a `§49` control is worse than a missing one.
   It now accepts only `EscalationRequired`, and a conformance control asserts
   that a broken fixture propagates rather than reading as a refusal.

2. **`self-authorization` invented the same API** and reported `UNCONTROLLED`.
   Both probes now build a Goal and Plan the way the resident suites do.

[C] The classifier was already correct: an unattempted control is `UNCONTROLLED`
and counted as not refused, never as a refusal. That is the rule that kept the
second defect visible instead of silently adding to the refusal count.

## 6. Why eleven refusals is not self-certifying

[C] Eleven refusals is what a module returning a constant would print. The
conformance suite establishes that an unrefused attempt is reported `ACCEPTED`
and named; that a raising attempt is `UNCONTROLLED`, never `REFUSED`; that no
live control reports its own exception; that the live run reaches `ACCEPTED` at
least once; and that all thirteen are attempted with zero uncontrolled. The same
movement is driven at runtime by `p12_negative_control_verification`, which now
covers sixteen instruments.

## 7. What this does not establish

[C] Eleven refusals establish that eleven **named** paths are refused. `§49`'s
thirteen are a mandatory minimum, not an enumeration of every way the system
could be subverted. An unnamed path is not covered by this record.

[C] `REFUSED` says the attempt was rejected at the surface exercised. It does not
say no other surface would have accepted it.

---

**Suite state at this record:** `native_core` 801 (1 expected failure) ·
`consumers` 276 · `tools` 992 · total **2069**.
