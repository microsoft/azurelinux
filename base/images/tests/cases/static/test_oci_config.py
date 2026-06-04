# SPDX-License-Identifier: MIT
"""OCI image-config validation (container images).

Shared test (not under a ``cases/<family>/`` directory) so it applies to
every container image family — both ``core`` (container-base) and the
``distroless-*`` variants. Gated on the ``container`` capability via
``@pytest.mark.require_capability`` so it only runs for container images
(VM images, which declare ``container = false``, are skipped).
"""

from __future__ import annotations

import pytest


@pytest.mark.require_capability("container")
def test_no_explicit_config_user(oci_image_config: dict[str, object]) -> None:
    """OCI ``Config.User`` must be unset.

    Azure Linux base/distroless images intentionally leave ``Config.User``
    unset (matching AZL 3.0 and mainstream base images such as Debian,
    Ubuntu, Alpine, UBI, Fedora). The OCI runtime default for an unset
    user is uid 0, so this does not change effective runtime behavior, but
    explicitly declaring a user diverges from that convention. An explicit
    empty string still counts as "set" and must therefore also fail.
    """
    config = oci_image_config.get("config")
    assert isinstance(config, dict), (
        f"OCI image config has no 'config' object (got {type(config).__name__}); "
        f"cannot validate Config.User. Full inspect output: {oci_image_config!r}"
    )
    assert "User" not in config, (
        "OCI Config.User must be unset, but the image explicitly declares "
        f"User={config['User']!r}. Remove the user attribute from the kiwi "
        "<containerconfig> so the published manifest leaves Config.User unset."
    )
