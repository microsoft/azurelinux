%global pkglibdir	%{_libdir}/dietlibc

%ifarch x86_64
%bcond_without		ssp
%else
%bcond_with		ssp
%endif

%global target_cpu	%{_target_cpu}

Summary:        Small libc implementation
Name:           dietlibc
Version:        0.34
Release:        6%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.fefe.de/dietlibc/
Source0:        https://www.fefe.de/dietlibc/%{name}-%{version}.tar.xz
Patch1:         dietlibc-insecure-defpath.patch

BuildRequires:  gcc
BuildRequires:  gdb

Requires:       %{name}-devel = %{version}-%{release}
#Requires:	dietlibc-lib = %%{version}-%%{release}}

%package devel
Summary:        dietlibc development files

Requires:       %{name} = %{version}-%{release}

Provides:       %{name}-header = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}
Provides:       %{name}-static%{?_isa} = %{version}-%{release}

%package lib
Summary:        Dynamic libraries for dietlibc

Requires:       %{name} = %{version}-%{release}

%description
The diet libc is a libc that is optimized for small size. It can be
used to create small statically linked binaries for Linux on alpha,
arm, hppa, ia64, i386, mips, s390, sparc, sparc64, ppc and x86_64.

%description devel
The diet libc is a libc that is optimized for small size. It can be
used to create small statically linked binaries for Linux on alpha,
arm, hppa, ia64, i386, mips, s390, sparc, sparc64, ppc and x86_64.

This package contains the object files for dietlibc.

%description lib
The diet libc is a libc that is optimized for small size. It can be
used to create small statically linked binaries for Linux on alpha,
arm, hppa, ia64, i386, mips, s390, sparc, sparc64, ppc and x86_64.

This package contains the dynamic libraries for dietlibc.

%prep
%setup -q

%patch1

%if %{without ssp}
sed -i -e 's!^#define WANT_SSP$!// \0!g;
	   s!.*\(#define WANT_STACKGAP\).*!\1!g' dietfeatures.h
%global xtra_fixcflags	-fno-stack-protector
%else
%global xtra_fixcflags	%{nil}
%endif

sed -i \
    -e '/#define \(WANT_LARGEFILE_BACKCOMPAT\|WANT_VALGRIND_SUPPORT\)/d' \
    dietfeatures.h

%ifarch arm
sed -i \
	-e '/#define WANT_DYN_PAGESIZE/{c\'	\
	-e '#define WANT_ELFINFO'		\
	-e '}'					\
	dietfeatures.h
%endif

%global fixcflags	-fomit-frame-pointer -fno-exceptions -fno-asynchronous-unwind-tables %{xtra_fixcflags} -Os -g3 -Werror-implicit-function-declaration -Wno-unused -Wno-switch
%global basemakeflags	prefix=%{pkglibdir} BINDIR=%{_bindir} MAN1DIR=%{_mandir}/man1 CFLAGS="%{optflags} %{fixcflags} $XTRA_CFLAGS" PDIET=%{pkglibdir} STRIP=:
%global makeflags	%{basemakeflags}


%build
make %{makeflags} all %{?_smp_mflags}

# 'dyn' target is not SMP safe
#make %%makeflags dyn


%install
install -d -m755 %{buildroot}%{_sysconfdir}
make %{makeflags} DESTDIR=%{buildroot} install

ln -s lib-%{_arch} %{buildroot}%{pkglibdir}/lib-%{_arch}-%{_vendor}

chmod a-x %{buildroot}%{pkglibdir}/lib-*/*.o
rm -f %{buildroot}%{_bindir}/dnsd


%check
XTRA_CFLAGS='-fno-builtin'
make %{makeflags} -C test      all %{?_smp_mflags} DIET=$(echo `pwd`/bin-*/diet) -k || :
make %{makeflags} -C test/inet all %{?_smp_mflags} DIET=$(echo `pwd`/bin-*/diet)    || :

cd test
ulimit -m $[ 128*1024 ] -v $[ 256*1024 ] -d $[ 128*1024 ] -s 512

#bash ./runtests-X.sh


%files
%license COPYING
%doc AUTHOR BUGS CAVEAT CHANGES FAQ PORTING README*
%doc SECURITY THANKS TODO
%{_mandir}/*/*
%{_bindir}/*

%files devel
%{pkglibdir}

%changelog
* Tue Mar 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.34-6
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.34-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 25 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.34-1
- 0.34

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-0.6.20170317
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.34-0.5.20170317
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-0.4.20170317
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-0.3.20170317
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-0.2.20170317
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 18 2017 Richard W.M. Jones <rjones@redhat.com> - 0.34-0.1
- Move to much newer upstream version which supports aarch64 and POWER.
- Fix bogus date in changelog.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 15 2016 Dan Horák <dan[at]danny.cz> - 0.33-10
- Enable s390x build

* Fri Aug 12 2016 Peter Robinson <pbrobinson@fedoraproject.org> - 0.33-9
- Exclude aarch64 Power64 s390x

* Mon Jul 25 2016 Jon Ciesla <limburgher@gmail.com> - 0.33-8
- Patch for insecure defpath, BZ 1359768.

* Thu Apr 07 2016 Jon Ciesla <limburgher@gmail.com> - 0.33-7
- Spec cleanup.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Nov 17 2014 Jon Ciesla <limburgher@gmail.com> - 0.33-4
- Fix FTBFS using latest official cvs which drops a test script.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Jon Ciesla <limburgher@gmail.com> - 0.33-1
- Latest upstream.

* Tue Sep 17 2013 Jon Ciesla <limburgher@gmail.com> - 0.33-0.1904.20120825
- Fix typo in %%files, BZ 1008729.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-0.1903.20120825
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 Jon Ciesla <limburgher@gmail.com> - 0.33-0.1902.20120825
- Macro cleanup.
- Merge header subpackage into devel.
- Converted lib <> Conflicts to Requires =.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-0.1901.20120825
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Aug 26 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.33-0.1900.20120825
- updated to recent snapshot
- fixed s390 issues (reported and patched by Dan Horák)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-0.1804.20120330
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 29 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.33-0.1803.20120330
- reverted removal of kernel headers; causes too much trouble

* Sun Apr 29 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.33-0.1802.20120330
- removed local include/linux headers; shipped ones are outdated and
  do not work well with those from the kernel-headers package
- added some '-Wno-*' build flags

* Thu Apr  5 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.33-0.1801.20120330
- updated git-patch (fstatat(2) implementation + actime_r(3) fixes)
- removed local runtests-X.sh; it is in git already

* Sat Mar 31 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.33-0.1800.20120330
- updated to 20120330 CVS snapshot
- versionized the patchset fetched from github
- fixed build on armv7+ systems (#800601)

* Sat Jan 14 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.33-0.1700.20111222
- updated to 20111222 CVS snapshot
- rediffed + updated patchset

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-0.1601.20110311
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Mar 12 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.33-0.1600.20110311
- updated to 20110311 CVS snapshot
- set fixed page size for arm
- disabled linux 2.2/2.4 compatibility code + valgrind nice mode
- reduced stack size for testsuite
- rediffed patches

* Sun Feb 20 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.33-0.1600.20101223
- other ARM enhancements
- fixed missing headers in last utime(2) + fadvise(2) patches

* Sun Feb 20 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.33-0.1505.20101223
- further ARM fixes
- global fixes for utime(2), fadvise*(2)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-0.1504.20101223
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de>
- added common alarm(2) implementation

* Sun Jan  9 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.33-0.1502.20101223
- replaced all the single patches with a big one from
  https://github.com/ensc/dietlibc/commits/rebase
- various ARM-EABI fixes (667852)

* Fri Dec 24 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.33-0.1500.20101223
- updated to 20101223 CVS snapshot

* Fri Jul  9 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.32-1400
- added -static provides (#609606)
- use %%apply, not %%patch
- updated %%release_func macro

* Sat Jul 25 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.32-0
- updated to 0.32
- fixed stackgap/auxvec patch
- added patches to fix SMP builds and to prevent object file stripping
- moved %%changelog entries from 2005 and before into ChangeLog.2005 file

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-9.20090228
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar  1 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.31-8.20090228
- splitted a noarch -header subpackage out of -devel

* Sun Mar  1 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.31-7.20090228
- updated to 20090228
- updated patches

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-7.20081017
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Oct 18 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.31-6.20081017
- updated to 20081017 CVS snapshot
- relaxed some sanity checks on architecture not supported by Fedora
  and use '#warning' instead of '#error'
- fixed ARM dynlib code

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.31-6.20080517
- fix license tag

* Sun May 18 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.31-5.20080517
- updated to 20080517 snapshot
- use patches from git repository

* Sun May 18 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.31-5.20080409
- fixed __signalfd() prototype

* Sat Apr 19 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.31-4.20080409
- update -pagesize patch

* Mon Apr 14 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.31-3.20080409
- removed debug stuff from specfile
- updated patches to work with new isinf() behavior of gcc 4.3

* Sun Apr 13 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.31-2.20080409
- added patch for dynamic PAGE_SIZE support
- fixed/enhanced testsuite and removed the '|| :' in %%check
- improved/fixed floating point support *printf(3)

* Thu Apr 10 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.31-1.20080409
- updated to CVS snapshot 20080409

* Fri Feb 22 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.31-1.20080221
- updated to CVS snapshot 20080221; removed most of the last patches
  as they are now in upstream
- moved files into platform neutral /usr/lib dir (not using %%_lib or
  %%_libdir macro)
- added -devel subpackage due to multiarch issues; main package contains
  only the 'diet' binary plus some tools while -devel holds all the
  header and object files.
- fixed optimized memcpy(3)

* Wed Feb 13 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.31-1.20080212
- updated to CVS snapshot 20080212
- fixed printf regression for '%%+04i' style formats
- added %%check and run a testsuite; it does not succeed now so it is
  for informational purposes only...
- added bunch of patches to fixes big-endian issues in string routines

* Sat Sep  1 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.31-1
- updated to 0.31
- removed the no-stack-protector bits for i386 and x86_64 archs
- improved stack-smash code a little bit
- disabled dynamic lib for all arches
- made objects non-executable to avoid "No build ID note" errors

* Wed Jan 17 2007 David Woodhouse <dwmw2@infradead.org> 0.30-4
- Bump release to be higher than unexplained 0.30-3.fc6

* Wed Jan 17 2007 David Woodhouse <dwmw2@infradead.org> 0.30-3
- Apply workaround for GCC PR26374 to build on PPC again (#182118)

* Fri Sep 15 2006 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.30-2
- rebuilt

* Sun Jul  9 2006 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.30-1
- updated to 0.30
- removed cross-arch support
- disable (non-working) SSP support; enable old stackgap code instead of

* Sat Feb 18 2006 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.29-6
- added '-Os' to the CFLAGS
- exclude PPC arch due to strange compilation errors
