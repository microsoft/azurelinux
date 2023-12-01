%define major 2
%define minor 10

Name:           cpprest
Version:        2.10.18
Release:        1%{?dist}
Summary:        C++ REST library
Group:          Applications/File
License:        MIT
Url:            https://github.com/microsoft/cpprestsdk
Source0:        https://github.com/microsoft/cpprestsdk/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Disable outside, failing and sometimes failing tests
Patch1:         cpprest-2.10.17-disable-outside-and-failing-tests.patch
# Disable tests with long timeouts
Patch2:         cpprest-2.10.9-disable-tests-long-timeouts.patch
# Disable test extract_floating_point, which fails on ppc64le and aarch64
Patch3:         cpprest-2.10.9-disable-test-extract_floating_point.patch
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  boost-devel >= 1.55
BuildRequires:  cmake >= 3.1
BuildRequires:  websocketpp-devel
BuildRequires:  brotli-devel
BuildRequires:  openssl >= 1.0
BuildRequires:  zlib

%description
The C++ REST SDK is a Microsoft project for cloud-based client-server
communication in native code using a modern asynchronous C++ API design. This
project aims to help C++ developers connect to and interact with services.

Also known as Casablanca.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       boost-devel
Requires:       openssl

%description devel
The C++ REST SDK is a Microsoft project for cloud-based client-server
communication in native code using a modern asynchronous C++ API design. This
project aims to help C++ developers connect to and interact with services.

Development files.

%prep
%setup -n cpprestsdk-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
# Remove bundled sources of websocketpp
rm -r Release/libs
# Remove file ThirdPartyNotices.txt, which is associated to websocketpp
rm ThirdPartyNotices.txt

%build
cd Release
# -Wl,--as-needed
mkdir build.release
cd build.release
export CXXFLAGS="%{optflags} -Wl,--as-needed"
%cmake .. -DBUILD_SAMPLES=OFF -Wno-dev -DWERROR=OFF -DCMAKE_BUILD_TYPE=Release -DWERROR=OFF -DCPPREST_EXPORT_DIR=cmake/cpprestsdk -DCPPREST_EXCLUDE_BROTLI=OFF
make %{?_smp_mflags}

%install
cd Release/build.release
%make_install

%check
# Run tests for the other buildArchs like x86_64, ppc64le, aarch64, i686, armv7hl
cd Release/build.release/Binaries
./test_runner *_test.so ||:

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc CONTRIBUTORS.txt
%license license.txt
%{_libdir}/libcpprest.so.%{major}.%{minor}

%files devel
%doc CONTRIBUTORS.txt
%{_includedir}/%{name}
%{_includedir}/pplx
%{_libdir}/libcpprest.so
%{_libdir}/cmake/cpprestsdk


%changelog
* Wed Jan 19 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 2.10.18-1
- Upgrade to 2.10.18

* Tue Dec 08 2020 Andrew Phelps <anphel@microsoft.com> - 2.10.14-6
- Remove -DBUILD_TESTS=OFF to allow running tests

* Sat Nov 21 2020 Olivia Crain <oliviacrain@microsoft.com> - 2.10.14-5
- Replace %%ldconfig_scriptlets with actual post/postun sections

* Tue Mar 31 2020 Paul Monson <paulmon@microsoft.com> 2.10.14-4
- Fix Source0 URL. License verified.

* Mon Dec 9 2019 Emre Girgin <mrgirgin@microsoft.com> 2.10.14-3
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.14-1
- New upstream version 2.10.14

* Fri May 31 2019 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.13-2
- cpprest-devel: Add boost-devel and pkgconfig(openssl) to "Requires"
  Fix #1715966

* Thu Apr 25 2019 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.13-1
- New upstream version 2.10.13
- Drop cpprest-2.10.12-fix_32bit_time_t.patch, fixed upstream

* Sat Mar 30 2019 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.12-3
- Add pkgconfig(zlib) to BR

* Fri Mar 29 2019 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.12-2
- Add cpprest-2.10.12-fix_32bit_time_t.patch

* Wed Mar 27 2019 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.12-1
- New upstream version 2.10.12

* Wed Mar 20 2019 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.11-1
- New upstream version 2.10.11

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.10-1
- New upstream version 2.10.10

* Tue Jan 29 2019 Jonathan Wakely <jwakely@redhat.com> - 2.10.9-3
- Rebuilt for Boost 1.69

* Mon Jan 28 2019 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.9-2
- Make tests non-fatal (for now).
  Reason: occasionally some tests are failing recently:
  'Unhandled exception: bind: Address already in use'
- Remove obsolete ldconfig scriptlets (Igor Gnatenko)

* Mon Jan 21 2019 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.9-1
- New upstream version 2.10.9
- Update patches to current code:
  cpprest-2.10.9-disable-outside-and-failing-tests.patch
  cpprest-2.10.9-disable-tests-long-timeouts.patch
  cpprest-2.10.9-disable-test-extract_floating_point.patch

* Thu Nov 15 2018 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.8-2
- Enable brotli HTTP compression
  add BR: pkgconfig(libbrotlidec), pkgconfig(libbrotlienc)
  add -DCPPREST_EXCLUDE_BROTLI=OFF to cmake

* Wed Nov 14 2018 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.8-1
- New upstream version

* Wed Oct 31 2018 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.7-1
- New upstream version
- Update -DCPPREST_EXPORT_DIR, because src/CMakeLists.txt uses
  CMAKE_INSTALL_LIBDIR now

* Thu Sep 13 2018 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.6-1
- New upstream version
- Since v2.10.0 the minimum required version of cmake is 3.1

* Sat Aug 18 2018 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.5-1
- New upstream version
- Remove cpprest-2.10.2-fix-libdir.patch
- Use -DCPPREST_EXPORT_DIR to install cmake files in correct path

* Sat Aug 04 2018 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.3-1
- New upstream version

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.2-3
- Fix #1589284 - Missing cmake files in cpprest-devel
- Add cpprest-2.10.2-fix-libdir.patch

* Fri Feb 16 2018 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.2-2
- Add BuildRequires: gcc-c++

* Mon Feb 12 2018 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.2-1
- New upstream version
- Update disable-outside-and-failing-tests.patch
- Remove cpprest-2.10.1-fix-warning-due-to-boost-1.66.patch

* Sun Feb 11 2018 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.1-4
- Rebuilt for Boost 1.66
- Added patch to fix warning due to boost 1.66
- Pass -DWERROR=OFF to cmake

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.10.1-2
- openssl-devel → pkgconfig(openssl)

* Tue Dec 19 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.1-1
- New upstream version

* Wed Oct 25 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.10.0-1
- New upstream version
- Fixed upstream, removed:
  cpprest-2.9.1-openssl-1.1.patch
  cpprest-2.9.1-asyncrt_utils_xlocale.patch
  Change end-of-line encoding to Unix (LF) of oauth1.cpp
  Remove spurious-executable-perm of oauth1.h and oauth1.cpp
- Updated patches:
  cpprest-2.10.0-disable-outside-and-failing-tests.patch
  cpprest-2.10.0-disable-tests-long-timeouts.patch
- Minimum required cmake version increased from 2.6 to 3.0
- Removed from cmake, because websocketpp is detected automatically now:
  -DCMAKE_INCLUDE_PATH=/usr/share/cmake/websocketpp/

* Fri Aug 18 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-21
- Updated cpprest-2.9.1-asyncrt_utils_xlocale.patch
  Remove condition fedora > 26 for this patch
- Cleanup spec file: Remove bundled sources of websocketpp.
  Use sed instead of dos2unix. Remove license file from devel package.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Jonathan Wakely <jwakely@redhat.com> - 2.9.1-18
- Rebuilt for s390x binutils bug

* Tue Jul 18 2017 Jonathan Wakely <jwakely@redhat.com> - 2.9.1-17
- Rebuilt for Boost 1.64

* Mon Jun 26 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-16
- Include and apply patch "cpprest-2.9.1-disable-test-extract_floating_point.patch" anyway.
  The condition for ppc64le aarch64 has been removed. Avoids missing patch file in SRPMS or
  rpmlint warning "ifarch-applied-patch" and possible ifarch related issues

* Mon Jun 26 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-15
- Do not run tests for ppc64 and s390x, because of many failing, even crashing tests

* Mon Jun 26 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-14
- Add patch for asyncrt_utils.h
  Change include xlocale.h to bits/types/locale_t.h for Fedora > 26, due to a change in glibc
- Disable test extract_floating_point, which fails on ppc64le and aarch64

* Wed Jun 07 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-13
- Add patch to disable tests with long timeouts, which fail in mock build

* Wed Jun 07 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-12
- Removed BR: gcc-c++
- Added check section and tests
- Add patch to disable outside/failing tests

* Mon May 29 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-11
- Explicitly require openssl-devel instead of pkgconfig(openssl), so we
  build against OpenSSL 1.1 on F26 and rawhide and not compat-openssl10.

* Wed May 24 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-10
- Apply cpprest-2.9.1-openssl-1.1.patch anyway, remove the condition
  fedora > 25, which is not needed

* Tue May 23 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-9
- Rebuild using websocketpp-0.7.0-5.fc26 for F26 and rawhide
- Rename patch file including version of cpprest
- Set license to MIT. This is the license of C++ REST SDK (license.txt).
  Websocket++ is a separate Fedora package (websocketpp-devel) and its
  license is handled there.
- Use BuildRequires: pkgconfig(openssl) instead of openssl-devel

* Thu May 18 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-8
- Rebuild for testing websocketpp-0.7.0-4.fc26

* Tue May 09 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-7
- Add requirement websocketpp-devel.
  Build against the Fedora websocketpp package and not the embedded version of cpprest.
- Add -DCMAKE_INCLUDE_PATH=/usr/share/cmake/websocketpp/ so that websocketpp is found
- Add patch cpprest-Fix-build-issue-with-openssl-1.1-From-Kurt-Roeckx

* Fri May 05 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-6
- Use directory build.release for cmake

* Sun Apr 30 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-5
- Fix unused-direct-shlib-dependency reported by rpmlint (installed packages)

* Sat Apr 29 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-4
- Updated spec file
- Remove spurious-executable-perm earlier in spec file (after setup)
- Change end-of-line encoding of two files to Unix (LF)

* Fri Apr 28 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-3
- Updated spec file
- Changed Source0 filename from v2.9.1.tar.gz to cpprest-2.9.1.tar.gz
- Convert ThirdPartyNotices.txt to utf-8

* Tue Apr 25 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-2
- Updated spec file according to package review feedback from:
  https://bugzilla.redhat.com/show_bug.cgi?id=1440704#c3

* Wed Apr 05 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-1
- Initial packaging
