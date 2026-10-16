# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Standard Azure Linux Repo Layout.

Defines the fixed `channel x kind x arch` matrix that every published
Azure Linux RPM tree follows. Both ``dnf-with-azl-repos`` (which
discovers the layout under one or more URL prefixes) and
``synthesize-repodata.py`` (which writes the layout from upstream
inputs) consume :data:`SUBREPOS` directly.

The matrix has six rows that have not changed for years; encoding it
as a Python constant keeps the consumers trivial and avoids a JSON
loader / validator layer that has to be kept in sync with the data.
"""

from __future__ import annotations

from dataclasses import dataclass

CHANNELS: tuple[str, ...] = ("base", "sdk")

KIND_MAIN = "main"
KIND_DEBUGINFO = "debuginfo"
KIND_SRPMS = "srpms"
ALL_KINDS: tuple[str, ...] = (KIND_MAIN, KIND_DEBUGINFO, KIND_SRPMS)


@dataclass(frozen=True)
class SubrepoSpec:
    """One sub-repo in the standard layout."""

    name: str  # stable short identifier (e.g. "base", "sdk-srpms")
    channel: str  # one of CHANNELS
    kind: str  # one of ALL_KINDS
    per_arch: bool  # True iff `subpath` contains $basearch
    subpath: str  # path under a layout prefix


SUBREPOS: tuple[SubrepoSpec, ...] = (
    SubrepoSpec(name="base", channel="base", kind=KIND_MAIN, per_arch=True, subpath="base/$basearch"),
    SubrepoSpec(
        name="base-debuginfo",
        channel="base",
        kind=KIND_DEBUGINFO,
        per_arch=True,
        subpath="base/debuginfo/$basearch",
    ),
    SubrepoSpec(name="base-srpms", channel="base", kind=KIND_SRPMS, per_arch=False, subpath="base/srpms"),
    SubrepoSpec(name="sdk", channel="sdk", kind=KIND_MAIN, per_arch=True, subpath="sdk/$basearch"),
    SubrepoSpec(
        name="sdk-debuginfo",
        channel="sdk",
        kind=KIND_DEBUGINFO,
        per_arch=True,
        subpath="sdk/debuginfo/$basearch",
    ),
    SubrepoSpec(name="sdk-srpms", channel="sdk", kind=KIND_SRPMS, per_arch=False, subpath="sdk/srpms"),
)


# Validate the fixed table at import time so future edits fail immediately,
# including when Python runs with assertions disabled.
if not all(s.channel in CHANNELS for s in SUBREPOS):
    raise ValueError("SUBREPOS contains an unsupported channel")
if not all(s.kind in ALL_KINDS for s in SUBREPOS):
    raise ValueError("SUBREPOS contains an unsupported kind")
if not all(s.per_arch == ("$basearch" in s.subpath) for s in SUBREPOS):
    raise ValueError("SUBREPOS contains inconsistent architecture paths")
if len({s.name for s in SUBREPOS}) != len(SUBREPOS):
    raise ValueError("SUBREPOS contains duplicate names")
