# `ACT-CC-P12-006` — P12 Frontier Reconciliation & Executable Surface Discovery Gate

**Mandate.** Discovery only. `ACT-CC-P12-006 §3`: *"Do not execute the next
frontier even if it is authorized. Record it."* Nothing was constructed,
wired, repaired or relabelled in this Act. Two live defects found here are
**recorded, not fixed**, for that reason, and both are disclosed in `O10`.

**Method.** Every figure below was re-derived by running the resident
instrument on the live corpus during this Act. Nothing is carried forward
from `P12-003`, `P12-004` or `P12-005` on the strength of those packages
having said it — where a prior package's claim is repeated it is because
the measurement was re-run and agreed, and where it disagreed that is
reported as a delta. `§8`: *"Do not rely on the previous Return Package as
current truth."*

---

## `O1` — Fresh Repository State

| Item | Value |
|---|---|
| Branch | `claude/aios-activation-authority-discovery-enq7bk` |
| Commit at discovery | `0f39339` — *"P12-005: wire the escalation-grant join into the three resident call sites"* |
| Working tree | clean — `git status --short` empty before any file in this Act was written |
| Files changed by this Act | this document only |
| `docs/program/AIOS_*` | **UNTOUCHED.** Last commit touching `docs/program/` is `e7a3d73`, which predates the entire `P12-00x` series; `git status --short docs/program/` returns 0 entries |
| Certified P10 evidence (`docs/architecture/p10/`) | untouched; `p12_certified_evidence_guard` re-demonstrated live (`O16`) |
| Certified P11 evidence (`docs/architecture/p11/`) | untouched; guard re-demonstrated live, refusing a write under it |
| Native Core | **11 boundaries**, re-counted live: `agent, capability, governance, infrastructure, knowledge, memory, optimization, runtime, skill, trace, workflow` |

---

## `O2` — W6 Complete Scope Inventory

All thirteen `§19` minimum-scope items, each re-measured this Act.

| # | `§19` item | Instrument | Live state |
|---|---|---|---|
| 1 | CROSS-PHASE | `p12_cross_phase_verification` | 8 canonical phases · **6 EXERCISED**, 2 NOT EXERCISED (`P6` Knowledge — `knowledge_consumed` empty in every Trace record; `P7` Memory — `memory_consumed` empty in every Trace record) |
| 2 | CROSS-PD | `p12_cross_pd_verification` | 6 checks · **6 CURRENT**, 0 stale · 5 evidenced edges of 90 ordered pairs (5.6%) · **0 edges carry a defined interface** |
| 3 | RUNTIME | `p12_runtime_verification` | 9 items · 8 DISCOVERED, **1 ABSENT** (`verification` — the ratified execution vocabulary is `['escalation','failure','success']`) · 10 root entry points, all `HAND-INVOKED ONLY` |
| 4 | WORKFLOW | `p12_workflow_verification` | 5 joins · 4 EVIDENCED, **1 BY CONVENTION** (`WORK → EXECUTION`: 7/10 executions name their work; 3 share only an actor name) · chain not fully connected |
| 5 | GOVERNANCE EVIDENCE | `p12_governance_evidence_verification` | 9 `§26` elements over a 403-instrument population · **1 ESTABLISHED** (`provenance`, structural) · 6 PARTIAL · **2 ABSENT** (`affected surfaces`, `verification`) |
| 6 | STATE | `p12_state_verification` | 4 links · 3 SATISFIED (`STATE`, `AUTHORITATIVE SOURCE`, `PROJECTION`) · **`CONSUMER` UNSATISFIED** — *the verdict is produced by a defective measurement; see `O8` and `O10`* |
| 7 | EVIDENCE | E12 Evidence Matrix | **AUTHORITY-BLOCKED** — `F-16`: `§54` of the Founder authorization leaves the E12 matrix `TBD`; no resident source defines the criteria to measure against |
| 8 | PROVENANCE | `p12_provenance_verification` | 11/11 elements carried, 0 absent · 10 executions, **7 joined** (evidence 3/3, Trace 4/7) · `assembly: NOT ASSEMBLABLE` |
| 9 | FAILURE | `p12_failure_verification` | 7 states · 3 DISTINGUISHED (`FAILED`, `ESCALATED`, `SUCCEEDED`) · 2 RAISED ONLY (`BLOCKED`, `REFUSED`) · 2 UNREACHABLE (`RETRYABLE`, `VERIFIED`) |
| 10 | SYSTEM NEGATIVE CONTROLS (`§49`) | `p12_system_negative_controls` | 13 controls · **13 attempted** · 11 REFUSED · **2 ACCEPTED** (`unauthorized P13 authorization`, `false certification`) · 0 UNCONTROLLED |
| 11 | MUTATION (`§50`) | `p12_mutation_verification` | 10 mutations · 10 attempted · 8 DETECTED · **2 MISSED** (`forge decision`, `duplicate delegation`) |
| 12 | REGRESSION (`§51`) | `p12_regression_verification` | 11 classes · 10 HELD · 0 REGRESSED · **1 UNANCHORED** (`quality` — no resident linter, formatter, coverage threshold or CI configuration) |
| 13 | FRESH PROCESS | `p12_fresh_process_verification` | 8 stages · **8/8 REPRODUCED**, 0 DIVERGED |

**Instrument falsifiability** (`§18`, a separate scope from `§49`):
`p12_negative_control_verification` — **25 instruments, 25 DEMONSTRATED,
0 undemonstrated**.

---

## `O3` — W6 Executability Matrix

Every W6 item that is not already closed, classified against `§29`. The
governing question is not *"could AIOS do this?"* but *"is AIOS authorized
to do this, and is anything blocking it?"* — `§6`: `NECESSITY ≠ AUTHORITY`.

| Remaining item | Classification | Authority | Dependency | Evidence |
|---|---|---|---|---|
| `§49` `unauthorized P13 authorization` ACCEPTED | **EXECUTABLE NOW** | delegated — reporting an already-issued Founder fact is integration, not authorization (`§16`; self-model discipline is *reported, never exercised*) | none | `_unauthorized_p13_authorization()` reads `p12_self_model.authority()` and finds no P13 status; `P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md §29` (*"P13 tetap unauthorized"*) and `§37.7` (*"P13 remains unauthorized"*) already state it |
| `§49` `false certification` ACCEPTED | **AUTHORITY-GAP** | Founder-reserved | needs a canonical definition of *issuance authenticity* — what makes a certification statement issued rather than planted | live detail: *"the guard reads bodies and cannot distinguish an issued instrument from a forged one"*; no resident source defines the distinction. Manufacturing one would be self-authorization |
| `§50` `forge decision` MISSED | **AUTHORITY-GAP** | Founder-reserved | same issuance-authenticity definition as above (one root cause, two symptoms) | same live detail; the two findings are not independently closable |
| `§50` `duplicate delegation` MISSED | **SOURCE-GAP** | — | needs a canonical prohibition that does not exist | `FD-P11-001 §6` and `DP-02 §6` were both read at body level this Act: **neither carries a rule against two ACTIVE grants of one capability to one recipient.** `DP-02 §11` item 10 positively legitimises multi-context grants. A detector would be enforcing a rule AIOS invented — `§6`, forbidden |
| CROSS-PD: 0 edges carry a defined interface | **SOURCE-GAP + ARCHITECT-RESERVED** | Architect (`ADR-0029`) | cross-PD interface definition (`F-18`) | `ESC-C7-01` open; no resident source defines the interface shape. Unchanged this Act |
| RUNTIME: `verification` ABSENT | **FOUNDER-RESERVED** | Founder — the execution vocabulary is ratified | ratifying a `verified` execution state | the vocabulary `['escalation','failure','success']` is ratified; adding a fourth state is constitutional-vocabulary change, not integration |
| FAILURE: `VERIFIED` UNREACHABLE | **FOUNDER-RESERVED** | same as above | same | the same ratified vocabulary; *a successful run is not a verified one* |
| FAILURE: `RETRYABLE` UNREACHABLE | **NOT-A-GAP** | — | — | no live retry mechanism exists; the only one in the repository is under `docs/architecture/history` and is not reachable. Building one would be capability creation with no canonical requirement |
| FAILURE / `BLOCKED` + `REFUSED` RAISED ONLY | **ALREADY SATISFIED to the limit of the frozen record** | — | modifying `EscalationRecord` would be needed to go further — refused by design | `P12-005` closed the joinable part beside the record; `escalation_join()` now reports `governance_surface: 2`. The record itself is a certified P11 shape and stays unmodified |
| GOVERNANCE EVIDENCE: `affected surfaces`, `verification` ABSENT; 6 PARTIAL | **AUTHORITY-GAP (majority) / OPTIONAL (remainder)** | — | see `O5` | the population is 403 resident governance instruments; the overwhelming majority are Founder-issued, certified, or historical. See `O4`/`O5` |
| STATE: `CONSUMER` UNSATISFIED | **CONTRADICTION** | — | an unsettled semantic question (see `O8`) | the verdict is produced by a measurement this Act proved defective. Whether the corrected verdict is SATISFIED depends on whether a verifier counts as a consumer — which no canonical source settles |
| PROVENANCE: `NOT ASSEMBLABLE` (3 of 10) | **NOT-A-GAP for the historical records** | — | — | the 3 unjoined executions are historical Trace records that name only an actor. Records are append-only; retro-fitting a delegation id would be rewriting historical evidence — `§17`, forbidden. New executions already carry manifests (4/4 joined, 0 dangling) |
| CROSS-PHASE: `P6`/`P7` NOT EXERCISED | **OUT-OF-SCOPE for W6** | — | real Knowledge/Memory consumption by real work | W6 measures; it does not manufacture the work it measures. Writing a Trace record with a populated `knowledge_consumed` purely to move this number is metric gaming — `§7`, forbidden |
| REGRESSION: `quality` UNANCHORED | **OPTIONAL** | delegated (tooling is not governance) | none | no linter/CI exists. Adding one is legitimate engineering but is not a canonical P12 requirement and would not close any `§19` item |

**Count.** Of fourteen remaining W6 lines, exactly **one is `EXECUTABLE NOW`**.

---

## `O4` — W3 Broader Governance Chain Inventory

`P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md §16` requires governance
integration to preserve:

`DECISION → AUTHORITY → RATIONALE → IMPLEMENTATION → VERIFICATION → CURRENT STATE`

`P12-005 O16` recorded *"`W3`'s broader `§16` chain … EXECUTABLE, large,
needs scoping."* This Act performed that scoping, and the result **revises
that classification** — see `O5`.

The chain's resident measurement is `§26`'s nine elements over the 403
indexed governance instruments:

| `§26` element | Chain link | Status | Instruments carrying a label |
|---|---|---|---|
| `decision body` | DECISION | PARTIAL | 93 / 403 |
| `authority` | AUTHORITY | PARTIAL | 107 / 403 |
| `effective date` | AUTHORITY | PARTIAL | 33 / 403 |
| `scope` | IMPLEMENTATION | PARTIAL | 23 / 403 |
| `status` | CURRENT STATE | PARTIAL | 133 / 403 |
| `provenance` | (structural) | **ESTABLISHED** | 403 / 403 — every indexed instrument carries `source_path` + `source_hash` |
| `affected surfaces` | IMPLEMENTATION | **ABSENT** | 0 / 403 |
| `current state` | CURRENT STATE | PARTIAL | 52 / 403 |
| `verification` | VERIFICATION | **ABSENT** | 0 / 403 |

`RATIONALE` has no `§26` element of its own and is therefore not separately
measurable by this instrument — recorded as a measurement gap, not as a
satisfied link.

**The escalation link, closed in `P12-003`/`P12-005`, re-verified live this
Act:** `escalation_join()` reports `{records: 3, structured field: 0,
parsed prose: 2, naming the refusal type: 0, governance surface: 2}`. The
structural join resolves independently of prose for the two escalations it
covers. The third is a historical record predating the join.

---

## `O5` — W3 Authorization Matrix

The `§16` authority is to **integrate existing governance mechanisms**. It
is explicitly not authority to resolve a reserved matter, and — the test
this Act applied — *labelling a governance instrument is editing that
instrument, not integrating it.*

| Candidate | Authorized? | Scope | Authority source | Dependency | Boundary |
|---|---|---|---|---|---|
| Add `affected surfaces` / `verification` labels to Founder-issued instruments (`docs/governance/acts/`, Founder Decisions, Delegation Registers) | **NO** | — | `§16` grants integration, not amendment of an issued instrument | — | editing a Founder-issued governance record is a Founder act. `§6`: `IDENTIFIER ≠ DECISION BODY` |
| Add the same labels to certified P10/P11 evidence | **NO** | — | — | — | `p12_certified_evidence_guard` refuses the write, correctly and live (`O16`) |
| Add the same labels to historical instruments under `docs/architecture/history` | **NO** | — | — | — | `§17`: historical evidence is not rewritten to improve a present metric |
| Add the same labels to P12-authored architecture documents only | **YES, but** classified **OPTIONAL / METRIC-GAMING RISK** | ~30 of 403 instruments | delegated — these are AIOS's own documents | none | would move `affected surfaces` from 0/403 to ≈30/403 and change no element's status from ABSENT to ESTABLISHED. Doing it *because it moves a number* is precisely what `§7` forbids |
| Build a structural join for another `§16` link, beside the record, in the `P12-003` pattern | **AUTHORITY-GAP** | — | — | needs a *named* second gap | `W4-GAP-008`/`W2-GAP-007` existed as gaps named by prior workstreams before `W3` closed them. **No equivalent named gap exists for any other link.** Inventing one would be AIOS setting its own construction scope |
| Escalation → grant join | **ALREADY SATISFIED** | closed | `§16` | — | closed `P12-003`, residently consumed `P12-005`, re-verified live this Act |

**Finding.** The "broader `§16` chain" that `P12-005` recorded as an
executable frontier is, on inspection, **not executable under delegated
authority**. Every path to moving an ABSENT element to ESTABLISHED runs
through either amending instruments AIOS may not amend, or relabelling
AIOS's own documents in a way that improves no element's status. This is a
correction to `P12-005 O16`, made by measurement rather than by re-reading
the package.

---

## `O6` — W3/W6 Dependency Analysis

**Verdict: `SHARED DEPENDENCY`, plus one `APPARENT RELATIONSHIP ONLY`.**

| Relationship | Classification | Basis |
|---|---|---|
| W3's `§26` governance-evidence elements ↔ W6 item 5 (GOVERNANCE EVIDENCE) | **SHARED DEPENDENCY** | one instrument, `p12_governance_evidence_verification`, is simultaneously W6's measurement of item 5 and the only resident measurement of W3's `§16` chain. Neither can advance without the same 403-instrument population changing |
| W3's escalation join ↔ W6 item 9 (FAILURE) | **DEPENDENCY** — W6 depends on W3 | `p12_failure_verification.escalation_join()` reads the W3 join surface through the independent reader. W3's construction moved W6's reported detail; the reverse is not true |
| W3's `§16` chain ↔ W6 item 10 (`§49` controls) | **APPARENT RELATIONSHIP ONLY** | both concern governance integrity, and it is tempting to treat the two ACCEPTED controls as W3 work. They are not: `false certification` needs an issuance-authenticity *definition*, which is Founder-reserved, not a `§16` integration. Recording it as W3 work would make a reserved matter look like delegated work |
| W3 ↔ W6 item 8 (PROVENANCE) | **INDEPENDENT** | provenance assembly turns on `ExecutionManifest` (W4), not on any governance join |
| W6 item 6 (STATE `CONSUMER`) ↔ W2 | **DEPENDENCY** — W6 measures W2 | `p12_state_verification.SURFACE = "tools.p12_operational_state"`. The module comment states the direction explicitly: *"W6 reads W2, it does not depend on it"* — i.e. no import-time coupling, but the verdict is entirely about W2's surface |

---

## `O7` — W1–W6 State Matrix

| WS | Live state this Act | Delta since `ACT-CC-P12-005` |
|---|---|---|
| **W1** System Integration | `p12_integration_graph`: 8 integration classes, 8 edges — 4 VERIFIED, 3 UNVERIFIED, 1 RESERVED, 0 INVALID, 0 DANGLING, **8 owners unresolved**. Not verified: `phase ↔ phase`, `platform ↔ phase`, `workflow ↔ runtime`, `memory ↔ state` | **none** |
| **W2** Unified Operational State | 8 declared sources across 7 state classes; all 8 name a canonical source and authority and every read path resolves; 8 projections each carrying source, observation time and transformation | **none** to the surface. Its *measured* `CONSUMER` verdict is disputed this Act — see `O8` |
| **W3** Governance Integration | escalation → grant join resident at all three refusal-recording call sites; `escalation_join()` = `{records 3, structured 0, prose 2, refusal-type 0, governance surface 2}` | **none since `P12-005`** — re-verified, not assumed. `§16` broader chain **re-classified** from EXECUTABLE to AUTHORITY-GAP (`O5`) |
| **W4** Execution Integration | `p12_execution_chain_reader`: 4 manifests, **4 JOINED**, 0 DANGLING, 0 UNRESOLVED, 7 edges per chain | **none** |
| **W5** Self-Model | `p12_self_model_contract`: 12 canonical questions, **12 BOUND**, in order, 0 unbound; sources — 7 AUTHORITATIVE SOURCE, 4 DECLARED CONSTANT, 1 DERIVED; projection freshness distinct from source freshness; **0 authority-creating functions** | **none** |
| **W6** System-wide Verification | 13 items as inventoried in `O2` | `FAILURE` detail richer (governance surface 1 → 2 was already recorded in `P12-005`; re-verified at 2 here). No item changed classification |

---

## `O8` — Consumer Rediscovery Matrix

Rediscovered by AST this Act, resolving **both** `ImportFrom.module` *and*
each `alias.name`, because `from tools import X as y` parses with
`node.module == "tools"` — the blind spot `P12-W1-SYSTEM-INTEGRATION.md
§11` disclosed, which this programme has now hit three times.

| Surface | Resident non-test consumers found | Kind |
|---|---|---|
| `p12_governance_escalation_join` (writer) | `tools/w4_first_run.py` · `tools/w1_coordination_run.py` · `tools/w1_cross_department_run.py` · `p12_negative_control_verification` · `p12_w3_resident_wiring_proof.py` | **3 real resident call sites** + 1 control + 1 proof script |
| `p12_governance_join_reader` (reader) | `tools/p12_failure_verification.py` · `p12_negative_control_verification` | real (the W6 FAILURE measurement resolves through it) |
| `p12_execution_provenance` / `p12_execution_chain_reader` | `tools/w4_first_run.py` · `p12_failure_verification` · `p12_negative_control_verification` | real |
| `p12_operational_state` (W2) | `p12_self_model_contract` · `p12_mutation_verification` · `p12_negative_control_verification` | **see the finding below** |

**Finding — the `CONSUMER: UNSATISFIED` verdict rests on a defective
measurement.** `tools/p12_state_verification.py:65` `consumers_of()`
collects, for an `ast.ImportFrom`, only `[node.module]`, then tests
`stem in module`. For `from tools import p12_operational_state as w2`,
`node.module` is `"tools"`, so `"p12_operational_state" in "tools"` is
`False`. Proven mechanically this Act: the current shape finds **0**
consumer files; a shape that also resolves `alias.name` finds exactly
**3** — `p12_self_model_contract.py`, `p12_mutation_verification.py`,
`p12_negative_control_verification.py`. The live import lines are, in all
three, `from tools import p12_operational_state as …`.

**Why this is recorded and not fixed.** Two reasons, both binding:

1. `§3` forbids construction in this Act.
2. Correcting the measurement does **not** straightforwardly yield
   `SATISFIED`, and claiming it would be the kind of promotion `§7`
   forbids. Two of the three found consumers are verifiers, and the
   function's own docstring gives the reason tests are excluded: *"counting
   tests as consumers is how a surface nothing uses comes to look
   integrated."* A verifier is not a test, but it is also not the
   *operational* consumer the link is asking about. The third,
   `p12_self_model_contract.projection_freshness_is_not_source_freshness()`,
   genuinely **reads projection values** (`entries["runtime.observed"]`,
   `.observed_at`, `.status`) to answer a W5 question — the strongest
   candidate for a real consumer, and still a verification surface.

No canonical source settles whether a verifier counts as a consumer. The
correct disposition is therefore: fix the measurement, and *separately*
settle the semantic — not fix the measurement and let the verdict move by
side effect. Recorded in `O17` as a compound frontier.

---

## `O9` — Operational State Matrix

`Exists → provisioned → reachable → consumed → invoked → executed →
observed → verified → operational.` `§6`: `CONSTRUCTED ≠ OPERATIONAL`.

| Surface | Exists | Provisioned | Reachable | Consumed | Invoked | Executed | Observed | Verified | Operational |
|---|---|---|---|---|---|---|---|---|---|
| W3 escalation → grant join | ✅ | ✅ | ✅ | ✅ 3 resident call sites | ✅ once, by real work (`P12-005` proof: delegation `2494015de36246fd` → escalation `9cb90fa0787a478c` → JOINED) | ✅ | ✅ read back by an independent reader | ✅ | **NO** — no resident surface runs unattended |
| W4 execution manifest / chain | ✅ | ✅ | ✅ | ✅ | ✅ 4 manifests | ✅ | ✅ 4/4 name a resolving observation subject | ✅ 4/4 JOINED | **NO** |
| W2 operational state projection | ✅ | ✅ | ✅ | **DISPUTED** (`O8`) | ✅ | ✅ re-derives on call | ✅ | ✅ | **NO** |
| W5 self-model | ✅ | ✅ | ✅ | ✅ by the `§49` controls | ✅ | ✅ | ✅ | ✅ 12/12 BOUND | **NO** |
| W1 integration graph | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ 4/8 edges VERIFIED | **NO** |
| W6 verifier suite | ✅ | ✅ | ✅ | ✅ | ✅ all 13 run this Act | ✅ | ✅ | ✅ 25/25 falsifiable | **NO** |

**Every row stops at `operational`, and that is the correct and intended
result.** `OA-1` (`ACT-CC-P12-OA-001`) found that a resident non-manual
activation mechanism is **not canonically required**; `p12_runtime_verification`
reports all 10 root entry points `HAND-INVOKED ONLY`. The absence of an
autonomous runtime is a satisfied boundary, not an open gap.

---

## `O10` — Regression Register

| # | Finding | Class | How caught | Disposition |
|---|---|---|---|---|
| 1 | **`consumers_of()` misses every `from tools import <surface>` import** (`tools/p12_state_verification.py:65`), so W6 STATE's `CONSUMER: UNSATISFIED` verdict is produced by a measurement that cannot see the consumers that exist | measurement defect, pre-existing (not introduced this Act) | AST rediscovery under `§22`, by running both the current and a corrected shape against the live corpus and comparing | **RECORDED, NOT FIXED** — `§3` forbids construction. Carried into `O17` as a frontier with its unsettled semantic attached |
| 2 | `P12-005 O16` classified W3's broader `§16` chain as **EXECUTABLE**. This Act's authorization test (`O5`) finds it **AUTHORITY-GAP**: every route to it requires amending instruments AIOS may not amend | classification error in a prior package | re-derived rather than inherited, per `§8` | **CORRECTED HERE.** The prior package is not edited — `§17`; the correction is recorded in this one |
| 3 | This Act's own first AST consumer pass was written in the defective `node.module`-only shape — the same blind spot as finding 1, and the third occurrence in this programme | self-introduced, in-process | caught before any consumer claim was written | corrected before `O8` was drafted; disclosed here per `§24` rather than concealed |
| 4 | `§51` regression classes re-run live: 11 classes, **10 HELD, 0 REGRESSED**, 1 UNANCHORED (`quality`) | — | — | no regression |
| 5 | Functional inventory diff: **2089 controls at `98c0a1e` → 2507 now, 0 removed, 0 weakened** | — | — | no regression |
| 6 | Citation audit: 261 documents, 1473 citations, **0 errors** before this document was written; **262 documents, 1495 citations, 0 errors** re-run with it present, so this Act's own 22 citations all resolve | — | re-run after writing, not only before | no regression |
| 7 | Stale-state audit: 536 documents, **0 live stale assertions**, 55 preserved as history | — | — | no regression |
| 8 | Governance index: 457 records from 537 sources, **0 stale** | — | — | no regression |

Findings 1 and 3 are the same defect class. Finding 3 is disclosed because
`§24` requires disclosure of self-introduced defects rather than
concealment, and because a discovery Act that silently corrected its own
method would leave no record that the method had been wrong.

---

## `O11` — Dependency Register

| Dependency | Depends on | Type | State | Blocking? |
|---|---|---|---|---|
| `§49` `false certification` · `§50` `forge decision` | a canonical definition of **issuance authenticity** | authority | does not exist | **YES** — Founder-reserved |
| `§50` `duplicate delegation` | a canonical **prohibition** on duplicate active grants | source | does not exist; `DP-02 §11` item 10 points the other way | **YES** — source gap |
| W6 EVIDENCE | E12 Evidence Matrix criteria (`§54` `TBD`) | authority | `F-16`, unresolved | **YES** — Founder-reserved |
| CROSS-PD interfaces | cross-PD interface definition | authority + source | `F-18` / `ADR-0029` / `ESC-C7-01` open | **YES** — Architect-reserved |
| RUNTIME `verification` · FAILURE `VERIFIED` | ratification of a `verified` execution state | authority | vocabulary is ratified at three states | **YES** — Founder-reserved |
| W3 `§16` broader chain | authority to amend issued governance instruments | authority | not granted by `§16` | **YES** |
| W6 STATE `CONSUMER` | (a) the `consumers_of()` fix, (b) a settled verifier-as-consumer semantic | (a) construction, (b) semantic | (a) available, (b) unsettled | **PARTIAL** — (a) is executable, (b) blocks the verdict moving |
| `§49` `unauthorized P13 authorization` | nothing | — | the Founder fact is already resident | **NO** |
| CROSS-PHASE `P6`/`P7` | real Knowledge/Memory consumption by real work | work | not performed | **NO** — but out of W6's scope to manufacture |
| `quality` regression anchor | a resident quality gate | tooling | none exists | **NO** — optional |

---

## `O12` — Authority Register

| Matter | Holder | State | Effect on P12 |
|---|---|---|---|
| **`F-16`** — E12 Evidence Matrix | **Founder** | unresolved; `§54` `TBD` | blocks W6 item 7 (EVIDENCE). Unchanged |
| **`F-17`** — Phase ↔ PD provider | **Founder** | unresolved | W1 `platform ↔ phase` edge stays UNVERIFIED. Unchanged |
| **`F-18`** — cross-PD interface | **Architect** + source gap | unresolved; `ADR-0029`, `ESC-C7-01` | blocks CROSS-PD interface definition. Unchanged |
| **`FDP-P10-001` Security** | **Founder** | unresolved | not a global blocker (per `§13.5` of the authorization, dependency must be proven); no P12 item this Act found depends on it |
| **`FDP-P10-003` Governance Authority** | **Founder** | unresolved | as above |
| **`FDP-P10-002` Quality** | **Founder** | unresolved | the `quality` regression class is UNANCHORED. Note the distinction: adding a linter is tooling and delegated; *ratifying a quality standard* is `FDP-P10-002` and reserved. This Act classifies the tooling as OPTIONAL and does not treat it as closing `FDP-P10-002` |
| **`ADP-P10-001`** entity semantics | **Architect** | unresolved | escalation entity semantics stay reserved; the `P12-003` join was built *beside* the record for exactly this reason |
| **`OA-001`** — operational activation | resolved | **`OA-1 — NOT-A-GAP`** | re-confirmed live: a resident non-manual activation mechanism is not canonically required. All 10 entry points `HAND-INVOKED ONLY` is compliant, not deficient. **No autonomous runtime, scheduler or daemon exists or was proposed** |
| **`P13`** | **Founder** | **NOT AUTHORIZED** — `P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md §29`, `§13.5`, `§37.7` | P12 authorization confers no P13 authorization. This is *resident in the governance corpus and absent from the self-model* — the one executable frontier (`O19`) |

---

## `O13` — W6 Classification Delta (before vs after `ACT-CC-P12-005`)

| `§19` item | Before `P12-005` | After / now | Changed? |
|---|---|---|---|
| CROSS-PHASE | 6 / 8 EXERCISED | 6 / 8 EXERCISED | NO |
| CROSS-PD | 6 CURRENT, 0 interfaces | 6 CURRENT, 0 interfaces | NO |
| RUNTIME | 8 DISCOVERED, 1 ABSENT | 8 DISCOVERED, 1 ABSENT | NO |
| WORKFLOW | 4 EVIDENCED, 1 BY CONVENTION | 4 EVIDENCED, 1 BY CONVENTION | NO |
| GOVERNANCE EVIDENCE | 1 / 6 / 2 | 1 / 6 / 2 | NO |
| STATE | `CONSUMER` UNSATISFIED | `CONSUMER` UNSATISFIED | NO (but now known to be defectively measured — `O8`) |
| EVIDENCE | AUTHORITY-BLOCKED | AUTHORITY-BLOCKED | NO |
| PROVENANCE | 11/11, 7/10 joined, NOT ASSEMBLABLE | 11/11, 7/10 joined, NOT ASSEMBLABLE | NO |
| FAILURE | `REFUSED` RAISED ONLY; `governance_surface: 1` | `REFUSED` RAISED ONLY; **`governance_surface: 2`** | **detail only** — classification unchanged |
| `§49` SYSTEM NEGATIVE CONTROLS | 13 attempted, 11 REFUSED, 2 ACCEPTED | identical | NO |
| MUTATION | 8 DETECTED, 2 MISSED | identical | NO |
| REGRESSION | 10 HELD, 1 UNANCHORED | identical, control inventory 2089 → 2507 | NO |
| FRESH PROCESS | 8/8 | 8/8 | NO |

`P12-005` was a wiring Act. It moved one detail figure and no
classification — which is what `P12-005 O8` claimed, and which this Act
**verified rather than accepted**.

---

## `O14` — Evidence Register

| Evidence | Location | State |
|---|---|---|
| W3 join construction | `tools/p12_governance_escalation_join.py`, `tools/p12_governance_join_reader.py` | resident; independent-reader discipline AST-enforced |
| W3 resident-consumption proof | `p12_w3_resident_wiring_proof.py`; `docs/architecture/p12/w4-operations/` | real end-to-end run through `tools.w4_first_run.run`, three disclosed patches |
| W3 conformance | `tools/tests/test_p12_w3_resident_wiring.py` (4 controls), `tools/tests/test_escalation_subject_integrity.py` | green |
| W4 execution chains | 4 `ExecutionManifest`s | 4 JOINED, 0 DANGLING, 7 edges each |
| Provenance | `p12_provenance_verification` | 11/11 elements carried; 7/10 executions joined; `NOT ASSEMBLABLE` on the 3 historical records |
| Governance index | 537 sources → 457 records | 0 stale |
| Citations | 262 documents, 1495 citations (including this document's own 22) | **0 errors** |
| Test suites | `native_core`, `consumers`, `tools` | re-run in full this Act: **801 OK** (1 expected failure) · **276 OK** · **1113 OK** (1 skip). No test was skipped, disabled or weakened |
| Certified-evidence protection | `tools/p12_certified_evidence_guard.guard` | live refusal re-demonstrated against `docs/architecture/p11` |

---

## `O15` — Fresh-Process Verification

`p12_fresh_process_verification` — every stage re-derived in a **separate
OS process**, compared against the in-process answer.

| Stage | In-process | Fresh process | Status |
|---|---|---|---|
| repository | 537 | 537 | REPRODUCED |
| canonical sources | `62b6c28971219611` | `62b6c28971219611` | REPRODUCED |
| registries | 457 | 457 | REPRODUCED |
| state | 12 questions / 10 verified / 2 inferred / 0 unknown | identical | REPRODUCED |
| decisions | 54 | 54 | REPRODUCED |
| integration graph | `(14, True)` | `(14, True)` | REPRODUCED |
| runtime | 7 | 7 | REPRODUCED |
| evidence | 7 | 7 | REPRODUCED |

**8 / 8 REPRODUCED, 0 DIVERGED.** The instrument's own falsifiability is
demonstrated: a subprocess made to answer differently yields 8 DIVERGED of 8.

---

## `O16` — Negative-Control Report

**`§49` system negative controls — 13 attempted, 11 REFUSED, 2 ACCEPTED, 0 UNCONTROLLED.**

| Control | Status | Detail |
|---|---|---|
| self-authorization | REFUSED | Planning cannot author a delegation record — `ACT-CC-P11-005 §11` |
| authority expansion | REFUSED | unregistered Agent Instance |
| governance bypass | REFUSED | adapting the plan would need authority the plan does not hold |
| invalid provenance | REFUSED | authority record does not resolve |
| fabricated actor | REFUSED | not a registered Agent Instance |
| unauthorized delegation | REFUSED | not the authorized W4 delegator — `FD-P11-001` |
| unauthorized state mutation | REFUSED | `CertifiedEvidenceProtected` |
| unauthorized architecture mutation | REFUSED | boundary detector reports 12, not 11 |
| **unauthorized P13 authorization** | **ACCEPTED** | *"no resident surface states P13's authorization status, so nothing would contradict a claim that it is authorized"* |
| false completion | REFUSED | contradicted by the resident answer to what is incomplete (29 unbridged gates, open escalations) |
| **false certification** | **ACCEPTED** | *"the guard reads bodies and cannot distinguish an issued instrument from a forged one"* |
| stale-state acceptance | REFUSED | stale `RUNNING` refused as evidence of current state |
| historical-as-current substitution | REFUSED | 6 superseded claims registered, 55 historical uses distinguished, 0 stand as current |

**`§50` mutations — 10 attempted, 8 DETECTED, 2 MISSED** (`forge decision`,
`duplicate delegation`). **`§18` instrument falsifiability — 25 instruments,
25 DEMONSTRATED.**

The two ACCEPTED and two MISSED results are **findings about the system,
reported as such**. None was driven to zero by weakening an attempt — every
control was genuinely attempted this Act, and `ATTEMPTED` is reported
separately from `REFUSED` for exactly that reason.

---

## `O17` — P12 Frontier Register

Every remaining candidate, classified. **Nothing below was executed.**

| # | Frontier | Classification | Why |
|---|---|---|---|
| 1 | **Surface P13's resident authorization posture in the W5 self-model's `authority()` answer** | **EXECUTABLE NOW — PRIMARY** | the Founder fact is already resident and merely unreported; reporting it is integration, not authorization. Detail in `O19` |
| 2 | **Correct `consumers_of()`'s AST shape** (`p12_state_verification.py:65`) | **EXECUTABLE NOW — COMPOUND, BLOCKED ON A SEMANTIC** | the defect is proven (`O8`). The *fix* is executable; the *verdict it produces* is not settled, because no canonical source says whether a verifier is a consumer. Must not be executed as a verdict-mover |
| 3 | `§49` `false certification` + `§50` `forge decision` | **AUTHORITY-GAP — Founder** | one root cause: no canonical definition of issuance authenticity |
| 4 | `§50` `duplicate delegation` | **SOURCE-GAP** | no canonical prohibition exists; `DP-02 §11` item 10 legitimises multi-context grants |
| 5 | W6 EVIDENCE / E12 matrix | **FOUNDER-RESERVED** | `F-16`, `§54` `TBD`. Unchanged |
| 6 | CROSS-PD interfaces | **ARCHITECT-RESERVED + SOURCE-GAP** | `F-18`, `ADR-0029`, `ESC-C7-01`. Unchanged |
| 7 | Phase ↔ PD provider | **FOUNDER-RESERVED** | `F-17`. Unchanged |
| 8 | RUNTIME `verification` · FAILURE `VERIFIED` | **FOUNDER-RESERVED** | ratified execution vocabulary |
| 9 | W3 broader `§16` chain (`affected surfaces`, `verification`, 6 PARTIAL elements) | **AUTHORITY-GAP** | **re-classified this Act** from `P12-005`'s EXECUTABLE. See `O5` |
| 10 | FAILURE `RETRYABLE` | **NOT-A-GAP** | no live retry mechanism; building one is capability creation with no canonical requirement |
| 11 | PROVENANCE `NOT ASSEMBLABLE` (3 historical executions) | **NOT-A-GAP** | append-only; retro-fitting would rewrite historical evidence — `§17` |
| 12 | CROSS-PHASE `P6`/`P7` | **OUT-OF-SCOPE** | W6 measures work; it does not manufacture it. Moving the number directly is metric gaming |
| 13 | `quality` regression anchor (linter / CI) | **OPTIONAL** | legitimate engineering, no canonical P12 requirement, closes no `§19` item. Note: tooling ≠ `FDP-P10-002` ratification |
| 14 | Resident non-manual activation | **NOT-A-GAP** | `OA-1`. Re-confirmed. Not proposed, not built |
| 15 | Widening the two non-refusing W1 run scopes | **OPTIONAL, NOT RECOMMENDED** | unchanged from `P12-005 O16`; would be behaviour creation outside any requirement |

---

## `O18` — Exhaustion Determination

Tested against `§32`, and against `§33`'s distinction: this is **P12
construction exhaustion**, not W6 scope exhaustion and not P12 completion.

The test is whether any authorized, unblocked frontier remains. Frontier 1
is authorized (reporting an issued Founder decision is squarely within
`§16` integration and within the self-model's *reported, never exercised*
discipline), is blocked by nothing, and is not begun.

**`O18: P12 NOT EXHAUSTED — EXECUTABLE FRONTIER REMAINS.`**

The count is narrow and worth stating plainly: of the fifteen frontiers in
`O17`, **one** is cleanly executable and one more is executable-but-
semantically-blocked. Six are Founder- or Architect-reserved, two are
source gaps, three are not gaps at all, one is out of scope, and two are
optional. P12's remaining executable surface is close to exhausted, but it
is **not** exhausted, and `P12 EXHAUSTED — PROVEN` would therefore be a
false return.

---

## `O19` — Next Authorized Frontier

| Field | Value |
|---|---|
| **Exact name** | Surface the resident per-phase authorization posture — specifically P13's — in the W5 self-model's `authority()` answer |
| **Scope** | `tools/p12_self_model.py::authority()`. Add the phase-authorization status the Founder has already issued, with its provenance citation, to the answer's value. **Nothing else** — no new authority, no new reserved matter, no change to any other of the 12 canonical questions |
| **Canonical requirement** | `ACT §49` names `unauthorized P13 authorization` a mandatory system negative control. It currently reports **ACCEPTED** — the system does not refuse a false claim that P13 is authorized. `§49` requires the control; it does not permit leaving it accepted because it is inconvenient |
| **Authority** | Delegated. `P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md §16` authorizes integrating existing governance mechanisms. The fact is already issued — `§29` *"P13 tetap unauthorized"*, `§13.5`, `§37.7` *"P13 remains unauthorized"*. **Reporting a Founder decision is not making one**: `§6`, `IDENTIFIER ≠ DECISION BODY`, is respected because the self-model would cite the Founder instrument as the source, not assert the status on its own authority |
| **Dependency** | **None.** Both halves already exist: the Founder statement is resident in the governance corpus, and `p12_self_model.authority()` already carries `"phase authorization"` in its `founder_reserved` tuple — it reports *who holds* the authority but not *what was decided under it* |
| **Why executable** | It requires no new authority, no reserved matter resolved, no certified or Founder-issued instrument amended, no record rewritten, no vocabulary ratified, and no canonical rule invented. It is the only frontier in `O17` of which all seven are true |
| **Why it is not executed in this Act** | `ACT-CC-P12-006 §3`: *"Do not execute the next frontier even if it is authorized. Record it. The purpose of this Act is to determine what should be executed next — not to execute the next frontier."* This Act's mandate is discovery. Executing it here would be the Act authorizing its own scope expansion, which is the failure mode `§6`'s `NECESSITY ≠ AUTHORITY` exists to prevent |

**Two constraints the executing Act must carry, recorded here so they are
not lost between Acts:**

1. **The control's own check is weak and must be strengthened in the same
   cycle.** `_unauthorized_p13_authorization()` flips to REFUSED on
   `if "P13" in value` — the mere presence of the string. Satisfying it by
   inserting the token without the actual status and its provenance would
   be metric gaming under `§7`. The answer must genuinely carry the
   status with its citation, and the control must genuinely test for the
   status rather than the substring.
2. **This closes one control, not the pair.** `false certification` remains
   ACCEPTED and is Founder-reserved (`O17` frontier 3). An executing Act
   must not report `§49` as closed on the strength of moving 11 → 12.

Frontier 2 (`consumers_of()`) is the natural follow-on, but it is
**compound**: the AST fix is executable, while the verdict it produces
turns on an unsettled semantic that a construction Act must surface rather
than resolve by side effect.

---

## Constraint Compliance

| Constraint | This Act |
|---|---|
| `§3` no construction | held — no source file, test, record or evidence artifact was created or modified; this document is the sole change |
| `NECESSITY ≠ AUTHORITY` | held — `O3`/`O5` classify by authority, not by whether AIOS is capable |
| `IDENTIFIER ≠ DECISION BODY` | held — `O19` reports a Founder decision with citation rather than asserting one |
| `IMPORT ≠ CONSUMER` | held — `O8` distinguishes verifier imports from operational reads and declines to call the question settled |
| `TEST ≠ REAL SYSTEM WORK` | held — `O9` separates conformance from the one real end-to-end execution |
| `CONSTRUCTED ≠ OPERATIONAL` | held — every `O9` row stops at `operational` |
| `NATIVE CORE = 11` | held — re-counted live |
| `docs/program/AIOS_*` untouched | held — `O1` |
| no autonomous runtime / scheduler / daemon | held — none exists, none proposed; `OA-1` re-confirmed |
| historical evidence not rewritten | held — `P12-005`'s classification error is corrected *here*, not by editing that package; the 3 historical provenance records are left unjoined |
| no metric gaming | held — `P6`/`P7`, `affected surfaces` relabelling, and the P13 substring check are each identified as available-but-gaming and declined |
| no self-authorization | held — the one executable frontier is recorded, not taken |
| self-introduced defects disclosed | held — `O10` finding 3 |
