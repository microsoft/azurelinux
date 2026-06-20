"""Tests for post-merge azldev version resolution."""

from __future__ import annotations

import subprocess
import sys
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
import resolve_azldev_version as resolver

if TYPE_CHECKING:
    from pathlib import Path


def _pull_request(*, number: int = 1, head_sha: str = "a" * 40, base_sha: str = "b" * 40) -> resolver.PullRequest:
    """Build a test pull request snapshot."""
    return resolver.PullRequest(
        repo="microsoft/azurelinux",
        number=number,
        head_sha=head_sha,
        base_sha=base_sha,
    )


def test_equal_versions_skip_merge_poll(monkeypatch: pytest.MonkeyPatch) -> None:
    """Validate one PR snapshot without polling for a test-merge commit."""
    github_api = Mock(return_value=f"{'a' * 40}\t{'b' * 40}\ttrue\n")
    monkeypatch.setattr(resolver, "_github_api", github_api)

    version, render_all = resolver.resolve_version(
        "v1.2.3",
        "v1.2.3",
        pull_request=_pull_request(),
    )

    if version != "v1.2.3" or render_all:
        pytest.fail(f"unexpected resolution: version={version!r}, render_all={render_all!r}")
    if github_api.call_count != 1:
        pytest.fail(f"expected one PR snapshot request, got {github_api.call_count}")


def test_differing_versions_use_test_merge_version(monkeypatch: pytest.MonkeyPatch) -> None:
    """Use the test-merge pin when the base and PR-head pins differ."""
    github_api = Mock(
        side_effect=[
            f"{'a' * 40}\t{'c' * 40}\tnull\n",
            f"{'a' * 40}\t{'c' * 40}\ttrue\n",
            "v2.0.0\n",
        ]
    )
    monkeypatch.setattr(resolver, "_github_api", github_api)
    monkeypatch.setattr(resolver.time, "sleep", Mock())

    version, render_all = resolver.resolve_version(
        "v1.2.3",
        "v2.0.0",
        pull_request=_pull_request(base_sha="c" * 40),
    )

    if version != "v2.0.0" or not render_all:
        pytest.fail(f"unexpected resolution: version={version!r}, render_all={render_all!r}")
    content_endpoint = github_api.call_args_list[-1].args[0]
    if content_endpoint != "repos/microsoft/azurelinux/contents/.azldev-version?ref=refs/pull/1/merge":
        pytest.fail(f"unexpected merge-ref endpoint: {content_endpoint}")


def test_behind_base_uses_base_version_without_full_render(monkeypatch: pytest.MonkeyPatch) -> None:
    """Avoid a full render when the PR merely has an older pin than base."""
    github_api = Mock(side_effect=[f"{'a' * 40}\t{'c' * 40}\ttrue\n", "v2.0.0\n"])
    monkeypatch.setattr(resolver, "_github_api", github_api)

    version, render_all = resolver.resolve_version(
        "v2.0.0",
        "v1.2.3",
        pull_request=_pull_request(base_sha="c" * 40),
    )

    if version != "v2.0.0" or render_all:
        pytest.fail(f"unexpected resolution: version={version!r}, render_all={render_all!r}")


@pytest.mark.parametrize(
    ("pr_number", "expected_head", "expected_base", "message"),
    [
        (0, "a" * 40, "b" * 40, "positive integer"),
        (1, "not-a-sha\n", "b" * 40, "head-sha.*40-character lowercase hex SHA"),
        (1, "a" * 40, "not-a-sha\n", "base-sha.*40-character lowercase hex SHA"),
    ],
)
def test_invalid_inputs_fail_before_github(
    monkeypatch: pytest.MonkeyPatch,
    pr_number: int,
    expected_head: str,
    expected_base: str,
    message: str,
) -> None:
    """Reject malformed reusable-workflow inputs before calling GitHub."""
    github_api = Mock()
    monkeypatch.setattr(resolver, "_github_api", github_api)

    with pytest.raises(resolver.ResolutionError, match=message):
        resolver.resolve_version(
            "v1.2.3",
            "v1.2.3",
            pull_request=_pull_request(
                number=pr_number,
                head_sha=expected_head,
                base_sha=expected_base,
            ),
        )

    github_api.assert_not_called()


def test_stale_base_fails_before_equal_pin_result(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reject a live PR base that differs from the trusted checkout."""
    github_api = Mock(return_value=f"{'a' * 40}\t{'c' * 40}\ttrue\n")
    monkeypatch.setattr(resolver, "_github_api", github_api)

    with pytest.raises(resolver.ResolutionError, match="PR base advanced"):
        resolver.resolve_version(
            "v1.2.3",
            "v1.2.3",
            pull_request=_pull_request(),
        )


def test_github_api_timeout_is_retryable(monkeypatch: pytest.MonkeyPatch) -> None:
    """Translate a hung gh process into the resolver's retryable error."""
    run = Mock(side_effect=subprocess.TimeoutExpired(["gh", "api"], 1))
    monkeypatch.setattr(resolver.subprocess, "run", run)

    with pytest.raises(resolver.GitHubApiError, match="timed out"):
        resolver._github_api("repos/microsoft/azurelinux/pulls/1")  # noqa: SLF001 - test timeout boundary directly


def test_github_api_pins_current_rest_version(monkeypatch: pytest.MonkeyPatch) -> None:
    """Request the REST contract used by the merge-ref implementation."""
    result = subprocess.CompletedProcess([], 0, stdout="ok", stderr="")
    run = Mock(return_value=result)
    monkeypatch.setattr(resolver.subprocess, "run", run)

    if (
        resolver._github_api(  # noqa: SLF001 - test API header boundary directly
            "repos/microsoft/azurelinux/pulls/1"
        )
        != "ok"
    ):
        pytest.fail("unexpected API output")
    command = run.call_args.args[0]
    expected_header = f"X-GitHub-Api-Version: {resolver.GITHUB_API_VERSION}"
    if expected_header not in command:
        pytest.fail(f"API version header missing from command: {command}")


def test_main_rejects_multiline_output_injection(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Reject a multiline pin without emitting attacker-controlled records."""
    base_file = tmp_path / "base-version"
    head_file = tmp_path / "head-version"
    base_file.write_text("v1.2.3\n", encoding="ascii")
    head_file.write_text("safe\nazldev-version=attacker-value\n", encoding="ascii")
    github_api = Mock()
    monkeypatch.setattr(resolver, "_github_api", github_api)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "resolve_azldev_version.py",
            "--repo",
            "microsoft/azurelinux",
            "--pr-number",
            "1",
            "--head-sha",
            "a" * 40,
            "--base-sha",
            "b" * 40,
            "--base-version-file",
            str(base_file),
            "--head-version-file",
            str(head_file),
        ],
    )

    if resolver.main() == 0:
        pytest.fail("multiline version unexpectedly succeeded")
    if capsys.readouterr().out:
        pytest.fail("resolver emitted machine-readable output after rejecting the version")
    github_api.assert_not_called()


def test_read_version_rejects_symlink(tmp_path: Path) -> None:
    """Reject a version-file symlink before reading its target."""
    target = tmp_path / "target"
    link = tmp_path / "version"
    target.write_text("v1.2.3\n", encoding="ascii")
    link.symlink_to(target)

    with pytest.raises(resolver.ResolutionError, match="symlink"):
        resolver._read_version(link)  # noqa: SLF001 - test symlink boundary directly
