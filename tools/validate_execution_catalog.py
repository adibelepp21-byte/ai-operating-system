#!/usr/bin/env python3
"""
CLI entry point for the execution-catalog validation tooling
(tools/validators/). Runs all six validators and prints a structured
report. Entirely read-only: no file is ever modified by this script or
anything it imports.

Usage:
    python3 tools/validate_execution_catalog.py
    python3 tools/validate_execution_catalog.py --json
    python3 tools/validate_execution_catalog.py --graph
    python3 tools/validate_execution_catalog.py --graph-out FILE

Exit status is 1 if any "error"-severity finding was reported, 0
otherwise ("warning" and "informational" findings do not affect exit
status).
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validators.catalog import CATALOG_ROOT
from validators.dependency_graph import to_json as graph_to_json
from validators.runner import run_all


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true", help="print the validation report as JSON")
    parser.add_argument("--graph", action="store_true", help="also print the dependency graph as JSON")
    parser.add_argument("--graph-out", metavar="FILE", help="write the dependency graph JSON to FILE instead of stdout")
    args = parser.parse_args()

    if not CATALOG_ROOT.is_dir():
        print(f"No execution-catalog directory found at {CATALOG_ROOT}")
        sys.exit(1)

    report = run_all()
    print(json.dumps(report.to_dict(), indent=2) if args.json else report.render_text())

    if args.graph or args.graph_out:
        graph_json = graph_to_json()
        if args.graph_out:
            Path(args.graph_out).write_text(graph_json + "\n", encoding="utf-8")
            print(f"\nDependency graph written to {args.graph_out}", file=sys.stderr)
        else:
            print("\n--- Dependency Graph (JSON) ---")
            print(graph_json)

    sys.exit(1 if report.totals_by_severity()["error"] else 0)


if __name__ == "__main__":
    main()
