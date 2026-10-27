# SPDX-License-Identifier: MIT
"""Focused regression checks for the image-owned package manifest helper."""

from __future__ import annotations

import runpy
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

pytestmark = pytest.mark.require_capability("container")
_GENERATOR = runpy.run_path(str(Path(__file__).parents[3] / "generate-package-manifest.py"))


@pytest.fixture
def rpm_root(tmp_path: Path) -> Path:
    """Provide an image database path without installing or querying real RPMs."""
    database = tmp_path / "usr/lib/sysimage/rpm"
    database.mkdir(parents=True)
    (database / "rpmdb.sqlite").touch()
    return tmp_path


@pytest.mark.parametrize("loader", ["ld-linux-x86-64.so.2", "ld-linux-aarch64.so.1"])
def test_runtime_dependencies(loader: str) -> None:
    """Discover shared libraries and the native loader on either architecture."""
    output = f"libc.so.6 => /lib64/libc.so.6 (0x1234)\n/lib64/{loader} (0x3456)\n"
    with patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, output)):
        dependencies = _GENERATOR["dependencies"](Path("/usr/bin/python3"))
    assert dependencies == {Path("/lib64/libc.so.6"), Path("/lib64") / loader}


def test_missing_runtime_dependency() -> None:
    """Do not silently stage an incomplete runtime."""
    result = subprocess.CompletedProcess([], 0, "libmissing.so => not found\n")
    with patch("subprocess.run", return_value=result), pytest.raises(RuntimeError, match="Unresolved dependencies"):
        _GENERATOR["dependencies"](Path("/usr/bin/python3"))


def test_staging_preserves_existing_data(tmp_path: Path) -> None:
    """Refuse to overwrite a nonempty helper destination."""
    existing = tmp_path / "existing"
    existing.write_text("preserve")
    with pytest.raises(ValueError, match="empty directory"):
        _GENERATOR["stage_tools"](tmp_path)
    assert existing.read_text() == "preserve"


def test_staged_rpm_rejects_empty_inventory(rpm_root: Path) -> None:
    """Query the final database through staged RPM and fail on an empty result."""
    tools = rpm_root / "tools"
    with (
        patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, "")) as query,
        pytest.raises(ValueError, match="no installed packages"),
    ):
        _GENERATOR["installed_packages"](rpm_root, tools)
    assert query.call_args is not None
    command = query.call_args.args[0]
    assert command[0] == str(tools / "loader")
    assert str(tools / "bin/rpm") in command
    assert str(rpm_root / "usr/lib/sysimage/rpm") in command


@pytest.mark.parametrize(
    ("record", "version", "purl"),
    [
        (
            "busybox|1|1.37.0|6.azl4|x86_64|Microsoft Corporation\n",
            "1:1.37.0-6.azl4",
            "pkg:rpm/azurelinux/busybox@1.37.0-6.azl4?arch=x86_64&epoch=1",
        ),
        (
            "libstdc++|(none)|15.2.0|3.azl4|aarch64|Microsoft Corporation\n",
            "15.2.0-3.azl4",
            "pkg:rpm/azurelinux/libstdc%2B%2B@15.2.0-3.azl4?arch=aarch64",
        ),
        (
            "filesystem|0|3.18|54.azl4|noarch|Microsoft Corporation\n",
            "0:3.18-54.azl4",
            "pkg:rpm/azurelinux/filesystem@3.18-54.azl4?arch=noarch&epoch=0",
        ),
    ],
)
def test_rpm_identity_and_purl(rpm_root: Path, record: str, version: str, purl: str) -> None:
    """Preserve epochs and architecture while encoding package names correctly."""
    with patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, record)):
        packages = _GENERATOR["installed_packages"](rpm_root)
    assert packages[0][1:3] == (version, purl)
    assert packages[0][3] == "Microsoft Corporation"


@pytest.mark.parametrize("vendor", ["", "(none)", "NOASSERTION", "   "])
def test_supplier_fallback(rpm_root: Path, vendor: str) -> None:
    """Missing vendor metadata resolves to the existing Microsoft Organization."""
    record = f"busybox|(none)|1|1.azl4|x86_64|{vendor}\n"
    with patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, record)):
        packages = _GENERATOR["installed_packages"](rpm_root)
    document = _GENERATOR["create_document"]("image", "1", packages, 0)
    nodes = {node["spdxId"]: node for node in document["@graph"] if "spdxId" in node}
    for node in nodes.values():
        if node["type"] == "software_Package":
            assert nodes[node["suppliedBy"]]["name"] == "Microsoft Corporation"
    assert [node["name"] for node in nodes.values() if node["type"] == "Organization"] == ["Microsoft Corporation"]


def test_multilib_and_duplicate_identities(rpm_root: Path) -> None:
    """Keep distinct architectures but reject duplicate complete RPM identities."""
    record = (
        "library|(none)|1|1.azl4|x86_64|Microsoft Corporation\n"
        "library|(none)|1|1.azl4|aarch64|Microsoft Corporation\n"
    )
    with patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, record)):
        packages = _GENERATOR["installed_packages"](rpm_root)
    assert {package[2] for package in packages} == {
        "pkg:rpm/azurelinux/library@1-1.azl4?arch=x86_64",
        "pkg:rpm/azurelinux/library@1-1.azl4?arch=aarch64",
    }
    with (
        patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, record * 2)),
        pytest.raises(ValueError, match="Duplicate installed package identity"),
    ):
        _GENERATOR["installed_packages"](rpm_root)


def test_document_license_suppliers_and_relationships() -> None:
    """Resolve CC0 and suppliers, and contain exactly the installed packages."""
    packages = [
        ("busybox", "1-1", "pkg:rpm/azurelinux/busybox@1-1?arch=x86_64", "Microsoft Corporation"),
        ("external", "1-1", "pkg:rpm/azurelinux/external@1-1?arch=noarch", "Other Vendor"),
        ("external-two", "2-1", "pkg:rpm/azurelinux/external-two@2-1?arch=noarch", "Other Vendor"),
    ]
    document = _GENERATOR["create_document"]("image", "1", packages, 0)
    graph = document["@graph"]
    nodes = {node["spdxId"]: node for node in graph if "spdxId" in node}
    spdx_document = next(node for node in graph if node["type"] == "SpdxDocument")
    license_node = nodes[spdx_document["dataLicense"]]
    assert license_node["type"] == "simplelicensing_LicenseExpression"
    assert license_node["simplelicensing_licenseExpression"] == "CC0-1.0"
    assert sorted(node["name"] for node in graph if node["type"] == "Organization") == [
        "Microsoft Corporation", "Other Vendor",
    ]
    for node in graph:
        if node["type"] == "software_Package":
            expected = "Other Vendor" if node["name"].startswith("external") else "Microsoft Corporation"
            assert nodes[node["suppliedBy"]]["name"] == expected
    containment = next(node for node in graph if node.get("relationshipType") == "contains")
    root_id = spdx_document["rootElement"][0]
    assert containment["from"] == root_id
    assert set(containment["to"]) == {
        node["spdxId"] for node in graph
        if node["type"] == "software_Package" and node["spdxId"] != root_id
    }
    assert not any("software_downloadLocation" in node for node in graph)
