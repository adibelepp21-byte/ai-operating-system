# PD-09 — Quality & Evaluation

> **Status: DERIVED.** Constructed under `FDE-P10-FRONTIER-02`, Decision A.
> **Binding open**, on the same pattern as `PD-08`. Below the Established
> section is bounded derivation, **not canonical**.

| | |
|---|---|
| **CPID** | `PD-09` — permanent |
| **Established name** | Quality & Evaluation |
| **Established domain** | Quality / evaluation domain |
| **Primary construction target** | Evaluation, verification, validation, evidence |
| **Maturity** | DISCOVERED → **CONSTRUCTED (derived, binding-open)** |

---

## 1. Established (source constraint)

- Frozen `PD-02 C8:303` — `PD-09 — Evaluate Quality`. A **role fragment**, and the only PD-09-specific statement in the corpus.
- Frozen `PD-02 A5:331` — `Quality Acceptance │ **ADVISE / INTERFACE** │ Quality authority remains applicable`.
- Frozen `PD-02 A5 §12` — PD-02 may not *"mengambil alih quality authority"*; `A3:123` — nor *"mengambil alih quality execution"*.
- Frozen `PD-02 A4:287` — domain label **Quality**.

## 2. The second unattached owner role

Like `PD-08`, a **Quality authority** is defined in the frozen corpus — PD-02
cannot take it over, and PD-02's own posture toward quality acceptance is
`ADVISE / INTERFACE` rather than decision. And like `PD-08`, **no resident source
states that PD-09 is that authority.**

**These are the two of five domains where the owner role exists and the platform
binding does not.** The pattern is consistent enough to be worth naming: the
frozen corpus reliably describes what PD-02 *may not do* to each domain, and
reliably omits who each domain belongs to — except for PD-05, PD-06 and PD-07,
where a prose binding happens to exist.

**The binding is not asserted here.**

## 3. A distinction this division sharpens

`A5:331` is the only row in PD-02's execution table reading `ADVISE / INTERFACE`
rather than `NONE`. Runtime, AI Engineering, Infrastructure and Security
execution are all simply **not PD-02's**. Quality acceptance is different: PD-02
*participates* through an interface without holding the authority.

Derived reading, offered as such: quality acceptance is a **shared boundary**
rather than an exclusive domain — evaluation crosses every division, so an
interface posture is coherent where exclusion would not be. **This is derivation
from one table cell and is not evidence of PD-09's model.**

## 4. Derived organizational structure

| Part | Derivation for PD-09 |
|---|---|
| **A — Identity & Mandate** | Quality / evaluation domain: evaluation, verification, validation, evidence |
| **B — Organization** | Candidate decomposition from the four construction targets. **Derived from the target list alone** |
| **C — Governance** | Holds quality authority (unbound); interfaces with PD-02 on acceptance rather than being subordinate to it |
| **D — Operating** | Evaluation lifecycle: criteria → measure → evidence → verdict. Constrained by the AIOS-wide rule that a passing test is not a governance result |
| **E — Performance** | Not derived — a division whose domain *is* evaluation cannot have its own evaluation model derived from nothing without circularity |

## 5. A constraint from this program's own history

The corpus already holds hard-won discipline this division's domain must respect:
`VERIFIED ≠ FROZEN` · `test PASS ≠ governance PASS` · raw counts require content
anchoring before they support conclusions. **Any PD-09 evaluation model must
inherit these, not re-derive them** — they were established at cost, including
several documented failures in this program's own verification work.

## 6bis. Inbound relationship — evidenced from another division's corpus

> **Added 2026-09-05** under `ACT-CC-P10-FINAL §26`. Every relationship this
> record previously carried was stated **from PD-02's side** or derived. This one
> is stated by **PD-03's own corpus**, naming this division. **Source body is
> NOT RESIDENT** (`ESC-C7-01`); recorded as evidence, not as a binding.

`PD-03 A1 §22` declares `PRIMARY DEPENDENCIES: Architecture · Security · Quality`
(`E-33`). **`Quality` is PD-09.**

**First evidenced relationship for PD-09.** It sits alongside the resident
`A5:331` `ADVISE / INTERFACE` posture PD-02 holds toward quality acceptance —
two different divisions, two different relations to the same domain.

**It does not bind the Quality authority to `PD-09`**, which remains open on the
same reasoning as `G-03`: naming a domain as a dependency is not naming its
owner.

## 6. Unresolved

Binding to the Quality authority role · whether evaluation is exclusive or shared
· relationship to the resident verification infrastructure (`tools/`,
conformance suites) — no binding evidenced · boundary with PD-03 where compliance
assessment meets quality evaluation.

## 7. Not constructed

No Quality authority declared or bound. No evaluation model imposed on other
divisions. No binding to resident verification infrastructure. Nothing
canonicalized or frozen.


---

## Model layer — what canon establishes for every Platform Division

**Integrated 2026-09-06, Cycle 25.** The four model artifacts in the parent
directory answer all ten construction dimensions **at model level**, from
canonical and frozen source. They apply to this division as to every other, and
**assign it nothing**.

| Established for every division | Source |
|---|---|
| Owns **exactly two** entity types — Capability (inv. 1) and Agent Definition (inv. 2), each *"exactly one Platform Division"* | `DIVISION-OWNERSHIP-MODEL.md` |
| Owns **none** of Skill, Workflow, Tool, Runtime (*"owned centrally"*) or Trace (*"owned by no one"*) | same |
| `home ≠ ownership ≠ privacy` for Knowledge; `accountable-for ≠ owns` for Agent Instance | same · `E-91` |
| Its **own creation, retirement and naming** are *"architectural decision, architect approval"* | `DIVISION-LIFECYCLE-AND-AUTHORITY-MODEL.md` |
| Its **one affirmative discretion**: Agent Definitions are *"created/deprecated at Platform Division discretion within Capability governance"* | same · `E-84` |
| `governs ≠ owns ≠ lifecycle authority` | `Domain Model §4` · `E-85` |
| Capability creation is *"intentionally… restricted to architect-approved decisions… not a gap"* | `DIVISION-CAPABILITY-ARCHITECTURE-EVOLUTION-MODEL.md` · `E-87` |
| The Spine is **three levels**, *"not to be deepened or bypassed without an architectural decision"* | `Domain Model §8` · `E-90` |
| Repository layout is a **projection** of the model — `correspondence ≠ ownership` | `IMPLEMENTATION-CORRESPONDENCE-MAP.md` · `E-90` |
| Performance follows the `E1`–`E10` chain, corroborated across two divisions; **`measurement ≠ authority`** | `DIVISION-OPERATION-AND-PERFORMANCE-MODEL.md` · `E-93` |
| Operation is a **position and shape**, domain-adapted — not common content | same · `E-94` |

**This changes nothing about this division's own content.** Per-division content
remains blocked at `G-01`/`ESC-C7-01`, and per-division **assignment** remains
reserved at `G-09`/`G-10`. `ACT-CC-P10-FINAL §26`: a division is **not** complete
because one dimension is.
