# P12 F-4 — Runtime Observation · discovery, construction, verification

> **`F-4 CLOSED — VERIFIED`**, with coverage stated rather than implied.
> **`P12 CONSTRUCTED = FALSE`** — a frontier result is not a phase result
> (`Gate V`).

---

## 1. The hypothesis was false

`ACT-CC-P12-F4-001 §1` forbids assuming a runtime-observation subsystem must be
created. It need not be. **Runtime observation already exists, and is canonical:**

```text
native_core/core/runtime/lifecycle.py
  RuntimeState      CREATED → INITIALIZED → RUNNING → STOPPING → STOPPED
  VALID_TRANSITIONS enforced; illegal transitions raise
  AIOSRuntime.state exposes the live value
```

It is also **already fed**. Two resident root proofs — `w1_coordination_proof.py`
and `cross_department_coordination_proof.py` — start a real `AIOSRuntime` and read
`execution.runtime.state` while it is genuinely `RUNNING`, recording
`runtime_state RUNNING` and `after stop RuntimeState.STOPPED` in their evidence.

**What is absent is externalization.** `self._state` is an in-memory instance
attribute; no other process can see it. That is precisely what `derived_views`
recorded — *"Runtime state is per-process and unobserved from outside"* — and it
is a narrower gap than "no observation exists".

**A substring false positive of mine, disclosed.** My keyword sweep for
`heartbeat|lease|liveness|keepalive` returned hits in `runtime.py` and
`facility.py`. Every one was **`release`** / **`released`** — facility lifecycle,
matched inside the word. No liveness mechanism exists; the evidence for that claim
had to be re-derived by reading, not by grepping.

---

## 2. What F-4 actually required — and why freshness is the whole problem

A published record reading `RUNNING` is evidence that a runtime **was** running
when it was written. Answering *"what is running"* with it later is
`HISTORICAL EVIDENCE` wearing the label `LIVE RUNTIME STATE` — the first
substitution the Act names. So an observation is reported live only while fresh:

```text
RUNNING + fresh    → LIVE
RUNNING + expired  → STALE        not "running", and not "stopped"
STOPPED            → TERMINATED
no record          → UNKNOWN      not "0 running"
```

**`STALE` is deliberately not `TERMINATED`.** A runtime that dies without
publishing a terminal state is indistinguishable, from the evidence, from one
still up. Claiming it stopped would be as false as claiming it runs.

---

## 3. Construction — `tools/p12_runtime_observation.py`

A projection, not a subsystem. **Native Core is untouched**: the runtime boundary
remains the only producer of `RuntimeState`, this reads what it exposes, and `§11`
expressly permits integration layers outside the eleven frozen boundaries.
`git status` confirms **zero** changes under `native_core/`.

`publish()` never computes, defaults or guesses a state — it records the value a
real runtime reported, so a caller without a runtime has nothing to publish.

---

## 4. Gate H + Gate I — a live runtime, observed from another process

`p12_runtime_observation_proof.py` starts a real `AIOSRuntime`, and the
observation is taken by a **child interpreter** that receives no runtime object —
only the published record and its own clock. Gate I forbids letting the same
in-memory object prove its own observability.

```text
runtime.start()       state RUNNING, asserted in-process
publish               record written
child process         → answerable: true · live: [p12-f4-runtime-observation @ 0.04s]
runtime.stop()        state STOPPED, asserted in-process
publish               record overwritten
child process         → live: [] · terminated: [p12-f4-runtime-observation]
```

Between the two child observations **nothing changed but the runtime's actual
state**, and the observer is the same code both times.

---

## 5. Gate Q — mutation controls

| Mutation | Detector response | Result |
|---|---|---|
| fresh → expired (same `RUNNING` record) | `LIVE` → `STALE`, `answerable` false | **FIRED** |
| `RUNNING` → `STOPPED` | `LIVE` → `TERMINATED` | **FIRED** |
| record present → absent | answerable → `UNKNOWN` | **FIRED** |
| `STOPPED` aged to 99 999 s | stays `TERMINATED` — terminal states do not decay | **FIRED** |
| `CREATED` / `INITIALIZED` | neither live nor terminated | **FIRED** |

`attempted 5 · fired 5 · missed 0`. A test asserts the detector does **not**
return the same answer across all three conditions — a constant detector is not
verification.

## 6. Gate P — negative controls

| # | Attack | Result |
|---|---|---|
| 1 | hand-written `RUNNING` record for a runtime that never existed | **HELD** — obeys the horizon, reads stale |
| 2 | historical evidence offered as live state | **HELD** — stale never answerable |
| 3 | empty state presented as success | **HELD** — `absence is not zero` |
| 4 | stale presented as current | **HELD** |
| 5 | observation mutating what it reads | **HELD** — byte-identical after read |
| 6 | answer granting authority | **HELD** — no permission token in any result |
| 7 | `publish` defaulting a state | **HELD** — records only what it is handed |

`attempted 7 · held 7 · missed 0` — each exercised, none asserted.

---

## 7. Gate J — self-model integration

```text
BEFORE   9 VERIFIED · 2 INFERRED · 1 UNKNOWN
AFTER   10 VERIFIED · 2 INFERRED · 0 UNKNOWN
```

**`0 UNKNOWN` was an overclaim, and was corrected before commit.** An empty `live`
list does not mean *nothing is running* — it means nothing **observed** is
running. The answer now carries its own scope as data, not as a docstring
caveat:

```text
scope: runtimes that publish observations; unobserved runtimes are not covered
```

The model reverts to `UNKNOWN` the moment the evidence is removed, proved by
pointing it at an empty observation root rather than by asserting a count.

**`What is running?` is not answered from Trace.** A test asserts the source
contains `observation` and **not** `Trace`, and that the two answers differ.
`F-3`'s evidence may not close `F-4`.

---

## 8. Gate L — coverage, measured not claimed

**One of three resident runtime-driving paths publishes observations.**

| Path | Starts a real runtime | Publishes |
|---|---|---|
| `p12_runtime_observation_proof.py` | yes | **yes** |
| `w1_coordination_proof.py` | yes | **no** |
| `cross_department_coordination_proof.py` | yes | **no** |

`ONE REAL PATH ≠ SYSTEM-WIDE COVERAGE`. The canonical requirement in `§18` is that
the self-model answer the question evidence-backed, which it now does with its
scope stated — so **F-4 is closed on the narrower requirement it actually sets**,
and the coverage gap is recorded as a new frontier rather than absorbed.

---

## 9. Gate U — fresh rediscovery

| ID | Frontier | Evidence | Class |
|---|---|---|---|
| `F-10` | Runtime observation covers 1 of 3 resident runtime paths | two P11 root proofs start real runtimes and publish nothing | INTEGRATION GAP · authorized |
| `F-11` | `WorkflowState` is a second live-state vocabulary with no projection | `DEFINED · READY · RUNNING · SUCCEEDED · FAILED`; nothing observes it externally | STATE GAP · authorized |

**`F-11` is the more interesting one.** *"What is running?"* plausibly includes
running **workflows**, not only runtimes, and the workflow lifecycle already
carries `RUNNING` — a second live state, unobserved, in a system that now believes
it can answer the question.

Neither was closed here, and neither is assumed to be closable by the same
mechanism.

---

## 10. Verification

```text
native_core 801 OK (1 expected failure) · consumers 276 OK · tools 772 OK = 1849
citation 208 documents / 0 errors · stale-state 505 / 0 stale assertions
mutation: attempted 5 · fired 5 · missed 0
negative: attempted 7 · held 7 · missed 0
Native Core 11 frozen · native_core changes 0 · protected read 0 / staged 0
```

**Defects this increment.** One pre-existing-class false positive (`lease` inside
`release`) — mine, disclosed, corrected by reading. One overclaim (`0 UNKNOWN`
without stated scope) — mine, introduced and corrected before commit. Two API
misreads against the real bootstrap and `TracedAction` contracts — transient,
corrected. Four tests updated because construction changed the measured state,
each replaced with a stricter invariant.

```text
F-4 CLOSED — VERIFIED     F-10, F-11 OPEN — AUTHORIZED
P12 AUTHORIZED = TRUE     P12 CONSTRUCTED = FALSE     E12 NOT RATIFIED
```

---

# Addendum — `F-11` closed in the same loop

## 11. `WorkflowMonitor` was the third surface built and never called

`F-11` was recorded as *"`WorkflowState` is a second live-state vocabulary with
no projection"*. Discovery falsified the strong reading, exactly as it did for
`F-4`: **`WorkflowMonitor` is a canonical, ratified observation surface** under
`§12.4` / `E9-04`, answering Workflow identity, current lifecycle state,
active-or-terminal, and success-or-failure — and *"nothing else"*. It carries
**no** transition method by design, which is how `E9-04`'s *"invalid state
mutation does not silently succeed"* holds structurally rather than by
convention.

**It is called from zero resident paths.** Built, conformance-tested, never used
outside its own tests — the third instance of this shape in two days:

```text
Trace boundary     built, never called      → fixed by R2-A
Trace store        never provisioned        → fixed by F-3
WorkflowMonitor    never called             → fixed here
```

The pattern is worth naming: this system's recurring defect is not missing
capability, it is **capability that nothing reaches**.

## 12. Proof — a live Workflow seen from another process

`p12_workflow_observation_proof.py` drives a real lifecycle
`define → mark_ready → enter_running`, reads state **through `WorkflowMonitor`**
rather than from the lifecycle directly, and publishes it:

```text
child process, while RUNNING   → live_by_kind: {runtime: [], workflow: [p12-f11-…]}
lifecycle.succeed()
child process, after SUCCESS   → live_by_kind: {runtime: [], workflow: []}
```

## 13. The two vocabularies are kept apart

`Runtime RUNNING` and `Workflow RUNNING` are **not the same claim**. A Workflow
can run on a Runtime that is only `INITIALIZED`; a Runtime can be `RUNNING` with
no Workflow at all. Six tests hold the separation, including that Workflow
terminals (`SUCCEEDED` / `FAILED`) are never translated into the Runtime
vocabulary's `STOPPED`, and that a stale `RUNNING` workflow is no more live than a
stale runtime.

**A record without a `kind` defaults to `runtime`, stated in code.** The
observation committed before workflow support existed carries no `kind` field;
the default is explicit rather than guessed downstream, with a test against it.

## 14. A stale label of my own, caught by the same discipline

After extending the answer to workflows, the `scope` string still read
*"runtimes that publish observations"* — an answer covering two vocabularies
while naming one. Precisely the mislabelling `§112` recorded for
`recorded_supersessions`, committed again three sections later. Corrected, and
the test now **requires the scope to name both vocabularies** rather than
matching a fixed sentence.

## 15. Re-verification

```text
native_core 801 OK (1 expected failure) · consumers 276 OK · tools 778 OK = 1855
citation 208 documents / 0 errors · stale-state 505 / 0 stale assertions
native_core changes 0 · Native Core 11 frozen · protected read 0 / staged 0

F-4 CLOSED · F-11 CLOSED · F-10 OPEN — AUTHORIZED
```

**`F-10` remains open deliberately.** Closing it means wiring the two P11 root
proofs to publish, and those proofs write P11 evidence artifacts; re-running them
rewrites dated records. `§13.8` forbids rewriting historical evidence, so that
increment needs to add publication **without** disturbing what the P11 records
already say — a question about evidence integrity, not a missing line of code,
and not one to settle in passing.
