# P12-W1 — System Integration

**Act:** `ACT-CC-P12-W1-001`.
**Status:** [E] constructed and independently verified. **Not operational.**
**Determination:** **W1 does not consume W2, and cannot** — W2 has no notion of
an edge.
**Instrument:** `tools/p12_integration_graph.py`
**Conformance:** `tools/tests/test_p12_integration_graph.py` (29 tests,
including `§11` Tests A–J).

---

## 1. The first finding was a name collision

[E] Three resident modules are named `w1_*`:
`tools/w1_coordination_run.py`, `tools/w1_cross_department_run.py`,
`w1_coordination_proof.py`.

[E] **All three are `P11-W1`**, executing `ACT-CC-P11-010 §20` and `DP-02 §11`.
They are organizational coordination surfaces, not system integration.

[D] **P12-W1 did not exist.** Read from the filenames, W1 looked implemented;
read from the bodies, nothing implemented it. `FILENAME ≠ CANONICAL STATUS`, and
this is the clearest instance of it the programme has produced: two different
work packages in two different phases share a label.

[E] Actual state at Act start: **`NOT_STARTED`**.

## 2. The second candidate was also a false positive

[E] `derived_views.interface_graph()` derives a 14-edge graph over Native Core
boundaries. Its relationship is `imports` — **not one of `§9`'s twelve
relationship classes**, and `ACT §8` is explicit: *"Do not count an edge merely
because two modules can import one another."*

[D] It is a structural import graph inside one boundary set, not a P12
integration graph. A conformance control asserts every edge of that graph uses
`imports` and no edge of this one does, so the two cannot be conflated later.

## 3. Canonical W1

[A] `§14` of the Authorization: *"Claude **wajib** memetakan"* —
`PHASE → CAPABILITY → PLATFORM → ORGANIZATION → RUNTIME → WORKFLOW → EVIDENCE →
VERIFICATION` — and *"Phase dan Platform Organization harus tetap dibedakan."*

[A] `§8`: eight integration classes and ten requirements. `§9`: a ten-attribute
edge model, twelve relationship classes, seven classifications. `§10`:
`DEPENDENCY ≠ OWNERSHIP`, `INTERACTION ≠ AUTHORITY TRANSFER`,
`COORDINATION ≠ OWNERSHIP`. `§11`: *"P12 may integrate a surface without taking
ownership of that surface."* `§12`: nine dependency classes.

[D] Mandatory (`wajib`) and authorized under `D1`. Construction proceeds.

## 4. A canonical ambiguity, recorded rather than resolved

[U] `§9` lists `STATE` in the edge model **and** gives a separate seven-value
classification. That leaves `STATE` ambiguous: the edge's own lifecycle state,
or a slot for the state the edge relates.

[D] Read here as **the edge's own state**. The alternative would make every edge
depend on a projection that summarises what an edge needs in full — the loss
`ACT-CC-P12-W5-001` already measured. The choice is stated in the module so it
can be argued with, and the ambiguity is recorded, not resolved by fiat.

## 5. The W1 ↔ W2 determination — measured

[C] `ACT §44`: *"DO NOT TREAT `§9`'S EDGE MODEL AS PROOF OF RUNTIME
CONSUMPTION."*

[E] **W2 cannot supply 8 of `§9`'s 10 edge attributes**: `target`,
`relationship`, `contract`, `state`, `evidence`, `verification`, `lifecycle`,
`owner`. The two names it shares — `source`, `authority` — mean different
things: W2's `source` is a read path and its `authority` is the source's;
`§9`'s are an edge endpoint and the edge's authority.

[D] **W2 is a per-state projection; a `§9` edge is a per-edge record.** They are
different shapes, not different detail levels. So the answer is not "W1 should
read sources directly instead" — it is that **W2 has no notion of an edge at
all**, and a W1→W2 dependency would have nothing to draw on.

[E] Measured from the import graph: W1 imports
`p12_runtime_observation`, `p12_provenance_verification`,
`p12_cross_phase_verification` and `p12_execution_chain_reader` — the
authoritative surfaces — and **does not import W2**.

[D] This is the third consecutive falsification of a proposed consumer of W2
(`W2 → W5` in `ACT-CC-P12-W5-001`, and now both directions of `W1 ↔ W2`). The
pattern is consistent and has a single cause: **W2 summarises, and every
proposed consumer needs references.**

## 6. The graph — eight edges, derived from artifacts

[E] Every edge is evidenced by a resident artifact that relates both ends. An
edge whose evidence does not resolve is `INVALID`, not omitted.

| `§8` class | Relationship | Classification | State |
|---|---|---|---|
| phase ↔ phase | DEPENDS_ON | **UNVERIFIED** | 6/8 exercised; P4, P9 demonstrator-only |
| platform ↔ phase | PROVIDES | **RESERVED** | mapped, provider unassigned (`F-17`) |
| governance ↔ execution | DELEGATES | VERIFIED | 4/4 manifests carry grant and record |
| organization ↔ runtime | COMPOSES | VERIFIED | 2 Departments reached |
| workflow ↔ runtime | OBSERVES | **UNVERIFIED** | 1 workflow, 2 runtime observations, no shared identity |
| memory ↔ state | CONSUMES | **UNVERIFIED** | 0/7 executions consumed memory |
| evidence ↔ verification | VERIFIES | VERIFIED | 4/4 carry requirement and outcome |
| authority ↔ execution | DELEGATES | VERIFIED | 4/4 chains resolve every reference |

[E] `4 verified · 3 unverified · 1 reserved · 0 invalid · 0 dangling ·
8 owners unresolved`.

### 6.1 `workflow ↔ runtime` — the `§48` case, found again

[E] Both kinds of observation exist. **No runtime identity appears on both
sides.** Two observations are not a relationship, and the hosting relation is
not recorded anywhere.

### 6.2 `memory ↔ state` — a field carried and never populated

[E] Every one of seven durable execution records carries `memory_consumed`, and
every one is empty. The Trace contract requires *captured content* (INV-6); the
field exists, is written, and nothing has ever put anything in it.

## 7. Nothing here owns what it integrates

[C] `§11`. The `owner` attribute is **read, never assigned**, and every one of
the eight reads `UNRESOLVED (F-17)`. A conformance control asserts
`owners_unresolved == edges`, and another fails if any function in the module is
named `authorize`, `certify`, `approve`, `permit`, `grant` or `own`.

[C] `platform ↔ phase` is classified **`RESERVED`, not `VERIFIED`**: the Phase↔PD
map is resident and the provider assignment is `F-17`. **Recording the crossing
is not assigning the provider.**

## 8. `§11` Falsification — Tests A–J

| Test | Result |
|---|---|
| A — semantic loss | W2 cannot supply 8 of 10 edge attributes |
| B — source bypass | W1 reads the authoritative surfaces directly; imports no projection |
| C — freshness mismatch | the graph is re-derived per call; an edge follows its source |
| D — authority contamination | no function creates authority; every owner is read |
| E — consumer illusion | test modules are excluded from consumer counting |
| F — directionality | each edge declares a direction; platform **provides to** phase |
| G — circularity | W1 and W2 do not depend on each other in either direction |
| H — historical contamination | the module contains no write path |
| I — provider inference | `platform ↔ phase` is `RESERVED`; no edge assigns a provider |
| J — operational illusion | the graph runs and has **zero resident consumers** |

## 9. `§23` Real system work

[E] A fourth integrated execution was run — real work, 14 criteria, **3
satisfied**, a genuine failure. The graph was told nothing and followed:

```text
governance ↔ execution    3/3 → 4/4 manifests
evidence ↔ verification   3/3 → 4/4
authority ↔ execution     3/3 → 4/4 chains
memory ↔ state            0/6 → 0/7   (denominator moved, numerator did not)
                          4 of 8 edges moved; the other 4 correctly did not
```

[D] The `memory ↔ state` movement is the honest one: a new execution was added
and it too consumed no memory. The edge stays `UNVERIFIED`.

## 10. `§12` Consumer determination

[E] Measured, tests excluded:

```text
tools.p12_integration_graph   non-test consumers: NONE
tools.p12_operational_state   non-test consumers: NONE
tools.p12_self_model          non-test consumers: NONE
```

[E] **`W1 CONSUMER = UNSATISFIED.`** None was manufactured.

[D] Three P12 surfaces are now constructed, verified, and unconsumed. The
programme hypothesis holds across all three — *capability exists, conformance
exists, operational reachability absent* — and W1 was the last workstream
canonically positioned to be a consumer of the others. **It is not one.** It
reads the authoritative sources, as `§8` requires it to.

## 11. Three defects in my own instruments, disclosed

1. **The dangling-evidence check compared a module name to the filesystem** and
   reported a resident module as dangling. A defect in the check, not a break in
   the graph. It now resolves a module reference as the file it names.
2. **A conformance control read only `node.module`** and so saw nothing but
   `"tools"` for `from tools import X as y`. It missed every real import it was
   written to find.
3. Neither was a finding about the system, and both are recorded rather than
   quietly corrected.

## 12. `§33` Regression

```text
controls at P11 certification 2089 → 2454 · 0 removed · 0 weakened
certified phases 10, 11 unchanged · regression 11 classes · 0 regressed
W2 unchanged: 8 sources CURRENT, 0 conflicts
W4 unchanged: 4 chains joined, 7 of 7 edges each
W5 unchanged: 0 unbound answers, semantic contract intact
W6 STATE unchanged: broken link still ('CONSUMER',)
mutation 10 attempted · 8 detected · 2 missed · 0 unavailable
negative controls 23 instruments · 23 demonstrated
fresh process 5 stages · 5 reproduced · 0 diverged
TraceRecord unchanged · Native Core 11 · protected packages untouched
F-16, F-17, F-18 untouched · no verifier weakened
```

## 13. `§40 B` — W1 state, not inflated

```text
W1 AUTHORIZED   = TRUE
W1 CONSTRUCTED  = TRUE
W1 INTEGRATED   = PARTIAL  (4 of 8 edges verified)
W1 VERIFIED     = TRUE     (29 controls, Tests A–J)
W1 OPERATIONAL  = FALSE    (zero resident consumers)
W1 EXHAUSTED    = FALSE
W1 COMPLETE     = FALSE
W1 CERTIFIED    = FALSE
```

## 14. What this does not establish

[C] Four verified edges say four relationships resolve an artifact relating both
ends. They do not say the system uses them.

[C] `W1 VERIFIED ≠ P12 VERIFIED ≠ P12 COMPLETE ≠ P12 CERTIFIED ≠ E12 RATIFIED`.

[C] `F-17` and `F-18` were not approached. No provider was assigned, no
cross-PD interface invented, no authority created.

---

**Suite state at this record:** `native_core` 801 (1 expected failure) ·
`consumers` 276 · `tools` 1118 · total **2195**.
