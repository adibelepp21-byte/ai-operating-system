# `ACT-CC-P12-027` — continuation return package

**Directive:** Founder — *CONTINUE ACT-CC-P12-027 · DO NOT CREATE ANOTHER ACT.*
No Act was created. Work continued under the existing authority.

**Baseline accepted as instructed:** `86c11c2` —
`§6.8` / `§6.9` / `§6.11` SATISFIED, `§6.7` / `§6.13` NOT SATISFIED,
`P12 COMPLETE = NO`.

```text
RESULT

§33  REFUSED   closed by construction     3 / 7  →  4 / 7
§6.13  NOT SATISFIED  →  SATISFIED
§6.7   NOT SATISFIED  →  NOT SATISFIED     (unchanged)
§6.14  NOT SATISFIED  →  NOT SATISFIED     (unchanged, rests on §6.7)

P12 COMPLETE = NO
```

---

## 1. What the directive asked, and where each answer is

| Priority | Surface | Answer |
|---|---|---|
| 1 | `§33` failure states | `P12-027-SECTION-6-7-FRONTIER-DETERMINATION.md §1`–`§4` |
| 2 | `§34` execution provenance | same, `§5` |
| 3 | `§31` workflow chain | same, `§5` — the **same eight executions**, not a second gap |
| 4 | `§30` runtime | same, `§3` — the **same root** as `VERIFIED`, not a third |
| 5 | `§35` self-model | same, `§7` — **already satisfied**; the finding filed under `§35` was `§26`'s |

Every finding carries CANONICAL REQUIREMENT / CURRENT STATE / EVIDENCE /
CLASSIFICATION / CLOSABLE WITHIN P12 / AUTHORITY / REQUIRED ACTION, with its
dependency evidence named as `§27` requires.

```text
CLASS A  1   §33 REFUSED                              — built
CLASS B  4   §33 BLOCKED · §33 VERIFIED · §30 verification · §34 live paths
CLASS D  3   §34/§31 eight historical executions · §26 corpus
CLASS E  1   §33 RETRYABLE
CLASS F  2   §35 self-model · the escalation delegation join
```

## 2. The one `A`, and why it was one

`§33` says only *"Failure behavior must distinguish"*. It names no record and no
field. **The record-level standard is not `§33`'s and is not the verifier's
invention either** — `§29` requires each material execution to **preserve** its
elements, and `§34` requires provenance to identify the **result**. That is
answer **(2)** to the directive's five-way question, not **(3)**.

Two sanctioned refusals — `EscalationRequired` (a *plan* exceeding its
authority) and `ExecutionRefused` (a *step* exceeding its delegation) —
persisted into a byte-indistinguishable record. `EscalationRecord` now carries
`refusal_type`, derived by `record()` from the raised exception and refused by
`__post_init__` for any name outside `SANCTIONED_REFUSALS`.

**The verifier was not touched.** `_refused()` is byte-identical to `86c11c2`,
and the closure criterion was written by an earlier Act:
*"the finding must close by itself once the record gains the field."*

**One consequence of the field was closed in the same change.** The `P12-W3`
governance-join beside the record already carried a `refusal_type` of its own,
so two surfaces now state one fact. `join_escalation_to_grant` refuses a join
that **contradicts** the record it sits beside — and does **not** refuse one
whose record is silent, because the three resident escalations predate the
field and *cannot check* is not *checked and found wrong*. Without that
asymmetry, adding the field would have retroactively made every historical
record unjoinable.

**Four prior declines were read before the field was built, not after.** Three
were workstream scope, which `ACT-CC-P12-027 §4` removes. The fourth called the
record *certified* — measured and not sustained:
`is_protected(tools/escalation_register.py)` is `False`, and `NATIVE CORE = 11`
does not reach `tools/`. Ordinary unfinished construction, which the directive
says not to call a hard boundary.

## 3. The decisions **not** taken, and why

Two readings were available that would have improved the count. Neither was
taken, by the same test `D-P12-027-02` was declined under.

- **`EscalationRequired → BLOCKED`.** Would close `§33`'s `BLOCKED` on a mapping
  `§33` does not make, of a term `§33` does not define, using a type whose own
  name is *escalation*. `_blocked()` is left exactly as it was.
- **`§6.7`'s *"has been completed"* as the activity rather than the result.**
  Prepared as **`D-P12-027-04`** and referred to the Founder. The Exit Contract
  uses *hold* three times within four lines of `§6.7` and does not use it there,
  which is a real argument — and taking it would move the contract to `14 / 0`
  and produce `P12 COMPLETE = YES` in one stroke. `§8` forbids choosing an
  interpretation because it produces PASS.

A cheap closure was also refused: adding `Affected surfaces:` and
`Verification:` labels to two new documents would move `§26`'s two `ABSENT`
elements to `PARTIAL` on a denominator of 440 — a status change bought with two
files and no change to the corpus. The module's own docstring forecloses it:
*"An element with no resident label at all is `ABSENT`… it is not closed by
inventing a label."* The population is the **tracked** governance corpus
(`git ls-files`), so a document that qualifies as a governance record enlarges
that denominator once committed rather than helping it.

## 4. Defects introduced by this work, disclosed

**One, found by the suite and fixed.** The `refusal_type` docstring named the
certified evidence roots by literal path. `test_p12_certified_evidence_guard`
selects modules to examine by searching source text for exactly those strings,
so the prose pulled `escalation_register.py` into the examined population and
its two legitimate `write_text` calls — which write to a caller-supplied root —
were reported as unguarded writers into certified evidence.

**The prose was changed, not the test.** The filter is deliberately coarse and
over-inclusive, which is what makes it fail safe; accommodating a docstring
would have narrowed a security conformance control to suit this Act.

**One incidental change to resident evidence, disclosed rather than reverted.**
Running `tools/p12_runtime_observation.py` re-took its observations, so
`aios-corpus-health*.observation.json` carry a new `observed_at` and `pid`. The
observed **states** are unchanged (`RuntimeState.STOPPED`,
`WorkflowState.SUCCEEDED`). That is the observer doing what it does when
invoked, not a rewrite of a finding.

## 5. Boundaries held

- No Act created. No Founder or human authority manufactured. No approval
  inferred from silence.
- No Trace vocabulary manufactured; `VALID_STATUSES` is untouched and so is
  `ExecutionOutcome`'s ratified three. No retry mechanism manufactured.
- No historical evidence rewritten. The three resident escalation records keep
  the shape they were written in, and a control asserts they do.
- No `docs/program/AIOS_*` package touched. No certified P10/P11 evidence
  modified. `NATIVE CORE = 11`.
- No runtime, daemon, scheduler, queue or self-activation.
- No trust anchor. No delegation issued. No corpus, namespace or interface
  manufactured.
- `R-A` and `R-B` not reopened — no fresh canonical evidence makes either a
  requirement.
- No P13 work and no P13 authorization.
- Nothing self-certified: `§57` reserves certification to the Founder.
