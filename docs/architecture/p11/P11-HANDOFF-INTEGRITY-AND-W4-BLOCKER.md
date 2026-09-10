# P11 Handoff Integrity, and the W4 Blocker — `ACT-CC-P11-007`

> **Verdict: `T2` — CURRENT FRONTIER COMPLETE; NEXT FRONTIER IN PROGRESS.**
> Five frontiers executed. **W4 is `AUTHORIZED + BLOCKED`** on a genuine
> authority boundary, documented below for Founder decision.

---

## A. Authority (`§1`, read from actual bodies)

```text
DP-04 = ISSUED (:77)   DP-03 = ISSUED (:77)   DP-01 = ISSUED (:66)
P11 AUTHORIZED = TRUE   E11 RATIFIED = FALSE   P12 AUTHORIZED = FALSE
Native Core = 11 frozen boundaries
```

## B. Package state (`§2`, verified independently)

| | State | How verified |
|---|---|---|
| W1 | architecturally satisfied; **gated, not unbuilt** | `DP-03 §8.1` = `CONFIRMED — WORKFLOW`; gate analysed below |
| W2 | CONSTRUCTED / VERIFIED | lifecycle suite, 20 tests |
| W3 | CONSTRUCTED; population **0** | loader output; 0 is correct |
| W4 | **NOT STARTED — BLOCKED** | `DELEGATE` step not traversable |
| W5 | **CONSTRUCTED (continuity)** | built this Act; 14 tests |
| W6 | connected | `W6 → W2` adapter |
| W7 | extended twice | now constrains every P11 surface |

A previous run recorded W5 as *not started* partly on a grep for `continuity`,
which hit `w4_continuity` in `tools/organization_catalog.py`. **That is P10's W4
chain check** — an identifier collision with P11-W4, not W5 work. Verified by
reading the function, not the name.

---

## C. `PLAN → WORKFLOW` — the finding that reversed my own classification

`ACT-CC-P11-006` recorded this as `AUTHORIZED + ACTIONABLE`, ranked fifth: an
implementation gap awaiting code. **It is not. It is `AUTHORIZED + BLOCKED`, and
blocked correctly.**

`WorkflowStep` requires `performed_by: AgentInstanceRef` and `composes:
SkillRef`. A `PlanStep` carries neither and cannot: naming who performs a piece
of work is **allocating work to an actor**, which is delegation. `DP-04 §8.2`
fixes the chain as

```text
GOAL → PLAN → DELEGATION → EXECUTION
```

so Plan does not reach Execution directly — **it reaches it through Delegation**,
and Workflow coordinates what has been delegated. W3's population is `0` because
no authorized delegator exists.

`§11`'s seven questions are answered in
`tools/tests/test_plan_to_workflow_gate.py`. The consequential answer is **#5**:
Workflow rejects an *empty* actor key but **accepts an invented one** — the refs
validate shape, not existence.

> **The gate is architectural, not type-enforced.** Nothing in the type system
> stops a future increment from "completing" this integration by inventing
> instance keys and calling it consumption.

So the gate was given an enforcer: **no P11 surface may construct
`AgentInstanceRef`, `SkillRef`, `WorkflowStep`, `WorkflowComposition` or
`WorkflowDeclaration`.** Probed by making Planning fabricate one — the control
names all three types.

---

## D. The W4 blocker, for Founder decision (`§33`)

**W4 cannot begin.** Its loop is
`PLAN → DELEGATE → EXECUTE → OBSERVE → VERIFY → ADAPT → CONTINUE / ESCALATE`,
and the second step is not traversable:

```text
Departments established : engineering, platform      Capabilities owned : 3
Agent Definitions       : 3                          Agent Instances    : 0
Delegations             : 0        →  DELEGATE traversable: False
```

**What is missing is not code.** The delegation mechanism exists and is tested.
What does not exist is a *delegation* — and authoring one is an exercise of the
authority being delegated. `ACT-CC-P11-005` established this and
`ACT-CC-P11-007 §12` restates it: *"Claude MUST NOT create artificial delegation
merely to demonstrate integration."*

### What a Founder decision would need to settle

1. **Who delegates.** An established Department owning the capability —
   Engineering owns `engineering-intelligence` and `cognitive-intelligence`;
   Platform owns `governance-artifact-integrity`.
2. **To whom.** No **Agent Instance** exists anywhere in the repository. W4
   requires a performer, and the instance population is a prior question.
3. **Under which instrument**, since a delegation must cite an authorizing
   instrument that resolves.
4. **Accountability**, which must not be the delegate.

**This is reported, not requested as a Micro Act.** `§22` bars escalating
ordinary engineering; this is not ordinary engineering — it is the creation of
organizational authority, which `§33` names a hard stop.

---

## E. Frontiers executed after selection (`§21`)

### 1. Provenance generalized across the P11 surface **class** (`§8`)

`ACT-CC-P11-006`'s control scanned `tools/planning/` only. `§8` forbids a control
that *"passes only because the known example is hard-coded"* — and a probe proved
it: adding `authority_cited: str` to `tools/performance_evidence.py`, a genuine
handoff surface, produced **no failure at all**.

The control now covers a declared surface set, with a **completeness guard**:
any module under `tools/` importing the planning package must be declared. That
guard then caught `escalation_register.py` **on the run that created it**,
without my remembering — which is the argument for guards over lessons.

### 2. Forgery, by name (`§6`)

`Founder Reserved Authority`, `Architect Authority`, `Governance Authority`,
`System Authority` — each refused at both handoffs, and refused again when used
to cite a non-existent instrument. **All four were accepted before
`ACT-CC-P11-006`.**

Stated alongside: a citation to a *real* instrument is accepted even if that
instrument grants nothing of the sort. Resolution proves the pointer, not the
grant.

### 3. `PLAN → WORKFLOW` gate + fabrication control — section C.

### 4. Escalation persistence (`§13`, `§14`)

Classified before building. *Authorized* — `DP-01 §3 W1` lists escalation.
*Materially required* — W4's loop terminates in `ESCALATE`, and today
`EscalationRequired` is raised and lost.

**Not Trace, though Trace ratifies `escalation` as an outcome.** `TraceRecord`
requires `agent_definition_version`, `agent_instance` and `runtime` — it records
what an agent *did*. A planning escalation has no instance and no runtime, so
writing one there means fabricating both.

`ESCALATION ≠ APPROVAL`, structurally: records are `OPEN`; **nothing in the
module can close one**; a response requires a `HumanAuthority`, which automation
cannot synthesise; the response is a **new file beside** the escalation, never
over it; and status is `OPEN` or `ANSWERED` — **never `APPROVED`**. Durability is
proven by reading records back **in a separate interpreter**.

### 5. W5 planning continuity — selected because nothing blocks it

`DP-01 §3 W5` authorizes *"planning continuity"* under `MEMORY ≠ AUTHORITY`.

**Authority is re-validated on restore, not restored.** A plan whose cited
instrument no longer resolves **does not come back** — it fails closed rather
than returning as a well-formed artifact asserting a vanished source.

> That is the difference between continuity and resurrection. Continuity carries
> what was decided; it does not carry permission across time.

Supersession is **recomputed** from the chain, never read from the file. Editing
the file to claim `Founder Reserved Authority` is refused. A restored plan
escalates exactly as it did before.

---

## F. Prove-me-wrong (`§19`) — selecting W4

| Test | Result |
|---|---|
| A Dependency | **FAILED** — `DELEGATE` not traversable |
| B Authority | delegation population needs organizational authority |
| C Architecture | consistent with `DP-04 §8.2` |
| D Already satisfied | no |
| E Reserved | **the blocker is** — authoring a delegation is exercising it |
| F Integration | W4 on an untraversable step yields an isolated capability |
| G Governance | would create an authority path by fabricating a delegator |
| H P12 | no |
| I Native Core | no |
| J Evidence | completion could not be verified |

**W4 selection falsified on A, E, F, G.** Re-ranked to W5 continuity, which
survived all ten.

---

## G. Defects (`§28`)

| Defect | Impact | Root cause | Action | Status |
|---|---|---|---|---|
| Provenance control scoped to one directory | a forgeable field on another P11 surface passed silently | generalized over the *directory* the example lived in, not the *class* | surface set + completeness guard | **FIXED** |
| `PLAN → WORKFLOW` misclassified as actionable | would have led to fabricating actor assignments | inferred a code gap without reading what Workflow requires | reclassified; gate control built | **FIXED** |
| Workflow accepts invented actor keys | architectural gate had no enforcement | refs validate shape, not existence | fabrication control | **MITIGATED** |
| **Fourth defective mutation probe** | suite crashed; no verdict printed | anchor was a **substring of a longer identifier**, so `replace` hit the wrong block | harness now asserts uniqueness + parseability | **FIXED, disclosed** |
| W5 assessed partly from a name collision | nearly recorded a P10 function as P11 work | `w4_continuity` matched a `continuity` grep | read the function | **CORRECTED** |

### The probe defect, disclosed

The fourth in four Acts, and a **new mechanism**. The previous three were: a
no-op expression, a dataclass-ordering error, and an unmatched anchor. This one
matched — **but `authority = AuthorityProvenance(` is a substring of
`goal_authority = AuthorityProvenance(`**, so `str.replace(…, 1)` mutated the
wrong block and produced unparseable code. The suite crashed and printed no
verdict, which a `grep "^FAILED"` reads as silence.

The harness now refuses to run unless the anchor matches **exactly once**, the
mutation **changes something**, and the result **still parses** — and it restores
the file in a `finally`. Each of those three checks corresponds to one probe that
previously failed silently.

---

## H. Verification

```text
tools 488 OK · native_core 801 OK (1 expected failure) · consumers 276 OK
citation 148 documents / 0 errors · stale-state 463 / 0 assertions
Native Core = 11 · departments = 2 · delegations = 0
regression: W2 lifecycle 20 OK · W3 boundary 22 OK · W7 governance 26 OK
```

`0 citation errors` means every pointer resolves — **not** that cited sources
support the claims made about them. `0 stale assertions` means no **registered**
superseded claim is restated — **not** that the corpus is clean.

---

## I. What this Act does not establish

`W4 READINESS ≠ W4 CONSTRUCTION`, and W4 is not even ready — it is blocked.
`P11 CONSTRUCTED = PARTIAL`. `E11 RATIFIED = FALSE`. `P12 AUTHORIZED = FALSE`.
Native Core = **11**.
