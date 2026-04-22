# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: A utility which lists open files on a Linux/UNIX system
Name: lsof
Version: 4.98.0
Release: 9%{?dist}
License: lsof
URL: https://github.com/lsof-org/lsof

# lsof contains licensed code that we cannot ship.  Therefore we use
# upstream2downstream.sh script to remove the code before shipping it.
#
# The script can be found in SCM or downloaded from:
# http://pkgs.fedoraproject.org/cgit/lsof.git/tree/upstream2downstream.sh

%global lsofrh lsof-%{version}-rh
Source0: %{lsofrh}.tar.xz
Source1: upstream2downstream.sh

# BZ#1260300 - move lsof man page to section 1
Patch0: lsof-man-page-section.patch
Patch1: f42-ftbfs.patch

BuildRequires: gcc
BuildRequires: libselinux-devel
BuildRequires: libtirpc-devel
BuildRequires: groff-base
BuildRequires: make
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: git

%description
Lsof stands for LiSt Open Files, and it does just that: it lists information
about files that are open by the processes running on a UNIX system.

%prep
%autosetup -n %{lsofrh} -S git

%build
%configure
%make_build DEBUG="%{build_cflags} -I/usr/include/tirpc" CFGL="%{build_ldflags} -L./lib -llsof -lselinux -ltirpc"
# rebase to 4.93 introduced change in Lsof.8 with unhandled .so inclusion
soelim -r Lsof.8 > lsof.1

%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
install -p -m 0755 lsof ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
install -p -m 0644 lsof.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/lsof.1

%files
%doc 00README 00CREDITS 00FAQ 00LSOF-L 00QUICKSTART
%{_bindir}/lsof
%{_mandir}/man*/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.98.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 24 2025 Jan Rybar <jrybar@redhat.com> - 4.98.0-7
- FTBFS: stricter check, incompatible types

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.98.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.98.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.98.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.98.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 23 2023 Jan Rybar <jrybar@redhat.com> - 4.98.0-2
- version bump due to licence fix

* Fri Oct 20 2023 Jan Rybar <jrybar@redhat.com> - 4.98.0-1
- rebase to lsof-4.98

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.96.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.96.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 21 2022 Florian Weimer <fweimer@redhat.com> - 4.96.3-2
- Fix C89isms in Configure

* Tue Sep 20 2022 Jan Rybar <jrybar@redhat.com> - 4.96.3-1
- rebase to 4.96.3

* Fri Sep 02 2022 Jan Rybar <jrybar@redhat.com> - 4.95.0-1
- rebase to 4.95.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.94.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.94.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.94.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Jan Rybar <jrybar@redhat.com> - 4.94.0-1
- Rebase to 4.94.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.93.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.93.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.93.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.93.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 28 2019 Jan Rybar <jrybar@redhat.com> - 4.93.2-1
- Rebase to lsof-4.93.2
- Upstream moved to GitHub and tarball structure changed
- Manpage patch needed to reflect the tarball changes

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 22 2018 Peter Schiffer <pschiffe@redhat.com> - 4.91-1
- resolves: #1560993
  updated to 4.91
- resolves: #1574669
  use tirpc library for rpc

* Fri Apr 13 2018 Rafael dos Santos <rdossant@redhat.com> - 4.90-2
- Use standard Fedora build flags (bug #1548552)

* Wed Feb 21 2018 Peter Schiffer <pschiffe@redhat.com> - 4.90-1
- resolves: #1545963
  updated to 4.90

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.89-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.89-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.89-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.89-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Mar  5 2016 Peter Robinson <pbrobinson@fedoraproject.org> 4.89-4
- Only ship end user useful docs, don't ship bits for building

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.89-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 30 2015 Peter Schiffer <pschiffe@redhat.com> - 4.89-2
- resolves #1260300
  moved lsof to /usr/bin, it's not sysadmin only utility

* Wed Jul 29 2015 Peter Schiffer <pschiffe@redhat.com> - 4.89-1
-  updated to 4.89

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.88-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan  6 2015 Peter Schiffer <pschiffe@redhat.com> - 4.88-2
-  added upstream patch fixing unwanted pipe file output
-  cleaned .spec file

* Wed Oct 15 2014 Peter Schiffer <pschiffe@redhat.com> - 4.88-1
-  updated to 4.88

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.87-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.87-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.87-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.87-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan  3 2013 Peter Schiffer <pschiffe@redhat.com> - 4.87-1
- resolves: #891508
  updated to 4.87

* Tue Aug 28 2012 Peter Schiffer <pschiffe@redhat.com> - 4.86-4
- .spec file cleanup

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.86-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 04 2012 Peter Schiffer <pschiffe@redhat.com> - 4.86-2
- added support for files on anon_inodefs

* Fri Apr 20 2012 Peter Schiffer <pschiffe@redhat.com> - 4.86-1
- resolves: #811520
  update to 4.86

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.85-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 30 2011 Peter Schiffer <pschiffe@redhat.com> - 4.85-1
- resolves: #741882
  update to 4.85

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.84-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Ville SkyttÃ¤ <ville.skytta@iki.fi> - 4.84-3
- Fix man page permissions.

* Wed Sep 29 2010 jkeating - 4.84-2
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Karel Zak <kzak@redhat.com> 4.84-1
- upgrade to 4.84
- remove lsof_4.81-threads.patch, "lsof -K" provides basic support for tasks now

* Fri Feb 19 2010 Karel Zak <kzak@redhat.com> 4.83-2
- minor changes in spec file (#226108 - Merge Review)

* Thu Feb 11 2010 Karel Zak <kzak@redhat.com> 4.83-1
- upgrade to 4.83 (see the 00DIST file for list of changes)
- remove lsof_4.83A-selinux-typo.patch (fixed upstream)

* Mon Jul 27 2009 Karel Zak <kzak@redhat.com> 4.82-1
- upgrade to 4.82 (see the 00DIST file for list of changes)
- backport an upstream patch from 4.83A-linux
- remove lsof_4.81-man.patch (fixed upstream)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.81-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.81-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Karel Zak <kzak@redhat.com> 4.81-2
- fix #480694 - lsof manpage mismarked and formats badly

* Tue Dec  2 2008 Karel Zak <kzak@redhat.com> 4.81-1
- upgrade to 4.81
  - lsof_4.80-threads.patch - rebased

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.80-2
- fix license tag

* Tue May 20 2008 Karel Zak <kzak@redhat.com> 4.80-1
- upgrade to 4.80
  - lsof_4.78C-inode.patch - merged upstream
  - lsof_4.78C-selinux.patch - merged upstream
  - lsof_4.78C-threads.patch - rebased

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.78-8
- Autorebuild for GCC 4.3

* Wed Oct  3 2007 Karel Zak <kzak@redhat.com> 4.78-7
- update selinux and inode patches (new versions are based on upstream)

* Tue Oct  2 2007 Karel Zak <kzak@redhat.com> 4.78-6
- fix #280651 - lsof prints entries in multiple lines when SElinux is disabled
- fix #243976 - mmap'd files with large inode numbers confuse lsof

* Thu Mar  1 2007 Karel Zak <kzak@redhat.com> 4.78-5
- fix License

* Thu Mar  1 2007 Karel Zak <kzak@redhat.com> 4.78-4
- fix #226108 - Merge Review: lsof

* Thu Aug 10 2006 Karel Zak <kzak@redhat.com> 4.78-3
- minor changes to thread patch

* Wed Aug  9 2006 Karel Zak <kzak@redhat.com> 4.78-2
- fix #184338 - allow lsof access nptl threads

* Wed Jul 19 2006 Karel Zak <kzak@redhat.com> 4.78-1
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.78-06122006devel.1.1
- rebuild

* Mon Jun 12 2006 Karel Zak <kzak@redhat.com> 4.78-06122006devel.1
- upgrade to 4.78C (last bugfix accepted by upstream)

* Mon Jun 12 2006 Karel Zak <kzak@redhat.com> 4.78-06052006devel.2
- added BuildRequires libselinux-devel
- fix #194864 - lsof segfaults on starting

* Wed May 24 2006 Karel Zak <kzak@redhat.com> 4.78-06052006devel.1
- upgrade to 4.78B (upstream devel version with selinux patch)

* Wed Feb 15 2006 Karel Zak <kzak@redhat.com> 4.76-2
- fix #175568 - lsof prints 'unknown inode type' for epoll

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.76-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.76-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Sep 19 2005 Karel Zak <kzak@redhat.com> 4.76-1
- new upstream version

* Tue May 10 2005 Karel Zak <kzak@redhat.com> 4.74-7
- fix debuginfo

* Wed Mar 23 2005 Karel Zak <kzak@redhat.com> 4.74-6
- fix "lsof -b" hangs if a process is stuck in disk-wait/NFS (#131712)

* Mon Mar 14 2005 Karel Zak <kzak@redhat.com> 4.74-5
- src.rpm cleanup

* Sat Mar  5 2005 Karel Zak <kzak@redhat.com> 4.74-3
- rebuilt

* Tue Feb  8 2005 Karel Zak <kzak@redhat.com> 4.74-2
- replace 'Copyright' with 'License' in .spec

* Tue Feb  8 2005 Karel Zak <kzak@redhat.com> 4.74-1
- sync with upstream 4.74

* Mon Dec 13 2004 Karel Zak <kzak@redhat.com> 4.73-1
- update to 4.73
- remove lsof_4.72-sock.patch, already in the upstream code

