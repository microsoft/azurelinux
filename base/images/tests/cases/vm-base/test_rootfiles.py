# SPDX-License-Identifier: MIT
"""Verify the ``rootfiles`` package and root's shell startup files on VM images.

These tests assert that VM images ship ``rootfiles`` and that root will
receive a ``.bashrc`` which sources ``/etc/bashrc``, yielding the
expected ``[root@host ~]#`` prompt for non-login root shells (e.g.
``sudo su``) rather than a bare ``bash-x.y#`` fallback. This guards
against AB#20506, where ``rootfiles`` was dropped from ``vm-base.kiwi``.

Why the assertions target ``/usr/share/rootfiles`` and ``tmpfiles.d``
rather than ``/root/.bashrc`` directly: ``/root/.bashrc`` is a
``%ghost`` entry created at boot by ``systemd-tmpfiles`` from the
canonical copy under ``/usr/share/rootfiles/``. On an unbooted,
statically mounted image the ghost file may not exist yet, so we verify
the deterministic build-time evidence chain instead — the canonical
copy, the tmpfiles.d drop-in that provisions ``/root/.bashrc`` from it,
and ``/etc/bashrc`` itself — which together guarantee the runtime
outcome regardless of whether the ghost file has been materialized.

Path constants below are rootfs-relative (no leading slash) so they can
be joined with ``rootfs / CONST``; failure messages prepend ``/`` to
show the absolute on-image path. Do not add a leading slash to the
constants — ``Path("/abs")`` discards the ``rootfs`` prefix when joined.
"""

from __future__ import annotations

from pathlib import Path

import pytest

# Canonical copy that systemd-tmpfiles installs into /root/.bashrc at boot.
ROOTFILES_SKEL_BASHRC = "usr/share/rootfiles/.bashrc"
# tmpfiles.d drop-in whose `C /root/.bashrc ... /usr/share/rootfiles/.bashrc`
# directive provisions root's .bashrc on first boot.
TMPFILES_CONF = "usr/lib/tmpfiles.d/rootfiles.conf"
ROOT_BASHRC = "/root/.bashrc"
# Global bashrc (shipped by setup) that actually sets the root prompt.
ETC_BASHRC = "etc/bashrc"


def _non_comment_lines(text: str) -> list[str]:
    """Return stripped, non-blank, non-comment lines from a config file."""
    lines = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped and not stripped.startswith("#"):
            lines.append(stripped)
    return lines


# require_capability gates only the rpmdb-querying test below: the marker
# means "this image ships an rpmdb to query". The file-reading tests need
# no gate — they inspect the mounted rootfs directly.
@pytest.mark.require_capability("runtime-package-management")
def test_rootfiles_package_installed(installed_packages: set[str]) -> None:
    """The ``rootfiles`` package must ship in the VM image."""
    assert "rootfiles" in installed_packages, (
        "rootfiles package is not installed; root's shell startup files "
        "(/root/.bashrc et al.) will be missing"
    )


def test_root_skel_bashrc_sources_global_bashrc(rootfs: Path) -> None:
    """The canonical root ``.bashrc`` must source ``/etc/bashrc``.

    This is the copy ``systemd-tmpfiles`` installs into ``/root``;
    sourcing ``/etc/bashrc`` is what yields the proper prompt.
    """
    skel = rootfs / ROOTFILES_SKEL_BASHRC
    assert skel.is_file(), (
        f"/{ROOTFILES_SKEL_BASHRC} is missing; root has no .bashrc to receive"
    )
    sources_global = any("/etc/bashrc" in line for line in _non_comment_lines(skel.read_text()))
    assert sources_global, (
        f"/{ROOTFILES_SKEL_BASHRC} does not source /etc/bashrc; the root "
        "prompt regression would not be fixed"
    )


def test_tmpfiles_provisions_root_bashrc(rootfs: Path) -> None:
    """The tmpfiles.d drop-in must create ``/root/.bashrc`` at boot."""
    conf = rootfs / TMPFILES_CONF
    assert conf.is_file(), (
        f"/{TMPFILES_CONF} is missing, so /root/.bashrc will not be created at boot"
    )
    # tmpfiles.d format: <type> <path> ...; require an active directive
    # whose target path is /root/.bashrc (not just an incidental mention).
    provisions = any(
        len(fields) >= 2 and fields[1] == ROOT_BASHRC
        for fields in (line.split() for line in _non_comment_lines(conf.read_text()))
    )
    assert provisions, f"/{TMPFILES_CONF} has no directive that creates {ROOT_BASHRC}"


def test_global_bashrc_present(rootfs: Path) -> None:
    """``/etc/bashrc`` must exist — it is the file that sets the prompt."""
    etc_bashrc = rootfs / ETC_BASHRC
    assert etc_bashrc.is_file(), (
        f"/{ETC_BASHRC} is missing; sourcing it from root's .bashrc would be a no-op"
    )
