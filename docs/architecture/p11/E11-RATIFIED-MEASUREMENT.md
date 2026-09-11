# P11 measured against ratified `E11`

> **`DP-02` is ISSUED.** `E11 RATIFIED` moves **`FALSE → TRUE`**. Nothing else
> moves — `§1` and `§8` say so directly, and `§10` fixes
> **`RATIFICATION ≠ PASS`**.
>
> Executed under `DP-02 §11`, the eleven-step post-decision sequence. **No new
> Act was created** (`§11`), no criterion was pre-populated (`§7`), and no
> cross-Department evidence was manufactured or substituted (`§11`).

---

## 1. Persistence and verification (`§11` 1–3)

The Decision is persisted verbatim at
[`docs/governance/acts/DP-02-P11-E11-RATIFICATION.md`](../../governance/acts/DP-02-P11-E11-RATIFICATION.md).

```text
sha256(body) = df769fb9a530eda91c8773eae9fb24b0b1464eedeb9aad073713a049f691d8ea
persisted body == supplied body : byte-identical, 15 162 bytes
Status : ISSUED · Authority : AIOS Founder · Effective : 2026-09-11
```

**The persisted body is byte-identical to the supplied text** — not even the
trailing-newline difference `FD-P10-004`'s persistence had to record. My first
provenance block claimed such a newline existed; it did not, and the claim was
corrected rather than left as harmless boilerplate.

**The ratification is the Founder's act.** `DP-01 §8` lists *"ratify E11
criteria"* among what the executor may not do; `FD-P11-001 §12` item 9 excludes
*"Authority to ratify E11"*. Neither was exercised.

---

## 2. Candidate → ratified reconciliation (`§11` 4–5)

| | Prepared as | Ratified as | Change |
|---|---|---|---|
| `E11-01`…`E11-03`, `E11-05`…`E11-08` | CANDIDATE | **RATIFIED** | status only |
| `E11-04` | CANDIDATE — two readings | **RATIFIED as Cross-Department Coordination** | the Founder chose the **canonical** reading |
| `E11-09` Organizational Continuity | *proposed, `F2`* | **RATIFIED** | new criterion |
| `E11-10` Bounded Autonomy & Governance Integrity | *proposed, `F3`* | **RATIFIED** | new criterion |
| Negative controls | *proposed as a dimension* | **mandatory integrity evidence, not a capability** (`§5`) | structural placement changed |
| Prioritization / ranking | excluded (`F7`) | **excluded, Architect-reserved** (`§6.1`) | confirmed |
| `E11-03` refusal semantics | flagged (`F5`) | **adopted into the criterion** (`§3`) | absorbed |
| P12 unified state | excluded (`F8`) | **excluded** (`§6.2`) | confirmed |

**All three open questions were settled in the stricter direction.** The package
presented `E11-04`'s narrow reading as satisfiable today; the Founder took the
canonical one, under which it is not.

---

## 3. Measurement (`§11` 6–8)

Instrument: [`tools/e11_measurement.py`](../../../tools/e11_measurement.py) —
what `DP-01 §9` permits construction to prepare, *"instrumentation and evidence
required to support future E11 verification."* Every verdict derives from
records on disk; nothing is asserted from a prior report. Record:
[`e11-measurement.json`](e11-measurement.json).

| | Criterion | Verdict |
|---|---|---|
| `E11-01` | Planning | **PASS** |
| `E11-02` | Delegation | **PASS** |
| `E11-03` | Execution | **PASS** |
| `E11-04` | **Cross-Department Coordination** | **FAIL / UNSATISFIED** |
| `E11-05` | Observation | **PASS** |
| `E11-06` | Verification | **PASS** |
| `E11-07` | Escalation | **PASS** |
| `E11-08` | Accountability | **PASS** |
| `E11-09` | Organizational Continuity | **PASS** |
| `E11-10` | Bounded Autonomy & Governance Integrity | **PASS** |

```text
PASS 9 · FAIL 1 · E11 = NOT PASSED
```

### `E11-04`, measured the way the Decision requires

`§10` fixes **`MULTI-AGENT ≠ CROSS-DEPARTMENT COORDINATION`**, so the check never
consults agent count. It resolves each coordination participant through its Agent
Definition to the **owning Department** — three independent surfaces joined, and
an instance whose Definition no Department claims resolves to nothing rather than
being attributed to one.

```text
departments resident            : engineering, platform
instance → department           : engineering-intelligence-instance-001    → engineering
                                  governance-artifact-integrity-instance-001 → platform
coordinations on record         : 1   (REAL-RUNTIME, terminal SUCCEEDED)
    participants                : ['governance-artifact-integrity-instance-001']
    departments spanned         : ['platform']   → 1
coordinations spanning > 1 dept : 0
```

**Both Departments exist. One registered instance each exists. No single
coordination has ever joined them.** `§7`: recorded `FAIL / UNSATISFIED` rather
than *"manufacturing a PASS through semantic substitution."*

### The other nine, and what each was measured on

- **`E11-01`** `PLANNED → ADAPTED → REVISED` exercised live; `sequence()` returns
  dependency order; both real runs carry a plan whose authority citation resolves;
  the planning surface exposes no authorization method.
- **`E11-02`** 14 grants — all cite an instrument, all provenance resolves, all
  recipients registered, all scopes within the instance's permitted surface, no
  recipient its own accountable party, revocation represented, 0 tracking defects,
  every ACTIVE grant represented.
- **`E11-03`** every run cites a real grant; every chain ends at `founder:Founder`;
  each refused step became a recorded escalation. **A correct refusal is not
  counted as failure** — `§3` says so in the criterion, so the verdict turns on
  whether refusals happened when they should, never on whether one occurred.
- **`E11-05`** detect-only: no public name on the observation surface contains
  `authorize`, `approve`, `decide`, `rank`, `prioriti` or `grant`.
- **`E11-06`** 801 + 276 + 707 = **1 784** tests; every grant states a verification
  requirement; every run carries outcome evidence.
- **`E11-07`** a real refusal persisted and `OPEN` against a human; no method on
  the register resolves, approves, authorizes, grants, permits or closes.
- **`E11-08`** every link of `who delegated → to whom → for what → under which
  authority → with what scope → what happened → who verified → who remains
  accountable` recoverable for both runs; accountability never transferred.
- **`E11-09`** a **second process** rebuilt both operational roots and agreed
  exactly; all eleven evidence classes `§4` names are covered; revoked stays
  revoked across the boundary.
- **`E11-10`** ten integrity controls, each exercised against a real attempt: six
  unauthorized delegation shapes refused; a revoked grant refused projection; four
  non-`HumanAuthority` approval attempts refused with the escalation left `OPEN`;
  a genuine `HumanAuthority` response still accepted, so the control is a boundary
  and not a wall; Native Core still 11.

---

## 4. A control fired on the run that created the instrument

`test_p11_governance_boundary`'s completeness guard **failed the first
measurement run**: `tools/e11_measurement.py` imports the planning package, which
makes it a P11 handoff surface, and it was not in the declared set.

`E11-06` was therefore measured **FAIL on that run**, correctly — the tools suite
was genuinely red, and the instrument refused to report verification as
established while it was. The surface was declared and the measurement re-taken.

**This is the fourth time that guard has collected, and the first time the
surface it caught was the instrument measuring whether the boundary holds.** A
measurement instrument outside the provenance control could have forged a
citation and measured itself compliant.

---

## 5. Rediscovery (`§11` 9)

**One actionable frontier: `E11-04`.** Its immediate blocker is not a missing
mechanism, and is stated here from the record rather than diagnosed:

`docs/architecture/organization/engineering/agent-definitions/engineering-intelligence-agent.md`,
`## Permitted Skills`:

> **None declared.** … *"No Skill exists within the Engineering Department's
> scope, and none is created by this document."*

A `WorkflowStep` requires `performed_by` **and** `composes: SkillRef`. Coordination
occurs *through* a Workflow (`INV-13`). So an Engineering actor cannot appear in
any coordination while no Skill is permitted to its Agent Definition — the same
class of blocker `ACT-CC-P11-008` hit, now on the other Department.

**Authority reading, stated so it can be checked rather than assumed.**

| Prerequisite | Canonical position | Tier |
|---|---|---|
| Create a Skill record | *"Skill / Tool / Runtime — **Owned centrally**"* (Domain Model `§5`); resident Skill records state *"It does not itself grant or define any authority"* | documentation of a centrally-owned execution artifact; no ADR |
| Amend an Agent Definition's Permitted Skills | *"created/deprecated at **Platform Division discretion** within Capability governance"* (Domain Model `§6`); `ADR-0003` — *"Department-discretion, Implementation Tier"* | Implementation Tier |
| The coordination itself | `DP-01 §3 W1` authorizes construction of *"cross-department coordination"* **by name** | already authorized |

**`DP-02 §11`'s prohibition is the binding constraint, not the authority.** The
Decision forbids manufacturing cross-Department evidence. A Skill invented so
that `E11-04` can pass would be exactly that. A Skill documenting work an
Engineering instance has **already performed and evidenced** — the `13/13`
conformance verification in `first-execution.evidence.json`, the Testing
sub-ability its own Agent Definition names — would not.

**That distinction is the whole of it, and it is checkable**: the work exists on
record before the Skill does.

---

## 6. State after this Decision

```text
P11 AUTHORIZED  = TRUE      P11 EXHAUSTED = TRUE  (construction frontier, §9)
P11 CONSTRUCTED = TRUE      P11 COMPLETE  = FALSE
P11 OPERATIONAL = TRUE      P11 CERTIFIED = FALSE
P11 VERIFIED    = TRUE      E11 RATIFIED  = TRUE   ← moved
                            E11 PASS      = FALSE  (9 of 10)
```

`§9`: construction exhaustion is **not invalidated** and is **not converted into
completion**. The sequence is
`CONSTRUCTION EXHAUSTION → FOUNDER E11 RATIFICATION → E11 MEASUREMENT →
ACTIONABLE GAP DISCOVERY → REMEDIATION IF AUTHORIZED → FRESH EXHAUSTION →
COMPLETION → CERTIFICATION`, and this document is the third and fourth steps.

Native Core **11**. Protected paths read **0**. No new Act, no new entity, no new
subsystem, no P12, no authority created.
