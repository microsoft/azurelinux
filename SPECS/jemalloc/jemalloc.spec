%define      debug_package %{nil}
Summary:        A General Purpose Malloc Implementation
Name:           jemalloc
Version:        5.3.0
Release:        1%{?dist}
# build-aux/config.guess is under GPLv3+
# build-aux/install-sh is under MIT
# msvc/test_threads/test_threads.cpp is under Public Domain
# m4/ax_cxx_compile_stdcxx.m4 is under FSFAP
License:        BSD AND GPLv3+ AND MIT AND Public Domain AND FSFAP
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            http://www.canonware.com/jemalloc/
Source0:        https://github.com/jemalloc/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2

%description
General-purpose scalable concurrent malloc(3) implementation that emphasizes
fragmentation avoidance and scalable concurrency support

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm %{buildroot}%{_docdir}/%{name}/jemalloc.html

find %{buildroot}%{_libdir}/ -name '*.a' -exec rm -vf {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libjemalloc.so.*
%{_bindir}/jemalloc.sh
%license COPYING
%doc README VERSION
%doc doc/jemalloc.html

%files devel
%{_includedir}/jemalloc
%{_bindir}/jemalloc-config
%{_libdir}/pkgconfig/jemalloc.pc
%{_bindir}/jeprof
%{_libdir}/libjemalloc.so
%{_mandir}/man3/jemalloc.3*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.3.0-1
- Auto-upgrade to 5.3.0 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 5.2.1-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.2.1-2
- Removing the explicit %%clean stage.

* Mon Dec 14 2020 Henry Li <lihl@microsoft.com> - 5.2.1-1
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- License verified.
	
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
	
 