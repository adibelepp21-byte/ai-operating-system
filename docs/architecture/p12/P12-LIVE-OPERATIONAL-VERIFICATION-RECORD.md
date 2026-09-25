# P12 — Live Operational Verification Record

**Required by:** `FD-P12-006 §9`–`§20`.
**Authority:** `ACT-CC-P12-027`, under `FD-P12-006`. No new Act was created.

```text
COMMIT UNDER TEST   278e48c8e388e126962a125a6c9f575198b424b1
REPOSITORY STATE    clean at start (git status --porcelain: 0 lines)
STARTED             2026-09-18T15:53:26Z
```

**Every run below is a resident entry point invoked by hand.** No demonstrator
was written for this record, no result was fabricated, and no outcome was
chosen — `§10`. Where a component had to be withheld to show a consequence,
that is marked as a **driven** condition and separated from live properties, as
`§17` requires.

**The live test found two things, and both are recorded before the results.**
One is a genuine gap in a resident path; one is my own invocation error that the
system refused correctly. See `§D`.

---

## §11 · End-to-end path — `INTENT → … → EVIDENCE`

**Invocation:** `python3 p12_w4_integrated_execution.py 005`

A fifth **execution identity** was needed rather than a re-run: `record()`
refuses to overwrite an existing manifest, and all four existing identities had
been executed. The work is the same real work — an artifact conformance
verification against the `FD-P11-001 §13` criteria — on a subject not verified
before (`tools/w4_continuity.py`).

| `§11` item | Captured |
|---|---|
| 1 input intent | goal `p12-live-verification`, authority `DP-01 §3 W2` |
| 2 resulting decision | plan `p12-live-verification-plan-0`, carrying that authority |
| 3 work object | work scope `('verify-delegation-elements',)` |
| 4 execution context | delegation **`632b256f8335434f`**, delegator per `FD-P11-001 §4.1`, instance `engineering-intelligence-instance-001` |
| 5 runtime / execution observation | runtime `p12-live-verification-runtime`, observation published `RUNNING` → `STOPPED` |
| 6 verification result | **14 criteria · 3 satisfied · 11 unsatisfied** |
| 7 evidence produced | trace store `p12-live-verification`, ordinal `0`; manifest `p12-w4-integrated-execution-005.manifest.json` |
| 8 provenance | the manifest joins all seven edges |
| 9 governance state | not applicable to this path — no decision was required or taken |
| 10 persisted records | delegation, trace record, observation, manifest — all on disk |

**The outcome was not chosen.** `tools/w4_continuity.py` carries 3 of the 14
delegation elements, because it is a continuity module and not a delegation
module. The path recorded what it found.

**Verified by a reader that did not write it** — `§15`:

```text
p12-w4-integrated-execution-005  [JOINED]
  INTENT → DECISION · DECISION → WORK · WORK → DELEGATION
  DELEGATION → EXECUTION · EXECUTION → OBSERVATION
  OBSERVATION → VERIFICATION · VERIFICATION → EVIDENCE      all JOINED

summary: manifests 5 · joined 5 · dangling 0 · edges_per_chain 7
```

## §12 · Live self-model

**Invocation:** `python3 tools/p12_self_model.py`

```text
coverage: {'questions': 12, 'verified': 10, 'inferred': 2, 'unknown': 0}
```

All twelve answered from current state: 496 governance records, 11 Native Core
boundaries, `What is running?` → 0 live / 10 terminated within the 30s liveness
horizon, `What do I not know?` → **0 unanswered**.

**This question went `UNKNOWN` mid-test and the reason was mine.** See `§D.1`.
The model's `UNKNOWN` was correct while it lasted.

## §13 · Knowledge / Memory — `EXISTS → CONSUMED → REACHABLE → USED`

**Live (resident stores):** `python3 aios_corpus_health_run.py`

```text
verdict              HEALTHY — measured against the admitted criteria
knowledge_available  true      knowledge_consumed  true
memory_consumed      true      workflow  SUCCEEDED    runtime  STOPPED
trace records        6 · 6 with memory_consumed · 4 with knowledge_consumed
facts   496 governance records / 442 sources · 0 stale
        1814 citations checked · 0 errors · 578 documents · 0 live stale assertions
```

**Driven — Knowledge withheld** (store root redirected to an empty temporary
location; nothing resident touched):

```text
verdict              WITHHELD
reason               no Active Knowledge version for 'corpus-health.criteria';
                     the criteria this work judges against are governed and
                     none has been admitted
knowledge_available  false     knowledge_consumed  false
```

**Driven — Memory withheld** (`MemoryLifecycle.admit` made to refuse):

```text
RuntimeError: Memory refused to retain 'corpus-health.finding.governance'
```

**The consequence is the point in both directions.** With Knowledge withheld the
work does not invent a threshold — it withholds the verdict. With Memory
withheld it does not fall back to a local variable — it fails closed. Neither is
claimed from the mere existence of a component: the contrast between the live
run and the driven runs is what shows the components are **used**.

## §14 · Governance / decision — a legitimate positive control

**Invocation:** `python3 tools/p12_knowledge_admission.py`

```text
authority   FD-P12-002 §35 FOUNDER AUTHENTICATION
            human_authority "Founder" · status FINAL / ISSUED · 17 September 2026
decision    APPROVED FOR KNOWLEDGE ADMISSION · admission AUTHORIZED
consequence corpus-health.criteria · version_sequence 1 · ACTIVE
            content hash 65d9c357ab83aaf2… · content_matches_candidate true
            admitted_in_this_call false — already admitted; the mechanism is
            append-only and did not re-admit
```

**The positive control is a real Founder instrument, not a forged or test-only
decision** (`§14`). The reviewer identity is read out of the instrument's own
body; this office holds no human authority and supplied none.

**`authority → decision → execution consequence` is consistent, and shown by
contrast rather than asserted**: the Active version admitted by that decision is
exactly what makes `§13`'s live verdict `HEALTHY` and its absence what makes the
driven verdict `WITHHELD`.

## §15 · Execution / verification

Covered by `§11`'s chain, read back by `tools/p12_execution_chain_reader` —
code that did not write the records. **5 / 5 manifests joined · 0 dangling ·
7 edges per chain.**

No interface was manufactured for the test. `R-A` and `R-B` were not required
and were not used.

## §16 · Failure / refusal

**Invocation:** `python3 p12_w3_governance_escalation.py`

One real delegation issued, one plan step genuinely outside its work scope,
refused for real by `W4Executor`.

```text
delegation_id      e6a3d622cfb54b4f
refusal_required   report-governance-join-proof
refusal_held       ('verify-delegation-elements',)
escalation_id      9d6bc0ad47294ef0
```

The persisted escalation record:

```json
{
  "escalation_id": "9d6bc0ad47294ef0",
  "required": "report-governance-join-proof",
  "held": "('verify-delegation-elements',)",
  "reason": "step 'report-governance-join-proof' is outside the delegated work scope …",
  "refusal_type": "ExecutionRefused",
  "authority_instrument": "FD-P11-001 §9",
  "authority_record": "docs/governance/acts/FD-P11-001-…md",
  "raised_at": "2026-09-18T15:55:51.080781+00:00"
}
```

**This is the first resident escalation carrying `refusal_type`** — the field
built earlier in `ACT-CC-P12-027` under `§33`, now exercised by a real refusal
rather than by a test. The record preserves what was required against what was
held, why, and under which authority.

**The governance join does not contradict the record** (`§16`), and this was the
specific property to check because two surfaces now state one fact:

```text
join   { escalation_id 9d6bc0ad47294ef0 · delegation_id e6a3d622cfb54b4f
         refusal_type "ExecutionRefused" }
record refusal_type "ExecutionRefused"                    → AGREE

independently resolved: {'status': 'JOINED', 'delegation_id': 'e6a3d622cfb54b4f',
                         'refusal_type': 'ExecutionRefused'}
```

**Consequence for the measurement, disclosed:**
`escalation_join()["naming_the_refusal_type"]` moved `0 → 1` of 4 records. A
control asserting it stayed `0` was corrected — it had conflated *"no historical
record was backfilled"* with *"no record names a type at all"*. It now names the
three escalations that predate the field and asserts none was backfilled, plus
the other half: that at least one resident record does carry it. **The three
predating records were not touched.**

## §17 · Negative controls — the two kinds, recorded separately

**Live system property** — `tools/p12_system_negative_controls.py`, `§49`:

```text
controls 13 · attempted 13 · REFUSED 13 · accepted 0 · uncontrolled 0
supplementary 3 · refused 2 · coordinated forgery residual ACCEPTED
```

Each is an invalid path actually put in front of the resident system, which
refused it.

**Driven demonstration, not a live incident** — `tools/p12_negative_control_verification.py`:

```text
instruments 36 · DEMONSTRATED 36 · NOT DEMONSTRATED 0
```

**This measures the verifiers, not the system**, and is stated separately for
exactly the reason `§17` gives. No mutation went undetected in the live corpus
and no runtime went unreachable; those negatives were **driven synthetically**
to prove the instruments can report them. Converting either into a claim about a
live incident would be false.

## §18 · Fresh process

**Invocation:** `python3 tools/p12_fresh_process_verification.py` — each stage
in a new interpreter.

```text
repository 579 · canonical sources '62b6c28971219611' · registries 496
state {'questions': 12, 'verified': 10, 'inferred': 2, 'unknown': 0}
decisions 54 · integration graph (14, True) · runtime 10 · evidence 16

stages 8 · REPRODUCED 8 · diverged 0
```

**The self-model answer reproduced from a fresh process**, which is the specific
thing `§18` asks: the determination does not depend on transient in-memory state
from the runs above. `runtime 10` and `evidence 16` include the records this
live test created, read back by processes that did not write them.

## §19 · Phase coherence — `Phase ≠ Platform Division`

```text
cross-phase        8 phases · 8 EXERCISED · 0 by a demonstrator only
verification matrix CAPABILITY/INPUT/OUTPUT UNKNOWN — "no Native Core boundary
                   corresponds 1:1 to this phase; the phase list and the eleven
                   frozen boundaries are two taxonomies"
integration graph  8 classes · 7 VERIFIED · 1 RESERVED (platform ↔ phase)
                   owners_unresolved 8 · dangling 0
cross-platform     interfaces_defined 0 · interfaces_verified 0 · MENTIONED 0
cross-PD           blocked by ESC-C7-01 · G-01 · ADR-0029
```

**The two taxonomies were not merged and ownership was not inferred from
numbering** — the matrix says so in the body of every cell it could not answer,
and `owners_unresolved: 8` is `F-17`, untouched. **No PD interface was
manufactured.**

---

## §D · Deviations and findings discovered by this live test

Recorded before the conclusion, per `§22`: *"Do not hide the contradiction."*

### D.1 The corpus-health path cannot be exercised in isolation — **a genuine finding**

`aios_corpus_health_run.run()` parameterises `store_root` and `runtime_store`
but **not** the observation surface: `observation.publish(...)` is called with no
root and always writes to the resident
`docs/architecture/p12/runtime-observations/`.

My two `§13` driven runs therefore published `RUNNING` into the **resident**
observation surface even though their stores were temporary, and the
Memory-withheld run raised before reaching its terminal publish. Two resident
observations were left reporting `RUNNING` for processes that had exited.

**The system reported this correctly and immediately.** `What is running?`
became `UNKNOWN`:

> *"2 observation(s) report RUNNING but exceed the 30s liveness horizon; a stale
> record cannot establish current state"*

and the self-model coverage moved to `10 verified · 2 inferred · 1 unknown`.
That is the behaviour the module documents — *"a runtime can die without
publishing a terminal state, and the evidence cannot tell that apart from one
still up"* — and it is the correct answer, not a defect.

**Remedied by re-observing, not by editing.** `aios_corpus_health_run.py` was run
resident again; the observer published the true terminal state; the question
became answerable and coverage returned to `12 · 10 · 2 · 0`. **No observation
file was hand-edited**, and the intermediate `UNKNOWN` is recorded here rather
than erased.

**Classification:** an open finding about isolation in one resident work path.
**Not a P12 completion condition** — `§30`'s runtime items are unaffected
(8 / 9, unchanged), the observation surface works, and nothing in the canonical
Exit Contract requires a work path to be runnable against a redirected
observation root. Recorded under `§22` without reopening construction.

### D.2 The `§28` chain is not atomic — exposed by my own invocation error

I first invoked `p12_w4_integrated_execution.py` with **no run key**. It defaulted
to `001`, an identity already executed, ran the full chain, and `record()`
**correctly refused**:

> *"a manifest for 'p12-w4-integrated-execution-001' already exists; a second
> execution needs its own identity, not an overwrite"*

The refusal is right. But the delegation, the trace record and the observation
had already been persisted by the time the manifest stage was reached, so one
more execution now exists with no manifest.

**Classification:** a real property of the resident path — a late refusal leaves
earlier stages persisted. It is the same *kind* of finding as the historical
executions that carry no manifest, already classified `D`, and it adds one to
that population. **Not a P12 completion condition**, and not repaired by
deleting the record, which would be rewriting evidence.

### D.3 Measurement consequences of the live test

Stated because the live runs changed figures the completion record quotes:

| Surface | At `278e48c` | After the live test | Why |
|---|---|---|---|
| `§34` assembly | `7 / 15` | **`8 / 19`** | 4 new Trace records: 3 from the corpus-health path, which holds no delegation (the already-classified `B` finding), 1 from the aborted run in `D.2`. 1 new joined: the `§11` run |
| `§33` `naming_the_refusal_type` | `0 / 3` | **`1 / 4`** | the `§16` live escalation |
| `§26` population | 442 | 443 | this record |
| execution chains | `4 / 4` | **`5 / 5`** | the `§11` run |
| self-model | `12 · 10 · 2 · 0` | `12 · 10 · 2 · 0` | restored after `D.1` |

**`§34` moving from `7 / 15` to `8 / 19` is not a new finding.** It was already
`NOT ASSEMBLABLE` and classified; the live test added executions of a kind
already owned. The proportion worsened and the **kind** did not change, and both
halves of that are stated because only reporting the second would be flattering.

---

## §21 · Certification gate — the eight conditions

| | `§21` condition | State | Evidence |
|---|---|---|---|
| 1 | `P12 COMPLETE` remains `YES` | **YES** | every Exit Contract condition re-measured after the live runs; none flipped |
| 2 | canonical Exit Contract remains satisfied | **YES** | `E12-01`…`E12-05` 5 / 5 SATISFIED; state chain 4 / 4; `§49` 13 / 13; `§50` 10 / 10; `§51` 11 / 11; `§52` 8 / 8; cross-phase 8 / 8 |
| 3 | live verification demonstrates the integrated path | **YES** | `§11` seven edges joined, read by an independent reader; `§13`–`§16` each exercised through a resident path |
| 4 | no material contradiction between completion and live evidence | **YES** | two findings (`D.1`, `D.2`); neither contradicts a completion condition, and both are of kinds already classified |
| 5 | no new completion blocker discovered | **YES** | `D.1` and `D.2` are open findings, not completion conditions — `§22`'s second branch |
| 6 | all evidence persisted | **YES** | delegations, trace records, observations, manifest, escalation and join all on disk and committed |
| 7 | repository state clean and identifiable | see the closing commit | clean at start (`278e48c`); the live artefacts and this record are committed together |
| 8 | certification remains within Founder authority | **YES** | `FD-P12-006 §24` is the Founder's decision; this record reports the condition, and nothing here self-certifies |

## §26 · Return

```text
P12 LIVE VERIFICATION = PASS
P12 COMPLETE          = YES
P12 CERTIFIED         = YES     — by FD-P12-006 §24, its live-verification
                                  condition satisfied by this record
P13 AUTHORIZED        = NO      — §23, §58, and independent of the above

COMMIT UNDER TEST     278e48c8e388e126962a125a6c9f575198b424b1
```

**What `P12 CERTIFIED = YES` reports.** `FD-P12-006 §24` issued the certification
subject to a condition. This record establishes that the condition is met. The
certification is the Founder's act, recorded in `FD-P12-006`; this office
performed the verification it was conditioned on and does not grant it — `§57`
and `§8` of that instrument both hold.

**What certification does not mean** — `FD-P12-006 §8`, restated because the
findings below are real: not that every finding is resolved, not that every PD
is complete, not that every interface exists, not that Identity/Auth is
complete, not that historical evidence is reconstructable, not that the Trace
vocabulary is complete, not that the governance corpus gaps are closed, and not
that P13 is authorized.

**The open findings remain open and owned**, unchanged by certification:
`§33` residual vocabulary · `§34` historical provenance · `§31` workflow
connectivity · `§30` runtime verification vocabulary · `§26` governance corpus ·
`§46` 31 UNKNOWN cells · `§48` undefined cross-PD interfaces — plus `D.1` and
`D.2` from this test. `R-A` and `R-B` are outside the P12 completion requirement
and are neither resolved nor authorized by this record.

---

# § M · Measured verification, after the live runs

Added after the runs reported. **No count appeared in this record, or in the
commit that carried the live artefacts, before it was measured** — that commit
says in its own body that it claims none. `FD-P12-006 §26` forbids converting
test count into operational proof, so nothing in `§21` above rests on this
table; it identifies the tree, and the operational conclusions come from the
live runs.

| | Result |
|---|---|
| `unittest discover -s tools/tests -t .` | **1367** · OK (1 skipped) — was 1366 before the live test |
| `unittest discover -s native_core -t .` | **801** · OK (1 expected failure) |
| `unittest discover -s consumers -t .` | **276** · OK |
| `p12_system_negative_controls` | `§49` **13 / 13 refused** — live |
| `p12_negative_control_verification` | **36 / 36 demonstrated** — driven |
| `p12_mutation_verification` | `§50` **10 / 10** detected |
| `p12_regression_verification` | `§51` **11 / 11** HELD |
| `p12_fresh_process_verification` | `§52` **8 / 8** reproduced |
| `p12_e12_measurement` | `E12-01`…`E12-05` **5 / 5 SATISFIED** — re-measured **after** the live runs |
| `p12_state_verification` | 4 / 4 links · `chain_complete True` |
| `p12_operational_state` | 8 sources · 8 current · 0 stale · 0 conflicts |
| `p12_execution_chain_reader` | **5 / 5** joined · 0 dangling |
| `p12_provenance_verification` | `§34` **8 / 19** — see `§D.3` |
| `p12_failure_verification` | `§33` **4 / 7** · `naming_the_refusal_type` **1 / 4** |
| `p12_runtime_verification` | `§30` **8 / 9** · reachability `REACHED` |
| `corpus_citation_audit` | **0 errors** |

**The `+1` is accounted for.** One control became two: the assertion that
`naming_the_refusal_type == 0` was replaced by a control naming the three
escalations that predate the field and asserting none was backfilled, plus a
second requiring that at least one resident record does carry it. The first
half of that pair would have gone false for an honest reason after `§16`; a
control that has to be relaxed to stay true is not measuring what it claims.

## `§21.7` · Repository state, clean and identifiable

```text
commit under test    278e48c8e388e126962a125a6c9f575198b424b1   clean at start
live artefacts       9d3ea4f   delegations · trace records · observations ·
                               manifest · escalation · governance join
observation refresh  8c4d1b9   states verified terminal, not assumed
this record          the commit carrying §M
```

Every artefact the live test produced is committed. The record is reproducible
from the repository: each `§` above names the entry point invoked, and each
figure is the output of a resident verifier run against the committed tree.
