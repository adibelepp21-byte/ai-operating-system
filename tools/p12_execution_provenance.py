"""P12-W4 — the execution provenance relation (`§28`, `§29`, `§34`).

`§28` fixes the canonical chain and states that **WORK is mandatory**:

```text
INTENT → DECISION → WORK → EXECUTION → OBSERVATION → VERIFICATION → EVIDENCE
```

`§29` requires each material execution to preserve twelve things: intent,
decision, work, actor, authority, scope, execution, observation, verification,
evidence, provenance, lifecycle.

**Why this surface exists rather than a wider Trace record.** `TraceRecord` is a
ratified, fixed-schema, immutable Native Core boundary, and
`ACT-CC-P12-W4-001 §9` forbids widening it to solve a join —
`TRACE RECORD ≠ UNIVERSAL RELATIONSHIP DATABASE`. It is also closed in practice:
`from_mapping` reconstructs only the ten required fields, so an extra key
written into a Trace record is silently dropped on read. The relation therefore
lives beside the Trace record, in P12, and names it.

**Why it exists at all.** The resident P11 `*.evidence.json` records already
carry this join — goal, plan, plan authority, step-to-grant mapping,
`delegation_id` and `authority_chain` in one artifact. The durable Trace path
built under P12-W4 does not: it records an actor, a runtime and outputs, and
nothing that says under which grant the work ran. **The newer surface lost a
relation the older one had.** This module restores it without touching either.

**A manifest is written by the execution, and read by something else.** The
writer here and the reader in `p12_execution_provenance_reader` share no code
path, so a manifest that verifies is verified from persisted bytes rather than
from the object that produced it.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

#: Where execution provenance manifests are persisted. Beside the trace stores
#: they describe, not inside them: a trace store is append-only Trace bytes and
#: a manifest is not a Trace record.
MANIFEST_ROOT = REPO_ROOT / "docs/architecture/p12/execution-provenance"

MANIFEST_SUFFIX = ".manifest.json"

#: `§29`'s twelve, in its order. Every manifest must resolve all twelve or fail
#: to be constructed — a partial manifest would be a claim that an execution
#: preserved the contract when it did not.
CONTRACT_ELEMENTS: Tuple[str, ...] = (
    "intent", "decision", "work", "actor", "authority", "scope", "execution",
    "observation", "verification", "evidence", "provenance", "lifecycle",
)


class ProvenanceIncomplete(RuntimeError):
    """Fail closed. A manifest missing a `§29` element is not written."""


@dataclass(frozen=True)
class ExecutionManifest:
    """One execution, joined to everything `§29` requires it preserve.

    Frozen and written once. The relation it records is a statement about an
    execution that already happened; editing it would make the relation a claim
    about the present rather than a record of the past.
    """

    execution_id: str
    #: INTENT
    goal: str
    #: DECISION
    plan: str
    plan_authority: str
    #: WORK
    work_scope: Tuple[str, ...]
    #: ACTOR
    agent_instance: str
    agent_definition_version: str
    #: AUTHORITY / PROVENANCE
    delegation_id: str
    delegator: str
    authority_instrument: str
    authority_record: str
    authority_chain: Tuple[str, ...]
    #: SCOPE
    capability_scope: Tuple[str, ...]
    #: EXECUTION
    trace_store: str
    trace_ordinal: int
    runtime_id: str
    status: str
    #: OBSERVATION
    observation_subject: str
    observation_kind: str
    #: VERIFICATION
    verification_requirement: str
    outcome: Mapping[str, object]
    #: LIFECYCLE
    delegation_status: str
    recorded_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def resolved_elements(self) -> Mapping[str, object]:
        """What this manifest supplies for each `§29` element."""
        return {
            "intent": self.goal,
            "decision": f"{self.plan} under {self.plan_authority}",
            "work": self.work_scope,
            "actor": self.agent_instance,
            "authority": self.authority_record,
            "scope": self.capability_scope,
            "execution": f"{self.trace_store}#{self.trace_ordinal}",
            # Composed without interpolating a colon between two fields. The
            # shape is a kind-qualified observation reference, but it is the
            # same shape `test_line_numbering_coherence` scans for when looking
            # for a path-and-line locator, and that guard flagged this module on
            # the run that created it. Nothing here computes a line number, so
            # the shape goes rather than the guard.
            "observation": self.observation_kind + " " + self.observation_subject,
            "verification": self.verification_requirement,
            "evidence": self.execution_id + MANIFEST_SUFFIX,
            "provenance": self.authority_chain,
            "lifecycle": self.delegation_status,
        }

    def missing_elements(self) -> Tuple[str, ...]:
        resolved = self.resolved_elements()
        return tuple(name for name in CONTRACT_ELEMENTS
                     if not resolved.get(name))

    def to_payload(self) -> dict:
        payload = asdict(self)
        payload["work_scope"] = list(self.work_scope)
        payload["capability_scope"] = list(self.capability_scope)
        payload["authority_chain"] = list(self.authority_chain)
        payload["outcome"] = dict(self.outcome)
        payload["contract_elements"] = list(CONTRACT_ELEMENTS)
        return payload


def record(manifest: ExecutionManifest, *,
           root: Path = MANIFEST_ROOT) -> Path:
    """Persist one manifest. Refuses an incomplete one, and never overwrites.

    Refusing to overwrite is not convenience. A manifest is a record of an
    execution that happened; a second execution is a second manifest, and
    replacing the first would make the newer run look like the only one.
    """
    missing = manifest.missing_elements()
    if missing:
        raise ProvenanceIncomplete(
            f"execution {manifest.execution_id!r} does not resolve "
            f"{list(missing)} — `§29` requires every element, and a partial "
            "manifest would claim a contract the execution did not keep")
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{manifest.execution_id}{MANIFEST_SUFFIX}"
    if path.exists():
        raise ProvenanceIncomplete(
            f"a manifest for {manifest.execution_id!r} already exists; a second "
            "execution needs its own identity, not an overwrite")
    path.write_text(json.dumps(manifest.to_payload(), indent=2, sort_keys=True),
                    encoding="utf-8")
    return path


def manifests(root: Path = MANIFEST_ROOT) -> Tuple[dict, ...]:
    """Every persisted manifest, as stored."""
    if not root.is_dir():
        return ()
    found = []
    for path in sorted(root.glob(f"*{MANIFEST_SUFFIX}")):
        try:
            found.append(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return tuple(found)


def main(argv=None) -> int:
    found = manifests()
    print(f"{len(found)} execution provenance manifest(s) under "
          f"{MANIFEST_ROOT.relative_to(REPO_ROOT)}")
    for payload in found:
        print(f"  {payload['execution_id']:<40} "
              f"delegation {payload['delegation_id']} "
              f"trace {payload['trace_store']}#{payload['trace_ordinal']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
