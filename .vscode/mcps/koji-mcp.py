#!/usr/bin/env python3
"""
Koji MCP Server — exposes tools for setting a Koji base URL and fetching
pages/logs relative to it. Designed for the build-triage agent.

All fetched content is written to temp files under a gitignored build
directory to avoid bloating LLM context. The agent can then use read_file
or grep_search to inspect the relevant parts.

This MCP is intentionally rudimentary and is focused primarily on simplifying the permission control.
Normally a user would have to accept every call to `curl` etc. from the agent, and accept file writes.
This MCP allows the user to accept the tools once, and then the agent can fetch as many pages/logs as needed without
bothering the user again.
"""

import os
import re
import ssl
import tempfile
import urllib.request
from urllib.parse import parse_qs, urlparse

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    import sys
    sys.stderr.write("\n" + "=" * 60 + "\n")
    sys.stderr.write("  MISSING DEPENDENCY: 'mcp' package not found\n")
    sys.stderr.write("  Install it with:  pip3 install --user mcp\n")
    sys.stderr.write("=" * 60 + "\n\n")
    sys.exit(1)

mcp = FastMCP("koji")

_base_url: str | None = None
_output_dir: str = os.path.join(
    os.environ.get("AZLDEV_WORK_DIR", "base/build/work"), "scratch", "koji"
)


def _derive_filename(path: str) -> str:
    """Turn a Koji URL path into a human-readable filename.

    /koji/taskinfo?taskID=3307         -> task_3307_info.html
    /koji/getfile?taskID=6059&name=build.log&offset=-4000  -> task_6059_build.log
    """
    parsed = urlparse(path)
    params = parse_qs(parsed.query)
    task_id = params.get("taskID", ["unknown"])[0]

    if "getfile" in parsed.path:
        name = params.get("name", ["output.txt"])[0]
        return f"task_{task_id}_{name}"
    else:
        page = parsed.path.rstrip("/").rsplit("/", 1)[-1] or "page"
        return f"task_{task_id}_{page}.html"


@mcp.tool()
def set_koji_url(base_url: str) -> str:
    """Set the Koji Web UI base URL (e.g. https://koji.example.com).
    Must be called before using koji_fetch."""
    global _base_url
    _base_url = base_url.rstrip("/")
    return f"Koji base URL set to {_base_url}"


@mcp.tool()
def koji_fetch(path: str) -> str:
    """Fetch a page or log from Koji.

    `path` is appended to the base URL. Examples:
      - /koji/taskinfo?taskID=3307
      - /koji/getfile?taskID=6059&volume=DEFAULT&name=build.log&offset=-4000

    `offset` is optional. The tool can easily handle large files and write them to disk, and agents can then use
    read_file or grep_search, shell(tail), shell(head), shell(grep) etc. to inspect specific parts.
    """
    if not _base_url:
        return "ERROR: Koji base URL not set. Call set_koji_url first."

    url = _base_url + path

    # Guard against SSRF via URL authority tricks (e.g. path="@evil.com/...")
    parsed_base = urlparse(_base_url)
    parsed_url = urlparse(url)
    if parsed_url.hostname != parsed_base.hostname:
        return (
            f"ERROR: Constructed URL points to a different host "
            f"({parsed_url.hostname!r} != {parsed_base.hostname!r}). Aborting."
        )

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url, headers={"User-Agent": "koji-mcp/1.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            data = resp.read()
    except Exception as e:
        return (
            f"ERROR fetching {url}: {e}\n\n"
            "NOTE: Koji is typically only accessible via a secure connection "
            "(e.g., VPN or corporate network). If you are seeing connection "
            "errors or timeouts, please verify that you are connected to the "
            "appropriate network before retrying."
        )

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("latin-1")

    # Always write to a temp file to keep context small
    os.makedirs(_output_dir, exist_ok=True)
    base_name = _derive_filename(path)
    # Use mkstemp so parallel fetches never collide
    fd, out_path = tempfile.mkstemp(
        prefix=re.sub(r"[^\w.-]", "_", base_name) + ".",
        suffix="",
        dir=_output_dir,
    )
    with os.fdopen(fd, "w") as f:
        f.write(text)

    size = len(data)
    lines = text.count("\n")
    return f"Wrote {size} bytes ({lines} lines) to {out_path}"


@mcp.tool()
def koji_cleanup() -> str:
    """Remove all fetched Koji temp files from the output directory.

    Call this to reclaim disk space after a triage session, or when
    starting a fresh investigation.
    """
    if not os.path.isdir(_output_dir):
        return "Nothing to clean up — output directory does not exist."

    count = 0
    total_bytes = 0
    for entry in os.scandir(_output_dir):
        if entry.is_file():
            total_bytes += entry.stat().st_size
            os.unlink(entry.path)
            count += 1

    return f"Removed {count} file(s) ({total_bytes} bytes) from {_output_dir}"


if __name__ == "__main__":
    mcp.run()
