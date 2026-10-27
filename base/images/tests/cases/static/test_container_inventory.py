# SPDX-License-Identifier: MIT
"""Validate container package inventories independently of runtime package management."""

from __future__ import annotations

import json
from collections import Counter
from typing import TYPE_CHECKING
from urllib.parse import parse_qs, unquote, urlsplit

import pytest
from utils.extract import read_text_confined

if TYPE_CHECKING:
    from pathlib import Path

pytestmark = pytest.mark.require_capability("container")

_RPM_MIN_FIELDS = 5
_MAIN_PACKAGES = {
    "container-busybox": "busybox",
    "container-nginx": "nginx",
    "container-postgres": "postgresql-server",
    "container-telegraf": "telegraf",
    "container-python": "python3",
    "container-nodejs": "nodejs",
    "container-pytorch": "python3-torch",
}


def _package_inventory(image_path: Path) -> Counter[tuple[str, str, str]]:
    """Read installed RPM identities, preserving epoch and architecture."""
    stem = image_path.name.removesuffix(".xz").removesuffix(".gz").removesuffix(".tar").removesuffix(".oci")
    inventory = image_path.with_name(f"{stem}.packages")
    assert inventory.is_file(), f"Missing package inventory: {inventory}"

    identities: Counter[tuple[str, str, str]] = Counter()
    for line in inventory.read_text().splitlines():
        if not line.strip():
            continue
        fields = line.split("|")
        assert len(fields) >= _RPM_MIN_FIELDS, f"Invalid package inventory entry: {line!r}"
        name, epoch, version, release, arch = fields[:_RPM_MIN_FIELDS]
        assert all((name, version, release, arch)), f"Incomplete package inventory entry: {line!r}"
        prefix = "" if epoch == "(none)" else f"{int(epoch)}:"
        identities[name, f"{prefix}{version}-{release}", arch] += 1

    assert identities, f"Package inventory is empty: {inventory}"
    return identities


def test_container_package_inventory(image_path: Path | None, image_name: str | None) -> None:
    """Built containers must have a nonempty inventory with the main package's version."""
    if image_path is None:
        pytest.skip("package inventories require a local image artifact")

    identities = _package_inventory(image_path)
    main_package = _MAIN_PACKAGES.get(image_name or "")
    if main_package is not None:
        assert any(name == main_package for name, _, _ in identities), f"Package inventory is missing {main_package}"


def test_distroless_container_package_manifest(
    rootfs: Path, image_path: Path | None, capabilities: set[str],
) -> None:
    """The exported SPDX manifest must describe the final installed RPM inventory."""
    if "runtime-package-management" in capabilities:
        pytest.skip("embedded manifests are only generated for distroless containers")
    if image_path is None:
        pytest.skip("manifest inventory comparison requires a local image artifact")

    document = json.loads(read_text_confined(rootfs, "usr/share/os-manifests/package-manifest.spdx.json"))
    assert document["@context"] == "https://spdx.org/rdf/3.0.1/spdx-context.jsonld"
    graph = document["@graph"]
    nodes = {node.get("spdxId", node.get("@id")): node for node in graph}
    assert None not in nodes, "Manifest elements must have identifiers"
    assert len(nodes) == len(graph), "Manifest element identifiers must be unique"
    spdx_document = next(node for node in graph if node["type"] == "SpdxDocument")
    assert nodes[spdx_document["creationInfo"]]["specVersion"] == "3.0.1"
    root = nodes[spdx_document["rootElement"][0]]
    assert root["type"] == "software_Package"
    license_node = nodes[spdx_document["dataLicense"]]
    assert license_node["type"] == "simplelicensing_LicenseExpression"
    assert license_node["simplelicensing_licenseExpression"] == "CC0-1.0"
    packages = [node for node in graph
                if node["type"] == "software_Package" and node["spdxId"] != root["spdxId"]]

    identities: Counter[tuple[str, str, str]] = Counter()
    for package in packages:
        purl = urlsplit(package["software_packageUrl"])
        assert purl.scheme == "pkg"
        assert purl.path.startswith("rpm/azurelinux/")
        name, version = purl.path.removeprefix("rpm/azurelinux/").rsplit("@", 1)
        assert unquote(name) == package["name"]
        qualifiers = parse_qs(purl.query, strict_parsing=True)
        epoch = qualifiers.get("epoch")
        prefix = "" if epoch is None else f"{int(epoch[0])}:"
        assert package["software_packageVersion"] == prefix + unquote(version)
        identities[package["name"], package["software_packageVersion"], qualifiers["arch"][0]] += 1
        assert nodes[package["suppliedBy"]]["type"] == "Organization"
    assert identities == _package_inventory(image_path), "Embedded manifest differs from final package inventory"

    contained = {
        target for node in graph
        if node.get("relationshipType") == "contains" and node["from"] == root["spdxId"]
        for target in node["to"]
    }
    assert contained == {package["spdxId"] for package in packages}, "Image must contain every installed package"


def test_minimal_container_package_database_excluded(rootfs: Path, capabilities: set[str]) -> None:
    """Minimal images keep package records in staging, not in their shipped filesystem."""
    if "runtime-package-management" in capabilities:
        pytest.skip("images with runtime package management retain their RPM database")

    for relative_path in ("usr/lib/sysimage/rpm", "var/lib/rpm"):
        path = rootfs / relative_path
        assert not path.exists(), f"Container retained package database: {path}"
        assert not path.is_symlink(), f"Container retained package database symlink: {path}"
