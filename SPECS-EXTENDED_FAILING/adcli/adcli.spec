Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		adcli
Version:	0.9.0
Release:	2%{?dist}
Summary:	Active Directory enrollment
License:	LGPLv2+
URL:		http://cgit.freedesktop.org/realmd/adcli
Source0:	https://gitlab.freedesktop.org/realmd/adcli/uploads/02d8757266c24fdc10822306582287bf/adcli-%{version}.tar.gz

Patch1:		0001-man-move-note-to-the-right-section.patch
Patch2:		0002-tools-add-show-computer-command.patch
Patch3:		0003-add-description-option-to-join-and-update.patch
Patch4:		0004-Use-GSS-SPNEGO-if-available.patch
Patch5:		0005-add-option-use-ldaps.patch
Patch6:		0006-discovery-fix.patch


BuildRequires:	cyrus-sasl-devel
BuildRequires:	gcc
BuildRequires:	intltool pkgconfig
BuildRequires:	libtool
BuildRequires:	gettext-devel
BuildRequires:	krb5-devel
BuildRequires:	openldap-devel
BuildRequires:	libxslt
BuildRequires:	xmlto

Requires:	cyrus-sasl-gssapi

# adcli no longer has a library of development files
# the adcli tool itself is to be used by callers
Obsoletes:	adcli-devel < 0.5

%description
adcli is a tool for joining an Active Directory domain using
standard LDAP and Kerberos calls.

%define _hardened_build 1

%prep
%autosetup -p1

%build
autoreconf --force --install --verbose
%configure --disable-static --disable-silent-rules
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=%{buildroot}
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets

%files
%{_sbindir}/adcli
%doc AUTHORS COPYING ChangeLog NEWS README
%doc %{_mandir}/*/*

%package doc
Summary: adcli documentation
BuildArch: noarch

%description doc
adcli is a tool for joining an Active Directory domain using
standard LDAP and Kerberos calls. This package contains its
documentation.

%files doc
%doc %{_datadir}/doc/adcli/*

%changelog
* Thu Sep 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Added missing BR on 'cyrus-sasl-devel'.

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
