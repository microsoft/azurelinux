Summary:    A GNU tool for automatically configuring source code
Name:       autoconf213
Version:    2.13
Release:    49%{?dist}
License:    GPLv2+
URL:        http://www.gnu.org/software/autoconf/
Source:     https://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.gz
Patch0:     autoconf-2.13-versioning.patch
Patch1:     autoconf213-destdir.patch
Patch2:     autoconf213-info.patch
Vendor:     Microsoft Corporation
Distribution:  Mariner

Requires:   gawk, m4 >= 1.1, coreutils
BuildRequires:   texinfo, m4 >= 1.1, perl, gawk, dejagnu, flex
BuildArch:  noarch

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to specify
various configuration options.
 
You should install Autoconf if you are developing software and you
would like to use it to create shell scripts that will configure your
source code packages. If you are installing Autoconf, you will also
need to install the GNU m4 package.
 
Note that the Autoconf package is not required for the end-user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not their
use.

%prep
%setup -q -n autoconf-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

mv autoconf.texi autoconf213.texi
rm -f autoconf.info

%build
%configure --program-suffix=-%{version}
make

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}/%{_bindir}/autoscan-%{version}

# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm -f ${RPM_BUILD_ROOT}%{_infodir}/standards*

%check
# Skip AC_FUNC_GETLOADAVG which fails to find /dev/kmem due to CONFIG_DEVKMEM not being set
sed -i 's/AC_DEFUN(AC_FUNC_GETLOADAVG,/AU_DEFUN(AC_FUNC_GETLOADAVG,/g' ./acspecific.m4
# Skip Fortan 77 (F77) tests which are not supported with our version of gcc
sed -i 's/AC_DEFUN(AC_PROG_F77,/AU_DEFUN(AC_PROG_F77,/g' ./acspecific.m4
sed -i 's/AC_DEFUN(AC_PROG_F77_WORKS,/AU_DEFUN(AC_PROG_F77_WORKS,/g' ./acspecific.m4
sed -i 's/AC_DEFUN(AC_F77_LIBRARY_LDFLAGS,/AU_DEFUN(AC_F77_LIBRARY_LDFLAGS,/g' ./acspecific.m4
make check
 
%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :
 
%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi
 
%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/*
%{_infodir}/*.info*
%{_datadir}/autoconf-%{version}/
 
%changelog
* Fri Jul 1 2022 Jamie Magee <jamagee@microsoft.com> - 2.13-49
- Switch from FTP to HTTPS source

*   Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.13-48
-   Removing the explicit %%clean stage.

*   Mon Dec 07 2020 Andrew Phelps <anphel@microsoft.com> 2.13-47
-   Fix check tests.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.13-46
-   Added %%license line automatically
*   Wed Apr 15 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.13-45
-   Initial CBL-Mariner import from Fedora 32 (license: MIT).
-   License verified.
-   Remove unused patches.
*   Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-44
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
*   Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-43
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild 
*   Thu Feb 21 2019 Jeroen van Meeuwen (Kolab Systems) <vanmeeuwen@kolabsys.com> - 2.13-42
-   Ensure %{_infodir}/standards* is not installed in install, or conflict with binutils'
    version.
*   Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-41
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild 
*   Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-40
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
*   Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-39
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
*   Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-38
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
*   Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-37
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
*   Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-36
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
*   Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-35
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
*   Fri Feb 20 2015 Pavel Raiskup <praiskup@redhat.com> - 2.13-34
-   don't ship broken (and ancient) autoscan (rhbz#1194568)
-   drop explicit 'Requires: perl' (related rhbz#1194568)
*   Mon Jul 28 2014 Pavel Raiskup <praiskup@redhat.com> - 2.13-32
-   don't build-require compat-gcc-34-g77 at all 
*   Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-31
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild 
*   Fri Oct 18 2013 Pavel Raiskup <praiskup@redhat.com> - 2.13-30
-   disable g77 tests for RHEL7 builds 
*   Wed Oct 09 2013 Pavel Raiskup <praiskup@redhat.com> - 2.13-29
-   enable testsuite for obsolescent autoconf213
*   Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-28
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
*   Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.13-27
-   Perl 5.18 rebuild
*   Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-26
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild
*   Mon Oct 29 2012 Pavel Raiskup <praiskup@redhat.com> - 2.13-25
-   remove unnecessary BR, remove trailing whitespaces 
*   Fri Oct 12 2012 Pavel Raiskup <praiskup@redhat.com> - 2.13-24
-   update license tag in specfile 
*   Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-23
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
*   Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-22
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
*   Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-21
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
*   Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-20
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
*   Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-19
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
*   Wed Aug 08 2007 Karsten Hopp <karsten@redhat.com> 2.13-18
-   update license tag 
*   Mon Feb 26 2007 Karsten Hopp <karsten@redhat.com> 2.13-17
-   our tarball hat different size and timestamps then the upstream
    tarball. No changes, though.
-   rebuild with upstream sources
*   Thu Feb 15 2007 Karsten Hopp <karsten@redhat.com> 2.13-16
-   delete old autoconf.info file
*   Thu Feb 15 2007 Karsten Hopp <karsten@redhat.com> 2.13-15
-   add autoconf213 info entry
-   add disttag
*   Wed Feb 14 2007 Karsten Hopp <karsten@redhat.com> 2.13-14
-   buildrequire perl for autoscan script 
*   Wed Feb 14 2007 Karsten Hopp <karsten@redhat.com> 2.13-13
-   buildroot fixed
-   removed textutils requirement
-   dot removed from summary
-   requires gawk, but not perl
-   use install-info
-   use BuildArch
-   replace tabs with spaces
-   fix defattr
-   use 'make install DESTDIR=...'
*   Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.13-12.1
-   rebuild
*   Mon Feb 27 2006 Karsten Hopp <karsten@redhat.de> 2.13-12
-   require m4 >= 1.1
*   Mon Feb 27 2006 Karsten Hopp <karsten@redhat.de> 2.13-11
-   BuildRequire m4 (#181959)
*   Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
-   rebuilt
*   Mon Feb 21 2005 Karsten Hopp <karsten@redhat.de> 2.13-10
-   Copyright -> License 
*   Thu Sep 23 2004 Daniel Reed <djr@redhat.com> - 2.13-9
-   rebuilt for dist-fc3
*   Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
-   rebuilt
*   Tue Dec  9 2003 Jens Petersen <petersen@redhat.com> - 2.13-7
-   buildrequire texinfo (#111169) [mvd@mylinux.com.ua]
*   Wed Jan 22 2003 Tim Powers <timp@redhat.com>
-   rebuilt
*   Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 2.13-5
-   Fix unpackaged file
*   Fri Jun 28 2002 Jens Petersen <petersen@redhat.com> 2.13-4
-   update url (#66840)
-   added doc files
*   Fri Jun 21 2002 Tim Powers <timp@redhat.com> 2.13-3
-   automated rebuild
*   Thu May 23 2002 Tim Powers <timp@redhat.com> 2.13-2
-   automated rebuild 
*   Wed May 15 2002 Jens Petersen <petersen@redhat.com> 2.13-1
-   new package based on autoconf-2.13-17
-   don't make unversioned bindir symlinks
-   version datadir
-   version info filename, but don't install-info it
-   update AC_OUTPUT_MAKE_DEFS to fix problem with c++exit patch (#62361)
*   Wed Mar 27 2002 Jens Petersen <petersen@redhat.com> 2.13-17
-   add URL
*   Wed Feb 27 2002 Jens Petersen <petersen@redhat.com> 2.13-16
-   add version suffix to bindir files and symlink them to their
    unversioned names
*   Mon Feb 25 2002 Elliot Lee <sopwith@redhat.com> 2.13-15
-   Add wait3test.patch to make sure that the child process actually does
    something that the kernel will take note of. Fixes the failing wait3 test
    that was worked around in time-1.7-15.
*   Mon Aug  6 2001 Tim Powers <timp@redhat.com>
-   rebuilt to fix bug #50761 
*   Thu Jul 26 2001 Than Ngo <than@redhat.com>
-   add patch to fix exit status 
*   Tue Jul 10 2001 Jens Petersen <petersen@redhat.com>
-   add patch to include various standard C headers as needed
    by various autoconf tests (#19114)
-   add patch to autoscan.pl to get a better choice of init
    file (#42071), to test for CPP after CC (#42072) and to
    detect C++ source and g++ (#42073).
*   Tue Jun 26 2001 Jens Petersen <petersen@redhat.com>
-   Add a back-port of _AC_PROG_CXX_EXIT_DECLARATION
    from version 2.50 to make detection of C++ exit()
    declaration prototype platform independent.  The check is
    done in AC_PROG_CXX with the result stored in "confdefs.h".
    The exit() prototype in AC_TRY_RUN_NATIVE is no longer needed.
    (fixes #18829)
*   Wed Nov 29 2000 Bernhard Rosenkraenzer <bero@redhat.com>
-   Fix up interoperability with glibc 2.2 and gcc 2.96:
    AC_TRY_RUN_NATIVE in C++ mode added a prototype for exit() to
    the test code without throwing an exception, causing a conflict
    with stdlib.h --> AC_TRY_RUN_NATIVE for C++ code including stdlib.h
    always failed, returning wrong results
*   Fri Jul 21 2000 Nalin Dahyabhai <nalin@redhat.com>
-   add textutils as a dependency (#14439)
*   Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
-   automatic rebuild
*   Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
-   FHS packaging. 
*   Sun Mar 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
-   fix preun
*   Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
-   add patch to help autoconf clean after itself and not leave /tmp clobbered
    with acin.* and acout.* files (can you say annoying?)
*   Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
-   auto rebuild in the new build environment (release 4)
-   use gawk, not mawk
*   Thu Mar 18 1999 Preston Brown <pbrown@redhat.com>
-   moved /usr/lib/autoconf to /usr/share/autoconf (with automake)
*   Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
-   Injected new description and group.
*   Tue Jan 12 1999 Jeff Johnson <jbj@redhat.com>
-   update to 2.13.
*   Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
-   build against glibc 2.1 
*   Mon Oct 05 1998 Cristian Gafton <gafton@redhat.com>
-   requires perl
*   Thu Aug 27 1998 Cristian Gafton <gafton@redhat.com>
-   patch for fixing /tmp race conditions
*   Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
-   spec file cleanups
-   made a noarch package
-   uses autoconf
-   uses install-info
*   Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
-   built with glibc
