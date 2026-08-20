"""
Capability dependency graph — the governed, queryable dependency model
(Blueprint §7 Capability Package; capability_spec §2/§6/§10/§11; Freeze
INV-9/INV-10/INV-11/INV-14).

Realizes the deliverable Roadmap §9.6 names: *"governed capability model"*,
with completion measured by *"INV-1/9/10/11/14 tests pass."*

What this module enforces, each traced to its invariant:

  - **INV-9** — every declared dependency is explicit and references a
    specific versioned contract. Enforced structurally by
    `CapabilityDependency` and re-checked here for target resolvability.
  - **INV-10** — a dependency crossing Department ownership must carry a
    governance record. Absent one, construction fails closed (PR-4;
    capability_spec §11). This boundary asserts *presence*, never authority
    (PR-3).
  - **INV-11** — the full dependency graph remains queryable and observable:
    every target resolves within the graph, and both directions are
    inspectable. A dependency naming a Capability outside the graph is an
    undocumented dependency and fails closed.
  - **INV-14** — a Capability with zero active Agent Definitions implementing
    it is *flagged*, not rejected. Domain Model §7 invariant 14 [E]: *"an
    invalid steady state and must be flagged for governance review."*
    capability_spec §10 [E]: *"Orphan capabilities are flagged."*
    `orphan_capabilities()` returns them. It raises nothing and decides
    nothing — Detect Don't Decide (PR-3).

Implementer counts are **supplied by the caller**, never stored on a
Capability. Domain Model §4 places the edge on *Agent Definition implements
Capability*, and capability_spec §7 restricts this boundary's dependencies to
its Department and other Capabilities — Agent is not among them. Reading
implementers from an argument keeps INV-14 detectable without creating a
`capability → agent` dependency.

Deliberately ABSENT: no execution of any kind (capability_spec §5/§8; Freeze
§4), no Skill or Workflow composition (Freeze §10 Inferred; Blueprint §7
reserved; capability_spec §12), no persistence, no registry, no mutation, no
Trace authorship (capability_spec §9), no external dependency (INV-12).

Dependencies: stdlib only, plus this package's own models and exceptions.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Iterable, Mapping, Tuple

from .exceptions import (
    InvalidCapability,
    UndocumentedCapabilityDependency,
    UngovernedCrossDepartmentDependency,
)
from .models import Capability, CapabilityIdentity


class CapabilityGraph:
    """An immutable, queryable graph of Capabilities and their dependencies.

    Construction validates INV-9, INV-10 and INV-11 and fails closed on any
    violation. INV-14 is a query, not a construction rule."""

    __slots__ = ("_capabilities", "_dependents")

    def __init__(self, capabilities: Iterable[Capability]) -> None:
        indexed = {}
        for capability in capabilities:
            if not isinstance(capability, Capability):
                raise InvalidCapability(
                    "every member of the graph must be a Capability"
                )
            key = capability.identity.capability_key
            if key in indexed:
                raise InvalidCapability(
                    f"duplicate capability_key in graph: {key!r}"
                )
            indexed[key] = capability

        dependents: dict = {key: [] for key in indexed}

        for capability in indexed.values():
            owner = capability.owning_department.department_key
            for dependency in capability.dependencies:
                target_key = dependency.depends_on.capability_key

                # INV-11 — no undocumented dependency.
                target = indexed.get(target_key)
                if target is None:
                    raise UndocumentedCapabilityDependency(
                        f"{capability.identity.capability_key!r} declares a "
                        f"dependency on {target_key!r}, which is not present "
                        "in the graph (INV-11: no undocumented dependencies)"
                    )

                # INV-9 — the declared contract version must be the one the
                # target actually offers; otherwise the reference is not to a
                # specific versioned contract.
                if (
                    dependency.depends_on.capability_version
                    != target.identity.capability_version
                ):
                    raise UndocumentedCapabilityDependency(
                        f"{capability.identity.capability_key!r} references "
                        f"{target_key!r} at version "
                        f"{dependency.depends_on.capability_version!r}, but the "
                        f"graph holds version "
                        f"{target.identity.capability_version!r} "
                        "(INV-9: a specific versioned contract)"
                    )

                # INV-10 — cross-Department dependency requires a governance
                # record. Presence is asserted; authority is never evaluated.
                if target.owning_department.department_key != owner:
                    if dependency.governance is None:
                        raise UngovernedCrossDepartmentDependency(
                            f"{capability.identity.capability_key!r} "
                            f"(department {owner!r}) depends on "
                            f"{target_key!r} (department "
                            f"{target.owning_department.department_key!r}) "
                            "without a governance record (INV-10: never "
                            "silent adoption)"
                        )

                dependents[target_key].append(capability.identity)

        self._capabilities = MappingProxyType(dict(indexed))
        self._dependents = MappingProxyType(
            {key: tuple(value) for key, value in dependents.items()}
        )

    # -- INV-11: queryable and observable -------------------------------

    def capabilities(self) -> Mapping[str, Capability]:
        """Every Capability in the graph, keyed by `capability_key`."""
        return self._capabilities

    def capability(self, capability_key: str) -> Capability:
        """The Capability for `capability_key`, or raise if absent."""
        try:
            return self._capabilities[capability_key]
        except KeyError:
            raise InvalidCapability(
                f"no capability named {capability_key!r} in the graph"
            ) from None

    def dependencies_of(self, capability_key: str) -> Tuple[CapabilityIdentity, ...]:
        """The versioned contracts `capability_key` depends on (INV-9/11)."""
        return tuple(
            dependency.depends_on
            for dependency in self.capability(capability_key).dependencies
        )

    def dependents_of(self, capability_key: str) -> Tuple[CapabilityIdentity, ...]:
        """The Capabilities that depend on `capability_key` (INV-11).

        The reverse direction is part of what makes the graph *observable*,
        not merely queryable."""
        self.capability(capability_key)
        return self._dependents[capability_key]

    def cross_department_dependencies(
        self,
    ) -> Tuple[Tuple[CapabilityIdentity, CapabilityIdentity], ...]:
        """Every dependency edge that crosses Department ownership (INV-10).

        Each is governed by construction; this exposes them for review."""
        edges = []
        for capability in self._capabilities.values():
            owner = capability.owning_department.department_key
            for dependency in capability.dependencies:
                target = self._capabilities[dependency.depends_on.capability_key]
                if target.owning_department.department_key != owner:
                    edges.append((capability.identity, target.identity))
        return tuple(edges)

    # -- INV-14: flag, never decide -------------------------------------

    # -- INV-2 clause 2: the Agent Definition side of the implementer edge --
    #
    # Declarations arrive as `(agent_definition_key, implemented_capability_keys)`
    # plain-key pairs, never Agent Definition objects. INV-2 clause 2 is a
    # per-Definition fact and the Definition contract enforces it there; what
    # this boundary adds is the *corpus* view, which no single Definition can
    # see. Keys rather than objects keep the module's stated dependency rule
    # intact: Agent is not among this boundary's permitted dependencies, and
    # `capability → agent` must not exist. Added under `ACT-CC-F03-040`.

    def implementer_counts(
        self, declarations: Iterable[Tuple[str, Iterable[str]]]
    ) -> Mapping[str, int]:
        """Count implementing Agent Definitions per Capability key.

        The mapping `orphan_capabilities` already expects, derived from what
        Definitions declare rather than assembled by hand. Counts *distinct*
        Definitions: one Definition contributes at most one to a Capability,
        so a Definition cannot make a Capability look implemented twice.

        Keys the graph does not contain are counted too — deciding what an
        unknown key means belongs to `unknown_implemented_capabilities`, not
        here."""
        counts = {}
        for definition_key, capability_keys in declarations:
            for capability_key in set(capability_keys):
                counts[capability_key] = counts.get(capability_key, 0) + 1
        return MappingProxyType(counts)

    def implementers_of(
        self,
        capability_key: str,
        declarations: Iterable[Tuple[str, Iterable[str]]],
    ) -> Tuple[str, ...]:
        """The Agent Definition keys declaring they implement a Capability."""
        return tuple(
            sorted(
                {
                    definition_key
                    for definition_key, capability_keys in declarations
                    if capability_key in set(capability_keys)
                }
            )
        )

    def unknown_implemented_capabilities(
        self, declarations: Iterable[Tuple[str, Iterable[str]]]
    ) -> Tuple[Tuple[str, str], ...]:
        """Declarations naming a Capability this graph does not contain.

        Each entry is `(agent_definition_key, capability_key)`. Reported, never
        raised (PR-3): over a partial corpus a Capability absent from *this*
        graph is ordinary incompleteness rather than a violation, and INV-2
        clause 2 — *"implements at least one Capability"* — is enforced on the
        Definition itself, which is where the invariant is stated. Whether an
        unresolvable declaration is a defect is a governance judgement, and
        this boundary does not make it."""
        return tuple(
            sorted(
                (definition_key, capability_key)
                for definition_key, capability_keys in declarations
                for capability_key in set(capability_keys)
                if capability_key not in self._capabilities
            )
        )

    def orphan_capabilities(
        self, implementer_counts: Mapping[str, int]
    ) -> Tuple[CapabilityIdentity, ...]:
        """Capabilities with zero active Agent Definitions implementing them.

        Returned as a governance flag, never raised — INV-14 [E]: *"an invalid
        steady state and must be flagged for governance review."* Detect Don't
        Decide (PR-3): this boundary reports the condition and takes no action
        on it.

        `implementer_counts` is supplied by the caller so that no
        `capability → agent` dependency is created. A Capability absent from
        the mapping counts as zero."""
        flagged = [
            capability.identity
            for key, capability in self._capabilities.items()
            if int(implementer_counts.get(key, 0)) <= 0
        ]
        return tuple(flagged)
