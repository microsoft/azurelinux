# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global upstream_name ibarr

%if 0%{?_ver:1}
%define ver 2604.0.0
%else
%define ver 0.1.3
%endif

%if 0%{?_rel:1}
%define rel 1
%else
%define rel 1
%endif

# Workaround for cmake-rpm-macros >= 3.27.9-8 on ctyunos25.07: the cmake
# macro configures in-source (no -B) but cmake_build still expects a build
# subdirectory at __cmake_builddir (e.g. x86_64-ctyunos-linux-gnu) which
# is never created. Force both macros to use "." so they agree.
%if "%{?_vendor}" == "ctyunos"
%global __cmake_builddir .
%endif

Name:		ibarr
Version: 2604.0.0
Release: 1%{?dist}
Summary:	Nvidia address and route userspace resolution services for Infiniband
Source0:	MLNX_OFED_SRC-26.04-0.8.5.0.tgz
Source6000:	MLNX_OFED_SRC-26.04-0.8.5.0.tgz
BuildRequires:	cmake gcc libnl3-devel rdma-core-ofed-devel

Group:		Applications/System
License:	(GPL-2.0 WITH Linux-syscall-note) OR BSD-2-Clause

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
%if %{defined kylin}
  %if %{defined cmake_conf}
    %global cmake %cmake_conf
  %endif
%endif

%description
a userspace application that interacts over NetLink with the Linux RDMA
subsystem and provides 2 services: ip2gid (address resolution) and gid2lid
(PathRecord resolution).

%prep
tar -xf %{SOURCE6000}
_ibarr_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/ibarr-%{version}-*.src.rpm' -print -quit)
if [ -z "$_ibarr_srpm" ]; then
  echo "ERROR: ibarr source RPM not found inside %{SOURCE6000}" >&2
  exit 1
fi
rpm2cpio "$_ibarr_srpm" | cpio -idm './ibarr-%{version}.tar.gz'
rm -rf MLNX_OFED_SRC-*
tar -xf ibarr-%{version}.tar.gz
%setup -q -T -D -n %{upstream_name}-%{version}

%build
%cmake
%cmake_build

%install
%cmake_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README.md
%{_bindir}/ibarr
# FIXME: should be in the standard directory, under _prefix.
/lib/systemd/system/%{upstream_name}.service

%changelog

* Mon May 04 2026 root - 2604.0.0-1
Automated build 1
