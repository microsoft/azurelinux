# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Behavioral tests for spec-review validation and comment formatting."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = REPO_ROOT / "scripts" / "ci" / "spec-review"
SCHEMA_SCRIPT = SCRIPT_DIR / "spec_review_schema.py"
FORMAT_SCRIPT = SCRIPT_DIR / "format_pr_comment.py"
ANNOTATIONS_SCRIPT = SCRIPT_DIR / "create_check_annotations.py"
INVALID_REPORT_EXIT = 2


@pytest.fixture
def reports() -> dict[str, dict[str, object]]:
    """Return reviewer and synthesis reports covering every finding category."""
    return {
        "a": {
            "spec_reviews": [
                {
                    "spec_file": "base/a.spec",
                    "errors": [
                        {
                            "description": "shared error",
                            "citation": "https://example.com/e",
                        }
                    ],
                    "warnings": [
                        {
                            "description": "dropped warning",
                            "citation": "N/A",
                        }
                    ],
                    "suggestions": [],
                }
            ]
        },
        "b": {
            "spec_reviews": [
                {
                    "spec_file": "base/a.spec",
                    "errors": [
                        {
                            "description": "shared error",
                            "citation": "https://example.com/e",
                        }
                    ],
                    "warnings": [],
                    "suggestions": [{"description": "kept suggestion"}],
                }
            ]
        },
        "final": {
            "spec_reviews": [
                {
                    "spec_file": "base/a.spec",
                    "errors": [
                        {
                            "description": "shared error",
                            "citation": "https://example.com/e",
                        }
                    ],
                    "warnings": [{"description": "synth warning"}],
                    "suggestions": [{"description": "kept suggestion"}],
                }
            ]
        },
    }


def _write_report(
    tmp_path: Path,
    name: str,
    report: dict[str, object],
) -> Path:
    path = tmp_path / f"{name}.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    return path


def _run(script: Path, *args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *(str(arg) for arg in args)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_validate_all_prints_current_report_format(
    tmp_path: Path,
    reports: dict[str, dict[str, object]],
) -> None:
    """Print aggregate counts and each selected finding category."""
    report_path = _write_report(tmp_path, "report", reports["a"])

    result = _run(SCHEMA_SCRIPT, report_path, "--all")

    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == (
        "ERRORS FOUND\n"
        "Specs: 1 | Errors: 1 | Warnings: 1 | Suggestions: 0\n"
        "\n"
        "a.spec:\n"
        "  [error] shared error\n"
        "     https://example.com/e\n"
        "\n"
        "a.spec:\n"
        "  [warning] dropped warning\n"
    )


def test_validate_json_prints_machine_readable_summary(
    tmp_path: Path,
    reports: dict[str, dict[str, object]],
) -> None:
    """Emit the stable aggregate JSON consumed by scripts."""
    report_path = _write_report(tmp_path, "report", reports["a"])

    result = _run(SCHEMA_SCRIPT, report_path, "--json")

    assert result.returncode == 0
    assert result.stderr == ""
    assert json.loads(result.stdout) == {
        "specs": 1,
        "errors": 1,
        "warnings": 1,
        "suggestions": 0,
        "blocking": True,
    }


def test_schema_mode_prints_report_schema() -> None:
    """Expose the schema used to instruct and validate review agents."""
    result = _run(SCHEMA_SCRIPT, "--schema")

    assert result.returncode == 0
    assert result.stderr == ""
    schema = json.loads(result.stdout)
    assert schema["title"] == "SpecReviewReport"
    assert {"Finding", "SpecReview"} <= set(schema["$defs"])


def test_compare_prints_current_model_diff(
    tmp_path: Path,
    reports: dict[str, dict[str, object]],
) -> None:
    """Show findings retained, dropped, and added by synthesis."""
    report_a = _write_report(tmp_path, "a", reports["a"])
    report_b = _write_report(tmp_path, "b", reports["b"])
    report_final = _write_report(tmp_path, "final", reports["final"])

    result = _run(
        SCHEMA_SCRIPT,
        "compare",
        report_a,
        report_b,
        report_final,
        "--label-a",
        "Reviewer A (model-a)",
        "--label-b",
        "Reviewer B (model-b)",
        "--label-final",
        "Synthesized (model-c)",
    )

    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == (
        "┌─────────────────────────┬────────┬──────────┬─────────────┐\n"
        "│ Model                   │ Errors │ Warnings │ Suggestions │\n"
        "├─────────────────────────┼────────┼──────────┼─────────────┤\n"
        "│ Reviewer A (model-a)    │      1 │        1 │           0 │\n"
        "│ Reviewer B (model-b)    │      1 │        0 │           1 │\n"
        "│ Synthesized (model-c)   │      1 │        1 │           1 │\n"
        "└─────────────────────────┴────────┴──────────┴─────────────┘\n"
        "\n"
        "── ERROR ERRORS ──\n"
        "  Kept (1):\n"
        "    + [A+B] a.spec: shared error\n"
        "\n"
        "── WARNING WARNINGS ──\n"
        "  Dropped (1):\n"
        "    - [A] a.spec: dropped warning\n"
        "  Added by synthesizer (1):\n"
        "    + a.spec: synth warning\n"
        "\n"
        "── SUGGESTION SUGGESTIONS ──\n"
        "  Kept (1):\n"
        "    + [B] a.spec: kept suggestion\n"
        "\n"
    )


def test_format_comment_prints_current_markdown(
    tmp_path: Path,
    reports: dict[str, dict[str, object]],
) -> None:
    """Render counts, links, findings, citations, and raw JSON."""
    report = reports["final"]
    report_path = _write_report(tmp_path, "final", report)

    result = _run(
        FORMAT_SCRIPT,
        report_path,
        "--repo",
        "microsoft/azurelinux",
        "--sha",
        "abc123",
        "--repo-root",
        REPO_ROOT,
    )

    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == (
        "<!-- SPEC_REVIEW_BOT -->\n"
        "## ❌ **Spec Review Failed**\n"
        "\n"
        "| Type | Count |\n"
        "|------|-------|\n"
        "| Errors | 1 |\n"
        "| Warnings | 1 |\n"
        "| Suggestions | 1 |\n"
        "\n"
        "🛠️ Debug locally: [scripts/ci/spec-review/README.md]"
        "(https://github.com/microsoft/azurelinux/blob/abc123/"
        "scripts/ci/spec-review/README.md)\n"
        "\n"
        "### [`a.spec`](https://github.com/microsoft/azurelinux/blob/abc123/base/a.spec)\n"
        "\n"
        "<details>\n"
        "<summary>❌ Errors (1)</summary>\n"
        "\n"
        "- shared error\n"
        "  - 📖 [https://example.com/e](https://example.com/e)\n"
        "\n"
        "</details>\n"
        "\n"
        "<details>\n"
        "<summary>⚠️ Warnings (1)</summary>\n"
        "\n"
        "- synth warning\n"
        "\n"
        "</details>\n"
        "\n"
        "<details>\n"
        "<summary>💡 Suggestions (1)</summary>\n"
        "\n"
        "- kept suggestion\n"
        "\n"
        "</details>\n"
        "\n"
        "<details>\n"
        "<summary>📄 Raw JSON Report</summary>\n"
        "\n"
        "```json\n"
        f"{json.dumps(report, indent=2)}\n"
        "```\n"
        "\n"
        "</details>\n"
    )


def test_format_comment_prints_all_clear_for_empty_findings(tmp_path: Path) -> None:
    """Render the all-clear message when no reviewed spec has findings."""
    report: dict[str, object] = {
        "spec_reviews": [
            {
                "spec_file": "base/empty.spec",
                "errors": [],
                "warnings": [],
                "suggestions": [],
            }
        ]
    }
    report_path = _write_report(tmp_path, "empty", report)

    result = _run(
        FORMAT_SCRIPT,
        report_path,
        "--repo",
        "microsoft/azurelinux",
        "--sha",
        "abc123",
        "--repo-root",
        REPO_ROOT,
    )

    assert result.returncode == 0
    assert "## ✅ **Spec Review Passed**" in result.stdout
    assert "✨ No issues found in any reviewed spec files." in result.stdout
    assert "### [`empty.spec`]" not in result.stdout


def test_format_comment_truncates_oversized_raw_json(tmp_path: Path) -> None:
    """Avoid embedding raw JSON that would exceed GitHub's comment limit."""
    report: dict[str, object] = {
        "spec_reviews": [],
        "padding": "x" * 51_000,
    }
    report_path = _write_report(tmp_path, "large", report)

    result = _run(
        FORMAT_SCRIPT,
        report_path,
        "--repo",
        "microsoft/azurelinux",
        "--sha",
        "abc123",
    )

    assert result.returncode == 0
    assert "Report too large to display inline" in result.stdout
    assert "x" * 100 not in result.stdout


def test_annotations_json_preserves_finding_fields(
    tmp_path: Path,
    reports: dict[str, dict[str, object]],
) -> None:
    """Render finding data for the GitHub Checks API."""
    report_path = _write_report(tmp_path, "report", reports["a"])

    result = _run(
        ANNOTATIONS_SCRIPT,
        report_path,
        "--json",
        "--repo-root",
        REPO_ROOT,
    )

    assert result.returncode == 0
    assert result.stderr == ""
    assert json.loads(result.stdout) == [
        {
            "path": "base/a.spec",
            "start_line": 1,
            "end_line": 1,
            "annotation_level": "failure",
            "message": "shared error\n\nRef: https://example.com/e",
            "title": "Spec Error",
        },
        {
            "path": "base/a.spec",
            "start_line": 1,
            "end_line": 1,
            "annotation_level": "warning",
            "message": "dropped warning",
            "title": "Spec Warning",
        },
    ]


def test_annotations_workflow_commands_escape_metadata(tmp_path: Path) -> None:
    """Escape workflow-command delimiters in paths and finding messages."""
    report: dict[str, object] = {
        "spec_reviews": [
            {
                "spec_file": "base/a,b.spec",
                "errors": [
                    {
                        "description": "bad: value\nnext",
                        "citation": "https://example.com/a,b",
                        "line": 7,
                    }
                ],
                "warnings": [],
                "suggestions": [],
            }
        ]
    }
    report_path = _write_report(tmp_path, "report", report)

    result = _run(
        ANNOTATIONS_SCRIPT,
        report_path,
        "--workflow-commands",
        "--repo-root",
        REPO_ROOT,
    )

    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == (
        "::error file=base/a%2Cb.spec,line=7::"
        "bad%3A value%0Anext (Ref: https%3A//example.com/a%2Cb)\n"
    )


def test_invalid_json_fails_cleanly(tmp_path: Path) -> None:
    """Reject malformed report JSON without producing normal output."""
    report_path = tmp_path / "invalid.json"
    report_path.write_text("{", encoding="utf-8")

    result = _run(SCHEMA_SCRIPT, report_path)

    assert result.returncode == INVALID_REPORT_EXIT
    assert result.stdout == ""
    assert result.stderr.startswith("Invalid JSON:")


@pytest.mark.parametrize("mode", ["validate", "compare"])
def test_invalid_encoding_fails_cleanly(tmp_path: Path, mode: str) -> None:
    """Reject non-UTF-8 reports through the documented validation path."""
    report_path = tmp_path / "invalid.json"
    report_path.write_bytes(b"\xff")
    args = (
        (report_path,)
        if mode == "validate"
        else ("compare", report_path, report_path, report_path)
    )

    result = _run(SCHEMA_SCRIPT, *args)

    assert result.returncode == INVALID_REPORT_EXIT
    assert result.stdout == ""
    assert result.stderr.startswith("Validation failed:")
