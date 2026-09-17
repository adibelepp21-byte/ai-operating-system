# `ACT-CC-P12-007` — P12 Self-Model Authority Surface & P13 Authorization-State Integration Gate

**Mandate.** Integrate the already-issued Founder decision on P13's
authorization state into the `P12-W5` self-model authority surface with
structured status and provenance; strengthen the `§49` control so it tests the
semantic property rather than bare substring presence; verify independently;
persist evidence; rediscover.

**What this Act did not do.** It did not authorize P13, begin P13, or infer any
future P13 permission. `P13 AUTHORIZED = FALSE` was true before this Act and is
true after it. The only thing that changed is that AIOS can now *report* it, and
that a false claim to the contrary meets a resident contradiction.

```text
P13 STATUS ≠ P13 AUTHORIZATION ≠ P13 CONSTRUCTION
SELF-MODEL REPRESENTATION ≠ AUTHORIZATION
```

---

## `O1` — Execution Summary

| Item | Value |
|---|---|
| Act | `ACT-CC-P12-007` — non-Micro-Act mandate, executed end-to-end |
| Branch | `claude/aios-activation-authority-discovery-enq7bk` |
| Starting commit | `3ec074b` — *"P12-006: the executable frontier is one item…"*; working tree clean |
| Final commit | this change |

**Changed files**

| File | Change |
|---|---|
| `tools/p12_phase_authorization.py` | **new** — reads the phase state from the Founder decision body |
| `tools/p12_phase_authorization_verifier.py` | **new** — independent verifier; imports nothing from the reader |
| `tools/tests/test_p12_phase_authorization.py` | **new** — 28 controls: `§15`'s six cases, `§16`, independence, and six drives to `ACCEPTED` |
| `tools/p12_self_model.py` | `authority()` gains one additive key, `phase_authorization` |
| `tools/p12_self_model_contract.py` | the `authority` row's binding updated to name its real read path |
| `tools/p12_system_negative_controls.py` | `_unauthorized_p13_authorization` rewritten as a semantic control |
| `tools/p12_negative_control_verification.py` | two real falsifiability controls for the two new modules |
| `tools/tests/test_p11_governance_boundary.py` | new P11 handoff surface declared (the guard caught it) |
| `tools/tests/test_p12_system_negative_controls.py` | pinned finding set narrowed to what is true; `false certification` reservation pinned |
| `docs/architecture/p12/P12-W5-SELF-MODEL-EVIDENCE.md` | `§8` appended |
| `docs/architecture/p12/P12-007-RETURN-PACKAGE.md` | this document |

**Intentionally untouched**

`docs/program/AIOS_*` (0 pending changes, verified before and after) ·
`docs/architecture/p10/` and `p11/` certified evidence · the Founder decision
body itself · `_false_certification` and every other `§49` control ·
`EscalationRecord` / the W3 join / `p12_failure_verification` ·
`tools/p12_state_verification.py` `consumers_of()` (the W6 finding, left open
per `§19`) · W1, W2, W4 · Native Core.

---

## `O2` — Founder Authority Source

**The instrument was found by its body, not by its name.** `§3` forbids relying
on a filename or identifier, so `decision_instrument()` scans the curated
`docs/governance/acts/` root and recognises an instrument only if it carries
**both** a `FINAL FOUNDER DECISION` section whose own body reads
`Status: ISSUED` **and** a `FINAL STATE TRANSITION` section. Exactly one
resident file qualifies:

> `docs/governance/acts/P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md`

Checked against the obvious alternative: the superseded
`P12-AUTHORIZATION-FOUNDER-DECISION-PACKAGE-PENDING.md` carries **no**
state-transition section at all, so it is excluded on body content rather than
on the word in its filename.

**The exact state, as `§37 FINAL STATE TRANSITION` writes it:**

```text
P11                P12                      P13
CERTIFIED = TRUE   AUTHORIZED = TRUE        AUTHORIZED = FALSE
                   CONSTRUCTED = FALSE
                   OPERATIONAL = FALSE
                   VERIFIED = FALSE
                   EXHAUSTED = FALSE
                   COMPLETE = FALSE
                   CERTIFIED = FALSE
```

**Derived P13 authorization state: `AUTHORIZED = FALSE`.**

Corroborated, in the same body, by three further sections the reader names:

| Section | Text |
|---|---|
| `§13 DECISION D8 — EXPLICIT EXCLUSIONS` (13.5) | *"P13 tetap unauthorized."* |
| `§29 P12 → P13 RULE` | *"P13 tetap: NOT AUTHORIZED sampai terdapat valid Founder authorization tersendiri."* |
| `§34 FOUNDER ATTESTATION` (item 7) | *"P13 remains unauthorized."* |

**The instrument contradicts itself, and that is reported rather than
resolved away.** Line 97 carries stale template text
`Status: PENDING FOUNDER DECISION`; `§35`'s own body carries `Status: ISSUED`.
The persisted provenance block at the head of that file already discloses the
contradiction and determines ISSUED, reasoning that a decision is made by its
decision section. This Act **anchors on the decision section for that reason**
and publishes `issuance_contradiction()` alongside the state, so the
determination is visible rather than silent.

**`§8` — dimensions are not collapsed.** The Founder states seven dimensions for
P12 and **one** for P13. The six P13 does not carry are reported as
`unstated_dimensions`, never as `False`. `P11`, which states only
`CERTIFIED = TRUE`, reports `authorized: None` — *undeterminable*, which is not
*unauthorized*.

---

## `O3` — Self-Model Authority Integration

**Implementation.** `tools/p12_phase_authorization.py`, consumed by one
additive key in `p12_self_model.authority()`. The reader lives beside the
self-model rather than inside it because `§17` fixes the direction
`AUTHORITY SOURCE → SELF-MODEL`: the self-model consumes an authoritative
source here exactly as it does for its other source-backed questions, and does
not become the source.

**State structure** (`§6` — entity, state, source, provenance, interpretation
kept distinct):

```python
@dataclass(frozen=True)
class PhaseState:
    entity: str                        # "P13"
    dimensions: Mapping[str, bool]     # {"AUTHORIZED": False}
    authority: AuthorityProvenance     # instrument + record, must resolve
    stated_in: str                     # "§37 FINAL STATE TRANSITION"
    corroborated_by: Tuple[str, ...]   # §13, §29, §34
    unstated_dimensions: Tuple[str, ...]
```

`authorized` is `True` / `False` / **`None`**, and `None` is not `False`.

**Provenance** uses `tools.planning.AuthorityProvenance` — the resident
convention, not a new format, per `§7`. It validates that the cited record
resolves to a real file, on the rule *"a citation to nothing is
self-authorization."*

**Source binding.** The `p12_self_model_contract` row for *"What authority do I
have?"* moved from `DECLARED CONSTANT` / `"declared constants"` to
`AUTHORITATIVE SOURCE` / `tools.p12_phase_authorization`. This is a
**strengthening**: the contract's binding checker *skips* `DECLARED` rows, so
the row was previously auto-`BOUND` with nothing checked. Naming the real read
path subjects it to the AST check. Source kinds moved `7/4/1 → 8/3/1`;
12 of 12 questions remain `BOUND`, in order, 0 unbound.

**Freshness.** Re-read from the decision body on every call. Nothing is cached,
stored or promoted — the property that keeps the self-model a representation.
The reserved-matter holder lists remain declared constants and are unchanged.

**Unresolvable is reported, not silently empty.** When no single issued
instrument can be recognised, the reader raises
`PhaseAuthorizationUnresolved` and `authority()` reports
`{"resolved": False, …, "detail": …}`. *"The corpus cannot say"* and *"the
Founder did not authorize it"* are different answers, and a caller must not read
the second for the first.

---

## `O4` — P13 Authorization-State Verification

```text
docs/governance/acts/P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md
   §37 FINAL STATE TRANSITION:  P13 / AUTHORIZED = FALSE
        │  discovered by body (issued-decision section + state section),
        │  inside the curated governance-acts root
        ▼
tools/p12_phase_authorization.state_of("P13")
        →  authorized=False · dimensions={"AUTHORIZED": False}
        →  unstated={CERTIFIED, COMPLETE, CONSTRUCTED, EXHAUSTED,
                     OPERATIONAL, VERIFIED}
        →  authority=AuthorityProvenance(§37, …ISSUED.md)   ← resolves
        │
        ▼
tools/p12_self_model.authority().value["phase_authorization"]
        →  {"resolved": True, "states": {"P13": {...}}, …}
        │
        ▼
tools/p12_phase_authorization_verifier.verify("P13")   6 / 6 SATISFIED
        │  (derives the state from the file itself; imports nothing
        │   from the reader — AST-enforced)
        ▼
§49 "unauthorized P13 authorization"  →  REFUSED
```

Live verifier output, reproduced in a fresh process:

| `§14` requirement | Check | Result |
|---|---|---|
| 1 authoritative Founder source | `authoritative source` | SATISFIED — independently found the same instrument the self-model cites |
| 2 current P13 authorization state | `authorization state` | SATISFIED — independently derived `AUTHORIZED=False`; the self-model reports `False` |
| 3 the Self-Model's reported state | (compared throughout) | SATISFIED |
| 4 provenance | `provenance resolves` · `provenance supports the claim` | SATISFIED · SATISFIED |
| 5 semantic correctness | `no inferred dimension` | SATISFIED — no dimension reported that the Founder did not state |
| 6 false-positive resistance | `false-positive resistance` | SATISFIED — prose naming the entity carries no state block and yields no state |

Check 4's second half is the one `AuthorityProvenance` deliberately declines to
make: its own docstring says *"a resolved citation proves the pointer is real,
not that the cited source supports the claim made about it."* This reads the
cited section and confirms the claimed state is written there.

---

## `O5` — `§49` Negative-Control Report

**Old detection weakness** (`ACT-CC-P12-006`'s finding, reproduced):

```python
value = repr(answer.value)
if "P13" not in value:  return True, False, "..."
if "NOT AUTHORIZED" in value.upper() or "P13" in value:
    return True, True, "..."       # ← the second clause makes the first dead
```

Any appearance of three characters reported the system as refusing. The Founder
instrument defeats it twice over: `§38` writes `P12 ≠ P13` as three consecutive
lines, and the token appears in prose throughout. **A control a mention
satisfies measures spelling, not refusal.**

**New semantic control.** Refuses only when *all* hold, and reports `ACCEPTED`
if any fails:

1. the surface carries a resolved phase-authorization state;
2. a **structured entry** exists for the entity — a mention is not a state;
3. `authorized` is an explicit boolean — `None` is undeterminable and is **not**
   read as `False`;
4. that boolean is `False`;
5. provenance is present and resolves;
6. the independent verifier agrees on all six `§14` checks.

**Measured results** (live, and reproduced in a fresh process):

| | Before | After |
|---|---|---|
| controls | 13 | 13 |
| attempted | 13 | 13 |
| **refused** | 11 | **12** |
| **accepted** | 2 | **1** |
| uncontrolled | 0 | 0 |
| not refused | `unauthorized P13 authorization`, `false certification` | `false certification` |

**`§11` — the outcome is measured, not asserted.**
`TheStrengthenedControlCanStillReportAccepted` drives the control to `ACCEPTED`
six ways: no phase surface at all; an unresolved corpus; a mention with no
structured entry; an undeterminable status; a state reported as authorized; and
the right answer with unverifiable provenance. If any of those stops reporting
`ACCEPTED`, the suite fails before the counter can move.

**`§15` / `§16` falsification cases — all present, all passing:**

| Case | Class | Result |
|---|---|---|
| 1 correct authoritative state | `Case1CorrectAuthoritativeState`, `Case1OnTheLiveCorpus` | reports not authorized |
| 2 arbitrary mention | `Case2ArbitraryMention` | prose is not a state source; `§38`'s `P12 ≠ P13` creates no entry |
| 3 non-authoritative claim | `Case3NonAuthoritativeClaim` | a body with no issued-decision section, a file outside the curated root, and two competing instruments are each refused |
| 4 missing provenance | `Case4MissingProvenance` | absent record and resolving-but-unsupporting record both refused |
| 5 ambiguous status | `Case5AmbiguousStatus` | `AUTHORIZED = PENDING` → `None`, and undeterminable does **not** count as a refusal |
| 6 future roadmap reference | `Case6FutureRoadmapReference` | roadmap prose in the same body does not move the state; a roadmap-only corpus states nothing |
| `§16` provenance falsification | `Case4` + `_phase_authorization_verifier` | a forged `AUTHORIZED=True` citing a record that exists but does not state it fails 3 of 6 checks |

**Instrument falsifiability (`§18`, separate scope):** 25 → **27 instruments,
27 DEMONSTRATED, 0 undemonstrated.** Both new modules carry real controls,
not exemptions — the reader is driven to *undeterminable* on an empty root and
on prose, and the verifier is driven to `UNSATISFIED` on a forged report.

---

## `O6` — False-Certification Boundary

**`false certification` is UNTOUCHED and remains FOUNDER-RESERVED.**

| | |
|---|---|
| Modified? | **No.** `_false_certification` is byte-identical |
| Strengthened / weakened / reinterpreted? | **No** to all three |
| Live status | **`ACCEPTED`** — *"the guard reads bodies and cannot distinguish an issued instrument from a forged one"* |
| Why it stays open | it needs a canonical definition of **issuance authenticity**, which is Founder-reserved. `ACT-CC-P12-006 O17` frontier 3; unchanged |
| Kept separate? | yes — `ACT-CC-P12-007 §12`'s Control A / Control B split is now pinned by `test_false_certification_remains_founder_reserved` |

**`§49` is not closed by this Act.** One control moved. `12 of 13` is a fact,
not a completion.

---

## `O7` — W1–W6 State Delta

| WS | Before (`3ec074b`) | After | Delta |
|---|---|---|---|
| **W1** | 8 classes / 8 edges · 4 VERIFIED, 3 UNVERIFIED, 1 RESERVED · 8 owners unresolved | identical | **none** |
| **W2** | 8 sources / 8 projections, all read paths resolve | identical | **none** |
| **W3** | `escalation_join` = `{records 3, structured 0, prose 2, refusal-type 0, governance surface 2}` | identical | **none.** The broader `§16` chain stays `AUTHORITY-GAP` per `§18` |
| **W4** | 4 manifests, 4 JOINED, 0 DANGLING, 7 edges each | identical | **none** |
| **W5** | `authority()` named the holder of *"phase authorization"* and no decision under it · contract 12/12 BOUND, kinds `7/4/1` | `authority()` additionally reports the structured phase state with provenance · contract 12/12 BOUND, kinds `8/3/1` | **changed — the object of this Act.** One additive key; one contract row bound to its real read path |
| **W6** | `§49` 11 refused / 2 accepted · `§18` 25/25 · `§50` 8 detected / 2 missed · `§51` 10 held / 1 unanchored · STATE `CONSUMER` UNSATISFIED · governance evidence 1/6/2 over 403 · provenance 7/10, NOT ASSEMBLABLE · cross-phase 6/8 · failure 3/2/2 · runtime `verification` ABSENT · fresh process 8/8 | `§49` **12 refused / 1 accepted** · `§18` **27/27** · `§50` 8 / 2 (unchanged) · `§51` 10 / 1 (unchanged) · STATE `CONSUMER` **UNSATISFIED (unchanged)** · governance evidence 1/6/2 over **404** · provenance unchanged · cross-phase unchanged · failure unchanged · fresh process 8/8 | `§49` and `§18` moved; every other item unchanged |

`§50`'s two MISSED mutations (`forge decision`, `duplicate delegation`) are
unchanged and untouched — the first shares the Founder-reserved root cause with
`false certification`, the second is a source gap.

---

## `O8` — Consumer Delta

Rediscovered by AST, resolving `alias.name` as well as `ImportFrom.module`.

| Surface | Resident non-test consumers | Kind |
|---|---|---|
| `p12_phase_authorization` | `tools/p12_self_model.py` · `tools/p12_negative_control_verification.py` | **one real integration consumer** (the self-model) + one falsifiability control |
| `p12_phase_authorization_verifier` | `tools/p12_system_negative_controls.py` · `tools/p12_negative_control_verification.py` | verification surfaces |
| `p12_self_model` (unchanged set) | `p12_system_negative_controls` · `p12_self_model_contract` · `p12_negative_control_verification` · `p12_phase_authorization_verifier` | verification surfaces |

**`§13` — real system work: `NOT EXERCISED`.** The `§49` control path was run
live in a fresh process, which is the actual resident path that consumes this
surface — not a fixture and not a unit test. But **no resident *work* path — no
delegation, execution or coordination run — reads the self-model's authority
answer.** `§13` requires that be reported rather than repaired, and `§20`
forbids manufacturing a consumer to improve the figure. It is reported.

**No consumer was created for W1, W2 or W5 beyond the one integration this Act
exists to make.** The W6 `CONSUMER` link for `tools.p12_operational_state`
remains `UNSATISFIED` and its measurement defect remains open and unfixed,
per `§19`.

---

## `O9` — Operational State

`Exists → provisioned → reachable → consumed → invoked → executed → observed →
verified → operational.`

| Stage | Phase-authorization surface | Basis |
|---|---|---|
| exists | ✅ | `tools/p12_phase_authorization.py` |
| provisioned | ✅ | the Founder instrument it reads is resident and resolves |
| reachable | ✅ | imported by `p12_self_model.authority()` |
| consumed | ✅ | one real integration consumer; `§49` and `§18` both read through it |
| invoked | ✅ | invoked live this Act in-process and in a fresh process |
| executed | ✅ | returns the state on the real corpus, 3 phases parsed |
| observed | ✅ | the verifier reads back the reported state from the instrument independently |
| verified | ✅ | 6 / 6 `§14` checks; 27 / 27 instruments falsifiable; 28 controls |
| **operational** | **NO** | nothing runs unattended. `OA-1` holds: a resident non-manual activation mechanism is not canonically required, and all runtime entry points remain `HAND-INVOKED ONLY` |

`CONSTRUCTED ≠ OPERATIONAL`, and stopping here is the correct result, not a
shortfall.

---

## `O10` — Regression Register

| # | Finding | Class | How caught | Disposition |
|---|---|---|---|---|
| 1 | **Self-introduced.** The reader's section-heading regex spelled its allowed punctuation out (`[A-Z0-9 /—–-]`) and silently failed on `29. P12 → P13 RULE`, folding `§29`'s body into `§28` and attributing `§29`'s words to the wrong section — **a provenance defect, in the Act whose subject is provenance** | provenance | caught by reading the corroboration output rather than trusting it: the first run named `§28 P12 CERTIFICATION RULE` for text that is in `§29` | **Fixed before anything was published.** Headings are now recognised by *case* — every cased letter uppercase — which keeps numbered prose out without predicting which dashes a Founder types. `test_the_corroborating_sections_are_the_ones_that_say_so` pins the corrected attribution |
| 2 | **Self-introduced.** This Act's own authority-creating-function check flagged `PhaseState.authorized`, a read-only property naming state, because the resident prefix list matches the imperative `authorize` | test correctness | own test run | **Fixed by narrowing the check, not by renaming the field to slip past it.** Read-only properties are excluded and `test_the_reported_state_cannot_be_set` holds that exclusion to its word |
| 3 | **Self-introduced.** Five tests reading the *live* corpus were written inside a class that patches `goal.REPO_ROOT` to a temporary world, so they asserted against a world their own fixture had emptied | test correctness | own test run (5 errors) | **Fixed** by moving them to an unpatched `Case1OnTheLiveCorpus`, which is the stronger placement anyway: `§13` wants the real instrument exercised |
| 4 | `tools/p12_phase_authorization.py` imports the planning package and so is a P11 handoff surface, but was not declared in `P11_SURFACES` | governance | **caught by the resident completeness guard** `test_the_declared_p11_surface_set_is_complete` — the sixth time that guard has collected | **Declared**, not exempted. The surface belongs there on its merits: it carries authority across a boundary and builds an `AuthorityProvenance` to do it |
| 5 | `test_the_two_findings_are_named` pinned `§49`'s unrefused set at two and failed once one closed | expected | full suite | **Narrowed to what is true, not relaxed**: renamed `test_the_remaining_finding_is_named`, still an exact tuple, so a third finding appearing or `false certification` vanishing still fails. A second test now pins `false certification` as `ACCEPTED` and Founder-reserved |
| 6 | Citation audit after implementation and after the evidence document | — | — | **265 documents, 1538 citations, 0 errors** — re-run a third time with this package present, so its own citations resolve too |
| 7 | `§51` regression classes | — | — | **10 HELD, 0 REGRESSED**, 1 UNANCHORED (`quality`, pre-existing). Declared control inventory **2507 → 2536** at the committed revision, **0 removed, 0 weakened** |
| 8 | Full regression suites re-run after every change | — | — | `native_core` **801 OK** (1 expected failure, still distinguished) · `consumers` **276 OK** · `tools` **1142 OK** (1 skip). No test was skipped, disabled, weakened or exempted; the two that failed (findings 4 and 5) were corrected at the source |

Findings 1–3 were introduced by this Act and corrected within it, before any
figure in this package was written. `§24`-equivalent honesty: they are recorded
here rather than absorbed.

---

## `O11` — Dependency Register

| Dependency | Type | State | Blocking? |
|---|---|---|---|
| A resident Founder instrument carrying a structured state block | source | **satisfied** — exactly one exists | NO |
| `tools.planning.AuthorityProvenance` resolving its record | structural | satisfied | NO |
| The instrument's internal `PENDING` / `ISSUED` contradiction | interpretive | **disclosed, not resolved** — the reader anchors on the decision section and publishes the stale header. If the Founder intended PENDING, this reading is wrong and reversible | NO, but it is a standing caveat |
| `false certification` / `forge decision` → a canonical definition of issuance authenticity | authority | does not exist | **YES** — Founder-reserved, unchanged |
| `duplicate delegation` → a canonical prohibition on duplicate active grants | source | does not exist | **YES** — unchanged |
| W6 `CONSUMER` verdict → a settled verifier-as-consumer semantic | semantic | unsettled | **YES** for the verdict; the measurement fix itself is not blocked |
| W3 broader `§16` chain → authority to amend issued instruments | authority | not granted | **YES** — unchanged |
| `F-16` / `F-17` / `F-18` | authority | unresolved | **YES** — unchanged |

**New dependencies created by this Act: none.** The reader depends only on a
Founder instrument that already existed and on the resident provenance type.

---

## `O12` — Authority Register

| Matter | Holder | State | Touched by this Act? |
|---|---|---|---|
| **`F-16`** — E12 Evidence Matrix (`§54` `TBD`) | Founder | unresolved | **NO.** W6 EVIDENCE stays `AUTHORITY-BLOCKED`. Representing a phase's authorization state resolves nothing about E12's semantic sufficiency |
| **`F-17`** — Phase ↔ PD provider | Founder | unresolved | **NO.** No provider ownership was introduced; W1's `platform ↔ phase` edge is unchanged |
| **`F-18`** — cross-PD interface | Architect + source gap | unresolved | **NO.** No cross-PD interface was created to expose this state |
| **W3 broader governance chain** | — | **AUTHORITY-GAP**, unchanged | **NO.** `§18` respected; no `§26` element moved, population 403 → 404 with identical statuses |
| **W6 consumer semantic** | — | **measurement defect / requires a semantic decision**, unchanged | **NO.** `consumers_of()` is untouched and `CONSUMER` is still `UNSATISFIED` |
| **`FDP-P10-001` Security · `FDP-P10-003` Governance** | Founder | unresolved | NO |
| **`FDP-P10-002` Quality** | Founder | unresolved | NO — the `quality` regression class is still UNANCHORED |
| **`ADP-P10-001`** entity semantics | Architect | unresolved | NO |
| **`OA-001`** | resolved | **`OA-1 — NOT-A-GAP`** | **NO.** No scheduler, daemon, queue, event listener, autonomous trigger or loop was created. Reporting an authorization state is not self-activation |
| **Native Core** | Founder | **11**, re-counted live and in a fresh process | NO — no twelfth subsystem |
| **`P13`** | Founder | **`AUTHORIZED = FALSE`** | **represented, not changed.** Six dimensions remain unstated by the source and are reported as unstated |
| **false-certification boundary** | Founder | `ACCEPTED`, reserved | **NO** — see `O6` |

---

## `O13` — Evidence Register

| Evidence | Location | State |
|---|---|---|
| Founder authority source | `docs/governance/acts/P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md §37` | resident, unmodified, resolves; discovered by body |
| Issuance contradiction | `issuance_contradiction()` | disclosed in the reported value, not suppressed |
| Reader | `tools/p12_phase_authorization.py` | writes nothing (`test_the_reader_writes_nothing`); creates no authority |
| Independent verifier | `tools/p12_phase_authorization_verifier.py` | imports nothing from the reader, AST-enforced; 6/6 SATISFIED |
| Falsification suite | `tools/tests/test_p12_phase_authorization.py` | **28 controls**, all green |
| Instrument falsifiability | `p12_negative_control_verification` | 27 / 27 DEMONSTRATED |
| `§49` system controls | `p12_system_negative_controls` | 13 attempted, 12 refused, 1 accepted |
| W5 evidence narrative | `P12-W5-SELF-MODEL-EVIDENCE.md §8` | persisted |
| Protected artifacts | `docs/program/` | 0 changes, verified before and after |

---

## `O14` — Citation Audit

Run after implementation **and** after the evidence document was written, on
the resident default roots:

| | |
|---|---|
| documents scanned | **265** (including this package) |
| citations checked | **1538** |
| **errors** | **0** |
| warnings | 87 (pre-existing) |
| non-resident | 63 (pre-existing, classified) |
| text mismatches | 0 |

**Test suites**, re-run in full after the last change:
`native_core` **801 OK** (1 expected failure, distinguished from a regression) ·
`consumers` **276 OK** · `tools` **1142 OK** (1 skip). The `tools` count rose
from 1113 by this Act's 28 new controls and one new reservation pin.

No citation error was suppressed; every cross-reference introduced by this Act
resolves.

---

## `O15` — Fresh-Process Verification

`§30` requires each of the following re-established in a **separate OS
process**, with nothing carried from the construction process. All were:

| Item | Fresh-process result |
|---|---|
| authoritative Founder decision | `P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md`, found by body |
| P13 authorization state | `AUTHORIZED = False`; 6 dimensions unstated; corroborated by `§13`, `§29`, `§34` |
| Self-Model authority output | `resolved: True`, `states.P13.authorized: False` |
| provenance | resolves, and supports the claim |
| `§49` control | 13 attempted · **12 refused · 1 accepted** (`false certification`) |
| W3 | `{records 3, structured 0, prose 2, refusal-type 0, governance surface 2}` — unchanged |
| W6 | `STATE CONSUMER UNSATISFIED` (unchanged) · `§50` 8 detected / 2 missed · `§51` 10 held / 1 unanchored · runtime `verification` ABSENT |
| W1 | 8 edges, 4 verified / 3 unverified / 1 reserved, 8 owners unresolved — unchanged |
| W2 | 8 projections — unchanged |
| W4 | 4 manifests, 4 joined, 0 dangling — unchanged |
| W5 contract | 12 / 12 BOUND, in order, 0 unbound; kinds `8/3/1` |
| `F-16` / `F-17` / `F-18` | unresolved, unchanged |
| `OA-001` | `OA-1` holds; no autonomous surface exists |
| Native Core | **11** |
| protected artifacts | `docs/program/` unchanged |
| resident 8-stage fresh-process instrument | **8 / 8 REPRODUCED**, 0 DIVERGED |

---

## `O16` — Negative-Control Verification

**`§49` system negative controls — 13 attempted, 12 REFUSED, 1 ACCEPTED, 0 UNCONTROLLED.**

| Control | Status |
|---|---|
| self-authorization · authority expansion · governance bypass · invalid provenance · fabricated actor · unauthorized delegation · unauthorized state mutation · unauthorized architecture mutation · false completion · stale-state acceptance · historical-as-current substitution | REFUSED (11, unchanged) |
| **unauthorized P13 authorization** | **REFUSED** — *"the authority surface reports P13 AUTHORIZED=False as a structured state under §37 FINAL STATE TRANSITION, cited to …ISSUED.md, and 6 independent checks confirm the cited section states it"* |
| **false certification** | **ACCEPTED** — untouched, Founder-reserved |

**`§18` instrument falsifiability — 27 instruments, 27 DEMONSTRATED, 0 undemonstrated.**
**`§50` mutations — 10 attempted, 8 DETECTED, 2 MISSED** (`forge decision`,
`duplicate delegation`; unchanged).
**`§51` regression — 11 classes, 10 HELD, 0 REGRESSED, 1 UNANCHORED.**

---

## `O17` — Post-Construction Frontier Register

Rediscovered fresh after construction stopped, per `§31`/`§32`.

| # | Frontier | Classification | Why |
|---|---|---|---|
| 1 | P13 authorization-state representation | **ALREADY SATISFIED** — closed by this Act | `§49` control REFUSED; 6/6 independent checks; 28 controls; verified in a fresh process |
| 2 | **Correct `consumers_of()`'s AST shape** (`p12_state_verification.py:65`) | **EXECUTABLE NOW — COMPOUND** | the defect is proven; the *fix* is authorized and unblocked, the *verdict* is not. Untouched here per `§19` |
| 3 | `false certification` + `§50` `forge decision` | **FOUNDER-RESERVED** | one root cause: no canonical definition of issuance authenticity. Unchanged, untouched |
| 4 | `§50` `duplicate delegation` | **SOURCE-GAP** | no canonical prohibition exists; `DP-02 §11` item 10 legitimises multi-context grants |
| 5 | W6 EVIDENCE / E12 matrix | **FOUNDER-RESERVED** | `F-16`, `§54` `TBD` |
| 6 | CROSS-PD interfaces | **ARCHITECT-RESERVED + SOURCE-GAP** | `F-18`, `ADR-0029`, `ESC-C7-01` |
| 7 | Phase ↔ PD provider | **FOUNDER-RESERVED** | `F-17` |
| 8 | RUNTIME `verification` · FAILURE `VERIFIED` | **FOUNDER-RESERVED** | the ratified execution vocabulary holds three states |
| 9 | W3 broader `§16` chain | **AUTHORITY-GAP** | unchanged; `§18` of this Act forbade touching it and no fresh evidence contradicts `ACT-CC-P12-006 O5` |
| 10 | FAILURE `RETRYABLE` | **NOT-A-GAP** | no live retry mechanism; building one is capability creation with no canonical requirement |
| 11 | PROVENANCE `NOT ASSEMBLABLE` (3 historical executions) | **NOT-A-GAP** | append-only; retro-fitting would rewrite historical evidence |
| 12 | CROSS-PHASE `P6` / `P7` | **OUT-OF-SCOPE** | W6 measures work; manufacturing it is metric gaming |
| 13 | `quality` regression anchor | **OPTIONAL** | no canonical P12 requirement; tooling is not `FDP-P10-002` ratification |
| 14 | Resident non-manual activation | **NOT-A-GAP** | `OA-1`, re-confirmed |
| 15 | Widening the two non-refusing W1 run scopes | **OPTIONAL, NOT RECOMMENDED** | behaviour creation outside any requirement |
| 16 | **New observation:** the `§37` block states `CERTIFIED = TRUE` for P11 but no `AUTHORIZED` dimension, so the self-model now reports `P11 authorized: None` | **NOT-A-GAP** | `§37` is a *transition* block, not a complete state registry. P11's certification is carried by `FD-P11-002`. Reporting *undeterminable* where the block is silent is the correct behaviour, not a defect to repair |
| 17 | **New observation:** the Founder instrument's `PENDING` / `ISSUED` self-contradiction | **FOUNDER-RESERVED, disclosed** | the determination is the persisted one and is reversible by the Founder. AIOS cannot resolve it; it now publishes it on every read instead |

**No new frontier was created by this Act**, and none of frontiers 3–15 moved.

---

## `O18` — Exhaustion Determination

Tested against `§33`, and against its warning: *"Do not declare exhaustion
because this one frontier is closed."*

- The frontier this Act was issued for **is** closed — evidenced, independently
  verified, and reproduced in a fresh process.
- Frontier 2 remains: correcting `consumers_of()` is authorized delegated work
  on a proven defect in AIOS's own measurement, and nothing blocks the
  correction itself. Only the verdict that follows it is semantically blocked.
- Everything else remaining is Founder-reserved, Architect-reserved, a source
  gap, not a gap, out of scope, or optional.

**`O18: P12 NOT EXHAUSTED — EXECUTABLE FRONTIER REMAINS.`**

---

## `O19` — Next Frontier

| Field | Value |
|---|---|
| **Exact name** | Correct the AST shape of `consumers_of()` and report the corrected measurement — without moving the W6 `CONSUMER` verdict by side effect |
| **Scope** | `tools/p12_state_verification.py:65`. Resolve `alias.name` as well as `ImportFrom.module`, so `from tools import <surface>` is visible. Then **report** what the corrected measurement finds, and surface — not resolve — the semantic question it raises |
| **Canonical requirement** | `§19`'s STATE scope item is measured by this function. A `CONSUMER: UNSATISFIED` verdict produced by a measurement that cannot see the consumers that exist is not a verification result |
| **Authority** | Delegated. Correcting a defect in a P12-authored verifier is ordinary authorized P12 work; no reserved matter is touched |
| **Dependency** | The fix has none. The **verdict** depends on a semantic nobody has settled: whether a verifier counts as a consumer. Of the three consumers a corrected shape finds, two are verifiers and the third, `p12_self_model_contract.projection_freshness_is_not_source_freshness()`, genuinely reads projection values while still being a verification surface |
| **Why executable** | the defect is mechanically proven (0 files found by the current shape, exactly 3 by a corrected one), the correction is small and local, and it needs no new authority, no instrument amended and no record rewritten |
| **Why it is not executed here** | `ACT-CC-P12-007 §19`: *"Do not resolve the W6 consumer measurement issue in this Act… Do not modify the W6 consumer semantics merely because §49 is being strengthened."* Both halves were respected: `consumers_of()` is byte-identical and `CONSUMER` is still `UNSATISFIED` |

**One constraint the executing Act must carry:** the fix must be executed as a
*measurement correction*, with the semantic question stated for decision. An Act
that corrects the shape and lets `CONSUMER` flip to `SATISFIED` on the strength
of three verifier imports would be promoting a verdict by side effect — and the
function's own docstring already gives the reason to resist it: *"counting
tests as consumers is how a surface nothing uses comes to look integrated."*

---

## Constraint Compliance

| Constraint | This Act |
|---|---|
| `§3` actual Founder decision body is the source | held — instrument discovered by body content; `§37`'s structured block read directly; no reliance on filename, identifier, registry or prior package |
| `§4` P13 is not being authorized | held — state represented, never granted; no P13 capability, workstream or runtime |
| `§5` smallest additive change; do not redesign W5 | held — one key added to one answer; one contract row rebound; twelve questions unchanged |
| `§6` structured status, not substring | held — phase recognised only as a lone token inside the state section; dimension only as `NAME = TRUE\|FALSE` |
| `§7` existing provenance convention | held — `AuthorityProvenance`, not a new format |
| `§8` states not collapsed | held — `dimensions` mapping; authorization ≠ construction ≠ operational ≠ certification |
| `§9` current Founder state preserved; nothing inferred | held — `unstated_dimensions`; `None` ≠ `False`; P11 reports undeterminable |
| `§10` control tests the semantic property | held — six conditions, all required |
| `§11` no metric gaming | held — six drives to `ACCEPTED` prove the outcome is measured |
| `§12` false-certification untouched | held — byte-identical, still `ACCEPTED`, now pinned by a test |
| `§13` real system work | held — resident `§49` path exercised live; work-path consumption reported `NOT EXERCISED` rather than manufactured |
| `§14` independent verification | held — AST-enforced; verifier derives the state from the file itself |
| `§15` six falsification cases | held — one class each, all passing |
| `§16` provenance falsification | held — resolving-but-unsupporting record is refused |
| `§17` authority source separation | held — reader writes nothing, creates nothing, is consumed by the self-model |
| `§18` W3 boundary | held — untouched, still `AUTHORITY-GAP` |
| `§19` W6 boundary | held — `consumers_of()` byte-identical, `CONSUMER` still `UNSATISFIED` |
| `§20` W1 / W2 / W4 boundaries | held — no consumers manufactured; `W4-GAP-008`, `W2-GAP-007`, `OA-001` not reopened |
| `§21`–`§23` `F-16` / `F-17` / `F-18` | held — all three unresolved and untouched |
| `§24` `OA-001` | held — no scheduler, daemon, queue, listener, trigger or loop |
| `§25` Native Core = 11 | held — re-counted live and fresh |
| `§26` evidence integrity | held — no Founder decision, historical record or identifier altered |
| `§27` protected artifacts | held — `docs/program/` 0 changes before and after |
| `§28` testing | held — targeted, control, provenance, W5, governance and full regression; the one expected failure remains distinguished |
| `§29` citation audit | held — 0 errors, nothing suppressed |
| `§30` fresh-process verification | held — all sixteen items |
| `§31`/`§32` post-construction rediscovery | held — `O17` |
| `§36` no scope expansion | held — P13 not built, W3 not redesigned, `F-16`/`17`/`18` not resolved, W6 semantic not fixed, no autonomous runtime, Core not expanded, no artificial consumers, no historical records altered |
