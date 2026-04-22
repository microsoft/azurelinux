# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Force out of source build
%undefine __cmake_in_source_build

%global min_libzypp_ver 17.37.12

Name:           zypper
Version:        1.14.94
Release: 2%{?dist}
Summary:        Command line package manager using libzypp

# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
URL:            http://en.opensuse.org/Portal:Zypper
Source0:        https://github.com/openSUSE/zypper/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  %{_bindir}/asciidoctor
BuildRequires:  %{_bindir}/xsltproc
BuildRequires:  cmake >= 3.5
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  perl-generators
BuildRequires:  glibc-all-langpacks
BuildRequires:  augeas-devel
BuildRequires:  boost-devel
BuildRequires:  gettext-devel
BuildRequires:  readline-devel
BuildRequires:  libxml2-devel
BuildRequires:  libzypp-devel >= %{min_libzypp_ver}
Requires:       libzypp%{?_isa} >= %{min_libzypp_ver}

# Blech, apparently we don't want bash-completion always... Cf. rhbz#1652183
Recommends:     bash-completion

Recommends:     logrotate
Recommends:     cron
Recommends:     zypper-log

# Zypper specific virtual provides
Provides:       zypper(oldpackage)
Provides:       zypper(updatestack-only)
Provides:       zypper(auto-agree-with-product-licenses)
Provides:       zypper(purge-kernels)
Provides:       zypper(include-all-archs)


%description
Zypper is a command line package manager tool using libzypp,
which can be used to manage software for RPM based systems.

%package log
Summary:        Zypper log file command line tool
Requires:       %{name} = %{version}-%{release}
Requires:       xz
BuildArch:      noarch

%description log
This package provides a command line tool for
accessing the Zypper log file.


%package aptitude
Summary:        apt/aptitude CLI compatibility interface for Zypper
Provides:       %{name}-apt = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
Enhances:       zypper
BuildArch:      noarch

%description aptitude
This package provides apt-get and aptitude frontends for Zypper,
for those used to the Debian package manager's CLI structure.

These can be accessed with either of the following:
* %{_bindir}/zypp-apt-get
* %{_bindir}/zypp-aptitude

%prep
%autosetup -p1

# Use correct libexecdir
find -type f -exec sed -i -e "s|/usr/lib/zypper|%{_libexecdir}/zypper|g" {} ';'
find -type f -exec sed -i -e "s|\${CMAKE_INSTALL_PREFIX}/lib/zypper|\${CMAKE_INSTALL_PREFIX}/libexec/zypper|g" {} ';'
find -type f -exec sed -i -e "s|\${CMAKE_INSTALL_PREFIX}/lib/\${PACKAGE}|\${CMAKE_INSTALL_PREFIX}/libexec/\${PACKAGE}|g" {} ';'

# Use correct docdir
find -type f -exec sed -i -e "s|\${INSTALL_PREFIX}/share/doc/packages/\${PACKAGE}|\${INSTALL_PREFIX}/share/doc/\${PACKAGE}|g" {} ';'

%build
%cmake  -DCMAKE_BUILD_TYPE=RelWithDebInfo -DDOC_INSTALL_DIR=%{_docdir} -DENABLE_BUILD_TESTS=ON -DENABLE_BUILD_TRANS=ON
%cmake_build


%install
%cmake_install

mkdir -p %{buildroot}%{_libexecdir}/zypper/commands

%find_lang %{name}

install -dm 0755 %{buildroot}%{_localstatedir}/log
touch %{buildroot}%{_localstatedir}/log/zypper.log

# Remove conflict with apt
mv %{buildroot}%{_bindir}/aptitude %{buildroot}%{_bindir}/zypp-aptitude
# Redo the symlink to point to the new binary name
rm %{buildroot}%{_bindir}/apt-get
ln -sf zypp-aptitude %{buildroot}%{_bindir}/zypp-apt-get
rm %{buildroot}%{_bindir}/apt
ln -sf zypp-aptitude %{buildroot}%{_bindir}/zypp-apt

%if "%{_sbindir}" != "/usr/sbin"
# If sbin-bin merge, move everything accordingly
mv %{buildroot}%{_prefix}/sbin/* %{buildroot}%{_sbindir}
rmdir %{buildroot}%{_prefix}/sbin
%endif

# Remove conflicting man page and rename needs-restarting
rm %{buildroot}%{_mandir}/man1/needs-restarting.1*
mv %{buildroot}%{_bindir}/needs-restarting %{buildroot}%{_bindir}/zypp-needs-restarting

%check
pushd %{_vpath_builddir}/tests
ctest -VV --output-on-failure .
popd

%files -f %{name}.lang
%license COPYING
%doc %{_docdir}/zypper/*
%config(noreplace) %{_sysconfdir}/zypp/zypper.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zypper.lr
%config(noreplace) %{_sysconfdir}/logrotate.d/zypp-refresh.lr
# Co-own bash-completion directories... Cf. rhbz#1652183
## This really should be owned by filesystem...
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/zypper
%{_bindir}/zypper
%{_bindir}/installation_sources
%{_bindir}/zypp-needs-restarting
%{_sbindir}/zypp-refresh
%{_datadir}/zypper/
%{_libexecdir}/zypper/
%{_mandir}/man8/zypper.8.*
%{_mandir}/man8/zypp-refresh.8.*
%ghost %config(noreplace) %attr(640,root,root) %{_localstatedir}/log/zypper.log

%files log
%{_sbindir}/zypper-log
%{_mandir}/man8/zypper-log.8.*

%files aptitude
%{_bindir}/zypp-aptitude
%{_bindir}/zypp-apt-get
%{_bindir}/zypp-apt
%dir %{_sysconfdir}/zypp/apt-packagemap.d/
%config(noreplace) %{_sysconfdir}/zypp/apt-packagemap.d/*


%changelog
* Fri Jan 16 2026 Neal Gompa <ngompa@fedoraproject.org> - 1.14.94-1
- Update to 1.14.94

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.88-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Mar 19 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.14.88-1
- Rebase to 1.14.88

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.73-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 1.14.73-3
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.73-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 05 2024 Neal Gompa <ngompa@fedoraproject.org> - 1.14.73-1
- Update to 1.14.73

* Sun Apr 14 2024 Neal Gompa <ngompa@fedoraproject.org> - 1.14.68-2
- Rebuild for libzypp-tui soname fix

* Mon Mar 04 2024 Neal Gompa <ngompa@fedoraproject.org> - 1.14.68-1
- Update to 1.14.68

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 09 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.14.59-1
- Update to 1.14.59

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep 02 2022 Neal Gompa <ngompa@fedoraproject.org> - 1.14.55-1
- Update to 1.14.55 (#1932773)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.42-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.42-5
- Perl 5.36 rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.42-2
- Perl 5.34 rebuild

* Thu Feb 11 2021 Neal Gompa <ngompa13@gmail.com> - 1.14.42-1
- Update to 1.14.42 (#1823433)

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 08 2020 Neal Gompa <ngompa13@gmail.com> - 1.14.37-1
- Update to 1.14.37 (#1823433)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.35-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.35-3
- Perl 5.32 rebuild

* Fri Mar 20 2020 Neal Gompa <ngompa13@gmail.com> - 1.14.35-2
- Backport fixup commit for building with C++17

* Fri Mar 20 2020 Neal Gompa <ngompa13@gmail.com> - 1.14.35-1
- Update to 1.14.35 (#1805837)

* Sat Mar 07 2020 Neal Gompa <ngompa13@gmail.com> - 1.14.34-1
- Update to 1.14.34

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Neal Gompa <ngompa13@gmail.com> - 1.14.33-1
- Update to 1.14.33 (#1777955)

* Tue Nov 12 2019 Neal Gompa <ngompa13@gmail.com> - 1.14.32-1
- Update to 1.14.32 (#1747529)

* Tue Aug 27 2019 Neal Gompa <ngompa13@gmail.com> - 1.14.29-1
- Update to 1.14.29 (#1719278)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.27-3
- Perl 5.30 rebuild

* Tue May 28 2019 Björn Esser <besser82@fedoraproject.org> - 1.14.27-2
- Rebuilt (libzypp)

* Mon Mar 25 2019 Björn Esser <besser82@fedoraproject.org> - 1.14.27-1
- Rebase to 1.14.27 (#1680605)

* Mon Mar 25 2019 Björn Esser <besser82@fedoraproject.org> - 1.14.25-5
- Explicitly enable translation on CMake command line

* Mon Mar 25 2019 Björn Esser <besser82@fedoraproject.org> - 1.14.25-4
- Explicitly enable tests on CMake command line

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.14.25-3
- Rebuild for readline 8.0

* Tue Feb 12 2019 Neal Gompa <ngompa13@gmail.com> - 1.14.25-2
- Downgrade bash-completion dependency to Recommends (#1652183)

* Tue Feb 12 2019 Neal Gompa <ngompa13@gmail.com> - 1.14.25-1
- Rebase to 1.14.25 (#1667664)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Nov 03 2018 Neal Gompa <ngompa13@gmail.com> - 1.14.15-1
- Update to 1.14.15

* Sun Aug 26 2018 Neal Gompa <ngompa13@gmail.com> - 1.14.8-1
- Update to 1.14.8 (#1555114)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.3-2
- Perl 5.28 rebuild

* Sun Mar 04 2018 Neal Gompa <ngompa13@gmail.com> - 1.14.3-1
- Update to 1.14.3 (#1550768)

* Wed Feb 07 2018 Neal Gompa <ngompa13@gmail.com> - 1.14.2-1
- Update to 1.14.2 (#1489428)
- Backport patch to fix build with GCC 8

* Sun Sep 03 2017 Neal Gompa <ngompa13@gmail.com> - 1.13.32-1
- Update to 1.13.32 (#1485336)

* Thu Aug 17 2017 Neal Gompa <ngompa13@gmail.com> - 1.13.31-1
- Update to 1.13.31 (#1480827)

* Sun Aug 06 2017 Neal Gompa <ngompa13@gmail.com> - 1.13.30-1
- Update to 1.13.30 (#1470434)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Neal Gompa <ngompa13@gmail.com> - 1.13.28-1
- Update to 1.13.28 (#1444590)

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.13.22-2
- Perl 5.26 rebuild

* Mon Apr 17 2017 Neal Gompa <ngompa13@gmail.com> - 1.13.22-1
- Update to 1.13.22
- Fix zypp-apt-get symlink
- Add missing (Build)Requires for zypper-aptitude
- Move bash completion file and add bash-completion Requires

* Fri Mar 31 2017 Neal Gompa <ngompa13@gmail.com> - 1.13.21-1
- Update to 1.13.21
- Drop merged patches
- Use correct libexecdir
- Use correct docdir

* Fri Feb 24 2017 Neal Gompa <ngompa13@gmail.com> - 1.13.19-1
- Update to 1.13.19
- Bump required libzypp version
- Backport patch from upstream to fix building tests

* Mon Dec 12 2016 Neal Gompa <ngompa13@gmail.com> - 1.13.14-1
- Update to 1.13.14
- Bump required libzypp version

* Sat Aug 27 2016 Neal Gompa <ngompa13@gmail.com> - 1.13.9-3
- Bump to rebuild against libzypp-16.2.2-3 to add suserepo support

* Thu Aug 25 2016 Neal Gompa <ngompa13@gmail.com> - 1.13.9-2
- Bump to rebuild against libzypp-16.2.2-2

* Wed Aug 24 2016 Neal Gompa <ngompa13@gmail.com> - 1.13.9-1
- Update to 1.13.9
- Bump required libzypp version

* Fri Jun 10 2016 Neal Gompa <ngompa13@gmail.com> - 1.13.2-1
- Update to 1.13.2

* Tue Apr 26 2016 Neal Gompa <ngompa13@gmail.com> - 1.13.0-2
- Rebuild against libzypp-15.22.0

* Wed Apr  6 2016 Neal Gompa <ngompa13@gmail.com> - 1.13.0-1
- Update to 1.13.0

* Thu Feb  4 2016 Neal Gompa <ngompa13@gmail.com> - 1.12.32-1
- Update to 1.12.32

* Mon Feb  1 2016 Neal Gompa <ngompa13@gmail.com> - 1.12.30-1
- Initial packaging
