# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:     libpcap
Epoch:    14
Version:  1.10.6
Release: 2%{?dist}
Summary:  A system-independent interface for user-level packet capture
License:  ISC AND BSD-2-Clause AND BSD-3-Clause AND BSD-4-Clause-UC
URL:      https://www.tcpdump.org/

BuildRequires: make
BuildRequires: bison
BuildRequires: bluez-libs-devel
BuildRequires: flex
BuildRequires: gcc
BuildRequires: git
BuildRequires: glibc-kernheaders >= 2.2.0
#rdma-core-devel not available on arm
%ifnarch %{arm}
BuildRequires: rdma-core-devel
%endif

Source0:  https://www.tcpdump.org/release/%{name}-%{version}.tar.xz
Source1:  https://www.tcpdump.org/release/%{name}-%{version}.tar.xz.sig

Patch0001:      0001-man-tcpdump-and-tcpslice-have-manpages-in-man8.patch
Patch0002:      0002-pcap-config-mitigate-multilib-conflict.patch
Patch0003:      0003-pcap-linux-apparently-ctc-interfaces-on-s390-has-eth.patch

%description
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

Install libpcap if you need to do low-level network traffic monitoring
on your network.

%package devel
Summary: Libraries and header files for the libpcap library
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

This package provides the libraries, include files, and other
resources needed for developing libpcap applications.

%prep
%autosetup -S git

#sparc needs -fPIC
%ifarch %{sparc}
sed -i -e 's|-fpic|-fPIC|g' configure
%endif

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%ifarch %{arm}
%configure
%else
%configure --enable-rdma
%endif
%make_build

%install
%make_install
rm -f $RPM_BUILD_ROOT%{_libdir}/libpcap.a

%ldconfig_scriptlets

%files
%license LICENSE
%doc README.md CHANGES CREDITS
%{_libdir}/libpcap.so.*
%{_mandir}/man7/pcap*.7*

%files devel
%{_bindir}/pcap-config
%{_includedir}/pcap*.h
%{_includedir}/pcap
%{_libdir}/libpcap.so
%{_libdir}/pkgconfig/libpcap.pc
%{_mandir}/man1/pcap-config.1*
%{_mandir}/man3/pcap*.3*
%{_mandir}/man5/pcap*.5*

%changelog
* Mon Jan 05 2026 Michal Ruprich <mruprich@redhat.com> - 14:1.10.6-1
- New version 1.10.6

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.10.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 03 2024 Michal Ruprich <mruprich@redhat.com> - 14:1.10.5-1
- New version 1.10.5

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.10.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.10.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.10.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Apr 12 2023 Michal Ruprich <mruprich@redhat.com> - 14:1.10.4-1
- New version 1.10.4

* Tue Mar 21 2023 Michal Ruprich <mruprich@redhat.com> - 14:1.10.3-3
- SPDX migration

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Michal Ruprich <mruprich@redhat.com> - 14:1.10.3-1
- New version 1.10.3

* Tue Jan 03 2023 Michal Ruprich <mruprich@redhat.com> - 14:1.10.2-1
- New version 1.10.2

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 10 2021 Michal Ruprich <mruprich@redhat.com> - 14:1.10.1-1
- New version 1.10.1

* Thu Feb 11 2021 Michal Ruprich <mruprich@redhat.com> - 14:1.10.0-1
- New version 1.10.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 12 2020 Michal Ruprich <mruprich@redhat.com> - 14:1.9.1-6
- Using make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 15 2020 Michal Ruprich <michalruprich@gmail.com> - 14:1.9.1-4
- Enabling rdma support in libpcap

* Mon Feb 24 2020 Michal Ruprich <mruprich@redhat.com> - 14:1.9.1-3
- libpcap should print an error on wrong IPv4 address

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 11 2019 Michal Ruprich <mruprich@redhat.com> - 14:1.9.1-1
- New version 1.9.1
- Fix for CVE-2018-16301, CVE-2019-15161, CVE-2019-15162, CVE-2019-15163, CVE-2019-15164, CVE-2019-15165

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Peter Robinson <pbrobinson@fedoraproject.org> 14:1.9.0-2
- pkgconfig file belong in devel package
- drop obsolete group in spec

* Wed Aug 01 2018 Michal Ruprich <mruprich@redhat.com> - 14:1.9.0-1
- New version 1.9.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.8.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 06 2018 Michal Ruprich <mruprich@redhat.com> - 14:1.8.1-10
- Adding support for AF_VSOCK

* Tue Feb 20 2018 Martin Sehnoutka <msehnout@redhat.com> - 14:1.8.1-9
- Add gcc to BuildRequires

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 14:1.8.1-7
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 18 2017 Martin Sehnoutka <msehnout@redhat.com> - 14:1.8.1-4
- Drop TPACKET_V3 patch as it should be fixed in kernel by now

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 1.8.1-2
- Add missing %%license macro

* Mon Oct 31 2016 Luboš Uhliarik <luhliari@redhat.com> - 14:1.8.1-1
- new version 1.8.1

* Mon Aug 08 2016 Luboš Uhliarik <luhliari@redhat.com> - 14:1.8.0-1
- new version 1.8.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 14:1.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jun 29 2015 Michal Sekletar <msekleta@redhat.com> - 14:1.7.4-1
- update to 1.7.4 (#1236387)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Michal Sekletar <msekleta@redhat.com> - 14:1.7.3-1
- update to 1.7.3 (#1214723)
- fix build against bluez-5 (#1178297)

* Fri Mar 13 2015 Michal Sekletar <msekleta@redhat.com> - 14:1.7.2-1
- update to 1.7.2 (#1201078)

* Mon Feb 23 2015 Michal Sekletar <msekleta@redhat.com> - 14:1.6.2-2
- fix scaling of pcap-ng timestamps (#1169322)
- remove kernel-devel from buildrequires

* Mon Sep 29 2014 Michal Sekletar <msekleta@redhat.com> - 14:1.6.2-1
- update to 1.6.2 (#1124174)
- disable TPACKET_V3 support (#1131500)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Michal Sekletar <msekleta@redhat.com> - 14:1.5.3-3
- don't link against libnl

* Fri Mar 28 2014 Michal Sekletar <msekleta@redhat.com> - 14:1.5.3-2
- link against libnl (#765716)

* Wed Jan 15 2014 Michal Sekletar <msekleta@redhat.com> - 14:1.5.3-1
- update to 1.5.3

* Thu Nov 28 2013 Michal Sekletar <msekleta@redhat.com> - 14:1.5.1-1
- update to 1.5.1

* Fri Nov 08 2013 Michal Sekletar <msekleta@redhat.com> - 14:1.5.0-1.20131108git459712e
- update to snapshot 20131108git459712e

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 06 2013 Michal Sekletar <msekleta@redhat.com> - 14:1.4.0-1
- update to 1.4.0

* Tue Mar 26 2013 Michal Sekletar <msekleta@redhat.com> - 14:1.3.0-4
- remove unused variable from pcap-config to prevent multilib conflicts
- specfile cleanup

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Michal Sekletar <msekleta@redhat.com> 14:1.3.0-1
- Update to 1.3.0

* Thu Jan 05 2012 Jan Synáček <jsynacek@redhat.com> 14:1.2.1-2
- Rebuilt for GCC 4.7

* Tue Jan 03 2012 Jan Synáček <jsynacek@redhat.com> 14:1.2.1-1
- Update to 1.2.1
- Drop unnecessary -fragment patch

* Fri Dec 02 2011 Michal Sekletar <msekleta@redhat.com> 14:1.2.0-1
- update to 1.2.0

* Tue Sep 06 2011 Michal Sekletar <msekleta@redhat.com> 14:1.1.1-4
- fix capture of fragmented ipv6 packets

* Fri Apr 22 2011 Miroslav Lichvar <mlichvar@redhat.com> 14:1.1.1-3
- ignore /sys/net/dev files on ENODEV (#693943)
- drop ppp patch
- compile with -fno-strict-aliasing

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Apr 06 2010 Miroslav Lichvar <mlichvar@redhat.com> 14:1.1.1-1
- update to 1.1.1

* Wed Dec 16 2009 Miroslav Lichvar <mlichvar@redhat.com> 14:1.0.0-5.20091201git117cb5
- update to snapshot 20091201git117cb5

* Sat Oct 17 2009 Dennis Gilmore <dennis@ausil.us> 14:1.0.0-4.20090922gite154e2
- use -fPIC on sparc arches

* Wed Sep 23 2009 Miroslav Lichvar <mlichvar@redhat.com> 14:1.0.0-3.20090922gite154e2
- update to snapshot 20090922gite154e2
- drop old soname

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.0.0-2.20090716git6de2de
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Miroslav Lichvar <mlichvar@redhat.com> 14:1.0.0-1.20090716git6de2de
- update to 1.0.0, git snapshot 20090716git6de2de

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:0.9.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jun 27 2008 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.8-3
- use CFLAGS when linking (#445682)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 14:0.9.8-2
- Autorebuild for GCC 4.3

* Wed Oct 24 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.8-1
- update to 0.9.8

* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.7-3
- update license tag

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 14:0.9.7-2
- Rebuild for RH #249435

* Tue Jul 24 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.7-1
- update to 0.9.7

* Tue Jun 19 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.6-1
- update to 0.9.6

* Tue Nov 28 2006 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.5-1
- split from tcpdump package (#193657)
- update to 0.9.5
- don't package static library
- maintain soname
