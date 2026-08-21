# `ACT-CC-F03-043` — T-3 EXECUTION: VERSIONED-CONTRACT REPRESENTATION

> **DRAFT — PREPARED BY THE CO-FOUNDER OFFICE · AWAITING FOUNDER ISSUANCE.**
> Produced under `ACT-CC-F03-042 §14`. **This document confers no authority on
> itself.** `ACT-CC-F03-042 §18` [E]: construction authority *"is granted only by
> a subsequent execution Act."* Until the Founder issues this Act, **no
> construction may begin.** Nothing here appoints, ratifies, or activates.

**Predecessor:** `ACT-CC-F03-042` · **Decision consumed:** `DEC-F03-042`
**Prepared:** 2026-08-21 · **Repository state at preparation:** `62fe1ce`, tree clean

---

## §1 — The exact Founder decision consumed (`§14.1`)

```text
DEC-F03-042 — NEXT CONSTRUCTION FRONTIER
OPTION B — AUTHORIZE T-3 · Versioned-contract representation
Founder: Moriarty · Date: 21-08-2026 · Signature / Confirmation: Moriarty.
```

Consumed exactly as supplied. The stray Option-E sub-bullet in `§16` is recorded
in `AIOS_DEC_F03_042_NEXT_FRONTIER_v1.0.md §2` and is **not** treated as
authorization; the OB-01 track remains closed.

## §2 — Selected frontier (`§14.2`)

**T-3 — the representation of the versioned Capability contract.** The
reservation, verbatim:

> `capability_spec §14` **[O]** — *"Versioned-contract representation (reserved
> — no format defined here)."*

The spec's own legend fixes what `[O]` means: *"**[O]** open / Architect
reserved."* `DEC-F03-042` opened it.

## §3 — Resident canonical basis (`§14.3`)

| Source | Statement |
|---|---|
| Freeze **INV-9** | **[E]** *"Every Capability-to-Capability dependency must be explicit and must reference a **specific versioned contract**."* |
| Freeze §4 — Capability | **[E]** *"declare explicit versioned dependencies (INV-9)"*; *"depend on Capabilities via **governed, versioned contracts**"* |
| `capability_spec §14` | **[O]** representation reserved — the frontier |
| `models.py` `CapabilityIdentity` | *"The version is **opaque** — capability_spec §14 reserves the versioned-contract representation, so no scheme is imposed here."* |
| `knowledge/models.py` `VersionIdentity` | **Resident precedent**: *"The **lexical form** and the allocation of `version_sequence` are **reserved to a later phase**; this model validates structure only (it does not allocate)."* |

**Not a Freeze §10 item.** Architecture Freeze §10's deferred list contains the
Inferred relationships (T-2) and the Knowledge admission model (T-12); it does
**not** contain versioned-contract representation. T-3's reservation therefore
sits at engineering-specification level over a *representation*, atop an
invariant that is already ratified **and already implemented**. This is what
distinguishes T-3 from T-2 and T-12, which Freeze §10 marks *"not frozen"* and
*"named as a boundary, not defined."*

## §4 — Architecture eligibility (`§14.4`)

**ELIGIBLE, with one question that may require escalation.**

INV-9 is ratified and enforced: `CapabilityDependency` requires a
`CapabilityIdentity`, which is `(capability_key, capability_version)`. A
dependency therefore already names a key and a version. No new entity, no new
boundary, no new invariant is needed to give that version a defined
representation.

### §4.1 Finding from consequence analysis (`ACT-CC-F03-042 §1.3`)

The version is currently an opaque non-empty string. Probed directly, it admits:

| Value | Accepted today? | Is it a *specific* contract? |
|---|---|---|
| `1.0.0` | yes | yes |
| `>=1.0` | **yes** | **no — a range** |
| `^2.1` | **yes** | **no — a range** |
| `1.x` | **yes** | **no — a range** |
| `*` | **yes** | **no — unbounded** |
| `latest` | **yes** | **no — floating** |
| `" 1.0 "` | **yes** | ambiguous — untrimmed |

INV-9 requires a dependency *"reference a **specific** versioned contract."*
**[A]** A range, a wildcard and a floating alias are not specific. So the
present surface admits values the ratified invariant appears to exclude.

### §4.2 The question the successor execution must answer first

**[D]** Two readings, and they lead to different authorized work:

- **Reading 1 — conformance repair.** "Specific" is already ratified by INV-9, so
  refusing ranges/wildcards/floating aliases enforces an *existing* requirement.
  This is repair under `ACT-CC-F03-042 §4` Option B and the standing defect
  discipline: existing requirement → implementation violation → repair.
- **Reading 2 — format definition.** Deciding *which* strings count as specific
  requires a scheme, and choosing a scheme is the representation `capability_spec
  §14` reserved. `DEC-F03-042` opened that reservation, but `§4` Option B still
  requires that *"if the representation requires an architectural decision,
  Claude Code must package that decision rather than silently resolving it."*

**[R]** The execution should establish which reading the resident evidence
supports **before** writing code, and must be prepared to stop at a decision
package rather than choose a scheme by implementation. **[O]** Whether a
specific lexical scheme is adopted is Architect-reserved unless the evidence
shows `DEC-F03-042` already settled it.

## §5 — Specification sufficiency (`§14.5`)

**PARTIAL — sufficient to state the requirement, insufficient to fix a format.**
`capability_spec §2`, `§6` and Freeze INV-9 establish *that* a dependency
references a specific versioned contract. No resident source defines *what a
version looks like*. `knowledge/models.py` shows the established treatment of
exactly this situation: **validate structure, impose no scheme, allocate
nothing.**

## §6 — Dependency status (`§14.6`)

**SATISFIED.** Capability architecture RATIFIED, specification COMPLETE,
implementation COMPLETE and green. INV-1, INV-2 clause 1, INV-2 clause 2, INV-9,
INV-10, INV-11, INV-14 all implemented. No unbuilt prerequisite. Native Core at
**eleven** boundaries.

## §7 — Authority status (`§14.7`)

`DEC-F03-042 = OPTION B` opens the `capability_spec §14` reservation **only**.
It does not amend the Constitution, Architecture Freeze or Canonical Domain
Model; does not create an entity or boundary; does not convert `[O]` to `[E]`
through implementation; and does not touch PD-02, OB-01, or any other frontier.

## §8 — Construction scope (`§14.8`)

Permitted, if and only if `§4.2` resolves to a reading that does not require a
further decision:

1. constrain `capability_version` so that a dependency references a **specific**
   contract, as INV-9 already requires;
2. keep INV-9's meaning unchanged — this narrows what is *accepted*, it does not
   redefine the invariant;
3. tests and conformance for the constrained surface;
4. specification synchronization where already required by ratified architecture;
5. full regression and independent verification.

## §9 — Hard exclusions (`§14.9`)

No new entity · no new core boundary · no change to INV-9's meaning · no new
governance semantics · no broadening of contract semantics beyond resident
authority · no dependency-order change · Constitution, Architecture Freeze,
Canonical Domain Model, Master Roadmap and Founder decision records unmodified ·
T-2, T-12, T-4/OB-01 untouched · Planner, Scheduler, Execution Orchestrator,
Intelligence not constructed · PD-02 not activated · conformance tests not
weakened · `P7-F-2`/`GDR-0014` not repaired.

## §10 — Verification requirements (`§14.10`, `§19`)

Selected decision · canonical source · reservation status · architecture surface ·
specification status · dependency status · authority status · protected artifact
hashes · core boundary count · `native_core` / `tools` / `bounded_exception`
regression · governance mutation count · unintended changes · escalation state.
At least one verification pass independent of the implementation's own tests.

## §11 — Escalation condition (`§14.11`)

**Stop and package a decision, rather than implement, if** choosing which values
count as *specific* requires adopting a lexical scheme that no resident source
establishes; or if the change would alter INV-9's meaning, require a new entity
or boundary, change governance semantics, or need a further Founder-reserved
decision. Per `ACT-CC-F03-042 §11`, the successor *"must not silently implement
the unresolved architecture."*

**[A] Honest expectation:** `§4.2` makes an escalation package a realistic
outcome of this frontier, alongside or instead of code. `ACT-CC-F03-042 §5`
already records that authorizing T-3 does **not** automatically authorize
construction.
