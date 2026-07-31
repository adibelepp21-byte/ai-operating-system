#!/usr/bin/env python3
"""
Runs the Memory extractor against every real Trace file currently on
disk, writes the resulting provisional MemoryRecords to disposable
experimental storage (execution/memory/records/), and prints an
evidence summary: how many Trace records were processed, how many
distinct Memory records were derived, and examples.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution.memory.extractor import MemoryStore, extract_memories, load_trace_records


def main():
    trace_records = load_trace_records()
    memories = extract_memories(trace_records)

    store = MemoryStore()
    path = store.write_all(memories)

    print(f"Trace records processed: {len(trace_records)}")
    print(f"Distinct provisional Memory records derived: {len(memories)}")
    print(f"Written to: {path}")
    print()

    by_kind = {}
    for m in memories:
        by_kind.setdefault(m.observation_kind, []).append(m)
    for kind, items in sorted(by_kind.items()):
        total_occurrences = sum(i.occurrence_count for i in items)
        print(f"kind={kind!r}: {len(items)} distinct record(s), {total_occurrences} total occurrence(s) across source traces")

    print("\nExamples:")
    for m in sorted(memories, key=lambda r: -r.occurrence_count)[:5]:
        print(
            f"  [{m.observation_kind}] occurrences={m.occurrence_count} instances={len(m.agent_instance_ids)} "
            f"traces={len(m.source_trace_ids)} frequency={m.observation_frequency} confidence={m.confidence} "
            f"first_observed_at={m.first_observed_at} last_observed_at={m.last_observed_at}"
        )
        print(f"    {m.content[:160]}")


if __name__ == "__main__":
    main()
