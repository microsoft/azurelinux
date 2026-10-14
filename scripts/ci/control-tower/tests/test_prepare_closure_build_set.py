"""Tests for closure-impact component selection."""

from __future__ import annotations

import json
import subprocess
from typing import TYPE_CHECKING

import prepare_closure_build_set as build_set
import pytest
from publication_policy import PublicationPolicy, parse_publication_policy

if TYPE_CHECKING:
    from pathlib import Path


def _policy(
    *,
    base: set[str] | None = None,
    exceptions: dict[str, str] | None = None,
) -> PublicationPolicy:
    return PublicationPolicy(
        base_components=frozenset(base or set()),
        sdk_exception_sources=exceptions or {},
    )


def test_policy_impacted_components_includes_component_channel_moves() -> None:
    """Build components moved between SDK and base even without source changes."""
    assert build_set.policy_impacted_components(
        _policy(base={"bash"}),
        _policy(base={"bash", "jq"}),
    ) == {"jq"}


def test_policy_impacted_components_includes_exception_owners() -> None:
    """Rebuild the source component when a binary carve-out changes."""
    assert build_set.policy_impacted_components(
        _policy(exceptions={"doxygen-latex": "doxygen"}),
        _policy(),
    ) == {"doxygen"}


def test_parse_publication_policy_requires_exception_source_owner() -> None:
    """Fail closed when package-level routing cannot identify its component."""
    text = """
[default-component-config.publish]
rpm-channel = "rpm-sdk"

[component-groups.base-packages]
default-component-config.publish.rpm-channel = "rpm-base"
components = ["doxygen"]

[package-groups.exceptions-packages]
default-package-config.publish.rpm-channel = "rpm-sdk"
packages = ["doxygen-latex"]
"""
    with pytest.raises(RuntimeError, match="missing '# srpm:' ownership"):
        parse_publication_policy(text, source="test policy")


def test_parse_publication_policy_rejects_unknown_routing_group() -> None:
    """Do not silently ignore new publication semantics."""
    text = """
[default-component-config.publish]
rpm-channel = "rpm-sdk"

[component-groups.base-packages]
default-component-config.publish.rpm-channel = "rpm-base"
components = []

[component-groups.future-channel]
components = []

[package-groups.exceptions-packages]
default-package-config.publish.rpm-channel = "rpm-sdk"
packages = []
"""
    with pytest.raises(RuntimeError, match="unsupported component groups"):
        parse_publication_policy(text, source="test policy")


def test_prepare_build_set_combines_source_and_policy_changes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Policy-only promotions augment rather than replace source changes."""
    changes = tmp_path / "changed-components.json"
    changes.write_text(
        json.dumps(
            [
                {"changeType": "changed", "component": "bash"},
                {"changeType": "unchanged", "component": "jq"},
            ]
        ),
        encoding="utf-8",
    )
    policies = iter([_policy(base={"bash"}), _policy(base={"bash", "jq"})])
    monkeypatch.setattr(build_set, "read_policy_at_commit", lambda *_args: next(policies))

    assert build_set.prepare_build_set(
        base_commit="base",
        changed_components_file=changes,
        policy_path=build_set.DEFAULT_POLICY_PATH,
        source_commit="source",
    ) == ["bash", "jq"]


def test_read_policy_at_commit_uses_exact_git_object(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Do not derive baseline policy from the candidate worktree."""
    policy = """
[default-component-config.publish]
rpm-channel = "rpm-sdk"

[component-groups.base-packages]
default-component-config.publish.rpm-channel = "rpm-base"
components = ["jq"]

[package-groups.exceptions-packages]
default-package-config.publish.rpm-channel = "rpm-sdk"
packages = []
"""
    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        del kwargs
        command = args[0]
        assert isinstance(command, list)
        return subprocess.CompletedProcess(command, 0, policy, "")

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = build_set.read_policy_at_commit("abc123", build_set.DEFAULT_POLICY_PATH)

    assert result.base_components == frozenset({"jq"})


def test_prepare_build_set_skips_explicit_deletions(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    """Supported removals become repository tombstones, not impossible builds."""
    changes = tmp_path / "changes.json"
    changes.write_text(json.dumps([
        {"changeType": "deleted", "component": "jq"},
        {"changeType": "changed", "component": "bash"},
    ]))
    policies = iter([_policy(base={"jq", "bash"}), _policy(base={"bash"})])
    monkeypatch.setattr(build_set, "read_policy_at_commit", lambda *_args: next(policies))
    assert build_set.prepare_build_set(
        base_commit="base", changed_components_file=changes,
        policy_path=build_set.DEFAULT_POLICY_PATH, source_commit="head",
    ) == ["bash"]
    assert build_set.package_build.load_deleted_components(changes) == {"jq"}


def test_prepare_build_set_still_rejects_unknown_policy_component(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    """Only explicit deletions excuse an unavailable component."""
    changes = tmp_path / "changes.json"
    changes.write_text("[]")
    policies = iter([_policy(), _policy(base={"typo"})])
    monkeypatch.setattr(build_set, "read_policy_at_commit", lambda *_args: next(policies))
    with pytest.raises(RuntimeError, match="absent from the candidate"):
        build_set.prepare_build_set(
            base_commit="base", changed_components_file=changes,
            policy_path=build_set.DEFAULT_POLICY_PATH, source_commit="head",
        )
