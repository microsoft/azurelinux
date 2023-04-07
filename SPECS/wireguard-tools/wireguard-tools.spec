Summary:        Fast, modern, secure VPN tunnel
Name:           wireguard-tools
Version:        1.0.20210914
Release:        4%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.wireguard.com/
Source0:        https://git.zx2c4.com/wireguard-tools/snapshot/wireguard-tools-%{version}.tar.xz
Source1:        %{name}.conf
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  systemd
%{?systemd_requires}

%description
WireGuard is a novel VPN that runs inside the Linux Kernel and uses
state-of-the-art cryptography (the "Noise" protocol). It aims to be
faster, simpler, leaner, and more useful than IPSec, while avoiding
the massive headache. It intends to be considerably more performant
than OpenVPN. WireGuard is designed as a general purpose VPN for
running on embedded interfaces and super computers alike, fit for
many different circumstances. It runs over UDP.

This package provides the wg binary for controlling WireGuard.

%prep
%autosetup -p1

%build
%{set_build_flags}
%make_build RUNSTATEDIR=%{_rundir} -C src

%install
%make_install BINDIR=%{_bindir} MANDIR=%{_mandir} RUNSTATEDIR=%{_rundir} \
WITH_BASHCOMPLETION=yes WITH_WGQUICK=yes WITH_SYSTEMDUNITS=yes -C src

# load wireguard module at every bootup
mkdir -p %{buildroot}%{_libdir}/modules-load.d
install -m755 %{SOURCE1} %{buildroot}%{_libdir}/modules-load.d/%{name}.conf

%post
# load wireguard module
%{_sbindir}/modprobe wireguard > /dev/null 2>&1

%preun
# Unload wireguard module
%{_sbindir}/modprobe -r wireguard > /dev/null 2>&1
# Remove module load conf file
%{_bindir}/rm -f %{_libdir}/modules-load.d/%{name}.conf

%files
%doc README.md contrib
%license COPYING
%{_bindir}/wg
%{_bindir}/wg-quick
%{_sysconfdir}/wireguard/
%{_datadir}/bash-completion/completions/wg
%{_datadir}/bash-completion/completions/wg-quick
%{_unitdir}/wg-quick@.service
%{_unitdir}/wg-quick.target
%{_libdir}/modules-load.d/%{name}.conf
%{_mandir}/man8/wg.8*
%{_mandir}/man8/wg-quick.8*

%changelog
* Sat Mar 25 2023 Sumedh Sharma <sumsharma@microsoft.com> - 1.0.20210914-4
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License verified

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.20210914-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.20210914-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 21 2021 Joe Doss <joe@solidadmin.com> - 1.0.20210914-1
- contrib/launchd: fix xml syntax error
- wg-quick: darwin: account for "link#XX" gateways
- ipc: add wireguard-nt support
- ipc: cache windows lookups to avoid O(n^2) with nested lookups
- ipc: remove windows elevation
- ipc: windows: don't display disabled adapters
- ipc: windows: use devpkey instead of nci for name
- wg-quick: android: adjust for android 12
- wg-quick: openbsd: set DNS with resolvd(8)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.20210424-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 30 2021 Joe Doss <joe@solidadmin.com> - 1.0.20210424-1
- wg-quick: freebsd: check for socket using -S, not -f
- wg-quick: freebsd: do not assume point-to-point interface flag
- wg-quick: freebsd: use ifconfig for determining if interface is up
- wg-quick: kill route monitor when loop terminates

* Mon Mar 15 2021 Joe Doss <joe@solidadmin.com> - 1.0.20210315-1
- Makefile: fix version indicator
- wireguard-tools: const correctness
- wireguard-tools: drag in headers for prototypes
- ipc: uniformly ignore preshared keys that are zero
- wg-quick: freebsd: add kernel support
- ipc: freebsd: add initial FreeBSD support
- wg-quick: freebsd: avoid writing private keys to /tmp

* Tue Feb 23 2021 Joe Doss <joe@solidadmin.com> - 1.0.20210223-1
- wg-quick: android: do not free iterated pointer
- wg-quick: openbsd: no use for userspace support
- embeddable-wg-library: sync latest from netlink.h
- wincompat: recent mingw has inet_ntop/inet_pton
- wincompat: add resource and manifest and enable lto
- wincompat: do not elevate by default
- completion: add help and syncconf completions
- sticky-sockets: do not use SO_REUSEADDR
- man: LOG_LEVEL variables changed name
- ipc: do not use fscanf with trailing \n
- ipc: read trailing responses after set operation

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.20200827-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 02 2020 Joe Doss <joe@solidadmin.com> - 1.0.20200827-2
- Disable contrib/dns-hatchet/apply.sh on Fedora 33+ and RHEL9+

* Sat Aug 29 2020 Joe Doss <joe@solidadmin.com> - 1.0.20200827-1
- Update to 1.0.20200827
- wg-quick: android: use iproute2 to bring up interface instead of ndc
- wg-quick: Revert wait on process substitutions

* Thu Aug 20 2020 Joe Doss <joe@solidadmin.com> - 1.0.20200820-1
- Update to 1.0.20200820
- ipc: split into separate files per-platform
- wincompat: fold random into genkey
- systemd: add reload target to systemd unit
- man: wg-quick: use syncconf instead of addconf for strip example
- pubkey: isblank is a subset of isspace
- ctype: use non-locale-specific ctype.h
- wg-quick: wait on process substitutions

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.20200513-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 13 2020 Joe Doss <joe@solidadmin.com> - 1.0.20200513-1
- Update to 1.0.20200513
- Makefile: remember to install all systemd units
- ipc: openbsd: switch to array ioctl interface

* Mon May 11 2020 Joe Doss <joe@solidadmin.com> - 1.0.20200510-1
- Update to 1.0.20200510
- ipc: add support for openbsd kernel implementation
- ipc: cleanup openbsd support
- wg-quick: add support for openbsd kernel implementation
- wg-quick: cleanup openbsd support
- wg-quick: support dns search domains
- Makefile: simplify silent cleaning
- ipc: remove extra space
- git: add gitattributes so tarball doesn't have gitignore files
- terminal: specialize color_mode to stdout only
- wg-quick: android: support application whitelist
- systemd: add wg-quick.target

* Wed Apr 15 2020 Leigh Scott <leigh123linux@gmail.com> - 1.0.20200319-2
- Add missing config directory
- Remove default buildroot BuildRequires
- Simplify doc install
- Remove commented lines
- Use correct macro for bash-completion

* Fri Mar 20 2020 Joe Doss <joe@solidadmin.com> - 1.0.20200319-1
- Update to 1.0.20200319

* Thu Feb 6 2020 Joe Doss <joe@solidadmin.com> - 1.0.20200206-1
- Update to 1.0.20200206
- Remove libmnl dependency

* Tue Jan 21 2020 Joe Doss <joe@solidadmin.com> - 1.0.20200121-1
- Update to 1.0.20200121
- Spec changes to pass Fedora RPM review

* Thu Jan 2 2020 Joe Doss <joe@solidadmin.com> - 1.0.20200102-1
- Update to 1.0.20200102
- Remove patch to fix dns-hatchet path

* Thu Dec 26 2019 Joe Doss <joe@solidadmin.com> - 1.0.20191226-1
- Update to 1.0.20191226
- Split wireguard-tools back into it's own spec file
- Add in patch to fix dns-hatchet path

* Mon Oct 14 2019 Joe Doss <joe@solidadmin.com> - 0.0.20191012-1
- Update to 0.0.20191012

* Mon Sep 16 2019 Joe Doss <joe@solidadmin.com> - 0.0.20190913-1
- Update to 0.0.20190913

* Mon Sep 9 2019 Joe Doss <joe@solidadmin.com> - 0.0.20190905-1
- Update to 0.0.20190905

* Tue Jul 2 2019 Joe Doss <joe@solidadmin.com> - 0.0.20190702-1
- Update to 0.0.20190702

* Sat Jun 1 2019 Joe Doss <joe@solidadmin.com> - 0.0.20190601-1
- Update to 0.0.20190601

* Fri May 31 2019 Joe Doss <joe@solidadmin.com> - 0.0.20190531-1
- Update to 0.0.20190531

* Sat Apr 6 2019 Joe Doss <joe@solidadmin.com> - 0.0.20190406-1
- Update to 0.0.20190406

* Wed Feb 27 2019 Joe Doss <joe@solidadmin.com> - 0.0.20190227-1
- Update to 0.0.20190227

* Thu Jan 24 2019 Joe Doss <joe@solidadmin.com> - 0.0.20190123-1
- Update to 0.0.20190123

* Wed Dec 19 2018 Joe Doss <joe@solidadmin.com> - 0.0.20181218-1
- Update to 0.0.20181218

* Thu Nov 15 2018 Joe Doss <joe@solidadmin.com> - 0.0.20181115-1
- Update to 0.0.20181115

* Sun Oct 14 2018 Joe Doss <joe@solidadmin.com> - 0.0.20181018-1
- Update to 0.0.20181018

* Sun Oct 14 2018 Joe Doss <joe@solidadmin.com> - 0.0.20181007-2
- Add make as a build dependency

* Sun Oct 7 2018 Joe Doss <joe@solidadmin.com> - 0.0.20181007-1
- Update to 0.0.20181007

* Tue Sep 25 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180925-1
- Update to 0.0.20180925

* Tue Sep 18 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180918-2
- Add BuildRequires gcc to fix builds on F29 and Rawhide

* Tue Sep 18 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180918-1
- Update to 0.0.20180918

* Mon Sep 10 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180910-1
- Update to 0.0.20180910

* Wed Sep 5 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180904-1
- Update to 0.0.20180904

* Thu Aug 9 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180809-1
- Update to 0.0.20180809

* Sun Aug 5 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180802-1
- Update to 0.0.20180802

* Wed Jul 18 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180718-1
- Update to 0.0.20180718

* Tue Jul 10 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180708-1
- Update to 0.0.20180708

* Fri Jun 29 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180625-1
- Update to 0.0.20180625

* Wed Jun 20 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180620-1
- Update to 0.0.20180620

* Wed Jun 13 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180613-1
- Update to 0.0.20180613

* Wed May 30 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180531-1
- Update to 0.0.20180531

* Wed May 23 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180524-1
- Update to 0.0.20180524

* Thu May 17 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180519-1
- Update to 0.0.20180519

* Sun May 13 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180513-1
- Update to 0.0.20180513
- Drop support for RHEL 7.4, moving on instead to RHEL 7.5

* Fri Apr 20 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180420-1
- Update to 0.0.20180420

* Sun Apr 15 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180413-1
- Update to 0.0.20180413

* Mon Mar 05 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180304-1
- Update to 0.0.20180304

* Mon Feb 19 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180218-1
- Update to 0.0.20180218

* Sun Feb 04 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180202-1
- Update to 0.0.20180202

* Thu Jan 18 2018 Joe Doss <joe@solidadmin.com> - 0.0.20180118-1
- Update to 0.0.20180118

* Thu Dec 21 2017 Joe Doss <joe@solidadmin.com> - 0.0.20171221-1
- Update to 0.0.20171221

* Tue Dec 12 2017 Joe Doss <joe@solidadmin.com> - 0.0.20171211-1
- Update to 0.0.20171211

* Mon Nov 27 2017 Joe Doss <joe@solidadmin.com> - 0.0.20171127-1
- Update to 0.0.20171127

* Thu Nov 23 2017 Joe Doss <joe@solidadmin.com> - 0.0.20171122-1
- Update to 0.0.20171122

* Sat Nov 11 2017 Joe Doss <joe@solidadmin.com> - 0.0.20171111-1
- Update to 0.0.20171111

* Wed Nov 01 2017 Joe Doss <joe@solidadmin.com> - 0.0.20171101-1
- Update to 0.0.20171101
- Add temporary DNS hatchet to wg-quick

* Thu Oct 26 2017 Joe Doss <joe@solidadmin.com> - 0.0.20171017-1
- Update to 0.0.20171017

* Wed Oct 11 2017 Joe Doss <joe@solidadmin.com> - 0.0.20171011-1
- Update to 0.0.20171011

* Fri Oct 6 2017 Joe Doss <joe@solidadmin.com> - 0.0.20171005-1
- Update to 0.0.20171005
- Update RPM spec URL to www.wireguard.com

* Mon Oct 2 2017 Joe Doss <joe@solidadmin.com> - 0.0.20171001-1
- Update to 0.0.20171001

* Mon Sep 18 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170918-1
- Update to 0.0.20170918
- Drop support for RHEL 7.3, moving on instead to RHEL 7.4.

* Thu Sep 7 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170907-1
- Update to 0.0.20170907

* Wed Aug 9 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170810-1
- Update to 0.0.20170810

* Mon Jul 31 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170726-1
- Update to 0.0.20170726

* Thu Jun 29 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170629-1
- Update to 0.0.20170629

* Tue Jun 13 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170613-1
- Update to 0.0.20170613

* Mon Jun 12 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170612-1
- Update to 0.0.20170612

* Wed May 31 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170531-1
- Update to 0.0.20170531

* Wed May 17 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170517-1
- Update to 0.0.20170517

* Mon Apr 24 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170421-1
- Update to 0.0.20170421

* Mon Apr 10 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170409-1
- Update to 0.0.20170409

* Fri Mar 24 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170324-1
- Update to 0.0.20170324

* Mon Mar 20 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170320.1-1
- Update to 0.0.20170320.1

* Thu Mar 2 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170223-1
- Update to 0.0.20170223

* Thu Feb 16 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170214-1
- Update to 0.0.20170214

* Thu Jan 5 2017 Joe Doss <joe@solidadmin.com> - 0.0.20170105-1
- Update to 0.0.20170105
- Add wg-quick, bash-completion, and systemd service

* Mon Dec 19 2016 Jason A. Donenfeld <jason@zx2c4.com> - 0.0.20161218-1
- Spec adjustments

* Wed Aug 17 2016 Joe Doss <joe@solidadmin.com> - 0.0.20160808-2
- Spec adjustments

* Mon Aug 15 2016 Joe Doss <joe@solidadmin.com> - 0.0.20160808-1
- Initial WireGuard Tools RPM
- Version 0.0.20160808
