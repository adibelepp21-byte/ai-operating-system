# AIOS Finding Register

**Status:** Permanent · Append-only
**Version:** v1.0
**Established:** 2026-08-06
**Authority Disclaimer:** This register **records** findings and the
classifications and dispositions an authority has assigned to them; it does not
classify, dispose, resolve, or repair anything on its own account, and it
carries no independent governance authority. Every entry is a record of an
observation made under an authorized baseline and of the decision an authority
took on it. Where anything here appears to conflict with the Engineering
Constitution or the Canonical Domain Model, those documents govern.

---

## 1. Purpose

This register is the repository's permanent record of **findings** — the
observations, limitations, and gaps surfaced during the Native Core Conformance
program (Baselines 01, 02, 04A, 04B, 04C) — together with the classification
and disposition each received.

It exists because those findings were, until this record, held in three
inconsistent places:

- three findings were embedded durably in transported test source
  (`F-2`, `F-3`, `F-4`);
- the remainder existed **only in implementation reports and session
  conversation**, and would not survive the loss of that context;
- the repository already contained *unrelated* observations carrying the same
  short labels, so the labels alone were ambiguous.

It follows the repository's established convention for permanent append-only
records (`AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md`,
`AIOS_PRINCIPLES_REGISTER_v1.0.md`,
`KNOWLEDGE_ADMISSION_BLOCKER_REGISTER_v1.0.md`).

---

## 2. Scope and Maintenance

### 2.1 What is recorded here

Findings raised under an authorized baseline: architectural observations,
verification limitations, reserved-decision notes, and governance record gaps —
each with its classification, its disposition, and the authority that assigned
them.

### 2.2 What is recorded elsewhere

- **Governance decisions** → `AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md`. This
  register never substitutes for a governance decision record; where a finding
  was disposed of by an Architect decision, this register cites that decision
  rather than restating its authority.
- **Architectural Tier decisions** → `docs/architecture/adr/decisions/`.
- **Baseline completion status** → `AIOS_NATIVE_CORE_CLOSEOUT_v1.0.md`.

### 2.3 Identifiers and the historical-label rule

Entries use the `P7-` namespace, assigned on entry:

| Prefix | Meaning |
|---|---|
| `P7-F-n` | Finding — an observation about the implementation or its documentation |
| `P7-O-n` | Reserved Observation — concerns an `[O]` item reserved to the Architect |
| `P7-L-n` | Coverage Limitation — something verification could not reach, by architectural reservation |
| `P7-G-n` | Governance Record Gap — a decision or artifact that is not durably recorded |

**The namespace is new; the historical labels are not changed.** Source files
frozen and transported under Baselines 04A, 04B, and 04C carry the bare labels
`F-2`, `F-3`, `F-4` in their docstrings. Those files are frozen: they are not
amended, re-labelled, or rewritten by this register. Every entry below instead
carries an explicit **cross-reference** to its historical label and to the file
that holds it.

This rule exists because the repository already contains unrelated
observations using the same short labels — see **P7-G-2**.

### 2.4 Maintenance rules

- **Append-only.** Entries are added, never rewritten. A superseded entry is
  marked superseded and retained in place; its text is not altered.
- **Recording only.** Recording a finding here neither repairs it nor
  authorizes its repair. No entry in this register may be read as permission to
  modify source, API, exports, or documentation.
- **Evidence discipline.** Every entry states where the finding can be observed
  — a file and line, a command, or a named session artifact — so a later reader
  can re-derive it rather than take this record on trust.
- **Honest provenance.** Where a finding's originating text is not available in
  the recording session, the entry says so plainly rather than paraphrasing it
  into the record.

---

## 3. Classification Model

The classifications below are the ones the Architect applied during the
program. They are recorded, not invented here.

| Classification | Meaning | Consequence |
|---|---|---|
| **Category A** | Invariant violation, frozen-entity modification, boundary expansion, governance violation, unauthorized dependency, ADR contradiction, or constitutional conflict | Requires manual Architect inspection; blocks acceptance |
| **Category B — Recorded Evidence** | A real observation that violates no invariant and blocks no gate | Recorded only; repair requires a separate authorization |
| **Category C — Governance Status Drift** | Documentation asserts a status the implementation no longer has | Recorded; correction is documentation synchronization, separately authorized |
| **Coverage Limitation** | Verification could not reach a requirement because the architecture reserves it | Not a defect; recorded and carried forward |
| **Reserved Observation** | Concerns an `[O]` item reserved to the Architect | Record-only; must not be resolved by engineering |
| **Governance Record Gap** | A decision or artifact whose durability is incomplete | Recorded; closing it requires a separate authorization |

---

## 4. Register Entries

---

### P7-F-1 — Knowledge boundary documentation asserts a dependency status the source contradicts

| Field | Value |
|---|---|
| **Identifier** | P7-F-1 |
| **Historical label** | `F-1` |
| **Boundary** | Knowledge (L8) |
| **Raised under** | Baseline 04A — Knowledge Conformance, Stage 2 |
| **Classification** | **Category C — Governance Status Drift** |
| **Assigned by** | Architect, P7-I11 — *F-1 Governance Resolution & Baseline 04A Continuation Authorization* |
| **Disposition** | Governance question resolved; **documentation synchronization remains open** and separately authorizable |
| **Durability before this register** | Session conversation only |

**Observation.** `native_core/core/knowledge/__init__.py:23` states that the
boundary *"imports none of its permitted future dependencies"*. The source
contradicts this: the boundary imports Governance, Memory, and an
Infrastructure storage facility.

**Evidence.** `native_core/core/knowledge/__init__.py:23`; the Baseline 04A
dependency sweep, reproduced by the conformance suite's cross-boundary import
test.

**Root-cause classification.** Case C — Governance Status Drift. Case B
(unauthorized import) was ruled out: the imports arrived through one authorized
commit with per-phase certification. Case D (terminology ambiguity) was ruled
out: no reading of "permitted future dependencies" rescues the claim
*"imports none"* when three such imports exist.

**Not authorized under any baseline to date:** editing the docstring or the
Knowledge README.

---

### P7-F-2 — Five Knowledge halt sites pass a non-string argument

| Field | Value |
|---|---|
| **Identifier** | P7-F-2 |
| **Historical label** | `F-2` |
| **Boundary** | Knowledge (L8) |
| **Raised under** | Baseline 04A — Knowledge Conformance, Stage 2 |
| **Classification** | **Category B — Recorded Evidence** |
| **Assigned by** | Architect, P7-I12 — Baseline 04A Stage 4 Acceptance |
| **Disposition** | Recorded only. Repair not authorized. |
| **Durability before this register** | **Durable in source** |

**Observation.** Five raise sites pass a list rather than a string to
`KnowledgeError`, so a halt reaches an operator as a structured object needing
interpretation rather than as a message.

**Evidence.** `admission.py:86`, `admission.py:88`, `repository.py:95`,
`repository.py:97`, `retrieval.py:64` — recorded in
`native_core/core/knowledge/tests/test_knowledge_conformance.py` as
`TestPr4FailClosed.test_halt_messages_are_strings`, marked
`@unittest.expectedFailure`.

**Standing effect.** This is the repository's **sole expected failure**. It is
reported by every full-suite run without blocking the green-suite gate. Should
the source be corrected under a future authorization, the test becomes an
*unexpected success* — which fails the suite and forces the record to be
revisited deliberately.

---

### P7-F-3 — Agent data contracts are absent from the boundary's public surface

| Field | Value |
|---|---|
| **Identifier** | P7-F-3 |
| **Historical label** | `F-3` |
| **Boundary** | Agent (L3) |
| **Raised under** | Baseline 04C — Agent Conformance, Stage 2 |
| **Classification** | **Category B — Recorded Evidence** |
| **Assigned by** | Architect, P7-I21 — Baseline 04C Stage 4 Acceptance |
| **Disposition** | Recorded only. Export change, API expansion, and documentation synchronization all explicitly **not** authorized. |
| **Durability before this register** | **Durable in source** |

**Observation.** The Agent package declares `Public surface: agent: Agent` and
exports `Agent` alone, while `definition.py` and `instance.py` define four
further public names reachable only through their own modules.

**Evidence.**

```
agent.__all__ = ['Agent']
hasattr(agent, 'AgentDefinition')        -> False
hasattr(agent, 'AgentInstance')          -> False
hasattr(agent, 'InvalidAgentDefinition') -> False
hasattr(agent, 'InvalidAgentInstance')   -> False
```

Recorded in `native_core/core/agent/tests/test_agent_conformance.py` as
`TestPublicApiSurface.test_recorded_finding_f3_the_data_contracts_are_off_the_public_surface`,
which asserts the state **as found** and passes.

**Verified non-violation.** P7-I21 confirms the finding violates none of INV-3,
INV-4, INV-12, INV-13, or PR-4. No specification requires these exports.

**Reserved future handling** (P7-I21, recorded as stated): acceptance without
change · documentation synchronization · a dedicated Agent maintenance baseline
· permanent acceptance as intentional design.

---

### P7-F-4 — The Execution consumer contract is absent from its package's public surface

| Field | Value |
|---|---|
| **Identifier** | P7-F-4 |
| **Historical label** | `F-4` |
| **Boundary** | Runtime (L2), Execution layer |
| **Raised under** | Baseline 04B — Runtime Conformance, Stage 2 |
| **Classification** | **Category B — Recorded Evidence** |
| **Assigned by** | Architect, P7-I16 — Baseline 04B Stage 3, reaffirmed at P7-I17 |
| **Disposition** | Recorded only. Export change and API modification **not** authorized. |
| **Durability before this register** | **Durable in source** |

**Observation.** `consumer.py` declares `ExecutionConsumer` to be *"the
canonical consumer boundary: the single interface every future execution
consumer implements"*, yet the Execution package's public surface — its
`__all__` and its docstring's *Public surface* list — omits it. The contract is
reachable only as
`native_core.core.runtime.execution.consumer.ExecutionConsumer`.

**Evidence.**

```
execution.__all__ = ['Execution', 'ExecutionSession', 'ExecutionContext',
                     'create_execution_layer', 'ExecutionError',
                     'InvalidExecutionConfiguration']
hasattr(execution, 'ExecutionConsumer') -> False
```

Recorded in `native_core/core/runtime/tests/test_runtime_conformance.py` as
`TestExecutionLayerStructure.test_recorded_finding_f4_consumer_contract_is_off_the_public_surface`.

**Verified non-violation.** P7-I16 confirms the finding violates none of INV-3,
INV-4, INV-12, INV-13, or OQ-2.

---

### P7-L-1 — INV-2 is not verifiable while the Agent Factory is reserved

| Field | Value |
|---|---|
| **Identifier** | P7-L-1 |
| **Historical label** | *INV-2 coverage limitation* |
| **Boundary** | Agent (L3) |
| **Raised under** | Baseline 04C — Agent Conformance, Stage 2 |
| **Classification** | **Coverage Limitation — Reserved Architecture** |
| **Assigned by** | Architect, P7-I21 — *"This is not classified as a defect… The absence is accepted as an architectural reservation."* |
| **Disposition** | Carried forward. Creating an Agent Factory, bootstrap path, Department binding, or Capability binding is explicitly **not** authorized. |
| **Durability before this register** | Session conversation only |

**Observation.** INV-2 — *an Agent Definition is owned by exactly one
Department and implements at least one Capability* — cannot be verified at the
Agent boundary, because neither binding is modelled. `agent_spec §12/§13` place
governed construction of Definitions and Instances (the *Agent Factory*) in
Phase 4, **[O] reserved to the Architect**.

**Evidence that the reservation is intact, not merely unimplemented.** Baseline
04C verified structurally: no `composition.py`, no `bootstrap.py`, **zero
module-level functions anywhere in the boundary**, and no factory, registry,
ownership, or capability identifier. The absence is a reservation being
honoured, not an omission.

**Consequence recorded.** Native Core conformance coverage is complete for
every invariant that the built architecture can express. INV-2 remains
unverifiable until the reserved phase supplies the bindings.

---

### P7-O-1 — The Runtime lifecycle state model is `[O]`-reserved yet exercised

| Field | Value |
|---|---|
| **Identifier** | P7-O-1 |
| **Historical label** | `O-1` (this program's sense — see P7-G-2) |
| **Boundary** | Runtime (L2) |
| **Raised under** | Baseline 04B — Runtime Conformance, Stage 2 |
| **Classification** | **Reserved Observation** |
| **Assigned by** | Architect, P7-I15 — *"Observation O-1 remains **record-only**. It shall not be resolved, modified, or interpreted during this baseline."* |
| **Disposition** | Record-only. Not resolved, not interpreted. |
| **Durability before this register** | Session conversation only |

**Observation.** Native Core Blueprint §6 and `runtime_spec §12/§14` reserve the
Runtime lifecycle state model to the Architect as an `[O]` item. The Phase 4.0
directive exercised that reservation and fixed the states
`CREATED → INITIALIZED → RUNNING → STOPPING → STOPPED`. The reservation and the
exercised decision coexist in the record.

**Treatment under Baseline 04B.** The conformance suite verifies the state model
**as implemented** — its determinism, completeness, terminality, and fail-closed
refusal — and states explicitly, in both the test package docstring and the
governing test class, that it *"neither ratifies nor questions the
reservation."*

---

### P7-O-2 — Roadmap §9 priority order is superseded by the certified build sequence

| Field | Value |
|---|---|
| **Identifier** | P7-O-2 |
| **Historical label** | `O-2` |
| **Boundary** | Program-level (Roadmap) |
| **Raised under** | Baseline 04A — Knowledge Conformance, Stage 2 |
| **Classification** | **Reserved Observation** |
| **Assigned by** | Recorded as evidence; no Architect disposition issued to date |
| **Disposition** | Open. Roadmap synchronization has never been authorized under any baseline. |
| **Durability before this register** | Session conversation only |

**Observation.** `AIOS_NATIVE_CORE_IMPLEMENTATION_ROADMAP_v1.0.md §9` assigns
each boundary a build **Priority** (Infrastructure 1 … Runtime 10,
Optimization 11). The certified Phase 4 sequence (GDR-0002) built Runtime and
Agent as sub-phases 4.0–4.6, ahead of several boundaries the Roadmap ranks
earlier. The Roadmap's priority column therefore no longer describes the
sequence actually followed and certified.

**Consequence.** None architectural. The observation matters only as a
documentation-accuracy question, and correcting it is roadmap synchronization —
which no baseline has authorized.

---

### P7-G-1 — Governance decisions from P7-I1 … P7-I15 are not durably recorded

| Field | Value |
|---|---|
| **Identifier** | P7-G-1 |
| **Classification** | **Governance Record Gap** |
| **Raised under** | Baseline 05 — Native Core Governance Closeout, Stage 2 |
| **Disposition** | Recorded. Closing it requires the Architect to supply the original directive text. |

**Observation.** The Native Core Conformance program was governed by a
directive series `P7-I1` … `P7-I22`. Only the decisions from **P7-I16 onward**
were available verbatim in the closeout session; the text of `P7-I1` … `P7-I15`
was not, and neither was `P5-I1N-A`.

**Why this matters here.** `AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md §2.3`
imposes **verbatim discipline**: *"A decision's text is recorded as the deciding
authority stated it, without reinterpretation, substitution, or paraphrase."*
Recording those earlier decisions from summary would have violated that rule.
They are therefore **not** recorded as register entries, and this gap is
recorded instead.

**Decisions known to be affected** (identified by directive, described only
by subject, not by paraphrased decision text):

| Directive | Subject |
|---|---|
| P7-I2 / P7-I3 / P7-I4 | Adoption of the six-stage baseline lifecycle and the Verification-Driven Acceptance framework |
| P7-I5 / P7-I6 | Baseline 02 Workflow — Stage 5 acceptance and Stage 6 transport |
| P7-I8 | Ruling splitting Baseline 04 into 04A / 04B / 04C |
| P7-I9 | Baseline 04A Stage 1 authorization |
| P7-I10 / P7-I11 | F-1 architecture review and governance resolution |
| P7-I12 / P7-I13 | Baseline 04A Stage 4 acceptance and Stage 6 transport |
| P7-I14 | Runtime and Agent conformance preparation review |
| P7-I15 | Baseline 04B Stage 1 authorization |
| P5-I1N-A | Architect ratification of ADR-B4 and ADR-B5 |

**To close:** supply each directive's text under a separate authorization; each
then becomes a register entry under the verbatim rule.

---

### P7-G-2 — Short finding labels collide with unrelated existing repository content

| Field | Value |
|---|---|
| **Identifier** | P7-G-2 |
| **Classification** | **Governance Record Gap** |
| **Raised under** | Baseline 05 — Native Core Governance Closeout, Stage 2 |
| **Disposition** | **Closed by the `P7-` namespace ruling** (R-2), recorded as GDR-0008 §3.8.1. |

**Observation.** Before this register, the program's findings were identified by
bare short labels. The repository already contained unrelated observations using
the same labels:

| Label | This program's meaning | Pre-existing unrelated meaning |
|---|---|---|
| `F-3` | Agent data contracts off the public surface | `docs/architecture/history/phase3/AIOS_PHASE3_25_TRACE_INDEPENDENT_AUDIT_v1.0.md` — INV-4 action-completeness enforced by the future caller |
| `O-1` | Runtime lifecycle model `[O]`-reserved yet exercised | `docs/architecture/history/AIOS_DECISION_REVIEW_METHOD_VALIDATION_PLAN_v1.0.md §9` — whether corpus-independence without reviewer-independence suffices for promotion |

**Verification note.** A substring search reported the program's labels in 17
document files. Every hit was a **false positive** — a different label with the
same characters. A word-boundary search for `FINDING F-n` / `Finding F-n` across
`docs/` returns **0 matches**, confirming that before this register no program
finding was recorded in any document.

**Resolution as ruled.** Governance identifiers carry the `P7-` namespace;
frozen source keeps its historical labels; every entry cross-references both.
No frozen artifact is modified.

---

### P7-G-3 — ADR-B4 and ADR-B5 were ratified but never written to the repository

| Field | Value |
|---|---|
| **Identifier** | P7-G-3 |
| **Classification** | **Governance Record Gap** |
| **Raised under** | Baseline 05 — Native Core Governance Closeout, Stage 2 |
| **Disposition** | Recorded. Writing the ADRs is **not** authorized under this baseline. |

**Observation.** Under `P5-I1N-A` the Architect ratified two Architecture
Decision Records, **ADR-B4** and **ADR-B5**, as normative decisions. Neither
exists in the repository.

**Evidence.**

```
grep -rl "ADR-B4\|ADR-B5" docs/   ->  0 files
docs/architecture/adr/decisions/  ->  ADR-0001 … ADR-0008 only
```

**Consequence.** Two ratified architectural decisions have no durable artifact.
The ADR Framework treats the decision record as the instrument; a ratification
without one leaves the decision unenforceable by review. Closing this requires
both the decisions' text and an authorization to create ADR files — neither of
which Baseline 05 carries.

---

## 5. Durability Status

State of each finding **at the establishment of this register**:

| Identifier | Historical | Durable before | Durable now | Disposition status |
|---|---|---|---|---|
| P7-F-1 | F-1 | ❌ conversation only | ✅ this register | Doc-sync open |
| P7-F-2 | F-2 | ✅ test source | ✅ both | Recorded; repair unauthorized |
| P7-F-3 | F-3 | ✅ test source | ✅ both | Recorded; reserved |
| P7-F-4 | F-4 | ✅ test source | ✅ both | Recorded; reserved |
| P7-L-1 | INV-2 limitation | ❌ conversation only | ✅ this register | Accepted, not a defect |
| P7-O-1 | O-1 | ❌ conversation only | ✅ this register | Record-only |
| P7-O-2 | O-2 | ❌ conversation only | ✅ this register | Open |
| P7-G-1 | — | ❌ | ✅ this register | Open |
| P7-G-2 | — | ❌ | ✅ this register | Closed by R-2 |
| P7-G-3 | — | ❌ | ✅ this register | Open |

Seven of ten findings had no durable repository record before this register.

**Not carried into this register:** the `C-1 … C-11` and `D-1 … D-7` series
referenced in program correspondence. `C-1` is already recorded and resolved in
`AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md` as GDR-0004; the remaining items'
subject matter could not be verified from repository evidence in the closeout
session, and they are therefore **not** recorded rather than recorded
speculatively. They fall under **P7-G-1**.

---

## 6. Integrity Verification

- **Register established:** 2026-08-06. Entries: 10 (P7-F-1 … P7-F-4, P7-L-1,
  P7-O-1, P7-O-2, P7-G-1 … P7-G-3).
- **Findings repaired:** 0.
- **Python files created, modified, or deleted:** 0.
- **Frozen or transported artifacts modified:** 0. Baselines 01, 02, 04A, 04B,
  and 04C remain byte-identical.
- **Historical finding labels changed:** 0.
- **API, export, or public-surface changes:** 0.
- **Specification, Blueprint, Roadmap, Constitution, Domain Model, or ADR
  changes:** 0.
- **Regression:** 421/421 pass; one expected failure (P7-F-2), unchanged.

---

## 7. Closing

This register records findings and nothing else. It creates no entity, amends no
governance text, redesigns no architecture, grants no authority, repairs no
finding, and authorizes no implementation.

Recording a finding here is not a decision about it. Every disposition shown is
one an authority already took, cited to the decision that took it; every
finding shown as open remains open.
