# FS-DP-05 C1 — Runtime-derived Run Identity: Implementation and Verification Record

| Field | Value |
|---|---|
| **Decision** | Architect: *"RATIFY … C1 — Runtime-derived Run Identity"*, `acts/FS-DP-05-ARCHITECT-DECISION-RATIFY-C1-RUNTIME-DERIVED-RUN-IDENTITY.md`, Register `§79` |
| **Act** | `ACT-CC-POST-P13-AIOS-FULL-STACK-003` (Register `§78`) |
| **Date** | 2026-09-27 |
| **State** | **IMPLEMENTED · VERIFIED LOCALLY**. Preview verification pending: FS-DP-02, EXT-03 and EXT-05 still block every live run |

`ARCHITECT DECISION ≠ IMPLEMENTATION ≠ VERIFICATION` (decision `§11`). The
decision is the Architect's. What follows is what was built under it and what
the evidence shows.

## 1. What changed

| Before | After (C1) |
|---|---|
| `run_id = run-<count of run records + 1>`, the count read from the store when the Runtime started | `run_id = run-<boot id>-<execution ordinal>`: the identity of the Runtime that performs the run, then the ordinal **that Runtime** issued for its execution (`native_core` `Runtime.create_context`, unchanged) |
| boot id: time plus 24 random bits | time plus **64** random bits (`new_boot_id`), as the ratified C1 describes |
| Run Trace = global positions `{from, to}` in the Trace partition | Run Trace = `{runtime, runtime_from, runtime_to, count}`: ordinals **among that Runtime's own records**. Records of other Runtimes never enter it |
| format `fullstack.run/1` | `fullstack.run/2`. `/1` records stay as appended and are still read and addressed (FS-04 `§4` successor rule) |
| no resolver | `AIOSApplication.run_trace(run_id)` selects a run's Trace by its Runtime (`/2`) or by its recorded range (`/1`) |

Files changed: `fullstack/backend/aios.py`, `fullstack/frontend/app.js`
(Trace label for both formats), and tests. Descriptions were updated in
FS-02 `§4` and FS-04.

**Why the Runtime-local range is sound.** Under FS-DP-04 A1 a Runtime serves
one request and performs one run, so its own records are exactly that run's
Trace. A long-lived Runtime (the local server) performs one run at a time
under its own lock, so its records between two counts are that run's. The
ordering relied on belongs to that one Runtime. It is not shared state between
requests, and **identity never depends on it**: the ordinal comes from the
Runtime's execution context.

## 2. Verification (decision `§10`)

| # | Requirement | Evidence | Result |
|---|---|---|---|
| V1 | sequential executions, distinct valid ids | `ThePerRequestFunction.test_sequential_requests_get_distinct_runtime_derived_ids`: 3 requests, 3 ids, each equal to `run_id_for(boot id, ordinal)` and addressable | **PASS** |
| V2 | concurrent executions, distinct ids | `TheConcurrencyResolution.test_concurrent_requests_mint_distinct_run_ids`, the former expected failure, **un-marked by this change**; `test_n_parallel_requests_…` (12 threads, 12 Runtimes); `test_parallel_runs_in_one_runtime_are_distinct` (8 threads, 1 Runtime: ordinals 0–7) | **PASS** |
| V3 | each execution's Trace resolves to its Runtime and run | same tests: every run's Trace has its count, only its Runtime's id, and exactly one Workflow record naming `document-conformance-review/<its run id>` | **PASS** |
| V4 | lookup independent of position | `test_lookup_does_not_depend_on_position`: store rows reversed and a foreign Trace record inserted; every run still found by id | **PASS** |
| V5 | N concurrent → N ids, no duplicates | tests: 12 of 12. Measurement: **N = 50** Runtimes in parallel threads over one store: 50 runs, **50 distinct ids**, 50 stored, 50 of 50 Traces correctly attributed (150 Trace rows), 0 errors | **PASS** |
| V6 | regression | `§3` | see `§3` |
| V7 | failure safety | `test_a_failed_or_partial_run_never_lends_its_identity`: a failed run keeps its own id and Trace. A run whose record is lost leaves 3 orphan Trace records. The same Runtime's next run takes ordinal 1, not 0, and its Trace range 3–6 excludes the orphans. The lost id never appears | **PASS** |
| — | the former finding | `test_the_former_finding_now_resolves`: the interleaving that minted `run-00001` twice now gives two runs, each addressable as itself | **PASS** |
| — | legacy records | `test_records_written_before_c1_are_still_read` | **PASS** |
| — | id fits the API route pattern; bad boot ids refused | `test_run_ids_fit_the_api_pattern_and_bad_boot_ids_are_refused` | **PASS** |
| — | browser end to end | `ConsoleInABrowser`: runs are listed and open by their new ids | **PASS** |

**Mutation checks** (each reverted afterwards; `aios.py` restored byte-identical):

| Mutation | Tests failing |
|---|---|
| M1: id from the ordinal only (Runtime identity dropped) | 12 |
| M2: Trace selection ignores the Runtime (global positions) | 14 |
| M3: own-record count counts every Runtime | 14 |
| M4: boot id back to 24 random bits | 2 |

## 3. Regression

Clean run on the final tree, bytecode caches cleared, no edits during the run:

| Suite | Result |
|---|---|
| `native_core` | 801 run · OK (1 expected failure, unchanged) |
| `consumers` | 276 run · OK |
| `tools/bounded_exception` | 29 run · OK |
| `fullstack` | **115** run · **OK**. It was 109 with 1 expected failure: the FS-DP-05 concurrency property now passes, un-marked, and the finding test became 8 verification tests |
| `tools` | 1933 run · **OK** (1 skipped). The P12 predecessor guard passes at this corpus state (`§6`); `test_e11_measurement_currency` passes in the full run, as before |
| Citation audit | 0 errors · 94 warnings (baseline) |

Overall: **PASS**. The known classified item (the P12 predecessor) is
reported separately in `§6`.

## 4. Negative controls (decision `§12`)

| Control | Result |
|---|---|
| Native Core #12, Runtime or Trace redesign | none: `native_core/` unchanged. The Runtime's existing execution ordinal and the Trace record's existing `runtime` field are used as they are |
| P12 evidence, P13 roots, certified manifests | unchanged (0 files under `docs/architecture/`, `tools/`) |
| Phase 14 | none |
| Authentication or authorization | unchanged: `security.py`, scopes and `authorize` untouched; the shipped function still authenticates nobody |
| Persistence architecture | unchanged: no schema, migration or `StorageFacility` change; the run record is a new format of the same record class |
| Public API contract | unchanged: routes and the `{run_id}` pattern are the same; only the id's value and the run record's Trace field changed, as the package stated (`§R2.3`) |
| Authority | the package's idempotency (I1/I2), partial-run and Part B sub-options are not named in the decision: **nothing implemented under them** (package `§R2.14`) |

## 5. Commit and state

| Field | Value |
|---|---|
| Implementation commit | the commit that adds this record (`git log -- docs/fullstack/FS-DP-05-C1-IMPLEMENTATION-RECORD.md`) |
| Live verification | **not possible yet**: no request authenticates (FS-DP-02 undecided), the Preview is behind SSO (EXT-03), and `SUPABASE_SECRET_KEY` is absent (EXT-05). Package `§R2.8` item 5 (two parallel `POST /api/v1/runs` on the Preview) is pending |
| FS-DP-05 | RATIFIED · IMPLEMENTED · VERIFIED (local) · PREVIEW VERIFICATION PENDING |
| FS-08 | **BLOCKED**: FS-DP-02, EXT-03, EXT-05 |

## 6. Observations during verification

- **The P12 predecessor guard currently passes.** With this change's records
  tracked, Founder acts label status at 49 of 99 (0.495) against the corpus's
  179 of 603 (0.297). The predecessor's bound is 0.297 + 0.2 = 0.497. The pass
  margin is 0.002 and comes only from corpus growth. It is a reading of a
  living check (`FD-P12-007` D2), not a resolution. The next labelled Founder
  act can flip it back. Its classification under `FD-P12-007` D4 and
  `FD-P12-008` D6 is unchanged; so is the certified Successor V2, which holds
  on all five elements.
- **Stale bytecode after mutation M4.** M4 changed `token_hex(8)` to
  `token_hex(3)`, which keeps the file the same size. It was reverted within
  the same second, so Python's bytecode cache (keyed on mtime seconds and
  size) kept serving the mutated module. The first regression run therefore
  showed two fullstack failures on the id format. The source was correct
  (`cmp` against the backup). With the cache cleared, fullstack ran 115, OK.
  The regression in `§3` was run on a clean cache.
- **The first `tools` run is not used.** It ran while the Register and records
  were still being edited. The index-determinism and duplicate-identifier
  failures it showed came from that. The duplicate was real, in this
  change's own preamble, and was fixed by declaring
  `FS-DP-05-ARCHITECT-DECISION` as the decision record's identifier. `§3` is a
  clean re-run.
