# P12-W5 — Self-Model Consumer Discovery and Semantic Reconciliation

**Act:** `ACT-CC-P12-W5-001`.
**Determination:** **W2 → W5 consumption is NOT REQUIRED and was NOT
CONSTRUCTED.** The proposed integration was falsified on two independent
grounds.
**Instrument:** `tools/p12_self_model_contract.py`
**Conformance:** `tools/tests/test_p12_self_model_contract.py` (17 tests).

---

## 1. Canonical reconciliation

[A] **`§18` of the Authorization is the controlling question set: twelve**, in
this order — What am I? / What do I own? / What authority do I have? / What
capabilities exist? / What is running? / What failed? / What is incomplete? /
What is authoritative? / What changed? / What is stale? / What do I not know? /
What decisions are recorded? It closes `SELF-MODEL ≠ AUTHORITY`.

[A] `§36`: *"The canonical question set must be preserved in full… No shortened
substitute set may silently replace the canonical model."* Its own inline list
of nine is prefixed *"At minimum the self-model must distinguish"* — a floor,
not the set. The resident model declares twelve and matches `§18` in order.

[A] **`§41` is the decisive clause**: *"Self-model operational state must derive
from current **authoritative state sources**."*

[A] **`§13` calls W2 a projection**, not a source: `P11 ORGANIZATIONAL STATE →
BOUNDED ORGANIZATIONAL PROJECTION → P12 UNIFIED OPERATIONAL STATE`.

[D] So the Act's question is not rhetorical. `§41` names *sources*; W2 is
canonically a *projection over* them. Routing W5 through W2 puts a projection
where `§41` names a source — which is admissible only if the projection
preserves what the source carries. That is a measurable question, and it was
measured.

## 2. W5-D1 — the actual read path, measured

[E] Twelve answers, every one bound to the source the contract names:

| Question | Answered by | Source | Kind |
|---|---|---|---|
| What am I? | `identity` | declared | DECLARED |
| What do I own? | `ownership` | declared | DECLARED |
| What authority do I have? | `authority` | declared | DECLARED |
| What capabilities exist? | `capabilities` | `organization_catalog` | AUTHORITATIVE |
| What is running? | `running` | `p12_runtime_observation` | AUTHORITATIVE |
| What failed? | `failed` | `p12_trace_registry` | AUTHORITATIVE |
| What is incomplete? | `incomplete` | `derived_views` | AUTHORITATIVE |
| What is authoritative? | `authoritative` | declared | DECLARED |
| What changed? | `changed` | `stale_state_audit` | AUTHORITATIVE |
| What is stale? | `stale` | `derived_views` | AUTHORITATIVE |
| What do I not know? | `unknowns` | this model's own answers | DERIVED |
| What decisions are recorded? | `decisions` | `derived_views` | AUTHORITATIVE |

[E] `12 contracted · in order · 0 missing · 0 unbound · 0 reading a projection`.

## 3. The falsification — two independent grounds

### 3.1 Semantic loss (`§9`, W5-D4)

[C] `§9` requires comparing **meaning**, not serialized representation. Measured
against the three answers whose sources W2 also reads:

```text
running       W5 carries  live · live_by_kind · observations · scope · terminated
              W2 carries  live · observations · terminated
              LOST        live_by_kind, scope

failed        W5 carries  failures · outputs · records_examined
              W2 carries  failures · records · stores
              LOST        outputs, records_examined

capabilities  W5 carries  count · declared · departments
              W2 carries  capabilities · departments
              LOST        declared, count
```

[D] **W2's projections are summaries; W5's answers are contents.** `failed`
would lose `outputs` — *what* failed, reduced to how many. `capabilities` would
lose `declared` — the capability names themselves. `running` would lose `scope`,
the qualifier stating what the answer covers, which the W5 evidence record
already records as essential.

[D] `§9` asks whether meaning is preserved. **It is not.** `§16` of the Act:
*"If any condition fails: DO NOT CONSTRUCT."*

[E] The remaining nine questions are not candidates at all: four read declared
constants, one derives from the model's own answers, and W2 carries **no
source** for `CHANGE`. W2 covers 7 of `§14`'s 17 state classes; ten — including
`CAPABILITY`, `CHANGE`, `IDENTITY`, `UNKNOWN`, `STALE` — have no W2 source.

[D] Where both carry a notion of staleness they mean different things: W5's
`stale` is an **unsynchronized external corpus**; W2's is an **index whose
content hash has drifted**. Routing one through the other would conflate two
distinct facts under one word.

### 3.2 The integration would have moved the gap, not closed it (W5-D6)

[E] Measured, not assumed:

```text
tools.p12_operational_state   non-test consumers: NONE
tools.p12_self_model          non-test consumers: NONE
```

[D] **W5 has no resident consumer either.** Wiring W5 to consume W2 would have
produced two surfaces with no consumer, joined to one another — not an
integration. The W2 `CONSUMER` link would still have been `UNSATISFIED`, because
the thing doing the consuming is itself unreached.

[C] This is the stronger ground. Even had the semantics been equivalent, the
construction would not have closed what it was proposed to close.

## 4. `ACT §10` — the freshness rule, proven with real data

[A] `NO INTERNAL CACHE ≠ NO STALE SOURCE`.

[E] W2 re-derives on every call, so its `observed_at` is always now and it
reports `CURRENT`. Meanwhile **6 of 6 underlying runtime observations are stale
or terminated, and 0 are live.**

[D] A self-model inferring source freshness from projection freshness would
**report a stopped world as live**. The two are measured separately, and a
conformance control asserts the live corpus demonstrates the distinction rather
than merely defining it.

## 5. Determination, per `§23`

| Item | Classification |
|---|---|
| W2 → W5 consumption | **NOT-A-GAP.** Not required by `§41`; W2 is a projection, and the projection loses what the answers carry |
| W2 `CONSUMER` link | **DEPENDENCY.** Unchanged at `UNSATISFIED`; not closable through W5 |
| W5 resident consumer | **MEASURED GAP.** Zero non-test consumers |
| W5 semantic contract | **CONSTRUCTED** — twelve questions bound, each with its authority and why its answer is correct |
| `F-17` | **RESERVED.** Untouched |

[C] **Nothing was constructed to make a criterion pass.** `§16`'s conditions
were not met and the integration was refused. The Act's `§37` defines success as
truthfully determining whether the relationship is required — not as building it.

## 6. A defect in my own checker, disclosed

[E] The binding check first inspected only imports written **inside** each
function and reported `incomplete`, `stale` and `decisions` as `UNBOUND`. All
three read `derived_views` through a module-level alias by way of the
`_projection` helper. **All three were bound and the checker could not see it.**

[D] A binding check that misses the way the module is actually written reports a
defect in the code it is reading when the defect is its own. It now resolves
module-level aliases and follows one level of helper delegation. A conformance
control and a runtime negative control both prove it can still report `UNBOUND`.

## 7. `§31` Regression

```text
controls at P11 certification 2089 → 2437 · 0 removed · 0 weakened
certified phases 10, 11 unchanged · regression 11 classes · 0 regressed
W2 behaviour unchanged · W4 behaviour unchanged
mutation 10 attempted · 8 detected · 2 missed · 0 unavailable
negative controls 22 instruments · 22 demonstrated
fresh process 5 stages · 5 reproduced
TraceRecord unchanged · Native Core 11 · protected packages untouched
```

[C] `§22` preserved: the two `§49` `ACCEPTED` controls remain individually
classified — `unauthorized P13 authorization` and `false certification` — and
are **not** rewritten as passing.

## 8. `§36 M` — W5 state, not inflated

```text
W5 AUTHORIZED    = TRUE
W5 CONSTRUCTED   = TRUE   (twelve answers, semantic contract bound)
W5 OPERATIONAL   = FALSE  (no resident non-test consumer)
W5 VERIFIED      = TRUE   (contract, bindings, freshness, authority)
W5 EXHAUSTED     = FALSE
W5 COMPLETE      = FALSE
```

## 9. What this does not establish

[C] A refused integration is a determination, not a closure. If W2's projections
were widened to carry what the answers carry, the semantic objection would
change — but that is **W2 construction**, it would make W2 a pass-through rather
than a projection, and it would still not give either surface a consumer.

[C] `W5 VERIFIED ≠ P12 VERIFIED ≠ P12 COMPLETE ≠ P12 CERTIFIED ≠ E12 RATIFIED`.

---

**Suite state at this record:** `native_core` 801 (1 expected failure) ·
`consumers` 276 · `tools` 1089 · total **2166**.
