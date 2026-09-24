# AIOS P13 — Canonical Blueprint v1.0 · Super Intelligence Ecosystem

| Field | Value |
|---|---|
| **Authority** | `FDR-2` (registered: Decision Register `§21`), which authorizes this canonicalization and pre-construction reconciliation (`D10`). V2 `A05`/`A06` for the architecture within `D09` |
| **Predecessors** | v0.1–v0.4 (preserved; v0.4 `00efeeae…` is the review basis under `FDR-1`) · `P13-015` · `P13-016` · `P13-017` |
| **Prepared by** | Claude Code — AIOS Co-Founder + Delegated CEO · 2026-09-24 |
| **Construction** | **NOT AUTHORIZED.** This Blueprint defines what a construction authorization would authorize. It authorizes nothing (`D10`, `GSI-10`) |
| **Construction decision (2026-09-24)** | `P13-018` — **APPROVED WITH BOUNDED INITIAL AUTHORITY** (`acts/P13-018-FOUNDER-CONSTRUCTION-AUTHORITY-GATE-DECISION.md`; Decision Register `§22`): `D-1` §10 IN authorized · `D-2b` envelope `P13-ENV-01` · `D-3` criteria read-only. The row above is this Blueprint as written. See §12 |

## 0. What is canonical here, and on what authority

| Layer | Status | Basis |
|---|---|---|
| Definition, meaning, mission, boundary, autonomy, relationships, exit contract, completion (§1–§2) | **CANONICAL** | quoted or converted from `FDR-2 D01`–`D09`; each contract cites its decision |
| Architecture, components, interfaces, authority mechanics, verification tests (§3–§11) | **CEO ARCHITECTURE DECISION** under `D09`/`D10`. Presented at the construction authority gate (`P13-018`) for the Founder to accept, amend or refuse | V2 `A05` (bounded architecture authority) · `A06` |
| Anything not traceable to either | **absent by design.** §9 maps every requirement to its source | — |

No v0.4 `PROPOSED` statement is carried forward on v0.4's authority
(`FDR-1 §6`). Where this Blueprint agrees with v0.4, the authority is `FDR-2`.

---

## 1. Canonical definition, meaning and mission

**Definition (`D01`, verbatim).** *P13 is the Super Intelligence Ecosystem layer
of AIOS in which AIOS develops the capability to understand its own relevant
system state, evaluate that state against defined criteria, reason over
evidence, determine appropriate next actions, and evolve its capabilities
within explicit governance and authority boundaries.*

**Not** (`D01`): a single Agent · a replacement for P1–P12 · a second AIOS ·
AGI · consciousness · omniscience · unlimited autonomy · unrestricted
self-modification.

**"Super Intelligence" (`D02`):** program identity and phase designation. **No
performance claim.** A future measurable intelligence claim needs its own
evaluation contract.

**Mission (`D03`), the operational spine:**

```text
WHAT STATE AM I IN? → IS THAT STATE GOOD? → WHAT SHOULD I DO NEXT?
   → AM I AUTHORIZED TO ACT? → WHAT HAPPENED? → WHAT SHOULD CHANGE?
answers: evidence-based · traceable · governed · refusable · authority-aware · verifiable
```

## 2. Canonical contracts: proposals converted

| ID | Contract | Source |
|---|---|---|
| **C-01 Semantic chain** | `OBSERVE → UNDERSTAND STATE → EVALUATE → REASON → DETERMINE/PROPOSE → AUTHORITY CHECK → EXECUTE IF AUTHORIZED → VERIFY → LEARN/EVOLVE → RE-DISCOVER`. *"The semantic chain is the architectural contract."* Every component in §3 is one link, and no link may be skipped | `D01` |
| **C-02 Autonomy** | Bounded Delegated Autonomy: execute **only** where an existing valid authority already permits the action. Otherwise escalate, refuse, or return UNKNOWN. `GSI-01…10` hold | `D05`, `§7` |
| **C-03 Relationships** | Build only relationships an evidenced requirement needs. The primary new one is **Memory ↔ Intelligence**, with no ownership transfer | `D06` |
| **C-04 Boundary** | Consume, extend, compose, evaluate or govern P1–P12. Never duplicate, reopen or redefine them. `NATIVE CORE = 11` | `D04`, `D09` |
| **C-05 Exit** | `E13-01`…`E13-07`, subject to *no unresolved blocking requirement + no unauthorized boundary crossing + no false completion claim* | `D07` |
| **C-06 Completion** | Bounded. `EXHAUSTED` or `EXHAUSTED_WITH_CLASSIFIED_REMAINDER` are valid terminal states. A residual frontier may remain | `D08` |

---

## 3. Architecture

### 3.1 Placement

```text
NATIVE CORE (11 boundaries, frozen, unchanged)
   ▲  read-only interfaces
TOOLS LAYER ── P1–P12 tools (P12 self-model, operational state, integrity, registers)
   ▲  read-only interfaces
tools/p13/      ← the P13 ecosystem layer (new package; the only code P13 owns)
docs/operations/p13/   ← P13 live records and Trace store (live root; never certified)
docs/architecture/p13/ ← P13 canonical documents (this Blueprint)
```

**Why the tools layer** [OBS]. It is what `D09` names (*"TOOLS / ECOSYSTEM /
APPROPRIATE EXISTING BOUNDARY"*). It is where every P12 capability P13
consumes already lives. And the P13-CORE questions need no new Native Core
contract: `P13-016 §1` shows all 21 map onto composition over existing
boundaries. **No twelfth boundary** (`GSI-08`).

**Region rules, inherited and binding.** `tools/` imports nothing from
`consumers/` (`consumers/tests/test_reference_agent.py`). Native Core is
imported read-side only. No file under `native_core/` changes.

### 3.2 Components: one per link of C-01

| Component | Link | Owns | Consumes (read-only) | Emits |
|---|---|---|---|---|
| `StateUnderstanding` | OBSERVE / UNDERSTAND | the `StateSnapshot` type | P12 self-model (12 answers), operational state, certified-evidence integrity, escalation register, **Memory via `MemoryReader`** | `StateSnapshot`: facts, each with source, status (`VERIFIED`/`INFERRED`/`UNKNOWN`) and observed-at |
| `Evaluation` | EVALUATE | `Criterion`, `EvaluationResult` | a snapshot; criteria, each carrying an `AuthorityProvenance` to its instrument | `PASS` / `FAIL` / `UNKNOWN`, with evidence and uncertainty. **Insufficient evidence → UNKNOWN, never PASS** |
| `Reasoning` | REASON | `Rule`, `Conclusion` | facts and evaluations | conclusions naming their premises and rule. **No premise, no conclusion** |
| `NextAction` | DETERMINE / PROPOSE | `ActionType`, `ActionProposal` | conclusions; the `ActionCatalog` | proposals, typed as proposals. There is no method that makes one an authorization |
| `AuthorityGate` | AUTHORITY CHECK | `GateDecision` | the proposal; authority envelopes (§5) | `EXECUTE(envelope)` / `ESCALATE` / `REFUSE` / `UNKNOWN` |
| `BoundedExecution` | EXECUTE IF AUTHORIZED / VERIFY | `Outcome` | an `EXECUTE` decision; the executor the `ActionType` declares (existing resident executors only) | outcome, plus a re-assembled snapshot and re-evaluation as verification |
| `Evolution` | LEARN / EVOLVE | `Gap`, `EvolutionProposal` | failed or unknown evaluations; open escalations; the `P13-015` matrix's CORE/PARTIAL rows | evolution **proposals**, routed through `AuthorityGate` like any action |
| `Frontier` | RE-DISCOVER / exhaustion | the residual frontier register | every prior output | exhaustion assessment (`EXHAUSTED…`) and the classified remainder |

A **cycle** is one invocation of the chain. It is bounded: at most one
executed action per cycle, a stop on no progress (the same state digest twice),
and no self-scheduling (`GAP-0019`; F6 `NC-ACE-013`).

### 3.3 Invocation

```text
human or CEO (under a Goal) → tools/p13 cycle entry point → one bounded cycle → records
```

No daemon, scheduler, queue, background thread or self-activation (standing
constraint; `D05` *"silence is never approval"*). **P13 runs when it is run.**

### 3.4 Technology neutrality

Reasoning and evaluation are **deterministic rule applications over typed
evidence**. The frozen architecture's `§6.2` invariant 1 (recorded as V2
constraint `C-4`, and applied by the P5 consumers) excludes a technology,
language, framework, model or vendor decision. The Implementation
Constitution's principle 8 (*Tool Boundary*) confines any external
dependency to the Tool boundary. A model-based reasoner would need both, and
it is outside this Blueprint (§10).

### 3.5 Implementation Constitution principles, binding on every component

| Principle | Consequence for P13 |
|---|---|
| 2 **Governance First** | P13 may propose; it never overrides governance (`GSI-01`) |
| 4 **Memory Never Self-Promote** | P13 reads Memory. It never promotes Memory to Knowledge; promotion stays governed human review |
| 5 **Knowledge Is Governed** | P13 never admits or edits Knowledge |
| 7 **Fail Closed** | uncertain conformance or authority → no execution (§5.2) |
| 8 **Tool Boundary** | no external dependency outside the Tool boundary |
| 9 **Immutable Trace** | P13's Trace is append-only, written at action time |

---

## 4. Integration map: requirement-driven (`D06`)

| Relationship | Requirement that proves it | Interface | Owner stays | Status now |
|---|---|---|---|---|
| **Memory → P13** (primary, `D06`) | E13-01 (*"relevant … state"*), E13-03 (reason over history), E13-06 (gaps) | `native_core.core.memory.reader.MemoryReader(trace_reader).read()`: retained Memory derived from Trace; **read-only** | P7 | **NOT CONNECTED** (measured) → the one new relationship to build |
| P12 self-model / operational state → P13 | E13-01 | `tools.p12_self_model.self_model()`, `tools.p12_operational_state.project()` | P12 | consumed |
| Certified-evidence integrity → P13 | E13-02 (a criterion with a Founder-issued basis), E13-06 non-regression | `tools.certified_evidence_integrity.verify()` | GOAL-V2-004 | consumed |
| Escalation register ↔ P13 | E13-05 (*"escalate reserved/ambiguous action"*), E13-06 | `EscalationRegister.record` / `open_escalations` (**write only through its existing `record`**) | P11 | consumed |
| Delegations → P13 | E13-05 (the authority check reads envelopes) | `tools.delegation_catalog.read_delegations`, W4 grants; `tools.authority_citation.refusal` | P11 / governance | consumed |
| Trace ← P13 | E13-01/05/06 trace model (§6) | `native_core.core.trace.TraceWriter` over a **P13-owned live store** | P3 | consumed |
| **Knowledge → P13** (conditional) | E13-02, **only if** a ratified criterion is admitted Knowledge (e.g. `FD-P12-002`'s corpus-health criteria, read the way `aios_corpus_health_run._active_criteria` reads them) | `knowledge.retrieval.active(key)`, read-only | P6 | **required only if the Founder includes that criterion** (gate decision) |
| Workflow, Tool, Agent, Organization (beyond delegations), Runtime | no E13 criterion requires them | — | — | **not built** (`D06`) |
| Optimization → Governance (`AD-P13-001`) | none. Evaluation reaches governance through the escalation register | — | Architect | **not needed; stays reserved** |

---

## 5. Authority & autonomy contract (`D05` → technical behaviour; `P13-PRE-03`)

### 5.1 Authority envelopes: the only source of "may execute"

An **envelope** is an existing, recorded, resolvable authority. It names the
action types it permits, and it cites an instrument that
`tools/authority_citation.refusal` resolves. P13 recognises exactly two kinds:

1. **W4 delegation grants** (`FD-P11-001`), for an action whose type matches
   the grant's `work_scope` and `capability_scope`;
2. **P13 action envelopes**: entries in the Delegation Register issued by an
   authority that holds the power delegated (the Founder, or the CEO under
   `A10`, never beyond its own). Each names its permitted action types.

**Today no P13 action envelope exists.** Under this contract, a constructed P13
could execute nothing on day one: every proposal would `ESCALATE`. That is
C-02 failing closed. It is not a defect. The initial envelope, if any, is a
decision at the construction authority gate (`P13-018` item 8).

### 5.2 The gate's decision table

| Condition (evaluated in this order) | Decision |
|---|---|
| the action type is not in the `ActionCatalog` | `REFUSE` (unknown action) |
| the action type is **reserved**: code change, governance or certified-evidence change, delegation issuance, knowledge admission, Native Core, Constitution | `ESCALATE` to Founder / CEO. **Never executable by P13** |
| the proposal's premises contain `UNKNOWN` | `UNKNOWN` → discover (`D05`: insufficient evidence) |
| no envelope permits it, or the envelope's citation does not resolve | `ESCALATE` (authority absent or uncertain) |
| two envelopes conflict | `ESCALATE` (governance conflict) |
| exactly one envelope permits it, and the citation resolves | `EXECUTE(envelope)` |

**Type-level separation** (`E13-04`, `GSI-02`). An `ActionProposal` has no
authorization field. Only `AuthorityGate` produces a `GateDecision`, and only
from an envelope. Nothing reads *"P13 believes it is necessary"* as authority.

### 5.3 Refusal and escalation

Refusal is typed, durable and recorded (§6). Escalation goes through
`EscalationRegister.record`, the existing path, and a human answers through
`record_response(HumanAuthority)` (Constitution `§6.2` inv. 2). A response
recorded as `ANSWERED` never becomes `APPROVED`.

---

## 6. Evidence & trace model

Every P13 output (snapshot, evaluation, conclusion, proposal, gate decision,
outcome, gap, exhaustion assessment) is a record under `docs/operations/p13/`.
It carries the twelve P12 `§29` preservation elements:

| `§29` element | P13 field |
|---|---|
| intent · decision · work | cycle intent · `GateDecision` · the action |
| actor · authority · scope | invoker (human/CEO) · envelope + resolved citation · action type and targets |
| execution · observation | executor and outcome · snapshot before and after |
| verification · evidence · provenance · lifecycle | re-evaluation · source facts · premise chain · record state |

Records are **append-only** and live; certified roots are never written (the
GOAL-V2-004 barrier refuses it regardless). Trace records go to a P13-owned
store under `docs/operations/p13/trace`, which is also how P13's own history
becomes Memory, through the same `MemoryReader`.

---

## 7. Verification contract (`D07` → measurable; `P13-PRE-04`)

Every criterion is verified **live on real system state**, with fixtures as
supplementary evidence only (P12 `§46`), and has a negative control that
*would* fail.

| Criterion | Acceptance (all must hold) | Negative controls |
|---|---|---|
| **E13-01** State understanding | a snapshot covers the 12 self-model questions, integrity, open escalations and **Memory**. Every fact has source, status and time. A removed source yields `UNKNOWN` for its facts, not omission | remove the Memory source → facts `UNKNOWN`; forge a fact without a source → rejected |
| **E13-02** Evaluation | each criterion cites a resolving authority and yields PASS/FAIL/UNKNOWN with evidence. Missing evidence gives UNKNOWN | a criterion without authority → refused; evidence removed → UNKNOWN, not PASS |
| **E13-03** Reasoning | every conclusion lists its premises and rule; each premise resolves to a fact or an evaluation in the same cycle | a premise-less conclusion → rejected; a premise naming a nonexistent fact → rejected |
| **E13-04** Next action | proposals are typed, derived from conclusions, and carry no authorization | attempt to execute a proposal directly → impossible by type; a recommendation presented as a decision → refused |
| **E13-05** Bounded execution | the §5.2 table is enforced: an authorized action executes via its declared executor with a recorded outcome, and a reserved or unknown one never executes | no envelope → ESCALATE; forged citation (GOAL-V2-005 pattern) → ESCALATE; a reserved type inside an envelope → ESCALATE; a second action in one cycle → refused |
| **E13-06** Evolution & re-discovery | gaps derive from failed or unknown evaluations; evolution proposals pass the gate; after an executed action the snapshot and evaluations are re-derived and the difference is recorded | an evolution proposal targeting code or governance → ESCALATE, never executed |
| **E13-07** Exhaustion & frontier | the P13 scope (the 21 CORE questions, mapped in §9) is each either verified-answered or classified in the residual frontier; `tools/foundational_question_reconciliation.py` holds with 0 P13 CORE rows unclassified | a CORE row with no evidence → the checker fails |

**Non-regression, held throughout:** the certified P10/P11/P12 manifests hold;
`NATIVE CORE = 11`; the write probe shows 0 certified writes; every suite is
green; no daemon, scheduler or thread is introduced (a static test).

---

## 8. Architect- and Founder-reserved matters, reconciled (`FDR-2 §8`)

| Matter | Reconciliation |
|---|---|
| `AD-P13-001` Optimization → Governance | **Not needed.** Evaluation reaches governance through the escalation register (§4). Stays Architect-reserved, and non-blocking |
| `AD-P13-002` / `ADR-0029` cross-PD interfaces | **Not touched.** P13 defines no cross-PD interface |
| `GAP-0009` Agent lifecycle canon | **Not needed.** P13 places nothing in the Agent contract (`D01`: *"not a single Agent"*) |
| `GAP-0006` corpus residency | **Not needed.** Every requirement's canonical source is `FDR-2` (§9) |
| `FD-2` Founder ≡ Architect | **Not relied on.** The one architecture choice with Architect flavour, placement, was made by the Founder in `D09` |
| Initial P13 action envelope | **Founder / CEO decision at the gate** (§5.1) |

## 9. Traceability map (closes `GAP-0026`)

| Requirement | Canonical source | Component | Criterion | P13-CORE questions answered |
|---|---|---|---|---|
| understand relevant state | `D01`, `D03` q1 | `StateUnderstanding` | E13-01 | Q17, Q61, Q62, Q63 |
| evaluate against defined criteria | `D01`, `D03` q2 | `Evaluation` | E13-02 | Q33, Q38, Q40, Q46, Q53 |
| reason over evidence | `D01` | `Reasoning` | E13-03 | Q28, Q57, Q59 |
| determine next action | `D01`, `D03` q3 | `NextAction` | E13-04 | Q19, Q41, Q69–Q73, Q89 |
| act within authority | `D05`, `D03` q4–5 | `AuthorityGate`, `BoundedExecution` | E13-05 | (Q48, Q74, Q75, Q77, Q90, Q92 resolved by `D05`) |
| evolve | `D01`, `D03` q6 | `Evolution` | E13-06 | Q27 |
| bounded completion | `D07`, `D08` | `Frontier` | E13-07 | Q94–Q97, Q99 (resolved by `D07`/`D08`) |

## 10. Construction scope (for the gate)

```text
IN        tools/p13/ (the eight components) · one cycle entry point ·
          docs/operations/p13/ (live records, P13 Trace store) · tests ·
          the Memory → P13 read path · a static no-scheduler test
OUT       any file under native_core/ · any consumers/ import · any P1–P12
          behaviour change (read-only use only) · certified-evidence writes ·
          new delegation issuance by P13 · knowledge admission by P13 ·
          model / vendor / technology decisions · daemon, scheduler, queue,
          thread · Optimization → Governance · a twelfth boundary
```

## 11. Certification path and rollback

**Certification** (after E13 is met; separately authorized, as with
`FD-P12-006`): Founder certification decision. Then `docs/architecture/p13/`
becomes a certified root, protected by the guard's default phase root. A P13
content manifest is added to the index, on the GOAL-V2-004 model.

**Rollback / recovery.** P13 writes only `tools/p13/`,
`docs/operations/p13/` and its own documents. Removing the package restores
pre-P13 behaviour exactly, because no P1–P12 code depends on it. An executed
action's effects are those of an existing executor, recorded with an outcome.
Reversal goes through that executor's own lifecycle (a W4 grant revoked, a
record superseded) and never through deletion. Certified evidence cannot be
harmed: the barrier refuses the write.

---

## 12. After the construction gate (added 2026-09-24; §0–§11 unchanged)

`P13-018` (Founder — Moriarty; Decision Register `§22`) decided the gate:
**APPROVED WITH BOUNDED INITIAL AUTHORITY**. Three statements above were true when
written and are superseded by that decision. They are left in place, as
written:

| Where | As written | Since `P13-018` |
|---|---|---|
| header, §5.1 | construction not authorized; *"Today no P13 action envelope exists"* | construction of §10 IN is authorized. `P13-ENV-01` (evidence-only, **initial, not maximum**) is recorded in the Delegation Register `§14` and `docs/governance/p13-envelopes/P13-ENV-01.json` |
| §4 | Memory → P13 **NOT CONNECTED**; Knowledge → P13 conditional | Memory → P13 is built (`tools/p13/state.py`, `MemoryReader`), and `tools/ecosystem_relationships.py` measures Memory ↔ Intelligence as CODE. Knowledge → P13 is required and read-only (`D-3`) |
| §8 last row | initial envelope is a gate decision | decided: `D-2b` |

**What is not changed:** certification is not granted, P13 completion is not
claimed, full autonomy is not authorized, and `NATIVE CORE = 11`. The
construction and its verification are recorded in
`docs/governance/AIOS_P13_CONSTRUCTION_RECORD_v1.0.md`.


## 13. After the post-construction reconciliation (added 2026-09-24; §0–§12 unchanged)

The reconciliation instruction
(`acts/P13-POST-CONSTRUCTION-RECONCILIATION-AND-E13-05-EXIT-BLOCKER-INSTRUCTION.md`)
asked for the E13-05 boundary to be made testable. Five additions to §5.2's
table follow from it. **Every one only refuses:**

* envelope anomalies EXPIRED and AMBIGUOUS;
* a target outside the envelope's declared scope;
* a state-changing type with no declared scope;
* a missing verification path;
* a failing precondition.

`BoundedExecution` gains §8.5's verification protocol for state-changing
types: observe the boundary, execute, observe again, compare against the
authorized targets, check the postcondition, then re-observe from scratch.
That protocol is **TEST-VERIFIED only**. No envelope grants a state-changing
type, and the production catalog has no executable one. The Founder decision
surface is `docs/architecture/p13-preparation/P13-019-E13-05-STATE-CHANGING-AUTHORITY-DECISION-SURFACE.md`,
and the record is `docs/governance/AIOS_P13_POST_CONSTRUCTION_RECONCILIATION_RECORD_v1.0.md`.

## 14. E13-05 consequence mechanism (added 2026-09-24; §0–§13 unchanged)

This follows the bounded-operational-state instruction
(`acts/P13-E13-05-BOUNDED-OPERATIONAL-STATE-PROOF-SURFACE-INSTRUCTION.md`).

**Proposals carry an expected consequence**, fixed before the gate:

* the gate refuses a state change that has none;
* the cycle compares expected against actual after re-evaluation;
* a mismatch is never a success, and the remedy goes to review
  (`review.consequence`, reserved) instead of being retried.

**Decision provenance is checked from evidence.** Every EXECUTE must trace, in
its own record, to premises P13 observed.

**No production state-changing action exists**, and no envelope grants one.
The operational surface is a Founder decision:
`docs/architecture/p13-preparation/P13-E13-05-OPERATIONAL-SURFACE-FOUNDER-DECISION-PACKAGE.md`.

## 15. Post-FDR-3 reconciliation (added 2026-09-24 under `FDR-4` `FD-C`; §0–§14 unchanged)

`FDR-4` (Founder — Moriarty; Decision Register `§24`) authorizes this
append-only note. §13 and §14 stay **as written**. They were correct when
written, before any state-changing authority existed. This note records what
followed. It does not revise them.

| Where | As written | Since `FDR-3` and `FDR-4` |
|---|---|---|
| §13 | *"No envelope grants a state-changing type, and the production catalog has no executable one"* | `FDR-3` (`§23`) authorized a dedicated, bounded S-OPS proof surface. `P13-ENV-02` (Delegation Register `§15`) granted `s_ops.open` / `s_ops.close` on `docs/operations/s-ops/S-OPS-01.json` only. §13's verification protocol then ran **live** |
| §14 | *"**No production state-changing action exists**, and no envelope grants one"* | the production catalog holds the two S-OPS transitions. `P13-ENV-02` granted them for the E13-05 proof alone, and is now **spent / retired / revoked** under `FDR-4` `FD-B` (Delegation Register `§16`). **No envelope grants a state-changing type today** |

**E13-05: VERIFIED.** The live proof is recorded in
`docs/governance/AIOS_P13_E13_05_S_OPS_LIVE_PROOF_RECORD_v1.0.md`:

* P13 decided from observed state;
* authority was checked against `P13-ENV-02`;
* a real state change was executed;
* the expected and actual consequences matched;
* the evidence and Trace were recorded;
* re-observation and rediscovery followed, and so did the reversal.

`FDR-4` `FD-A` holds that a live ESCALATE is not required for E13-05. The
escalate branch is test-proven.

**What did not change:**

* no general or production write authority was granted;
* no P1–P12 or P11 ownership changed;
* §5's authority contract and §7's verification contract stand as written;
* the S-OPS surface is a historical proof surface, not a P13 component.

**Status:** P13 is **EXIT-READY** (`FDR-4` `FD-D`), which is not exit contract
satisfied, not certified, and not Phase 13 closed. The Founder decides the exit
gate.
