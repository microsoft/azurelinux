Summary:        Statically linked binary providing simplified versions of system commands
Name:           busybox
Version:        1.35.0
Release:        9%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://busybox.net/
Source:         https://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
Source1:        busybox-static.config
Source2:        busybox-petitboot.config
Patch0:         busybox-1.31.1-stime-fix.patch
Patch1:         CVE-2022-28391.patch
Patch2:         awk-input-numbers-are-never-octal-or-hex-only-progra.patch
Patch3:         CVE-2022-30065.patch
Patch4:         ash-fix-use-after-free-in-pattern-substituon-code.patch
Patch5:         ash-fix-use-after-free-in-bash-pattern-substitution.patch
BuildRequires:  gcc
BuildRequires:  glibc-static >= 2.38-1%{?dist}
BuildRequires:  libselinux-devel >= 1.27.7-2
BuildRequires:  libsepol-devel
# libbb/hash_md5_sha.c
# https://bugzilla.redhat.com/1024549
Provides:       bundled(md5-drepper2)

%package petitboot
Summary:        Version of busybox configured for use with petitboot

%description
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries.

%description petitboot
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  The version contained in this
package is a minimal configuration intended for use with the Petitboot
bootloader used on PlayStation 3. The busybox package provides a binary
better suited to normal use.

%prep
%autosetup -p1

%build

cp %{SOURCE1} .config
# set all new options to defaults
yes "" | make oldconfig
mv .config .config1
grep -v \
     -e ^CONFIG_FEATURE_HAVE_RPC \
     -e ^CONFIG_FEATURE_MOUNT_NFS \
     -e ^CONFIG_FEATURE_INETD_RPC \
     .config1 >.config
echo "# CONFIG_FEATURE_HAVE_RPC is not set" >>.config
echo "# CONFIG_FEATURE_MOUNT_NFS is not set" >>.config
echo "# CONFIG_FEATURE_INETD_RPC is not set" >>.config
yes "" | make oldconfig
cat .config
make V=1 CC="gcc %{optflags}"
cp busybox_unstripped busybox.static
cp docs/busybox.1 docs/busybox.static.1

# create busybox optimized for petitboot
make clean
# copy new configuration file
cp %{SOURCE2} .config
# set all new options to defaults
yes "" | make oldconfig
cat .config
make V=1 CC="gcc %{optflags}"
cp busybox_unstripped busybox.petitboot
cp docs/busybox.1 docs/busybox.petitboot.1

%install
mkdir -p %{buildroot}/sbin
install -m 755 busybox.static %{buildroot}/sbin/busybox
install -m 755 busybox.petitboot %{buildroot}/sbin/busybox.petitboot
mkdir -p %{buildroot}/%{_mandir}/man1
install -m 644 docs/busybox.static.1 %{buildroot}/%{_mandir}/man1/busybox.1
install -m 644 docs/busybox.petitboot.1 %{buildroot}/%{_mandir}/man1/busybox.petitboot.1

%files
%license LICENSE
%doc README
/sbin/busybox
%{_mandir}/man1/busybox.1.gz

%files petitboot
%license LICENSE
%doc README
/sbin/busybox.petitboot
%{_mandir}/man1/busybox.petitboot.1.gz

%changelog
* Tue Nov 07 2023 Andrew Phelps <anphel@microsoft.com> - 1.35.0-9
- Bump release to rebuild against glibc 2.38-1

* Wed Oct 04 2023 Minghe Ren <mingheren@microsoft.com> - 1.35.0-8
- Bump release to rebuild against glibc 2.35-6

* Tue Oct 03 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 1.35.0-7
- Bump release to rebuild against glibc 2.35-5

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.35.0-6
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Jul 05 2023 Andrew Phelps <anphel@microsoft.com> - 1.35.0-5
- Bump release to rebuild against glibc 2.35-4

* Fri Oct 07 2022 Andy Caldwell <andycaldwell@microsoft.com> - 1.35.0-4
- Build with `glibc-static` on all platforms

* Wed Aug 10 2022 Muhammad Falak <mwani@microsoft.com> - 1.35.0-3
- Patch CVE-2022-30065
- Introduce patch for: awk: input numbers are never octal or hex
- Introduce patch for: use-after-free in pattern substituon code
- Introduce patch for: use-after-free in bash pattern substitution

* Fri May 20 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.35.0-2
- Patch CVE-2022-28391.

* Thu Jan 06 2022 Henry Li <lihl@microsoft.com> - 1.35.0-1
- Upgrade to version 1.35.0

* Fri Mar 26 2021 Henry Beberman <henry.beberman@microsoft.com> - 1.32.0-2
- Patch CVE-2021-28831

* Thu Oct 15 2020 Mateusz Malisz <mamalisz@microsoft.com> - 1.32.0-1
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- License Verified
- Add -fno-stack-protector for x86 builds
- Changed version from 1.31.1 to 1.32.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.31.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 13 2019 Tom Callaway <spot@fedoraproject.org> - 1:1.31.1-1
- update to 1.31.1 (fix FTBFS)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.30.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 13 2019 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.30.1-2
- Tweak .config files

* Mon May 13 2019 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.30.1-1
- Update to 1.30.1

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.28.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.28.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 05 2018 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.28.3-1
- Update to 1.28.3

* Mon Mar 26 2018 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.28.2-1
- Update to 1.28.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.26.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.26.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.26.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 30 2017 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.26.2-1
- Update to 1.26.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.22.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.22.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.22.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 1:1.22.1-3
- Provides: bundled(md5-drepper2)  (rhbz #1024549)

* Thu Mar 05 2015 Dan Horák <dan[at]danny.cz> - 1:1.22.1-2
- drop unneeded patch (#1182677)

* Tue Dec 16 2014 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.22.1-1
- Update to 1.22.1

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.19.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.19.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1:1.19.4-13
- uClibc not supported on aarch64

* Fri May 16 2014 Jaromir Capik <jcapik@redhat.com> - 1:1.19.4-12
- Disabled uClibc on ppc64le

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.19.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 24 2013 Dan Horák <dan[at]danny.cz> - 1.19.4-10
- disable uClib on s390(x)

* Wed May 15 2013 Karsten Hopp <karsten@redhat.com> 1.19.4-9
- disable uClibc on ppc, too

* Wed May 15 2013 Karsten Hopp <karsten@redhat.com> 1.19.4-8
- include sys/resource.h for RLIMIT_FSIZE (rhbz #961542) on PPC*

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.19.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.19.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun  1 2012 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.4-5
- Added bboconfig applet - useful for running testsuite

* Fri Apr 13 2012 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.4-4
- Fixed breakage with newer kernel headers
- Excluded Sun-RPC dependednt features not available in newer static glibc

* Mon Mar 12 2012 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.4-3
- Tweaked spec file again to generate even more proper debuginfo package

* Wed Mar  7 2012 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.4-2
- Tweaked spec file to generate proper debuginfo package

* Tue Feb 28 2012 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.4-1
- update to 1.19.4

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 31 2011 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.3-1
- update to 1.19.3

* Sat Aug 27 2011 Daniel Drake <dsd@laptop.org> - 1:1.18.2-6
- Fix compilation against uClibc and Linux-3.0 headers

* Fri Aug 26 2011 Daniel Drake <dsd@laptop.org> - 1:1.18.2-5
- Remove Linux 2.4 support from insmod/modprobe/etc.
- Fixes build failures on ARM, where such ancient syscalls are not present

* Sat Jun 11 2011 Peter Robinson <pbrobinson@gmail.com> - 1:1.18.2-4
- Add support for ARM

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Tom Callaway <spot@fedoraproject.org> - 1:1.18.2-2
- apply fixes from upstream

* Mon Feb  7 2011 Tom Callaway <spot@fedoraproject.org> - 1:1.18.2-1
- update to 1.18.2
- use system uClibc

* Mon Oct  4 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-10
- add compatibility with man-db config file (#639461)

* Wed Sep 29 2010 jkeating - 1:1.15.1-9
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-8
- fix build system so that it works with make 3.82 too

* Wed May  5 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-7
- teach uclibc to use /etc/localtime

* Wed Feb 24 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-6
- tweak installed docs

* Wed Jan 27 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-5
- enable Fedora-specific uname -p behavior (#534081)

* Fri Nov 26 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-4
- make uclibc use 32-bit compat struct utmp (#541587)

* Fri Nov 10 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-3
- re-enable rpm applet (#534092)

* Fri Oct  2 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-2
- add manpage generation (#525658)

* Sun Sep 13 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-1
- Rebase to 1.15.1

* Fri Sep 11 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.14.1-6
- REALLY fix build on s390, ia64

* Fri Sep 11 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.14.1-5
- fix build on s390, ia64

* Wed Sep 02 2009 Chris Lumens <clumens@redhat.com> 1.14.1-4
- Remove busybox-anaconda (#514319).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Ivana Varekova <varekova@redhat.com> - 1:1.14.1-2
- add new options to readlink - patch created by Denys Valsenko

* Thu May 28 2009 Ivana Varekova <varekova@redhat.com> - 1:1.14.1-1
- fix ppc problem
- update to 1.14.1

* Sun May 24 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 1:1.13.2-4
- Fixing FTBFS on i586/x86_64/ppc, ppc64 still an issue:
- Updated uClibc to 0.9.30.1, subsequently:
- Removed uClibc-0.9.30 patch (merged upstream).
- Added uClibc-0.9.30.1-getline.patch -- prevents conflicts with getline()
  from stdio.h
- Temporarily disable C99 math to bypass ppc bug, see https://bugs.uclibc.org/show_bug.cgi?id=55

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.13.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  9 2009 Ivana Varekova <varekova@redhat.com> - 1:1.13.2-2
- use uClibc instead of glibc for static build - thanks Denys Vlasenko

* Mon Jan 19 2009 Ivana Varekova <varekova@redhat.com> - 1:1.13.2-1
- update to 1.13.2

* Tue Dec  2 2008 Ivana Varekova <varekova@redhat.com> - 1:1.12.1-2
- enable selinux in static version of busybox (#462724)

* Mon Nov 10 2008 Ivana Varekova <varekova@redhat.com> - 1:1.12.1-1
- update to 1.12.1

* Tue Aug 26 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.3-3
- fix findfs problem - #455998

* Wed Jul 23 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.3-2
- add findfs to static version of busybox
  (kexec-tools need it #455998)

* Tue Jun 10 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.3-1
- update to 1.10.3

* Fri May 16 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.2-1
- update to 1.10.2

* Thu May  9 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.1-1
- update to 1.10.1

* Thu Feb 14 2008 Ivana Varekova <varekova@redhat.com> - 1:1.9.1-1
- update to 1.9.1
- fix a problem with netfilter.h - thanks dwmw2

* Fri Feb  8 2008 Ivana Varekova <varekova@redhat.com> - 1:1.9.0-2
- fix hwclock on ia64 machines

* Mon Jan  7 2008 Ivana Varekova <varekova@redhat.com> - 1:1.9.0-1
- update to 1.9.0

* Mon Dec  3 2007 Ivana Varekova <varekova@redhat.com> - 1:1.8.2-1
- update to 1.8.2

* Wed Nov 21 2007 Ivana Varekova <varekova@redhat.com> - 1:1.8.1-1
- update to 1.8.1

* Tue Nov  6 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.3-1
- update to 1.7.3
- remove --gc-sections from static build Makefile

* Thu Nov  1 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.2-4
- fix 359371 - problem with grep output

* Wed Oct 31 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.2-3
- fix another sed problem (forgotten fflush - #356111)

* Mon Oct 29 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.2-2
- fix sed problem with output (#356111)

* Mon Oct 22 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.2-1
- update to 1.7.2

* Tue Sep  4 2007 Ivana Varekova <varekova@redhat.com> - 1:1.6.1-2
- spec file cleanup

* Mon Jul 23 2007 Ivana Varekova <varekova@redhat.com> - 1:1.6.1-1
- update to 1.6.1

* Fri Jun  1 2007 Ivana Varekova <varekova@redhat.com> - 1:1.5.1-2
- add msh shell

* Thu May 24 2007 Ivana Varekova <varekova@redhat.com> - 1:1.5.1-1
- update to 1.5.1

* Sat Apr  7 2007 David Woodhouse <dwmw2@redhat.com> - 1:1.2.2-8
- Add busybox-petitboot subpackage

* Mon Apr  2 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-7
- Resolves: 234769
  busybox ls does not work without a tty

* Mon Feb 19 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-6
- incorporate package review feedback

* Fri Feb  2 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-5
- fix id_ps patch (thanks Chris MacGregor)

* Tue Jan 30 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-4
- remove debuginfo

* Mon Jan 22 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-3
- Resolves: 223620
  id output shows context twice
- fix iptunnel x kernel-headers problem

* Mon Dec 10 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-2
- enable ash

* Thu Nov 16 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-1
- update to 1.2.2

* Mon Aug 28 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.0-3
- fix #200470 - dmesg aborts
  backport dmesg upstream changes

* Mon Aug 28 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.0-2
- fix #202891 - tar problem

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2.0-1.1
- rebuild

* Tue Jul  4 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.0-1
- update to 1.2.0

* Thu Jun  8 2006 Jeremy Katz <katzj@redhat.com> - 1:1.1.3-2
- fix so that busybox.anaconda has sh

* Wed May 31 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.3-1
- update to 1.1.3

* Mon May 29 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.2-3
- fix Makefile typo (#193354)

* Fri May  5 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.2-1
- update to 1.1.2

* Thu May  4 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.1-2
- add -Z option to id command, rename ps command -Z option (#190534)

* Wed May 03 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.1-1
- update to 1.1.1
- fix CVE-2006-1058 - BusyBox passwd command
  fails to generate password with salt (#187386)
- add -minimal-toc option
- add RPM_OPT_FLAGS
- remove asm/page.h used sysconf command to get PAGE_SIZE
- add overfl patch to aviod Buffer warning

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.01-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.01-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Oct 13 2005 Daniel Walsh <dwalsh@redhat.com> -  1.01-2
- Add sepol for linking load_policy

* Thu Sep  1 2005 Ivana Varekova <varekova@redhat.com> - 1.01-1
- update to 1.01

* Tue May 11 2005 Ivana Varekova <varekova@redhat.com> - 1.00-5
- add debug files to debug_package

* Mon Mar  7 2005 Ivana Varekova <varekova@redhat.com> - 1.00-4
- rebuilt

* Wed Jan 26 2005 Ivana Varekova <varekova@redhat.com> - 1.00-3
- update to 1.00 - fix bug #145681
- rebuild

* Thu Jan 13 2005 Jeremy Katz <katzj@redhat.com> - 1.00.rc1-6
- enable ash as the shell in busybox-anaconda

* Sat Oct  2 2004 Bill Nottingham <notting@redhat.com> - 1.00.rc1-5
- fix segfault in SELinux patch (#134404, #134406)

* Fri Sep 17 2004 Phil Knirsch <pknirsch@redhat.com> - 1.00.rc1-4
- Fixed double free in freecon() call (#132809)

* Fri Sep 10 2004 Daniel Walsh <dwalsh@redhat.com> - 1.00.rc1-3
- Add CONFIG_STATIC=y for static builds

* Wed Aug 25 2004 Jeremy Katz <katzj@redhat.com> - 1.00.rc1-2
- rebuild

* Fri Jun 25 2004 Dan Walsh <dwalsh@redhat.com> 1.00-pre10.1
- Add BuildRequires libselinux-devel
- Update to latest from upstream

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 11 2004 Karsten Hopp <karsten@redhat.de> 1.00.pre8-4
- add mknod to busybox-anaconda

* Wed Apr 21 2004 Karsten Hopp <karsten@redhat.de> 1.00.pre8-3
- fix LS_COLOR in anaconda patch

* Tue Mar 23 2004 Jeremy Katz <katzj@redhat.com> 1.00.pre8-2
- add awk to busybox-anaconda

* Sat Mar 20 2004 Dan Walsh <dwalsh@redhat.com> 1.00-pre8.1
- Update with latest patch.
- Turn off LS_COLOR in static patch

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Dan Walsh <dwalsh@redhat.com> 1.00-pre5.2
- Fix is_selinux_enabled calls

* Mon Dec 29 2003 Dan Walsh <dwalsh@redhat.com> 1.00-pre5.1
-Latest update

* Wed Nov 26 2003 Dan Walsh <dwalsh@redhat.com> 1.00-pre3.2
- Add insmod

* Mon Sep 15 2003 Dan Walsh <dwalsh@redhat.com> 1.00-pre3.1
- Upgrade to pre3

* Thu Sep 11 2003 Dan Walsh <dwalsh@redhat.com> 1.00.2
- Upgrade selinux support

* Wed Jul 23 2003 Dan Walsh <dwalsh@redhat.com> 1.00.1
- Upgrade to 1.00 package

* Wed Jul 16 2003 Elliot Lee <sopwith@redhat.com> 0.60.5-10
- Rebuild

* Mon Jul 14 2003 Jeremy Katz <katzj@redhat.com> 0.60.5-9
- rebuild

* Mon Jul 14 2003 Jeremy Katz <katzj@redhat.com> 0.60.5-8
- add dmesg to busybox-anaconda

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Jeremy Katz <katzj@redhat.com> 0.60.5-5
- lost nolock for anaconda mount when rediffing, it returns (#81764)

* Mon Jan 6 2003 Dan Walsh <dwalsh@redhat.com> 0.60.5-4
- Upstream developers wanted to eliminate the use of floats

* Thu Jan 3 2003 Dan Walsh <dwalsh@redhat.com> 0.60.5-3
- Fix free to work on large memory machines.

* Sat Dec 28 2002 Jeremy Katz <katzj@redhat.com> 0.60.5-2
- update Config.h for anaconda build to include more useful utils

* Thu Dec 19 2002 Dan Walsh <dwalsh@redhat.com> 0.60.5-1
- update latest release

* Thu Dec 19 2002 Dan Walsh <dwalsh@redhat.com> 0.60.2-8
- incorporate hammer changes

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 06 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix compilation on mainframe

* Tue Apr  2 2002 Jeremy Katz <katzj@redhat.com>
- fix static busybox (#60701)

* Thu Feb 28 2002 Jeremy Katz <katzj@redhat.com>
- don't include mknod in busybox.anaconda so we get collage mknod

* Fri Feb 22 2002 Jeremy Katz <katzj@redhat.com>
- rebuild in new environment

* Wed Jan 30 2002 Jeremy Katz <katzj@redhat.com>
- update to 0.60.2
- include more pieces for the anaconda version so that collage can go away
- make the mount in busybox.anaconda default to -onolock

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
`- automated rebuild

* Mon Jul  9 2001 Tim Powers <timp@redhat.com>
- don't obsolete sash
- fix URL and spelling in desc. to satisfy rpmlint

* Thu Jul 05 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add missing defattr for anaconda subpackage

* Thu Jun 28 2001 Erik Troan <ewt@redhat.com>
- initial build for Red Hat
