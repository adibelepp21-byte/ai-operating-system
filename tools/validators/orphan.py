"""
Orphan Artifact Detector.

Purpose: identify instances never referenced by any other instance in
the catalog, as an informational signal, not an error.

Validation scope: intra-catalog Markdown links, plus, where available,
an Agent Definition's Permitted Skills / Permitted Workflows links (see
agent_definitions.py) — an artifact referenced only from an Agent
Definition, not from another catalog file, is not treated as an orphan.

Assumptions: an unreferenced instance is not necessarily invalid — a
Tool with no current Skill invoking it, or a Skill not yet composed into
any Workflow, is explicitly a valid architectural state per this
corpus's own invariants (e.g. Domain Model §7 invariant 15's treatment
of empty declarations as valid).

False-positive risk: none, by design — this validator does not claim
orphan status is a defect, only reports it.

Operational value: medium — useful for spotting instances that may have
been created but never wired into any real composition, worth a human
glance, not an automatic flag.

Severity model: always "informational".
"""

from .agent_definitions import agent_definition_references
from .catalog import catalog_files, extract_md_links, read_text, rel
from .models import Finding

NAME = "Orphan Artifact Detector"


def run():
    all_files = {f.resolve() for _, f in catalog_files()}
    referenced = set()
    for etype, f in catalog_files():
        for link in extract_md_links(read_text(f)):
            if link.startswith("http"):
                continue
            target = (f.parent / link).resolve()
            if target in all_files:
                referenced.add(target)
    referenced |= agent_definition_references(all_files)

    findings = []
    for etype, f in catalog_files():
        if f.resolve() not in referenced:
            findings.append(Finding(
                NAME, "informational",
                "not referenced by any other catalog artifact or Agent Definition",
                rel(f),
            ))
    return findings
