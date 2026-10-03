# S-5 — Disposition Semantics Discovery & Exhaustion Gate: Record

| Field | Value |
|---|---|
| **Directive** | `docs/governance/acts/DIR-AIOS-AGENCY-S5-DISPOSITION-SEMANTICS-DISCOVERY.md` (verbatim; content sha256 `59983a317fb7518e2a32db394f4a3ee2668470acbf72dad5460e957752a42ee0`). Register `§149` (receipt), `§150` (result) |
| **Mode** | READ-ONLY. No source, schema, lifecycle, reader, ledger, plan, delegation or escalation was changed |
| **Evidence** | `evidence/s5_semantics_discovery.py` (READ-ONLY EVIDENCE TOOL) → `evidence/S5-SEMANTICS-DISCOVERY-2026-10-03.json`. 229 operational and certified files were hashed before and after: **identical**. Integrity: no faults. Certified roots: git-clean |
| **Conclusion** | • **G-S4-1:** REPRESENTATION GAP.<br>• **G-S4-2:** PARTIALLY DETERMINISTIC.<br>• **G-S4-3:** INTENTIONAL ARCHITECTURE.<br>• **Next action:** one MINIMAL REMEDIATION (MR-S5-1) resolves G-S4-1 and G-S4-2 together. No Founder decision is required. One question becomes Founder-reserved **only if** a plan- or goal-terminal outcome is ever wanted (`§I`) |

---

## A. Semantic inventory (read from the modules, not assumed)

| Mechanism | Actual values | Source | Writer | Reader | Authority | Kind |
|---|---|---|---|---|---|---|
| Delegation record status | `ACTIVE`, `REVOKED` | `tools/w4_delegation.py` | `issue()`, `revoke()` (in place, uncertified roots only, guarded) | `reconstruct`, executor `is_executable` | FD-P11-001 §9 | historical / canonical record |
| Operational disposition | `COMPLETED`, `REVOKED` | live ledger | `record_disposition`, `review_result` | `read_dispositions`, `operational_state`, `plan_outcome` | A2; FD-CG7-001 FQ-CG7-1/2; FD-P11-001 §15.2 (uncertified only) | operational, hash-bound to the record |
| Executable / current | derived: operational `ACTIVE` ∧ recipient REGISTERED in root | `w4_continuity.operational_overview` | none (derived) | same | — | derived |
| Execution outcome | `success`, `failure`, `escalation` (Domain Model §2.1, ratified) | `tools/w4_execution.py` | `W4Executor` | evidence records | grant scope | event / evidence |
| Verification | **no persisted state.** `plan_completion` → met / not met, with computed reasons. *"Cannot yet be evaluated"* = *"0 evidence records …"* | `w4_delegation.plan_completion` | none | ledger (`COMPLETED` gate), `plan_outcome` | — | derived. P12 §33 `VERIFIED` is recorded *unreachable* at rest under the ratified vocabulary (P12 open finding 2) |
| Instance lifecycle | `REGISTERED`, `RETIRED` | `agent_instance_registry` | registry | executor, `reconstruct` | FD-P11-001 §7 | canonical |
| Escalation | `OPEN`, `ANSWERED` (never `APPROVED`) | `escalation_register` | `record_refusals`; response only by a `HumanAuthority` | `reconstruct`, `status` | human (Founder in B1 / FQ-CG7-2) | decision **request** / blocker |
| Plan origin | `PLANNED`, `ADAPTED`, `REVISED` | `tools/planning/plan.py` | `adopt`, `adapt`, `revise` | `history`, `plan_outcome` | V2 A01 (carried, never widened) | canonical |
| Plan supersession | derived (`superseded`, `is_superseded`) | `PlanningSurface` | — | same | — | derived, *"never stamped"* |
| Adaptation class | `WITHIN_AUTHORITY`, `REQUIRES_ESCALATION` | `tools/planning/interfaces.py` | `classify_adaptation` | `adapt` / `revise` | — | decision gate |
| Planning operations | `declare`, `goal`, `adopt`, `adapt`, `revise`, `current`, `history`, `superseded`, `is_superseded`, `prepare_for_workflow`, `delegation_requirements` | `PlanningSurface` | — | — | — | **no** abandon / close / cancel / terminate / drop / reject / complete operation exists |
| Goal | `key`, `statement`, `authority`; **no status** | `tools/planning/goal.py` | `declare` | — | Founder instrument | canonical |
| Workflow | `DEFINED`, `READY`, `RUNNING`, `SUCCEEDED`, `FAILED` | Native Core | workflow layer | — | — | separate. *"A Plan is never RUNNING and never SUCCEEDED"* |
| Native review | `approve`, `reject` | `native_core/core/governance/decision.py` | `GovernanceReview` | — | `HumanAuthority` only | Memory-promotion review; not delegated results |
| P12 §33 failure states | `RETRYABLE`, `BLOCKED`, `REFUSED`, `FAILED`, `ESCALATED`, `SUCCEEDED`, `VERIFIED` | `p12_failure_verification` | — (a measurement) | — | — | `REFUSED` = an execution refused outside scope, persisted as an escalation. **Not** a reviewer's refusal |
| S-4 review decision | `ACCEPT`, `REWORK` (function arguments) | `w4_delegation.review_result` | — | — | FD-P11-001 §15.2; V2 A09 / A11 | persisted only as disposition + reason text, plus a plan revision |

Vocabulary not present anywhere as a delegation, plan or decision state: `EXPIRED` (Memory only), `CANCEL`, `ABANDON`, `DROPPED`, `WITHDRAWN`, `ACHIEVED`.

## B. Decision / state / evidence map

| Mechanism | Event | Evidence | Decision | State | Plan outcome | Derived |
|---|---|---|---|---|---|---|
| Execution outcome | ■ | ■ | | | | |
| Evidence record | | ■ | | | | |
| `plan_completion` (verification) | | | | | | ■ |
| Disposition `COMPLETED` | | ■ (hash-bound) | ■ (delegator) | ■ (operational) | | |
| Disposition `REVOKED` | | | ■ (delegator) | ■ | | |
| Disposition reason text | | ■ (textual) | ■ (the word) | | | |
| Plan revision (`REVISED`, `supersedes`) | | ■ (reason, evidence strings) | ■ (CEO, A01) | ■ (plan chain) | | |
| Escalation | ■ | ■ | requests one | `OPEN` / `ANSWERED` | blocks | |
| `plan_outcome` (step done, plan completed) | | | | | ■ | ■ |
| ACCEPT | | | ■ | ⇒ `COMPLETED` | ⇒ step done | |
| REWORK | | | ■ | ⇒ `REVOKED` + `REVISED` | ⇒ plan open | partly |

## C. ACCEPT

ACCEPT is **four separate facts**, all persisted or computed:

| Fact | Where it comes from |
|---|---|
| verification met | computed |
| delegator decided | disposition `recorded_by` / `authority_instrument` |
| delegation completed | `COMPLETED` |
| plan step done | derived |

**Reconstruction without text:** `COMPLETED` ⇔ verified completion recorded by the delegator. The ledger refuses `COMPLETED` unless verification is met, and binds the grant's and the evidence's sha256.

All 4 resident `COMPLETED` dispositions read correctly with no reason text:
- S-4 `4ff84423`, which carries the word ACCEPT;
- S-1 `4daebea9`, `0f7ac078`, `a437cdbb`, which carry no decision word but have the same meaning.

**DETERMINISTIC.**

## D. REWORK

REWORK = failed or insufficient verification + `REVOKED` + bound plan `REVISED` + a successor with replacement work.

**Structural** (no text):
- the grant is `REVOKED`;
- its bound plan (`lifecycle_boundary`) is superseded on the restored surface;
- the successor exists;
- verification not met (computed).

**Textual only:**
- that the revision was **caused by** this grant's result. The plan's reason and evidence are persisted as joined strings, and with several delegated steps the cause is not structural;
- that the successor's step **redoes** the work. Step keys are unique only within one plan (`plan.py:107`), and **no lineage across versions exists**;
- S-4's own REWORK used a new key (`successor_keeps_step_key: false`).

**PARTIALLY DETERMINISTIC.** The text-free reading of `9925366405d44af8` is *"REVOKED + bound plan revised (REWORK or refusal — not distinguishable)"*.

## E. REJECT

Investigated in the repository's own terms:

| Meaning | Exists? | How |
|---|---|---|
| result refused | **yes** | verification not met and / or delegator `REVOKED` |
| work not redone, plan continues | **yes** | `revise` with the step omitted (`revise` accepts any steps; the original stays in `history`) |
| refusal needing authority beyond the CEO | **yes** | escalation (`REQUIRES_ESCALATION` / `EscalationRegister`) |
| step or plan **terminal without completion** | **no** | no plan or goal status; no abandon / close / terminate operation |

**Telling REWORK from refusal-without-rework**, from structure alone (in memory, `E_rework_vs_refusal`):

| Successor | Text-free shape |
|---|---|
| rework, same key | step kept: **distinguishable** from a drop |
| refusal, drop only | step dropped, nothing added: distinguishable |
| rework, new key ≡ refusal with replacement work | step dropped, one added: **identical up to step names**, which carry no contract meaning |

**Classification: Case B, representation gap.**
- The meaning exists; it is not reconstructable deterministically in every shape.
- Not Case D: *"refused without rework"* has a meaning.
- Not Case C: it reaches plan state through `revise`.
- Not Case E: step-level refusal stays within existing CEO authority (A01 revise, A09 operational decision, delegator revocation).
- **REJECT would not duplicate ESCALATE.** Escalation routes a blocked step to human authority and never decides. A refusal within CEO authority is a delegator decision.

## F. CEO-owned steps (G-S4-3)

| Question | Finding (evidence) |
|---|---|
| Intentional? | **Yes.** The W4 execution chain (FD-P11-001 §18) executes **delegated** work. `W4Executor` holds a delegation and refuses any step outside its scope. `plan_to_workflow.compose` requires a delegation per step. Planning is not Workflow (*"A Plan is never RUNNING and never SUCCEEDED"*) |
| Is CEO work represented elsewhere? | The CEO's **review** step *is* its decision record: the disposition carries `recorded_by`, `recorded_at`, authority, reason and hash bindings. The CEO's operating actions are recorded by P13 (`docs/operations/p13/cycles`, `trace`), which is not linked to plan steps |
| Reconstructable? | Yes for review steps: done ⇔ every delegated dependency has a recorded decision (`plan_outcome`) |
| Only observability? | For **non-review** CEO steps (e.g. S-3 *"report-to-founder"*), there is no structural completion fact. That is an observability limit, not an execution-state gap |
| Would an execution record be redundant? | For review steps, **yes**: it would duplicate the disposition |

**INTENTIONAL ARCHITECTURE.**

## G. Provenance

| Direction | Result |
|---|---|
| Forward | Founder Goal → plan → step → delegation → agent → result → verification → decision → outcome. Rebuilt from file (S-4 verification); `founder_goal VERIFIED` |
| Reverse | plan outcome → disposition → verification (computed) → evidence → agent → delegation → plan → goal → Founder instrument. Complete for both S-4 paths (`G_provenance`, no faults) |
| Reverse from the REWORK **open step** | reaches the predecessor plan structurally (`supersedes`) and its revoked grant. *Which* predecessor step it replaces: reason text only (`§D`) |

## H. Observability: *"why is this step in this state?"*

Per step (`H_observability`):
- **structural:** status, done, grant, operational status, verification met / not (with computed reasons), evidence path, deciding instrument, `superseded_by`;
- **textual only:** the decision word, the rationale, and why the plan was revised.

| Step | Can the state be explained without text? |
|---|---|
| ACCEPT steps | **yes**, entirely |
| REWORK steps | *that* it was revoked after failed verification and the plan was revised: structural. *Whether* it is being redone, and *as which step*: textual |

Overall: **PARTIALLY DETERMINISTIC.**

## I. Governance

| Who | May | Basis | Changed by S-5? |
|---|---|---|---|
| Agent | produce evidence only; no accept, reject or send-back | FD-AGENCY-001 Q4-A | no |
| CEO (delegator) | review its grants (`COMPLETED` / `REVOKED`), revise plans within the goal, decide operationally | FD-P11-001 §9 / §15.2; V2 A01 / A09 / A11 / A15 | no |
| CEO | recognize verified completion; accept, send back or refuse a result **within a plan** | same | no |
| Human / Founder | answer escalations; final acceptance (A19) | `HumanAuthority`; V2 A18 / A19 | no |
| **Unassigned** | close, abandon or terminate a **plan** or **Founder Goal** unresolved | none. V2 A01 operates *"within Founder Goal / Target"*; goals carry Founder instruments; Planning has no such operation | — |

**Founder decision required? No.** Resolving G-S4-1 and G-S4-2 needs no Founder-reserved choice: step-level refusal and rework are within existing authority.

**Conditional (not raised):** if AIOS is ever to end a plan or a Founder Goal *unresolved* (*"Can rejection abandon a strategic Plan?"*), that is Founder-reserved. Nothing in S-4 or S-5 requires it.

## J. Negative controls

| # | Control | Result |
|---|---|---|
| N1 | Agent cannot create review authority | refused: *"'AGENT REVIEW AUTHORITY' is not an instrument under which a disposition is recorded"* |
| N2 | Agent cannot self-accept | refused: *"may not review delegated results"* |
| N3 | Agent cannot self-reject | refused (the same, before the decision word is even read) |
| N4 | CEO ACCEPT ≠ Founder APPROVE | held: `founder_acceptance` NOT RECORDED |
| N5 | Failed verification cannot complete | refused: *"termination by completion is not established"* |
| N6 | Revision keeps history | held: `founder-s4-rework-plan-0` retained, superseded |
| N7 | Reading does not make history current | held: no historical or decided grant appears current |
| N8 | Escalation is not authorization | held: `9cb90fa0` ANSWERED and its grant stays `REVOKED` |
| N9 | No operational change | held: 229 files identical before and after |
| N10 | No certified change | held: the same; integrity no faults; git-clean |

## K. Gap classification (one primary each)

| Finding | Primary classification | Evidence |
|---|---|---|
| **G-S4-1** No explicit REJECT | **REPRESENTATION GAP** (Case B) | `§E`: the meaning exists (`REVOKED` + `revise` without the step; escalation beyond authority), but rework-under-a-new-key and refusal-with-replacement are structurally identical |
| **G-S4-2** ACCEPT / REWORK via structure + text | **PARTIALLY DETERMINISTIC** | `§C` ACCEPT deterministic (4 / 4); `§D` REWORK's cause and redo relation textual |
| **G-S4-3** CEO steps without execution records | **INTENTIONAL ARCHITECTURE** | `§F`: W4 executes delegated work by design; the review step's record is the disposition; an execution record would be redundant |

## L. Exhaustion conclusion

| Finding | Conclusion |
|---|---|
| G-S4-1 | **MINIMAL REMEDIATION REQUIRED** (with G-S4-2) |
| G-S4-2 | **MINIMAL REMEDIATION REQUIRED** |
| G-S4-3 | **SEMANTICS SUFFICIENT**: no action |
| Founder decision | **not required**; one conditional, unraised question (`§I`) |
| Architectural / contract gap | **none** |

**MR-S5-1 (recommended, not implemented):**

| Field | Value |
|---|---|
| Affected mechanism | the delegator's disposition record (operational ledger), written by `w4_delegation.review_result` |
| Change | record the delegator's decision **structurally**, using existing semantics only:<br>• `decision`: one of the outcomes the system already has — completion recognized (ACCEPT ≡ `COMPLETED`), sent back (REWORK ≡ `REVOKED` + successor with replacement work), refused without rework (≡ `REVOKED` + successor omitting the step);<br>• `successor_plan`: the plan version the decision produced;<br>• `replaced_by`: for REWORK, the successor step that redoes the work. |
| What stays the same | no new disposition value, no plan state, no Planning contract change |
| Expected behaviour | a text-free reader distinguishes every shape in `§E`, links the open step to the failed step, and answers *"why is this step in this state?"* deterministically |
| Authority basis | the ledger and `review_result` are CEO-built operational mechanisms (S-1, S-4) under FD-P11-001 §15.2 + V2 A09 / A11. Labels for existing meanings add no authority |
| Risk | low. It is additive to the operational record only. `read_dispositions` must tolerate legacy records without the field (all S-1, CG-7, S-4 records); certified bytes are not touched |
| Verification | re-run this tool's `§E` and `§H`: every shape deterministic, the textual-only column empty for decided steps. Plus legacy-record and negative-control tests |

**Not recommended:**
- an execution record for CEO steps (`§F`);
- a new disposition or plan state;
- any plan- or goal-terminal semantics, which would be Founder-reserved.

```text
S-5  →  G-S4-1 + G-S4-2: MINIMAL REMEDIATION (MR-S5-1)  ·  G-S4-3: SEMANTICS SUFFICIENT
     →  no Founder decision required  ·  no architectural gap
```
