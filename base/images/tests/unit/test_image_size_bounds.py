# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Unit coverage for footprint configuration and checks, without image extraction."""

from __future__ import annotations

import importlib
import json
import shutil
import tomllib
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from types import ModuleType

_TEST_ROOT = Path(__file__).resolve().parents[1]

pytest_plugins = ["pytester"]


@pytest.fixture(scope="session")
def footprint(request: pytest.FixtureRequest) -> ModuleType:
    """Import the filesystem test module without changing its package layout."""
    request.config.addinivalue_line("markers", "require_capability(name): require an image capability")
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.syspath_prepend(str(_TEST_ROOT))
        return importlib.import_module("cases.static.test_footprint")


@pytest.fixture
def footprint_pytest(pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch) -> pytest.Pytester:
    """Run fresh copies of the real pytest wiring without native-tool preflight."""
    monkeypatch.setenv("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1")
    monkeypatch.setattr("utils.pytest_plugin.check_tools", lambda **_: [])
    pytester.makeini("[pytest]\naddopts = --import-mode=importlib\n")
    pytester.makeconftest((_TEST_ROOT / "conftest.py").read_text(encoding="utf-8"))
    cases = pytester.path / "cases" / "static"
    cases.mkdir(parents=True)
    shutil.copyfile(_TEST_ROOT / "cases/static/test_footprint.py", cases / "test_footprint_contract.py")
    shutil.copyfile(_TEST_ROOT / "image-size-bounds.json", pytester.path / "image-size-bounds.json")
    return pytester


@pytest.fixture(params=["missing", "malformed", "invalid"])
def invalid_bounds(footprint_pytest: pytest.Pytester, request: pytest.FixtureRequest) -> None:
    """Replace an isolated bounds file with missing, malformed, or invalid data."""
    bounds = footprint_pytest.path / "image-size-bounds.json"
    if request.param == "missing":
        bounds.unlink()
    else:
        content = {
            "malformed": "{",
            "invalid": json.dumps({"custom": {"x86_64": {"min_kib": 3, "max_kib": 2}}}),
        }[request.param]
        bounds.write_text(content, encoding="utf-8")


def _run_footprint(pytester: pytest.Pytester, *args: str) -> pytest.RunResult:
    return pytester.runpytest_inprocess(
        "-p",
        "utils.pytest_plugin",
        "cases/static/test_footprint_contract.py::test_image_tarball_within_limits",
        *args,
        "-q",
        "--tb=short",
        "-rs",
    )


def test_configured_images_and_architecture_bounds(footprint: ModuleType) -> None:
    """Every tarball image stores only minimum and maximum bounds per architecture."""
    with (_TEST_ROOT / "image-size-bounds.json").open(encoding="utf-8") as stream:
        configured = json.load(stream)
    limits = footprint.validate_artifact_limits(configured)
    with (_TEST_ROOT.parent / "images.toml").open("rb") as stream:
        images = tomllib.load(stream)["images"]
    tarball_images = {
        name
        for name, image in images.items()
        if image["capabilities"].get("container") or image["capabilities"].get("wsl")
    }
    assert set(limits) == tarball_images
    for name, architectures in limits.items():
        assert set(architectures) == set(images[name]["architectures"])
        for arch, bounds in architectures.items():
            assert set(configured[name][arch]) == {"min_kib", "max_kib"}
            assert all(value % 1024 == 0 for value in bounds), f"bounds for '{name}/{arch}' must be KiB-aligned"


@pytest.mark.parametrize(
    ("config", "message"),
    [
        ("invalid", "expected an image bounds dictionary"),
        (None, "expected an image bounds dictionary"),
        ({1: {}}, "image names must be strings"),
        ({"test": "invalid"}, "must contain architecture mappings"),
        ({"test": {"min_kib": 1}}, "unsupported architecture"),
        ({"test": {"amd64": {"min_kib": 1, "max_kib": 2}}}, "unsupported architecture"),
        ({"test": {"arm64": {"min_kib": 1, "max_kib": 2}}}, "unsupported architecture"),
        ({"test": {"x86_64": "invalid"}}, "specify min_kib and max_kib"),
        ({"test": {"x86_64": {"min_kib": 1}}}, "specify min_kib and max_kib"),
        (
            {"test": {"x86_64": {"min_kib": 1, "max_kib": 2, "extra": 3}}},
            "specify min_kib and max_kib",
        ),
        ({"test": {"x86_64": {"min_bytes": 1, "max_bytes": 2}}}, "specify min_kib and max_kib"),
        ({"test": {"x86_64": {"min_kib": True, "max_kib": 2}}}, "integer KiB counts"),
        ({"test": {"x86_64": {"min_kib": 1, "max_kib": 2.0}}}, "integer KiB counts"),
        ({"test": {"x86_64": {"min_kib": -1, "max_kib": 2}}}, "requires 0 <="),
        ({"test": {"x86_64": {"min_kib": 3, "max_kib": 2}}}, "requires 0 <="),
        ({"test": {"x86_64": {"min_kib": 0, "max_kib": 0}}}, "requires 0 <="),
    ],
)
def test_invalid_configuration(
    footprint: ModuleType,
    config: object,
    message: str,
) -> None:
    """Invalid ranges and malformed mappings must not silently disable checks."""
    with pytest.raises((TypeError, ValueError), match=message):
        footprint.validate_artifact_limits(config)


def test_empty_configuration(footprint: ModuleType) -> None:
    """An empty mapping leaves every image unconfigured."""
    assert footprint.validate_artifact_limits({}) == {}


def test_custom_configuration(footprint: ModuleType) -> None:
    """Normalize integer KiB bounds to byte ranges."""
    config = {"custom": {"x86_64": {"min_kib": 0, "max_kib": 123}}}
    assert footprint.validate_artifact_limits(config) == {"custom": {"x86_64": (0, 125952)}}


@pytest.mark.parametrize(
    ("filename", "configured", "expected"),
    [
        ("azurelinux-4-core.x86_64-0.1.0-41.oci.tar.xz", None, "x86_64"),
        ("azurelinux-4-core.aarch64-0.1.0-41.oci.tar.xz", None, "aarch64"),
        ("AzureLinux-4-x86_64.wsl", None, "x86_64"),
        ("AzureLinux-4-aarch64.wsl", None, "aarch64"),
        ("image.tar", "x86_64", "x86_64"),
        ("image.tar", "aarch64", "aarch64"),
        ("image.x86_64.tar", "x86_64", "x86_64"),
    ],
)
def test_target_architecture(
    footprint: ModuleType,
    filename: str,
    configured: str | None,
    expected: str,
) -> None:
    """Resolve the target independently of the test host architecture."""
    assert footprint.artifact_architecture(Path(filename), configured) == expected


@pytest.mark.parametrize(
    ("filename", "configured", "message"),
    [
        ("image.tar", None, "Cannot determine target architecture"),
        ("image.notx86_64.tar", None, "Cannot determine target architecture"),
        ("image.x86_64extra.tar", None, "Cannot determine target architecture"),
        ("image_x86_64.tar", None, "Cannot determine target architecture"),
        ("image_aarch64.tar", None, "Cannot determine target architecture"),
        ("image.x86_64-aarch64.tar", None, "Conflicting architectures"),
        ("image.x86_64.tar", "aarch64", "disagrees with artifact filename"),
        ("image_amd64.tar", None, "Cannot determine target architecture"),
        ("image.arm64.tar", None, "Cannot determine target architecture"),
        ("image.tar", "amd64", "Unsupported --image-arch"),
        ("image.tar", "arm64", "Unsupported --image-arch"),
        ("image.tar", "unknown", "Unsupported --image-arch"),
    ],
)
def test_invalid_target_architecture(
    footprint: ModuleType,
    filename: str,
    configured: str | None,
    message: str,
) -> None:
    """Unknown and conflicting target architectures fail explicitly."""
    with pytest.raises(pytest.fail.Exception, match=message):
        footprint.artifact_architecture(Path(filename), configured)


@pytest.mark.parametrize("image_type", ["container", "wsl"])
@pytest.mark.parametrize("size", [90, 100, 110])
def test_tarball_inclusive_bounds(footprint: ModuleType, tmp_path: Path, image_type: str, size: int) -> None:
    """Both endpoints of a configured range are accepted."""
    artifact = tmp_path / "image.x86_64.tar"
    artifact.write_bytes(b"x" * size)
    footprint.test_image_tarball_within_limits(artifact, image_type, "custom", {"custom": {"x86_64": (90, 110)}}, None)


@pytest.mark.parametrize(("arch", "size"), [("x86_64", 100), ("aarch64", 200)])
def test_architecture_specific_bounds(footprint: ModuleType, tmp_path: Path, arch: str, size: int) -> None:
    """The same image name uses different bounds for each target architecture."""
    artifact = tmp_path / f"image.{arch}.tar"
    artifact.write_bytes(b"x" * size)
    footprint.test_image_tarball_within_limits(
        artifact,
        "container",
        "custom",
        {"custom": {"x86_64": (90, 110), "aarch64": (190, 210)}},
        None,
    )


@pytest.mark.parametrize("size", [0, 89, 111])
def test_tarball_outside_bounds(footprint: ModuleType, tmp_path: Path, size: int) -> None:
    """Empty, undersized, and oversized artifacts fail."""
    artifact = tmp_path / "image.x86_64.tar"
    artifact.write_bytes(b"x" * size)
    with pytest.raises(AssertionError, match=r"empty|outside the configured range"):
        footprint.test_image_tarball_within_limits(
            artifact, "container", "custom", {"custom": {"x86_64": (90, 110)}}, None
        )


@pytest.mark.parametrize("name", ["unlisted", "container-base-variant"])
def test_unknown_image_skips(footprint: ModuleType, tmp_path: Path, name: str) -> None:
    """Unknown exact names skip before touching the artifact, without family fallback."""
    with pytest.raises(pytest.skip.Exception, match=f"No tarball footprint limits configured for image '{name}'"):
        footprint.test_image_tarball_within_limits(
            tmp_path / "not-accessed.tar",
            "container",
            name,
            {"container-base": {"x86_64": (90, 110)}},
            None,
        )


def test_unsampled_architecture_skips(footprint: ModuleType, tmp_path: Path) -> None:
    """A missing architecture skips before accessing the artifact, without fallback."""
    with pytest.raises(pytest.skip.Exception, match="image 'custom' architecture 'aarch64'"):
        footprint.test_image_tarball_within_limits(
            tmp_path / "image.aarch64.tar",
            "container",
            "custom",
            {"custom": {"x86_64": (90, 110)}},
            None,
        )


@pytest.mark.parametrize(
    ("image_type", "has_path", "message"),
    [("vm", True, "only applies to rootfs-tarball"), ("container", False, "requires --image-path")],
)
def test_inapplicable_inputs_skip(
    footprint: ModuleType,
    tmp_path: Path,
    image_type: str,
    *,
    has_path: bool,
    message: str,
) -> None:
    """VM images and registry references keep their existing skip behavior."""
    with pytest.raises(pytest.skip.Exception, match=message):
        footprint.test_image_tarball_within_limits(
            tmp_path / "not-accessed.tar" if has_path else None,
            image_type,
            "custom",
            {"custom": {"x86_64": (90, 110)}},
            None,
        )


@pytest.mark.parametrize(
    ("image_name", "cap_mib"),
    [("container-base", 400), ("container-base-variant", 400), ("wsl", 800), ("minimal-os", 2048)],
)
def test_installed_limits_unchanged(footprint: ModuleType, image_name: str, cap_mib: int) -> None:
    """Installed-size checks retain their existing family caps and fallback."""
    size = cap_mib * 1024 * 1024
    footprint.test_installed_footprint_under_threshold({"package": size}, image_name)
    with pytest.raises(AssertionError, match="exceeds"):
        footprint.test_installed_footprint_under_threshold({"package": size + 1}, image_name)


@pytest.mark.parametrize(
    ("name", "image_type", "arch"),
    [("container-base", "container", "x86_64"), ("wsl", "wsl", "aarch64")],
)
def test_pytest_default_bounds(
    footprint_pytest: pytest.Pytester,
    name: str,
    image_type: str,
    arch: str,
) -> None:
    """Actual fixture resolution loads the default bounds for both tarball types."""
    with (footprint_pytest.path / "image-size-bounds.json").open(encoding="utf-8") as stream:
        bounds = json.load(stream)[name][arch]
    artifact = footprint_pytest.path / f"image.{arch}.tar"
    with artifact.open("wb") as stream:
        stream.truncate((bounds["min_kib"] + bounds["max_kib"]) * 1024 // 2)
    result = _run_footprint(
        footprint_pytest,
        "--image-path",
        str(artifact),
        "--image-type",
        image_type,
        "--image-name",
        name,
    )
    result.assert_outcomes(passed=1)


@pytest.mark.parametrize("arch", ["x86_64", "aarch64"])
@pytest.mark.parametrize(
    ("size_bytes", "expected"),
    [
        (90 * 1024 - 1, "failed"),
        (90 * 1024, "passed"),
        (100 * 1024, "passed"),
        (110 * 1024, "passed"),
        (110 * 1024 + 1, "failed"),
    ],
)
def test_pytest_bounds_with_explicit_architecture(
    footprint_pytest: pytest.Pytester,
    arch: str,
    size_bytes: int,
    expected: str,
) -> None:
    """Explicit architecture selects bounds from the JSON file for renamed artifacts."""
    artifact = footprint_pytest.path / "image.tar"
    artifact.write_bytes(b"x" * size_bytes)
    bounds = footprint_pytest.path / "image-size-bounds.json"
    bounds.write_text(json.dumps({"custom": {arch: {"min_kib": 90, "max_kib": 110}}}), encoding="utf-8")
    result = _run_footprint(
        footprint_pytest,
        "--image-path",
        str(artifact),
        "--image-name",
        "custom",
        "--image-arch",
        arch,
    )
    result.assert_outcomes(**{expected: 1})
    if expected == "failed":
        result.stdout.fnmatch_lines(["*outside the configured range*"])


@pytest.mark.parametrize("arch", ["amd64", "arm64"])
def test_pytest_rejects_architecture_aliases(footprint_pytest: pytest.Pytester, arch: str) -> None:
    """CLI architecture aliases are rejected before running image checks."""
    artifact = footprint_pytest.path / "image.tar"
    artifact.write_bytes(b"x")
    result = _run_footprint(
        footprint_pytest,
        "--image-path",
        str(artifact),
        "--image-name",
        "container-base",
        "--image-arch",
        arch,
    )
    assert result.ret == pytest.ExitCode.USAGE_ERROR
    result.stderr.fnmatch_lines(["*--image-arch*invalid choice*"])


@pytest.mark.parametrize("arch", ["amd64", "arm64"])
def test_pytest_rejects_filename_architecture_aliases(footprint_pytest: pytest.Pytester, arch: str) -> None:
    """Artifact filenames cannot select bounds through architecture aliases."""
    artifact = footprint_pytest.path / f"image.{arch}.tar"
    artifact.write_bytes(b"x")
    result = _run_footprint(
        footprint_pytest,
        "--image-path",
        str(artifact),
        "--image-name",
        "container-base",
    )
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["*Cannot determine target architecture*"])


@pytest.mark.usefixtures("invalid_bounds")
@pytest.mark.parametrize("image_type", ["vm", "reference"])
def test_pytest_inapplicable_skips_invalid_bounds(
    footprint_pytest: pytest.Pytester,
    image_type: str,
) -> None:
    """Excluded sessions skip before missing or malformed policy can cause setup errors."""
    if image_type == "vm":
        artifact = footprint_pytest.path / "image.raw"
        artifact.write_bytes(b"x")
        image_args = ["--image-path", str(artifact)]
        message = "*only applies to rootfs-tarball*"
    else:
        image_args = ["--image-ref", "example.invalid/image:latest"]
        message = "*requires --image-path*"
    result = _run_footprint(footprint_pytest, *image_args)
    result.assert_outcomes(skipped=1)
    result.stdout.fnmatch_lines([message])


@pytest.mark.usefixtures("invalid_bounds")
def test_pytest_applicable_invalid_bounds_fail(
    footprint_pytest: pytest.Pytester,
) -> None:
    """Applicable tarballs still fail explicitly when configuration cannot be loaded."""
    artifact = footprint_pytest.path / "image.x86_64.tar"
    artifact.write_bytes(b"x" * 100)
    result = _run_footprint(
        footprint_pytest,
        "--image-path",
        str(artifact),
        "--image-name",
        "container-base",
    )
    result.assert_outcomes(errors=1)
    result.stdout.fnmatch_lines(["*Cannot load tarball footprint limits*"])


def test_pytest_unknown_image_skips(footprint_pytest: pytest.Pytester) -> None:
    """An unconfigured exact name skips without requiring an architecture token."""
    artifact = footprint_pytest.path / "image.tar"
    artifact.write_bytes(b"x")
    result = _run_footprint(
        footprint_pytest,
        "--image-path",
        str(artifact),
        "--image-name",
        "unlisted",
    )
    result.assert_outcomes(skipped=1)
    result.stdout.fnmatch_lines(["*No tarball footprint limits configured for image 'unlisted'*"])
