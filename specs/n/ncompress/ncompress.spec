# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Fast compression and decompression utilities
Name: ncompress
Version: 5.0
Release: 11%{?dist}
License: Unlicense
URL: https://github.com/vapier/%{name}
Source: https://github.com/vapier/%{name}/archive/refs/tags/v%{version}.tar.gz

# allow to build ncompress
# ~> downstream
Patch0: ncompress-5.0-make.patch

# from dist-git commit 0539779d937
# (praiskup: removed redundant part as -DNOFUNCDEF is defined)
# ~> downstream
Patch1: ncompress-5.0-lfs.patch

# exit when too long filename is given (do not segfault)
# ~> #unknown
# ~> downstream
# Patch2: ncompress-4.2.4.4-filenamelen.patch
# Did not segfault, Prints error 'File name too long'

# permit files > 2GB to be compressed
# ~> #126775
Patch3: ncompress-5.0-2GB.patch

# do not fail to compress on ppc/s390x
# ~> #207001
Patch4: ncompress-5.0-endians.patch

# use memmove instead of memcpy
# ~> 760657
# ~> downstream
Patch5: ncompress-5.0-memmove.patch

# silence gcc warnings
# ~> downstream
# Patch6: ncompress-4.2.4.4-silence-gcc.patch
# Fixed with %ld and brackets are included

BuildRequires: make
BuildRequires: gcc
BuildRequires: glibc-devel

%description
The ncompress package contains the compress and uncompress file
compression and decompression utilities, which are compatible with the
original UNIX compress utility (.Z file extensions).  These utilities
can't handle gzipped (.gz file extensions) files, but gzip can handle
compressed files.

Install ncompress if you need compression/decompression utilities
which are compatible with the original UNIX compress utility.


%prep
%ifarch sparc m68k armv4l ppc s390 s390x ppc64 sparc64
ARCH_FLAGS="$ARCH_FLAGS -DBYTEORDER=1234"
%endif

%ifarch alpha ia64
ARCH_FLAGS="$ARCH_FLAGS -DNOALLIGN=0"
%endif

%autosetup -n %{name}-%{version} -p2

%build
make CFLAGS="%{optflags} %{?nc_endian} %{?nc_align} %{build_ldflags} -std=gnu17"


%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -p -m755 compress $RPM_BUILD_ROOT/%{_bindir}
ln -sf compress $RPM_BUILD_ROOT/%{_bindir}/uncompress
install -p -m644 compress.1 $RPM_BUILD_ROOT%{_mandir}/man1
ln -sf compress.1 $RPM_BUILD_ROOT%{_mandir}/man1/uncompress.1

%check
./tests/runtests.sh


%files
%{_bindir}/compress
%{_bindir}/uncompress
%{_mandir}/man1/*
%doc LZW.INFO README.md


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jan 29 2025 Lukas Javorsky <ljavorsk@redhat.com> - 5.0-9
- Fix the FTBFS caused by new C23 standard
- Resolves: rhbz#2340909

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 24 2022 Ondrej Sloup <osloup@redhat.com> - 5.0-1
- Use autosetup
- Change source links
- Redo patch files and remove obsolete ones
- Add runtests.sh
- Rebase to the latest upstream version (rhbz#1924029)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Pavel Raiskup <praiskup@redhat.com> - 4.2.4.4-14
- fix FTBFS (missing gcc), rhbz#1604928
- cleanup rpmlint issues

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Feb 24 2018 Florian Weimer <fweimer@redhat.com> - 4.2.4.4-12
- Use LDFLAGS from redhat-rpm-config

* Fri Feb 23 2018 Pavel Raiskup <praiskup@redhat.com> - 4.2.4.4-11
- drop fileutils BR, rhbz#1548106

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 01 2013 Pavel Raiskup <praiskup@redhat.com> - 4.2.4.4-1
- upstream is dead -> rebase to fork of Mike Frysinger
- silence gcc warnings, fedora-review fixes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-59
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 03 2012 Ondrej Vasik <ovasik@redhat.com> - 4.2.4-56
- use memmove instead of memcpy to prevent memory overlap corruption
 (#760657)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 23 2010 Ondrej Vasik <ovasik@redhat.com> - 4.2.4-54
- do patch original Makefile.def instead of creating new Makefile

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ondrej Vasik <ovasik@redhat.com> - 4.2.4-51
- check malloc success (#473488)
- fix few compiler warnings, free malloc memory before exit
- new URL

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.2.4-50
- Autorebuild for GCC 4.3

* Fri Feb 09 2007 Peter Vrabec <pvrabec@redhat.com> 4.2.4-49
- fix spec file to meet Fedora standards (#226185) 

* Wed Jan 10 2007 Peter Vrabec <pvrabec@redhat.com> 4.2.4-48
- fix some rpmlint issues

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 4.2.4-47
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Peter Vrabec <pvrabec@redhat.com> 4.2.4-46
- fix endian problem (#207001)

* Thu Aug 10 2006 Peter Vrabec <pvrabec@redhat.com> 4.2.4-45
- fix bss buffer underflow CVE-2006-1168 (#201919)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.2.4-44.1
- rebuild

* Fri Apr 21 2006 Peter Vrabec <pvrabec@redhat.com> 4.2.4-44
- fix problems with compressing zero-sized files (#189215, #189216)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.2.4-43.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.2.4-43.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Sep 22 2005 Peter Vrabec <pvrabec@redhat.com> 4.2.4-43
- compress zero-sized files when -f is used(#167615)

* Fri Mar 18 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuilt

* Thu Feb 10 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuilt

* Tue Oct 05 2004 Than Ngo <than@redhat.com> 4.2.4-40
- permit files > 2GB to be compressed (#126775).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 4.2.4-32
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Trond Eivind Glomsrod <teg@redhat.com> 4.2.4-30
- Don't strip when installing

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Feb 27 2002 Trond Eivind Glomsrod <teg@redhat.com> 4.2.4-28
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Nov 26 2001 Trond Eivind Glomsrod <teg@redhat.com> 4.2.4-26
- Rebuild, to fix problem with broken man page (#56654)

* Wed Nov 21 2001 Trond Eivind Glomsrod <teg@redhat.com> 4.2.4-25
- Exit, don't segfault, when given too long filenames

* Sat Jun 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- s390x change

* Tue May  8 2001 Trond Eivind Glomsrod <teg@redhat.com>
- Make it support large files (structs, stats, opens and of course:
  _don't use signed longs for file size before and after compression_.)
  This should fix #39470

* Thu Apr 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add s390x, patch from Oliver Paukstadt <oliver.paukstadt@millenux.com>

* Mon Nov 13 2000 Oliver Paukstadt <oliver.paukstadt@millenux.com>
- add s390 to the bigendian arch list

* Thu Aug 17 2000 Trond Eivind Glomsrod <teg@redhat.com>
- change category to Applications/File, to match
  gzip and bzip2 
- rename the spec file to ncompress.spec
- add ppc to the bigendian arch list

* Fri Jul 21 2000 Trond Eivind Glomsrod <teg@redhat.com>
- rebuild

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 13 2000 Trond Eivind Glomsrod <teg@redhat.com>
- update URL
- use %%{_mandir}

* Fri May  5 2000 Bill Nottingham <notting@redhat.com>
- fix "build" for ia64

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Tue Jan 12 1999 Cristian Gafton <gafton@redhat.com>
- build on armv4l too
- build for 6.0

* Thu Aug 13 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 22 1997 Cristian Gafton <gafton@redhat.com>
- fixed the spec file

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
