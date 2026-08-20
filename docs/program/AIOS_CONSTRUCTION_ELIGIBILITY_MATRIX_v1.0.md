# AIOS Construction Eligibility Matrix

**Prepared under:** FOUNDER · `ACT-CC-F03-031 §9`, `§12.4` · **Date:** 2026-08-20
**Empirical baseline:** full suite **495 tests, OK** (1 declared expected failure)

---

## 1. Capability construction eligibility (`§9`)

Verification of `native_core/core/capability/` against every condition `§9` names:

| Condition | Result | Evidence |
|---|---|---|
| Canonical architecture | **SATISFIED** | Capability is a ratified entity — Freeze **21** refs, Domain Model **26** |
| Capability specification | **SATISFIED** | `docs/engineering/capability/capability_spec.md`, 14 sections |
| Domain Model | **SATISFIED** | Capability on the Spine; INV-1/9/10/11/14 apply |
| Ownership rules | **SATISFIED** | INV-1 modelled — `DepartmentRef`, `CapabilityIdentity` |
| Dependency rules | **SATISFIED** | INV-9/10/11 modelled — `CapabilityDependency`, `GovernanceRecord`, `CapabilityGraph` |
| Existing implementation | **SATISFIED** | 517 lines across `models.py`, `graph.py`, `exceptions.py`, `__init__.py` |
| Test surface | **SATISFIED** | `test_capability_conformance.py`; INV-1/9/10/11/14 each covered |
| Roadmap priority | **SATISFIED** | Phase 5 track, Priority 1 |

### `CAPABILITY CONSTRUCTION — ELIGIBLE`

**All eight conditions are satisfied, and no architectural invention was used to
reach that result.**

## 2. The finding that follows — the eligible surface is already built

`NCIR §9.6` fixes this boundary's completion criterion as *"INV-1/9/10/11/14
tests pass."* **They pass.** The Capability subsystem is therefore **complete
against its own defined completion criterion.**

Everything beyond that point is reserved by the Capability specification itself:

| Beyond-current work | Status |
|---|---|
| Department Architecture realizing Organization/Department/Capability ownership | **[O] reserved to the Architect** (`capability_spec §13`) |
| Capability↔Skill/Workflow composition | **[O] Inferred, reserved** (`§12`) |
| Versioned-contract representation | **[O] reserved, no format defined** (`§14`) |
| Instantiating Capability Catalog categories | requires Department Architecture (INV-1 needs a Department owner) |

**Capability is eligible *and* complete.** There is no gap to fill inside the
authorized surface — not a block, a completed boundary.

## 3. Native Core — completion criteria across all subsystems

Every `NCIR §9` completion criterion is invariant-test-based, and all pass:

| Subsystem | Completion criterion | Met |
|---|---|---|
| Infrastructure | INV-12; facilities author no Trace (OQ-2) | ✓ |
| Trace | INV-4/5/6 | ✓ |
| Memory | INV-5/7/8; no promotion path | ✓ |
| Governance | no automatic promotion | ✓ |
| Knowledge | no unguided write path; INV-8 | ✓ |
| **Capability** | **INV-1/9/10/11/14** | **✓** |
| Skill | INV-12/15 | ✓ |
| Workflow | INV-13/4 | ✓ |
| Agent | INV-2/3/4/13/15 | ✓ |
| Runtime | INV-3/4; no Knowledge ownership | ✓ |
| Optimization | PR-3 upheld; no decision path under test | ✓ |

**11 of 11 subsystems complete. 495 tests OK.**

## 4. Eligibility across candidate targets

| Target | Eligibility | Reason |
|---|---|---|
| **Capability** | **ELIGIBLE — and COMPLETE** | all eight `§9` conditions met; completion criterion met |
| Other 10 native_core subsystems | ELIGIBLE — and COMPLETE | completion criteria met |
| Planner | **NOT ELIGIBLE** | no architectural surface anywhere in `docs/` |
| Scheduler | **NOT ELIGIBLE** | `[O]`-reserved (`NCIR §9.10`) |
| Execution Orchestrator | **NOT ELIGIBLE** | `[O]`-reserved; forward-dependent (`GDR-0002`) |
| Capability Catalog category instantiation | **BLOCKED BY ARCHITECTURE** | needs Department Architecture, `[O]`-reserved |
| Intelligence as an entity | **BLOCKED BY ARCHITECTURE** | not ratified; `§18` Founder-reserved |
| PD-02 activation-dependent work | **BLOCKED BY GOVERNANCE** | `DEC-REVOCATION`, `DEC-AE04`, `DEC-ADOPTION`, `OB-01` |

## 5. Conclusion

**The Native Core is complete against the frozen architecture.** The frozen
architecture stops where Phase 4 stops, deliberately. No construction target
inside the ratified surface has outstanding work, and every target outside it is
`[O]`-reserved pending ratification.

This is **`BLOCKED BY ARCHITECTURE`** in the `ACT-CC-F03-031 §17` sense — an
authority boundary, reached after the engineering was verified complete, not an
engineering shortfall.
