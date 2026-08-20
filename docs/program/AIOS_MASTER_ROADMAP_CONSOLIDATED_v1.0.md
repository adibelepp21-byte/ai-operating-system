# AIOS Master Roadmap — Consolidated

> **Status per its own §42: `CONSOLIDATED MASTER ROADMAP — DECISION/IMPLEMENTATION
> REFERENCE`. NOT `CANONICAL MASTER ROADMAP v2.0`.** It consolidates existing
> project sources; it does not convert them into governance decisions. Elements
> its own §39 marks **PROPOSED** remain proposed.

**Supplied by:** Founder, 2026-08-20 · **Recorded by:** Claude Code / Co-Founder
**Authority:** follows the status of each underlying source
**Resolves:** the target-selection block reported at `ACT-CC-F03-030` (F-05 — no resident Master Roadmap)

---

## 1. Precedence

Per `ACT-CC-F03-030 §6`, this artifact sits **below** the Constitution, canonical
architecture, canonical governance and Founder Decisions. Where it and a resident
canonical record disagree, **the canonical record governs** and the divergence is
recorded rather than reconciled silently. Two such divergences are recorded in
`AIOS_CONSTRUCTION_POSITION_v1.0.md §2`.

## 2. Structure

Four dimensions read together, not four separate roadmaps:

```text
                     AIOS MASTER ROADMAP
                              │
        ┌─────────────────────┼─────────────────────┐
     PHASES 0→13         PLATFORMS PD-01→PD-10    WAVES
        └─────────────────────┼─────────────────────┘
                        CONSTRUCTION
                Architecture → Build → Verify
```

**Phase** = which system capability is built · **Platform** = which organization
owns the domain capability · **Wave** = which external intelligence is needed and
when · **Construction** = how the work is realised and validated.

## 3. Non-skippable principle

```text
Dependency → Implementation → Verification → Exit Criteria → Phase Eligible
```

A Phase may not begin because the previous one *looks* sufficient.

## 4. Phases 0–13

| # | Name | Objective | Dependency | Exit |
|---|---|---|---|---|
| 0 | Vision & Constitution | vision, constitution, principles, constraints | — | Vision + Constitution |
| 1 | Core Architecture | canonical architecture | P0 | Architecture baseline |
| 2 | Runtime Foundation | runtime / Native Core | P1 | Runtime foundation stable |
| 3 | Execution Contracts | execution contract layer | P2 | Contract + Workflow + Skill + Planner + Scheduler + Execution Orchestrator stable |
| 4 | AI Runtime | run agents directly | P2 + P3 | Agent end-to-end |
| 5 | Intelligence Ecosystem | intelligence capabilities | P4 | Intelligence executable |
| 6 | Knowledge Ecosystem | retrieval / reasoning | P4 + P5 | Knowledge integrated |
| 7 | Memory Ecosystem | agent memory | P4 | Memory integrated |
| 8 | Tool Ecosystem | tool integration | P4 + Governance | Tool execution governed |
| 9 | Workflow Ecosystem | composition layer | P5–P8 | Multi-capability workflow |
| 10 | Department Ecosystem | agents → Departments | P9 | Department operational |
| 11 | Autonomous Organization | cross-department autonomy | P10 | Routine ops without per-task instruction |
| 12 | AI Operating System | full layer integration | P4–P11 | All layers as one system |
| 13 | Super Intelligence | post-AIOS evolution | P12 | **UNDEFINED BY DESIGN** |

**Era 2 (Master Program, Volumes I–VIII) runs in parallel and is not a technical
Phase.** Volume I complete; II in progress; III–VIII pending.

## 5. Platform registry

`PD-01` Executive · `PD-02` Architecture · `PD-03` Governance & Compliance ·
`PD-04` Knowledge & Intelligence · `PD-05` Runtime & Execution · `PD-06` AI
Engineering · `PD-07` Infrastructure & Platform · `PD-08` Security · `PD-09`
Quality & Evaluation · `PD-10` Developer Experience.

**CPIDs are permanent and never reused.** `PD-01` is the Gold Standard Reference
Implementation; `PD-02`–`PD-10` follow by **domain adaptation, not content copy**.
Numeric order is not full technical dependency, and dependency is **not**
subordination — PD-02 is not a parent owner of other platforms.

## 6. Repository waves

Foundation P1–4 · Intelligence P5–6 · Coding P5+ · Quant after P5 · **Scientific
unscheduled (no real capability need yet)** · Media after P9 · Production P2+
continuous. Waves activate on need, not calendar.

## 7. Construction priority engine

```text
Candidate Target → Phase dep? · Platform dep? · Capability dep? · Governance block?
                 · Evidence? · Architecture stable? · Implementation ready? · MVP value?
                 → Priority Assessment
```

**Priority 1** unblock critical dependency · **2** required foundation · **3**
critical MVP path · **4** reference implementation reuse · **5** domain expansion.

**Construction gate G1–G7:** in roadmap · dependencies met · architecture source
available · authority available · evidence sufficient · verification method
available · real downstream value. All → ELIGIBLE; some → CONDITIONALLY ELIGIBLE;
hard dependency → BLOCKED.

## 8. Open gaps carried forward (roadmap §39)

| ID | Gap |
|---|---|
| GAP-01 | Phase 3 exact percentage — the ±75% is a 2026-07-26 snapshot; recompute from repository evidence. **Done — see `AIOS_CONSTRUCTION_POSITION_v1.0.md`** |
| GAP-02 | Phase 5–13 detailed exit metrics remain at principle level |
| GAP-03 | Phase 13 scope intentionally open |
| GAP-04 | Department priority (Engineering → Finance → Research → Content → Marketing → Executive Office) **PROPOSED**, needs program-owner confirmation |
| GAP-05 | This artifact is a consolidation, not a canonical governance decision |

**Personal Finance AIOS MVP path (Engineering → Finance → Research) is likewise
PROPOSED**, not a new Founder decision.

## 9. What this artifact does not do

It does not clear PD-02's governance debt. `DEC-REVOCATION`, `DEC-AE04`,
`DEC-ADOPTION` and `OB-01` remain on their own governance tracks. It removes only
their incidental effect of blocking *unrelated* subsystem construction.
