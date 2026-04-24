# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libseccomp
Version:        2.6.0
Release: 4%{?dist}
Summary:        Enhanced seccomp library
License:        LGPL-2.1-only
URL:            https://github.com/seccomp/libseccomp
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz

# Backports from upstream

# From https://github.com/seccomp/libseccomp/pull/459
Patch0101:      fix-murmur-hash-strict-aliasing-violation.patch
# https://github.com/seccomp/libseccomp/pull/452
Patch0102: remove-fuzzer-test-from-62-sim-arch_transactions.patch

BuildRequires:  gcc
BuildRequires:  gperf
BuildRequires:  make

%ifnarch riscv64 s390
# Versions prior to 3.13.0-4 do not work on ARM with newer glibc 2.25.0-6
# See https://bugzilla.redhat.com/show_bug.cgi?id=1466017
BuildRequires:  valgrind >= 1:3.13.0-4
%endif

%description
The libseccomp library provides an easy to use interface to the Linux Kernel's
syscall filtering mechanism, seccomp.  The libseccomp API allows an application
to specify which syscalls, and optionally which syscall arguments, the
application is allowed to execute, all of which are enforced by the Linux
Kernel.

%package devel
Summary:        Development files used to build applications with libseccomp support
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The libseccomp library provides an easy to use interface to the Linux Kernel's
syscall filtering mechanism, seccomp.  The libseccomp API allows an application
to specify which syscalls, and optionally which syscall arguments, the
application is allowed to execute, all of which are enforced by the Linux
Kernel.

%package static
Summary:        Enhanced seccomp static library
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The libseccomp library provides an easy to use interface to the Linux Kernel's
syscall filtering mechanism, seccomp.  The libseccomp API allows an application
to specify which syscalls, and optionally which syscall arguments, the
application is allowed to execute, all of which are enforced by the Linux
Kernel.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_includedir}
mkdir -p %{buildroot}/%{_mandir}

%make_install

rm -f %{buildroot}/%{_libdir}/libseccomp.la

%check
%make_build check


%files
%license LICENSE
%doc CREDITS README.md CHANGELOG CONTRIBUTING.md
%{_libdir}/libseccomp.so.*

%files devel
%{_includedir}/seccomp.h
%{_includedir}/seccomp-syscalls.h
%{_libdir}/libseccomp.so
%{_libdir}/pkgconfig/libseccomp.pc
%{_bindir}/scmp_sys_resolver
%{_mandir}/man1/*
%{_mandir}/man3/*

%files static
%{_libdir}/libseccomp.a

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 18 2025 Romain Geissler <romain.geissler@amadeus.com> - 2.6.0-1
- New upstream version (#2341880)

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Neal Gompa <ngompa@fedoraproject.org> - 2.5.5-1
- New upstream version (#2077899)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 01 2023 Anderson Toshiyuki Sasaki <ansasaki@redhat.com> - 2.5.3-5
- SPDX migration

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 06 2021 Neal Gompa <ngompa@fedoraproject.org> - 2.5.3-1
- New upstream version (#2020824)

* Wed Nov 03 2021 Debarshi Ray <rishi@fedoraproject.org> - 2.5.2-1
- New upstream version (#1900097)

* Wed Nov 03 2021 Debarshi Ray <rishi@fedoraproject.org> - 2.5.1-1
- New upstream version (#1900097)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 05 2020 Neal Gompa <ngompa13@gmail.com> - 2.5.0-3
- Apply fixes to change internal handling of the notification fd (#1865802)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Neal Gompa <ngompa13@gmail.com> - 2.5.0-1
- New upstream version (#1858965)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 16 2019 Neal Gompa <ngompa13@gmail.com> - 2.4.2-2
- Modernize spec
- Backport fix for missing __SNR_ppoll symbol (#1777889)
- Refresh patch to build on aarch64 with upstream version

* Wed Nov 20 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.2-1
- New upstream version (#1765314)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 17 2019 Paul Moore <paul@paul-moore.com> - 2.4.1-0
- New upstream version

* Thu Mar 14 2019 Paul Moore <paul@paul-moore.com> - 2.4.0-0
- New upstream version
- Added a hack to workaround test failures (see %%check above)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 07 2018 Paul Moore <paul@paul-moore.com> - 2.3.3-4
- Remove ldconfig scriptlet, thanks to James Antill (RHBZ #1644074)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 10 2018 Paul Moore <pmoore@redhat.com> - 2.3.3-1
- New upstream version

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 Stephen Gallagher <sgallagh@redhat.com> - 2.3.2-3
- Re-enable valgrind-based tests on ARMv7

* Thu Jun 29 2017 Stephen Gallagher <sgallagh@redhat.com> - 2.3.2-2
- Disable running valgrind-based tests on ARMv7 due to glibc/valgrind bug (RHBZ #1466017)

* Wed Mar 01 2017 Paul Moore <pmoore@redhat.com> -2.3.2-1
- New upstream version

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Apr 20 2016 Paul Moore <pmoore@redhat.com> - 2.3.1-1
- Cleanup the changelog whitespace and escape the macros to make rpmlint happy

* Wed Apr 20 2016 Paul Moore <pmoore@redhat.com> - 2.3.1-0
- New upstream version

* Tue Mar  1 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.3.0-1
- No valgrind on s390

* Mon Feb 29 2016 Paul Moore <pmoore@redhat.com> - 2.3.0-0
- New upstream version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 08 2015 Paul Moore <pmoore@redhat.com> - 2.2.3-0
- New upstream version

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Paul Moore <pmoore@redhat.com> - 2.2.1-0
- New upstream version

* Thu Feb 12 2015 Paul Moore <pmoore@redhat.com> - 2.2.0-0
- New upstream version
- Added aarch64 support
- Added a static build

* Thu Sep 18 2014 Paul Moore <pmoore@redhat.com> - 2.1.1-6
- Fully builds on i686, x86_64, and armv7hl (RHBZ #1106071)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.1.1-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 27 2014 Paul Moore <pmoore@redhat.com> - 2.1.1-2
- Build with CFLAGS="${optflags}"

* Mon Feb 17 2014 Paul Moore <pmoore@redhat.com> - 2.1.1-1
- Removed the kernel dependency (RHBZ #1065572)

* Thu Oct 31 2013 Paul Moore <pmoore@redhat.com> - 2.1.1-0
- New upstream version
- Added a %%check procedure for self-test during build

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Paul Moore <pmoore@redhat.com> - 2.1.0-0
- New upstream version
- Added support for the ARM architecture
- Added the scmp_sys_resolver tool

* Mon Jan 28 2013 Paul Moore <pmoore@redhat.com> - 2.0.0-0
- New upstream version

* Tue Nov 13 2012 Paul Moore <pmoore@redhat.com> - 1.0.1-0
- New upstream version with several important fixes

* Tue Jul 31 2012 Paul Moore <pmoore@redhat.com> - 1.0.0-0
- New upstream version
- Remove verbose build patch as it is no longer needed
- Enable _smp_mflags during build stage

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Paul Moore <pmoore@redhat.com> - 0.1.0-1
- Limit package to x86/x86_64 platforms (RHBZ #837888)

* Tue Jun 12 2012 Paul Moore <pmoore@redhat.com> - 0.1.0-0
- Initial version
