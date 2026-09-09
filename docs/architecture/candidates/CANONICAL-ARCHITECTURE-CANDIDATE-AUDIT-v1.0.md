# Canonical Architecture Candidate — Evidence Audit v1.0

> **Act:** `ACT-CC-CANONICAL-ARCHITECTURE-RECONSTITUTION-SUBMISSION-v1.0`
> **Audited:** 2026-09-09 · **Auditor:** Claude Code / Co-Founder
> **Subject:** `AIOS_CANONICAL_ARCHITECTURE_RECONSTITUTED_CANDIDATE_v1.0.md` (same directory)
> **Candidate status, preserved:** `RECONSTITUTED CANDIDATE — NOT YET FOUNDER-RATIFIED`
>
> **This audit does not adopt, ratify, or elevate anything.** `ACT §3`:
> SUBMITTED ≠ VERIFIED ≠ RATIFIED ≠ CANONICAL.

---

## §0 — Guard verification (`ACT §12`), executed before any scan

`ACT §12` requires the protected boundary to be verified **first**, and to fail
closed. Executed in that order:

| Check | Result |
|---|---|
| `ScopeGuardTests` (3 tests, incl. the `VF-10` and `VF-11` regressions) | **OK** |
| Protected set = untracked files under `docs/program/` | **13 files**, all `AIOS_*` packages |
| Protected files read during this audit | **0** |
| `docs/program/` **tracked** files (readable; not protected) | 100+, incl. the Blueprint, both Roadmaps, and `SG-01` |

**A correction to my own prior reporting.** Earlier cycles spoke of
`docs/program/` as protected *as a directory*. **It is not.** The protection is
keyed on **path policy for untracked files** (`VF-11`'s fix), and the tracked
artifacts in that directory — including the `P10–P13 Blueprint` and the
`Gap Closure Roadmap` — have always been readable. Several claims this audit
confirms depend on that, and the distinction is stated here so the confirmations
are not later mistaken for boundary violations.

---

## A. INTAKE RESULT

| Field | Value |
|---|---|
| File received | **Yes** — Founder upload |
| `sha256` (body) | `cf27ac264887ce7a408024c7c5f52b8cb8f6205be4e68a56108e6272caf72397` |
| Size | **29,881 bytes** |
| Line count (newline-only, the rule `sed`/editors/citations use) | **475** |
| Line count (`str.splitlines()`) | **804** |
| Repository location | `docs/architecture/candidates/AIOS_CANONICAL_ARCHITECTURE_RECONSTITUTED_CANDIDATE_v1.0.md` |
| Candidate status | `RECONSTITUTED CANDIDATE — NOT YET FOUNDER-RATIFIED` — **preserved unchanged** |
| Body alteration | **None.** Persisted body `sha256` equals the upload's, exactly |

### A.1 Three structural intake defects — `CORRECTION REQUIRED`, not corrected

Per `ACT §13` the candidate was **not** rewritten. These are recorded for the
Founder's decision.

| # | Defect | Measurement | Consequence |
|---|---|---|---|
| **IN-1** | **329 `U+2028` LINE SEPARATOR** characters | 37 lines carry them | The file's line numbering is **ambiguous by 329 lines**. Any future citation `AIOS_CANONICAL_ARCHITECTURE.md:NNN` resolves to two different places depending on the reader's splitting rule |
| **IN-2** | **All six Markdown tables are collapsed onto single lines** | lines 19, 52, 93, 117, 205, 408 — one is **1,312 characters** long | **No standard Markdown processor will render them as tables.** The document's Status Vocabulary, Layer Semantics, Document Precedence, Phase roster, PD roster, and the entire `UNKNOWN` register are affected |
| **IN-3** | **30 fenced code blocks open and close on the same line**; **32 `U+FFFC`** OBJECT REPLACEMENT characters | | Every architectural diagram in the candidate (layer sequence, execution chain, decision lineage, P13 loop) is a single run-on line. `U+FFFC` marks **32 points where embedded content was lost in export** |

**IN-1 is not cosmetic here.** This programme spent two cycles (`§40`, `§51`)
hardening its tooling against exactly this hazard, and the file it now lands on
is the candidate for the architecture SSOT. **A canonical body whose line
numbers are ambiguous cannot be cited stably.**

**Recommended (not applied):** re-export from the authoring tool with real
newlines before ratification. **Authority:** Founder — it is the submitted
artifact.

---

## B. EVIDENCE COVERAGE

**30 candidate sections audited.** Claims are counted at the level of *material
architectural assertion*, not sentence.

| Class | Count | Examples |
|---|---:|---|
| **CONFIRMED** — directly supported by a surviving authoritative source | **9** | PD roster (§12), external-repo roster (§21), connective systems (§9), execution chain (§8), state model (§10), recoverability boundary (§25), PD-01 reference-implementation role (§13), CPID rule (§12.1), P13 evolution loop (§19) |
| **SUPPORTED** — supported in substance, wording not reproducible | **6** | native-system identity (§1), governance supremacy (§3.4), boundary principles (§12.2), change control (§20), integrity principles (§22), integrity loop (§23) |
| **RECONSTITUTED** — structurally built from evidence; review required | **4** | layer semantics table (§2.2), domain-model partial (§5), control/execution boundary (§15), P12 integration (§18) |
| **UNKNOWN / UNSUPPORTED IN SCOPE** | **5** | backend decomposition (§15), Foundation→Execution-Foundation progression (§7), P0 name *Vision & Constitution*, P3 name *Execution Contracts*, Volume VII Department definition (§17) |
| **REQUIRES RATIFICATION** | **11** | the whole of `CA-01`…`CA-11` (§26), which the candidate itself already reserves |
| **HISTORICAL SNAPSHOT** | **1** | §24, drawn from current execution records — see `C.4` |
| **CONTRADICTED** | **4** | §2 layer model · §3.2/§5 entity roster · §4 document hierarchy · §12/§14 "parallel track" |

**The four CONTRADICTED claims are the audit's material result.** Three of them
are labelled `CONFIRMED` **in the candidate itself**.

---

## C. PROVENANCE FINDINGS

### C.1 `PR-1` — §2's stated warrant does not exist · **UNSUPPORTED CITATION**

**Candidate §2:** *"This sequence is directly preserved from the Engineering
Constitution's Dependency Direction Rules."*

**Measured:** the resident `docs/constitution/engineering-constitution-v1.md`
contains **zero** occurrences of "Dependency Direction", and has **no section of
that name**. Its sixteen sections are Preamble, Vision, Core Philosophy,
Decision-Making, **Governance Artifact Relationship**, Semantic Foundation,
Invariants, Research, Engineering/Architecture/Documentation/Knowledge/Memory/
Security/AI-Collaboration Principles, Definition of Done, Amendment.

**The rule the candidate states is real; the source it names is wrong.**

### C.2 `PR-2` — §3.2's entity list is contradicted by the Constitution's own list · **OVEREXTENDED, at `CONFIRMED`**

**Candidate §3.2** (status `CONFIRMED`): *"The surviving Constitution explicitly
names: Agent Definition; Agent Instance; Execution Contract; Skill; Memory
Record; Knowledge Node."*

**Measured, by exact string count:**

| Candidate entity | Engineering Constitution | Canonical Domain Model | Architecture Freeze |
|---|---:|---:|---:|
| Agent Definition | 4 | 25 | 10 |
| Agent Instance | 4 | 31 | 10 |
| Skill | 4 | 16 | 9 |
| **Execution Contract** | **0** | **0** | **0** |
| **Memory Record** | **0** | **0** | **0** |
| **Knowledge Node** | **0** | **0** | **0** |

**Three of the six named entities do not exist in any of the three governing
sources.** And the Constitution *does* carry an explicit canonical entity list —
**Appendix A, line 242**:

> **Organization, Department, Capability, Agent Definition, Agent Instance,
> Skill, Workflow, Tool, Runtime, Knowledge, Memory, Trace** — defined
> exclusively in the Canonical Domain Model.

**Twelve entities, not six.** The candidate omits six that the Constitution
names and adds three that no source defines.

### C.3 `PR-3` — §11's roadmap citation cannot resolve, **and the defect is mine, not the candidate's**

**Candidate §11:** *"The surviving roadmap requires evidence to control the
detector, not the reverse."*

**Measured:** the persisted `AIOS_MASTER_ROADMAP_PHASE10_PLATFORM_ORGANIZATION_CONSTRUCTION_v1.0.md`
(sha `c6c32a23…`) contains **zero** occurrences of "detector" and has
**seventeen sections (§0–§17)** — no `§27`, no `§28`.

**The rule is real** — the Founder stated it in the Act stream — **but this
repository's record has been citing it to an artifact that does not contain
it.** Measured across my own governance record:

| Citation form | Occurrences | Resolves in the persisted Roadmap? |
|---|---:|---|
| `Roadmap §32` | 4 | **No** — §32 does not exist |
| `Roadmap §28` | 3 | **No** — §28 does not exist |
| `Roadmap §27` | 1 | **No** — §27 does not exist |
| `Roadmap §5`, `Roadmap §6` | 2 | Sections exist; content not re-verified here |

**Eight unresolvable citations, standing since Cycle 26.** `§40`'s own heading
names *"the `§27` Citation Truth check"*. **The check built to catch mis-citation
was itself introduced under a mis-citation.**

**This is `E-41`'s exact class — a true statement behind a false pointer — and
it is the sixth occurrence of the "verified before verifying" pattern**
(`§34.3`, `§35.4`, `§36.7`, `§51.4` defects 3 and 5). It is **not corrected
here**: correcting it is a separate action against my own record, and the
standing rule is that defects in my own verification work are **disclosed, never
silently corrected**.

**Why it belongs in this audit:** the candidate's §28 names *"current execution
records and Acts supplied during the recovery process"* as a source basis.
**The candidate inherited my mis-citation.** That is a closed provenance loop:
my error → my record → the candidate → proposed canon.

### C.4 `PR-4` — §24 is secondary-source promotion, and the candidate says so

§24 draws its operating principles from **my own execution records**. The
candidate correctly labels them *"execution/governance controls"* that
*"must not be mistaken for replacement content from the lost canonical
architecture."* **That self-limitation is accepted and should survive
ratification verbatim.** Flagged under `ACT §10` because a canonical
architecture sourced from an auditor's own working record is the definition of
secondary-source promotion, however well labelled.

### C.5 `PR-5` — claims with no identifiable source in scope

| Candidate | Claim | Measured |
|---|---|---|
| §15 | the `AIOS BACKEND` decomposition *"used in surviving material"* | **0 occurrences** of `AIOS BACKEND` or `Control Plane` anywhere in scope |
| §7 | `Foundation → Execution Foundation → AI Runtime → …` progression | **0 occurrences** of "Execution Foundation" in scope |
| §6 | P0 *"Vision & Constitution"*, P3 *"Execution Contracts"* as Phase names | **0 files** carry either as a Phase name; the other **12 of 14** Phase names are corpus-supported |

**§15's own hedge is correct and is the right disposition** — it explicitly
declines to promote the decomposition. The finding is that **the source it
declines to promote cannot be located at all**, so even its status as a
"candidate decomposition" is unverifiable here.

### C.6 Correctly supported — recorded so the audit is not read as uniformly negative

| Candidate | Verification |
|---|---|
| §12 PD roster | **All ten** CPIDs and names corroborated; every division has a resident record |
| §21 external repositories | **All ten** named repositories present in the resident corpus |
| §9 seven connective systems | **All seven** present by name in the tracked `P10–P13 Blueprint` |
| §8 execution chain, §10 state model, §19 P13 loop | Present in the tracked Blueprint / Gap Closure Roadmap, in the candidate's own wording |
| §25 recoverability boundary | Matches `SG-01` exactly: not in working tree, git history/branches, uploads, or examined archives |

---

## D. CONTRADICTION REGISTER

### `CD-1` — the layer model contradicts a FROZEN source

| | |
|---|---|
| **Candidate claim** | §2: eight layers — Governance → Runtime → **Agent System** → Skill → Memory → Knowledge → **Intelligence Improvement** → Infrastructure |
| **Authoritative source** | `AIOS_ARCHITECTURE_FREEZE_v1.0.md §5` — *"The ten layers (Architecture Specification), **frozen**"* |
| **Exact conflict** | Frozen: 1 Governance · 2 Runtime · 3 Agent · 4 **Capability** · 5 Skill · 6 **Workflow** · 7 Memory · 8 Knowledge · 9 Infrastructure · 10 **Optimization**. The candidate **omits Capability and Workflow entirely**, renames Optimization to "Intelligence Improvement", and **moves it from position 10 (below Infrastructure) to position 7 (above it)** — inverting a frozen dependency edge |
| **Authority level** | **Canonical / Frozen** |
| **Classification** | **CONTRADICTION — FROZEN SOURCE** |
| **Required resolution** | **REQUIRES FOUNDER / ARCHITECT RATIFICATION.** A frozen layer model cannot be amended by a recovery candidate |

**Capability's absence is the load-bearing one.** Freeze §5 layer 4 takes
`Department ownership` as its input, and `INV-1`/`INV-10` are stated in terms of
Capability. A layer model without Capability **cannot express the invariants the
Freeze declares binding.**

### `CD-2` — the document hierarchy contradicts `Constitution §4`

| | |
|---|---|
| **Candidate claim** | §4 (status `CONFIRMED`): *"The surviving Constitution establishes **six document layers**"* — Constitutional · Canonical · Governance · Engineering · Strategic · Implementation |
| **Authoritative source** | `engineering-constitution-v1.md §4` *Governance Artifact Relationship* |
| **Exact conflict** | The Constitution establishes **five named artifacts**: 1 This Constitution · 2 The Canonical Domain Model · 3 The ADR Framework · 4 Principle Documents · 5 The Glossary. It is a **named-artifact** hierarchy, not a **document-class** ordering. Neither the count, the members, nor the kind of ordering match |
| **Authority level** | **Constitutional** |
| **Classification** | **CONTRADICTION — CONSTITUTIONAL, asserted as `CONFIRMED`** |
| **Required resolution** | **REQUIRES FOUNDER / ARCHITECT RATIFICATION** |

### `CD-3` — the entity roster contradicts the sole semantic authority

| | |
|---|---|
| **Candidate claim** | §3.2 / §5: six core entities, including Execution Contract, Memory Record, Knowledge Node |
| **Authoritative source** | `Constitution` Appendix A (twelve entities); `AIOS_ARCHITECTURE_FREEZE_v1.0.md §4` — *"The **twelve** ratified entities … **No new entity.**"*; `Constitution §5` — the Canonical Domain Model is *"the sole semantic authority"* |
| **Exact conflict** | Three candidate entities exist in **no** governing source; six governing entities (Organization, Department, Capability, Workflow, Tool, Runtime, Trace) are **absent from the candidate** |
| **Authority level** | **Constitutional + Canonical (Frozen)** |
| **Classification** | **CONTRADICTION — and a prospective breach of `Constitution §6.2` invariant 3** |
| **Required resolution** | **REQUIRES FOUNDER / ARCHITECT RATIFICATION** |

> `Constitution §6.2` invariant 3: *"No document other than the Canonical Domain
> Model may introduce, redefine, or contradict a Domain Model entity,
> relationship, or invariant."*
>
> **Adopting the candidate as canonical in its current form would place a
> constitutional invariant in breach on the day of adoption.** This is the single
> strongest reason the readiness verdict is not `READY`.

### `CD-4` — "Department" is used as current terminology; a Founder decision made it historical

| | |
|---|---|
| **Candidate claim** | §17 *"DEPARTMENT AND ORGANIZATION ARCHITECTURE"*; §6/§17 *"P10 Department Ecosystem"*; §14: `PD ≠ Department automatically` |
| **Authoritative source** | `canonical-domain-model-v1.md`, terminology note |
| **Exact conflict** | *"The canonical organizational-unit entity is **Platform Division**, per Founder decision **FD-6** (`GDR-0020`), **ADR-0010** and **ADR-0011**. **Department** is its recorded **historical alias**… There `Department` denotes **the same entity**."* The candidate's `PD ≠ Department automatically` **directly negates** the Domain Model's "same entity" |
| **Authority level** | **Founder Decision + Canonical** |
| **Classification** | **CONTRADICTION — FOUNDER DECISION** |
| **Required resolution** | **REQUIRES FOUNDER / ARCHITECT RATIFICATION.** Note `GDR-0020 §3` excludes global renaming of historical evidence — so the candidate may *quote* Department historically; it may not *define* with it |

### `CD-5` — the "parallel track" claim was already withdrawn by this corpus

| | |
|---|---|
| **Candidate claim** | §12: *"The Platform Organization is a parallel/cross-phase construction track. It does not replace Phase 1–13."* Repeated at §14 |
| **Authoritative source** | `platform-organization/README.md §1a` (`VF-9b`) |
| **Exact conflict** | *"**That attribution is false and is withdrawn.** The string occurs **only in this repository's own derived files — zero occurrences in any source**."* The nearest true statement is `Master Program Volume II §8`, about **Track Graphify** — a **different workstream** — and the range is **Phase 0–13**, not 1–13 |
| **Authority level** | **Derived corpus correction** |
| **Classification** | **CONTRADICTION — REPRODUCES A RETRACTED CLAIM** |
| **Required resolution** | **CORRECTION REQUIRED** before ratification. Resolvable by evidence; **no Founder authority needed** |

**`CD-5` is the second closed provenance loop.** The claim was mine, was
withdrawn, survived in historical sections deliberately preserved unaltered, and
has now been read back out of them into a candidate for canon. **Retraction in
place does not prevent re-ingestion.** That is a finding about this corpus's
recovery process, not only about this candidate.

### `CD-6` — the upward-dependency prohibition is stated absolutely; the Freeze permits one governed path

| | |
|---|---|
| **Candidate claim** | §2.1: *"A lower layer MUST NOT create an architectural dependency back upward toward a higher layer."* |
| **Authoritative source** | `AIOS_ARCHITECTURE_FREEZE_v1.0.md §6` direction summary |
| **Exact conflict** | *"authority ↓, execution ↓, **information/knowledge ↑ through the single governed promotion gate (INV-8)**"*. The candidate's absolute prohibition omits the one upward path the Freeze explicitly protects |
| **Authority level** | **Canonical / Frozen** |
| **Classification** | **OVEREXTENSION** — plausibly a data-flow/dependency conflation rather than a contradiction |
| **Required resolution** | **CORRECTION REQUIRED** — resolvable by evidence |

---

## E. MISSING ARCHITECTURE REGISTER

**`MISSING FROM CANDIDATE` ≠ `NEVER EXISTED`.** Every row below has surviving
evidence that the element exists.

| ID | Missing element | Evidence of existence | Recoverability | Status |
|---|---|---|---|---|
| **MA-01** | **Capability** as a layer and entity | `Freeze §4`, `§5` layer 4, `INV-1`, `INV-9`, `INV-10`, `INV-14` | **Fully recoverable** — resident and frozen | **MISSING FROM CANDIDATE** |
| **MA-02** | **Workflow** as a layer and entity | `Freeze §4`, `§5` layer 6, `INV-13` | **Fully recoverable** | **MISSING FROM CANDIDATE** |
| **MA-03** | **Tool**, **Trace**, **Organization**, **Department/Platform Division**, **Runtime** as entities | `Freeze §4`; `Constitution` Appendix A | **Fully recoverable** | **MISSING FROM CANDIDATE** |
| **MA-04** | The **fifteen Frozen Architectural Invariants** (`INV-1`…`INV-15`) | `Freeze §3` | **Fully recoverable** | **ABSENT — no invariant register in the candidate at all** |
| **MA-05** | **Frozen Relationship Rules** (ten relationships, allowed/forbidden direction, ownership, lifecycle) | `Freeze §6` | **Fully recoverable** | **MISSING FROM CANDIDATE** |
| **MA-06** | **Ownership rules** and **lifecycle rules** | `canonical-domain-model-v1.md §5`, `§6` | **Fully recoverable** | Candidate reserves them as `CA-05`/`CA-06` `UNKNOWN` — **but they are resident** |
| **MA-07** | The **`governs` ≠ `owns` ≠ lifecycle-authority** distinction | `canonical-domain-model-v1.md §4.1`; `DEC-F03-057`, `DEC-F03-058` | **Fully recoverable** | **MISSING** — §12.2 paraphrases it without the canonical terms |
| **MA-08** | The original's **`§3.1`–`§3.4` dependency principles, ARB-002-ratified** | `AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md:182` — *"Its **ARB-002-ratified §3.1–§3.4 dependency principles** remain a valid Founder-ratified record of the dependency direction the implementation follows"* | **Structure known; wording not resident** | **MISSING — and the candidate does not cite ARB-002 at all** |
| **MA-09** | The **`GDR-0001` / `G1′` precedence determination** about a document of this name | `AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md:181-183`; `AIOS_FOUNDER_DECISION_G1_PRIME_RATIFICATION_v1.0.md:161` | **Fully recoverable** | **ABSENT — see `H-1`** |
| **MA-10** | **Architecture Freeze §8** load-bearing walls / governance boundaries that cannot be bypassed | `Freeze §8` | **Fully recoverable** | **MISSING FROM CANDIDATE** |

**`MA-06` deserves separate emphasis.** The candidate reserves ownership,
dependency and lifecycle matrices as `UNKNOWN` (`CA-04`, `CA-05`, `CA-06`).
**They are not unknown — they are resident, frozen, and were not consulted.**
Marking a recoverable fact `UNKNOWN` is the mirror image of status inflation and
is equally a defect: it under-claims what the evidence supports, and would
freeze a false gap into canon.

**`MA-04` is the largest single omission.** A canonical architecture that
contains **no invariant register** cannot serve the role every conformance
report in this repository already assigns to one.

---

## F. PHASE-STATE FINDING

**No current canonical Phase 4–9 state has been recovered. None. Not partially.**

| Question | Answer |
|---|---|
| Does the candidate assert a current Phase 4–9 state? | **No.** §6.2 records `CURRENT CANONICAL PHASE-STATE = UNKNOWN / REQUIRES CURRENT SOURCE` |
| Is that correct? | **Yes — and it is the candidate's single best decision.** |
| Was any Phase-state evidence recovered by this audit? | **No** |
| Is the 26 July snapshot substituted anywhere? | **No** — checked; `E-46` remains labelled `SOURCE-VERIFIED / STALE BY DECLARATION` |
| Does the candidate's own §6.1 P10←P9 dependency change the P10 gate? | **No** — it restates the existing prerequisite; it supplies no current state |

**`ACT §15` observed:** `RECOVERY CANDIDATE ≠ P10 READINESS`. **The P10 entry
gate is unchanged.** `R3`'s verdict `P10 BLOCKED` stands, on the same
determining condition, with no new evidence for or against it. **No P10
self-authorization occurred and none is proposed.**

**One precision correction to the candidate's framing.** §0 and §25 describe the
original as *"lost"*. `SG-01`'s finding is stronger and narrower:
*"`AIOS_CANONICAL_ARCHITECTURE.md` **has never existed in this repository's
history**"*, and explicitly *"it is **not** concluded that the document does not
exist."* **`NEVER RESIDENT HERE` ≠ `LOST`.** The distinction matters: a file
that was never here may still exist in the Founder's own corpus, which makes
`H-2` a live question rather than a closed one.

---

## G. CANONICAL-READINESS VERDICT

```text
NOT READY — CONTRADICTIONS
NOT READY — MISSING ARCHITECTURE
NOT READY — EVIDENCE GAPS
```

**All three apply, in that order of severity.**

| Reason | Basis |
|---|---|
| **CONTRADICTIONS** | `CD-1` (frozen layer model) · `CD-2` (constitutional hierarchy) · `CD-3` (entity roster, prospective `§6.2` inv. 3 breach) · `CD-4` (Founder decision FD-6) |
| **MISSING ARCHITECTURE** | `MA-01`…`MA-10`, of which **eight are fully recoverable from resident frozen sources** |
| **EVIDENCE GAPS** | `PR-1`, `PR-3`, `PR-5` — three warrants that do not resolve |

**`BLOCKED — SOURCE DEPENDENCY` is deliberately NOT listed.** The Master Program
and Volume VII remain non-resident, but **the contradictions and omissions above
are resolvable from sources already in this repository.** Naming a source
dependency here would attribute to a missing document a blockage that resident
frozen material is sufficient to clear. **The candidate is not blocked. It is
wrong in four places and short in ten, and both are fixable.**

### G.1 What the candidate gets right

Recorded deliberately, because a verdict of `NOT READY` on a document that
mostly behaves well would otherwise mislead:

- It **refuses to manufacture Phase state** (§6.2) — the discipline that matters most.
- It **declines to promote** the backend decomposition (§15) even while quoting it.
- It **labels its own §24 material** as execution controls, not recovered canon.
- Its **§26 register** reserves eleven items rather than filling them.
- Its **§25 recoverability boundary** matches `SG-01` exactly.
- **Nine claims are outright CONFIRMED** against resident sources.

**The candidate's failures are failures of *provenance*, not of intent.** Every
contradiction found is a case of reaching for a plausible formulation where a
frozen resident one already existed.

---

## H. REQUIRED FOUNDER / ARCHITECT INPUT

**Only decisions that genuinely require reserved authority.** Everything
resolvable by evidence has been excluded — `CD-5`, `CD-6`, `PR-1`, `PR-5`,
`MA-06` and the `IN-1`…`IN-3` intake defects are **not** listed here, because
they can be fixed by reading sources this repository already holds.

| ID | Decision | Why it is reserved |
|---|---|---|
| **H-1** | **Does the candidate inherit `GDR-0001` / `G1′`?** The Register determines that a document of this name is *"**not** the semantic authority; that is the Canonical Domain Model"*, while its *"ARB-002-ratified §3.1–§3.4 dependency principles remain a valid Founder-ratified record"*. **Is the candidate the successor to that ratified instrument, or a new document that must be ratified on its own footing?** | Amending or inheriting a **Founder Decision** — `Constitution §16`, non-delegable |
| **H-2** | **Does an original `AIOS_CANONICAL_ARCHITECTURE.md` exist outside this repository?** `SG-01` establishes it was **never resident here**, not that it never existed — and records that *"`Master Program Pasal 7` names it Layer 2 Canonical"* with `E-52` placing it in the same layer in the Governance Baseline Bundle. **Two surviving sources describe a document this repository never held.** If a Founder-held copy exists, reconstitution is the wrong instrument entirely | **Source supply** — only the Founder can answer |
| **H-3** | **Which layer model governs — Freeze §5's frozen ten, or the candidate's eight?** They cannot both stand | Amending a **frozen** canonical model — Architect-reserved |
| **H-4** | **Are `Execution Contract`, `Memory Record`, `Knowledge Node` real AIOS entities?** If yes, the **Canonical Domain Model** must define them (`§6.2` inv. 3) and this candidate may not. If no, they must be struck | **Domain Model semantics** — `DEL-T4.4-CF-001 §3.2` exclusion 9 |
| **H-5** | **Does `Department` remain a live architectural term?** `FD-6`/`GDR-0020` made it a historical alias of Platform Division; the candidate uses it definitionally and asserts `PD ≠ Department` | Reversing or scoping a **Founder Decision** |

**Not asked, deliberately:** whether to adopt the candidate. `ACT §14` reserves
that, and this audit is not the action that opens it.

---

## I. PROPOSED NEXT ACTION

**Selected under `ACT-CC-CONTINUATION §10A` priority, P3 before P9.**

```text
ACTION       Produce `RECONSTITUTED CANDIDATE — AUDITED REVISION` (ACT §13),
             applying ONLY the evidence-resolvable corrections: CD-5, CD-6,
             PR-1, PR-5, MA-04, MA-05, MA-06, MA-07, MA-10.
CLASS        FIX (evidence-resolvable), not BUILD
AUTHORITY    ACT §13 — a working revision is permitted if labelled, and
             MUST NOT be labelled canonical
EXCLUDED     CD-1, CD-2, CD-3, CD-4 — every one needs H-1..H-5 first.
             A revision that "fixed" them would be self-ratification.
NOT PROPOSED Canonical adoption (ACT §14, reserved);
             writing this body to AIOS_CANONICAL_ARCHITECTURE.md;
             any P10 action whatsoever (ACT §15)
```

**Held pending Founder input:** the revision would close **nine** of the
fourteen findings and leave the four contradictions and `H-1`…`H-5` standing and
visible. **It is offered, not begun** — `ACT §13` permits it, and permission is
not instruction.

**No BUILD action was manufactured.** The audit produced two artifacts — the
persisted candidate and this record — and nothing else was constructed.

---

## §Z — Defects in my own work disclosed by this audit

Recorded here because the standing rule is that defects in my own verification
work are **disclosed, never silently corrected**.

| # | Defect | Where |
|---|---|---|
| 1 | **Eight `Roadmap §27/§28/§32` citations that cannot resolve** — the persisted Roadmap has only §0–§17. Standing since Cycle 26; used twice in this session, most recently two commits ago | `PR-3` |
| 2 | **My corpus citation auditor has never scanned `docs/governance/`** — its root is `docs/architecture/platform-organization/` only. The record carrying the most citations is the one the citation checker cannot see. **Same failure shape as `VF-11`: a guard that passes because it cannot look** | `PR-3` |
| 3 | **I described `docs/program/` as a protected directory in four return contracts.** It is not — protection is keyed on *untracked* paths there. Tracked artifacts including the Blueprint and both Roadmaps were readable all along, and `§52.1` reclassified a frontier item partly on the strength of that misdescription | `§0` |

**Defect 3 changes a conclusion I reported two commits ago.** `§52.1` held that
the ERROR-severity calibration item could not be acted on because its evidence
lay behind a protected boundary. **The boundary is narrower than I said.** The
reclassification to `NO DEFECT IN SCOPE` still stands on its *other* leg — the
in-scope audit reports zero errors, measured again today — but **one of its two
stated reasons was wrong**, and the item should be re-examined against the
tracked `docs/program/` artifacts rather than treated as closed.

**None of these three is corrected in this commit.** Each is a separate action
against a separate artifact, and folding them into an audit of the Founder's
submission would mix two authorities in one change.
