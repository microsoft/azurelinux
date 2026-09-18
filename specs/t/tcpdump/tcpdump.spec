# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define tcpslice_dir tcpslice-1.8

Summary: A network traffic monitoring tool
Name: tcpdump
Epoch: 14
Version: 4.99.6
Release: 2%{?dist}
License: BSD-2-Clause AND BSD-3-Clause AND BSD-4-Clause AND BSD-4-Clause-UC AND ISC AND NTP
URL: http://www.tcpdump.org
BuildRequires: make
BuildRequires: automake openssl-devel libpcap-devel git-core gcc
BuildRequires: systemd-rpm-macros

Source0: http://www.tcpdump.org/release/tcpdump-%{version}.tar.xz
Source1: http://www.tcpdump.org/release/%{tcpslice_dir}.tar.gz
Source2: http://www.tcpdump.org/release/tcpdump-%{version}.tar.xz.sig
Source3: tcpdump-sysusers.conf

Patch0002:      0002-Use-getnameinfo-instead-of-gethostbyaddr.patch
Patch0003:      0003-Drop-root-priviledges-before-opening-first-savefile-.patch
Patch0007:      0007-Introduce-nn-option.patch
Patch0009:      0009-Change-n-flag-to-nn-in-TESTonce.patch

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires:       filesystem(unmerged-sbin-symlinks)
Provides:       /usr/sbin/tcpdump
%endif

%description
Tcpdump is a command-line tool for monitoring network traffic.
Tcpdump can capture and display the packet headers on a particular
network interface or on all interfaces.  Tcpdump can display all of
the packet headers, or just the ones that match particular criteria.

Install tcpdump if you need a program to monitor network traffic.

%prep
%autosetup -a 1 -S git

%build
export CFLAGS="$RPM_OPT_FLAGS $(getconf LFS_CFLAGS) -fno-strict-aliasing -DGUESS_TSO"

pushd %{tcpslice_dir}
# update config.{guess,sub}
automake -a -f 2> /dev/null || :
./autogen.sh
%configure
%{make_build}
popd

%configure --with-crypto --with-user=tcpdump --without-smi
%{make_build}

%check
make check

%install
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}

pushd %{tcpslice_dir}
install -m755 tcpslice ${RPM_BUILD_ROOT}%{_sbindir}
install -m644 tcpslice.1 ${RPM_BUILD_ROOT}%{_mandir}/man8/tcpslice.8
popd

install -m755 tcpdump ${RPM_BUILD_ROOT}%{_sbindir}
install -m644 tcpdump.1 ${RPM_BUILD_ROOT}%{_mandir}/man8/tcpdump.8

install -p -D -m 0644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysusersdir}/tcpdump.conf

# fix section numbers
sed -i 's/\(\.TH[a-zA-Z ]*\)[1-9]\(.*\)/\18\2/' \
	${RPM_BUILD_ROOT}%{_mandir}/man8/*


%files
%license LICENSE
%doc README.md CHANGES CREDITS
%{_sbindir}/tcpdump
%{_sbindir}/tcpslice
%{_sysusersdir}/tcpdump.conf
%{_mandir}/man8/tcpslice.8*
%{_mandir}/man8/tcpdump.8*

%changelog
* Fri Feb 13 2026 Michal Ruprich <mruprich@redhat.com> - 14:4.99.6-2
- Resolves: #2343526 - tcpdump crashes with -w -Z root options

* Mon Jan 05 2026 Michal Ruprich <mruprich@redhat.com> - 14:4.99.6-1
- New version 4.99.6

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.99.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 05 2025 Michal Ruprich <mruprich@redhat.com> - 14:4.99.5-5
- Updating tcpslice to version 1.8

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 14:4.99.5-4
- Drop call to %sysusers_create_compat

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.99.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 14:4.99.5-2
- Rebuilt for the bin-sbin merge (2nd attempt)

* Tue Sep 03 2024 Michal Ruprich <mruprich@redhat.com> - 14:4.99.5-1
- New version 4.99.5

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.99.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 14:4.99.4-8
- Rebuilt for the bin-sbin merge

* Sun May 05 2024 Michal Ruprich <mruprich@redhat.com> - 14:4.99.4-7
- Resolves: #2274793 - Crafted .pcap file may lead to Denial of Service

* Mon Feb 12 2024 Michal Ruprich <mruprich@redhat.com> - 14:4.99.4-6
- New version of tcpslice, 1.7 (rhbz #2263644)

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.99.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 02 2023 Pavol Žáčik <pzacik@redhat.com> - 14:4.99.4-4
- Fix PGM option printing

* Mon Aug 21 2023 Michal Ruprich <mruprich@redhat.com> - 14:4.99.4-3
- Enabling BIG TCP packets in tcpdump

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.99.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Apr 12 2023 Michal Ruprich <mruprich@redhat.com> - 14:4.99.4-1
- New version 4.99.4

* Wed Mar 22 2023 Michal Ruprich <mruprich@redhat.com> - 14:4.99.3-3
- SPDX migration

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.99.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Michal Ruprich <mruprich@redhat.com> - 14:4.99.3-1
- New version 4.99.3

* Tue Jan 03 2023 Michal Ruprich <mruprich@redhat.com> - 14:4.99.2-1
- New version 4.99.2

* Wed Aug 03 2022 Luca BRUNO <lucab@lucabruno.net> - 14:4.99.1-8
- Simplify sysusers.d configuration fragment

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.99.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Michal Ruprich <mruprich@redhat.com> - 14:4.99.1-6
- Using systemd-sysusers

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.99.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Michal Ruprich <mruprich@redhat.com> - 14:4.99.1-4
- New version of tcpslice-1.5

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 14:4.99.1-3
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Michal Ruprich <mruprich@redhat.com> - 14:4.99.1-1
- New versiom 4.99.1

* Mon Mar 15 2021 Michal Ruprich <mruprich@redhat.com> - 14:4.99.0-3
- Testing gating

* Fri Mar 12 2021 Michal Ruprich <mruprich@redhat.com> - 14:4.99.0-2
- New version of tcpslice-1.3

* Thu Feb 11 2021 Michal Ruprich <mruprich@redhat.com> - 14:4.99.0-1
- New version 4.99.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.9.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 26 2020 Michal Ruprich <mruprich@redhat.com> - 14:4.9.3-6
- Fix for CVE-2020-8037

* Thu Nov 19 2020 Michal Ruprich <mruprich@redhat.com> - 14:4.9.3-5
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Michal Ruprich <michalruprich@gmail.com> - 14:4.9.3-3
- Fixing a -G option bug in one of our patches

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 15 2019 Michal Ruprich <mruprich@redhat.com> - 14:4.9.3-1
- New version 4.9.3
- Fixes CVE-2017-16808, CVE-2018-14468, CVE-2018-14469, CVE-2018-14470, CVE-2018-14466, CVE-2018-14461, CVE-2018-14462, CVE-2018-14465, CVE-2018-14881, CVE-2018-14464, CVE-2018-14463, CVE-2018-14467, CVE-2018-10103, CVE-2018-10105, CVE-2018-14880, CVE-2018-16451, CVE-2018-14882, CVE-2018-16227, CVE-2018-16229, CVE-2018-16301, CVE-2018-16230, CVE-2018-16452, CVE-2018-16300, CVE-2018-16228, CVE-2019-15166, CVE-2019-15167

* Mon Sep 16 2019 Michal Ruprich <mruprich@redhat.com> - 14:4.9.2-9
- Adding getent to pre scriptlet to avoid audit messages (rhbz#1715420)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.9.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.9.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.9.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 21 2018 Michal Ruprich <mruprich@redhat.com> - 14:4.9.2-5
- Removing sharutils from build-time dependencies
- Changing git dependency to smaller git-core

* Thu May 10 2018 Michal Ruprich <mruprich@redhat.com> - 14:4.9.2-4
- Enabling upstream tests
- Adding VSOCK support

* Tue Feb 20 2018 Martin Sehnoutka <msehnout@redhat.com> - 14:4.9.2-3
- Add gcc to BuildRequires

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 05 2017 Martin Sehnoutka <msehnout@redhat.com> - 14:4.9.2-1
- New upstream release 4.9.2

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Florian Weimer <fweimer@redhat.com> - 14:4.9.1-2
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Martin Sehnoutka <msehnout@redhat.com> - 14:4.9.1-1
- New upstream release 4.9.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 03 2017 Martin Sehnoutka <msehnout@redhat.com> - 14:4.9.0-1
- New upstream version 4.9.0

* Mon Oct 31 2016 Luboš Uhliarik <luhliari@redhat.com> - 14:4.8.1-1
- new version 4.8.1

* Tue Aug 09 2016 Luboš Uhliarik <luhliari@redhat.com> - 14:4.8.0-1
- new version 4.8.0

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 14:4.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jun 29 2015 Michal Sekletar <msekleta@redhat.com> - 14:4.7.4-3
- prevent sefaulting by properly initializing chown_flag variable (#1223329)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:4.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May  5 2015 Michal Sekletar <msekleta@redhat.com> - 14:4.7.4-1
- rebase to 4.7.4 (#1214753)

* Wed Mar 25 2015 Michal Sekletar <msekleta@redhat.com> - 14:4.7.3-1
- rebase to 4.7.3 (#1201573)
- contains fixes for CVE-2015-0261 CVE-2015-2154 CVE-2015-2153 CVE-2015-2155 (#1201799,#1201792,#1201795,#1201797)

* Wed Dec 03 2014 Michal Sekletar <msekleta@redhat.com> - 14:4.6.2-3
- fix for CVE-2014-9140

* Thu Nov 20 2014 Michal Sekletar <msekleta@redhat.com> - 14:4.6.2-2
- fix for CVE-2014-8767 (#1165160)
- fix for CVE-2014-8768 (#1165161)
- fix for CVE-2014-8769 (#1165162)

* Mon Oct 20 2014 Michal Sekletar <msekleta@redhat.com> - 14:4.6.2-1
- update to 4.6.2 (#1124289)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:4.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 28 2013 Michal Sekletar <msekleta@redhat.com> - 14:4.5.1-1
- update to 4.5.1

* Fri Nov 08 2013 Michal Sekletar <msekleta@redhat.com> - 14:4.5.0-1.20131108gitb07944a
- update to snaphot gitb07944a

* Mon Oct  7 2013 Michal Sekletar <msekleta@redhat.com> - 14:4.4.0-3
- don't try to change ownership of stdout (#1015767)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 06 2013 Michal Sekletar <msekleta@redhat.com> - 14:4.4.0-1
- update to 4.4.0

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:4.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Michal Sekletar <msekleta@redhat.com> - 14:4.3.0-1
- Update to 4.3.0

* Wed May 16 2012 Michal Sekletar <msekleta@redhat.com>
- Resolves: #809638
- created savefile has proper owner

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 03 2012 Jan Synáček <jsynacek@redhat.com> - 14:4.2.1-1
- Update to 4.2.1
- Remove ppi.h from sources (readded again in upstream tarball)

* Fri Dec 02 2011 Michal Sekletar <msekleta@redhat.com> - 14:4.2.0-1
- updated to 4.2.0
- added new source file ppi.h, missing in upstream tarball
- disabled make check because of missing .pcap files in testsuite
- dropped unnecessary patches

* Wed Aug 24 2011 Michal Sekletar <msekleta@redhat.com> - 14:4.1.1-3
- Fix manpage (#663739)
- Fix improper handling of bad date format in tcpslice (#684005)
- Spec file clean up

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Apr 06 2010 Miroslav Lichvar <mlichvar@redhat.com> - 14:4.1.1-1
- update to 4.1.1
- add %%check

* Wed Sep 23 2009 Miroslav Lichvar <mlichvar@redhat.com> - 14:4.0.0-3.20090921gitdf3cb4
- update to snapshot 20090921gitdf3cb4

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 14:4.0.0-2.20090818git832d2c
- rebuilt with new openssl

* Thu Aug 20 2009 Miroslav Lichvar <mlichvar@redhat.com> - 14:4.0.0-1.20090818git832d2c
- update to post 4.0.0 git snapshot 20090818git832d2c
- print retrans and reachable times in ICMPv6 as milliseconds (#474264)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:3.9.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:3.9.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Miroslav Lichvar <mlichvar@redhat.com> - 14:3.9.8-7
- rebuild for new openssl
- convert CREDITS to UTF-8 (#226481)

* Fri Aug 29 2008 Miroslav Lichvar <mlichvar@redhat.com> - 14:3.9.8-6
- rediff patches with fuzz
- add -fno-strict-aliasing to CFLAGS

* Mon Jun 02 2008 Miroslav Lichvar <mlichvar@redhat.com> - 14:3.9.8-5
- update config.{guess,sub} when building tcpslice
- remove -D_GNU_SOURCE from CFLAGS
- disable libsmi check in configure

* Wed Feb 13 2008 Miroslav Lichvar <mlichvar@redhat.com> - 14:3.9.8-4
- fix building with new glibc headers

* Thu Dec 06 2007 Miroslav Lichvar <mlichvar@redhat.com> - 14:3.9.8-3
- update IKEv2 support

* Thu Dec  6 2007 Jeremy Katz <katzj@redhat.com> - 14:3.9.8-2
- rebuild for new openssl

* Wed Oct 24 2007 Miroslav Lichvar <mlichvar@redhat.com> - 14:3.9.8-1
- update to 3.9.8
- don't use gethostbyaddr
- fix default user in man page

* Tue Sep 18 2007 Miroslav Lichvar <mlichvar@redhat.com> - 14:3.9.7-5
- support decoding IKEv2 packets

* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> - 14:3.9.7-4
- rebuild

* Thu Aug 09 2007 Miroslav Lichvar <mlichvar@redhat.com> - 14:3.9.7-3
- enable crypto support on 64-bit architectures
- update license tag

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 14:3.9.7-2
- rebuild for toolchain bug

* Tue Jul 24 2007 Miroslav Lichvar <mlichvar@redhat.com> - 14:3.9.7-1
- update to 3.9.7
- with -C option, drop root privileges before opening first savefile (#244860)
- update tcpslice to 1.2a3
- include time patch from Debian to fix tcpslice on 64-bit architectures

* Thu Mar 15 2007 Miroslav Lichvar <mlichvar@redhat.com> - 14:3.9.5-3
- fix buffer overflow in 802.11 printer (#232349, CVE-2007-1218)
- spec cleanup (#226481)

* Tue Dec 12 2006 Miroslav Lichvar <mlichvar@redhat.com> - 14:3.9.5-2
- use tcpdump user, fix scriptlet (#219268)

* Wed Nov 29 2006 Miroslav Lichvar <mlichvar@redhat.com> - 14:3.9.5-1
- split off libpcap and arpwatch (#193657)
- update to 3.9.5
- force linking with system libpcap

* Fri Nov 17 2006 Miroslav Lichvar <mlichvar@redhat.com> - 14:3.9.4-9
- fix processing of Prism and AVS headers (#206686)
- fix arp2ethers script
- update ethercodes.dat
- move pcap man page to devel package

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 14:3.9.4-8.1
- rebuild

* Thu Jun 22 2006 Martin Stransky <stransky@redhat.com> - 14:3.9.4-8
- more ipv6 flags

* Sun Jun  4 2006 Jeremy Katz <katzj@redhat.com> - 14:3.9.4-7
- fix libpcap-devel inclusion of .so and its deps (#193189)

* Thu Jun 1 2006 Martin Stransky <stransky@redhat.com> - 14:3.9.4-6
- added release to arpwatch package name

* Wed May 31 2006 Martin Stransky <stransky@redhat.com> - 14:3.9.4-5
- removed libpcap-devel dependency from libpcap

* Mon May 29 2006 Martin Stransky <stransky@redhat.com> - 14:3.9.4-4
- added libpcap-devel package (#193189)

* Tue Mar 28 2006 Martin Stransky <stransky@redhat.com> - 14:3.9.4-3
- updated ethernet codes (#186633)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 14:3.9.4-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 14:3.9.4-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Dec 20 2005 Martin Stransky <stransky@redhat.com> - 14:3.9.4-2
- fix for #176010 - file owner problem when using 'ring buffer

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Martin Stransky <stransky@redhat.com> - 14:3.9.4-1
- new upstream

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> - 14:3.9.3-5
- rebuilt against new openssl

* Wed Nov  9 2005 Martin Stransky <stransky@redhat.com> - 14:3.9.3-4
- rebuilt

* Tue Aug  9 2005 Jeremy Katz <katzj@redhat.com> - 14:3.9.3-3
- remove explicit kernel dep for libpcap too

* Tue Jul 26 2005 Martin Stransky <stransky@redhat.com> - 14:3.9.3-2
- fixed typo in last patch

* Tue Jul 26 2005 Martin Stransky <stransky@redhat.com> - 14:3.9.3-1
- New upstream version - 3.9.3
- fix for #164227 (buffer overflow)
- fix for #164230 (missing debug info)

* Thu Jul 14 2005 Martin Stransky <stransky@redhat.com> - 14:3.9.1-1
- New upstream version

* Tue Jun 21 2005 Martin Stransky <stransky@redhat.com> - 14:3.8.2-14
- add shadow-utils to Prereq (#160643)

* Tue Jun  7 2005 Martin Stransky <stransky@redhat.com> - 14:3.8.2-13
- fix for CAN-2005-1267 - BGP DoS, #159209

* Thu Apr 28 2005 Martin Stransky <stransky@redhat.com> - 14:3.8.2-12
- fix for CAN-2005-1280 Multiple DoS issues in tcpdump
  (CAN-2005-1279 CAN-2005-1278), #156041

* Mon Mar 7 2005 Martin Stransky <stransky@redhat.com>
- rebuilt

* Mon Feb 14 2005 Martin Stransky <stransky@redhat.com> - 14:3.8.2-10
- remove explicit kernel dependecy (#146165)
- support for files larger than 2GB (#147840)

* Fri Feb 11 2005 Ivana Varekova <varekova@redhat.com> - 14:3.8.2-9
- added arpsnmp options to specify sender and recipient
  and corrected arpwatch and arpsnmp man pages (#70386)

* Thu Feb 10 2005 Ivana Varekova <varekova@redhat.com> - 14:3.8.2-8
- rebuilt

* Tue Oct 12 2004 Harald Hoyer <harald@redhat.com> - 14:3.8.2-7
- fixed nfs protocol parsing for 64 bit architectures (bug 132781)

* Wed Sep 15 2004 Harald Hoyer <harald@redhat.com> - 14:3.8.2-6
- added libpcap-0.8.3-ppp.patch for ppp (bug 128053)

* Wed Jun 23 2004 Elliot Lee <sopwith@redhat.com>
- added flex to BuildRequires

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun May 30 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- simplify rpm scripts

* Tue Apr  6 2004 Harald Hoyer <harald@redhat.com> - 14:3.8.2-3
- added LICENSE files

* Wed Mar 31 2004 Harald Hoyer <harald@redhat.com> - 14:3.8.2-2
- update to libpcap-0.8.3 (tcpdump-3.8.3 seems to be older that 3.8.2!!)

* Tue Mar 30 2004 Harald Hoyer <harald@redhat.com> - 14:3.8.2-1
- update to tcpdump-3.8.2, libpcap-0.8.2, arpwatch-2.1a13
- patched tcpdump configure for gcc34 optimizations
- removed obsolete patches

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 23 2004 Harald Hoyer <harald@redhat.de> 14:3.8.1-4/17
- fixed arpwatch version
- fixed libpcap library version
- fixed tcpdump droproot

* Tue Jan 20 2004 Harald Hoyer <harald@redhat.de> 14:3.8.1-3
- corrected tcpslice (bpf.h issue)

* Tue Jan 13 2004 Harald Hoyer <harald@redhat.de> 14:3.8.1-2
- more security issues (patch 18)

* Fri Jan 09 2004 Phil Knirsch <pknirsch@redhat.com> 14:3.8.1-1
- Updated to latest version because of security issue

* Fri Aug 29 2003 Harald Hoyer <harald@redhat.de> 14:3.7.2-7
- build libpcap shared library with gcc and not ld

* Tue Jul 22 2003 Phil Knirsch <pknirsch@redhat.com> 14:3.7.2-6.1
- rebuilt

* Mon Jul 21 2003 Phil Knirsch <pknirsch@redhat.com> 14:3.7.2-6
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 21 2003 Harald Hoyer <harald@redhat.de> 14:3.7.2-5
- add proper attributes for arp.dat, ethercodes

* Tue May 20 2003 Harald Hoyer <harald@redhat.de> 14:3.7.2-4
- take ethercodes.dat from the arpwatch package now

* Tue May  6 2003 Harald Hoyer <harald@redhat.de> 14:3.7.2-3
- compile tcpdump with autoheader #90208

* Thu May  1 2003 Elliot Lee <sopwith@redhat.com> 14:3.7.2-2
- Add sctpdef patch to fix ppc64 builds

* Thu Feb 27 2003 Phil Knirsch <pknirsch@redhat.com> 14:3.7.2-1
- Update to upstream version 3.7.2

* Sat Feb 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- sanitized rpm scripts

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 12:3.6.3-20
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 12:3.6.3-19/0.6.2-19/2.1a11-19
- rebuild

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 12:3.6.3-18/0.6.2-18/2.1a11-18
- set execute bits on library so that requires are generated.

* Wed Dec 11 2002 Harald Hoyer <harald@redhat.de> 12:3.6.3-17/0.6.2-17/2.1a11-17
- common release no. across all subpackages

* Wed Dec 11 2002 Harald Hoyer <harald@redhat.de> 12:3.6.3-5/0.6.2-16/2.1a11-16
- print_bgp security fix

* Mon Nov 18 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Fri Aug  2 2002 Harald Hoyer <harald@redhat.de> 12:3.6.3-3/0.6.2-16/2.1a11-16
- added man page descriptions for the new parameters

* Thu Aug  1 2002 Harald Hoyer <harald@redhat.de> 12:3.6.3-2
- added arpwatch options to specify sender and recipient (#70386)

* Tue Jul 23 2002 Harald Hoyer <harald@redhat.de> 12:3.6.3-1
- removed prestripping

* Thu May 16 2002 Harald Hoyer <harald@redhat.de> 12:3.6.2-13
- added official 3.6.3 fix
- fixed 6.2 compat #63113

* Wed Jan 23 2002 Harald Hoyer <harald@redhat.de> 12:3.6.2-12
- tcpdump-3.6.2-snaplen.patch added to fix #55145

* Tue Dec 18 2001 Harald Hoyer <harald@redhat.de> 12:3.6.2-10
- took old purge patch for filters
- fixed #54225,#58346
- drop root by default #49635
- fixed #54593
- fixed #57711

* Fri Aug 31 2001 Harald Hoyer <harald@redhat.de> 12:3.6.2-9
- took better fix for #52654 from tcpdump cvs

* Thu Aug 30 2001 Harald Hoyer <harald@redhat.de> 11:3.6.2-8
- fixed #52654

* Thu Jul 19 2001 Harald Hoyer <harald@redhat.de> 10:3.6.2-7
- added shared library to libpcap (#47174)
- afs printing security patch (#49294)

* Wed Jun 20 2001 Harald Hoyer <harald@redhat.de>
- use initgroups, instead of setgroups

* Mon Jun 18 2001 Harald Hoyer <harald@redhat.de>
- added dropgroup patches (#44563)

* Mon May 07 2001 Harald Hoyer <harald@redhat.de>
- switched to Pekka's tcpdump-3.6.2 package
- incremented epoch

* Sat Apr 14 2001 Pekka Savola <pekkas@netcore.fi>
- fix building of tcpslice on glibc 2.2.2 (time.h)
- disable /etc/init.d requirement and fix %%post scripts in arpwatch

* Wed Feb 14 2001 Harald Hoyer <harald@redhat.de>
- glibc sys/time -> time include patch

* Wed Feb  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add space to this check

* Wed Feb 07 2001 Harald Hoyer <harald@redhat.com>
- added check for presence of /etc/sysconfig/arpwatch (#23172)

* Wed Feb  7 2001 Pekka Savola <pekkas@netcore.fi>
- update to 3.6.2, 0.6.2 and new CVS of tcpslice.
- i18n'ize arpwatch init script

* Fri Feb  2 2001 Trond Eivind Glomsrød <teg@redhat.com>
- i18nize initscript

* Mon Jan 29 2001 Harald Hoyer <harald@redhat.com>
- fixed EINTR stopping for e.g. SIGSTOP. (#22008)
- added -u option for tcpdump (#20231)
- new arpwatch version (#23172)
- added "all" and "one" interface for -i (#20907)
- added arpwatch sysconfig (#23172)

* Mon Jan 22 2001 Harald Hoyer <harald@redhat.com>
- more (potential) overflows in libpcap. #21373
- documentation fix for #20906

* Sun Jan 14 2001 Pekka Savola <pekkas@netcore.fi>
- use --enable-ipv6
- Add two patches from CVS to enhance 802.2 printing, and more importantly,
  to be able to specify 'no stp'

* Sat Jan 13 2001 Pekka Savola <pekkas@netcore.fi>
- Make SMB printing output a lot more quiet unless in verbose mode.
- Make -n resolve port/protocol numbers but not hostnames, -nn for no
  resolving at all
- Separate droproot patch from a more generic man/usage fix one
- Add non-promiscuous mode -by default patch, but don't apply it by default

* Thu Jan 11 2001 Pekka Savola <pekkas@netcore.fi>
- Update to tcpdump 3.6.1 and libpcap 0.6.1 releases.

* Mon Jan  8 2001 Pekka Savola <pekkas@netcore.fi>
- Update to 20010108 CVS, disable some upstreamed patches.
- Change some additional .1 pages to .8.
- Add droproot patch, some --usage and man page fixes.

* Mon Jan  1 2001 Pekka Savola <pekkas@netcore.fi>
- Initial packaging with latest tcpdump.org CVS tcpdump-3.6 and libpcap-0.6.
- add earlier print-domain.c, the latest is segfaulting
- don't unnecesessarily include snprintf.o, it didn't compile with gcc 2.96 anyway
- don't use savestr, require openssl, tweak tweak tweak
- add tcpslice, patch it a bit for egcs detection

* Sun Dec 31 2000 Pekka Savola <pekkas@netcore.fi>
- tcpdump: spice up the manpage about interfaces
- tcpdump: add 'all' and 'any' keywords to -i, saner default behaviour.
- upgrade arpwatch to 2.1a10

* Sun Nov 26 2000 Jeff Johnson <jbj@redhat.com>
- more (potential) overflows in libpcap.

* Sun Nov 12 2000 Jeff Johnson <jbj@redhat.com>
- eliminate still more buffer overflows (from FreeBSD) (#20069).

* Thu Nov  2 2000 Jeff Johnson <jbj@redhat.com>
- eliminate more buffer overflows (from FreeBSD) (#20069).
- 802.1q ether type incorrect (#19850).
- add -u flag to drop arpwatch privs (#19696).

* Sun Oct 15 2000 Jeff Johnson <jbj@redhat.com>
- updated ethercodes.dat

* Thu Oct 12 2000 Jeff Johnson <jbj@redhat.com>
- fix arpwatch tmp race (#18943).

* Fri Aug 11 2000 Bill Nottingham <notting@redhat.com>
- fix condrestart

* Fri Aug 11 2000 Jeff Johnson <jbj@redhat.com>
- correct arpsnmp man pages (#15442).
- don't print harmless ENOPROTOOPT message (#13518).

* Fri Aug  4 2000 Jeff Johnson <jbj@redhat.com>
- rebuild with final kernel headers (#13518).

* Sat Jul 22 2000 Jeff Johnson <jbj@redhat.com>
- add STP patch (#14112).

* Fri Jul 14 2000 Matt Wilson <msw@redhat.com>
- source /etc/init.d/functions
- back out /etc/init.d/arpwatch, place file in /etc/rc.d
- move initscript to /etc/init.d
- changed initscript to use start() and stop() functions
- added condrestart to init script
- added %%post %%preun %%postun scripts to register arpwatch script
- added Prereq: for all things needed in post/preun/postun

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul 11 2000 Jeff Johnson <jbj@redhat.com>
- updated man page and help (pekkas@netcore.fi) (#10739 et al).

* Sun Jun 18 2000 Jeff Johnson <jbj@redhat/com>
- FHS packaging.

* Tue May  9 2000 Bill Nottingham <notting@redhat.com>
- minor tweaks for ia64 (prototypes)

* Thu Feb 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Compile shared libpcap with -fPIC (Bug #6342)

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix descriptions
- man pages are compressed

* Wed Dec 22 1999 Jeff Johnson <jbj@redhat.com>
- remove sparc64 SIOCGIFNAME hack, not needed with (at least) kernel 2.2.12-40.
- upgrade to ANK ss991030 snapshot with pcap magic fix (#6773).
- add getprotobyname lookup (#6725).
- getservbyname port lookup appears functional (#7569).
- remove uid 2090 backdoor (sorry Dave) (#7116).

* Thu Sep 09 1999 Cristian Gafton <gafton@redhat.com>
- fox the pcap.h header

* Fri Aug 20 1999 Jeff Johnson <jbj@redhat.com>
- prevent segfault on obscure spoofed ip header (#4634).

* Wed Aug 18 1999 Jeff Johnson <jbj@redhat.com>
- add defattr to arpwatch (#4591).

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Sun Aug  8 1999 Jeff Johnson <jbj@redhat.com>
- add -DWORDS_BIGINDIAN to tcpdump compile on sparc sparc61.

* Tue Aug  3 1999 Jeff Johnson <jbj@redhat.com>
- include A. Kuznetsov's patches to libpcap/tcpdump.
- added arpsnmp to package (#3258).
- arp2ethers written for different of awk (#4326).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 10)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- strip binaries.

* Wed Jan 13 1999 Bill Nottingham <notting@redhat.com>
- autoconf fixes for arm

* Tue Sep 29 1998 Jeff Johnson <jbj@redhat.com>
- libpcap description typo.

* Sat Sep 19 1998 Jeff Johnson <jbj@redhat.com>
- fix arpwatch summary line.

* Mon Aug 17 1998 Jeff Johnson <jbj@redhat.com>
- enable arpwatch

* Mon Aug  3 1998 Jeff Johnson <jbj@redhat.com>
- separate package for libpcap.
- update tcpdump to 3.4, libpcap to 0.4.
- added arpwatch (but disabled for now)

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat May  2 1998 Alan Cox <alan@rehat.com>
- Added the SACK printing fix so you can dump Linux 2.1+.

* Tue Oct 21 1997 Erik Troan <ewt@redhat.com>
- updated to release 3.4a5
- uses a buildroot and %%attr

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
