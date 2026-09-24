"""Are the ecosystem's relationships actually connected? Measured, not asserted.

Built under `GOAL-V2-005 §14`, which asks whether these relationships are
*"actually connected and operational"*:

```text
Knowledge ↔ Memory ↔ Intelligence ↔ Capability ↔ Workflow ↔ Organization
          ↔ Governance ↔ Founder Decision
```

The chain is the P13 corpus's own question (F1 `§5`, and `§17` *Systemic
Intelligence*). **Answering it does not define P13, and nothing here
constructs P13.** It measures the system that exists, so that whoever decides
what P13 is decides from evidence. Every run recomputes from the tree:

| Binding | Evidence it takes |
|---|---|
| `CODE` | an import between the two nodes' resident modules, either direction, read from the syntax tree |
| `DATA` | resident records on one side that name or resolve the other (for example, escalations whose `authority_record` reaches a registered Founder Decision) |
| `MEDIATED` | no direct binding; the two nodes connect only through a third node, which is named |
| `NOT CONNECTED` | none of the above. Where the codebase records *why*, the reason is quoted, and the quote is re-checked in its file on every run, so a stale reason fails instead of persisting |

**Node membership is declared, and it is the only judgement in this module.**
Each node lists the resident modules that realize it, with the phase that owns
them. A different membership would give a different map. That is why the
membership is printed with every result, and not hidden.

Nothing here authorizes anything, and nothing here writes.
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

CHAIN: Tuple[str, ...] = (
    "Knowledge", "Memory", "Intelligence", "Capability", "Workflow",
    "Organization", "Governance", "FounderDecision",
)

# Node → (owning phase, resident module prefixes). Declared; see the docstring.
NODES: Dict[str, Tuple[str, Tuple[str, ...]]] = {
    "Knowledge": ("P6", ("native_core.core.knowledge", "consumers.knowledge_agent")),
    "Memory": ("P7", ("native_core.core.memory", "consumers.memory_agent")),
    "Intelligence": ("P5", ("consumers.cognitive_intelligence_agent",
                            "consumers.engineering_intelligence_agent")),
    "Capability": ("P1–P8 core", ("native_core.core.capability",
                                  "native_core.core.skill")),
    "Workflow": ("P9 (+ P11 bridge)", ("native_core.core.workflow",
                                       "consumers.workflow_agent",
                                       "tools.plan_to_workflow")),
    "Organization": ("P10–P11", ("tools.organization_catalog", "tools.planning",
                                 "tools.agent_instance_registry",
                                 "tools.w4_delegation", "tools.w4_execution",
                                 "tools.w4_first_run", "tools.w1_coordination_run",
                                 "tools.w1_cross_department_run")),
    "Governance": ("core + P11–P12", ("native_core.core.governance",
                                      "tools.escalation_register",
                                      "tools.p12_governance_escalation_join")),
    "FounderDecision": ("governance corpus", ("tools.p12_certified_evidence_guard",
                                              "tools.p12_phase_authorization",
                                              "tools.authority_citation",
                                              "tools.governance_delegation_register")),
}

# Recorded reasons a relationship is absent. Each is (file, exact phrase),
# whitespace-normalized, and is re-verified against the file on every run.
RECORDED_ABSENCE: Dict[Tuple[str, str], Tuple[Tuple[str, str], ...]] = {
    ("Memory", "Intelligence"): (
        ("consumers/cognitive_intelligence_agent.py",
         "No Knowledge, no Governance, no Memory"),
        ("consumers/engineering_intelligence_agent.py",
         "Nothing from Knowledge, Governance, Memory"),
    ),
    ("Capability", "Workflow"): (
        ("native_core/core/workflow/__init__.py",
         "Workflow↔Skill relationship"),
        ("native_core/core/workflow/__init__.py",
         "Inferred relationships are NOT frozen.\"* Not modelled."),
    ),
}

CONNECTED_CODE = "CODE"
CONNECTED_DATA = "DATA"
MEDIATED = "MEDIATED"
NOT_CONNECTED = "NOT CONNECTED"


@dataclass
class Relationship:
    left: str
    right: str
    status: str
    code: List[str] = field(default_factory=list)
    data: List[str] = field(default_factory=list)
    mediated_by: List[str] = field(default_factory=list)
    recorded_reason: List[str] = field(default_factory=list)
    stale_reason: List[str] = field(default_factory=list)


def _tracked_python(root: Path) -> List[str]:
    out = subprocess.run(["git", "ls-files", "*.py"], cwd=str(root),
                         capture_output=True, text=True, check=True).stdout
    return [n for n in out.split() if "/tests/" not in n
            and not n.startswith("docs/")]


def _module(name: str) -> str:
    return name[:-3].replace("/", ".").replace(".__init__", "")


def _imports(root: Path) -> Dict[str, Set[str]]:
    graph: Dict[str, Set[str]] = {}
    for name in _tracked_python(root):
        module = _module(name)
        package = module.split(".")
        if not name.endswith("__init__.py"):
            package = package[:-1]
        found: Set[str] = set()
        tree = ast.parse((root / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                found |= {a.name for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    base = package[:len(package) - node.level + 1]
                    target = ".".join(base + ([node.module] if node.module else []))
                else:
                    target = node.module or ""
                found.add(target)
                found |= {f"{target}.{a.name}" for a in node.names}
        graph[module] = found
    return graph


def _member(module: str, node: str) -> bool:
    return any(module == p or module.startswith(p + ".") for p in NODES[node][1])


def code_bindings(graph: Dict[str, Set[str]], a: str, b: str) -> List[str]:
    edges = []
    for source, targets in sorted(graph.items()):
        for x, y in ((a, b), (b, a)):
            if _member(source, x):
                hits = sorted({t for t in targets if _member(t, y)})
                if hits:
                    edges.append(f"{source} → {hits[0]}")
    return sorted(set(edges))


def _records(root: Path, pattern: str) -> List[Tuple[Path, dict]]:
    found = []
    for base in (root / "docs/architecture", root / "docs/operations"):
        for path in sorted(base.rglob(pattern)):
            try:
                found.append((path, json.loads(path.read_text(encoding="utf-8"))))
            except (OSError, ValueError):
                continue
    return found


def data_bindings(root: Path, a: str, b: str) -> List[str]:
    """Resident records that bind the two nodes, computed each run."""
    from tools import authority_citation
    pair = {a, b}
    out: List[str] = []
    if pair == {"Governance", "FounderDecision"}:
        records = _records(root, "*.escalation.json")
        reached = [p for p, r in records if r.get("authority_record") and
                   authority_citation.refusal(
                       r.get("authority_instrument", ""), r["authority_record"],
                       "FD-P11-001", repo_root=root) is None]
        if reached:
            out.append(f"{len(reached)}/{len(records)} escalation records cite "
                       "a Founder Decision that resolves in the Register "
                       "(FD-P11-001)")
    if pair == {"Organization", "FounderDecision"}:
        records = (_records(root, "*.delegation.json")
                   + _records(root, "*.instance.json"))
        reached = [p for p, r in records if r.get("authority_record") and
                   authority_citation.refusal(
                       r.get("authority_instrument", ""), r["authority_record"],
                       "FD-P11-001", repo_root=root) is None]
        if reached:
            out.append(f"{len(reached)}/{len(records)} delegation/instance "
                       "records reach FD-P11-001")
    if pair == {"Intelligence", "Capability"}:
        from tools import organization_catalog as org
        departments = org.read_departments(
            root / org.ORGANIZATION_ROOT.relative_to(org.REPO_ROOT))
        declared = sorted({c for d in departments for c in d.capabilities
                           if c in ("cognitive-intelligence",
                                    "engineering-intelligence")})
        if declared:
            out.append("the P5 intelligence capabilities are declared as "
                       f"Department capabilities: {', '.join(declared)}")
    if pair == {"Organization", "Intelligence"}:
        instances = [p.name for p, r in _records(root, "*.instance.json")
                     if "intelligence" in str(r.get("agent_definition_key", ""))]
        if instances:
            out.append(f"{len(instances)} registered Agent Instances realize an "
                       "intelligence Agent Definition")
    if pair == {"Organization", "Governance"}:
        records = _records(root, "*.escalation.json")
        if records:
            out.append(f"{len(records)} escalation records raised by "
                       "organizational execution")
    return out


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def recorded_reasons(root: Path, a: str, b: str) -> Tuple[List[str], List[str]]:
    held, stale = [], []
    for key in ((a, b), (b, a)):
        for relative, phrase in RECORDED_ABSENCE.get(key, ()):
            path = root / relative
            text = path.read_text(encoding="utf-8") if path.is_file() else ""
            target = held if _normalized(phrase) in _normalized(text) else stale
            target.append(f"{relative}: “{phrase}”")
    return held, stale


def measure(root: Path = REPO_ROOT,
            chain: Sequence[str] = CHAIN) -> List[Relationship]:
    graph = _imports(root)
    direct: Dict[frozenset, Tuple[List[str], List[str]]] = {}
    names = list(NODES)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            direct[frozenset((a, b))] = (code_bindings(graph, a, b),
                                         data_bindings(root, a, b))
    results = []
    for a, b in zip(chain, chain[1:]):
        code, data = direct[frozenset((a, b))]
        mediators = [x for x in names if x not in (a, b)
                     and any(direct[frozenset((a, x))])
                     and any(direct[frozenset((x, b))])]
        held, stale = recorded_reasons(root, a, b)
        status = (CONNECTED_CODE if code else CONNECTED_DATA if data
                  else MEDIATED if mediators else NOT_CONNECTED)
        results.append(Relationship(a, b, status, code, data,
                                    [] if code or data else mediators,
                                    held, stale))
    return results


def report(root: Path = REPO_ROOT) -> dict:
    relationships = measure(root)
    return {
        "chain": list(CHAIN),
        "membership": {k: {"phase": v[0], "modules": list(v[1])}
                       for k, v in NODES.items()},
        "relationships": [asdict(r) for r in relationships],
        "summary": {s: sum(r.status == s for r in relationships)
                    for s in (CONNECTED_CODE, CONNECTED_DATA, MEDIATED,
                              NOT_CONNECTED)},
        "stale_reasons": sum(len(r.stale_reason) for r in relationships),
    }


def main() -> int:
    result = report()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["stale_reasons"] == 0 else 1


if __name__ == "__main__":
    import os, sys  # noqa: E401
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
