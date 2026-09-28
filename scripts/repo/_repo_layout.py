# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
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

import urllib.parse
from dataclasses import dataclass

CHANNELS: tuple[str, ...] = ("base", "sdk")

KIND_MAIN = "main"
KIND_DEBUGINFO = "debuginfo"
KIND_SRPMS = "srpms"
ALL_KINDS: tuple[str, ...] = (KIND_MAIN, KIND_DEBUGINFO, KIND_SRPMS)
ALLOWED_REPO_SCHEMES = frozenset({"file", "http", "https"})


class UnsupportedRepoSchemeError(ValueError):
    """Indicate that a repository URL uses a disallowed scheme."""


def validate_repo_url(url: str) -> None:
    """Reject repository URLs whose scheme urllib must not open."""
    scheme = urllib.parse.urlsplit(url).scheme.lower()
    if scheme not in ALLOWED_REPO_SCHEMES:
        allowed = ", ".join(sorted(ALLOWED_REPO_SCHEMES))
        raise UnsupportedRepoSchemeError(
            f"unsupported repository URL scheme {scheme or '<missing>'!r} for {url!r}; expected one of: {allowed}"
        )


@dataclass(frozen=True)
class SubrepoSpec:
    """One sub-repo in the standard layout."""

    name: str  # stable short identifier (e.g. "base", "sdk-srpms")
    channel: str  # one of CHANNELS
    kind: str  # one of ALL_KINDS
    subpath: str  # path under a layout prefix

    @property
    def per_arch(self) -> bool:
        """Return whether this sub-repository has one path per architecture."""
        return "$basearch" in self.subpath


SUBREPOS: tuple[SubrepoSpec, ...] = (
    SubrepoSpec("base", "base", KIND_MAIN, "base/$basearch"),
    SubrepoSpec("base-debuginfo", "base", KIND_DEBUGINFO, "base/debuginfo/$basearch"),
    SubrepoSpec("base-srpms", "base", KIND_SRPMS, "base/srpms"),
    SubrepoSpec("sdk", "sdk", KIND_MAIN, "sdk/$basearch"),
    SubrepoSpec("sdk-debuginfo", "sdk", KIND_DEBUGINFO, "sdk/debuginfo/$basearch"),
    SubrepoSpec("sdk-srpms", "sdk", KIND_SRPMS, "sdk/srpms"),
)


# Validate the fixed table at import time so future edits fail immediately,
# including when Python runs with assertions disabled.
if not all(s.channel in CHANNELS for s in SUBREPOS):
    raise ValueError("SUBREPOS contains an unsupported channel")
if not all(s.kind in ALL_KINDS for s in SUBREPOS):
    raise ValueError("SUBREPOS contains an unsupported kind")
if len({s.name for s in SUBREPOS}) != len(SUBREPOS):
    raise ValueError("SUBREPOS contains duplicate names")
