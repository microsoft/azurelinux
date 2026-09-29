# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Static shapes for raw spec-review JSON consumers."""

from __future__ import annotations

from typing import TypedDict


class RawFinding(TypedDict, total=False):
    """Finding fields consumed by report renderers."""

    description: str
    citation: str | None
    line: int


class RawReview(TypedDict, total=False):
    """Per-spec fields consumed by report renderers."""

    spec_file: str
    errors: list[RawFinding]
    warnings: list[RawFinding]
    suggestions: list[RawFinding]


class RawReport(TypedDict, total=False):
    """Top-level fields consumed from a raw spec-review report."""

    spec_reviews: list[RawReview]
