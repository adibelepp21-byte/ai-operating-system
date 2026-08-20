# `DEC-AGENT-DEPT-OWNERSHIP` — Founder Decision & Execution Record

**Recorded under:** FOUNDER · `ACT-CC-F03-039 §16`, `§21`, `§23` · **Date:** 2026-08-21
**Status:** **CANONICAL — DECIDED**, and executed.

> Records an already-made Founder decision and its execution. Ratifies nothing.

---

## 1. Founder decision — consumed exactly as supplied (`§23.1`)

Transcribed verbatim from the Act's `§3` Founder Decision Block:

```text
DEC-AGENT-DEPT-OWNERSHIP = OPTION A — AUTHORIZE
Founder: Moriarty.
Date: 21-07-2026
Signature / Confirmation: Moriarty.
```

**Provenance.** Supplied and signed by the Founder in the `§3` block of
`ACT-CC-F03-039`, an Act whose header status read *"FOUNDER DECISION REQUIRED"*
and which was returned filled after a first issuance in which every decision
field was blank. **Claude Code did not select the option**, and no branch was
inferred at any point: the first issuance was answered with a report of the
blank fields and the exact minimal action required, not with work.

**[O] Two observations recorded, neither corrected** — the decision is consumed
exactly as supplied (`§23.1`), and no successor may reinterpret it (`§23`):
1. The Act's `§21` duplicate Founder Decision Record remains unchecked and
   unsigned. The `§3` block is filled and signed; the two are the same decision.
2. The date reads **21-07-2026**. Adjacent decisions are dated 21-08-2026, and
   the recording date is 2026-08-21, so 21-07 falls a month before them.
   Transcribed as given.

## 2. Authorized scope (`§23.2`)

Option A authorizes realizing INV-2 clause 1 **to the minimum extent necessary**,
and expressly not general Agent Factory construction (`§3`, `§4`, `§18`).

## 3. Resident evidence used (`§23.3`)

| Source | Statement |
|---|---|
| Freeze §4 — **INV-2** | *"Every Agent Definition is owned by exactly one Department and implements at least one Capability."* |
| Freeze §4 — Agent Definition entry | *"**Ownership**: exactly one Department."* |
| `agent_spec §3` **Owned Data** | **[E]** *"Agent Definitions owned by exactly one Department (INV-2)."* |
| Domain Model §5 — Ownership Rules | `Agent Definition` → *"Exactly one Platform Division"* (*"Historical alias: **Department**"*, ADR-0010) |
| `agent_spec §12`/`§13` | **[O]** *"Agent **construction** discipline…"* / *"governed **construction** of Definitions/Instances… reserved to the Architect."* |
| `Blueprint §26` (via Agent conformance) | `capability` is among the boundaries Agent must not import |

## 4. Agent Factory reservation boundary actually exercised (`§23.4`)

**None was exercised — none needed to be.**

**[E]** Ownership of an Agent Definition by a Department is ratified in the three
sources above and reserved in none. The `agent_spec §12`/`§13` reservation
covers *construction* — governed creation, registration, and validation of
Definitions against Capabilities — and does not reach ownership. The field was
absent before now for a historical reason rather than a reserved one: in Phase 3
the Department entity did not exist, only the `DepartmentRef` stub, and
Department was realized under `ACT-CC-F03-036`.

This was reported to the Founder **before** the decision was given, as a
correction to `ACT-CC-F03-038`'s own erroneous finding, which `ACT-CC-F03-039
§2.2` had carried forward in good faith. The Founder selected **OPTION A**
notwithstanding. The authorization is therefore honoured as given, and the
reservation stands **unnarrowed**: nothing in this execution lifted, weakened or
relied upon lifting any `[O]` marker (`§7.10`).

**Still reserved, untouched:** INV-2 **clause 2** — that a Definition
*implements at least one Capability* — which does require checking a Definition
against Capabilities, and is squarely the reserved construction discipline.
Also untouched: Agent Definition lifecycle, creation policy, registration, Agent
Instance ownership, and every item enumerated in `§2.3` and `§18`.

## 5. Implementation changes (`§23.5`)

- **`AgentDefinition.owning_department_key: str`** — required, single-valued,
  fails closed on empty/blank/non-string (PR-4), because INV-2 admits no
  unowned Definition. Held as a **plain key**, not the Capability boundary's
  `DepartmentRef`, so the Agent boundary takes **no `capability` import** and
  its `Blueprint §26` dependency-direction conformance is left intact.
- **`OwnershipGraph`** — the Definition side of the edge, mirroring exactly what
  `-037` built for Capabilities: `resolve_agent_definitions` (requires **both**
  sides to agree; fails closed on contradiction and on unknown Department),
  `disputed_agent_definition_ownership` (PR-3 survey),
  `unresolved_agent_definition_ownership`, `unbacked_agent_definition_claims`.
  Declarations arrive as `(agent_definition_key, named_department_key)` plain
  pairs — neither boundary may import the other, so a caller that sees both
  supplies them.
- **`DisputedAgentDefinitionOwnership`**; package exports 22 → **24**.

## 6. Specification changes (`§23.6`)

`department_spec §13` records the target RESOLVED on both sides, **discloses the
`-038` provenance error** rather than quietly amending it, and states what
remains reserved. `AIOS_CONSTRUCTION_FRONTIER_v1.0.md` carries a matching
correction. **`agent_spec` was not modified** — its `§3` already states the
ratified relationship; there was nothing to add. No `[O]` was converted to `[E]`
(`§16`), and INV-2's meaning is unchanged.

## 7. Tests and regression (`§23.7`)

`native_core` **556 OK** (1 expected failure) · `tools` **20 OK** ·
`bounded_exception` **29 OK**. `P7-F-2` / `GDR-0014` untouched (`§15`).

**Three conformance tests updated, each toward its own cited authority (`§14`).**
`test_it_carries_exactly_identity_and_version` → `…_version_and_its_owner`: its
basis is `agent_spec §3/§4`, and §3 is the Owned Data clause that states the
ownership this field carries. `test_both_fields_are_required` →
`test_every_field_is_required`, generalized rather than relaxed — it still
asserts every field is mandatory with no default. The halt-message guard count
moved 4 → 5 under its own stated rule, *"one guard per declared field"*; the
string assertion it exists to make is untouched and now covers the new guard.
**No test was weakened**, and the eleven-boundary and reserved-structure guards
were not touched.

## 8. Independent verification (`§23.8`)

`§5.1`–`§5.8` were each exercised directly, separately from the test suite:
relation represented · resolvable · invalid ownership rejected (4 forms) ·
conflicting ownership rejected, with the dispute distinguished from an unknown
Department · unowned state detectable under PR-3 · Capability ownership
unaffected (`owner_of` and `resolve` re-probed) · `AgentInstance` fields
unchanged · Agent Factory authority otherwise reserved.

**[E] Defect disclosed in this program's own verification code.** A test added in
this Act asserted `assertNotIn("AgentDefinition", source)` to prove the
Capability boundary imports nothing from Agent. That is a substring check, and
it matched the module's own legitimate exception names
`ConflictingAgentDefinitionOwnership` and `DisputedAgentDefinitionOwnership`.
Replaced with an AST-anchored check of the actual import graph. Disclosed, not
silently corrected.

## 9. Architecture / governance mutations (`§23.9`)

Constitution, Architecture Freeze, Canonical Domain Model and Finding Register
**hash-identical**. No governance register mutated. No canonical entity created;
no Native Core boundary created — core region remains **eleven**. PD-02
untouched; `DEC-AE04`, `DEC-REVOCATION`, `DEC-ADOPTION`, `OB-01`, `RG-2`, `RG-3`
untouched (`§13`, `§18`).

## 10. Escalation (`§23.10`)

**None.** No architecture gap was encountered. The one structural obstacle — that
neither boundary may import the other — was an ordinary engineering constraint
and was resolved within authority by passing plain keys (`§11`).

## 11. Remaining construction frontier (`§23.12`)

**[A]** No non-reserved engineering gap remains in the Capability boundary or its
ownership context. Remaining candidates: **T-11** (INV-2 clause 2) and **T-2**,
**T-3**, **T-12** are `[O]`-reserved to the Architect; **T-4** is blocked on a
Founder-reserved authority question entangled with `OB-01`; **T-5**–**T-8**
(Intelligence · Planner · Scheduler · Execution Orchestrator) are unratified and
excluded.

**[D]** The next increment requires a decision, not further engineering.
