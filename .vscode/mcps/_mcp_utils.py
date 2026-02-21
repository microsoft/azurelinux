"""
Shared utilities for Azure Linux MCP servers.

Provides common helpers for URL validation, SSRF guards, and output handling
so individual MCP servers stay DRY.
"""

import os
import re
import tempfile
from urllib.parse import urlparse

# If output is at most this many bytes, include it inline in the return
# to save the agent a follow-up read_file call.
INLINE_THRESHOLD_BYTES = 4096

# Valid RPM package name characters: starts with alphanumeric, then
# alphanumerics plus . _ + -
_VALID_PACKAGE_NAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._+-]*$")


def validate_base_url(base_url: str) -> tuple[str, str | None]:
    """Validate and normalize a base URL for an MCP server.

    Returns (normalized_url, error_message_or_None).
    On success, error is None. On failure, normalized_url is empty.
    """
    normalized = base_url.rstrip("/")
    parsed = urlparse(normalized)

    if parsed.scheme not in ("http", "https"):
        return "", f"ERROR: Only http/https URLs are supported (got {parsed.scheme!r})"
    if parsed.username or parsed.password:
        return "", "ERROR: URLs with embedded credentials are not supported"

    return normalized, None


def effective_port(parsed) -> int | None:
    """Return the effective port for a parsed URL (explicit or scheme default)."""
    if parsed.port is not None:
        return parsed.port
    if parsed.scheme == "http":
        return 80
    if parsed.scheme == "https":
        return 443
    return None


def check_ssrf(base_url: str, constructed_url: str) -> str | None:
    """Guard against SSRF via URL authority tricks.

    Returns an error string if the constructed URL doesn't match the base
    URL's scheme/host/port. Returns None if the URL is safe.
    """
    parsed_base = urlparse(base_url)
    parsed_url = urlparse(constructed_url)

    base_port = effective_port(parsed_base)
    url_port = effective_port(parsed_url)

    if (
        parsed_url.hostname != parsed_base.hostname
        or parsed_url.scheme != parsed_base.scheme
        or url_port != base_port
    ):
        return (
            "ERROR: Constructed URL does not match the configured endpoint "
            f"(scheme/host/port mismatch: {parsed_url.scheme!r}://{parsed_url.hostname!r}:{url_port!r} "
            f"!= {parsed_base.scheme!r}://{parsed_base.hostname!r}:{base_port!r}). Aborting."
        )
    return None


def validate_package_name(name: str) -> str | None:
    """Validate a package name against RPM naming rules.

    Returns an error string if invalid, None if valid.
    """
    if not name:
        return "ERROR: Package name must not be empty."
    if not _VALID_PACKAGE_NAME_RE.match(name):
        return (
            f"ERROR: Invalid package name {name!r}. "
            "Package names must start with an alphanumeric character and "
            "contain only alphanumerics, '.', '_', '+', or '-'."
        )
    return None


def write_output(
    text: str,
    output_dir: str,
    prefix: str,
    extra_msg: str = "",
) -> str:
    """Write text to a temp file and return a summary.

    If the output is small (<= INLINE_THRESHOLD_BYTES), the content is
    included inline so the agent doesn't need a follow-up read_file call.
    """
    os.makedirs(output_dir, exist_ok=True)
    fd, out_path = tempfile.mkstemp(prefix=prefix, dir=output_dir)
    with os.fdopen(fd, "w") as f:
        f.write(text)

    size = len(text.encode("utf-8", errors="replace"))
    lines = text.count("\n")
    header = f"Wrote {size} bytes ({lines} lines) to {out_path}"
    if extra_msg:
        header = f"{extra_msg}\n{header}"

    if size <= INLINE_THRESHOLD_BYTES:
        return f"{header}\n\n{text}"
    return header
