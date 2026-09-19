# P12-005 — W3 Structural Governance Join Resident Consumption — Return Package

**Act:** `ACT-CC-P12-005`. **Non-Micro-Act, single bounded mandate.**
**Frontier closed:** wire the existing structural escalation→delegation-grant
join into the three resident refusal-recording call sites.
**Result: `STOP C1`** (the three-site frontier is correctly closed) →
verification → post-construction rediscovery → **`O17`:
`P12 NOT EXHAUSTED — EXECUTABLE FRONTIER REMAINS`.**

---

## O1 — Execution Summary

- **Act:** `ACT-CC-P12-005`.
- **Branch:** `claude/aios-activation-authority-discovery-enq7bk`.
- **Starting commit:** `227dc0f` (`P12-004`), clean working tree, verified
  fresh at the start of this Act.
- **Final commit:** this Act's commit, on top of `227dc0f`.
- **Files changed:** `tools/p12_governance_escalation_join.py` (new
  `join_refusals_to_grants` helper, additive) ·
  `tools/w4_first_run.py`, `tools/w1_coordination_run.py`,
  `tools/w1_cross_department_run.py` (wiring: `record_refusals` →
  `join_refusals_to_grants`) · `tools/p12_failure_verification.py`
  (self-caught bugfix, see O9) · `tools/tests/test_escalation_subject_integrity.py`
  (updated `E2` to the new wiring call name, added two tests) ·
  `tools/tests/test_p12_failure_verification.py` (rewrote one test that
  became inaccurate, added one) · `tools/tests/test_p12_w3_resident_wiring.py`
  (new, 4 tests) · `p12_w3_resident_wiring_proof.py` (new, real execution) ·
  `docs/architecture/p12/{P12-W2-UNIFIED-OPERATIONAL-STATE,P12-W3-GOVERNANCE-INTEGRATION,P12-W4-EXECUTION-INTEGRATION}.md`
  (disclosed updates, no history rewritten) · one real delegation, escalation,
  join, instance registration and evidence file under
  `docs/architecture/p12/w4-operations/`.
- **Files intentionally untouched:** `EscalationRecord`, `EscalationRegister`'s
  existing methods, `record_refusals` itself; `docs/program/AIOS_*`;
  `native_core/`; every certified P10/P11 evidence file, including the one
  historical escalation (`23f315ba9f504272`) and its delegation
  (`4313bd2246124a94`).

## O2 — Three Call-Site Wiring Matrix

| Site | Wired | Invoked (code reached) | Real execution | Join produced | Independently verified |
|---|---|---|---|---|---|
| `tools/w4_first_run.py` | YES | YES | **YES** — real refusal, real escalation, real join, this Act | YES | YES — fresh process, adversarial mutation, real delegation resolution |
| `tools/w1_coordination_run.py` | YES | YES (reachable; `report.refusals` is always empty because both real plan steps are always in scope — confirmed by reading `STEP_SKILLS`, not by absence of evidence) | NO — cannot occur through this site's own real scenario today | N/A — nothing to join, correctly | Wiring pattern (single delegation) verified via `w4_first_run`'s identical shape |
| `tools/w1_cross_department_run.py` | YES | YES (reachable; each grant is scoped to exactly the one step it covers, so its own real scenario also never refuses) | NO — cannot occur through this site's own real scenario today | N/A | Multi-grant lookup (`grants[refusal.required]`) verified directly with two real delegations and two real refusals, plus a negative fixture proving a naive static lookup would mis-join |

**Not reported as `3/3 operational`.** One site is fully exercised with real
content; two are correctly wired and reachable but structurally cannot
produce the condition being wired for, through their own real, unmodified
scenarios, today.

## O3 — Structural Governance Chain Proof

```
REFUSAL       real — W4Executor._authorize_step raised ExecutionRefused for
              step "report-conformance", genuinely outside work_scope
              ("verify-delegation-elements",)
ESCALATION    real — recorded via the unmodified record_refusals, through
              join_refusals_to_grants, escalation_id 9cb90fa0787a478c
DELEGATION    real — delegation_id 2494015de36246fd, issued by
GRANT         W4DelegationRegistry.issue, independently resolves in
              tools.p12_provenance_verification.delegation_records()
JOIN          independently resolved JOINED by tools.p12_governance_join_reader
              (imports nothing from the writer), in a fresh subprocess
```

Adversarial mutations run live against copies of this real record this Act
(forged delegation id, forged refusal type, deleted escalation) all
correctly resolved `DANGLING`.

## O4 — Prose-Parsing Independence Report

**Mixed, by record, and precisely reported:**

- The `ACT-CC-P12-003` record (`docs/architecture/p12/w3-operations/`) was
  deliberately worded not to match the old regex and resolves `JOINED`
  through the governance surface only. **Independent of prose parsing.**
- This Act's new record (`docs/architecture/p12/w4-operations/`) uses
  `tools/w4_first_run.py`'s own unchanged subject format
  (`"plan {plan.key} / delegation {delegation.delegation_id}"`), which
  happens to also satisfy the old regex. **The reader never runs the regex
  either way** — `tools.p12_governance_join_reader` contains no prose
  parsing at all — but this specific record's subject does not, by itself,
  demonstrate independence the way the `P12-003` record does. That
  demonstration was not repeated here because changing this site's subject
  wording was outside this Act's minimal-wiring scope (`§8`/`§9`).
- **Aggregate, fresh this Act:** `records: 3 · joined_by_structured_field: 0
  · joined_by_parsed_prose: 2 · joined_by_governance_surface: 2`. Prose
  parsing is not required for either real governance-surface join to
  resolve; it happens to also succeed for one of them.

## O5 — W3 State Report

```
CONSTRUCTED    first increment (P12-003) + resident wiring (P12-005) — the
               join mechanism and its consumption at all three call sites
INTEGRATED     into three resident call sites, all three
CONSUMED       by one site with real content (w4_first_run.py); by two
               sites in the sense of "code reachable, never yet exercised"
OPERATIONAL    for the one exercised site: yes, in the narrow sense that a
               real refusal now produces a real structural join without
               further action; for the other two: the mechanism is present
               but has nothing to consume under their current real scenarios
VERIFIED       yes — independent reader, adversarial mutation, fresh
               process, 20 new/updated conformance tests across two files
REMAINING      the full §16 DECISION→AUTHORITY→RATIONALE→IMPLEMENTATION→
               VERIFICATION→CURRENT STATE chain beyond this one gap; whether
               the two never-refusing sites' scope should ever be widened
               (not decided or implied here — that would be scope creation,
               out of bounds for this Act)
```

## O6 — W1/W2/W5 Consumer Delta

| Surface | Pre-`P12-005` | Post-`P12-005` | Delta |
|---|---|---|---|
| W1 (`p12_integration_graph.py`) | 4 verified / 3 unverified / 1 reserved, 0 consumers | **identical**, re-measured fresh this Act | NONE |
| W2 (`p12_operational_state.py` via `escalation_join()`) | PARTIAL, incidental (pre-existing call, `P12-004`'s finding) | PARTIAL, incidental — same call, now returns more accurate data (bugfix, O9) | NONE (no new relationship; existing one more accurate) |
| W5 (`p12_self_model.py`, `p12_self_model_contract.py`) | 0 consumers, no reference to W3 surfaces | **identical**, re-confirmed via AST this Act | NONE |

No new consumer was created for W1, W2, or W5. Per `§22`/`§33`: none was
constructed to improve a metric.

## O7 — W4-GAP-008 / W2-GAP-007 Status

- **Classification: `CONSTRUCTED — BESIDE THE RECORD`, unchanged from
  `P12-003`.** Resident consumption added; the classification itself was
  already correct and is not re-opened.
- **Closure evidence, strengthened:** one real, resident-produced instance
  now exists in addition to the standalone proof-script instance from
  `P12-003` — two independent real demonstrations rather than one.
- **Semantic limitation, preserved (`P12-004`'s finding):** the writer
  proves a named delegation resolves to *a* real grant, not that it is *the*
  grant the specific refusal was raised under. At the one resident site
  exercised this Act, correctness rests on the caller (`w4_first_run.py`)
  supplying its own `delegation.delegation_id` — true and re-verified.
- **A second limitation, newly measured this Act:** the join does not
  distinguish an `ACTIVE` grant from a `REVOKED` one — a revoked delegation
  still resolves `JOINED`. Not new behavior (the original
  `joined_by_structured_field` measure never checked status either); stated
  because this Act specifically tested it and found it undocumented until
  now.

## O8 — W6 Classification Delta

No `§19` scope item changed classification. `FAILURE`'s `REFUSED` state
remains `RAISED_ONLY` (re-verified live this Act — `EscalationRecord` still
carries no type field). The instrument-falsifiability list
(`p12_negative_control_verification.CONTROLS`, a narrower and separate scope
from `§49`) is unchanged at 25 instruments / 25 demonstrated — no new
instrument was added this Act (the two `P12-003` entries already cover the
module-level population; `join_refusals_to_grants` is a new function in an
already-covered module, not a new module).

## O9 — Regression Register

| # | Finding | How caught | Disposition |
|---|---|---|---|
| 1 | First attempt at `p12_w3_resident_wiring_proof.py` forgot to patch `w4_first_run.OPERATIONS`, so it ran several real stages against the certified `docs/architecture/p11/w4-operations/` before `tools/p12_certified_evidence_guard.guard` correctly refused the final evidence write. Four new (not overwritten — new) files landed there. | Self-caught, before committing | Deleted (all four were untracked, none pre-existing was touched); script corrected; re-run cleanly against the intended P12 root |
| 2 | `escalation_join()`'s `joined_by_governance_surface` count was hardcoded to one directory (`docs/architecture/p12/w3-operations`) and silently missed this Act's own new join in a different directory | Caught by re-running the measurement against real new evidence rather than trusting the figure from `P12-003` | Fixed: resolves per-escalation, beside whichever directory it actually lives in; two dependent tests updated to match the corrected reality (2 real joins, not 1) |
| 3 | No modification to `EscalationRecord`, `record_refusals`, any certified P10/P11 evidence, `TraceRecord`, Native Core, or any protected artifact | — | none found |
| 4 | Full regression suite (`native_core` 801, `consumers` 276, `tools` 1113) re-run after every change: all green throughout | — | none found |

Both self-introduced defects were disclosed and corrected within this same
Act, before the Return Package was written — not carried forward silently.

## O10 — Dependency Register

| Dependency | Type | State | Blocking? |
|---|---|---|---|
| Wiring `w1_coordination_run.py`/`w1_cross_department_run.py`'s real refusal condition (would require widening their real plan/scope beyond their current grants) | design decision, not authority | not pursued — out of this Act's minimal-wiring mandate | non-blocking; explicitly not a frontier this Act opens |
| `W6 GOVERNANCE` scope item's full evidentiary chain | evidentiary | fed incrementally, not closed | non-blocking |
| `F-16`/`F-17`/`F-18` | authority | unchanged, reserved | blocking only their own scope items, untouched here |

`DEPENDENCY ≠ OWNERSHIP` and `DEPENDENCY ≠ AUTHORITY` preserved — no
dependency above was converted into either.

## O11 — Authority Register

```
F-16                    RESERVED, unchanged, not approached
F-17                    RESERVED, unchanged; no provider assignment anywhere
                        in the wired files (grepped this Act)
F-18                    RESERVED, unchanged; no interface/API/contract
                        introduced (grepped this Act)
OA-1 (NOT-A-GAP)         reconfirmed; no scheduler/daemon/loop/listener
                        pattern in any new or modified file (grepped this
                        Act); resident invocation through a hand-run proof
                        script is not autonomous self-activation
Native Core = 11         reconfirmed via derived_views._boundaries this Act
P13                      unauthorized, unchanged, not approached
```

## O12 — Negative Control Report

```
attempted:    3 live adversarial mutations this Act (forged delegation id,
              forged refusal type, deleted escalation) + 2 registered
              negative-control instruments (unchanged from P12-003) + 4 new
              conformance-level negative tests (empty/unsanctioned inputs,
              duplicate join, wrong static lookup)
detected:     all — every mutation correctly resolved DANGLING; every
              conformance negative correctly raised or asserted wrong
missed:        0
accepted:      0
unavailable:   0
added:         0 new CONTROLS registry entries this Act (P12-003's two
              entries already cover the modules touched); 4 new dedicated
              tests, 2 rewritten tests
removed:       0
weakened:      0
```

Full `p12_negative_control_verification.verify()`: **25 of 25
`DEMONSTRATED`**, re-run fresh this Act.

## O13 — Fresh-Process Verification

- Both real joins (`P12-003`'s and this Act's) resolved `JOINED`
  independently in a brand-new subprocess, and `escalation_join()`'s
  aggregate figures reproduced identically outside this session's
  interpreter.
- `native_core` (801, 1 expected failure), `consumers` (276), `tools` (1113,
  1 pre-existing environment-conditional skip) — full fresh discovery runs,
  all green, after every change in this Act.
- `tools/corpus_citation_audit.py`: 0 errors, re-run after every
  documentation change.
- `tools/p12_regression_verification.py`: 22/22 tests pass, 0 of its
  anchors regressed.
- `derived_views._boundaries`: 11, re-verified.
- `git status --short docs/program/`: empty, re-verified.

## O14 — Evidence Register

| Evidence | Type | Provenance | Verification | Freshness |
|---|---|---|---|---|
| `docs/architecture/p12/w4-operations/2494015de36246fd.delegation.json` | real delegation | `p12_w3_resident_wiring_proof.py`, this Act | resolves in `delegation_records()` | current |
| `docs/architecture/p12/w4-operations/9cb90fa0787a478c.escalation.json` | real escalation | same run, via unmodified `record_refusals` | resolves via `EscalationRegister.load` | current |
| `docs/architecture/p12/w4-operations/9cb90fa0787a478c.governance-join.json` | real structural join | `join_refusals_to_grants`, this Act | independently `JOINED`, fresh subprocess | current |
| `docs/architecture/p12/w4-operations/first-execution.evidence.json` | real run evidence | `tools.w4_first_run.run`, this Act, isolated params | contains the full evidence dict, including `escalations` | current |
| `tools/tests/test_p12_w3_resident_wiring.py` | 4 conformance tests | this Act | all pass, real objects, no mocks for the property under test | current |
| Two rewritten tests in `test_p12_failure_verification.py` | conformance | this Act | pass; distinguish per-record independence from aggregate counts | current |

## O15 — Protected Artifact Confirmation

```
docs/program/AIOS_*        modified: 0 · staged: 0 · committed: 0 ·
                            untracked: 0 (re-verified this Act)
docs/architecture/p11/      modified: 0 · untracked: 0 (the self-caught
                            defect's 4 files were deleted before commit —
                            see O9 #1; final state clean, re-verified)
Native Core                 11, unchanged
EscalationRecord             class definition unchanged; all existing
                            methods unchanged; record_refusals unchanged
TraceRecord                  untouched
```

## O16 — Post-Construction Frontier Register

Rediscovered fresh, per `§31`:

| ID | Classification | Why |
|---|---|---|
| `W6` remaining actionable scope items | **EXECUTABLE** | unchanged from `P12-004`; continue in a dedicated `W6` cycle |
| `W3`'s broader `§16` chain (`DECISION → AUTHORITY → RATIONALE → IMPLEMENTATION → VERIFICATION → CURRENT STATE` beyond escalation) | **EXECUTABLE**, large, needs scoping | not begun |
| Widening `w1_coordination_run.py`/`w1_cross_department_run.py`'s real scope so their own scenarios could refuse | **OPTIONAL, NOT RECOMMENDED** | would be scope/behavior creation outside minimal wiring; no canonical requirement calls for it |
| `W1`/`W2`/`W5` consumer gaps | **NOT-A-GAP** | unchanged, correctly not manufactured |
| `F-16`/`F-17`/`F-18` | **FOUNDER/ARCHITECT-RESERVED** | unchanged |
| `FDP-P10-001`/`003` | **FOUNDER-RESERVED** | unchanged |
| Revoked-grant join semantics (O7) | **OPTIONAL** | disclosed, not required to fix; original gap never asked for it |

## O17 — Exhaustion Determination

Tested against `§32`. Condition equivalent to `P12-004`'s "no executable
item skipped" still fails: `W6`'s remaining actionable scope items and
`W3`'s broader `§16` chain are both genuinely executable under existing
delegated authority and were not begun this Act (correctly — this Act's
mandate was the one named frontier, now closed).

**`O17: P12 NOT EXHAUSTED — EXECUTABLE FRONTIER REMAINS.`**

## O18 — Next Action

Two legitimate candidates, neither begun here:

1. Continue `P12-W6`'s own remaining actionable scope items in a dedicated
   `W6` cycle.
2. Scope (not yet construct) the remainder of `P12-W3`'s `§16` governance
   chain beyond the escalation join.

Selecting between them, or opening either, is for the governing workflow —
not decided or begun by this discovery-adjacent closing note.
