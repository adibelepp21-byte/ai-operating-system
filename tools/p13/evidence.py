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
                faults.extend(f"{path.name}: {f}" for f in decision_provenance(body))
                records[body.get("cycle_id")] = claimed
        executed_in_record = {}
        if self._paths.cycles.is_dir():
            for path in sorted(self._paths.cycles.glob("*.json")):
                try:
                    body = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    continue
                executed_in_record[body.get("cycle_id")] = (
                    (body.get("executed") or {}).get("action_type"))
        traced: Dict[str, str] = {}
        traced_executed: Dict[str, Any] = {}
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
                traced_executed[cycle] = (entry.outputs or {}).get("executed")
        for cycle, recorded_digest in records.items():
            if cycle not in traced:
                faults.append(f"{cycle}: record has no Trace entry")
            elif traced[cycle] != recorded_digest:
                faults.append(f"{cycle}: Trace names a different record digest")
        for cycle in traced:
            if cycle not in records:
                faults.append(f"{cycle}: Trace entry has no record")
            elif traced_executed.get(cycle) != executed_in_record.get(cycle):
                faults.append(f"{cycle}: Trace and record disagree on the executed action")
        return {"records": len(records), "trace_entries": len(traced),
                "holds": not faults, "faults": faults}


def decision_provenance(record: Dict[str, Any]) -> List[str]:
    """P1 from evidence alone: did P13 decide what it executed?

    Every EXECUTE must name a proposal present in the same record. The proposal
    must derive from conclusions present in the record, and every premise of
    those conclusions must be a fact P13 observed, or an evaluation it made, in
    that cycle. An action that arrives any other way, for example put there by a
    test runner, has no such chain, and the record says so.

    Where the record carries a consequence (every cycle since it was
    introduced), its expectation must be the one the proposal carried before the
    gate. An expectation rewritten to fit the result would not match.
    """
    faults: List[str] = []
    proposals = {p.get("id"): p for p in record.get("proposals") or []}
    conclusions = {c.get("id"): c for c in record.get("conclusions") or []}
    observed = {f.get("key") for f in
                ((record.get("observation") or {}).get("before") or {}).get("facts") or []}
    evaluated = {f"eval:{e.get('criterion')}" for e in record.get("evaluations_before") or []}
    verification = record.get("verification") or {}
    executes = [d for d in record.get("decisions") or [] if d.get("decision") == "EXECUTE"]
    if executes and "consequence" in verification and verification["consequence"] is None:
        faults.append("an action executed, but its consequence was not verified")
    for decision in executes:
        proposal = proposals.get(decision.get("proposal"))
        if proposal is None:
            faults.append(f"EXECUTE of {decision.get('proposal')!r} has no proposal "
                          "in the record")
            continue
        for cid in proposal.get("derived_from") or []:
            conclusion = conclusions.get(cid)
            if conclusion is None:
                faults.append(f"{proposal['id']}: derives from {cid!r}, which the "
                              "record does not hold")
                continue
            dangling = [p for p in conclusion.get("premises") or []
                        if p not in observed and p not in evaluated]
            if dangling:
                faults.append(f"{cid}: premises {dangling} were not observed or "
                              "evaluated in this cycle")
        consequence = (record.get("verification") or {}).get("consequence")
        if consequence is not None and consequence.get("expected") != dict(
                tuple(pair) for pair in proposal.get("expected") or []):
            faults.append(f"{proposal['id']}: the recorded expected consequence is "
                          "not the one the proposal carried")
    return faults
