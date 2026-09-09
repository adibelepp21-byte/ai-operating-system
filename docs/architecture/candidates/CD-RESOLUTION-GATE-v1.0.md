# CD-1 – CD-4 Authority & Evidence Resolution Gate — Result v1.0

> **Act:** `ACT-CC-CANONICAL-ARCHITECTURE-AUTHORITY-EVIDENCE-RESOLUTION-GATE-v1.0`
> **Executed:** 2026-09-09 · **Baseline:** `bd55316`
> **Subject:** the four contradictions raised by `CANONICAL-ARCHITECTURE-CANDIDATE-AUDIT-v1.0.md`
>
> **This gate adopts nothing.** `§2`: not a revision Act, not an adoption Act,
> not a P10 Act. The candidate is **unchanged** (`§15`).

---

## A. GUARD RESULT (`§4`)

`§4` requires the guard to be **probed**, not merely present. A live probe wrote
one file with a deliberately broken citation into a protected path and one into
an audit root, in the same run:

| Direction | Expectation | Measured |
|---|---|---|
| Protected content → **not read** | 0 findings sourced from `docs/program/` | **0** |
| Authorized new work → **not omitted** | the untracked probe is caught | **1 ERROR raised on it** |

Both probes deleted; untracked count back to **13**. **No conclusion in this
report rests on a scanner whose effective scope was not demonstrated.**

### A.1 The actual protection rule (`§5.2`) — policy, stated separately from state

| | |
|---|---|
| **PROTECTED PATH POLICY** | An **untracked** file under `docs/program/` is refused. Tracked files there are read normally. Determination fails **closed** if tracked status cannot be established |
| **CURRENT UNTRACKED FILE STATE** | **13** untracked `AIOS_*` packages under `docs/program/`; **73** tracked files there; **0** untracked files anywhere else |

**The earlier generalization — "`docs/program/` is protected" — is not repeated.**
It described the state as though it were the policy. The Blueprint, both
Roadmaps and `SG-01` are tracked, and **this gate's conclusions depend on
reading them.**

---

## B. INFRASTRUCTURE CORRECTIONS (`§5`)

### B.1 `§5.1` — the governance root **can** affect this gate, and was corrected

The evidence for all four contradictions turned out to live substantially in
`docs/governance/` — the Governance Decision Register, `G1′`, and the External
Corpus Synchronization Ledger. The auditor's roots excluded it.

**Root added.** Default run went from 25 documents to **68**, and citations
checked from 222 to **622**.

### B.2 `§5.1` — 10 ERRORs surfaced, and **all 10 were miscalibrated severity**

| Cited | Classification | Basis |
|---|---|---|
| `extract.py`, `llm.py`, `watch.py`, `requirements.txt`, `setup.py`, `factory.py` | **external corpus** | Graphify archive at Intake (`E-66`) |
| `AIOS_COFOUNDER_DELEGATION_CHARTER_v1.0.txt` (×2) | **non-resident supplied upload** | `ESC-C5-01`; disclosed at `ACT-CC-P6-070 §2.1` |
| `scripts/check_dependency_boundaries.py` | **external repository** | `EAI-0001` = `1jehuang/jcode` (`GDR-0012`). **Verified: this basename has never existed anywhere in this repository's history, and `dd8755f7` is not a commit here** |
| `docs/architecture/adr/decisions/ADR-NNNN.md` | **template route** | `NNNN` is a literal placeholder; the ADR naming convention |

**Errors 10 → 0. Zero corpus defects.**

**The registry was restructured so it cannot silence anything.** It is now
consulted **only on the resolution-failure branch**, so a generic key like
`setup.py` can never mask a citation that resolves. A test asserts this
structurally by reading the source order of `audit()`.

**45 WARNs remain and were deliberately left.** All are the ambiguous
bare-basename class — a section letter-number filename, or a module name that
several packages share. `§5.3` states a basename match alone is insufficient
evidence — **WARN is the correct severity, and resolving them away would be the
error.**

**A note on how this paragraph is written.** An earlier draft named two example
basenames in backticks and **the auditor flagged the report itself**, correctly:
prose that quotes a bare basename is indistinguishable from prose that cites
one. The prose was changed rather than the detector, per the rule that evidence
controls the detector. **A report about ambiguous citations should not contain
ambiguous citations.**

### B.3 `§5.2`/`§5.3`/`§5.4` — disposition

- **`§5.3`** — every citation in this report gives **exact path**, and where two
  documents share the name "Roadmap" the **filename and section count** are
  stated. The 17-section Master Roadmap and the 37-section Gap Closure Roadmap
  are never referred to as "the Roadmap".
- **`§5.4`** — one stale test of mine was **narrowed, not deleted**, with the
  date and reason in its docstring; the prior finding it encoded stays
  traceable. `§53.4`'s superseded claim remains standing under a correction
  banner. **No original finding was erased.**
- **`§52.1` is falsified.** It reclassified the ERROR-severity item as
  `NO DEFECT IN SCOPE`, partly because its evidence supposedly lay behind a
  protected boundary. **There was a defect, it was in scope, and the boundary
  was never in the way — the audit root was simply wrong.**

---

## C. CD-1 RESULT — the layer model

### C.1 What the source actually says (`§7` Q1–Q3)

| Field | Value |
|---|---|
| **Authoritative layer model** | The **ten-layer model**, `AIOS_ARCHITECTURE_FREEZE_v1.0.md §5` |
| **Source status** | **FROZEN and enumerated as frozen.** `Freeze §2`, tagged `[E]`: *"**Frozen by this document** (the ratified canon): … **Layers** — the ten-layer model (§5)"* |
| **Authority** | Architect-authorized (Phase 2). `Freeze §1`: after the freeze, *"architectural change requires formal governance"* |
| **Originating document** | `Freeze §11` `AD-4`: *"Ten-layer model — Architecture Specification"* |
| **Supersession** | **None found.** No ADR and no later source amends it |

### C.2 The finding that changes the classification (`§7` Q4–Q7)

**A Founder Decision has already ruled on this exact question.** `G1′`
(`AIOS_FOUNDER_DECISION_G1_PRIME_RATIFICATION_v1.0.md:178`, echoed at
`AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md:199`):

> *"Boundary/layer enumerations (**ten layers, eleven modules, nine boundaries,
> eight layers**) — Multiple **projections** of one model, expressly permitted by
> Canonical Domain Model §8. **Not competing taxonomies and not a conflict.**"*

**And the specific divergence is already on the record as an open item.**
`S-4`, External Corpus Synchronization Ledger, under the same Founder decision:

> *"Master Program **Volume I Pasal 3** — Record the divergence identified during
> validation: **Pasal 3's eight-layer chain omits Capability and Workflow**,
> which Architecture Freeze §5 carries as **frozen layers 4 and 6**."* — Status: **Open**

**Three things follow, and they were all determinable from resident evidence.**

1. **The candidate's eight-layer chain is Master Program Volume I `Pasal 3`'s.**
   That independently confirms `PR-1`: the sequence did not come from the
   Engineering Constitution, which has no such section.
2. **A differing layer *count* is not a conflict** — `G1′` says so, on the
   warrant of `Canonical Domain Model §8` (*"separate, later artifacts that will
   be **projections** of this model, not extensions to it"*).
3. **But omitting Capability and Workflow is a recorded divergence**, already
   identified during `G1′` validation, and the required synchronization runs
   **toward the Freeze**: the Master Program is to record the divergence, not
   the Freeze to yield.

**Capability and Workflow are mandatory** (`§7` Q5): both are among the twelve
frozen entities (`Freeze §4`), both are frozen layers (`§5`), and `INV-1`,
`INV-9`, `INV-10`, `INV-13`, `INV-14` are stated in terms of them. **A layer
model without them cannot express invariants the Freeze declares binding.**
`G1′` separately fixes *"Capability standing — a **first-class canonical
entity** … carrying invariants 1, 9, 10, 11, 14"*.

### C.3 `§7` Q6 — Optimization, separately

**Not a rename in the sense the audit implied.** `Freeze §5` layer 10
Optimization is a *governed learning loop* whose output is **"proposals only"**,
forbidden from *"deciding governance (PR-3)"* and *"auto-promote (INV-8)"*. The
candidate's layer 7 *"Intelligence Improvement — reasoning/**model
improvement**"* is broader and carries none of those constraints — and
**`Freeze §2` lists "Model-optimization" as explicitly OUTSIDE the freeze**,
`§10` Architect-reserved.

**So the candidate names deferred architecture as a layer.** `[O]` — recorded,
not resolved, and not escalated: it changes nothing until a revision is
authorized.

### C.4 Verdict

```text
CD-1 RESOLVED — CANDIDATE CORRECTED BY EVIDENCE
```

**The ten-layer frozen model governs.** Capability and Workflow are frozen
layers 4 and 6 and must appear. A different *count* is a permitted projection
(`G1′`); *omitting these two* is a divergence already recorded as `S-4` Open.

**Correction to my own audit, disclosed:** `CD-1` was reported as a **newly
discovered contradiction requiring Architect ratification**. It is neither new
nor Architect-reserved — it is a **pre-existing, Founder-acknowledged open
synchronization item**, and the audit did not find it because the record that
carries it sits in the root the auditor could not see (`B.1`). **The
observation was right; its novelty and its severity were both wrong.**

---

## D. CD-2 RESULT — the document hierarchy

### D.1 What `Constitution §4` defines (`§8` Q1–Q2)

`docs/constitution/engineering-constitution-v1.md §4` *Governance Artifact
Relationship* names **five artifacts**: this Constitution → Canonical Domain
Model → ADR Framework → Principle Documents → Glossary, closing with
*"Authority flows downward."*

**It is a named-artifact hierarchy scoped to repository artifacts**, not an
exhaustive taxonomy of document classes. `G1′` states its scope in those exact
terms: *"Governing precedence scheme **for repository artifacts** — Engineering
Constitution §4"*.

### D.2 What establishes the candidate's six classes (`§8` Q3–Q5)

**`S-3`, again in the `G1′` synchronization ledger:**

> *"Master Program **Volume I Pasal 7** — Record that, **for repository
> architecture**, Pasal 7's precedence table is **not an independent
> constitutional source**; repository artifact precedence is Engineering
> Constitution §4."* — Status: **Open**

**The candidate's six-class hierarchy is `Pasal 7`'s precedence table**, and its
disposition was settled by `G1′`: it is not an independent constitutional source
*for repository architecture*, while **its role within the Master Program corpus
is unchanged** (`Register:182`, same determination for the sibling document).

### D.3 `§8` Q4 / Q6 — the two are compatible; the attribution is not

**The taxonomies do not compete.** One governs **repository artifact
precedence** (five artifacts); the other is the **Master Program corpus's**
document-class ordering (six classes). Each is authoritative in its own scope,
and `S-3` says exactly that.

**The defect is the attribution, not the content.** The candidate says *"The
surviving **Constitution** establishes six document layers"* at status
`CONFIRMED`. **The Constitution establishes no such thing.** This is a
provenance error of the `PR-1` class, not a contradiction between authorities.

### D.4 Verdict

```text
CD-2 RESOLVED — AUDIT FINDING WAS INCORRECT
```

**No constitutional interpretation was required, and none was made** (`§8`
closing rule). The question was settled by an existing Founder decision plus the
scoping language already in `Constitution §4` and `G1′`.

**Correction to my own audit, disclosed:** `CD-2` was classified
`CONTRADICTION — CONSTITUTIONAL` and routed to Founder ratification. **It is a
mis-citation inside the candidate, resolvable without any authority input.**
I compared two hierarchies without first asking whether they addressed the same
subject — `§11` requires exactly that check, and the audit skipped it.

---

## E. CD-3 RESULT — the entity roster

### E.1 The canonical entity set is settled (`§9` Q1–Q2)

| Source | Statement |
|---|---|
| `Constitution` Appendix A | *"**Organization, Department, Capability, Agent Definition, Agent Instance, Skill, Workflow, Tool, Runtime, Knowledge, Memory, Trace** — defined exclusively in the Canonical Domain Model."* — **twelve** |
| `Freeze §4` | *"The **twelve** ratified entities, in four categories … **No new entity.**"* |
| `G1′` / `Register:194` | *"Canonical entity set — Canonical Domain Model §1: **twelve entities in four categories**."* — **Founder-decision level** |

### E.2 The three disputed names, searched across the whole corpus (`§9` Q4–Q5)

| Name | Files in corpus | What it actually is |
|---|---:|---|
| **Execution Contract** | **10** | **An implementation artifact.** `AIOS_PHASE_RECONCILIATION_v1.0.md:32` maps it to `runtime/contract.py`, `runtime/execution/contract.py`. It is also the **Phase 3 name**. **Nowhere in the corpus is it called an entity** |
| **Memory Record** | **2** | Only the candidate and this audit. **No independent corpus support** |
| **Knowledge Node** | **3** | Only the candidate, this audit, and the execution record quoting them. **No independent corpus support** |

**A correction to my own audit:** it implied all three were unsupported.
**`Execution Contract` is real** — as an implementation artifact and a Phase
name. That does not make it a Domain Model entity, but the audit's phrasing
overstated the finding.

### E.3 What `§6.2` invariant 3 prohibits (`§9` Q3, Q7)

> *"No document other than the Canonical Domain Model may **introduce, redefine,
> or contradict** a Domain Model entity, relationship, or invariant."*

The candidate presents the six names under **§3.2 "Domain Model and Ownership"**,
opening *"Core AIOS entities must have one canonical domain model."* **They are
presented as canonical domain entities.** Presenting `Execution Contract`,
`Memory Record` and `Knowledge Node` in that frame is **introducing Domain Model
entities outside the Domain Model** — the precise act invariant 3 forbids.

**The audit's interpretation is correct** (`§9` Q8), and is now additionally
supported at Founder-decision level by `G1′`'s twelve-entity determination.

### E.4 Verdict

```text
CD-3 NARROWED — MATERIAL AUTHORITY QUESTION REMAINS
```

**`§9`'s mandatory constitutional safeguard controls.** Adoption in the current
form would breach `§6.2` invariant 3, so the contradiction **must remain
unresolved** until the authority question is legitimately settled. **The
invariant was not reinterpreted to accommodate the candidate, and the
candidate's entities were not redefined to avoid the contradiction.**

**What evidence did settle** — and what therefore leaves the Founder's desk:
the three names are **not Domain Model entities today**, and the canonical set
is **twelve**. **What remains reserved** is only whether the Founder intends to
propose any of them *as* entities, which `Constitution §3.4` routes through an
ADR and `§3.2` makes non-delegable.

**NARROWED ≠ RESOLVED** (`§3`). It is recorded as narrowed.

---

## F. CD-4 RESULT — "Department"

### F.1 What FD-6 / GDR-0020 establish (`§10` Q1–Q4)

`GDR-0020`, **2026-08-15**, decided by **Founder**, decision text verbatim:

> **"FD-6 = OPTION A — PLATFORM DIVISION IS THE CANONICAL ORGANIZATIONAL UNIT"**

| Field | Value |
|---|---|
| Decision status | **DECIDED** |
| Canonical organizational unit | **Platform Division** |
| Domain Model mutation | **NOT EXECUTED BY THAT ACT** (executed later via `ADR-0010`, `ADR-0011`) |
| Scope boundary | Does **not** authorize renaming every occurrence of "Department"; **no historical rewrite** |

`canonical-domain-model-v1.md` — the **sole semantic authority**
(`Constitution §5`) — records the result: *"**Department** is its recorded
**historical alias** … There `Department` denotes **the same entity** and is
historical terminology, not current canonical terminology."*

**Deprecated? No. Replaced? No. Aliased? Yes — same entity, historical term.**

### F.2 How the candidate uses it (`§10` Q5–Q6)

**Definitionally and currently**, not historically: §17 is titled
*"DEPARTMENT AND ORGANIZATION ARCHITECTURE"* and defines Department from
Volume VII. And §14 asserts:

> `PD ≠ Department automatically`

**That directly negates the Domain Model's "denotes the same entity."**

**Chronology resolved first, as `§10` requires:** Volume VII predates `FD-6`
(2026-08-15). The candidate reproduces pre-decision terminology — **it was not
wrong when written; it is wrong now.**

### F.3 Verdict

```text
CD-4 RESOLVED — CANDIDATE CORRECTED BY EVIDENCE
```

**Platform Division is canonical by Founder decision.** `PD ≠ Department
automatically` is contradicted by the sole semantic authority and must be
corrected at revision.

**Two safeguards honoured.** Department was **not restored** to current status
merely because older documents use it; and it was **not removed** merely because
a later document differs — `FD-6` is a decision, not a change of fashion.
**`FD-6 §3` and `GDR-0020 §3` mean the candidate may still *quote* "Department"
historically** (including the Master Program's phase name *"P10 Department
Ecosystem"*). What it may not do is **define** with it.

---

## G. AUTHORITY MATRIX — H-1 … H-5 (`§12`)

**None was forwarded to the Founder without first testing it against resident
evidence. Three of the five come off the desk.**

| ID | Question | Disposition | Evidence |
|---|---|---|---|
| **H-1** | Does the candidate inherit `GDR-0001`/`G1′`? | **REQUIRES FOUNDER — narrowed** | `Register:182` attaches the determination to a document with **`ARB-002`-ratified `§3.1`–`§3.4` dependency principles**. The candidate has no such sections and never cites `ARB-002`. **Inheritance-by-default is evidence-refuted;** only affirmative designation is reserved |
| **H-2** | Does an original exist outside this repository? | **SOURCE DEPENDENCY** | See `H` below — evidence proves one existed and partially identifies its contents |
| **H-3** | Which layer model governs? | **EVIDENCE RESOLVED** | `Freeze §2` freezes the ten-layer model by enumeration; `S-4` records the divergence as Open; `G1′` rules counts are projections. **Off the Founder's desk** |
| **H-4** | Are the three names real entities? | **REQUIRES FOUNDER — narrowed** | Evidence settles that they are **not entities today** (`E.2`). Only *proposing* them is reserved, and `Constitution §3.4` routes it through an ADR |
| **H-5** | Does "Department" remain live? | **AUTHORITY RESOLVED** | `FD-6`/`GDR-0020`, **DECIDED**, Founder. **Off the Founder's desk** |

---

## H. SOURCE GAP REGISTER (`§13`) — genuinely unrecoverable only

### `SG-01` — the original canonical architecture body

| `§13` question | Answer |
|---|---|
| **1. Does surviving evidence prove an original existed?** | **Yes.** `G1′` validation quotes and rules on its **SSOT statement, `§1`, `§2.1`, `§7`, `§14`** (`S-5`, `S-6`), its **`ARB-002`-ratified `§3.1`–`§3.4`** (`Register:182`), and its **`§9`, `§10`**. `Master Program Pasal 7` names it Layer 2 Canonical; `E-52` places it in the same layer |
| **2. Does evidence identify its location?** | **No.** `SG-01`: *"has never existed in this repository's history."* It was validated from outside this repository |
| **3. Does any reference identify its contents?** | **Partially, and specifically.** It declared itself SSOT for *Entity, Ownership, Dependency, Lifecycle, Relationship*; it treated **Trace as a Memory sub-entity** (corrected by `S-5`); it carried an **open Agent Instance status conflict** at `§7`/`§14` (superseded by `S-6`); and its `§3.1`–`§3.4` dependency principles **remain Founder-ratified** |
| **4. Has an actual original been recovered?** | **No.** |

```text
ORIGINAL NOT RECOVERED        ← current state
ORIGINAL NEVER EXISTED        ← NOT established; the evidence points the other way
```

**This is a materially stronger position than `SG-01` last recorded.** At least
**nine sections of the original are identifiable by number**, and the content of
four is partly known from the decisions that corrected them.

### `SG-02` — the 53-section Master Roadmap (`§14`)

**`SOURCE REQUIRED`.** Not reconstructed from conversation, memory, inferred
numbering, the candidate, or citations. **Not needed for any verdict in this
report** — every CD verdict rests on resident sources.

---

## I. CANDIDATE STATUS (`§19 I`)

```text
AUDIT COMPLETE — AUTHORITY INPUT REQUIRED
```

**CD-1, CD-2 and CD-4 are resolved by evidence. CD-3 is narrowed and holds the
candidate.** `§9`'s safeguard keeps it there: adoption in current form would
breach `Constitution §6.2` invariant 3.

**The candidate is byte-for-byte unchanged** (`§15`). No overwrite, no rename,
no claim altered, no contradiction removed.

---

## J. P10 STATUS (`§19 J`, `§17`)

```text
UNCHANGED — P10 BLOCKED
```

**This gate did not reopen P10 and does not propose to.**

### J.1 `§16` NEW VERDICT-SENSITIVE EVIDENCE — reported separately, verdict not altered

**The External Corpus Synchronization Ledger records that the Master Program's
0% figures for Phases 5–9 are superseded by fact**, each against a named,
dated, resident Founder Decision:

| Item | Statement | Certification |
|---|---|---|
| `S-13` | *"Intelligence Ecosystem (Phase 5) — Belum Dimulai / 0%" is superseded by fact* | `FD-P5-001` |
| `S-14` | *"Knowledge Ecosystem (Phase 6) — … 0%" is superseded by fact* | `FD-P6-002` |
| `S-15` | *"Memory Ecosystem (Phase 7) — … 0%" is superseded by fact* | `FD-P7-003` |
| `S-16` | *"Tool Ecosystem (Phase 8) — … 0%" is superseded by fact* | `FD-P8-002` |
| **`S-17`** | ***"Workflow Ecosystem (Phase 9) — Belum Dimulai / 0%" is superseded by fact*** | **`FD-P9-002`** (2026-09-03) |
| `S-9` | *"AI Runtime (Phase 4) — 0%" is superseded by fact* | Gate 4 / `Phase 4.6 CLOSED`, 2026-07-30 |

**`R3`'s supporting figure was wrong.** The `P10 Entry Baseline` recorded
*"Phase 9 stands at 0%"*, sourced from the **26 July snapshot** — the very
figure `S-17` supersedes. **That snapshot was already labelled
`STALE BY DECLARATION` (`E-46`), and I used it anyway.**

**The verdict does not move, and here is why it does not.** `Volume VII §1.2`
conditions P10 on Phase 9 being ***matang*** — **mature**. `S-17` establishes
only that Phase 9 is **not zero**. **NOT ZERO ≠ MATURE.** Per `§3`,
`EVIDENCE FOUND ≠ CURRENT STATE`, and per `§16` a recovered Phase state does not
automatically alter the P10 verdict.

**What changes is the basis, not the conclusion:** from *"Phase 9 is 0%"*
(**false**) to *"Phase 9 maturity is not established"* (**true, and weaker**).
A weaker basis for the same verdict is still a correction, and it is recorded as
one.

**`§16` firewall honoured:** nothing was substituted from the snapshot,
historical review, candidate inference, roadmap inference, or execution state.
The figures above are quoted from resident governance records only.

---

## K. NEXT ACTION (`§19 K`, selected under `§6`)

```text
ACTION   Reconcile the P10 entry baseline against S-9 and S-13..S-17:
         correct the falsified "Phase 4-9 all 0%" figure wherever this
         corpus asserts it, and re-state R3's basis as
         "Phase 9 maturity not established" rather than "Phase 9 is 0%".
CLASS    FIX (self-error correction) — §6 PRIORITY 4
```

**WHY THIS ACTION.** It is the only remaining item that is **verdict-sensitive**
(`§6` PRIORITY 1). A falsified figure is currently load-bearing in the corpus's
central blocking verdict.

**WHY IT OUTRANKS ALTERNATIVES.** The candidate revision (`ACT §13`) is
**PRIORITY 6 hardening** while `CD-3` holds the candidate — revising around an
unresolved authority question is precisely what `§6` forbids. The remaining
`WARN` calibration is non-verdict-sensitive. **No lower-priority work is being
used to avoid the authority question**: `CD-3`, `H-1` and `H-4` are stated
plainly above and are not being worked around.

**WHAT IT CAN CHANGE.** The **stated basis** of `P10 BLOCKED`, and the accuracy
of every Phase figure this corpus carries.

**WHAT IT CANNOT CHANGE.** **The P10 verdict itself** (`§17`), Phase 9 maturity,
`CD-3`, or the candidate's status. **`R3`'s determining condition is untouched.**

---

## §Z — EXHAUSTION (`§21`)

```text
AUTHORITY-BLOCKED + INDEPENDENT EVIDENCE WORK CONTINUES
```

**Not** `NO MATERIAL EXECUTABLE FRONTIER IDENTIFIED`: the `K` action is
executable now. **Not** `EXHAUSTED`: the candidate's non-adoptability is an
authority state, not an exhaustion state. **No work was manufactured** — `K`
corrects a figure this gate proved false.
