# P13 — E13-05 Operational Surface: Founder Decision Package

| Field | Value |
|---|---|
| **Prepared under** | `docs/governance/acts/P13-E13-05-BOUNDED-OPERATIONAL-STATE-PROOF-SURFACE-INSTRUCTION.md` (`§12`, `§13`) |
| **Date** | 2026-09-24 |
| **Prepared by** | Claude Code — AIOS Co-Founder + Delegated CEO |
| **Nature** | A decision package. **Not an FDR, and not a decision.** No option is selected, no authority is granted, and no envelope is issued. The Founder decides, and records the decision under an identifier of the Founder's choosing (see `P13-019`: the decision should not reuse a preparation number) |
| **Execution record** | `docs/governance/AIOS_P13_E13_05_OPERATIONAL_SURFACE_RECORD_v1.0.md` |

## 1. Exact decision question

> **Which bounded operational state, if any, may P13 change under explicit
> delegated authority, so that E13-05's *execute authorized action* can be
> demonstrated live, and under exactly what envelope?**

## 2. Why the decision is required

* Every category-B (operational, non-epistemic) state that P13 could change
  falls into one of three groups. It is P13's own control state (C1); or it is
  owned by another domain (C3); or it lives under a certified root the barrier
  refuses. See the record's §C.
* None is covered by existing authority: state-changing authority is **NONE**
  (FE-2, measured). `P13-018` `§4` requires any expansion to rest on *"the
  applicable governance decision"*, and P13 may not infer it (`G-08`).
* Choosing *whose* state P13 may change is an ownership and governance
  boundary. The C1/C3 framing was the Founder's own. It is not an engineering
  detail.

## 3. Current state

| | |
|---|---|
| E13-05 | **LIMITED**. Live: read-only EXECUTE, refusals, cycle bound, and now expected-vs-actual consequence (read-only). TEST-VERIFIED: the full state-changing loop, Cases A–F |
| Operational envelope | `P13-ENV-01`, evidence-only |
| State-changing authority | **NONE** |
| Construction | `P13-018` `D-1`: the E13-05 mechanism is built. No production state-changing action type exists |

## 4. Evidence

* **Mechanism, TEST-VERIFIED** (`tools/tests/test_p13_e13_05.py`, 16 tests, on a
  fixture operational object with a real state model):
  * P13 decides the target and action from observed state;
  * the expected consequence is fixed before the gate;
  * the executed action is re-observed and compared;
  * a mismatch is never a success, and is reviewed rather than retried;
  * decision provenance is verified from evidence.
* **Mutation checks.** Every new protection was removed in turn; each removal
  failed a test (M17–M27).
* **Surfaces investigated.** Twelve were classified (record §C). Organizational
  lifecycle objects (agent instances, delegations, W1/W4 operations) persist
  under certified P11 roots, which the barrier refuses [measured]. The only
  writable live operational roots are P12's `runtime-observations` (it needs a
  real Runtime) and P13's own live root.

## 5. Candidate operational surfaces

| ID | Surface | Class | Operational meaning | Live trigger today |
|---|---|---|---|---|
| **S-HOLD** | a **P13 execution hold**: a P13-owned control object, ACTIVE ↔ HELD | C1 (P13's own operational control, not knowledge) | while HELD, the gate executes nothing. P13 may move ACTIVE → HELD when an authority-bearing integrity criterion fails; only a human may move it back | none (all criteria PASS) |
| **S-CITE** | **corpus citation integrity** in a named class of non-certified, non-governance documents | C3 (documents owned by their authors) | a broken citation made to resolve. `FD-P12-002`'s criterion goes FAIL → PASS | none now. The criterion has failed live twice this session, both times from my own forward references, which I fixed by hand |
| **S-W4** | **organizational work** under existing W4 grants (`FD-P11-001`) | C3 (P11) | a delegated step executed | **blocked**: W4 operations persist under certified P11 roots. This needs a P11 relocation decision first |
| (S-RUN) | runtime observations | C3 (P12) | — | **not an option**: P13 would have to host a Runtime, which Blueprint `§4` excludes (`D06`). Recorded for completeness |

## 6. Exact state transitions

| ID | Transition | Expected consequence (fixed before execution) | Verification |
|---|---|---|---|
| S-HOLD | `hold: ACTIVE --hold--> HELD`, only when a named integrity criterion FAILs on verified evidence | next cycle: the hold is observed HELD, and every EXECUTE is refused | observe the hold object before and after; the next cycle's gate decisions all non-EXECUTE |
| S-CITE | `citation c in document d: BROKEN --repair--> RESOLVED`. Replaces exactly one broken path with the **single** existing file whose name matches. Anything ambiguous is refused | `CR-CORPUS-CITATION-ERRORS`: FAIL → PASS (or errors −1); no other line of d changes | observe d before and after (diff = one citation); re-run the audit |
| S-W4 | a delegated step PLANNED → EXECUTED, per W4 | the step's W4 outcome | W4's own verification, plus P13's consequence check |

## 7. Exact authority required (per option; each to be Founder-issued, recorded, expiring, revocable)

| Element | S-HOLD | S-CITE | S-W4 |
|---|---|---|---|
| TARGET | one hold object in `docs/operations/p13/workspace/` | the documents in a Founder-named root, **excluding** acts, registers, certified roots, `GOVERNANCE_INDEX.md` and canonical architecture | named W4 grants |
| ACTION TYPE | `p13.hold` | `corpus.repair_citation` | `w4.execute_step` |
| BOUNDARY | the hold object only | one citation, in one document, per cycle | the grant's `work_scope` and `capability_scope` |
| ALLOWED TRANSITION | ACTIVE → HELD only | BROKEN → RESOLVED only | as W4 defines |
| PRECONDITIONS | the named integrity criterion FAILs, VERIFIED | the audit reports the citation broken; exactly one candidate file exists; d is outside every excluded root | W4 grant valid; instance registered |
| VERIFICATION | §6 | §6 | §6 |
| REVERSIBILITY | human release (HELD → ACTIVE) only | prior text retained in Trace; reversal by a human edit | per W4 |
| EXPIRY | a stated date | a stated date | a stated date |
| REVOCATION | a Register REVOKED line, which is effective at the next gate decision (tested) | the same | the same |
| TRACE | premises → proposal → expected → gate → execution → before/after → consequence (built) | the same | the same |
| PROHIBITED | P13 releasing the hold; any other state | any other edit; any excluded root; creating files; deleting | anything outside the grant |

## 8. What is already authorized

* construction of the E13-05 mechanism (`P13-018` `D-1`), which is done;
* evidence-only operation (`P13-ENV-01`);
* creating escalation records (item 5). That is E13-05's *escalate* leg,
  **not** its *execute* leg: FDR-2 lists them separately.

## 9. What is not authorized

* any state-changing action;
* building a production executor for any option above;
* relocating P11 operations;
* P13 hosting a Runtime.

## 10. Options

* **O-0 — no live surface now.** E13-05 stays LIMITED, and the mechanism stays
  TEST-VERIFIED.
* **O-1 — S-HOLD.**
* **O-2 — S-CITE**, within a Founder-named document class.
* **O-3 — S-W4**, which needs a P11 relocation decision first.
* **O-4 — other.** The Founder names the surface.
* **Not an engineering option, listed because the criterion is the Founder's:**
  interpreting or amending E13-05 (FDR-2 `D07`). The instruction forbids
  weakening it, and this package does not propose that.

## 11. Consequences of each option

| Option | Consequence |
|---|---|
| O-0 | exit contract NOT MET; certification is not possible (FDR-2 `D07`, C-05). No new risk |
| O-1 | smallest risk: the action can only *restrict* P13. But it is C1, which the Founder judged *"too narrow"* as the primary proof. A live trigger needs a real integrity failure, which has not occurred |
| O-2 | the most operationally meaningful: real AIOS corpus state, and a Founder-issued criterion as the consequence. It crosses ownership (C3) and edits records' text, so the document class must exclude everything historical or authoritative. A live trigger needs a real broken citation |
| O-3 | the widest: it is organizational work. It depends on P11 changes first |
| O-4 | as specified |

## 12. Verification design (built; TEST-VERIFIED)

```text
observe → evaluate → reason → proposal WITH expected consequence (fixed)
→ gate (envelope · scope · target · preconditions · verification path · expected required · cycle bound)
→ execute (declared executor) → observe the boundary before and after (nothing outside scope)
→ fresh re-observation → re-evaluate → compare expected vs actual → matched?
→ record + Trace (the full chain) → next cycle: Memory → R-MISMATCH / rediscovery
```

Each option supplies its own `observe`, `verify` and preconditions. The chain
is common, and it exists.

## 13. Negative controls (built; TEST-VERIFIED; mutation-checked)

* Case A valid; B no authority; C expired or conflicting; D wrong target or
  tampered target list; E failed precondition; F consequence mismatch, and a
  failing executor never credited.
* Action injection (the harness cannot make P13 act; an injected EXECUTE has no
  provenance); an expectation rewritten to fit the result; execution without
  consequence verification; Trace/record disagreement; a state change with no
  expected consequence.
* Each option's own Cases A–F would be written against its real object once it
  is authorized.

## 14. What Claude can continue without the decision

* maintain and extend the mechanism and its tests;
* run evidence-only cycles, whose read-only consequences are now verified
  live;
* keep the residual frontier classified;
* prepare the residual frontier register (epistemic, E13-07 infrastructure)
  once the definition questions are answered;
* all other authorized P13 work.

## 15. Exact construction blocked by the decision

For the chosen surface only:

* its production action type (`observe`, `verify`, preconditions);
* its observation source;
* the envelope record, which only the Founder may issue;
* the live execution;
* the live Cases A–F against the real object.

**Nothing else is blocked.**

---

**Answered (appended 2026-09-24; everything above unchanged).** The Founder
decided `FDR-3` (Decision Register `§23`). It is a dedicated, bounded,
reversible S-OPS object, which is none of `S-HOLD`, `S-CITE` or `S-W4` (this
package's `O-4`). Its executable form is `P13-ENV-02` (Delegation Register
`§15`). The S-OPS surface is defined in
`docs/operations/s-ops/S-OPS-DEFINITION.md`. The live proof and its disposition
are in `docs/governance/AIOS_P13_E13_05_S_OPS_LIVE_PROOF_RECORD_v1.0.md`.
