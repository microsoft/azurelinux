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

# snapshot version
%global snapver .20240616git
# use hardened build
%global _hardened_build 1
# udev rules prefix
%global udev_prefix 70

Name:     hyperv-daemons
Version:  6.10
Release:  %autorelease
Summary:  Hyper-V daemons suite

License:  GPL-2.0-only
URL:      http://www.kernel.org

# Source files obtained from kernel upstream 6.10-rc4 (6ba59ff4227927d3a8530fc2973b80e94b54d58f)
# git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
Source0:  tools-hv-6ba59ff42279.tar.gz
Source1:  COPYING

# HYPERV KVP DAEMON
Source5:  hypervkvpd.service
Source6:  hypervkvp.rules

# HYPERV VSS DAEMON
Source101:  hypervvssd.service
Source102:  hypervvss.rules

# HYPERV FCOPY DAEMON
Source201:  hypervfcopyd.service
Source202:  hypervfcopy.rules

# Hyper-V is available only on x86 and aarch64 architectures
# The base empty (a.k.a. virtual) package can not be noarch
# due to http://www.rpm.org/ticket/78
ExclusiveArch:  i686 x86_64 aarch64

Requires:       hypervkvpd = %{version}-%{release}
Requires:       hypervvssd = %{version}-%{release}
# Fcopy UIO driver is x86 only
%ifarch i686 x86_64
Requires:       hypervfcopyd = %{version}-%{release}
%else
Obsoletes:      hypervfcopyd <= %{version}-%{release}
%endif
BuildRequires:  gcc

%description
Suite of daemons that are needed when Linux guest
is running on Windows Host with Hyper-V.


%package -n hypervkvpd
Summary: Hyper-V key value pair (KVP) daemon
Requires: %{name}-license = %{version}-%{release}
BuildRequires: systemd, kernel-headers
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description -n hypervkvpd
Hypervkvpd is an implementation of Hyper-V key value pair (KVP)
functionality for Linux. The daemon first registers with the
kernel driver. After this is done it collects information
requested by Windows Host about the Linux Guest. It also supports
IP injection functionality on the Guest.


%package -n hypervvssd
Summary: Hyper-V VSS daemon
Requires: %{name}-license = %{version}-%{release}
BuildRequires: systemd, kernel-headers
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description -n hypervvssd
Hypervvssd is an implementation of Hyper-V VSS functionality
for Linux. The daemon is used for host initiated guest snapshot
on Hyper-V hypervisor. The daemon first registers with the
kernel driver. After this is done it waits for instructions
from Windows Host if to "freeze" or "thaw" the filesystem
on the Linux Guest.

# Fcopy UIO driver is x86 only
%ifarch i686 x86_64
%package -n hypervfcopyd
Summary: Hyper-V FCOPY daemon
Requires: %{name}-license = %{version}-%{release}
BuildRequires: systemd, kernel-headers
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description -n hypervfcopyd
Hypervfcopyd is an implementation of file copy service functionality
for Linux Guest running on Hyper-V. The daemon enables host to copy
a file (over VMBUS) into the Linux Guest. The daemon first registers
with the kernel driver. After this is done it waits for instructions
from Windows Host.
%endif

%package license
Summary:    License of the Hyper-V daemons suite
BuildArch:  noarch

%description license
Contains license of the Hyper-V daemons suite.

%package -n hyperv-tools
Summary:    Tools for Hyper-V guests
BuildArch:  noarch

%description -n hyperv-tools
Contains tools and scripts useful for Hyper-V guests.

%prep
%setup -q -n tools/hv
cp -pvL %{SOURCE1} COPYING

%build
%make_build

%install
%make_install sbindir=%{_sbindir}

# Systemd unit file
mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE101} %{buildroot}%{_unitdir}
%ifarch i686 x86_64
install -p -m 0644 %{SOURCE201} %{buildroot}%{_unitdir}
%endif
# Udev rules
mkdir -p %{buildroot}%{_udevrulesdir}
install -p -m 0644 %{SOURCE6} %{buildroot}%{_udevrulesdir}/%{udev_prefix}-hypervkvp.rules
install -p -m 0644 %{SOURCE102} %{buildroot}%{_udevrulesdir}/%{udev_prefix}-hypervvss.rules
%ifarch i686 x86_64
install -p -m 0644 %{SOURCE202} %{buildroot}%{_udevrulesdir}/%{udev_prefix}-hypervfcopy.rules
%endif
# Shell scripts for the KVP daemon
mkdir -p %{buildroot}%{_libexecdir}/hypervkvpd
install -p -m 0755 hv_get_dhcp_info.sh %{buildroot}%{_libexecdir}/hypervkvpd/hv_get_dhcp_info
install -p -m 0755 hv_get_dns_info.sh %{buildroot}%{_libexecdir}/hypervkvpd/hv_get_dns_info
install -p -m 0755 hv_set_ifconfig.sh %{buildroot}%{_libexecdir}/hypervkvpd/hv_set_ifconfig
# Directory for pool files
mkdir -p %{buildroot}%{_sharedstatedir}/hyperv

sed -i 's,#!/usr/bin/env python,#!/usr/bin/python3,' %{buildroot}%{_sbindir}/lsvmbus

%post -n hypervkvpd
if [ $1 -gt 1 ] ; then
	# Upgrade
	systemctl --no-reload disable hypervkvpd.service >/dev/null 2>&1 || :
fi

%preun -n hypervkvpd
%systemd_preun hypervkvpd.service

%postun -n hypervkvpd
# hypervkvpd daemon does NOT support restarting (driver, neither)
%systemd_postun hypervkvpd.service
# If removing the package, delete %%{_sharedstatedir}/hyperv directory
if [ "$1" -eq "0" ] ; then
    rm -rf %{_sharedstatedir}/hyperv || :
fi


%post -n hypervvssd
if [ $1 -gt 1 ] ; then
	# Upgrade
	systemctl --no-reload disable hypervvssd.service >/dev/null 2>&1 || :
fi

%postun -n hypervvssd
%systemd_postun hypervvssd.service

%preun -n hypervvssd
%systemd_preun hypervvssd.service

%ifarch i686 x86_64
%post -n hypervfcopyd
%systemd_postun hypervfcopyd.service

%postun -n hypervfcopyd
%systemd_postun hypervfcopyd.service

%preun -n hypervfcopyd
%systemd_preun hypervfcopyd.service
%endif

%files
# the base package does not contain any files.

%files -n hypervkvpd
%{_sbindir}/hv_kvp_daemon
%{_unitdir}/hypervkvpd.service
%{_udevrulesdir}/%{udev_prefix}-hypervkvp.rules
%dir %{_libexecdir}/hypervkvpd
%{_libexecdir}/hypervkvpd/*
%dir %{_sharedstatedir}/hyperv

%files -n hypervvssd
%{_sbindir}/hv_vss_daemon
%{_unitdir}/hypervvssd.service
%{_udevrulesdir}/%{udev_prefix}-hypervvss.rules

%ifarch i686 x86_64
%files -n hypervfcopyd
%{_sbindir}/hv_fcopy_uio_daemon
%{_unitdir}/hypervfcopyd.service
%{_udevrulesdir}/%{udev_prefix}-hypervfcopy.rules
%endif

%files license
%doc COPYING

%files -n hyperv-tools
%{_sbindir}/lsvmbus

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 6.10-3
- Latest state for hyperv-daemons

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 23 2025 Vitaly Kuznetsov <vkuznets@redhat.com> - 6.10-1
- Use Linux kernel version instead of '0'

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.49.20240616git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.48.20240616git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 28 2024 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.47.20240616git
- Particularize hypervfcopyd service requirements

* Tue Jun 25 2024 Adam Williamson <awilliam@redhat.com> - 0-0.46.20240616git
- Fix hypervfcopyd dep on aarch64

* Thu Jun 20 2024 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.45.20240616git
- Update to 6.10-rc4

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.44.20220731git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.43.20220731git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.42.20220731git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.41.20220731git
- Switch to SPDX identifiers for the license field

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.40.20220731git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 02 2022 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.39.20220731git
- Enable aarch64 build (#2111394)
- Fix typos in shell scripts

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.38.20220710git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.37.20220710git
- Update to 5.19-rc6

* Fri Jul 01 2022 Chris Patterson <cpatterson@microsoft.com> - 0-0.37.20190303git
- Only start kvpd under Hyper-V
- Minimize dependencies for kvpd to ensure it starts before cloud-init

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.36.20190303git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.35.20190303git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.34.20190303git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.33.20190303git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.32.20190303git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Tom Stellard <tstellar@redhat.com> - 0-0.31.20190303git
- Use __cc macro instead of hard-coding gcc

* Fri Nov 08 2019 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.30.20190303git
- Rebase to 5.4-rc6
- Add IgnoreOnIsolate to systemd units

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.29.20190303git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 15 2019 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.28.20190303git
- Rebase to 5.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.27.20180415git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.26.20180415git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 11 2018 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.25.20180415git
- Switch lsvmbus to Python3

* Thu Apr 26 2018 Tomas Hozza <thozza@redhat.com> - 0-0.24.20180415git
- Added gcc as an explicit BuildRequires

* Thu Apr 19 2018 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.23.20180415git
- Rebase to 4.17-rc1

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.22.20170105git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.21.20170105git
- Rebase to 4.15-rc2, drop fedora patches as changes are upstream
- Start kvpd after network.target

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.20.20170105git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.19.20170105git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.18.20170105git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.17.20160728git
- Use '-gt' instead of '>' to do the right comparison (#1412033)

* Thu Jan 05 2017 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.16.20160728git
- Rebase to 4.9
- hyperv-tools subpackage added

* Thu Jul 28 2016 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.15.20160728git
- Rebase to 4.8-rc0 (20160728 git snapshot)
- Disable services and remove ConditionVirtualization, multi-user.target
  dependencies switching to udev-only activation (#1331577)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.14.20150702git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.13.20150702git
- Add udev rules to properly restart services (#1195029)
- Spec cleanup

* Thu Jul 02 2015 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.12.20150702git
- Rebase to 4.2-rc0 (20150702 git snapshot)
- Switch to new chardev-based communication layer (#1195029)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.11.20150108git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 08 2015 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.10.20150108git
- Rebase to 3.19-rc3 (20150108 git snapshot)
- Drop 'nodaemon' patches, use newly introduced '-n' option

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.9.20140714git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 14 2014 Tomas Hozza <thozza@redhat.com> - 0-0.8.20140714git
- Update the File copy daemon to the latest git snapshot
- Fix hyperfcopyd.service to check for /dev/vmbus/hv_fcopy

* Wed Jun 11 2014 Tomas Hozza <thozza@redhat.com> - 0-0.7.20140611git
- Fix FTBFS (#1106781)
- Use kernel-headers instead of kernel-devel for building
- package new Hyper-V fcopy daemon as hypervfcopyd sub-package

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.6.20140219git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 19 2014 Tomas Hozza <thozza@redhat.com> - 0-0.5.20140219git
- rebase to the latest git snapshot next-20140219
  - KVP, VSS: removed inclusion of linux/types.h
  - VSS: Ignore VFAT mounts during freeze operation

* Fri Jan 10 2014 Tomas Hozza <thozza@redhat.com> - 0-0.4.20131022git
- provide 'hyperv-daemons' package for convenient installation of all daemons

* Tue Oct 22 2013 Tomas Hozza <thozza@redhat.com> - 0-0.3.20131022git
- rebase to the latest git snapshot next-20130927 (obtained 2013-10-22)
  - KVP, VSS: daemon use single buffer for send/recv
  - KVP: FQDN is obtained on start and cached

* Fri Sep 20 2013 Tomas Hozza <thozza@redhat.com> - 0-0.2.20130826git
- Use 'hypervkvpd' directory in libexec for KVP daemon scripts (#1010268)
- daemons are now WantedBy multi-user.target instead of basic.target (#1010260)

* Mon Aug 26 2013 Tomas Hozza <thozza@redhat.com> - 0-0.1.20130826git
- Initial package

## END: Generated by rpmautospec
