"""Shared utilities for spec review scripts."""

from pathlib import Path
from typing import Optional


def get_repo_relative_path(spec_file: str, repo_root: Optional[Path] = None) -> str:
    """Convert absolute path to repo-relative path.

    Uses repo_root if available; falls back to filename only so that
    GitHub annotations/links still have a chance of matching.
    """
    spec_path = Path(spec_file)

    if not spec_path.is_absolute():
        return spec_file

    if repo_root:
        try:
            return str(spec_path.resolve().relative_to(repo_root.resolve()))
        except ValueError:
            pass

    return spec_path.name
