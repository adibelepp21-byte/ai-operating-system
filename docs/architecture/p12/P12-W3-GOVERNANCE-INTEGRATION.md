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

**Superseded by `ACT-CC-P12-005`, §14 below.** All three now call it. Not
withdrawn — the boundary this paragraph named was real at the time it was
written, and closing it is exactly the future increment it anticipated.

[C] `W3 GOVERNANCE INTEGRATION AUTHORITY` (`§16`) is broader than this one
gap — the `DECISION → AUTHORITY → RATIONALE → IMPLEMENTATION → VERIFICATION →
CURRENT STATE` chain across Founder Decisions and ADRs generally was not
addressed here and remains open `P12-W3` scope.

[C] `W3 VERIFIED ≠ P12 VERIFIED ≠ P12 COMPLETE ≠ P12 CERTIFIED ≠ E12 RATIFIED`.
`F-16`, `F-17`, `F-18` were not approached. No Founder- or Architect-reserved
matter was settled. No Native Core subsystem was created — `EscalationGrantJoin`
lives in `tools/`, alongside `ExecutionManifest`, not in `native_core/`.

---

## 14. `ACT-CC-P12-005` — resident consumption

[E] All three refusal-recording call sites now call one shared, additive
helper, `join_refusals_to_grants` (`tools/p12_governance_escalation_join.py`),
in place of calling `record_refusals` directly. It calls the unmodified
`record_refusals` internally (unchanged behaviour) and additionally joins
each resulting escalation to the grant the caller names —
`delegation.delegation_id` for the two single-grant sites
(`tools/w4_first_run.py`, `tools/w1_coordination_run.py`), and
`grants[refusal.required].delegation_id` for the one multi-grant site
(`tools/w1_cross_department_run.py`, one delegation per step). Neither
`EscalationRecord` nor `record_refusals`'s own signature changed.

[E] **Real, end-to-end proof through the actual resident call site.**
`p12_w3_resident_wiring_proof.py` calls `tools.w4_first_run.run` for real —
real agent registration, real delegation, a real out-of-scope step
`W4Executor` genuinely refuses, real escalation recording, real structural
join — with three narrow, disclosed substitutions so the run cannot corrupt
shared state: `OPERATIONS` stays the resident `docs/architecture/p12/w4-operations/`
root; `INSTANCE_KEY` is a fresh, non-colliding value, because the module's
own `engineering-intelligence-instance-001` is shared with
`p12_w4_integrated_execution.py`'s live grants in the same directory, and
`_revoke_stale_grants` would otherwise have revoked them; `project()` (a
different, `docs/architecture/p11/`-scoped organizational-state surface this
Act does not touch) is a no-op for this one call. Result:

```text
delegation_id      2494015de36246fd   (real, issued by W4DelegationRegistry)
escalations        ['9cb90fa0787a478c']
join                JOINED, independently, via tools.p12_governance_join_reader
delegation resolves independently:  True
```

[C] **A self-caught defect, disclosed rather than concealed.** The first
attempt at this script forgot to patch `OPERATIONS`, so it ran against the
real, certified `docs/architecture/p11/w4-operations/` for several stages
before the existing `tools/p12_certified_evidence_guard.guard` correctly
refused the final evidence write. Four new, real, but unwanted files had
already been written there (`§10`/`§21` — none pre-existing was modified;
`guard` did its job) and were deleted before being committed. The script was
corrected — `OPERATIONS` is now explicitly patched — and re-run cleanly. No
historical evidence was ever overwritten; the near-miss is recorded so it is
not repeated.

[E] **The other two sites cannot currently produce a refusal through their
own real scenarios, confirmed by reading their source, not by absence of
evidence.** `tools/w1_coordination_run.py`'s real plan has exactly two
steps, and `STEP_SKILLS` — the source of its granted `work_scope` — names
both; `tools/w1_cross_department_run.py` issues one grant per step, each
scoped to exactly that step. Neither can exceed its own grant today. This
matches, and now explains rather than merely observes,
`tools/tests/test_escalation_subject_integrity.py`'s own finding that *"no
W1 refusal has ever occurred."*

[E] **The multi-grant lookup, proven directly.** `tools/tests/test_p12_w3_resident_wiring.py`
builds two real delegations and two real refusals (real `W4Executor`, real
`W4DelegationRegistry`, no mocks) and asserts each escalation joins the
grant its own refusal named — `grants[refusal.required]`, not a shared
constant — plus a negative-fixture proving a naive constant lookup really
would mis-join one of the two. This is real work on the exact pattern
`tools/w1_cross_department_run.py` now uses, independent of whether that
site's own historical scenario ever exercises it.

[C] **A second, self-caught defect: `escalation_join()`'s new-surface count
only checked one hardcoded directory.** Written under `ACT-CC-P12-003`
against `docs/architecture/p12/w3-operations` alone, it silently missed the
real join this increment produced in `docs/architecture/p12/w4-operations` —
the exact `DELEGATION_ROOTS`-shaped defect
`tools/p12_provenance_verification.py`'s own comment already names once.
Found by re-running the measurement against the new evidence rather than
trusting the old figure. Fixed to resolve each escalation's join beside
whichever directory that escalation actually lives in:

```text
records                          3   (1 historical, 1 P12-003, 1 P12-005)
joined_by_structured_field       0   (EscalationRecord still unmodified)
joined_by_parsed_prose           2   (historical + this increment's; the
                                      P12-003 record was deliberately worded
                                      not to match)
joined_by_governance_surface     2   (both real joins, resolved independently,
                                      each in its own directory)
```

[C] **A known, unchanged semantic limitation, preserved not upgraded.** The
join resolves whether a named delegation *exists*, not whether it is
currently `ACTIVE` — a revoked grant still resolves `JOINED`. This is the
same standard `joined_by_structured_field` always used and is not new to
resident wiring; recorded because `ACT-CC-P12-004` disclosed the adjacent
"is this the *specific* grant the refusal named" limitation and this one is
its sibling, not because either changed this Act.

### Three-site coverage

| Call site | Wired | Reachable | Real refusal possible today | Invoked with real content | Independently verified |
|---|---|---|---|---|---|
| `tools/w4_first_run.py` | YES | YES | YES (`report-conformance` outside `work_scope`) | YES, this Act | YES — real run, independent reader, fresh process |
| `tools/w1_coordination_run.py` | YES | YES | NO — both real steps are always in scope | NO — never, by construction | wiring pattern verified via `w4_first_run`'s identical single-grant shape |
| `tools/w1_cross_department_run.py` | YES | YES | NO — each grant always covers exactly its own step | NO — never, by construction | multi-grant lookup verified directly, real objects, `test_p12_w3_resident_wiring.py` |

**Not `3/3 operational`.** One site is wired, reachable, and exercised with
real content this Act. Two are wired and reachable, and — by the shape of
their own real work, not by any limitation in the join — have never
produced, and today cannot produce, the condition the join exists to
handle. Their wiring's correctness rests on direct proof of the pattern
each uses, not on an occurrence that has never happened.

---

**Suite state at this record:** `native_core` 801 (1 expected failure) ·
`consumers` 276 · `tools` 1113 (net of `ACT-CC-P12-005`'s 4 new tests, one
rewritten test, and one bugfix to `escalation_join()`) · regression `0`
classes regressed · fresh-process unchanged.
