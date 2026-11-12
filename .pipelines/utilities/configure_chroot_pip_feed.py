#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import argparse
import os
from pathlib import Path
import urllib.parse


MARKER = "# Package-test job-local pip feed configuration\n"
CONFIG_PATH = Path("etc/pip.conf")
AUTH_PATH = Path("root/.netrc")


def parse_feed(index_url):
    if any(ord(character) <= 32 or ord(character) >= 127 for character in index_url):
        raise ValueError("The authenticated feed URL contains invalid characters.")
    try:
        parsed = urllib.parse.urlsplit(index_url)
        port = parsed.port
    except ValueError:
        raise ValueError("The authenticated feed URL is malformed.") from None
    if (
        parsed.scheme != "https"
        or parsed.hostname != "pkgs.dev.azure.com"
        or port not in (None, 443)
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Expected the HTTPS Azure Artifacts Python feed.")
    parts = parsed.path.rstrip("/").lower().split("/")
    # PR checks use the organization feed; Fast-Track uses the project feed.
    organization_feed = (
        len(parts) == 6
        and parts[1:3] == ["mariner-org", "_packaging"]
        and parts[3] in ("marinerfeed", "3a751d8b-0b69-4afc-a438-9487dba86628")
        and parts[4:] == ["pypi", "simple"]
    )
    project_feed = (
        len(parts) == 7
        and parts[1] == "mariner-org"
        and parts[2] in ("mariner", "36d030d6-1d99-4ebd-878b-09af1f4f722f")
        and parts[3] == "_packaging"
        and parts[4] in ("mariner-pypi-feed", "ca2ce712-f15f-4dd0-b8c8-518db39ff9ec")
        and parts[5:] == ["pypi", "simple"]
    )
    if not (organization_feed or project_feed):
        raise ValueError("Expected an approved Mariner Python feed simple index.")
    username = urllib.parse.unquote(parsed.username or "")
    password = urllib.parse.unquote(parsed.password or "")
    for value in (username, password):
        if not value or any(ord(c) <= 32 or ord(c) >= 127 or c in '"\\#' for c in value):
            raise ValueError("The feed requires valid job-local authentication.")
    clean_url = urllib.parse.urlunsplit(("https", parsed.hostname, parsed.path, "", ""))
    return clean_url, parsed.hostname, username, password


def contained_path(root, relative):
    destination = root / relative
    if not destination.resolve().is_relative_to(root) or destination.is_symlink():
        raise ValueError("The pip configuration path escapes the worker chroot.")
    return destination


def configure_feed(root, index_url):
    clean_url, hostname, username, password = parse_feed(index_url)
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("The worker chroot is not a directory.")
    config = contained_path(root, CONFIG_PATH)
    auth = contained_path(root, AUTH_PATH)
    for destination in (config, auth):
        if destination.exists():
            raise FileExistsError("Refusing to overwrite existing worker pip configuration.")
    config.parent.mkdir(parents=True, exist_ok=True)
    auth.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    # Separate job authentication from the index URL so pip need not log a
    # credential-bearing URL. No host .netrc is read or copied.
    with auth.open("x", encoding="ascii", newline="\n") as output:
        auth.chmod(0o600)
        output.write(MARKER)
        output.write(f"machine {hostname}\nlogin {username}\npassword {password}\n")
    with config.open("x", encoding="ascii", newline="\n") as output:
        output.write(
            MARKER
            + "[global]\n"
            + f"index-url = {clean_url}\n"
            + "extra-index-url =\n"
            + "cert = /etc/pki/tls/certs/ca-bundle.crt\n"
            + "no-cache-dir = true\n"
            + "disable-pip-version-check = true\n"
        )


def cleanup_feed(root):
    root = root.resolve()
    worker = root.parent
    roots = [root]
    # Failed or retained package workers can contain copies of the same files.
    chroots = worker / "chroot"
    if chroots.exists():
        if chroots.is_symlink():
            raise ValueError("Refusing to traverse a symlinked package-chroot directory.")
        for package in chroots.iterdir():
            if package.is_symlink():
                raise ValueError("Refusing to traverse a symlinked package chroot.")
            if package.is_dir():
                roots.append(package.resolve())
    managed = []
    for candidate in roots:
        for relative in (AUTH_PATH, CONFIG_PATH):
            path = contained_path(candidate, relative)
            if path.exists():
                with path.open("rb") as source:
                    # Leave pre-existing configuration alone; remove our
                    # credential-free pip.conf along with its job authentication.
                    if source.readline() == MARKER.encode("ascii"):
                        managed.append(path)
    if managed:
        # The archive also contains credentials; deleting only .netrc from the
        # extracted files would leave a reusable credential-bearing copy behind.
        archive = worker / "worker_chroot.tar.gz"
        if archive.is_symlink():
            raise ValueError("Refusing to remove a symlinked worker archive.")
        archive.unlink(missing_ok=True)
        for path in managed:
            path.unlink()


def main():
    parser = argparse.ArgumentParser(
        description="Configure job-local, on-demand pip feed access in package-test chroots."
    )
    parser.add_argument("root", type=Path)
    parser.add_argument("--cleanup", action="store_true")
    args = parser.parse_args()
    try:
        if args.cleanup:
            cleanup_feed(args.root)
            print("Removed managed worker pip credentials and their job-local archive.")
        else:
            index_url = os.environ.get("PIP_INDEX_URL")
            if not index_url:
                raise ValueError("PIP_INDEX_URL must be supplied by PipAuthenticate.")
            configure_feed(args.root, index_url)
            print("Configured the approved pip feed; credentials remain job-local.")
    except OSError as error:
        detail = error.strerror or str(error)
        parser.exit(1, f"ERROR: Cannot configure or clean up the worker pip feed: {detail}.\n")
    except ValueError as error:
        parser.exit(1, f"ERROR: Cannot configure or clean up the worker pip feed: {error}.\n")


if __name__ == "__main__":
    main()
