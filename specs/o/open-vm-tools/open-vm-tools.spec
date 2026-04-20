## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

################################################################################
### Copyright 2013-2024 Broadcom. All rights reserved.
### The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.
###
### RPM SPEC file for building open-vm-tools packages.
###
###
### This program is free software; you can redistribute it and/or modify
### it under the terms of version 2 of the GNU General Public License as
### published by the Free Software Foundation.
###
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
###
### You should have received a copy of the GNU General Public License
### along with this program; if not, write to the Free Software
### Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
################################################################################

%global toolsbuild      25056151
%global toolsdaemon     vmtoolsd
%global vgauthdaemon    vgauthd

Name:             open-vm-tools
Version:          13.0.10
Release:          %autorelease
Summary:          Open Virtual Machine Tools for virtual machines hosted on VMware
License:          GPL-2.0-only AND W3C AND LGPL-2.1-only AND ICU AND ISC AND MIT
URL:              https://github.com/vmware/%{name}

Source0:          https://github.com/vmware/%{name}/releases/download/stable-%{version}/%{name}-%{version}-%{toolsbuild}.tar.gz
Source1:          %{toolsdaemon}.service
Source2:          %{vgauthdaemon}.service
Source3: run-vmblock-fuse.mount.in
Source4:          open-vm-tools.conf
Source5:          vmtoolsd.pam

Patch0:           open-vm-tools-gcc16.patch

ExclusiveArch:    %{ix86} x86_64 aarch64

BuildRequires:    autoconf
BuildRequires:    automake
BuildRequires:    libtool
BuildRequires:    make
BuildRequires:    gcc-c++
BuildRequires:    doxygen
BuildRequires:    fuse3-devel >= 3.10.0
BuildRequires:    libtool-ltdl-devel
BuildRequires:    libX11-devel
BuildRequires:    libXext-devel
BuildRequires:    libXi-devel
BuildRequires:    libXinerama-devel
BuildRequires:    libXrandr-devel
BuildRequires:    libXrender-devel
BuildRequires:    libXtst-devel
BuildRequires:    pam-devel
BuildRequires:    pkgconfig(glib-2.0) >= 2.34.0
BuildRequires:    pkgconfig(gmodule-2.0) >= 2.34.0
BuildRequires:    pkgconfig(gobject-2.0) >= 2.34.0
BuildRequires:    pkgconfig(gthread-2.0) >= 2.34.0
BuildRequires:    pkgconfig(gtk+-3.0) >= 3.0.0
BuildRequires:    pkgconfig(gtkmm-3.0) >= 3.0.0
BuildRequires:    pkgconfig(icu-i18n)
BuildRequires:    pkgconfig(libdrm)
BuildRequires:    pkgconfig(libmspack) >= 0.0.20040308alpha
BuildRequires:    pkgconfig(libudev)
BuildRequires:    pkgconfig(libtirpc)
BuildRequires:    pkgconfig(openssl)
BuildRequires:    pkgconfig(protobuf) >= 3.0.0
BuildRequires:    procps-devel
BuildRequires:    rpcgen
# Required otherwise udev rules are not built:
BuildRequires:    systemd-udev
BuildRequires:    xmlsec1-openssl-devel

Requires:         coreutils
Requires:         fuse3
Requires:         grep
Requires:         iproute
Requires:         pciutils
Requires:         sed
Requires:         tar
Requires:         util-linux
Requires:         which
# xmlsec1-openssl needs to be added explicitly
Requires:         xmlsec1-openssl

# open-vm-tools >= 10.0.0 do not require open-vm-tools-deploypkg provided by
# VMware. That functionality is now available as part of open-vm-tools package
# itself.
Obsoletes:        open-vm-tools-deploypkg <= 10.0.5

%description
The %{name} project is an open source implementation of VMware Tools. It
is a suite of open source virtualization utilities and drivers to improve the
functionality, user experience and administration of VMware virtual machines.
This package contains only the core user-space programs and libraries of
%{name}.

%package          desktop
Summary:          User experience components for Open Virtual Machine Tools
Requires:         %{name}%{?_isa} = %{version}-%{release}

%description      desktop
This package contains only the user-space programs and libraries of
%{name} that are essential for improved user experience of VMware virtual
machines.

%package          sdmp
Summary:          Service Discovery components for Open Virtual Machine Tools
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         coreutils
Requires:         gawk
Requires:         glibc-common
Requires:         grep
Requires:         iproute
Requires:         procps

%description      sdmp
This package contains only the user-space programs and utility scripts of
%{name} that are essential for performing service discovery in VMware
virtual machines by vRealize Operations Service Discovery Management Pack.

%package          salt-minion
Summary:          Script file to install/uninstall salt-minion
Requires:         %{name}%{?_isa} = %{version}-%{release}, systemd, curl, coreutils, gawk, grep
ExclusiveArch:    x86_64

%description      salt-minion
This package contains a script to setup Salt Minion on VMware virtual machines.

%package          devel
Summary:          Development libraries for Open Virtual Machine Tools
Requires:         %{name}%{?_isa} = %{version}-%{release}

%description      devel
This package contains only the user-space programs and libraries of
%{name} that are essential for developing customized applications for
VMware virtual machines.

%package          test
Summary:          Test utilities for Open Virtual Machine Tools
Requires:         %{name}%{?_isa} = %{version}-%{release}

%description      test
This package contains only the test utilities for %{name} that are
useful for verifying the functioning of %{name} in VMware virtual
machines.

%prep
%autosetup -p1 -n %{name}-%{version}-%{toolsbuild}

%build
autoreconf -vif

%configure \
    --enable-resolutionkms \
    --enable-servicediscovery \
%ifarch x86_64
    --enable-salt-minion \
%endif
    --enable-vmwgfxctrl \
    --with-fuse \
    --with-tirpc \
    --with-xmlsec1 \
    --without-gtk2 \
    --without-gtkmm \
    --without-kernel-modules \
    --disable-static

sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build

%install
%make_install

# Remove exec bit from config files
chmod a-x %{buildroot}%{_sysconfdir}/pam.d/*
chmod a-x %{buildroot}%{_sysconfdir}/vmware-tools/*.conf
chmod a-x %{buildroot}%{_sysconfdir}/vmware-tools/vgauth/schemas/*

# Remove exec bit on udev rules.
chmod a-x %{buildroot}%{_udevrulesdir}/99-vmware-scsi-udev.rules

# Remove the DOS line endings
sed -i "s|\r||g" README

# Remove "Encoding" key from the "Desktop Entry"
sed -i "s|^Encoding.*$||g" %{buildroot}%{_sysconfdir}/xdg/autostart/vmware-user.desktop

# Remove unnecessary files from packaging
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -fr %{buildroot}%{_defaultdocdir}
rm -f docs/api/build/html/FreeSans.ttf

# Systemd unit files
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_unitdir}/%{toolsdaemon}.service
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_unitdir}/%{vgauthdaemon}.service
install -p -m 644 -D '%{SOURCE3}' %{buildroot}%{_unitdir}/run-vmblock\\x2dfuse.mount
install -p -m 644 -D %{SOURCE4} %{buildroot}%{_modulesloaddir}/open-vm-tools.conf
install -p -m 644 -D %{SOURCE5} %{buildroot}%{_sysconfdir}/pam.d/vmtoolsd

# 'make check' in open-vm-tools rebuilds docs and ends up regenerating the font
# file. We can add %%check secion once 'make check' is fixed upstream.

%post
%?ldconfig
# Setup mount point for Shared Folders
# NOTE: Use systemd-detect-virt to detect VMware platform because
#       vmware-checkvm might misbehave on non-VMware platforms.
if [ -f %{_bindir}/vmware-checkvm -a                     \
     -f %{_bindir}/vmhgfs-fuse ] &&                      \
   %{_bindir}/systemd-detect-virt | grep -iq VMware &&   \
   %{_bindir}/vmware-checkvm &> /dev/null &&             \
   %{_bindir}/vmware-checkvm -p | grep -q Workstation && \
   %{_bindir}/vmhgfs-fuse -e &> /dev/null; then
   mkdir -p /mnt/hgfs
fi

if [ "$1" = "2" ]; then
   # Cleanup GuestProxy certs, relevant for upgrades only
   if [ -f %{_bindir}/vmware-guestproxycerttool ]; then
      %{_bindir}/vmware-guestproxycerttool -e &> /dev/null || /bin/true
   fi
   if [ -d /etc/vmware-tools/GuestProxyData ]; then
      rm -rf /etc/vmware-tools/GuestProxyData &> /dev/null || /bin/true
   fi

   # Cleanup vmtoolsd-init.service in case of upgrades
   %{_bindir}/systemctl disable %{toolsdaemon}-init.service &> /dev/null || /bin/true
fi
%systemd_post %{vgauthdaemon}.service %{toolsdaemon}.service

%post desktop
%systemd_post run-vmblock\\x2dfuse.mount
# Need to enable the service as it is not enabled by default.
# Enabling an already-enabled service is not an error. So, we can perform this
# step everytime during the post-install.
if [ -f %{_bindir}/vmware-checkvm ] &&                   \
   %{_bindir}/systemd-detect-virt | grep -iq VMware &&   \
   %{_bindir}/vmware-checkvm &> /dev/null &&             \
   %{_bindir}/vmware-checkvm -p | grep -q Workstation; then
   %{_bindir}/systemctl enable run-vmblock\\x2dfuse.mount &> /dev/null || /bin/true
fi

%post sdmp
# Load the newly installed or upgraded SDMP plugin
if %{_bindir}/systemctl is-active %{toolsdaemon}.service &> /dev/null; then
   %{_bindir}/systemctl restart %{toolsdaemon}.service &> /dev/null || /bin/true
fi

%preun
%?ldconfig
%systemd_preun %{toolsdaemon}.service %{vgauthdaemon}.service

if [ "$1" = "0" -a                                       \
     -f %{_bindir}/vmware-checkvm ] &&                   \
   %{_bindir}/systemd-detect-virt | grep -iq VMware &&   \
   %{_bindir}/vmware-checkvm &> /dev/null; then

   # Tell VMware that open-vm-tools is being uninstalled
   if [ -f %{_bindir}/vmware-rpctool ]; then
      %{_bindir}/vmware-rpctool 'tools.set.version 0' &> /dev/null || /bin/true
   fi

   # Teardown mount point for Shared Folders
   if [ -d /mnt/hgfs ] &&                               \
      %{_bindir}/vmware-checkvm -p | grep -q Workstation; then
      umount /mnt/hgfs &> /dev/null || /bin/true
      rmdir /mnt/hgfs &> /dev/null || /bin/true
   fi
fi

%preun desktop
%systemd_preun run-vmblock\\x2dfuse.mount

%postun
%?ldconfig
%systemd_postun_with_restart %{toolsdaemon}.service %{vgauthdaemon}.service

%postun desktop
%systemd_postun run-vmblock\\x2dfuse.mount

%postun sdmp
# In case of uninstall, unload the uninstalled SDMP plugin
if [ "$1" = "0" ] &&                                       \
   %{_bindir}/systemctl is-active %{toolsdaemon}.service &> /dev/null; then
   %{_bindir}/systemctl restart %{toolsdaemon}.service &> /dev/null || /bin/true
fi

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%config(noreplace) %{_sysconfdir}/pam.d/*
%dir %{_sysconfdir}/vmware-tools/
%dir %{_sysconfdir}/vmware-tools/vgauth
%dir %{_sysconfdir}/vmware-tools/vgauth/schemas
%config(noreplace) %{_sysconfdir}/vmware-tools/*.conf
# Don't expect users to modify example tools.conf file
%config %{_sysconfdir}/vmware-tools/tools.conf.example
# Don't expect users to modify VGAuth schema files
%config %{_sysconfdir}/vmware-tools/vgauth/schemas/*
%{_sysconfdir}/vmware-tools/*-vm-default
%{_sysconfdir}/vmware-tools/scripts
%{_sysconfdir}/vmware-tools/statechange.subr
%{_bindir}/VGAuthService
%{_bindir}/vm-support
%{_bindir}/vmhgfs-fuse
%{_bindir}/vmtoolsd
%{_bindir}/vmware-alias-import
%{_bindir}/vmware-checkvm
%{_bindir}/vmware-hgfsclient
%{_bindir}/vmware-namespace-cmd
%{_bindir}/vmware-rpctool
%{_bindir}/vmware-toolbox-cmd
%{_bindir}/vmware-vgauth-cmd
%{_bindir}/vmware-xferlogs
%{_libdir}/libDeployPkg.so.*
%{_libdir}/libguestlib.so.*
%{_libdir}/libguestStoreClient.so.*
%{_libdir}/libhgfs.so.*
%{_libdir}/libvgauth.so.*
%{_libdir}/libvmtools.so.*
%dir %{_libdir}/%{name}/
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/plugins/common
%{_libdir}/%{name}/plugins/common/*.so
%dir %{_libdir}/%{name}/plugins/vmsvc
%{_libdir}/%{name}/plugins/vmsvc/libappInfo.so
%{_libdir}/%{name}/plugins/vmsvc/libcomponentMgr.so
%{_libdir}/%{name}/plugins/vmsvc/libdeployPkgPlugin.so
%{_libdir}/%{name}/plugins/vmsvc/libgdp.so
%{_libdir}/%{name}/plugins/vmsvc/libguestInfo.so
%{_libdir}/%{name}/plugins/vmsvc/libguestStore.so
%{_libdir}/%{name}/plugins/vmsvc/libpowerOps.so
%{_libdir}/%{name}/plugins/vmsvc/libresolutionKMS.so
%{_libdir}/%{name}/plugins/vmsvc/libtimeSync.so
%{_libdir}/%{name}/plugins/vmsvc/libvmbackup.so

%{_datadir}/%{name}/
%{_udevrulesdir}/99-vmware-scsi-udev.rules
%{_unitdir}/%{toolsdaemon}.service
%{_unitdir}/%{vgauthdaemon}.service
%{_modulesloaddir}/open-vm-tools.conf

%files desktop
%{_sysconfdir}/xdg/autostart/*.desktop
%{_bindir}/vmware-user
%{_bindir}/vmwgfxctrl
%attr(4755,-,-) %{_bindir}/vmware-user-suid-wrapper
%{_bindir}/vmware-vmblock-fuse
%{_libdir}/%{name}/plugins/vmusr/
%{_unitdir}/run-vmblock\x2dfuse.mount

%files sdmp
%{_libdir}/%{name}/plugins/vmsvc/libserviceDiscovery.so
%{_libdir}/%{name}/serviceDiscovery

%ifarch x86_64
%files salt-minion
%dir %{_libdir}/%{name}/componentMgr/
%dir %{_libdir}/%{name}/componentMgr/saltMinion/
%{_libdir}/%{name}/componentMgr/saltMinion/svtminion.sh
%endif

%files devel
%doc docs/api/build/*
%exclude %{_includedir}/libDeployPkg/
%{_includedir}/vmGuestLib/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libDeployPkg.so
%{_libdir}/libguestlib.so
%{_libdir}/libguestStoreClient.so
%{_libdir}/libhgfs.so
%{_libdir}/libvgauth.so
%{_libdir}/libvmtools.so

%files test
%{_bindir}/vmware-vgauth-smoketest

%changelog
## START: Generated by rpmautospec
* Thu Apr 16 2026 azldev <azurelinux@microsoft.com> - 13.0.10-3
- Latest state for open-vm-tools

* Mon Feb 02 2026 Simone Caronni <negativo17@gmail.com> - 13.0.10-2
- Upload sources

* Mon Feb 02 2026 Simone Caronni <negativo17@gmail.com> - 13.0.10-1
- Update to 13.0.10

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 13.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Nov 04 2025 Tom spot Callaway <spotaws@amazon.com> - 13.0.0-2
- rebuild for new fuse3

* Thu Jul 24 2025 Simone Caronni <negativo17@gmail.com> - 13.0.0-1
- Update to 13.0.0

* Fri May 16 2025 Simone Caronni <negativo17@gmail.com> - 12.5.2-1
- Update to 12.5.2

* Thu Mar 20 2025 Richard W.M. Jones <rjones@redhat.com> - 12.4.0-4
- Bump and rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 12.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 05 2024 John Wolfe <john.wolfe@broadcom.com> - 12.4.0-1
- Package a new upstream version of open-vm-tools-12.4.0-23259341.
  - A number of Coverity reported issues have been addressed.

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 8 2023 John Wolfe <jwolfe@vmware.com> - 12.3.5-1
- Package new upstream version of open-vm-tools-12.3.5-22544099.
  . fix for CVE-2023-34058 - another SAML token signature bypass vulnerability.
  . fix for CVE-2023-34059 - a file descriptor hijack vulnerability in the
                             vmware-user-suid-wrapper.
  . address https://github.com/vmware/open-vm-tools/issues/310
- Remove CVE-2023-34058.patch and CVE-2023-34059.patch as no longer needed.

* Mon Oct 30 2023 John Wolfe <jwolfe@vmware.com> - 12.3.0-3
- Address CVE-2023-34058 - BZ 2246963 - SAML token signature token bypass.
- Address CVE-2023-34059 - BZ 2246962 - vmware-user-suid-wrapper
  file descriptor hijack vulnerability
* Thu Oct 05 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 12.3.0-2
- Use fuse3 on new RHEL

* Sat Sep 9 2023 John Wolfe <jwolfe@vmware.com> - 12.3.0-1
- Package new upstream version of open-vm-tools-12.3.0-22234872.
  - Fix for CVE-2023-20900 - a SAML token signature bypass vulnerability.
  - Fix for CVE-2023-20867 - an Authentication Bypass vulnerability.
  - Linux quiesced snapshots have been updated to avoid intermittent hangs
    of the vmtoolsd process.
    - File systems prefrozen by custom quiescing scripts must be listed on the
      "excludedFileSystems" setting in the "vmbackup" section of the tools.conf
      file.
    - A tools.conf configuration setting is available to temporaily direct
      Linux quiesced snaphots to restore pre open-vm-tools 12.2.0 behavior
      of ignoring file systems already frozen.
  - A number of Coverity reported issues have been addressed.
  - A number of GitHub issues and pull requests have been handled.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 1 2023 John Wolfe <jwolfe@vmware.com> - 12.1.5-2
- Update the copyright date in the open-vm-tools.spec file.

* Sun Jan 1 2023 John Wolfe <jwolfe@vmware.com> - 12.1.5-1
- Package new upstream version of open-vm-tools-12.1.5-20735119.
  - The deployPkg plugin may prematurely reboot the guest VM before cloud-init
    has completed user data setup
  - A SIGSEGV may be encountered when a non-quiescing snapshot times out.
  - A number of Coverity reported issues have been addressed.

* Thu Sep 8 2022 John Wolfe <jwolfe@VMWARE.COM> - 12.1.0-1
- Package new upstream version open-vm-tools-12.1.0-20219665.
  . fix for CVE-2022-31676 - a local privilege escalation vulnerability.
  . address a number of Coverity reported issues.
- Remove patch 1205-Properly-check-authorization-on-incoming-guestOps-re.patch
  as no longer needed.

* Sun Sep 4 2022 John Wolfe <jwolfe@vmware.com> - 12.0.5-3
- Add patch 1205-Properly-check-authorization-on-incoming-guestOps-re.patch
  to fix CVE-2022-31676 in open-vm-tools 12.0.5 tracked in PR 120976.
- Correct build requirements - replace systemd-rpm-macros with systemd_udev.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 12.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 John Wolfe <jwolfe@vmware.com> - 12.0.5-1
- Package new upstream version open-vm-tools-12.0.5-19716617.
 - Maintenance release addressing some potential FTBFS issues.
- Remove asyncsocket.patch as no longer needed.

* Mon May 9 2022 John Wolfe <jwolfe@vmware.com> - 12.0.0-1
- Package new upstream version open-vm-tools-12.0.0-19345655.
- Enable build of the new salt-minion plugin package.
- Deferring enablement of new containerInfo plugin until a later revision.
- Build with fuse3 on Fedora.

* Thu Feb 24 2022 John Wolfe <jwolfe@vmware.com> - 11.3.5-1
- Package new upstream version open-vm-tools-11.3.5-18557794.

* Wed Feb 9 2022 John Wolfe <jwolfe@vmware.com> - 11.3.0-6
- Refactored asyncsocket.c patch to use size_t size and index variables.

* Tue Feb 1 2022 John Wolfe <jwolfe@vmware.com> - 11.3.0-5
- Address (fix) strings or array bounds warnings from GCC 12.0.x.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 11.3.0-3
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 15 2021 Ravindra Kumar <ravindrakumar@vmware.com> - 11.3.0-1
- Package new upstream version open-vm-tools-11.3.0-18090558.
- Add vmware-alias-import, vmwgfxctrl, libgdp.so, libguestStore.so
  and libguestStoreClient.so.*.
- Remove open-vm-tools-fix-kms-autodetection.patch,
  open-vm-tools-gcc11.patch and open-vm-tools-gdk-glib.patch
  as no longer needed.

* Tue Jun 01 2021 Simone Caronni <negativo17@gmail.com> - 11.2.5-9
- Backport patch for KMS autodetection.

* Tue Jun 01 2021 Simone Caronni <negativo17@gmail.com> - 11.2.5-8
- Trim changelog.
- Fix libdrm/udev build requirement.

* Tue Jun 01 2021 Simone Caronni <negativo17@gmail.com> - 11.2.5-7
- Fix build on CentOS/RHEL 7.
- Allow building on aarch64 for CentOS/RHEL 8+ and Fedora.
- Clean up SPEC file (conditionals, build requirements, scriptlets, formatting).

* Mon Apr 05 2021 Ravindra Kumar <ravindrakumar@vmware.com> - 11.2.5-6
- Added missing escape char in run-vmblock\\x2dfuse.mount service name.
- Enabled run-vmblock\\x2dfuse.mount service during post-install.
- Moved run-vmblock\x2dfuse.mount service unit to desktop package.

* Fri Mar 19 2021 Ravindra Kumar <ravindrakumar@vmware.com> - 11.2.5-5
- Added open-vm-tools-gdk-glib.patch to fix RHBZ#1939718.

* Tue Mar 16 2021 Neal Gompa <ngompa13@gmail.com> - 11.2.5-4
- Add missing BRs
- Clean up conditionals to build correctly with EL8+
- Simplify systemd scriptlets

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 11.2.5-3
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Ravindra Kumar <ravindrakumar@vmware.com> - 11.2.5-1
- Package new upstream version open-vm-tools-11.2.5-17337674.
- libdnet dependency was removed in open-vm-tools 11.0.0. So,
  removed the stale BuildRequires for libdnet.

* Thu Jan 14 2021 Richard W.M. Jones <rjones@redhat.com> - 11.2.0-2
- Bump and rebuild against libdnet 1.14 (RHBZ#1915838).

* Fri Nov 06 2020 Ravindra Kumar <ravindrakumar@vmware.com> - 11.2.0-1
- Package new upstream version open-vm-tools-11.2.0-16938113.

* Fri Oct 30 2020 Jeff Law <law@redhat.com> - 11.1.5-2
- Fix incorrect volatile exposed by gcc-11

* Tue Sep 08 2020 Ravindra Kumar <ravindrakumar@vmware.com> - 11.1.5-1
- Package new upstream version open-vm-tools-11.1.5-16724464.
- Removed gcc10-warning.patch and sdmp-fixes.patch (no longer needed).

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 09 2020 Merlin Mathesius <mmathesi@redhat.com> - 11.1.0-3
- Conditional fixes to build for ELN

* Sun Jun 21 2020 Ravindra Kumar <ravindrakumar@vmware.com> - 11.1.0-2
- Added sdmp-fixes.patch from upstream to remove net-tools dependency
  and couple of important fixes

* Mon May 25 2020 Ravindra Kumar <ravindrakumar@vmware.com> - 11.1.0-1
- Package new upstream version open-vm-tools-11.1.0-16036546.
- Added new open-vm-tools-sdmp package.
- Workaround for vm-support script path is no longer needed.
- Added missing dependencies for vm-support script.
- Updated gcc10-warning.patch.
- Removed gcc9-static-inline.patch and diskinfo-log-spew.patch that
  are no longer needed.

* Sun May 17 2020 Ravindra Kumar <ravindrakumar@vmware.com> - 11.0.5-4
- Updated PAM configuration file to follow configured authn scheme.

* Tue Mar 24 2020 Ravindra Kumar <ravindrakumar@vmware.com> - 11.0.5-3
- Use /sbin/ldconfig on older than Fedora 28 and RHEL 8 platforms.

* Fri Feb 07 2020 Ravindra Kumar <ravindrakumar@vmware.com> - 11.0.5-2
- Added patch diskinfo-log-spew.patch.

* Tue Feb 04 2020 Ravindra Kumar <ravindrakumar@vmware.com> - 11.0.5-1
- Package new upstream version open-vm-tools-11.0.5-15389592.
- Removed vix-memleak.patch which is no longer needed.

* Tue Feb 04 2020 Ravindra Kumar <ravindrakumar@vmware.com> - 11.0.0-6
- Added gcc10-warning.patch for fixing compilation issues.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

## END: Generated by rpmautospec
