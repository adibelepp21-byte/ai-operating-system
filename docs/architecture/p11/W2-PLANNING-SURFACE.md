# W2 — The Organizational Planning Surface

> **Constructed under `ACT-CC-P11-005`** — 2026-09-10.
> Authorized by [`DP-01`](../../governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md) `§3 W2`;
> shaped by [`DP-03`](DP-03-P11-ORGANIZATIONAL-ARCHITECTURAL-SURFACE.md) `§8.4`
> and [`DP-04`](DP-04-P11-ORGANIZATIONAL-ENTITY-MODEL.md) `§8.1`/`§8.2`.
>
> **Implementation:** `tools/planning/` · **Tests:** 83 across three suites.
> `P11 CONSTRUCTED = PARTIAL` — W2 is one of seven packages.

---

## 1. The sentence that determined the design

`DP-03 §8.4` chooses an `ORGANIZATIONAL-LAYER PLANNING SURFACE` and then says:

> *"It may use persisted organizational records where appropriate, but the
> architecture MUST support the mutable Plan lifecycle"*

followed by `PLAN → SEQUENCE → ADAPT → REVISE`, and:

> *"A Plan is therefore not constrained to the semantics of a static declaration
> loaded once."*

**That rules out the pattern W3 used.** `tools/delegation_catalog.py` is a loader
over persisted markdown: read once, verified, never evolving. Reusing it here
would have satisfied the word *record* and failed the word *lifecycle* — and
`ACT-CC-P11-005 §20` Test A exists to catch exactly that substitution.

`DP-01 §3 W3` had permitted reusing the P10 pattern *"where technically
appropriate"*. **For W2 it is not appropriate**, and the instrument that says so
is `DP-03 §8.4`, which the Architect issued after accepting my objection that a
static surface could not carry `ADAPT` and `REVISE`.

---

## 2. Immutable versions, a mutable chain

A `Plan` is **frozen**. Adaptation and revision **construct a successor**;
neither edits a predecessor. Supersession is **derived** from the chain's shape,
never stamped onto the record it retires.

```text
Goal ── decomposed by ──▶  Plan v0  ──adapt──▶  Plan v1  ──revise──▶  Plan v2
                           (PLANNED)            (ADAPTED)            (REVISED)
                              │                    │                    │
                           superseded          superseded            current
                              └─ still readable, still intact ─┘
```

This is how `ACT-CC-P11-005 §16` is satisfied. It forbids erasing *"the
distinction between prior and current state"*, forbids presenting *"a revised
plan as the original plan"*, and forbids mutating history *"merely to make the
current plan appear continuous."* **None of the three is possible, because no
operation writes to an existing version.** The guarantee is the absence of a
capability, not a rule someone has to remember.

Attempting `plan.steps = (...)` raises `FrozenInstanceError`. That is asserted as
a test, because the defining property of a static record is that it *can* be
overwritten.

---

## 3. Sequencing versus prioritization — the reserved boundary

`DP-01 §3 W2`: *"The reserved prioritization/ranking/decision-heuristic frontier
remains reserved."* `ACT-CC-P11-005 §13` requires the implementation to
distinguish `SEQUENCING` from `AUTONOMOUS PRIORITIZATION / DECISION AUTHORITY`.

The line drawn is exact:

| | Derived from | Verdict |
|---|---|---|
| **Sequencing** | declared dependencies; ties broken by **declaration order** | authorized |
| **Prioritization** | computed desirability — score, weight, urgency, dependents | **reserved** |

`sequence()` is a stable topological sort. Among steps whose dependencies are
satisfied, the one the author **declared first** goes first.

**The tie-break is the whole boundary.** Declaration order reads a fact the
author stated. Any computed tie-break — cost, urgency, how many steps something
unblocks — would be this module forming a judgement about what matters more.
*The difference is not the sophistication of the rule; it is whether the order
comes from the author or from here.*

`PlanStep` therefore carries **no** score, weight, rank, priority, urgency or
importance field. Such a field would not merely enable prioritization later —
**its presence is the judgement**, because something must set it, and whatever
sets it is deciding what matters. A cycle raises rather than resolving: a cycle
declares no order, and inventing one enters the frontier through the back door.

---

## 4. What the surface cannot do

There is **no method anywhere in `tools/planning/` that returns whether something
is authorized.** A Plan carries a *citation* to the authority under which it was
formed and can be asked what that citation is. Nothing converts a plan's
existence, readiness, revision count, or history of success into permission.

`ACT-CC-P11-005 §14`:

```text
PLAN EXISTENCE ≠ AUTHORIZATION      PLAN READINESS  ≠ AUTHORIZATION
PLAN PRIORITY  ≠ AUTHORIZATION      PLAN COMPLETION ≠ AUTHORITY
```

**There is no `READY` state to misread**, because `READY` belongs to Workflow.

`AuthorityProvenance` requires its record to resolve on disk — a plan whose
authority points at nothing has authorized itself, and `DP-04 §8.2` states *"A
Plan cannot authorize itself."* Resolution proves the pointer is real; it does
**not** prove the cited instrument grants what the citing artifact claims. That
reading is a human act, and the corpus citation auditor makes the same
disclaimer in the same words.

---

## 5. The three boundaries Planning touches

Each neighbour receives an **inert** frozen description. Planning describes;
others act.

### Workflow — `PLANNING ≠ WORKFLOW`

`prepare_for_workflow()` returns `WorkPreparation` in dependency order, carrying
the authority citation forward so `PLANNING → WORKFLOW` *"preserves authority
provenance"* (`§10`). It has no method that starts, runs, transitions or
completes anything.

`PlanOrigin` is `PLANNED · ADAPTED · REVISED`. `WorkflowState` is
`DEFINED · READY · RUNNING · SUCCEEDED · FAILED`. **The two name sets are
disjoint, and a test asserts it.** A Plan is never RUNNING and never SUCCEEDED:
those describe work being done, and Planning does not do work.

### Delegation — `PLANNING ≠ DELEGATION`

`delegation_requirements()` identifies steps flagged as needing delegation.
**`DelegationRequirement` has no delegator field, and that absence is the
control.** A field would have to be filled, Planning has nobody legitimate to
fill it with, and a guessed delegator is the impersonation `§11` forbids.

Calling `as_delegation_record()` raises `NotImplementedError`. A prove-me-wrong
test writes the most generous record Planning could produce and feeds it to the
real W3 catalog, **which rejects it.** The resident W3 population remains **0**
after Planning runs — `§11`: the empty population *"remains valid if no
legitimate delegator exists."*

### Observation / Performance — `EVIDENCE ≠ AUTHORIZATION`

`PlanningEvidence` records what was observed and why a change was made. It plays
**no part** in the authority decision: `adapt()` checks the citation separately
and ignores evidence entirely when doing so.

Tested at the extreme — twenty observations authorize exactly as much as zero,
and evidence claiming a source of *"founder"* or *"governance"* carries no more
weight than any other. `DP-03 §8.3` confirms Performance as `DETECT-ONLY`.

---

## 6. Escalation, not expansion

`ACT-CC-P11-005 §15`: `ADAPT ≠ SELF-AUTHORIZATION`. The required behaviour is
`DETECT → CLASSIFY → ESCALATE`, never `DETECT → SELF-AUTHORIZE`.

`classify_adaptation()` performs `DETECT → CLASSIFY` **without changing
anything** — a caller can learn what a change would need before attempting it.
`adapt()` and `revise()` raise `EscalationRequired`, naming what is required and
what is held, so the escalation gives a human something to decide with.

**Neither operation has a parameter that sets authority** — not because widening
is checked and refused, but because the operation cannot express it. There is no
`force`, `override`, `approved`, `confirm` or `bypass` parameter, and tests
assert each absence. Repeating an escalated request escalates again, every time:
`SILENCE ≠ APPROVAL`.

A change that escalates leaves the chain **untouched** — fail closed (`PR-4`),
not half-advanced.

---

## 7. Residency, and a question left open

`DP-03 §8.4` places Planning *"outside the frozen Native Core"*; `DP-01 §4`
confirms `NO NEW NATIVE CORE SUBSYSTEM OR ENTITY #12 IS AUTHORIZED`. The
organizational layer's existing code home is `tools/`, where
`organization_catalog` and `delegation_catalog` already live, so `tools/planning`
joins them.

> **Reported, not resolved.** `consumers/` exists as a top-level region only
> because `DEC-P6-042` authorized it. A dedicated organizational-layer region
> would need its own authorizing decision, which `ACT-CC-P11-005 §28` does not
> grant. `tools/` is correct today; whether the organizational layer eventually
> deserves its own region is **a decision, and not mine to take.**

**No persisted plan-record directory was created.** The Plan lifecycle is a
runtime chain, not a file store, and `DP-03 §8.4` says records may be used *where
appropriate* — not that they must be. Creating `docs/architecture/organization/
planning/` to hold records that will never exist would have been cosmetic
construction of exactly the kind the empty W3 population was built to avoid.
