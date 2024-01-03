Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:        Intrusion detection environment
Name:           aide
Version:        0.18.6
Release:        1%{?dist}
URL:            https://github.com/aide/aide
License:        GPLv2+

Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:        aide.conf
Source2:        README.quickstart
Source3:        aide.logrotate

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  bison flex
BuildRequires:  pcre2-devel
BuildRequires:  libgpg-error-devel libgcrypt-devel
BuildRequires:  zlib-devel
BuildRequires:  libcurl-devel
BuildRequires:  libacl-devel
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  libattr-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  audit-libs-devel
BuildRequires:  autoconf automake libtool

# Patch1: aide-0.16rc1-man.patch
# Patch2: aide-0.16b1-fipsfix.patch
# Patch3: aide-0.16-Use-LDADD-for-adding-curl-library-to-the-linker-comm.patch
#
# Patch4: aide-0.15-syslog-format.patch
# Patch5: aide-0.16-crypto-disable-haval-and-others.patch
# Patch6: coverity.patch
# Patch7: aide-0.16-crash-elf.patch

%description
AIDE (Advanced Intrusion Detection Environment) is a file integrity
checker and intrusion detection program.

%prep
%autosetup -p1
cp -a %{S:2} .

%build
%configure  \
  --disable-static \
  --with-config_file=%{_sysconfdir}/aide.conf \
  --with-gcrypt \
  --with-zlib \
  --with-curl \
  --with-posix-acl \
  --with-selinux \
  --with-xattr \
  --with-e2fsattrs \
  --with-audit
%make_build

%install
%make_install bindir=%{_sbindir}
install -Dpm0644 -t %{buildroot}%{_sysconfdir} %{S:1}
install -Dpm0644 %{S:3} %{buildroot}%{_sysconfdir}/logrotate.d/aide
mkdir -p %{buildroot}%{_localstatedir}/log/aide
mkdir -p -m0700 %{buildroot}%{_localstatedir}/lib/aide

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README contrib/
%doc README.quickstart
%{_sbindir}/aide
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/aide.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/aide
%dir %attr(0700,root,root) %{_localstatedir}/lib/aide
%dir %attr(0700,root,root) %{_localstatedir}/log/aide

%changelog
* Wed Jan 03 2024 Rakshaa Viswanathan <rviswanathan@microsoft.com> - 0.18.6-1
- Bump version to 0.18.6

* Thu Jan 05 2023 Thien Trung Vuong <tvuong@microsoft.com> - 0.16-16
- Updated project URL to Github
- Verified license

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.16-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jun 24 2020 Radovan Sroka <rsroka@redhat.com> 0.16-14
- AIDE breaks when setting report_ignore_e2fsattrs
  Resolves: rhbz#1850276

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 31 2019 Radovan Sroka <rsroka@redhat.com> - 0.16-12
- backport some patches
  Resolves: rhbz#1717140

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 20 2019 Daniel Kopecek <dkopecek@redhat.com> - 0.16-10
- Fix building with curl
  Resolves: rhbz#1674637

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.16-8
- Rebuild with fixed binutils

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.16-6
- Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 05 2017 Radovan Sroka <rsroka@redhat.com> - 0.16-2
- fixed upstream link

* Tue Apr 04 2017 Radovan Sroka <rsroka@redhat.com> - 0.16-1
- rebase to stable v0.16
- specfile cleanup
- make doc readable
  resolves: #1421355
- make aide binary runable for any user
  resolves: #1421351

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-0.3.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 12 2016 Tomas Sykora <tosykora@redhat.com> - 0.16-0.2.rc1
- New upstream devel version

* Mon Jun 20 2016 Tomas Sykora <tosykora@redhat.com> - 0.16-0.1.b1
- New upstream devel version

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jul 25 2015 Till Maas <opensource@till.name> - 0.15.1-11
- Remove prelink dependency because prelink was retired

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 0.15.1-8
- Fix FTBFS with -Werror=format-security (#1036983, #1105942)
- Avoid prelink BR on aarch64, ppc64le (#924977, #1078476)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Daniel Kopecek <dkopecek@redhat.com> - 0.15.1-4
- added patch to fix aide in FIPS mode
- use only FIPS approved digest algorithms in aide.conf so that
  aide works by default in FIPS mode

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 11 2010 Steve Grubb <sgrubb@redhat.com> - 0.15.1-1
- New upstream release

* Tue May 18 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-5
- Apply 2 upstream bug fixes

* Tue May 18 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-4
- Use upstream's patch to fix bz 590566

* Sat May 15 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-3
- Fix bz 590561 aide does not detect the change of SElinux context
- Fix bz 590566 aide reports a changed file when it has not been changed

* Wed Apr 28 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-2
- Fix bz 574764 by replacing abort calls with exit
- Apply libgcrypt init patch

* Tue Mar 16 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-1
- New upstream release final 0.14

* Thu Feb 25 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-0.4.rc3
- New upstream release

* Thu Feb 25 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-0.3.rc2
- New upstream release

* Tue Feb 23 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-0.2.rc1
- Fix dirent detection on 64bit systems

* Mon Feb 22 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-0.1.rc1
- New upstream release

* Fri Feb 19 2010 Steve Grubb <sgrubb@redhat.com> - 0.13.1-16
- Add logrotate script and spec file cleanups

* Fri Dec 11 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-15
- Get rid of .dedosify files

* Wed Dec 09 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-14
- Revise patch for Initialize libgcrypt correctly (#530485)

* Sat Nov 07 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-13
- Initialize libgcrypt correctly (#530485)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.13.1-12
- rebuilt with new audit

* Wed Aug 19 2009 Steve Grubb <sgrubb@redhat.com> 0.13.1-11
- rebuild for new audit-libs
- Correct regex for root's dot files (#509370)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 08 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-9
- Make aide smarter about prelinked files (Peter Vrabec)
- Add /lib64 to default config

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-6
- enable xattr support and update config file

* Fri Sep 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13.1-5
- fix selcon patch to apply without fuzz

* Fri Feb 15 2008 Steve Conklin <sconklin@redhat.com>
- rebuild for gcc4.3

* Tue Aug 21 2007 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Jul 22 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.13.1-2
- Apply Steve Conklin's patch to increase displayed portion of
  selinux context.

* Sun Dec 17 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.13.1-1
- Update to 0.13.1 release.

* Sun Dec 10 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.13-1
- Update to 0.13 release.
- Include default aide.conf from RHEL5 as doc example file.

* Sun Oct 29 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12-3.20061027cvs
- CAUTION! This changes the database format and results in a report of
  false inconsistencies until an old database file is updated.
- Check out CVS 20061027 which now contains Red Hat's
  acl/xattr/selinux/audit patches.
- Patches merged upstream.
- Update manual page substitutions.

* Mon Oct 23 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12-2
- Add "memory leaks and performance updates" patch as posted
  to aide-devel by Steve Grubb.

* Sat Oct 07 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12-1
- Update to 0.12 release.
- now offers --disable-static, so -no-static patch is obsolete
- fill last element of getopt struct array with zeroes

* Mon Oct 02 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.11-3
- rebuilt

* Mon Sep 11 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.11-2
- rebuilt

* Sun Feb 19 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.11-1
- Update to 0.11 release.
- useless-includes patch merged upstream.
- old Russian man pages not available anymore.
- disable static linking.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Nov 28 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.10-0.fdr.1
- Update to 0.10 release.
- memleaks patch merged upstream.
- rootpath patch merged upstream.
- fstat patch not needed anymore.
- Updated URL.

* Thu Nov 13 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.10-0.fdr.0.2.cvs20031104
- Added buildreq m4 to work around incomplete deps of bison package.

* Tue Nov 04 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.10-0.fdr.0.1.cvs20031104
- Only tar.gz available upstream.
- byacc not needed when bison -y is available.
- Installed Russian manual pages.
- Updated with changes from CVS (2003-11-04).
- getopt patch merged upstream.
- bison-1.35 patch incorporated upstream.

* Tue Sep 09 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.9-0.fdr.0.2.20030902
- Added fixes for further memleaks.

* Sun Sep 07 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.9-0.fdr.0.1.20030902
- Initial package version.
