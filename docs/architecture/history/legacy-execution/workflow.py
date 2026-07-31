"""
Workflow loading and execution-evidence tracking.

`load()` reads a Workflow instance and exposes its ordered Contains
Skill list (Domain Model §4, Workflow-contains-Skill). Workflow
Framework §10 explicitly excludes execution-order semantics from
governance ("a note on the sequencing or composition structure among
contained Skills... not as an assertion of execution semantics — Domain
Model §8 excludes implementation/execution-order detail from this
document's authority"). This module therefore treats document order (the
order Skills are listed under Composed Elements) as the execution order,
as an explicit implementation-tier choice, not a governance
interpretation.

`WorkflowExecution` (added in the Execution Foundation Stabilization
Phase) records what actually happened during one run — start time, the
order Skills were actually executed in, each Skill's outcome, and a
completion state. This is observation of fact, not the assertion of a
universal ordering, retry, or branching rule; recording what happened is
not the same as governing how it must happen. Retry policy, branching
standards, and scheduling behavior remain explicitly unaddressed here.
"""

import time
from dataclasses import dataclass, field
from pathlib import Path

from .governance_reader import CATALOG_ROOT, canonical_key, read, section_links


@dataclass(frozen=True)
class WorkflowInstance:
    canonical_key: str
    path: Path
    skill_paths: tuple


def load(canonical_key_str):
    slug = canonical_key_str.split(".", 1)[-1]
    path = CATALOG_ROOT / "workflow" / f"{slug}.md"
    text = read(path)
    links = section_links(text, "Composed Elements")
    skill_paths = tuple((path.parent / l).resolve() for l in links if "/skill/" in l)
    return WorkflowInstance(canonical_key=canonical_key(text), path=path, skill_paths=skill_paths)


@dataclass
class SkillExecutionRecord:
    order_index: int
    skill_key: str
    status: str  # mirrors SkillResult.status, plus "escalation" for an authorization refusal


@dataclass
class WorkflowExecution:
    workflow_key: str
    started_at: float = field(default_factory=time.time)
    skill_records: list = field(default_factory=list)
    completion_state: str = "in_progress"  # "in_progress" | "completed" | "failed" | "escalated"
    completed_at: float = None

    def record_skill(self, skill_key, status):
        self.skill_records.append(SkillExecutionRecord(len(self.skill_records), skill_key, status))

    def complete(self, state):
        self.completion_state = state
        self.completed_at = time.time()
