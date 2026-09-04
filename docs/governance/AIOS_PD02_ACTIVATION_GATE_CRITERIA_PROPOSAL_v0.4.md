# PD-02 Activation Gate Criteria — ADOPTED / CANONICAL

> # ADOPTED — CANONICAL
>
> **Adopted by the Founder, recorded at `GDR-0030`** (`ACT-CC-R12 §7.7` —
> *"ADOPT AGC v0.4 as the canonical Activation Gate criteria"*). These are the
> canonical criteria the PD-02 Activation Gate tests.
>
> Adoption fixes **what the Gate tests**. It is **not** a Gate result, **not**
> Activation Eligibility, **not** Activation Authorization, and **not**
> Activation. No criterion below is thereby marked passed: criterion assessment
> happens at Gate execution, and **the Gate has not been executed**.

**Version:** v0.4 · **Supersedes:** v0.3 (v0.1–v0.3 retained as provenance)
**Prepared under:** FOUNDER · `ACT-CC-F03-030 §8`, `§9`, `§10`, `§15`
**Prepared by:** Claude Code / Co-Founder (Construction Phase) · **Date:** 2026-08-20
**Founder Adoption:** **EXECUTED — `GDR-0030`, 2026-09-03** · **Canonical status:** **CANONICAL**
**Record-currency reconciled under:** `ACT-CC-R13A` (status metadata only; no criterion changed)

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
| **AGC-06** | FAIL | **FAIL** *(as authored 2026-08-20)* | Option C *sharpens* it — revocation now means withdrawal of operative authority — but no revocation mechanism is resident. `DEC-REVOCATION` stays Founder-reserved. **Superseded in its stated reason:** `DEC-REVOCATION` was decided at `GDR-0030` — see §6A |

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
| **Canonical Status** | **CANONICAL** — adopted by the Founder at `GDR-0030` |

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
| **Canonical Status** | **CANONICAL** — adopted by the Founder at `GDR-0030` |

### AGC-03 — Verification Currency

| Field | Content |
|---|---|
| **Criterion ID** | AGC-03 |
| **Criterion Name** | Verification Currency |
| **Purpose** | Ensure the Gate relies on verification performed *at gate time*, never on a prior report |
| **Normative Condition** | Corpus integrity, review integrity and freeze state are recomputed at gate execution and match their recorded values |
| **Evidence Required** | Per-section SHA-256 · review record blob · freeze record. *(Corpus digest removed by Founder decision `GDR-0031` — A-01 = A3.)* |
| **Evidence Source** | **ESTABLISHED and recomputable.** `RESIDENCY-MANIFEST.md` (50 hashes) · `P7-I99-VOLUME-2-PD-02-REVIEW.md` · `GDR-0026`. The historical corpus digest `506818698fc7a241683c9257d81a2ee2` is **preserved as historical evidence** in the review record; its derivation method remains **NOT VERIFIED** and is not reconstructed. It is no longer required evidence for currency (`GDR-0031`). |
| **Pass Condition** | All three recomputed at gate time and matching |
| **Fail Condition** | Any mismatch |
| **Unresolved Condition** | A source not recomputable at gate time |
| **Rationale** | GG-2 requires that architecture, evidence and lifecycle state *"have been independently verified."* This program has repeatedly found records that were true when written and stale when relied upon; the Gate is where currency must be established, not assumed |
| **Dependencies** | None |
| **Scope** | Integrity |
| **Provenance** | GG-2 · verification method of `ACT-CC-F03-017` FZ-01/FZ-03. Newly formulated as a Gate criterion |
| **Founder Decision Dependency** | NO |
| **Verification Method** | Recompute at gate time: 50 per-section SHA-256 against the manifest, review-record blob against HEAD, freeze record count. Compare to recorded values. The corpus digest is **not** recomputed (`GDR-0031`); no retroactive recomputation is authorized |
| **Failure Handling** | Any mismatch is FAIL and halts the Gate run; do not repair the mismatch inside the Gate |
| **Related Rules** | GER-02 (currency evidence supports the result; it is not the result) |
| **Change Control** | Recorded values change only through an authorized lifecycle act |
| **Canonical Status** | **CANONICAL** — adopted by the Founder at `GDR-0030` |

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
| **Canonical Status** | **CANONICAL** — adopted by the Founder at `GDR-0030` |

### AGC-06 — Post-Activation Change Control and Reversibility

| Field | Content |
|---|---|
| **Criterion ID** | AGC-06 |
| **Criterion Name** | Post-Activation Change Control and Reversibility |
| **Purpose** | Ensure the exit path is examined before the door is opened |
| **Normative Condition** | A resident mechanism governs post-activation change, **and** a resident mechanism permits revocation — or the Founder has expressly determined that irreversibility is intended |
| **Evidence Required** | Change-control procedure · revocation mechanism |
| **Evidence Source** | **(a) Change control — RESOLVED.** Founder decision `GDR-0032` (B-01 = B1) classifies a material change to the Volume's **architectural content** as an **architectural-tier** change, governed through the applicable Architecture Change Control and effected through an **ADR** under `Engineering Constitution §3.4`. Supporting resident mechanism: `D8 §70 — Architecture Change Control` (PD-02 corpus, FROZEN) states the six required elements an architecture change must carry, and therefore supplies the record shape; `C2 §32`, `E6 §48` and `D8 §23` route into it. **Boundaries the decision fixes:** Volume ***lifecycle state*** remains **Founder-reserved / governance-lifecycle** (`GDR-0026 §1`) and is unaffected, and inferring lifecycle classification from this content classification is **expressly prohibited**; `GDR-0032` grants **no** modification authority, and Appointment Register §3.2 exclusion 25 remains applicable, so no ADR may be approved on the strength of holding the Architecture Authority role. Investigated under `ACT-CC-R13B` / `ACT-CC-R14C` / `ACT-CC-R14X` / `ACT-CC-R14Y`; decided by the Founder at `GDR-0032`. **(b) Revocation — RESOLVED.** No resident revocation mechanism exists, and the Founder has **expressly determined that irreversibility is intended** (`GDR-0030`, `DEC-REVOCATION` = irreversible by design), which is the Pass Condition's second disjunct. *(Historical: this field previously read "EVIDENCE NOT ESTABLISHED, both halves", then "APPLICABILITY UNRESOLVED"; corrected under `ACT-CC-R14X` and `ACT-CC-R14Z`.)* |
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
| **Canonical Status** | **CANONICAL** — adopted by the Founder at `GDR-0030` |

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

## 6. Standing as authored on 2026-08-20 — what a Gate run would have returned then

| ID | Would return | Because |
|---|---|---|
| AGC-01 | **PASS** | `GDR-0027 §4` enumerates activation effects; none contradicts frozen architecture |
| AGC-02 | **PASS** | Consumers enumerated (18/50 → PD-03…PD-10); reliance content defined by OA-01…OA-06 |
| AGC-03 | **PASS** | All four sources recompute and match |
| AGC-05 | **PASS** | Zero instruments grant Co-Founder activation authority |
| AGC-06 | **FAIL** | Neither an Architecture Change Control procedure nor a revocation mechanism is resident |

**4 of 5 passed — because the Founder answered the load-bearing question, not
because the criteria were softened.** Every pass/fail threshold is byte-identical
to v0.3; only the evidence changed. This table records the position on
2026-08-20; for what has changed since, see §6A.

## 6A. Record-currency note — `ACT-CC-R13A`

`GDR-0030` (2026-09-03) decided `DEC-REVOCATION` as **irreversible by design**,
after §6 above was written. That determination bears directly on AGC-06, whose
**Fail Condition** is *"Activation would be irreversible with no Founder
determination that irreversibility is intended."* **That fail condition is no
longer met.** The §6 row's stated reason is therefore superseded in part.

**No new verdict is assigned here, and none may be inferred.** `ACT-CC-R13A`
authorizes record-currency reconciliation only; it does not assess criteria. What
is established, and what is not:

| | State |
|---|---|
| AGC-06 revocation half — a resident revocation mechanism | **absent**, and the Founder has **expressly determined that irreversibility is intended** (`GDR-0030`) |
| AGC-06 change-control half — a resident Architecture Change Control **procedure** | **A resident definition exists; its applicability was not established when this note was written.** `D8 §70 — Architecture Change Control` (PD-02 corpus, `Status: FROZEN`) states what an architecture change must carry: *change context · affected architecture · impact · applicable review · applicable decision · implementation/follow-up reference*. Two resident flows route into it — `C2 §32` (`Decision → Baseline Impact Assessment → Architecture Change Control → Approved Baseline Update`) and `E6 §48` (`Architecture Change Need → Architecture Change Control → Architecture Review → Architecture Authority → Approved Change`). **What is not established is which procedure is *applicable*:** `GDR-0017` requires *"the **applicable** Architecture Change Control"* and no resident source *then* determined which one applies to a Volume-level post-activation change; the two flows serve different entry points and neither is declared canonical. Established under `ACT-CC-R13B`, disposition **B — SOURCE EXISTS / PROCEDURE UNRESOLVED**. **Superseded by `GDR-0032` (2026-09-04),** whose `§8` records that *"`AGC-06(a)` now has a named applicable path"*: a material change to the Volume's architectural content is **architectural-tier**, governed through the applicable Architecture Change Control and effected through an **ADR** under `Engineering Constitution §3.4`. The residual this row recorded is therefore closed by Founder decision, not by this note |
| AGC-06 criterion result | **NOT ASSESSED** — assessment occurs at Gate execution |
| Gate execution | **NOT PERFORMED** |

A Gate run must evaluate AGC-06's two halves separately, exactly as its own
Verification Method directs: *"(a) locate a defined Architecture Change Control
procedure; (b) locate a Volume revocation mechanism. Absence of either is a
finding, not a pass."*

**Three states stay distinct, and remain distinct after `GDR-0032`:**

```text
ACC mechanism exists          →  YES   (D8 §70, resident, FROZEN)
Applicable ACC procedure      →  NAMED  (GDR-0032 §8: architectural-tier
                                         → ACC → ADR, Constitution §3.4)
AGC-06                        →  NOT ASSESSED — assessment occurs at
                                  Gate execution, which has not been performed
```

**Correction note — `ACT-CC-R14A`.** The row above previously read *"still not
established … every resident occurrence requires it or records its absence."*
That was inaccurate: `D8 §70` defines required content and had been missed,
because earlier searches read `docs/governance/` and grepped for definitional
phrasing rather than reading the frozen corpus bodies. The claim originated in
`v0.1` and was repeated through `v0.4`, `ACT-CC-R13` and `ACT-CC-R13A`. Only this
row is corrected here.

**Recorded, and since corrected under its own authorization.** When this note was
written, AGC-06's own **`Evidence Source`** field in §4 still read *"EVIDENCE NOT
ESTABLISHED, both halves … no resident document defines that procedure."* Half (a)
of that sentence was inaccurate for the same reason, and half (b) was superseded by
`GDR-0030`; `ACT-CC-R14A` authorized correction of the §6A statement only, so the
field was left as committed and its correction was said to warrant its own
authorization. It received one: the field was corrected under `ACT-CC-R14X` and
again under `ACT-CC-R14Z` following `GDR-0032`, and now records both halves as
**RESOLVED**. The sentence quoted above is retained as the record of what the field
said at the time, not as a description of what it says now.

**Correction note — `ACT-CC-R14AF`.** The three statements above were stale
against `GDR-0032` (2026-09-04): the change-control row, the `Applicable ACC
procedure → NOT ESTABLISHED` line, and the claim that §4's `Evidence Source` field
was still uncorrected. §6 directs the reader here for *"what has changed since"*,
so a Gate executor following that pointer met a reading contradicting the criterion
block's, which had already been updated. Only the currency of these records is
changed. `GDR-0032` is not reinterpreted — its own `§8` authorizes *"the bounded
AGC-06 applicability update reflecting this"*, and the criterion block received
that update while this section did not. **No criterion, threshold, acceptance
condition, required evidence, authority boundary or activation condition is
altered, and no verdict is assigned:** AGC-06 remains **NOT ASSESSED**, and the
Gate remains **NOT PERFORMED**.

## 7. Founder decisions this proposal cannot make

| § of `ACT-CC-F03-028` | Decision | Blocks |
|---|---|---|
| §10 | What PD-02 activation confers | AGC-01, and AGC-02/AGC-06 downstream |
| §11 | Whether activation is revocable, and on what terms | AGC-06 |
| §§4–6 | AE-04.1 / .2 / .3 dispositions | AE-04 |

**Currency (`ACT-CC-R13A`):** all three were subsequently decided by the Founder
— §10 at `GDR-0027` (Option C), §11 and §§4–6 at `GDR-0030`. The table is
retained as the record of what this proposal could not decide for itself.
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

**ADOPTED — CANONICAL (`GDR-0030`). Gate execution: NOT PERFORMED. Activation
Eligibility, Activation Authorization and Activation: unchanged by adoption.**
