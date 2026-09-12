# P12-W6 — Runtime and Workflow Integration Verification

**Scope items:** `§19` **RUNTIME** (`§30`) and **WORKFLOW** (`§31`).
**Status:** [E] measured.
RUNTIME — **8 of 9 items discovered · 1 absent · reachability HAND-INVOKED ONLY.**
WORKFLOW — **2 of 5 joins evidenced · 1 by convention · 2 broken · chain NOT connected.**
**Instruments:** `tools/p12_runtime_verification.py` ·
`tools/p12_workflow_verification.py`
**Conformance:** 12 tests · 15 tests.

---

## PART A — RUNTIME (`§30`)

### A.1 What `§30` asks

[A] `§30` requires discovery of nine things and closes: *"Claims about runtime
integration require runtime evidence where runtime evidence is the relevant
proof."*

[C] **Two questions, reported separately and never merged.** Discovery asks
whether each item has resident runtime evidence. Reachability asks what `§30`
implies without spelling out: whether the runtime is entered *by the system* or
only by hand. Merging them would let nine green discoveries describe a system
that never runs.

### A.2 Discovery result

| `§30` item | Status | Measured |
|---|---|---|
| runtime entry points | DISCOVERED | 7 root entry points |
| runtime state | DISCOVERED | 2 published runtime observations |
| runtime-hosted workflows | DISCOVERED | 1 workflow observation |
| execution actors | DISCOVERED | 1 distinct actor in durable records |
| state transitions | DISCOVERED | 2 distinct observed states |
| observation | DISCOVERED | answerable, 3 observations |
| **verification** | **ABSENT** | ratified vocabulary is `{success, failure, escalation}` |
| failure | DISCOVERED | 1 durable failure record |
| persistence | DISCOVERED | 1 trace store, observation root present |

### A.3 The finding: the runtime is entered only by hand

[E] **`HAND-INVOKED ONLY`.** No root entry point is reached from any surface
other than a hand-run script. There is no service, no scheduler, no dispatcher
that enters the runtime. Of the seven, six are imported by nothing at all, and
the seventh is imported by another root script which is itself imported by
nothing.

[C] **Measured from the import graph, not from file names.** Classifying an
entry point as a demonstrator because it is called `..._proof.py` would be
inference from a name — the thing this programme repeatedly has to undo. A
conformance control parses this module and fails if any *executable* string
literal contains `_proof`, so the name-based shortcut cannot creep back in.

[C] Two hand-invoked scripts do not make one reachable. A caller that is itself
only hand-invoked is excluded, and a control fixes that choice against the one
real instance in the corpus.

[D] This sharpens the programme hypothesis rather than confirming it. The
capability is not merely reached only by its own demonstrator — **the runtime
has no non-manual entry at all.** `§30` says runtime claims require runtime
evidence; the resident runtime evidence is real, and every run that produced it
was started by a person.

---

## PART B — WORKFLOW (`§31`)

### B.1 What `§31` asks

[A] `§31`: workflow must connect `PLAN → HANDOFF → WORK → EXECUTION →
OBSERVATION → VERIFICATION`, and *"P12 must verify actual workflow behavior
rather than merely inspect definitions."*

[C] **The unit measured is the link, not the element.** Six present elements
prove nothing about a chain — `§48`: a relationship is not verified merely
because both surfaces exist. So the five joins are measured, and each is
`EVIDENCED` (an artifact names both sides), `BY CONVENTION` (the only connection
is a shared name), or `BROKEN`.

### B.2 Result

| Join | Status | Evidence |
|---|---|---|
| PLAN → HANDOFF | EVIDENCED | `delegation.lifecycle_boundary`, 24/24 name their bound plan |
| HANDOFF → WORK | EVIDENCED | `delegation.work_scope`, 24/24 declare authorized work |
| **WORK → EXECUTION** | **BY CONVENTION** | actor name only |
| **EXECUTION → OBSERVATION** | **BROKEN** | no execution runtime matches any observed subject |
| **OBSERVATION → VERIFICATION** | **BROKEN** | no execution record can hold a verified state |

[E] `chain_connected: False`.

### B.3 The findings

[E] **`WORK → EXECUTION` is held together by a shared actor name.** This is the
same break `§34` provenance found, reached from the other direction: an
execution record carries no reference to the work it performed. One actor holds
many grants, so a name identifies a set, not a link.

[E] **`EXECUTION → OBSERVATION` is broken.** The executions that produced
durable traces ran under `p12-w4-durability-proof`; the published observations
are of `p11-w1-runtime`, `p12-f4-runtime-observation` and
`p12-f11-workflow-observation`. **No name appears on both sides.** Runs that
produce execution records are not observed, and runs that are observed produce
no execution records.

[E] **`OBSERVATION → VERIFICATION` is broken.** Nothing an observation reaches
can record that the thing observed was verified: the ratified execution
vocabulary has no verified state.

[C] `BY CONVENTION` never counts as connected, and a conformance control asserts
it. A convention is how a chain looks joined until two things happen to share a
name.

---

## PART C — Two defects in these instruments, disclosed

[C] Both were caught by running the modules, and both would have overstated a
defect in the system.

1. **The runtime observation probe called `len()` on a count.** `observations`
   in the `what_is_running` answer is an integer. The probe raised `TypeError`
   and the item was reported `ABSENT` with the exception as its reason — **a
   working observation surface reported as missing by a defect in the thing
   measuring it.** Fixed; a conformance control asserts no probe ever reports
   its own exception as a finding.

2. **The workflow observation join read a field that does not exist.** It read
   `Observation.subject`; the real field is `runtime_id`. The join was reported
   `BROKEN` with an `AttributeError` as its reason. It is still `BROKEN` after
   the fix — but for a measured reason rather than a crash, and the difference
   is the whole point. A control asserts the dataclass has `runtime_id` and not
   `subject`, so the finding rests on the real shape.

[C] A third defect was in a conformance control rather than a module: the check
forbidding name-based classification scanned every string constant and matched
this module's own docstring — the paragraph explaining that names are *not*
used. Docstrings are now excluded. It is the same shape as the line-locator
guard that matched the comment describing it.

---

## PART D — What this does not establish

[C] Eight discovered items say eight kinds of runtime evidence exist. They do
not say the runtime is integrated — the reachability result says it is not
entered by anything but a person, and the two are reported side by side so
neither can stand in for the other.

[C] Two evidenced joins say two links are carried by a real reference. They do
not say the workflow behaves correctly, only that those two links exist as more
than a coincidence of naming.

[C] No ratified vocabulary was widened, no record shape changed, no entry point
added. **RUNTIME and WORKFLOW are truthfully classified here; neither is
closed.**

---

**Suite state at this record:** `native_core` 801 (1 expected failure) ·
`consumers` 276 · `tools` 975 · total **2052**.
