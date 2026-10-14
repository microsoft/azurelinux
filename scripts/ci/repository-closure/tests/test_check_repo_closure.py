"""Tests for the portable candidate repository closure checker."""

from __future__ import annotations

import argparse
import subprocess
import sys
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
    assert (tmp_path / "output" / "candidate-base" / "jq.rpm").stat().st_ino == (
        jq_path.stat().st_ino
    )


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

    with pytest.raises(RuntimeError, match="not selected from"):
        closure.assert_candidate_selected(
            architecture="x86_64",
            config_path=tmp_path / "dnf.conf",
            expected_repositories={"jq": "candidate-base"},
            log_directory=tmp_path,
        )


def test_assert_candidate_selected_parses_tied_dnf5_rows(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Policy-only rebuilds may tie baseline EVRs without losing the candidate."""
    commands: list[list[str]] = []

    def fake_run(
        command: list[str],
        *,
        log_path: Path,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        del log_path, check
        commands.append(command)
        return subprocess.CompletedProcess(
            command,
            0,
            "jq|1.8.1-8.azl4|x86_64|candidate-base\n"
            "jq|1.8.1-8.azl4|x86_64|baseline-base\n",
        )

    monkeypatch.setattr(closure, "run_command", fake_run)

    selected = closure.assert_candidate_selected(
        architecture="x86_64",
        config_path=tmp_path / "dnf.conf",
        expected_repositories={"jq": "candidate-base"},
        log_directory=tmp_path,
    )

    assert [row["repository"] for row in selected] == ["candidate-base", "baseline-base"]
    assert len(commands) == 1
    assert commands[0][commands[0].index("--qf") + 1].endswith("\\n")


@pytest.mark.parametrize(
    ("first_dependency", "second_dependency"),
    [
        (
            "(crate(lzma-rust2/std) >= 0.16.1 with crate(lzma-rust2/std) < 0.17.0~)",
            "(crate(lzma-rust2/xz) >= 0.16.1 with crate(lzma-rust2/xz) < 0.17.0~)",
        ),
        (
            "(crate(lzma-rust2/xz) >= 0.16.1 with crate(lzma-rust2/xz) < 0.17.0~)",
            "(crate(lzma-rust2/std) >= 0.16.1 with crate(lzma-rust2/std) < 0.17.0~)",
        ),
    ],
)
def test_run_repoclosure_keeps_stderr_out_of_dependency_identity(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    first_dependency: str,
    second_dependency: str,
) -> None:
    """DNF's error summary must not turn existing failures into new ones."""
    script = f"""
import sys
sys.stdout.write("package: rust-zip+lzma-devel-7.2.0-5.azl4.noarch from baseline-sdk\\n")
sys.stdout.write("  unresolved deps:\\n    {first_dependency}")
sys.stdout.flush()
sys.stderr.write("Error: Repoclosure ended with unresolved dependencies.\\n")
sys.stderr.flush()
sys.stdout.write("\\n    {second_dependency}\\n")
sys.exit(1)
"""
    monkeypatch.setattr(closure, "dnf_prefix", lambda *_args: [sys.executable, "-c", script])
    log_path = tmp_path / "repoclosure.log"

    exit_code, issues = closure.run_repoclosure(
        architecture="x86_64",
        config_path=tmp_path / "dnf.conf",
        dnf_major_version=5,
        log_path=log_path,
        repositories=["baseline-sdk"],
    )

    assert exit_code == 1
    assert issues == {
        ("rust-zip+lzma-devel.noarch", first_dependency): "rust-zip+lzma-devel-7.2.0-5.azl4.noarch",
        ("rust-zip+lzma-devel.noarch", second_dependency): "rust-zip+lzma-devel-7.2.0-5.azl4.noarch",
    }
    assert log_path.read_text() == (
        "package: rust-zip+lzma-devel-7.2.0-5.azl4.noarch from baseline-sdk\n"
        f"  unresolved deps:\n    {first_dependency}\n    {second_dependency}\n"
        "Error: Repoclosure ended with unresolved dependencies.\n"
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


def test_run_repoclosure_rejects_unparsed_dependency_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Fail closed if a DNF output change defeats the issue parser."""
    monkeypatch.setattr(
        closure,
        "run_command",
        lambda command, **_kwargs: subprocess.CompletedProcess(
            command,
            1,
            "Error: Repoclosure ended with unresolved dependencies in a new format.\n",
        ),
    )

    with pytest.raises(RuntimeError, match="no parseable"):
        closure.run_repoclosure(
            architecture="x86_64",
            config_path=tmp_path / "dnf.conf",
            dnf_major_version=5,
            log_path=tmp_path / "repoclosure.log",
            repositories=["baseline-base"],
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
    assert not (tmp_path / "output" / "views" / "base" / "cache").exists()


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
    assert report["baselineRepositories"] == {
        "base": {"url": "https://packages.example/base/x86_64"},
        "sdk": {"url": "https://packages.example/builddeps/x86_64"},
    }
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


def test_remove_runtime_directories_preserves_evidence(tmp_path: Path) -> None:
    """Drop DNF state without deleting reports or command logs."""
    cache = tmp_path / "views" / "base" / "cache"
    persist = tmp_path / "views" / "base" / "persist"
    cache.mkdir(parents=True)
    persist.mkdir()
    report = tmp_path / "repository-closure.json"
    report.write_text("{}\n", encoding="utf-8")

    closure.remove_runtime_directories(tmp_path)

    assert not cache.exists()
    assert not persist.exists()
    assert report.exists()


@pytest.mark.parametrize(
    ("source_names", "expected_names"),
    [
        ({"jq"}, {"jq", "jq-old"}),
        ({"deleted-component"}, {"deleted-library"}),
        ({"moved-to-sdk"}, {"moved-library"}),
    ],
)
def test_query_replaced_binary_names_includes_all_former_outputs(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    source_names: set[str],
    expected_names: set[str],
) -> None:
    """Source inventory tombstones removed binaries, deletions, and channel moves."""
    monkeypatch.setattr(
        closure, "run_command",
        lambda command, **_kwargs: subprocess.CompletedProcess(
            command, 0,
            "jq|jq-1.0-1.src.rpm\n"
            "jq-old|jq-1.0-1.src.rpm\n"
            "deleted-library|deleted-component-2-1.src.rpm\n"
            "moved-library|moved-to-sdk-3-1.src.rpm\n"
            "unrelated|unrelated-4-1.src.rpm\n",
        ),
    )
    assert closure.query_replaced_binary_names(
        architecture="x86_64", config_path=tmp_path / "dnf.conf",
        log_path=tmp_path / "inventory.log", replaced_components=source_names,
    ) == expected_names


@pytest.mark.parametrize("include_sdk", [False, True])
def test_negative_deltas_are_excluded_from_candidate_view_only(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, *, include_sdk: bool,
) -> None:
    """No candidate may borrow deleted outputs or base-to-SDK moved packages."""
    monkeypatch.setattr(
        closure, "run_command",
        lambda command, **_kwargs: subprocess.CompletedProcess(command, 0, ""),
    )
    monkeypatch.setattr(closure, "run_repoclosure", lambda **_kwargs: (0, {}))
    monkeypatch.setattr(closure, "assert_candidate_selected", lambda **_kwargs: [])
    monkeypatch.setattr(
        closure, "query_replaced_binary_names",
        lambda **_kwargs: {"deleted-library", "old-subpackage"},
    )
    report = closure.run_closure_view(
        architecture="x86_64", base_repo_url="https://example.com/base",
        candidate_base_repo=tmp_path / "base", candidate_sdk_repo=tmp_path / "sdk",
        dnf_major_version=4, expected_repositories={}, include_sdk=include_sdk,
        output_directory=tmp_path, sdk_repo_url="https://example.com/sdk",
        view_name="test", replaced_components={"deleted-component", "rebuilt"},
        overlaid_package_names={"moved-to-sdk"},
    )
    assert report["excludedBaselinePackages"] == [
        "deleted-library", "moved-to-sdk", "old-subpackage",
    ]
    directory = tmp_path / "views" / "test"
    assert "excludepkgs=" not in (directory / "baseline-dnf.conf").read_text()
    assert "excludepkgs=" not in (directory / "selection-dnf.conf").read_text()
    assert "excludepkgs=deleted-library,moved-to-sdk,old-subpackage" in (
        directory / "candidate-dnf.conf"
    ).read_text()


def test_run_check_supports_deletion_without_any_candidate_rpms(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    """Deletion-only PRs run both solver views even without a scratch build."""
    replaced_file = tmp_path / "replaced.json"
    replaced_file.write_text('["deleted-component"]')
    args = argparse.Namespace(
        architecture="x86_64", base_repo_url="https://example.com/base",
        sdk_repo_url="https://example.com/sdk", candidate_base_dir=None,
        candidate_sdk_dir=None, output_directory=tmp_path / "reports",
        work_directory=tmp_path / "runtime",
        replaced_source_components_file=replaced_file,
    )
    monkeypatch.setattr(closure, "detect_dnf_major_version", lambda _path: 4)
    monkeypatch.setattr(
        closure, "run_command",
        lambda command, **_kwargs: subprocess.CompletedProcess(command, 0, ""),
    )
    views: list[dict[str, object]] = []

    def fake_view(**kwargs: object) -> dict[str, object]:
        views.append(kwargs)
        return {"result": "passed", "name": kwargs["view_name"]}

    monkeypatch.setattr(closure, "run_closure_view", fake_view)
    report = closure.run_check(args)
    assert report["candidateRpms"] == []
    assert [view["view_name"] for view in views] == ["base", "base-plus-sdk"]
    assert all(view["replaced_components"] == {"deleted-component"} for view in views)
    assert (args.work_directory / "candidate-base").is_dir()
    assert not (args.output_directory / "candidate-base").exists()


def test_run_repoclosure_accepts_parsed_failure_without_english_summary(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    """Both DNF generations report dependency failures through exit status."""
    monkeypatch.setattr(
        closure, "run_command",
        lambda command, **_kwargs: subprocess.CompletedProcess(
            command, 1, "package: jq-1-1.x86_64 from baseline-base\n    missing\n",
        ),
    )
    code, issues = closure.run_repoclosure(
        architecture="x86_64", config_path=tmp_path / "dnf.conf",
        dnf_major_version=5, log_path=tmp_path / "closure.log",
        repositories=["baseline-base"],
    )
    assert code == 1
    assert ("jq.x86_64", "missing") in issues
