"""
Agent Integration Validator.

Purpose: confirm that an Agent Definition's declared Permitted Skills and
Permitted Workflows (Agent Definition Framework §8) are consistent with
the execution-catalog artifacts that exist, in both directions: that
every declared permission resolves to a real, correctly-typed artifact,
and that every artifact already declaring this Agent Definition as its
invoker is reflected back in the Agent Definition's own permissions.

Validation scope: every Agent Definition instance found under
docs/architecture/organization/*/agent-definitions/*.md, checked against
every Skill/Workflow instance in the execution catalog.

Assumptions: a catalog artifact "declares" a given Agent Definition as
its invoker if it links to that Agent Definition's file anywhere in its
body — the same heuristic link_classifier.py already uses for its
agent-definition-reference category. The Agent Definition's own
Permitted Skills / Permitted Workflows sections are parsed the same way
agent_definitions.py already does for the dependency graph. A section's
prose may contain a link unrelated to the permission itself (for
example, a citation to the ADR that resolved minimum-cardinality); this
validator only evaluates links whose target lies inside the
execution-catalog directory and silently ignores any other link in that
section as incidental prose, not a permission entry.

False-positive risk: medium in the reverse direction — an artifact could
cite an Agent Definition incidentally rather than as a genuine invocation
declaration. No structured field distinguishes intent from incidental
citation yet, the same limitation the Cross-Reference Validator already
documents for links in general. Low in the forward direction — a
Permitted Skills/Permitted Workflows link either resolves to the
expected entity type or it does not.

Operational value: high — this is exactly the class of gap the Architect
identified by direct inspection during the Agent Integration Validation
Phase: Permitted Skills/Permitted Workflows declared empty while ten
Skills and five Workflows already named this Agent Definition as their
invoker. This validator makes that class of gap detectable by tooling
going forward, instead of requiring another manual discovery.

Severity model:
  - a Permitted Skills/Permitted Workflows link that does not resolve to
    a real file: "error".
  - a link listed under Permitted Skills pointing outside skill/ (or
    under Permitted Workflows pointing outside workflow/): "error".
  - a catalog Skill/Workflow that names this Agent Definition as its
    invoker but is not listed in the Agent Definition's own matching
    Permitted section: "warning" — a valid, non-blocking lifecycle state
    per Domain Model §7 invariant 15 and ADR-0007, not a structural
    defect, but worth surfacing since closing it is exactly what this
    validator exists to make visible.
"""

from . import catalog
from .agent_definitions import agent_definition_files, permitted_links
from .catalog import catalog_files, extract_canonical_key, extract_md_links, read_text, rel
from .models import Finding

NAME = "Agent Integration Validator"

SECTION_EXPECTED_TYPE = {
    "Permitted Skills": "skill",
    "Permitted Workflows": "workflow",
}
SECTION_FOR_TYPE = {v: k for k, v in SECTION_EXPECTED_TYPE.items()}


def _citing_artifacts(agent_def_path):
    resolved = agent_def_path.resolve()
    citing = []
    for etype, f in catalog_files():
        if etype not in SECTION_FOR_TYPE:
            continue
        for link in extract_md_links(read_text(f)):
            if link.startswith("http"):
                continue
            if (f.parent / link).resolve() == resolved:
                citing.append((etype, f))
                break
    return citing


def run():
    findings = []
    for adf in agent_definition_files():
        adf_rel = rel(adf)
        permitted_targets = set()

        for a, header, link in permitted_links():
            if a != adf:
                continue
            target = (adf.parent / link).resolve()
            if not target.is_file():
                findings.append(Finding(
                    NAME, "error", f"{header} link '{link}' does not resolve", adf_rel,
                ))
                continue
            if catalog.CATALOG_ROOT not in target.parents:
                continue  # incidental prose link, not a permission entry
            expected_type = SECTION_EXPECTED_TYPE[header]
            try:
                actual_type = target.relative_to(catalog.CATALOG_ROOT).parts[0]
            except ValueError:
                actual_type = None
            if actual_type != expected_type:
                findings.append(Finding(
                    NAME, "error",
                    f"{header} links to {rel(target)}, which is in "
                    f"'{actual_type}/', expected '{expected_type}/'",
                    adf_rel,
                ))
                continue
            permitted_targets.add(target)

        for etype, f in _citing_artifacts(adf):
            if f.resolve() in permitted_targets:
                continue
            key = extract_canonical_key(read_text(f)) or rel(f)
            findings.append(Finding(
                NAME, "warning",
                f"{key} ({rel(f)}) names this Agent Definition as its invoker but "
                f"is not listed in its {SECTION_FOR_TYPE[etype]}",
                adf_rel,
            ))
    return findings
