# P12-004 — Post-Cycle Frontier Reconciliation & Exhaustion Discovery

**Act:** `ACT-CC-P12-004`. **Mode: discovery/reconciliation only — no
construction performed.** Every claim below was re-derived this Act, in a
fresh process where practicable, from the actual repository state on branch
`claude/aios-activation-authority-discovery-enq7bk` at commit `a094f2c`
(clean working tree, in sync with origin, verified at the start of this Act).
**Result: `STOP B` — an authorized frontier is identified and recorded, not
executed.** **`O12`: `P12 NOT EXHAUSTED — EXECUTABLE FRONTIER REMAINS`.**

---

## Q1 — Is `W4-GAP-008`/`W2-GAP-007` actually closed?

[E] Re-derived, not assumed. `tools/p12_failure_verification.escalation_join()`,
called fresh this Act:

```text
records                          2
joined_by_structured_field       0
joined_by_parsed_prose           1
naming_the_refusal_type          0
joined_by_governance_surface     1
```

[E] The two persisted records were read directly, byte-for-byte, this Act:
`docs/architecture/p11/w4-operations/23f315ba9f504272.escalation.json`
(historical, `subject` contains `"delegation 4313bd2246124a94"`, matches the
regex) and `docs/architecture/p12/w3-operations/0991300404cf44d8.escalation.json`
(new, `subject` deliberately does not match the regex) plus its beside file
`0991300404cf44d8.governance-join.json` naming
`delegation_id: aa591daf55ca4714`, `refusal_type: ExecutionRefused`.

[E] **Fresh-process re-verification, this Act, a brand-new interpreter**:
`tools.p12_governance_join_reader.resolve_all` over
`docs/architecture/p12/w3-operations/` returns exactly one result,
`status: JOINED`, and independently confirms `aa591daf55ca4714` is present in
`tools.p12_provenance_verification.delegation_records()`'s live population.

[E] **Live adversarial falsification, run this Act** (not merely cited from
the prior Act's tests): a copy of the real join, in a temporary directory,
was mutated three ways and resolved independently each time —

| Mutation | Result |
|---|---|
| `delegation_id` forced to `"f"*16` (nobody issued) | `DANGLING` — *"does not resolve to a real grant"* |
| `refusal_type` forced to `"TotallyMadeUp"` | `DANGLING` — *"is not a sanctioned refusal"* |
| the escalation record deleted, join left in place | `DANGLING` — *"join names an escalation the register does not hold"* |

[D] The chain does not silently degrade to `JOINED` under any of the three
falsifications `Q4` names. **Prose regex is not required for this new
record** — `joined_by_parsed_prose` stays at exactly `1` (the historical
record only), which is the deliberate proof this increment's `subject` was
worded not to match it.

[C] **What is not proven, disclosed rather than left implicit.** The writer
(`join_escalation_to_grant`) validates that `delegation_id` is a non-empty
string and resolves to *some* real grant — it does not independently
re-derive that the named delegation is *the one the specific refusal was
actually raised under*. In the one real instance, that correctness rests on
the caller (`p12_w3_governance_escalation.py`) supplying the same
`delegation.delegation_id` object it used to construct the `W4Executor` that
raised the refusal — which is true and was re-read from source this Act — but
the mechanism itself does not cross-check it against, say, the escalation's
`required`/`held` fields or the delegation's `work_scope`. This is not a
regression: it matches the semantics `escalation_join()`'s **original**
`joined_by_structured_field` check already used (`payload.get("delegation_id")
in known`) — the original gap never asked for cryptographic non-repudiation,
only for a structural reference instead of a parsed one, and that is what
exists. Recorded as a boundary of this increment, not a defect.

**Q1 answer: `CLOSED`**, under the gap's own originally-stated definition
(structural reference vs. parsed prose), with the boundary above disclosed
rather than hidden. The historical gap is preserved as historical fact — the
one pre-existing record was not touched, gained no join file, and its
`joined_by_parsed_prose` status is unchanged.

---

## Q2 — Is `W3` now `CONSTRUCTED`?

[D] **Granular, not blanket.**

| Component | State |
|---|---|
| Escalation→grant structural join (writer + reader) | **CONSTRUCTED**, verified |
| Real execution proving the join for one instance | **CONSTRUCTED** |
| Wiring into the three resident refusal-recording call sites (`tools/w4_first_run.py`, `tools/w1_coordination_run.py`, `tools/w1_cross_department_run.py`) | **NOT CONSTRUCTED** — confirmed by AST this Act: none of the three imports `p12_governance_escalation_join` |
| `DECISION → AUTHORITY → RATIONALE → IMPLEMENTATION → VERIFICATION → CURRENT STATE` chain across Founder Decisions/ADRs generally (`§16`'s full scope) | **NOT CONSTRUCTED** — this increment addressed one named gap inside that chain (`AUTHORITY` for one escalation class), not the general chain |
| Governance visibility integration (the broader `W3` charter beyond escalation) | **NOT CONSTRUCTED** |

**`W3 = CONSTRUCTED`** is false as a blanket statement. **`W3`'s first
increment is `CONSTRUCTED`**, precisely bounded to the table above.

---

## Q3 — Is `W3` operational?

[E] Distinguished, per the Act's own vocabulary, using AST-confirmed real
imports (not grep — grep initially misreported this exact check on a
`from tools import X as y` pattern during this Act's own investigation,
disclosed in the Regression section below):

```text
provisioned   YES — both modules exist and import cleanly
reachable     YES — importable from tools/
consumed      PARTIAL — see O6 below
invoked       YES, once for real (p12_w3_governance_escalation.py)
executed      YES, once for real
observed      YES — the join and escalation files are on disk, readable
verified      YES — independent reader, 16 tests, 2 negative controls, fresh
              process
operational   NO, in the sense of "resident production path" — nothing in
              the three real refusal-recording call sites invokes the
              writer; the only non-test, non-demonstration invocation is the
              one-off proof script, which is hand-invoked exactly like every
              other P12 root entry point (`P12-OA-001` precedent)
```

**Q3 answer: `W3`'s new surface is constructed and verified, not
operational.** The real system work that exists (`p12_w3_governance_escalation.py`'s
one run) proves the mechanism works; it does not make the mechanism part of
any resident, repeatedly-exercised production path.

---

## Q4 — Does `REFUSAL → ESCALATION → DELEGATION GRANT` hold structurally?

Answered item by item, all re-verified this Act:

1. **Refusal real?** Yes — `W4Executor._authorize_step` raised
   `ExecutionRefused` for a genuine out-of-scope step, not a constructed
   exception object.
2. **Escalation real?** Yes — recorded through the unmodified, reused
   `record_refusals` helper, on disk, readable.
3. **Escalation structurally references the delegation context?** Yes, via
   the beside-file, not via the escalation record itself (which is
   unmodified).
4. **Delegation grant real?** Yes — resolves in
   `tools.p12_provenance_verification.delegation_records()`'s live
   population, re-confirmed this Act.
5. **Relation machine-readable?** Yes — plain JSON, three fields.
6. **Independent reader resolves it?** Yes, in a fresh subprocess this Act.
7. **Survives adversarial wording?** Yes — the `subject` text was worded to
   defeat the old regex, and does; the three mutation attacks above (Q1) all
   correctly produced `DANGLING`.
8. **Prose regex still a required fallback?** For the **one historical
   record**, yes — permanently, since `§22` forbids retroactively joining it.
   For **new refusals through the three resident call sites**, effectively
   yes **today**, because those call sites do not yet call the new writer
   (Q2) — the fallback is not required by the mechanism, but by the absence
   of wiring.
9. **Observable and persistable?** Yes — plain files under
   `docs/architecture/p12/w3-operations/`.

[D] **Structural join exists ≠ governance system operationally consumes
it**, exactly as `§28` of this Act requires distinguishing. The join
mechanism is proven; it is not yet load-bearing for any resident execution
path.

---

## W1–W6 Post-Cycle Reconciliation

**W1** — `CONSTRUCTED=TRUE · VERIFIED=TRUE · OPERATIONAL=FALSE`, unchanged.
[E] `tools/p12_integration_graph.py` imports nothing related to `W3`'s new
surfaces (AST-confirmed this Act). **W3 did not change any W1 edge, edge
count, or classification.** The `governance ↔ execution` `DELEGATES` edge
(already `VERIFIED`, `4/4` manifests) is unrelated to the escalation join —
it resolves `ExecutionManifest`↔`TraceRecord`, a different pair.

**W2** — `CONSTRUCTED=TRUE · VERIFIED=TRUE · OPERATIONAL=FALSE`, unchanged in
classification, **one real evidentiary change found and disclosed**: `W2`'s
own module, `tools/p12_operational_state.py`, still imports nothing from `W3`
directly (AST-confirmed), but its `_project_escalation()` calls
`tools.p12_failure_verification.escalation_join()`, which **this Act's prior
cycle extended** to also report `joined_by_governance_surface`. Because
`_project_escalation` does `dict(join)` — spreading the *entire* returned
dict — **`W2`'s projected `escalation.raised` state entry now factually
carries a value sourced from `W3`**, without `W2`'s own code having been
touched or having deliberately chosen to consume `W3`. This is `PARTIAL`
consumption in `O6` below, not `NO` and not full architectural integration —
recorded precisely rather than rounded either direction. `W2-GAP-007`'s
disclosure (added in the prior cycle) remains accurate: the *count* `W2`
projects is unchanged; what changed is the shape of the dict one already-read
field inside it carries.

**W3** — see `Q1`–`Q4` above. `CONSTRUCTED = first increment only`,
`OPERATIONAL = NO`, `VERIFIED = TRUE` for what was built.

**W4** — `CONSTRUCTED=TRUE · VERIFIED=TRUE · OPERATIONAL=FALSE` (hand-invoked
by design), unchanged. [E] The `W4-GAP-008` note in
`P12-W4-EXECUTION-INTEGRATION.md §13` was updated in the prior cycle to point
at `W3`'s fix; re-read this Act, still accurate. **`OA-1 — NOT-A-GAP`
re-confirmed** — no new canonical text, Founder instrument, or Architect
decision surfaced this Act that bears on activation authority; nothing in
`W3`'s construction touches invocation mechanism (the new driver script is
hand-invoked, hasn't been added to any scheduler, and contains no such
pattern — re-verified by grep this Act, no matches for
`schedule|daemon|cron|while True|event_loop|listen(`).

**W5** — `CONSTRUCTED=TRUE · VERIFIED=TRUE · OPERATIONAL=FALSE`, unchanged.
[E] `tools/p12_self_model.py` and `tools/p12_self_model_contract.py` import
nothing related to `W3`'s new surfaces (AST-confirmed this Act). **`W5` has
no new consumer and was not asked to gain one.** No technically-possible
new self-model representation (e.g., "what governance joins exist") was
constructed merely because it is now possible — `§3`'s prohibition on
building a consumer to look busy was honored.

**W6** — see `O10` below. `EXHAUSTED=FALSE`, unchanged. `REFUSED` remains
`RAISED_ONLY` (re-verified this Act, live) — `W3`'s fix did **not** promote
this `W6 FAILURE` classification, correctly, since `EscalationRecord` itself
still carries no type field.

---

## O6 — Consumer Rediscovery Matrix

AST-verified this Act (not grep — see Regression Register for why that
distinction matters here specifically):

| Surface | Exists | Consumed | Resident consumer | Real system work | Verified |
|---|---|---|---|---|---|
| `p12_governance_escalation_join` (writer) | YES | PARTIAL | `p12_negative_control_verification` (negative-control demonstration only, temp dir) · `p12_w3_governance_escalation.py` (one-off proof script) | YES, once | YES |
| `p12_governance_join_reader` (reader) | YES | YES | `tools/p12_failure_verification.py` (real, in `escalation_join()`) · `p12_negative_control_verification` | YES | YES |
| `p12_failure_verification` (extended) | YES | YES | `tools/p12_operational_state.py` (**W2**, pre-existing call, now returns richer data) · `p12_negative_control_verification` (**W6**) | YES | YES |
| `W1` integration graph | YES | NO | none (unchanged, `P12-W1` finding stands) | — | YES |
| `W2` operational state | YES | PARTIAL (see above) | none *new*; pre-existing `W6` verifier call | — | YES |
| `W5` self-model | YES | NO | none (unchanged) | — | YES |

**Central question — did `W3` create a real consumer relationship for `W1`,
`W2`, or `W5`?**

- **`W1`: NO.**
- **`W2`: PARTIAL.** Not a deliberate architectural integration — `W2`'s own
  code is untouched and does not reference `W3` — but a factual, transitive
  data-flow exists through a pre-existing `W6` call `W2` already made, whose
  return shape `W3`'s prior-cycle work extended.
- **`W5`: NO.**
- **`W6`: YES**, deliberately — this is expected and correct; `W6` exists to
  verify `P12` surfaces including new ones.

No test, fixture, import-only reference, or documentation mention was
counted as a resident consumer anywhere in this table.

---

## O7 — Regression Register

| # | Finding | Severity | Disposition |
|---|---|---|---|
| 1 | This Act's own first consumer-discovery pass used a substring/grep-adjacent AST check that inspected only `ImportFrom.module`, missing `from tools import p12_governance_escalation_join as join` — the exact `node.module == "tools"` blind spot `P12-W1-SYSTEM-INTEGRATION.md §11` already disclosed once this programme. **Caught before being reported**, not after: the check was corrected (also resolving `alias.name`) before any consumer claim in this document was written. | Self-caught, in-process | Disclosed here per `§17` historical-integrity and `§24` honesty; no artifact was published with the wrong figures |
| 2 | Writer accepts any resolvable `delegation_id` without cross-checking it against the specific refusal's `required`/`held` fields (`Q1`, disclosed above) | Structural boundary, not a regression — matches the original gap's own definition of "structured" | Recorded as a frontier item, not fixed this Act (`No-Construction Rule`) |
| 3 | No change found in: unauthorized escalation, escalation without provenance, fabricated grant, stale grant reference, missing grant reference, historical-record overwrite, frozen-record mutation, provenance loss, UUID regeneration, evidence mismatch, Native Core expansion, hidden ownership/authority transfer, `W3` absorbing `W4`/`W5`/`W6` scope, `W2` becoming an implicit universal source, verifier/writer coupling (the reader provably does not import the writer — re-parsed by `ast` this Act), false `PASS`, stale cached result, test-only evidence, Founder/Architect authority inference, silent authorization | none found | — |

Full regression suite re-run this Act: `native_core` 801 (1 expected
failure), `consumers` 276, `tools` 1107 (1 pre-existing environment-skip) —
**all green, identical to the end of the prior cycle.** Citation audit: 0
errors. `tools/p12_regression_verification.py`'s eleven anchors: re-run,
**0 regressed**.

---

## O8 — Dependency Register

| Source | Target | Type | Canonical basis | State | Blocking? | Unblock path |
|---|---|---|---|---|---|---|
| Wiring the join into the 3 resident call sites | `W3`'s writer | uses | `§16` | not yet exercised | non-blocking for anything else | future increment, within existing delegated authority |
| `W2`'s `escalation.raised` projection | `W3`'s reader (transitively) | data-flow | pre-existing `W6` call | live, incidental | non-blocking | none needed |
| `W6 GOVERNANCE` scope item | `W3`'s full `§16` chain | evidentiary | `§19` | partially fed by this increment | non-blocking | continue `W3`/`W6` in a future cycle |
| `W6 EVIDENCE` scope item | `F-16` | authority | `§54` | unchanged, reserved | blocking (for that one item only) | Founder decision |
| `W6 CROSS-PD` scope item | `F-18` | authority + source | `§48` | unchanged, reserved | blocking (for that one item only) | Architect decision + interface definition |
| `W1`/`W2` provider assignment | `F-17` | authority | `§9`/`§17` | unchanged, reserved, 16/16 reads unresolved | blocking (for those edges only) | Founder/Architect decision |

`DEPENDENCY ≠ OWNERSHIP` and `DEPENDENCY ≠ AUTHORITY` preserved throughout —
no dependency above was converted into an ownership or authority claim.

---

## O9 — Authority Boundary Register

| Boundary | Status this Act | Evidence |
|---|---|---|
| `F-16` (E12 Evidence Matrix) | **RESERVED, unchanged** | `§54` still `TBD`; not approached this Act |
| `F-17` (Phase↔PD provider) | **RESERVED, unchanged** | no provider assignment found anywhere in `W1`–`W6`, re-scanned this Act |
| `F-18` (cross-PD interface) | **RESERVED, unchanged; `NO NEW F-18 SURFACE CREATED`** | grep + reading confirms no interface/API/signature/contract introduced |
| Security (`FDP-P10-001`) | **RESERVED, unchanged** | no binding decision body found; not re-searched this Act beyond confirming no new claim was made |
| Governance Authority (`FDP-P10-003`) | **RESERVED, unchanged** | same |
| Quality (`FDP-P10-002`) | **RESERVED, unchanged, untouched** | not implicated by this increment |
| Autonomous runtime / self-activation | **`OA-1 — NOT-A-GAP`, reconfirmed** | no scheduler/daemon/loop pattern in any new file (re-grepped this Act); the new driver script is hand-invoked |
| `P13` | **UNAUTHORIZED, unchanged** | not approached |

No Founder or Architect authority was inferred from technical necessity
anywhere in this Act's own reasoning — every classification above traces to
an actual decision body already read in a prior cycle and re-confirmed by
absence-of-new-evidence this Act, not re-derived from scratch where nothing
changed.

---

## O10 — W6 Classification Delta

| `§19` item | Pre-cycle (start of `ACT-CC-P12-003`) | Post-cycle (now) | Changed? |
|---|---|---|---|
| CROSS-PHASE CONTRACTS | VERIFIED (partial) | unchanged | NO |
| CROSS-PD INTERFACES | SOURCE-BLOCKED + ARCHITECT-RESERVED (`F-18`) | unchanged | NO |
| RUNTIME | ACTIONABLE / measured | unchanged | NO |
| WORKFLOW | ACTIONABLE / measured | unchanged | NO |
| GOVERNANCE | ACTIONABLE — `P12` | **evidentiary progress** (one `W3` gap closed feeds this item) but not reclassified — the broader chain this item ultimately needs is still open | PARTIALLY — evidence added, classification unchanged |
| STATE | BLOCKED — DEPENDENCY (`P12-W2`) | unchanged | NO |
| EVIDENCE | AUTHORITY-BLOCKED (`F-16`) | unchanged | NO |
| PROVENANCE | ACTIONABLE | unchanged (escalation join is not part of `§34` execution provenance) | NO |
| FAILURE | `RAISED_ONLY` for `REFUSED`; richer `escalation_join()` detail | **classification unchanged**, detail text richer (re-verified live this Act) | NO (detail only) |
| NEGATIVE CONTROLS (`§49`, system-level) | 13 attempted / 11 refused / 2 `ACCEPTED` | **unchanged** — `tools/p12_system_negative_controls.py` has zero dependency on the new `W3` surfaces (AST-confirmed this Act) | NO |
| (instrument-falsifiability list, `p12_negative_control_verification.CONTROLS` — a different, narrower scope than `§49`) | 23 instruments, 23 demonstrated | 25 instruments, 25 demonstrated | grew by 2, all still `DEMONSTRATED` — this is coverage of the new instruments themselves, not a `§19` scope-item reclassification |
| MUTATION | unchanged | unchanged | NO |
| REGRESSION | unchanged | unchanged, re-run this Act, 0 regressed | NO |
| FRESH PROCESS | unchanged | unchanged, re-run this Act | NO |

**No `§19` scope item changed classification this cycle.** The only
movement is additional evidence inside `FAILURE`'s detail text and two new
entries in a narrower, separate instrument-coverage list. No item was newly
discovered, closed, or reopened.

---

## O11 — Frontier Register

| ID | Classification | Why | Authority | Dependency | Next action |
|---|---|---|---|---|---|
| Wire `join_escalation_to_grant` into `w4_first_run.py`/`w1_coordination_run.py`/`w1_cross_department_run.py` | **EXECUTABLE** | mechanism exists, tested, verified; only the three call sites need one additional call each | delegated, `§16`, unexercised | none blocking | candidate for next construction Act |
| Writer cross-validation against the specific refusal (`Q1` boundary) | **OPTIONAL** | hardens the join beyond the original gap's own success definition | delegated if pursued | none blocking | not required; record only |
| `W3`'s broader `DECISION → AUTHORITY → RATIONALE → IMPLEMENTATION → VERIFICATION → CURRENT STATE` chain | **EXECUTABLE**, large scope | `§16`'s full charter, only one narrow slice addressed so far | delegated, `§16` | needs its own scoping pass | future increment; scope before constructing |
| `W1`/`W2`/`W5` consumer gaps | **NOT-A-GAP** (already falsified) | tried once (`W2→W5`), correctly refused; not retried | delegated | a genuine consumer with matching semantics, none found | none — do not manufacture |
| `F-16` | **FOUNDER-RESERVED** | unchanged | Founder | none | none |
| `F-17` | **FOUNDER/ARCHITECT-RESERVED** | unchanged | Founder + Architect | none | none |
| `F-18` | **ARCHITECT-RESERVED + SOURCE-GAP** | unchanged | Architect | interface definition | none |
| `FDP-P10-001`/`003` | **FOUNDER-RESERVED** | unchanged | Founder | none | none |
| `W6` remaining actionable items | **EXECUTABLE** | `RUNTIME`/`WORKFLOW`/`PROVENANCE` already `ACTIONABLE` per prior classification | delegated, `§19` | none blocking | candidate for a dedicated `W6` cycle |
| Blueprint v2.1 formal canonicalization | **FOUNDER-RESERVED** (classified, not exercised) | `DERIVED ≠ CANONICAL`, no resident adoption mechanism | Founder | none | decision-ready if ever wanted |

---

## O12 — Exhaustion Determination

[D] Tested against all fourteen conditions in `§15`:

```
1.  all canonical P12 surfaces rediscovered         YES — this Act
2.  W1–W6 reconciled                                YES — above
3.  all known gaps classified                        YES — O11
4.  all authorized executable items considered        YES — O11
5.  no executable item skipped                        NO — see below
6.  reserved matters remain reserved                   YES
7.  dependencies explicit                              YES — O8
8.  source gaps explicit                               YES
9.  no new regression unresolved                       YES — O7, none found
10. no new dependency blocks an otherwise-executable item  YES
11. evidence current enough for its claim              YES — fresh this Act
12. fresh-process verification succeeds                YES
13. current state reproducible                         YES
14. protected artifacts remain protected               YES
```

**Condition 5 fails.** `O11` names at least one genuinely `EXECUTABLE` item
under existing delegated authority (wiring the join into the three resident
call sites) that was deliberately **not** executed this Act — correctly,
under `§24`'s `No-Construction Rule` for a discovery gate, but its existence
means exhaustion cannot be truthfully claimed.

**`O12: P12 NOT EXHAUSTED — EXECUTABLE FRONTIER REMAINS.`**

Not `AUTHORITY/DEPENDENCY BOUND`: the remaining item is not blocked by any
reserved boundary. Not `UNKNOWN`: the evidence is sufficient to classify it
positively. `STOP A` from the end of the prior cycle is superseded — `§28`'s
own invariant, `STOP A FOR ONE CYCLE ≠ P12 EXHAUSTION`, is exactly what this
determination demonstrates rather than merely states.

---

## O13 — Fresh-Process Verification

- `tools.p12_governance_join_reader.resolve_all` — re-run in a new
  interpreter, matches the in-process result.
- Adversarial mutation suite (Q1) — run against temporary copies, in-process
  this Act; all three mutations correctly produced `DANGLING`.
- `native_core` (801, 1 expected failure), `consumers` (276), `tools` (1107,
  1 pre-existing skip) — full fresh discovery runs, all green.
- `tools/corpus_citation_audit.py` — 0 errors.
- `tools/p12_regression_verification.py` — 0 of 11 anchors regressed.
- `tools/p12_negative_control_verification.verify()` — 25 of 25
  `DEMONSTRATED`, 0 `NOT DEMONSTRATED`, 0 `UNAVAILABLE`.
- `derived_views._boundaries` — 11, re-verified.
- `git status --short docs/program/` — empty, re-verified.

## O14 — Negative-Control Report

```
attempted:    25 total (23 carried, 2 from the prior W3 cycle)
detected:     25
missed:        0
accepted:      0
unavailable:   0
added:         0 this Act (all additions were the prior cycle's)
removed:       0
weakened:      0
```

Plus the three live adversarial mutations run directly by this Act against
the real `W3` join (Q1) — all three correctly refused (`DANGLING`), not
counted in the 25 above since they are ad hoc falsification, not entries in
the `CONTROLS` registry.

## O15 — Protected Artifact Confirmation

```
docs/program/AIOS_*    modified: 0 · staged: 0 · committed: 0 · untracked: 0
                        (git status --short docs/program/ empty, re-verified this Act)
Native Core             11 boundaries, re-verified this Act
```

## O16 — Recommended Next Action

Only because `O11`/`O12` found a genuine executable frontier: **wire
`join_escalation_to_grant` into the three resident refusal-recording call
sites** (`tools/w4_first_run.py`, `tools/w1_coordination_run.py`,
`tools/w1_cross_department_run.py`), so future real refusals gain a
structural join automatically rather than requiring a separate proof script.
This is recorded as a candidate, not begun — the governing workflow, not
this discovery Act, decides whether and when to open the next construction
cycle.

---

## Historical Integrity Statement

Preserved, not rewritten: the original gap (`W4-GAP-008`/`W2-GAP-007`, prose
join), the original defect (`EscalationRecord` carries no structured
reference), the original evidence (`23f315ba9f504272`, still resident,
still joined only by prose, still untouched), the closure mechanism (beside
the record, `tools/p12_governance_escalation_join.py`), the closure evidence
(the new real escalation and join, this cycle), and this cycle's
independent verification (this document). Nothing above required editing a
previously-persisted record to remain true.
