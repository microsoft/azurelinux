# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ruff: noqa: INP001  # RPM build-time entry point, not an importable Python package.
"""Validate generated certificate stores against the JSON exclusion policy."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

CERTIFICATE = re.compile(
    r"-----BEGIN (?P<kind>(?:TRUSTED )?CERTIFICATE)-----.*?-----END (?P=kind)-----",
    re.DOTALL,
)


@dataclass(frozen=True)
class ExclusionPolicy:
    """Certificate identities and issuer/name restrictions for this component."""

    prohibited_names: tuple[str, ...]
    fingerprints: frozenset[tuple[str, str]]


def load_policy(path: Path) -> ExclusionPolicy:
    """Read the component-local policy without a nonstandard Python dependency."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"prohibited_names", "certificates"}:
        raise ValueError(f"{path}: expected prohibited_names and certificates")
    names = data["prohibited_names"]
    if not isinstance(names, list) or any(not isinstance(name, str) or not name.strip() for name in names):
        raise ValueError(f"{path}: prohibited_names must contain nonempty strings")
    certificates = data["certificates"]
    if not isinstance(certificates, list) or not certificates:
        raise ValueError(f"{path}: certificates must be a nonempty list")
    fingerprints: set[tuple[str, str]] = set()
    for certificate in certificates:
        if (
            not isinstance(certificate, dict)
            or set(certificate) - {"name", "sha1", "sha256"}
            or not isinstance(certificate.get("name"), str)
            or not certificate["name"].strip()
            or not ({"sha1", "sha256"} & certificate.keys())
        ):
            raise ValueError(f"{path}: invalid certificate policy entry")
        for algorithm, length in (("sha1", 40), ("sha256", 64)):
            if algorithm not in certificate:
                continue
            fingerprint = certificate[algorithm]
            if not isinstance(fingerprint, str) or not re.fullmatch(rf"[0-9a-f]{{{length}}}", fingerprint):
                raise ValueError(f"{path}: invalid {algorithm} fingerprint for {certificate['name']}")
            fingerprints.add((algorithm, fingerprint))
    return ExclusionPolicy(tuple(name.casefold() for name in names), frozenset(fingerprints))


def check_store(path: Path, policy: ExclusionPolicy) -> int:
    """Validate labels, certificate identities, and fingerprints in one store."""
    contents = path.read_text(encoding="utf-8")
    for line in contents.splitlines():
        if line.startswith("label:") and any(name in line.casefold() for name in policy.prohibited_names):
            raise ValueError(f"{path}: prohibited certificate label: {line}")

    certificates = list(CERTIFICATE.finditer(contents))
    for boundary in ("BEGIN", "END"):
        markers = re.findall(rf"-----{boundary} (?:TRUSTED )?CERTIFICATE-----", contents)
        if len(markers) != len(certificates):
            raise ValueError(f"{path}: malformed certificate bundle")

    for index, certificate in enumerate(certificates, start=1):
        der = subprocess.run(
            ["openssl", "x509", "-outform", "DER"],
            input=certificate[0].encode("ascii"),
            stdout=subprocess.PIPE,
            check=True,
        ).stdout
        fingerprints = {
            ("sha256", hashlib.sha256(der).hexdigest()),
            ("sha1", hashlib.sha1(der, usedforsecurity=False).hexdigest()),
        }
        if fingerprints & policy.fingerprints:
            raise ValueError(f"{path}: certificate {index} matches an excluded fingerprint")
        identity = subprocess.run(
            ["openssl", "x509", "-inform", "DER", "-noout", "-subject", "-issuer", "-nameopt", "RFC2253"],
            input=der,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.decode("utf-8")
        if any(name in identity.casefold() for name in policy.prohibited_names):
            raise ValueError(f"{path}: certificate {index} has a prohibited subject or issuer: {identity.strip()}")

    print(f"{path}: checked {len(certificates)} certificates")
    return len(certificates)


def main() -> None:
    """Check a nonempty primary store and optionally empty legacy stores."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=Path(__file__).with_name("excluded-certificates.json"))
    parser.add_argument("stores", nargs="+", type=Path, help="Primary store followed by optional legacy stores")
    args = parser.parse_args()
    policy = load_policy(args.policy)
    counts = [check_store(path, policy) for path in args.stores]
    if not counts[0]:
        raise ValueError(f"{args.stores[0]}: primary certificate store is empty")


if __name__ == "__main__":
    main()
