## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without tests

%{!?python3_pkgversion:%global python3_pkgversion 3}

%global srcname cryptography

Name:           python-%{srcname}
Version:        45.0.4
Release:        %autorelease
Summary:        PyCA's cryptography library

# cryptography is dual licensed under the Apache-2.0 and BSD-3-Clause,
# as well as the Python Software Foundation license for the OS random
# engine derived by CPython.
# Rust crate dependency licenses:
# Apache-2.0
# Apache-2.0 OR MIT
# BSD-3-Clause
# MIT
# MIT OR Apache-2.0
License:        (Apache-2.0 OR BSD-3-Clause) AND PSF-2.0 AND Apache-2.0 AND BSD-3-Clause AND MIT AND (MIT OR Apache-2.0)
URL:            https://cryptography.io/en/latest/
Source0:        https://github.com/pyca/cryptography/archive/%{version}/%{srcname}-%{version}.tar.gz
                # created by ./vendor_rust.py helper script
Source1:        cryptography-%{version}-vendor.tar.bz2
Source2:        conftest-skipper.py

ExclusiveArch:  %{rust_arches}

BuildRequires:  openssl-devel
BuildRequires:  gcc
BuildRequires:  gnupg2
%if 0%{?fedora}
BuildRequires:  rust-packaging
%else
BuildRequires:  rust-toolset
%endif

BuildRequires:  python%{python3_pkgversion}-cffi >= 1.12
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-setuptools-rust >= 0.11.4

%if %{with tests}
%if 0%{?fedora}
BuildRequires:  python%{python3_pkgversion}-certifi
BuildRequires:  python%{python3_pkgversion}-hypothesis >= 1.11.4
BuildRequires:  python%{python3_pkgversion}-iso8601
BuildRequires:  python%{python3_pkgversion}-pretend
BuildRequires:  python%{python3_pkgversion}-pytest-benchmark
BuildRequires:  python%{python3_pkgversion}-pytest-xdist
BuildRequires:  python%{python3_pkgversion}-pytz
%endif
BuildRequires:  python%{python3_pkgversion}-pytest >= 6.2.0
%endif

%description
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%package -n  python%{python3_pkgversion}-%{srcname}
Summary:        PyCA's cryptography library
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

Requires:       openssl-libs
%if 0%{?fedora} >= 35 || 0%{?rhel} >= 9
# Can be safely removed in Fedora 37
Obsoletes: python%{python3_pkgversion}-cryptography-vectors < 3.4.7
%endif

%description -n python%{python3_pkgversion}-%{srcname}
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%prep
%autosetup -p1 %{!?fedora:-a1} -n %{srcname}-%{version}
%if 0%{?fedora}
%cargo_prep
sed -i 's/locked = true//g' pyproject.toml
%else
# RHEL: use vendored Rust crates
%cargo_prep -v vendor
%endif

%if ! 0%{?fedora}
sed -i 's,--benchmark-disable,,' pyproject.toml
%endif


%generate_buildrequires
%pyproject_buildrequires
%if 0%{?fedora}
# Fedora: use RPMified crates
%cargo_generate_buildrequires
%endif


%build
export RUSTFLAGS="%build_rustflags"
export OPENSSL_NO_VENDOR=1
export CFLAGS="${CFLAGS} -DOPENSSL_NO_ENGINE=1 "
%pyproject_wheel

%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%if ! 0%{?fedora}
%cargo_vendor_manifest
%endif


%install
# Actually other *.c and *.h are appropriate
# see https://github.com/pyca/cryptography/issues/1463
find . -name .keep -print -delete
find . -name Cargo.toml -print -delete
%pyproject_install
%pyproject_save_files %{srcname}


%check
%if %{with tests}
%if 0%{?rhel}
# skip benchmark, hypothesis, and pytz tests on RHEL
rm -rf tests/bench tests/hypothesis
# append skipper to skip iso8601 and pretend tests
cat < %{SOURCE2} >> tests/conftest.py
%endif

# enable SHA-1 signatures for RSA tests
# also see https://github.com/pyca/cryptography/pull/6931 and rhbz#2060343
export OPENSSL_ENABLE_SHA1_SIGNATURES=yes

# see https://github.com/pyca/cryptography/issues/4885 and
# see https://bugzilla.redhat.com/show_bug.cgi?id=1761194 for deselected tests
# see rhbz#2042413 for memleak. It's unstable under Python 3.11 and makes
# not much sense for downstream testing.
# see rhbz#2171661 for test_load_invalid_ec_key_from_pem: error:030000CD:digital envelope routines::keymgmt export failure
PYTHONPATH=${PWD}/vectors:%{buildroot}%{python3_sitearch} \
    %{__python3} -m pytest \
    --ignore vendor \
    -k "not (test_buffer_protocol_alternate_modes or test_dh_parameters_supported or test_load_ecdsa_no_named_curve or test_decrypt_invalid_decrypt or test_openssl_memleak or test_load_invalid_ec_key_from_pem)"
%endif


%files -n python%{python3_pkgversion}-%{srcname} -f %{pyproject_files}
%doc README.rst docs
%license LICENSE LICENSE.APACHE LICENSE.BSD
%license LICENSE.dependencies
%if ! 0%{?fedora}
%license cargo-vendor.txt
%endif


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 45.0.4-2
- test: add initial lock files

* Wed Jun 11 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 45.0.4-1
- Update to v45.0.4

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 45.0.3-3
- Rebuilt for Python 3.14

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 45.0.3-2
- Bootstrap for Python 3.14

* Sun May 25 2025 Jeremy Cline <jeremy@jcline.org> - 45.0.3-1
- Update to v45.0.3

* Mon May 19 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 45.0.2-1
- Update to v45.0.2

* Thu Mar 06 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 44.0.0-5
- Modernize Rust macro usage

* Tue Mar 04 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 44.0.0-4
- Do not delete tests/x509 on RHEL

* Thu Feb 06 2025 Fabio Valentini <decathorpe@gmail.com> - 44.0.0-3
- Rebuild for openssl crate >= v0.10.70 (RUSTSEC-2025-0004)

* Tue Jan 21 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 44.0.0-1
- Update to v44.0.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 43.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Francisco Trivino <ftrivino@redhat.com> - 43.0.0-3
- allow sha1 in OAEP

* Wed Jul 24 2024 Jeremy Cline <jeremycline@linux.microsoft.com> - 43.0.0-1
- Update to v43.0.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 42.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 12 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 42.0.8-6
- Remove unused pytest-subtests dependency

* Fri Jul 12 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 42.0.8-5
- Skip benchmark tests on RHEL

* Wed Jul 03 2024 Jeremy Cline <jeremycline@linux.microsoft.com> - 42.0.8-4
- Fix the build for ELN

* Wed Jul 03 2024 Miro Hrončok <miro@hroncok.cz> - 42.0.8-3
- Drop unneeded dependency on tox

* Tue Jul 02 2024 Jeremy Cline <jeremycline@linux.microsoft.com> - 42.0.8-1
- Update to 42.0.8, fixes rhbz#2251816

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 41.0.7-3
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 41.0.7-2
- Bootstrap for Python 3.13

* Thu Feb 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 41.0.7-1
- Update to 41.0.7, fixes rhbz#2255351, CVE-2023-49083

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 41.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 41.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 01 2023 Fabio Valentini <decathorpe@gmail.com> - 41.0.5-2
- Rebuild for openssl crate >= v0.10.60 (RUSTSEC-2023-0044, RUSTSEC-2023-0072)

* Thu Oct 26 2023 Christian Heimes <cheimes@redhat.com> - 41.0.5-1
- Update to 41.0.5, resolves RHBZ#2239707

* Mon Aug 14 2023 Christian Heimes <cheimes@redhat.com> - 41.0.3-2
- Build with ouroboros 0.17, fixes rhbz#2214228 / RUSTSEC-2023-0042

* Wed Aug 09 2023 Christian Heimes <cheimes@redhat.com> - 41.0.3-1
- Update to 41.0.3, resolves rhbz#2211237
- Use pyo3 0.19

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 40.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Python Maint <python-maint@redhat.com> - 40.0.2-4
- Rebuilt for Python 3.12

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 40.0.2-3
- Bootstrap for Python 3.12

* Tue Jun 13 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 40.0.2-2
- Use vendored rust-pem in RHEL builds

* Tue Apr 18 2023 Christian Heimes <cheimes@redhat.com> - 40.0.2-1
- Update to 40.0.2, resolves rhbz#2181430

* Thu Mar 09 2023 Miro Hrončok <mhroncok@redhat.com> - 39.0.2-2
- Don't run tests requiring pytz on RHEL
- Don't try to run tests of vendored dependencies in %%check

* Sat Mar 04 2023 Christian Heimes <cheimes@redhat.com> - 39.0.2-1
- Update to 39.0.2, resolves rhbz#2124729

* Tue Feb 28 2023 Fabio Valentini <decathorpe@gmail.com> - 37.0.2-9
- Ensure correct compiler flags are used for Rust code.

* Wed Feb 22 2023 Christian Heimes <cheimes@redhat.com> - 37.0.2-8
- Fix CVE-2023-23931: Don't allow update_into to mutate immutable objects, resolves rhbz#2171820
- Fix FTBFS due to failing test_load_invalid_ec_key_from_pem and test_decrypt_invalid_decrypt, resolves rhbz#2171661

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 37.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 09 2022 Christian Heimes <cheimes@redhat.com> - 37.0.2-6
- Enable SHA1 signatures in test suite (ELN-only)

* Wed Aug 17 2022 Miro Hrončok <mhroncok@redhat.com> - 37.0.2-5
- Drop unused requirement of python3-six

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 37.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 37.0.2-3
- Rebuilt for Python 3.11

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 37.0.2-2
- Bootstrap for Python 3.11

* Thu May 05 2022 Christian Heimes <cheimes@redhat.com> - 37.0.2-1
- Update to 37.0.2, resolves rhbz#2078968

* Thu Jan 27 2022 Christian Heimes <cheimes@redhat.com> - 36.0.0-3
- Skip unstable memleak tests, resolves: RHBZ#2042413

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 36.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 22 2021 Christian Heimes <cheimes@redhat.com> - 36.0.0-1
- Update to 36.0.0, fixes RHBZ#2025347

* Thu Sep 30 2021 Christian Heimes <cheimes@redhat.com> - 35.0.0-2
- Require rust-asn1 >= 0.6.4

* Thu Sep 30 2021 Christian Heimes <cheimes@redhat.com> - 35.0-1
- Update to 35.0.0 (#2009117)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 3.4.7-6
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 10 2021 Stephen Gallagher <sgallagh@redhat.com> - 3.4.7-4
- Don't conditionalize Source: directives

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 3.4.7-3
- Rebuilt for Python 3.10

* Tue May 11 2021 Christian Heimes <cheimes@redhat.com> - 3.4.7-2
- Fix compatibility issue with Python 3.10. Enums now use same
  representation as on Python 3.9. (#1952522)
- Backport OpenSSL 3.0.0 compatibility patches.

* Wed Apr 21 2021 Christian Heimes <cheimes@redhat.com> - 3.4.7-1
- Update to 3.4.7
- Remove dependency on python-cryptography-vectors package and use vectors
  directly from Github source tar ball. (#1952024)

* Wed Mar 03 2021 Christian Heimes <cheimes@redhat.com> - 3.4.6-1
- Update to 3.4.6 (#1927044)

* Mon Feb 15 2021 Christian Heimes <cheimes@redhat.com> - 3.4.5-1
- Update to 3.4.5 (#1927044)

* Fri Feb 12 2021 Christian Heimes <cheimes@redhat.com> - 3.4.4-3
- Skip iso8601 and pretend tests on RHEL

* Fri Feb 12 2021 Christian Heimes <cheimes@redhat.com> - 3.4.4-2
- Provide RHEL build infrastructure

* Wed Feb 10 2021 Christian Heimes <cheimes@redhat.com> - 3.4.4-1
- Update to 3.4.4 (#1927044)

* Mon Feb 08 2021 Christian Heimes <cheimes@redhat.com> - 3.4.2-1
- Update to 3.4.2 (#1926339)
- Package no longer depends on Rust (#1926181)

* Mon Feb 08 2021 Fabio Valentini <decathorpe@gmail.com> - 3.4.1-2
- Use dynamically generated BuildRequires for PyO3 Rust module.
- Drop unnecessary CARGO_NET_OFFLINE environment variable.

* Sun Feb 07 2021 Christian Heimes <cheimes@redhat.com> - 3.4.1-1
- Update to 3.4.1 (#1925953)

* Sun Feb 07 2021 Christian Heimes <cheimes@redhat.com> - 3.4-2
- Add missing abi3 and pytest dependencies

* Sun Feb 07 2021 Christian Heimes <cheimes@redhat.com> - 3.4-1
- Update to 3.4 (#1925953)
- Remove Python 2 support
- Remove unused python-idna dependency
- Add Rust support

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 10 2020 Christian Heimes <cheimes@redhat.com> - 3.3.1-1
- Update to 3.3.1 (#1905756)

* Wed Oct 28 2020 Christian Heimes <cheimes@redhat.com> - 3.2.1-1
- Update to 3.2.1 (#1892153)

* Mon Oct 26 2020 Christian Heimes <cheimes@redhat.com> - 3.2-1
- Update to 3.2 (#1891378)

* Mon Sep 07 2020 Christian Heimes <cheimes@redhat.com> - 3.1-1
- Update to 3.1 (#1872978)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Christian Heimes <cheimes@redhat.com> - 3.0-1
- Update to 3.0 (#185897)

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 2.9-3
- Rebuilt for Python 3.9

* Tue May 12 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 2.9-2
- add source file verification

* Fri Apr 03 2020 Christian Heimes <cheimes@redhat.com> - 2.9-1
- Update to 2.9 (#1820348)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Christian Heimes <cheimes@redhat.com> - 2.8-2
- cryptography 2.8+ no longer depends on python-asn1crypto

* Thu Oct 17 2019 Christian Heimes <cheimes@redhat.com> - 2.8-1
- Update to 2.8
- Resolves: rhbz#1762779

* Sun Oct 13 2019 Christian Heimes <cheimes@redhat.com> - 2.7-3
- Skip unit tests that fail with OpenSSL 1.1.1.d
- Resolves: rhbz#1761194
- Fix and simplify Python 3 packaging

* Sat Oct 12 2019 Christian Heimes <cheimes@redhat.com> - 2.7-2
- Drop Python 2 package
- Resolves: rhbz#1761081

* Tue Sep 03 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 2.7-1
- Update to 2.7 (#1715680).

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 28 2019 Christian Heimes <cheimes@redhat.com> - 2.6.1-1
- New upstream release 2.6.1, resolves RHBZ#1683691

* Wed Feb 13 2019 Alfredo Moralejo <amoralej@redhat.com> - 2.5-1
- Updated to 2.5.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Christian Heimes <cheimes@redhat.com> - 2.3-2
- Use TLSv1.2 in test as workaround for RHBZ#1615143

* Wed Jul 18 2018 Christian Heimes <cheimes@redhat.com> - 2.3-1
- New upstream release 2.3
- Fix AEAD tag truncation bug, RHBZ#1602752

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.2.1-2
- Rebuilt for Python 3.7

* Wed Mar 21 2018 Christian Heimes <cheimes@redhat.com> - 2.2.1-1
- New upstream release 2.2.1

* Sun Feb 18 2018 Christian Heimes <cheimes@redhat.com> - 2.1.4-1
- New upstream release 2.1.4

* Sun Feb 18 2018 Christian Heimes <cheimes@redhat.com> - 2.1.3-4
- Build requires gcc

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.1.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

## END: Generated by rpmautospec
