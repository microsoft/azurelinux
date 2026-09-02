#!/usr/bin/env python3
"""Repack the gnome-autoar upstream tarball with its encrypted test fixtures removed.

The three ``tests/files/extract/test-encrypted*/`` fixtures ship
password-protected ``input/arextract.zip`` files that the package-signing scan
refuses to inspect and blocks on (the flagged bytes live in the ``.src.rpm``
itself, so skipping the tests at ``%check`` time would not help -- the files
have to physically leave the tarball). This script removes those fixture
directories, drops the three meson test cases that read them so ``%meson_test``
still passes, and repacks the tarball deterministically.

This component uses ``modify_source.py`` + ``origin=download`` rather than an
azldev archive overlay because the upstream tarball ships an absolute-target
symlink fixture (``tests/files/extract/test-symlink-parent/reference/arextract
-> /tmp``) that azldev's overlay extractor refuses to extract. ``tar`` handles
it, so the repack is done out-of-band and the result is served via
``origin=download``.

The repack pins the umask and fixes the ``tar`` member order, mtime and owner so
the output is stable for a given ``tar``/``xz`` toolchain (``xz`` output is not
guaranteed identical across liblzma versions). The published artifact -- pinned
by SHA-512 in ``specs/g/gnome-autoar/sources`` -- is the source of truth the
build downloads; this script only regenerates an equivalent tarball.
Regenerating on a different toolchain may yield a new hash, which then has to be
re-published and re-pinned.

Output lands under ``<repo-root>/base/build/work/scratch/<package>/``.
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PACKAGE_NAME = "gnome-autoar"
VERSION = "0.4.5"
ORIGINAL_NAME = f"{PACKAGE_NAME}-{VERSION}.tar.xz"
TOPDIR = f"{PACKAGE_NAME}-{VERSION}"

# Pristine upstream Source0 SHA-512 (download.gnome.org), used to verify the
# download before repacking. This is the ORIGINAL upstream checksum, not the
# modified/served hash that now lives in specs/g/gnome-autoar/sources.
UPSTREAM_SHA512 = (
    "ba38dfc0ad3c00fd8316d02d1a8e38ce3c743e11032f7c4efff74e7c3f8e8e815"
    "a1debe51eae8e2ee653155356d34992f1bc0e35e6cfab82398265fde8648050"
)
UPSTREAM_URL = (
    f"https://download.gnome.org/sources/{PACKAGE_NAME}/0.4/{ORIGINAL_NAME}"
)

# Encrypted extract-test fixture directories removed to avoid scan failures on
# the SRPM. Each ships an encrypted input/arextract.zip. Paths are relative to
# the tarball's top-level directory. Sorted alphabetically.
FIXTURE_DIRS_TO_REMOVE = (
    "tests/files/extract/test-encrypted",
    "tests/files/extract/test-encrypted-request-passphrase",
    "tests/files/extract/test-encrypted-wrong-passphrase",
)

# The meson extract-unit test hard-codes three encrypted cases that read the
# fixtures above; drop their function definitions and g_test_add_func
# registrations so the remaining suite still runs.
TEST_FILE = "tests/test-extract-unit.c"

# Fixed umask so `tar -x` records reproducible file modes regardless of the
# caller's environment (extracting the same archive under different umasks would
# otherwise yield different modes and therefore a different repacked SHA-512).
REPACK_UMASK = 0o022


def sha512_of(path: Path) -> str:
    """Return the hex SHA-512 digest of the file at ``path``."""
    digest = hashlib.sha512()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edit_test_file(path: Path) -> None:
    """Drop the three encrypted test cases + their registrations in place."""
    text = path.read_text(encoding="utf-8")

    # 1) Remove the three contiguous encrypted test function definitions
    #    (test_encrypted, test_encrypted_request_passphrase,
    #     test_encrypted_wrong_passphrase).
    defs = re.compile(
        r"\nstatic void\ntest_encrypted \(void\)\n.*?"
        r"\nstatic void\ntest_encrypted_wrong_passphrase \(void\)\n\{.*?\n\}\n",
        re.DOTALL,
    )
    text, n_defs = defs.subn("", text, count=1)
    if n_defs != 1:
        sys.exit(f"expected 1 encrypted-def block, removed {n_defs}")

    # 2) Remove the three contiguous g_test_add_func registrations.
    regs = re.compile(
        r'\n\n  g_test_add_func \("/autoar-extract/test-encrypted",\n'
        r".*?test_encrypted_wrong_passphrase\);",
        re.DOTALL,
    )
    text, n_regs = regs.subn("", text, count=1)
    if n_regs != 1:
        sys.exit(f"expected 1 encrypted-registration block, removed {n_regs}")

    if "test_encrypted" in text:
        sys.exit("residual test_encrypted reference remains after edit")

    path.write_text(text, encoding="utf-8")


def main() -> None:
    """Download, verify, de-fixture, and deterministically repack the tarball."""
    os.umask(REPACK_UMASK)

    # Repo root from this script's own path (<root>/base/comps/<pkg>/), not the
    # caller's CWD, so it resolves correctly when invoked by absolute path.
    repo_root = Path(__file__).resolve().parents[3]
    workdir = repo_root / "base" / "build" / "work" / "scratch" / PACKAGE_NAME
    workdir.mkdir(parents=True, exist_ok=True)
    os.chdir(workdir)

    original = Path(ORIGINAL_NAME)
    print(f"[1/6] Downloading {ORIGINAL_NAME}")
    if not original.exists():
        try:
            subprocess.run(
                ["curl", "-fsSL", "--retry", "3", "-o", ORIGINAL_NAME, UPSTREAM_URL],
                check=True,
            )
        except subprocess.CalledProcessError:
            original.unlink(missing_ok=True)  # don't leave a partial that blocks re-runs
            raise

    print("[2/6] Verifying upstream SHA512")
    computed = sha512_of(original)
    if computed != UPSTREAM_SHA512:
        original.unlink(missing_ok=True)  # drop the bad file so a re-run re-downloads
        sys.exit(
            "ERROR: upstream SHA512 mismatch\n"
            f"  expected: {UPSTREAM_SHA512}\n"
            f"  computed: {computed}"
        )

    print("[3/6] Extracting")
    extract_dir = Path("extracted")
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir()
    subprocess.run(["tar", "-xf", ORIGINAL_NAME, "-C", str(extract_dir)], check=True)

    print(f"[4/6] Removing {len(FIXTURE_DIRS_TO_REMOVE)} encrypted fixture dirs")
    for rel in FIXTURE_DIRS_TO_REMOVE:
        target = extract_dir / TOPDIR / rel
        if not target.is_dir():
            sys.exit(
                f"ERROR: expected fixture dir not present in upstream tarball: {rel}"
            )
        shutil.rmtree(target)

    print(f"[5/6] Dropping encrypted test cases from {TEST_FILE}")
    test_path = extract_dir / TOPDIR / TEST_FILE
    edit_test_file(test_path)
    # Sanity: sibling tests must survive.
    if "test_readonly_directory" not in test_path.read_text(encoding="utf-8"):
        sys.exit("ERROR: sibling test unexpectedly removed")

    print("[6/6] Repacking deterministically")
    modified = Path(f"{ORIGINAL_NAME}.modified")
    modified.unlink(missing_ok=True)
    # Stable byte output: sorted names, fixed mtime, zeroed owner/group,
    # single-threaded xz. tar writes to xz's stdin; xz writes the archive.
    with modified.open("wb") as out:
        tar = subprocess.Popen(
            [
                "tar",
                "--sort=name",
                "--mtime=2024-01-01 00:00:00 UTC",
                "--owner=0",
                "--group=0",
                "--numeric-owner",
                "-cf",
                "-",
                TOPDIR,
            ],
            cwd=extract_dir,
            stdout=subprocess.PIPE,
        )
        if tar.stdout is None:
            sys.exit("ERROR: failed to open tar output pipe")
        xz = subprocess.Popen(
            ["xz", "-T1", "-9e"], stdin=tar.stdout, stdout=out
        )
        tar.stdout.close()  # allow tar to receive SIGPIPE if xz exits
        if xz.wait() != 0 or tar.wait() != 0:
            sys.exit("ERROR: repack failed")

    modified_sha512 = sha512_of(modified)
    # Record the checksum against the actual modified file so `sha512sum -c` works.
    Path(f"{ORIGINAL_NAME}.modified.sha512").write_text(
        f"{modified_sha512}  {ORIGINAL_NAME}.modified\n", encoding="utf-8"
    )

    print(
        f"\nRegenerated tarball: {workdir / modified.name}\n"
        f"SHA512:              {modified_sha512}\n\n"
        "Publish this artifact to the project source mirror and pin the SHA-512\n"
        "above in specs/g/gnome-autoar/sources. See the maintainer documentation\n"
        "for the publishing steps."
    )


if __name__ == "__main__":
    main()
