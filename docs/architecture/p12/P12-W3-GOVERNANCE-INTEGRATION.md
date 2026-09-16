# P12-W3 — Governance Integration · first construction increment

**Act:** `ACT-CC-P12-003`.
**Status:** [E] constructed and independently verified. **One real refusal,
escalated, and joined to its grant by structural reference — not parsed
prose.** `W4-GAP-008` / `W2-GAP-007`: **CONSTRUCTED, beside the record.**
**Instruments:** `tools/p12_governance_escalation_join.py` (writer) ·
`tools/p12_governance_join_reader.py` (independent reader) ·
`p12_w3_governance_escalation.py` (the real path).
**Conformance:** `tools/tests/test_p12_governance_escalation_join.py` (16
tests) · two new `tools/p12_negative_control_verification.py` controls.

---

## 1. What `§16` of the Founder P12 Authorization actually grants

[A] `P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md §16`: *"Claude berwenang
mengintegrasikan existing governance mechanisms. Governance integration wajib
mempertahankan: DECISION → AUTHORITY → RATIONALE → IMPLEMENTATION →
VERIFICATION → CURRENT STATE. Claude tidak boleh menggunakan P12 sebagai
alasan untuk menyelesaikan Founder/Architect reserved matter."*

[D] This is authority to **integrate**, not to modify a certified P11
mechanism's ratified shape, and not to resolve a reserved matter. Three
prior Acts had already found the same concrete governance-integration gap and
each explicitly declined to close it inside its own workstream, naming it
`W3`'s:

- `P12-W4-EXECUTION-INTEGRATION.md §13`: *"Not constructed here.
  `EscalationRecord` is a frozen, written-once governance surface... `ACT §30`:
  `W4 ≠ W3`."*
- `P12-W2-UNIFIED-OPERATIONAL-STATE.md §11` (`W2-GAP-007`): *"`escalation.raised`
  is projected as a count. `W4-GAP-008`... remains `W3`'s to close. `ACT §44`:
  do not repair W3 from W2."*

[C] This increment is the first real `P12-W3` construction: it closes exactly
that named gap, and nothing else.

## 2. The gap, precisely

[E] `tools/p12_failure_verification.escalation_join()` measured (before this
increment): one resident escalation record, joined to the grant it was
refused under only by a regex over its prose `subject` field
(`r"delegation ([0-9a-f]{16})"`). `EscalationRecord.to_payload()`
(`tools/escalation_register.py`) carries no `delegation_id` and no
`refusal_type` field. **The relation was carried by a spelling, not a
reference** — true until somebody rewords the subject.

[D] The delegation id was never actually unavailable — `tools/w4_first_run.py:314`
already holds `delegation.delegation_id` in scope at the moment it writes
`subject=f"plan {plan.key} / delegation {delegation.delegation_id}"`. What was
missing was a place to put it that a reader could resolve **by reference**.

## 3. What was built, and why it is not inside `EscalationRecord`

[C] `tools/escalation_register.py`'s own docstring: *"Frozen, and written
once... there is no operation that edits a past record."* Widening the
dataclass would touch a P11-era, already-certified mechanism during a P12
integration phase — precisely the boundary `P12-W4-EXECUTION-INTEGRATION.md
§3` found for `TraceRecord` and refused to cross, choosing instead to build
`ExecutionManifest` **beside** it. The same choice is made here.

- **`tools/p12_governance_escalation_join.py`** — `EscalationGrantJoin`,
  persisted beside the escalation record it names. Refuses: an empty
  `delegation_id`, an unsanctioned `refusal_type`, a join naming an
  escalation the register does not hold, and overwriting an existing join
  (append-only, exactly as `EscalationRecord` itself is). **No existing
  function's signature changed.** `EscalationRecord`, `EscalationRegister`,
  and every one of their three resident callers
  (`tools/w4_first_run.py`, `tools/w1_coordination_run.py`,
  `tools/w1_cross_department_run.py`) are untouched.
- **`tools/p12_governance_join_reader.py`** — independent reader. `§24`:
  *"IMPLEMENTATION → SELF-REPORT → PASS"* is forbidden, so this module
  **imports nothing from the writer** and resolves both references itself:
  the escalation, through the resident `EscalationRegister`; the delegation,
  through `tools/p12_provenance_verification.delegation_records()` — the
  same resident population `escalation_join()` already reads. A conformance
  control parses this module's imports and fails if it ever imports the
  writer.
- **`tools/p12_failure_verification.escalation_join()`** — extended, not
  replaced, with a `joined_by_governance_surface` count, resolved through the
  new reader. The three original counts (`joined_by_structured_field`,
  `joined_by_parsed_prose`, `naming_the_refusal_type`) are computed exactly
  as before and still read `0`, `1`, `0` against the historical record — the
  finding they encode is unchanged and still true of `EscalationRecord`
  itself.

## 4. Real system work

[C] `§16`-equivalent (this program's standing rule): real execution, not a
unit test, not a mock, not a demonstrator.

[E] `p12_w3_governance_escalation.py` issues one real delegation (via the
existing, unmodified `W4DelegationRegistry`, reusing the `p12/w4-operations`
delegation root `tools/p12_provenance_verification.DELEGATION_ROOTS` already
searches — a new, unlisted root is exactly the defect that module's own
comment records having made once), runs a two-step plan through
`tools/w4_execution.W4Executor` where one step is genuinely outside the
delegation's `work_scope`, lets the executor refuse it for real, records the
refusal through the existing `record_refusals` helper (unmodified, reused —
the same one wiring path `tools/w4_first_run.py`,
`tools/w1_coordination_run.py` and `tools/w1_cross_department_run.py` already
share), and joins the resulting escalation to its grant.

[E] The run's `subject` text (`"P12-W3 real refusal proof for FD-P11-001
conformance — structural join only, no parsed reference intended"`) was
deliberately worded **not** to match the historical regex. Measured after the
run:

```text
records                          2   (1 historical + 1 real, this increment)
joined_by_structured_field       0   (EscalationRecord unmodified)
joined_by_parsed_prose           1   (the historical record only)
naming_the_refusal_type          0   (EscalationRecord unmodified)
joined_by_governance_surface     1   (this increment's record, and only it)
```

[D] **This is the falsification the increment exists to pass.** The new
record does not ride along on the old regex — `joined_by_parsed_prose` stays
at exactly `1`. It resolves only through
`tools/p12_governance_join_reader.py`, independently, which is proof the fix
is real rather than an artifact of matching the same convention that already
worked.

## 5. Independent verification

[E] `tools/p12_governance_join_reader.resolve_all` over
`docs/architecture/p12/w3-operations/`: **`JOINED`, 1 of 1**, delegation id
resolved against the live resident population, refusal type sanctioned.

[E] Negative controls, driven at runtime against a temporary copy of the real
records (`tools/p12_negative_control_verification._governance_join_writer`,
`._governance_join_reader`):

| Falsification | Result |
|---|---|
| an unsanctioned refusal type | refused, `GovernanceJoinError` |
| a second join over an existing one | refused, original survives unchanged |
| a join naming a delegation nobody issued | `DANGLING`, not `JOINED` |

[E] Sixteen conformance tests
(`tools/tests/test_p12_governance_escalation_join.py`): writer refusals (empty
delegation id, unsanctioned type, nonexistent escalation, duplicate write),
writer does not touch the escalation record it sits beside, reader imports
nothing from the writer (parsed by `ast`, not substring-matched), six
`DANGLING` cases resolved independently, and two tests reading the real
resident instance directly rather than a fixture.

## 6. Gap register

### W4-GAP-008 / W2-GAP-007 — escalation → grant join

- **Canonical requirement:** `§16` — governance integration must preserve
  `DECISION → AUTHORITY → RATIONALE → IMPLEMENTATION → VERIFICATION →
  CURRENT STATE`; `§34`/`§29` require a refusal traceable to its authority.
- **Original state:** joined only by regex over prose (`P12-W4-EXECUTION-INTEGRATION.md §13`).
- **Actual state:** `EscalationRecord` itself is unchanged and still joins
  only by prose for records that do not also carry a beside-join. A new,
  independently-resolvable structural join now exists and is proven against
  one real instance.
- **Classification:** **CONSTRUCTED — BESIDE THE RECORD.** Not
  `EscalationRecord` modification, not historical-record reinterpretation
  (`§22`: the one resident historical record, `23f315ba9f504272`, was not
  touched and gained no new file).
- **Verification:** independent reader, 16 conformance tests, 2 negative
  controls, real execution.
- **Remaining dependency:** none for this gap. Future refusals recorded
  through `record_refusals` **without** a follow-up call to
  `join_escalation_to_grant` will still join only by prose — the wiring is
  available, not mandatory, and making it mandatory would mean editing the
  three resident call sites, which is a further increment, not this one.

## 7. What this does not establish

[C] One real refusal is joined structurally. The historical escalation
(`23f315ba9f504272`) is not, and is not retroactively reinterpreted — `§22`
forbids manufacturing a join a record's author never captured.

[C] `tools/w4_first_run.py`, `tools/w1_coordination_run.py`,
`tools/w1_cross_department_run.py` do not call the new join function. Wiring
them is possible within the same delegated authority and is future,
independent `P12-W3` work, not implied by this increment.

[C] `W3 GOVERNANCE INTEGRATION AUTHORITY` (`§16`) is broader than this one
gap — the `DECISION → AUTHORITY → RATIONALE → IMPLEMENTATION → VERIFICATION →
CURRENT STATE` chain across Founder Decisions and ADRs generally was not
addressed here and remains open `P12-W3` scope.

[C] `W3 VERIFIED ≠ P12 VERIFIED ≠ P12 COMPLETE ≠ P12 CERTIFIED ≠ E12 RATIFIED`.
`F-16`, `F-17`, `F-18` were not approached. No Founder- or Architect-reserved
matter was settled. No Native Core subsystem was created — `EscalationGrantJoin`
lives in `tools/`, alongside `ExecutionManifest`, not in `native_core/`.

---

**Suite state at this record:** `native_core` 801 (1 expected failure) ·
`consumers` 276 · `tools` 1123 (net of this increment's 16 new tests and one
negative-control-coverage fix) · regression `0` of `12` classes regressed ·
mutation and fresh-process unchanged from the pre-increment baseline.
