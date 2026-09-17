# `P12-W6` — STATE verification · `§19` scope item, closed by measurement

**Instrument:** `tools/p12_state_verification.py`
**Independent verifier:** `tools/p12_consumer_evidence_verifier.py`
**Falsification:** `tools/tests/test_p12_consumer_measurement.py` (19 controls),
`tools/tests/test_p12_state_verification.py` (17 controls)
**Executed under:** `ACT-CC-P12-008`

This document records the STATE scope item's own evidence. It **supersedes
nothing**: `P12-W2-UNIFIED-OPERATIONAL-STATE.md §9` and
`P12-W6-SCOPE-DISCOVERY-AND-CLASSIFICATION.md` truthfully record what W6
measured when they were written, and neither was edited. What changed is the
measurement, not the history.

---

## 1. The chain, and the link that decides

[A] `§17 State Authority` of `AIOS_P12_ROADMAP_PRD_CONSTRUCTION_BLUEPRINT_v1.0.md`
fixes the chain every state class must satisfy:

```text
STATE → AUTHORITATIVE SOURCE → PROJECTION → CONSUMER
```

[D] Three of the four links have been SATISFIED since W2 built the surface. The
fourth is the one that decides whether a projection is operational state or
just a projection, and it reported `UNSATISFIED` from the moment it was first
measured until this Act.

**Live result:**

```text
STATE                  SATISFIED   8 declared sources across 7 state classes
AUTHORITATIVE SOURCE   SATISFIED   all 8 name a source and authority; every read path resolves
PROJECTION             SATISFIED   8 projections, each carrying source, time, transformation
CONSUMER               SATISFIED   2 evidenced consumers of 3 importers
```

---

## 2. What `§16` actually says

[A] `§16 State Consumers`, read from the instrument body — `ACT-CC-P12-008 §3`
required exactly this and forbade inferring it from an identifier, an index row,
a search hit, an existing implementation, or a previous report's wording:

> P12 shall discover actual consumers rather than assume them.
> Consumers may include:
> * runtime;
> * workflow;
> * organization;
> * governance;
> * **verification**;
> * **self-model**;
> * **observability**;
> * **evidence**;
> * reconciliation.
>
> Each claimed consumer requires evidence that it actually consumes the state.

[D] Two findings follow, and they pull in opposite directions — which is why
reading the section mattered rather than reasoning about it.

1. **`verification` and `self-model` are named consumer kinds.**
   `ACT-CC-P12-006 O8` and `ACT-CC-P12-007 O19` both recorded *"does a verifier
   count as a consumer?"* as **semantically unsettled**. It was not unsettled.
   It was answered in the instrument, in a list those Acts did not read. The
   prior classification was taken from `tools/p12_state_verification.py`'s own
   docstring, which quotes `§16`'s **first and last sentences and omits the
   enumeration between them** — a paraphrase read as the source.

2. **Being a named kind is not sufficient.** The closing sentence requires
   *evidence that it actually consumes the state*. Import is not that evidence.

[C] So the corrected measurement answers two questions and keeps them apart:

```text
who imports the surface        →  importers_of()   3
who actually consumes it (§16) →  consumers_of()   2
```

---

## 3. The defect, precisely

[E] The superseded implementation, in full:

```python
if isinstance(node, ast.ImportFrom) and node.module:
    modules = [node.module]
elif isinstance(node, ast.Import):
    modules = [alias.name for alias in node.names]
if any(stem in module for module in modules):
```

[D] **One expression, two opposite defects.**

| | |
|---|---|
| **False negative** | For `from tools import p12_operational_state as state`, `node.module` is `"tools"`. `"p12_operational_state" in "tools"` is `False`. This is the form **every** resident importer uses, so the measurement reported zero consumers for a surface that has real ones. |
| **False positive** | `stem in module` is a substring test. `"p12_operational_state" in "tools.p12_operational_state_verifier"` is `True`. A module importing only the *verifier* would have counted as a consumer of the *surface*. |

[E] Both are controlled now: `NC01` drives five import shapes through the
corrected resolver; `NC03` proves a prefix name is a different module and keeps
the old expression's truth (`assertIn("p12_operational_state",
"tools.p12_operational_state_verifier")`) as a standing reminder of what it did.

---

## 4. The correction

[C] Import resolution is by **module identity**, across the five shapes the
repository actually demonstrates:

```python
from pkg import surface            from pkg import surface as s
import pkg.surface                 import pkg.surface as s
from pkg.surface import project
```

[C] Consumption evidence is `§16`'s closing sentence made measurable. A read is
a call to the surface's projection API — `project`, `conflicts`, `declares`,
`summary` — and a read made inside a `with` block that substitutes the surface
is recorded as a **fixture read**, separately, not dropped and not counted:

```python
@dataclass(frozen=True)
class ConsumerEvidence:
    module: str
    reads: Tuple[str, ...]           # over the resident sources
    fixture_reads: Tuple[str, ...]   # over a substituted source set
```

[D] `ACT-CC-P12-008 §11`: `TEST ≠ REAL SYSTEM WORK`. Replacing `SOURCES` and
then calling `project()` reads your own fixture. That is a legitimate thing for
a negative control to do and it is not evidence of consuming the system's state.

---

## 5. The measured result

| Module | `§16` kind | Reads (resident) | Reads (fixture) | Consumer? |
|---|---|---|---|---|
| `tools/p12_self_model_contract.py` | **self-model** | `project` | — | **YES** |
| `tools/p12_negative_control_verification.py` | **verification** | `summary` | `project` | **YES** |
| `tools/p12_mutation_verification.py` | verification | — | `conflicts` | **NO** — every read is over a substituted source set |

[E] `p12_self_model_contract.projection_freshness_is_not_source_freshness()`
reads `w2.project()` and uses `entries["runtime.observed"].observed_at` and
`.status` to answer a W5 question. That is a self-model consuming the
projection, which is `§16`'s second-named kind doing the thing `§16` describes.

---

## 6. Independent verification — by observation, not a second parse

[A] `ACT-CC-P12-008 §4.1.C`: the verifier *"MUST NOT simply reproduce the same
implementation logic in a different function and call that independence."*

[C] `tools/p12_consumer_evidence_verifier.py` does not parse Python and imports
nothing from the measurement. It wraps the surface's projection entry points
with a recorder, **actually calls** each candidate's own function, and records
for every projection call whether `surface.SOURCES` **is** the resident tuple at
that moment — identity, not equality. The AST infers substitution from a `with`
block's extent; this watches it happen.

```text
p12_self_model_contract.projection_freshness_is_not_source_freshness
    resident=['project']                        substituted=[]
p12_negative_control_verification._operational_state_projection
    resident=['conflicts','project','summary']  substituted=['project']
p12_mutation_verification._alter_state_authority
    resident=[]                                 substituted=['conflicts']
```

[E] Four checks, **4 AGREES / 0 DISAGREES / 0 UNOBSERVABLE**, reproduced in a
fresh process. The claim is **passed in** rather than imported, which is how the
module stays independent of the one it checks.

---

## 7. What this does **not** establish

[D] `ACT-CC-P12-008 §11` requires these kept apart, and they are:

```text
COMPONENT EXISTS ≠ CONSUMED ≠ EXECUTED ≠ INTEGRATION VERIFIED
```

| | |
|---|---|
| The surface **exists** and is **provisioned** | yes |
| It is **consumed** — two modules read the projection | yes, evidenced two ways |
| It is **executed by real system work** | **NO.** Both consumers are verification surfaces. No delegation, execution or coordination run reads the projection |
| It is **operational** | **NO.** Nothing runs unattended; `OA-1` holds |

[D] `§16` names `verification` a consumer kind, so the `CONSUMER` link is
satisfied on the instrument's own terms. It does **not** follow that the
projection is exercised by the system doing work. That remains `NOT EXERCISED`
and is reported rather than manufactured — `§9` forbids creating a synthetic
operational path to improve the figure, and none was created.

[D] `W6 CLASSIFICATION ≠ P12 CERTIFICATION`. One `§19` scope item's chain is
complete. Twelve others are unchanged.
