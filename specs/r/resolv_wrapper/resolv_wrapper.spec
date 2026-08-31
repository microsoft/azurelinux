# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           resolv_wrapper
Version:        1.1.8
Release:        10%{?dist}

Summary:        A wrapper for dns name resolving or dns faking
License:        BSD-3-Clause
Url:            http://cwrap.org/

Source0:        https://ftp.samba.org/pub/cwrap/%{name}-%{version}.tar.gz
Source1:        https://ftp.samba.org/pub/cwrap/%{name}-%{version}.tar.gz.asc
Source2:        resolv_wrapper.keyring

Patch0:         resolv_wrapper-fix-cmocka-1.1.6+-support.patch

BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  cmake
BuildRequires:  libcmocka-devel
BuildRequires:  socket_wrapper

Recommends:     cmake
Recommends:     pkgconfig

%description
It is likely that if you have a server/client architecture, you need to do DNS
queries or a third party library, like Kerberos needs to be able to do queries.
In the case of Kerberos the client needs to look the address of the KDC up via a
SRV record. resolv_wrapper is able to either redirect all DNS queries to your
DNS server implementation, or fake DNS replies!

To use it set the following environment variables:

LD_PRELOAD=libresolv_wrapper.so
RESOLV_WRAPPER_CONF=./my_resolv.conf

This package doesn't have a devel package because this project is for
development/testing.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
%cmake \
  -DUNIT_TESTING=ON

%cmake_build

%install
%cmake_install

%ldconfig_scriptlets

%check
%ctest

LD_PRELOAD=%{__cmake_builddir}/src/libpam_wrapper.so bash -c '>/dev/null'

%files
%doc AUTHORS README.md CHANGELOG
%license LICENSE
%{_libdir}/libresolv_wrapper.so*
%dir %{_libdir}/cmake/resolv_wrapper
%{_libdir}/cmake/resolv_wrapper/resolv_wrapper-config-version.cmake
%{_libdir}/cmake/resolv_wrapper/resolv_wrapper-config.cmake
%{_libdir}/pkgconfig/resolv_wrapper.pc
%{_mandir}/man1/resolv_wrapper.1*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Mar 06 2023 Andreas Schneider <asn@redhat.com> - 1.1.8-4
- Update License to SPDX expression

* Mon Feb 27 2023 Andreas Schneider <asn@redhat.com> - 1.1.8-3
- Fix building with cmocka >= 1.1.6

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Andreas Schneider <asn@redhat.com> - 1.1.7-6
 - Update to version 1.1.8
   o https://gitlab.com/cwrap/resolv_wrapper/-/blob/resolv_wrapper-1.1.8/CHANGELOG

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 28 2022 Andreas Schneider <asn@redhat.com> - 1.1.7-4
- resolves: #2046942 - Fix detection of a fully seperate libresolv

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 19 2021 Andreas Schneider <asn@redhat.com> - 1.1.7-1
 - Update to version 1.1.7
   o https://gitlab.com/cwrap/resolv_wrapper/-/blob/resolv_wrapper-1.1.7/CHANGELOG

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Mar 24 2020 Andreas Schneider <asn@redhat.com> - 1.1.6-8
- Update to version 1.1.6
  * https://gitlab.com/cwrap/resolv_wrapper/-/blob/master/CHANGELOG

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Apr 24 2017 Jakub Hrozek <jhrozek@redhat.com> - 1.1.5-1
- Update to version 1.1.5
  * Support URI DNS records
  * Support PTR DNS records

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun 02 2016 Andreas Schneider <asn@redhat.com> - 1.1.4-1
- Update to version 1.1.4
  * Added support for faking NS entries
  * Fixed some platform compatibility bugs

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 02 2015 Andreas Schneider <asn@redhat.com> - 1.1.3-1
- Update to version 1.1.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 16 2014 Andreas Schneider <asn@redhat.com> - 1.1.0-2
- Add Requires for pkgconfig and cmake.

* Wed Dec 10 2014 Andreas Schneider <asn@redhat.com> - 1.1.0-1
- resolves: #1172534 - Initial package.
