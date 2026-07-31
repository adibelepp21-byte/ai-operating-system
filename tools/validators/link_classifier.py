"""
Classifies a Markdown link found in an execution-catalog artifact by what
kind of reference it represents, so the Cross-Reference Validator and the
dependency graph builder can reason about link *purpose* rather than
treat every link as interchangeable — the Cross-Reference Validator's
previously documented limitation ("treats all markdown links equally").

Classification is evidence-based and heuristic, derived from the actual
link path patterns already present across the 23 execution-catalog
artifacts (verified by direct inspection of skill/, workflow/, tool/, and
runtime/ files before this module was written). It does not define or
redefine any governed relationship — it only labels existing links for
reporting purposes, using plain path-pattern rules. Two of the six
categories the Architect named (Skill invocation, Tool invocation) are
ambiguous in isolation from the Domain Model's own relationship names, so
this module documents the specific mapping it uses:

  - Workflow composition: Workflow -> Skill link (Domain Model
    Workflow-contains-Skill). Present in the corpus today (each Workflow
    lists its Contains Skill elements as links into skill/).
  - Skill invocation: Skill -> Tool link (Domain Model
    Skill-invokes-Tool). Present in the corpus today (5 of 10 Skills
    link to a Tool from their Interface section).
  - Tool invocation: reserved for a Workflow/Runtime -> Tool link. No
    Domain Model relationship of this shape is declared anywhere in the
    ratified governance baseline, and no such link exists in the corpus
    today. Kept as a defined-but-currently-empty category rather than
    omitted, since silently dropping a category the Architect explicitly
    named would understate the taxonomy requested.
  - Framework reference / Agent Definition reference / Navigation
    convenience link: as named, see classify() below.
"""

FRAMEWORK_REFERENCE = "framework-reference"
AGENT_DEFINITION_REFERENCE = "agent-definition-reference"
WORKFLOW_COMPOSITION = "workflow-composition"
SKILL_INVOCATION = "skill-invocation"
TOOL_INVOCATION = "tool-invocation"
NAVIGATION_CONVENIENCE = "navigation-convenience-link"

# Expected target entity-type directory for relationship categories that
# have one. Used to detect a link classified as a specific relationship
# shape but pointing at the wrong kind of file.
EXPECTED_TARGET_TYPE = {
    WORKFLOW_COMPOSITION: "skill",
    SKILL_INVOCATION: "tool",
}


def classify(source_type, source_path, target_path, catalog_root):
    name = target_path.name
    if name.endswith("-framework.md") or name == "agent-definitions.md":
        return FRAMEWORK_REFERENCE
    if "agent-definitions" in target_path.parts:
        return AGENT_DEFINITION_REFERENCE

    try:
        target_type = target_path.relative_to(catalog_root).parts[0]
    except ValueError:
        target_type = None

    if source_type == "workflow" and target_type == "skill":
        return WORKFLOW_COMPOSITION
    if source_type == "skill" and target_type == "tool":
        return SKILL_INVOCATION
    if target_type == "tool" and source_type in ("workflow", "runtime"):
        return TOOL_INVOCATION
    return NAVIGATION_CONVENIENCE
