# AIOS P13 — Certification Readiness Package v1.0

| Field | Value |
|---|---|
| **Instrument** | `FDR-6` (Decision Register `§26`; act content sha256 `473f6e33…`), `§15` step 19 and `§17` |
| **Prepared by** | Claude Code — AIOS Co-Founder + Delegated CEO · 2026-09-25 |
| **Nature** | the readiness package the Founder Certification Decision follows. **It certifies nothing and decides nothing. It creates no certification or closure record, and it is not a draft of the Certification Decision** |
| **Revised** | 2026-09-25 under `ACT-CC-P13-CERT-GATE-002` (see §G) |
| **Commits** | `4d12c4c` persist and register `FDR-6` · `0eb2900` `CR-3` · `8114f9b` `CR-4` · `edd7219` `CR-1`/`CR-2` · `2ffb175` `FDQ-4`/`FDQ-5` records |

## A. Founder Decision Integrity

| | |
|---|---|
| Identifier | `FDR-6`, as the instrument states it twice (*"Decision ID"*, *"Decision Record ID"*). It is the next number in the registered `FDR` series |
| Persisted text | `docs/governance/acts/FDR-6-P13-CERTIFICATION-GATE-FOUNDER-DECISION.md`. The Founder's message is verbatim in one fenced block. It was checked equal to the message as received |
| Decision hash | content sha256 `473f6e33a3eb82d1ac0606bcdff5df39a700d1b34bed9d59e384a0c8dc47862b`, over the fenced text. The file's own sha256 is `8d1ef837…` |
| Decision Register | `§26` (2026-09-25) |
| Resolution | `tools/authority_citation.refusal("FDR-6", <act>, "FDR-6")` returns no refusal. The governance index holds one `FDR-6` record, from the Register. The phase reader resolves the act against the Register (identity `FDR-6-P13-CERTIFICATION-GATE-FOUNDER-DECISION`), and so does the independent verifier, by the act's path |
| Disclosed at persistence | an unissued `FDR-6` label in `GOAL-V2-005` `§12` (*corpus residency*, `GAP-0006`), not answered by this decision. The instrument's header reads *"PENDING FOUNDER AUTHORIZATION"*, but its signature block says *"APPROVED FOR PERSISTENCE AND BOUNDED EXECUTION"*. The signature block governs, as with the P12 decision's stale header |
| Certification statement in `FDR-6` | **none.** The guard's three recognised forms match nothing in the act. Certified phases are still `{10, 11, 12}` |

**Authority projection** (`tools/p13/authority.authority_dimensions`, recomputed on `2ffb175`):

| Dimension | Before `CR-3` (step 3) | Now |
|---|---|---|
| Phase authorization | NOT AUTHORIZED. The machinery could not yet represent `FDQ-1` | **AUTHORIZED**. Source: `FDR-6` `§19 FOUNDER DECISION`. The `§37` value `FALSE` is kept as superseded |
| Construction authorization | AUTHORIZED, bounded to Blueprint §10 IN (`P13-018`) | unchanged |
| Operational envelope | EVIDENCE-ONLY (`P13-ENV-01`) | unchanged |
| State-changing authority | NONE; `P13-ENV-02` retired (`FDR-4`) | unchanged |
| Certification authority | NOT GRANTED | unchanged |

## B. FDQ Disposition Matrix

| Question | Founder disposition | Result | Evidence |
|---|---|---|---|
| FDQ-1 — Phase Authorization | AUTHORIZE PHASE 13 | **AUTHORIZED** | `p12_phase_authorization.current_states()`: P13 `AUTHORIZED = TRUE`, cited to `FDR-6` `§19`. The verifier independently finds 6/6 checks satisfied |
| FDQ-2 — Fresh Live Verification | NOT REQUIRED | **NO NEW LIVE PROOF REQUIRED** | no state-changing execution took place. `S-OPS-01` is still sha256 `e2781df3…`, and `docs/operations/p13/` has no new record |
| FDQ-3 — Blueprint §16 | AUTHORIZE APPEND-ONLY RECONCILIATION | **AUTHORIZED, EXECUTED** | `§16` appended at `8114f9b`. The §0–§15 prefix (24,949 bytes) is still sha256 `6f022d89…` |
| FDQ-4 — Residual Frontier | ADOPT CLASSIFICATION | **NON-BLOCKING / PRESERVED** | P13-017 `§9`. No classification changed and nothing was resolved |
| FDQ-5 — Evidence Protection | ADOPT `docs/architecture/p13/` | **CERTIFIED ROOT DEFINED** | the P13 manifest lists the root's actual contents: 1 file |

## C. Construction Matrix

| CR | Condition | Executed? | Evidence |
|---|---|---|---|
| CR-1 | always | **YES** | `AIOS_P13_CERTIFICATION_MANIFEST_v1.0.json` · sha256 `127b97fd…` · PREPARED — NOT CERTIFIED · at `8114f9b` · Decision Register `§27` |
| CR-2 | always | **YES** | `tools/certified_evidence_integrity.py` (prepared manifests, index supplements) · `tools/tests/test_p13_certification_gate.py` · updated pins in five test modules |
| CR-3 | FDQ-1-A | **YES** | `authorizations()` and the supersession in `current_states()` (`tools/p12_phase_authorization.py`). Independent recognition in the verifier. The `§49` control is re-grounded |
| CR-4 | FDQ-3 | **YES** | Blueprint `§16` |
| CR-5 | — | **NO**, not authorized | `P13-ENV-02` stays retired; there was no S-OPS execution |

**How each was built, and what was chosen:**

* **CR-3: one reader added, no new instrument model.** `FDR-6` `§11` allows a
  new mechanism only if the existing one cannot represent the decision. It
  cannot, for two reasons. `decision_instrument()` reads exactly one
  `FINAL STATE TRANSITION` block and refuses a second, correctly. And
  `certifications()` never supersedes `AUTHORIZED`. So `authorizations()`
  mirrors `certifications()`. It uses the same Register resolution rule
  (`FD-P12-004`) and the same kind of supersession. The `§37` snapshot is
  never rewritten: `phase_states()` and `state_of()` still return
  `P13 AUTHORIZED = FALSE` as written. An authorization is read only from
  a line that is exactly `AUTHORIZE PHASE <n>`, inside a section headed
  exactly `FOUNDER DECISION`, in a Register-resolving act.
* **CR-3 has a cross-phase consequence, stated rather than hidden.** P12's
  `§49` control "unauthorized P13 authorization" and one `§18` verifier
  control assumed P13 was unauthorized. The Founder changed that. Left alone,
  the `§49` control would have reported the Founder's own authorization as an
  unrefused unauthorized claim.
  * The `§49` control now first verifies that the `TRUE` is the Founder's.
    It then plants an **unregistered** authorization in a sandbox and requires
    it to be rejected. `§49` stays 13/13, and the new branch can still be
    driven to `ACCEPTED`, which a test shows.
  * The `§18` verifier control now forges the opposite of the live state.
  * No P12 certified evidence changed.
  * The P12 `§46` phase-verification matrix still names the `§37` instrument
    for P13. That is where the snapshot states P13, and it is still true.
    It was left unchanged.
* **CR-1: prepared, not protecting.** The certified-write barrier protects
  every file matching `AIOS_*CERTIFIED_EVIDENCE_MANIFEST*.json`, and every
  root those files name. A P13 manifest with that name would have protected
  `docs/architecture/p13/` at once, which is a certification in effect. The
  manifest is therefore named `AIOS_P13_CERTIFICATION_MANIFEST_v1.0.json`, and
  a test holds that it stays outside the pattern. The registered P10–P12
  index (sha256 `34f9673a…`) is unchanged. Promotion at certification is an
  **index supplement**, a new file, and never a rewrite of that index.
* **Order, disclosed.** `§15` lists CR-1 before CR-4. The manifest was
  built after the `§16` append, because `FDQ-5` requires *"the actual contents
  of the certified root"*, and `§16` is part of them.

## D. Certification Integrity

| Check | Result |
|---|---|
| P13 certified root | `docs/architecture/p13/`: one file, `AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md` (sha256 `0b13e300…`). **Not protected**: `barrier.refuses` is false, and the root is in neither the guard's nor the barrier's roots |
| P13 manifest | present. It is PREPARED — NOT CERTIFIED, has `certifying_instrument` and `certified_commit` null, and is rebuilt identically from `8114f9b` by `from_commit` |
| Manifest hash | `127b97fd9dcd8aaa14f2f94039a86655fe5b8f21a77b2c1e349a4701a27d259d`, recorded in Decision Register `§27`. Detection requires it there |
| Certification guard | `certified_phases()` = `{10, 11, 12}`. `certification_anomalies()` = none. Protected roots and instruments unchanged |
| Certified-phase detection | `certified_evidence_integrity.verify()` **holds**: P10 36, P11 58, P12 121 intact; prepared P13 1 intact; no faults |
| Premature-certification protection | tested in disposable copies. An unregistered P13 certification is rejected. A registered one makes the guard protect `docs/architecture/p13/`, and detection then **faults** until the manifest is promoted. Promotion leaves the registered index byte-identical. Root drift, added supplementary evidence and a manifest claiming certification are all faults |
| Test suite | on the tree of `2ffb175`: `tools/tests` 1671 tests OK (1 skipped); `native_core` 801 OK (1 expected failure); `consumers` 276 OK; `tools/bounded_exception/tests` 29 OK |
| Mutation protections | 19 of 19 injected defects were caught (see below) |
| Tree cleanliness | `git status` clean at `2ffb175` after the suites, the probe and the re-discovery cycle |
| No unauthorized writes | `python -m tools.certified_write_probe --commit 2ffb175 --jobs 4`: 142 entry points (113 non-writing, 12 guarded, 4 safe, 13 retired or historical), **0 certified writes**, holds. `docs/architecture/p13/` is not among the probe's certified prefixes, which is correct before certification. `S-OPS-01` is unchanged. `docs/operations/` and every certified root are unchanged since `58e197e`. The re-discovery cycle wrote only to a scratch root |

**Mutations (each caught by at least one test):**

* the reader:
  * Register resolution removed;
  * the form matched anywhere in a line;
  * any section read, not only `FOUNDER DECISION`;
  * ambiguous authorizations applied;
  * the snapshot value dropped rather than kept as superseded;
  * the authorization also marking `CERTIFIED`;
* the verifier:
  * Register path check removed;
  * authorizing provenance always accepted;
* the control:
  * sandbox leg skipped;
  * an unverified `TRUE` refused;
* integrity:
  * prepared drift ignored;
  * a certified-but-only-prepared phase accepted;
  * the certification claim not checked;
  * phase authorization not checked;
  * the prepared sha not checked against the Register;
  * the supplement sha not checked;
  * a phase indexed twice;
  * the prepared root not pinned to the guard's root;
  * supplements not read.

**Defects introduced during this execution, disclosed:**

1. With the Register rule disabled, the first version of the sandbox leg in
   the `§49` control raised an error instead of reporting `ACCEPTED`. A new
   test caught it before commit, and it now fails visibly.
2. One existing test forged `AUTHORIZED = True` as the wrong state. That is
   now the true state, so the forgery now uses the opposite of the live one.
3. Mutation V2 (authorizing provenance always accepted) first survived. A
   test for a claim that reads more than the decision states was added.
4. The first I2 mutation was malformed and "caught" only by a syntax error.
   It was re-run correctly and caught.

## E. Certification Blocker Matrix

Every item is classified. None is inferred resolved. **UNKNOWN: none.**

| # | Item | Classification | Basis |
|---|---|---|---|
| 1 | Founder Certification Decision | **FOUNDER DECISION REQUIRED** | certification is Founder-reserved (`FDR-6` `§1`, `§18`). Nothing here generates it |
| 2 | Phase authorization | **RESOLVED** | `FDR-6` `FDQ-1`, represented under `CR-3`; independently verified |
| 3 | Exit contract | **RESOLVED** | `FDR-5` `FD-E` |
| 4 | Fresh live verification | **RESOLVED**: not required | `FDQ-2` |
| 5 | Certified root | **RESOLVED** | `FDQ-5`: `docs/architecture/p13/` |
| 6 | P13 manifest | **RESOLVED**: prepared, registered, holding | `CR-1`, Register `§27`. Any change to the root before certification must be followed by a new manifest and Register entry, or detection faults |
| 7 | Integrity and test reconciliation | **RESOLVED** | `CR-2`; suites and mutations above |
| 8 | Blueprint currency | **RESOLVED** | `CR-4`, `§16` |
| 9 | Residual frontier (Q38, Q39, Q91 frontier; Q23 unknown; `GAP-0017`/`0018`; the E13-07 register) | **NON-BLOCKING**, not resolved | `FDQ-4`; P13-017 `§9` |
| 10 | E13-05 escalate branch and consequence mismatch (test-proven) | **NON-BLOCKING** | `FDQ-2`'s basis names both as proven through test evidence. They stay test-proven |
| 11 | E13-03 test-only rules (`R-MISMATCH`, `R-AUTHORITY`, `R-GAP`) and the E13-06 test-only evolution-proposal path | **FOUNDER DECISION REQUIRED** | accepted for exit by `FDR-5`. `FDQ-2` carries them by their actual class, and no decision yet accepts them for certification |
| 12 | Blueprint layer status: §0 marks §3–§11 a *CEO architecture decision*. `P13-018` `D-1` approved construction of §10 IN only | **FOUNDER DECISION REQUIRED** | handoff §C.5; not addressed by `FDR-6` |
| 13 | S-OPS residue in `tools/p13/` (the `s_ops` source, two criteria, two action types) | **NON-BLOCKING** | outside the certified root (`FDQ-5`). S-OPS is historical only (`§14`), and no envelope permits the actions. Retiring them would be construction, which nothing authorizes |
| 14 | Operation after certification | **NON-BLOCKING** | `FDR-6` `§16` expects `P13-ENV-01` ACTIVE / EVIDENCE-ONLY. It continues as it is |
| 15 | Governance items outside P13: `FD-2`, `AD-P13-001` (Architect-reserved), `AD-P13-002`, F-4, the four OPEN escalations, `GAP-0006` corpus residency | **FOUNDER DECISION REQUIRED**, to confirm them outside the certification of P13 | handoff §C.11; not addressed by `FDR-6`. P13 does not rely on any of them |
| 16 | Guard recognition of a P13 certification | **RESOLVED** | the guard's default root is `docs/architecture/p13`. A resolving certification is recognised and protects it (tested in a disposable copy) |
| 17 | Promotion of the manifest after a certification | **CONSTRUCTION REQUIRED**, but only after a Founder Certification Decision, and not before it | create the certified manifest and an index supplement, and register both hashes. The machinery supports this and a test shows it; until then detection faults |
| 18 | Phase 13 closure | **NON-BLOCKING** to certification | a separate gate. **NOT GRANTED** |
| 19 | Roadmap endpoint | **RESOLVED** | the Master Roadmap (`AIOS_MASTER_ROADMAP_CONSOLIDATED_v1.0.md` §4) establishes Phases 0–13. P13 is the final phase currently established. The phase model holds P11–P13 and authorizations hold P13 only, so no phase beyond P13 exists there. Certification of P13 depends on no later phase |
| 20 | `P13-ENV-02` | **RESOLVED**: retired | `FDR-4` `FD-B`; `CR-5` |

**What the machinery recognises as a certification.** This describes the
machinery and prescribes no decision. The guard reads certification only from
an act in `docs/governance/acts/` that the Decision Register resolves. It
recognises three statement forms, set out in
`tools/p12_certified_evidence_guard.py` (`_CERTIFIES`). A decision in any
other form, or one the Register does not record, is not recognised.

## E′. Re-discovery (step 18)

One P13 cycle ran through `tools.p13.cycle.run_cycle`. It read the real
tree, and its cycle record went to a scratch root, not
`docs/operations/p13/`, so no live record was added. What it observed:

* `phase_authorization`: P13 authorized under `FDR-6`, with the `§37` value
  kept as superseded;
* certification `{P10, P11, P12}`;
* `integrity.holds` true;
* envelopes `[P13-ENV-01]`, no anomalies.

It executed `verify.ecosystem_relationships` under `P13-ENV-01`. The other two
verify actions were refused by the one-action-per-cycle bound (Blueprint
§3.2). `CR-RECONCILIATION` and `CR-P13-EVIDENCE` read UNKNOWN only because the
scratch root holds no earlier evidence. The eight other criteria passed.
`S-OPS-01` is still sha256 `e2781df3…`.

## F. Final State

```text
P13 MASTER PROGRAM AUTHORIZATION = TRUE              (FDR-6 FDQ-1; CR-3)
P13 EXIT CONTRACT               = SATISFIED          (FDR-5)
P13 CERTIFICATION               = NOT GRANTED
P13 PHASE CLOSURE               = NOT GRANTED
ROADMAP                         = P0–P13   (P13 = final currently established phase)
P13-ENV-01                      = ACTIVE / EVIDENCE-ONLY
P13-ENV-02                      = RETIRED / REVOKED
S-OPS                           = HISTORICAL EVIDENCE ONLY
CERTIFIED ROOT                  = docs/architecture/p13/   (defined; not yet protected)
P13 MANIFEST                    = PRESENT                  (prepared; sha256 127b97fd…)
CERTIFICATION GUARD             = INTEGRITY-PROTECTED      (certified phases {10, 11, 12})
RESIDUAL FRONTIER               = PRESERVED / CLASSIFIED ≠ SOLVED
FRESH LIVE VERIFICATION         = NOT REQUIRED
BLUEPRINT §16                   = APPENDED
BLUEPRINT §0–§15                = PRESERVED
```

**P13 CERTIFICATION GATE PREPARED. FOUNDER CERTIFICATION DECISION REQUIRED.**

```text
P13 CERTIFICATION READINESS PACKAGE  ─── HARD STOP ───▶  FOUNDER CERTIFICATION DECISION  ▶  certification only if the Founder explicitly certifies
```

## G. Revision under `ACT-CC-P13-CERT-GATE-002` (2026-09-25)

`ACT-CC-P13-CERT-GATE-002` reconciles assertions about a phase beyond P13. Its
premise, verified independently: the Master Roadmap ends at P13 and
establishes no later phase. Three phrases in this package, written during the
`FDR-6` execution, treated such a phase as having an authorization state. They
were corrected:

* the **Nature** row no longer names a record for it;
* blocker item 19 is now **Roadmap endpoint**;
* the Final State line is now `ROADMAP = P0–P13`.

**Nothing else changed.** P13 authorization, exit, certification state,
certified root, manifest (`127b97fd…`), guard, blocker classifications 1–18
and 20, and every `FDQ` disposition are as before. `FDR-6` is unchanged. Its
own text still states that it grants no authority for a later phase; that is
the Founder's non-grant clause, and it is preserved. `FDR-6` `§11` and `§16`
include a line about the next phase number. It is satisfied in its strongest
form: no roadmap artifact, state reader, verifier or authorization defines,
holds or authorizes any phase beyond P13.

## H. Superseded for current state (2026-09-25)

`ACT-CC-P13-CERT-GATE-003` changed Blueprint §16 and rebuilt the prepared
manifest (now `6265477f…`, Decision Register `§28`). This package stays as
the record of the state at `FDR-6` execution. The current package is
`AIOS_P13_CERTIFICATION_READINESS_PACKAGE_v1.1.md`.
