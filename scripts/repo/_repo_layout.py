# SPDX-License-Identifier: MIT
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

    name: str           # stable short identifier (e.g. "base", "sdk-srpms")
    channel: str        # one of CHANNELS
    kind: str           # one of ALL_KINDS
    per_arch: bool      # True iff `subpath` contains $basearch
    subpath: str        # path under a layout prefix


SUBREPOS: tuple[SubrepoSpec, ...] = (
    SubrepoSpec("base",           "base", KIND_MAIN,      True,  "base/$basearch"),
    SubrepoSpec("base-debuginfo", "base", KIND_DEBUGINFO, True,  "base/debuginfo/$basearch"),
    SubrepoSpec("base-srpms",     "base", KIND_SRPMS,     False, "base/srpms"),
    SubrepoSpec("sdk",            "sdk",  KIND_MAIN,      True,  "sdk/$basearch"),
    SubrepoSpec("sdk-debuginfo",  "sdk",  KIND_DEBUGINFO, True,  "sdk/debuginfo/$basearch"),
    SubrepoSpec("sdk-srpms",      "sdk",  KIND_SRPMS,     False, "sdk/srpms"),
)


# A handful of light invariants asserted at import time. These can
# never fire with the constant above unmodified, but they guard
# against typos in any future edit.
assert all(s.channel in CHANNELS for s in SUBREPOS)
assert all(s.kind in ALL_KINDS for s in SUBREPOS)
assert all(s.per_arch == ("$basearch" in s.subpath) for s in SUBREPOS)
assert len({s.name for s in SUBREPOS}) == len(SUBREPOS)
