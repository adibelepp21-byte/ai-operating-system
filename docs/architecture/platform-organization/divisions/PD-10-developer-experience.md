# PD-10 — Developer Experience

> **Status: DERIVED.** Constructed under `FDE-P10-FRONTIER-02`, Decision A.
> **Naming divergence unresolved — see §2.** Below the Established section is
> bounded derivation, **not canonical**.

| | |
|---|---|
| **CPID** | `PD-10` — permanent, and the stable identity anchor while the name is contested |
| **Name used for construction** | Developer Experience — per `FDE-P10-FRONTIER-02 §20` |
| **Established domain** | Developer-facing interface |
| **Primary construction target** | SDK, CLI, API, tooling, documentation |
| **Maturity** | DISCOVERED → **CONSTRUCTED (derived, name-contested)** |

---

## 1. Established (source constraint)

- `MASTER_ROADMAP §5` — *"`PD-10` **Developer Experience**"*.
- Frozen `PD-02 A4:288` — *"PD-10 **Developer Enablement**"*.
- `PD-01 C10:92` — own domain success criteria.
- Frozen `PD-02 E4:1431`, `D4:1125` — *"PD-03 hingga PD-10 dengan domain adaptation"*, *"tanpa memaksakan metric PD-02"*.

## 2. The name is used, not decided

`FDE-P10-FRONTIER-02 §20` permits construction under **Developer Experience**
while forbidding resolution of the divergence: *"Claude must not resolve a
previously identified naming divergence merely for consistency… record →
reconcile → escalate, rather than choose → normalize → declare."*

**Accordingly: the name above is a construction convenience authorized by the
event, and is not a determination.** The frozen corpus says *Enablement*; the
registry says *Experience*; neither is a truncation of the other, and no resident
source establishes precedence between a frozen corpus and the program registry
(`G-02`). **The CPID carries identity in the meantime**, which is exactly what
`§3.1`'s permanence rule is for.

Worth noting the two names are not synonyms. *Enablement* suggests capability
provision; *Experience* suggests interface quality. Which one governs would
change this division's decomposition — so §4 below is provisional in a way the
other divisions' are not.

## 3. The reference-count trap, recorded because this division set it

PD-10 carries **40 resident references — third-highest of the eight** — and
essentially no domain substance. Nearly every reference is the adaptation rule
naming *"PD-03 hingga PD-10"* as a **range**, not a statement about PD-10.

A raw count would have ranked this division better-defined than `PD-05`, which
owns Runtime outright with 11 references. That is `G-08`, and this division is
where it was found.

## 4. Derived organizational structure

| Part | Derivation for PD-10 |
|---|---|
| **A — Identity & Mandate** | Developer-facing interface domain: SDK, CLI, API, tooling, documentation |
| **B — Organization** | Candidate decomposition follows the five construction targets. **Derived from the target list alone** — and provisional pending the name question, since *Enablement* and *Experience* would weight these differently |
| **C — Governance** | No resident governance statement. Subject to architecture like any division; nothing further evidenced |
| **D — Operating** | Not derived — an interface-surface operating model without a resident source would be invention |
| **E — Performance** | Not derived. Under *Experience* this would be developer-outcome measurement; under *Enablement*, capability coverage. **The unresolved name blocks a defensible derivation**, which is the clearest practical cost of `G-02` |

## 5. A boundary worth flagging early

AIOS already has substantial developer-facing surface — `tools/` (25 modules),
the governance index CLI, conformance suites, and the documentation corpus. **None
is bound to PD-10**, and no binding is asserted. If PD-10 is later bound to that
surface, the `tools/` ↔ `consumers/` mutual isolation guards already in the test
suite become a PD-10 concern, not merely an engineering one.

## 6. Unresolved

**The name** (`G-02`) — and it is not cosmetic: it changes §4's decomposition ·
binding to the resident developer surface · whether "documentation" here includes
the governance corpus or only developer-facing material · relationship to PD-09
where tooling meets verification.

## 7. Not constructed

No name resolved, normalized, or declared. No binding to `tools/` or any resident
developer surface. No operating or performance model invented on a contested
identity. Nothing canonicalized or frozen.


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

### Specific to `PD-10`

- **`G-02` is now unavailable on a second, independent ground.** The
  *Developer **Enablement*** / *Developer **Experience*** divergence is a naming
  question about an entity whose lifecycle is *"created/retired via architectural
  decision, **architect approval**"* (`Domain Model §6`, `E-83`). It was already
  unresolvable for want of a precedence rule; renaming is now barred on the
  lifecycle rule as well.
