# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


#%%global dev rc1

Name:           civetweb
Summary:        Embedded C/C++ web server
Version:        1.16
Release:        16%{?dev:%{dev}}%{?dist}
License:        MIT
Url:            https://github.com/civetweb/civetweb
Source:         https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
#               Test framework files
Source:         https://github.com/civetweb/check/archive/master/civetweb-check-master.tar.gz

#               Patches based on commits in upstream's git repository
#               commit: e927db7979e07ca5ceb06a61889a69b733dc029d and
#                       08b7241f4bce808c3a932a5fddc1181acee5c0c1
Patch:          0001-CMakeLists.txt.patch
#               commit: 76e222bcb77ba8452e5da4e82ae6cecd499c25e0
Patch:          0002-src-civetweb.c.patch
#               commit: 782e18903515f43bafbf2e668994e82bdfa51133
Patch:          0003-src-civetweb.c.patch
#               commit: b20a7bc1bf70b66448bec6b68a61328766cd2e19
Patch:          0004-unittest-CMakeLists.txt.patch
#               commit: aa7de369a47903de2417e2a8bf5be1f3df2acd10
Patch:          0005-unittest-public_server.c.patch
#               Patches based on pull requests not yet merged
#               https://github.com/civetweb/civetweb/pull/1389
Patch:          0006-src-civetweb.c.patch
#               https://github.com/civetweb/civetweb/pull/1423
Patch:          0007-src-civetweb.c.patch
#               https://github.com/civetweb/civetweb/pull/1424
Patch:          0008-unittest-private.c.patch

BuildRequires:  cmake make gcc-c++
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

%description
Civetweb is an easy to use, powerful, C (C/C++) embeddable web server
with optional CGI, SSL and Lua support.

CivetWeb can be used by developers as a library, to add web server
functionality to an existing application. It can also be used by end
users as a stand-alone web server running on a Windows or Linux PC.
It is available as single executable, no installation is required.

%package devel
Summary:        Civetweb Client Library C and C++ header files
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Civetweb shared libs and associated header files

%prep
%autosetup -p1

%build
export CHECK_URL=%{SOURCE1}
%{cmake} . \
    -G "Unix Makefiles" \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DBUILD_CONFIG=rpmbuild \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DCIVETWEB_ENABLE_CXX:BOOL=ON \
    -DCIVETWEB_ENABLE_WEBSOCKETS:BOOL=ON \
    -DCIVETWEB_ENABLE_X_DOM_SOCKET:BOOL=ON \
    -DCIVETWEB_ENABLE_ZLIB:BOOL=ON \
    -DCIVETWEB_ENABLE_SSL_DYNAMIC_LOADING:BOOL=OFF \
    -DCIVETWEB_SSL_OPENSSL_API_1_1:BOOL=OFF \
    -DCIVETWEB_SSL_OPENSSL_API_3_0:BOOL=ON

export GCC_COLORS=
export VERBOSE=1
%cmake_build %{?_smp_mflags}

%install
%cmake_install
mkdir -p %{buildroot}%{_docdir}/civetweb

%check
# Compile cgi program used by tests
mkdir output
${CC:-gcc} ${CFLAGS:-} ${LDFLAGS:-} unittest/cgi_test.c -o output/cgi_test.cgi

# The tests use the same ports (8080 and 8443) and can therefore not
# be run in parallel
# The excluded client tests require external network and can not be
# run during a package build
%ctest -- -j1 -E 'test-publicserver-minimal-https?-client'

%files
%{_bindir}/civetweb
%{_libdir}/libcivetweb.so.*
%{_libdir}/libcivetweb-cpp.so.*
%license LICENSE.md
%doc README.md RELEASE_NOTES.md SECURITY.md

%files devel
%{_includedir}/*.h
%{_libdir}/libcivetweb.so
%{_libdir}/libcivetweb-cpp.so
%{_libdir}/cmake/civetweb/
%{_datadir}/pkgconfig/*

%changelog
* Thu Aug 20 2026 Mattias Ellert <mattias.ellert@physics.uu.se> - 1.16-16
- Link to openssl libraries instead of using runtime dynamic loading
- Use openssl 3.0 API instead of the default openssl 1.1 API
- Let the devel package own the cmake subdirectory
- Run tests in check

* Fri Aug 7 2026 Mattias Ellert <mattias.ellert@physics.uu.se> - 1.16-15
- Add upstream's fix to actually support X_DOM_SOCKET with cmake
- Enable ZLIB compression support
- rhbz#2512488

* Mon Jun 8 2026 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 1.16-14
- enable WEBSOCKETS and X_DOM_SOCKET as requested

* Thu Feb 19 2026 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 1.16-13
- civetweb 1.16, handle cmake-4 doesn't support cmake < 3.5
- upstream, civetweb-1.16+ has updated to minimum cmake-3.10, and there
  don't seem to be any adverse effects building civetweb with that change.
  And someday there might even be a civetweb-1.17.

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Sep 29 2025 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 1.16-10
- civetweb 1.16, rhbz 2400162-2400166

* Wed Sep 3 2025 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 1.16-9
- civetweb 1.16

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 1.16-7
- civetweb 1.16, rhbz#2380496

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 11 2023 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 1.16-1
- civetweb 1.16 GA

* Tue Mar 7 2023 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 1.15-1
- civetweb 1.15 GA, initial build

