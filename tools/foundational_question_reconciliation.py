"""Check the P13 foundational-question reconciliation against the live tree.

`FDR-1 §12` makes the 100-question set a reconciliation instrument. For each
question it asks whether the question is ALREADY SOLVED, PARTIAL, P13 CORE,
P13 FRONTIER, OUT OF SCOPE, FOUNDER RESERVED or UNKNOWN. The matrix is in
`docs/architecture/p13-preparation/P13-015-FOUNDATIONAL-QUESTION-RECONCILIATION.json`.
It is evidence for `FDR-2` and decides nothing.

A classification that cites nothing is an opinion. This module makes each
citation checkable, and re-checks it on every run:

```text
path::text      the text must appear in the file
!dir::regex     no .py file under dir may match: a measured absence
```

When the system changes, the check makes the matrix fail rather than drift.
For example, if an `Evaluation` capability is built, every "P13 CORE —
requires evaluation" row that cites the absence stops verifying.

Nothing here authorizes anything, and nothing here writes.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parents[1]
MATRIX = (REPO_ROOT / "docs/architecture/p13-preparation/"
          "P13-015-FOUNDATIONAL-QUESTION-RECONCILIATION.json")
CATEGORIES = ("ALREADY SOLVED", "PARTIAL", "P13 DEPENDENCY", "P13 CORE",
              "P13 FRONTIER", "OUT OF SCOPE", "FOUNDER RESERVED", "UNKNOWN")
# A claim that the system already answers a question must say where.
MUST_CITE = ("ALREADY SOLVED", "PARTIAL", "FOUNDER RESERVED")


def pointer_holds(pointer: str, root: Path = REPO_ROOT) -> bool:
    if pointer.startswith("!"):
        directory, _, pattern = pointer[1:].partition("::")
        rx = re.compile(pattern)
        return not any(rx.search(p.read_text(encoding="utf-8"))
                       for p in (root / directory).rglob("*.py")
                       if "__pycache__" not in p.parts)
    path, _, text = pointer.partition("::")
    target = root / path
    return target.is_file() and text in target.read_text(encoding="utf-8")


def verify(matrix: Path = MATRIX, root: Path = REPO_ROOT) -> Dict[str, object]:
    record = json.loads(matrix.read_text(encoding="utf-8"))
    questions = record["questions"]
    faults: List[str] = []
    ids = [q["id"] for q in questions]
    if ids != [f"Q{i}" for i in range(1, 101)]:
        faults.append("the matrix does not hold exactly Q1…Q100, in order")
    counts: Dict[str, int] = {}
    for q in questions:
        counts[q["category"]] = counts.get(q["category"], 0) + 1
        if q["category"] not in CATEGORIES:
            faults.append(f"{q['id']}: unknown category {q['category']!r}")
        if q["category"] in MUST_CITE and not q["evidence"]:
            faults.append(f"{q['id']}: {q['category']} cites no evidence")
        for pointer in q["evidence"]:
            if not pointer_holds(pointer, root):
                faults.append(f"{q['id']}: evidence no longer holds: {pointer}")
    return {"holds": not faults, "counts": counts, "faults": faults}


def main() -> int:
    result = verify()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["holds"] else 1


if __name__ == "__main__":
    import os, sys  # noqa: E401
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
