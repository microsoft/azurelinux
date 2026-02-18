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
import ssl
import tempfile
import urllib.error
import urllib.request
from typing import Optional
from urllib.parse import urlparse

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

_base_url: Optional[str] = None
_allow_insecure: bool = False
_ssl_error_seen_for: Optional[str] = None
_output_dir: str = os.path.join(
    os.environ.get("AZLDEV_WORK_DIR", "base/build/work"), "scratch", "koji"
)


@mcp.tool()
def set_koji_url(base_url: str) -> str:
    """Set the Koji Web UI base URL (e.g. https://koji.example.com).
    Must be called before using koji_fetch.

    SSL certificate verification is enabled by default. If the Koji server
    uses self-signed certificates, use the separate koji_allow_insecure tool
    to disable verification after confirming with the user."""
    global _base_url, _allow_insecure, _ssl_error_seen_for
    normalized = base_url.rstrip("/")

    # Reset insecure flag if the URL changed
    if normalized != _base_url:
        _allow_insecure = False
        _ssl_error_seen_for = None

    _base_url = normalized
    return f"Koji base URL set to {_base_url}"


@mcp.tool()
def koji_allow_insecure() -> str:
    """Disable SSL certificate verification for the configured Koji URL.

    This is a SEPARATE tool so the user explicitly approves skipping SSL
    verification. It can only be called after:
      1. A Koji base URL has been set via set_koji_url.
      2. A prior koji_fetch call has failed with an SSL certificate error.

    DO NOT call this tool without first confirming with the user that they
    want to allow insecure connections."""
    global _allow_insecure

    if not _base_url:
        return "ERROR: No Koji URL set. Call set_koji_url first."

    if _ssl_error_seen_for != _base_url:
        return (
            "ERROR: Cannot enable insecure mode — no SSL error has been "
            "observed for the current URL yet. Call koji_fetch first; if it "
            "fails with a certificate error, then call this tool."
        )

    _allow_insecure = True
    return f"SSL verification DISABLED for {_base_url}"


@mcp.tool()
def koji_fetch(path: str) -> str:
    """Fetch a page or log from Koji.

    `path` is appended to the base URL. Examples:
      - /koji/taskinfo?taskID=3307
      - /koji/getfile?taskID=6059&volume=DEFAULT&name=build.log&offset=-4000

    `offset` is optional. The tool can easily handle large files and write them to disk, and agents can then use
    read_file or grep_search, shell(tail), shell(head), shell(grep) etc. to inspect specific parts.
    """
    global _ssl_error_seen_for

    if not _base_url:
        return "ERROR: Koji base URL not set. Call set_koji_url first."

    url = _base_url + path

    # Guard against SSRF via URL authority tricks (e.g. path="@evil.com/..." or ":8080/...")
    parsed_base = urlparse(_base_url)
    parsed_url = urlparse(url)

    def _effective_port(parsed):
        """Return the effective port for a parsed URL (explicit or scheme default)."""
        if parsed.port is not None:
            return parsed.port
        if parsed.scheme == "http":
            return 80
        if parsed.scheme == "https":
            return 443
        return None

    base_port = _effective_port(parsed_base)
    url_port = _effective_port(parsed_url)

    if (
        parsed_url.hostname != parsed_base.hostname
        or parsed_url.scheme != parsed_base.scheme
        or url_port != base_port
    ):
        return (
            "ERROR: Constructed URL does not match the configured Koji endpoint "
            f"(scheme/host/port mismatch: {parsed_url.scheme!r}://{parsed_url.hostname!r}:{url_port!r} "
            f"!= {parsed_base.scheme!r}://{parsed_base.hostname!r}:{base_port!r}). Aborting."
        )

    # SSL: verify certs by default, only disable if the user explicitly opted in
    ssl_ctx = None
    if parsed_url.scheme == "https" and _allow_insecure:
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
            _ssl_error_seen_for = _base_url
            return (
                f"ERROR: SSL certificate verification failed for {url}: {e.reason}\n\n"
                "The server **may** be using a self-signed certificate (don't assume — it could be a misconfiguration or an attack). "
                "You **MUST** inform the user about the security implications of allowing insecure connections, then"
                "offer the user a selecton of two options: proceed or abort (use 'ask_questions' tool if available, with 'no' as the default answer). "
                "If the user chooses to proceed, call the koji_allow_insecure tool. "
                "DO NOT proceed without explicit user approval for the SPECIFIC URL."
            )
        return (
            f"ERROR fetching {url}: {e}\n\n"
            "NOTE: Koji is typically only accessible via a secure connection "
            "(e.g., VPN or corporate network). If you are seeing connection "
            "errors or timeouts, please verify that you are connected to the "
            "appropriate network before retrying."
        )
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
    fd, out_path = tempfile.mkstemp(prefix="koji_", dir=_output_dir)
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
