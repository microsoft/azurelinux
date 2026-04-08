# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without i18n

%define testrelease 0
%define releasecandidate 0
%if 0%{testrelease}
  %define extrapath test-releases/
  %define extraversion test%{testrelease}
%endif
%if 0%{releasecandidate}
  %define extrapath release-candidates/
  %define extraversion rc%{releasecandidate}
%endif

%define _hardened_build 1
# path to upstream git repository
%global forgeurl0 git://thekelleys.org.uk/dnsmasq.git
# tag of selected version
%global gittag v%{version}%{?extraversion}


# Attempt to prepare source-git with downstream repos
%bcond_with sourcegit
%bcond_without annocheck

Name:           dnsmasq
Version:        2.92
Release:        1%{?extraversion:.%{extraversion}}%{?dist}
Summary:        A lightweight DHCP/caching DNS server

# SPDX identifiers already
License:        GPL-2.0-only OR GPL-3.0-only
URL:            http://www.thekelleys.org.uk/dnsmasq/
VCS:            git:%{forgeurl0}
Source0:        %{url}%{?extrapath}%{name}-%{version}%{?extraversion}.tar.xz
Source1:        %{name}.service
Source2:        dnsmasq-systemd-sysusers.conf
Source3:        %{url}%{?extrapath}%{name}-%{version}%{?extraversion}.tar.xz.asc
# GPG public key
%if 0%{?testrelease} || 0%{?releasecandidate}
Source4:        %{url}%{?extrapath}test-release-public-key
%else
Source4:        http://www.thekelleys.org.uk/srkgpg.txt
%endif

# https://bugzilla.redhat.com/show_bug.cgi?id=1495409
Patch1:         dnsmasq-2.77-underflow.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1852373
Patch2:         dnsmasq-2.81-configuration.patch
Patch3:         dnsmasq-2.78-fips.patch
Patch7:         dnsmasq-2.90-dbus-interfaces.patch
# https://lists.thekelleys.org.uk/pipermail/dnsmasq-discuss/2026q1/018378.html
Patch8:         https://thekelleys.org.uk/gitweb/?p=dnsmasq.git;a=patch;h=f603a4f920e6953b11667d424956fd47373870e9#/dnsmasq-2.92-dnssec-wildcard.patch


Requires:       nettle

BuildRequires:  dbus-devel
BuildRequires:  pkgconfig
BuildRequires:  libidn2-devel
BuildRequires:  pkgconfig(libnetfilter_conntrack)
BuildRequires:  nettle-devel
BuildRequires:  nftables-devel
Buildrequires:  gcc
BuildRequires:  gnupg2

BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros
%{?systemd_ordering}
%if %{with sourcegit}
BuildRequires:  git-core
%endif
BuildRequires: make
%if %{with i18n}
BuildRequires: gettext
%endif
%if %{with annocheck}
BuildRequires: annobin-annocheck
%endif

%description
Dnsmasq is lightweight, easy to configure DNS forwarder and DHCP server.
It is designed to provide DNS and, optionally, DHCP, to a small network.
It can serve the names of local machines which are not in the global
DNS. The DHCP server integrates with the DNS server and allows machines
with DHCP-allocated addresses to appear in the DNS with names configured
either in each host or in a central configuration file. Dnsmasq supports
static and dynamic DHCP leases and BOOTP for network booting of disk-less
machines.

%package        utils
Summary:        Utilities for manipulating DHCP server leases

%description    utils
Utilities that use the standard DHCP protocol to query/remove a DHCP
server's leases.

%if %{with i18n}
%package        langpack
Summary:        Translations for few languages
License:        LicenseRef-Fedora-Public-Domain AND GPL-2.0-or-later
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
# Will not do separate packages for every single language, those translations are small enough
Supplements:    (%{name} = %{version}-%{release} and (langpacks-de or langpacks-es or langpacks-fi or langpacks-fr or langpacks-id or langpacks-it or langpacks-ka or langpacks-no or langpacks-pl or langpacks-pt_BR or langpacks-ro) )

%description    langpack
Translations for few languages on dnsmasq.

%endif

%prep
%if 0%{?fedora}
%gpgverify -k 4 -s 3 -d 0
%endif
%if %{with sourcegit}
%autosetup -n %{name}-%{version}%{?extraversion} -N -S git_am
# If preparing with sourcegit, drop again source directory
# and clone git repository
# FIXME: deleting just unpacked sources is dangerous
# But using %%setup changes used directories in %%build and %%install
rm -rf %{_builddir}/%{name}-%{version}%{?extraversion}
cd %{_builddir}
git clone -b %{gittag} %{forgeurl0} %{name}-%{version}%{?extraversion}
cd %{name}-%{version}%{?extraversion}
git checkout -b rpmbuild
%else
%autosetup -n %{name}-%{version}%{?extraversion} -N
%endif
# Apply patches on top
%autopatch -p1

# use /var/lib/dnsmasq instead of /var/lib/misc
for file in dnsmasq.conf.example man/dnsmasq.8 man/es/dnsmasq.8 src/config.h; do
    sed -i 's|/var/lib/misc/dnsmasq.leases|/var/lib/dnsmasq/dnsmasq.leases|g' "$file"
done

#set default user /group in src/config.h
sed -i 's|#define CHUSER "nobody"|#define CHUSER "dnsmasq"|' src/config.h
sed -i 's|#define CHGRP "dip"|#define CHGRP "dnsmasq"|' src/config.h
sed -i "s|\(#\s*define RUNFILE\) \"/var/run/dnsmasq.pid\"|\1 \"%{_rundir}/dnsmasq.pid\"|" src/config.h

# optional parts
sed -i 's|^COPTS[[:space:]]*=|\0 -DHAVE_DBUS -DHAVE_LIBIDN2 -DHAVE_DNSSEC -DHAVE_CONNTRACK -DHAVE_NFTSET|' Makefile

%build
%make_build CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS" BINDIR=%{_sbindir} \
%if %{with i18n}
  all-i18n
%else
  all
%endif
%make_build -C contrib/lease-tools CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS" BINDIR=%{_sbindir}

%install
# normally i'd do 'make install'...it's a bit messy, though
mkdir -p $RPM_BUILD_ROOT%{_sbindir} \
        $RPM_BUILD_ROOT%{_mandir}/man8 \
        $RPM_BUILD_ROOT%{_var}/lib/dnsmasq \
        $RPM_BUILD_ROOT%{_sysconfdir}/dnsmasq.d \
        $RPM_BUILD_ROOT%{_datadir}/dbus-1/system.d
install -p src/dnsmasq $RPM_BUILD_ROOT%{_sbindir}/dnsmasq
install -p -m 0644 dnsmasq.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/dnsmasq.conf
install -p -m 0644 dbus/dnsmasq.conf $RPM_BUILD_ROOT%{_datadir}/dbus-1/system.d/
install -p -m 0644 man/dnsmasq.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install -p -D -m 0644 trust-anchors.conf $RPM_BUILD_ROOT%{_datadir}/%{name}/trust-anchors.conf

# utils sub package
mkdir -p $RPM_BUILD_ROOT%{_bindir} \
         $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m 755 contrib/lease-tools/dhcp_release $RPM_BUILD_ROOT%{_bindir}/dhcp_release
install -p -m 644 contrib/lease-tools/dhcp_release.1 $RPM_BUILD_ROOT%{_mandir}/man1/dhcp_release.1
install -p -m 755 contrib/lease-tools/dhcp_release6 $RPM_BUILD_ROOT%{_bindir}/dhcp_release6
install -p -m 644 contrib/lease-tools/dhcp_release6.1 $RPM_BUILD_ROOT%{_mandir}/man1/dhcp_release6.1
install -p -m 755 contrib/lease-tools/dhcp_lease_time $RPM_BUILD_ROOT%{_bindir}/dhcp_lease_time
install -p -m 644 contrib/lease-tools/dhcp_lease_time.1 $RPM_BUILD_ROOT%{_mandir}/man1/dhcp_lease_time.1

# Systemd
mkdir -p %{buildroot}%{_unitdir}
install -p -m644 %{SOURCE1} %{buildroot}%{_unitdir}
rm -rf %{buildroot}%{_initrddir}

#install systemd sysuser file
install -p -Dpm 644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf

%if %{with i18n}
%make_install PREFIX=%{_prefix} CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS" BINDIR=%{_sbindir} install-i18n
%find_lang %{name} --with-man
%endif

%check
# Minimalistic build check
$RPM_BUILD_ROOT%{_sbindir}/dnsmasq --help
$RPM_BUILD_ROOT%{_sbindir}/dnsmasq --help dhcp
$RPM_BUILD_ROOT%{_sbindir}/dnsmasq --help dhcp6
$RPM_BUILD_ROOT%{_sbindir}/dnsmasq --test --conf-file=$RPM_BUILD_ROOT%{_datadir}/%{name}/trust-anchors.conf
if [ -d "%{_sysconfdir}/dnsmasq.d" ]; then
  # this would fail in mock if that directory does not exist
  $RPM_BUILD_ROOT%{_sbindir}/dnsmasq --test --conf-file=$RPM_BUILD_ROOT%{_sysconfdir}/dnsmasq.conf
fi
# check link flags
if type -p annocheck; then
  annocheck --no-use-debuginfod --ignore-unknown --verbose --debug-dir=$RPM_BUILD_ROOT%{_prefix}/lib/debug/%{_sbindir} $RPM_BUILD_ROOT%{_sbindir}/dnsmasq
fi

%post
%systemd_post dnsmasq.service

%preun
%systemd_preun dnsmasq.service

%postun
%systemd_postun_with_restart dnsmasq.service

%files
%doc CHANGELOG FAQ doc.html setup.html dbus/DBus-interface
%license COPYING COPYING-v3
%config(noreplace) %{_sysconfdir}/dnsmasq.conf
%dir %{_sysconfdir}/dnsmasq.d
%dir %attr(0755,root,dnsmasq) %{_var}/lib/dnsmasq
%{_datadir}/dbus-1/system.d/dnsmasq.conf
%{_unitdir}/%{name}.service
%{_sbindir}/dnsmasq
%{_mandir}/man8/dnsmasq*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/trust-anchors.conf
%{_sysusersdir}/dnsmasq.conf

%files utils
%license COPYING COPYING-v3
%{_bindir}/dhcp_*
%{_mandir}/man1/dhcp_*

%if %{with i18n}
%files langpack -f %{name}.lang
%endif

%changelog
* Fri Jan 16 2026 Petr Menšík <pemensik@redhat.com> - 2.92-1
- Update to 9.29 (rhbz#2429567)

* Thu Aug 14 2025 Petr Menšík <pemensik@redhat.com> - 2.91-1
- Update to 2.91 (rhbz#2353910)
- Move dbus-1 definition to _datadir
- Drop call to %sysusers_create_compat

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.90-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Feb 07 2025 Petr Menšík <pemensik@redhat.com> - 2.90-6
- Fix building after GCC 15 update (rhbz#2340085)

* Thu Jan 16 2025 Petr Menšík <pemensik@redhat.com> - 2.90-6
- Refresh interface after each DBus servers reset (v2)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.90-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 27 2024 Dmitry Konishchev <konishchev@gmail.com> - 2.90-4
- Enable nftables sets support

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 09 2024 Petr Menšík <pemensik@redhat.com> - 2.90-2
- Update SPDX in license tag to use uppercase conjunction

* Tue Feb 13 2024 Petr Menšík <pemensik@redhat.com> - 2.90-1
- Update to 2.90 (#2264049)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.89-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.89-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 12 2024 Petr Menšík <pemensik@redhat.com> - 2.89-7
- Use local-service=host for initial configuration (#2258062)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.89-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 27 2023 Petr Menšík <pemensik@redhat.com> - 2.89-5
- Prevent crash on dbus reconnection (#2186468)

* Thu Apr 27 2023 Petr Menšík <pemensik@redhat.com> - 2.89-4
- Actually enable localization support in dnsmasq (#2131681)

* Wed Apr 05 2023 Petr Menšík <pemensik@redhat.com> - 2.89-3
- Add separate SPDX licenses also to translations
- Include localized man pages simpler way, make them noarch

* Mon Apr 03 2023 Petr Menšík <pemensik@redhat.com> - 2.89-2
- Limit offered EDNS0 size 1232 (CVE-2023-28450)

* Mon Feb 13 2023 Petr Menšík <pemensik@redhat.com> - 2.89-1
- Update to 2.89 (#2167121)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.88-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 08 2022 Petr Menšík <pemensik@redhat.com> - 2.88-2
- Create dnsmasq-langpack subpackage with translations (#2131681)

* Tue Dec 06 2022 Petr Menšík <pemensik@redhat.com> - 2.88-1
- Update to 2.88 (#2150667)

* Fri Nov 25 2022 Petr Menšík <pemensik@redhat.com> - 2.87-3
- Fix regression removing config statements on DBus change (#2148301)

* Fri Sep 30 2022 Petr Menšík <pemensik@redhat.com> - 2.87-2
- Update License tag to SPDX identifier

* Tue Sep 27 2022 Petr Menšík <pemensik@redhat.com> - 2.87-1
- Update to 2.87 (#2129658)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.86-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Petr Menšík <pemensik@redhat.com> - 2.86-10
- Do not own configuration by dnsmasq group (#2104973)

* Fri Jun 17 2022 Petr Menšík <pemensik@redhat.com> - 2.86-9
- Do not drop static forwarders on DBus reconfiguration (#2061944)

* Fri Apr 29 2022 Anssi Hannula <anssi.hannula@iki.fi> - 2.86-8
- Enable conntrack support

* Fri Apr 29 2022 Petr Menšík <pemensik@redhat.com> - 2.86-7
- Correct GNU address in license file

* Wed Feb 23 2022 Petr Menšík <pemensik@redhat.com> - 2.86-6
- Fix errors on server reload

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.86-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 16 2022 Petr Menšík <pemensik@redhat.com> - 2.86-4
- Add writeable group flag to log file (#2024166)

* Thu Oct 14 2021 Petr Menšík <pemensik@redhat.com> - 2.86-3
- Rebuild server_array on any server change (#2009975)
- Compare case-insensitive also TCP queries (#2014019)

* Thu Sep 23 2021 Petr Menšík <pemensik@redhat.com> - 2.86-2
- Attempt to fix regression found on recent release (#2006367)

* Thu Sep 09 2021 Petr Menšík <pemensik@redhat.com> - 2.86-1
- Update to 2.86 (#2002475)
- Apply coverity detected issues patches

* Wed Aug 04 2021 Petr Menšík <pemensik@redhat.com> - 2.85-6
- Do not require systemd

* Thu Jul 22 2021 Petr Menšík <pemensik@redhat.com> - 2.85-5
- Start before nss-lookup.target, hint modification to listen on IP (#1984618)

* Thu Jul 22 2021 Petr Menšík <pemensik@redhat.com> - 2.85-4
- Update lease if hostname is assigned to a new lease (#1978718)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Apr 08 2021 Petr Menšík <pemensik@redhat.com> - 2.85-2
- Update to 2.85 (#1947198)

* Wed Mar 31 2021 Petr Menšík <pemensik@redhat.com> - 2.85-1.rc2
- Update to 2.85rc2 (CVE-2021-3448)
- Switch systemd unit to forking, reports error on startup (#1774028)

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.84-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Petr Menšík <pemensik@redhat.com> - 2.84-1
- Update to 2.84

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Petr Menšík <pemensik@redhat.com> - 2.83-1
- Update to 2.83, fix CVE-2020-25681-7

* Fri Oct 09 2020 Petr Menšík <pemensik@redhat.com> - 2.82-4
- Remove uninitialized condition from downstream patch

* Wed Sep 30 2020 Petr Menšík <pemensik@redhat.com> - 2.82-3
- Listen only on localhost interface, return port unreachable on all others
  (#1852373)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Petr Menšík <pemensik@redhat.com> - 2.82-1
- Update to 2.82

* Tue Jun 30 2020 Petr Menšík <pemensik@redhat.com> - 2.81-4
- Accept queries only from localhost (CVE-2020-14312)

* Mon May 11 2020 Petr Menšík <pemensik@redhat.com> - 2.81-3
- Correct multiple entries with the same mac address (#1834454)

* Thu Apr 16 2020 Petr Menšík <pemensik@redhat.com> - 2.81-2
- Update to 2.81 (#1823139)

* Mon Mar 23 2020 Petr Menšík <pemensik@redhat.com> - 2.81-1.rc3
- Update to 2.81rc3

* Mon Mar 23 2020 Petr Menšík <pemensik@redhat.com> - 2.80-14
- Fix last build breakage of DNS (#1814468)

* Tue Mar 10 2020 Petr Menšík <pemensik@redhat.com> - 2.80-13
- Respond to any local name also withou rd bit set (#1647464)

* Wed Mar 04 2020 Petr Menšík <pemensik@redhat.com> - 2.80-12
- Support multiple static leases for single mac on IPv6 (#1810172)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.80-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 28 2019 Petr Menšík <pemensik@redhat.com> - 2.80-10
- Fix CPU intensive RA flood (#1739797)

* Fri Aug 09 2019 Petr Menšík <pemensik@redhat.com> - 2.80-9
- Remove SO_TIMESTAMP support, DHCP was broken (#1739081)

* Wed Jul 31 2019 Petr Menšík <pemensik@redhat.com> - 2.80-8
- Compile with nettle 3.5
- Support missing SIOCGSTAMP ioctl

* Wed Jul 31 2019 Petr Menšík <pemensik@redhat.com> - 2.80-7
- Fix TCP listener after interface recreated (#1728701)

* Wed Jul 24 2019 Petr Menšík <pemensik@redhat.com> - 2.80-6
- Do not return NXDOMAIN on empty non-terminals (#1674067)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.80-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 08 2019 Petr Menšík <pemensik@redhat.com> - 2.80-4
- Use more recent macro to create dnsmasq user

* Fri Feb 15 2019 Petr Menšík <pemensik@redhat.com> - 2.80-3
- Apply patches by autosetup

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 20 2018 Petr Menšík <pemensik@redhat.com> - 2.80-1
- Update to 2.80

* Thu Aug 09 2018 Petr Menšík <pemensik@redhat.com> - 2.79-8
- Better randomize ports

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 2.79-7
- Rebuild with fixed binutils

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.79-6
- Rebuild for new binutils

* Thu Jul 26 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.79-5
- Fix %%pre scriptlet (#1548050)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.79-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Petr Menšík <pemensik@redhat.com> - 2.79-3
- Make dnsmasq leases writeable by root again (#1554390)

* Mon Jul 02 2018 Petr Menšík <pemensik@redhat.com> - 2.79-2
- Fix passing of dnssec enabled queries (#1597309)

* Thu Mar 15 2018 Petr Menšík <pemensik@redhat.com> - 2.79-1
- Rebase to 2.79
- Stop using nettle_hashes directly, use access function (#1548060)
- Do not break on cname with spaces (#1498667)
- Require nettle 3.4+
- Do not own sysusers.d directory, already depends on systemd providing it

* Fri Mar 02 2018 Petr Menšík <pemensik@redhat.com> - 2.78-7
- Emit warning with dnssec enabled on FIPS system (#1549507)

* Sun Feb 25 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.78-6
- Create user before installing files (#1548050)

* Fri Feb 23 2018 Petr Menšík <pemensik@redhat.com> - 2.78-5
- Create user first and then restart service

* Thu Feb 22 2018 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.78-4
- add gcc into buildrequires
- deliver an extra sysusers.d file to create dnsmasq user/group
- set CHUSER and CHGRP to dnsmasq in src/config.h

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.78-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Petr Menšík <pemensik@redhat.com> - 2.78-2
- DNSSEC fix for wildcard NSEC records (CVE-2017-15107)

* Tue Oct 03 2017 Petr Menšík <pemensik@redhat.com> - 2.78-1
- Rebase to 2.78

* Tue Oct 03 2017 Petr Menšík <pemensik@redhat.com> - 2.77-9
- More patches related to CVE-2017-14491

* Mon Oct 02 2017 Petr Menšík <pemensik@redhat.com> - 2.77-8
- Security fix, CVE-2017-14491, DNS heap buffer overflow
- Security fix, CVE-2017-14492, DHCPv6 RA heap overflow
- Security fix, CVE-2017-14493, DHCPv6 - Stack buffer overflow
- Security fix, CVE-2017-14494, Infoleak handling DHCPv6
- Security fix, CVE-2017-14496, Integer underflow in DNS response creation
- Security fix, CVE-2017-14495, OOM in DNS response creation
- Misc code cleanups arising from Google analysis
- Do not include stdio.h before dnsmasq.h

* Thu Sep 14 2017 Petr Menšík <pemensik@redhat.com> - 2.77-7
- Fix CVE-2017-13704

* Mon Aug 14 2017 Petr Menšík <pemensik@redhat.com> - 2.77-6
- Own the /usr/share/dnsmasq dir (#1480856)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.77-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.77-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Petr Menšík <pemensik@redhat.com> - 2.77-3
- Update to 2.77

* Fri May 12 2017 Petr Menšík <pemensik@redhat.com> - 2.77-2.rc2
- Fix dhcp

* Thu May 11 2017 Petr Menšík <pemensik@redhat.com> - 2.77-1
- Update to 2.77rc2

* Thu May 11 2017 Petr Menšík <pemensik@redhat.com>
- Include dhcp_release6 tool and license in utils
- Support for IDN 2008 (#1449150)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.76-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 19 2016 Pavel Šimerda <psimerda@redhat.com> - 2.76-2
- Resolves: #1373485 - dns not updated after sleep and resume laptop

* Fri Jul 15 2016 Pavel Šimerda <psimerda@redhat.com> - 2.76-1
- New version 2.76

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.75-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Tomas Hozza <thozza@redhat.com> - 2.75-3
- Fixed minor bug in dnsmasq.conf (#1295143)

* Fri Oct 02 2015 Pavel Šimerda <psimerda@redhat.com> - 2.75-2
- Resolves: #1239256 - install trust-anchors.conf

* Wed Aug 05 2015 Pavel Šimerda <psimerda@redhat.com> - 2.75-1
- new version 2.75

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.72-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 06 2014 Nils Philippsen <nils@redhat.com> - 2.72-3
- don't include /etc/dnsmasq.d in triplicate, ignore RPM backup files instead
- package is dual-licensed GPL v2 or v3
- drop %%triggerun, we're not supposed to automatically migrate from SysV to
  systemd anyway

* Mon Oct 06 2014 Tomas Hozza <thozza@redhat.com> - 2.72-2
- Fix typo in default configuration (#1149459)

* Thu Sep 25 2014 Tomas Hozza <thozza@redhat.com> - 2.72-1
- Update to 2.72 stable

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.71-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Tomas Hozza <thozza@redhat.com> - 2.71-1
- Update to 2.71 stable

* Fri Apr 25 2014 Tomas Hozza <thozza@redhat.com> - 2.70-1
- Update to 2.70 stable

* Fri Apr 11 2014 Tomas Hozza <thozza@redhat.com> - 2.69-1
- Update to 2.69 stable

* Mon Mar 24 2014 Tomas Hozza <thozza@redhat.com> - 2.69-0.1.rc1
- Update to 2.69rc1
- enable DNSSEC implementation

* Mon Dec 09 2013 Tomas Hozza <thozza@redhat.com> - 2.68-1
- Update to 2.68 stable

* Tue Nov 26 2013 Tomas Hozza <thozza@redhat.com> - 2.68-0.1.rc3
- Update to 2.68rc3

* Fri Nov 01 2013 Tomas Hozza <thozza@redhat.com> - 2.67-1
- Update to 2.67 stable
- Include one post release upstream fix for CNAME

* Fri Oct 18 2013 Tomas Hozza <thozza@redhat.com> - 2.67-0.9.rc4
- update to 2.67rc4

* Wed Oct 02 2013 Tomas Hozza <thozza@redhat.com> - 2.67-0.8.rc2
- update to 2.67rc2

* Thu Sep 12 2013 Tomas Hozza <thozza@redhat.com> - 2.67-0.7.test13
- update to 2.67test13
- use .tar.xz upstream archives

* Thu Aug 15 2013 Tomas Hozza <thozza@redhat.com> - 2.67-0.6.test7
- Use SO_REUSEPORT and SO_REUSEADDR if possible for DHCPv4/6 (#981973)

* Mon Aug 12 2013 Tomas Hozza <thozza@redhat.com> - 2.67-0.5.test7
- Don't use SO_REUSEPORT on DHCPv4 socket to prevent conflicts with ISC DHCP (#981973)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.67-0.4.test7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Tomas Hozza <thozza@redhat.com> - 2.67-0.3.test7
- update to 2.67test7
- drop merged patch
- use _hardened_build macro instead of hardcoded flags

* Fri May 17 2013 Tomas Hozza <thozza@redhat.com> - 2.67-0.2.test4
- Fix failure to start with ENOTSOCK (#962874)

* Wed May 15 2013 Tomas Hozza <thozza@redhat.com> - 2.67-0.1.test4
- update to the latest testing release 2.67test4 (#962246)
- drop mergerd patches

* Tue Apr 30 2013 Tomas Hozza <thozza@redhat.com> - 2.66-5
- dnsmasq unit file cleanup
  - drop forking Type and PIDfile and rather start dnsmasq with "-k" option
  - drop After syslog.target as this is by default

* Thu Apr 25 2013 Tomas Hozza <thozza@redhat.com> - 2.66-4
- include several fixes from upstream repo:
  - Send TCP DNS messages in one packet
  - Fix crash on SERVFAIL when using --conntrack option
  - Fix regression in dhcp_lease_time utility
  - Man page typos fixes
  - Note that dhcp_lease_time and dhcp_release work only for IPv4
  - Fix for --dhcp-match option to work also with BOOTP protocol

* Sat Apr 20 2013 Tomas Hozza <thozza@redhat.com> - 2.66-3
- Use Full RELRO when linking the daemon
- compile the daemon with PIE
- include two fixes from upstream git repo

* Thu Apr 18 2013 Tomas Hozza <thozza@redhat.com> - 2.66-2
- New stable version dnsmasq-2.66
- Drop of merged patch

* Fri Apr 12 2013 Tomas Hozza <thozza@redhat.com> - 2.66-1.rc5
- Update to latest dnsmasq-2.66rc5
- Include fix for segfault when lease limit is reached

* Fri Mar 22 2013 Tomas Hozza <thozza@redhat.com> - 2.66-1.rc1
- Update to latest dnsmasq-2.66rc1
- Dropping unneeded patches
- Enable IDN support

* Fri Mar 15 2013 Tomas Hozza <thozza@redhat.com> - 2.65-5
- Allocate dhcp_buff-ers also if daemon->ra_contexts to prevent SIGSEGV (#920300)

* Thu Jan 31 2013 Tomas Hozza <thozza@redhat.com> - 2.65-4
- Handle locally-routed DNS Queries (#904940)

* Thu Jan 24 2013 Tomas Hozza <thozza@redhat.com> - 2.65-3
- build dnsmasq with $RPM_OPT_FLAGS, $RPM_LD_FLAGS explicitly (#903362) 

* Tue Jan 22 2013 Tomas Hozza <thozza@redhat.com> - 2.65-2
- Fix for CVE-2013-0198 (checking of TCP connection interfaces) (#901555)

* Sat Dec 15 2012 Tomas Hozza <thozza@redhat.com> - 2.65-1
- new version 2.65

* Wed Dec 05 2012 Tomas Hozza <thozza@redhat.com> - 2.64-1
- New version 2.64
- Merged patches dropped

* Tue Nov 20 2012 Tomas Hozza <thozza@redhat.com> - 2.63-4
- Remove EnvironmentFile from service file (#878343)

* Mon Nov 19 2012 Tomas Hozza <thozza@redhat.com> - 2.63-3
- dhcp6 support fixes (#867054)
- removed "-s $HOSTNAME" from .service file (#753656, #822797)

* Tue Oct 23 2012 Tomas Hozza <thozza@redhat.com> - 2.63-2
- Introduce new systemd-rpm macros in dnsmasq spec file (#850096)

* Thu Aug 23 2012 Douglas Schilling Landgraf <dougsland@redhat.com> - 2.63-1
- Use .tar.gz compression, in upstream site there is no .lzma anymore
- New version 2.63

* Sat Feb 11 2012 Pádraig Brady <P@draigBrady.com> - 2.59-5
- Compile DHCP lease management utils with RPM_OPT_FLAGS

* Thu Feb  9 2012 Pádraig Brady <P@draigBrady.com> - 2.59-4
- Include DHCP lease management utils in a subpackage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 26 2011 Douglas Schilling Landgraf <dougsland@redhat.com> - 2.59-2
- do not enable service by default

* Fri Aug 26 2011 Douglas Schilling Landgraf <dougsland@redhat.com> - 2.59-1
- New version 2.59
- Fix regression in 2.58 (IPv6 issue) - bz 744814

* Fri Aug 26 2011 Douglas Schilling Landgraf <dougsland@redhat.com> - 2.58-1
- Fixed License
- New version 2.58

* Mon Aug 08 2011 Patrick "Jima" Laughton <jima@fedoraproject.org> - 2.52-5
- Include systemd unit file

* Mon Aug 08 2011 Patrick "Jima" Laughton <jima@fedoraproject.org> - 2.52-3
- Applied Jóhann's patch, minor cleanup

* Tue Jul 26 2011 Jóhann B. Guðmundsson <johannbg@gmail.com> - 2.52-3
- Introduce systemd unit file, drop SysV support

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 26 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.52-1
- New Version 2.52
- fix condrestart() in initscript bz 547605
- fix sed to enable DBUS(the '*' need some escaping) bz 553161

* Sun Nov 22 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.51-2
- fix bz 512664

* Sat Oct 17 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.51-1
- move initscript from patch to a plain text file
- drop (dnsmasq-configuration.patch) and use sed instead
- enable /etc/dnsmasq.d fix bz 526703
- change requires to package name instead of file
- new version 2.51

* Mon Oct  5 2009 Mark McLoughlin <markmc@redhat.com> - 2.48-4
- Fix multiple TFTP server vulnerabilities (CVE-2009-2957, CVE-2009-2958)

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.48-3
- Use lzma compressed upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.48-1
- Bugfix/feature enhancement update
- Fixing BZ#494094

* Fri May 29 2009 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.47-1
- Bugfix/feature enhancement update

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Matěj Cepl <mcepl@redhat.com> - 2.45-2
- rebuilt

* Mon Jul 21 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.45-1
- Upstream release (bugfixes)

* Wed Jul 16 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.43-2
- New upstream release, contains fixes for CVE-2008-1447/CERT VU#800113
- Dropped patch for newer glibc (merged upstream)

* Wed Feb 13 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.8
- Added upstream-authored patch for newer glibc (thanks Simon!)

* Wed Feb 13 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.7
- New upstream release

* Wed Jan 30 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.6.rc1
- Release candidate
- Happy Birthday Isaac!

* Wed Jan 23 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.5.test30
- Bugfix update

* Mon Dec 31 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.4.test26
- Bugfix/feature enhancement update

* Thu Dec 13 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.3.test24
- Upstream fix for fairly serious regression

* Tue Dec 04 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.41-0.2.test20
- New upstream test release
- Moving dnsmasq.leases to /var/lib/dnsmasq/ as per BZ#407901
- Ignoring dangerous-command-in-%%post rpmlint warning (as per above fix)
- Patch consolidation/cleanup
- Removed conditionals for Fedora <= 3 and Aurora 2.0

* Tue Sep 18 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.40-1
- Finalized upstream release
- Removing URLs from patch lines (CVS is the authoritative source)
- Added more magic to make spinning rc/test packages more seamless

* Sun Aug 26 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.40-0.1.rc2
- New upstream release candidate (feature-frozen), thanks Simon!
- License clarification

* Tue May 29 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.39-1
- New upstream version (bugfixes, enhancements)

* Mon Feb 12 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.38-1
- New upstream version with bugfix for potential hang

* Tue Feb 06 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.37-1
- New upstream version

* Wed Jan 24 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.36-1
- New upstream version

* Mon Nov 06 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.35-2
- Stop creating /etc/sysconfig on %%install
- Create /etc/dnsmasq.d on %%install

* Mon Nov 06 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.35-1
- Update to 2.35
- Removed UPGRADING_to_2.0 from %%doc as per upstream change
- Enabled conf-dir in default config as per RFE BZ#214220 (thanks Chris!)
- Added %%dir /etc/dnsmasq.d to %%files as per above RFE

* Tue Oct 24 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.34-2
- Fixed BZ#212005
- Moved %%postun scriptlet to %%post, where it made more sense
- Render scriptlets safer
- Minor cleanup for consistency

* Thu Oct 19 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.34-1
- Hardcoded version in patches, as I'm getting tired of updating them
- Update to 2.34

* Mon Aug 28 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.33-2
- Rebuild for FC6

* Tue Aug 15 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.33-1
- Update

* Sat Jul 22 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.32-3
- Added pkgconfig BuildReq due to reduced buildroot

* Thu Jul 20 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.32-2
- Forced update due to dbus version bump

* Mon Jun 12 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.32-1
- Update from upstream
- Patch from Dennis Gilmore fixed the conditionals to detect Aurora Linux

* Mon May  8 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.31-1
- Removed dbus config patch (now provided upstream)
- Patched in init script (no longer provided upstream)
- Added DBus-interface to docs

* Tue May  2 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-4.2
- More upstream-recommended cleanups :)
- Killed sysconfig file (provides unneeded functionality)
- Tweaked init script a little more

* Tue May  2 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-4
- Moved options out of init script and into /etc/sysconfig/dnsmasq
- Disabled DHCP_LEASE in sysconfig file, fixing bug #190379
- Simon Kelley provided dbus/dnsmasq.conf, soon to be part of the tarball

* Thu Apr 27 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-3
- Un-enabled HAVE_ISC_READER, a hack to enable a deprecated feature (request)
- Split initscript & enable-dbus patches, conditionalized dbus for FC3
- Tweaked name field in changelog entries (trying to be consistent)

* Mon Apr 24 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-2
- Disabled stripping of binary while installing (oops)
- Enabled HAVE_ISC_READER/HAVE_DBUS via patch
- Added BuildReq for dbus-devel

* Mon Apr 24 2006 Patrick "Jima" Laughton <jima@auroralinux.org> 2.30-1
- Initial Fedora Extras RPM
