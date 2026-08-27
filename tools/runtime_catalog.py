"""
Runtime hosting-declaration reader.

Surfaces, as structured records, the hosting relationship that Runtime catalog
entries already document: which Agent Definitions each governed Runtime declares
it may host. Output is shaped for `DefinitionCatalog.from_records` so the
Native Core can resolve a host without this module knowing anything about the
Native Core — it returns plain mappings and imports nothing from `native_core`.

**Why this reads links.** Runtime Framework §9 defines `Hosts Agent Instance`
as a documentation field recording the relationship *"by reference only"*; no
structured field carries the Definition identity. This module therefore reuses
the extraction rule this repository already established and ships:
`link_classifier.py` classifies a link whose target lies under
`agent-definitions/` as an `agent-definition-reference`, and
`agent_integration.py` states the same assumption in terms — *"a catalog
artifact 'declares' a given Agent Definition as its invoker if it links to that
Agent Definition's file"* — while recording that *"no structured field
distinguishes intent from incidental citation yet."* That limitation is the
repository's known, documented state, not a new one introduced here.

**Two deliberate narrowings** over the existing reverse-direction heuristic,
both reducing its documented medium false-positive risk:

1. Only links inside the ratified `## Hosted Relationship` section are read.
   Runtime Framework §8 makes that section mandatory and places the
   `Hosts Agent Instance` field in it, so the section boundary is itself
   ratified structure rather than a guess. A citation elsewhere in the document
   — an ADR reference, a Domain Model pointer — cannot be mistaken for a
   hosting declaration.
2. A Definition is identified by the `**Name:**` its own Metadata declares, not
   by the link's display text. Identity comes from the Definition document,
   which owns it.

**Authority.** This module reports what the governed documents record. Whether a
documented hosting reference is *authoritative input to execution* — as opposed
to descriptive documentation — is an open classification reserved to the
Architect, and nothing here decides it. Reading a value confers no authority on
it (`ADR-0022`).

Fail closed (PR-4): an entry whose canonical key is missing, whose hosting link
does not resolve, or whose target Definition declares no Name raises. A silently
skipped entry would yield a catalog that answers confidently from partial data.
"""

import re
from pathlib import Path

from .validators.catalog import (
    CATALOG_ROOT,
    extract_canonical_key,
    extract_md_links,
    read_text,
    rel,
)

#: The ratified section carrying the `Hosts Agent Instance` field
#: (Runtime Framework §8/§9).
HOSTED_SECTION = "## Hosted Relationship"

#: An Agent Definition's own documentation-level identifier, per the
#: Agent Definition Framework's Metadata block.
NAME_RE = re.compile(r"^-\s+\*\*Name:\*\*\s*(.+?)\s*$", re.MULTILINE)

RUNTIME_DIR = CATALOG_ROOT / "runtime"


class CatalogReadError(RuntimeError):
    """A governed catalog entry could not be read accountably (PR-4)."""


def _section(text, heading):
    """The body of one `##` section, exclusive of the next `##` heading."""
    start = text.find(heading)
    if start == -1:
        return ""
    after = start + len(heading)
    nxt = text.find("\n## ", after)
    return text[after:] if nxt == -1 else text[after:nxt]


def _is_agent_definition_link(target):
    """The rule `link_classifier.py` already applies for this category."""
    parts = Path(target).parts
    if "agent-definitions" not in parts:
        return False
    name = Path(target).name
    return not (name.endswith("-framework.md") or name == "agent-definitions.md")


def _definition_name(entry_path, target):
    resolved = (entry_path.parent / target).resolve()
    if not resolved.is_file():
        raise CatalogReadError(
            f"{rel(entry_path)} declares a hosting reference to {target!r}, "
            "which does not resolve to a file"
        )
    match = NAME_RE.search(read_text(resolved))
    if not match:
        raise CatalogReadError(
            f"{rel(resolved)} declares no **Name:** and cannot identify a Definition"
        )
    return match.group(1)


def host_declarations(runtime_dir=None):
    """Read every governed Runtime entry as a hosting-declaration record.

    Returns a list of `{"runtime_key": str, "definition_names": [str, ...]}`,
    ordered by `runtime_key` so repeated reads of the same catalog agree.
    Entries declaring no Agent Definition are included with an empty list: the
    entry exists and declares nothing, which is different from absent.
    """
    directory = Path(runtime_dir) if runtime_dir is not None else RUNTIME_DIR
    if not directory.is_dir():
        raise CatalogReadError(f"no Runtime catalog directory at {directory}")

    records = []
    for path in sorted(directory.glob("*.md")):
        text = read_text(path)
        key = extract_canonical_key(text)
        if not key:
            raise CatalogReadError(f"{rel(path)} declares no **Canonical Key:**")
        names = []
        for target in extract_md_links(_section(text, HOSTED_SECTION)):
            if not _is_agent_definition_link(target):
                continue
            name = _definition_name(path, target)
            if name not in names:
                names.append(name)
        records.append({"runtime_key": key, "definition_names": names})
    return sorted(records, key=lambda record: record["runtime_key"])


if __name__ == "__main__":
    for record in host_declarations():
        print(f"{record['runtime_key']}  ->  {record['definition_names']}")
