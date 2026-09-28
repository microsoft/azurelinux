#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Validate spec review report JSON and print findings.

Usage:
    python spec_review_schema.py report.json [--errors] [--warnings] [--json]

Exit codes:
    0 = Valid report (regardless of findings)
    2 = Invalid JSON, file error, or schema validation failure
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class Finding(BaseModel):
    """One actionable issue or suggestion identified in a spec file."""

    model_config = ConfigDict(extra="forbid")

    description: str = Field(..., min_length=1)
    citation: str | None = None
    line: int | None = Field(None, ge=1, description="Line number in the spec file")

    @field_validator("citation", mode="before")
    @classmethod
    def normalize_citation(cls, v: str | None) -> str | None:
        """Normalize empty citation markers to ``None``."""
        if v in (None, "N/A", "n/a", ""):
            return None
        return v


class SpecReview(BaseModel):
    """Validated findings for one reviewed spec file."""

    model_config = ConfigDict(extra="forbid")

    spec_file: str = Field(..., min_length=1)
    errors: list[Finding] = Field(default_factory=list)
    warnings: list[Finding] = Field(default_factory=list)
    suggestions: list[Finding] = Field(default_factory=list)

    @property
    def spec_name(self) -> str:
        """Return the spec file's base name."""
        return Path(self.spec_file).name


class SpecReviewReport(BaseModel):
    """Validated collection of per-spec review results."""

    model_config = ConfigDict(extra="forbid")

    spec_reviews: list[SpecReview] = Field(..., min_length=1)

    @classmethod
    def from_file(cls, path: str | Path) -> SpecReviewReport:
        """Load and validate a report from a JSON file."""
        with Path(path).open(encoding="utf-8") as f:
            return cls.model_validate(json.load(f))

    @property
    def total_errors(self) -> int:
        """Return the total number of errors."""
        return sum(len(r.errors) for r in self.spec_reviews)

    @property
    def total_warnings(self) -> int:
        """Return the total number of warnings."""
        return sum(len(r.warnings) for r in self.spec_reviews)

    @property
    def total_suggestions(self) -> int:
        """Return the total number of suggestions."""
        return sum(len(r.suggestions) for r in self.spec_reviews)

    @property
    def has_errors(self) -> bool:
        """Return whether the report contains errors."""
        return self.total_errors > 0

    def print_summary(self) -> None:
        """Print aggregate finding counts."""
        status = "ERRORS FOUND" if self.has_errors else "No errors"
        print(f"{status}")
        print(
            f"Specs: {len(self.spec_reviews)} | Errors: {self.total_errors} | "
            f"Warnings: {self.total_warnings} | Suggestions: {self.total_suggestions}"
        )

    def print_errors(self) -> None:
        """Print all error findings."""
        for review in self.spec_reviews:
            if review.errors:
                print(f"\n{review.spec_name}:")
                for e in review.errors:
                    print(f"  [error] {e.description}")
                    if e.citation:
                        print(f"     {e.citation}")

    def print_warnings(self) -> None:
        """Print all warning findings."""
        for review in self.spec_reviews:
            if review.warnings:
                print(f"\n{review.spec_name}:")
                for w in review.warnings:
                    print(f"  [warning] {w.description}")
                    if w.citation:
                        print(f"     {w.citation}")

    def print_suggestions(self) -> None:
        """Print all suggestion findings."""
        for review in self.spec_reviews:
            if review.suggestions:
                print(f"\n{review.spec_name}:")
                for s in review.suggestions:
                    print(f"  [suggestion] {s.description}")
                    if s.citation:
                        print(f"     {s.citation}")

    def to_summary_dict(self) -> dict:
        """Return aggregate finding counts as a dictionary."""
        return {
            "specs": len(self.spec_reviews),
            "errors": self.total_errors,
            "warnings": self.total_warnings,
            "suggestions": self.total_suggestions,
            "blocking": self.has_errors,
        }


def _load_report(path: Path) -> SpecReviewReport:
    """Load and validate a report, raising on any error."""
    return SpecReviewReport.from_file(path)


def _findings_set(reviews: list[SpecReview], severity: str) -> dict[tuple[str, str], Finding]:
    """Build a lookup of (spec_name, description) -> Finding for a severity level."""
    result: dict[tuple[str, str], Finding] = {}
    for review in reviews:
        for finding in getattr(review, severity):
            result[(review.spec_name, finding.description)] = finding
    return result


@dataclass(frozen=True)
class LabeledReport:
    """A validated report paired with its display label."""

    label: str
    report: SpecReviewReport


@dataclass(frozen=True)
class ReportComparison:
    """The two reviewer reports and their synthesized result."""

    reviewer_a: LabeledReport
    reviewer_b: LabeledReport
    synthesized: LabeledReport


def _print_comparison_summary(comparison: ReportComparison) -> None:
    """Print aggregate counts for each report in a comparison."""
    reports = (comparison.reviewer_a, comparison.reviewer_b, comparison.synthesized)
    col_w = max(*(len(item.label) for item in reports), 5) + 2
    print(f"┌─{'─' * col_w}─┬────────┬──────────┬─────────────┐")
    print(f"│ {'Model':<{col_w}} │ Errors │ Warnings │ Suggestions │")
    print(f"├─{'─' * col_w}─┼────────┼──────────┼─────────────┤")
    for item in reports:
        print(
            f"│ {item.label:<{col_w}} │ {item.report.total_errors:>6} │ "
            f"{item.report.total_warnings:>8} │ "
            f"{item.report.total_suggestions:>11} │"
        )
    print(f"└─{'─' * col_w}─┴────────┴──────────┴─────────────┘")
    print()


def _finding_sources(
    key: tuple[str, str],
    findings_a: dict[tuple[str, str], Finding],
    findings_b: dict[tuple[str, str], Finding],
) -> str:
    """Return the reviewer labels that reported one finding."""
    sources = []
    if key in findings_a:
        sources.append("A")
    if key in findings_b:
        sources.append("B")
    return "+".join(sources)


def _print_severity_comparison(
    comparison: ReportComparison,
    severity: str,
    icon: str,
) -> None:
    """Print kept, dropped, and synthesized-only findings for one severity."""
    findings_a = _findings_set(comparison.reviewer_a.report.spec_reviews, severity)
    findings_b = _findings_set(comparison.reviewer_b.report.spec_reviews, severity)
    findings_final = _findings_set(comparison.synthesized.report.spec_reviews, severity)

    all_keys = set(findings_a) | set(findings_b)
    kept = all_keys & set(findings_final)
    dropped = all_keys - set(findings_final)
    added = set(findings_final) - all_keys

    if not any((kept, dropped, added)):
        return

    print(f"── {icon} {severity.upper()} ──")
    if kept:
        print(f"  Kept ({len(kept)}):")
        for spec, description in sorted(kept):
            sources = _finding_sources((spec, description), findings_a, findings_b)
            print(f"    + [{sources}] {spec}: {description}")
    if dropped:
        print(f"  Dropped ({len(dropped)}):")
        for spec, description in sorted(dropped):
            sources = _finding_sources((spec, description), findings_a, findings_b)
            print(f"    - [{sources}] {spec}: {description}")
    if added:
        print(f"  Added by synthesizer ({len(added)}):")
        for spec, description in sorted(added):
            print(f"    + {spec}: {description}")
    print()


def compare_reports(comparison: ReportComparison) -> None:
    """Print a human-readable comparison of two reviewer reports and the synthesis."""
    _print_comparison_summary(comparison)
    for severity, icon in (
        ("errors", "ERROR"),
        ("warnings", "WARNING"),
        ("suggestions", "SUGGESTION"),
    ):
        _print_severity_comparison(comparison, severity, icon)


def _run_compare(argv: list[str]) -> int:
    """Run the multi-model report comparison command."""
    parser = argparse.ArgumentParser(description="Compare multi-model spec review reports")
    parser.add_argument("_cmd", metavar="compare")
    parser.add_argument("report_a", type=Path, help="Report from reviewer A")
    parser.add_argument("report_b", type=Path, help="Report from reviewer B")
    parser.add_argument("report_final", type=Path, help="Final synthesized report")
    parser.add_argument("--label-a", default="Reviewer A", help="Display label for reviewer A")
    parser.add_argument("--label-b", default="Reviewer B", help="Display label for reviewer B")
    parser.add_argument(
        "--label-final",
        default="Synthesized",
        help="Display label for final report",
    )
    args = parser.parse_args(argv)

    try:
        comparison = ReportComparison(
            reviewer_a=LabeledReport(args.label_a, _load_report(args.report_a)),
            reviewer_b=LabeledReport(args.label_b, _load_report(args.report_b)),
            synthesized=LabeledReport(args.label_final, _load_report(args.report_final)),
        )
    except FileNotFoundError as exc:
        print(f"File not found: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 2
    except (OSError, UnicodeError, ValidationError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 2

    compare_reports(comparison)
    return 0


def _print_requested_findings(
    report: SpecReviewReport,
    args: argparse.Namespace,
) -> None:
    """Print the finding categories selected by validation CLI flags."""
    show_all = args.all
    show_errors = args.errors or show_all or not any(
        (args.errors, args.warnings, args.suggestions)
    )
    if show_errors:
        report.print_errors()
    if args.warnings or show_all:
        report.print_warnings()
    if args.suggestions or show_all:
        report.print_suggestions()


def _run_validate(argv: list[str]) -> int:
    """Run the report validation and inspection command."""
    parser = argparse.ArgumentParser(description="Validate spec review report")
    parser.add_argument("file", type=Path, help="Path to report JSON")
    parser.add_argument("--errors", action="store_true", help="Print errors", default=False)
    parser.add_argument("--warnings", action="store_true", help="Print warnings", default=False)
    parser.add_argument("--suggestions", action="store_true", help="Print suggestions", default=False)
    parser.add_argument("--all", action="store_true", help="Print all findings", default=False)
    parser.add_argument("--json", action="store_true", help="Output summary as JSON", default=False)

    args = parser.parse_args(argv)

    try:
        report = SpecReviewReport.from_file(args.file)
    except FileNotFoundError:
        print(f"File not found: {args.file}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 2
    except (OSError, UnicodeError, ValidationError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report.to_summary_dict(), indent=2))
    else:
        report.print_summary()
        _print_requested_findings(report, args)

    return 0


def main() -> int:
    """Validate, summarize, or compare spec-review reports."""
    argv = sys.argv[1:]
    if argv and argv[0] == "compare":
        return _run_compare(argv)
    if argv and argv[0] == "--schema":
        print(json.dumps(SpecReviewReport.model_json_schema(), indent=2))
        return 0
    return _run_validate(argv)


if __name__ == "__main__":
    sys.exit(main())
