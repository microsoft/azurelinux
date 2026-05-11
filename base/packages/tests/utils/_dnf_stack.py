# SPDX-License-Identifier: MIT
"""Lazy loaders for the dnf-stack Python libraries.

Two concerns drive this module:

1. **`createrepo_c` triggers noisy librpm init at import.**
   The PyPI wheel bundles its own librpm. When that librpm initializes
   (which it does on first ``import createrepo_c``), it reads the
   host's ``/usr/lib/rpm/macros.d/`` files. Azure Linux hosts ship
   ``azurelinux-rpm-macros`` / ``forge-srpm-macros`` that define
   constructs (``%add_sysuser``, ``%constrain_build``,
   ``%cargo_feature_subpackage``, ...) that the bundled librpm cannot
   parse — librpm logs ``error: Macro %... has unterminated body``
   straight to stderr (fd 2). This is pure noise: we don't use any
   librpm functionality, only XML parsing. We swallow the noise by
   redirecting fd 2 to ``/dev/null`` for the duration of the import
   only, so any *real* parser errors during later use still surface.

2. **`librepo` / `libdnf5` / `rpm` are NOT pip-installable system packages.**
   Their PyPI presence is essentially nil; users must install
   ``python3-librepo`` / ``python3-libdnf5`` / ``python3-rpm`` via the
   system package manager. Importing them eagerly at module load
   time would break ``pytest --collect-only`` and ``pytest --help``
   whenever the system packages aren't visible to the active
   interpreter (e.g. when running inside a ``uv``-managed isolated
   venv, which has no equivalent of ``--system-site-packages``). We
   therefore lazy-import them at first use and surface a clear,
   actionable error message naming the system package to install.
"""

from __future__ import annotations

import os
from typing import Any

# ---------------------------------------------------------------------------
# createrepo_c — eager import, stderr suppressed during librpm init
# ---------------------------------------------------------------------------


def _import_createrepo_c() -> Any:
    """Import ``createrepo_c`` with fd 2 redirected to /dev/null.

    librpm initializes on first import and prints macro-parse warnings
    to stderr (fd 2) — none of which we care about because we only use
    createrepo_c's XML parsers. We only suppress during the import
    itself; real parser errors raised later still surface normally.
    """
    saved_fd = os.dup(2)
    devnull_fd = os.open(os.devnull, os.O_WRONLY)
    try:
        os.dup2(devnull_fd, 2)
        try:
            import createrepo_c as cr  # noqa: PLC0415 (intentional lazy import)
        except ImportError as exc:
            # Restore fd 2 before raising so the error is visible.
            os.dup2(saved_fd, 2)
            raise _missing_dep_error(
                "createrepo_c",
                pip_name="createrepo_c",
                purpose="parsing primary.xml / filelists.xml metadata",
            ) from exc
    finally:
        os.dup2(saved_fd, 2)
        os.close(devnull_fd)
        os.close(saved_fd)
    return cr


# Eagerly load createrepo_c at module import. It IS pip-installable
# (it ships as a manylinux wheel via this project's pyproject.toml),
# so any user with the project installed has it. The only reason this
# loader exists is the librpm-noise suppression above; loading once
# at import time keeps the suppression scope tight (a single fd dance
# rather than one per parser call).
cr = _import_createrepo_c()


# ---------------------------------------------------------------------------
# librepo — lazy, system package
# ---------------------------------------------------------------------------


def get_librepo() -> Any:
    """Import and return the ``librepo`` module, with a clear missing-dep error."""
    try:
        import librepo  # noqa: PLC0415 (intentional lazy import)
    except ImportError as exc:
        raise _missing_dep_error(
            "librepo",
            system_package="python3-librepo",
            purpose=(
                "fetching repomd.xml / primary.xml / filelists.xml from "
                "remote repositories"
            ),
        ) from exc
    return librepo


# ---------------------------------------------------------------------------
# rpm — lazy, system package
# ---------------------------------------------------------------------------


def get_rpm() -> Any:
    """Import and return the ``rpm`` module, with a clear missing-dep error.

    The :mod:`rpm` module ships with the system ``rpm`` package as
    ``python3-rpm`` (Fedora / Azure Linux / RHEL) or ``python3-rpm``
    (Debian / Ubuntu). It is NOT pip-installable: the bindings are
    tightly coupled to the host's ``librpm`` ABI, which is why every
    distro provides them through the system package manager rather
    than PyPI.

    We use it to parse per-file metadata (mode, owner, group, size,
    digest, linkto) from downloaded RPMs in
    :mod:`utils.repodata`. ``createrepo_c`` and ``libdnf5`` only
    expose the subset of file attributes that fit the createrepo XML
    schema (path + type + digest), which is not enough to mirror
    ``rpmfilesCompare`` semantics for the cross-repo file-conflicts
    test — that comparison is mode/owner/group/linkto-aware.
    """
    try:
        import rpm  # noqa: PLC0415 (intentional lazy import)
    except ImportError as exc:
        raise _missing_dep_error(
            "rpm",
            system_package="python3-rpm",
            purpose=(
                "parsing per-file metadata (mode, owner, group, size, "
                "digest, linkto) from downloaded RPMs to mirror RPM's "
                "own ``rpmfilesCompare`` rules in the cross-repo "
                "file-conflicts test"
            ),
        ) from exc
    return rpm


# ---------------------------------------------------------------------------
# libdnf5 — lazy, system package
# ---------------------------------------------------------------------------


def get_libdnf5() -> Any:
    """Import and return the ``libdnf5`` package, with a clear missing-dep error.

    Returns the top-level ``libdnf5`` package; submodules
    (``libdnf5.base``, ``libdnf5.rpm``, ``libdnf5.repo``,
    ``libdnf5.conf``) are accessed via attribute lookup. We
    deliberately import the umbrella package only so this loader stays
    a single-line probe; the consumer (:mod:`utils.repoclosure`) does
    its own ``import libdnf5.base`` etc. once it has confirmed the
    package is installed.
    """
    try:
        import libdnf5  # noqa: PLC0415 (intentional lazy import)
        # Submodule imports are what the consumer actually calls; do
        # them here so a partial install (umbrella present, submodules
        # missing) surfaces as the same "install python3-libdnf5"
        # error rather than a confusing AttributeError later.
        import libdnf5.base  # noqa: F401, PLC0415
        import libdnf5.conf  # noqa: F401, PLC0415
        import libdnf5.repo  # noqa: F401, PLC0415
        import libdnf5.rpm  # noqa: F401, PLC0415
    except ImportError as exc:
        raise _missing_dep_error(
            "libdnf5",
            system_package="python3-libdnf5",
            purpose=(
                "running repoclosure (libsolv-backed dependency "
                "evaluation, including rich/boolean deps)"
            ),
        ) from exc
    return libdnf5


# ---------------------------------------------------------------------------
# Error helper
# ---------------------------------------------------------------------------


class MissingDependencyError(ImportError):
    """Raised when one of the dnf-stack libraries is not importable.

    Subclass of :class:`ImportError` so existing ``except ImportError``
    blocks (including pytest's own collection diagnostics) handle it
    naturally. The message names the package to install so the user
    doesn't have to guess.
    """


def _missing_dep_error(
    module: str,
    *,
    system_package: str | None = None,
    pip_name: str | None = None,
    purpose: str = "",
) -> MissingDependencyError:
    """Build a clear, actionable missing-dependency error message."""
    lines = [
        f"the Python module {module!r} is required for {purpose} "
        f"but could not be imported."
    ]
    if system_package:
        lines.append(
            f"It is provided by your distribution's {system_package!r} "
            f"package (NOT pip-installable). Install via your system "
            f"package manager:\n"
            f"    dnf install {system_package}        # Fedora / AZL / RHEL\n"
            f"    apt install {system_package}        # Debian / Ubuntu"
        )
        lines.append(
            "If you are running inside a virtualenv, recreate it with "
            "system site-packages enabled so the system module is "
            "visible:\n"
            "    python -m venv --system-site-packages .venv\n"
            "    .venv/bin/pip install -e base/packages/tests\n"
            "Note: 'uv venv' / 'uv run' do NOT support "
            "--system-site-packages and therefore cannot see system "
            "modules; use the stdlib venv command shown above."
        )
    if pip_name:
        lines.append(f"It is normally provided by `pip install {pip_name}`.")
    return MissingDependencyError("\n\n".join(lines))
