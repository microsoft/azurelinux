%define libidl_version 0.8.2-1
%define glib2_version 2.2.0
Summary:        A high-performance CORBA Object Request Broker
Name:           ORBit2
Version:        2.14.19
Release:        30%{?dist}
License:        LGPLv2+ AND GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.gnome.org/projects/ORBit2
Source:         https://download.gnome.org/sources/%{name}/2.14/%{name}-%{version}.tar.gz
Patch0:         ORBit2-2.14.3-multilib.patch
# handle ref leaks in the a11y stack more gracefully
Patch1:         ORBit2-2.14.3-ref-leaks.patch
Patch2:         ORBit2-make-j-safety.patch
Patch3:         ORBit2-allow-deprecated.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  chrpath
BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  gtk-doc
BuildRequires:  libIDL-devel >= %{libidl_version}
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig
%if 0%{?with_check}
BuildRequires:  procps-ng
%endif

%description
ORBit is a high-performance CORBA (Common Object Request Broker
Architecture) ORB (object request broker). It allows programs to
send requests and receive replies from other programs, regardless
of the locations of the two programs. CORBA is an architecture that
enables communication between program objects, regardless of the
programming language they're written in or the operating system they
run on.

You will need to install this package and ORBit-devel if you want to
write programs that use CORBA technology.

%package  devel
Summary:        Development libraries, header files and utilities for ORBit
Requires:       %{name} = %{version}-%{release}
# we install an automake macro
Requires:       automake
Requires:       glib2-devel >= %{glib2_version}
Requires:       indent
Requires:       libIDL-devel >= %{libidl_version}
# we install a pc file
Requires:       pkgconfig
Conflicts:      ORBit-devel <= 1:0.5.8

%description devel
ORBit is a high-performance CORBA (Common Object Request Broker
Architecture) ORB (object request broker) with support for the
C language.

This package contains the header files, libraries and utilities
necessary to write programs that use CORBA technology. If you want to
write such programs, you'll also need to install the ORBIT package.

%prep
%autosetup -p1 %{name}-%{version}

%build
%configure --disable-gtk-doc --enable-purify --disable-static --disable-rpath
%make_build %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/ORBit-2.0/*.*a
rm -f %{buildroot}%{_libdir}/orbit-2.0/*.*a

# fix multilib conflict caused by orbit-config.h
%define wordsize %{__isa_bits}

mv %{buildroot}%{_includedir}/orbit-2.0/orbit/orbit-config.h \
   %{buildroot}%{_includedir}/orbit-2.0/orbit/orbit-config-%{wordsize}.h

cat >%{buildroot}%{_includedir}/orbit-2.0/orbit/orbit-config.h <<EOF
#ifndef ORBIT_MULTILIB
#define ORBIT_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "orbit-config-32.h"
#elif __WORDSIZE == 64
# include "orbit-config-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

chrpath --delete %{buildroot}%{_libdir}/libORBitCosNaming-2.so.0.1.0
chrpath --delete %{buildroot}%{_libdir}/libORBit-imodule-2.so.0.0.0
chrpath --delete %{buildroot}%{_libdir}/orbit-2.0/Everything_module.so
chrpath --delete %{buildroot}%{_bindir}/ior-decode-2
chrpath --delete %{buildroot}%{_bindir}/typelib-dump

%check
cd test
# command 'killall' is not found in mariner.
# use 'pkill' instead to terminate the timeout-server test process, using the created process name
sed 's/\(^.*\)killall\(.*$\)/\1pkill -9 lt-timeout-serv/' < timeout.sh > timeout.tmp.sh
install -m 0777 timeout.tmp.sh timeout.sh
make check-TESTS

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS README TODO
%{_libdir}/*.so.*
%dir %{_libdir}/orbit-2.0
%{_libdir}/orbit-2.0/*.so*

%files devel
%{_libdir}/*.so
# this is needed by libbonobo
%{_libdir}/libname-server-2.a
%{_libdir}/pkgconfig/*
%{_bindir}/orbit-idl-2
%{_bindir}/typelib-dump
%{_bindir}/orbit2-config
%{_bindir}/ior-decode-2
%{_includedir}/*
%{_datadir}/aclocal/*
%{_datadir}/idl/orbit-2.0
%{_bindir}/linc-cleanup-sockets
%{_datadir}/gtk-doc

%changelog
* Wed Oct 26 2022 Sumedh Sharma <sumsharma@microsoft.com> - 2.14.19-30
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- Enable check section.
- License verified.

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.19-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.19-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.19-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Mar 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.14.19-26
- Fix autoconf 2.71 FTBFS.

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.19-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.19-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.19-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.19-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.19-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.19-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.19-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.19-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.19-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.19-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.19-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.19-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.19-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.19-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 10 2013 Petr Pisar <ppisar@redhat.com> - 2.14.19-11
- Correct __isa_bits macro name

* Thu Dec  5 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.14.19-10
- Simplify wordsize definition (fix FTBFS on aarch64)

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Dan Winship <danw@redhat.com> - 2.14.19-8
- Fix FTBFS by not trying to use G_DISABLE_DEPRECATED any more (#913861)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Dan Winship <danw@redhat.com> - 2.14.19-5
- Make orbit-idl-compiler work reliably under "make -j"

* Thu Apr 26 2012 Jon Ciesla <limburgher@gmail.com> - 2.14.19-4
- Minor merge review fixes, BZ 226223.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.14.19-1
- Update to 2.14.19

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> - 2.14.18-2
- Co-own /usr/share/gtk-doc (#604406)
- Some packaging cleanups

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.14.18-1
- Update to 2.14.18

* Mon Mar  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.14.17-4
- Drop ownership of /usr/share/idl, since filesystem owns it

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.14.17-1
- 2.14.17

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.14.16-2
- Merge review trivia

* Sun Sep 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.14.16-1
- Update to 2.14.16

* Thu Sep 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.14.15-1
- Update to 2.14.15

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.14.14-1
- Update to 2.14.14

* Wed Jun  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.14.13-1
- Update to 2.14.13

* Sat Mar 15 2008 Matthias Clasen <mclasen@redhat.com> - 2.14.12-3
- Fix some packaging trivia

* Fri Feb  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.14.12-2
- Rebuild for gcc 4.3

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.14.12-1
- Update to 2.14.12

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.14.11-1
- Update to 2.14.11

* Tue Oct 16 2007 Dennis Gilmore <dennis@ausil.us> - 2.14.10-2
- add sparc64 to the list  of 64 bit archs

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.10-1
- Update to 2.14.10 (bug fixes)

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.9-1
- Update to 2.14.9

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.14.7-6
- Rebuild for selinux ppc32 issue.

* Wed Aug  8 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.7-5
- Update the license field

* Sat Jul  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.7-4
- Fix directory ownership issues

* Mon Apr 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.7-3
- Add alpha to 64bit arches (#236544)

* Sun Mar 25 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.7-2
- Fix a directory ownership issue (#233755)

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.7-1
- Update to 2.14.7

* Mon Feb 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.6-1
- Update to 2.14.6

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.5-2
- Re-add a static library that is needed by libbonobo

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.5-1
- Update to 2.14.5

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.4-1
- Update to 2.14.4

* Fri Dec  8 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.3-4
- Handle ref leaks in the a11y stack more gracefully (#214795)

* Sun Sep 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.3-3
- Make non-local IPv4 work again  (#205950)

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.3-2.fc6
- Fix remaining multilib issues (#205228)

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.3-1.fc6
- Update to 2.14.3

* Wed Aug  2 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.2-1.fc6
- Update to 2.14.2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.14.0-3.1
- rebuild

* Thu Jun  8 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-3
- Add missing BuildRequires

* Wed May 24 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-2
- Don't rebuild api docs
- Fix multilib conflicts

* Tue Mar 14 2006 Ray Strode <rstrode@redhat.com> - 2.14.1-1
- Update to 2.14.1

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 2.13.3-1.2
- rebump for build order issues during double-long bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.3-1.1
- bump again for double-long bug on ppc(64)

* Mon Feb  6 2006 Matthias Clasen <mclasen@redhat.com> 2.13.3-1
- Update to 2.13.3

* Mon Dec 19 2005 Matthias Clasen <mclasen@redhat.com> 2.13.2-2
- Fix multilib issues

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Matthias Clasen <mclasen@redhat.com> 2.13.2-1
- Update to 2.13.2
- Drop upstreamed patch

* Tue Oct 25 2005 Alexander Larsson <alexl@redhat.com> 2.12.4-3
- Build with --enable-purify to avoid valgrind warnings

* Wed Oct  5 2005 Matthias Clasen <mclasen@redhat.com> 2.12.4-2
- Use gmodule-no-export in the .pc file

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> 2.12.4-1
- Update to 2.12.4

* Fri Aug  5 2005 Matthias Clasen <mclasen@redhat.com> 2.12.2-1
- Update to 2.12.2

* Tue May 10 2005 Mark McLoughlin <markmc@redhat.com> 2.12.1-3
- Add patch to set the size of the IO thread stack to 256k in
  order to mitigate the apparent 10M jump in GNOME processes
  memory usage (#157297)

* Wed Mar  2 2005 Mark McLoughlin <markmc@redhat.com> 2.12.1-2
- Rebuild with gcc4

* Wed Feb  9 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1-1
- Update to 2.12.1

* Wed Sep 29 2004 Mark McLoughlin <markmc@redhat.com> 2.12.0-3
- Remove the linc obsoletes - we don't technically obsolete it

* Tue Sep 28 2004 Mark McLoughlin <markmc@redhat.com> 2.12.0-2
- Add Obseletes: linc

* Tue Sep 21 2004 Mark McLoughlin <markmc@redhat.com> 2.12.0-1
- Update to 2.12.0

* Mon Aug 30 2004 Mark McLoughlin <markmc@redhat.com> 2.11.2-1
- Update to 2.11.2
- Remove gcc on pcc workaround patch

* Mon Aug  9 2004 Mark McLoughlin <markmc@redhat.com> 2.11.1-2
- Add temporary workaround patch for bug #129329

* Tue Aug  3 2004 Mark McLoughlin <markmc@redhat.com> 2.11.1-1
- Update to 2.11.1

* Tue Jul 27 2004 Mark McLoughlin <markmc@redhat.com> 2.10.0-5
- Rebuilt

* Tue Jul 27 2004 Mark McLoughlin <markmc@redhat.com> 2.10.0-4
- Backport alignment fix for 64 bit from 0.10.3 - fixes Nautilus crashing
  on startup (#126181). Thanks to Lamont R. Peterson <lamont@gurulabs.com>

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Mar 11 2004 Alex Larsson <alexl@redhat.com> 2.10.0-2
- enable gtk-doc

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com> 2.10.0-1
- Update to 2.10.0

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 23 2004 Alexander Larsson <alexl@redhat.com> 2.9.8-1
- update to 2.9.8

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 16 2004 Alexander Larsson <alexl@redhat.com> 2.9.6-1
- update to 2.9.6

* Wed Oct 22 2003 Jeremy Katz <katzj@redhat.com> 2.8.2-1
- 2.8.2

* Mon Oct  6 2003 Jeremy Katz <katzj@redhat.com> 2.8.1.90-1
- update to CVS snap off of gnome-2-4 branch

* Fri Oct  3 2003 Alexander Larsson <alexl@redhat.com> 2.8.1-1
- 2.8.1
- BuildRequire a newer gtk-doc

* Wed Sep  3 2003 Alexander Larsson <alexl@redhat.com> 2.8.0-1
- 2.8.0

* Mon Aug 11 2003 Alexander Larsson <alexl@redhat.com> 2.7.5-5
- Remove obsoletes linc line

* Mon Aug 11 2003 Alexander Larsson <alexl@redhat.com> 2.7.5-4
- Add gtk-doc to devel

* Thu Aug  7 2003 Jonathan Blandford <jrb@redhat.com>
- rebuild for 2.4

* Fri Jul 11 2003 Havoc Pennington <hp@redhat.com>
- automated rebuild

* Mon Jul  7 2003 Havoc Pennington <hp@redhat.com> 2.6.2-1
- 2.6.2

* Fri Jun 27 2003 Havoc Pennington <hp@redhat.com> 2.6.0-5
- add lame _exit(0) hack to work around problem on ia64 temporarily

* Thu Jun 26 2003 Havoc Pennington <hp@redhat.com> 2.6.0-4
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Mon Feb 10 2003 Bill Nottingham <notting@redhat.com> 2.6.0-2
- own %%{_datadir}/idl/orbit-2.0 (#74020)

* Tue Feb  4 2003 Havoc Pennington <hp@redhat.com> 2.6.0-1
- 2.6.0

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Jan 12 2003 Havoc Pennington <hp@redhat.com>
- 2.5.1

* Fri Nov  8 2002 Havoc Pennington <hp@redhat.com>
- 2.5.0

* Tue Aug  6 2002 Havoc Pennington <hp@redhat.com>
- 2.4.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 06 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue Jun  4 2002 Havoc Pennington <hp@redhat.com>
- 2.4.0

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Fri May 17 2002 Havoc Pennington <hp@redhat.com>
- 2.3.109

* Thu May  2 2002 Havoc Pennington <hp@redhat.com>
- 2.3.108

* Thu Apr  4 2002 Jeremy Katz <katzj@redhat.com>
- 2.3.107

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- 2.3.105

* Wed Jan 30 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.3.103
- Rebuild for dependencies

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- build system somehow built against libglib-1.3.so.11
  even though pkg-config found 1.3.12? wtf?
  trying again

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- 2.3.100.90 snap

* Mon Nov 26 2001 Havoc Pennington <hp@redhat.com>
- 2.3.99

* Sun Nov 25 2001 Havoc Pennington <hp@redhat.com>
- new snap 2.3.97.90, rebuild for glib 1.3.11

* Fri Oct 26 2001 Havoc Pennington <hp@redhat.com>
- new snap, glib 1.3.10 rebuild

* Tue Oct  9 2001 Havoc Pennington <hp@redhat.com>
- check rebuild against new linc with headers moved
- remove epoch, that was a screwup

* Thu Oct  4 2001 Havoc Pennington <hp@redhat.com>
- cvs snap
- require specific glib2

* Thu Sep 27 2001 Havoc Pennington <hp@redhat.com>
- 2.3.95 tarball
- depend on new standalone libIDL, remove all libIDL stuff from file list

* Fri Sep 21 2001 Havoc Pennington <hp@redhat.com>
- require specific linc version, unrequire specific glib version since
  we get that via linc

* Mon Sep 17 2001 Havoc Pennington <hp@redhat.com>
- newer orbit2 from CVS

* Thu Sep 13 2001 Havoc Pennington <hp@redhat.com>
- conflict with old orbit with headers not moved

* Wed Sep 12 2001 Havoc Pennington <hp@redhat.com>
- renaming more things
- remove smp flags, doesn't work atm
- fix .pc file, trying to get bonobo-activation to build

* Tue Sep 11 2001 Havoc Pennington <hp@redhat.com>
- kill all file conflicts with ORBit1

* Mon Sep 10 2001 Havoc Pennington <hp@redhat.com>
- convert to ORBit2 spec file (from ORBit original)

* Tue Jul 24 2001 Alexander Larsson <alexl@redhat.com>
- Added glib-devel BuildRequires

* Thu Jun 21 2001 Elliot Lee <sopwith@redhat.com> 0.5.8-2
- Use _smp_mflags if possible.

* Mon May 14 2001 Jonathan Blandford <jrb@redhat.com>
- bumped version

* Thu Mar 01 2001 Owen Taylor <otaylor@redhat.com>
- Rebuild for GTK+-1.2.9

* Tue Jan 30 2001 Elliot Lee <sopwith@redhat.com>
- 0.5.7 for real

* Thu Jan 18 2001 Elliot Lee <sopwith@redhat.com>
- 0.5.7

* Tue Dec 19 2000 Elliot Lee <sopwith@redhat.com>
- 0.5.6

* Thu Nov 30 2000 Elliot Lee <sopwith@redhat.com>
- 0.5.5

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Tue Jul 25 2000 Elliot Lee <sopwith@redhat.com>
- 0.5.3

* Wed Jul 19 2000 Jonathan Blandford <jrb@redhat.com>
- fixed to work with new cpp.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul 11 2000 Jonathan Blandford <jrb@redhat.com>
- Upgraded to 0.5.2 - a bug fix release.

* Tue Jun 27 2000 Havoc Pennington <hp@redhat.com>
- Trying to build the package for Preston and the build
  system wants a new changelog entry

* Sat Jun 24 2000 Preston Brown <pbrown@redhat.com>
- defattr the devel pkg
- FHS paths

* Fri May 19 2000 Jonathan Blandford <jrb@redhat.com>
- Upgraded to 0.5.1

* Thu Feb 03 2000 Elliot Lee <sopwith@redhat.com> 0.5.0-3
- Strip shared libraries

* Mon Aug 30 1999 Elliot Lee <sopwith@redhat.com> 0.4.94-1
- Spec file fixes from RHL 6.0.

* Wed Jun 2 1999  Jose Mercado <jmercado@mit.edu>
- Fixed configure.in so spec.in could be used.

* Mon Nov 23 1998 Pablo Saratxaga <srtxg@chanae.alphanet.ch>
- improved %%files section, and added use of %%{prefix} and install-info
  (well,... no. The info file has not dir info inside, commented out)
