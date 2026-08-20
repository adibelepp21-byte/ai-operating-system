# PD-02 Activation Gate Criteria — ADOPTION-READY PROPOSAL

> # PROPOSED — NOT CANONICAL
>
> No governance authority. Not a Gate criterion, Gate result, Activation
> Eligibility, Activation Authorization, or Activation. Becomes canonical **only**
> by explicit Founder Adoption (`ACT-CC-F03-028 §15`, `§19`). Commit, push,
> verification and "adoption-ready" status constitute **no** adoption.

**Version:** v0.4 · **Supersedes:** v0.3 (v0.1–v0.3 retained as provenance)
**Prepared under:** FOUNDER · `ACT-CC-F03-030 §8`, `§9`, `§10`, `§15`
**Prepared by:** Claude Code / Co-Founder (Construction Phase) · **Date:** 2026-08-20
**Founder Adoption:** **NOT EXECUTED** · **Canonical instrument:** **NOT CREATED**

---

## 0. What changed in v0.4 — reconciliation against Founder Option C

The Founder decided **DEC-ACT-SEMANTICS = OPTION C — OPERATIVE AUTHORITY**
(`ACT-CC-F03-030 §1`, recorded at **`GDR-0027`**). v0.4 reconciles the criteria
against that decision. **No criterion was added, removed, renumbered or
re-scoped; AGC-04 remains retired.** Changes are confined to `Evidence Source`,
`Founder Decision Dependency` and present standing, with the change ledger below.

| ID | Was | Now | Reason |
|---|---|---|---|
| **AGC-01** | FAIL — no resident instrument defined activation effects | **PASS-capable** | `GDR-0027 §4` enumerates the effects as **OA-01…OA-07**, bounded by `§5`. Founder dependency **RESOLVED** |
| **AGC-02** | UNRESOLVED — reliance undefined pending AGC-01 | **testable; PASS on present evidence** | With OA-01…OA-06 enumerated, consumer reliance has defined content. Tested explicitly per `ACT-CC-F03-030 §9`: Option C **does** make it testable, so it is **retained, not retired** |
| **AGC-03** | PASS | **PASS** | unchanged |
| **AGC-05** | PASS | **PASS** | unchanged |
| **AGC-06** | FAIL | **FAIL** | Option C *sharpens* it — revocation now means withdrawal of operative authority — but no revocation mechanism is resident. `DEC-REVOCATION` stays Founder-reserved |

**The v0.3 observation that AGC-02 might be permanently unpassable is now
resolved against the evidence, not by preference:** it was contingent on
Status-only semantics, which the Founder did not select.

**New open boundary carried from `GDR-0027 §6`: `OB-01` — no resident instrument
names the actor through which PD-02's operative authority is exercised.** OB-01
affects *exercise*, not *definition*, so it does not fail AGC-02; it is recorded
and routed to the Founder.

---

## 0A. What changed in v0.3

**Schema completion (DOCUMENTATION / STRUCTURAL, per `ACT-CC-F03-029 §11`).** v0.2
satisfied 11/15 of the `§11` schema. Four descriptive fields were missing:
**Verification Method · Failure Handling · Related Rules · Change Control.** They
are added to every criterion and rule below. Classification: documentation and
structural — no normative condition, pass/fail semantic, evidence claim, or
identifier was altered. `§11` bars silently overwriting a canonical schema; this
proposal is **non-canonical**, so no canonical schema was touched.

**External architecture intelligence added** under `§13`–`§16`, recorded as
**EXTERNAL EVIDENCE** and never as AIOS authority. It informs AGC-06's
`Verification Method` and `Change Control`, and the §11 Founder decision package.
No external pattern was adopted into AIOS by this document.

**No criterion was added, removed, renumbered, or re-scoped in v0.3.** AGC-04
remains retired.

---

## 1. What changed from v0.1 to v0.2, and why

The `§8` analytical review found **two structural defects in v0.1**, both mine.

**Defect 1 — AGC-04 was self-referential.** Its evidence was *"the gate record's
own reasoning."* That made the Gate test its own justification rather than a
property of the Volume. GG-2's negative clause is real and binding, but it is a
**rule constraining how the Gate is run**, not a criterion a Volume can pass.

**Defect 2 — AGC-05 mixed two different things.** *"Zero instruments grant the
Co-Founder activation authority"* is a testable repository fact. *"The gate result
is recorded as evidence, never a decision"* is a recording rule. Bundling them
made neither cleanly testable.

**Resolution** (`§14` permits correcting structurally defective criteria, and
splitting for testability): the rule-shaped material moves to a new **Gate
Execution Rules** section. No substance was added or removed — only relocated to
a structurally correct home.

**IDs are stable and never reused.** This repository has been bitten repeatedly by
label collisions (`F-12`, `AG-0x`, `O-5`), so `AGC-04` is **retired, not
recycled**:

| v0.1 | v0.2 | Change |
|---|---|---|
| AGC-01 | **AGC-01** | unchanged |
| AGC-02 | **AGC-02** | unchanged |
| AGC-03 | **AGC-03** | unchanged |
| AGC-04 | **→ GER-01** | reclassified as a Gate Execution Rule; **ID AGC-04 retired** |
| AGC-05 | **AGC-05** + **GER-02** | split: testable half stays, recording rule moves |
| AGC-06 | **AGC-06** | unchanged |

**Result: 5 criteria (AGC-01, -02, -03, -05, -06) + 2 execution rules.** Five was
reached by removing a defect, not by trimming to a number.

Every criterion is also restated in the full 15-field `§14` schema; v0.1 carried
11 fields and lacked **Purpose**, **Scope**, **Founder Decision Dependency** and
**Canonical Status**.

## 2. Derivation basis

Unchanged from v0.1 and re-verified. Criteria derive from **GG-2**
(`ACT-CC-F03-015 §5`) — the sole resident Founder statement of what an activated
Volume *is* — plus its negative clause, `ACT-CC-F03-014 §3`, and `GDR-0011` /
`GDR-0017` as provenance. Not derived from absence, from `T7`/`T8`, from
capability tables, from `AE-01…AE-06`, or from assumed norms (`§13`, and
`ACT-CC-F03-027 §14`).

### §13 required disclosure — similarity to the non-canonical AG-01…AG-10 scaffold

Two **nominal** similarities exist. Both are independently justified from current
canonical evidence; **no AG content was copied**:

| Historical AG | Proposed AGC | Why distinct |
|---|---|---|
| AG-06 *Traceability / evidence integrity* | AGC-03 *Verification Currency* | AG-06 was a derived mechanical roll-up of AG-01…AG-05 at **eligibility** time. AGC-03 tests whether verification is **recomputed at gate time**. Justified from GG-2's *"have been independently verified"* |
| AG-05 *Authority integrity* | AGC-05 *Authority Chain Integrity at Gate Time* | AG-05 pointed at static authority sources. AGC-05 tests, at gate time, that zero instruments grant the Co-Founder activation authority. Justified from `ACT-CC-F03-014 §3`'s recorded Prohibited Pattern |

`AG-01`, `-02`, `-04`, `-07`, `-09`, `-10` have no AGC counterpart. `AG-08` was
superseded by the RG-1 resolution.

## 3. Relationship to AE-01…AE-06 — adjacency disclosed

```text
AE-01 … AE-06   backward-looking : is the RECORD sound enough to ask the question?
AGC / GER       forward-looking  : if the answer is YES, WHAT HAPPENS — and is that
                                   consequence defined, bounded and acceptable?
```

Two adjacencies are disclosed rather than hidden:

- **AGC-03 ~ AE-01 / AE-03.** Different object (the *verification act*, not the records or the review) and different time (gate execution, not eligibility). Distinct, but substantively adjacent.
- **AGC-05 ~ AE-06.** Different object (*gate* result vs *eligibility* result), same underlying principle. Adjacent by design: the principle must bind at both points, because the Prohibited Pattern can be entered at either.

No AE condition is reused as an AGC criterion. `AE-01…AE-06` are untouched.

---

## 4. Proposed criteria — `§14` schema

### AGC-01 — Activation Effect Definition

| Field | Content |
|---|---|
| **Criterion ID** | AGC-01 |
| **Criterion Name** | Activation Effect Definition |
| **Purpose** | Ensure the Gate never certifies readiness for a state whose content is undefined |
| **Normative Condition** | A resident Founder instrument enumerates the effects activation confers, and no stated effect contradicts the frozen architecture |
| **Evidence Required** | A resident instrument stating conferred effects |
| **Evidence Source** | **ESTABLISHED — `GDR-0027 §4`**, recorded under Founder decision `ACT-CC-F03-030 §1`. Effects enumerated as **OA-01…OA-07**, each cited to PD-02's frozen `A5`/`C8` or an existing Founder decision, and bounded by `GDR-0027 §5` (what activation does **not** confer). *Historical note:* before `GDR-0027` this read EVIDENCE NOT ESTABLISHED, with 3 candidates all eliminated |
| **Pass Condition** | A resident Founder instrument enumerates the effects; none contradicts frozen architecture |
| **Fail Condition** | No such instrument, or a stated effect contradicts frozen architecture |
| **Unresolved Condition** | An instrument exists but its effects are not determinable from its text |
| **Rationale** | GG-2 makes the Volume *"an active canonical platform artifact."* `GDR-0011`/RI-0001 shows this repository already separates governance status from operational effect (*"Approval establishes governance status only"*), so the effect must be separately known, never assumed to follow from the status |
| **Dependencies** | None inbound. AGC-02 and AGC-06 depend on it |
| **Scope** | Governance — semantics of the activated state |
| **Provenance** | GG-2 (`ACT-CC-F03-015 §5`) · `GDR-0023` GG-2 · `GDR-0011` RI-0001. Newly formulated |
| **Founder Decision Dependency** | **RESOLVED** — Founder selected Option C; recorded `GDR-0027` |
| **Verification Method** | Query the repository for a resident Founder instrument enumerating activation effects; content-anchor every candidate before counting it (three prior candidates were all false positives) |
| **Failure Handling** | FAIL is terminal for the Gate run: no downstream criterion can be assessed while the effect set is undefined |
| **Related Rules** | GER-01 (an undefined effect cannot be substituted by an excluded ground) |
| **Change Control** | Changes only by a Founder instrument defining or amending activation effects |
| **Canonical Status** | PROPOSED — NOT CANONICAL |

### AGC-02 — Downstream Consumer Impact

| Field | Content |
|---|---|
| **Criterion ID** | AGC-02 |
| **Criterion Name** | Downstream Consumer Impact |
| **Purpose** | Ensure the Gate tests the *transition*, not only the artifact — who may rely on PD-02 once active |
| **Normative Condition** | Downstream consumers are identified, the nature of their reliance is defined, and activation leaves no consumer in an undefined state |
| **Evidence Required** | PD-02 cross-platform content; declared responsibility; the AGC-01 effect definition |
| **Evidence Source** | **ESTABLISHED.** Reliance content is now defined by `GDR-0027 §4` (OA-01…OA-06, incl. OA-06 cross-platform architectural responsibility). 18/50 bodies reference PD-03…PD-10 (PD-03 ×12 · PD-04 ×6 · PD-05 ×16 · PD-06 ×11 · PD-07 ×10 · PD-08 ×6 · PD-09 ×7 · PD-10 ×13; independently re-derived at 18/50). PD-02 declares itself keeper of *"reference architecture"* that is *"acuan structural bagi pengembangan AIOS."* What consumers may do once PD-02 is active is **not** established — it depends on AGC-01 |
| **Pass Condition** | Consumers enumerated; reliance defined; no consumer depends on an undefined effect |
| **Fail Condition** | A consumer's reliance depends on an undefined or contradicted effect |
| **Unresolved Condition** | Consumers identified but the nature of reliance not determinable |
| **Rationale** | Activation is what makes PD-02 usable by others. A Gate that ignores consumers tests the artifact but not the transition |
| **Dependencies** | **Depends on AGC-01.** Not independently assessable until AGC-01 resolves |
| **Scope** | Architecture — integration readiness |
| **Provenance** | PD-02 corpus · GG-2 *"active canonical platform artifact"*. Newly formulated |
| **Founder Decision Dependency** | **RESOLVED** via AGC-01. Residual: `OB-01` affects exercise, not definition |
| **Verification Method** | Enumerate PD-02 bodies referencing PD-03…PD-10; cross-check each consumer's declared reliance against the AGC-01 effect set |
| **Failure Handling** | UNRESOLVED while AGC-01 is unresolved; do not downgrade to FAIL, and do not pass by assuming an effect |
| **Related Rules** | AGC-01 (blocking dependency) |
| **Change Control** | Changes when the consumer set or the AGC-01 effect set changes |
| **Canonical Status** | PROPOSED — NOT CANONICAL |

### AGC-03 — Verification Currency

| Field | Content |
|---|---|
| **Criterion ID** | AGC-03 |
| **Criterion Name** | Verification Currency |
| **Purpose** | Ensure the Gate relies on verification performed *at gate time*, never on a prior report |
| **Normative Condition** | Corpus integrity, review integrity and freeze state are recomputed at gate execution and match their recorded values |
| **Evidence Required** | Corpus digest · per-section SHA-256 · review record blob · freeze record |
| **Evidence Source** | **ESTABLISHED and recomputable.** `RESIDENCY-MANIFEST.md` (50 hashes) · digest `506818698fc7a241683c9257d81a2ee2` · `P7-I99-VOLUME-2-PD-02-REVIEW.md` · `GDR-0026` |
| **Pass Condition** | All four recomputed at gate time and matching |
| **Fail Condition** | Any mismatch |
| **Unresolved Condition** | A source not recomputable at gate time |
| **Rationale** | GG-2 requires that architecture, evidence and lifecycle state *"have been independently verified."* This program has repeatedly found records that were true when written and stale when relied upon; the Gate is where currency must be established, not assumed |
| **Dependencies** | None |
| **Scope** | Integrity |
| **Provenance** | GG-2 · verification method of `ACT-CC-F03-017` FZ-01/FZ-03. Newly formulated as a Gate criterion |
| **Founder Decision Dependency** | NO |
| **Verification Method** | Recompute at gate time: corpus digest, 50 per-section SHA-256 against the manifest, review-record blob against HEAD, freeze record count. Compare to recorded values |
| **Failure Handling** | Any mismatch is FAIL and halts the Gate run; do not repair the mismatch inside the Gate |
| **Related Rules** | GER-02 (currency evidence supports the result; it is not the result) |
| **Change Control** | Recorded values change only through an authorized lifecycle act |
| **Canonical Status** | PROPOSED — NOT CANONICAL |

### AGC-05 — Authority Chain Integrity at Gate Time

| Field | Content |
|---|---|
| **Criterion ID** | AGC-05 |
| **Criterion Name** | Authority Chain Integrity at Gate Time |
| **Purpose** | Close the self-authorization path at the exact moment it could be entered |
| **Normative Condition** | At gate time, **zero** resident instruments grant the Co-Founder activation authority, and the authority chain is reconstructible |
| **Evidence Required** | Appointment Register · Delegation Register · GDR |
| **Evidence Source** | **ESTABLISHED.** `GDR-0023` (*"Volume Activation authority is retained by the Founder"*) · `ACT-CC-F03-014 §3` + Prohibited Pattern · `DEL-F03-015-P7I99-001` exclusions 1–4. Current measured value: **0** |
| **Pass Condition** | Zero such instruments; chain reconstructible |
| **Fail Condition** | Any instrument grants such authority, or the chain cannot be reconstructed |
| **Unresolved Condition** | Authority chain partially reconstructible |
| **Rationale** | `ACT-CC-F03-014 §3` records the pattern *Co-Founder passes its own gate → Co-Founder activates Volume* as **FORBIDDEN**. That pattern is entered, if ever, at gate time |
| **Dependencies** | None |
| **Scope** | Authority |
| **Provenance** | `ACT-CC-F03-014 §3` · `GDR-0023`. Newly formulated as a Gate criterion. **Split from v0.1 AGC-05**; its recording rule moved to GER-02 |
| **Founder Decision Dependency** | NO |
| **Verification Method** | Count resident instruments granting the Co-Founder activation authority; reconstruct the chain Founder → Act → delegation → executor |
| **Failure Handling** | FAIL halts the Gate run and is escalated as an authority defect, never remediated by the executor |
| **Related Rules** | GER-02 (the result must be recorded as evidence, not decision) |
| **Change Control** | Changes only through an Appointment or Delegation Register act |
| **Canonical Status** | PROPOSED — NOT CANONICAL |

### AGC-06 — Post-Activation Change Control and Reversibility

| Field | Content |
|---|---|
| **Criterion ID** | AGC-06 |
| **Criterion Name** | Post-Activation Change Control and Reversibility |
| **Purpose** | Ensure the exit path is examined before the door is opened |
| **Normative Condition** | A resident mechanism governs post-activation change, **and** a resident mechanism permits revocation — or the Founder has expressly determined that irreversibility is intended |
| **Evidence Required** | Change-control procedure · revocation mechanism |
| **Evidence Source** | **EVIDENCE NOT ESTABLISHED, both halves.** (a) `GDR-0017` requires *"the applicable Architecture Change Control"*, but **no resident document defines that procedure** — the term appears only as a requirement inside body content. (b) Volume deactivation / revocation / suspension: **0 files**, re-derived independently by token scan. By contrast `DEL-T4.4-CF-001 §6` defines revocation for a *delegation*, with reversion to `STATE 0` |
| **Pass Condition** | Both mechanisms resident, **or** their absence expressly determined by the Founder to be intended |
| **Fail Condition** | Activation would be irreversible with no Founder determination that irreversibility is intended |
| **Unresolved Condition** | A mechanism is referenced but its procedure is not determinable |
| **Rationale** | Every other authority in this repository is revocable. Without this criterion, Volume activation is the one governance act with no defined exit — a one-way door opened without a recorded decision that it should be one-way |
| **Dependencies** | Depends on AGC-01 |
| **Scope** | Governance — lifecycle |
| **Provenance** | `GDR-0017` · `DEL-T4.4-CF-001 §6` as contrast. Newly formulated |
| **Founder Decision Dependency** | **YES** — `ACT-CC-F03-028 §11` |
| **Verification Method** | Test both halves separately: (a) locate a defined Architecture Change Control procedure; (b) locate a Volume revocation mechanism. Absence of either is a finding, not a pass |
| **Failure Handling** | FAIL unless the Founder has expressly determined irreversibility is intended; the executor may not supply that determination |
| **Related Rules** | AGC-01 (revocation semantics depend on what activation confers) |
| **Change Control** | Changes only by a Founder instrument defining change control or revocation |
| **Canonical Status** | PROPOSED — NOT CANONICAL |

---

## 5. Gate Execution Rules

Rules constrain **how the Gate is run**. They are not criteria the Volume passes,
and they have no PASS/FAIL against the Volume.

### GER-01 — Insufficient-Ground Exclusion *(was v0.1 AGC-04)*

No Gate result may rest, in whole or part, on any ground GG-2 expressly excludes:
*completion of AIOS · completion of future Volumes · Freeze alone · P7-I99 PASS
alone · section-level `PASS` · section-level `FROZEN` · designation · architecture
ownership · execution authority.*

The gate record must state its grounds explicitly so this is checkable after the
fact. **Provenance:** GG-2 negative clause. **Founder Decision Dependency:** NO.
**Verification Method:** inspect the gate record's stated grounds against GG-2's eight excluded grounds.
**Failure Handling:** a result resting on an excluded ground is void, not corrigible.
**Related Rules:** GER-02. **Change Control:** changes only if GG-2 is amended.

### GER-02 — Gate Result Is Evidence, Not Decision *(split from v0.1 AGC-05)*

The Gate result must be recorded as **evidence of eligibility**, never as an
activation decision, and must not be framed so that it could be read as one.

> `ACT-CC-F03-014 §3`: *"A passing gate is evidence of eligibility. It is not an
> activation decision."*

**Provenance:** `ACT-CC-F03-014 §3`. **Founder Decision Dependency:** NO.
**Verification Method:** inspect the recorded result's wording for decision-framing.
**Failure Handling:** re-record the result; never re-run the Gate to obtain different wording.
**Related Rules:** GER-01. **Change Control:** changes only if `ACT-CC-F03-014 §3` is superseded.

---

## 6. Present standing — what a Gate run would return today

| ID | Would return | Because |
|---|---|---|
| AGC-01 | **PASS** | `GDR-0027 §4` enumerates activation effects; none contradicts frozen architecture |
| AGC-02 | **PASS** | Consumers enumerated (18/50 → PD-03…PD-10); reliance content defined by OA-01…OA-06 |
| AGC-03 | **PASS** | All four sources recompute and match |
| AGC-05 | **PASS** | Zero instruments grant Co-Founder activation authority |
| AGC-06 | **FAIL** | Neither an Architecture Change Control procedure nor a revocation mechanism is resident |

**4 of 5 now pass — because the Founder answered the load-bearing question, not
because the criteria were softened.** Every pass/fail threshold is byte-identical
to v0.3; only the evidence changed. **AGC-06 still fails**, and it is the single
remaining criterion-level blocker.

## 7. Founder decisions this proposal cannot make

| § of `ACT-CC-F03-028` | Decision | Blocks |
|---|---|---|
| §10 | What PD-02 activation confers | AGC-01, and AGC-02/AGC-06 downstream |
| §11 | Whether activation is revocable, and on what terms | AGC-06 |
| §§4–6 | AE-04.1 / .2 / .3 dispositions | AE-04 |
| §15 | Adoption outcome | Canonicalization (`§19`) |

`ACT-CC-F03-028 §29` reserves each of these to the Founder in terms. None was
inferred, drafted, or defaulted.

---

## 8. External architecture intelligence — EXTERNAL EVIDENCE only

Recorded under `ACT-CC-F03-029 §13`–`§19`. **External references are evidence and
knowledge inputs. They are not AIOS authority and none was adopted here.**

| Ref | Source | Observed pattern | AIOS comparison | Recommendation |
|---|---|---|---|---|
| **EXT-01** | MADR / ADR status lifecycle (`realpython.com` glossary; `ctaverna.github.io`) | `Proposed → Accepted → Deprecated / Superseded`. *"Once accepted, a decision is not edited; if the conclusion changes, a new ADR is written that supersedes the old one."* Revocation is by **supersession, not mutation** | AIOS already runs ADRs and an **append-only** register with the same immutability property. The mechanism is **native, not foreign** — but AIOS applies it to *decision records*, never to a *Volume lifecycle state* | **ADAPT** |
| **EXT-02** | IETF RFC 2026 §4.2.4 + IESG "Designating RFCs as Historic" (`rfc-editor.org`, `ietf.org`) | A superseded/obsolete specification moves to **Historic** *"with the same Last-Call and notification procedures used for any other standards action"* | The reverse transition uses **the same authority and procedure as the forward one**. AIOS has a forward path (Founder authorization) and **no reverse path at all** | **ADAPT** |
| **EXT-03** | Kubernetes API deprecation policy (`kubernetes.io`, `kubernetes/website`) | GA confers **enumerable guarantees to consumers**: deprecation protection, replacement rules, minimum support duration | Shape-relevant to AGC-01: an activation state can be defined as *a set of guarantees owed to downstream consumers* rather than a bare status flag. AIOS has PD-03…PD-10 as consumers and no stated guarantee | **OBSERVE** |

**Why no ADOPT.** Each pattern's object differs from AIOS's object (decision
record / specification / API version vs **Volume lifecycle state**). Direct
adoption would distort AIOS boundaries; `§16` reserves ADOPT for compatible
patterns. **EXT-03 is OBSERVE, not ADAPT**, because acting on it would answer the
`§10` Founder question — which is Founder-reserved.

**Separation held (`§17`, `§18`):** Decision Recommendation = ADAPT/OBSERVE ·
Governance Decision = **NONE** · Implementation Authorization = **NONE** ·
Implementation Status = **NOT IMPLEMENTED**. No external source was used to change
the Constitution, canonical architecture, governance model, or any Founder
decision, and none was used to bypass an unresolved Founder decision.

---

**PROPOSED — NOT CANONICAL. Founder Adoption: NOT EXECUTED. Canonical instrument: NOT CREATED.**
