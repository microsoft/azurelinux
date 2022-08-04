Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:        A console-based network monitoring utility
Name:           iptraf-ng
Version:        1.2.1
Release:        1%{?dist}
Source0:        https://github.com/iptraf-ng/iptraf-ng/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-logrotate.conf
Source2:        %{name}-tmpfiles.conf
URL:            https://github.com/iptraf-ng/iptraf-ng/
License:        GPLv2+
BuildRequires:  gcc
BuildRequires:  ncurses-devel
Obsoletes:      iptraf < 3.1
Provides:       iptraf = 3.1

%description
IPTraf-ng is a console-based network monitoring utility.  IPTraf gathers
data like TCP connection packet and byte counts, interface statistics
and activity indicators, TCP/UDP traffic breakdowns, and LAN station
packet and byte counts.  IPTraf-ng features include an IP traffic monitor
which shows TCP flag information, packet and byte counts, ICMP
details, OSPF packet types, and oversized IP packet warnings;
interface statistics showing IP, TCP, UDP, ICMP, non-IP and other IP
packet counts, IP checksum errors, interface activity and packet size
counts; a TCP and UDP service monitor showing counts of incoming and
outgoing packets for common TCP and UDP application ports, a LAN
statistics module that discovers active hosts and displays statistics
about their activity; TCP, UDP and other protocol display filters so
you can view just the traffic you want; logging; support for Ethernet,
FDDI, ISDN, SLIP, PPP, and loopback interfaces; and utilization of the
built-in raw socket interface of the Linux kernel, so it can be used
on a wide variety of supported network cards.

%prep
%autosetup

%build
make %{?_smp_mflags} V=1 \
  CFLAGS="-g -O2 -Wall -W -std=gnu99 -Werror=format-security %{optflags}" \
  LDFLAGS="$RPM_LD_FLAGS"

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} prefix=%{_prefix}

# remove everything besides the html and pictures in Documentation
find Documentation -type f | grep -v '\.html$\|\.png$\|/stylesheet' | \
     xargs rm -f

install -D -m 0644 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/iptraf-ng

install -d -m 0755 %{buildroot}%{_localstatedir}/{log,lib}/iptraf-ng

mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d
install -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf

mkdir -p %{buildroot}/run
install -d -m 0755 %{buildroot}/run/%{name}/

%files
%doc CHANGES FAQ LICENSE README*
%doc Documentation
%{_sbindir}/iptraf-ng
%{_mandir}/man8/iptraf-ng.8*
%{_localstatedir}/log/iptraf-ng
%{_localstatedir}/lib/iptraf-ng
%config(noreplace) %{_sysconfdir}/logrotate.d/iptraf-ng
%dir /run/%{name}/
%{_prefix}/lib/tmpfiles.d/%{name}.conf

%changelog
* Tue Jun 21 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.2.1-1
- Upgrading to fix build break and align with latest ncurses update.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.4-25
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 11 2019 Phil Cameron <pcameron@redhat.com> - 1.1.4-22
- add test case
  Resolves: 1682317

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 16 2018 Phil Cameron <pcameron@redhat.com> - 1.1.4-20
- add BuildRequires: gcc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb  1 2018 Florian Weimer <fweimer@redhat.com> - 1.1.4-17
- Build with linker flags from redhat-rpm-config

* Mon Jan 22 2018 Phil Cameron <pcameron@redhat.com> - 1.1.4-16
- Moved upstream from https://fedorahosted.org/iptraf-ng/ to 
  https://github.com/iptraf-ng/iptraf-ng/ with release v1.1.4
  Fixes error in patch Patch03 - this fixes 1283773

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Apr 17 2016 Alejandro Pérez  <aeperezt@fedoraproject.org> - 1.1.4-12
- Added sources and clean tree
* Fri Apr 15 2016 Phil Cameron <pcameron@redhat.com> - 1.1.4-11
- fix 1283773
  bugfix-positionptr-properly-allocate-newly-create
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Alejandro Pérez  <aeperezt@fedoraproject.org> - 1.1.4-7
- fix 1109768
  bad configuration logrotate
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
* Sun Mar 02 2014 Alejandro Pérez  <aeperezt@fedoraproject.org> - 1.1.4-5
- fix bug 1020552
  rpm report /var/lock/ipraf-ng is missing
  fix dates on changelog
  added missing file iptraf-nf-tmpfiles.conf
* Tue Dec 03 2013 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.4-4
- iptraf-ng-1.1.4-4

  Fedora start using -Werror=format-security and iptraf-ng had some
  parts where error compilation was trigged.

  202b2e7b27a1 Makefile: add -Werror=format-security

  Resolved: #1037133

* Mon Sep 02 2013 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.4-3
- 9b32013 BUGFIX: fix "Floating point exception" in tcplog_flowrate_msg() (Vitezslav Samel)
  
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.4
- new upstream iptraf-ng-1.1.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.3.1-2
- append standard CFLAGS

* Wed May 23 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.3.1-1
- new upstream iptraf-ng-1.1.3.1-1

* Fri May 04 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.2-1
- new upstream iptraf-ng-1.1.2-1

* Fri Apr 27 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.2.rc0-1
- new upstream iptraf-ng-1.1.2.rc0-1

* Thu Feb 02 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.1-1
- new upstream iptraf-ng-1.1.1

* Sun Jan 16 2011 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.0-2
- fix wrongly used execl

* Tue Jan 11 2011 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.0-1
- Initialization build
