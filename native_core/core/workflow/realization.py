"""
Workflow realization — the Workflow-to-Capability relation (Domain Model §4;
Architecture Freeze §6; Blueprint §10; workflow_spec §7).

Canonical Domain Model §4 [E]: *"Workflow **realizes** Capability."* Architecture
Freeze §6 carries it in the frozen *Observed* relationship table:

    | Workflow realizes Capability | Workflow→Capability | Capability→Workflow
    (Blueprint §7 [E] admits only its Department and other Capabilities) |
    unchanged — Workflow central, Capability Dept-owned (INV-1) | governed |

`workflow_spec §7` [E], synchronized under `DEC-F03-047` S-1: *"Executed by
Runtime; composes Skills; **realizes Capabilities**."*

**Provenance.** The relationship was ratified by the Founder as T-2 ALT-3
(`DEC-F03-045 = OPTION C`), canonicalized under `DEC-F03-046` (C-1 Domain Model,
C-2 Freeze, C-3 Blueprint), specification-synchronized under `DEC-F03-047`, and
only then authorized for construction by `DEC-F03-048 = OPTION A`. **This module
is not the source of the architectural decision** — it is the last stage of it,
and it ratifies nothing.

**Direction is load-bearing.** The edge runs **Workflow → Capability** and the
converse does not hold: a Capability declares no Workflow. Blueprint §7 [E]
still admits only *"its Department; other Capabilities"* as the Capability
package's dependencies, so nothing here may be mirrored on that side.

**No Capability import.** Blueprint §10 admits the relation *"by reference only
… so the package takes no import of `core/capability/` and holds no Capability
state."* `CapabilityRef` therefore carries a key and nothing else, exactly as
`SkillRef` and `AgentDefinitionRef` already do in this package. A Capability's
identity, version lineage, ownership and dependency graph belong to
`core/capability/`, which this boundary does not import.

**Cardinality is not stated by any canonical source, and none is invented.**
Freeze §6, Domain Model §4 and `workflow_spec §7` fix the relationship and its
direction; not one of them fixes how many Capabilities a Workflow realizes.
`realizes` therefore imposes the weakest structural constraint available — a
possibly-empty set of distinct keys — because requiring a minimum would be
inventing an invariant this boundary has no authority to create. Where the
architecture *has* spoken on a comparable cardinality it said the same thing:
INV-15 [E], *"No minimum cardinality is required for either relationship."*
That is cited as posture, not as authority over this edge.

Deliberately ABSENT, because no canonical source establishes them here: the
**Skill** half of T-2 (`Capability↔Skill` remains **[O]** reserved — Freeze §10,
`capability_spec §12`/`§14`); Capability version binding (Domain Model §6 binds
an *Agent Definition's* version to the Capability contract it implements and says
nothing about Workflows); ownership (a Workflow is owned centrally and owns no
Capability — INV-1 gives a Capability exactly one Department); lifecycle states;
execution; Trace authorship (INV-4); and any query that would require reading
Capability state.

Dependencies: stdlib only, plus this package's own exceptions. No import of
`core/capability/`, `core/skill/`, `core/agent/`, `core/runtime/` or any other
boundary; no external dependency (INV-12).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from .exceptions import InvalidWorkflowRealization
from .models import WorkflowIdentity


@dataclass(frozen=True, order=True)
class CapabilityRef:
    """Reference to a Capability a Workflow realizes.

    A stub carrying only the reference the realization needs. It models no
    Capability contract, version lineage, ownership or dependency — those
    belong to `core/capability/`, and this boundary does not import it."""

    capability_key: str

    def __post_init__(self) -> None:
        if not isinstance(self.capability_key, str) or not self.capability_key.strip():
            raise InvalidWorkflowRealization(
                "capability_key must be a non-empty string"
            )


@dataclass(frozen=True)
class WorkflowRealization:
    """The Capabilities one Workflow realizes (Domain Model §4; Freeze §6).

    `realizes` may be empty. No canonical source states a cardinality for this
    edge, so none is imposed: an empty set is a valid structural state, not an
    incomplete one. Construction validates structure only — every entry must be
    a `CapabilityRef`, and no `capability_key` may repeat, since a repeated key
    makes the realized set ambiguous."""

    realized_by: WorkflowIdentity
    realizes: Tuple[CapabilityRef, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.realized_by, WorkflowIdentity):
            raise InvalidWorkflowRealization(
                "realized_by must be a WorkflowIdentity"
            )
        if not isinstance(self.realizes, tuple):
            raise InvalidWorkflowRealization("realizes must be a tuple")

        seen = set()
        for entry in self.realizes:
            if not isinstance(entry, CapabilityRef):
                raise InvalidWorkflowRealization(
                    "every realized capability must be a CapabilityRef"
                )
            if entry.capability_key in seen:
                raise InvalidWorkflowRealization(
                    "capability_key realized more than once: "
                    f"{entry.capability_key!r}"
                )
            seen.add(entry.capability_key)

    # -- queries ---------------------------------------------------------
    #
    # The minimum surface needed to realize and verify the relationship
    # (`ACT-CC-F03-048 §4`). Both answer from what this Workflow declares;
    # neither reads Capability state, and neither can, since no Capability is
    # visible from this boundary.

    def capability_keys(self) -> Tuple[str, ...]:
        """The Capability keys this Workflow declares it realizes, sorted."""
        return tuple(sorted(ref.capability_key for ref in self.realizes))

    def realizes_capability(self, capability_key: str) -> bool:
        """Whether this Workflow declares it realizes the named Capability.

        Answers only what was declared. Whether that Capability *exists* is a
        corpus fact this boundary cannot see — a caller holding both sides
        reconciles it, exactly as INV-2's implementer edge is reconciled."""
        return capability_key in {ref.capability_key for ref in self.realizes}
