#!/usr/bin/env python3
"""Guard source-origin configuration for rendered-spec checks."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any

# Intentionally duplicated from trusted defaults in distro/fedora.distro.toml.
# Keep this allowlist in sync when Fedora source origins are intentionally updated.
ALLOWED_FEDORA_DIST_GIT_BASE_URI = "https://src.fedoraproject.org/rpms/$pkg.git"
ALLOWED_FEDORA_LOOKASIDE_BASE_URI = "https://src.fedoraproject.org/repo/pkgs/$pkg/$filename/$hashtype/$hash/$filename"
ALLOWED_FEDORA_REPO_BASE_URIS = {
    "https://na.edge.kernel.org/fedora/releases/$releasever/Everything/source/tree",
    "https://na.edge.kernel.org/fedora/updates/$releasever/Everything/source/tree",
    "https://na.edge.kernel.org/fedora/development/$releasever/Everything/source/tree",
}


def _run(
    cmd: list[str], *, cwd: str | None = None, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def _load_config() -> dict[str, Any]:
    env = os.environ.copy()
    env["AZLDEV_ALLOW_ROOT"] = "1"
    result = _run(["azldev", "config", "dump", "-q", "-f", "json"], env=env)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        if stderr:
            print(f"::error::azldev config dump failed: {stderr}", file=sys.stderr)
        else:
            print("::error::azldev config dump failed", file=sys.stderr)
        raise SystemExit(result.returncode)
    return json.loads(result.stdout)


def _validate_fedora_sources(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    fedora = config.get("distros", {}).get("fedora")
    if not isinstance(fedora, dict):
        return ["Resolved config is missing distros.fedora"]

    dist_git = fedora.get("distGitBaseUri")
    lookaside = fedora.get("lookasideBaseUri")
    repos = fedora.get("repos")

    if dist_git != ALLOWED_FEDORA_DIST_GIT_BASE_URI:
        errors.append(
            f"distros.fedora.distGitBaseUri resolved to {dist_git!r}, expected {ALLOWED_FEDORA_DIST_GIT_BASE_URI!r}"
        )

    if lookaside != ALLOWED_FEDORA_LOOKASIDE_BASE_URI:
        errors.append(
            f"distros.fedora.lookasideBaseUri resolved to {lookaside!r}, expected {ALLOWED_FEDORA_LOOKASIDE_BASE_URI!r}"
        )

    if not isinstance(repos, list):
        errors.append("distros.fedora.repos is missing or not a list")
        return errors

    actual_repos: set[str] = set()
    for index, item in enumerate(repos):
        if not isinstance(item, dict):
            errors.append(f"distros.fedora.repos entry {index} is not a dictionary: {item!r}")
            continue
        base_uri = item.get("baseUri")
        if not isinstance(base_uri, str):
            errors.append(f"distros.fedora.repos entry {index} has non-string baseUri: {base_uri!r}")
            continue
        actual_repos.add(base_uri)
    missing_repos = sorted(ALLOWED_FEDORA_REPO_BASE_URIS - actual_repos)
    extra_repos = sorted(actual_repos - ALLOWED_FEDORA_REPO_BASE_URIS)

    if missing_repos:
        errors.append("Missing approved Fedora repo base URIs:")
        errors.extend(f"  - {uri!r}" for uri in missing_repos)
    if extra_repos:
        errors.append("Unexpected Fedora repo base URIs:")
        errors.extend(f"  - {uri!r}" for uri in extra_repos)

    return errors


def validate() -> int:
    """Validate resolved Fedora source origins against the allowlist."""
    config = _load_config()
    errors = _validate_fedora_sources(config)
    if errors:
        print("::error::Source-origin allowlist check failed", file=sys.stderr)
        for error in errors:
            print(f"::error::{error}", file=sys.stderr)
        return 1

    print("Source-origin allowlist check passed.")
    return 0


def main() -> int:
    """Run the source-origin validation."""
    return validate()


if __name__ == "__main__":
    sys.exit(main())
