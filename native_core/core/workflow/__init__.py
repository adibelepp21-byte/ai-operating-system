"""
Workflow boundary (Native Core Blueprint §3 root tree; workflow_spec; Domain
Model §1/§2/§4/§5/§6/§7; Freeze §4/§5 layer 6, §6; Roadmap §9.8;
INV-13/INV-4/INV-12/INV-15; ADR-0004; ADR-0007).

Workflow is one of the **eleven frozen subsystem boundaries** — Blueprint §3
fixes the tree as `core/{trace, memory, knowledge, governance, runtime, agent,
capability, skill, workflow, infrastructure, optimization}`, and §4 states the
core region *"contains exactly the eleven frozen subsystem boundaries — no
more."* No entity and no subsystem is introduced here.

Domain Model §2 [E]: a Workflow is *"an explicit, inspectable composition of
Skills (and possibly Agent Instance invocations) accomplishing a multi-step
outcome."* Freeze §4 [E] states its governing role: *"governed composition; the
sanctioned multi-agent channel (INV-13)."*

What this boundary realizes, per workflow_spec §2 and Roadmap §9.8:

    Workflow   —is—        the SOLE sanctioned multi-agent channel   (INV-13)
               —contains→  Skills, in explicit ordered steps
               —coordinates→ Agent Instances, each step an action    (INV-4)
    Agent Def  —declares→  zero or more Workflows                    (INV-15)

Public surface:
  - models:       WorkflowIdentity · Workflow
  - composition:  SkillRef · AgentInstanceRef · WorkflowStep · WorkflowComposition
  - coordination: WorkflowCoordination
  - declaration:  AgentDefinitionRef · WorkflowDeclaration
  - lifecycle:    WorkflowState · WorkflowLifecycleModel ·
                  WorkflowLifecycleState · WorkflowLifecycle · WorkflowMonitor
  - subsystem:    WorkflowSubsystem · create_workflow_subsystem
  - exceptions:   WorkflowError · InvalidWorkflow · InvalidWorkflowStep ·
                  InvalidWorkflowComposition · InvalidWorkflowDeclaration ·
                  UnresolvedWorkflow · DuplicateWorkflowDeclaration ·
                  DirectCollaborationForbidden · WorkflowLifecycleError ·
                  InvalidWorkflowTransition · UnknownWorkflowLifecycle ·
                  DuplicateWorkflowLifecycle

**How INV-13 is enforced structurally** — the reason this boundary exists.
Freeze §6 [E] forbids the `direct Instance↔Instance` direction, and Freeze AD-9
names free agent-to-agent delegation a rejected anti-pattern, which Roadmap
§9.8 lists as this boundary's principal risk. Three structural properties, none
of them a bypassable check:

  1. `AgentInstanceRef` carries a key and nothing else — no peer, target,
     recipient, or channel field exists anywhere in this package.
  2. `WorkflowCoordination` cannot be constructed without a `Workflow`. No
     two-instance constructor exists, and no function accepts a pair.
  3. Participants are **derived from the composition's steps**, never supplied
     independently — so no value in this package can assert that two Agent
     Instances collaborate outside a Workflow.

INV-13 sanctions three channels; this boundary owns exactly one. Knowledge and
scoped Memory belong to `core/knowledge/` and `core/memory/` and are not
reachable from here. Domain Model §4 [E] notes that *"a transient, pairwise
coordination need is satisfiable as a Memory scoped to that pair — this does
not require a new entity"*; that path runs through Memory.

NOT implemented here, and reserved by the frozen architecture:
  - **Execution of any kind** — no `execute`/`run`/`invoke`/`perform`/
    `dispatch`. workflow_spec §8 [E]: a Workflow *"is not the Runtime."*
    Running a composition is Runtime driving Agent-Instance actions (Freeze §5
    layer 2). **Phase 9 did not relax this.** `lifecycle.py` owns the *state
    semantics* of an execution — which transitions are lawful, and what the
    current condition is — and performs no work whatsoever. The two are
    genuinely different: `ACT-CC-P9-001 §11.2` gives Workflow the lifecycle
    while `§10.1` gives Runtime the hosting, and this package holds only the
    first half.
  - **Resumability, retry, recovery, compensation, rollback** —
    `ACT-CC-P9-001 §11.4`/`§11.5`/`§13.2` place all of them outside Phase 9.
    `SUCCEEDED` and `FAILED` have no lawful successor, so a terminal Workflow
    cannot be resumed rather than merely being expected not to be.
  - **Trace authorship.** INV-4 gives each Agent-Instance action exactly one
    Trace; workflow_spec §9 [E] makes each step's actor the author. The
    Workflow authors none of its own.
  - **Failure recovery, compensation, retry, timeout, parallelism** —
    workflow_spec §13/§14 [O] reserve the failure-recovery model; the
    fail-closed baseline holds (§11).
  - **Compile-time composition validation** — workflow_spec §12 [O] marks it a
    candidate evolution, admissible only under governance.
  - **A Runtime↔Workflow relationship modelled from this side.** `FD-P9-001`
    ratifies the hosting direction — `ACT-CC-P9-001 §8.1`: *"Runtime MAY depend
    on and access the Workflow capability for authorized execution hosting,
    without becoming the owner of Workflow semantics."* That edge runs
    **Runtime → Workflow and not back**. This package imports no Runtime type,
    names no Runtime, and exports nothing containing `runtime`; the Workflow
    conformance suite still asserts it. `§8.3` is the reason — *"Hosting is not
    ownership"* — and an edge modelled from both ends would be the ownership
    inversion it prohibits.
  - **Workflow↔Skill relationship** — workflow_spec §7/§14 still mark it
    *Inferred*, and Freeze §6 [E] states *"Inferred relationships are NOT
    frozen."* Not modelled.
  - **Registry, discovery, or catalogue** — reserved (Blueprint §25;
    skill_spec §13/§14 precedent). `resolve()` searches one declaration only.
  - **Workflow instances** — none is created here. This package models the
    entity type, exactly as `core/capability/` and `core/skill/` do.

Ownership: this boundary owns **only the Workflow contract, its composition,
its coordination, and the Agent-Definition declaration**. ADR-0004 [E] decides
that *"Workflow is owned centrally, per Domain Model §5, joining Skill, Tool,
and Runtime in that ownership category"* — so a Workflow carries no owning
Department. ADR-0004 further separates specification from ownership: a
Definition declaring a Workflow confers no ownership over it. Runtime owns
hosting and execution · Agent owns definition and instance identity · Skill
owns reusable ability · Governance owns authority · Trace owns history ·
Infrastructure owns facilities. No ownership transfer.

Dependencies: stdlib only. This package imports nothing from Runtime, Agent,
Skill, Capability, Governance, Trace, Memory, Knowledge, Optimization or
Infrastructure, and holds no external dependency (INV-12; workflow_spec §8).
workflow_spec §7 [E] would permit depending on Skill (*"composes Skills"*);
opaque `SkillRef` and `AgentInstanceRef` stubs are used instead, matching the
pattern established by `core/capability/`'s `DepartmentRef` and `core/skill/`'s
`AgentDefinitionRef`.
"""

from .composition import (
    AgentInstanceRef,
    SkillRef,
    WorkflowComposition,
    WorkflowStep,
)
from .coordination import WorkflowCoordination
from .declaration import AgentDefinitionRef, WorkflowDeclaration
from .realization import CapabilityRef, WorkflowRealization
from .exceptions import (
    DirectCollaborationForbidden,
    DuplicateWorkflowDeclaration,
    DuplicateWorkflowLifecycle,
    InvalidWorkflow,
    InvalidWorkflowComposition,
    InvalidWorkflowDeclaration,
    InvalidWorkflowRealization,
    InvalidWorkflowStep,
    InvalidWorkflowTransition,
    UnknownWorkflowLifecycle,
    UnresolvedWorkflow,
    WorkflowError,
    WorkflowLifecycleError,
)
from .lifecycle import (
    WorkflowLifecycle,
    WorkflowLifecycleModel,
    WorkflowLifecycleState,
    WorkflowMonitor,
    WorkflowState,
)
from .models import Workflow, WorkflowIdentity
from .subsystem import WorkflowSubsystem, create_workflow_subsystem

__all__ = [
    "AgentDefinitionRef",
    "CapabilityRef",
    "AgentInstanceRef",
    "DirectCollaborationForbidden",
    "DuplicateWorkflowDeclaration",
    "DuplicateWorkflowLifecycle",
    "InvalidWorkflow",
    "InvalidWorkflowComposition",
    "InvalidWorkflowDeclaration",
    "InvalidWorkflowRealization",
    "InvalidWorkflowStep",
    "InvalidWorkflowTransition",
    "SkillRef",
    "UnknownWorkflowLifecycle",
    "UnresolvedWorkflow",
    "Workflow",
    "WorkflowComposition",
    "WorkflowCoordination",
    "WorkflowDeclaration",
    "WorkflowError",
    "WorkflowIdentity",
    "WorkflowLifecycle",
    "WorkflowLifecycleError",
    "WorkflowLifecycleModel",
    "WorkflowLifecycleState",
    "WorkflowMonitor",
    "WorkflowRealization",
    "WorkflowState",
    "WorkflowStep",
    "WorkflowSubsystem",
    "create_workflow_subsystem",
]
