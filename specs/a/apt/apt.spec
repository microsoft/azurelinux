# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Force out of source build
%undefine __cmake_in_source_build

%{!?jobs:%global jobs %(/usr/bin/getconf _NPROCESSORS_ONLN)}

# apt library somajor...
%global libsomajor 7.0
%global libprivsomajor 0.0

# Disable integration tests by default,
# as there is a bunch of failures on non-Debian systems currently.
# Additionally, these tests take a long time to run.
%bcond_with check_integration

Name:           apt
Version:        3.1.16
Release:        2%{?dist}
Summary:        Command-line package manager for Debian packages

License:        GPL-2.0-or-later
URL:            https://tracker.debian.org/pkg/apt
Source0:        https://salsa.debian.org/apt-team/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz
Patch1:         apt_include_cstdint.patch
Patch2:         apt-2.9.27-cstdint.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.4
BuildRequires:  ninja-build
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig(gnutls) >= 3.4.6
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libxxhash)
%{?el9:BuildRequires: gcc-toolset-15}
%{?el9:BuildRequires: gcc-toolset-15-gcc-plugin-annobin}

# Package manager BRs
BuildRequires:  dpkg-dev

# These BRs lack pkgconfig() names
BuildRequires:  libdb-devel
BuildRequires:  gtest-devel
BuildRequires:  bzip2-devel

# Misc BRs
BuildRequires:  triehash
BuildRequires:  po4a >= 0.35
BuildRequires:  docbook-style-xsl, docbook-dtds
BuildRequires:  gettext >= 0.19
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  w3m
BuildRequires:  %{_bindir}/xsltproc

%if %{with check_integration}
BuildRequires:  coreutils, moreutils,
BuildRequires:  moreutils-parallel
BuildRequires:  fakeroot, lsof, sed
BuildRequires:  tar, wget, stunnel
BuildRequires:  gnupg, gnupg2
BuildRequires:  perl(File::FcntlLock)
BuildRequires:  perl(Digest::SHA)
BuildRequires:  debhelper >= 9
# Unbreak running tests in non-interactive terminals
BuildRequires:  expect
%endif

# For ensuring the user is created
%{?el9:Requires(pre): shadow-utils}

# Apt is essentially broken without dpkg
Requires:       dpkg >= 1.17.14

# To ensure matching apt libs are installed
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

# These is one optional script in apt that still requires perl, so let's make
# perl a recommended dependency as apt can be used without perl.
%global __requires_exclude_from ^%{_libexecdir}/dpkg/methods/apt/setup$
Recommends: /usr/bin/perl

# apt-transport-curl-https is gone...
Provides:       %{name}-transport-https = %{version}-%{release}
Provides:       %{name}-transport-curl-https = %{version}-%{release}

%description
This package provides commandline tools for searching and
managing as well as querying information about packages
as a low-level access to all features of the libapt-pkg library.

These include:
  * apt-get for retrieval of packages and information about them
    from authenticated sources and for installation, upgrade and
    removal of packages together with their dependencies
  * apt-cache for querying available information about installed
    as well as installable packages
  * apt-cdrom to use removable media as a source for packages
  * apt-config as an interface to the configuration settings
  * apt-key as an interface to manage authentication keys

%package libs
Summary:        Runtime libraries for %{name}

%description libs
This package includes the libapt-pkg library.

libapt-pkg provides the common functionality for searching and
managing packages as well as information about packages.
Higher-level package managers can depend upon this library.

This includes:
  * retrieval of information about packages from multiple sources
  * retrieval of packages and all dependent packages
    needed to satisfy a request either through an internal
    solver or by interfacing with an external one
  * authenticating the sources and validating the retrieved data
  * installation and removal of packages in the system
  * providing different transports to retrieve data over cdrom, ftp,
    http, rsh as well as an interface to add more transports like
    debtorrent (apt-transport-debtorrent).

%package doc
Summary:        Documentation for APT
BuildArch:      noarch

%description doc
This package contains the user guide and offline guide for various
APT tools which are provided in a html and a text-only version.

%package devel
Summary:        Development files for APT's libraries
Provides:       libapt-pkg-devel%{?_isa} = %{version}-%{release}
Provides:       libapt-pkg-devel = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and libraries for
developing with APT's libapt-pkg Debian package manipulation
library.

%package apidoc
Summary:        Documentation for developing against APT libraries
Provides:       libapt-pkg-doc = %{version}-%{release}
Obsoletes:      %{name}-devel-doc < 1.9.7-1
Provides:       %{name}-devel-doc = %{version}-%{release}
BuildArch:      noarch

%description apidoc
This package contains documentation for development of the APT
Debian package manipulation program and its libraries.

This includes the source code documentation generated by doxygen
in html format.

%package utils
Summary:        Package management related utility programs
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
This package contains some less used commandline utilities related
to package management with APT.

  * apt-extracttemplates is used by debconf to prompt for configuration
    questions before installation.
  * apt-ftparchive is used to create Packages and other index files
    needed to publish an archive of Debian packages
  * apt-sortpkgs is a Packages/Sources file normalizer.

%prep
%autosetup -p1

# Create a sysusers.d config file
cat >apt.sysusers.conf <<EOF
u _apt - 'APT account for owning persistent & cache data' %{_sharedstatedir}/apt -
EOF

%build
%{?el9:source /opt/rh/gcc-toolset-15/enable}
%cmake -GNinja
%cmake_build

%install
%{?el9:source /opt/rh/gcc-toolset-15/enable}
%cmake_install

%find_lang %{name}
%find_lang %{name}-utils
%find_lang libapt-pkg%{libsomajor}

cat libapt*.lang >> %{name}-libs.lang

mkdir -p %{buildroot}%{_localstatedir}/log/apt
touch %{buildroot}%{_localstatedir}/log/apt/{term,history}.log
mkdir -p %{buildroot}%{_sysconfdir}/apt/{apt.conf,preferences,sources.list,trusted.gpg}.d
install -pm 644 doc/examples/apt.conf %{buildroot}%{_sysconfdir}/apt/
touch %{buildroot}%{_sysconfdir}/apt/sources.list
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
cat > %{buildroot}%{_sysconfdir}/logrotate.d/apt <<EOF
%{_localstatedir}/log/apt/term.log {
  rotate 12
  monthly
  compress
  missingok
  notifempty
}
%{_localstatedir}/log/apt/history.log {
  rotate 12
  monthly
  compress
  missingok
  notifempty
}
EOF

%if 0%{?fedora} || 0%{?rhel} > 9
install -m0644 -D apt.sysusers.conf %{buildroot}%{_sysusersdir}/apt.conf
%endif

%check
%{?el9:source /opt/rh/gcc-toolset-15/enable}
%ctest
%if %{with check_integration}
unbuffer ./test/integration/run-tests -q %{?jobs:-j %{jobs}}
%endif

# Create the _apt user+group for apt data
%pre
getent group _apt >/dev/null || groupadd -r _apt
getent passwd _apt >/dev/null || \
    useradd -r -g _apt -d %{_sharedstatedir}/apt -s /sbin/nologin \
    -c "APT account for owning persistent & cache data" _apt
exit 0

%ldconfig_scriptlets libs

%files -f %{name}.lang
%license COPYING*
%doc README.* AUTHORS
%{_bindir}/apt
%{_bindir}/apt-cache
%{_bindir}/apt-cdrom
%{_bindir}/apt-config
%{_bindir}/apt-get
%{_bindir}/apt-mark
%dir %{_libexecdir}/apt
%{_libexecdir}/apt/apt-helper
%{_libexecdir}/apt/methods
%{_libexecdir}/dpkg/methods/apt
%attr(-,_apt,_apt) %{_sharedstatedir}/apt
%attr(-,_apt,_apt) %{_localstatedir}/cache/apt
%dir %attr(-,_apt,_apt) %{_localstatedir}/log/apt
%ghost %{_localstatedir}/log/apt/history.log
%ghost %{_localstatedir}/log/apt/term.log
%dir %attr(-,_apt,_apt) %{_sysconfdir}/apt/apt.conf.d
%dir %attr(-,_apt,_apt) %{_sysconfdir}/apt/preferences.d
%dir %attr(-,_apt,_apt) %{_sysconfdir}/apt/sources.list.d
%dir %attr(-,_apt,_apt) %{_sysconfdir}/apt/trusted.gpg.d
%config(noreplace) %attr(-,_apt,_apt) %{_sysconfdir}/apt/apt.conf
%ghost %{_sysconfdir}/apt/sources.list
%config(noreplace) %{_sysconfdir}/logrotate.d/apt
%{_datadir}/bash-completion/completions/apt
%{_mandir}/*/*/apt.*
%{_mandir}/*/*/apt-cache.*
%{_mandir}/*/*/apt-cdrom.*
%{_mandir}/*/*/apt-config.*
%{_mandir}/*/*/apt-get.*
%{_mandir}/*/*/apt-mark.*
%{_mandir}/*/*/apt-patterns.*
%{_mandir}/*/*/apt-secure.*
%{_mandir}/*/*/apt-transport-http.*
%{_mandir}/*/*/apt-transport-https.*
%{_mandir}/*/*/apt-transport-mirror.*
%{_mandir}/*/*/apt_auth.*
%{_mandir}/*/*/apt_preferences.*
%{_mandir}/*/*/sources.list.*
%{_mandir}/*/apt.*
%{_mandir}/*/apt-cache.*
%{_mandir}/*/apt-cdrom.*
%{_mandir}/*/apt-config.*
%{_mandir}/*/apt-get.*
%{_mandir}/*/apt-mark.*
%{_mandir}/*/apt-patterns.*
%{_mandir}/*/apt-secure.*
%{_mandir}/*/apt-transport-http.*
%{_mandir}/*/apt-transport-https.*
%{_mandir}/*/apt-transport-mirror.*
%{_mandir}/*/apt_auth.*
%{_mandir}/*/apt_preferences.*
%{_mandir}/*/sources.list.*
%doc %{_docdir}/%{name}/*
%if 0%{?fedora} || 0%{?rhel} > 9
%{_sysusersdir}/apt.conf
%endif

%files libs -f %{name}-libs.lang
%license COPYING*
%{_libdir}/libapt-pkg.so.%{libsomajor}{,.*}
%{_libdir}/libapt-private.so.%{libprivsomajor}{,.*}

%files doc
%doc %{_docdir}/%{name}-doc

%files apidoc
%doc %{_docdir}/libapt-pkg-doc

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%files utils -f %{name}-utils.lang
%{_bindir}/apt-ftparchive
%{_bindir}/apt-sortpkgs
%{_libexecdir}/apt/apt-extracttemplates
%{_libexecdir}/apt/planners
%{_libexecdir}/apt/solvers
%{_mandir}/*/*/apt-extracttemplates.*
%{_mandir}/*/*/apt-ftparchive.*
%{_mandir}/*/*/apt-sortpkgs.*
%{_mandir}/*/apt-extracttemplates.*
%{_mandir}/*/apt-ftparchive.*
%{_mandir}/*/apt-sortpkgs.*
%doc %{_docdir}/%{name}-utils

%changelog
* Tue Feb 17 2026 Terje Rosten <terjeros@gmail.com> - 3.1.16-2
- Backport 3.1.16 to epel9

* Tue Feb 17 2026 Packit <hello@packit.dev> - 3.1.16-1
- Update to version 3.1.16
- Resolves: rhbz#2440372

* Mon Feb 16 2026 Terje Rosten <terjeros@gmail.com> - 3.1.15-2
- Rebuild due to so name bump

* Sun Feb 15 2026 Terje Rosten <terjeros@gmail.com> - 3.1.15-1
- 3.1.15

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Oct 06 2025 Terje Rosten <terjeros@gmail.com> - 3.1.8-1
- 3.1.8
- apt-key is gone
- Add openssl-devel to buildreq
- Fix include issue
- apt-extracttemplates has moved

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.9.27-2
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Mon Feb 03 2025 Packit <hello@packit.dev> - 2.9.27-1
- Update to version 2.9.27
- Resolves: rhbz#2319327

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 09 2024 Packit <hello@packit.dev> - 2.9.8-1
- Update to version 2.9.8
- Resolves: rhbz#2283193

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 22 2024 Packit <hello@packit.dev> - 2.9.2-1
- Update to version 2.9.2
- Resolves: rhbz#2274776

* Sun Apr 14 2024 Packit <hello@packit.dev> - 2.9.1-1
- Update to version 2.9.1
- Resolves: rhbz#2274776

* Sat Apr 13 2024 Daan De Meyer <daan.j.demeyer@gmail.com> - 2.7.14-2
- Make perl a Recommends dependency

* Fri Mar 22 2024 Packit <hello@packit.dev> - 2.7.14-1
- Release 2.7.14 (Julian Andres Klode)
- Add an artificial Conflicts: against libnettle8 (Steve Langasek)
- Revert "debrecords: Do not reparse if given same location" (Julian Andres Klode)
- debrecords: Do not reparse if given same location (Julian Andres Klode)
- pkgTagFile::Jump: Use lookback buffer to rejump to current position (Julian Andres Klode)
- s#http://bugs.debian.org/src/#https://bugs.debian.org/src# (Wesley Schwengle)
- Update VCG tool URI to new location (Wesley Schwengle)
- Update Graphviz URL to https://graphviz.org/ (Wesley Schwengle)
- Include Dutch translation for apt/apt-get upgrade documenation update (Wesley Schwengle)
- Update documentation for apt upgrade with pkg arg (Wesley Schwengle)
- Update documentation for apt-get upgrade with pkg arg (Wesley Schwengle)
- Dutch manpages translation update (Frans Spiesschaert)
- Dutch program translation update (Frans Spiesschaert)
- Parse unsupported != relation in dependencies (David Kalnischkies)
- Remove non-existent Debug::BuildDeps from apt.conf(5) (David Kalnischkies)
- Handle EINTR in the static FileFd::Write overload (David Kalnischkies)
- Support building without gnutls (Steve Langasek)
- Resolves rhbz#2270952

* Tue Feb 20 2024 Packit <hello@packit.dev> - 2.7.12-1
- Release 2.7.12 (Julian Andres Klode)
- Move systemd units to /usr/lib (Julian Andres Klode)
- test-snapshot: Add test case for automatic snapshot (Julian Andres Klode)
- test-snapshot: Fix a test case (Julian Andres Klode)
- Delete SHADOWED metaIndex if we don't actually use snapshots (Julian Andres Klode)
- Automatically enable snapshots where supported (Julian Andres Klode)
- Modernize standard library includes (Julian Andres Klode)
- Bump Ubuntu apt-key deprecation notice to 24.04 (Julian Andres Klode)

* Tue Feb 13 2024 Sérgio M. Basto <sergio@serjux.com> - 2.7.11-1
- Release 2.7.11 (Julian Andres Klode)
- Show a separate list of upgrades deferred due to phasing (Julian Andres Klode)
- Add the ?security pattern (Julian Andres Klode)
- Add a new ?phasing pattern (Julian Andres Klode)
- Add public phased update API (Julian Andres Klode)
- For phasing, check if current version is a security update, not just previous ones (Julian Andres Klode)
- Support -a for setting host architecture in apt-get source -b (David Kalnischkies)
- Remove erroneous -a flag from apt-get synopsis in manpage (David Kalnischkies)

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.7.6-1
- Update to 2.7.6 (#2239816)

* Sat Sep 16 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.7.5-1
- Update to 2.7.5 (#2222361)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jun 24 2023 Sérgio Basto <sergio@serjux.com> - 2.7.1-2
- Migrate to SPDX license format

* Mon Jun 12 2023 Mosaab Alzoubi <moceap[At]fedoraproject[Dot]org> - 2.7.1-1
- Update to 2.7.1

* Thu Feb 23 2023 Sérgio Basto <sergio@serjux.com> - 2.5.6-1
- Update apt to 2.5.6 (#2168285)

* Wed Jan 25 2023 Sérgio Basto <sergio@serjux.com> - 2.5.5-1
- Update apt to 2.5.5 (#2161700)
- Fix build with gcc13

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 23 2022 Sérgio Basto <sergio@serjux.com> - 2.5.4-1
- Update apt to 2.5.4 (#2138830)

* Mon Oct 03 2022 Sérgio Basto <sergio@serjux.com> - 2.5.3-1
- Update apt to 2.5.3 (#2130611)

* Fri Aug 05 2022 Sérgio Basto <sergio@serjux.com> - 2.5.2-1
- Update apt to 2.5.2 (#2087682)

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 14 2022 Sérgio Basto <sergio@serjux.com> - 2.4.5-1
- Update apt to 2.4.5 (#2049183)

* Sat Feb 12 2022 Jeff Law <jeffreyalaw@gmail.com> - 2.3.14-3
- Re-enable LTO

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 16 2022 Sérgio Basto <sergio@serjux.com> - 2.3.14-1
- Update apt to 2.3.14 (#2037920)

* Sat Dec 18 2021 Sérgio Basto <sergio@serjux.com> - 2.3.13-1
- Update apt to 2.3.13 (#2024297)

* Thu Oct 21 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.3.11-1
- Update to 2.3.11 (#2002944)

* Sat Aug 14 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.3.8-1
- Update to 2.3.8 (#1993644)

* Thu Jul 29 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.3.7-1
- Update to 2.3.7 (#1987763)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 09 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.3.6-1
- Update to 2.3.6 (#1969935)

* Mon May 17 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.3.5-1
- Update to 2.3.5 (#1930430)

* Mon Feb 15 2021 Mosaab Alzoubi <moceap[At]hotmail[Dot]com> - 2.1.20-1
- Update to 2.1.20

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.1.18-1
- Update to 2.1.18 (#1906457)

* Mon Nov 23 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.1.12-1
- Update to 2.1.12 (#1900787)

* Wed Oct 21 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.1.11-1
- Update to 2.1.11 (#1890077)

* Tue Aug 11 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.1.10-1
- Update to 2.1.10 (#1868031)

* Mon Aug 10 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.1.9-1
- Update to 2.1.9 (#1867591)

* Tue Aug 04 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.1.8-1
- Update to 2.1.8 (#1865853)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.7-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Jeff law <law@redhat.com> - 2.1.7-3
- Disable LTO for now

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Sérgio Basto <sergio@serjux.com> - 2.1.7-1
- Update apt to 2.1.7 (#1854759)

* Wed Jun 03 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.1.6-1
- Update to 2.1.6 (#1831062)

* Tue May 26 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.1.5-1
- Update to 2.1.5 (#1831062)

* Tue May 19 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.1.4-1
- Update to 2.1.4 (#1831062)

* Thu Apr 09 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2 (#1816610)

* Sat Mar 07 17:26:29 EST 2020 Neal Gompa <ngompa13@gmail.com> - 2.0.0-1
- Update to 2.0.0

* Tue Feb 18 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1.9.10-1
- Update to 1.9.10 (#1804170)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 09:50:33 EST 2020 Neal Gompa <ngompa13@gmail.com> - 1.9.7-1
- Update to 1.9.7
- Rename apt-devel-doc to apt-apidoc to better reflect the content

* Mon Dec 16 22:10:42 EST 2019 Neal Gompa <ngompa13@gmail.com> - 1.9.4-1
- Switch from apt-rpm to apt from Debian and rebase to v1.9.4
  + This drops rpm support from apt
- Truncate changelog due to complete spec rewrite and replacement of apt implementation
