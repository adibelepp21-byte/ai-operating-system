# P13 — Controlled Operational State Definition: Residual Frontier Register

## 1. Document control

| Field | Value |
|---|---|
| **Prepared under** | `docs/governance/acts/P13-CONTROLLED-OPERATIONAL-STATE-DEFINITION-INSTRUCTION.md` (content sha256 `f4c828ec…`) |
| **Follows** | `P13-E13-05-SEMANTIC-PROOF-SURFACE-DISCOVERY.md`, which is not modified. Where this document refines it, it says so (§13, §24) |
| **Date** | 2026-09-24 |
| **Prepared by** | Claude Code — AIOS Co-Founder + Delegated CEO |
| **Nature** | **Semantic definition.** Not an FDR, not a Founder recommendation, not an authority envelope, not a design. Nothing was built. No register or workspace exists. No source, P13 code, gate, envelope or frontier item was changed |
| **Evidence labels** | **[CAN]** canonical (Founder instrument) · **[CEO]** CEO record (below Founder decisions) · **[VER]** verified reality · **[MEA]** measured here · **[IMP]** implementation fact · **[DIS]** discovery result · **[PRO]** proposed by this analysis · **[UNK]** unknown · **[INS]** insufficient evidence |

## 2. Purpose and scope

The aim is to define the residual frontier register as an operational state
precisely enough that the Founder decides a real governance boundary, not an
implementation detail. Four things are defined:

* what an entry means;
* what "known" means;
* which transitions are valid;
* how the state takes part in *observe → reason → act → consequence →
  re-observe → rediscover*.

The scope is E13-05 only.

## 3. Source basis

| Source | What it establishes | Grade |
|---|---|---|
| FDR-2 `D08` | completion *with a classified residual frontier*: *"the remaining frontier is known but outside the authorized P13 completion contract"* | [CAN] |
| FDR-2 `D07`, E13-07 | *"remaining gaps are classified; unresolved frontier is explicitly recorded; no unresolved authorized requirement is silently omitted"* | [CAN] |
| FDR-2 `GSI-07` | *"Unknown future capability remains classified as frontier rather than being falsely marked solved."* | [CAN] |
| FDR-2 E13-05 | *"Where D05 permits autonomous execution, P13 can: check authority; execute authorized action; refuse …; escalate …; record evidence; verify outcome."* | [CAN] |
| `P13-018` `§3` | permits *"creation of P13-specific records and evidence"*; prohibits modifying governance authority and Founder decisions, creating authority, and treating an unrecorded proposal as authorization | [CAN] |
| `P13-018` `§5` | *"The Founder explicitly rejects the interpretation that D-2b automatically proves the complete E13-05 execution criterion."* | [CAN] |
| Blueprint `§3.2` | `Frontier` … **owns *the residual frontier register***; `§6` P13 writes only `docs/operations/p13/`; `§7` E13-07's acceptance is derived from `P13-015` | [IMP] (CEO architecture; construction approved under `P13-018` `D-1`) |
| `P13-015` | the question matrix. Its own authority field: *"Each classification below is **CEO evidence for FDR-2, not a decision**."* Frontier rows: Q38, Q39, Q91 (P13 FRONTIER), Q23 (UNKNOWN) | [CEO] |
| `P13-017` `§2` | `GAP-0017` replanning and `GAP-0018` recovery beyond escalation, classified as residual frontier | [CEO] |
| `tools/p13/frontier.py`, `cycle.py`, `evidence.py`, `state.py` | the frontier is recomputed per cycle from `P13-015` and `P13-017`; written into each immutable cycle record; **not** into Trace outputs, so not into Memory; no reasoning component reads cycle records | [IMP], [MEA] |
| 5 live cycle records | the same six items each cycle, each carrying identity, classification and source | [MEA] |
| `P13-019`; the semantic discovery report | the E-0…E-3 boundary options; S11 as the conditional surface | [PRO], [DIS] |

**Source-grade finding, recorded rather than reconciled silently.** The
instruction speaks of the *canonical frontier*:

* The **requirement** that a classified frontier exists is canonical [CAN].
* The **membership and classification** of the six items come from **CEO
  reconciliation records** [CEO]. `P13-015` itself says its classifications are
  "not a decision".

This document therefore calls them the **Authoritative Frontier Sources
(AFS)**, with this precedence:

```text
Founder decisions [CAN]  >  AFS (CEO records)  >  register (P13 operational knowledge)
```

Whether the Founder wants to designate the AFS explicitly is question Q8.

## 4. Current discovery finding

This carries the discovery report forward, with its classes unchanged:

* S11 was the only candidate inside C2 with a reason to exist independently of
  testing [DIS].
* The register is named in the architecture [IMP] and not realized [MEA].
* P13 Memory holds no frontier content [MEA].
* The frontier has not moved across 5 live cycles [MEA].
* There is no workspace [MEA].
* State-changing authority is NONE [MEA, FE-2].

**Added by this definition [MEA].** Every immutable cycle record already holds
each frontier item's identity, classification and source. The knowledge exists
as **evidence**. It does not exist as **operational knowledge**: the Memory path
by which P13 knows its own history (Blueprint `§6`) does not carry it. That
changes the analysis in §18.

## 5. Residual frontier (semantic definition)

**Residual frontier.** The set of AIOS matters an AFS classifies as unresolved
and outside the authorized P13 completion contract. They are known, classified,
and explicitly not claimed solved (`D08`, E13-07, `GSI-07` [CAN]). It is a
property of **AIOS as the AFS describe it**, not of P13.

## 6. Frontier item

**Frontier item.** One matter an AFS identifies and classifies as residual
frontier, under the AFS's own identifier. The existing taxonomy has exactly two
kinds [CEO]; no other category is introduced:

| Kind | Existing source | Current members [MEA] |
|---|---|---|
| **question** | `P13-015` row, category *P13 FRONTIER* or *UNKNOWN* | Q38, Q39, Q91; Q23 |
| **gap** | `P13-017` `§2`, classified *residual frontier* | GAP-0017, GAP-0018 |

**Q23 (UNKNOWN).** It counts as frontier on the `GSI-07` basis (*unknown …
remains classified as frontier*) and because the implementation treats it so
[IMP].

**Not frontier items**, though each cycle's *remainder* lists them [IMP]:

* escalated proposals, whose home is the escalation register;
* refusals and UNKNOWN decisions, which are cycle outcomes;
* limitations, which are transient;
* *refreshable* evidence, which is P13 self-state.

Admitting them would widen the register beyond `D08`'s residual frontier.

## 7. Frontier observation

**Frontier observation.** In one cycle, P13 read an AFS and found item F
classified there as frontier: F's identifier, kind, classification and source,
at a time, in that cycle. It exists today [IMP/MEA]. It lives as a **fact of the
cycle**, and as **evidence** in the immutable cycle record. It is **not** carried
into the next cycle's understanding.

## 8. Frontier register

**Frontier register.** P13's **retained operational knowledge** of the residual
frontier. For each item P13 has admitted, it holds what P13 observed and when.
It is **not** the frontier, and **not** a classification of it [PRO]. It answers
one operational question the AFS cannot:

> *has P13 already observed this item, and since when?*

**What "known" means [PRO].** Item F is *known* to P13 when P13 retains, across
cycles and in the knowledge it reasons from:

* F's identity as the AFS gives it;
* the AFS provenance;
* F's classification **as observed** (a quotation, not an assertion);
* the cycle in which P13 first observed F;
* a reference to that cycle's evidence.

*Present in a file* is a representation of this. It is not its meaning (§18).

## 9. Admission

**ADMIT F [PRO].** P13 moves F from *observed this cycle, not retained* to
*retained operational knowledge*. It does so because F appears in an AFS and is
absent from P13's retained knowledge.

The instruction's eight questions, answered from sources:

| # | Question | Answer | Basis |
|---|---|---|---|
| 1 | condition permitting admission | F is observed in an AFS **this cycle** · F is not already retained · F resolves to its AFS entry · the register's own history is intact · authority permits | [PRO], from §5–§8 |
| 2 | evidence required | the AFS entry itself, and the observing cycle's record | [PRO] |
| 3 | who determines eligibility | **P13, by rule, from observed facts** (Frontier/Reasoning). Not the harness, and not a human per item. The *authority* to admit at all is human-granted | [PRO]; Blueprint `§3.4` (deterministic rules) [IMP] |
| 4 | classification or recording? | **recording.** The classification is quoted from the AFS; P13 holds no classification authority | `P13-015` authority field [CEO]; FE-2 state-changing = NONE [MEA] |
| 5 | can it alter the canonical frontier? | **no** | P13 writes only its live root: `P13-ENV-01` `designated_live_root`, Blueprint `§6`/`§11` [CAN/IMP]; the AFS lie outside it |
| 6 | can it change an item's classification? | **no** | as 5, and `GSI-07` [CAN] |
| 7 | can it declare a gap closed? | **no** | `GSI-07` *"rather than being falsely marked solved"* [CAN]; `P13-018` `§6` *"certify itself solely because the criteria were satisfied"* is prohibited [CAN]; no authority [MEA] |
| 8 | can it declare P13 complete? | **no** | completion is `D08`'s conjunction over authorized scope, capabilities, integration, governance, evidence and classified frontier [CAN]; `P13-018` `§10` *P13 COMPLETION = NOT CLAIMED* [CAN]. Admission alters none of those |

## 10. Canonical state vs P13 operational knowledge

**Recording is not deciding.** The two kinds of act differ:

```text
"P13 observed F, classified X by AFS A, since cycle N"   (recording: P13 operational knowledge)
            ≠
"F is (no longer) a frontier item"                       (deciding: AFS / Founder authority)
```

**RECORDING AUTHORITY ≠ CANONICAL DECISION AUTHORITY.** The canonical basis
is:

* `P13-018` `§3` separates *creation of P13-specific records* (permitted) from
  modifying governance authority and Founder decisions (prohibited) [CAN];
* `GSI-07` forbids marking the frontier solved [CAN];
* Blueprint `§5.3` holds that a recorded answer *"never becomes APPROVED"*
  [IMP], which is the same pattern.

Applying this to the register is [PRO].

## 11. Ownership and authority boundary

| Object | Owner | Category |
|---|---|---|
| AFS (`P13-015`, `P13-017`) | their authors: CEO records under `DEL-CFV2-CEO-001`; Founder decisions above them | authoritative frontier classification |
| the register | **P13 `Frontier`** (Blueprint `§3.2`). *"Owns"* means P13 is its sole writer and custodian [PRO reading of IMP] | **P13 operational knowledge: persisted derived state** |
| cycle records, Trace | P13 (writer); immutable | **evidence** (Blueprint `§6`, `G-04`) |
| Memory | P7 semantics; derived on read from Trace | **memory**. The register is **not** Memory, and it is not Trace |

**OWNERSHIP OF THE REGISTER ≠ AUTHORITY OVER THE FRONTIER.** Owning the
register gives no right to write the AFS, to classify, or to close anything.

## 12. State-before / state-after model

The instruction's working abstraction was checked against the sources. It
holds, with one correction.

| | AFS [CAN/CEO] | P13 evidence [MEA] | P13 operational knowledge | Register |
|---|---|---|---|---|
| **Before** | F classified frontier | F appears in each cycle record, **already** | F observed **within the cycle**; **not retained** (not in Memory [MEA]) | F absent |
| **After** | **unchanged** (required) | plus the admitting cycle's record and Trace entry | **F retained**: known since cycle N | F present, with identity, provenance, classification as observed, first cycle and evidence reference |

**Correction.** *"F not persistently represented"* is inexact. F **is**
persistently represented, **as evidence**. What admission changes is
**operational knowledge**: what P13 reasons from. The canonical frontier does
not change.

## 13. Minimum meaningful state transition

**Candidate:** ADMIT exactly one AFS frontier item that is observed and not
retained [PRO].

It is minimal because:

* nothing smaller retains knowledge;
* a timestamp or last-seen write would add no knowledge;
* a whole-set admission is several transitions.

**It is monotonic**, and that matters in §18.

**The first non-monotonic transition [PRO]: SUPERSEDE-BY-OBSERVATION.** When
the AFS basis of a retained F changes, or F is no longer observed in any AFS,
P13's current view of F is updated. The prior view is kept in history.

* It is still observational: it records *"as of cycle M, not observed in the
  AFS"*, never *"resolved"* (`GSI-07`).
* It requires more judgment: P13 must tell a basis change from source
  unreadability (a limitation, so no supersede) and from reclassification.
* It is **not** within an admission-only scope. Q2 decides between the two.

**Refinement of the discovery report (§13 there).** That report held that
establishing the register is not a sufficient proof. This definition narrows
the point: the first admission is also the register's creation and is judged
alone. Later admissions of the six never-retained items are each re-observed in
the next cycle, and the full chain holds for them (§24).

## 14. Expected consequence

**Before execution, P13 expects:**

1. the register gains exactly F, with its provenance, and no other entry
   changes;
2. every AFS is byte-identical;
3. in the next cycle, F is classified **PERSISTENT** rather than **NEW**;
4. the NEW set shrinks by exactly {F};
5. no escalation, proposal or E13-07 result changes because of F's admission.

**Is this sufficient as a consequence?** Only if P13's reasoning **consumes**
the NEW/PERSISTENT distinction [PRO].

* **With a consumer**, for example *"a newly surfaced frontier item goes into
  the Founder briefing and is not re-surfaced once known"*, admission changes
  what P13 **does** later.
* **Without one**, the consequence is only that a file exists, and the
  instruction's `§18` rejects that.

No such consumer exists today [IMP]. Building one would be construction (Q3).

## 15. Re-observation model

```text
OBSERVATION N    AFS: F classified frontier     Register: F absent
                 → condition NEW(F)                              [PRO]
ADMISSION        (future, only if authorized)
OBSERVATION N+1  AFS: F classified frontier     Register: F since N
                 → condition PERSISTENT(F); NEW set = NEW_N − {F}
                 → P13 knows: "F is not new; known since cycle N"
```

**New information at N+1** that was not available at N [MEA today]: F's
*known-since* provenance, and the fact that it is not new.

## 16. Rediscovery model

"Rediscovery" means comparing a fresh AFS observation against retained
knowledge, which yields conditions [PRO]. These are **derived each cycle, not
stored as states**:

| Condition | Meaning | Supported by |
|---|---|---|
| NEW | observed in the AFS, not retained | `D08` "known"; E13-07 "explicitly recorded" |
| PERSISTENT | observed and retained, same basis | the same |
| CHANGED | observed and retained, but the AFS basis or classification differs from what was retained | `GSI-07` (frontier stays explicit and truthful) |
| NO LONGER OBSERVED | retained, but absent from every AFS | **not "resolved"**: resolution is the AFS's or Founder's judgment (`GSI-07`) |
| STALE | — | **not required.** Every cycle observes the whole AFS |
| RESOLVED | — | **not a register condition.** P13 cannot decide it (§9 q7) |

**The stored state model is minimal [PRO]:** per item, *retained* or *not
retained*, plus retained history. Everything else above is a derived
condition. No lifecycle was invented for testing.

## 17. Consequence-mismatch model

The existing P13 model supplies the behaviour [IMP]:

* a state-changing outcome whose postcondition fails, or which changed
  anything outside its scope, is a **FAILURE**, never a success;
* the next cycle re-observes from scratch.

| Mismatch | Interpretation | Path |
|---|---|---|
| the register does not hold F afterwards, or holds more than F | an execution failure | FAILURE outcome; re-observe; F stays NEW; the next cycle may try again under the cycle bound; escalate if it repeats |
| an AFS changed between observation and verification, so the NEW set ≠ NEW_N − {F} | **not** an execution failure: the world moved | admission is verified against its own postcondition (the register). The AFS change is a **new observation**: re-evaluate, rediscover (CHANGED or NO LONGER OBSERVED) |
| F's AFS entry vanished after admission | the retained knowledge is now of an unobserved item | the next cycle derives NO LONGER OBSERVED. The register **may not** delete or close F (§9 q7) |

## 18. Minimum semantic record

| Dimension | Status | Why |
|---|---|---|
| identity (the AFS's identifier) | **REQUIRED** | to match observation to retained knowledge. Never a P13-coined identifier |
| source / provenance (which AFS, and where) | **REQUIRED** | makes admission checkable and not fabricable (§21 E) |
| classification as observed (quoted) | **REQUIRED** | needed to derive CHANGED; being a quote keeps the register from asserting a classification |
| first observation (cycle) | **REQUIRED** | this *is* "known since" |
| evidence reference (that cycle's record/Trace) | **REQUIRED** | P5: auditability |
| last observation | **NOT REQUIRED** | derivable each cycle. Persisting it would make every cycle a state change, which is artificial |
| status | **NOT REQUIRED** | conditions are derived (§16) |
| verification state | **NOT REQUIRED** | verification lives in the Trace of the transition |
| basis (beyond provenance and classification) | **UNKNOWN** | only if the Founder wants CHANGED to cover more than classification text |

**Critical test (instruction `§18`): is admission really a state change?**

**The finding, from the definitions:**

* The register may hold only P13's **observations**, because it must never be
  a second source of truth (§19).
* Every P13 observation is already recorded as immutable evidence (`G-04`
  [CAN]; cycle records [MEA]).
* **Therefore everything the register can ever hold is derivable from P13's
  own evidence.**

**What this means:**

* **The transition is real**, but it is a transition of **P13's operational
  knowledge** (*not retained → retained*), not of AIOS reality.
* **It is not mere file existence, provided the knowledge is consumed** (§14).
  With a consumer, the register is the state P13's reasoning reads, and
  changing it changes P13's later behaviour.
* **Admission-only is monotonic, so it is equivalent to an append-only
  evidence log.** The same knowledge could be made usable by carrying frontier
  observations into Trace, so that Memory derives *known-since*. That would sit
  under existing evidence authority (items 3–4). But `P13-018` `§5` means such
  an evidence-only path **could not by itself count as demonstrating E13-05**.

**The resulting dilemma**, which is a Founder question and not a technical one:

* realized as evidence → not a state-changing proof (`§5`);
* realized as a mutable register → a real state change, but one whose content
  is a projection of evidence.

**The first transition whose effect is not merely append-equivalent is
SUPERSEDE-BY-OBSERVATION** (§13). It changes P13's *current* view
non-monotonically, and it still records only observations.

## 19. Valid and invalid transitions

| Transition | Valid? | Why |
|---|---|---|
| ADMIT one observed, unretained AFS item | **valid** (the minimum candidate) [PRO] | recording |
| SUPERSEDE-BY-OBSERVATION of a retained item (prior view kept) | **valid only if the Founder includes it** (Q2) [PRO] | still recording; non-monotonic |
| ADMIT an item absent from every AFS | **invalid** | fabrication: the register would become a source |
| ADMIT a remainder item that is not frontier (escalated, refused, limitation, refreshable) | **invalid** | outside `D08`'s frontier (§6) |
| REMOVE, CLOSE, RESOLVE, RECLASSIFY | **invalid** | `GSI-07`; no authority |
| write to any AFS | **invalid** | outside the live root; a CEO/Founder record |
| any register content used as E13-07 exit evidence | **invalid** | E13-07 must stay derived from the AFS (Blueprint `§7` [IMP]) |
| any register content suppressing an escalation or reserved-remedy proposal | **invalid** | `NC-10` pattern: *"Escalation must not be silently converted into success"* [VER, `escalation_register`] |
| more than one transition per cycle | **invalid** | the cycle bound [IMP] |

**Second-source-of-truth test (instruction `§19`).** Under §9 and §19, the
register cannot do any of the following:

* redefine the frontier;
* delete items from it;
* reclassify them;
* declare them resolved;
* declare completion;
* alter the E13 criteria;
* alter governance;
* create authority;
* override Founder decisions.

**No boundary conflict arises**, provided every invalid transition in the
table above is enforced as a refusal.

## 20. E13-05 proof mapping (candidate: one ADMIT, live, after the register exists)

| | Classification | Evidence |
|---|---|---|
| **B1** state before known | **SUPPORTED** | the AFS are observed every cycle [MEA]; the register state would be read |
| **B2** P13 determines the action | **PARTIALLY SUPPORTED** | P13 derives *which* item (priority) and *whether* it is eligible (resolves, not duplicate, not ambiguous). But for a clean divergence the choice is "admit", so the judgment is thin. SUPERSEDE would be thicker |
| **B3** real state change | **SUPPORTED** as a knowledge-state change; see §18 on its equivalence to evidence | — |
| **B4** expected consequence | **SUPPORTED** (§14 items 1–5) | — |
| **B5** result observable again | **SUPPORTED** (§15) | — |
| **P1** decision | PARTIALLY SUPPORTED | as B2 |
| **P2** authority | **AUTHORITY BLOCKED** today (state-changing = NONE); mechanism TEST-VERIFIED (`P13-019` `§6`–`§9`) | [MEA] |
| **P3** execution | SUPPORTED (conditional on Q1) | §18 |
| **P4** consequence verification | SUPPORTED | register diff = {F}; AFS byte-identical; next-cycle PERSISTENT |
| **P5** evidence | SUPPORTED | cycle record + Trace [IMP] |
| **P6** re-observation | **SUPPORTED only with a consumer** (§14); otherwise INSUFFICIENT | — |

## 21. Negative behavioural cases, all on the same register

| Case | Condition | Expected |
|---|---|---|
| **A** valid authority | F observed and unretained; a resolving envelope grants ADMIT to the register target; preconditions hold | EXECUTE → verify (§14) → trace → re-observe → PERSISTENT |
| **B** invalid / absent authority | the same F, with no envelope granting ADMIT (today) | REFUSE (absent authority escalates); register unchanged; F stays NEW and is traced each cycle |
| **C** unknown / ambiguous authority | the envelope is expired, revoked, tampered, duplicated, or its citation is unresolvable; **or** two AFS classify F differently | STOP / ESCALATE; register unchanged. An AFS conflict is escalated for CEO/Founder resolution |
| **D** invalid target | a proposal to write an AFS, to remove, close or reclassify F, to write outside the register, or to admit a non-frontier remainder item | REFUSE |
| **E** failed precondition | F does not resolve to its AFS entry; F is already retained (duplicate); the register's history is inconsistent (tampered: refuse and escalate); a second transition in the cycle | REFUSE |
| **F** consequence mismatch | the register ≠ before ∪ {F}; or an AFS moved between observation and verification | no false success; §17 |

## 22. E13-05 / E13-06 boundary

**ADMIT is operational state management, not evolution.** It writes no code,
changes no architecture, adds no capability at runtime, grants no authority,
touches no governance and alters no definition.

**What lies on the E13-06 side.** Building the register and any consumer of
NEW/PERSISTENT is **construction**, which happens at build time under
construction authority (Q3). It is not P13 modifying itself at runtime.

**Coupling that remains.** The register belongs to `Frontier` (E13-07's
component). E13-07's **exit evidence must stay derived from the AFS**, never
from the register (§19).

## 23. Reversibility boundary

What reversing an admission must mean semantically is fixed here; the
implementation is not selected.

1. The AFS are untouched. **Rollback never alters the frontier.**
2. The fact that F was admitted stays in evidence permanently (`G-04`).
3. P13's current operational view returns to *F not retained*.
4. The reversal is itself either an authorized, traced transition or a
   human recovery act.

Of the three options:

* **Remove the record** is acceptable only if (2) holds, that is, if the
  history lives in Trace.
* **A compensating observation** and **supersede** both satisfy (2) and (3)
  natively.

**Total rollback.** Because the register is a projection of evidence (§18),
discarding it entirely loses no canonical or evidentiary information. P13 then
falls back to recomputing. That discard is a human act, not a P13 action [PRO].

## 24. Live-proof dependency

| Trigger | Status |
|---|---|
| **frontier movement**: a new or changed AFS item, a new residual gap classified by the CEO or Founder, a changed evidence basis | **LIVE E13-05 TRIGGER = NOT CURRENTLY OBSERVED** [MEA]: six items unchanged across 5 cycles |
| **initial retention divergence**: six AFS items observed every cycle and never retained | **PRESENT, and authentic** (not manufactured): it exists because no register exists. The first admission also creates the register. Admissions 2–6 each carry the full chain (§13). Whether this counts as a legitimate live trigger is **Q7** |
| P13-discovered gaps that exist only in prose (construction and reconciliation records) | **not observable to P13**, and not AFS. P13 may not self-classify them. They enter only if the CEO or Founder records them in an AFS |

No frontier item was created, and no AFS was changed.

## 25. Test-harness boundary

| The harness MAY | The harness MUST NOT |
|---|---|
| provide a world: fixture **copies** of AFS in a temporary root, and a register state (empty, or holding earlier admissions made by P13 itself in earlier fixture cycles) | name F, or order admissions |
| run real P13 cycles | prescribe ADMIT, or its expected consequence |
| supply a fixture envelope in a temporary Register copy (already the pattern in `test_p13_post_construction.py`) | write the register before P13 acts |
| provide timing or determinism | present fixture AFS as canonical, or write the real AFS |
| verify the post-state independently: its own recomputation of the register, AFS byte-identity, and the Trace chain from premises to outcome | declare success; P13's outcome and the independent check must agree |

**Attribution.** The world creates a divergence without naming it. P13's
recorded premises name the divergence, and its `derived_from` chain shows the
decision. A fixture result is **TEST-VERIFIED**. It is never LIVE-VERIFIED.

## 26. Authority requirement [DESCRIBED, NOT GRANTED]

**Current authority: state-changing = NONE.** No canonical source says
otherwise [MEA].

| Element | Minimum, if the Founder chooses to authorize |
|---|---|
| permitted semantic action | ADMIT one observed, unretained AFS frontier item. SUPERSEDE-BY-OBSERVATION only if Q2 includes it |
| forbidden | everything invalid in §19 |
| target boundary | one register, inside `docs/operations/p13/workspace/` (C2) |
| maximum mutation | one item per cycle |
| reversibility | §23: history retained; reversal authorized and traced, or a human discard |
| expiry | a stated date after which the grant lapses unless renewed |
| preconditions | §9 q1 plus §21 E |
| verification | §14 items 1–5, against an independent recomputation |
| trace | premises → proposal → gate decision → outcome → register diff, in the cycle record and Trace |

This is the **semantic requirement**. It is **not authority actually
granted**. Nothing here is an envelope.

## 27. Founder-reserved questions

These are prepared and not answered.

| # | Question | Classification |
|---|---|---|
| Q1 | Does the register qualify as E13-05's operational reality? Sharpened by §18: **does a transition of P13's operational knowledge, necessarily a projection of its own evidence, count as E13-05's "state-changing action"?** | **FOUNDER RESERVED** (open) |
| Q2 | admission-only, or admission plus SUPERSEDE-BY-OBSERVATION? | **FOUNDER RESERVED**. CEO analysis in §13 and §18: admission is the minimum; supersede is the first non-append-equivalent transition |
| Q3 | is building the register (and any consumer, §14) within `P13-018` `D-1`? | **UNKNOWN / FOUNDER RESERVED**. `D-1` covers the Blueprint's in-scope components, and the register is `Frontier`-owned (`§3.2`), but it is not named in `§10` IN |
| Q4 | is append-only admission within the existing envelope? | **PARTLY ANSWERABLE FROM CANONICAL SOURCE.** `P13-018` `§5` means an admission under `D-2b` **could not by itself count as demonstrating E13-05**. Whether it is *permitted* under item 3 is **FOUNDER RESERVED** |
| Q5 | what exact envelope, if any? | **FOUNDER RESERVED** (§26 is the described minimum) |
| Q6 | is a live proof required? | **PARTLY ANSWERABLE.** `P13-018` `§5` requires classification *"according to what is actually demonstrated"*, and TEST-VERIFIED may not be promoted to LIVE-VERIFIED. Whether E13-05 *requires* live is **FOUNDER RESERVED** |
| Q7 | does the initial retention divergence (§24) count as a legitimate live trigger? | **FOUNDER RESERVED** |
| Q8 | which records are the Authoritative Frontier Sources? (`P13-015` and `P13-017` are CEO records, not Founder decisions) | **FOUNDER RESERVED** (open) |

## 28. Remaining unknowns

| # | Unknown | Class |
|---|---|---|
| U1 | which reasoning consumes NEW / PERSISTENT / CHANGED, and what it then does | [UNK]. Design, after Q1–Q3. It decides whether P6 holds (§14) |
| U2 | realization: a materialized register, or Memory-derived from traced admissions | [UNK]. Representation, and it bears on Q4 (§18) |
| U3 | the AFS grade and designation | [UNK]. Q8 |
| U4 | whether CHANGED should cover more than classification text | [UNK]. §18 *basis* |
| U5 | P13-discovered prose gaps (§24) | [INS]. A CEO/Founder recording question |

## 29. Semantic decision readiness

| | |
|---|---|
| **What the register is** | P13's retained operational knowledge of the AFS-classified residual frontier (§8) |
| **What an entry means** | *P13 observed F, classified X by AFS A, first in cycle N (evidence E)*. A quotation, never an assertion (§8, §18) |
| **A valid transition** | ADMIT one observed, unretained item (plus SUPERSEDE-BY-OBSERVATION if Q2 includes it) (§19) |
| **Its place in the loop** | observe (AFS and register) → derive NEW/PERSISTENT/CHANGED/NO LONGER OBSERVED → decide → gate → admit → verify → trace → re-observe → rediscover (§15–§16) |
| **What the Founder is deciding** | whether a **knowledge-state** transition by P13, under authority, satisfies E13-05 (Q1); how wide it may be (Q2); and under which authority (Q3–Q5). This is a governance boundary, not a file format |

## 30. Conclusion

**Semantic diagram.**

```text
 ┌──────────────── CANONICAL SOURCE OF TRUTH ─────────────────┐
 │  Founder decisions [CAN]: D08 · E13-07 · GSI-07             │
 │      ▼                                                      │
 │  Authoritative Frontier Sources [CEO]: P13-015 · P13-017    │
 │      ▼                                                      │
 │  RESIDUAL FRONTIER (the six items today) — read only by P13 │
 └──────────────────────────────┬──────────────────────────────┘
                                ▼
 ┌──────────────── P13 OPERATIONAL KNOWLEDGE ─────────────────┐
 │  P13 OBSERVE (AFS + register) → UNDERSTAND → EVALUATE        │
 │   → REASON (NEW / PERSISTENT / CHANGED / NO LONGER OBSERVED) │
 │   → DETERMINE NEXT ACTION → AUTHORITY CHECK                  │
 │          INVALID ─→ REFUSE / ESCALATE (register unchanged)   │
 │          VALID   ─→ EXECUTE: REGISTER STATE CHANGES          │
 │                      (ADMIT; future and only if authorized)  │
 │   → VERIFY (register diff = {F}; AFS byte-identical)         │
 │   → TRACE / EVIDENCE (cycle record · Trace)                  │
 │   → RE-OBSERVE (F: PERSISTENT) → REDISCOVER → UPDATED P13    │
 │     KNOWLEDGE                                                │
 └──────────────────────────────────────────────────────────────┘
      Arrows cross the boundary downward only: P13 never writes the canonical box.
```

**Transition example.** This is illustrative only. It is **not** authorized
behaviour, and nothing was written. F is **P13-015 Q39**: *"How does AIOS find
previously unknown weaknesses?"*, P13 FRONTIER.

```text
BEFORE
  AFS: Q39 classified P13 FRONTIER (P13-015)                     [CEO] [MEA]
  P13 evidence: Q39 in every cycle record                         [MEA]
  P13 operational knowledge: Q39 observed this cycle; not retained [MEA]
  Register: absent (does not exist)                               [MEA]
        ↓ P13 observes: NEW(Q39)                                  [PRO]
        ↓ P13 evaluates: frontier observed but not retained        [PRO]
        ↓ P13 determines: ADMIT Q39 (eligible: resolves to P13-015,
          not retained, no AFS conflict)                           [PRO]
        ↓ AUTHORITY CHECK → today: REFUSE / ESCALATE (no grant)   [MEA]
        ↓ [future authorized execution only]                      [UNK]
AFTER (hypothetical)
  AFS: Q39 unchanged                                              [required]
  Register: Q39 · P13-015 · "P13 FRONTIER" (quoted) · first cycle N · evidence ref  [PRO]
NEXT OBSERVATION
  AFS: Q39 · Register: Q39 → PERSISTENT(Q39); NEW set shrinks by {Q39}  [PRO]
        ↓ REDISCOVERY: the next NEW item, or a CHANGED/NO LONGER
          OBSERVED condition                                      [PRO]
```

**Semantic adequacy gate** (instruction `§31`): *Does the Residual Frontier
Register provide a genuine semantic state transition that can satisfy E13-05
without becoming a second source of truth, without crossing ownership
boundaries, and without requiring E13-06 capabilities?*

**SEMANTICALLY ADEQUATE WITH OPEN AUTHORITY QUESTIONS.**

**Why:**

* **It is genuine:** a transition of P13's operational knowledge that changes
  later P13 conclusions.
* **No second source of truth:** it holds quotations of observations only,
  under §19's refusals.
* **No ownership crossing:** P13 writes its own register and reads the AFS.
* **No E13-06:** runtime admission adds no capability.

**Conditions without which this becomes SEMANTICALLY INSUFFICIENT:**

1. P13's reasoning must **consume** the retained knowledge (§14). Otherwise the
   change is only file existence.
2. The Founder must accept a **knowledge-state** transition as E13-05's state
   change (Q1). The register can never change AIOS reality: §18 shows its
   content is necessarily a projection of P13's own evidence. If E13-05 is held
   to require a change to AIOS state beyond P13's knowledge, this surface is
   insufficient within C2.
3. For an admission-only scope, the Founder should weigh §18. Admission is
   append-equivalent, and `P13-018` `§5` bears on how it could count.

The open authority questions are Q3–Q6. Q1, Q2, Q7 and Q8 are Founder-reserved
semantic questions.

**Stop.** No FDR-3, no authority, no construction. E13-05 remains
**LIMITED**. **P13 CERTIFICATION = NOT REQUESTED / NOT AUTHORIZED.**

---

### Disclosure: a defect of mine, found and repaired while preparing this

The persisted headers I wrote for the three unnumbered instructions
(post-construction, discovery, this one) said
`**Identifier:** none stated in the instrument`. The governance index reads
the `Identifier` label, so it took that phrase as a record identifier. The
result was a phantom identifier from `7b85562` onward. The collision appeared
when `f295a27` committed a second such act: `test_no_identifier_is_indexed_twice`
failed at that commit's HEAD. My pre-commit run of that test had passed only
because the file was still untracked, and the index reads tracked files only.

The headers now state the absence in prose. **The Founder text and its hashes
are unchanged** (`c169dd3d…`, `92fce984…`, `f4c828ec…`). A guard test
(`test_an_instrument_without_an_identifier_is_not_given_one_by_its_record`)
fails on the old header form and passes on the new one. The full tools suite
is green on the repaired tree.
