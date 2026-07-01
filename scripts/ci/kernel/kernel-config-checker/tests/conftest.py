"""Shared pytest fixtures for kernel config validation checks."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import pytest
from kernel_config_checker.schema.schema import (
    IntentionalKernelConfigSchema,
    load_schema,
)

KERNEL_CONFIG_PATH_PATTERN = re.compile(r"^base/comps/kernel.*/.*config.*$")
KERNEL_CONFIG_JSON_PATH = Path("kernel_config_checker/kernel_configs_json/azl4-os-required-kernel-configs.json")


def pytest_addoption(parser: pytest.Parser) -> None:
    """Allow CI and local runs to pass the diff range explicitly."""
    parser.addoption("--base-sha", action="store", default=os.environ.get("BASE_SHA"))
    parser.addoption("--head-sha", action="store", default=os.environ.get("HEAD_SHA"))
    parser.addoption("--repo-root", action="store", default=os.environ.get("REPO_ROOT"))


def _git_repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


def _checker_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _git_diff_names(repo_root: Path, base_sha: str, head_sha: str, diff_filter: str) -> list[str]:
    result = subprocess.run(
        [
            "git",
            "diff-tree",
            f"--diff-filter={diff_filter}",
            "--no-commit-id",
            "--name-only",
            "-r",
            base_sha,
            head_sha,
        ],
        check=True,
        capture_output=True,
        text=True,
        cwd=repo_root,
    )
    return [line for line in result.stdout.splitlines() if line]


def _kernel_config_path(path: str) -> bool:
    return bool(KERNEL_CONFIG_PATH_PATTERN.match(path))


def _kernel_name_from_path(path: str) -> str:
    return Path(path).parts[2]


def _architecture_from_path(path: str) -> str:
    return "arm64" if "aarch64" in path else "x86_64"


@pytest.fixture(scope="session")
def repo_root(pytestconfig: pytest.Config) -> Path:
    """Return the repository root used for git diff lookups."""
    option = pytestconfig.getoption("repo_root")
    return Path(option).resolve() if option else _git_repo_root()


@pytest.fixture(scope="session")
def base_sha(pytestconfig: pytest.Config) -> str:
    """Return the diff base SHA for the current validation run."""
    return pytestconfig.getoption("base_sha") or "HEAD^"


@pytest.fixture(scope="session")
def head_sha(pytestconfig: pytest.Config) -> str:
    """Return the diff head SHA for the current validation run."""
    return pytestconfig.getoption("head_sha") or "HEAD"


@pytest.fixture(scope="session")
def intentional_schema() -> IntentionalKernelConfigSchema:
    """Load the intentional kernel config schema from the checked-in policy JSON."""
    return load_schema(_checker_root() / KERNEL_CONFIG_JSON_PATH)


@pytest.fixture(scope="session")
def deleted_kernel_config_files(repo_root: Path, base_sha: str, head_sha: str) -> list[str]:
    """Return deleted kernel config files detected between the diff range."""
    return [path for path in _git_diff_names(repo_root, base_sha, head_sha, "D") if _kernel_config_path(path)]


def _tracked_changed_kernel_config_cases(pytestconfig: pytest.Config) -> list[tuple[str, str, str]]:
    repo_root = (
        Path(pytestconfig.getoption("repo_root")).resolve() if pytestconfig.getoption("repo_root") else _git_repo_root()
    )
    checker_root = _checker_root()
    base_sha = pytestconfig.getoption("base_sha") or "HEAD^"
    head_sha = pytestconfig.getoption("head_sha") or "HEAD"
    schema = load_schema(checker_root / KERNEL_CONFIG_JSON_PATH)
    tracked_kernels = {override.name for override in schema.overrides}

    cases: list[tuple[str, str, str]] = []
    for path in _git_diff_names(repo_root, base_sha, head_sha, "d"):
        if not _kernel_config_path(path):
            continue

        kernel_name = _kernel_name_from_path(path)
        if kernel_name not in tracked_kernels:
            continue

        cases.append((path, kernel_name, _architecture_from_path(path)))

    return cases


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Parametrize kernel config validation over changed tracked config files."""
    if "kernel_config_case" not in metafunc.fixturenames:
        return

    cases = _tracked_changed_kernel_config_cases(metafunc.config)
    ids = [f"{kernel_name}:{architecture}:{Path(path).name}" for path, kernel_name, architecture in cases]
    metafunc.parametrize("kernel_config_case", cases, ids=ids)
