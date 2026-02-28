#!/usr/bin/env python3
"""Koji MCP Server.

Exposes tools for setting a Koji base URL and fetching pages/logs relative
to it.  Designed for the build-triage agent.

All fetched content is written to temp files under a gitignored build
directory to avoid bloating LLM context.  The agent can then use read_file
or grep_search to inspect the relevant parts.

This MCP is intentionally rudimentary and is focused primarily on
simplifying the permission control.  Normally a user would have to accept
every call to ``curl`` etc. from the agent, and accept file writes.  This
MCP allows the user to accept the tools once, and then the agent can fetch
as many pages/logs as needed without bothering the user again.
"""

from __future__ import annotations

import os
import ssl
import sys
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
    write_output,
)

mcp = FastMCP("koji")

# Load .env config — may set KOJI_BASE_URL and KOJI_INSECURE_URLS
load_env()

_base_url: str | None = None
_ssl_errors_seen: set[str] = set()
_output_dir = Path(os.environ.get("AZLDEV_WORK_DIR", "base/build/work"), "scratch", "koji")

# URLs allowed to skip SSL verification — seeded from .env, extended at
# runtime via koji_allow_insecure.
_insecure_urls: set[str] = set()
for _raw_url in os.environ.get("KOJI_INSECURE_URLS", "").split(","):
    _raw_url = _raw_url.strip()
    if _raw_url:
        _normalized, _err = validate_base_url(_raw_url)
        if not _err:
            _insecure_urls.add(_normalized)

# Auto-set base URL from env
if os.environ.get("KOJI_BASE_URL"):
    _normalized, _err = validate_base_url(os.environ["KOJI_BASE_URL"])
    if not _err:
        _base_url = _normalized

# Log startup config
if _base_url:
    _flags = []
    if _base_url in _insecure_urls:
        _flags.append("insecure=yes")
    print(f"[koji-mcp] Base URL: {_base_url}" + (f" ({', '.join(_flags)})" if _flags else ""), file=sys.stderr)
if _insecure_urls:
    print(f"[koji-mcp] Pre-approved insecure URLs: {', '.join(sorted(_insecure_urls))}", file=sys.stderr)


def _add_status(result: StatusDict, *, full: bool) -> StatusDict:
    """Build a snapshot of the MCP server's current state."""
    status = {
        "default_base_url": _base_url,
        "output_dir": str(_output_dir),
    }
    if full:
        cached_files = 0
        if _output_dir.is_dir():
            for entry in os.scandir(_output_dir):
                if entry.is_file():
                    cached_files += 1
        status["insecure_urls"] = sorted(_insecure_urls)
        status["ssl_errors_seen"] = sorted(_ssl_errors_seen)
        status["cached_files"] = cached_files

    return result | status


@mcp.tool()
def koji_status() -> StatusDict:
    """Return current MCP server state.

    This returns a snapshot of the current state of the MCP server, including
    the URL configuration.
    """
    return _add_status({}, full=True)


@mcp.tool()
def set_koji_url(base_url: str) -> StatusDict:
    """Set the default Koji Web UI base URL.

    Set the default Koji Web UI base URL (e.g. https://koji.example.com).
    This is optional — you can also pass `override_base_url` directly to each
    tool. Setting a default is convenient when all requests target the same
    Koji instance. The user may have pre-configured this via the
    KOJI_BASE_URL environment variable, but the tool will still
    allow resetting it at runtime.
    """
    global _base_url
    old_url = _base_url
    normalized, err = validate_base_url(base_url)
    if err:
        return _add_status({"error": err}, full=False)

    _base_url = normalized

    return _add_status({"old_url": old_url}, full=False)


@mcp.tool()
def koji_allow_insecure(override_base_url: str | None = None) -> StatusDict:
    """Disable SSL certificate verification for a Koji URL.

    Disable SSL certificate verification for a Koji URL. The allow insecure tool is intentionally separate from the
    fetch tool to ensure that the user can explicitly approve skipping SSL verification for a specific URL. This tool
    can only be called after a prior koji_fetch call has failed with an SSL certificate error for that URL.

    DO NOT call this tool without first confirming with the user that they want to allow insecure connections, and
    that they understand the security implications.
    """
    if override_base_url:
        url, err = validate_base_url(override_base_url)
        if err:
            return _add_status({"error": err}, full=False)
    else:
        url = _base_url

    if not url:
        return _add_status(
            {"error": "No Koji URL available. Pass override_base_url or call set_koji_url first."}, full=False
        )

    if url not in _ssl_errors_seen:
        return _add_status(
            {
                "error": (
                    "Cannot enable insecure mode — no SSL error has been "
                    f"observed for {url}. Call koji_fetch first; if it "
                    "fails with a certificate error, then call this tool."
                )
            },
            full=False,
        )

    _insecure_urls.add(url)
    return _add_status({"allowed_url": url}, full=True)


@mcp.tool()
def koji_fetch(path: str, override_base_url: str | None = None) -> StatusDict:
    """Fetch a page or log from Koji.

    `path` is appended to the base URL. The base URL is resolved as: `override_base_url` if provided, otherwise the
    default set via set_koji_url. At least one must be available.
    Examples of `path`:
    - /koji/taskinfo?taskID=3307
    - /koji/getfile?taskID=6059&volume=DEFAULT&name=build.log&offset=-4000

    The tool will automatically handle large files by writing them to disk.
    Agents can then use read_file, grep_search, shell(tail), shell(head), shell(grep) etc. to inspect specific parts
    without bloating the LLM context.
    """
    if override_base_url:
        base, err = validate_base_url(override_base_url)
        if err:
            return _add_status({"error": err}, full=False)
    else:
        base = _base_url

    if not base:
        return _add_status(
            {"error": "No Koji URL available. Pass override_base_url or call set_koji_url first."}, full=False
        )

    if not path.startswith("/"):
        return _add_status({"error": "path must start with '/'"}, full=False)

    url = base + path

    # Guard against SSRF via URL authority tricks (e.g. path="@evil.com/..." or ":8080/...")
    ssrf_err = check_ssrf(base, url)
    if ssrf_err:
        return _add_status({"error": ssrf_err}, full=False)

    parsed_url = urlparse(url)

    # SSL: verify certs by default, only disable if the user explicitly opted in
    ssl_ctx = None
    if parsed_url.scheme == "https" and base in _insecure_urls:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url, headers={"User-Agent": "koji-mcp/1.0"})
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=10) as resp:
            data = resp.read()
    except urllib.error.URLError as e:
        # urllib wraps SSL errors inside URLError.reason
        if isinstance(e.reason, (ssl.SSLCertVerificationError, ssl.SSLError)):
            _ssl_errors_seen.add(base)
            return _add_status(
                {
                    "error": (
                        f"SSL certificate verification failed for {url}: "
                        f"{e.reason}. "
                        "The server **may** be using a self-signed "
                        "certificate (don't assume — it could be a "
                        "misconfiguration or an attack). "
                        "You **MUST** inform the user about the security "
                        "implications of allowing insecure connections, "
                        "then offer the user a selection of two options: "
                        "proceed or abort (use 'ask_questions/ask_user' "
                        "tools if available, with 'no' as the "
                        "default/first option). "
                        "If the user chooses to proceed, call the "
                        "koji_allow_insecure tool. "
                        "DO NOT proceed without explicit user approval "
                        "for the SPECIFIC URL."
                    )
                },
                full=False,
            )
        return _add_status(
            {
                "error": (
                    f"can't fetch {url}: {e}. "
                    "NOTE: Koji is typically only accessible via a secure connection "
                    "(e.g., VPN or corporate network). If you are seeing connection "
                    "errors or timeouts, please verify that you are connected to the "
                    "appropriate network before retrying."
                )
            },
            full=False,
        )
    except Exception as e:
        return _add_status(
            {
                "error": (
                    f"can't fetch {url}: {e}. "
                    "NOTE: Koji is typically only accessible via a secure connection "
                    "(e.g., VPN or corporate network). If you are seeing connection "
                    "errors or timeouts, please verify that you are connected to the "
                    "appropriate network before retrying."
                )
            },
            full=False,
        )

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("latin-1")

    output = write_output(text, output_dir=_output_dir, prefix="koji_")
    return _add_status({"output": output}, full=False)


@mcp.tool()
def koji_cleanup() -> StatusDict:
    """Remove all fetched Koji temp files from the output directory.

    Call this to reclaim disk space after a triage session, or when
    starting a fresh investigation.
    """
    if not _output_dir.is_dir():
        return _add_status({"files_removed": 0}, full=False)

    count = 0
    total_bytes = 0
    for entry in os.scandir(_output_dir):
        if entry.is_file():
            total_bytes += entry.stat().st_size
            Path(entry.path).unlink()
            count += 1

    return _add_status({"files_removed": count, "bytes_reclaimed": total_bytes}, full=False)


if __name__ == "__main__":
    mcp.run()
