# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Tests for mutable kernel policy updates."""

from __future__ import annotations

from typing import TYPE_CHECKING

from kernel_config_checker.add_config import _add_config_to_data, _insert_or_replace

if TYPE_CHECKING:
    import pytest
    from kernel_config_checker.add_config import KernelConfigData, SchemaData


def _config(name: str, value: str = "y") -> KernelConfigData:
    return {
        "name": name,
        "values": [{"architecture": "x86_64", "value": value}],
        "justification": "test",
    }


def test_add_config_creates_default_section() -> None:
    """Create the default section when updating an empty document."""
    data: SchemaData = {}
    config = _config("CONFIG_EXAMPLE")

    section = _add_config_to_data(data, config, None)

    assert section == "default section"
    assert data == {
        "default": {
            "name": "default",
            "kernel_configs": [config],
        }
    }


def test_add_config_creates_named_override() -> None:
    """Create a requested override when it is not already present."""
    data: SchemaData = {
        "default": {
            "name": "default",
            "kernel_configs": [],
        }
    }
    config = _config("CONFIG_EXAMPLE")

    section = _add_config_to_data(data, config, "kernel-azure")

    assert section == "'kernel-azure' override section"
    assert data.get("overrides") == [
        {
            "name": "kernel-azure",
            "kernel_configs": [config],
        }
    ]


def test_insert_or_replace_preserves_declined_duplicate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Leave an existing config unchanged when replacement is declined."""
    existing = _config("CONFIG_EXAMPLE")
    configs = [existing]
    monkeypatch.setattr("builtins.input", lambda _prompt: "n")

    assert not _insert_or_replace(configs, _config("CONFIG_EXAMPLE", "m"))
    assert configs == [existing]


def test_insert_or_replace_updates_approved_duplicate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Replace an existing config after explicit approval."""
    configs = [_config("CONFIG_EXAMPLE")]
    replacement = _config("CONFIG_EXAMPLE", "m")
    monkeypatch.setattr("builtins.input", lambda _prompt: "y")

    assert _insert_or_replace(configs, replacement)
    assert configs == [replacement]
