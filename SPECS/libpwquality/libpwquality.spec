# This spec is adapted from the spec in libpwquality-1.4.2.tar.bz2

Summary:        A library for password generation and password quality checking
Name:           libpwquality
Version:        1.4.5
Release:        1%{?dist}
License:        BSD OR GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/libpwquality/libpwquality/
Source0:        https://github.com/libpwquality/libpwquality/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
%global _pwqlibdir %{_libdir}
%global _moduledir %{_libdir}/security
%global _secconfdir %{_sysconfdir}/security
%global __python3 \/usr\/bin\/python3
%define python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")
# we don't want to provide private python extension libs
%define __provides_exclude_from ^(%{python_sitearch}|%{python3_sitearch})/.*\.so$.
BuildRequires:  cracklib-devel
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  pam-devel
BuildRequires:  python3-devel
Requires:       pam

%description
This is a library for password quality checks and generation
of random passwords that pass the checks.
This library uses the cracklib and cracklib dictionaries
to perform some of the checks.

%package devel
Summary:        Support for development of applications using the libpwquality library
Requires:       libpwquality%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Files needed for development of applications using the libpwquality
library.
See the pwquality.h header file for the API.

%package -n python3-pwquality
Summary:        Python bindings for the libpwquality library
Requires:       libpwquality%{?_isa} = %{version}-%{release}

%description -n python3-pwquality
This is pwquality Python module that provides Python bindings
for the libpwquality library. These bindings can be used
for easy password quality checking and generation of random
pronounceable passwords from Python applications.

%prep
%setup -q

%build
[ -f %{_bindir}/python3 ] || ln -s %{_bindir}/python3 /bin/python

%configure \
	--with-securedir=%{_moduledir} \
	--with-pythonsitedir=%{python3_sitearch} \
	--with-python-binary=%{__python3} \
	--disable-static

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

%if "%{_pwqlibdir}" != "%{_libdir}"
pushd %{buildroot}%{_libdir}
mv libpwquality.so.* %{buildroot}%{_pwqlibdir}
ln -sf %{_pwqlibdir}/libpwquality.so.*.* libpwquality.so
popd
%endif
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_moduledir}/*.la

mkdir %{buildroot}%{_secconfdir}/pwquality.conf.d

%find_lang libpwquality

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f libpwquality.lang
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README NEWS AUTHORS
%{_bindir}/pwmake
%{_bindir}/pwscore
%{_moduledir}/pam_pwquality.so
%{_pwqlibdir}/libpwquality.so.*
%config(noreplace) %{_secconfdir}/pwquality.conf
%{_secconfdir}/pwquality.conf.d
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
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.5-1
- Auto-upgrade to 1.4.5 - Azure Linux 3.0 - package upgrades

* Wed Jan 12 2022 Henry Li <lihl@microsoft.com> - 1.4.4-1
- Upgrade to version 1.4.4

* Sat Nov 21 2020 Thomas Crain <thcrain@microsoft.com> - 1.4.2-6
- Replace %%ldconfig_scriptlets with actual post/postun sections

* Thu Nov 19 2020 Andrew Phelps <anphel@microsoft.com> 1.4.2-5
- Remove empty check section.

* Mon Jun 29 2020 Paul Monson <paulmon@microsoft.com> 1.4.2-4
- Only create python3 symbolic link if /usr/bin/python3 does not exist.

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 1.4.2-3
- Renaming Linux-PAM to pam

* Mon Apr 13 2020 Joe Schmitt <joschmit@microsoft.com> 1.4.2-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Remove python2 build options and force python3.
- License verified.

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
