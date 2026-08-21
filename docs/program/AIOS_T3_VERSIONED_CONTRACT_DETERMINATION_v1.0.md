# T-3 — Versioned-Contract Representation · Determination Record

**Executed under:** FOUNDER · `ACT-CC-F03-043` · **Date:** 2026-08-21
**Founder decision consumed:** `DEC-F03-042 = OPTION B — AUTHORIZE T-3` · Moriarty · 21-08-2026
**Result:** **STATE C — NO DEFECT / NO CONSTRUCTION REQUIRED** (`§14`)

> **NOT CANONICAL.** A determination and its evidence. Ratifies nothing, adopts
> nothing, and does not alter `capability_spec §14`, which remains **[O]**.

---

## 1. Determination

**[E] The existing representation satisfies INV-9 as far as resident authority
defines it. No conformance defect is confirmed, so no construction is
performed.**

The condition `§7` reports is real and was independently reproduced. It does
**not** constitute an INV-9 violation. `§7` required exactly this test:

> *"The statement that these values violate INV-9 MUST be tested against the
> canonical meaning of `specific versioned contract`."*

It was tested. It does not hold.

## 2. Evidence sweep (`§5`) — what resident authority does and does not fix

| # | Source | Statement |
|---|---|---|
| 1 | Freeze **INV-9** | **[E]** *"Every Capability-to-Capability dependency must be explicit and must reference a **specific versioned contract**."* — no format |
| 2 | Canonical Domain Model §7.9 | identical wording — no format |
| 3 | Freeze §4 — Capability | **[E]** *"depend on Capabilities via governed, versioned contracts"* — no format |
| 4 | `capability_spec §5` | **[E]** *"**(No signatures/formats.)**"* — the spec expressly declines |
| 5 | `capability_spec §14` | **[O]** *"Versioned-contract representation (reserved — **no format defined here**)"* |
| 6 | `models.py CapabilityIdentity` | *"The version is **opaque** — capability_spec §14 reserves the versioned-contract representation, so **no scheme is imposed here**."* |
| 7 | `knowledge/models.py VersionIdentity` | **Resident precedent** — *"The **lexical form** and the allocation … are **reserved to a later phase**; this model **validates structure only**."* |
| 8 | ADR-0002/0004/0005/0008 | none defines a version representation; ADR-0008 treats INV-9 as *"preserved, vacuously"* |
| 9 | `KNOWLEDGE_ENTITY_PROPOSAL` (history) | *"no evidence yet of what a version identifier should look like for this system (semantic version, monotonic integer, and Trace-linked timestamp are all plausible, **none evidenced**)"* |

**[A] Nine sources converge: the version namespace is deliberately opaque.** No
resident source defines, or permits deriving, a lexical scheme.

## 3. Independent reproduction (`§7`, `§12`)

Reproduced in a fresh interpreter, before treating anything as a defect.
`CapabilityIdentity` accepts `>=1.0`, `^2.1`, `1.x`, `*`, `latest`, `1.0.0`,
`" 1.0 "`, and `"not a version at all"` — every non-empty string.

## 4. Why that is not an INV-9 violation

### 4.1 The decisive test — dependencies must already resolve to one exact contract

`CapabilityGraph` requires every dependency target to resolve in-graph
(INV-11: *"A dependency naming a Capability outside the graph is an undocumented
dependency and fails closed"*). Verified directly, against a graph holding
`cap.b` at version `1.0.0`:

| Dependency declared on | Result |
|---|---|
| `("cap.b", "1.0.0")` | **RESOLVES** |
| `("cap.b", ">=1.0")` | **FAILS CLOSED** — `UndocumentedCapabilityDependency` |
| `("cap.b", "^2.1")` | **FAILS CLOSED** |
| `("cap.b", "latest")` | **FAILS CLOSED** |
| `("cap.b", "*")` | **FAILS CLOSED** |

**[E] A range, wildcard or floating alias cannot stand as a dependency in a
validated graph.** It resolves only if a Capability literally exists at that
exact `(key, version)` pair — in which case it is, by definition, one specific
contract. INV-9's requirement is therefore already enforced operationally, not
merely declared.

### 4.2 "Range-ness" is not a property of the string

**[A]** To classify `">=1.0"` as a *range* rather than as a literal version
label, one must assume a scheme in which `>=` is an operator. Under the only
semantics resident authority actually states — **opaque** — `">=1.0"` is a
specific, if oddly named, version. The apparent defect arises **only by
importing semver**, an external convention AIOS has not adopted. `§9` is
explicit that external research *"MUST NOT become canonical authority"*, and
judging these strings by semver would do precisely that.

### 4.3 What INV-9 requires, and what is enforced

INV-9 requires a dependency be **explicit** and **reference a specific versioned
contract**. `CapabilityDependency.depends_on` must be a `CapabilityIdentity`,
which requires **both** a non-empty key and a non-empty version — a dependency
naming only a key cannot be constructed — and the graph requires that pair to
resolve to exactly one Capability. Both clauses are enforced and fail closed.

## 5. `§6` Case determination

**Neither Case A nor Case B is entered.**

- **Not Case A** — no conformance repair is available, because no defect is
  confirmed. Under `§8`'s minimal-change rule the smallest correct change is
  **none**.
- **Not Case B** — no escalation is *required*, because construction did not
  reach a boundary of authority. Nothing was implemented, so nothing was paused
  mid-flight.

Constraining the namespace further would mean **selecting a previously undefined
versioning scheme**, which `§13` lists as requiring escalation and `§4` forbids
inventing. That option was therefore not taken.

## 6. Own-work disclosure (`§17`)

**[E] My `ACT-CC-F03-042` completion report pointed toward a defect that fuller
testing does not support.** It stated the surface *"admits values the ratified
invariant appears to exclude"* and tabulated the five values as *"not
specific."* The hedge *"appears to"* was carried, and the report did flag that
deciding the question might require a reserved scheme — but it did **not** test
the graph-level behaviour in `§4.1`, which is what actually settles it. Had that
test been run then, the finding would have been reported as **no defect**, not
as a probable one. `ACT-CC-F03-043 §7` then elevated the observation into its
premise. Disclosed rather than quietly dropped.

**No verification-code defect** arose in this execution; both probes were run
directly against the public surface in a fresh interpreter.

## 7. Changes

**Implementation changes: NONE.** **Test changes: NONE** — no conformance test
was read as obsolete, so `§10`'s disclosure list is empty. **Specification
changes: NONE** — `capability_spec §14` stays **[O]**; nothing here adopts a
representation or narrows the reservation.

**External research: NOT USED** (`§9`) — resident evidence was sufficient, and
`§9` directs that it then *should not* be used.

## 8. Verification (`§11`, `§12`)

| Check | Result |
|---|---|
| `native_core` | **566 OK** (1 expected failure) |
| `tools` | **20 OK** |
| `bounded_exception` | **29 OK** |
| INV-9 behaviour | verified independently — see §4.1 |
| INV-1 / INV-2 ownership behaviour | unaffected — no code touched |
| Capability conformance | unchanged |
| Core boundary count | **11** |
| Protected canonical artifacts | hash-identical |
| `P7-F-2` / `GDR-0014` | untouched |
| Governance mutations | **0** |
| Unintended changes | **0** |

## 9. Residual reserved question — **optional**, not an escalation

**[O]** `capability_spec §14` remains reserved, and one governance-relevant
consequence of an opaque namespace is worth stating plainly: a Capability may be
*created* at a version literally named `"latest"` or `"*"`, and dependencies on
it will then resolve. Each remains one specific contract, so INV-9 holds — but
the system cannot *detect* an author who intends floating resolution.

**[D]** Whether AIOS adopts a version scheme so that such labels become
detectable is the reserved representation decision. **It is not raised here as
an escalation**, because no defect forces it — `§13` requires escalation only
when implementation *needs* the scheme, and no implementation was undertaken.
`§18`'s successor-gate obligation attaches to STATE B and does not arise.

If the Founder wishes to close it, the single question is:

> *Does AIOS adopt a lexical scheme for `capability_version`, and if so which —
> semantic version, monotonic integer, or Trace-linked timestamp (the three the
> program has previously named as plausible and unevidenced)?*

**[R]** No recommendation is offered on that choice, and none may be read into
this record.
