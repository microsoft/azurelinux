%{?!WITH_COMPAT_DNSSD:  %global WITH_COMPAT_DNSSD 1}
%{?!WITH_COMPAT_HOWL:   %global WITH_COMPAT_HOWL  1}
Summary:        Local network service discovery
Name:           avahi
Version:        0.8
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://avahi.org
Source0:        https://github.com/lathiat/avahi/releases/download/v%{version}/%{name}-%{version}.tar.gz
Patch0:         %{name}-libevent-pc-fix.patch
Patch1:         CVE-2021-3468.patch
Patch2:         CVE-2021-3502.patch
BuildRequires:  automake
BuildRequires:  dbus-devel >= 0.90
BuildRequires:  dbus-glib-devel >= 0.70
BuildRequires:  desktop-file-utils
BuildRequires:  expat-devel
BuildRequires:  gcc
BuildRequires:  gdbm-devel
BuildRequires:  glib2-devel
BuildRequires:  intltool
BuildRequires:  libcap-devel
BuildRequires:  libdaemon-devel >= 0.11
BuildRequires:  libevent-devel
BuildRequires:  libtool
BuildRequires:  perl-XML-Parser
BuildRequires:  pkg-config
BuildRequires:  systemd
BuildRequires:  xmltoman
BuildRequires:  pkgconfig(pygobject-3.0)
Requires:       %{name}-libs = %{version}-%{release}
Requires:       dbus
Requires:       expat
Requires:       libdaemon >= 0.11
# For /usr/bin/dbus-send
Requires(post): dbus
Requires(pre):  coreutils
Requires(pre):  shadow-utils
%{?systemd_requires}

%description
Avahi is a system which facilitates service discovery on
a local network -- this means that you can plug your laptop or
computer into a network and instantly be able to view other people who
you can chat with, find printers to print to or find files being
shared. This kind of technology is already found in MacOS X (branded
'Rendezvous', 'Bonjour' and sometimes 'ZeroConf') and is very
convenient.

%package        tools
Summary:        Command line tools for mDNS browsing and publishing
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}

%description tools
Command line tools that use avahi to browse and publish mDNS services.

%package        glib
Summary:        Glib libraries for avahi
Requires:       %{name}-libs = %{version}-%{release}

%description glib
Libraries for easy use of avahi from glib applications.

%package        glib-devel
Summary:        Libraries and header files for avahi glib development
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-glib = %{version}-%{release}
Requires:       glib2-devel

%description glib-devel
The avahi-devel package contains the header files and libraries
necessary for developing programs using avahi with glib.

%package        gobject
Summary:        GObject wrapper library for Avahi
Requires:       %{name}-glib = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}

%description gobject
This library contains a GObject wrapper for the Avahi API

%package        gobject-devel
Summary:        Libraries and header files for Avahi GObject development
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-gobject = %{version}-%{release}

%description gobject-devel
The avahi-gobject-devel package contains the header files and libraries
necessary for developing programs using avahi-gobject.

%package        libs
Summary:        Libraries for avahi run-time use

%description libs
The avahi-libs package contains the libraries needed
to run programs that use avahi.

%package        devel
Summary:        Libraries and header files for avahi development
# for libavahi-core
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}

%description devel
The avahi-devel package contains the header files and libraries
necessary for developing programs using avahi.

%if %{WITH_COMPAT_HOWL}
%package        compat-howl
Summary:        Libraries for howl compatibility
Requires:       %{name}-libs = %{version}-%{release}
Provides:       howl-libs = %{version}-%{release}

%description compat-howl
Libraries that are compatible with those provided by the howl package.

%package        compat-howl-devel
Summary:        Header files for development with the howl compatibility libraries
Requires:       %{name}-compat-howl = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}
Provides:       howl-devel = %{version}-%{release}

%description compat-howl-devel
Header files for development with the howl compatibility libraries.
%endif

%if %{WITH_COMPAT_DNSSD}
%package        compat-libdns_sd
Summary:        Libraries for Apple Bonjour mDNSResponder compatibility
Requires:       %{name}-libs = %{version}-%{release}

%description compat-libdns_sd
Libraries for Apple Bonjour mDNSResponder compatibility.

%package        compat-libdns_sd-devel
Summary:        Header files for the Apple Bonjour mDNSResponder compatibility libraries
Requires:       %{name}-compat-libdns_sd = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}

%description compat-libdns_sd-devel
Header files for development with the Apple Bonjour mDNSResponder compatibility
libraries.
%endif

%package        autoipd
Summary:        Link-local IPv4 address automatic configuration daemon (IPv4LL)
Requires:       %{name}-libs = %{version}-%{release}
Requires(pre):  shadow-utils

%description autoipd
avahi-autoipd implements IPv4LL, "Dynamic Configuration of IPv4
Link-Local Addresses"  (IETF RFC3927), a protocol for automatic IP address
configuration from the link-local 169.254.0.0/16 range without the need for a
central server. It is primarily intended to be used in ad-hoc networks which
lack a DHCP server.

%package        dnsconfd
Summary:        Configure local unicast DNS settings based on information published in mDNS
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}

%description dnsconfd
avahi-dnsconfd connects to a running avahi-daemon and runs the script
%{_sysconfdir}/avahi/dnsconfd.action for each unicast DNS server that is announced on the
local LAN. This is useful for configuring unicast DNS servers in a DHCP-like
fashion with mDNS.

%prep
%autosetup -p1
rm -fv docs/INSTALL

%build
# Use autogen to kill rpaths
rm -fv missing
NOCONFIGURE=1 ./autogen.sh

# Note that "--with-distro=none" is necessary to prevent initscripts from being installed
%configure \
        --with-distro=none \
        --disable-monodoc \
        --with-avahi-user=avahi \
        --with-avahi-group=avahi \
        --with-avahi-priv-access-group=avahi \
        --with-autoipd-user=avahi-autoipd \
        --with-autoipd-group=avahi-autoipd \
        --with-systemdsystemunitdir=%{_unitdir} \
        --enable-introspection=no \
        --enable-shared=yes \
        --enable-static=no \
        --disable-silent-rules \
	      --disable-python \
%if %{WITH_COMPAT_DNSSD}
        --enable-compat-libdns_sd \
%endif
%if %{WITH_COMPAT_HOWL}
        --enable-compat-howl \
%endif
        --disable-qt3 \
        --disable-qt4 \
        --disable-qt5 \
        --disable-gtk \
        --disable-gtk3 \
        --disable-mono \
;

# workaround parallel build issues (aarch64 only so far, bug #1564553)
%make_build -k V=1 || make V=1


%install
%make_install

# omit libtool .la files
find %{buildroot} -type f -name "*.la" -delete -print

# remove example
rm -fv %{buildroot}%{_sysconfdir}/avahi/services/ssh.service
rm -fv %{buildroot}%{_sysconfdir}/avahi/services/sftp-ssh.service

# create /var/run/avahi-daemon to ensure correct selinux policy for it:
mkdir -p %{buildroot}%{_localstatedir}/run/avahi-daemon
mkdir -p %{buildroot}%{_localstatedir}/lib/avahi-autoipd

# remove the documentation directory - let % doc handle it:
rm -rfv %{buildroot}%{_datadir}/%{name}-%{version}

# Make /etc/avahi/etc/localtime owned by avahi:
mkdir -p %{buildroot}%{_sysconfdir}/avahi/etc
touch %{buildroot}%{_sysconfdir}/avahi/etc/localtime

# fix bug 197414 - add missing symlinks for avahi-compat-howl and avahi-compat-dns-sd
%if %{WITH_COMPAT_HOWL}
ln -s avahi-compat-howl.pc  %{buildroot}/%{_libdir}/pkgconfig/howl.pc
%endif
%if %{WITH_COMPAT_DNSSD}
ln -s avahi-compat-libdns_sd.pc %{buildroot}/%{_libdir}/pkgconfig/libdns_sd.pc
ln -s avahi-compat-libdns_sd/dns_sd.h %{buildroot}/%{_includedir}/
%endif

# unpackaged files
rm -fv  %{buildroot}%{_datadir}/applications/{bssh,bvnc}.desktop
rm -fv  %{buildroot}%{_datadir}/avahi/interfaces/avahi-discover.ui

%find_lang %{name}


%check

%pre
getent group avahi >/dev/null || groupadd -f -g 70 -r avahi
if ! getent passwd avahi > /dev/null ; then
  if ! getent passwd 70 > /dev/null ; then
    useradd -r -l -u 70 -g avahi -d %{_localstatedir}/run/avahi-daemon -s %{_sbindir}/nologin -c "Avahi mDNS/DNS-SD Stack" avahi
  else
    useradd -r -l -g avahi -d %{_localstatedir}/run/avahi-daemon -s %{_sbindir}/nologin -c "Avahi mDNS/DNS-SD Stack" avahi
  fi
fi
exit 0

%post
%{?ldconfig}
%{_bindir}/dbus-send --system --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ReloadConfig >/dev/null 2>&1 || :
if [ "$1" -eq 1 -a -s %{_sysconfdir}/localtime ]; then
        %{_bindir}/cp -cfp %{_sysconfdir}/localtime %{_sysconfdir}/avahi/etc/localtime >/dev/null 2>&1 || :
fi
%systemd_post avahi-daemon.socket avahi-daemon.service

%preun
%systemd_preun avahi-daemon.socket avahi-daemon.service

%postun
%{?ldconfig}
%systemd_postun_with_restart avahi-daemon.socket avahi-daemon.service

%pre autoipd
getent group avahi-autoipd >/dev/null || groupadd -f -g 170 -r avahi-autoipd
if ! getent passwd avahi-autoipd > /dev/null ; then
  if ! getent passwd 170 > /dev/null; then
    useradd -r -u 170 -l -g avahi-autoipd -d %{_localstatedir}/lib/avahi-autoipd -s %{_sbindir}/nologin -c "Avahi IPv4LL Stack" avahi-autoipd
  else
    useradd -r -l -g avahi-autoipd -d %{_localstatedir}/lib/avahi-autoipd -s %{_sbindir}/nologin -c "Avahi IPv4LL Stack" avahi-autoipd
  fi
fi
exit 0

%post dnsconfd
%systemd_post avahi-dnsconfd.service

%preun dnsconfd
%systemd_preun avahi-dnsconfd.service

%postun dnsconfd
%systemd_postun_with_restart avahi-dnsconfd.service

%ldconfig_scriptlets glib

%ldconfig_scriptlets compat-howl

%ldconfig_scriptlets compat-libdns_sd

%ldconfig_scriptlets libs

%ldconfig_scriptlets ui

%ldconfig_scriptlets gobject

%files -f %{name}.lang
%doc docs/* avahi-daemon/example.service avahi-daemon/sftp-ssh.service avahi-daemon/ssh.service
%dir %{_sysconfdir}/avahi
%dir %{_sysconfdir}/avahi/etc
%ghost %{_sysconfdir}/avahi/etc/localtime
%config(noreplace) %{_sysconfdir}/avahi/hosts
%dir %{_sysconfdir}/avahi/services
%ghost %dir %{_localstatedir}/run/avahi-daemon
%config(noreplace) %{_sysconfdir}/avahi/avahi-daemon.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/avahi-dbus.conf
%{_sbindir}/avahi-daemon
%dir %{_datadir}/avahi
%{_datadir}/avahi/*.dtd
%dir %{_libdir}/avahi
%{_mandir}/man5/*
%{_mandir}/man8/avahi-daemon.*
%{_unitdir}/avahi-daemon.service
%{_unitdir}/avahi-daemon.socket
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.Avahi.service
%{_libdir}/libavahi-core.so.*

%files autoipd
%{_sbindir}/avahi-autoipd
%config(noreplace) %{_sysconfdir}/avahi/avahi-autoipd.action
%attr(1770,avahi-autoipd,avahi-autoipd) %dir %{_localstatedir}/lib/avahi-autoipd/
%{_mandir}/man8/avahi-autoipd.*

%files dnsconfd
%config(noreplace) %{_sysconfdir}/avahi/avahi-dnsconfd.action
%{_sbindir}/avahi-dnsconfd
%{_mandir}/man8/avahi-dnsconfd.*
%{_unitdir}/avahi-dnsconfd.service

%files tools
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%{_libdir}/libavahi-common.so
%{_libdir}/libavahi-core.so
%{_libdir}/libavahi-client.so
%{_libdir}/libavahi-libevent.so
%{_includedir}/avahi-client
%{_includedir}/avahi-common
%{_includedir}/avahi-core
%{_includedir}/avahi-libevent
%{_libdir}/pkgconfig/avahi-core.pc
%{_libdir}/pkgconfig/avahi-client.pc
%{_libdir}/pkgconfig/avahi-libevent.pc

%files libs
%doc README
%license LICENSE
%{_libdir}/libavahi-common.so.*
%{_libdir}/libavahi-client.so.*
%{_libdir}/libavahi-libevent.so.*

%files glib
%{_libdir}/libavahi-glib.so.*

%files glib-devel
%{_libdir}/libavahi-glib.so
%{_includedir}/avahi-glib
%{_libdir}/pkgconfig/avahi-glib.pc

%files gobject
%{_libdir}/libavahi-gobject.so.*

%files gobject-devel
%{_libdir}/libavahi-gobject.so
%{_includedir}/avahi-gobject
%{_libdir}/pkgconfig/avahi-gobject.pc

%if %{WITH_COMPAT_HOWL}
%files compat-howl
%{_libdir}/libhowl.so.*

%files compat-howl-devel
%{_libdir}/libhowl.so
%{_includedir}/avahi-compat-howl
%{_libdir}/pkgconfig/avahi-compat-howl.pc
%{_libdir}/pkgconfig/howl.pc
%endif

%if %{WITH_COMPAT_DNSSD}
%files compat-libdns_sd
%{_libdir}/libdns_sd.so.*

%files compat-libdns_sd-devel
%{_libdir}/libdns_sd.so
%{_includedir}/avahi-compat-libdns_sd
%{_includedir}/dns_sd.h
%{_libdir}/pkgconfig/avahi-compat-libdns_sd.pc
%{_libdir}/pkgconfig/libdns_sd.pc
%endif

%changelog
* Wed Apr 20 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.8-1
- Upgrade to latest upstream version to fix CVE-2017-6519
- Add upstream patch to fix CVE-2021-3502
- Add security researcher's patch to fix CVE-2021-3468
- Add nopatch for CVE-2021-26720
- Remove mono patch- we don't build with mono.
- Remove local services patch- upstreamed

* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.7-26
- License verified
- Lint spec

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7-25
- Making binaries paths compatible with CBL-Mariner's paths.

* Wed Nov 04 2020 Joe Schmitt <joschmit@microsoft.com> - 0.7-24
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove python, mono, gtk, gtk3, qt3, and qt4 dependencies.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 19 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.7-22
- drop python bindings/support (includes -ui-tools that use the bindings) on f31+ (#1751484)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7-21
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 22 2019 Michal Sekletár <msekleta@redhat.com> - 0.7-19
- add support for advertising services on the local machine only (i.e. on loopback)

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 0.7-18
- Update requires for pygobject3 -> python2-gobject rename

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 30 2018 Adam Williamson <awilliam@redhat.com> - 0.7-16
- Update python3 sed hack to avoid '/usr/bin/python32' dep

* Tue Jul 24 2018 Jan Grulich <jgrulich@redhat.com> - 0.7-15
- Requires: tigervnc
  Tigervnc removed old obsoleted provides

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7-13
- Rebuilt for Python 3.7

* Thu Apr 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.7-12
- use %%make_build %%ldconfig_scriptlets %%license
- %%build: --enable-shared=yes --enable-static=no --disable-silent-rules

* Thu Apr 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.7-11
- avahi-discover is missing "gi" module (#1564059)

* Mon Mar 19 2018 Michal Sekletar <msekleta@redhat.com> - 0.7-10
- add gcc to build reqs
- disable mono and qt support on RHEL

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 15 2017 Iryna Shcherbina <ishcherb@redhat.com> - 0.7-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Mon Dec 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.7-7
- %%check: validate .desktop files (#1524175)

* Tue Oct 24 2017 Merlin Mathesius <mmathesi@redhat.com> - 0.7-6
- Add option to disable qt4 support

* Sat Oct 07 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.7-5
- consistently use %%{_unitdir} macro

* Mon Oct 02 2017 Troy Dawson <tdawson@redhat.com> - 0.7-4
- Cleanup spec file conditionals

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.7-1
- avahi-0.7 (#1469100)
- rename python-avahi => python2-avahi

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.32-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 0.6.32-6
- Rebuild for Python 3.6

* Thu Oct 13 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.32-5
- rebuild - mono on aarch64

* Fri Aug 05 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.6.32-4
- -devel: fix typo in Requires: (#1364505)

* Thu Aug 04 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.6.32-3
- include dbus xml interfaces in main pkg, apparently used there for runtime introspection

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.32-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Apr 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.6.32-1
- 0.6.32 (final)

* Fri Mar 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.6.32-0.7.rc
- clean/simplify scriptlet deps (#1319207)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.32-0.6.rc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 21 2015 Rex Dieter <rdieter@fedoraproject.org> 0.6.32-0.5.rc
- enable use-ipv6=yes only for f24+

* Thu Nov 19 2015 Rex Dieter <rdieter@fedoraproject.org> 0.6.32-0.4.rc
- pull in upstream fixes, translations mostly (#1270332)

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.32-0.3.rc
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Nov  5 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.32-0.2.rc
- Modify a shebang in the python3 module so it doesn't drag in /usr/bin/python2.

* Sat Oct 10 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.6.32-0.1.rc
- avahi-0.6.32-rc
- -devel: move dbus-1/interfaces here
- Avahi's IPv6 support is disabled by default (#821127)
- avahi: script and/or trigger should not directly enable systemd units (#1094899)

* Tue Sep 22 2015 Rafael Fonseca <rdossant@redhat.com> - 0.6.31-43
- use %%{mono_arches} instead of hardcoded list

* Tue Sep 22 2015 Rex Dieter <rdieter@fedoraproject.org> 0.6.31-42
- treat "Invalid response packet from host" as avahi_log_debug (#1240711)

* Fri Sep 18 2015 Richard Hughes <rhughes@redhat.com> - 0.6.31-41
- Remove no longer required AppData file

* Thu Sep 17 2015 Rex Dieter <rdieter@fedoraproject.org> 0.6.31-40
- non-existing homedir /var/lib/avahi-autoipd (#1173822)

* Thu Sep 17 2015 Rex Dieter <rdieter@fedoraproject.org> 0.6.31-39
- Syslog Filled With "Invalid response packet from host" Message (#1240711)
- avahi-daemon manpage references file locations under /home/lennart/tmp (#991094)
- fix python-avahi dep botched in build -38

* Thu Sep 17 2015 Rex Dieter <rdieter@fedoraproject.org> 0.6.31-38
- pull in post 0.6.31 upstream fixes (#1246849), python related packaging polish

* Tue Jul 14 2015 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.6.31-37
- Add old patch from SuSE to fix 100%% CPU bug (RHBZ 952193).
- Don't install py2.7 .py{o,c} files in py3.4 package.

* Sun Jun 21 2015 Bastien Nocera <bnocera@redhat.com> 0.6.31-36
- Split off Python bindings, add Python3 support

* Wed Jun 17 2015 Michal Sekletar <msekleta@redhat.com> - 0.6.31-35
- check that rtnetlink messages has pid == 0, i.e. they sender is kernel (#1227052)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.31-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.31-33
- Rebuild (mono4)

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.6.31-32
- Rebuilt for GCC 5 C++11 ABI change

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 0.6.31-31
- Add an AppData file for the software center

* Thu Nov 27 2014 Peter Lemenkov <lemenkov@gmail.com> - 0.6.31-30
- Drop post-stage dependency on initscripts (rhbz #1168566). See also rhbz #182462.

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.31-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 26 2014 Bastien Nocera <bnocera@redhat.com> 0.6.31-28
- Disable publish-workstation= and publish-hinfo= by default (#1105647)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.31-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun  3 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.31-26
- Re-enable qt3 on aarch64

* Sat Mar 22 2014 Rex Dieter <rdieter@fedoraproject.org> 0.6.31-25
- support ppc64le (#1079392)

* Thu Jan 16 2014 Ville Skyttä <ville.skytta@iki.fi> - 0.6.31-24
- Drop INSTALL from docs, fix some trivial rpmlint warnings.

* Wed Jan  8 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.31-23
- Fix minor issue in exclude logic

* Tue Jan  7 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.31-22
- Add option to disable qt3 support (and disable on aarch64)

* Tue Oct 08 2013 Rex Dieter <rdieter@fedoraproject.org> 0.6.31-21
- avahi-libs should not require avahi, f20+ (#913168)

* Thu Sep 26 2013 Rex Dieter <rdieter@fedoraproject.org> 0.6.31-20
- conform to http://fedoraproject.org/wiki/Packaging/UsersAndGroups#Soft_static_allocation

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 0.6.31-19
- Make sure the split up -devel package require avahi-devel

* Sat Sep 21 2013 Kalev Lember <kalevlember@gmail.com> - 0.6.31-18
- Allow building with deprecated GTK+ symbols (#1001676)

* Fri Sep 20 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.6.31-17
- -libs: %%doc README LICENSE
- drop some explicit -devel deps, rely on automatic pkgconfig deps
- drop -Werror compiler flag
- cleanup/tighten subpkg deps
- trim changelog
- avahi-libs should not require avahi, f21+ (#913168)

* Thu Sep 19 2013 Rex Dieter <rdieter@fedoraproject.org> 0.6.31-16
- no hardened build (#1008395)

* Thu Sep 19 2013 Rex Dieter <rdieter@fedoraproject.org> 0.6.31-15
- Fix/workaround gtkstock.h deprecation (#1001676)

* Mon Aug 26 2013 Jon Ciesla <limburgher@gmail.com> - 0.6.31-14
- libmng rebuild.

* Wed Aug 14 2013 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.31-13
- Disable mono on aarch64 as it's not yet been ported

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.31-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Feb 02 2013 Kalev Lember <kalevlember@gmail.com> - 0.6.31-11
- Correct a typo in inter-subpackage deps

* Fri Feb  1 2013 Matthias Clasen <mclasen@redhat.com> - 0.6.31-10
- Tighten inter-subpackage deps

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 0.6.31-9
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.6.31-8
- fix path to ldconfig

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.6.31-7
- rebuild against new libjpeg

* Tue Aug  7 2012 Lennart Poettering <lpoetter@redhat.com> - 0.6.31-6
- Use new systemd macros
- Other modernizations

* Mon Aug 6 2012 Stef Walter <stefw@redhat.com> - 0.6.31-5
- Don't ship ssh service by default file since openssh-server isn't
  running by default, and shouldn't be advertised without user
  confirmation.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.31-3
- Merge F-17 into master
- ARM has mono

* Tue Feb 14 2012 Lennart Poettering <lpoetter@redhat.com> - 0.6.31-2
- Fix tarball

* Tue Feb 14 2012 Lennart Poettering <lpoetter@redhat.com> - 0.6.31-1
- New upstream release

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Christian Krause <chkr@fedoraproject.org> - 0.6.30-6
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> 0.6.30-5
- Rebuild to break bogus libpng dep

* Mon Aug 22 2011 Lennart Poettering <lpoetter@redhat.com> - 0.6.30-4
- Remove sysv init script (#714649)

* Thu May  5 2011 Bill Nottingham <notting@redhat.com> - 0.6.30-3
- fix versioning on triggers

* Tue May  3 2011 Lennart Poettering <lpoetter@redhat.com> - 0.6.30-2
- Enable Avahi by default
- https://bugzilla.redhat.com/show_bug.cgi?id=647831

* Mon Apr  4 2011 Lennart Poettering <lpoetter@redhat.com> - 0.6.30-1
- New upstream release

* Wed Mar  9 2011 Lennart Poettering <lpoetter@redhat.com> - 0.6.29-1
- New upstream release
- Fixes CVE-2011-1002 among other things

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.6.28-9
- Rebuild against new gtk

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.28-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 2 2011 Matthias Clasen <mclasen@redhat.com> - 0.6.28-7
- Rebuild against new gtk

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 0.6.28-6
- Rebuild against new gtk

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 0.6.28-5
- Rebuild against new gtk

* Wed Nov 24 2010 Dan Horák <dan[at]danny.cz> - 0.6.28-4
- Updated the archs without mono

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> - 0.6.28-3
- Rebuild against newer gtk3

* Wed Oct 27 2010 paul <paul@all-the-johnsons.co.uk> - 0.6.28-2
- rebuilt

* Tue Oct  5 2010 Lennart Poettering <lpoetter@redhat.com> - 0.6.28-1
- New upstream release

* Wed Aug  4 2010 Lennart Poettering <lpoetter@redhat.com> - 0.6.27-3
- convert from systemd-install to systemctl enable

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.27-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> 0.6.27-1
- New upstream release

* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> 0.6.26-4
- On request of Colin Walters, disable introspection again for now.

* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> 0.6.26-3
- Fix systemd unit installation

* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> 0.6.26-2
- Add missing dependencies

* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> 0.6.26-1
- New upstream release

* Mon Apr 19 2010 Bastien Nocera <bnocera@redhat.com> 0.6.25-7
- Split avahi libraries in -libs

* Mon Jan 25 2010 Lennart Poettering <lpoetter@redhat.com> - 0.6.25-6
- Move avahi-discover from avahi-tools to avahi-ui-tools
- https://bugzilla.redhat.com/show_bug.cgi?id=513768

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Karsten Hopp <karsten@redhat.com> 0.6.25-4
- Build *-sharp & *-ui-sharp for s390x

* Thu Jun 11 2009 Matthias Clasen <mclasen@redhat.com> - 0.6.25-4
- Use %%find_lang

* Tue May 26 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.25-3
- Create avahi-ui-sharp-devel package for pkgconfig dep-chain (#477308).

* Mon May 25 2009 Xavier Lamien <laxathom@fedoraproject.org> - 0.6.25-2
- Build arch ppc64 for *-sharp & *-ui-sharp.

* Mon Apr 13 2009 Lennart Poettering <lpoetter@redhat.com> - 0.6.25-1
- New upstream release

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Lennart Poettering <lpoetter@redhat.com> - 0.6.24-1
- New upstream release

* Wed Dec  3 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.22-13
- Fix libtool errors

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.22-12
- Rebuild for Python 2.6

* Wed Jun 04 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.6.22-11
- qt4 bindings (#446904)
- devel: BR: pkgconfig
- nuke rpaths

* Thu Mar 27 2008 Lennart Poettering <lpoetter@redhat.com> - 0.6.22-10
- Add release part to package dependencies (Closed #311601)

* Mon Mar 10 2008 Christopher Aillon <caillon@redhat.com> - 0.6.22-9
- The qt3 subpackage should (Build)Require: qt3

* Mon Mar 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.6.22-8
- updated (completed) German translation by Fabian Affolter (#427090)

* Thu Feb 21 2008 Adam Tkac <atkac redhat com> - 0.6.22-7
- really rebuild against new libcap

* Sun Feb 17 2008 Adam Tkac <atkac redhat com> - 0.6.22-6
- rebuild against new libcap

* Sat Feb 09 2008 Dennis Gilmore <dennis@ausil.us> - 0.6.22-5
- sparc64 does not have mono

* Tue Dec 18 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.6.22-4
- Make bvnc call vncviewer instead of xvncviewer
- Let ui-tools depend on necessary packages

* Mon Dec 17 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.22-3
- Add missing intltool dependency

* Mon Dec 17 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.22-2
- Fix mistag

* Mon Dec 17 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.22-1
- resolves #274731, #425491: New upstream version

* Tue Sep 25 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.21-6
- resolves #279301: fix segfault when no domains are configured in resolv.conf (pulled from upstream SVN r1525)

* Thu Sep 6 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.21-5
- resolves #249044: Update init script to use runlevel 96
- resolves #251700: Fix assertion in libdns_sd-compat

* Thu Sep 6 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.21-4
- Ship ssh static service file by default, don't ship ssh-sftp by default
- resolves: #269741: split off avahi-ui-tools package
- resolves: #253734: add missing dependency on avahi-glib-devel to avahi-ui-devel

* Tue Aug 28 2007 Martin Bacovsky <mbacovsk@redhat.com> - 0.6.21-3
- resolves: #246875: Initscript Review

* Sun Aug 12 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.21-2
- Fix avahi-browse --help output

* Sun Aug 12 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.21-1
- New upstream release

* Thu Aug 9 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.20-7
- Fix tagging borkage

* Thu Aug 9 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.20-6
- fix avahi-autoipd corrupt packet bug
- drop dependency on python for the main package

* Wed Jul 11 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.20-5
- add two patches which are important to get RR updating work properly.
  Will be part of upstream 0.6.21

* Thu Jul  5 2007 Dan Williams <dcbw@redhat.com> - 0.6.20-4
- Add Requires(pre): shadow-utils for avahi-autoipd package

* Mon Jun 25 2007 Bill Nottingham <notting@redhat.com> - 0.6.20-3
- fix %%endif typo

* Mon Jun 25 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.20-2
- add gtk-sharp2-devel to build deps

* Fri Jun 22 2007 Lennart Poettering <lpoetter@redhat.com> - 0.6.20-1
- upgrade to new upstream 0.6.20
- fix a few rpmlint warnings
- create avahi-autoipd user
- no longer create avahi user with a static uid, move to dynamic uids
- drop a couple of patches merged upstream
- Provide "howl" and "howl-devel"
- Split off avahi-autoipd and avahi-dnsconfd
- Introduce avahi-ui packages for the first time
- Reload D-Bus config after installation using dbus-send
- add a couple of missing ldconfig invocations

* Mon Mar 12 2007 Martin Bacovsky <mbacovsk@redhat.com> - 0.6.17-1
- upgrade to new upstream 0.6.17
- redundant patches removal
- removed auto* stuff from specfile since that was no longer needed
- Resolves: #232205: 'service {avahi-dnsconfd,avahi-daemon} status'
  returns 0 when the service is stopped

* Fri Feb  2 2007 Christopher Aillon <cailloN@redhat.com> - 0.6.16-3
- Remove bogus mono-libdir patches

* Tue Jan 23 2007 Jeremy Katz <katzj@redhat.com> - 0.6.16-2
- nuke bogus avahi-sharp -> avahi-devel dep

* Mon Jan 22 2007 Martin Bacovsky <mbacovsk@redhat.com> - 0.6.16-1.fc7
- Resolves: #221763: CVE-2006-6870 Maliciously crafted packed can DoS avahi daemon
- upgrade to new upstream
- patch revision
- Resolves: #218140: avahi configuration file wants a non-existent group

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 0.6.15-4
- rebuild against python 2.5

* Mon Nov 27 2006 Martin Bacovsky <mbacovsk@redhat.com> - 0.6.15-3
- automake-1.10 required for building

* Mon Nov 27 2006 Martin Bacovsky <mbacovsk@redhat.com> - 0.6.15-2
- automake-1.9 required for building

* Thu Nov 24 2006 Martin Bacovsky <mbacovsk@redhat.com> - 0.6.15-1
- Upgrade to 0.6.15
- patches revision

* Mon Sep 18 2006 Martin Stransky <stransky@redhat.com> - 0.6.11-6
- added patch from #206445 - ia64: unaligned access errors seen
  during startup of avahi-daemon
- removed unused patches

* Thu Sep 7 2006 Dan Walsh <dwalsh@redhat.com> - 0.6.11-5
- Maintain the security context on the localtime file

* Wed Aug 23 2006 Martin Stransky <stransky@redhat.com> - 0.6.11-4
- fix for #204710 - /etc/init.d/avahi-dnsconfd missing line
  continuation slash (\) in description

* Wed Aug 23 2006 Martin Stransky <stransky@redhat.com> - 0.6.11-3
- added fix for #200767 - avahi-dnsconfd Segmentation fault
  with invalid command line argument
- added dist tag

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.6.11-2.fc6
- add BR for dbus-glib-devel
- fix deprecated functions

* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.11-1.fc6
- Upgrade to upstream version 0.6.11
- fix bug 195674: set 'use-ipv6=yes' in avahi-daemon.conf
- fix bug 197414: avahi-compat-howl and avahi-compat-dns-sd symlinks
- fix bug 198282: avahi-compat-{howl-devel,dns-sd-devel} Requires:

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Tue Jun 13 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.10-3.FC6
- rebuild for broken mono deps

* Tue Jun 06 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.10-2.FC6
- fix bug 194203: fix permissions on /var/run/avahi-daemon

* Tue May 30 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.10-1.FC6
- Upgrade to upstream version 0.6.10
- fix bug 192080: split avahi-compat-libdns_sd into separate package
                  (same goes for avahi-compat-howl)

* Tue May 02 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.9-9.FC6
- fix avahi-sharp issues for banshee - patches from caillon@redhat.com

* Thu Apr 20 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.9-9.FC6
- fix bug 189427: correct avahi-resolve --help typo

* Mon Mar 20 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.9-8.FC6
- fix bug 185972: remove ellipses in initscript
- fix bug 185965: make chkconfigs unconditional

* Thu Mar 16 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.9-6
- Fix bug 185692: install avahi-sharp into %%{_prefix}/lib, not %%{_libdir}

* Thu Mar 09 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.9-4
- fix scriptlet error introduced by last fix:
  if user has disabled avahi-daemon, do not enable it during post

* Wed Mar 08 2006 Bill Nottingham <notting@redhat.com> - 0.6.9-2
- fix scriplet error during installer
- move service-types* to the tools package (avoids multilib conflicts)

* Tue Mar 07 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.9-1
- Upgrade to upstream version 0.6.9

* Thu Feb 23 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.8-1
- Upgrade to upstream version 0.6.8
- fix bug 182462: +Requires(post): initscripts, chkconfig, ldconfig

* Fri Feb 17 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.7-1
- Upgrade to upstream version 0.6.7

* Fri Feb 17 2006 Karsten Hopp <karsten@redhat.de> - 0.6.6-4
- BuildRequires pygtk2

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.6.6-3.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.6-3
- rebuild for new gcc (again)
- further fix for bug 178746: fix avahi-dnsconfd initscript

* Tue Feb 07 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.6-2
- rebuild for new gcc, glibc, glibc-kernheaders

* Wed Feb 01 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.6-1
- fix bug 179448: mis-alignment of input cmsghdr msg->msg_control buffer on ia64
- Upgrade to 0.6.6

* Thu Jan 26 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.5-1
- Upgrade to upstream version 0.6.5
- Make /etc/avahi/etc and /etc/avahi/etc/localtime owned by avahi
  package; copy system localtime into chroot in post

* Mon Jan 23 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.4-4
- fix bug 178689: copy localtime to chroot
- fix bug 178784: fix avahi-dnsconfd initscript

* Fri Jan 20 2006 Peter Jones <pjones@redhat.com> - 0.6.4-3
- fix subsystem locking in the initscript

* Thu Jan 19 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.4-2
- fix bug 178127: fully localize the initscript

* Mon Jan 16 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.4-1
- Upgrade to upstream version 0.6.4

* Thu Jan 12 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.3-2
- fix bug 177610: Enable mono support with new avahi-sharp package
- fix bug 177609: add gdbm / gdbm-devel Requires for avahi-browse

* Mon Jan 09 2006 Jason Vas Dias <jvdias@redhat.com> - 0.6.3-1
- Upgrade to upstream version 0.6.3
- fix bug 177148: initscript start should not fail if avahi-daemon running

* Thu Dec 22 2005 Jason Vas Dias <jvdias@redhat.com> - 0.6.1-3
- move initscripts from /etc/init.d to /etc/rc.d/init.d

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec 09 2005 Jason Vas Dias<jvdias@redhat.com> - 0.6.1-2
- fix bug 175352: Do not chkconfig --add avahi-daemon
  if user has already configured it

* Wed Dec 07 2005 Jason Vas Dias<jvdias@redhat.com> - 0.6.1-1
- Upgrade to 0.6.1

* Mon Dec 05 2005 Jason Vas Dias<jvdias@redhat.com> - 0.6-6
- fix bug 174799 - fix .spec file files permissions

* Fri Dec 02 2005 Jason Vas Dias<jvdias@redhat.com> - 0.6-5
- python-twisted has been removed from the FC-5 distribution - disable its use

* Thu Dec 01 2005 Jason Vas Dias<jvdias@redhat.com> - 0.6-4
- Rebuild for dbus-0.6 - remove use of DBUS_NAME_FLAG_PROHIBIT_REPLACEMENT

* Wed Nov 30 2005 Jason Vas Dias<jvdias@redhat.com> - 0.6-3
- fix bug 172047 - tools should require python-twisted
- fix bug 173985 - docs directory permissions

* Mon Nov 21 2005 Jason Vas Dias<jvdias@redhat.com> - 0.6-1
- Upgrade to upstream version 0.6 - now provides 'avahi-howl-compat'
  libraries / includes.

* Mon Nov 14 2005 Jason Vas Dias<jvdias@redhat.com> - 0.5.2-7
- fix bug 172034: fix ownership of /var/run/avahi-daemon/
- fix bug 172772: .spec file improvements from matthias@rpmforge.net

* Mon Oct 31 2005 Jason Vas Dias<jvdias@redhat.com> - 0.5.2-6
- put back avahi-devel Obsoletes: howl-devel

* Mon Oct 31 2005 Alexander Larsson <alexl@redhat.com> - 0.5.2-5
- Obsoletes howl, howl-libs, as we want to get rid of them on updates
- No provides yet, as the howl compat library is in Avahi 0.6.0.

* Sun Oct 30 2005 Florian La Roche <laroche@redhat.com>
- disable the Obsoletes: howl until the transition is complete

* Fri Oct 28 2005 Jason Vas Dias<jvdias@redhat.com> - 0.5.2-3
- change initscript to start avahi-daemon AFTER messagebus

* Wed Oct 26 2005 Karsten Hopp <karsten@redhat.de> 0.5.2-2
- add buildrequires dbus-python

* Fri Oct 21 2005 Alexander Larsson <alexl@redhat.com> - 0.5.2-1
- Initial package
