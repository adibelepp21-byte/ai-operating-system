# W4 — Authority Chain and Execution, under `FD-P11-001`

> **`FD-P11-001` = ISSUED · W4 authority = RESOLVED · W4 CONSTRUCTED = TRUE ·
> W4 VERIFIED = TRUE (this Act's scope) · W4 CERTIFIED = FALSE.**
>
> The Decision is persisted at
> [`FD-P11-001`](../../governance/acts/FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md),
> body byte-exact, `sha256 7caf9bea52f0b345aa1513ec5ad2c8d007baa77e782b5dc2aeb5e321b814924e`.

---

## 1. `§37.3` — the authority chain, verified and one link reported

`§3` fixes the hierarchy from Constitution down to Implementation, with the
**Co-Founder Delegation Charter** between Canonical Architecture and the Master
Roadmap.

> **Reported, not resolved: the Charter is not resident in this repository.**
> `tools/corpus_citation_audit.py` has recorded
> `AIOS_COFOUNDER_DELEGATION_CHARTER_v1.0.txt` as *"supplied upload, outside the
> repository — ESC-C5-01"* since long before this Act. `§3`'s characterization of
> what the Charter establishes therefore rests on **Founder attestation, which I
> cannot verify against a source body.**
>
> This does not invalidate `FD-P11-001`: `§4.1` is a Founder determination in its
> own right and does not depend on my reading the Charter. But `§34.1` and `§34.3`
> make the Charter a ground on which this Decision could be challenged, and I can
> check neither. **Recorded as a verification limit, not a defect.**

Everything else in the chain was verified from actual bodies: `DP-04`, `DP-03`
and `DP-01` all `Status: ISSUED`, and the three Agent Definitions read from their
resident records with owning department and implemented capability.

---

## 2. The four stages, built as four separate things

`§29` forbids the shortcut `0 instances → create one → delegate to it → W4
works` *"unless every transition is separately represented and verified."*

| Stage | Where | What it is — and is not |
|---|---|---|
| Authorized delegator | `FD-P11-001 §4.1` | a **Founder determination**, read as a constant; not a caller-supplied argument |
| Agent Definition | resident records + `native_core` | describes *what an agent may be* |
| Agent Instance | `tools/agent_instance_registry.py` | *an actual execution identity*; **not** authority (`§17`) |
| Delegation | `tools/w4_delegation.py` | the bounded grant; **not** authority creation (`§16`) |
| Execution | `tools/w4_execution.py` | bounded work; **not** governance authority (`§39`) |

**The canonical mechanism is used, not replaced.** `§7` requires instances be
created *"through the canonical Agent Instance creation mechanism"*, and
`native_core/core/agent/instance.py` already owns `AgentInstance` — deliberately
*"Identity only — no execution, no hosting, no lifecycle, no behavior."* That
supplies two of `§7`'s eight required elements; the other six are organizational
and `DP-04` places them outside the frozen core, so they live in a registration
record wrapping the canonical identity. **Native Core remains at eleven.**

---

## 3. Where the Decision's inequalities became code

`§16` states the rule formally:

```text
Delegated Authority ≤ Available Delegator Authority ∩ FD-P11-001 Scope ∩ Canonical Boundaries
```

Enforced as an **intersection at two levels**, not as a promise:

* an instance may not be registered with capabilities its **Definition** does not
  implement (`§8`);
* a delegation may not grant capabilities beyond the **instance's** permitted
  surface (`§16`).

`§24` demands provenance to `FD-P11-001` **specifically**. Both the registry and
the delegation refuse a citation naming any other instrument — so `DP-01`, which
resolves perfectly well, is rejected for both. That is `§10` in code:
**`DP-01 ≠ SPECIFIC W4 DELEGATION`.**

`§5` rejects Engineering or Platform becoming delegator by label. `engineering`,
`Engineering`, `platform`, `Platform` and `Platform Organization` are each
refused as delegator by name.

`§19` keeps Planning authority with Planning: the executor holds **no**
`adopt`, `adapt`, `revise` or `declare`. An executor that could revise the plan
it is executing would be authorizing its own next instruction.

`§22`/`§27`: a step outside the delegated work scope is **recorded as an
escalation and skipped, and the run continues** with the steps that remain in
scope. Aborting would discard authorized work because unrelated work was refused.

**Outcomes use the ratified Trace vocabulary** — `success · failure ·
escalation`, Domain Model `§2.1`. There is no `authorized` among them, so a W4
outcome cannot claim a status the canonical model does not recognise.

---

## 4. W3 is untouched

`§20`: W3 *"may represent and track"* this Delegation but *"must not manufacture
authority absent valid provenance."*

**The W3 organizational population remains `0`.** W3 is the unit-to-unit
organizational relation, whose delegator would be a Department; this is the W4
*operational* grant from the authorized delegator to a registered instance. They
are different relations at different levels, and collapsing them would make a W4
grant appear as an organizational delegation nobody issued. Asserted as a test.

---

## 5. Verification

`§23`'s twenty controls, `§25`'s ten instance proofs, `§26`'s completeness rule,
and `§18`'s chain walked end to end — **40 tests**, all passing.

### Every control mutation-probed

```text
delegator not checked (§14)         -> FAILED (5)
FD-P11-001 provenance not required  -> FAILED
scope may exceed instance (§16)     -> FAILED
unregistered recipient accepted     -> FAILED
instance may exceed definition (§8) -> FAILED
work scope not enforced (§22)       -> FAILED
unratified status permitted         -> FAILED
anonymous instance permitted (§7)   -> OK   ← a real gap, not a bad probe
```

**The eighth probe found a missing control.** Disabling the identity check left
the entire suite passing, which meant nothing tested `§7`'s *"No anonymous Agent
Instance is valid."* The harness — which now refuses to run unless the anchor
matches exactly once, the mutation changes something, and the result parses — had
already ruled out the probe being at fault, so the `OK` could only mean the
control did not exist. Three tests were added; the probe now fails with five.

**This is the first time the mutation discipline found a missing control rather
than confirming an existing one.** Four Acts of defective probes made that
possible: each fix removed a way for a probe to lie, and what is left is a probe
that can only be telling the truth.

---

## 6. Defects

| Defect | Impact | Root cause | Action | Status |
|---|---|---|---|---|
| Executor accepted a non-Delegation | authority stage skippable; failed later with `AttributeError` | validated at use rather than construction | refuses at construction (`§18`) | **FIXED** |
| No control for anonymous instances | `§7` requirement untested | never written | three tests added | **FIXED** |
| My assertion `"Founder" not in delegator` | test failed against correct code | **`Co-Founder` contains `Founder`** — substring false positive | asserted as identity inequality | **FIXED** |
| Six typographic characters flattened | canonical text silently altered | shell heredoc | restored before hashing | **FIXED, disclosed** |
| Charter non-resident | one chain link unverifiable | outside the repository | reported as a verification limit | **OPEN, classified** |

The substring error is the same mechanism as the probe defect two Acts ago
(`authority = AuthorityProvenance(` matching inside `goal_authority = …`) and the
`Volume VII`/`Volume VIII` inflation before that. **Three occurrences, three
different contexts: substring reasoning fails here repeatedly, and it fails
silently in the direction of a conclusion I already expect.**

---

## 7. State

```text
tools 528 OK · native_core 801 OK (1 expected failure) · consumers 276 OK
citation 153 documents / 0 errors · stale-state 463 / 0 assertions
Native Core = 11 · Agent Definitions = 3 · W3 organizational delegations = 0

FD-P11-001 = ISSUED       W4 AUTHORITY   = RESOLVED
W4 CONSTRUCTED = TRUE     W4 OPERATIONAL = FALSE (no resident instance registered)
W4 VERIFIED = TRUE (chain + controls)    W4 CERTIFIED = FALSE
E11 RATIFIED = FALSE      P12 AUTHORIZED = FALSE      NATIVE CORE #12 = NOT AUTHORIZED
```

**`W4 OPERATIONAL = FALSE` deliberately.** The machinery is built and exercised
end to end in tests. **No Agent Instance is registered in a resident, persisted
population**, because registering one commits the organization to an execution
identity, and `§7` makes creation an `AUTHORIZED ACTION` rather than an automatic
consequence of the machinery existing. The mechanism-before-population order is
the same one W3 follows.

`§35`: authority resolution *"does not mean W4 is already"* constructed,
operational, verified, complete or certified.
