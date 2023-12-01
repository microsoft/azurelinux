Summary:        DNS proxy with integrated DHCP server
Name:           dnsmasq
Version:        2.89
Release:        2%{?dist}
License:        GPLv2 or GPLv3
Group:          System Environment/Daemons
URL:            https://www.thekelleys.org.uk/dnsmasq/
Source0:        https://www.thekelleys.org.uk/%{name}/%{name}-%{version}.tar.xz
Vendor:         Microsoft Corporation
Distribution:   Mariner
Patch0:         fix-missing-ioctl-SIOCGSTAMP-add-sockios-header-linux-5.2.patch
Patch1:         CVE-2023-28450.patch

BuildRequires:  kernel-headers

%description
Dnsmasq a lightweight, caching DNS proxy with integrated DHCP server.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_sharedstatedir}/dnsmasq
mkdir -p %{buildroot}%{_sysconfdir}/dnsmasq.d
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
mkdir -p %{buildroot}%{_bindir}
install src/dnsmasq %{buildroot}%{_sbindir}/dnsmasq
install dnsmasq.conf.example %{buildroot}%{_sysconfdir}/dnsmasq.conf
install dbus/dnsmasq.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/
install -m 644 man/dnsmasq.8 %{buildroot}%{_mandir}/man8/
install -D trust-anchors.conf %{buildroot}%{_datadir}/%{name}/trust-anchors.conf

install -m 755 contrib/wrt/lease_update.sh %{buildroot}%{_sbindir}/lease_update.sh

mkdir -p %{buildroot}/usr/lib/systemd/system
cat << EOF >> %{buildroot}/usr/lib/systemd/system/dnsmasq.service
[Unit]
Description=A lightweight, caching DNS proxy
After=network.target

[Service]
ExecStart=/usr/sbin/dnsmasq -k
Restart=always

[Install]
WantedBy=multi-user.target
EOF

%post

%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/systemd/*
%exclude %{_libdir}/debug
%{_sbindir}/*
%{_mandir}/*
%{_sysconfdir}/*
%dir %{_sharedstatedir}
%config  /usr/share/dnsmasq/trust-anchors.conf

%changelog
* Thu Mar 23 2023 Rohit Rawat <rohitrawat@microsoft.com> - 2.89-2
- Patch CVE-2023-28450

* Tue Mar 14 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.89-1
- Auto-upgrade to 2.89 - fix CVE-2021-45951 CVE-2021-45952 CVE-2021-45953 CVE-2021-45955 CVE-2021-45956 CVE-2021-45957 CVE-2022-0934

* Tue Mar 08 2022 Andrew Phelps <anphel@microsoft.com> - 2.86-1
- Upgrade to version 2.86

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.85-2
- Removing the explicit %%clean stage.

* Fri Apr 23 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.85-1
- Upgrade to version 2.85 to fix  CVE-2021-3348

* Thu Jan 28 2021 Henry Li <lihl@microsoft.com> - 2.84-1
- Upgrade to version 2.84
- Fix CVE-2020-25683, CVE-2020-25686, CVE-2020-25687
- Remove Patch CVE-2019-14834
- Use autosetup

* Thu Jun 18 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.79-11
- Removing runtime dependency on a specific kernel package.

* Thu Jun 11 2020 Christopher Co <chrco@microsoft.com> - 2.79-10
- Remove KERNEL_VERSION macro from BuildRequires

* Thu May 21 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.79-9
- Fix CVE-2019-14834

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.79-8
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.79-7
- Renaming linux-api-headers to kernel-headers

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.79-6
- Renaming linux to kernel

* Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.79-5
- Fixed "Source0" tag.
- Removed "%%define sha1".

* Mon Mar 23 2020 Christopher Co <chrco@microsoft.com> - 2.79-4
- Remove KERNEL_RELEASE macro from required packages

* Wed Jan 08 2020 Christopher Co <chrco@microsoft.com> - 2.79-3
- Fix missing SIOCGSTAMP ioctl definition due to linux 5.2 header refactor
- Verified License

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.79-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> - 2.79-1
- Upgrading to version 2.79

* Tue Feb 13 2018 Xiaolin Li <xiaolinl@vmware.com> - 2.76-5
- Fix CVE-2017-15107

* Mon Nov 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 2.76-4
- Always restart dnsmasq service on exit

* Wed Oct 11 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.76-3
- Fix CVE-2017-13704

* Wed Sep 27 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.76-2
- Fix CVE-2017-14491..CVE-2017-14496

* Sun Nov 27 2016 Vinay Kulkarni <kulkarniv@vmware.com> - 2.76-1
- Upgrade to 2.76 to address CVE-2015-8899

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.75-2
- GA - Bump release of all rpms

* Mon Apr 18 2016 Xiaolin Li <xiaolinl@vmware.com> - 2.75-1
- Initial version
