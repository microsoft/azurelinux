# SPDX-License-Identifier: MIT
"""Validate shipped repository defaults independently of image build sources."""

from __future__ import annotations

from configparser import ConfigParser
from typing import TYPE_CHECKING

import pytest
from utils.extract import read_text_confined

if TYPE_CHECKING:
    from pathlib import Path

pytestmark = pytest.mark.require_capability("runtime-package-management")

CHANNELS = ("base", "cloud-native", "microsoft")
PRODUCTION_REPOS = {f"azurelinux-{channel}" for channel in CHANNELS}


@pytest.fixture
def repositories(rootfs: Path) -> ConfigParser:
    config = ConfigParser(interpolation=None)
    for path in sorted((rootfs / "etc/yum.repos.d").glob("*.repo")):
        config.read_string(
            read_text_confined(rootfs, f"etc/yum.repos.d/{path.name}"),
            source=path.name,
        )
    if not config.sections():
        pytest.fail("No repository definitions shipped in /etc/yum.repos.d")
    return config


@pytest.mark.parametrize("channel", CHANNELS)
@pytest.mark.parametrize("preview", [False, True])
@pytest.mark.parametrize("suffix", ["", "-source", "-debuginfo"])
def test_repository_defaults(
    repositories: ConfigParser,
    channel: str,
    preview: bool,
    suffix: str,
) -> None:
    repo_id = f"azurelinux-{'preview-' if preview else ''}{channel}{suffix}"
    assert repositories.has_section(repo_id), f"Missing repository definition: {repo_id}"

    expected_enabled = not preview and not suffix
    assert repositories.getboolean(repo_id, "enabled") == expected_enabled, (
        f"{repo_id}: expected enabled={int(expected_enabled)}"
    )

    content = "srpms" if suffix == "-source" else (
        "debuginfo/$basearch" if suffix == "-debuginfo" else "$basearch"
    )
    expected_url = (
        f"https://packages.microsoft.com/azurelinux/4/"
        f"{'preview' if preview else 'prod'}/{channel}/{content}"
    )
    assert repositories.get(repo_id, "baseurl") == expected_url, (
        f"{repo_id}: expected baseurl={expected_url}"
    )


def test_only_production_repositories_enabled(repositories: ConfigParser) -> None:
    enabled = {
        repo_id
        for repo_id in repositories.sections()
        if repositories.getboolean(repo_id, "enabled", fallback=True)
    }
    assert enabled == PRODUCTION_REPOS, (
        f"Expected only {sorted(PRODUCTION_REPOS)} enabled, got {sorted(enabled)}"
    )
