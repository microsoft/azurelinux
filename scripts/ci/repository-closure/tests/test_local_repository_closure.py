"""Exercise negative deltas and equal-EVR overlays with real local repositories."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import check_repo_closure as closure
import pytest


def _run(command: list[str]) -> None:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        pytest.fail(f"{command!r} failed:\n{result.stdout}\n{result.stderr}")


def _build(
    directory: Path, name: str, subpackage: str | None = None, *, architecture: str = "noarch",
) -> list[Path]:
    directory.mkdir(parents=True)
    extra = ""
    if subpackage is not None:
        extra = f"""
%package -n {subpackage}
Summary: Closure test subpackage
BuildArch: noarch
%description -n {subpackage}
Closure test subpackage.
%files -n {subpackage}
"""
    requires = "Requires: closure-old\n" if name == "closure-consumer" else ""
    build_arch = "BuildArch: noarch\n" if architecture == "noarch" else ""
    spec = directory / f"{name}.spec"
    spec.write_text(
        f"""Name: {name}
Version: 1
Release: 1
Summary: Closure test fixture
License: MIT
{build_arch}{requires}
%description
Closure test fixture.
%files
{extra}
""",
        encoding="utf-8",
    )
    command = ["rpmbuild", "-bb", "--define", f"_topdir {directory}"]
    if architecture != "noarch":
        command.extend(["--target", architecture])
    _run([*command, str(spec)])
    return sorted((directory / "RPMS").rglob("*.rpm"))


@pytest.fixture(params=["x86_64", "aarch64"])
def architecture(request: pytest.FixtureRequest) -> str:
    """Exercise native and noarch repository metadata for each supported target."""
    assert isinstance(request.param, str)
    return request.param


@pytest.fixture
def local_repositories(tmp_path: Path, architecture: str) -> dict[str, object]:
    """Build isolated fixtures without downloads or package installation."""
    for tool in ("rpmbuild", "createrepo_c", closure.DNF_COMMAND):
        if shutil.which(tool) is None:
            pytest.skip(f"Local repository integration requires {tool}")
    result = subprocess.run(
        [closure.DNF_COMMAND, "repoclosure", "--help"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        pytest.skip("Local repository integration requires the repoclosure plugin")
    baseline_rpms = _build(
        tmp_path / "build-baseline", "closure-source", "closure-old", architecture=architecture,
    )
    consumer_rpms = _build(tmp_path / "build-consumer", "closure-consumer")
    replaced_rpms = _build(
        tmp_path / "build-replaced", "closure-source", architecture=architecture,
    )
    renamed_rpms = _build(
        tmp_path / "build-renamed", "closure-source", "closure-new", architecture=architecture,
    )
    base = tmp_path / "baseline-base"
    sdk = tmp_path / "baseline-sdk"
    base.mkdir()
    sdk.mkdir()
    for rpm in baseline_rpms + consumer_rpms:
        shutil.copy2(rpm, base / rpm.name)
    _run(["createrepo_c", str(base)])
    _run(["createrepo_c", str(sdk)])
    return {
        "base": base, "sdk": sdk, "original": baseline_rpms,
        "removed": replaced_rpms, "renamed": renamed_rpms,
    }


@pytest.mark.parametrize(
    ("scenario", "candidate_channel", "expected_results"),
    [
        ("original", "candidate-base", ["passed", "passed"]),
        ("original", "candidate-sdk", ["failed", "passed"]),
        ("removed", "candidate-base", ["failed", "failed"]),
        ("renamed", "candidate-base", ["failed", "failed"]),
        ("deleted", "candidate-base", ["failed", "failed"]),
    ],
)
def test_local_repository_deltas(
    local_repositories: dict[str, object],
    tmp_path: Path,
    scenario: str,
    candidate_channel: str,
    expected_results: list[str],
    architecture: str,
) -> None:
    """Actual DNF must not satisfy dependencies from tombstoned baseline RPMs."""
    inputs: list[closure.CandidateInput] = []
    if scenario != "deleted":
        rpms = local_repositories[scenario]
        assert isinstance(rpms, list)
        inputs = [{"path": rpm, "repository": candidate_channel} for rpm in rpms]
    candidate_base, candidate_sdk, _, routes = closure.prepare_candidate_repositories(
        architecture=architecture, candidates=inputs, output_directory=tmp_path / "runtime",
    )
    base = local_repositories["base"]
    sdk = local_repositories["sdk"]
    assert isinstance(base, Path)
    assert isinstance(sdk, Path)
    version = closure.detect_dnf_major_version(tmp_path / "dnf-version.log")
    results = []
    for include_sdk, name in [(False, "base"), (True, "base-plus-sdk")]:
        report = closure.run_closure_view(
            architecture=architecture, base_repo_url=base.as_uri(),
            sdk_repo_url=sdk.as_uri(), candidate_base_repo=candidate_base,
            candidate_sdk_repo=candidate_sdk, dnf_major_version=version,
            expected_repositories={
                package: repository for package, repository in routes.items()
                if include_sdk or repository == "candidate-base"
            },
            include_sdk=include_sdk, output_directory=tmp_path / "reports",
            view_name=name, replaced_components={"closure-source"},
            overlaid_package_names=set(routes),
        )
        assert report["baselineUnresolvedDependencies"] == []
        assert "closure-old" in report["excludedBaselinePackages"]
        results.append(report["result"])
        if report["result"] == "failed":
            assert report["newUnresolvedDependencies"] == [{
                "dependency": "closure-old",
                "package": "closure-consumer-1-1.noarch",
            }]
    assert results == expected_results
