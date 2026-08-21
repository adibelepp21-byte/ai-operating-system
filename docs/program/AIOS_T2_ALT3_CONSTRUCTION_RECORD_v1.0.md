# T-2 / ALT-3 Construction Record — `Workflow realizes Capability`

**Executed under:** FOUNDER · `ACT-CC-F03-048` `DEC-F03-048 = OPTION A` · Moriarty · 21-08-2026
**Delivered as:** the `ACT-CC-F03-049` execution (`§18`)
**Result:** **CONSTRUCTION COMPLETE** · **STOP** (`§5`, `§13`, `§14`)

---

## 1. Decision consumed (`§10.1`)

```text
DEC-F03-048 = OPTION A — AUTHORIZE
Scope: T-2 ALT-3 — Workflow → realizes → Capability construction only.
Founder: Moriarty · Date: 21-08-2026 · Confirmation: Moriarty.
```

`§17` validity: exactly one option checked · attribution · date · confirmation.
**VALID.**

## 2. Preconditions (`§8`) — all thirteen verified before any mutation

Domain Model carries the relationship · Freeze §6 frozen table carries the row ·
Blueprint §10 permits it · `workflow_spec §7`/`§14` synchronized ·
`capability_spec §12`/`§14` synchronized · `Capability↔Skill` still `[O]` in
three places · Runtime↔Workflow still reserved · Workflow imports no Capability ·
entity count **12** · core boundaries **11** · Constitution and Finding Register
hash-identical · `P7-F-2` intact and still marked *"repair not authorized"* ·
tree clean.

## 3. Minimum implementation surface (`§10.4`)

**Determined from the package's own structure, not chosen freely.** `Workflow`
in `models.py` carries **only** its identity; every relationship lives in a
sibling module with its own key-only reference — `composition.py`/`SkillRef`,
`coordination.py`/`AgentInstanceRef`, `declaration.py`/`AgentDefinitionRef`.
Realization is a relationship, so it takes the same shape:

**`native_core/core/workflow/realization.py`** — new, ~130 lines.

- **`CapabilityRef`** — `capability_key` and nothing else, exactly as `SkillRef`
  and `AgentDefinitionRef` do. This is what Blueprint §10's *"by reference only …
  no import of `core/capability/` and holds no Capability state"* requires.
- **`WorkflowRealization`** — `realized_by: WorkflowIdentity` ·
  `realizes: Tuple[CapabilityRef, ...]`. Structural validation only, failing
  closed (PR-4) on a malformed reference, a non-`CapabilityRef` entry, a
  non-tuple, a wrong subject, or a `capability_key` realized twice.
- **Queries** — `capability_keys()` and `realizes_capability(key)`: the minimum
  surface needed to realize and verify the relationship. Both answer from what
  the Workflow *declares*; neither reads Capability state, and neither can.
- **`InvalidWorkflowRealization`** in `exceptions.py`; package exports 17 → **20**.

`Workflow` itself was **not** modified — asserted by test.

### 3.1 Cardinality was not invented

**[E] No canonical source states a cardinality for this edge.** Domain Model §4,
Freeze §6 and `workflow_spec §7` fix the relationship and its direction; none
fixes how many Capabilities a Workflow realizes. `realizes` therefore imposes the
**weakest structural constraint available** — a possibly-empty set of distinct
keys. Requiring a minimum would have invented an invariant this boundary has no
authority to create (`§5`). Where the architecture *has* spoken on a comparable
cardinality it said the same: INV-15 [E], *"No minimum cardinality is required."*
Cited as posture, not as authority over this edge.

### 3.2 Version binding was not invented

`CapabilityRef` carries a key, not a version. Domain Model §6 binds an **Agent
Definition's** version to the Capability contract it implements and says nothing
about Workflows; INV-9's *specific versioned contract* governs
**Capability→Capability** dependencies, not this edge. Both resident sibling refs
are key-only. Nothing was extrapolated.

## 4. Independent verification (`§10.6`) — run **before** any test was written

Nine properties exercised directly against the public surface in a fresh
interpreter: relationship realized and queryable · positive and negative query ·
empty realization valid · empty / `None` / non-text keys each rejected ·
duplicate key fails closed · non-`CapabilityRef` entry fails closed · wrong
subject type fails closed · instance immutable (`FrozenInstanceError`) · the
Capability surface names no Workflow.

## 5. Conformance tests (`§10.7`) — updated **toward their cited authority**

| Test | Before | Change | Why authorized |
|---|---|---|---|
| `test_capability_composition_is_not_modelled` | asserted the package models no Capability | **replaced** by `test_capability_realization_is_modelled_by_reference_only` | Its basis, restated under `DEC-F03-047`, was *"Until a construction Act grants that authority the package must still expose nothing named for it."* `DEC-F03-048 = OPTION A` **is** that Act. The gate it held is open. |
| `test_public_surface_is_exactly_the_declared_exports` | 17 names | **extended** by exactly the three authorized names | enumeration guard; growth must be declared |

**Neither was weakened.** The replaced guard is **stricter** than its
predecessor: instead of asserting absence, it now asserts the shape Blueprint §10
actually mandates — that the reference carries a key and nothing else — plus a
companion test that the Capability boundary still names no Workflow, holding the
ratified **direction**. Ten new tests cover the relationship, including that the
Skill half is not built and that `Workflow` itself is unchanged.

**Not touched:** `test_runtime_relationship_is_not_modelled` (Runtime↔Workflow
remains `[O]`) · the eleven-boundary guard · and
`TestInv12NoExternalDependency.test_no_other_core_boundary_import`, whose
`FORBIDDEN_BOUNDARIES` already contains `"capability"` and which **still passes
untouched** — that is the authoritative proof no Capability import was
introduced, and it is deliberately not duplicated.

## 6. Verification (`§10.8`–`§10.9`)

| Check | Result |
|---|---|
| `native_core` | **577 OK** (was 566; +11) · 1 expected failure |
| `tools` · `bounded_exception` | **20 OK** · **29 OK** |
| Entity count | **12**, unchanged |
| Core boundary count | **11**, unchanged |
| Workflow imports Capability | **NONE** — AST-verified |
| Capability surface names a Workflow | **NONE** — direction preserved |
| Skill half of T-2 | **not built** |
| Canonical artifacts | Domain Model, Freeze, Blueprint — **hash-identical** |
| Specifications | `capability_spec`, `workflow_spec`, `skill_spec` — **hash-identical** |
| Constitution · Finding Register | **hash-identical** |
| Governance mutations | **0** |
| `P7-F-2` / `GDR-0014` | untouched |

**[E] This construction changed no specification and no canonical artifact.** The
diff is four files, all inside `native_core/core/workflow/`, plus this record.

## 7. Architecture or authority gaps (`§10.10`)

**None encountered.** The relationship, its direction, its boundary discipline
and its representation shape were all already determined by the preceding three
stages; construction required no new decision. Cardinality and version binding
were the two places where a decision *could* have been smuggled in, and both
were resolved by imposing nothing (§3.1, §3.2).

**`§14` respected:** the recorded `workflow_spec §14` Workflow↔Skill
inconsistency was **not** touched and was not needed. Construction never
depended on resolving it.

## 8. Own-work disclosure

**Two defects in my own test code, both caught by the suite and fixed, neither
silently corrected.**

1. `dataclasses` was used without being imported in the workflow test module — I
   assumed an import that module did not have. Fixed by adding it.
2. I called `_import_records()`, a helper that exists in the **agent** test
   module, not this one. Rather than port it, I removed the check entirely: the
   resident `test_no_other_core_boundary_import` already parses the real import
   graph with `"capability"` in its forbidden set, so my version was a worse
   duplicate of an existing guard. The replacement cites it instead.

Neither defect reached the committed state, and both are recorded here rather
than dropped.

## 9. Terminal state (`§13`, `§14`)

**STOP.** Construction stopped at the authorized boundary.

Untouched and unauthorized: the **Skill half of T-2** (`Capability↔Skill`
remains `[O]`) · INV-15 · T-12 · OB-01 · PD-02 activation · `DEC-AE04` ·
`DEC-REVOCATION` · `DEC-ADOPTION` · `RG-2` · `RG-3` · the `workflow_spec §14`
Workflow↔Skill inconsistency · ownership · lifecycle · operative authority.

**T-2 remains half closed.** The Workflow half is now decided, canonicalized,
specified, constructed and verified. The Skill half has not moved.
