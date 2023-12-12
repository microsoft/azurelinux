%bcond_with selinux
%bcond_with systemd

Vendor:         Microsoft Corporation
Distribution:   Mariner

%if %{with selinux}
%global selinuxtype targeted
%endif

%global moduletype contrib
%define semodule_version 0.0.4

Name:           usbguard
Version:        1.1.0
Release:        1%{?dist}
Summary:        A tool for implementing USB device usage policy
License:        GPLv2+
## Not installed
# src/ThirdParty/Catch: Boost Software License - Version 1.0
URL:            https://usbguard.github.io/
Source0:        https://github.com/USBGuard/usbguard/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%if %{with selinux}
Source1:        https://github.com/USBGuard/usbguard/releases/download/%{name}-selinux-%{semodule_version}/%{name}-selinux-%{semodule_version}.tar.gz
%endif
Source2:        usbguard-daemon.conf

%if %{with systemd}
Requires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
%if %{with selinux}
Recommends: %{name}-selinux
%endif
Obsoletes: %{name}-applet-qt < 0.7.6

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libqb-devel
BuildRequires: libgcrypt-devel
BuildRequires: libstdc++-devel
BuildRequires: protobuf-devel
BuildRequires: PEGTL-static
BuildRequires: catch-devel
BuildRequires: autoconf automake libtool
BuildRequires: bash-completion
BuildRequires: asciidoc
BuildRequires: audit-libs-devel
# For `pkg-config systemd` only
BuildRequires: systemd

Patch1: usbguard-0.7.6-libqb.patch

%description
The USBGuard software framework helps to protect your computer against rogue USB
devices by implementing basic whitelisting/blacklisting capabilities based on
USB device attributes.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       libstdc++-devel


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        tools
Summary:        USBGuard Tools
Requires:       %{name} = %{version}-%{release}

%description    tools
The %{name}-tools package contains optional tools from the USBGuard
software framework.


# dbus
%package        dbus
Summary:        USBGuard D-Bus Service
Requires:       %{name} = %{version}-%{release}
BuildRequires:	dbus-glib-devel
BuildRequires:	dbus-devel
BuildRequires:	glib2-devel
BuildRequires:	polkit-devel
BuildRequires:	libxslt
BuildRequires:	libxml2
Requires:       dbus
Requires:       polkit

%description    dbus
The %{name}-dbus package contains an optional component that provides
a D-Bus interface to the USBGuard daemon component.

%if %{with selinux}
%package        selinux
Summary:        USBGuard selinux
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}
BuildRequires:  selinux-policy
BuildRequires:  selinux-policy-devel
BuildArch: noarch
%{?selinux_requires}

%description    selinux
The %{name}-selinux package contains selinux policy for the USBGuard
daemon.
%endif

# usbguard
%prep
%setup -q

%if %{with selinux}
# selinux
%setup -q -D -T -a 1
%endif

%patch1 -p1 -b .libqb

# Remove bundled library sources before build
rm -rf src/ThirdParty/{Catch,PEGTL}


%build
mkdir -p ./m4
autoreconf -i -v --no-recursive ./
%configure \
    --disable-silent-rules \
    --without-bundled-catch \
    --without-bundled-pegtl \
%if %{with systemd}
    --enable-systemd \
%else
    --disable-systemd \
%endif
    --with-dbus \
    --with-polkit \
    --with-crypto-library=gcrypt

make %{?_smp_mflags}

%if %{with selinux}
# selinux
pushd %{name}-selinux-%{semodule_version}
make
popd
%endif

%check
make check


%if %{with selinux}
# selinux
%pre selinux
%selinux_relabel_pre -s %{selinuxtype}
%endif

%install
make install INSTALL='install -p' DESTDIR=%{buildroot}

# Overwrite configuration with distribution defaults
mkdir -p %{buildroot}%{_sysconfdir}/usbguard
mkdir -p %{buildroot}%{_sysconfdir}/usbguard/IPCAccessControl.d
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/usbguard/usbguard-daemon.conf

%if %{with selinux}
# selinux
install -d %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}
install -m 0644 %{name}-selinux-%{semodule_version}/%{name}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}
install -d -p %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -p -m 644 %{name}-selinux-%{semodule_version}/%{name}.if %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}/ipp-%{name}.if
%endif

# Cleanup
find %{buildroot} \( -name '*.la' -o -name '*.a' \) -exec rm -f {} ';'

%if %{with systemd}
%preun
%systemd_preun usbguard.service
%endif

%post
%{?ldconfig}
%if %{with systemd}
%systemd_post usbguard.service
%endif

%postun
%{?ldconfig}
%if %{with systemd}
%systemd_postun usbguard.service
%endif

%files
%doc README.adoc CHANGELOG.md
%license LICENSE
%{_libdir}/*.so.*
%{_sbindir}/usbguard-daemon
%{_bindir}/usbguard
%dir %{_localstatedir}/log/usbguard
%dir %{_sysconfdir}/usbguard
%dir %{_sysconfdir}/usbguard/IPCAccessControl.d
%config(noreplace) %attr(0600,-,-) %{_sysconfdir}/usbguard/usbguard-daemon.conf
%config(noreplace) %attr(0600,-,-) %{_sysconfdir}/usbguard/rules.conf
%{_datadir}/man/man8/usbguard-daemon.8.gz
%{_datadir}/man/man5/usbguard-daemon.conf.5.gz
%{_datadir}/man/man5/usbguard-rules.conf.5.gz
%{_datadir}/man/man1/usbguard.1.gz
%{_datadir}/bash-completion/completions/usbguard
%if %{with systemd}
%{_unitdir}/usbguard.service
%endif

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files tools
%{_bindir}/usbguard-rule-parser

# dbus
%files dbus
%{_sbindir}/usbguard-dbus
%{_datadir}/dbus-1/system-services/org.usbguard1.service
%{_datadir}/dbus-1/system.d/org.usbguard1.conf
%{_datadir}/polkit-1/actions/org.usbguard1.policy
%{_mandir}/man8/usbguard-dbus.8.gz
%if %{with systemd}
%{_unitdir}/usbguard-dbus.service
%endif

%if %{with systemd}
%preun dbus
%systemd_preun usbguard-dbus.service

%post dbus
%systemd_post usbguard-dbus.service

%postun dbus
%systemd_postun_with_restart usbguard-dbus.service
%endif

%if %{with selinux}
%files selinux
%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2
%ghost %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{name}
%{_datadir}/selinux/devel/include/%{moduletype}/ipp-%{name}.if

%post selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{name}
fi

%posttrans selinux
%selinux_relabel_post -s %{selinuxtype}
%endif

%changelog
* Tue Sep 05 2023 Archana Choudhary <archana1@microsoft.com> - 1.1.0-1
- Upgrade to 1.1.0 - CVE-2019-25058
- Update build requirement catch1 -> catch
- License verified

* Wed Aug 11 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Disabling the 'selinux' subpackage to remove BR on 'policy-selinux'.
- Disabling building with systemd.
- Removing BR on 'protobuf-compiler'.

* Thu Jan 14 2021 Zoltan Fridrich <zfridric@redhat.com> - 1.0.0-1
- rebase usbguard to 1.0.0
- added support for rules covering combination of classes
- fix usbguard being killed
Resolves: rhbz#1916039
Resolves: rhbz#1861330
Resolves: rhbz#1905257

* Wed Jun 24 2020 Radovan Sroka <rsroka@redhat.com> - 0.7.8-3
- rebase usbguard to 0.7.8
- rebase selinux tarball to v0.0.4
- enable forking style in unit file
- added rules.d/ directory
- set DevicePolicy to closed in unit file
- usbguard prevented from writing conf via dontaudit rule
Resolves: rhbz#1804713
Resolves: rhbz#1789923
Resolves: rhbz#1808527

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 19 2019 Orion Poplawski <orion@nwra.com> - 0.7.6-7
- Rebuild for protobuf 3.11

* Wed Dec 18 2019 Radovan Sroka <rsroka@redhat.com> - 0.7.6-6
- fix selinux problems

* Mon Dec 02 2019 Radovan Sroka <rsroka@redhat.com> - 0.7.6-5
- obsolete applet-qt subpackage

* Mon Nov 25 2019 Attila Lakatos <alakatos@redhat.com> - 0.7.6-4
- added patch for libqb related permission issues
  resolves: rhbz#1776357
- added patch to ensure that usbguard-daemons is still running after locked screen
  resolves: rhbz#1751861
- added patch to fix permanent device policy changes

* Wed Nov 13 2019 Radovan Sroka <rsroka@redhat.com> - 0.7.6-3
- fixed typo in specfile
- usbguard.conf was generated incorrectly

* Wed Nov 13 2019 Radovan Sroka <rsroka@redhat.com> - 0.7.6-2
- added selinux subpackage

* Mon Nov 11 2019 Radovan Sroka <rsroka@redhat.com> - 0.7.6-1
- rebase to 0.7.6
- removed usbguard-applet subpackage which is not in upstream anymore

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 21 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.2-6
- Rebuild for protobuf 3.6

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 05 2018 Daniel Kopeček <dkopecek@redhat.com> - 0.7.2-4
- Update to latest PEGTL API

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Daniel Kopeček <dkopecek@redhat.com> - 0.7.2-2
- Escape rpm macros mentioned in changelog section

* Tue Jan 23 2018 Daniel Kopeček <dkopecek@redhat.com> - 0.7.2-1
- Update to 0.7.2
- Don't use --enable-werror downstream
- Removed patches related to compiler warnings

* Mon Jan 15 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.1-2
- catch → catch1

* Wed Dec 06 2017 Daniel Kopeček <dkopecek@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Wed Nov 29 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.7.0-9
- Rebuild for protobuf 3.5

* Mon Nov 13 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.0-8
- Rebuild for protobuf 3.4

* Mon Oct 16 2017 Daniel Kopeček <dkopecek@redhat.com> 0.7.0-7
- Fix enumeration timeout on kernel >= 4.13
  Resolves: rhbz#1499052

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Daniel Kopeček <dkopecek@redhat.com> 0.7.0-4
- Added patch to disable unused parameter warning for protobuf
  generated sources to fix compilation with newer protobuf version

* Tue Jun 13 2017 Orion Poplawski <orion@cora.nwra.com> - 0.7.0-3
- Rebuild for protobuf 3.3.1

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Thu Apr 13 2017 Daniel Kopeček <dkopecek@redhat.com> 0.7.0-1
- Update to 0.7.0
  - changed PresentDevicePolicy setting from keep to apply-policy
  - added AuditFilePath configuration option pointing to
    /var/log/usbguard/usbguard-audit.log file
  - install bash-completion script
  - use 0600 file permissions for usbguard-daemon.conf and rules.conf

* Sun Mar 19 2017 Daniel Kopeček <dkopecek@redhat.com> 0.6.3-0.1.20170319
- Update to latest git snapshot

* Fri Mar 17 2017 Daniel Kopeček <dkopecek@redhat.com> 0.6.3-0.1.20170317
- Update to latest git snapshot
- Use --enable-werror configure option as the upstream default
  changed to not use -Werror.

* Thu Mar 02 2017 Daniel Kopeček <dkopecek@redhat.com> 0.6.3-0.1.20170301
- Update to latest git snapshot
- Disabled upstream alignment warning compiler flag

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Orion Poplawski <orion@cora.nwra.com> - 0.6.2-3
- Rebuild for protobuf 3.2.0

* Sat Nov 19 2016 Orion Poplawski <orion@cora.nwra.com> - 0.6.2-2
- Rebuild for protobuf 3.1.0

* Sun Sep 18 2016 Daniel Kopeček <dkopecek@redhat.com> 0.6.2-1
- Update to 0.6.2

* Fri Sep 16 2016 Daniel Kopeček <dkopecek@redhat.com> 0.6.1-1
- Update to 0.6.1

* Sun Sep 04 2016 Daniel Kopeček <dkopecek@redhat.com> 0.6.0-1
- Update to 0.6.0

* Thu Aug 18 2016 Daniel Kopeček <dkopecek@redhat.com> 0.5.14-1
- Update to 0.5.14

* Tue Aug 16 2016 Daniel Kopeček <dkopecek@redhat.com> 0.5.13-1
- Update to 0.5.13

* Sun Aug 14 2016 Daniel Kopeček <dkopecek@redhat.com> 0.5.12-1
- Update to 0.5.12

* Sat Aug 13 2016 Daniel Kopeček <dkopecek@redhat.com> 0.5.11-2
- Update source tarball
- Ship CHANGELOG.md

* Sat Aug 13 2016 Daniel Kopeček <dkopecek@redhat.com> 0.5.11-1
- Update to 0.5.11
- Use libgcrypt instead of libsodium for crypto

* Thu Jul 21 2016 Daniel Kopecek <dkopecek@redhat.com> 0.5.10-2
- Adjust the default configuration to keep the authorization state
  of present controller devices.

* Sat Jul 09 2016 Daniel Kopecek <dkopecek@redhat.com> 0.5.10-1
- Update to release 0.5.10

* Mon Mar 07 2016 Remi Collet <remi@fedoraproject.org> - 0.4-5
- rebuild for new libsodium soname

* Sun Feb 07 2016 Daniel Kopecek <dkopecek@redhat.com> 0.4-4
- Update to version 0.4
- added usbguard CLI
- added a tools subpackage with usbguard-rule-parser binary

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3p3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3p3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Daniel Kopecek <dkopecek@redhat.com> 0.3p3-1
- Update to version 0.3p3
- added %%check section
- removed explicit -devel requires on systemd, libqb and
  libsodium devel files
- added -devel requires on libstdc++-devel

* Sat Apr 11 2015 Daniel Kopecek <dkopecek@redhat.com> 0.3p2-1
- Update to version 0.3p2
- use system-wide json and spdlog packages

* Fri Apr 10 2015 Daniel Kopecek <dkopecek@redhat.com> 0.3p1-1
- Update to version 0.3p1
- removed bundled cppformat copylib

* Thu Apr 09 2015 Daniel Kopecek <dkopecek@redhat.com> 0.3-1
- Update to version 0.3
- disabled silent rules
- install license file
- added man pages
- use _hardened_build 1 instead of custom compilation flags
- fix file permissions on files in /etc
- do not install an empty rule set file

* Fri Apr 03 2015 Daniel Kopecek <dkopecek@redhat.com> 0.2-1
- Update to version 0.2
- Updated description
- Corrected package group

* Tue Mar 17 2015 Daniel Kopecek <dkopecek@redhat.com> 0.1-1
- Initial package
