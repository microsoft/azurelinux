Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		pciutils
Version:	3.7.0
Release:	4%{?dist}
Summary:	PCI bus related utilities
License:	GPLv2+
URL:		https://mj.ucw.cz/sw/pciutils/

Source0:	https://www.kernel.org/pub/software/utils/pciutils/%{name}-%{version}.tar.xz
Source1:	multilibconfigh

#change pci.ids directory to hwdata, fedora/rhel specific
Patch1:		pciutils-2.2.1-idpath.patch

#add support for directory with another pci.ids, rejected by upstream, rhbz#195327
Patch2:		pciutils-dir-d.patch
Patch3: 	pciutils-3.7.0-decodercec.patch

Requires:	hwdata
Requires:	%{name}-libs = %{version}-%{release}
BuildRequires:	gcc make sed kmod-devel
Provides:	/sbin/lspci /sbin/setpci

%description
The pciutils package contains various utilities for inspecting and
setting devices connected to the PCI bus.

%package devel
Summary: Linux PCI development library
Requires: zlib-devel pkgconfig %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains a library for inspecting and setting
devices connected to the PCI bus.

%package libs
Summary: Linux PCI library

%description libs
This package contains a library for inspecting and setting
devices connected to the PCI bus.

%package devel-static
Summary: Linux PCI static library
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description devel-static
This package contains a static library for inspecting and setting
devices connected to the PCI bus.

%prep
%autosetup -p1

%build
%make_build SHARED="no" ZLIB="no" LIBKMOD=yes STRIP="" OPT="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS" PREFIX="/usr" LIBDIR="%{_libdir}" IDSDIR="/usr/share/hwdata" PCI_IDS="pci.ids"
mv lib/libpci.a lib/libpci.a.toinstall

make clean

%make_build SHARED="yes" ZLIB="no" LIBKMOD=yes STRIP="" OPT="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS" PREFIX="/usr" LIBDIR="%{_libdir}" IDSDIR="/usr/share/hwdata" PCI_IDS="pci.ids"


%install
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{7,8},%{_libdir},%{_libdir}/pkgconfig,%{_includedir}/pci}

install -p lspci setpci update-pciids $RPM_BUILD_ROOT%{_sbindir}
install -p -m 644 lspci.8 setpci.8 update-pciids.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 644 pcilib.7 $RPM_BUILD_ROOT%{_mandir}/man7
install -p lib/libpci.so.* $RPM_BUILD_ROOT%{_libdir}/
ln -s $(basename $RPM_BUILD_ROOT%{_libdir}/*.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libpci.so

mv lib/libpci.a.toinstall lib/libpci.a
install -p -m 644 lib/libpci.a $RPM_BUILD_ROOT%{_libdir}
install -p -m 644 lib/pci.h $RPM_BUILD_ROOT%{_includedir}/pci
install -p -m 644 lib/header.h $RPM_BUILD_ROOT%{_includedir}/pci
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_includedir}/pci/config.h
install -p -m 644 lib/config.h $RPM_BUILD_ROOT%{_includedir}/pci/config.%{_lib}.h
ln -s config.%{_lib}.h $RPM_BUILD_ROOT%{_includedir}/pci/config.%{_lib64}.h
install -p -m 644 lib/types.h $RPM_BUILD_ROOT%{_includedir}/pci
install -p -m 644 lib/libpci.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig

%ldconfig_scriptlets libs

%files
%doc README ChangeLog pciutils.lsm
%{_sbindir}/lspci
%{_sbindir}/setpci
%{_sbindir}/update-pciids
%{_mandir}/man8/*

%files libs
%license COPYING
%{_libdir}/libpci.so.*

%files devel-static
%{_libdir}/libpci.a

%files devel
%{_libdir}/pkgconfig/libpci.pc
%{_libdir}/libpci.so
%{_includedir}/pci
%{_mandir}/man7/*

%changelog
* Tue Jul 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.7.0-4
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Linking 'config.lib64.h' to 'config.lib.h' for compatibility with other projects.

* Tue Feb 02 2021 Michal Hlavinka <mhlavink@redhat.com> - 3.7.0-3
- spec file cleanup

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 30 2020 Michal Hlavinka <mhlavink@redhat.com> - 3.7.0-1
- updated to 3.7.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Feb 28 2020 Michal Hlavinka <mhlavink@redhat.com> - 3.6.4-1
- pciutils updated to 3.6.4

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Peter Robinson <pbrobinson@fedoraproject.org> 3.6.3-1
- pciutils updated to 3.6.3
- spec cleanups, use %%license, use kernel.org download

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Michal Hlavinka <mhlavink@redhat.com> - 3.6.2-1
- pciutils updated to 3.6.2

* Fri Jul 13 2018 Michal Hlavinka <mhlavink@redhat.com> - 3.6.1-1
- pciutils updated to 3.6.1

* Mon Jul 09 2018 Michal Hlavinka <mhlavink@redhat.com> - 3.6.0-1
- pciutils updated to 3.6.0

* Wed Mar 07 2018 Michal Hlavinka <mhlavink@redhat.com> - 3.5.6-4
- add gcc buildrequire

* Sat Feb 24 2018 Florian Weimer <fweimer@redhat.com> - 3.5.6-3
- Use LDFLAGS from redhat-rpm-config

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 20 2017 Michal Hlavinka <mhlavink@redhat.com> - 3.5.6-1
- pciutils updated to 3.5.6

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Michal Hlavinka <mhlavink@redhat.com> - 3.5.5-1
- pciutils updated to 3.5.5

* Mon Feb 27 2017 Michal Hlavinka <mhlavink@redhat.com> - 3.5.4-1
- pciutils updated to 3.5.4

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 04 2016 Michal Hlavinka <mhlavink@redhat.com> - 3.5.2-1
- pciutils updated to 3.5.2

* Thu Aug 11 2016 Michal Toman <mtoman@fedoraproject.org> - 3.5.1-2
- Add support for MIPS to multilibconfigh

* Tue May 24 2016 Michal Hlavinka <mhlavink@redhat.com> - 3.5.1-1
- pciutils updated to 3.5.1

* Fri May 20 2016 Michal Hlavinka <mhlavink@redhat.com> - 3.5.0-1
- pciutils updated to 3.5.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Michal Hlavinka <mhlavink@redhat.com> - 3.4.1-1
- pciutils updated to 3.4.1

* Tue Sep 15 2015 Michal Hlavinka <mhlavink@redhat.com> - 3.4.0-1
- pciutils updated to 3.4.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 10 2015 Michal Hlavinka <mhlavink@redhat.com> - 3.3.1-1
- pciutils updated to 3.3.1

* Wed Nov 12 2014 Michal Hlavinka <mhlavink@redhat.com> - 3.3.0-1
- updated to 3.3.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Michal Hlavinka <mhlavink@redhat.com> - 3.2.1-2
- enable libkmod support (#1087862)

* Fri Nov 15 2013 Michal Hlavinka <mhlavink@redhat.com> - 3.2.1-1
- updated to 3.2.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 31 2013 Michal Hlavinka <mhlavink@redhat.com> - 3.2.0-2
- updated to 3.2.0
- add aarch64 support (#969138)

* Mon Apr 22 2013 Michal Hlavinka <mhlavink@redhat.com> - 3.2.0-1
- updated to 3.2.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Michal Hlavinka <mhlavink@redhat.com> - 3.1.10-1
- updated to 3.1.10

* Mon Jan 16 2012 Michal Hlavinka <mhlavink@redhat.com> - 3.1.9-1
- updated to 3.1.9

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 03 2011 Michal Hlavinka <mhlavink@redhat.com> - 3.1.8-1
- updated to 3.1.8

* Thu Mar 17 2011 Michal Hlavinka <mhlavink@redhat.com> - 3.1.7-6
- don't forget to close pci.ids directory

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Dan Horák <dan[at]danny.cz> - 3.1.7-4
- fix the multilib header on s390x

* Tue Jan 18 2011 Michal Hlavinka <mhlavink@redhat.com> - 3.1.7-3
- different approach to fix multilib issues

* Mon Jan 10 2011 Michal Hlavinka <mhlavink@redhat.com> - 3.1.7-2
- removed obsolete patches

* Mon Aug 30 2010 Michal Hlavinka <mhlavink@redhat.com> - 3.1.7-1
- updated to 3.1.7

* Wed Jul 07 2010 Michal Hlavinka <mhlavink@redhat.com> - 3.1.6-5
- follow licensing guideline update

* Thu Feb 04 2010 Michal Hlavinka <mhlavink@redhat.com> - 3.1.6-4
- move update-pciids

* Thu Feb 04 2010 Michal Hlavinka <mhlavink@redhat.com> - 3.1.6-3
- spec cleanup

* Wed Feb 03 2010 Michal Hlavinka <mhlavink@redhat.com> - 3.1.6-2
- libpci moved to /lib

* Mon Jan 25 2010 Michal Hlavinka <mhlavink@redhat.com> - 3.1.6-1
- updated to 3.1.6

* Mon Nov 02 2009 Michal Hlavinka <mhlavink@redhat.com> - 3.1.4-6
- spec cleanup

* Mon Oct 26 2009 Michal Hlavinka <mhlavink@redhat.com> - 3.1.4-5
- fix build to enable -F option (#531020)

* Mon Oct 26 2009 Michal Hlavinka <mhlavink@redhat.com> - 3.1.4-4
- enable direct hardware access method for 64bit architectures

* Mon Oct 12 2009 Michal Hlavinka <mhlavink@redhat.com> - 3.1.4-3
- don't ship static library in -devel sub-package

* Tue Sep 01 2009 Michal Hlavinka <mhlavink@redhat.com> - 3.1.4-2
- add COPYING to docs

* Tue Sep 01 2009 Michal Hlavinka <mhlavink@redhat.com> - 3.1.4-1
- updated to 3.1.4

* Wed Jul 29 2009 Michal Hlavinka <mhlavink@redhat.com> - 3.1.3-1
- updated to 3.1.3

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 29 2009 Michal Hlavinka <mhlavink@redhat.com> - 3.1.2-5
- add support for ARM

* Fri Feb 27 2009 Michal Hlavinka <mhlaivnk@redhat.com> - 3.1.2-4
- fix typo & rebuild

* Fri Feb 27 2009 Michal Hlavinka <mhlaivnk@redhat.com> - 3.1.2-3
- fix: lspci segfaults when pci.ids cannot be found (#487516)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Michal Hlavinka <mhlavink@redhat.com> 3.1.2-1
- version 3.1.2
- fix for the syntax error checks in setpci argument parser

* Wed Feb 04 2009 Michal Hlavinka <mhlavink@redhat.com> 3.1.1-1
- version 3.1.1

* Tue Jan 27 2009 Michal Hlavinka <mhlavink@redhat.com> 3.1.0-2
- fix typo in multilib patch - for s390x building

* Mon Jan 19 2009 Michal Hlavinka <mhlavink@redhat.com> 3.1.0-1
- version 3.1.0

* Tue Dec 09 2008 Michal Hlavinka <mhlavink@redhat.com> 3.0.3-1
- version 3.0.3

* Mon Sep 22 2008 Michal Hlavinka <mhlavink@redhat.com> 3.0.2-1
- version 3.0.2

* Fri Sep 19 2008 Michal Hlavinka <mhlavink@redhat.com> 3.0.1-1
- version 3.0.1
- add support for Super-H (sh3,sh4) (#446600)
- fix: broken -L in libpci.pc (#456469)

* Mon Sep 01 2008 Harald Hoyer <harald@redhat.com> 3.0.0-2
- rebuild to eliminate fuzz patches

* Mon Jun 02 2008 Harald Hoyer <harald@redhat.com> 3.0.0-1
- version 3.0.0

* Mon May 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.10-2
- add sparc support

* Wed Feb 20 2008 Harald Hoyer <harald@redhat.com> 2.2.10-1
- version 2.2.10

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2.9-6
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Bill Nottingham <notting@redhat.com> 2.2.9-5
- put library back

* Mon Jan 21 2008 Harald Hoyer <harald@redhat.com> 2.2.9-4
- fixed segfault, if subdir does not exists

* Fri Jan 18 2008 Harald Hoyer <harald@redhat.com> 2.2.9-3
- removed static library, preserve timestamps on install (rhbz#226236)
- added modified patch from Michael E. Brown @ Dell, to also
  read all /usr/share/hwdata/pci.ids.d/*.ids files (rhbz#195327)

* Thu Jan 10 2008 Harald Hoyer <harald@redhat.com> 2.2.9-2
- added more requirements for pciutils-devel

* Tue Nov 20 2007 Harald Hoyer <harald@redhat.com> - 2.2.9-1
- version 2.2.9
- added package config file (rhbz#389451)

* Wed Aug 22 2007 Harald Hoyer <harald@redhat.com> - 2.2.6-3
- changed license tag

* Thu Jul 12 2007 Harald Hoyer <harald@redhat.com> - 2.2.6-2
- fixed update-pciids.sh

* Wed Jun 27 2007 Harald Hoyer <harald@redhat.com> - 2.2.6-1
- version 2.2.6
- fixed URL in update-pciids.sh 

* Thu May 31 2007 Harald Hoyer <harald@redhat.com> - 2.2.5-1
- version 2.2.5

* Thu Apr  5 2007 Peter Jones <pjones@redhat.com> - 2.2.4-3
- buildreq zlib-devel, so we know configure will find it consistently.

* Mon Apr  2 2007 Harald Hoyer <harald@redhat.com> - 2.2.4-2
- added alpha to multilib patch (#231790)
- specfile cleanup
- Resolves: rhbz#231790

* Fri Jan 26 2007 Harald Hoyer <harald@redhat.com> - 2.2.4-1
- version 2.2.4
- truncate long device names (#205948)
- Resolves: rhbz#205948

* Wed Aug  9 2006 Peter Jones <pjones@redhat.com> - 2.2.3-4
- Add definitions for more pci storage classes

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com> - 2.2.3-3
- rebuild

* Fri Jun 02 2006 Harald Hoyer <harald@redhat.com> 2.2.3-2
- corrected multilib patch

* Tue May 23 2006 Harald Hoyer <harald@redhat.com> 2.2.3-1
- version 2.2.3
- multilib patch (bug #192743)

* Thu Feb 23 2006 Harald Hoyer <harald@redhat.com> 2.2.1-2
- added update-pciids shell script and manpage (bz #178582)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.2.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.2.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Dec 13 2005 Bill Nottingham <notting@redhat.com> - 2.2.1-1
- update to 2.2.1, adjust patches

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu May 19 2005 Bill Nottingham <notting@redhat.com> - 2.1.99.test8-10
- allow 64-bit addresses on x86_64 (#158217, <Matt_Domsch@dell.com>)

* Tue May 10 2005 Bill Nottingham <notting@redhat.com> - 2.1.99.test8-9
- fix debuginfo generation

* Mon Mar 14 2005 Bill Nottingham <notting@redhat.com> - 2.1.99.test8-8
- add patch for glibc macros (#151032, <redhat-bugzilla@linuxnetz.de>)

* Wed Mar  2 2005 Bill Nottingham <notting@redhat.com> - 2.1.99.test8-7
- FC4. GCC 4. fore!

* Tue Jan 25 2005 Bill Nottingham <notting@redhat.com> - 2.1.99.test8-6
- remove explicit kernel dep (#146153)

* Fri Jan 21 2005 Bill Nottingham <notting@redhat.com> - 2.1.99.test8-5
- fix domain bug (#138722, #144383)

* Mon Nov 22 2004 Jeremy Katz <katzj@redhat.com> - 2.1.99.test8-4
- don't use dietlibc on x86 anymore

* Thu Sep  2 2004 Bill Nottingham <notting@redhat.com> 2.1.99.test8-3
- change sysfs access for detecting devices who get fixed up in the
  kernel (#115522, #123802)

* Tue Aug 31 2004 Bill Nottingham <notting@redhat.com> 2.1.99.test8-2
- update to test8
- fix headers

* Fri Jul  9 2004 Bill Nottingham <notting@redhat.com> 2.1.99.test7-1
- update to test7
- fix segfault on some x86-64 boxen

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Dec  8 2003 Bill Nottingham <notting@redhat.com> 2.1.11-4
- fix paths for pci.ids, etc. (#111665)

* Tue Nov 25 2003 Bill Nottingham <notting@redhat.com> 2.1.11-3
- remove a few calls to ->error() in the sysfs code

* Fri Nov 21 2003 Jeremy Katz <katzj@redhat.com> 2.1.11-2
- build a diet libpci_loader.a on i386
- always assume pread exists, it does with diet and all vaguely recent glibc

* Fri Nov 21 2003 Bill Nottingham <notting@redhat.com> 2.1.11-1
- update to 2.1.11
- add patch for sysfs & pci domains support (<willy@debian.org>)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 12 2003 Bill Nottingham <notting@redhat.com>
- don't segfault when there's no pci bus (#84146)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 05 2002 Elliot Lee <sopwith@redhat.com> 2.1.10-5
- Add patch4 for ppc64. The basic rule seems to be that on any platform
where it is possible to be running a 64-bit kernel, we need to always 
print out 64-bit addresses.

* Mon Nov  4 2002 Bill Nottingham <notting@redhat.com> 2.1.10-4
- fix dir perms on /usr/include/pci

* Tue Oct 15 2002 Bill Nottingham <notting@redhat.com> 2.1.10-3
- use %%{_libdir}
- own /usr/include/pci
- build library with -fPIC

* Mon Jul  8 2002 Bill Nottingham <notting@redhat.com> 2.1.10-2
- don't build with -fomit-frame-pointer

* Mon Jun 24 2002 Bill Nottingham <notting@redhat.com> 2.1.10-1
- update to 2.1.10

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 17 2002 Bill Nottingham <notting@redhat.com> 2.1.9-4
- don't forcibly strip binaries

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Feb 22 2002 Bill Nottingham <notting@redhat.com>
- rebuild

* Wed Jan 30 2002 Bill Nottingham <notting@redhat.com>
- require hwdata now that pci.ids is there

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Dec 30 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- man page is now owned by root

* Wed Oct 17 2001 Bill Nottingham <notting@redhat.com>
- dump all the patches, ship pci.ids direct out of sourceforge CVS

* Wed Sep 26 2001 Bill Nottingham <notting@redhat.com>
- broadcom bcm5820 id (#53592)

* Fri Aug 10 2001 Bill Nottingham <notting@redhat.com>
- more ids

* Tue Jul 17 2001 Bill Nottingham <notting@redhat.com>
- add newline in printf in PCI-X patch (#49277)

* Mon Jul  9 2001 Bill Nottingham <notting@redhat.com>
- update broadcom patch
- add new ids from 2.4.6

* Mon May 28 2001 Bill Nottingham <notting@redhat.com>
- add a couple of e1000 ids

* Thu Mar 22 2001 Bill Nottingham <notting@redhat.com>
- another megaraid id

* Wed Mar 21 2001 Bill Nottingham <notting@redhat.com>
- another megaraid id

* Wed Mar 14 2001 Preston Brown <pbrown@redhat.com>
- LSI SCSI PCI id

* Wed Feb 21 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix formatting problems

* Wed Feb 21 2001 Preston Brown <pbrown@redhat.com>
- add IBM ServeRAID entries

* Tue Feb 20 2001 Preston Brown <pbrown@redhat.com>
- i860 entries.

* Mon Feb 19 2001 Helge Deller <hdeller@redhat.de>
- added various pci ids 

* Fri Feb  2 2001 Bill Nottingham <notting@redhat.com>
- fix mishap in fixing mishap

* Thu Feb  1 2001 Bill Nottingham <notting@redhat.com>
- fix apparent mishap in pci.ids update from kernel (#25520)

* Tue Jan 23 2001 Bill Nottingham <notting@redhat.com>
- pci.ids updates

* Tue Dec 12 2000 Bill Nottingham <notting@redhat.com>
- big pile of pci.ids updates

* Tue Jul 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- clean up patches to not generate badly-formatted files

* Tue Jul 25 2000 Preston Brown <pbrown@redhat.com>
- Vortex fixes laroche originally applied on kudzu moved here.

* Fri Jul 14 2000 Preston Brown <pbrown@redhat.com>
- pci ids for i815, new ati hardware

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul 11 2000 Bill Nottingham <notting@redhat.com>
- yet more IDs
- PCI-X support from Matt Domsch

* Fri Jul  7 2000 Bill Nottingham <notting@redhat.com>
- some more QLogic ids

* Mon Jun 26 2000 Bill Nottingham <notting@redhat.com>
- more IDs from Dell

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- update to 2.1.8

* Fri Apr 21 2000 Bill Nottingham <notting@redhat.com>
- update to 2.1.7

* Mon Apr 17 2000 Bill Nottingham <notting@redhat.com>
- update to 2.1.6

* Fri Mar  3 2000 Bill Nottingham <notting@redhat.com>
- add a couple of ids

* Mon Feb 14 2000 Bill Nottingham <notting@redhat.com>
- update to 2.1.5

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Mon Jan 24 2000 Bill Nottingham <notting@redhat.com>
- update to 2.1.4

* Thu Jan 20 2000 Bill Nottingham <notting@redhat.com>
- update to 2.1.3

* Fri Dec 24 1999 Bill Nottingham <notting@redhat.com>
- update to 2.1.2

* Tue Jun 29 1999 Bill Nottingham <notting@redhat.com>
- add -devel package

* Thu May 20 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0

* Mon Apr 19 1999 Jakub Jelinek <jj@ultra.linux.cz>
- update to 1.99.5
- fix sparc64 operation

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Thu Feb  4 1999 Bill Nottingham <notting@redhat.com>
- initial build
