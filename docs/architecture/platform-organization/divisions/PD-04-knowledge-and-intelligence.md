# PD-04 — Knowledge & Intelligence

> **Status: DERIVED.** Constructed under `FDE-P10-FRONTIER-02`, Decision A.
> Below the Established section is bounded derivation, **not canonical**.

| | |
|---|---|
| **CPID** | `PD-04` — permanent |
| **Established name** | Knowledge & Intelligence |
| **Established domain** | Knowledge domain |
| **Primary construction target** | Knowledge assets, repository, semantics, context |
| **Maturity** | EVIDENCE-READY → **CONSTRUCTED (derived)** |

---

## 1. Established (source constraint)

- Frozen `PD-02 A4:282` — domain label **Knowledge**, PD-02 owns it not.
- **`Volume 4 C3`** *(mis-attributed until 2026-09-05 — see below)* — *"PD-05 sebagai consumer Knowledge"*: Runtime consumes Knowledge, placing PD-04 in a **provider** relation to at least one other division.

> **Citation corrected 2026-09-05.** This statement was cited here, and in two
> other places, as **Frozen `PD-02`** evidence. **It is not in PD-02's corpus** —
> zero occurrences across `volume-1` and `volume-2`. Its actual source is
> **PD-04's own `Volume 4 Part C`, section `C3`**, confirmed both in the
> recovered body and independently at `ACT-CC-P6-071:188`, which cites it as
> `C3`. The error originated in the original `FDE-P10-FRONTIER-02` construction
> (commit `9c96ab3`) and survived ten cycles.
>
> **The correction downgrades the citation's standing**, and that matters:
> *frozen resident PD-02* is the strongest evidence class this corpus has;
> *non-resident PD-04* is among the weakest. **The statement is real; its
> authority was overstated.**
>
> **It also weakens the relationship claim.** `A1` names `Runtime` as a primary
> dependency and `C3` calls PD-05 a consumer — **both from PD-04's own corpus.**
> This is PD-04 describing both directions of its own relationship, **not two
> independent sides corroborating each other**, which is what the PD-03↔PD-04
> boundary (`E-25`) genuinely is.
- `MASTER_ROADMAP §5`; `PD-01 C10:86` — own domain success criteria.
- **84 statements counted from the frozen `PD-02` corpus** — the largest such base of the eight, and the only division carrying that corpus's sole interface and lifecycle statements. **That count measured `PD-02` only; §1.1–§1.4 below are the far larger PD-04 evidence base, harvested 2026-09-05.**

### 1.1 Declared identity — the first evidenced authority statement outside PD-02

`ACT-CC-P6-071 §2` (resident, 567 lines) records PD-04's supplied Part A
declaring, verbatim:

```text
Platform Authority     : Knowledge Authority
Primary Responsibility : Knowledge, Context, Intelligence Assets
Primary Dependencies   : AI Engineering, Runtime
```

**This is materially different in kind from every other division's evidence**
(`E-24`). Elsewhere in this corpus, authority is described from PD-02's side —
what PD-02 may *not* do. Here a division's own corpus **declares its authority,
its responsibility and its dependencies**. `PD-04` is the only one of the eight
for which that exists.

**Two consequences, and one non-consequence:**

- It supplies the corpus's **first positive inter-PD dependency statement** — `AI Engineering` and `Runtime`, i.e. `PD-06` and `PD-05`. `G-05` recorded that *"no positive dependency is evidenced anywhere"*; that is **no longer true**, and `G-05` is updated accordingly.
- It supplies an **authority name** — `Knowledge Authority` — parallel to the `Governance Authority` and `Security Owner` roles named for other domains.
- **It does not bind that authority to the CPID by this record's act.** The corpus declares it; recording a declaration is evidence, not assignment (`§19` of the operative event). The `G-03` pattern — role named, binding open — is **not** repeated here only because the declaration is PD-04's own; whether that constitutes binding is **not decided here**.

**What is absent from the responsibility list is recorded as carefully as what is present:** *"Language Intelligence, and any phase."*

### 1.1a Canonical identity — **read from the source body**, 2026-09-05

`Volume 4 Part A`, section `A1 — Platform Identity`, declares:

```text
Platform ID        : PD-04
Platform Name      : Knowledge & Intelligence
Platform Authority : Knowledge Authority
```

matching the same header family as `PD-03 A1` and frozen `PD-02 A4`. **`E-24`'s
declaration, previously known only through `ACT-CC-P6-071`'s report of it, is now
read directly from the body.**

Part C's ten section titles, read from source: Knowledge Architecture
Constitution · Knowledge Model Architecture · Knowledge Asset Architecture ·
Knowledge Repository Architecture · Knowledge Semantic Architecture · Knowledge
Graph Architecture · Context Knowledge Architecture · Knowledge Integrity &
Governance Interface · Knowledge Evolution & Improvement · Knowledge Architecture
Success.

**Part B carries a second, interleaved series `B01`–`B06`** whose titles are
constraint statements rather than section subjects: *"No Cross-Team Ownership
Without Delegation"* · *"Dependency Does Not Create Ownership"* · *"Consumer Does
Not Become Owner"* · *"Quality Does Not Become Domain Owner"* · *"Evolution Does
Not Become Uncontrolled"* · *"Workforce Does Not Redefine Boundary"*.

**Those six are the same distinctions this corpus has been enforcing** —
`Dependency ≠ Ownership`, `Collaboration ≠ Control` — stated independently inside
PD-04's own volume. They were derived here from `MASTER_ROADMAP §5` and PD-02's
frozen text; PD-04 states them natively. **Convergent, not copied.**

`A1`'s Canonical Status block adds, verbatim:

```text
CPID                 : PD-04
AUTHORITY            : Knowledge Authority
PRIMARY DOMAIN       : Knowledge, Context, Intelligence Assets
SOURCE-FIDELITY MODE : Bounded Canonical Synthesis
SOURCE SUPPORT       : Strong for Identity · Bounded for Constitutional Framing
UNSUPPORTED AUTHORITY: NONE IDENTIFIED
BOUNDARY EXPANSION   : NONE IDENTIFIED
FREEZE DECISION      : APPROVED
```

**`CPID: PD-04` is stated explicitly** — the only division besides PD-02 whose own
corpus names its CPID in an identity block.

**`SOURCE-FIDELITY MODE: Bounded Canonical Synthesis`** is the source declaring
its own construction method, and **`SOURCE SUPPORT: Strong for Identity ·
Bounded for Constitutional Framing`** is it grading its own evidence. Together
with `UNSUPPORTED AUTHORITY: NONE IDENTIFIED` and `BOUNDARY EXPANSION: NONE
IDENTIFIED`, the volume runs the same checks this corpus runs — **authority not
claimed beyond evidence, boundary not widened by construction.**

**Provenance:** the source body is **NOT RESIDENT** (`ESC-C7-01`).

### 1.2 The supplied corpus — 30 sections, and its freeze state

`ACT-CC-P6-071 §2` (`E-23`): **30 / 30 sections accounted for** across 3 files,
**102,540 lines / 1,508,896 bytes**, with 56 section-ID declarations resolving to
30 distinct sections (26 declared twice).

| Part | Sections | Subject |
|---|---|---|
| **A** | `A1`–`A10` | Platform Identity · Strategic Purpose · Mission/Vision/Values · **Knowledge & Intelligence Charter** · **Knowledge Authority & Mandate** · Organizational Boundary · Core Principles · Strategic Objectives · Success Criteria · Relationship to AIOS Architecture Baseline |
| **B** | `B1`–`B10` | Organizational Model · Sub Division · **Capability** · Team · Role Group · Reporting · Interface · Coordination · Governance · Organizational Success |
| **C** | `C1`–`C10` | **Knowledge Architecture Constitution** · Knowledge Model · Knowledge Asset · **Knowledge Repository** · **Knowledge Semantic** · **Knowledge Graph** · **Context Knowledge** · **Knowledge Integrity & Governance Interface** · Knowledge Evolution · **Knowledge Architecture Success** |

Declared freeze state: **23 FROZEN · 2 Bounded Canonical Synthesis · 2 Bounded
Canonical Reconstruction · 1 FROZEN WITH QUALIFICATION · 2 unstated.** *"No
`NOT FROZEN` section exists in PD-04"* — unlike PD-03, whose `B2`–`B10` are
`NOT FROZEN — SOURCE GATE BLOCKED`.

**Part `C` is the structural difference from PD-03**: ten sections of Knowledge
architecture, where PD-03's volume contains none.

**None of the 30 bodies is resident — and all 30 exist.** A source-recovery pass
under `ACT-CC-P10-C7 §9` located the three Part files and verified them:
**30/30 section identities present, 1,508,896 bytes — an exact match to the byte
total `ACT-CC-P6-071 §2` recorded** (`E-23`). This record inventories the corpus
and reconstructs nothing. **Residency is a Founder supply act** (`E-29`,
`ESC-C7-01`).

### 1.3 Ownership boundary toward PD-03 — evidenced from both sides

`ACT-CC-P6-071 §12` (`E-25`):

> `C8` — *"**PD-04 owns Knowledge Integrity** within the Knowledge & Intelligence domain. **PD-03 owns Governance & Compliance** and provides certification/compliance"*
> `C8 §36` — routes certification criteria through PD-03, with PD-04 supplying evidence

Against PD-03's own `B1 §11`/`B1 §12`. **Conflict: NONE.** Tested independently
by that Act and consistent from both directions.

### 1.4 What the assessment expressly refused

`ACT-CC-P6-071 §12` tested and **rejected** the proposition *"PD-03 says PD-04
owns Knowledge & Intelligence, therefore PD-04 defines Phase 6"*: PD-04 holds
**Knowledge Authority, not phase authority.** Recorded here because the same
inference — domain ownership read as programme authority — is exactly the
conflation this corpus is built to avoid.

## 2. What distinguishes this division

PD-04 is the one division whose domain has both **substantial resident
architecture** (`native_core/core/knowledge/`, the Knowledge Admission Model,
`KNOWLEDGE_ADMISSION_BLOCKER_REGISTER`, `GDR-0028`'s T-12 ratification of the
Phase 3.289 Knowledge Admission Model) **and** an evidenced consumer relation.

That makes it the strongest candidate for a genuine interface map — and the same
caution applies as for PD-05: **the resident Knowledge subsystem is a frozen core
boundary, not PD-04's property.** No source binds them, and none is asserted.

## 3. Derived organizational structure

| Part | Derivation for PD-04 |
|---|---|
| **A — Identity & Mandate** | Knowledge domain: assets, repository, semantics, context |
| **B — Organization** | Candidate decomposition from the four construction targets: asset custody · repository · semantic model · context provision. **Derived** |
| **C — Governance** | The Knowledge domain is already governed by a ratified admission model — governed **human decision**, no automatic arbitration, fail-closed on conflict (`Phase 3.289`, `GDR-0028`). PD-04's governance must sit **inside** that, not replace it |
| **D — Operating** | Admission pipeline: candidate → conflict detection → governed decision → Active version → supersession. Taken from the ratified model, cited as **canonical evidence of the domain**, not as PD-04's charter |
| **E — Performance** | Admission throughput, conflict resolution latency, currency of Active versions. **Derived** |

## 4. Boundary notes

**Knowledge ≠ Memory.** Both are separate frozen core boundaries. The
memory→knowledge promotion path is governed and human-decided; PD-04's domain is
Knowledge, and nothing extends it over Memory.

**Provider ≠ owner of the consumer.** *"PD-05 sebagai consumer Knowledge"* (`Volume 4 C3`, non-resident — see §1 citation correction)
establishes a dependency, and `§13` is explicit: `Dependency ≠ Ownership`.

## 5. Unresolved

Binding to the Knowledge subsystem · whether "Intelligence" in the name denotes a
second domain (the P5 Intelligence Ecosystem) or qualifies Knowledge — **UNKNOWN,
and material**: if two domains, the decomposition above is incomplete · capability
decomposition · sub-division structure.

## 6. Not constructed

No binding to `native_core/core/knowledge/`. No change to the ratified admission
model. No claim over Memory. No resolution of the Knowledge/Intelligence scope
question. Nothing canonicalized or frozen.
