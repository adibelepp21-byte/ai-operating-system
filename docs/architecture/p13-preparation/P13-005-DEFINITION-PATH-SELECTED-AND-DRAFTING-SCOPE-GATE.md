# P13 Definition Path Selected · Drafting Scope Gate

**Produced under:** the standing record-keeping duty; **no new Act**
**Trigger:** `FD-P13-001`, issued by the Founder — **Option B selected**
**Predecessors:** `P13-001` · `P13-002` · `P13-003` · `P13-004`

```text
P13 AUTHORIZATION   NOT GRANTED
P13 CONSTRUCTION    NOT AUTHORIZED
P13 CERTIFICATION   NOT AUTHORIZED
NATIVE CORE         11
```

---

## 1. What the Founder decided, and what remains undecided

**Decided.** The *method* by which a P13 definition may be reached:

```text
DISCOVERY / ARCHITECTURAL SYNTHESIS → NON-CANONICAL DRAFT → FOUNDER REVIEW
  → FOUNDER CANONICALIZATION → CANONICAL P13 DEFINITION → SEPARATE GATES
```

**Not decided.** Everything the method would carry. `FD-P13-001 §12` states it
in its own words: *"Selecting Path B does NOT mean `P13 AUTHORIZED = YES`. It
means only: `DEFINITION METHOD SELECTED`."*

| | State after `FD-P13-001` |
|---|---|
| P13 canonical identity | **NOT ESTABLISHED** — `GAP-0001` remains the apex |
| P13 required state | **NOT ESTABLISHED** |
| P13 Blueprint | **NOT CANONICAL**, and **not yet drafted** |
| Drafting authority | **SUBJECT TO `FD-P13-002`** — the record's own machine-readable summary |
| Canonicalization authority | **FOUNDER RESERVED**, reaffirmed |
| P13 construction | **NOT AUTHORIZED** |

## 2. Why no draft was started

`FD-P13-001` selected the path this office had recommended. That is precisely
the condition under which it would be easiest to start work and easiest to be
wrong about it.

The record forecloses it in three separate places:

```text
§6   "FD-P13-001 memilih mekanisme Path B, tetapi tidak boleh memalsukan
      bahwa FD-P13-002 sudah diputuskan."

§12  "The separate FD-P13-002 authority question must be resolved before
      Claude begins work that depends on the disputed drafting scope."

§15  "No P13 Blueprint drafting action that depends on this unresolved
      scope question may be treated as authorized merely from selection
      of Option B."
      NON_CANONICAL_DRAFT: PERMITTED_ONLY_SUBJECT_TO_FD-P13-002
      DRAFTING_AUTHORITY:  SUBJECT_TO_FD-P13-002
```

**And the delegation names this exact situation and prescribes this exact
response.** `DEL-T4.4-CF-001 §3.3`:

```text
AUTHORIZED ACTION = EXPLICIT DELEGATION × VALID SCOPE × VALID TIER × VALID ARTIFACT
If any factor is absent, the action is NOT AUTHORIZED.
...
STOP → RECORD → ESCALATE → FOUNDER DECISION
```

The scope factor is the one in doubt. `STOP → RECORD → ESCALATE` is not
this office's caution; it is the instrument's instruction. **A Founder's
agreement with a recommendation is not a scope ruling**, and treating it as one
would be inferring authority from confidence and from the Founder's assent —
two of the six sources `§3.3` names as forbidden.

## 3. `FD-P13-002` — decision package

**Options are listed. None is chosen.** `DECISION PACKAGE ≠ DECISION`.

### The question

> Does `DEL-T4.4-CF-001`'s effective state — *"AIOS Construction Phase"* —
> extend to producing a **non-canonical P13 preparation artifact**, while P13
> itself is not an authorized construction phase?

### Evidence that bears on it, read from source

| Reading | Evidence for | Evidence against |
|---|---|---|
| **Scope is a program era** (AIOS is in its construction era; the delegation spans it) | The field reads *"AIOS Construction Phase"*, **not** *"P12"* or any phase index. The delegation is dated `2026-08-15` and has been `ACTIVE` across P10, P11 and P12 — it is demonstrably not bound to one phase. `Review Condition` is a standing *"construction-phase governance review"*, not a per-phase expiry | The era's content has so far been phases that **were** authorized for construction. P13 is not |
| **Scope is phase-bound** (it reaches only authorized construction phases) | `§3.2` excludes *"create authority by implication"* (`.11`) and self-expansion of the delegation (`.20`); reading an era broadly is the looser reading | Nothing in `§3.1` or the Founder decision text conditions the scope on the *target* phase being authorized |
| **The artifact factor is separately satisfied either way** | `§3.1 A` delegates *"perform architecture design · prepare architecture decisions · prepare architecture recommendations"*; `§3.1 D` adds documentation and roadmap sequencing. A non-canonical draft is an architecture recommendation, and `ACT-CC-P13-003 §11` permits non-canonical working material | `§5.10` excludes *"unilateral authorship of a canonical P13 Blueprint"* — which the draft is not, provided it stays non-canonical |

### A fact that changes the shape of the question

**Every P13 preparation output so far was produced under a Founder-issued Act,
not under the delegation's standing scope.** `P13-001`, `P13-002`, `P13-003` and
`P13-004` exist because `ACT-CC-P13-001`, `ACT-P13-001`, `ACT-CC-P13-002` and
`ACT-CC-P13-003` each commissioned them by name.

This is offered as a **structural observation, not as precedent** — `§3.3` names
precedent among the forbidden inference sources, and this office is not
inferring from it. Its relevance is the opposite of a licence: it shows that the
delegation's standing scope has **not** in fact been the basis for P13 work to
date, which is why the scope question is live now rather than settled.

It also makes option (c) below the cleanest resolution, because it is what has
already been working.

### Options

| | Option | Consequence |
|---|---|---|
| **(a)** | **Confirm in scope.** The delegation's construction-phase effective state covers non-canonical P13 preparation artifacts | Drafting may begin under the existing delegation. Broadest reading; the Founder should be aware it also settles the scope question for future P13 preparation work generally, not just this draft |
| **(b)** | **Confirm out of scope.** The delegation does not reach P13 while P13 is unauthorized | Path B stalls unless the Founder supplies authority another way. Option B of `FD-P13-001` would become unavailable in its delegated form, and the definition would need Path A or a new instrument |
| **(c)** | **Issue a bounded Act** commissioning the non-canonical draft, as `ACT-CC-P13-001` … `-003` each did | Sidesteps the scope question rather than ruling on it. Narrowest grant: authority attaches to one named artifact, expires with it, and sets no precedent for the delegation's reach. **Leaves the `§3.3` scope ambiguity open** — which is a cost, not a benefit, if the Founder wants it settled |

### What a decision on this does **not** do, under any option

```text
does not establish P13 identity                  (GAP-0001, still the apex)
does not establish P13 required state
does not make any draft canonical                (§58 · GAP-0003b, Founder-reserved)
does not authorize P13 construction
does not alter Native Core = 11
```

## 4. Carried, and not resolved by `FD-P13-001`

`FD-P13-003` corpus residency (`GAP-0006`) · `FD-P13-004` P1–P9 residency
ruling (`D-1`, non-blocking) · `FD-P13-005` Agent lifecycle canon (`GAP-0009`) ·
`FD-P13-006` P13 reserved-authority enumeration (`GAP-0004`) ·
`FD-P13-007` `H-1` phase-state register (inherited from P12) ·
`AD-P13-001` `Optimization → Governance` · `AD-P13-002` `ADR-0029` ·
**`FD-2`** Founder ≡ Architect equivalence — resident, open, and load-bearing
for `DEL-T4.4-CF-001` itself and therefore for any answer to `FD-P13-002`.

**`GAP-0006` touches this record directly.** `FD-P13-001 §2` cites an
*"AIOS CO-FOUNDER DELEGATION CHARTER v1.0"* that is **not resident**. It was
reported as absent, not read, and no adjacent document was substituted for it.
The analysis above rests on `DEL-T4.4-CF-001` in the resident Delegation
Register, which `FD-P13-001 §4.1` itself quotes.

## 5. Register effect

| Gap | Was | Now |
|---|---|---|
| `GAP-0001` | apex · `FOUNDER DECISION REQUIRED` | **unchanged — still open, still the apex.** The method for closing it is now selected; the content is not |
| `GAP-0003` drafting | `RESOLVED — ESTABLISHABLE`, not exercised | **unchanged.** Still establishable, still not exercised |
| `GAP-0003b` canonicalization | `FOUNDER RESERVED` | **reaffirmed** by the decision body |
| all 15 `BLOCKING` gaps | open | **unchanged** — none was closed by the path selection |

**No downstream gap was closed because a path was chosen.** Selecting how a
question will be answered does not answer it. Register total remains 28.

## 6. Exit state

```text
FD-P13-001             = ISSUED — OPTION B (per its §16 interpretation rule;
                         its metadata Status line still reads PENDING, noted
                         in the record and not silently reconciled)
DEFINITION METHOD      = SELECTED
P13 IDENTITY           = NOT ESTABLISHED   ← GAP-0001, still the apex
P13 REQUIRED STATE     = NOT ESTABLISHED
P13 BLUEPRINT          = NOT DRAFTED · NOT CANONICAL
DRAFTING AUTHORITY     = SUBJECT TO FD-P13-002 — NOT EXERCISED
CANONICALIZATION       = FOUNDER RESERVED (§58)

NEXT GATE              = FD-P13-002 — drafting scope
P13 AUTHORIZATION      = NOT GRANTED
P13 CONSTRUCTION       = NOT AUTHORIZED
P13 CERTIFICATION      = NOT AUTHORIZED
```

**Nothing was constructed and no Blueprint was drafted.** No code, test,
contract, capability, Native Core boundary, architecture, subsystem, authority
or decision was created or modified. No P13 definition was invented and no
absent source reconstructed. `docs/architecture/p13/` does not exist.
`P13 AUTHORIZED` reads `False` from the instrument body. Native Core remains 11.

**This record does not authorize the next gate.** It states what the gate is.
