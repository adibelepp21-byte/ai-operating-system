# S-3 — Founder Goal → CEO Planning: Execution Record

| Field | Value |
|---|---|
| **Directive** | `docs/governance/acts/DIR-AIOS-AGENCY-S3-FOUNDER-GOAL-TO-PLANNING.md` (verbatim; content sha256 `b062955eabae1ae49ecf096d365cf8183b4315608da0bb93b8a3af60265714b6`). Authority `FD-AGENCY-001`; baselines `§138` (S-1), `§139` (S-2). Register `§140` (receipt), `§141` (result) |
| **Result** | **S-3 COMPLETE / VERIFIED**. Founder Goal → CEO Plan → Delegation Requirement → CEO Delegation → existing Agent Instance, with durable provenance back to the Founder instrument |
| **Evidence** | `evidence/s3_founder_goal_run.py` (execution); `evidence/S3-VERIFICATION-2026-10-03.json` from `evidence/s3_verification.py` (fresh process, `all_ok: true`) |
| **Candidates** | not created, registered or activated. All ten: **CANDIDATE — NO ACTIVE INSTANCE** |

---

## A. Discovery

| Need | Existing mechanism |
|---|---|
| Founder Goal / Target | **Founder instruments persisted verbatim as acts**, with the content hash registered: the `GOAL-V2-00N` Goal / Target acts, the V2 "first CEO goal" act, and the S-directives. This is the V2 Founder → CEO interface (A01 *"within Founder Goal / Target"*). It is a governance practice; no code read it |
| Goal model | `tools/planning` `Goal(key, statement, authority: AuthorityProvenance)`: frozen, carries no permission, authority is a citation |
| Goal ↔ plan | `Plan.goal_key`; `PlanningSurface.declare` refuses a re-declared goal key |
| CEO planning, bounded work | `PlanningSurface.adopt`, `PlanStep.requires_delegation`, `delegation_requirements` |
| Plan → delegation | S-2 `issue_from_plan` (delegator only) |
| Citation verification | `tools/authority_citation.refusal`: the citation names the identifier, the record is that instrument's act, and the identifier is in the Register |
| Persistence / rebuild | `planning_continuity` (re-validates citations); delegation and instance records; `w4_continuity.reconstruct` |
| Provenance | S-2 `plan_provenance` (grant → plan → step) |
| Candidate model | FD-AGENCY-001 Q5-C, decision record `§4.1`, directive `§2`: **vocabulary only**. No entity, registry or contract field represents a candidate (Q6-A: role is a non-canonical descriptor) |
| Agent Instances | `AgentInstanceRegistry`; resident definitions `engineering-intelligence-agent`, `governance-artifact-integrity-agent`, `cognitive-intelligence-agent` |

**Missing:** nothing checked that a planning Goal claiming to be the Founder's actually is: that it points at a registered Founder instrument and says what the Founder said. Provenance also stopped at the plan, short of the goal.

## B. Connection (minimal; no new subsystem, entity, field or store)

| Change | What |
|---|---|
| `tools/authority_citation.py` (additions) | **`founder_goal_refusal(instrument, record, statement)`**, a reader. It accepts a Goal only if all of these hold:<br>• the citation reaches the instrument (existing `refusal`: own act, in the Register);<br>• the act is recorded as a message **from the Founder**;<br>• the sha256 of its verbatim content is **registered** (both corpus conventions; abbreviated 16-hex entries accepted);<br>• the statement occurs **verbatim** in it.<br>`founder_text(record)` returns the verbatim content |
| `tools/w4_delegation.py` (additive) | `plan_provenance` also reports `goal_statement`, `goal_authority` and `founder_goal` (`VERIFIED` / `NOT VERIFIED: …`). Reported, not required |
| `tools/tests/test_w4_plan_delegation.py` | the fresh-process assertion now checks the S-2 keys as a subset (new keys are additive), and asserts the S-2 test goal reads `NOT VERIFIED`: it is CEO-written, not a Founder quotation |

`tools/planning` is **unchanged**. Goal and plan remain separate objects with separate authorities.

## C. Founder Goal lifecycle demonstrated

Root: `docs/architecture/agency/operations/w4-s3-founder-goal/` (non-certified, outside the P11 discovery).

```text
FOUNDER GOAL   "S-3 — Connect Founder Goal to the CEO Planning Surface"
               authority  DIR-AIOS-AGENCY-S3-FOUNDER-GOAL-TO-PLANNING (registered, verbatim) → VERIFIED
     ↓ persisted (planning.state.json)
CEO PLAN       founder-s3-connect-goal-to-planning-plan-0
               authority  Co-Founder V2 A01 Executive Command   (≠ goal authority)
               steps      verify-founder-goal-intake  (delegated)
                          review-founder-goal-verification  (CEO, A11)
                          report-to-founder  (CEO, A18)
     ↓
REQUIREMENT    verify-founder-goal-intake   (inert; no delegator)
     ↓
CEO DELEGATION 50367d99c2dd4708   delegator Claude Code / AIOS Co-Founder · FD-P11-001 §9
               capability engineering-intelligence · scope verify-founder-goal-intake
     ↓
AGENT          engineering-intelligence-instance-001   (engineering-intelligence-agent v1.0, department engineering)
```

A re-run is refused (no second grant). The grant is **not executed**; that is outside S-3.

## D. Executive candidate mapping

The goal's delegated step is engineering verification, so its function target is **CTO / Engineering → Franky**.

| | Value |
|---|---|
| Candidate | Franky |
| Intended function | CTO / Engineering |
| Canonical status | CANDIDATE ONLY — NOT CANONICAL — NOT REGISTERED — NOT ACTIVATED |
| Agent Instance status | **CANDIDATE — NO ACTIVE INSTANCE** (no instance record anywhere is named after a candidate) |
| Required capability | `engineering-intelligence` (resident, department engineering) |
| Was delegation possible? | **Yes, to the existing instance** `engineering-intelligence-instance-001`, **not to Franky** |
| Evidence | `s3-run.result.json` `executive_target`; verification `candidates` |

**All ten** (from the run's `candidate_map`, re-checked in the verifier):
- every candidate is CANDIDATE — NO ACTIVE INSTANCE;
- only **CTO / Engineering** has a resident Capability;
- CEO / Executive Leadership is held by the Co-Founder / CEO office, and Luffy is not available for it (FD-AGENCY-001);
- the other eight functions have **no resident capability**. For a goal targeting them, such as the directive's marketing example (Usopp / Creative), the chain **stops at the boundary**: there is no capability and no instance to delegate to, and nothing is manufactured.

## E. Provenance: "why does this agent have this work?"

From files, in a fresh process:

```text
agent       engineering-intelligence-instance-001  (engineering-intelligence-agent v1.0, engineering)
work        verify-founder-goal-intake           ← delegation 50367d99c2dd4708 (CEO, FD-P11-001 §9)
plan step   verify-founder-goal-intake           ← requirement from plan …-plan-0 (CEO, V2 A01)
goal        founder-s3-connect-goal-to-planning  "S-3 — Connect Founder Goal to the CEO Planning Surface"
founder     DIR-AIOS-AGENCY-S3-FOUNDER-GOAL-TO-PLANNING — founder_goal VERIFIED
```

## F. Authority verification

**Positive:**
- The CEO issues.
- The Founder Goal and the CEO plan carry different authorities.
- The recipient is a registered instance of an existing definition.

**Negative** (directive `§12`; in-memory, root unchanged):

| # | Control | Result |
|---|---|---|
| 1 | Agent output cannot be a Founder Goal | refused |
| 2 | Agent cannot convert a goal into a delegation | refused |
| 3 | Planning cannot issue (`as_delegation_record`) | refused (`NotImplementedError`) |
| 4 | Non-current plan cannot produce a delegation | refused (`InvalidPlan`) |
| 5 | Candidate name cannot receive or become an instance (`usopp`) | refused |
| 6 | Candidate label cannot exercise authority (`Monkey D. Luffy` as delegator) | refused |
| 7 | Altered Founder intent (paraphrase) cannot become the goal; goal cannot be re-declared | refused |
| 8 | Scope cannot be widened | refused (`TypeError`) |
| 9 | Candidate without an instance is not an active agent (`franky`) | refused |
| 10 | Founder-reserved instrument is not delegation authority | refused |

**Unit tests:** `test_w4_founder_goal` (16) covers the same, plus fake, unregistered, changed and non-Founder instruments in a temporary repository. Two mutations were checked.

## G. Persistence and reconstruction

In a fresh process, these are rebuilt from files:
- the Founder Goal, with its statement and authority, re-validated and re-verified;
- the goal → plan link (`plan.goal_key`);
- the plan and its authority;
- the requirement, the delegation and the agent identity;
- the candidate target (from the run's non-canonical annotation);
- the provenance chain and the authority basis.

No process-local registration is relied on: the negative controls use in-memory registries and write nothing.

## H. Regression

**33 suites, all OK**, run in parallel:
- `test_w4_founder_goal` 16 · `test_w4_plan_delegation` 13 · `test_w4_operational_ledger` 24 · `test_w4_authority_chain` 47 · `test_w4_first_run_attack` 27;
- planning: continuity 14 · lifecycle 20 · negative controls 41 · prove-me-wrong 27 · plan-to-workflow 14;
- `test_delegation_reconciliation` 44 · `test_delegation_catalog` 22 · `test_escalation_register` 14 · `test_escalation_subject_integrity` 41 · `test_organization_catalog` 46;
- `test_p11_governance_boundary` 26 · `test_p11_integration_reconciliation` 24 · `test_w1_handoff_authority` 22 · `test_goal_v2_005_repairs` 12 · `test_performance_evidence` 12;
- P12 guard 30 · certified-write closure 51 · failure 24 · escalation join 20 · mutation 30 · phase authorization 45 · system negative controls 25 · W3 wiring 4;
- `test_p13` 58 · `test_p13_closure_gate` 21 · `test_p13_post_construction` 35 · `test_governance_index` 77 · `test_corpus_citation_audit` 35.

Audits: citation 0 errors; stale-state 0; certified evidence integrity no faults.

## I. Findings

| ID | Finding | Class |
|---|---|---|
| S3-1 | Founder attribution rests on the persisted verbatim instrument and its registered hash. The *"from the Founder"* header is written by the CEO when persisting, so the trust root is the persisting discipline (transcript → act → Register), the same as for every act | OBSERVATION |
| S3-2 | Two content-hash conventions exist in the Register (with and without the leading newline; some abbreviated). `GOAL-V2-002` / `-003` record their hash only in their own act header, so they cannot be verified as Founder Goals by register. They are completed and were not edited | OBSERVATION |
| S3-3 | The planning contract has no field for an executive-function target. The target is a non-canonical annotation in the run record: reconstructable from file, but not part of the planning state. This is consistent with Q6-A. Carrying it inside plans would be a contract change | OBSERVATION (decision only if wanted) |
| S3-4 | `AgentInstanceRegistry` accepts any well-formed instance key, so nothing *in code* stops the delegator from naming an instance after a candidate. That boundary is governance (FD-AGENCY-001 conditions 1 and 5). Candidates themselves have no path to create an instance, and the planning and delegation paths never register one | MINOR |
| S3-5 | The registries are in-process (S2-2): continuing to issue in a root from a fresh process needs re-registration | OBSERVATION (carried) |
| S3-6 | Eight of the ten candidate functions have no resident capability. Goals targeting them stop at the capability boundary (FD-AGENCY-001 `§4.2` gaps) | OBSERVATION; organizational expansion is Founder-reserved |

No BLOCKING finding and no true architectural gap.

## J. Disposition

**S-3 COMPLETE / VERIFIED.**
- No executive agent was instantiated.
- No hierarchy, employee structure or PD-01 change was made.
- S-4 not started.
