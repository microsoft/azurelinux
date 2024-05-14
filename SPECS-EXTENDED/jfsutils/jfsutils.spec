Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%define _legacy_common_support 1

Summary: Utilities for managing the JFS filesystem
Name: jfsutils
Version: 1.1.15
Release: 18%{?dist}
Source0: https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0: jfsutils-1.1.15_stdint.patch
Patch1: jfsutils_format-security_ftbs.patch
Patch2: jfsutils_sysmacros.patch
URL: https://jfs.sourceforge.net/
License: GPLv2+
Buildrequires: libuuid-devel

BuildRequires:  gcc
%description
The jfsutils package contains a number of utilities for creating,
checking, modifying, and correcting any inconsistencies in JFS
filesystems.  The following utilities are available: fsck.jfs - initiate
replay of the JFS transaction log, and check and repair a JFS formatted
device; logdump - dump a JFS formatted device's journal log; logredo -
"replay" a JFS formatted device's journal log;  mkfs.jfs - create a JFS
formatted partition; xchkdmp - dump the contents of a JFS fsck log file
created with xchklog; xchklog - extract a log from the JFS fsck workspace
into a file;  xpeek - shell-type JFS file system editor.


%prep
%setup -q
find . -type f -name *.[ch] -exec chmod -x {} \;
%patch 0 -p1
%patch 1 -p1
%patch 2 -p1

%build
%configure 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%files
%{_sbindir}/*
%{_mandir}/man8/*
%doc AUTHORS COPYING NEWS ChangeLog

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.15-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sun Mar 29 2020 François Cami <fcami@fedoraproject.org> - 1.1.15-17
- Fix rhbz#1799538 (FTBFS)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 15 2018 François Cami <fcami@fedoraproject.org> - 1.1.15-13
- Fix rhbz#1604441 (FTBFS)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 04 2013 François Cami <fcami@fedoraproject.org> - 1.1.15-3
- Fix FTBS with -Werror=format-security (#1037145).

* Thu Sep 05 2013 François Cami <fcami@fedoraproject.org> - 1.1.15-2
- Install in /usr

* Mon Sep 02 2013 François Cami <fcami@fedoraproject.org> - 1.1.15-1
- Update to latest upstream.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Josh Boyer <jwboyer@gmail.com> - 1.1.13-7
- Update for e2fsprogs package split-up

* Wed Mar 25 2009 Josh Boyer <jwboyer@gmail.com> - 1.1.13-6
- Trivialities

* Wed Mar 25 2009 Josh Boyer <jwboyer@gmail.com> - 1.1.13-5
- Fix merge review issues, again (bug 225945)

* Mon Mar 23 2009 Josh Boyer <jwboyer@gmail.com> - 1.1.13-4
- Fix merge review issues, again (bug 225945)

* Mon Mar 23 2009 Josh Boyer <jwboyer@gmail.com> - 1.1.13-3
- Fix merge review issues (bug 225945)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 13 2009 Josh Boyer <jwboyer@gmail.com> - 1.1.13-1
- Update to latest release (bug 479565)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.12-2
- Autorebuild for GCC 4.3

* Sat Aug 25 2007 Josh Boyer <jwboyer@jdub.homelinux.org> - 1.1.12-1
- Update to latest release
- Drop obsoleted patch (fixed upstream)

* Wed Aug 22 2007 Josh Boyer <jwboyer@jdub.homelinux.org> - 1.1.11-2
- Add patch to fix open call

* Fri Aug 03 2007 Josh Boyer <jwboyer@jdub.homelinux.org> - 1.1.11-1
- Update license field

* Fri May 18 2007 Josh Boyer <jwboyer@jdub.homelinux.org> - 1.1.11-0
- Update to latest upstream release

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.1.10-4.1
- rebuild

* Wed Mar 01 2006 Karsten Hopp <karsten@redhat.de> 1.1.10-4
- BuildRequires: e2fsprogs-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.1.10-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1.10-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com>
- rebuilt again

* Fri Dec  9 2005 Dave Jones <davej@redhat.com>
- Update to newer upstream 1.1.10 release.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Apr 15 2005 Dave Jones <davej@redhat.com>
- rebuilt.

* Tue Oct 12 2004 Florian La Roche <laroche@redhat.com>
- 1.1.7

* Thu Jun 17 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.1.6

* Thu Feb 26 2004 Jeff Garzik <jgarzik@redhat.com>
- Version 1.1.4

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Oct 25 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.1.3

* Sun Aug 10 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.1.2

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Matt Wilson <msw@redhat.com> 1.0.17-5
- use #include <errno.h>, not extern int errno;

* Mon Nov 18 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr 09 2002 Michael K. Johnson <johnsonm@redhat.com>
- updated to jfsutils 1.0.17

* Fri Feb 08 2002 Michael K. Johnson <johnsonm@redhat.com>
- typo fixed

* Tue Jan 29 2002 Michael K. Johnson <johnsonm@redhat.com>
- Initial packaging
