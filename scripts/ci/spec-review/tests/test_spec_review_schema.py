# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Tests for spec-review input error handling."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from types import ModuleType

_SCRIPT = Path(__file__).resolve().parents[1] / "spec_review_schema.py"
_VALIDATION_FAILURE_EXIT_CODE = 2


def _load_module() -> ModuleType:
    """Load the spec-review schema entrypoint."""
    spec = importlib.util.spec_from_file_location("_test_spec_review_schema", _SCRIPT)
    if spec is None or spec.loader is None:
        pytest.fail(f"Unable to load module spec for {_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_schema_loads_without_sys_modules_registration() -> None:
    """Support importlib callers that execute the module without registering it."""
    module_name = "_test_unregistered_spec_review_schema"
    spec = importlib.util.spec_from_file_location(module_name, _SCRIPT)
    if spec is None or spec.loader is None:
        pytest.fail(f"Unable to load module spec for {_SCRIPT}")
    module = importlib.util.module_from_spec(spec)

    assert module_name not in sys.modules
    spec.loader.exec_module(module)
    assert module.ComparisonLabels().final == "Synthesized"


@pytest.mark.parametrize("compare", [False, True])
def test_oversized_json_integer_is_a_validation_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    *,
    compare: bool,
) -> None:
    """Return the documented validation exit code for oversized integers."""
    digit_limit = sys.get_int_max_str_digits()
    if digit_limit == 0:
        pytest.skip("Python integer digit limit is disabled")

    report = tmp_path / "report.json"
    oversized_integer = "1" + ("0" * digit_limit)
    report.write_text(f'{{"spec_reviews": [{oversized_integer}]}}', encoding="utf-8")

    module = _load_module()
    argv = [str(_SCRIPT), str(report)]
    if compare:
        argv = [str(_SCRIPT), "compare", str(report), str(report), str(report)]
    monkeypatch.setattr(sys, "argv", argv)

    assert module.main() == _VALIDATION_FAILURE_EXIT_CODE
    assert "Validation failed:" in capsys.readouterr().err


def test_compare_reports_preserves_summary_and_finding_categories(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Report kept, dropped, and synthesized-only findings with their sources."""
    module = _load_module()

    def report(*descriptions: str) -> object:
        return module.SpecReviewReport.model_validate(
            {
                "spec_reviews": [
                    {
                        "spec_file": "example.spec",
                        "errors": [{"description": description} for description in descriptions],
                    }
                ]
            }
        )

    module.compare_reports(
        report("shared", "only-a"),
        report("shared", "only-b"),
        report("shared", "synthesized"),
        module.ComparisonLabels("Alpha", "Beta", "Final"),
    )

    output = capsys.readouterr().out
    assert "│ Alpha   │      2 │        0 │           0 │" in output
    assert "│ Beta    │      2 │        0 │           0 │" in output
    assert "│ Final   │      2 │        0 │           0 │" in output
    assert "    + [A+B] example.spec: shared" in output
    assert "    - [A] example.spec: only-a" in output
    assert "    - [B] example.spec: only-b" in output
    assert "    + example.spec: synthesized" in output
