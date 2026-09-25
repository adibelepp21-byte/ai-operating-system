# S-OPS — Operational Proof Surface: Definition v1.0

| Field | Value |
|---|---|
| **Surface** | S-OPS, the dedicated operational proof surface for E13-05 |
| **Owner** | **S-OPS operational proof surface** (this definition, its object, and `tools/s_ops/`). Ownership is not transferred from P1–P12 or P11 |
| **Authority** | `FDR-3` (Decision Register `§23`): *"a dedicated bounded operational object (S-OPS) as the first live proof surface for E13-05"*, with *"only the minimum authority required to construct and execute that S-OPS proof"* |
| **Executable form** | envelope `P13-ENV-02` (Delegation Register `§15`): the two transitions below, on the one object below, and nothing else |
| **Object** | `docs/operations/s-ops/S-OPS-01.json` (one object; this surface has no other) |
| **Defined by** | Claude Code — AIOS Co-Founder + Delegated CEO, under `FDR-3` `§6`–`§7` (the design is delegated to discovery and architectural reasoning) · 2026-09-24 |
| **Certification** | NOT GRANTED. A proof on this surface certifies nothing |

## 1. Discovery: can an existing surface serve?

`FDR-3` `§6` requires this question to be answered before anything new is
designed, and *"Do not select a candidate merely because it is technically
writable."* Each surface below was checked on all nine dimensions. It fails on
at least one of them, marked **✗**.

| Candidate | Semantics | Owner | P13 may mutate under FDR-3? | Boundary | Reversible by P13 | Observable | Consequence | Isolation | Proof value |
|---|---|---|---|---|---|---|---|---|---|
| P13 cycle records and Trace (`docs/operations/p13/`) | **✗** epistemic: P13's own evidence | P13 | **✗** excluded (*"P13's own knowledge/evidence state"*) | yes | **✗** append-only | yes | none on the world | yes | none |
| residual frontier register | **✗** epistemic (definition `§18`) | P13 | **✗** excluded by name | — | — | — | — | yes | none |
| escalation records (`OPEN → ANSWERED`) | operational | P11 register; a human answers | **✗** only a human records a response (`HumanAuthority`) | yes | **✗** | yes | the *escalate* leg, not *execute* | P11 register | none for *execute* |
| live runtime observations (`docs/operations/runtime-observations/`) | operational | **✗** P12 runtime publication | **✗** P13 would have to host a Runtime (Blueprint `§4`, `D06`) | — | — | yes | — | **✗** P12 | — |
| agent instances, W4 delegations and operations, Planning (`tools/planning`, P11-W2) | operational | **✗** P11 | **✗** `I-08`; certified P11 roots | — | — | yes | yes | **✗** P11 | — |
| Knowledge versions | operational | **✗** P6 / governance | **✗** governed admission; certified | — | — | yes | — | **✗** | — |
| `GOVERNANCE_INDEX.md`, the Registers, `p13-envelopes/` | governance | governance | **✗** *"a governance artifact whose mutation could alter authority"* | — | — | yes | — | **✗** | — |
| P13 execution hold (package `S-HOLD`) | operational | **✗** P13 itself | **✗** it gates P13's own gate: P13 changing its own authority to act (`I-06`) | yes | **✗** by design, only a human releases | yes | restricts P13 only | yes | partial |
| corpus citation repair (package `S-CITE`) | operational | **✗** each document's author; many are canonical P1–P12 records | **✗** P1–P12 artifacts; arbitrary repository write | **✗** open-ended | human edit | yes | yes | **✗** | yes |
| Workflow and Tool lifecycles | operational | **✗** P9 / Native Core | **✗** | — | — | **✗** in memory only | — | **✗** | — |

**Result: no existing surface is adequate.** Every operational surface is owned
by P1–P12 or P11, or is governance, or would let P13 change its own authority.
Every surface P13 owns is epistemic. A dedicated surface is constructed
(`FDR-3` `§7`).

## 2. Why a scheduled window

The state model is taken from patterns the repository already uses. It is not
invented for the proof:

* **Recorded state bound to time.** P13 envelopes carry an `expires` date. The
  gate reads a Register entry marked ACTIVE as no authority once that date
  passes (`tools/p13/authority.py`, check 8). W4 grants likewise carry validity
  windows. In both, a recorded state must follow a schedule it cannot follow by
  itself.
* **A parameter set by an operator, a state changed by the system.** An
  escalation's subject is set by whoever raises it; its lifecycle is moved by
  someone else. Here the operator sets the schedule, and only P13 moves the
  state.

An operational window has exactly those properties:

* a finite state, OPEN or CLOSED;
* a schedule fixed when the window is provisioned;
* a contract that says which state the schedule requires at any moment.

When the clock crosses a boundary of the schedule, the recorded state no longer
satisfies the contract. Something must observe that, decide what to do, be
authorized, act and verify. That is E13-05's loop on real operational state.
Nobody tells P13 *when* or *what*.

## 3. State model

```text
S-OPS-01 = {
  object:   "S-OPS-01",
  owner:    "S-OPS operational proof surface",
  kind:     "scheduled operational window",
  state:    CLOSED | OPEN,                     ← the operational state
  window:   {opens_at, closes_at},             ← UTC, fixed at provisioning, opens_at < closes_at
  history:  [ {at, event, from, to, actor, basis}, … ]   ← append-only
}

phase(now) = BEFORE  if now <  opens_at
             WITHIN  if opens_at <= now < closes_at
             AFTER   if now >= closes_at

contract:   BEFORE → CLOSED     WITHIN → OPEN     AFTER → CLOSED
```

The phase is **observed**: it is derived from the object's recorded window and
the UTC clock at the moment of observation. The object does not store it.

An object that does not exist is observed as `UNPROVISIONED`. The contract
requires nothing of it.

## 4. Permitted transitions (exactly two; nothing else is writable)

| Action type | Transition | Preconditions, all re-checked at the gate immediately before execution |
|---|---|---|
| `s_ops.open` | `CLOSED → OPEN` | the target is `S-OPS-01`, its file exists, and its owner is this surface · state is `CLOSED` · phase **now** is `WITHIN` |
| `s_ops.close` | `OPEN → CLOSED` | the target is `S-OPS-01`, its file exists, and its owner is this surface · state is `OPEN` · phase **now** is `BEFORE` or `AFTER` |

The surface enforces the same rules again. It refuses any transition whose
recorded `from` state is not the current state (compare-and-set), any
transition outside the table, and any path outside its root.

There is no API to:

* change the window;
* delete the object;
* create a second object;
* write any other field.

## 5. Expected consequence and verification conditions

| | `s_ops.open` | `s_ops.close` |
|---|---|---|
| **Fixed before the gate** (on P13's proposal) | `CR-SOPS-01-OPEN-WITHIN-WINDOW: PASS` | `CR-SOPS-01-CLOSED-OUTSIDE-WINDOW: PASS` |
| **Execution postcondition** (the executor's own check) | on a fresh read, state = OPEN; the last history entry is this `CLOSED → OPEN` | on a fresh read, state = CLOSED; the last history entry is this `OPEN → CLOSED` |
| **Boundary check** | before and after hashes of the whole S-OPS root, the two Registers, the envelopes and the `FDR-3` act. Only `S-OPS-01.json` may differ | same |
| **Consequence check** (the cycle) | a fresh `StateUnderstanding` observation from disk, then re-evaluation. Expected vs actual; a mismatch is never a success | same |
| **Rediscovery** | the next cycle observes `OPEN` from disk and does not act on S-OPS | the next cycle observes `CLOSED` and does not act on S-OPS |

The two criteria cite `FDR-3`. Their threshold is this surface's contract, which
`tools/s_ops/surface.py` declares (`REQUIRED`). P13 reads the contract and
authors none of it.

## 6. Reversibility

`open` and `close` are each other's inverse within the surface. Reversal is
**not** a separate privilege:

* when the window ends, the contract itself requires `CLOSED`;
* P13 determines the reversal (`s_ops.close`) exactly as it determined the
  opening. It is then authorized, executed, verified and traced the same way.

The reversal restores the operational state and never touches history. The
object's `history` is append-only, and P13's cycle records and Trace are never
rewritten. Evidence of the proof therefore survives the reversal.

No reversal outside these two transitions is authorized: no deletion, no
rewinding of history, no schedule change. Anything else would be a STOP.

## 7. Observation

* **P13** observes S-OPS through a dedicated Source (`s_ops` in
  `tools/p13/state.py`), which reads the object from disk. The facts are:
  * `s_ops.S-OPS-01.state`;
  * `s_ops.S-OPS-01.phase`;
  * `s_ops.S-OPS-01.window`.
* **Independently of P13:**
  * `python -m tools.s_ops.surface show` prints the object and its phase;
  * the file is plain JSON, and `git diff` shows every change.

## 8. Traceability

| Element | Where |
|---|---|
| decision provenance | the cycle record: observed facts → evaluations → conclusion `R-DEFECT` → proposal → `EXECUTE` (verified by `evidence.decision_provenance`) |
| authority provenance | the record and the Trace: `P13-ENV-02`, `FDR-3 §4`, the act path, the scope |
| target and preconditions | the gate's decision reason; the proposal's target |
| expected consequence | on the proposal, fixed before the gate |
| actual consequence and verification | the record's `verification.consequence`; `execution.<type>` (changed paths, boundary, postcondition) |
| execution result | the record's `executed`; the Trace `execution` block |
| re-observation | the record's `observation.after` (fresh from disk) |
| rediscovery | the next cycle's record (`R-CHANGED`, S-OPS criteria PASS, no S-OPS action) |
| the object's own history | `S-OPS-01.json` `history`: `actor` and `basis` (the envelope and the gate's decision) for each transition |

## 9. Who does what

* **The operator** provisions the object once (`provision`), choosing the
  window. Provisioning is **environment**, not action. The operator never
  names an action or a target to P13, and never moves the state.
* **The runner** invokes P13 cycles (`python -m tools.p13.cycle`) with an
  invoker and an intent that name no action.
* **P13** observes, evaluates, reasons, proposes, passes the gate, and executes
  through the surface's API only.
* **Nobody else** writes the object. Tests use temporary directories and
  never touch this root (`tools/p13/paths.py`).

## 10. Isolation and exclusions (`FDR-3` `§2`)

| S-OPS MUST NOT BE | Why this surface is not |
|---|---|
| P13's knowledge or evidence state | its state is a window's OPEN/CLOSED, outside `docs/operations/p13/`. It is not derived from P13's evidence |
| the residual frontier register | not related |
| a test fixture disguised as operational state | a persisted live object, with an owner, a definition and an envelope. It is changed only by the production executor through the real gate. Tests never touch it |
| a canonical P1–P12 artifact | new, under `docs/operations/s-ops/`, outside every phase directory |
| a governance artifact whose mutation could alter authority | no gate, envelope or Register reads its state. Its state changes nothing's authority |
| P11 organizational state | no P11 record, registry or root |
| a production or external system | a file in this repository; no network, no process |
| arbitrary repository write access | two transitions, one object, compare-and-set; the gate's scope and the execution boundary check both enforce it |
| source-code self-modification | P13 changes no code. The object is data |
| P13 self-expansion | P13 cannot provision objects, change the window, or widen `P13-ENV-02` |
| an authority-generation mechanism | nothing reads S-OPS state as authority |

## 11. Limitations

* **Nothing outside the surface consumes the window.** That is by design:
  isolation. The consequence is operational, since the object's state conforms
  to its operational contract, but its meaning is self-contained.
* **The phase depends on the UTC system clock.** A wrong clock gives a wrong
  phase. The clock is trusted as it is everywhere else in AIOS (envelope
  expiry, Trace timestamps).
* **The window is chosen by the operator.** The operator therefore decides
  *when* the contract changes, but never *what* P13 does about it.
* **The authority exhausts itself.** Once the window has ended and the object
  is CLOSED, no precondition of either transition can hold again, and
  `P13-ENV-02` can no longer execute anything. A new proof would need a new
  object, and so a new, wider decision.
* **One object.** Extension beyond `S-OPS-01` is not authorized (`FDR-3` `§3`:
  *"expand the S-OPS boundary"*).

This file carries no authority. `FDR-3` does.

---

**Retired (appended 2026-09-24; everything above unchanged).** The E13-05 proof
on this surface is complete: `docs/governance/AIOS_P13_E13_05_S_OPS_LIVE_PROOF_RECORD_v1.0.md`.
`FDR-4` `FD-B` (Decision Register `§24`) retires `P13-ENV-02` as spent, and the
retirement is recorded in Delegation Register `§16`. S-OPS is now a **historical
proof surface**:

* its operational authority is retired, and no envelope permits either
  transition;
* its evidence is retained: this definition, `S-OPS-01.json` and its history,
  the envelope record, the cycle records and the Trace.

P13 still reads the object each cycle, read-only. That is not an execution
dependency.
