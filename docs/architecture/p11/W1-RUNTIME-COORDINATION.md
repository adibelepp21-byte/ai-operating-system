# W1 Runtime Coordination — three frontiers, none of them missing

> **`F1-A` · `F2-B` · `F3-C`.** All three investigated frontiers resolve to
> *existing canonical mechanism*. **Nothing was built that the system already
> had.**
>
> The proof level rose from `INJECTED` to **`REAL-RUNTIME`**.
> `P11 OPERATIONAL` remains **FALSE** (`§47`).

---

## A. F1 — Runtime-hosted path: **`F1-A`, EXISTING PATH SUFFICIENT**

The whole path is resident and was found by reading, not built:

```text
build_default_infrastructure(base_dir)        → filesystem · storage
                                                tool-boundary · execution-substrate
AIOSRuntime(runtime_id, storage, substrate)   → initialize() → start() → RUNNING
create_execution_layer(runtime)               → ExecutionSession (.runtime, .context)
WorkflowParticipatingAgent.participate(exec)  → execution.runtime.workflows
```

`WorkflowParticipatingAgent._resolve` had said so all along: *"Otherwise it comes
from the Runtime hosting this Execution — `execution.runtime.workflows` — which
is RUNNING-gated by the Runtime itself."*

**The real run used it with no injection**:

```text
proof_level        REAL-RUNTIME          subsystem_injected  false
subsystem_source   execution.runtime.workflows
runtime_id         p11-w1-runtime        runtime_state       RUNNING
execution_context  ExecutionContext(runtime_id='p11-w1-runtime', execution_sequence=0)
terminal           WorkflowState.SUCCEEDED (ordinal 4)
after stop         RuntimeState.STOPPED
```

`§8` is honoured: `ACT-CC-P11-010`'s injected-collaborator result stands for what
it proved and is **not** retracted — it is superseded at this stage by a stronger
one. `§35`'s hierarchy: `INJECTED` → **`REAL PROCESS`**.

`§10` holds — the Runtime hosts and **refuses**; it grants nothing. Stopped, it
raises `RuntimeNotRunning` for both `workflows` and `create_execution_layer`.

---

## B. F2 — Multi-agent necessity: **`F2-B`, NOT REQUIRED**

Answered from the canonical contract, `native_core/core/workflow/coordination.py`:

> *"Coordination of Agent Instances, bound to exactly one Workflow."*
>
> *"A coordination with an empty composition is structurally valid — it
> coordinates no one."*
>
> `is_multi_agent()`: *"Reported, never acted on (PR-3). A multi-agent
> coordination is legal precisely because it is expressed through this
> Workflow."*

So multi-agent is **permitted, not mandated**, and a coordination of zero or one
participant is *structurally valid*. What actually constrains coordination is
`INV-13` — it must be **through a Workflow**, which `WorkflowCoordination`
enforces by refusing to exist without one.

**This corrects my own frontier entry.** `ACT-CC-P11-010` listed *"cross-agent
coordination (needs a second instance)"* as `AUTHORIZED + ACTIONABLE`. It is
**optional**, and `is_multi_agent: false` is a property of a valid coordination,
not a deficiency (`§14`).

---

## C. F3 — Resident consumer: **`F3-C`, EXISTING MECHANISM SATISFIES THE ROLE**

`consumers/workflow_agent.py` drove the whole lifecycle. What I recorded in
`ACT-CC-P11-010` as *"no resident consumer for
`governance-artifact-integrity-agent`"* is an absence of a **capability
implementation**, not of the coordination mechanism.

`§1`: *"Absence of implementation is not proof of absence of a canonical
mechanism."* The run proves it directly — **no consumer implements that
capability, and the Workflow still reached terminal `SUCCEEDED`** with both steps
completed. The performer is injected, so coordination never needed one.

---

## D. Canonical-home verdicts (`§21`)

| Frontier | Verdict | Built? |
|---|---|---|
| Runtime-hosted path | **H1** — existing home; use | no |
| Multi-agent coordination | **H1** — exists, optional | no |
| Resident participant | **H1** — existing home; use | no |
| Proof-level labelling | **H2** — bounded extension | coherence control added |

**Nothing in `§41`'s prohibited list was created.** No Unit Delegator, no new
authority, no entity, no Native Core #12, no P12.

---

## E. Verification, and two controls that could not detect their own prohibition

`§39` mutation-probed every material control. Four fired immediately. **Two
returned `OK`, and both were real findings:**

**The proof label was checked for membership, not for truth.** A run could claim
`REAL-MULTI-AGENT` while recording one participant and pass, because the control
only asked whether the label was a recognised category. `§36` forbids silent
promotion — *and a label nobody cross-checks is exactly how promotion stays
silent.* Each label is now tied to the evidence that would have to be true, and
verified by running a deliberately mislabelled proof: it fails on two
assertions.

**The idempotency control inspected a clean result.** Disabling the stale-grant
sweep changed nothing it could see, because it read files the last real run had
already tidied. *A control that inspects a clean result cannot tell whether the
thing that cleaned it still works.* It now drives the mechanism against a
temporary root.

```text
tools 623 OK · native_core 801 OK (1 expected failure) · consumers 276 OK
citation 162 documents / 0 errors · stale-state 463 / 0 assertions
Native Core = 11 · W1 live grants = 1 · protected = 13 untouched
```

---

## F. Defects

| Defect | Detection | Action |
|---|---|---|
| Evidence `act` field hardcoded | the run labelled itself with the previous Act | parameterized; `module_constructed_under` kept separately |
| Label control checked membership, not truth | mutation probe returned `OK` | coherence control; verified by a mislabelled run |
| Idempotency control read a tidied result | mutation probe returned `OK` | mechanism exercised against a temp root |
| **`tools/` imported `consumers/` — again** | the region invariant | assertion rewritten to use the run's own evidence |

**The import violation is the second of its kind.** `ACT-CC-P11-008` did it from
`w4_first_run.py`; this time from a *test*, which is the same edge in the
dependency graph. The fix was not a weaker assertion: the claim — coordination
needs no capability implementation — is proven **more** directly by the run than
by the signature I was reaching for.

---

## G. `§50` final state matrix

```text
F1 Runtime-hosted Path : F1-A — EXISTING PATH SUFFICIENT
F2 Multi-agent         : F2-B — NOT REQUIRED (optional, INV-13 constrains via Workflow)
F3 Resident Consumer   : F3-C — EXISTING PARTICIPANT SATISFIES ROLE
W1 Authority           : RESOLVED (U2, carried forward)
W1 Handoff             : PROVEN — REAL-RUNTIME
W1 Coordination        : PROVEN for single-participant, through the Workflow channel
W3 ↔ W4               : CONNECTED         W4 ↔ Runtime : PROVEN (this Act)
W1 ↔ W4               : CONNECTED         W4 ↔ W5      : PROVEN
W1 ↔ W5               : PROVEN — fresh process reconstructs the W1 run
P11 Operational        : FALSE            P11 Exhausted : FALSE
P11 Complete           : FALSE            P11 Certified : FALSE
E11 : NOT RATIFIED     P12 : NOT AUTHORIZED
Native Core : 11       Protected Packages : 13 UNTOUCHED
```

`§46`: a real single-participant Runtime-hosted coordination is exactly that. It
is **not** multi-agent coordination, and the canonical contract says it does not
need to be.

---

## H. Remaining frontier (`§45`, `§48`)

| Item | Class |
|---|---|
| Multi-agent coordination proof | **AUTHORIZED + ACTIONABLE, OPTIONAL** — permitted, not required |
| Consumer implementing `governance-artifact-integrity` | **AUTHORIZED + ACTIONABLE** — capability work, not coordination |
| Escalation `23f315ba` | **HUMAN-RESERVED** |
| Co-Founder Delegation Charter | **UNKNOWN** — non-resident |
| Prioritization / ranking | **RESERVED** |
| P12 unified state | **OUT OF SCOPE** |

**`§48`: NOT EXHAUSTED.**
