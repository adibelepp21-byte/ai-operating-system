# Engineering Intelligence

This Capability was established by
[ADR-0008](../../../adr/decisions/ADR-0008.md), owned by the
[Engineering](../README.md) Department. This document records that
decision; it does not itself grant or define any authority.

## Name

Engineering Intelligence

## Owner

Engineering Department

## Definition

The ability to construct, change, verify, and safeguard AIOS's own
engineered artifacts, as a governed contract independent of the models,
tools, or techniques used to deliver it.

## Scope

This Capability covers seven sub-abilities, which together constitute its
long-term architecture:

1. Architecture
2. Coding
3. Testing
4. Security
5. Review
6. Refactoring
7. Documentation

**Phase 5 realization (intentionally limited).** Only two of the seven —
Coding and Testing — are realized in Phase 5. The remaining five
(Architecture, Security, Review, Refactoring, Documentation) are not
required for Phase 5 exit.

The Capability boundary is long-term architecture; the Phase 5
realization is a deliberate, bounded subset of it. The two are not the
same and neither redefines the other. Declaring the full seven-part scope
does not authorize building the other five, and realizing only two does
not narrow the Capability's contract.

This Capability does not cover governance-artifact maintenance, which
belongs to Platform under ADR-0003. It names no technology, language,
framework, model, vendor, or infrastructure; per Canonical Domain Model
§8, only Runtime and Tool may do so.

## Status

The [Engineering Intelligence Agent](../agent-definitions/engineering-intelligence-agent.md)
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
`consumers/engineering_intelligence_agent.py`, which realizes the Coding
and Testing sub-abilities only. The remaining five remain unrealized, as
recorded above. That consumer is an implementation of the Agent contract
and holds no authority; it neither extends this Capability's scope nor
narrows it.
