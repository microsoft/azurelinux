# SPDX-License-Identifier: MIT
"""Generic, component-agnostic checks for built RPM artifacts."""

from __future__ import annotations

import os
import subprocess
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path


RPM_QUERY_SETS = (
    pytest.param(("-qip",), id="package-information"),
    pytest.param(("-qpl",), id="file-manifest"),
    pytest.param(("-qp", "--requires"), id="dependencies"),
    pytest.param(("-qp", "--provides"), id="provided-capabilities"),
    pytest.param(("-qp", "--scripts"), id="scriptlets"),
)


def run_rpm(args: Sequence[str], rpm_path: Path) -> subprocess.CompletedProcess[str]:
    """Run an RPM inspection command and retain output for assertion messages."""
    return subprocess.run(
        ["rpm", *args, str(rpm_path)],
        check=False,
        capture_output=True,
        text=True,
    )


def rpm_name_architecture(rpm_path: Path) -> str:
    """Return the peer identity used to compare local RPM artifacts."""
    result = run_rpm(("--queryformat", "%{NAME}.%{ARCH}", "--query", "--package"), rpm_path)
    assert result.returncode == 0, (
        f"Unable to query rpminspect peer identity for {rpm_path} (rc={result.returncode})\n"
        f"{result.stdout}{result.stderr}"
    )
    return result.stdout


def rpm_peer_map(rpm_paths: list[Path], artifact_type: str) -> dict[str, Path]:
    """Map RPM paths by peer identity and reject ambiguous comparison inputs."""
    peers: dict[str, Path] = {}
    for rpm_path in rpm_paths:
        peer = rpm_name_architecture(rpm_path)
        assert peer not in peers, (
            f"Multiple {artifact_type} RPMs have rpminspect peer identity {peer}: "
            f"{peers[peer]} and {rpm_path}"
        )
        peers[peer] = rpm_path
    return peers


@pytest.mark.requires_tool("rpm")
@pytest.mark.rpm_artifact
def test_rpm_signature_and_payload_are_valid(rpm_paths: list[Path]) -> None:
    """Every candidate RPM must have a readable, intact signature and payload."""
    failures: list[str] = []
    for rpm_path in rpm_paths:
        result = run_rpm(("--checksig", "--verbose"), rpm_path)
        if result.returncode != 0:
            failures.append(
                f"{rpm_path}: rpm --checksig failed (rc={result.returncode})\n"
                f"{result.stdout}{result.stderr}"
            )
    assert not failures, "\n".join(failures)


@pytest.mark.requires_tool("rpm")
@pytest.mark.rpm_artifact
@pytest.mark.parametrize("query_args", RPM_QUERY_SETS)
def test_rpm_metadata_is_queryable(
    rpm_paths: list[Path], query_args: tuple[str, ...]
) -> None:
    """RPM headers, payload manifest, dependencies, provides, and scripts must parse."""
    failures: list[str] = []
    for rpm_path in rpm_paths:
        result = run_rpm(query_args, rpm_path)
        if result.returncode != 0:
            failures.append(
                f"{rpm_path}: rpm {' '.join(query_args)} failed (rc={result.returncode})\n"
                f"{result.stdout}{result.stderr}"
            )
    assert not failures, "\n".join(failures)


@pytest.mark.requires_tool("rpmlint")
@pytest.mark.rpmlint
def test_rpmlint_reports_no_findings(rpm_paths: list[Path]) -> None:
    """Lint candidate RPMs with the Azure Linux policy applied explicitly.

    The Azure Linux rpmlint policy fragment (zz-azurelinux.toml, named so it
    also sorts last if ever autoloaded) ships from microsoft/azurelinux#19745,
    not this component. rpmlint's autoloader sorts fragments under
    /etc/xdg/rpmlint/ by filename and applies them in that order, so relying
    on autoload would let a later-sorting fragment (e.g. fedora.toml) silently
    override the Azure Linux release-suffix policy. Disable autoloading and
    pass the Azure Linux fragment explicitly so it is the only policy applied.
    """
    result = subprocess.run(
        [
            "rpmlint",
            "--config",
            "/etc/xdg/rpmlint/zz-azurelinux.toml",
            *map(str, rpm_paths),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "CONFIG_DISABLE_AUTOLOADING": "1"},
    )
    assert result.returncode == 0, (
        "rpmlint failed with the Azure Linux policy from microsoft/azurelinux#19745 "
        f"(rc={result.returncode})\n{result.stdout}{result.stderr}"
    )


@pytest.mark.requires_tool("rpm")
@pytest.mark.requires_tool("rpminspect")
@pytest.mark.rpminspect
def test_rpminspect_reports_no_regressions(
    rpm_paths: list[Path],
    baseline_rpm_paths: list[Path],
    rpminspect_policy: Path,
    rpminspect_local_policy: Path | None,
) -> None:
    """Compare each candidate RPM with its matching baseline using AZL policy."""
    baseline_peers = rpm_peer_map(baseline_rpm_paths, "baseline")
    candidate_peers = rpm_peer_map(rpm_paths, "candidate")
    assert baseline_peers.keys() == candidate_peers.keys(), (
        "rpminspect baseline and candidate RPM sets must have matching NAME.ARCH peers\n"
        f"Missing baseline peers: {sorted(candidate_peers.keys() - baseline_peers.keys())}\n"
        f"Missing candidate peers: {sorted(baseline_peers.keys() - candidate_peers.keys())}"
    )

    failures: list[str] = []
    for peer in sorted(candidate_peers):
        baseline_rpm = baseline_peers[peer]
        candidate_rpm = candidate_peers[peer]
        result = subprocess.run(
            [
                "rpminspect",
                "-c",
                str(rpminspect_policy),
                str(baseline_rpm),
                str(candidate_rpm),
            ],
            check=False,
            capture_output=True,
            text=True,
            cwd=rpminspect_local_policy.parent if rpminspect_local_policy else None,
        )
        if result.returncode != 0:
            failures.append(
                f"{peer}: rpminspect failed (rc={result.returncode})\n"
                f"{result.stdout}{result.stderr}"
            )

    assert not failures, "\n".join(failures)
