# S-2 — Plan-to-Delegation: Execution Record

| Field | Value |
|---|---|
| **Directive** | `docs/governance/acts/DIR-AIOS-AGENCY-S2-PLAN-TO-DELEGATION.md` (verbatim; content sha256 `37484137d73a61f5120feb5c036680a1874d680d275857a5f028a58b463f92d1`). Authority `FD-AGENCY-001`; S-1 baseline Register `§138`. Register `§139` |
| **Result** | **S-2 COMPLETE / VERIFIED**. The connection *CEO Goal → Plan → bounded work → delegation → persisted → reconstructed*, with plan provenance, was discovered, constructed, executed, persisted, reconstructed and verified |
| **Evidence** | `evidence/s2_plan_delegation_run.py` (execution); `evidence/S2-VERIFICATION-2026-10-03.json` from `evidence/s2_verification.py` (fresh process, `all_ok: true`) |

---

## 1. Existing mechanisms discovered (No-New-Subsystem walk)

| Need | Existing mechanism | Found? |
|---|---|---|
| CEO goal, plan | `tools/planning`: `PlanningSurface.declare` / `adopt`, `Goal`, `Plan`, `PlanStep` | yes |
| Bounded work selection | `PlanStep.requires_delegation`, `PlanningSurface.delegation_requirements(plan)` returns an inert `DelegationRequirement(plan_key, step_key, scope_described, authority)`. It has **no delegator field** and `as_delegation_record` is deliberately absent (`ACT-CC-P11-005 §11`) | yes |
| Plan currency | `_require_current`: a superseded plan yields no requirement | yes |
| Issuance + authority checks | `W4DelegationRegistry.issue`: fixed delegator (`FD-P11-001 §4.1`), FD-P11-001 citation, registered live recipient, capability ⊆ permitted, all elements present, accountable ≠ recipient | yes |
| Execution bound to plan | `W4Executor.execute_plan`: refuses any step outside the work scope | yes |
| Plan persistence | `tools/planning_continuity.save` / `restore`, which re-validates every citation and recomputes supersession | yes |
| Grant persistence | `<id>.delegation.json` written by the registry | yes |
| Reconstruction | `tools/w4_continuity.reconstruct` | yes |
| Plan provenance on the grant | **existing convention**: `lifecycle_boundary = "one execution of plan <key>"`, used by every W4 grant and parsed by `_bound_plan` (S-1); the work scope names the step | yes, as a convention, not a structured field (see `§8`) |
| **Requirement → grant** | **none.** `delegation_requirements()` was called only by tests and negative controls | **the one missing link** |

The missing link cannot belong to Planning: Planning is forbidden to delegate and has no delegator. It belongs to the delegator.

## 2. Connection implemented

`tools/w4_delegation.py`, delegator side only. Two functions, no new state, field, store or authority:

- **`issue_from_plan(delegations, surface, plan, step_key, *, delegator, recipient_instance, authority, capability_scope, resource_boundary, output_expectation, verification_requirement, escalation_condition)`**
  - Checks the delegator first.
  - **Re-derives** the requirement from the surface, so it is genuine and its plan is current.
  - Refuses a step the plan did not mark for delegation.
  - Fixes everything that carries provenance or accountability. The caller cannot supply:
    - objective = the step statement;
    - work scope = that one step;
    - lifecycle = `one execution of plan <key>`;
    - accountable = the delegator;
    - termination = `on completion of the bound plan, or revocation`.
  - Then calls the unchanged `issue()`.
- **`plan_provenance(record, surface)`** traces a persisted grant back to its plan step from existing fields. It reports faults and decides nothing.

`tools/planning` is **unchanged**; Planning still delegates nothing. The delegation contract, `issue()`, `revoke()` and the S-1 ledger are unchanged; the S-1 ledger is not used.

## 3. Representative execution

Root: `docs/architecture/agency/operations/w4-s2-plan-delegation/`. It is not certified, and it is outside the P11 operation-root discovery.

| Stage | Result |
|---|---|
| CEO goal | `agency-s2-ledger-rule-verification`, authority `FD-AGENCY-001 S-2` (this directive) |
| CEO plan | `agency-s2-ledger-rule-verification-plan-0`:<br>• `verify-ledger-rules` (requires delegation);<br>• `review-ledger-verification` (CEO, A11; **not** delegated) |
| Bounded work selected | exactly one requirement: `verify-ledger-rules` |
| Recipient | `engineering-intelligence-instance-001`, an instance of the existing definition `engineering-intelligence-agent`, registered in this root under `FD-P11-001 §7`. This is the minimum non-certified fixture, as every W4 root has done |
| Delegation issued | **`0a697039a63f4c17`**, ACTIVE:<br>• delegator `Claude Code / AIOS Co-Founder`, authority `FD-P11-001 §9`;<br>• capability `engineering-intelligence`, work scope `verify-ledger-rules`;<br>• lifecycle `one execution of plan agency-s2-ledger-rule-verification-plan-0`;<br>• verification: every one of seven rules reported, with code locations;<br>• escalation: out-of-scope step, revoked grant or retired instance;<br>• accountable: delegator |
| Persisted | `0a697039a63f4c17.delegation.json`, `engineering-intelligence-instance-001.instance.json`, `planning.state.json`, `s2-run.result.json` |
| Re-run | **refused**: the script will not issue a second grant into a root that already holds one |
| Execution of the grant | **not performed.** It is not S-2. The grant waits, bounded, for its one execution |

## 4. Plan → delegation provenance (fresh process)

`plan_provenance(record, restore(planning.state.json))` returns:
- plan `agency-s2-ledger-rule-verification-plan-0` (current);
- goal `agency-s2-ledger-rule-verification`;
- step `verify-ledger-rules`;
- plan authority `FD-AGENCY-001 S-2`;
- **faults: none**.

The objective equals the step statement, and the step is marked for delegation.

## 5. Persistence and reconstruction

In a fresh process, `reconstruct(root)` gives:
- instances `[engineering-intelligence-instance-001]`;
- active grants `[0a697039a63f4c17]`;
- no unreadable records and no escalations.

`planning_continuity.restore` rebuilds the goal and plan with re-validated citations.

## 6. Authority and negative controls

Against the real restored plan, with in-memory registries (root unchanged: verified):

| Control | Result |
|---|---|
| Agent as delegator | refused (`DelegationError`) |
| Step not marked for delegation (the CEO review step) | refused |
| Widen work scope / rename plan / move accountability | refused: the function takes no such argument (`TypeError`) |
| Capability beyond the recipient | refused |
| Founder-reserved instrument as delegation authority | refused (must cite FD-P11-001, whose `§12` excludes reserved matters) |
| Unregistered recipient | refused |
| Superseded plan | refused (`InvalidPlan`) |

Also covered by the unit tests:
- the grant is immutable (frozen);
- the executor refuses the plan's second step (`review` → `escalation`);
- the grant payload has no decision or delegation field.

## 7. Regression

**31 suites, all OK**, run in parallel:
- `test_w4_plan_delegation` 13 · `test_w4_operational_ledger` 24 · `test_w4_authority_chain` 47 · `test_w4_first_run_attack` 27;
- `test_planning_continuity` 14 · `test_planning_lifecycle` 20 · `test_planning_negative_controls` 41 · `test_planning_prove_me_wrong` 27 · `test_plan_to_workflow_gate` 14;
- `test_delegation_reconciliation` 44 · `test_delegation_catalog` 22 · `test_escalation_register` 14 · `test_escalation_subject_integrity` 41;
- `test_p11_governance_boundary` 26 · `test_p11_integration_reconciliation` 24 · `test_w1_handoff_authority` 22 · `test_goal_v2_005_repairs` 12 · `test_performance_evidence` 12 · `test_organization_catalog` 46;
- `test_p12_certified_evidence_guard` 30 · `test_certified_write_closure` 51 · `test_p12_failure_verification` 24 · `test_p12_governance_escalation_join` 20 · `test_p12_mutation_verification` 30 · `test_p12_phase_authorization` 45 · `test_p12_system_negative_controls` 25 · `test_p12_w3_resident_wiring` 4;
- `test_p13` 58 · `test_p13_closure_gate` 21 · `test_governance_index` 77 · `test_corpus_citation_audit` 35.

## 8. Findings (no gap blocks S-2)

| ID | Finding | Classification |
|---|---|---|
| S2-1 | Plan provenance on a grant is a **text convention** (`lifecycle_boundary` names the plan; the work scope names the step), not a structured field. It is reliable because `issue_from_plan` fixes it, and it is parsed by the existing `_bound_plan`. A grant issued directly through `issue()` can carry any text | contract observation; **no decision needed** for S-2. A structured plan reference would be a contract change for a later step |
| S2-2 | `AgentInstanceRegistry` and `W4DelegationRegistry` are in-process. A fresh process can **read** state (`reconstruct`) but cannot **continue issuing** in the same root without re-registering (the S-1 C-2 pattern) | relevant to S-3 / S-7; not to S-2 |
| S2-3 | `delegation_catalog.operation_roots()` discovers only `docs/architecture/p11/*`. Post-P11 operational roots are therefore not represented in W3 or E11. That is correct for certified P11 measurement, and it is what the S-6 unified view must address | observation for S-6 |

## 9. Files and records changed

- **Code:** `tools/w4_delegation.py` (additions only: `TERMINATION_ON_PLAN`, `issue_from_plan`, `plan_provenance`); `tools/tests/test_w4_plan_delegation.py` (13 tests, mutation-checked).
- **Operational:** `docs/architecture/agency/operations/w4-s2-plan-delegation/` (4 files).
- **Evidence:** `evidence/s2_plan_delegation_run.py`, `evidence/s2_verification.py`, `evidence/S2-VERIFICATION-2026-10-03.json`.
- **Records:** this file; `acts/DIR-AIOS-AGENCY-S2-PLAN-TO-DELEGATION.md`; Register `§139`.
- **Not changed:**
  - `tools/planning`;
  - the delegation contract;
  - the S-1 ledger;
  - every certified root (58 P11 files byte-identical; integrity no faults; `git status` clean).

**S-2 COMPLETE / VERIFIED.** S-3 not started.
