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
from pathlib import Path
from typing import NamedTuple

from pydantic import BaseModel, ConfigDict, Field, field_validator


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


def _print_comparison_summary(
    labeled_reports: tuple[tuple[str, SpecReviewReport], ...],
) -> None:
    """Print aggregate counts for each report in a comparison."""
    col_w = max(*(len(label) for label, _report in labeled_reports), 5) + 2
    print(f"┌─{'─' * col_w}─┬────────┬──────────┬─────────────┐")
    print(f"│ {'Model':<{col_w}} │ Errors │ Warnings │ Suggestions │")
    print(f"├─{'─' * col_w}─┼────────┼──────────┼─────────────┤")
    for label, report in labeled_reports:
        print(
            f"│ {label:<{col_w}} │ {report.total_errors:>6} │ "
            f"{report.total_warnings:>8} │ {report.total_suggestions:>11} │"
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
    reports: tuple[SpecReviewReport, SpecReviewReport, SpecReviewReport],
    severity: str,
    icon: str,
) -> None:
    """Print kept, dropped, and synthesized-only findings for one severity."""
    report_a, report_b, report_final = reports
    findings_a = _findings_set(report_a.spec_reviews, severity)
    findings_b = _findings_set(report_b.spec_reviews, severity)
    findings_final = _findings_set(report_final.spec_reviews, severity)

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


class ComparisonLabels(NamedTuple):
    """Display labels for the two input reports and synthesized result."""

    report_a: str = "Reviewer A"
    report_b: str = "Reviewer B"
    final: str = "Synthesized"


_DEFAULT_COMPARISON_LABELS = ComparisonLabels()


def compare_reports(
    report_a: SpecReviewReport,
    report_b: SpecReviewReport,
    report_final: SpecReviewReport,
    labels: ComparisonLabels = _DEFAULT_COMPARISON_LABELS,
) -> None:
    """Print a human-readable comparison of two reviewer reports and the synthesis."""
    reports = (report_a, report_b, report_final)
    _print_comparison_summary(
        (
            (labels.report_a, report_a),
            (labels.report_b, report_b),
            (labels.final, report_final),
        )
    )
    for severity, icon in (
        ("errors", "ERROR"),
        ("warnings", "WARNING"),
        ("suggestions", "SUGGESTION"),
    ):
        _print_severity_comparison(reports, severity, icon)


def _compare_parser() -> argparse.ArgumentParser:
    """Build the compare-mode argument parser."""
    parser = argparse.ArgumentParser(description="Compare multi-model spec review reports")
    parser.add_argument("_cmd", metavar="compare")
    parser.add_argument("report_a", type=Path, help="Report from reviewer A")
    parser.add_argument("report_b", type=Path, help="Report from reviewer B")
    parser.add_argument("report_final", type=Path, help="Final synthesized report")
    parser.add_argument("--label-a", default="Reviewer A", help="Display label for reviewer A")
    parser.add_argument("--label-b", default="Reviewer B", help="Display label for reviewer B")
    parser.add_argument("--label-final", default="Synthesized", help="Display label for final report")
    return parser


def _validation_parser() -> argparse.ArgumentParser:
    """Build the report-validation argument parser."""
    parser = argparse.ArgumentParser(description="Validate spec review report")
    parser.add_argument("file", type=Path, help="Path to report JSON")
    parser.add_argument("--errors", action="store_true", help="Print errors", default=False)
    parser.add_argument("--warnings", action="store_true", help="Print warnings", default=False)
    parser.add_argument("--suggestions", action="store_true", help="Print suggestions", default=False)
    parser.add_argument("--all", action="store_true", help="Print all findings", default=False)
    parser.add_argument("--json", action="store_true", help="Output summary as JSON", default=False)
    return parser


def _run_compare(args: argparse.Namespace) -> int:
    """Load and compare three review reports."""
    try:
        report_a = _load_report(args.report_a)
        report_b = _load_report(args.report_b)
        report_final = _load_report(args.report_final)
    except FileNotFoundError as e:
        print(f"File not found: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        return 2
    except (OSError, ValueError) as e:
        print(f"Validation failed: {e}", file=sys.stderr)
        return 2

    compare_reports(
        report_a,
        report_b,
        report_final,
        ComparisonLabels(args.label_a, args.label_b, args.label_final),
    )
    return 0


def _run_validation(args: argparse.Namespace) -> int:
    """Load and display one review report."""
    try:
        report = SpecReviewReport.from_file(args.file)
    except FileNotFoundError:
        print(f"File not found: {args.file}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        return 2
    except (OSError, ValueError) as e:
        print(f"Validation failed: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report.to_summary_dict(), indent=2))
    else:
        report.print_summary()
        # If --all or no specific flags, show errors by default
        show_all = args.all
        show_errors = args.errors or show_all or (not args.errors and not args.warnings and not args.suggestions)
        show_warnings = args.warnings or show_all
        show_suggestions = args.suggestions or show_all

        if show_errors:
            report.print_errors()
        if show_warnings:
            report.print_warnings()
        if show_suggestions:
            report.print_suggestions()

    # Only return error if there is an issue loading the report
    return 0


def main() -> int:
    """Validate, summarize, or compare spec-review reports."""
    if len(sys.argv) > 1 and sys.argv[1] == "compare":
        return _run_compare(_compare_parser().parse_args())
    if len(sys.argv) > 1 and sys.argv[1] == "--schema":
        print(json.dumps(SpecReviewReport.model_json_schema(), indent=2))
        return 0
    return _run_validation(_validation_parser().parse_args())


if __name__ == "__main__":
    sys.exit(main())
