# SPDX-License-Identifier: MIT
"""Clean-root installation checks for built component RPM artifacts."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from utils.pytest_plugin import CONTAINER_ENVIRONMENT_FLAG


def rpm_package_nevra(rpm_path: Path) -> str:
    """Read the exact package identity required from the candidate repository."""
    result = subprocess.run(
        [
            "rpm",
            "--queryformat",
            "%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}",
            "--query",
            "--package",
            str(rpm_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Unable to query the candidate NEVRA for {rpm_path} (rc={result.returncode})\n"
        f"{result.stdout}{result.stderr}"
    )
    return result.stdout


def component_work_directory() -> Path:
    """Return the writable scratch directory used by component tests."""
    work_directory = Path.cwd() / ".rpm-validation-work"
    work_directory.mkdir(parents=True, exist_ok=True)
    return work_directory


def candidate_repository(rpm_paths: list[Path], directory: Path) -> Path:
    """Publish candidate RPMs as repository metadata consumable by DNF tooling."""
    repository_path = directory / "candidate-repo"
    repository_path.mkdir()
    for rpm_path in rpm_paths:
        shutil.copy2(rpm_path, repository_path / rpm_path.name)

    result = subprocess.run(
        ["createrepo_c", "--quiet", str(repository_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Unable to create candidate repository (rc={result.returncode})\n"
        f"{result.stdout}{result.stderr}"
    )
    return repository_path


@pytest.mark.requires_tool("rpm")
@pytest.mark.requires_tool("createrepo_c")
@pytest.mark.requires_tool("dnf5")
@pytest.mark.container_smoke
def test_candidate_repository_installs_in_clean_container(rpm_paths: list[Path]) -> None:
    """Install the candidate repository into a fresh, empty install root.

    Only runs inside the purpose-built validation container
    (AZL_COMPONENT_TESTS_IN_CONTAINER=1); running --allowerasing against the
    live host root would risk erasing host packages and executing untrusted
    scriptlets outside an isolated environment. Uses a fresh --installroot
    rather than the running container's own root so installing a candidate
    that happens to share a NEVRA with a tool already present in the runner
    image (e.g. rpmlint) still genuinely exercises the candidate's payload
    and scriptlets instead of trivially matching the pre-installed package.
    """
    if os.environ.get(CONTAINER_ENVIRONMENT_FLAG) != "1":
        pytest.skip(
            "container_smoke only runs inside the validation container; use --container-image"
        )
    with TemporaryDirectory(
        prefix="azl-component-repo-", dir=component_work_directory()
    ) as temporary_directory:
        repository_path = candidate_repository(rpm_paths, Path(temporary_directory))
        install_root = Path(temporary_directory) / "install-root"
        install_root.mkdir()
        package_nevras = [rpm_package_nevra(rpm_path) for rpm_path in rpm_paths]
        result = subprocess.run(
            [
                "dnf5",
                "--assumeyes",
                "--nogpgcheck",
                "--setopt=install_weak_deps=False",
                "--installroot",
                str(install_root),
                "--setopt=reposdir=/etc/yum.repos.d",
                "--repofrompath",
                f"candidate,{repository_path.as_uri()}",
                "install",
                "--allowerasing",
                *package_nevras,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    assert result.returncode == 0, (
        "Unable to install the candidate repository in a clean install root "
        f"(rc={result.returncode})\n{result.stdout}{result.stderr}"
    )


@pytest.mark.requires_tool("createrepo_c")
@pytest.mark.requires_tool("rmdepcheck")
@pytest.mark.rmdepcheck
def test_candidate_repository_has_no_reverse_dependency_regressions(
    rpm_paths: list[Path], rmdepcheck_baseline_repositories: list[str]
) -> None:
    """Compare the candidate repository with configured AZL baseline repositories."""
    with TemporaryDirectory(
        prefix="azl-rmdepcheck-", dir=component_work_directory()
    ) as temporary_directory:
        repository_path = candidate_repository(rpm_paths, Path(temporary_directory))
        result = subprocess.run(
            [
                "rmdepcheck",
                ",".join(rmdepcheck_baseline_repositories),
                repository_path.as_uri(),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    assert result.returncode == 0, (
        "rmdepcheck found candidate repository regressions "
        f"(rc={result.returncode})\n{result.stdout}{result.stderr}"
    )
