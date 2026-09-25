"""P13 — the Super Intelligence Ecosystem layer of AIOS.

*"P13 is the Super Intelligence Ecosystem layer of AIOS in which AIOS develops
the capability to understand its own relevant system state, evaluate that state
against defined criteria, reason over evidence, determine appropriate next
actions, and evolve its capabilities within explicit governance and authority
boundaries."* — `FDR-2 D01`. "Super Intelligence" is the program's name. It is
not a performance claim (`D02`).

Built under `P13-018` (`D-1`: Blueprint `§10` IN) to
`docs/architecture/p13/AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md`. There is one
component per link of the semantic chain (C-01):

| Link | Component | Module |
|---|---|---|
| OBSERVE / UNDERSTAND | `StateUnderstanding` | `state` |
| EVALUATE | `Evaluation` | `evaluation` |
| REASON | `Reasoning` | `reasoning` |
| DETERMINE / PROPOSE | `NextAction` | `next_action` (+ `catalog`) |
| AUTHORITY CHECK | `AuthorityGate` | `authority` |
| EXECUTE IF AUTHORIZED / VERIFY | `BoundedExecution` | `execution` |
| LEARN / EVOLVE | `Evolution` | `evolution` |
| RE-DISCOVER / exhaustion | `Frontier` | `frontier` |

`cycle` composes the components into one bounded cycle, and `evidence` records
it.

**Boundaries this package keeps.** It lives in the tools layer: `NATIVE CORE =
11`, and it changes nothing under `native_core/`. It imports nothing from
`consumers/`. It reads P1–P12 and changes none of them. It writes its evidence
only under `docs/operations/p13/`. It has no scheduler, thread or daemon, and
runs when it is run. It executes only what a recorded envelope permits:

* `P13-ENV-01`: evidence-only, initial, not maximum;
* `P13-ENV-02` (`FDR-3`): two transitions of the S-OPS proof object, made
  through that surface's own API. **Spent and retired** under `FDR-4`
  `FD-B` once the E13-05 proof completed, so it permits nothing now.

`CAPABILITY ≠ AUTHORITY`. Importing this package does nothing.
"""
