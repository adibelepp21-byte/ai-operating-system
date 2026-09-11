# `E11-04` — cross-Department coordination, remediated and re-measured

> Executed under **`DP-02 §11` item 10** and the **E11-04 Evidence-Anchored
> Skill Reconciliation Directive**. No new authority, no new Act, no new entity,
> no Native Core change, no P12, no protected-package access.
>
> **`E11` now measures `PASS`, 10 of 10.** `DP-02 §10` still holds:
> **`E11 PASS ≠ P11 COMPLETION ≠ P11 CERTIFICATION`**.

---

## 1. Evidence proving pre-existing capability (`§3`)

Read from the actual evidence and from git, not from filenames.

| `§3` question | Answer | Source |
|---|---|---|
| what work was performed | verified `tools/w4_delegation.py` against 13 stated conformance criteria; `criteria_satisfied: 13`, `criteria_unsatisfied: []` | `first-execution.evidence.json` |
| when | `2026-09-11T02:33:13.801174+00:00` | same |
| which Agent Instance | `engineering-intelligence-instance-001`, `instance_lifecycle: REGISTERED` | same |
| which Department owned it | `engineering` — instance → `engineering-intelligence-agent` → the Department record that lists it | `registered_instances()`, `read_departments()` |
| what capability was exercised | Engineering Intelligence, **Testing** sub-ability | `capability_scope`, and the Definition's *"Verify engineered artifacts against their stated conformance criteria, within the Testing sub-ability"* |
| genuinely Testing | yes — sub-ability 3 of 7 in the Capability's Scope, and one of the two the record names as realized | Capability record |
| predates the Skill | **yes, by every measure** — see below | git |
| independently sufficient | **yes** | below |

### The timeline, from `git log`

```text
2026-07-30  ADR-0008 establishes the Capability, Testing among its seven sub-abilities
2026-08-28  Capability record: Coding and Testing are the realized Phase 5 subset
2026-09-02  consumers/engineering_intelligence_agent.py — REALIZED_SUB_ABILITIES
            = ("Coding", "Testing"), with verify() implemented
2026-09-11  the ability exercised and evidenced: 13/13 against tools/w4_delegation.py
    ↓
   now      skill.artifact-conformance-verification written
```

**Six weeks from the ADR, nine days from the implementation.** None of those four
artifacts was written for `E11`, and `E11-04` did not exist when three of them
were created.

---

## 2. Capability-ownership determination (`§4`)

```text
PD-06 AI Engineering          "PD-06 owns implementation" — E-08, FROZEN, CANONICAL
      ↓
Engineering Department        established by ADR-0008; scope: "the abilities by
                              which AIOS builds, changes, verifies, and plans
                              work on itself"
      ↓
engineering-intelligence-agent   owned by that Department, per its record
      ↓
existing demonstrated work       13/13 conformance verification, 2026-09-11
      ↓
Engineering Intelligence         Testing sub-ability, realized since 2026-09-02
```

**`PD-06` supports the hypothesis; it does not carry the determination.** The
Platform Organization plane and the P11 organizational layer are separate and
`ACT-CC-P11-015 §38` forbids collapsing them, so the determinative facts are
`ADR-0008`, the Capability record, and the Department record — all in the P11
organizational layer, all resident.

---

## 3. Non-manufacture determination (`§5`)

**This documents an existing capability.** The test that settles it:

> Would removing `E11-04` from existence change whether the capability exists?

**No.** `ADR-0008`, the Capability record, the consumer and the 13/13 evidence
would each be unchanged. The Skill record names an ability that was established,
implemented, exercised and evidenced before the record was written.

The prohibited shape — `E11-04 FAIL → need a Skill → invent Skill → create
capability → PASS` — would have required inventing the Testing sub-ability. It
was not invented; it was six weeks old.

**`STOP A` not triggered · `STOP B` not triggered.**

---

## 4. Skill reconciliation result

**Created:** `skill.artifact-conformance-verification` — *"checks an engineered
artifact against a stated set of conformance criteria and reports, per criterion,
whether the artifact satisfies it."* Owned centrally (`Domain Model §5`), as
every Skill is.

**Amended:** `engineering-intelligence-agent` **v1.0 → v1.1**. Its
`## Permitted Skills` read *"None declared"*, which was accurate — no Skill
record existed to name.

> **A correction recorded rather than made silently.** The prior text also said
> *"No Skill exists within the Engineering Department's scope"*, which conflated
> two things `Domain Model §5` keeps apart: **Skills are owned centrally, not by
> a Department.** What an Agent Definition declares is which centrally owned
> Skill it may use. The same conflation appeared in the Permitted Workflows
> section and is corrected there too.

**Amended:** `governance-artifact-integrity-agent` **v1.1 → v1.2** — the new
Workflow added to Permitted Workflows. **No Skill, Capability or permission was
added**; `skill.citation-discipline-verification` was already specified by that
Definition.

**`§6` honoured:** `VALID SKILL ≠ CROSS-DEPARTMENT COORDINATION`. The Skill is a
prerequisite. What follows is the coordination.

---

## 5. Actual cross-Department workflow evidence (`§7`, `§10`)

`workflow.cross-department-artifact-conformance-review` — the first resident
Workflow whose composed Skills are invoked by instances of Definitions owned by
**two different Departments**.

```text
DEPARTMENT A   engineering
      ↓        verify-artifact-conformance
               grant 0f7ac0785bd8442b · skill.artifact-conformance-verification
               performed by consumers.engineering_intelligence_agent
                            .EngineeringIntelligenceAgent.verify  (RESIDENT CONSUMER)
               → 14/14 conformance criteria · WRITES conformance-record.md
      ↓
HANDOFF / DEPENDENCY   verify-citation-discipline depends_on verify-artifact-conformance
      ↓
DEPARTMENT B   platform
               grant a437cdbbd29940af · skill.citation-discipline-verification
               performed by tools.corpus_citation_audit.audit
                            (RESIDENT REPOSITORY TOOLING — no Platform consumer exists)
               → READS that record: 4 citations, 0 unresolvable, 0 warnings
      ↓
WORK CONTINUITY / OBSERVATION / VERIFICATION
               one Workflow, resident Runtime, terminal SUCCEEDED
      ↓
PERSISTED EVIDENCE   x-department-operations/cross-department.evidence.json
```

| `§15` item | Evidence |
|---|---|
| 6 — Department A identity | `engineering`, resolved `instance → Definition → Department record` |
| 7 — Department B identity | `platform`, resolved the same way |
| 8 — dependency / handoff | `{"verify-citation-discipline": ["verify-artifact-conformance"]}`, and **the dependency was demonstrated by failure before it was demonstrated by success** — see `§7` |
| 9 — observation / verification | two outcomes recorded `success`; `proof_level: REAL-RUNTIME`, `subsystem_injected: false`, `participants: 2`, terminal `WorkflowState.SUCCEEDED` |

**`§8` honoured — agent count is never the criterion.** The measurement resolves
each participant through its Agent Definition to the owning Department and counts
**distinct Departments**: `department_count: 2`, `cross_department: true`. A
two-agent run inside one Department would measure `1` and fail.

**`§9` honoured — the work is genuine.** Conformance verification of an
engineered artifact and citation-discipline checking of a governance record are
both operations this programme performs in the ordinary course. Neither was
fabricated, and the performers are named for exactly what they are: a resident
consumer, and resident repository tooling — because **no Platform consumer
exists**, which `ACT-CC-P11-012` classified `OPTIONAL` and this Act did not
build.

---

## 6. `E11-04` re-measurement (`§10`)

**Not predeclared. Measured four times, and it failed three of them.**

| Run | Result |
|---|---|
| before remediation | `E11-04` **FAIL** — one coordination, one Department |
| after the Skill and the first run | `E11-04` **PASS**, and `E11-02`, `E11-06`, `E11-09`, `E11-10` **regressed to FAIL** |
| after the projection-key fix | `E11-09` still **FAIL** — `across_process_boundary` |
| final | **10 of 10 PASS** |

```text
E11-01 Planning                                PASS
E11-02 Delegation                              PASS
E11-03 Execution                               PASS
E11-04 Cross-Department Coordination           PASS
E11-05 Observation                             PASS
E11-06 Verification                            PASS
E11-07 Escalation                              PASS
E11-08 Accountability                          PASS
E11-09 Organizational Continuity               PASS
E11-10 Bounded Autonomy & Governance Integrity PASS

E11 = PASS (10/10)
```

---

## 7. Newly discovered gaps, and their authority classification (`§15` 11–12)

Every one was found by a control firing, not by inspection.

| | Gap | Found by | Class | Resolution |
|---|---|---|---|---|
| **G1** | **The W3 projection key assumed one live grant per instance.** The cross-Department run reuses both existing instances in a third operational root, so `project()` overwrote the W4 and W1 projections and **orphaned two live grants** | four reconciliation controls + two completeness guards | actionable, within authority | key widened to `w3-current-<context>-<instance>`; within one root an instance still has exactly one live grant, because each run revokes before issuing |
| **G2** | **Three hardcoded operational-root lists** — in `delegation_catalog`, `delegation_reconciliation` and `e11_measurement` — all went stale the moment a third root existed | `project()` refused a grant that was in no ledger | actionable, within authority | replaced by `operation_roots()`, which **discovers** roots by the records they hold |
| **G3** | **A fourth hardcoded root list, inside the measurement instrument's own subprocess** — written the same day the other three were fixed | `E11-09` measured FAIL on `across_process_boundary` | actionable, within authority | discovery in both processes |
| **G4** | The workflow-skill check required **every** invoker to permit **every** contained Skill, assuming one invoker per Workflow | `skill-not-permitted` on a canonical Workflow | actionable, within authority | widened to *"permitted by an invoker the Workflow names"* — see `§8` |
| **G5** | Three count-based controls (`len(chains)==5`, `len(contained)==10`, `len(terminal)==2`) and two more (`len(active_grants)==2`, `permitted_skills(...)==()`) encoded population snapshots | each failed on a legitimate change | control defect | re-anchored in the invariants they name |
| **G6** | `plan_to_workflow` defined a helper whose **name** read as granting | `test_the_adapter_defines_no_way_to_grant_anything` | control caught an ambiguous name | renamed to `_delegation_for`; **the control was not relaxed** |
| **G7** | `consumers.Artifact` requires an immutable line sequence; a list raised `TypeError` | the first real run's step 1 **failed** | my defect | fixed; the failure is retained in this record rather than smoothed away |

**`G2` and `G3` are the same defect, and `G3` is the more instructive.** I
replaced three hardcoded population lists with discovery and then, in the *same
session*, shipped a fourth inside the instrument whose job is to measure whether
populations are complete. It was caught because a criterion I had not weakened
went red.

---

## 8. Why `G4` is a widening and not a relaxation

`Domain Model §4` fixes **no cardinality** on `Workflow invokes Agent Instance`,
and its own `collaborates with` edge makes a one-invoker assumption untenable:
instances collaborate *"only through a shared Workflow"*, so a Workflow able to
invoke only one instance would make instance collaboration impossible in the
model that requires it.

The check still rejects the fabrication case — a Skill **no** invoker permits —
and still requires reciprocity. What it no longer does is demand that an
Engineering Definition permit a governance Skill so that two Departments can
appear in one Workflow. **That would have been authority expansion dressed as a
conformance fix**, and it is the outcome the directive's `§11` exists to
prevent.

---

## 9. Fresh P11 state (`§15` 13–15)

```text
P11 AUTHORIZED  = TRUE      E11 RATIFIED = TRUE
P11 CONSTRUCTED = TRUE      E11 PASS     = TRUE  (10/10)
P11 OPERATIONAL = TRUE      P11 COMPLETE = FALSE   ← not declared here
P11 VERIFIED    = TRUE      P11 CERTIFIED = FALSE  ← Founder act

native_core 801 OK (1 expected failure) · consumers 276 OK · tools 707 OK = 1784
citation 177 documents / 0 errors · stale-state 488 / 0 assertions
W3 4 records + 1 HISTORICAL · 0 catalog defects · 0 reconciliation defects
4 ACTIVE grants, all represented · execution-catalog 0 error 0 warning
Native Core 11 · protected paths read 0
```

**Does P11 remain incomplete? Yes.** `DP-02 §8` fixes the sequence, and
`E11 PASS` is one step in it:

```text
CONSTRUCTION EXHAUSTION → E11 RATIFICATION → E11 MEASUREMENT
→ GAP DISCOVERY → REMEDIATION → FRESH EXHAUSTION → COMPLETION → CERTIFICATION
```

This Act completed measurement, gap discovery and remediation. **Fresh
exhaustion has not been performed against the post-remediation state**, and
completion and certification are not the executor's to declare.

**Does an actionable authorized frontier remain?** Seven gaps were found and all
seven were closed within existing authority. Whether anything else remains is a
question for a fresh exhaustion pass over this new state — which is the next step
in `DP-02 §8`'s own sequence, and which this document does not pre-empt by
asserting an answer.
