# `ACT-CC-P12-008` — W6 Consumer Measurement Correction & Semantic Classification Gate

**Headline.** The measurement defect is corrected, the corrected result is
independently verified by a second mechanism, and the semantic question two
prior Acts recorded as *unsettled* turns out to be **settled by the instrument
body** — which those Acts had not read. `§16 State Consumers` enumerates
`verification` and `self-model` among the nine kinds a consumer may be.

**W6 STATE now reports 4 of 4 links SATISFIED.** That verdict moved because a
defective measurement was corrected and a canonical definition was read from its
source — not because a threshold was moved or a consumer was manufactured.
`§9` was the constraint under which every decision below was taken.

---

## `O1` — Execution Identity

| Item | Value |
|---|---|
| Act | `ACT-CC-P12-008` — non-Micro-Act execution mandate, executed end-to-end |
| Branch | `claude/aios-activation-authority-discovery-enq7bk` |
| Starting commit | `04ad53d` — *"P12-007: record the post-commit control inventory…"*; tree clean |
| Execution state | **COMPLETE** — all of `§14`'s `C1`–`C12` satisfied |

**Changed files**

| File | Change |
|---|---|
| `tools/p12_state_verification.py` | `consumers_of()` corrected; `importers_of()`, `consumption_evidence()`, `ConsumerEvidence`, `CONSUMER_KINDS`, `PROJECTION_READS` added; `_link_consumer` reports both figures |
| `tools/p12_consumer_evidence_verifier.py` | **new** — independent dynamic verifier, imports nothing from the measurement |
| `tools/tests/test_p12_consumer_measurement.py` | **new** — 19 controls: `NC-01`…`NC-05` plus semantic-classification controls |
| `tools/tests/test_p12_state_verification.py` | five controls realigned to the corrected truth, one added |
| `tools/p12_negative_control_verification.py` | `_state_chain` inverted; `_consumer_evidence_verifier` control added |
| `docs/architecture/p12/P12-W6-STATE-VERIFICATION.md` | **new** — the STATE scope item's evidence |
| `docs/architecture/p12/P12-008-RETURN-PACKAGE.md` | this document |

**Deliberately not changed:** `P12-W2-UNIFIED-OPERATIONAL-STATE.md §9` and
`P12-W6-SCOPE-DISCOVERY-AND-CLASSIFICATION.md` record what W6 measured when
written and were **not edited**. The new measurement is recorded in a new
document. History is not rewritten to agree with the present.

---

## `O2` — Canonical Source Basis

`§3` required the actual instrument bodies, and forbade inferring authority from
a filename, identifier, index row, search hit, test name, existing
implementation or previous report wording. Read this Act:

| Source | Section | What it actually says |
|---|---|---|
| `docs/architecture/p12/AIOS_P12_ROADMAP_PRD_CONSTRUCTION_BLUEPRINT_v1.0.md` | **`§16 State Consumers`** | *"P12 shall discover actual consumers rather than assume them. Consumers may include: runtime; workflow; organization; governance; **verification**; **self-model**; **observability**; **evidence**; reconciliation. Each claimed consumer requires evidence that it actually consumes the state."* |
| same | **`§17 State Authority`** | `STATE → AUTHORITATIVE SOURCE → PROJECTION → CONSUMER`; a `STATE AUTHORITY CONFLICT` must be discovered and resolved or escalated |
| same | `§14`, `§15`, `§18` | state domains; sources (`MEMORY ≠ AUTHORITY`); lifecycle |
| `tools/p12_state_verification.py` | module docstring | the **paraphrase** that misled two prior Acts — see `O9` |

**The decisive finding.** `§16` names `verification`, `self-model`,
`observability` and `evidence` as consumer kinds. `ACT-CC-P12-006 O8` and
`ACT-CC-P12-007 O19` recorded *"is a verifier a consumer?"* as **semantically
unsettled**, reasoning from the implementation's docstring — which quotes `§16`'s
first and last sentences and omits the enumeration between them. `§3` of this
Act exists to catch exactly that, and it did.

**The counterweight, from the same section.** Being a named kind is not
sufficient: *"Each claimed consumer requires evidence that it actually consumes
the state."* Import is not that evidence.

---

## `O3` — Measurement Defect

The superseded implementation, in full:

```python
if isinstance(node, ast.ImportFrom) and node.module:
    modules = [node.module]
elif isinstance(node, ast.Import):
    modules = [alias.name for alias in node.names]
if any(stem in module for module in modules):
```

**One expression, two opposite defects.**

| Defect | Mechanism | Consequence |
|---|---|---|
| **False negative** (the known one) | `from tools import p12_operational_state as state` parses with `node.module == "tools"`; the surface's name is in `alias.name`, which was never collected. `"p12_operational_state" in "tools"` is `False` | **every** resident importer uses this form, so the measurement reported **0** consumers for a surface that has real ones |
| **False positive** (found this Act) | `stem in module` is a substring test. `"p12_operational_state" in "tools.p12_operational_state_verifier"` is `True` | a module importing only the *verifier* would have counted as a consumer of the *surface* |
| **Insufficient evidence** (found this Act, from `§16`) | import alone was treated as consumption | correcting only the shape would have moved `CONSUMER` to SATISFIED on three matches, one of which never reads the system's state |

The third is the one that mattered most: the narrow fix would have produced the
right verdict for the wrong reason, which `§9` forbids as surely as the wrong
verdict.

---

## `O4` — Correction

**Import resolution is by module identity**, never by substring, across the five
shapes the repository demonstrates — `§4.1.A` forbade limiting the fix to the
known example:

```python
from pkg import surface            from pkg import surface as s
import pkg.surface                 import pkg.surface as s
from pkg.surface import project
```

**Consumption evidence** makes `§16`'s closing sentence measurable. A read is a
call to the surface's projection API (`project`, `conflicts`, `declares`,
`summary`); a read inside a `with` block that substitutes the surface is
recorded separately as a **fixture read** — not dropped, not counted:

```python
@dataclass(frozen=True)
class ConsumerEvidence:
    module: str
    reads: Tuple[str, ...]           # over the resident sources
    fixture_reads: Tuple[str, ...]   # over a substituted source set
```

**Why this is semantically correct rather than convenient.** `§16` asks two
things and the code now answers two things: `importers_of()` answers *who binds
this name*; `consumers_of()` answers *who has evidence of consuming*. The
distinction is the repository's own `IMPORT ≠ CONSUMER` invariant, and it is what
keeps this a correction rather than a redefinition. `CONSUMER_KINDS` is `§16`'s
list verbatim and in its order; a test reads it back out of the instrument body.

**Not a redesign.** `§17`'s chain, its four links, the surface, and W2 are
untouched. One function was corrected and two were added beside it.

---

## `O5` — Corrected Measurement

Complete result for `tools.p12_operational_state`, reproduced in a fresh process:

| Module | `§16` kind | Reads (resident) | Reads (fixture) | Consumer? |
|---|---|---|---|---|
| `tools/p12_self_model_contract.py` | **self-model** | `project` | — | **YES** |
| `tools/p12_negative_control_verification.py` | **verification** | `summary` | `project` | **YES** |
| `tools/p12_mutation_verification.py` | verification | — | `conflicts` | **NO** |

```text
importers_of()  →  3
consumers_of()  →  2
CONSUMER        →  SATISFIED
```

**Full `§17` chain:** `STATE` SATISFIED · `AUTHORITATIVE SOURCE` SATISFIED ·
`PROJECTION` SATISFIED · `CONSUMER` SATISFIED — **4 / 4, chain complete,
0 authority conflicts, 0 undeclared claims.**

---

## `O6` — Independent Verification

`§4.1.C` forbade *"reproducing the same implementation logic in a different
function"*. `tools/p12_consumer_evidence_verifier.py` **does not parse Python**
and imports nothing from the measurement. Its method is dynamic observation: it
wraps the surface's projection entry points with a recorder, **actually calls**
each candidate's own function, and records for every projection call whether
`surface.SOURCES` **is** the resident tuple at that moment — identity, not
equality. The AST infers substitution from a `with` block's extent; this watches
it happen.

```text
p12_self_model_contract.projection_freshness_is_not_source_freshness
    resident=['project']                        substituted=[]
p12_negative_control_verification._operational_state_projection
    resident=['conflicts','project','summary']  substituted=['project']
p12_mutation_verification._alter_state_authority
    resident=[]                                 substituted=['conflicts']
```

| `§4.1.C` requirement | Check | Result |
|---|---|---|
| 1 the previously missed shape is recognized | `the missed import shape is recognized` | **AGREES** — 3 of 3 |
| 2 nothing omitted, nothing invented | `consumers are neither omitted nor invented` | **AGREES** — observed set == measured set |
| 3 unrelated/superficial matches excluded | `a substituted read is not counted` | **AGREES** — the fixture-only reader is observed and is not counted |
| 4 (added) prefix name is not the surface | `a prefix name is not the surface` | **AGREES** |

**4 AGREES / 0 DISAGREES / 0 UNOBSERVABLE**, in-process and in a fresh process.
The claim is **passed in** rather than imported — that is what keeps the module
independent, and an AST control enforces it.

---

## `O7` — Negative Controls

| ID | Requirement | Control | Outcome |
|---|---|---|---|
| **NC-01** | previously missed shape now detected | `NC01ThePreviouslyMissedImportShape` — five import forms in a temp world; plus a control keeping the old rule's blindness (`node.module == "pkg"`) as a standing reminder | **PASS** — 5 / 5 recognized |
| **NC-02** | irrelevant textual reference | `NC02AnIrrelevantTextualReference` — docstring, string literal and comment all naming the surface | **PASS** — 0 importers, 0 consumers |
| **NC-03** | unrelated import | `NC03AnUnrelatedImport` — a module whose name *contains* the surface's, plus an unrelated import | **PASS** — and the old expression's truth is pinned: `"p12_operational_state" in "tools.p12_operational_state_verifier"` |
| **NC-04** | verifier-only usage | `NC04VerifierOnlyUsage` — both directions: an importer that never reads, and a read over a substituted source set, are **not** consumers; a verifier that really reads **is** | **PASS** — 5 controls, including dynamic confirmation |
| **NC-05** | fresh-process reproduction | `NC05FreshProcessReproduction` — subprocess re-derives the consumer set, importer set and link status | **PASS** — identical |
| *added* | the kinds come from the instrument | `TheSemanticClassificationRestsOnTheInstrument` — reads `§16`'s section out of the Blueprint and asserts every kind appears in it | **PASS** |
| *added* | independence is structural | `test_the_independent_verifier_does_not_import_the_measurement` | **PASS** — this one failed first; see `O10` |

**Instrument falsifiability (`§18` of the governing Act):** 27 → **28
instruments, 28 DEMONSTRATED**. The new verifier carries a real control (fed a
claim that omits a real consumer, and one that invents the fixture-only reader
as a consumer; it rejects both), and `_state_chain` was **inverted, not
weakened** — it now asserts the live SATISFIED and drives the link *down* two
ways.

---

## `O8` — Semantic Classification

| Surface | Classification | Authority |
|---|---|---|
| `tools/p12_self_model_contract.py` | **W6 CONSUMER** — kind: `self-model` | `§16` names `self-model`; evidence: reads `project()` and uses `entries["runtime.observed"].observed_at` / `.status` to answer a W5 question |
| `tools/p12_negative_control_verification.py` | **W6 CONSUMER** — kind: `verification` | `§16` names `verification`; evidence: reads `summary()` over the resident sources before any substitution |
| `tools/p12_mutation_verification.py` | **NOT a W6 consumer** — kind would be `verification`; evidence absent | `§16`'s closing sentence. Every projection call it makes is over a substituted `SOURCES`; observed dynamically as well as by AST |
| `tools/p12_operational_state_verifier.py` | **not an importer of the surface at all** | it is a different module whose *name contains* the surface's; the superseded substring rule would have counted it |
| any `tools/tests/*` | **not a consumer** | `§16` lists nine kinds and `test` is not among them; a test proves importability, not consumption |

**The prohibited inferences were not used.** Neither `imports state → therefore
consumer` nor `used by verifier → therefore operational consumer` appears
anywhere in the classification: the first is refused by the evidence
requirement, the second by `O9`'s explicit separation of *consumed* from
*executed*.

---

## `O9` — Semantic Uncertainty

**The central question is `SETTLED`, and the record of it being open was an
error of reading, not a gap in the corpus.**

| | |
|---|---|
| Question | *Does a verifier that reads operational state constitute a W6 CONSUMER?* |
| Prior classification | `SEMANTICALLY UNSETTLED` (`ACT-CC-P12-006 O8`, `ACT-CC-P12-007 O19`) |
| **Corrected classification** | **`SETTLED BY CANONICAL AUTHORITY`** — `§16` enumerates `verification` among the consumer kinds |
| Why it was recorded as unsettled | the prior reading came from `tools/p12_state_verification.py`'s docstring, which quotes `§16`'s first and last sentences and omits the enumeration. `§3` of this Act forbids inferring authority from an existing implementation, and this is the case it was written for |

**What remains genuinely unsettled — and is smaller than it sounds:** `§16` says
what kinds *may* be consumers and that evidence of consumption is required. It
does not define what counts as a read for an arbitrary surface. This Act used
the surface's own declared projection API, which is well-defined for
`p12_operational_state` and is a **heuristic** if `consumers_of()` is pointed at
a module with a different shape. Recorded as a **scope limitation of the
instrument**, not as an authority gap: no `§19` item currently depends on it.

**No authority gap was found**, and none was manufactured. `§7` was not reached:
every action this Act needed was inside its own grant.

---

## `O10` — Defects Discovered

| # | Defect | Origin | How caught | Disposition |
|---|---|---|---|---|
| 1 | `consumers_of()` false negative — blind to `from X import Y as z` | pre-existing | `ACT-CC-P12-006` | **Corrected** |
| 2 | `consumers_of()` **false positive** — `stem in module` counts a prefix match, so the verifier would have counted as the surface | pre-existing, **found this Act** | reading the expression rather than the reported symptom | **Corrected**; `NC-03` pins it |
| 3 | `_link_consumer` treated import as consumption, contrary to `§16`'s closing sentence — which its own docstring already cited | pre-existing, **found this Act** | reading `§16`'s body | **Corrected**; the link now reports importers and evidenced consumers separately |
| 4 | Two prior Return Packages recorded a settled question as unsettled, on a docstring paraphrase | pre-existing, **found this Act** | `§3`'s requirement to read the instrument body | **Corrected here**, in `O9`. The prior packages are **not edited** |
| 5 | **Self-introduced.** `p12_consumer_evidence_verifier.main()` imported `p12_state_verification` for convenience, breaking the independence the module's own docstring asserts | this Act | **this Act's own control** `test_the_independent_verifier_does_not_import_the_measurement` | **Fixed at the source**: `main()` now prints only what it observed. The control was not narrowed to permit it |
| 6 | **Self-introduced.** The verifier used `str.replace`, which the resident *"this module writes nothing"* control reads by AST and cannot distinguish from `Path.replace` | this Act | the same suite | **Fixed by not using the name** (`"/".join(...)`). Narrowing a real write-check to accommodate a cosmetic choice was rejected |
| 7 | Five existing controls pinned the pre-correction state and failed | expected | full suite | **Realigned, not relaxed** — see below |
| 8 | `_state_chain` negative control assumed the live link was UNSATISFIED | expected | instrument falsifiability run | **Inverted**: asserts live SATISFIED, drives it down two ways |

**On finding 7 — realigned, not relaxed.** `test_the_projection_currently_has_no_consumer`
asserted the set was empty and said in its own message: *"if a consumer has been
wired, the STATE item's classification must be updated rather than this control
relaxed."* It is now `test_the_evidenced_consumer_set_is_exactly_this`, pinning
the two-element set **exactly**, so drift in either direction still fails.
`TheItemIsNotClosed` became `TheItemIsClosedByMeasurementNotByAssumption` and
gained `test_closure_rests_on_evidence_that_can_be_withdrawn`, which drives the
chain back to incomplete. `test_a_real_consumer_is_found_when_one_exists` now
builds a fixture that actually reads, plus one that only imports, and asserts
both outcomes. **No assertion was deleted or weakened; each was made stricter.**

---

## `O11` — Regression

| Suite | Result |
|---|---|
| Targeted — `test_p12_consumer_measurement` | **19 OK** |
| Targeted — `test_p12_state_verification` | **17 OK** |
| `native_core` | **801 OK** (1 **expected failure**, still distinguished from a regression) |
| `consumers` | **276 OK** |
| `tools` | **1163 OK** (1 skip) — up from 1142 by this Act's 19 new and 2 added controls |

**`§51` regression classes:** 11 classes, **10 HELD, 0 REGRESSED**, 1 UNANCHORED
(`quality` — pre-existing: no resident linter, formatter, coverage threshold or
CI configuration). **`§50` mutations:** 10 attempted, **8 DETECTED, 2 MISSED**
(`forge decision`, `duplicate delegation`) — unchanged and untouched.
**`§49` system controls:** 13 attempted, **12 REFUSED, 1 ACCEPTED**
(`false certification`, Founder-reserved) — unchanged.

---

## `O12` — Fresh-Process Verification

Every figure below was re-derived in a **separate OS process**:

| Item | Result |
|---|---|
| `consumers_of(SURFACE)` | `p12_negative_control_verification`, `p12_self_model_contract` |
| `importers_of(SURFACE)` | those two plus `p12_mutation_verification` |
| per-module evidence | identical `reads` / `fixture_reads` split |
| `§17` chain | 4 / 4 SATISFIED, chain complete |
| independent verifier | 4 AGREES / 0 DISAGREES |
| instrument falsifiability | 28 / 28 DEMONSTRATED |
| `§49` · `§50` · `§51` | 12/1 · 8/2 · 10 held |
| resident 8-stage fresh-process instrument | **8 / 8 REPRODUCED** |
| W1 · W2 · W3 · W4 · W5 · P13 · Native Core | all unchanged (see `O15`) |

---

## `O13` — Citation Audit

| | |
|---|---|
| documents scanned | **268** (including both new documents and this package) |
| citations checked | **1578** |
| **errors** | **0** |
| warnings / non-resident / text mismatches | 87 / 63 / 0 — all pre-existing |

Nothing suppressed; every cross-reference introduced by this Act resolves.

---

## `O14` — Control Inventory

| | Before | After |
|---|---|---|
| declared control inventory (`§51` functional anchor) | 2536 | **2555** |
| removed | — | **0** |
| weakened | — | **0** |
| falsifiable instruments | 27 | **28**, all DEMONSTRATED |
| `tools` suite | 1142 | **1163** |

---

## `O15` — Boundary Integrity

| Boundary | Before | After |
|---|---|---|
| **W1** | 8 edges · 4 verified / 3 unverified / 1 reserved · 8 owners unresolved | identical |
| **W2** | 8 sources / 8 projections | identical — the surface was read, never modified |
| **W3** | `{records 3, structured 0, prose 2, refusal-type 0, governance surface 2}` | identical; broader `§16` chain still `AUTHORITY-GAP` |
| **W4** | 4 manifests / 4 joined / 0 dangling | identical; `W4-GAP-008` and `W2-GAP-007` not reopened |
| **W5 / `P12-007` authority integration** | 12/12 BOUND, kinds `8/3/1` | identical |
| **P13** | `AUTHORIZED = FALSE` | identical — not authorized, not constructed |
| **`F-16` / `F-17` / `F-18`** | unresolved | unresolved, untouched |
| **`OA-001`** | `OA-1 — NOT-A-GAP` | unchanged; no scheduler, daemon, queue or self-activation exists or was created |
| **Native Core** | 11 | **11** |
| **Founder-reserved false-certification control** | `ACCEPTED` | identical, byte-identical source |
| **`docs/program/AIOS_*`** | `sha256 abfc6b09…` | **`sha256 abfc6b09…`** — identical, 0 pending changes |
| **certified P10 / P11 evidence** | — | 0 pending changes |

---

## `O16` — Evidence Locations

| Evidence | Location |
|---|---|
| Canonical `§16` / `§17` bodies | `docs/architecture/p12/AIOS_P12_ROADMAP_PRD_CONSTRUCTION_BLUEPRINT_v1.0.md` |
| STATE scope item evidence | `docs/architecture/p12/P12-W6-STATE-VERIFICATION.md` (§§1–7) |
| Corrected measurement | `tools/p12_state_verification.py` — `consumers_of`, `importers_of`, `consumption_evidence`, `CONSUMER_KINDS` |
| Independent verification | `tools/p12_consumer_evidence_verifier.py` |
| Falsification | `tools/tests/test_p12_consumer_measurement.py` (19), `tools/tests/test_p12_state_verification.py` (17) |
| Instrument falsifiability | `tools/p12_negative_control_verification.py` — `_state_chain`, `_consumer_evidence_verifier` |
| This package | `docs/architecture/p12/P12-008-RETURN-PACKAGE.md` |

---

## `O17` — Frontier Status

**`CLOSED`.**

`§16`'s ten rediscovery questions, answered from fresh repository state:

1. **Did the correction close the defect?** Yes — three defects, two of them
   found during this Act.
2. **Corrected inventory?** 3 importers, 2 evidenced consumers.
3. **Which are actual W6 consumers?** `p12_self_model_contract` (self-model),
   `p12_negative_control_verification` (verification).
4. **Which are other roles?** `p12_mutation_verification` — importer and
   fixture-only reader, not a consumer.
5. **What authority supports this?** `§16 State Consumers`, quoted in `O2`.
6. **Does W6 STATE remain UNSATISFIED?** No — **SATISFIED, 4 / 4, chain
   complete**, on corrected measurement and canonical definition.
7. **Another executable W6 frontier?** See `O19`.
8. **Another authorized P12 frontier?** See `O19`.
9. **New authority gap?** **None.** One instrument scope limitation recorded in
   `O9`; no `§19` item depends on it.
10. **Is P12 exhausted?** See `O18`.

`§15` was applied: no further ordinary step remains *inside this frontier*, so
execution stopped here rather than expanding into a different one.

---

## `O18` — P12 Exhaustion

Remaining P12 surface, rediscovered fresh after construction stopped:

| Frontier | Classification |
|---|---|
| `consumers_of()` measurement + semantic classification | **CLOSED** (this Act) |
| P13 authorization-state representation | **ALREADY SATISFIED** (`ACT-CC-P12-007`) |
| `false certification` + `§50` `forge decision` | **FOUNDER-RESERVED** — one root cause: no canonical definition of issuance authenticity |
| `§50` `duplicate delegation` | **SOURCE-GAP** — no canonical prohibition; `DP-02 §11` item 10 legitimises multi-context grants |
| W6 EVIDENCE / E12 matrix | **FOUNDER-RESERVED** — `F-16`, `§54` `TBD` |
| CROSS-PD interfaces | **ARCHITECT-RESERVED + SOURCE-GAP** — `F-18`, `ADR-0029`, `ESC-C7-01` |
| Phase ↔ PD provider | **FOUNDER-RESERVED** — `F-17` |
| RUNTIME `verification` · FAILURE `VERIFIED` | **FOUNDER-RESERVED** — ratified execution vocabulary holds three states |
| W3 broader `§16` governance chain | **AUTHORITY-GAP** — unchanged, untouched |
| FAILURE `RETRYABLE` · PROVENANCE `NOT ASSEMBLABLE` (3 historical) · resident non-manual activation | **NOT-A-GAP** |
| CROSS-PHASE `P6` / `P7` | **OUT-OF-SCOPE** — W6 measures work, it does not manufacture it |
| `quality` regression anchor · widening the two non-refusing W1 run scopes | **OPTIONAL** |
| W6 STATE projection exercised by **real system work** | **NOT-A-GAP for W6** — reported `NOT EXERCISED`; manufacturing a path is forbidden by `§9` |

**`O18: P12 NOT EXHAUSTED — EXECUTABLE FRONTIER REMAINS.`**

The remaining executable surface is **thin and optional**: of the frontiers
above, none is both authorized-and-unblocked *and* required by a canonical
`§19` item. The one item that is authorized and unblocked — anchoring the
`quality` regression class with a resident linter or CI configuration — is
genuinely `OPTIONAL` (see `O19`), and `P12 EXHAUSTED` would therefore be a
premature return rather than a false one. Every other remaining item is
Founder-reserved, Architect-reserved, a source gap, not a gap, or out of scope.

`FRONTIER CLOSED ≠ P12 EXHAUSTION`, and `§15` forbids expanding this Act to
close the difference.

---

## `O19` — Next Action

**Not executed here.** `§15`: a frontier outside this one is recorded, not
entered.

| Field | Value |
|---|---|
| **Name** | Anchor the `§51` `quality` regression class with a resident quality gate |
| **Scope** | A linter/formatter configuration and, if the environment permits, a CI configuration that runs the three suites |
| **Classification** | **OPTIONAL — EXECUTABLE NOW** |
| **Authority** | Delegated. Tooling is ordinary engineering. **`FDP-P10-002 Quality` is Founder-reserved and would *not* be resolved by it** — anchoring the class is not ratifying a quality standard |
| **Dependency** | none |
| **Why it is optional** | it closes no `§19` scope item. `quality` is the only one of eleven regression classes with no anchor, and `UNANCHORED` is honest reporting rather than a failure |
| **Why not executed here** | it is a **different frontier**. `§15`: *"Do not silently expand this Act into that frontier"* |

Everything else remaining is reserved, a source gap, not a gap, or out of scope
— as itemised in `O18`.

---

## Constraint Compliance

| Constraint | This Act |
|---|---|
| `§3` actual instrument bodies | held — `§16`/`§17` read from the Blueprint; the finding in `O9` is the direct result |
| `§4.1.A` correction not limited to known examples | held — five import shapes, resolved by module identity |
| `§4.1.C` independent verification | held — dynamic observation, imports nothing from the measurement, AST-enforced |
| `§4.1.D` classification from authority | held — `§16`'s enumerated kinds, verbatim; both prohibited inferences refused |
| `§5` no W6 redesign, no redefinition without authority | held — one function corrected, two added; `§17`'s chain untouched |
| `§5` W1 / W2 / W3 / W4 / P13 / `F-16`–`F-18` / `OA-001` / Native Core / protected packages | held — `O15`, all identical |
| `§8` `READS STATE ≠ OPERATIONAL CONSUMER` | held — `§16` decides the kind; evidence decides the instance; `O9` keeps *consumed* separate from *executed* |
| `§9` no metric gaming | held — the verdict moved on a corrected measurement and a read instrument; a narrower fix that would have produced the same verdict on worse evidence was **rejected** (`O3`, defect 3) |
| `§10` NC-01…NC-05 | held — `O7`, all passing, plus two added |
| `§11` real system work distinguished | held — `consumed` YES, `executed by real work` **NO**, reported not manufactured |
| `§12` regression and disclosure | held — `O10`, `O11`; two self-introduced defects disclosed and fixed at the source, neither by narrowing the control that caught it |
| `§13` protected boundaries | held — `O15`, before/after hashes identical |
| `§14` `C1`–`C12` | all satisfied |
| `§15` exhaustion rule | held — same frontier completed; a different one recorded, not entered |
| `§16` post-construction rediscovery | held — `O17`, from fresh state |
| `§18` invariants | held throughout; `AST MATCH ≠ SEMANTIC CONSUMER` is the one this Act is about |
