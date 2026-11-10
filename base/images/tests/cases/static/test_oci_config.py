# SPDX-License-Identifier: MIT
"""OCI image-config validation (container images).

Shared test (not under a ``cases/<family>/`` directory) so it applies to
every container image family — both ``core`` (container-base) and the
``distroless-*`` variants. Gated on the ``container`` capability via
``@pytest.mark.require_capability`` so it only runs for container images
(VM images, which declare ``container = false``, are skipped).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path


_WORKLOAD_USERS = {
    "container-busybox": "65534:65534",
    "container-nginx": "nginx",
    "container-postgres": "postgres",
    "container-telegraf": "telegraf",
    "container-python": "65534:65534",
    "container-nodejs": "65534:65534",
    "container-pytorch": "65534:65534",
}

_PACKAGE_MANAGEMENT_PATHS = (
    "usr/bin/dnf",
    "usr/bin/dnf5",
    "usr/bin/rpm",
    "etc/dnf",
    "etc/yum.repos.d",
    "usr/lib/sysimage/libdnf5",
    "usr/lib/sysimage/rpm",
    "var/lib/dnf",
    "var/lib/rpm",
)


@pytest.mark.require_capability("container")
def test_config_user_policy(
    oci_image_config: dict[str, object],
    image_name: str | None,
) -> None:
    """OCI ``Config.User`` must follow the image-family security policy.

    Azure Linux base/distroless images intentionally leave ``Config.User``
    unset (matching AZL 3.0 and mainstream base images such as Debian,
    Ubuntu, Alpine, UBI, Fedora). Workload images execute applications rather
    than serve as extensible bases, so they must declare a non-root user.
    """
    config = oci_image_config.get("config")
    assert isinstance(config, dict), (
        f"OCI image config has no 'config' object (got {type(config).__name__}); "
        f"cannot validate Config.User. Full inspect output: {oci_image_config!r}"
    )
    expected_user = _WORKLOAD_USERS.get(image_name or "")
    if expected_user is not None:
        assert config.get("User") == expected_user, (
            f"workload image {image_name!r} must declare Config.User={expected_user!r}, got {config.get('User')!r}"
        )
    else:
        assert "User" not in config, (
            f"OCI Config.User must be unset for base images, but the image explicitly declares User={config['User']!r}."
        )


@pytest.mark.require_capability("container")
def test_workload_package_management_removed(
    rootfs: Path,
    image_name: str | None,
) -> None:
    """Single-purpose workload images must not retain package-management tooling."""
    if image_name not in _WORKLOAD_USERS:
        pytest.skip("package-management removal is specific to workload images")

    retained = []
    for relative_path in _PACKAGE_MANAGEMENT_PATHS:
        path = rootfs / relative_path
        # Installing all BusyBox applets exposes rpm without retaining the RPM package.
        if (
            image_name == "container-busybox"
            and relative_path == "usr/bin/rpm"
            and path.is_symlink()
            and path.readlink().as_posix() == "/bin/busybox"
        ):
            continue
        if path.exists() or path.is_symlink():
            retained.append(path)
    assert not retained, f"workload image retained package-management paths: {retained!r}"


@pytest.mark.parametrize(
    ("image_name", "relative_path", "symlink_target", "allowed"),
    [
        ("container-busybox", "usr/bin/rpm", "/bin/busybox", True),
        ("container-busybox", "usr/bin/rpm", "/usr/bin/other", False),
        ("container-busybox", "usr/bin/rpm", None, False),
        ("container-nginx", "usr/bin/rpm", "/bin/busybox", False),
        ("container-busybox", "usr/lib/sysimage/rpm", None, False),
    ],
)
def test_workload_package_management_busybox_exception(
    tmp_path: Path,
    image_name: str,
    relative_path: str,
    symlink_target: str | None,
    *,
    allowed: bool,
) -> None:
    """Only the BusyBox image's rpm applet symlink is exempt from the tooling ban."""
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True)
    if symlink_target is None:
        path.touch()
    else:
        path.symlink_to(symlink_target)

    if allowed:
        test_workload_package_management_removed(tmp_path, image_name)
    else:
        with pytest.raises(AssertionError, match="retained package-management paths"):
            test_workload_package_management_removed(tmp_path, image_name)
