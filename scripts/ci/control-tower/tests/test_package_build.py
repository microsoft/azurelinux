"""Contract tests for Control Tower package-build entry points."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import Mock

import package_build
import pytest
import run_official_package_build
import run_scratch_package_build


@pytest.fixture
def lifecycle_mocks(monkeypatch: pytest.MonkeyPatch) -> tuple[Mock, Mock, Mock, Mock]:
    """Replace package-build authentication and transport dependencies."""
    post_scenario = Mock(return_value={"jobId": "job-id"})
    poll_until_terminal = Mock(return_value=({"status": package_build.ct.SUCCESS_STATUS}, False))
    print_final_status = Mock()
    report_failure = Mock()

    monkeypatch.setattr(package_build, "DefaultAzureCredential", Mock(return_value=object()))
    monkeypatch.setattr(package_build.ct, "get_token", Mock(return_value="token"))
    monkeypatch.setattr(package_build.ct, "make_session", Mock(return_value=object()))
    monkeypatch.setattr(package_build.ct, "poll_until_terminal", poll_until_terminal)
    monkeypatch.setattr(package_build.ct, "post_scenario", post_scenario)
    monkeypatch.setattr(package_build.ct, "print_final_status", print_final_status)
    monkeypatch.setattr(package_build.ct, "report_failure", report_failure)

    return post_scenario, poll_until_terminal, print_final_status, report_failure


def _submit(*, wait_for_completion: bool = False) -> None:
    """Call the shared lifecycle with stable test inputs."""
    package_build.submit_and_monitor(
        api_audience="api://control-tower",
        api_base_url="https://control-tower.example/",
        request=package_build.ScenarioRequest(
            context="package-build-test",
            path="/api/Scenario/packages",
            payload={"environment": "4.0", "packages": ["bash"]},
        ),
        poll_timeout_seconds=10,
        wait_for_completion=wait_for_completion,
    )


class TestPackageBuildLifecycle:
    """Verify shared submission and polling behavior."""

    @pytest.mark.parametrize("job_id", [None, 123])
    def test_missing_or_non_string_job_id_fails(
        self,
        lifecycle_mocks: tuple[Mock, Mock, Mock, Mock],
        job_id: object,
    ) -> None:
        """Reject responses that cannot identify a job to poll."""
        post_scenario, poll_until_terminal, _, _ = lifecycle_mocks
        post_scenario.return_value = {"jobId": job_id}

        with pytest.raises(SystemExit) as exc_info:
            _submit()

        if exc_info.value.code != 1 or poll_until_terminal.called:
            pytest.fail("Invalid job IDs must fail before polling")

    def test_submission_error_fails(self, lifecycle_mocks: tuple[Mock, Mock, Mock, Mock]) -> None:
        """Convert Control Tower submission errors into a failed pipeline step."""
        post_scenario, poll_until_terminal, _, _ = lifecycle_mocks
        post_scenario.side_effect = RuntimeError("submission failed")

        with pytest.raises(SystemExit) as exc_info:
            _submit()

        if exc_info.value.code != 1 or poll_until_terminal.called:
            pytest.fail("Submission errors must fail before polling")

    def test_poll_error_fails(self, lifecycle_mocks: tuple[Mock, Mock, Mock, Mock]) -> None:
        """Convert Control Tower polling errors into a failed pipeline step."""
        _, poll_until_terminal, _, _ = lifecycle_mocks
        poll_until_terminal.side_effect = RuntimeError("poll failed")

        with pytest.raises(SystemExit) as exc_info:
            _submit()

        if exc_info.value.code != 1:
            pytest.fail(f"Unexpected polling-error exit code: {exc_info.value.code!r}")

    def test_terminal_success_returns(self, lifecycle_mocks: tuple[Mock, Mock, Mock, Mock]) -> None:
        """Return successfully after Control Tower reports completion."""
        _, _, print_final_status, report_failure = lifecycle_mocks

        _submit()

        if print_final_status.call_count != 1 or report_failure.called:
            pytest.fail("A successful job must print its status without reporting failure")

    def test_terminal_failure_reports_and_exits(self, lifecycle_mocks: tuple[Mock, Mock, Mock, Mock]) -> None:
        """Report terminal Control Tower failures and fail the pipeline step."""
        _, poll_until_terminal, _, report_failure = lifecycle_mocks
        poll_until_terminal.return_value = ({"status": "Failed"}, False)

        with pytest.raises(SystemExit) as exc_info:
            _submit()

        if exc_info.value.code != 1 or report_failure.call_count != 1:
            pytest.fail("A terminal failure must be reported exactly once")

    @pytest.mark.parametrize(("wait_for_completion", "should_fail"), [(False, False), (True, True)])
    def test_timeout_behavior_depends_on_completion_mode(
        self,
        lifecycle_mocks: tuple[Mock, Mock, Mock, Mock],
        *,
        wait_for_completion: bool,
        should_fail: bool,
    ) -> None:
        """Accept async timeouts but reject completion-gate timeouts."""
        _, poll_until_terminal, _, _ = lifecycle_mocks
        poll_until_terminal.return_value = ({"status": "Running"}, True)

        if should_fail:
            with pytest.raises(SystemExit) as exc_info:
                _submit(wait_for_completion=wait_for_completion)
            if exc_info.value.code != 1:
                pytest.fail(f"Unexpected timeout exit code: {exc_info.value.code!r}")
            return

        _submit(wait_for_completion=wait_for_completion)


class TestBuildComponentLoading:
    """Verify changed-component input validation."""

    @pytest.mark.parametrize("entry", ["bash", {"changeType": "changed"}])
    def test_malformed_build_entry_fails_cleanly(
        self,
        monkeypatch: pytest.MonkeyPatch,
        entry: object,
    ) -> None:
        """Report malformed entries without leaking AttributeError or KeyError."""

        def _read_text(_path: Path, *, encoding: str) -> str:
            if encoding != "utf-8":
                pytest.fail(f"Unexpected changed-components encoding: {encoding}")
            return json.dumps([entry])

        monkeypatch.setattr(Path, "read_text", _read_text)

        with pytest.raises(SystemExit) as exc_info:
            package_build.load_build_components(Path("changed-components.json"))

        if exc_info.value.code != 1:
            pytest.fail(f"Unexpected malformed-entry exit code: {exc_info.value.code!r}")


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

    def test_request_supports_branch_override(self) -> None:
        """Send an optional branch override without a commit override."""
        request = run_scratch_package_build.build_request(
            "4.0",
            ["bash"],
            branch="users/test/topic",
        )
        expected = package_build.ScenarioRequest(
            context="scratch-package-build",
            path="/api/Scenario/packages",
            payload={
                "environment": "4.0",
                "packages": ["bash"],
                "branch": "users/test/topic",
            },
        )

        if request != expected:
            pytest.fail(f"Unexpected scratch branch request: {request!r}")

    def test_branch_and_commit_overrides_are_rejected(self) -> None:
        """Reject ambiguous scratch source selection."""
        with pytest.raises(ValueError, match="mutually exclusive"):
            run_scratch_package_build.build_request(
                "4.0",
                ["bash"],
                branch="users/test/topic",
                commit_sha="0123456789abcdef0123456789abcdef01234567",
            )
