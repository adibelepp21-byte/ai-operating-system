# PD-05 — Runtime & Execution

> **Status: DERIVED.** Constructed under `FDE-P10-FRONTIER-02`, Decision A.
> Established identity and domain are constraints. Everything below the
> Established section is bounded derivation and is **not canonical**.

| | |
|---|---|
| **CPID** | `PD-05` — permanent, not reassignable |
| **Established name** | Runtime & Execution |
| **Established domain** | Runtime / execution domain |
| **Primary construction target** | Runtime, execution layer, contracts, services |
| **Maturity** | EVIDENCE-READY → **CONSTRUCTED (derived)** |

---

## 1. Established (source constraint — not derived)

**PD-05 has the clearest ownership mandate of the eight, stated in prose in the
frozen corpus rather than inferred from a diagram:**

- Frozen `PD-02 B7:212` — ***"PD-05 owns Runtime."***
- Frozen `PD-02 A5:703` — *"PD-05 tetap menentukan operational execution dalam domain Runtime"* — PD-05 continues to determine operational execution within the Runtime domain.
- Frozen `PD-02 A5:327` — `Runtime Execution │ **NONE** │ Runtime owner`. PD-02 holds **no** runtime execution authority.
- Frozen `PD-02 A3:121-122` — PD-02 may not *"memiliki infrastructure execution"* nor *"mengambil alih security execution"*; the same exclusion pattern places execution outside PD-02 generally.
- `MASTER_ROADMAP §5`; `PD-01 C10:87` — own domain success criteria.

## 2. The unusual position of this division

PD-05 is the only division whose domain **already has a substantial resident
implementation**. `native_core/core/runtime/` holds `bootstrap`, `composition`,
`context`, `contract`, `discovery`, `lifecycle`, `runtime`, and an `execution`
package — one of the eleven frozen subsystem boundaries.

**This does not mean PD-05 owns that code.** The boundary between an
*organizational division* that owns the Runtime **domain** and a *frozen core
subsystem* named Runtime is exactly the distinction `ADE-P10-G04` preserved:
`ORGANIZATIONAL SOURCE ≠ ORGANIZATIONAL RUNTIME`. Nothing in the corpus binds
`PD-05` to `native_core/core/runtime/`, and **no such binding is asserted here.**

## 3. Derived organizational structure

| Part | Derivation for PD-05 |
|---|---|
| **A — Identity & Mandate** | Owns the Runtime domain; determines operational execution within it. Bounded by the frozen Runtime subsystem's own contracts, which it does not amend |
| **B — Organization** | Candidate decomposition: execution contracts · runtime services · lifecycle management · execution observability. **Derived** |
| **C — Governance** | Subject to Architecture Authority for architectural decisions (`PD-02` OA-01…OA-06) while retaining execution. *"PD-05 tetap menentukan operational execution"* is the boundary: architecture may constrain, it does not execute |
| **D — Operating** | Execution contract lifecycle: declare → compose → run → observe → close. Mirrors the resident `runtime` package's own shape, cited as **implementation evidence**, not as PD-05's charter |
| **E — Performance** | Execution success, contract conformance, observability completeness. **Derived** |

## 4. The boundary that matters most here

```text
PD-05                          native_core/core/runtime
organizational division        frozen subsystem boundary
owns the Runtime DOMAIN        implements runtime BEHAVIOUR
                ↑
        no resident source binds these
```

Collapsing them would be the single easiest error available in this
construction, and it is barred: `Dependency ≠ Ownership`, and the frozen
boundary set admits no organizational entity.

## 5bis. Inbound relationship — evidenced from another division's corpus

> **Added 2026-09-05** under `ACT-CC-P10-FINAL §26`. Every relationship this
> record previously carried was stated **from PD-02's side** or derived. This one
> is stated by **PD-04's own corpus**, naming this division. **Source body is
> NOT RESIDENT** (`ESC-C7-01`); recorded as evidence, not as a binding.

`PD-04 A1` declares `PRIMARY DEPENDENCIES: AI Engineering, Runtime` (`E-24`).
**`Runtime` is PD-05.**

**And PD-04's `C3` calls PD-05 a consumer of Knowledge**, so both directions are
recorded — **but both come from PD-04's corpus**, not from two independent
sides. PD-04 describes its own relationship in both directions; **PD-05's corpus
does not exist to corroborate or contradict it.** That is materially weaker than
the PD-03↔PD-04 boundary (`E-25`), which is stated independently from each side,
and it is recorded at that lower strength deliberately.

**Nothing here binds PD-05 to `native_core/core/runtime/`.** §4's boundary
stands unchanged.

## 5. Unresolved

| | |
|---|---|
| **Binding to implementation** | Whether PD-05 owns, governs, or merely names the Runtime subsystem — **UNKNOWN**. This is the most consequential unresolved question of the eight |
| **Runtime owner ↔ PD-05** | `A5:327` names a *"Runtime owner"* role. `B7:212` says PD-05 owns Runtime. Whether these are the same is **strongly suggested and not stated** — and suggestion is not evidence |
| **Contract authority** | Whether PD-05 may define execution contracts, or only operate them — **UNKNOWN** |

> **Narrowed 2026-09-09 by the model layer — not resolved.**
> **"Whether PD-05 owns, governs, or merely names the Runtime subsystem"** — the
> record's own most consequential question — is now sharper on both sides.
> `Freeze §4` holds the **Runtime entity** *"owned centrally"* and *"a facility,
> not an actor"*; frozen `volume-2/.../B7.md:212` says *"PD-05 owns Runtime."*
> **`domain accountability ≠ entity ownership`** (`E-79`), and `Domain Model §4`
> states the general form: **`governs ≠ owns ≠ lifecycle authority`**, adding
> that `governs` *"establishes no creation, retirement, deprecation, or
> unilateral mutation authority."*
> **So three readings are now distinguishable where the record could only name
> them:** domain accountability (supported), entity ownership (**contradicted**
> by `Freeze §4`), and lifecycle authority (**excluded** — `Domain Model §6`
> reserves it). **Which one `B7:212` asserts is still not stated**, and
> *"suggestion is not evidence"* stands.
> **Contract authority** unchanged.

## 6. Not constructed

No binding between PD-05 and any `native_core` package. No claim to the frozen
Runtime subsystem. No execution contract authority asserted. Nothing
canonicalized or frozen.


---

## Model layer — what canon establishes for every Platform Division

**Integrated 2026-09-06, Cycle 25.** The four model artifacts in the parent
directory answer all ten construction dimensions **at model level**, from
canonical and frozen source. They apply to this division as to every other, and
**assign it nothing**.

| Established for every division | Source |
|---|---|
| Owns **exactly two** entity types — Capability (inv. 1) and Agent Definition (inv. 2), each *"exactly one Platform Division"* | `DIVISION-OWNERSHIP-MODEL.md` |
| Owns **none** of Skill, Workflow, Tool, Runtime (*"owned centrally"*) or Trace (*"owned by no one"*) | same |
| `home ≠ ownership ≠ privacy` for Knowledge; `accountable-for ≠ owns` for Agent Instance | same · `E-91` |
| Its **own creation, retirement and naming** are *"architectural decision, architect approval"* | `DIVISION-LIFECYCLE-AND-AUTHORITY-MODEL.md` |
| Its **one affirmative discretion**: Agent Definitions are *"created/deprecated at Platform Division discretion within Capability governance"* | same · `E-84` |
| `governs ≠ owns ≠ lifecycle authority` | `Domain Model §4` · `E-85` |
| Capability creation is *"intentionally… restricted to architect-approved decisions… not a gap"* | `DIVISION-CAPABILITY-ARCHITECTURE-EVOLUTION-MODEL.md` · `E-87` |
| The Spine is **three levels**, *"not to be deepened or bypassed without an architectural decision"* | `Domain Model §8` · `E-90` |
| Repository layout is a **projection** of the model — `correspondence ≠ ownership` | `IMPLEMENTATION-CORRESPONDENCE-MAP.md` · `E-90` |
| Performance follows the `E1`–`E10` chain, corroborated across two divisions; **`measurement ≠ authority`** | `DIVISION-OPERATION-AND-PERFORMANCE-MODEL.md` · `E-93` |
| Operation is a **position and shape**, domain-adapted — not common content | same · `E-94` |

**This changes nothing about this division's own content.** Per-division content
remains blocked at `G-01`/`ESC-C7-01`, and per-division **assignment** remains
reserved at `G-09`/`G-10`. `ACT-CC-P10-FINAL §26`: a division is **not** complete
because one dimension is.

### Specific to `PD-05`

- **The *"PD-05 owns Runtime"* citation is reconciled, not contradicted.**
  `Freeze §4` holds the **Runtime entity** *"owned centrally"*; frozen
  `volume-2/.../B7.md:212` says PD-05 owns Runtime. **`domain accountability ≠
  entity ownership`** — the distinction this record already drew
  (`owns the Runtime DOMAIN` vs `implements runtime BEHAVIOUR`) is confirmed from
  `Freeze §4` (`E-79`). **Recorded as a latent collision:** a reader taking it as
  *entity* ownership would contradict frozen canon.
- **The open *"Runtime owner"* question stands.** Whether `A5:327`'s role and
  `B7:212`'s ownership statement are the same thing remains *"strongly suggested
  and not stated"* — and `Domain Model §4`'s `governs ≠ owns ≠ lifecycle
  authority` sharpens why suggestion is insufficient.
