"""
Structured finding/report model shared by every validator.

Introduced in the Execution Catalog Tooling Stabilization Phase to
replace the original single-file validator's plain strings with a
severity-classified, timestamped, machine-readable structure, per the
Architect's directive (structured validation reporting).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone

SEVERITIES = ("error", "warning", "informational")


@dataclass
class Finding:
    validator: str
    severity: str
    message: str
    file: str = None

    def __post_init__(self):
        if self.severity not in SEVERITIES:
            raise ValueError(f"invalid severity: {self.severity!r}")

    def render(self):
        loc = f" {self.file}:" if self.file else ""
        return f"  [{self.severity}]{loc} {self.message}"

    def to_dict(self):
        return {"severity": self.severity, "file": self.file, "message": self.message}


@dataclass
class ValidatorResult:
    name: str
    findings: list

    @property
    def counts(self):
        counts = {s: 0 for s in SEVERITIES}
        for f in self.findings:
            counts[f.severity] += 1
        return counts


@dataclass
class Report:
    artifacts_scanned: int
    results: list
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def total_findings(self):
        return sum(len(r.findings) for r in self.results)

    def totals_by_severity(self):
        totals = {s: 0 for s in SEVERITIES}
        for r in self.results:
            for s, n in r.counts.items():
                totals[s] += n
        return totals

    def render_text(self):
        lines = [
            f"Execution Catalog Validators — {self.artifacts_scanned} artifacts scanned",
            f"Run at: {self.timestamp}",
            "",
        ]
        for r in self.results:
            counts = r.counts
            summary = ", ".join(f"{n} {s}" for s, n in counts.items() if n) or "none"
            lines.append(f"=== {r.name} ({len(r.findings)} finding(s): {summary}) ===")
            if not r.findings:
                lines.append("  none")
            for finding in r.findings:
                lines.append(finding.render())
            lines.append("")
        totals = self.totals_by_severity()
        lines.append(
            f"Total findings across all validators: {self.total_findings()} "
            f"({totals['error']} error, {totals['warning']} warning, "
            f"{totals['informational']} informational)"
        )
        return "\n".join(lines)

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "artifacts_scanned": self.artifacts_scanned,
            "totals_by_severity": self.totals_by_severity(),
            "results": [
                {"validator": r.name, "findings": [f.to_dict() for f in r.findings]}
                for r in self.results
            ],
        }
