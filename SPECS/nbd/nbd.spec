Summary:        Network Block Device user-space tools (TCP version)
Name:           nbd
Version:        3.25
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://nbd.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/nbd/%{name}/%{version}/%{name}-%{version}.tar.xz
Source1:        nbd-server.service
Source2:        nbd-server.sysconfig
BuildRequires:  gcc
BuildRequires:  glib2-devel >= 2.26
BuildRequires:  gnutls-devel
BuildRequires:  zlib-devel
BuildRequires:  libnl3-devel
BuildRequires:  systemd
%{?systemd_requires}

%description
Tools for the Linux Kernel's network block device, allowing you to use
remote block devices over a TCP/IP network.

%prep
%autosetup -p1

%build
%configure --enable-syslog --enable-lfs --enable-gznbd
%make_build

%install
%make_install
install -pDm644 systemd/nbd@.service %{buildroot}%{_unitdir}/nbd@.service
mkdir -p %{buildroot}%{_unitdir}/nbd@.service.d
cat > %{buildroot}%{_unitdir}/nbd@.service.d/modprobe.conf <<EOF
[Service]
ExecStartPre=/sbin/modprobe nbd
EOF
install -pDm644 %{S:1} %{buildroot}%{_unitdir}/nbd-server.service
install -pDm644 %{S:2} %{buildroot}%{_sysconfdir}/sysconfig/nbd-server

# Disable tests as it hangs the pipeline infinitely
# %%check
# wait longer for nbd-server to fully start,
# one second may not be enough on Fedora building infra
# sed -i -e 's/sleep 1/sleep 10/' tests/run/simple_test
# make check

%post
%systemd_post nbd-server.service

%preun
%systemd_preun nbd-server.service

%postun
%systemd_postun nbd-server.service

%files
%doc README.md doc/*.md doc/todo.txt
%license COPYING
%{_bindir}/nbd-server
%{_bindir}/nbd-trdump
%{_bindir}/gznbd
%{_mandir}/man*/nbd*
%{_sbindir}/nbd-client
%{_sbindir}/min-nbd-client
%config(noreplace) %{_sysconfdir}/sysconfig/nbd-server
%{_unitdir}/nbd-server.service
%{_unitdir}/nbd@.service
%{_unitdir}/nbd@.service.d

%changelog
* Thu Feb 01 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.25-1
- Auto-upgrade to 3.25 - none

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.20-6
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Jul 15 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.20-5
- Promote to Mariner base repo
- Modify test disabling in a way that's more friendly to our package test log parser
- Lint spec

* Sun Apr 17 2022 Muhammad Falak <mwani@microsoft.com> - 3.20-4
- Disable tests as they hang the ptest pipeline
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.20-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Sep 28 2019 Robin Lee <cheeselee@fedoraproject.org> - 3.20-1
- New upstream version 3.20 (RHBZ#1752353).

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb  7 2019 Richard W.M. Jones <rjones@redhat.com> - 3.19-1
- New upstream version 3.19 (RHBZ#1671079).

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov  4 2018 Robin Lee <cheeselee@fedoraproject.org> - 3.18-1
- Update to 3.18

* Sun Sep  2 2018 Richard W.M. Jones <rjones@redhat.com> - 3.17-3
- Add upstream fix for timeout issue which makes nbd-client almost unusable.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr  2 2018 Robin Lee <cheeselee@fedoraproject.org> - 3.17-1
- Update to 3.17

* Sat Mar 10 2018 Robin Lee <cheeselee@fedoraproject.org> - 3.16.2-3
- BR gcc for http://fedoraproject.org/wiki/Changes/Remove_GCC_from_BuildRoot

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Sep 23 2017 Robin Lee <cheeselee@fedoraproject> - 3.16.2-1
- Update to 3.16.2 (BZ#1490655, BZ#1490039)
- nbd@.service would automatically modprobe nbd (BZ#1480986)
- Fix scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 29 2017 Robin Lee <cheeselee@fedoraproject.org> - 3.16.1-1
- Update to 3.16.1

* Tue May 23 2017 Robin Lee <cheeselee@fedoraproject.org> - 3.15.3-1
- Update to 3.15.3

* Sun Feb 12 2017 Robin Lee <cheeselee@fedoraproject.org> - 3.15.1-1
- Update to 3.15.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 17 2016 Robin Lee <cheeselee@fedoraproject.org> - 3.14-2
- Install the nbd@.service systemd unit file (BZ#1367679)

* Sun Aug 14 2016 Robin Lee <cheeselee@fedoraproject.org> - 3.14-1
- Update to 3.14 (BZ#1279876)
- Enable gznbd
- Extend nbd-server waiting time during tests

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jul 11 2015 Christopher Meng <rpm@cicku.me> - 3.11-1
- Update to 3.11

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 21 2014 Christopher Meng <rpm@cicku.me> - 3.8-1
- Update to 3.8

* Thu Jan 30 2014 Christopher Meng <rpm@cicku.me> - 3.7-2
- Patch to support systemd init system in order to avoid kernel panic.

* Mon Jan 27 2014 Christopher Meng <rpm@cicku.me> - 3.7-1
- Update to 3.7

* Sat Jan 04 2014 Christopher Meng <rpm@cicku.me> - 3.6-1
- Update to 3.6

* Mon Dec 02 2013 Christopher Meng <rpm@cicku.me> - 3.5-1
- Fix incorrect parsing of access control file in nbd-server(CVE-2013-6410).
- Add systemd support for nbd-server(BZ#877518).
- Enable logging to syslog.

* Tue Sep 17 2013 Christopher Meng <rpm@cicku.me> - 3.4-1
- Update to 3.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Richard W.M. Jones <rjones@redhat.com> - 3.3-1
- New upstream version 3.3.
- Modernize the spec file.
- There is a new program (nbd-trdump).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Miloš Jakubíček <xjakub@fi.muni.cz> - 2.9.20-1
- Update to 2.9.20: fix CVE-2005-3534, BZ#673562

* Fri Mar 26 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 2.9.15-1
- Update to 2.9.15
- Remove file dep on stubs-32.h, doesn't seem to be necessary anymore

* Thu Aug  6 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 2.9.13-1
- Update to 2.9.13
- Dropped nbd-module.patch (merged upstream)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 13 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 2.9.12-1
- Update to 2.9.12 (resolves BZ#454099).
- Added nbd-module.patch (resolves BZ#496751).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Apr 09 2008 Warren Togami <wtogami@redhat.com> - 2.9.10-1
- match nbd in kernel-2.6.24+
- remove 32bit crack from x86_64 that made no sense

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.9.7-5
- Autorebuild for GCC 4.3

* Wed Nov 07 2007 Warren Togami <wtogami@redhat.com> 2.9.7-4
- include nbd-client i386 in x86-64 RPM because initrd images need it

* Sat Oct 13 2007 Eric Harrison <eharrison@mesd.k12.or.us> 2.9.7-3
- add buildrequires

* Sat Oct 13 2007 Eric Harrison <eharrison@mesd.k12.or.us> 2.9.7-2
- package cleanups

* Sat Oct 13 2007 Eric Harrison <eharrison@mesd.k12.or.us> 2.9.7-1
- update to 2.9.7

