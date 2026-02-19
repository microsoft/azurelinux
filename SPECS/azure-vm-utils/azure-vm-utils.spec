%global dracutmodulesdir %(pkg-config --variable=dracutmodulesdir dracut || echo '/usr/lib/dracut/modules.d')

Name:           azure-vm-utils
Version:        0.7.0
Release:        1%{?dist}
Summary:        Utilities and udev rules for Linux on Azure
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        MIT
URL:            https://github.com/Azure/%{name}
Source0:        https://github.com/Azure/azure-vm-utils/archive/refs/tags/v0.7.0.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  binutils
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  json-c-devel
BuildRequires:  kernel-headers
BuildRequires:  libcmocka-devel
BuildRequires:  make
Requires:       mdadm
Requires:       util-linux

%description
A collection of utilities and udev rules to make the most of the Linux
experience on Azure.

%package selftest
Summary:        Self-test script for Azure VM Utils
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description selftest
This package contains the self-test script for the Azure VM Utils package.

%prep
%autosetup

%build
%cmake -DVERSION="%{version}-%{release}"
%cmake_build

%install
%cmake_install
mkdir -p %{buildroot}%{dracutmodulesdir}
cp -a initramfs/dracut/modules.d/* %{buildroot}%{dracutmodulesdir}

%check
%ctest

%files
%{_libdir}/dracut/modules.d/97azure-disk/module-setup.sh
%{_libdir}/dracut/modules.d/97azure-unmanaged-sriov/module-setup.sh
%{_libdir}/systemd/network/01-azure-unmanaged-sriov.network
%{_libdir}/systemd/system/azure-ephemeral-disk-setup.service
%{_libdir}/udev/rules.d/10-azure-unmanaged-sriov.rules
%{_libdir}/udev/rules.d/80-azure-disk.rules
%{_sbindir}/azure-ephemeral-disk-setup
%{_sbindir}/azure-nvme-id
%{_mandir}/man8/azure-ephemeral-disk-setup.8.gz
%{_mandir}/man8/azure-nvme-id.8.gz
%{_sysconfdir}/azure-ephemeral-disk-setup.conf

%files selftest
%{_sbindir}/azure-vm-utils-selftest
%{_mandir}/man8/azure-vm-utils-selftest.8.gz

%changelog
* Thu Feb 19 2026 Sumit Jena (HCL Technologies Ltd) - 1.14.0-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
