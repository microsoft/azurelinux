# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Tests for lock-file drift parsing and rendering."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from types import ModuleType

_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "post_locks_comment.py"


@pytest.fixture(scope="module")
def locks_comment() -> ModuleType:
    """Load the lock-comment script as a module."""
    spec = importlib.util.spec_from_file_location("_test_post_locks_comment", _SCRIPT_PATH)
    if spec is None or spec.loader is None:
        pytest.fail(f"Unable to load module spec for {_SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_json(tmp_path: Path, value: object) -> Path:
    path = tmp_path / "update-output.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_parse_update_output_filters_unchanged_entries(
    locks_comment: ModuleType,
    tmp_path: Path,
) -> None:
    """Return only changed components while preserving optional commits."""
    path = _write_json(
        tmp_path,
        [
            {"component": "changed", "changed": True, "upstreamCommit": "abcdef"},
            {"component": "unchanged", "changed": False},
        ],
    )

    assert locks_comment.parse_update_output(path) == [
        {"component": "changed", "changed": True, "upstreamCommit": "abcdef"}
    ]


@pytest.mark.parametrize(
    "entry",
    [
        {"changed": True},
        {"component": "example"},
        {"component": 42, "changed": True},
        {"component": "example", "changed": "yes"},
        {"component": "example", "changed": True, "upstreamCommit": 42},
    ],
)
def test_parse_update_output_rejects_invalid_entry_fields(
    locks_comment: ModuleType,
    tmp_path: Path,
    entry: object,
) -> None:
    """Reject entries whose required or optional fields have invalid types."""
    path = _write_json(tmp_path, [entry])

    with pytest.raises(SystemExit, match="unexpected shape"):
        locks_comment.parse_update_output(path)


def test_format_comment_renders_typed_entries(locks_comment: ModuleType) -> None:
    """Render component names and optional upstream commits."""
    comment = locks_comment.format_comment(
        [
            {"component": "alpha", "changed": True, "upstreamCommit": "abcdef"},
            {"component": "beta", "changed": True},
        ]
    )

    assert "| `alpha` | `abcdef` |" in comment
    assert "| `beta` | `-` |" in comment
