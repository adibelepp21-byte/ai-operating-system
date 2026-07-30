"""
Knowledge composition root (Phase 3.331) — dependency wiring only.

Assembles the already-certified Knowledge components (Phases 3.313–3.330) into a
single dependency graph via constructor injection, eliminating manual
construction. It contains NO business logic, NO architectural change, and NO
contract change; it only instantiates existing certified implementations and
wires them together.

Wiring graph (constructor injection only):

    StorageFacility (Infrastructure, supplied by caller)
        └─► InfrastructureKnowledgeStore  (Knowledge persistence over the facility)
    InMemoryKnowledgeVersioning           (Active/status derivation)
        └─► InMemoryKnowledgeRepository(store, versioning)   (orchestration)
              ├─► InMemoryKnowledgeAdmission(repository, versioning)  (orchestration)
              └─► InMemoryKnowledgeRetrieval(repository)              (read delegation)

The factory owns ONLY object construction; after it returns it holds no runtime
state. There is no global, singleton, registry, service locator, reflection,
runtime discovery, dependency cache, or lazy magic.

Ownership after construction is unchanged: Infrastructure owns bytes; the store
owns Knowledge persistence; Versioning owns derivation; Repository/Admission own
orchestration; Retrieval owns read delegation; Governance owns authority; Memory
owns candidate creation. The composition root owns none of these.

Dependencies: the Knowledge implementations + contracts from THIS package, and
the Infrastructure `StorageFacility` (for the factory's input type). It imports
nothing from Memory or Governance (admission receives those at call time, not at
construction), and nothing from Runtime, Execution, Workflow, Agent, Trace,
Scheduler, or any registry/reflection/importlib. Stdlib only.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..infrastructure import StorageFacility
from .admission import InMemoryKnowledgeAdmission, KnowledgeAdmission
from .infrastructure_store import InfrastructureKnowledgeStore
from .repository import InMemoryKnowledgeRepository, KnowledgeRepository
from .retrieval import InMemoryKnowledgeRetrieval, KnowledgeRetrieval
from .storage import KnowledgeStore
from .versioning import InMemoryKnowledgeVersioning, KnowledgeVersioning


@dataclass(frozen=True)
class KnowledgeSubsystem:
    """The assembled Knowledge subsystem — an immutable bundle of the wired
    components. Exposes exactly the five collaborators and nothing else: no
    helper method, no business operation, no lifecycle management."""

    repository: KnowledgeRepository
    admission: KnowledgeAdmission
    retrieval: KnowledgeRetrieval
    storage: KnowledgeStore
    versioning: KnowledgeVersioning


def create_knowledge_subsystem(storage: StorageFacility) -> KnowledgeSubsystem:
    """Assemble the certified Knowledge subsystem over an Infrastructure
    `StorageFacility`, by constructor injection only. Instantiates existing
    certified implementations and wires them; adds no behavior and holds no
    state after returning. Repeated calls produce an identical graph topology.
    """
    store = InfrastructureKnowledgeStore(storage)
    versioning = InMemoryKnowledgeVersioning()
    repository = InMemoryKnowledgeRepository(store, versioning)
    admission = InMemoryKnowledgeAdmission(repository, versioning)
    retrieval = InMemoryKnowledgeRetrieval(repository)
    return KnowledgeSubsystem(
        repository=repository,
        admission=admission,
        retrieval=retrieval,
        storage=store,
        versioning=versioning,
    )
