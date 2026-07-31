"""
Loads the one real Agent Definition instance this phase targets and
exposes exactly what orchestration needs: its Permitted Skills and
Permitted Workflows (for authorization checks — Domain Model §4's
Agent-Definition-specifies-Skill/Workflow relationship), and its
declared Version (recorded into every Trace this run produces, per
Domain Model §2.1's "Agent Definition version" field).

Reads the real governance document only. Never writes to it.
"""

from dataclasses import dataclass
from pathlib import Path

from .governance_reader import ORG_ROOT, read, section_links, version

AGENT_DEFINITION_PATH = ORG_ROOT / "platform" / "agent-definitions" / "governance-artifact-integrity-agent.md"


@dataclass(frozen=True)
class AgentDefinition:
    name: str
    version: str
    path: Path
    permitted_skills: tuple
    permitted_workflows: tuple


def load(path=AGENT_DEFINITION_PATH):
    text = read(path)
    return AgentDefinition(
        name="Governance Artifact Integrity Agent",
        version=version(text),
        path=path,
        permitted_skills=tuple((path.parent / l).resolve() for l in section_links(text, "Permitted Skills")),
        permitted_workflows=tuple((path.parent / l).resolve() for l in section_links(text, "Permitted Workflows")),
    )
