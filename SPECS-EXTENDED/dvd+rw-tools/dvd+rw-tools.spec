Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		dvd+rw-tools
Version:	7.1
Release:	33%{?dist}
Summary:	Toolchain to master DVD+RW/+R media
License:	GPLv2
URL:		https://fy.chalmers.se/~appro/linux/DVD+RW/

Source:		https://fy.chalmers.se/~appro/linux/DVD+RW/tools/dvd+rw-tools-%{version}.tar.gz
Source1:	index.html
Patch1:		dvd+rw-tools-7.0.manpatch
Patch2:		dvd+rw-tools-7.0-wexit.patch
Patch3:		dvd+rw-tools-7.0-glibc2.6.90.patch
Patch4:		dvd+rw-tools-7.0-reload.patch
Patch5:		dvd+rw-tools-7.0-wctomb.patch
Patch6:		dvd+rw-tools-7.0-dvddl.patch
Patch7:		dvd+rw-tools-7.1-noevent.patch
Patch8:		dvd+rw-tools-7.1-lastshort.patch
Patch9:		dvd+rw-tools-7.1-format.patch
Patch10:	dvd+rw-tools-7.1-bluray_srm+pow.patch
Patch11:	dvd+rw-tools-7.1-bluray_pow_freespace.patch
Patch12:	dvd+rw-tools-7.1-sysmacro-inc.patch

Requires:	genisoimage
BuildRequires:	gcc gcc-c++
BuildRequires:	kernel-headers m4

%description
Collection of tools to master DVD+RW/+R media. For further
information see https://fy.chalmers.se/~appro/linux/DVD+RW/.

%prep
%setup -q
%patch 1 -p1 -b .manpatch
%patch 2 -p1 -b .wexit
%patch 3 -p1 -b .glibc2.6.90
%patch 4 -p1 -b .reload
%patch 5 -p0 -b .wctomb
%patch 6 -p0 -b .dvddl
%patch 7 -p1 -b .noevent
%patch 8 -p1 -b .lastshort
%patch 9 -p1 -b .format
%patch 10 -p1 -b .pow
%patch 11 -p1 -b .freespace
%patch 12 -p1 -b .sysmacro

install -m 644 %{SOURCE1} index.html

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export CXXFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export LDFLAGS="$RPM_LD_FLAGS"
make WARN="-DDEFAULT_BUF_SIZE_MB=16 -DRLIMIT_MEMLOCK" %{?_smp_mflags}

%install
# make install DESTDIR= does not work here
%makeinstall

%files
%license LICENSE
%doc index.html
%{_bindir}/*
%{_mandir}/man1/*.1*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.1-33
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul  9 2018 Peter Robinson <pbrobinson@fedoraproject.org> 7.1-28
- Fix version check

* Mon Jul  9 2018 Peter Robinson <pbrobinson@fedoraproject.org> 7.1-27
- Package cleanups, add patch to fix FTBFS, use %%license

* Fri Feb 23 2018 Florian Weimer <fweimer@redhat.com> - 7.1-26
- Use LDFLAGS from redhat-rpm-config

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 09 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 7.1-20
- serious typo in spec file - patch10 applied twice, patch11 not at all

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 7.1-18
- Rebuilt for GCC 5 C++11 ABI change

* Fri Nov 14 2014 Frantisek Kluknavsky <fkluknav@redhat.com> - 7.1-17
- added dvd+rw-tools-7.1-bluray_pow_freespace.patch,
  based on https://bugzilla.redhat.com/show_bug.cgi?id=1082360
  count nwa (next writeable address) even in pow (pseudo overwrite) mode

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 7.1-13
- when formating blu-ray as srm+pow, handle it later correctly as srm+pow, not srm
(credits Thomas Schmitt)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 27 2012 Honza Horak <hhorak@redhat.com> - 7.1-11
- Spec file cleanup
- Print error in case we want to write already written DVD-RW in Sequential
  Recording mode (bug #810838)
- Add man page for dvd+rw-format

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 16 2012 Honza Horak <hhorak@redhat.com> - 7.1-9
- Allow buffer length of the block to be shorter than multiple of 16, 
  even in case of DAO writing (replaces the previous fix)
  Resolves: #810483

* Fri Apr 06 2012 Honza Horak <hhorak@redhat.com> - 7.1-8
- Align blocks count to multiple of 16 also in case of DAO writing
  Resolves: #810483

* Wed Mar 07 2012 Honza Horak <hhorak@redhat.com> - 7.1-7
- applied patch from Petr Sumbera to handle Teac DVD drive timeout issue
  Resolves: #799299

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 23 2010 Roman Rakus <rrakus@redhat.com> - 7.1-5
- Compile with -fno-strict-aliasing CFLAG

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 17 2008 Roman Rakus <rrakus@redhat.com> - 7.1-2
- Allow burn small images on dvd-dl
  Resolves: #476154

* Fri Aug 15 2008 Roman Rakus <rrakus@redhat.com> - 7.1-1
- new version 7.1

* Wed Mar 26 2008 Harald Hoyer <harald@redhat.com> 7.0-11
- fixed widechar overflow (bug #426068) (patch from Jonathan Kamens)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 7.0-9
- Autorebuild for GCC 4.3

* Tue Nov 20 2007 Harald Hoyer <harald@redhat.com> - 7.0-8
- added a patch to fix a reload problem on some drives, 
  after a successful burn

* Fri Aug 31 2007 Matthias Saou <https://freshrpms.net/> 7.0-7
- Minor spec file cleanups (tabs vs. spaces, etc.).
- Use install instead of cp for the html file to avoid umask differences.

* Fri Aug 17 2007 Harald Hoyer <harald@rawhide.home> - 7.0-6
- changed license to GPLv2

* Wed Aug 15 2007 Harald Hoyer <harald@redhat.com> - 7.0-5
- added limits.h to transport.hxx

* Thu Jun 21 2007 Harald Hoyer <harald@redhat.com> - 7.0-4
- fixed exit status (#243036)
- Allow session to cross 4GB boundary regardless of medium type.
  Add a -F option (used instead of -M or -Z), which displays 
  next_session offset and capacity. (#237967)

* Tue Feb 27 2007 Harald Hoyer <harald@redhat.com> - 7.0-3
- fixed specfile issues (#209985)

* Thu Dec 14 2006 Harald Hoyer <harald@redhat.com> - 7.0-0.4
- set pthread stack size according to limit (#215818)

* Wed Dec 13 2006 Harald Hoyer <harald@redhat.com> - 7.0-0.3
- use _SC_PHYS_PAGES instead of _SC_AVPHYS_PAGES to determine available memory
- Resolves: rhbz#216794

* Fri Nov 03 2006 Harald Hoyer <harald@redhat.com> - 7.0-0.2
- define RLIMIT_MEMLOCK, which should resolve the memlock problems

* Thu Oct 26 2006 Harald Hoyer <harald@redhat.com> - 7.0-0.1
- new version 7.0
