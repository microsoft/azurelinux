# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global forgeurl https://github.com/jemalloc/jemalloc

Name:           jemalloc
Version:        5.3.0

Release:        13%{?dist}
Summary:        General-purpose scalable concurrent malloc implementation

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://jemalloc.net/
VCS:            git:%{forgeurl}
Source0:        %{forgeurl}/releases/download/%{version}/%{name}-%{version}.tar.bz2
Patch1:         jemalloc-5.3.0_fno-builtin.patch

BuildRequires:  gcc
BuildRequires:  /usr/bin/xsltproc
BuildRequires:  perl-generators
%ifarch %{valgrind_arches}
BuildRequires:  valgrind-devel
%endif
BuildRequires: make

%description
General-purpose scalable concurrent malloc(3) implementation.
This distribution is the stand-alone "portable" implementation of %{name}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup

# Override PAGESIZE, bz #1545539
%ifarch %ix86 %arm x86_64 s390x riscv64
%define lg_page --with-lg-page=12
%endif

%ifarch ppc64 ppc64le aarch64
%define lg_page --with-lg-page=16
%endif

# Disable thp on systems not supporting this for now
%ifarch %ix86 %arm aarch64 s390x
%define disable_thp --disable-thp
%endif


%build
%if 0%{?rhel} && 0%{?rhel} < 7
export LDFLAGS="%{?__global_ldflags} -lrt"
%endif

%if 0%{?fedora} > 41
export CFLAGS="$CFLAGS -std=gnu17"
%endif

echo "For debugging package builders"
echo "What is the pagesize?"
getconf PAGESIZE

echo "What mm features are available?"
ls /sys/kernel/mm
ls /sys/kernel/mm/transparent_hugepage || true
cat /sys/kernel/mm/transparent_hugepage/enabled || true

echo "What kernel version and config is this?"
uname -a

%configure %{?disable_thp} %{?lg_page} --enable-prof
make %{?_smp_mflags}


%check
make %{?_smp_mflags} check


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Install this with doc macro instead
rm %{buildroot}%{_datadir}/doc/%{name}/jemalloc.html

# None of these in fedora
find %{buildroot}%{_libdir}/ -name '*.a' -exec rm -vf {} ';'



%files
%{_libdir}/libjemalloc.so.*
%{_bindir}/jemalloc.sh
%doc COPYING README VERSION
%doc doc/jemalloc.html

%files devel
%{_includedir}/jemalloc
%{_bindir}/jemalloc-config
%{_libdir}/pkgconfig/jemalloc.pc
%{_bindir}/jeprof
%{_libdir}/libjemalloc.so
%{_mandir}/man3/jemalloc.3*

%ldconfig_scriptlets

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Mar 31 2025 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.3.0-12
- Support allocation profiling, i.e. build with --enable-prof flag

* Wed Mar 26 2025 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.3.0-11
- Added build fix from upstream for new gcc

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 25 2024 Petr Menšík <pemensik@redhat.com> - 5.3.0-9
- Correct actual project URL (rhbz#2188965)

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 5.3.0-8
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 09 2022 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.3.0-1
- New upstream release 5.3.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 06 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.2.1-1
- New upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 03 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.2.0-1
- New upstream release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 18 2018 Joe Orton <jorton@redhat.com> - 5.1.0-3
- move jemalloc.pc and jemalloc-config to -devel (#1593484)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 09 2018 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.1.0-1
- New upstream release
- Removed patches merged upstream

* Thu Mar 08 2018 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.0.1-5
- Actually, specify pagesizes according to arches, closes #1545539
- Remove patch disabling thp as this is now handled by configure, see
  upstream issue 526

* Tue Mar 06 2018 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.0.1-4
- Support different pagesizes, ie. build with --with-lg-page=16, closes #1545539

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.0.1-2
- Switch to %%ldconfig_scriptlets

* Wed Dec 13 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.0.1-1
- New upstream release
- Added patch for upstream issue #979 "Test suite segv on arm64"
- Moved jeprof util to jemalloc-devel, to give less dependencies
  on the library package, closes bz #1519586
- Respun the patch removing explicit altivec usage. Not all
  ppc64 have altive

* Wed Aug 16 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> - 4.5.0-4
- Rather use ifarch than checking builder kernel for thp support
- Cleanup; removed unnecessary patch for atomic ops on arm, pulled el5 support,
  use ix86 macro for ifarch i386 and friends

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 01 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> - 4.5.0-1
- New upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> - 4.4.0-2
- Disable transparent hugepages on systems not supporting them

* Fri Dec 09 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> - 4.4.0-1
- New upstream release

* Wed Nov 09 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> - 4.3.1-1
- New upstream release
- Removed patches from upstream that are merged

* Tue Nov 01 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> - 4.2.1-2
- Fixes for upstream bug #392. Package will now build on el5/ppc,
  el5/i386 and el6/i386

* Tue Aug 23 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> - 4.2.1-1
- New upstream release

* Thu Aug 11 2016 Michal Toman <mtoman@fedoraproject.org> - 4.1.1-2
- No valgrind on MIPS (#1366685)

* Wed May 04 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> - 4.1.1-1
- New upstream release

* Mon Feb 29 2016 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 4.1.0-1
- Update to 4.1.0 (#1312699)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Oct 24 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> - 4.0.4-1
- New upstream release

* Fri Sep 25 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> - 4.0.3-1
- New upstream release
- Removed oom test patch, it has been fixed upstream

* Thu Sep 24 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> - 4.0.2-2
- oom test also fails on 32bit ppc, so patch it out there as well

* Tue Sep 22 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> - 4.0.2-1
- New upstream release
- Added a patch removing a non-critical test that fails on i386
- Removed now included negative bitshift patch.

* Wed Aug 19 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> - 4.0.0-1
- New upstream release
- Removed the no-pprof patch, as jemalloc now comes with its own prof variant
- Removed atomic.h patch for armv5tel. jemalloc now provides a specific
  variant for armv5tel
- Added a patch from upstream for errnous bitshift by negative amounts on pagesize >8KiB
- Added -lrt to LDFLAGS for rhel<7

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.6.0-8
- valgrind-devel is not available on s390, closes #1131014

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.6.0-6
- bz #1106933 fix only for fedora 21 and above

* Fri Aug 15 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.6.0-5
- Added valgrind-devel to BuildRequires, fixing bz #974270

* Fri Aug 15 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.6.0-4
- Added an i686 build fixing bz #1106933

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 01 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.6.0-2
- Patch that removes explicit altivec on el5/ppc

* Mon Mar 31 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.6.0-1
- New upstream release. This release fixes a critical regression 

* Fri Mar 28 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.5.1-1
- New upstream release
- Updated nopprof patch to match new release
- Fixed a few bogus changelog entries

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.4.0-1
- New upstream release

* Mon Mar 11 2013 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.3.1-1
- New upstream release
- Dropped s390 patch, it's in upstream now.

* Fri Jan 25 2013 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.3.0-1
- New upstream release
 
* Mon Nov 19 2012 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.2.0-1
- New upstream release
 
* Tue Oct 23 2012 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.1.0-1
- New upstream release
- Removed ptmalloc_lock_all patch, it is merged upstream

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.0.0-2
- Added a patch from upstream, fixing a crash in ptmalloc_lock_all,
  closing #824646

* Mon May 14 2012 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.0.0-1
- New upstream release
- Updated no_pprof patch to match new release
- Updated s390 patch to match new relase
- Added make check
- Added new script jemalloc.sh
- Added a patch for atomic operations on epel5/ppc

* Sat Apr 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.2.5-5
- Improve ARM patch

* Fri Apr 20 2012 Dennis Gilmore <dennis@ausil.us> - 2.2.5-4
- no attomics on armv5tel

* Wed Feb 08 2012 Dan Horák <dan[at]danny.cz> - 2.2.5-3
- substitute version information in the header (#788517)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 06 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.2.5-1
- New upstream release, closes #75618

* Sun Nov 06 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.2.4-1
- New upstream release

* Thu Oct 13 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.2.3-1
- New upstream release, closes #735057

* Mon Aug 01 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.2.2-1
- New upstream release, closes #727103
- Updated no_pprof patch for 2.2.2

* Thu Mar 31 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.2.1-1
- New upstream release

* Sun Mar 27 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.2.0-1
- New upstream release
- Updated no_pprof patch for 2.2.0

* Tue Mar 15 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.3-2
- New upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.1-1
- New upstream release

* Wed Jan 05 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.0-1
- New upstream release
- Updated patch to remove pprof
- Added html doc and xsltproc as a requirement to build it

* Sat Dec 11 2010 Dan Horák <dan[at]danny.cz> - 2.0.1-3
- fix build on s390

* Thu Nov 18 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.0.1-2
- Added a patch that removes pprof, as it already exists in the
  google-perftools package
- Cosmetic fixes as requested in the package review (rhbz#653682)

* Mon Nov 15 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.0.1-1
- First cut of an rpm distribution of jemalloc
