# P12-W3 — `F-12` closed · certification enforced, not merely recorded

> **`F-12 CLOSED — VERIFIED`.** `P12 CONSTRUCTED = FALSE` — a frontier result is
> not a phase result.
>
> **`historical rewrite = 0`** — verified by fingerprint before and after a real
> refused re-run.

---

## 1. The defect

`FD-P11-002` certified P11 on 2026-09-11. The P11 work paths were **designed**
re-runnable, and during construction that was correct: eight delegation records
span `03:32 → 07:33` that day, seven `REVOKED` and one `ACTIVE`, and the evidence
file carries four commits.

**The operation did not change. Its meaning did, at certification.** The same
re-run now overwrites certified-phase evidence and flips the one `ACTIVE`
delegation to `REVOKED`. Nothing in the repository noticed.

```text
CERTIFIED DOCUMENT   ≠   ENFORCED BOUNDARY
```

A certification that constrains documents but not behaviour is a record, not a
boundary. `§16` requires governance *"dapat diterapkan lintas layer"* — applied
across layers — which is precisely the gap between the two.

---

## 2. What was built

`tools/p12_certified_evidence_guard.py` — a checkpoint, not a new authority.

**Certification is read from instrument bodies.** `IDENTIFIER ≠ DECISION BODY`,
so the phase set comes from a certification *statement* inside a resident
instrument: `FD-P11-002 §1` *"PHASE 11 — AUTONOMOUS ORGANIZATION IS CERTIFIED"*
and `FD-P10-005 §16` *"Phase 10 — Department Ecosystem is hereby certified"*.
Result: `{10, 11}`, and only `docs/architecture/p11` exists as an evidence root,
so that is what is protected.

**Deriving it from the Register's prose was tried and rejected.** The Register
contains *"It does **not** establish `PHASE 8 — CERTIFIED / COMPLETE`"* — a
sentence every naive pattern reads as a certification. A guard fooled by a
negation is worse than no guard, and a test now holds that case.

**It fails closed.** Unreadable governance raises `CertificationUndeterminable`
rather than permitting the write: an undeterminable boundary is not an absent one.

**It refuses writes, not executions.** Certified phases may still be *run* —
that is how observation evidence gets produced, and `F-10′` depends on it. Only
the persisting write is refused.

---

## 3. Proof against a real re-run

```text
BEFORE   w1-coordination.evidence.json   d54499a0b32c208332eee234d0242ece
         cross-department.evidence.json  9048e4e1b9348e667bceca51f10f3c25
         ACTIVE delegations 1 · records 8

python3 w1_coordination_proof.py
  → CertifiedEvidenceProtected: …/4daebea9012d4cc7.delegation.json
  → exit 1

AFTER    d54499a0b32c208332eee234d0242ece   (identical)
         9048e4e1b9348e667bceca51f10f3c25   (identical)
         ACTIVE delegations 1 · records 8   · git p11 changes 0
```

**The guard fired on the first write the run attempted — the revocation of the
single `ACTIVE` delegation.** That is exactly the hazard `F-12` described,
reproduced against the real path rather than argued.

The refusal is **loud**: exit 1, not a silent skip. And it is **precise** — the
uncertified observation proofs still run clean at exit 0.

---

## 4. Two defects found in this increment, both mine

### `D-1` — the first wiring left a real hole open

`_revoke_stale` mutates delegation records in place, `ACTIVE → REVOKED`. It is a
rewrite of frozen evidence and the first wiring missed it, in **three** modules.

### `D-2` — my conformance test could not see `D-1`

The first version asked whether a **module** imported the guard. `w1_coordination_run.py`
did — so the module passed while an unguarded call site sat inside it.

**A module-level check cannot see an unguarded call in a guarded module.**
Rewritten to check **per call site**: every `write_text` / `write_bytes` whose
receiver is not a `guard(...)` call is an offender. The strengthened test
immediately failed and named three more sites — two genuine holes in the other
modules, and one false positive from my own two-statement form, which was
normalized so the rule has exactly one shape.

**The test that found `D-1` is the one I had to fix first.** A conformance check
that passes because it is looking at the wrong granularity is the same failure as
a guard that passes because it cannot see.

---

## 5. The population is verified, not remembered

`EveryWriterIntoCertifiedEvidenceIsGuarded` walks every non-test module under
`tools/` and the repository root, finds those referencing a certified phase root,
and fails on any unguarded write call. A second test asserts the check **can**
fail — a conformance test that cannot fail proves nothing.

This is the same correction applied to the identifier classes and the citation
roots: a hand-kept list of guarded call sites would drift silently; a measured
one cannot.

---

## 6. Verification

```text
native_core 801 OK (1 expected failure) · consumers 276 OK · tools 789 OK = 1866
   tools +11 — certified-evidence guard conformance
citation 211 documents / 1137 citations / 0 errors
stale-state 507 documents / 0 stale assertions
certified phases {10, 11} · protected roots: docs/architecture/p11
historical rewrite 0 · p11 git changes 0 · protected read 0 / staged 0
```

---

## 7. Frontier

`F-12` **closed**. `F-10′` is now **unblocked**: work paths can execute for
observation without rewriting certified evidence, which was the ordering the
evidence forced. `F-13` remains — W5's *"What is running?"* observes a population
consisting entirely of demonstrators.

```text
P12 AUTHORIZED = TRUE   P12 CONSTRUCTED = FALSE   E12 NOT RATIFIED
```
