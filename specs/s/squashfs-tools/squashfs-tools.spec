# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: squashfs-tools
Version: 4.6.1
Summary: Utility for the creation of squashfs filesystems
%global forgeurl https://github.com/plougher/%{name}
%global tag %{version}
%forgemeta
URL:	 %{forgeurl}
Source:  %{forgesource}
# https://github.com/plougher/squashfs-tools/pull/231
# https://github.com/plougher/squashfs-tools/issues/230
# https://bugzilla.redhat.com/show_bug.cgi?id=2178510
# Fix a crash caused by an out-of-bounds access that was inadvertently
# re-introduced in a memory leak fix
Release: 7%{dist}
License: GPL-2.0-or-later

BuildRequires: make
BuildRequires: gcc
BuildRequires: zlib-devel
BuildRequires: xz-devel
BuildRequires: lzo-devel
BuildRequires: libattr-devel
BuildRequires: lz4-devel
BuildRequires: libzstd-devel
BuildRequires: help2man

%description
Squashfs is a highly compressed read-only filesystem for Linux.  This package
contains the utilities for manipulating squashfs filesystems.

%prep
%forgesetup

%build
%set_build_flags
pushd squashfs-tools
CFLAGS="%optflags" XZ_SUPPORT=1 LZO_SUPPORT=1 LZMA_XZ_SUPPORT=1 LZ4_SUPPORT=1 ZSTD_SUPPORT=1 make %{?_smp_mflags}

%install
pushd squashfs-tools
make INSTALL_PREFIX=%{buildroot}/usr INSTALL_DIR=%{buildroot}%{_sbindir} INSTALL_MANPAGES_DIR=%{buildroot}%{_mandir}/man1 install

%files
%doc ACKNOWLEDGEMENTS README* CHANGES COPYING USAGE* ACTIONS-README

%{_mandir}/man1/mksquashfs.1.gz
%{_mandir}/man1/unsquashfs.1.gz
%{_mandir}/man1/sqfstar.1.gz
%{_mandir}/man1/sqfscat.1.gz

%{_sbindir}/mksquashfs
%{_sbindir}/unsquashfs
%{_sbindir}/sqfstar
%{_sbindir}/sqfscat

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 16 2023 Pavel Reichl <preichl@redhat.com> - 4.6.1-3
- Convert License tag to SPDX format

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 29 2023 Bruno Wolff III <bruno@wolff.to> - 4.6.1-1
- Phillip is now doing two tags per release and we can
- use the one that works better with forgemeta
- There are a few fixes after the 4.6 release. I think only
- one applies to Fedora because of the build options we use.
- It was not something that affects image builds.

* Fri Mar 17 2023 Bruno Wolff III <bruno@wolff.to> - 4.6-2
- Remove the dist prefix from the release

* Fri Mar 17 2023 Bruno Wolff III <bruno@wolff.to> - 4.6-1
- 4.6 release
- PR #231 was merged
- See https://github.com/plougher/squashfs-tools/blob/master/CHANGES

* Wed Mar 15 2023 Adam Williamson <awilliam@redhat.com> - 4.6-0.7.20230314git36abab0
- Backport PR #231 to fix a crash (#2178510)

* Tue Mar 14 2023 Bruno Wolff III <bruno@wolff.to> - 4.6-0.6^20230314git36abab0
- A few minor memory leaks were fixed

* Sun Mar 12 2023 Bruno Wolff III <bruno@wolff.to> - 4.6-0.5^20230312gitaaf011a
- Doc updates
- Probably the last version before the official release (tentatively tomorrow)

* Mon Mar 06 2023 Bruno Wolff III <bruno@wolff.to> - 4.6-0.4^20230306git1eaad6d
- Doc updates and unanchored search improvemebts

* Tue Feb 28 2023 Bruno Wolff III <bruno@wolff.to> - 4.6-0.3^20230228git746a81c
- Doc updates and minor bug fix

* Thu Feb 23 2023 Bruno Wolff III <bruno@wolff.to> - 4.6-0.2^20230323git7cf6cee
- Remove the -i and -v forgemeta flags to get rid of the extra noise

* Thu Feb 23 2023 Bruno Wolff III <bruno@wolff.to> - 4.6-0.1^20230323git7cf6cee
- Prerelease snapshot of 4.6

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - Packaging variables read or set by %forgemeta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - Packaging variables read or set by %forgemeta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Mar 19 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-1
- 4.5.1 release
- Up to date man pages
- Lots of little fixes

* Fri Mar 11 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-27.20220311git76624e1
- Continue testing upstream patches prior to 4.5.1 release.
- Minor fixes

* Thu Mar 10 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-26.20220310gitde61d0a
- Continue testing upstream patches prior to 4.5.1 release.
- Minor fixes
- Doc updates

* Tue Mar 08 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-25.20220308git2ac40ca
- Upstream fix for unsquashfs breakage from recent commit

* Tue Mar 08 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-24.20220308git8b6ee89
- Continue testing upstream patches prior to 4.5.1 release.
- Minor fixes
- Man page tweaks
- Tentative 4.5.1 change log

* Mon Mar 07 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-23.20220307git580b4e1
- Continue testing upstream patches prior to 4.5.1 release.
- Minor fixes

* Fri Mar 04 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-22.20220304git2baf12e
- Continue testing upstream patches prior to 4.5.1 release.
- Minor fixes

* Mon Feb 28 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-21.20220228git263a14e
- Continue testing upstream patches prior to 4.5.1 release.
- Man page improvement

* Fri Feb 25 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-20.20220225gitc883f32
- Continue testing upstream patches prior to 4.5.1 release.
- Man page improvement

* Wed Feb 23 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-19.20220223git2dfbcda
- Continue testing upstream patches prior to 4.5.1 release.
- Man page improvement

* Mon Feb 21 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-18.20220221gitbc0c097
- Continue testing upstream patches prior to 4.5.1 release.
- Some minor fixes.

* Fri Feb 18 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-17.20220218gitf3783bb
- Continue testing upstream patches prior to 4.5.1 release.
- Some minor fixes.

* Thu Feb 17 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-16.20220217git75951fb
- Continue testing upstream patches prior to 4.5.1 release.
- Some minor fixes.

* Tue Feb 15 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-15.20220215gitf491ad8
- Continue testing upstream patches prior to 4.5.1 release.
- Some minor fixes.

* Mon Feb 14 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-14.20220214gitde944c3
- Continue testing upstream patches prior to 4.5.1 release.
- Some minor fixes.

* Thu Feb 10 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-13.20220210gita8f61e2
- Continue testing upstream patches prior to 4.5.1 release.
- Some code cleanups for stuff noted by gcc.

* Thu Feb 10 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-12.20220210gite7e96fe
- Continue testing upstream patches prior to 4.5.1 release.
- Add man page for sqfscat.

* Wed Feb 09 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-11.20220209git0425d3d
- Continue testing upstream patches prior to 4.5.1 release.
- Add man page for sqfstar.

* Tue Feb 08 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-10.20220208git9e46a75
- Continue testing upstream patches prior to 4.5.1 release.
- Upstream man page for unsquashfs replaces out of date one froom Debian.

* Mon Feb 07 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-9.20220207gitbd186a7
- Continue testing upstream patches
- The deprecated lzma support options are improved in the man page

* Mon Feb 07 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-8.20220207git7f9203e
- Continue testing upstream patches
- Man pages are now built during the build process

* Fri Feb 04 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-7.20220204git8a9d02e
- Continue testing upstream patches
- A makefile for mksquashfs is now included

* Wed Feb 02 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-6.20220202git11c9591
- Continue testing upstream patches
- This includes help text changes

* Fri Jan 28 2022 Bruno Wolff III <bruno@wolff.to> - 4.5-5.20220128gitd5a583e
- Test a few changes before upstream tags a new point release

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - Packaging variables read or set by %forgemeta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 27 2021 Bruno Wolff III <bruno@wolff.to> - 4.5-4.20211227git5ae7238
- Get fixes for a few minor bugs

* Mon Sep 13 2021 Bruno Wolff III <bruno@wolff.to> - 4.5-3.20210913gite048580
- Fix bug 2003701 (additional write outside destination directory exploit)

* Mon Jul 26 2021 Bruno Wolff III <bruno@wolff.to> - 4.5-2
- Fix for sparse fragment bug 1985561

* Fri Jul 23 2021 Bruno Wolff III <bruno@wolff.to> - 4.5-1
- First crack at 4.5 release
- Man pages still need significant work

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4-5.git1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Nov 14 2020 Bruno Wolff III <bruno@wolff.to> - 4.4-4.git1
- Gating tests failed and unable to rerun them

* Wed Nov 11 2020 Bruno Wolff III <bruno@wolff.to> - 4.4-3.git1
- New upstream release with a minor fix

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 12 2020 Bruno Wolff III <bruno@wolff.to> - 4.4-1.20200513gitc570c61
- Go to 4.4 release + plus a few upstream post release patches

* Sat Feb 08 2020 Bruno Wolff III <bruno@wolff.to> - 4.3-25
- Fix duplicate definition flagged by gcc10

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Jeff Law <law@redhat.com> - 4.3-23
- Fix undefined symbol when building with LTO due to incorrect
  use of inline function

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Bruno Wolff III <bruno@wolff.to> - 4.3-21
- Add zstd compression support (Sean Purcell via github.com/plougher/squashfs-tools)

* Tue May 21 2019 Bruno Wolff III <bruno@wolff.to> - 4.3-20
- Fix issue with LDFLAGS not being set

* Tue May 21 2019 Bruno Wolff III <bruno@wolff.to> - 4.3-19
- Fix issue with glibc changes

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 23 2015 Bruno Wolff III <bruno@wolff.to> - 4.3-10
- Fix for CVE 2015-4645/4646

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Sep 13 2014 Bruno Wolff III <bruno@wolff.to> 4.3-8
- Fix for files >= 2gb rhbz #1141206

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Bruno Wolff III <bruno@wolff.to> 4.3-6
- Apply a couple of upstream patches.
- Fixes issue issue with too much memory use under PAE kernels

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bruno Wolff III <bruno@wolff.to> 4.3-4
- Even more man page fixes

* Wed May 14 2014 Bruno Wolff III <bruno@wolff.to> 4.3-3
- More mksquashfs man page fixes

* Tue May 13 2014 Bruno Wolff III <bruno@wolff.to> 4.3-2
- Add missed option to the mksquashfs man page

* Tue May 13 2014 Bruno Wolff III <bruno@wolff.to> 4.3-1
- Update to real 4.3 release
- Added support for lz4 since the stable snapshot
- Added support for alternate zlib compression strategies

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-0.19.gitaae0aff4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 22 2013 Bruno Wolff III <bruno@wolff.to> - 4.3-0.18.gitaae0aff4
- Latest pre 4.3 stable snapshot
- A few minor bug fixes
- Improvements in getting status info while running unsquashfs

* Tue Jun 04 2013 Bruno Wolff III <bruno@wolff.to> - 4.3-0.17.git5c6f0024
- Latest pre 4.3 snapshot
- Includes fix for mksquashfs hangs
- Switch to get pre-release updates from the stable branch at kernel.org

* Thu May 23 2013 Bruno Wolff III <bruno@wolff.to> - 4.3-0.16.git84d8ae5c
- Latest pre 4.3 snapshot
- Fix for a rare race condition

* Sun May 19 2013 Bruno Wolff III <bruno@wolff.to> - 4.3-0.15.git27d7c14b
- Latest pre 4.3 snapshot
- queue fragment and empty file buffers directly to main thread

* Wed May 15 2013 Bruno Wolff III <bruno@wolff.to> - 4.3-0.14.git8ce5585e
- Latest pre 4.3 snapshot
- Includes upstream bugfix introduced with the sequential queue change

* Sat May 11 2013 Bruno Wolff III <bruno@wolff.to> - 4.3-0.13.gitc2362556
- Latest pre 4.3 snapshot
- Sequential queue change

* Mon May 06 2013 Bruno Wolff III <bruno@wolff.to> - 4.3-0.12.git9353c998
- Latest pre 4.3 snapshot

* Sun Mar 31 2013 Bruno Wolff III <bruno@wolff.to> - 4.3-0.11.git8228a3e8
- Latest pre 4.3 snapshot
- SIGQUIT now displays the file being squashed

* Wed Mar 06 2013 Bruno Wolff III <bruno@wolff.to> - 4.3-0.10.git6a103792
- Latest pre 4.3 snapshot
- Pick up some more error handling improvements

* Sun Mar 03 2013 Kyle McMartin <kmcmarti@redhat.com>
- Move mksquashfs to /usr/sbin, as per UsrMove.

* Sun Mar 03 2013 Kyle McMartin <kmcmarti@redhat.com>
- Add mksquashfs.1 and unsquashfs.1 manpages from Debian.

* Mon Feb 18 2013 Bruno Wolff III <bruno@wolff.to> - 4.3-0.9.git3ec9c8f7
- Latest pre 4.3 snapshot
- Better error handling when space runs out

* Wed Feb 13 2013 Bruno Wolff III <bruno@wolff.to> - 4.3-0.8.gitca6a1c90
- Latest pre 4.3 snapshot
- New option to display compression options used
- Some error message improvements

* Fri Feb 01 2013 Bruno Wolff III <bruno@wolff.to> - 4.3-0.7.gitb10063a9
- Latest pre 4.3 snapshot
- More checks for bad data

* Sun Jan 13 2013 Bruno Wolff III <bruno@wolff.to> - 4.3-0.6.git6c0f229d
- Latest pre 4.3 snapshot
- Quote and backslash parsing for lexical analyzer

* Mon Dec 31 2012 Bruno Wolff III <bruno@wolff.to> - 4.3-0.5.gitc11af515
- Latest pre 4.3 snapshot
- A few memory leak fixes
- Additional checks for handling bad data

* Sun Dec 23 2012 Bruno Wolff III <bruno@wolff.to> - 4.3-0.4.git99a009c8
- Better checking of data in psuedo files

* Fri Dec 21 2012 Bruno Wolff III <bruno@wolff.to> - 4.3-0.3.git7ec6bd7a
- Better checking of data in sort, extract and exclude files

* Thu Dec 13 2012 Bruno Wolff III <bruno@wolff.to> - 4.3-0.2.git54719971
- Pick up a few more changes to better handle bad data

* Sat Dec 01 2012 Bruno Wolff III <bruno@wolff.to> - 4.3-0.1.git0be606be
- Pre-release of 4.3 to get early testing
- This update includes a bit of internal code infrastructure changes
- There are lots of fixes to better handle bad data
- The final release is expected sometime in December
- Until the release only the README doc file is available

* Sun Nov 25 2012 Bruno Wolff III <bruno@wolff.to> - 4.2-5
- Backported fix for bz 842460 (CVE-2012-4025)

* Thu Nov 22 2012 Bruno Wolff III <bruno@wolff.to> - 4.2-4
- Backported fix for bz 842458 (CVE-2012-4024)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 01 2011 Bruno Wolff III <bruno@wolff.to> - 4.2-1
- 4.2 is released.
- Bugfix for bad data causing crash.
- Include doc files added for release.
- Big endian patch is now upstream.
- Buildroot tag isn't needed any more.
- We can now specify CFLAGS on the make call.
- Compressor options are now passed with the make call.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2-0.4.20101231
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Dan Horák <dan[at]danny.cz> - 4.2-0.3.20101231
- Add fixes for big-endian machines

* Sat Jan 01 2011 Bruno Wolff III <bruno@wolff.to> - 4.2-0.2.20101231
- Pull latest upstream snapshot
- Includes check for matching compression type when adding to an existing image
- Sample cvs command now includes timezone and specifies when on the date to use for the snapshot

* Fri Dec 24 2010 Bruno Wolff III <bruno@wolff.to> - 4.2-0.1.20101223
- Switch to 4.2 development snapshot to get new XZ support
- LZMA and XZ (LZMA2) support are now different

* Wed Oct 27 2010 Bruno Wolff III <bruno@wolff.to> - 4.1-3
- Rebuild for xz soname bump

* Wed Sep 29 2010 jkeating - 4.1-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Bruno Wolff III <bruno@wolff.to> - 4.1-1
- Update to 4.1 final.
- Byte swap patch is now upstream.
- LZO compression type is now supported.

* Mon Sep 6 2010 Dan Horák <dan[at]danny.cz> - 4.1-0.5.20100827
- Add fixes for big-endian machines

* Sat Aug 28 2010 Bruno Wolff III <bruno@wolff.to> - 4.1-0.4.20100827
- Rebase to latest upstream.
- The main reason is to pick up a fix for large xattr similar to the large inode fix. This doesn't need to get backported as 4.0 doesn't have xattr support.
- An option was added to build without xattr support.
- Various source cleanups have been done as well.

* Tue Aug 03 2010 Bruno Wolff III <bruno@wolff.to> - 4.1-0.3.20100803
- Rebase to latest upstream
- Prevent warning message for xattr for virtual directory
- Fix issue with large inodes - BZ 619020

* Tue Jul 27 2010 Bruno Wolff III <bruno@wolff.to> - 4.1-0.2.20100727
- Rebase to latest upstream devel state. Mostly xattr fixes and cleanup.

* Tue Jun 08 2010 Bruno Wolff III <bruno@wolff.to> - 4.1-0.1.20100607
- Rebase to 4.1 prerelease with xz wrapper
- Provides lzma compression as an option.
- squashfs-fix-unsquashing-v3.patch is part of the 4.1 prerelease

* Wed May 5 2010 Kyle McMartin <kyle@redhat.com> 4.0-4
- squashfs-fix-unsquashing-v3.patch: pull in fix from cvs. Thanks pkl!
  (rhbz#523504)

* Thu Feb 18 2010 Kyle McMartin <kyle@redhat.com> 4.0-3
- Update to release tarball as opposed to cvs snapshot.
- Add dist tag.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 05 2009 Kyle McMartin <kyle@redhat.com> - 4.0-1
- Update to release 4.0

* Mon Mar 16 2009 Kyle McMartin <kyle@redhat.com> - 4.0-0.20090316
- update to cvs snap from 2009-03-16.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-0.20090126
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kyle McMartin <kyle@redhat.com> - 4.0-0.20090125
- update to cvs snap that should unbreak big endian machines creating
  little endian fs.

* Mon Jan 12 2009  <katzj@redhat.com> - 4.0-0.20090112
- update to cvs snap that generates v4.0 images

* Tue Sep 30 2008 Jeremy Katz <katzj@redhat.com> - 3.4-1
- update to 3.4

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.3-2
- Autorebuild for GCC 4.3

* Fri Dec 14 2007 Jeremy Katz <katzj@redhat.com> - 3.3-1
- Update to 3.3

* Wed Sep  5 2007 Jeremy Katz <katzj@redhat.com> - 3.2-2
- fixes from package review (#226430)

* Tue Mar 20 2007 Jeremy Katz <katzj@redhat.com> - 3.2-1
- update to 3.2r2

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 3.0-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Jeremy Katz <katzj@redhat.com> - 3.0-3
- updated fragment size patch (#204638)

* Wed Aug 16 2006 Jeremy Katz <katzj@redhat.com> - 3.0-2
- add upstream patch for fragment size problem (#202663)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.0-1.1
- rebuild

* Fri Jun 23 2006 Jeremy Katz <katzj@redhat.com> - 3.0-1
- update to 3.0
- include unsquashfs

* Tue May 16 2006 Jeremy Katz <katzj@redhat.com> 
- add BR on zlib-devel (Andreas Thienemann, #191880)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.2r2-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.2r2-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Jeremy Katz <katzj@redhat.com> - 2.2r2-1
- Initial build

