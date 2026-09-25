# `ACT-CC-P12-021` — P12 Completion Blocker Reconciliation · Return Package

> **Scope-locked.** Three targets only: `§6.8` negative controls, `§6.9`
> mutation tests, `§6.11` / `F-18` / `ESC-C7-01`. Nothing else was reclassified,
> and two adjacent items that this Act's own findings make suspect are recorded
> as **rediscovered, not investigated** (`§F`) rather than pulled into scope.

```text
P12 COMPLETE = NO
```

**The completion state did not change.** One blocker was legitimately closed,
one was proved to be the same blocker as another wearing a second label, and the
third was reclassified from *"the source does not exist"* to *"the source exists,
is authoritative, and says something different."* None of that moves `§6`.
Stated first because a reconciliation Act that improved three metrics and left
completion where it was is the only honest shape this could have taken — `§20`.

---

## A. `§6.8` — negative controls

### A.1 The exact failure

```text
python3 -m tools.p12_system_negative_controls
summary: {'controls': 13, 'attempted': 13, 'refused': 12, 'accepted': 1,
          'uncontrolled': 0, 'not_refused': ('false certification',)}
```

[E] One control of thirteen is `ACCEPTED`: **`false certification`**. A document
containing the sentence `PHASE 42 — FABRICATED ECOSYSTEM IS CERTIFIED.` causes
`p12_certified_evidence_guard.certified_phases` to report phase 42 as certified.
No Founder issued it. Nothing in the repository notices.

### A.2 `§6.8` and `§6.9` are one behaviour, not two

[E] `_false_certification` is three lines: `from tools.p12_mutation_verification
import _forge_decision; return _forge_decision()`. The `§6.8` control and the
`§6.9` mutation are **literally the same test**.

[D] `P12-019-RETURN-PACKAGE §7` listed them as two rows of a four-row blocker
table. That is not wrong about either, but it counts one finding twice, and a
completion table that double-counts overstates how much remains. Recorded here,
and the delegation left in place rather than re-implemented so the two can never
drift apart.

### A.3 The actual requirement, and the actual authority

[E] The guard determines certification by matching a certification **statement**
inside a resident instrument body, never from a filename. That was a deliberate
and correct choice — `IDENTIFIER ≠ DECISION BODY` — and the module records that
deriving the phase set from the Register's prose *was tried and rejected*,
because the Register contains the sentence *"It does **not** establish `PHASE 8
— CERTIFIED / COMPLETE`"* and every naive pattern reads a negation as a
certification.

[E] So the guard is not naive. It is **structurally unable** to do what is asked
of it, and the structure has a name.

### A.4 Root cause — this is `F-G1`, exactly

[E] Phase 3.285 found `F-G1` by live probe: `promotion_authorized` read the
`governance_decisions` **storage partition** and trusted **existence**, so a
component holding the storage handle could write a forged `approve` directly,
bypass `record_decision`'s `HumanAuthority` validation, and get `True`.

[E] Phase 3.286 closed it with *"an **in-memory authoritative provenance index**
that only a validated `record_decision` call populates"* — trust deliberately
**process-scoped**, *"because a persistent trust anchor is exactly what
Identity/Auth reserves."*

| | `F-G1` (closed) | `false certification` / `forge decision` (open) |
|---|---|---|
| Trusted store | `governance_decisions` partition | `docs/governance/acts/*.md` |
| Access control on it | none | none |
| Forgery | write a record directly | write a document directly |
| What would close it | an index only validated issuance populates | the same |
| Can that index be in-memory? | **yes** — the approving process is the consulting process | **no** — the guard runs in a fresh process and reads instruments no process here witnessed being issued |

[D] The one structural difference is decisive. `F-G1`'s fix works because
Governance approves and consults within one process lifetime. Certification does
not: the Founder issues an instrument outside any process, and every later
process must decide whether to believe a file. An index over that is
**persistent and cross-process** by definition.

### A.5 Security / identity dependency

[E] `Freeze §10` reserves the persistent cross-process trust anchor to
Identity/Authentication. `AIOS_PHASE3_300 §104` states the consequence without
hedging:

> *"a persistent cross-process trust anchor is reserved to
> Identity/Authentication (Freeze §10); introducing one now is out of scope and
> **forbidden**. No present defect."*

[E] `AIOS_PHASE3_298` carries the same as `I-2`, and `AIOS_PHASE3_333` as
`I-3333-03`. Three independent certified records, none of them P12's.

[C] **Classification: `SECURITY / IDENTITY DEPENDENCY` — EXTERNAL BOUNDARY, and
forbidden to resolve within P12.** Not an unfixed defect awaiting effort. The
last certified word on it is *"No present defect."*

### A.6 Falsification (`§19`)

**CLAIM.** `false certification` / `forge decision` cannot be resolved with
P12-authorized information without introducing a new trust authority.

**COUNTEREXAMPLE 1 — restrict the acts root.** The probe plants its document in
a `TemporaryDirectory`; `certified_phases(acts_root=…)` is parameterised and
defaults to the real root. If the parameter were removed, the mutation could not
plant and both metrics would go green.

> **OBSERVATION.** Planted the forgery inside a `shutil.copytree` of the real
> `docs/governance/acts` and called the guard on it.
>
> ```text
> resident certified phases:              [10, 11]
> with forgery planted in a full copy:    [10, 11, 42]
> 42 accepted:                            True
> ```
>
> **RESULT: REJECTED.** The forgery succeeds against the real root's own
> contents. Removing the parameter would move `§6.8` to `13/13` and `§6.9` to
> `10/10` while the system gained **no** ability to tell an issued instrument
> from a planted one. This is precisely the repair `§20` forbids, and it is now
> pinned as a test so it can never be mistaken for a resolution.

**COUNTEREXAMPLE 2 — require the Founder authentication block.** Genuine
instruments carry `Founder Name` / `Signature` / `Decision Status: FINAL /
ISSUED` / `Founder Authority: ISSUED`. Requiring it would reject the bare
forgery.

> **OBSERVATION.** Planted a forgery carrying a complete authentication block.
> `certified_phases` reports `42` as certified.
>
> **RESULT: REJECTED.** The block is body text; a forger writes body text. This
> is the certified `§124.1` finding — *"The guard cannot tell an instrument the
> Founder issued from one that merely says so"* — exercised rather than quoted.
> Also pinned as a test.

**COUNTEREXAMPLE 3 — an in-process provenance index, as `F-G1` used.** It closed
the structurally identical finding, so it should close this one.

> **OBSERVATION.** `F-G1`'s index is populated by `record_decision` — the
> validated call the approving process itself makes. No process in this
> repository observes the Founder issuing an instrument; the guard meets
> instruments only as resident files, in a process that did not witness their
> arrival. An index it could trust must therefore survive process boundaries.
>
> **RESULT: REJECTED** — and it is the rejection that identifies the missing
> thing precisely. What is needed is a *persistent cross-process* trust anchor,
> which is the reserved artifact by name.

**COUNTEREXAMPLE 4 — cross-check against a resident register of issued
instruments.** No new authority, just a second resident surface.

> **OBSERVATION.** Any such register is itself a document body in the same
> unprotected store. Planting a row in it is the same forgery one level out, and
> the guard's own header records that deriving the phase set from the Register's
> prose was tried and rejected for an independent reason.
>
> **RESULT: REJECTED.** Adding a second unauthenticated surface does not produce
> authentication.

**CLAIM SURVIVES.** Four candidate resolutions, two driven empirically, all
rejected. `§7`'s prohibitions were never approached: no trust anchor fabricated,
no authentication authority created, no identity boundary bypassed, no
authentication semantics weakened, no canonical security authority replaced with
a P12-local mechanism.

### A.7 Determination

[U] **EXTERNAL BOUNDARY. Not remediated, and not remediable within P12.**
`§6.8` stays `12 / 13`. `§6.9`'s `forge decision` stays `MISSED`. Both are the
same behaviour and both close together, when Identity/Authentication is ratified
and supplies the anchor — a Founder/Architect decision this Act does not
approach.

---

## B. `§6.9` — `duplicate delegation`

### B.1 The canonical search actually performed

[E] Searched for the prohibition at body level, not by citation:

| Searched | Result |
|---|---|
| `DP-02 §11` item 10 — **the citation six packages rest on** | `§11` is `REQUIRED POST-DECISION ACTION`; item 10 reads *"Continue only where existing authority permits."* **It says nothing about grants, instances, contexts or multiplicity.** |
| `w4_continuity.continuation_conditions` | *"`MORE THAN ONE LIVE GRANT FOR ONE INSTANCE` … a re-run must supersede rather than add to them (`§34`)"* |
| `ACT-CC-P11-009 §22`, as implemented | `duplicate` is one of nine states that must stay distinguishable |
| `AIOS_P10_…_VERIFICATION §94.3` (**certified**) | the second run *"superseded rather than accumulated"* |
| `docs/architecture/p12/w4-operations/first-execution.evidence.json` | a **fired** instance of the condition at `prior_state.continuation_conditions[0]`, written by `ACT-CC-P11-008`'s first execution on 2026-09-16, naming five accumulated grants for `engineering-intelligence-instance-001` |

### B.2 The actual body, against the classification built on it

[D] The recorded classification — *"no canonical prohibition exists; `DP-02 §11`
item 10 legitimises multi-context grants"* — is wrong twice over. The citation
does not say what it was said to say, and a canonical requirement does exist.
**This is my defect, carried unexamined across seven P12 records**
(`P12-006`, `P12-007`, `P12-008`, `P12-009`, `P12-016`, `P12-019`, `P12-74`),
and it is the same `§n`-namespace failure this programme has already caught
twice. Disclosed
rather than quietly corrected.

[E] The strongest evidence is not documentary. The resident P12 W4 evidence
record **already contains the fired condition.** The system detected this
in a real run while the mutation suite reported that it could not.

### B.3 Root cause — TEST-ORACLE DEFECT

[E] The probe drove `delegation_reconciliation.reconcile`, whose `DEFECT_KINDS`
are about the ledger ↔ projection relationship: unrepresented grants, stale
claims, provenance mismatch, duplicated *representation*. Grant **accumulation**
is not among them and never was.

[C] So the `MISSED` was never a system finding. It was `§48` — *"a relationship
is not considered verified merely because both surfaces exist"* — committed
inside the instrument built to refuse it: a system property asserted from a
component that does not hold it. **`TEST-ORACLE DEFECT`, not a system defect and
not a source gap.**

### B.4 Falsification (`§19`)

**CLAIM.** `duplicate delegation` MISSED was a test-oracle defect.

**COUNTEREXAMPLE 1 — `w4_continuity`'s condition is a rule AIOS invented**, so
re-pointing the probe at it launders an invented prohibition into a detection,
and `§11` forbids creating a prohibition because a mutation test expects one.

> **OBSERVATION.** `w4_continuity` predates P12 and was built under
> `ACT-CC-P11-009`, citing `§34`. Its condition is carried in **certified** P10
> evidence (`§94.3`) as the behaviour that actually occurred, and in live P12 W4
> evidence as a fired finding. Nothing was created this Act: no rule, no
> detector, no condition, no prohibition.
>
> **RESULT: REJECTED.** The prohibition is pre-existing and canonically anchored.

**COUNTEREXAMPLE 2 — the detector fires unconditionally**, so `DETECTED` is
meaningless.

> **OBSERVATION.** The probe's control drives two instances holding one live
> grant each. `duplicate_active` is `False`, `accumulated_grants` is `{}`. Pinned
> as its own test, because this exact shape was once a **false positive**:
> `duplicate_active` read `len(active) > 1` and reported the legitimate
> cross-Department state as a permanent blocker until P11 re-anchored it per
> recipient instance.
>
> **RESULT: REJECTED.** It discriminates, and the discrimination it makes is the
> one P11 paid for.

**COUNTEREXAMPLE 3 — the probe can no longer report `MISSED`**, so it has become
the unfalsifiable control this programme keeps catching.

> **OBSERVATION.** Two tests substitute a silent detector: one where
> `reconstruct` reports no accumulation, one where `continuation_conditions`
> surfaces nothing. Both drive the probe to `MISSED` with its reason.
>
> **RESULT: REJECTED.** The null result is still reachable.

**COUNTEREXAMPLE 4 — this is `§20` metric gaming**: `8/10 → 9/10` is the motive.

> **OBSERVATION.** The repair's justification is `§48` applied to the probe, not
> the count. If the count were the motive, the count would have bought
> something: it does not. `§6.9` remains **NO** on `forge decision` and
> `P12 COMPLETE` remains **NO**. The repair purchased **zero** completion
> progress and was made anyway.
>
> **RESULT: REJECTED.**

**CLAIM SURVIVES.**

### B.5 Remediation and its limit

[E] `_duplicate_delegation` now drives `w4_continuity` with a control in both
directions. Result: **DETECTED**. Suite: `8 / 10 → 9 / 10`.

[C] **Correspondence is a superset, not an identity.** `§50` names two grants of
the *same capability*; `w4_continuity` fires on any two live grants held by one
instance, whatever their scope. Detecting a superset does detect the named
mutation. Recorded as the broader reading it is rather than claimed as an exact
match — a claim of exact correspondence would be unevidenced.

[U] **REMEDIATED.** `§6.9` moves from `8/10` to `9/10` and stays **NO**.

---

## C. `§6.11` / `F-18` / `ESC-C7-01`

### C.1 Source discovery — complete

[E] **`ESC-C7-01` is resident, and has a full body.**
`docs/governance/AIOS_P10_AUTONOMOUS_EXECUTION_VERIFICATION_v1.0.md §21.3`,
titled *"`ESC-C7-01` — **NEW** · Volume 3 and Volume 4 residency"*, ten labelled
parts `A`–`J`. It recurs at 25 further locations in the same corpus as a
standing blocker across Cycles 7–15.

### C.2 Classification: **SOURCE FOUND — AUTHORITATIVE**

[E] The recorded classification — *"`ESC-C7-01`, the defining source, does not
exist"* (`P12-019-RETURN-PACKAGE` lines 115, 214) and *"`ESC-C7-01` absent"*
(`P12-016-RETURN-PACKAGE` line 297) — is **wrong in fact**. A citation audit
counted it among instruments *"cited, non-resident"*. It is resident. Disclosed
as my defect; corrected additively in both packages.

### C.3 The actual body

[E] Read and reported as written, not paraphrased into P12's vocabulary:

| Part | What it actually says |
|---|---|
| **A. Frontier** | *"The PD-03 and PD-04 canonical corpora exist, are complete, and are not resident. `G-01` was diagnosed as **absence**; for these two it is **non-residency**, which is a cheaper problem."* |
| **B. Evidence** | Volume 3 — 8 Part files, `A1`…`H10`, **80/80 identities, 3,704,607 bytes**. Volume 4 — 3 Part files, `A1`…`C10`, **30/30 identities, 1,508,896 bytes, matching `ACT-CC-P6-071 §2` to the byte** |
| **D. Classification** | `OWNERSHIP` / `CANONICAL` — supply of canonical corpus |
| **E. Current authority** | `DEL §3.1 C` repository mutation; `FDE §9` standing construction |
| **F. Missing authority** | **`E-29` — residency is conferred by Founder supply under a named Act.** Three requirements, none met: Founder/Architect transmission (*"files sit in a session path, not transmitted into an Act"*); a named authorizing Act; a namespace decision. `GDR-0026 §1` additionally reserves Volume lifecycle state to the Founder |
| **G. Minimum decision** | **(a)** authorize residency from the verified supplied-source path plus a namespace; **(b)** transmit them by explicit supply as PD-02 was; **(c)** direct that they remain non-resident |
| **H. Consequence if granted** | `G-01` closable for two of eight divisions; **110 verified section bodies** become constructible source — *"the single largest unlock available to this programme"* |
| **I. Non-impact** | *"Nothing else is blocked. `PD-05`…`PD-10` remain genuinely absent"* |

### C.4 What this changes about `F-18`

[D] **`ESC-C7-01` is not `F-18`'s defining source, and never claimed to be.** It
is a **residency escalation** over corpora in which a cross-PD interface
definition might be found. The two are different objects:

```text
ESC-C7-01   Founder residency decision  · source EXISTS, verified, NOT RESIDENT
ADR-0029    Architect-reserved          · INV-10 applicability undetermined
F-18        interface definition        · UNKNOWN — not "absent", NOT READABLE
```

[C] The interface's **existence is undetermined, not negative.** The corpora
that would answer it are verified to exist at byte level and are not resident.
Recording that as *"the defining source does not exist"* asserts absence where
the canonical record asserts non-residency, and `ESC-C7-01 §A` is explicit that
these are different problems and that non-residency is *"a cheaper problem"*.

[E] Corrected in the instrument as well as the prose. `p12_cross_pd_verification`
reported a single `SOURCE GAP (ESC-C7-01)` covering all eight silent divisions;
it now names the two halves separately, and a test pins the distinction:

```text
SOURCE GAP — NON-RESIDENCY (ESC-C7-01)   PD-03 / PD-04, exist and verified
SOURCE GAP — ABSENCE (G-01)              PD-05 … PD-10, genuinely absent
ARCHITECT-RESERVED (ADR-0029)            INV-10 applicability
```

[D] A cheap blocker hidden behind an expensive one is a blocker nobody brings to
the Founder. That is the operative harm in the old label, and it is the reason
this correction is worth more than the metric it does not move.

### C.5 Verification state, unchanged

```text
python3 -m tools.p12_cross_pd_verification
summary: {'checks': 6, 'current': 6, 'drifted': 0, 'unavailable': 0,
          'drifted_checks': (), 'interfaces_verified': 0, …}
```

[C] `interfaces_verified = 0`, and `§48` still cannot be met: an undefined
interface cannot be exercised. **`F-18` final state: `SOURCE GAP (NON-RESIDENCY)
+ ARCHITECT-RESERVED` — preserved, not manufactured.**

[U] `§16`'s prohibitions hold. Nothing was manufactured: not the source, its
contents, its authority, its interface definition, its ownership, or its
verification result. The source was **found and read**, which is the opposite
operation.

### C.6 Completion consequence

[U] `§6.11` stays **NO**. What changes is what the Founder is told: not *"a
source we need does not exist"* but *"a verified 5.2 MB corpus exists, is
complete, sits in a session path, and needs one of three named decisions —
`ESC-C7-01 §G` (a), (b) or (c)."* The first is not actionable by anyone. The
second is a decision that has been available since Cycle 7.

---

## D. `§18` — shared root cause across the three targets

| Target | Root cause | Shared with |
|---|---|---|
| `§6.8` `false certification` | reader derives authority from an unprotected store; the anchor that would fix it is `Freeze §10`-reserved | **`§6.9` `forge decision` — same behaviour, same code** |
| `§6.9` `forge decision` | as above | `§6.8` |
| `§6.9` `duplicate delegation` | probe asked a component that does not own the property | **none** |
| `§6.11` / `F-18` | corpora exist and are non-resident; `E-29` residency authority unmet | **none** |

[D] `P12-019 §7` said *"three of the four are the same finding wearing different
labels."* Two of the three are — and they are the same **code**, not merely the
same finding. The third was a different failure entirely, and treating it as
part of the security cluster is what kept it unexamined across seven records.

[C] There is a second shared cause, and it is mine rather than the system's.
Two of the three blockers were **misclassified by citation** — `DP-02 §11.10`
and *"`ESC-C7-01` does not exist"* — and in both cases the citation was carried
forward across multiple packages without anyone reading the body. `§5`'s actual
canonical body rule exists for exactly this, and I did not apply it to my own
prior work. The mechanism that caught both was the same: **read the body**.

---

## E. `§6` Exit Contract — recomputed

| | Condition | Before | **After** |
|---|---|---|---|
| 7 | system-wide verification completed | PARTIAL | **PARTIAL** — unchanged |
| 8 | negative controls hold | NO — `12/13` | **NO** — `12/13`, unchanged; `EXTERNAL BOUNDARY` |
| 9 | mutation tests hold | NO — `8/10` | **NO** — `9/10`; `duplicate delegation` remediated, `forge decision` is `§6.8` |
| 11 | cross-phase / cross-platform evidence | NO | **NO** — `interfaces_verified = 0`, blocker reclassified |

```text
P12 COMPLETE = NO
BLOCKING: §6 conditions 8, 9, 11   (and 7, partial)

  §6.8 + §6.9 forge decision   ONE behaviour · SECURITY/IDENTITY DEPENDENCY
                               Freeze §10 · forbidden to resolve in P12
  §6.9 duplicate delegation    CLOSED (test-oracle defect, remediated)
  §6.11 / F-18                 SOURCE NON-RESIDENT · ESC-C7-01 §G (a)/(b)/(c)
```

[U] `§21`: `COMPLETE ≠ CERTIFIED ≠ GOVERNANCE CLOSED ≠ P13 AUTHORIZED`. None is
claimed. `§57` certification remains Founder-reserved and is not approached.

---

## F. Fresh rediscovery

Re-derived after the work, not inherited.

| Item | State |
|---|---|
| `§6` blockers | 3 conditions, reducible to **2 distinct causes** (was 4 rows / 3 causes, one of them double-counted) |
| Founder-decidable now | **`ESC-C7-01 §G`** — (a) authorize residency + namespace, (b) transmit by supply, (c) direct non-residency. Available since Cycle 7 |
| Architect-reserved | `ADR-0029` / `ADP-P10-001` — `INV-10` applicability |
| Blocked on Identity/Auth ratification | `§6.8` + `§6.9 forge decision` — `Freeze §10` |
| Authorized actionable construction remaining | **none found** |

**Rediscovered, in scope of nothing, investigated by no one:** `P12-016 §474`
lists `ACT-CC-R2BC-IMPL-001` and `ACT-CC-P6-066-R2` alongside `ESC-C7-01` as
*"cited, non-resident"*. `ESC-C7-01` was in that list and is resident, so the
list's method is now suspect. Both identifiers do appear in the Governance
Decision Register and elsewhere. **Not investigated** — `ACT-CC-P12-021` is
scope-locked to three targets and widening it here would breach the lock.
Recorded as a frontier item for a future Act, unclassified.

---

## G′. The Act body is not persisted, and that is deliberate

[C] `ACT-CC-P12-019` was persisted verbatim under `docs/governance/acts/`
because its authentication was itself the question. `ACT-CC-P12-020` was not,
and `ACT-CC-P12-021` is not, for the same reason: **I do not hold its text
verbatim any more.** Writing a reconstruction into the governance corpus and
labelling it an Act would manufacture provenance for a document the Founder
never signed in that form — the one thing this programme forbids most often.

[U] This package cites the Act's sections (`§7`, `§11`, `§16`, `§18`, `§19`,
`§20`, `§25`, `§26`) as constraints I worked under, not as a resident body
anyone can re-read here. If a persisted copy is wanted, the Founder supplies it;
I do not author it.

---

## G. `§25` — persistence record

| # | Statement | Kind |
|---|---|---|
| 1 | `_false_certification` returns `_forge_decision()`; `§6.8` and `§6.9` share one code path | **FACT** |
| 2 | The forgery is accepted against a faithful copy of the resident acts root | **TEST RESULT** |
| 3 | The forgery is accepted when carrying a complete Founder authentication block | **TEST RESULT** |
| 4 | `Freeze §10` reserves the persistent cross-process trust anchor; `AIOS_PHASE3_300 §104` calls introducing one *"out of scope and forbidden"* | **FACT** (certified) |
| 5 | `false certification` / `forge decision` is a `SECURITY / IDENTITY DEPENDENCY`, not remediable in P12 | **INFERENCE**, from 2–4, four counterexamples rejected |
| 6 | `DP-02 §11` is `REQUIRED POST-DECISION ACTION`; item 10 is *"Continue only where existing authority permits"* | **FACT** |
| 7 | Six P12 packages classify `duplicate delegation` as a source gap citing `DP-02 §11.10` | **FACT** |
| 8 | That classification is false — citation misattributed, and a canonical requirement exists | **INFERENCE**, from 6 and B.1 |
| 9 | `w4_continuity` fires `MORE THAN ONE LIVE GRANT FOR ONE INSTANCE` for one instance × two grants, and is silent for two instances × one grant | **TEST RESULT** |
| 10 | The resident P12 W4 evidence record contains a fired instance of that condition | **FACT** |
| 11 | `duplicate delegation` MISSED was a `TEST-ORACLE DEFECT` | **INFERENCE**, from 8–10, four counterexamples rejected |
| 12 | `_duplicate_delegation` re-pointed at `w4_continuity`; suite `8/10 → 9/10` | **DECISION** + **TEST RESULT** |
| 13 | `w4_continuity` detects a superset of what `§50` names | **FACT**, recorded as a limit on 12 |
| 14 | `ESC-C7-01` is resident at `AIOS_P10_…_VERIFICATION §21.3` with a full `A`–`J` body | **FACT** |
| 15 | Prior packages record it as non-existent / absent | **FACT** |
| 16 | `ESC-C7-01` is about **non-residency** of PD-03/PD-04, not a missing interface definition | **FACT** (its `§A`) |
| 17 | `F-18`'s interface existence is **undetermined**, not absent | **INFERENCE**, from 16 |
| 18 | `ESC-C7-01` and `G-01` separated in `p12_cross_pd_verification`; both named, test-pinned | **DECISION** |
| 19 | `E-29` residency authority unmet on three independent requirements | **AUTHORITY GAP** (Founder) |
| 20 | `ADR-0029` / `INV-10` applicability undetermined | **AUTHORITY GAP** (Architect) |
| 21 | Identity/Authentication ratification and the trust anchor | **AUTHORITY GAP** (Founder/Architect, `Freeze §10`) |
| 22 | `P12 COMPLETE = NO`, blocking `§6` 8, 9, 11 | **INFERENCE**, unchanged by this Act |

---

## H. Prohibitions honoured

| `ACT-CC-P12-021` | Held |
|---|---|
| `§7` fabricate a trust anchor / create an authentication authority / bypass an identity boundary / weaken authentication semantics / replace canonical security authority with a P12-local mechanism | none approached; four candidate resolutions rejected, two empirically |
| `§11` create a prohibition solely because the mutation test expects one | none created — `w4_continuity` predates P12 and is certified-evidenced |
| `§16` manufacture `ESC-C7-01`'s source / contents / authority / interface definition / ownership / verification result | none — the source was found and read |
| `§20` repair merely because it improves a metric | the one repair made **buys zero completion progress**; the two repairs that *would* have improved metrics were driven, rejected, and pinned as tests |
| Manufacture Founder authority, consent or provenance | none |
| `docs/program/AIOS_*`, certified P10/P11 evidence | untouched; `§4.2` above preserved and corrected **additively** |
| Historical evidence rewritten | none — every correction is appended and labelled |

---

## I. Suites and instruments, as run

| | Result |
|---|---|
| `python3 -m unittest discover -s native_core -t .` | **801** tests · OK (1 expected failure) |
| `python3 -m unittest discover -s consumers -t .` | **276** tests · OK |
| `python3 -m unittest discover -s tools/tests -t .` | **1312** tests · OK (1 skipped) |
| `python3 -m tools.p12_system_negative_controls` | 13 attempted · **12 refused** · 1 accepted |
| `python3 -m tools.p12_mutation_verification` | 10 attempted · **9 detected** · 1 missed |
| `python3 -m tools.p12_cross_pd_verification` | 6 checks · 6 current · 0 drifted · **interfaces_verified 0** |
| `python3 -m tools.corpus_citation_audit` | no unresolved citation |

**Five tests were added, all of them adversarial**: two pin the falsified
`forge decision` repairs so neither can later be mistaken for a resolution; one
pins the two-instances control against the P11 false positive; two drive the
corrected `duplicate delegation` probe to `MISSED` with a silenced detector, so
its `DETECTED` remains a measurement. One test was **changed** — it asserted the
`MISSED` this Act proved was the probe's own defect, and the change is labelled
in the test body rather than made silently.
