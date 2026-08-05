"""
Workflow domain model — IMMUTABLE DATA CONTRACTS (Blueprint §3 root tree;
workflow_spec §1–§11; Domain Model §2/§4/§5/§6/§7; Freeze §4/§5 layer 6;
INV-13/INV-4/INV-12/INV-15; ADR-0004).

Declares the canonical **Workflow**. Domain Model §2 [E]: *"An explicit,
inspectable composition of Skills (and possibly Agent Instance invocations)
accomplishing a multi-step outcome."* Freeze §4 [E] adds its governing role:
*"governed composition; the sanctioned multi-agent channel (INV-13)."*

**Composition, not execution.** workflow_spec §8 [E]: a Workflow *"is not the
Runtime"*. Running a composition is Runtime driving Agent-Instance actions
(Freeze §5 layer 2); this boundary declares the shape a composition may take
and nothing about how it runs. These are frozen dataclasses following the
established Native Core convention (`CapabilityIdentity`, `SkillIdentity`,
`AgentDefinition`); `__post_init__` performs *structural* fail-closed validation
only (PR-4), never domain logic and never authority evaluation (PR-3).

Contracts declared here:

  - `WorkflowIdentity` — `(workflow_key, workflow_version)`. **ADR-0004** [E]
    fixes Workflow's lifecycle as *"versioned independently … evolved through
    governed revisions … compatibility boundaries preserved where applicable …
    behavioral drift documented at change time."* **No version format is
    imposed** — no ratified source defines one, so the version is an opaque
    non-empty string, exactly as for Skill.

  - `Workflow` — identity plus nothing further. Ownership is **not** a field:
    **ADR-0004** [E] decides that *"Workflow is owned centrally, per Domain
    Model §5, joining Skill, Tool, and Runtime in that ownership category."*
    There is therefore no owning Department to reference. This is the
    load-bearing difference from Capability, which carries `owning_department`
    because INV-1 requires it, and the shared property with Skill.

ADR-0004 is also explicit that central ownership does **not** follow from
Agent Definition's `specifies` relationship: *"specification and ownership are
separate concerns in the Domain Model, exactly as Agent Definition's specifies
relationship to Skill does not make Skill Department-owned either."* The
declaration model in `declaration.py` therefore confers no ownership.

Deliberately ABSENT, each for a stated reason:

  - **No execution, invocation, or dispatch** — no `execute`/`run`/`invoke`/
    `perform`/`dispatch`. workflow_spec §8 [E]: *"Is not the Runtime."*
  - **No Trace authorship.** INV-4 [E] gives each Agent-Instance action exactly
    one Trace; workflow_spec §9 [E]: *"Each coordinated step is an
    Agent-Instance action producing exactly one Trace record."* The step's
    actor produces it, never the Workflow.
  - **No Workflow instances** — this models the entity type, exactly as
    `core/capability/` and `core/skill/` do.
  - **No registry, lookup index, or discovery.** Registry discipline is [O]
    reserved (skill_spec §13/§14 precedent; Blueprint §25).
  - **No failure-recovery or compensation model.** workflow_spec §13/§14 [O]
    reserve it; the fail-closed baseline holds.
  - **No Workflow↔Capability relationship.** workflow_spec §7/§14 mark it
    *Inferred*, and Freeze §6 [E] states *"Inferred relationships are NOT
    frozen."*

Dependencies: stdlib only. This module imports nothing from Runtime, Agent,
Skill, Capability, Governance, Trace, Memory, Knowledge, Optimization, or
Infrastructure, and holds no external dependency (INV-12; workflow_spec §8).
"""

from __future__ import annotations

from dataclasses import dataclass

from .exceptions import InvalidWorkflow


def _require_text(value: object, label: str, error: type) -> None:
    """Fail closed on anything that is not a non-empty string (PR-4)."""
    if not isinstance(value, str) or not value.strip():
        raise error(f"{label} must be a non-empty string")


@dataclass(frozen=True, order=True)
class WorkflowIdentity:
    """The stable identity of a Workflow: its key and its version.

    Frozen, hashable and comparable. ADR-0004 versions Workflow independently;
    no version scheme is imposed, because none is ratified."""

    workflow_key: str
    workflow_version: str

    def __post_init__(self) -> None:
        _require_text(self.workflow_key, "workflow_key", InvalidWorkflow)
        _require_text(self.workflow_version, "workflow_version", InvalidWorkflow)


@dataclass(frozen=True)
class Workflow:
    """A governed, inspectable composition — the sole multi-agent channel.

    Owned centrally (ADR-0004) — deliberately carries no owner reference,
    because no Department owns a Workflow. Descriptive only: it holds no
    execution, authors no Trace (INV-4), and holds no external dependency
    (INV-12)."""

    identity: WorkflowIdentity

    def __post_init__(self) -> None:
        if not isinstance(self.identity, WorkflowIdentity):
            raise InvalidWorkflow("identity must be a WorkflowIdentity")
