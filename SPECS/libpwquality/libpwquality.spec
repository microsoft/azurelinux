# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: A library for password generation and password quality checking
Name: libpwquality
Version: 1.4.5
Release: 14%{?dist}
URL: https://github.com/libpwquality/libpwquality/
Source0: https://github.com/libpwquality/libpwquality/releases/download/libpwquality-%{version}/libpwquality-%{version}.tar.bz2

# Use setuptools instead of distutils
# This fixes the build with Python 3.12+
# https://bugzilla.redhat.com/2165572
# Upstream PR: https://github.com/libpwquality/libpwquality/pull/74
Patch1: setuptools.patch

# The package is BSD licensed with option to relicense as GPLv2+
# - this option is redundant as the BSD license allows that anyway.
License: BSD-3-Clause OR GPL-2.0-or-later

%global _moduledir %{_libdir}/security
%global _secconfdir %{_sysconfdir}/security

# This allows minimal installs to not drag in the big wordlist package
# but anyone doing this should be careful as it causes various
# password set/change operations to fail
Recommends: cracklib-dicts >= 2.8

BuildRequires: gcc make
BuildRequires: cracklib-devel
BuildRequires: gettext
BuildRequires: pam-devel
BuildRequires: python3-devel
BuildRequires: python3-setuptools

%description
This is a library for password quality checks and generation
of random passwords that pass the checks.
This library uses the cracklib and cracklib dictionaries
to perform some of the checks.

%package devel
Summary: Support for development of applications using the libpwquality library
Requires: libpwquality%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files needed for development of applications using the libpwquality
library.
See the pwquality.h header file for the API.

%package -n python3-pwquality
Summary: Python bindings for the libpwquality library
Requires: libpwquality%{?_isa} = %{version}-%{release}

%description -n python3-pwquality
This is pwquality Python module that provides Python bindings
for the libpwquality library. These bindings can be used
for easy password quality checking and generation of random
pronounceable passwords from Python applications.

%prep
%autosetup -p1

%build
%configure \
	--with-securedir=%{_moduledir} \
	--with-pythonsitedir=%{python3_sitearch} \
	--with-python-binary=%{__python3} \
	--disable-static

%make_build

%install
%make_install

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_moduledir}/*.la
mkdir %{buildroot}%{_secconfdir}/pwquality.conf.d

%find_lang libpwquality

%check
# Nothing yet

%ldconfig_scriptlets

%files -f libpwquality.lang
%license COPYING
%doc README NEWS AUTHORS
%{_bindir}/pwmake
%{_bindir}/pwscore
%dir %{_moduledir}
%{_moduledir}/pam_pwquality.so
%{_libdir}/libpwquality.so.*
%dir %{_secconfdir}
%config(noreplace) %{_secconfdir}/pwquality.conf
%dir %{_secconfdir}/pwquality.conf.d
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%{_includedir}/pwquality.h
%{_libdir}/libpwquality.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%files -n python3-pwquality
%{python3_sitearch}/*.so
%{python3_sitearch}/*.egg-info

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.4.5-13
- Rebuilt for Python 3.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.4.5-10
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Aug 04 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1.4.5-7
- migrated to SPDX license

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.4.5-5
- Rebuilt for Python 3.12

* Fri Mar 31 2023 Miro Hrončok <mhroncok@redhat.com> - 1.4.5-4
- Use setuptools instead of distutils to build this package
- Resolves: rhbz#2165572

* Wed Feb 01 2023 Adam Williamson <awilliam@redhat.com> - 1.4.5-3
- Strengthen cracklib-dicts dependency to Recommends (#2158891)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 22 2022 Paul Wouters <paul.wouters@aiven.io - 1.4.5-1
- Resolves: rhbz#2154991 libpwquality fails to build with Python 3.12: ModuleNotFoundError: No module named 'distutils'
- Resolves: rhbz#2006063 RFE: Support running without cracklib-dicts installed
- Cleanup and remove python2/3 conditional macros

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.4.4-10
- Rebuilt for Python 3.11

* Fri Mar 04 2022 Karolina Surma <ksurma@redhat.com> - 1.4.4-9
- Don't BR setuptools, use Python's bundled distutils

* Wed Feb 16 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4.4-8
- Co-own security directory instead of pulling in pam (#2018913)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 11 2021 Paul Wouters <paul.wouters@aiven.io> - 1.4.4-6
- Resolves: rhbz#1992607 libpwquality: regression in minimal image size because of hard dependency on cracklib-dicts

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.4.4-4
- Rebuilt for Python 3.10

* Thu Mar 11 2021 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1.4.4-3
- Resolves: rhbz#1919026 libpwquaily rpm requires cracklib to function but RPM missing requirement [updated]

* Tue Jan 26 10:55:14 EST 2021 Paul Wouters <pwouters@redhat.com> - 1.4.4-2
- Resolves rhbz#1919026 libpwquaily rpm requires cracklib-dict to function but RPM missing requirement

* Tue Oct 13 2020 Tomáš Mráz <tmraz@redhat.com> 1.4.4-1
- Translation updates
- Fix regression with enabling the cracklib check during build

* Mon Oct 12 2020 Tomáš Mráz <tmraz@redhat.com> 1.4.3-1
- Multiple translation updates
- Add usersubstr check for substrings of N characters from the username
  patch by Danny Sauer

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 1.4.2-4
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Thu Oct 31 2019 Tomáš Mráz <tmraz@redhat.com> 1.4.2-1
- Fix previous release regression in handling retry, enforce_for_root,
  and local_users_only options

* Tue Sep 17 2019 Tomáš Mráz <tmraz@redhat.com> 1.4.1-1
- Disable python2 bindings in Fedora 31 and above
- Add conditionals for Python2 and Python3
- pam_pwquality: Abort the retry loop if user requests it
- Allow setting retry, enforce_for_root, and local_users_only options
  in the pwquality.conf config file

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.0-5
- Switch to %%ldconfig_scriptlets

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4.0-4
- Python 2 binary package renamed to python2-pwquality
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Fri May 26 2017 Tomáš Mráz <tmraz@redhat.com> 1.4.0-1
- Do not try to check presence of too short username in password
- Make the user name check optional (via usercheck option)
- Add an 'enforcing' option to make the checks to be warning-only
  in PAM
- The difok = 0 setting will disable all old password similarity
  checks except new and old passwords being identical
- Updated translations from Zanata

* Mon Aug 24 2015 Tomáš Mráz <tmraz@redhat.com> 1.3.0-2
- Fix possible stack overflow in the generate function (#1255935)

* Thu Jul 23 2015 Tomáš Mráz <tmraz@redhat.com> 1.3.0-1
- Change the defaults for credits, difok, and minlen
- Make the cracklib check optional but on by default
- Add implicit support for parsing  <cfgfile>.d/*.conf files
- Add libpwquality API manual page

* Wed Aug  6 2014 Tomáš Mráz <tmraz@redhat.com> 1.2.4-1
- fix license handling (by Tom Callaway)
- add Python3 module subpackage

* Thu Sep 12 2013 Tomáš Mráz <tmraz@redhat.com> 1.2.3-1
- fix problem with parsing the pam_pwquality options
  patch by Vladimir Sorokin.
- updated translations from Transifex
- treat empty user or password as NULL
- move the library to /usr

* Wed Jun 19 2013 Tomas Mraz <tmraz@redhat.com> 1.2.2-1
- manual page fixes
- make it possible to set the maxsequence configuration value
- updated translations from Transifex

* Thu Dec 20 2012 Tomas Mraz <tmraz@redhat.com> 1.2.1-1
- properly free pwquality settings
- add extern "C" to public header
- updated translations from Transifex

* Thu Aug 16 2012 Tomas Mraz <tmraz@redhat.com> 1.2.0-1
- add maxsequence check for too long monotonic character sequence.
- clarified alternative licensing to GPLv2+.
- add local_users_only option to skip the pwquality checks for
  non-locals. (thanks to Stef Walter)

* Wed Jun 13 2012 Tomas Mraz <tmraz@redhat.com> 1.1.1-1
- use rpm built-in filtering of provides (rhbz#830153)
- remove strain debug fprintf() (rhbz#831567)

* Thu May 24 2012 Tomas Mraz <tmraz@redhat.com> 1.1.0-1
- fix leak when throwing PWQError exception
- added pkgconfig file
- call the simplicity checks before the cracklib check
- add enforce_for_root option to the PAM module
- updated translations from Transifex

* Thu Dec  8 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0-1
- added a few additional password quality checks
- bugfix in configuration file parsing

* Fri Nov 11 2011 Tomas Mraz <tmraz@redhat.com> 0.9.9-1
- added python bindings and documentation

* Mon Oct 10 2011 Tomas Mraz <tmraz@redhat.com> 0.9-2
- fixes for problems found in review (missing BR on pam-devel,
  License field, Source URL, Require pam, other cleanups)

* Mon Oct  3 2011 Tomas Mraz <tmraz@redhat.com> 0.9-1
- first spec file for libpwquality
