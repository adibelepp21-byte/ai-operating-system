"""
Runtime hosting composition root.

The supported path from a governed catalog artifact to a resolved host, as one
call:

    governed catalog artifact
            │  tools.runtime_catalog.host_declarations()
            ▼
    hosting-declaration records
            │  DefinitionCatalog.from_records()
            ▼
    DefinitionCatalog
            │  .resolve()
            ▼
    HostDeclaration

Before this module a caller had to know both halves and assemble them by hand.
Each half is deliberately blind to the other: `tools.runtime_catalog` imports
nothing from `native_core` (`ADR-0024`), and `native_core` imports nothing from
`tools` — the core stays independent of repository layout, and the Runtime
boundary's stdlib allowlist admits no parsing module anyway. Neither side can
therefore compose the path, and something above both must. This is that
caller — the one `agent/definition.py` twice describes as *"a caller that can
see both sides"* and which had not been built.

**Composition only.** Following the pattern `runtime/composition.py`,
`knowledge/composition.py`, `optimization/composition.py` and
`runtime/execution/composition.py` already establish, this module assembles
existing collaborators and adds no behaviour of its own. It decides nothing,
caches nothing, and holds no state: every call reads the catalog fresh, so a
catalog edited between calls is observed, never remembered (Blueprint §26).

**Errors stay separated by owner.** A representation failure raises
`CatalogReadError` from the reader; a meaning failure raises the Runtime
boundary's own `MalformedDeclaration`, `UndeclaredDefinition` or `UnknownHost`.
They are deliberately *not* collapsed into one type: which layer refused a
resolution is diagnostic information, and flattening it would hide the
ownership split `ADR-0021` established.

**Authority.** This composes reading. Whether a documented hosting reference is
authoritative input to execution, rather than descriptive documentation, remains
an open classification reserved to the Architect (`ADR-0024` §3). Assembling a
path confers no authority on what flows through it.
"""

from native_core.core.runtime.discovery import DefinitionCatalog, HostDeclaration

from .runtime_catalog import host_declarations


def create_definition_catalog(runtime_dir=None) -> "DefinitionCatalog":
    """Assemble a `DefinitionCatalog` from the governed Runtime catalog.

    Reads the catalog through the tool-level reader and hands the records to the
    Native Core, which applies its own Definition rules. Nothing is constructed
    here except the catalog itself; a malformed record is rejected by
    `DefinitionCatalog`, not by this function.
    """
    return DefinitionCatalog.from_records(host_declarations(runtime_dir))


def resolve_host(
    definition_name: str, selector=None, runtime_dir=None
) -> "HostDeclaration":
    """Resolve a Definition name to the governed host that declares it.

    The whole supported path in one call. Without a `selector` the first
    declaring host in `runtime_key` order is returned; with one, that host must
    exist and must itself declare the name. Every other outcome raises (PR-4).
    """
    return create_definition_catalog(runtime_dir).resolve(definition_name, selector)


if __name__ == "__main__":
    catalog = create_definition_catalog()
    for declaration in catalog.declarations:
        for name in declaration.definition_names:
            print(f"{name}  ->  {catalog.resolve(name).runtime_key}")
