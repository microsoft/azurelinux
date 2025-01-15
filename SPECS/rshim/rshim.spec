# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C) 2019 Mellanox Technologies. All Rights Reserved.
#

Name:		 rshim
Version:	 2.1.5
Release:	 1%{?dist}
Summary:	 User-space driver for Mellanox BlueField SoC
License:	 GPLv2
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
URL:		 https://github.com/mellanox/rshim-user-space
Source0:         https://linux.mellanox.com/public/repo/mlnx_ofed/24.10-0.7.0.0/SRPMS/rshim-2.1.5.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:   x86_64
BuildRequires:	 gcc, autoconf, automake, pkgconfig, make
BuildRequires:	 pkgconfig(libpci), pkgconfig(libusb-1.0) fuse3-devel fuse3-libs

%global with_systemd %(if (test -d "%{_unitdir}" > /dev/null); then echo -n '1'; else echo -n '0'; fi)
%global debug_package %{nil}

%description
This is the user-space driver to access the BlueField SoC via the rshim
interface. It provides ways to push boot stream, debug the target or login
via the virtual console or network interface.

%prep
rm -fr %{name}-%{version}
mkdir %{name}-%{version}
tar -axf %{SOURCE0} -C %{name}-%{version} --strip-components 1
%setup -q -D -T

%build
./bootstrap.sh
%configure
%if %{?make_build:1}%{!?make_build:0}
%make_build
%else
make
%endif

%install
%undefine _missing_build_ids_terminate_build
%makeinstall -C src INSTALL_DIR="%{buildroot}%{_sbindir}"
%if "%{with_systemd}" == "1"
  %{__install} -d %{buildroot}%{_unitdir}
  %{__install} -m 0644 rshim.service %{buildroot}%{_unitdir}
%endif
%{__install} -d %{buildroot}%{_mandir}/man8
%{__install} -m 0644 man/rshim.8 %{buildroot}%{_mandir}/man8
%{__install} -m 0644 man/bfb-install.8 %{buildroot}%{_mandir}/man8
%{__install} -m 0644 man/bf-reg.8 %{buildroot}%{_mandir}/man8
%{__install} -d %{buildroot}%{_sysconfdir}
%{__install} -m 0644 etc/rshim.conf %{buildroot}%{_sysconfdir}
%{__install} -m 0755 scripts/bfb-install %{buildroot}%{_sbindir}
%{__install} -m 0755 scripts/bf-reg %{buildroot}%{_sbindir}

%pre
%if "%{with_systemd}" == "1"
  if systemctl is-active --quiet rshim ; then
      systemctl stop rshim
  fi
%endif

%post
%if "%{with_systemd}" == "1"
  echo "Installation complete. To enable and start the rshim service, run:"
  echo "  systemctl daemon-reload"
  echo "  systemctl enable rshim"
  echo "  systemctl start rshim"
%endif

%preun
if [ "$1" = "0" ]; then
%if "%{with_systemd}" == "1"
  if systemctl is-active --quiet rshim ; then
      systemctl stop rshim
  fi
%else
  killall -9 rshim
%endif
fi

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%defattr(-,root,root,-)
%doc README.md
%config(noreplace) %{_sysconfdir}/rshim.conf
%if "%{with_systemd}" == "1"
  %{_unitdir}/rshim.service
%endif
%{_sbindir}/rshim
%{_sbindir}/bfb-install
%{_sbindir}/bf-reg
%{_mandir}/man8/rshim.8.gz
%{_mandir}/man8/bfb-install.8.gz
%{_mandir}/man8/bf-reg.8.gz

%changelog
* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com>
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified

* Mon Oct 14 2024 Penghe Geng <pgeng@nvidia.com> - 2.1.5
- Revert "Abort rshim rpm installation if no cuse.ko found"

* Thu Oct 10 2024 Penghe Geng <pgeng@nvidia.com> - 2.1.4
- Make rshim run in single instance
- Abort rshim rpm installation if no cuse.ko found
- Increase default boot timeout to 300s
- bfb-install: Fix premature bfb-install exit when rebooting BMC

* Tue Sep 10 2024 Penghe Geng <pgeng@nvidia.com> - 2.1.3
- Reduce the access_check() wait time

* Fri Aug 30 2024 Liming Sun <limings@nvidia.com> - 2.1.2
- Improve access_check() to reduce likelihood of race condition
- Revert the 2-second delay

* Thu Aug 15 2024 Liming Sun <limings@nvidia.com> - 2.1.1
- Add support for command mode
- Fix some coding style issues
- Cleanup rshim debug/syslog messages

* Thu Aug 08 2024 Liming Sun <limings@nvidia.com> - 2.0.41
- Add a small delay to access the boot file
- Fix a valgrind warning

* Mon Aug 05 2024 Penghe Geng <pgeng@nvidia.com> - 2.0.40
- Fix rshim deb package for DOCA build on Ubuntu

* Fri Aug 02 2024 Penghe Geng <pgeng@nvidia.com> - 2.0.39
- Fix rshim masking issue on Ubuntu
- bfb-install: Fix NIC_MODE installation for BlueField-2
- pcie: Add VFIO support for BlueField-3

* Fri Jul 26 2024 Penghe Geng <pgeng@nvidia.com> - 2.0.38
- Make sending the initial force command a one-time event
- bfb-install: adjust the log file to be per rshim

* Tue Jul 16 2024 Penghe Geng <pgeng@nvidia.com> - 2.0.37
- add missing --force in help menu

* Mon Jul 15 2024 Penghe Geng <pgeng@nvidia.com> - 2.0.36
- Allow /dev/rshim<N> devfs creation only with --force option enabled
- bfb-install: fix for NIC mode
- bfb-install: Exit with error if running remote bfb-install without
  password-less root SSH
- Fix compiling issue for FreeBSD

* Fri Jul 05 2024 Penghe Geng <pgeng@nvidia.com> - 2.0.35
- Add ownership transfer feature (primarily via "FORCE_CMD")
- bfb-install: enhancement for NIC mode

* Tue Jun 11 2024 Liming Sun <limings@nvidia.com> - 2.0.34
- bfb-install: Enable CLEAR_ON_READ
- bfb-install: add cleanup code for runtime update

* Thu Jun 06 2024 Liming Sun <limings@nvidia.com> - 2.0.33
- misc: add 'CLEAR_ON_READ' command
- bfb-install: add runtime image support

* Tue Jun 04 2024 Liming Sun <limings@nvidia.com> - 2.0.32
- bf3/pcie_lf: Fix the 4B access via MSN GW

* Fri May 17 2024 Liming Sun <limings@nvidia.com> - 2.0.31
- bf3/pcie_lf: support register read/write via /dev/rshim0/rshim
- Only poll/check locked mode for PCIe backend
- Remove workaround support for BF2 A0 chip

* Mon May 13 2024 Liming Sun <limings@nvidia.com> - 2.0.30
- pcie: Adjust default reset delay to 3 seconds
- Avoid polling blocked status during reset
- Disable installation of rshim on host by default

* Tue Apr 30 2024 Liming Sun <limings@nvidia.com> - 2.0.29
- Some robust fixes for rshim over USB
- Lower log level for register read errors as it's normal during reset

* Thu Apr 25 2024 Penghe Geng <pgeng@nvidia.com> - 2.0.28
- Secure NIC Mode: Prevent running simultaneously on both bmc and host

* Fri Apr 12 2024 Penghe Geng <pgeng@nvidia.com> - 2.0.27
- bfb-install: Fix incorrect IP address resolution for multi-hop routing

* Fri Apr 12 2024 Liming Sun <limings@nvidia.com> - 2.0.26
- rshim_pcie: set PCIE bit in scratchpad6
- Revert semantics of --reverse-nc

* Fri Apr 05 2024 Liming Sun <limings@nvidia.com> - 2.0.25
- Avoid a race of rshim ownership during bfb push

* Thu Apr 04 2024 Liming Sun <limings@nvidia.com> - 2.0.24
- DROP_MODE: sync-up the Rx FIFO when clearing DROP_MODE

* Tue Apr 02 2024 Liming Sun <limings@nvidia.com> - 2.0.23
- Add some robust fixes for the DROP_MODE

* Fri Mar 22 2024 Penghe Geng <pgeng@nvidia.com> - 2.0.22
- bfb-install: add support for remote rshim update; add speed optimizations

* Tue Mar 19 2024 Penghe Geng <pgeng@nvidia.com> - 2.0.21
- rshim_pci: output Secure NIC mode status in misc file

* Fri Feb 16 2024 Liming Sun <limings@nvidia.com> - 2.0.20
- rshim_pci: adjust delay time for nic_fw reset
- bfb-install: Exit on "Linux up"

* Wed Jan 10 2024 Liming Sun <limings@nvidia.com> - 2.0.19
- Fix incorrect console message drop
- Allow runtime debug code for DK cards

* Thu Dec 14 2023 Liming Sun <limings@nvidia.com> - 2.0.18
- Clear scratchpad1 register when setting drop_mode

* Wed Nov 22 2023 Liming Sun <limings@nvidia.com> - 2.0.17
- bfb-install: Fix duplicate output

* Thu Nov 16 2023 Liming Sun <limings@nvidia.com> - 2.0.16
- Remove fuse build dependency

* Tue Nov 14 2023 Liming Sun <limings@nvidia.com> - 2.0.15
- Add BFB completion condition for enhanced NIC mode

* Fri Nov 10 2023 Liming Sun <limings@nvidia.com> - 2.0.14
- Fix 9f19cfb4a75687ae

* Wed Nov 08 2023 Liming Sun <limings@nvidia.com> - 2.0.13
- Several robust fixes
- Add fuse3 support

* Mon Oct 23 2023 Liming Sun <limings@nvidia.com> - 2.0.12
- BF3: Add UPTIME display in seconds

* Tue Sep 26 2023 Liming Sun <limings@nvidia.com> - 2.0.11
- Remove version 0 support for NIC FW_RESET
- bfb-install: Return failure code

* Mon Sep 18 2023 Liming Sun <limings@nvidia.com> - 2.0.10
- Fix interrupt handling for NIC FW_RESET

* Sat Jun 17 2023 Liming Sun <limings@nvidia.com> - 2.0.9
- rshim/usb/bf3: fix timeout logic

* Tue May 16 2023 Liming Sun <limings@nvidia.com> - 2.0.8
- Fix the fall-back logic of direct-mapping

* Thu Mar 30 2023 Liming Sun <limings@nvidia.com> - 2.0.7
- Avoid opening /dev/uio multiple times
- Update common files to dual-license
- Adjust rshim reset delay

* Sun Nov 20 2022 Liming Sun <limings@nvidia.com> - 2.0.6-19
- BF3: Support 4B access for PCIe

* Tue Oct 25 2022 Liming Sun <limings@nvidia.com> - 2.0.6-18
- pcie: fix initialization issue when setting DROP_MODE in rshim.conf

* Thu Oct 20 2022 Liming Sun <limings@nvidia.com> - 2.0.6-17
- pcie: Avoid using cached pci_dev
- rshim_fuse: display misc file even when rshim is not accessible

* Thu Oct 06 2022 Liming Sun <limings@nvidia.com> - 2.0.6-16
- pcie: Support mixed vfio and direct mapping mode

* Thu Sep 29 2022 Liming Sun <limings@nvidia.com> - 2.0.6-15
- Add dependency of libfuse2 for .deb
- rshim-pcie: add a new bad-access code
- Fix a potential NULL pointer access during USB disconnect
- Adjust default boot timeout to 150s

* Tue Aug 16 2022 Liming Sun <limings@nvidia.com> - 2.0.6-14
- Avoid potential race when stopping the rshim process
- Add configuration option to enable/disable PCIe VFIO/UIO
- Fix warnings for compiling on 32-bit BMC
- Mustang rshim usb supports for 4B and 8B transactions

* Sun Jul 17 2022 Liming Sun <limings@nvidia.com> - 2.0.6-13
- BF3: Support 32-bit CR-space access via USB
- Avoid kernel-modules-extra dependency on ctyunos

* Thu Jun 16 2022 Liming Sun <limings@nvidia.com> - 2.0.6-12
- Optimize the rshim_work_fd
- Detect new USB/rshim hot plugin

* Mon May 16 2022 Liming Sun <limings@nvidia.com> - 2.0.6-11
- Avoid kernel crash when unbind rshim from uio

* Mon May 02 2022 Liming Sun <limings@nvidia.com> - 2.0.6-10
- Fix several compiling issues for FreeBSD

* Thu Apr 28 2022 Liming Sun <limings@nvidia.com> - 2.0.6-9
- Use per-device memory-map mode

* Mon Apr 18 2022 Liming Sun <limings@nvidia.com> - 2.0.6-8
- Add interrupt polling for direct mmap() mode
- Fix several coverity warnings

* Thu Apr 07 2022 Liming Sun <limings@nvidia.com> - 2.0.6-7
- Keep intr_fd during rshim_pcie disable/enable
- Mustang: Add support for rshim over pcie and pcie_lf

* Wed Mar 30 2022 Liming Sun <limings@nvidia.com> - 2.0.6-6
- Clear scratchpad1 to 0 before PCI resources are unmapped
- Fallback to UIO if VFIO failed

* Fri Mar 18 2022 Liming Sun <limings@nvidia.com> - 2.0.6-5
- PCIe: Add UIO and IRQ support
- PCIe: Remove 32-bit support

* Mon Feb 28 2022 Liming Sun <limings@nvidia.com> - 2.0.6-4
- VFIO support
- Fix potential race in rshim_work_signal

* Mon Nov 29 2021 Liming Sun <limings@nvidia.com> - 2.0.6-3
- Adjust the defaul value of usb_reset_delay to 5
- Add a delay after USB probe
- Make the reset delay configurable

* Wed Nov 03 2021 Liming Sun <limings@nvidia.com> - 2.0.6-2
- bfb-install: Handle new indications for installation completion
- Clean up some un-needed register definition
- Fix MTU of the tmfifo_net0 interface on FreeBSD
- Several fixes to prevent hypervisor crash
- Refine some BF-2 Rev0 workaround condition

* Wed May 12 2021 Liming Sun <limings@nvidia.com> - 2.0.6-1
- Disable the background timer if no rshim devices
- Setting default path for rshim config file

* Wed Mar 10 2021 Liming Sun <limings@nvidia.com> - 2.0.5-10
- PCIe hotplug support
- Reduce CPU utilization when there is no rshim device

* Wed Jan 27 2021 Liming Sun <limings@nvidia.com> - 2.0.5-9
- Fix potential tmfifo data loss
- Add workaround checking for Bluefield-2 REV-0
- Fix network traffic stop issue when Tx buffer full

* Fri Dec 11 2020 Liming Sun <limings@nvidia.com> - 2.0.5-8
- Don't allow any register access when DROP_MODE is set
- Avoid potential race in rshim_fifo_read

* Wed Dec 09 2020 Liming Sun <limings@nvidia.com> - 2.0.5-7
- Fix potential dead-lock when calling rshim_access_check
- Ignore rshim access checking when global drop mode is enabled
- Fix some secure boot related issue

* Wed Dec 02 2020 Liming Sun <limings@nvidia.com> - 2.0.5-6
- Add some default configuration in rshim.conf
- Change the debug level of Rshim byte access widget timeout
- Add bfb-install script

* Thu Oct 29 2020 Liming Sun <lsun@mellanox.com> - 2.0.5-5
- Check rshim accessibility when re-enabling it
- Enable console output during boot stream pushing
- Add some delay for the pcie_lf probe
- Auto-start rshim service after installation

* Fri Sep 25 2020 Liming Sun <lsun@mellanox.com> - 2.0.5-4
- Some robust fixes for USB rshim
- Fix a typo in pcie mmap

* Mon Aug 17 2020 Liming Sun <lsun@mellanox.com> - 2.0.5-3
- Fix several coverity warnings
- Add workaround to boot Viper rev A0 in LiveFish mode
- Display/configure OPN string for BlueField-2

* Fri Jul 24 2020 Liming Sun <lsun@mellanox.com> - 2.0.5-2
- Add configuration file support
- misc: Display device version / revision ID
- Add service file for FreeBSD

* Tue Jun 16 2020 Liming Sun <lsun@mellanox.com> - 2.0.5-1
- Improve response time to ctrl+c for boot stream
- Fix a rpmbuild issue when make_build is not defined
- Add DROP_MODE configuration in misc file
- Avoid reading the fifo if still booting
- Fix configure issue for FreeBSD 12.1-RELEASE
- Add domain id to the DEV_NAME in the misc file
- Fix the debian copyright format
- Enhance rshim_pcie_enable function

* Tue Apr 21 2020 Liming Sun <lsun@mellanox.com> - 2.0.4-1
- Update .spec file according to review comments
- Fix the 'KillMode' in rshim.service
- Support process termination by SIGTERM
- Fix some compiling warnings and configure issue for FreeBSD
- Fix a read()/write() issue in rshim_pcie.c caused by optimization

* Tue Apr 14 2020 Liming Sun <lsun@mellanox.com> - 2.0.3-1
- Enable pci device during probing
- Map the pci resource0 file instead of /dev/mem
- Add copyright header in bootstrap.sh
- Add 'Requires' tag check in the rpm .spec for kernel-modules-extra
- Fix the 'rshim --version' output

* Thu Apr 09 2020 Liming Sun <lsun@mellanox.com> - 2.0.2-1
- Remove unnecessary dependency in .spec and use make_build
- Add package build for debian/ubuntu
- Fix some format in the man page
- Add check for syslog headers

* Mon Mar 23 2020 Liming Sun <lsun@mellanox.com> - 2.0.1-1
- Rename bfrshim to rshim
- Remove rshim.spec since it's auto-generated from rshim.spec.in
- Fix some warnings reported by coverity
- Add file rhel/rshim.spec.in for fedora
- Move rshim to sbin and move man page to man8

* Fri Mar 13 2020 Liming Sun <lsun@mellanox.com> - 2.0-1
- Update the spec file according to fedora packaging-guidelines

* Mon Dec 16 2019 Liming Sun <lsun@mellanox.com>
- Initial packaging
