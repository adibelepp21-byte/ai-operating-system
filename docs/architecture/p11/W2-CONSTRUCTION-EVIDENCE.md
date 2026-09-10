# W2 Construction Evidence — `ACT-CC-P11-005`

> **Verdict: `T2` — W2 CONSTRUCTED WITH NON-BLOCKING RESERVED FRONTIERS.**
> `E-W2-01` … `E-W2-20` below. Implementation `tools/planning/` · **83 tests**
> across three suites, every control mutation-tested.
>
> `W2 CONSTRUCTED ≠ E11 RATIFIED` · `P11 CONSTRUCTED = PARTIAL`.

---

## Authority state, read from actual bodies (`§1`, `§4`)

Verified by reading each instrument's own `Status:` line, not by identifier.
`IDENTIFIER ≠ DECISION BODY` · `FILENAME ≠ CANONICAL STATUS`.

```text
DP-04 = ISSUED   (DP-04-P11-ORGANIZATIONAL-ENTITY-MODEL.md:77)
DP-03 = ISSUED   (DP-03-P11-ORGANIZATIONAL-ARCHITECTURAL-SURFACE.md:77)
DP-01 = ISSUED   (DP-01-P11-FOUNDER-AUTHORIZATION.md:66)

P11 AUTHORIZED = TRUE      P11 CONSTRUCTED = PARTIAL
W2 CONSTRUCTED = TRUE      E11 RATIFIED    = FALSE
P12 AUTHORIZED = FALSE     Native Core     = 11 frozen boundaries
```

**No contradiction with the expected state was found**, so construction
proceeded rather than stopping under `§1`.

---

## Evidence register

| ID | Requirement | Evidence |
|---|---|---|
| `E-W2-01` | DP-04 body verified | `§8.1` Goal, `§8.2` Plan read in full; `GOAL → PLAN → DELEGATION → EXECUTION` |
| `E-W2-02` | DP-03 `§8.4` verified | read in full; `ORGANIZATIONAL-LAYER PLANNING SURFACE` + mutable lifecycle mandate |
| `E-W2-03` | DP-01 W2 authorization verified | `§3 W2` read in full; seven permitted capabilities, reserved frontier restated |
| `E-W2-04` | Goal representation | `tools/planning/goal.py` — frozen, no state, no permission method |
| `E-W2-05` | Plan representation | `tools/planning/plan.py` — frozen version, chain-linked |
| `E-W2-06` | `PLAN` | `ThePlanStepOfTheLifecycle` — 3 tests |
| `E-W2-07` | `SEQUENCE` | `TheSequenceStepOfTheLifecycle` — 4 tests, incl. cycle refusal |
| `E-W2-08` | `ADAPT` | `TheAdaptStepOfTheLifecycle` — 4 tests |
| `E-W2-09` | `REVISE` | `TheReviseStepOfTheLifecycle` — 5 tests |
| `E-W2-10` | Plan provenance | citation carried unchanged through every successor; `NC-W2-14/15` |
| `E-W2-11` | Workflow interface | `prepare_for_workflow()`; vocabularies proven disjoint; `NC-W2-16`, Test E |
| `E-W2-12` | W3 Delegation interface | `delegation_requirements()`; W3 rejects Planning's best record — Test D |
| `E-W2-13` | Observation evidence path | `PlanningEvidence` recorded as motivation; `NC-W2-09…12` |
| `E-W2-14` | Observation cannot authorize | 20 observations authorize as much as 0 — Test F |
| `E-W2-15` | Reserved frontier bounded | no ranking field, no ranking callable; Test G |
| `E-W2-16` | Negative controls executed | 36 tests, `NC-W2-01` … `NC-W2-24` |
| `E-W2-17` | Prove-me-wrong executed | 27 tests, Tests A–K, **every attack failed** |
| `E-W2-18` | Persistence | implementation, tests, this package, architecture record — all committed |
| `E-W2-19` | Repository integrity | citation 143 docs / 0 errors · stale-state 0 assertions · core = 11 |
| `E-W2-20` | Exhaustion | `§26` classification below |

---

## Prove-me-wrong results (`§20`)

**All eleven attacks failed to break the architecture.** Each is an attempt, not
a demonstration.

| | Attack | Outcome |
|---|---|---|
| A | Show the representation is a static P10-style record | **failed** — 3 versions coexist; overwrite raises `FrozenInstanceError` |
| B | Show Goal collapsed into a Core entity or authority | **failed** — not a `Department`, not a `HumanAuthority`, not in core |
| C | Make Plan existence/readiness authorize execution | **failed** — no permission method; 4 revisions still escalate |
| D | Make Planning create or impersonate a delegation | **failed** — W3 rejects Planning's most generous record |
| E | Make Planning silently become Workflow | **failed** — no execution state, no transition, no entry point |
| F | Make evidence authorize | **failed** — 20 observations, and a source claiming *"founder"*, change nothing |
| G | Make sequencing become ranking | **failed** — order follows declaration against every metric |
| H | Use adaptation to expand authority | **failed** — escalates; a forged wider-authority successor is refused |
| I | Revise while erasing previous state | **failed** — no delete path; unexplained revision refused |
| J | Make planning state the P12 unified state | **failed** — surface holds goals and chains only |
| K | Satisfy W2 with a twelfth Native Core boundary | **failed** — satisfied with the core untouched |

### Controls proven able to fire

Zero failures from a suite that has never failed is not evidence. Each control
was broken deliberately:

```text
Plan becomes mutable                   -> FAILED
sequence() ranks by statement length   -> FAILED (2)
Plan gains is_authorized()             -> FAILED (3)
escalation becomes a warning           -> FAILED (10, +3 errors)
adapt() gains an authority parameter   -> FAILED
DelegationRequirement gains delegator  -> FAILED
```

**Two of my first six probes were defective and are recorded as such.** The
`adapt()` probe used a walrus expression that evaluated back to the original
value — a no-op that reported `OK` and would have been read as *"this control
cannot fire."* The delegator probe placed a defaulted field before a
non-defaulted one, so the suite **errored** rather than failing, producing no
verdict line at all. Both were rewritten and both then failed the suite
correctly. **A defective probe reporting `OK` is indistinguishable from a
genuinely dead control**, which is why the first results are printed here beside
the corrected ones rather than replaced by them.

---

## `§26` exhaustion classification

| Remaining item | Class | Note |
|---|---|---|
| Persisted plan-record directory | **OUT OF SCOPE** | `DP-03 §8.4` permits records *where appropriate*; the lifecycle is a runtime chain. Creating a store for records that will never exist is cosmetic construction |
| Prioritization / ranking / heuristics | **RESERVED** | `DP-01 §3 W2` holds the frontier; not required by any authorized W2 capability, so non-blocking (`§13`) |
| Organizational-layer top-level region | **AUTHORIZED + BLOCKED** | `consumers/` needed `DEC-P6-042`; a fifth region needs its own decision (`§28`, `§34.3`). Reported, not taken |
| Five citation findings under `tools/` | **FALSE POSITIVE** | auditor's own grammar examples, its `ILLUSTRATIVE` worked example, and the VF-11 fixture that must not resolve |
| W1/W4/W5/W6 packages | **OUT OF SCOPE** | this Act governs *"only the W2 frontier"* (`§0`) |

**No `AUTHORIZED + ACTIONABLE` item remains within the W2 frontier.**

---

## `§23` source integrity — with the meaning of each metric stated

```text
roots     : docs/architecture/platform-organization · docs/architecture/candidates
            docs/governance · docs/architecture/p11 · docs/architecture/organization
            tools/planning                                    ← added by this Act
documents : 143          citation errors : 0
stale-state: 463 documents / 0 stale assertions
```

**What these numbers mean, precisely.**

`0 citation errors` means every file-shaped pointer in the audited roots resolves
to a real file. **It does not mean the cited sources support the claims made
about them** — that reading is a human act, and the auditor prints the
disclaimer itself.

`0 stale assertions` means **no claim recorded as superseded in the Register is
restated.** It is *not* a proof that the corpus is clean. The audit tests only
registered claims, so a claim superseded in the same act that supersedes it is
invisible to it — a limit found in `§86.8` and restated here rather than
allowed to fade.

### A blind spot this Act closed

`§23` requires roots covering *"all repository surfaces that materially
participate."* Applying it revealed that the auditor scanned **`*.md` only**.
W2's decisive citations — `DP-01 §3 W2`, `DP-03 §8.4`, `DP-04 §8.2` — live in
module docstrings and **had never been auditable at all.** Neither had any
docstring citation anywhere in this repository.

Python is now scanned, and `tools/planning` is a root. Measured before deciding:
`tools/planning` 6 documents / 0 errors, `native_core` 122 / 0, `tools` 54 / **5**
— the five being the auditor documenting its own citation grammar, its
`ILLUSTRATIVE` worked example, and the VF-11 regression fixture that exists
*because* it must not resolve. **Clearing them would mean five exemptions added
so the tool could read itself**, which is the pressure the registries are written
to resist. Scoped to W2 as `§23` asks; the rest is recorded, not silently
widened (`§28`).

---

## Defects (`§33 F`)

| Defect | Impact | Action | Status |
|---|---|---|---|
| Citation auditor read `*.md` only | every docstring citation in the repository unverifiable, including all of W2's | extended to `*.py`; `tools/planning` added as a root; guards added | **FIXED** |
| Two of six mutation probes defective | one reported `OK` for a live control; one errored, printing no verdict | both rewritten; both then failed correctly | **FIXED, disclosed** |
| Five citation findings under `tools/` | none — all false positives of the self-reference class | classified, recorded, left for a change that is about them | **OPEN, classified** |
| Dangling markdown link reference in the W2 record | cosmetic | corrected before commit | **FIXED** |

**No defect changed authority semantics.** None was silently repaired.

---

## What this evidence does not establish

`W2 CONSTRUCTED ≠ E11 RATIFIED` and `W2 VERIFIED ≠ E11 RATIFIED` (`§29`).
`DP-02` remains a separate Founder decision.

Three of seven P11 packages are now touched — W3 (mechanism, empty population),
W7 (controls, no capability), W2 (this). `DP-01 §13`: authorization is not
construction, operational, verified, exhausted, complete or certified.

`P11 PLANNING STATE ≠ P12 UNIFIED OPERATIONAL STATE` (`§30`).
Native Core remains at **11** frozen boundaries (`§31`).
