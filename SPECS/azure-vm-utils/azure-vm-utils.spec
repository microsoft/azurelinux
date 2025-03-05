Name:           azure-vm-utils
Version:        0.5.1
Release:        1%{?dist}
Summary:        Core utilities and configuration for Linux VMs on Azure

License:        MIT
URL:            https://github.com/Azure/%{name}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  binutils
BuildRequires:  cmake
BuildRequires:  dracut
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  json-c-devel
BuildRequires:  kernel-headers
BuildRequires:  libcmocka-devel
BuildRequires:  make
BuildRequires:  pkgconfig(libudev)

%description
This package provides a home for core utilities, udev rules and other
configuration to support Linux VMs on Azure.

Provides:       azure-nvme-utils = %{version}-%{release}
Obsoletes:      azure-nvme-utils < %{version}-%{release}

%package test
Summary:        Self-test script for Azure VM Utils
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description test
This package provides self-tests to validate azure-vm-utils is functioning
as expected (correct symlinks, azure-nvme-id outputs, etc.).  It is primarily
intended to help developers and package maintainers to vet functionality in any
environment.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -DVERSION="%{version}-%{release}"
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%defattr(-,root,root,-)
%{_mandir}/man8/azure-nvme-id.8.gz
%dir %{_prefix}/lib/dracut/modules.d/97azure-disk
%{_prefix}/lib/dracut/modules.d/97azure-disk/module-setup.sh
%{_sbindir}/azure-nvme-id
%{_udevrulesdir}/80-azure-disk.rules

%files test
%{_sbindir}/azure-vm-utils-selftest
%{_mandir}/man8/azure-vm-utils-selftest.8.gz


%changelog
* Wed Mar 05 2025 Chris Patterson <cpatterson@microsoft.com> - 0.5.1-1
- Rename azure-nvme-utils -> azure-vm-utils to match upstream change.
- Upgrade to v0.5.1.
- Add -test package.

* Tue Sep 03 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 0.1.1-2
- Add missing Vendor and Distribution tags.

* Mon Mar 18 2024 Chris Patterson <cpatterson@microsoft.com> - 0.1.1-1
- Original version for Azure Linux.
- License verified.
- Initial package.
