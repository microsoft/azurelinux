# SPDX-License-Identifier: MIT
"""Pytest plugin for Azure Linux image validation.

Registered via ``[project.entry-points."pytest11"]`` so that custom CLI
options are known to pytest *before* rootdir determination. This prevents
pytest from misinterpreting ``--image-path <existing-file>`` as a
positional test-path argument.
"""

from __future__ import annotations

import pytest

# Map file-extension suffixes to image types for auto-detection.
_EXT_TO_TYPE: dict[str, str] = {
    ".raw": "vm",
    ".vhd": "vm",
    ".vhdx": "vm",
    ".vhdfixed": "vm",
    ".qcow2": "vm",
    ".oci.tar.xz": "container",
    ".tar.xz": "container",
    ".tar.gz": "container",
    ".tar": "container",
}

# Capabilities that imply an image type.
_CAPABILITY_TO_TYPE: dict[str, str] = {
    "machine-bootable": "vm",
    "container": "container",
}


def detect_image_type(image_path: str) -> str | None:
    """Guess image type from *image_path* file extension."""
    lower = image_path.lower()
    # Try longest suffixes first so ".oci.tar.xz" matches before ".xz".
    for suffix in sorted(_EXT_TO_TYPE, key=len, reverse=True):
        if lower.endswith(suffix):
            return _EXT_TO_TYPE[suffix]
    return None


def derive_image_type_from_capabilities(capabilities: set[str]) -> str | None:
    """Infer image type from capability set."""
    for cap, itype in _CAPABILITY_TO_TYPE.items():
        if cap in capabilities:
            return itype
    return None


def parse_capabilities(raw: str | None) -> set[str]:
    """Parse a comma-separated capabilities string into a set."""
    if not raw:
        return set()
    return {c.strip() for c in raw.split(",") if c.strip()}


def pytest_addoption(parser) -> None:  # type: ignore[no-untyped-def]
    group = parser.getgroup("image", "Azure Linux image validation")
    group.addoption(
        "--image-path",
        required=True,
        help="Path to the built image artifact (VHD, raw, OCI tar.xz, etc.)",
    )
    group.addoption(
        "--image-name",
        default=None,
        help="Image name (e.g. vm-base, container-base). Used for logging "
        "and for filtering tests marked with @pytest.mark.image.",
    )
    group.addoption(
        "--image-type",
        choices=("vm", "container"),
        default=None,
        help=(
            "Image type: 'vm' or 'container'. "
            "If omitted, derived from --capabilities or --image-path extension."
        ),
    )
    group.addoption(
        "--capabilities",
        default=None,
        help=(
            "Comma-separated image capabilities "
            "(e.g. 'systemd,runtime-package-management,machine-bootable'). "
            "Tests marked with @pytest.mark.require_capability are skipped "
            "when the required capability is absent."
        ),
    )
    group.addoption(
        "--workdir",
        default=None,
        help=(
            "Working directory for temporary files (mounts, extractions). "
            "Defaults to a temporary directory."
        ),
    )


def pytest_configure(config) -> None:  # type: ignore[no-untyped-def]
    """Register markers and fail fast if required native tools are missing."""
    config.addinivalue_line(
        "markers",
        "require_capability(name): skip test unless the image has the named capability",
    )
    config.addinivalue_line(
        "markers",
        "image(name): only run this test when --image-name matches the named image family "
        "(exact match, or a ``<family>-<variant>`` image-name)",
    )

    from utils.tools import check_tools

    # Determine image type early (before fixtures) so we only check
    # the tools that are actually needed for this run.
    image_type = config.getoption("--image-type", default=None)
    if image_type is None:
        caps = parse_capabilities(config.getoption("--capabilities", default=None))
        if caps:
            image_type = derive_image_type_from_capabilities(caps)
    if image_type is None:
        image_path = config.getoption("--image-path", default=None)
        if image_path:
            image_type = detect_image_type(image_path)

    missing = check_tools(when=image_type)
    if missing:
        names = ", ".join(t.name for t in missing)
        hints = "\n".join(
            f"  - {t.name}: {t.reason} (install: {t.package_hint})"
            for t in missing
        )
        raise pytest.UsageError(
            f"Missing required native tool(s): {names}\n{hints}\n\n"
            "Run 'uv run python -m utils.tools' for a full status check."
        )


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Skip tests whose marks are not satisfied."""
    # require_capability: skip if image doesn't have the required capability.
    caps = parse_capabilities(item.config.getoption("--capabilities", default=None))
    for marker in item.iter_markers("require_capability"):
        required = marker.args[0] if marker.args else None
        if required and required not in caps:
            pytest.skip(f"requires capability '{required}' (not in: {sorted(caps)})")

    # image: skip if --image-name doesn't match the marker's family.
    # Family matching: the marker's value is treated as a family name that
    # matches an image-name exactly OR matches a `<family>-<variant>` name
    # (e.g. ``image("vm-base")`` matches both ``vm-base`` and
    # ``vm-base-dev``). This lets tests under ``cases/<family>/`` apply
    # to every variant of an image without per-variant duplication.
    image_name = item.config.getoption("--image-name", default=None)
    for marker in item.iter_markers("image"):
        expected = marker.args[0] if marker.args else None
        if not expected:
            continue
        if image_name == expected:
            continue
        if image_name and image_name.startswith(expected + "-"):
            continue
        pytest.skip(
            f"test is specific to image family '{expected}' "
            f"(running: '{image_name}')"
        )


def pytest_collection_modifyitems(config, items) -> None:  # type: ignore[no-untyped-def]
    """Auto-apply ``@pytest.mark.image("<dir>")`` to tests under ``cases/<dir>/``.

    Convention: any test file inside ``cases/<image-family>/`` (at any
    depth) is automatically restricted to images whose name belongs to
    that family. The directory name is the family; an ``--image-name``
    matches the family if it equals the family exactly OR if it has the
    form ``<family>-<variant>`` (e.g. ``vm-base-dev`` matches the
    ``vm-base`` family). See :func:`pytest_runtest_setup`.

    This keeps the routing rule co-located with the directory layout —
    no per-subdir conftest, and no per-file ``pytestmark`` boilerplate
    that contributors might forget to add.

    Tests directly under ``cases/`` (no image subdir) get no marker
    and run for every image.
    """
    from pathlib import Path

    for item in items:
        parts = Path(str(item.fspath)).parts
        # Anchor on the right-most "cases" segment so the convention is
        # robust against arbitrary parent directory names.
        try:
            cases_idx = len(parts) - 1 - parts[::-1].index("cases")
        except ValueError:
            continue
        # Need at least cases/<image-family>/<file>.py to derive a family name.
        if cases_idx + 2 < len(parts):
            image_dir = parts[cases_idx + 1]
            item.add_marker(pytest.mark.image(image_dir))
