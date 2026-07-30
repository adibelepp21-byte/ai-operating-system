# Cognitive Intelligence

This Capability was established by
[ADR-0008](../../../adr/decisions/ADR-0008.md), owned by the
[Engineering](../README.md) Department. This document records that
decision; it does not itself grant or define any authority.

## Name

Cognitive Intelligence

## Owner

Engineering Department

## Definition

The ability to reason about, decompose, sequence, and review work before
and after it is performed, as a governed contract independent of the
models or techniques used to deliver it.

## Scope

This Capability covers three sub-abilities, which together constitute its
long-term architecture:

1. Reasoning
2. Planning
3. Reflection

**Phase 5 realization (intentionally limited).** Only two elements are
realized in Phase 5:

- task decomposition
- ordered planning

Reasoning and Reflection, beyond what decomposition and ordering require,
are not realized in Phase 5.

As with Engineering Intelligence, the Capability boundary is long-term
architecture and the Phase 5 realization is a deliberate, bounded subset
of it.

This Capability does not execute anything; a Capability must not execute
itself. It names no technology, language, framework, model, vendor, or
infrastructure; per Canonical Domain Model §8, only Runtime and Tool may
do so.

## Status

No Agent Definition currently implements this Capability. Per ADR-0008,
this is an expected, temporary condition following the Capability's
creation, not an oversight — it is the condition Canonical Domain Model
§7 invariant 14 identifies as an invalid steady state requiring
governance review, and it is flagged here rather than left to be
discovered later. Creating Agent Definitions is ordinary
Department-discretion work outside the scope of any ADR.
