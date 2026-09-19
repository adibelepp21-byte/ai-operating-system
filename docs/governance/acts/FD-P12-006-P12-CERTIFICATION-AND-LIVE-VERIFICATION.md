# `FD-P12-006` — Founder Decision · P12 Certification & Live Operational Verification

**Document type:** Founder Decision Record
**Phase:** P12 — System Integration / Unified Operational State / System-wide Verification
**Decision:** CERTIFY P12
**Status:** FINAL / ISSUED — SUBJECT TO LIVE VERIFICATION RECORD
**Founder:** Moriarty
**Date:** 18 September 2026

---

## Provenance

The body below `§ RECORD` is the Founder's, persisted **verbatim**. The
surrounding material is Claude's and is separated for that reason.

This instrument certifies P12 **conditionally**: `§24` issues the certification
and `§9`–`§20` state the condition. The live verification it requires was
executed against the commit `§2` names and is recorded in
[`P12-LIVE-OPERATIONAL-VERIFICATION-RECORD.md`](../../architecture/p12/P12-LIVE-OPERATIONAL-VERIFICATION-RECORD.md).

**Certification is the Founder's act, made in `§24`.** Claude performed the
verification the act was conditioned on and reports that the condition is met;
it does not grant the certification. `§57` of the Blueprint and `§8` of this
instrument both hold.

**The live test found two things and neither is a completion contradiction.**
One is a genuine isolation gap in a resident work path; one is an invocation
error of Claude's that the system refused correctly. Both are recorded in the
verification record's `§D` rather than resolved silently, as `§22` requires.

---

# § RECORD — issued by the Founder, verbatim

FD-P12-006

FOUNDER DECISION RECORD — P12 CERTIFICATION & LIVE OPERATIONAL VERIFICATION

Document Type: Founder Decision Record
Phase: P12 — System Integration / Unified Operational State / System-wide Verification
Decision: CERTIFY P12
Status: FINAL / ISSUED — SUBJECT TO LIVE VERIFICATION RECORD
Founder: Moriarty
Date: 18 September 2026

1. DECISION

The Founder recognizes the P12 completion determination established against the current repository state and authorizes P12 Certification, subject to completion of the explicit live operational verification defined in this record.

The certification basis is:

P12 COMPLETE = YES
P12 EXIT CONTRACT = 14/14 SATISFIED
P12 CONSTRUCTION = COMPLETE / EXHAUSTED
P12 CERTIFICATION = PENDING LIVE VERIFICATION

Certification shall not be inferred merely from the completion record or test count.

2. PRIMARY COMPLETION EVIDENCE

The primary technical completion state is the repository state represented by:

278e48c

The completion evidence associated with this state includes:

tools             1366 OK (1 skipped)
native_core        801 OK (1 expected failure)
consumers          276 OK
falsifiability      36 / 36 demonstrated
citation audit       0 errors
stale-state          0
protected package    unchanged

The repository was reported clean at the completion state.

These figures are evidence supporting the certification review.

They are not, by themselves, sufficient grounds for certification.

3. P12 EXIT CONTRACT

The final P12 determination reported:

14 SATISFIED
0 NOT SATISFIED
P12 COMPLETE = YES

The Founder accepts this as the current P12 completion determination, subject to the live verification specified below.

The certification review must preserve the distinction:

VERIFICATION ACTIVITY COMPLETE
≠
ALL FINDINGS RESOLVED

P12 contains remaining open findings.

Those findings were determined not to be independent P12 completion conditions.

They must remain recorded and owned rather than silently removed or converted into completion failures.

4. FOUNDER RULINGS INCORPORATED

This certification incorporates the Founder rulings previously applied during P12 completion, including:

D-P12-027-02

false certification is interpreted as:

refusal of a certification claim that cannot resolve against an authoritative certification record.

It is not interpreted as a requirement for P12 to detect a coordinated forgery capable of reproducing the entire certification/trust surface.

D-P12-027-04

§6.7 "has been completed" refers to completion of the verification activity/process required by §6.7, including verification, classification, and gap recording.

It does not implicitly require every property examined by the activity to be resolved or PASS.

These interpretations were applied to implementation and verification rather than merely changing reported numbers.

5. E12 AUTHORITY BASIS

The completion determination's E12 requirement basis is recorded as:

ACT-CC-P12-019 §7

This authority is distinct from:

FD-P12-003

which remains a signed but unfilled Founder Decision template.

No claim shall be made that FD-P12-003 contains Founder selections that were never entered.

The certification record must preserve this provenance distinction.

6. OPEN FINDINGS

The following findings remain open and are not erased by certification:

§33 residual escalation vocabulary limitations
§34 historical provenance assembly limitation
§31 historical execution/workflow relationship limitation
§30 runtime verification vocabulary limitation
§26 governance corpus findings
§46 UNKNOWN cells
§48 undefined cross-PD interfaces

Their respective ownership and authority boundaries remain unchanged.

Certification of P12 does not constitute certification of those external, historical, architectural, or governance matters.

7. R-A / R-B STATUS

The following remain outside the P12 completion requirement:

R-A = supporting verification / Identity-Auth dependency
R-B = supporting verification / cross-PD dependency

They must not be represented as P12 certification blockers.

Certification does not resolve either matter.

Certification does not authorize construction of either matter.

8. P12 CERTIFICATION BOUNDARY

Certification means:

The Founder recognizes that P12's canonical completion requirements have been demonstrated according to the current authoritative completion determination.

Certification does not mean:

* every AIOS finding is resolved;
* every PD is complete;
* every interface exists;
* Identity/Auth is complete;
* all historical evidence is reconstructable;
* all Trace vocabulary is complete;
* all governance corpus gaps are resolved;
* P13 is authorized.

9. LIVE PHASE 12 VERIFICATION

Before final certification is marked irrevocably complete, execute a live operational verification of P12 against the exact repository state associated with the completion determination.

The purpose is to demonstrate that P12 is not merely a collection of documents and passing tests.

The live test must exercise the actual integrated system.

10. LIVE TEST PRINCIPLE

Use:

REAL SYSTEM WORK
→ OBSERVATION
→ VERIFICATION
→ EVIDENCE
→ PERSISTENCE
→ FRESH REDISCOVERY

Do not use:

test-only demonstrator
→ simulated completion
→ certification

A live test must exercise resident P12 behavior through its actual integration path.

11. LIVE TEST — P12 END-TO-END PATH

Execute at least one genuine P12 work path through:

INTENT
→ DECISION
→ WORK
→ EXECUTION
→ OBSERVATION
→ VERIFICATION
→ EVIDENCE

The live run must demonstrate the actual relationships established by P12.

Capture:

1. input intent;
2. resulting decision;
3. work object;
4. execution context;
5. runtime/execution observation;
6. verification result;
7. evidence produced;
8. provenance;
9. governance state where applicable;
10. persisted records.

No manually fabricated result may be substituted for any of these.

12. LIVE SELF-MODEL TEST

Exercise the P12 Self-Model against the live system.

The live system must answer, using actual current state:

What am I?
What do I own?
What authority do I have?
What capabilities exist?
What is running?
What changed?
What is stale?
What is unknown?
What decisions are recorded?
What failed?
What is incomplete?
What is authoritative?

The answers must be derived from actual system state rather than hard-coded demonstration output.

Record the result as evidence.

13. LIVE KNOWLEDGE / MEMORY TEST

Exercise the P12 integration between Knowledge and Memory.

Perform a real operation requiring:

Knowledge
+
Memory
+
Execution
+
Verification

Demonstrate that removing or withholding either component produces the expected system-level consequence.

Do not claim consumption merely because a component exists.

Demonstrate:

EXISTS
→ CONSUMED
→ REACHABLE
→ USED

where the canonical requirement requires it.

14. LIVE GOVERNANCE / DECISION TEST

Execute one legitimate decision path through the canonical decision mechanism.

Demonstrate that:

authority
→ decision
→ execution consequence

remains consistent.

Do not use a forged or test-only decision as the positive control.

Where a negative control is required, use the canonical P12 semantics already established by D-P12-027-02.

15. LIVE EXECUTION / VERIFICATION TEST

Exercise the actual execution integration.

Demonstrate:

WORK
→ EXECUTION
→ OBSERVATION
→ VERIFICATION
→ EVIDENCE

using real system work.

Do not manufacture an interface merely for the test.

Do not require unresolved R-A or R-B dependencies unless the canonical P12 Exit Contract explicitly requires them.

16. LIVE FAILURE / REFUSAL TEST

Exercise at least one legitimate refusal/failure path.

Demonstrate that the resulting escalation record preserves the required material information, including the now-established refusal semantics.

Verify that the governance join does not contradict the actual escalation record.

The test must use the current EscalationRecord behavior.

17. LIVE NEGATIVE-CONTROL TEST

Execute the P12 negative-control suite against the live/current system.

The test must distinguish:

negative behavior demonstrated

from:

live system property

Do not convert synthetic negative demonstrations into claims about live incidents.

Record both separately.

18. FRESH-PROCESS TEST

Restart the relevant runtime/process boundary.

Repeat the minimum P12 observation path from a fresh process.

Verify that the result does not depend on transient in-memory state from the previous run.

Record:

fresh process
→ same canonical state
→ same relevant determination

where required by the P12 evidence contract.

19. LIVE PHASE COHERENCE TEST

Exercise all Phase relationships required by P12.

The test must verify that the live work path can traverse the integrated Phase surfaces without treating:

Phase
=
Platform Division

as the same taxonomy.

Do not manufacture PD interfaces.

Do not infer ownership from numbering.

20. LIVE EVIDENCE RECORD

Persist one:

P12 LIVE OPERATIONAL VERIFICATION RECORD

containing:

* exact commit SHA;
* date/time;
* test invocation;
* real work performed;
* observations;
* outputs;
* evidence identifiers;
* fresh-process result;
* negative-control result;
* failures/refusals;
* deviations;
* repository state;
* conclusion.

The record must be reproducible from the repository.

21. CERTIFICATION GATE

After the live test, perform one final fresh determination.

Certification may be marked:

P12 CERTIFIED = YES

only if:

1. P12 COMPLETE remains YES;
2. the canonical Exit Contract remains satisfied;
3. live verification demonstrates the integrated P12 operating path;
4. no material contradiction exists between completion evidence and live evidence;
5. no new completion blocker has been discovered;
6. all evidence is persisted;
7. the repository state is clean and identifiable;
8. certification itself remains within Founder authority.

22. FAILURE OF LIVE TEST

If the live test discovers a genuine P12 completion contradiction:

P12 COMPLETE = NO

must be reconsidered from the actual canonical Exit Contract.

Do not hide the contradiction.

Do not modify the test merely to preserve certification.

Do not declare certification despite contradictory evidence.

If the live test discovers only an external/open finding that is not a P12 completion condition, record it without reopening P12 construction.

23. NO P13 EFFECT

Nothing in this Founder Decision authorizes P13.

Maintain:

P12 CERTIFIED = YES/NO
P13 AUTHORIZED = NO

as independent states.

P13 requires its own canonical authorization chain.

24. CERTIFICATION DECISION

Subject to successful completion of the live verification defined in this record:

FOUNDER DECISION:
P12 CERTIFICATION = CERTIFY

The certification is based on:

P12 completion evidence
+
canonical Exit Contract determination
+
Founder rulings
+
live operational verification

not on test count alone.

25. FINAL FOUNDER AUTHORITY

Founder: Moriarty

Decision: CERTIFY P12

Certification Condition: Successful live P12 operational verification and final fresh reconciliation as specified by this record.

P12 Construction: COMPLETE / EXHAUSTED

P12 Completion: YES

P12 Certification: PENDING LIVE VERIFICATION

P13 Authorization: NO

Signature: Moriarty

Date: 18 September 2026

Status: FINAL / ISSUED

26. FINAL DIRECTIVE

Claude Code shall execute the live P12 verification defined herein against the actual completion state.

Do not manufacture evidence.

Do not convert test count into operational proof.

Do not reopen P12 merely because an open finding exists.

Do not suppress a genuine contradiction.

After the live test, perform one fresh P12 determination and return:

P12 LIVE VERIFICATION = PASS / FAIL
P12 COMPLETE = YES / NO
P12 CERTIFIED = YES / NO
P13 AUTHORIZED = NO

with exact evidence and commit SHA.

END OF FD-P12-006

---

# § APPLICATION — what the live verification actually produced

**The condition in `§9`–`§20` was executed against `278e48c`, the commit `§2`
names, with the repository clean at the start.** Nine live tests ran through
resident entry points invoked by hand. No demonstrator was written; no result
was chosen.

| `§` | Test | Result |
|---|---|---|
| 11 | end-to-end `INTENT → … → EVIDENCE` | a real execution, 7 / 7 edges joined, read back by an independent reader |
| 12 | self-model | 12 questions · 10 verified · 2 inferred · **0 unknown** |
| 13 | Knowledge / Memory | live `HEALTHY`; Knowledge withheld → `WITHHELD`; Memory withheld → fails closed |
| 14 | governance decision | a real Founder instrument → Active Knowledge version → the `§13` consequence |
| 15 | execution / verification | 5 / 5 chains joined · 0 dangling |
| 16 | failure / refusal | a real refusal; the first resident escalation carrying `refusal_type`; join agrees |
| 17 | negative controls | live `§49` **13 / 13 refused**; driven falsifiability **36 / 36** — recorded separately |
| 18 | fresh process | 8 / 8 reproduced, including the self-model answer |
| 19 | phase coherence | 8 / 8 exercised; two taxonomies kept apart; `interfaces_defined 0` |

## The two findings, and why neither reopens P12

`§22` distinguishes a completion contradiction from an open finding. Both of
these are the second kind, and both are recorded rather than repaired quietly.

1. **A resident work path cannot be exercised in isolation.**
   `aios_corpus_health_run.run()` parameterises its stores but not its
   observation root, so two driven runs published `RUNNING` into the resident
   observation surface and one died before its terminal publish. **The system
   caught it immediately** — `What is running?` answered `UNKNOWN` with the
   reason *"a stale record cannot establish current state"*. Remedied by
   **re-observing**, never by editing a file, and the intermediate `UNKNOWN` is
   preserved in the record.
2. **The `§28` chain is not atomic.** An invocation error of Claude's reached a
   correct refusal — `record()` would not overwrite an existing manifest — after
   the delegation, trace record and observation had already been persisted. One
   more execution now carries no manifest, which is the same kind of finding as
   the historical ones already classified `D`.

**`§34` moved from `7 / 15` to `8 / 19` as a consequence**, and that is stated
plainly: the proportion worsened, the kind of finding did not change, and
reporting only the second half would have been flattering.

## Compliance with `§26`'s prohibitions

| Prohibition | Compliance |
|---|---|
| Do not manufacture evidence | Every artefact was produced by a resident entry point. The one addition to a resident script was a fifth **execution identity**, needed because `record()` refuses to overwrite a manifest; the work it performs is the same real conformance verification, and its outcome (3 of 14 criteria satisfied) was recorded, not chosen |
| Do not convert test count into operational proof | The suite figures appear only as identification of the tree. Every `§21` condition is answered from a live run or a relation verifier |
| Do not reopen P12 merely because an open finding exists | Neither finding reopened construction; both are recorded under `§22`'s second branch |
| Do not suppress a genuine contradiction | The two findings, the `UNKNOWN` interval, the adverse `§34` movement and the corrected control are all in the record |

## Result

```text
P12 LIVE VERIFICATION = PASS
P12 COMPLETE          = YES
P12 CERTIFIED         = YES   — by §24, its condition satisfied
P13 AUTHORIZED        = NO    — §23, independent
```

Full evidence:
[`P12-LIVE-OPERATIONAL-VERIFICATION-RECORD.md`](../../architecture/p12/P12-LIVE-OPERATIONAL-VERIFICATION-RECORD.md).
