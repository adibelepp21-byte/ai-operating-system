# T-12 — Scoped Ratification Instrument · **DRAFT**

> # DRAFT — PREPARED BY THE CO-FOUNDER OFFICE · AWAITING FOUNDER ISSUANCE
> Produced under `ACT-CC-P6-017 §18`, which permits preparing this instrument
> **if and only if** OPTION A is selected — it is. **This document confers no
> authority on itself.** `ACT-CC-P6-017 §16`: **Ratification Authority: NONE.**
> `§18`: the successor Act *"MUST STOP before execution unless explicit
> ratification authority is present."* It is not present.
>
> **Act ID: UNASSIGNED — see §0.1.**

**Prepared:** 2026-08-21 · **Predecessor:** `ACT-CC-P6-017`
**Decision consumed:** `DEC-P6-017 = OPTION A — SCOPED RATIFICATION` · `Confirmation: Moriarty` · 2026-08-22
**Mutation:** NONE · **Construction:** NONE · **Ratification:** NONE · **Commit:** NONE

---

## §0.1 — Act ID unassigned, and why I did not assign one

**[E]** The `§22` decision block's **Successor** field reads
`ACT-CC-P6-017 — T-12 Scoped Ratification Execution & Verification Gate` — which
is **this predecessor Act's own ID** (`Act ID: ACT-CC-P6-017`). A self-reference.

**[A] Two readings** — a transcription slip for `P6-018`, or an intent that the
gate be re-issued under the same number. **[E] `§23` requires STOP where a field
is *"incomplete, conflicting, or ambiguous"*.** **[A] It is not materially
blocking** — the decision itself is complete and unambiguous, and `§18` names the
instrument by *function*, not number — so I prepared the draft rather than
halting. **But I did not assign the ID on your behalf**, consistent with the same
call made on `ACT-CC-P6-013`'s unassigned successor field. The number is yours.

---

## §1 — `§18.1` Ratification target

**`AIOS_PHASE3_289_KNOWLEDGE_ADMISSION_MODEL_v1.0.md`** —
`docs/architecture/history/phase3/`, **159 lines**, SHA-256 `1c7b5eaa6102f151…`,
**unmodified against HEAD** (RV-01).

Ratified **as the canonical admission-model definition for T-12**, within the
scope at `§4`–`§6` and no further.

## §2 — `§18.2` Ratification version

| Field | Value |
|---|---|
| Document version | **v1.0**, as written — no amendment |
| Terminology state | includes the Phase 3.296 F-K1 hardening (Knowledge lifecycle = {Candidate, Active, Superseded}; *"deprecation"* reserved to Capability / Agent Definition) |
| Audit state | Phase 3.295 independent audit — **PASS WITH CONDITIONS**, its single condition (F-K1) closed by 3.296 |
| Integrity | the hash and line count above are the ratified article; any later differing text is **not** what was ratified |

## §3 — `§18.3` Canonical effect — **proposed, not performed**

**[E] Executing this instrument would make Phase 3.289 §1–§15 the canonical
admission model.** Concretely, the ratified content is:

lifecycle {Candidate → Active → Superseded}, no intermediate state · Memory as
sole candidate source, `occurrence_count` non-gating · human-authorized promotion
only · **exactly one gate** — Governance's `promotion_authorized`, affirmative
`True` only · reject absolute · conflict by governed human review · governed
replacement producing a new Active with the prior Superseded-and-retained ·
**new version, never in-place edit** · immutability of an admitted version ·
fail-closed on absence or non-authorization · Knowledge holds no authority.

### §3.1 **The downstream canonical entries — and a bundling hazard that must not be mishandled**

**[E] Three canonical entries name the T-12 item, and every one of them bundles
it with other reserved items:**

| Entry | Exact text | Composition |
|---|---|---|
| **Freeze §10** | *"Knowledge admission model **& versioned repository discipline** — design-only, open"* | **2 items** |
| **NCIR §9.5** | *"Reserved [O]: **admission model, versioned-repository discipline, consumption path**"* | **3 items** |
| **`knowledge_spec §14`** | *"[O] Admission model finalization. [O] Versioned-repository discipline. [O] Governed read/consumption path"* | **3 items** |

**[A] This ratification discharges only the *admission model* item in each.** The
other two are already addressed — **but by different instruments**:

```text
admission model              ←  THIS ratification
versioned-repository disc.   ←  DEC-P6-014, T12-D-002 (accept realized form)
consumption path             ←  DEC-P6-014, T12-D-001 (governed read-path not required)
```

**[A] The hazard is precise and this program has hit it three times before**
(`workflow_spec §14`, `skill_spec §14`, `NCIR §9.6`): an entry bundling several
items, where discharging one leaves the others mis-stated. **A synchronization
act that strikes these entries wholesale on the strength of ratification alone
would over-discharge; one that leaves them untouched would under-discharge.**
Each entry needs all three attributions, or none.

**[E] Also affected:** NCIR §9.5's *"**Blocked by [O]:** Knowledge admission
model"* — discharged by this ratification alone · Architecture Review checklist
**C-5**, *"Decide Knowledge admission/repository status: remain design-only [O] or
ratify"*, currently `[ ]` unchecked · `knowledge_spec §4/§12/§13`.

**[E] None of these is touched by this instrument.** Each is a canonical mutation
requiring its own explicit authorization. `ACT-CC-P6-017 §14`: **Mutation
Authority NONE.** They are enumerated here so the successor synchronization act
has an accurate target list rather than deriving one.

## §4 — `§18.4` Explicit exclusions

**[E] Ratification does NOT:**

| Excluded | Status |
|---|---|
| **T12-D-003** — validity-condition catalogue and semantics | **DEFERRED.** Not inferred from behavioural tests, from the observed `{}`, from the existing implementation, from 3.289 wording alone, or from engineering convenience |
| **T12-D-004** — storage facility | **DEFERRED.** No selection, provisioning, migration, or persistence architecture |
| **T12-D-006** — durable cross-process provenance | **PROCESS-SCOPED / ROUTED** to Identity/Authentication. No redesign, no reconstruction, no absorption of that authority into T-12 |
| **Governed read-path construction** | Not authorized. **D-001 = NOT REQUIRED** decides the *question*; it authorizes no construction. A future consumer may reopen it |
| Phase-6 construction · Knowledge store · repository construction · admission implementation · Knowledge consumption architecture beyond D-001 | **NOT AUTHORIZED** |
| **RU-5** | **NOT DISCHARGED** — remains OPEN, partially materialized |
| Conformance of the existing implementation | **NOT DEEMED FULL.** The behavioural evidence covers the five D-005 scopes; it is **not** blanket conformance evidence for every clause |

## §5 — `§18.5` Supersession notes

**[E] `ACT-CC-P6-017 §6` requires this section, and `§22` records the disposition
as `EXPLICITLY SUPERSEDED`.**

Phase 3.289 **§16** reserves nine items. **Two have since received explicit
Founder / Architect dispositions and are no longer reserved:**

| 3.289 §16 item | Superseded by | Current status |
|---|---|---|
| **1** — version-identifier scheme; **versioned-repository discipline** | **`DEC-P6-014` · T12-D-002** | **ACCEPT REALIZED FORM AS CANON-CONSISTENT** |
| **2** — **read / consumption path**, whether consumption needs governance | **`DEC-P6-014` · T12-D-001** | **NOT REQUIRED** |

**[E] These two reservations shall not be re-imported as unresolved merely
because the historical document retains the original reservation language.**

**[E] The remaining seven §16 items are preserved unchanged:**

| # | Item | Status |
|---|---|---|
| 3 | Storage-facility choice | DEFERRED — D-004 |
| 4 | **Validity-condition catalogue**; conflict-detection signals | DEFERRED — D-003 |
| 5 | Knowledge Trust Scoring | untouched — deferred by the Domain Model |
| 6 | Policy as a category of Knowledge | untouched — deferred by the Domain Model |
| 7 | Persistent cross-process trust of the promotion signal | ROUTED — D-006 → Identity/Authentication |
| 8 | Agent-Instance acting-path Trace of a governed decision | untouched |
| 9 | F-H2 / F-G2 | untouched, carried |

**[E] `§6`: this is a supersession clarification. It authorizes no new
architecture and does not retroactively rewrite Phase 3.289.**

## §6 — `§18.6` Deferred questions, restated so they cannot be absorbed by silence

```text
D-003  validity-condition catalogue      DEFERRED
D-004  storage facility                  DEFERRED
D-006  durable cross-process provenance  ROUTED → Identity/Authentication
T12-R-001  validity conditions never captured   ARCHITECTURAL DECISION (folded into D-003)
RU-5   building before admission model decided  OPEN — partially materialized
```

**[E] `§19`'s prohibited inferences are not drawn** — D-001 resolved ≠ read-path
authorized · D-002 resolved ≠ repository construction authorized · D-003 deferred
≠ validity semantics are empty · D-004 deferred ≠ storage approved · D-005
sufficient ≠ entire 3.289 behaviour proven · D-006 routed ≠ Identity/Auth decided.
**READY ≠ AUTHORIZED · RECOMMENDED ≠ DECIDED · DECIDED ≠ EXECUTED.**

## §7 — `§18.7` Evidence basis

| Layer | Evidence |
|---|---|
| **Canonical consistency** | Reconciliation (`P6-013`): **no contradiction found** between 3.289 and canon. Independently corroborated by the Phase 3.295 adversarial audit — PASS WITH CONDITIONS, condition closed by 3.296 |
| **Clause correspondence** | 20-row matrix, **C1=9 · C2=7 · C3=2 · C4=1 · C5=4** — *as recorded in `P6-013`, not re-graded here* |
| **Behavioural** | `P6-015`: **13 tests**, five scopes, all passing; every asserted value independently reproduced by a probe run outside the test assertions. **Disclosed:** 12 behavioural + **1 structural** (`E3`, an `issubclass` check duplicating the resident suite); `D1` subsumed by `D2`. Removing both, every scope retains behavioural coverage |
| **D-005** | **SUFFICIENT** — determined on evidence against `ACT-CC-P6-016 §6`'s eight sub-checks, **not** on the count |
| **T12-R-003** | **CLOSED within its defined evidence scope** — recorded as a subsequent assessment |
| **Regression** | `native_core` **601 OK (expected failures = 1 — P7-F-2)** · `tools` **49 OK** |

## §8 — `§18.8` Known citation defect — **preserved with disclosure**

**[E] `§22` disposition: `PRESERVE WITH DISCLOSURE`.**

Phase 3.289 **§8** and **§16** cite *"Impl Constitution §13"*. **[E] The
Implementation Constitution ends at §12**, and its **§12 — Reserved Future
Topics** is where *"Version-identifier scheme; migration and deprecation
workflow"* actually appears.

**[E] Pointer wrong, substance traceable and correct.** The defect is
**disclosed, not corrected**, and **shall not be represented as having been
corrected by this ratification.** No amendment of the historical document is
authorized (`§7`, `§14`).

**[A] A second citation of the same class exists but is out of scope here:**
`models.py:31` cites `knowledge_spec §6/§22`, and that spec has **14** sections.
It sits in the implementation, is **`T12-R-007`**, and is **routed to a
Maintenance Baseline** under GDR-0010 Ruling 3 — not to this instrument.

## §9 — `§18.9` Historical record protection

**[E] `§20` declares these immutable, and none was altered:**

| Record | Verified state |
|---|---|
| `ACT-CC-P6-013` reconciliation | **PARTIALLY ESTABLISHED**; `C1=9 C2=7 C3=2 C4=1 C5=4`; **T12-R-003 still HIGH / OPEN** |
| `ACT-CC-P6-014` disposition | unchanged |
| `ACT-CC-P6-015` behavioural evidence | unchanged |
| `ACT-CC-P6-016` readiness assessment | unchanged |

**[E] Every reassessment is recorded as a new state**, never as a rewrite. **[A]
In particular, the seven C2 rows and one C4 row that the behavioural evidence
bears on (`1b, 2, 4, 5, 7, 9, 15`) are *not* re-graded here.** Whether the
ratified model warrants re-grading them is work for a separate assessment with
this instrument in hand.

## §10 — `§18.10` Mutation authority

# **NONE**

No canonical artifact may be mutated. Freeze §10, NCIR §9.5, `knowledge_spec`,
the Domain Model, the Relationship Model, the Governance Decision Register and
the Finding Register are **untouched** — verified: `git diff` over all tracked
paths is **empty**.

## §11 — `§18.11` Construction authority

# **NONE**

No Knowledge store · no repository construction · no admission implementation ·
no governed read-path · no storage provisioning · no Identity/Auth construction ·
**no Phase-6 construction.**

## §12 — `§18.12` Effective date

**[D] Not set.** The instrument takes effect only on an explicit Founder /
Architect ratification authorization (`§13`). **[E] `ACT-CC-P6-017 §16`:
Ratification Authority NONE** — so no effective date can be entered by me, and
none is.

## §13 — `§18.13` Founder / Architect confirmation — **UNFILLED**

```text
T-12 SCOPED RATIFICATION — EXECUTION AUTHORIZATION

Act ID:               ____________________   (unassigned — see §0.1)

Authorization:
[ ] EXECUTE the scoped ratification as drafted above
[ ] EXECUTE with the amendments stated below
[ ] DO NOT EXECUTE — return for revision

Amendments (if any): ____________________

Ratification Authority:  ____________________   (must read GRANTED to execute)
Mutation Authority:      ____________________   (required for the §3.1 canonical
                                                 synchronization; NONE by default)
Construction Authority:  NONE
Effective Date:          ____________________

Founder / Architect: ____________________      Date: ____________________
Confirmation:        ____________________
```

**[E] Left unfilled.** `§13.MAY-NOT.3`: I may not select the option. **[E] `§18`:
this instrument STOPS before execution — explicit ratification authority is not
present.**

---

## §14 — `§17` Verification — twelve checks

| ID | Requirement | Result |
|---|---|---|
| **RV-01** | Phase 3.289 source unchanged | ✅ unmodified vs HEAD · `1c7b5eaa…` · 159 lines |
| **RV-02** | D-003 remains deferred | ✅ §4, §6 — no validity semantics inferred from any source, including the observed `{}` |
| **RV-03** | D-004 remains deferred | ✅ §4 — no facility named, selected or provisioned |
| **RV-04** | D-006 remains routed | ✅ §4, §5 item 7 — Identity/Authentication untouched |
| **RV-05** | D-001 explicitly represented as NOT REQUIRED | ✅ §4, §5 item 2, §6 |
| **RV-06** | D-002 explicitly represented as accepted realized form | ✅ §5 item 1, §6 |
| **RV-07** | D-005 evidence scope is exactly the approved scope | ✅ five test classes, one per approved clause — `ScopeA…ScopeE`; **nothing beyond** |
| **RV-08** | `P6-013` record unchanged | ✅ §9 — verified at source, still HIGH/OPEN with the original matrix |
| **RV-09** | Citation defect explicitly disclosed | ✅ §8 |
| **RV-10** | The two superseded §16 reservations explicitly handled | ✅ §5, with the remaining seven enumerated and preserved |
| **RV-11** | No new architectural semantics introduced | ✅ §3 ratifies 3.289 §1–§15 **as written**; every statement here is quotation, status, or exclusion |
| **RV-12** | No construction authorization created accidentally | ✅ §11; §3.1's canonical effects are listed as **proposed targets requiring separate authorization**, never as performed |

**Additional integrity:** `git diff` over all tracked paths **empty** · P7-F-2
five sites and `@unittest.expectedFailure` marker intact · entity count **12** ·
core boundaries **11** · Domain Model **26** ratified edges · governance register
mutations **0**.

## §15 — `§24` Successor path *(identification only)*

```text
DEC-P6-017 = OPTION A                    ✅ recorded
        ↓
THIS scoped ratification instrument      ✅ prepared — DRAFT, unissued
        ↓
Founder ratification authorization       ⏸  §13 unfilled
        ↓
Ratification executed                    ⛔ not authorized
        ↓
Canonical synchronization                ⛔ separate authority; targets at §3.1,
                                            each needing all three attributions
        ↓
Independent verification                 ⛔
        ↓
Phase 6 reassessment                     ⛔ separate, and not implied
```

**In parallel and independent:** a **Maintenance Baseline instrument** for
`T12-R-004` and `T12-R-007`-`models.py`, under `P7-F-1` → GDR-0010 Ruling 3.

## §16 — `§26` State declaration

```text
T-12                    READY WITH SCOPED DEFERRALS
DEC-P6-017              DECIDED — OPTION A — SCOPED RATIFICATION
Phase 3.289             NOT RATIFIED — instrument drafted, unissued
D-001                   DECIDED — NOT REQUIRED
D-002                   DECIDED — ACCEPT REALIZED FORM
D-003                   DEFERRED
D-004                   DEFERRED
D-005                   SUFFICIENT / SCOPED
D-006                   ROUTED
T12-R-003               CLOSED WITHIN DEFINED EVIDENCE SCOPE
T12-R-004 / R-007       MAINTENANCE BASELINE PATH
RU-5                    OPEN
Phase 6 Construction    NOT AUTHORIZED
MUTATIONS PERFORMED     0
```

**`§21` — Commit Authority: NONE.** This draft joins the five prior artifacts and
the evidence module as uncommitted, pending explicit path-specific authority.

**`§25` — STOP.** Decision recorded · scoped successor prepared and identified ·
nothing ratified, constructed, mutated, or inferred.
