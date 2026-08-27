"""
Infrastructure boundary (Native Core Blueprint §14; infrastructure_spec).

The facilities *beneath* the entities: storage under substrate, the execution
substrate, and the single external boundary (Tool) — audited through the
invoking actions, never as independent actors (Infrastructure spec §1; INV-12;
OQ-2). Infrastructure serves; it does not govern (spec §10).

Module isolation (Blueprint §26): this boundary exposes only its permitted
interactions and hides nothing external. It holds no external dependency
(INV-12), owns no Knowledge, and authors no Trace (OQ-2). Its allowed
consumers are the substrate subsystems (storage), Runtime (substrate), and
Agent Instances (the Tool boundary) — Infrastructure spec §7 — none of which
exists yet in Stage I.

Public surface (the only names other boundaries may depend on):
  - lifecycle: Facility, FacilityState, FacilityUnavailable
  - storage:   StorageFacility, LocalAppendOnlyStorage
  - records:   decode_record, decode_records, read_records, RecordDecodeError
  - external:  ToolBoundary, ExternalTool
  - substrate: ExecutionSubstrate, LocalExecutionSubstrate
  - bootstrap: Bootstrap, BootstrapError
  - assembly:  build_default_infrastructure()
"""

from pathlib import Path

from .bootstrap import Bootstrap, BootstrapError
from .facility import Facility, FacilityState, FacilityUnavailable
from .filesystem import FilesystemFacility
from .records import (
    RecordDecodeError,
    decode_record,
    decode_records,
    read_records,
)
from .storage import LocalAppendOnlyStorage, StorageFacility
from .substrate import ExecutionSubstrate, LocalExecutionSubstrate
from .tool_boundary import ExternalTool, ToolBoundary

__all__ = [
    "Facility",
    "FacilityState",
    "FacilityUnavailable",
    "FilesystemFacility",
    "StorageFacility",
    "LocalAppendOnlyStorage",
    "RecordDecodeError",
    "decode_record",
    "decode_records",
    "read_records",
    "ToolBoundary",
    "ExternalTool",
    "ExecutionSubstrate",
    "LocalExecutionSubstrate",
    "Bootstrap",
    "BootstrapError",
    "build_default_infrastructure",
]

# Canonical facility names used within the Infrastructure boundary's own
# bootstrap wiring. These are internal facility names, not entity canonical
# keys (Infrastructure owns no entity).
FILESYSTEM = "filesystem"
STORAGE = "storage"
TOOL_BOUNDARY = "tool-boundary"
SUBSTRATE = "execution-substrate"


def build_default_infrastructure(
    storage_subdir: str = "native_core_storage",
    base_dir: "Path | None" = None,
) -> Bootstrap:
    """Assemble the Stage-I Infrastructure facilities into a single, fail-closed
    Bootstrap, wired in dependency order:

        filesystem  (no deps; discovers the repository root, or uses base_dir)
            -> storage        (persists beneath that root)
        tool-boundary         (no deps; the single external boundary, empty)
        execution-substrate   (no deps; the local substrate beneath Runtime)

    Returns the Bootstrap *un-established* — the caller (the invoking action,
    per spec §4) decides when to `establish()`, keeping facility lifecycle
    subordinate to that action. Establishes nothing on import.

    `base_dir` selects the filesystem facility's root: when None (the default,
    production behaviour) the root is discovered; when provided, that directory
    is the root. The parameter exists so callers — notably hermetic tests — can
    root all storage in an isolated location instead of under the repository,
    without changing production behaviour. It uses the FilesystemFacility's
    existing `root` injection point and adds no new mechanism.

    This assembles ONLY Infrastructure facilities. It does not initialize any
    other subsystem — none exists in Stage I.
    """
    fs = FilesystemFacility(root=base_dir)
    boot = Bootstrap()
    boot.register(FILESYSTEM, fs)

    # Storage persists beneath the discovered repository root. The base
    # directory is computed lazily at establish() time via a thin facility
    # that provisions after filesystem; to keep wiring simple and explicit,
    # we provision filesystem first, then hand its resolved path to storage.
    boot.register(TOOL_BOUNDARY, ToolBoundary())
    boot.register(SUBSTRATE, LocalExecutionSubstrate())

    # Storage depends on filesystem: establish filesystem, then bind storage's
    # base dir under the root. We express this dependency to Bootstrap and
    # resolve the concrete path inside a small deferred provisioning step.
    storage = _DeferredLocalStorage(fs, storage_subdir)
    boot.register(STORAGE, storage, depends_on=(FILESYSTEM,))
    return boot


class _DeferredLocalStorage(LocalAppendOnlyStorage):
    """LocalAppendOnlyStorage whose base directory is resolved from the
    filesystem facility at provision time (after filesystem is ready).

    This keeps storage's dependency on filesystem explicit and fail-closed:
    if filesystem is not provisioned when storage provisions, resolving the
    base path raises (FacilityUnavailable), and Bootstrap halts.
    """

    def __init__(self, filesystem: FilesystemFacility, subdir: str):
        # Base dir is a placeholder until provision(); pass the eventual
        # parent lazily by overriding _provision below.
        super().__init__(base_dir=Path(subdir))
        self._filesystem = filesystem
        self._subdir = subdir

    def _provision(self) -> None:
        # filesystem.root fails closed if filesystem isn't provisioned.
        base = self._filesystem.root / self._subdir
        self._base_dir = base
        super()._provision()
