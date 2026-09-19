"""`ACT-CC-P12-015 §19` — independent verification of the `P6` admission chain.

**This module imports nothing from `tools.p12_knowledge_admission`.** `§19`
closes with *"the verifier must not simply trust the admission writer"*, and a
verifier that called the writer's own resolver could not tell *"the candidate's
identity is X"* from *"the writer says the candidate's identity is X"*. The
independence is enforced structurally by
`tools/tests/test_p12_knowledge_admission.py`, which reads this file's imports
by AST — the same discipline `p12_phase_authorization_verifier` is held to.

Every one of the ten checks derives its own answer from a primary source:

```text
1  candidate identity        this module's own parse of the work's source
2  admitted version          the Native Core Knowledge store, read canonically
3  provenance                the append-only provenance partition, read raw
4  Founder authorization     this module's own parse of the instrument
5  HumanAuthority            the append-only Governance decision log, read raw
6  Active Knowledge state    KnowledgeRetrieval.active — the canonical surface
7  actual consumer path      AST of the consumer, not its output
8  real system work          durable Trace records, attributed structurally
9  captured observation      the Trace record's own captured content (INV-6)
10 fresh-process reproducibility  a child interpreter that shares no object
```

**What it deliberately does not do.** It never admits, records a decision, or
constructs a `HumanAuthority` — reading one out of a log is not holding one. It
writes nothing anywhere. And it reports `UNSATISFIED` rather than raising when
a check fails, because `§19` asks what is true, and a verifier that cannot
report a failure has not verified anything.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from collections.abc import Mapping
from typing import Any, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

SATISFIED = "SATISFIED"
UNSATISFIED = "UNSATISFIED"
UNRESOLVED = "UNRESOLVED"

#: Primary sources, named here so this module resolves them itself rather than
#: asking the writer where it put them.
WORK_SOURCE = Path("aios_corpus_health_run.py")
ACTS_ROOT = Path("docs/governance/acts")
KNOWLEDGE_ROOT = Path("docs/architecture/p12/aios-runtime-store")
DECISIONS = Path("docs/architecture/p12/governance-decisions/governance_decisions")
PROVENANCE = Path("docs/architecture/p12/knowledge-admissions/admission_provenance")
TRACE_STORE = Path("docs/architecture/p12/trace-stores/aios-corpus-health")

ITEM_KEY = "corpus-health.criteria"

#: This module's own recognisers, written independently of the reader's: a
#: single authentication block located by its heading and the next heading,
#: rather than a general section split.
_AUTH_BLOCK = re.compile(
    r"^\d+\.\s+FOUNDER AUTHENTICATION\s*$(.*?)(?=^\d+\.\s+\S|\Z)", re.M | re.S)
_FIELD = re.compile(r"^(?P<label>[A-Za-z][^:\n]*):[ \t]*(?P<inline>\S[^\n]*)?$",
                    re.M)

#: `CRITERIA_CONTENT = { ... }` in the work's source, matched as text. The
#: writer reads it by AST; this reads the braces. Two different parses of the
#: same bytes disagreeing is exactly the signal independence is for.
_CRITERIA = re.compile(r"^CRITERIA_CONTENT\s*=\s*\{(?P<body>.*?)^\}", re.M | re.S)
_ENTRY = re.compile(r'"(?P<key>[^"]+)"\s*:\s*(?P<value>[^,\n]+),')


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str


def _canonical(value: Any) -> bytes:
    return json.dumps(_plain(value), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    return value


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


# -- primary sources, each read this module's own way -----------------------

def declared_criteria(root: Path = REPO_ROOT) -> Optional[dict]:
    """The criteria as written in the work's source, by text, not by AST."""
    source = root / WORK_SOURCE
    if not source.is_file():
        return None
    match = _CRITERIA.search(source.read_text(encoding="utf-8"))
    if match is None:
        return None
    resolved = {}
    for entry in _ENTRY.finditer(match.group("body")):
        raw = entry.group("value").strip()
        if raw.isdigit():
            resolved[entry.group("key")] = int(raw)
        elif raw.startswith('"') and raw.endswith('"'):
            resolved[entry.group("key")] = raw[1:-1]
        elif raw == "KNOWLEDGE_KEY":
            # The one name the literal uses. Resolve it from its own
            # declaration in the same file, by the same textual reading.
            named = re.search(r'^KNOWLEDGE_KEY\s*=\s*"([^"]+)"\s*$',
                              source.read_text(encoding="utf-8"), re.M)
            if named is None:
                return None
            resolved[entry.group("key")] = named.group(1)
        else:
            return None
    return resolved or None


def stated_authorization(root: Path = REPO_ROOT) -> Optional[dict]:
    """The Founder authentication block, found by this module's own parse."""
    directory = root / ACTS_ROOT
    if not directory.is_dir():
        return None
    found = []
    for path in sorted(directory.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        block = _AUTH_BLOCK.search(text)
        if block is None:
            continue
        fields: dict = {}
        lines = block.group(1).split("\n")
        for index, line in enumerate(lines):
            field = _FIELD.match(line)
            if field is None:
                continue
            label = field.group("label").strip()
            inline = (field.group("inline") or "").strip()
            if inline:
                fields.setdefault(label, inline)
                continue
            for nxt in lines[index + 1:]:
                if nxt.strip():
                    if _FIELD.match(nxt):
                        break
                    fields.setdefault(label, nxt.strip())
                    break
        if fields.get("Decision") != "APPROVED FOR KNOWLEDGE ADMISSION":
            continue
        fields["_instrument"] = path.relative_to(root).as_posix()
        found.append(fields)
    return found[0] if len(found) == 1 else None


def recorded_decisions(root: Path = REPO_ROOT) -> Tuple[dict, ...]:
    """The durable Governance audit log, read raw."""
    return _jsonl(root / DECISIONS)


def provenance_records(root: Path = REPO_ROOT) -> Tuple[dict, ...]:
    return _jsonl(root / PROVENANCE)


def _jsonl(path: Path) -> Tuple[dict, ...]:
    if not path.is_file():
        return ()
    out = []
    for line in path.read_text(encoding="utf-8").split("\n"):
        if line.strip():
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
    return tuple(out)


def active_version(root: Path = REPO_ROOT) -> Optional[dict]:
    """The Active version through the canonical retrieval surface.

    Read through Native Core, not through the admission tool: `Active` is
    *derived* from the append-only sequence by `KnowledgeVersioning`, and
    deriving it here a second way would be this module inventing a status.
    """
    from native_core.core.infrastructure import LocalAppendOnlyStorage
    from native_core.core.knowledge.composition import create_knowledge_subsystem

    base = root / KNOWLEDGE_ROOT / "native_core_storage"
    if not base.is_dir():
        return None
    storage = LocalAppendOnlyStorage(base)
    storage.provision()
    subsystem = create_knowledge_subsystem(storage)
    version = subsystem.retrieval.active(ITEM_KEY)
    if version is None:
        return None
    return {"knowledge_item_key": version.identity.knowledge_item_key,
            "version_sequence": version.identity.version_sequence,
            "content": _plain(version.content)}


def trace_records(root: Path = REPO_ROOT):
    from native_core.core.infrastructure import LocalAppendOnlyStorage
    from native_core.core.trace import TraceReader

    store = root / TRACE_STORE
    if not store.is_dir():
        return ()
    storage = LocalAppendOnlyStorage(store)
    storage.provision()
    return tuple(TraceReader(storage).read())


# -- `§19`'s ten checks ------------------------------------------------------

def _candidate_identity(root: Path) -> Check:
    declared = declared_criteria(root)
    if declared is None:
        return Check("1 candidate identity", UNRESOLVED,
                     f"{WORK_SOURCE} declares no readable criteria literal")
    provenance = provenance_records(root)
    if not provenance:
        return Check("1 candidate identity", UNRESOLVED,
                     "no admission provenance has been recorded")
    claimed = provenance[-1].get("candidate_immutable_identity")
    mine = _digest(declared)
    if claimed != mine:
        return Check("1 candidate identity", UNSATISFIED,
                     f"provenance claims {claimed}; independently computed "
                     f"{mine} over {sorted(declared)}")
    return Check("1 candidate identity", SATISFIED,
                 f"{WORK_SOURCE}:CRITERIA_CONTENT hashes to {mine}")


def _admitted_version(root: Path) -> Check:
    provenance = provenance_records(root)
    if not provenance:
        return Check("2 admitted version", UNRESOLVED, "no provenance recorded")
    identity = provenance[-1].get("resulting_knowledge_identity") or {}
    version = active_version(root)
    if version is None:
        return Check("2 admitted version", UNSATISFIED,
                     "provenance records an admission but the Knowledge store "
                     "holds no Active version for it")
    if (identity.get("knowledge_item_key") != version["knowledge_item_key"]
            or identity.get("version_sequence") != version["version_sequence"]):
        return Check("2 admitted version", UNSATISFIED,
                     f"provenance names {identity}; the store holds "
                     f"({version['knowledge_item_key']}, "
                     f"{version['version_sequence']})")
    return Check("2 admitted version", SATISFIED,
                 f"version {version['version_sequence']} of "
                 f"{version['knowledge_item_key']!r} is in the store")


def _provenance(root: Path) -> Check:
    """`§8`'s nine elements, each present and non-empty."""
    required = ("candidate_artifact", "candidate_immutable_identity",
                "source_location", "decision_instrument", "founder_authority",
                "admission_action", "admission_timestamp",
                "resulting_knowledge_identity")
    records = provenance_records(root)
    if not records:
        return Check("3 provenance", UNRESOLVED, "no provenance recorded")
    record = records[-1]
    missing = [name for name in required if not record.get(name)]
    if missing:
        return Check("3 provenance", UNSATISFIED,
                     f"provenance omits {missing}")
    # `candidate_version` is required to be *present* and is legitimately
    # null: a candidate holds no version until admission allocates one.
    if "candidate_version" not in record:
        return Check("3 provenance", UNSATISFIED,
                     "provenance does not address the candidate's version")
    return Check("3 provenance", SATISFIED,
                 f"{len(required) + 1} elements recorded, written at "
                 f"{record['admission_timestamp']}")


def _founder_authorization(root: Path) -> Check:
    stated = stated_authorization(root)
    if stated is None:
        return Check("4 Founder authorization", UNRESOLVED,
                     "no single instrument states an admission approval")
    for label, expected in (("Admission", "AUTHORIZED"),
                            ("Status", "FINAL / ISSUED")):
        if stated.get(label) != expected:
            return Check("4 Founder authorization", UNSATISFIED,
                         f"{stated['_instrument']} states {label}="
                         f"{stated.get(label)!r}, not {expected!r}")
    records = provenance_records(root)
    if records and records[-1].get("decision_instrument") != stated["_instrument"]:
        return Check("4 Founder authorization", UNSATISFIED,
                     f"the admission cites {records[-1].get('decision_instrument')!r}; "
                     f"the issued instrument is {stated['_instrument']!r}")
    return Check("4 Founder authorization", SATISFIED,
                 f"{stated['_instrument']} — Admission: AUTHORIZED, "
                 "Status: FINAL / ISSUED")


def _human_authority(root: Path) -> Check:
    stated = stated_authorization(root)
    if stated is None:
        return Check("5 HumanAuthority", UNRESOLVED, "no issued instrument")
    reviewer = (stated.get("HumanAuthority") or "").strip()
    if not reviewer:
        return Check("5 HumanAuthority", UNSATISFIED,
                     f"{stated['_instrument']} names no human authority")
    approvals = [d for d in recorded_decisions(root)
                 if d.get("scope") == ITEM_KEY and d.get("decision") == "approve"]
    if not approvals:
        return Check("5 HumanAuthority", UNSATISFIED,
                     f"no approve decision for {ITEM_KEY!r} is on record")
    wrong = [d for d in approvals if d.get("reviewer_id") != reviewer]
    if wrong:
        return Check("5 HumanAuthority", UNSATISFIED,
                     f"{len(wrong)} recorded approval(s) name a reviewer other "
                     f"than the instrument's {reviewer!r}")
    if any(not (d.get("rationale") or "").strip() for d in approvals):
        return Check("5 HumanAuthority", UNSATISFIED,
                     "a recorded approval carries no rationale")
    return Check("5 HumanAuthority", SATISFIED,
                 f"{len(approvals)} approval(s) recorded, reviewer {reviewer!r}, "
                 "each carrying a rationale")


def _active_state(root: Path) -> Check:
    version = active_version(root)
    if version is None:
        return Check("6 Active Knowledge", UNSATISFIED,
                     f"no Active version for {ITEM_KEY!r}")
    declared = declared_criteria(root)
    if declared is None:
        return Check("6 Active Knowledge", UNRESOLVED,
                     "the candidate source is unreadable")
    if _digest(version["content"]) != _digest(declared):
        return Check("6 Active Knowledge", UNSATISFIED,
                     "the Active content differs from the repository candidate")
    return Check("6 Active Knowledge", SATISFIED,
                 f"Active is ({ITEM_KEY}, {version['version_sequence']}) and its "
                 "content matches the repository candidate byte for byte")


#: The call chain the consumer must actually contain. `§15` fixes it, and an
#: AST walk is the only reading that cannot be satisfied by a comment.
def _consumer_path(root: Path) -> Check:
    source = root / WORK_SOURCE
    if not source.is_file():
        return Check("7 consumer path", UNRESOLVED, f"{WORK_SOURCE} is absent")
    tree = ast.parse(source.read_text(encoding="utf-8"))
    calls = {n.func.attr for n in ast.walk(tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
    names = {n.func.id for n in ast.walk(tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    attributes = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    required_call = "create_execution_layer" in names
    reaches = {"runtime", "knowledge", "retrieval"} <= attributes
    reads_active = "active" in calls
    if not (required_call and reaches and reads_active):
        return Check("7 consumer path", UNSATISFIED,
                     f"execution layer={required_call} · "
                     f"runtime.knowledge.retrieval={reaches} · "
                     f"active()={reads_active}")
    # `§15`: the worker must not substitute a local threshold. The criteria
    # literal must be inert — declared, never read by the work.
    read_names = [n.id for n in ast.walk(tree)
                  if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)]
    if "CRITERIA_CONTENT" in read_names:
        return Check("7 consumer path", UNSATISFIED,
                     "the work reads its local CRITERIA_CONTENT, so Knowledge "
                     "is not the source of the criteria it judges against")
    return Check("7 consumer path", SATISFIED,
                 "create_execution_layer → runtime.knowledge.retrieval.active, "
                 "and the local criteria literal is never read by the work")


#: Executions written to show a surface rather than to perform system work.
#: Named because the distinction is material; the same three the resident
#: cross-phase verifier names.
_DEMONSTRATORS = ("p12-w4-durability-proof", "p12-f4-runtime-observation",
                  "p12-f11-workflow-observation")


def _real_system_work(root: Path) -> Check:
    records = [r for r in trace_records(root) if r.knowledge_consumed]
    if not records:
        return Check("8 real system work", UNSATISFIED,
                     "no Trace record in the corpus-health store consumed "
                     "Knowledge")
    demonstrator = [r for r in records
                    if any(d in (r.runtime or "") for d in _DEMONSTRATORS)]
    if demonstrator:
        return Check("8 real system work", UNSATISFIED,
                     f"{len(demonstrator)} of {len(records)} Knowledge-consuming "
                     "records were authored by a demonstrator")
    runtimes = sorted({r.runtime for r in records if r.runtime})
    actors = sorted({r.agent_instance for r in records if r.agent_instance})
    if not runtimes or not actors:
        return Check("8 real system work", UNSATISFIED,
                     "a Knowledge-consuming record names no runtime or no actor")
    return Check("8 real system work", SATISFIED,
                 f"{len(records)} record(s) from {runtimes} authored by {actors}")


def _captured_evidence(root: Path) -> Check:
    """`INV-6` — the record must hold *content*, not a key it points at."""
    version = active_version(root)
    records = [r for r in trace_records(root) if r.knowledge_consumed]
    if not records:
        return Check("9 captured evidence", UNSATISFIED,
                     "no Knowledge consumption is recorded")
    captured = []
    for record in records:
        for entry in record.knowledge_consumed:
            if not isinstance(entry, Mapping):
                return Check("9 captured evidence", UNSATISFIED,
                             f"an entry is {type(entry).__name__}, not captured "
                             "content — INV-6 requires capture, not reference")
            content = entry.get("content")
            if not isinstance(content, Mapping):
                return Check("9 captured evidence", UNSATISFIED,
                             "an entry carries no captured content")
            captured.append(_plain(content))
    if version is not None and not any(
            _digest(c) == _digest(version["content"]) for c in captured):
        return Check("9 captured evidence", UNSATISFIED,
                     "no captured content matches the Active version")
    return Check("9 captured evidence", SATISFIED,
                 f"{len(captured)} captured Knowledge payload(s), matching the "
                 "Active version")


_PROBE = (
    "import json,sys;"
    "sys.path.insert(0, %r);"
    "from native_core.core.infrastructure import LocalAppendOnlyStorage;"
    "from native_core.core.knowledge.composition import create_knowledge_subsystem;"
    "s=LocalAppendOnlyStorage(%r);s.provision();"
    "v=create_knowledge_subsystem(s).retrieval.active(%r);"
    "print(json.dumps(None if v is None else "
    "{'seq': v.identity.version_sequence, 'content': dict(v.content)}))"
)


def _fresh_process(root: Path) -> Check:
    """`§19.10` — a child interpreter, sharing no object with this one."""
    base = root / KNOWLEDGE_ROOT / "native_core_storage"
    try:
        completed = subprocess.run(
            [sys.executable, "-c",
             _PROBE % (str(root), str(base), ITEM_KEY)],
            capture_output=True, text=True, check=True, cwd=str(root))
    except (OSError, subprocess.CalledProcessError) as exc:
        return Check("10 fresh process", UNRESOLVED,
                     f"the probe did not complete: {exc}")
    try:
        observed = json.loads(completed.stdout.strip() or "null")
    except ValueError:
        return Check("10 fresh process", UNRESOLVED,
                     f"unreadable probe output: {completed.stdout!r}")
    if observed is None:
        return Check("10 fresh process", UNSATISFIED,
                     "a fresh process sees no Active version")
    mine = active_version(root)
    if mine is None or _digest(observed["content"]) != _digest(mine["content"]):
        return Check("10 fresh process", UNSATISFIED,
                     "a fresh process sees different content")
    return Check("10 fresh process", SATISFIED,
                 f"a child interpreter reads version {observed['seq']} with "
                 "identical content")


_CHECKS = (_candidate_identity, _admitted_version, _provenance,
           _founder_authorization, _human_authority, _active_state,
           _consumer_path, _real_system_work, _captured_evidence,
           _fresh_process)


def verify(root: Path = REPO_ROOT) -> Tuple[Check, ...]:
    """`§19`'s ten items, each established from a primary source."""
    return tuple(check(root) for check in _CHECKS)


def summary(root: Path = REPO_ROOT) -> dict:
    checks = verify(root)
    return {
        "checks": len(checks),
        "satisfied": sum(1 for c in checks if c.status == SATISFIED),
        "unsatisfied": sum(1 for c in checks if c.status == UNSATISFIED),
        "unresolved": sum(1 for c in checks if c.status == UNRESOLVED),
        "failing": tuple(c.name for c in checks if c.status != SATISFIED),
    }


def main(argv=None) -> int:
    for check in verify():
        print(f"{check.status:<12} {check.name:<28} {check.detail}")
    print()
    print("summary:", summary())
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
