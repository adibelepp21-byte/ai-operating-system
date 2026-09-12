# P12-W6 — Remaining Scope: Discovery and Classification

**Act:** `ACT-CC-P12-W6-CONTINUATION-001`.
**Mode:** Discovery and classification only. **No construction is performed in
this record** (`§12`: *"Construction Before Classification: PROHIBITED"*).
**Objective:** `§13` — not `13/13 PASS`, but **`13/13 TRUTHFULLY CLASSIFIED`**.

---

## 1. Canonical reconciliation of `§19` (Rule 0)

[A] `§19` of the P12 Authorization names a **minimum verification scope of
thirteen items**. Read from the instrument body, not from any prior report:

```text
CROSS-PHASE CONTRACTS · CROSS-PD INTERFACES · RUNTIME · WORKFLOW · GOVERNANCE
STATE · EVIDENCE · PROVENANCE · FAILURE · NEGATIVE CONTROLS · MUTATION
REGRESSION · FRESH PROCESS
```

[A] `§19` closes: *"P12-W6 tidak boleh dianggap selesai hanya karena unit tests
individual hijau."*

[D] **The thirteen are verification scopes over subjects defined elsewhere in
the Blueprint.** They are not thirteen new Blueprint sections. Read against the
actual bodies, they resolve as:

| `§19` item | Canonical body that defines the subject |
|---|---|
| CROSS-PHASE CONTRACTS | `§10`, `§46`, `§47` |
| CROSS-PD INTERFACES | `§48` Cross-Platform Tests |
| RUNTIME | `§30` Runtime Integration |
| WORKFLOW | `§31` Workflow Integration |
| GOVERNANCE | `§21`–`§27`, in particular `§26` Governance Evidence |
| STATE | `§13`–`§20` (P12-W2) |
| EVIDENCE | `§54` Evidence Matrix |
| PROVENANCE | `§34` Execution Provenance |
| FAILURE | `§33` Failure / Retry / Escalation |
| NEGATIVE CONTROLS | **`§49` Negative Controls** |
| MUTATION | `§50` |
| REGRESSION | `§51` |
| FRESH PROCESS | `§52` |

## 2. Self-correction: NEGATIVE CONTROLS was misclassified as closed

[C] Required by `ACT-CC-P12-W6-CONTINUATION-001 §28`: *"DO NOT DEFEND THE
PREVIOUS CLAIM."*

[A] **`§49` names thirteen mandatory negative controls**, and they are about the
**system**, not about the verifiers:

```text
self-authorization · authority expansion · governance bypass · invalid provenance
fabricated actor · unauthorized delegation · unauthorized state mutation
unauthorized architecture mutation · unauthorized P13 authorization
false completion · false certification · stale-state acceptance
historical-as-current substitution
```

[A] `§49` closes: *"Negative controls are integrity evidence, not an independent
capability dimension."*

[E] `docs/architecture/p12/P12-W6-NEGATIVE-CONTROL-VERIFICATION.md` verified
something different: that **ten P12 verification instruments can each report a
negative result**. That work is real, it is correctly evidenced, and its finding
(the Self-Model answering about a corpus it had not read) is sound.

[C] **But it is not `§49`.** `§49` asks whether the system refuses thirteen
named illegitimate actions. My record claimed the scope item closed. **It is not
closed.** The prior record is not withdrawn — it is reclassified as verifier
falsifiability evidence, which `§18` of the governing Act independently
requires, and `§49` is reopened as an actionable frontier.

[D] The error is the same shape as the one corrected in `§126.1`: a scope item
was treated as satisfied by the work I had done rather than by the requirement
the canonical body states. Finding it required reading `§49`, not `§19`.

## 3. Item-by-item classification

Reported as `ACT §29` requires: **ITEM → REQUIREMENT → STATE → EVIDENCE →
VERIFICATION → CLASSIFICATION → AUTHORITY**.

### 3.1 NEGATIVE CONTROLS — `§49`

- **Requirement:** thirteen named negative controls, each an illegitimate action
  the system must refuse.
- **State:** [E] seven of the thirteen overlap `§50` mutations already attempted
  — invalid provenance, fabricated actor, unauthorized delegation, unauthorized
  state mutation, unauthorized architecture mutation, stale-state acceptance,
  false certification. **Six have never been attempted:** self-authorization,
  authority expansion, governance bypass, unauthorized P13 authorization, false
  completion, historical-as-current substitution.
- **Evidence:** `P12-W6-MUTATION-VERIFICATION.md` for the seven; none for the six.
- **Classification:** **ACTIONABLE — REOPENED.**
- **Authority:** within existing P12 authorization.

### 3.2 RUNTIME — `§30`

- **Requirement:** nine required discovery items — runtime entry points, runtime
  state, runtime-hosted workflows, execution actors, state transitions,
  observation, verification, failure, persistence. *"Claims about runtime
  integration require runtime evidence where runtime evidence is the relevant
  proof."*
- **State:** [E] seven root entry points resident; three runtime observations in
  two kinds; two durable Trace records.
- **Evidence:** [E] **every one of the seven root entry points is a proof or
  demonstrator** (`*_proof.py`, `w4_first_execution.py`). No resident runtime
  entry point is production system work.
- **Classification:** **ACTIONABLE**, with the expectation that the honest
  result is `DEMONSTRATOR-ONLY` for part of the scope — a valid outcome under
  `ACT §13`, and one that must not be eliminated by manufacturing execution
  (`ACT §14`, `§31`).
- **Authority:** within existing P12 authorization.

### 3.3 WORKFLOW — `§31`

- **Requirement:** workflow must connect `PLAN → HANDOFF → WORK → EXECUTION →
  OBSERVATION → VERIFICATION`, and *"P12 must verify actual workflow behavior
  rather than merely inspect definitions."*
- **State:** [U] not yet measured as a chain. The six-element chain has not been
  traced end to end against resident evidence.
- **Classification:** **ACTIONABLE.**
- **Authority:** within existing P12 authorization.

### 3.4 GOVERNANCE — `§26`

- **Requirement:** governance evidence must establish nine elements — decision
  body, authority, effective date, scope, status, provenance, affected surfaces,
  current state, verification.
- **State:** [E] measured against `governance_index.Record` fields. **Six of the
  nine have a resident field**: issuer (decision body), authority, date
  (effective date), status, `source_path`/`source_hash` (provenance),
  `decision_state` (current state). **Three do not: `scope`, `affected
  surfaces`, `verification`.**
- **Classification:** **ACTIONABLE** as verification. Adding the three missing
  fields would be W3 construction and is out of scope for this record.
- **Authority:** within existing P12 authorization for the verification.

### 3.5 PROVENANCE — `§34`

- **Requirement:** execution provenance must identify, where applicable: actor,
  delegator, authority, objective, work scope, capability, workflow, runtime,
  result, evidence, verification. *"Provenance is part of system integrity."*
- **State:** [E] measured against the two resident record types, reading stored
  records rather than class definitions.
  - A resident **delegation record** carries delegator, recipient instance
    (actor), authority instrument **and** authority record, objective,
    capability scope, work scope, verification requirement, and an explicit
    `authority_chain` to the Founder. It carries **no workflow, no runtime, no
    result, and no evidence reference**.
  - A resident **Trace record** carries agent instance (actor), runtime, and
    outputs (result). It carries **no delegation id, no delegator, no authority,
    no objective, no work scope, no workflow, no evidence, no verification**.
- **Finding:** [E] **the two surfaces are not joined.** Nothing links a specific
  execution to the specific delegation that authorized it. The actor name
  appears on both sides, and an actor name is not a link — the same instance
  holds many grants.
- **Classification:** **ACTIONABLE**, and the highest-value item remaining: `§34`
  provenance cannot currently be assembled end to end for any execution.
- **Authority:** within existing P12 authorization.

### 3.6 FAILURE — `§33`

- **Requirement:** failure behavior must distinguish seven states — `RETRYABLE`,
  `BLOCKED`, `REFUSED`, `FAILED`, `ESCALATED`, `SUCCEEDED`, `VERIFIED`. Retry
  must not create duplicate authority, duplicate delegation, duplicate
  execution, orphan state, or false success.
- **State:** [E] the ratified Trace vocabulary is
  `VALID_STATUSES = {success, failure, escalation}` — **three**, not seven.
  `RETRYABLE` has no resident representation in any non-test module.
- **Classification:** **ACTIONABLE** as verification of which of the seven the
  system can actually distinguish. [C] Widening the ratified Trace vocabulary is
  **not** in scope: that vocabulary is ratified, and `§33` does not state that
  Trace must be the surface that carries all seven.
- **Authority:** within existing P12 authorization for the verification.

### 3.7 STATE — `§13`–`§20`

- **Requirement:** `§17` — for every state class, `STATE → AUTHORITATIVE SOURCE
  → PROJECTION → CONSUMER`, and a `STATE AUTHORITY CONFLICT` between two
  surfaces claiming the same system-wide state must be discovered and resolved
  or escalated.
- **State:** [E] **P12-W2 unified operational state is not built.** There is no
  state-authority registry, so there is no surface on which a conflict could be
  discovered. This is the same absence `§124.2` recorded as `UNAVAILABLE` rather
  than `MISSED`.
- **Classification:** **BLOCKED — DEPENDENCY (P12-W2).**
- **Authority:** [C] W2 construction is authorized (`FD §31` D7), but it is
  **construction, not W6 verification**, and `ACT §12` forbids treating a
  candidate as an automatic construction requirement. Verifying state authority
  before a state authority exists is not possible, and manufacturing one inside
  W6 would let an implementation convention establish state authority — which
  `ACT §26` forbids explicitly.

### 3.8 EVIDENCE — `§54`

- **Requirement:** the Evidence Matrix: `Criterion · Requirement · Evidence ·
  Verification · Status · Defect · Authority` for `E12-01`…`E12-06`.
- **State:** [A] every cell of `§54` reads `TBD by canonical reconciliation`, and
  the section states: *"This table is intentionally not pre-certified."*
- **Classification:** **AUTHORITY-BLOCKED — FOUNDER-RESERVED (`F-16`).**
- **Authority:** [O] Filling `§54` assigns requirements and statuses to the E12
  criteria. `ACT §7` forbids selecting an E12 interpretation as canonical, and
  `ACT §25` states `W6 CONSTRUCTION ≠ E12 RATIFICATION`. **Stop at this
  boundary.** [C] Governance evidence per `§26` is a different subject and is
  classified separately at `§3.4` above; it is not a route to `§54`.

## 4. Summary of the thirteen

| # | `§19` item | Classification | Authority |
|---|---|---|---|
| 1 | CROSS-PHASE CONTRACTS | VERIFIED (2 of 8 phases NOT EXERCISED, demonstrator-only for P4/P9) | — |
| 2 | CROSS-PD INTERFACES | SOURCE-BLOCKED + ARCHITECT-RESERVED (`F-18`) | Architect |
| 3 | RUNTIME | **ACTIONABLE** | P12 |
| 4 | WORKFLOW | **ACTIONABLE** | P12 |
| 5 | GOVERNANCE | **ACTIONABLE** | P12 |
| 6 | STATE | **BLOCKED — DEPENDENCY (P12-W2)** | — |
| 7 | EVIDENCE | **AUTHORITY-BLOCKED (`F-16`)** | Founder |
| 8 | PROVENANCE | **ACTIONABLE** | P12 |
| 9 | FAILURE | **ACTIONABLE** | P12 |
| 10 | NEGATIVE CONTROLS | **ACTIONABLE — REOPENED** (was misclassified closed) | P12 |
| 11 | MUTATION | VERIFIED (7 detected, 2 missed, 1 unavailable) | — |
| 12 | REGRESSION | VERIFIED (10 held, 1 unanchored) | — |
| 13 | FRESH PROCESS | VERIFIED (8/8 reproduced) | — |

[E] **Four truthfully classified as verified. Six actionable. Two blocked at a
boundary that is not mine. One — CROSS-PD — blocked at two boundaries at once.**

[C] This is `13/13 TRUTHFULLY CLASSIFIED`, not `13/13 PASS`. `ACT §13`: *"Do not
manufacture work merely to eliminate NOT EXERCISED, UNKNOWN, BLOCKED."*

## 5. What this record does not do

[C] No construction was performed. No frontier was closed. No classification
above is a verification result — each names what must be verified next and under
whose authority.

[C] `F-16`, `F-17` and `F-18` were not approached. `EVIDENCE` stops at `F-16`
and is recorded there rather than routed around.

[C] `E12 RATIFIED = FALSE`. `P12 CONSTRUCTED = FALSE`.
