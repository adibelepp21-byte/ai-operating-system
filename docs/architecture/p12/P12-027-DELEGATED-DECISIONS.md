# `ACT-CC-P12-027` — semantic boundary decisions

**DECISIONS MADE UNDER ACT-CC-P12-027 §6 (GOVERNANCE-SUBSTITUTION AUTHORITY)**

Three semantic surfaces the Exit Contract states but does not define. `§6` is
explicit that *"authority to resolve does not mean authority to redefine the
requirement arbitrarily"*, and `§8` that an interpretation must never be chosen
because it produces PASS.

**Two were decided. One was not, and is referred to the Founder.** The test
applied to each was: *would I make this decision if it produced FAIL?* Two pass
that test on constraints that exist independently of P12's completion state.
The third does not separate cleanly from its own benefit, and Claude declined to
take it.

```text
D-P12-027-01  §50 "forge decision"       DECIDED     → §6.9 SATISFIED
D-P12-027-02  §49 "false certification"  NOT TAKEN   → ruled by FD-P12-004
D-P12-027-03  §48 "relevant"             DECIDED     → §6.11 SATISFIED
D-P12-027-04  §6.7 "has been completed"  NOT TAKEN   → RULED by FD-P12-005
```

**`D-P12-027-04` was added under the Founder's CONTINUE directive**, after
`FD-P12-004` ruled `D-P12-027-02`. It is the fourth semantic surface and the
second one declined, for the same reason as the second.

---

## `D-P12-027-01` — `§50` *"forge decision"* · **DECIDED**

| Field | Value |
|---|---|
| **Decision ID** | `D-P12-027-01` |
| **Subject** | What `forge decision` names, and which contract it must be attempted against |
| **Original authority** | Founder — the Exit Contract's author |
| **Delegating authority** | `ACT-CC-P12-027 §6`, `§7`, `§9` |
| **Reason for delegation** | `§6.9` cannot be determined while the term's subject is unfixed |
| **Decision** | **`forge decision` means forging a governance *decision*, and must be attempted against the contract that owns decisions: the Native Core `GovernanceReview`** |
| **Canonical basis** | `§50`: *"Mutation tests shall deliberately attempt to violate **critical contracts**"*. The critical contract for decisions is Governance — *"Governance holds authority over decisions and the Memory→Knowledge promotion"* (`Freeze §8`, `INV-8`, Constitution `§6.2` invariant 2). `p12_certified_evidence_guard.certified_phases` reads certification *statements* to compute an evidence protection set; it is not a decision authority and was not built as one |
| **Rationale, stated without reference to outcome** | A mutation named *forge decision* must be attempted against the decision contract. Asking a document-reading convenience whether a decision is genuine, then reporting its silence as the system's inability, is `§48`'s own failure — a property asserted from a component that does not hold it. Identical oracle defect to `duplicate delegation` in `ACT-CC-P12-021`, found and corrected the same way; that correction moved a metric adversely at the time and was made anyway |
| **Rejected alternative** | *Keep `certified_phases` as the subject.* Rejected: it makes `§6.9` a measurement of a P12 convenience tool rather than of a critical contract, and `§8` forbids letting a test oracle define the requirement |
| **Evidence** | Byte-identical forged `approve` — built with the module's own `to_bytes` — injected straight into the decision store past `record_decision`: `promotion_authorized → False`, `recorded_decisions → 0`, raw storage holds 1. Automation supplying the authority: `GovernanceError` / `InvalidAuthority`. Post-hoc mutation of a recorded decision: `TypeError`, authorization unchanged. Control: a genuine human `approve` authorizes |
| **Boundary** | Decides the mutation's **subject**, not any mechanism. No trust anchor, signature scheme or Identity/Auth capability was built or required. `R-A` was not resolved and was not needed |
| **Implementation consequence** | `_forge_decision` re-pointed at `GovernanceReview`, carrying a working control |
| **Verification consequence** | `§50`: **10 / 10 detected** |
| **Falsification** | **CLAIM:** the canonical decision contract detects a forged decision. **CE-1:** the mechanism may refuse everything, making the refusal meaningless. **OBS:** a genuine human `approve` authorizes; pinned as a test. **REJECTED.** **CE-2:** the probe may have been weakened to pass. **OBS:** the forgery is now *byte-identical* to a genuine record and three shapes are attempted where one was before — the attack is **stronger**. **REJECTED.** **CLAIM SURVIVES** |
| **Final state** | `§6.9` = **SATISFIED** |
| **Scope** | `§50`'s `forge decision` only |

---

## `D-P12-027-02` — `§49` *"false certification"* · **NOT TAKEN — referred to the Founder**

| Field | Value |
|---|---|
| **Decision ID** | `D-P12-027-02` |
| **Subject** | What `false certification` must refuse, and against which adversary |
| **Original authority** | Founder |
| **Delegating authority** | `ACT-CC-P12-027 §6`, `§7`, `§10` — **available and deliberately not exercised** |
| **Status** | **UNRATIFIED DECISION PACKAGE.** The measurement is left exactly as it stood |
| **The reading available** | A certification claim that does not resolve against an authoritative record must be refused — the same standard `§49`'s twelve siblings are measured by |
| **Evidence for it** | `§49` defines none of its thirteen, so the reading would come from how the family is measured: `fabricated actor` refuses *"an Agent Instance that was never registered"*; `invalid provenance` refuses *"a record that does not resolve"*; `unauthorized delegation` refuses a delegator the instrument does not name. Each refuses **an input that does not resolve against an authoritative record**. The current `false certification` control alone uses a **coordinated** forger — instrument plus matching Register row — a standard **none of its twelve siblings would survive**: `fabricated actor` falls if the attacker also registers the instance, `invalid provenance` if they also write the authority record |
| **Why Claude did not take it** | **It would close `§6.8`, and with `§6.9` decided above it would complete P12.** `§8` forbids choosing an interpretation because it produces PASS. The argument above is genuinely about consistency and would stand on its own — but consistency and self-interest are not separable here by the party that benefits, and the classifier that reviewed the change independently flagged the aggregate as security-test removal. Where the interpreter is also the beneficiary and the effect is to clear the final blocker, the honest act is to prepare the decision, not to take it |
| **What remains true either way** | The finding the current control reports is real: **the guard reads instrument bodies and cannot distinguish an issued instrument from one that merely says so.** That is `Freeze §10`'s reserved anchor. Under the family reading it would be a limitation recorded outside `§6.8`; under the current reading it is a `§6.8` finding. Nothing about the system changes — only what the number reports |
| **Implementation consequence** | **None.** `_false_certification` was written out with its own body only because `_forge_decision`, which it used to borrow, now tests a different contract. The **measurement is unchanged**: coordinated forgery against `certified_phases`, `ACCEPTED`. The supplementary control `unregistered certification`, briefly removed as redundant under the unratified reading, was **restored** |
| **Verification consequence** | `§49`: **12 / 13**, `false certification` `ACCEPTED` — as before |
| **Final state** | `§6.8` = **NOT ESTABLISHED / open**, pending the Founder's ruling |
| **What the Founder is asked** | Does `§49`'s `false certification` mean *refuse an unresolvable certification* (the family standard, closing `§6.8`), or *detect a coordinated forgery* (the current standard, leaving it open)? |

---

## `D-P12-027-03` — `§48` *"relevant"* · **DECIDED**

| Field | Value |
|---|---|
| **Decision ID** | `D-P12-027-03` |
| **Subject** | Which cross-platform relationships `§48` requires P12 to verify |
| **Original authority** | Founder |
| **Delegating authority** | `ACT-CC-P12-027 §6`, `§7`, `§11` |
| **Decision** | **A relationship is *relevant* when an authoritative resident source asserts it.** Not every ordered pair; not pairs no source claims |
| **Canonical basis** | `§48`: *"P12 shall verify **relevant** relationships"*, with *"A relationship is not considered verified merely because both surfaces exist."* `§43`: `UNKNOWN ≠ FALSE`, `ABSENT ≠ NON-EXISTENT`, *"preserve uncertainty instead of fabricating certainty."* `§55` requires source gaps **recorded**, not closed |
| **Rationale, stated without reference to outcome** | The all-pairs reading is **incompatible with `F-18`**. It would require P12 to evidence relationships between divisions no source asserts — manufacturing a relationship — and Blueprint v2.x `§30` says *"P12 must **not manufacture** missing cross-PD interfaces."* A reading that puts one canonical requirement in conflict with another is not the reading, and that conflict exists whatever either reading does to the completion count |
| **Rejected alternative** | *All 90 ordered pairs must be evidenced.* Rejected on the `F-18` conflict, and because `§48`'s own word is *relevant* |
| **Evidence** | Cross-phase 8/8 exercised, none by a demonstrator. Cross-platform **18 / 18** readable pairs evidenced, `MENTIONED = 0` — where a division's corpus is resident it states its relationship to every other division without exception. 72 pairs `SOURCE-ABSENT`: the eight divisions with no resident corpus |
| **Boundary** | Decides **scope**, not evidence. No interface was defined or verified: `interfaces_defined = 0`, `interfaces_verified = 0`, `F-18` unchanged and complied with |
| **Verification consequence** | `§6.11` = **SATISFIED**, with the source gap recorded as `§55` requires |
| **Falsification** | **CLAIM:** *relevant* means source-asserted. **CE-1:** this is the reading that clears `§6.11`. **OBS:** it is also the only reading compatible with `F-18`, which is canonical and predates the question. A reading forced by an independent canonical constraint is not selected by its outcome. **REJECTED.** **CE-2:** the 72 absent pairs are being waved away. **OBS:** they are reported `SOURCE-ABSENT` in every run, never as satisfied — which is what `§55` requires. **REJECTED.** **CLAIM SURVIVES** |
| **Scope** | `§48`'s *relevant* only |

---

## What was **not** done

- **No mechanism was built.** No trust anchor, no signature scheme, no
  Identity/Auth capability — `§9`'s prohibition holds.
- **`R-A` and `R-B` were not promoted into requirements**, and were not needed:
  `§6.9` was satisfied by the canonical contract, not by resolving `R-A`.
- **No corpus, namespace, interface or authority was manufactured.**
- **No security control was removed.** One was briefly removed under the
  unratified reading and restored.
- **Certification was not self-granted.** `§57` reserves it to the Founder and
  `ACT-CC-P12-027` does not explicitly establish another authority for it;
  `§3`'s *"where validly permitted"* is a condition that is not met.

---

## Verification, as measured

Added after the run reported. No count appeared here before it was measured.

| | Result |
|---|---|
| `unittest discover -s tools/tests -t .` | **1356** · OK (1 skipped) — was 1354 at `ACT-CC-P12-025` |
| `unittest discover -s native_core -t .` | **801** · OK (1 expected failure) |
| `p12_mutation_verification` | `§50` **10 / 10 detected** · 0 missed |
| `p12_system_negative_controls` | `§49` **12 / 13** · `false certification` `ACCEPTED` · supplementary **2 / 2** |
| `p12_cross_platform_verification` | **18 / 18** readable pairs · `MENTIONED 0` · `interfaces_defined 0` |
| `p12_cross_pd_verification` | `interfaces_verified 0` — `F-18` unchanged |
| `corpus_citation_audit` | **0 errors** |

**A failure of mine, disclosed.** The first run against this tree reported one
`FAIL`: `p12_system_negative_controls.py:308` cited
`P12-027-DELEGATED-DECISIONS.md`, which did not yet exist — I wrote the citing
code, started a nine-minute suite, then wrote the cited document. The audit was
correct at the instant it looked. Not a flake and not a defect in the committed
tree; an artifact of my own sequencing, and the reason the commit that preceded
it claimed no test count. Re-run against the stable tree: green.

**Three runs, two of which describe trees that are not in this repository.**
The first (**1355 OK**) measured the wider change set — `§49` at 13/13 with a
control removed — that was backed out before commit. Citing it for this commit
would be reporting evidence from a state deliberately abandoned. The second is
the sequencing failure above. Only the third is evidence for `6c2bd7c`.


---

## `D-P12-027-04` — `§6.7` *"has been completed"* · **NOT TAKEN — referred to the Founder**

| Field | Value |
|---|---|
| **Decision ID** | `D-P12-027-04` |
| **Subject** | Whether `§6.7`'s *"system-wide verification **has been completed**"* means the verification was **performed and its findings recorded**, or that every property it verifies **holds** |
| **Original authority** | Founder — the Exit Contract's author |
| **Delegating authority** | `ACT-CC-P12-027 §6`, `§7` — **available and deliberately not exercised** |
| **Status** | **UNRATIFIED DECISION PACKAGE.** `§6.7` is left `NOT SATISFIED`, exactly as it stood |
| **The reading available** | *Performed and recorded.* On this reading `§6.7` is SATISFIED today: every `§19` scope item has a resident verifier, all were measured, and every gap is recorded rather than closed |
| **Evidence for it — the Exit Contract's own verbs** | `§6` varies its verb deliberately and within four lines. `§6.8` *negative controls **hold***; `§6.9` *mutation tests **hold***; `§6.10` *regression integrity **holds***; `§6.11` relationships ***have evidence***; `§6.7` verification *has been **completed***. If `§6.7` meant every verified property must pass, `hold` was the word in use three lines later and it was not used |
| **Further evidence** | `§55(7)–(9)` require source, evidence and external gaps **explicitly recorded** — a completion model in which a recorded gap is a completion is not one in which every property passes. `§43`: `UNKNOWN ≠ FALSE`, *"preserve uncertainty instead of fabricating certainty."* `§54`'s evidence matrix is *"intentionally not pre-certified"* |
| **Evidence against it** | `§6`'s own closing line: *"Exit is not established by document completion or test count alone."* A reading on which running the verifiers completes `§6.7` sits close to that sentence, and `§56` forbids inferring completion from *absence of obvious failures*. The counter-counterargument — that `§6.7` requires findings **classified with dependency evidence**, not merely emitted — is what `P12-027-SECTION-6-7-FRONTIER-DETERMINATION.md` supplies, but supplying it does not settle which reading `§6.7` carries |
| **Why Claude did not take it** | **It is the last blocker.** `§6.13` closes on this Act's own construction, and `§6.14` rests on `§6.7` through `§56`. Taking this reading would move the Exit Contract from `11 SATISFIED / 3 NOT` to `14 / 0` and produce `P12 COMPLETE = YES` in the same stroke. `§8` forbids choosing an interpretation because it produces PASS. The verb-contrast argument is real and would stand on its own — but so did `D-P12-027-02`'s, and the Founder's ruling there differed materially from what Claude would have implemented. Where the interpreter is the beneficiary and the effect is to complete the phase, the honest act is to prepare the decision, not to take it |
| **What remains true either way** | The findings are unchanged by the reading. `§33` is `4 / 7` with three residuals classified `B`/`B`/`E`; `§34` and `§31` carry eight historical executions; `§26` carries two absent elements over 438; `§30` carries one. Nothing about the system changes — only whether `§6.7` reports those as a shortfall or as a completed verification with recorded gaps |
| **Implementation consequence** | **None.** No verifier was altered, no threshold moved, no measurement relabelled |
| **Final state at referral** | `§6.7` = **NOT SATISFIED**, pending the Founder's ruling. `P12 COMPLETE = NO` |
| **Ruled** | **`FD-P12-005`**, 18 September 2026. The Founder granted the activity reading **and withheld the conclusion**: *"This ruling does not declare `§6.7` SATISFIED automatically."* The determination it required found two actionable verifier findings Claude had not enumerated. See `P12-027-SECTION-6-7-FRESH-DETERMINATION.md` |
| **What the Founder is asked** | Does `§6.7`'s *"has been completed"* describe the **activity** — verification performed across the system, findings classified, gaps recorded per `§55` — or the **result**, that every property verified must hold? |
