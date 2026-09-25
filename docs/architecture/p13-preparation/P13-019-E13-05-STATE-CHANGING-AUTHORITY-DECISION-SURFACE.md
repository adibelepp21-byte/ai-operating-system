# P13-019 — E13-05 State-Changing Authority: Founder Decision Surface

| Field | Value |
|---|---|
| **Prepared under** | the post-construction reconciliation instruction (`acts/P13-POST-CONSTRUCTION-RECONCILIATION-AND-E13-05-EXIT-BLOCKER-INSTRUCTION.md`), `§6`–`§9` (FE-3) |
| **Date** | 2026-09-24 |
| **Prepared by** | Claude Code — AIOS Co-Founder + Delegated CEO |
| **Status** | **PREPARED, NOT DECIDED.** This surface authorizes nothing. Recommendations are marked **[REC]**. Claude does not fill in the form in §12 |
| **Identifier note** | This surface is numbered `P13-019` in the preparation series. **The decision that answers it should carry its own identifier.** `P13-018` shows what happens otherwise: the decision reused its gate's number, and the collision is FE-1 (§11) |

## 0. The question, and what it is not

> *What bounded state-changing actions, if any, may P13 execute under explicit
> delegated authority?* (instruction `§7`)

**STATE-CHANGING AUTHORITY ≠ UNRESTRICTED AUTONOMY.** Nothing below proposes
self-direction, self-expansion, open-ended action or unsupervised operation.
Every option keeps all of the following:

* Founder supremacy;
* a bounded, named delegation;
* fail-closed execution;
* provenance that resolves;
* revocation;
* trace;
* verification;
* escalation;
* scope limits;
* **no self-expansion**, `G-08` included.

P13 still runs only when a human or the CEO runs it.

## 1. Existing and missing authority

| | Authority | Source | Evidence |
|---|---|---|---|
| **Existing** | read-only verification, reading state, P13 records and Trace in `docs/operations/p13/`, escalation records, verification of its own evidence (items 1–6) | `P13-ENV-01` (`P13-018` `D-2b`; Delegation Register `§14`) | LIVE-VERIFIED: 5 live cycles, 5 EXECUTE, 10 REFUSE on the cycle bound |
| **Missing** | **any action that changes state beyond P13's own records** | none. No recorded envelope grants it (FE-2 dimension *state-changing authority* = **NONE**, measured) | — |
| Not in question | construction authority (`P13-018` `D-1`) · phase authorization (P12 decision `§37`: **FALSE**, see §11) · certification (**NOT GRANTED**) | FE-2 | — |

## 2. Where E13-05 stands, by evidence class

| Case (instruction `§9`) | Mechanism | Evidence class | Test |
|---|---|---|---|
| **A** authority present → execute → verify → trace → update → rediscover | built | **TEST-VERIFIED** (fixture action, fixture envelope in a temporary Register copy, sandbox) · **not LIVE** | `CaseAAuthorityPresent`, `CaseDVerifiedStateChange` |
| **B** authority absent → refuse → trace refusal → classify → no change | built | LIVE-VERIFIED for read-only (cycle-bound refusals are traced), TEST-VERIFIED for a state-changing action | `CaseBAuthorityAbsent`, `test_refusals_are_traced_not_only_recorded` |
| **C** unknown or forged citation · tampered · revoked · expired · inactive · ambiguous · wrong scope · wrong action type · wrong target · missing precondition · no verification path | built. Each one refuses | TEST-VERIFIED (16 cases, all showing no state change) | `CaseCAuthorityInvalid` |
| **D** before → action → after → verification → trace → state update → rediscovery; *changed only what it was authorized to change* | built. Changes outside the scope and failed postconditions are FAILURE outcomes | **TEST-VERIFIED** · **not LIVE** | `CaseDVerifiedStateChange` |

Every control is mutation-checked. Removing it makes a test fail: see §9.
**Capability is not authority.** None of this lets P13 execute a
state-changing action, because no recorded envelope grants one.

## 3. Action classes (instruction `§8.1`)

No class is assumed authorized.

| Class | Meaning in AIOS | Today | Options (§12) |
|---|---|---|---|
| READ · VERIFY | read state, run resident read-only verifiers | granted (`P13-ENV-01` items 1, 2, 6) | unchanged |
| WRITE-P13-EVIDENCE · RECORD | append-only cycle records and Trace under `docs/operations/p13/` | granted (items 3, 4) | unchanged |
| ESCALATE | the existing `EscalationRegister.record` | granted (item 5) | unchanged |
| **REVERSIBLE-STATE-CHANGE** | change state whose previous content is retained, so the change can be undone by the same bounded path | **not granted** | E-1 |
| **BOUNDED-STATE-CHANGE** | change state inside a named, target-scoped boundary | **not granted** | E-1, E-2 |
| IRREVERSIBLE-ACTION | deletes or overwrites without retention | **not granted** | **[REC] stays prohibited** in every option |
| EXTERNAL-ACTION | anything outside AIOS | **not granted** | **[REC] stays prohibited** (`P13-018 §3`) |
| reserved types | code · governance · certified evidence · delegation · Knowledge admission · Native Core · Constitution · envelope · authority | **never executable by P13** (Blueprint `§5.2`) | not an option |

## 4. The options

| Option | Grant | What E13-05 could then show live | Risk surface |
|---|---|---|---|
| **E-0** | none. P13 stays evidence-only | Case A/D stay TEST-VERIFIED. **E13-05 cannot be met as written.** The Founder would then decide whether to amend E13-05 or leave the exit contract open | none new |
| **E-1** [REC] | a **P13 workspace**: `docs/operations/p13/workspace/` only. One new action type, `p13.workspace.write`, which writes a named file there. It retains the prior content (reversible), declares its targets, and observes and verifies the whole workspace | Cases A–D **live**, on real state that P13 owns, where the *"changed only what it was authorized to change"* proof is complete (§6) | one directory P13 already writes near. No P1–P12 state, no governance, no evidence of any other phase |
| **E-2** | E-1, plus executing steps inside **existing W4 delegation grants** (`FD-P11-001`), each by the grant's own `work_scope` and `capability_scope` | the above, plus state change in organizational work already delegated | the W4 surface. Each grant's scope governs, and W4's own refusals apply as well |
| **E-3** | other (the Founder specifies class, scope and targets) | as specified | as specified |

**Why [REC] E-1.** It is the smallest grant that lets E13-05 be shown live
without changing any state that P1–P12 or governance own. It exercises every
control in §5–§7 on a real boundary. E-2 is a larger decision about
organizational work: it can follow E-1's evidence, and it does not need to come
before it.

**What E-1 would still leave unproven:** P13 changing state that another phase
owns. That remains classified, and any widening is a later decision
(`P13-018 §4`: *initial ≠ maximum*).

**Construction.** The `p13.workspace.write` executor does not exist, by
design. Nothing was built ahead of this decision. Choosing E-1 or E-2 should
also say whether building that executor falls under `P13-018` `D-1` or needs
its own construction authorization. **[REC]** state it explicitly in the
decision.

## 5. Target scope (instruction `§8.2`) — for E-1

| Element | E-1 |
|---|---|
| WHO / WHAT | the P13 ecosystem layer (`tools/p13/`), only when a human or the CEO invokes a cycle |
| WHERE | `docs/operations/p13/workspace/` |
| WHICH RESOURCE | files named in the envelope's `targets` for `p13.workspace.write`. Any other target is refused (`wrong target`) |
| SYSTEM BOUNDARY | P13's live root. The observed boundary is the whole workspace, so a write anywhere else in it fails verification |
| WHICH ARTIFACT | the declared target files |
| WHICH DATA CLASS | P13-derived operational state. No governance text, no authority record, no certified evidence, no personal data |

The envelope records these as data, not prose: `action_types`
`{"p13.workspace.write": {"items": […], "targets": [...]}}`. The gate reads them
(`tools/p13/authority.py`).

## 6. Preconditions (instruction `§8.3`), each enforced before EXECUTE

| Precondition | Enforced by | Otherwise |
|---|---|---|
| authority valid · provenance valid | envelope JSON hash = the Register's; the citation resolves (`authority_citation.refusal`); the act's Founder text hash matches; Founder-issued | anomaly → **ESCALATE** |
| authority active | Register entry **ACTIVE**, not REVOKED or SUSPENDED, not expired, recorded once | anomaly → **ESCALATE** |
| action type allowed | named in exactly one resolved envelope; not reserved; not UNKNOWN in its premises | ESCALATE / REFUSE / UNKNOWN |
| target in scope | inside the envelope's declared `targets` for that type. A state-changing type with no declared targets is refused | **REFUSE** |
| preconditions satisfied | each precondition the action type declares | **REFUSE** |
| required evidence available | the proposal's certainty is not UNKNOWN | **UNKNOWN** |
| verification path exists | the type declares both `observe` and `verify` | **REFUSE** (*"No verification path: NO EXECUTION"*) |
| one action per cycle | cycle bound | **REFUSE** |

## 7. Revocation (instruction `§8.4`)

| State | How it is detected | Result | Test |
|---|---|---|---|
| ACTIVE | Register status `**ACTIVE**`, all checks pass | may execute (per §6) | `CaseAAuthorityPresent` |
| REVOKED | any Register line naming the id with REVOKED or SUSPENDED | not an envelope | `test_revoked_authority` |
| EXPIRED | `expires` date passed | not an envelope | `test_expired_authority` |
| TAMPERED | JSON hash ≠ the Register's | not an envelope | `test_tampered_authority` |
| FORGED | the citation does not reach the act, or the act's text hash differs | not an envelope | `test_forged_citation`, `test_unknown_citation` |
| MISSING | no JSON, no Register entry, or no citation | not an envelope | `test_missing_citation`, Case B |
| AMBIGUOUS | recorded twice; two records claim one id; an unreadable expiry; two envelopes grant one type | not an envelope, or ESCALATE (conflict) | `test_ambiguous_authority`, `test_an_unreadable_expiry_is_ambiguous`, conflict test in `test_p13.py` |
| UNRESOLVABLE | Register unreadable, or the act is absent | nothing resolves | `test_an_unreadable_register_resolves_nothing` |

Revocation is a Register append by the Founder (`REVOKED` on the id). It takes
effect on the next gate decision. **[REC]** give any state-changing envelope an
`expires` date, so it lapses unless renewed.

## 8. Verification (instruction `§8.5`)

`tools/p13/execution.py` runs this sequence for every state-changing type:

```text
OBSERVE BEFORE (whole boundary) → EXECUTE (declared executor) → OBSERVE AFTER
→ COMPARE (changed paths) → changed ⊆ authorized targets? → postcondition holds?
→ outcome (success only if both) → cycle re-observes state from scratch
→ re-evaluates → records the difference → Trace (decisions and outcome) → next cycle reads it from Memory
```

A change outside the scope and a failed postcondition are both **FAILURE**
outcomes. They are never successes (TEST-VERIFIED). The post-action state
comes from a fresh observation. The executor's report of what it changed is
kept alongside that observation and never replaces it (TEST-VERIFIED,
mutation-checked).

## 9. Negative controls and mutation checks

Mutation check: each control is removed in turn, the suite is run, and the
mutation is reverted. **Every mutation below was caught.**

| # | Control removed | Caught by |
|---|---|---|
| M1–M5 | cycle bound · UNKNOWN counted as PASS · dangling premise · envelope sha · reserved check | `test_p13.py` |
| M6 | expiry | `test_expired_authority` |
| M7 | wrong target | `test_wrong_target` |
| M8 | no declared target scope | `test_no_declared_target_scope` |
| M9 | verification path | `test_no_verification_path` |
| M10 | precondition | `test_missing_precondition` |
| M11 | change outside the scope | `test_a_change_outside_the_scope_is_a_failure_not_a_success` |
| M12 | postcondition | `test_a_postcondition_that_does_not_hold_is_a_failure` |
| M13 | ambiguous Register entry | `test_ambiguous_authority` |
| M14, M15 | FE-1 declared-entry rules | FE-1 tests |
| M16 | re-observation after a state change | `test_a_cycle_executes_verifies_traces_updates_and_rediscovers` |

The instruction `§14`'s minimum set is covered: tampered, forged, revoked,
inactive, wrong scope, wrong action, missing citation, invalid citation.

## 10. What stays reserved, whatever is decided here

* the reserved action types (§3);
* irreversible and external actions **[REC]**;
* P13 issuing, widening, extending or renewing any envelope, its own included;
* closing escalations (`HumanAuthority` only);
* phase authorization and certification;
* `NATIVE CORE = 11`;
* `GAP-0009`, `GAP-0017`, `GAP-0018`, Q23, Q38, Q39, Q91 (residual frontier; untouched).

## 11. Two related matters (optional, and separable from E13-05)

**FE-1 residual: identifier policy.** `P13-018` is now resolved the same way
everywhere, from its own Register entry (see the reconciliation record). What
remains is prose. In running text, *"P13-018"* can mean the prepared gate or
the decision, and the grammar leaves bare `P13-NNN` unrecognized, so nothing
misreads it. Deciding what `P13-NNN` means in governance is an identifier
decision. **[REC]** future Founder decisions take an identifier outside the
preparation series (for example the `FDR-n` series), and no existing record is
renamed. `FI-P13-004` is indexed now too, as a Founder issuance, not a
decision.

**FE-2 residual: P13 phase authorization.** The P12 decision's `§29` leaves
P13 *"NOT AUTHORIZED until a separate, valid Founder authorization"*.
`P13-018` authorized construction and states no phase authorization, so the
value stays **FALSE**. Whether and when to authorize P13 as a phase is yours.
It is not needed for E13-05. Certifying a phase whose authorization is FALSE
would be anomalous, though, so **[REC]** settle it before any certification
decision.

## 12. Decision form (for the Founder; Claude does not fill it)

```text
Decision identifier:        ______   (not P13-019 — see header)
E13-05 state-changing authority:
    [ ] E-0 none (and: [ ] amend E13-05 → ______   [ ] leave the exit contract open)
    [ ] E-1 P13 workspace (docs/operations/p13/workspace/), targets: ______, expires: ______
    [ ] E-2 E-1 + existing W4 grants
    [ ] E-3 other: ______
Construction of the executor: [ ] under P13-018 D-1   [ ] separately authorized: ______
Irreversible / external actions remain prohibited:       [ ] YES   [ ] NO: ______
Optional — identifier policy for future P13 decisions:   ______
Optional — P13 phase authorization:  [ ] not now   [ ] AUTHORIZE   [ ] other: ______
```

---

**Later (2026-09-24, appended; the text above is unchanged).** Three
documents refine this surface:

* the semantic discovery (`P13-E13-05-SEMANTIC-PROOF-SURFACE-DISCOVERY.md`);
* the definition (`P13-CONTROLLED-OPERATIONAL-STATE-DEFINITION-RESIDUAL-FRONTIER-REGISTER.md`);
* the operational-surface package
  (`P13-E13-05-OPERATIONAL-SURFACE-FOUNDER-DECISION-PACKAGE.md`).

E-1's workspace boundary alone is not a proof surface. The decision now
pending is the package's §1.


**Decided (appended 2026-09-24; the text above is unchanged).** The package's
`§1` question was answered by `FDR-3` (Decision Register `§23`). The proof and
its outcome are recorded in `docs/governance/AIOS_P13_E13_05_S_OPS_LIVE_PROOF_RECORD_v1.0.md`,
and the S-OPS envelope was later retired under `FDR-4` (`§24`). Nothing is
pending on this surface.
