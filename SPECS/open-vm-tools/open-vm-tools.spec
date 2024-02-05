################################################################################
### Copyright 2013-2020 VMware, Inc.  All rights reserved.
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

%global _hardened_build 1
%global toolsbuild      22544099
%global toolsdaemon     vmtoolsd
%global vgauthdaemon    vgauthd
Summary:        Open Virtual Machine Tools for virtual machines hosted on VMware
Name:           open-vm-tools
Version:        12.3.5
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/vmware/%{name}
Source0:        https://github.com/vmware/%{name}/releases/download/stable-%{version}/%{name}-%{version}-%{toolsbuild}.tar.gz
Source1:        %{toolsdaemon}.service
Source2:        %{vgauthdaemon}.service
Source3:        vmblock.mount
Source4:        open-vm-tools.conf
Source5:        vmtoolsd.pam
BuildRequires:  autoconf
BuildRequires:  automake
#BuildRequires:    doxygen
# Fuse is optional and enables vmblock-fuse
BuildRequires:  fuse-devel
# This used to be gcc-c++ because it probably needs gcc-libstdc++-devel
BuildRequires:  gcc
BuildRequires:  glib-devel >= 2.14.0
BuildRequires:  libdnet-devel
#BuildRequires:    libicu-devel
BuildRequires:  libmspack-devel
BuildRequires:  libtirpc-devel
BuildRequires:  libtool
# Unfortunately, xmlsec1-openssl does not add libtool-ltdl
# dependency, so we need to add it ourselves.
#BuildRequires:    libtool-ltdl-devel
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
#BuildRequires:    procps-devel
#BuildRequires:    rpcgen
# For Mariner, it's called
BuildRequires:  rpcsvc-proto
BuildRequires:  systemd
BuildRequires:  xmlsec1-devel
Requires:       coreutils
Requires:       fuse
Requires:       grep
#Requires:         libdrm
Requires:       iproute
Requires:       pciutils
Requires:       sed
Requires:       systemd
Requires:       tar
Requires:       util-linux
Requires:       which
# xmlsec1-openssl needs to be added explicitly
Requires:       xmlsec1
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
# open-vm-tools >= 10.0.0 do not require open-vm-tools-deploypkg
# provided by VMware. That functionality is now available as part
# of open-vm-tools package itself.
Obsoletes:      open-vm-tools-deploypkg <= 10.0.5
ExclusiveArch:  x86_64

%description
The %{name} project is an open source implementation of VMware Tools. It
is a suite of open source virtualization utilities and drivers to improve the
functionality, user experience and administration of VMware virtual machines.
This package contains only the core user-space programs and libraries of
%{name}.

%package          sdmp
Summary:        Service Discovery components for Open Virtual Machine Tools
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       coreutils
Requires:       gawk
Requires:       glibc
Requires:       grep
Requires:       iproute
#Requires:         procps

%description      sdmp
This package contains only the user-space programs and utility scripts of
%{name} that are essential for performing service discovery in VMware virtual
machines by vRealize Operations Service Discovery Management Pack.

%package          devel
Summary:        Development libraries for Open Virtual Machine Tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description      devel
This package contains only the user-space programs and libraries of
%{name} that are essential for developing customized applications for
VMware virtual machines.

%package          test
Summary:        Test utilities for Open Virtual Machine Tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description      test
This package contains only the test utilities for %{name} that are
useful for verifying the functioning of %{name} in VMware virtual
machines.

%prep
%autosetup -n %{name}-%{version}-%{toolsbuild}

%build
# Required for regenerating configure script when
# configure.ac get modified
autoreconf -vif

%global usetirpc with-tirpc

%configure \
    --without-kernel-modules \
    --without-x \
    --enable-xmlsec1 \
    --enable-resolutionkms \
    --enable-servicediscovery \
    --%{usetirpc} \
    --disable-static \
    --with-udev-rules-dir=%{_udevrulesdir}

sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build

%install
export DONT_STRIP=1
%make_install

# Remove exec bit from config files
chmod a-x %{buildroot}%{_sysconfdir}/pam.d/*
chmod a-x %{buildroot}%{_sysconfdir}/vmware-tools/*.conf
chmod a-x %{buildroot}%{_sysconfdir}/vmware-tools/vgauth/schemas/*

# Remove exec bit on udev rules.
chmod a-x %{buildroot}%{_udevrulesdir}/99-vmware-scsi-udev.rules

# Remove the DOS line endings
sed -i "s|\r||g" README

# Remove unnecessary files from packaging
find %{buildroot} -type f -name "*.la" -delete -print
rm -fr %{buildroot}%{_defaultdocdir}
rm -f docs/api/build/html/FreeSans.ttf

# Remove mount.vmhgfs & symlink
rm -fr %{buildroot}%{_sbindir} %{buildroot}/sbin/mount.vmhgfs

# Systemd unit files
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_unitdir}/%{toolsdaemon}.service
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_unitdir}/%{vgauthdaemon}.service
install -p -m 644 -D '%{SOURCE3}' %{buildroot}%{_unitdir}/run-vmblock\\x2dfuse.mount
install -p -m 644 -D %{SOURCE4} %{buildroot}%{_modulesloaddir}/open-vm-tools.conf
install -p -m 644 -D %{SOURCE5} %{buildroot}%{_sysconfdir}/pam.d/vmtoolsd

# 'make check' in open-vm-tools rebuilds docs and ends up regenerating
# the font file. We can add %%check secion once 'make check' is fixed
# upstream


%{?ldconfig}

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
   if [ -d %{_sysconfdir}/vmware-tools/GuestProxyData ]; then
      rm -rf %{_sysconfdir}/vmware-tools/GuestProxyData &> /dev/null || /bin/true
   fi

   # Cleanup vmtoolsd-init.service in case of upgrades
   %{_bindir}/systemctl disable %{toolsdaemon}-init.service &> /dev/null || /bin/true
fi
%systemd_post %{vgauthdaemon}.service
%systemd_post %{toolsdaemon}.service


%systemd_post run-vmblock\x2dfuse.mount

%post sdmp
# Load the newly installed or upgraded SDMP plugin
if %{_bindir}/systemctl is-active %{toolsdaemon}.service &> /dev/null; then
   %{_bindir}/systemctl restart %{toolsdaemon}.service &> /dev/null || /bin/true
fi

%preun
%systemd_preun %{toolsdaemon}.service
%systemd_preun %{vgauthdaemon}.service

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

%systemd_preun run-vmblock\x2dfuse.mount

%postun
%{?ldconfig}

%systemd_postun_with_restart %{toolsdaemon}.service
%systemd_postun_with_restart %{vgauthdaemon}.service

%systemd_postun run-vmblock\x2dfuse.mount

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
%{_libdir}/%{name}/plugins/vmsvc/libdeployPkgPlugin.so
%{_libdir}/%{name}/plugins/vmsvc/libguestInfo.so
%{_libdir}/%{name}/plugins/vmsvc/libpowerOps.so
%{_libdir}/%{name}/plugins/vmsvc/libresolutionKMS.so
%{_libdir}/%{name}/plugins/vmsvc/libtimeSync.so
%{_libdir}/%{name}/plugins/vmsvc/libvmbackup.so
%{_libdir}/%{name}/plugins/vmsvc/libgdp.so
%{_libdir}/%{name}/plugins/vmsvc/libguestStore.so
%{_libdir}/%{name}/plugins/vmsvc/libcomponentMgr.so
#Usually in desktop package
%{_bindir}/vmware-vmblock-fuse

%{_datadir}/%{name}/
%{_udevrulesdir}/99-vmware-scsi-udev.rules
%{_unitdir}/%{toolsdaemon}.service
%{_unitdir}/%{vgauthdaemon}.service
%{_unitdir}/run-vmblock\x2dfuse.mount
%{_modulesloaddir}/open-vm-tools.conf

%files sdmp
%{_libdir}/%{name}/plugins/vmsvc/libserviceDiscovery.so
%{_libdir}/%{name}/serviceDiscovery

%files devel
%exclude %{_includedir}/libDeployPkg/
%{_includedir}/vmGuestLib/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libDeployPkg.so
%{_libdir}/libguestlib.so
%{_libdir}/libhgfs.so
%{_libdir}/libvgauth.so
%{_libdir}/libvmtools.so
%{_libdir}/libguestStoreClient.so

%files test
%{_bindir}/vmware-vgauth-smoketest

%changelog
* Wed Jan 31 2024 Bala <balakumaran.kannan@microsoft.com> - 12.3.5-1
- Upgrade to version 12.3.5

* Wed Mar 16 2022 Matthew Torr <matthewtorr@microsoft.com> - 11.3.0-2
- Reinstate ConditionVirtualization service option so that the services only run on VMware.

* Thu Jan 27 2022 Henry Li <lihl@microsoft.com> - 11.3.0-1
- Upgrade to version 11.3.0
- Remove patches that no longer apply
- Add vmware-alias-import,libgdp.so, libguestStore.so, libguestStoreClient.so
  and libguestStoreClient.so.*
- License Verified

* Wed Nov 04 2020 Ruying Chen <v-ruyche@microsoft.com> - 11.1.0-5
- Systemd supports merged /usr. Configure to build with corresponding directory.

* Fri Aug 07 2020 Mateusz Malisz <mamalisz@microsoft.com> 11.1.0-4
- Rename input file for run-vmblock\x2dfuse.mount to avoid problems with backslash in the name.

* Wed Aug 05 2020 Mateusz Malisz <mamalisz@microsoft.com> 11.1.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT)

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

* Wed Oct 09 2019 Ravindra Kumar <ravindrakumar@vmware.com> - 11.0.0-4
- Fixes for drag-n-drop that needs vmblock-fuse mount.
- Added run-vmblock\x2dfuse.mount service unit for vmblock-fuse mount.
- Added open-vm-tools.conf for loading Fuse.

* Wed Oct 09 2019 Ravindra Kumar <ravindrakumar@vmware.com> - 11.0.0-3
- Cleanup GuestProxy certs from /etc/vmware-tools/GuestProxyData if needed.
- Cleanup vmtoolsd-init service symlinks.

* Wed Oct 02 2019 Ravindra Kumar <ravindrakumar@vmware.com> - 11.0.0-2
- vmtoolsd-init.service is no longer needed for 11.0.0, removed it.

* Wed Oct 02 2019 Ravindra Kumar <ravindrakumar@vmware.com> - 11.0.0-1
- Package new upstream version open-vm-tools-11.0.0-14549434.
- Added gcc9-static-inline.patch for gcc9 warnings.
- Added vix-memleak.patch for a memory leak.
- Removed gcc9-warnings.patch which is no longer needed.
- Removed vmware-guestproxycerttool as it is no longer available upstream.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Mar 16 2019 Ravindra Kumar <ravindrakumar@vmware.com> - 10.3.10-1
- Package new upstream version open-vm-tools-10.3.10-12406962.
- Removed quiescing-combined.patch which is no longer needed.

* Wed Feb 13 2019 Ravindra Kumar <ravindrakumar@vmware.com> - 10.3.5-2
- Combine all gcc9 warning patches into one single gcc9-warnings.patch.

* Tue Feb 12 2019 Ravindra Kumar <ravindrakumar@vmware.com> - 10.3.5-1
- Package new upstream version open-vm-tools-10.3.5-10430147.
- Removed cloud-init.patch which is no longer needed.
- Removed hgfsPlugin-crash.patch which is no longer needed.
- Removed linuxDeploymentUtils-strncat.patch which is no longer needed.
- Added quiescing-combined.patch for quiesced snapshot fixes.
- Updated hgfsServer-aligned.patch for open-vm-tools-10.3.5.

* Tue Feb 12 2019 Ravindra Kumar <ravindrakumar@vmware.com> - 10.3.0-8
- Updated *-aligned.patch files with more tweaks.
- Filed a regression in readdir operation in dir-aligned.patch.

* Sun Feb 03 2019 Ravindra Kumar <ravindrakumar@vmware.com> - 10.3.0-7
- Added hgfsServer-aligned.patch for "address-of-packed-member" error.
- Added hgfsmounter-aligned.patch for "address-of-packed-member" error.
- Added util-misc-format.patch for "format-overflow" error.
- Added linuxDeploymentUtils-strncat.patch for "stringop-truncation" error.
- Added filesystem-aligned.patch for "address-of-packed-member" error.
- Added file-aligned.patch for "address-of-packed-member" error.
- Added fsutil-aligned.patch for "address-of-packed-member" error.
- Added dir-aligned.patch for "address-of-packed-member" error.
- Added link-aligned.patch for "address-of-packed-member" error.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 01 2018 Simone Caronni <negativo17@gmail.com> - 10.3.0-5
- Update SPEC file to match packaging guidelines.
- Re-add ldconfig scriptlets. They expand to nothing in Fedora 28+, but they
  are still required for Fedora 27. These can be removed when Fedora 27 is EOL.

* Fri Aug 10 2018 Ravindra Kumar <ravindrakumar@vmware.com> - 10.3.0-4
- Fixed few bugs related to vmtoolsd-init.service.

* Tue Aug 07 2018 Ravindra Kumar <ravindrakumar@vmware.com> - 10.3.0-3
- Implement the https://pagure.io/packaging-committee/issue/506 guideline.
- Added vmtoolsd-init.service per the guideline.
- Replaced the certificate cleanup with "vmware-guestproxycerttool -e".

* Mon Aug 06 2018 Ravindra Kumar <ravindrakumar@vmware.com> - 10.3.0-2
- Added hgfsPlugin-crash.patch for vmtoolsd crash (RHBZ#1612470).

* Thu Aug 02 2018 Ravindra Kumar <ravindrakumar@vmware.com> - 10.3.0-1
- Package new upstream version open-vm-tools-10.3.0-8931395.
- Updated cloud-init.patch for 10.3.0.
- Removed use-tirpc.patch which is no longer needed.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Ravindra Kumar <ravindrakumar@vmware.com> - 10.2.5-6
- Added cloud-init.patch to detect cloud-init correctly.
- Added cleanup for /etc/vmware-tools directory on uninstall.

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 10.2.5-5
- Rebuild for ICU 62

* Thu Jul 05 2018 Richard W.M. Jones <rjones@redhat.com> - 10.2.5-4
- Remove ldconfig
  https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/SU3LJVDZ7LUSJGZR5MS72BMRAFP3PQQL/

* Tue May 15 2018 Pete Walter <pwalter@fedoraproject.org> - 10.2.5-3
- Rebuild for ICU 61.1

* Wed May 09 2018 Ravindra Kumar <ravindrakumar@vmware.com> - 10.2.5-2
- Use tirpc for Fedora 28 onwards.

* Wed May 09 2018 Ravindra Kumar <ravindrakumar@vmware.com> - 10.2.5-1
- Package new upstream version open-vm-tools-10.2.5-8068406 (RHBZ#1431376).
- Added use-tirpc.patch to use libtirpc instead of deprecated Sun RPC.
- Removed wayland-crash.patch which is no longer needed.

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 10.2.0-5
- Rebuild for ICU 61.1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 29 2017 Ravindra Kumar <ravindrakumar@vmware.com> - 10.2.0-3
- Patch for a Wayland related crash in the desktopEvents plugin (RHBZ#1526952).
- gdk_set_allowed_backends() is available in version 3.10 and later only.

* Mon Dec 18 2017 Ravindra Kumar <ravindrakumar@vmware.com> - 10.2.0-2
- Build with gtk3 only on newer distros.

* Fri Dec 15 2017 Ravindra Kumar <ravindrakumar@vmware.com> - 10.2.0-1
- Package new upstream version open-vm-tools-10.2.0-7253323.
- Remove the patches that are no longer needed.
- New version builds with gtk3 by default.
- Package vmware-user symlink in desktop.
- Add a new test package for test utilities.
- Pick a fix to a conditional from Miroslav Vadkerti <mvadkert@redhat.com>.

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 10.1.10-4
- Rebuild for ICU 60.1

* Thu Sep 28 2017 Ravindra Kumar <ravindrakumar@vmware.com> - 10.1.10-3
- Replaced 'net-tools' dependency with 'iproute' (RHBZ#1496134).
- Added resolutionKMS-wayland-2.patch with some new fixes.

* Fri Aug 11 2017 Kalev Lember <klember@redhat.com> - 10.1.10-2
- Bump and rebuild for an rpm signing issue

* Thu Aug 10 2017 Ravindra Kumar <ravindrakumar@vmware.com> - 10.1.10-1
- Package new upstream version open-vm-tools-10.1.10-6082533.
- Remove the patches that are no longer needed.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Richard W.M. Jones <rjones@redhat.com> - 10.1.5-5
- Fix /tmp race conditions in libDeployPkg (CVE-2015-5191).

* Sun Apr 02 2017 Ravindra Kumar <ravindrakumar@vmware.com> - 10.1.5-4
- ResolutionKMS patch for Wayland (RHBZ#1292234).

* Thu Mar 16 2017 Ravindra Kumar <ravindrakumar@vmware.com> - 10.1.5-3
- Need to add xmlsec1-openssl dependency explicitly.

* Tue Feb 28 2017 Richard W.M. Jones <rjones@redhat.com> - 10.1.5-2
- Use 0644 permissions for udev rules file.

* Fri Feb 24 2017 Ravindra Kumar <ravindrakumar@vmware.com> - 10.1.5-1
- Package new upstream version open-vm-tools-10.1.5-5055683 (RHBZ#1408959).

* Fri Feb 17 2017 Ravindra Kumar <ravindrakumar@vmware.com> - 10.1.0-1
- Package new upstream version open-vm-tools-10.1.0-4449150 (RHBZ#1408959).
- Remove patches that are no longer needed.
- Build with --enable-xmlsec1 to avoid dependency on xerces-c and xml-security-c.
- Replace _prefix/lib/udev/rules.d/ with _udevrulesdir macro.

* Thu Feb 16 2017 Ravindra Kumar <ravindrakumar@vmware.com> - 10.0.5-10
- sysmacros patch for glibc-2.25 (RHBZ#1411807).
- vgauth patch for openssl-1.1.0.

* Thu Feb 16 2017 Ravindra Kumar <ravindrakumar@vmware.com> - 10.0.5-9
- udev rules patch for longer SCSI timeouts (RHBZ#1214347).

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 26 2016 Richard W.M. Jones <rjones@redhat.com> - 10.0.5-5
- vm-support script needs lspci from pciutils (RHBZ#1388766).

* Wed Sep 14 2016 Ravindra Kumar <ravindrakumar@vmware.com> - 10.0.5-4
- Patch for HGFS stale caching issues (RHBZ#1342181).

* Mon Jun 20 2016 Ravindra Kumar <ravindrakumar@vmware.com> - 10.0.5-3
- Use systemd-detect-virt to detect VMware platform (RHBZ#1251656).

* Wed May 25 2016 Ravindra Kumar <ravindrakumar@vmware.com> - 10.0.5-2
- Obsolete open-vm-tools-deploypkg because its not needed for v10.x.

* Wed May 25 2016 Ravindra Kumar <ravindrakumar@vmware.com> - 10.0.5-1
- Package new upstream version open-vm-tools-10.0.5-3227872.
- Add a patch for fixing GCC 6 build issue (RHBZ#1305108).
- Replace kill-werror.patch with no-unused-const.patch.

* Wed May 25 2016 Richard W.M. Jones <rjones@redhat.com> - 10.0.0-12
- Bump and rebuild.

* Sat Apr 23 2016 Richard W.M. Jones <rjones@redhat.com> - 10.0.0-11
- Kill -Werror with fire (RHBZ#1305108).

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 10.0.0-10
- rebuild for ICU 57.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 10.0.0-8
- rebuild for ICU 56.1

* Thu Oct 01 2015 Ravindra Kumar <ravindrakumar@vmware.com> - 10.0.0-7
- Added a missing output redirection

* Thu Oct 01 2015 Ravindra Kumar <ravindrakumar@vmware.com> - 10.0.0-6
- Setup Shared Folders mount point when 'vmhgf-fuse -e' is success

* Thu Oct 01 2015 Ravindra Kumar <ravindrakumar@vmware.com> - 10.0.0-5
- Setup and teardown Shared Folders mount point on VMs running
  on VMware Workstation or VMware Fusion.

* Wed Sep 30 2015 Ravindra Kumar <ravindrakumar@vmware.com> - 10.0.0-4
- vmhgfs-fuse needs 'fusermount' from 'fuse'

* Wed Sep 30 2015 Ravindra Kumar <ravindrakumar@vmware.com> - 10.0.0-3
- Replace -std=c++11 with -std=gnu++11 to get "linux" definitions work
  in order to fix the build issue,
  https://kojipkgs.fedoraproject.org//work/tasks/4823/11274823/build.log
- Removed unused definitions for CFLAGS and CXXFLAGS

* Wed Sep 30 2015 Ravindra Kumar <ravindrakumar@vmware.com> - 10.0.0-2
- Add -std=c++11 to CXXFLAGS for fixing the build issue,
  https://kojipkgs.fedoraproject.org//work/tasks/3685/11273685/build.log

* Tue Sep 29 2015 Ravindra Kumar <ravindrakumar@vmware.com> - 10.0.0-1
- Package new upstream version open-vm-tools-10.0.0-3000743

* Wed Aug 26 2015 Simone Caronni <negativo17@gmail.com> - 9.10.2-2
- Add license macro.
- Remove initscripts requirement (#1226369).
- Delete mount.vmhgfs instead of excluding from packaging, so the debug
  information is not included in the package (#1190540).
- Be more explicit with configuration files, newer mock complains of files being
  listed twice.

* Tue Jul 07 2015 Ravindra Kumar <ravindrakumar@vmware.com> - 9.10.2-1
- Package new upstream version open-vm-tools-9.10.2-2822639
- Removed the patches that are no longer needed

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 Ravindra Kumar <ravindrakumar@vmware.com> - 9.10.0-4
- Claim ownership for /etc/vmware-tools directory

* Fri May 15 2015 Ravindra Kumar <ravindrakumar@vmware.com> - 9.10.0-3
- Put Fedora 23 specific fix under a conditional, so that the change
  can be backported to other branches easily if required.

* Fri May 08 2015 Ravindra Kumar <ravindrakumar@vmware.com> - 9.10.0-2
- F23 has split gdk-pixbuf2-devel >= 2.31.3-5 into 3 packages, gdk-pixbuf2-devel,
  gdk-pixbuf2-modules-devel, and gdk-pixbuf2-xlib-devel. gtk2-devel does not depend
  on gdk-pixbuf2-xlib-devel. Therefore, we need to pull in gdk-pixbuf2-xlib-devel
  dependency ourselves.

* Thu Apr 30 2015 Ravindra Kumar <ravindrakumar@vmware.com> - 9.10.0-1
- Package new upstream version open-vm-tools-9.10.0-2476743
- New version requires adding a new service vgauthd
- Removed old patches that are no longer needed
- Fix (asm_x86.patch) for correct GCC version check
- Fix (strerror_r.patch) for picking GNU signature of strerror_r
- Fix (toolboxcmd.patch) for compiling toolboxcmd-shrink.c with gcc 5.0.1

* Wed Feb 04 2015 Ravindra Kumar <ravindrakumar@vmware.com> - 9.4.6-6
- Added a patch for missing NetIpRouteConfigInfo (BZ#1189295)

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 9.4.6-5
- rebuild for ICU 54.1

* Wed Sep 24 2014 Simone Caronni <negativo17@gmail.com> - 9.4.6-4
- Rebuild for new procps-ng version.

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 9.4.6-3
- rebuild for ICU 53.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 16 2014 Ravindra Kumar <ravindrakumar@vmware.com> - 9.4.6-1
- Package new upstream version open-vm-tools-9.4.6-1770165
- Added "autoreconf -i" and its build dependencies (autoconf, automake and libtool)
  to generate configure script, this is required for version 9.4.6 as it does not
  have configure script bundled in the tar
- Fix (sizeof_argument.patch) for bad sizeof argument error

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Ravindra Kumar <ravindrakumar@vmware.com> - 9.4.0-9
- Removed unnecessary package dependency on 'dbus'
- Moved 'vm-support' script to /usr/bin
- Added a call to 'tools.set.version' RPC to inform VMware
  platform when open-vm-tools has been uninstalled

* Wed Mar 26 2014 Ravindra Kumar <ravindrakumar@vmware.com> - 9.4.0-8
- Add missing package dependency on 'which' (BZ#1045709)

* Tue Mar 25 2014 Ravindra Kumar <ravindrakumar@vmware.com> - 9.4.0-7
- Add -D_DEFAULT_SOURCE to suppress warning as suggested in
  https://sourceware.org/bugzilla/show_bug.cgi?id=16632

* Fri Mar 21 2014 Ravindra Kumar <ravindrakumar@vmware.com> - 9.4.0-6
- Add missing package dependencies (BZ#1045709, BZ#1077320)

* Tue Feb 18 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 9.4.0-5
- Fix FTBFS g_info redefine (RHBZ #1063847)

* Fri Feb 14 2014 David Tardon <dtardon@redhat.com> - 9.4.0-4
- rebuild for new ICU

* Tue Feb 11 2014 Richard W.M. Jones <rjones@redhat.com> - 9.4.0-3
- Only build on x86-64 for RHEL 7 (RHBZ#1054608).

* Wed Dec 04 2013 Richard W.M. Jones <rjones@redhat.com> - 9.4.0-2
- Rebuild for procps SONAME bump.

* Wed Nov 06 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.4.0-1
- Package new upstream version open-vm-tools-9.4.0-1280544.
- Added CUSTOM_PROCPS_NAME=procps and -Wno-deprecated-declarations
  for version 9.4.0.

* Thu Aug 22 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.3-11
- Added copyright and license text.
- Corrected summary for all packages.

* Thu Aug 08 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.3-10
- Added options for hardening build (bug 990549).
- Excluded unwanted file mount.vmhgfs from packaging (bug 990547).
- Removed deprecated key "Encoding" from "Desktop Entry" (bug 990552).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun  4 2013 Richard W.M. Jones <rjones@redhat.com> - 9.2.3-8
- RHEL 7 now includes libdnet, so re-enable it.

* Fri May 24 2013 Richard W.M. Jones <rjones@redhat.com> - 9.2.3-6
- +BR gcc-c++.  If this is missing it fails to build.
- On RHEL, disable libdnet.

* Mon May 06 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.3-5
- Renamed source file open-vm-tools.service -> vmtoolsd.service
  to match it with the service name.

* Wed May 01 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.3-4
- Bumped the release to pick the new service definition with
  no restart directive.

* Mon Apr 29 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.3-3
- open-vm-tools-9.2.3 require glib-2.14.0.

* Mon Apr 29 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.3-2
- Bumped the release to pick the new service definition.

* Thu Apr 25 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.3-1
- Package new upstream version open-vm-tools-9.2.3-1031360.
- Removed configure options CUSTOM_PROCPS_NAME (for libproc) and
  -Wno-deprecated-declarations as these have been addressed in
  open-vm-tools-9.2.3-1031360.

* Wed Apr 24 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.2-12
- Removed %%defattr and BuildRoot.
- Added ExclusiveArch.
- Replaced /usr/sbin/ldconfig with /sbin/ldconfig.

* Mon Apr 22 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.2-11
- Removed the conditional steps for old versions of Fedora and RHEL.

* Thu Apr 18 2013 Ravindra Kumar <ravindrakumar at vmware.com> - 9.2.2-10
- Addressed formal review comments from Simone Caronni.
- Removed %%check section because 'make check' brings font file back.

* Wed Apr 17 2013 Simone Caronni <negativo17@gmail.com> - 9.2.2-9
- Removed rm command in %%check section.
- Remove blank character at the beginning of each changelog line.

* Mon Apr 15 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.2-8
- Removed FreeSans.ttf font file from packaging.
- Added 'rm' command to remove font file in %%check section because
  'make check' adds it back.
- Added doxygen dependency back.

* Thu Apr 11 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.2-7
- Applied patch from Simone for removal of --docdir option from configure.
- Removed unnecessary --enable-docs option from configure.
- Removed doxygen dependency.

* Thu Apr 11 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.2-6
- Replaced vmtoolsd with a variable.
- Changed summary for subpackages to be more specific.
- Removed drivers.txt file as we don't really need it.
- Fixed vmGuestLib ownership for devel package.
- Removed systemd-sysv from Requires for Fedora 18+ and RHEL 7+.
- Made all "if" conditions consistent.

* Wed Apr 10 2013 Simone Caronni <negativo17@gmail.com> - 9.2.2-5
- Added RHEL 5/6 init script.
- Renamed SysV init script / systemd service file to vmtoolsd.
- Fixed ownership of files from review.
- Moved api documentation in devel subpackage.
- Removed static libraries.

* Tue Apr 09 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.2-4
- Applied part of review fixes patch from Simone Caronni for systemd setup.
- Replaced tabs with spaces all over.

* Tue Apr 09 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.2-3
- Applied review fixes patch from Simone Caronni.
- Added missing *.a and *.so files for devel package.
- Removed unnecessary *.la plugin files from base package.

* Mon Apr 08 2013 Ravindra Kumar <ravindrakumar@vmware.com> - 9.2.2-2
- Modified SPEC to follow the conventions and guidelines.
- Addressed review comments from Mohamed El Morabity.
- Added systemd script.
- Verified and built the RPMS for Fedora 18.
- Fixed rpmlint warnings.
- Split the UX components in a separate package for desktops.
- Split the help files in a separate package for help.
- Split the guestlib headers in a separate devel package.

* Mon Jan 28 2013 Sankar Tanguturi <stanguturi@vmware.com> - 9.2.2-1
- Initial SPEC file to build open-vm-tools for Fedora 17.
