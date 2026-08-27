"""
Runtime-side Agent Definition discovery (Roadmap §7/§8; runtime_spec §2/§5/§6).

Runtime's canonical responsibility is to *bind Definition→Instance*
(`runtime_spec §6`) and to expose *"host/instantiate an Agent Definition"*
(`runtime_spec §5`). Freeze §5 layer 2 lists `Agent` among Runtime's
dependencies, while Blueprint §21 prohibits a cyclic import between core
boundaries. Roadmap §7 reconciles the two by naming this exact pair:

    "Agent↔Runtime mutual reference is resolved by building Runtime as a
     facility that discovers Agent Definitions dynamically ... so Runtime need
     not statically know concrete definitions at construction; it hosts
     whatever Agent Definitions exist. This keeps the graph acyclic in code."

Roadmap §8 writes the same asymmetry into the frozen build-time graph:
`Runtime → Agent Definition (dynamically)`. **Dynamic means dynamic in time,
not dynamic in Python.** `ADR-0019` established empirically that the mechanism
is data discovery: a Definition arrives here as a **name**, and resolution
reads governed **data**. Nothing in this module imports the Agent boundary,
and nothing loads a Python module — the acyclic graph is preserved by
construction, not by convention.

What this module does: resolve a Definition name to the declared Runtime host
that may host it, deterministically, failing closed when nothing declares it.

Deliberately ABSENT — this is discovery, not construction. There is no Agent
Definition type, no Instance, no governed construction, no capability binding,
no lifecycle, no mutable collection of live actors, and no authority. Governed
construction of Definitions/Instances is the **Agent Factory**, which
`agent_spec §12/§13` places in Phase 4 and reserves to the Architect; this
module deliberately stops short of it.

Ownership: Runtime owns hosting (`runtime_spec §3` — transient hosting/binding
state, owned centrally). A `HostDeclaration` names a host and the Definition
names it declares it may host; it holds no Agent-owned data and confers no
authority (§6.2 invariant 2).

Dependencies: this boundary's own exception taxonomy, and stdlib typing only.
Declarations arrive **already decoded**: Infrastructure owns I/O and encoding
(Blueprint §14), Runtime owns interpretation and resolution. The Runtime
boundary's stdlib allowlist admits no serialization module, and that is the
architecture speaking rather than an obstacle — a boundary that decodes bytes
has taken on a facility's work. It imports nothing from Agent, Workflow,
Skill, Capability, Trace, Memory, Governance or Optimization. No reflection,
no dynamic import, no module-level state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Optional, Sequence, Tuple

from .exceptions import RuntimeSubsystemError


class UndeclaredDefinition(RuntimeSubsystemError):
    """No declared host may host a Definition of that name (PR-4).

    Fail closed: an unknown or undeclared name never resolves to an arbitrary
    host. Silence is not a default host.
    """


class UnknownHost(RuntimeSubsystemError):
    """A selector named a host that does not exist in the catalog (PR-4)."""


class MalformedDeclaration(RuntimeSubsystemError):
    """A declaration could not be read accountably (PR-4).

    An incomplete or ill-typed declaration is never coerced into a valid one.
    """


@dataclass(frozen=True)
class HostDeclaration:
    """One declared Runtime host, and the Definition names it may host.

    Immutable and comparable by value. `runtime_key` is the host's canonical
    key; `definition_names` are the Agent Definition names this host declares
    it may host — **names only**, never Agent-owned structure. Recording the
    existence of the relationship is the whole of it (Domain Model §4,
    Runtime-hosts-Agent-Instance).
    """

    runtime_key: str
    definition_names: Tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.runtime_key, str) or not self.runtime_key.strip():
            raise MalformedDeclaration("runtime_key must be a non-empty string")
        if not isinstance(self.definition_names, tuple):
            raise MalformedDeclaration("definition_names must be a tuple")
        for name in self.definition_names:
            if not isinstance(name, str) or not name.strip():
                raise MalformedDeclaration(
                    "every declared Definition name must be a non-empty string"
                )
        if len(set(self.definition_names)) != len(self.definition_names):
            raise MalformedDeclaration(
                f"{self.runtime_key} declares a duplicate Definition name"
            )

    def declares(self, definition_name: str) -> bool:
        """Whether this host declares it may host that Definition name."""
        return definition_name in self.definition_names


class DefinitionCatalog:
    """Governed host declarations, resolvable by Definition name.

    Immutable once constructed and ordered by `runtime_key`, so resolution over
    equivalent catalog state is deterministic and reproducible. Construction is
    by injection: the catalog is given its declarations, it discovers nothing
    by itself and reaches no facility on its own initiative.
    """

    def __init__(self, declarations: Sequence["HostDeclaration"]) -> None:
        for declaration in declarations:
            if not isinstance(declaration, HostDeclaration):
                raise MalformedDeclaration(
                    "a catalog holds HostDeclaration values only"
                )
        keys = [declaration.runtime_key for declaration in declarations]
        if len(set(keys)) != len(keys):
            raise MalformedDeclaration("a runtime_key appears twice in the catalog")
        self._declarations: Tuple[HostDeclaration, ...] = tuple(
            sorted(declarations, key=lambda declaration: declaration.runtime_key)
        )

    @property
    def declarations(self) -> Tuple["HostDeclaration", ...]:
        """The declarations, in deterministic `runtime_key` order."""
        return self._declarations

    def resolve(
        self, definition_name: str, selector: Optional[str] = None
    ) -> "HostDeclaration":
        """Resolve a Definition name to the host that may host it.

        Without a `selector`, the first declaring host in `runtime_key` order is
        returned — a stated deterministic default, not incidental first-match.
        With a `selector`, that host must exist and must itself declare the
        name. Every other outcome raises (PR-4): nothing here degrades to an
        arbitrary host.
        """
        if not isinstance(definition_name, str) or not definition_name.strip():
            raise UndeclaredDefinition(
                "a Definition name must be a non-empty string"
            )

        if selector is not None:
            for declaration in self._declarations:
                if declaration.runtime_key == selector:
                    if not declaration.declares(definition_name):
                        raise UndeclaredDefinition(
                            f"{selector} does not declare it may host a Definition "
                            f"of {definition_name!r}"
                        )
                    return declaration
            raise UnknownHost(f"no declared host with runtime_key {selector!r}")

        for declaration in self._declarations:
            if declaration.declares(definition_name):
                return declaration
        raise UndeclaredDefinition(
            f"no declared host may host a Definition of {definition_name!r}"
        )

    @classmethod
    def from_records(
        cls, records: Iterable[Mapping[str, object]]
    ) -> "DefinitionCatalog":
        """Build a catalog from decoded declaration mappings.

        Each mapping carries `runtime_key` and `definition_names`. A mapping
        missing either, or carrying an unexpected shape, raises rather than
        being silently skipped — a partially-read catalog would resolve
        accountably-looking answers from incomplete data.
        """
        declarations = []
        for record in records:
            if not isinstance(record, Mapping):
                raise MalformedDeclaration("a declaration must be a mapping")
            if "runtime_key" not in record or "definition_names" not in record:
                raise MalformedDeclaration(
                    "a declaration needs 'runtime_key' and 'definition_names'"
                )
            names = record["definition_names"]
            if not isinstance(names, (list, tuple)):
                raise MalformedDeclaration("'definition_names' must be a sequence")
            declarations.append(
                HostDeclaration(
                    runtime_key=record["runtime_key"],
                    definition_names=tuple(names),
                )
            )
        return cls(declarations)
