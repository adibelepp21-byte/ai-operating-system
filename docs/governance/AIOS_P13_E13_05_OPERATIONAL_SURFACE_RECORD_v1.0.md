# AIOS P13 — E13-05 Operational Surface Record v1.0

| Field | Value |
|---|---|
| **Instruction** | `acts/P13-E13-05-BOUNDED-OPERATIONAL-STATE-PROOF-SURFACE-INSTRUCTION.md` (content sha256 `7871c8c4…`). It grants no authority |
| **Authority used** | `P13-018` `D-1` (construction of `tools/p13` components) · `P13-ENV-01` (the live evidence-only cycle) · `DEL-CFV2-CEO-001` (recording). **No authority was created or assumed** |
| **Prepared by** | Claude Code — AIOS Co-Founder + Delegated CEO · 2026-09-24 |
| **Final classification** | **E13-05 BLOCKED — FOUNDER DECISION REQUIRED.** See §N and §P |

## A. Target

E13-05's *execute authorized action* leg, demonstrated **live**, on an
**operational** state (category B). It must not be P13's knowledge or
evidence. The full loop and all six dimensions P1–P6 were required.

## B. Semantic finding

**The proof surface must be operational state, and no such state is available
to P13 under existing authority.**

* The residual frontier register is **epistemic** (A): the definition
  document's §18 shows its content is necessarily a projection of P13's
  evidence.
* The one operational object P13 already creates under authority, an
  escalation record (item 5), is E13-05's *escalate* leg. FDR-2 lists that
  separately from *execute authorized action*.

## C. Existing surfaces investigated

| Surface | A/B | Owner | Writable? [measured] | Authority | Classification |
|---|---|---|---|---|---|
| agent instance lifecycle (REGISTERED → RETIRED) | B | P11 | **refused** (certified P11 roots) | `FD-P11-001` (P11) | BOUNDARY CONFLICT |
| W4 delegations; W1/W4 operations | B | P11 | **refused** | W4 grants | BOUNDARY CONFLICT |
| Runtime lifecycle + runtime observations | B | Native Core / P12 | the live root is writable | a real Runtime publishing its own state; P13 hosting a Runtime is excluded (Blueprint `§4`, `D06`) | BOUNDARY CONFLICT |
| Workflow / Tool lifecycles | B | P9 / Native Core | in memory; not persisted | — | UNSUITABLE |
| **escalation records** (OPEN → ANSWERED) | B | P11 register; human | writable (`docs/operations/p13/escalations`) | **ENV-01 item 5** | **the escalate leg only**. It cannot stand in for *execute* |
| `GOVERNANCE_INDEX.md` | B | governance | writable | F-4 open | AUTHORITY BLOCKED |
| Knowledge versions | B | P6 / governance | refused (certified) | governed admission | AUTHORITY BLOCKED |
| residual frontier register | **A** | P13 | — (not built) | — | epistemic: E13-07 infrastructure, **not** the E13-05 proof |
| P13 cycle records / Trace | **A** | P13 | writable | items 3–4 | evidence |
| P13 execution hold (proposed) | B | P13 | — | none | C1: a Founder option (package S-HOLD) |
| corpus citation integrity (proposed) | B | document authors | writable where uncertified | none | C3: a Founder option (package S-CITE) |
| organizational work under W4 grants | B | P11 | refused | W4 | C3; blocked on relocation (package S-W4) |

## D. Selected proof surface

**None selected, because none may be.** Choosing an operational surface
decides whose state P13 may change (C1/C3) and grants authority for it. Both
are Founder-reserved.

The package sets out three candidates, S-HOLD, S-CITE and S-W4, each with an
exact envelope:
`docs/architecture/p13-preparation/P13-E13-05-OPERATIONAL-SURFACE-FOUNDER-DECISION-PACKAGE.md`.

## E. Construction (under `P13-018` `D-1`; no state-changing authority used)

| Built | Where | What it adds |
|---|---|---|
| **expected consequence** | `model.ActionProposal.expected`; `next_action._expected` | each proposal says, **before** the gate, what it should bring about: criterion → PASS / DETERMINED / VERIFIED |
| **gate: expectation required** | `tools/p13/authority.py` | a state change with no expected consequence is REFUSED |
| **consequence verification** | `cycle._consequence` | expected vs actual after re-evaluation. A failed execution is never credited, and a mismatch is never a success. The expectation is compared and never rewritten |
| **mismatch reasoning** | `reasoning.R-MISMATCH`; `next_action` | the next cycle concludes the remedy failed. It does **not** re-propose it, and sends it for review (`review.consequence`, reserved, so ESCALATE) |
| **decision provenance** | `evidence.decision_provenance` | from evidence alone: each EXECUTE → a proposal in the record → conclusions in the record → premises observed or evaluated in that cycle. The recorded expectation must be the proposal's. An execution with no consequence verification is a fault |
| **Trace completeness** | `cycle.py` Trace outputs | `execution`: action, target, `derived_from`, envelope, authority citation and record, scope, gate reason, status, consequence. Also `consequence`. The Trace status is *failure* on a mismatch |
| **Trace/record agreement** | `EvidenceStore.verify` | the Trace and the record must name the same executed action |
| **dedicated suite** | `tools/tests/test_p13_e13_05.py` (16) | Cases A–F on a fixture operational object; injection, tampering and omission tests |

**Not built, by design:** any production state-changing action type or
executor, any workspace object, and any envelope.

## F. State transition

The fixture below is TEST-VERIFIED, not live.

```text
BEFORE      WO-1 = OPEN, WO-2 = DONE (the harness sets the world; it names no target)
P13         observes both; CR-WO-1 FAIL, CR-WO-2 PASS → defect(WO-1) → proposal close(WO-1)
            expected {CR-WO-1: PASS}
GATE        EXECUTE under the fixture envelope (target in scope; precondition "OPEN" holds)
ACTION      close(WO-1)
AFTER       WO-1 = DONE (freshly re-observed from disk); WO-2 and ledger unchanged
EXPECTED    CR-WO-1 PASS        ACTUAL   CR-WO-1 PASS/VERIFIED    → matched
NEXT CYCLE  no action; both PASS (rediscovery from the changed state)
```

**Live** (read-only, under `P13-ENV-01`): see §I.

## G. P1–P6 evidence

| Dimension | Result | Evidence |
|---|---|---|
| P1 Decision | **LIVE** for read-only actions; **TEST-VERIFIED** for state change | `decision_provenance` holds on every live record (all 6); fixture: the target is chosen from the world, and the harness cannot make P13 act |
| P2 Authority | **LIVE** for read-only (`P13-ENV-01`); **TEST-VERIFIED** for state change (fixture envelope, temporary Register) | the gate; Cases B–E |
| **P3 Execution** | **NOT LIVE.** No operational state changed live. TEST-VERIFIED only | no authority exists for a live state change |
| P4 Consequence verification | **LIVE** for read-only (expected DETERMINED/VERIFIED, matched); **TEST-VERIFIED** for state change and mismatch | §I; Cases A and F |
| P5 Evidence | **LIVE** (record + Trace with the full chain) | §I |
| P6 Re-observation | **LIVE** for read-only; **TEST-VERIFIED** for state change | re-observation after a state change is mutation-checked |

## H. Negative controls

Every one of these is TEST-VERIFIED, and every refusal is checked to leave the
state unchanged:

* Case A valid;
* Case B no grant;
* Case C expired, and conflicting grants;
* Case D grant for another object, and a tampered target list;
* Case E failed precondition (LOCKED);
* Case F: a rogue executor's mismatch is not a success and is reviewed, not
  retried;
* a failing executor is never credited with a consequence;
* the harness cannot make P13 act;
* an injected EXECUTE, a severed derivation, and an unobserved premise are
  each detected;
* a rewritten expectation is detected;
* an execution without consequence verification is detected;
* Trace/record disagreement is detected;
* a state change without an expectation is refused.

The earlier suites add authority tampering, forgery, revocation, expiry,
ambiguity, wrong scope and wrong action.

**Mutation checks M17–M27, plus re-observation:** each protection was removed,
and a test failed every time. Two protections first survived (M19, M22); tests
were added until both were caught.

## I. Live vs test evidence

| LIVE (real system, `P13-ENV-01`) | TEST-VERIFIED (fixture only) |
|---|---|
| read-only EXECUTE; cycle-bound REFUSE; decision provenance on every live record; expected-vs-actual consequence for the executed verifier (cycle `20260924T144955-e18d957a`: executed `verify.p13_evidence`, expected `{CR-P13-EVIDENCE: VERIFIED}`, actual `PASS/VERIFIED`, matched); re-observation; Trace | every state-changing step: the operational transition, the state-change consequence, mismatch review, Cases A–F |

**No test evidence is reported as live.**

## J. Authority state (FE-2 projection, measured)

| Dimension | State |
|---|---|
| Phase authorization | NOT AUTHORIZED |
| Construction authorization | AUTHORIZED — bounded to Blueprint `§10` IN (`P13-018` `D-1`) |
| Operational envelope | EVIDENCE-ONLY (`P13-ENV-01`) |
| State-changing authority | **NONE** |
| Certification | NOT GRANTED |

## K. Residual frontier register

It **remains epistemic, E13-07 infrastructure. It is not part of the E13-05
proof.** Its content is necessarily a projection of P13's evidence (definition
document `§18`). It is preserved as defined, and nothing was built for it.

## L. New dependencies

* The cycle's consequence check depends on every criterion a proposal names
  being admitted and evaluated.
* `EvidenceStore.verify` now reads each record's decision chain.
* The reserved-type list includes `review.consequence`.
* The P11 relocation question is a prerequisite for S-W4.

## M. Documentation synchronization

**Written:** this record; the decision package; the persisted instruction;
append-only notes in Blueprint `§14` and `P13-019`.

**Unchanged and still accurate:**

* the construction and reconciliation records;
* the semantic discovery and definition documents. The definition document's
  finding (the register is epistemic) is *applied* here, not revised.

## N. Remaining blocker

**No recorded authority permits P13 to change any operational state.** Which
state it may change, and under what envelope, is a Founder decision: ownership
(C1/C3) plus a grant. It is not something engineering can resolve.

## O. Founder decision required

**Yes.** The package's §1 question, with options O-0 to O-4 and exact
envelopes. **No option is selected.**

## P. Exhaustion

**AUTHORIZED ACTIONABLE CONSTRUCTION EXHAUSTED for E13-05. E13-05 = BLOCKED —
FOUNDER DECISION REQUIRED.**

* Everything `D-1` covers is built and verified.
* The live execute leg (P3) cannot proceed without a grant.

**Not COMPLETE, not DEMONSTRATED. P13 CERTIFICATION = NOT REQUESTED / NOT
AUTHORIZED.**

---

### Disclosure

A first draft of §I held a live cycle identifier and values written **before**
the live cycle had run: `…131930-e36c14c7`, `CR-MEMORY-INTELLIGENCE`. They were
a placeholder presented as evidence. I caught this before any commit and
replaced them with the actual cycle (`20260924T144955-e18d957a`). The committed
record carries only measured values.
