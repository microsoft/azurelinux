"""Shared utilities for rendered-spec checks."""

from __future__ import annotations

MAX_COMPONENTS_IN_COMMAND = 30


def render_command(components: list[str], *, use_all: bool = False) -> str:
    """Build the azldev command that restores rendered specs."""
    if use_all or len(components) > MAX_COMPONENTS_IN_COMMAND:
        return "azldev component render -a --clean-stale"
    return f"azldev component render {' '.join(components)}"
