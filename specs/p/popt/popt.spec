# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global ver 1.19
#%%global snap rc1
%global srcver %{ver}%{?snap:-%{snap}}
%global sover 0

Summary:        C library for parsing command line parameters
Name:           popt
Version:        %{ver}%{?snap:~%{snap}}
Release:        9%{?dist}
# COPYING:      MIT text
# po/eo.po:     LicenseRef-Fedora-Public-Domain
# po/fi.po:     MIT AND LicenseRef-Fedora-Public-Domain
# po/lv.po:     MIT AND LicenseRef-Fedora-Public-Domain
# popt.3:       MIT ("the X consortium license, see the file COPYING")
License:        MIT AND LicenseRef-Fedora-Public-Domain
URL:            https://github.com/rpm-software-management/popt/
Source0:        http://ftp.rpm.org/popt/releases/popt-1.x/%{name}-%{srcver}.tar.gz
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  make

%description
Popt is a C library for parsing command line parameters. Popt was
heavily influenced by the getopt() and getopt_long() functions, but
it improves on them by allowing more powerful argument expansion.
Popt can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments. Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

%package devel
Summary:        Development files for the popt library
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}, pkgconfig

%description devel
The popt-devel package includes header files and libraries necessary
for developing programs which use the popt C library. It contains the
API documentation of the popt library, too.

%if 0%{!?_without_static:1}
%package static
Summary:        Static library for parsing command line parameters
License:        MIT
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The popt-static package includes static libraries of the popt library.
Install it if you need to link statically with libpopt.
%endif

%prep
%autosetup -n %{name}-%{srcver} -p1

%build
%configure %{?_without_static:--disable-static}
%make_build

%install
%make_install

# Multiple popt configurations are possible
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/popt.d/

%find_lang %{name}

%check
make check || (cat tests/*.log; exit 1)

%files -f %{name}.lang
%license COPYING
%{_sysconfdir}/popt.d/
%{_libdir}/libpopt.so.%{sover}*

%files devel
%doc README
%{_libdir}/libpopt.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/popt.h
%{_mandir}/man3/popt.3*

%if 0%{!?_without_static:1}
%files static
%{_libdir}/libpopt.a
%endif

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 23 2023 Petr Pisar <ppisar@redhat.com> - 1.19-4
- Correct a license tag to "MIT AND LicenseRef-Fedora-Public-Domain"

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep 16 2022 Robert Scheck <robert@fedoraproject.org> 1.19-1
- Upgrade to 1.19 (#2127400)

* Wed Aug 24 2022 Panu Matilainen <pmatilai@redhat.com> - 1.19~rc1-4
- Restore the memleak fix now that authselect should be fixed

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.19~rc1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Panu Matilainen <pmatilai@redhat.com> - 1.19~rc1-2
- Temporarily revert a memleak fix due to authselect breakage (#2100287)

* Wed Jun 22 2022 Panu Matilainen <pmatilai@redhat.com> - 1.19~rc1-1
- Rebase to 1.19-rc1 (https://github.com/rpm-software-management/popt/releases/tag/popt-1.19-rc1)
- Remove manual .la cleanup, it's automatic nowadays
- Add a guard against accidental soname changes

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Panu Matilainen <pmatilai@redhat.com> - 1.18-5
- Fix test-suite expectation on rawhide
- Dump test-suite logs for post-mortem on failure

* Sat Mar 06 2021 Robert Scheck <robert@fedoraproject.org> 1.18-4
- Conditionalize static subpackage during build-time

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 24 2020 Panu Matilainen <pmatilai@redhat.com> - 1.18-1
- Update to popt 1.18 final (no changes from rc1)

* Fri May 29 2020 Panu Matilainen <pmatilai@redhat.com> - 1.18~rc1-1
- Rebase to popt 1.18-rc1
- Update URLs to the new upstream

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Panu Matilainen <pmatilai@redhat.com> - 1.16-16
- Use modern build helper macros
- Drop support for pre-usrmove versions (Fedora < 17 and RHEL < 7)
- Erm, dont nuke build-root at beginning of %%install

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.16-13
- Switch to %%ldconfig_scriptlets

* Thu Oct 12 2017 Robert Scheck <robert@fedoraproject.org> 1.16-12
- Added upstream patch to handle glob(3) error returns (#1051685)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Fri Jul 28 2017 Peter Jones <pjones@redhat.com> - 1.16-10
- Make it use %%autosetup -S git
- Fix a memory leak

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 26 2014 Panu Matilainen <pmatilai@redhat.com> - 1.16-4
- Mark license as such, not documentation

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 08 2014 Robert Scheck <robert@fedoraproject.org> 1.16-2
- Added patch to have --help and --usage translatable (#734434)

* Sun Nov 24 2013 Robert Scheck <robert@fedoraproject.org> 1.16-1
- Upgrade to 1.16 (#448286, #999377)
- Tight run-time dependencies between sub-packages via %%{?_isa}
- Added patch for spelling mistakes in popt man page (#675567)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 14 2012 Panu Matilainen <pmatilai@redhat.com> - 1.13-13
- Remove useless doxygen docs to eliminate multilib conflicts (#533829)

* Thu Aug 02 2012 Panu Matilainen <pmatilai@redhat.com> - 1.13-12
- Hack poptBadOption() to return something semi-meaningful on exec alias
  failures (#697435, #710267)
- Run internal test-suite on build, minimal as it might be

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 14 2011 Panu Matilainen <pmatilai@redhat.com>
- Backport upstream patch to fix --opt=<arg> syntax for aliases (#293531)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 16 2010 Robert Scheck <robert@fedoraproject.org> 1.13-7
- Solved multilib problems at doxygen generated files (#517509)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 1.13-5
- Rebuilt against gcc 4.4 and rpm 4.6

* Sun May 25 2008 Robert Scheck <robert@fedoraproject.org> 1.13-4
- Solved multilib problems at doxygen generated files (#342921)

* Wed Feb 20 2008 Robert Scheck <robert@fedoraproject.org> 1.13-3
- Revert the broken bind_textdomain_codeset() patch (#433324)

* Thu Feb 14 2008 Robert Scheck <robert@fedoraproject.org> 1.13-2
- Added patch to work around missing bind_textdomain_codeset()

* Sun Dec 30 2007 Robert Scheck <robert@fedoraproject.org> 1.13-1
- Upgrade to 1.13 (#290531, #332201, #425803)
- Solved multilib problems at doxygen generated files (#342921)

* Thu Aug 23 2007 Robert Scheck <robert@fedoraproject.org> 1.12-3
- Added buildrequirement to graphviz (#249352)
- Backported bugfixes from CVS (#102254, #135428 and #178413)

* Sun Aug 12 2007 Robert Scheck <robert@fedoraproject.org> 1.12-2
- Move libpopt to /lib[64] (#249814)
- Generate API documentation, added buildrequirement to doxygen

* Mon Jul 23 2007 Robert Scheck <robert@fedoraproject.org> 1.12-1
- Changes to match with Fedora Packaging Guidelines (#249352)

* Tue Jul 10 2007 Jeff Johnson <jbj@rpm5.org>
- release popt-1.12 through rpm5.org.

* Sat Jun  9 2007 Jeff Johnson <jbj@rpm5.org>
- release popt-1.11 through rpm5.org.

* Thu Dec 10 1998 Michael Johnson <johnsonm@redhat.com>
- released 1.2.2; see CHANGES

* Tue Nov 17 1998 Michael K. Johnson <johnsonm@redhat.com>
- added man page to default install

* Thu Oct 22 1998 Erik Troan <ewt@redhat.com>
- see CHANGES file for 1.2

* Thu Apr 09 1998 Erik Troan <ewt@redhat.com>
- added ./configure step to spec file
