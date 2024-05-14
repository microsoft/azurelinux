Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: A binary file delta generator
Name: xdelta
Version: 3.1.0
Release: 11%{?dist}
License: ASL 2.0
Source0: https://github.com/jmacd/xdelta-devel/releases/download/v%{version}/xdelta3-%{version}.tar.gz
URL: https://xdelta.org/

# for testsuite
BuildRequires:  gcc, gcc-c++
BuildRequires: ncompress
BuildRequires: xz-devel
%if 0%{?with_check}
BuildRequires: sudo
%endif

# Man page day fixes
# ~> proposal: https://code.google.com/p/xdelta/issues/detail?id=158
# ~> private #958492
Patch1: xdelta-3.0.6-man-page-day.patch

%description
Xdelta (X for XCF: the eXperimental Computing Facility at Berkeley) is
a binary delta generator (like a diff program for binaries) and an RCS
version control replacement library. Xdelta uses a binary file delta
algorithm to replace the standard diff program used by RCS

%prep
%setup -q -n %{name}3-%{version}
%patch 1 -p2 -b .man-page-day

%build
%configure
make %{?_smp_mflags} V=0

%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1

install -m755 xdelta3 $RPM_BUILD_ROOT/%{_bindir}
install -m 644 xdelta3.1 $RPM_BUILD_ROOT/%{_mandir}/man1

# Create compat symlinks
pushd $RPM_BUILD_ROOT/%{_bindir}
ln -s xdelta3 xdelta
popd

pushd $RPM_BUILD_ROOT/%{_mandir}/man1
ln -s xdelta3.1 xdelta.1
popd

%check
useradd test
sudo -u test ./xdelta3 test && userdel test

%files
%doc README.md COPYING
%{_bindir}/xdelta*
%{_mandir}/man1/xdelta*

%changelog
* Mon Aug 22 2022 Muhammad Falak <mwani@microsoft.com> - 3.1.0-11
- Run the `%check` section via a non-root user to fix ptest build
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.0-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 30 2018 Pavel Raiskup <praiskup@redhat.com> - 3.1.0-5
- fix FTBFS rhbz#1606730

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 23 2017 Pavel Raiskup <praiskup@redhat.com> - 3.1.0-1
- rebase to latest upstream release (rhbz#1405345)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Pavel Raiskup <praiskup@redhat.com> - 3.0.11-2
- add xz-devel BR and remove the patch1 (per rhbz#1295527)

* Sun Jan 10 2016 Pavel Raiskup <praiskup@redhat.com> - 3.0.11-1
- update to 3.0.11
- remove 'autoreconf -vfi' call

* Wed Jun 17 2015 Jindrich Novy <novyjindrich@gmail.com> - 3.0.9-1
- update to 3.0.9

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Pavel Raiskup <praiskup@redhat.com> - 3.0.7-4
- s/autoreconf -v/autoreconf -vfi/, per #1071980

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Pavel Raiskup <praiskup@redhat.com> - 3.0.7-2
- really remove the gcc-warning patch & remove old Makefile from git
- s/Url/URL/, for both fixes thanks to pshiffer

* Tue Jun 18 2013 Pavel Raiskup <praiskup@redhat.com> - 3.0.7-1
- rebase to 3.0.7, remove unneeded patch (#962800)
- allow the build for 32 bit arches

* Mon May 13 2013 Pavel Raiskup <praiskup@redhat.com> - 3.0.6-1
- rebase to 3.0.6 (#958492)
- cleanup, enable tests, man-page-day fix (private #948411)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 04 2012 Adam Tkac <atkac redhat com> - 3.0.4-1
- update to 3.0.4

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Adam Tkac <atkac redhat com> 3.0.0-1
- update to 3.0.0

* Mon Oct 11 2010 Adam Tkac <atkac redhat com> 3.0-1.z
- update to 3.0z
- obsolete patches:
  - xdelta-1.1.3-aclocal.patch
  - xdelta-1.1.3-edsio.patch
  - xdelta-1.1.4-glib2.patch
  - xdelta-1.1.3-pkgconfig.patch

* Thu Dec 03 2009 Adam Tkac <atkac redhat com> 1.1.4-9
- use appropriate BuildRoot

* Mon Nov 30 2009 Adam Tkac <atkac redhat com> 1.1.4-8
- merge review related fixes (#226552)

* Tue Aug 11 2009 Adam Tkac <atkac redhat com> 1.1.4-7
- update source + project URLs

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct 03 2008 Adam Tkac <atkac redhat com> 1.1.4-4
- updated patches due rpm 4.6 (#465102)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.4-3
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Adam Tkac <atkac redhat com> 1.1.4-2
- rebuild (BuildID feature)
- changed license to GPLv2

* Tue Jan 30 2007 Adam Tkac <atkac redhat com> 1.1.4-1
- version 1.1.4 has been marked as final 1.1.4 version

* Mon Jan 29 2007 Adam Tkac <atkac redhat com> 1.1.4pre1-1
- started using dist macro
- updated to 1.1.4pre1

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> 1.1.3-20
- rebuild

* Tue May 30 2006 Ludek Smid <lsmid@redhat.com> 1.1.3-19
- libtoolize and autotools are now run during build phase
- resolved multilib conflict using pkgconfig tool

* Fri May 05 2006 Ludek Smid <lsmid@redhat.com> 1.1.3-18
- patches created on i386 fail to apply on x86_64 (#190406)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.1.3-17.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1.3-17.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Sep 09 2005 Jindrich Novy <jnovy@redhat.com>1.1.3-17
- link libxdelta against libedsio (#165978)
- add support for large files (#155524)
- port to use glib2 instead of obsolete glib1.2 (#136221)

* Wed Mar 23 2005 Jindrich Novy <jnovy@redhat.com> 1.1.3-16
- fix conflicting storage classes that causes build failure with gcc4
- gcc4 warnfixes
- create backups for patches
- drop libtool BuildRequires
- rebuild with gcc4

* Wed Oct 20 2004 Miloslav Trmac <mitr@redhat.com> - 1.1.3-15
- Add BuildRequires: glib-devel (#123759)
- Properly quote aclocal macro definition

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 19 2003 Elliot Lee <sopwith@redhat.com> 1.1.3-11
- xdelta-config belongs in the -devel subpackage - fix it

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 18 2002 Elliot Lee <sopwith@redhat.com> 1.1.3-9
- Rebuild

* Mon Oct 21 2002 Elliot Lee <sopwith@redhat.com> 1.1.3-8
- Rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Feb 15 2002 Elliot Lee <sopwith@redhat.com> 1.1.3-5
- Undo fixscribble patch, jmacd explained why my code+edsio API was at 
  fault and not xdelta.

* Fri Jan 25 2002 Elliot Lee <sopwith@redhat.com> 1.1.3-4
- Fix the bad estimation of checksum array size that caused libxdelta to
  scribble over unallocated memory when generating a delta.

* Thu Jan 24 2002 Elliot Lee <sopwith@redhat.com> 1.1.3-3
- Fix the lack of xdp_generator_free function
- Use _smp_mflags
- Prevent configure.in from chucking -O3 into CFLAGS

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Sep 24 2001 Than Ngo <than@redhat.com> 1.1.3-1
- update to 1.1.3
- Copyright -> License

* Mon Jul 23 2001 Jeff Johnson <jbj@redhat.com>
- add build dependency on zlib-devel (#49739).

* Tue Jun 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- do not use attr, as it also modifies symlinks in binary rpms :-)

* Tue Jun 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- man-pages owned by root
- include link from lib major version number

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Dec 11 2000 Erik Troan <ewt@redhat.com>
- rebuilt

* Fri Jun 09 2000 Than Ngo <than@redhat.de>
- FHS fixes
- use rpm macros

* Tue May 23 2000 Karsten Hopp <Karsten.Hopp@redhat.de>
- rebuild for 7.0
- changed mandir to /usr/share/man

* Mon Jul 26 1999 Tim Powers <timp@redhat.com>
- rebuilt for 6.1

* Tue May 11 1999 Cristian Gafton <gafton@redhat.com>
- don't ship /usr/info/dir

* Tue Apr 13 1999 Michael Maher <mike@redhat.com>
- built package fpr 6.0
- updated package

* Thu Jul 23 1998 Jeff Johnson <jbj@redhat.com>
- package for powertools.

* Tue Jul 07 1998 Arne Coucheron <arneco@online.no>
  [0.22-1]
- removed running of automake, problem fixed in sources

* Sat Jul 04 1998 Arne Coucheron <arneco@online.no>
  [0.21-1]
- added xdelta.magic to %%doc
- added running of automake before configure to make this version build
- changed %%defattr

* Sat Jun 27 1998 Arne Coucheron <arneco@online.no>
  [0.20-1]

* Sun Jun  7 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [0.19-3]
- fixed configuring sources by add --x-includes=/usr/lib/glib/include
  configure parameter (for glibconfig.h),
- changed Source url to ftp://www.xcf.berkeley.edu/pub/xdelta/
- fixed %%defattr macros (thanks to René Wuttke <Rene.Wuttke@gmx.net>).

* Wed May  6 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [0.19-2]
- %%{version} macro instead %%{PACKAGE_VERSION},
- added -q %%setup parameter,
- added using %%{name} macro in Buildroot, Source and Rquires in devel
  fields.

* Sun May 03 1998 Arne Coucheron <arneco@online.no>
  [0.19-1]
- removed some older changelogs

* Wed Apr 29 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [0.18-2]
- removed COPYING from %%doc (copyright statment is in Copyright field),
- /sbin/ldconfig is now -p parameter in %%post, %%postun,
- replaced "mkdir -p" with "install -d" in %%install,
- added "Requires: xdelta = %%{PACKAGE_VERSION}" for devel,
- added using %%defattr macro in %%files (requires rpm >= 2.4.99),
- added using predefined macro %%{PACKAGE_VERSION} instead %%{version},
- changed permission on /usr/lib/lib*.so links to 644,
- removed /usr/lib/libxdelta.la from devel,
- added striping /usr/lib/lib*.so.*.* libs,
- Buildroot changed to /tmp/xdelta-%%{PACKAGE_VERSION}-root.

* Fri Apr 24 1998 Arne Coucheron <arneco@online.no>
  [0.18-1]
- removed the fakeglib patch

* Wed Apr 08 1998 Arne Coucheron <arneco@online.no>
  [0.15-2]
- splitted the package into a main and devel package

* Sat Apr 04 1998 Arne Coucheron <arneco@online.no>
  [0.15-1]
