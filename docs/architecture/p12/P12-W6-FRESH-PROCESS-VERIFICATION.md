# P12-W6 — fresh-process verification (`§52`)

> **8 of 8 stages reproduced. 0 diverged.** `P12 CONSTRUCTED = FALSE` ·
> `E12 RATIFIED = FALSE` — nothing here depends on ratification, and nothing
> here asserts a threshold.

---

## 1. The requirement

`§52`: *"Material P12 claims must survive fresh-process reconstruction where
applicable"*, across `repository → canonical sources → registries → state →
decisions → integration graph → runtime → evidence`, and — the clause that gives
the check its point — ***"without relying on hidden conversational state."***

`§19` names `FRESH PROCESS` in W6's minimum scope. Pieces of it existed
(`e11_measurement` shells out; `w4_first_run` mentions it); **no phase-level
verifier covered the eight stages.**

## 2. Why it is not ceremony

Every P12 claim in this corpus was produced inside one very long session. A
figure computed there can be right for reasons that do not survive the session —
a module imported earlier, a file written mid-run, a value held in a live object.
The only way to tell a reproducible claim from a session-dependent one is to
recompute it **in an interpreter that never saw the session**.

Each stage is therefore derived **twice**: once here, once in a subprocess that
receives no object, no module reference and no value from this process — only the
repository path. Agreement means the claim is reconstructible from the repository
alone. Disagreement would mean a claim leaning on something the repository does
not carry.

## 3. Result

```text
repository           REPRODUCED   513 tracked markdown documents
canonical sources    REPRODUCED   blueprint sha256 62b6c28971219611…
registries           REPRODUCED   435 governance index records
state                REPRODUCED   12 questions · 10 VERIFIED · 2 INFERRED · 0 UNKNOWN
decisions            REPRODUCED   54
integration graph    REPRODUCED   14 edges, acyclic
runtime              REPRODUCED   3 observations
evidence             REPRODUCED   2 durable Trace records

stages 8 · reproduced 8 · diverged 0 · unavailable 0
```

**No P12 claim in this corpus depends on session state.**

## 4. Eight-of-eight is the result a broken comparator also gives

So the comparator is proved able to fail:

| Control | Result |
|---|---|
| inject a value differing from every stage | **all 8 report `DIVERGED`** |
| make the subprocess fail | **all 8 report `UNAVAILABLE`**, none `REPRODUCED` |
| summary under injected divergence | `diverged == stages`, `reproduced == 0` |

A subprocess that cannot run must never read as agreement — that control exists
because *"the child failed"* and *"the values match"* are easy to conflate and
produce opposite meanings.

## 5. Reproducibility is not adequacy

Whether these values **satisfy** `E12-06` is a measurable interpretation only
Founder ratification supplies (`§53`, `F-16`). This module reports that the
claims reconstruct; it asserts no threshold and returns no pass/fail verdict, and
a test holds it to that.

## 6. Verification

```text
native_core 801 OK (1 expected failure) · consumers 276 OK · tools 825 OK = 1902
   tools +10 — fresh-process conformance, including the mutation control
citation 219 documents / 1163 citations / 0 errors · stale-state 513 / 0
historical rewrite 0 · protected read 0 · Native Core 11
```

## 7. `W6` scope after this increment

```text
CROSS-PHASE CONTRACTS   addressed   (exercise verifier)
FRESH PROCESS           addressed   (this)
CROSS-PD INTERFACES     not built
MUTATION                per-module only, not phase level
REGRESSION              per-module only, not phase level
RUNTIME · WORKFLOW · GOVERNANCE · STATE · EVIDENCE · PROVENANCE · FAILURE
                        partial, via the surfaces built in F-3/F-4/F-10′/F-11/F-12
```

**`W6` remains incomplete**, and `§19` is explicit that green tests do not close
it.
