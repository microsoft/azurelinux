Summary:        SELinux Translation Daemon
Name:           mcstrans
Version:        3.2
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/SELinuxProject/selinux/wiki
Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:        secolor.conf.8
BuildRequires:  gcc
BuildRequires:  libcap-devel
BuildRequires:  libselinux-devel >= %{version}
BuildRequires:  libsepol-devel >= %{version}
BuildRequires:  pcre-devel
BuildRequires:  systemd
Requires:       pcre
Provides:       setransd = %{version}-%{release}
Provides:       libsetrans = %{version}-%{release}
Obsoletes:      libsetrans <= %{version}-%{release}
%{?systemd_requires}

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

mcstrans provides an translation daemon to translate SELinux categories
from internal representations to user defined representation.

%prep
%autosetup -p 1 -n mcstrans-%{version}

%build
%{set_build_flags}
%make_build LIBDIR="%{_libdir}" CFLAGS="%{build_cflags} -fno-semantic-interposition"

%install
mkdir -p %{buildroot}/%{_lib}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_datadir}/mcstrans
mkdir -p %{buildroot}%{_sysconfdir}/selinux/mls/setrans.d

%make_install LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" SBINDIR="%{_sbindir}" SYSTEMDDIR="/usr/lib/systemd"
rm -f %{buildroot}%{_libdir}/*.a
cp -r share/* %{buildroot}%{_datadir}/mcstrans/

# Systemd
rm -rf %{buildroot}/%{_sysconfdir}/rc.d/init.d/mcstrans
install -m644 %{SOURCE1} %{buildroot}%{_mandir}/man8/

%post
%systemd_post mcstrans.service

%preun
%systemd_preun mcstrans.service

%postun
%systemd_postun mcstrans.service

%files
%license COPYING
%{_mandir}/man8/mcs.8.gz
%{_mandir}/man8/mcstransd.8.gz
%{_mandir}/man5/setrans.conf.5.gz
%{_mandir}/ru/man8/mcs.8.gz
%{_mandir}/ru/man8/mcstransd.8.gz
%{_mandir}/ru/man5/setrans.conf.5.gz
%{_mandir}/man8/secolor.conf.8.gz
%{_sbindir}/mcstransd
%{_unitdir}/mcstrans.service
%dir %{_sysconfdir}/selinux/mls/setrans.d
%dir %{_datadir}/mcstrans

%defattr(0644,root,root,0755)
%dir %{_datadir}/mcstrans/util
%dir %{_datadir}/mcstrans/examples
%{_datadir}/mcstrans/examples/*

%defattr(0755,root,root,0755)
%{_datadir}/mcstrans/util/*

%changelog
* Fri Aug 13 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.2-1
- Upgrade to latest upstream version
- Add -fno-semantic-interposition to CFLAGS as recommended by upstream
- Update source URL to new format
- Lint spec
- License verified

* Thu Aug 27 2020 Daniel Burgener <daburgen@microsoft.com> - 2.9-3
- Initial CBL-Mariner import from Fedora 31 (license: MIT)
- License verified

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 19 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-1
- SELinux userspace 2.9 release

* Mon Mar 11 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-0.rc2.1
- SELinux userspace 2.9-rc2 release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-0.rc1.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-0.rc1.1
- Update to mcstrans-2.9-rc1

* Tue Oct  2 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-1
- Update to mcstrans-2.8

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 Karsten Hopp |karsten@redhat.com> - 0.3.4-4
- fix changelog order so that it builds with a recent rpm

* Wed Oct 16 2013 Dan Walsh <dwalsh@redhat.com> - 0.3.4-3
- Make mcstrans PIE and fully relro 
- Resolves: #983268

* Tue Oct 15 2013 Dan Walsh <dwalsh@redhat.com> - 0.3.4-2
- Add RELRO support for long running services

* Thu Sep 12 2013 Dan Walsh <dwalsh@redhat.com> - 0.3.4-1
- Update to latest version/applying patches
- Move binary to /usr/sbin rather then /sbin

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Dan Walsh <dwalsh@redhat.com> - 0.3.3-7
- Add secolor.conf.5 man page
- Make mcstransd watch for content being written to /run/setrans for files names containing translations.
-- This will allow apps like libvirt to write content nameing randomly selected MCS labels
- Fix memory leak in mcstransd

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 0.3.3-4
- Rebuild against PCRE 8.30

* Thu Feb 2 2012 Dan Walsh <dwalsh@redhat.com> - 0.3.3-3
- Fix the systemd service file

* Wed Feb 1 2012 Dan Walsh <dwalsh@redhat.com> - 0.3.3-2
- Update to upstream
- Write pid file

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Ted X Toth <txtoth@gmail.com> - 0.3.2-0
- Add constraints
- Add setrans.conf man page
- Fix mixed raw and translated range bug
- Moved todo comments to TODO file

* Fri Oct 16 2009 Dan Walsh <dwalsh@redhat.com> 0.3.1-4
- Add mcstransd man page

* Thu Sep 17 2009 Miroslav Grepl <mgrepl@redhat.com> 0.3.1-3
- Fix init script

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 5 2009 Joe Nall <joe@nall.com> 0.3.1-1
- Rewrite translations to allow individual word/category mapping
- Eamon Walsh's color mapping changes

* Wed May 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.2.11-2
- fix license tag

* Wed May 7 2008 Dan Walsh <dwalsh@redhat.com> 0.2.11-1
- More fixes from Jim Meyering

* Tue May 6 2008 Dan Walsh <dwalsh@redhat.com> 0.2.10-1
- More error checking on failed strdup

* Tue May 6 2008 Dan Walsh <dwalsh@redhat.com> 0.2.9-1
- Start mcstrans before netlabel

* Mon Apr 14 2008 Dan Walsh <dwalsh@redhat.com> 0.2.8-1
- Fix error handling

* Tue Feb 12 2008 Dan Walsh <dwalsh@redhat.com> 0.2.7-2
- Rebuild for gcc 4.3

* Tue Oct 30 2007 Steve Conklin <sconklin@redhat.com> - 0.2.7-1
- Folded current patches into tarball

* Thu Oct 25 2007 Steve Conklin <sconklin@redhat.com> - 0.2.6-3
- Fixed a compile problem with max_categories

* Thu Oct 25 2007 Steve Conklin <sconklin@redhat.com> - 0.2.6-2
- Fixed some init script errors

* Thu Sep 13 2007 Dan Walsh <dwalsh@redhat.com> 0.2.6-1
- Check for max_categories and error out

* Thu Mar 1 2007 Dan Walsh <dwalsh@redhat.com> 0.2.5-1
- Fix case where s0=""

* Mon Feb 26 2007 Dan Walsh <dwalsh@redhat.com> 0.2.4-1
- Translate range if fully specified correctly

* Mon Feb 12 2007 Dan Walsh <dwalsh@redhat.com> 0.2.3-1
- Additional fix to handle ssh root/sysadm_r/s0:c1,c2
Resolves: #224637

* Mon Feb 5 2007 Dan Walsh <dwalsh@redhat.com> 0.2.1-1
- Rewrite to handle MLS properly
Resolves: #225355

* Mon Jan 29 2007 Dan Walsh <dwalsh@redhat.com> 0.1.10-2
- Cleanup memory when complete

* Mon Dec 4 2006 Dan Walsh <dwalsh@redhat.com> 0.1.10-1
- Fix Memory Leak
Resolves: #218173

* Thu Sep 21 2006 Dan Walsh <dwalsh@redhat.com> 0.1.9-1
- Add -pie
- Fix compiler warnings
- Fix Memory Leak
Resolves: #218173

* Wed Sep 13 2006 Peter Jones <pjones@redhat.com> - 0.1.8-3
- Fix subsys locking in init script

* Wed Aug 23 2006 Dan Walsh <dwalsh@redhat.com> 0.1.8-1
- Only allow one version to run

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Mon Jun 19 2006 Dan Walsh <dwalsh@redhat.com> 0.1.7-1
- Apply sgrubb patch to only call getpeercon on translations

* Tue Jun 6 2006 Dan Walsh <dwalsh@redhat.com> 0.1.6-1
- Exit gracefully when selinux is not enabled

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> 0.1.5-1
- Fix sighup handling

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> 0.1.4-1
- Add patch from sgrubb
- Fix 64 bit size problems
- Increase the open file limit
- Make sure maximum size is not exceeded

* Fri May 12 2006 Dan Walsh <dwalsh@redhat.com> 0.1.3-1
- Move initscripts to /etc/rc.d/init.d

* Thu May 11 2006 Dan Walsh <dwalsh@redhat.com> 0.1.2-1
- Drop Privs

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> 0.1.1-1
- Initial Version
- This daemon reuses the code from libsetrans
