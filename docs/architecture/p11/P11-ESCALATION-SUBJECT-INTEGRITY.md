# Escalation Same-Subject Idempotency & Organizational State Integrity

> **Executed under `ACT-CC-P11-014`** — 2026-09-11.
> **The reported defect was mine, and it is falsified.** The investigation found
> a different one, in the other half of the same frontier, and repaired that.
>
> Native Core = **11** · protected packages = **13 untracked, UNTOUCHED** ·
> no new entity · no new authority · no new Agent Instance · no new consumer ·
> `E11 RATIFIED = FALSE` · `P12 AUTHORIZED = FALSE`.

---

## A. Executive result

The Act names a **two-part** frontier — *"Escalation same-subject idempotency
**and** organizational state integrity"* — and the investigation returned a
different result for each part. Both are stated; the one answering `§4`'s
PRIMARY QUESTION is marked.

| Part | Classification | |
|---|---|---|
| Same-subject idempotency | **`E4` — FALSE POSITIVE / DUPLICATION INTENTIONAL** | **← answers `§4`** |
| Organizational state integrity | **`E2` — EXISTING MECHANISM, INCORRECTLY WIRED** | proven and repaired |

**`E4`, exact reason.** There is no canonical escalation identity to deduplicate
on, because there is **no canonical escalation entity**. The ratified Canonical
Domain Model `§10` lists *Escalation / Incident* among *"Deferred concepts. Not
canonical entities in v1.0."* — deferred precisely because *"escalation is
adequately handled procedurally via the existing Decision-Making Process plus
Trace's success/failure/escalation status field — **no dedicated entity required
yet**."* `DP-04 §7`, an **ISSUED Architect Decision**, fixes the same placement:
*"Escalation is represented as a ratified Trace status rather than an
independent organizational entity."* And the semantics of that surface are the
opposite of idempotent — Domain Model `§7` invariant 4, *"production is
unconditional, never optional"*, and invariant 5, *"Trace is immutable and
append-only; once written, never edited or deleted."*

Two identical refusals are **two occurrences**, and recording both is what an
append-only occurrence surface does. Suppressing the second is what `DP-01`
`NC-10` forbids: *"Escalation must not be silently converted into success."*

**`E2`, exact reason.** `tools/w1_coordination_run.py` **constructed no
escalation register at all**. A W1 coordination refusal would have survived only
as a string in `evidence["refusals"]` — an outcome transient to one run, with no
lifecycle, no accountable party and no way to resolve. That is verbatim the
condition `ACT-CC-P11-009 §13` identified and fixed **on the W4 path only**;
this module was written afterwards and did not carry the fix.

---

## B. Canonical escalation model, reconstructed (`§9`)

```text
W4 / W1 EXECUTION
      ↓  step outside the delegation            producer: W4Executor
REFUSAL  (ExecutionRefused | EscalationRequired) authority: none — it is a stop
      ↓  record_refusals(root, refusals, …)      producer: the run path
ESCALATION RECORD  <id>.escalation.json          persistence: append-only file
      ↓  status derived, never stored            OPEN  ⟺ no response file
HUMAN RESPONSE  <id>.response.json               requires HumanAuthority
      ↓                                          status: ANSWERED — never APPROVED
CONTINUATION governed elsewhere                  authority: the instruments governance issues
```

| Transition | Producer | Authority | Failure behaviour |
|---|---|---|---|
| refusal → record | run path via `record_refusals` | none created | non-sanctioned error refused; unvalidated citation refused |
| record → persisted | `EscalationRegister.record` | none | refuses to overwrite an existing file |
| OPEN → ANSWERED | `record_response` | **`HumanAuthority` only** | any non-`HumanAuthority` refused; second response refused |
| ANSWERED → anything | **does not exist** | — | there is no method that closes, approves or resolves |

`§9`'s required distinctions, each enforced rather than described:

- `W4 REFUSAL ≠ ESCALATION CREATION` — the refusal is an exception; it becomes
  organizational state only when a run path records it, and `SANCTIONED_REFUSALS`
  is an explicit type list, not duck-typing.
- `ESCALATION CREATION ≠ ESCALATION APPROVAL` — nothing in the module closes one.
- `ESCALATION OPEN ≠ GOVERNANCE DECISION` — `status()` returns `OPEN`/`ANSWERED`
  and the only occurrence of the string `APPROVED` in the module is the line
  forbidding it.
- `HUMAN RESPONSE ≠ AUTOMATIC SYSTEM AUTHORIZATION` — `ANSWERED` says a human
  responded, not what they decided. No caller can read permission out of it.

**Lifecycle owner (`§14`).** The **record set on disk** owns lifecycle: status is
*derived* from which files exist, not stored in a mutable field. No projection,
observer or reader is the owner — `w4_continuity.reconstruct()` reads escalations
and reports `open_escalations` as a **continuation condition**, never acting on
it. `DETECTION ≠ AUTHORITY` holds because the detector has no method that could
change anything.

---

## C. Same-subject definition (`§10`)

**There is none, and none was invented.**

`subject` is a free-form string the caller supplies — today
`f"plan {plan.key} / delegation {delegation.delegation_id}"`. It is **provenance
text, not an identity**: no canonical body defines it, nothing validates it, and
two runs of the same plan under different grants produce different strings while
naming the same governance question.

`§10` is explicit: *"Do not silently invent a composite key."* Any uniqueness
constraint would require choosing one — blocked action, authority frontier,
underlying delegation, originating execution — and **each choice is a different
governance semantic**, deciding which recurrences count as the same unresolved
matter. Choosing one for implementation convenience is exactly the substitution
this Act forbids.

Making escalation a *"structural, queryable state"* with identity is the Domain
Model's own stated trigger for promoting it out of the backlog. That is an
Architect/Founder act, and `DP-04 §7` has already placed it the other way.

**So if one-open-per-subject is wanted, it is `E5`, not engineering.** Reported,
not taken.

---

## D. Actual duplication (`§12`)

Reproduced through the exact register call the W4 path makes, at a **temporary
root**. It is **not** a real W4 run and is not reported as one — see `§G`.

```text
OBSERVED DUPLICATION   : YES   two records, two ids, two OPEN, from identical input
REPRODUCIBLE           : YES   deterministic; payloads identical but id and timestamp
THEORETICALLY POSSIBLE : YES
CANONICALLY FORBIDDEN  : NO    no resident body states a uniqueness rule
CANONICALLY ALLOWED    : YES   Domain Model §10 + DP-04 §7 place escalation on an
                               append-only surface whose production is unconditional
```

**These five are reported separately on purpose.** Collapsing them is how the
claim arose in the first place: `ACT-CC-P11-013 §G` observed that ids are
`uuid4` with no dedup, and wrote *"would duplicate an open human-reserved
escalation"* — true as mechanism, and stated as though *theoretically possible*
and *canonically forbidden* were the same field. They are not, and only one of
them was ever checked.

### Falsification gate (`§11`)

| | Question | Result |
|---|---|---|
| `F1` | similar text, different subject | **stay distinct** — nothing collapses |
| `F2` | same subject, repeated | **two OPEN occurrences** — duplication real |
| `F3` | resolved, then recurs | new `OPEN` record; the `ANSWERED` one unaffected |
| `F4` | lifecycle states that exist | exactly `OPEN` and `ANSWERED` — no `RESOLVED`/`REJECTED`/`CLOSED`/`EXPIRED` |
| `F5` | different provenance | separate record |
| `F6` | fresh process | identical reconstruction; **no in-memory dedup exists to be fooled** |

`F4` matters more than it looks: the Act asks about behaviour under `CLOSED` and
`EXPIRED`. **Those states do not exist**, and inventing them to answer the
question would have been the same error as inventing a subject key.

---

## E. Existing mechanisms found (`§13`)

Searched before building anything.

| Mechanism | Where | What it guards |
|---|---|---|
| overwrite refusal | `record()` | **id-collision idempotency** — a record is never written over |
| response append-only | `record_response()` | **response idempotency** — a second answer is refused |
| derived status | `status()` | no mutable flag that could be set to approved |
| type gate | `SANCTIONED_REFUSALS` | only a refusal actually raised may become state |
| provenance gate | `AuthorityProvenance` check | a citation, not a string |
| human gate | `HumanAuthority` | automation cannot close an escalation |
| continuity read | `w4_continuity.reconstruct()` | open escalations reported as a blocking condition |

**The register already has idempotency exactly where canon requires it —
append-only — and deliberately not where canon does not.** That asymmetry is the
design, not an omission.

### Population completeness (`§23`)

Discovered before any count was asserted: escalation records can live under
**either** operational root. Both were enumerated. `w4-operations` holds one;
`w1-operations` holds none — **and the reason it holds none is not that W1 never
refused. It is that W1 could not have recorded one.** A count taken without
checking the wiring would have read an empty population as a healthy one.

---

## F. Construction (`§16`)

Minimum repair for `E2`. No new mechanism, no new entity, no new authority, no
subject key.

**Created**

| File | What |
|---|---|
| `tools/tests/test_escalation_subject_integrity.py` | 38 tests — `§20` controls, `§21` mutations, `§22` false-positive, canonical grounding |

**Modified**

| File | Why necessary |
|---|---|
| `tools/escalation_register.py` | `record_refusals()` — **one** wiring path from refusal to organizational state, reusing `EscalationRegister.record` |
| `tools/w1_coordination_run.py` | had **no** register; now records refusals and carries `escalations` in its evidence |
| `tools/w4_first_run.py` | routed through the shared path so there is one wiring, not two copies |

**Why no broader change.** No idempotency was added — `§34`: *"DO NOT REPAIR THE
HYPOTHESIS."* No subject key, no lifecycle states, no new statuses, no change to
`EscalationRegister`'s public surface, and the open human-reserved escalation was
not touched.

**Why two copies were collapsed into one.** W1 came to have no wiring precisely
because the W4 fix lived inline in the W4 module, where nothing carried it
across. One shared path is a place a control can fire; two inline copies is a
place a third can be forgotten.

---

## G. Verification

```text
tools       705 OK   (was 667 — +38)
consumers   276 OK
native_core 801 OK   (1 expected failure)
citation audit  167 documents / 0 errors
stale-state     478 documents / 0 assertions
W3 catalog 0 defects · W3↔ledger reconciliation 0 defects
```

**Real run.** `w1_coordination_proof.py` executed on the resident Runtime:
`proof_level: REAL-RUNTIME`, `subsystem_injected: false`, terminal
`WorkflowState.SUCCEEDED`, `refusals: []`, and the new `escalations: []` key
present. Rotation `94a4df7aca4543ef → 4daebea9012d4cc7` with the W3 projection
following, 0 reconciliation defects. **The reserved escalation `23f315ba…`
remained exactly one record, still `OPEN`.**

**What was deliberately not run, and why (`§19`).** The W4 first-execution proof
was **not** re-run. Its refusal path writes into the resident operations
directory, so a real repetition would add a second record about a
**Founder-reserved open escalation** — mutating governance state to test a
hypothesis, which `§24` forbids. The repetition was therefore performed through
the same register call at a temporary root and is labelled **canonically
equivalent, not real-runtime**. `§19`: *"Do not manufacture a substitute that
falsely claims to be real runtime evidence."*

A W1 refusal could not be induced either: `run()` takes no plan, and its two
steps are exactly its delegated work scope. The W1 wiring is therefore proven at
the helper behaviourally and at the call site by AST, and that is stated as what
it is rather than implied to be more.

**`§20` controls — all ten, each on an enduring invariant.**

| | Control | Asserted |
|---|---|---|
| 1 | same-subject repeated | two occurrences; payloads agree but for id and time; the helper adds no suppression |
| 2 | different subject | similar text stays distinct; both refusal types distinguishable |
| 3 | resolved then recurs | new `OPEN`; answering one occurrence does not answer another |
| 4 | stale reference | unknown id fails closed on `status`, `load`, `record_response` |
| 5 | missing escalation | an evidence-named id with no record is recoverable as **absent** |
| 6 | invalid provenance | unsanctioned error refused; unvalidated citation refused; helper inherits both |
| 7 | unauthorized response | `None`, a string, a bare object and an `AuthorityProvenance` all refused; stays `OPEN` |
| 8 | duplicate persistence | second response refused; the original claim survives byte-identical |
| 9 | fresh process | separate interpreter agrees on open set and statuses |
| 10 | human authority | no method name contains approve/authorize/permit/grant/resolve/close |

**`§21` mutations — all eight fired; none failed to fire.** Applied to **state
and inputs**, not to module source: a source-rewriting probe of mine has produced
a false verdict by four distinct mechanisms in this programme.

| Mutated | Control fired |
|---|---|
| subject identity | records diverge |
| active-state filtering | a planted response moves the id out of `open_escalations` |
| deduplication lookup | asserted **absent** — acquiring one later fails loudly |
| persistence | deleting the record makes `status` fail closed |
| provenance | `None`, a bare string and `0` all refused |
| lifecycle state | planting and removing a response flips `ANSWERED`/`OPEN` |
| human-authority requirement | a duck-typed object with `reviewer_id` is refused |
| fresh-process reconstruction | a second interpreter records a second occurrence |

**`§22` false-positive controls.** The `E2` wiring check is read by **AST**: a
substring search for `record_refusals` would match the import, a comment, or the
test's own docstring — the class that has produced five false conclusions here
already. It is itself mutation-tested against a modified copy of the source.
Every population these tests measure is one they created; none asserts *"there is
one file"*, *"the count is expected"*, or *"the directory is empty"* about the
resident corpus.

**Canonical grounding, re-read every run.** Five controls assert the exact
sentences the `E4` classification rests on, from the ratified Domain Model,
`DP-04` and `DP-01`. If a future edit changes what those documents say, the
classification stops being supported and the suite fails — the difference between
a classification and a memory of one.

---

## H. Governance

- **No authority created.** `record_refusals` records; it decides nothing.
- **No Founder boundary crossed.** Escalation `23f315ba9f504272` remains `OPEN`,
  unmodified, un-duplicated, and unanswered.
- **No Architect boundary crossed.** `DP-04 §7`'s placement of escalation as a
  non-entity is preserved — the repair depends on it rather than working around
  it.
- **No `E11` change, no `P12` change, no Native Core #12.** Core = 11.
- **Human escalation semantics preserved.** `record_response` still requires
  `HumanAuthority`; there is still no `APPROVED`.
- **`§24` intact.** Nothing auto-resolves, auto-approves, suppresses a legitimate
  escalation, or mutates governance state to satisfy idempotency — and the reason
  is structural: **no idempotency was added.**

---

## I. Protected boundary

```text
protected paths touched : 0
```

The 13 untracked `docs/program/AIOS_*` paths were not read, inspected, staged,
committed, modified, renamed, relocated, deleted, normalized or persisted, and
**their existence was not used as evidence for anything in this Act** (`§25`).

---

## J. Global P11 rediscovery (`§28`)

Measured from disk after the repair.

| Package | State | Evidence |
|---|---|---|
| **W1** Coordination | satisfied | real Runtime run this Act — `REAL-RUNTIME`, `SUCCEEDED`, 0 refusals |
| **W2** Planning | satisfied | `PLAN → SEQUENCE → ADAPT → REVISE`; prioritization reserved and structurally absent |
| **W3** Delegation | satisfied | 3 records, 0 catalog defects, 0 reconciliation defects, 2/2 active represented |
| **W4** Execution | satisfied | bounded, revocable, provenance-bearing; 13/13 on first real execution |
| **W5** Continuity | satisfied | both roots reconstruct; no duplicate-active, no unreadable records |
| **W6** Performance | satisfied | detect-only; no approval-shaped key in any result |
| **W7** Governance boundary | satisfied | one `OPEN` human-reserved escalation, correctly blocking |

Cross-surface relations checked: `W3 ↔ ledger` (0 defects), `evidence ↔
escalations` in both roots (**0 dangling, 0 orphan**), `grants ↔ instances` (all
recipients registered), `instances ↔ Agent Definitions` (both resolve),
`W5 ↔ both roots` (coherent; the only blocking condition is the reserved
escalation, correctly reported).

---

## K. Exhaustion status

```text
NOT EXHAUSTED — RESERVED FRONTIER
```

No **actionable** frontier was found by the rediscovery sweep. What remains is
reserved, optional, or a source gap:

| | Item | Class |
|---|---|---|
| 1 | One-open-per-subject escalation semantics | **`E5` — Architect/Founder.** Requires promoting a deferred Domain Model concept into a structural queryable state, against `DP-04 §7` |
| 2 | Prioritization / ranking / decision heuristics | Architect-reserved — `DP-01 §2`, `§3 W2`, `NC-08` |
| 3 | Escalation `23f315ba9f504272` | Human-reserved — answering it widens a delegated scope |
| 4 | `E11` ratification · `P12` · Native Core #12 | Founder-reserved |
| 5 | Multi-agent coordination proof | Optional — permitted, not required |
| 6 | A `governance-artifact-integrity` consumer | Optional — the canonical implementer is the Agent Definition, and it exists |
| 7 | Co-Founder Delegation Charter | Source gap — non-resident, and modification excluded from this delegation |
| 8 | `ACT-CC-P11-008`…`014` not persisted to `docs/governance/acts/` | Source gap — their coded verdict scales remain unreadable |

**`§29` observed.** No new work was invented to avoid exhaustion. The sweep
returned no actionable frontier, and the correct response is to stop building —
not to search for another gap.

---

## L. Next authorized state

**The P11 Exhaustion / Completion / Certification Gate is the next frontier.**

`§30` is not satisfied by this Act alone, and is not claimed: exhaustion requires
all remaining items classified, reserved items preserved, optional items not
misclassified as required, source gaps recorded, protected boundaries intact and
no unauthorized construction — all of which this document reports, but the
determination itself is a gate, not a side effect of a successful Act.

Item 1 above is the only item that would change escalation behaviour, and it is
`E5`. **It is reported, not constructed.**
