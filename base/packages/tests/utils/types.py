# SPDX-License-Identifier: MIT
"""Shared dataclasses used by fixtures, the metadata service, and tests.

Tests import these to type-annotate fixture results. They never construct
these directly — that's the metadata service's job.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

RepoKind = Literal["binary", "srpm", "debuginfo"]
ALL_REPO_KINDS: tuple[RepoKind, ...] = ("binary", "srpm", "debuginfo")


@dataclass(frozen=True)
class NEVRA:
    """Name-Epoch-Version-Release-Arch tuple. Hashable so it can be used in sets/dicts."""

    name: str
    epoch: int
    version: str
    release: str
    arch: str

    def __str__(self) -> str:
        if self.epoch:
            return f"{self.name}-{self.epoch}:{self.version}-{self.release}.{self.arch}"
        return f"{self.name}-{self.version}-{self.release}.{self.arch}"


@dataclass(frozen=True)
class FileEntry:
    """A single file (or dir) entry from a package's filelist."""

    path: str
    is_directory: bool = False
    is_ghost: bool = False
    """True iff RPM marked the entry as ``%ghost`` — the package claims
    the path but does not actually install the file. Multiple packages
    may legitimately ``%ghost`` the same path (this is the canonical
    mechanism for non-conflicting shared file ownership)."""


@dataclass(frozen=True)
class FileMeta:
    """Per-file attributes RPM compares when deciding whether two
    packages owning the same path actually conflict.

    Mirrors the inputs to ``rpmfilesCompare`` (``lib/rpmfi.cc``). The
    rules — quoted from RPM's own implementation — are:

    * Either side ``%ghost`` → never a conflict.
    * Modes must match exactly, *except* when both entries are
      symlinks (``LINK`` mode bits are deliberately ignored).
    * ``user`` / ``group`` must match.
    * For ``REG`` / ``LINK``: ``size`` must match.
    * For ``REG``: ``digest`` must match (with the same ``digest_algo``).
    * For ``LINK``: ``linkto`` must match.
    * For ``CDEV`` / ``BDEV``: ``rdev`` must match.

    Anything else is a conflict.

    *digest_algo* is the libgcrypt-style numeric algo id RPM stamps
    on the package via ``RPMTAG_FILEDIGESTALGO`` (e.g. ``8`` for
    SHA-256). RPM refuses to compare digests across different algos
    even when the digest bytes happen to be the same length.

    *fmode* is the full mode value (with the ``S_IFMT`` type bits
    intact) so consumers can re-derive the file type without
    importing :mod:`stat` themselves.
    """

    fmode: int
    user: str
    group: str
    size: int
    digest: str = ""
    digest_algo: int = 0
    linkto: str = ""
    rdev: int = 0


@dataclass(frozen=True)
class ConflictEntry:
    """A single ``Conflicts:`` entry parsed from primary repodata.

    *flags* is the dnf-style operator string (``EQ``, ``LT``, ``LE``,
    ``GT``, ``GE``) when the conflict is versioned, or ``None`` for a
    bare ``Conflicts: <name>`` with no version constraint. *epoch*,
    *version*, and *release* are populated only when the conflict
    declares them; consumers that don't need version-aware matching
    can use :attr:`name` alone.
    """

    name: str
    flags: str | None = None
    epoch: int | None = None
    version: str | None = None
    release: str | None = None

    @property
    def is_versioned(self) -> bool:
        """True iff this conflict declares any version constraint."""
        return self.flags is not None or self.version is not None


@dataclass(frozen=True)
class ProvidesEntry:
    """A single ``Provides:`` entry parsed from primary repodata.

    Mirrors :class:`ConflictEntry` — ``flags`` is the dnf-style
    operator string (``EQ`` is the only one RPM emits for provides in
    practice) when the provide carries a version, or ``None`` for a
    bare ``Provides: <name>``. *epoch*, *version*, *release* are
    populated only when present.

    RPM auto-emits a versioned provide of the package's own name+EVR
    (``Provides: <name> = E:V-R``); :func:`utils.repodata` ensures
    this is always present even when createrepo somehow omits it.
    """

    name: str
    flags: str | None = None
    epoch: int | None = None
    version: str | None = None
    release: str | None = None

    @property
    def is_versioned(self) -> bool:
        """True iff this provide carries a version."""
        return self.flags is not None or self.version is not None


@dataclass
class Package:
    """Rich package record sourced from primary repodata.

    The ``files`` attribute is populated lazily — primary metadata only
    contains a small subset of files (those marked "primary" by
    createrepo). Full file listings come from filelists metadata and
    are surfaced through the ``cross_repo_file_index`` fixture, not
    through this attribute.

    *location_href* and *location_base* are the repo-relative path
    and (optional) override base URL emitted by createrepo into
    ``primary.xml``. Together with the parent :class:`Repo`'s
    ``url`` they let consumers reconstruct the package's download
    URL, which the file-conflicts test uses to fetch RPMs on demand
    for ``rpmfilesCompare``-equivalent metadata extraction.
    """

    nevra: NEVRA
    vendor: str | None
    sourcerpm: str | None
    summary: str | None = None
    provides: list[ProvidesEntry] = field(default_factory=list)
    conflicts: list[ConflictEntry] = field(default_factory=list)
    files: list[FileEntry] = field(default_factory=list)
    location_href: str | None = None
    location_base: str | None = None

    @property
    def name(self) -> str:
        return self.nevra.name

    @property
    def arch(self) -> str:
        return self.nevra.arch

    @property
    def is_source(self) -> bool:
        """True if this is a source RPM (arch is ``src`` or ``nosrc``)."""
        return self.nevra.arch in ("src", "nosrc")

    @property
    def provide_names(self) -> list[str]:
        """The bare names of all ``Provides:`` entries.

        Provided for callers that don't care about version constraints
        (e.g., name-only virtual-provide checks). Callers that need
        version-aware matching should iterate :attr:`provides`
        directly.
        """
        return [p.name for p in self.provides]

    @property
    def conflict_names(self) -> list[str]:
        """The bare names of all ``Conflicts:`` entries.

        Provided for callers that don't care about version constraints
        (e.g., the cross-repo duplicate-name check). Callers that need
        version-aware matching should iterate :attr:`conflicts`
        directly.
        """
        return [c.name for c in self.conflicts]


@dataclass(frozen=True)
class FileOwner:
    """An owner of a file path in the cross-repo file index."""

    nevra: NEVRA
    repo_name: str
    is_directory: bool
    is_ghost: bool = False


@dataclass
class RepoclosureResult:
    """Outcome of an in-process repoclosure run against a target repo set."""

    target_repo_names: tuple[str, ...]
    arch: str
    unresolved: dict[NEVRA, list[str]] = field(default_factory=dict)
    repos_by_nevra: dict[NEVRA, str] = field(default_factory=dict)
    """Per-NEVRA source repo. Populated by
    :meth:`utils.repoclosure.Repoclosure.run` from
    ``libdnf5.rpm.Package.get_repo_id`` so failure messages can name
    which repo each unresolved consumer came from."""

    @property
    def success(self) -> bool:
        return not self.unresolved

    def __str__(self) -> str:
        if self.success:
            return (
                f"repoclosure OK for [{', '.join(self.target_repo_names)}] "
                f"on {self.arch}"
            )
        lines = [
            f"repoclosure FAILED for [{', '.join(self.target_repo_names)}] "
            f"on {self.arch}: {len(self.unresolved)} package(s) "
            "with unresolved deps:"
        ]
        for nevra, missing in sorted(self.unresolved.items(), key=lambda x: str(x[0])):
            repo = self.repos_by_nevra.get(nevra)
            suffix = f" (from {repo!r})" if repo else ""
            lines.append(f"  {nevra}{suffix}:")
            for dep in missing:
                lines.append(f"    - {dep}")
        return "\n".join(lines)
