"""
Agent Instance materialization.

Deliberately not a documented artifact — Domain Model §5 marks Agent
Instance "Not owned — a transient instantiation, tracked by Runtime,"
and §6 marks its lifecycle "Fastest-changing... by design: spawned,
active, terminated — no governance overhead per instance." This module
represents that ephemerality faithfully: an AgentInstance object exists
only in memory for the duration of one harness run, is never written to
disk as a persistent record, and is identified by a freshly generated id
each time. What outlives the instance is not the instance itself but the
Trace records it produces (Domain Model invariant 4) — this module
supplies the instance id those records reference; it is not itself a
record.
"""

import time
import uuid
from dataclasses import dataclass, field


@dataclass
class AgentInstance:
    instance_id: str
    agent_definition_name: str
    agent_definition_version: str
    runtime_key: str
    status: str = "spawned"
    spawned_at: float = field(default_factory=time.time)

    def activate(self):
        self.status = "active"

    def terminate(self):
        self.status = "terminated"


def spawn(agent_definition, runtime):
    return AgentInstance(
        instance_id=f"instance-{uuid.uuid4().hex[:12]}",
        agent_definition_name=agent_definition.name,
        agent_definition_version=agent_definition.version,
        runtime_key=runtime.canonical_key,
    )
