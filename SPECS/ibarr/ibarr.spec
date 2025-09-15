Name:		ibarr
Version:	0.1.3
Release:        2%{?dist}
Summary:	Nvidia		 address and route userspace resolution services for Infiniband
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://linux.mellanox.com/public/repo/mlnx_ofed/24.10-0.7.0.0/SRPMS/ibarr-0.1.3.tar.gz#/%{name}-%{version}.tar.gz
Group:		Applications/System
License:	(GPL-2.0 WITH Linux-syscall-note) OR BSD-2-Clause
ExclusiveArch:   x86_64

BuildRequires:	cmake
BuildRequires:	gcc
BuildRequires:	libnl3-devel
BuildRequires:	rdma-core-devel

# The SLES cmake macros do more than the RHEL ones, and have an extra
# cmake_install with a 'cd build' inside.
%if %{undefined cmake_install}
%global cmake_install %make_install
%endif
%if %{undefined cmake_build}
  %if %{defined make_jobs}
    # SLES12
    %global cmake_build %make_jobs
  %else
    # RHEL < 9, Fedora < ??
    %global cmake_build %make_build
  %endif
%endif

%description
a userspace application that interacts over NetLink with the Linux RDMA
subsystem and provides 2 services: ip2gid (address resolution) and gid2lid
(PathRecord resolution).

%prep
%setup -q

%build
%cmake
%cmake_build

%install
%cmake_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README.md
%license COPYING.BSD_MIT
%{_bindir}/ibarr
# FIXME: should be in the standard directory, under _prefix.
/lib/systemd/system/%{name}.service

%changelog
* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com>
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
