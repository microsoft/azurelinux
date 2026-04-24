# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# The testsuite does not pass on all targets.
#
# aarch64
#     Gtest-exc
#     Ltest-exc
#     Gtest-trace
#     Ltest-trace
#     Ltest-init-local-signal
#     Ltest-mem-validate: https://github.com/libunwind/libunwind/issues/388
#     test-reg-state
#     Ltest-varargs
#     Lrs-race
#     test-ptrace
#     run-check-namespace: https://github.com/libunwind/libunwind/issues/389
#     run-ptrace-mapper
#     run-ptrace-misc
# i686
#     Ltest-mem-validate: https://github.com/libunwind/libunwind/issues/391
#     test-async-sig
#     test-ptrace
# ppc64le
#     Gtest-exc
#     Ltest-exc
#     Gtest-resume-sig
#     Ltest-resume-sig
#     Gtest-resume-sig-rt
#     Ltest-resume-sig-rt
#     test-ptrace
#     run-check-namespace
#     run-ptrace-mapper
#     run-ptrace-misc
#
# s390x
#     Gtest-resume-sig-rt
#     Ltest-resume-sig-rt
#     test-ptrace

%ifarch i686 ppc64le s390x
%global test_failure_override true
%else
%global test_failure_override false
%endif

# %%global prerel rc2

Summary: An unwinding library
Name: libunwind
Version: 1.8.1
Release: 4%{?dist}
License: MIT
URL: http://savannah.nongnu.org/projects/libunwind
Source: https://github.com/libunwind/libunwind/releases/download/v%{version}/%{name}-%{version}.tar.gz

#Fedora specific patch
Patch1: libunwind-arm-default-to-exidx.patch
# Make libunwind.h multilib friendly
Patch2: libunwind-1.3.1-multilib-fix.patch
Patch5: libunwind-no-dl-iterate-phdr.patch
# Fix C23 issue
Patch6: https://github.com/libunwind/libunwind/commit/457612f470f8c0e718cdf7f14ef1ecb583f3b3a6.patch

ExclusiveArch: %{arm} aarch64 hppa ia64 mips ppc %{power64} s390x %{ix86} x86_64 riscv64

BuildRequires: automake libtool autoconf texlive-latex2man
BuildRequires: make
BuildRequires: gcc-c++

# host != target would cause REMOTE_ONLY build even if building i386 on x86_64.
%global _host %{_target_platform}

%description
Libunwind provides a C ABI to determine the call-chain of a program.

%package devel
Summary: Development package for libunwind
Requires: libunwind%{_isa} = %{version}-%{release}

%description devel
The libunwind-devel package includes the libraries and header files for
libunwind.

%package tests
Summary: Test binaries for libunwind
Requires: libunwind%{_isa} = %{version}-%{release}

%description tests
Test executables for libunwind. Not needed for library functionality.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%ifarch aarch64
# LTO causes FTBFS on aarch64 (rhbz#2261344)
%global _lto_cflags %{nil}
%endif

%global optflags %{optflags} -fcommon
aclocal
libtoolize --force
autoheader
automake --add-missing
autoconf
%configure --enable-static --enable-shared --enable-setjmp=no
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# /usr/include/libunwind-ptrace.h
# [...] aren't really part of the libunwind API.  They are implemented in
# a archive library called libunwind-ptrace.a.
mv -f $RPM_BUILD_ROOT%{_libdir}/libunwind-ptrace.a $RPM_BUILD_ROOT%{_libdir}/libunwind-ptrace.a-save
rm -f $RPM_BUILD_ROOT%{_libdir}/libunwind*.a
mv -f $RPM_BUILD_ROOT%{_libdir}/libunwind-ptrace.a-save $RPM_BUILD_ROOT%{_libdir}/libunwind-ptrace.a

# The tests want this one.
# rm -f $RPM_BUILD_ROOT%{_libdir}/libunwind-ptrace*.so*

# fix multilib conflicts
touch -r NEWS $RPM_BUILD_ROOT%{_includedir}/libunwind.h

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

echo ====================TESTING=========================
if ! make check ; then
    echo ====================FAILED TESTS=====================
    cat tests/test-suite.log || true
    %{test_failure_override}
fi
echo ====================TESTING END=====================

%ldconfig_scriptlets

%files
%license COPYING
%doc README NEWS
%{_libdir}/libunwind*.so.*

%files devel
%{_libdir}/libunwind*.so
%{_libdir}/libunwind-ptrace.a
%{_libdir}/pkgconfig/libunwind*.pc
%{_mandir}/*/*
# <unwind.h> does not get installed for REMOTE_ONLY targets - check it.
%{_includedir}/unwind.h
%{_includedir}/libunwind*.h

%files tests
%{_libexecdir}/libunwind

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Feb 13 2025 Tom Callaway <spot@fedoraproject.org> - 1.8.1-2
- package libunwind-ptrace.so.0 for the tests
- apply upstream fix for C23 issue

* Mon Feb 10 2025 Tom Callaway <spot@fedoraproject.org> - 1.8.1-1
- update to 1.8.1
- tighten requires to _isa
- add tests subpackage
- use -std=c17 because of Gtest-nomalloc.c

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 12 2024 Songsong Zhang <U2FsdGVkX1@gmail.com> - 1.8.0-5
- Fix test failure in riscv64

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 06 2024 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-3
- Bump and rebuild package (for riscv64)

* Thu Feb 08 2024 Kalev Lember <klember@redhat.com> - 1.8.0-2
- Disable LTO on aarch64 to fix the build (rhbz#2261344)
- Re-enable tests on aarch64

* Mon Jan 29 2024 Tom Callaway <spot@fedoraproject.org> - 1.8.0-1
- update to 1.8.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug  9 2023 Tom Callaway <spot@fedoraproject.org> - 1.7.2-1
- update to 1.7.2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-0.2.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Feb 20 2023 Tom Callaway <spot@fedoraproject.org> - 1.7.0-0.1.rc2
- update to 1.7.0-rc2
- disable tests on s390x (reported upstream: https://github.com/libunwind/libunwind/issues/464)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep  7 2022 Florian Weimer <fweimer@redhat.com> - 1.6.2-5
- Run the testsuite during build

* Wed Sep  7 2022 Florian Weimer <fweimer@redhat.com> - 1.6.2-4
- Enable %%autosetup to apply all patches (#2118019)

* Sun Aug 28 2022 Leif Liddy <leif.liddy@gmail.com> - 1.6.2-3
- enable dynamic page size support (bz2118019)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 20 2021 Tom Callaway <spot@fedoraproject.org> - 1.6.2-1
- update to 1.6.2

* Wed Jul 21 2021 Tom Callaway <spot@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 13 2020 Tom Callaway <spot@fedoraproject.org> - 1.4.0-4
- revert previous change
- fix it properly

* Mon Aug 10 2020 Tom Callaway <spot@fedoraproject.org> - 1.4.0-3
- fix multilib issues with libunwind.h (bz1866512)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Apr 14 2020 Dan Horák <dan[at]danny.cz> - 1.4.0-1
- Update to 1.4.0 with s390x support

* Fri Jan 31 2020 Tom Callaway <spot@fedoraproject.org> - 1.3.1-5
- backport change from upstream to fix reported test failures (bz1795896)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 13 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.1-1
- Update to 1.3.1
- Remove no longer needed patch (builds on all arches without it)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.2.1-5
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 29 2017 Tom Callaway <spot@fedoraproject.org> - 1.2.1-3
- fix multilib conflicts

* Sat Oct 14 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.1-2
- Add patch to fix ARM issues

* Fri Sep  1 2017 Tom Callaway <spot@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 1 2017 Jes Sorensen <jes.sorensen@gmail.com> - 1.2-1
- Update to libunwind-1.2 (#1439962)
- Disable setjmp the correct way and get rid of messy patch

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 10 2015 Tom Callaway <spot@fedoraproject.org> - 1.1-10
- fix CVE-2015-3239

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  2 2015 Tom Callaway <spot@fedoraproject.org> - 1.1-8 
- default arm unwinding method to exidx, old default of dwarf never works on Fedora
  (#1226806)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Jaromir Capik <jcapik@redhat.com> - 1.1-5
- Replacing ppc64 with the power64 macro (#1051641)

* Mon Jan 20 2014 Kyle McMartin <kmcmarti@redhat.com> 1.1-4
- Link test_ppc64_altivec against libunwind in tests/Makefile.am to fix build
  on ppc64.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 Kyle McMartin <kmcmarti@redhat.com> 1.1-2
- Add aarch64 support from backported ac6c0a65. (Mark Salter)
  (rhbz#969689)

* Mon Feb 18 2013 Kyle McMartin <kmcmarti@redhat.com> 1.1-1
- Update to upstream v1.1
- libunwind-install-ptrace.patch: drop upstream patch
- libunwind-arm-register-rename.patch: fixed upstream
- Add pkg-config files to libunwind-devel

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.1-3
- Add patch to fix build on ARM

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 15 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.0.1-1.fc17
- Upgrade to the upstream release. (BZ 738595).
- Use official distribution URL for %%{source}.

* Thu Jun 02 2011 Paul Whalen <paul.whalen@senecac.on.ca> - 0.99-3.20110424git1e10c293
- Added arm macro to ExclusiveArch

* Mon May  9 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 0.99-2.20110424git1e10c293
- Install static libunwind-ptrace library into system (for ltrace, BZ 703159).

* Sun Apr 24 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 0.99-1.20110424git1e10c293
- Rebase to the upstream post-0.99 snapshot (BZ 697453).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.16.20090430betagit4b8404d1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.99-0.15.20090430betagit4b8404d1
- Rebuilt for gcc bug 634757

* Sat Sep 11 2010 Parag Nemade <paragn AT fedoraproject.org> 0.99-0.14.20090430betagit4b8404d1.fc15
- Merge-review cleanup (#226052)

* Fri Dec  4 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.13.20090430betagit4b8404d1
- The devel package now requires also base package's %%{release}.
- Update the obsolete macro %%{package_version}.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.12.20090430betagit4b8404d1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 0.99-0.11.20090430betagit4b8404d1
- Disable the libunwind-setjmp library as no longer compatible with glibc and
  no Fedora dependencies on it (FTBSFS BZ 511562).

* Thu Apr 30 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 0.99-0.10.20090430betagit4b8404d1
- Fix the ia64 variant of GetIPInfo() (BZ 480412).

* Mon Apr 13 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 0.99-0.9.20090413betagitb483ea3f
- Rebase the package on the upstream variant: http://www.nongnu.org/libunwind/
  - Drop the patch libunwind-snap-070224-frysk20070405cvs.patch
    as even frysk-0.4-8.fc11 still has this library bundled statically.
- Disable the testsuite by default during the build.
  - It should be run separately as it crashes some ia64 kernels.
  - Drop the patch libunwind-snap-070224-orphanripper.patch.
- Drop the patch libunwind-snap-070224-dprintf-vs-stdio.h as no longer needed.
- Drop libunwind-snap-070224-multilib-rh342451.patch as accepted upstream.
- Fix and enable ppc (ppc32) arch.

* Tue Mar  3 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 0.99-0.8.frysk20070405cvs
- Fix .spec ExclusiveArch from i386 to %%{ix86}.
- Remove `BuildRequires: glibc gcc make tar gzip' - minimum build environment.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.7.frysk20070405cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 22 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 0.99-0.6.frysk20070405cvs
- Fix build error due to a `dprintf' conflict on recent glibc.
- New rpmbuild parameter: --without check

* Sun Feb 24 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 0.99-0.5.frysk20070405cvs
- Fix the multilib conflicts (BZ 342451).

* Sun Feb 24 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 0.99-0.4.frysk20070405cvs
- Abort the possibly hung up testcases after 120 seconds (BZ 427850, BZ 434147).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.99-0.3.frysk20070405cvs
- Autorebuild for GCC 4.3

* Sun Apr 22 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 0.99-0.2.frysk20070405cvs
- Require conflict with gdb < gdb-6.6-9 as it would not find `libunwind.so'.
- Fixed (unused - commented) rule for a RPM build with embedded debug info.

* Thu Apr  5 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 0.99-0.1.frysk20070405cvs
- Update to the upstream snapshot snap-070224.
- Use the Frysk's modified version, currently snapshot 20070405cvs.
- Extend the supported architectures from ia64 also to x86_64, i386 and ppc64.
- Spec file fixups.
- Split the package to its base and the `devel' part.
- Drop the statically built libraries.

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 0.98.5-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 0.98.5-2
- SELinux compatibility fix - stack is now non-exec (Jakub Jelinek suggestion).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.98.5-1.1
- rebuild

* Sat May 27 2006 Alexandre Oliva <aoliva@redhat.com> - 0.98.5-1
- Import version 0.98.5.

* Thu Feb 09 2006 Florian La Roche <laroche@redhat.com>
- remove empty scripts

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.98.2-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Mar 01 2005 Jeff Johnston <jjohnstn@redhat.com>	0.98.2.3
- Bump up release number

* Thu Nov 11 2004 Jeff Johnston <jjohnstn@redhat.com>	0.98.2.2
- Import version 0.98.2.

* Wed Nov 10 2004 Jeff Johnston <jjohnstn@redhat.com>	0.97.6
- Bump up release number

* Thu Aug 19 2004 Jeff Johnston <jjohnstn@redhat.com>	0.97.3
- Remove debug file from files list.

* Fri Aug 13 2004 Jeff Johnston <jjohnstn@redhat.com>	0.97.2
- Import version 0.97.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 09 2004  Elena Zannoni <ezannoni@redhat.com>	0.96.4
- Bump release number.

* Mon Feb 23 2004  Elena Zannoni <ezannoni@redhat.com>	0.96.3
- Bump release number.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004  Jeff Johnston <jjohnstn@redhat.com>	0.96.1
- Import version 0.96.

* Tue Jan 06 2004  Jeff Johnston <jjohnstn@redhat.com>	0.92.2
- Bump release number.

* Mon Oct 06 2003  Jeff Johnston <jjohnstn@redhat.com>	0.92.1
- Initial release

libunwind = %{version}-%{release}
