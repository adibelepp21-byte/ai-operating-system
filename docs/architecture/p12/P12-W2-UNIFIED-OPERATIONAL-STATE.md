# P12-W2 — Unified Operational State

**Act:** `ACT-CC-P12-W2-001`.
**Status:** [E] constructed and independently verified. **Not operational** —
the projection has no consumer, and W6 says so rather than W2.
**Instruments:** `tools/p12_operational_state.py` (projection) ·
`tools/p12_operational_state_verifier.py` (independent verifier) ·
`tools/p12_state_verification.py` (W6 `§19` STATE scope item).
**Conformance:** 30 tests (`§32` Tests A–H) + 15 tests.

---

## 1. The architecture question was answered by canonical text, not by me

[C] `ACT §19` asks whether Unified Operational State means a physical store
(A), a logical projection over distributed sources (B), a hybrid (C), or
something else (D), and warns: *"Do not choose A merely because it is
technically convenient."*

[A] **The canonical bodies settle it.** `§13`: *"P12-W2 is the canonical
integration **surface**"*, with the chain `P11 ORGANIZATIONAL STATE → BOUNDED
ORGANIZATIONAL **PROJECTION** → P12 UNIFIED OPERATIONAL STATE`. `§15` of the
Authorization grants authority to build a *"state **integration surface**"*.
Neither text names a store.

[D] **Option B.** Nothing here holds a durable copy of anything a source owns.
Every entry is re-derived on every call, which makes a stale projection
structurally impossible — there is no second copy to drift. A conformance
control parses the module and **fails if it contains any write path at all**:
no `write_text`, no `mkdir`, no `unlink`.

## 2. W1 / W2 / W3 boundary matrix

[A] Derived from the canonical bodies, not from convenience.

| Question | W1 | W2 | W3 | Canonical basis |
|---|---|---|---|---|
| System integration | **OWNS** | consumes | consumes | `§8` *"W1 establishes operational relationships across P4–P11"* |
| Integration edges | **OWNS** | — | — | `§9` edge model `SOURCE TARGET RELATIONSHIP OWNER AUTHORITY CONTRACT STATE …` |
| Operational state | consumes | **OWNS** | consumes | `§13`; and `§9` lists `STATE` as an **attribute** of a W1 edge, so W1 reads it |
| Governance state | — | projects, attributed | **OWNS** | `§21` *"decision / authority / delegation / escalation visibility"* |
| Authority projection | — | carries, never asserts | **OWNS** | `§22`; `ACT §28` `SYSTEM-READABLE STATE ≠ GOVERNANCE AUTHORITY` |
| State ownership | — | **declares per source** | governance sources only | `§17` `STATE → SOURCE → PROJECTION → CONSUMER` |
| Cross-layer relationship | **OWNS** | — | — | `§9`, `§10` |
| Escalation | — | projects count | **OWNS** | `§21`; W4-GAP-008 is a W3 dependency |
| Verification | — | — | — | **W6 owns it** (`§45`); `ACT §22`: `W2 ≠ W6` |

## 3. State inventory — eight declared sources

[C] **Declared, never discovered by inference.** A registry built by scanning for
things that look like state would silently acquire whatever appeared next, and
its owner and authority columns would be guesses.

| State | Class | Semantics | Owner | Provider |
|---|---|---|---|---|
| `runtime.observed` | RUNTIME | OBSERVATIONAL | P12-W4 runtime observation | UNRESOLVED (F-17) |
| `execution.recorded` | EXECUTION | SOURCE-OF-TRUTH | Native Core Trace boundary | UNRESOLVED (F-17) |
| `execution.provenance` | EVIDENCE | SOURCE-OF-TRUTH | P12-W4 execution provenance | UNRESOLVED (F-17) |
| `delegation.granted` | AUTHORITY | SOURCE-OF-TRUTH | FD-P11-001 delegator | UNRESOLVED (F-17) |
| `escalation.raised` | GOVERNANCE | SOURCE-OF-TRUTH | escalation register | UNRESOLVED (F-17) |
| `organization.declared` | ORGANIZATION | SOURCE-OF-TRUTH | P11 organization | UNRESOLVED (F-17) |
| `governance.declared` | GOVERNANCE | GOVERNANCE-DECLARED | governance instruments | UNRESOLVED (F-17) |
| `architecture.boundaries` | ARCHITECTURE | SOURCE-OF-TRUTH | Native Core | UNRESOLVED (F-17) |

[E] **All eight providers are `UNRESOLVED (F-17)`**, and a verifier check fails
if any is assigned. `IMPLEMENTATION LOCATION ≠ CANONICAL PROVIDER OWNERSHIP`: a
projection filling the column from the directory a reader happens to live in
would resolve `F-17` by convention, which `§17`/`§18` forbid.

## 4. This surface holds no authority

[C] `ACT §28`: `SYSTEM-READABLE STATE ≠ GOVERNANCE AUTHORITY`. `§29` forbids
establishing certification state.

- `StateEntry.is_authority()` returns **False, always**, so the answer is
  written down rather than assumed.
- `declares()` is the only governance accessor: it returns *what an instrument
  declares*, attributed to that instrument, with an explicit
  `is_authority: False` and a note to read the instrument.
- A conformance control parses the module and **fails if any function name
  begins with `authorize`, `certify`, `approve`, `permit` or `grant`**.
- An independent check fails if any projected value contains
  `certified: true`-shaped content — and it is written in the verifier, not
  delegated to the writer's own `is_authority`, because a surface asserting its
  own harmlessness proves nothing.

## 5. A false positive in my own conflict detector, disclosed

[E] The first `§17` conflict detector compared **state classes** and reported a
`GOVERNANCE` conflict between `escalation.raised` and `governance.declared`.

[D] `§17` says *"the same system-wide state"*, not *"the same class"*. Those two
hold different facts and neither disputes the other's. **The finding was a
false positive produced by my own coarseness.**

[C] The fix is not to re-label sources until the detector goes quiet. Each
source now declares `owns_within_class` — the portion it owns — and a conflict
fires only when two sources claim the **same portion**. A source declaring no
portion is reported `UNDECLARED`, which is a finding rather than an exemption:
an unstated claim cannot be checked against anyone else's.

[E] Live result: **0 conflicts, 0 undeclared claims.** A control proves a
duplicate portion still fires, and that a class collision alone does not.

## 6. `§31` Real system work

[C] W2 is a projection, so "change real state" means causing a real *source*
state change and seeing the projection follow it, with the projection told
nothing about the run.

[E] A third integrated execution was run (`p12-w2-state-transition`, real work:
14 criteria against `tools/w4_execution.py`, **4 satisfied — a genuine
failure**). The projection was captured before and after:

```text
delegation.granted     grants 27 → 28 · active 7 → 8
execution.provenance   manifests 2 → 3
execution.recorded     records 5 → 6 · stores 3 → 4 · failures 2 → 3
runtime.observed       a new terminated runtime
                       — 4 of 8 sources moved; the other 4 correctly did not
```

[E] Read through the independent verifier afterwards: **9 of 9 checks
verified**. The new execution's chain: **JOINED, 7 of 7 edges.**

## 7. `§32` Falsification — Tests A–H

| Test | Result |
|---|---|
| A — wrong source | a declared path that does not resolve is `VIOLATED`; a source with no projection yields `UNKNOWN` |
| B — wrong owner | a duplicate portion is `VIOLATED` and reported as a conflict; a class collision alone is not |
| C — stale state | a cached timestamp is `VIOLATED`; a stale governance source projects `STALE`; an empty observation root projects `UNKNOWN` |
| D — missing source | an entry without provenance is `VIOLATED`; a value with no source cannot be `CURRENT`; a raising projection yields `UNKNOWN` with no value |
| E — historical rewrite | the module contains **no write path at all**; a full projection leaves `git status` byte-identical |
| F — governance impersonation | a projected `certified: true` is `VIOLATED`; no accessor may be named `authorize`/`certify`/… |
| G — F-17 provider injection | an assigned provider is `VIOLATED`; all eight remain unresolved |
| H — projection drift | the projection follows its source when the source changes |

[C] The verifier's own freshness check is the one that makes Option B
falsifiable: **if any entry's `observed_at` predates the verification run,
something cached it.**

## 8. `§33` The verifier is independent, and the one shared dependency is disclosed

[C] It imports nothing from the writer at module scope — a control parses its
imports and fails if it ever does. It re-declares the status vocabulary rather
than importing it, so agreement is visible instead of automatic, and resolves
every declared read path itself.

[C] **Disclosed**: it must obtain the projection in order to judge it, so it
loads `project` and `SOURCES` **as data** through `importlib`. Every *property*
checked is re-derived in the verifier. `§33` requires disclosure where a shared
dependency is unavoidable; this is it.

## 9. `§48` W6 re-verification — and W6 says the item is not closed

[C] `ACT §48`: *"do not assume W2 automatically closes W6 STATE. W6 must
independently verify it."*

[E] `tools/p12_state_verification.py` verifies `§17`'s four-link chain and reads
W2 as data:

```text
STATE                  SATISFIED     8 sources across 7 state classes
AUTHORITATIVE SOURCE   SATISFIED     every source names a canonical source and authority
PROJECTION             SATISFIED     8 projections, each carrying provenance
CONSUMER               UNSATISFIED   no non-test module reads the projection
```

[E] **`chain_complete: False`.** W6 STATE moves from `BLOCKED — DEPENDENCY` to
**`PARTIAL`**, not to closed.

[C] `§16`: *"Each claimed consumer requires evidence that it actually consumes
the state."* A conformance suite is **not** counted as a consumer — counting
tests is how a surface nothing uses comes to look integrated.

[D] W2 has reproduced the programme hypothesis on itself: capability exists,
conformance exists, operational reachability absent.

## 10. W2 closed a mutation that was previously unattemptable

[E] `§50`'s `alter state authority` was `UNAVAILABLE` — honestly so, because
there was no surface on which two competing claims could be planted. **W2 built
one, so the mutation is now attempted, and the conflict detector refuses it.**

```text
§50 mutations   before: 10 named · 9 attempted · 7 detected · 1 unavailable
                after:  10 named · 10 attempted · 8 detected · 0 unavailable
```

[C] The conformance control that asserted the mutation was unattempted was
corrected **because the system changed**, not because the control was wrong.

## 11. `§45` Gap register

### W2-GAP-001 — state inventory
Eight material state surfaces existed, each with its own reader and no common
declaration of owner, authority or freshness. **CONSTRUCTED** — declared source
registry, every read path verified to resolve.

### W2-GAP-002 — state authority conflict detection
`§17` requires conflicts be discovered. Nothing detected them. **CONSTRUCTED**,
after a false-positive detector was replaced (`§5` above). 0 conflicts live.

### W2-GAP-003 — state provenance
`§36` requires each projection answer where state came from, when, and by what
transformation. **CONSTRUCTED** — every entry carries source, `observed_at`,
transformation and authority; a verifier check fails if any lacks one.

### W2-GAP-004 — freshness
`§14` requires `CURRENT` / `STALE` / `UNKNOWN` stay distinct and absence never
become a negative. **CONSTRUCTED** — a raising projection yields `UNKNOWN` with
no value, and a control proves it.

### W2-GAP-005 — provider ownership
**BLOCKED — RESERVED (F-17).** All eight providers `UNRESOLVED`, enforced by a
check that fails if any is assigned.

### W2-GAP-006 — consumers
**PARTIAL.** Zero non-test consumers. Wiring one is the next frontier and is
*not* done here: the natural consumer is W5, and `ACT §20` forbids W2
redefining W5 semantics silently. Changing W5's read path changes what W5's
recorded measurements mean, which needs its own reconciliation.

### W2-GAP-007 — W3 dependency
**DEPENDENCY (W3).** `escalation.raised` is projected as a count. W4-GAP-008 —
a refusal joining its grant through parsed prose — remains W3's to close.
`ACT §44`: do not repair W3 from W2.

### W2-GAP-008 — W1 dependency
**DEPENDENCY (W1).** `§9`'s integration graph is W1's, and its edge model lists
`STATE` as an edge attribute. W1 is a **consumer** of W2, not a duplicate of it.
Not constructed here.

## 12. `§47` Regression

```text
certified phases 10, 11 unchanged · regression 11 classes · 10 held · 0 regressed
mutation 10 attempted · 8 detected  (improved by W2; nothing weakened)
execution chain 3 manifests · 7 of 7 edges each · 0 dangling
negative controls 21 instruments · 21 demonstrated
fresh process 5 stages · 5 reproduced · 0 diverged
TraceRecord unchanged · Native Core 11 · protected packages untouched
F-16, F-17, F-18 untouched · no verifier weakened to obtain PASS
```

## 13. What this does not establish

[C] **W2 is constructed and verified. It is not operational**, and W6 — not W2 —
is what says so.

[C] `W2 VERIFIED ≠ P12 VERIFIED ≠ P12 COMPLETE ≠ P12 CERTIFIED ≠ E12 RATIFIED`.

[C] No governance authority was created. No provider was assigned. No frozen
surface was modified. `F-16`, `F-17`, `F-18` were not approached.

---

**Suite state at this record:** `native_core` 801 (1 expected failure) ·
`consumers` 276 · `tools` 1072 · total **2149**.
