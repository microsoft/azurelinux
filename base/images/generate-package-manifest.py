#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Prototype: write package-only SPDX 3.0.1 from a prepared image's RPM database."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import sysconfig
import uuid
from pathlib import Path
from urllib.parse import quote

MANIFEST_PATH = "usr/share/os-manifests/package-manifest.spdx.json"
DEFAULT_SUPPLIER = "Microsoft Corporation"
RPM_QUERY = "%|ARCH?{%{NAME}|%{EPOCH}|%{VERSION}|%{RELEASE}|%{ARCH}|%{VENDOR}\n}:{}|"


def dependencies(binary: Path) -> set[Path]:
    """Resolve the installed executable or extension's dynamic dependencies."""
    result = subprocess.run(
        ["ldd", str(binary)], capture_output=True, text=True, check=True, timeout=30
    )
    if "not found" in result.stdout:
        raise RuntimeError(f"Unresolved dependencies for {binary}: {result.stdout}")
    return {
        Path(match.group(1))
        for line in result.stdout.splitlines()
        if (match := re.search(r"(/[^ ]+)\s+\(", line))
    }


def stage_tools(destination: Path) -> None:
    """Copy build helpers as unregistered files, without changing package state."""
    if not destination.is_dir() or any(destination.iterdir()):
        raise ValueError("Helper destination must be an existing empty directory")
    destination = destination.resolve()
    if not destination.is_relative_to(Path("/tmp")):  # noqa: S108 - caller uses mktemp; KIWI excludes /tmp.
        raise ValueError("Helper destination must be below /tmp")
    (destination / "bin").mkdir()
    (destination / "lib").mkdir()
    python = Path(sys.executable).resolve()
    rpm_binary = shutil.which("rpm")
    if rpm_binary is None:
        raise RuntimeError("RPM is required before package cleanup")
    rpm = Path(rpm_binary).resolve()
    shutil.copy2(python, destination / "bin/python3")
    shutil.copy2(rpm, destination / "bin/rpm")
    stdlib = Path(sysconfig.get_path("stdlib"))
    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    copied_stdlib = destination / sys.platlibdir / python_version
    shutil.copytree(
        stdlib,
        copied_stdlib,
        ignore=shutil.ignore_patterns(
            "site-packages", "__pycache__", "test", "tests",
            "idlelib", "tkinter", "turtledemo", "ensurepip",
        ),
    )
    binaries = [python, rpm, *stdlib.rglob("lib-dynload/*.so")]
    libraries = set()
    for binary in binaries:
        libraries.update(dependencies(binary))
    loaders = [path for path in libraries if path.name.startswith("ld-linux")]
    if len(loaders) != 1:
        raise RuntimeError(f"Expected one ELF interpreter, found {loaders}")
    shutil.copy2(loaders[0], destination / "loader")
    for library in sorted(libraries):
        target = destination / "lib" / library.name
        if target.exists() and target.read_bytes() != library.read_bytes():
            raise RuntimeError(f"Conflicting runtime library: {library.name}")
        shutil.copy2(library, target)
    configuration = subprocess.run(
        ["rpm", "--eval", "%{_rpmconfigdir}"],
        capture_output=True, text=True, check=True, timeout=30,
    )
    rpm_config = Path(configuration.stdout.strip())
    (destination / "rpm").mkdir()
    for name in ("rpmrc", "macros"):
        shutil.copy2(rpm_config / name, destination / "rpm" / name)
    print(f"Staged build-only Python/RPM helpers in {destination}")


def installed_packages(root: Path, tools: Path | None = None) -> list[tuple[str, str, str, str]]:
    """Query the final target database using normal or staged RPM tooling."""
    for relative in ("usr/lib/sysimage/rpm", "var/lib/rpm"):
        database = (root / relative).resolve()
        if not database.is_relative_to(root):
            raise ValueError(f"RPM database escapes image root: {relative}")
        if (database / "rpmdb.sqlite").is_file():
            break
    else:
        raise ValueError("Prepared image has no SQLite RPM database")
    command = ["rpm"] if tools is None else [
        str(tools / "loader"), "--library-path", str(tools / "lib"),
        str(tools / "bin/rpm"), "--rcfile", str(tools / "rpm/rpmrc"),
        "--macros", str(tools / "rpm/macros"), "--noplugins",
    ]
    result = subprocess.run(
        [*command, "--dbpath", str(database), "-qa", "--queryformat", RPM_QUERY],
        capture_output=True,
        text=True,
        check=True,
        timeout=120,
    )
    packages = []
    identities = set()
    for line in result.stdout.splitlines():
        name, epoch, version, release, arch, vendor = line.split("|", 5)
        if not all((name, version, release, arch)):
            raise ValueError(f"Incomplete installed package identity: {line!r}")
        epoch_prefix = "" if epoch == "(none)" else f"{int(epoch)}:"
        package_version = f"{epoch_prefix}{version}-{release}"
        if (name, package_version, arch) in identities:
            raise ValueError(f"Duplicate installed package identity: {name}-{package_version}.{arch}")
        identities.add((name, package_version, arch))
        qualifiers = f"arch={quote(arch, safe='')}"
        if epoch != "(none)":
            qualifiers += f"&epoch={int(epoch)}"
        package_url = (
            f"pkg:rpm/azurelinux/{quote(name, safe='')}@"
            f"{quote(f'{version}-{release}', safe=':')}?{qualifiers}"
        )
        vendor = vendor.strip()
        if vendor in ("(none)", "NOASSERTION"):
            vendor = ""
        packages.append((name, package_version, package_url, vendor))
    if not packages:
        raise ValueError("Prepared image reports no installed packages")
    return sorted(packages)


def create_document(
    name: str, version: str, packages: list[tuple[str, str, str, str]], created_epoch: int
) -> dict:
    """Construct the same SPDX JSON-LD dialect used by SbomToolkit's 3.0 adapter."""
    source_digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    seed = json.dumps([name, version, packages, created_epoch, source_digest])
    namespace = (
        f"https://azurelinux.microsoft.com/spdxdocs/{quote(name, safe='')}-"
        f"{uuid.uuid5(uuid.NAMESPACE_URL, seed)}"
    )
    creation = namespace + "/CreationInfo/0"
    organization = namespace + "/Organization/0"
    tool = namespace + "/Tool/0"
    document = namespace + "/SpdxDocument/0"
    root_package = namespace + "/RootPackage/0"
    data_license = namespace + "/LicenseExpression/0"
    graph = [
        {
            "type": "CreationInfo",
            "@id": creation,
            "specVersion": "3.0.1",
            "created": dt.datetime.fromtimestamp(
                created_epoch, tz=dt.UTC
            ).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "createdBy": [organization],
            "createdUsing": [tool],
        },
        {
            "type": "Organization",
            "spdxId": organization,
            "name": DEFAULT_SUPPLIER,
            "creationInfo": creation,
        },
        {
            "type": "Tool",
            "spdxId": tool,
            "name": f"generate-package-manifest.py-sha256:{source_digest}",
            "creationInfo": creation,
        },
        {
            "type": "simplelicensing_LicenseExpression",
            "spdxId": data_license,
            "simplelicensing_licenseExpression": "CC0-1.0",
            "creationInfo": creation,
        },
        {
            "type": "SpdxDocument",
            "spdxId": document,
            "name": f"{name} {version}",
            "creationInfo": creation,
            "dataLicense": data_license,
            "rootElement": [root_package],
        },
        {
            "type": "software_Package",
            "spdxId": root_package,
            "name": name,
            "software_packageVersion": version,
            "suppliedBy": organization,
            "creationInfo": creation,
        },
    ]
    suppliers = {DEFAULT_SUPPLIER: organization}
    package_ids = []
    for index, (package, package_version, package_url, vendor) in enumerate(packages):
        identifier = namespace + f"/Package/{index}"
        package_ids.append(identifier)
        package_node = {
            "type": "software_Package",
            "spdxId": identifier,
            "name": package,
            "software_packageVersion": package_version,
            "software_packageUrl": package_url,
            "creationInfo": creation,
        }
        supplier = vendor or DEFAULT_SUPPLIER
        if supplier not in suppliers:
            suppliers[supplier] = namespace + f"/Organization/{len(suppliers)}"
            graph.append(
                {
                    "type": "Organization",
                    "spdxId": suppliers[supplier],
                    "name": supplier,
                    "creationInfo": creation,
                }
            )
        package_node["suppliedBy"] = suppliers[supplier]
        graph.append(package_node)
    for index, (source, relationship, targets) in enumerate(
        [
            (document, "describes", [root_package]),
            (root_package, "contains", package_ids),
        ]
    ):
        graph.append(
            {
                "type": "Relationship",
                "spdxId": namespace + f"/Relationship/{index}",
                "from": source,
                "relationshipType": relationship,
                "to": targets,
                "creationInfo": creation,
            }
        )
    return {
        "@context": "https://spdx.org/rdf/3.0.1/spdx-context.jsonld",
        "@graph": graph,
    }


def main() -> None:
    """Stage helpers before cleanup or write the manifest after package removal."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    staging = commands.add_parser("stage", help="Preserve temporary build helpers before cleanup")
    staging.add_argument("destination", type=Path)
    generation = commands.add_parser("generate", help="Write SPDX from the final installed package set")
    generation.add_argument("--root", type=Path, required=True)
    generation.add_argument("--name", required=True)
    generation.add_argument("--version", required=True)
    generation.add_argument("--created-epoch", type=int)
    generation.add_argument("--tools-dir", type=Path)
    args = parser.parse_args()
    if args.command == "stage":
        stage_tools(args.destination)
        return
    root = args.root.resolve(strict=True)
    packages = installed_packages(root, args.tools_dir)
    epoch = args.created_epoch
    if epoch is None:
        source_epoch = os.environ.get("SOURCE_DATE_EPOCH")
        epoch = int(source_epoch) if source_epoch is not None else int((root / "usr/lib/os-release").stat().st_mtime)
    if epoch < 0:
        parser.error("--created-epoch must be nonnegative")
    output = root / MANIFEST_PATH
    if not output.resolve().is_relative_to(root):
        raise ValueError("Manifest path escapes prepared image root")
    document = create_document(args.name, args.version, packages, epoch)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".tmp")
    with temporary.open("x", encoding="utf-8") as stream:
        json.dump(document, stream, indent=2)
        stream.write("\n")
    temporary.chmod(0o644)
    temporary.replace(output)
    print(f"Embedded SPDX 3.0.1: {len(packages)} installed packages at {output}")


if __name__ == "__main__":
    main()
