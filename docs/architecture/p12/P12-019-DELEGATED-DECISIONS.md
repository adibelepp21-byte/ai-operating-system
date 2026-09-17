# `E12-01`–`E12-05` — delegated decision records

> **DECISION MADE UNDER `ACT-CC-P12-019`.**
>
> These five decisions were made by Claude Code under an explicit, temporary,
> Founder-issued delegation of P12 completion authority —
> [`ACT-CC-P12-019-P12-COMPLETION-AUTHORITY-DELEGATION.md`](../../governance/acts/ACT-CC-P12-019-P12-COMPLETION-AUTHORITY-DELEGATION.md),
> authenticated at `§3` and `§25`: *Founder Name: Moriarty · Signature:
> Moriarty · Date Issued: 18 September 2026 · Decision Status: FINAL / ISSUED ·
> Founder Authority: ISSUED*.
>
> **They are not Founder ratifications and must never be read as any.** `§7`:
> *"Claude SHALL NOT manufacture a prior Founder ratification. The resulting
> decision SHALL be recorded as: DECISION MADE UNDER ACT-CC-P12-019."*
>
> ```text
> DELEGATED AUTHORITY ≠ TRANSFER OF FOUNDER AUTHORITY
> DECIDED ≠ IMPLEMENTED ≠ INTEGRATED ≠ VERIFIED ≠ COMPLETE
> ```

---

## Governance-substitution audit (`§18`)

| Required field | Answer |
|---|---|
| **Previous authority state** | `E12-01`…`E12-05` were Founder-reserved. `E12-RATIFICATION-DECISION-PACKAGE.md §B` records the five interpretations as *"PROPOSED by this office"* with *"no standing until ratified"*. `FD-P12-001 §5` ratified `§C = R1` for `E12-06` **only**. `FD-P12-003` was issued with all ten decision fields as `[INSERT …]` placeholders and was consumed as `STOP-B`. `ACT-CC-P12-018` prepared the surface and stopped, twenty options unticked. |
| **Founder issuance** | `ACT-CC-P12-019`, authenticated `§3`/`§25`, `FINAL / ISSUED`, 18 September 2026. |
| **Delegated resolution** | These records. |
| Original authority | Founder Reserved Authority |
| Delegating authority | Founder (Moriarty) |
| Delegation instrument | `ACT-CC-P12-019` |
| Reason for delegation | `§1` — to establish `P12 = COMPLETE` without a separate Micro-Act per decision surface. |
| Scope | P12 completion only. |
| Temporal validity | Active while `P12 ≠ COMPLETE`; terminates automatically on verified `P12 COMPLETE` (`§22`). |

**Historical records are unchanged** (`§18`). `FD-P12-003` keeps its
placeholders; `P12-017` keeps its `STOP-B`; `P12-018` keeps its unticked
surface; the Founder P12 Authorization `§16` is not edited. The `§16`
restriction is expressly modified for this scope by `ACT-CC-P12-019 §4`, and
remains operative outside it.

## How these decisions were reached

`§8` forbids automatically choosing the existing proposal, automatically
rejecting it, hybridising for convenience, or modifying a boundary to obtain
`PASS`. Each proposal was read against the **requirement body it claims to
operationalise**, and the question asked was: *does this proposal measure what
the requirement actually asks?*

**Four did not, and the gap was the same shape each time** — the proposal
operationalises part of its requirement and is silent on a named element:

| | Requirement names | Proposal measures | Gap |
|---|---|---|---|
| `E12-01` | eight layers including **CAPABILITY** | integration edges | `CAPABILITY` is not an endpoint of any of `§8`'s eight integration classes |
| `E12-02` | sources, consumers, lifecycle, **staleness**, conflict, reconciliation, provenance | the `STATE → SOURCE → PROJECTION → CONSUMER` chain | freshness is never tested |
| `E12-03` | the **six-link chain** `DECISION → … → CURRENT STATE` | discoverability and enforcement | the chain itself is never resolved |
| `E12-05` | twelve answers **and `SELF-MODEL ≠ AUTHORITY`** | the twelve answers and reversion | the authority prohibition is absent from the clause |

Each modification is **strictly additive and can fail**. None loosens a
boundary. `E12-04`'s proposal was found complete and is ratified unchanged.

**A stricter reading considered and rejected on evidence, not convenience:**
requiring `E12-01`'s `OWNER` attribute to be *assigned* rather than *carried*.
No resident source assigns a provider PD to a phase — the central finding of
`PHASE-PD-CAPABILITY-AND-DEPENDENCY-MAP.md §2` — and `ACT-CC-P6-071 §12`
**tested and rejected** the inference that would supply one. Ratifying a
boundary meetable only by manufacturing that relation would breach
`ACT-CC-P12-019 §10` (*"SHALL NOT infer ownership merely from proximity or
naming"*). It is not an available reading, and `F-17` stays open.

---

## `E12-01`

| | |
|---|---|
| Decision subject | System Integration acceptance boundary |
| Canonical requirement | Founder P12 Authorization **§14 — P12-W1 System Integration Authority**: *"Claude wajib memetakan: PHASE ↓ CAPABILITY ↓ PLATFORM ↓ ORGANIZATION ↓ RUNTIME ↓ WORKFLOW ↓ EVIDENCE ↓ VERIFICATION"*; *"Phase dan Platform Organization harus tetap dibedakan."* |
| Existing proposal | *"every material integration edge carries `SOURCE · TARGET · RELATIONSHIP · OWNER · AUTHORITY · CONTRACT · STATE · EVIDENCE · VERIFICATION · LIFECYCLE` (`§9` edge model) and is classified `VERIFIED/UNVERIFIED/BLOCKED/INVALID/STALE/RESERVED/N-A`"* |
| **Decision** | **RATIFY WITH MODIFICATIONS** |

**Acceptance boundary:**

- **(a)** every material integration edge in `§8`'s eight integration classes carries all ten `§9` attributes and is classified with the `§9` vocabulary;
- **(b)** all eight layers named in `§14` are covered by a resident surface — the P4–P11 verification matrix or an integration-edge endpoint — and every matrix cell is either resolved to a resident source or recorded `UNKNOWN` **with a stated reason**;
- **(c)** Phase and Platform Organization stay distinguished: no edge asserts a Phase↔PD provider relation that no resident source establishes.

**Modification rationale.** The proposal measures edges only. `§14` names
`CAPABILITY`, and `CAPABILITY` is not an endpoint of any of the eight
integration classes — so the proposal as written cannot establish the mapping
`§14` requires. Clause (b) closes that gap using `§46`'s matrix, built under
`ACT-CC-P12-016`. Clause (c) makes *"Phase dan Platform Organization harus
tetap dibedakan"* measurable instead of aspirational.

| | |
|---|---|
| Alternatives considered | RATIFY AS PROPOSED · RATIFY WITH MODIFICATIONS (owner **assigned**) · DO NOT RATIFY · DEFER |
| Rejected — as proposed | under-measures `§14`: `CAPABILITY` untested |
| Rejected — owner assigned | unavailable on evidence: no resident source assigns a provider PD, and `ACT-CC-P6-071 §12` rejected the inference |
| Rejected — DO NOT RATIFY | `§14` is an issued Founder requirement; declining to bound it would leave a canonical requirement unmeasurable |
| Rejected — DEFER | `ACT-CC-P12-019 §13` necessity test passes; deferral reproduces the deadlock the Act exists to end |
| Implementation consequence | none — clause (b)'s surface already exists |
| Verification state | **NOT MEASURED** — see *Measurement state* below |
| Falsification state | **NOT PERFORMED** — measurement is a precondition |
| What remains outside | `F-17` (provider assignment) stays open and Founder-reserved |

---

## `E12-02`

| | |
|---|---|
| Decision subject | Unified Operational State acceptance boundary |
| Canonical requirement | Founder P12 Authorization **§15 — P12-W2 Unified Operational State Authority**: state sources, consumers, lifecycle, staleness, conflict, reconciliation, provenance, cross-phase state relationships; *"Claude tidak boleh menciptakan competing system-wide state authority."* |
| Existing proposal | *"for each state class, `STATE → AUTHORITATIVE SOURCE → PROJECTION → CONSUMER` is established, and no two surfaces claim authority over the same system-wide state"* |
| **Decision** | **RATIFY WITH MODIFICATIONS** |

**Acceptance boundary:**

- **(a)** for each state class, `STATE → AUTHORITATIVE SOURCE → PROJECTION → CONSUMER` is established and the chain is complete;
- **(b)** no two surfaces claim authority over the same system-wide state, and no surface makes an undeclared claim;
- **(c)** every projected state carries an explicit freshness classification (`CURRENT` / `STALE` / `UNKNOWN`) rather than an assumed one.

**Modification rationale.** `§15` names **staleness** and **lifecycle**
explicitly; the proposal's four-link chain never reaches them. Clause (c) makes
the distinction the observation surface was built around — *a stale record is
not evidence of current state* — part of the criterion rather than an
implementation detail beside it.

| | |
|---|---|
| Alternatives considered | RATIFY AS PROPOSED · RATIFY WITH MODIFICATIONS · DO NOT RATIFY · DEFER |
| Rejected — as proposed | silent on staleness, which `§15` names |
| Rejected — DO NOT RATIFY / DEFER | as `E12-01` |
| Implementation consequence | none — freshness classification is resident |
| Verification state | **NOT MEASURED** — see *Measurement state* below |
| What remains outside | `providers_unresolved = 8` (`F-17`) is not made a condition: `§15` does not require a named provider |

---

## `E12-03`

| | |
|---|---|
| Decision subject | Governance Integration acceptance boundary |
| Canonical requirement | Founder P12 Authorization **§16 — P12-W3 Governance Integration Authority**: *"Governance integration wajib mempertahankan: DECISION ↓ AUTHORITY ↓ RATIONALE ↓ IMPLEMENTATION ↓ VERIFICATION ↓ CURRENT STATE."* |
| Existing proposal | *"every resident governance decision is discoverable, and at least one governance decision **constrains runtime behaviour** rather than only describing it"* |
| **Decision** | **RATIFY WITH MODIFICATIONS** |

**Acceptance boundary:**

- **(a)** every resident governance decision is discoverable, and no indexed source is stale;
- **(b)** at least one governance decision constrains runtime behaviour rather than only describing it — demonstrated against a real attempt;
- **(c)** at least one governance decision resolves `DECISION → AUTHORITY → RATIONALE → IMPLEMENTATION → VERIFICATION → CURRENT STATE` by **structural reference**, not parsed prose.

**Modification rationale.** `§16`'s requirement is that the six-link chain be
*preserved*. The proposal tests discoverability and enforcement and never tests
the chain. Clause (c) tests it, and is met by the `W3` escalation→grant join
built under `ACT-CC-P12-003`, which exists precisely because the chain had until
then been joined only by regex over prose.

**Deliberately not added:** `§26`'s nine governance-evidence elements, of which
`affected surfaces` and `verification` are `ABSENT` at `0 / 419`. Closing them
means adding labels to 419 instruments, many historical and some protected —
forbidden by `ACT-CC-P12-019 §23.6`/`§23.7`. Importing an unmeetable clause
would create an unsatisfiable criterion, which `§8` forbids in the other
direction. The gap stays recorded as a non-blocking `EVIDENCE GAP`.

| | |
|---|---|
| Alternatives considered | RATIFY AS PROPOSED · RATIFY WITH MODIFICATIONS (+ `§26`'s nine) · DO NOT RATIFY · DEFER |
| Rejected — as proposed | never tests `§16`'s chain |
| Rejected — with `§26`'s nine | unmeetable without rewriting historical instruments |
| Implementation consequence | none |
| Verification state | **NOT MEASURED** — see *Measurement state* below |
| What remains outside | `§26` `affected surfaces` and `verification` — `EVIDENCE GAP` |

---

## `E12-04`

| | |
|---|---|
| Decision subject | Execution Integration acceptance boundary |
| Canonical requirement | Founder P12 Authorization **§17 — P12-W4 Execution Integration Authority**: `INTENT ↓ DECISION ↓ WORK ↓ EXECUTION ↓ OBSERVATION ↓ VERIFICATION ↓ EVIDENCE`; *"WORK adalah bagian canonical dan tidak boleh dihilangkan"*; *"harus membuktikan hubungan antar-surface, bukan hanya keberadaan masing-masing subsystem."* |
| Existing proposal | *"at least one **real system work** execution traverses the full chain, with each stage evidenced by an execution-produced record, and `WORK` never elided"* |
| **Decision** | **RATIFY AS PROPOSED** |

**Acceptance boundary:**

- **(a)** at least one execution traverses the full `§17` chain with every stage joined and no dangling reference;
- **(b)** `WORK` is never elided — every joined chain carries its work scope;
- **(c)** a demonstrator's traversal does not satisfy the criterion.

**Rationale for ratifying unchanged.** This proposal names `§17`'s chain in
full, requires an **execution-produced** record per stage rather than a
declaration, and carries `§17`'s `WORK` protection in its own text. Its negative
control — *"a demonstrator's traversal must not satisfy the criterion"* — is the
`§17` sentence about proving relationships rather than existence, made
falsifiable. Nothing `§17` names is left unmeasured, so there is nothing to add;
adding anything would be modification for its own sake, which `§8` forbids as
squarely as modification for convenience.

| | |
|---|---|
| Alternatives considered | RATIFY AS PROPOSED · RATIFY WITH MODIFICATIONS (every execution names its work) · DO NOT RATIFY · DEFER |
| Rejected — every execution | three historical executions name only an actor and can never be joined without rewriting history (`§23.6`); and `AIOS_P10… §117.5` established per-path coverage as **not canonically required** |
| Implementation consequence | none |
| Verification state | **NOT MEASURED** — see *Measurement state* below |
| What remains outside | `WORK → EXECUTION` reads `BY CONVENTION` at `7 / 15` corpus-wide — a permanent `EVIDENCE GAP`, not a condition of this criterion |

---

## `E12-05`

| | |
|---|---|
| Decision subject | AIOS Self-Model acceptance boundary |
| Canonical requirement | Founder P12 Authorization **§18 — P12-W5 AIOS Self-Model Authority**: twelve questions answered evidence-backed; *"Self-model hanya merupakan representation/observation mechanism"*; `SELF-MODEL ≠ AUTHORITY`. |
| Existing proposal | *"each of the twelve returns `VERIFIED`, `INFERRED` or `UNKNOWN` with a named source, and **reverts to `UNKNOWN` when its source is removed**"* |
| **Decision** | **RATIFY WITH MODIFICATIONS** |

**Acceptance boundary:**

- **(a)** each of `§18`'s twelve questions returns `VERIFIED`, `INFERRED` or `UNKNOWN`, with none unanswered;
- **(b)** every declared binding resolves — an answer that cannot reach its source is `UNBOUND`, not `VERIFIED`;
- **(c)** no answer returns a permission or authorization: `SELF-MODEL ≠ AUTHORITY`.

**Modification rationale.** `§18` states the authority prohibition in terms and
the proposal's clause omits it — it appears only in the package's
negative-control cell, which is not the boundary. Clause (c) makes `SELF-MODEL ≠
AUTHORITY` part of what is measured, structurally, so the self-model cannot
begin returning permissions without failing its own criterion.

| | |
|---|---|
| Alternatives considered | RATIFY AS PROPOSED · RATIFY WITH MODIFICATIONS · DO NOT RATIFY · DEFER |
| Rejected — as proposed | silent on the prohibition `§18` states twice |
| Rejected — `F-13` taxonomy required | no canonical source classifies a subject as work or demonstration; requiring it would make the criterion depend on a `SOURCE GAP` |
| Implementation consequence | none |
| Verification state | **NOT MEASURED** — see *Measurement state* below |
| What remains outside | `F-13` — the model does not distinguish work subjects from demonstration subjects |

---

## What these decisions do not establish

```text
DECIDED ≠ MEASURED ≠ VERIFIED ≠ COMPLETE
RATIFICATION ≠ SATISFACTION
```

`ACT-CC-P12-019 §20`: *"No single decision, including E12-01 through E12-05,
automatically establishes P12 COMPLETE."* These records fix five acceptance
boundaries and nothing else.

## Measurement state — NOT MEASURED

**No criterion in this record has been measured.** `ACT-CC-P12-020 §6`
explicitly permits the single command that would measure them, and the
execution environment denied it — four times, classified as a permission
boundary, including the exact permitted command. `§25` of that Act requires the
denial to be reported rather than worked around, and forbids fabricating
execution results.

Accordingly:

```text
E12-01 … E12-05   DECIDED, NOT MEASURED
```

The measurement module that reads this record was written and then **removed**,
because it could not be executed, could not be registered with a negative
control the resident verification framework requires, and an unrunnable module
left in `tools/` would break that framework's own coverage guard. Renaming it
out of discovery or exempting it to obtain green status are both forbidden by
`ACT-CC-P12-020 §9`, and neither was done.

**An expectation is not evidence.** `ACT-CC-P12-020 §8`: `PREDICTION ≠
MEASUREMENT ≠ EVIDENCE`. This office expects all five clauses to hold — which
is the most convenient possible result and precisely why it is recorded here as
an expectation and nowhere as a finding.
