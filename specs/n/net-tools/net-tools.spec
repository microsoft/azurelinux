# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global checkout 20160912git

Summary: Basic networking tools
Name: net-tools
Version: 2.0
Release: 0.74.%{checkout}%{?dist}
License: GPL-2.0-or-later
URL: http://sourceforge.net/projects/net-tools/

# git archive --format=tar --remote=git://git.code.sf.net/p/net-tools/code master | xz > net-tools-%%{version}.%%{checkout}.tar.xz
Source0: net-tools-%{version}.%{checkout}.tar.xz
Source1: net-tools-config.h
Source2: net-tools-config.make
Source3: ether-wake.c
Source4: ether-wake.8
Source5: mii-diag.c
Source6: mii-diag.8
Source7: iptunnel.8
Source8: ipmaddr.8
Source9: arp-ethers.service

# adds <delay> option that allows netstat to cycle printing through statistics every delay seconds.
Patch1: net-tools-cycle.patch

# various man page fixes merged into one patch
Patch2: net-tools-man.patch

# linux-4.8
Patch3: net-tools-linux48.patch

# use all interfaces instead of default (#1003875)
Patch20: ether-wake-interfaces.patch

# use all interfaces instead of default (#1003875)
Patch21: net-tools-ifconfig-EiB.patch
Patch22: net-tools-timer-man.patch
Patch23: net-tools-interface-name-len.patch
Patch24: net-tools-correct-exit-code.patch
Patch25: net-tools-spelling-error.patch
Patch26: net-tools-route-inet6-output.patch
Patch27: net-tools-iface-name-too-long.patch

BuildRequires: make
BuildRequires: bluez-libs-devel
BuildRequires: gettext, libselinux
BuildRequires: libselinux-devel
BuildRequires: systemd
BuildRequires: gcc
%{?systemd_requires}

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires:       filesystem(unmerged-sbin-symlinks)
Provides:       /usr/sbin/ifconfig
%endif

%description
The net-tools package contains basic networking tools,
including ifconfig, netstat, route, and others.
Most of them are obsolete. For replacement check iproute package.

%prep
%setup -q -c
%patch -P1 -p1 -b .cycle
%patch -P2 -p1 -b .man
%patch -P3 -p1 -b .linux48

cp %SOURCE1 ./config.h
cp %SOURCE2 ./config.make
cp %SOURCE3 .
cp %SOURCE4 ./man/en_US
cp %SOURCE5 .
cp %SOURCE6 ./man/en_US
cp %SOURCE7 ./man/en_US
cp %SOURCE8 ./man/en_US

%patch -P20 -p1 -b .interfaces
%patch -P21 -p1 -b .ifconfig-EiB
%patch -P22 -p1 -b .timer-man
%patch -P23 -p1 -b .interface-name-len
%patch -P24 -p1 -b .exit-codes
%patch -P25 -p1 -b .spelling
%patch -P26 -p1 -b .inet6-output
%patch -P27 -p1 -b .iface-name-too-long

touch ./config.h

%build
# Sparc and s390 arches need to use -fPIE
%ifarch sparcv9 sparc64 s390 s390x
export CFLAGS="${RPM_OPT_FLAGS} -fPIE"
%else
export CFLAGS="${RPM_OPT_FLAGS} -fpie"
%endif
# RHBZ #853193
export LDFLAGS="${RPM_LD_FLAGS} -pie -Wl,-z,now"

make
make ether-wake
gcc ${RPM_OPT_FLAGS} ${RPM_LD_FLAGS} -o mii-diag mii-diag.c

%install
mv man/de_DE man/de
mv man/fr_FR man/fr
mv man/pt_BR man/pt

make BASEDIR=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} install

%if "%{_sbindir}" != "%{_bindir}"
# ifconfig and route are installed into /usr/bin by default
# mv them back to /usr/sbin (#1045445)
mv %{buildroot}%{_bindir}/ifconfig %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/route %{buildroot}%{_sbindir}
%endif

install -p -m 755 ether-wake %{buildroot}%{_sbindir}
install -p -m 755 mii-diag %{buildroot}%{_sbindir}

rm %{buildroot}%{_sbindir}/rarp
rm %{buildroot}%{_mandir}/man8/rarp.8*
rm %{buildroot}%{_mandir}/de/man8/rarp.8*
rm %{buildroot}%{_mandir}/fr/man8/rarp.8*
rm %{buildroot}%{_mandir}/pt/man8/rarp.8*

# otherwise %%find_lang finds them even they're empty
rm -rf %{buildroot}%{_mandir}/de/man1
rm -rf %{buildroot}%{_mandir}/fr/man1
rm -rf %{buildroot}%{_mandir}/man1
rm -rf %{buildroot}%{_mandir}/pt/man1
rm -rf %{buildroot}%{_mandir}/pt/man5

# install systemd unit file
install -D -p -m 644 %{SOURCE9} %{buildroot}%{_unitdir}/arp-ethers.service

%find_lang %{name} --all-name --with-man

%post
%systemd_post arp-ethers.service

%files -f %{name}.lang
%license COPYING
%{_bindir}/netstat
%{_sbindir}/ifconfig
%{_sbindir}/route
%{_sbindir}/arp
%{_sbindir}/ether-wake
%{_sbindir}/ipmaddr
%{_sbindir}/iptunnel
%{_sbindir}/mii-diag
%{_sbindir}/mii-tool
%{_sbindir}/nameif
%{_sbindir}/plipconfig
%{_sbindir}/slattach
%{_mandir}/man[58]/*

%attr(0644,root,root)   %{_unitdir}/arp-ethers.service

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.74.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.73.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0-0.72.20160912git
- Rebuilt for the bin-sbin merge (2nd attempt)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.71.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0-0.70.20160912git
- Rebuilt for the bin-sbin merge

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.69.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.68.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.67.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Mar 20 2023 Michal Ruprich <mruprich@redhat.com> - 2.0-0.66.20160912git
- SPDX migration

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.65.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 23 2022 Michal Ruprich <mruprich@redhat.com> - 2.0-0.64.20160912git
- Resolves: #2077846 - net-tools utilities display incorrect statistics for interfaces with 15-character names

* Wed Aug 03 2022 Michal Ruprich <mruprich@redhat.com> - 2.0-0.63.20160912git
- Resolves: #2114821 - The output of `route -A inet6` does not display properly when the 'Use' column output is over 6 digits

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.62.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.61.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.60.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.59.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 06 2020 Michal Ruprich <michalruprich@gmail.com> - 2.0-0.58.20160912git
- Resolves: #1835155 - netstat says "packetes" instead of "packets"

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.57.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.56.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.55.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 06 2019 Michal Ruprich <mruprich@redhat.com> - 2.0-0.54.20160912git
- Resolves: #1670779 - Exit code on wrong parameter is zero for many net-tools binaries

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.53.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Michal Ruprich <mruprich@redhat.com> - 2.0-0.52.20160912git
- Resolves: #1604937 - net-tools: FTBFS in Fedora rawhide

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.51.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 25 2018 Michal Ruprich <mruprich@redhat.com> - 2.0-0.50.20160912git
- Resolves: 1557470 - netstat -i cut's interface names
- Resolves: 1566084 - netstat -agn only shows 10 character interface name for IPv4 addressing

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0-0.49.20160912git
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.48.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb  1 2018 Florian Weimer <fweimer@redhat.com> - 2.0-0.47.20160912git
- Link mii-diag with $RPM_LD_FLAGS

* Tue Jan 30 2018 Michal Ruprich <mruprich@redhat.com> - 2.0-0.46.20160912git
- removing dependencies on systemd-units from spec file

* Fri Nov 24 2017 Michal Ruprich <mruprich@redhat.com> - 2.0-0.45.20160912git
- Resolves: #1478868 - netstat(8) portion on Timer needs writing

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.44.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.43.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.42.20160912git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Michal Ruprich <mruprich@redhat.com> - 2.0-0.41.20160912git
- Resolves: #1414765 - ifconfig inaccurately rounds exabytes

* Wed Oct 12 2016 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.40.20160912git
- fix build on linux-4.8

* Mon Sep 12 2016 mruprich <mruprich@redhat.com> - 2.0-0.39.20160912git
- latest upstream snapshot

* Wed Mar 30 2016 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.38.20160329git
- just few nitpicks :)

* Tue Mar 29 2016 Zdenek Dohnal <zdohnal@redhat.com> - 2.0-0.37.20160329git
- latest upstream snapshot
- adding HAVE_PLIP_TOOLS=1, HAVE_SERIAL_TOOLS=1, HAVE_ARP_TOOLS=1 into net-tools-config.h and net-tools-config.make
- commenting out "%%{buildroot}%%{_mandir}/man8/rarp.8*" and its language alternatives in spec
- adding "rm -rf %%{buildroot}%%{_mandir}/pt/man5" in spec

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.36.20150915git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 15 2015 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.35.20150915git
- ether-wake: add interface into message (#1149502)
- latest upstream snapshot (ipx.patch & sctp-statistics.patch merged)

* Wed Jul 15 2015 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.34.20150715git
- latest upstream snapshot

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.33.20150416git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 16 2015 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.32.20150416git
- latest upstream snapshot

* Mon Nov 24 2014 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.31.20141124git
- latest upstream snapshot (#1162284)

* Thu Nov 20 2014 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.30.20141007git
- ether-wake: apply Debian's hardening patch

* Tue Oct 07 2014 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.29.20141007git
- latest upstream snapshot (#1149405)

* Fri Oct 03 2014 Lubomir Rintel <lkundrak@v3.sk> - 2.0-0.28.20140707git
- Enable bluetooth

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.27.20140707git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.0-0.26.20140707git
- fix license handling

* Mon Jul 07 2014 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.25.20140707git
- latest upstream snapshot

* Tue Jun 10 2014 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.24.20131119git
- __global_ldflags -> RPM_LD_FLAGS, optflags -> RPM_OPT_FLAGS

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.23.20131119git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Jaromír Končický <jkoncick@redhat.com> - 2.0-0.22.20131119git
- output sctp endpoints without -a parameter (#1063913)

* Fri Feb 14 2014 Jaromír Končický <jkoncick@redhat.com> - 2.0-0.21.20131119git
- remake sctp-quiet.patch (#1063906#c7)

* Tue Feb 11 2014 Jaromír Končický <jkoncick@redhat.com> - 2.0-0.20.20131119git
- make sctp quiet on systems without sctp (#1063906)

* Fri Dec 20 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.19.20131119git
- move ifconfig and route back to sbin (#1045445)

* Tue Dec 03 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.18.20131119git
- make mii-diag compile with -Werror=format-security (#1037218)

* Tue Nov 19 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.17.20131119git
- latest snapshot (#1021109)

* Fri Nov 01 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.16.20131004git
- use different compiler/linker flags macros

* Thu Oct 10 2013 Jaromír Končický <jkoncick@redhat.com> - 2.0-0.15.20131004git
- install binaries into /usr/bin and /usr/sbin (#1016674)

* Fri Oct 04 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.14.20131004git
- latest snapshot

* Mon Sep 23 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.13.20130910git
- remove %%ifarch alpha condition from %%prep
- improve sctp-statistics.patch (#982638#c10)

* Tue Sep 10 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.12.20130910git
- latest snapshot

* Wed Sep 04 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.11.20130607git
- amend ether-wake-interfaces.patch

* Wed Sep 04 2013 Jaromír Končický <jkoncick@redhat.com> - 2.0-0.10.20130607git
- use all interfaces instead of default (#1003875)
- reverted all changes on ether-wake.c and put original file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.9.20130607git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.8.20130607git
- latest snapshot

* Thu Apr 25 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.7.20130425git
- latest snapshot

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.6.20130109git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 09 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.5.20130109git
- latest snapshot (#579855)

* Fri Nov 30 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.4.20121106git
- fix URL

* Fri Nov 16 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.3.20121106git
- match actual license

* Tue Nov 06 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.2.20121106git
- few man page fixes

* Thu Oct 04 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0-0.1.20121004git
- the git snapshot we ship is actually much more a
  2.0 pre-release then 1.60 post-release

* Mon Oct 01 2012 Jiri Popelka <jpopelka@redhat.com> - 1.60-145.20120917git
- compile without STRIP (Metricom radio) support

* Mon Sep 17 2012 Jiri Popelka <jpopelka@redhat.com> - 1.60-144.20120917git
- upstream git snapshot

* Wed Sep 05 2012 Jiri Popelka <jpopelka@redhat.com> - 1.60-143.20120702git
- Sparc and s390 arches need to use -fPIE

* Wed Sep 05 2012 Jiri Popelka <jpopelka@redhat.com> - 1.60-142.20120702git
- compile with PIE and full RELRO flags (#853193)

* Wed Aug 22 2012 Jiri Popelka <jpopelka@redhat.com> - 1.60-141.20120702git
- fixed building with kernel-3.6

* Wed Aug 22 2012 Jiri Popelka <jpopelka@redhat.com> - 1.60-140.20120702git
- use new systemd-rpm macros (#850225)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.60-139.20120702git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 02 2012 Jiri Popelka <jpopelka@redhat.com> - 1.60-138.20120702git
- fixes for #834110 and #836258 merged upstream

* Wed Jun 20 2012 Jiri Popelka <jpopelka@redhat.com> - 1.60-137.20120509git
- compile without Token ring support (http://lwn.net/Articles/497397/)

* Tue Jun 19 2012 Jiri Popelka <jpopelka@redhat.com> - 1.60-136.20120509git
- better SCTP support (#826676)

* Wed May 09 2012 Jiri Popelka <jpopelka@redhat.com> - 1.60-135.20120509git
- don't require hostname package

* Fri Jan 27 2012 Jiri Popelka <jpopelka@redhat.com> - 1.60-134.20120127git
- Do not show interface metric in 'ifconfig', 'ifconfig -s' and 'netstat -i'.
  Spare place is used for interface name so trim_iface.patch is no longer needed.
- No need to convert man pages to utf-8 as upstream ship them in utf-8 now.

* Thu Jan 19 2012 Jiri Popelka <jpopelka@redhat.com> - 1.60-133.20120119git
- SELinux patch merged upstream
- several page fixes merged upstream
- mark localized man pages with %%lang

* Wed Jan 11 2012 Jiri Popelka <jpopelka@redhat.com> - 1.60-132.20120111git
- 3 patches merged upstream
- removed 2digit.patch (#718610)
- removed fgets.patch (probably not needed anymore)

* Thu Jan 05 2012 Jiri Popelka <jpopelka@redhat.com> - 1.60-131.20120105git
- next 11 patches merged upstream
- removed bcast.patch (seems to be fixed upstream)
- removed netstat-p-basename.patch (upstream is not happy with it)
- netstat-leak.patch merged into duplicate-tcp.patch

* Wed Dec 07 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-130.20111207git
- removed virtualname.patch
- added back isofix.patch
- improved mii-registers.patch

* Tue Dec 06 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-129.20111206git
- upstream git snapshot
- reduced number of patches from 95 to 32
- netstat -T/--notrim option is now -W/--wide

* Tue Oct 25 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-128
- Removed HFI support.
- Improved num-ports.patch

* Thu Oct 20 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-127
- Merge all upstream fixes into net-tools-1.60-upstream.patch

* Tue Oct 18 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-126
- Upstream is migrating to Sourceforge.

* Mon Oct 03 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-125
- Fixed ether-wake(8) and mii-diag(8) man pages (#742629)

* Mon Sep 19 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-124
- Improved arp-ethers.service unit file (#735617)

* Wed Aug 24 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-123
- Improved netstat_stop_trim.patch to not truncate IPV6 UDP sockets (#732984)

* Mon Jul 04 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-122
- Update for 2 digit Linux version numbers (#718610)

* Fri Jun 17 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-121
- Added arp-ethers.service systemd unit file to run 'arp -f /etc/ethers'
  on startup of system. Don't ship default /etc/ethers (#713759)

* Wed May 25 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-120
- Do not mention /proc/net/socket in ifconfig(8) (#661905)
- Merge all 'man page only fix' patches into net-tools-1.60-man.patch

* Thu Apr 28 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-119
- Fix possible problems found by static analysis of code.

* Thu Apr 21 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-118
- patch netstat to separate basename of -p only if it is absolute
  path (in order to make argv[0]="sshd pty/0" display as sshd, and not as /0).

* Thu Apr 14 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-117
- plipconfig man page and usage output fixes. (#694766)

* Mon Mar 07 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-116
- Fix mii-tool/mii-diag/ether-wake to not default to eth0 because
  since Fedora 15 network devices can have arbitrary names (#682367)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.60-115
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-114
- Improve scanf-format.patch (#668047)

* Fri Jan 21 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-113
- Improve route(8) man page saying that 'route mss' actually sets MTU (#671321)

* Mon Jan 03 2011 Jiri Popelka <jpopelka@redhat.com> - 1.60-112
- Fix the handling of some of the HAVE_* flags ifdef vs if. (BerliOS #17812)

* Thu Dec 16 2010 Jiri Popelka <jpopelka@redhat.com> - 1.60-111
- fixed mii-diag(8) man page (#663689)
- fixed route(8) man page (#664171)

* Thu Dec 16 2010 Jiri Popelka <jpopelka@redhat.com> - 1.60-110
- fixed ifconfig(8) man page (#663469)

* Wed Nov 17 2010 Jiri Popelka <jpopelka@redhat.com> - 1.60-109
- improved netstat(8) man page (#614931)

* Mon Nov 01 2010 Jiri Popelka <jpopelka@redhat.com> - 1.60-108
- added netstat(8) support for RcvbufErrors, SndbufErrors (BerliOS #17645)

* Wed Sep 29 2010 jkeating - 1.60-107
- Rebuilt for gcc bug 634757

* Thu Sep 16 2010  Jiri Popelka <jpopelka@redhat.com> - 1.60-106
- HFI support

* Thu Sep 16 2010  Jiri Popelka <jpopelka@redhat.com> - 1.60-105
- fixed memory leak in netstat when run with -c option

* Tue Aug 10 2010  Jiri Popelka <jpopelka@redhat.com> - 1.60-104
- improved statistics-doubleword.patch (Bug #579854)

* Mon Jun 14 2010  Jiri Popelka <jpopelka@redhat.com> - 1.60-103
- updated mii-tool to support gigabit links (#539575)

* Wed Apr  7 2010  Jiri Popelka <jpopelka@redhat.com> - 1.60-102
- fixed statistics.c to use unsigned long long (instead of int) to handle 64 bit integers (Bug #579854, Debian #561161)
- fixed typo in statistics.c (Bug #579855)

* Sat Jan  2 2010  Jiri Popelka <jpopelka@redhat.com> - 1.60-101
- fixed overflow patch (#551625)
- ifconfig interface:0 del <IP> will remove the Aliased IP on IA64 (#473211)
- interface slip: cast keepalive/outfill to unsigned long to fix warnings on 64bit hosts -- no functional changes since these only have an 8bit range anyways
- interface: fix IPv6 parsing of interfaces with large indexes (> 255) (Debian #433543)

* Mon Dec 21 2009  Jiri Popelka <jpopelka@redhat.com> - 1.60-100
- Move hostname to separate package

* Thu Dec  3 2009  Jiri Popelka <jpopelka@redhat.com> - 1.60-99
- return defining of BuildRoot even it's no longer necessary
  (https://fedoraproject.org/wiki/Packaging:Guidelines#BuildRoot_tag)
  to silent rpmlint false warning

* Wed Nov  4 2009  Jiri Popelka <jpopelka@redhat.com> - 1.60-98
- in mii-tool.c use <linux/mii.h> instead of "mii.h" and fix Bug #491358

* Thu Oct 29 2009  Jiri Popelka <jpopelka@redhat.com> - 1.60-97
- Make "hostname -s" display host name cut at the first dot (no
  matter if the host name resolves or not) (bug #531702)

* Wed Sep 30 2009  Jiri Popelka <jpopelka@redhat.com> - 1.60-96
- netplug moved to separate package
- #319981 and #322901 - minor man pages changes
- applied changes from berlios cvs, which fix: Berlios #16232, Gentoo #283759 and polish Makefile and slattach 

* Tue Sep 1 2009  Jiri Popelka <jpopelka@redhat.com> - 1.60-95
- netstat - avoid name resolution for listening or established sockets (-l) by return fast. 
- netstat - --continuous should flush stdout
- added missing man pages (iptunnel, ipmaddr, netplug, netplug.d, netplugd.conf)
- added note about obsolete commands to existing man pages 
- let the user know that ifconfig can correctly show only first 8 bytes of Infiniband hw address

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.60-94
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  8 2009  Jiri Popelka <jpopelka@redhat.com> - 1.60-93
- scanf format length fix (non exploitable?) from Fabian Hugelshofer <hugelshofer2006@gmx.ch>
- URL tag changed to http://net-tools.berlios.de/

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.60-92
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 16 2008 Zdenek Prikryl <zprikryl@redhat.com> - 1.60-91
- fixed tcp timers info in netstat (#466845)

* Thu Sep 25 2008 Zdenek Prikryl <zprikryl@redhat.com> - 1.60-90
- fixed ifconfig's man page (#454271, #432328)

* Tue Jul 15 2008 Zdenek Prikryl <zprikryl@redhat.com> - 1.60-89
- fixed man pages for arp (#446195)
- fixed netstat --interfaces option (#446187)
- fixed clearing flags in ifconfig (#450252)

* Tue Jul  8 2008 Radek Vokál <rvokal@redhat.com> - 1.60-88
- netstat displays correct sctp statistics (#445535) <zprikryl@redhat.com>

* Tue Mar  4 2008 Radek Vokál <rvokal@redhat.com> - 1.60-87
- fix buffer for newer kernels (#435554)

* Mon Feb 25 2008 Radek Vokal <rvokal@redhat.com> - 1.60-86
- fix for GCC 4.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.60-85
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Radek Vokál <rvokal@redhat.com> - 1.60-84
- rebuilt

* Fri Jun  8 2007 Radek Vokál <rvokal@redhat.com> - 1.60-83
- fix netplugd init script (#242919)

* Tue May 22 2007 Radek Vokál <rvokal@redhat.com> - 1.60-82
- better SELinux patch by <dwalsh@redhat.com>

* Tue Mar 27 2007 Radek Vokál <rvokal@redhat.com> - 1.60-81
- fix segfault for empty interface (#234045)

* Thu Mar 15 2007 Radek Vokál <rvokal@redhat.com> - 1.60-80
- we don't have -n/--node option (#225554)

* Thu Feb 22 2007 Radek Vokál <rvokal@redhat.com> - 1.60-79
- quiet sctp (#229232)

* Mon Feb 19 2007 Radek Vokál <rvokal@redhat.com> - 1.60-78
- spec file cleanup (#226193)

* Tue Jan 30 2007 Radek Vokál <rvokal@redhat.com> - 1.60-77
- touch /etc/ethers (#225381)

* Wed Dec 27 2006 Radek Vokál <rvokal@redhat.com> - 1.60-76
- fix arp unaligned access (#220438)

* Wed Oct  4 2006 Radek Vokal <rvokal@redhat.com> - 1.60-75
- fix nameif crash for 16char long interface names (#209120)

* Mon Oct  2 2006 Radek Vokal <rvokal@redhat.com> - 1.60-74
- fix -I option for nestat, works as -I=eth0 again.
- add dist tag

* Mon Aug  7 2006 Radek Vokal <rvokal@redhat.com> - 1.60-73
- directory entries . and .. should be skipped

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.60-72.1
- rebuild

* Wed Jun  7 2006 Radek Vokal <rvokal@redhat.com> - 1.60-72
- switch --trim to --notrim .. make it less confusing 

* Fri May 19 2006 Radek Vokal <rvokal@redhat.com> - 1.60-71
- BuildRequires: libselinux-devel (#191737)

* Tue May 09 2006 Radek Vokál <rvokal@redhat.com> - 1.60-70
- add netdevice.h, fix x25
- fix ifconfig crash when interface name is too long (#190703)

* Tue May 02 2006 Radek Vokál <rvokal@redhat.com> - 1.60-69
- fix arp man page to correspond to man ethers (#190425)

* Fri Apr 14 2006 Radek Vokál <rvokal@redhat.com> - 1.60-68
- display sctp connections using netstat -S <jbj@redhat.com>

* Thu Apr 13 2006 Radek Vokál <rvokal@redhat.com> - 1.60-67
- fix wrong definition of _PATH_PROCNET_X25_ROUTE (#188786)

* Thu Apr 06 2006 Radek Vokál <rvokal@redhat.com> - 1.60-66
- add note about -T to netstat

* Thu Mar 30 2006 Radek Vokál <rvokal@redhat.com> - 1.60-65
- add note to ifconfig(8) about supported format for IPv4 addresses (#176661)

* Thu Mar 16 2006 Radek Vokál <rvokal@redhat.com> - 1.60-64
- remove duplicate arp entries (#185604)

* Thu Feb 23 2006 Radek Vokál <rvokal@redhat.com> - 1.60-63
- show inodes in netstat (#180974)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.60-62.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Radek Vokál <rvokal@redhat.com> - 1.60-62
- new option for netstat - -T stops trimming remote and local addresses (#176465)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.60-61.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Radek Vokál <rvokal@redhat.com> 1.60-61
- mii-tool manpage fixed (#180055)

* Tue Jan 17 2006 Radek Vokal <rvokal@redhat.com> 1.60-60
- forget to enable the new selinux option :( - config.make changed

* Tue Jan 17 2006 Radek Vokal <rvokal@redhat.com> 1.60-59
- new option for nestat, -Z shows selinux context. Patch by <dwalsh@redhat.com>

* Mon Jan 02 2006 Radek Vokal <rvokal@redhat.com> 1.60-58
- clear static buffers in interface.c by <drepper@redhat.com> (#176714)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Oct 15 2005 Radek Vokal <rvokal@redhat.com> 1.60-57
- add note to hostname man page about gethostbyname() (#166581)
- don't ship any rarp man page (#170537)

* Wed Aug 03 2005 Radek Vokal <rvokal@redhat.com> 1.60-56
- fixed buffer overflow in arp (#164695)

* Wed Jul 20 2005 Radek Vokal <rvokal@redhat.com> 1.60-55
- ifconfig - fixed virtual interface dropping (#162888)

* Wed Jun 22 2005 Radek Vokal <rvokal@redhat.com> 1.60-54
- fr man pages are back (#159702)

* Mon Jun 06 2005 Radek Vokal <rvokal@redhat.com> 1.60-53
- etherwake man page changed to ether-wake (#159156)

* Tue Apr 26 2005 Radek Vokal <rvokal@redhat.com> 1.60-52
- don't show "duplicate line" warning (#143933)
- netstat has new statistcs (#133032)
- /etc/neplug is owned by net-tools (#130621)

* Tue Apr 05 2005 Radek Vokal <rvokal@redhat.com> 1.60-51
- flush output in mii-tool (#152568)

* Wed Mar 30 2005 Radek Vokal <rvokal@redhat.com> 1.60-50
- added mii-diag tool
- added newer ether-wake
- remove useless -i option from ifconfig
- stop trimming interface names (#152457)

* Wed Mar 16 2005 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 01 2005 Radek Vokal <rvokal@redhat.com> 1.60-48
- behaviour of netstat -i option changed (#115987)
- netstat -i shows all interface, -I<Iface> only one

* Mon Feb 28 2005 Radek Vokal <rvokal@redhat.com> 1.60-47
- added RPM_OPT_FLAGS
- execshield patch for netplug <t8m@redhat.com>

* Wed Feb 16 2005 Radek Vokal <rvokal@redhat.com> 1.60-46
- small typo in german translation (#148775)

* Wed Feb 09 2005 Radek Vokal <rvokal@redhat.com> 1.60-45
- included infiniband support (#147396) <tduffy@sun.com>
- added etherwake man page

* Mon Feb 07 2005 Radek Vokal <rvokal@redhat.com> 1.60-44
- net-plug-1.2.9 - no changes, upstream included Red Hat patches
- ether-wake-1.08 - few changes in implementation (#145718)

* Mon Jan 10 2005 Radek Vokal <rvokal@redhat.com> 1.60-43
- don't report statistics for virtual devices (#143981) <kzak@redhat.com>
- fixing translation headers - content type format
- kill bitkeeper warning messages

* Fri Dec 03 2004 Radek Vokal <rvokal@redhat.com> 1.60-42
- filter out duplicate tcp entries (#139407)

* Thu Nov 25 2004 Radek Vokal <rvokal@redhat.com> 1.60-41
- added note to hostname(1) (#140239)
- fixed --num-ports option for netstat (#115100)

* Thu Nov 11 2004 Radek Vokal <rvokal@redhat.com> 1.60-40
- mii-tool(8) fixed, labeled as obsolete, added info (#138687)
- netstat crashing on i64 fixed (#138804) Patch by <Andreas.Hirstius@cern.ch>

* Thu Nov 04 2004 Radek Vokal <rvokal@redhat.com> 1.60-39
- IBM patch for netstat -s returning negative values on 64bit arch (#144064)
- broadcast calulated if only netmask provided (#60509)

* Tue Nov 02 2004 Radek Vokal <rvokal@redhat.com> 1.60-38
- fixed fail to assign the specified netmask before adress is assigned
- patch by Malita, Florin <florin.malita@glenayre.com>

* Wed Sep 29 2004 Radek Vokal <rvokal@redhat.com> 1.60-37
- spec file updated, added conversion for french and portugal man pages to UTF-8

* Mon Sep 06 2004 Radek Vokal <rvokal@redhat.com> 1.60-36
- parse error fixed (#131539)

* Fri Sep 03 2004 Radek Vokal <rvokal@redhat.com> 1.60-35
- The return value of nameif was wrong (#129032) - patch from Fujitsu QA 

* Mon Aug 30 2004 Radek Vokal <rvokal@redhat.com> 1.60-34
- Trunc patch added (#128359)

* Mon Aug 30 2004 Radek Vokal <rvokal@redhat.com> 1.60-33
- Added patch for SI units by Tom "spot" Callaway <tcallawa@redhat.com> #118006

* Tue Aug 17 2004 Phil Knirsch <pknirsch@redhat.com> 1.60-32
- Fix installopts for netplug.

* Sun Aug 08 2004 Alan Cox <alan@redhat.com> 1.60-31
- Build requires gettext.

* Mon Aug 02 2004 Phil Knirsch <pknirsch@redhat.com> 1.60-30
- Update to latest netplugd version.

* Mon Jul 12 2004 Phil Knirsch <pknirsch@redhat.com> 1.60-29
- Fixed initscript patch for netplug (#127351)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 14 2004 Phil Knirsch <pknirsch@redhat.com> 1.60-27
- Fixed compiler warning/error in netplug.
- Updated to netplug-1.2.6 for security update and fixes.

* Thu May 06 2004 Phil Knirsch <pknirsch@redhat.com> 1.60-26
- Updated netplugd to latest upstream version.
- Fixed execshield problem in main.c of netplugd.

* Thu Apr 15 2004 Phil Knirsch <pknirsch@redhat.com> 1.60-25
- Fixed several possible buffer overflows (#120343)

* Tue Mar 30 2004 Harald Hoyer <harald@redhat.com> - 1.60-24
- fixed compilation with gcc34

* Tue Mar 23 2004 Karsten Hopp <karsten@redhat.de> 1.60-23 
- add chkconfig call in post and preun, fix init script (#116555)

* Thu Feb 19 2004 Phil Knirsch <pknirsch@redhat.com>
- Added netplug-1.2.1 to net-tools (FR #103419).

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Aug 25 2003 Phil Knirsch <pknirsch@redhat.com> 1.60-20.1
-rebuilt

* Mon Aug 25 2003 Phil Knirsch <pknirsch@redhat.com> 1.60-20
- interface option now works as described in the man page (#61113).

* Tue Aug 19 2003 Phil Knirsch <pknirsch@redhat.com> 1.60-19.1
- rebuilt

* Tue Aug 19 2003 Phil Knirsch <pknirsch@redhat.com> 1.60-19
- Fixed trailing blank bug in hostname output (#101263).
- Remove -O2 fir alpha (#78955).
- Updated netstat statistic output, was still broken.

* Tue Jun 17 2003 Phil Knirsch <pknirsch@redhat.com> 1.60-18.1
- rebuilt

* Tue Jun 17 2003 Phil Knirsch <pknirsch@redhat.com> 1.60-18
- fix ether-wake.c build with gcc 3.3
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Phil Knirsch <pknirsch@redhat.com> 1.60-16.1
- Bumped release and rebuilt

* Fri May 23 2003 Phil Knirsch <pknirsch@redhat.com> 1.60-16
- Fixed ether-wake usage output (#55801).

* Thu May 22 2003 Jeremy Katz <katzj@redhat.com> 1.60-15
- fix build with gcc 3.3

* Thu May 22 2003 Phil Knirsch <pknirsch@redhat.com> 1.60-14
- Fixed wrong manpage (#55473).

* Wed May 21 2003 Phil Knirsch <pknirsch@redhat.com>
- Added inet6-lookup patch from John van Krieken (#84108).
- Fixed outdated link in ifconfig manpage (#91287).

* Tue May 20 2003 Phil Knirsch <pknirsch@redhat.com>
- Fixed incorrect address display for ipx (#46434).
- Fixed wrongly installed manpage dirs (#50664).

* Wed Mar 19 2003 Phil Knirsch <pknirsch@redhat.com> 1.60-13
- Fixed nameif problem (#85748).

* Fri Feb 07 2003 Phil Knirsch <pknirsch@redhat.com> 1.60-12
- Fixed -s parameter.
- Fix /proc statistics for -nic operation.
- Fixed -i operation in general.

* Mon Jan 27 2003 Phil Knirsch <pknirsch@redhat.com> 1.60-11
- Disable smp build.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 1.60-10
- rebuilt

* Tue Dec 17 2002 Phil Knirsch <pknirsch@redhat.com> 1.60-9
- Rebuild
- Copyright -> License.

* Thu Dec 05 2002 Elliot Lee <sopwith@redhat.com> 1.60-8
- Rebuild

* Tue Aug 06 2002 Phil Knirsch <pknirsch@redhat.com> 
- Added patch from Norm for a corrected output.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Apr 12 2002 Jeremy Katz <katzj@redhat.com>
- fix nstrcmp() to be correct in the case where there are many devices 
  of the same type, eg, "eth10" > "eth1"  (#61436)

* Tue Jul 31 2001 Bill Nottingham <notting@redhat.com>
- do *not* use SIOCDEVPRIVATE for MII ioctls

* Fri Jun  1 2001 Preston Brown <pbrown@redhat.com>
- include wake-on-lan wakeup utility, ether-wake by Donald Becker

* Wed Apr 18 2001 Crutcher Dunnavant <crutcher@redhat.com>
- itterate to 1.60

* Sun Apr  8 2001 Preston Brown <pbrown@redhat.com>
- use find_lang macro
- less specific locale dirs for man pages

* Mon Apr  2 2001 Preston Brown <pbrown@redhat.com>
- don't use this version of rarp, doesn't work with our 2.4.

* Tue Feb  6 2001 Crutcher Dunnavant <crutcher@redhat.com>
- fixed man page typo, closing bug #25921

* Thu Feb  1 2001 Crutcher Dunnavant <crutcher@redhat.com>
- applied twaugh's patch to close bug #25474
- which was a buffer length bug.

* Wed Dec 27 2000 Jeff Johnson <jbj@redhat.com>
- locales not initialized correctly (#20570).
- arp: document -e option (#22040).

* Sat Oct  7 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.57.
- MTU (and other) option(s) not parsed correctly (#9215).
- allow more granularity iwth --numeric (#9129).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun  6 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.56.
- FHS packaging.

* Sat Apr 15 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.55.

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Fri Jan 14 2000 Jeff Johnson <jbj@redhat.com>
- fix "netstat -ci" (#6904).
- document more netstat options (#7429).

* Thu Jan 13 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.54.
- enable "everything but DECnet" including IPv6.

* Sun Aug 29 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.53.

* Wed Jul 28 1999 Jeff Johnson <jbj@redhat.com>
- plug "netstat -c" fd leak (#3620).

* Thu Jun 17 1999 Jeff Johnson <jbj@redhat.com>
- plug potential buffer overruns.

* Sat Jun 12 1999 John Hardin <jhardin@wolfenet.com>
- patch to recognize ESP and GRE protocols for VPN masquerade

* Fri Apr 23 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.52.

* Thu Mar 25 1999 Jeff Johnson <jbj@redhat.com>
- update interface statistics continuously (#1323)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.51.
- strip binaries.

* Tue Feb  2 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.50.
- added slattach/plipconfig/ipmaddr/iptunnel commands.
- enabled translated man pages.

* Tue Dec 15 1998 Jakub Jelinek <jj@ultra.linux.cz>
- update to 1.49.

* Sat Dec  5 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.48.

* Thu Nov 12 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.47.

* Wed Sep  2 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.46

* Thu Jul  9 1998 Jeff Johnson <jbj@redhat.com>
- build root
- include ethers.5

* Thu Jun 11 1998 Aron Griffis <agriffis@coat.com>
- upgraded to 1.45
- patched hostname.c to initialize buffer
- patched ax25.c to use kernel headers

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Feb 27 1998 Jason Spangler <jasons@usemail.com>
- added config patch

* Fri Feb 27 1998 Jason Spangler <jasons@usemail.com>
- changed to net-tools 1.432
- removed old glibc 2.1 patch
 
* Wed Oct 22 1997 Erik Troan <ewt@redhat.com>
- added extra patches for glibc 2.1

* Tue Oct 21 1997 Erik Troan <ewt@redhat.com>
- included complete set of network protocols (some were removed for
  initial glibc work)

* Wed Sep 03 1997 Erik Troan <ewt@redhat.com>
- updated glibc patch for glibc 2.0.5

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- updated to 1.33
