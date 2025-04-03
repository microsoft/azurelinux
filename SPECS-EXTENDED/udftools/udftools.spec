Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Linux UDF Filesystem userspace utilities
Name: udftools
Version: 2.3
Release: 10%{?dist}
License: GPL-2.0-or-later
URL: https://sourceforge.net/projects/linux-udf/
Source: https://github.com/pali/udftools/releases/download/%{version}/udftools-%{version}.tar.gz
Patch1: udftools-2.3-backported_fixes.patch
BuildRequires: make
BuildRequires: readline-devel, ncurses-devel
BuildRequires: autoconf, automake, libtool, perl-Carp
BuildRequires: udev
Requires: udev

%description
Linux UDF Filesystem userspace utilities.


%prep
%autosetup -p1

%build
#./bootstrap #not in the tarball anymore, lets use pregenerated autotools
##export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing --std=gnu99"
%configure
%make_build
##%%{__make} %%{?_smp_mflags}

%install
%make_install
#./libtool --finish %%{buildroot}%%{_libdir} #causes failure and is probably unneeded, we dont ship a library
rm -rf %{buildroot}%{_bindir}/udffsck


%files
%doc AUTHORS NEWS
%license COPYING
%{_bindir}/*
%{_sbindir}/*
%{_pkgdocdir}/*
%{_mandir}/man?/*
%{_udevrulesdir}/80-pktsetup.rules


%changelog
* Mon Jan 13 2025 Archana Shettigar <v-shettigara@microsoft.com> - 2.3-10
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Jiri Kucera <jkucera@redhat.com> - 2.3-2
- wrudf: Fix parsing Volume Descriptor Sequence
- wrudf: Exit on allocation failure

* Wed Jun 09 2021 Jiri Kucera <jkucera@redhat.com> - 2.3-1
- Update to 2.3

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 20 2020 Filipe Rosset <rosset.filipe@gmail.com> - 2.2-1
- Update to 2.2


* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.1-3
- Rebuild for readline 8.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 29 2018 Filipe Rosset <rosset.filipe@gmail.com> - 2.1-1
- new upstream version 2.1 fixes rhbz #1625987 + spec cleanup and modernization

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.3-1
- rebase to 1.3

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.2-2
- Rebuild for readline 7.x

* Wed Jul 13 2016 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.2-1
- Rebase from a new upstream, dropped patches
- Several binaries moved from bin to sbin

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0b3-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0b3-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 20 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.0.0b3-29
- FTBFS fixed, --std=gnu89 is no longer default with gcc-5

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0b3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0b3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 09 2014 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.0.0b3-26
- added missing option in man pages

* Fri Oct 04 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.0.0b3-25
- invalid source url fixed

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0b3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 16 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.0.0b3-23
- Build dependency on txt2man unacceptable. Included final man page wrudf.1 instead of source.

* Tue Apr 16 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.0.0b3-22
- added man page for wrudf

* Mon Apr 15 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.0.0b3-21
- added "--help"/"-h" with basic info to wrudf

* Fri Apr 05 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.0.0b3-20
- udffsck is an empty placeholder, erased

* Mon Mar 25 2013 Harald Hoyer <harald@redhat.com> 1.0.0b3-19
- run autoreconf to support aarch64 architecture
Resolves: rhbz#926671

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0b3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 18 2012 Honza Horak <hhorak@redhat.com> - 1.0.0b3-17
- Minor spec file fixes

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0b3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 26 2012 Honza Horak <hhorak@redhat.com> - 1.0.0b3-15
- fixed segmentation fault
  Resolves: #685005
- fixed some most obvious issues from static analysis

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0b3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0b3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 23 2010 Roman Rakus <rrakus@redhat.com> - 1.0.0b3-12
- Build with -fno-strict-aliasing CFLAG

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0b3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0b3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.0b3-9
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Harald Hoyer <harald@redhat.com> - 1.0.0b3-8
- fixed compile issues
- added more bigendian patches
- changed license tag

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 1.0.0b3-7
- FC6 rebuild.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 1.0.0b3-6
- Add ncurses-devel build requirement, since it's not pulled in anymore.
- Add patch to fix as many trivial warnings as possible. Some stuff seems to
  still not be 64bit clean, though.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 1.0.0b3-5
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 1.0.0b3-4
- Rebuild for new gcc/glibc.
- Exclude the static library... there isn't even a header file.

* Tue May  3 2005 Matthias Saou <http://freshrpms.net/> 1.0.0b3-3
- Include patches to fix big endian issue and gcc4 compile.

* Mon Feb  7 2005 Matthias Saou <http://freshrpms.net/> 1.0.0b3-1
- Initial RPM release, based on spec file from John Treacy.
- Exclude .la file.
- Remove unneeded /sbin/ldconfig calls (only a static lib for now).

