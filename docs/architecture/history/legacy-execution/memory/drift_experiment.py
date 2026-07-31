"""
Memory Drift Experiment.

Tests whether Memory correctly handles a real, controlled change to the
world it observed — not a hypothetical. Uses fully self-contained
scratch files (execution/memory/drift_scratch/), never docs/, so a real
edit can be introduced between Run A and Run B without touching any
governance artifact.

Design:
  - citing.md: a scratch document containing one citation, "§9", to
    cited.md, with no Markdown link (matching this harness's
    cross-reference-check convention of a bare section citation).
  - cited.md: starts with NO heading numbered 9. A real Tool call
    against it resolves False.

Run A: real Tool call against the initial state. Real Trace produced.
        Memory extracted from it.
Controlled change: cited.md is edited to add a genuine "## 9. ..."
        heading — the fact on the ground changes for real.
Run B: a memory-aware call using the Run-A-derived cache, immediately
        followed by a real, live call against the new state, so the two
        can be compared directly.

Evaluates exactly what the directive asks:
  - Did Memory detect the outdated information? (only if is_expired()
    or a drift check catches it — tested explicitly, not assumed)
  - Did Memory incorrectly reuse stale evidence? (does the cache blindly
    serve the pre-change answer with no signal that it's now wrong)
  - Was confidence adjusted appropriately? (it is not, by construction —
    confidence in this harness reflects repetition/diversity, not
    ground-truth freshness; this experiment demonstrates that gap)
  - Was fallback execution triggered? (this harness has no automatic
    fallback; whether cache-miss-triggered live-call behavior exists is
    checked directly)
"""

from pathlib import Path

from . import extractor as extractor_mod
from .consumption import build_input_keyed_cache
from .. import tool as tool_mod
from ..trace_schema import normalize_record

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRATCH_DIR = REPO_ROOT / "execution" / "memory" / "drift_scratch"
CROSS_REF_TOOL_PATH = REPO_ROOT / "docs" / "architecture" / "organization" / "execution-catalog" / "tool" / "cross-reference-link-validator-interface.md"


def setup_scratch():
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    citing = SCRATCH_DIR / "citing.md"
    cited = SCRATCH_DIR / "cited.md"
    citing.write_text("# Citing Document\n\nThis document cites §9 of the cited document.\n", encoding="utf-8")
    cited.write_text("# Cited Document\n\n## 1. Introduction\n\nNo section 9 exists yet.\n", encoding="utf-8")
    return citing, cited


def introduce_controlled_change(cited_path):
    """The real, controlled change: cited.md genuinely gains a heading
    numbered 9. Nothing about this is simulated — the file on disk
    actually changes, outside docs/ entirely."""
    text = cited_path.read_text(encoding="utf-8")
    cited_path.write_text(text + "\n## 9. A New Section\n\nThis section did not exist during Run A.\n", encoding="utf-8")


def call_tool(citing_path, cited_path):
    return tool_mod.invoke(
        CROSS_REF_TOOL_PATH, action="verify_cross_reference",
        citing_document=str(citing_path), repository_path=str(REPO_ROOT),
        reference_target=str(cited_path), expected_reference="§9",
    )
