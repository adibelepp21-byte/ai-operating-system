# F-5 — Construction Evidence Classification · PD-05 … PD-10

| Field | Value |
|---|---|
| **Under** | `ACT-CC-POST-P13-PLATFORM-ORG-003` v1.1 `§14` (replacing F-5), `§16` |
| **Prepared by** | Claude Code — Co-Founder / CEO · 2026-09-26 |
| **Nature** | Evidence classification made **before** construction, as `§14` requires. It is recorded here as it stood, with the finding that changed during construction marked |

## 1. The matrix

The columns are those of `§14`.

| PD | Source evidence | Reference evidence | Domain evidence | Existing artifact | Authority | Construction readiness |
|---|---|---|---|---|---|---|
| **PD-05** | **Strong.** Frozen PD-02 prose: *"PD-05 owns Runtime."* (B7); A5 execution rows; C8 §32. `ADR-0019` (Approved): the Runtime → Execution Layer → consumer boundary. Freeze §4: Runtime entity *"owned centrally"* | ACT-003 `§23` candidate Part C (10 titles; none resident) and D list | `runtime_spec.md` §1–§13 | `native_core/core/runtime/`: name correspondence, **not** ownership; P10 record (DERIVED) | Operational execution in the Runtime domain; the *"Runtime owner"* role is not stated to be PD-05 | **Constructible.** Architecture core source-derived |
| **PD-06** | **Moderate.** *"PD-06 owns implementation."* (B4); C8 §33 *"implementation responsibility"*; D8; A5 row; C8 §18 | ACT-003 `§24` scope (no section list) | none dedicated | `agent` and `skill` subsystems, no name correspondence; P10 record | Implementation execution; the scope of "implementation" is not stated | **Constructible.** Scope held unknown |
| **PD-07** | **Strong.** *"PD-07 tetap memiliki ownership atas Infrastructure."* (C8); C8 §34; A5 row; Infrastructure Auditing Principle Review | ACT-003 `§25` candidate Part C | `infrastructure_spec.md` §1–§13 | `native_core/core/infrastructure/`: name correspondence; P10 record | Infrastructure execution; facilities hold none | **Constructible.** Five candidate sections fall in reserved architecture |
| **PD-08** | **Role only.** Security owner properties (A5, A6, C8 §35). No statement binds them to PD-08 | ACT-003 `§26` candidate Part C | Freeze §8 walls (Tool, Human-Authority) | none | **Reserved:** `FDP-P10-001`, Founder, conditional-blocking (P12 D2) | **Constructible around the binding.** Authority and ownership sections reserved; operation and performance unknown |
| **PD-09** | **Role only.** Quality owner properties (A5 ADVISE / INTERFACE, C8 §36); *"PD-09 — Evaluate Quality"* (C8 §18) | ACT-003 `§27` candidate Part C | Master Map state discipline; Freeze §8 | resident verification tooling, not bound | **Reserved:** `FDP-P10-002`, Founder | **Constructible around the binding.** Performance unknown (circularity) |
| **PD-10** | **Weak.** Boundary label and A6 owner row. **Two names in the frozen corpus itself** (see §3) | ACT-003 `§28` scope (no section list) | none | `tools/`, governance index, conformance suites: not bound | **Unknown.** No A5 row | **Constructible under the CPID.** Name-dependent sections reserved (`G-02`) |

## 2. What the classification determined (`§14`, `§15`)

**Known and source-backed.** Each division's identity, and its boundary
against PD-02.

**Ownership.**
- Prose ownership statements exist for PD-05, PD-06 and PD-07.
- For PD-08 and PD-09, only the owner **role** is defined.
- For PD-10, an owner row exists, but no statement names the division as that
  owner.

**Inherited.** The Part arrangement of PD-01. The adaptation rule itself is
frozen: PD-02 E4 says the framework may be inherited *"dengan domain
adaptation"*, and E3 says *"tanpa memaksakan metric PD-02"*.

**Reconstructible.**
- Capability *areas*. No Capability is created (`DM-6`).
- Candidate operating cycles.
- Candidate performance measures, without thresholds.

**Unknown.**
- PD-06's implementation scope;
- the security operating and performance model;
- PD-09's own evaluation;
- PD-10's authority and operation;
- the Part C structure of PD-06 and PD-10.

**Reserved.**
- The Security and Quality bindings (Founder);
- PD-10's name (Founder / Architect);
- the Part arrangement (`C6-A1`);
- internal units (`G-10`, `DM-8`);
- Capabilities (`DM-6`);
- deferred architecture and reserved concepts (`FRZ-10`, `FRZ-2`).

**Actually blocked.** Nothing, for **construction**. Each reserved matter
blocks only the content that depends on it (`§17`), and construction proceeds
around it.

**Canonicalization** is a separate step and is Founder-reserved (`§24`).

**Minimum Founder Decision test (`§15`).** Before escalation, each reserved
item was put through `§15`'s sequence. None can be settled by existing
canonical authority, the reference pattern, domain adaptation, bounded
reconstruction or delegated authority:
- the bindings are recorded as Founder-reserved (`FD-P10-005 §4`);
- the Part arrangement, internal units and Capabilities are
  non-delegable Domain Model or structural matters (Constitution `§3.2`;
  REG-CFV2-001 C-2 and C-3).

Construction proceeded while preserving each one, so **none needs a decision
for construction to proceed.**

## 3. Findings that the classification did not anticipate

Two surfaced during construction, and both are recorded in the volumes.

1. **Several candidate sections fall inside reserved architecture.**
   - ACT-003's PD-07 list: C3 Compute, C4 Storage, C5 Network, C6 Resource and
     C9 Reliability touch Freeze §10 (Deployment, Scaling, Database
     implementation, Networking, Observability implementation) or Freeze §2
     (Resource).
   - ACT-003's PD-08 list: C3 Identity & Access touches Identity and
     Authentication (Freeze §10) and Permission (Freeze §2); C6 Security
     Context touches Context (Freeze §2).
   - ACT-003's PD-05 list: C6 Runtime Context touches Context.

   Adopting those lists as written would have designed Architect-reserved
   architecture. This is the concrete reason v1.1 `§11` matters.

2. **PD-10's name divergence is inside the frozen corpus too.**
   - Frozen PD-02 says *Developer Enablement* in A4, A6 and B1, and *Developer
     Experience* in D7 §69.
   - `G-02` records the divergence as frozen corpus vs registry. A rule that
     "the frozen corpus governs" would not by itself settle the name.
   - This is recorded as evidence for `G-02`, not resolved.
