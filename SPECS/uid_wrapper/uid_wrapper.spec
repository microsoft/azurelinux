Name:           uid_wrapper
Version:        1.3.0
Release:        1%{?dist}
Summary:        A wrapper for privilege separation
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://cwrap.org/
Source0:        https://ftp.samba.org/pub/cwrap/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  libcmocka-devel >= 1.1.0

Recommends:     cmake
Recommends:     pkgconfig

%description
Some projects like a file server need privilege separation to be able to switch
to the connection user and do file operations. uid_wrapper convincingly lies
to the application letting it believe it is operating as root and even
switching between UIDs and GIDs as needed.

To use it set the following environment variables:

LD_PRELOAD=libuid_wrapper.so
UID_WRAPPER=1

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
popd

%ldconfig_scriptlets

%check
pushd obj
make test || cat $(find Testing -name "*.log")
popd

%files
%doc AUTHORS README.md CHANGELOG
%license LICENSE
%{_libdir}/libuid_wrapper.so*
%dir %{_libdir}/cmake
%dir %{_libdir}/cmake/uid_wrapper
%{_libdir}/cmake/uid_wrapper/uid_wrapper-config-version.cmake
%{_libdir}/cmake/uid_wrapper/uid_wrapper-config.cmake
%dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/uid_wrapper.pc
%{_mandir}/man1/uid_wrapper.1*

%changelog
* Wed Jan 31 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.0-1
- Auto-upgrade to 1.3.0 in Mariner 3.0

* Mon Jul 25 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.2.9-1
- Bumping version to 1.2.9.
- Remove gpg signature check.
- Remove patches which are fixed in this version.
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.7-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Mar 03 2020 Anderson Sasaki <ansasaki@redhat.com> - 1.2.7-3
- Fix invalid library path in cmake configuration file (bz#1809275)

* Wed Feb 12 2020 Andreas Schneider <asn@redhat.com> - 1.2.7-2
- resolves: #1801869 - Fix invalid lib pkg-config lib path

* Tue Feb 11 2020 Andreas Schneider <asn@redhat.com> - 1.2.7-1
- Update to version 1.2.7
  * Fix unsetting initial XIDs
  * Fix manpage installation
  * Fix cmake-config installation
  * Fixed running with sanitizers
- resolves: #1690028 - Allow running without RTLD_DEEPBIND

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jul 31 2017 Andreas Schneider <asn@redhat.com> - 1.2.4-1
- Update to version 1.2.4
  * Added deadlock workaround for glibc < 2.24
  * Fixed a possible deadlock bug if uid_wrapper is turned off
  * Logging is always turned on now
  * Fixed a memory leak
  * Limited number of groups during fork+exec

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Andreas Schneider <asn@redhat.com> - 1.2.2-1
- Update to version 1.2.2:
  * Added support for fork'ed and then exec'ed processes
  * Added support for Alpha

* Tue Jun 27 2017 Nils Philippsen <nils@redhat.com> - 1.2.1-3
- drop requirements on cmake, pkgconfig and rather own the directories for the
  files augmenting these packages

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Mar 23 2016 Andreas Schneider <asn@redhat.com> - 1.2.1-1
- Update to version 1.2.1
  * Documented missing options.
  * Fixed a comipilation issue with -O3.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 29 2015 Andreas Schneider <asn@redhat.com> - 1.2.0-1
- Update to version 1.2.0
  * Added privilege checks for all set*uid and set*gid functions.
  * Added a lot more and accurate tests which work as root.
  * Fixed some minor issues

* Wed Sep 02 2015 Andreas Schneider <asn@redhat.com> - 1.1.1-1
- Update to version 1.1.1

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jan 21 2015 Andreas Schneider <asn@redhat.com> - 1.1.0-1
- Update to version 1.1.0

* Mon Dec 15 2014 Michael Adam <madam@redhat.com> - 1.0.2-5
- Fix format errors in changelog.
- Require cmake.
- Don't own _libdir/pkgconfig, and require pkgconfig instead.

* Thu Oct 02 2014 Andreas Schneider <asn@redhat.com> - 1.0.2-4
- resolves: #1146410 - Do not own /usr/lib64/cmake.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 04 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.0.2-2
- Handle lack of SYS_access on AArch64

* Thu Jul 31 2014 Andreas Schneider <asn@redhat.com> - 1.0.2-1
- Update to version 1.0.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 11 2014 Andreas Schneider <asn@redhat.com> - 1.0.1-3
- Fix some typos.
- resolves: #1060910 - Fedora import

* Tue Feb 11 2014 Andreas Schneider <asn@redhat.com> - 1.0.1-2
- Remove Group
- Remove glibc-devel build requirement
- Do not create a subpackage.

* Tue Feb 04 2014 Andreas Schneider <asn@redhat.com> - 1.0.1-1
- Update to version 1.0.1
  * Added --libs to pkg-config.
  * Added socket_wrapper-config.cmake
  * Fixed a bug packaging the obj directory.

* Mon Feb 03 2014 Andreas Schneider <asn@redhat.com> - 1.0.0-1
- Initial version 1.0.0
