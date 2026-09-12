# P12-W6 — Execution Provenance Verification

**Scope item:** `§19` **PROVENANCE**, specified by Blueprint `§34`.
**Status:** [E] measured. **9 of 11 elements carried · 2 absent · 0 of 2
executions assemblable.**
**Instrument:** `tools/p12_provenance_verification.py`
**Conformance:** `tools/tests/test_p12_provenance_verification.py` (17 tests).

---

## 1. What `§34` asks

[A] `§34`: execution provenance must identify, where applicable — actor,
delegator, authority, objective, work scope, capability, workflow, runtime,
result, evidence, verification. It closes: *"Provenance is part of system
integrity."*

[C] The question is **not** whether each of the eleven appears somewhere in the
corpus. It is whether provenance can be **assembled for an execution**. An
element carried on one record and another element carried on a different record
is provenance only if the two records can be joined. So this module reports two
measurements and never merges them.

## 2. Read from stored records, not class definitions

[C] A dataclass field proves a field *can* be written; only a stored record
proves one *was*. Here the two genuinely diverge:
`TraceRecord.from_mapping` reconstructs only the ten required fields, so any
additional key written into a Trace record is **silently dropped on read**. A
schema inspection would report a carrier that a corpus inspection shows is not
there. A conformance control asserts this drop directly against Native Core, so
the choice cannot rot silently if Trace ever gains the field.

## 3. Element coverage

[E] 24 resident delegation records, 2 durable Trace records.

| `§34` element | Status | Carrier |
|---|---|---|
| actor | CARRIED | `delegation.recipient_instance` 24/24 · `trace.agent_instance` 2/2 |
| delegator | CARRIED | `delegation.delegator` 24/24 |
| authority | CARRIED | `delegation.authority_record` 24/24 |
| objective | CARRIED | `delegation.objective` 24/24 |
| work scope | CARRIED | `delegation.work_scope` 24/24 |
| capability | CARRIED | `delegation.capability_scope` 24/24 |
| **workflow** | **ABSENT** | no resident record type declares a key |
| runtime | CARRIED | `trace.runtime` 2/2 |
| result | CARRIED | `trace.outputs` 2/2 |
| **evidence** | **ABSENT** | no resident record type declares a key |
| verification | CARRIED | `delegation.verification_requirement` 24/24 |

[C] A key present with an empty value is **not** counted as coverage.
`skills_used: []` identifies no skill, and counting it would be how an empty
field comes to look like a filled one. A conformance control holds this.

## 4. The finding: provenance cannot be assembled

[E] **`NOT ASSEMBLABLE` — 0 of 2 executions joined.**

[E] A delegation record carries the authority half of `§34` completely, down to
an explicit `authority_chain` ending at the Founder. A Trace record carries the
execution half: actor, runtime, result. **Neither references the other.** A
Trace record has no `delegation_id`; a delegation record has no runtime, no
result and no evidence reference.

[C] **The actor name is not a join.** It appears on both sides, and matching on
it identifies a *set* of grants rather than the one in force: one Agent Instance
holds many grants. Where the match happens to be unique today, it is unique by
accident of how many grants that instance currently holds — a second grant would
silently make the same execution ambiguous. The module counts such matches as
**not joined**, and a conformance control fixes that choice.

[D] So for every execution this corpus contains, `§34` provenance stops at the
boundary between the decision and the execution. The system can say who was
authorized to do what, and it can say what ran and what came out. It cannot say
that *this run* happened under *that grant*.

[D] This is the `§29` canonical chain — `INTENT → DECISION → WORK → EXECUTION →
OBSERVATION → VERIFICATION → EVIDENCE` — broken between `DECISION` and
`EXECUTION`, and it is broken in the records rather than in the code.

## 5. Classification, and what was deliberately not done

[C] **PROVENANCE is truthfully classified, not passed.** The finding is
recorded, not eliminated.

[C] No Trace record was modified and no delegation record was altered. Writing a
`delegation_id` into the existing stored Trace records would be manufacturing
historical execution evidence, which `ACT §19` forbids: new evidence requires
`NEW REAL EXECUTION → NEW OBSERVATION → NEW EVIDENCE`.

[C] The join is **not** built inside Native Core. `TraceRecord` is a ratified,
fixed-schema, immutable boundary and extending it is a Native Core change.
Any join must live on a P12 surface that records the relation at execution time.
That is P12-W4 execution-integration construction, and it is surfaced as a
decision rather than performed here — `ACT §12` prohibits construction before
classification, and this record is the classification.

## 6. Why two measurements, never merged

[C] Nine carried elements and zero assemblable executions co-exist, and reporting
a single number over them would hide exactly the defect. A conformance control
asserts both states simultaneously on the live corpus. Others prove each
measurement can move: an execution naming a real delegation is `ASSEMBLABLE`;
one naming a delegation that does not exist is not; partial joining is not; an
empty corpus reports `NO EXECUTIONS` rather than success.

## 7. What this does not establish

[C] Nine carried says nine elements are populated in resident records. It does
not say they are correct, current, or mutually consistent.

[C] `workflow` and `evidence` are reported `ABSENT` from the two record types
that carry execution provenance. Other surfaces in the corpus hold workflow
definitions and evidence documents; the finding is that **execution provenance**
does not reach them, not that they do not exist.

---

**Suite state at this record:** `native_core` 801 (1 expected failure) ·
`consumers` 276 · `tools` 913 · total **1990**.
