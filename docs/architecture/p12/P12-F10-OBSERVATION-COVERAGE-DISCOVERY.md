# P12 F-10 — Observation Coverage & Historical Evidence Integrity · discovery

> **Classification: `Y7` — F-10 DEEPER FRONTIER DISCOVERED.**
>
> **No construction was performed. No historical record was changed.**
> `historical rewrite = 0` · code changes = 0 · `P12 CONSTRUCTED = FALSE`.

---

## 1. Baseline (Gate A) — measured before any action

```text
HEAD 4f8c4d9 · non-protected dirty 0 · protected untracked 13 · Native Core 11
native_core 801 OK (1 expected failure) · consumers 276 OK · tools 778 OK = 1855
citation 208 / 0 errors · stale-state 505 / 0 assertions
self-model 10 VERIFIED · 2 INFERRED · 0 UNKNOWN
observations 2 · live_by_kind {runtime: (), workflow: ()}
```

---

## 2. The hypothesis did not survive (Gates C, J)

**Original F-10:** *"Runtime observation covers 1 of 3 resident runtime paths."*

Three falsifications, all measured:

### `J-1` — the denominator counts the wrong unit

Canon does not measure coverage in scripts. `§46` sets the verification matrix
***"For every phase"***; `§47` says *"the actual graph governs"*. A count of
files that construct an `AIOSRuntime` is an artifact of repository layout, not a
canonical population.

### `J-2` — the one "covered" path performs no work

| Path | delegated-work references | publishes observation |
|---|---|---|
| `w1_coordination_proof.py` | **9** | no |
| `cross_department_coordination_proof.py` | **15** | no |
| `p12_runtime_observation_proof.py` | **0** | yes |

The single path counted as coverage is the one that **does nothing but
demonstrate observation**. Restated honestly:

```text
0 of 2 work-performing runtime paths publish observation
```

**That is a worse result than "1 of 3", and my own earlier framing flattered it**
by counting the demonstrator as coverage.

### `J-3` — per-path publication is not canonically required

`§30`: *"Claims about runtime integration require runtime evidence **where
runtime evidence is the relevant proof**"* — conditional, not blanket. `§18`
requires the self-model answer *"What is running?"* evidence-backed; it does not
require every path to publish. **No canonical clause mandates per-path
publication.** Under Gate D, the absence of publication is therefore not, by
itself, a defect.

---

## 3. What *is* canonically grounded (Gate G)

`§45`: *"W6 verifies P4–P11 as an integrated operating system. Verification must
test relationships, not only isolated components."*
`§48`: **"A relationship is not considered verified merely because both surfaces
exist."**

A demonstrator proves that a work surface and an observation surface **can** be
wired. It does not verify the **relationship** between the system's actual work
paths and observation — because that relationship does not exist. So the real
gap is not coverage arithmetic; it is that `W6`'s `RUNTIME` and `WORKFLOW`
verification scope **cannot be satisfied by demonstrators**.

| Work package | Observation required? | Basis |
|---|---|---|
| `W1` Coordination | **NOT ESTABLISHED** | W1 needs coordination and workflow evidence; `§30`'s runtime-evidence clause is conditional and its condition is not met |
| `W3` Governance Integration | **NOT ESTABLISHED** | governance decision/authority/delegation/escalation evidence is not runtime observation, and neither converts into the other |
| `W6` System-wide Verification | **REQUIRED** | `§45` + `§48` — relationship verification, with `RUNTIME` and `WORKFLOW` named in the `§19` minimum scope |

---

## 4. The programme hypothesis survived, and sharpened (Gate I)

It was to be attacked, not assumed. Measured across every observation surface,
counting **non-test resident callers only**:

| Surface | Canonical home | Resident non-test caller |
|---|---|---|
| `TraceWriter` supplied to an agent | `native_core/core/trace` | **only** `p12_trace_durability_proof.py` |
| `WorkflowMonitor` constructed | `native_core/core/workflow` | **only** `p12_workflow_observation_proof.py` |
| runtime observation `publish()` | `tools/p12_runtime_observation.py` | **only** the two proofs above |

**Three surfaces. Three callers. All three are proofs written to demonstrate the
surface they call.**

The earlier statement — *"capability that nothing reaches"* — was too generous.
The accurate one is:

```text
CAPABILITY REACHED ONLY BY ITS OWN DEMONSTRATOR
```

**This narrows my own three closures.** `F-3`, `F-4` and `F-11` each closed
against what they actually asked — does durable Trace survive a process, can the
system distinguish live from historical, is Workflow state projectable — and each
answer stands. **None of them established that the system's work is observed**,
and the frontier list was measuring surface existence while reading as
integration. Recorded because the distinction was invisible until the
demonstrator/work-path split was measured.

---

## 5. Historical evidence integrity (Gate K) — and a new hazard

Both work paths write **tracked, dated** records:

```text
w1-coordination.evidence.json          executed_at 2026-09-11T07:33:36Z
cross-department.evidence.json         executed_at 2026-09-11T09:57:01Z
```

`tools/w1_coordination_run.py:215` **overwrites** the evidence file, and each run
mints a fresh `uuid4` delegation record. Eight already exist — `03:32 → 07:33` on
2026-09-11, **seven `REVOKED`, one `ACTIVE`** — and the evidence file carries
**four commits**. The path was *designed* to be re-runnable, and during P11
construction that was ordinary.

**`F-12` — post-certification re-execution hazard.** `FD-P11-002` certified P11
on 2026-09-11. The same re-run that was ordinary during construction now
**overwrites certified-phase evidence** and supersedes the one `ACTIVE`
delegation. **No guard exists** — the only hit for `certified|frozen|immutable|
read-only` in those modules is an unrelated resource-boundary string.

The operation did not change. Its meaning did, at certification, and nothing in
the repository noticed.

**This is why no execution was performed in this Act.** Gate M permits a real
execution for measurement; doing so here would have rewritten a certified record
to measure whether certified records are at risk.

---

## 6. Coverage matrix (Gate R)

| Path | Exists | Canonically requires observation | Observation capability | Resident caller | Real execution observed | Independent observation | Freshness | W5 visibility | Status |
|---|---|---|---|---|---|---|---|---|---|
| `w1_coordination_proof.py` | YES | **NOT ESTABLISHED** (W1) / **REQUIRED** (W6 relationship) | YES — unused | NO | NO | NO | N/A | NO | **GAP — W6 only** |
| `cross_department_coordination_proof.py` | YES | as above | YES — unused | NO | NO | NO | N/A | NO | **GAP — W6 only** |
| `p12_runtime_observation_proof.py` | YES | NO — it is the demonstrator | YES | YES (itself) | YES | YES | LIVE→TERMINATED | YES | NOT COVERAGE |
| `p12_workflow_observation_proof.py` | YES | NO — demonstrator | YES | YES (itself) | YES | YES | LIVE→TERMINATED | YES | NOT COVERAGE |
| `p12_trace_durability_proof.py` | YES | NO — demonstrator | YES | YES (itself) | YES | YES | durable/historical | YES | NOT COVERAGE |

This matrix is evidence, **not an authority source**.

---

## 7. Defects and disclosures (Gate V)

| Defect | Class |
|---|---|
| F-10 stated as "1 of 3", counting the demonstrator as coverage | **INTRODUCED** (mine, prior Act) · **CORRECTED** here · NON-VERDICT-AFFECTING |
| Frontier list measured surface existence, read as integration | **INTRODUCED** (mine) · **DISCLOSED**, narrows `F-3`/`F-4`/`F-11` without invalidating them |
| Post-certification re-execution hazard | **PRE-EXISTING** · newly discovered · recorded as `F-12` |
| *"capability nothing reaches"* too generous | **CORRECTED** to *"reached only by its own demonstrator"* |

---

## 8. Fresh rediscovery (Gate X)

| ID | Frontier | Class |
|---|---|---|
| `F-10′` | `W6` cannot verify the RUNTIME/WORKFLOW relationship: no work-performing path is observed | **AUTHORIZED INTEGRATION GAP** — bounded, not yet executed |
| `F-12` | Re-running any P11 proof overwrites certified evidence; no guard exists | **EVIDENCE-INTEGRITY GAP** — authorized, and a prerequisite for closing `F-10′` |
| `F-13` | W5's *"What is running?"* scope is accurate but its observed population is entirely demonstrators — true and near-useless | **AUTHORIZED ACTIONABLE** — classified, not built (Gate T) |

**`F-12` must be settled before `F-10′`.** Closing `F-10′` means making work paths
publish, which means running them, which today rewrites certified evidence. The
ordering is forced by the evidence, not chosen.

---

## 9. Final

```text
F-10 CLASSIFICATION       Y7 — DEEPER FRONTIER DISCOVERED
historical rewrite        0
code changes              0
real executions performed 0   (deliberately — see §5)
protected read/stage/commit/modify/relocate/delete/authority   0
P12 CONSTRUCTED = FALSE · VERIFIED = FALSE · E12 NOT RATIFIED · P13 NOT AUTHORIZED
```
