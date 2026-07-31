"""
Reads Agent Definition instance documents — which live outside the
execution-catalog directory, under
docs/architecture/organization/*/agent-definitions/ — for their
Permitted Skills and Permitted Workflows sections, so the dependency
graph, Orphan Artifact Detector, and Agent Integration Validator can
account for the Agent-Definition-to-Skill and
Agent-Definition-to-Workflow edges the Domain Model recognizes, even
though those instances are not themselves execution-catalog artifacts.

permitted_links() returns every link found in these sections whether or
not it resolves to a real file, so callers that need to report a broken
permission link (Agent Integration Validator) can do so; agent_definition_edges()
and agent_definition_edges_by_section() filter to resolvable links only,
for callers (dependency graph, Orphan Artifact Detector) that only care
about links that actually connect to something. This module never
modifies any Agent Definition document.
"""

import re

from . import catalog
from .catalog import extract_md_links, read_text

PERMITTED_HEADERS = ("Permitted Skills", "Permitted Workflows")


def agent_definition_files():
    # Reads catalog.ORG_ROOT via the module (not a direct name import) so
    # tests can patch it — a direct `from .catalog import ORG_ROOT` binds
    # the value at import time and would not see a later patch.
    return sorted(catalog.ORG_ROOT.glob("**/agent-definitions/*.md"))


def _section_body(text, header):
    pattern = re.compile(rf"^## {re.escape(header)}\s*\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    m = pattern.search(text)
    return m.group(1) if m else ""


def permitted_links():
    """Returns [(agent_definition_path, header, link_str), ...] for every
    link found in a Permitted Skills or Permitted Workflows section,
    resolved or not."""
    results = []
    for adf in agent_definition_files():
        text = read_text(adf)
        for header in PERMITTED_HEADERS:
            for link in extract_md_links(_section_body(text, header)):
                if not link.startswith("http"):
                    results.append((adf, header, link))
    return results


def agent_definition_edges_by_section():
    """Returns [(agent_definition_path, header, target_path), ...] for
    every Permitted Skills / Permitted Workflows link that resolves to a
    real file."""
    edges = []
    for adf, header, link in permitted_links():
        target = (adf.parent / link).resolve()
        if target.is_file():
            edges.append((adf, header, target))
    return edges


def agent_definition_edges():
    """Returns [(agent_definition_path, target_path), ...] for every
    resolvable Permitted Skills / Permitted Workflows link, header
    dropped. See agent_definition_edges_by_section() to keep it."""
    return [(adf, target) for adf, _header, target in agent_definition_edges_by_section()]


def agent_definition_references(candidate_targets):
    """Returns the subset of candidate_targets (a set of resolved Paths)
    referenced by any Agent Definition's Permitted Skills / Permitted
    Workflows links."""
    referenced = set()
    for _, target in agent_definition_edges():
        if target in candidate_targets:
            referenced.add(target)
    return referenced
