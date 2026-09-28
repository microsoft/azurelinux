# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Tests for component render-set computation."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from types import ModuleType

_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "compute_render_set.py"


@pytest.fixture(scope="module")
def render_set() -> ModuleType:
    """Load the render-set script as a module."""
    spec = importlib.util.spec_from_file_location("_test_compute_render_set", _SCRIPT_PATH)
    if spec is None or spec.loader is None:
        pytest.fail(f"Unable to load module spec for {_SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_json(tmp_path: Path, value: object) -> Path:
    path = tmp_path / "changed-components.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_load_entries_preserves_optional_fields(
    render_set: ModuleType,
    tmp_path: Path,
) -> None:
    """Accept entries with only the component field or all known fields."""
    path = _write_json(
        tmp_path,
        [
            {"component": "minimal"},
            {
                "component": "complete",
                "changeType": "changed",
                "sourcesChange": True,
            },
        ],
    )

    assert render_set._load_entries(path) == [  # noqa: SLF001 - tests parsing boundary
        {"component": "minimal"},
        {
            "component": "complete",
            "changeType": "changed",
            "sourcesChange": True,
        },
    ]


@pytest.mark.parametrize(
    "value",
    [
        {},
        ["component"],
        [{"changeType": "changed"}],
        [{"component": 42}],
        [{"component": "example", "changeType": 42}],
        [{"component": "example", "sourcesChange": "yes"}],
    ],
)
def test_load_entries_rejects_invalid_shapes(
    render_set: ModuleType,
    tmp_path: Path,
    value: object,
) -> None:
    """Reject malformed top-level values and component entries."""
    path = _write_json(tmp_path, value)

    with pytest.raises(TypeError, match=r"changed-components|invalid"):
        render_set._load_entries(path)  # noqa: SLF001 - tests parsing boundary


def test_from_changed_preserves_selection_rules(render_set: ModuleType) -> None:
    """Include identity changes and source drift while excluding deletions."""
    entries = [
        {"component": "added", "changeType": "added"},
        {"component": "source-drift", "changeType": "unchanged", "sourcesChange": True},
        {"component": "unchanged", "changeType": "unchanged"},
        {"component": "deleted", "changeType": "deleted", "sourcesChange": True},
        {"component": "future-type", "changeType": "future"},
    ]

    assert render_set.from_changed(entries) == [
        "added",
        "source-drift",
        "future-type",
    ]


def test_from_specs_diff_filters_unknown_and_deleted_components(
    render_set: ModuleType,
    tmp_path: Path,
) -> None:
    """Extract only known renderable components from changed spec paths."""
    diff_path = tmp_path / "specs-diff.txt"
    diff_path.write_text(
        "specs/a/alpha/alpha.spec\n"
        "specs/d/deleted/deleted.spec\n"
        "specs/u/unknown/unknown.spec\n"
        "README.md\n",
        encoding="utf-8",
    )

    assert render_set.from_specs_diff(
        diff_path,
        Path("specs"),
        {"alpha"},
    ) == ["alpha"]
