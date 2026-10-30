# SPDX-License-Identifier: MIT
"""Pytest options and native-tool preflight for component RPM validation."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse

import pytest

RPMINSPECT_POLICY_PATH = Path("/usr/share/rpminspect/azurelinux.yaml")
CONTAINER_ENVIRONMENT_FLAG = "AZL_COMPONENT_TESTS_IN_CONTAINER"
CONTAINER_RUNNER_IMAGE = "localhost/azl4-rpm-validation:dev"


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register candidate-RPM inputs before pytest resolves test paths."""
    group = parser.getgroup("component", "Azure Linux component validation")
    group.addoption(
        "--rpm-path",
        action="append",
        default=[],
        metavar="PATH",
        help="Candidate RPM file to validate; may be specified multiple times.",
    )
    group.addoption(
        "--rpm-dir",
        action="append",
        default=[],
        metavar="DIR",
        help="Directory containing candidate RPM files; may be specified multiple times.",
    )
    group.addoption(
        "--baseline-rpm-path",
        action="append",
        default=[],
        metavar="PATH",
        help="Baseline RPM file for rpminspect comparison; may be specified multiple times.",
    )
    group.addoption(
        "--baseline-rpm-dir",
        action="append",
        default=[],
        metavar="DIR",
        help="Directory containing baseline RPM files for rpminspect comparison.",
    )
    group.addoption(
        "--rpminspect-local-config",
        default=None,
        metavar="PATH",
        help="Optional component rpminspect.yaml overlay discovered from its source tree.",
    )
    group.addoption(
        "--rmdepcheck-base-repo",
        action="append",
        default=[],
        metavar="URL",
        help="Baseline repository URL for rmdepcheck; may be specified multiple times.",
    )
    group.addoption(
        "--rpmdeplint-repo",
        action="append",
        default=[],
        metavar="NAME[,URL_OR_PATH]",
        help=(
            "Repo to resolve candidate dependencies against for rpmdeplint; "
            "may be specified multiple times."
        ),
    )
    group.addoption(
        "--container-image",
        default=None,
        metavar="IMAGE",
        help="Run validation in a fresh container built from this AZL base image.",
    )


def rpm_inputs(
    config: pytest.Config, path_option: str, directory_option: str, description: str
) -> list[Path]:
    """Return sorted, unique RPM inputs supplied through matching CLI options."""
    paths: set[Path] = set()

    for raw_path in config.getoption(path_option):
        path = Path(raw_path).resolve()
        if not path.is_file():
            raise pytest.UsageError(f"{path_option} is not a file: {path}")
        if path.suffix != ".rpm":
            raise pytest.UsageError(f"{path_option} must name an RPM file: {path}")
        paths.add(path)

    for raw_dir in config.getoption(directory_option):
        directory = Path(raw_dir).resolve()
        if not directory.is_dir():
            raise pytest.UsageError(f"{directory_option} is not a directory: {directory}")
        paths.update(path for path in directory.rglob("*.rpm") if path.is_file())

    if not paths:
        raise pytest.UsageError(f"At least one {description} RPM is required.")

    return sorted(paths)


def candidate_rpms(config: pytest.Config) -> list[Path]:
    """Return candidate RPM artifacts supplied through the command line."""
    return rpm_inputs(config, "--rpm-path", "--rpm-dir", "candidate")


def baseline_rpms(config: pytest.Config) -> list[Path]:
    """Return baseline RPM artifacts used for rpminspect comparisons."""
    return rpm_inputs(
        config,
        "--baseline-rpm-path",
        "--baseline-rpm-dir",
        "baseline",
    )


def rpminspect_local_config(config: pytest.Config) -> Path | None:
    """Return the optional component-local rpminspect.yaml overlay."""
    raw_path = config.getoption("--rpminspect-local-config")
    if raw_path is None:
        return None

    path = Path(raw_path).resolve()
    if not path.is_file() or path.name != "rpminspect.yaml":
        raise pytest.UsageError(
            "--rpminspect-local-config must name an rpminspect.yaml file: "
            f"{path}"
        )
    return path


def rmdepcheck_base_repos(config: pytest.Config) -> list[str]:
    """Return baseline repository URLs used for reverse-dependency validation."""
    repositories = config.getoption("--rmdepcheck-base-repo")
    if not repositories:
        raise pytest.UsageError(
            "rmdepcheck validation requires at least one --rmdepcheck-base-repo URL"
        )
    return repositories


def rpmdeplint_repos(config: pytest.Config) -> list[str]:
    """Return repo arguments used to resolve candidate dependencies with rpmdeplint."""
    repositories = config.getoption("--rpmdeplint-repo")
    if not repositories:
        raise pytest.UsageError(
            "rpmdeplint validation requires at least one --rpmdeplint-repo NAME[,URL_OR_PATH]"
        )
    return repositories


def container_image(config: pytest.Config) -> str | None:
    """Return the optional AZL base image used for isolated validation."""
    return config.getoption("--container-image")


def pytest_cmdline_main(config: pytest.Config) -> int | None:
    """Re-execute generic validation inside the requested fresh AZL container."""
    base_image = container_image(config)
    if base_image is None or os.environ.get(CONTAINER_ENVIRONMENT_FLAG) == "1":
        return None

    candidate_paths = candidate_rpms(config)
    baseline_paths = (
        baseline_rpms(config)
        if config.getoption("--baseline-rpm-path") or config.getoption("--baseline-rpm-dir")
        else []
    )
    local_config = (
        rpminspect_local_config(config)
        if config.getoption("--rpminspect-local-config") is not None
        else None
    )

    test_directory = Path(__file__).resolve().parents[1]
    dockerfile = test_directory / "container" / "Dockerfile"
    _require_container_base_image(base_image)
    image_id = _run_container_build(dockerfile, test_directory, base_image)

    command = [
        "podman",
        "run",
        "--rm",
        "--network",
        "host",
        "--env",
        f"{CONTAINER_ENVIRONMENT_FLAG}=1",
    ]
    inner_args = _mounted_rpm_arguments(command, candidate_paths, "/candidate", "--rpm-path")

    if baseline_paths:
        inner_args.extend(
            _mounted_rpm_arguments(command, baseline_paths, "/baseline", "--baseline-rpm-path")
        )
    if local_config is not None:
        command.extend(("--volume", f"{local_config.parent}:/rpminspect-local:ro"))
        inner_args.extend(("--rpminspect-local-config", "/rpminspect-local/rpminspect.yaml"))

    base_repositories = config.getoption("--rmdepcheck-base-repo")
    for repository in base_repositories:
        inner_args.extend(("--rmdepcheck-base-repo", repository))

    rpmdeplint_repositories = config.getoption("--rpmdeplint-repo")
    for index, repository in enumerate(rpmdeplint_repositories):
        inner_args.extend(("--rpmdeplint-repo", _mounted_repo_argument(command, repository, index)))

    markers = config.getoption("markexpr")
    if not markers:
        markers = "rpm_artifact or rpmlint or container_smoke"
        if baseline_paths:
            markers += " or rpminspect"
        if base_repositories:
            markers += " or rmdepcheck"
        if rpmdeplint_repositories:
            markers += " or rpmdeplint"
    inner_args.extend(("-m", markers))

    if config.option.keyword:
        inner_args.extend(("-k", config.option.keyword))
    if getattr(config.option, "collectonly", False):
        inner_args.append("--collect-only")
    if getattr(config.option, "exitfirst", False):
        inner_args.append("-x")

    node_ids = list(config.args) if config.args else ["cases/"]

    command.extend((image_id, *node_ids, *inner_args))
    result = subprocess.run(command, check=False)
    return result.returncode


def _require_container_base_image(base_image: str) -> None:
    """Ensure the selected base image can install the validation toolchain."""
    result = subprocess.run(
        [
            "podman",
            "run",
            "--rm",
            "--user",
            "0",
            "--entrypoint",
            "/bin/sh",
            base_image,
            "-c",
            "test -r /usr/lib/rpm/rpmrc && command -v dnf5 >/dev/null",
        ],
        check=False,
    )
    if result.returncode != 0:
        raise pytest.UsageError(
            "--container-image must name a project-built AZL4 container-base image; "
            "build it with 'azldev image build container-base'"
        )


def _run_container_build(dockerfile: Path, test_directory: Path, base_image: str) -> str:
    """Build the local runner image with the supplied AZL base image.

    Installs rpmlint, rpminspect, rpminspect-data-azurelinux, rmdepcheck, and
    rpmdeplint by name from the repos already configured in the base image
    (see base/comps/tests/container/Dockerfile), so no locally built RPMs are
    required here. Returns the built image's immutable ID (via --iidfile)
    rather than the mutable CONTAINER_RUNNER_IMAGE tag, so a concurrent build
    from another invocation can never cause this run to execute against a
    different base image, tool set, or policy.
    """
    with NamedTemporaryFile(prefix="azl-rpm-validation-iid-") as iid_file:
        result = subprocess.run(
            [
                "podman",
                "build",
                "--file",
                str(dockerfile),
                "--tag",
                CONTAINER_RUNNER_IMAGE,
                "--iidfile",
                iid_file.name,
                "--build-arg",
                f"BASE_IMAGE={base_image}",
                "--build-arg",
                f"AZL_ARCH={os.uname().machine}",
                str(test_directory),
            ],
            check=False,
        )
        if result.returncode != 0:
            raise pytest.UsageError("unable to build the Azure Linux RPM validation container")
        return Path(iid_file.name).read_text().strip()


def _mounted_rpm_arguments(
    command: list[str], rpm_paths: list[Path], container_directory: str, option: str
) -> list[str]:
    """Mount RPM paths read-only and return their matching container options."""
    arguments: list[str] = []
    for index, rpm_path in enumerate(rpm_paths):
        target = f"{container_directory}/{index}-{rpm_path.name}"
        command.extend(("--volume", f"{rpm_path}:{target}:ro"))
        arguments.extend((option, target))
    return arguments


def _mounted_repo_argument(command: list[str], repository: str, index: int) -> str:
    """Mount a local repo path read-only and rewrite the NAME,PATH argument.

    rpmdeplint's --repo option accepts NAME[,URL_OR_PATH]. A URL is passed
    through unchanged, but a local filesystem path is only meaningful on the
    host; without mounting it into the container, the path either does not
    exist there or resolves against the wrong working directory.
    """
    if "," not in repository:
        return repository
    name, _, location = repository.partition(",")
    if urlparse(location).scheme:
        return repository
    host_path = Path(location).resolve()
    if not host_path.exists():
        raise pytest.UsageError(f"--rpmdeplint-repo path does not exist: {host_path}")
    target = f"/rpmdeplint-repo/{index}"
    command.extend(("--volume", f"{host_path}:{target}:ro"))
    return f"{name},{target}"


def pytest_configure(config: pytest.Config) -> None:
    """Register markers used by component validation tests."""
    config.addinivalue_line(
        "markers",
        "requires_tool(name): skip test unless the named native tool is available",
    )
    config.addinivalue_line(
        "markers",
        "rpm_artifact: generic RPM signature, payload, and metadata validation",
    )
    config.addinivalue_line(
        "markers",
        "rpmlint: packaging-policy validation performed by rpmlint",
    )
    config.addinivalue_line(
        "markers",
        "rpminspect: static RPM comparison performed by rpminspect",
    )
    config.addinivalue_line(
        "markers",
        "rmdepcheck: candidate repository reverse-dependency validation",
    )
    config.addinivalue_line(
        "markers",
        "rpmdeplint: candidate RPM dependency satisfiability, conflicts, and upgrade validation",
    )
    config.addinivalue_line(
        "markers",
        "container_smoke: candidate repository installation in the clean validation container",
    )
    config.addinivalue_line(
        "markers",
        "installability: install the candidate RPM set from a temporary repository",
    )
    if config.getoption("--rpminspect-local-config") is not None:
        rpminspect_local_config(config)


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Skip a test when a required tool is unavailable, fail inside the container.

    The purpose-built validation container always provides every validation
    tool; a missing tool there means the runner image is misconfigured, not
    that the check is optional, so it must fail rather than silently skip
    (which would otherwise let a run report success with that check never
    having executed). Outside the container (native-host execution), a
    missing tool remains an environment limitation and is skipped.
    """
    in_container = os.environ.get(CONTAINER_ENVIRONMENT_FLAG) == "1"
    for marker in item.iter_markers("requires_tool"):
        tool = marker.args[0] if marker.args else None
        if tool and shutil.which(tool) is None:
            message = f"requires native tool '{tool}' on PATH"
            if in_container:
                pytest.fail(f"{message} (missing inside the validation container)")
            pytest.skip(message)
