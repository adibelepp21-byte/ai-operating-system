# PD-02 Activation Gate Criteria — PROPOSAL

> # PROPOSED — NOT CANONICAL
>
> This document has **no governance authority**. Nothing in it is an Activation
> Gate criterion, an Activation Gate result, Activation Eligibility, an
> Activation Authorization, or an Activation. It becomes canonical **only** by a
> separate explicit Founder adoption record (`ACT-CC-F03-027 §18`). Completion,
> verification, commit and push of this file constitute **no** adoption.

**Version:** v0.1 · **Status:** PROPOSED — NOT CANONICAL
**Prepared under:** FOUNDER · `ACT-CC-F03-027 §8` (proposal authority only)
**Prepared by:** Claude Code / Co-Founder (Construction Phase)
**Date:** 2026-08-20
**Subject:** PD-02 — Architecture Office / Volume 2
**Adoption:** **NOT EXECUTED**

---

## 1. What this proposal answers

`ACT-CC-F03-024` established **AE-05 = NOT SATISFIED**: no resident source
enumerates what the PD-02 Activation Gate must test. The repository defines the
Gate's **position** (`T7`/`T8`) and its **authority** (Founder-reserved) but never
its **content**.

This document proposes that content for Founder decision.

## 2. Derivation basis — what the proposal is built from

`ACT-CC-F03-027 §14` bars deriving Gate criteria from absence, from `T7`/`T8`,
from capability tables, from `AE-01…AE-06` alone, from `AG-01…AG-10`, or from
assumed norms. The criteria below are instead derived from the **resident Founder
definition of Activation** — the one canonical source that states what an
activated Volume *is*:

> **GG-2** (`ACT-CC-F03-015 §5`), recorded as the Founder stated it:
> *"Activation is a **Founder-authorized lifecycle transition** in which a Volume
> is formally recognized as an operationally accepted and governance-authorized
> Volume whose architecture, evidence, lifecycle state, and required activation
> conditions have been independently verified, and whose use as an active
> canonical platform artifact is expressly authorized by the Founder."*

and its negative clause:

> *"**Activation is NOT:** completion of AIOS · completion of future Volumes ·
> Freeze alone · P7-I99 PASS alone · section-level `PASS` · section-level
> `FROZEN` · designation · architecture ownership · execution authority."*

A Gate's job is to test whether that definition actually holds. Each criterion
below traces to a specific element of it.

| Supporting source | Use |
|---|---|
| `ACT-CC-F03-014 §3` | *"A passing gate is evidence of eligibility. It is not an activation decision."* — fixes the Gate's output as evidence; and its recorded **Prohibited Pattern** |
| `GDR-0011` / RI-0001 | Resident precedent for an "artifact becomes authoritative for downstream use" decision: *"Approval establishes governance status only. Approval does not perform repository configuration."* Inspected as **provenance**, not adopted |
| `GDR-0017` | Frozen Volumes require *"the applicable Architecture Change Control"* |
| `GDR-0023` GG-2 | Records the original gap: *"No source defines what activation confers or requires"* |
| PD-02 corpus | Downstream reliance evidence (§4 AGC-02) |

**`AG-01 … AG-10` were inspected as historical provenance only** (`§13`
permits this). None is adopted, promoted, or copied.

## 3. Why these are not a restatement of AE-01…AE-06

`ACT-CC-F03-027 §12` requires the proposed set to remain analytically distinct.
The distinction proposed is directional:

```text
AE-01 … AE-06   backward-looking : is the RECORD sound enough to ask the question?
                (record hygiene, freeze state, review integrity, residual
                 dispositions, gate readiness, authority separation)

AGC-01 … AGC-06 forward-looking  : if the answer is YES, WHAT HAPPENS —
                and is that consequence defined, bounded and acceptable?
```

No AE condition is reused as an AGC criterion.

---

## 4. Proposed criteria

### AGC-01 — Activation Effect Definition

| Field | Content |
|---|---|
| **Gate Question** | What concretely changes — in the repository and in governance — at the moment PD-02 becomes `ACTIVATED`? |
| **Condition** | A resident Founder instrument enumerates the effects activation confers, and those effects are consistent with the frozen architecture |
| **Evidence** | A resident instrument stating conferred effects |
| **Evidence Location** | **EVIDENCE NOT ESTABLISHED.** A scan for resident statements of activation effects returned 3 candidates, all eliminated: the Activation Model's GG-2 *status* row; `GDR-0023`'s statement of the gap itself (*"No source defines what activation confers or requires"*); and `ACT-CC-T4.4:120`, which concerns **Co-Founder office** activation, a different construct |
| **Pass** | A resident Founder instrument enumerates the effects, and none contradicts the frozen architecture |
| **Fail** | No such instrument exists, or a stated effect contradicts frozen architecture |
| **Unresolved** | An instrument exists but its effects are not determinable from its text |
| **Rationale** | GG-2 makes the Volume *"an active canonical platform artifact."* A Gate cannot certify readiness for a state whose content is undefined. RI-0001 shows this repository already separates governance status from operational effect — so the effect must be separately known, not assumed to follow from the status |
| **Relationship** | Prerequisite to AGC-02 and AGC-06 |
| **Classification** | Governance — semantics |
| **Provenance** | GG-2; `GDR-0023` GG-2; `GDR-0011` RI-0001. **Newly formulated under `ACT-CC-F03-027 §14`** |

### AGC-02 — Downstream Consumer Impact

| Field | Content |
|---|---|
| **Gate Question** | Which artifacts or platforms may rely on PD-02 once it is active, and is that reliance defined? |
| **Condition** | The set of downstream consumers is identified, the nature of their reliance is defined, and activation leaves no consumer in an undefined state |
| **Evidence** | PD-02's own cross-platform content and its declared responsibility |
| **Evidence Location** | **PARTIALLY ESTABLISHED.** 18/50 bodies reference PD-03…PD-10 (PD-03 ×12 · PD-04 ×6 · PD-05 ×16 · PD-06 ×11 · PD-07 ×10 · PD-08 ×6 · PD-09 ×7 · PD-10 ×13). PD-02 declares itself keeper of *"reference architecture"* that is *"acuan structural bagi pengembangan AIOS."* **What consumers may do once PD-02 is active is not established** — it depends on AGC-01 |
| **Pass** | Consumers enumerated; reliance defined; no consumer depends on an undefined effect |
| **Fail** | A consumer's reliance depends on an effect that is undefined or contradicted |
| **Unresolved** | Consumers identified but the nature of reliance is not determinable |
| **Rationale** | Activation is what makes PD-02 usable by others. A Gate that ignores who consumes it tests the artifact but not the transition |
| **Relationship** | Depends on AGC-01 |
| **Classification** | Architecture — integration readiness |
| **Provenance** | PD-02 corpus; GG-2 *"active canonical platform artifact"*. **Newly formulated** |

### AGC-03 — Verification Currency

| Field | Content |
|---|---|
| **Gate Question** | Is the independent verification of architecture, evidence and lifecycle state current **at gate time**, rather than inherited from an earlier report? |
| **Condition** | Corpus integrity, review integrity and freeze state are recomputed at gate execution and match their recorded values |
| **Evidence** | Corpus digest · per-section SHA-256 · review record blob · freeze record |
| **Evidence Location** | **ESTABLISHED and recomputable.** `RESIDENCY-MANIFEST.md` (50 per-section hashes); corpus digest `506818698fc7a241683c9257d81a2ee2`; `P7-I99-VOLUME-2-PD-02-REVIEW.md`; `GDR-0026` |
| **Pass** | All four recomputed at gate time and matching |
| **Fail** | Any mismatch |
| **Unresolved** | A source is not recomputable at gate time |
| **Rationale** | GG-2 requires that architecture, evidence and lifecycle state *"have been independently verified."* The Gate is the point at which that must hold — not a point at which a prior report is trusted. This program has repeatedly found stale records that were true when written |
| **Relationship** | Independent |
| **Classification** | Integrity |
| **Provenance** | GG-2; verification method of `ACT-CC-F03-017` FZ-01/FZ-03. **Newly formulated as a Gate criterion** |

### AGC-04 — Insufficient-Ground Exclusion

| Field | Content |
|---|---|
| **Gate Question** | Is the activation being justified, in whole or part, by any ground GG-2 expressly excludes? |
| **Condition** | None of GG-2's eight excluded grounds is load-bearing in the gate reasoning |
| **Evidence** | The gate record's own recorded reasoning |
| **Evidence Location** | **ESTABLISHED as a rule** (GG-2 negative clause). The evidence to test is produced by the gate run itself |
| **Pass** | Zero excluded grounds load-bearing |
| **Fail** | Any excluded ground is load-bearing |
| **Unresolved** | Gate reasoning not recorded in a form that permits the test |
| **Rationale** | GG-2's negative clause is resident, explicit and eight items long. The Gate is the one place it can actually bind. Without this criterion the clause is decorative |
| **Relationship** | Applies across all other criteria |
| **Classification** | Governance |
| **Provenance** | GG-2 negative clause. **Directly derived from resident Founder text** |

### AGC-05 — Authority Chain Integrity at Gate Time

| Field | Content |
|---|---|
| **Gate Question** | At gate time, does activation authority remain Founder-reserved, with no self-authorization path open? |
| **Condition** | Zero resident instruments grant the Co-Founder activation authority; the gate result is recorded as **evidence**, never as a decision |
| **Evidence** | Appointment Register · Delegation Register · GDR |
| **Evidence Location** | **ESTABLISHED.** `GDR-0023` (*"Volume Activation authority is retained by the Founder"*); `ACT-CC-F03-014 §3` including its recorded **Prohibited Pattern**; `DEL-F03-015-P7I99-001` exclusions 1–4 |
| **Pass** | Zero such instruments; gate result recorded as evidence |
| **Fail** | Any instrument grants it, or the gate result is framed as a decision |
| **Unresolved** | The authority chain cannot be reconstructed at gate time |
| **Rationale** | `ACT-CC-F03-014 §3`: *"A passing gate is evidence of eligibility. It is not an activation decision."* The prohibited pattern it records — *Co-Founder passes its own gate → Co-Founder activates Volume* — is defeated at exactly this point |
| **Relationship** | Independent; conceptually adjacent to AE-06 but tested **at gate time**, not at eligibility time |
| **Classification** | Authority |
| **Provenance** | `ACT-CC-F03-014 §3`; `GDR-0023`. **Newly formulated as a Gate criterion** |

### AGC-06 — Post-Activation Change Control and Reversibility

| Field | Content |
|---|---|
| **Gate Question** | After activation, what governs changes to the Volume — and can activation be revoked? |
| **Condition** | A resident mechanism governs post-activation change, and a resident mechanism permits revocation or defines its absence as intentional |
| **Evidence** | Change-control procedure; revocation mechanism |
| **Evidence Location** | **EVIDENCE NOT ESTABLISHED, both halves.** (a) `GDR-0017` requires *"the applicable Architecture Change Control"* for changes to the frozen Volume, but **no resident document defines that procedure** — the term appears only as a requirement inside body content. (b) A scan for Volume deactivation / revocation / suspension returned **0 files**. By contrast `DEL-T4.4-CF-001 §6` defines revocation for a *delegation*, with reversion to `STATE 0` — the repository knows how to write one and has not written one for Volumes |
| **Pass** | Both mechanisms resident, or their absence expressly determined by the Founder to be intentional |
| **Fail** | Activation would be irreversible with no Founder determination that irreversibility is intended |
| **Unresolved** | A mechanism is referenced but its procedure is not determinable |
| **Rationale** | Every other authority in this repository is revocable. Without this criterion, Volume activation is the one governance act with no defined exit — a one-way door opened without a recorded decision that it should be one-way |
| **Relationship** | Depends on AGC-01 |
| **Classification** | Governance — lifecycle |
| **Provenance** | `GDR-0017`; `DEL-T4.4-CF-001 §6` as contrast. **Newly formulated** |

---

## 5. Cardinality

Six criteria were **derived, not targeted**. Four trace to distinct elements of
GG-2's definition (effect · consumers · independent verification · the negative
clause), one to the Gate's role as evidence rather than decision
(`ACT-CC-F03-014 §3`), and one to the unexamined exit path. No criterion was
added to reach six, and none was merged to avoid seven.

## 6. What this proposal does not do

It does not resolve the gaps it identifies. **AGC-01 and AGC-06 would fail today**
— on present evidence a Gate run would return FAIL on both, because what
activation confers and whether it can be revoked are undefined. That is a
finding, not a defect of the proposal: a Gate whose criteria the Volume cannot
yet pass is more useful than criteria written to be passable.

It also does not touch `AE-01 … AE-06`, does not promote `AG-01 … AG-10`, and
creates no canonical instrument.

## 7. Open questions for the Founder

1. **AGC-01** — what does activation actually confer? Until this is answered, no
   Gate can be run to a PASS.
2. **AGC-06** — is Volume activation intended to be revocable? If deliberately
   irreversible, that determination should be recorded rather than left implicit.
3. **AGC-06(a)** — Architecture Change Control is required by `GDR-0017` but has
   no defined procedure anywhere in the repository.
4. Whether six is the right cardinality, and whether any criterion should be
   struck, split, or replaced.

---

**PROPOSED — NOT CANONICAL. Founder adoption: NOT EXECUTED.**
