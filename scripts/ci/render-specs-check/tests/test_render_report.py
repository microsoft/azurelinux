# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Tests for rendered-spec report construction and formatting."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import check_rendered_specs
import post_render_comment

if TYPE_CHECKING:
    from _report_types import ContentDiff, RenderReport


def test_build_report_assigns_components() -> None:
    """Build the exact report shape consumed by the PR comment renderer."""
    content_diffs: list[ContentDiff] = [
        {
            "path": "specs/a/alpha/alpha.spec",
            "component": "alpha",
            "diff": "changed",
        }
    ]

    report = check_rendered_specs.build_report(
        content_diffs,
        ["specs/b/beta/beta.spec"],
        ["specs/g/gamma/gamma.spec"],
        Path("specs"),
    )

    assert report == {
        "content_diffs": content_diffs,
        "extra_files": [
            {
                "path": "specs/b/beta/beta.spec",
                "component": "beta",
            }
        ],
        "missing_files": [
            {
                "path": "specs/g/gamma/gamma.spec",
                "component": "gamma",
            }
        ],
    }


def test_format_comment_renders_every_report_category() -> None:
    """Render content, extra, and missing entries from a shared report."""
    report: RenderReport = {
        "content_diffs": [
            {
                "path": "specs/a/alpha/alpha.spec",
                "component": "alpha",
                "diff": "-old\n+new",
            }
        ],
        "extra_files": [
            {
                "path": "specs/b/beta/beta.spec",
                "component": "beta",
            }
        ],
        "missing_files": [
            {
                "path": "specs/g/gamma/gamma.spec",
                "component": "gamma",
            }
        ],
    }

    comment = post_render_comment.format_comment(report)

    assert "azldev component render -a --clean-stale" in comment
    assert "`specs/a/alpha/alpha.spec`" in comment
    assert "-old\n+new" in comment
    assert "- `specs/b/beta/beta.spec`" in comment
    assert "- `specs/g/gamma/gamma.spec`" in comment
