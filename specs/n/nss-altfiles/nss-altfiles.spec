# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: NSS module to look up from files in /usr/lib as well
Name: nss-altfiles
Version: 2.23.0
Release: 8%{?dist}
Source0: https://github.com/flatcar/nss-altfiles/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch1: 0001-build-sys-Inherit-LDFLAGS.patch
# From https://github.com/flatcar/nss-altfiles/commit/de2b32289bf701ce3c8167a1b58436866922085e
Patch2: 0003-deprecate-RES_USE_INET6.patch
License: LGPL-2.1-or-later and MIT
URL: https://github.com/flatcar/nss-altfiles

BuildRequires: make
BuildRequires: glibc-devel
BuildRequires: gcc
BuildRequires: git

%description
When installed, this package allows looking up users in %{_prefix}/lib/passwd,
and from respective files for all other NSS maps.

%prep
%autosetup -Sgit

%build
./configure --with-types=all --prefix=%{_prefix} --libdir=%{_libdir} CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}"
%make_build

%install
%make_install

%files
%doc README.md
%{_libdir}/*.so.*

%ldconfig_scriptlets

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 20 2024 Timothée Ravier <tim@siosm.fr> - 2.23.0-4
- Fix macro expansion in description
- Use make macros: https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro
- Use SPDX identifiers for license: https://fedoraproject.org/wiki/Changes/SPDX_Licenses_Phase_3

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Jan Pazdziora <jpazdziora@redhat.com> - 2.23.0-1
- Rebase to 2.23.0 (fedora#2036375)
- Change upstream to https://github.com/flatcar/nss-altfiles
- Enable all maps (fedora#2036375)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Colin Walters <walters@verbum.org> - 2.18.1-13
- BR gcc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Ville Skyttä <ville.skytta@iki.fi> - 2.18.1-3
- Build with $RPM_OPT_FLAGS

* Tue Apr 08 2014 Colin Walters <walters@verbum.org>
- Revert patch to link to libc, causes a dep on GLIBC_PRIVATE

* Sat Mar 22 2014 Colin Walters <walters@verbum.org>
- Initial packaging
