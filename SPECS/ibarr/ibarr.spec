Name:           ibarr
Version:        0.1.5
Release:        1%{?dist}
Summary:        Nvidia address and route userspace resolution services for Infiniband
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.1.0/SOURCES/mlnx_ofed/MLNX_OFED_SRC-25.07-0.9.7.0.tgz
Source0:        %{_distro_sources_url}/%{name}-%{version}.tar.gz
Group:		Applications/System
License:	(GPL-2.0 WITH Linux-syscall-note) OR BSD-2-Clause
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
* Tue Oct 04 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.1.5-1
- Upgrade version to 0.1.5.
- Update source path
* Mon Sep 15 2025 Elaheh Dehghani <edehghani@microsoft.com> - 0.1.3-3
- Enable ARM64 build by removing ExclusiveArch
* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com> - 0.1.3-2
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
