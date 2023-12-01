Vendor:         Microsoft Corporation
Distribution:   Mariner
# For deep debugging we need to build binaries with extra debug info
%bcond_with     debug

# Disable CMake in-source builds
#   This is a fix for the https://fedoraproject.org/wiki/Changes/CMake_to_do_out-of-source_builds
#   So the beaviour will be the same also in F31 nad F32
#%%undefine __cmake_in_source_build



Name:           mariadb-connector-odbc
Version:        3.1.11
Release:        3%{?dist}
Summary:        The MariaDB Native Client library (ODBC driver)
License:        LGPLv2+
Source:         https://downloads.mariadb.org/f/connector-odbc-%{version}/%{name}-%{version}-ga-src.tar.gz
Url:            https://mariadb.org/en/
# Online documentation can be found at: https://mariadb.com/kb/en/library/mariadb-connector-odbc/

BuildRequires:  cmake unixODBC-devel gcc-c++
BuildRequires:  mariadb-connector-c-devel >= 3.0.6

Patch1:         libraries_include_path.patch

%description
MariaDB Connector/ODBC is a standardized, LGPL licensed database driver using
the industry standard Open Database Connectivity (ODBC) API. It supports ODBC
Standard 3.5, can be used as a drop-in replacement for MySQL Connector/ODBC,
and it supports both Unicode and ANSI modes.



%prep
%setup -q -n %{name}-%{version}-ga-src
%patch1 -p1

%build

%cmake . \
       -DCMAKE_BUILD_TYPE="%{?with_debug:Debug}%{!?with_debug:RelWithDebInfo}" \
       -DMARIADB_LINK_DYNAMIC="%{_libdir}/libmariadb.so" \
       -DINSTALL_LAYOUT=RPM \
       -DINSTALL_LIBDIR="%{_lib}" \
       -DINSTALL_LIB_SUFFIX="%{_lib}" \
       -DINSTALL_DOCDIR="%{_defaultdocdir}/%{name}" \
       -DINSTALL_LICENSEDIR="%{_defaultlicensedir}/%{name}" \

# Override all optimization flags when making a debug build
%if %{with debug}
CFLAGS="$CFLAGS     -O0 -g"; export CFLAGS
CXXFLAGS="$CXXFLAGS -O0 -g"; export CXXFLAGS
FFLAGS="$FFLAGS     -O0 -g"; export FFLAGS
FCFLAGS="$FCFLAGS   -O0 -g"; export FCFLAGS
%endif

#cmake -B %_vpath_builddir -LAH

%cmake_build



%install
%cmake_install



%files
%license COPYING
%doc     README

# This is unixODBC plugin. It resides directly in %%{_libdir} to be consistent with the rest of unixODBC plugins. Since it is plugin, it doesn´t need to be versioned.
%{_libdir}/libmaodbc.so



%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.11-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Jun 28 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.1.11-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Turn in-source builds back on to fix build break regarding cmake macro compatibility

* Mon Dec 14 2020 Lukas Javorsky <ljavorsk@redhat.com> - 3.1.11-1
- Rebase to 3.1.11
- Add updates for paths in libraries_include_path.patch

* Thu Aug 06 2020 Michal Schorm <mschorm@redhat.com> - 3.1.9-4
- Force the CMake change regarding the in-source builds also to F31 and F32
- %%cmake macro covers the %%{set_build_flags}, so they are not needed
  That also means, the debug build changes to the build flags must be done AFTER the
  %%cmake macro was used.
- %%cmake macro also covers several other options which redudndant specification I removed in this commit
- Default to %%cmake commands instead of %%make commands

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.9-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 02 2020 Lukas Javorsky <ljavorsk@redhat.com> - 3.1.9-1
- Rebase to 3.1.9
- Add patch add_docs_license_dir_option

* Thu Apr 09 2020 Michal Schorm <mschorm@redhat.com> - 3.1.7-1
- Rebase to 3.1.7

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Lukas Javorsky <ljavorsk@redhat.com> - 3.1.6-1
- Rebase to 3.1.6

* Fri Nov 15 2019 Lukas Javorsky <ljavorsk@redhat.com> - 3.1.5-1
- Rebase to 3.1.5

* Tue Nov 12 2019 Michal Schorm <mschorm@redhat.com> - 3.1.4-2
- Rebuild on top of new mariadb-connector-c

* Mon Nov 04 2019 Michal Schorm <mschorm@redhat.com> - 3.1.4-1
- Rebase to 3.1.4

* Mon Aug 19 2019 Michal Schorm <mschorm@redhat.com> - 3.1.3-1
- Rebase to 3.1.3

* Wed Jul 31 2019 Michal Schorm <mschorm@redhat.com> - 3.1.2-1
- Rebase to 3.1.2
- Patch2 upstreamed

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 19 2019 Michal Schorm <mschorm@redhat.com> - 3.1.1-4
- Use macro for setting the compiler flags

* Wed Jun 05 2019 Michal Schorm <mschorm@redhat.com> - 3.1.1-3
- Added debug build switch
- Added patch2: configurable doc and license dirs paths

* Wed Jun 05 2019 Michal Schorm <mschorm@redhat.com> - 3.1.1-2
- Patch solution found

* Tue Jun 04 2019 Michal Schorm <mschorm@redhat.com> - 3.1.1-1
- Rebase to 3.1.1

* Tue Jun 04 2019 Michal Schorm <mschorm@redhat.com> - 3.0.9-1
- Rebase to 3.0.9

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Björn Esser <besser82@fedoraproject.org> - 3.0.8-2
- Append curdir to CMake invokation. (#1668512)

* Sun Jan 06 2019 Michal Schorm <mschorm@redhat.com> - 3.0.8-1
- Rebase to 3.0.8

* Tue Nov 20 2018 Michal Schorm <mschorm@redhat.com> - 3.0.7-1
- Rebase to 3.0.7

* Fri Aug 03 2018 Michal Schorm <mschorm@redhat.com> - 3.0.6-1
- Rebase to 3.0.6
- Raise the minimal version of the connector-c required, because of a fixed bug
  which affected connector-odbc builds

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Feb 10 2018 Michal Schorm <mschorm@redhat.com> - 3.0.3-1
- Rebase to 3.0.3 version
- Use more macros

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Michal Schorm <mschorm@redhat.com> - 3.0.2-1
- Rebase to 3.0.2 version
- Update ldconfig scriptlets
- Remove Group tag

* Thu Sep 07 2017 Augusto Caringi <acaringi@fedoraproject.org> - 3.0.1-2
- Update to top of 3.0 branch from GitHub 860e7f8b754f (version supporting dynamic linking)
- Source tarball composed from upstream GitHub, because the latest version solves the issues
  with dynamic linking.

* Mon Sep 04 2017 Augusto Caringi <acaringi@fedoraproject.org> - 3.0.1-1
- Update to version 3.0.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 16 2017 Michal Schorm <mschorm@redhat.com> - 2.0.14-1
- Update to version 2.0.14 and check, if blockers still apply. They do.
- Upstream issue created

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 19 2016 Michal Schorm <mschorm@redhat.com> - 2.0.12-1
- Initial version for 2.0.12
