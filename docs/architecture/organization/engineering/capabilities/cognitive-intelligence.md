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

The [Cognitive Intelligence Agent](../agent-definitions/cognitive-intelligence-agent.md)
implements this Capability.

ADR-0008 recorded that this Capability began with zero implementers, and
noted that this was an expected, temporary condition following the
Capability's creation rather than an oversight — the condition Canonical
Domain Model §7 invariant 14 identifies as an invalid steady state
requiring governance review. That condition was closed by the creation of
the Agent Definition named above, as ordinary Department-discretion work
outside the scope of any ADR, exactly as ADR-0008 anticipated. This
section is updated to record that closure; the Capability's contract is
unchanged by it.

The Phase 5 realization is exercised by a resident consumer,
`consumers/cognitive_intelligence_agent.py`, which realizes task
decomposition and ordered planning only. That consumer is an
implementation of the Agent contract and holds no authority; it neither
extends this Capability's scope nor narrows it.
