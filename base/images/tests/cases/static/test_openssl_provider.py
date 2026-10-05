# SPDX-License-Identifier: MIT
"""Validate each image's selected OpenSSL FIPS provider."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

_UPSTREAM_PROVIDER = "openssl-fips-provider"
_FIRST_PARTY_PROVIDER = "SymCrypt-OpenSSL"
_PROVIDER_PACKAGES = {_UPSTREAM_PROVIDER, _FIRST_PARTY_PROVIDER}
_PROVIDER_PROPERTY = "openssl-fips-provider"
_PROPERTY_TO_PACKAGE = {
    "upstream": _UPSTREAM_PROVIDER,
    "symcrypt": _FIRST_PARTY_PROVIDER,
    "none": None,
}

_UPSTREAM_PROVIDER_FILES = {
    "etc/pki/tls/azl-openssl-fips-provider.d/openssl.cnf",
    "etc/pki/tls/openssl.d/fipsmodule.cnf",
    "usr/lib64/ossl-modules/fips.so",
}
_FIRST_PARTY_PROVIDER_FILES = {
    "etc/pki/tls/azl-openssl-fips-provider.d/symcrypt.cnf",
    "etc/pki/tls/openssl.d/symcrypt_prov.cnf",
    "usr/lib64/ossl-modules/symcryptprovider.so",
}


def _expected_provider(image_name: str, properties: dict[str, str]) -> str | None:
    policy = properties.get(_PROVIDER_PROPERTY)
    if policy is None:
        pytest.fail(f"OpenSSL FIPS provider policy is not defined for image '{image_name}'")
    if policy not in _PROPERTY_TO_PACKAGE:
        pytest.fail(
            f"Image '{image_name}' has invalid {_PROVIDER_PROPERTY} policy '{policy}'; "
            f"expected one of {sorted(_PROPERTY_TO_PACKAGE)}"
        )
    return _PROPERTY_TO_PACKAGE[policy]


@pytest.mark.require_capability("runtime-package-management")
def test_selected_openssl_fips_provider_package(
    image_name: str | None,
    properties: dict[str, str],
    installed_packages: set[str],
) -> None:
    """Images with an RPM database contain exactly their selected provider."""
    assert image_name is not None, "--image-name is required to resolve OpenSSL FIPS provider policy"
    expected = _expected_provider(image_name, properties)
    installed_providers = installed_packages & _PROVIDER_PACKAGES
    expected_providers = {expected} if expected is not None else set()
    assert installed_providers == expected_providers, (
        f"Image '{image_name}' has OpenSSL FIPS providers {sorted(installed_providers)}; "
        f"expected {sorted(expected_providers)}"
    )


def test_selected_openssl_fips_provider_files(
    image_name: str | None,
    properties: dict[str, str],
    rootfs: Path,
) -> None:
    """Provider artifacts match policy, including images without an RPM database."""
    assert image_name is not None, "--image-name is required to resolve OpenSSL FIPS provider policy"
    expected = _expected_provider(image_name, properties)

    if expected == _UPSTREAM_PROVIDER:
        required = _UPSTREAM_PROVIDER_FILES
        forbidden = _FIRST_PARTY_PROVIDER_FILES
    elif expected == _FIRST_PARTY_PROVIDER:
        required = _FIRST_PARTY_PROVIDER_FILES
        forbidden = _UPSTREAM_PROVIDER_FILES
    else:
        required = set()
        forbidden = _UPSTREAM_PROVIDER_FILES | _FIRST_PARTY_PROVIDER_FILES

    missing = sorted(path for path in required if not (rootfs / path).is_file())
    unexpected = sorted(path for path in forbidden if (rootfs / path).exists())
    assert not missing, f"Image '{image_name}' is missing provider files: {missing}"
    assert not unexpected, f"Image '{image_name}' contains files from the wrong provider: {unexpected}"
