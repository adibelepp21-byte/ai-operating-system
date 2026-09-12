"""P12-W4 — the durable Trace store registry.

Authorized by the Founder P12 Authorization `§17` (Execution Integration), whose
canonical chain terminates in **EVIDENCE**:

```text
INTENT → DECISION → WORK → EXECUTION → OBSERVATION → VERIFICATION → EVIDENCE
```

**What this module exists to fix.** `derived_views` answers *"what has run"* and
*"what has failed"* with `UNKNOWN`, explaining that a Trace store is
per-`StorageFacility` and no cross-process registry exists. That explanation was
accurate and incomplete. Measured at P12-W4 entry:

```text
durable trace partitions on disk          0
constructions of LocalAppendOnlyStorage   0  (outside its own definition)
resident executions supplying a writer    0  (TraceWriter is an optional argument,
                                              defaulted to None everywhere)
```

**The boundary was wired and never fed.** A registry alone would have enumerated
an empty set and reported success — a guard that passes because there is nothing
to see. So this module does two things that must stay together: it *discovers*
stores, and the accompanying root proof *produces* one by running a real
execution through a real `TraceWriter` over `LocalAppendOnlyStorage`.

**It owns no truth.** Discovery is by filesystem shape — a store is a directory
holding a partition file — and reading is delegated to the Native Core
`TraceReader`, which is the only thing entitled to interpret a Trace record. This
module never parses a record itself, so it cannot become a second Trace
vocabulary.

**Native Core is untouched.** `§11` freezes eleven boundaries; this is `tools/`
integration over them, which `§11` expressly permits: *"P12 tetap boleh
menggunakan existing architecture dan integration layers yang sah di luar frozen
Native Core."*
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Tuple

from native_core.core.infrastructure import LocalAppendOnlyStorage
from native_core.core.trace import TRACE_PARTITION, TraceReader, TraceRecord

REPO_ROOT = Path(__file__).resolve().parents[1]

#: Where P12 keeps durable trace stores. One subdirectory per store, each
#: holding the partition files its facility wrote. The location is a P12
#: integration decision, not a Native Core one: the facility resolves nothing
#: outside the `base_dir` it is handed.
STORE_ROOT = REPO_ROOT / "docs/architecture/p12/trace-stores"


@dataclass(frozen=True)
class TraceStore:
    """One durable store, addressed by the directory its facility wrote into."""

    name: str
    path: Path

    @property
    def partition_file(self) -> Path:
        return self.path / TRACE_PARTITION

    def reader(self) -> TraceReader:
        """A Native Core reader over this store. Read-only by construction."""
        storage = LocalAppendOnlyStorage(self.path)
        storage.provision()
        return TraceReader(storage)

    def records(self) -> Tuple[TraceRecord, ...]:
        return tuple(self.reader().read())


def discover(root: Path = STORE_ROOT) -> Tuple[TraceStore, ...]:
    """Every durable trace store beneath `root`, found by the shape on disk.

    A store is a directory containing a `trace` partition file. Nothing is
    listed, registered or configured: a store that exists is found, and a store
    that does not exist is absent rather than assumed.
    """
    if not root.is_dir():
        return ()
    found = [
        TraceStore(name=child.name, path=child)
        for child in sorted(root.iterdir())
        if child.is_dir() and (child / TRACE_PARTITION).is_file()
    ]
    return tuple(found)


def all_records(root: Path = STORE_ROOT) -> Iterator[Tuple[str, TraceRecord]]:
    """Every record in every discovered store, paired with its store name."""
    for store in discover(root):
        for record in store.records():
            yield store.name, record


def what_has_run(root: Path = STORE_ROOT) -> dict:
    """Evidence for *"what has run"* — or an empty result that says so.

    Returns counts by status using the **ratified** Trace vocabulary. It does
    not invent a status, and it does not report success for a store it could
    not read.
    """
    by_status: dict = {}
    stores = discover(root)
    total = 0
    for _name, record in all_records(root):
        status = record.status
        by_status[status] = by_status.get(status, 0) + 1
        total += 1
    return {
        "stores": len(stores),
        "records": total,
        "by_status": by_status,
        "store_names": tuple(s.name for s in stores),
    }


def what_has_failed(root: Path = STORE_ROOT) -> Tuple[TraceRecord, ...]:
    """Records whose ratified status is `failure`.

    An escalation is **not** a failure. `DP-02 §3 E11-03` settled that a correct
    refusal is not an execution failure merely because the action was not
    performed, and the Trace vocabulary keeps `escalation` distinct from
    `failure` for the same reason. Collapsing them here would re-introduce the
    conflation one layer down.
    """
    return tuple(
        record for _name, record in all_records(root) if record.status == "failure"
    )


def main(argv=None) -> int:
    summary = what_has_run()
    print(f"stores   : {summary['stores']}")
    print(f"records  : {summary['records']}")
    print(f"by status: {summary['by_status']}")
    for name in summary["store_names"]:
        print(f"  - {name}")
    failures = what_has_failed()
    print(f"failures : {len(failures)}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
