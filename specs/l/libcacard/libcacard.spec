# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libcacard
Version:        2.8.1
Release: 13%{?dist}
Summary:        CAC (Common Access Card) library
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+
URL:            https://gitlab.freedesktop.org/spice/libcacard
Source0:        http://www.spice-space.org/download/libcacard/%{name}-%{version}.tar.xz
Source1:        http://www.spice-space.org/download/libcacard/%{name}-%{version}.tar.xz.sig
Source2:        gpgkey-A3DDE969.gpg
Source3:        db2.crypt
# https://gitlab.freedesktop.org/spice/libcacard/-/merge_requests/31
Patch1:         libcacard-2.8.1-sort-certificates.patch
Epoch:          3

BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  nss-devel
BuildRequires:  softhsm
BuildRequires:  opensc
BuildRequires:  gnutls-utils
BuildRequires:  nss-tools
BuildRequires:  openssl
BuildRequires:  gnupg2
BuildRequires:  meson
BuildRequires:  gcc-c++
BuildRequires:  pcsc-lite-devel
Conflicts:      qemu-common < 2:2.5.0

%description
This library provides emulation of smart cards to a virtual card
reader running in a guest virtual machine.

It implements DoD CAC standard with separate pki containers
(compatible coolkey), using certificates read from NSS.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%setup -q
%patch -P1 -p1
cp %{SOURCE3} tests/

%build
%meson
%meson_build

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

# Do not run the tests on s390x, which fails
%ifnarch s390x
%meson_test
%endif

%install
%meson_install

%ldconfig_scriptlets

%files
%license COPYING
%doc NEWS
%{_libdir}/libcacard.so.*

%files devel
%{_includedir}/cacard
%{_libdir}/libcacard.so
%{_libdir}/pkgconfig/libcacard.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.8.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.8.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep  2 2024 Miroslav Suchý <msuchy@redhat.com> - 3:2.8.1-10
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.8.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 18 2023 Jakub Jelen <jjelen@redhat.com> - 2.8.1-5
- Sort certificates by ID

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 16 2021 Jakub Jelen <jjelen@redhat.com> - 2.8.1-1
- New upstream release

* Mon Aug  2 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 3:2.8.0-5.20210801gitcf6121deb4
- Fix UNKNOWN pkg-config version, rhbz#1989031

* Sun Aug  1 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 3:2.8.0-4.20210801gitcf6121deb4
- Update to git snapshot v2.8.0.22
- Fix FTBFS rhbz#1987641

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Oct 06 2020 Jakub Jelen <jjelen@redhat.com> - 2.8.0-1
- New upstream release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 29 2019 Jakub Jelen <jjelen@redhat.com> - 2.7.0-3
- Backport an upstream patch to unbreak testing

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 31 2018 Christophe Fergeau <cfergeau@redhat.com> - 2.6.1-1
- Update to new upstream release

* Wed Aug  8 2018 Marc-André Lureau <marcandre.lureau@redhat.com> - 3:2.6.0-1
- Update to release v2.6.0
- remove vscclient, drop libcacard-tools

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 01 2017 Marc-André Lureau <marcandre.lureau@redhat.com> - 3:2.5.3-1
- new upstream release 2.5.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec  8 2015 Marc-André Lureau <marcandre.lureau@redhat.com> - 3:2.5.2-1
- Update to latest libcacard's release (2.5.2)

* Wed Nov 25 2015 Fabiano Fidêncio <fidencio@redhat.com> - 3:2.5.1-1
- Update to latest libcacard's release (2.5.1)

* Wed Sep 23 2015 Marc-André Lureau <marcandre.lureau@redhat.com> - 3:2.5.0-1
- Initial standalone libcacard package.
