#!/usr/bin/env python3
"""
Validate spec review report JSON and print findings.

Usage:
    python spec_review_schema.py report.json [--errors] [--warnings] [--json]

Exit codes:
    0 = Valid report (regardless of findings)
    2 = Invalid JSON, file error, or schema validation failure
"""

import json
import sys
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Finding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str = Field(..., min_length=1)
    citation: Optional[str] = None
    line: Optional[int] = Field(None, ge=1, description="Line number in the spec file")

    @field_validator("citation", mode="before")
    @classmethod
    def normalize_citation(cls, v: Optional[str]) -> Optional[str]:
        if v in (None, "N/A", "n/a", ""):
            return None
        return v


class SpecReview(BaseModel):
    model_config = ConfigDict(extra="forbid")

    spec_file: str
    errors: list[Finding] = Field(default_factory=list)
    warnings: list[Finding] = Field(default_factory=list)
    suggestions: list[Finding] = Field(default_factory=list)

    @property
    def spec_name(self) -> str:
        return Path(self.spec_file).name


class SpecReviewReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    spec_reviews: list[SpecReview] = Field(..., min_length=1)

    @classmethod
    def from_file(cls, path: str | Path) -> "SpecReviewReport":
        with open(path, encoding="utf-8") as f:
            return cls.model_validate(json.load(f))

    @property
    def total_errors(self) -> int:
        return sum(len(r.errors) for r in self.spec_reviews)

    @property
    def total_warnings(self) -> int:
        return sum(len(r.warnings) for r in self.spec_reviews)

    @property
    def total_suggestions(self) -> int:
        return sum(len(r.suggestions) for r in self.spec_reviews)

    @property
    def has_errors(self) -> bool:
        return self.total_errors > 0

    def print_summary(self):
        status = "❌ ERRORS FOUND" if self.has_errors else "✅ No errors"
        print(f"{status}")
        print(f"Specs: {len(self.spec_reviews)} | Errors: {self.total_errors} | Warnings: {self.total_warnings} | Suggestions: {self.total_suggestions}")

    def print_errors(self):
        for review in self.spec_reviews:
            if review.errors:
                print(f"\n{review.spec_name}:")
                for e in review.errors:
                    print(f"  ❌ {e.description}")
                    if e.citation:
                        print(f"     {e.citation}")

    def print_warnings(self):
        for review in self.spec_reviews:
            if review.warnings:
                print(f"\n{review.spec_name}:")
                for w in review.warnings:
                    print(f"  ⚠️  {w.description}")
                    if w.citation:
                        print(f"     {w.citation}")

    def print_suggestions(self):
        for review in self.spec_reviews:
            if review.suggestions:
                print(f"\n{review.spec_name}:")
                for s in review.suggestions:
                    print(f"  💡 {s.description}")
                    if s.citation:
                        print(f"     {s.citation}")

    def to_summary_dict(self) -> dict:
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


def compare_reports(
    report_a: SpecReviewReport,
    report_b: SpecReviewReport,
    report_final: SpecReviewReport,
    label_a: str = "Reviewer A",
    label_b: str = "Reviewer B",
    label_final: str = "Synthesized",
) -> None:
    """Print a human-readable comparison of two reviewer reports and the synthesis."""
    severities = ["errors", "warnings", "suggestions"]
    icons = {"errors": "❌", "warnings": "⚠️ ", "suggestions": "💡"}

    # --- Per-model summary table ---
    col_w = max(len(label_a), len(label_b), len(label_final), 5) + 2
    print(f"┌─{'─' * col_w}─┬────────┬──────────┬─────────────┐")
    print(f"│ {'Model':<{col_w}} │ Errors │ Warnings │ Suggestions │")
    print(f"├─{'─' * col_w}─┼────────┼──────────┼─────────────┤")
    for label, report in [(label_a, report_a), (label_b, report_b), (label_final, report_final)]:
        print(f"│ {label:<{col_w}} │ {report.total_errors:>6} │ {report.total_warnings:>8} │ {report.total_suggestions:>11} │")
    print(f"└─{'─' * col_w}─┴────────┴──────────┴─────────────┘")
    print()

    # --- Per-severity diff ---
    for sev in severities:
        set_a = _findings_set(report_a.spec_reviews, sev)
        set_b = _findings_set(report_b.spec_reviews, sev)
        set_final = _findings_set(report_final.spec_reviews, sev)

        all_keys = set(set_a) | set(set_b)
        kept = all_keys & set(set_final)
        dropped = all_keys - set(set_final)
        added = set(set_final) - all_keys  # synthesizer invented new ones

        if not any([kept, dropped, added]):
            continue

        print(f"── {icons[sev]} {sev.upper()} ──")

        if kept:
            print(f"  Kept ({len(kept)}):")
            for spec, desc in sorted(kept):
                sources = []
                if (spec, desc) in set_a:
                    sources.append("A")
                if (spec, desc) in set_b:
                    sources.append("B")
                print(f"    ✓ [{'+'.join(sources)}] {spec}: {desc}")

        if dropped:
            print(f"  Dropped ({len(dropped)}):")
            for spec, desc in sorted(dropped):
                sources = []
                if (spec, desc) in set_a:
                    sources.append("A")
                if (spec, desc) in set_b:
                    sources.append("B")
                print(f"    ✗ [{'+'.join(sources)}] {spec}: {desc}")

        if added:
            print(f"  Added by synthesizer ({len(added)}):")
            for spec, desc in sorted(added):
                print(f"    + {spec}: {desc}")

        print()


def main() -> int:
    import argparse

    # Route to compare subcommand if first arg is "compare"
    if len(sys.argv) > 1 and sys.argv[1] == "compare":
        parser = argparse.ArgumentParser(description="Compare multi-model spec review reports")
        parser.add_argument("_cmd", metavar="compare")
        parser.add_argument("report_a", type=Path, help="Report from reviewer A")
        parser.add_argument("report_b", type=Path, help="Report from reviewer B")
        parser.add_argument("report_final", type=Path, help="Final synthesized report")
        parser.add_argument("--label-a", default="Reviewer A", help="Display label for reviewer A")
        parser.add_argument("--label-b", default="Reviewer B", help="Display label for reviewer B")
        parser.add_argument("--label-final", default="Synthesized", help="Display label for final report")
        args = parser.parse_args()

        try:
            ra = _load_report(args.report_a)
            rb = _load_report(args.report_b)
            rf = _load_report(args.report_final)
        except FileNotFoundError as e:
            print(f"❌ File not found: {e}", file=sys.stderr)
            return 2
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}", file=sys.stderr)
            return 2
        except Exception as e:
            print(f"❌ Validation failed: {e}", file=sys.stderr)
            return 2

        compare_reports(ra, rb, rf, args.label_a, args.label_b, args.label_final)
        return 0

    # Handle --schema flag before argparse to avoid positional arg requirement
    if len(sys.argv) > 1 and sys.argv[1] == "--schema":
        print(json.dumps(SpecReviewReport.model_json_schema(), indent=2))
        return 0

    # Original validate behavior
    parser = argparse.ArgumentParser(description="Validate spec review report")
    parser.add_argument("file", type=Path, help="Path to report JSON")
    parser.add_argument("--errors", action="store_true", help="Print errors", default=False)
    parser.add_argument("--warnings", action="store_true", help="Print warnings", default=False)
    parser.add_argument("--suggestions", action="store_true", help="Print suggestions", default=False)
    parser.add_argument("--all", action="store_true", help="Print all findings", default=False)
    parser.add_argument("--json", action="store_true", help="Output summary as JSON", default=False)

    args = parser.parse_args()

    try:
        report = SpecReviewReport.from_file(args.file)
    except FileNotFoundError:
        print(f"❌ File not found: {args.file}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"❌ Validation failed: {e}", file=sys.stderr)
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


if __name__ == "__main__":
    sys.exit(main())
