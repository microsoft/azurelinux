"""Load the package publication policy used by closure validation."""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

_SOURCE_COMPONENT_PATTERN = re.compile(
    r'^\s*"(?P<package>[^"]+)"\s*,?\s*#\s*srpm:\s*(?P<component>\S+)\s*$',
    re.MULTILINE,
)


@dataclass(frozen=True, slots=True)
class PublicationPolicy:
    """Publication routing relevant to binary repository closure."""

    base_components: frozenset[str]
    sdk_exception_sources: dict[str, str]

    @property
    def sdk_exceptions(self) -> frozenset[str]:
        """Return binary packages explicitly carved out into SDK."""
        return frozenset(self.sdk_exception_sources)


def parse_publication_policy(text: str, *, source: str) -> PublicationPolicy:
    """Parse publication policy and require source ownership for exceptions."""
    try:
        data = tomllib.loads(text)
        base_components = data["component-groups"]["base-packages"]["components"]
        sdk_exceptions = data["package-groups"]["exceptions-packages"]["packages"]
    except (KeyError, TypeError, tomllib.TOMLDecodeError) as exc:
        raise RuntimeError(f"Failed to parse publication policy {source}: {exc}") from exc

    expected_top_level = {
        "component-groups",
        "default-component-config",
        "package-groups",
    }
    expected_component_groups = {"base-packages"}
    expected_package_groups = {"exceptions-packages"}
    if set(data) != expected_top_level:
        raise RuntimeError(
            f"Publication policy {source} has unsupported top-level sections: "
            f"{sorted(set(data) ^ expected_top_level)}"
        )
    if set(data["component-groups"]) != expected_component_groups:
        raise RuntimeError(
            f"Publication policy {source} has unsupported component groups: "
            f"{sorted(set(data['component-groups']) ^ expected_component_groups)}"
        )
    if set(data["package-groups"]) != expected_package_groups:
        raise RuntimeError(
            f"Publication policy {source} has unsupported package groups: "
            f"{sorted(set(data['package-groups']) ^ expected_package_groups)}"
        )
    try:
        default_rpm_channel = data["default-component-config"]["publish"]["rpm-channel"]
        base_rpm_channel = data["component-groups"]["base-packages"][
            "default-component-config"
        ]["publish"]["rpm-channel"]
        exception_rpm_channel = data["package-groups"]["exceptions-packages"][
            "default-package-config"
        ]["publish"]["rpm-channel"]
    except (KeyError, TypeError) as exc:
        raise RuntimeError(
            f"Publication policy {source} has unsupported publish-channel configuration"
        ) from exc
    if (
        default_rpm_channel != "rpm-sdk"
        or base_rpm_channel != "rpm-base"
        or exception_rpm_channel != "rpm-sdk"
    ):
        raise RuntimeError(
            f"Publication policy {source} uses unsupported RPM channel semantics"
        )

    if not isinstance(base_components, list) or not all(
        isinstance(value, str) and value for value in base_components
    ):
        raise RuntimeError(f"Publication policy {source} has a malformed base component list")
    if not isinstance(sdk_exceptions, list) or not all(
        isinstance(value, str) and value for value in sdk_exceptions
    ):
        raise RuntimeError(f"Publication policy {source} has a malformed SDK exception list")

    duplicate_base = {value for value in base_components if base_components.count(value) > 1}
    duplicate_exceptions = {
        value for value in sdk_exceptions if sdk_exceptions.count(value) > 1
    }
    if duplicate_base:
        raise RuntimeError(
            f"Publication policy {source} repeats base components: {sorted(duplicate_base)}"
        )
    if duplicate_exceptions:
        raise RuntimeError(
            f"Publication policy {source} repeats SDK exceptions: {sorted(duplicate_exceptions)}"
        )

    source_components = {
        match.group("package"): match.group("component")
        for match in _SOURCE_COMPONENT_PATTERN.finditer(text)
    }
    missing_sources = set(sdk_exceptions) - set(source_components)
    unexpected_sources = set(source_components) - set(sdk_exceptions)
    if missing_sources or unexpected_sources:
        details: list[str] = []
        if missing_sources:
            details.append(f"missing '# srpm:' ownership: {sorted(missing_sources)}")
        if unexpected_sources:
            details.append(f"orphan '# srpm:' ownership: {sorted(unexpected_sources)}")
        raise RuntimeError(f"Publication policy {source} is ambiguous ({'; '.join(details)})")

    return PublicationPolicy(
        base_components=frozenset(base_components),
        sdk_exception_sources=source_components,
    )


def load_publication_policy(path: Path) -> PublicationPolicy:
    """Load publication policy from disk."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Failed to read publication policy {path}: {exc}") from exc
    return parse_publication_policy(text, source=str(path))
