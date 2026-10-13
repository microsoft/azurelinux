"""Tests for the portable candidate repository closure checker."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import check_repo_closure as closure
import pytest


def test_collect_candidate_inputs_uses_directory_routing(tmp_path: Path) -> None:
    """Directory placement is the complete routing contract for the engine."""
    base_directory = tmp_path / "base"
    sdk_directory = tmp_path / "sdk"
    base_directory.mkdir()
    sdk_directory.mkdir()
    jq_path = base_directory / "jq.rpm"
    jo_path = sdk_directory / "jo.rpm"
    jq_path.touch()
    jo_path.touch()

    candidates = closure.collect_candidate_inputs(base_directory, sdk_directory)

    assert candidates == [
        {"path": jq_path.resolve(), "repository": "candidate-base"},
        {"path": jo_path.resolve(), "repository": "candidate-sdk"},
    ]


def test_collect_candidate_inputs_requires_at_least_one_rpm(tmp_path: Path) -> None:
    """Do not accidentally report closure without checking fresh artifacts."""
    base_directory = tmp_path / "base"
    base_directory.mkdir()

    with pytest.raises(RuntimeError, match="contain no RPMs"):
        closure.collect_candidate_inputs(base_directory, None)


def test_write_dnf_config_models_both_views(tmp_path: Path) -> None:
    """Include SDK only in the combined published view."""
    candidate_base_repo = tmp_path / "candidate-base"
    candidate_sdk_repo = tmp_path / "candidate-sdk"
    candidate_base_repo.mkdir()
    candidate_sdk_repo.mkdir()
    baseline_config = tmp_path / "baseline.conf"
    candidate_config = tmp_path / "candidate.conf"

    common = {
        "base_repo_url": "https://packages.example/base/x86_64",
        "candidate_base_repo": candidate_base_repo,
        "candidate_sdk_repo": candidate_sdk_repo,
        "sdk_repo_url": "https://packages.example/builddeps/x86_64",
    }
    closure.write_dnf_config(
        config_path=baseline_config,
        excluded_baseline_packages=[],
        include_candidates=False,
        include_sdk=False,
        **common,
    )
    closure.write_dnf_config(
        config_path=candidate_config,
        excluded_baseline_packages=["jq"],
        include_candidates=True,
        include_sdk=True,
        **common,
    )

    baseline_text = baseline_config.read_text(encoding="utf-8")
    candidate_text = candidate_config.read_text(encoding="utf-8")
    assert "[candidate-base]" not in baseline_text
    assert "[candidate-sdk]" not in baseline_text
    assert "[baseline-base]" in baseline_text
    assert "[baseline-sdk]" not in baseline_text
    assert "[candidate-base]" in candidate_text
    assert "[candidate-sdk]" in candidate_text
    assert "[baseline-sdk]" in candidate_text
    assert [
        line for line in candidate_text.splitlines() if line == "excludepkgs=jq"
    ] == ["excludepkgs=jq", "excludepkgs=jq"]


def test_prepare_candidate_repositories_uses_existing_routing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """The engine preserves input routing and builds both overlay repositories."""
    jq_path = tmp_path / "inputs" / "jq.rpm"
    jo_path = tmp_path / "inputs" / "jo.rpm"
    jq_path.parent.mkdir()
    jq_path.write_bytes(closure.RPM_MAGIC + b"jq")
    jo_path.write_bytes(closure.RPM_MAGIC + b"jo")

    headers = {
        jq_path: ("jq", "x86_64"),
        jo_path: ("jo", "x86_64"),
    }
    monkeypatch.setattr(
        closure,
        "query_candidate_header",
        lambda path, _logs: headers[path],
    )
    commands: list[list[str]] = []

    def fake_run(
        command: list[str],
        *,
        log_path: Path,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        del log_path, check
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, "")

    monkeypatch.setattr(closure, "run_command", fake_run)

    _, _, candidates, routes = closure.prepare_candidate_repositories(
        architecture="x86_64",
        candidates=[
            {"path": jq_path, "repository": "candidate-base"},
            {"path": jo_path, "repository": "candidate-sdk"},
        ],
        output_directory=tmp_path / "output",
    )

    assert routes == {"jq": "candidate-base", "jo": "candidate-sdk"}
    assert {candidate["repository"] for candidate in candidates} == {
        "candidate-base",
        "candidate-sdk",
    }
    assert [command[0] for command in commands] == ["createrepo_c", "createrepo_c"]


def test_prepare_candidate_repositories_preserves_input_rpms(tmp_path: Path) -> None:
    """Refuse inputs that would be deleted while regenerating an overlay."""
    output_directory = tmp_path / "output"
    rpm_path = output_directory / "candidate-base" / "jq.rpm"

    with pytest.raises(RuntimeError, match="inside a generated repository"):
        closure.prepare_candidate_repositories(
            architecture="x86_64",
            candidates=[{"path": rpm_path, "repository": "candidate-base"}],
            output_directory=output_directory,
        )


def test_assert_candidate_selected_rejects_baseline_winner(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Prevent a green result that actually solved against the old RPM."""

    def fake_run(
        command: list[str],
        *,
        log_path: Path,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        del log_path, check
        return subprocess.CompletedProcess(
            command,
            0,
            "jq|1.8.1-7.azl4|x86_64|baseline-base\n",
        )

    monkeypatch.setattr(closure, "run_command", fake_run)

    with pytest.raises(RuntimeError, match="not selected exclusively"):
        closure.assert_candidate_selected(
            architecture="x86_64",
            config_path=tmp_path / "dnf.conf",
            expected_repositories={"jq": "candidate-base"},
            log_directory=tmp_path,
        )


def test_parse_repoclosure_issues_ignores_repository_identity() -> None:
    """Compare package/dependency failures independently of repository labels."""
    output = """package: esmtp-1.2-34.azl4.x86_64 from candidate-base
  unresolved deps (2):
    libesmtp.so.6()(64bit)
    liblockfile
Error: Repoclosure ended with unresolved dependencies (2) across 1 packages.
"""

    assert closure.parse_repoclosure_issues(output) == {
        ("esmtp.x86_64", "libesmtp.so.6()(64bit)"): "esmtp-1.2-34.azl4.x86_64",
        ("esmtp.x86_64", "liblockfile"): "esmtp-1.2-34.azl4.x86_64",
    }


@pytest.mark.parametrize(
    ("dnf_major_version", "expected_arch_options", "expected_check_options"),
    [
        (
            4,
            ["--arch=x86_64", "--arch=noarch"],
            ["--check=baseline-base", "--check=candidate-base"],
        ),
        (
            5,
            ["--arch=x86_64,noarch"],
            ["--check=baseline-base,candidate-base"],
        ),
    ],
)
def test_run_repoclosure_uses_generation_specific_list_syntax(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    dnf_major_version: int,
    expected_arch_options: list[str],
    expected_check_options: list[str],
) -> None:
    """DNF 4 repeats list options while DNF5 accepts comma-separated values."""
    commands: list[list[str]] = []

    def fake_run(
        command: list[str],
        *,
        log_path: Path,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        del log_path, check
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, "")

    monkeypatch.setattr(closure, "run_command", fake_run)

    exit_code, issues = closure.run_repoclosure(
        architecture="x86_64",
        config_path=tmp_path / "dnf.conf",
        dnf_major_version=dnf_major_version,
        log_path=tmp_path / "repoclosure.log",
        repositories=["baseline-base", "candidate-base"],
    )

    assert exit_code == 0
    assert issues == {}
    assert [option for option in commands[0] if option.startswith("--arch=")] == (
        expected_arch_options
    )
    assert [option for option in commands[0] if option.startswith("--check=")] == (
        expected_check_options
    )


@pytest.mark.parametrize(
    ("version_output", "expected_major"),
    [("4.24.0\n", 4), ("dnf5 version 5.2.18.0\n", 5)],
)
def test_detect_dnf_major_version_supports_dnf4_and_dnf5(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    version_output: str,
    expected_major: int,
) -> None:
    """Use the argument syntax matching the selected DNF generation."""
    monkeypatch.setattr(
        closure,
        "run_command",
        lambda command, **_kwargs: subprocess.CompletedProcess(
            command,
            0,
            version_output,
        ),
    )

    assert closure.detect_dnf_major_version(tmp_path / "dnf-version.log") == expected_major


@pytest.mark.parametrize(
    ("candidate_issues", "expected_result"),
    [
        (
            {
                (
                    "existing.x86_64",
                    "missing-capability",
                ): "existing-2.azl4.x86_64"
            },
            "passed",
        ),
        (
            {
                (
                    "existing.x86_64",
                    "missing-capability",
                ): "existing-2.azl4.x86_64",
                ("esmtp.x86_64", "liblockfile"): "esmtp-1.2-34.azl4.x86_64",
            },
            "failed",
        ),
    ],
)
def test_run_closure_view_fails_only_on_new_issues(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    candidate_issues: closure.ClosureIssues,
    expected_result: str,
) -> None:
    """Existing baseline failures remain visible without blocking unrelated changes."""
    baseline_issues = {
        ("existing.x86_64", "missing-capability"): "existing-1.azl4.x86_64"
    }
    responses = iter([(1, baseline_issues), (1, candidate_issues)])
    monkeypatch.setattr(
        closure,
        "run_repoclosure",
        lambda **_kwargs: next(responses),
    )
    monkeypatch.setattr(
        closure,
        "run_command",
        lambda command, **_kwargs: subprocess.CompletedProcess(command, 0, ""),
    )
    selection_configs: list[Path] = []

    def fake_assert_candidate_selected(**kwargs: object) -> list[dict[str, str]]:
        config_path = kwargs["config_path"]
        assert isinstance(config_path, Path)
        selection_configs.append(config_path)
        return []

    monkeypatch.setattr(
        closure,
        "assert_candidate_selected",
        fake_assert_candidate_selected,
    )

    report = closure.run_closure_view(
        architecture="x86_64",
        base_repo_url="https://packages.example/base/x86_64",
        candidate_base_repo=tmp_path / "candidate-base",
        candidate_sdk_repo=tmp_path / "candidate-sdk",
        dnf_major_version=4,
        expected_repositories={"esmtp": "candidate-base"},
        include_sdk=False,
        output_directory=tmp_path / "output",
        sdk_repo_url="https://packages.example/builddeps/x86_64",
        view_name="base",
    )

    assert report["result"] == expected_result
    assert report["newUnresolvedDependencies"] == (
        []
        if expected_result == "passed"
        else [
            {
                "dependency": "liblockfile",
                "package": "esmtp-1.2-34.azl4.x86_64",
            }
        ]
    )
    assert selection_configs == [
        tmp_path / "output" / "views" / "base" / "selection-dnf.conf"
    ]


def test_run_check_is_shared_pytest_engine(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Pytest invokes the same engine used by the command-line entry point."""
    rpm_path = tmp_path / "jq.rpm"
    args = argparse.Namespace(
        architecture="x86_64",
        base_repo_url="https://packages.example/base/x86_64",
        candidate_base_dir=tmp_path / "inputs" / "base",
        candidate_sdk_dir=None,
        output_directory=tmp_path / "output",
        sdk_repo_url="https://packages.example/builddeps/x86_64",
    )
    monkeypatch.setattr(
        closure,
        "collect_candidate_inputs",
        lambda _base, _sdk: [{"path": rpm_path, "repository": "candidate-base"}],
    )
    candidate_manifest: list[closure.CandidateRpm] = []
    monkeypatch.setattr(
        closure,
        "prepare_candidate_repositories",
        lambda **_kwargs: (
            tmp_path / "candidate-base",
            tmp_path / "candidate-sdk",
            candidate_manifest,
            {"jq": "candidate-base"},
        ),
    )
    monkeypatch.setattr(
        closure,
        "repomd_checksum",
        lambda url: {"url": f"{url}/repodata/repomd.xml", "sha256": "abc"},
    )
    monkeypatch.setattr(closure, "detect_dnf_major_version", lambda _log_path: 4)

    def fake_view(**kwargs: object) -> dict[str, object]:
        return {
            "baselineRepoclosureExitCode": 0,
            "baselineUnresolvedDependencies": [],
            "candidateRepoclosureExitCode": 0,
            "candidateSelection": [],
            "candidateUnresolvedDependencies": [],
            "name": str(kwargs["view_name"]),
            "newUnresolvedDependencies": [],
            "result": "passed",
        }

    monkeypatch.setattr(closure, "run_closure_view", fake_view)

    report = closure.run_check(args)

    assert report["result"] == "passed"
    assert [view["name"] for view in report["views"]] == ["base", "base-plus-sdk"]


def test_format_new_closure_failures_names_view_package_and_dependency() -> None:
    """Put actionable closure failures directly in CI output."""
    report = {
        "views": [
            {
                "name": "base",
                "newUnresolvedDependencies": [
                    {
                        "dependency": "liblockfile",
                        "package": "esmtp-1.2-34.azl4.x86_64",
                    }
                ],
            },
            {
                "name": "base-plus-sdk",
                "newUnresolvedDependencies": [],
            },
        ]
    }

    assert closure.format_new_closure_failures(report) == [
        "New closure failures in base:",
        "  esmtp-1.2-34.azl4.x86_64 requires liblockfile",
    ]
