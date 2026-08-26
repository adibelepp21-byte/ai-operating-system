# agent_execution_semantics_spec

**Authority:** `P6-AES-01 — Agent Execution Semantics`, authorized scope items **4** (rejection), **5** (termination), **9** (failure and its evidence requirements), **10** (evidence and conformance criteria), per `DEC-P6-029` issuance 3 as accepted by issuance 4.
**Delegation:** Co-Founder / Delegated Architecture Authority, `AIOS CO-FOUNDER DELEGATION CHARTER v1.0` §4.1/§4.4. Frontier identified under `ACT-CC-P6-033` §13.
**Status:** Specification. **No construction authority. No construction target. Class H remains EMPTY.**

## 1. Purpose
[A] Defines what **rejection**, **failure** and **termination** mean for an Agent participating through `ExecutionConsumer.participate(execution)`, and what evidence establishes each. It defines meanings; it implements nothing.

## 2. Non-Goals
[E] Out of scope by governing decision, not by omission: Agent → Capability **reference** (Founder-reserved, `DEC-P6-032`); Capability **invocation** (excluded, `DEC-P6-029` issuance 4); Capability **self-execution** (forbidden, Freeze §4); execution-**result** model (declared absent, `consumer.py:75`); **cancellation** mechanism (excluded unless separately established by canon); Agent Factory, bootstrap, Department/Capability binding (`P7-L-1`); Runtime lifecycle redesign (`P7-O-1`); Knowledge access redefinition (C-01/D-001 — preserved, not redefined).

## 3. The three events are distinct
[A] They are separated by **whether participation was accepted** and **whether an action occurred**:

```
rejection    refused BEFORE participation is accepted   → no action occurred
failure      accepted participation does not complete   → an action occurred
termination  an accepted, in-progress execution stops   → see §6
```
[A] No two may be collapsed. A rejection is not a failed action; a failure is not a refusal.

## 4. Rejection semantics
[A] **Definition:** a rejection is a refusal to accept a participation attempt, raised before the consumer's own work begins. The participation attempt has no effect.

[E] Two rejection conditions are already canonical and realized:
- `RuntimeNotRunning` — *"a hosted resource or execution context is requested while the Runtime is not RUNNING"* (`runtime/exceptions.py`). The RUNNING-only gate is enforced by `_require_running` on `create_context` and `knowledge`.
- `InvalidExecutionConfiguration` — *"an execution boundary cannot be constructed accountably"* (`execution/exceptions.py`); `ExecutionSession.__post_init__` refuses a non-`Runtime` or non-`ExecutionContext` binding.

[E] **Rejection is fail-closed (PR-4).** It is signalled by raising, never by a return value — `participate` returns `None` and no result model is ratified (`consumer.py:75`).

[A] **Rejection produces no Trace.** INV-4 binds *"every Agent-Instance **action**"*. A rejected attempt is not an action: nothing was accepted and nothing was done. This is not an exemption from INV-4 — INV-4 never applies, because its subject does not exist.

[A] **Rejection is not the consumer's decision to make about its own admission.** Both realized conditions are enforced at the Runtime/Execution boundary before the consumer is reached. A consumer that refuses work it *was* given has failed (§5), not rejected.

## 5. Failure semantics
[A] **Definition:** a failure is an accepted participation that does not complete according to its semantics. Acceptance has already occurred; an action exists.

[E] **Signalled by raising, under `ExecutionError`** — already canonical as *"Base for every fail-closed Execution-layer halt (PR-4)"* (`execution/exceptions.py`). No new base is introduced and none is needed.

[E] **INV-4 fires: exactly one Trace record, unconditionally.** A failed action is still an action.

[E] **PR-4 governs the untraceable case.** `agent_spec §11`: *"if an action cannot produce Trace, it is not accountable and must not be treated as done."* Therefore an action whose Trace cannot be written is **not done** — it is neither a success nor a completed failure, and no downstream state may treat it as either.

[A] **Observable state on failure:** the exception propagates to the caller; `Runtime` state is unchanged by the failure itself (Execution is lifecycle-neutral — `contract.py`); Trace, once written, is immutable (INV-5) and captures cited content at write-time (INV-6).

[A] **A failure never silently degrades to a success.** Because no result model exists, there is no value a consumer could return to signal partial success; the only signals are *returned* or *raised*.

## 6. Termination semantics
[A] **Definition:** an Agent execution ends exactly when `participate(execution)` returns or raises. **There is no separate termination event.**

[E] Basis — a positive architectural fact, not an inference from missing machinery:
- `participate(execution) -> None` is synchronous;
- the execution layer declares *"no threads, no futures, no timers"* (`session.py`) and *"no… retries, queues"* (`contract.py`);
- `Execution` is *"lifecycle-neutral: it starts nothing and stops nothing"* (`contract.py`).

[A] With no concurrency primitive, no second party can be executing while `participate` is in flight. `RuntimeState.STOPPING` therefore cannot interleave with an in-progress participation on the same thread, and an external stop-signal has no realizable delivery path. **Termination is not absent for want of a mechanism; it is not a distinct event in a synchronous, single-threaded contract.**

[A] **Scope of this definition.** It holds for the execution contract as ratified. Introducing concurrency would create an interleaving this definition does not cover — and concurrency is itself unauthorized. **If concurrency is ever authorized, this section requires re-specification.** Recorded as a standing dependency, not a hidden assumption.

[A] **Termination is not cancellation.** Cancellation — a request to stop work already accepted — remains excluded unless separately established by canonical authority. Nothing here introduces one.

## 7. Trace obligation mapping
| Event | Action occurred | INV-4 obligation | Signal |
|---|---|---|---|
| Accepted, completed | YES | exactly one Trace | returns `None` |
| Accepted, failed (§5) | YES | exactly one Trace | raises under `ExecutionError` |
| Rejected (§4) | NO | none — INV-4's subject does not exist | raises under `RuntimeSubsystemError` |
| Accepted, Trace unwritable | YES | obligation unmet | **not done** (PR-4; `agent_spec §11`) |

## 8. Halt taxonomy — existing, unchanged
```
RuntimeError
└── RuntimeSubsystemError            fail-closed Runtime halt (PR-4)
    ├── InvalidLifecycleTransition
    ├── RuntimeNotRunning            → §4 rejection
    ├── InvalidRuntimeConfiguration
    └── ExecutionError               fail-closed Execution-layer halt (PR-4)
        └── InvalidExecutionConfiguration  → §4 rejection
```
[A] Failure (§5) belongs under `ExecutionError`. **No type is added by this specification** — placement is specified; construction is not authorized.

## 9. Evidence requirements
[A] Sufficient evidence for these semantics must establish, per event:

**Rejection** — the refusal occurs before consumer work begins; it raises rather than returns; **no Trace is written**; Runtime and Knowledge state are unchanged.
**Failure** — the action is accepted; it raises under `ExecutionError`; **exactly one Trace exists** (INV-4); the Trace is immutable (INV-5) and carries captured content, never references (INV-6).
**Untraceable action** — the action is not reported done, and no downstream state treats it as done (PR-4).
**Termination** — that the contract exposes no path by which an accepted participation is stopped other than returning or raising.

[A] **Negative evidence is required, not optional:** that no forbidden import appears; that `PERMITTED_BOUNDARIES == {"runtime"}` still holds by equality; that no Capability execution primitive exists; that no result object is produced.

## 10. Conformance criteria
[A] A future conformance suite for these semantics must: exercise each event class separately; assert Trace **count**, not merely presence; assert the *absence* of a Trace for rejection; assert exception **type**, not message text; and add no assertion that presumes a Capability reference, a result model, or a cancellation path.

[E] **`test_agent_conformance.py` and its dependency-boundary rules are not modified by this specification** — excluded by the governing phase boundary.

## 11. Preserved boundaries
[E] C-01 · D-001…D-006 · `P7-L-1` · `P7-O-1` · `P7-O-2` · `RU-5` (open) · Freeze §4 · INV-4/5/6 · PR-3 · PR-4 — all unchanged by this document.

## 12. Reserved / still open
[E] Agent ↔ Capability **reference** — Founder-reserved (`DEC-P6-032`), and no part of this specification presumes, implies or requires one. Execution **result** model — declared absent. **Cancellation** — excluded. **Concurrency** — unauthorized; §6 depends on its absence. Readiness reassessment — belongs to a gate, not to this document.
