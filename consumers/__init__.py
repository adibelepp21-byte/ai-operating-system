"""
AIOS Consumers — product/application consumer residency.

The fourth top-level region, authorized by `DEC-P6-042`. It exists for one
architectural reason: **concrete implementations of Native Core contracts must
live outside the contract boundaries they implement.**

`native_core/core/agent/` is a *contract* boundary, and its conformance suite
enforces that — a resident there may hold exactly one cross-boundary import, may
not name the Execution layer, may not name the hosting Runtime, and may not add
a raise site. Those constraints are not obstacles; they are what keeps a
contract boundary a contract boundary. Three core modules say the same thing in
the same words: implementations belong to *"future, separately authorized
consumer phases"* (`agent.py`, `consumer.py`, `execution/contract.py`). This
region is where such a phase resides.

**Dependency direction — the whole point of the region:**

```
consumers/            ──depends on──▶   native_core (public contracts)
native_core/          ──never──────▶    consumers/
```

The core must never learn that a consumer exists. Placing consumers here is what
makes that possible without weakening a single core assertion.

**What lives here:** concrete implementations of Native Core contracts —
today, `ExecutionConsumer` realizations.

**What does not:** anything belonging to the Native Core itself; repository
tooling, validators and catalog readers (those are `tools/`); documentation
(`docs/`); and anything with no core contract to implement. This region is not a
second core, not a replacement for `tools/`, and not a general holding area — a
module that implements no core contract does not belong here.

Ownership: a consumer owns only its own behaviour. It holds no governance
authority, authors no Trace, and grants itself nothing: being handed a bound
`Execution` is *"entry, not authority"* (`agent_execution_semantics_spec` §13.1).
"""

from .reference_agent import ReferenceAgent

__all__ = ["ReferenceAgent"]
