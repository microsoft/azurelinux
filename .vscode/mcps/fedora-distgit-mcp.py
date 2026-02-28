#!/usr/bin/env python3
"""
Fedora Dist-Git MCP Server — exposes tools for querying Fedora's package
repositories via the Pagure API and performing git-level searches (pickaxe,
grep) on cloned repos.

All fetched content and cloned repos are stored under a gitignored scratch
directory to avoid bloating LLM context. Agents use read_file / grep_search
on the resulting files.

Repo caching: clones are kept between calls so repeated queries on the same
package don't re-clone. A configurable limit (default 5) caps the number of
cached repos. When the limit is reached, the oldest repo is evicted
automatically if auto_clean=True was passed, otherwise a warning is returned.

Dist-git repos are tiny (spec + patches, tarballs live in lookaside), so
regular (non-bare) clones are used. This means the agent's built-in file
tools (read_file, grep_search, semantic_search) work directly on the
checked-out tree, and git read-only operations (log, diff, blame) are
auto-approved.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from _mcp_utils import (
    FastMCP,
    StatusDict,
    check_ssrf,
    load_env,
    validate_base_url,
    validate_package_name,
    write_output,
)

mcp = FastMCP("fedora-distgit")

# Load .env config — may set AZLDEV_WORK_DIR etc.
load_env()

_DEFAULT_BASE_URL = "https://src.fedoraproject.org"
_base_url: str = _DEFAULT_BASE_URL

_scratch_dir: str = os.path.join(
    os.environ.get("AZLDEV_WORK_DIR", "base/build/work"), "scratch", "distgit"
)
_repos_dir: str = os.path.join(_scratch_dir, "repos")
_fetch_dir: str = os.path.join(_scratch_dir, "fetched")

# Maximum number of cached repos before eviction kicks in
_MAX_CACHED_REPOS = 5


def _add_status(result: StatusDict, *, full: bool) -> StatusDict:
    """Append server state to a tool result."""
    status: StatusDict = {
        "default_base_url": _base_url,
        "scratch_dir": _scratch_dir,
    }
    if full:
        repos = _cached_repos()
        status["cached_repos"] = [os.path.relpath(r, _repos_dir) for r, _ in repos]
    return result | status


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _repo_path(package: str, base_url: str) -> str:
    """Return the on-disk path for a cached clone, namespaced by origin host."""
    hostname = urlparse(base_url).hostname or "unknown"
    return os.path.join(_repos_dir, hostname, package)


def _git_dir(package: str, base_url: str) -> str:
    """Return the .git directory for a cached clone."""
    return os.path.join(_repo_path(package, base_url), ".git")


def _touch_repo(repo_dir: str) -> None:
    """Update the mtime of a repo dir to track LRU."""
    os.utime(repo_dir)


def _cached_repos() -> list[tuple[str, float]]:
    """Return list of (repo_dir, mtime) sorted oldest-first.

    Scans ``_repos_dir/<hostname>/<package>`` (current layout) and also
    ``_repos_dir/<package>`` (legacy layout before host-namespacing) so
    old caches are still visible for eviction and cleanup.
    """
    if not os.path.isdir(_repos_dir):
        return []
    repos: list[tuple[str, float]] = []
    for entry in os.scandir(_repos_dir):
        if not entry.is_dir():
            continue
        # Legacy layout: _repos_dir/<package>/.git
        if os.path.isdir(os.path.join(entry.path, ".git")):
            repos.append((entry.path, entry.stat().st_mtime))
        else:
            # Current layout: _repos_dir/<hostname>/<package>/.git
            for sub in os.scandir(entry.path):
                if sub.is_dir() and os.path.isdir(os.path.join(sub.path, ".git")):
                    repos.append((sub.path, sub.stat().st_mtime))
    repos.sort(key=lambda x: x[1])
    return repos


def _evict_if_needed(auto_clean: bool) -> str | None:
    """Evict oldest repo(s) if cache is at capacity.

    Returns None on success, or a warning string if eviction is needed
    but auto_clean is False.
    """
    repos = _cached_repos()
    if len(repos) < _MAX_CACHED_REPOS:
        return None

    if not auto_clean:
        names = [os.path.basename(r) for r, _ in repos]
        return (
            f"WARNING: Repo cache is full ({len(repos)}/{_MAX_CACHED_REPOS}). "
            f"Cached repos: {', '.join(names)}. "
            "Call distgit_cleanup to free space, or re-run with auto_clean=true "
            "to automatically remove the oldest repo."
        )

    # Remove oldest repos until we're one under the limit (to make room)
    to_remove = len(repos) - _MAX_CACHED_REPOS + 1
    for repo_dir, _ in repos[:to_remove]:
        shutil.rmtree(repo_dir, ignore_errors=True)
    return None


def _ensure_repo(package: str, auto_clean: bool, base_url: str) -> tuple[str, str | None]:
    """Ensure a clone exists for `package`. Returns (repo_dir, error_or_None)."""
    name_err = validate_package_name(package)
    if name_err:
        return "", name_err

    repo_dir = _repo_path(package, base_url)

    if os.path.isdir(os.path.join(repo_dir, ".git")):
        _touch_repo(repo_dir)
        # Fetch latest refs (best-effort)
        try:
            subprocess.run(
                ["git", "fetch", "--quiet", "--all"],
                cwd=repo_dir,
                capture_output=True,
                timeout=60,
            )
        except Exception:
            pass
        return repo_dir, None

    # Check cache capacity before cloning
    warn = _evict_if_needed(auto_clean)
    if warn:
        return "", warn

    os.makedirs(os.path.dirname(repo_dir), exist_ok=True)
    clone_url = f"{base_url}/rpms/{package}.git"
    try:
        result = subprocess.run(
            ["git", "clone", "--quiet", clone_url, repo_dir],
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        shutil.rmtree(repo_dir, ignore_errors=True)
        return "", f"Clone of {clone_url} timed out after 120s."
    except FileNotFoundError:
        return "", "git is not installed or not in PATH."

    if result.returncode != 0:
        shutil.rmtree(repo_dir, ignore_errors=True)
        stderr = result.stderr.strip()
        return "", f"git clone failed (exit {result.returncode}): {stderr}"

    _touch_repo(repo_dir)
    return repo_dir, None


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def distgit_status() -> StatusDict:
    """Return current MCP server state.

    Returns the configured base URL, scratch directory, and cached repos.
    """
    return _add_status({}, full=True)


@mcp.tool()
def set_distgit_url(base_url: str) -> StatusDict:
    """Set the Fedora dist-git base URL.

    Defaults to https://src.fedoraproject.org. Only needs to be called if
    using a mirror or alternate instance."""
    global _base_url
    old_url = _base_url
    normalized, err = validate_base_url(base_url)
    if err:
        return _add_status({"error": err}, full=False)
    _base_url = normalized
    return _add_status({"old_url": old_url}, full=False)


@mcp.tool()
def distgit_fetch(path: str, override_base_url: str | None = None) -> StatusDict:
    """Fetch a page from Fedora dist-git (Pagure API or raw file).

    `path` is appended to the base URL. The base URL is resolved as:
    `override_base_url` if provided, otherwise the default set via
    set_distgit_url. At least one must be available.
    Examples of `path`:
      - /api/0/rpms/atlas              (package metadata)
      - /api/0/rpms/atlas/git/branches (list branches)
      - /rpms/atlas/raw/rawhide/f/atlas.spec  (raw spec file)

    Response is written to a temp file. Use read_file or grep_search to inspect."""
    if override_base_url:
        base, err = validate_base_url(override_base_url)
        if err:
            return _add_status({"error": err}, full=False)
    else:
        base = _base_url

    if not path.startswith("/"):
        return _add_status({"error": "path must start with '/'"}, full=False)

    url = base + path

    # Guard against SSRF via URL authority tricks
    ssrf_err = check_ssrf(base, url)
    if ssrf_err:
        return _add_status({"error": ssrf_err}, full=False)

    req = urllib.request.Request(url, headers={"User-Agent": "fedora-distgit-mcp/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        return _add_status({"error": f"HTTP {e.code} fetching {url}: {e.reason}"}, full=False)
    except urllib.error.URLError as e:
        return _add_status({"error": f"can't fetch {url}: {e.reason}"}, full=False)
    except Exception as e:
        return _add_status({"error": f"can't fetch {url}: {e}"}, full=False)

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("latin-1")

    # Pretty-print JSON responses for readability
    try:
        parsed = json.loads(text)
        text = json.dumps(parsed, indent=2)
    except (json.JSONDecodeError, ValueError):
        pass

    output = write_output(text, output_dir=_fetch_dir, prefix="distgit_")
    return _add_status({"output": output}, full=False)


@mcp.tool()
def distgit_search(
    package: str,
    query: str,
    ref: str = "rawhide",
    mode: str = "pickaxe",
    auto_clean: bool = False,
    override_base_url: str | None = None,
) -> StatusDict:
    """Search a Fedora package's git history or content.

    Clones (or reuses a cached clone of) the package's dist-git repo,
    then runs the requested search.

    Args:
        package: Fedora package name (e.g. "atlas", "lapack")
        query: The search string
        ref: Git ref to search (default "rawhide"). Use "--all" for all refs
            (pickaxe and log-grep modes only; grep requires a single ref).
        mode: Search mode — one of:
            - "pickaxe": git log -S (find commits that add/remove `query`)
            - "grep": git grep (find `query` in current tree at `ref`)
            - "log-grep": git log --grep (find commits whose message contains `query`)
        auto_clean: If true, automatically evict the oldest cached repo when
            the cache is full. If false (default), return a warning instead.
        override_base_url: If provided, clone from this dist-git instance
            instead of the default. Clones are cached per-host so different
            instances don't collide.

    Results are written to a temp file. Use read_file or grep_search to inspect.
    """
    if override_base_url:
        base, err = validate_base_url(override_base_url)
        if err:
            return _add_status({"error": err}, full=False)
    else:
        base = _base_url

    valid_modes = ("pickaxe", "grep", "log-grep")
    if mode not in valid_modes:
        return _add_status({"error": f"mode must be one of {valid_modes}, got {mode!r}"}, full=False)
    if not query:
        return _add_status({"error": "query must not be empty."}, full=False)
    if ref != "--all" and ref.startswith("-"):
        return _add_status(
            {"error": f"ref must not start with '-' (got {ref!r}). Use a branch name like 'rawhide'."},
            full=False,
        )

    repo_dir, err = _ensure_repo(package, auto_clean, base)
    if err:
        return _add_status({"error": err}, full=False)

    git_dir = _git_dir(package, base)

    # Build the git command
    if mode == "pickaxe":
        ref_args = ["--all"] if ref == "--all" else [ref]
        cmd = [
            "git", "--git-dir", git_dir, "log",
            "--oneline", "-20",
            f"-S{query}",
            *ref_args,
            "--",
        ]
    elif mode == "grep":
        if ref == "--all":
            return _add_status(
                {"error": "--all is not supported for grep mode; specify a single ref (e.g. 'rawhide')."},
                full=False,
            )
        cmd = [
            "git", "--git-dir", git_dir, "grep",
            "-n", "-i", "-e", query, ref, "--",
        ]
    elif mode == "log-grep":
        ref_args = ["--all"] if ref == "--all" else [ref]
        cmd = [
            "git", "--git-dir", git_dir, "log",
            "--oneline", "-20",
            f"--grep={query}",
            *ref_args,
        ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        return _add_status({"error": "Search timed out after 30s."}, full=False)
    except Exception as e:
        return _add_status({"error": f"running git: {e}"}, full=False)

    output = result.stdout
    if result.returncode != 0 and not output:
        # git grep returns 1 for "no match" — that's expected
        if mode == "grep" and result.returncode == 1:
            return _add_status(
                {"output": f"No matches found for {query!r} in {package} at {ref}."},
                full=False,
            )
        stderr = result.stderr.strip()
        return _add_status({"error": f"git exited with {result.returncode}: {stderr}"}, full=False)

    if not output.strip():
        return _add_status(
            {"output": f"No matches found for {query!r} in {package} ({mode} on {ref}).", "repo_dir": repo_dir},
            full=False,
        )

    lines = output.count("\n")
    written = write_output(
        output,
        output_dir=_fetch_dir,
        prefix=f"distgit_{package}_{mode}_",
        extra_msg=f"Found {lines} result(s). Repo cloned at: {repo_dir}",
    )
    return _add_status({"output": written, "repo_dir": repo_dir}, full=False)


@mcp.tool()
def distgit_show(
    package: str,
    commit: str,
    auto_clean: bool = False,
    override_base_url: str | None = None,
) -> StatusDict:
    """Show a specific commit from a Fedora package's dist-git repo.

    Clones (or reuses cache) and runs `git show <commit>`. Output is
    written to a temp file.

    Args:
        package: Fedora package name (e.g. "atlas")
        commit: Commit hash (full or abbreviated)
        auto_clean: Auto-evict oldest cached repo if cache is full.
        override_base_url: If provided, clone from this dist-git instance
            instead of the default.
    """
    if override_base_url:
        base, err = validate_base_url(override_base_url)
        if err:
            return _add_status({"error": err}, full=False)
    else:
        base = _base_url

    # Validate commit is a hex SHA (prevents argument injection when commit
    # appears before "--" in the arg list)
    if not re.match(r"^[a-fA-F0-9]{4,40}$", commit):
        return _add_status({"error": "commit must be a hex SHA hash (4-40 chars)."}, full=False)

    repo_dir, err = _ensure_repo(package, auto_clean, base)
    if err:
        return _add_status({"error": err}, full=False)

    git_dir = _git_dir(package, base)

    try:
        result = subprocess.run(
            ["git", "--git-dir", git_dir, "show", "--stat", "--patch", commit, "--"],
            capture_output=True, text=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        return _add_status({"error": "git show timed out after 30s."}, full=False)
    except Exception as e:
        return _add_status({"error": f"running git: {e}"}, full=False)

    if result.returncode != 0:
        stderr = result.stderr.strip()
        return _add_status({"error": f"git show failed (exit {result.returncode}): {stderr}"}, full=False)

    output = result.stdout

    written = write_output(
        output,
        output_dir=_fetch_dir,
        prefix=f"distgit_{package}_show_",
        extra_msg=f"Repo cloned at: {repo_dir}",
    )
    return _add_status({"output": written, "repo_dir": repo_dir}, full=False)


@mcp.tool()
def distgit_cleanup(remove_repos: bool = True) -> StatusDict:
    """Remove fetched temp files and (optionally) cached repos.

    Args:
        remove_repos: If true (default), also remove all cached git repos.
            Set to false to only clean fetched files while preserving clones.
    """
    removed_files = 0
    removed_bytes = 0

    # Clean fetched files
    if os.path.isdir(_fetch_dir):
        for entry in os.scandir(_fetch_dir):
            if entry.is_file():
                removed_bytes += entry.stat().st_size
                Path(entry.path).unlink()
                removed_files += 1

    # Clean repos
    removed_repos_count = 0
    if remove_repos and os.path.isdir(_repos_dir):
        # Count actual repos (hostname/package) before bulk-removing the tree.
        removed_repos_count = len(_cached_repos())
        for entry in os.scandir(_repos_dir):
            if entry.is_dir():
                shutil.rmtree(entry.path, ignore_errors=True)

    return _add_status(
        {
            "files_removed": removed_files,
            "bytes_reclaimed": removed_bytes,
            "repos_removed": removed_repos_count,
        },
        full=False,
    )


if __name__ == "__main__":
    mcp.run()
