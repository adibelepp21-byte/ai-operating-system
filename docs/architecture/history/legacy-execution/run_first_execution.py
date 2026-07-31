#!/usr/bin/env python3
"""
Runs an execution of the AIOS harness: Agent Definition
(governance-artifact-integrity-agent) -> Agent Instance -> Runtime ->
Workflow -> Skill -> Tool -> Result -> Trace.

Entirely self-contained; reads real repository files under docs/ and
writes only to execution/traces/. Never touches docs/.

Usage:
    python3 execution/run_first_execution.py
    python3 execution/run_first_execution.py --runtime runtime.interactive-governance-session-substrate
    python3 execution/run_first_execution.py --target /path/to/some/document.md
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from execution import orchestrator


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runtime", default=None, help="Runtime canonical key to bind explicitly (default: deterministic first-match)")
    parser.add_argument("--target", default=None, help="Target document path for Skill invocation (default: the Agent Definition itself)")
    args = parser.parse_args()

    try:
        result = orchestrator.run(target_document=args.target, runtime_selector=args.runtime)
    except orchestrator.AuthorizationError as exc:
        print(json.dumps({"status": "escalation", "error": str(exc)}, indent=2))
        return

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
