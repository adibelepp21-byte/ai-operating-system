"""
Skill invocation.

Capability Hardening Phase upgrade. On top of the request/execution
separation and handler abstraction introduced in the two prior phases,
this revision adds:

  - **Formal input/output validation pipelines** — `validate_input`
    and `validate_output` now each run an ordered list of independent
    validator callables (`input_validators` / `output_validators`),
    not one monolithic check. Every handler gets the same default
    pipeline (target-document existence, target-document readability,
    output type, evidence-tuple shape) and may extend it.
  - **Evidence mapping** — both of a Skill's previously separate result
    shapes (a heuristic-flagged passage; a Tool execution's returned
    evidence) are now normalized into one common `Evidence` structure
    (`source`, `kind`, `resolved`, `detail`, `raw`), so a caller does
    not need to know which stage produced a given finding to use it.
  - **Failure classification** — `SkillResult.failure_class` names
    exactly which pipeline stage failed (`"input_validation"`,
    `"execution"`, `"output_validation"`, `"not_implemented"`), instead
    of a single undifferentiated "failure" status. `invoke()` now runs
    each stage in its own try/except so the classification is exact,
    not inferred after the fact.

Skill invokes Tool remains a direct, static, code-level dependency (this
module imports tool.py) mirroring the ratified Domain Model §4
relationship. Tool invocation only ever originates from inside a Skill
handler — no Agent-Definition-to-Tool path exists anywhere in this
harness.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from . import tool as tool_mod
from .governance_reader import CATALOG_ROOT, canonical_key, read, version as extract_version

CROSS_REF_TOOL_PATH = CATALOG_ROOT / "tool" / "cross-reference-link-validator-interface.md"
DOC_STRUCTURE_TOOL_PATH = CATALOG_ROOT / "tool" / "document-structure-parser-interface.md"
TEXT_SIMILARITY_TOOL_PATH = CATALOG_ROOT / "tool" / "text-similarity-comparison-interface.md"
REPO_ROOT = CATALOG_ROOT.parent.parent.parent.parent

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)\)")
SECTION_RE = re.compile(r"§(\d+)")
NAME_RE = re.compile(r"\*\*Name:\*\*\s*([^\n]+)")

FAILURE_CLASSES = ("input_validation", "execution", "output_validation", "not_implemented")


@dataclass(frozen=True)
class SkillMetadata:
    canonical_key: str
    name: str
    version: str


@dataclass(frozen=True)
class SkillInput:
    """The Skill's input contract: what a caller must supply. Mirrors
    each Skill's own documented Interface field (Skill Framework §9) —
    e.g. 'Accepts a document reference' — as a real, typed, validated
    parameter rather than only prose."""
    skill_canonical_key: str
    target_document: Path


@dataclass(frozen=True)
class Evidence:
    """Normalizes a Skill's two internal result shapes — a
    heuristic-flagged passage, and a Tool execution's returned evidence
    — into one common structure. `resolved` is meaningful only for
    tool-sourced evidence (None for a bare heuristic flag, which makes
    no resolved/unresolved claim). `raw` retains the original object
    for callers that need the full, un-normalized detail."""
    source: str          # "heuristic" | "tool"
    kind: str
    resolved: Optional[bool]
    detail: str
    raw: Any = None


@dataclass(frozen=True)
class SkillOutput:
    """The Skill's output contract: what a caller receives back.
    Mirrors each Skill's own documented Interface 'Returns...' clause,
    expressed as a tuple of normalized Evidence."""
    evidence: tuple


@dataclass(frozen=True)
class SkillResult:
    input: SkillInput
    output: Optional[SkillOutput]
    status: str  # "success" | "failure" | "not_implemented"
    failure_class: Optional[str] = None  # one of FAILURE_CLASSES, set only when status != "success"
    error: Optional[str] = None


def load_canonical_key(skill_path):
    return canonical_key(read(skill_path))


def load_metadata(skill_path) -> SkillMetadata:
    text = read(skill_path)
    name_match = NAME_RE.search(text)
    return SkillMetadata(
        canonical_key=canonical_key(text),
        name=name_match.group(1).strip() if name_match else "unknown",
        version=extract_version(text),
    )


# --- default validation pipeline steps -------------------------------------

def _target_document_exists(skill_input: SkillInput) -> None:
    if not skill_input.target_document.is_file():
        raise ValueError(f"target_document does not resolve: {skill_input.target_document}")


def _target_document_readable(skill_input: SkillInput) -> None:
    try:
        skill_input.target_document.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as exc:
        raise ValueError(f"target_document is not readable as UTF-8 text: {exc}")


def _output_is_skill_output(output) -> None:
    if not isinstance(output, SkillOutput):
        raise TypeError(f"handler must return a SkillOutput, got {type(output).__name__}")


def _evidence_is_well_formed(output: SkillOutput) -> None:
    if not isinstance(output.evidence, tuple):
        raise TypeError("SkillOutput.evidence must be a tuple")
    for e in output.evidence:
        if not isinstance(e, Evidence):
            raise TypeError("every SkillOutput.evidence entry must be an Evidence instance")


DEFAULT_INPUT_VALIDATORS = (_target_document_exists, _target_document_readable)
DEFAULT_OUTPUT_VALIDATORS = (_output_is_skill_output, _evidence_is_well_formed)


class SkillHandler:
    """Base class for a Skill implementation. Subclasses set
    `canonical_key`, implement `execute`, and may extend
    `extra_input_validators` / `extra_output_validators` with
    Skill-specific checks beyond the shared defaults."""

    canonical_key: str = None
    extra_input_validators: tuple = ()
    extra_output_validators: tuple = ()

    def validate_input(self, skill_input: SkillInput) -> None:
        for validator in DEFAULT_INPUT_VALIDATORS + self.extra_input_validators:
            validator(skill_input)

    def execute(self, skill_input: SkillInput) -> SkillOutput:
        raise NotImplementedError

    def validate_output(self, output: SkillOutput) -> None:
        for validator in DEFAULT_OUTPUT_VALIDATORS + self.extra_output_validators:
            validator(output)


class AuthorityBoundaryCheckHandler(SkillHandler):
    """Heuristic: flags paragraphs containing an authority-claiming
    phrase with no nearby negation, as a crude stand-in for 'exceeds
    declared authority tier.' High false-negative risk (most real
    authority-tier violations don't use these exact phrases) and
    nonzero false-positive risk. Not real reasoning."""

    canonical_key = "skill.authority-boundary-check"

    CLAIM_PHRASES = ("is defined as", "hereby establishes", "creates a new", "grants authority")
    NEGATIONS = ("does not", "never", "no provision", "not itself", "no ")

    def execute(self, skill_input: SkillInput) -> SkillOutput:
        text = read(skill_input.target_document)
        evidence = []
        for para in text.split("\n\n"):
            low = para.lower()
            if any(p in low for p in self.CLAIM_PHRASES) and not any(n in low for n in self.NEGATIONS):
                evidence.append(Evidence(
                    source="heuristic", kind="authority_claim_flag",
                    resolved=None, detail=para.strip()[:200], raw=para,
                ))
        return SkillOutput(evidence=tuple(evidence))


class CitationDisciplineVerificationHandler(SkillHandler):
    """Heuristic: within each paragraph, if both a Markdown link and a
    '§N' marker appear, treats the first link found as the cited
    document and the first §N found as the cited section, and invokes
    the Cross-Reference Link Validator Interface Tool to check it. The
    pairing itself is still naive — a paragraph containing an unrelated
    link and an unrelated section number is still paired incorrectly;
    this is a known, real limitation surfaced as operational evidence
    rather than concealed. Paragraphs that mention 'Constitution' or
    '(Canonical) Domain Model' with neither a link nor a section marker
    are flagged as possible restatement-without-citation."""

    canonical_key = "skill.citation-discipline-verification"

    def execute(self, skill_input: SkillInput) -> SkillOutput:
        target_document = skill_input.target_document
        text = read(target_document)
        evidence = []
        for para in text.split("\n\n"):
            links = LINK_RE.findall(para)
            sections = SECTION_RE.findall(para)
            mentions_governance = any(term in para for term in ("Constitution", "Domain Model"))
            if links and sections:
                _, link_path = links[0]
                execution = tool_mod.invoke(
                    CROSS_REF_TOOL_PATH,
                    action="verify_cross_reference",
                    citing_document=str(target_document),
                    repository_path=str(REPO_ROOT),
                    reference_target=str((target_document.parent / link_path).resolve()),
                    expected_reference=f"§{sections[0]}",
                )
                ev = execution.evidence or {}
                detail = execution.error or ev.get("failure_reason") or "resolved"
                evidence.append(Evidence(
                    source="tool", kind="cross_reference_check",
                    resolved=ev.get("resolved"), detail=detail, raw=execution,
                ))
            elif mentions_governance and not sections and not links:
                evidence.append(Evidence(
                    source="heuristic", kind="uncited_restatement_flag",
                    resolved=None, detail=para.strip()[:200], raw=para,
                ))
        return SkillOutput(evidence=tuple(evidence))


class StalenessDetectionHandler(SkillHandler):
    """Heuristic: flags paragraphs containing a staleness-indicating
    phrase, severity-ranked by which phrase matched. High severity
    ("to be determined", "tbd", "not yet resolved") suggests content
    that may have been genuinely forgotten; medium severity ("remains
    open", "pending") is common, deliberate, and often still accurate
    provisional language — not itself evidence of staleness. No Tool
    invocation: this Skill's own declared Interface names none."""

    canonical_key = "skill.staleness-detection"

    HIGH_SEVERITY_PHRASES = ("to be determined", "tbd", "not yet resolved")
    MEDIUM_SEVERITY_PHRASES = ("remains open", "pending", "still open", "not yet defined")

    def execute(self, skill_input: SkillInput) -> SkillOutput:
        text = read(skill_input.target_document)
        flagged = []
        for para in text.split("\n\n"):
            low = para.lower()
            if any(p in low for p in self.HIGH_SEVERITY_PHRASES):
                flagged.append((3, para.strip()[:200]))
            elif any(p in low for p in self.MEDIUM_SEVERITY_PHRASES):
                flagged.append((2, para.strip()[:200]))
        flagged.sort(key=lambda t: -t[0])
        evidence = tuple(
            Evidence(source="heuristic", kind="staleness_flag", resolved=None, detail=f"[severity={sev}] {content}", raw=None)
            for sev, content in flagged
        )
        return SkillOutput(evidence=evidence)


class DuplicateContentDetectionHandler(SkillHandler):
    """Heuristic: pairwise-compares every paragraph in the target
    document against every other paragraph via the Text Similarity
    Comparison Interface Tool, flagging pairs at or above a similarity
    threshold. O(n^2) Tool calls in paragraph count — acceptable only at
    this corpus's small per-document paragraph counts, a real, disclosed
    scaling limitation. This Skill's own declared Interface names
    multiple document references as its input; this implementation
    narrows that to paragraph-pairs within one target_document, matching
    this harness's established single-document convention — a real
    simplification, not a redefinition of the Skill's governed scope."""

    canonical_key = "skill.duplicate-content-detection"
    SIMILARITY_THRESHOLD = 0.7

    def execute(self, skill_input: SkillInput) -> SkillOutput:
        text = read(skill_input.target_document)
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 40]
        evidence = []
        for i in range(len(paragraphs)):
            for j in range(i + 1, len(paragraphs)):
                execution = tool_mod.invoke(
                    TEXT_SIMILARITY_TOOL_PATH, action="compare_similarity",
                    passage_a=paragraphs[i], passage_b=paragraphs[j],
                )
                ev = execution.evidence or {}
                similarity = ev.get("similarity")
                if similarity is not None and similarity >= self.SIMILARITY_THRESHOLD:
                    evidence.append(Evidence(
                        source="tool", kind="duplicate_content_flag", resolved=True,
                        detail=f"paragraphs {i} and {j} are {similarity:.0%} similar", raw=execution,
                    ))
        return SkillOutput(evidence=tuple(evidence))


class SectionNumberingConsistencyCheckHandler(SkillHandler):
    """Real Tool-backed check: parses the target document's own heading
    structure via the Document Structure Parser Interface Tool, then
    scans the document's prose for bare '§N' markers not preceded
    (within ~40 characters) by "Domain Model" or "Constitution" —
    treating those as candidate self-references — and flags any whose
    number isn't among the document's own real headings. The exclusion
    window is a crude, disclosed heuristic: any external citation not
    phrased with one of those two exact lead-in phrases will be
    misclassified as an internal reference."""

    canonical_key = "skill.section-numbering-consistency-check"
    EXTERNAL_PREFIXES = ("Domain Model", "Constitution")
    SECTION_RE = re.compile(r"§(\d+)")

    def execute(self, skill_input: SkillInput) -> SkillOutput:
        target_document = skill_input.target_document
        execution = tool_mod.invoke(
            DOC_STRUCTURE_TOOL_PATH, action="parse_structure", document_path=str(target_document),
        )
        ev = execution.evidence or {}
        if not execution.succeeded or not ev.get("resolved"):
            return SkillOutput(evidence=(Evidence(
                source="tool", kind="document_structure_parse_failure", resolved=False,
                detail=execution.error or ev.get("failure_reason") or "parse failed", raw=execution,
            ),))

        real_numbers = {el["number"] for el in ev["elements"] if el.get("number")}
        text = read(target_document)
        evidence = []
        for m in self.SECTION_RE.finditer(text):
            num = m.group(1)
            preceding = text[max(0, m.start() - 40):m.start()]
            if any(p in preceding for p in self.EXTERNAL_PREFIXES):
                continue
            if num not in real_numbers:
                evidence.append(Evidence(
                    source="tool", kind="section_numbering_mismatch", resolved=False,
                    detail=f"§{num} cited internally but no heading numbered {num} exists in this document",
                    raw=execution,
                ))
        return SkillOutput(evidence=tuple(evidence))


class TerminologyConsistencyScanHandler(SkillHandler):
    """Real Tool-backed check: for each paragraph mentioning one of a
    fixed reference term set (the Domain Model's own canonical entity
    names, per Domain Model §2), compares that paragraph against its own
    term's canonical one-line definition and against every other term's
    definition via the Text Similarity Comparison Interface Tool,
    flagging a paragraph as a "terminology confusion" candidate if it
    reads more similar to a different term's definition than to the term
    it actually names. O(terms^2) Tool calls per mentioning paragraph —
    real, bounded by this harness's small fixed term set (9 entities)."""

    canonical_key = "skill.terminology-consistency-scan"

    REFERENCE_DEFINITIONS = {
        "Agent Instance": "A single, ephemeral runtime execution of an Agent Definition, hosted by a Runtime.",
        "Agent Definition": "A stable, versioned specification of what a class of Agent does and is permitted to use.",
        "Skill": "A discrete, reusable, bounded unit of executable ability.",
        "Workflow": "An explicit, inspectable composition of Skills accomplishing a multi-step outcome.",
        "Tool": "An integration point to something outside AIOS's own cognition.",
        "Runtime": "The execution substrate that hosts Agent Instances.",
        "Knowledge": "Curated, canonical, reviewed, versioned understanding that is durable.",
        "Memory": "A dynamic, experiential, scoped record of what an Agent Instance has encountered.",
        "Trace": "The immutable, append-only, unconditional audit record of one Agent Instance action.",
    }

    def execute(self, skill_input: SkillInput) -> SkillOutput:
        text = read(skill_input.target_document)
        evidence = []
        for para in text.split("\n\n"):
            mentioned = [term for term in self.REFERENCE_DEFINITIONS if term in para]
            for term in mentioned:
                own_exec = tool_mod.invoke(
                    TEXT_SIMILARITY_TOOL_PATH, action="compare_similarity",
                    passage_a=para, passage_b=self.REFERENCE_DEFINITIONS[term],
                )
                own_sim = (own_exec.evidence or {}).get("similarity") or 0.0
                for other_term, other_def in self.REFERENCE_DEFINITIONS.items():
                    if other_term == term:
                        continue
                    other_exec = tool_mod.invoke(
                        TEXT_SIMILARITY_TOOL_PATH, action="compare_similarity",
                        passage_a=para, passage_b=other_def,
                    )
                    other_sim = (other_exec.evidence or {}).get("similarity") or 0.0
                    if other_sim > own_sim:
                        evidence.append(Evidence(
                            source="tool", kind="terminology_confusion_flag", resolved=True,
                            detail=f"paragraph mentioning '{term}' reads more similar to '{other_term}' ({other_sim:.2f} vs {own_sim:.2f})",
                            raw=other_exec,
                        ))
        return SkillOutput(evidence=tuple(evidence))


HANDLERS = {
    h.canonical_key: h()
    for h in (
        AuthorityBoundaryCheckHandler, CitationDisciplineVerificationHandler,
        StalenessDetectionHandler, DuplicateContentDetectionHandler,
        SectionNumberingConsistencyCheckHandler, TerminologyConsistencyScanHandler,
    )
}


def invoke(skill_path, target_document):
    key = load_canonical_key(skill_path)
    skill_input = SkillInput(skill_canonical_key=key, target_document=Path(target_document))
    handler = HANDLERS.get(key)
    if handler is None:
        return SkillResult(input=skill_input, output=None, status="not_implemented", failure_class="not_implemented")

    try:
        handler.validate_input(skill_input)
    except Exception as exc:
        return SkillResult(
            input=skill_input, output=None, status="failure",
            failure_class="input_validation", error=f"{type(exc).__name__}: {exc}",
        )

    try:
        output = handler.execute(skill_input)
    except Exception as exc:
        return SkillResult(
            input=skill_input, output=None, status="failure",
            failure_class="execution", error=f"{type(exc).__name__}: {exc}",
        )

    try:
        handler.validate_output(output)
    except Exception as exc:
        return SkillResult(
            input=skill_input, output=None, status="failure",
            failure_class="output_validation", error=f"{type(exc).__name__}: {exc}",
        )

    return SkillResult(input=skill_input, output=output, status="success")
