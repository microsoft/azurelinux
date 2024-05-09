Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:             rtkit
Version:          0.11
Release:          24%{?dist}
Summary:          Realtime Policy and Watchdog Daemon
# The daemon itself is GPLv3+, the reference implementation for the client BSD
License:          GPLv3+ and BSD
URL:              https://git.0pointer.net/rtkit.git/
Requires:         dbus
Requires:         polkit
BuildRequires:    systemd
BuildRequires:    dbus-devel >= 1.2
BuildRequires:    libcap-devel
BuildRequires:    polkit-devel
BuildRequires:    autoconf automake libtool
Source0:          https://0pointer.de/public/%{name}-%{version}.tar.xz
Patch1:           rtkit-mq_getattr.patch
Patch2:           0001-SECURITY-Pass-uid-of-caller-to-polkit.patch
Patch3:           rtkit-controlgroup.patch

# Temporarily disable -Werror=format-security since it breaks the build
Patch4:           format-security.patch

%{?systemd_requires}

%description
RealtimeKit is a D-Bus system service that changes the
scheduling policy of user processes/threads to SCHED_RR (i.e. realtime
scheduling mode) on request. It is intended to be used as a secure
mechanism to allow real-time scheduling to be used by normal user
processes.

%prep
%autosetup -p1

%build
autoreconf -fvi
%configure --with-systemdsystemunitdir=/usr/lib/systemd/system
make V=1 %{?_smp_mflags}
./rtkit-daemon --introspect > org.freedesktop.RealtimeKit1.xml

%install
%make_install
install -Dm0644 org.freedesktop.RealtimeKit1.xml %{buildroot}%{_datadir}/dbus-1/interfaces/org.freedesktop.RealtimeKit1.xml

%pre
getent group rtkit >/dev/null 2>&1 || groupadd \
        -r \
        -g 172 \
        rtkit
getent passwd rtkit >/dev/null 2>&1 || useradd \
        -r -l \
        -u 172 \
        -g rtkit \
        -d /proc \
        -s /sbin/nologin \
        -c "RealtimeKit" \
        rtkit
:;

%post
%systemd_post rtkit-daemon.service
dbus-send --system --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ReloadConfig >/dev/null 2>&1 || :

%preun
%systemd_preun rtkit-daemon.service

%postun
%systemd_postun_with_restart rtkit-daemon.service

%files
%doc README GPL LICENSE rtkit.c rtkit.h
%attr(0755,root,root) %{_sbindir}/rtkitctl
%attr(0755,root,root) %{_libexecdir}/rtkit-daemon
%{_datadir}/dbus-1/system-services/org.freedesktop.RealtimeKit1.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.RealtimeKit1.xml
%{_datadir}/polkit-1/actions/org.freedesktop.RealtimeKit1.policy
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.RealtimeKit1.conf
%{_prefix}/lib/systemd/system/rtkit-daemon.service
%{_mandir}/man8/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.11-24
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug  2 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.11-22
- Fix %%systemd_postun macro use (#1736594)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct  9 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.11-20
- Modernize a bit and fix BuildRequires (#1637496)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 12 2017 Stephen Gallagher <sgallagh@redhat.com> - 0.11-15
- Temporarily disable -Werror=format-security to unbreak the build
- Build with verbose command-line visible in the logs
- Resolves: rhbz#1424270

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov  4 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.11-12
- Make dbus interface file non-executable (#1245938)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Nov 16 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.11-8
- Use a simpler patch for -lrt.
- Remove ControlGroup setting from the service file
  Resolves: #1010534
- Turn on hardening flags
  Resolves: #996735, #1008399

* Mon Sep 23 2013 Colin Walters <walters@verbum.org> - 0.11-7
- CVE-2013-4326
  Resolves: #1009543

* Thu Aug 22 2013 Colin Walters <walters@verbum.org> - 0.11-6
- Add patch to make this build again

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 14 2012 Lennart Poettering <lpoetter@redhat.com> - 0.11-3
- Make use of the new systemd macros

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Lennart Poettering <lpoetter@redhat.com> - 0.11-1
- New upstream release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Feb 17 2011 Lennart Poettering <lpoetter@redhat.com> - 0.10-1
- new upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug  4 2010 Lennart Poettering <lpoetter@redhat.com> - 0.9-2
- Convert systemd-install to systemctl

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> - 0.9-1
- New upstream release

* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> - 0.8-1
- New upstream release

* Fri Dec 18 2009 Lennart Poettering <lpoetter@redhat.com> - 0.5-1
- New release
- By default don't demote unknown threads
- Make messages less cute
- Fixes 530582

* Wed Aug 5 2009 Lennart Poettering <lpoetter@redhat.com> - 0.4-1
- New release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 2 2009 Lennart Poettering <lpoetter@redhat.com> - 0.3-1
- New release

* Wed Jun 17 2009 Lennart Poettering <lpoetter@redhat.com> - 0.2-1
- Initial packaging
