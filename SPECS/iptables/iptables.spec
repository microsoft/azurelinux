Summary:        Linux kernel packet control tool
Name:           iptables
Version:        1.8.7
Release:        5%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://www.netfilter.org/projects/iptables
Source0:        http://www.netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2
Source1:        iptables.service
Source2:        iptables
Source3:        iptables.stop
Source4:        ip4save
Source5:        ip6save
BuildRequires:  jansson-devel
BuildRequires:  libmnl-devel
BuildRequires:  libnftnl-devel
BuildRequires:  systemd-bootstrap-rpm-macros
Requires:       iana-etc
Requires:       systemd
Provides:       %{name}-services = %{version}-%{release}

%description
The next part of this chapter deals with firewalls. The principal
firewall tool for Linux is Iptables. You will need to install
Iptables if you intend on using any form of a firewall.

%package        devel
Summary:        Header and development files for iptables
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications.

%prep
%autosetup

%build
%configure \
    --disable-silent-rules \
    --exec-prefix= \
    --with-xtlibdir=%{_libdir}/iptables \
    --with-pkgconfigdir=%{_libdir}/pkgconfig \
    --disable-nftables \
    --enable-libipq \
    --enable-devel

make V=0

%install
%make_install
ln -sfv ../../sbin/xtables-multi %{buildroot}%{_libdir}/iptables-xml
#   Install daemon scripts
install -vdm755 %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -vdm755 %{buildroot}%{_sysconfdir}/systemd/scripts
install -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/systemd/scripts
install -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/systemd/scripts
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/systemd/scripts
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/systemd/scripts

find %{buildroot} -name '*.a'  -delete
find %{buildroot} -type f -name "*.la" -delete -print
%{_fixperms} %{buildroot}/*

%preun
%systemd_preun iptables.service

%post
/sbin/ldconfig
%systemd_post iptables.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart iptables.service

%files
%defattr(-,root,root)
%license COPYING
%config(noreplace) %{_sysconfdir}/systemd/scripts/iptables
%config(noreplace) %{_sysconfdir}/systemd/scripts/iptables.stop
%config(noreplace) %{_sysconfdir}/systemd/scripts/ip4save
%config(noreplace) %{_sysconfdir}/systemd/scripts/ip6save
%{_unitdir}/iptables.service
%{_sbindir}/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/iptables/*
%{_libdir}/iptables-xml
%{_mandir}/man1/*
%{_mandir}/man8/*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Thu Jan 25 18:31:11 EST 2024 Dan Streetman <ddstreet@ieee.org> - 1.8.7-5
- use bootstrap to avoid "circular deps"

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.8.7-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Jun 08 2023 Andy Zaugg <azaugg@linkedin.com> - 1.8.7-3
- Removed icmpv6 redirect iptables rule and disabled redirect kernel option
- Adding icmpv4 type 3, 11 for TTL decrementation and MTU negotiation

* Wed May 31 2023 Rachel Menge <rachelmenge@microsoft.com> - 1.8.7-2
- Modify defaults to account for DHCPv6

* Wed Jan 05 2022 Rachel Menge <rachelmenge@microsoft.com> - 1.8.7-1
- Update to version 1.8.7

* Wed Nov 10 2021 Rachel Menge <rachelmenge@microsoft.com> - 1.8.3-8
- Revert ssh brute force prevention

* Thu Sep 30 2021 Thomas Crain <thcrain@microsoft.com> - 1.8.3-7
- Add provides from main package for services subpackage
- Lint spec

* Mon Jun 21 2021 Rachel Menge <rachelmenge@microsoft.com> - 1.8.3-6
- Add dependency on iana-etc (JOSLOBO 7/26: bumped dash version for merge)

* Fri Apr 02 2021 Thomas Crain <thcrain@microsoft.com> - 1.8.3-5
- Merge the following releases from 1.0 to dev branch
- rachelmenge@microsoft.com, 1.8.3-4: Add ssh brute force prevention to ip4save and ip6save
- License verified

* Tue Nov 03 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.8.3-4
- Systemd supports merged /usr. Update with corresponding file locations and macros.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.8.3-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.8.3-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jul 30 2019 Shreyas B. <shreyasb@vmware.com> 1.8.3-1
- Updated to version 1.8.3

* Tue Feb 26 2019 Alexey Makhalov <amakhalov@vmware.com> 1.8.0-2
- Flush ip6tables on service stop

* Mon Sep 10 2018 Ankit Jain <ankitja@vmware.com> 1.8.0-1
- Updated to version 1.8.0

* Thu Aug 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.1-4
- fix ip4save script for upgrade issues.

* Mon Jul 24 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.1-3
- use iptables-restore to reload rules.

* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 1.6.1-2
- Add devel package.

* Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.6.1-1
- Updated to version 1.6.1

* Wed Jan 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.6.0-6
- Flush iptables on service stop

* Tue Aug 30 2016 Anish Swaminathan <anishs@vmware.com> 1.6.0-5
- Change config file properties for iptables script

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-4
- GA - Bump release of all rpms

* Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 1.6.0-3
- Adding package support in pre/post/un scripts section.

* Thu Apr 21 2016 Divya Thaluru <dthaluru@vmware.com> 1.6.0-2
- Enabled iptable service. Added iptable rule to accept ssh connections by default.

* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.6.0-1
- Updated to version 1.6.0

* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  1.4.21-3
- Add systemd to Requires and BuildRequires.
- Use systemctl to enable/disable service.

* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.4.21-2
- Updated group.

* Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 1.4.21-1
- Initial build.  First version
