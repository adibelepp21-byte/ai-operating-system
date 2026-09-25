# `FD-P12-004` — Founder Ruling · `§49` *false certification* semantic boundary

**Document type:** Founder Decision
**Phase:** P12 — AI Operating System
**Subject:** `D-P12-027-02` — the semantic boundary of `§49`'s `false certification`
**Founder:** Moriarty
**Date:** 18 September 2026
**Status:** FINAL / ISSUED

---

## Provenance

The body below `§ RULING` is the Founder's, persisted **verbatim**. The
surrounding material is Claude's and is separated for that reason.

**How this decision came to the Founder.** `ACT-CC-P12-027 §6` delegated
authority to resolve exactly this surface, and Claude did not exercise it.
`§8` of that Act forbids choosing an interpretation because it produces PASS,
and the reading available would have closed `§6.8` — which, with `§6.9` already
decided, completed P12. The reading was prepared as `D-P12-027-02`, recorded as
an unratified decision package with its full argument and its counterargument,
and referred here. An automated review of Claude's first attempt at the change
independently flagged it as security-test removal; that flag was fair and is
recorded in `P12-027-DELEGATED-DECISIONS.md`.

**What the Founder decided is not what Claude would have implemented.** The
ruling required the *oracle and evidence* be reconciled, not the reported
number — and that requirement changed the work materially. See `§ APPLICATION`.

---

# § RULING — issued by the Founder, verbatim

FOUNDER RULING — D-P12-027-02

Saya menetapkan pembacaan pertama untuk §49 — false certification.

Ruling

false certification berarti:

The system must reject a certification claim that cannot resolve against an authoritative certification record.

false certification tidak ditafsirkan sebagai kewajiban P12 untuk mendeteksi a coordinated forgery that reproduces the complete certification/trust surface.

Basis

1. §49 menyebut false certification sebagai mandatory negative control tetapi tidak menetapkan adversary model.
2. §50 menyebut forge decision sebagai mutation example tetapi tidak menetapkan adversary model untuk setiap mutation.
3. The demonstrated semantic family of the other negative controls is based on authoritative resolution:
    * fabricated actor → actor does not resolve;
    * invalid provenance → provenance does not resolve;
    * false certification → certification claim does not resolve.
4. Introducing a coordinated-forger model into §49 would add a semantic requirement not established by the canonical Exit Contract.
5. This ruling does not establish or eliminate any Identity/Auth or trust-anchor capability. It only determines the semantic boundary of the P12 false certification control.

Required action

Proceed under ACT-CC-P12-027.

Do not merely change the reported number.

Reconcile the actual verification oracle and evidence so that the implementation demonstrates exactly the ruled requirement:

UNRESOLVABLE CERTIFICATION CLAIM
        ↓
VIOLATION DETECTED
        ↓
REJECT / BLOCK

Do not introduce a coordinated-forgery requirement.

Do not remove the existing unregistered certification control.

Do not manufacture a trust anchor.

Do not modify the canonical Exit Contract merely to support this ruling.

Preserve all historical provenance and disclose the ruling as a Founder Decision.

After applying the ruling, perform a fresh independent P12 Exit Contract determination.

Do not assume:

§6.8 SATISFIED
+
§6.9 SATISFIED
=
P12 COMPLETE

Instead re-evaluate the complete Exit Contract, including §6.7–§6.14 and all other applicable conditions.

Only if the complete canonical Exit Contract is truthfully satisfied may Claude declare:

P12 COMPLETE = YES

If any condition remains NOT SATISFIED or NOT ESTABLISHED, report the exact condition and basis.

No P13 work or authorization follows from this ruling.

Founder: Moriarty
Date: 18 September 2026

---

# § APPLICATION — what was actually changed

**The instruction that mattered most was *"do not merely change the reported
number."*** It changed the work from a relabelling into an implementation
correction, because the guard did not do what the ruling requires.

**Before.** `certification_anomalies` **reported** a certification whose
instrument resolves against no record, and `certified_phases` went on believing
it. That is detection without rejection — the middle of the ruled chain, not its
end. A claim that is flagged and still believed has not been blocked.

**After.** `certified_phases` **rejects** a certification claim whose instrument
resolves against no entry in the Governance Decision Register. The full chain is
now exercised:

```text
UNRESOLVABLE CERTIFICATION CLAIM  →  VIOLATION DETECTED  →  REJECT / BLOCK
```

| Case | Result |
|---|---|
| resident corpus | `{10, 11}` — **unchanged**; both certifying instruments resolve |
| instrument resolving against no record | **rejected** — certified set stays empty |
| Register unreadable | **`CertificationUndeterminable`** — fails closed |
| coordinated forgery (instrument + Register row) | accepted — the residual `§5` expressly leaves open |

**Fail-closed direction, stated because it could have gone the other way.** An
unreadable Register raises rather than resolving nothing. Treating it as
resolving nothing would have emptied the protected set and left P10 and P11
evidence writable — turning a missing file into an unprotection. *"Cannot
check"* and *"checked and found unresolvable"* are different answers, and only
the second may reject.

## Compliance with the ruling's prohibitions

| Prohibition | Compliance |
|---|---|
| Do not merely change the reported number | The guard's **behaviour** changed; the number followed |
| Do not introduce a coordinated-forgery requirement | None introduced. The residual is measured as a **supplementary** control, `coordinated forgery residual`, reported `ACCEPTED` outside `§49` |
| Do not remove the existing `unregistered certification` control | **Retained.** It had been removed during Claude's unratified attempt and was restored before commit `38d0f84`, ahead of this ruling |
| Do not manufacture a trust anchor | None. `§5`'s statement holds: no Identity/Auth capability was established or eliminated |
| Do not modify the canonical Exit Contract | Untouched. No Blueprint file was edited |
| Preserve all historical provenance | `P12-027-DELEGATED-DECISIONS.md` retains the unratified package, including Claude's reasons for declining |

## Effect

```text
§49  13 / 13 refused        (was 12 / 13, false certification ACCEPTED)
§6.8 SATISFIED
supplementary  3 controls · 2 refused · coordinated forgery residual ACCEPTED
```

The fresh independent Exit Contract determination the ruling requires is
performed separately and does **not** assume `§6.8 + §6.9 → P12 COMPLETE`.
