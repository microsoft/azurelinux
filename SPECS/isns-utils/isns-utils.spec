Summary:        The iSNS daemon and utility programs
Name:           isns-utils
Version:        0.102
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/open-iscsi/open-isns
Source0:        https://github.com/open-iscsi/open-isns/archive/v%{version}.tar.gz#/open-isns-%{version}.tar.gz
Source1:        isnsd.service

BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  openssl-devel
BuildRequires:  pkg-config
BuildRequires:  systemd
BuildRequires:  systemd-devel

Requires(post): systemd-units
Requires(postun): systemd-units
Requires(preun): systemd-units

%description
The iSNS package contains the daemon and tools to setup a iSNS server,
and iSNS client tools. The Internet Storage Name Service (iSNS) protocol
allows automated discovery, management and configuration of iSCSI and
Fibre Channel devices (using iFCP gateways) on a TCP/IP network.

%package libs
Summary:        Shared library files for iSNS

%description libs
Shared library files for iSNS

%package devel
Summary:        Development files for iSNS

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development files for iSNS

%prep
%autosetup -n open-isns-%{version}

%build
%configure --enable-shared --disable-static
%make_build

%install
make install DESTDIR=%{buildroot}
make install_hdrs DESTDIR=%{buildroot}
make install_lib DESTDIR=%{buildroot}
chmod 755 %{buildroot}%{_sbindir}/isns*
chmod 755 %{buildroot}%{_libdir}/libisns.so.0
rm %{buildroot}%{_unitdir}/isnsd.service
rm %{buildroot}%{_unitdir}/isnsd.socket
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/isnsd.service

%post
%systemd_post isnsd.service

%postun
%systemd_postun isnsd.service

%preun
%systemd_preun isnsd.service

%triggerun -- isns-utils < 0.91-7
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
%{_bindir}/systemd-sysv-convert --save isnsd >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del isnsd >/dev/null 2>&1 || :
/bin/systemctl try-restart isnsd.service >/dev/null 2>&1 || :

%ldconfig_scriptlets -n %{name}-libs

%files
%license COPYING
%doc README
%{_sbindir}/isnsd
%{_sbindir}/isnsadm
%{_sbindir}/isnsdd
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_unitdir}/isnsd.service
%dir %{_sysconfdir}/isns
%dir %{_sharedstatedir}/isns
%config(noreplace) %{_sysconfdir}/isns/*

%files libs
%{_libdir}/libisns.so.0

%files devel
%dir %{_includedir}/libisns
%{_includedir}/libisns/*.h
%{_libdir}/libisns.so

%changelog
* Tue Jan 16 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 0.102-1
- Update source to v0.102

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.101-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Feb 23 2022 Cameron Baird <cameronbaird@microsoft.com> - 0.101-1
- Update source to v0.101

* Thu Jul 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.97-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Added the '%%license' macro.
- Using '%%autosetup' and the '%%make_build' macro instead of 'make'.
- License verified.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.97-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.97-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.97-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.97-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.97-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.97-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.97-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 12 2017 Chris Leech <cleech@redhat.com> - 0.97-3
- switch to building as a shared library instead of static

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Miro Hrončok <mhroncok@redhat.com> - 0.97-1
- Update to 0.97
- Upstream moved on GitHub

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.94-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 12 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 0.94-2
- add -static Provides to the -devel package (#1284298)

* Mon Oct 05 2015 Chris Leech <cleech@redhat.com> - 0.94-1
- new upstream location, update to 0.94
- new devel package, upstream open-iscsi is dropping it's internal copy

* Wed Jun 17 2015 Chris Leech <cleech@redhat.com> - 0.93-8
- use of systemd rpm macros now require systemd as a BuildRequires

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug  4 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.93-4
- Fix FTBFS, modernise spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 10 2012 Chris Leech <cleech@redhat.com> - 0.93-1
- Rebase to 0.93
- Make use of systemd rpm macros for scriptlets, BZ 850174

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Jon Ciesla <limburgher@gmail.com> - 0.91-7
- Migrate to systemd, BZ 789707.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.91-4
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.91-1
- rebuild with new openssl

* Wed Jan 16 2008 Mike Christie <mchristie@redhat.com> - 0.91-0.0
- first build
