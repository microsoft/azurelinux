Summary:        A library which provides easy access to huge pages of memory
Name:           libhugetlbfs
Version:        2.23
Release:        5%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/libhugetlbfs/libhugetlbfs
Source0:        https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
# Patch0: build flags adjusts to build in stricter RHEL-8 buildroots
Patch0:         0000-build_flags.patch
# Downstream patch testcases to avoid bogus annoying failures
# RHBZ#1611780 && RHBZ#1611782
Patch1:         0001-testutils-fix-range_is_mapped.patch
Patch2:         0002-stack_grow_into_huge-don-t-clobber-existing-mappings.patch
# RHBZ#1628794 undersized SHMMAX when running on aarch64
# https://github.com/libhugetlbfs/libhugetlbfs/issues/39
Patch3:         0003-tests_shm-perms_adjust_max_segment_size_for_bigger_hugepages.patch
# Downstream patches to remove an IA-64 target leftover that breaks the
# tests install and fix run_tests.py path for hugeadm tool call
Patch4:         0004-tests-makefile-fix.patch
Patch5:         0005-tests-run_tests-fix-hugeadm-path.patch
# Fixes for downstream COVSCAN and RPMDiff execshield complaints:
Patch6:         0007-tests-fix-covscan-SHELLCHECK_WARNING-complaints.patch
Patch7:         0008-tests-include-missing-LDFLAGS-to-make-targets.patch
# __morecore feature has been removed from glibc 2.34+ so disable it
Patch8:         0009-Disable-hugepage-backed-malloc-if-__morecore-is-not-.patch
Patch9:         0010-only-link-libhugetlbfs-statically.patch
%global _hardened_build 1
%define ldscriptdir %{_datadir}/%{name}/ldscripts
BuildRequires:  execstack
BuildRequires:  glibc-devel
BuildRequires:  python3-devel
BuildRequires:  which

%description
libhugetlbfs is a library which provides easy access to huge pages of memory.
It is a wrapper for the hugetlbfs file system. Applications can use huge pages
to fulfill malloc() requests without being recompiled by using LD_PRELOAD.
Alternatively, applications can be linked against libhugetlbfs without source
modifications to load BSS or BSS, data, and text segments into large pages.

%package devel
Summary:        Header files for libhugetlbfs
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Contains header files for building with libhugetlbfs.

%package utils
Summary:        Userspace utilities for configuring the hugepage environment
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}
Requires:       perl
Requires:       python3

%description utils
This packages contains a number of utilities that will help administrate the
use of huge pages on your system.  hugeedit modifies binaries to set default
segment remapping behavior. hugectl sets environment variables for using huge
pages and then execs the target program. hugeadm gives easy access to huge page
pool size control. pagesize lists page sizes available on the machine.

%package tests
Summary:        Test cases to help on validating the library environment
Group:          Development/Libraries
Requires:       %{name}-utils = %{version}-%{release}

%description tests
This packages contains a number of testcases that will help developers
to verify the libhugetlbfs functionality and validate the library.

%prep
%autosetup -p1

%build
%make_build all BUILDTYPE=NATIVEONLY V=1

%install
make install PREFIX=%{_prefix} LIB64="%{_lib}" DESTDIR=%{buildroot} LDSCRIPTDIR=%{ldscriptdir} BUILDTYPE=NATIVEONLY
make install-helper PREFIX=%{_prefix} LIB64="%{_lib}" DESTDIR=%{buildroot} LDSCRIPTDIR=%{ldscriptdir} BUILDTYPE=NATIVEONLY
make install-tests PREFIX=%{_prefix} LIB64="%{_lib}" DESTDIR=%{buildroot} LDSCRIPTDIR=%{ldscriptdir} BUILDTYPE=NATIVEONLY

# clear execstack flag
execstack --clear-execstack %{buildroot}/%{_libdir}/libhugetlbfs.so
execstack --clear-execstack %{buildroot}/%{_libdir}/libhugetlbfs_privutils.so

# remove statically built libraries:
rm -f %{buildroot}/%{_libdir}/*.a
# remove unused sbin directory
rm -fr %{buildroot}/%{_sbindir}/

%ldconfig_scriptlets

%files
%{_libdir}/libhugetlbfs.so*
%{_libdir}/libhugetlbfs_privutils.so*
%{_datadir}/%{name}/
%{_mandir}/man7/libhugetlbfs.7.gz
%ghost %config(noreplace) %{_sysconfdir}/security/limits.d/hugepages.conf
%doc README HOWTO NEWS
%license LGPL-2.1

%files devel
%{_includedir}/hugetlbfs.h
%{_mandir}/man3/getpagesizes.3.gz
%{_mandir}/man3/free_huge_pages.3.gz
%{_mandir}/man3/get_huge_pages.3.gz
%{_mandir}/man3/gethugepagesize.3.gz
%{_mandir}/man3/gethugepagesizes.3.gz
%{_mandir}/man3/free_hugepage_region.3.gz
%{_mandir}/man3/get_hugepage_region.3.gz
%{_mandir}/man3/hugetlbfs_find_path.3.gz
%{_mandir}/man3/hugetlbfs_find_path_for_size.3.gz
%{_mandir}/man3/hugetlbfs_test_path.3.gz
%{_mandir}/man3/hugetlbfs_unlinked_fd.3.gz
%{_mandir}/man3/hugetlbfs_unlinked_fd_for_size.3.gz

%files utils
%{_bindir}/hugeedit
%{_bindir}/hugeadm
%{_bindir}/hugectl
%{_bindir}/pagesize
%{_bindir}/huge_page_setup_helper.py
%{_mandir}/man8/hugeedit.8.gz
%{_mandir}/man8/hugectl.8.gz
%{_mandir}/man8/hugeadm.8.gz
%{_mandir}/man1/pagesize.1.gz
%{_mandir}/man1/ld.hugetlbfs.1.gz

%files tests
%{_libdir}/libhugetlbfs

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.23-5
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Oct 05 2022 Andy Caldwell <andycaldwell@microsoft.com> - 2.23.4
- Allow building without `glibc-static`

* Tue Jul 26 2022 Sriram Nambakam <snambakam@microsoft.com> - 2.23-3
- Remove patch that applies usage of python3

* Fri Feb 18 2022 Vince Perri <viperri@microsoft.com> - 2.23-2
- Initial CBL-Mariner import from Fedora 35 (license: MIT).
- Verified license
- Added patch that disables memcore feature to support glibc-2.34

* Mon Mar 15 2021 Hernan Gatta <hegatta@microsoft.com> - 2.23-1
- Initial import into ECF Mariner (License: LGPLv2+)

* Tue May 26 2020 Rafael Aquini <aquini@redhat.com> - 2.21-17
- hugeadm: "ERROR: Invalid group specification" fix (1832243)

* Mon Apr 13 2020 Rafael Aquini <aquini@redhat.com> - 2.21-16
- libhugetlbfs-tests: harden the testcases to satisfy EXECSHIELD RPMDiff checks (1785296)

* Thu Apr  9 2020 Rafael Aquini <aquini@redhat.com> - 2.21-14
- Follow up fix for harden the testcases (1785296)

* Thu Apr  9 2020 Rafael Aquini <aquini@redhat.com> - 2.21-13
- Fix: huge_page_setup_helper.py: SyntaxError: Missing parentheses in call to 'print' (1821938)
- libhugetlbfs-tests: harden the testcases to satisfy EXECSHIELD RPMDiff checks (1785296)

* Tue Oct 29 2019 Rafael Aquini <aquini@redhat.com> - 2.21-12
- Fix: Introduce libhugetlbfs-tests subpkg for CI tests (1688930)
- trim repetitive changelogs for interim debug builds

* Mon Oct 28 2019 Rafael Aquini <aquini@redhat.com> - 2.21-4
- Fix: task-size-overrun hung over 8 hours on ppc64le (1737370)
- Introduce libhugetlbfs-tests subpkg for CI tests (1688930)

* Tue Apr  2 2019 Rafael Aquini <aquini@redhat.com> - 2.21-3
- Fix: Adding CI gating basic infrastructure (1680621)

* Mon Apr  1 2019 Rafael Aquini <aquini@redhat.com> - 2.21-2
- Adding CI gating basic infrastructure (1680621)

* Wed Oct  3 2018 Rafael Aquini <aquini@redhat.com> - 2.21-1
- Fix small_const/small_data is not hugepage test failures (1628794)

* Tue Sep 11 2018 Rafael Aquini <aquini@redhat.com> - 2.20-12
- Finish up Python3 conversion fo tests/run_tests.py (1620250)

* Mon Sep 10 2018 Rafael Aquini <aquini@redhat.com> - 2.20-11
- Fix up rpmdiff execshield flag failures (1627532)

* Tue Sep 04 2018 Rafael Aquini <aquini@redhat.com> - 2.20-10
- Fix up annocheck distro flag failures (1624131)
- Convert libhugetlbfs run_tests.py to Python3 (1620250)

* Thu Aug 02 2018 Rafael Aquini <aquini@redhat.com> - 2.20-9
- Fix up libhugetlbfs testcase problems (1611780 1611782)

* Wed Aug 01 2018 Charalampos Stratakis <cstratak@redhat.com> - 2.20-8
- Fix python shebangs

* Thu Jul 05 2018 Rafael Aquini <aquini@redhat.com> - 2.20-7
- Remove python2 dependency for RHEL8 mass rebuilds (1561516 1580761)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 03 2015 Eric B Munson <emunson@mgebm.net> - 2.20-1
- Update to 2.20 upstream

* Wed Jul 01 2015 Eric B Munson <emunson@mgebm.net> - 2.19-1
- Update to 2.19 upstream

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 07 2014 Eric B Munson <emunson@mgebm.net> - 2.18-2
- Remove unnecessary ppc makefile patch

* Sun Apr 06 2014 Eric B Munson <emunson@mgebm.net> - 2.18-1
- Update to 2.18 upstream

* Sat Mar 15 2014 Eric B Munson <emunson@mgebm.net> - 2.12-2
- Add Patch to support building on ppc64le

* Wed Jan 29 2014 Kyle McMartin <kyle@fedoraproject.org> - 2.17-1
- Update for upstream 2.17 release (adds AArch64 support)
- update libhugetlbfs-2.16-s390.patch for 2.17 changes to Makefile
- add libhugetlbfs-2.17-ppc.patch to fix powerpc{,64}

* Thu Jul 25 2013 Dan Horák <dan[at]danny.cz> - 2.16-2
- Fix build on s390/s390x (patch by aarapov@rh.c)
- Use Fedora CFLAGS for build

* Mon Apr 29 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.16-1
- Upstream 2.16 release (adds ARM support)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 08 2012 Eric B Munson <emunson@mgebm.net> - 2.15
- Update for upstream 2.15 release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 24 2012 Eric B Munson <emunson@mgebm.net>
- Update for upstream 2.13 release

* Wed Jul 20 2011 Eric B Munson <emunson@mgebm.net>
- Update for upstream 2.12 release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Apr 05 2010 Eric B Munson <ebmunson@us.ibm.com> 2.8-1
- Update for upstream 2.8 release

* Wed Feb 10 2010 Eric B Munson <ebmunson@us.ibm.com> 2.7-2
- Include patch that fixes build on ppc

* Tue Jan 05 2010 Eric B Munson <ebmunson@us.ibm.com> 2.7-1
- Update for upstream 2.7 release

* Fri Oct 02 2009 Jarod Wilson <jarod@redhat.com> 2.6-3
- Add hopefully-about-to-be-merged-upstream hugeadm enhancements
- Add huge pages setup helper script, using new hugeadm enhancements

* Thu Sep 03 2009 Nils Philippsen <nils@redhat.com> 2.6-2
- fix building on s390x

* Mon Aug 31 2009 Eric Munson <ebmunson@us.ibm.com> 2.6-1
- Updating for the libhugetlbfs-2.6 release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Eric Munson <ebmunson@us.ibm.com> 2.5-2
- Update Group for -utils package to Applications/System

* Tue Jun 30 2009 Eric Munson <ebmunson@us.ibm.com> 2.5-1
- Updating for the libhugetlbfs-2.5 release

* Tue Jun 02 2009 Eric Munson <ebmunson@us.ibm.com> 2.4-2
- Adding patch to remove S390 32 bit build

* Fri May 29 2009 Eric Munson <ebmunson@us.ibm.com> 2.4-1
- Updating for the libhugetlbfs-2.4 release

* Wed Apr 15 2009 Eric Munson <ebmunson@us.ibm.com> 2.3-1
- Updating for the libhugetlbfs-2.3 release

* Wed Feb 11 2009 Eric Munson <ebmunson@us.ibm.com> 2.2-1
- Updating for the libhugetlbfs-2.2 release

* Fri Dec 19 2008 Eric Munson <ebmunson@us.ibm.com> 2.1.2-1
- Updating for libhugetlbfs-2.1.2 release

* Fri Dec 19 2008 Eric Munson <ebmunson@us.ibm.com> 2.1.1-1
- Updating for libhugetlbfs-2.1.1 release

* Thu Dec 18 2008 Josh Boyer <jwboyer@gmail.com> 2.1-2
- Fix broken dependency caused by just dropping -test
  subpackage

* Thu Oct 16 2008 Eric Munson <ebmunson@us.ibm.com> 2.1-1
- Updating for libhuge-2.1 release
- Adding -devel and -utils subpackages for various utilities
  and devel files.

* Wed May 14 2008 Eric Munson <ebmunson@us.ibm.com> 1.3-1
- Updating for libhuge-1.3 release

* Tue Mar 25 2008 Eric Munson <ebmunson@us.ibm.com> 1.2-1
- Removing test rpm target, and excluding test files

* Mon Mar 26 2007 Steve Fox <drfickle@k-lug.org> - 1.1-1
- New release (1.1)
- Fix directory ownership

* Wed Aug 30 2006 Steve Fox <drfickle@k-lug.org> - 0.20060825-1
- New release (1.0-preview4)
- patch0 (Makefile-ldscript.diff) merged upstream

* Tue Jul 25 2006 Steve Fox <drfickle@k-lug.org> - 0.20060706-4
- Bump for build system

* Tue Jul 25 2006 Steve Fox <drfickle@k-lug.org> - 0.20060706-3
- Don't use parallel build as it has random failures

* Thu Jul 20 2006 Steve Fox <drfickle@k-lug.org> - 0.20060706-2
- Fix the Makefile so that the ld.hugetlbfs script doesn't store the
  DESTDIR in the path to the ldscripts dir

* Fri Jul 7 2006 Steve Fox <drfickle@k-lug.org> - 0.20060706-1
- New release which includes a fix for the syscall macro removal in the
  Rawhide kernels

* Thu Jun 29 2006 Steve Fox <drfickle@k-lug.org> - 0.20060628-1
- First Fedora package
