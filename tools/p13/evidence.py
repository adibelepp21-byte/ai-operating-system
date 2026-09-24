"""P13 evidence: cycle records and P13's Trace (Blueprint `§6`; `P13-018` items 3, 4, 6).

Everything is written beneath `docs/operations/p13/`, the live root
`P13-ENV-01` designates, and nowhere else.

* `cycles/<cycle_id>.json` holds one record per cycle, in P12 `§29`'s twelve
  elements. It is created exclusively (`open(..., "x")`) and never rewritten.
  It carries a `record_digest` over its own content.
* `trace/trace` is a Native Core `TraceWriter` over `LocalAppendOnlyStorage`,
  written at the end of each cycle (Constitution `§3.5` principle 9). It is also
  how P13's own history becomes Memory, through `MemoryReader`.

`verify()` is item 6, *verification of its own authorized evidence operations*.
Every record must hash to its digest. Every record must have exactly one Trace
entry, and every Trace entry must have exactly one record.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from tools.p13.model import digest
from tools.p13.paths import Paths

P13_DEFINITION = "aios-p13-ecosystem/1.0"


class EvidenceStore:
    def __init__(self, paths: Paths):
        self._paths = paths

    # -- writing -----------------------------------------------------------
    def write_cycle(self, record: Dict[str, Any]) -> Tuple[Path, str]:
        body = dict(record)
        body["record_digest"] = digest(record)
        self._paths.cycles.mkdir(parents=True, exist_ok=True)
        path = self._paths.cycles / f"{record['cycle_id']}.json"
        with open(path, "x", encoding="utf-8") as handle:
            json.dump(body, handle, indent=2, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
        return path, body["record_digest"]

    def readback(self, path: Path, expected: str) -> bool:
        body = json.loads(path.read_text(encoding="utf-8"))
        claimed = body.pop("record_digest", None)
        return claimed == expected == digest(body)

    def write_trace(self, *, outputs, status, tools_used, knowledge_consumed,
                    memory_consumed) -> None:
        from native_core.core.infrastructure import LocalAppendOnlyStorage
        from native_core.core.trace import TraceWriter
        from native_core.core.trace.record import new_record
        from tools.p13.state import P13_INSTANCE
        storage = LocalAppendOnlyStorage(self._paths.trace)
        storage.provision()
        TraceWriter(storage).write(new_record(
            agent_definition_version=P13_DEFINITION, agent_instance=P13_INSTANCE,
            runtime="p13-cycle", skills_used=("p13-cycle",),
            tools_used=tuple(tools_used), knowledge_consumed=tuple(knowledge_consumed),
            memory_consumed=tuple(memory_consumed), outputs=outputs,
            cost_resource_metadata={}, status=status))

    # -- item 6 ------------------------------------------------------------
    def verify(self) -> Dict[str, Any]:
        faults: List[str] = []
        records = {}
        if self._paths.cycles.is_dir():
            for path in sorted(self._paths.cycles.glob("*.json")):
                try:
                    body = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, ValueError) as error:
                    faults.append(f"{path.name}: unreadable ({error})")
                    continue
                claimed = body.pop("record_digest", None)
                if claimed != digest(body):
                    faults.append(f"{path.name}: content does not hash to its digest")
                records[body.get("cycle_id")] = claimed
        traced: Dict[str, str] = {}
        if (self._paths.trace / "trace").is_file():
            from native_core.core.infrastructure import LocalAppendOnlyStorage
            from native_core.core.trace import TraceReader
            storage = LocalAppendOnlyStorage(self._paths.trace)
            storage.provision()
            for entry in TraceReader(storage).read():
                cycle = (entry.outputs or {}).get("cycle_id")
                if cycle in traced:
                    faults.append(f"{cycle}: traced twice")
                traced[cycle] = (entry.outputs or {}).get("record_digest")
        for cycle, recorded_digest in records.items():
            if cycle not in traced:
                faults.append(f"{cycle}: record has no Trace entry")
            elif traced[cycle] != recorded_digest:
                faults.append(f"{cycle}: Trace names a different record digest")
        for cycle in traced:
            if cycle not in records:
                faults.append(f"{cycle}: Trace entry has no record")
        return {"records": len(records), "trace_entries": len(traced),
                "holds": not faults, "faults": faults}
