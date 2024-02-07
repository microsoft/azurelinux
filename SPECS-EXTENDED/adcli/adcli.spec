%define _hardened_build 1
Summary:        Active Directory enrollment
Name:           adcli
Version:        0.9.2
Release:        2%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://gitlab.freedesktop.org/realmd/adcli
Source0:        https://gitlab.freedesktop.org/realmd/adcli/uploads/ea560656ac921b3fe0d455976aaae9be/adcli-%{version}.tar.gz
BuildRequires:  cyrus-sasl-devel
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  intltool
BuildRequires:  krb5-devel
BuildRequires:  libtool
BuildRequires:  libxslt
BuildRequires:  make
BuildRequires:  openldap-devel
BuildRequires:  xmlto
Requires:       cyrus-sasl-gssapi
Conflicts:      adcli-doc < %{version}-%{release}
# adcli no longer has a library of development files
# the adcli tool itself is to be used by callers
Obsoletes:      adcli-devel < 0.5

%description
adcli is a tool for joining an Active Directory domain using
standard LDAP and Kerberos calls.

%prep
%autosetup -p1

%build
autoreconf --force --install --verbose
%configure --disable-static --disable-silent-rules %{nil}
%make_build

%check
%make_build check

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%ldconfig_scriptlets

%files
%{_sbindir}/adcli
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%doc %{_mandir}/*/*

%package doc
Summary:        adcli documentation
Conflicts:      adcli < %{version}-%{release}
BuildArch:      noarch

%description doc
adcli is a tool for joining an Active Directory domain using
standard LDAP and Kerberos calls. This package contains its
documentation.

%files doc
%doc %{_datadir}/doc/adcli/*

%changelog
* Wed Nov 02 2022 Sumedh Sharma <sumsharma@microsoft.com> - 0.9.2-2
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Remove unsed configuration flags in build
- Fix BR to add cyrus-sasl-devel
- License verified

* Thu Sep 29 2022 Sumit Bose <sbose@redhat.com> - 0.9.2-1
- Update to upstream release 0.9.2

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 28 2021 Sumit Bose <sbose@redhat.com> - 0.9.1-9
- Add ns_get16() and ns_get32() to configure check
  Resolves: rhbz#1984891

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Sumit Bose <sbose@redhat.com> - 0.9.1-7
- Add user-passwd sub-command
- Add setattr/delattr option

* Thu Jun 03 2021 Sumit Bose <sbose@redhat.com> - 0.9.1-6
- Add fix for dont-expire-password option

* Wed Jun 02 2021 Sumit Bose <sbose@redhat.com> - 0.9.1-5
- Add dont-expire-password option and coverity fixes

* Wed Apr 07 2021 Sumit Bose <sbose@redhat.com> - 0.9.1-4
- Add macro updates for autoconf-2.71 and downstream gating

* Mon Mar 29 2021 Sumit Bose <sbose@redhat.com> - 0.9.1-3
- Add vendor error message
  Resolves: rhbz#1889386

* Sat Feb 20 2021 Sumit Bose <sbose@redhat.com> - 0.9.1-2
- Add Conflicts to avoid update/downgrade issues

* Sat Feb 20 2021 Sumit Bose <sbose@redhat.com> - 0.9.1-1
- Update to upstream release 0.9.1

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 13 2020 Sumit Bose <sbose@redhat.com> - 0.9.0-6
- Include the latest upstream patches with use-ldaps fixes, man page
  improvements and a new sub-command to create managed service accounts

* Thu Aug 13 2020 Sumit Bose <sbose@redhat.com> - 0.9.0-5
- man page and help output fixes

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 08 2020 Sumit Bose <sbose@redhat.com> - 0.9.0-2
- Include the latest upstream patches

* Wed Mar 18 2020 Sumit Bose <sbose@redhat.com> - 0.9.0-1
- Update to upstream release 0.9.0 and latest patches

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 26 2019 Sumit Bose <sbose@redhat.com> - 0.8.2-8
- various fixes and improvements
  Resolves: rhbz#1683745, rhbz#1738573

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul  5 2019 Jakub Hrozek <jhrozek@redhat.com> - 0.8.2-6
- Resolves: rhbz#1727144 - adcli join fails with new krb5-libs; adcli
                           needs to backport patches to only use permitted
                           enctypes from upstream

* Tue Apr 30 2019 Sumit Bose <sbose@redhat.com> - 0.8.2-5
- addition patch for rhbz#1630187 and new ones for rhbz#1588596
  Resolves: rhbz#1630187, rhbz#1588596

* Fri Mar 22 2019 Sumit Bose <sbose@redhat.com> - 0.8.2-4
- various fixes and improvements
  Resolves: rhbz#1593240, rhbz#1608212, rhbz#1547014, rhbz#1547014,
            rhbz#1649868, rhbz#1588596, rhbz#1642546, rhbz#1595911,
            rhbz#1644311, rhbz#1337489, rhbz#1630187, rhbz#1622583

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Sumit Bose <sbose@redhat.com> - 0.8.0-1
- Update to upstream release 0.8.2
- various other fixes and improvements
- add option to enable "Trust this computer for delegation"
  Resolves: rhbz#988349
- fix typos in the adcli man page
  Resolves: rhbz#1440533

* Wed Mar 07 2018 Sumit Bose <sbose@redhat.com> - 0.8.0-7
- Added BuildRequires gcc

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Sumit Bose <sbose@redhat.com> - 0.8.0-1
- Update to upstream release 0.8.0

* Mon Oct 19 2015 Stef Walter <stefw@redhat.com> - 0.7.6-1
- Fix issue with keytab use with sshd
- Resolves: rhbz#1267319
- Put documentation in a subpackage

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 30 2014 Stef Walter <stefw@redhat.com> - 0.7.5-2
- Fix incorrect ownership of manual page directory

* Fri Sep 13 2013 Stef Walter <stefw@redhat.com> - 0.7.5-1
- Update to upstream point release 0.7.5
- Workaround for discovery via IPv6 address
- Correctly put IPv6 addresses in temporary krb5.conf

* Mon Sep 09 2013 Stef Walter <stefw@redhat.com> - 0.7.4-1
- Update to upstream point release 0.7.4
- Correctly handle truncating long host names
- Try to contact all available addresses for discovery
- Build fixes

* Wed Aug 07 2013 Stef Walter <stefw@redhat.com> - 0.7.3-1
- Update to upstream point release 0.7.3
- Don't try to set encryption types on Windows 2003

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Stef Walter <stefw@redhat.com> - 0.7.2-1
- Update to upstream point release 0.7.2
- Part of fix for bug [#961244]

* Mon Jul 15 2013 Stef Walter <stefw@redhat.com> - 0.7.1-4
- Build with verbose output logging

* Tue Jun 11 2013 Stef Walter <stefw@redhat.com> - 0.7.1-3
- Run 'make check' when building the package

* Mon May 13 2013 Stef Walter <stefw@redhat.com> - 0.7.1-2
- Bump version to get around botched update

* Mon May 13 2013 Stef Walter <stefw@redhat.com> - 0.7.1-1
- Update to upstream 0.7.1 release
- Fix problems with salt discovery [#961399]

* Mon May 06 2013 Stef Walter <stefw@redhat.com> - 0.7-1
- Work around broken krb5 with empty passwords [#960001]
- Fix memory corruption issue [#959999]
- Update to 0.7, fixing various bugs

* Mon Apr 29 2013 Stef Walter <stefw@redhat.com> - 0.6-1
- Update to 0.6, fixing various bugs

* Wed Apr 10 2013 Stef walter <stefw@redhat.com> - 0.5-2
- Add appropriate Obsoletes line for libadcli removal

* Wed Apr 10 2013 Stef Walter <stefw@redhat.com> - 0.5-1
- Update to upstream 0.5 version
- No more libadcli, and thus no adcli-devel
- Many new adcli commands
- Documentation

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Stef Walter <stefw@redhat.com> - 0.4-1
- Update for 0.4 version, fixing various bugs

* Sat Oct 20 2012 Stef Walter <stefw@redhat.com> - 0.3-1
- Update for 0.3 version

* Tue Sep 4 2012 Stef Walter <stefw@redhat.com> - 0.2-1
- Update for 0.2 version

* Wed Aug 15 2012 Stef Walter <stefw@redhat.com> - 0.1-1
- Initial 0.1 package
