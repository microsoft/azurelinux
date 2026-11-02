# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Exercise Base membership and the actual package-build change classification."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import check_base_promotions as guard
import pytest


def _git(*args: str) -> str:
    """Run git in the isolated fixture repository."""
    return subprocess.run(
        ["git", "-c", "core.hooksPath=/dev/null", *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _commit_members(members: list[str]) -> str:
    """Commit only the publishing configuration for a range endpoint."""
    config = Path(guard.PUBLISH_CHANNELS_PATH)
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(
        "[component-groups.base-packages]\ncomponents = " + json.dumps(members, indent=2) + "\n",
        encoding="utf-8",
    )
    _git("add", guard.PUBLISH_CHANNELS_PATH)
    _git("commit", "-m", "test: set Base membership")
    return _git("rev-parse", "HEAD")


@pytest.fixture
def base_ref(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    """Create a small committed baseline, independent of Azure Linux history."""
    monkeypatch.chdir(tmp_path)
    _git("init")
    _git("config", "user.name", "Tobias Brick")
    _git("config", "user.email", "tobiasb@microsoft.com")
    _git("config", "commit.gpgsign", "false")
    return _commit_members(["existing"])


def _changes(tmp_path: Path, entries: object) -> Path:
    """Write the change-set artifact that the pipeline would produce."""
    path = tmp_path / "changed-components.json"
    path.write_text(json.dumps(entries), encoding="utf-8")
    return path


@pytest.mark.parametrize("change_type", ["added", "changed"])
def test_promotion_with_build_identity_change_passes(base_ref: str, tmp_path: Path, change_type: str) -> None:
    """A new component or genuine input change needs no additional manual bump."""
    head = _commit_members(["existing", "promoted"])
    changes = _changes(tmp_path, [{"component": "promoted", "changeType": change_type, "sourcesChange": False}])
    guard.check_base_promotions(base_ref, head, changes)


@pytest.mark.parametrize("change_type", ["unchanged", "deleted", None])
def test_promotion_outside_build_set_fails(base_ref: str, tmp_path: Path, change_type: str | None) -> None:
    """A sources-only signal or missing entry does not cause an official rebuild."""
    head = _commit_members(["existing", "promoted"])
    entries = [] if change_type is None else [
        {"component": "promoted", "changeType": change_type, "sourcesChange": True}
    ]
    with pytest.raises(ValueError, match="azldev comp update -p promoted --bump"):
        guard.check_base_promotions(base_ref, head, _changes(tmp_path, entries))


@pytest.mark.usefixtures("base_ref")
def test_reordering_comments_and_removal_do_not_require_bumps(tmp_path: Path) -> None:
    """Membership is a set comparison, not a textual diff or whole-list rebuild."""
    before = _commit_members(["existing", "retained", "removed"])
    _commit_members(["retained", "existing"])
    config = Path(guard.PUBLISH_CHANNELS_PATH)
    config.write_text(config.read_text(encoding="utf-8") + "# formatting only\n", encoding="utf-8")
    _git("add", guard.PUBLISH_CHANNELS_PATH)
    _git("commit", "-m", "test: add a comment")
    guard.check_base_promotions(before, "HEAD", _changes(tmp_path, []))


def test_committed_refs_not_working_tree_determine_additions(base_ref: str, tmp_path: Path) -> None:
    """An unstaged edit cannot hide a committed promotion from the guard."""
    head = _commit_members(["existing", "promoted"])
    Path(guard.PUBLISH_CHANNELS_PATH).write_text(
        "[component-groups.base-packages]\ncomponents = []\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="'promoted'"):
        guard.check_base_promotions(base_ref, head, _changes(tmp_path, []))


def test_merge_base_excludes_target_branch_removals(base_ref: str, tmp_path: Path) -> None:
    """A stale PR must not treat a target-only Base removal as its own promotion."""
    _git("checkout", "-b", "target")
    target = _commit_members([])
    _git("checkout", "-b", "topic", base_ref)
    head = _commit_members(["existing", "promoted"])
    changes = _changes(tmp_path, [{"component": "promoted", "changeType": "changed"}])

    with pytest.raises(ValueError, match="'existing'"):
        guard.check_base_promotions(target, head, changes)
    merge_base = _git("merge-base", target, head)
    guard.check_base_promotions(merge_base, head, changes)


def test_current_base_excludes_already_landed_stacked_promotions(base_ref: str, tmp_path: Path) -> None:
    """A base advance before execution must not charge a child PR for its parent."""
    current_base = _commit_members(["existing", "landed"])
    head = _commit_members(["existing", "landed", "promoted"])
    changes = _changes(
        tmp_path,
        [
            {"component": "landed", "changeType": "unchanged"},
            {"component": "promoted", "changeType": "changed"},
        ],
    )

    with pytest.raises(ValueError, match="'landed'"):
        guard.check_base_promotions(_git("merge-base", base_ref, head), head, changes)
    guard.check_base_promotions(_git("merge-base", current_base, head), head, changes)


def _commit_file(path: str, content: str) -> str:
    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content, encoding="utf-8")
    _git("add", path)
    _git("commit", "-m", "test: change component input")
    return _git("rev-parse", "HEAD")


def _prepare_merge(base: str, head: str) -> subprocess.CompletedProcess[str]:
    helper = Path(guard.__file__).with_name("prepare_base_promotion_merge.sh")
    return subprocess.run(
        ["bash", str(helper), base, head],
        check=False,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize("landing", ["squash", "rebase"])
@pytest.mark.usefixtures("base_ref")
def test_merged_comparison_rejects_rewritten_parent_bump(tmp_path: Path, landing: str) -> None:
    """A parent bump already in the target cannot fund a child-only promotion."""
    initial = _commit_file("locks/promoted.lock", 'input-fingerprint = "original"\n')
    _git("checkout", "-b", "parent")
    parent = _commit_file("locks/promoted.lock", 'input-fingerprint = "parent-bump"\n')
    _git("checkout", "-b", "child")
    head = _commit_members(["existing", "promoted"])
    _git("checkout", "-b", "target", initial)
    _commit_file("target-only", "Unrelated target advance\n")
    if landing == "squash":
        _git("merge", "--squash", parent)
        _git("commit", "-m", "test: squash parent bump")
    else:
        _git("cherry-pick", parent)
    target = _git("rev-parse", "HEAD")
    assert target != parent
    _git("checkout", "child")

    # The old fork-point comparison incorrectly accepts the already-landed bump.
    fork_point = _git("merge-base", target, head)
    assert _git("show", f"{fork_point}:locks/promoted.lock") != _git("show", f"{head}:locks/promoted.lock")
    guard.check_base_promotions(
        fork_point, head, _changes(tmp_path, [{"component": "promoted", "changeType": "changed"}])
    )

    result = _prepare_merge(target, head)
    assert result.returncode == 0, result.stderr
    merged = result.stdout.strip()
    assert _git("rev-parse", "HEAD") == merged
    assert _git("show", "-s", "--format=%P", merged) == f"{target} {head}"
    assert _git("show", f"{target}:locks/promoted.lock") == _git("show", f"{merged}:locks/promoted.lock")
    with pytest.raises(ValueError, match="'promoted'"):
        guard.check_base_promotions(
            target, merged, _changes(tmp_path, [{"component": "promoted", "changeType": "unchanged"}])
        )


@pytest.mark.usefixtures("base_ref")
def test_merged_comparison_preserves_target_changes_and_accepts_fresh_bump(tmp_path: Path) -> None:
    """A stale branch must not undo target-only inputs or Base removals."""
    retained = [f"retained-{index}" for index in range(10)]
    initial = _commit_members(["existing", *retained])
    _git("checkout", "-b", "target")
    _commit_file("locks/target-only.lock", 'input-fingerprint = "target-bump"\n')
    target = _commit_members(retained)
    _git("checkout", "-b", "child", initial)
    _commit_file("locks/promoted.lock", 'input-fingerprint = "fresh-bump"\n')
    head = _commit_members(["existing", *retained, "promoted"])

    result = _prepare_merge(target, head)
    assert result.returncode == 0, result.stderr
    merged = result.stdout.strip()
    assert _git("show", f"{target}:locks/target-only.lock") == _git("show", f"{merged}:locks/target-only.lock")
    assert guard.base_components_at(merged) == {*retained, "promoted"}
    guard.check_base_promotions(
        target, merged, _changes(tmp_path, [{"component": "promoted", "changeType": "added"}])
    )


def test_conflicting_merge_fails_before_changing_checkout(base_ref: str) -> None:
    """Conflicts must fail explicitly, not fall back to the stale PR tree."""
    _git("checkout", "-b", "target")
    target = _commit_members(["existing", "target"])
    _git("checkout", "-b", "child", base_ref)
    head = _commit_members(["existing", "promoted"])

    result = _prepare_merge(target, head)
    assert result.returncode != 0
    assert "PR does not merge cleanly with the captured target" in result.stderr
    assert "CONFLICT" in result.stderr
    assert _git("rev-parse", "HEAD") == head


@pytest.mark.parametrize(
    "entries",
    [
        {},
        [None],
        [{"changeType": "changed"}],
        [{"component": "promoted", "changeType": "unknown"}],
        [{"component": "promoted", "changeType": "changed"}] * 2,
    ],
)
def test_malformed_change_sets_fail_closed(base_ref: str, tmp_path: Path, entries: object) -> None:
    """Invalid artifacts must not turn the guard into a success-shaped fallback."""
    with pytest.raises((TypeError, ValueError), match=r"changed-components\.json"):
        guard.check_base_promotions(base_ref, base_ref, _changes(tmp_path, entries))


@pytest.mark.parametrize(
    "config",
    [
        "not valid TOML",
        "[component-groups.base-packages]\n",
        '[component-groups.base-packages]\ncomponents = "promoted"\n',
        '[component-groups.base-packages]\ncomponents = ["promoted", 42]\n',
    ],
)
def test_invalid_committed_channel_config_fails(base_ref: str, tmp_path: Path, config: str) -> None:
    """Unreadable membership is an error, not an empty list of additions."""
    Path(guard.PUBLISH_CHANNELS_PATH).write_text(config, encoding="utf-8")
    _git("add", guard.PUBLISH_CHANNELS_PATH)
    _git("commit", "-m", "test: invalidate channel config")
    with pytest.raises(ValueError, match=r"Expected|components"):
        guard.check_base_promotions(base_ref, "HEAD", _changes(tmp_path, []))


def test_cli_failure_reports_missing_components_and_returns_nonzero(base_ref: str, tmp_path: Path) -> None:
    """The executable must fail CI with an actionable diagnostic."""
    head = _commit_members(["existing", "promoted"])
    result = subprocess.run(
        [
            sys.executable,
            guard.__file__,
            "--from-commit",
            base_ref,
            "--to-commit",
            head,
            "--changed-components-file",
            str(_changes(tmp_path, [])),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1, "routing-only promotion should fail CI"
    assert "azldev comp update -p promoted --bump" in result.stderr, "diagnostic should prescribe the bump"
    assert 'release.calculation = "manual"' in result.stderr, "manual releases also need explicit advancement"
