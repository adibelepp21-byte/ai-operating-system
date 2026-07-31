"""
Dependency Graph Generation.

Purpose: produce a machine-readable graph of the relationships already
declared across the execution catalog and the Agent Definition instances
that reference it, to enable future dependency visualization, impact
analysis (what breaks if this artifact changes), and a structural
alternative to the current link-based Orphan Artifact Detector.

This module performs no validation itself — it is a read-only,
report-only extraction, reusing the same classification logic the
Cross-Reference Validator uses so the graph and the validator can never
disagree about what a link means.

Nodes: every catalog artifact (labeled with its Canonical Key) plus
every Agent Definition instance found under
docs/architecture/organization/*/agent-definitions/.

Edges: derived from link_classifier categories —
  - workflow-composition  (Workflow -> Skill)
  - skill-invocation      (Skill -> Tool)
  - declares-invocation-context (any catalog artifact -> Agent
    Definition instance; the artifact's own citation of who may invoke
    it, not a claim about the Agent Definition's authority)
  - permits (Agent Definition -> Skill or Workflow, from its Permitted
    Skills / Permitted Workflows sections)

Assumptions: same as link_classifier.py and agent_definitions.py.

False-positive risk: none — this is not a pass/fail check; correctness
depends entirely on the same heuristics already documented for those two
modules.

Operational value: currently modest (23 catalog nodes, 1 Agent
Definition node, no visualization consumer exists yet), but this export
is what the Architect's stated next uses (dependency visualization,
impact analysis, improved orphan detection) would consume, without
requiring a schema redesign later since it is derived from the same data
already validated by the other five checks in this package.
"""

import json

from . import catalog
from .agent_definitions import agent_definition_edges, agent_definition_files
from .catalog import catalog_files, extract_canonical_key, extract_md_links, read_text, rel
from .link_classifier import classify, WORKFLOW_COMPOSITION, SKILL_INVOCATION, AGENT_DEFINITION_REFERENCE


def build():
    nodes = {}
    edges = []

    for etype, f in catalog_files():
        key = extract_canonical_key(read_text(f)) or rel(f)
        nodes[str(f.resolve())] = {"id": key, "type": etype, "path": rel(f)}

    for adf in agent_definition_files():
        nodes[str(adf.resolve())] = {"id": rel(adf), "type": "agent-definition", "path": rel(adf)}

    for etype, f in catalog_files():
        text = read_text(f)
        for link in extract_md_links(text):
            if link.startswith("http"):
                continue
            target = (f.parent / link).resolve()
            if not target.is_file():
                continue
            category = classify(etype, f, target, catalog.CATALOG_ROOT)
            src = nodes.get(str(f.resolve()))
            dst = nodes.get(str(target))
            if not src or not dst:
                continue
            if category in (WORKFLOW_COMPOSITION, SKILL_INVOCATION):
                edges.append({"from": src["id"], "to": dst["id"], "relationship": category})
            elif category == AGENT_DEFINITION_REFERENCE:
                edges.append({"from": src["id"], "to": dst["id"], "relationship": "declares-invocation-context"})

    for adf, target in agent_definition_edges():
        src = nodes.get(str(adf.resolve()))
        dst = nodes.get(str(target))
        if src and dst:
            edges.append({"from": src["id"], "to": dst["id"], "relationship": "permits"})

    return {"nodes": list(nodes.values()), "edges": edges}


def to_json(indent=2):
    return json.dumps(build(), indent=indent, sort_keys=False)
