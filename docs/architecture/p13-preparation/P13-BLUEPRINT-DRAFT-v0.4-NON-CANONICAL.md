# P13 Blueprint — **NON-CANONICAL DRAFT** v0.4

> ```text
> STATUS: NON-CANONICAL DRAFT — NOT A FOUNDER DECISION
> P13 CANONICAL DEFINITION = NOT ESTABLISHED
> ```
>
> **Revision authority:** [`ACT-CC-P13-008`](../../governance/acts/ACT-CC-P13-008-V0-3-F1-F2-BOUNDED-CORRECTION-ACT.md)
> — Founder-issued, under `FD-P13-005` Option B. **Scope: `F-1` and `F-2` only.**
> **Baseline:** `…v0.3…` `sha256 6212a717…39e2` · **PRESERVED, UNMODIFIED**
> **Predecessors:** `…v0.2…` `a4095a33…9c57` · `…v0.1…` `75775cbd…d5f1` · **both PRESERVED**
>
> **Minimum change.** Exactly two corrections were applied — the `§O5.4`
> completeness claim (`F-1`) and the change-ledger reconciliation (`F-2`).
> `ACT-CC-P13-008 §12` lists the sections that must remain unchanged; all of
> them are byte-identical to v0.3. No architectural redesign (`§13`).
>
> ```text
> P13 AUTHORIZATION  NOT GRANTED     P13 CONSTRUCTION  NOT AUTHORIZED
> P13 CERTIFICATION  NOT AUTHORIZED  NATIVE CORE       11 — FROZEN
> GAP-0001           OPEN · APEX     CANONICALIZATION  FOUNDER RESERVED
> ```

---

## §0 — Authority boundary of this document

**This is an artifact revision. It is nothing else.** Stated explicitly because
`ACT-CC-P13-005 §6.7` and `FD-P13-003 MOD-07` require it:

```text
REVISION  ≠ CANONICALIZATION        ≠ P13 AUTHORIZATION
          ≠ P13 CONSTRUCTION        ≠ P13 CERTIFICATION
          ≠ NATIVE CORE AUTHORIZATION
          ≠ FOUNDER-RESERVED DECISION
          ≠ ARCHITECT-RESERVED DECISION
```

**No statement anywhere in this document may be read as self-generated
authority.** `ACT-CC-P13-005 §7.30` forbids creating authority through the
Blueprint itself, and `§2` forbids inferring it from document existence,
repository convention, architectural necessity, technical convenience, silence,
precedent, or spent authority.

### The one rule that governs this revision more than any other

`ACT-CC-P13-005 §6.3`:

> **"No epistemic upgrade may occur merely because the Blueprint is being
> revised."**

A second draft is under constant pressure to *read* more settled than the first.
**This revision resists that by design.** Where v0.2 differs from v0.1, the
difference is in *how precisely a claim is sourced*, never in *how strongly it
is asserted*. The change ledger (`§L`) records every difference and its reason,
and **no claim moved up a class**. One moved *sideways* into a more exact class,
and it is named there.

---

## §0.1 — Evidence classes

Five, per `ACT-CC-P13-005 §6.1`. v0.1 used four; the fifth is the split the
Founder required.

| Mark | Meaning | May it be read as established fact? |
|---|---|---|
| **`CANONICAL`** | a resident canonical file, cited by section, with its text | **Yes**, as to what the source says |
| **`MEASURED`** | a named, re-runnable command against resident code, **run during this execution** | **Yes**, as to observed system state |
| **`PREP-RECORD`** | a `P13-001`…`P13-007` record's measurement of a **non-resident** source. **Not direct inspection** | **No** — evidence *about* a measurement, one remove from the source |
| **`PROPOSED`** | this draft's own synthesis, with reasoning | **No** — a proposal |
| **`UNKNOWN / NOT DIRECTLY VERIFIED`** | no fact, or no direct verification available, with the named absent source | **No** — and `UNKNOWN ≠ FALSE` |

```text
PROPOSED ≠ CANONICAL        UNKNOWN ≠ FACT
MEASURED ≠ CANONICAL        PREP-RECORD ≠ DIRECT SOURCE
NOT FOUND ≠ FALSE           NO EVIDENCE ≠ EVIDENCE OF ABSENCE
```

**Why `PREP-RECORD` matters.** v0.1 marked corpus-derived statements `MEASURED`
and disclosed the limitation in prose at the top. That was honest but
structurally imprecise: a reader scanning marks alone would see `MEASURED`
against a claim nobody has directly verified. `PREP-RECORD` makes the distance
visible at the point of the claim, which is what `FD-P13-003 MOD-01` requires:
*"A preparation record, measurement, or synthesis may not be presented as though
it were direct canonical source evidence."*

---

## §0.2 — Corpus transparency

### What was actually done this execution

`ACT-CC-P13-005 §6.2` permits inspecting *"any actually resident and authorized
P13 source material"*. **A direct residency search was run**, rather than
inheriting v0.1's statement:

```text
COMMAND   find . -type f \( -name "*.md" -o -name "*.pdf" -o -name "*.txt" \)
            | xargs grep -ril "Super Intelligence Blueprint|
                               P13 Autonomous Construction|
                               P13 Systemic Gap Discovery"
          find . -type d -iname "*p13*"

RESULT    3 files matched — all of them AIOS preparation records that
          MENTION the corpus titles.  None is a corpus document.
          Only directory: docs/architecture/p13-preparation/ (this programme's
          own records).

FINDING   P13 SIX-FILE CORPUS = NOT FOUND, verified by direct search
                                 during this execution
```

**This is a strengthening of provenance, not of conclusion.** v0.1 said it *"did
not re-read the corpus"*. v0.2 says the corpus *was searched for and is not
present* — the same conclusion, now directly verified rather than inherited.
`NOT FOUND` remains `NOT FOUND` and is **not** converted to `FALSE`
(`§6.2`): the documents exist outside this repository; they are simply not
reachable from it.

### The three-way distinction, applied

| | What it means here |
|---|---|
| **DIRECT SOURCE INSPECTION** | resident files opened and read this execution — the Acts, decisions, registers, Native Core tree, preparation records |
| **PREP-RECORD EVIDENCE** | anything about the six corpus files. Reached only through `P13-001`…`P13-004`, which measured them when they were in hand |
| **INFERENCE / SYNTHESIS** | this draft's proposals — marked `PROPOSED`, never mixed with either above |

**Nothing was reconstructed** (`§11`). Where the corpus is the only possible
source for a claim, the claim carries `PREP-RECORD` or `UNKNOWN`, never
`CANONICAL`.

---

## `O1` — P13 identity proposal

### What is established

| Claim | Class | Source |
|---|---|---|
| Program label *"P13 — Super Intelligence Ecosystem"* exists | `PREP-RECORD` | `P13-001`, quoting the Master Program position. **The Master Program document is not resident**; the label reaches this draft through the record |
| No resident source defines P13's canonical identity | `MEASURED` | direct search this execution: no resident file states a P13 definition |
| Corpus self-assessment: 7 of 7 identity questions `UNKNOWN`; F1 `§2` calls its own problem statement *"investigation framing, bukan final definition"* | `PREP-RECORD` | `P13-001`. **Not directly inspected** |

**`P13 IDENTITY ≠ PHASE LABEL`.** The label is attested; the identity is not.

> **v0.1 → v0.2 change.** Row 1 and row 3 were `CANONICAL`/`MEASURED` in v0.1.
> Both are now `PREP-RECORD`. **This is a downgrade in class precision, not a
> change in what is claimed** — see `§L-01`.

### The proposal

**`PROPOSED`.** Built on two measurements, both re-verified this execution where
resident code permitted:

```text
REQUIREMENT FAMILIES (11)                          PREP-RECORD — P13-001 O2
  PARTIAL / CONNECTIVE      6
  MISSING                   4    evaluation · reasoning · next-action · completion
  DISCONNECTED BY RULING    1    Optimization → Governance

AGENT DIMENSIONS (17)                              PREP-RECORD — P13-001 O3
  EXISTING 6 · PARTIAL 5 · MISSING 5 · DISCONNECTED 1

RE-VERIFIED DIRECTLY THIS EXECUTION                MEASURED
  grep "class Reasoning|def reason("  native_core/  →  0
  grep "class Evaluation|def evaluate(" native_core/ →  0
```

**The two MISSING dimensions most load-bearing for the proposal were
re-measured directly and hold.** The remaining counts rest on `PREP-RECORD`
evidence and are marked so.

> **Proposed — and it is a proposal, not a finding:**
>
> **P13 is the phase in which AIOS acquires the capacity to reason about,
> evaluate, and govern its own state and its own next action — built as
> connective tissue across the eleven frozen Native Core boundaries, not as a
> twelfth.**

On this proposal the five `MISSING` dimensions are P13's **content** and the six
`EXISTING` are its **substrate**. Both halves are `PROPOSED`.

### What constrains the proposal

| Constraint | Class | Basis |
|---|---|---|
| `NATIVE CORE = 11` | **`MEASURED`** — counted this execution, see `§N` | the tree itself |
| `§58`'s five-link chain for P13 | `CANONICAL` | P12 Blueprint, resident |
| `P12 EXIT CRITERIA ≠ P13 EXIT CRITERIA` | `PREP-RECORD` | `P13-001 O2` |

### What this proposal does not claim

```text
NOT CLAIMED  that "Super Intelligence" names an autonomy level, capability
             tier, or intelligence guarantee                  → UNKNOWN, see §S
NOT CLAIMED  that the five MISSING dimensions are the ONLY content of P13
             → NO EVIDENCE ≠ EVIDENCE OF ABSENCE
NOT CLAIMED  that P13 must proceed at all    → FD-P13-001 §7 Path C is open
NOT CLAIMED  that this proposal answers GAP-0001
```

**`GAP-0001` is not closed by this section, and this draft may not close it**
(`ACT-CC-P13-005 §8`).

```text
PROPOSED P13 DEFINITION  ≠  CANONICAL P13 DEFINITION
```

---

## `O2` — Mission / scope proposal

**`PROPOSED`** throughout, derived from `O1`.

> To make AIOS able to answer, from evidence and under governance, three
> questions it currently cannot: **What state am I actually in? · Is that state
> good? · What should I do next?** — each answer traceable, refusable, and
> subject to human authority.

| Question | Measured absence | Class | Existing substrate | Class |
|---|---|---|---|---|
| *What state am I in?* | `CONTEXT` — `RuntimeContext` carries no business knowledge, Memory contents, Governance decisions or Agent state | `PREP-RECORD` | `STATE` — `p12_operational_state`, 8 sources · 0 stale | `PREP-RECORD` |
| *Is that state good?* | `EVALUATION` — **0 symbols in `native_core/`** | **`MEASURED`** | `OBSERVATION` — `TracedAction`, 30s liveness horizon | `PREP-RECORD` |
| *What should I do next?* | `REASONING` — **0 symbols in `native_core/`** | **`MEASURED`** | `DECISION` — `GovernanceReview`, `HumanAuthority` fails closed | `PREP-RECORD` |

### Proposed scope — in `PROPOSED`

```text
IN   context assembly — composes agent-facing context from existing
     boundaries, without moving knowledge into RuntimeContext
IN   evaluation — judges observed state against stated criteria
IN   reasoning — traceable, evidence-bearing conclusions
IN   next-action — PROPOSES, never self-authorizes
IN   evolution — supersession as a capability, not only a record
IN   completing the five PARTIAL dimensions
```

### Proposed scope — out `PROPOSED`, on the bases shown

| Out of scope | Basis | Class |
|---|---|---|
| a twelfth Native Core boundary | the freeze; and `ACT-CC-P13-005 §6.5` forbids it outright | `CANONICAL` |
| autonomous runtime · daemon · scheduler · queue · self-activation | standing programme constraint | `CANONICAL` |
| `Optimization → Governance` connection | ruled absent *"by construction"*, `P7-I27 Conflict A`; **Architect-reserved** | `PREP-RECORD` |
| a P13 system-integration layer | `D-2` — P12 owns it and it is certified | `PREP-RECORD` |
| any weakening of `HumanAuthority` | Constitution `§6.2` invariant 2 | `PREP-RECORD` |

**The next-action surface is the authority-sensitive one.** It is proposed as
**proposes only** — `RECOMMENDATION ≠ DECISION`. **Any stronger reading is
`UNKNOWN` and Founder-reserved** (`GAP-0004`), and this draft does not take it.

---

## `O3` — Required-state proposal

**`PROPOSED`** throughout. v0.1 recorded required state as `NOT ESTABLISHED`;
**v0.2 does not change that** — it proposes answers and marks them as proposals.

| Question | Proposed answer | Basis class |
|---|---|---|
| What must **exist**? | five candidate surfaces | `PROPOSED` from `O1` |
| What must be **implemented**? | the five, plus the five `PARTIAL` | `PROPOSED` / `PREP-RECORD` |
| What must be **integrated**? | **nothing new at system level** — P12's is certified | `PREP-RECORD` — `D-2` |
| What must be **verified**? | each surface **live**, not documentary | `CANONICAL` — `§46` |
| What must be **governed**? | all through `HumanAuthority`; none may synthesise authority | `PREP-RECORD` — `§6.2` inv. 2 |
| What must be **traceable**? | every conclusion, evaluation, proposed action; `§29`'s twelve elements | `CANONICAL` — P12 `§29` |
| What must be **refusable**? | every next-action proposal; durable and typed | `PREP-RECORD` — `refusal_type` |
| What is **complete**? | **`UNKNOWN`** — Founder-reserved | `CANONICAL` — `GAP-0002` |

**The last row is deliberate, not a gap in effort.** A draft proposing P13's
completion criteria would be proposing its own success condition.

---

## `O4` — Relationship to P1–P12

| | Class |
|---|---|
| `P13 CONSUMES` — Native Core 11 · Knowledge/Memory · Execution·Runtime·Trace (8 classes, 7 verified, 0 dangling) · Governance·Delegation (4/4 chains) · P12 verification architecture | `PREP-RECORD`, except the boundary count which is `MEASURED` |
| `P13 EXTENDS` — the five candidate surfaces | `PROPOSED` |
| `P13 MUST NOT DUPLICATE` — system integration (`D-2`) · self-model · operational state | `PREP-RECORD` |

P1–P9 residency is `PARTIALLY REQUIRED`, **not blocking** — `D-1`,
`PREP-RECORD`. **P1–P9 documents are `NOT FOUND`, not absent from existence**
(`§6.2`).

---

## `O5` — Architecture across the seventeen scope items

> **`O5` was verified item-by-item under `ACT-CC-P13-006`.** The aggregate claim
> v0.2 carried — *"Seven of seventeen already have canonical sources"* — is
> replaced below by the seven items **named individually with their resident
> sources**, as `§9` requires: *"shall not be retained as an unsupported
> aggregate assertion when the seven items can be individually named."*
>
> **Outcome A — DIRECTLY VERIFIED**, with two qualifications recorded at `V-5`
> and `V-7`, and one enumeration defect in v0.2 corrected at `§O5.3`.

### `§O5.1` — The seven items claiming canonical sources, individually verified

Each tested against `ACT-CC-P13-006 §12`'s four conditions —
`EXISTS → RESIDENT → AUTHORITATIVE → ACTUALLY SUPPORTS THE ITEM`.

| | Item | Claimed source | Actual location, inspected this Act | 4 conditions | Result |
|---|---|---|---|---|---|
| `V-1` | **Dependencies** | `§58` | `AIOS_P12_ROADMAP_PRD_CONSTRUCTION_BLUEPRINT_v1.0.md:645` — *"P13 requires its own: `Blueprint → Canonical Reconciliation → Authority Preparation → Founder Authorization → Construction`"* | ✓✓✓✓ | **DIRECTLY VERIFIED** |
| `V-2` | **Runtime interaction** | Native Core = 11; `Agent → Execution → Runtime` | `…v1.0.md:784` `NATIVE CORE = 11 FROZEN BOUNDARIES`; `DP-01-P11-FOUNDER-AUTHORIZATION-SURFACE.md:135`; `native_core/core/agent/agent.py:58` `class Agent(ExecutionConsumer)`, importing `..runtime.execution.consumer` | ✓✓✓✓ | **DIRECTLY VERIFIED** |
| `V-3` | **Knowledge / Memory** | P6/P7 boundaries resident | `native_core/core/knowledge/{admission,composition,repository,retrieval,models}.py`; `native_core/core/memory/` | ✓✓✓✓ | **DIRECTLY VERIFIED** |
| `V-4` | **Governance** | Constitution `§6.2` inv. 2; `HumanAuthority` | `AIOS_IMPLEMENTATION_CONSTITUTION_v1.0.md:49` — *"Governance First … automation and tooling may propose but never override"*; `native_core/core/governance/authority.py:33` `class HumanAuthority` | ✓✓✓✓ | **DIRECTLY VERIFIED** |
| `V-5` | **Verification** | *"F5 discipline **+** P12's verification architecture"* | P12 half: **14** `tools/p12_*verification*.py` modules, resident. **F5 half: `NOT FOUND`** — corpus non-resident | ✓✓✓✓ *on the resident half only* | **DIRECTLY VERIFIED on the P12 half** · F5 component `NOT DIRECTLY VERIFIED` |
| `V-6` | **Evidence** | P12's evidence model, certified | `tools/p12_execution_provenance.py`, `p12_provenance_verification.py`, `p12_governance_evidence_verification.py`, `p12_certified_evidence_guard.py`; certification `FD-P12-006`, resident | ✓✓✓✓ | **DIRECTLY VERIFIED** |
| `V-7` | **Exhaustion** | *"`§55` precedent; **F3/F6 agree**"* | `§55` at `…v1.0.md` *"55. Exhaustion Model"*, ten conditions, read directly. **F3/F6: `NOT FOUND`** — corpus non-resident | ✓✓✓✓ *on `§55` only* | **DIRECTLY VERIFIED on `§55`** · F3/F6 component `NOT DIRECTLY VERIFIED` |

```text
DIRECTLY VERIFIED                    7 of 7 items
  — of which fully verified          5   (V-1 V-2 V-3 V-4 V-6)
  — of which verified on the
    resident portion of a compound
    citation                         2   (V-5 V-7)
NOT DIRECTLY VERIFIED (components)   2   F5 · F3/F6 — non-resident corpus
```

**The two qualifications are stated rather than smoothed.** `V-5` and `V-7` each
cite **two** sources joined by *"+"* / *";"*. In both cases the **resident**
source independently satisfies all four conditions and the item classification
stands on it alone. The **corpus** component could not be inspected — the corpus
is `NOT FOUND` (`§0.2`) — and is marked `NOT DIRECTLY VERIFIED`. It was **not
reconstructed** (`§11`), and `NOT FOUND` is **not** converted to `FALSE`
(`§10`).

### `§O5.2` — The remaining ten items

Unchanged from `P13-004 O5`; classifications preserved, not re-derived
(`§9`: *"preserve the remaining ten classifications"*).

| Item | Classification | Evidence class |
|---|---|---|
| Identity · Mission · Boundary | `REQUIRES FOUNDER DECISION` (3) | `PREP-RECORD` |
| Requirements · Capabilities · Conformance | `SOURCE EXISTS, NON-CANONICAL` (3) | `PREP-RECORD` |
| Agent model | `REQUIRES RECONCILIATION` | `PREP-RECORD` |
| Architecture · Contracts | `NOT ESTABLISHED` (2) | `PREP-RECORD` |
| **System integration** | **`NOT IN SCOPE`** — `D-2` | `PREP-RECORD` |

### `§O5.3` — An enumeration defect in v0.2, corrected

**v0.2's `O5` table was headed *"the seventeen scope items"* and enumerated
only fourteen.** Counted this Act:

```text
v0.2 rows:  Requirements·Capabilities·Conformance 3 · Agent model 1 ·
            System integration 1 · Architecture·Contracts 2 ·
            Dependencies…Exhaustion 7                        =  14
P13-004 O5 full list                                          =  17
ABSENT from v0.2's table:  Identity · Mission · Boundary      =   3
```

The three absent items are the `REQUIRES FOUNDER DECISION` set. v0.2's prose
referred to them — *"only three items are genuinely Founder-reserved"* — while
its table omitted them. **`§O5.2` restores all three.** They remain
`REQUIRES FOUNDER DECISION`; **nothing about them was decided** (`§18`).

### `§O5.4` — What this verification does and does not establish

```text
ESTABLISHED   seven named items have resident canonical sources, each
              inspected directly and cited to file and line
ESTABLISHED   two of those citations are compound, and their corpus half
              remains NOT DIRECTLY VERIFIED
ESTABLISHED   all seventeen items of the PREPARATION-RECORD enumeration are
              represented again — three were absent from v0.2's table

NOT ESTABLISHED   that seventeen is the canonical P13 scope, or that the
                  enumeration is complete against any canonical definition
NOT ESTABLISHED   that the P13 architecture is correct or canonical
NOT ESTABLISHED   that P13 should proceed
NOT ESTABLISHED   anything about GAP-0001
```

**`F-1`, corrected under `ACT-CC-P13-008 §7`.** v0.3 stated *"the seventeen-item
list is complete again"* inside the `ESTABLISHED` block. **"Seventeen" is a
`PREP-RECORD` enumeration**, originating in `P13-004 O5` and derived from the
non-resident corpus; **no resident canonical source enumerates seventeen P13
scope items.** What is established is representation against *that* list, not
completeness against a canonical scope.

```text
17-ITEM PREPARATION-RECORD ENUMERATION   ≠   CANONICAL P13 SCOPE
```

The list, its classifications and the seven verified mappings are unchanged
(`§8`). **What P13's scope canonically contains remains `UNKNOWN`** and is part
of `GAP-0001`, which this correction does not touch.

**`ACT-CC-P13-006 §15` governs, and it is the point of this section:**

```text
O5 verification  →  O5 EVIDENCE STATUS ESTABLISHED
O5 verification  ↛  P13 ARCHITECTURE VALIDATED
```

**The downstream inference v0.2 drew from `O5` is weakened, not strengthened,
by verifying it.** v0.2 said: *"If it holds, a real P13 Blueprint is mostly
citation and only three items are genuinely Founder-reserved."* It holds — and
it supports only that **seven of seventeen scope items can cite existing canon**.
It says nothing about whether the other ten can be filled, and the three
Founder-reserved items are precisely the ones no citation can supply.

### Proposed placement — and the question it must not answer

**`PROPOSED`.** The five surfaces are proposed for the **tools layer**, on the
`PREP-RECORD` observation that agent identity already lives there
(`AgentDefinition`, `AgentInstanceRegistry`) while `native_core/core/agent/`
answers only *"how does an Agent enter the execution system?"*.

> **`UNKNOWN` — and it stays `UNKNOWN`.** Whether any candidate capability
> *requires* Native Core placement is **not decided here and may not be**.
> `ACT-CC-P13-005 §6.5`: the revision *"may identify a possible Native Core
> placement as an unresolved architectural question"* and *"may NOT ... declare
> a new Native Core subsystem"*. If revision work were to require a Native Core
> change, `§6.5` directs `STOP AND ESCALATE`. **It did not: identifying the
> question is within scope; answering it is not.**

---

## `O6` — Agent-model reconciliation

`GAP-0009` records three disagreeing agent lists. **This draft does not close
it** — Founder-reserved as `FD-P13-005`.

```text
PREP-RECORD — P13-001 O3
  native_core/core/agent/agent.py answers exactly one question:
    "how does an Agent enter the execution system?"
  It deliberately answers none of: which agent · version · instance · model.
  Agent extends ExecutionConsumer; participate(execution) is its only entry.
  Identity lives in tools: AgentDefinition, AgentInstanceRegistry.

MEASURED — this execution
  native_core/core/agent/ exists as one of the eleven boundaries.
```

**`PROPOSED` principle:** any P13 agent list is a tools-layer registry
reconciled *against* the Native Core entry contract, never a redefinition of it.
**Which list is canonical remains `UNKNOWN`.**

---

## `O7` — Dependency and sequencing

**`PROPOSED`**, respecting `§58`'s chain (`CANONICAL`).

```text
GAP-0001  WHAT IS P13?                    ← APEX · FOUNDER · blocks 21
    ├── GAP-0002  P13 Exit Contract        cannot precede identity
    ├── GAP-0004  reserved authority       autonomy boundary
    └── specification of the five surfaces (NOT construction)
            ▼
        §58  CANONICAL RECONCILIATION → AUTHORITY PREPARATION
                                       → FOUNDER AUTHORIZATION → CONSTRUCTION

PARALLEL: GAP-0005 · GAP-0006 · GAP-0008 · GAP-0010 (ARCHITECT)
```

**Proposed build order, conditional on an authorization that does not exist:**
context assembly → evaluation → reasoning → next-action → evolution. Each
consumes the previous; `next-action`, the authority-sensitive one, comes last.

---

## `O8` — Governance / authority boundary

**`PROPOSED`**, deliberately conservative.

```text
EVERY candidate surface would:
  · fail CLOSED on absent authority
  · produce PROPOSALS, never decisions
  · carry §29's twelve preservation elements
  · be refusable, typed, durable
  · synthesise NO authority

NEXT-ACTION specifically:
  · proposes; a human decides
  · no self-activation, scheduler, daemon or queue
  · silence is never approval
```

**What this draft cannot propose: the autonomy boundary itself.** `GAP-0004` is
Founder-reserved and downstream of `GAP-0001`. **`UNKNOWN`.**

---

## `O9` — Verification and exhaustion criteria

**`PROPOSED`**, reusing P12's architecture rather than inventing one.

| Criterion | Proposed standard | Precedent class |
|---|---|---|
| Existence | resolves and is importable | `PREP-RECORD` |
| Integration | exercised **live**, not documented | `CANONICAL` — `§46` |
| Refusal | reachable, typed, durable | `PREP-RECORD` |
| Negative control | every prohibition has a control that *would* fail | `PREP-RECORD` |
| Unknown-handling | `UNKNOWN` on absent evidence is **correct** | `CANONICAL` — `§43` |
| Exhaustion | `EXHAUSTED` · `…_WITH_CLASSIFIED_REMAINDER` · `BLOCKED_AUTHORITY` | `CANONICAL` |

**P13's exit contract is not proposed here.** These are methods, not completion
conditions.

---

## `O10` — Gap-closure map

**Conditional throughout.** `ACT-CC-P13-005 §7.20` forbids closing `GAP-0001` by
assertion and `FD-P13-003 §20` forbids closing any gap because a proposal
exists.

```text
WOULD CLOSE — IF a canonical P13 definition were established     ~15
  GAP-0002 · GAP-0004 · GAP-0012–0022 (11) · GAP-0026 · GAP-0027
  — for SPECIFICATION only.  Construction stays unauthorized.

WOULD NOT CLOSE — separate authority paths
  GAP-0003b canonicalization (FOUNDER §58) · GAP-0005 P1–P9 ·
  GAP-0006 corpus residency · GAP-0008 H-1 (inherited) ·
  GAP-0009 agent canon · GAP-0010 (ARCHITECT) ·
  FD-2 Founder ≡ Architect — open, load-bearing

ALREADY RESOLVED, NOT REOPENED
  GAP-0003 drafting authority · GAP-0011 system integration (D-2)
```

**Register total: 28 — unchanged. No gap closed, reopened or reclassified by
this revision.**

---

## `§N` — Native Core boundary

`ACT-CC-P13-005 §6.5` and `FD-P13-003 MOD-05` require five categories be kept
apart. **`NATIVE CORE = 11` is `MEASURED` this execution**, not inherited.

### The measurement, and a caveat that matters

```text
COMMAND  ls -d native_core/core/*/ | grep -v __pycache__ | wc -l
RESULT   11
NAMES    agent · capability · governance · infrastructure · knowledge ·
         memory · optimization · runtime · skill · trace · workflow

CAVEAT   The naive count `ls -d native_core/core/*/ | wc -l` returns 12,
         because __pycache__ is a directory.  It is a build artifact, not a
         boundary.  Reported because a future reader running the naive
         command would otherwise see 12 and believe the freeze had broken.
```

### The five categories

| # | Category | State | Class |
|---|---|---|---|
| 1 | **Existing Native Core capability** | the eleven above | **`MEASURED`** |
| 2 | **Connective tissue** | composition *between* boundaries; no new boundary | `PROPOSED` |
| 3 | **Tools-layer capability** | where agent identity already lives | `PREP-RECORD` |
| 4 | **Proposed architectural placement** | the five surfaces → tools layer | `PROPOSED` |
| 5 | **Unresolved Native Core placement question** | whether any candidate *requires* Native Core placement | **`UNKNOWN`** |

```text
NATIVE CORE = 11 FROZEN BOUNDARIES
```

**Nothing in this document creates, declares, implies or authorizes a twelfth.**
Category 5 is stated as a question and left as one. `§6.5`'s `STOP AND ESCALATE`
was not triggered, because identifying the question required no Native Core
change.

---

## `§S` — "Super Intelligence"

`ACT-CC-P13-005 §6.6` permits clarifying the terminology and forbids assigning
it a canonical substantive meaning.

| Layer | State | Class |
|---|---|---|
| **Program label** — *"P13 — Super Intelligence Ecosystem"* | **attested** | `PREP-RECORD` — via `P13-001`; the Master Program document is not resident |
| **Substantive meaning** — what the phrase denotes | **`NOT ESTABLISHED`** | `UNKNOWN` |
| Autonomy level it implies | none stated by any resident source | `UNKNOWN` |
| Capability tier it guarantees | none stated by any resident source | `UNKNOWN` |
| Intelligence claim it makes | none stated by any resident source | `UNKNOWN` |

**Why the label is used at all:** it is the identifier under which this
programme's instruments refer to P13. **Using a label is not defining it.**

```text
PROGRAM LABEL  ≠  CANONICAL SUBSTANTIVE DEFINITION
```

**This draft assigns the phrase no meaning.** `O1`'s proposal describes a
capability shape derived from measured absence; **it is not offered as the
meaning of "Super Intelligence"**, and the two must not be conflated. Whether
they coincide is Founder-reserved.

---

## `§R` — Reserved matters, preserved

`ACT-CC-P13-005 §9`, `§10` — identified, traced, prepared, **not decided**.

### Founder-reserved

| Matter | State |
|---|---|
| Canonical P13 definition (`GAP-0001`) | **OPEN · APEX** |
| Substantive meaning of "Super Intelligence" | **UNRESOLVED** |
| P13 continuation at all (`FD-P13-001` Path C) | **OPEN** |
| P13 canonicalization · construction authorization · certification | **RESERVED** |
| Native Core expansion | **RESERVED** |
| P13 exit criteria (`GAP-0002`) | **OPEN** |
| P13 autonomy boundary (`GAP-0004`) | **OPEN** |
| Agent lifecycle canon (`GAP-0009`) | **OPEN** |
| Corpus residency (`GAP-0006`) | **OPEN** |
| `FD-2` Founder ≡ Architect | **OPEN — `IMPLIED`, not separately ratified** |

### Architect-reserved

| Matter | State |
|---|---|
| `AD-P13-001` `Optimization → Governance` | **CONFLICTED — preserved, not reconciled** |
| `AD-P13-002` `ADR-0029` cross-PD interface | **OPEN — inherited, not P13's** |

**`§11` applied:** the `Optimization → Governance` conflict is preserved as
`CONFLICTED`. **No reconciliation was manufactured.**

**Count: 10 Founder-reserved and 2 Architect-reserved matters identified;
0 decided.**

---

## `§D` — Decision-readiness package

`ACT-CC-P13-005 §6.7`'s ten separations.

| | | |
|---|---|---|
| **1. Established facts** | `NATIVE CORE = 11` · `P13 AUTHORIZED = False` · `§58`'s chain · P12 certified · `docs/architecture/p13/` absent | `CANONICAL` / `MEASURED` |
| **2. Measured state** | 11 boundaries · 0 `Reasoning` symbols · 0 `Evaluation` symbols · corpus `NOT FOUND` | `MEASURED`, this execution |
| **3. Prep-record evidence** | 17 agent dimensions · 11 requirement families · 8 integration classes · 28-gap register · `D-1`/`D-2`/`D-3` | `PREP-RECORD` |
| **4. Proposals** | the identity · mission · five surfaces · tools-layer placement · build order · governance shape | `PROPOSED` |
| **5. Unknowns** | ten, in `§Q` | `UNKNOWN` |
| **6. Founder decisions required** | ten, in `§R` | — |
| **7. Architect decisions required** | two, in `§R` | — |
| **8. Evidence still required** | direct corpus access (`GAP-0006`); item-by-item re-verification of `O5`'s 17; P1–P9 documents if ever cited as authority | — |
| **9. Authority dependencies** | `GAP-0001` gates 21 · `FD-2` is load-bearing beneath this Act's own delegation chain | — |
| **10. Stop conditions** | Native Core placement · canonicalization · construction · any reserved matter — all live, none crossed | — |

**The objective was decision clarity, not artificial completeness**
(`§6.7`). Where completeness would have required inventing an answer, the
question is listed instead.

---

## `§Q` — Open questions

| # | Question | Class | Owner |
|---|---|---|---|
| 1 | What **is** P13, canonically? | `UNKNOWN` | **Founder** — `GAP-0001` |
| 2 | What does *"Super Intelligence"* denote? | `UNKNOWN` | **Founder** |
| 3 | Do the five surfaces belong in tools or Native Core? | `UNKNOWN` | **Founder / Architect** |
| 4 | Where is P13's autonomy boundary? | `UNKNOWN` | **Founder** — `GAP-0004` |
| 5 | What are P13's exit criteria? | `UNKNOWN` | **Founder** — `GAP-0002` |
| 6 | Which agent list is canonical? | `UNKNOWN` | **Founder** — `GAP-0009` |
| 7 | Should `Optimization → Governance` be connected? | `CONFLICTED` | **Architect** — `AD-P13-001` |
| 8 | Does the corpus become resident? | `UNKNOWN` | **Founder** — `GAP-0006` |
| 9 | Is Founder ≡ Architect ratified? | `UNKNOWN` | **Founder** — `FD-2` |
| 10 | Must P13 proceed at all? | `UNKNOWN` | **Founder** |

**Ten, unchanged from v0.1.** None was answered by this revision, and **none was
added** — the revision found no new question it could legitimately raise as a
gap (see `§X`).

---

## `§L` — Change ledger, v0.1 → v0.2

`ACT-CC-P13-005 §13.7` requires that no unsupported epistemic upgrade occurred.
**Every change is listed. None is an upgrade.**

| ID | Change | Direction | Reason |
|---|---|---|---|
| `L-01` | Corpus-derived claims reclassified `MEASURED`/`CANONICAL` → **`PREP-RECORD`** | **more precise / weaker** | `MOD-01`; `PREP-RECORD ≠ DIRECT SOURCE` |
| `L-02` | Corpus residency: *"did not re-read"* → **`NOT FOUND`, verified by direct search this execution** | **sideways — provenance strengthened, conclusion unchanged** | `§6.2`; the one change that improves an evidence basis, and it improves *how it is known*, not *what is known* |
| `L-03` | `NATIVE CORE = 11` reclassified `CANONICAL` → **`MEASURED`**, with the `__pycache__` caveat | **more precise** | counted from the tree this execution |
| `L-04` | `Reasoning`/`Evaluation` absence re-measured directly → **`MEASURED`** | **more precise** | `§22` — not established merely by appearing in v0.1 |
| `L-05` | Evidence classes 4 → **5** | structural | `§6.1` |
| `L-06` | New `§N` Native Core section, five categories | structural | `MOD-05` |
| `L-07` | New `§S` "Super Intelligence" section | structural | `MOD-06` |
| `L-08` | New `§R` reserved matters, counted | structural | `MOD-08` |
| `L-09` | New `§D` decision-readiness, ten separations | structural | `MOD-10` |
| `L-10` | New `§0` authority-boundary statement | structural | `MOD-07` |
| `L-11` | `O10` made explicitly conditional | **weaker** | `§7.20` |
| `L-12` | This ledger | structural | `MOD-01` |
| `L-13` | **v0.3:** `O5` aggregate claim replaced by seven named items with file-and-line citations | **stronger — and directly evidenced** | `ACT-CC-P13-006 §9`; the only upgrade in this lineage, and it is carried by direct inspection |
| `L-14` | **v0.3:** `V-5` and `V-7` corpus components marked `NOT DIRECTLY VERIFIED` | **weaker** | `§12`; compound citations, resident half only |
| `L-15` | **v0.3:** `§O5.2` restores Identity · Mission · Boundary, absent from v0.2's table | correction | `§O5.3` |
| `L-16` | **v0.3:** `§O5.4` states what `O5` verification does **not** establish | **weaker** | `§15` |

```text
LEDGER ROWS PRESENT:  16   (L-01 … L-16)

UPGRADES (weaker → stronger class):             1   (L-13)
DOWNGRADES / PRECISION GAINS:                   6   (L-01, L-03, L-04,
                                                     L-11, L-14, L-16)
CORRECTIONS:                                    1   (L-15)
STRUCTURAL:                                     7   (L-05, L-06, L-07, L-08,
                                                     L-09, L-10, L-12)
PROVENANCE STRENGTHENED, CONCLUSION UNCHANGED:  1   (L-02)
-------------------------------------------------------------------------
TOTAL ACCOUNTED:                               16   = ROWS PRESENT
```

**`F-2`, corrected under `ACT-CC-P13-008 §10`.** v0.3's counter read
`UPGRADES: 0` while row `L-13` reads *"stronger"* and names itself the only
upgrade, and the four counted categories reconciled 15 of 16 rows. Every row is
now accounted exactly once, `L-02` retained in its own fifth category
(`§9.1`: it *"MUST NOT be forced into one of the four other categories"*).

**The row-level facts are unchanged** — only the summary was stale.

**No proposal became canonical. No unknown became fact. No gap closed.**

---

## `§C` — v0.3 → v0.4 corrections

**Kept out of the `L-` series deliberately.** `ACT-CC-P13-008 §11` fixes the
accounting invariant at `COUNT(L-01 … L-16) = SUM(categories) = 16`. Adding
`L-17`/`L-18` would make the ledger reconcile 18 and break the invariant the
same Act requires. The two corrections are therefore recorded here, outside the
ledger, leaving the sixteen-row reconciliation exactly as `§10` prescribes.

| | Correction | Direction | Authority |
|---|---|---|---|
| `C-1` | `§O5.4` — completeness claim reclassified; `PREP-RECORD ≠ CANONICAL SCOPE` stated; a matching `NOT ESTABLISHED` line added | **weaker** | `§7`, `§8` |
| `C-2` | Change-ledger summary reconciled to all 16 rows across five named categories | **correction** | `§10`, `§11` |

**Neither is an epistemic upgrade.** `C-1` weakens a claim; `C-2` corrects
arithmetic without touching any row-level fact.

---

## Verification — `ACT-CC-P13-005 §13`

| # | Requirement | Result |
|---|---|---|
| 1 | v0.1 baseline integrity preserved | **VERIFIED** — `sha256 75775cbd…d5f1`, matches the Founder's `FD-P13-003 §2` |
| 2 | v0.2 is a distinct artifact | **VERIFIED** — separate path, separate file |
| 3 | v0.1 remains recoverable | **VERIFIED** — unmodified in tree and at commit `55d3d6b` |
| 4 | v0.1 original SHA256 remains verified | **VERIFIED** — re-checked after every write |
| 5 | Revision provenance recorded | **VERIFIED** — header, `§L`, `P13-008` |
| 6 | Evidence classes correctly separated | **VERIFIED** — five classes, `§0.1` |
| 7 | No unsupported epistemic upgrade | **VERIFIED** — `§L`: 0 upgrades |
| 8 | Corpus limitations accurately represented | **VERIFIED** — `§0.2`; `NOT FOUND ≠ FALSE` |
| 9 | Native Core remains 11 | **VERIFIED** — `MEASURED`, `§N` |
| 10 | `GAP-0001` remains OPEN | **VERIFIED** — `O1`, `§R`, `§Q` |
| 11 | P13 remains unauthorized for construction | **VERIFIED** — `P13 AUTHORIZED = False` from the instrument body |
| 12 | Canonicalization did not occur | **VERIFIED** — status block, `§0` |
| 13 | Founder-reserved matters unresolved | **VERIFIED** — 10 identified, 0 decided |
| 14 | Architect-reserved matters unresolved | **VERIFIED** — 2 identified, 0 decided |
| 15 | No self-authorization | **VERIFIED** — authority cited is `ACT-CC-P13-005` alone |
| 16 | No standing delegation expansion | **VERIFIED** — `DEL-T4.4-CF-001` untouched and uncited as basis |
| 17 | No certified evidence improperly modified | **VERIFIED** — no P10/P11/P12 file touched |
| 18 | Repository state internally consistent | **VERIFIED** — citation audit 0 errors; guard tests pass |

**`§13`'s own caution is adopted:** *"A passing test suite does not by itself
prove architectural correctness."* The suite proves the repository is
consistent; it does not prove `O1`'s proposal is right, and nothing here claims
it does.

### Negative controls — `§14`

| ID | Control | Result | Evidence |
|---|---|---|---|
| NC-01 | self-authorize | **HELD** | sole authority cited is `ACT-CC-P13-005` |
| NC-02 | issue its own authority | **HELD** | no instrument created this execution |
| NC-03 | create Native Core #12 | **HELD** | `MEASURED` 11; `§N` cat. 5 left `UNKNOWN` |
| NC-04 | modify Native Core #11 | **HELD** | no file under `native_core/` touched |
| NC-05 | canonically define P13 | **HELD** | `O1` marked `PROPOSED` in heading and `§D` |
| NC-06 | canonicalize v0.2 | **HELD** | status block; `§0` |
| NC-07 | authorize P13 construction | **HELD** | `P13 AUTHORIZED = False` |
| NC-08 | construct P13 | **HELD** | no code, test, schema, config; `p13/` absent |
| NC-09 | certify P13 | **HELD** | no certification statement exists |
| NC-10 | close `GAP-0001` by assertion | **HELD** | `O1`, `§R`, `§Q`, exit state all `OPEN` |
| NC-11 | overwrite v0.1 | **HELD** | hash unchanged, re-verified |
| NC-12 | erase historical provenance | **HELD** | `§L` records every change |
| NC-13 | resolve Founder-reserved matter | **HELD** | 10 identified, 0 decided |
| NC-14 | resolve Architect-reserved matter | **HELD** | 2 identified, 0 decided; conflict preserved |
| NC-15 | convert `UNKNOWN` into fact | **HELD** | 10 unknowns in, 10 out |
| NC-16 | convert `PROPOSED` into `CANONICAL` | **HELD** | `§L`: 0 upgrades |
| NC-17 | infer authority from necessity | **HELD** | `§N` cat. 5 left open *because* deciding it needs authority |
| NC-18 | infer approval from silence | **HELD** | no silence read as assent anywhere |

```text
HELD 18 · FAILED 0 · NOT EXERCISED 0 · UNKNOWN 0
```

---

## `§X` — Re-discovery — `ACT-CC-P13-005 §17`

Run fresh **after** revision and initial verification, as `§17` requires
(*"must not be skipped merely because the first revision pass succeeded"*).

| Probe | Finding |
|---|---|
| **Additional evidence?** | **Yes, one, and it is small:** the naive Native Core directory count returns **12** because `__pycache__` is a directory. Recorded in `§N` so a future reader does not mistake it for a broken freeze. **The boundary count is 11.** |
| **Contradictory source?** | **None found.** No resident source contradicts `NATIVE CORE = 11`, `P13 AUTHORIZED = False`, or any `CANONICAL` claim above |
| **Authority conflict?** | **None new.** `AD-P13-001` remains `CONFLICTED` and preserved; `FD-2` remains open and load-bearing — both pre-existing and disclosed |
| **New boundary issue?** | **None.** `§N` category 5 was already the known open question; it was not sharpened into a decision |
| **New dependency?** | **None.** `GAP-0001` still gates 21 |
| **Unresolved revision defect?** | **One, disclosed:** `O5`'s *"7 of 17 have canonical sources"* is `PREP-RECORD` and was **not** re-verified item-by-item against the resident tree this execution. It is the largest remaining `PREP-RECORD` claim carrying architectural weight. Listed in `§D.8` as evidence still required |
| **Verification failure?** | **None.** 18/18 requirements, 18/18 controls |

**New gaps registered: 0.** Registering a gap is the gap lifecycle's act, not
this draft's, and nothing found warranted one.

---

## Exhaustion — `ACT-CC-P13-005 §18`

```text
EXHAUSTED_WITH_CLASSIFIED_REMAINDER
```

**Exhausted as to the authorized scope.** All seven areas of `§6` were worked:
provenance, corpus transparency, epistemic classification, candidate surfaces,
Native Core boundary, terminology, decision readiness. No remaining work exists
inside this Act's boundary that is *sufficiently evidenced, actionable and
authorized*.

**The classified remainder, in three kinds — each with why it is not this Act's
to finish:**

| Remainder | Why not exhaustible here |
|---|---|
| **10 Founder-reserved + 2 Architect-reserved matters** | deciding them is outside this Act (`§9`, `§10`) |
| **`O5`'s 17-item classification not re-verified item-by-item** | verifiable in principle, but re-deriving all seventeen against the tree is a **new discovery operation**, not an artifact revision — outside `§1`'s scope. Disclosed rather than quietly left |
| **Direct corpus access (`GAP-0006`)** | the corpus is `NOT FOUND` in this repository; recovering it is a Founder matter, and `§11` forbids reconstruction |

**Exhaustion was not manufactured to obtain closure** (`§18`). The honest
terminal state has a remainder, and the remainder is named.

```text
EXHAUSTION DOES NOT MEAN:
  P13 is complete · P13 is canonical · GAP-0001 is closed ·
  P13 construction is authorized
```

---

## Exit state

```text
ACT-CC-P13-008         = EXECUTION COMPLETE  (F-1 / F-2 scope)
EXHAUSTION             = EXHAUSTED_WITH_CLASSIFIED_REMAINDER

P13 BLUEPRINT          = NON-CANONICAL DRAFT v0.4 — EXISTS
F-1 · F-2              = CORRECTED
O5                     = DIRECTLY VERIFIED (7/7 items named)
                         2 compound citations' corpus half NOT DIRECTLY VERIFIED
v0.1                   = PRESERVED · sha256 75775cbd…d5f1 · UNMODIFIED
v0.2                   = PRESERVED · sha256 a4095a33…9c57 · UNMODIFIED
v0.3                   = PRESERVED · sha256 6212a717…39e2 · UNMODIFIED
P13 CANONICAL DEF.     = NOT ESTABLISHED
GAP-0001               = OPEN · STILL THE APEX
REGISTER               = 28 — unchanged
P13 AUTHORIZATION      = NOT GRANTED
P13 CONSTRUCTION       = NOT AUTHORIZED
P13 CERTIFICATION      = NOT AUTHORIZED
NATIVE CORE            = 11 — MEASURED
CANONICALIZATION       = FOUNDER RESERVED

NEXT AUTHORITY GATE    = FOUNDER REVIEW → FOUNDER DECISION → CANONICALIZATION
```

**Nothing was constructed, canonicalized, authorized or certified.** No code,
test, contract, capability, Native Core boundary, subsystem, authority, Act or
decision was created or modified. No absent source was reconstructed. No gap was
closed. `docs/architecture/p13/` does not exist.

**This draft is a proposal to the Founder and nothing else.** v0.4 differs from
v0.3 in two places only: the `§O5.4` completeness claim is correctly classified
as a preparation-record enumeration, and the change ledger reconciles all
sixteen of its rows.
