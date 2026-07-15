"""Contract tests for Control Tower package-build entry points."""

from __future__ import annotations

import package_build
import pytest
import run_official_package_build
import run_scratch_package_build


class TestOfficialPackageBuildRequest:
    """Verify the official package scenario contract."""

    def test_request_uses_official_endpoint_and_minimal_payload(self) -> None:
        """Keep source and scratch controls out of official requests."""
        request = run_official_package_build.build_request("4.0", ["bash", "curl"])
        expected = package_build.ScenarioRequest(
            context="official-package-build",
            path="/api/Scenario/official/packages",
            payload={
                "environment": "4.0",
                "packages": ["bash", "curl"],
            },
        )

        if request != expected:
            pytest.fail(f"Unexpected official package-build request: {request!r}")

    def test_pull_request_build_is_rejected(self) -> None:
        """Prevent unmerged code from producing official artifacts."""
        with pytest.raises(SystemExit) as exc_info:
            run_official_package_build.validate_build_reason("PullRequest")

        if exc_info.value.code != 1:
            pytest.fail(f"Unexpected official PR rejection exit code: {exc_info.value.code!r}")


class TestScratchPackageBuildRequest:
    """Verify the scratch package scenario contract."""

    def test_request_uses_plural_endpoint_and_source_override(self) -> None:
        """Send the PR commit without legacy target or scratch controls."""
        request = run_scratch_package_build.build_request(
            "4.0",
            ["bash", "curl"],
            commit_sha="0123456789abcdef0123456789abcdef01234567",
        )
        expected = package_build.ScenarioRequest(
            context="scratch-package-build",
            path="/api/Scenario/packages",
            payload={
                "environment": "4.0",
                "packages": ["bash", "curl"],
                "commitSha": "0123456789abcdef0123456789abcdef01234567",
            },
        )

        if request != expected:
            pytest.fail(f"Unexpected scratch package-build request: {request!r}")

    def test_branch_and_commit_overrides_are_rejected(self) -> None:
        """Reject ambiguous scratch source selection."""
        with pytest.raises(ValueError, match="mutually exclusive"):
            run_scratch_package_build.build_request(
                "4.0",
                ["bash"],
                branch="users/test/topic",
                commit_sha="0123456789abcdef0123456789abcdef01234567",
            )
