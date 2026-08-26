# agent_execution_semantics_spec

**Authority:** `P6-AES-01 — Agent Execution Semantics`, authorized scope items **1** (execution semantics), **2** (participation semantics), **4** (rejection), **5** (termination), **8** (lifecycle/state), **9** (failure and its evidence requirements), **10** (evidence and conformance criteria), per `DEC-P6-029` issuance 3 as accepted by issuance 4.
**Delegation:** Co-Founder / Delegated Architecture Authority, `AIOS CO-FOUNDER DELEGATION CHARTER v1.0` §4.1/§4.4. §§1–12 written under `ACT-CC-P6-034`; §§13–17 under `ACT-CC-P6-035`.
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

---

## 13. Participation semantics

[A] **Claim classification for §§13–17**, per `ACT-CC-P6-035` §8: **[E]** = canonical fact with a cited source · **[A]** = delegated architectural synthesis, reasoned from evidence and not itself canon · **[O]** = open / unresolved. No `[A]` entry may be cited later as canonical fact.

### 13.1 What participation is
[E] Participation is an Agent taking part in one bound `Execution` through the inherited `participate(execution)` — its *"sole required responsibility and sole entry point"*, making the `Execution` boundary *"its only route to the hosting Runtime"* (`agent.py`).

[A] Participation is therefore **entry, not authority**. Being handed a bound `Execution` grants an Agent nothing it did not already have: `Execution` *"adds no authority and bypasses nothing"* (`contract.py`), and reaching anything the Runtime hosts still passes the Runtime's own controls.

### 13.2 Preconditions for acceptance
[E] Four conditions must hold before a participation can be accepted:

1. **Runtime is RUNNING.** `_require_running` gates `create_context` and `knowledge`; `RuntimeNotRunning` otherwise.
2. **A Runtime-issued `ExecutionContext` exists.** `create_context` mints it with `runtime_id` and a monotonically incremented `execution_sequence` (`runtime.py`).
3. **A well-formed binding exists.** `ExecutionSession.__post_init__` refuses a non-`Runtime` or non-`ExecutionContext` with `InvalidExecutionConfiguration`.
4. **The consumer implements `ExecutionConsumer`.** `participate` is abstract; a non-implementor cannot be constructed.

[A] **Precondition 1 is enforced upstream of the execution itself.** Because `create_context` is RUNNING-gated, an `ExecutionContext` cannot be minted at all while the Runtime is not RUNNING — so condition 2 cannot be satisfied without condition 1. The RUNNING requirement is structural, not a check performed at participation time.

### 13.3 Participation outcomes
[E] The outcomes are exactly those already specified, and there are no others: **rejected** (§4) · **completed** · **failed** (§5). Termination is not a fourth outcome (§6).

[A] **Completion is defined negatively and deliberately so:** a participation completes when `participate` returns and does not raise. There is no success value, because no result model is ratified (`consumer.py:75`). Completion is the *absence* of rejection and failure, not a positive assertion carried in a return.

## 14. Execution phase model

### 14.1 There is no execution state
[E] Re-verified by AST across `native_core/core/`: the only `state` members anywhere are `Runtime.state`, `AIOSRuntime.state` and `Facility.state`. **No `Execution`, `ExecutionSession`, `ExecutionContext`, `Agent`, `AgentDefinition` or `AgentInstance` carries state.**

[E] `Execution` is *"lifecycle-neutral: it starts nothing and stops nothing"* (`contract.py`). `ExecutionContext` *"carries only the hosting Runtime's identity and the Runtime-issued execution ordinal"*.

[A] **Therefore an execution has phases, not states.** A *state* is a persisted, queryable attribute; a *phase* is a position in the call's progression, observable only at the boundary. Canonical evidence justifies phases. It justifies no state attribute, and none is specified here.

### 14.2 The three phases
[A] Justified by the call boundary alone:

```
NOT ACCEPTED     before participate() is entered      — rejection may occur here
ACCEPTED         participate() has been entered
CONCLUDED        participate() has returned or raised — terminal
```

[E] This is consistent with `agent_spec §4`, which gives the Instance lifecycle as *"Definition → Runtime creates Instance (INV-3) → governed action(s) each producing Trace (INV-4) → **conclusion**"*. "Conclusion" is the terminal, and it is the only lifecycle terminal canon names.

## 15. Transitions

### 15.1 Valid
| # | Transition | Cause | Action occurred | Trace |
|---|---|---|---|---|
| T1 | NOT ACCEPTED → ACCEPTED | all four §13.2 preconditions hold | — | — |
| T2 | NOT ACCEPTED → CONCLUDED *(rejected)* | a precondition fails; raises under `RuntimeSubsystemError` | **NO** | **none** — INV-4's subject does not exist |
| T3 | ACCEPTED → CONCLUDED *(completed)* | `participate` returns `None` | YES | exactly one (INV-4) |
| T4 | ACCEPTED → CONCLUDED *(failed)* | `participate` raises under `ExecutionError` | YES | exactly one (INV-4) |

### 15.2 Not permitted, with the evidence that forbids each
| Transition | Why not |
|---|---|
| ACCEPTED → NOT ACCEPTED | Acceptance is not revocable. Rejection is *defined* as pre-acceptance (§4); a consumer refusing work it was given has failed, not rejected |
| CONCLUDED → ACCEPTED | **No resumption.** `execution_sequence` is issued once per context and monotonically incremented by the Runtime; a further participation necessarily carries a different ordinal and is therefore a *different execution*, not a continuation |
| CONCLUDED *(completed)* → CONCLUDED *(failed)*, or the reverse | Terminal is terminal. Trace is immutable once written (INV-5), so a recorded outcome cannot be restated |
| Any transition driven by a second party mid-flight | No concurrency primitive exists (§6). There is no path by which another party executes while `participate` is in flight |

### 15.3 Terminal
[A] **All three CONCLUDED forms are terminal** — rejected, completed, failed. An execution is entered at most once and concluded exactly once.

## 16. Outcome verification

[A] **An execution's outcome cannot be verified by querying the execution**, because the execution holds no state (§14.1). It is verified by two things only:

1. **The boundary signal** — returned, or raised and of which type.
2. **The Trace** — for accepted actions, exactly one record (INV-4), immutable (INV-5), carrying captured content rather than references (INV-6).

[A] **Consequence: the Trace is the only durable record of an execution's outcome.** The execution is transient and stateless; the Runtime's state is its own and is unchanged by a participation; the boundary signal exists only for the duration of the call. Nothing else survives.

[E] **A missing Trace for an accepted action is never a completion.** `agent_spec §11`: *"if an action cannot produce Trace, it is not accountable and must not be treated as done."* Per §7, that action is **not done** — neither success nor completed failure.

[O] **How an unwritable Trace is surfaced is not specified here.** Canon establishes the obligation and its fail-closed consequence; it does not establish a reporting mechanism, and none is invented.

## 17. Boundary allocation

| Owner | Owns |
|---|---|
| **Runtime** | hosting; its own lifecycle `CREATED → INITIALIZED → RUNNING → STOPPING → STOPPED` via guarded transition; RUNNING-only access control; issuance of execution ordinals |
| **Execution** | the transient binding of a Runtime to an execution identity. Lifecycle-neutral. No state, no verbs |
| **Agent Definition** | specification identity — key, version, owning Department, declared Capabilities/Skills/Workflows. **No execution semantics** |
| **Agent Instance** | runtime identity; *"the only actor"*; ephemeral; exactly one Definition on exactly one Runtime (INV-3) |
| **Trace** | the durable, immutable record of what occurred (INV-4/5/6) |
| **Agent (contract)** | the behavioural abstraction only — entry via `participate`, nothing else |

[A] **The Definition / Execution separation is preserved absolutely.** Nothing in §§13–17 reads an execution semantic out of a Definition field, and nothing assigns an execution concern to the Definition layer.

### 17.1 Deliberately undefined
[E] **Founder-reserved:** Agent → Capability reference (`DEC-P6-032`) — no part of §§13–17 presumes, implies or requires one.
[E] **Declared absent:** execution-result model.
[E] **Excluded:** Capability invocation · Capability self-execution · cancellation · concurrency.
[E] **Belonging elsewhere and not specified here:** scheduling · dispatch · retry · queueing · planner · workflow · tool execution · Agent Factory, bootstrap, Department/Capability binding (`P7-L-1`) · Runtime lifecycle redesign (`P7-O-1`).

### 17.2 No implementation by implication
[A] Per `ACT-CC-P6-035` §11, and stated so it cannot be read otherwise:

- Specifying **phases** does **not** authorize a state machine, a state field, or a state enum.
- Specifying that an outcome is **verified via Trace** does **not** authorize changing Trace, its storage, or its writer.
- Specifying that failure belongs under **`ExecutionError`** does **not** authorize adding a type.
- Specifying **preconditions** does **not** authorize adding a precondition check.

[A] **Everything in §§13–17 describes meaning. No mechanism is authorized, and none is created.**
