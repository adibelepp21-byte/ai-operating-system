# PD-06 — AI Engineering

> **Status: DERIVED.** Constructed under `FDE-P10-FRONTIER-02`, Decision A.
> Below the Established section is bounded derivation, **not canonical**.

| | |
|---|---|
| **CPID** | `PD-06` — permanent |
| **Established name** | AI Engineering |
| **Established domain** | AI engineering domain |
| **Primary construction target** | Agent framework, AI components, engineering |
| **Maturity** | EVIDENCE-READY → **CONSTRUCTED (derived)** |

---

## 1. Established (source constraint)

- Frozen `PD-02 B4:731` — ***"PD-06 owns implementation."*** A prose ownership binding, not a diagram label.
- Frozen `PD-02 A4:284` — domain label **AI Engineering**.
- Frozen `PD-02 A5:328` — `AI Engineering Execution │ **NONE** │ AI Engineering owner`.
- Frozen `PD-02 A5 §12` — PD-02 may not *"memaksa implementation execution"* — cannot compel implementation execution.
- Frozen `PD-02 C8:303`-region — `PD-06 — Implement AI Engineering`.

## 2. The sharpest boundary in the Platform Organization

*"PD-06 owns implementation"* sits directly against PD-02's *"PD-02 tidak menjadi
implementation owner hanya karena mengontrol architecture change"* — **PD-02 does
not become implementation owner merely by controlling architecture change**
(`D8 §70`).

The two statements are complementary, and together they draw the clearest
architecture/implementation line in the corpus:

```text
PD-02  architecture authority ── may constrain, review, approve
                                  may NOT execute or compel implementation
PD-06  implementation owner  ── executes
                                  bounded by architecture it does not set
```

This is `Governance ≠ Execution` (`§13`) instantiated between two named
divisions, and it is **evidenced rather than derived** — unusual in this set.

## 3. Derived organizational structure

| Part | Derivation for PD-06 |
|---|---|
| **A — Identity & Mandate** | AI engineering domain; owns implementation |
| **B — Organization** | Candidate decomposition from the construction targets: agent framework · AI components · engineering practice. **Derived** |
| **C — Governance** | Receives architectural constraint from PD-02 across the ADR path (`Constitution §3.4`); retains execution. PD-02 may not compel it |
| **D — Operating** | Implementation lifecycle: specification → build → verify → integrate. **Derived** |
| **E — Performance** | Conformance to architecture, verification coverage. **Derived** |

## 4. Scope caution

*"Owns implementation"* is stated without a stated **scope**. Read at its widest
it would place all AIOS implementation under PD-06 — including work inside other
divisions' domains, which would contradict `§13`'s `Dependency ≠ Ownership` and
every other division's domain ownership.

**The scope of "implementation" is therefore recorded as UNKNOWN, not resolved
to the widest reading.** Taking the widest reading would be the convenient move
and an unsupported one.

## 5bis. Inbound relationship — evidenced from another division's corpus

> **Added 2026-09-05** under `ACT-CC-P10-FINAL §26`. Every relationship this
> record previously carried was stated **from PD-02's side** or derived. This one
> is stated by **PD-04's own corpus**, naming this division. **Source body is
> NOT RESIDENT** (`ESC-C7-01`); recorded as evidence, not as a binding.

`PD-04 A1` declares `PRIMARY DEPENDENCIES: AI Engineering, Runtime` (`E-24`).
**`AI Engineering` is PD-06.**

**This is the first evidenced relationship PD-06 has of any kind.** Its only
prior evidence was the frozen ownership statement *"PD-06 owns implementation"*
(`B4:731`) — a statement about PD-06 alone. A division that owns implementation
being depended upon by the Knowledge domain is the first indication of **where
that implementation ownership is consumed.**

**It does not resolve `§4`'s scope caution.** *"Owns implementation"* remains
unscoped, and one inbound dependency does not bound it.

## 5. Unresolved

Scope of "implementation" · relationship to the `agent` and `skill` frozen
subsystems · whether "AI Engineering owner" (`A5:328`) is PD-06 — **suggested by
adjacency, not stated** · boundary with PD-05 where execution meets
implementation.

## 6. Not constructed

No scope assigned to "implementation". No binding to `native_core` subsystems.
No AI Engineering owner binding asserted. Nothing canonicalized or frozen.
