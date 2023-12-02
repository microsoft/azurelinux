Summary:        HA monitor built upon LVS, VRRP and services poller
Name:           keepalived
Version:        2.2.8
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.keepalived.org/
Source0:        https://www.keepalived.org/software/%{name}-%{version}.tar.gz
Source1:        %{name}.service

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  ipset-devel
BuildRequires:  iptables-devel
BuildRequires:  kernel-headers
BuildRequires:  libmnl-devel
BuildRequires:  libnfnetlink-devel
BuildRequires:  libnl3-devel
BuildRequires:  net-snmp-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  systemd
BuildRequires:  unzip

Requires:       iptables
Requires:       kmod
Requires:       libnl3-devel
Requires:       net-snmp
Requires:       openssl
Requires:       systemd

%description
The main goal of the keepalived project is to add a strong & robust keepalive
facility to the Linux Virtual Server project. This project is written in C with
multilayer TCP/IP stack checks. Keepalived implements a framework based on
three family checks : Layer3, Layer4 & Layer5/7. This framework gives the
daemon the ability to check the state of an LVS server pool. When one of the
servers of the LVS server pool is down, keepalived informs the linux kernel via
a setsockopt call to remove this server entry from the LVS topology. In
addition keepalived implements an independent VRRPv2 stack to handle director
failover. So in short keepalived is a userspace daemon for LVS cluster nodes
healthchecks and LVS directors failover.

%prep
%setup -q

%build
autoreconf -f -i
%configure \
    --with-systemdsystemunitdir=%{_unitdir} \
    --disable-nftables  \
    --enable-snmp       \
    --enable-snmp-rfc   \
    --with-init=systemd
make %{?_smp_mflags} STRIP=/bin/true

%install
make install DESTDIR=%{buildroot}
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
mkdir -p doc_install/samples
cp doc/keepalived.conf.SYNOPSIS doc_install
cp doc/samples/* doc_install/samples
rm -f doc_install/samples/*.pem
rm -rf %{buildroot}%{_sysconfdir}/rc.d/init.d/
rm -rf %{buildroot}%{_sysconfdir}/%{name}/samples/*
mkdir -p %{buildroot}%{_libexecdir}/keepalived
# After keepalived v2.2.4 we stopped installing a default keepalived.conf and instead install
# keepalived.conf.sample.
mv %{buildroot}/etc/keepalived/keepalived.conf.sample %{buildroot}/etc/keepalived/keepalived.conf

%check
# A build could silently have LVS support disabled if the kernel includes can't
# be properly found, we need to avoid that.
if ! grep -q "#define _WITH_LVS_ *1" lib/config.h; then
    %{__echo} "ERROR: We do not want keepalived lacking LVS support."
    exit 1
fi

%post
/sbin/ldconfig
%systemd_post keepalived.service

%preun
%systemd_preun keepalived.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart keepalived.service

%files
%defattr(-, root, root, -)
%license COPYING
%doc AUTHOR ChangeLog CONTRIBUTORS README TODO
%doc doc_install/*
%dir %{_sysconfdir}/keepalived/
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/keepalived/keepalived.conf
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/keepalived
%{_unitdir}/keepalived.service
%{_datadir}/snmp/mibs/KEEPALIVED-MIB.txt
%{_datadir}/snmp/mibs/VRRP-MIB.txt
%{_datadir}/snmp/mibs/VRRPv3-MIB.txt
%{_bindir}/genhash
%attr(0755,root,root) %{_sbindir}/keepalived
%{_mandir}/man1/genhash.1*
%{_mandir}/man5/keepalived.conf.5*
%{_mandir}/man8/keepalived.8*

%changelog
* Mon Nov 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.2.8-1
- Auto-upgrade to 2.2.8 - Azure Linux 3.0 - package upgrades

* Tue Feb 08 2022 Cameron Baird <cameronbaird@microsoft.com> - 2.2.7-1
- Update source to v2.2.7
- Using Fedora 36 spec (license: MIT) for guidance.
- Using spec shipped with source (license: GPLv2) for guidance.

* Thu Apr 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.10-6
- Adding an explicit run-time dependency on 'net-snmp'.
- Bumping up release number to link against newer version of 'net-snmp' libraries.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.0.10-5
- Added %%license line automatically

* Thu Apr 30 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.0.10-4
- Rename libnl to libnl3.

* Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> 2.0.10-3
- Verified license. Removed sha1. Fixed Source0 URL. URL to https. dded note about alternate source location.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.0.10-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Feb 15 2019 Ashwin H <ashwinh@vmware.com> 2.0.10-1
- Updated to version 2.0.10

* Wed Sep 12 2018 Ankit Jain <ankitja@vmware.com> 2.0.7-1
- Updated to version 2.0.7

* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 1.3.5-2
- Add iptables-devel to BuildRequires

* Thu Apr 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.3.5-1
- Initial build.  First version
