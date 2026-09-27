# P12 Population Guard Successor — Version 2: Specification and Verification

| Field | Value |
|---|---|
| **Identity** | P12 POPULATION GUARD SUCCESSOR |
| **Version** | 2 |
| **Predecessor** | P12 HISTORICAL POPULATION GUARD, version 1 |
| **Authority** | `FD-P12-007` (Register `§73`): D3 *"L2 — VERSIONED SUCCESSOR"*; D5 *"EXPLICIT LIMITED MODIFICATION AUTHORIZATION"* |
| **Implementation** | `tools/tests/test_p12_population_guard_successor.py` (one new file) |
| **Certification** | **NOT CERTIFIED.** Constructed and verified; acceptance by the applicable authority is still required (`FD-P12-007` `§19` item 8) |

## 1. Pre-modification identification (`FD-P12-007` `§12`)

Each file considered, before anything was written:

| File | Current role | Relation to the guard | Change | Authority | Expected effect |
|---|---|---|---|---|---|
| `tools/tests/test_p12_population_guard_successor.py` | none (new) | **the successor** | created | D5 *"successor Population Guard implementation"* | 13 new tests, all passing |
| `tools/tests/test_p12_governance_evidence_verification.py` | the predecessor guard and its 16 sibling controls | **the predecessor** | **none**, pinned by sha256 | D3 forbids rewriting in place | still runs, still fails visibly |
| `tools/p12_governance_evidence_verification.py` | the measurement both guards read | the measurement | **none**, pinned by sha256 | D1, D3 | unchanged |
| `tools/governance_index.py` | the population classifier | the classifier | **none**, fingerprinted (`§5`) | `§15` option 1 | unchanged |
| `tools/corpus_citation_audit.py` · `tools/p12_negative_control_verification.py` | registries that must list every **top-level** `tools/*.py` / `tools/p12_*.py` | unrelated machinery | **none** | *outside* D5 | avoided, not modified: the successor is a test module, which neither registry covers |

No file outside D5 was modified. No authority gap arose, so nothing was
escalated.

## 2. Specification (`FD-P12-007` `§6`)

| Requirement | Version 2 |
|---|---|
| 1 · Identity | `IDENTITY = "P12 POPULATION GUARD SUCCESSOR"` |
| 2 · Version | `VERSION = 2`, one after the predecessor's 1 |
| 3 · Purpose | watch the **current** directional property of the population comparison, and fail loudly if it inverts again |
| 4 · Population | the predecessor's, unchanged: every tracked `docs/**/*.md` that `governance_index.is_governance_record` accepts, read through `p12_governance_evidence_verification.by_population()` |
| 5 · Founder-act subset | the predecessor's, unchanged: the corpus documents whose path lies under `docs/governance/acts/` |
| 6 · Semantic delta | **only the direction.** v1: Founder-act ratio ≤ corpus ratio + 0.2. v2: Founder-act ratio **≥** corpus ratio − 0.2. Same five elements, same label rule, same 0.2 |
| 7 · Relation to the predecessor | named, with its identity, version, test id, introducing commit and first failing commit; its two files pinned byte for byte; checked to be neither skipped nor marked expected-failure |
| 8 · Authority | `AUTHORITY` names `FD-P12-007` |
| 9 · Verification criteria | `§4` |
| 10 · Regression evidence | `§6` |

### 2.1 Why this direction, and why this threshold

- **Direction.** It is observed, not chosen. Founder acts score higher than the
  corpus on all five elements at every measured commit from `ddc6fe3` on
  (`docs/fullstack/evidence/P12-POPULATION-GUARD-SERIES-2026-09-27.json`).
- **Threshold.** None is new. The 0.2 margin is the predecessor's, and it
  keeps v2 clear of the boundary: the smallest current v2 margin is +0.22
  (`§3`).
- **What v2 does not do.** It does not support the predecessor's historical
  argument (that the corpus-wide `§26` result is not an artefact of dilution).
  It does not restate what the predecessor meant, and it does not turn the
  predecessor's failure into a pass (`FD-P12-007` `§14`).

### 2.2 Classifier (`FD-P12-007` `§15`)

**Option 1: the current classifier is preserved.** v2 fingerprints everything
`is_governance_record` decides membership with: the identifier classes and
patterns, the label and rule patterns, the metadata fallback, `FIELD_LABELS`,
and the source of the seven functions involved. Fingerprint at construction:
`a89ac04e3c286254fe431c56aebcf579369beeb58251e49f354c880a195d421a`.

A later classifier change fails v2 with the instruction to record it as a new
successor version. Corpus evolution and classifier evolution can then no
longer mix unrecorded, as `76366be` did (the change before this successor,
which remains unquantified).

## 3. Observed at construction (dated; data, not an assertion)

Measured on the tree of this record's commit, including `FD-P12-007` itself:

| Element | Corpus | Founder acts | v1 (predecessor) | v2 (successor) | v2 margin |
|---|---|---|---|---|---|
| decision body | 110/592 = 0.186 | 21/93 = 0.226 | PASS | PASS | +0.240 |
| authority | 130/592 = 0.220 | 25/93 = 0.269 | PASS | PASS | +0.249 |
| scope | 37/592 = 0.062 | 15/93 = 0.161 | PASS | PASS | +0.299 |
| status | 176/592 = 0.297 | 47/93 = 0.505 | **FAIL** | PASS | +0.408 |
| current state | 70/592 = 0.118 | 13/93 = 0.140 | PASS | PASS | +0.222 |

## 4. Verification criteria and results

| # | Criterion | Test | Result |
|---|---|---|---|
| 1 | identity, version and authority explicit | `test_identity_version_and_authority_are_explicit` | OK |
| 2 | predecessor preserved byte for byte | `test_the_predecessor_is_preserved_byte_for_byte` | OK |
| 3 | predecessor still runs; not skipped or suppressed | `test_the_predecessor_still_runs_and_is_not_suppressed` | OK |
| 4 | same populations and margin as the predecessor | `test_it_measures_the_predecessors_populations` | OK |
| 5 | classifier preserved | `test_the_classifier_is_the_one_this_version_declares` | OK |
| 6 | a classifier change is detected | `test_a_classifier_change_moves_the_fingerprint` | OK |
| 7 | v2 holds on the current corpus | `test_founder_acts_are_not_markedly_less_machine_readable` | OK |
| 8 | the predecessor's arithmetic passes on the certified W6 figures (it works where the record says it held) | `test_the_predecessor_arithmetic_passes_on_the_historical_figures` | OK |
| 9 | every live predecessor violation is the inversion (Founder acts higher), and v2 holds on it: the exception covers nothing else | `test_every_live_predecessor_violation_is_an_inversion` | OK |
| 10 | the two versions fail only on opposite sides of the band | `test_the_two_versions_can_disagree_only_in_the_expected_direction` | OK |
| 11–13 | negative controls: v2 fails when Founder acts label far less; holds when alike; v1 fails where v2 holds | `TheSuccessorCanFail` | OK |

**Mutation checks.** Each of the following was injected at runtime and caught
by the named control, with no file changed: v2's property replaced by v1's
(criterion 7); a drifted predecessor digest (2); a stale classifier
fingerprint (5); the predecessor marked expected-failure (3); a changed
margin (4). **5 of 5 caught.**

## 5. Historical evidence intact (`FD-P12-007` `§17`, `§28` items 3–4)

`tools/p12_certified_evidence_manifest.py` `verify()` against the P12
manifest: **holds**, nothing modified or missing. Diff of the commit: 0 files
under `docs/architecture/p12/`, 0 in the manifest, 0 in the predecessor's two
files.

## 6. Regression evidence

On this commit, no existing test modified:

| Suite | Result |
|---|---|
| `tools` | **1933** run (1920 + 13 successor): 1932 pass, 1 skipped; **1 failure**, the predecessor `test_the_narrower_population_is_not_better` [status]: the classified exception |
| `native_core` | 801 OK (1 expected failure, unchanged) |
| `consumers` | 276 OK |
| `tools/bounded_exception` | 29 OK |
| `fullstack` | 109 OK (1 expected failure: FS-DP-05 concurrency property) |
| Citation audit | 0 errors; 94 warnings, unchanged |

## 7. What remains

- **Acceptance.** v2 is not certified until the applicable authority accepts
  it (`FD-P12-007` `§19` item 8). Until then the predecessor's failure is the
  classified exception in FS-08's evidence.
- **The predecessor keeps failing** while Founder acts label status more than
  the corpus. That is the signal, and it stays visible by design.
