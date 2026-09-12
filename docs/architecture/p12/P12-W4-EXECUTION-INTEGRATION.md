# P12-W4 — Execution Integration

**Act:** `ACT-CC-P12-W4-001`.
**Status:** [E] two real executions keep the whole `§29` contract and are verified
independently. **7 of 7 canonical edges JOINED** for both executions run under it —
one success, one failure; 3 older executions remain unjoined and were not retroactively joined.
**Instruments:** `tools/p12_execution_provenance.py` (writer) ·
`tools/p12_execution_chain_reader.py` (independent reader) ·
`p12_w4_integrated_execution.py` (the real path).
**Conformance:** `tools/tests/test_p12_execution_chain.py` (27 tests, including
`§23` Tests A–H and Test G at corpus level).

---

## 1. The W6 finding this Act acted on was wrong, and falsifying it came first

[C] `ACT-CC-P12-W4-001 §4` requires every W6 finding be independently reproduced
before being acted on, and `§10` W4-D3 says plainly: *"Do not merely reproduce
the earlier 9/11 measurement. Try to falsify it."*

[E] **It falsified.** `P12-W6-PROVENANCE-VERIFICATION.md` reported 9 of 11 `§34`
elements carried and **0 of 2 executions assemblable**. That measurement read
two surfaces: delegation records and Trace records. It did not read the resident
`*.evidence.json` execution records, which carry `goal`, `plan`,
`plan_authority`, the step-to-grant mapping, `workflow_steps`, `delegation_id`
and `authority_chain` **in one artifact** — precisely the join the module
reported missing.

[E] Corrected measurement over the full population:

| | before | after |
|---|---|---|
| `§34` elements carried | 9 of 11 | **11 of 11** |
| executions joined | 0 of 2 | **3 of 3 evidence records, 0 of 4 Trace records** |

[D] The finding was **true of the surfaces measured and false as a statement
about the system**. The conformance controls that asserted `absent_elements ==
("workflow", "evidence")` and `executions_joined == 0` encoded that falsehood
and were corrected — *because they were wrong*, not to make an implementation
pass. The corrected element control asserts a **stronger** result.

## 2. The real gap, which is narrower and is mine

[E] The P11 `*.evidence.json` path records the join. The durable Trace path built
under P12-W4 does not: it records an actor, a runtime and outputs, and nothing
naming the grant under which the work ran. Worse, the P12 trace path **issues no
delegation at all** — it names an instance, and no grant authorizes that specific
execution.

[D] **The newer surface lost a relation the older one had.** That is the W4 gap,
and it was introduced by this programme's own P12-W4 construction.

## 3. What was built, and why it is not inside `TraceRecord`

[C] `ACT §9` and `STOP-G` forbid widening `TraceRecord` to solve a join:
`TRACE RECORD ≠ UNIVERSAL RELATIONSHIP DATABASE`. It is also closed in practice —
`from_mapping` reconstructs only the ten required fields, so a key written into a
Trace record is **silently dropped on read**. A conformance control asserts that
drop directly against Native Core.

[C] So the relation lives beside the Trace record, on a P12 surface, and names
it. **No Native Core file was modified. No ratified vocabulary was widened. No
twelfth subsystem was created.**

- **`ExecutionManifest`** — resolves all twelve `§29` elements and **refuses to
  be written incomplete**: a partial manifest would claim a contract the
  execution did not keep. It also refuses to overwrite: a second execution needs
  its own identity, not a replacement of the first.
- **`p12_execution_chain_reader`** — `§24` forbids
  `IMPLEMENTATION → SELF-REPORT → PASS`, so the reader **imports nothing from the
  writer**, reads bytes off disk, and resolves every reference against the record
  it points at. A conformance control parses the reader's imports and fails if it
  ever imports the writer.

## 4. Real system work

[C] `§16` forbids proving W4 by unit tests, mocks, synthetic graphs, static
inspection, fabricated rows, or demonstration-only scripts.

[E] `p12_w4_integrated_execution.py` runs the chain once, each stage producing
the artifact the next refers to: a declared Goal → an adopted Plan carrying its
authority → a work scope → **a real delegation issued by the delegator
`FD-P11-001 §4.1` names** → real conformance work written through `TraceWriter`
to durable storage → a runtime observation **published under the execution's own
runtime identity** → the outcome recorded against the delegation's verification
requirement → one manifest joining all of it.

[E] The work performed is real: 14 conformance criteria against
`tools/w4_delegation.py`, result `14 satisfied, 0 unsatisfied`. The manifest
records that outcome; it does not choose it. The script deliberately issues **no
verdict** — `§24` requires the verdict to come from the reader.

[E] Independent verdict: **`JOINED`, 7 of 7 edges**, every reference resolved.

## 5. `§23` falsification — and the one that broke my construction

[E] All eight named tests are implemented and attack the **reader**, because a
join only the writer believes in is not a join.

| `§23` test | Result |
|---|---|
| A — wrong delegation | a nonexistent grant is `DANGLING`; a real grant issued to another recipient is refused |
| B — wrong work | work outside the granted scope is refused |
| C — missing execution | an ordinal past the end, and an absent store, are `DANGLING` |
| D — missing observation | an unobserved subject gives **no verified closure** |
| E — missing evidence | an unpersisted manifest gives no closure; an incomplete manifest is never written |
| F — process restart | the chain verifies in a fresh interpreter |
| G — duplicate actor | **see below** |
| H — stale observation | the terminated execution is not reported live |

[E] **Test G failed on first run.** Substituting a *different grant held by the
same actor* still verified. The reader checked `actor == recipient`, which is
true for every grant that actor holds — and this actor holds seven.

[D] **That is the shared-name defect reappearing inside the fix built to remove
it.** Found by falsification, not by review.

[E] Fixed by requiring the binding that actually ties a grant to an execution:
the delegation's `lifecycle_boundary` names the plan it was issued for. A grant
bound to another plan authorizes another execution, whatever its scope says. The
live chain still joins under the stronger check.

## 6. Two further defects in my own measurement, disclosed

1. **A manifest appeared to join two Trace records.** The first version matched
   manifests to traces on `runtime_id` + actor — **a name match, in the module
   that exists to reject name matches, for the third time.** Both records of the
   integrated store shared a runtime identity, so one manifest counted twice.
   Traces are now addressed by store and ordinal, exactly as a manifest
   addresses them, and the count fell from `2/4` to the correct `1/4`.

2. **The P12 delegation root was missing from the provenance module's search
   path.** The new grant was written to `docs/architecture/p12/w4-operations`,
   which was not in `DELEGATION_ROOTS`; the module reported the join missing
   because it was not looking where the grant was written.

[C] A third was not mine but was caught the same way: the line-locator guard
flagged the manifest surface for an interpolated `kind:subject` reference. The
shape was removed rather than the guard loosened, as before.

## 7. `§35` Gap register

### W4-GAP-001 — DELEGATION → EXECUTION

- **Canonical requirement:** `§29` — each material execution preserves authority
  and provenance; `§34` — provenance identifies the delegator and authority.
- **Original state (W6):** `0/2 executions joinable`.
- **Actual state:** the W6 figure was measured over an incomplete population.
  True prior state: `3/3` evidence-record executions joined, `0/2` Trace-record
  executions joined.
- **Falsification:** attempted and **succeeded** — the evidence-record surface
  carried the join all along.
- **Authority:** P12-W4 delegated.
- **Classification:** **PARTIAL → CONSTRUCTED.**
- **Remediation:** execution provenance manifest, written by the execution,
  resolved by an independent reader.
- **Verification:** 7/7 edges `JOINED`; `§23` Tests A, B, G refuse false joins.
- **Final state:** `4/7` executions joined corpus-wide. **Not 7/7, deliberately**
  — see W4-GAP-006.
- **Remaining dependency:** none.

### W4-GAP-002 — DECISION → WORK

- **Canonical requirement:** `§28` — WORK is mandatory and may not be elided.
- **Actual state:** the plan carries its authority citation and its steps; the
  delegation's `lifecycle_boundary` names the plan.
- **Classification:** **NOT-A-GAP** — verified, and now load-bearing: this
  binding is what `§23` Test G forced the reader to check.

### W4-GAP-003 — WORK → EXECUTION

- **Original state (W6):** `BY CONVENTION`, actor name only.
- **Actual state:** `4/7` executions name the work they performed.
- **Classification:** **PARTIAL.** Reported `BY CONVENTION` because the weakest
  link governs — a chain most executions satisfy is not one that can be followed
  for an arbitrary execution.

### W4-GAP-004 — EXECUTION → OBSERVATION

- **Original state (W6):** `BROKEN` — no execution runtime matched any observed
  subject.
- **Actual state:** **`EVIDENCED`.** The integrated execution publishes its
  observation under its own runtime identity, and the reader resolves the
  manifest's `observation_subject` against a published observation.
- **Classification:** **BROKEN → CONSTRUCTED**, by real execution rather than by
  changing what the verifier accepts.

### W4-GAP-005 — OBSERVATION → VERIFICATION → EVIDENCE

- **Original state (W6):** `BROKEN` — the ratified execution vocabulary
  `{success, failure, escalation}` holds no verified state.
- **Actual state:** **still true, and not changed.** The edge is carried by the
  manifest, which records the delegation's verification requirement together
  with the observed execution's outcome.
- **Classification:** **CONSTRUCTED ON THE P12 SURFACE**, which is the separation
  `§9` requires. The vocabulary finding in
  `P12-W6-FAILURE-VERIFICATION.md` stands unchanged, and a conformance control
  asserts `"verified" not in VALID_STATUSES` so it cannot quietly become false.

### W4-GAP-006 — historical executions

- **Actual state:** three Trace records carry no manifest — two from the earlier
  durability proof, one from a first attempt of the integrated run that failed at
  the evidence stage after its work had already executed.
- **Classification:** **OUT OF SCOPE — HISTORICAL INTEGRITY.**
- [C] Writing manifests for them would be manufacturing historical evidence.
  `§22` forbids it and `§19` of the governing W6 Act requires new evidence to come
  from `NEW REAL EXECUTION → NEW OBSERVATION → NEW EVIDENCE`. They stay unjoined,
  and the corpus-wide figure stays `4/7` rather than being driven to `7/7`.

### W4-GAP-007 — runtime reachability

- **Canonical requirement:** `§17`, `§29` of the Act — resident entry,
  reachability, execution, observation, evidence.
- **Actual state:** **unchanged.** Eight root entry points, `HAND-INVOKED ONLY`.
  The integrated execution is itself hand-invoked.
- **Classification:** **BLOCKED — DEPENDENCY.** A resident non-manual entry means
  a scheduler, service or dispatcher deciding *when* AIOS acts. That is an
  operational-authority question, not an execution-integration one, and
  constructing one inside W4 would establish operational authority by engineering
  convention — `STOP-D`.

## 8. `§38` Regression

[E] Pre- and post-construction: **no regression.**

```text
certified phases 10, 11 unchanged · 2 protected roots · 0 certified-evidence changes
regression verification 11 classes · 10 held · 0 regressed
mutation 10 named · 9 attempted · 7 detected  (unchanged)
cross-phase 8 phases · 6 exercised  (unchanged)
fresh process 8/8 reproduced  (unchanged)
§49 system controls 13 attempted · 11 refused  (unchanged)
negative controls 18 instruments · 18 demonstrated
F-4, F-5, F-10′, F-11, F-12 valid · F-15 still a false positive
no verifier weakened to obtain PASS
```

## 10. `§26` The chain carries a non-success outcome

[C] `§26`: *"W4 must not assume only successful execution."* A terminal state
nothing has ever reached is not a state the system distinguishes, and the chain
had only ever carried a success.

[E] A second real execution was run against an artifact the work genuinely fails
against: `tools/p12_execution_provenance.py` does not contain the
`FD-P11-001 §13` delegation element names. **The criteria are identical in both
runs and nothing was injected** — only the subject differs, and the outcome is
whatever the verification produced.

```text
001  subject tools/w4_delegation.py              14 criteria · 14 satisfied · success
002  subject tools/p12_execution_provenance.py   14 criteria ·  5 satisfied · failure
```

[E] Both chains verify **`JOINED`, 7 of 7 edges**. The failure carries the chain
as completely as the success: its Trace record holds `status: failure`, its
manifest holds the unsatisfied criteria by name, and its observation resolves.

## 11. `§23` Test G, at corpus level

[E] The two executions share **one actor** — `engineering-intelligence-instance-001`
performed both — and are distinguished by grant, not by name:

- two distinct `delegation_id` values, each bound to its own plan;
- two distinct trace addresses, `store` and `ordinal`;
- **swapping the two real grants breaks both chains**, verified against
  persisted records rather than a mutated copy.

[D] This is the strongest available form of the test: the earlier version
substituted a grant belonging to an older programme run, and this one swaps two
grants issued minutes apart to the same actor under the same integration. The
join holds because it resolves a binding, not because the names differ.

[E] Corpus state after the second run: **5 of 8 executions joined**, `2/5` Trace
records, 2 manifests. The three unjoined remain unjoined.

## 12. `§25` Fresh-process rediscovery

[E] Five stages, each re-derived in two independent fresh interpreters:
canonical state, integration relations, persisted records, verification,
manifests. **5 reproduced, 0 diverged.**

[C] The first run of this comparison reported two divergences. **Both were a
defect in the comparison harness** — it compared an in-process tuple `(5, 8)`
against the string `'5 8'` printed by the subprocess. Disclosed rather than
quietly corrected, because a harness that manufactures divergence is as
misleading as one that hides it, and this one would have reported a false
regression in the work it was checking.

## 13. `§26` REFUSED and ESCALATED — W4-GAP-008

[E] Both states are reached and persisted: `EscalationRequired` and
`ExecutionRefused` are raised and recorded, and one escalation record is
resident.

[E] Measured, not asserted (`tools/p12_failure_verification.escalation_join`):

```text
escalation records                 1
joined by a structured field       0
joined by parsed prose             1
naming which refusal type          0
```

[D] The refusal **does** reach the grant it was refused under — through a regex
over the record's prose `subject` field. That works until somebody rewords the
subject. **It is the same class of fragility as joining on an actor name: the
relation is carried by a spelling rather than by a reference.**

- **Classification:** **PARTIAL — DEPENDENCY (P12-W3).**
- [C] **Not constructed here.** `EscalationRecord` is a frozen, written-once
  governance surface, and adding a structured delegation field or a refusal-type
  field to it is governance-integration work. `ACT §30`: `W4 ≠ W3`, and
  absorbing the escalation record into W4 would be exactly the silent absorption
  it forbids.
- [C] A conformance control asserts the current values and says in its own
  message that the finding closes if escalation records gain the field.

## 14. Remaining W4 frontier

[E] Re-discovered after construction. **No actionable authorized W4 frontier
remains.**

| Item | Classification | Why it stops here |
|---|---|---|
| W4-GAP-003 historical executions | OUT OF SCOPE | manifests for them would manufacture history (`§22`) |
| W4-GAP-007 runtime reachability | BLOCKED | a resident non-manual entry decides *when* AIOS acts — operational authority, `STOP-D` |
| W4-GAP-008 refusal join | DEPENDENCY (W3) | `EscalationRecord` is a governance surface; `W4 ≠ W3` (`§30`) |

## 9. What this does not establish

[C] Two executions keep the whole contract. **Six others do not**, and three of
those cannot without fabricating history.

[C] `§17` runtime reachability is **not** resolved. The chain is integrated; the
runtime is still entered by a person.

[C] `W4 VERIFIED ≠ P12 VERIFIED ≠ P12 COMPLETE ≠ P12 CERTIFIED ≠ E12 RATIFIED`.
`F-16`, `F-17`, `F-18` were not approached. No Founder- or Architect-reserved
matter was settled.

---

**Suite state at this record:** `native_core` 801 (1 expected failure) ·
`consumers` 276 · `tools` 1025 · total **2102**.
