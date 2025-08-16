Summary:        Linux API header files
Name:           kernel-hwe-headers
Version:        6.12.40.1
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
Source0:        https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/hwe/%{version}.tar.gz#/kernel-hwe-%{version}.tar.gz

%description
The Linux API Headers expose the kernel's API for use by downstream builds.

%prep
%setup -q -n CBL-Mariner-Linux-Kernel-rolling-lts-hwe-%{version}

%build
make mrproper
make headers

%install
find usr/include* \( -name ".*" -o -name "Makefile" \) -delete

mkdir -p /%{buildroot}%{_includedir}
cp -rv usr/include/* /%{buildroot}%{_includedir}

%files
%defattr(-,root,root)
%license COPYING
%{_includedir}/*

%changelog
* Fri Aug 15 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 6.12.40.1-1
- Original version for Azure Linux
- License verified
