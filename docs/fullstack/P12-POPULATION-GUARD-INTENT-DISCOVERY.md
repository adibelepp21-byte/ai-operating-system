# P12 Population Guard — Intent Discovery Package

Return package for `ACT-CC-POST-P13-AIOS-FULL-STACK-P12-001`. **Discovery and
evidence only.** Nothing here decides, and nothing under `tools/` or in P12
certified evidence was changed.

Evidence classes (Act `§15`): **CANONICAL** > **CERTIFIED HISTORICAL** >
**DIRECT** (repository) · **GIT** (history) · **DERIVED** (measurement) ·
**INFERENCE** · **UNKNOWN** · **CONFLICT**.

## A. Act identity

| Field | Value |
|---|---|
| Act | `docs/governance/acts/ACT-CC-POST-P13-AIOS-FULL-STACK-P12-001-P12-POPULATION-GUARD-INTENT-DISCOVERY.md` |
| Stated status | *"PROPOSED FOR FOUNDER AUTHORIZATION"*; *"DISCOVERY / EVIDENCE ONLY"*; construction and test-modification authority *"NONE"* |
| Executed under | reading the repository and its history, and documenting an escalation, which `ACT-CC-POST-P13-AIOS-FULL-STACK-002` (Founder-authorized, Register `§71`) already routes as *"IDENTIFY → FREEZE → DOCUMENT → ESCALATE"* |
| Register | `§72` |
| Subject | `tools/tests/test_p12_governance_evidence_verification.py` · `TheResultDoesNotDependOnMyChoiceOfPopulation.test_the_narrower_population_is_not_better` |

## B. Execution status

**INTENT DETERMINED WITH RESIDUAL.** The guard's population semantics are
determined with high confidence. What it was meant to do after the comparison
inverts, and who may change it, are not stated anywhere (`§O`).

## C. Six question findings

### C.1 Q1 — historical or living

**Intent: LIVING** (the guard). **Confidence: HIGH** for population semantics,
**MEDIUM** for the intended response once it fires.

The P12 evidence as a whole is **hybrid**: a dated historical record, pinned by
the P12 manifest, plus a living guard. The guard itself carries no historical
baseline, so it is not option C as the Act defines it.

| Evidence | Class |
|---|---|
| The module selects its population when it runs: every tracked `docs/**/*.md` that `tools.governance_index.is_governance_record` accepts, and the Founder-act subset by path `docs/governance/acts/`. No commit, list, count or hash is pinned (`instruments()`, `by_population()`) | DIRECT |
| The W6 record `§8`, *"The population is time-indexed, and this record is inside it"*: *"A verifier whose population includes the documents its own programme produces reports a different denominator on every run, and there is no fixed number to correct the figures to."* The figures are *"left as measured and dated rather than rewritten"* | CERTIFIED HISTORICAL (`docs/architecture/p12/P12-W6-GOVERNANCE-EVIDENCE-VERIFICATION.md`, pinned in the P12 manifest) |
| The same record `§5`: *"a conformance control holds that comparison so it cannot silently invert"*. The guard exists to keep a comparison from inverting unnoticed as the corpus changes | CERTIFIED HISTORICAL |
| The same record `§8` rejected narrowing the population: *"excluding the documents that would lower a score is how a measurement becomes an argument"* | CERTIFIED HISTORICAL |
| Introduced in `14afe69` (2026-09-12) and **never modified**. It ran in every suite since, including the certified-state suite (`tools` 1367) over a population that had already grown (40 Founder acts against 33 at creation) | GIT · DERIVED |

### C.2 Q2 — population at creation

| Item | Finding | Class |
|---|---|---|
| Source | tracked Markdown under `docs/` (`git ls-files`), not the working tree | DIRECT (`tools/governance_index.py` `tracked_markdown`) |
| Inclusion | the document's metadata block names a governance identifier or carries a recognized governance label; *"Location and filename are deliberately not consulted"* | DIRECT (`is_governance_record`) |
| Founder-act subset | path contains `docs/governance/acts/` | DIRECT (`by_population`) |
| Status detection | a line `Status: <non-empty>` (optionally bold or bulleted) within the first 80 lines | DIRECT (`_LABEL_LINE`, `_HEADER_LINES = 80`) |
| Count stated at creation | **385** instruments · **33** Founder acts · status **123/385** and **6/33** | CERTIFIED HISTORICAL (record `§3`, `§5`) |
| Count derived at the creating commit `14afe69` | **389** · **33** · status **127/389** and **6/33** | DERIVED |
| Why 385 ≠ 389 | the record measured before its own W6 records were committed (record `§8` gives 390 one commit later) | CERTIFIED HISTORICAL |
| The exact 385-document list | **UNKNOWN**: a working-tree measurement, not stored. The 389-document list at `14afe69` is exactly derivable | UNKNOWN · DERIVED |
| Classifier drift | `76366be` (2026-09-24) added `FDR` and `GOAL` to the governance identifier classes, which can change membership. Its separate effect is **UNKNOWN**: isolating it would mean running one commit's classifier on another commit's corpus | GIT · UNKNOWN |

### C.3 Q3 — Founder instruments after P12

| Population | Post-P12 Founder instruments | Evidence |
|---|---|---|
| **Historical** (the W6 record's dated figures; P12 certification) | **EXCLUDED**: they did not exist, and nothing pins a population that could include them. The manifest pins the record's bytes, not a document list | CERTIFIED HISTORICAL (manifest scope) · GIT |
| **Current living** (the guard as it runs) | **INCLUDED**: by construction, and by the record's explicit rejection of excluding later governance records that *"are governance records by the same test every other instrument passes"* | DIRECT · CERTIFIED HISTORICAL |

`P12 HISTORICAL POPULATION ≠ CURRENT GOVERNANCE CORPUS`: shown, not assumed.
They were already different at certification (444 against 389).

### C.4 Q4 — baseline, hash, snapshot

**Baseline type: DERIVABLE.** There is no explicit baseline in the guard.

| Item | Finding | Class |
|---|---|---|
| Pinned commit, tree, list, count or hash in the test or module | **none** | DIRECT |
| P12 certified evidence manifest | `docs/governance/AIOS_P12_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json`: certified commit `6968c6e1fda014ff4c07cd1f82762d3190918895`, 121 files under `docs/architecture/p12/`, certifying instrument `FD-P12-006` | CERTIFIED HISTORICAL |
| The W6 record in that manifest | `P12-W6-GOVERNANCE-EVIDENCE-VERIFICATION.md` · sha256 `5470b8c8abbea864b0c42284e45d5f737c0c784bd5fc5e19ba8813b4cadd02e9` | CERTIFIED HISTORICAL |
| `tools/` in any manifest | **no**; the manifest covers `docs/architecture/p12/` only | DIRECT |
| Population at certification | derivable from `6968c6e`: **444** instruments · **40** Founder acts · status **137/444**, **10/40** | DERIVED |

### C.5 Q5 — certified test immutability

**CONDITIONAL.** No canonical rule names `tools/` tests as certified baselines,
and none permits editing a W6 conformance control when the corpus grows.

| Source | What it says | Class |
|---|---|---|
| `FDR-G1` `§3`–`§7` | *"A certified baseline is immutable evidence of the state that was certified at the time of certification."* Evolution by versioned successor and Founder certification; changing certification semantics is Founder-reserved | CANONICAL |
| `FDR-G2` `§9` | *"Non-material maintenance that does not alter certified architectural semantics may continue under existing delegated authority"*; it *"MUST NOT … modify certification semantics"*; otherwise the evolution model applies | CANONICAL |
| `FD-P12-006` | *"Certification shall not be inferred merely from the completion record or test count"*; the `§26` governance corpus findings stay open residuals *"Their respective ownership and authority boundaries remain unchanged"*; for the live test, *"Do not modify the test merely to preserve certification"* | CANONICAL |
| P12 manifest scope | certified evidence is `docs/architecture/p12/`; `tools/` is not in it | CERTIFIED HISTORICAL |
| P12 certification handoff record | *"None of the certification conclusions rests on the test suite."* Added **after** certification (`e5ac0f5`) and not in the manifest | DIRECT |
| Full Stack Act, operative | `native_core/`, `consumers/`, `tools/` are modified only *"unless strictly necessary and independently authorized"* | CANONICAL (operative Act) |
| That the guard is therefore *not* a certified baseline | read from the manifest's scope | **INFERENCE**: not a rule, and not used as one |

The condition that decides: whether changing this guard would *"modify
certification semantics"* (`FDR-G2` `§9`). No canonical text answers it, and
certification semantics are Founder-reserved (`FDR-G1` `§7`).

### C.6 Q6 — lifecycle when the population changes

**The existing structure is HYBRID, and that part is determined.** The
historical figures are preserved and pinned: the record, the manifest, and
record `§8`'s *"left as measured and dated"*. The measurement is living: the
guard.

**What happens to the living guard once its comparison inverts: UNKNOWN.** No
record states it.

| Candidate | Evidence for or against |
|---|---|
| A · test revision | not ruled out; needs `tools/` authority and the `§C.5` condition |
| B · successor test | FDR-G1's model, **if** the guard counts as certified; the Q5 condition is undecided. Any successor must also settle what the superseded guard does in the suite, which touches `tools/` too |
| C · baseline pinning | **evidence against**: record `§8` rejected narrowing the population; pinning to a pre-growth tree excludes exactly the documents that now fail the guard |
| D · re-measurement | the guard already re-measures on every run; there is nothing separate to re-run |
| E · hybrid | describes the structure that already exists |

Every option except leaving the guard red touches `tools/`.

## D. Evidence inventory

| # | Evidence | Class |
|---|---|---|
| 1 | `tools/p12_governance_evidence_verification.py` | DIRECT |
| 2 | `tools/tests/test_p12_governance_evidence_verification.py` | DIRECT |
| 3 | `tools/governance_index.py` (`tracked_markdown`, `is_governance_record`) | DIRECT |
| 4 | `docs/architecture/p12/P12-W6-GOVERNANCE-EVIDENCE-VERIFICATION.md` `§3`, `§5`, `§8` | CERTIFIED HISTORICAL |
| 5 | `docs/governance/AIOS_P12_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json` | CERTIFIED HISTORICAL |
| 6 | `docs/governance/acts/FD-P12-006-P12-CERTIFICATION-AND-LIVE-VERIFICATION.md` | CANONICAL |
| 7 | `docs/governance/acts/FDR-G1-POST-P13-GOVERNANCE-FOUNDATION.md` `§3`–`§7` | CANONICAL |
| 8 | `docs/governance/acts/FDR-G2-P13-CLOSURE-RESIDUAL-GOVERNANCE-AND-POST-CLOSURE-OPERATING-MODEL.md` `§9`, `§10` | CANONICAL |
| 9 | `docs/architecture/p12/AIOS-P12-FINAL-CERTIFICATION-AND-P13-TRANSITION-HANDOFF-RECORD.md` | DIRECT (post-certification) |
| 10 | `docs/governance/AIOS_P10_AUTONOMOUS_EXECUTION_VERIFICATION_v1.0.md` `§128.4` (the same dated figures) | DIRECT |
| 11 | commits `14afe69`, `0e2badd`, `67b405b`, `76366be`, `e5ac0f5`, `6968c6e` | GIT |
| 12 | `docs/fullstack/evidence/P12-POPULATION-GUARD-SERIES-2026-09-27.json` (53 commits) | DERIVED |

## E. Historical population · F. Current population (Act `§14`)

| Measurement | At creation `14afe69` | At P12 certification `6968c6e` | Current `96bab67` | With this Act's record tracked |
|---|---|---|---|---|
| Total population | 389 (record: 385) | 444 | 588 | 589 |
| Founder instruments | 33 | 40 | 91 | 92 |
| Founder `Status` labels | 6 | 10 | 46 | 47 |
| Founder ratio | 0.182 | 0.250 | 0.505 | 0.511 |
| Corpus ratio | 0.327 (127/389) | 0.309 (137/444) | 0.298 (175/588) | 0.299 (176/589) |
| Threshold (corpus + 0.2) | 0.527 | 0.509 | 0.498 | 0.499 |
| Guard | PASS | PASS | **FAIL** | **FAIL** |

All four columns are DERIVED by the unchanged module on each tree. The record's
own figures at creation (385, 123/385) are CERTIFIED HISTORICAL.

## G. Baseline, hash, snapshot

`§C.4`.

## H. Test history

| Commit | Date | Change |
|---|---|---|
| `14afe69` | 2026-09-12 | guard, module, W6 record created together |
| `0e2badd` | 2026-09-12 | record `§8` added (population time-indexed); guard unchanged |
| `6968c6e` | 2026-09-18 | P12 certified state; guard unchanged; passes |
| `67b405b` | 2026-09-24 | module: certified-write barrier in `__main__` only; measurement unchanged |
| `76366be` | 2026-09-24 | classifier: identifier classes gain `FDR`, `GOAL` (population definition) |
| `20742f5` | 2026-09-27 | first commit at which the guard fails |

No rename. The test file has exactly one commit.

## I. P12 certification relationship

The guard **existed before** certification and **passed** at the certified
state. Certification's conclusions do not rest on the suite (`FD-P12-006`; the
handoff record, post-certification). The guard's *subject*, the `§26`
governance corpus finding, is an open residual of P12 certification whose
*"ownership and authority boundaries remain unchanged"* (`FD-P12-006`).

## J. Corpus growth analysis

- Founder acts' status labelling rose steadily: **0.18** at creation, **0.25**
  at certification, **0.51** now. The limit stayed near **0.50** throughout.
  This is a trend over 53 commits, not one outlier.
- The guard's directional claim, *"It scores worse"*, had inverted on **all
  five** checked elements by `ddc6fe3`, long before any failure. The +0.2
  tolerance absorbed it until `status` crossed.
- The first failing commit is `20742f5`, which tracked the verbatim ACT-002
  instrument. Its text states its status as a label, like most recent Founder
  instruments.
- **Classification of the failure** (Act `§5.4`): **CORPUS EVOLUTION**,
  detected as the guard was designed to detect it (*"cannot silently
  invert"*). Also **TEST ASSUMPTION**: the guard holds an empirical premise
  (Founder acts label less) that was true of 33 acts. A possible **BASELINE
  DRIFT** component (`76366be`) is unquantified. **Not TEST DEFECT**: the code
  does what the record says.
- **Substantive consequence for `§26`.** The finding the guard protected, that
  a narrower population does *not* score better, no longer holds for `status`:
  Founder instruments are now more machine-readable than the corpus on that
  element. This bears on the `§26` residual and its owner (*"governance
  labelling standard"*, P12 handoff record row 8), not only on the test.

## K. Immutability rule

`§C.5`: **CONDITIONAL**.

## L. Lifecycle determination

`§C.6`: structure **HYBRID** (determined); post-inversion treatment of the
living guard **UNKNOWN**.

## M. Disposition matrix

| Question | Finding | Evidence | Classification | Confidence |
|---|---|---|---|---|
| Q1 Historical vs living | guard **LIVING**; the P12 evidence set is hybrid | module code; record `§5`, `§8`; git | DIRECT · CERTIFIED HISTORICAL · GIT | HIGH (response on inversion: MEDIUM) |
| Q2 Original population | tracked `docs/**/*.md` accepted by `is_governance_record`; acts by path; stated 385/33, derived 389/33 | module; record `§3`; derived | DIRECT · CERTIFIED HISTORICAL · DERIVED; the 385 list UNKNOWN | HIGH |
| Q3 Post-P12 Founder instruments | historical **EXCLUDED**; living **INCLUDED** | manifest scope; record `§8`; module | CERTIFIED HISTORICAL · DIRECT | HIGH |
| Q4 Baseline / hash / snapshot | **DERIVABLE**; none in the guard; record pinned `5470b8c8…` at `6968c6e` | manifest; git | CERTIFIED HISTORICAL · DERIVED | HIGH |
| Q5 Certified test immutability | **CONDITIONAL** on *"modify certification semantics"* | FDR-G1; FDR-G2 `§9`; FD-P12-006; manifest scope | CANONICAL; one INFERENCE flagged | MEDIUM |
| Q6 Population-change lifecycle | structure HYBRID; post-inversion **UNKNOWN** | record `§8`; no rule found | CERTIFIED HISTORICAL · UNKNOWN | MEDIUM |

## N. Proposed disposition

**Proposed, not decided** (Act `§20`): **D + F**.

- **D.** Keep the historical record exactly as it is: it is correct for its
  dated corpus and is pinned by the manifest. Treat the guard as the living
  measurement it was built to be.
- **F. Founder Decision Required** for the living guard, because every
  remaining option touches `tools/` and may touch certification semantics
  (`FDR-G1` `§7`; `FDR-G2` `§9`; the Full Stack Act's `tools/` clause). Options
  for the Founder:

| # | Option | Note |
|---|---|---|
| F1 | Revise the guard in place under an explicit authorization, restating the comparison the evidence now supports | the Founder decides whether this is non-material maintenance (`FDR-G2` `§9`) |
| F2 | Supersede it with a versioned successor guard; state what the superseded one does in the suite | FDR-G1 route; also needs `tools/` authority |
| F3 | Pin it to a historical tree | the certified record `§8` weighs against this |
| F4 | Leave it failing as a standing signal, and decide how the FS-08 criterion *"Full regression passes"* treats it | no `tools/` change |

Also for the owner of the `§26` labelling standard: the population finding
itself changed (`§J`).

**Not proposed:** any change to Founder instruments, their placement or their
status lines (Act NC-05, NC-07, NC-08).

## O. Unknowns

| # | Unknown | Missing evidence |
|---|---|---|
| U-1 | What the guard should do after its comparison inverts | no record states it; the author wrote only *"cannot silently invert"* |
| U-2 | Whether changing a W6 conformance control *"modifies certification semantics"* | no canonical text; Founder-reserved |
| U-3 | The exact 385-document list the record measured | never stored |
| U-4 | The separate effect of the classifier change `76366be` | would need a cross-commit counterfactual run, which this Act excludes |

## P. Conflicts

| # | Conflict | Resolution |
|---|---|---|
| CF-1 | Record `§5` says Founder acts *"score worse"*, yet its own figures show them **better** on two elements: authority 11/33 (0.333) against 107/385 (0.278), and effective date 7/33 (0.212) against 33/385 (0.086). The guard's +0.2 tolerance absorbed authority and does not check effective date | **reported, not resolved.** The record is certified and unchanged |
| CF-2 | 385 (record) against 389 (derived at the same commit) | explained by the record's own `§8`; not a contradiction |
| CF-3 | `§70` reported `tools` 1920 OK on a tree where the ACT-002 file was untracked | already corrected in Register `§71` |

## Q. Negative-control results

| Control | Result |
|---|---|
| NC-01 no change under `tools/` | 0 files (verified by diff at commit) |
| NC-02 threshold | unchanged |
| NC-03 baseline | unchanged (manifest untouched) |
| NC-04 P12 certification records | 0 changes under `docs/architecture/p12/`; manifest untouched |
| NC-05 Founder instruments | no existing instrument changed; one new verbatim record added |
| NC-06 corpus deletion | none |
| NC-07 renaming to alter population | none |
| NC-08 status-line relocation | none; this Act's own record keeps its status line and is counted (`§E`) |
| NC-09 suppression · NC-10 skip | none |
| NC-11 self-ratification · NC-12 Founder decision · NC-13 Architect decision | none created |
| NC-14 FS-08 gate | unchanged (`fullstack/readiness.py` untouched) |
| NC-15 production | untouched |

The historical measurements ran in a disposable worktree outside the
repository, removed afterwards.

## R. Repository change report

Added: this package; the Act, verbatim; the measurement series; Register `§72`.
Changed: nothing else. Effect on the guard: tracking the Act's record adds one
Founder act with a status label, so 46/91 becomes **47/92**, and the guard
still fails (`§E`).

## S. Regression result

Run on the tree this package is committed with; no test modified:

| Suite | Result |
|---|---|
| `tools` | **1919 / 1920**: FAILED (failures=1, skipped=1). The one failure is `test_the_narrower_population_is_not_better` [status] |
| `native_core` | 801 OK (1 expected failure, unchanged) |
| `consumers` | 276 OK |
| `tools/bounded_exception` | 29 OK |
| `fullstack` | 109 OK (1 expected failure: the FS-DP-05 concurrency property) |
| Citation audit | 0 errors; 94 warnings, unchanged |

The failure is reported as it stands and not turned into a pass.

## T. Required next decision

**Founder:** a disposition for the living guard (`§N` F1–F4), including any
authorization to change `tools/`, and whether the FS-08 criterion *"Full
regression passes"* is met while it stands. **Architect:** none; this is not
a Freeze `§10` area.
