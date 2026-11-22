#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Redact the values of named environment variables from files under the given directories.

Package builds that run %check can receive environment variables (see CHECK_ENV_PASSTHROUGH), and
package tests can print them, for example a feed URL with an embedded credential. Pipeline secret
masking covers console output only, so run this over build logs before publishing them.

Usage: redact_env_values.py "NAME [NAME ...]" [DIR ...]

Values are read from this process's environment and never taken from arguments. Values (and URL
passwords) shorter than MIN_SECRET_LENGTH cannot be redacted safely because they are too likely to
match unrelated text, so they are rejected: the script exits 1 without modifying any file. Without
DIR arguments it only performs that validation, so callers can reject such values before a build.

On failure, logs may still contain the values; callers decide whether to publish them.
"""

from __future__ import annotations

import os
import sys
import urllib.parse
from pathlib import Path

MIN_SECRET_LENGTH = 8
MIN_ARGUMENTS = 1
REDACTED = b"***"


class UnsupportedSecretError(ValueError):
    """A forwarded value is too short to redact safely. Messages never include the value."""


def secret_patterns(names: list[str], environment: dict[str, str]) -> list[bytes]:
    """Return the byte strings to redact for the variables ``names``, longest first.

    Each value is redacted whole. When a value is a URL with a password, the password is also
    redacted in both its encoded and decoded forms. Unset and empty variables are skipped.

    Raises:
        UnsupportedSecretError: A value or URL password is shorter than ``MIN_SECRET_LENGTH``.
    """
    secrets: set[str] = set()
    for name in names:
        value = environment.get(name, "")
        candidates = {value}
        try:
            password = urllib.parse.urlsplit(value).password
        except ValueError:
            password = None
        if password:
            candidates.update({password, urllib.parse.unquote(password)})
        for candidate in candidates - {""}:
            if len(candidate) < MIN_SECRET_LENGTH:
                message = f"{name}: value or URL password is shorter than {MIN_SECRET_LENGTH} characters"
                raise UnsupportedSecretError(message)
        secrets.update(candidates - {""})
    # Longest first, so a full URL is replaced before the credential inside it.
    return sorted((secret.encode() for secret in secrets), key=len, reverse=True)


def redact_tree(root: Path, patterns: list[bytes]) -> int:
    """Replace ``patterns`` in every regular file under ``root``; return the number of files changed."""
    changed = 0
    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file():
            continue
        original = path.read_bytes()
        content = original
        for pattern in patterns:
            content = content.replace(pattern, REDACTED)
        if content != original:
            path.write_bytes(content)
            changed += 1
    return changed


def main(argv: list[str]) -> int:
    """Redact the named variables' values under each existing directory; return the exit code."""
    if len(argv) < MIN_ARGUMENTS:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        patterns = secret_patterns(argv[0].split(), dict(os.environ))
    except UnsupportedSecretError as error:
        print(f"redact_env_values: cannot redact {error}", file=sys.stderr)
        return 1
    if len(argv) == MIN_ARGUMENTS:
        return 0
    roots = [Path(directory) for directory in argv[1:] if Path(directory).is_dir()]
    changed = sum(redact_tree(root, patterns) for root in roots)
    print(f"Redacted forwarded check variables from {changed} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
