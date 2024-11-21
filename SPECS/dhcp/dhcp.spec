Summary:        Dynamic host configuration protocol
Name:           dhcp
Version:        4.4.3
Release:        2%{?dist}
License:        MPLv2.0
Url:            https://www.isc.org/dhcp/
Source0:        ftp://ftp.isc.org/isc/dhcp/%{version}/%{name}-%{version}.tar.gz
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
BuildRequires:  systemd
%description
The ISC DHCP package contains both the client and server programs for DHCP. dhclient (the client) is used for connecting to a network which uses DHCP to assign network addresses. dhcpd (the server) is used for assigning network addresses on private networks

%package libs
Summary:    Libraries for dhcp
%description libs
Libraries for the dhcp.

%package devel
Summary:    Development Libraries and header files for dhcp
Requires:   dhcp-libs
%description devel
Headers and libraries for the dhcp.

%package server
Summary:    Provides the ISC DHCP server
Requires:   dhcp-libs
%description server
dhcpd is the name of a program that operates as a daemon on a server to provide Dynamic Host Configuration Protocol (DHCP) service to a network. Clients may solicit an IP address (IP) from a DHCP server when they need one

%package client
Summary:	Provides the ISC DHCP client daemon and dhclient-script
Requires:	dhcp-libs
Provides:	dhclient
%description client
The ISC DHCP Client, dhclient, provides a means for configuring one or more network interfaces using the Dynamic Host Configuration Protocol, BOOTP protocol, or if these protocols fail, by statically assigning an address.


%prep
%autosetup -p1

%build
CFLAGS="$CFLAGS \
        -D_PATH_DHCLIENT_SCRIPT='\"/sbin/dhclient-script\"' \
        -D_PATH_DHCPD_CONF='\"/etc/dhcp/dhcpd.conf\"' \
        -D_PATH_DHCLIENT_CONF='\"/etc/dhcp/dhclient.conf\"'" \
./configure \
    --prefix=%{_prefix} \
    --sysconfdir=/etc/dhcp                                  \
    --localstatedir=/var                                    \
    --with-srv-lease-file=/var/lib/dhcpd/dhcpd.leases       \
    --with-srv6-lease-file=/var/lib/dhcpd/dhcpd6.leases     \
    --with-cli-lease-file=/var/lib/dhclient/dhclient.leases \
    --with-cli6-lease-file=/var/lib/dhclient/dhclient6.leases \
    --with-srv-pid-file=%{_localstatedir}/run/dhcpd.pid \
    --with-srv6-pid-file=%{_localstatedir}/run/dhcpd6.pid \
    --with-cli-pid-file=%{_localstatedir}/run/dhclient.pid \
    --with-cli6-pid-file=%{_localstatedir}/run/dhclient6.pid \
    --with-relay-pid-file=%{_localstatedir}/run/dhcrelay.pid \
    --enable-log-pid \
    --enable-paranoia --enable-early-chroot

make
%install
make DESTDIR=%{buildroot} install
install -v -m755 client/scripts/linux %{buildroot}/usr/sbin/dhclient-script

cat > %{buildroot}/etc/dhcp/dhclient.conf << "EOF"
# Begin /etc/dhcp/dhclient.conf
#
# Basic dhclient.conf(5)

option rfc3442-classless-static-routes code 121 = array of unsigned integer 8;

#prepend domain-name-servers 127.0.0.1;
request subnet-mask, broadcast-address, time-offset, routers,
        domain-name, domain-name-servers, domain-search, host-name,
        netbios-name-servers, netbios-scope, interface-mtu,
        ntp-servers;
require subnet-mask, domain-name-servers;
#timeout 60;
#retry 60;
#reboot 10;
#select-timeout 5;
#initial-interval 2;

# End /etc/dhcp/dhclient.conf
EOF
install -v -dm 755 %{buildroot}/usr/lib/systemd/system
cat > %{buildroot}/usr/lib/systemd/system/dhcp.service << "EOF"
[Unit]
Description=ISC DHCP Server
Documentation=man:dhcpd(8) man:dhcpd.conf(5)
After=network.target

[Service]
EnvironmentFile=/etc/default/dhcpd
ExecStart=/usr/sbin/dhcpd -f --no-pid $DHCPD_OPTS

[Install]
WantedBy=multi-user.target
EOF

install -v -dm 755 %{buildroot}%{_localstatedir}/lib/dhclient
install -v -dm 755 %{buildroot}%{_sysconfdir}/default
cat > %{buildroot}%{_sysconfdir}/default/dhcpd << "EOF"
DHCPD_OPTS=
EOF

mkdir -p %{buildroot}%{_sysconfdir}/dhcp
touch %{buildroot}%{_sysconfdir}/dhcp/dhcpd.conf
touch %{buildroot}%{_sysconfdir}/dhcp/dhcpd6.conf

mkdir -p %{buildroot}%{_localstatedir}/lib/dhcpd/
touch %{buildroot}%{_localstatedir}/lib/dhcpd/dhcpd.leases
touch %{buildroot}%{_localstatedir}/lib/dhcpd/dhcpd6.leases
mkdir -p %{buildroot}%{_localstatedir}/lib/dhclient/

#%check
#Commented out %check due to missing support of ATF.

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%defattr(-,root,root)
%license LICENSE
%{_libdir}/libdhcp*.a
%{_libdir}/libomapi.a

%files devel
%defattr(-,root,root)
%{_includedir}/dhcpctl
%{_includedir}/omapip

%files server
%defattr(-,root,root)
%dir %{_sysconfdir}/dhcp
%dir %{_localstatedir}/lib/dhcpd
%{_sysconfdir}/dhcp/dhcpd.conf.example
%config(noreplace) %{_sysconfdir}/default/dhcpd
%config(noreplace) %{_sysconfdir}/dhcp/dhcpd.conf
%config(noreplace) %{_sysconfdir}/dhcp/dhcpd6.conf
%config(noreplace) %{_localstatedir}/lib/dhcpd/dhcpd.leases
%config(noreplace) %{_localstatedir}/lib/dhcpd/dhcpd6.leases
%{_bindir}/omshell
%{_sbindir}/dhcpd
%{_sbindir}/dhcrelay
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/dhcp-eval.5.gz
%{_mandir}/man5/dhcp-options.5.gz
%{_mandir}/man5/dhcpd.conf.5.gz
%{_mandir}/man5/dhcpd.leases.5.gz
%{_mandir}/man8/dhcpd.8.gz
%{_mandir}/man8/dhcrelay.8.gz
/usr/lib/systemd/system/dhcp.service

%files client
%defattr(-,root,root)
%dir %{_sysconfdir}/dhcp
%{_sysconfdir}/dhcp/dhclient.conf.example
%config(noreplace) %{_sysconfdir}/dhcp/dhclient.conf
%{_sbindir}/dhclient
%{_sbindir}/dhclient-script
%dir %{_localstatedir}/lib/dhclient
%{_mandir}/man5/dhclient.conf.5.gz
%{_mandir}/man5/dhclient.leases.5.gz
%{_mandir}/man8/dhclient-script.8.gz
%{_mandir}/man8/dhclient.8.gz

%changelog
* Fri Mar 08 2024 Chris Patterson <cpatterson@microsoft.com> - 4.4.3-2
- Add option for classless static route configuration in dhclient.conf

* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.4.3-1
- Auto-upgrade to 4.4.3 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 4.4.2-6
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Jul 28 2023 Suresh Thelkar <sthelkar@microsoft.com> - 4.4.2-5
- Fix a bug in applying earlier patches.

* Wed Nov 10 2021 Pawel Winogrodzki <pawel.winogrodzki@microsoft.com> - 4.4.2-4
- Modified "CFLAGS" to include CBL-Mariner defaults.

* Tue Jun 08 2021 Muhammad Falak Wani <mwani@microsoft.com> 4.4.2-3
- Add an explicit provides for dhclient.

* Wed May 26 2021 Jon Slobodzian <joslobo@microsoft.com> 4.4.2-2
- Patch to fix CVE-2021-25217.

* Thu May 28 2020 Nicolas Ontiveros <niontive@microsoft.com> 4.4.2-1
- Update to version 4.4.2, which fixes CVE-2017-3144 and CVE-2018-5733.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 4.3.6-2
- Added %%license line automatically

* Thu Mar 26 2020 Nicolas Ontiveros <niontive@microsoft.com> 4.3.6-1
- Update version to 4.3.6. License verified. URL updated.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.3.5-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jul 05 2017 Chang Lee <changlee@vmware.com> 4.3.5-4
- Commented out %check due to missing support of ATF.

* Thu Apr 20 2017 Divya Thaluru <dthaluru@vmware.com> 4.3.5-3
- Added default dhcp configuration and lease files

* Wed Dec 7 2016 Divya Thaluru <dthaluru@vmware.com> 4.3.5-2
- Added configuration file for dhcp service

* Mon Nov 14 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.3.5-1
- Upgraded to version 4.3.5.

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 4.3.3-4
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.3.3-3
- GA - Bump release of all rpms

* Wed Mar 30 2016 Anish Swaminathan <anishs@vmware.com>  4.3.3-2
- Add patch for CVE-2016-2774

* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 4.3.3-1
- Updated to version 4.3.3

* Wed Jul 15 2015 Divya Thaluru <dthaluru@vmware.com> 4.3.2-1
- Initial build.
