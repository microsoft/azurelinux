%define kernel_full_version 5.15.45.1-2%{?dist}

Summary:        Set of livepatches for kernel %{kernel_full_version}
Name:           livepatch-%{kernel_full_version}
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/microsoft/CBL-Mariner

BuildRequires:  binutils
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  rpm-build
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  kernel-debuginfo = %{kernel_full_version}
BuildRequires:  kernel-headers = %{kernel_full_version}
BuildRequires:  kpatch-build
BuildRequires:  audit-devel
BuildRequires:  bash
BuildRequires:  bc
BuildRequires:  diffutils
BuildRequires:  dwarves
BuildRequires:  elfutils-libelf-devel
BuildRequires:  glib-devel
BuildRequires:  kbd
BuildRequires:  kmod-devel
BuildRequires:  libdnet-devel
BuildRequires:  libmspack-devel
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  procps-ng-devel
BuildRequires:  python3-devel

Requires:       kpatch

%description
A set of kernel livepatches addressing CVEs present in Mariner's
kernel version %{kernel_full_version}.

%prep
%autopatch -p1

%build

%install

%post
%preun

%files

%changelog
* Wed Jun 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-1
- Original version for CBL-Mariner.
- License verified.
