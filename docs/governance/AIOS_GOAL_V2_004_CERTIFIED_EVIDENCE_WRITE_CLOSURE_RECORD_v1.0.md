# GOAL-V2-004 — Certified-Evidence Write Closure · P10 · P11 · P12 — Record v1.0

| Field | Value |
|---|---|
| **Goal** | `GOAL-V2-004` (`acts/GOAL-V2-004-CERTIFIED-EVIDENCE-WRITE-CLOSURE.md`) |
| **Frontier** | `FR-3-01`, determined by `GOAL-V2-003` |
| **Executor** | Claude Code — AIOS Co-Founder + Delegated CEO (`DEL-CFV2-CEO-001`) |
| **Date** | 2026-09-24 |
| **Measured from** | `ef89545`, clean tree (baseline) |
| **Construction commit** | `67b405b` |
| **Re-discovery commit** | `7e45d9d` (pushed) |
| **Result** | **GOAL-V2-004 TARGET ACHIEVED — CERTIFIED-EVIDENCE WRITE CLOSURE ESTABLISHED FOR P10, P11, AND P12** (§1, §26) |

Labels: **[OBS]** observed or measured this execution · **[INF]** inference ·
**[REC]** recommendation. No prior report is relied on. Each prior claim used
here was re-measured.

---

## 1. Target status

**GOAL-V2-004 TARGET ACHIEVED — CERTIFIED-EVIDENCE WRITE CLOSURE ESTABLISHED FOR P10, P11, AND P12.**

That claim means only that the evidence-protection Target was achieved (Goal
`§27`). It does not mean P10, P11 or P12 are complete again, AIOS complete,
system integrity complete, architecture final, or Founder acceptance. The
sequence was verify (`acc8bb3`), persist (`7e45d9d`, pushed), re-discover and
verify again (`7e45d9d`, §24).

## 2. Current certified state of P10

| Question (`§11`) | Answer | Label |
|---|---|---|
| What is certified | Phase 10 — Department Ecosystem | [OBS] |
| Who certified it | Founder (Moriarty), `FD-P10-005`, *"☒ APPROVED — CERTIFY P10 AS COMPLETE"* | [OBS] |
| When | Instrument dated 10-09-2026. Registered in Decision Register `§13` | [OBS] |
| Exact state | The 36 files under `docs/architecture/platform-organization`, as at `e7a3d73`. That is the commit that persisted `FD-P10-005` and the first in which the root exists. **Anchor choice:** the instrument names no evidence commit. No later commit changes the root, so every candidate anchor yields the same bytes | [OBS] / anchor [INF] |
| Where represented | Evidence root from the guard's `PHASE_EVIDENCE_ROOTS`. Manifest: `AIOS_P10_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json` | [OBS] |
| How verified | `tools/certified_evidence_integrity.py`. The manifest is rebuilt from `e7a3d73` by `from_commit` and compared in the suite | [OBS] |

Current state: **36/36 intact**, 0 modified, 0 missing, 0 unreadable, 0
unexpected [OBS].

## 3. Current certified state of P11

| Question | Answer | Label |
|---|---|---|
| What | Phase 11 — Autonomous Organization | [OBS] |
| Who | Founder, `FD-P11-002` (*"YES — CERTIFY"*) | [OBS] |
| When | Effective 2026-09-11. Register `§13` | [OBS] |
| Exact state | The 58 files under `docs/architecture/p11` at `98c0a1e`, the commit that persisted `FD-P11-002`. The root last changed at `e4a8ad5`, an ancestor, and never after. Same anchor reasoning as P10 | [OBS] / anchor [INF] |
| Where | `docs/architecture/p11`. Manifest: `AIOS_P11_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json` | [OBS] |
| How verified | As P10 | [OBS] |

Current state: **58/58 intact**, no drift [OBS].

## 4. Current certified state of P12

| Question | Answer | Label |
|---|---|---|
| What | Phase 12 | [OBS] |
| Who | Founder, `FD-P12-006` (decision field `P12 CERTIFICATION = CERTIFY`) | [OBS] |
| When | 2026-09-18. Register `§15` | [OBS] |
| Exact state | 121 files at `6968c6e`, named *"final measured certified state"* by the handoff record `§1.2` | [OBS] |
| Where | `docs/architecture/p12`. Manifest `AIOS_P12_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json` (`GOAL-V2-002`), **unchanged** | [OBS] |
| How verified | `tools/p12_certified_evidence_manifest.py`, still passing, and now also the common verifier | [OBS] |

Current state: **121/121 intact**. One *declared* addition, the handoff record,
which is recorded in the index with its basis [OBS].

No certification was created, changed or revoked. The guard still resolves
exactly `{10, 11, 12}` from the same three instruments. That was checked before
and after the one change to its resolution rule (§21, `N-2`) [OBS].

## 5. Entry points discovered

Discovery is by content, not by list. An entry point is any tracked `.py` file
carrying a `__main__` guard, plus every `__main__.py`
(`tools/certified_write_probe.py discover`). Test modules run as suites [OBS].

| Group | Count at `ef89545` | Forms run |
|---|---|---|
| Repository-root scripts | 11 | by path |
| `tools/*.py` CLIs | 47 | `-m tools.x` **and** by path (94 runs) |
| Package `__main__` (`tools.bounded_exception`) | 1 | `-m` |
| Historical (`docs/architecture/history/legacy-execution`) | 13 | by path |
| Argument-targeted writer invocations | 4 | aimed at P10, P11 and P12 |
| Test suites (tools, native_core, consumers, bounded_exception) | 4 | `unittest discover` |
| **Total runs** | **127** | |

Construction adds three CLIs (`certified_write_barrier`,
`certified_evidence_integrity`, `certified_write_probe`). The post-construction
probe at `acc8bb3` found 11 + 50 + 1 + 13 entry points and ran **133**
invocations [OBS].

**Classification after construction** (`acc8bb3`, `§12` vocabulary) [OBS]:

| Class | Runs | Entry points |
|---|---|---|
| GUARDED | 12 | W-1…W-8 (5 historical proofs plus 3 argument-targeted runs), the `corpus_health`, `cross_department` and `w1` proofs, and the tools suite (its deliberate controls) |
| SAFE | 3 | the observation, workflow and observed-work proofs, which write only `docs/operations/runtime-observations/` |
| NON-WRITING | 105 | every other tools CLI in both forms, the `bounded_exception` package, three suites, the unknown-key run, and the probe itself, which refuses to nest (rc 3) |
| RETIRED / HISTORICAL | 13 | `docs/architecture/history/legacy-execution` scripts. They fail at import (ADR-0019) and write nothing |
| **UNKNOWN** | **0** | |
| WRITES-CERTIFIED | **0** | |

**Certified writes: 0.** No GUARDED run changed any file before its refusal:
no certified file, and no live file either. There are no half-writes.

## 6. Write paths discovered

**Baseline probe at `ef89545`**, each run in a disposable worktree
[OBS]: `GUARDED 3 · SAFE 3 · WRITES-CERTIFIED 8 · RETIRED/HISTORICAL 13 ·
NON-WRITING 100 · UNKNOWN 0`. There were **11 certified changes** in total.

| # | Entry point | Certified write (in the copy) | API | Half-write |
|---|---|---|---|---|
| W-1 | `p12_trace_durability_proof.py` | M `p12/trace-stores/w4-conformance-verification/trace` | Native Core storage `open(…, "ab")` | — |
| W-2 | `p12_w3_governance_escalation.py` | A escalation and governance-join (`p12/w3-operations`), A delegation (`p12/w4-operations`) | `write_text` in `escalation_register`, `p12_governance_escalation_join`, `w4_delegation` | — |
| W-3 | `p12_w3_resident_wiring_proof.py` | M a `p12/w4-operations` instance | `agent_instance_registry` `write_text` | **yes**: written, then refused |
| W-4 | `p12_w4_integrated_execution.py` | M `p12-w4-integrated-execution/trace`, A a delegation | storage append, `w4_delegation` | **yes**: written, then stopped by `p12_execution_provenance`'s no-overwrite check (`ProvenanceIncomplete`) |
| W-5 | `w4_first_execution.py` | M `p11/w4-operations/engineering-intelligence-instance-001.instance.json` | `agent_instance_registry` | **yes** |
| W-6 | `validate_execution_catalog.py --graph-out <P10 file>` | M `platform-organization/README.md` | `Path.write_text` on an argument | — |
| W-7 | `validate_execution_catalog.py --graph-out <P11 path>` | A `p11/probe-graph.json` | same | — |
| W-8 | `governance_index --index <P12 path> build` | A `p12/probe-index.json` | `GovernanceIndex.write` | — |
| W-9 | tools test suite: `test_corpus_citation_audit` VF-11 fixture | A then D a probe file (ZZ-VF11-PROBE) in the P10 root `platform-organization`, on every suite run | `write_text` / `unlink` | net zero: **invisible to any after-the-fact check** |

W-1…W-5 are `GOAL-V2-003`'s `B-03`, re-found fresh. **W-6…W-9 are new.**
W-9 is a test fixture that wrote into certified P10 evidence and then removed
its own file. Neither the manifests nor `git status` could see it. The barrier
found it the first time the suite ran under it (§21, `N-1`).

A static scan found further unguarded writers that no entry point's default
invocation reaches: `delegation_reconciliation`, `planning_continuity`,
`escalation_register`, `agent_instance_registry`, `w4_delegation`,
`p12_governance_escalation_join`, `governance_index.write`, `p12_knowledge_admission`,
and the Native Core storage backend. It also found `subprocess` use: Python
children (the three observation proofs, `e11_measurement`,
`p12_fresh_process_verification`, `p12_knowledge_admission_verifier`) and
read-only `git` [OBS]. The barrier sits below all of them, so they need no
per-writer repair (§9).

## 7. Write paths repaired

| Path | Repair |
|---|---|
| W-9 | The fixture now writes its untracked probe into `docs/architecture/candidates/`, which the audit also scans and which is not certified. The regression it guards (VF-11) is tested unchanged |
| W-1…W-8 and every static writer | Not repaired one by one. The barrier refuses each write before it begins, whatever API it uses (§8, §9) |

## 8. Write paths intentionally refused

W-1…W-8. Their targets are certified evidence: P12's trace, w3 and w4 stores,
P11's w4 store, and P10, P11 and P12 paths named by argument. The historical
proofs W-1…W-5 are one-shot executions, and their outputs are the certified
record. Re-running one has no live target under any current Goal, so refusal
is the correct outcome, not an inconvenience (§16). W-6…W-8 write wherever
their caller points. Pointing them at a live path still works [OBS].

## 9. Certified evidence protection model

```text
PREVENTION   tools/certified_write_barrier.py   refuse before the write begins
DETECTION    tools/certified_evidence_integrity  compare by content, every phase
REFERENCE    manifests + index, index sha256 in Register §18
```

**Prevention.** A CPython audit hook (`sys.addaudithook`, PEP 578). The
interpreter raises an audit event *before* each of these operations takes
effect: `open` in any writing mode or flag, `os.rename`/`replace`, `remove`,
`rmdir`, `mkdir`, `truncate`, `chmod`, `chown`, `utime`, `link`, `symlink`,
xattr, the `shutil` copy, move, rmtree and archive family, and
`sqlite3.connect`. The hook resolves the path, including relative paths,
`dir_fd`, symlinks and ancestors of a root, and raises
`CertifiedWriteRefused`. That exception is a `CertifiedEvidenceProtected` and a
`PermissionError`. The operation never starts:
`TARGET CERTIFIED → REFUSE → NO WRITE`.

* **What is protected** is determined at installation from two sources, and
  neither can shrink the other. The guard (from instruments and Register)
  supplies the certified roots and the certifying instruments. The manifests
  supply their own files and recorded roots. Striking a certification from
  the Register leaves the evidence protected (§13, M4).
* **Fail-closed.** If the set cannot be determined, every write inside the
  repository is refused (§13).
* **Installation.** On `import tools` (new `tools/__init__.py`). In the
  `__main__` block of every path-runnable CLI (37 files; the block is inserted
  there so no cited line number shifts). In every Python child, through a
  `PYTHONPATH` bootstrap (`tools/certified_write_barrier_site/sitecustomize.py`,
  which chains the system `sitecustomize`).
* **Processes.** A shell, `os.system` or any unknown program is refused. `git`
  may run read-only subcommands against this repository, and anything against
  another tree. A Python child must carry the bootstrap. `-I`, `-S` and `-E`
  are refused.
* **Stated limits** [INF]. The hook governs Python code. It does not govern
  native code that writes directly (C extensions, `ctypes`). It cannot see the
  `dir_fd` of `os.open(..., dir_fd=)`. A test holds that no resident code uses
  that form. It does not defend against resident code deliberately rewriting
  the barrier's own in-process state. Detection covers whatever passes
  regardless.

## 10. P10 integrity mechanism

A content manifest, the same mechanism as P12. Content manifests fit here:
P10's evidence is a fixed set of documents with no legitimate live mutation.
Detection is via `tools/certified_evidence_integrity.py`, with the manifest's
and instrument's sha256 held in the index.

## 11. P11 integrity mechanism

The same. P11's `w1-operations`, `w4-operations` and
`x-department-operations` are certified run records (§16).

## 12. P12 integrity mechanism

The `GOAL-V2-002` manifest and verifier, **unchanged and still passing**
(`test_p12_certification_integrity`, 22 tests). It is now also verified by the
common verifier, which adds `UNREADABLE`, declared additions and reference
checks.

## 13. Mutation / negative-control results

Every control runs against a temporary copy (unit tests) or a disposable
worktree (`certified_write_probe --mutations`). The authoritative tree was
verified intact **before and after** each run [OBS].

| Control (`§15`) | Where | Result |
|---|---|---|
| M1 remove / bypass the write barrier | worktree of `67b405b`: `tools/__init__.py` and the bootstrap emptied, then `w4_first_execution.py` run | The writer modified `p11/w4-operations/…instance-001.instance.json` **in the copy**. Detection: P11 `MODIFIED`, holds = false |
| M2 target a live writer at a certified root | worktree, barrier intact: `validate_execution_catalog --graph-out docs/architecture/p12/…` | **Refused**, 0 certified writes |
| M3 change / delete / add / unreadable | worktree | P10 `MODIFIED`, P11 `MISSING`, P12 `UNEXPECTED` and `UNREADABLE`, each named |
| M4a alter reference: Register strikes `FD-P12-006` | worktree | Fault *"P12 has a manifest but is not certified"*. The barrier **still protects** P12 |
| M4b alter reference: a P11 manifest hash | worktree | `manifest altered` fault |
| M4c alter reference: `FD-P10-005` bytes | worktree | `certifying instrument altered` fault |
| Unit: 14 write-API cases on a protected temp root (every `open` mode and `os.open` flag, `json.dump`, rename/replace in and out, remove/unlink/rmdir/rmtree, mkdir/touch, truncate/chmod/utime, hard and symbolic links, the `shutil` family, sqlite, a symlink alias, a relative path) | temp | All refused, bytes unchanged. Reading still works |
| Unit: shell, `os.system`, unknown program, bootstrap-skipping Python | process | All refused |
| Unit: fail-closed on an unreadable reference | child process | Every write in the repository refused. A write outside it still works |
| Unit: index altered | temp copy | *"index sha256 is not recorded in the Decision Register"* |
| Unit: a planted, unregistered P12 instrument (number 999) | temp copy | No longer resolves (§21, `N-2`) |
| Unit: dangling symlink or directory in place of a file | temp copy | `UNREADABLE` |

## 14. Regression results

Measured on the construction tree (`acc8bb3` plus this record) [OBS]:

| Suite | Run A | Run B |
|---|---|---|
| tools | **1454 OK** (1 skipped) | **1454 OK** (1 skipped) |
| native_core | 801 OK (1 expected failure) | 801 OK (1 expected failure) |
| consumers | 276 OK | 276 OK |
| bounded_exception | 29 OK | 29 OK |
| legacy-execution archive | 21 import errors: known, ADR-0019, unchanged | same |
| Citation audit | 0 errors · 89 warnings (unchanged) | same |
| Stale-state audit | 0 live stale · 55 historical | same |

In both runs, every barrier refusal in the tools suite was one of the
deliberate controls: 46 against temporary roots, and 8 process-launch
controls. **No other test attempted a certified write.** After both runs the
working tree was unchanged and the live root was empty.

Tools went from 1404 to 1454 tests: 50 new in `test_certified_write_closure`.
No existing test was weakened. Three were changed: the VF-11 fixture location
(W-9), the `governance_index` boundary (N-4), and the guard oracle that a
planted prefix no longer resolves (added, not relaxed).

Before these clean runs, run #1 failed four tests. All four came from one
citation in this record, which named the removed VF-11 probe path. That was
corrected before runs A and B.

## 15. Evidence integrity results

`tools/certified_evidence_integrity.py` on the authoritative tree, before and
after every run above [OBS]:

| Phase | Intact | MODIFIED | MISSING | UNREADABLE | UNEXPECTED | Reference faults |
|---|---|---|---|---|---|---|
| P10 | 36/36 | 0 | 0 | 0 | 0 | 0 |
| P11 | 58/58 | 0 | 0 | 0 | 0 | 0 |
| P12 | 121/121 | 0 | 0 | 0 | 0 (1 declared) | 0 |

Cross-checks: certified `{P10, P11, P12}` = indexed `{P10, P11, P12}`. The
index sha256 is recorded in Register `§18`. Each manifest was rebuilt from its
commit and is identical.

## 16. Live/certified separation result

The `GOAL-V2-002` separation holds. The live root
`docs/operations/runtime-observations` is not protected: the barrier's
`refuses()` returns False for it. The three observation proofs wrote there in
the baseline, and do so again under the barrier (§24) [OBS].

**No directory was frozen that holds legitimate live state** [INF, reasoned].
The only stores inside certified roots that anything writes are P12's trace,
w3 and w4 stores and P11's w4 store. Each is the output of a completed,
certified execution (W-1…W-5). No current Goal, scheduler or runtime needs
new executions of them. The runtime is not autonomous and has no daemon. The
barrier refuses by path, and any live store is outside every certified root.
If a future Goal re-enables those workflows, their stores belong under
`docs/operations/`, as the observations were moved. That is a dependency to
record (§18), not construction this Goal authorizes.

## 17. Historical modifications preserved

Nothing was rewritten. The P12 post-certification rewrites (`7f6120c`,
`d18bac4`) remain in history. The `GOAL-V2-002` restoration and Register
`§16` stand. The Registers were appended to (`§18`) and not edited. No
certified file was touched: all three manifests hold [OBS].

## 18. Dependencies discovered

* **D-1.** Re-running the W-1…W-5 workflows as *live* work would need live
  stores outside the certified roots. None exists, and none is needed now.
  This relates to the recorded future dependency `W-1`.
* **D-2.** Barrier coverage depends on CPython audit events. A change of
  interpreter implementation would need re-verification.
* **D-3.** A process started outside the repository's Python (a shell script,
  a non-Python tool) is not governed. Detection still sees what it changes.

## 19. Remaining work

None within this Target [INF]. The governed residuals are stated rather than
closed: the audit-hook limits (§9) and D-1…D-3. None of them is an open write
path from a resident entry point. The probe and the static completeness tests
hold that.

## 20. Blocked work

Unchanged and outside this Goal: P13 (Founder review of v0.4 and `GAP-0001`),
`FD-2`, escalation `23f315ba9f504272`, F-4's `GOVERNANCE_INDEX.md` authority
question, and the legacy-execution archive import errors (ADR-0019, Architect
ruling pending).

## 21. New findings

* **N-1.** A test fixture wrote into certified P10 evidence on every suite
  run, and was invisible to content checks (W-9). It is repaired.
* **N-2.** A guard resolution defect. `_register_identity` accepted any prefix
  of two or more tokens containing a digit, so `FD-P12` matched because the
  Register mentions other `FD-P12-…` records. An unregistered
  P12 instrument numbered 999 therefore *resolved*, and striking `FD-P12-006` from the
  Register left P12 resolved. That contradicts the rule the function
  implements (`FD-P12-004` / `D-P12-027-02`: a claim must resolve against a
  record). It now requires the candidate as a whole identifier (not followed by
  `-` or a word character). The resolved set is identical before and after:
  `{10, 11, 12}` from the same three instruments, and 0 anomalies. The fix is
  one line, so no cited line shifts.
* **N-3.** Three argument-driven writers (W-6…W-8) could be aimed at certified
  evidence. `B-03` had not found them, because it ran only default invocations.
* **N-4.** The `governance_index` module declares *"Dependencies: Python
  standard library only"*, and a boundary test holds it. The library stays
  stdlib-only. The test now also permits exactly one import: `tools` inside
  `__main__`, for the barrier. The module docstring says so on the same line.

### Self-introduced defects, disclosed

* **S-1.** The probe discovered itself as an entry point and recursively
  probed itself. About 540 disposable worktrees were created under `/tmp`
  before I stopped it. It wrote nothing outside those copies: the
  authoritative tree, the working tree and all three manifests held. Fixed in
  `acc8bb3`: a nested probe refuses to run. A test holds that.
* **S-2.** Stopping a run with `pkill -f` matched my own shell (exit 144), a
  repeat of the `GOAL-V2-002` slip. Later stops matched by an escaped pattern.
  No tree effect.
* **S-3.** Early in discovery I ran two tools CLIs by path in the
  authoritative checkout. Both failed at import and wrote nothing (verified
  with `git status`). Every later run was in a worktree.
* **S-4.** The first P10/P11 manifest text truncated the instrument identifier
  (the P10 instrument's number cut to two digits). I regenerated the manifests before they were registered. The
  barrier refused my own in-place rewrite of the new manifest, which confirms
  it protects references created after installation. The regeneration went
  through a shell `rm`.
* **S-5.** The first draft of W-4 said it was *"refused by `record()`"*. The
  probe tail shows `ProvenanceIncomplete` from `p12_execution_provenance`.
  Corrected.

## 22. Authority analysis

| Act | Authority |
|---|---|
| Barrier, integrity verifier, probe, manifests, index, test changes | `GOAL-V2-004` §7–§16, under `DEL-CFV2-CEO-001`, E0/E1 construction within the Goal (`IAM-04`) |
| Guard resolution tightening (N-2) | Brings the implementation into conformity with an existing Founder ruling. It **creates no rule and changes no decision**. The resolved set is unchanged |
| P10/P11 anchor choice | Implementation choice, stated as one. It confers nothing. The instruments remain the authority (`CERTIFICATION AUTHORITY ≠ IMPLEMENTATION ASSUMPTION`) |
| Register `§18` | Append-only status note, same form as `§16` |

**Not done:** no certification change, no P13, no Native Core change
(`native_core/` untouched), no roadmap or governance-model change, and no
`GOVERNANCE_INDEX.md` edit. F-4 was **not needed** for this Goal and remains
separately classified. `docs/program/AIOS_*` were not touched.

## 23. Evidence persisted

`GOAL-V2-004` act · this record · Register `§18` ·
`AIOS_P10_…MANIFEST_v1.0.json` · `AIOS_P11_…MANIFEST_v1.0.json` ·
`AIOS_CERTIFIED_EVIDENCE_MANIFEST_INDEX_v1.0.json` (sha256 `34f9673a…`) ·
`tools/__init__.py` · `tools/certified_write_barrier.py` ·
`tools/certified_write_barrier_site/sitecustomize.py` ·
`tools/certified_evidence_integrity.py` · `tools/certified_write_probe.py` ·
`tools/tests/test_certified_write_closure.py` (50 tests). Commits `67b405b`,
`acc8bb3`, and the commit carrying this record.

## 24. Re-discovery result

Run on the pushed commit `7e45d9d`, which carries this record (verify →
persist → **re-discover → verify again**) [OBS]:

| Question (Goal `§22`) | Result |
|---|---|
| New write paths? | None. 133 invocations over 11 + 50 + 1 + 13 entry points, 4 targeted runs and 4 suites. **0 certified writes**, 0 UNKNOWN, 0 half-writes, and no GUARDED run changed any file. Static: every write added since `ef89545` is either a guarded write into a disposable worktree or a test write into a temporary copy |
| New certified surfaces? | None. The guard still resolves `{10, 11, 12}` from the same three instruments, with 0 anomalies. No file under `docs/architecture/`, `native_core/` or `docs/program/` changed |
| Protection bypass? | Only the stated limits (§9), plus deliberate tampering with the barrier's in-process state by code that is itself resident. That is detection's case, not prevention's. M1 shows detection catching a write made with the barrier removed |
| New live/certified conflicts? | None. The three observation proofs still write only the live root (SAFE) |
| Existing consumers broke? | No. All four suites pass inside the re-discovery worktree (tools 1454, native_core 801, consumers 276, bounded_exception 29). The post-construction worktree run at `acc8bb3` had failed four tools tests only because this record was not yet committed, so the act and Register cited a missing file |
| New dependencies? | D-1…D-3 (§18). Nothing new at re-discovery |
| Integrity model coherent? | Yes. The mutation controls re-run on `7e45d9d` give the same results as §13 (M1 MODIFIED, M2 refused, M3 all four findings, M4a–c faults), and the authoritative tree held before and after |

## 25. Founder decisions required

None for this Target. The standing items are unchanged: Founder review of
`GOAL-V2-002`…`004`, `FD-2`, P13 review, and F-4 authority.

## 26. Whether Target is achieved

**Yes.** Every criterion is supported by the evidence cited:

| Criterion | Evidence |
|---|---|
| T4-01 entry points discovered or classified | §5: content discovery, 133 runs, 0 UNKNOWN |
| T4-02 write paths identified | §6: W-1…W-9, the static writer scan, subprocess use |
| T4-03 live-only or refused before first certified write | §5 classification, §8, §24 |
| T4-04 no half-write | §5 and §24: no GUARDED run changed any file. The three `B-03` half-writers are now refused first |
| T4-05 P10 integrity | §2, §10 |
| T4-06 P11 integrity | §3, §11 |
| T4-07 P12 mechanism still valid | §4, §12 |
| T4-08 detects modification, addition, deletion and drift | §13 M3/M4, unit controls, and `UNREADABLE` |
| T4-09 mutation testing effective | §13 (twice: `67b405b` and `7e45d9d`) |
| T4-10 authoritative evidence intact | §15, before and after every run |
| T4-11 live/certified separation valid | §16 |
| T4-12 historical records preserved | §17 |
| T4-13 full regression passes | §14 (two clean runs) and §24 (a third, in the worktree) |
| T4-14 post-construction re-discovery complete | §24 |
| T4-15 evidence persisted | §23, pushed |

## 27. Whether authorized construction remains

**None within `GOAL-V2-004`.** No actionable construction item remains inside
this Goal's envelope. Stated residuals (§9, §18) are governed, not open write
paths. Work outside the envelope is not absorbed (Goal `§20`). Any next
construction needs its own Goal or frontier determination (`IAM-04`).

## 28. Whether V2 exhaustion applies

**Not declared.** The Goal (`§26`) forbids declaring exhaustion because the
known writers are fixed or the tests pass. What this record establishes is
narrower: under `GOAL-V2-004`, discovery, classification, authorized work,
verification, evidence and re-discovery found no further item. V2 exhaustion
as a program-level condition is not assessed here. The standing Founder
matters (§20, §25) remain.
