# GOAL-V2-002 — P12 Certification & Evidence Integrity — Execution Record v1.0

| Field | Value |
|---|---|
| **Goal** | `GOAL-V2-002` (`acts/GOAL-V2-002-P12-CERTIFICATION-AND-EVIDENCE-INTEGRITY.md`) — *"RESTORE AND ENFORCE THE INTEGRITY OF P12 CERTIFICATION STATE AND ITS ASSOCIATED CERTIFIED EVIDENCE."* |
| **Executor** | Claude Code — AIOS Co-Founder + Delegated CEO (`DEL-CFV2-CEO-001`) |
| **Control surface** | `AIOS-CEO-AUTHORITY-ESCALATION-MATRIX-V2-001` |
| **Date** | 2026-09-24 |
| **Target status** | **ACHIEVED** — T2-01 … T2-10 all met (§20) |

Labels: **[OBS]** observed or measured in this execution, **[VER]** verified by
a test or check that can fail, **[INF]** inference, **[REC]** recommendation.
The starting findings (`B-01`, `B-02`, `H-1`) were **re-verified from source**
before any change (Goal `§4`, `§6`). They were not taken from the prior
baseline.

---

## 1. Target status

**ACHIEVED.** P12's certification is now represented and enforced consistently
across the surfaces below. Certified evidence is fixed by content, verified on
every suite run, and restored where it had drifted. The one process that was
rewriting it (the corpus-health run, via the tools suite) can no longer reach
it.

This is **not** P12 complete, AIOS complete, system integrity verified, final
architecture, or Founder acceptance (Goal `§20`).

## 2. Current P12 certification state — one traceable answer

**P12 is certified**, by `FD-P12-006`. Each surface in the chain below agrees
with that decision, and each carries its own provenance:

| Link | Surface | State | Label |
|---|---|---|---|
| Founder decision | `acts/FD-P12-006-…md`, decision field: *"FOUNDER DECISION:"* / *"P12 CERTIFICATION = CERTIFY"* | Certified | [OBS] |
| Registered governance | Decision Register `§15` entry `FD-P12-006`; `§16` status note | Registered | [OBS] |
| Enforcement reader | `p12_certified_evidence_guard.certified_phases()` → **{10, 11, 12}**; resolves against `§15`; 0 anomalies | Recognized | [VER] |
| Phase reader | `p12_phase_authorization.certifications()` → P12 by `FD-P12-006`. `current_states()` sets the `§37` snapshot's FALSE values aside as `superseded_by_certification` | Recognized | [VER] |
| Self-model | `authority().phase_authorization`: `certification.phases.P12` present. `states.P12.dimensions` = `{AUTHORIZED: true}` and no longer asserts `CERTIFIED: false` | Consistent | [VER] |
| Evidence control | `AIOS_P12_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json` names `FD-P12-006` and commit `6968c6e` | Consistent | [VER] |

**One intentional difference, kept and justified.** `phase_states()` still
reads the `§37` block exactly as written, including `P12 CERTIFIED = FALSE`.
That block is a Founder-issued **entry snapshot** and is historical truth. It is
preserved, not rewritten (Goal `§18`). The current view sets its superseded
values aside and names the instrument that supersedes them. The guard and the
phase reader are checked for agreement by a test.

## 3. Current evidence state

| | State | Label |
|---|---|---|
| What certified P12 evidence is | Every file under `docs/architecture/p12/` at commit **`6968c6e`**, which the certification handoff names *"final measured certified state"* (`handoff §1.2`). **121 files** | [OBS] |
| Integrity | **121 / 121 intact**, compared with the manifest by sha256 | [VER] |
| Additions since certification | 1: the certification handoff record (`e5ac0f5`). It is a record, not evidence, and is listed so that nothing else can hide in the root | [VER] |
| Prevention | The guard refuses writes into `docs/architecture/p12/` and into `FD-P12-006` itself | [VER] |
| Detection | A suite test fails on any modified, missing or unexpected file | [VER] |
| Provenance of the manifest | Rebuilt from git history by `from_commit` and compared with the committed copy on every run. It is not trusted as written | [VER] |

**Who may do what with certified P12 evidence:**

| Action | Permitted | Enforced by |
|---|---|---|
| Read (verifiers, self-model, auditors) | Yes | — |
| Write, overwrite or add under `docs/architecture/p12/` | **No** | guard (routed writers) · manifest test (all writers) |
| Legitimate regeneration | Not by rewriting. New evidence goes to a new, uncertified location; the certified bytes stay | guard message; this record |

## 4. Current runtime-observation state

**Classification of the observed rewriting (`B-02`):** an
**EVIDENCE-LIFECYCLE DEFECT** plus a **BUG** (Goal `§9`) [VER]:

- **Lifecycle defect.** An observation is a *live projection* (*"these files
  state what was last observed"*, commit `d18bac4`). It was published into the
  phase directory that `FD-P12-006` later certified. Certification froze a
  surface whose purpose is to change. No record stated which files under the P12
  root were frozen evidence and which were live.
- **Bug (`D.1`).** `aios_corpus_health_run.run()` parameterised its stores but
  not its observation root. The tools suite drives `run()`, so every suite run
  wrote into the resident root.

**Resulting state:**

| Root | Role | Writable |
|---|---|---|
| `docs/operations/runtime-observations/` | **Live** observations. Outside every phase directory, so no future phase certification can freeze them | Yes. The default `publish` root |
| `docs/architecture/p12/runtime-observations/` | P12's observations **as certified** (origin `certified-p12`) | No. `publish` routes through the guard |

`observations()` on the default root reads both. A live record supersedes a
certified one for the same id, and each record carries its `origin`. The suite
now passes an isolated observation root, and the live root stayed **empty**
across two consecutive full suite runs (§8).

## 5. Current self-model state

| Question | Before | After |
|---|---|---|
| Phase state P12 | `CERTIFIED: false` (and five other FALSE values from the entry snapshot) | `dimensions: {AUTHORIZED: true}`; the FALSE values are in `superseded_by_certification`, by `FD-P12-006`. `certification.phases` lists P10, P11 and P12 |
| P13 | `AUTHORIZED: false` | unchanged |
| *"What is running?"* | read the P12 root only | reads live + certified, with origin; unchanged answer (nothing live) |
| Independent verifier (`p12_phase_authorization_verifier`) for P12 and P13 | — | 6 / 6 SATISFIED each |

No governance decision was manufactured. The self-model reads `FD-P12-006`. It
does not restate it (Goal `§10`, `§11`).

## 6. Changes made

| # | Change | Files |
|---|---|---|
| C-1 | Guard recognizes the decision-field certification form, anchored to the *"FOUNDER DECISION:"* label so the conditional *"P12 CERTIFIED = YES"* in `§21` is not read as a decision | `tools/p12_certified_evidence_guard.py` |
| C-2 | Observation lifecycle split: live root, certified root, merged read with origin, guarded publish | `tools/p12_runtime_observation.py`; `docs/operations/` (new) |
| C-3 | `D.1` fixed: observation root is a parameter of `run()`; `run()` refuses before writing if any target store is certified | `aios_corpus_health_run.py`; `tools/tests/test_p12_knowledge_admission.py` |
| C-4 | Manifest writes guarded; 12 temporary-directory writes routed through the guard so the per-call-site coverage check holds | `tools/p12_execution_provenance.py`; `tools/p12_negative_control_verification.py` |
| C-5 | Certified evidence manifest and verifier (detection, whatever the writer), with a negative control | `tools/p12_certified_evidence_manifest.py`; `docs/governance/AIOS_P12_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json` |
| C-6 | Phase reader: `certifications()`, `current_states()`; self-model uses them | `tools/p12_phase_authorization.py`; `tools/p12_self_model.py` |
| C-7 | The descriptive read paths name the live observation root. Both fields must be one resolvable path, and the readers behind them read live and certified | `tools/p12_operational_state.py`; `tools/p12_integration_graph.py`; `docs/operations/runtime-observations/.gitkeep` |
| C-8 | Evidence restored: 2 observation files returned to their certified bytes | `docs/architecture/p12/runtime-observations/aios-corpus-health{,-runtime}.observation.json` |
| C-9 | Tests: 6 stale pre-certification oracles corrected with their reasons recorded; 23 new tests | `tools/tests/test_p12_certified_evidence_guard.py`; `tools/tests/test_p12_certification_integrity.py` (new) |
| C-10 | Recording: Goal persisted verbatim; Register `§16` status note; this record | `acts/GOAL-V2-002-…md`; Register; this file |

## 7. Authority basis

| Change | Authority | State |
|---|---|---|
| C-1 … C-7, C-9 | A06 Engineering, A07 cross-phase repair, A11 verification; Goal `§13` | AUTHORIZED |
| C-2 root location | A05 bounded architecture: a technical storage location. It touches no Domain Model entity, cross-Platform-Division structure or Constitution clause (`REG-CFV2-001` `C-1`…`C-4`) | AUTHORIZED WITH BOUNDARY (E1) |
| C-8 restoration | A07, A12. It restores certified evidence to the state the certification names. The later bytes and their commits remain in history, and nothing historical is rewritten | AUTHORIZED WITH BOUNDARY (E1) |
| C-10 | A12 | AUTHORIZED |
| Any change to `FD-P12-006`, the certification, or what P12 certifies | — | **Not done. Not needed** |

**The stale-test corrections are not *"modifying a test to preserve
certification"*** (`FD-P12-006`, *"Do not modify the test merely to preserve
certification"*). They run the other way. The old oracles asserted that P12 was
**not** certified, and they could keep passing only while the guard failed to
read the decision.

## 8. Verification performed

| Check | Result |
|---|---|
| Full `tools/tests`, **two consecutive runs** | 1404 OK · 1404 OK (§19) |
| Manifest after each run | holds · holds (§19) |
| Files the suite changed after each run | none · none (§19) |
| Live observation root after each run | empty · empty (§19) |
| `native_core` · `consumers` · `tools/bounded_exception` | 801 OK (1 expected failure) · 276 OK · 29 OK |
| Mutation: remove the decision-field form | 7 tests fail. **Nothing written** (manifest holds, no additions) |
| Mutation: point the live root back into P12 | 1 test fails |
| Negative control for the manifest | intact → holds; changed byte → MODIFIED; removed file → MISSING; unreadable manifest → raises |
| Phase verifier, P12 and P13 | 6 / 6 SATISFIED |
| Stale-state audit | 0 |
| Citation audit | 0 errors (§19) |

## 9. Regression results

No existing certified evidence was invalidated: 121/121 intact [VER]. The P10
and P11 protections are unchanged, and their tests pass. The P13 state is
unchanged. The self-model overstates nothing: it adds a certification that a
Founder instrument states, and asserts no dimension the instrument does not
state. **Evidence controls are stronger, not weaker.** P12 gained prevention,
detection was added, and the certifying instrument is itself protected.

## 10. Evidence persisted

This record · the manifest · the Goal record · Register `§16` · the tests above
· `docs/operations/README.md`.

## 11. Historical anomalies preserved

| Anomaly | Treatment |
|---|---|
| `7f6120c` (2026-09-18) and `d18bac4` (2026-09-19) committed post-certification observation rewrites into the certified root. **`d18bac4` was mine**, made in a prior execution, when I judged the observation files to be live state and committed the refresh with a disclosure | Certified bytes restored. Both commits and their bytes remain in history, and they are named here and in Register `§16` |
| `§37` entry snapshot says `P12 CERTIFIED = FALSE` | Preserved and still read verbatim by `phase_states()`; set aside, not deleted, in the current view |
| Handoff finding `H-1` (row 14, *"no machine-readable register reflects the certification"*) | Resolved in the readers. The handoff record is certified-root content and is **not edited** |
| `§15`'s *"does not yet recognize"* note | Kept; superseded by Register `§16` |
| `FD-P12-003`'s date | Untouched |

## 12. Re-discovery findings

| # | Finding | Class | Disposition |
|---|---|---|---|
| RD-1 | The static writer-coverage check sees only `write_text` / `write_bytes`. Stores written through Native Core backends (trace, knowledge, memory) are invisible to it | Limitation | **Mitigated:** the manifest test catches any modification or addition, whatever the write API |
| RD-2 | Resident P12 proof scripts (`p12_w4_integrated_execution`, `p12_w3_governance_escalation`, `p12_w3_resident_wiring_proof`, and the trace/workflow proofs) still default their trace, delegation and governance stores into the certified root | DEPENDENCY | Not run by the suite. If run, `record()` refuses the manifest write, and the suite reports any other write. They could **half-write** before refusing (with `D.2`, non-atomic chain). See W-1 |
| RD-3 | New live executions of the `§28` chain now have no permitted store: manifests are refused in the certified root, and no live root exists for the chain's stores | DEPENDENCY | W-1 |
| RD-4 | The certified-evidence guard now protects `FD-P12-006`. The Register, which the resolution depends on, is not protected: the forgery residual (`FD-P12-004 §5`) | Known, unchanged | Recorded; `Freeze §10` anchor required, as before |
| RD-5 | P10 appears in `certifications()` but not in `states`, because the `§37` block does not state P10 | Intentional | Documented |
| RD-6 | Two of my own mutation runs wrote into certified evidence (X-3, X-4). **The new manifest control caught both** | Self-introduced defect | Restored; tests hardened (§19.1) |

## 13. Remaining work

| # | Work | State | Authority | Dependency |
|---|---|---|---|---|
| W-1 | Give the `§28` execution chain and the knowledge-admission path live stores outside the certified root (trace, execution provenance, delegation, governance-join, knowledge). Readers must read certified + live, as observations now do. Add pre-write root checks to the resident proof scripts | PARTIAL / DEPENDENCY | AUTHORIZED WITH BOUNDARY (A05 E1, A06) | Needed only when a Goal requires new live executions |
| W-2 | `D.2`: make the `§28` chain atomic, or pre-check all roots before the first write | Open | AUTHORIZED | W-1 |
| W-3 | Extend the static writer check beyond `write_text` / `write_bytes` | Optional | AUTHORIZED | — |
| W-4 | From the prior baseline: `F-3` (the `D.2` part merges into W-2) and `F-4` (index and catalogue sync). **`F-1` and `F-2` are closed by this Goal** | Open | AUTHORIZED | — |

## 14. Blocked work

None inside this Target. Outside it, unchanged from the baseline: P13 (Founder),
the vocabulary rows (Domain Model), cross-PD interfaces (Architect).

## 15. New dependencies

RD-2 and RD-3 → W-1. A live `§28` execution needs W-1 before it can run
post-certification without being refused.

## 16. New conflicts

None. The only difference between surfaces (snapshot vs current state) is
intentional, documented and tested (§2).

## 17. Founder decisions required

**None for this Target.** Carried from earlier returns: FD-2, the P13 disposition
and escalation `23f315ba9f504272`.

## 18. CEO recommendation

[REC] **APPROVE** this Target. Issue W-1 as a Goal only when live post-P12
execution is needed; until then the fail-closed state is correct. Otherwise the
next authorized work is `F-4` (index and catalogue synchronization).

## 19. Verification results (measured on the final tree)

| Check | Pass 1 | Pass 2 |
|---|---|---|
| `tools/tests` | **1404 run · OK · 1 skipped** | **1404 run · OK · 1 skipped** |
| Certified evidence (manifest) | **holds** · 121 intact · 0 modified · 0 missing · 1 known addition | **holds** · 121 intact · 0 modified · 0 missing · 1 known addition |
| Files the suite changed (`git diff --stat` against the staged tree, `docs/architecture` + `docs/operations`) | **none** | **none** |
| Live observation root after the run | empty (`.gitkeep` only) | empty (`.gitkeep` only) |

**This is the first time a full suite run has left the working tree unchanged.**
Before this Goal, every run rewrote two certified P12 files. Two consecutive
runs are the repeat evidence Goal `§16` asks for: the mutation no longer occurs.

| Other checks on the final tree | Result |
|---|---|
| `native_core` · `consumers` · `tools/bounded_exception` | 801 OK (1 expected failure) · 276 OK · 29 OK |
| Citation audit | 0 errors · 89 warnings (unchanged) |
| Stale-state audit | 0 |

The only changes after these runs are this table and the §19.1 rows for X-4 and
X-6, which record defects the runs themselves exposed. No test reads either.

### 19.1 Self-introduced defects

| # | Defect | Found by | Correction |
|---|---|---|---|
| X-1 | `d18bac4` (prior execution) committed a test-caused rewrite into what was already certified evidence | This Goal's manifest | Restored (C-8); disclosed (§11) |
| X-2 | The first mutation run of this Goal left the guard tests able to write when the guard is broken | Manifest test, in the same session | Tests now assert protection before any write attempt |
| X-3 | That mutation run wrote `runtime-observations/probe.observation.json` into certified evidence | Manifest test (addition) | Removed; never committed |
| X-4 | The same run appended to the certified trace store `trace-stores/aios-corpus-health/trace`, and published two observations into the new live root | Manifest test (modified); the post-run live-root check (the two files carried that run's pid and timestamp) | Trace restored from `6968c6e`; live files removed; none committed. Re-running the mutation afterwards: 7 failures, **nothing written**. Each candidate test module run alone writes 0 files to the live root |
| X-5 | An in-flight suite run was stopped with `pkill`, whose pattern also matched its own shell | Exit 144 | Restoration re-run separately; the suite relaunched on the corrected tree |
| X-6 | Two edits broke existing checks. The manifest built a git revision spec as an f-string of the shape `path:line`, which the coherence check reads as a citation locator. The integration graph's evidence field was given a two-path description, which its dangling-reference check reads as one unresolvable path | Full suite, pass 1 | Spec built by concatenation. The evidence field names the live root, a single real path, and the graph still reads both roots |

## 20. Target completion criteria

| # | Criterion | Met | Evidence |
|---|---|---|---|
| T2-01 | Authoritative certification state identified | ✅ | §2 |
| T2-02 | Readers resolve it | ✅ | guard {10, 11, 12}; `certifications()`; tests |
| T2-03 | Self-model does not contradict it | ✅ | §5; verifier 6/6 |
| T2-04 | Explicit, correct protection boundary | ✅ | §3; guard + manifest |
| T2-05 | Normal verification no longer corrupts it | ✅ | §19: two consecutive runs, 0 changes |
| T2-06 | Tests and guards exercise the behaviour | ✅ | 23 new tests; 2 mutations; negative control |
| T2-07 | Historical records preserved | ✅ | §11 |
| T2-08 | Changes verified and evidenced | ✅ | §8, §19 |
| T2-09 | Re-discovery completed | ✅ | §12 |
| T2-10 | Remaining work classified | ✅ | §13 – §15 |

**Authorized actionable construction remains** (W-1 … W-4), so exhaustion is
not declared.
