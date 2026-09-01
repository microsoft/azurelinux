%bcond_without compat
%global compat_soname libminizip.so.1

# Compatible with the following minizip-compat version.
%global minizip_ver 1.2.13
# Obsoletes minizip versions less than.
%global minizip_obsoletes 1.3
# Old minizip-ng version before it was renamed to minizip-ng-compat
%global minizip_ng_ver 3.0.7
# Obsolete version of old minizip-ng
%global minizip_ng_obsoletes 3.0.7-5

Name:           minizip-ng
Version:        4.0.7
Release:        3%{?dist}
Summary:        Minizip-ng contrib in zlib-ng with the latest bug fixes and advanced features
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        Zlib
URL:            https://github.com/nmoinvaz/%{name}
Source0:        https://github.com/nmoinvaz/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: libbsd-devel
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: libzstd-devel
BuildRequires: xz-devel

%description
Minizip-ng zlib-ng contribution that includes:
* AES encryption
* I/O buffering
* PKWARE disk splitting
It also has the latest bug fixes that having been found all over the internet.


%package devel
Summary:    Development files for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   zlib-devel

%description devel
Development files for %{name} library.

%if %{with compat}

%package       compat
Summary:       Minizip implementation provided by %{name}
Provides:      minizip = %{minizip_ver}
Provides:      minizip-compat%{?_isa} = %{minizip_ver}
Obsoletes:     minizip-compat < %{minizip_obsoletes}
# We need to Provide and Obsolete the old minizip-ng package before it was rename to minizip-ng-compat
Provides:      minizip-ng = %{minizip_ng_ver}
Obsoletes:     minizip-ng < %{minizip_ng_obsoletes}

# This part is mandatory for the renaming process
# It can be removed in Fedora 42
Obsoletes: minizip < 3.0.3

%description   compat
minizip-ng is a minizip replacement that provides optimizations for "next generation"
systems.
The %{name}-compat package contains the library that is API and binary
compatible with minizip.

%package       compat-devel
Summary:       Development files for %{name}-compat
Requires:      %{name}-compat%{?_isa} = %{version}-%{release}
Provides:      minizip-compat-devel = %{minizip_ver}
Provides:      minizip-compat-devel%{?_isa} = %{minizip_ver}
Obsoletes:     minizip-compat-devel < %{minizip_obsoletes}
# We need to Provide and Obsolete the old minizip-ng package before it was rename to minizip-ng-compat
Provides:      minizip-ng-devel = %{minizip_ng_ver}
Obsoletes:     minizip-ng-devel < %{minizip_ng_obsoletes}

# This part is mandatory for the renaming process
# It can be removed in Fedora 42
Obsoletes: minizip-devel < 3.0.3

%description   compat-devel
The %{name}-compat-devel package contains libraries and header files for
developing application that use minizip.

%endif


%prep
%autosetup -p 1 -n %{name}-%{version}


%build

cat <<_EOF_
###########################################################################
#
# Build the default minizip-ng library
#
###########################################################################
_EOF_

%global __cmake_builddir %{_vpath_builddir}
%cmake \
  -DMZ_BUILD_TESTS:BOOL=ON \
  -DSKIP_INSTALL_BINARIES:BOOL=ON \
  -DCMAKE_INSTALL_INCLUDEDIR=include \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
  -DMZ_FORCE_FETCH_LIBS:BOOL=OFF \
  -DMZ_COMPAT:BOOL=OFF

%cmake_build

%if %{with compat}
cat <<_EOF_
###########################################################################
#
# Build the compat mode library
#
###########################################################################
_EOF_

%global __cmake_builddir %{_vpath_builddir}-compat
%cmake \
  -DMZ_BUILD_TESTS:BOOL=ON \
  -DSKIP_INSTALL_BINARIES:BOOL=ON \
  -DCMAKE_INSTALL_INCLUDEDIR=include \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
  -DMZ_FORCE_FETCH_LIBS:BOOL=OFF \
  -DMZ_COMPAT:BOOL=ON

%cmake_build
%endif

%install
%global __cmake_builddir %{_vpath_builddir}
%cmake_install

%if %{with compat}
%global __cmake_builddir %{_vpath_builddir}-compat
%cmake_install
%endif


%files
%license LICENSE
%doc README.md
%{_libdir}/libminizip-ng.so.4
%{_libdir}/libminizip-ng.so.4{,.*}


%files devel
%{_libdir}/libminizip-ng.so
%{_libdir}/pkgconfig/minizip-ng.pc
%{_libdir}/cmake/minizip-ng/
%{_includedir}/minizip-ng/mz*.h


# Compat files
%if %{with compat}

%files compat
%{_libdir}/%{compat_soname}
%{_libdir}/libminizip.so.4{,.*}

%files compat-devel
%{_libdir}/libminizip.so
%{_libdir}/pkgconfig/minizip.pc
%{_libdir}/cmake/minizip/
%{_includedir}/minizip/mz*.h
%{_includedir}/minizip/unzip.h
%{_includedir}/minizip/zip.h
%{_includedir}/minizip/ioapi.h

%endif


%changelog
* Wed Jan 14 2026 Aditya Singh <v-aditysing@microsoft.com> - 4.0.7-3
- Updated to build minizip-compat-devel package which is needed by
- freexl package.

* Fri Feb 21 2025 Archana Shettigar <v-shettigara@microsoft.com> - 4.0.7-2
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Tue Jul 30 2024 Lukas Javorsky <ljavorsk@redhat.com> - 4.0.7-1
- Rebase to version 4.0.7

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Feb 15 2024 Orion Poplawski <orion@nwra.com> - 3.0.10-8
- Backport upstream change of MZ_VERSION_BUILD to hex number

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Lukas Javorsky <ljavorsk@redhat.com> - 3.0.10-5
- Fix unzLocateFile incompability (upstream commit)
- Fix zip_fileinfo incompability (upstream commit)

* Mon Dec 18 2023 Lukas Javorsky <ljavorsk@redhat.com> - 3.0.10-4
- Fix CVE-2023-48107 (Heapbuffer Overflow)

* Mon Dec 04 2023 Lukas Javorsky <ljavorsk@redhat.com> - 3.0.10-3
- Release bump

* Tue Aug 29 2023 Lukas Javorsky <ljavorsk@redhat.com> - 3.0.10-1
- Rebase to version 3.0.10
- Build both compat and classic minizip-ng libraries

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 14 2022 Julian Sikorski <belegdol@fedoraproject.org> - 3.0.7-2
- Fix broken pkg-config file (RH #1998742)
- Update %%cmake call to use current and supported variables

* Fri Nov 04 2022 Lukas Javorsky <ljavorsk@redhat.com> - 3.0.7-1
- Rebase to version 3.0.7

* Fri Nov 04 2022 Lukas Javorsky <ljavorsk@redhat.com> - 3.0.6-1
- Rebase to version 3.0.6

* Fri Nov 04 2022 Lukas Javorsky <ljavorsk@redhat.com> - 3.0.5-1
- Rebase to version 3.0.5

* Fri Nov 04 2022 Lukas Javorsky <ljavorsk@redhat.com> - 3.0.4-1
- Rebase to version 3.0.4

* Fri Nov 04 2022 Lukas Javorsky <ljavorsk@redhat.com> - 3.0.3-1
- Rebase to version 3.0.3

* Thu Oct 06 2022 Lukas Javorsky <ljavorsk@redhat.com> - 3.0.2-7
- Renaming the minizip package to minizip-ng
- Fedora change dedicated to this: https://fedoraproject.org/wiki/Changes/MinizipRenaming

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 3.0.2-5
- Rebuilt with OpenSSL 3.0.0

* Wed Aug 11 2021 Björn Esser <besser82@fedoraproject.org> - 3.0.2-4
- Add patch to fix pkgconfig file

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Rex Dieter <rdieter@fedoraproject.org> - 3.0.2-2
- drop ldconfig scriptlets (https://fedoraproject.org/wiki/Changes/Removing_ldconfig_scriptlets)
- drop explicit BR: make (already pulled in via cmake)
- %%build: one cmake option per line
- %%check: drop 'make test', does nothing
- -devel: drop explicit cmake dep (autodeps should add cmake-filesystem already)

* Wed Jun 09 2021 Patrik Novotný <panovotn@redhat.com> - 3.0.2-1
- Rebase to upstream release 3.0.2

* Wed Apr 14 2021 Patrik Novotný <panovotn@redhat.com> - 3.0.1-1
- Rebase to upstream release 3.0.1

* Tue Feb 09 2021 Patrik Novotný <panovotn@redhat.com> - 3.0.0-1
- Rebase to upstream release 3.0.0
- Use OpenSSL instead of BRG libraries

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Patrik Novotný <panovotn@redhat.com> - 2.10.6-1
- Rebase to upstream release 2.10.6

* Mon Oct 26 2020 Patrik Novotný <panovotn@redhat.com> - 2.10.2-1
- Rebase to upstream release 2.10.2

* Tue Oct 13 2020 Patrik Novotný <panovotn@redhat.com> - 2.10.1
- Rebase to upstream release 2.10.1

* Tue Aug 11 2020 Honza Horak <hhorak@redhat.com> - 2.10.0-4
- Fix FTBFS caused by cmake changes
  Resolves: #1864153

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 2020 Patrik Novotný <panovotn@redhat.com> - 2.10.0-1
- Rebase to upstream release 2.10.0

* Tue May 26 2020 Patrik Novotný <panovotn@redhat.com> - 2.9.3-1
- Rebase to upstream release 2.9.3

* Tue May 05 2020 Patrik Novotný <panovotn@redhat.com> - 2.9.2-1
- Rebase to upstream release 2.9.2

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Patrik Novotný <panovotn@redhat.com> - 2.9.1-1
- New upstream release: 2.9.1

* Tue Sep 24 2019 Patrik Novotný <panovotn@redhat.com> - 2.9.0-1
- New upstream release: 2.9.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Patrik Novotný <panovotn@redhat.com> - 2.8.9-1
- New upstream release: 2.8.9

* Mon Jun 17 2019 Patrik Novotný <panovotn@redhat.com> - 2.8.8-2
- Move header files to minizip subdirectory (fix implicit conflict)

* Wed Jun 12 2019 Patrik Novotný <panovotn@redhat.com> - 2.8.8-1
- New upstream release: 2.8.8

* Tue Apr 09 2019 Patrik Novotný <panovotn@redhat.com> - 2.8.6-1
- Rebase to upstream version 2.8.6

* Thu Mar 21 2019 Patrik Novotný <panovotn@redhat.com> 2.8.5-1
- Rebase to upstream version 2.8.5

* Wed Feb 13 2019 Patrik Novotný <panovotn@redhat.com> 2.8.3-4
- Fix shared library prefix

* Tue Feb 12 2019 Patrik Novotný <panovotn@redhat.com> 2.8.3-3
- Fix ldconfig execution during build

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Patrik Novotný <panovotn@redhat.com> 2.8.3-1
- Update to upstream version 2.8.3

* Thu Dec 06 2018 Patrik Novotný <panovotn@redhat.com> 2.8.1-1
- Update to upstream version 2.8.1

* Wed Nov 28 2018 Patrik Novotný <panovotn@redhat.com> 2.8.0-2
- Use absolute paths for install directories

* Wed Nov 28 2018 Patrik Novotný <panovotn@redhat.com> 2.8.0-1
- Update to upstream version 2.8.0

* Sun Oct  7 2018 Orion Poplawski <orion@nwra.com> 2.5.4-1
- Update to 2.5.4

* Thu Aug 30 2018 Patrik Novotný <panovotn@redhat.com> 2.5.0-2
- Provide bundled AES and SHA1 libraries

* Thu Aug 16 2018 Patrik Novotný <panovotn@redhat.com> 2.5.0-1
- Version update. Build againts system bzip2.

* Thu Aug  9 2018 Patrik Novotný <panovotn@redhat.com> 2.3.9-1
- Initial build
