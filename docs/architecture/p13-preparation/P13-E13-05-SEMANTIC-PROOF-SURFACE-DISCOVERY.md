# P13 — E13-05 Semantic Proof Surface Discovery

| Field | Value |
|---|---|
| **Prepared under** | `docs/governance/acts/P13-E13-05-SEMANTIC-PROOF-SURFACE-DISCOVERY-INSTRUCTION.md` (content sha256 `92fce984…`). It authorizes discovery, semantic analysis, evidence reconciliation, boundary analysis and decision preparation, and nothing else |
| **Date** | 2026-09-24 |
| **Prepared by** | Claude Code — AIOS Co-Founder + Delegated CEO |
| **Nature** | **Discovery report. Not an FDR, not a decision, not a design.** Nothing here selects an authority option, grants authority, or builds anything. No code, register, governance record or canonical document was changed to produce it |
| **Evidence labels** | **[CAN]** canonical · **[VER]** verified reality · **[MEA]** measured in this discovery · **[IMP]** implementation fact · **[DIS]** discovery result · **[PRO]** proposed · **[UNK]** unknown · **[INS]** insufficient evidence |

---

## 1. Executive finding

**One operational reality inside the C2 boundary has a reason to exist
independently of E13-05 testing: the *residual frontier register* (candidate
S11).** It is AIOS's standing record of what is known to be unresolved and
outside the authorized completion contract. Each item carries its
classification basis and status over time. The canonical architecture already
assigns it to P13 [CAN/IMP]:

* FDR-2 `D08` requires completion *with a classified residual frontier*;
* E13-07 requires that *"unresolved frontier is explicitly recorded"*;
* the Blueprint's `Frontier` component **owns *"the residual frontier
  register"*** (`§3.2`).

**It is not realized** [MEA]. Each cycle recomputes the frontier and writes it
into that cycle's record. P13's Memory keeps only the exhaustion state. So P13
cannot tell a frontier item it has classified before from one it has just
discovered. Frontier items that humans have recorded in prose are also
invisible to it.

**A defensible semantic chain can be established on S11 (§6–§8), but only
under three conditions the Founder must decide (§15):**

1. That a P13-owned register *about AIOS's frontier* counts as operational
   reality beyond P13's internal existence. It sits between C1 and C3, and this
   report places it in C2 but cannot settle that alone.
2. That the register **never becomes a second source of classification
   authority**. Canonical frontier classification stays in `P13-015` and
   `P13-017` and with the Founder/CEO. The register tracks it and may never
   reclassify or close anything.
3. That a **live** proof waits for real frontier movement after the register
   is first established. The frontier has not moved across 5 live cycles [MEA],
   and establishing the register is not itself a sufficient proof (instruction
   `§18` item 12).

**If the Founder rejects condition 1, the finding is: NO SUFFICIENT SEMANTIC
PROOF SURFACE IDENTIFIED within C2.** Every other operational reality P13
observes is one of the following [MEA]:

* P13's own mechanics (C1);
* owned by another domain (C3);
* stored under a certified root that the certified-write barrier refuses;
* governed, needing a human authority or a Founder/Architect decision.

In that case E13-05 would need either a C3 decision or an amendment of the
criterion. §15 frames both.

---

## 2. The E13-05 contract being tested

| Source | Text |
|---|---|
| **[CAN]** FDR-2 `D07` | *"E13-05 — Bounded Autonomous Execution. Where D05 permits autonomous execution, P13 can: check authority; execute authorized action; refuse unauthorized action; escalate reserved/ambiguous action; record evidence; verify outcome."* |
| **Accepted working definition** (instruction `§2`; no registered identifier) | *determine and execute an appropriate state-changing action within a valid authority envelope, while refusing unauthorized or ambiguous actions, verifying the resulting state against expected consequences, recording evidence, and re-observing / re-discovering the changed state* |
| Proof dimensions (instruction `§3`) | P1 Decision · P2 Authority · P3 Execution · P4 Consequence verification · P5 Evidence · P6 Re-observation |
| Minimum meaningful change (instruction `§4`) | B1 state before known · B2 P13 determines the action · B3 real state change · B4 expected consequence · B5 result observable again |

**Reconciliation.** The two do not conflict. The working definition elaborates
the canonical text: it adds *determine*, *expected consequence* and
*re-observe*. The canonical text is conditional (*"Where D05 permits"*), so
E13-05 is met only where authority permits. The working definition is not
registered, so where the two appear to differ, FDR-2 governs.

**Overlap to keep in view.** FDR-2's E13-06 [CAN] reads: *"propose or execute
authorized changes; verify changes; rediscover resulting state; maintain
evidence of what changed."* The overlap is examined in §12.

## 3. Evidence reviewed

| Evidence | What it established |
|---|---|
| FDR-2 `D05`, `D07` (E13-05/06/07), `D08` [CAN] | the contract and bounded completion, with a classified residual frontier |
| `P13-018` (`D-1`, `D-2b`, `§3`–`§9`) [CAN] | construction authorized; the evidence-only envelope; its prohibitions |
| Blueprint `§3.2`, `§5`, `§6`, `§10`, `§12`, `§13` [IMP, CEO architecture] | `Frontier` *owns the residual frontier register*; the gate table; the evidence model |
| `P13-019` decision surface [PRO] | E-0…E-3. E-1 is a *boundary*, the workspace, with no semantic content: the gap this discovery exists to fill |
| Delegation Register `§14` / `P13-ENV-01` [CAN] | item 3: *creation of P13-specific records and evidence in the designated live root* |
| `tools/p13/frontier.py`, `cycle.py`, `state.py` [IMP] | the remainder is recomputed each cycle from `P13-015` and `P13-017` and the cycle's decisions; it is not persisted beyond the cycle record |
| P13 Trace, latest entry [MEA] | outputs hold `exhaustion` but no frontier content, so Memory has no frontier |
| 5 live cycle records [MEA] | the same 6 frontier items in every cycle (`GAP-0017`, `GAP-0018`, Q23, Q38, Q39, Q91); the rest of the remainder is *refreshable* |
| `docs/operations/README.md` [VER] | `runtime-observations/` is live state written by a P12 tool; currently empty (`.gitkeep`) |
| Certified-write barrier, queried [MEA] | refuses `docs/architecture/p12/trace-stores/…` and `docs/architecture/p11/w4-operations/…`; allows `docs/operations/**`, `GOVERNANCE_INDEX.md` and `P13-015` |
| Self-model [MEA] | 4 OPEN escalations (P11/P12); *"What is running?"* live = none |
| Construction and reconciliation records [VER] | P13-discovered gaps that exist **only in prose**: sub-record span overrun, Trace actor, 4 rules not live-exercised |

## 4. Candidate operational realities (Q1)

"Owner" and "authority" are as the canonical sources state them.

| ID | Semantic name | Real operational condition | Source | Owner | Authority to change | Observable | Mutable | Lifecycle | Why P13 cares |
|---|---|---|---|---|---|---|---|---|---|
| S1 | Evidence currency | whether P13's verified facts are current or only remembered | `R-STALE`, Memory [IMP] | P13 | ENV-01 items 1, 3, 6 (already) | yes | append-only records | per cycle | E13-01/02 certainty |
| S2 | Open escalations | a refusal awaiting a human answer | escalation register [VER] | P11 register; human | `record_response` needs `HumanAuthority` | yes (4 OPEN) | human only | OPEN → ANSWERED | `R-AWAITING` |
| S3 | Corpus-health defects | citation errors, live stale assertions, stale governance sources | `FD-P12-002` criteria [CAN] | the owners of each document | governance / architecture edits (reserved) | yes (0 now) | not by P13 | occurs on edits | `CR-CORPUS-*` |
| S4 | Governed Knowledge criteria | the admitted thresholds P13 judges by | `FD-P12-002`, `P13-018` `D-3` [CAN] | P6 / governance | governed admission (reserved) | yes | not by P13 | admission / revision | E13-02 |
| S5 | Foundational-question classification | what each P13 question's status is | `P13-015` [PRO/CEO] | CEO record; Founder decisions | CEO/Founder; reclassifying frontier is prohibited here (instruction `§18` item 20) | yes | writable, not by P13 | revisions | E13-07 |
| S6 | Governance Index currency | whether `GOVERNANCE_INDEX.md` reflects the corpus | `GOVERNANCE_INDEX.md` [VER] | governance | **F-4 edit authority open** | yes | writable, not authorized | — | E13-01 |
| S7 | Runtime observations | *"what is running"*, the latest state per runtime/workflow | `docs/operations/runtime-observations` [VER] | P12 tool `p12_runtime_observation` | a real Runtime publishing its own state | yes (empty) | by publishers | overwritten per publish | self-model *What is running?* |
| S8 | Organizational W4 work | delegated work executing | `FD-P11-001`, W4 [CAN] | P11 organization | W4 grants | yes | writes certified `…/p11/w4-operations` | per run | `P13-019` E-2 |
| S9 | Corpus-health work path | the P12 hosted assessment (Runtime, Workflow, Memory, Knowledge) | `aios_corpus_health_run` [IMP] | P12 | P12 | yes | its Trace store is under a certified root | per run | the Memory → P13 source |
| S10 | Founder attention state | what currently needs the Founder | `_briefing`, Q61/Q62 [IMP] | P13 | ENV-01 items 3–4 (per cycle) | yes | per-cycle records | per cycle | Q61, Q62 |
| **S11** | **Residual frontier register** | **what AIOS knows to be unresolved and outside its completion contract, each item with its classification basis, first-observed and status over time** | **FDR-2 `D08`, E13-07 [CAN]; Blueprint `§3.2` "Frontier … owns the residual frontier register" [IMP/CEO architecture]** | **P13 (`Frontier`), per the Blueprint** | **none granted for a standing register** | **its inputs yes; the register itself does not exist [MEA]** | **would be mutable, with retained history** | **item admitted → annotated → canonically resolved elsewhere** | **E13-07; `D08`; telling new frontier from known** |
| S12 | P13's deferred agenda | which verifications P13 still owes itself | `NOT_EXHAUSTED` deferral, `last_executed` [IMP] | P13 | ENV-01 | yes | via Memory | per cycle | NextAction ordering |

**Artificiality test** (instruction `§20`: *would this make sense if E13-05
testing did not exist?*):

* **S11 passes.** It was named in the Blueprint before E13-05 was an exit
  blocker. It answers a requirement that is already canonical, and a real gap
  shows today: P13 has no cross-cycle frontier knowledge.
* **S10 and S12 pass only as P13 mechanics.**
* Nothing was invented for this report.

## 5. Candidate analysis (Q2)

The instruction asks for classification, not a ranking or score.

| ID | B1 | B2 | B3 | B4 | B5 | P1–P6 | Classification | Evidence |
|---|---|---|---|---|---|---|---|---|
| S1 | yes | yes | only records (C1) | weak | yes | P3 is not beyond P13 | **UNSUITABLE FOR FIRST PROOF** (C1) | a P13 → P13 refresh, already inside ENV-01 |
| S2 | yes | no action exists for P13 | no | — | — | P2 impossible | **AUTHORITY BLOCKED** | `record_response` requires `HumanAuthority` (Constitution `§6.2` inv. 2) |
| S3 | yes | yes (the remedy is determinable) | only by editing other domains' documents | yes | yes | P2 reserved | **BOUNDARY CONFLICT** (C3) · **AUTHORITY BLOCKED** | the remedy is `change.governance`, reserved, always escalated. It is the most *meaningful* reality, which is why it is recorded here: it is the natural later extension, not the first proof |
| S4 | yes | yes | only by admission | yes | yes | P2 reserved | **AUTHORITY BLOCKED** | governed admission (principle 5) |
| S5 | yes | partly | only by reclassification | — | yes | prohibited | **AUTHORITY BLOCKED** | instruction `§18` item 20; classification is a CEO/Founder instrument |
| S6 | yes | yes | yes, technically (writable) | yes | yes | P2 open question | **AUTHORITY BLOCKED** | F-4 must not be converted into authorization |
| S7 | yes | no | only by a Runtime publishing its own state | — | — | P3 would be fabricated | **BOUNDARY CONFLICT** · **UNSUITABLE** | P13 has no Runtime, and `publish` forbids fabricated state |
| S8 | yes | yes | writes certified roots | yes | yes | barrier refuses | **BOUNDARY CONFLICT** | `…/p11/w4-operations` is refused [MEA] |
| S9 | yes | yes | writes a certified root | yes | yes | barrier refuses | **BOUNDARY CONFLICT** | its Trace store is refused [MEA]. **New observation:** that P12 path cannot currently run in place |
| S10 | yes | yes | yes | only tautologically (content = composition) | re-reading adds nothing | P4 and P6 weak | **INSUFFICIENT for P6** | the consequence (the Founder informed) is not observable to P13 |
| **S11** | **yes** (its inputs are observed every cycle) | **yes** (P13 derives the divergence between register and observed frontier) | **yes** (a standing, mutable register) | **yes** (§7) | **yes** (observed next cycle; changes what P13 classifies as new vs known) | P1–P6 each satisfiable (§6–§8) | **PARTIALLY SUPPORTED** | conditional on the §1 and §15 questions; live divergence currently only at establishment [MEA] |
| S12 | yes | yes | only via Memory | yes | yes | P3 P13 → P13 | **UNSUITABLE FOR FIRST PROOF** (C1) | P13's own scheduling |

## 6. State before → action → state after (Q3), for S11

```text
STATE BEFORE      register R holds items {g1…gn}, each with basis, first-observed, status.
                  The observed frontier F (from P13-015 / P13-017 / the cycle's classified
                  remainder) contains an item x ∉ R.
P13 OBSERVATION   StateUnderstanding reads R and F: fact "frontier.divergence" = {x}.
P13 EVALUATION    criterion (authority FDR-2 D08 / E13-07: "unresolved frontier is
                  explicitly recorded"): R ≡ F on items → FAIL, evidence {x}.
P13 REASONING     x is classified in a resolving source; the right transition is ADMIT,
                  not ANNOTATE (basis changed) and never REMOVE (closure is not P13's).
P13 ACTION        propose "frontier.admit x, basis b"; the gate checks the envelope.
CONSEQUENCE       R' = R ∪ {x: basis b, first-observed now, status registered}.
STATE AFTER       R' on disk; the canonical sources are unchanged.
RE-OBSERVATION    the next cycle reads R': divergence = {}; x is reported as known since
                  cycle N, not new; the criterion PASSes.
REDISCOVERY       attention moves to the next divergence, or to an annotated item whose
                  basis has since changed.
```

**Why R ≠ R' is an operational transition, not a mutation.**

* Before, AIOS's knowledge of its own unresolved frontier existed only as a
  per-cycle recomputation that P13 could not remember.
* After, P13 holds that knowledge persistently, with provenance.
* That changes what P13 subsequently concludes. It can say *"new since the last
  cycle"* versus *"known since cycle N"*, which today it cannot [MEA]. It can
  also notice when a known item's basis has moved.
* The transition's meaning is causal (§8), not its size.

## 7. Expected consequence (Q5)

**Expected before execution.** All five must hold:

1. R' contains exactly x with basis b, and no other item changes;
2. the canonical sources are byte-identical;
3. the next observation's divergence equals the previous divergence minus
   {x};
4. the frontier criterion's result changes from FAIL to PASS if x was the
   only divergence;
5. no escalation or proposal of a reserved remedy is suppressed by x's
   registration.

**Expected = actual.** The outcome is success. The difference is recorded, and
the next cycle starts from R'.

**Expected ≠ actual. Not automatically a failure; an intelligence condition
S11 supports naturally:**

| Mismatch | What it means | P13's path |
|---|---|---|
| R' lacks x, or holds more than x | the write was incomplete or reached outside the target | a FAILURE outcome (no false success). Re-observe R; the divergence persists; rediscover, and escalate if it repeats |
| divergence ≠ previous − {x} | the frontier itself moved between observation and verification: a source changed, or the Founder/CEO reclassified something | **not an execution failure.** Re-observe F, re-evaluate, and rediscover the new divergence. This is exactly the condition the register exists to surface |
| x's basis no longer resolves after admission | the canonical row was reclassified or removed | the next cycle ANNOTATEs x as *basis changed*, and never removes it. Closure is proposed through escalation |

## 8. Re-observation and rediscovery (Q6)

**New information after the change:**

* item x's *registered* status and first-observed provenance;
* the divergence fact, now {} for x;
* thereafter, *basis-changed* detection for x.

None of these is observable today [MEA].

```text
before (R)  → ADMIT x → after (R') → new observation: x known since N; divergence reduced
            → new evaluation: frontier criterion PASS for x
            → rediscovery: next divergence, or a basis-changed annotation
```

The changed state alters what P13 *concludes* in every later cycle, not only
what a file contains. That is the P6 property E13-05 requires.

## 9. Causal attribution (Q4)

| | |
|---|---|
| **The harness may provide** | a world state: a register state R (possibly empty or behind) and frontier sources F, real or fixture copies. It may also provide an envelope record (fixture only, in a temporary Register copy, as in `test_p13_post_construction.py`) |
| **The harness may NOT provide** | the item x, the transition type, the target entry, the basis, the expected consequence, or any instruction to "admit" |
| **P13 must infer** | the divergence R vs F; each item's classification basis from the sources that resolve it |
| **P13 must determine** | which transition (ADMIT / ANNOTATE; never REMOVE), which item first (priority), the expected consequence |
| **Must be independently verified** | R' against the harness's own recomputation; the canonical sources byte-identical; nothing else in the boundary changed; the Trace entry naming P13's derivation (premises → conclusion → proposal → gate → outcome) |

Attribution holds if the harness's world change is **indifferent** to the
action: it creates a divergence without naming it. It holds if P13's recorded
premises name the observed divergence. Under those two conditions, P13's
reasoning is the only source of *which* transition occurred. That is shown by
the proposal's `derived_from` chain in the cycle record.

## 10. Authority analysis (Q9)

The requirement is stated here only after the surface was established.

| Dimension | Current state (FE-2, measured) | What S11's transition needs |
|---|---|---|
| Phase authorization | NOT AUTHORIZED | not needed for this proof; unchanged |
| Construction authorization | AUTHORIZED, `P13-018` `D-1` | realizing the register and a transition executor. **[UNK]** whether this falls under `D-1` (Blueprint `§3.2` names the register as a `Frontier`-owned object) or needs its own construction authority. **Not inferred** |
| Operational envelope | EVIDENCE-ONLY (`P13-ENV-01`) | **[UNK]**. An append-only realization (each transition an appended record, the register a derived view) *could be argued* to fall under item 3, *"creation of P13-specific records"*. **This report does not make that argument** (instruction `§15`: technical feasibility is not authority) |
| State-changing authority | NONE | **needed** for a standing, mutable register |
| Certification | NOT GRANTED | unaffected |

**Minimum authority, described and not granted:**

* **one action class**: register transitions ADMIT and ANNOTATE only;
* **one target**: a single register artifact in `docs/operations/p13/workspace/`;
* **forbidden**: REMOVE, CLOSE, RECLASSIFY, any write to canonical sources, any
  field that carries authority;
* **reversible**: prior state retained; reversal by a later authorized
  transition, never by deletion;
* **one transition per cycle** (already the cycle bound);
* **preconditions** (§11 E);
* **a verification path** (§7);
* **Founder-issued, recorded, expiring, revocable**.

**Relationship to `P13-019`.** This surface fits inside E-1's boundary. E-1 as
written supplied the boundary and not the semantics. **This report does not
select E-1** (instruction `§18` item 3).

## 11. Negative behavioural cases, all on S11

Each case is tied to the same operational reality (instruction `§17`):

| Case | Concrete condition | Expected |
|---|---|---|
| **A** valid authority | a divergence x exists; a resolving envelope grants frontier ADMIT for the register target; the preconditions hold | EXECUTE → verify (§7) → trace → re-observe → rediscover |
| **B** invalid / absent authority | the same divergence, with no envelope granting ADMIT (today's state) | REFUSE (escalate as absent authority); R unchanged; the divergence persists and is traced every cycle |
| **C** unknown / ambiguous authority | the envelope is expired, revoked, tampered, duplicated, or its citation does not resolve | STOP / ESCALATE; R unchanged |
| **D** invalid target | a proposal that would write `P13-015` or `P13-017`, **remove** or **close** an item, or write outside the register artifact | REFUSE (wrong target / action not granted); canonical sources untouched |
| **E** failed precondition | x's classification basis does not resolve; R fails its own history check (tampered); two sources classify x differently (conflict) | REFUSE; the conflict case ESCALATEs (canonical sources conflict: Founder/CEO) |
| **F** consequence mismatch | the frontier moves between observation and verification, or R' ≠ R ∪ {x} | no false success; re-observe, re-evaluate, rediscover (§7 table) |

The gate already refuses every Case C and D form generically, and that is
TEST-VERIFIED (`P13-019` `§7`, `§9`). What is missing is S11's own
preconditions and its own verification. Both are design work for after the
decision.

## 12. E13-05 vs E13-06 (Q10)

| Hazard | Does an S11 transition become it? | Why not |
|---|---|---|
| source-code self-modification | no | the register is data; the transition writes no code |
| architectural self-modification | no | the register is *named* by the architecture; realizing it is construction, separately authorized; a transition changes no architecture |
| capability self-expansion | no | tracking what is unresolved adds no capability; closing gaps (E13-06) is excluded |
| governance modification | no, **if condition 2 holds** | canonical classification stays in `P13-015`/`P13-017` and with the Founder/CEO; the register may not reclassify or close |
| authority synthesis | no | the register may hold no authority-bearing field and may not suppress escalations |
| uncontrolled evolution | no | one bounded transition per cycle, under an expiring envelope |

**What remains coupled.** The register is E13-07's owned object, so the
E13-05 proof would act on state that E13-07's *tracking* uses. **E13-07's exit
evidence must stay derived from the canonical sources and never from the
register** [PRO]. Otherwise an E13-05 action could move an E13-07 result.

## 13. Minimum meaningful state transition (Q7)

**One ADMIT of one real divergence, after the register exists.**

**Why this is the minimum:**

* **Bootstrap is not enough.** Establishing the register from nothing is a
  file creation (instruction `§18` item 12). It loses B4: every item is
  "expected" trivially. It also loses P6: there is no prior known/new
  distinction.
* **ANNOTATE depends on ADMIT.** It is only meaningful for an item already
  admitted, so it is not smaller.
* **A smaller write** (a timestamp, a counter, re-writing an unchanged item)
  loses the decision (P1) or the consequence (P4/P6).

**Live availability [MEA].** Across 5 live cycles the frontier has not moved,
and P13's own discoveries are not yet observable to it. A **live** ADMIT
therefore needs one of the following, whose timing is **[UNK]**:

* a genuine new frontier item, recorded canonically by the CEO or Founder;
* a genuine P13-detected gap, such as an R-GAP limitation or capability gap;
* the Founder's own decisions moving a classification.

A **test** can provide the divergence through a fixture world (§9) without
prescribing the action.

## 14. Remaining unknowns

| # | Unknown | Class |
|---|---|---|
| U1 | whether a P13-owned register of AIOS's frontier is beyond C1 | [UNK], Founder (Q-S1) |
| U2 | whether realizing the register falls under `D-1` | [UNK], Founder (Q-S3) |
| U3 | whether an append-only realization falls under ENV-01 item 3 | [UNK], Founder (Q-S4). Not argued |
| U4 | when live frontier movement will occur | [UNK], reality |
| U5 | how P13-discovered gaps that live only in prose (construction and reconciliation records) should enter the observable frontier: CEO recording in `P13-017`, or P13 observing them | [INS] |
| U6 | the P12 corpus-health work path writes its Trace under a certified root, which the barrier refuses. Whether that path is meant to run again in place, and where its live Trace belongs | [MEA] observation. The owner is P12, the decision the Founder's. Recorded, not acted on |

## 15. Founder-reserved questions

These are prepared here and not answered.

* **Q-S1 (semantic).** Does a P13-owned register *of AIOS's residual frontier*
  count as operational reality beyond P13's own existence, and so as a valid
  C2 proof surface? *If no:* **NO SUFFICIENT SEMANTIC PROOF SURFACE
  IDENTIFIED within C2.** E13-05 would then need a C3 decision (for example
  S3, corpus-health remediation, which is the most meaningful reality found)
  or an amendment of E13-05 as FDR-2 states it.
* **Q-S2 (canonicality).** Is it accepted that the register may never
  reclassify, close or remove frontier items, and that E13-07 stays derived
  from canonical sources?
* **Q-S3 (construction).** Is realizing the register within `P13-018` `D-1`,
  or separate?
* **Q-S4 (envelope).** Is any register transition within `P13-ENV-01` item 3
  if realized append-only, or is **new state-changing authority** required
  regardless? This report assumes nothing either way.
* **Q-S5 (live proof).** Is a TEST-VERIFIED Case A–F on a fixture world an
  acceptable interim, pending a live divergence (U4)? It would **not** count as
  LIVE-VERIFIED.

## 16. Recommendation for the next decision surface

This section identifies what comes next and decides none of it.

The next surface should be **controlled operational state definition** for S11
(instruction `§24`: *semantic discovery → controlled operational state
definition → minimum meaningful transition → minimum authority → Founder
decision surface → FDR-3*). It should put Q-S1 and Q-S2 **first**, because a
negative answer to either ends the S11 path. Only if both are affirmative
should it define:

* the register's item model;
* the ADMIT and ANNOTATE semantics;
* the preconditions;
* the verification;
* the Case A–F acceptance;
* the minimum authority (§10).

**No FDR-3 is drafted here, and no option is selected.**

---

## Decision readiness (instruction `§22`)

| | Answer |
|---|---|
| **A** operational reality | AIOS's residual frontier: what it knows to be unresolved and outside its completion contract, each item with its basis and status over time (S11) |
| **B** why P13 cares | FDR-2 `D08` and E13-07 require it to be classified and recorded; the Blueprint gives it to `Frontier`; today P13 cannot remember it across cycles [MEA] |
| **C** what state changes | the register gains one item (ADMIT), or annotates one (ANNOTATE); nothing else, and the canonical sources never change |
| **D** why it is meaningful | it changes what P13 concludes in every later cycle: new vs known, basis-changed detection (§6, §8) |
| **E** how P13 determines the action | from the divergence it observes between the register and the canonical frontier, by rule and priority; the harness never names the item (§9) |
| **F** how authority is checked | the existing gate (envelope resolution, target scope, preconditions, verification path, cycle bound), plus S11-specific preconditions (§11 E) |
| **G** how execution is verified | observe before and after over the register's boundary; changes ⊆ the target entry (`BoundedExecution` protocol, TEST-VERIFIED) |
| **H** how the consequence is verified | against §7's five expectations; mismatch handled per §7 |
| **I** how later observation changes | divergence reduced; x reported as known since N; basis tracked (§8) |
| **J** how rediscovery follows | the next divergence or basis change drives the next decision; frontier movement is re-examined, not assumed (§7, §8) |
| **K** minimum authority | §10: Founder-issued, one action class (ADMIT/ANNOTATE), one target, no remove/close/reclassify, reversible, expiring, one per cycle. **Not granted.** Whether any of it falls under existing authority is **UNKNOWN** (Q-S3, Q-S4) |
| **L** Founder-reserved | Q-S1 to Q-S5; the authority itself; FDR-3 |

**E13-05 remains LIMITED. P13 CERTIFICATION = NOT REQUESTED / NOT
AUTHORIZED.**
