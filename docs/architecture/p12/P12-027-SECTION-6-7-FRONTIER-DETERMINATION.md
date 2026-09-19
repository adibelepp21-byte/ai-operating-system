# `§6.7` — frontier determination and ownership

**Authority:** `ACT-CC-P12-027` (Founder directive *CONTINUE — DO NOT CREATE
ANOTHER ACT*). No new Act is created by this record.

**Baseline accepted:** `86c11c2`. `§6.8` / `§6.9` / `§6.11` SATISFIED;
`§6.7` / `§6.13` NOT SATISFIED; `P12 COMPLETE = NO`.

```text
§33  4 / 7 distinguished   (was 3 / 7 — REFUSED closed by construction here)
§34  NOT ASSEMBLABLE       7 / 15
§31  chain_connected False WORK→EXECUTION by convention
§30  1 / 9 absent          runtime `verification`
§26  2 / 9 absent          affected surfaces · verification, over 440
§35  12 questions · 10 verified · 2 inferred · 0 unknown  — already satisfied
```

---

## 0. Two corrections to the record this continues

Both are stated first because the rest of this determination uses them.

**`§35` was the wrong section number.** `P12-FRESH-EXIT-CONTRACT-DETERMINATION.md
§2.5` headed the nine-element governance-evidence finding *"`§35` — governance
evidence"*. The nine elements are **`§26` Governance Evidence**. `§35` is
*P12-W5 — AIOS Self-Model*, and it is not the surface that finding measures —
`tools/p12_governance_evidence_verification.py` says `§26` in its own first
line. Corrected throughout below. The finding itself is unchanged; only its
citation was wrong.

**`§35` itself is not a `§6.7` shortfall at all.** Measured fresh:
12 questions · **10 VERIFIED · 2 INFERRED · 0 UNKNOWN**. No element is absent.
It is the surface `§6.6` carries, and `§6.6` is SATISFIED.

---

## 1. The question `§33` actually turns on

The directive required this to be settled before anything was built:

> *Determine independently whether each distinction is: 1. explicitly required
> by `§33`; 2. required by another canonical `P12` source; 3. merely inferred by
> the verifier; 4. dependent on a capability outside `P12`; 5. actionable.*

`§33` verbatim, entire:

```text
Failure behavior must distinguish:
RETRYABLE BLOCKED REFUSED FAILED ESCALATED SUCCEEDED VERIFIED
Retry must not create: duplicate authority; duplicate delegation;
duplicate execution; orphan state; false success.
```

**`§33` does not say where a state must be distinguishable.** It does not
mention a record, a field, or persistence. The verifier's standard — *"a state
is distinguished only if it can be reached AND told apart afterwards; the record
is what anyone reads later, not the traceback"* — is **not** in `§33`.

**It is, however, carried by two other canonical sections**, which is the
difference between a verifier's gloss and a verifier's inference:

- **`§29`** — *"Each material execution must preserve: intent; decision; work;
  actor; authority; scope; execution; observation; verification; evidence;
  provenance; lifecycle."* **Preserve** is a word about rest, not flight.
- **`§34`** — *"Execution provenance must identify, where applicable: … result
  …"* A refusal is the result of an attempted execution. A preserved result
  that cannot say which refusal it was is a result under-identified.

So the answer to the directive's question is **(2), not (3)**: the record-level
standard is not stated by `§33` and is not merely the verifier's invention
either — `§29`'s *preserve* and `§34`'s *result* carry it. `§8` of
`ACT-CC-P12-027` forbids a test oracle defining a requirement, and it does not
define this one; it measures a requirement two other sections state.

**Consequence, stated because it cuts the other way too.** The same reading that
makes `REFUSED` actionable makes `BLOCKED` and `VERIFIED` *not* closable, for a
reason that has nothing to do with effort. See `§3`.

---

## 2. `REFUSED` — **CLASS A**, closed by construction

| Field | Value |
|---|---|
| **Canonical requirement** | `§33` distinguish `REFUSED`; `§29` preserve; `§34` identify `result` |
| **Current state (before)** | `RAISED ONLY`. Two sanctioned refusals — `EscalationRequired` (a *plan* exceeding its authority) and `ExecutionRefused` (a *step* exceeding its delegation) — persisted into a **byte-indistinguishable** record shape. The distinction was drawn in flight, by exception type, and lost at rest |
| **Evidence** | `EscalationRecord` carried `escalation_id · subject · required · held · reason · authority · raised_at` — nothing naming which refusal occurred |
| **Classification** | **A** — a `P12` requirement, and actionable |
| **Closable within P12?** | **Yes, and it is now closed** |
| **Authority** | `ACT-CC-P12-027 §4`. See the boundary check below |
| **Action taken** | `EscalationRecord` gained `refusal_type`, derived by `record()` from `type(error).__name__` and refused by `__post_init__` for any name outside `SANCTIONED_REFUSALS` |

### 2.1 The boundary that had to be checked first

Three prior packages declined exactly this field, and a fourth called it
reserved. Their reasons were read before it was built, not after:

| Source | Reason given | Status now |
|---|---|---|
| `P12-W4-EXECUTION-INTEGRATION.md §13` | *"`EscalationRecord` is a frozen, written-once governance surface… `ACT §30`: `W4 ≠ W3`"* | **Workstream scope.** `ACT-CC-P12-027 §4`'s No-Micro-Act Rule removes the partition the decline rested on |
| `P12-W2-UNIFIED-OPERATIONAL-STATE.md §11` | *"`ACT §44`: do not repair W3 from W2"* | Same |
| `P12-005` | closed the joinable part **beside** the record instead | Complementary, and left intact |
| `P12-016-RETURN-PACKAGE.md` | *"requires a field on the certified, frozen `EscalationRecord` — **RESERVED** (P11-certified surface)"* | **Checked and not sustained.** See below |

**Is the record certified or frozen? Measured, not assumed.**

```text
p12_certified_evidence_guard.protected_roots()
  docs/architecture/platform-organization
  docs/architecture/p11
is_protected(tools/escalation_register.py)  →  False
```

`NATIVE CORE = 11 FROZEN BOUNDARIES` fixes Native Core; `tools/` is not Native
Core, and `EscalationRecord` is not `TraceRecord`. The word *frozen* in those
packages is the dataclass's own `frozen=True` and its written-once file
discipline — **both preserved here**: no record is edited, no record is
rewritten, and `record()` still refuses to overwrite a file.

**This is ordinary unfinished construction, which the directive says not to call
a hard boundary.** It was declined four times on scope, and once on a
certification claim that does not hold.

### 2.2 What was built, and why it is not the number

- `refusal_type` is **derived from the raised exception**, exactly as `required`
  and `held` already are. A caller cannot assert it. `record()` takes
  `type(error).__name__` after the `isinstance(error, SANCTIONED_REFUSALS)`
  check that was already there.
- `__post_init__` refuses any name outside the sanctioned set, so a record
  naming a refusal nothing can raise cannot be constructed.
- **No lifecycle, no flag, no state.** `§14`'s prohibition — *a flag that could
  be set to "approved"* — is untouched; `status` is still derived from whether a
  response file exists.
- **The verifier was not modified.** `_refused()` already read
  `[f for f in fields if "type" in f or "kind" in f or "refusal" in f]`, and
  `test_refused_would_be_distinguished_if_the_record_named_the_type` already
  declared, in its own docstring, *"the finding must close by itself once the
  record gains the field."* The criterion was written by an earlier Act, before
  this one had a reason to want it met.
- **The resident records were not rewritten.** All three predate the field.
  `escalation_join()["naming_the_refusal_type"]` is still `0`, and a control now
  asserts it stays `0` **and says why**: backfilling a value nobody observed
  onto a historical record would be manufacturing evidence.

### 2.2a The divergence the field could have created, closed in the same change

The `P12-W3` governance-join already carried its own `refusal_type`. With the
record carrying one too, two surfaces state a single fact and nothing checked
they agreed. `join_escalation_to_grant` now refuses a join that contradicts the
record it sits beside.

**The asymmetry is the point.** A record that names **no** type is not treated
as contradicting anything: the three resident escalations predate the field, and
refusing on silence would have made every historical record unjoinable the
moment the field was added. *Cannot check* and *checked and found wrong* are
different answers — the same direction `FD-P12-004` fixed for an unreadable
Register, applied the other way because the failure mode is the other way.

Controlled four ways: the contradiction is refused and leaves no file behind; an
agreeing join is written (so the control does not refuse everything); a silent
record is joined; and the one resident wiring path is exercised with **both**
sanctioned refusal types, with record and join compared on disk.

### 2.3 Falsification

**CLAIM:** the persisted escalation record now names which refusal occurred.

- **CE-1: the field is cosmetic — it flips a schema check and nothing writes
  it.** **OBS:** two real refusals of different types were recorded through
  `EscalationRegister.record` and their persisted payloads read back:
  `refusal_type` is `EscalationRequired` and `ExecutionRefused` respectively,
  and the two differ. Pinned as a test. **REJECTED.**
- **CE-2: a caller could supply any string, so the record proves nothing.**
  **OBS:** `record()` derives it from the exception; direct construction with an
  unsanctioned name raises `EscalationRegisterError`. Pinned. **REJECTED.**
- **CE-3: the verifier was bent to accept it.** **OBS:** `_refused()` is
  byte-identical to its state at `86c11c2`; `git diff` touches no line of it.
  A control strips the field via mock and requires the finding to **re-open** to
  `RAISED ONLY`. **REJECTED.**

**CLAIM SURVIVES.** `§33` `REFUSED` = `DISTINGUISHED`, persisted as
`escalation record .refusal_type`.

---

## 3. `BLOCKED` and `VERIFIED` — **CLASS B**, one root cause

These are the two the `§1` reading closes off, and the reason is the same for
both: **the ratified outcome vocabulary is three, and `§33` names seven.**

```text
native_core.core.trace.VALID_STATUSES   = {success, failure, escalation}
tools.w4_execution: SUCCESS, FAILURE, ESCALATION  — and
  ExecutionOutcome.__post_init__ refuses anything else,
  citing ratified Domain Model §2.1
```

| | `BLOCKED` | `VERIFIED` |
|---|---|---|
| **Canonical requirement** | `§33` | `§33`; and `§30`'s `verification` runtime item, which is the same cause |
| **Current state** | `RAISED ONLY` | `UNREACHABLE` |
| **Evidence** | every persisted refusal is *in the escalation register*, so at rest it is `ESCALATED`; a block that is **not** escalated is not persisted at all — `record_refusals(root=None, …)` returns `()`. On the evidence surface the same collapse occurs: a refused step is written as `ExecutionOutcome(status=ESCALATION)` | `"verified"` is not in `VALID_STATUSES`; a successful run is not a verified one |
| **Classification** | **B** | **B** |
| **Closable within P12?** | **No** | **No** |
| **Authority** | ratified Domain Model `§2.1`; `ACT-CC-P12-W4-001 §9` (`TRACE RECORD ≠ UNIVERSAL RELATIONSHIP DATABASE`); `NATIVE CORE = 11` | same |
| **Required action** | none available to `P12`. Recorded as an external dependency per `§55(9)` |

**Why the `refusal_type` field does not also close `BLOCKED`, although it would
have been easy to say it does.** `refusal_type` distinguishes *which refusal*.
It does not distinguish *blocked* from *escalated*, because in this system every
persisted refusal is escalated — the register is the only durable home a refusal
has. Mapping `EscalationRequired → BLOCKED` and `ExecutionRefused → REFUSED`
would close `BLOCKED` on a reading `§33` does not make, of a term `§33` does not
define, using a type whose own name is *escalation*. **That decision was
available and is not taken**, for the reason `D-P12-027-02` was not taken: it is
the reading that improves the number, chosen by the party the number belongs to.
`_blocked()` is left exactly as it was.

**Why building the missing surface is not the answer either.** Distinguishing a
non-escalated block at rest needs a durable record of blocked-but-unescalated
actions. `tools/escalation_register.py` states why it has no default root:
*"Choosing a canonical on-disk home for runtime escalation records is a
deployment decision this Act does not grant."* `ACT-CC-P12-027` does not grant
it either. Per `§27`, this is stated **with** its dependency evidence rather
than classified silently.

---

## 4. `RETRYABLE` — **CLASS E**

| Field | Value |
|---|---|
| **Canonical requirement** | `§33` distinguishes `RETRYABLE` and constrains retry: it must not create duplicate authority, duplicate delegation, duplicate execution, orphan state or false success |
| **Current state** | `UNREACHABLE`. `retry_mechanisms()` finds none in the live system; the only one in the repository is in `docs/architecture/history` and is unreachable from it |
| **Classification** | **E** — the requirement that the system *possess retry* is not established. `§33` constrains retry **if it occurs**; no canonical section requires it to exist |
| **Closable within P12?** | **No**, and not because it is hard. Building one is construction no Act authorizes, and the directive forbids manufacturing retry outright |
| **Required action** | none. The measurement stays `UNREACHABLE` — truthful, and **not** relabelled `NOT APPLICABLE` to improve the count |

The five prohibitions stay `NOT APPLICABLE` with the module's own words:
*"no live retry mechanism exists, so none of the five can be violated — and none
is controlled against."* Absence of the hazard is not a control against it.

---

## 5. `§34` provenance and `§31` workflow — **CLASS D**, one population

Both findings are the **same eight executions**. `§31`'s weakest link
(`WORK → EXECUTION`, `7/15` by convention) and `§34`'s assembly (`7/15`) count
the same records; they are not two gaps.

```text
8 unjoined Trace records
  aios-corpus-health            #0 #1 #2 #3 #4
  p12-w4-integrated-execution   #0          (the run before manifests existed)
  w4-conformance-verification   #0 #1
```

| Field | Value |
|---|---|
| **Canonical requirement** | `§34` — provenance must identify, **where applicable**, actor, delegator, authority, … `§31` — `PLAN → HANDOFF → WORK → EXECUTION → OBSERVATION → VERIFICATION` must connect |
| **Current state** | 11/11 elements `CARRIED`; `assembly` = `NOT ASSEMBLABLE` because `ASSEMBLABLE` requires **every** execution ever recorded to join |
| **Evidence** | the four executions that join do so through an `ExecutionManifest` written beside the Trace record at execution time. The eight that do not were run before that surface existed, or on paths that hold no delegation at all |
| **Classification** | **D** — historical evidence limitation |
| **Closable within P12?** | **No.** A manifest asserts under which grant a past execution ran. Writing one now for an execution nobody observed under a grant nobody issued is retroactive attribution — `§43`'s `UNKNOWN ≠ FALSE` in the direction that matters, and the *"never rewrite historical evidence"* boundary |
| **Required action** | recorded as an evidence gap per `§55(8)`. Not closed |

### 5.1 The live part, and why it is **B** rather than **A**

Five of the eight are not merely historical: `aios_corpus_health_run.py` holds
**no delegation at all**, so re-running it tomorrow would add more unjoined
executions. That is a live gap, not a closed one, and it was examined as
candidate `A` work.

It is not actionable, and the reason is a prohibition rather than a difficulty.
A manifest cannot be written without a resolving `delegation_id`, and
`tools/w4_delegation.py` fixes the delegator as a constant read from
`FD-P11-001 §4.1` under

```text
Delegated Authority ≤ Available Delegator Authority
                    ∩ FD-P11-001 Scope
                    ∩ Canonical Boundaries
```

`FD-P11-001` authorizes **W4** delegation. Corpus-health assessment is
`ACT-CC-P12-014` work. Issuing a delegation for it under `FD-P11-001` would
widen that Decision's scope to make a metric join — **manufacturing authority in
substance while satisfying the form**, which is the one thing that must never
happen. **Classification B**, owned by whoever may extend the delegation scope.

---

## 6. `§26` governance evidence — **CLASS D**

| Field | Value |
|---|---|
| **Canonical requirement** | `§26`: governance evidence must establish nine elements, among them `affected surfaces` and `verification` |
| **Current state** | over **440** instruments: 1 `ESTABLISHED`, 6 `PARTIAL`, 2 `ABSENT` — no resident instrument carries a **label** for either absent element |
| **Classification** | **D** — a property of a corpus issued across the whole programme |
| **Closable within P12?** | **No** |
| **Authority** | whoever sets the labelling standard for governance instruments |
| **Required action** | none taken. Recorded as a source gap per `§55(7)` |

**The cheap closure was available and is refused.** `ABSENT` is `0/440`. Writing
two new documents carrying `Affected surfaces:` and `Verification:` labels would
move both elements to `PARTIAL` — a status change bought with two files and no
change to the corpus. The module pre-empts it in its own docstring: *"An element
with no resident label at all is `ABSENT`… it is not closed by inventing a
label."* Retrofitting labels onto the other 438 would be rewriting historical
evidence.

**The denominator is the tracked corpus, and this determination is in it.** The
population is read through `git ls-files`, so it was `438` while this record and
the return package were untracked and `440` once they were staged. Writing
documents about the gap **enlarges** it. That is worth stating plainly: a
verification whose own output counts against it cannot be improved by reporting.

---

## 7. `§35` self-model — **CLASS F**

Measured fresh: `{'questions': 12, 'verified': 10, 'inferred': 2, 'unknown': 0}`.
No element absent. `§35` is **not** a `§6.7` shortfall; it is the surface `§6.6`
carries, and the *"2 of 9 absent"* figure attached to it in the previous record
belongs to `§26`. **Measurement correction, made against the record this
continues.**

---

## 7a. The adjacent field that was **not** added, and why

Once `EscalationRecord` is established as neither certified nor frozen, the
obvious next question is why it did not also gain a `delegation_id` — the other
finding the same control tracks (`joined_by_structured_field: 0`), with its own
pre-declared closure message.

It was examined and declined, on three grounds that are not effort:

1. **It is not applicable to half the population.** An `EscalationRequired` is a
   *planning* escalation — the module's own words: *"A planning escalation has no
   instance and no runtime; it happens before execution, at the authority
   boundary."* There is no delegation to name. `§34`'s *"where applicable"* is
   doing real work here, unlike in the `refusal_type` case where the value was
   in hand for **every** record.
2. **The relation already resolves structurally, beside the record.**
   `P12-W3`/`P12-005` built exactly that surface and `escalation_join()` reports
   `joined_by_governance_surface: 2` of 3 records — the third predates it.
   Putting the same relation inside the record would create a second home for
   one relation, which is the defect `ExecutionManifest`-beside-`TraceRecord`
   was shaped to avoid.
3. **It moves no `§6.7` measurement.** `escalation_join()` is context in
   `_refused()`'s detail line; it feeds neither `§33`'s state count nor `§34`'s
   assembly, which counts executions, not escalations.

**Classified `F`** — met, by a different surface than the control's wording
anticipated — with the one pre-`P12-W3` record classified `D`. The control is
left asserting `0` so the finding cannot quietly close by accident.

---

## 8. Where `§6.7` now stands

```text
§33  REFUSED    CLASS A   closed here — 4 / 7
§33  BLOCKED    CLASS B   ratified outcome vocabulary
§33  VERIFIED   CLASS B   ratified outcome vocabulary
§30  verification CLASS B  same root as VERIFIED
§33  RETRYABLE  CLASS E   requirement to possess retry not established
§34  8 executions CLASS D  historical
§34  live non-delegated paths CLASS B  delegation scope not established
§31  same 8 executions CLASS D  historical
§26  2 of 9 over 438  CLASS D  historical corpus
§35  —          CLASS F   already satisfied; citation corrected
```

**One `A` existed. It is done.** Everything remaining is `B`, `D`, `E` or `F`,
each with its dependency evidence named above as `§27` requires.

**`§6.7` is still reported `NOT SATISFIED`** — and whether that report is
*correct* is a question this record does not answer by itself. It turns on what
`§6.7`'s *"has been completed"* means, which is the subject of
`P12-027-DELEGATED-DECISIONS.md` `D-P12-027-04`, **prepared and not taken**.

**`§6.13` becomes SATISFIED**, on the enumeration above: the one authorized
actionable item the previous determination found has been constructed, and no
other survives classification. This is stated with its own counterargument in
the Exit Contract determination rather than asserted here.

**`P12 COMPLETE = NO`**, on `§6.7` and `§6.14`.
