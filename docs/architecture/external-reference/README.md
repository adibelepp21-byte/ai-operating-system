# AIOS External Reference Registry

**Status:** Permanent · Append-only
**Version:** v1.0
**Established:** 2026-08-08
**Authority:** Directive P7-I43 §5

---

## 1. Purpose

This directory is the permanent record of **External Architecture Intelligence
(EAI)** reviews: architecture-level evaluations of external systems, performed
against the AIOS architecture, and the Governance Decisions that resulted.

Each review answers one question:

> **What does this external reference mean for AIOS Architecture?**

A legitimate answer is **nothing**.

---

## 2. Authority Disclaimer

This registry carries **zero independent governance authority**. It records
external evidence and the decisions taken about it; it defines no entity,
amends no governance text, and authorizes no implementation. Every decision
recorded here derives its authority from the Governance Decision Register entry
it cites. Where anything here appears to conflict with the Engineering
Constitution, the Canonical Domain Model, or a Governance Decision Register
entry, those govern.

An external reference is **not** an AIOS architectural baseline. The normative
comparison baseline is:

```
AIOS Native Core v1.0 / RI-0001
024b9f0c3d2681b463a1421ae88dcf11bf0d7336
```

---

## 3. Governing Hierarchy

```
AIOS Constitution
        ↓
AIOS Architecture Baseline
        ↓
AIOS Native Core v1.0 / RI-0001
        ↓
AIOS Governance Decisions
        ↓
External Reference Knowledge
        ↓
EAI-0001 · EAI-0002 · future external references
```

External references may **challenge**, **corroborate**, or **expose a gap in**
AIOS. They do not automatically redefine AIOS.

---

## 4. The Separation That Must Never Collapse

```
EAI Recommendation
        ≠
Governance Decision
        ≠
Implementation Authorization
```

EAI evaluates and produces a **Decision Recommendation**. Governance produces
the **final architectural decision**. Implementation requires a **separate
engineering authorization** carrying its own six-stage baseline lifecycle. An
EAI recommendation is never represented as a final architectural decision, and
a Governance Decision never authorizes implementation by itself.

---

## 5. Lifecycle

```
Reference Intake
      ↓
Source Verification
      ↓
Extraction
      ↓
Architecture Observation
      ↓
AIOS Comparison
      ↓
Evaluation
      ↓
Decision Recommendation
      ↓
Governance Decision
      ↓
Reference Knowledge
      ↓
Optional Future Maintenance / Architecture Work
```

Stages are not collapsed.

---

## 6. Decision Vocabulary

Exactly one value is assigned per evaluated external pattern.

| Value | Meaning |
|---|---|
| **ADOPT** | Accepted as AIOS Architecture Knowledge / Reference Pattern without substantive architectural transformation. Authorizes no implementation. |
| **ADAPT** | The architectural principle has value but must be transformed to preserve AIOS architectural identity, invariants, governance, or lifecycle. Accepted only in the adapted form, never as a copy. |
| **REJECT** | Not accepted into the AIOS architecture under the current baseline and constraints. The underlying knowledge is retained and remains available to future review. **REJECT ≠ irrelevant.** |
| **OBSERVE** | Potentially relevant but insufficiently mature, applicable, or verifiable for an adoption decision. Alters no AIOS architecture. |

The distribution of outcomes is never optimized. The purpose of EAI is not to
import external architecture; it is to improve AIOS architectural intelligence.

---

## 7. Evidence Rules

Every meaningful claim identifies its source, the exact revision, and the
relevant source location. Documentation claims are distinguished from
implementation evidence. Architecture is never inferred from naming alone.
Where evidence is unavailable, **UNVERIFIED** is recorded rather than
speculation.

Confidence is tagged: **[E]** direct evidence · **[A]** analysis ·
**[O]** Architect-reserved. Tags are never mixed.

---

## 8. No Automatic Pattern Transfer

A prior review is comparative context, never a decision template. The following
inference is prohibited:

```
EAI-000N approved X  →  EAI-000M contains X  →  therefore approve X
```

Similarity of shape is not similarity of architectural meaning:

```
Same pattern shape  ≠  Same architectural meaning  ≠  Same AIOS decision
```

Each review proves its own architectural relevance independently.

---

## 9. Registry Entries

| ID | External reference | Revision | Review status | Governance Decision |
|---|---|---|---|---|
| [**EAI-0001**](EAI-0001.md) | `1jehuang/jcode` (v0.71.1) | `dd8755f7e71f0673911d481b625b8a559c81a8b6` | Complete | **GDR-0012** — recorded 2026-08-08 |

---

## 10. Related Records

- **Governance Decision Register** — `docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md`
- **Finding Register** — `docs/governance/AIOS_FINDING_REGISTER_v1.0.md`
- **Baseline Governance Lifecycle** — `docs/governance/AIOS_BASELINE_LIFECYCLE_v1.0.md`
- **Native Core Closeout** — `docs/governance/AIOS_NATIVE_CORE_CLOSEOUT_v1.0.md`
