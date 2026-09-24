"""`StateUnderstanding` — OBSERVE / UNDERSTAND (E13-01; `D03` q1).

*What state am I in?* Each source declares the facts it answers **before** it is
read. A source that cannot be read therefore still yields its facts, marked
`UNKNOWN` with the reason, and never drops them (E13-01's negative control).

**Memory is a source, and it is material** (`D06`, `P13-018 §7`). P13 reads
Memory only through `MemoryReader`, over Trace, which is how Memory is defined
(Memory is derived on read from Trace). It reads the P12 stores and its own
Trace store. It never admits, promotes or writes Memory, and Memory stays P7's.
Three things in a cycle rest on it:

* what P13 verified in earlier cycles comes back as `INFERRED` evidence, so a
  criterion can be judged, with lower certainty, without re-running everything;
* *"what changed since the last cycle?"*, which has no other source;
* which verification is least recently done, which orders the next action.

Remove the Memory source and all three become `UNKNOWN`.

The Knowledge read is `FD-P12-002`'s corpus-health criteria, admitted to P13
**read-only** by `P13-018` `D-3`. It is read through the Knowledge subsystem's
own retrieval, and it is never written.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Iterable, Optional, Tuple

from tools.p12_self_model import QUESTIONS
from tools.p13.model import (INFERRED, UNKNOWN, VERIFIED, Fact, StateSnapshot)
from tools.p13.paths import Paths

P13_INSTANCE = "aios-p13-ecosystem"
KNOWLEDGE_KEY = "corpus-health.criteria"

Reading = Dict[str, Tuple[Any, str]]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Source:
    name: str
    describe: str
    keys: Tuple[str, ...]
    read: Callable[[Paths, "Context"], Reading]


@dataclass
class Context:
    """What earlier sources in the same observation found (Memory, mainly)."""

    previous: Optional[dict] = None
    memory_available: bool = False


# -- the sources ------------------------------------------------------------

def _slug(question: str) -> str:
    return question.lower().rstrip("?").replace(" ", "_")


def _self_model(paths: Paths, _: Context) -> Reading:
    from tools import p12_self_model as model
    answers = model.self_model(paths.repo)
    reading = {f"self_model.{_slug(a.question)}": (a.value, a.status)
               for a in answers}
    incomplete = next(a for a in answers if a.question == "What is incomplete?")
    reading["escalations.open"] = (list(incomplete.value["open_escalations"]),
                                   VERIFIED)
    return reading


def _integrity(paths: Paths, _: Context) -> Reading:
    from tools import certified_evidence_integrity as integrity
    report = integrity.verify(paths.repo)
    return {"integrity.holds": (report.holds, VERIFIED),
            "integrity.phases": ({p: r.holds for p, r in report.phases.items()},
                                 VERIFIED)}


def _native_core(paths: Paths, _: Context) -> Reading:
    core = paths.repo / "native_core/core"
    boundaries = sorted(d.name for d in core.iterdir()
                        if d.is_dir() and not d.name.startswith("__"))
    return {"native_core.boundaries": (len(boundaries), VERIFIED)}


def _corpus(paths: Paths, _: Context) -> Reading:
    from tools import corpus_citation_audit, stale_state_audit
    from tools.governance_index import GovernanceIndex, tracked_markdown
    citations = corpus_citation_audit.audit(
        list(corpus_citation_audit.DEFAULT_ROOTS))
    stale = stale_state_audit.audit(paths.repo)
    index, _ = GovernanceIndex.build(tracked_markdown(paths.repo), paths.repo)
    return {
        "corpus.citation_errors": (citations["errors"], VERIFIED),
        "corpus.live_stale_assertions": (stale["errors"], VERIFIED),
        "corpus.stale_governance_sources": (len(index.stale_sources(paths.repo)),
                                            VERIFIED),
    }


def read_criteria(paths: Paths) -> Optional[dict]:
    """The Active `corpus-health.criteria` version, read-only, or None."""
    from native_core.core.infrastructure import LocalAppendOnlyStorage
    from native_core.core.knowledge.composition import create_knowledge_subsystem
    if not (paths.knowledge_store / "knowledge_versions").is_file():
        return None
    storage = LocalAppendOnlyStorage(paths.knowledge_store)
    storage.provision()          # the directory exists; this creates nothing
    version = create_knowledge_subsystem(storage).retrieval.active(KNOWLEDGE_KEY)
    if version is None:
        return None
    content = {k: v for k, v in dict(version.content).items()
               if k != "knowledge_item_key"}
    return {"content": content,
            "version_sequence": version.identity.version_sequence}


def _knowledge(paths: Paths, _: Context) -> Reading:
    criteria = read_criteria(paths)
    if criteria is None:
        return {}                # → UNKNOWN: nothing Active is admitted
    return {"knowledge.corpus_health_criteria": (criteria, VERIFIED)}


def _memory_records(storage_dir, scope=None):
    from native_core.core.infrastructure import LocalAppendOnlyStorage
    from native_core.core.memory.reader import MemoryReader
    from native_core.core.trace import TraceReader
    storage = LocalAppendOnlyStorage(storage_dir)
    storage.provision()
    return MemoryReader(TraceReader(storage)).read(scope)


def _thaw(value):
    return json.loads(json.dumps(value, default=lambda v: dict(v)
                                 if hasattr(v, "items") else list(v)))


def _memory(paths: Paths, context: Context) -> Reading:
    from tools import p12_trace_registry as registry
    stores = {}
    corpus_health = None
    for store in registry.discover(paths.trace_stores):
        records = _memory_records(store.path)
        stores[store.name] = len(records)
        if store.name == "aios-corpus-health":
            verdicts = [_thaw(m.content) for m in records
                        if m.content is not None and "verdict" in m.content]
            corpus_health = verdicts[-1] if verdicts else None
    previous = None
    if (paths.trace / "trace").is_file():
        own = _memory_records(paths.trace, P13_INSTANCE)
        stores["p13"] = len(own)
        previous = _thaw(own[-1].content) if own else None
    context.previous = previous
    context.memory_available = True
    reading = {"memory.stores": (stores, VERIFIED),
               "memory.p13.previous": (previous, VERIFIED)}
    if corpus_health is not None:
        reading["memory.corpus_health.last"] = (
            {"verdict": corpus_health["verdict"], "facts": corpus_health.get("facts")},
            VERIFIED)
    return reading


def _authority(paths: Paths, _: Context) -> Reading:
    from tools.p13.authority import authority_dimensions, load_envelopes
    envelopes, anomalies = load_envelopes(paths)
    return {"authority.envelopes": ({e.id: list(e.action_types) for e in envelopes},
                                    VERIFIED),
            "authority.anomalies": (list(anomalies), VERIFIED),
            "authority.dimensions": (authority_dimensions(paths), VERIFIED)}


def _remembered_verifications(paths: Paths, context: Context) -> Reading:
    """What earlier cycles verified, as INFERRED evidence (Memory is history).

    Each entry names the cycle that verified it, which may be older than the
    previous cycle: an entry is carried forward until it is verified again.
    """
    if not context.memory_available or not context.previous:
        return {}
    remembered = context.previous.get("verified") or {}
    return {key: (entry["value"], INFERRED,
                  f"Memory: verified by P13 cycle {entry['cycle_id']} at {entry['at']}")
            for key, entry in remembered.items() if key in VERIFICATION_KEYS}


VERIFICATION_KEYS = (
    "verification.foundational_question_reconciliation",
    "verification.ecosystem_relationships",
    "verification.p13_evidence",
)

SELF_MODEL_KEYS = tuple(f"self_model.{_slug(q)}" for q in QUESTIONS)

SOURCES: Tuple[Source, ...] = (
    Source("memory", "Memory via MemoryReader over Trace (P12 stores + P13 store)",
           ("memory.stores", "memory.p13.previous", "memory.corpus_health.last"),
           _memory),
    Source("self_model", "tools.p12_self_model.self_model()",
           SELF_MODEL_KEYS + ("escalations.open",), _self_model),
    Source("integrity", "tools.certified_evidence_integrity.verify()",
           ("integrity.holds", "integrity.phases"), _integrity),
    Source("native_core", "native_core/core boundary directories",
           ("native_core.boundaries",), _native_core),
    Source("corpus", "corpus_citation_audit · stale_state_audit · governance_index",
           ("corpus.citation_errors", "corpus.live_stale_assertions",
            "corpus.stale_governance_sources"), _corpus),
    Source("knowledge", "Knowledge retrieval: corpus-health.criteria (FD-P12-002)",
           ("knowledge.corpus_health_criteria",), _knowledge),
    Source("authority", "Delegation Register + docs/governance/p13-envelopes "
           "+ phase snapshot + Decision Register §22 + certification guard",
           ("authority.envelopes", "authority.anomalies", "authority.dimensions"),
           _authority),
    Source("remembered", "Memory: verifications recorded by earlier P13 cycles",
           VERIFICATION_KEYS, _remembered_verifications),
)


class StateUnderstanding:
    def __init__(self, paths: Paths, sources: Iterable[Source] = SOURCES,
                 clock: Callable[[], str] = now):
        self._paths = paths
        self._sources = tuple(sources)
        self._clock = clock
        self.context = Context()

    def observe(self) -> StateSnapshot:
        facts = []
        taken_at = self._clock()
        for source in self._sources:
            try:
                reading = source.read(self._paths, self.context)
                failure = None
            except Exception as error:      # a source down is a fact, not a crash
                reading, failure = {}, f"{type(error).__name__}: {error}"
            for key in source.keys:
                if key in reading:
                    value, status, *origin = reading[key]
                    facts.append(Fact(key, value, status,
                                      origin[0] if origin else source.describe,
                                      taken_at))
                else:
                    why = (f"unavailable — {failure}" if failure
                           else "not reported")
                    facts.append(Fact(key, None, UNKNOWN,
                                      f"{source.describe}: {why}", taken_at))
        return StateSnapshot(tuple(facts), taken_at)
