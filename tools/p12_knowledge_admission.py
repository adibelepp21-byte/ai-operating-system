"""Executes the Founder-authorized `P6` Knowledge admission. Holds no authority.

`FD-P12-002` (`ACT-CC-P12-015`) records the decision this module executes:

```text
§5   CORPUS-HEALTH CRITERIA = APPROVED FOR KNOWLEDGE ADMISSION
§34  HUMAN AUTHORITY        = FOUNDER
§10  CLAUDE CODE            = AUTHORIZED TO EXECUTE THE CANONICAL
                              KNOWLEDGE ADMISSION AFTER VERIFYING
                              THIS ACT'S ACTUAL DECISION BODY
```

and `§9` fixes the split this module is built around:

> *"Claude Code may execute the admission. Claude Code may not become the human
> authority for the admission."*

**So the reviewer identity is read, never chosen.** `HumanAuthority(reviewer_id)`
is constructed from the `HumanAuthority:` line in the issued instrument's own
authentication section, and the rationale is the instrument's own decision
paragraph. Delete the instrument and this module raises; blank the decision and
it raises; change the reviewer line and the recorded authority changes with it.
There is no default, no fallback, and no literal reviewer name anywhere in this
file. `FOUNDER APPROVAL ≠ CLAUDE EXECUTION ≠ HUMAN AUTHORITY`.

**The candidate is resolved from the repository, not supplied.** `§6` requires
the *exact immutable identity* — path, identifier, content, hash — to be
resolved from the current repository before admission, and forbids substituting
an artifact that is easier to admit. `candidate_identity()` therefore reads the
criteria out of the work's own source with `ast`, never by importing it: the
identity that gets admitted is the repository's, byte for byte, and a criteria
literal that cannot be read statically fails closed rather than being
approximated. The resolved key is then checked against the candidate the
instrument names, so an approval of *these* criteria cannot be spent on others.

**Nothing here decides.** `KnowledgeAdmission.admit` admits **iff**
`GovernanceReview.promotion_authorized` returns `True`, and that reflects only a
provenance-verified human `approve` this Governance instance itself recorded.
This module records the human decision the instrument carries, hands the
candidate and the review surface to the canonical admission, and reports what
came back. It never writes a `KnowledgeVersion`, never marks anything Active —
Active is *derived* from the append-only sequence — and never catches
`UnauthorizedPromotion` to soften it.

**Admission is not consumption.** `§14`: *"Admission itself does not satisfy
R1."* This module ends at an Active version. Whether any work consumes it is
`aios_corpus_health_run` to do and `p12_cross_phase_verification` to measure.

**Provenance is written by the admission act, not after it.** `§8`: *"No
provenance may be manufactured after admission."* The nine elements it names are
assembled before `admit` is called (the six that are knowable then) and
completed from the admission's own return value, and the record is appended to
an append-only partition in the same call. There is no later pass that could
compose a provenance record for an admission it did not perform.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The curated root a Founder instrument may be recognised in. Body plus
#: curated root, the discipline `p12_phase_authorization` applies for the same
#: reason: an arbitrary directory must not be able to manufacture a decision.
DECISION_ROOT = Path("docs/governance/acts")

#: The authentication section an issued admission instrument must carry.
AUTHENTICATION_SECTION = "FOUNDER AUTHENTICATION"

#: The decision the instrument must state, verbatim. A different decision — or
#: a blank one — is not this decision.
REQUIRED_DECISION = "APPROVED FOR KNOWLEDGE ADMISSION"
REQUIRED_ADMISSION = "AUTHORIZED"
REQUIRED_STATUS = "FINAL / ISSUED"

#: The Knowledge item the work judges against.
KNOWLEDGE_ITEM_KEY = "corpus-health.criteria"

#: Where the candidate lives in the repository, and under what name. `§6`: the
#: identity is resolved from the repository, and no substitution is authorized.
CANDIDATE_SOURCE = Path("aios_corpus_health_run.py")
CANDIDATE_IDENTIFIER = "CRITERIA_CONTENT"

#: The durable store the admitted Knowledge lives in. Knowledge is *"durable,
#: authoritative, versioned understanding"* by its boundary's own definition; a
#: version that evaporates with the process that admitted it would not be
#: Knowledge, and no later execution could consume it.
RUNTIME_STORE = Path("docs/architecture/p12/aios-runtime-store")

#: Governance owns its decision records and persists them append-only. This is
#: the durable audit log, not the trust index — the index is in-memory by
#: design, so a restart trusts nothing it did not itself record.
DECISION_STORE = Path("docs/architecture/p12/governance-decisions")

#: Where the admission act writes its own provenance, append-only.
PROVENANCE_STORE = Path("docs/architecture/p12/knowledge-admissions")
PROVENANCE_PARTITION = "admission_provenance"


class AdmissionAuthorityUnresolved(Exception):
    """No single issued Founder instrument authorizes this admission.

    Raised rather than proceeding unauthorized. `§11` forbids manufacturing
    `HumanAuthority`, and an admission that cannot find its authority has none.
    """


class CandidateIdentityUnresolved(Exception):
    """The candidate's exact identity could not be resolved from the repository.

    `§6` makes identity verification a precondition, so an unreadable candidate
    is a stop, never an approximation.
    """


class AdmissionRefused(Exception):
    """The admission was refused for a reason that is not the gate's own.

    `UnauthorizedPromotion` is Governance's refusal and is allowed to propagate
    untouched; this covers the checks that run before the gate is reached.
    """


# ---------------------------------------------------------------------------
# THE DECISION — read out of the issued instrument's own body
# ---------------------------------------------------------------------------

#: A numbered section heading (``35. FOUNDER AUTHENTICATION``), recognised by
#: case rather than by an allow-list of punctuation — the fix
#: `p12_phase_authorization` made after an arrow in a heading silently folded
#: one section's body into another.
_HEADING = re.compile(r"^(\d+)\.\s+(\S.*\S)\s*$")

#: ``HumanAuthority:`` alone on its line, or ``HumanAuthority: Founder``. Both
#: forms occur in issued instruments and neither is the "real" one, so the
#: reader accepts what a Founder actually typed.
_LABEL = re.compile(r"^([A-Za-z][A-Za-z0-9 \"'()/-]*?):\s*(.*?)\s*$")


@dataclass(frozen=True)
class FounderAuthorization:
    """What the issued instrument states. Every field is quoted from its body."""

    instrument: str
    section: str
    decision: str
    admission: str
    human_authority: str
    delegated_execution: str
    candidate_described_as: str
    status: str
    date: str
    rationale: str

    def as_reported(self) -> dict:
        return {
            "instrument": self.instrument,
            "section": self.section,
            "decision": self.decision,
            "admission": self.admission,
            "human_authority": self.human_authority,
            "delegated_execution": self.delegated_execution,
            "candidate_described_as": self.candidate_described_as,
            "status": self.status,
            "date": self.date,
        }


def _is_heading_text(text: str) -> bool:
    letters = [c for c in text if c.isalpha()]
    return bool(letters) and all(c.isupper() for c in letters)


def _sections(text: str) -> Tuple[Tuple[int, str, str], ...]:
    """Split a body into `(number, heading, body)`, in document order."""
    found = []
    current: Optional[list] = None
    for line in text.split("\n"):
        match = _HEADING.match(line)
        if match and _is_heading_text(match.group(2)):
            if current is not None:
                found.append((current[0], current[1], "\n".join(current[2])))
            current = [int(match.group(1)), match.group(2).strip(), []]
            continue
        if current is not None:
            current[2].append(line)
    if current is not None:
        found.append((current[0], current[1], "\n".join(current[2])))
    return tuple(found)


def _labelled(body: str) -> dict:
    """Label/value pairs from an authentication block.

    Both layouts appear in the corpus — ``Status: ISSUED`` on one line, and a
    bare ``Status:`` with its value on the next. Reading only one of them would
    make the parser, not the Founder, decide which instruments count.
    """
    values: dict = {}
    lines = body.split("\n")
    for index, line in enumerate(lines):
        match = _LABEL.match(line)
        if match is None:
            continue
        label, inline = match.group(1).strip(), match.group(2).strip()
        if inline:
            values.setdefault(label, inline)
            continue
        for following in lines[index + 1:]:
            if following.strip():
                if _LABEL.match(following):
                    break  # the next label, not this label's value
                values.setdefault(label, following.strip())
                break
    return values


def _decision_paragraph(sections) -> str:
    """The instrument's own decision sentence, used as the recorded rationale.

    `ReviewDecision` requires a rationale and refuses to record without one —
    *"a decision without a reason is not accountable"*. The reason belongs to
    the decision-maker, so it is quoted from the instrument rather than
    composed here.
    """
    for _number, heading, body in sections:
        if "FOUNDER DECISION" not in heading:
            continue
        paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
        for paragraph in paragraphs:
            if paragraph.startswith("The Founder authorizes"):
                return " ".join(paragraph.split())
    return ""


def founder_authorization(root: Path = REPO_ROOT) -> FounderAuthorization:
    """The one issued instrument authorizing this admission, or raise.

    Recognised by body, not by filename: an authentication section stating the
    decision, the admission state, a non-empty human authority, and
    `FINAL / ISSUED`. `IDENTIFIER ≠ ACTUAL DECISION BODY`.
    """
    directory = root / DECISION_ROOT
    if not directory.is_dir():
        raise AdmissionAuthorityUnresolved(
            f"the governance acts root does not resolve: {DECISION_ROOT}")
    found = []
    for path in sorted(directory.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        sections = _sections(text)
        block = [s for s in sections if s[1] == AUTHENTICATION_SECTION]
        if len(block) != 1:
            continue
        number, heading, body = block[0]
        values = _labelled(body)
        if values.get("Decision") != REQUIRED_DECISION:
            continue
        if values.get("Admission") != REQUIRED_ADMISSION:
            continue
        if values.get("Status") != REQUIRED_STATUS:
            continue
        reviewer = (values.get("HumanAuthority") or "").strip()
        if not reviewer:
            continue
        found.append(FounderAuthorization(
            instrument=path.relative_to(root).as_posix(),
            section=f"§{number} {heading}",
            decision=values["Decision"],
            admission=values["Admission"],
            human_authority=reviewer,
            delegated_execution=values.get("Delegated Execution", ""),
            candidate_described_as=values.get("Candidate", ""),
            status=values["Status"],
            date=values.get("Date", ""),
            rationale=_decision_paragraph(sections)))
    if len(found) != 1:
        raise AdmissionAuthorityUnresolved(
            f"{len(found)} issued instruments authorize a Knowledge admission; "
            "exactly one must. Which decision governs is a Founder question, "
            "not a parsing one")
    authorization = found[0]
    if not authorization.rationale:
        raise AdmissionAuthorityUnresolved(
            f"{authorization.instrument} states a decision but no reason for "
            "it; a decision without a rationale cannot be recorded")
    return authorization


# ---------------------------------------------------------------------------
# THE CANDIDATE — resolved from the repository, never supplied
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CandidateIdentity:
    """`§6`'s exact immutable identity, as read from the repository."""

    knowledge_item_key: str
    source_path: str
    source_identifier: str
    content: Mapping
    content_hash: str
    source_hash: str

    def as_reported(self) -> dict:
        return {
            "knowledge_item_key": self.knowledge_item_key,
            "source_path": self.source_path,
            "source_identifier": self.source_identifier,
            "content": dict(self.content),
            "content_hash": self.content_hash,
            "source_hash": self.source_hash,
            # `§6` asks for the candidate's version. A candidate has none:
            # version identity is allocated by `KnowledgeVersioning` at
            # admission and by nothing else, so claiming one here would be the
            # `§7` error — `ACTIVE VERSION = NOT YET CLAIMED`.
            "version": None,
            "version_allocated_by": "KnowledgeVersioning.next_version_identity",
        }


def canonical_bytes(content: Any) -> bytes:
    """The content's deterministic encoding — the same stdlib shape the
    Knowledge store itself writes, so a hash taken here and a hash taken over a
    stored version are hashes of the same thing."""
    return json.dumps(content, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def content_hash(content: Any) -> str:
    return hashlib.sha256(canonical_bytes(content)).hexdigest()


def _static_value(node: ast.AST, bindings: Mapping) -> Any:
    """Evaluate a literal that may name another module-level constant.

    `ast.literal_eval` alone cannot read the criteria, because the mapping
    binds its own key through the module's `KNOWLEDGE_KEY` constant rather
    than repeating the string. Resolving that name against the *same module's*
    preceding bindings is not an approximation and not an execution — it reads
    the one binding the name has at that point in the file. A name with no such
    binding raises, so a criteria literal assembled at runtime still fails
    closed rather than being guessed at.
    """
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id not in bindings:
            raise CandidateIdentityUnresolved(
                f"{node.id!r} is not bound to a literal above "
                f"{CANDIDATE_IDENTIFIER} in {CANDIDATE_SOURCE}")
        return bindings[node.id]
    if isinstance(node, ast.Dict):
        return {_static_value(k, bindings): _static_value(v, bindings)
                for k, v in zip(node.keys, node.values)}
    if isinstance(node, (ast.List, ast.Tuple)):
        return [_static_value(e, bindings) for e in node.elts]
    raise CandidateIdentityUnresolved(
        f"{CANDIDATE_IDENTIFIER} in {CANDIDATE_SOURCE} contains "
        f"{type(node).__name__}, which is not a literal and cannot be "
        "identified statically")


def candidate_identity(root: Path = REPO_ROOT) -> CandidateIdentity:
    """Resolve the candidate's identity from the repository source.

    Read with `ast`, not by import: the artifact being admitted is the one
    committed to the repository, and a value produced by executing a module is
    a runtime value, which is a different thing. A literal that cannot be read
    statically raises — `§6` makes identity a precondition, and an
    approximation of an identity is not one.
    """
    source = root / CANDIDATE_SOURCE
    if not source.is_file():
        raise CandidateIdentityUnresolved(
            f"the candidate's source does not resolve: {CANDIDATE_SOURCE}")
    raw = source.read_bytes()
    try:
        tree = ast.parse(raw.decode("utf-8"), filename=str(source))
    except SyntaxError as exc:
        raise CandidateIdentityUnresolved(
            f"{CANDIDATE_SOURCE} does not parse: {exc}") from exc
    literal = None
    bindings: dict = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if CANDIDATE_IDENTIFIER in names:
            literal = _static_value(node.value, bindings)
            break
        # Record the module-level constants declared *above* the candidate, so
        # a name it uses resolves to the binding it actually has here.
        if isinstance(node.value, ast.Constant):
            for name in names:
                bindings[name] = node.value.value
    if literal is None:
        raise CandidateIdentityUnresolved(
            f"{CANDIDATE_SOURCE} declares no module-level "
            f"{CANDIDATE_IDENTIFIER}")
    if not isinstance(literal, dict):
        raise CandidateIdentityUnresolved(
            f"{CANDIDATE_IDENTIFIER} is {type(literal).__name__}, not a mapping")
    key = literal.get("knowledge_item_key")
    if key != KNOWLEDGE_ITEM_KEY:
        raise CandidateIdentityUnresolved(
            f"the resolved criteria name knowledge item {key!r}, but the "
            f"admission is for {KNOWLEDGE_ITEM_KEY!r}")
    return CandidateIdentity(
        knowledge_item_key=KNOWLEDGE_ITEM_KEY,
        source_path=CANDIDATE_SOURCE.as_posix(),
        source_identifier=CANDIDATE_IDENTIFIER,
        content=dict(literal),
        content_hash=content_hash(literal),
        source_hash=hashlib.sha256(raw).hexdigest())


def _tokens(text: str) -> frozenset:
    return frozenset(t for t in re.split(r"[^a-z0-9]+", text.lower()) if t)


def approval_covers(authorization: FounderAuthorization,
                    candidate: CandidateIdentity) -> bool:
    """Whether the instrument's named candidate is the resolved one.

    `§11`: *"FOUNDER APPROVAL = APPROVAL OF THE IDENTIFIED CANDIDATE"*. An
    approval of the corpus-health criteria must not be spendable on a different
    Knowledge item, so the resolved key's own words must appear in the
    candidate the instrument names. This is a containment check over the
    decision body, not a judgement about what the Founder meant.
    """
    described = _tokens(authorization.candidate_described_as)
    if not described:
        return False
    return _tokens(candidate.knowledge_item_key) <= described


# ---------------------------------------------------------------------------
# THE ADMISSION — canonical mechanism, executed, never simulated
# ---------------------------------------------------------------------------

def admit(root: Path = REPO_ROOT, *,
          store_root: Optional[Path] = None,
          decision_root: Optional[Path] = None,
          provenance_root: Optional[Path] = None) -> dict:
    """Execute the authorized admission. Returns what happened, not a verdict.

    The order is the one `§22` fixes, and each step is a real one:

    ```text
    CANDIDATE   resolved from the repository, by identity
    REVIEW      a ReviewDecision carrying the instrument's human authority
    AUTHORIZED  recorded through GovernanceReview.record_decision
    ADMISSION   KnowledgeAdmission.admit, which consults the gate itself
    ACTIVE      derived by KnowledgeVersioning from the append-only sequence
    ```
    """
    from native_core.core.governance import (
        GovernanceReview, HumanAuthority, ReviewDecision)
    from native_core.core.infrastructure import (
        LocalAppendOnlyStorage, build_default_infrastructure)
    from native_core.core.memory import MemoryReader, PromotionCandidate
    from native_core.core.runtime import AIOSRuntime, RuntimeState
    from native_core.core.trace import TraceReader

    from tools.p12_trace_registry import STORE_ROOT

    authorization = founder_authorization(root)
    candidate_id = candidate_identity(root)
    if not approval_covers(authorization, candidate_id):
        raise AdmissionRefused(
            f"{authorization.instrument} approves "
            f"{authorization.candidate_described_as!r}, which does not name "
            f"the resolved candidate {candidate_id.knowledge_item_key!r}")

    store_root = store_root or (root / RUNTIME_STORE)
    decision_root = decision_root or (root / DECISION_STORE)
    provenance_root = provenance_root or (root / PROVENANCE_STORE)

    # The filesystem facility requires its root to exist; it establishes
    # storage beneath a root, it does not invent one.
    store_root.mkdir(parents=True, exist_ok=True)
    bootstrap = build_default_infrastructure(base_dir=store_root)
    bootstrap.establish()
    runtime = AIOSRuntime(
        runtime_id="p12-knowledge-admission",
        storage=bootstrap.get("storage"),
        substrate=bootstrap.get("execution-substrate"))
    runtime.initialize()
    runtime.start()
    if runtime.state is not RuntimeState.RUNNING:
        raise AdmissionRefused(f"runtime did not reach RUNNING: {runtime.state}")
    try:
        knowledge = runtime.knowledge

        # Already Active? Then this admission is finished, and appending a
        # second identical version would be version churn dressed as work. A
        # *different* content under the same key is a governed revision, which
        # this instrument does not authorize.
        existing = knowledge.retrieval.active(candidate_id.knowledge_item_key)
        if existing is not None:
            stored = _plain(existing.content)
            if content_hash(stored) != candidate_id.content_hash:
                raise AdmissionRefused(
                    f"{candidate_id.knowledge_item_key!r} already has an Active "
                    "version whose content differs from the approved "
                    "candidate; superseding it is a governed revision this "
                    "instrument does not authorize")
            return _result(authorization, candidate_id, existing,
                           admitted_now=False, provenance=None)

        candidate = PromotionCandidate(
            scope=candidate_id.knowledge_item_key,
            observed_content=candidate_id.content,
            occurrence_count=1)

        # Governance's evidence source is the real work's own Trace store.
        trace_storage = LocalAppendOnlyStorage(STORE_ROOT / "aios-corpus-health")
        trace_storage.provision()
        decision_storage = LocalAppendOnlyStorage(decision_root)
        decision_storage.provision()
        review = GovernanceReview(
            memory_reader=MemoryReader(TraceReader(trace_storage)),
            decision_storage=decision_storage)

        # The human authority is the instrument's, quoted. Nothing in this
        # module supplies a reviewer identity of its own.
        decision = ReviewDecision(
            candidate=candidate,
            decision="approve",
            authority=HumanAuthority(reviewer_id=authorization.human_authority),
            rationale=(f"{authorization.instrument} {authorization.section}: "
                       f"{authorization.rationale}"))
        review.record_decision(decision)

        # `§8`: assembled before the admission, completed from its result, and
        # written in this call. Nothing later composes a provenance record.
        provenance = {
            "candidate_artifact": candidate_id.source_identifier,
            "candidate_version": None,
            "candidate_immutable_identity": candidate_id.content_hash,
            "source_location": candidate_id.source_path,
            "source_hash": candidate_id.source_hash,
            "decision_instrument": authorization.instrument,
            "decision_section": authorization.section,
            "founder_authority": authorization.human_authority,
            "admission_action": "KnowledgeAdmission.admit",
        }

        # The gate. `UnauthorizedPromotion` propagates untouched — catching it
        # would convert a fail-closed gate into a fail-open one.
        version = knowledge.admission.admit(candidate, review)

        provenance["admission_timestamp"] = datetime.now(timezone.utc).isoformat()
        provenance["resulting_knowledge_identity"] = {
            "knowledge_item_key": version.identity.knowledge_item_key,
            "version_sequence": version.identity.version_sequence,
        }
        provenance["admitted_content_hash"] = content_hash(
            _plain(version.content))
        _record_provenance(provenance_root, provenance)

        active = knowledge.retrieval.active(candidate_id.knowledge_item_key)
        return _result(authorization, candidate_id, active,
                       admitted_now=True, provenance=provenance)
    finally:
        runtime.stop()


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    return value


def _record_provenance(provenance_root: Path, provenance: dict) -> None:
    from native_core.core.infrastructure import LocalAppendOnlyStorage
    storage = LocalAppendOnlyStorage(provenance_root)
    storage.provision()
    storage.append(PROVENANCE_PARTITION, canonical_bytes(provenance))


def _result(authorization, candidate_id, version, *, admitted_now, provenance):
    stored = None if version is None else _plain(version.content)
    return {
        "authorization": authorization.as_reported(),
        "candidate": candidate_id.as_reported(),
        "admitted_in_this_call": admitted_now,
        "active_version": None if version is None else {
            "knowledge_item_key": version.identity.knowledge_item_key,
            "version_sequence": version.identity.version_sequence,
            "content": stored,
            "content_hash": content_hash(stored),
        },
        "content_matches_candidate": (
            stored is not None
            and content_hash(stored) == candidate_id.content_hash),
        "provenance": provenance,
    }


def admission_provenance(root: Path = REPO_ROOT) -> Tuple[dict, ...]:
    """Every provenance record written by an admission, in append order."""
    path = root / PROVENANCE_STORE / PROVENANCE_PARTITION
    if not path.is_file():
        return ()
    records = []
    for line in path.read_text(encoding="utf-8").split("\n"):
        if line.strip():
            records.append(json.loads(line))
    return tuple(records)


def main(argv=None) -> int:
    result = admit()
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
