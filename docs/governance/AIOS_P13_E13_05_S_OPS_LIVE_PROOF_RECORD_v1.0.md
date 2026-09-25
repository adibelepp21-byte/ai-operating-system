# AIOS P13 — E13-05 S-OPS Controlled Live Proof Record v1.0

| Field | Value |
|---|---|
| **Authority** | `FDR-3` (Decision Register `§23`; `acts/FDR-3-S-OPS-DEDICATED-BOUNDED-OPERATIONAL-PROOF-SURFACE-FOR-E13-05.md`, content sha256 `e7dc3fa9…`) |
| **Executable authority used** | `P13-ENV-02` (Delegation Register `§15`) for the two S-OPS transitions · `P13-ENV-01` for observing and recording · `FDR-3` with `P13-018` `D-1` for construction · `DEL-CFV2-CEO-001` for recording. **No authority was created, widened or inferred** |
| **Prepared by** | Claude Code — AIOS Co-Founder + Delegated CEO · 2026-09-24 |
| **Disposition** | **E13-05 VERIFIED**, in `FDR-3` `§15`'s sense: P1–P6 are demonstrated by live evidence, and the negative controls pass. See §H |
| **Certification** | NOT GRANTED. P13 completion is not claimed. Phase 13 completion and any later phase are not authorized |

## A. Founder Decision persistence

| | |
|---|---|
| Decision | `FDR-3`. It is the next identifier in the `FDR` series, and the one three persisted Founder instruments give this decision. The act header shows the derivation and discloses an earlier, unused label |
| Record | `docs/governance/acts/FDR-3-S-OPS-DEDICATED-BOUNDED-OPERATIONAL-PROOF-SURFACE-FOR-E13-05.md`. The Founder's text is verbatim; sha256 `e7dc3fa9bdf8ed81bb6decff3f0b0d4a3d4fcab2c781fd8efabacc87fb3a820f` |
| Registration | Decision Register `§23`. The index sees one Register record, `FDR-3`, issued by the Founder. `tools/authority_citation.refusal` resolves it |
| Executable form | `P13-ENV-02`: `docs/governance/p13-envelopes/P13-ENV-02.json`, sha256 `b572ebf5…`, recorded in Delegation Register `§15` |
| Order (hard gate `§5`) | the decision was persisted and registered (commit `ee5014d`), then the definition and envelope were recorded (`89a6721`), then construction (`de0fc36`), then the live proof. The proof ran on `de0fc36` with a clean tree |
| Projection | state-changing authority: `BOUNDED: s_ops.close → docs/operations/s-ops/S-OPS-01.json (P13-ENV-02 · FDR-3 §4); s_ops.open → docs/operations/s-ops/S-OPS-01.json (P13-ENV-02 · FDR-3 §4)`. Operational envelope: `EVIDENCE-ONLY + BOUNDED STATE-CHANGING`. Phase: NOT AUTHORIZED. Certification: NOT GRANTED |

## B. S-OPS

This section summarises `docs/operations/s-ops/S-OPS-DEFINITION.md`.

| | |
|---|---|
| Identity | `S-OPS-01`, a scheduled operational window, at `docs/operations/s-ops/S-OPS-01.json` |
| Owner | S-OPS operational proof surface. Its only writer is `tools/s_ops/surface.py` |
| State model | `CLOSED`, `OPEN`. The window is fixed at provisioning. Its phase (`BEFORE`, `WITHIN`, `AFTER`) is observed and never stored. The contract is BEFORE → CLOSED, WITHIN → OPEN, AFTER → CLOSED |
| Permitted transitions | `s_ops.open` (CLOSED → OPEN, WITHIN only) and `s_ops.close` (OPEN → CLOSED, outside the window only) |
| Preconditions | re-checked at the gate: the object exists and the surface owns it · the state is the `from` state · the phase **now** is the one permitted. The surface re-checks them itself (compare-and-set) |
| Expected consequence | fixed on P13's proposal before the gate: the criterion that failed (`CR-SOPS-01-OPEN-WITHIN-WINDOW` or `-CLOSED-OUTSIDE-WINDOW`) becomes PASS |
| Reversibility | `close` is `open`'s inverse, and the contract requires it once the window ends. The history is append-only |
| Observation | P13's `s_ops` Source reads from disk. Independently: `python -m tools.s_ops.surface show`, sha256, `git diff` |
| Exclusions | definition `§10`. It is not P13's knowledge, not the frontier register, not P1–P12, not P11, not governance, not production or external, not arbitrary write access, not code, and not an authority source |

## C. Construction

**Discovery.** Definition `§1` checked ten existing surfaces on all nine
dimensions. None is adequate:

* the operational ones are owned by P1–P12, P11 or governance;
* the ones P13 owns are epistemic;
* `S-HOLD` would let P13 alter its own authority to act;
* `S-CITE` would write P1–P12 artifacts.

| Built | Where |
|---|---|
| the surface (provision, transition, read, observe; no other writer) | `tools/s_ops/__init__.py`, `tools/s_ops/surface.py` |
| `s_ops` Source; `Context.taken_at` | `tools/p13/state.py` |
| `CR-SOPS-01-OPEN-WITHIN-WINDOW`, `CR-SOPS-01-CLOSED-OUTSIDE-WINDOW`, citing `FDR-3` and judged by the surface's `REQUIRED` | `tools/p13/evaluation.py` |
| `s_ops.open`, `s_ops.close`: state-changing, three preconditions, a boundary covering the S-OPS root, the Registers, the envelopes and the `FDR-3` act, and a read-back postcondition | `tools/p13/catalog.py` |
| `Paths.s_ops`, which follows a test's live override | `tools/p13/paths.py` |
| an unambiguous state-changing projection | `tools/p13/authority.py` |
| docstrings updated to the new authority state | `tools/p13/__init__.py`, `tools/p13/execution.py`, `tools/p13/evolution.py` (the ERROR disposition), `tools/p13/catalog.py` |
| tests | `tools/tests/test_s_ops.py` (34). Changed with evidence: `test_p13.py` and `test_p13_post_construction.py`, whose pins now expect both envelopes and FDR-3's two executable types |

**Disclosed defect (self-introduced).** The first full regression failed
`EveryEntryPointInstallsTheBarrierBeforeItCanWrite`. `tools/s_ops/surface.py`'s `__main__`
did not import `tools` when run by path, so it could have run without the
certified-write barrier. It was fixed before commit `de0fc36`, as the other
entry points do it.

## D. E13-05 live proof

Every cycle was one invocation of `python -m tools.p13.cycle`, with:

* invoker *"Claude Code — AIOS Co-Founder + Delegated CEO (runner; FDR-3 §8)"*;
* intent *"E13-05 controlled live proof under FDR-3: observe, evaluate, reason
  and decide; act only within recorded authority"*.

The invocation was the same all five times. It names no action and no target.
The operator provisioned `S-OPS-01` at 16:37:27 UTC, with the window 16:39:57 →
16:44:57 UTC.

| Cycle | Observed | S-OPS criteria before | P13's decision on S-OPS | S-OPS-01 sha256 |
|---|---|---|---|---|
| `20260924T163728-11fe8aed` | CLOSED · BEFORE | both PASS | **none**; it refreshed evidence, read-only | `813837ea…` → `813837ea…` |
| `20260924T164000-d1954b46` | CLOSED · WITHIN | OPEN-WITHIN **FAIL** | `s_ops.open` **EXECUTE** under `P13-ENV-02` | `813837ea…` → `c3d2203c…` |
| `20260924T164018-34223b91` | OPEN · WITHIN | both PASS | **none** (rediscovery) | unchanged |
| `20260924T164501-7f84980f` | OPEN · AFTER | CLOSED-OUTSIDE **FAIL** | `s_ops.close` **EXECUTE** under `P13-ENV-02` (the reversal) | `c3d2203c…` → `e2781df3…` |
| `20260924T164519-b7456bbc` | CLOSED · AFTER | both PASS | **none** (rediscovery) | unchanged |

**The chain in `20260924T164000-d1954b46`, read from the record:**

1. **Observe.** Facts `s_ops.S-OPS-01.state = CLOSED` and `phase = WITHIN`,
   VERIFIED, source `tools.s_ops.surface.observe()`.
2. **Evaluate.** `CR-SOPS-01-OPEN-WITHIN-WINDOW` = FAIL.
3. **Reason.** `c:defect:CR-SOPS-01-OPEN-WITHIN-WINDOW` (`R-DEFECT`), from
   premises `eval:CR-SOPS-01-OPEN-WITHIN-WINDOW`, `s_ops.S-OPS-01.state` and
   `s_ops.S-OPS-01.phase`. `R-CHANGED`: the phase changed since the previous
   cycle.
4. **Decide.** Proposal `p:s_ops.open:docs/operations/s-ops/S-OPS-01.json`,
   rank 0. Expected `{CR-SOPS-01-OPEN-WITHIN-WINDOW: PASS}`, fixed before the
   gate.
5. **Authority.** EXECUTE, *"permitted by P13-ENV-02 (FDR-3 §4)"*, scope
   `[docs/operations/s-ops/S-OPS-01.json]`. The three other proposals were
   refused by the cycle bound.
6. **Execute.** `tools.s_ops.surface.transition`. Changed:
   `[docs/operations/s-ops/S-OPS-01.json]`. Outside scope: `[]`. The
   postcondition held: *"S-OPS-01 reads back OPEN; its last history entry is
   open CLOSED → OPEN"*.
7. **Re-observe.** A fresh observation from disk: state OPEN.
8. **Consequence.** Re-evaluation gives FAIL → PASS. Expected
   `{…: PASS}`, actual `{…: PASS/VERIFIED}`, **matched: true**.
9. **Trace.** Status `success`. The `execution` block names `P13-ENV-02`,
   `FDR-3 §4` and the scope.
10. **Decision provenance** (`evidence.decision_provenance`): no faults.

`20260924T164501-7f84980f` has the same chain for `s_ops.close`: expected
`{CR-SOPS-01-CLOSED-OUTSIDE-WINDOW: PASS}`, actual PASS/VERIFIED, matched.

| Dimension | Status | Evidence |
|---|---|---|
| **P1 Decision** | **LIVE PROVEN** | the chain above, twice. The same invocation gave no action (C1, C3, C5), `open` (C2) and `close` (C4), each determined by what P13 observed. Provenance holds on every record |
| **P2 Authority** | **LIVE PROVEN** | `FDR-3` → `P13-ENV-02`, resolved with no anomalies. The target was in scope. The transition is permitted, and its preconditions were re-checked at the gate. The boundary hashes show that no Register, envelope or act changed |
| **P3 Execution** | **LIVE PROVEN** | the object on disk changed from `813837ea…` (CLOSED) to `c3d2203c…` (OPEN) and then to `e2781df3…` (CLOSED). `S-OPS-01.json` is committed with its three-entry history |
| **P4 Consequence verification** | **LIVE PROVEN** (match) · mismatch handling **TEST PROVEN** | expected vs actual, from a fresh re-observation, matched twice live. A mismatch is never a success, and it is reviewed rather than retried: NC-05 and `test_p13_e13_05.py` |
| **P5 Evidence** | **LIVE PROVEN** | five cycle records and five Trace entries. `EvidenceStore.verify` holds on all 11 live records. C5's own verifier found `CR-P13-EVIDENCE` PASS/VERIFIED. The object's history names the actor and basis of each transition |
| **P6 Re-observation / rediscovery** | **LIVE PROVEN** | C3 observed OPEN from disk, reported no change and did not act. C4's `R-CHANGED` saw the phase move. C5 observed CLOSED and did not act |

**Independent observation.** After each cycle, `python -m tools.s_ops.surface
show` read the object in a separate process: CLOSED/BEFORE, OPEN/WITHIN,
OPEN/WITHIN, CLOSED/AFTER, CLOSED/AFTER. The sha256 was taken before and after
each cycle.

## E. Negative controls

**TEST PROVEN** (`tools/tests/test_s_ops.py`). Each runs the real code path
against a temporary S-OPS, with copies of the real authority records. Each
asserts the decision, that the object's bytes are unchanged, and that the
refusal is in the Trace.

| Control | Expected | Actual | Status |
|---|---|---|---|
| NC-01 Invalid authority | REFUSE | no S-OPS envelope → ESCALATE (*"no recorded envelope permits"*: a refusal that is also escalated) · a non-Founder envelope → anomaly → ESCALATE · a type the envelope does not name → REFUSE | PASS |
| NC-02 Ambiguous authority | STOP/ESCALATE | two envelopes granting one transition → ESCALATE (*"envelopes conflict"*) · the envelope recorded twice → AMBIGUOUS anomaly → ESCALATE · an expiry that is not a date → AMBIGUOUS → ESCALATE | PASS |
| NC-03 Invalid target | REFUSE | a target the envelope does not name → REFUSE (*"wrong target"*) · six other paths → REFUSE | PASS |
| NC-04 Failed precondition | REFUSE | the window had not opened when the gate decided → REFUSE · the state had changed → REFUSE · an object the surface does not own → REFUSE | PASS |
| NC-05 Consequence mismatch | DETECT / NO FALSE SUCCESS | a change undone before re-observation → `matched: false`, Trace `failure`. The next cycle raises `R-MISMATCH` → `review.consequence` ESCALATE, and `s_ops.open` is **not** re-proposed · a postcondition that fails → a `failure` outcome · a change outside the object → a `failure` outcome | PASS |

**Also LIVE.** These are runner-built proposals given to the real gate, with
the real envelopes and the real object, at 16:45:52 UTC. They are not P13
decisions. The gate alone writes no Trace, so they are recorded here. The tree
was byte-identical afterwards.

```text
NC-01 | s_ops.delete → S-OPS-01.json          | REFUSE | unknown action type: not in the ActionCatalog
NC-03 | s_ops.open → Delegation Register        | REFUSE | wrong target: … is outside P13-ENV-02's scope
NC-03 | s_ops.open → S-OPS-DEFINITION.md        | REFUSE | wrong target: … is outside P13-ENV-02's scope
NC-04 | s_ops.open → S-OPS-01.json (AFTER)      | REFUSE | missing precondition: S-OPS-01's window phase is now AFTER, not WITHIN
NC-04 | s_ops.close → S-OPS-01.json (CLOSED)    | REFUSE | missing precondition: S-OPS-01 is CLOSED, not OPEN
```

NC-02 and NC-05 were **not** run live. Doing so would mean making the real
authority records ambiguous, or injecting a fault into the real surface.
`FDR-3` `§3` excludes both.

**Mutation checks S1–S15.** Each S-OPS protection was removed in turn, and a
test failed every time:

* the three gate preconditions;
* the surface's compare-and-set and window check;
* the postcondition, and two kinds of boundary narrowing;
* the criterion judge;
* the test root override, and the observation instant;
* re-provisioning, history rewrite, the wrong transition, and an absent object
  judged as a violation.

## F. Live vs test evidence

| LIVE PROVEN | TEST PROVEN ONLY | NOT PROVEN |
|---|---|---|
| P1–P6 on the real S-OPS-01 (§D) · the reversal (C4) · refusals by the live cycle bound · the NC-01/03/04 gate probes | NC-01…NC-05 as full cycles with Trace · the mismatch path (P4's negative branch) · mutation checks S1–S15 · the pre-live rehearsal on a temporary root | NC-02 and NC-05 live, which were excluded (§E) · the proof on a surface with an external consumer (§I) |

No test output is reported as live. The rehearsal ran five cycles in a
temporary directory before the live proof. It left no live record.

## G. Governance integrity

**Confirmed.** The live proof changed exactly these, and nothing else (`git
status`):

* `docs/operations/s-ops/S-OPS-01.json`;
* five new records in `docs/operations/p13/cycles/`;
* `docs/operations/p13/trace/trace`.

In detail:

* **No P1–P12 ownership mutation.** No file under a phase directory changed.
* **No P11 organizational mutation.**
* **No production or external mutation.** There was no network or process
  action.
* **No arbitrary write authority.** One object and two transitions. The gate's
  scope and the execution boundary both enforce it, and the boundary hashes
  showed only the object changed.
* **No self-authorization, and no authority synthesis.** `P13-ENV-02` was
  recorded before construction, cites `FDR-3`, and did not change. P13 cannot
  provision objects, move the window or widen the envelope.
* **No certification granted.** The certification guard still reads P13 NOT
  GRANTED.

## H. E13-05 final disposition

**VERIFIED.**

* All six dimensions are demonstrated by live evidence on real operational
  state.
* The action was determined by P13: the same invocation led to three different
  behaviours, each from observed state.
* Authority came from a recorded Founder decision, and nothing else.
* The real mutation was verified against an expectation fixed beforehand.
* The changed state entered the next cycle's cognition.
* The negative controls pass. The mismatch branch and NC-02/NC-05 are
  test-proven, not live.

**VERIFIED is a proof result, not certification.** It does not make P13
complete. The other exit criteria are not assessed here.

## I. Residual frontier

Nothing below is resolved by this proof:

1. **NC-02 and NC-05 live.** They are not demonstrable within `FDR-3`'s bounds.
2. **Operational meaning.** Nothing outside the surface consumes S-OPS-01, by
   design. A proof on a surface with real consumers is a separate decision.
3. **Operator-chosen window.** The operator decides *when* the contract changes;
   P13 decides *what* to do (definition `§11`).
4. **`P13-ENV-02` is exhausted.** Any further live state-changing work needs a
   new Founder decision.
5. **Compare-and-set is not atomic across concurrent writers.** One runner is
   assumed; there is no daemon.
6. **The UTC clock is trusted.**
7. **Standing:**
   * phase authorization NOT AUTHORIZED;
   * certification NOT GRANTED;
   * `FD-2` open;
   * the F-4 question open;
   * the residual frontier register epistemic and not built (E13-07);
   * `GAP-0017`/`GAP-0018` frontier.
8. **Canonical architecture not updated.** `FDR-3` does not authorize
   modifying canonical architecture, so the Blueprint was not touched. Its
   appended status note (`§14`) still reads *"No production state-changing
   action exists, and no envelope grants one"*. That is now stale. Correcting
   it needs authority beyond `FDR-3`.
9. **Superseded, not rewritten.** The earlier E13-05 operational surface record
   stays as written (BLOCKED). This record supersedes its classification.
10. **Documentation gap (pre-existing).** `docs/operations/README.md` does not
    list the `p13/` root.

## J. Evidence

| | |
|---|---|
| Commits | `ee5014d` (`FDR-3`) · `89a6721` (definition, `P13-ENV-02`, projection) · `de0fc36` (construction) · this record's commit (live evidence and records) |
| Live cycles | `20260924T163728-11fe8aed` · `20260924T164000-d1954b46` · `20260924T164018-34223b91` · `20260924T164501-7f84980f` · `20260924T164519-b7456bbc` (`docs/operations/p13/cycles/`) |
| S-OPS-01 | `docs/operations/s-ops/S-OPS-01.json`, final sha256 `e2781df37148d80b1e404c2cba9583d50daeee35271cdece12fc4f018c527edd` |
| Tests at `de0fc36` | tools 1632 OK (1 skipped) · native_core 801 OK (1 expected failure) · consumers 276 OK · bounded_exception 29 OK |

---

### Appended 2026-09-24 — FDR-4 (everything above unchanged)

`FDR-4` (Decision Register `§24`):

* **`FD-A`.** Live ESCALATE proof is not required for E13-05 verification.
  The escalate branch is test-proven and remains so. **E13-05 remains
  VERIFIED.**
* **`FD-B`.** `P13-ENV-02` is spent / retired / revoked (Delegation Register
  `§16`). §I item 4 above is therefore settled by decision, not only by the
  object's state.
* **`FD-C`.** §I item 8 is reconciled by an append-only Blueprint note
  (`§15`); `§13` and `§14` are kept as written.
* **`FD-D`.** P13 is EXIT-READY. The reconciled state is in
  `docs/governance/AIOS_P13_EXIT_READINESS_PACKAGE_v1.0.md`.
