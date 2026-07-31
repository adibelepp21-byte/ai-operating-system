#!/usr/bin/env python3
"""
Aggregates every Trace record this harness has produced so far across
all prior phases and prints a summary, as evidence toward whether
execution-history aggregation has operational value.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution.memory.history import load_all_records, summarize


def main():
    records = load_all_records()
    summary = summarize(records)
    print(f"Total Trace records: {summary.total_records}")
    print(f"Status counts: {summary.status_counts}")
    print(f"Skill invocation counts: {summary.skill_invocation_counts}")
    print(f"Tool invocation counts: {summary.tool_invocation_counts}")
    print(f"Tool resolution rate by action: {summary.tool_resolution_rate}")


if __name__ == "__main__":
    main()
