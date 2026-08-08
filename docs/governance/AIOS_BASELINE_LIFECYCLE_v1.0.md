# AIOS Baseline Governance Lifecycle

**Status:** Permanent · Append-only
**Version:** v1.0
**Established:** 2026-08-07
**Authority Disclaimer:** This document **records** the baseline lifecycle as it
was operated across the Native Core program; it does not create, amend, or
delegate authority, and it carries no independent governance authority. Every
stage described here derives its authority from the Architect act that
authorizes it. Where anything here appears to conflict with the Engineering
Constitution or the Canonical Domain Model, those documents govern.

---

## 1. Purpose

This document is the permanent record of the **six-stage baseline lifecycle** —
the governance procedure by which every unit of Native Core work was authorized,
built, verified, accepted, frozen, and transported.

It exists because that procedure had no repository artifact. It was applied
seven times without variation, but lived only in the directive series and the
session correspondence that carried it. A reference implementation whose
governance procedure is undocumented cannot be used as an authoritative
construction baseline: a future division could replicate the architecture but
not the discipline that produced it.

Recording it closes the **R11 — Construction Readiness** observation of the
Native Core Completion Review, and the governance-standards half of **R8**.

It follows the repository's established convention for permanent append-only
records (`AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md`,
`AIOS_FINDING_REGISTER_v1.0.md`, `AIOS_PRINCIPLES_REGISTER_v1.0.md`).

---

## 2. Scope

Recorded here: the stage sequence, what each stage requires and produces, the
authorities that must exist before each stage proceeds, and the disciplines that
apply throughout.

Recorded elsewhere:

- **Governance decisions** (including every authorization named below) →
  `AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md`
- **Findings, classifications, dispositions** → `AIOS_FINDING_REGISTER_v1.0.md`
- **Baseline completion status** → `AIOS_NATIVE_CORE_CLOSEOUT_v1.0.md`

This document defines no new authority and no new entity. It describes a
procedure the Architect already exercised.

---

## 3. The Governing Principle

> **One Objective → One Deliverable → One Baseline**

A baseline carries exactly one objective. Work that serves a second objective
belongs to a second baseline, even when the two are adjacent and even when
combining them would be convenient. This is why Native Core conformance was
split into Baselines 04A, 04B, and 04C rather than one; why the governance
closeout (Baseline 05) is separate from the boundary it records; and why
building Optimization (Baseline 06) is separate from any later work on it.

---

## 4. The Six Stages

```
1 Implementation Authorization
        ↓
2 Implementation
        ↓
3 Automated Verification
        ↓
4 Architect Acceptance
        ↓
5 Commit & Freeze
        ↓
6 Transport
```

Each stage requires its own explicit Architect authorization. Completing one
stage authorizes nothing beyond it. **Commit authority (Stage 5) and transport
authority (Stage 6) are separately preserved** — the grant of one is never the
grant of the other.

### Stage 1 — Implementation Authorization

The Architect fixes, in writing and before any work begins:

- the **baseline identifier** and its single objective;
- the **exact allowed path(s)**; no other repository path may be touched;
- the authorized deliverables;
- the forbidden modifications, stated explicitly;
- how findings are to be handled;
- the exit condition.

The engineer then performs a **collision check** (does anything already occupy
the allowed path?) and **Rule 0** (re-read the authoritative sources directly
from source, treating all previous reports as untrusted). If a scope conflict is
found, work stops before implementation and the conflict is reported for a
ruling rather than resolved by the engineer.

### Stage 2 — Implementation

Work proceeds strictly inside the authorized path. The stage produces an
**Implementation Report** stating what was built, what evidence supports it, any
deviation from the authorized structure and why, and every finding discovered.

A discovered problem is **evidence, not a work order**. Verification is never
authorization: nothing found during a baseline may be repaired inside it unless
the repair was itself authorized.

Exit: STOP after Stage 2. No commit, no push.

### Stage 3 — Automated Verification

Independent verification against named gates. Two disciplines are mandatory:

- **Independent re-derivation.** Stage 3 does not reuse Stage 2's helpers or
  conclusions as proof. Where practical it verifies by a *different method* —
  recomputing git blob hashes rather than trusting `git diff`, implementing
  import resolution from the specification rather than reusing the Stage 2
  resolver, cross-checking a static sweep against runtime inspection.
- **False-positive elimination.** Substring and keyword matching produce false
  positives. A finding is not reported until it survives AST-level or
  directory-level analysis. Defects found in the verification code itself are
  **disclosed in the report**, not silently corrected.

Every gate concludes PASS or FAIL, with evidence.

Exit: STOP. No commit, no push.

### Stage 4 — Architect Acceptance

The Architect reviews **evidence, not code**, and issues exactly one decision:
ACCEPTED or REJECTED. Manual code inspection is reserved for two categories:

- **Category A** — invariant violation, frozen-entity modification, boundary
  expansion, governance violation, unauthorized dependency, ADR contradiction,
  or constitutional conflict;
- **Category B** — a failed gate, unexpected regression, missing evidence,
  ambiguous verification, or inconclusive compliance.

Acceptance authorizes Stage 5 and nothing further.

### Stage 5 — Commit & Freeze

Exactly one commit, containing exactly the authorized files. Before committing,
the staged set is verified against the authorization: file count, nothing
outside the allowed path, no protected area, no excluded artifact. After
committing, the freeze is verified independently — commit contents, blob
identity, dependency graph unchanged, protected areas untouched, regression
preserved.

No amend. No squash. No rebase. No history rewrite.

Exit: STOP. **Do not push** — transport authority is a separate act.

### Stage 6 — Transport

The frozen commit is pushed, unchanged, to its branch. Pre-transport
verification confirms HEAD equals the authorized commit, the tree is clean, and
exactly one commit is ahead. Post-transport verification confirms local HEAD
equals remote HEAD, ahead and behind are zero, and no repository content changed
during transport.

On success the baseline is **Frozen & Transported**, and closed: no further
change to it is permitted except through a future authorized **Maintenance
Baseline**, which carries its own full six-stage lifecycle.

---

## 5. Disciplines That Apply Throughout

**Evidence first.** Every claim carries evidence a later reader can re-derive —
a file and line, a command and its output, or a named artifact. Confidence is
tagged: **[E]** direct evidence · **[A]** analysis · **[O]** Architect-reserved.
Tags are never mixed.

**Additive by default.** Ratified and frozen documents are not modified.
Append-only records are appended to; superseded content is marked superseded and
retained in place, never rewritten.

**Reserved means reserved.** An `[O]` item is not resolved by engineering
judgement. It is either exercised by an explicit Architect act — which is then
recorded — or left absent, with the absence verified rather than filled.

**Proposer is not approver.** The party that implements a baseline does not
accept it. This separation holds across all eight repository ADRs and every
Stage 4 of the Native Core program.

**Automation may not self-authorize.** Engineering Constitution §6.2 invariant 2:
*"No governance action proceeds solely because of urgency, automation, tooling
signals, inferred permission, or external pressure. Required approval must exist
before execution. Automation may request. Automation may recommend. Automation
may not override governance authority."* Tooling that requests a commit or a
push — including any automated repository check — is a request, never an
authorization.

**Contradiction halts.** If the authoritative sources contradict one another, or
contradict a prior report, work stops and the contradiction is reported. The
engineer does not resolve it.

---

## 6. Completion Review Outcome Model

From AIOS Native Core v1.0 onward, a Completion Review domain returns one of
three outcomes:

| Outcome | Meaning | Consequence |
|---|---|---|
| **FAIL** | Architecture defect, invariant violation, dependency violation, implementation defect, or repository defect | **Architecture Repair** required before the review may continue |
| **OBSERVATION** | Not a defect: governance completeness, documentation completeness, intentional design, or an architectural evolution candidate | **Governance Resolution**, or classification as an **Accepted Architectural Decision** |
| **PASS** | All acceptance criteria met | Eligible for **Reference Implementation Approval** |

An observation does not imply redesign, and Reference Implementation approval is
not withheld solely because an architectural evolution candidate has been
accepted as an Accepted Architectural Decision.

A Completion Review validates architecture that has been built. It is not a
mechanism for redesigning architecture that has satisfied every invariant and
every conformance gate. Architectural change after a freeze proceeds only
through a Maintenance Baseline with its own lifecycle.

*(Established by P7-I32 Governance Ruling 4; recorded verbatim as GDR-0010 in*
`AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md`*.)*

---

## 7. Application Record

The lifecycle was applied seven times without variation during Native Core
construction, and once more as the program's first Maintenance Baseline:

| Baseline | Objective | Frozen commit | Status |
|---|---|---|---|
| 01 — Skill | Skill boundary (L5) | `21aae20` | Frozen & Transported |
| 02 — Workflow | Workflow boundary (L6) | `bf0a3be` | Frozen & Transported |
| 04A — Knowledge Conformance | Verify Knowledge (L8) | `8dd6513` | Frozen & Transported |
| 04B — Runtime Conformance | Verify Runtime (L2) | `9731964` | Frozen & Transported |
| 04C — Agent Conformance | Verify Agent (L3) | `43652de` | Frozen & Transported |
| 05 — Governance Closeout | Durable governance records | `bb781b9` | Frozen & Transported |
| 06 — L10 Optimization | Optimization boundary (L10) | `c45d82a` | Frozen & Transported |
| MB-01 — Bounded Exception Register | Establish the bounded-exception mechanism (Objective A) | `f76f314` | Frozen & Transported |

History is linear across all eight: no merge, no amend, no squash, no rewrite.

---

## 8. Integrity Verification

- **Document established:** 2026-08-07.
- **Authority created:** none. This document records a procedure; it grants
  nothing.
- **Python files created, modified, or deleted:** 0.
- **`native_core/` changes:** 0.
- **Frozen or transported artifacts modified:** 0.
- **Specification, Blueprint, Roadmap, Freeze, Constitution, Domain Model, or
  ADR changes:** 0.
- **Findings repaired:** 0.
- **Regression:** 495/495 pass; one expected failure (P7-F-2), unchanged.

---

## 9. Closing

This document records a governance procedure and nothing else. It creates no
entity, amends no governance text, redesigns no architecture, grants no
authority, repairs no finding, and authorizes no implementation.

The lifecycle it describes is the one the Native Core was built under. A future
division constructing from the Native Core as its reference inherits both the
architecture and this procedure; neither is complete without the other.
