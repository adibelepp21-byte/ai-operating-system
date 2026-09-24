# AIOS P13 Construction Record v1.0 — under `P13-018`

| Field | Value |
|---|---|
| **Authority** | `P13-018` — Founder Construction Authority Gate Decision, **APPROVED WITH BOUNDED INITIAL AUTHORITY** (`acts/P13-018-FOUNDER-CONSTRUCTION-AUTHORITY-GATE-DECISION.md`, content sha256 `6dd19861…`; Decision Register `§22`) |
| **Scope built** | Canonical Blueprint `§10` IN (`docs/architecture/p13/AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md`) |
| **Envelope** | `P13-ENV-01`, evidence-only, **initial, not maximum** (Delegation Register `§14`; `docs/governance/p13-envelopes/P13-ENV-01.json`, sha256 `d9ad1e36…`) |
| **Prepared by** | Claude Code — AIOS Co-Founder + Delegated CEO (`DEL-CFV2-CEO-001`) · 2026-09-24 |
| **Claims** | Construction of the authorized scope, verified as stated below. **P13 completion is NOT claimed. Certification is NOT requested and NOT authorized.** |

`P13-018 §12` requires this report to distinguish fifteen things, and it
says: *"No item may be reported as complete solely because code exists."* Each
item below states the evidence for what it reports.

---

## 1. Built

`tools/p13/` has one component per link of C-01, a cycle entry point, and an
evidence store. It is 1,829 lines, and the stdlib and resident AIOS modules are
its only dependencies.

| Component | Module | Link |
|---|---|---|
| `StateUnderstanding` | `state.py` | OBSERVE / UNDERSTAND. Eight sources, each declaring its facts before it is read |
| `Evaluation` | `evaluation.py` | EVALUATE. Eight criteria, each citing a resolving Founder instrument |
| `Reasoning` | `reasoning.py` | REASON. Eight deterministic rules; each conclusion names its premises |
| `NextAction` + `ActionCatalog` | `tools/p13/next_action.py`, `tools/p13/catalog.py` | DETERMINE / PROPOSE. Fixed priority rule; ten reserved types, four read-only verifiers |
| `AuthorityGate` | `tools/p13/authority.py` | AUTHORITY CHECK. Envelope resolution (seven checks) and the Blueprint `§5.2` table, plus the cycle bound |
| `BoundedExecution` | `execution.py` | EXECUTE IF AUTHORIZED / VERIFY |
| `Evolution` | `evolution.py` | LEARN / EVOLVE. Every proposal it makes is reserved, so each one escalates |
| `Frontier` | `frontier.py` | RE-DISCOVER / exhaustion |
| cycle, evidence, model, paths | `cycle.py`, `evidence.py`, `model.py`, `paths.py` | composition · records and Trace · types · roots |

Also built or recorded:

* the envelope record `P13-ENV-01` (Delegation Register `§14` and its JSON);
* the Decision Register registration of `P13-018` (`§22`);
* `tools/tests/test_p13.py`, with 58 tests.

## 2. Verified

| Check | Result |
|---|---|
| `tools/tests/test_p13.py` | 58 OK. **Live:** two full cycles on the real tree against a temporary live root. **Negative controls:** at least one for every E13 criterion that Blueprint `§7` lists |
| Mutation check of the negative controls (a scratch copy of each module, reverted afterwards) | 5/5 detected: cycle bound removed · UNKNOWN-as-PASS · dangling premise accepted · envelope sha check removed · reserved check removed |
| Full suites | see §15 and the commit record: tools, native_core, consumers, bounded_exception |
| Certified evidence | P10/P11/P12 manifests hold · guard `{10, 11, 12}`, no anomalies · the write probe runs a real P13 cycle as a targeted entry (`tools/certified_write_probe.py` `TARGETED`) |
| Corpus | citation audit 0 errors · stale-state 0 · `P13-015` checker holds, and now requires evidence on every P13 CORE row |

## 3. Integrated

| Relationship | How | Measured |
|---|---|---|
| **Memory → P13** (`D06`, `P13-018 §7`) | `MemoryReader` over `TraceReader`, over the seven P12 trace stores and P13's own store. Read-only; Memory stays P7's | `tools/ecosystem_relationships.py`: **Memory ↔ Intelligence is CODE** (was NOT CONNECTED), via `tools.p13.state → native_core.core.memory.reader`. P13 was added to the declared Intelligence membership, which is stated with every result |
| Knowledge → P13 (`D-3`) | `create_knowledge_subsystem(…).retrieval.active("corpus-health.criteria")`, read-only | The criteria file's hash is unchanged by the read (test), and the barrier refuses writes to it |
| P12 self-model, integrity, escalation register, delegations, `authority_citation`, trace registry | consumed read-only | every live cycle |
| Escalation register | `EscalationRegister.record` only, via `EscalationRequired` | fixtures; `self_model.incomplete()` counts `docs/operations/**` |
| Governance boundary | `tools/p13/authority.py` declared a P11 handoff surface. The completeness guard caught it on the run that created it | `test_p11_governance_boundary` |

## 4. Evidence produced

Live root `docs/operations/p13/` holds four cycle records and four Trace
entries, one to one. `verify.p13_evidence` and `EvidenceStore.verify()` both
report `holds: True`.

| Cycle | Executed (under `P13-ENV-01`) | Result | Exhaustion |
|---|---|---|---|
| `20260924T121248-10b44fdb` | `verify.ecosystem_relationships` | CR-MEMORY-INTELLIGENCE UNKNOWN → PASS | NOT_EXHAUSTED (2 deferred) |
| `20260924T121257-8291ac4c` | `verify.foundational_question_reconciliation` | CR-RECONCILIATION UNKNOWN → PASS | NOT_EXHAUSTED (1 deferred) |
| `20260924T121305-22ddda05` | `verify.p13_evidence` | CR-P13-EVIDENCE UNKNOWN → PASS | **EXHAUSTED_WITH_CLASSIFIED_REMAINDER** |
| `20260924T121441-5d9aafbe` | `verify.ecosystem_relationships` (least recently verified, **chosen from Memory**) | INFERRED → VERIFIED | EXHAUSTED_WITH_CLASSIFIED_REMAINDER |

All eight criteria are PASS on the real system. The admitted `FD-P12-002`
thresholds judge the corpus: citation errors 0, live stale assertions 0, stale
governance sources 0.

## 5. Authority exercised

| Authority | Exercised as |
|---|---|
| `P13-018` `D-1` | construction of `§10` IN, by the CEO |
| `P13-ENV-01` items 1, 2, 3, 4, 6 | live: read-only verification, reading state, P13 records and Trace in the live root, and verification of P13's own evidence |
| `P13-ENV-01` item 5 | **not exercised live.** No live cycle needed an escalation. It was exercised only in the tests, against temporary roots |
| Recording `P13-ENV-01` and `§22` | an Implementation-Tier recording act, under explicit Founder direction. **Not an issuance** (`G-08`) |
| Invocation | each live run was invoked by the CEO, who is named in the record. P13 never ran itself |

## 6. Authority refused

* **Live.** Eight `REFUSE` decisions, all on the cycle bound: the second and third verifier proposed in each cycle.
* **Tests** (real governance texts, temporary copies of the envelopes and register):
  * unknown action type;
  * objects that are not proposals (a dict marked `authorized`, a prior `GateDecision`);
  * a tampered envelope;
  * a planted envelope, not in the Register;
  * a forged citation (`FD-P11-001` pointing at `README.md`);
  * a CEO-issued envelope;
  * an inactive envelope;
  * a revoked envelope;
  * a wrong live root;
  * an unreadable Register.

  Each of the envelope cases is an anomaly, not an authority.
* **Design narrowing.** Blueprint `§5.1` allowed an envelope issued *"by the
  Founder, or the CEO under `A10`"*. The gate recognizes only Founder-issued
  envelopes. This narrows the Blueprint. Widening it is a decision, and this
  record does not make it.

## 7. Escalations raised

**Live: none.** No live cycle met a reserved action, an unresolved authority
or an envelope anomaly. The four escalations `R-AWAITING` reports as OPEN are
the pre-existing P11/P12 ones. P13 cannot answer them, because
`record_response` requires `HumanAuthority`.

**For the Founder, from this report (not register entries):**

| # | Matter | Why it is yours |
|---|---|---|
| FE-1 | `P13-018` is invisible to the governance index and self-model decision list (81 decisions). The index reads `P13-NNN` as preparation numbering, and the decision shares the prepared gate's number | Choosing an alias identifier or an index rule is a governance-identifier decision. It was not made silently |
| FE-2 | The phase snapshot still reports P13 `AUTHORIZED: FALSE` (P12 `§37`). `P13-018` authorizes construction and states no phase authorization | Only a Founder decision can state a phase state. It was not inferred |
| FE-3 | E13-05 beyond evidence-only (§9) | A larger envelope is `P13-018 §4`'s *"applicable governance decision"* |

## 8. Remaining gaps

| Gap | Status |
|---|---|
| `P13-017` `0012`–`0016`, `0019`–`0022`, `0026`, `0027` | **BUILT and verified**, within the bounds stated in §9 and in `P13-015` `p13_status` |
| Five of eight reasoning rules fired only in fixtures | Live state gave `R-DEFECT`, `R-GAP`, `R-AUTHORITY` and `R-SYSTEMIC` (after the repair) nothing to fire on. Each is tested; none is live-demonstrated |
| P13's Trace actor `aios-p13-ecosystem` | This is not a registered Agent Instance. The Trace contract needs only a non-empty identity, and `D01` says P13 is not an Agent. It is adjacent to `GAP-0009`, which stays open |
| Corpus source isolation | The corpus audits read their own module root, so that one source cannot be pointed at a copy |
| `GAP-0005`, `0006`, `0009`, `0010`, `0023`–`0025` | unchanged, and not needed by P13 (Blueprint `§8`) |
| FE-1, FE-2 | §7 |

## 9. E13-01 … E13-07

| Criterion | Classification | Demonstrated by |
|---|---|---|
| E13-01 State understanding | **DEMONSTRATED (live)** | Every snapshot covers the 12 self-model answers, integrity, escalations, Memory and Knowledge. Each fact carries source, status and time. A removed source gives UNKNOWN, and a sourceless fact is rejected |
| E13-02 Evaluation | **DEMONSTRATED (live)** | 8 criteria, each resolving its authority. An unresolvable citation is refused, and missing evidence gives UNKNOWN |
| E13-03 Reasoning | **DEMONSTRATED.** Live for 4 rules; fixture for the others (§8) | Premise-less and dangling-premise conclusions are rejected |
| E13-04 Next action | **DEMONSTRATED** | Separated at the type level: no authorization field, only the gate can mint a decision, and a proposal is not executable |
| **E13-05** Bounded execution | **LIMITED — demonstrated within D-2b only** (`P13-018 §5`) | **Live:** authorized limited execution (4 × EXECUTE of read-only verifiers under `P13-ENV-01`) and the cycle bound (8 × REFUSE). **Fixture:** ESCALATE for no envelope, forged citation, reserved type and conflict; UNKNOWN; REFUSE for unknown type. **Not demonstrated:** execution of any action that changes state, because the envelope permits none. That remainder is classified, and needs a governance decision (FE-3). **E13-05 is not met in full** |
| E13-06 Evolution and re-discovery | **DEMONSTRATED**, bounded | After each execution the state is re-derived and the difference recorded, live 4×. Gaps come from failed or unknown evaluations. Evolution proposals escalate (fixture). Learning is proposal-only (`GAP-0022`) |
| E13-07 Exhaustion and frontier | **DEMONSTRATED (live)** | `EXHAUSTED_WITH_CLASSIFIED_REMAINDER`. All 20 P13 CORE rows cite evidence: 12 ANSWERED, 8 ANSWERED — BOUNDED with the bound stated (Q33, Q53, Q57, Q61, Q63, Q70, Q71, Q72). Q38 was reclassified to FRONTIER on `FDR-2 D02`. A CORE row without evidence fails the checker |

**Exit contract (C-05): NOT MET.** E13-05 is limited by design of the initial
envelope, and it is not falsely marked complete.

## 10. Residual frontier

The live classified remainder:

* `Q23` (UNKNOWN);
* `Q38`, `Q39` and `Q91` (P13 FRONTIER);
* `GAP-0017` replanning and `GAP-0018` recovery beyond escalation (`P13-017 §2`);
* re-verification of evidence already in Memory, which is always possible and
  classified as *refreshable*;
* E13-05's state-changing execution (§9).

## 11. Newly discovered dependencies

* P13 reads through, and is therefore sensitive to, `p12_self_model`,
  `certified_evidence_integrity`, the three corpus audits, `governance_index`,
  `p12_trace_registry`, Native Core Memory, Trace, Knowledge and Infrastructure,
  `escalation_register`, `planning` (`AuthorityProvenance`,
  `EscalationRequired`), `authority_citation`, `ecosystem_relationships` and
  `foundational_question_reconciliation`.
* A change to any of their outputs changes P13's facts. That is intended.
* The P11 governance boundary now constrains `tools/p13/authority.py`.

## 12. Scope pressure

Everything outside `tools/p13/` that this construction touched is listed here.
None of it widens P13's authority:

| Change | Why |
|---|---|
| `tools/certified_write_barrier.py`: absent `dir_fd` (-1) read as a descriptor | **A defect I introduced under GOAL-V2-004.** It refused every relative-path mkdir, rename, remove, chmod and utime, everywhere, including outside certified evidence. It failed closed, so nothing was exposed. Found while wiring the Knowledge read. Fixed, and a test was added that fails without the fix |
| `tools/ecosystem_relationships.py` | P13 added to the Intelligence membership. Escalations now resolve against the identifier they cite: pinned to `FD-P11-001`, P13's escalations would have read as unresolved and as *"organizational"* |
| `tools/foundational_question_reconciliation.py` | `MUST_CITE` includes P13 CORE, which is Blueprint `§7` E13-07's negative control |
| `P13-015` matrix | evidence and `p13_status` added to 20 CORE rows; Q38 → FRONTIER; a revision entry |
| `tools/certified_write_probe.py` | a targeted entry that runs a real P13 cycle |
| Blueprint, prepared gate | append-only status rows and a Blueprint `§12`. The original text is untouched |
| Test pins | ecosystem state, FDR-2 pins, P11 surface list, P13-015 checker: each updated with the evidence that changed it |

## 13. Authority conflict

**None found.** The one divergence from the Blueprint is a narrowing: only
Founder-issued envelopes are recognized (§6).

## 14. Native Core pressure

**None.** `NATIVE CORE = 11`, and no file under `native_core/` changed. P13
uses the Trace record without any schema change. The only stretch is a
semantic one: the actor string (§8).

## 15. Certification readiness

**NOT READY, and NOT AUTHORIZED.**

* E13-05 is limited (§9).
* Five rules are not live-demonstrated.
* FE-1 to FE-3 are open.
* No P13 manifest exists.

Certification would take a separate Founder decision, a P13 content manifest
on the GOAL-V2-004 model, and `docs/architecture/p13/` becoming a certified root
(Blueprint `§11`).

---

## Disclosed defects of my own, found during construction

1. **Barrier `dir_fd` defect.** From GOAL-V2-004; see §12.
2. **`R-SYSTEMIC` false positive.** Found live. The first two live cycles
   (`…10b44fdb`, `…8291ac4c`) concluded *"3 criteria … on one source (Memory):
   one cause"* from evidence that had simply never been verified. The records
   are immutable and are left as written. The rule now counts an UNKNOWN only
   against a source that was down. A test holds the corrected behaviour, and
   cycle `…5d9aafbe` ran after the repair.
3. **Caught before the first commit:**
   * a record path displayed relative to the wrong root;
   * two matrix pointers broken by a docstring line wrap;
   * a write-detector test that counted `str.replace` as a write;
   * a revoked-envelope test that read the wrong anomaly.
