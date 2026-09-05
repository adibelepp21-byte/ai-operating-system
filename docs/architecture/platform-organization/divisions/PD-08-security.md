# PD-08 — Security

> **Status: DERIVED.** Constructed under `FDE-P10-FRONTIER-02`, Decision A.
> **`§19` of that event is controlling here:** this construction does **not**
> declare `PD-08 = Security Owner`. The binding remains open.

| | |
|---|---|
| **CPID** | `PD-08` — permanent, not reassignable |
| **Established name** | Security |
| **Established domain** | Security domain |
| **Primary construction target** | Security architecture, access, protection, controls |
| **Maturity** | DISCOVERED → **CONSTRUCTED (derived, binding-open)** |

---

## 1. Established (source constraint — not derived)

The domain intent above is established by `FDE-P10-FRONTIER-02 §35`. Independently,
the frozen corpus defines a **Security Owner / Security Authority** in
substantial detail:

- Frozen `PD-02 A5 §12 Override Limit` — PD-02 may not *"mengambil alih security authority"*. PD-02's override cannot reach it.
- Frozen `PD-02 A5:330` — `Security Execution │ **NONE** │ Security owner`. PD-02 holds none.
- Frozen `PD-02 A3:122` — PD-02 may not *"mengambil alih security execution"*.
- Frozen `PD-02 C5:240`, `:272`; `C2:740` — Security Authority named among authorities PD-02 does not hold.
- Frozen `PD-02 A6:452` — `Security → Security Owner`; `A6:671` — `Security │ Security Owner │ **Architectural Interface**`.
- Frozen `PD-02 C8:570` — *"Security owner tetap memiliki security domain responsibility"* — the Security owner **retains** security domain responsibility.

## 2. The finding that shapes this entire record

**AIOS's security responsibility model is not missing. It is unattached.**

The corpus defines the role, its execution authority, its interface with
architecture, and an explicit prohibition on PD-02 absorbing it. What it never
states is *"PD-08 is the Security Owner."* The only PD-08 occurrences —
`A4:286`, `A6:299` — are boundary-diagram labels (`├── PD-08 Security`),
identical in kind to `├── PD-05 Runtime`, and **not ownership statements**.

Compare: `PD-05` carries a prose binding (*"PD-05 owns Runtime"*), `PD-06` and
`PD-07` likewise. **PD-08 and PD-09 are the two of five domains whose owner role
is defined and whose platform binding is absent.**

## 3. Derived organizational structure

Derived from the established domain intent (`§35`) and the Kernel spine. **Every
row is derivation from a domain label, not from PD-08 domain substance — because
none exists.**

| Part | Derivation for PD-08 |
|---|---|
| **A — Identity & Mandate** | Security domain: architecture, access, protection, controls. Whether this division *is* the Security Owner is **open** — see §4 |
| **B — Organization** | Candidate decomposition following the four established construction targets: security architecture · access · protection · controls. **Derived from the target list alone** |
| **C — Governance** | Meets Architecture Authority across an **Architectural Interface** (`A6:671`) — architecture may set requirements in its own domain authority while security domain responsibility stays with the Security owner (`C8:570`) |
| **D — Operating** | Not derived. Security operating structure without a resident source would be invention on a subject where invention is least acceptable |
| **E — Performance** | Not derived. Same reason |

**Parts D and E are deliberately empty.** For most divisions a derived operating
model is harmless scaffolding. For Security it would be a security design
authored from nothing, and `§9`'s *"no false closure"* applies most sharply
where the subject matter is protection.

## 4. The open binding — stated, not resolved

```text
Security Owner            defined in frozen corpus, holds Security Execution,
                          retains security domain responsibility
        ?                 ← no resident source connects these
PD-08 Security            established CPID and domain
```

`FDE-P10-FRONTIER-02 §19`: *"This authorization does not itself declare PD-08 =
Security Owner… Claude must not convert the existence of a Security domain into
an unsupported ownership assertion."* **It is not converted.**

The decision is one sentence in either direction, and it is not mine.

## 5bis. Inbound relationship — evidenced from another division's corpus

> **Added 2026-09-05** under `ACT-CC-P10-FINAL §26`. Every relationship this
> record previously carried was stated **from PD-02's side** or derived. This one
> is stated by **PD-03's own corpus**, naming this division. **Source body is
> NOT RESIDENT** (`ESC-C7-01`); recorded as evidence, not as a binding.

`PD-03 A1 §22` declares `PRIMARY DEPENDENCIES: Architecture · Security · Quality`
(`E-33`). **`Security` is PD-08.**

**This is the first evidenced relationship for PD-08**, and it is worth being
precise about what it does and does not do for `G-03`.

**It does not bind the Security Owner role to `PD-08`.** PD-03 names *Security*
as a **domain** it depends on. `G-03`'s open question is whether `PD-08` **is**
the Security Owner — a role-to-CPID binding — and a dependency statement from a
third division cannot supply it. **`G-03` is unchanged.**

What it does establish: the Security domain is depended upon by the Governance
authority, which is consistent with `A6:671`'s `Security │ Security Owner │
Architectural Interface`.

## 5. Unresolved

Binding to the Security Owner role · access-control model · protection scope ·
relationship to `native_core` security surfaces (none identified) · whether
"controls" here means the same controls PD-03 defines under compliance — a
possible **PD-03/PD-08 boundary question**, recorded, not resolved.

## 6. Not constructed

No Security authority declared. No ownership model asserted. No canonical
boundary drawn. No operating or performance structure invented. Nothing
canonicalized or frozen.
