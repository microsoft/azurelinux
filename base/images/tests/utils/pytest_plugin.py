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
    ".wsl": "wsl",
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
        default=None,
        help="Path to the built image artifact (VHD, raw, OCI tar.xz, etc.). "
        "Mutually exclusive with --image-ref.",
    )
    group.addoption(
        "--image-ref",
        default=None,
        help="Container image reference (e.g. 'mcr.microsoft.com/azurelinux/base/core:4.0' "
        "or 'localhost/container-base:latest'). Podman will pull from the "
        "registry if not already present locally. "
        "Mutually exclusive with --image-path.",
    )
    group.addoption(
        "--image-name",
        default=None,
        help="Image name (e.g. vm-base, container-base). Used for logging "
        "and for filtering tests marked with @pytest.mark.image.",
    )
    group.addoption(
        "--image-type",
        choices=("vm", "container", "wsl"),
        default=None,
        help=(
            "Image type: 'vm', 'container', or 'wsl'. If omitted, derived "
            "from --capabilities or --image-path extension."
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
        help=("Working directory for temporary files (mounts, extractions). Defaults to a temporary directory."),
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
    config.addinivalue_line(
        "markers",
        "runtime: auto-applied to tests under cases/runtime/; "
        "use -m 'not runtime' to exclude runtime tests",
    )
    config.addinivalue_line(
        "markers",
        'dockerfile(path=None): build a custom image from a Dockerfile before '
        'running the test. With no args, auto-discovers "Dockerfile" in the '
        "test file's directory. With an arg, uses that path relative to the "
        "test file's directory. The image-under-test is injected as the "
        "BASE_IMAGE build arg.",
    )

    from utils.tools import check_tools

    # Validate that exactly one of --image-path or --image-ref is provided.
    image_path_raw = config.getoption("--image-path", default=None)
    image_ref_raw = config.getoption("--image-ref", default=None)
    if image_path_raw and image_ref_raw:
        raise pytest.UsageError(
            "--image-path and --image-ref are mutually exclusive. "
            "Provide one or the other."
        )
    if not image_path_raw and not image_ref_raw:
        raise pytest.UsageError(
            "Either --image-path or --image-ref is required."
        )

    # Determine image type early (before fixtures) so we only check
    # the tools that are actually needed for this run.
    image_type = config.getoption("--image-type", default=None)
    if image_type is None:
        caps = parse_capabilities(config.getoption("--capabilities", default=None))
        if caps:
            image_type = derive_image_type_from_capabilities(caps)
    if image_type is None:
        if config.getoption("--image-ref", default=None):
            image_type = "container"
    if image_type is None:
        image_path = config.getoption("--image-path", default=None)
        if image_path:
            image_type = detect_image_type(image_path)

    missing = check_tools(when=image_type)
    if missing:
        names = ", ".join(t.name for t in missing)
        hints = "\n".join(f"  - {t.name}: {t.reason} (install: {t.package_hint})" for t in missing)
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
    # (e.g. ``image("marketplace-gen2")`` matches both ``marketplace-gen2``
    # and ``marketplace-gen2-fips``). This lets tests under ``cases/<family>/`` apply
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
        pytest.skip(f"test is specific to image family '{expected}' (running: '{image_name}')")


def pytest_collection_modifyitems(config, items) -> None:  # type: ignore[no-untyped-def]
    """Auto-apply markers based on directory layout under ``cases/``.

    Layout convention (after restructure)::

        cases/
            static/
                test_*.py                   # shared static tests
                <image-family>/test_*.py    # image-specific static
            runtime/
                test_*.py                   # shared runtime tests
                <image-family>/test_*.py    # image-specific runtime

    Auto-applied markers:

    - ``@pytest.mark.image("<family>")`` on any test under
      ``cases/static/<family>/`` or ``cases/runtime/<family>/`` so it
      only runs when ``--image-name`` belongs to that family.
    - ``@pytest.mark.runtime`` on any test under ``cases/runtime/`` so
      static-only suites can exclude them with ``-m "not runtime"``.

    Tests directly under ``cases/static/`` or ``cases/runtime/`` (no
    image subdir) get no ``image`` marker and run for every image.
    """
    from pathlib import Path

    for item in items:
        parts = Path(str(item.fspath)).parts
        # Anchor on the right-most "cases" segment.
        try:
            cases_idx = len(parts) - 1 - parts[::-1].index("cases")
        except ValueError:
            continue

        remaining = parts[cases_idx + 1:]
        if not remaining:
            continue

        # remaining[0] is "static" or "runtime"; remaining[1] (if present)
        # is the image-family directory.
        category = remaining[0]  # "static" or "runtime"

        # Auto-apply runtime marker.
        if category == "runtime":
            item.add_marker(pytest.mark.runtime)

        # Auto-apply image() marker if there's an image-family subdir.
        # e.g. cases/static/vm-base/test_kernel.py → image("vm-base")
        #      cases/runtime/container-base/test_foo.py → image("container-base")
        if len(remaining) >= 3:  # category + family_dir + file
            image_dir = remaining[1]
            item.add_marker(pytest.mark.image(image_dir))
