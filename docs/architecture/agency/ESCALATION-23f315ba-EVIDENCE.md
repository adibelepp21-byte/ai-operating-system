# Escalation `23f315ba9f504272` — Evidence for Founder Decision Q-S1-B

| Field | Value |
|---|---|
| **Requested by** | Founder, S-1 decision (`docs/governance/acts/FD-AGENCY-001-S1-TERMINAL-STATE-DECISION.md`, Q-S1-B: *"DEFER PENDING EVIDENCE"*) |
| **Status of this document** | Evidence only. The escalation is **not closed**; no grant was issued; nothing was written to the escalation's root |
| **Escalation record** | `docs/architecture/p11/w4-operations/23f315ba9f504272.escalation.json`, certified P11 evidence (sha256 `0e81b017…` in the P11 manifest), byte-intact. State: **OPEN** (no response file) |

---

## The record, verbatim

```json
{
  "escalation_id": "23f315ba9f504272",
  "subject": "plan w4-first-execution-proof-plan-0 / delegation 4313bd2246124a94",
  "required": "report-conformance",
  "held": "('verify-delegation-elements',)",
  "reason": "step 'report-conformance' is outside the delegated work scope — `§22`: the organization may execute more work, it may not expand the authority under which it operates",
  "authority_instrument": "FD-P11-001 §9",
  "authority_record": "docs/governance/acts/FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md",
  "raised_at": "2026-09-11T02:33:13.801276+00:00"
}
```

## 1. Escalation reason

The W4 executor refused step `report-conformance` because the grant `4313bd2246124a94` held only `verify-delegation-elements`.

This was a **deliberately constructed proof**. `P11-INTEGRATION-RECONCILIATION.md` records it as *"a **second real run** with a deliberately narrowed work scope"*. Its purpose was to show that a refusal becomes persisted organizational state in the escalation register. The runner's own default scope includes both steps (`tools/w4_first_run.py`, `run(work_scope=("verify-delegation-elements", "report-conformance"))`); the evidenced run passed only the first.

## 2. Remaining requested action

Step 2 of plan `w4-first-execution-proof-plan-0`:

> `PlanStep("report-conformance", "Report which criteria were satisfied.", depends_on=("verify-delegation-elements",))`. Source: `tools/w4_first_run.py`.

## 3. Authority currently available

| Holder | Authority | Basis |
|---|---|---|
| Grant `4313bd2246124a94` | `verify-delegation-elements` only. Its lifecycle ("one execution of plan …") is **consumed**. Operationally ACTIVE: no disposition recorded, because its plan did not complete and Q-S1-B is open | the delegation record; S-1 |
| Co-Founder / CEO (delegator) | may issue a **new** bounded W4 grant for the step. A grant cannot be widened: records are append-only. `FD-P11-001 §22`: *"the organization may execute more work"* | A10; `FD-P11-001 §4.1`, `§9`, `§22` |
| Founder | the only authority that can **close** the escalation: `EscalationRegister.record_response()` requires a `HumanAuthority` | `tools/escalation_register.py`; Constitution `§6.2` inv. 2 |

## 4. Is the requested action within the original delegation scope?

**No.** `required: report-conformance` is not in `held: ('verify-delegation-elements',)`. That is the reason the escalation exists.

## 5. Is execution required?

**No canonical condition requires it.** The information the step would report already exists:

- `first-execution.evidence.json`: `criteria_total 13`, `criteria_satisfied 13`, `criteria_unsatisfied []`;
- the cross-department run later re-verified the same module against **14/14** criteria, including the provenance element the first run did not check (`cross-department.evidence.json`; `conformance-record.md`);
- `P11-FOUNDER-COMPLETION-REVIEW.md §3`: no completion condition, P11 acceptance criterion, operational integrity condition or P12 entry condition depends on this escalation.

Executing the step would add a duplicate report of a result already recorded twice.

## 6. Consequences of closing without execution (B1)

| Effect | Detail |
|---|---|
| Plan `w4-first-execution-proof-plan-0` | stays **incomplete** permanently: step 2 never runs |
| Grant `4313bd2246124a94` | can never reach `COMPLETED` (its plan did not complete). Its correct operational end would be a `REVOKED` disposition (delegator withdrawal) in the live ledger |
| E11 measurements | **E11-07** still passes: it requires that an escalation was *persisted*, and the record stays. **E11-05** `blocked_work_observable` would read `False` on live data, but E11-05's PASS does not depend on it (`tools/e11_measurement.py`) |
| Continuity | `w4-operations` would stop reporting `OPEN ESCALATIONS`; no other root is affected |
| Certified P11 evidence | unchanged, **provided the response is not written beside the escalation** (finding F-S1-4, below) |

## 7. Would a new delegation be required?

- **B1 (close, no execution):** no.
- **B2 (execute the step):** **yes.** It needs a new bounded grant with `work_scope = ("report-conformance",)` to `engineering-intelligence-instance-001` (capability `engineering-intelligence`), issued by the CEO office. Two further facts bind B2:
  - the resident runner persists into `docs/architecture/p11/w4-operations`, which is certified, so the guard refuses its writes. B2's execution evidence would need a location outside the certified root, which is new execution wiring;
  - it duplicates an existing result (item 5).

## 8. Founder decision explicitly requested by the escalation

**None is named in the record.** The record states only `required` versus `held` authority and the reason. It does not request a specific decision.

The register routes it to the human/Founder authority (`P11-FOUNDER-COMPLETION-REVIEW.md §2`). The only action it structurally awaits is a **recorded human response**.

## F-S1-4 — applies to either choice

`record_response()` writes `23f315ba9f504272.response.json` **beside the escalation**, inside the certified P11 root, with no guard call. Under either B1 or B2, persisting your response there would add an undeclared file to certified evidence (an integrity fault).

So whichever you choose, the response must be recorded **outside the certified root**, following the same A2 pattern as the delegation ledger. That is a small, bounded change to the escalation register, and it needs your authorization together with Q-S1-B.

## Summary

| | B1 — acknowledge and close | B2 — new bounded grant |
|---|---|---|
| New authority | none | one bounded grant (CEO-issued) |
| New work | none | one step, duplicating an existing result |
| New wiring | response recorded outside the certified root | the same, **plus** execution evidence outside the certified root |
| Grant `4313bd22` afterwards | `REVOKED` disposition (live ledger) | `REVOKED` disposition; the new grant would follow its own lifecycle |
