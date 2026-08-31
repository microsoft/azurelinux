## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autochangelog
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# For deep debugging we need to build binaries with extra debug info
%bcond debug 0
# Enable building and packing of the testsuite
%bcond testsuite 1

# Override all optimization flags when making a debug build
%if %{with debug}
%global _pkg_extra_cflags   -O0 -g
%global _pkg_extra_cxxflags -O0 -g
# -D_FORTIFY_SOURCE requires some optimizations to be enabled. Disable the fortification.
%undefine _fortify_level
%endif



Name:           mariadb-connector-c
Version:        3.4.9
Release:        2%{?with_debug:.debug}%{?dist}
Summary:        MariaDB Native Client library (C driver)
License:        LGPL-2.1-or-later AND PHP-3.0 AND PHP-3.01 AND LicenseRef-Fedora-Public-Domain
Source0:        https://archive.mariadb.org/connector-c-%{version}/%{name}-%{version}-src.tar.gz
Source2:        my.cnf.in
Source3:        client.cnf
URL:            https://mariadb.org/
# More information: https://mariadb.com/docs/connectors/mariadb-connector-c/building-connectorc-from-source/configuration-settings-for-building-connectorc

%if %{with testsuite}
Patch1:         testsuite.patch
%endif

# Downstream fix attempt for https://jira.mariadb.org/browse/CONC-821
# No upstream fix as of 2026-06-28 (checked 3.4 branch and PRs)
Patch2:         conc-821-fix-bind-result-length.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libzstd-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
# Remote-IO plugin
BuildRequires:  libcurl-devel
# auth_gssapi_client plugin
BuildRequires:  krb5-devel

Requires:       %{name}-config = %{version}-%{release}

# The client_ed25519 plugin bundles a modified copy of the SUPERCOP/NaCl
# Ed25519 "ref10" implementation (public domain, unversioned).
# The sign function is modified to take a password instead of a secret key.
# Cannot be unbundled -- the connector uses the modified internal API.
Provides:       bundled(ed25519-ref10)

%description
The MariaDB Native Client library (C driver) is used to connect applications
developed in C/C++ to MariaDB and MySQL databases.



%package devel
Summary:        Development files for mariadb-connector-c
Requires:       %{name}%{?_isa} = %{version}-%{release}
Recommends:     %{name}-doc = %{version}-%{release}
Requires:       openssl-devel
Requires:       zlib-devel
%{!?rhel:BuildRequires:  multilib-rpm-config}
Conflicts:      mysql-devel-any

%description devel
Development files for mariadb-connector-c.
Contains everything needed to build against libmariadb.so >=3 client library.


%package doc
Summary:        Manual pages documenting API of the libmariadb.so library
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Manual pages documenting API of the libmariadb.so library.



%if %{with testsuite}
%package test
Summary:        Testsuite files for mariadb-connector-c
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake
Recommends:     mariadb-server

%description test
Testsuite files for mariadb-connector-c.
Contains binaries and a prepared CMake ctest file.
Requires running MariaDB / MySQL server with create database "test".
%endif


%package config
Summary:        Configuration files for packages that use /etc/my.cnf as a configuration file
BuildArch:      noarch

%description config
This package delivers /etc/my.cnf that includes other configuration files
from the /etc/my.cnf.d directory and ships this directory as well.
Other packages should only put their files into /etc/my.cnf.d directory
and require this package, so the /etc/my.cnf file is present.



%prep
%autosetup -p1 -n %{name}-%{version}-src

# Remove unused parts
rm -r win win-iconv external/zlib



%build
# https://jira.mariadb.org/browse/MDEV-13836:
#   The server has (used to have for ages) some magic around the port number.
#   If it's 0, the default port value will use getservbyname("mysql", "tcp"), that is, whatever is written in /etc/services.
#   If it's a positive number, say, 3306, it will be 3306, no matter what /etc/services say.
#   I don't know if that behavior makes much sense, /etc/services wasn't supposed to be a system configuration file.

# The INSTALL_* macros have to be specified relative to CMAKE_INSTALL_PREFIX
# so we can't use %%{_datadir} and so forth here.

%cmake . \
       -DCMAKE_BUILD_TYPE="%{?with_debug:Debug}%{!?with_debug:RelWithDebInfo}" \
       -DCMAKE_SYSTEM_PROCESSOR="%{_arch}" \
       -DCMAKE_COMPILE_WARNING_AS_ERROR=0 \
\
       -DMARIADB_UNIX_ADDR=%{_sharedstatedir}/mysql/mysql.sock \
       -DMARIADB_PORT=3306 \
\
       -DWITH_EXTERNAL_ZLIB=ON \
       -DWITH_SSL=OPENSSL \
       -DWITH_MYSQLCOMPAT=ON \
       -DPLUGIN_CLIENT_ED25519=DYNAMIC \
\
       -DDEFAULT_SSL_VERIFY_SERVER_CERT=OFF \
\
       -DINSTALL_LAYOUT=RPM \
       -DINSTALL_BINDIR="bin" \
       -DINSTALL_LIBDIR="%{_lib}" \
       -DINSTALL_INCLUDEDIR="include/mysql" \
       -DINSTALL_PLUGINDIR="%{_lib}/mariadb/plugin" \
       -DINSTALL_PCDIR="%{_lib}/pkgconfig" \
\
%if %{with testsuite}
       -DWITH_UNIT_TESTS=ON
%endif

# Print all cached CMake options values; "-N" means to run in read-only mode; "-LAH" means "List Advanced Help" for each option
cmake -B %{_vpath_builddir} -N -LAH

%cmake_build

sed -e 's|@SYSCONFDIR@|%{_sysconfdir}|' %{SOURCE2} > my.cnf


%install
%cmake_install

%if %{undefined rhel}
%multilib_fix_c_header --file %{_includedir}/mysql/mariadb_version.h
%endif

# Remove static linked libraries and symlinks to them
rm %{buildroot}%{_libdir}/lib*.a

# Add a compatibility symlinks
ln -s mariadb_config %{buildroot}%{_bindir}/mysql_config
ln -s mariadb_version.h %{buildroot}%{_includedir}/mysql/mysql_version.h

# Install config files
install -D -p -m 0644 my.cnf %{buildroot}%{_sysconfdir}/my.cnf
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/my.cnf.d/client.cnf
%if %{with testsuite}
echo %{_libdir}/mariadb/connector-c/tests > %{name}.conf
install -D -p -m 0644 %{name}.conf %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf
%endif



%check
# Check the generated configuration on the actual machine
%{buildroot}%{_bindir}/mariadb_config

# Run the unit tests
# - don't run mytap tests
# - ignore the testsuite result for now. Enable tests now, fix them later.
# Note: there must be a database called 'test' created for the testcases to be run
%if %{with testsuite}
%ctest --test-dir %{_vpath_builddir}/unittest/libmariadb/
%endif


%files
%{_libdir}/libmariadb.so.3

%dir %{_libdir}/mariadb
%dir %{_libdir}/mariadb/plugin
%{_libdir}/mariadb/plugin/auth_gssapi_client.so
%{_libdir}/mariadb/plugin/caching_sha2_password.so
%{_libdir}/mariadb/plugin/client_ed25519.so
%{_libdir}/mariadb/plugin/dialog.so
%{_libdir}/mariadb/plugin/mysql_clear_password.so
%{_libdir}/mariadb/plugin/parsec.so
%{_libdir}/mariadb/plugin/remote_io.so
%{_libdir}/mariadb/plugin/sha256_password.so
%{_libdir}/mariadb/plugin/zstd.so

%doc README
%license COPYING.LIB



%files doc
# Library manual pages
%{_mandir}/man3/{mariadb,mysql}_*.3*



%files devel
# Binary which provides compiler info for software compiling against this library
%{_bindir}/mariadb_config
%{_bindir}/mysql_config

# Symlinks to the versioned library
%{_libdir}/libmariadb.so
%{_libdir}/libmysqlclient.so
%{_libdir}/libmysqlclient_r.so

# Pkgconfig
%{_libdir}/pkgconfig/libmariadb.pc

# Header files
%dir %{_includedir}/mysql
%{_includedir}/mysql/*



%files config
%license COPYING.LIB
%dir %{_sysconfdir}/my.cnf.d
%config(noreplace) %{_sysconfdir}/my.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/client.cnf



%if %{with testsuite}
%files test
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%dir %{_libdir}/mariadb/connector-c
%dir %{_libdir}/mariadb/connector-c/tests
%{_libdir}/mariadb/connector-c/tests/libcctap.so
%{_sysconfdir}/ld.so.conf.d/%{name}.conf
%endif


# Opened issues on the upstream tracker:
#   https://jira.mariadb.org/browse/CONC-293
#      DESCRIPTION: add mysql_config and mariadb_config man page
#      IN_PROGRESS: upsteam plans to add it to 3.1 release
#   https://jira.mariadb.org/browse/CONC-436
#      DESCRIPTION: Make testsuite independent / portable
#      NEW:         PR submitted, problem explained, waiting on upstream response

# Downstream issues:
#   Start running this package testsuite at the build time
#      It requires a running MariaDB server
#         mariadb-server package pulls in mariadb-connector-c as a dependency
#         Need to ensure, that the testsuite is ran against the newly build library, instead of the one from the pulled package
#      Need to ensure, that the testsuite will also run properly on 'fedpkg local' buid, not damaging the host machine

%changelog
## START: Generated by rpmautospec
* Tue Sep 01 2026 Unknown User <please-configure-git-user@example.com> - 3.4.9-3
- Uncommitted changes

* Sun Jun 28 2026 Michal Schorm <mschorm@redhat.com> - 3.4.9-2
- Patch CONC-821: 'mysql_stmt_bind_result()' breaks temporal and string
  type lengths

* Wed Jun 24 2026 Michal Schorm <mschorm@redhat.com> - 3.4.9-1
- Rebase to 3.4.9

* Wed Jun 24 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-28
- [packaging bugfix] Add '-N' (read-only) flag to 'cmake -LAH' cache dump

* Wed Jun 24 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-27
- [cleanup] Replace private '%%__cmake_builddir' macro with public
  '%%{_vpath_builddir}'

* Wed Jun 24 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-26
- [bugfix] Disable '_FORTIFY_SOURCE' when building with '-O0' debug flags

* Wed Jun 24 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-25
- [cleanup] Remove Fortran debug flags override

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-24
- Bump release for package rebuild

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-23
- [cleanup] Use '%%autosetup' instead of '%%setup' + conditional '%%patch'

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-22
- [cleanup] Update building-from-source documentation URL

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-21
- [cleanup] Replace flatpak-conditional '/etc/my.cnf' dependency with
  '-config'

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-20
- [cleanup] Modernize '%%bcond' declarations to explicit 0/1 format

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-19
- [cleanup] Remove leading article from 'Summary'

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-18
- [cleanup] Remove stale 'rpmlintrc' filters for 'debuginfo'/'debugsource'

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-17
- [cleanup] Remove deprecated 'ldconfig' scriptlets from '-test' subpackage

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-16
- [cleanup] Remove stale 'mariadb-config' Obsoletes

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-15
- [bugfix] Fix 'BuildRequires' from 'gcc-c++' to 'gcc'

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-14
- [cleanup] Split 'BuildRequires' and 'Requires' to one dependency per line

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-13
- [cleanup] Fix typo in '%%prep' section comment

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-12
- [cleanup] Fix 'URL' tag capitalization and use HTTPS

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-11
- [cleanup] Normalize 'Source' tag to 'Source0'

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-10
- [bugfix] Declare bundled 'ed25519-ref10' in 'client_ed25519' plugin

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-9
- [bugfix] Add '%%license' to '-config' subpackage

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-8
- [bugfix] Fix debug build flag overrides using package-specific macros

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-7
- [bugfix] Add '%%{?_isa}' qualifier to arch-dependent subpackage
  'Requires'

* Tue Jun 23 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-6
- [cleanup] Switch to '%%autochangelog'

* Fri Jun 12 2026 Yaakov Selkowitz <yselkowi@redhat.com> - 3.4.8-5
- Rebuilt for openssl 4.0

* Thu May 21 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-4
- Drop multilib-rpm-config usage on RHEL

* Sat Jan 24 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-3
- [Fedora 44 change] Remove 'community-mysql' names

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Jan 06 2026 Michal Schorm <mschorm@redhat.com> - 3.4.8-1
- Rebase to 3.4.8

* Mon Sep 29 2025 Pavol Sloboda <psloboda@redhat.com> - 3.4.7-1
- Rebase to 3.4.7

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 16 2025 Michal Schorm <mschorm@redhat.com> - 3.4.5-6
- [SPECfile enhancement] List plugins by name instead of glob

* Wed May 07 2025 Pavol Sloboda <psloboda@redhat.com> - 3.4.5-5
- Moved the libcctap.so library from %%{_libdir}

* Tue May 06 2025 Michal Schorm <mschorm@redhat.com> - 3.4.5-4
- [license fix] Add discovered PHP licenses to the list

* Mon Apr 28 2025 Pavol Sloboda <psloboda@redhat.com> - 3.4.5-3
- updated the patch fixing the compilation with gcc 15

* Mon Apr 28 2025 Pavol Sloboda <psloboda@redhat.com> - 3.4.5-2
- fix: stopped ignoring the test return codes

* Mon Apr 28 2025 Pavol Sloboda <psloboda@redhat.com> - 3.4.5-1
- Rebase to 3.4.5

* Thu Feb 27 2025 Michal Schorm <mschorm@redhat.com> - 3.4.4-3
- Bump release for package rebuild

* Thu Feb 27 2025 Michal Schorm <mschorm@redhat.com> - 3.4.4-2
- Cherry-pick commits from the upstream latest git content

* Wed Feb 12 2025 Michal Schorm <mschorm@redhat.com> - 3.4.4-1
- Rebase to 3.4.4

* Tue Feb 04 2025 Michal Schorm <mschorm@redhat.com> - 3.4.3-4
- Disable option that requires all connections to be SSL encrypted by
  default

* Fri Jan 24 2025 Michal Schorm <mschorm@redhat.com> - 3.4.3-3
- Fix FTBFS caused by GCC 15

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 14 2024 Michal Schorm <mschorm@redhat.com> - 3.4.3-1
- Rebase to 3.4.3

* Thu Aug 22 2024 Michal Schorm <mschorm@redhat.com> - 3.4.1-1
- Rebase to 3.4.1

* Wed Jul 31 2024 Michal Schorm <mschorm@redhat.com> - 3.3.10-1
- Rebase to 3.3.10

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Apr 17 2024 Michal Schorm <mschorm@redhat.com> - 3.3.8-7
- [Fixup] Fix my.cnf dependency

* Tue Apr 09 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 3.3.8-6
- Fix my.cnf dependency

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 12 2024 Michal Schorm <mschorm@redhat.com> - 3.3.8-3
- [LTO FTBFS] Responsible upstream code found, switch back to building with
  LTO

* Mon Jan 08 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 3.3.8-2
- Fix flatpak build

* Sun Jan 07 2024 Michal Schorm <mschorm@redhat.com> - 3.3.8-1
- Rebase to 3.3.8

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 23 2023 Michal Schorm <mschorm@redhat.com> - 3.3.5-2
- Update the URL to the source tarball

* Tue May 23 2023 Michal Schorm <mschorm@redhat.com> - 3.3.5-1
- Rebase to 3.3.5

* Wed Apr 19 2023 Michal Schorm <mschorm@redhat.com> - 3.3.4-6
- Bump release for the production build

* Wed Apr 19 2023 Michal Schorm <mschorm@redhat.com> - 3.3.4-5
- Added a note for future maintainers

* Wed Apr 19 2023 Michal Schorm <mschorm@redhat.com> - 3.3.4-4
- Fix RPM syntax: '%%patchN' has been deprecated https://lists.fedoraprojec
  t.org/archives/list/devel@lists.fedoraproject.org/thread/VBFDPQHAHF3WG6WB
  ZR2L5GSWMW6CVTJS/

* Wed Apr 19 2023 Michal Schorm <mschorm@redhat.com> - 3.3.4-3
- Start building 'zstd.so' plugin

* Wed Apr 19 2023 Michal Schorm <mschorm@redhat.com> - 3.3.4-2
- Switch to the CMake out-of-source building

* Wed Apr 19 2023 Michal Schorm <mschorm@redhat.com> - 3.3.4-1
- Rebase to 3.3.4

* Thu Mar 30 2023 Lukas Javorsky <ljavorsk@redhat.com> - 3.2.7-4
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 11 2022 Michal Schorm <mschorm@redhat.com> - 3.2.7-1
- Rebase to 3.2.7

* Tue May 24 2022 Stephan Bergmann <sbergman@redhat.com> - 3.2.6-2
- Fix flatpak builds see <https://docs.fedoraproject.org/en-
  US/flatpak/troubleshooting/#_uncompressed_manual_pages>

* Thu Feb 17 2022 Michal Schorm <mschorm@redhat.com> - 3.2.6-1
- Rebase to 3.2.6
- Introduction of a new '*-doc' subpackage

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 3.1.13-4
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 13 2021 Michal Schorm <mschorm@redhat.com> - 3.1.13-2
- Update RPMLint whitelist

* Thu May 13 2021 Michal Schorm <mschorm@redhat.com> - 3.1.13-1
- Rebase to 3.1.13

* Tue Apr 27 2021 Michal Schorm <mschorm@redhat.com> - 3.1.12-2
- Fix package Conflicts on other OS than Fedora

* Wed Feb 24 2021 Michal Schorm <mschorm@redhat.com> - 3.1.12-1
- Rebase to 3.1.12

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 04 2020 Michal Schorm <mschorm@redhat.com> - 3.1.11-1
- Rebase to 3.1.11

* Fri Sep 18 2020 Lukas Javorsky <ljavorsk@redhat.com> - 3.1.10-1
- Rebase to 3.1.10

* Fri Aug 14 2020 Michal Schorm <mschorm@redhat.com> - 3.1.9-7
- Start using %%__cmake_builddir, packaging guidelines has been updated

* Wed Aug 05 2020 Michal Schorm <mschorm@redhat.com> - 3.1.9-6
- Revert the CMake change regarding the in-source builds for now -
  %%%%cmake macro covers the %%%%{set_build_flags}, so they are not needed
  That also means, the debug buildchnages to the build flags must be done
  AFTER the %%%%cmake macro was used. - %%%%cmake macro also covers the
  CMAKE_INSTALL_PREFIX="%%%%{_prefix}" option - Default to %%%%cmake
  commands instead fo %%%%make commands - Update the WITH_UNITTEST macro to
  the one upstream use now - Introduce macro to enable / disable testusite
  (and building of the *-test subpackage)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.9-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Michal Schorm <mschorm@redhat.com> - 3.1.9-3
- Remove completed items from TO-DO list

* Tue Jul 14 2020 Michal Schorm <mschorm@redhat.com> - 3.1.9-2
- Add explicit confict between mariadb-connector-c-devel and community-
  mysql-devel packages

* Wed Jun 24 2020 Lukas Javorsky <ljavorsk@redhat.com> - 3.1.9-1
- Rebase to 3.1.9

* Sat May 23 2020 Lukas Javorsky <ljavorsk@redhat.com> - 3.1.8-1
- Rebase to 3.1.8

* Mon Mar 16 2020 Michal Schorm <mschorm@redhat.com> - 3.1.7-2
- Rebase to 3.1.7 latest git Fix for:
  https://jira.mariadb.org/browse/CONC-441

* Mon Feb 03 2020 Michal Schorm <mschorm@redhat.com> - 3.1.7-1
- Rebase to 3.1.7

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 17 2019 Lukas Javorsky <ljavorsk@redhat.com> - 3.1.6-1
- Rebase to 3.1.6

* Tue Nov 12 2019 Michal Schorm <mschorm@redhat.com> - 3.1.5-1
- Rebase to 3.1.5

* Sun Nov 03 2019 Michal Schorm <mschorm@redhat.com> - 3.1.4-3
- Fix for #1624533

* Sun Nov 03 2019 Michal Schorm <mschorm@redhat.com> - 3.1.4-2
- Remove a misleading comment which was deprecated by commit 3228be76

* Fri Oct 04 2019 Lukas Javorsky <ljavorsk@redhat.com> - 3.1.4-1
- Rebase to 3.1.4

* Wed Sep 11 2019 Michal Schorm <mschorm@redhat.com> - 3.1.3-5
- Enable building of the ed25519 client plugin. It won't be shipped anymore
  by 'mariadb-server'

* Wed Aug 21 2019 Michal Schorm <mschorm@redhat.com> - 3.1.3-4
- The testsuite is now fully working NOTE: 4th test of 'misc' suite, called
  "test_sslenforce", needs SSL encryption to be set up

* Wed Aug 21 2019 Michal Schorm <mschorm@redhat.com> - 3.1.3-3
- Extract the prepared testsuite to the standalone subpackage so it can be
  run outside of the buildroot

* Wed Aug 21 2019 Michal Schorm <mschorm@redhat.com> - 3.1.3-2
- Remove glob from library version, as per Fedora Packaging Guidelines

* Fri Aug 02 2019 Michal Schorm <mschorm@redhat.com> - 3.1.3-1
- Rebase to 3.1.3

* Fri Jul 19 2019 Michal Schorm <mschorm@redhat.com> - 3.1.2-6
- Fix typo

* Fri Jul 19 2019 Michal Schorm <mschorm@redhat.com> - 3.1.2-5
- Use macro to set the build flags

* Fri Jul 19 2019 Michal Schorm <mschorm@redhat.com> - 3.1.2-4
- Fix the debug build

* Thu Jul 18 2019 Michal Schorm <mschorm@redhat.com> - 3.1.2-3
- Use macro for tarball name

* Tue Jul 16 2019 Michal Schorm <mschorm@redhat.com> - 3.1.2-2
- Added a debug switch

* Tue Jul 16 2019 Michal Schorm <mschorm@redhat.com> - 3.1.2-1
- Rebase to 3.1.2 version Disabling the ED25519 plugin Plugindir patch
  upstreamed

* Thu Jul 11 2019 Michal Schorm <mschorm@redhat.com> - 3.0.10-8
- Tweak SPECfile: use macros for make commands

* Tue May 21 2019 Michal Schorm <mschorm@redhat.com> - 3.0.10-7
- Fix overlinking issues

* Tue May 21 2019 Michal Schorm <mschorm@redhat.com> - 3.0.10-6
- Add info for the testsuite execution

* Tue May 21 2019 Michal Schorm <mschorm@redhat.com> - 3.0.10-5
- Add info about the downstream issues

* Tue May 21 2019 Michal Schorm <mschorm@redhat.com> - 3.0.10-4
- Update info about the issues reported to the upstream

* Tue May 21 2019 Michal Schorm <mschorm@redhat.com> - 3.0.10-3
- Remove scriplet; no longer needed It fixed an issue in F26 and F27. We
  gave the users enough time to update

* Tue May 21 2019 Michal Schorm <mschorm@redhat.com> - 3.0.10-2
- Update RPMLint whitelist

* Wed May 15 2019 Michal Schorm <mschorm@redhat.com> - 3.0.10-1
- Rebase to 3.0.10

* Fri Mar 29 2019 Michal Schorm <mschorm@redhat.com> - 3.0.9-3
- Add "zlib-devel" requirement in "-devel" subpackage. MariaDB requires
  linking with "-lz", which will fail without the zlib library Related:
  #1693966

* Thu Mar 21 2019 Michal Schorm <mschorm@redhat.com> - 3.0.9-2
- Fix plugindir issues Resolves: #1624533

* Mon Feb 18 2019 Michal Schorm <mschorm@redhat.com> - 3.0.9-1
- Rebase to 3.0.9

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Michal Schorm <mschorm@redhat.com> - 3.0.8-2
- Update commands for newer CMake

* Wed Jan 02 2019 Michal Schorm <mschorm@redhat.com> - 3.0.8-1
- Rebase to 3.0.8

* Mon Nov 19 2018 Michal Schorm <mschorm@redhat.com> - 3.0.7-1
- Rebase to 3.0.7

* Tue Sep 04 2018 Michal Schorm <mschorm@redhat.com> - 3.0.6-3
- Bump release for the last fix

* Tue Sep 04 2018 Michal Schorm <mschorm@redhat.com> - 3.0.6-2
- Fix parallel installability of x86_64 and i686 devel package

* Fri Aug 03 2018 Michal Schorm <mschorm@redhat.com> - 3.0.6-1
- Rebase to 3.0.6 - Require base openssl-devel for *-devel - Provides for
  *-config shouldn't be needed, since only mariadb and mysql packages rely
  on it by requiring specific file from inside

* Sat Jul 21 2018 Honza Horak <hhorak@redhat.com> - 3.0.5-6
- Use Provides and Obsoletes in -config, not main package

* Wed Jul 18 2018 Honza Horak <hhorak@redhat.com> - 3.0.5-5
- Obsolete mariadb-config and make the main package require /etc/my.cnf

* Tue Jul 17 2018 Honza Horak <hhorak@redhat.com> - 3.0.5-4
- Add -config sub-package that delivers system-wide /etc/my.cnf and
  /etc/my.cnf.d directory, that other packages should use

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Michal Schorm <mschorm@redhat.com> - 3.0.5-2
- Remove the cmake.patch; fix SPECfile to compile correctly without it
  SPECfile tweaks

* Fri Jun 08 2018 Michal Schorm <mschorm@redhat.com> - 3.0.5-1
- Rebase to 3.0.5

* Mon Jun 04 2018 Michal Schorm <mschorm@redhat.com> - 3.0.4-3
- Whitelist some RPMLint warnings and errors

* Wed May 16 2018 Michal Schorm <mschorm@redhat.com> - 3.0.4-2
- Enable the testsuite (but ingore its results for now) Related: #1519945

* Thu Apr 26 2018 Michal Schorm <mschorm@redhat.com> - 3.0.4-1
- Rebase to 3.0.4

* Mon Apr 23 2018 Michal Schorm <mschorm@redhat.com> - 3.0.3-7
- Further fix of the '--plugindir' output from the config binary; #1569159

* Wed Mar 21 2018 Richard W.M. Jones <rjones@redhat.com> - 3.0.3-6
- Fix plugin install directory (INSTALL_PLUGINDIR not PLUGIN_INSTALL_DIR).

* Sun Feb 18 2018 Michal Schorm <mschorm@redhat.com> - 3.0.3-5
- Add a compiler to buildroot;
  https://fedoraproject.org/wiki/Changes/Remove_GCC_from_BuildRoot

* Fri Feb 09 2018 Michal Schorm <mschorm@redhat.com> - 3.0.3-4
- Remove Group tag

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Michal Schorm <mschorm@redhat.com> - 3.0.3-2
- Remove ldconfig scriplets, not needed on F28+

* Fri Jan 19 2018 Michal Schorm <mschorm@redhat.com> - 3.0.3-1
- Rebase to 3.0.3 version

* Mon Nov 27 2017 Honza Horak <hhorak@redhat.com> - 3.0.2-22
- Remove unneeded dependency on xmlto

* Tue Nov 14 2017 Pavel Raiskup <praiskup@redhat.com> - 3.0.2-21
- spec: drop misleading provides

* Wed Nov 08 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-20
- Move scriplet to the correct package

* Wed Nov 01 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-19
- Typo fix

* Wed Nov 01 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-18
- Use correct require for OpenSSL

* Wed Nov 01 2017 Merlin Mathesius <mmathesi@redhat.com> - 3.0.2-17
- Correct typo in spec file conditional

* Tue Oct 31 2017 Merlin Mathesius <mmathesi@redhat.com> - 3.0.2-16
- Cleanup spec file conditionals

* Tue Oct 31 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-15
- Remove Requires for openssl. Managed by RPM.

* Mon Oct 30 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-14
- Update scriplet dealing with symlinks as Gudelines suggests

* Thu Oct 26 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-13
- Move library directly to libdir, don't create any symlinks to directories
  Related: #1501933 Add 'Conflicts' with mariadb package on F<28 Related:
  #1506441

* Mon Oct 09 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-12
- Fix ldconfig path. It does not work with symlinks

* Mon Oct 09 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-11
- Fix rpm warning from %%post script

* Wed Oct 04 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-10
- Add scriptlets to handle errors in /usr/lib64/ created by older versions
  of mariadb and mariadb-connector-c pakages

* Tue Oct 03 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-9
- Change libdir from .../lib64/mariadb to mysql Related: #1497234

* Wed Sep 20 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-8
- Add symlinks so more packages will build succesfully

* Sun Sep 17 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-7
- Add provides "libmysqlclient.so"

* Wed Sep 13 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-6
- Move header files to the same location, as they would be in mariadb-
  server (10.2.8) which means from /usr/include to /usr/include/mysql

* Tue Sep 05 2017 Honza Horak <hhorak@redhat.com> - 3.0.2-5
- Remove a symlink /usr/lib64/mysql that conflicts with mariadb-libs

* Mon Aug 14 2017 Honza Horak <hhorak@redhat.com> - 3.0.2-4
- Add compatibility symlinks

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-1
- Rebase to version 3.0.2 Library libmariadb.so.3 introduced Plugin Remote-
  IO enabled

* Thu Jun 15 2017 Michal Schorm <mschorm@redhat.com> - 2.3.3-3
- Some fixes for RPMLint warnings and errors

* Wed Jun 14 2017 Michal Schorm <mschorm@redhat.com> - 2.3.3-2
- Update of Source URL

* Wed Jun 07 2017 Michal Schorm <mschorm@redhat.com> - 2.3.3-1
- Rebase to version 2.3.3 Patch "v2.3.2" dropped, solved by upstream

* Tue May 16 2017 Michal Schorm <mschorm@redhat.com> - 2.3.2-4
- SPECfile enhanced

* Mon Feb 06 2017 Michal Schorm <mschorm@redhat.com> - 2.3.2-3
- Fix based on RMPLint output

* Mon Jan 23 2017 Michal Schorm <mschorm@redhat.com> - 2.3.2-1
- Rebase to versionn 2.3.2, patch needed (fixed by upstream in later
  versions) Plugin dir moved from /libdir/plugin to /libdir/mariadb/plugin

* Thu Nov 03 2016 Michal Schorm <mschorm@redhat.com> - 2.3.1-4
- Minor corrections, because scratch build failed. Moved comments, typos,
  etc. Changelog remained the same.

* Thu Oct 27 2016 FaramosCZ <mschorm@centrum.cz> - 2.3.1-3
- Fixed ownership of {_libdir}/mariadb (this dir must me owned by package)
- Fixed ownership of {_sysconfigdir}/ld.so.conf.d (this dir must me owned
  by package)
- Fixed redundnace on lines with {_sysconfigdir}/ld.so.conf.d
- Fixed ownership of {_bindir} (only one program is owned, so let's be
  accurate)
- Some comments added, for me and futura maintainers

* Tue Oct 18 2016 Michal Schorm <mschorm@redhat.com> - 2.3.1-2
- RPATH fix

* Tue Sep 13 2016 Michal Schorm <mschorm@redhat.com> - 2.3.1-1
- Rebase to version 2.3.1

* Thu Feb 04 2016 Dennis Gilmore <dennis@ausil.us> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 23 2015 Matej Muzila <mmuzila@redhat.com> - 2.1.0-1
- Rebase to version 2.1.0

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Sep 24 2014 Matej Mužila <mmuzila@redhat.com> - 2.0.0-2
- Fixed html IDs in documentation

* Wed Sep 24 2014 Matej Mužila <mmuzila@redhat.com> - 2.0.0-1
- Initial version for 2.0.0
## END: Generated by rpmautospec
