Name:           azure-vm-utils
Version:        0.4.0
Release:        1%{?dist}
Summary:        Core utilities and configuration for Linux VMs on Azure

License:        MIT
URL:            https://github.com/Azure/%{name}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  binutils
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  kernel-headers
BuildRequires:  make
BuildRequires:  pkgconfig(libudev)

%description
This package provides a home for core utilities, udev rules and other
configuration to support Linux VMs on Azure.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -DVERSION="%{version}-%{release}"
%cmake_build

%install
%cmake_install
install -D -m 0755 initramfs/dracut/modules.d/97azure-disk/module-setup.sh %{buildroot}%{_prefix}/lib/dracut/modules.d/97azure-disk/module-setup.sh

%check
%ctest

%files
%defattr(-,root,root,-)
%{_mandir}/man8/azure-nvme-id.8.gz
%dir %{_prefix}/lib/dracut/modules.d/97azure-disk
%{_prefix}/lib/dracut/modules.d/97azure-disk/module-setup.sh
%{_sbindir}/azure-nvme-id
%{_udevrulesdir}/80-azure-disk.rules

%changelog
* Wed Oct 16 2024 Chri Patterson <cpatterson@microsoft.com> - 0.4.0-1
- Rename azure-nvme-utils -> azure-vm-utils to match upstream change.
- Upgrade to v0.4.0.

* Tue Sep 03 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 0.1.1-2
- Add missing Vendor and Distribution tags.

* Mon Mar 18 2024 Chris Patterson <cpatterson@microsoft.com> - 0.1.1-1
- Original version for Azure Linux.
- License verified.
- Initial package.
