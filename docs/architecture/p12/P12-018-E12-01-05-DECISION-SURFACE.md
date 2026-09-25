# `E12-01`–`E12-05` — Founder decision surface

> **THIS IS A DECISION SURFACE. IT IS NOT A DECISION.** Prepared under
> `ACT-CC-P12-018`, which `§1` bounds to preparation and `§21` stops at
> `STOP-B — FOUNDER DECISION BOUNDARY`. Every option below is unticked.
>
> ```text
> PREPARATION ≠ RATIFICATION      PROPOSAL ≠ RATIFICATION
> ONE CANDIDATE ≠ A SELECTION     SILENCE ≠ APPROVAL
> CLAUDE PREPARATION ≠ FOUNDER DECISION
> ```

---

## 0. What this replaces, and what it does not

`FD-P12-003` was issued with its five decisions as `[INSERT …]` placeholders and
was consumed as `STOP-B` — see
[`P12-017-RETURN-PACKAGE.md`](P12-017-RETURN-PACKAGE.md). That instrument is
**not edited**; it stands as issued. This document is the surface `§8` of
`ACT-CC-P12-018` requires, so that a next decision has source-backed content
beside each box.

**Two documents share the filename `E12-RATIFICATION-DECISION-PACKAGE.md`.**
The artifact supplied with `ACT-CC-P12-018` is a **blank template** — its
criterion sections read `TO BE POPULATED FROM ACTUAL CANONICAL SOURCE`, 25
times. The **resident** document at
[`E12-RATIFICATION-DECISION-PACKAGE.md`](E12-RATIFICATION-DECISION-PACKAGE.md)
is populated and carries the six proposed interpretations. They are different
documents:

| | sha256 | `TO BE POPULATED` | proposals |
|---|---|---|---|
| supplied template | `0b1dfe15d785c7aa…` | 25 | 0 |
| resident package | `4131531bb892f308…` | 0 | 6 |

The resident one is used, because it is the one `FD-P12-003 §3` names as the
source of truth and the one `tools/p12_e12_criteria` already checks selections
against. The template is **not** written over it. `FILENAME ≠ CANONICAL STATUS`.

## 1. Where the requirements actually come from

Each criterion's canonical requirement is in the **Founder P12 Authorization**,
not the Blueprint. This matters because a bare `§n` resolves to a different
section in each:

| | Founder Authorization `§n` | Blueprint v1.0 `§n` |
|---|---|---|
| `§14` | P12-W1 — System Integration Authority | State Model |
| `§15` | P12-W2 — Unified Operational State Authority | State Sources |
| `§16` | P12-W3 — Governance Integration Authority | State Consumers |
| `§17` | P12-W4 — Execution Integration Authority | State Authority |
| `§18` | P12-W5 — AIOS Self-Model Authority | State Lifecycle |

`ACT-CC-P12-016` found the same split at `§19`. Reading the wrong document would
attribute every criterion to the wrong requirement.

`tools/p12_e12_source_discovery` resolves all five from actual bodies and
verifies that each quotation the package attributes to a section **is present in
that section's body** — a resolved citation is not a citation that supports the
claim. Live: **5 RESOLVED · 0 SOURCE-GAP · 0 CONTRADICTION · 0 AUTHORITY-GAP ·
0 RATIFIED.**

---

## `E12-01`

### Canonical Requirement

| | |
|---|---|
| Originating artifact | `docs/governance/acts/P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md` |
| Exact section | **§14 P12-W1 — SYSTEM INTEGRATION AUTHORITY** |
| Authority | Founder P12 Authorization — ISSUED |
| Provenance | 1 quotation(s) verified present in §14; proposal read from docs/architecture/p12/E12-RATIFICATION-DECISION-PACKAGE.md |
| Discovery status | **RESOLVED** |

Actual body, quoted:

> Dengan D1 = AUTHORIZE P12, Claude berwenang melakukan integration terhadap P4–P11 dalam delegated scope.
> 
> Claude wajib memetakan:
> 
> PHASE
> ↓
> CAPABILITY
> ↓
> PLATFORM
> ↓
> ORGANIZATION
> ↓
> RUNTIME
> ↓
> WORKFLOW
> ↓
> EVIDENCE
> ↓
> VERIFICATION
> 
> Phase dan Platform Organization harus tetap dibedakan.
> 
> Canonical source mensyaratkan explicit Phase ↔ PD capability/dependency mapping.
> 
> ⸻

### Existing Proposed Interpretation

> every material integration edge carries `SOURCE · TARGET · RELATIONSHIP · OWNER · AUTHORITY · CONTRACT · STATE · EVIDENCE · VERIFICATION · LIFECYCLE` (`§9` edge model) and is classified `VERIFIED/UNVERIFIED/BLOCKED/INVALID/STALE/RESERVED/N-A`

**Status: `EXISTING PROPOSAL — NOT RATIFIED`.** This is the interpretation the canonical
package already carries. It is presented as an **existing proposal**, not as a
selection, and it is the only one the corpus contains.

### Existing Acceptance Boundary

- **Evidence source** — derived interface graph; organization records; delegation ledger
- **Verification method** — edge-by-edge classification; no edge admitted on existence alone
- **Negative control** — an edge whose two surfaces exist but which nothing crosses must classify `UNVERIFIED`
- **Failure semantics** — an unclassified material edge is a failure; a `BLOCKED` or `RESERVED` edge is not

### Measurement Consequence

`tools/p12_integration_graph` already derives the eight `§8` integration classes and classifies each with the `§9` vocabulary. Under this proposal the measurement is the existing one: **8 edges — 7 VERIFIED · 0 UNVERIFIED · 1 RESERVED** (`platform ↔ phase`, `F-17`). The `OWNER` attribute reads `UNRESOLVED (F-17)` on all eight, so a reading that required every attribute to be *assigned* rather than *carried* would not be satisfiable by any measurement — it would be satisfiable only by a Founder resolving `F-17`.

### Verification Consequence

Independent: `tools/p12_phase_verification_matrix` reports the same edges through a different derivation, and `p12_negative_control_verification._integration_graph` drives the edge classification in both directions. Falsified by: an edge whose two surfaces exist but which nothing crosses must read `UNVERIFIED` — proved live.

### Founder Decision

```text
[ ] RATIFY AS PROPOSED
[ ] RATIFY WITH MODIFICATIONS
    Modification:
    ________________________________
[ ] DO NOT RATIFY
[ ] DEFER
```

---

## `E12-02`

### Canonical Requirement

| | |
|---|---|
| Originating artifact | `docs/governance/acts/P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md` |
| Exact section | **§15 P12-W2 — UNIFIED OPERATIONAL STATE AUTHORITY** |
| Authority | Founder P12 Authorization — ISSUED |
| Provenance | 1 quotation(s) verified present in §15; proposal read from docs/architecture/p12/E12-RATIFICATION-DECISION-PACKAGE.md |
| Discovery status | **RESOLVED** |

Actual body, quoted:

> Claude berwenang membangun state integration surface untuk:
> 
> * state sources;
> * state consumers;
> * lifecycle;
> * staleness;
> * conflict;
> * reconciliation;
> * provenance;
> * cross-phase state relationships.
> 
> Claude tidak boleh menciptakan competing system-wide state authority.
> 
> ⸻

### Existing Proposed Interpretation

> for each state class, `STATE → AUTHORITATIVE SOURCE → PROJECTION → CONSUMER` is established, and no two surfaces claim authority over the same system-wide state

**Status: `EXISTING PROPOSAL — NOT RATIFIED`.** This is the interpretation the canonical
package already carries. It is presented as an **existing proposal**, not as a
selection, and it is the only one the corpus contains.

### Existing Acceptance Boundary

- **Evidence source** — runtime/workflow observations; governance records; organization records
- **Verification method** — conflict detection across claimed authorities; freshness classification
- **Negative control** — a stale record must not read as current; an empty store must read `UNKNOWN`, never zero
- **Failure semantics** — two live authorities over one state class is a failure; an `UNKNOWN` with a named absent source is not

### Measurement Consequence

`tools/p12_operational_state` and `tools/p12_state_verification` already derive it: **8 sources, 8 projected, 8 current, 0 stale, 0 unknown, 0 conflicts, 0 undeclared claims**, and the `STATE → AUTHORITATIVE SOURCE → PROJECTION → CONSUMER` chain reports **4 / 4 links satisfied, chain complete**. `providers_unresolved` is 8 — `F-17` again — so a reading requiring a named provider per state class would not be measurable today.

### Verification Consequence

Independent: `tools/p12_operational_state_verifier` checks the state properties without importing the projection. Falsified by: a stale record read as current, and an empty store read as zero rather than `UNKNOWN` — both refused live by `§49` controls.

### Founder Decision

```text
[ ] RATIFY AS PROPOSED
[ ] RATIFY WITH MODIFICATIONS
    Modification:
    ________________________________
[ ] DO NOT RATIFY
[ ] DEFER
```

---

## `E12-03`

### Canonical Requirement

| | |
|---|---|
| Originating artifact | `docs/governance/acts/P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md` |
| Exact section | **§16 P12-W3 — GOVERNANCE INTEGRATION AUTHORITY** |
| Authority | Founder P12 Authorization — ISSUED |
| Provenance | 1 quotation(s) verified present in §16; proposal read from docs/architecture/p12/E12-RATIFICATION-DECISION-PACKAGE.md |
| Discovery status | **RESOLVED** |

Actual body, quoted:

> Claude berwenang mengintegrasikan existing governance mechanisms.
> 
> Governance integration wajib mempertahankan:
> 
> DECISION
> ↓
> AUTHORITY
> ↓
> RATIONALE
> ↓
> IMPLEMENTATION
> ↓
> VERIFICATION
> ↓
> CURRENT STATE
> 
> Claude tidak boleh menggunakan P12 sebagai alasan untuk menyelesaikan Founder/Architect reserved matter.
> 
> ⸻

### Existing Proposed Interpretation

> every resident governance decision is discoverable, and at least one governance decision **constrains runtime behaviour** rather than only describing it

**Status: `EXISTING PROPOSAL — NOT RATIFIED`.** This is the interpretation the canonical
package already carries. It is presented as an **existing proposal**, not as a
selection, and it is the only one the corpus contains.

### Existing Acceptance Boundary

- **Evidence source** — the Register; resident instruments; the certified-evidence guard
- **Verification method** — decision visibility measured; enforcement demonstrated against a real attempt
- **Negative control** — an attempt to overwrite certified evidence must be refused **loudly**, and a guard that cannot see an unguarded call site must fail its own conformance check
- **Failure semantics** — a decision that constrains documents but not behaviour is unintegrated

### Measurement Consequence

`tools/governance_index` reports **473 records from 553 sources, 0 stale**, and the second clause — *at least one governance decision constrains runtime behaviour* — is met by `tools/p12_certified_evidence_guard`, which refuses a real write under `docs/architecture/p11`. `§26`'s nine governance-evidence elements measure **1 established · 6 partial · 2 absent**, so a reading that required all nine machine-readable would not be satisfiable without editing 419 instruments, which `§17.7` forbids.

### Verification Consequence

Independent: `tools/p12_governance_evidence_verification` measures the corpus rather than the parser, per element, as a count. Falsified by: an attempt to overwrite certified evidence must be refused loudly — exercised live, and a planted certification statement is still **accepted** by `certified_phases`, which the mutation suite reports as `MISSED` and `Freeze §10` reserves.

### Founder Decision

```text
[ ] RATIFY AS PROPOSED
[ ] RATIFY WITH MODIFICATIONS
    Modification:
    ________________________________
[ ] DO NOT RATIFY
[ ] DEFER
```

---

## `E12-04`

### Canonical Requirement

| | |
|---|---|
| Originating artifact | `docs/governance/acts/P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md` |
| Exact section | **§17 P12-W4 — EXECUTION INTEGRATION AUTHORITY** |
| Authority | Founder P12 Authorization — ISSUED |
| Provenance | 1 quotation(s) verified present in §17; proposal read from docs/architecture/p12/E12-RATIFICATION-DECISION-PACKAGE.md |
| Discovery status | **RESOLVED** |

Actual body, quoted:

> Canonical execution chain:
> 
> INTENT
> ↓
> DECISION
> ↓
> WORK
> ↓
> EXECUTION
> ↓
> OBSERVATION
> ↓
> VERIFICATION
> ↓
> EVIDENCE
> 
> WORK adalah bagian canonical dan tidak boleh dihilangkan.
> 
> P12 execution integration harus membuktikan hubungan antar-surface, bukan hanya keberadaan masing-masing subsystem.
> 
> ⸻

### Existing Proposed Interpretation

> at least one **real system work** execution traverses the full chain, with each stage evidenced by an execution-produced record, and `WORK` never elided

**Status: `EXISTING PROPOSAL — NOT RATIFIED`.** This is the interpretation the canonical
package already carries. It is presented as an **existing proposal**, not as a
selection, and it is the only one the corpus contains.

### Existing Acceptance Boundary

- **Evidence source** — durable Trace records; published observations
- **Verification method** — independent process reads the evidence; `DEMONSTRATOR ≠ SYSTEM WORK` enforced
- **Negative control** — a demonstrator's traversal must not satisfy the criterion
- **Failure semantics** — a chain missing `WORK` or `OBSERVATION` is incomplete regardless of test results

### Measurement Consequence

`tools/p12_execution_chain_reader` reports **4 / 4 manifests joined, 0 dangling, 7 edges per chain**, and `aios_corpus_health_run` is a real-work execution that reaches `OBSERVATION` and `EVIDENCE`. The `WORK → EXECUTION` link reads **BY CONVENTION at 7 / 15**: three historical executions name only an actor and can never be joined without rewriting history. A reading requiring *every* execution to name its work is therefore permanently unsatisfiable; a reading requiring *at least one* full traversal is satisfied today.

### Verification Consequence

Independent: `tools/p12_provenance_verification` assembles the chain from records it did not write and reports `NOT ASSEMBLABLE` where it cannot. Falsified by: a demonstrator's traversal must not satisfy it — enforced structurally by `_is_demonstrator_only`.

### Founder Decision

```text
[ ] RATIFY AS PROPOSED
[ ] RATIFY WITH MODIFICATIONS
    Modification:
    ________________________________
[ ] DO NOT RATIFY
[ ] DEFER
```

---

## `E12-05`

### Canonical Requirement

| | |
|---|---|
| Originating artifact | `docs/governance/acts/P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md` |
| Exact section | **§18 P12-W5 — AIOS SELF-MODEL AUTHORITY** |
| Authority | Founder P12 Authorization — ISSUED |
| Provenance | 1 quotation(s) verified present in §18; proposal read from docs/architecture/p12/E12-RATIFICATION-DECISION-PACKAGE.md |
| Discovery status | **RESOLVED** |

Actual body, quoted:

> Self-model P12 harus dapat membangun evidence-backed answers terhadap:
> 
> What am I?
> What do I own?
> What authority do I have?
> What capabilities exist?
> What is running?
> What failed?
> What is incomplete?
> What is authoritative?
> What changed?
> What is stale?
> What do I not know?
> What decisions are recorded?
> 
> Self-model hanya merupakan representation/observation mechanism.
> 
> SELF-MODEL
> ≠
> AUTHORITY
> 
> Self-model tidak dapat mengotorisasi dirinya sendiri berdasarkan informasi yang ditemukannya.
> 
> ⸻

### Existing Proposed Interpretation

> each of the twelve returns `VERIFIED`, `INFERRED` or `UNKNOWN` with a named source, and **reverts to `UNKNOWN` when its source is removed**

**Status: `EXISTING PROPOSAL — NOT RATIFIED`.** This is the interpretation the canonical
package already carries. It is presented as an **existing proposal**, not as a
selection, and it is the only one the corpus contains.

### Existing Acceptance Boundary

- **Evidence source** — governance index; Trace registry; observation registry; organization records
- **Verification method** — answer each with its source; prove reversion against emptied evidence roots
- **Negative control** — no answer returns a permission; an absent source must not be filled in
- **Failure semantics** — a `VERIFIED` answer that survives removal of its source is fabricated

### Measurement Consequence

`tools/p12_self_model` answers the twelve `§18` questions with a named source each, and reversion is proved: emptying an evidence root returns the affected answers to `UNKNOWN`. `F-13` remains open — the model does not distinguish work subjects from demonstration subjects — and no canonical source supplies that taxonomy, so a reading requiring it would be blocked by a `SOURCE GAP` rather than by engineering.

### Verification Consequence

Independent: `tools/p12_self_model_contract` checks each binding and reports `UNBOUND` on a wrong one. Falsified by: a `VERIFIED` answer that survives removal of its source is fabricated — the reversion proof is exactly that control.

### Founder Decision

```text
[ ] RATIFY AS PROPOSED
[ ] RATIFY WITH MODIFICATIONS
    Modification:
    ________________________________
[ ] DO NOT RATIFY
[ ] DEFER
```

---

## Cross-criterion analysis

| Relationship | Finding |
|---|---|
| **Shared evidence** | `E12-01` and `E12-02` both read the observation store; `E12-04` and `E12-05` both read durable Trace records. The same record therefore supports more than one criterion, which is legitimate — but a single corrupted store would move four criteria at once, so their results are **not independent failures**. |
| **Criterion-specific evidence** | `E12-03`'s enforcement clause rests on the certified-evidence guard, which nothing else uses; `E12-05`'s reversion proof requires *removing* evidence roots, which no other criterion does. |
| **Sequencing** | None. The five are measurable in any order once ratified. |
| **Semantic dependency** | `E12-01`'s `OWNER` attribute and `E12-02`'s `providers_unresolved` are the **same open matter** (`F-17`). A reading of `E12-01` that required owners to be *assigned* would make `E12-02` unsatisfiable by the same fact, and vice versa. This is the one place where deciding one criterion silently constrains another. |
| **Overlapping boundaries** | `E12-04`'s *"at least one real system work execution traverses the full chain"* and `E12-06`'s ratified `R1` *"consumption by real system work"* are adjacent but distinct: `E12-04` is about one chain being complete, `E12-06` about eight phases being crossed. Neither subsumes the other. |
| **Contradiction between criteria** | **None found.** |

`CONSISTENCY ANALYSIS ≠ FOUNDER DECISION` — the `F-17` interaction is reported,
not resolved.

---

## `§54` consequence

```text
§54 = NOT YET RECONCILED
```

The five `Requirement` cells read `TBD by canonical reconciliation` and stay
that way until a Founder decision issues. Their `Evidence` and `Verification`
columns are already resident and measured. `RATIFICATION ≠ SATISFACTION`:
ratification would fix the boundary; measurement would then decide whether the
evidence meets it, and independent verification would test the measurement.

## `§74-J` consequence

```text
§74-J = NOT YET EVALUABLE for condition 1
```

`§56`'s eight completion conditions: seven are evidenced in
[`P12-74-PART-J-COMPLETION-EVIDENCE.md`](P12-74-PART-J-COMPLETION-EVIDENCE.md);
`REQUIREMENTS` is not, and needs all five decisions. No pre-ratification
evidence has been backfilled as post-decision evidence.

## P12 completion consequence

```text
P12 CONSTRUCTION EXHAUSTED  ≠  P12 COMPLETE  ≠  P12 CERTIFIED
P12 COMPLETION = NOT COMPLETE — blocked on the five decisions above
```

## Protected boundaries

`P13` not authorized · Native Core `11` · `F-17` unchanged · `F-18` unchanged
(Architect-reserved under `ADR-0029`) · no autonomous runtime · no historical
evidence rewritten · no Founder or Architect authority created.
