# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		numactl
Summary:	Library for tuning for Non Uniform Memory Access machines
Version:	2.0.19
Release: 4%{?dist}
# libnuma is LGPLv2 and GPLv2
# numactl binaries are GPLv2 only
License:	GPL-2.0-only
URL:		https://github.com/numactl/numactl
Source0:	%{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: make
BuildRequires: libtool automake autoconf

ExcludeArch: s390 %{arm}

%description
Simple NUMA policy support. It consists of a numactl program to run
other programs with a specific NUMA policy.

%package libs
Summary: libnuma libraries
# There is a tiny bit of GPLv2 code in libnuma.c
License: LGPL-2.1-only and GPL-2.0-only

%description libs
numactl-libs provides libnuma, a library to do allocations with
NUMA policy in applications.

%package devel
Summary: Development package for building Applications that use numa
Requires: %{name}-libs = %{version}-%{release}
License: LGPL-2.1-only and GPL-2.0-only

%description devel
Provides development headers for numa library calls

%prep
%autosetup

%build
%configure --prefix=/usr --libdir=%{_libdir}
%make_build

%install
rm -rf $RPM_BUILD_ROOT
%make_install

%ldconfig_scriptlets
%ldconfig_scriptlets libs

%files
%doc README.md
%{_bindir}/numactl
%{_bindir}/numademo
%{_bindir}/numastat
%{_bindir}/memhog
%{_bindir}/migspeed
%{_bindir}/migratepages
%{_mandir}/man8/*.8*
%exclude %{_mandir}/man2/*.2*

%files libs
%{_libdir}/libnuma.so.1.0.0
%{_libdir}/libnuma.so.1

%files devel
%{_libdir}/libnuma.so
%exclude %{_libdir}/libnuma.a
%{_libdir}/pkgconfig/numa.pc
%{_includedir}/numa.h
%{_includedir}/numaif.h
%{_includedir}/numacompat1.h
%{_mandir}/man3/*.3*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 05 2024 Jonathan Wright <jonathan@almalinux.org> - 2.0.19-1
- update to 2.0.19 rhbz#2321909
- Fixes "numactl exits if MPOL_PREFERRED_MANY isn't supported"
  https://github.com/numactl/numactl/issues/231

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 23 2024 Jonathan Wright <jonathan@almalinux.org> - 2.0.18-1
- update to 2.0.18 rhbz#2258959

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Oct 08 2022 Filipe Brandenburger <filbranden@gmail.com> - 2.0.16-1
- Upgrade to 2.0.16

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 11 2020 Florian Weimer <fweimer@redhat.com> - 2.0.14-2
- Trigger rebuild to avoid DT_INIT/DT_FINI with zero values

* Thu Sep 17 2020 Filipe Brandenburger <filbranden@gmail.com> - 2.0.14-1
- Upgrade to 2.0.14
- Re-enabled LTO, now that upstream has been fixed to support it.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 2020 Jeff Law <law@redhat.com> - 2.0.12-5
- Disable LTO

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 25 2018 Filipe Brandenburger <filbranden@gmail.com> - 2.0.12-1
- Rebased to version 2.0.12

* Wed Jul 25 2018 Filipe Brandenburger <filbranden@gmail.com>
- Fix check-rpaths warning about including /usr/lib64 in RPATH of the binaries.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Mar 24 2018 Richard W.M. Jones <rjones@redhat.com> - 2.0.11-9%{dist}
- Fix major/minor macros on glibc 2.27.
- Update config.{guess,sub} with versions which understand riscv64.
- Remove obsolete Buildroot tag.

* Sat Feb 24 2018 Florian Weimer <fweimer@redhat.com> - 2.0.11-8%{dist}
- Use LDFLAGS from redhat-rpm-config

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.11-7
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 06 2017 Petr Holasek <holasekp@gmail.com> - 2.0.11-3
- s390x arch enabled (bz1419064)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 14 2015 Petr Holasek <pholasek@redhat.com> - 2.0.11-1
- Rebased to version 2.0.11 (bz1290941)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 13 2014 Petr Holasek <pholasek@redhat.com> 2.0.10-2
- Fixing package conflict with man-pages (bz1151552)

* Wed Oct 08 2014 Petr Holasek <pholasek@redhat.com> 2.0.10-1
- Rebased to version 2.0.10 (bz1150511)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 31 2014 Petr Holasek <pholasek@redhat.com> 2.0.9-3
- fixed segfault on non-NUMA systems (bz1080421)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 09 2013 Petr Holasek <pholasek@redhat.com> 2.0.9-1
- rebased to version 2.0.9

* Fri Aug 02 2013 Karsten Hopp <karsten@redhat.com> 2.0.8-4
- rebuild in F20 to fix some dependency issues on PPC

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Petr Holasek <pholasek@redhat.com> - 2.0.8-3
- deleted empty numastat file

* Thu Nov  1 2012 Tom Callaway <spot@fedoraproject.org> - 2.0.8-2
- fix license issues

* Fri Oct 26 2012 Petr Holasek <pholasek@redhat.com> - 2.0.8-1
- Rebased to version 2.0.8

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May 19 2012 Petr Holasek <pholasek@redhat.com> - 2.0.7-6
- numademo segfault fix (bz823125, bz823127)

* Sun Apr 15 2012 Petr Holasek <pholasek@redhat.com> - 2.0.7-5
- Library splitted out of numactl package to numactl-libs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 02 2012 Anton Arapov <anton@redhat.com> - 2.0.7-3
- Include missing manpages

* Sat Jun 18 2011 Peter Robinson <pbrobinson@gmail.com> - 2.0.7-2
- Exclude ARM platforms

* Fri Apr 15 2011 Anton Arapov <anton@redhat.com> - 2.0.7-1
- Update to latest upstream stable version (bz 696703)

* Tue Mar 22 2011 Anton Arapov <anton@redhat.com> - 2.0.6-2
- Better manpages (bz 673613)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 04 2011 Neil Horman <nhorman@redhat.com> - 2.0.6-1
- Update to latest upstream stable version (bz 666379)

* Mon Oct 18 2010 Neil Horman <nhorman@redhat.com> - 2.0.5-1
- Update to latest stable upstream source

* Mon Feb 15 2010 Neil Horman <nhorman@redhat.com> - 2.0.3-8
- Remove static libs from numactl (bz 556088)

* Mon Aug 10 2009 Neil Horman <nhorman@redhat.com> - 2.0.3-7
- Add destructor to libnuma.so to free allocated memory (bz 516227)

* Mon Aug 10 2009 Neil Horman <nhorman@redhat.com> - 2.0.3-6
- Fix obo in nodes_allowed_list strncpy (bz 516223)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Neil Horman <nhorman@redhat.com>
- Update to full 2.0.3 version (bz 506795)

* Wed Jun 17 2009 Neil Horman <nhorman@redhat.com>
- Fix silly libnuma warnings again (bz 499633)

* Fri May 08 2009 Neil Horman <nhorman@redhat.com>
- Update to 2.0.3-rc3 (bz 499633)

* Wed Mar 25 2009 Mark McLoughlin <markmc@redhat.com> - 2.0.2-4
- Remove warning from libnuma (bz 484552)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 29 2008 Neil Horman <nhorman@redhat.com> - 2.0.2-2
- Fix build break due to register selection in asm

* Mon Sep 29 2008 Neil Horman <nhorman@redhat.com> - 2.0.2-1
- Update rawhide to version 2.0.2 of numactl

* Fri Apr 25 2008 Neil Horman <nhorman@redhat.com> - 1.0.2-6
- Fix buffer size passing and arg sanity check for physcpubind (bz 442521)

* Fri Mar 14 2008 Neil Horman <nhorman@redhat.com> - 1.0.2-5
- Fixing spec file to actually apply alpha patch :)

* Fri Mar 14 2008 Neil Horman <nhorman@redhat.com> - 1.0.2-4
- Add alpha syscalls (bz 396361)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.2-3
- Autorebuild for GCC 4.3

* Thu Dec 20 2007 Neil Horman <nhorman@redhat.com> - 1.0.2-1
- Update numactl to fix get_mempolicy signature (bz 418551)

* Fri Dec 14 2007 Neil Horman <nhorman@redhat.com> - 1.0.2-1
- Update numactl to latest version (bz 425281)

* Tue Aug 07 2007 Neil Horman <nhorman@redhat.com> - 0.9.8-4
- Fixing some remaining merge review issues (bz 226207)

* Fri Aug 03 2007 Neil Horman <nhorman@redhat.com> - 0.9.8-3
- fixing up merge review (bz 226207)

* Fri Jan 12 2007 Neil Horman <nhorman@redhat.com> - 0.9.8-2
- Properly fixed bz 221982
- Updated revision string to include %%{dist}

* Thu Jan 11 2007 Neil Horman <nhorman@redhat.com> - 0.9.8-1.38
- Fixed -devel to depend on base package so libnuma.so resolves

* Thu Sep 21 2006 Neil Horman <nhorman@redhat.com> - 0.9.8-1.36
- adding nodebind patch for bz 207404

* Fri Aug 25 2006 Neil Horman <nhorman@redhat.com> - 0.9.8-1.35
- moving over libnuma.so to -devel package as well

* Fri Aug 25 2006 Neil Horman <nhorman@redhat.com> - 0.9.8-1.34
- split out headers/devel man pages to a devel subpackage

* Tue Aug 15 2006 Neil Horman <nhorman@redhat.com> - 0.9.8-1.32
- add patch for broken cpu/nodebind output (bz 201906)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.9.8-1.31
- rebuild

* Tue Jun 13 2006 Neil Horman <nhorman@redhat.com>
- Rebased numactl to version 0.9.8 for FC6/RHEL5

* Wed Apr 26 2006 Neil Horman <nhorman@redhat.com>
- Added patches for 64 bit overflows and cpu mask problem

* Fri Mar 10 2006 Bill Nottingham <notting@redhat.com>
- rebuild for ppc TLS issue (#184446)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.6.4-1.25.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Jul  7 2005 Dave Jones <davej@redhat.com>
- numactl doesn't own the manpage dirs. (#161547)

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4

* Tue Feb  8 2005 Dave Jones <davej@redhat.com>
- rebuild with -D_FORTIFY_SOURCE=2

* Wed Nov 10 2004 David Woodhouse <dwmw2@redhat.com>
- Fix build on x86_64

* Thu Oct 21 2004 David Woodhouse <dwmw2@redhat.com>
- Add PPC support

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jun 05 2004 Warren Togami <wtogami@redhat.com> 
- spec cleanup

* Sat Jun 05 2004 Arjan van de Ven <arjanv@redhat.com>
- initial packaging

