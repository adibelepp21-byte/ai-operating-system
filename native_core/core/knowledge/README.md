# Knowledge Subsystem (Native Core)

**Status:** Skeleton (Phase 3.310) — architecture-complete, **behavior-empty**. No business logic, persistence, storage, admission, retrieval, or versioning is implemented. Concrete behavior is built in later authorized phases; the concrete Version Model is Phase 3.311.

## Purpose

Knowledge is **durable, authoritative, versioned understanding**, entered **only** through governed promotion (Freeze INV-7/INV-8; knowledge_spec §1). It records the durable authoritative outcome of a human-authorized governed promotion of a Memory candidate. It holds **no authority of its own** — Governance decides; Knowledge records (Phase 3.289 §13).

## Boundaries

- **Owns:** its version records and their canonical-status derivation.
- **Consumes:** a Memory promotion candidate (sole content source) and a Governance promotion authorization (the gate).
- **Never:** approves, rejects, promotes, or authorizes; never reads Trace directly; never mutates Trace, Memory, or Governance; never self-admits; never bypasses `promotion_authorized` (Phase 3.308 B7/B8; INV-8; §6.2 invariant 2).

## Lifecycle

```
Candidate  →  Governed Review  →  Active  →  Superseded
```

- A rejected candidate is **not admitted** (a non-state; reject is absolute).
- A governed revision records a **new Active** version and derives the prior as **Superseded (retained forever, never deleted)** — INV-7.
- Versions are **immutable**; a change is a **new version**, never an in-place edit. Exactly **one Active** version per item at a time; canonical status is **derived** from the append-only sequence (Phase 3.306 D2).
- No other state exists (no Draft/Pending/Archive/Historical/Retired/Deprecated/Tombstone/Soft-Delete/Confidence/Trust-Score/Ranking).

## Ownership & Storage

Knowledge owns the version **data**; the **persistence facility** is provided by Infrastructure (Blueprint §14). Storage is **append-only, durable, retained forever**, in a **Knowledge-owned partition separate from Trace, Governance, and Memory** — backend-agnostic (no database/filesystem/serialization chosen; Phase 3.306 D3).

## Dependency Graph

```
Knowledge ──► Memory                 (candidate source)
Knowledge ──► Governance             (promotion authorization; read of the signal only)
Knowledge ──► Infrastructure storage (facility beneath it)
```

- Acyclic, strictly downward; **no reverse edge, no cycle, no lateral edge**.
- **No dependency** on Trace, Runtime, Agent, Workflow, Capability, Execution, Identity, or Authentication.
- Holds no external dependency (INV-12); authors no Trace (OQ-2).

> In the **skeleton phase** none of these permitted dependencies is imported yet — the package imports only its own intra-package contracts. The edges above are wired when behavior is implemented in later authorized phases.

## Reserved (future authorized phases)

Concrete Version Model (Phase 3.311); repository/storage/admission/retrieval behavior; version-identifier lexical form; storage backend; validity-condition catalogue; per-consumer read authorization and persistent provenance trust (Identity/Authentication); Knowledge Trust Scoring and Policy-as-Knowledge (deferred by the Domain Model).
