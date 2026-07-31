#!/usr/bin/env python3
"""
Runs real retrieval queries relevant to this harness's own execution
through both interfaces — the naive linear search() baseline and the
index-backed KnowledgeRetrievalAdapter — and reports hit quality and
timing for both, as evidence toward whether the adapter's added
structure (document loader, index, evidence references with heading
context) is operationally worth its cost over the naive baseline.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution.knowledge.retrieval import REPO_ROOT, KnowledgeRetrievalAdapter, search

QUERIES = [
    "escalation status",
    "compatibility boundary",
    "Canonical Key",
    "no minimum cardinality",
]


def main():
    print("--- Baseline: naive linear search() ---\n")
    start = time.perf_counter()
    for q in QUERIES:
        hits = search(q, max_hits=5)
        print(f"Query: {q!r} -> {len(hits)} hit(s)")
        for h in hits[:3]:
            print(f"  {h.file.relative_to(REPO_ROOT)}:{h.line_number}: {h.line_text[:100]}")
    baseline_elapsed = time.perf_counter() - start
    print(f"\nBaseline total time for {len(QUERIES)} queries: {baseline_elapsed * 1000:.2f} ms\n")

    print("--- Adapter: document loader + index + EvidenceReference ---\n")
    build_start = time.perf_counter()
    adapter = KnowledgeRetrievalAdapter()
    build_elapsed = time.perf_counter() - build_start
    print(f"Index build time: {build_elapsed * 1000:.2f} ms, vocabulary size: {adapter.index.vocabulary_size}\n")

    query_start = time.perf_counter()
    for q in QUERIES:
        hits = adapter.retrieve(q, max_hits=5)
        print(f"Query: {q!r} -> {len(hits)} hit(s)")
        for h in hits[:3]:
            print(f"  {h.file.relative_to(REPO_ROOT)}:{h.line_number} [{h.heading_context}] (score={h.score}): {h.line_text[:100]}")
    query_elapsed = time.perf_counter() - query_start
    print(f"\nAdapter query-only time for {len(QUERIES)} queries: {query_elapsed * 1000:.2f} ms")
    print(f"Adapter total time (build + queries): {(build_elapsed + query_elapsed) * 1000:.2f} ms")


if __name__ == "__main__":
    main()
