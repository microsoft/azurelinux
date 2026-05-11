# SPDX-License-Identifier: MIT
"""Loader for the Standard Azure Linux Repo Layout JSON.

The fixed channel x kind x arch matrix that defines a published
Azure Linux RPM tree (the layout consumed by ``dnf-with-azl-repos``,
``synthesize-repodata.py``, and the ``--repo-prefix`` mode of this
test suite) is encoded once at ``base/packages/repo-layout.json`` and
described by the companion ``base/packages/repo-layout.schema.json``.

This loader reads the JSON and runs a small structural-validation
pass so a malformed file fails at load time with a clear message
rather than producing mysterious downstream errors. We intentionally
do NOT pull in :mod:`jsonschema` here -- the layout JSON is also
consumed by scripts that should run from a plain Python environment
without the test suite's dependencies installed, and the schema is
small enough that the ~30 lines of hand-rolled checks below carry
their weight. The companion ``.schema.json`` is the canonical
reference for editor IntelliSense and humans.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

# ``base/packages/repo-layout.json`` resolved relative to this file:
#   utils -> tests -> packages -> repo-layout.json
LAYOUT_JSON_PATH = (
    Path(__file__).resolve().parent.parent.parent / "repo-layout.json"
)

ALLOWED_KINDS = frozenset({"binary", "debuginfo", "srpm"})


@dataclass(frozen=True)
class SubrepoSpec:
    """One sub-repo in the standard layout."""

    name: str           # stable short identifier (e.g. "base", "sdk-srpms")
    channel: str        # channel name (must appear in RepoLayoutSpec.channels)
    kind: str           # "binary" | "debuginfo" | "srpm"
    per_arch: bool      # whether subpath contains $basearch
    subpath: str        # path under the prefix; contains $basearch iff per_arch


@dataclass(frozen=True)
class RepoLayoutSpec:
    """The full layout description loaded from JSON."""

    version: int
    channels: tuple[str, ...]
    subrepos: tuple[SubrepoSpec, ...]


class RepoLayoutError(ValueError):
    """Raised when the layout JSON is missing or structurally invalid."""


def _bad(msg: str, *, path: Path) -> RepoLayoutError:
    return RepoLayoutError(f"{path}: {msg}")


def _check_subrepo(
    d: object, idx: int, channels: Iterable[str], path: Path,
) -> SubrepoSpec:
    if not isinstance(d, dict):
        raise _bad(
            f"subrepos[{idx}] must be an object, got {type(d).__name__}",
            path=path,
        )
    required = {"name", "channel", "kind", "per_arch", "subpath"}
    extra = set(d) - required
    if extra:
        raise _bad(
            f"subrepos[{idx}]: unexpected key(s) {sorted(extra)}", path=path,
        )
    missing = required - set(d)
    if missing:
        raise _bad(
            f"subrepos[{idx}]: missing key(s) {sorted(missing)}", path=path,
        )
    if d["kind"] not in ALLOWED_KINDS:
        raise _bad(
            f"subrepos[{idx}]: kind {d['kind']!r} not in "
            f"{sorted(ALLOWED_KINDS)}",
            path=path,
        )
    if d["channel"] not in channels:
        raise _bad(
            f"subrepos[{idx}]: channel {d['channel']!r} not in "
            f"{sorted(channels)}",
            path=path,
        )
    if not isinstance(d["per_arch"], bool):
        raise _bad(
            f"subrepos[{idx}]: per_arch must be a boolean", path=path,
        )
    if not isinstance(d["subpath"], str) or not d["subpath"]:
        raise _bad(
            f"subrepos[{idx}]: subpath must be a non-empty string", path=path,
        )
    if d["per_arch"] and "$basearch" not in d["subpath"]:
        raise _bad(
            f"subrepos[{idx}]: per_arch=true but subpath {d['subpath']!r} "
            f"contains no $basearch placeholder",
            path=path,
        )
    if not d["per_arch"] and "$basearch" in d["subpath"]:
        raise _bad(
            f"subrepos[{idx}]: per_arch=false but subpath {d['subpath']!r} "
            f"contains a $basearch placeholder",
            path=path,
        )
    return SubrepoSpec(
        name=d["name"], channel=d["channel"], kind=d["kind"],
        per_arch=d["per_arch"], subpath=d["subpath"],
    )


def load_repo_layout(path: Path | None = None) -> RepoLayoutSpec:
    """Load, validate, and return the repo layout from JSON.

    *path* defaults to the canonical location at
    ``base/packages/repo-layout.json``.
    """
    src = path or LAYOUT_JSON_PATH
    try:
        text = src.read_text()
    except FileNotFoundError as exc:
        raise RepoLayoutError(f"layout file not found at {src}") from exc
    try:
        raw = json.loads(text)
    except json.JSONDecodeError as exc:
        raise _bad(f"invalid JSON: {exc}", path=src) from exc
    if not isinstance(raw, dict):
        raise _bad(
            f"top level must be an object, got {type(raw).__name__}", path=src,
        )

    version = raw.get("version")
    if version != 1:
        raise _bad(
            f"unsupported version {version!r}; this loader understands "
            f"version 1",
            path=src,
        )

    channels = raw.get("channels")
    if not isinstance(channels, list) or not all(
        isinstance(c, str) and c for c in channels
    ):
        raise _bad(
            "channels must be a non-empty array of non-empty strings",
            path=src,
        )
    if len(channels) != len(set(channels)):
        raise _bad("channels has duplicate entries", path=src)

    subrepos_raw = raw.get("subrepos")
    if not isinstance(subrepos_raw, list) or not subrepos_raw:
        raise _bad("subrepos must be a non-empty array", path=src)
    subrepos = tuple(
        _check_subrepo(d, i, channels, src)
        for i, d in enumerate(subrepos_raw)
    )

    seen_names = [s.name for s in subrepos]
    dupes = sorted({n for n in seen_names if seen_names.count(n) > 1})
    if dupes:
        raise _bad(f"subrepo names not unique: {dupes}", path=src)

    return RepoLayoutSpec(
        version=version, channels=tuple(channels), subrepos=subrepos,
    )
