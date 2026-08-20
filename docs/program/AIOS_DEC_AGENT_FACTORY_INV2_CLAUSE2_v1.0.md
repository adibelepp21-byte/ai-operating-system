# `DEC-AGENT-FACTORY-INV2-CLAUSE2` — Decision Record & Execution Record

> **NOT CANONICAL.** `ACT-CC-F03-040 §20` [E]: *"The conversational decision
> must not automatically be promoted into a canonical governance artifact unless
> the Founder separately authorizes that canonicalization."* No such
> authorization was given, so this is a **recorded** decision, not a canonical
> governance artifact. It ratifies nothing.

**Recorded under:** FOUNDER · `ACT-CC-F03-040 §20` · **Recording date:** 2026-08-21

---

## 1. Decision record (`§20`)

| Field | Value |
|---|---|
| **DECISION ID** | `DEC-AGENT-FACTORY-INV2-CLAUSE2` |
| **DECISION** | **OPTION A — AUTHORIZE** |
| **FOUNDER** | Moriarty |
| **DATE** | 21-08-2026 |
| **PROVENANCE** | Founder Decision supplied in the `§4` block of `ACT-CC-F03-040` |
| **SCOPE** | Agent Factory / INV-2 Clause 2 |
| **AUTHORITY** | Construction authorization only |

Transcribed from `§4` as supplied:

```text
DECISION ID: DEC-AGENT-FACTORY-INV2-CLAUSE2
Founder Decision: OPTION A — AUTHORIZE
[ X] OPTION A — AUTHORIZE
Founder: Moriaty.
Date: 21-08-2026
Signature / Confirmation: Moriarty. 
```

Exactly one option was checked. The decision was **not** inferred from any of
the sources `§4` forbids. **[O]** The `Founder:` line reads *"Moriaty."* and the
confirmation reads *"Moriarty."*; recorded as supplied, not corrected.

## 2. `§7`/`§8` — what the reservation meant, established from source first

`§8` requires the reservation be classified from resident evidence before
construction. Of its four readings, the evidence gives **reading 2 — the
relationship is ratified, its realization was reserved**:

| Source | Statement |
|---|---|
| Freeze **INV-2** | *"Every Agent Definition is owned by exactly one Department **and implements at least one Capability**."* |
| Freeze §4 — Capability | *"Allowed: **be implemented by Agent Definitions**"*; *"Forbidden [E]: … existing with zero implementers as a steady state (INV-14)"* |
| Freeze **INV-14** | *"A Capability with zero active Agent Definitions implementing it is an invalid steady state and must be flagged for governance review."* |
| `agent_spec §2` | **[E]** *"An Agent Definition implements ≥1 Capability (INV-2)"* |
| `agent_spec §10` | **[E]** *"Capability implementation counts toward INV-14"* |
| `agent_spec §11` | **[A]** *"Definition without an implemented Capability is invalid (INV-2/14) and flagged for governance"* |
| `agent_spec §12`/`§13` | **[O]** *"Agent **construction** discipline…"* — governed creation, registration, validation |

The entity is ratified; the relationship is ratified; only the *realization* —
the *"validated against Capabilities"* surface — was reserved. Option A opened
exactly that.

### 2.1 A discrepancy in this Act, resolved from canonical source

**[E]** `ACT-CC-F03-040 §2` and `§9` describe INV-2 clause 2 as
*"Agent Definition → owning Department"* / *"declares / resolves owning
Department"*. **That is clause 1, not clause 2**, and it was already complete at
`bc34d2e` under `ACT-CC-F03-039`.

INV-2 verbatim splits as: **clause 1** *"owned by exactly one Department"* ·
**clause 2** *"and implements at least one Capability"*.

`§8` [E] directs that *"Claude Code must not treat a historical docstring,
roadmap statement, or previous interpretation as superior to canonical
evidence."* Canonical evidence governs, so **clause 2 was built as INV-2
actually states it** — the implementer edge — which is also the only remaining
reserved item the Act's `§1` purpose describes as *"menghalangi INV-2 Clause 2"*.
The outcome sketched in `§9` was verified as already satisfied rather than
rebuilt. The discrepancy is reported, not silently resolved; the label in `§2`
and `§9` most likely derives from `ACT-CC-F03-038`'s frontier report, drafted
before `-039` completed clause 1.

## 3. Implementation (`§9`, `§12`)

- **`AgentDefinition.implemented_capabilities: Tuple[str, ...]`** — **at least
  one**, distinct, non-empty text; fails closed (PR-4) on an empty tuple, a
  non-tuple, a non-text member, and a duplicate. This *is* INV-2 clause 2 as
  stated, at the only place a single Definition can assert it.
- **`CapabilityGraph`** — the corpus view no single Definition can see:
  `implementer_counts` (one Definition counts once per Capability however often
  it repeats the key), `implementers_of`, `unknown_implemented_capabilities`
  (flagged, never raised — PR-3). These feed the existing
  `orphan_capabilities`, so the **INV-14 loop now closes from what Definitions
  actually declare** instead of from a hand-assembled mapping.
- Declarations are plain `(agent_definition_key, capability_keys)` pairs.
  Verified by AST that **neither package imports the other**.

**Implementation location** was determined, not assumed: the per-Definition
invariant belongs on the Definition contract; the corpus invariant belongs on
the graph that already owns INV-14. No new module, no new boundary.

## 4. Verification (`§13`)

| Check | Result |
|---|---|
| **V-01** Decision recorded exactly as supplied | PASS — verbatim, typo included |
| **V-02** INV-2 clause 2 satisfied | PASS — *at least one* enforced; 6 malformed inputs refused |
| **V-03** INV-2 clause 1 regression | PASS — ownership and `resolve_agent_definitions` re-probed |
| **V-04** Failure closure | PASS — PR-4 on every invalid declaration |
| **V-05** PR-3 / PR-4 distinction consistent | PASS — per-Definition facts raise; corpus facts flag |
| **V-06** Boundary integrity | PASS — core region **11** |
| **V-07** Agent forbidden-boundary constraints | PASS — AST-verified, no `capability` import |
| **V-08** Protected state | PASS — four artifacts hash-identical |
| **V-09** Regression | `native_core` **566 OK** (1 expected failure) · `tools` **20 OK** · `bounded_exception` **29 OK** |
| **V-10** Independent verification | PASS — outcome exercised outside the suite |

**`P7-F-2` / `GDR-0014`** untouched, still the sole expected failure (`§17`).

## 5. Conformance test discipline (`§14`)

Four tests updated, each toward its own cited authority; **none weakened**.

- The Definition **shape** test — its basis is `agent_spec §3`/`§4`; `§2` states
  the implements-≥1 relationship the new field carries. Renamed to match.
- `test_every_field_is_required` — **extended**, adding a third arity case.
- The **halt-message guard count** 5 → 9, under its own stated rule *"one guard
  per declared field"*. **[E] My first estimate was 8 and was wrong** — a
  collection-valued field needs four guards, not three. Corrected against
  measurement, disclosed rather than quietly adjusted. The string assertion the
  test exists to make is untouched and covers all nine.
- The **stdlib allowlist** gained `typing`, for `Tuple[str, ...]`. Its basis is
  INV-12 — *"Tool is the only entity permitted an external dependency"* — and
  `typing` is stdlib, which the same test re-checks independently against
  `sys.stdlib_module_names`. The guard remains real.

**Not touched:** the eleven-boundary constraint, the reserved-structure guard,
and the Agent boundary's forbidden-boundary set.

**[E] A conformance test was respected rather than amended.** The Agent
boundary forbids all assignment beyond field declarations — *"it stores nothing
and mutates nothing."* My duplicate check used a local accumulator and tripped
it. The **implementation** was rewritten as an assignment-free comparison; the
test stands unmodified.

## 6. Specification synchronization (`§15`)

`department_spec §13` and `AIOS_CONSTRUCTION_FRONTIER_v1.0.md` updated to record
T-11 complete and to state that clause 2 is **not** a Department fact. No new
architectural meaning was introduced, and no governance authority was altered.
**`agent_spec` was not modified** — `§2`, `§10` and `§11` already state the
relationship. No `[O]` was converted to `[E]`.

## 7. External research (`§16`)

**External Research: NOT USED.**

## 8. Boundary compliance (`§6`, `§19`)

No canonical entity created · no core boundary created · Constitution,
Architecture Freeze, Canonical Domain Model unmodified · INV-2's meaning
unchanged · no governance register mutated · PD-02, AGC, `DEC-AE04`,
`DEC-REVOCATION`, `DEC-ADOPTION`, `OB-01` untouched · Planner, Scheduler,
Execution Orchestrator, Intelligence **not** constructed · Agent lifecycle,
Agent Instance, Department, Capability, Workflow, Runtime, Knowledge, Memory and
Tool **not** redesigned.

**Reservation exercised:** the *"validated against Capabilities"* surface only.
Governed **creation, registration and lifecycle** of Agent Definitions remain
`[O]` reserved to the Architect and unbuilt.

## 9. Remaining frontier

**[A]** No non-reserved engineering gap remains in the Capability boundary, its
ownership context, or the INV-2 edge. **T-2**, **T-3**, **T-12** are
`[O]`-reserved to the Architect; **T-4** is blocked on Founder-reserved
authority entangled with `OB-01`; **T-5**–**T-8** are unratified and excluded.

**[D]** The next increment requires a decision, not further engineering.
