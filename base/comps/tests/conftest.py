# SPDX-License-Identifier: MIT
"""Fixtures for generic Azure Linux component validation."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from utils.pytest_plugin import (
    RPMINSPECT_POLICY_PATH,
    baseline_rpms,
    candidate_rpms,
    rmdepcheck_base_repos,
    rpmdeplint_repos,
    rpminspect_local_config,
)

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(scope="session")
def rpm_paths(request: pytest.FixtureRequest) -> list[Path]:
    """Candidate RPM artifacts supplied through the pytest command line."""
    return candidate_rpms(request.config)


@pytest.fixture(scope="session")
def baseline_rpm_paths(request: pytest.FixtureRequest) -> list[Path]:
    """Baseline RPM artifacts supplied for rpminspect comparisons."""
    return baseline_rpms(request.config)


@pytest.fixture(scope="session")
def rpminspect_policy() -> Path:
    """Use the Azure Linux policy packaged in the validation container."""
    assert RPMINSPECT_POLICY_PATH.is_file(), (
        "Azure Linux rpminspect policy is missing; use the rpm-validation container image"
    )
    return RPMINSPECT_POLICY_PATH


@pytest.fixture(scope="session")
def rpminspect_local_policy(request: pytest.FixtureRequest) -> Path | None:
    """Optional component-local rpminspect.yaml overlay."""
    return rpminspect_local_config(request.config)


@pytest.fixture(scope="session")
def rmdepcheck_baseline_repositories(request: pytest.FixtureRequest) -> list[str]:
    """Baseline repository URLs supplied for rmdepcheck validation."""
    return rmdepcheck_base_repos(request.config)


@pytest.fixture(scope="session")
def rpmdeplint_repositories(request: pytest.FixtureRequest) -> list[str]:
    """Repo arguments supplied for rpmdeplint dependency validation."""
    return rpmdeplint_repos(request.config)
