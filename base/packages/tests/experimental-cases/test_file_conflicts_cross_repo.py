# SPDX-License-Identifier: MIT
"""Across all provided binary repos, distinct packages from *different
SRPMs* that own the same file path must not actually conflict at
RPM-install time.

The check is a two-pass refinement of the cross-repo file index:

1. **Repodata pass** (cheap, all packages). Build the full
   ``path -> [FileOwner]`` map from every binary repo's
   ``filelists.xml``. Skip dirs and ``%ghost`` entries; dedupe
   identical NEVRAs across repos.

2. **RPM-header pass** (lazy, only for candidate overlaps). For each
   surviving cross-SRPM, cross-name pair on a shared path, fetch
   both RPMs and compare per-file metadata using the same rules
   ``rpmfilesCompare`` (RPM's own ``lib/rpmfi.cc``) applies at
   install time. RPM permits two packages to own the same path iff
   **all** of these match between their file entries:

   * either side ``%ghost`` (already filtered above);
   * mode bits — except both being symlinks (``LINK`` mode is
     deliberately ignored by RPM);
   * owner (``user``) and group;
   * for ``REG`` / ``LINK``: ``size``;
   * for ``REG``: digest *and* digest algo;
   * for ``LINK``: ``linkto`` target;
   * for ``CDEV`` / ``BDEV``: ``rdev``.

   Anything else is reported as a real install-time conflict.

A pair declaring a ``Conflicts:`` that actually applies to the other
package is also accepted (the user has explicitly told RPM "we know
about each other"); see :func:`_are_marked_conflicting` and
:func:`_conflict_matches_target` for the exact rule. Either side
declaring the conflict is sufficient — RPM doesn't require it to be
mutual.

What gets filtered out *in this test* (because it's a different class
of finding):

* Same-SRPM same-arch sibling pairs. Two sub-packages produced by the
  same SRPM at the same arch are checked against each other by
  ``rpmbuild`` at build time; if they reach the published repo with
  overlapping files, that's an upstream packaging hygiene issue rather
  than the install-time conflict this test is meant to catch. We
  exempt these so the cross-SRPM signal isn't drowned out. A noarch
  sibling of an arch-specific sibling is *not* exempted because both
  do install simultaneously.

What counts as "marked as conflicting" (between two packages A and B):

* A's ``Conflicts:`` matches one of B's ``Provides:`` entries (or
  vice versa) under standard RPM provides/conflicts unification:

  - the names match,
  - if either side is unversioned the constraint is satisfied,
  - otherwise the provide's EVR satisfies the conflict's
    operator+EVR per :func:`rpm.labelCompare`.

  RPM auto-emits ``Provides: <name> = E:V-R`` for every package, so
  even pairs whose ``Conflicts:`` targets only the literal name
  (e.g. ``Conflicts: python3-sqlalchemy >= 2``) get evaluated
  against the other side's full NEVRA.

Both directions are checked; either side declaring the conflict is
sufficient — RPM doesn't require it to be mutual.

Known limitations
-----------------

* **Single-arch perspective.** The test runs once per ``(arch, repo
  set)`` pair, so we never compare an ``x86_64`` package against an
  ``aarch64`` package — that's by design (the install target is one
  arch at a time). Multilib coexistence (e.g. ``glibc.i686`` next to
  ``glibc.x86_64`` on an ``x86_64`` host) and RPM's
  ``handleColorConflict`` ELF-color override are also out of scope.
* **Boolean / rich dependencies are not modelled.** A
  ``Conflicts: (foo and bar)`` style entry is treated as a literal
  name lookup and will not match either operand's provides. RPM
  packages in this repo set use rich deps almost exclusively for
  ``Requires:`` rather than ``Conflicts:``, so the gap is mostly
  theoretical.
"""

from __future__ import annotations

import logging
import re
import stat

import pytest

from utils._dnf_stack import get_rpm
from utils.repos import Repo
from utils.types import ConflictEntry, FileMeta, NEVRA, Package, ProvidesEntry


logger = logging.getLogger(__name__)


# rules-as-code: paths where multiple owners are intentionally
# permitted (e.g. ``alternatives``-managed slots that escape the
# ghost-filter for whatever reason). Each entry's value is a short
# comment explaining why. Add new entries sparingly, and always with
# a justification.
PATH_ALLOWLIST: dict[str, str] = {
    # "/usr/bin/sendmail": "managed by alternatives across MTAs",
}


_SRPM_NAME_RE = re.compile(
    r"^(?P<name>.+)-(?P<ver>[^-]+)-(?P<rel>[^-]+)\.(?:src|nosrc)\.rpm$"
)


def _srpm_name_of(pkg: Package) -> str | None:
    """Extract the SRPM *name* from ``pkg.sourcerpm`` (e.g. ``foo``)."""
    if not pkg.sourcerpm:
        return None
    m = _SRPM_NAME_RE.match(pkg.sourcerpm)
    return m.group("name") if m else None


def _build_pkg_index(
    by_repo: dict[Repo, list[Package]]
) -> dict[NEVRA, Package]:
    """Map ``NEVRA`` -> :class:`Package`.

    Source RPMs are excluded; the file-conflicts test only operates on
    the binary side. If the same NEVRA appears in more than one binary
    repo (it shouldn't, but multilib pools occasionally race), the
    last writer wins — only the first three indexed attributes
    (``nevra``, ``conflicts``, ``provides``) are read by this test
    and they are identical across repos for a given NEVRA.
    """
    out: dict[NEVRA, Package] = {}
    for packages in by_repo.values():
        for pkg in packages:
            if pkg.is_source:
                continue
            out[pkg.nevra] = pkg
    return out


# Cache for the dnf-style flag string -> RPM sense bitmask mapping.
# Populated on first use because :mod:`rpm` is loaded lazily through
# the dnf-stack shim (it's a system package, not a venv import) and
# we want module import to stay cheap for ``--collect-only``.
_FLAG_TO_SENSE: dict[str, int] | None = None


def _flag_sense(flags: str) -> int:
    global _FLAG_TO_SENSE
    if _FLAG_TO_SENSE is None:
        rpm = get_rpm()
        _FLAG_TO_SENSE = {
            "EQ": rpm.RPMSENSE_EQUAL,
            "LT": rpm.RPMSENSE_LESS,
            "LE": rpm.RPMSENSE_LESS | rpm.RPMSENSE_EQUAL,
            "GT": rpm.RPMSENSE_GREATER,
            "GE": rpm.RPMSENSE_GREATER | rpm.RPMSENSE_EQUAL,
        }
    return _FLAG_TO_SENSE[flags]


def _evr_tuple(epoch, version: str | None, release: str | None) -> tuple[str, str, str]:
    """Build the ``(epoch, version, release)`` tuple ``rpm.labelCompare`` expects.

    Empty epoch is represented as ``""`` (which RPM treats as 0).
    """
    e = "" if epoch in (None, 0, "0", "") else str(epoch)
    return (e, version or "", release or "")


def _conflict_matches_provide(c: ConflictEntry, p: ProvidesEntry) -> bool:
    """Does conflict ``c`` (versioned or not) match provide ``p``?

    Standard RPM provides/conflicts unification:

    * Names must match.
    * If either side is unversioned, the constraint is satisfied
      (an unversioned ``Conflicts:`` matches any provide; an
      unversioned ``Provides:`` matches any conflict). This mirrors
      libsolv / rpm's "no version means any version" rule for the
      simple (non-rich) dependency form.
    * Otherwise compare the provide's EVR against the conflict's
      EVR with the conflict's operator via :func:`rpm.labelCompare`.
    """
    if c.name != p.name:
        return False
    if c.flags is None or p.flags is None:
        return True
    rpm = get_rpm()
    cflag = _flag_sense(c.flags)
    cmp = rpm.labelCompare(
        _evr_tuple(p.epoch, p.version, p.release),
        _evr_tuple(c.epoch, c.version, c.release),
    )
    if cmp < 0:
        return bool(cflag & rpm.RPMSENSE_LESS)
    if cmp > 0:
        return bool(cflag & rpm.RPMSENSE_GREATER)
    return bool(cflag & rpm.RPMSENSE_EQUAL)


def _conflict_matches_target(c: ConflictEntry, target: Package) -> bool:
    """Does the ``Conflicts:`` entry ``c`` actually apply to ``target``?

    Mirrors RPM's install-time evaluation: ``c`` matches ``target`` iff
    any of ``target``'s ``Provides:`` entries (which always include a
    versioned ``Provides: <name> = E:V-R`` for the package's own name,
    plus any explicit/virtual provides) satisfies ``c`` per
    :func:`_conflict_matches_provide`.
    """
    return any(_conflict_matches_provide(c, p) for p in target.provides)


def _rpmfiles_compatible(a: FileMeta, b: FileMeta) -> bool:
    """Return True iff RPM's ``rpmfilesCompare`` would accept ``a == b``.

    Mirrors ``int rpmfilesCompare(...)`` in RPM upstream
    (``lib/rpmfi.cc``). The C function returns 0 (== "no conflict")
    only when every applicable attribute matches; we return ``True``
    in the same cases.

    Ghost handling is *not* re-checked here — the cross-repo file
    index already strips ghost entries before they reach this
    function (see :class:`utils.metadata.MetadataService.build_file_index`).
    """
    a_what = stat.S_IFMT(a.fmode)
    b_what = stat.S_IFMT(b.fmode)

    # Mode difference is a conflict, except for symlink-vs-symlink.
    both_links = a_what == stat.S_IFLNK and b_what == stat.S_IFLNK
    if not both_links and a.fmode != b.fmode:
        return False

    # Owner / group must match for any file type.
    if a.user != b.user or a.group != b.group:
        return False

    # Type-specific: size (REG/LINK), digest (REG), linkto (LINK), rdev (CDEV/BDEV).
    if a_what in (stat.S_IFREG, stat.S_IFLNK):
        if a.size != b.size:
            return False

    if a_what == stat.S_IFLNK:
        # rpmfilesCompare allows null-vs-null on LINK target; both
        # being non-null and equal is the common case.
        if a.linkto != b.linkto:
            return False
    elif a_what == stat.S_IFREG:
        if not a.digest or not b.digest:
            # rpmfilesCompare treats a missing digest on either side
            # as "can't prove equality" -> conflict.
            return False
        if a.digest_algo != b.digest_algo:
            return False
        if a.digest != b.digest:
            return False
    elif a_what in (stat.S_IFCHR, stat.S_IFBLK):
        if a.rdev != b.rdev:
            return False

    # DIR / FIFO / SOCKET reach this point with everything we can
    # check having matched. RPM does not compare additional
    # attributes for them.
    return True


def test_file_conflicts_across_binary_repos(
    arch: str,
    binary_repos: list[Repo],
    all_binary_packages,
    cross_repo_file_index,
    package_file_metadata,
    subtests,
) -> None:
    if not binary_repos:
        pytest.fail(
            "misconfigured run: no binary --repo provided. This test "
            "validates a cross-repo invariant and is only meaningful "
            "with the full set of binary repos provided. Pass at least "
            "one --repo name=...,kind=binary,url=... — or use pytest -k "
            "/ --ignore to deselect this test if you intentionally want "
            "to skip it."
        )

    by_repo = all_binary_packages(arch)
    file_index = cross_repo_file_index(arch)

    pkg_by_nevra = _build_pkg_index(by_repo)

    def _are_marked_conflicting(a_nevra, b_nevra) -> bool:
        # Either side declaring a ``Conflicts:`` that actually applies
        # to the other package is sufficient — RPM doesn't require
        # the declaration to be mutual.
        #
        # Versioned conflicts are evaluated for real via
        # :func:`rpm.labelCompare` against the target package's NEVRA
        # (see :func:`_conflict_matches_target`); we no longer drop
        # the whole ranged form to "treat as no match", which used to
        # produce false positives for pairs like
        # ``python3-sqlalchemy`` (2.0.46) vs ``python3-sqlalchemy1.4``
        # (which declares ``Conflicts: python3-sqlalchemy >= 2``).
        a_pkg = pkg_by_nevra.get(a_nevra)
        b_pkg = pkg_by_nevra.get(b_nevra)
        if a_pkg is None or b_pkg is None:
            # Should not happen for binary packages we already iterated
            # — but if it does, fail safe and let the pair surface.
            return False
        for c in a_pkg.conflicts:
            if _conflict_matches_target(c, b_pkg):
                return True
        for c in b_pkg.conflicts:
            if _conflict_matches_target(c, a_pkg):
                return True
        return False

    def _same_srpm(a_nevra, b_nevra) -> bool:
        # Compare BOTH SRPM name AND arch. A noarch sub-package and an
        # arch-specific sub-package from the same SRPM can coexist on
        # one system, so a path overlap between them IS an install-time
        # conflict — even though they share an SRPM. Only true same-arch
        # siblings benefit from rpmbuild's build-time check.
        a_pkg = pkg_by_nevra.get(a_nevra)
        b_pkg = pkg_by_nevra.get(b_nevra)
        if a_pkg is None or b_pkg is None:
            return False
        sa = _srpm_name_of(a_pkg)
        sb = _srpm_name_of(b_pkg)
        if sa is None or sa != sb:
            return False
        return a_nevra.arch == b_nevra.arch

    # Per-NEVRA file-metadata cache populated lazily as the loop
    # discovers candidate overlaps. ``None`` is stored on download
    # failure so the same broken NEVRA is not retried on every path.
    files_by_nevra: dict[NEVRA, dict[str, FileMeta] | None] = {}

    def _files_for(nevra: NEVRA) -> dict[str, FileMeta] | None:
        cached = files_by_nevra.get(nevra, _MISSING)
        if cached is not _MISSING:
            return cached
        try:
            meta = package_file_metadata(arch, nevra)
        except Exception as exc:  # noqa: BLE001 — log + treat as opaque
            logger.warning(
                "could not load file metadata for %s: %s — falling back "
                "to reporting any overlap involving this package as a "
                "conflict",
                nevra, exc,
            )
            files_by_nevra[nevra] = None
            return None
        files_by_nevra[nevra] = meta
        return meta

    def _rpm_would_accept(a_nevra, b_nevra, path) -> bool:
        a_files = _files_for(a_nevra)
        b_files = _files_for(b_nevra)
        if a_files is None or b_files is None:
            # Be conservative: can't prove equivalence -> report.
            return False
        a_meta = a_files.get(path)
        b_meta = b_files.get(path)
        if a_meta is None or b_meta is None:
            # The cross-repo index said both packages own this path,
            # but we couldn't find it in one of their RPM headers.
            # That's a metadata mismatch worth surfacing — keep the
            # pair as a candidate.
            return False
        return _rpmfiles_compatible(a_meta, b_meta)

    # (name_a, repo_a, name_b, repo_b) -> list[paths]; the tuple is
    # always sorted so order is canonical regardless of which file
    # encountered the pair first.
    pair_to_paths: dict[tuple[str, str, str, str], list[str]] = {}

    for path, owners in sorted(file_index.items()):
        if len(owners) <= 1:
            continue
        if path in PATH_ALLOWLIST:
            continue

        # Same-name owners (different NEVRAs of the same name) are not
        # an install-time conflict — only one of them ends up installed.
        names = {o.nevra.name for o in owners}
        if len(names) <= 1:
            continue

        owner_list = sorted(owners, key=lambda o: o.nevra.name)
        for i in range(len(owner_list)):
            for j in range(i + 1, len(owner_list)):
                a = owner_list[i]
                b = owner_list[j]
                if a.nevra.name == b.nevra.name:
                    continue
                if _same_srpm(a.nevra, b.nevra):
                    continue
                if _are_marked_conflicting(a.nevra, b.nevra):
                    continue
                if _rpm_would_accept(a.nevra, b.nevra, path):
                    continue
                key = tuple(sorted(
                    [(a.nevra.name, a.repo_name), (b.nevra.name, b.repo_name)]
                ))
                flat: tuple[str, str, str, str] = (
                    key[0][0], key[0][1], key[1][0], key[1][1]  # type: ignore[index]
                )
                pair_to_paths.setdefault(flat, []).append(path)

    # Each offending package pair becomes its own subtest failure.
    # Sorted worst-first so the largest offenders surface first in
    # report output. Sample paths shown per subtest.
    for (name_a, repo_a, name_b, repo_b), paths in sorted(
        pair_to_paths.items(), key=lambda kv: (-len(kv[1]), kv[0])
    ):
        subtest_id = f"{name_a}-vs-{name_b}"
        with subtests.test(pair=subtest_id, arch=arch):
            sample = paths[:_SAMPLE_PATHS_PER_PAIR]
            more = len(paths) - len(sample)
            lines = [
                f"on {arch}: {name_a} (from {repo_a!r}) and "
                f"{name_b} (from {repo_b!r}) own {len(paths)} shared "
                "file path(s) without an applicable Conflicts: "
                "declaration on either side and with mismatched "
                "per-file metadata (rpmfilesCompare-equivalent). "
                f"Sample paths:",
            ]
            for p in sample:
                lines.append(f"  {p}")
            if more > 0:
                lines.append(f"  ... and {more} more")
            pytest.fail("\n".join(lines))


# How many sample paths to show per offending package pair in each
# subtest's failure message.
_SAMPLE_PATHS_PER_PAIR = 5

# Sentinel for the "not yet looked up" state in the per-NEVRA file
# metadata cache (``None`` already means "looked up and the lookup
# failed"; we need a distinct "never tried" value for ``dict.get``).
_MISSING = object()

