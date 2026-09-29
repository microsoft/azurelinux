# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Static shapes for rendered-spec drift reports."""

from __future__ import annotations

from typing import TypedDict


class RenderedFile(TypedDict):
    """A rendered file and its owning component."""

    path: str
    component: str


class ContentDiff(RenderedFile):
    """A rendered file whose committed and generated contents differ."""

    diff: str


class RenderReport(TypedDict):
    """The JSON report shared by the checker and PR comment renderer."""

    content_diffs: list[ContentDiff]
    extra_files: list[RenderedFile]
    missing_files: list[RenderedFile]
