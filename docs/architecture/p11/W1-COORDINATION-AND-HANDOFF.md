# W1 `PLAN → WORKFLOW` — the hypothesis, falsified

> **Verdict `U2` — existing authority already satisfies the role.**
> The *"unit-level delegator"* requirement was **mine**, not the architecture's,
> and the real blocker was something else entirely.
>
> A real `PLAN → HANDOFF → WORKFLOW → COORDINATION → EXECUTION` completed, with
> the Workflow reaching terminal **`SUCCEEDED`**. `P11 OPERATIONAL` remains
> **FALSE** (`§40`).

---

## A. The falsification

`ACT-CC-P11-007` reported `PLAN → WORKFLOW` as `AUTHORIZED + BLOCKED`, requiring
a *"unit-level delegator"*. `§1` of this Act correctly treats that as a
hypothesis. It does not survive:

| `§8` Test | Result |
|---|---|
| A — does Workflow require one? | **No.** `WorkflowStep` takes `step_key`, `performed_by: AgentInstanceRef`, `composes: SkillRef`. An actor and a skill; **no delegating unit** |
| C/D/E — do DP-03, DP-04, FD-P11-001? | **No.** The phrase occurs **zero** times across all four issued instruments |
| F — does an existing P10 mechanism provide the role? | **Yes.** `workflow.governance-corpus-health-check` already reads *"invoked by an Agent Instance of the Governance Artifact Integrity Agent"* |
| H — is it a consequence of my data model? | **Yes** |

The phrase appears in exactly three documents, **all written by me**.

### Where my reasoning went wrong

> *"Naming the actor for a piece of work is allocating work to an actor, which
> is delegation."*

That much is sound. The hidden step was **"and the delegator must be a unit"** —
never stated by any instrument, and falsified by `FD-P11-001 §4.1`, which
established a delegator that is explicitly *not* a unit and whose `§5` rejects
Engineering or Platform becoming one by label.

### What was actually blocking

Two things, neither of them a delegator:

1. **No Agent Instance existed at all** — zero, until `FD-P11-001 §7` authorized
   creating one.
2. **The Definition I chose for W4 has no Skills.**
   `engineering-intelligence-agent` declares *"Permitted Skills: None
   declared"*, and a `WorkflowStep` requires a Skill. An instance of it can never
   produce one.

`governance-artifact-integrity-agent` carries **ten** permitted Skills and
**five** permitted Workflows. `ACT-CC-P11-008 §8` ranked it *second*, correctly,
because that Act asked for the safest observable first proof — **and that
correct choice is precisely what made W1 unreachable from it.**

---

## B. The living proof (`§20`)

```text
delegation:1700394c2fea4a88 → delegator:Claude Code / AIOS Co-Founder
                            → decision:FD-P11-001 §9 → founder:Founder

plan w1-coordination-proof-plan-0
  prepared steps   review-open-items · summarize-diffs
  workflow steps   review-open-items · summarize-diffs
  acting instance  governance-artifact-integrity-instance-001
  composed skills  open-item-tracking-review · governance-artifact-diff-summary
  terminal state   WorkflowState.SUCCEEDED  (ordinal 4)
  superseded       f24d8954e64b40df
  boundary crossed false
```

**The Skills are the two the resident workflow record names.** Nothing was
chosen; they were read.

`§20`: *"No new authority may be created solely to make the test pass."* None
was. `FD-P11-001` already authorized the delegator and instance creation; the
Definition, its Skills and its Workflows are resident P10 records.

### What was exercised, precisely

Real `WorkflowSubsystem`, real `WorkflowComposition`, real lifecycle
`DEFINED → READY → RUNNING → SUCCEEDED` driven by the resident
`WorkflowParticipatingAgent`. The Execution context is the **injected-collaborator
stand-in** the consumer's own tests use, whose docstring says *"The real path is
exercised against a real Runtime in the companion module."* **The Runtime-hosted
path was not exercised** and is reported as remaining frontier, not claimed.

`is_multi_agent: false` — one acting instance is a **handoff**. Calling it
cross-agent coordination would overstate it (`§19`).

---

## C. `TRANSLATION ≠ AUTHORIZATION` (`§18`)

Every field of the produced `WorkflowStep` is copied from something already
authorized:

```text
step_key      ← the Plan, via WorkPreparation
performed_by  ← the recipient of an ACTIVE W4 Delegation
composes      ← a Skill the recipient's Definition already permits
```

Nothing is chosen, defaulted or invented. Eight refusals, each
mutation-tested, cover a different way the handoff could occur without
authority: no delegation · revoked delegation · step outside scope · capability
outside scope · unregistered instance · retired instance · skill not permitted ·
unprepared work.

---

## D. A ninth proxy control found — same pattern as `§94.4`

`ACT-CC-P11-007` established: **no P11 surface may construct
`AgentInstanceRef`, `SkillRef` or `WorkflowStep`.** That control fired against
the adapter.

**It was a proxy.** It asserted *"nobody constructs these types"* as a stand-in
for *"nobody fabricates an actor assignment"* — and the stand-in held only while
no legitimate construction path existed. `ACT-CC-P11-009 §94.4` found eight
controls of exactly this shape; this is the ninth.

**Narrowed, not weakened.** Planning still constructs none of them — that is the
boundary that was always meant, since naming who acts is not Planning's to do.
Two new guards make the narrowing safe: **exactly one** module may name actors,
and it must refuse without authority. Both were mutation-tested; smuggling a
construction into a second surface fails, and reintroducing one into Planning
fails.

---

## E. Continuity (`§22`) — and a gap it exposed

A fresh process reconstructs the W1 state: instance, live grant, revoked grant,
plan, outcomes.

**It did not, at first.** The continuity reader looked only for
`first-execution.evidence.json`, so the W1 run reconstructed its grants correctly
while reporting `last_plan: null`. That is the `§22` collapse arriving by an
unexpected route — **not stale read as current, but present read as absent.** The
reader now finds any evidence record and reports which it used.

---

## F. Verification

```text
tools 605 OK · native_core 801 OK (1 expected failure) · consumers 276 OK
citation 161 documents / 0 errors · stale-state 463 / 0 assertions
Native Core = 11 · W1 live grants = 1 · W3 records = 1 · open escalations = 1
```

Ten mutation probes this Act; **all ten fired.**

---

## G. Remaining frontier (`§41`)

| Item | Class |
|---|---|
| Runtime-hosted Workflow path | **AUTHORIZED + ACTIONABLE** — the companion real-Runtime path exists and is unexercised |
| Cross-agent coordination (`is_multi_agent`) | **AUTHORIZED + ACTIONABLE** — needs a second registered instance |
| No resident consumer for `governance-artifact-integrity-agent` | **AUTHORIZED + ACTIONABLE** — the Definition has Skills but no implementation |
| Escalation `23f315ba` | **HUMAN-RESERVED** |
| Co-Founder Delegation Charter | **UNKNOWN** — non-resident |
| Prioritization / ranking | **RESERVED** |

**`§41`: NOT EXHAUSTED.** `§40`: W1 proven does not make P11 operational — six of
eight exit dimensions have now been exercised, coordination only as a
single-actor handoff.
