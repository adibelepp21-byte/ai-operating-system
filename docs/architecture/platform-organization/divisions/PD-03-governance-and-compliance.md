# PD-03 — Governance & Compliance

> **Status: DERIVED.** Constructed under `FDE-P10-FRONTIER-02`, Decision A.
> Established identity and domain are constraints, not proposals. Everything
> below the Established section is bounded derivation and is **not canonical**.

| | |
|---|---|
| **CPID** | `PD-03` — permanent, not reassignable |
| **Established name** | Governance & Compliance |
| **Established domain** | Governance authority |
| **Primary construction target** | Policy, standards, controls, compliance |
| **Maturity** | EVIDENCE-READY → **CONSTRUCTED (derived)** |

---

## 1. Established (source constraint — not derived)

- `MASTER_ROADMAP §5` — official name; CPID permanent, never reused.
- Frozen `PD-02 A4:281` — domain label **Governance**, inside the architectural boundary diagram, with *"PD-02 tidak menjadi owner atas domain tersebut"* — PD-02 owns none of these domains.
- Frozen `PD-02 A5 §12 Override Limit` — PD-02 may not *"membatalkan Governance Authority"*. **A Governance Authority exists and is not PD-02's.**
- Frozen `PD-02 A5:324` — `Governance Policy │ ADVISE │ Governance Authority remains applicable`. PD-02 advises; it does not decide governance policy.
- `PD-01 C10:85` — PD-03 owns its own domain success criteria.

### 1.1 The canonical volume structure — evidenced 2026-09-05, **eight Parts, not five**

`ACT-CC-P6-070 §2.2` (resident, 590 lines) inventories PD-03's canonical volume.
**Its structure is `A`–`H` × 10 = 80 sections**, and the Parts are named:

| Part | Subject |
|---|---|
| **A** | Platform Identity & Strategic Foundation |
| **B** | Organization Architecture |
| **C** | Governance Architecture |
| **D** | Governance Operations |
| **E** | Performance Architecture |
| **F** | Lifecycle Architecture |
| **G** | Platform Integration |
| **H** | Platform Evolution |

**This matters for §3 below.** The derived structure there uses the five-part
`A`–`E` Kernel spine abstracted from PD-01 and PD-02. **PD-03's own recorded
structure has eight Parts** — `F` Lifecycle, `G` Integration and `H` Evolution
have no counterpart in the spine. The spine is therefore **not** a reduced form
of PD-03's structure; it is a different structure, and §3's five-part derivation
should be read as a Kernel projection rather than as PD-03's shape (`E-20`).

**No Part `F`, `G` or `H` is constructed here.** Their identities are evidenced;
their content is not.

### 1.1a Canonical identity — **read from the source body**, 2026-09-05

`Volume 3 Part A`, section `A1 — Platform Identity`, carries this header
verbatim:

```text
Platform ID        : PD-03
Platform Name      : Governance & Compliance
Platform Type      : Platform Division
Platform Authority : Governance Authority
Volume             : 3
Document Type      : Platform Encyclopedia Volume
Part               : Part A — Platform Identity & Strategic Foundation
Section            : A1 — Platform Identity
Status             : FROZEN
Version            : 1.0
Classification     : Core Platform Identity
Reference Baseline : Governance Baseline
Gold Standard Review : PASS
Freeze Decision    : APPROVED
```

**Three things follow, and one deliberately does not.**

1. **`Platform Authority: Governance Authority` is declared by PD-03's own corpus.** Until now this record stated that no source says *"PD-03 is the Governance Authority"* — that was true of the **resident** corpus and is **superseded** by the source body. The Governance Authority row in `divisions/README.md §6` is updated from *unbound* to **self-declared**.
2. **`Platform Type: Platform Division`** independently corroborates `ADR-0010` (FD-6, `GDR-0020`) from a corpus written outside this repository. `ADE-P10-G04`'s determination is confirmed by a second, unrelated source.
3. **The header format matches frozen `PD-02 A4` exactly** — same fields, same `Gold Standard Review: PASS` / `Freeze Decision: APPROVED` pattern. The two volumes are the same document family.

**What does not follow: a binding performed by this record.** PD-03's corpus
declares its own authority; recording that declaration is evidence. **Binding the
Governance Authority role to `PD-03` as an act of this corpus would be
assignment**, reserved by `FDE §19`. Not done — the declaration is reported as
the source's, not adopted as mine.

**Provenance:** the source body is **NOT RESIDENT** (`ESC-C7-01`). Every quotation
above is cited to a supplied-source path, and nothing is reconstructed.

### 1.1bis The Claude Code Handoff Package — read 2026-09-05

A fourth PD-03 source exists and had never been opened: **`AIOS Volume 3 — PD-03
Canonical Source Consolidation & Claude Code Handoff Package`**, `Document Type:
Canonical Source Consolidation / Engineering Handoff`, **`Target: Claude Code /
AIOS Repository`**, `Status: CLOSED / FROZEN / TERMINAL`.

It is the most directly relevant document in the entire recovery, and it adds
material no other source carries.

**Canonical identity, fuller than `A1`'s:**

```text
Primary Authority       : Governance Authority
Primary Domain          : Governance & Compliance
Primary Responsibilities: Policy · Control · Certification ·
                          Compliance · applicable Governance Standards
```

`A1 §22` lists three responsibilities; the handoff lists **five**. Both are
source; the wider list is recorded as the handoff's, not merged silently.

**What PD-03 does NOT automatically own** — the negative boundary, enumerated:
architecture design · security execution · quality execution · runtime execution
· engineering implementation · operational management of another Platform ·
technical design belonging to another owner. And: *"PD-03 tidak boleh mengambil
alih domain ownership Platform lain hanya karena memiliki governance
authority."*

**Canonical governance chain:**

```text
Requirement → Policy / Standard → Governance Action → Decision / Approval
   → Evidence → Finding / Outcome → Corrective Action → Verification
```

**Part-specific canonical positions**, which constrain how each Part may be read:
Part A is *"the constitutional identity layer… must not become a detailed
operating manual"* · `B1` *"establishes the organizational model; it does not
arbitrarily invent the final Sub Division list"*, and for PD-03 that model *"must
derive from its actual responsibilities and boundaries rather than copying
PD-01"* · `C1` is the Governance Constitution and parent of the governance
architecture · Part D *"must not become an alternative governance constitution"*
· Part E performance must remain distinct from governance authority, operational
execution and lifecycle change authority.

**`Part I` is intentionally absent** — `Part I: NOT ESTABLISHED / NOT
CONSTRUCTED`, and *"Do not construct Part I. Do not treat absence of a canonical
successor as a missing section."* **The eight-Part structure is terminal by
design, not incomplete**, and `H10` is the terminal section.

**The handoff independently confirms the `B1`→`B6`→`B7`–`B10` sequence** this
record derived from section titles, and states the same source-fidelity rule this
corpus applies: *"Do not convert B into A silently. Do not convert C into A. Do
not fill C with model assumptions."*

**On residency — see `ESC-C7-01`.** The handoff's `§11` accepts consolidation
*"only if A1–A10 are **resident** … B1–B10 are **resident** …"* and its `§12`
requires a *"Volume 3 residency result"*. **It specifies the outcome in detail and
carries no issuance**: no signature, no date, no authorizing Act, no target
repository path. It is the missing *specification*, not the missing *authority*.

### 1.1c `A1` Canonical Status & Freeze Record — read from source

`Volume 3 Part A`, `A1` §22, states verbatim:

```text
PLATFORM AUTHORITY         : Governance Authority
PRIMARY DOMAIN             : Governance & Compliance
PRIMARY RESPONSIBILITIES   : Policy · Control · Certification
PRIMARY DEPENDENCIES       : Architecture · Security · Quality
CANONICAL REFERENCE        : Governance Baseline
PRIMARY OUTPUTS            : Policy · Standards
TECHNICAL DESIGN OWNERSHIP : NOT OWNED BY PD-03
STATUS                     : FROZEN
GOLD STANDARD REVIEW       : PASS
MATERIAL GAP               : NONE DETECTED FOR A1 IDENTITY
FREEZE DECISION            : APPROVED
```

and its `§24 Canonical Freeze Statement`:

> *"A1 — Platform Identity establishes PD-03 Governance & Compliance as the
> **Governance Authority** within the Governance & Compliance domain, with primary
> responsibility for **Policy, Control, and Certification**, and with
> **Architecture, Security, and Quality** identified as primary dependencies.
> **PD-03 does not own Technical Design.**"*

**This fills four dimensions the Evidence Ledger recorded ABSENT for PD-03** —
Authority, Ownership (negative), Dependency, and Interface — **from PD-03's own
corpus rather than from PD-02's side.**

**A second positive dependency set.** `PD-03 → Architecture`, `Security`,
`Quality` — that is `PD-02`, `PD-08`, `PD-09`. With `E-24`'s
`PD-04 → PD-06`, `PD-05`, the corpus now evidences **five directional edges
across two divisions**, where Cycle 5 recorded none at all. `G-05` is extended
again.

**A negative ownership boundary, stated by the owner.** `TECHNICAL DESIGN
OWNERSHIP: NOT OWNED BY PD-03` is PD-03 declaring what it does **not** own —
structurally the same move frozen `PD-02 A4:289` makes (*"PD-02 tidak menjadi
owner atas domain tersebut"*). **Both volumes define themselves substantially by
exclusion.**

### 1.1d The source states its own limits — `A1 §21`

`A1 §21 Source-Fidelity Boundary` records what the baseline **explicitly
supports** — Platform ID · Platform Name · Authority Level · Primary
Responsibility · Primary Dependencies · Canonical Reference · Primary Outputs ·
Technical Design boundary — and what it **does not establish at `A1` level**:

> detailed Governance Charter · detailed Governance Authority Matrix · internal
> organizational structure · governance workflow · performance model ·
> governance maturity target · detailed certification lifecycle
>
> *"Karena itu item tersebut tidak diklaim sebagai canonical content A1."*

**The source applies the same discipline this corpus does**: it enumerates what
its own evidence does not reach and declines to claim it. That is independent
corroboration that the method here is not idiosyncratic — and it means the seven
items above are **source-acknowledged gaps**, not gaps this record discovered.

### 1.1b The 80 sections — titles read from source

| Part | Sections |
|---|---|
| **A** Platform Identity & Strategic Foundation | Platform Identity · Strategic Purpose · Mission, Vision & Core Values · Governance Charter · Authority & Mandate · Organizational Boundary · Core Principles · Strategic Objectives · Success Criteria · Relationship to AIOS Architecture Baseline |
| **B** Organization Architecture | Governance & Compliance Organization · Sub Division · Capability · Team · Role Group · Reporting · **`B7`–`B10`: *"Canonical Section Identity Pending"*** |
| **C** Governance Architecture | Governance Constitution · Decision · Delegation · Accountability · Authority · Review · Escalation · Cross-Platform Governance · `C9` conditional on source baseline · Source Resolution |
| **D** Governance Operations | Operating Model · Executive Governance Interface · Platform Governance Coordination · Decision Operations · Delegation Operations · Operating Rhythm · Collaboration Architecture · Operational Control · Operating Improvement · Operating Success |
| **E** Performance Architecture | Performance Constitution · Model · Measurement · KPI & Success Metrics · Review · Governance · Reporting · Improvement · Maturity Model · Success Constitution |
| **F** Lifecycle Architecture | Lifecycle Constitution · Model · States · Transition · Change Governance · Review · Control · Implementation · Improvement & Maturity · Success |
| **G** Platform Integration | Integration Constitution · `G2` · Cross-Platform Dependency Architecture · Governance Integration · Compliance Integration · Certification Integration · Shared Governance Services · Integration Contracts · Cross-Platform Integration Review · Integration Success |
| **H** Platform Evolution | Evolution Constitution · Model · Drivers · Change Architecture · Decision Governance · Review · Control · Implementation · Improvement & Expansion · `H10` unresolved in source |

**`B7`–`B10` carry the literal title *"Canonical Section Identity Pending"***, and
`C9` and `H10` are unresolved in the body itself. This **corroborates `E-22`
from the source side**: `B2`–`B10` were recorded `NOT FROZEN — SOURCE GATE
BLOCKED`, and the body shows exactly that. **The volume is internally incomplete,
and that incompleteness is the source's, not this record's.**

### 1.2 What is supplied, frozen, and blocked

- **`E-21`, corrected 2026-09-05** — **the 80 section bodies EXIST; 0 are resident.** Cycle 6 recorded *"0 supplied, 0 resident"* from `ACT-CC-P6-070`, which had counted only the four control artifacts before it. A source-recovery pass under `ACT-CC-P10-C7 §8` located **all eight Part bodies** and verified them: `A`–`H`, **80/80 section identities present, 3,704,607 bytes** (`E-20`). The four control artifacts remain what that Act said they were — prose references and an empty template. **What is absent is residency, not the bodies**, and residency is a Founder supply act (`E-29`, `ESC-C7-01`).
- **`E-22`** — **`B2`–`B10` declare `NOT FROZEN — SOURCE GATE BLOCKED`** (`ACT-CC-P6-071 §2`). PD-03 is the only one of the two assessed volumes carrying a `NOT FROZEN` state.
- **`E-26`** — *"Platform Encyclopedia Volume 3"* is **CITATION ONLY relative to this repository**.

### 1.3 Ownership boundary toward PD-04 — stated from PD-03's own side

`ACT-CC-P6-071 §12` (`E-25`) records PD-03's supplied corpus stating:

> `B1 §11` — *"PD-03 tidak menjadi organizational owner atas: … **Knowledge & Intelligence** …"*
> `B1 §12` — lists **`PD-04 Knowledge & Intelligence`** as a cross-platform interface

**Conflict with PD-04's own statement: NONE.** This is the first cross-platform
ownership boundary in this corpus evidenced **from both sides independently** —
every other relationship recorded here is stated from PD-02's side alone.

## 2. What the resident evidence establishes and does not

79 statements were counted from the frozen `PD-02` corpus, and almost all of them
describe PD-03 **from PD-02's side**: what PD-02 may not do to Governance
Authority. That is real evidence of PD-03's authority **boundary**, and it is
not evidence of PD-03's internal structure.

**Materially extended 2026-09-05.** `ACT-CC-P6-070` and `ACT-CC-P6-071` add
structural and ownership evidence stated from PD-03's *own* side — §1.1–§1.3
above. **The count of 79 measured only the `PD-02` corpus and was never a measure
of all resident PD-03 evidence.**

**Evidenced:** identity · domain · the existence of a Governance Authority
distinct from Architecture Authority · PD-02's advisory-only posture toward
governance policy · **the 80-section canonical structure** · **the `NOT FROZEN`
state of `B2`–`B10`** · **the ownership boundary toward PD-04**.
**Absent:** all 80 section bodies · capability decomposition · sub-division
structure · teams · roles · change control.

**Evidenced:** identity · domain · the existence of a Governance Authority
distinct from Architecture Authority · PD-02's advisory-only posture toward
governance policy.
**Absent:** capability decomposition · sub-division structure · teams · roles ·
lifecycle · interfaces beyond the PD-02 relationship · change control.

## 3. Derived organizational structure

Adapted from the Kernel spine (`A`–`E`), specialised to a governance-authority
domain. **Derived, not sourced.**

| Part | Derivation for PD-03 |
|---|---|
| **A — Identity & Mandate** | Governance authority over policy, standards, controls and compliance. Distinct from Architecture Authority (`PD-02`) and from Executive direction (`PD-01`) |
| **B — Organization** | Candidate decomposition: policy authorship · standards custody · control definition · compliance assessment. **Derived; no resident source enumerates these** |
| **C — Governance** | The domain's own subject matter. PD-03 both *holds* governance authority and is *subject to* the Constitution and the Governance Decision Register, which are AIOS-wide, not PD-03-owned |
| **D — Operating** | Policy lifecycle: draft → review → decide → publish → supersede. Mirrors the Register's append-only discipline. **Derived** |
| **E — Performance** | Compliance measurement against published standards. **Derived** |

## 4. Ownership and authority — a distinction that must not collapse

**Governance Authority ≠ the Governance Decision Register.** The Register is an
AIOS-wide instrument that *records* decisions and *"carries no independent
governance authority"* by its own Authority Disclaimer. PD-03 holding governance
authority does not make PD-03 the owner of the Register, and no resident source
says it does.

**Governance ≠ Execution** (`§13`). PD-03's domain is policy and control
definition. Enforcement executed inside another division's domain remains that
division's execution.

## 5. Unresolved

| | |
|---|---|
| **Binding** | No resident source states *"PD-03 is the Governance Authority."* The authority is named; the binding to the CPID is not — the same pattern as `G-03` for Security. **Not asserted here** |
| **Relationship to the Constitution** | Whether PD-03's governance authority sits under, beside, or partly over the Engineering Constitution is **UNKNOWN**. Constitutional tier is Architect-exclusive (`§3.1`), so this is a boundary question requiring authority |
| **Compliance scope** | Whether "compliance" means internal conformance, external regulatory, or both — **UNKNOWN** |

## 6. Not constructed

No governance authority declared or bound. No relationship to the Constitution
asserted. No enforcement mechanism designed — that would cross into execution.
Nothing canonicalized or frozen.


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

### Specific to `PD-03`

- **`Policy` is placed, not excluded.** `Domain Model §9`: *"**Policy** as a
  top-level entity — **modeled as a category of Knowledge**."* PD-03's canonical
  domain (*Policy · Standards · Approval · Control · Certification · Compliance*)
  therefore has a canonical representation: Knowledge items, homed to a Division,
  entered only via governed promotion (inv. 8). **No `Policy` entity may be
  constructed** — `Freeze §4`: *"No new entity."* `E-80` recorded the exclusion;
  `E-92` supplies the mapping it missed.
- **`Permission` is likewise a reserved concept with no ratified entity.**
- **Sub Divisions deferred by `A6`** to *"later architecture layers"* now meet
  `Domain Model §8`'s three-level Spine: a Sub Division would be a **fourth
  level**, behind an architectural decision.
