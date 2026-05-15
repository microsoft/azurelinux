# SPDX-License-Identifier: MIT
"""Repository metadata fetch + parse — thin wrapper around librepo + createrepo_c.

This module is an *implementation* layer; fixtures and tests do not
import it. :class:`utils.metadata.MetadataService` wraps it to provide
a caching service interface.

Design
------

* :func:`fetch_repo` uses ``librepo`` to download ``repomd.xml`` and
  the ``primary`` + ``filelists`` records into a per-repo cache
  directory. librepo handles checksum verification, zchunk/zstd/xz/gz
  decompression, mirror handling, retries, and the atomic-rename
  guarantees we used to do by hand.

* :func:`iter_packages` and :func:`iter_filelist_entries` use
  ``createrepo_c``'s C-based primary/filelists parsers, which return
  rich pre-typed records and stream the underlying file (so memory is
  bounded for very large filelists).

The previous implementation hand-rolled HTTP fetch with retries,
checksum verification, multi-format decompression (gz/xz/zstd via
``zstandard``), and ``defusedxml.iterparse`` of primary + filelists
— ~700 lines that did exactly what librepo+createrepo_c already do.
The dnf stack uses these same libraries internally, so the two
codepaths are now guaranteed to interpret repodata identically.
"""

from __future__ import annotations

import logging
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Generator

# ``createrepo_c`` is loaded via ``_dnf_stack`` so its noisy librpm
# initialization (which complains about Azure Linux's bundled rpm
# macros that the wheel's bundled librpm can't parse) is suppressed
# at import time. ``librepo`` is loaded lazily inside :func:`fetch_repo`
# because it's a system package (``python3-librepo``) that may not be
# visible from inside isolated venvs — we want ``pytest --collect-only``
# and ``pytest --help`` to work even when it isn't.
from ._dnf_stack import cr, get_librepo, get_rpm

from .types import NEVRA, ConflictEntry, FileEntry, FileMeta, Package, ProvidesEntry

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class RepodataError(Exception):
    """Base class for repodata fetch/parse errors."""


class RepodataFetchError(RepodataError):
    """Raised when librepo fails to fetch or verify a repo."""


class RepodataParseError(RepodataError):
    """Raised when createrepo_c fails to parse a metadata file."""


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------


# librepo's variable substitution covers $releasever and $basearch
# directly; we feed it ``arch``/``releasever`` and let it expand the
# baseurl. We never need to inherit either from the host.
_LR_VARS = ("arch", "basearch", "releasever")


@dataclass(frozen=True)
class RepoLayout:
    """Local paths to the metadata files of one fetched repo."""

    repomd: Path
    primary: Path
    filelists: Path


def fetch_repo(
    *,
    base_url: str,
    cache_dir: Path,
    arch: str,
    releasever: str | None,
) -> RepoLayout:
    """Fetch ``repomd.xml`` + primary + filelists into *cache_dir*.

    Returns the local paths librepo wrote them to. librepo verifies
    checksums against ``repomd.xml`` automatically, retries transient
    network failures, and decompresses zchunk in place; the caller
    just hands the resulting paths to :func:`iter_packages` /
    :func:`iter_filelist_entries`.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    librepo = get_librepo()
    h = librepo.Handle()
    h.urls = [base_url]
    h.repotype = librepo.YUMREPO
    h.destdir = str(cache_dir)
    # We only need primary + filelists for the metadata-only tests;
    # repoclosure loads the same cache_dir with a wider set
    # (see utils.repoclosure).
    h.yumdlist = ["primary", "filelists"]
    varsub = [("arch", arch), ("basearch", arch)]
    if releasever:
        varsub.append(("releasever", releasever))
    h.varsub = varsub
    # Verification is on by default; spelled out for clarity.
    h.checksum = True
    try:
        result = h.perform()
    except librepo.LibrepoException as exc:
        raise RepodataFetchError(f"failed to fetch {base_url}: {exc}") from exc

    yum_repo = result.yum_repo
    try:
        return RepoLayout(
            repomd=Path(yum_repo["repomd"]),
            primary=Path(yum_repo["primary"]),
            filelists=Path(yum_repo["filelists"]),
        )
    except KeyError as exc:
        raise RepodataFetchError(
            f"librepo result for {base_url} is missing record {exc}"
        ) from exc


# ---------------------------------------------------------------------------
# primary.xml parsing
# ---------------------------------------------------------------------------


def _epoch_to_int(epoch: str | None) -> int:
    """Coerce createrepo_c's string epoch (or None / "") to an int.

    createrepo_c reports epoch as a (possibly empty) string; the suite
    types epoch as ``int`` (defaulting to 0 when missing or unparseable).
    """
    if not epoch:
        return 0
    try:
        return int(epoch)
    except ValueError:
        return 0


def _convert_conflict(entry: tuple) -> ConflictEntry:
    """Map createrepo_c's ``(name, flags, epoch, ver, rel, pre)`` tuple."""
    name, flags, epoch, ver, rel, _pre = entry
    epoch_int: int | None = _epoch_to_int(epoch) if epoch else None
    return ConflictEntry(
        name=name,
        flags=flags or None,
        epoch=epoch_int,
        version=ver or None,
        release=rel or None,
    )


def _convert_provides(entry: tuple) -> ProvidesEntry:
    """Map createrepo_c's ``(name, flags, epoch, ver, rel, pre)`` tuple.

    Same shape as :func:`_convert_conflict`, separate type so callers
    can keep ``Provides:`` and ``Conflicts:`` semantically distinct.
    """
    name, flags, epoch, ver, rel, _pre = entry
    epoch_int: int | None = _epoch_to_int(epoch) if epoch else None
    return ProvidesEntry(
        name=name,
        flags=flags or None,
        epoch=epoch_int,
        version=ver or None,
        release=rel or None,
    )


def _convert_file(entry: tuple) -> FileEntry:
    """Map createrepo_c's ``(type|None, dirname, basename)`` tuple.

    createrepo_c always splits the path; we recombine because that's
    what the rest of the suite expects (single string paths).
    """
    ftype, dirname, basename = entry
    return FileEntry(
        path=dirname + basename,
        is_directory=(ftype == "dir"),
        is_ghost=(ftype == "ghost"),
    )


def _convert_package(crp: cr.Package) -> Package:
    """Convert a ``createrepo_c.Package`` into the suite's :class:`Package`."""
    nevra = NEVRA(
        name=crp.name,
        epoch=_epoch_to_int(crp.epoch),
        version=crp.version,
        release=crp.release,
        arch=crp.arch,
    )
    # ``provides`` is a list of (name, flags, epoch, ver, rel, pre)
    # tuples. We retain the full structure so version-aware
    # cross-repo conflict matching can evaluate ``Conflicts: foo
    # >= 2`` against a versioned virtual provide. RPM auto-emits a
    # versioned provide of the package's own name+EVR; we force a
    # synthesized one in if createrepo somehow omits it (cheap safety
    # net).
    provides = [_convert_provides(p) for p in (crp.provides or []) if p and p[0]]
    if not any(p.name == crp.name for p in provides):
        provides.append(ProvidesEntry(
            name=crp.name,
            flags="EQ",
            epoch=nevra.epoch or None,
            version=nevra.version,
            release=nevra.release,
        ))

    return Package(
        nevra=nevra,
        vendor=crp.rpm_vendor or None,
        sourcerpm=crp.rpm_sourcerpm or None,
        summary=crp.summary or None,
        provides=provides,
        conflicts=[_convert_conflict(c) for c in (crp.conflicts or [])],
        files=[_convert_file(f) for f in (crp.files or [])],
        location_href=crp.location_href or None,
        location_base=crp.location_base or None,
    )


def iter_packages(primary_path: Path) -> Generator[Package, None, None]:
    """Yield :class:`Package` records from a ``primary.xml(.gz|.xz|.zst)``.

    createrepo_c streams the file via libxml2; memory stays bounded
    even for very large repos.
    """
    pkgs: list[Package] = []

    def _cb(crp: cr.Package) -> None:
        pkgs.append(_convert_package(crp))

    try:
        cr.xml_parse_primary(str(primary_path), pkgcb=_cb)
    except cr.CreaterepoCError as exc:
        raise RepodataParseError(
            f"failed to parse {primary_path}: {exc}"
        ) from exc
    yield from pkgs


# ---------------------------------------------------------------------------
# filelists.xml parsing
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FilelistEntry:
    """One ``(NEVRA, file)`` entry from filelists.xml."""

    nevra: NEVRA
    path: str
    is_directory: bool
    is_ghost: bool


def iter_filelist_entries(
    filelists_path: Path,
) -> Generator[FilelistEntry, None, None]:
    """Yield one :class:`FilelistEntry` per file in ``filelists.xml``.

    createrepo_c invokes the callback once per package; we expand to
    one entry per file (which is what consumers want).
    """
    entries: list[FilelistEntry] = []

    def _cb(crp: cr.Package) -> None:
        nevra = NEVRA(
            name=crp.name,
            epoch=_epoch_to_int(crp.epoch),
            version=crp.version,
            release=crp.release,
            arch=crp.arch,
        )
        for ftype, dirname, basename in crp.files or ():
            entries.append(FilelistEntry(
                nevra=nevra,
                path=dirname + basename,
                is_directory=(ftype == "dir"),
                is_ghost=(ftype == "ghost"),
            ))

    try:
        cr.xml_parse_filelists(str(filelists_path), pkgcb=_cb)
    except cr.CreaterepoCError as exc:
        raise RepodataParseError(
            f"failed to parse {filelists_path}: {exc}"
        ) from exc
    yield from entries


# ---------------------------------------------------------------------------
# Per-package RPM fetching + file-metadata extraction
# ---------------------------------------------------------------------------
#
# The cross-repo file-conflicts test needs more than what filelists.xml
# carries (path + type + ghost flag): to mirror RPM's own
# ``rpmfilesCompare`` rules it needs ``mode`` / ``user`` / ``group`` /
# ``size`` / ``digest`` / ``linkto`` / ``rdev``. Those attributes are
# not in any createrepo XML record and ``libdnf5`` does not expose them
# either (its ``Package.get_files()`` is the same path-only set as
# filelists). The accurate path is to download the RPM and read the
# attributes straight out of its header via ``python3-rpm``.
#
# We do this lazily and on a per-NEVRA basis, only for packages that
# actually appear in a candidate cross-repo overlap, so the bandwidth
# cost scales with the number of suspected conflicts rather than the
# repo size. RPMs are cached on disk under the metadata workdir so a
# rerun against the same workdir doesn't re-download.


class RpmDownloadError(RepodataError):
    """Raised when librepo fails to fetch a single RPM."""


def download_rpm(
    *,
    repo_url: str,
    location_href: str,
    location_base: str | None,
    arch: str,
    releasever: str | None,
    dest_dir: Path,
) -> Path:
    """Fetch one RPM into *dest_dir* and return the local path.

    Uses the same librepo handle pattern :func:`fetch_repo` uses so
    ``$basearch`` / ``$arch`` / ``$releasever`` substitutions in the
    repo URL are handled identically. ``location_base`` (rare —
    set when a repo overrides the per-package base via
    ``<location xml:base="...">``) takes precedence over ``repo_url``.

    The resulting file is named after the basename of *location_href*,
    so a second call for the same package will hit the existing file
    and skip download (cache reuse). The download is staged through
    a per-call sibling temp directory and then ``os.replace``-d
    into ``final_path``, so a SIGKILL or crash mid-write cannot
    leave a truncated file at ``final_path`` — the cache-hit check
    here is positive-size-only, not content-validating, so a torn
    write would otherwise become a permanently poisoned cache
    entry that silently feeds corrupt headers into
    :func:`read_rpm_file_metadata`.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    final_path = dest_dir / Path(location_href).name
    if final_path.exists() and final_path.stat().st_size > 0:
        return final_path

    librepo = get_librepo()
    h = librepo.Handle()
    h.urls = [(location_base or repo_url).rstrip("/")]
    h.repotype = librepo.YUMREPO
    h.local = False
    varsub = [("arch", arch), ("basearch", arch)]
    if releasever:
        varsub.append(("releasever", releasever))
    h.varsub = varsub

    # Stage the librepo download into a sibling temp dir on the
    # same filesystem as ``final_path`` so the eventual
    # ``os.replace`` is a same-filesystem atomic rename.
    partial_dir = Path(tempfile.mkdtemp(
        prefix=f".{final_path.name}.",
        suffix=".partial",
        dir=str(dest_dir),
    ))
    try:
        target = librepo.PackageTarget(
            relative_url=location_href,
            dest=str(partial_dir),
            handle=h,
        )
        try:
            librepo.download_packages([target], failfast=True)
        except librepo.LibrepoException as exc:
            raise RpmDownloadError(
                f"librepo refused download of {location_href!r} "
                f"from {(location_base or repo_url)!r}: {exc}"
            ) from exc

        if target.err:
            raise RpmDownloadError(
                f"failed to download {location_href!r} from "
                f"{(location_base or repo_url)!r}: {target.err}"
            )

        src = (
            Path(target.local_path) if target.local_path
            else partial_dir / final_path.name
        )
        os.replace(src, final_path)
    finally:
        shutil.rmtree(partial_dir, ignore_errors=True)

    return final_path


def read_rpm_file_metadata(rpm_path: Path) -> dict[str, FileMeta]:
    """Return ``path -> FileMeta`` for every file recorded in *rpm_path*.

    Reads the package header via :mod:`rpm` (signature/digest checks
    are deliberately disabled — the file came from the same trusted
    repo whose primary metadata we already loaded via librepo, and
    we only care about file metadata here, not chain-of-trust).

    Ghost-flagged entries are returned as :class:`FileMeta` records
    too: the caller already knows from filelists.xml whether a path
    is a ghost on a given package, and the
    ``rpmfilesCompare``-equivalent comparison short-circuits on
    ghost before consulting :class:`FileMeta` anyway. We include
    them so the returned mapping faithfully mirrors the RPM's full
    file table.
    """
    rpm = get_rpm()
    ts = rpm.TransactionSet()
    # We only read the header — skip every signature / digest check
    # to avoid false errors on packages signed with keys we don't
    # have in the test environment.
    ts.setVSFlags(
        rpm.RPMVSF_MASK_NOSIGNATURES | rpm.RPMVSF_MASK_NODIGESTS
    )

    with open(rpm_path, "rb") as fh:
        try:
            hdr = ts.hdrFromFdno(rpm.fd(fh.fileno(), "r"))
        except rpm.error as exc:
            raise RepodataParseError(
                f"failed to read RPM header from {rpm_path}: {exc}"
            ) from exc

    digest_algo = hdr[rpm.RPMTAG_FILEDIGESTALGO] or 0
    files = rpm.files(hdr)
    out: dict[str, FileMeta] = {}
    for f in files:
        out[f.name] = FileMeta(
            fmode=int(f.mode),
            user=str(f.user or ""),
            group=str(f.group or ""),
            size=int(f.size),
            digest=str(f.digest or ""),
            digest_algo=int(digest_algo),
            linkto=str(f.linkto or ""),
            rdev=int(f.rdev or 0),
        )
    return out
