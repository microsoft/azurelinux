Name:           nss_wrapper
Version:        1.1.15
Release:        1%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Mariner
License:        BSD
Summary:        A wrapper for the user, group and hosts NSS API
URL:            https://cwrap.org/
Source0:        https://ftp.samba.org/pub/cwrap/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  libcmocka-devel
BuildRequires:  perl-generators

Recommends:     cmake
Recommends:     pkgconfig

%description
There are projects which provide daemons needing to be able to create, modify
and delete Unix users. Or just switch user ids to interact with the system e.g.
a user space file server. To be able to test that you need the privilege to
modify the passwd and groups file. With nss_wrapper it is possible to define
your own passwd and groups file which will be used by software to act correctly
while under test.

If you have a client and server under test they normally use functions to
resolve network names to addresses (dns) or vice versa. The nss_wrappers allow
you to create a hosts file to setup name resolution for the addresses you use
with socket_wrapper.

To use it set the following environment variables:

LD_PRELOAD=libuid_wrapper.so
NSS_WRAPPER_PASSWD=/path/to/passwd
NSS_WRAPPER_GROUP=/path/to/group
NSS_WRAPPER_HOSTS=/path/to/host

This package doesn't have a devel package cause this project is for
development/testing.

%prep
%autosetup -p1

%build
if test ! -e "obj"; then
    mkdir obj
fi
pushd obj
%cmake \
  -DUNIT_TESTING=ON \
  %{_builddir}/%{name}-%{version}

make %{?_smp_mflags} VERBOSE=1
popd

%install
pushd obj
make DESTDIR=%{buildroot} install

sed -i '1 s|/usr/bin/env\ perl|/usr/bin/perl|' %{buildroot}%{_bindir}/nss_wrapper.pl

popd

%ldconfig_scriptlets

%check
pushd obj
ctest --output-on-failure
popd

%files
%doc AUTHORS README.md CHANGELOG
%license LICENSE
%{_bindir}/nss_wrapper.pl
%{_libdir}/libnss_wrapper.so*
%dir %{_libdir}/cmake/nss_wrapper
%{_libdir}/cmake/nss_wrapper/nss_wrapper-config-version.cmake
%{_libdir}/cmake/nss_wrapper/nss_wrapper-config.cmake
%{_libdir}/pkgconfig/nss_wrapper.pc
%{_mandir}/man1/nss_wrapper.1*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.15-1
- Auto-upgrade to 1.1.15 - Azure Linux 3.0 - package upgrades

* Mon Jul 25 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.1.12-1
- Bumping version to 1.1.12
- Remove gpg signature check.
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.11-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Apr 02 2020 Andreas Schneider <asn@redhat.com> - 1.1.11-1
- Update to version 1.1.11
  https://gitlab.com/cwrap/nss_wrapper/-/blob/master/CHANGELOG

* Mon Mar 16 2020 Andreas Schneider <asn@redhat.com> - 1.1.10-1
- Update to version 1.1.10
  https://gitlab.com/cwrap/nss_wrapper/-/blob/master/CHANGELOG

* Mon Mar 16 2020 Andreas Schneider <asn@redhat.com> - 1.1.9-1
- Update to version 1.1.9

* Mon Feb 17 2020 Andreas Schneider <asn@redhat.com> - 1.1.8-1
- Update to version 1.1.8
- resolves: #1799808

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 18 2019 Andreas Schneider <asn@redhat.com> - 1.1.7-3
- Fixed patch for pkg-config

* Mon Nov 18 2019 Andreas Schneider <asn@redhat.com> - 1.1.7-2
- resolves: #1772368 - Incorrect path in pkg-config file

* Wed Nov 13 2019 Andreas Schneider <asn@redhat.com> - 1.1.7-1
- Update to version 1.1.7

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 13 2018 Andreas Schneider <asn@redhat.com> - 1.1.5-1
- resolves: #1340724 - Use Recommends for cmake and pkgconfig

* Fri Nov 02 2018 Andreas Schneider <asn@redhat.com> - 1.1.5-1
- Update to version 1.1.5

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Mar 23 2016 Andreas Schneider <asn@redhat.com> - 1.1.3-1
- Update to version 1.1.3
  * Added support for BSD 'struct passwd' members
  * Replaced strcpy() with snprintf()
  * Fixed segfault while reloading hosts file
  * Fixed issue where are not fault tolerant if an alias has already
    been added
  * Fixed nss_wrapper build on Solaris

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 20 2015 Andreas Schneider <asn@redhat.com> - 1.1.0-1
- Update to version 1.1.0
  * Added support for initgroups()
  * Added support for shadow files (getspnam(), etc.)
  * Improved support for multi address handling in getaddrinfo()
  * Improved file parser
  * Fixed compilation on machines without IPv4 support
  * Fixed service string sanity check in getaddrinfo() (bso #11501)
  * Fixed AI_NUMERICHOST handling in getaddrinfo() (bso #11477)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec 15 2014 Michael Adam <madam@redhat.com> - 1.0.3-2
- Fix format of changelog entries.
- Require cmake.
- Don't own _libdir/pkgconfig, and require pkgconfig instead.

* Thu Sep 11 2014 Andreas Schneider <asn@redhat.com> - 1.0.3-1
- Update to version 1.0.3.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 09 2014 Andreas Schneider <asn@redhat.com> - 1.0.2-1
- Update to version 1.0.2.

* Fri Mar 14 2014 Andreas Schneider <asn@redhat.com> - 1.0.1-3
- resolves: #1075932 - Fix segfault in 'getent hosts'.

* Tue Feb 11 2014 Andreas Schneider <asn@redhat.com> - 1.0.1-2
- resolves: #1060906 - Fedora package.
- Remove Group
- Remove glibc-devel build requirement
- Do not create a subpackage.

* Tue Feb 04 2014 Andreas Schneider <asn@redhat.com> - 1.0.1-1
- Update to version 1.0.1
  * Added --libs to pkg-config.
  * Added nss_wrapper-config.cmake
  * Fixed a bug packaging the obj directory.

* Mon Feb 03 2014 Andreas Schneider <asn@redhat.com> - 1.0.0-1
- Initial version 1.0.0
