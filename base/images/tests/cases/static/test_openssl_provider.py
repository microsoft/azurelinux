# SPDX-License-Identifier: MIT
"""Validate each image's selected OpenSSL FIPS provider."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

_UPSTREAM_PROVIDER = "openssl-fips-provider"
_FIRST_PARTY_PROVIDER = "SymCrypt-OpenSSL"
_OPENSSL_LIBS_PACKAGE = "openssl-libs"
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
_REGISTRATION_DIRECTORY = "etc/pki/tls/azl-openssl-fips-provider.d"
_REGISTRATION_FILES = {
    _UPSTREAM_PROVIDER: {"openssl.cnf"},
    _FIRST_PARTY_PROVIDER: {"symcrypt.cnf"},
    None: set(),
}
_OPENSSL_LIBS_PATTERNS = (
    "lib*/libcrypto.so*",
    "lib*/libssl.so*",
    "usr/lib*/libcrypto.so*",
    "usr/lib*/libssl.so*",
)


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
    if expected is None:
        assert _OPENSSL_LIBS_PACKAGE not in installed_packages, (
            f"Image '{image_name}' has provider policy 'none' but contains "
            f"{_OPENSSL_LIBS_PACKAGE}"
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
    unexpected_openssl_libraries = (
        sorted(
            path.relative_to(rootfs).as_posix()
            for pattern in _OPENSSL_LIBS_PATTERNS
            for path in rootfs.glob(pattern)
        )
        if expected is None
        else []
    )
    registration_directory = rootfs / _REGISTRATION_DIRECTORY
    registrations = (
        {
            path.name
            for path in registration_directory.iterdir()
            if path.is_file() and path.name.lower().endswith(".cnf")
        }
        if registration_directory.is_dir()
        else set()
    )

    assert not missing, f"Image '{image_name}' is missing provider files: {missing}"
    assert not unexpected, f"Image '{image_name}' contains files from the wrong provider: {unexpected}"
    assert not unexpected_openssl_libraries, (
        f"Image '{image_name}' has provider policy 'none' but contains "
        f"OpenSSL libraries: {unexpected_openssl_libraries}"
    )
    assert registrations == _REGISTRATION_FILES[expected], (
        f"Image '{image_name}' has OpenSSL FIPS provider registrations "
        f"{sorted(registrations)}; expected {sorted(_REGISTRATION_FILES[expected])}"
    )
