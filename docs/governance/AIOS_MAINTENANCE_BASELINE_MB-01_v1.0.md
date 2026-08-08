# Maintenance Baseline MB-01 — Stage 1 Implementation Authorization

**Status:** Stage 1 — Authorization boundary established · Implementation NOT authorized
**Version:** v1.0
**Established:** 2026-08-08
**Governing act:** P7-I48 — EP-1 Bounded Exception Register · Maintenance Baseline Stage 1 Authorization
**Authority Disclaimer:** This artifact records the Stage 1 authorization boundary for one Maintenance Baseline. It creates no entity, amends no governance text, grants no authority beyond what P7-I48 states, and authorizes no implementation. Where anything here conflicts with the Engineering Constitution, the Canonical Domain Model, `AIOS_BASELINE_LIFECYCLE_v1.0.md`, or GDR-0012, those govern.

---

## 1. Baseline Identity

| Field | Value |
|---|---|
| **Baseline identifier** | **MB-01** |
| **Class** | **Maintenance Baseline** — the first in the AIOS program |
| **Title** | Bounded Exception Register — Mechanism Establishment |
| **Date** | 2026-08-08 |
| **Governing act** | P7-I48 |
| **Related governance decision** | **GDR-0012** §3.12.2, §3.12.3 — EP-1 Ratcheting Quality Budgets, **APPROVED AS ADAPT** |
| **Related findings** | **P7-F-2** (subject of the *successor* baseline MB-02, not of MB-01) |
| **Related reference knowledge** | GDR-0013 / EAI-0002 **RK-10** — advisory only, not authority |
| **Lifecycle** | The six-stage lifecycle of `AIOS_BASELINE_LIFECYCLE_v1.0.md` §4 |
| **Current stage** | **Stage 1 — Implementation Authorization** |

**[A] Identifier convention.** No Maintenance Baseline has previously existed, and the corpus fixes no naming convention for one. `MB-01` is adopted here to keep the maintenance series visibly distinct from the construction series (01, 02, 04A, 04B, 04C, 05, 06) recorded in `AIOS_BASELINE_LIFECYCLE_v1.0.md` §7. **[O]** The Architect may substitute another identifier; nothing else in this artifact depends on the choice.

---

## 2. Single Objective

> **Establish the Bounded Exception Register as an AIOS conformance mechanism: a committed, append-only, identity-based allowlist of known conformance-exception sites, together with a fail-closed verifier that fails when an unregistered exception site appears *and* fails when a registered site is absent — delivered with no registered entries, applied to no existing finding, and modifying no frozen baseline.**

**[A] Why this is operationally testable.** The objective is satisfied exactly when the verifier, run against an empty register, (a) passes on a tree containing no exception sites, (b) fails on the introduction of an unregistered site, and (c) fails when an entry names a site that does not exist. Each condition is decidable by execution. The objective explicitly does **not** include making any real finding pass, which is what keeps it a single objective.

**Delivered empty and unapplied.** MB-01 builds the instrument. It does not use it.

---

## 3. Scope

### 3.1 Scope decision — TWO baselines

**[E] `AIOS_BASELINE_LIFECYCLE_v1.0.md` §3:** *"A baseline carries exactly one objective. Work that serves a second objective belongs to a second baseline, even when the two are adjacent and even when combining them would be convenient."*

EP-1 carries two objectives:

| | Objective | Baseline |
|---|---|---|
| **A** | Establish the Bounded Exception Register mechanism | **MB-01** — this baseline |
| **B** | Apply the mechanism to the five P7-F-2 `KnowledgeError` sites inside frozen Baseline 04A | **MB-02** — a separate, later, separately authorized baseline |

**[E] The two are not merely adjacent — they carry different authorization requirements.** Objective B necessarily modifies `native_core/core/knowledge/tests/test_knowledge_conformance.py`, whose `@unittest.expectedFailure` marker at line 358 is the very mechanism the register would replace. `git log` shows that file last committed at **`8dd6513` — "Baseline 04A: Knowledge Conformance"**, a frozen and transported baseline. Objective A touches no frozen artifact at all.

**[E] GDR-0010 Ruling 3** requires, for any change to Baseline 04A: *"Maintenance Baseline yang secara eksplisit mengotorisasi perubahan terhadap Baseline 04A."* That condition attaches to **B only**.

**[A]** Combining them would place a low-risk new-path deliverable and the program's first modification of a frozen baseline under one authorization, so that accepting the mechanism would implicitly accept the frozen-baseline change. The lifecycle's precedent runs the other way: Native Core conformance was split into 04A/04B/04C rather than one, and Baseline 05 was kept separate from the boundary it records.

**Scope decision: TWO BASELINES. MB-01 is Objective A only.**

### 3.2 Authorized paths

```
tools/bounded_exception/          — mechanism implementation (new)
tools/bounded_exception/tests/    — mechanism tests (new)
```

**[E] Path rationale.** `tools/` is the established location for repository-level validation outside `native_core/`: it already carries `tools/validate_execution_catalog.py`, `tools/validators/` (14 modules), and `tools/tests/`. **[E] Native Core Blueprint §31** forbids a twelfth boundary, so the mechanism cannot be added to `native_core/`'s eleven-boundary tree, and `native_core/shared/` is reserved for primitives consumed by those boundaries.

No other path may be touched.

### 3.3 Scope coverage — explicit answers

| Question | Answer |
|---|---|
| Does MB-01 cover mechanism construction? | **YES** |
| Does MB-01 cover P7-F-2 application? | **NO** — deferred to MB-02 |
| Is frozen Baseline 04A in scope? | **NO.** MB-01 authorizes **no** change to Baseline 04A, and none is required by its objective |
| Is `native_core/` in scope? | **NO** — zero modifications |
| One or two baselines required? | **TWO** (§3.1) |

---

## 4. Authorized Deliverables

Stage 1 fixes these as the complete deliverable set. Nothing outside it is authorized.

| # | Deliverable | Constraint |
|---|---|---|
| D-1 | **Register format** — a committed, append-only, machine-readable record of exception entries. Each entry carries file, locator, and the governing **Finding ID** and **Governance Decision ID** | Identity-based, never a count |
| D-2 | **Register instance** — created **empty**, with zero entries | No finding may be registered under MB-01 |
| D-3 | **Verifier** — fails on an unregistered exception site; fails on a registered site that is absent | Fail-closed in **both** directions |
| D-4 | **Tests** for D-1 … D-3, covering the three conditions in §2 | Tests of the mechanism only; no Native Core test may be added or altered |
| D-5 | **Documentation** of the mechanism, its invariants, and the authorization required to add an entry | Records the mechanism; grants no authority |

**[E] Each deliverable traces to GDR-0012's approved direction**, which requires the adaptation to preserve *"fail-closed enforcement; explicit exception identity; append-only governance; Architect authorization; traceability to a Finding / Governance Decision; no self-service baseline expansion."*

**[E] Explicitly excluded by GDR-0012's own terms:** any `--update`, `--fix`, or equivalent flag capable of expanding the register. Growth is an Architect act recorded as a Governance Decision Register entry. GDR-0012: *"It must NOT become a mechanism for silently normalizing architectural violations."*

**[A] Discipline constraints inherited from the program:** standard library only, offline, no singleton, registry, reflection, dynamic import, cache, global, async, thread, UUID, timestamp, or randomness.

---

## 5. Forbidden Modifications

MB-01 prohibits, without exception:

- any modification to `native_core/**`;
- any modification to frozen Baseline 04A, and to Baselines 01, 02, 04B, 04C, 05, 06;
- any modification to the five P7-F-2 raise sites (`admission.py:86,88`, `repository.py:95,97`, `retrieval.py:64`) or to the `@unittest.expectedFailure` marker at `test_knowledge_conformance.py:358`;
- registering any finding, P7-F-2 included, in the register delivered by MB-01;
- any modification to GDR-0012, GDR-0013, or any other register entry;
- any modification to EAI-0001, EAI-0002, or the External Reference Registry;
- creation or modification of an ADR (see §7);
- any modification to the Constitution, Canonical Domain Model, Architecture Freeze, Blueprint, Roadmap, or Implementation Constitution;
- any unrelated Native Core, governance, or architecture change;
- any unrelated test, refactor, or optimization;
- any change to the freeze tag `aios-native-core-v1.0`, and any retry of its blocked transport;
- **`tools/.gitignore`** — the permanent untracked exclusion, which must remain untracked, unstaged, unmodified, and uncommitted;
- any EAI-0003 work of any kind;
- any change outside the paths of §3.2.

---

## 6. Finding Handling

**[E] `AIOS_BASELINE_LIFECYCLE_v1.0.md` §4, Stage 2:** *"A discovered problem is **evidence, not a work order**. Verification is never authorization: nothing found during a baseline may be repaired inside it unless the repair was itself authorized."*

That rule governs MB-01 unchanged.

| Case | Handling |
|---|---|
| **P7-F-2** | **Not touched.** MB-01 neither repairs nor registers it. Its Category B disposition — *"Recorded only. Repair not authorized."* — is unchanged. It is the subject of MB-02. |
| **A new finding inside the authorized paths** | Recorded in the Stage 2 Implementation Report and appended to `AIOS_FINDING_REGISTER_v1.0.md` only under a separate recording authorization. Not repaired inside MB-01. |
| **A new finding outside the authorized paths** | Recorded and reported. Not repaired. Not entered into the register. |
| **A defect in MB-01's own verification code** | **Disclosed in the report**, per the Stage 3 discipline, not silently corrected. |

**Escalation trigger.** Any discovery that would materially change the objective, the scope, the frozen-baseline posture, the governance posture, or the deliverable set **halts work immediately** and is reported for an Architect ruling. It is never resolved by engineering judgement, and implementation convenience never expands scope.

---

## 7. ADR Requirement — RESOLVED: **ADR REQUIRED**

**[E] Engineering Constitution §3.4:** *"An Architecture Decision Record (ADR) is the required instrument for any architectural-tier change."* An ADR *"may change: the Canonical Domain Model; Department and Capability structure; the Architectural Backlog; **cross-Department architectural conventions**."*

**[E] ADR Framework** (`docs/architecture/adr/README.md`): *"An ADR is not required for implementation-tier work within already-approved Capabilities, or for Knowledge additions made through the governed-review promotion pipeline."*

**[A] Determination.** The Bounded Exception Register is not implementation-tier work inside an approved Capability. GDR-0012's approved direction describes a mechanism carrying *governance* properties — *"append-only governance,"* *"Architect authorization,"* *"traceability to a Finding / Governance Decision,"* *"no self-service baseline expansion"* — and it is framed generally, not as a Knowledge-local test helper. A verification instrument whose allowlist can be changed only by an Architect act recorded in the Governance Decision Register is a **cross-Department architectural convention**, which §3.4 places squarely inside the ADR instrument.

**Determination: ADR REQUIRED** for the establishment of the mechanism.

**[E] P7-I48 did NOT authorize its creation.** P7-I48 §8 and §17: *"Do not create an ADR unless the ADR requirement is explicitly resolved AND its creation is separately authorized."*

**[E] P7-I49 §6 subsequently authorized creation.** The ADR is
**[ADR-0009](../architecture/adr/decisions/ADR-0009.md)** — *"Establish the
Bounded Exception Register as the AIOS mechanism for bounded, identity-based
conformance exceptions"* — filed with status **Proposed**. P7-I49 authorized
creation, not approval; approval rests with the Architect under Constitution
§3.4, and `AIOS_BASELINE_LIFECYCLE_v1.0.md` §5 holds that the proposer is not
the approver.

**[E] ADR-0009 was approved by the Architect under P7-I50** on 2026-08-08, with
its decision text unchanged. Prerequisite **E-10** in §8 below is therefore
**SATISFIED**.

**Consequence:** **E-11 — Stage 2 authorization — remains UNSATISFIED.**
P7-I50 §4: *"The approval does not authorize implementation."* Approving the
architectural decision is not authorization to build it; Stage 2 requires its
own separate Architect act.

**[O] Reserved.** Should the Architect intend a deliberately narrower mechanism — scoped to a single boundary and carrying no cross-boundary convention — the determination would change to ADR NOT REQUIRED. That narrowing is an Architect ruling, not an engineering judgement, and is not assumed here.

---

## 8. Exit Condition

Stage 1 is complete when **all** of the following hold. Each is presently satisfied unless marked otherwise.

| # | Condition | State |
|---|---|---|
| E-1 | Governing decision verified from source (GDR-0012 §3.12.2 / §3.12.3) | ✅ |
| E-2 | Frozen-baseline precedent verified (GDR-0010 Ruling 3) | ✅ |
| E-3 | Canonical lifecycle verified (`AIOS_BASELINE_LIFECYCLE_v1.0.md`) | ✅ |
| E-4 | Baseline 04A identity and frozen status verified (`8dd6513`) | ✅ |
| E-5 | P7-F-2 evidence verified at source | ✅ |
| E-6 | Scope decision resolved — **TWO baselines** | ✅ |
| E-7 | Authorized paths fixed, collision-checked, outside every frozen boundary | ✅ |
| E-8 | Deliverables, forbidden modifications, and finding handling fixed in writing | ✅ |
| E-9 | ADR requirement resolved — **REQUIRED** | ✅ |
| E-10 | Approved ADR exists for the mechanism | ✅ **SATISFIED** — **ADR-0009 Approved** by the Architect under P7-I50, 2026-08-08 |
| E-11 | Stage 2 authorization issued by the Architect | ✅ **SATISFIED** — **P7-I52**, 2026-08-08. Stage 2 completed at `f76f314`; Stage 3 independently verified under P7-I53; Stage 4 **ACCEPTED** under P7-I54 |

**E-1 … E-9 are satisfied: the authorization boundary is established.**

**[E] Stage 1 completion does not authorize Stage 2.** `AIOS_BASELINE_LIFECYCLE_v1.0.md` §4: *"Each stage requires its own explicit Architect authorization. Completing one stage authorizes nothing beyond it."* The canonical lifecycle grants **no** automatic progression. Implementation begins only when E-10 and E-11 are both satisfied.

---

## 9. Successor Baseline (recorded, not authorized)

**MB-02 — Bounded Exception Register · Application to P7-F-2.** Objective B of §3.1. It will require, at minimum: explicit authorization to modify **frozen Baseline 04A** per GDR-0010 Ruling 3; a decision on whether registering P7-F-2's five sites supersedes or accompanies the `@unittest.expectedFailure` marker; and its own full six-stage lifecycle.

**MB-02 is not authorized, not opened, and not begun.** It is recorded here only so MB-01's deliberate incompleteness is legible.

---

## 10. Integrity Verification

- **Authority created:** none. This artifact records a boundary; it grants nothing.
- **Implementation performed:** none.
- **Python files created, modified, or deleted:** 0.
- **`native_core/` changes:** 0.
- **Frozen or transported baselines modified:** 0.
- **P7-F-2 sites modified:** 0. `expectedFailure` marker: unchanged.
- **Register entries created or modified:** 0. GDR-0012 and GDR-0013 unchanged.
- **EAI records modified:** 0.
- **ADRs created:** 0.
- **Findings repaired:** 0.
- **Freeze tag:** untouched.
- **`tools/.gitignore`:** untracked, unstaged, unmodified.
- **Regression:** 495/495 pass; one expected failure (P7-F-2), unchanged.
- **Governance Decision Register entry:** none created. Per the **GDR-0009** precedent — *"Baseline 06 · L10 Optimization — **Full Lifecycle Record**"*, recorded across directives P7-I26 … P7-I30 at completion — a baseline is entered in the register as a completed lifecycle record, not at Stage 1. That entry remains a future act requiring its own authorization.

---

## 11. Closing

MB-01 establishes an authorization boundary and nothing else. It builds no mechanism, registers no exception, touches no frozen artifact, and repairs no finding.

Its purpose is that when the Bounded Exception Register is eventually built, the boundary it was built inside was fixed in writing beforehand — by the Architect, before any work began, exactly as the lifecycle requires.
