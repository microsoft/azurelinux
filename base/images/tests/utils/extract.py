# SPDX-License-Identifier: MIT
"""Image mounting/unmounting orchestration.

Uses CLI tools (guestmount, skopeo, umoci) via subprocess to avoid
system site-packages dependencies.
"""

from __future__ import annotations

import contextlib
import json
import logging
import os
import shutil
import subprocess
import tarfile
from collections.abc import Callable
from pathlib import Path, PurePosixPath
from typing import Any

from .tools import NativeTool

logger = logging.getLogger(__name__)

# Native tool dependencies. Declared at module level so they're registered
# (and used at the call sites below) where they're needed.
GUESTMOUNT = NativeTool(
    name="guestmount",
    package_hint="libguestfs",
    reason="FUSE-mount VM images read-only",
    when="vm",
)
GUESTUNMOUNT = NativeTool(
    name="guestunmount",
    package_hint="libguestfs",
    reason="unmount guestmount FUSE mounts",
    when="vm",
)
SKOPEO = NativeTool(
    name="skopeo",
    package_hint="skopeo",
    reason="convert OCI archives to OCI layouts",
    when="container",
)
UMOCI = NativeTool(
    name="umoci",
    package_hint="umoci",
    reason="rootless OCI image unpacking",
    when="container",
)
BUILDAH = NativeTool(
    name="buildah",
    package_hint="buildah",
    reason="cleanup rootless umoci extracts (buildah unshare)",
    when="container",
)


def _run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
    """Run a command, logging it and raising with stderr on failure."""
    logger.info("Running: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    if result.returncode != 0:
        logger.error(
            "Command failed (rc=%d): %s\nstdout: %s\nstderr: %s",
            result.returncode,
            " ".join(cmd),
            result.stdout,
            result.stderr,
        )
        raise subprocess.CalledProcessError(
            result.returncode,
            cmd,
            output=result.stdout,
            stderr=result.stderr,
        )
    return result


# -- VM image mounting (libguestfs FUSE) ------------------------------------


def _guestfs_env() -> dict[str, str]:
    """Build environment with direct libguestfs backend."""
    return {**os.environ, "LIBGUESTFS_BACKEND": "direct"}


def mount_vm_image(image_path: Path, mountpoint: Path) -> Path:
    """Mount a VM image read-only via ``guestmount``.

    Enables aggressive FUSE kernel caching since the mount is read-only
    and the image never changes during the test session.

    Returns the *mountpoint* path on success.
    """
    mountpoint.mkdir(parents=True, exist_ok=True)
    cmd = [
        GUESTMOUNT.name,
        "--ro",
        "-a",
        str(image_path),
        "-i",
        str(mountpoint),
        # Aggressive caching — safe because the mount is read-only.
        "-o",
        "kernel_cache",
        "-o",
        "entry_timeout=3600",
        "-o",
        "attr_timeout=3600",
        "-o",
        "negative_timeout=3600",
        "-o",
        "noforget",
        "--dir-cache-timeout",
        "3600",
    ]
    _run(cmd, env=_guestfs_env())
    return mountpoint


def unmount_vm_image(mountpoint: Path) -> None:
    """Unmount a guestmount FUSE mount.

    Logs a warning on failure rather than raising — leaving teardown
    to fail the whole pytest session would obscure the real test
    result, and a stale FUSE mount is recoverable manually with
    ``fusermount -u``.
    """
    logger.info("Unmounting VM image at %s", mountpoint)
    result = subprocess.run(
        [GUESTUNMOUNT.name, str(mountpoint)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        logger.warning(
            "guestunmount failed for %s (rc=%d): %s",
            mountpoint,
            result.returncode,
            result.stderr.strip(),
        )


# -- Container image extraction (skopeo + umoci) ---------------------------


def mount_container_image(image_path: Path, extract_dir: Path) -> Path:
    """Extract a container image rootfs using ``skopeo`` + ``umoci``.

    Converts the OCI archive to an OCI layout via ``skopeo copy``, then
    unpacks it with ``umoci unpack --rootless``. Returns the rootfs path.
    """
    image_path = image_path.resolve()
    extract_dir = extract_dir.resolve()
    oci_layout = extract_dir / "oci-layout"
    bundle = extract_dir / "bundle"
    extract_dir.mkdir(parents=True, exist_ok=True)

    # Convert OCI archive → OCI layout
    logger.info("Converting OCI archive to layout: %s", image_path)
    _run(
        [
            SKOPEO.name,
            "copy",
            f"oci-archive:{image_path}",
            f"oci:{oci_layout}:latest",
        ]
    )

    # Unpack into an OCI runtime bundle (rootless, no user-ns required)
    logger.info("Unpacking OCI layout to bundle: %s", bundle)
    _run(
        [
            UMOCI.name,
            "unpack",
            "--rootless",
            "--image",
            f"{oci_layout}:latest",
            str(bundle),
        ]
    )

    rootfs = bundle / "rootfs"
    logger.info("Container rootfs at %s", rootfs)
    return rootfs


def unmount_container_image(extract_dir: Path) -> None:
    """Clean up the extracted container filesystem.

    Uses ``buildah unshare`` so that read-only directories (preserved by
    rootless ``umoci unpack``) can be removed without permission errors.
    Failures are logged rather than raised; see :func:`unmount_vm_image`.
    """
    logger.info("Removing container extract dir %s", extract_dir)
    result = subprocess.run(
        [BUILDAH.name, "unshare", "rm", "-rf", str(extract_dir)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        logger.warning(
            "buildah unshare rm failed for %s (rc=%d): %s",
            extract_dir,
            result.returncode,
            result.stderr.strip(),
        )


# -- WSL image extraction (plain rootfs tarball) ---------------------------


def _resolves_within(dest: Path, candidate: Path) -> bool:
    """Return True if ``candidate`` normalizes to ``dest`` or a path under it."""
    resolved = Path(os.path.normpath(candidate))
    return resolved == dest or dest in resolved.parents


def _require_within(dest: Path, candidate: Path, message: str) -> None:
    """Raise ``RuntimeError(message)`` unless ``candidate`` stays within ``dest``."""
    if not _resolves_within(dest, candidate):
        raise RuntimeError(message)


def _find_preceding_member(
    members: list[tarfile.TarInfo],
    normalized_names: list[str],
    index: int,
    linkname: str,
) -> tarfile.TarInfo | None:
    """Resolve a hardlink target the way :class:`tarfile.TarFile` does.

    ``TarFile._find_link_target`` normalizes the linkname and, for a hardlink,
    searches only the members *before* the link (a hardlink references an
    already-archived file), returning the latest match by normalized name.
    Mirror that exactly so this precheck cannot disagree with what extraction
    actually links to (e.g. a ``linkname`` like ``a/b/../b/s`` or duplicate
    member names would otherwise be missed by a raw-name lookup).
    """
    assert len(members) == len(normalized_names), "members and normalized_names must be parallel"
    wanted = os.path.normpath(linkname)
    for j in range(index - 1, -1, -1):
        if normalized_names[j] == wanted:
            return members[j]
    return None


def _assert_wsl_members_contained(members: list[tarfile.TarInfo], dest: Path) -> None:
    """Reject an archive whose members would escape ``dest``.

    The stdlib ``tar``/``data`` extraction filters are not a sufficient
    boundary on their own: CVE-2026-11940 shows unpatched CPython (any
    version below the fix, which ``requires-python = ">=3.12"`` still permits)
    can be tricked into writing outside the destination when a hardlink
    references a symlink stored at a deeper name than the hardlink itself.
    We therefore validate every member up front and extract nothing if any
    of them could escape, so a damaged or hostile ``--image-path`` cannot
    write outside the extraction tree.

    A rootfs legitimately contains symlinks with *absolute* targets (e.g.
    ``/usr/bin``). Those denote paths inside the image and stay contained when
    re-based at the root, so they are permitted here; the separate risk of a
    host-side read following such a link out of the tree is handled at read
    time by :func:`read_text_confined`, not by rejecting the link.

    Hardlink resolution mirrors :func:`_find_preceding_member` so this check
    agrees with ``tarfile``'s own link handling.

    Raises:
        RuntimeError: If any member name or relative symlink target resolves
            outside ``dest``, or if a hardlink resolves to a symlink member
            (the CVE-2026-11940 escape primitive).
    """
    normalized_names = [os.path.normpath(member.name) for member in members]
    for index, member in enumerate(members):
        member_path = dest / member.name
        _require_within(dest, member_path, f"WSL archive member escapes destination: {member.name!r}")

        # Relative symlinks are allowed only if their target, resolved from the
        # link's own directory, stays inside the tree; a relative target that
        # climbs out (e.g. ``../../../../etc/passwd``) is rejected here.
        # Absolute symlink targets (e.g. ``/usr/bin``) are intentionally NOT
        # checked here: they denote a path inside the image once re-based at
        # the rootfs and are normal in a real rootfs, so they are permitted at
        # extraction time and instead confined at read time by
        # :func:`read_text_confined`.
        if member.issym() and not PurePosixPath(member.linkname).is_absolute():
            target = member_path.parent / member.linkname
            _require_within(
                dest,
                target,
                f"WSL archive symlink escapes destination: {member.name!r} -> {member.linkname!r}",
            )

        if member.islnk():
            # A hardlink's linkname is a path inside the archive; it must stay
            # within the destination on its own.
            _require_within(
                dest,
                dest / os.path.normpath(member.linkname),
                f"WSL archive hardlink escapes destination: {member.name!r} -> {member.linkname!r}",
            )
            # CVE-2026-11940: a hardlink whose resolved member is a symlink is
            # the escape primitive. During extraction ``tarfile`` performs
            # ``os.link(rootfs/<target>, <hardlink>)`` which *follows* the
            # symlink, hardlinking the host inode it points at and then applying
            # archive-controlled metadata to it. A single lexical target check
            # is insufficient because a chain (``s1 -> s2 -> /host/file``) keeps
            # each intermediate lexically inside the archive. A hardlink to a
            # symlink is never legitimate in a rootfs tarball, so reject it
            # outright regardless of where the chain ultimately points.
            #
            # A hardlink must also resolve to an *exact* earlier archive
            # member. If it does not, ``tarfile`` falls back to ``os.link`` on
            # whatever ``rootfs/<linkname>`` resolves to on disk — and an
            # intermediate component may itself be an already-extracted symlink
            # to a host path (e.g. member ``a -> /home/runner/...`` then a
            # hardlink with linkname ``a/file``). That would hardlink a host
            # inode and then apply archive-controlled metadata to it, so an
            # unresolved target is rejected.
            linked = _find_preceding_member(members, normalized_names, index, member.linkname)
            if linked is None:
                raise RuntimeError(
                    f"WSL archive hardlink has no matching earlier member (would link a host path): "
                    f"{member.name!r} -> {member.linkname!r}",
                )
            if linked.issym():
                raise RuntimeError(
                    f"WSL archive hardlink targets a symlink (CVE-2026-11940 escape primitive): "
                    f"{member.name!r} -> {linked.name!r}",
                )


def read_text_confined(root: Path, relative_path: str, *, max_links: int = 40) -> str:
    """Read a text file under ``root`` without following links out of the tree.

    An extracted rootfs is inspected through ordinary host paths (there is no
    chroot), so the host resolves symlinks against the *host* root: an absolute
    link such as ``/etc/os-release -> /etc/shadow`` — or a ``../`` chain — would
    otherwise let a crafted image make a test read a file outside ``root``.
    Resolve the path chroot-style instead: absolute link targets restart at
    ``root`` and ``..`` never climbs above it, so the read is confined to the
    extraction tree while still honouring the absolute intra-image symlinks a
    rootfs legitimately uses.

    Raises:
        RuntimeError: If the path cannot be resolved within ``root`` (e.g. a
            symlink loop exceeds ``max_links``).
    """
    root = root.resolve()
    current = root
    pending = list(PurePosixPath(relative_path).parts)
    links_followed = 0
    while pending:
        name = pending.pop(0)
        # PurePosixPath.parts collapses "" and "." components, so the only
        # non-name element that can appear is the "/" anchor of an absolute path.
        if name == "/":
            continue
        if name == "..":
            if current != root:
                current = current.parent
            continue
        candidate = current / name
        if candidate.is_symlink():
            links_followed += 1
            if links_followed > max_links:
                raise RuntimeError(f"too many symlinks resolving {relative_path!r} under {root}")
            link_target = PurePosixPath(candidate.readlink())
            if link_target.is_absolute():
                current = root
                pending = [*link_target.parts[1:], *pending]
            else:
                pending = [*link_target.parts, *pending]
        else:
            current = candidate
    return current.read_text()


def mount_wsl_image(image_path: Path, extract_dir: Path) -> Path:
    """Extract a WSL image rootfs and return its path.

    A WSL image is a plain (optionally gzip-compressed) rootfs tarball, not
    an OCI archive. Every member is validated against the destination up
    front (see :func:`_assert_wsl_members_contained`) so nothing is written
    if the archive could escape the extraction tree; this does not rely on
    the stdlib extraction filter, which CVE-2026-11940 shows is bypassable on
    unpatched interpreters that ``requires-python = ">=3.12"`` still permits.
    Only then is it unpacked rootlessly with the ``tar`` filter, which
    additionally preserves absolute symlink targets used by a rootfs and
    normalizes leading separators in member names. File *content* is later
    read via :func:`read_text_confined` so absolute symlinks cannot escape the
    tree at read time either.
    """
    image_path = image_path.resolve()
    extract_dir = extract_dir.resolve()
    rootfs = extract_dir / "rootfs"
    rootfs.mkdir(parents=True, exist_ok=True)

    logger.info("Extracting WSL rootfs tarball %s to %s", image_path, rootfs)
    with tarfile.open(image_path) as tar:
        _assert_wsl_members_contained(tar.getmembers(), rootfs.resolve())
        tar.extractall(rootfs, filter="tar")

    logger.info("WSL rootfs at %s", rootfs)
    return rootfs


def unmount_wsl_image(extract_dir: Path) -> None:
    """Remove the extracted WSL rootfs.

    Rootless extraction can leave read-only directories, so make entries
    writable before unlinking. Failures are logged, not raised.
    """
    logger.info("Removing WSL extract dir %s", extract_dir)

    def _make_writable_and_retry(func: Callable[[str], object], path: str, _exc: BaseException) -> None:
        entry = Path(path)
        # Unlink permission comes from the parent directory, so making the
        # parent writable is what allows the retry to remove a child of a
        # read-only (e.g. 0555) directory. shutil.rmtree never recurses into
        # symlinked directories (it unlinks them as leaves), so the parent is
        # always a real directory here; guard it anyway to make that explicit
        # and to never chmod through a symlink out of the extraction tree.
        parent = entry.parent
        if not parent.is_symlink():
            with contextlib.suppress(OSError):
                parent.chmod(0o700)
        # Only chmod real directories/files so recursion into a read-only
        # subdir can proceed. Never chmod a symlink: Path.chmod follows the
        # link and the tar filter permits absolute symlink targets, so this
        # could alter a host path outside the extraction tree. Unlinking a
        # symlink needs only the parent to be writable, handled above.
        if not entry.is_symlink():
            with contextlib.suppress(OSError):
                entry.chmod(0o700)
        func(path)

    try:
        shutil.rmtree(extract_dir, onexc=_make_writable_and_retry)
    except OSError as exc:
        # Mirror unmount_vm_image: a teardown failure shouldn't fail the
        # pytest session; a leftover dir is recoverable manually.
        logger.warning("Failed to remove WSL extract dir %s: %s", extract_dir, exc)


def inspect_oci_config(image_path: Path) -> dict[str, Any]:
    """Return the OCI image configuration for a container archive.

    Runs ``skopeo inspect --config`` against the OCI archive and parses
    the resulting JSON (the OCI image config, which carries the
    ``config`` object with ``User``, ``Cmd``, ``WorkingDir``, etc.).
    Unlike rootfs extraction this needs only ``skopeo`` — no umoci unpack.
    """
    image_path = image_path.resolve()
    logger.info("Inspecting OCI image config: %s", image_path)
    result = _run(
        [
            SKOPEO.name,
            "inspect",
            "--config",
            f"oci-archive:{image_path}",
        ]
    )
    return json.loads(result.stdout)
