Name:           azure-vm-utils
Version:        0.7.0
Release:        1%{?dist}
Summary:        Core utilities and configuration for Linux VMs on Azure
 
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/Azure/%{name}
Source:         %{url}/archive/v%{version}/%{name}-v%{version}.tar.gz
 
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  pkgconfig(libudev)
BuildRequires:  json-c-devel
BuildRequires:  libcmocka-devel
BuildRequires:  systemd-bootstrap-rpm-macros
Requires:       util-linux
Recommends:     mdadm
 
Provides:       azure-nvme-utils = %{version}-%{release}
Obsoletes:      azure-nvme-utils < 0.1.3-3
 
 
%post
%systemd_post azure-ephemeral-disk-setup.service
 
%preun
%systemd_preun azure-ephemeral-disk-setup.service
 
%postun
%systemd_postun azure-ephemeral-disk-setup.service
 
 
%description
This package provides a home for core utilities, udev rules and other
configuration to support Linux VMs on Azure.
 
%prep
%autosetup -n %{name}-%{version}
 
%build
%cmake -DVERSION="%{version}-%{release}" -DAZURE_NVME_ID_INSTALL_DIR="%{_bindir}"
%cmake_build

%install
%cmake_install
install -D -m 0755 initramfs/dracut/modules.d/97azure-disk/module-setup.sh %{buildroot}%{_prefix}/lib/dracut/modules.d/97azure-disk/module-setup.sh
install -D -m 0755 initramfs/dracut/modules.d/97azure-unmanaged-sriov/module-setup.sh %{buildroot}%{_prefix}/lib/dracut/modules.d/97azure-unmanaged-sriov/module-setup.sh
rm %{buildroot}%{_bindir}/azure-vm-utils-selftest
rm %{buildroot}%{_mandir}/man8/azure-vm-utils-selftest.8
 
%check
%ctest

%files
%defattr(-,root,root,-)
%dir %{_prefix}/lib/dracut/modules.d/97azure-disk
%{_prefix}/lib/dracut/modules.d/97azure-disk/module-setup.sh
%{_prefix}/lib/dracut/modules.d/97azure-unmanaged-sriov/module-setup.sh
%{_prefix}/lib/systemd/network/01-azure-unmanaged-sriov.network
%{_unitdir}/azure-ephemeral-disk-setup.service
%{_udevrulesdir}/10-azure-unmanaged-sriov.rules
%{_udevrulesdir}/80-azure-disk.rules
%{_bindir}/azure-ephemeral-disk-setup
%{_bindir}/azure-nvme-id
%{_mandir}/man8/azure-ephemeral-disk-setup.8.*
%{_mandir}/man8/azure-nvme-id.8.*
%config(noreplace) %{_sysconfdir}/azure-ephemeral-disk-setup.conf
 
%changelog
* Tue Feb 17 2025 Mayank Singh <mayansingh@microsoft.com> - 0.7.0-1
- Original version for Azure Linux.
- License verified.
- Initial package.


