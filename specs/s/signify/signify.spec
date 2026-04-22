# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:     signify
Version:  32
Release: 5%{?dist}
Summary:  Sign and verify signatures on files

# signify itself is ISC but uses other source codes, breakdown:
# Beerware: helper.c
# BSD-3-Clause: blf.h and blowfish.c and sha2.[ch]
# MIT: explicit_bzero.h
# LicenseRef-Fedora-Public-Domain: crypto_api.[ch] and explicit_bzero.c and
#                                  {fe,sc}25519.[ch] ge25519{.h,_base.data}
#                                  and mod_{ed,ge}25519.c
License:  ISC AND Beerware AND BSD-3-Clause AND MIT AND LicenseRef-Fedora-Public-Domain
URL:      https://github.com/aperezdc/%{name}
Source0:  %url/releases/download/v%{version}/%{name}-%{version}.tar.xz
Source1:  %url/releases/download/v%{version}/%{name}-%{version}.tar.xz.asc
Source2:  https://keys.openpgp.org/vks/v1/by-fingerprint/5AA3BC334FD7E3369E7C77B291C559DBE4C9123B

BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  make
BuildRequires:  pkgconfig(libbsd)
BuildRequires:  pkgconfig(libmd)

%description
The signify utility creates and verifies cryptographic signatures, as used
by the OpenBSD release maintainers.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1
# Remove upstream bundled optional libraries from source
rm -rf libbsd libwaive

%build
%set_build_flags
%make_build

%install
%make_install PREFIX=%{_prefix}

%check
make check

%files
%license COPYING
%doc CHANGELOG.md README.md
%{_bindir}/signify
%{_mandir}/man1/signify.*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Mar 09 2024 Robert Scheck <robert@fedoraproject.org> - 32-1
- Update to release v32 (#2268373)

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 24 2022 Robert Scheck <robert@fedoraproject.org> - 31-1
- Update to release v31

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Robert Scheck <robert@fedoraproject.org> - 30-6
- Spec file improvements by Robert-André Mauchin
  - Add tarball signature verification
  - Add patch to keep files timestamps
  - Rewrite summary (no encrypt)
  - Add Public Domain License
- Switch to upstream commit for keeping file timestamps

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Feb 28 2021 Marcus Müller <marcus@hostalia.de> - 30-3
- Fixed License tag
- rid of unescaped macros in %%changelog

* Wed Feb 24 2021 Marcus Müller <marcus@hostalia.de> - 30-2
- enable tests

* Wed Feb 24 2021 Marcus Müller <marcus@hostalia.de> - 30-1
- Bump upstream version
- Include the upstreamed license file
- Add newlines to changelog
- set LD explicitly (thanks sagitter)

* Sat Jan 11 2020 Marcus Müller <marcus@hostalia.de> - 27-2
- removed bundled library libwaive from source

* Fri Jan 10 2020 Marcus Müller <marcus@hostalia.de> - 27-1
- updated to release v27
- prepared `%%check` for as soon as regression tests are released
- fixed `%%set_build_flags` (thanks Antonio <anto.trande@gmail.com>)
- proper _prefix (thanks Vít Ondruch <vondruch@redhat.com>)

* Fri Nov 01 2019 Marcus Müller <marcus@hostalia.de> - 26-1
- Initial import
