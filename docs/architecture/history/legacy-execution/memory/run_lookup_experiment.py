#!/usr/bin/env python3
"""
Memory lookup experiment: builds a memory index from every Trace record
that exists before this run, actually executes the harness once more to
produce a genuinely new Trace (not a replay), then looks up the new
Trace's evidence against the prior index.

Also runs a second, deliberately stress-tested lookup using an
artificially tiny retention window, since default retention (1 hour)
cannot organically produce an "outdated" classification within one
working session — the same deliberate-exercise practice this program
has used throughout (input-validation failures, escalation) to generate
evidence for paths real data wouldn't otherwise reach.
"""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import orchestrator
from execution.memory.extractor import extract_memories, load_trace_records
from execution.memory.lookup import build_index, lookup_evidence
from execution.trace_schema import normalize_record


def _report(results):
    counts = Counter(r.classification for r in results)
    print(f"Total evidence entries checked: {len(results)}")
    print(f"Classification counts: {dict(counts)}")
    for r in results:
        tag = " (near-miss: same kind, different content exists)" if r.near_miss_kind_match else ""
        print(f"  [{r.classification}]{tag} {r.kind}: {r.content[:110]}")


def main():
    prior_records = load_trace_records()
    prior_memories = extract_memories(prior_records)
    print(f"Prior memory index built from {len(prior_records)} existing Trace records -> {len(prior_memories)} memories\n")

    print("Executing a genuinely new run to produce a fresh Trace...")
    result = orchestrator.run()
    print(f"New run trace file: {result['trace_file']}\n")

    new_records = [
        normalize_record(json.loads(line))
        for line in Path(result["trace_file"]).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    print("=== Standard lookup (default retention: 3600s) ===")
    index = build_index(prior_memories)
    standard_results = []
    for r in new_records:
        standard_results.extend(lookup_evidence(r, index))
    _report(standard_results)

    print("\n=== Stress test: artificially tiny retention (forces 'outdated') ===")
    stale_memories = extract_memories(prior_records, retention_seconds=0.0001)
    stale_index = build_index(stale_memories)
    stale_results = []
    for r in new_records:
        stale_results.extend(lookup_evidence(r, stale_index))
    _report(stale_results)


if __name__ == "__main__":
    main()
